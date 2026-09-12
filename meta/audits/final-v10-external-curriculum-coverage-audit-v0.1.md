# Final External Curriculum + Coverage Audit v0.1 — v1.0 Candidate

**Task:** Issue #157 — `[Audit] Final external curriculum + coverage audit v1.0 candidate`
**Role:** Independent External Curriculum / Coverage Auditor
**Audit base (`AUDIT_BASE`):** `97096c9dd7e30b27fa885f9c45a3c291380c908e` (`main` @ `[Governance] Resolve deferred v1.0 Core-scope questions (#155)`)
**Audit branch:** `audit/issue-157-final-v10-external-curriculum-coverage`
**Date (UTC):** 2026-09-12
**Status:** `READY FOR LEAD FINAL EXTERNAL AUDIT REVIEW` (audit report only; not `VERIFIED` / `RELEASED` / v1.0)

---

## 1. Auditor independence statement

This audit was performed in the **Independent External Curriculum / Coverage Auditor** role under Issue #157.
The auditor is **not the Web Lead**, and is **not the author, designer, implementer, verifier, or repair executor** of the material under audit. No material under audit was authored by this session.

No file of the audited object was modified during this audit:

- no Lesson / Lab / test / fixture / preflight / evidence-template change;
- no Research / Design / Registry / Matrix / Map / Decision / Open Question / PROJECT_STATUS change;
- no environment / CI / `project/` / lifecycle-state change;
- no prior verification or audit report change;
- Issue #34 was not touched, closed, or re-scoped.

Gaps found are classified and routed in this report. Nothing was silently repaired.
The only committed change allowed by the Task Contract is this file:

`meta/audits/final-v10-external-curriculum-coverage-audit-v0.1.md`

**Independence limits (disclosed):** this auditor read repository history authored by other agents and relied on committed CI/Actions provenance for some runtime claims (see §10). Any judgement here is about the authored artifact at `AUDIT_BASE`, not about those other sessions.

---

## 2. Base lock and scope

- At audit start, Issue #157 comments = **0** and open PRs = **none** → **no competing claim**. (Verified again at handoff.)
- `origin/main` at claim time: `97096c9dd7e30b27fa885f9c45a3c291380c908e` → recorded as `AUDIT_BASE`; a worktree was created at that exact SHA.
- **After** base lock, `main` advanced to `cd7396c`. Per the Issue base rule, this report remains **explicitly scoped to `AUDIT_BASE = 97096c9`**; the Web Lead decides whether later material changes require a refresh.
- Open issues at handoff: #34 (learner validation), #141 (handoff), #153 (durable pin re-verification), #157 (this audit), #158 (final stable multi-role verification), #161 (release gate). None duplicates this audit.

---

## 3. Evidence and source method

Three evidence classes are kept strictly separate, as the Task Contract requires:

1. **Repository / static evidence** — committed prose, maps, registries, code, tree modes, blob identity, file:line inspection at `AUDIT_BASE`.
2. **Executable evidence** — actual runs. Two sources:
   - **This auditor's own runs** on a non-canonical Windows host (see §10 for the exact commands and results);
   - **committed canonical CI/Actions provenance** from `meta/verification/stable-environment-ci-independent-verification-v0.1.md`, `meta/verification/maintenance-review-operating-evidence-v0.1.md`, `.github/workflows/{ci-fast,ci-qemu-lane,ci-mini-cloud}.yml` — cited as provenance, **not relabelled** as this auditor's runtime.
3. **External-source evidence** — live authoritative sources consulted on 2026-09-12 for materially time-sensitive claims (§8).

Mapping prose is never treated as implementation. Executor runtime is never relabelled as auditor runtime. Document existence is never counted as operating evidence.

---

## 4. Core coverage findings (M00–M24 / 70 Lessons)

### 4.1 Inventory — PASS

- `book/**/*.md` = **76 files** = **70 learner Lessons** + **6 non-lesson companions** (`LAB-OPT-02/03/05`, `EXP-02/03/05`).
- All 25 Modules M00–M24 present with the canonical lesson split (S1:9, S2:8, S3:12, S4:10, S5:9, S6:12, S7:10 = 70). Verified against `meta/blueprint/core-stage-module-lesson-map-v0.1.md` and `meta/verification/full-core-integration-v09-rc-readiness-v0.1.md`.
- No duplicate, missing, or extra Lesson IDs; no M25+ leakage.

### 4.2 Lesson structure — one MAJOR deviation, otherwise consistent

Two templates coexist (`M00–M12` unnumbered sections; `M13–M24` numbered 17-field), and both carry the Definition of Done content in the sampled cases.

- **F-04-01 (MAJOR, SIMPLE FIX)** — `book/04-memory-locality-measurement/L04-01.md` and `L04-02.md` **omit the explicit learning-objective, prerequisite, and provenance/time-sensitivity blocks** that `meta/DEFINITION_OF_DONE.md` requires. `L04-02.md` additionally has **no `What You Can Ignore—for Now`** field; `L14-02.md` is the only other Lesson missing that field. This matters because `L04-02` is the newly promoted **applied measurement-uncertainty / experimental-pattern first home** (`meta/CURRICULUM_MAP.md:82-83`), so its self-study scaffolding should be at least as strong as peer Lessons, not weaker.
- **F-04-02 (MINOR, SIMPLE FIX)** — `book/13-databases-storage-indexing/L13-01.md` and `book/15-concurrency-threads-races-synchronization/L15-01.md` (a Module first home with hard prerequisite M06) state **no prerequisites at all**, so required inputs are not discoverable from the Lesson (Module DAG remains authoritative; no contradiction).
- **F-04-03 (MINOR, SIMPLE FIX — documentation accuracy)** — `meta/verification/full-core-integration-v09-rc-readiness-v0.1.md` describes the template split as “M00–M01 pilot format; M02+ 17-field”. The actual split is M00–M12 unnumbered / M13–M24 numbered; the verification document's claim is inaccurate.

### 4.3 Dependency / DAG integrity — PASS

- `meta/blueprint/dependency-graph-v0.1.md` declares 62 edges (**40 H / 22 S**); the edge table and the Mermaid block agree 62/62; acyclicity holds on inspection; no backward `H` edges. (Static verification only; the repository's automated topological routine was not re-run by this auditor.)
- Stage-boundary lesson prerequisites sampled (S1/S2, S2/S3, S3/S4, S3/S5, S4/S6, S5/S6) are consistent with the Module DAG.
- **F-04-04 (MINOR, SIMPLE FIX)** — `book/11-networking-tls-http-cdn-proxies/L11-03.md:32` declares **`M04` as a hard prerequisite**, but no all-hard `M04→…→M11` ancestry path exists (the only route is via soft edges `M04→M09 S`, `M09→M10 S`). This violates the dependency-graph rule that lesson-level hard cross-module prerequisites must lie on an existing Module-`H` path. `book/08-files-filesystems-io/L08-02.md:30` likewise lists a `M04 L04-01` prerequisite that the map does not require.
- **F-04-05 (INFO, SIMPLE FIX)** — `book/10-networking-ip-dns-transport/L10-01.md:31` describes the M09 soft context as “分布式系统部分失败直觉”; M09 is storage/durability (partial failure is M16). Mis-description only.

### 4.4 First homes and duplication — PASS with one MAJOR contradiction

- **All 18 canonical first homes exist** as Lesson files and reference their Registry ID: `L00-01` (001/002/004/005), `L01-01` (003), `L02-02` (006), `L02-03` (007/008/009), `L03-03` (010), `L04-01` (011), `L04-02` (012), `L07-01` (013/017), `L14-02` (014), `L15-01` (015), `L09-01` (016), `L06-01` (018).
- No **second full canonical definition** was found for the checked concepts; several later Lessons explicitly defer (e.g. `L08-02.md:123-125,252` defers EC-CON-016 to M09; `L12-04.md:19,34` defers EC-CON-015 to M15).
- **F-04-06 (MAJOR, SIMPLE FIX) — concept contradiction.** `book/17-distributed-systems-replication-consistency-consensus/L17-03.md:16` states that in M14 the learner “first encountered `EC-CON-014 Consistency` — it means an **application-level conservation constraint**”. This is exactly the ACID-“C” confusion the Registry warns against: `meta/CONCEPT_REGISTRY.md:147-154` defines EC-CON-014 as *the relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee*, and its “Common confusions” explicitly separate ACID-C from visibility guarantees. The true first home (`L14-02.md:86-102`) states this correctly. A learner reaching M17 receives a factually wrong description of the canonical concept.
- **F-04-07 (MINOR, SIMPLE FIX)** — `book/13-databases-storage-indexing/L13-02.md:26` labels 抽象 (Abstraction) as `EC-CON-005 Interface`; Abstraction is `EC-CON-002`. Wrong ID.
- **F-04-08 (MINOR, SIMPLE FIX)** — `book/21-security-synthesis-trust-crypto/L21-01.md:42,89-94` goes beyond a bounded recap and re-derives the EC-CON-017 Trust Boundary definition and its isolation distinction. M21 is a scheduled synthesis revisit, so this is authorized in principle, but it is more than the “one-sentence recap + application” the Registry rule permits. Bounded editorial tightening, not a second full teaching.

---

## 5. Required Lab findings

Accepted selection: 5 Required Labs (`meta/blueprint/lab-source-selection-map-v0.1.md`; `meta/CURRICULUM_MAP.md:113-119`; `meta/COMPETENCY_MATRIX.md:80-88`). Tables agree exactly on module homes and assessed competencies.

### 5.1 Runnability and mechanism coverage — PASS (with executable evidence in §10)

- **LAB-REQ-01** — real stdlib origin with strong `ETag`/304-zero-body and a real intermediary that strips `Connection` options, sets truthful `Via`, and maps owned upstream failure to `502`; not an open proxy (405).
- **LAB-REQ-02** — real xv6 route; `verify_source_route.py` machine-checks `SYS_pause`/`sys_pause`/generated stub/`ecall`/trap dispatch, and `smoke.sh` runs a prompt-paced QEMU shell test with reap/cleanup. Executable on the canonical image only (`git clone` of the pinned tree at runtime; gitignored).
- **LAB-REQ-03** — real pthreads: defined C11-atomic compound lost update (`broken_counter.c`), mutex repair, predicate-loop condition-variable rendezvous, and an owned-child watchdog deadlock boundary. No simulator.
- **LAB-REQ-04** — real `sqlite3` CLI `EXPLAIN QUERY PLAN` before/after index, semantic plan categorisation, SHA-256 result-equivalence; no hard-coded planner outcome; CLI absence fails closed.
- **LAB-REQ-05** — two real connections, committed-only visibility, structurally classified BUSY conflict, explicit rollback, owned-child process-interruption recovery with an explicit non-power-loss inference limit, and a real online backup/restore.
- **No third-party vendoring** in `lab_req_01/03/04/05`; xv6 is runtime-cloned and gitignored. Consistent with `ATTRIBUTION.md`.

### 5.2 Curricular alignment — MAJOR gap (BLOCKER B-2)

The Required Labs are **not reachable from the learner’s Lessons for 3 of 5 cases**:

| Lab | Referenced from `book/`? | Form |
|---|---|---|
| LAB-REQ-01 | Yes | `L11-03.md:26,112,116` by ID |
| LAB-REQ-02 | **No** | `book/06/*` route to `labs/foundations/m06/*`; xv6 mentioned only in passing (`L06-01.md:77`) |
| LAB-REQ-03 | Yes | `L15-01.md:107-111`, `L15-02.md:110-118` by path; harness imported by `labs/foundations/m15/*` |
| LAB-REQ-04 | **No** | `L13-01.md:97` routes to `labs/foundations/m13/fixture_l13.py` |
| LAB-REQ-05 | **No** | `L14-01/02/03.md` route to `labs/foundations/m14/activity_l14_0*.py`; `LAB-REQ-05` appears only inside the Optional PostgreSQL guide as a non-dependency |

A self-study learner following `book/` is routed to *different* `labs/foundations/` fixtures, not to the canonical Required mechanism Labs. Because Invariant 14 (self-study first) and the Required-Lab assessment gate depend on learners actually reaching these Labs, this is a curricular-alignment blocker, not a cosmetic link gap.

### 5.3 Other Lab findings

- **F-05-01 (MAJOR, SIMPLE FIX)** — The accepted LAB-REQ-03 controlled-break set includes “remove or move one predicate wait/notification” and “use `if` instead of a predicate loop” (`lab-source-selection-map-v0.1.md:430-434`), and `COMPETENCY_MATRIX.md:84` names a “held/reversed predicate break”. **No such artifact exists** in `labs/lab_req_03/`; only the mutex-removed break and the reversed-lock break are runnable. The assessed evidence pattern is therefore not fully covered.
- **F-05-02 (MINOR, SIMPLE FIX)** — `lab_req_01` implements a 405 for unsupported methods but no harness/test exercises the accepted “malformed/unsupported request” or “non-matching cache validator” breaks.
- **F-05-03 (MINOR, SIMPLE FIX)** — Accepted LAB-REQ-04 “two bounded data sizes” is not exercised by the learner harness (`DEFAULT_ROW_COUNT = 5000` only; other sizes appear only in tests).
- **F-05-04 (MINOR, SIMPLE FIX)** — Accepted LAB-REQ-05 breaks “remove the transaction around a multi-step update” and “restore an old/missing backup” are not present as artifacts.
- **F-05-05 (MINOR, SIMPLE FIX)** — LAB-REQ-01/02/03/05 READMEs omit explicit prerequisites / prediction / exit-criteria / provenance sections (the DoD Lab list expects them); REQ-03/REQ-05 READMEs omit the `tests/preflight_data_concurrency.py` entry point.
- **F-05-06 (MINOR, SIMPLE FIX)** — `labs/lab_req_03/harness.py:399-405` requires a 5-event rendezvous order while `course/evidence/lab-req-03-evidence-template.md:81-85` lists only 4 events.
- **F-05-07 (MINOR, SIMPLE FIX)** — Lesson-declared competencies are narrower than the Matrix's assessed set for some Labs (M11 lacks Observe/Correctness/Trace; M14 lacks Observe/Estimate; M06 lacks Learn-New-Tech).
- **F-05-08 (INFO)** — LAB-REQ-05 uses the stdlib `sqlite3` module only (no CLI); this is permitted by the selection map, but `CURRICULUM_MAP.md:119` wording implies a `sqlite3` prerequisite — ambiguous, not wrong.

---

## 6. Mini Cloud P0–P9 findings

### 6.1 Implementation vs accepted mapping — PASS

- `project/` contains a runnable stdlib-only Python package (`project/minicloud/`, 16 modules), scripts, and 6 unittest modules; P0–P9 are represented as modules plus a README map table and milestone-pair tests. **All ten milestones are running code**, none documented-only.
- Every milestone exposes its declared constraint (P0 durable collection; P1 narrow interface; P2 trust boundaries; P3 ambiguous timeout; P4 query/index measurement; P5 transaction/conflict; P6 migration/backup/restore; P7 config/reproducibility; P8 redacted bounded-cardinality telemetry; P9 integrated walkthrough).
- **No mandatory excluded component** is present: no queue, cache, replica, container, proxy, PostgreSQL, framework, ORM, real IdP, or cloud deployment. `project/README.md:44-51,222-231` explicitly lists postponed/rejected components. Rejection remains a tested outcome. This matches D-006 and the `final-reconciliation-v0.1.md` §6 guardrails.
- No scope creep into web-development training.

### 6.2 Integration and linkage — MAJOR gap (BLOCKER B-1)

- **F-06-01 (BLOCKER, COMPLEX REWORK)** — The runnable Mini Cloud is **orphaned from the learner-facing curriculum**. `project/minicloud` / `minicloud.cli` appear **only** in `project/`, `.github/workflows/ci-mini-cloud.yml`, and `project/README.md` — **no `book/`, `course/`, or `labs/` file references it**. Only `book/24-final-system-defense/L24-01.md:26,78,150` mentions the “Mini Cloud” as a conceptual case, and `course/evidence/foundations-m24-evidence-template.md:10` leaves “Actual system under defense: [Record actual project/system]” generic.
- **F-06-02 (BLOCKER, COMPLEX REWORK)** — The M24 System Defense surface (`labs/foundations/m24/`) uses a **synthetic dossier** and does not consume `project/` (`L24-01.md:191` states the sample is synthetic). The D-006 chain “final assessment = System Defense over the evolving Mini Cloud App” is therefore not wired end-to-end.
- **F-06-03 (MAJOR, SIMPLE FIX)** — `meta/PROJECT_STATUS.md` at `AUDIT_BASE` is **stale**: “Last updated 2026-09-10”, active task still Issue #145, and it does not mention #146/#148/#150/#152/#154/#156/#159/#160, the realized environment pin, the Mini Cloud implementation, or D-033/D-034. The current state exists only in `meta/verification/maintenance-review-operating-evidence-v0.1.md` and `.devcontainer/CANONICAL_ENVIRONMENT.md`.

### 6.3 Other Mini Cloud findings

- **F-06-04 (MINOR, SIMPLE FIX)** — P1 ships the HTTP adapter unconditionally, while the alignment made HTTP conditional on M11/M12 (`mini-cloud-curriculum-alignment-v0.1.md:96`; `final-reconciliation-v0.1.md:113`). Permitted but a deviation from the literal contract.
- **F-06-05 (MINOR, SIMPLE FIX)** — P4's owner/time index is baked into canonical migration 2 (`schema.py:19,97-103`), so the “no-index baseline” exists only in a temp copy; the mapping says add an index only after a measured baseline.
- **F-06-06 (MINOR, SIMPLE FIX)** — P2 privacy: `service.py` `share_item`/`revoke_share` raise “no such user: {username}”, leaking grantee existence, and login/create log the raw username. This is a bounded username side channel, not a secrets exposure, but it is outside the P2 non-enumeration intent.
- **F-06-07 (MINOR, SIMPLE FIX)** — P3 introduces a third loopback process (link-indexer dependency) not enumerated in the P3 mechanism list; bounded, removable, and not an excluded mandatory component.
- **F-06-08 (MINOR, SIMPLE FIX)** — P0 ships a minimal ordered migration mechanism ahead of P6; minimal, not a framework.
- **F-06-09 (INFO)** — “One constraint per milestone” is design-level only (single PR #154 tree; no per-milestone history), so it cannot be checked incrementally.

---

## 7. Accepted AI / human-facing scope decision review (D-033 / D-034)

**No unintended scope expansion found.**

- **D-033 (bounded AI literacy).** No AI/ML/LLM Core module or new canonical thread exists. AI appears only as the accepted CURRENT CASE: `book/00-the-map/L00-02.md:213-262` and `book/23-systems-thinking-judgment/L23-02.md:124-142,320`, both explicitly declining to create an AI module. `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md:3` is marked `RESOLVED FOR v1.0 BY D-033`.
- **D-034 (human-facing boundary).** No new HCI/accessibility Core first home exists (repo-wide search for accessibility/WCAG/ARIA/screen-reader terms in `book/`, `course/`, `labs/`, `project/` returns no genuine Core content). `RFC-CAND-002` is marked resolved.
- **F-07-01 (MAJOR, SIMPLE FIX) — stale governance status in learner material.** Learner-facing content still asserts the **pre-decision** OPEN/RFC-GATED state that D-033 closed:
  - `book/00-the-map/L00-02.md:333` — “AI boundary preserves OQ-BP-001 safe interim state; this Lesson does not close that Open Question.”
  - `book/23-systems-thinking-judgment/L23-02.md:126,142,320` — “OQ-BP-001 安全过渡态 … OPEN / RFC-GATED（核对：2026-09）”.
  - `tests/preflight_security_synthesis.py:521,633-634` **asserts** `OQ_BP_001 == "OPEN / RFC-GATED (AI outputs treated as unverified candidate hypotheses)"`, so the test now **enforces** the outdated status and would fail if the Lesson were corrected.
  This is a truthfulness/consistency defect: a Decision has resolved the question, but learners and the test harness teach/require the obsolete state. The substantive AI-verification practice remains correct and is unaffected — only the lifecycle label is wrong.
- **F-07-02 (MINOR, SIMPLE FIX)** — `meta/CURRICULUM_MAP.md:84,147` and `meta/CONCEPT_REGISTRY.md:199-200` still describe OQ-BP-001/OQ-BP-003 as RFC-gated/open, predating D-033/D-034.
- **F-07-03 (MINOR, FUTURE REVIEW)** — D-034's accepted bounded hook (“accessibility consideration where relevant in Mini Cloud P2/P9 and existing browser/security contexts”) is **under-delivered**: P2/P9 and the browser Lessons contain denial/error/recovery/privacy hooks but no accessibility hook. This is under-delivery of accepted scope, not expansion.

---

## 8. Currentness / staleness review

### 8.1 External spot-checks — PASS

Materially time-sensitive claims were checked against live authoritative sources on 2026-09-12:

| Claim at `AUDIT_BASE` | External check | Verdict |
|---|---|---|
| `L11-01.md:264` RFC 9846 = TLS 1.3, Jul 2026, obsoletes RFC 8446 | rfc-editor.org / datatracker RFC 9846 | **Accurate** |
| `L11-01.md:267` RFC 9849 = TLS Encrypted Client Hello, Mar 2026 | rfc-editor.org RFC 9849 | **Accurate** |
| `L11-01.md:266` RFC 9525 Service Identity in TLS, Nov 2023, obsoletes RFC 6125 | rfc-editor.org RFC 9525 | **Accurate** |
| `L22-01.md:369` OAuth 2.1 = `draft-ietf-oauth-v2-1-16` | datatracker draft-ietf-oauth-v2-1 | **Accurate** |
| `L22-01.md:365` NIST SP 800-63B-4 (final) | csrc.nist.gov SP 800-63B-4 final | **Accurate** |
| `L15-03.md:55-59` Python free-threading = PEP 779 Phase II (supported, optional) | peps.python.org PEP 779 | **Accurate** |
| `L22-03.md:342` / `L19-03.md:285` SLSA v1.2 (2025) | slsa.dev spec v1.2 / v1.2 announcement | **Accurate** (approval Nov 2025; repo date 2025-11-24 is within tolerance) |

No examined currentness claim was found materially outdated for 2026.

### 8.2 Marking discipline — MAJOR gap (F-08-01, CURRENTNESS / SOURCE REFRESH)

Formal dated source tables exist **only in the late spine** (M19–M24; e.g. `L19-01.md:291`, `L20-01.md:285`, `L21-01.md:307`, `L23-01.md:338`, `L24-01.md:334`). They are **absent across M00–M18**, including the highest-risk network claims: `L11-01.md:264-267` (TLS/ECH/X.509) is the only load-bearing RFC source list with **no check date or STABLE/CURRENT/FRONTIER classification**, and `L12-01.md:115-134,216` carries Chromium current-practice claims without a recheck date (only `EXP-03` does). `meta/LIVING_CURRICULUM_POLICY.md:5-16` requires time-sensitivity classification. The claims are individually accurate today, but the currentness apparatus cannot triage them later without re-reading every Lesson.

### 8.3 Other currentness findings

- **F-08-02 (MINOR, SOURCE REFRESH)** — Volatile, already-labelled CURRENT items need periodic rechecks: Kafka 4.3.1 / Redis 8 licensing (`L23-02.md:315-316`), PostgreSQL 18.6 (`L17-01.md:318`; `EXP-02`), OpenTelemetry Python v1.44.0 (`labs/foundations/m20/optional_exp04_otel.py:18`, oldest check date 2026-07-16), AWS us-east-1 pricing (`L09-03.md:102`). All are Optional/parameterised, so blast radius is low.
- **F-08-03 (MINOR, SIMPLE FIX)** — Python baseline is stated inconsistently across the spine (3.12 in `L00-02`/`L01`, 3.13 in `L05-01`, 3.14/3.14.7 in `L15-03`/`L21`/`L23`/`L24`). Mostly environmental observation vs documentation; worth an explicit “supported floor vs observed host” note.
- **F-08-04 (MINOR, SIMPLE FIX)** — `L13-02` presents PostgreSQL as “Named Engine 2” inside the Core mechanism diagram/provenance without an in-Lesson “not required / docs-only” note; the canonical map classifies it Optional. Risk of reading as a hidden requirement.

---

## 9. Omissions / duplication / hidden-prerequisite review

- **Hidden prerequisites (Issue #9 resolutions):** toolchain → `L00-02` PASS; statistics → `L04-02` PASS; clock semantics → `L20-01`/`L23-01` PASS; environment preflight → covered for M03 (`labs/foundations/m03/preflight.sh`), M05–M09 (`scripts/preflight-m05-m09.sh`), M13–M15 (`tests/preflight_data_concurrency.py`), and LAB-REQ-02 PASS.
- **Duplicate canonical explanations:** none found beyond F-04-06/F-04-08.
- **F-09-01 (MAJOR, COMPLEX REWORK) — thin horizontal thread.** `meta/CURRICULUM_MAP.md:80` names **Privacy / Data Responsibility** as a horizontal thread, but it is essentially absent: only 5 occurrences of 隐私 and 4 of “privacy” across 4 Lessons (`L11-01`, `L12-03`, `L20-01`, `L24-01`) versus 116 occurrences of 一致性 (consistency) across 22 Lessons. There is no dedicated privacy treatment in the storage, database, distributed, or concurrency Modules, and no privacy evidence home analogous to the “security/privacy horizontal” claim. The other five horizontal threads recur adequately.
- **F-09-02 (MINOR, SIMPLE FIX)** — The 5 Optional Labs / 5 Source Expeditions are declared but only 3+3 have `book/` companions (`LAB-OPT-01/04`, `EXP-01/04` have none). Likely intentional for rights-gated link-only items, but not stated as such in the map.
- **Modern-worldview coverage vs the accepted reference set:** measured against `meta/audits/external-curriculum-audit-v0.1.md` R1–R15 and CS2023 knowledge areas, the authored spine covers representations, computation, machine, PL/runtime, OS, storage, networking, web/browser, databases, concurrency, distributed systems, infrastructure, security, judgment, and defense. R1 (applied MSF), R2 (toolchain), R6 (data evolution), R7 (experimental pattern), R9 (models/limits), R10 (consensus concept) all have explicit homes; R3/R4 are resolved by D-034/D-033; R11/R12/R14/R15 remain correctly bounded. The only coverage shortfalls are the privacy thread (F-09-01) and the Mini Cloud/lab integration gaps above — not missing macro areas.

---

## 10. Verification actually run by this auditor

Host: Windows (`win32`), Python 3.13.1, embedded SQLite 3.45.3, `curl` present, `gcc` present (MinGW), **`sqlite3` CLI absent**, **QEMU/RISC-V toolchain absent**. This host is **not** the canonical Linux image; these results complement, and never replace, canonical CI evidence.

| Surface | Command (from `AUDIT_BASE` worktree) | Result |
|---|---|---|
| LAB-REQ-05 | `python -m unittest discover -s labs/lab_req_05 -t labs/lab_req_05 -p "test_*.py"` | **7/7 PASS** (0.38 s) |
| LAB-REQ-04 | `… labs/lab_req_04 …` | **6/6 PASS** (0.09 s); CLI-absence path exercised |
| LAB-REQ-03 | `… labs/lab_req_03 …` | **8/8 PASS** (4.08 s, MinGW gcc) |
| LAB-REQ-01 | `… labs/lab_req_01 …` | **6/6 PASS** (7.34 s; real curl trace) |
| Mini Cloud | `python -m unittest discover -s project/tests -p "test_*.py"` | **66/66 PASS** (16.8 s) |
| LAB-REQ-02 | canonical QEMU smoke | **NOT RUN — ENVIRONMENT-BLOCKED** (no QEMU/RISC-V toolchain; requires `git clone` of pinned xv6) |
| Canonical CI lanes | provenance: `ci-fast` run 34679423472, `ci-mini-cloud` run 34679423473, `ci-qemu-lane` retained evidence | **PASS per committed record** (cited, not relabelled as this auditor's runtime) |

Worktree status after all runs: **clean** (no leftover artifacts).

---

## 11. Blockers and routing

Severity: **BLOCKER** (must be repaired/decided before v1.0 stable disposition) / **MAJOR** / **MINOR**.
Routing vocabulary: `SIMPLE FIX` / `COMPLEX REWORK` / `ARCHITECTURE` / `CURRENTNESS / SOURCE REFRESH` / `NO BLOCKER / FUTURE REVIEW`.

| ID | Finding | Severity | Route |
|---|---|---|---|
| **B-1** | Mini Cloud P0–P9 is implemented but **orphaned from the learner surface**; no `book/`/`course/`/`labs/` route; M24 defense uses a synthetic dossier, not the app (F-06-01/F-06-02) | **BLOCKER** | `COMPLEX REWORK` (bounded curriculum-integration design) |
| **B-2** | Required Labs **LAB-REQ-02 / 04 / 05** are not reachable from any Lesson; canonical Lessons route to different `labs/foundations/` fixtures (F-05 §5.2) | **BLOCKER** | `COMPLEX REWORK` (bounded; may reduce to linkage) |
| **B-3** | Learner material + preflight test assert **OQ-BP-001 OPEN/RFC-GATED**, contradicting **D-033** (and stale OQ refs in maps) (F-07-01) | **BLOCKER** | `SIMPLE FIX` (status reconciliation; must also fix the coupled test) |
| M-1 | `L17-03:16` mischaracterizes EC-CON-014 first home (ACID-C vs named visibility) (F-04-06) | MAJOR | `SIMPLE FIX` |
| M-2 | `L04-01`/`L04-02` missing objective/prerequisite/provenance; `L04-02` missing ignore-field (F-04-01) | MAJOR | `SIMPLE FIX` |
| M-3 | Privacy / Data Responsibility horizontal thread thin/effectively absent (F-09-01) | MAJOR | `COMPLEX REWORK` |
| M-4 | Currentness marking discipline uneven; M00–M18 largely unmarked (F-08-01) | MAJOR | `CURRENTNESS / SOURCE REFRESH` |
| M-5 | LAB-REQ-03 accepted predicate break (`if`-instead-of-`while` / removed wait) absent (F-05-01) | MAJOR | `SIMPLE FIX` |
| M-6 | `meta/PROJECT_STATUS.md` stale (predates #146–#160) (F-06-03) | MAJOR | `SIMPLE FIX` (status-only reconciliation) |
| m-1 | Unsound lesson hard-prereq `M04` in `L11-03`/extra in `L08-02` (F-04-04) | MINOR | `SIMPLE FIX` |
| m-2 | `L13-02:26` wrong concept ID (F-04-07) | MINOR | `SIMPLE FIX` |
| m-3 | `L13-01`/`L15-01` state no prerequisites (F-04-02) | MINOR | `SIMPLE FIX` |
| m-4 | LAB-REQ-01/04/05 missing accepted break artifacts (F-05-02/03/04) | MINOR | `SIMPLE FIX` |
| m-5 | Required-Lab READMEs omit DoD fields; REQ-03/05 omit preflight pointer (F-05-05) | MINOR | `SIMPLE FIX` |
| m-6 | REQ-03 rendezvous event-count mismatch between harness/template (F-05-06) | MINOR | `SIMPLE FIX` |
| m-7 | Lesson competency labels narrower than Matrix for REQ-01/02/05 (F-05-07) | MINOR | `SIMPLE FIX` |
| m-8 | Stale OQ refs in `CURRICULUM_MAP`/`CONCEPT_REGISTRY` (F-07-02) | MINOR | `SIMPLE FIX` |
| m-9 | D-034 bounded accessibility hook under-delivered in P2/P9/browser (F-07-03) | MINOR | `NO BLOCKER / FUTURE REVIEW` |
| m-10 | P1 HTTP unconditional; P4 index pre-baked; P2 username enumeration; P3 extra process; P0 early migration (F-06-04…08) | MINOR | `SIMPLE FIX` |
| m-11 | Python baseline stated inconsistently; `L13-02` PostgreSQL “Named Engine 2” ambiguity (F-08-03/04) | MINOR | `SIMPLE FIX` |
| m-12 | Optional-lab/expedition companions 3+3 not explained; verification doc template-split claim inaccurate (F-09-02/F-04-03) | MINOR | `SIMPLE FIX` |

**No ARCHITECTURE finding** is raised: no canonical concept ID, first-home assignment, DAG edge, Required/Optional lab selection, or accepted scope decision needs to change. B-1/B-2 are bounded integration/linkage work within the accepted architecture.

---

## 12. Limitations and NOT RUN items

- **Canonical environment execution (NOT RUN by this auditor):** the full 296-test matrix, all five shared preflights, M03 GDB three-point, M10/m20 canonical lanes, and the LAB-REQ-02 QEMU smoke were **not** re-run here. This audit host is non-canonical (Windows) and lacks the `sqlite3` CLI, QEMU, and the RISC-V toolchain. Canonical runtime is cited from committed CI/Actions provenance only.
- **LAB-REQ-02 QEMU smoke: NOT RUN — ENVIRONMENT-BLOCKED** on this host.
- **External re-fetch of every cited source (NOT RUN):** §8 spot-checked the highest-risk claims only; unwrapped external claims remain as repository record.
- **Learner validation:** NOT RUN and not satisfiable by AI (Issue #34 remains the human gate).
- **This audit does not establish:** stable `VERIFIED`, `RELEASED`, v1.0, learner validation, or the final stable multi-role verification (Issue #158). It also does not close OQ-BP-006 (independent pin re-verification, Issue #153).
- **Base movement:** the report is scoped to `AUDIT_BASE = 97096c9`; `main` moved to `cd7396c` afterward and was not audited. Web Lead decides whether a refresh is required.

---

## 13. Explicit non-claims

This audit does **not** claim, and must not be read as claiming:

- that any Lesson, Lab, test, fixture, environment, CI, Mini Cloud, policy, Decision, or lifecycle state was repaired, improved, or changed by this audit;
- that the project is `VERIFIED`, `RELEASED`, or v1.0-ready;
- that learner validation has occurred;
- that the final stable multi-role curriculum verification (Issue #158) is complete;
- that OQ-BP-006 has closed;
- that the earlier External Curriculum Coverage Audit v0.1 is superseded beyond this report's explicit findings;
- that runtime/bug/dependency assumptions relied upon for future software work are correct.

---

## 14. Final recommendation

**`FINAL EXTERNAL AUDIT FOUND BLOCKERS — REPAIR REQUIRED`**

Rationale: the authored Core is genuinely broad and largely sound — 25 Modules / 70 Lessons / 5 Required Labs are present, the DAG and all 18 concept first homes are internally consistent, the Required-Lab mechanism implementations are real (and independently executable here), the Mini Cloud P0–P9 implementation matches its accepted mapping with no forbidden components, D-033/D-034 scope is not expanded, and every spot-checked currentness claim is accurate. However, three BLOCKERS prevent a stable-gate PASS: the runnable Mini Cloud is orphaned from the learner-facing curriculum and the M24 defense exercise does not use it (B-1); three of five Required Labs are not reachable from any Lesson (B-2); and learner-facing material plus a preflight test still assert a governance status that D-033 has closed (B-3). These are bounded integration/consistency repairs, not architecture changes, so repair — not redesign — is the correct next step.

This recommendation concerns the audited object at `AUDIT_BASE` only. It does not establish learner validation, `VERIFIED`, `RELEASED`, or v1.0.
