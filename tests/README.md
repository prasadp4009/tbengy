# tbengy selfcheck suite

`tests/` is tbengy's one-stop selfcheck: CLI surface, generation
for every backend/type combination, the F4PGA alignment
invariants, golden files pinning the default (Vivado) output, and
opt-in end-to-end toolchain builds.

## Running it

From the repo root, with plain Python 3 (no pytest required):

```bash
python3 tests/selfcheck.py
```

`selfcheck.py` runs every module in order, streams each test's
PASS/FAIL/SKIP line, prints a summary, and exits 0 only if every
non-skipped test passed.

Each module is also runnable on its own, and all modules are
pytest-structured for environments that have pytest
(`pytest tests/`):

| Module | Covers |
|---|---|
| `test_cli.py` | `--help`/`-v`/`--version`/`-l` surface and counts (derived from `digilent-xdc/`), argparse error paths (no args, invalid `-t`, invalid `--backend`), tbengy error paths (`-b` without `-f`, nonexistent `-d`, unknown board) |
| `test_generation.py` | SV+board generation for both backends (files, flow contents, delegating Makefile), backend-neutral files identical across backends, F4PGA tool-probe completeness and engagement, second module/board alignment, full UVM file set, UVM has no synthesis artifacts with either backend, UVM output byte-identical with/without `--backend f4pga` |
| `test_alignment.py` | Executable form of the pre-push audit: probe tool set == tools the generated flow invokes; no dead variables in `f4pga.mk` (`CLK_PERIOD_NS` stays absent -- the clock period lives only in the `.sdc`); single bitstream path (`make program` resolves via `f4pga.mk` to `$(BUILD_DIR)/$(TOP).bit`); generated-project `.gitignore` whitelists every generated source while ignoring build artifacts (via `git check-ignore` in a scratch repo); repo README and generated F4PGA README agree on prerequisites/limits |
| `test_golden.py` | Golden-file pinning of the default outputs (below), plus a guard that no file under `tests/` is silently git-ignored |
| `test_e2e.py` | Opt-in heavy toolchain builds (below) |

Generation tests are subprocess-driven into temporary directories;
nothing is written into the repo.

## End-to-end tests (opt-in)

`test_e2e.py` SKIPs unless `TBENGY_E2E=1` is set:

```bash
python3 tests/selfcheck.py --e2e     # sets TBENGY_E2E=1 for children
```

Even then, each test probes for its toolchain and skips with a
reason if it is missing:

- **F4PGA e2e** -- needs the F4PGA xc7 environment activated
  (`symbiflow_synth` on PATH). Generates `led_blink --backend
  f4pga`, runs `make synth`, asserts rc=0 and a 2,083,847-byte
  `synth/led_blink.bit` (the xc7z010 configuration size).
- **Vivado e2e** -- additionally needs `TBENGY_E2E_VIVADO=1`. It is
  double-gated on purpose: the default flow's `synth.tcl` does not
  stop at bitstream generation, its final step *programs the
  attached board*. Enable it only when that is intended; it
  generates the default `led_blink`, runs `make synth`, and
  asserts `synth/design.bit` exists.

## Golden files

`tests/golden/<case>/` holds the complete default generated
project -- file tree plus full contents -- for three cases:

- `led_blink_sv_zybo` -- `-m led_blink -t sv -b zybo -f xc7z010clg400-1`
- `demo_sv_noboard` -- `-m demo_sv -t sv`
- `demo_uvm` -- `-m demo_uvm -t uvm`

`test_golden.py` regenerates each case into a temp dir and
compares it against the golden. One documented exception:
generated Makefiles embed `# @Author : <username>` and
`# @Date : <date>` header lines, which depend on who runs the tool
and when; those two lines (and only those) are normalised on both
sides before comparison. Every other byte of every file is
compared exactly.

**Provenance:** the goldens were generated on 2026-10-24 from the
`feature/f4pga-backend` branch tip, whose default output had been
verified byte-identical to master `e826a56` (via a clean
`git worktree` of master). They pin *current, known-good* default
behaviour, not a hand-written ideal.

**Updating goldens** -- only when a template or generator change
is intentional and reviewed:

```bash
python3 tests/test_golden.py --update-golden
# (equivalently: TBENGY_UPDATE_GOLDEN=1 python3 tests/test_golden.py)
```

Then re-run `python3 tests/selfcheck.py` and treat the golden diff
in `git status`/`git diff` as part of the change under review. A
golden failure on an *unintentional* change is the suite doing its
job: fix the generator, don't refresh the goldens.

**gitignore note:** the repo `.gitignore` is a whitelist (`*` plus
exceptions), so `tests/golden/**` carries explicit exceptions in
it. `test_no_tests_file_is_git_ignored` in `test_golden.py`
verifies nothing under `tests/` is ignored (bytecode caches
excepted), so a future golden file type cannot vanish silently.
One wrinkle: a golden case's own generated `.gitignore` (itself
golden data) ignores `scripts/synth.tcl` and `synth/*.xdc` in the
nested-project sense, so those two files needed a one-time
`git add -f` when the goldens were first committed; once tracked,
gitignore no longer applies to them and the guard test passes.
