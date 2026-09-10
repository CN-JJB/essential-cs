# LAB-REQ-02 Direct-Invocation Final Re-Check v0.1

Status: **INDEPENDENT VERIFICATION REPORT — Issue #137 (not a repair, not VERIFIED/RELEASED)**
Verification base: `main @ 8e867153c64106e718cd4c4770df138f9b2ea700`
Verification branch: `verification/issue-137-lab-req-02-direct-invocation`
Runtime window (UTC): `2026-09-10T02:45:02Z` – `2026-09-10T02:45:52Z`
Final recommendation: **`READY FOR WEB LEAD v0.9 RC REVIEW`**

This report is the narrow closure verification of **V-133-01**. It re-checks only whether a fresh Linux materialization of the merged repository runs the documented LAB-REQ-02 `./...` workflow directly, with **no chmod or equivalent permission mutation**. It is not a rerun of the Issue #129 Full-Core matrix, and it does not re-adjudicate the Issue #131 semantic smoke repair beyond the negative predicate re-derivation recorded in section 12.

---

## 1. Exact canonical base

| Item | Value |
|---|---|
| Locked canonical base | `8e867153c64106e718cd4c4770df138f9b2ea700` |
| `git rev-parse HEAD` at verification start | `8e867153c64106e718cd4c4770df138f9b2ea700` — **PASS (exact match)** |
| `git rev-parse origin/main` after fetch | `8e867153c64106e718cd4c4770df138f9b2ea700` — **PASS** |
| Merge-base with `origin/main` | `8e867153c64106e718cd4c4770df138f9b2ea700` — **PASS (== base)** |
| Ahead/behind at start | ahead `0`, behind `0` |
| Base commit subject | `chore(status): enter LAB-REQ-02 direct-invocation re-check (#137)` |
| Working tree at start | clean except pre-existing untracked agent session directory `.commandcode/` |

Commands:

```bash
git fetch origin
git checkout main
git reset --hard origin/main
git rev-parse HEAD
git status --short
```

No silent base substitution was performed. After this report commit the branch is ahead of the locked base by this report only.

---

## 2. Verifier independence statement

Role: **Independent Technical Integration Verifier**.

This session is not the Issue #135 / PR #136 repair Executor and did not author the repaired Git file modes. It did not modify any verified material:

- `labs/lab-req-02-xv6-syscall/preflight.sh`, `setup.sh`, `smoke.sh`, `reset.sh`, `README.md`
- tests, preflights, source pin, licenses, Lessons, `meta/PROJECT_STATUS.md`, policies, prior verification reports

No file of the material under review was modified. Defects, if found, would have been recorded, classified, and routed — not repaired. No new defect was found, so no routing action was required.

Allowed committed change: this report only.

All runtime evidence was produced by **this session's own** fresh Linux materializations. The Issue #135 Executor's direct-run evidence (recorded in `meta/PROJECT_STATUS.md`) was **not** reused as this verification's runtime.

Ephemeral artifacts, none committed:

- `/tmp/issue-137.tar`, `/tmp/issue-137-direct/**` (archive materialization)
- `/tmp/issue-137-clone/**` (clone materialization)
- verification-only learner fixture `user/sleep.c` + `$U/_sleep` inside the gitignored xv6 worktree
- `%TEMP%\i137_*.sh`, `%TEMP%\i137_fixture.py`, `%TEMP%\i137-*-run.log`

Verifier AI self-claim comment: posted on Issue #137 as `CLAIMED BY INDEPENDENT VERIFIER AI` before any verification work began.

---

## 3. Environment identity

| Capability | Windows host | WSL2 Ubuntu (canonical Linux verification environment) |
|---|---|---|
| OS / kernel | Windows 11, AMD64 | Ubuntu 24.04.4 LTS (Noble Numbat), `6.18.33.2-microsoft-standard-WSL2`, x86_64 |
| Verification identity | — | `uid=0(root)`, `umask 0022`, `nproc 24`, 15 GiB RAM |
| Storage of runtime tree | — | WSL2 ext4 `/dev/sdd` (not drvfs) |
| Python | CPython 3.13.1 | CPython 3.12.3 |
| QEMU RISC-V | NOT FOUND | QEMU 8.2.2 (`Debian 1:8.2.2+ds-0ubuntu1.18`) |
| RISC-V GCC | NOT FOUND | `riscv64-linux-gnu-gcc` 13.3.0; xv6 build used `riscv64-unknown-elf-gcc` 13.2.0 |
| RISC-V objdump | NOT FOUND | GNU objdump 2.42 (`riscv64-unknown-elf-objdump` / `riscv64-linux-gnu-objdump`) |
| make / git | git 2.55.0.windows.5 | GNU Make 4.3 / git 2.43.0 |
| perl / bc / curl | — | perl v5.38.2 / bc 1.07.1 / curl 8.5.0 |
| strace | — | `MISSING` (unchanged; see V-129-05) |

Exact verification SHA: `8e867153c64106e718cd4c4770df138f9b2ea700`.

The Windows host has no RISC-V QEMU or cross-toolchain, so the WSL2 Ubuntu runtime is the independent Required-Lab environment, as in Issues #129 and #133.

---

## 4. Issue #135 / PR #136 repair ownership

| Item | Value | Confirmed |
|---|---|---|
| Issue #135 — `[Repair] LAB-REQ-02 executable entrypoints v0.1` | **CLOSED** (2026-09-09T14:32:28Z) | **PASS** |
| Repair PR #136 | **MERGED** (2026-09-09T14:31:27Z) | **PASS** |
| Repair head | `0295536b8e23c0400ac0bb0822650d9429372f44` | **PASS (exact)** |
| Merge commit | `6108df2aae7c599e8c6b01a38e322612cccce1fa` | **PASS (exact)** |
| Merge parents | `c65cba0` (main) + `0295536` (repair) | **PASS** |

Merge commit content audit (`git show --stat 6108df2a`): exactly four paths, **0 insertions / 0 deletions**, and four `mode change 100644 => 100755` entries.

```text
 labs/lab-req-02-xv6-syscall/preflight.sh | 0
 labs/lab-req-02-xv6-syscall/reset.sh     | 0
 labs/lab-req-02-xv6-syscall/setup.sh     | 0
 labs/lab-req-02-xv6-syscall/smoke.sh     | 0
 4 files changed, 0 insertions(+), 0 deletions(-)
```

**No later unexpected repair of the four shell files exists before this verification base.**

- `git log --oneline 6108df2a..HEAD -- labs/lab-req-02-xv6-syscall/` → **empty**.
- The only commit after the merge is `8e86715 chore(status): enter LAB-REQ-02 direct-invocation re-check (#137)`, which touches `meta/PROJECT_STATUS.md` only.
- Full path history of the four scripts since their introduction: `bc8e952` (initial LAB-REQ-02 packet) → `54bcf9e` / `2db5a83` / `8125b2a` (Lead hardening) → `e63ea2d` (Issue #131 smoke/license repair) → `0295536` (Issue #135 mode repair). Nothing after `0295536`.

**Result: PASS.**

---

## 5. Gate A — Git tree modes

```bash
git ls-tree HEAD \
  labs/lab-req-02-xv6-syscall/preflight.sh \
  labs/lab-req-02-xv6-syscall/setup.sh \
  labs/lab-req-02-xv6-syscall/smoke.sh \
  labs/lab-req-02-xv6-syscall/reset.sh
```

| File | Git mode at base | Required | Result |
|---|---|---|---|
| `labs/lab-req-02-xv6-syscall/preflight.sh` | `100755` | `100755` | **PASS** |
| `labs/lab-req-02-xv6-syscall/setup.sh` | `100755` | `100755` | **PASS** |
| `labs/lab-req-02-xv6-syscall/smoke.sh` | `100755` | `100755` | **PASS** |
| `labs/lab-req-02-xv6-syscall/reset.sh` | `100755` | `100755` | **PASS** |

`git ls-tree HEAD labs/lab-req-02-xv6-syscall/` confirms the surrounding non-executable files are unchanged (`README.md`, `SOURCE_PIN.md`, `fallback_trace.md`, `.gitignore`, `verify_source_route.py` all remain `100644`), so the repair was correctly scoped to shell entrypoints.

**Result: PASS — 4/4 `100755`, 0/4 `100644`.**

---

## 6. Gate B — Blob identity

Blobs resolved at the locked base via `git rev-parse HEAD:<path>`:

| File | Expected blob | Blob at base | Result |
|---|---|---|---|
| `preflight.sh` | `912dd79c308e789a174d0ffc40970ef8109e1b97` | `912dd79c308e789a174d0ffc40970ef8109e1b97` | **PASS (identical)** |
| `setup.sh` | `68510543528a2fea4f1a148f412c72f6c983d356` | `68510543528a2fea4f1a148f412c72f6c983d356` | **PASS (identical)** |
| `smoke.sh` | `40d815625dbfb9a873a919d06a133c5b754581df` | `40d815625dbfb9a873a919d06a133c5b754581df` | **PASS (identical)** |
| `reset.sh` | `201734795ee9b7197f7c55ac44a0fb126d334139` | `201734795ee9b7197f7c55ac44a0fb126d334139` | **PASS (identical)** |

These are the pre-#135 content blobs, so the repair is proven to be **mode-only**: script content did not drift.

Independent byte-level confirmation against the fresh Linux materialization (`cmp` of each extracted file against `git cat-file blob <expected-blob>`):

| File | `cmp` vs committed blob | SHA-256 of fresh file | Bytes |
|---|---|---|---|
| `preflight.sh` | IDENTICAL | `4347640e5c83b0ea16bae04759482d559478356242a8c7a896827cdeec5b7696` | 1812 |
| `setup.sh` | IDENTICAL | `b05c73366d21214d2b2134fd8cb403bfad5f640cef7b62f1d8c462ad700f53c4` | 1817 |
| `smoke.sh` | IDENTICAL | `c86bddb3e14a489eefd98f2cf7d7aff579de4b5f7bf950cb3bd68f420b9dc85b` | 8696 |
| `reset.sh` | IDENTICAL | `5c80aedcfda77518b1d566db4af0b09c6ecc7346c11768c294cfc0f67c057c75` | 1493 |

All four files are LF in both the committed objects and the fresh Linux tree (no CR bytes; `cmp` against the `i/lf` blob is byte-exact). The Windows `core.autocrlf=true` working-tree conversion did not contaminate the verification tree.

**Result: PASS — mode-only repair, content unchanged.**

---

## 7. Gate C — Fresh Linux materialization and the explicit no-chmod statement

> **No chmod or equivalent permission mutation was performed before the direct-invocation verification.**
>
> No `chmod`, `chmod +x`, `install -m`, `setfacl`, permission-changing `tar`/`cp`/`rsync` option, or any other permission mutation was executed at any point in this verification, before or after the direct-invocation runs. No `umask` change was made. The four permissions observed in section 8 are exactly the permissions produced by materialization from the Git tree; they were never rewritten.

Two **new** independent Linux materializations were created from the locked base. Neither reuses the Issue #135 Executor's tree.

### Method 1 — `git archive` extraction (`/tmp/issue-137-direct`)

```bash
cd /mnt/g/ai_project/research/cs
git -c core.autocrlf=false archive --format=tar HEAD > /tmp/issue-137.tar
tar -tvf /tmp/issue-137.tar | grep -E 'lab-req-02-xv6-syscall/(preflight|setup|smoke|reset)[.]sh'
tar -xf /tmp/issue-137.tar -C /tmp/issue-137-direct
```

| Provenance item | Value |
|---|---|
| Archive SHA-256 | `ef9da7c26341d524411f4bf40cd77279700cc6a334d4964063a11bf39fe147dd` |
| Archive size | 6,133,760 bytes, 513 members |
| Archive rendering of the four scripts | `-rwxrwxr-x` (execute bits recorded in the archive itself) |
| Extraction command | plain `tar -xf` — no `--mode`, no `--no-same-permissions`, no post-extraction fix |

### Method 2 — fresh Linux clone (`/tmp/issue-137-clone`)

```bash
git -c core.autocrlf=false clone --quiet /mnt/g/ai_project/research/cs /tmp/issue-137-clone
git -c core.autocrlf=false -C /tmp/issue-137-clone checkout --quiet --detach \
  8e867153c64106e718cd4c4770df138f9b2ea700
```

This reproduces what a learner actually receives from a normal Linux `git clone` / `git checkout`, because it honors the Git tree mode directly rather than an archive rendering.

The **full documented workflow** (preflight → setup → source route → learner fixture → smoke → reset) was executed **directly** in **both** materializations, giving two independent real-QEMU PASS runs.

---

## 8. Gate D — Recorded fresh permissions before any lab script ran

Recorded **before** any lab command was invoked, in both fresh trees:

| Materialization | `stat -c '%A %a %n'` before first script run | Owner execute |
|---|---|---|
| `/tmp/issue-137-direct` (git archive) | `-rwxrwxr-x 775` × 4 (`preflight.sh`, `setup.sh`, `smoke.sh`, `reset.sh`) | **present** |
| `/tmp/issue-137-clone` (fresh checkout) | `-rwxr-xr-x 755` × 4 | **present** |

Ownership: `root:root` (`uid=0:gid=0`); type `regular file` for all four.

The archive materialization renders `0775` rather than `0755` because `git archive` masks the tree mode with an archive-derived umask (`0777 & ~002`, applied to `100755`). This is a tar-rendering artifact, not a repository property:

- Git tree authority remains `100755` (section 5).
- The real Linux checkout — the learner-facing path — yields exactly `0755`.

Re-stat after both complete workflows returned the identical values, confirming no permission mutation occurred anywhere in the workflow. **Execute bits were present in both materializations, `./...` direct invocation worked, and Git tree authority is `100755`.**

**Result: PASS.**

---

## 9. Gate E — Direct `./preflight.sh`

Invoked exactly as documented, directly (never as `bash preflight.sh`):

```bash
cd /tmp/issue-137-direct/labs/lab-req-02-xv6-syscall
./preflight.sh
```

| Materialization | Output tail | Exit code | `Permission denied` / rc=126 | Result |
|---|---|---|---|---|
| archive | `STATUS: PASS — Required LAB-REQ-02 build/smoke capabilities are present.` | `0` | absent | **PASS** |
| clone | `STATUS: PASS — Required LAB-REQ-02 build/smoke capabilities are present.` | `0` | absent | **PASS** |

Detected capabilities: git 2.43.0, GNU Make 4.3, python3 3.12.3, perl, bc 1.07.1, RISC-V GCC + objdump pair (`riscv64-linux-gnu`), QEMU RISC-V 8.2.2. No capability BLOCKED; the script launched and executed directly.

**Result: PASS — direct execution, no executable-bit failure, capability PASS.**

---

## 10. Gate F — Direct `./setup.sh`

```bash
./setup.sh
```

| Check | archive run | clone run | Result |
|---|---|---|---|
| Exit code | `0` | `0` | **PASS** |
| Canonical origin | `https://github.com/mit-pdos/xv6-riscv.git` | same | **PASS** |
| Exact pin | `35b088427ef37611c38afdeed5a52a278cae38f9` | same | **PASS** |
| `HEAD is now at 35b0884 test for nlink overflow` | observed | observed | **PASS** |
| Upstream license file present | `${WORKTREE_DIR}/LICENSE` reported | same | **PASS** |
| `=== Setup Complete ===` | observed | observed | **PASS** |

Upstream license identity in the pinned worktree: 1,174 bytes, SHA-256 `677302f30c9882c1f81b9be8ceda6efd4edff5576b9e02963b6114cf70c3162c`, Git blob `af50cb2508331d748e7fa5340ec882720f24f1af`, MIT-style permission grant (`Copyright (c) 2006-2024 Frans Kaashoek, Robert Morris, Russ Cox, Massachusetts Institute of Technology` + the standard "Permission is hereby granted, free of charge…" / "THE SOFTWARE IS PROVIDED \"AS IS\"" text). The file is the canonical upstream `LICENSE`; it does not literally contain the phrase "MIT License", which is expected for this upstream.

**Result: PASS — canonical origin, exact pin, upstream license present, setup completes directly.**

---

## 11. Gate G — Source route

```bash
python3 verify_source_route.py worktree
```

Both runs: `STATUS: PASS — Exact pin and current pause/sys_pause route verified.` Exit code `0`.

| Route anchor | Observed | Result |
|---|---|---|
| Exact pin | `HEAD == 35b088427ef37611c38afdeed5a52a278cae38f9` | **PASS** |
| `SYS_pause` | `#define SYS_pause 13` | **PASS** |
| Stale route absent | no `SYS_sleep` / `sys_sleep` in `syscall.h`/`syscall.c`/`sysproc.c`/`usys.pl` | **PASS** |
| Dispatcher | `[SYS_pause] -> sys_pause` | **PASS** |
| Kernel implementation | `sys_pause(void)` | **PASS** |
| User prototype | `int pause(int);` in `user/user.h` | **PASS** |
| Syscall stub generator | `entry("pause")` → `li a7, SYS_${name}` → `ecall` → `ret` | **PASS** |
| Trap route | `usertrap` + `r_scause() == 8` + `syscall()` | **PASS** |
| Trampoline | `uservec:` present | **PASS** |
| Learner `pause(...)` call | reported as "learner `user/sleep.c` not present yet" **before** the fixture; after the fixture the route re-check is covered by `smoke.sh` step 2 and by the direct route run recorded in section 15 | **PASS (see note)** |

Note: `python3 verify_source_route.py worktree` was deliberately run **before** the learner fixture was introduced (gate order in the Issue contract), so it correctly reported the upstream-only route. The learner-side `pause(...)` anchor is independently confirmed by `smoke.sh` step 2 disassembly (`main -> pause stub -> ecall`) in both runs, and by the fixture source audit in section 12.

**Result: PASS — route unchanged.**

---

## 12. Gate H — Verification-only learner input

Prepared **only** inside the dedicated gitignored xv6 worktree (`labs/lab-req-02-xv6-syscall/worktree/`, excluded by `labs/lab-req-02-xv6-syscall/.gitignore` line 1 `worktree/`).

| Item | Value |
|---|---|
| `user/sleep.c` | original verification-only C, 228 bytes |
| `Makefile` | `$U/_sleep\` inserted immediately after the `$U/_zombie\` line inside `UPROGS` |
| Fixture correctness | validates `argc != 2` → `fprintf(2, "Usage: sleep ticks\n")` + `exit(1)`; else `ticks = atoi(argv[1]); pause(ticks); exit(0);` |
| Uncommitted | yes — `git status --porcelain` inside the xv6 worktree showed ` M Makefile` and `?? user/sleep.c` |
| Course repo source | untouched |

This is a runtime verification fixture only. It was never committed, and `reset.sh` removed it (section 14).

**Result: PASS.**

---

## 13. Gate I — Real direct smoke (`./smoke.sh`, no chmod)

```bash
./smoke.sh     # invoked directly, never as `bash smoke.sh`
```

Executed in **both** materializations. Committed script, unmodified, blob `40d815625dbfb9a873a919d06a133c5b754581df`.

Observed guest console (byte-identical contract in both runs):

```text
xv6 kernel is booting

hart 2 starting
hart 1 starting
init: starting sh
$ sleep
Usage: sleep ticks
$ sleep 10
$ echo LAB_REQ_02_OK
LAB_REQ_02_OK
$ 
```

Script-reported verdicts, both runs:

```text
MARKER_SELF_CHECK: PASS
QEMU_SMOKE_STATUS: PASS
USAGE_OUTPUT_OBSERVED: YES
SLEEP10_RETURNED: YES
EXECUTION_MARKER_OBSERVED: YES
QEMU_REAPED: TRUE
PID_MARKER_CLEAN: YES
=== LAB-REQ-02 Smoke Test PASS ===
```

| Run | Materialization | UTC window | Exit | Shell reached | `Usage: sleep ticks` | `sleep 10` returned | Standalone `LAB_REQ_02_OK` | Following `$ ` | `QEMU_REAPED` | PID file after | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `/tmp/issue-137-direct` (git archive) | 2026-09-10T02:45:02Z–02:45:33Z | `0` | **PASS** | **PASS** (output line, not command echo) | **PASS** | **PASS** | **PASS** | `TRUE` | absent | **PASS** |
| 2 | `/tmp/issue-137-clone` (fresh checkout) | 2026-09-10T02:45:39Z–02:45:52Z | `0` | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | `TRUE` | absent | **PASS** |

Supporting build/disassembly evidence from the same runs:

- `make fs.img kernel/kernel` completed from a **fresh upstream clone of the exact pin** in both runs (`riscv64-unknown-elf-gcc` 13.2.0, `riscv64-unknown-elf-ld`), including `user/_sleep` linked into `mkfs/mkfs fs.img README … user/_sleep …`.
- Step 2: `[+] Disassembly relation verified: main -> pause stub -> ecall.`
- Step 3 self-check: `MARKER_SELF_CHECK: PASS`.
- Only benign upstream linker notes appeared (`has a LOAD segment with RWX permissions` for `user/_forktest` and `kernel/kernel`), which are expected for the pinned xv6 build.

**Independent echo-only predicate re-derivation.** The predicate in committed `smoke.sh` was re-implemented independently and run against constructed buffers (`normalize`, `has_prompt` = ends with `"$ "`, `has_execution_marker` = a stripped line equal to `LAB_REQ_02_OK`):

| Buffer | `has_execution_marker` | `execution_marker_satisfied` | Expected | Result |
|---|---|---|---|---|
| `init: starting sh\n$ echo LAB_REQ_02_OK\n` | False | False | (False, False) | OK |
| that buffer plus trailing `$ ` | False | False | (False, False) | OK |
| `$ echo LAB_REQ_02_OK\n` | False | False | (False, False) | OK |
| `echo LAB_REQ_02_OK\n$ ` | False | False | (False, False) | OK |
| `$ echo LAB_REQ_02_OK\necho LAB_REQ_02_OK\nLAB_REQ_02_OK\n$ ` | True | True | (True, True) | OK |
| standalone marker without following prompt | True | False | (True, False) | OK |
| `Usage: sleep ticks\n$ ` | False | False | (False, False) | OK |
| full real-session buffer | True | True | (True, True) | OK |

`INDEPENDENT_MARKER_PREDICATE: PASS`. The real QEMU console shows the echoed command line and the execution line as two distinct lines; only the latter plus the following prompt satisfies the predicate.

**This proves the required property: the fresh materialization's own repository permissions were sufficient to execute `./smoke.sh` directly — the run was not enabled by a temporary chmod.**

**Result: PASS — 2/2 real QEMU PASS, direct invocation, no permission mutation.**

---

## 14. Gate J — Direct reset (`./reset.sh`, no chmod)

```bash
./reset.sh     # invoked directly, never as `bash reset.sh`
```

Both runs exited `0` with `=== Reset Complete ===`.

| Check (post-reset, both runs) | Observed | Result |
|---|---|---|
| Worktree HEAD is exact pin | `35b088427ef37611c38afdeed5a52a278cae38f9` | **PASS** |
| `git status --porcelain` in worktree | empty | **PASS** |
| Learner `user/sleep.c` | `sleep.c present: NO` | **PASS** |
| `$U/_sleep` in `Makefile` | `0` matches | **PASS** |
| Build residue `kernel/kernel` | `ABSENT` | **PASS** |
| Build residue `fs.img` | `ABSENT` | **PASS** |
| Build residue `user/_sleep` | `ABSENT` | **PASS** |
| Build residue `user/usys.o` | `ABSENT` | **PASS** |
| `.qemu_smoke.pid` | `ABSENT` | **PASS** |
| Owned QEMU process | none | **PASS** |

`git clean -fdx` output additionally enumerated removal of the full build residue set (`*.o`, `*.d`, `*.asm`, `*.sym`, `user/usys.S`, `mkfs/mkfs`, `fs.img`, `kernel/kernel`, all `user/_*`) plus `user/sleep.c`, and `git reset --hard` restored `Makefile`.

**Result: PASS — exact pin restored, learner input and build residue removed, no QEMU, no PID marker.**

---

## 15. Cleanup / reap / PID evidence

| Evidence | Run 1 (archive) | Run 2 (clone) |
|---|---|---|
| `QEMU_REAPED` | `TRUE` | `TRUE` |
| `PID_MARKER_CLEAN` | `YES` | `YES` |
| `.qemu_smoke.pid` after smoke | absent | absent |
| `.qemu_smoke.pid` after reset | absent | absent |
| `find … -name '*.pid'` under both materializations | no match | no match |
| Host-level QEMU process check | no match | no match |

The authoritative reap claim is `smoke.sh`'s own assertion: cleanup closes stdin, sends `SIGTERM` to the owned process group (`os.killpg` on the `start_new_session=True` leader), waits, escalates to `SIGKILL`, and raises `owned QEMU process group was not reaped` if `poll()` is still `None`; `reaped=True` is only set after a confirmed reap, and the PID file is unlinked only after that.

**Verifier-side method correction (recorded for honesty).** The host-level process check originally used `pgrep -a qemu-system-riscv64`, which can never match because `pgrep` matches the 15-character `comm` field and the command name is longer; `pgrep` printed that warning to stderr and returned no match. That check was therefore **not** valid evidence on its own. It was re-run correctly with `ps -eo pid,ppid,etimes,args | grep -i 'qemu-system'` and `pgrep -af 'qemu-system'`; both reported no match after all four script runs (28 processes total in the namespace, none QEMU). This is a defect in the verifier's own check command, **not** in any verified material, and the reap/PID conclusion is unchanged.

**Result: PASS.**

---

## 16. Targeted regression

Run against the fresh materialization `/tmp/issue-137-direct` (Linux) plus Windows parity where relevant. The full 296-test Core matrix was **NOT RUN** by contract: Issue #129 remains the accepted full-Core baseline and no new failure evidence required expansion.

| Surface | Command | Result |
|---|---|---|
| Shell syntax ×4 | `bash -n labs/lab-req-02-xv6-syscall/{preflight,setup,smoke,reset}.sh` | **PASS** — all four RC=0 |
| M06 (WSL2 / CPython 3.12.3) | `python3 -m unittest discover -s labs/foundations/m06 -p "test_*.py"` | **PASS** — `Ran 7 tests in 1.066s`, `OK` |
| M06 (Windows / CPython 3.13.1) | `python -m unittest discover -s labs/foundations/m06 -p "test_*.py"` | **PASS** — `Ran 7 tests in 0.158s`, `OK (skipped=5)` (Windows capability gating; 0 failures) |
| Shared M05–M09 preflight | `bash scripts/preflight-m05-m09.sh` | **PASS** — RC=0; M06/M07/M08/M09 host capability `PASS`; LAB-REQ-02 `RUNNABLE`; `strace: MISSING (not installed)` reported truthfully |
| Source-route | `python3 verify_source_route.py worktree` | **PASS** (×2 runs) |
| LAB-REQ-02 preflight | `./preflight.sh` | **PASS** (direct) |
| LAB-REQ-02 setup | `./setup.sh` | **PASS** (direct) |
| LAB-REQ-02 smoke | `./smoke.sh` | **PASS** (direct, ×2 real QEMU) |
| LAB-REQ-02 reset | `./reset.sh` | **PASS** (direct) |
| Whitespace | `git diff --check` | **PASS** — exit 0 |

**Result: PASS — no regression evidence.**

---

## 17. V-133-01 closure decision

V-133-01 — *LAB-REQ-02 shell entrypoints are non-executable in the Git tree* — closes only if all ten conditions hold.

| # | Closure condition | Evidence | Result |
|---|---|---|---|
| 1 | Git tree shows all four `100755` | section 5 | **PASS** |
| 2 | Expected blob IDs preserved (content unchanged) | section 6 | **PASS** |
| 3 | Fresh Linux materialization | section 7 (two independent materializations) | **PASS** |
| 4 | No chmod / no permission mutation | section 7 / section 8 | **PASS** |
| 5 | Direct `./preflight.sh` succeeds | section 9 (RC=0 ×2) | **PASS** |
| 6 | Direct `./setup.sh` succeeds | section 10 (RC=0 ×2, exact pin, canonical origin, license) | **PASS** |
| 7 | Direct real `./smoke.sh` succeeds | section 13 (RC=0 ×2, real QEMU PASS, `Usage: sleep ticks`, `sleep 10` returned, standalone `LAB_REQ_02_OK` + prompt) | **PASS** |
| 8 | Direct `./reset.sh` succeeds | section 14 (RC=0 ×2) | **PASS** |
| 9 | Cleanup truthful | section 15 (`QEMU_REAPED: TRUE`, `PID_MARKER_CLEAN: YES`, no residue) | **PASS** |
| 10 | Targeted regression acceptable | section 16 | **PASS** |

## **V-133-01 = CLOSED**

The learner-documented workflow `./preflight.sh` → `./setup.sh` → `python3 verify_source_route.py worktree` → `./smoke.sh` → `./reset.sh` now executes directly from a fresh Linux materialization of the merged repository, with no chmod or equivalent permission mutation, and a real QEMU smoke PASS was observed in two independent materializations.

---

## 18. Prior findings reconciliation

No historical classification is changed without new evidence. No new blocker was found by this re-check.

| ID | Prior classification | This re-check | Closure |
|---|---|---|---|
| **V-129-01** | BLOCKING — LAB-REQ-02 committed smoke false-positive / burst interaction; routed SIMPLE FIX; closed by Issue #133 | Indirectly re-confirmed at the corrected base: committed `smoke.sh` (blob `40d8156…`) ran to real QEMU PASS twice with prompt-paced interaction, standalone-marker-only acceptance, and `MARKER_SELF_CHECK: PASS`; independent predicate re-derivation PASS (section 13). No new false-positive path observed. | **CLOSED** (unchanged) |
| **V-129-06** | release-hygiene gate — canonical Apache-2.0 / CC BY-SA 4.0 texts required before public v0.9 tag/release; closed by Issue #133 | Not re-verified in this narrow re-check (out of scope; no new evidence, no new risk). Committed `LICENSES/Apache-2.0.txt` and `LICENSES/CC-BY-SA-4.0.txt` are untouched by #135/#136. | **CLOSED** (unchanged) |
| **V-129-02** | ENVIRONMENT — WSL2 M10 localhost-relay cleanup probe | No new M10 evidence collected (full matrix NOT RUN by contract). | **ENVIRONMENT / unchanged** |
| **V-129-03** | ENVIRONMENT — Windows m00–m01/m07/m08 limits | Windows M06 this session: 7 tests, 5 skipped, 0 failures — consistent with the prior bounded-host characterization; no new course defect. | **ENVIRONMENT / informational — unchanged** |
| **V-129-04** | bounded — no deployable Mini Cloud tree (D-024, v1.0-tracked) | No `project/` tree introduced; out of scope. | **bounded / v1.0-tracked — unchanged** |
| **V-129-05** | bounded environment/governance — sqlite3 CLI provisioning / OQ-BP-006 | `strace: MISSING` and the environment-provisioning gap are unchanged; OQ-BP-006 remains OPEN. | **bounded environment/governance — unchanged; OQ-BP-006 remains OPEN** |
| **V-133-01** | BLOCKING — SIMPLE FIX (four entrypoints committed `100644`) | Repaired by Issue #135 / PR #136; **independently direct-invocation verified here**. | **CLOSED** (§17) |

---

## 19. New defects found

**None.**

No defect was found in the verified material. Consequently no classification (`SIMPLE FIX` / `COMPLEX REWORK` / `ARCHITECTURE` / `ENVIRONMENT` / `NOT A BLOCKER / BOUNDED LIMIT`) and no routing to Web Lead was required.

One **informational, non-blocking** observation is recorded for completeness:

- **`git archive` mode rendering.** `git archive` emitted the four entrypoints as `-rwxrwxr-x` (`0775`) rather than `0755`, because it masks the tree mode with an archive-derived umask. Execute bits are present either way, and a genuine Linux checkout yields exactly `0755`. **Classification: `NOT A BLOCKER / BOUNDED LIMIT`** — a property of tar rendering, not of the repository. Anyone verifying executable bits should prefer a real clone/checkout, or compare against `git ls-tree`.

One **verifier-side method correction** (not a defect in verified material) is recorded in section 15: `pgrep -a qemu-system-riscv64` cannot match because of the 15-character `comm` limit; the host-level process check was re-run correctly.

---

## 20. NOT RUN / BLOCKED

| Item | Status | Reason |
|---|---|---|
| Full 296-test Core matrix | **NOT RUN** | Issue #129 remains the accepted Full-Core baseline; no new failure evidence required expansion |
| Windows-host LAB-REQ-02 QEMU smoke | **NOT RUN** | No QEMU RISC-V / RISC-V cross-toolchain on the Windows host |
| Official MIT course-fork `grade-lab-util` | **NOT RUN** | Not present at the pinned xv6 commit; README already declares it NOT RUN |
| Live `strace` | **NOT RUN** | Shared preflight reports `MISSING`; not required for this re-check |
| V-129-06 license byte/hash comparison | **NOT RUN** | Out of this Issue's narrow scope; unchanged material; Issue #133 accepted baseline retained |
| M10 WSL2 relay re-probe (V-129-02) | **NOT RUN** | No new evidence; historical ENVIRONMENT classification retained |
| Issue #34 real learner validation | **NOT RUN** | Separate mandatory gate; an AI cannot satisfy it |
| v0.9 tag / GitHub Release | **NOT RUN** | Out of verifier authority |
| Web Lead executable re-run | **NOT RUN by this session** | Web Lead authority; the Lead container's GitHub resolution limit is a separate, already-recorded environment constraint |

Nothing in this table substitutes for the independent QEMU evidence in section 13. No gate relevant to V-133-01 was left BLOCKED.

---

## 21. Repository hygiene

At verification start and before the report commit:

```text
git status --short
?? .commandcode/
git diff --check      # exit 0
git diff --name-only  # (empty)
git diff --cached --name-only  # (empty)
```

`.commandcode/` is a pre-existing untracked agent session directory and is not course content.

**No verified material appears in `git diff --name-only`.** The four shell entrypoints, `README.md`, `verify_source_route.py`, tests, preflights, licenses, Lessons, `PROJECT_STATUS.md`, policies, and prior verification reports were not modified.

The verification branch commit adds only:

`meta/verification/lab-req-02-direct-invocation-recheck-v0.1.md`

Deliberately **not** committed:

- `/tmp/issue-137.tar` and both materializations `/tmp/issue-137-direct/**`, `/tmp/issue-137-clone/**`
- the xv6 worktree / upstream clone
- verification-only learner `user/sleep.c` and the `$U/_sleep` `Makefile` edit
- xv6 build outputs (`kernel/kernel`, `fs.img`, `user/_sleep`, `*.o`, `*.d`, `*.asm`, `*.sym`, `user/usys.S`)
- `.qemu_smoke.pid`
- ephemeral drivers/logs (`%TEMP%\i137_*.sh`, `%TEMP%\i137_fixture.py`, `%TEMP%\i137-*-run.log`)
- `.commandcode/`

Pre-existing local state disclosure: a Windows-side `labs/lab-req-02-xv6-syscall/worktree/` directory exists from an earlier local run. It is excluded by `labs/lab-req-02-xv6-syscall/.gitignore` (`worktree/`), is not authored by this session, and was **not** used as evidence for this verification.

---

## 22. Explicit non-claims

This report does **not** establish:

- that a `v0.9` tag exists, has been created, or may be created by this verifier;
- that a public release has been published;
- real learner validation (Issue #34 remains OPEN / deferred under D-027);
- `VERIFIED` or `RELEASED` lifecycle states;
- v1.0 readiness;
- closure of OQ-BP-006;
- a Mini Cloud deployable tree;
- that Issue #129's full-Core matrix was rerun at this SHA;
- that Issue #131's license-text gate was re-adjudicated here (V-129-06 rests on the accepted Issue #133 baseline);
- that this verification was performed by the Issue #135 repair Executor — it was not;
- anything about the Web Lead's own final governance decision.

A `READY FOR WEB LEAD v0.9 RC REVIEW` recommendation means only that:

- the accepted Issue #129 full-Core baseline exists;
- the Issue #131 smoke/license repairs passed independent re-verification (Issue #133);
- the Issue #135 file-mode repair now passes fresh-Linux direct-invocation verification from the merged head;
- no known v0.9 technical/public-license blocker remains;
- the result may be handed to Web Lead for the final v0.9 RC governance decision.

---

## 23. PR execution trace / work log

**Starting state.** Assigned base `8e867153c64106e718cd4c4770df138f9b2ea700`; starting HEAD was the pre-existing local branch `repair/issue-135-lab-req-02-executable-bits` at `0295536b8e23c0400ac0bb0822650d9429372f44` (the #135 repair head, i.e. the previous session's branch — **not** this agent's work). Worktree clean apart from pre-existing untracked `.commandcode/`. `git fetch origin` advanced `origin/main` `c65cba0..8e86715`; `git checkout main` + `git reset --hard origin/main` locked the base; branch `verification/issue-137-lab-req-02-direct-invocation` created at that exact SHA.

**Actions performed.**

1. Checked Issue #137 state, comments (0), open PRs referencing it (0), and remote branch presence (absent) — confirmed no active claim; posted the `CLAIMED BY INDEPENDENT VERIFIER AI` comment **before** any verification work.
2. Confirmed Issue #135 CLOSED, PR #136 MERGED, repair head `0295536…`, merge commit `6108df2…`; audited the merge as 4 paths / 0 insertions / 0 deletions / 4 `100644 → 100755` mode changes; confirmed no later commit touched `labs/lab-req-02-xv6-syscall/`.
3. Read the four scripts, `README.md`, `verify_source_route.py`, `SOURCE_PIN.md`, and the prior Issue #133 report to fix the documented workflow and prior findings.
4. Ran Gate A/B (`git ls-tree`, `git rev-parse HEAD:<path>`) at the locked base.
5. Created materialization 1 via `git archive` (recorded tar SHA-256 and member modes) and materialization 2 via a real fresh Linux clone + detached checkout; verified modes and byte-identity against the committed blobs.
6. Ran the full documented workflow **directly** in both materializations: `./preflight.sh`, `./setup.sh`, `python3 verify_source_route.py worktree`, verification-only learner fixture, `./smoke.sh`, `./reset.sh` — capturing exit codes, guest console, reap/PID state, and post-reset assertions.
7. Ran targeted regression (`bash -n` ×4, M06 on Linux and Windows, `bash scripts/preflight-m05-m09.sh`, `git diff --check`) and an independent echo-only predicate re-derivation.
8. Collected license identity, environment identity, and corrected the host-level QEMU process check.
9. Wrote this report; committed it alone; pushed the branch; opened exactly one PR.

**Problems encountered and disposition.**

| # | Problem | Cause / diagnosis | Resolution | Verified |
|---|---|---|---|---|
| 1 | First archive listing grep returned nothing under `set -e` | Grep pattern/anchoring mismatch in an ephemeral driver script; the archive itself was fine | Re-ran the listing directly; archive contained all four members with `-rwxrwxr-x` | Yes — archive member listing |
| 2 | A `file <path>` call failed with `No such file or directory` for a path with a trailing `\015` | The ephemeral driver was written from a PowerShell here-string with CRLF line endings, so a trailing CR was appended to the last argument | Rewrote all drivers to LF via `[IO.File]::WriteAllText(... -replace "`r`n","`n")`; re-ran affected checks. This affected only the verifier's helper scripts, never the materialized tree (whose LF status is proven by byte-identity `cmp` against the `i/lf` blobs) | Yes — `cmp` IDENTICAL ×4 |
| 3 | `pgrep -a qemu-system-riscv64` printed a 15-character `comm` warning and could not match | `pgrep` matches the process name field, which is truncated to 15 characters; the command name is longer | Recorded as a verifier-side method defect and re-ran the host check correctly with `ps -eo … args` and `pgrep -af` — no QEMU process | Yes — see section 15 |
| 4 | A filtered clone-run log appeared to omit the fixture's `git status` lines | The output filter for that run did not include those patterns | Read the raw log file, which contains ` M Makefile` and `?? user/sleep.c` | Yes — raw log |

No problem was encountered with the verified material itself.

**Ownership boundary.** The only file authored by this agent is `meta/verification/lab-req-02-direct-invocation-recheck-v0.1.md`. The `100755` file modes, the four script contents, the smoke semantics, and the license texts are the work of earlier Executors/Lead and are explicitly not claimed here. The pre-existing local `repair/issue-135-…` branch and the Windows-side `labs/lab-req-02-xv6-syscall/worktree/` are prior-session local state, not this agent's.

**Residual risk / not-run work.** The Windows host cannot run the QEMU smoke, so all runtime evidence is WSL2-Linux-derived — the same constraint recorded in Issues #129 and #133. The full 296-test matrix was not rerun by contract. `strace` remains unavailable. The official MIT course-fork grader remains absent at the pinned commit. Issue #34 learner validation remains a separate mandatory human gate that no AI verification can discharge.

---

## 24. Final recommendation

**`READY FOR WEB LEAD v0.9 RC REVIEW`**

Rationale: at the exact locked base `8e867153c64106e718cd4c4770df138f9b2ea700`, all four LAB-REQ-02 shell entrypoints are committed as Git mode `100755` with their pre-#135 content blobs intact, proving the Issue #135 / PR #136 repair persisted as mode-only. Two independent fresh Linux materializations — a `git archive` extraction and a real `git clone` + detached checkout — each carried execute bits without any `chmod` or equivalent permission mutation and each ran the documented learner workflow **directly**: `./preflight.sh` (capability PASS), `./setup.sh` (canonical origin, exact pin `35b088427ef37611c38afdeed5a52a278cae38f9`, upstream MIT-style `LICENSE` present), `python3 verify_source_route.py worktree` (route unchanged), a real `./smoke.sh` producing a genuine QEMU PASS (`Usage: sleep ticks`, `sleep 10` returned to a following prompt, standalone `LAB_REQ_02_OK` plus prompt, `QEMU_REAPED: TRUE`, `PID_MARKER_CLEAN: YES`), and `./reset.sh` (exact pin restored, learner input and build residue removed, no owned QEMU, no PID marker). Targeted regression (`bash -n` ×4, M06 7/7 on Linux and Windows, shared M05–M09 preflight, `git diff --check`) passed. V-133-01 is therefore **CLOSED**, and with V-129-01 and V-129-06 already closed, no known v0.9 technical or public-license blocker remains. This recommendation does not create or tag v0.9, does not constitute a release, and does not imply learner validation, `VERIFIED`, `RELEASED`, or v1.0 readiness; the final v0.9 RC governance decision belongs to the Web Lead.
