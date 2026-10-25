#!/usr/bin/env python3
"""End-to-end toolchain tests (OPT-IN, heavy).

Every test here SKIPs unless TBENGY_E2E=1 is set (tests/selfcheck.py
sets it when passed --e2e), so the default selfcheck stays fast and
hermetic. Even with TBENGY_E2E=1, each test probes for its toolchain
and skips with a reason if it is not on PATH.

  * F4PGA e2e: generate led_blink --backend f4pga, run `make synth`,
    assert rc=0 and a 2,083,847-byte synth/led_blink.bit (the
    xc7z010 configuration size). Requires the F4PGA xc7 environment
    activated (symbiflow_synth on PATH).
  * Vivado e2e: ADDITIONALLY requires TBENGY_E2E_VIVADO=1. The
    default flow's synth.tcl does not stop at bitstream generation
    -- its final step programs the attached board -- so this test
    is double-gated to keep the suite from ever touching hardware
    by accident. When enabled it generates the default led_blink,
    runs `make synth`, and asserts synth/design.bit exists.

Both tests build inside temp dirs and clean up after themselves.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TBENGY = REPO_ROOT / "tbengy.py"
XC7Z010_BIT_BYTES = 2083847
F4PGA_TIMEOUT_S = 1200
VIVADO_TIMEOUT_S = 1800


class SkipTest(Exception):
    """Raise to mark a test as skipped (with a reason)."""


def _e2e_enabled():
    return os.environ.get("TBENGY_E2E") == "1"


def _generate(dest_dir, extra_args):
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(TBENGY),
           "-m", "led_blink", "-t", "sv", "-b", "zybo",
           "-f", "xc7z010clg400-1", "-d", str(dest)] + list(extra_args)
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT),
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True)
    assert proc.returncode == 0, "tbengy failed:\n" + proc.stdout
    proj = dest / "led_blink"
    assert proj.is_dir(), "project dir not generated:\n" + proc.stdout
    return proj


def _make_synth(proj, timeout_s):
    return subprocess.run(["make", "synth"], cwd=str(proj / "scripts"),
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True, timeout=timeout_s)


def test_f4pga_e2e():
    if not _e2e_enabled():
        raise SkipTest("TBENGY_E2E is not set (opt-in heavy test)")
    if shutil.which("symbiflow_synth") is None:
        raise SkipTest("symbiflow_synth not on PATH "
                       "(activate the F4PGA xc7 environment)")
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate(tmp, ["--backend", "f4pga"])
        proc = _make_synth(proj, F4PGA_TIMEOUT_S)
        assert proc.returncode == 0, \
            "make synth failed:\n" + proc.stdout[-4000:]
        bit = proj / "synth" / "led_blink.bit"
        assert bit.is_file(), "no bitstream produced:\n" + proc.stdout[-2000:]
        size = bit.stat().st_size
        assert size == XC7Z010_BIT_BYTES, \
            "bitstream size %d != %d (xc7z010)" % (size, XC7Z010_BIT_BYTES)


def test_vivado_e2e():
    if not _e2e_enabled():
        raise SkipTest("TBENGY_E2E is not set (opt-in heavy test)")
    if os.environ.get("TBENGY_E2E_VIVADO") != "1":
        raise SkipTest("TBENGY_E2E_VIVADO is not set: the default "
                       "flow's synth.tcl also programs the attached "
                       "board, so this test is double-gated")
    if shutil.which("vivado") is None:
        raise SkipTest("vivado not on PATH")
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate(tmp, [])
        proc = _make_synth(proj, VIVADO_TIMEOUT_S)
        bit = proj / "synth" / "design.bit"
        assert bit.is_file(), \
            "make synth produced no synth/design.bit (rc=%s):\n%s" % (
                proc.returncode, proc.stdout[-4000:])


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
