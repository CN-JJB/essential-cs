# Project Status

Last updated: 2026-08-30

## Current phase

**Curriculum Blueprint v0.1 — COMPLETE / CLOSED**

**Post-Blueprint Build-First Core Production — ACTIVE**

Requirements / Grill Me is complete. GitHub remains the persistent source of truth. Issue #23 / PR #24 completed the independent Blueprint Final Exit Audit. The audit initially found two narrow production-facing consistency blockers; Web Lead direct fixes reconciled prerequisite metadata and competency labels without changing the accepted architecture. The narrow re-audit passed **30/30 Blueprint exit criteria**, and Blueprint v0.1 closed on 2026-08-30.

Blueprint closure means the project may now build and validate the curriculum through stage-by-stage vertical slices. It does **not** mean Lessons/Labs are VERIFIED or released, and it does not satisfy the later v1.0 gate.

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
- **Issue #19 / PR #20 — Lead-reviewed and merged:** Course Charter, Learner Profile, Learning Outcomes, Bridge / diagnostic.
- **Issue #21 / PR #22 — Lead-reviewed and merged:** Assessment Architecture + Modern Technology Case Map.
- **Issue #23 / PR #24 — Final Exit Audit merged 2026-08-30:** initial audit FAIL identified narrow prerequisite/competency inconsistencies; Web Lead direct-fixed them without changing 40H/22S architecture; narrow re-audit passed 30/30 criteria; Blueprint v0.1 closed.
- **Issue #25 / PR #26 — Foundations/System Mechanics Research Dossier v0.1:** Lead-reviewed and merged with `READY FOR DESIGN`.
- **Issue #27 / PR #28 — Foundations/System Mechanics Vertical-Slice Design v0.1:** Lead-reviewed and merged with `READY FOR LESSON / ACTIVITY IMPLEMENTATION`.
- **Issue #29 / PR #30 — M00–M01 Learner Lesson + Activity Pilot v0.1:** independently Lead-reviewed, narrow SIMPLE FIXes applied (L00-02 debugger-light outcome, progressive disclosure, Mermaid polish), and merged 2026-08-30. Merge does **not** mark the packet VERIFIED or learner-validated.
- **Issue #31 / PR #33 — M00–M01 Technical Verification + Learner-Pilot Readiness v0.1:** independently verified, Lead-reviewed, and merged. Debian 13 / Python 3.13.5 reproduced the activity contract; Ubuntu 24.04 Noble / Python 3.12 remains NOT RUN and OQ-BP-006 remains OPEN. A first-pilot observation template is now available; this is not learner validation.
- **Issue #38 / PR #39 — M02 Computation & Complexity learner packet v0.1:** Lead-reviewed, two SIMPLE FIXes applied for concept first-home discipline and canonical Invariant/Correctness wording, then merged. Three Lessons, coherent activity, tests, evidence template, progressive support, and required visuals are present.
- **Issue #41 / PR #42 — M03 Machine: ISA & Execution learner packet v0.1:** Lead-reviewed and merged after one evidence-wording SIMPLE FIX. Independent Lead reproduction passed native x86-64 build/baseline/disassembly/direct hosted failure; GDB three-point/debugger-failure runtime remains BLOCKED/NOT RUN because GDB is unavailable in both author and Lead environments. The packet preserves C / ISA / ABI / compiler-build / hosted-observation boundaries and keeps OQ-BP-006 OPEN.
- **Issue #44 / PR #45 — M04 Memory Hierarchy, Locality & Measurement learner packet v0.1:** Lead-reviewed and merged after SIMPLE FIXes aligning canonical Caching/Locality definitions, making elapsed-time subtraction explicit, and machine-checking counterbalanced trial order. Committed author-smoke statistics independently recomputed exactly; final-head Lead rerun on x86-64 Debian/GCC reproduced the predicted direction with 30 trials and a ~19.72× column/row median ratio. This remains environment-specific microbenchmark evidence, not a universal hardware claim.
- **Issue #47 / PR #48 — Runtime, OS & Persistence Research Dossier v0.1 (M05–M09):** Lead-reviewed and merged with **READY FOR DESIGN** after current-source/boundary fixes covering Fall 2025 xv6 `sleep`→`pause` routing, lab-page licensing uncertainty, ptrace/strace permissions, durability write-path checkpoints, CPython implementation boundaries, and SSD source classification. LAB-REQ-02 selection remains accepted; OQ-BP-006 remains OPEN.
- **Issue #50 / PR #51 — Runtime, OS & Persistence Design Dossier v0.1 (M05–M09):** Lead-reviewed and merged with **READY FOR LESSON / ACTIVITY IMPLEMENTATION** after SIMPLE DESIGN FIXes tightening write-path/durability claims, hosted ptrace/QEMU/root-permission assumptions, M07 bad-address/OOM evidence, Isolation vs Trust Boundary wording, and SSD/WAL inference boundaries. All 15 canonical Lesson IDs and first homes remain intact.
- **Issue #53 / PR #54 — M05 Languages, VM & Compiler Pipeline learner packet v0.1:** Lead-reviewed and merged after SIMPLE FIXes separating Python specification from CPython AST/bytecode implementation evidence, removing unsafe/fixed bytecode/performance claims, tightening type-system/GCC diagnostic boundaries, and gating bytecode inspection to CPython. Author Windows CPython 3.13.1/GCC 14.2 tests passed 9/9; Lead Debian CPython 3.13.5/GCC 14.2 independently reproduced the core 9/9 contract and compiler/bytecode relations.
- **Issue #56 / PR #57 — M06 Processes, Syscalls & LAB-REQ-02 learner packet v0.1:** Lead-reviewed and merged after SIMPLE FIXes adding real fork→exec→exit→wait evidence, removing synthetic strace evidence, bounding zombie/scheduler observations, hardening xv6 pin/setup/reset/QEMU smoke, and correcting Process/POSIX/Linux/xv6 claim boundaries. Author WSL reproduced xv6 build/QEMU execution at the accepted Fall 2025 pin; Lead Debian independently reproduced the final host M06 suite at 7/7 and rechecked the official pinned pause/sys_pause route. Official course-fork grader remains NOT RUN.
- **Issue #59 / PR #60 — M07 Virtual Memory & Isolation learner packet v0.1:** Lead-reviewed and merged after SIMPLE FIXes bounding Isolation/TLB wording, converting exact RSS/minor-fault/page-frame relations into hosted directional evidence, tightening Linux overcommit/OOM claims, removing stale kernel-internal implementation details, and preserving the C UB → hardware event → OS handling → hosted signal separation. Canonical first homes EC-CON-013 Isolation and EC-CON-017 Trust Boundary remain in L07-01; Process remains revisit-only.

## Active workstream

The project is in **post-Blueprint build-first Core production**. Research, Design, M00–M01 learner-facing implementation, and the independent technical verification/pilot-readiness gate are complete. Issue #34 remains OPEN as a truthful real-learner validation task, but under D-027 it is **DEFERRED / NON-BLOCKING** while the full course is authored.

Completed closure sequence:

- Issue #19 / PR #20 — Course Charter, Learner Profile, Learning Outcomes, Bridge / diagnostic;
- Issue #21 / PR #22 — Assessment Architecture + Modern Technology Case Map;
- Issue #23 / PR #24 — Final Exit Audit, Lead direct fixes, narrow re-audit, **PASS — BLUEPRINT v0.1 READY TO CLOSE**;
- Issue #25 / PR #26 — Foundations/System Mechanics Research Dossier v0.1, Lead-reviewed, narrow provenance fixes applied, merged with **READY FOR DESIGN**;
- Issue #27 / PR #28 — Foundations/System Mechanics Design v0.1, Lead-reviewed, M03 provenance/M04 benchmark-control fixes applied, merged with **READY FOR LESSON / ACTIVITY IMPLEMENTATION**;
- Issue #29 / PR #30 — M00–M01 learner Lesson + shared activity/evidence packet, independently Lead-reviewed, SIMPLE FIXes applied, merged with **PASS FOR MERGE** while explicitly remaining pre-VERIFIED / pre-learner-validation;
- Issue #31 / PR #33 — independent technical verification + learner-pilot readiness, Lead-reviewed and merged with **PASS FOR MERGE — READY TO ENTER REAL LEARNER VALIDATION / FIRST PILOT**.

Production now follows D-027's bounded build-first sequence:

`Research → Design → Lesson/Lab/Project Implementation → Independent Verification/Lead Review → Next Ready Batch`

Learner Validation is deferred during authoring but remains mandatory before v1.0 / `RELEASED`. The accepted Research + Design slice for **M00–M04 is now fully implemented through M04 after Lead review**. The **M05–M09 Research + Design slice is Lead-accepted; M05–M07 implementations are Lead-reviewed and merged, including LAB-REQ-02**. The next bounded production step is learner-facing **M08 — Files, Filesystems & System I/O**.

## Current priority

1. Implement the next bounded learner-facing **M08 — Files, Filesystems & System I/O** packet from the accepted M05–M09 Design; do not jump ahead to M09 in the same PR.
2. Keep independent Verification/Lead Review on every bounded implementation batch even though learner validation is deferred.
3. Keep **Issue #34 OPEN / DEFERRED / NON-BLOCKING** until real learning begins; never fabricate learner evidence.
4. Preserve OQ-BP-001 and OQ-BP-003 as RFC-gated/non-blocking and OQ-BP-006 as OPEN; Noble/Python 3.12 remains unverified.
5. Preserve the M03 GDB verification limitation as explicit technical debt; do not silently convert the blocked debugger path into PASS.
6. Preserve M04 microbenchmark evidence as environment-specific; do not turn the observed ratio into a curriculum constant.
7. Complete real learner validation and disposition material findings before v1.0 / `RELEASED`.

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
