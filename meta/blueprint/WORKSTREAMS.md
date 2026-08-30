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

## Issue #9 reconciliation — INTEGRATED (under Lead review)

Issue #9 performed the single Canonical modification pass on top of the merged inputs:

- created `meta/blueprint/final-reconciliation-v0.1.md` (integration record + canonical P0–P9 Module mapping);
- reconciled `meta/CURRICULUM_MAP.md`, `meta/COMPETENCY_MATRIX.md`, `meta/CONCEPT_REGISTRY.md`, `meta/OPEN_QUESTIONS.md`;
- updated the two Issue #1 maps (Lesson map, dependency graph) for resolved hidden prerequisites and disposition outcomes — **no DAG edge changed; graph re-verified acyclic**;
- created `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md` and `meta/rfcs/RFC-CAND-002-human-facing-boundary.md` (candidates, no decision);
- did not alter Lab selection, Mini Cloud App evolution/accepted alignment content, policies, invariants, decisions, or licensing.

**Status:** READY FOR LEAD REVIEW (one PR, `Closes #9`). Do not mark `VERIFIED` before Lead review.

## Remaining Blueprint work

| Workstream | Owner | Status |
|---|---|---|
| Lead review of the #9 PR (direct-fix small inconsistencies; escalate large ones) | Web Lead | Pending — current primary workstream |
| Course Charter, Learner Profile, Learning Outcomes, Bridge artifacts | Blueprint task (after #9) | Not started — exit-criteria gaps |
| Assessment Architecture consolidation (packet model exists in COMPETENCY_MATRIX) | Blueprint task (after #9) | Partial |
| Modern Technology Case Map | Blueprint task (after #9) | Partial (D-015 framework + project admission table exist) |
| OQ-BP-001 / OQ-BP-003: Open Question → research → RFC/Decision | Architecture process (RFC candidates ready) | Open — Core-scope, not decided |
| OQ-BP-006 environment/version pinning + latency-constant list | Module dossiers + lab implementation | Open — implementation-time |
| Stage-by-stage vertical slices (Research → Design → Lesson → Lab → Project → Verification → Learner Validation) from an early Foundations slice | Post-Blueprint | Blocked on exit criteria |

## Rules for the next phase

- The Module DAG remains authoritative; Stage narrative is not dependency; S4/S5 partial independence preserved.
- `meta/blueprint/final-reconciliation-v0.1.md` is the record of which proposal artifacts became canonical and what remains proposal-only.
- No large-scale Lesson writing begins until Blueprint v0.1 exit criteria are satisfied (`meta/blueprint/README.md`; gap list in `final-reconciliation-v0.1.md` §11).
- Any change to Core scope (incl. decisions inside the two RFC candidates) proceeds through `Open Question → Research → RFC/Decision`.
