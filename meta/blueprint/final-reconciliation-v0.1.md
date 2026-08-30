# Issue #9 Final Reconciliation — Blueprint v0.1

**Task:** Issue #9 — [Blueprint] Reconcile Issues #1–#4 into Blueprint v0.1 maps
**Role:** Curriculum Architecture Integrator
**Status:** `READY FOR LEAD REVIEW` — not `VERIFIED`, not canonical-process-complete
**Date:** 2026-08-30
**Base branch:** `origin/main` `eae3de6` (fetched before work; GitHub authoritative)

This record explains what entered the canonical Blueprint and what did not. It is the single place a new Web Lead reads to understand the reconciled Blueprint without reconstructing eight proposal PRs. It is not a transcript.

---

## 1. Inputs and provenance

| Input | Issue | PR / artifact | Merged state |
|---|---|---|---|
| Core Stage/Module/Lesson map + dependency graph | #1 | #5 (`core-stage-module-lesson-map-v0.1.md`, `dependency-graph-v0.1.md`) | Merged; Lead dependency-model fixes applied (S4/S5 partial independence; `M14→M16` soft; `M14→M17` hard; 70-lesson count) |
| External Curriculum Coverage Audit | #2 | #6 (`audits/external-curriculum-audit-v0.1.md`) | Merged as evidence |
| Mini Cloud App evolution map | #3 | #7 (`mini-cloud-app-evolution-v0.1.md`) | Merged (P0–P9 stable IDs; macro-area anchors) |
| Classic Lab + Source Expedition candidates | #4 | #8 (`lab-and-source-expedition-candidates-v0.1.md`) | Merged as candidate research |
| Mini Cloud App ↔ curriculum alignment | #11 | #14 (`mini-cloud-curriculum-alignment-v0.1.md`) | Merged; E-family evidence hooks accepted |
| Competency + Concept Registry integration | #13 | #15 (`competency-concept-integration-v0.1.md`) | Merged after Lead direct fixes |
| Lab + Source Expedition selection | #12 | #16 (`lab-source-selection-map-v0.1.md`) | Merged after Lead-accepted rework (5 Required / 5 Optional / 5 Expeditions; POSIX-thread Build correction) |
| Audit → architecture disposition | #10 | #17 (`audit-to-architecture-disposition-v0.1.md`) | Merged (R1–R15 dispositions; R3/R4 escalations) |

All eight input artifacts remain in the repository as history/provenance. They are **inputs**, and where they now conflict with canonical state, the canonical state (this record + the artifacts it lists as canonical) wins.

## 2. Canonical vs proposal-only

**Canonical (Blueprint v0.1) after this integration:**

- `meta/CURRICULUM_MAP.md` — stage/module/lab/project/registry overview (updated)
- `meta/blueprint/core-stage-module-lesson-map-v0.1.md` — Modules + 70 Lessons + first-home table (updated)
- `meta/blueprint/dependency-graph-v0.1.md` — H/S/R/P semantics, acyclic proof (updated)
- `meta/COMPETENCY_MATRIX.md` — competency growth + evidence model (updated)
- `meta/CONCEPT_REGISTRY.md` — initial 18-concept population (updated)
- `meta/OPEN_QUESTIONS.md` — 3 open, 3 closed with provenance (updated)
- `meta/blueprint/final-reconciliation-v0.1.md` — this record
- `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md`, `meta/rfcs/RFC-CAND-002-human-facing-boundary.md` — **candidates**, not decisions
- `meta/PROJECT_STATUS.md`, `meta/blueprint/WORKSTREAMS.md` — state (updated)

**Proposal-only (kept, but not decision authority on their own):**

- `audit-to-architecture-disposition-v0.1.md` — dispositions now transcribed into canonical maps; the matrix remains the rationale record.
- `competency-concept-integration-v0.1.md` — the accepted population source; canonical copy lives in the Registry/Matrix.
- `mini-cloud-curriculum-alignment-v0.1.md` — the accepted per-milestone design; canonical mapping below (§6) is the integration.
- `mini-cloud-app-evolution-v0.1.md` — the accepted P0–P9 evolution; canonical mapping adds the Module/Lesson alignment.
- `lab-and-source-expedition-candidates-v0.1.md`, `external-curriculum-audit-v0.1.md` — research evidence (audit stays authoritative for its own claims only).

**Not changed (protected):** Curriculum Invariants, Decisions, Review/AI/Lab/Source/Living-Curriculum/DoD/Tech-eval policies, licensing policy, `book/``course/``labs/``project/` (do not exist yet).

## 3. What was accepted, modified, or explicitly not integrated

| Source | Accepted as-is | Modified during integration | Remained proposal-only |
|---|---|---|---|
| #1 map | 7 Stages, 25 Modules, 70 Lessons, mechanism classes | Stage dependency chain corrected (narrative vs H); M00/M02/M04/M05/M13/M17/M20/M23 learning outcomes enriched; §8 table linked to Registry IDs; §10/§11 marked resolved; stale 58→70 fixed | nothing substantive |
| #1 dependency graph | 62 H/S edges (40 H / 22 S) | Header/status; §2 narrative decision note; §6 hidden-prereq resolutions; §7 U-table resolution column; §8 resolved; §9 re-verification note | nothing (no edge changed) |
| #2 audit | Coverage findings as evidence | N/A (authoritative as evidence only) | R3/R4 remain architectural; R2-R15 transcribed |
| #3 evolution | P0–P9, one-constraint-per-milestone | Canonical Module/Lesson mapping added (§6) | Simpler-alternative/When-NOT cases preserved per milestone |
| #4 candidates | Candidate inventory | Selection reduced by #16; no candidate left as a Required Lab without a license-clear or original route | full CS:APP lab suite, Nand2Tetris, Full-xv6, CS144 sequence (Deep Dive/optional) |
| #10 dispositions | R1–R15 outcomes as summarized in this record §4 | transcribed into map/thread/first-home wording | R3/R4 escalated (not decided) |
| #14 | Evidence hooks (P2/P9), Technology Admission (container optional, queue/cache/replica rejected as mandatory, native path canonical) | canonical §6 mapping | Project-only decisions remain project-scope |
| #15 | 18-concept population, competency table, evidence packet, guardrails | canonicalized; Registry file structure completed | other named-but-deferred concepts |
| #16 | 5/5/5 selection; LAB-REQ-03 defined-race design; SQLite baseline; PostgreSQL optional; OSTEP link-only; xv6 licensing scoped | referenced into Curriculum Map + R14 boundary wording | Lab code is not implemented |

## 4. Audit disposition integration (R1–R15)

| Rec. | Disposition | Where it landed |
|---|---|---|
| R1 Applied MSF | BOUNDED CORE ADDITION | Measurement-uncertainty toolkit first home M04 `L04-02`; M02 `L02-01` discrete/asymptotic; revisits M13/M16/M17/M19/M20/M23; no math Module, no gate; threads: Measurement & Performance + Estimate |
| R2 Toolchain | INTEGRATE EXISTING CORE | M00 `L00-02` explicit outcomes + REQUIRED-lab entry gate (course discipline, not DAG edge); env preflight at M03/M06/M13; no command encyclopedia |
| R3 Human-facing boundary | ARCHITECTURE ESCALATION | OQ-BP-003 open; RFC-CAND-002 created; P2/P9 evidence hooks remain (no Core HCI content) |
| R4 Bounded AI literacy | ARCHITECTURE ESCALATION | OQ-BP-001 open; RFC-CAND-001 created; safe interim = verification-of-AI-claims (Current Case) |
| R5 GenAI/agentic coding | CURRENT CASE | M00 `L00-02` + M23 `L23-02`; generated output = untrusted hypothesis; no AI Module; review cadence 6–12 months |
| R6 Data modeling/evolution/provenance | BOUNDED CORE ADDITION | M13 `L13-03` extended (schema evolution, reader/writer compatibility, migration/backfill, source-of-truth vs derived, lightweight provenance); application pattern, no new concept ID |
| R7 Experimental pattern | INTEGRATE EXISTING CORE | Enumerated once at M04 `L04-02` (first assessed), production revisit M20 `L20-01`, consolidation M23 `L23-01`; clock-semantics bridge resolved at M20/M23 |
| R8 Security/privacy horizontal | INTEGRATE EXISTING CORE | First intros M07 `L07-01` / M11 `L11-01` / M12 `L12-03` / M19 `L19-03`; per-milestone evidence P0–P9; synthesis M21/M22; judgment M23/M24; accessibility NOT resolved here (R3) |
| R9 Models/limits/language connection | INTEGRATE EXISTING CORE | M02 `L02-01..03` (intuitive tractability/expressibility/decidability intuition) + M05 `L05-01..03` (algorithm ↔ language/runtime connection); formal theory Deep Dive |
| R10 Consensus concept | INTEGRATE EXISTING CORE | M17 `L17-02` concept Core; no implementation required; EXP-05 case + LAB-REQ-05 local analogue; Registry ID deferred |
| R11 Full consensus impl. | DEEP DIVE | Optional post-S7 / EXP-05 extension; explicit stopping point; no required replicated service |
| R12 Physical/embedded/real-time | DEEP DIVE (pending evidence) | No dependency; trigger = learner-validation evidence; no stage/edge change |
| R13 Cloud/orchestration breadth | CURRENT CASE (stable mechanisms Core) | M19 stable mechanisms; product case replaceable via Technology Admission; container = optional P7 comparison; No Kubernetes/cloud-vendor training |
| R14 Full kernel/stack/compiler/DB builds | DEEP DIVE (small slices only) | Slices = accepted Required Labs (LAB-REQ-01/02/03/04/05); full builds optional/Deep Dive; Attack Lab rejected; xv6 page-vs-software license scoping kept |
| R15 Quantum/specialist inventories | REJECT from v0.1 Core | No concept ID, no project, no expedition; reopen only via RFC with demonstrated dependency |

## 5. Stage / dependency reconciliation

- **Stage names and order unchanged** (7 Stages S1–S7; macro area mapping unchanged). No Stage renaming was needed or authorized; clarity improvements were made by restating the narrative-vs-dependency distinction, not by renaming.
- **Hard structure (unchanged):** `S1 → S2 → S3`; `S4`/`S5` partially independent after S3; both feed S6; S6 → S7.
- **Default learner path (labeled, not encoded):** request-centric `S1→S2→S3→S4→S5→S6→S7` = pedagogical preference (OQ-BP-004 resolved); state-centric `S3→S5→S4` equally allowed.
- **Edge semantics preserved:** 62 Module-level H/S edges (40 H, 22 S), 0 changes; `H`=hard, `S`=soft, `R`=revisit, `P`=project-integration; the REQUIRED-lab entry gate is **not** an H edge.
- **Acyclic verification:** re-run by topological ordering after integration — no cycle (unchanged edges + intra-Module lesson gains + non-ordering R/P edges cannot create one). Detail in `dependency-graph-v0.1.md` §5.
- **Hidden prerequisites (all 4 DAG §6 flags):** resolved (toolchain → L00-02 + gate; statistics → M04 L04-02; clock semantics → M20/M23; env repetition → preflight).

## 6. Canonical Mini Cloud App ↔ curriculum mapping

Single-process, locally bounded, deliberately simple notes/bookmarks service. P IDs stable. Native Linux path canonical; SQLite baseline; one constraint per milestone. Full design detail: `mini-cloud-curriculum-alignment-v0.1.md` (accepted propos). Canonical mapping below. **Project order is not a curriculum DAG.**

### P0 — One process, one durable collection

- **Mechanism exposed:** transient vs durable state; representation/serialization; identifiers; file/DB boundary; commit-and-retrieve; parameterized SQL boundary.
- **Competency exercised:** Trace (input → representation → process memory → durable state → read); Explain (what baseline does/doesn't guarantee); Correctness (ownership + schema invariant); Estimate (size/growth).
- **Canonical dependency:** M00 `L00-01` (map, first intro of State/Abstraction/Interface); M01 `L01-01/04` (representation/serialization); M08–M09 `L08-01/02`, `L09-01` (files/durability) for truthful discussion; **M13** `L13-01` is a later canonical revisit — do not teach SQLite internals at P0.
- **First intro vs application:** application/orientation at P0; mechanism revisits at M01/M08/M09; canonical DB mechanism at M13.
- **Deliberately not added:** HTTP; auth; multiple processes; replication; migrations-as-framework; full-text search; encryption at rest; production backups; PostgreSQL; cache; queue; container; deployment automation.
- **When NOT to add SQLite:** if the checkpoint is only about Python data structures, serialization, or a classic file mechanism; do not add a DB merely because later milestones say "cloud".
- **Beyond-the-Project:** CLI config/state files; compiler output caches; notebook checkpoints; batch-job restart state.

### P1 — Process boundary and narrow interface

- **Mechanism exposed:** interface contract vs implementation; framing; status/error representation; validation location; transport vs service core; process boundary.
- **Competency:** Trace (across a boundary); Explain (interface promise/limits); Diagnose (malformed/partial/unsupported); Correctness (one response or bounded error).
- **Canonical dependency:** M00 `L00-01/02`; M06 `L06-01/02` (processes); M10 `L10-01/02` (sockets); M11 `L11-02` (HTTP) only if HTTP is used; M12 is NOT required for CLI/process boundary.
- **First intro vs revisit:** process/interface mechanism is canonical teaching at M06/M10/M11; project is integration.
- **Deliberately not added:** framework internals; HTTP/2–3 implementation; TLS cert ops; browser JS; service discovery; version proliferation; public deployment.
- **When NOT to add HTTP:** only to look like a web app; a CLI/pipe/Unix-socket exposes the interface concept more clearly.
- **Beyond-the-Project:** Unix pipelines; compiler CLIs; file formats; database clients; library APIs.

### P2 — Multiple users, explicit trust boundaries

- **Mechanism exposed:** identity; authn vs authz; effective user; trust boundary; least privilege; sessions/tokens as state; private vs shared visibility; revocation; denial behavior; untrusted client claims.
- **Competency:** Judge (boundary design); Correctness (authorization invariant); Explain (what the service trusts); Diagnose (cross-user bypass); Learn-New-Tech (read a security API).
- **Canonical dependency:** after P0 ownership; M01 `L01-01` (input boundaries); **M07 `L07-01` supplies the canonical trust-boundary concept**; M13 (DB-integrated authz) optional. M21 remains the hard prerequisite for the canonical M22 `L22-01/02` threat/crypto/authn/authz security sequence, but not for a bounded early fixed-user authorization fixture.
- **First intro vs revisit:** trust boundary is already canonical at M07; the early fixture applies/previews identity and authorization; M21/M22 later synthesize threat/crypto/authn/authz.
- **Deliberately not added:** OAuth providers; enterprise identity; password-reset email; WAFs; threat hunting; real identity; public exposure; token products for résumé value.
- **When NOT to add authentication:** before the ownership invariant is understood; never a real identity provider on a teaching app.
- **Beyond-the-Project:** file permissions; database roles; mobile capabilities; package signing; OS privilege boundaries.

### P3 — Real network path, bounded failure

- **Mechanism exposed:** socket; client/server; DNS as bounded local case; TCP byte stream; HTTP messages; timeout; disconnect; retry; idempotency; partial-failure ambiguity.
- **Competency:** Trace (app data through protocol layers); Diagnose (timeout ≠ non-commit); Judge (retry by operation semantics); Estimate (local overhead, no Internet inference).
- **Canonical dependency:** M06 (processes); M08 (I/O intuition); M10 `L10-01..03`; M11 if HTTP. M15 not required for a sequential exercise; M14 soft aid; M12 not required. Later revisit: M16 `L16-01/02` (same ambiguity at scale).
- **First intro vs revisit:** transport/timeout semantics canonical at M10/M11; distributed version at M16.
- **Deliberately not added:** public DNS; global routing; QUIC implementation; CDN; multi-region deployment; uncontrolled public performance claims.
- **When NOT to add retries:** without a specified mutation policy and a way to distinguish ambiguous outcomes; never benchmark uncontrolled public services or treat loopback as Internet.
- **Beyond-the-Project:** DB clients; remote build executors; package downloads; message consumers.

### P4 — Query shape, indexes, measurement

- **Mechanism exposed:** scan vs index; B-tree-like index; selectivity; query plan; page/IO cost; locality; warm/cold state; measurement noise; space/write cost.
- **Competency:** Observe (plan); Diagnose (cold/cache confounds); Estimate (page/IO); Judge (index vs query-shape vs schema for the workload); Correctness (result equivalence).
- **Canonical dependency:** M08 `L08-02` + M09 `L09-01/02` (storage model); M02 `L02-01/02`; M04 `L04-01/02` (locality+measurement); **M13** `L13-01` canonical. M10–M12 are NOT prerequisites.
- **First intro vs revisit:** canonical mechanism at M13/LAB-REQ-04; P4 is domain-relevant application + measurement integration; M23 `L23-01` revisits validity.
- **Deliberately not added:** distributed query planners; sharding; production SLOs; cache layers; generic dashboards.
- **When NOT to add an index:** without a measured query, stated workload, correctness comparison, and evidence the index changes the relevant cost. Improve query/schema first.
- **Beyond-the-Project:** compiler optimization; filesystem/build caches; algorithmic data structures — same space/time + invalidation trade-off.

### P5 — Concurrent requests, transactional correctness

- **Mechanism exposed:** interleaving; shared state; race; atomicity; transaction; isolation; lock; MVCC concept; deadlock; idempotency/conflict response; app-lock vs DB guarantee.
- **Competency:** Correctness (invariant); Diagnose (race/lost update); Judge (serialization cost); Explain (which guarantee from where).
- **Canonical dependency:** M06 (execution context); M13 (if DB state tested); **M14** `L14-01/02` (transactions/isolation — canonical); **M15** `L15-01/02` (threads/races — canonical, LAB-REQ-03). Soft: M03 `L03-01`, M12 `L12-04` (event loop comparison). No M10–M12 hard prerequisite — P3-before-P5 does not make network a hard prerequisite for data work.
- **First intro vs revisit:** mechanism first at M14/M15 via LAB-REQ-03/05; project = ownership-aware integration (controlled race harness only after the mechanism lab).
- **Deliberately not added:** distributed locks; global ordering; actor frameworks; serializable-by-default claims; sharded transactions; queue-based coordination.
- **When NOT to add threads:** merely to increase throughput; never claim correctness from a stress test without invariant + controlled schedule + mechanism explanation.
- **Beyond-the-Project:** file updates; GUI event handlers; inventory/booking/accounting; build graphs.

### P6 — Durable recovery, operational evidence

- **Mechanism exposed:** durability; crash recovery; WAL concept; schema version; migration; backup/restore; RPO/RTO; resource exhaustion; recovery evidence; local vs replicated state.
- **Competency:** Observe (recovery artifacts); Correctness (version + invariant after restore); Judge (backup vs replication); Estimate (recovery cost).
- **Canonical dependency:** M09 `L09-01` (durability first intro); M13 `L13-03` (schema evolution) + M14 `L14-01/03` (transaction/recovery) for DB migration correctness; LAB-REQ-05 supplies mechanism evidence; M19/M20 are later operational revisits; M23 for RPO/RTO judgment.
- **First intro vs revisit:** durability canonical M09; recovery canonical M14/LAB-REQ-05; project integration after mechanism.
- **Deliberately not added:** managed backups; multi-region DR; object-store semantics; compliance; HA databases; automatic migration orchestration.
- **When NOT to add a migration framework:** before schema evolution is an actual problem; a second copy, a backup, and a tested restore are three different claims.
- **Beyond-the-Project:** package-lock updates; VM snapshots; notebook checkpoints; build artifacts.

### P7 — Deployment boundary, reproducible environment

- **Mechanism exposed:** executable artifact; environment/dependency; process vs image; namespace; cgroup; filesystem/mount; port; config/state boundary; reproducibility vs security isolation; build provenance; resource limit.
- **Competency:** Explain (image vs process); Observe (process/mount/port comparison); Judge (virtualenv vs script vs VM vs container); Learn-New-Tech (deployment description from authoritative sources).
- **Canonical dependency:** native reproducibility M00 `L00-02`, M06, M08; container mechanism hard M06 `L06-01` + M07 `L07-01` + M08 `L08-01` + M16 `L16-01`; **M19** `L19-01/02` canonical (S6). M20 not required; no Kubernetes knowledge required. Container is an **optional** P7 comparison (Technology Admission).
- **First intro vs revisit:** native path first (M00/M06); container mechanism at M19 — the project must not pull the container checkpoint earlier than the DAG allows.
- **Deliberately not added:** Kubernetes; service mesh; orchestration; cloud IAM; autoscaling; registry operations; image supply-chain policy beyond bounded provenance.
- **When NOT to require Docker:** when it hides process/syscall teaching, requires unsupported host setup, or makes the canonical Linux path less reproducible; never split the app into services to justify containers.
- **Beyond-the-Project:** hermetic builds; package managers; VMs; CI runners; mobile sandboxes.

### P8 — Instrumentation before scaling

- **Mechanism exposed:** structured log; metric; duration; trace/span; correlation ID; cardinality; sampling; missing signal; causal evidence; overhead; retention; SLO/SLI concept; privacy-aware telemetry.
- **Competency:** Observe (hidden behavior); Diagnose (symptom vs cause, one correlated request); Judge (signal value vs overhead/storage/privacy); Correctness (redaction invariant).
- **Canonical dependency:** minimal signals M00/M04/M10 recurs; full cross-layer: hard M16 + M19 → **M20** `L20-01/02` (canonical, S6); M11 soft; M23 `L23-01` revisits measurement methodology; LAB-OPT-04/EXP-04 are the optional trace comparison.
- **First intro vs revisit:** local logs/timers first; canonical observability at M20; project integration after mechanism.
- **Deliberately not added:** vendor dashboards; full SRE platform; anomaly-detection AI; collector internals; long-term retention; telemetry without a diagnostic question.
- **When NOT to add a tracing backend:** before the learner can formulate a failure/performance question that simpler evidence cannot answer.
- **Beyond-the-Project:** compiler profiling; OS tracing; DB query plans; batch-job counters; build telemetry.

### P9 — System Defense candidate state

- **Mechanism exposed:** partial failure; consistency; queue/replica alternatives; trust boundaries; privacy; cost/resource economics; evidence; assumptions; scale thresholds; complexity moved elsewhere; **rejection as an engineering decision**.
- **Competency:** all eight, integrated and defended.
- **Canonical dependency:** M23 `L23-01..03` (judgment toolkit) + complete shared S1–S6 + security synthesis M21/M22; final defense at **M24** `L24-01/02`. Scenario cards may use smaller subsets (stated scope).
- **First intro vs revisit:** scenario-judgment practice can appear at M23; final defense only after the complete shared chain.
- **Deliberately not added:** mandatory queue/cache/replica/PostgreSQL cluster/reverse proxy/service mesh/cloud deployment/microservices; no feature-build contest.
- **When NOT to add components:** P9 passes with the smallest justified evolution — or with **no change** when evidence supports rejection; "more components" is not a passing argument.
- **Beyond-the-Project:** defend a build cache, local DB, data pipeline, compiler service, batch workflow, or messaging system under the same question set.

**Admission guardrails (accepted):** PostgreSQL = Optional comparison (LAB-OPT-03) after SQLite; cache = not canonical (bounded branch only); queue = scenario-only; container = optional P7 comparison; reverse proxy/TLS = bounded optional case; observability backends = optional (LAB-OPT-04); replicas/distributed components/deployment automation = not baseline; minimal structured logs + timers = admitted (evidence is a required competency, not a modern badge).

## 7. Lab / Source Expedition integration

Source: `lab-source-selection-map-v0.1.md` (accepted). Summary:

- **5 Required:** LAB-REQ-01 (M11 HTTP/intermediary trace, Adapt RFC 9110), LAB-REQ-02 (M06 xv6 `sleep` syscall route, Adapt MIT 6.1810 + MIT-licensed xv6; CC BY 3.0 US page scope separate), LAB-REQ-03 (M15 POSIX threads **Build** — defined C11 atomic lost-update, mutex repair, condition rendezvous, watchdog deadlock boundary; OSTEP remains link-only), LAB-REQ-04 (M13 SQLite query/index **Build**), LAB-REQ-05 (M14 SQLite transactions/isolation/rollback/interruption-recovery/backup **Build**; PostgreSQL remains Optional comparison LAB-OPT-03).
- **5 Optional:** LAB-OPT-01 Data Lab (rights-gated), LAB-OPT-02 CS144 receiver (rights-gated), LAB-OPT-03 PostgreSQL (Adapt, after SQLite), LAB-OPT-04 OpenTelemetry (Adapt, license-cleared in principle), LAB-OPT-05 OSTEP rendezvous (Adopt link-only).
- **5 Source Expeditions:** EXP-01 xv6 (M06), EXP-02 PostgreSQL planner (M13), EXP-03 Chromium site isolation (M12), EXP-04 OpenTelemetry span (M20), EXP-05 MIT 6.033 replication/transactions/logging (M17, revisits M23/M24).
- **Counts with no overlap:** each ID unique; Required/Optional/Expedition sets disjoint.
- **No Lab code was implemented** in this task; smoke tests, pins, and learner instructions belong to later Lab dossiers.
- **License gates preserved:** no unresolved-license assignment is a learner-facing Required dependency; bundling anything requires the stated release-time legal check.

## 8. Competency integration

- Matrix grew from scaffold to I/P/A model: Stage × 8 competencies with sparse cells (no "every module teaches everything").
- Stage exits = evidence packets (predict/specify → observe/break → mechanism explanation → invariant/uncertainty → judge/estimate → transfer), not recall quizzes.
- Required Labs map to competencies and to the packet; all five Lab IDs carry their assessed competency set.
- P0–P9 map to competencies with bounded boundaries; P9 assesses all eight via the integrated defense.
- First-assessed homes added by dispositions: M04 `L04-02` (Estimate/Diagnose: uncertainty + experimental pattern), M13 `L13-03` (Correctness/Judge: schema evolution), M00 `L00-02` (Observe/Learn-New-Tech: toolchain evidence), M20 `L20-01` (Diagnose clock semantics).
- No competency renamed, added, or removed; #15's capability spine retained.

## 9. Concept Registry integration

- **Accepted:** 18 concepts EC-CON-001–018 — the 15 Big Ideas as concepts plus Process (EC-CON-018), Durability (EC-CON-016), Trust Boundary (EC-CON-017).
- **Big Ideas unchanged:** 15; Process/Durability/Trust Boundary are concepts, not Big Ideas (explicitly recorded in the Registry).
- **Deferred (with reasons recorded):** Consensus (concept Core at M17 per R10, ID deferred per #15 §8.5); schema-evolution/provenance (application pattern over existing Representation/State/Interface/Invariant; R6); Queue/Replication/Transaction/RPC/Container/Observability IDs; AI/model/evaluation concepts (OQ-BP-001); HCI/accessibility/consent concepts (OQ-BP-003); applied statistics/uncertainty concepts (toolkit under Estimate, R1).
- **First-home changes applied:** Invariant/Correctness/Specification → M02 `L02-03` (M01 application-only); Failure → M03 `L03-03` (M00 preview); Isolation → M07 `L07-01`; **Trust Boundary → M07 `L07-01` as the first concrete protection/trust boundary, explicitly distinguished from isolation; M21 is synthesis**; Concurrency → M15 `L15-01`; Consistency → M14 `L14-02`; Caching → M04 `L04-01`; Locality → M04 `L04-02`; Durability → M09 `L09-01`; Process → M06 `L06-01`.
- **Hygiene:** zero product names/commands/frameworks/vendors as IDs; no new ID in any RFC-gated area.

## 10. Architecture escalations (explicit, unresolved)

1. **OQ-BP-001 — bounded AI literacy** (R4). Options: (A) Core thread; (B) bounded M23 module; (C) Current Case only; (D) A + C. Wait: Core-scope; RFC required. Candidate: `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md` — **no option chosen here**. Interim-safe: AI-output verification pattern (Current Case).
2. **OQ-BP-003 — human-facing/accessibility boundary** (R3). Options: (A) M00-anchored spiral; (B) bounded M12 module; (C) project/rubric only (current); (D) Current Case. Core-scope; RFC required. Candidate: `meta/rfcs/RFC-CAND-002-human-facing-boundary.md` — **no option chosen here**. Interim-safe: P2/P9 evidence hooks.
3. **No new architecture question surfaced** that requires blocking: hidden-prereq resolutions, U-table, and lab sizing were all decided within the accepted disposition set. OQ-BP-006 (versions) is an implementation-time pin, not architecture.

## 11. Blueprint v0.1 remaining gaps (exit criteria in `meta/blueprint/README.md`)

| Exit criterion | Status after #9 |
|---|---|
| Course Charter | **GAP** — no standalone artifact (README/DECISIONS carry partial content; charter document needed) |
| Curriculum Invariants | Done |
| Learner Profile | **GAP** — only D-002 (a paragraph); standalone profile document needed |
| Learning Outcomes | **GAP** — stage/lesson outcome lines exist in the map, but no consolidated Learning Outcomes artifact |
| Big Ideas | Done (15; Registry) |
| Core Stage / Module Map | Done (map §4 + CURRICULUM_MAP) |
| Lesson Map | Done at Blueprint granularity (70 preliminary entries) |
| Dependency Graph | Done (reconciled; acyclic) |
| Competency Matrix | Done (I/P/A model) |
| Mini Cloud App Evolution Map | Done (evolution + alignment + §6 canonical mapping) |
| Lab Map | Done at selection level (5/5/5); implementation dossiers are post-Blueprint |
| Source Expedition Map | Done (5 routes with stopping points) |
| Modern Technology Case Map | **GAP — partial.** Technology Evaluation Framework policy (D-015) + M23 home + project admission table exist; a case-level map entry (which stable technology gets a Technology Card, when, what evidence) is scheduled for the M23 dossier |
| Assessment Architecture | **GAP — partial.** Evidence-packet model in COMPETENCY_MATRIX (S-stage exits + defense); standalone assessment-architecture artifact would consolidate rubrics/sample prompts (post-verification design work) |
| Bridge | **GAP** — bridge material for the entry assumptions (D-002) is not yet designed; the L00-02 toolchain outcome is the first chunk of that bridge |
| Deep Dive / Extension boundaries | Done (map §9 + disposition R11/R12/R14) |
| Repo Architecture / policies / DoD / Review / Protocols | Done |
| Concept Registry policy + initial structure | Done (schema + 18 entries + explicit deferrals) |
| Living Curriculum / Maintenance | Done |
| v1.0 Release Criteria | Done as policy (D-024; RELEASE_AND_MAINTENANCE_POLICY) — compliance is verified by v1.0 gate, not Blueprint |
| External Curriculum Audit v0.1 | Done (with dispositions integrated) |
| Explicitly tracked Open Questions | Done (3 open with escalation paths; 3 resolved with provenance) |

**Bottom line:** Blueprint v0.1 is **not complete**. The remaining gaps are: Course Charter, Learner Profile, Learning Outcomes, Bridge, and partial Assessment Architecture + Modern Technology Case Map. These are design artifacts, not lesson prose, and are natural next issues after Lead approval of #9.

## 12. Verification performed

- `git diff --check` (for this branch) — passed.
- Cycles: re-run topological check; 62 edges unchanged; no cycle (see dependency graph §5).
- IDs: 25 Modules unique (M00–M24); 70 Lesson IDs unique per `Lxx-yy` prefix; 5/5/5 Lab/Expedition IDs unique and disjoint; 18 concept IDs unique.
- Cross-references: CURRICULUM_MAP ↔ module map ↔ dependency graph ↔ Lab map ↔ Registry ↔ Matrix checked for stale references (e.g., "58 lessons" fixed; #16 not marked CHANGES REQUIRED; #10 not marked open; mandatory-PostgreSQL/OStep-Required wording absent from canonical text).
- Counts: 40 H / 22 S edges verified against the file; module-per-stage counts verified; lesson per module verified (S1:9 S2:8 S3:12 S4:10 S5:9 S6:12 S7:10 = 70).
- No technical claim invented from model memory: all claims trace to the accepted artifacts (their registers list live checks of 2026-08-30); no new primary-source fetch was needed for this integration task.

## 13. Completion report

**Status:** `READY FOR LEAD REVIEW` (not VERIFIED; PR open awaiting review).

**Files changed:** see the PR body — 4 rewrites (CURRICULUM_MAP, COMPETENCY_MATRIX, CONCEPT_REGISTRY, OPEN_QUESTIONS), 2 updated proposal-state maps (core-stage-module-lesson-map, dependency-graph), 2 state files (PROJECT_STATUS, WORKSTREAMS), 1 new reconciliation record, 2 new RFC candidates. No protected policy, invariant, decision, licensing, or lab-selection content was altered; no lab code; no lesson prose.

**Assumptions:** (1) merged #5–#8/#14–#17 represent the accepted input set as of `origin/main` `eae3de6`; (2) the corrected DAG semantics recorded in PROJECT_STATUS (S4/S5 partial independence; M14→M16 soft, M14→M17 hard) are the authoritative Lead fixes — preserved; (3) Issue #9 does not itself make a Core-scope decision beyond what the accepted disposition matrix permitted; (4) "canonical" here means canonical-in-Blueprint (under Lead review), not VERIFIED-and-released; (5) Chinese canonical names in the Registry follow D-005 and the #15 proposal text (Lead may refine terminology at dossier time).

**Open questions:** OQ-BP-001, OQ-BP-003 (architecture escalations, RFC candidates created); OQ-BP-006 (implementation-time environment/baseline pin). The former Proposal OQ-9 latency-constant question is **subsumed by OQ-BP-006 + module-dossier/Living Curriculum baselining**, not maintained as a separate durable Open Question.

**Prompt deviations:** none material. The allow-list's "update cross-reference metadata in accepted Blueprint artifacts only when mechanically stale" was interpreted narrowly — no acceptance-level substance was changed in `mini-cloud-app-evolution-v0.1.md`, `mini-cloud-curriculum-alignment-v0.1.md`, or `lab-source-selection-map-v0.1.md`.

**Out-of-scope necessary fixes:** the two proposal-map files corrected their own stale states (Stage-dependency-line contradiction with the Lead-fixed graph; 58→70 lesson-count in OQ-2; proposal-status headers updated to RECONCILED). These are in-task file states, not new scope.

**Recommended Web Lead review focus (highest integration risk):**
1. M04 `L04-02` enrichment — confirm it stays a measured-variation toolkit (R1) and does not drift into a statistics course; confirm the experimental pattern wording equals the #16 measurement rule.
2. Concept first-home changes (Invariant/Correctness/Failure/Isolation/Concurrency/Consistency) — check none breaks the DAG direction or creates a second canonical explanation.
3. P0–P9 canonical table — verify project order never reads as a curriculum DAG and P7 container stays optional per M19's DAG.
4. LAB-REQ-03 boundary — verify the defined C11-atomic broken path (not undefined data race) survived integration; it is the highest technical-risk teaching decision.
5. Registry admission — confirm Process/Durability/Trust Boundary remain concepts (not Big Ideas) and Consensus stays deferred with the R10 concept note.
6. Exit-criteria gaps (§11) — confirm the gap list and that PROJECT_STATUS still says ACTIVE (Blueprint not complete).
