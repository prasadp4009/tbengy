#!/usr/bin/env python3
"""Generation tests for tbengy's synthesis backends (vivado / f4pga).

Plain-python, subprocess-driven: runnable directly
(`python3 tests/test_generation.py`) or under pytest
(`pytest tests/test_generation.py`). No third-party dependencies.

Covered:
  a) Default (vivado) generation for an SV+board project still emits
     scripts/synth.tcl and the Vivado `synth:` Makefile target.
  b) `--backend f4pga` generation emits NO synth.tcl, emits
     scripts/f4pga.mk + synth/<module>.sdc, and the Makefile routes
     synthesis through f4pga.mk / programs via openFPGALoader, with no
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


def _generate(dest_dir, extra_args):
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(TBENGY),
           "-m", MODULE, "-t", "sv", "-b", "zybo", "-f", PART,
           "-d", str(dest)] + list(extra_args)
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT),
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True)
    assert proc.returncode == 0, "tbengy failed:\n" + proc.stdout
    proj = dest / MODULE
    assert proj.is_dir(), "project dir not generated:\n" + proc.stdout
    return proj


def test_default_backend_is_vivado():
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate(tmp, [])
        synth_tcl = proj / "scripts" / "synth.tcl"
        assert synth_tcl.is_file(), "default generation must emit synth.tcl"
        assert "set_part " + PART in synth_tcl.read_text()
        makefile = (proj / "scripts" / "Makefile").read_text()
        assert "vivado -mode batch" in makefile
        assert "synth.tcl" in makefile
        assert not (proj / "scripts" / "f4pga.mk").exists(), \
            "default generation must not emit f4pga.mk"


def test_f4pga_backend():
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate(tmp, ["--backend", "f4pga"])
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
        makefile = (proj / "scripts" / "Makefile").read_text()
        assert "f4pga.mk" in makefile, "Makefile synth must invoke f4pga.mk"
        assert "openFPGALoader" in makefile
        assert "vivado -mode batch" not in makefile
        readme = (proj / "README.md").read_text()
        assert "EXPERIMENTAL" in readme and "PL-only" in readme


def test_backend_neutral_files_identical():
    with tempfile.TemporaryDirectory() as tmp:
        default_proj = _generate(str(Path(tmp) / "default"), [])
        f4pga_proj = _generate(str(Path(tmp) / "f4pga"),
                               ["--backend", "f4pga"])
        for rel in ("rtl/" + MODULE + ".sv",
                    "sim/tb/" + MODULE + "_tb.sv",
                    "synth/Zybo-Master.xdc"):
            a = (default_proj / rel).read_bytes()
            b = (f4pga_proj / rel).read_bytes()
            assert a == b, rel + " differs between backends"


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
