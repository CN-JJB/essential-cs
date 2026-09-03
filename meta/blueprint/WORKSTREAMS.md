# Blueprint v0.1 Workstreams

## First parallel wave — COMPLETE

| Issue | Workstream | Result |
|---|---|---|
| #1 | Detailed Core stages, Module/Lesson map, dependency graph | Completed; PR #5 merged after Lead dependency-model fixes |
| #2 | External Curriculum Coverage Audit v0.1 | Completed; PR #6 merged as independent audit evidence |
| #3 | Mini Cloud App evolution map | Completed; PR #7 merged |
| #4 | Classic lab and Source Expedition candidate research | Completed; PR #8 merged after exact concurrency-source fix |

The four artifacts are **inputs** to reconciliation; the reconciled state is canonical, not each proposal alone.

## Integration wave — COMPLETE

| Issue | Workstream | Result |
|---|---|---|
| #10 | Audit recommendations → architecture disposition matrix | Completed; PR #17 merged (R1–R15 disposed; R3/R4 escalated to OQ-BP-003/OQ-BP-001) |
| #11 | Mini Cloud App P0–P9 ↔ Module/Stage alignment | Completed; PR #14 merged (per-milestone design; Technology Admission) |
| #12 | Blueprint Lab + Source Expedition selection map | Completed; PR #16 merged (5 Required / 5 Optional / 5 Source Expeditions; POSIX-thread Build correction) |
| #13 | Competency + Concept Registry integration proposal | Completed; PR #15 merged (competency table, evidence packets, 18-concept proposal) |

## Issue #9 reconciliation — COMPLETE / LEAD-ACCEPTED

Issue #9 performed the single Canonical modification pass on top of the merged inputs:

- created `meta/blueprint/final-reconciliation-v0.1.md` (integration record + canonical P0–P9 Module mapping);
- reconciled `meta/CURRICULUM_MAP.md`, `meta/COMPETENCY_MATRIX.md`, `meta/CONCEPT_REGISTRY.md`, `meta/OPEN_QUESTIONS.md`;
- updated the two Issue #1 maps (Lesson map, dependency graph) for resolved hidden prerequisites and disposition outcomes — **no DAG edge changed; graph re-verified acyclic**;
- created `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md` and `meta/rfcs/RFC-CAND-002-human-facing-boundary.md` (candidates, no decision);
- did not alter Lab selection, Mini Cloud App evolution/accepted alignment content, policies, invariants, decisions, or licensing.

**Status:** PR #18 Lead-reviewed and merged. This remains the canonical Issue #9 integration record; final Blueprint exit status is owned by Issue #23 / PR #24.

## Remaining Blueprint work — COMPLETE / DEFERRED BY DESIGN

| Workstream | Owner | Status |
|---|---|---|
| Course Charter, Learner Profile, Learning Outcomes, Bridge artifacts | Issue #19 / PR #20 | **COMPLETE — Lead-reviewed and merged** |
| Assessment Architecture consolidation | Issue #21 / PR #22 | **COMPLETE — Lead-reviewed and merged** |
| Modern Technology Case Map | Issue #21 / PR #22 | **COMPLETE — Lead-reviewed and merged** |
| Final Exit Audit | Issue #23 / PR #24 | **COMPLETE — PASS after Lead direct fixes; Blueprint v0.1 closed** |
| OQ-BP-001 / OQ-BP-003: Open Question → research → RFC/Decision | Architecture process (RFC candidates ready) | **OPEN — non-blocking until an affected slice requires a Core-scope decision** |
| OQ-BP-006 environment/version + hardware-dependent baseline pinning | First Module dossier + environment/Lab implementation | **OPEN — intentionally implementation-time** |
| Build-first bounded course production | M00–M07 implementation complete after Lead review; LAB-REQ-02 remains merged; M05–M09 Research #47/#48 and Design #50/#51 accepted; M03 GDB debt, M06 official course-fork grader NOT RUN, and OQ-BP-006 remain explicit | **ACTIVE — implement M08 next** |

## Final Blueprint gate — PASSED

Issue #23 / PR #24 audited all 30 criteria in `meta/blueprint/README.md`. The independent audit initially reported four blocking criterion rows caused by two narrow inconsistency classes. Web Lead direct fixes preserved the accepted architecture, and the narrow re-audit finished at:

- COMPLETE: 30
- PARTIAL — BLOCKING: 0
- INTENTIONALLY DEFERRED — NON-BLOCKING: 0
- NOT APPLICABLE: 0

Final recommendation: **PASS — BLUEPRINT v0.1 READY TO CLOSE**.

Blueprint v0.1 is therefore **COMPLETE / CLOSED**.

## Rules for the next phase

- The Module DAG remains authoritative; Stage narrative is not dependency; S4/S5 partial independence preserved.
- `meta/blueprint/final-reconciliation-v0.1.md` remains the Issue #9 integration/provenance record; `meta/blueprint/final-exit-audit-v0.1.md` owns the Blueprint exit result.
- Blueprint exit criteria are satisfied. Under D-027, production is build-first in bounded batches: after Research/Design and independent implementation review/verification, authoring may continue to the next ready batch without waiting for a real learner. **Issue #34 remains OPEN / DEFERRED / NON-BLOCKING** and must still use real learner evidence when resumed. Learner validation remains required before v1.0 / `RELEASED`. The M02–M04 learner packets are merged after Lead review. The accepted M00–M04 Research/Design slice is consumed. **M05–M09 Research and Design are complete/Lead-accepted; M05–M07 implementation is merged after Lead review, including LAB-REQ-02. The next valid step is bounded learner-facing M08 implementation, then independent Lead review before advancing to M09.** M03's unavailable-GDB runtime path remains explicit verification debt rather than a hidden PASS.
- Any change to Core scope (incl. decisions inside the two RFC candidates) proceeds through `Open Question → Research → RFC/Decision`.
