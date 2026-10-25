#!/usr/bin/env python3
"""CLI surface tests for tbengy.

Plain-python, subprocess-driven: runnable directly
(`python3 tests/test_cli.py`) or under pytest. No third-party
dependencies. All invocations run with cwd=repo root (tbengy locates
./digilent-xdc relative to the cwd) and write only into temp dirs.

Note on exit codes: tbengy's argparse errors (no args, invalid
choices) exit non-zero via argparse, while several of tbengy's own
error paths print an error message and exit via sys.exit(0). The
tests below assert non-zero exactly where argparse guarantees it,
and assert the message + "nothing was generated" for tbengy's own
error paths, matching the tool's established behaviour.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TBENGY = REPO_ROOT / "tbengy.py"


class SkipTest(Exception):
    """Raise to mark a test as skipped (with a reason)."""


def _run(args, cwd=None):
    proc = subprocess.run([sys.executable, str(TBENGY)] + list(args),
                          cwd=str(cwd or REPO_ROOT),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True)
    return proc


def _norm(text):
    # Lower-case and drop separators so "Basys-3" / "basys3" /
    # "nexys4_ddr" style spellings compare equal.
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _expected_version():
    text = (REPO_ROOT / "tbengy.py").read_text()
    match = re.search(r'^toolVersion\s*=\s*"([^"]+)"', text, re.M)
    assert match, "toolVersion not found in tbengy.py"
    return match.group(1)


def _expected_boards():
    xdc_dir = REPO_ROOT / "digilent-xdc"
    boards = []
    for xdc in sorted(xdc_dir.glob("*.xdc")):
        boards.append(xdc.name.replace(".xdc", "").replace("-Master", "").strip())
    return boards


def test_help():
    proc = _run(["-h"])
    assert proc.returncode == 0, proc.stderr
    help_text = proc.stdout
    flat = re.sub(r"\s+", " ", help_text)
    for token in ("-h", "--help", "-v", "--version",
                  "-l", "--listboards", "-m", "--modulename",
                  "-t", "--tbtype", "-b", "--boardtype",
                  "-f", "--fpga", "--backend", "-d", "--dirpath"):
        assert token in flat, "help output missing " + token
    # The mutually exclusive requirement must be visible in usage.
    assert "(-l | -m" in flat, "usage must show the (-l | -m ...) group"
    # Choices text: tb types and backends are spelled out in the help.
    for token in ("uvm", "sv", "vivado", "f4pga"):
        assert token in flat, "help output missing choice " + token
    assert "{vivado,f4pga}" in flat or "vivado (default)" in flat, \
        "help must present vivado as the default backend choice"


def test_version():
    expected = _expected_version()
    for flag in ("-v", "--version"):
        proc = _run([flag])
        assert proc.returncode == 0, proc.stderr
        assert proc.stdout.strip() == expected, \
            "%s printed %r, expected %r" % (flag, proc.stdout.strip(), expected)


def test_listboards():
    proc = _run(["-l"])
    assert proc.returncode == 0, proc.stderr
    expected = _expected_boards()
    assert expected, "no XDC files found under digilent-xdc/"
    norm_out = _norm(proc.stdout)
    for board in expected:
        assert _norm(board) in norm_out, "board not listed: " + board
    assert "zybo" in norm_out and "basys3" in norm_out
    match = re.search(r"Total boards found:\s*(\d+)", proc.stdout)
    assert match, "listboards must print a total count"
    assert int(match.group(1)) == len(expected), \
        "board count %s != XDC file count %d" % (match.group(1), len(expected))


def test_no_args_exits_nonzero():
    proc = _run([])
    assert proc.returncode != 0, "no-args invocation must fail (rc!=0)"
    assert "usage" in (proc.stderr + proc.stdout).lower()


def test_board_without_fpga():
    with tempfile.TemporaryDirectory() as tmp:
        proc = _run(["-m", "cli_probe", "-t", "sv", "-b", "zybo",
                     "-d", tmp])
        assert "FPGA info is needed" in proc.stdout, proc.stdout
        assert not (Path(tmp) / "cli_probe").exists(), \
            "nothing may be generated when -f is missing"


def test_nonexistent_dirpath():
    with tempfile.TemporaryDirectory() as tmp:
        missing = str(Path(tmp) / "does" / "not" / "exist")
        proc = _run(["-m", "cli_probe", "-d", missing])
        assert "don't exist" in proc.stdout, proc.stdout
        assert not Path(missing).exists()


def test_unknown_board():
    with tempfile.TemporaryDirectory() as tmp:
        proc = _run(["-m", "cli_probe", "-t", "sv", "-b", "nosuchboard",
                     "-f", "xc7z010clg400-1", "-d", tmp])
        assert "not found" in proc.stdout, proc.stdout
        assert not (Path(tmp) / "cli_probe").exists()


def test_invalid_tbtype_rejected():
    proc = _run(["-m", "cli_probe", "-t", "bogus"])
    assert proc.returncode != 0, "invalid -t choice must fail (rc!=0)"
    assert "invalid choice" in proc.stderr, proc.stderr


def test_invalid_backend_rejected():
    proc = _run(["-m", "cli_probe", "-t", "sv", "--backend", "bogus"])
    assert proc.returncode != 0, "invalid --backend choice must fail (rc!=0)"
    assert "invalid choice" in proc.stderr, proc.stderr


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
