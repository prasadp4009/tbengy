#!/usr/bin/env python3
"""Golden-file tests pinning tbengy's DEFAULT (Vivado) output.

The goldens under tests/golden/<case>/ hold the complete default
generated project (file tree + full contents) for three cases.
Regenerating a case and comparing against its golden fails the
suite if any default output changes -- deliberately or not --
which is the property the F4PGA work proved by hand against
master (e826a56): default output must not move.

One documented exception: generated Makefiles embed two volatile
header lines, `# @Author : <username>` and `# @Date   : <date>`,
which depend on who runs the tool and when. Those two lines (and
only those) are normalised on both sides before comparison;
every other byte of every file is compared exactly.

Refresh goldens ONLY when a template/generator change is
intentional:

    python3 tests/test_golden.py --update-golden

(or TBENGY_UPDATE_GOLDEN=1). Provenance: goldens were generated
2026-10-24 from the feature/f4pga-backend branch tip, whose
default output was verified byte-identical to master e826a56.
See tests/README.md.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TBENGY = REPO_ROOT / "tbengy.py"
GOLDEN_ROOT = Path(__file__).resolve().parent / "golden"

CASES = {
    "led_blink_sv_zybo": (
        ["-m", "led_blink", "-t", "sv", "-b", "zybo",
         "-f", "xc7z010clg400-1"], "led_blink"),
    "demo_sv_noboard": (
        ["-m", "demo_sv", "-t", "sv"], "demo_sv"),
    "demo_uvm": (
        ["-m", "demo_uvm", "-t", "uvm"], "demo_uvm"),
}

_VOLATILE = (b"# @Author", b"# @Date")


class SkipTest(Exception):
    """Raise to mark a test as skipped (with a reason)."""


def _generate(case, dest_dir):
    args, module = CASES[case]
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run([sys.executable, str(TBENGY)] + args +
                          ["-d", str(dest)],
                          cwd=str(REPO_ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, universal_newlines=True)
    assert proc.returncode == 0, "tbengy failed:\n" + proc.stdout
    proj = dest / module
    assert proj.is_dir(), "project dir not generated:\n" + proc.stdout
    return proj


def _tree(root):
    return {str(p.relative_to(root)): p
            for p in sorted(Path(root).rglob("*")) if p.is_file()}


def _normalised(path):
    data = Path(path).read_bytes()
    if Path(path).name != "Makefile":
        return data
    lines = []
    for line in data.split(b"\n"):
        if any(line.startswith(prefix) for prefix in _VOLATILE):
            lines.append(line.split(b":")[0] + b": <volatile>")
        else:
            lines.append(line)
    return b"\n".join(lines)


def _compare(case):
    golden_dir = GOLDEN_ROOT / case
    assert golden_dir.is_dir(), \
        "golden data missing for %s (run --update-golden)" % case
    golden = _tree(golden_dir)
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate(case, tmp)
        fresh = _tree(proj)
        assert set(fresh) == set(golden), \
            "%s: file tree drifted. missing=%s extra=%s" % (
                case, sorted(set(golden) - set(fresh)),
                sorted(set(fresh) - set(golden)))
        for rel in sorted(golden):
            assert _normalised(golden[rel]) == _normalised(fresh[rel]), \
                "%s: content drifted in %s" % (case, rel)


def _update(case):
    golden_dir = GOLDEN_ROOT / case
    if golden_dir.exists():
        shutil.rmtree(str(golden_dir))
    golden_dir.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        proj = _generate(case, tmp)
        for rel, path in _tree(proj).items():
            target = golden_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(path), str(target))
    print("UPDATED golden " + case)


def test_golden_led_blink_sv_zybo():
    _compare("led_blink_sv_zybo")


def test_golden_demo_sv_noboard():
    _compare("demo_sv_noboard")


def test_golden_demo_uvm():
    _compare("demo_uvm")


def test_no_tests_file_is_git_ignored():
    # The repo .gitignore is a whitelist; anything under tests/ that
    # it silently ignores would never be committed. Bytecode caches
    # are the one expected exception.
    tests_dir = Path(__file__).resolve().parent
    paths = []
    for path in sorted(tests_dir.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        paths.append(str(path.relative_to(REPO_ROOT)))
    assert paths, "no test files found"
    proc = subprocess.run(["git", "check-ignore"] + paths,
                          cwd=str(REPO_ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, universal_newlines=True)
    ignored = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    assert not ignored, "files under tests/ are git-ignored: %s" % ignored


if __name__ == "__main__":
    update = ("--update-golden" in sys.argv or
              os.environ.get("TBENGY_UPDATE_GOLDEN") == "1")
    if update:
        for case in sorted(CASES):
            _update(case)
        print("Goldens updated for %d cases" % len(CASES))
        sys.exit(0)
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
