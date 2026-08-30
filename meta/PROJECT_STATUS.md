# Project Status

Last updated: 2026-08-30

## Current phase

**Curriculum Blueprint v0.1 — ACTIVE**

Requirements / Grill Me is complete. GitHub is the persistent source of truth. The first parallel Blueprint research/design wave, reconciliation inputs (#10–#13), and **Issue #9 final canonical reconciliation have all passed Web Lead review and are merged**. Blueprint v0.1 is **not complete**: several exit criteria still lack artifacts.

## Completed

- Project vision, learner profile, curriculum philosophy, macro Core spine, Core/Deep Dive principles, Mini Cloud App strategy, research/lab/review/maintenance rules, and multi-agent governance agreed.
- Root repository instructions and governance scaffold created.
- Curriculum Invariants, Decisions, Open Questions, Curriculum Map, Competency Matrix, Concept Registry, Blueprint v0.1 charter, and work-session/prompt protocols seeded.
- Research/Source, Lab, Review, Living Curriculum, Technology Evaluation, Release/Maintenance, Definition of Done, Visual/Writing, and AI Collaboration policies persisted.
- PR/Issue templates, attribution/licensing intent, repository architecture, Local Agent task/rework templates, and first Web Lead handoff created.
- **Issues #1–#4 completed and Lead-reviewed.**
  - PR #5: Core Stage/Module/Lesson proposal + dependency graph.
  - PR #6: External Curriculum Coverage Audit v0.1.
  - PR #7: Mini Cloud App evolution map.
  - PR #8: Classic Lab + Source Expedition candidate research.
- **Issues #10–#13 completed and Lead-reviewed.**
  - PR #14: Mini Cloud App ↔ curriculum alignment (Lead-accepted).
  - PR #15: Competency + Concept Registry integration (Lead direct fixes, then merged).
  - PR #16: Lab + Source Expedition selection (reworked after Lead review: 5 Required / 5 Optional / 5 Source Expeditions; Required concurrency is a self-contained Essential CS POSIX/C11 Lab; SQLite Required DB Labs; OSTEP optional/link-only; PostgreSQL optional comparison; xv6 licensing scoped separately; LAB-REQ-03 broken path uses defined C11 atomic operations, not undefined-behavior data races).
  - PR #17: Audit → Architecture disposition matrix (R1–R15 outcomes; R3/R4 escalated).
- **Issue #9 final reconciliation (PR #18) — Lead-reviewed and merged 2026-08-30.** Canonical Blueprint state now includes:
  - `meta/blueprint/final-reconciliation-v0.1.md` — integration record + canonical P0–P9 Module mapping.
  - `meta/CURRICULUM_MAP.md` — reconciled stage/module/lab/project/registry overview.
  - `meta/blueprint/core-stage-module-lesson-map-v0.1.md` and `meta/blueprint/dependency-graph-v0.1.md` — reconciled for Issue #9 (no DAG edge changes; hidden prerequisites resolved; proposal-level OQ-1–OQ-9 closed).
  - `meta/COMPETENCY_MATRIX.md` — Introduce/Practice/Assess model; Stage exit evidence packets; Lab/Milestone mappings.
  - `meta/CONCEPT_REGISTRY.md` — 18-concept initial population (Big Ideas unchanged: 15).
  - `meta/OPEN_QUESTIONS.md` — 3 open (OQ-BP-001/003 Core-scope escalations; OQ-BP-006 versions), 3 closed with provenance (OQ-BP-002/004/005).
  - `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md` (OQ-BP-001) and `meta/rfcs/RFC-CAND-002-human-facing-boundary.md` (OQ-BP-003) — candidates only, no decision.
  - `meta/PROJECT_STATUS.md`, `meta/blueprint/WORKSTREAMS.md` — state updated.

## Active workstream

The first half of the **exit-criteria completion wave** is complete.

Lead-reviewed and merged in Issue #19 / PR #20:

- Course Charter;
- Learner Profile;
- consolidated Learning Outcomes;
- Bridge / diagnostic design.

The remaining Blueprint exit-criteria design work is now:

- Assessment Architecture consolidation;
- Modern Technology Case Map.

Architecture questions **OQ-BP-001** (bounded AI literacy) and **OQ-BP-003** (human-facing/accessibility boundary) remain RFC-gated and are not silently decided by #9. OQ-BP-006 owns implementation-time environment/version/baseline pinning.

## Current priority

1. Produce the remaining exit-criteria Blueprint artifacts: Assessment Architecture and Modern Technology Case Map.
2. Resolve OQ-BP-001 and OQ-BP-003 through Open Question → research → RFC/Decision when needed; they do not block unrelated exit-criteria work.
3. Re-audit Blueprint v0.1 against `meta/blueprint/README.md` and close remaining gaps.
4. Then begin stage-by-stage vertical slices (Research → Design → Lesson → Lab → Project → Verification → Learner Validation) from an early Foundations/System Mechanics slice — **no large-scale lesson writing before exit criteria**.

## Current architecture attention points

- bounded AI literacy (OQ-BP-001): Core thread/module vs Current Case — RFC candidate exists, undecided;
- bounded HCI/accessibility/user-boundary reasoning (OQ-BP-003) — RFC candidate exists, undecided; P2/P9 evidence hooks remain interim-safe;
- default S4/S5 learner narrative — decided (request-centric preference, not a hard dependency);
- just-in-time applied MSF/statistics (M04 `L04-02` first home) and explicit toolchain/SDF outcomes (M00 `L00-02` + lab-entry gate);
- canonical software/environment versions and hardware-dependent latency/cost baselines (OQ-BP-006) — implementation-time;
- Lab implementation dossiers (setup validation, smoke tests, license/pinning audits) — post-Blueprint.

## Lifecycle

`IDEA → PLANNED → RESEARCHED → DRAFTED → VERIFIED → RELEASED → NEEDS_REVIEW`

## Source of truth

When chat context conflicts with a formal repository Decision/Status, use the latest explicit repository state unless a newer approved change is currently being persisted.
