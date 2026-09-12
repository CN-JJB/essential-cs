## Exact base / head lineage

- Canonical base (locked): `main @ d6641e8e2053f86a0c3a09c02d274554bfd0fbcf`
- Branch: `verification/issue-129-full-core-v09-rc-readiness`
- Exact final head: `6214e37c8dc35554d3b1a57f17c102b04cc6110d`
- Merge base: `d6641e8e2053f86a0c3a09c02d274554bfd0fbcf` (== canonical base)
- Ahead/behind: ahead `1` (this report commit only), behind `0`

## Changed paths

- `meta/verification/full-core-integration-v09-rc-readiness-v0.1.md` (new — the only changed path)

## Independence / no-repair statement

This PR is an independent verification deliverable. No file of the verified material (lessons, activities, validators, tests, harnesses, runners, resets, preflights, Required Labs, evidence templates, Research/Design, Registry/Matrix/Map, Decisions, Open Questions, PROJECT_STATUS, release policies, visuals, source pins) was modified. All verification helper scripts were ephemeral and are not committed.

## Environment matrix

- Host: Windows 11 (10.0.26200), AMD64, CPython 3.13.1; MinGW gcc 14.2.0 (host-only)
- Linux verification env: WSL2 Ubuntu 24.04 (kernel 6.18.33.2-microsoft-standard-WSL2), CPython 3.12.3, gcc 13.3.0, curl 8.5.0, sqlite3 CLI 3.45.1 (provisioned), QEMU 8.2.2, riscv64-linux-gnu-gcc 13.3.0, gdb 15.1, make 4.3; strace NOT installed (truthfully reported)
- Clean LF checkout of the exact base at `/tmp/verify-tree` used for all Linux runs

## Module / Lesson count

- 25 Core modules (M00–M24): PASS
- 70 learner Lessons: PASS (no duplicates, no missing IDs, per-module counts exactly match the canonical map S1 9 / S2 8 / S3 12 / S4 10 / S5 9 / S6 12 / S7 10; no M25+)

## Executable test summary

26 Python unittest surfaces + 4 shell/C surfaces + 4 preflight surfaces (full inventory in the report §7). Total: **296 tests — 295 PASS, 1 FAIL** (M10 cleanup probe under WSL2 localhost relay; same suite 10/10 PASS on native Windows host; classified ENVIRONMENT, not a blocker). Linux: all 26 suites green except that single M10 probe. Windows host additionally limited by native mmap/cp1252/open-file-unlink semantics in m00-m01/m07/m08 (all pass on Linux; ENVIRONMENT-classified). Shared preflight discovery: 10/10.

## 5 Required Lab matrix

| Lab | Result |
|---|---|
| LAB-REQ-01 | **PASS** — real curl 8.5.0 four-step trace `ALL_STEPS_PASSED`; tests 6/6; clean reset |
| LAB-REQ-02 | **Mechanism PASS; committed smoke.sh FAIL (blocker V-129-01)** — exact pin + source route + build + disassembly `main→pause stub→ecall` + QEMU boot + paced learner sleep evidence all PASS; `smoke.sh` FAIL 2/2 (burst-write console race + marker matches echoed input). Routing: SIMPLE FIX |
| LAB-REQ-03 | **PASS** — real Linux gcc 13.3 `-pthread`; 5/5 checkpoints incl. defined UB-free lost update, mutex repair, CV rendezvous, deadlock watchdog; tests 8/8 |
| LAB-REQ-04 | **PASS** — real sqlite3 CLI 3.45.1; SCAN→SEARCH, result equivalence, write/space cost, changed-workload plan; tests 6/6 |
| LAB-REQ-05 | **PASS** — 5/5 checkpoints incl. committed visibility, writer conflict, rollback, child-interruption recovery with honest inference limit, backup boundary; tests 7/7 |

## Preflight summary

M03 preflight PASS (incl. gdb); `scripts/preflight-m05-m09.sh` PASS (LAB-REQ-02 RUNNABLE; strace truthfully MISSING); network/web PASS (curl gate YES); data/concurrency PASS (sqlite3 CLI + c11 -pthread + atomics + mutex/cond + watchdog); distributed/infra PASS (M16–M20 READY); security synthesis M21–M24 all REQUIRED PASS with M24 reviewer boundary preserved. No preflight modified.

## Integration summary

- Lesson structural audit PASS (no empty major sections, 0 `<details open>`, no prefilled learner/reviewer PASS, no M25 leakage).
- DAG stage boundaries verified (S1→S2→S3; S3→S4/S5; S4&S5→S6; S6→S7) with all sampled H edges resolving; no hidden prerequisite drift.
- Concepts: 18/18 registered; all lesson EC-CON references resolve; all 18 first homes verified intact. Competencies: 8 canonical labels valid, no drift.
- Evidence templates: neutral, reviewer fields unfilled, machine≠reviewer boundary preserved (33 templates spot-checked).
- Provenance/rights: zero third-party vendoring; Optional labs link-only; M11 certs labeled test fixtures; LAB-REQ-02 pin internally consistent (verified against live upstream).
- Safety: localhost/course-owned only, no real credentials, no destructive ops, no orphan processes. PASS.
- Mini Cloud P0–P9: mapping resolves to existing verified material; no deployable tree (per blueprint bounded — v1.0 tracked).
- M23/M24 synthesis: machine PASS stays separate from reviewer/learner judgment.

## Blocker table

| ID | Location | Classification | Severity | Routing |
|---|---|---|---|---|
| V-129-01 | `labs/lab-req-02-xv6-syscall/smoke.sh` | bounded robustness defect (not pure environment; marker can match echoed input) | **BLOCKING v0.9** | SIMPLE FIX (pace console writes; require executed-output marker) |
| V-129-02 | M10 cleanup probe under WSL2 relay | ENVIRONMENT | non-blocking | informational |
| V-129-03 | Windows mmap/cp1252/open-unlink limits | ENVIRONMENT | non-blocking | informational |
| V-129-04 | no deployable Mini Cloud tree | NOT A BLOCKER / BOUNDED LIMIT | v1.0 tracked | Web Lead v1.0 governance |
| V-129-05 | sqlite3 CLI not preinstalled (provisioned) | NOT A BLOCKER / BOUNDED LIMIT | OQ-BP-006 | document provisioning in canonical image |
| V-129-06 | ATTRIBUTION ledger empty; LICENSES lacks full texts | NOT A BLOCKER / BOUNDED LIMIT | pre-release item | Web Lead release checklist |

Full reproduction evidence, expected vs actual, and severity notes are in the report §20.

## NOT RUN / BLOCKED table

- WSL2 HTTPS egress to github.com broken (plain HTTP works) — clone performed from Windows host with identical pin/origin/license checks; recorded.
- strace: NOT installed (preflight truthfully reports MISSING; no lab relabels absence as PASS).
- psql (LAB-OPT-03), argon2 (optional), live Chromium recheck (EXP-03), OpenTelemetry live route: OPTIONAL NOT RUN / SKIP per design.
- Bare-metal Linux (non-WSL) run: NOT RUN (no bare-metal Linux host available); WSL2 is a genuine Linux userspace but not bare metal, and is recorded as such.

## Cleanup

All applicable course-owned resets run and idempotent (m00-m01, m03, m04, m10, m11, m21–m24, lab_req_01 ×2, lab_req_03/04/05, lab-req-02). No learner-owned data touched; no orphan owned processes; `git status --short` clean except untracked session dir; `git diff --check` exit 0 at final head.

## Open Questions

- OQ-BP-006: remains OPEN (capability-based evidence recorded; no canonical pin declared). Bounded for v0.9; blocks v1.0 stable pin.
- OQ-BP-001 / OQ-BP-003: OPEN, RFC-gated; interim patterns verified intact; do not block v0.9.
- Issue #34 (real learner validation): OPEN, deferred under D-027; not satisfiable by this verification.

## Final recommendation

**`NOT READY — BLOCKERS REQUIRE REPAIR`** — one blocker (V-129-01, LAB-REQ-02 `smoke.sh`, SIMPLE FIX routing). All other gates PASS or are truthfully classified (ENVIRONMENT / NOT A BLOCKER). The Required Lab mechanism itself is verified; after Web Lead disposition of V-129-01 the readiness re-review can proceed.

## Non-claims

- No real learner validation implied; Issue #34 remains real-human evidence.
- No external curriculum/coverage audit implied.
- No `VERIFIED` / `RELEASED` state granted; no v0.9 tag created by the verifier.
- No v1.0 readiness implied.
- Merge of this PR does not change any content state; Web Lead owns tag/status governance.
