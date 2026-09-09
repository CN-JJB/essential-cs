# v0.9 RC Readiness Re-Verification v0.1

Status: **INDEPENDENT RE-VERIFICATION REPORT — Issue #133 (not a repair, not VERIFIED/RELEASED)**
Verification base: `main @ e6b8a2f357efe4ed8a02306dede1c556b8da628b`
Date: 2026-09-09
Final recommendation: **`NOT READY — BLOCKERS REQUIRE REPAIR`**

This report re-verifies the two Issue #131 / PR #132 repairs of the accepted Issue #129 Full-Core verification. It is not a rerun of the 25-Module / 70-Lesson / 5-Required-Lab matrix.

---

## 1. Exact canonical base

| Item | Value |
|---|---|
| Locked canonical base (Issue #133) | `e6b8a2f357efe4ed8a02306dede1c556b8da628b` |
| Actual `git rev-parse HEAD` at verification start | `e6b8a2f357efe4ed8a02306dede1c556b8da628b` — **PASS (exact match)** |
| Branch | `verification/issue-133-v09-rc-readiness-reverify` |
| Merge-base with `origin/main` | `e6b8a2f357efe4ed8a02306dede1c556b8da628b` — **PASS (== base)** |
| Ahead/behind at start | ahead `0`, behind `0` |
| Working tree at start | clean except untracked agent session directory `.commandcode/` (not course content, never committed) |

Commands:

```bash
git fetch origin
git checkout main
git reset --hard origin/main
git rev-parse HEAD
git status --short
```

No silent base substitution was performed.

After this report commit the branch is ahead of the locked base by this report only.

---

## 2. Verifier independence statement

Role: **Independent Technical Integration Verifier**.

This session is not the Issue #131 repair Executor and did not author the repaired `smoke.sh`, LAB-REQ-02 README, or license texts. No file of the material under review was modified. Defects, if found, were to be recorded, classified, and routed — not repaired.

Allowed committed change: this report only.

Ephemeral local helpers used for verification (WSL `/tmp/issue-133/**`, `%TEMP%\issue-133-*.sh`, gitignored xv6 worktree learner input) were not committed.

---

## 3. Environment matrix

| Capability | Windows host | WSL2 Ubuntu (canonical Linux verification env) |
|---|---|---|
| OS / kernel | Windows 11 NT 10.0.26200, AMD64 | Ubuntu 24.04, kernel `6.18.33.2-microsoft-standard-WSL2`, x86_64 |
| Python | CPython 3.13.1 (MSC 64-bit) | CPython 3.12.3 |
| QEMU RISC-V | NOT FOUND | QEMU 8.2.2 (`Debian 1:8.2.2+ds-0ubuntu1.18`) |
| RISC-V GCC | NOT FOUND | `riscv64-linux-gnu-gcc` 13.3.0; xv6 build used `riscv64-unknown-elf-gcc` 13.2.0 |
| RISC-V objdump | NOT FOUND | GNU objdump 2.42 (`riscv64-linux-gnu-objdump` / `riscv64-unknown-elf-objdump`) |
| make | present (host) | GNU Make 4.3 |
| git | 2.55.0.windows.5 | 2.43.0 |
| perl / bc | — | perl 5.38.2 / bc 1.07.1 |
| sqlite3 CLI | — | 3.45.1 (present in this environment; see V-129-05) |

Exact verification SHA: `e6b8a2f357efe4ed8a02306dede1c556b8da628b`.

Independent LAB-REQ-02 runtime was executed on a `git archive` LF tree at that SHA extracted to WSL ext4 `/tmp/issue-133/tree`. This avoids Windows `core.autocrlf` working-tree conversion and drvfs build artifacts. Learner `user/sleep.c` and `$U/_sleep` existed only in the gitignored xv6 worktree copy under that tree.

Committed LAB-REQ-02 entrypoint scripts are stored in the Git tree as mode `100644`: `preflight.sh`, `setup.sh`, `smoke.sh`, and `reset.sh`. The learner README requires direct `./preflight.sh` / `./setup.sh` / `./smoke.sh` / `./reset.sh` invocation. On a fresh Linux checkout, those commands therefore fail with `Permission denied` until a user performs an undocumented `chmod +x`. The verifier applied ephemeral `chmod +x` only to obtain the independent runtime evidence; that proves the script logic but does not prove the committed learner workflow is directly runnable as documented. **Classification: `SIMPLE FIX` / BLOCKING v0.9 readiness (V-133-01).** This is repository metadata, not a Windows/WSL-only environment artifact.

---

## 4. Issue #131 repair ownership

| Item | Value |
|---|---|
| Issue | #131 — `[Repair] Close v0.9 smoke & license gates v0.1` — **CLOSED** 2026-09-09 |
| Repair PR | #132 — **MERGED** |
| Repair head | `e63ea2d9a29bc0621e6da26dca427aba0a6dae75` |
| Merge commit | `3d561bbdd48116ae35cb0e052747330026d62e19` |
| Merge parents | `57cc7d8` (main) + `e63ea2d` (repair) |

PR #132 changed exactly five paths:

1. `labs/lab-req-02-xv6-syscall/smoke.sh`
2. `labs/lab-req-02-xv6-syscall/README.md`
3. `LICENSES/Apache-2.0.txt` (added)
4. `LICENSES/CC-BY-SA-4.0.txt` (added)
5. `LICENSES/README.md`

Those five blobs are present at the locked verification base.

Between Issue #129's verification base `d6641e8e2053f86a0c3a09c02d274554bfd0fbcf` and this re-verification base, the additional non-#131 paths are the Issue #129 report, PROJECT_STATUS routing into #131/#133, and this phase's status commit `e6b8a2f` (`meta/PROJECT_STATUS.md` only). **No unexpected follow-on repair of verified smoke/license material occurred after PR #132.**

---

## 5. V-129-01 source audit (`labs/lab-req-02-xv6-syscall/smoke.sh`)

Independent inspection of the committed script at blob `40d815625dbfb9a873a919d06a133c5b754581df`. Result: **PASS**. No remaining semantic false-positive path found.

| Required property | Evidence | Result |
|---|---|---|
| No burst-write of `sleep` / `sleep 10` / `echo LAB_REQ_02_OK` | Three separate `send_command(...)` calls, each after a `wait_until` predicate | **PASS** |
| Bounded shell-startup wait | `wait_until(..., 20, "xv6 shell start (init: starting sh)")` | **PASS** |
| Prompt-readiness synchronization | `has_prompt` requires normalized buffer `endswith("$ ")`; initial prompt wait 10s | **PASS** |
| No-arg `sleep` must observe `Usage: sleep ticks` | `sleep_usage_complete` requires `USAGE in new` **and** `has_prompt` | **PASS** |
| `sleep 10` must return to a subsequent prompt | `sleep10_returned` requires `has_prompt(text)` and `"$ "` in the *new* slice (15s bound) | **PASS** |
| Final marker is standalone `LAB_REQ_02_OK` | `has_execution_marker` requires `line.strip() == MARKER` | **PASS** |
| Echoed `echo LAB_REQ_02_OK` cannot satisfy the predicate | `$ echo LAB_REQ_02_OK` and `echo LAB_REQ_02_OK` are not equal to `LAB_REQ_02_OK` after strip | **PASS** |
| Negative self-check fails echo-only input | Step 3 Python self-check; `MARKER_SELF_CHECK: PASS` on all three runtime runs | **PASS** |
| QEMU process group is owned | `start_new_session=True`; PID file stores session-leader pid | **PASS** |
| Cleanup bounded with SIGTERM/SIGKILL fallback | `os.killpg(..., SIGTERM)` + `wait(2)` then `SIGKILL` + `wait(3)` | **PASS** |
| Process must reap | `p.poll() is None` raises `owned QEMU process group was not reaped`; `reaped=True` only after reap | **PASS** |
| PID marker removal truthful | unlink only after reap; remaining pid file raises; runtime `PID_MARKER_CLEAN: YES` | **PASS** |

`bash -n labs/lab-req-02-xv6-syscall/smoke.sh` — **PASS**.

No blocking source-level remainder of V-129-01 was found. Nothing was repaired.

---

## 6. Independent real QEMU runtime

Environment: WSL2 Ubuntu 24.04, QEMU 8.2.2, `riscv64-unknown-elf-gcc` 13.2.0, exact base SHA above.

Commands actually run (ephemeral LF tree; committed scripts unmodified):

```bash
cd labs/lab-req-02-xv6-syscall
./preflight.sh
./setup.sh
python3 verify_source_route.py worktree
# legal learner input only in gitignored worktree: user/sleep.c + $U/_sleep
./smoke.sh   # three consecutive independent runs
./reset.sh
```

| Step | Result |
|---|---|
| `./preflight.sh` | **PASS** — git/make/python3/perl/bc, RISC-V GCC+objdump, QEMU RISC-V present |
| `./setup.sh` | **PASS** — origin `https://github.com/mit-pdos/xv6-riscv.git`, HEAD `35b088427ef37611c38afdeed5a52a278cae38f9`, upstream `LICENSE` present |
| `python3 verify_source_route.py worktree` | **PASS** — `SYS_pause == 13`, `[SYS_pause] -> sys_pause`, `sys_pause(void)`, `int pause(int);`, stub `a7 → ecall → ret`, trap `scause 8`, trampoline `uservec`, learner `sleep.c` calls `pause(...)` |
| Disassembly in smoke Step 2 | **PASS** — `main -> pause stub -> ecall` |
| Official course-fork grader | **NOT RUN** (not in the pinned tree; out of this Issue's scope) |

Learner input was original verification-only C: validate argc, print `Usage: sleep ticks`, `pause(ticks)`, `exit`. It was not committed.

This runtime does **not** reuse Issue #131 Executor output.

---

## 7. Three consecutive independent smoke runs

All three runs executed committed `./smoke.sh` against the same legal learner worktree. Observed guest console (identical contract on all three runs):

```text
xv6 kernel is booting
hart 1 starting
hart 2 starting
init: starting sh
$ sleep
Usage: sleep ticks
$ sleep 10
$ echo LAB_REQ_02_OK
LAB_REQ_02_OK
$
```

| Run | UTC window | Shell | `Usage: sleep ticks` | `sleep 10` returned | Standalone `LAB_REQ_02_OK` | Following `$ ` | `QEMU_REAPED` | PID file after | Host `qemu-system-riscv64` after | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-09T13:46:46Z–13:46:49Z | **PASS** | **PASS** (output line, not command echo) | **PASS** | **PASS** (distinct from `$ echo LAB_REQ_02_OK`) | **PASS** | TRUE | NO | none | **PASS** |
| 2 | 2026-09-09T13:46:49Z–13:46:51Z | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | TRUE | NO | none | **PASS** |
| 3 | 2026-09-09T13:46:51Z–13:46:52Z | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | TRUE | NO | none | **PASS** |

Smoke also printed on every run:

- `MARKER_SELF_CHECK: PASS`
- `USAGE_OUTPUT_OBSERVED: YES`
- `SLEEP10_RETURNED: YES`
- `EXECUTION_MARKER_OBSERVED: YES`
- `PID_MARKER_CLEAN: YES`
- `=== LAB-REQ-02 Smoke Test PASS ===`

Windows-host QEMU smoke: **NOT RUN** (no RISC-V QEMU/toolchain on the Windows host). The WSL2 runtime is the independent Required-Lab evidence.

---

## 8. Echo-only negative verification

Independent of Executor claims and of the in-script self-check, the same predicate as committed `smoke.sh` was executed on constructed buffers:

| Buffer | `has_execution_marker` | `execution_marker_satisfied` |
|---|---|---|
| `init: starting sh\n$ echo LAB_REQ_02_OK\n` | False | False |
| that buffer plus following `$ ` | False | False |
| `$ echo LAB_REQ_02_OK\n` | False | False |
| `echo LAB_REQ_02_OK\n$ ` (bare echoed command) | False | False |
| `$ echo LAB_REQ_02_OK\necho LAB_REQ_02_OK\nLAB_REQ_02_OK\n$ ` | True | True |
| standalone marker without following prompt | True marker / **not** satisfied | False |
| `Usage: sleep ticks\n$ ` | False | False |

Independent predicate result: **PASS**.

Committed Step 3 self-check: **PASS** on all three smoke runs.

Real QEMU output (section 7) shows the echoed command line and the execution line as **two different lines**. The predicate accepts only the latter plus the following prompt.

---

## 9. Targeted regression

| Surface | Command | Result |
|---|---|---|
| Shell syntax | `bash -n labs/lab-req-02-xv6-syscall/smoke.sh` | **PASS** |
| M06 (WSL2 / CPython 3.12.3) | `python3 -m unittest discover -s labs/foundations/m06 -p "test_*.py"` | **PASS** — 7/7 in 1.065s |
| M06 (Windows / CPython 3.13.1) | `python -m unittest discover -s labs/foundations/m06 -p "test_*.py"` | **PASS** — 7 tests, 5 skipped (host capability-gating; not a Linux regression) |
| Shared M05–M09 preflight | `bash scripts/preflight-m05-m09.sh` | **PASS** — M06/M07/M08/M09 host capability PASS; LAB-REQ-02 `RUNNABLE`; `strace` truthfully `MISSING` |
| LAB-REQ-02 preflight | `./preflight.sh` | **PASS** |
| LAB-REQ-02 setup | `./setup.sh` | **PASS** |
| Source-route | `python3 verify_source_route.py worktree` | **PASS** |
| Smoke | `./smoke.sh` ×3 | **PASS** |
| Reset | `./reset.sh` | **PASS** |
| Whitespace | `git diff --check` | **PASS** (exit 0) |

Full 296-test Core matrix: **NOT RUN** (Issue #129 remains the accepted baseline; no new failure evidence required expansion).

---

## 10. Cleanup / reap / reset evidence

After each smoke run:

- `QEMU_REAPED: TRUE`
- `PID_MARKER_CLEAN: YES`
- `.qemu_smoke.pid` absent
- no leftover `qemu-system-riscv64` process

After `./reset.sh`:

| Check | Result |
|---|---|
| Worktree HEAD | `35b088427ef37611c38afdeed5a52a278cae38f9` — **PASS** |
| `git status --porcelain` | empty — **PASS** |
| `user/sleep.c` | removed — **PASS** |
| `$U/_sleep` in Makefile | 0 matches — **PASS** |
| Build residue (`kernel/kernel`, `fs.img`, `user/_sleep`, `*.o`) | removed by `git clean -fdx` — **PASS** |
| `.qemu_smoke.pid` | absent — **PASS** |
| owned QEMU process | none — **PASS** |

---

## 11. V-129-06 canonical license comparison

Verification date (UTC): **2026-09-09**.

Authoritative sources fetched with `curl -fsSL` the same day:

- Apache Software Foundation Apache License 2.0 plaintext: `https://www.apache.org/licenses/LICENSE-2.0.txt`
- Creative Commons CC BY-SA 4.0 International legal code plaintext: `https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt`

Comparison is against **committed git blobs** at the locked base (`git show HEAD:LICENSES/...`), not the Windows working-tree checkout. `git ls-files --eol` records `i/lf w/crlf` because `core.autocrlf=true`. Working-tree CRLF is a checkout conversion, not the committed object.

| File | Official SHA-256 | Committed blob SHA-256 | `cmp` vs official | Result |
|---|---|---|---|---|
| `LICENSES/Apache-2.0.txt` | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` | identical (11358 bytes, LF) | **MATCH** |
| `LICENSES/CC-BY-SA-4.0.txt` | `28a9529c7d0bb4dc51f4bf5c116a3d16ef247a052f7591466768ddf563fd1cf5` | `28a9529c7d0bb4dc51f4bf5c116a3d16ef247a052f7591466768ddf563fd1cf5` | identical (20138 bytes, UTF-8 LF) | **MATCH** |

Git blob IDs: Apache `d645695673349e3947e8e5ae42332d0ac3164cd7`; CC BY-SA `2d58298e6eda10e7204abb52722efbc840db2390`.

This is exact byte/hash identity with the official sources named by `LICENSES/README.md`, not a “looks like a license” judgment.

---

## 12. `LICENSES/README.md` / `ATTRIBUTION.md` audit

`LICENSES/README.md`:

- Points to committed [`LICENSES/CC-BY-SA-4.0.txt`](../../LICENSES/CC-BY-SA-4.0.txt) and [`LICENSES/Apache-2.0.txt`](../../LICENSES/Apache-2.0.txt) — **PASS**
- Names the same official URLs used in section 11 — **PASS**
- Does **not** say canonical full texts remain to be added before release — **PASS**
- Retains the third-party provenance / `ATTRIBUTION.md` rule — **PASS**

`ATTRIBUTION.md`:

- Entries section remains `_No third-party material has been incorporated yet._`
- Repository still has no incorporated third-party material requiring a ledger row
- Empty state is truthful — **PASS**
- Not modified by this verification

---

## 13. Issue #129 blocker closure matrix

| ID | Issue #129 classification | This re-verification | Closure |
|---|---|---|---|
| **V-129-01** | BLOCKING — LAB-REQ-02 committed smoke false-positive / burst interaction; routed SIMPLE FIX | Source audit PASS; 3/3 independent real QEMU PASS; echo-only negative PASS; reap/PID cleanup PASS | **CLOSED** |
| **V-129-02** | ENVIRONMENT — WSL2 M10 localhost-relay cleanup probe | No new M10 evidence collected (full matrix NOT RUN by contract) | **UNCHANGED** — ENVIRONMENT, not a v0.9 repair item |
| **V-129-03** | ENVIRONMENT — Windows m00-m01/m07/m08 limits | Windows M06 this run: 5 skips, 0 failures. No new course defect | **UNCHANGED** — informational |
| **V-129-04** | NOT A BLOCKER / BOUNDED LIMIT — no deployable Mini Cloud tree | Confirmed: no `project/` directory. Governance remains v1.0-tracked (D-024) | **UNCHANGED** — not a v0.9 requirement invented here |
| **V-129-05** | NOT A BLOCKER / BOUNDED LIMIT — sqlite3 CLI provisioning / OQ-BP-006 | This WSL environment now has sqlite3 3.45.1 (prior provisioning). OQ-BP-006 remains OPEN. No new evidence that the governance item is closed | **UNCHANGED** — bounded environment/governance |
| **V-129-06** | release-hygiene gate — canonical Apache-2.0 / CC BY-SA 4.0 texts required before public v0.9 tag/release | Committed blobs MATCH official ASF and Creative Commons plaintext; README/ATTRIBUTION truthful | **CLOSED FOR PUBLIC v0.9 RELEASE HYGIENE** |

No historical classification was changed without new evidence.

---

## 14. New blocker found by re-verification

### V-133-01 — LAB-REQ-02 shell entrypoints are non-executable in the Git tree (BLOCKING — SIMPLE FIX)

- **Location:** Git tree modes for:
  - `labs/lab-req-02-xv6-syscall/preflight.sh`
  - `labs/lab-req-02-xv6-syscall/setup.sh`
  - `labs/lab-req-02-xv6-syscall/smoke.sh`
  - `labs/lab-req-02-xv6-syscall/reset.sh`
- **Observed committed mode:** `100644` for all four scripts.
- **Learner contract:** the LAB-REQ-02 README instructs direct `./preflight.sh`, `./setup.sh`, `./smoke.sh`, and `./reset.sh` invocation.
- **Independent reproduction:** the verifier's first Linux direct invocation returned rc=126 / `Permission denied`; verification could continue only after an ephemeral `chmod +x` in the temporary Linux tree.
- **Why this is not environment-only:** Git executable mode is part of the repository tree object. A fresh Linux checkout that honors Git file modes receives these scripts as non-executable regardless of WSL timing behavior.
- **Expected:** Required Lab entrypoints are directly runnable using the commands published in the README.
- **Actual:** the published commands fail until an undocumented permission mutation is performed.
- **Classification:** `SIMPLE FIX`.
- **Severity / readiness effect:** **BLOCKING v0.9 readiness** because a Required Lab is not directly runnable from a clean canonical Linux checkout according to its own documented workflow.
- **Recommended routing:** separate narrow repair setting the executable bit (`100755`) on the four LAB-REQ-02 shell entrypoints, followed by targeted independent re-verification. Do not repair inside this verification PR.

## 15. BLOCKED / NOT RUN items

| Item | Status | Reason |
|---|---|---|
| Full 296-test Core matrix | **NOT RUN** | Issue #129 remains accepted baseline; no new failure evidence required expansion |
| Windows-host LAB-REQ-02 QEMU smoke | **NOT RUN** | No QEMU RISC-V / RISC-V GCC on the Windows host |
| Official MIT course-fork `grade-lab-util` | **NOT RUN** | Not present at the pinned xv6 commit |
| Live `strace` | **NOT RUN** | Shared preflight reports `MISSING`; not required for this re-verification |
| Issue #34 real learner validation | **NOT RUN** | Separate gate; AI cannot satisfy it |
| v0.9 tag / GitHub Release | **NOT RUN** | Out of verifier authority |
| M10 WSL2 relay re-probe (V-129-02) | **NOT RUN** | No new evidence; historical ENVIRONMENT classification retained |

Nothing in this table is treated as a substitute for the independent QEMU evidence in sections 6–7.

---

## 16. Repository hygiene

At verification start and before the report commit:

```text
git status --short
?? .commandcode/
git diff --check    # exit 0
```

`.commandcode/` is an untracked agent session directory and is not course content.

The verification branch commit adds only:

`meta/verification/v09-rc-readiness-reverification-v0.1.md`

Not committed:

- xv6 worktree / clone
- learner `sleep.c` / `$U/_sleep`
- xv6 build outputs (`kernel/kernel`, `fs.img`, `user/_sleep`, `*.o`)
- `.qemu_smoke.pid`
- `/tmp/issue-133/**` logs and ephemeral drivers
- license download scratch
- `.commandcode/`

---

## 17. Explicit non-claims

This report does **not** establish:

- that a `v0.9` tag exists or may be created by this verifier
- that a public release has been published
- real learner validation (Issue #34 remains OPEN / deferred under D-027)
- `VERIFIED` or `RELEASED` lifecycle states
- v1.0 readiness
- closure of OQ-BP-006
- a Mini Cloud deployable tree
- that Issue #129's full-Core matrix was rerun at this SHA

The Issue #131 smoke semantics and public-license-text gates passed independent re-verification, but V-133-01 prevents a READY recommendation until the committed LAB-REQ-02 shell entrypoints are directly executable in a clean Linux checkout.

---

## 18. Final recommendation

**`NOT READY — BLOCKERS REQUIRE REPAIR`**

Rationale: the Issue #131 semantic smoke repair is independently validated by source audit, three consecutive real QEMU runs, echo-only rejection, cleanup/reap evidence, and targeted regressions. The Apache-2.0 and CC BY-SA 4.0 committed blobs are byte-identical to the official sources, so V-129-01 and V-129-06 are closed. However, this re-verification also independently confirmed V-133-01: all four documented LAB-REQ-02 shell entrypoints are committed as Git mode `100644`, while the learner README requires direct `./...` execution. A clean Linux checkout therefore fails the Required Lab workflow with `Permission denied` until an undocumented `chmod +x`. Because the Required Lab is not directly runnable as documented from the repository state, v0.9 readiness remains blocked pending a narrow executable-bit repair and targeted independent re-verification.
