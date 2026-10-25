#!/usr/bin/env python3
"""Generation tests for tbengy's synthesis backends (vivado / f4pga).

Plain-python, subprocess-driven: runnable directly
(`python3 tests/test_generation.py`) or under pytest
(`pytest tests/test_generation.py`). No third-party dependencies.

Covered:
  a) Default (vivado) generation for an SV+board project still emits
     scripts/synth.tcl and the Vivado `synth:` Makefile target.
  b) `--backend f4pga` generation emits NO synth.tcl, emits
     scripts/f4pga.mk + synth/<module>.sdc, and the Makefile delegates
     both synth and program to f4pga.mk (single source of truth for
     the bitstream path / openFPGALoader board), with no
     `vivado -mode batch` anywhere in the Makefile.
  c) Backend-neutral files (RTL, testbench, board XDC) are
     byte-identical between the default and f4pga generations.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TBENGY = REPO_ROOT / "tbengy.py"
MODULE = "led_blink"
PART = "xc7z010clg400-1"


def _generate(dest_dir, extra_args, module=MODULE, board="zybo",
              part=PART, env=None):
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(TBENGY),
           "-m", module, "-t", "sv", "-b", board, "-f", part,
           "-d", str(dest)] + list(extra_args)
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True)
    assert proc.returncode == 0, "tbengy failed:\n" + proc.stdout
    proj = dest / module
    assert proj.is_dir(), "project dir not generated:\n" + proc.stdout
    return proj, proc.stdout


def test_default_backend_is_vivado():
    with tempfile.TemporaryDirectory() as tmp:
        proj, _ = _generate(tmp, [])
        synth_tcl = proj / "scripts" / "synth.tcl"
        assert synth_tcl.is_file(), "default generation must emit synth.tcl"
        assert "set_part " + PART in synth_tcl.read_text()
        makefile = (proj / "scripts" / "Makefile").read_text()
        assert "vivado -mode batch" in makefile
        assert "synth.tcl" in makefile
        assert not (proj / "scripts" / "f4pga.mk").exists(), \
            "default generation must not emit f4pga.mk"
        assert "f4pga.mk" not in (proj / ".gitignore").read_text(), \
            "default project .gitignore must not mention f4pga.mk"


def test_f4pga_backend():
    with tempfile.TemporaryDirectory() as tmp:
        proj, _ = _generate(tmp, ["--backend", "f4pga"])
        assert not (proj / "scripts" / "synth.tcl").exists(), \
            "f4pga generation must not emit synth.tcl"
        flow = proj / "scripts" / "f4pga.mk"
        assert flow.is_file(), "f4pga generation must emit scripts/f4pga.mk"
        flow_text = flow.read_text()
        for wrapper in ("symbiflow_synth", "symbiflow_pack",
                        "symbiflow_place", "symbiflow_route",
                        "symbiflow_write_fasm", "symbiflow_write_bitstream"):
            assert wrapper in flow_text, "f4pga.mk missing " + wrapper
        assert PART in flow_text
        assert "xc7z010_test" in flow_text
        assert "zynq7" in flow_text
        sdc = proj / "synth" / (MODULE + ".sdc")
        assert sdc.is_file(), "f4pga generation must emit synth/<module>.sdc"
        sdc_text = sdc.read_text()
        assert "create_clock" in sdc_text
        assert "8.000" in sdc_text, "125 MHz Zybo clock -> 8.000 ns period"
        assert "CLK_PERIOD_NS" not in flow_text, \
            "clock period must live in the .sdc only, not as a dead f4pga.mk var"
        assert "openFPGALoader" in flow_text, \
            "program target (openFPGALoader) must live in f4pga.mk"
        assert "$(BUILD_DIR)/$(TOP).bit" in flow_text
        assert "OFL_BOARD" in flow_text and "zybo_z7_10" in flow_text
        makefile = (proj / "scripts" / "Makefile").read_text()
        assert "-f f4pga.mk all" in makefile, "Makefile synth must delegate to f4pga.mk"
        assert "-f f4pga.mk program" in makefile, \
            "Makefile program must delegate to f4pga.mk (one bitstream path)"
        assert "\n\topenFPGALoader" not in makefile, \
            "no Makefile recipe may invoke openFPGALoader directly (f4pga.mk only)"
        assert "vivado -mode batch" not in makefile
        readme = (proj / "README.md").read_text()
        assert "EXPERIMENTAL" in readme and "PL-only" in readme
        gitignore = (proj / ".gitignore").read_text()
        assert "!f4pga.mk" in gitignore and "!*.sdc" in gitignore, \
            "f4pga source files must be whitelisted in the project .gitignore"


def test_backend_neutral_files_identical():
    with tempfile.TemporaryDirectory() as tmp:
        default_proj, _ = _generate(str(Path(tmp) / "default"), [])
        f4pga_proj, _ = _generate(str(Path(tmp) / "f4pga"),
                                  ["--backend", "f4pga"])
        for rel in ("rtl/" + MODULE + ".sv",
                    "sim/tb/" + MODULE + "_tb.sv",
                    "synth/Zybo-Master.xdc"):
            a = (default_proj / rel).read_bytes()
            b = (f4pga_proj / rel).read_bytes()
            assert a == b, rel + " differs between backends"


def test_probe_lists_all_flow_tools():
    # With an empty PATH, every tool the generated flow invokes must be
    # named in tbengy's non-fatal F4PGA probe warning -- the probe list
    # and the flow's tool list must not drift apart.
    import os
    with tempfile.TemporaryDirectory() as tmp:
        empty_bin = Path(tmp) / "emptybin"
        empty_bin.mkdir()
        env = dict(os.environ)
        env["PATH"] = str(empty_bin)
        _, out = _generate(str(Path(tmp) / "gen"), ["--backend", "f4pga"],
                           env=env)
        assert "F4PGA tool(s) not found" in out
        for tool in ("symbiflow_synth", "symbiflow_pack", "symbiflow_place",
                     "symbiflow_route", "symbiflow_write_fasm",
                     "symbiflow_write_bitstream", "openFPGALoader"):
            assert tool in out, "probe warning does not name " + tool


def test_second_module_and_board_alignment():
    # A different module name and a non-Zybo board: generated file names,
    # f4pga.mk variables and the copied XDC must all track the inputs.
    with tempfile.TemporaryDirectory() as tmp:
        proj, _ = _generate(str(Path(tmp) / "a"), ["--backend", "f4pga"],
                            module="blink2")
        flow_text = (proj / "scripts" / "f4pga.mk").read_text()
        assert "TOP              ?= blink2" in flow_text
        assert (proj / "synth" / "blink2.sdc").is_file()
        proj2, out2 = _generate(str(Path(tmp) / "b"), ["--backend", "f4pga"],
                                module="basysblink", board="basys3",
                                part="xc7a35tcsg324-1")
        assert "tuned for xc7z010" in out2, "non-xc7z010 part must warn"
        flow2 = (proj2 / "scripts" / "f4pga.mk").read_text()
        assert "XDC_FILE    ?= Basys-3-Master.xdc" in flow2
        assert (proj2 / "synth" / "Basys-3-Master.xdc").is_file()
        sdc2 = (proj2 / "synth" / "basysblink.sdc").read_text()
        assert "10.000" in sdc2, "Basys3 100 MHz clock -> 10.000 ns period"


if __name__ == "__main__":
    tests = [(name, fn) for name, fn in sorted(globals().items())
             if name.startswith("test_") and callable(fn)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("PASS " + name)
        except AssertionError as exc:
            failed += 1
            print("FAIL " + name + ": " + str(exc))
    print("%d/%d tests passed" % (len(tests) - failed, len(tests)))
    sys.exit(1 if failed else 0)
