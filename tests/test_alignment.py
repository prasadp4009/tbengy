#!/usr/bin/env python3
"""Alignment invariants for tbengy's F4PGA backend.

These tests pin the cross-references that the pre-push alignment
audit established by hand, so they cannot silently drift apart
again:

  * the tool list tbengy's F4PGA probe checks == the external
    commands the generated f4pga.mk / Makefile actually invoke;
  * no dead variables in the generated f4pga.mk (every `?=` variable
    is consumed via $(VAR)); CLK_PERIOD_NS must stay absent -- the
    clock period lives only in the generated .sdc;
  * exactly one bitstream path: the generated Makefile holds no
    literal .bit path, and `make program` resolves through f4pga.mk
    to $(BUILD_DIR)/$(TOP).bit;
  * the generated project's .gitignore whitelists every generated
    source file (checked exactly, via `git check-ignore` in a
    scratch git repo) while still ignoring build artifacts;
  * repo README and the generated F4PGA project README agree on the
    prerequisites and limits they document.

Plain-python, subprocess-driven; runnable directly or under pytest.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TBENGY = REPO_ROOT / "tbengy.py"
MODULE = "led_blink"
PART = "xc7z010clg400-1"
EXPECTED_TOOLS = {
    "symbiflow_synth", "symbiflow_pack", "symbiflow_place",
    "symbiflow_route", "symbiflow_write_fasm",
    "symbiflow_write_bitstream", "openFPGALoader",
}
EXPECTED_VARS = {
    "PARTNAME", "TOP", "DEVICE", "FAMILY", "BITSTREAM_DEVICE",
    "OFL_BOARD", "RTL_SOURCES", "XDC_FILE", "SDC_FILE", "BUILD_DIR",
}


class SkipTest(Exception):
    """Raise to mark a test as skipped (with a reason)."""


def _generate_f4pga(dest_dir):
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(TBENGY),
           "-m", MODULE, "-t", "sv", "-b", "zybo", "-f", PART,
           "--backend", "f4pga", "-d", str(dest)]
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT),
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True)
    assert proc.returncode == 0, "tbengy failed:\n" + proc.stdout
    proj = dest / MODULE
    assert proj.is_dir(), "project dir not generated:\n" + proc.stdout
    return proj


def _probe_tool_set():
    src = (REPO_ROOT / "tbengy.py").read_text()
    match = re.search(r"f4pgaTools\s*=\s*\[(.*?)\]", src, re.S)
    assert match, "f4pgaTools list not found in tbengy.py"
    return set(re.findall(r'"([^"]+)"', match.group(1)))


def _flow_tool_set(proj):
    flow = (proj / "scripts" / "f4pga.mk").read_text()
    makefile = (proj / "scripts" / "Makefile").read_text()
    tools = set(re.findall(r"\b(symbiflow_\w+)\b", flow))
    if "openFPGALoader" in flow:
        tools.add("openFPGALoader")
    # The Makefile must not invoke flow tools directly (it delegates
    # to f4pga.mk); anything it did invoke would belong in this set.
    tools |= set(re.findall(r"\b(symbiflow_\w+)\b", makefile))
    if re.search(r"^\topenFPGALoader", makefile, re.M):
        tools.add("openFPGALoader")
    return tools


def test_probe_matches_flow_tools():
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate_f4pga(tmp)
        probe = _probe_tool_set()
        flow = _flow_tool_set(proj)
        assert probe == EXPECTED_TOOLS, \
            "probe tool list drifted: %s" % sorted(probe)
        assert flow == EXPECTED_TOOLS, \
            "generated flow tool set drifted: %s" % sorted(flow)
        assert probe == flow, \
            "probe %s != flow %s" % (sorted(probe), sorted(flow))


def test_no_dead_variables_in_f4pga_mk():
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate_f4pga(tmp)
        flow = (proj / "scripts" / "f4pga.mk").read_text()
        assert "CLK_PERIOD_NS" not in flow, \
            "clock period must live in the .sdc only (no f4pga.mk copy)"
        defined = re.findall(r"^([A-Z][A-Z0-9_]*)\s*\?=", flow, re.M)
        assert set(defined) == EXPECTED_VARS, \
            "f4pga.mk variable set drifted: %s" % sorted(defined)
        for var in defined:
            uses = len(re.findall(r"\$\(%s\)" % re.escape(var), flow))
            assert uses >= 1, \
                "variable %s is defined but never consumed via $(%s)" % (var, var)


def test_single_bitstream_path():
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate_f4pga(tmp)
        scripts = proj / "scripts"
        makefile = (scripts / "Makefile").read_text()
        assert ".bit" not in makefile, \
            "Makefile must not hold a literal .bit path (f4pga.mk owns it)"
        assert "-f f4pga.mk program" in makefile
        flow = (scripts / "f4pga.mk").read_text()
        build_dir = re.search(r"^BUILD_DIR\s*\?=\s*(\S+)", flow, re.M).group(1)
        top = re.search(r"^TOP\s*\?=\s*(\S+)", flow, re.M).group(1)
        expected_bit = "%s/%s.bit" % (build_dir, top)
        dry = subprocess.run(["make", "-n", "program"], cwd=str(scripts),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True)
        assert dry.returncode == 0, dry.stdout
        loader_lines = [ln.strip() for ln in dry.stdout.splitlines()
                        if "openFPGALoader" in ln]
        assert loader_lines, "make -n program shows no openFPGALoader line"
        assert any(expected_bit in ln for ln in loader_lines), \
            "program must resolve to %s, got: %s" % (expected_bit, loader_lines)
        dry_synth = subprocess.run(["make", "-n", "synth"], cwd=str(scripts),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   universal_newlines=True)
        assert dry_synth.returncode == 0, dry_synth.stdout
        assert "-f f4pga.mk all" in dry_synth.stdout


def test_gitignore_whitelists_f4pga_sources():
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate_f4pga(tmp)
        # Snapshot the generated file set BEFORE `git init` adds its
        # own .git/ internals to the tree.
        sources = [str(p.relative_to(proj))
                   for p in sorted(proj.rglob("*")) if p.is_file()]
        assert sources, "no generated files found"
        init = subprocess.run(["git", "init", "-q"], cwd=str(proj),
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              universal_newlines=True)
        assert init.returncode == 0, init.stdout

        def is_ignored(rel):
            proc = subprocess.run(["git", "check-ignore", rel],
                                  cwd=str(proj), stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  universal_newlines=True)
            return proc.returncode == 0

        for rel in sources:
            assert not is_ignored(rel), \
                "generated source file is git-ignored: " + rel
        for artifact in ("synth/%s.bit" % MODULE, "synth/%s.eblif" % MODULE,
                         "synth/%s.fasm" % MODULE):
            assert is_ignored(artifact), \
                "build artifact should stay ignored: " + artifact


def test_readmes_agree_on_prerequisites():
    repo_readme = (REPO_ROOT / "README.md").read_text()
    assert "--backend" in repo_readme
    assert "F4PGA backend (experimental)" in repo_readme
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate_f4pga(tmp)
        proj_readme = (proj / "README.md").read_text()
        # The prerequisite story must match in both documents: F4PGA
        # (xc7) installed, F4PGA_INSTALL_DIR set, conda env used, and
        # openFPGALoader as the programming tool; both must state the
        # backend is experimental and PL-only.
        for token in ("F4PGA_INSTALL_DIR", "openFPGALoader", "conda"):
            assert token in proj_readme, "project README missing " + token
            assert token in repo_readme, "repo README missing " + token
        for text, label in ((proj_readme, "project"), (repo_readme, "repo")):
            assert "PL-only" in text, label + " README must state PL-only"
            assert "experimental" in text.lower(), \
                label + " README must state the backend is experimental"
            assert re.search(r"xc7", text), label + " README must name xc7"


if __name__ == "__main__":
    tests = [(name, fn) for name, fn in sorted(globals().items())
             if name.startswith("test_") and callable(fn)]
    passed = failed = skipped = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
            print("PASS " + name)
        except SkipTest as exc:
            skipped += 1
            print("SKIP " + name + ": " + str(exc))
        except Exception as exc:
            failed += 1
            print("FAIL " + name + ": " + str(exc))
    print("%d/%d tests passed" % (passed, len(tests)))
    sys.exit(1 if failed else 0)
