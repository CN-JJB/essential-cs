# Foundations M24 Evidence Template — Final System Defense & Pre-Ship Assessment

Use this template for **one actual learner system**. All volatile values and reviewer judgments start blank.

> **Evaluation invariant:** machine structural PASS != learner competency / capstone PASS.

## A — Environment / Execution Identity

- Execution commit/ref: `[Record actual ref]`
- Actual system under defense: `[Record actual project/system]`
- Exact command(s): `[Record exact commands]`
- Runtime disposition per command: `[PASS / FAIL / BLOCKED / NOT RUN]`
- Host/runtime facts actually observed: `[Record, or NOT RUN]`
- OQ-BP-006: `OPEN / UNRESOLVED`

## B — Architectural Claim Register

Register at least five claims.

| Claim ID | Architectural Claim Text | Evidence Category | Artifact Reference | Core Assumption | Exact Inference Limit | Validation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[CLM-01]` | `[Record claim]` | `[E01–E12]` | `[Record actual artifact/path/symbol]` | `[Record assumption]` | `[Record inference limit]` | `[VERIFIED / UNVERIFIED / NOT RUN as actually supported]` |
| `[CLM-02]` | `[Record claim]` | `[E01–E12]` | `[Record actual artifact/path/symbol]` | `[Record assumption]` | `[Record inference limit]` | `[Record truthful status]` |
| `[CLM-03]` | `[Record claim]` | `[E01–E12]` | `[Record actual artifact/path/symbol]` | `[Record assumption]` | `[Record inference limit]` | `[Record truthful status]` |
| `[CLM-04]` | `[Record claim]` | `[E01–E12]` | `[Record actual artifact/path/symbol]` | `[Record assumption]` | `[Record inference limit]` | `[Record truthful status]` |
| `[CLM-05]` | `[Record claim]` | `[E01–E12]` | `[Record actual artifact/path/symbol]` | `[Record assumption]` | `[Record inference limit]` | `[Record truthful status]` |

## C — 16-Trace Defense Dossier

### 1. Request Trace
`[Trace the actual request path and evidence anchors]`

### 2. Data & State Trace
`[Trace actual volatile/durable/config/replicated state transitions]`

### 3. Control & Authority Trace
`[Trace actual identity, authority, and authorization decisions]`

### 4. State Inventory
`[List actual volatile, durable, configuration, and replicated state; write NONE where truly absent]`

### 5. Invariants & Specifications
`[Record actual invariants/specifications and where enforced]`

### 6. Trust Boundaries
`[Record actual trust-boundary crossings, controls, and residual risks]`

### 7. Isolation Boundaries
`[Record actual process/filesystem/transaction/tenant isolation that exists]`

### 8. Failure & Risk Walkthrough
`[Walk through actual failure models; distinguish process crash, power loss, resource exhaustion, and downstream failure as applicable]`

### 9. Security & Privacy Decisions
`[Record only controls actually implemented/evidenced]`

### 10. Measurements & Performance Evidence
`[Record actual M20/M23 measurement evidence, or explicitly NOT MEASURED]`

### 11. Cost & Scale Estimates
`[Record assumption-first units/arithmetic and sensitivity, or NOT RUN]`

### 12. Alternatives Considered
`[Record actual D-015 alternatives]`

### 13. When-Not-To-Use & Rejected Choices
`[Record rejected choice, rationale, and reconsideration condition]`

### 14. Explicit Unknowns
- `[UNK-01]`: `[Record a real bounded unknown]`
- `[UNK-02]`: `[Record another real bounded unknown, if applicable]`

### 15. Learning Plan
- `[UNK-01]` → `[Record verification/learning action]`
- `[UNK-02]` → `[Record verification/learning action]`

### 16. Changed-Constraint Adaptation
`[Record changed assumption, affected invariants/evidence, candidate adaptation, trade-off, and new evidence required]`

## D — 12-Evidence-Area Traceability Matrix

| Area ID | Evidence Area Name | Claim ID(s) | Artifact Reference | Evidence Sufficiency Summary | Exact Inference Limit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E01 | End-to-End Request Flow | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E02 | State & Data Lifecycle | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E03 | Core Invariants & Specs | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E04 | Trust & Isolation Boundaries | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E05 | Failure Domains & Resilience | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E06 | Transport & App Security | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E07 | Empirical Measurement | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E08 | Capacity & Cost Models | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E09 | Trade-Off & Alternative Analysis | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E10 | Explicit Unknowns & Limits | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E11 | Changed-Constraint Adaptation | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |
| E12 | Pre-Ship Operational Readiness | `[CLM-..]` | `[artifact]` | `[summary]` | `[limit]` |

## E — Invariant / Specification Register

| Invariant / Spec | Source / Contract | Implementation Point | Failure Condition | Evidence | Inference Limit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[Record]` | `[Record]` | `[Record]` | `[Record]` | `[Record]` | `[Record]` |

## F — Trust / Isolation / Security Boundary Audit

| Boundary | Authority / Data Crossing | Protective Control | Evidence | Residual Risk / Limit |
| :--- | :--- | :--- | :--- | :--- |
| `[Record]` | `[Record]` | `[Record]` | `[Record]` | `[Record]` |

## G — Failure / Recovery Walkthrough

| Failure Scenario | Detection | Immediate State | Recovery | Availability Bound | Data-Loss Bound / N/A Rationale | Unknowns |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[Record actual failure model]` | `[Record]` | `[Record]` | `[Record]` | `[Record actual bound or NOT MEASURED]` | `[Record evidence-backed bound, or N/A with reason]` | `[Record]` |

## H — Measurement / Capacity / Cost Evidence

- Engineering question: `[Record]`
- Exact measurement/model command: `[Record, or NOT RUN]`
- Actual workload/arrival assumptions: `[Record]`
- Actual observed distribution/result: `[Record, or NOT MEASURED]`
- Units and estimate assumptions: `[Record]`
- Sensitivity result: `[Record, or NOT RUN]`
- Exact inference limit: `[Record]`

## I — Alternatives / Rejections / Unknowns / Learning Plan

- D-015 alternatives: `[Record]`
- Decision / rejection rationale: `[Record]`
- Reconsideration trigger: `[Record]`
- Unknown IDs and linked learning actions: `[Record]`

## J — Changed-Constraint Challenge

- Scenario Card ID: `[Record]`
- Original assumption: `[Record]`
- Changed constraint: `[Record]`
- Affected and unaffected invariants/evidence: `[Record]`
- Plausible bottleneck/failure shift: `[Record learner reasoning]`
- Candidate adaptation and trade-off: `[Record learner reasoning]`
- New evidence required: `[Record]`
- Inference limit: `[Record]`

## K — Pre-Ship Risk-Prioritized Evidence Matrix

| Class | ID | Target / Unknown | Methodology / Justification | Success Criterion (if applicable) | Severity | Criticality | Evidence Gap | Blast Radius if Omitted |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Must Measure | `[MM-..]` | `[Record]` | `[Record]` | `[Project/scenario-specific]` | `[Record]` | `[Record]` | `[Record]` | `[Record]` |
| Must Test | `[MT-..]` | `[Record]` | `[Record]` | `[Project-specific]` | `[Record]` | `[Record]` | `[Record]` | `[Record]` |
| Must Inspect | `[MI-..]` | `[Record]` | `[Record]` | `[Project-specific]` | `[Record]` | `[Record]` | `[Record]` | `[Record]` |
| Acceptable Unknown | `[AU-..]` | `[Record bounded unknown]` | `[Record why currently acceptable]` | N/A | `[Record]` | `[Record]` | `[Record]` | `[Record]` |

## L — Deployment Compatibility / Recovery Strategy

- Application code compatibility: `[Record actual analysis]`
- Schema/data compatibility analysis: `[Record actual analysis]`
- Chosen recovery strategy: `[Freeform project-specific strategy]`
- Recovery justification: `[Record why it fits this architecture/failure model]`
- Data loss applicable: `[true / false]`
- Stated data-loss bound, if applicable: `[Record evidence-backed bound]`
- If not applicable, reason: `[Record why]`
- Reversal/recovery verification evidence: `[Record actual evidence]`

## M — Reviewer Judgment

> Leave this section unfilled until an actual reviewer session.

- Reviewer Identity: `[Unfilled / Reviewer will complete]`
- Review Date: `[Unfilled / Reviewer will complete]`
- Evaluation Disposition: `[Unfilled / Reviewer selects PASS / REVISE / FAIL / BLOCKED / NOT RUN]`
- Evidence Sufficiency: `[Unfilled / Reviewer evaluation]`
- Changed-Constraint Coherence: `[Unfilled / Reviewer evaluation]`
- Pre-Ship Risk Prioritization / Recovery: `[Unfilled / Reviewer evaluation]`
- Mandatory Revision Items: `[Unfilled / Reviewer notes]`

## N — Currentness / Provenance / Rights / Cleanup

| Source | Version / Date / Status | Checked Date | Bounded Claim Used | Inference Limit | Rights / Provenance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[Record source]` | `[Record]` | `[Record]` | `[Record]` | `[Record]` | `[Record]` |

- Cleanup/reset command: `[Record exact command, or NOT RUN / NOT APPLICABLE]`
- Cleanup disposition: `[PASS / FAIL / BLOCKED / NOT RUN / NOT APPLICABLE]`
- Remaining course-owned scratch: `[Record actual observation]`
- Learner competency / capstone defense disposition before reviewer session: `NOT RUN`
