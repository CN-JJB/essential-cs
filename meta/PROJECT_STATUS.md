# Project Status

Last updated: 2026-08-30

## Current phase

**Curriculum Blueprint v0.1 — ACTIVE**

Requirements / Grill Me is complete. GitHub is the persistent source of truth. The first parallel Blueprint research/design wave has completed Lead review and is merged; the project is now in **reconciliation/integration**.

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
- **Issue #9 reconciliation proposals reviewed (2026-08-30):**
  - PR #14 / Issue #11 — Mini Cloud App ↔ curriculum alignment: Lead-accepted and squash-merged.
  - PR #15 / Issue #13 — Competency + Concept Registry integration: Lead direct fixes applied, then squash-merged.
  - PR #16 / Issue #12 — Lab + Source Expedition selection: reworked, Lead-reviewed, and squash-merged.
    - Required concurrency is now a self-contained Essential CS POSIX/C11 Lab; OSTEP remains optional/link-only evidence.
    - Required Database coverage now includes real SQLite query/index and transaction/isolation/rollback/recovery Labs; PostgreSQL remains optional.
    - xv6 course-page licensing is scoped separately from the MIT-licensed xv6 software and linked/generated assets.
    - Lead corrected the Required concurrency design to avoid teaching a plain-C data race/undefined behavior as if it were only an interleaving; the broken path now uses defined C11 atomic load/store operations to demonstrate lost-update atomicity.
- Lead direct fixes during review:
  - corrected Stage narrative vs hard-dependency semantics in the dependency graph;
  - corrected `M14 → M16` from hard to soft while preserving `M14 → M17` as the consistency hard dependency;
  - corrected the stale 58→70 Lesson-count uncertainty;
  - pinned the concurrency lab candidate to OSTEP v1.10 Threads (Semaphores) Homework (Code);
  - normalized missing Completion Reports for PRs #7/#8.

- **PR #17 / Issue #10 — Audit → Architecture disposition matrix:** Lead-reviewed and squash-merged.
  - R1 applied measurement/statistics → bounded Core addition.
  - R6 schema evolution/provenance → bounded Core addition.
  - R2/R7/R8/R9/R10 → integrate existing Core.
  - R5/R13 → Current Case.
  - R11/R12/R14 → Deep Dive.
  - R15 → Reject from v0.1 Core.
  - R3 human-facing/accessibility boundary and R4 bounded AI literacy remain explicit architecture escalations for #9/RFC handling.

## Active workstream

- **#9 — [Blueprint] Reconcile Issues #1–#4 into Blueprint v0.1 maps**
  - audit findings → architecture outcomes;
  - Stage/Module/Lesson/dependency reconciliation;
  - Mini Cloud App ↔ curriculum mapping;
  - Blueprint Lab Map + Source Expedition Map;
  - Competency Matrix integration;
  - initial stable Concept Registry population;
  - explicit Open Question / RFC escalation for unresolved Core-scope choices.

Issue #9 is the primary integration workstream. Avoid parallel edits to the same canonical Blueprint maps until its reconciliation contract is settled.

## Current priority

1. Execute and Lead-review Issue #9.
2. Resolve architecture-level Open Questions through the required Open Question → research/RFC → Decision path where Core scope or philosophy changes.
3. Integrate accepted outcomes into the detailed Curriculum/Lesson Map, Dependency Graph, Mini Cloud App Evolution Map, Lab Map, Source Expedition Map, Competency Matrix, and Concept Registry.
4. Continue Blueprint v0.1 until its exit criteria are satisfied.
5. Do **not** begin large-scale lesson writing.

## Current architecture attention points

- bounded AI literacy: Core thread/module vs Current Case;
- just-in-time applied MSF/statistics and explicit toolchain/SDF outcomes;
- bounded HCI/accessibility/user-boundary reasoning;
- default learner narrative for partially independent S4 (Network/Web) and S5 (Data/Concurrency);
- final Adopt/Adapt lab selection with license/reproducibility review;
- canonical software/environment versions.

## Lifecycle

`IDEA → PLANNED → RESEARCHED → DRAFTED → VERIFIED → RELEASED → NEEDS_REVIEW`

## Source of truth

When chat context conflicts with a formal repository Decision/Status, use the latest explicit repository state unless a newer approved change is currently being persisted.
