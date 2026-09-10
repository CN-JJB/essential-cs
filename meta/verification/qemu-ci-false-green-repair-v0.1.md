# QEMU CI false-green repair v0.1 — V-147-01 (Issue #149)

- **Assigned Issue:** #149 `[Repair] Canonical QEMU CI false-green repair v0.1`
- **Role:** Stable Environment / CI Repair Executor (Local Executor)
- **Canonical base:** `main @ e19c7256319366c105f90170f1b4b46d159c35c6`
- **Branch:** `repair/issue-149-qemu-ci-false-green-v0.1`
- **Scope:** V-147-01 only. V-147-02 / OQ-BP-006 remain OPEN and out of scope.

## 1. Defect being repaired (V-147-01)

The `canonical-qemu-lane` workflow could report the `qemu-smoke` job `success` while
`labs/lab-req-02-xv6-syscall/smoke.sh` never executed and `req02-smoke.log` was never
written. Confirmed in #147 / PR #148: run `34469175287` concluded success, its log showed
`here-document ... delimited by end-of-file (wanted 'SLEEPEOF')`, and artifact
`canonical-qemu-evidence` (id `10148808999`) contained no `req02-smoke.log`.

## 2. Root cause

The fixture was created with two **indented nested heredocs** inside a `bash -c '…'`
string embedded in a YAML block scalar:

```yaml
run: |
  docker run … bash -c '
    cat > worktree/user/sleep.c << "SLEEPEOF"
    #include "kernel/types.h"
    …
    SLEEPEOF
    … ./smoke.sh …'
```

Failure chain:

1. The YAML block scalar strips its block indent (10 spaces), leaving the inner
   `bash -c` script indented by 2 spaces.
2. `<< "SLEEPEOF"` is a **non-stripping** heredoc (quoted delimiter, no `<<-`), so bash
   requires the terminator line to be exactly `SLEEPEOF` at column 0.
3. After YAML stripping, the terminator line is `␣␣SLEEPEOF` (column 2), which does **not**
   match. Bash keeps consuming every following line — the second heredoc `<< "PYEOF"`, the
   `grep`, `./smoke.sh`, everything — as heredoc body until end-of-file.
4. Bash emits the `here-document … delimited by end-of-file` message as a **warning, not an
   error**, so `set -e` does not abort. `cat` (the heredoc's command) exits 0, so the inner
   script exits 0.
5. `./smoke.sh` never ran, `req02-smoke.log` was never created, yet `docker run` exited 0,
   `test "${PIPESTATUS[0]}" -eq 0` passed, and the job went green.

## 3. Repair mechanism

Both nested heredocs are replaced with indentation-immune file writes inside the same
canonical-image `docker run` (the container runs as root, so fixture files are written in
the image, never on the hosted runner):

- **`sleep.c`** — `printf "%s\n"` with 12 double-quoted arguments (`\"` for `"`, `\\n` for
  the literal C `\n` escape).
- **`$U/_sleep` Makefile registration** — a short Python file-write emitted by
  `printf "%s\n"` into `/tmp/patch_uprogs.py`, then executed. Tab/newline/backslash are
  built with `chr(9)` / `chr(10)` / `chr(92)` so no backslash has to survive the
  YAML → outer single-quote → inner bash double-quote layers.

No heredoc remains in the repaired step (the only `<<` in the file is inside an explanatory
comment). The exact xv6 pin/source-route/setup semantics, `set -euo pipefail`, package
identity checks, and QEMU cleanup are unchanged.

## 4. Fail-closed recurrence guard

Two independent layers make a green job impossible unless the real smoke actually executed
and the bundle is complete:

- **In-step postcondition** (immediately after `./smoke.sh | tee req02-smoke.log`): asserts
  `req02-smoke.log` exists and is non-empty, and contains:
  - `QEMU_SMOKE_STATUS: PASS` (smoke.sh's own PASS, emitted only after the full QEMU round-trip),
  - `=== LAB-REQ-02 Smoke Test PASS ===` (final smoke banner),
  - a standalone `LAB_REQ_02_OK` line (`^[[:space:]]*LAB_REQ_02_OK[[:space:]]*$` — the guest
    execution marker that a simple `echo` cannot forge),
  - `QEMU_REAPED: TRUE` and `PID_MARKER_CLEAN: YES`.
- **Evidence completeness gate** (separate step before upload): asserts all six required
  files exist and are non-empty:
  `qemu-env-snapshot.txt`, `req02-preflight.log`, `req02-setup.log`,
  `req02-source-route.log`, `req02-smoke.log`, `qemu-lane-outer.log`.

Either guard failing exits non-zero and fails the job; the upload step keeps `if: always()`
so a failed run still uploads whatever evidence exists for diagnosis.

## 5. Regression proof

**Static / structural:**

- YAML parse (PyYAML 6.0.3): PASS.
- `bash -n` on every `run:` block (outer) and every inner `bash -c` string: PASS
  (bash 5.2.21). 16 checks, 0 failures.
- `git diff --check`: PASS (no whitespace errors).
- Grep confirms no `<<` heredoc remains in the repaired step.

**Functional simulation of the new fixture mechanism** (exact `printf`/Python copied from
the workflow, run in an isolated temp tree):

- `sleep.c` produced is byte-identical to the intended C source, including the literal C
  `\n` escape in `fprintf(2, "Usage: sleep ticks\n");`.
- `patch_uprogs.py` inserts `\t$U/_sleep\` immediately after `\t$U/_zombie\` (exit 0);
  `_zombie` count stays 1, `_sleep` count becomes 1 (single, idempotent insertion).
- `grep 'pause[[:space:]]*(' sleep.c` and `grep 'U/_sleep' Makefile` both PASS — the same
  predicates smoke.sh itself enforces.

## 6. Forbidden / non-claims

- Forbidden surfaces untouched: `.devcontainer/**`, `.github/workflows/ci-fast.yml`,
  `scripts/canonical-env-capture.sh`, `book/**`, learner-facing `labs/**`, `project/**`,
  `meta/DECISIONS.md`, `meta/OPEN_QUESTIONS.md`, `meta/PROJECT_STATUS.md`, tags/releases,
  Issue #34 evidence.
- Only `.github/workflows/ci-qemu-lane.yml` is modified, plus this one narrow report.
- **No** learner validation, v1.0, VERIFIED, or stable RELEASED claim. **No** V-147-02 work.
  **No** OQ-BP-006 closure.

## 7. Final exact-head Actions evidence

The required live `canonical-qemu-lane` run (run ID/URL, exact checkout SHA, job conclusion,
environment/package identity, source pin/route, smoke execution proof, artifact metadata and
inventory) is recorded in the accompanying **PR body / Completion Report** — the canonical
delivery surface — because the run must occur against the head that includes this report.
