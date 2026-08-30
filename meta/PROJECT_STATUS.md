# Project Status

Last updated: 2026-08-30

## Current phase

**Curriculum Blueprint v0.1 — ACTIVE**

Requirements / Grill Me is complete. GitHub is the persistent source of truth. The first parallel Blueprint research/design wave and the reconciliation inputs wave (Issues #10–#13) are merged; **Issue #9 integration has been executed and is under Lead review** (branch `blueprint/issue-9-final-reconciliation`, PR with `Closes #9`). Blueprint v0.1 is **not complete**: several exit criteria still lack artifacts.

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
- **Issue #9 integrated (2026-08-30) — under Lead review.** Canonical Blueprint state now includes:
  - `meta/blueprint/final-reconciliation-v0.1.md` — integration record + canonical P0–P9 Module mapping.
  - `meta/CURRICULUM_MAP.md` — reconciled stage/module/lab/project/registry overview.
  - `meta/blueprint/core-stage-module-lesson-map-v0.1.md` and `meta/blueprint/dependency-graph-v0.1.md` — reconciled for Issue #9 (no DAG edge changes; hidden prerequisites resolved; proposal-level OQ-1–OQ-9 closed).
  - `meta/COMPETENCY_MATRIX.md` — Introduce/Practice/Assess model; Stage exit evidence packets; Lab/Milestone mappings.
  - `meta/CONCEPT_REGISTRY.md` — 18-concept initial population (Big Ideas unchanged: 15).
  - `meta/OPEN_QUESTIONS.md` — 3 open (OQ-BP-001/003 Core-scope escalations; OQ-BP-006 versions), 3 closed with provenance (OQ-BP-002/004/005).
  - `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md` (OQ-BP-001) and `meta/rfcs/RFC-CAND-002-human-facing-boundary.md` (OQ-BP-003) — candidates only, no decision.
  - `meta/PROJECT_STATUS.md`, `meta/blueprint/WORKSTREAMS.md` — state updated.

## Active workstream

- **Lead review of the Issue #9 integration PR** (`Closes #9`).
  - verify the highest-risk integration decisions (M04 `L04-02` uncertainty-toolkit boundary, concept first-home changes, P0–P9 project-order vs DAG separation, LAB-REQ-03 defined-race design, Registry admission scope, exit-criteria gap list);
  - the Reviewer may directly fix small inconsistencies before merge (review policy, D-018/D-019).
- **After #9 merges** (or in parallel once unblocked), next Blueprint work:
  - remaining exit-criteria artifacts: **Course Charter, Learner Profile, Learning Outcomes, Bridge**, partial **Assessment Architecture** and **Modern Technology Case Map** (see `final-reconciliation-v0.1.md` §11);
  - eventually: Open Question → research → RFC/Decision for **OQ-BP-001** and **OQ-BP-003** (Core-scope; not decided by #9);
  - environment/version pinning (OQ-BP-006) at first module dossier + lab implementation.

## Current priority

1. Lead review and merge of Issue #9 (do not mark Blueprint v0.1 complete until its exit criteria are met).
2. Resolve architecture-level Open Questions through the required Open Question → research/RFC → Decision path (OQ-BP-001, OQ-BP-003).
3. Produce the missing exit-criteria Blueprint artifacts (charter, learner profile, outcomes, bridge, assessment architecture, technology case map).
4. Then begin stage-by-stage vertical slices (Research → Design → Lesson → Lab → Project → Verification → Learner Validation) from an early Foundations/System Mechanics slice — **no large-scale lesson writing before exit criteria**.

## Current architecture attention points

- bounded AI literacy (OQ-BP-001): Core thread/module vs Current Case — RFC candidate exists, undecided;
- bounded HCI/accessibility/user-boundary reasoning (OQ-BP-003) — RFC candidate exists, undecided; P2/P9 evidence hooks remain interim-safe;
- default S4/S5 learner narrative — decided (request-centric preference, not a hard dependency);
- just-in-time applied MSF/statistics (M04 `L04-02` first home) and explicit toolchain/SDF outcomes (M00 `L00-02` + lab-entry gate);
- canonical software/environment versions (OQ-BP-006) and latency-constant list — implementation-time;
- Lab implementation dossiers (setup validation, smoke tests, license/pinning audits) — post-Blueprint.

## Lifecycle

`IDEA → PLANNED → RESEARCHED → DRAFTED → VERIFIED → RELEASED → NEEDS_REVIEW`

## Source of truth

When chat context conflicts with a formal repository Decision/Status, use the latest explicit repository state unless a newer approved change is currently being persisted.
