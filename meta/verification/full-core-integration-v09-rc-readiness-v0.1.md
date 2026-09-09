# Full-Core Integration Verification / v0.9 RC Readiness v0.1

Status: **INDEPENDENT VERIFICATION REPORT — Issue #129 (not a repair, not VERIFIED/RELEASED)**
Verification base: `main @ d6641e8e2053f86a0c3a09c02d274554bfd0fbcf`
Date: 2026-09-08

---

## 1. Exact verification base

| Item | Value |
|---|---|
| Canonical base (locked by Issue #129) | `d6641e8e2053f86a0c3a09c02d274554bfd0fbcf` |
| Actual `git rev-parse HEAD` at verification | `d6641e8e2053f86a0c3a09c02d274554bfd0fbcf` — **PASS (exact match)** |
| Branch | `verification/issue-129-full-core-v09-rc-readiness` |
| Merge-base | `d6641e8e2053f86a0c3a09c02d274554bfd0fbcf` — **PASS (== base)** |
| Ahead/behind | ahead `1` (this report commit only), behind `0` — **PASS** |
| Working tree at start | clean except untracked agent session directory `.commandcode/` (not course content, never committed) |

All runtime evidence below belongs to the exact base `d6641e8e2053f86a0c3a09c02d274554bfd0fbcf`; no historical PR/Executor/Lead runtime was relabeled as current evidence.

## 2. Verifier role / independence statement

This verification was performed in the **Independent Technical Integration Verification Engineer** role under Issue #129. The verifier is not the author or repair Executor of the M00–M24 material under review. No file of the verified material was modified during this verification (see §22). Defects are recorded, classified, and routed; nothing was repaired inside this PR.

## 3. Environment matrix

| Capability | Windows host | WSL2 Ubuntu (verification Linux env) |
|---|---|---|
| OS / kernel | Windows 11 10.0.26200, AMD64 | Ubuntu 24.04, kernel `6.18.33.2-microsoft-standard-WSL2`, x86_64 |
| Python | CPython 3.13.1 (MSC 64-bit) | CPython 3.12.3 |
| C compiler | MinGW-Builds gcc 14.2.0 (non-canonical host) | gcc (Ubuntu 13.3.0) — canonical `cc` |
| curl | 8.21.0 (Schannel) | 8.5.0 (OpenSSL 3.0.13) |
| sqlite3 CLI | NOT INSTALLED | NOT INSTALLED initially; **provisioned 3.45.1 during verification** (`apt-get install sqlite3`) |
| QEMU RISC-V | NOT FOUND | QEMU 8.2.2 (Debian 1:8.2.2+ds-0ubuntu1.18) |
| RISC-V toolchain | NOT FOUND | riscv64-linux-gnu-gcc 13.3.0 (+ xv6's riscv64-unknown-elf) |
| gdb | mingw gdb (host) | GNU gdb 15.1 |
| make / perl / bc / git | present | make 4.3, git 2.43.0, present |
| strace | — | NOT installed (preflight truthfully reports MISSING) |

The verification used two runtimes:
- **Windows host** (native CPython 3.13.1) for the committed Python suites;
- **WSL2 Ubuntu 24.04** on a clean LF checkout (`git archive` of the exact base extracted to `/tmp/verify-tree`, ext4) for the canonical-Linux surfaces: M03/M04 shell flows, LAB-REQ-02 xv6 build/QEMU, LAB-REQ-03 gcc `-pthread`, LAB-REQ-04 sqlite3 CLI, LAB-REQ-05, and the bash preflight.

WSL2 is a genuine Linux userspace on a Linux kernel, but it is **not bare-metal Linux**; WSL2-specific relay/emulation artifacts are called out in §20 and never relabeled as course defects.

## 4. 25-module / 70-Lesson inventory

- **Module directories:** `labs/foundations/` contains `m00-m01` plus `m02`–`m24` (24 directories representing exactly the 25 Core modules M00–M24). **PASS — 25/25.**
- **Learner Lesson files:** `book/**/Lxx-yy.md` contains exactly **70** files.
- **No duplicate Lesson IDs** — **PASS** (all 70 unique).
- **No missing Lesson IDs** — **PASS**: per-module counts exactly match the canonical map (S1: 9, S2: 8, S3: 12, S4: 10, S5: 9, S6: 12, S7: 10).
- **No post-M24 module/lesson** — **PASS** (no `M25`/`L25-` anywhere in lessons).
- Six non-lesson companion files are correctly present as reference guides (LAB-OPT-02/03/05, EXP-02/03/05).

## 5. Lesson structural / DAG audit

- All 70 lessons carry their implementation-era section structure (M00–M01 pilot format; M02+ 17-field numbered format). Automated scan found **no accidental empty major sections** (single flagged "thin" section is a two-bullet prerequisite list — legitimate), **no `<details open>` answer-first leakage** (0 hits), **no prefilled learner/reviewer PASS** (all regex hits were anti-fabrication rules such as "绝不伪造 PASS"), and **no M25+ leakage** (0 hits). **PASS.**
- DAG stage-boundary sampling — **PASS**, edges verified in `meta/blueprint/dependency-graph-v0.1.md`:
  - S1→S2: M01/M02 → M03 (H); S2→S3: M03 → M06 (H), M04 → M07 (H);
  - S3→S4: M06 → M10 (H); S3→S5: M08/M09 → M13 (H), M06 → M15 (H);
  - S5→S6: M15/M10 → M16 (H), M14 → M17 (H);
  - S6→S7: M20 → M23 (H), M21 → M23 (H), M23 → M24 (H), soft edges as documented.
  - No hidden prerequisite drift found; acyclicity per the Issue #9 topological method remains intact.

## 6. Concept / competency audit

- Concept Registry has 18 entries (`EC-CON-001`–`EC-CON-018`). All `EC-CON-xxx` references found in the 70 lessons **resolve** (0 unresolved IDs). All 18 canonical **first homes** exist as lesson files and reference their ID (spot-verified: EC-CON-001/002/004/005 in L00-01; EC-CON-003 L01-01; EC-CON-006 L02-02; EC-CON-007/008/009 L02-03; EC-CON-010 L03-03; EC-CON-011 L04-01; EC-CON-012 L04-02; EC-CON-013/017 L07-01; EC-CON-018 L06-01; EC-CON-016 L09-01; EC-CON-014 L14-02; EC-CON-015 L15-01). **PASS — no first-home drift.**
- Competency mappings use the 8 canonical labels (Trace/Explain/Observe/Diagnose/Correctness/Judge/Estimate/Learn-New-Tech); automated scan found **no invalid competency label** (all suspect regex matches were false positives such as person names or ordinary English words). **PASS.**

## 7. Executable verification inventory (actual tree)

Python unittest surfaces (26):
`labs/foundations/m00-m01/test_activity.py`, `m02/test_activity.py`, `m05`–`m16/test_activity.py`, `m17/test_trace.py`, `m18/test_m18.py`, `m19/test_m19.py`, `m20/test_m20.py`, `m21/test_m21.py`, `m22/test_m22.py`, `m23/test_m23.py`, `m24/test_m24.py`, `labs/lab_req_01/test_lab.py`, `labs/lab_req_03/test_lab.py`, `labs/lab_req_04/test_lab.py`, `labs/lab_req_05/test_lab.py`.

Shell/C surfaces (4):
`labs/foundations/m03/{preflight,build,inspect,capture-gdb,observe-failure,smoke-test,reset}.sh` + `fixture.c`/`failure.c`;
`labs/foundations/m04/{run.py,benchmark.c,reset.sh}`;
`labs/lab-req-02-xv6-syscall/{preflight,setup,smoke,reset}.sh` + `verify_source_route.py`;
`scripts/preflight-m05-m09.sh`.

Preflight Python surfaces (4): `tests/preflight_network_web.py`, `tests/preflight_data_concurrency.py`, `tests/preflight_distributed_infra.py`, `tests/preflight_security_synthesis.py`.

**M03/M04 have no `test_*.py` by design** (`unittest discover` returns "NO TESTS RAN", exit 5) — their verification is via the shell flows above.

## 8. Full Python / Core regression matrix

Command per suite: `python3 -m unittest discover -s <dir> -p 'test_*.py'` (documented canonical invocation; direct `-m unittest labs...` import style also recorded where applicable).

Linux (WSL2 Ubuntu, clean LF tree at base):

| Suite | Result | Suite | Result |
|---|---|---|---|
| m00-m01 (8) | **PASS** | m17 (15) | **PASS** |
| m02 (9) | **PASS** | m18 (14) | **PASS** |
| m05 (9) | **PASS** | m19 (20) | **PASS** |
| m06 (7) | **PASS** | m20 (36) | **PASS** |
| m07 (4) | **PASS** | m21 (15) | **PASS** |
| m08 (12) | **PASS** | m22 (20) | **PASS** |
| m09 (16) | **PASS** | m23 (23) | **PASS** |
| m10 (10) | **1 FAIL** (V-129-02, ENVIRONMENT) | m24 (23) | **PASS** |
| m11 (4) | **PASS** | lab_req_01 (6) | **PASS** |
| m12 (6) | **PASS** | lab_req_03 (8) | **PASS** |
| m13 (4) | **PASS** | lab_req_04 (6) | **PASS** |
| m14 (5) | **PASS** | lab_req_05 (7) | **PASS** |
| m15 (4) | **PASS** | | |
| m16 (5) | **PASS** | | |

Total: **296 tests, 295 PASS, 1 FAIL** (M10 cleanup probe under WSL2 localhost relay — environment-classified, see V-129-02; the same suite passes 10/10 on the native Windows host).

Windows host (native CPython 3.13.1): the same 26 suites — all suites that ran green on Linux also ran green on Windows **except** the three environment-limited modules: m00-m01 (1 ERROR: `change.py` prints Chinese to a cp1252 console — encoding limitation), m07 (1 ERROR: `mmap.MAP_PRIVATE/MAP_ANONYMOUS` unavailable on Windows; 1 skip: `/proc/self/maps` absent — capability-gated correctly), m08 (3 ERRORs: Windows refuses `os.unlink` on an open file — the POSIX open-unlink semantics being taught). m10 passes **10/10 on Windows** (no relay). Shared preflight discovery: **10/10 OK**.

## 9. Preflight matrix

| Surface | Result |
|---|---|
| M03 `preflight.sh` | **PASS** (cc/objdump/nm/gdb 15.1/git all present; x86_64) |
| `scripts/preflight-m05-m09.sh` | **PASS** — M06/M07/M08/M09 host capability PASS; LAB-REQ-02 `RUNNABLE`; `strace` truthfully `MISSING` |
| `tests/preflight_network_web.py` | **PASS** — curl gate `YES` (8.5.0); optional tools truthful (traceroute/tcpdump UNAVAILABLE; openssl AVAILABLE; Chromium recheck NOT_REQUESTED) |
| `tests/preflight_data_concurrency.py` | **PASS** — READY for M15+LAB-REQ-03; `sqlite3` CLI REQUIRED PASS; `-std=c11 -pthread`/atomics/mutex-cond/watchdog REQUIRED PASS; psql OPTIONAL UNAVAILABLE/SKIP |
| `tests/preflight_distributed_infra.py` | **PASS** — M16–M20 READY; all REQUIRED PASS; OQ-BP-006 OPEN/UNRESOLVED |
| `tests/preflight_security_synthesis.py --module M21/M22/M23/M24` | **PASS** — all REQUIRED capabilities PASS; argon2 OPTIONAL NOT INSTALLED/NOT RUN; M24 `defense_evaluation` REVIEWER-REQUIRED boundary preserved |
| `python -m unittest discover -s tests -p "preflight*.py"` | **PASS** — 10/10 |

No preflight was modified to make the machine pass. Absent capabilities are reported as absent.

## 10. Required Lab 1–5 DoD / runtime matrix

### F1. LAB-REQ-01 — PASS
DoD fields present in README (goal/prereqs/prediction/steps/observations/break/cleanup/exit/provenance/smoke). Runtime in WSL2 Linux with **real `curl 8.5.0`**: harness `ALL_STEPS_PASSED` — step 1 direct origin 200 (no `Via`), step 2 forwarded 200 (`Via: 1.1 essential-cs-intermediary`), step 3 conditional `If-None-Match` 304 with 0 body bytes, step 4 stopped origin → 502 with course `Via`; lifecycle `reaped=True old_endpoints_closed=True`. Tests 6/6 PASS. Reset: `CLEAN_NO_PERSISTENT_ARTIFACTS`.

### F2. LAB-REQ-02 — mechanism PASS, committed smoke FAIL (blocker V-129-01)
- Capability preflight **PASS** (QEMU 8.2.2 + riscv64 toolchain present — this environment is the first in project history to hold the full Required toolchain).
- Source pin/setup: canonical origin `https://github.com/mit-pdos/xv6-riscv.git`, exact HEAD `35b088427ef37611c38afdeed5a52a278cae38f9`, upstream `LICENSE` present — **PASS** (WSL HTTPS egress to github.com was broken — plain HTTP 301 OK, TLS no response — so the clone was performed from the Windows host into the WSL tree with the identical pin/origin/license checks; environment limitation recorded).
- `verify_source_route.py` **PASS**: `SYS_pause == 13`, dispatcher `[SYS_pause] -> sys_pause`, `sys_pause(void)`, user declaration, generated stub `a7 → ecall → ret`, trap `scause 8`, trampoline `uservec`.
- Build (`make fs.img kernel/kernel`) **PASS**; disassembly relation `main → pause stub → ecall` **PASS**.
- QEMU boot to `init: starting sh` **PASS**.
- Learner `sleep` behavior (paced interactive run): no-arg `Usage: sleep ticks` observed; `sleep 10` returned; executed `echo LAB_REQ_02_OK` observed — **PASS** (full Required mechanism evidence).
- Committed `smoke.sh`: **FAIL, deterministic 2/2** in this environment — see blocker V-129-01 (routing: SIMPLE FIX; not repaired here).
- Reset **PASS** (worktree restored to clean pin; no orphan QEMU process).

### F3. LAB-REQ-03 — PASS
Canonical Linux + `gcc -std=c11 -pthread`. Runner: CP1 deterministic UB-free lost update (5/5 rounds, actual=5 vs expected=10, `Shared-counter data-race UB: False`); CP2 natural scheduler observation (10000 iterations → 10726/20000, lost update manifested); CP3 mutex repair (20000/20000 invariant preserved); CP4 condition-variable rendezvous (predicate recheck guard True); CP5 controlled deadlock + watchdog (preconditions proven, child reaped rc=-15). Tests 8/8 PASS. Reset clean.

### F4. LAB-REQ-04 — PASS
Mandatory `sqlite3` CLI gate satisfied (provisioned 3.45.1; Python module NOT substituted). Harness `PASS`: unindexed `SCAN orders`; indexed `SEARCH orders USING INDEX idx_orders_user`; result equivalence rows=18 hash-matched; symmetric repeated-read timing; write/storage cost delta (303104→356352 bytes; bulk insert 10.14→12.22 ms); changed-workload planner choice `SEARCH_INDEX`. Tests 6/6 PASS. Reset: zero lingering files.

### F5. LAB-REQ-05 — PASS
All five checkpoints PASS on Linux (embedded SQLite 3.45.1, DELETE journal mode): committed visibility across two connections; bounded writer conflict (structural `database is locked`); explicit rollback restoration (600/400, sum 1000); owned-child interruption & reopen recovery (child reaped, balances restored, honest inference limit — "Client process kill proves client crash recovery via rollback journal, NOT OS crash survival or physical power-loss durability"); backup & storage boundary. Tests 7/7 PASS.

### F6. Five-Lab disposition table

| Lab | Environment capability | README/DoD | Test/smoke result | Cleanup | Limitation | Disposition |
|---|---|---|---|---|---|---|
| LAB-REQ-01 | curl 8.5.0 (Linux) | complete | tests 6/6; 4-step real curl trace ALL_STEPS_PASSED | clean | none | **PASS** |
| LAB-REQ-02 | QEMU 8.2.2 + RISC-V toolchain | complete | build/route/disassembly/boot/learner-sleep PASS; committed `smoke.sh` FAIL 2/2 (V-129-01) | clean pin, no orphans | smoke robustness defect → repair | **FAIL (one committed surface; mechanism PASS)** |
| LAB-REQ-03 | Linux gcc 13.3 `-pthread` | complete | runner 5/5 CP PASS; tests 8/8 | clean | none | **PASS** |
| LAB-REQ-04 | sqlite3 CLI 3.45.1 (provisioned) | complete | harness PASS; tests 6/6 | clean | CLI not preinstalled (OQ-BP-006 open) | **PASS** |
| LAB-REQ-05 | Python + SQLite 3.45.1 | complete | runner 5/5 CP PASS; tests 7/7 | clean | WSL2 timing = environment-specific evidence | **PASS** |

## 11. Cleanup / reset results

All applicable course-owned resets executed and idempotent: m00-m01, m10, m11, m21, m22, m23, m24, lab_req_01 (2×), lab_req_03, lab_req_04, lab_req_05, m03, m04, lab-req-02. Only course-owned scratch removed; no learner-owned or source data deleted; no orphan owned child process found (QEMU/pgrep check clean; harnesses report reaped children). **PASS.**

## 12. Cross-stage integration findings

- Shared helpers/preflight regressions: all preflight surfaces run at base; later-stage preflights (distributed, security) run green against earlier-stage fixtures. **PASS.**
- Reset isolation: every reset is scoped to its own directory/scratch and idempotent (verified by double-run where promised). **PASS.**
- Stage boundary continuity: §5 DAG audit — all sampled H edges resolve to existing material; no hidden prerequisite introduced. **PASS.**

## 13. Mini Cloud P0–P9 mapping audit

- Mapping exists and is internally consistent across `meta/CURRICULUM_MAP.md` (milestone → constraint → module home → competency), `meta/blueprint/final-reconciliation-v0.1.md` §6 (canonical per-milestone detail), and `meta/blueprint/mini-cloud-curriculum-alignment-v0.1.md` (earliest safe entry / primary home / mechanism ownership).
- Every milestone points at existing Module/Lesson/Lab evidence (M00–M24 all exist; LAB-REQ-01..05 all exist and are runnable — verified above).
- No milestone depends on a missing Required mechanism.
- M24 conceptually consumes prior milestone evidence (sample dossier references the LAB-REQ-05 executable fixture and the 12 evidence areas).
- The repository contains **no `project/` directory and no deployable Mini Cloud tree** — consistent with the authoritative blueprint treatment of Mini Cloud as a recurring milestone mapping, not a separately committed application. Not a fabricated claim; not a v0.9 blocker; remains a v1.0-tracked item (D-024 "complete Mini Cloud App"). See V-129-04.

## 14. Evidence-template assessment audit

33 evidence templates exist (26 module templates + 5 Required Lab templates + pilot/EXP companions). Spot-checks across all seven Stages and all five Required Labs: neutral initial state (`<actual ...>` / `[Record ...]` placeholders), no fabricated runtime output, no prefilled learner PASS, reviewer fields unfilled, cleanup fields truthful, environment/runtime identity fields present, machine-vs-reviewer distinction explicit (e.g., M23 "Machine PASS != learner competency PASS"; M24 reviewer-owned fields). **PASS.**

## 15. Provenance / rights / source-route audit

- **Zero third-party vendoring in Required Core** — `git ls-files labs` contains no xv6, OSTEP, CS:APP, or CS144 source; the LAB-REQ-02 xv6 tree is runtime-cloned, not committed. **PASS.**
- Rights-gated Optional Labs remain Strictly Optional / link-only with explicit zero-vendoring statements (LAB-OPT-02 CS144, LAB-OPT-03 PostgreSQL, LAB-OPT-05 OSTEP verified in the companion guides). **PASS.**
- Course-owned PKI material labeled: M11 `certs/` documented as "public localhost test fixtures, not secrets; never reuse for a real service". **PASS.**
- LAB-REQ-02 source pin/route internally consistent: pin `35b088427ef37611c38afdeed5a52a278cae38f9` identical in README, SOURCE_PIN.md, setup.sh, smoke.sh, and verified against the live upstream at clone time. **PASS.**
- Per-lab provenance/license statements present in all 5 Required Lab READMEs (RFC 9110 link/paraphrase; xv6 MIT + lab-page CC BY scope; POSIX link/paraphrase + original code; SQLite public-domain statement). **PASS.**
- Bounded gap (V-129-06): `ATTRIBUTION.md` ledger is empty ("No third-party material has been incorporated yet") and `LICENSES/` contains only the policy README without the canonical full license texts. Since no third-party material is actually incorporated, this is a **pre-release item**, not a v0.9 blocker; LICENSES/README itself schedules the full-text addition "before the first public content/code release".

No external source was bulk-rechecked; the only material currentness claim rechecked was the xv6 upstream HEAD/pin (via clone) because LAB-REQ-02 depends on it.

## 16. Safety / locality audit

- Network use is localhost/course-owned only (127.0.0.1 binds, port 0 allocation, `.local`/`.example`/`example.com` synthetic hosts); no public stress target.
- No real credentials: password/secret strings in `labs/` are synthetic teaching fixtures or `secrets.token_bytes` draws.
- No destructive production operations, no unrelated process killing (child/watchdog kill scoped to owned process groups, verified reaped).
- No learner-owned data deletion (resets scoped to course-owned scratch; idempotence verified).
- Optional live/cloud routes remain Optional and capability-gated (psql/argon2/Chromium/OpenTelemetry all OPTIONAL NOT RUN/SKIP where absent).
- **PASS — no safety violation found.**

## 17. Repository hygiene

At the verification base / report head: `git status --short` shows only the untracked agent session directory `.commandcode/`; `git diff --check` exit 0. Generated scratch before/after cleanup recorded (course-owned `.scratch` dirs removed by resets; no generated artifacts committed). The report commit introduces only `meta/verification/full-core-integration-v09-rc-readiness-v0.1.md`. **PASS.**

## 18. Current vs historical runtime ownership

| Layer | Status |
|---|---|
| Historical Executor runtime (PRs #33–#128) | Provenance only; NOT relabeled as this verification's evidence |
| Historical Lead runtime | Provenance only (several were ENVIRONMENT-BLOCKED, e.g., could not clone GitHub) |
| This Issue's independent verification runtime | All evidence in §§3–17 belongs to exact base `d6641e8e2053f86a0c3a09c02d274554bfd0fbcf` |
| Environment-blocked items | WSL2 HTTPS egress to github.com (worked around via host clone with identical pin checks); strace absent; native-Windows mmap/cp1252/open-unlink limits (§8) |

## 19. Open Questions disposition

- **OQ-BP-006 (canonical environment versions) — remains OPEN.** This verification recorded actual versions (Python 3.12.3/3.13.1, gcc 13.3/14.2, sqlite3 3.45.1, QEMU 8.2.2, curl 8.5.0/8.21.0, riscv toolchain 13.3.0) as capability evidence but does **not** declare a canonical pin. Governance rationale: implementation-time pin; bounded/deferred for v0.9 (capability-based verification suffices to demonstrate traversal reproducibility in the recorded environment); blocks the v1.0 stable-environment pin (RELEASE_AND_MAINTENANCE_POLICY "Stable environment"). **Not modified or closed.**
- **OQ-BP-001 (bounded AI literacy) — OPEN, RFC-gated.** Interim pattern (AI output = untrusted hypothesis; M00 L00-02 / M23 L23-02) verified intact. Does not block v0.9; blocks only a future Core-scope change.
- **OQ-BP-003 (human-facing boundary) — OPEN, RFC-gated.** Evidence hooks intact. Does not block v0.9.
- **Issue #34 (real learner validation) — OPEN, deferred under D-027.** Explicitly not satisfiable by this verification (see §21).

## 20. Blocker register

### V-129-01 — LAB-REQ-02 `smoke.sh` machine-checkable smoke fails deterministically in the verification environment (BLOCKING — SIMPLE FIX routing)
- **Location:** `labs/lab-req-02-xv6-syscall/smoke.sh` (Step 3 QEMU interaction).
- **Reproduction:** `./smoke.sh` at exact pin in WSL2 Ubuntu (QEMU 8.2.2) → `RuntimeError: missing-argument sleep usage output was not observed`; **2/2 deterministic**. Controlled experiments (ephemeral scripts, not committed):
  - burst-writing all three console commands immediately after `init: starting sh` → guest echoes the commands but executes none (0 `$` prompts in a 20s observation window, `PROBE_ALIVE` never executed); with 0.2–1.0s pre-delay the shell runs but the no-arg `sleep` usage line is still never captured (3/3);
  - fully paced single-command writes produce the complete Required evidence (usage line, `sleep 10` return, executed marker);
  - the smoke's `LAB_REQ_02_OK` marker check matches **guest-echoed input** (the command text itself contains the marker), so the marker is not execution evidence — demonstrated in a run where the guest executed nothing yet the marker check passed.
- **Expected:** burst-written commands execute and the usage output is captured; the marker proves execution.
- **Actual:** burst input either wedges the fresh xv6 guest console or loses the first command's output; the marker can be satisfied by echo alone.
- **Classification:** bounded robustness defect in the committed smoke script (script design contributes independently of environment: the echo-marker vacuity holds wherever the guest echoes input). The Required Lab **mechanism** itself is fully verified PASS via paced interaction + build/disassembly/boot checks.
- **Severity / readiness effect:** the only committed Required/Core surface that FAILs at base → v0.9 RC blocker under Issue #129 rules (not pure environment).
- **Recommended routing (no repair performed here):** `SIMPLE FIX` — (a) pace console writes with prompt-synchronized reads instead of one burst; (b) make the marker check require executed output (e.g., marker on its own line followed by the next `$ ` prompt, or an echo-free check), so it cannot match echoed input. Web Lead owns the repair decision.

### V-129-02 — M10 cleanup probe fails under WSL2 localhost relay (ENVIRONMENT — NOT a blocker)
- **Location:** `labs/foundations/m10/test_activity.py::test_dynamic_port_and_loopback_exchange` (cleanup probe).
- **Reproduction:** minimal repro (ephemeral): bind/accept/close on 127.0.0.1 in WSL2, then `connect_ex` immediately after close → **connected=True 5/5**; after 0.2s → ECONNREFUSED. The same suite passes **10/10 on the native Windows host** and the invariant is sound on non-relayed loopback.
- **Classification:** `ENVIRONMENT` (WSL2 localhost-forwarding relay teardown window). Routing: informational; no course repair indicated.

### V-129-03 — Windows-host environment limits for m00-m01/m07/m08 (ENVIRONMENT — NOT a blocker)
- m00-m01: `change.py` prints Chinese to a cp1252 Windows console → `UnicodeEncodeError` (Linux UTF-8: 8/8 PASS).
- m07: `mmap.MAP_PRIVATE|MAP_ANONYMOUS` absent on Windows (Linux: 4/4 PASS); `/proc/self/maps` skip is correct capability-gating.
- m08: `os.unlink` on an open file → `PermissionError WinError 32` (the POSIX open-unlink semantics being taught; Linux: 12/12 PASS).
- **Classification:** `ENVIRONMENT`; canonical environment is Linux per D-008. Routing: informational; optional cross-platform hardening for m00-m01 console encoding only.

### V-129-04 — No deployable Mini Cloud tree (NOT A BLOCKER / BOUNDED LIMIT)
- Repository has no `project/` directory. Per the authoritative blueprint the Mini Cloud App is a milestone mapping surface, not a separately committed app; P0–P9 mappings resolve to existing verified material. Tracked for v1.0 (D-024). Routing: Web Lead v1.0 governance.

### V-129-05 — sqlite3 CLI not preinstalled (NOT A BLOCKER / BOUNDED LIMIT)
- LAB-REQ-04's mandatory CLI gate requires the `sqlite3` binary; it was absent in both runtimes and provisioned (3.45.1) for this verification. Documented as environment provisioning; relates to OQ-BP-006 (no canonical pin). Routing: Web Lead to consider a documented provisioning step in the canonical environment image.

### V-129-06 — Attribution ledger / license texts not yet populated (NOT A BLOCKER / BOUNDED LIMIT)
- `ATTRIBUTION.md` has no entries; `LICENSES/` lacks full license texts. Accurate today because **no third-party material is incorporated**; LICENSES/README explicitly schedules full texts before first public release. Routing: Web Lead pre-release checklist.

## 21. What this verification does NOT establish

- Real learner validation — not performed; Issue #34 remains OPEN (AI cannot simulate it).
- External curriculum/coverage audit — not performed.
- `VERIFIED` / `RELEASED` state — not granted by this report.
- v1.0 readiness — no; v1.0 requires learner validation, external audit, operating maintenance, and zero critical blockers.
- No `v0.9` tag or release action was or may be performed by the verifier.
- WSL2 timing/emulation observations are environment-specific evidence, not universal hardware claims.

## 22. No-repair statement / verification PR scope

The verification PR diff contains only this report (`meta/verification/full-core-integration-v09-rc-readiness-v0.1.md`). No `book/**`, activity, validator, test, harness, runner, reset, preflight, Required Lab, evidence template, Research/Design, Registry, Matrix, Map, Decision, Open Question, PROJECT_STATUS, release policy, visual, or source pin was modified. All helper scripts used for verification were ephemeral and are not committed.

## 23. Final v0.9 RC readiness recommendation

**`NOT READY — BLOCKERS REQUIRE REPAIR`**

Rationale: 295/296 Python tests PASS, all preflights PASS, M03/M04 flows PASS, and four of five Required Labs are fully PASS with real canonical mechanisms. LAB-REQ-02's Required mechanism is fully verified PASS, but its committed machine-checkable `smoke.sh` fails deterministically at the locked base (V-129-01) and contains an environment-independent marker-vacuity defect. Under Issue #129's rules a failing committed Required surface is a v0.9 blocker unless purely environmental; V-129-01 is not purely environmental. The repair is small and well-scoped (`SIMPLE FIX` routing above). Everything else is PASS or truthfully classified (ENVIRONMENT / NOT A BLOCKER). After Web Lead disposition of V-129-01 (and optionally the bounded items V-129-04/05/06), the readiness re-review can proceed.
