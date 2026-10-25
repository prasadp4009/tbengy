#!/usr/bin/env python3
"""tbengy selfcheck -- the single entry point for the test suite.

Runs every test module under tests/ in order, streams each test's
PASS/FAIL/SKIP lines as they happen, and prints a summary. Exit
code is 0 only if every non-skipped test passed.

Usage (from the repo root, plain python3 -- no pytest needed):

    python3 tests/selfcheck.py           # fast suite (e2e skipped)
    python3 tests/selfcheck.py --e2e     # also run opt-in e2e tests
                                         # (needs TBENGY_E2E toolchains
                                         #  on PATH; see tests/README.md)

Each module also remains runnable on its own, e.g.
`python3 tests/test_cli.py`, and pytest-structured for when pytest
is available (`pytest tests/`).
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent

MODULES = [
    "test_cli.py",
    "test_generation.py",
    "test_alignment.py",
    "test_golden.py",
    "test_e2e.py",
]

_RESULT = re.compile(r"^(PASS|FAIL|SKIP)\s")


def run_module(module, env):
    path = TESTS_DIR / module
    print("=" * 70)
    print("tests/" + module)
    print("=" * 70, flush=True)
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    started = time.time()
    proc = subprocess.Popen([sys.executable, str(path)],
                            cwd=str(REPO_ROOT), env=env,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        match = _RESULT.match(line)
        if match:
            counts[match.group(1)] += 1
    rc = proc.wait()
    duration = time.time() - started
    if rc != 0 and counts["FAIL"] == 0:
        # A module that dies without reporting a FAIL (crash, syntax
        # error, missing golden data) is a failure, not a pass.
        counts["FAIL"] += 1
        print("FAIL %s: module exited with rc=%d" % (module, rc))
    print("-- tests/%s: %d passed, %d failed, %d skipped (%.1fs, rc=%d)"
          % (module, counts["PASS"], counts["FAIL"], counts["SKIP"],
             duration, rc), flush=True)
    return counts, rc, duration


def main(argv):
    env = dict(os.environ)
    if "--e2e" in argv:
        env["TBENGY_E2E"] = "1"
        print("selfcheck: --e2e given (TBENGY_E2E=1 for child tests)")
    elif env.get("TBENGY_E2E") == "1":
        print("selfcheck: TBENGY_E2E=1 already set in the environment")
    total = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    bad_modules = []
    started = time.time()
    for module in MODULES:
        counts, rc, _ = run_module(module, env)
        for key in total:
            total[key] += counts[key]
        if counts["FAIL"] or rc != 0:
            bad_modules.append(module)
    duration = time.time() - started
    print("=" * 70)
    print("SELFCHECK SUMMARY: %d passed, %d failed, %d skipped "
          "(%d tests, %d modules, %.1fs)"
          % (total["PASS"], total["FAIL"], total["SKIP"],
             total["PASS"] + total["FAIL"] + total["SKIP"],
             len(MODULES), duration))
    if bad_modules:
        print("SELFCHECK RESULT: FAIL (modules with failures: %s)"
              % ", ".join(bad_modules))
        return 1
    print("SELFCHECK RESULT: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
