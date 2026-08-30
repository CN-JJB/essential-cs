# Web Lead Handoff — Blueprint Final Exit Audit

Date: 2026-08-30
Project: `CN-JJB/essential-cs`
Role: Web Lead / Curriculum Architect / Lead Reviewer
Current main checked: `2427611fb046f26d4bdf9cedbcb790acfd195f46`

## Current phase

**Curriculum Blueprint v0.1 — ACTIVE / Final Exit Audit**

Requirements / Grill Me is complete. Do not resume broad requirement questioning. GitHub is the durable source of truth; this handoff is only a navigation aid.

## Current live GitHub state at handoff

- Open Issues: **#23 only**
  - `#23 [Blueprint] Final Exit Audit v0.1`
- Open PRs: **none**
- Issue #23 has already been created and a full Local Agent prompt has been given to the user.
- The next expected event is: the Local Agent opens a PR for Issue #23 containing exactly:
  - `meta/blueprint/final-exit-audit-v0.1.md`

## Major completed work

Lead-reviewed and merged:

- #1–#4 / PRs #5–#8 — initial Blueprint research/design wave.
- #10–#13 / PRs #14–#17 — reconciliation inputs.
- #9 / PR #18 — final canonical Blueprint reconciliation.
- #19 / PR #20 — Course Charter, Learner Profile, Learning Outcomes, Bridge/Diagnostic.
- #21 / PR #22 — Assessment Architecture + Modern Technology Case Map.

## Current canonical Blueprint shape

- 7 learner-visible Stages.
- 25 Modules.
- 70 preliminary Lessons.
- Module DAG: 62 H/S edges = 40 Hard + 22 Soft; last Lead check was acyclic.
- 8 competencies:
  - Trace
  - Explain
  - Observe
  - Diagnose
  - Correctness
  - Judge
  - Estimate
  - Learn-New-Tech
- 15 Big Ideas.
- 18 initial Concept Registry entries.
- 5 Required Labs.
- 5 Optional Labs.
- 5 Source Expeditions.
- Mini Cloud App P0–P9.
- 52 technology cases/families in the Modern Technology Case Map after PR #22:
  - 21 STABLE CORE MECHANISM
  - 28 CURRENT CASE
  - 1 DEEP DIVE
  - 2 current non-admissions / REJECT-NOT-CORE pending RFC
  - Time classes: 23 STABLE / 28 CURRENT / 1 FRONTIER.

## Important Lead corrections already merged

Do not regress these:

1. **Trust Boundary**
   - canonical first home = M07 `L07-01`;
   - explicitly distinguish trust boundary from isolation boundary;
   - M21 = security/threat-model/crypto synthesis, not first definition.

2. **Distributed systems**
   - consensus concept is Core;
   - no required 3-node implementation;
   - no required Raft/Paxos implementation;
   - `EXP-05` is bounded distributed-systems Source Expedition;
   - full consensus implementation = Deep Dive.

3. **Messaging / infrastructure**
   - Kafka / RabbitMQ / Redis Streams / cloud queues are replaceable cases, not Core prerequisites.
   - Redis/Kubernetes/commercial cloud are not mandatory.
   - container/cache/queue/replica/proxy are conditional project additions only.

4. **Concurrency Required Lab**
   - `LAB-REQ-03` must not rely on plain-C data-race undefined behavior;
   - the broken path uses defined C11 atomic load/store operations to demonstrate lost-update/compound-atomicity failure, then synchronization repair.

5. **Database**
   - Required Core includes real SQLite mechanism Labs:
     - `LAB-REQ-04` query/index/workload;
     - `LAB-REQ-05` transaction/isolation/rollback/recovery.
   - PostgreSQL remains Optional comparison.

6. **Bridge**
   - skippable;
   - learner with required practical skills need not even run the diagnostic;
   - outside Core DAG;
   - no H edge;
   - M00 `L00-02` remains canonical first Core home of technical-investigation workflow.

7. **Assessment**
   - evidence-based and qualitative;
   - no numeric grading bureaucracy;
   - no mandatory new administrative artifact per Module;
   - Explain / Predict / Break / Judge;
   - Recall / Connect / Transfer;
   - Stage checkpoints + M24/P9 System Defense;
   - author cannot self-mark VERIFIED.

8. **Technology Map**
   - stable principle ≠ product;
   - HTTP/2 wording explicitly preserves TCP-level HOL;
   - browser multi-process/site-isolation architecture is stable mechanism; Chromium/Firefox are replaceable implementation cases;
   - OQ-BP-001/003 rows mean current non-admission pending RFC/Decision, not permanent rejection.

## Open Questions

### OQ-BP-001 — bounded AI literacy
OPEN, Core-scope escalation.

Safe interim state:
- AI-generated code/doc/claim/config = untrusted hypothesis requiring source/test/measurement/security verification.
- No AI/ML/LLM Core module.
- RFC candidate exists.
- Do not silently decide this while reviewing #23.

### OQ-BP-003 — human-facing/accessibility boundary
OPEN, Core-scope escalation.

Safe interim state:
- P2/P9 evidence hooks may exist;
- no settled HCI/accessibility Core track.
- RFC candidate exists.
- Do not silently decide this while reviewing #23.

### OQ-BP-006 — canonical environment/version/baseline pin
OPEN, intentionally implementation-time unless Final Exit Audit finds a real reason it blocks production.

Exact Python/Linux/dev-container/toolchain/browser/optional-component versions and hardware-dependent baselines belong to first Module Dossier / Lab implementation.

## Issue #23 contract

The Local Agent must act as an **independent Blueprint Exit Auditor**, not a designer.

Expected branch:
`blueprint/issue-23-final-exit-audit`

Expected single content file:
`meta/blueprint/final-exit-audit-v0.1.md`

Every exit criterion in `meta/blueprint/README.md` must appear exactly once with one of:

- COMPLETE
- PARTIAL — BLOCKING
- INTENTIONALLY DEFERRED — NON-BLOCKING
- NOT APPLICABLE

Final recommendation must be exactly one of:

- `PASS — BLUEPRINT v0.1 READY TO CLOSE`
- `FAIL — BLUEPRINT v0.1 REMAINS ACTIVE`

The Agent must not edit canonical architecture/status/policies.

## What the next Web Lead should do first

1. Inspect live GitHub state; repository state outranks this handoff.
2. Read:
   - `AGENTS.md`
   - `meta/PROJECT_STATUS.md`
   - `meta/CURRICULUM_INVARIANTS.md`
   - `meta/DECISIONS.md`
   - `meta/OPEN_QUESTIONS.md`
   - `meta/blueprint/README.md`
   - `meta/blueprint/WORKSTREAMS.md`
   - `meta/blueprint/final-reconciliation-v0.1.md`
   - `meta/blueprint/course-charter-v0.1.md`
   - `meta/blueprint/learner-profile-v0.1.md`
   - `meta/blueprint/learning-outcomes-v0.1.md`
   - `meta/blueprint/bridge-and-diagnostic-v0.1.md`
   - `meta/blueprint/assessment-architecture-v0.1.md`
   - `meta/blueprint/modern-technology-case-map-v0.1.md`
   - `meta/CURRICULUM_MAP.md`
   - `meta/COMPETENCY_MATRIX.md`
   - `meta/CONCEPT_REGISTRY.md`
   - `meta/blueprint/core-stage-module-lesson-map-v0.1.md`
   - `meta/blueprint/dependency-graph-v0.1.md`
   - `meta/blueprint/lab-source-selection-map-v0.1.md`
   - Issue #23 and any PR it creates.
3. If the Issue #23 PR exists, review the audit rather than redoing the audit from scratch.
4. Independently spot-check the auditor's structural claims (DAG/counts/open-question treatment).
5. If PASS and Lead agrees:
   - direct-fix small inconsistencies if needed;
   - merge;
   - update Project Status / Workstreams;
   - mark Blueprint v0.1 complete/closed only after confirming the exit criteria;
   - create the first post-Blueprint vertical-slice task.
6. If FAIL:
   - accept only genuine blockers;
   - route small fixes directly;
   - create the smallest possible blocking repair task for larger issues;
   - re-audit only the affected exit criteria.

## First post-Blueprint direction if PASS

Do not start mass lesson writing.

Begin an early Foundations / System Mechanics vertical slice:

`Research → Design → Lesson → Lab → Project → Verification → Learner Validation`

The previously accepted first-pilot direction is roughly:
- Information / Representation
- Computation
- Machine
- first Mini Cloud App connection

Prefer a Research Dossier / vertical-slice architecture task before full Lesson writing.

## Session rule

The user decides when browser context is too long. Do not proactively force another session switch.

When the user asks for another handoff:
- persist current durable state first;
- then provide a fresh Web Lead bootstrap prompt.
