# Blueprint v0.1 Workstreams

## First parallel wave — COMPLETE

| Issue | Workstream | Result |
|---|---|---|
| #1 | Detailed Core stages, Module/Lesson map, dependency graph | Completed; PR #5 merged after Lead dependency-model fixes |
| #2 | External Curriculum Coverage Audit v0.1 | Completed; PR #6 merged as independent audit evidence |
| #3 | Mini Cloud App evolution map | Completed; PR #7 merged |
| #4 | Classic lab and Source Expedition candidate research | Completed; PR #8 merged after exact concurrency-source fix |

The four artifacts are **inputs to reconciliation**, not independently final Blueprint architecture.

## Active integration wave

| Issue | Workstream | Dependency / coordination |
|---|---|---|
| #9 | Reconcile Issues #1–#4 into Blueprint v0.1 maps | Parent integrator; waits for #10–#13 parallel input proposals before canonical-map integration |
| #10 | Audit recommendations → architecture disposition matrix | Parallel-safe; separate proposal artifact |
| #11 | Mini Cloud App P0–P9 ↔ Module/Stage alignment | Parallel-safe; separate proposal artifact |
| #12 | Blueprint Lab + Source Expedition selection map | Parallel-safe; separate proposal artifact |
| #13 | Competency + Concept Registry integration proposal | Parallel-safe; separate proposal artifact |

### Parallel input rule

Issues #10–#13 may run concurrently. Each owns only its dedicated proposal artifact and must not edit shared canonical Blueprint maps. After Lead review/merge, Issue #9 performs the single reconciliation/integration pass.

### #9 integration responsibilities

- reconcile audit recommendations R1–R15 against the detailed Module/Lesson proposal;
- keep the Module DAG authoritative and distinguish hard prerequisites from preferred narrative;
- map Mini Cloud App P0–P9 to the reconciled architecture;
- turn lab/source research into a Blueprint selection map using Adopt → Adapt → Build;
- integrate Stage/Module/Lab/Project competency coverage;
- seed stable Concept Registry first-introduction/revisit decisions;
- escalate Core-scope conflicts through Open Question → RFC/Decision.

## Parallel plan

Avoid parallel edits to the same canonical Blueprint maps while #9 is active.

Targeted research may run in parallel only when #9 or an Open Question identifies a bounded evidence gap and the research has a separate file/ownership claim.

## Semantic ownership

- Issue #1 artifact remains the proposed curriculum/dependency architecture input.
- Issue #2 remains audit evidence and does not silently rewrite architecture.
- Issue #3 owns the proposed Mini Cloud App evolution logic, not Core scope.
- Issue #4 owns candidate research, not final Lab implementation.
- Issue #9 owns **reconciliation proposals**; major Core-scope changes still require the repository's architecture decision path.

No large-scale Lesson writing begins until Blueprint v0.1 exit criteria are satisfied.
