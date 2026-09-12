# Foundations M24 Evidence Template — Final System Defense & Pre-Ship Assessment

Use this template for **one actual learner system**. All volatile values and reviewer judgments start blank.

> **Evaluation invariant:** machine structural PASS != learner competency / capstone PASS.

## A — Environment / Execution Identity

- Execution commit/ref: `[Record actual ref]`
- Actual system under defense: Mini Cloud (`project/minicloud/`) — multi-user note/bookmark service
- Exact command(s): `python3 -m minicloud.cli walkthrough` and `bash project/scripts/smoke.sh`
- Runtime disposition per command: `[PASS / FAIL / BLOCKED / NOT RUN]`
- Host/runtime facts actually observed: `[Record, or NOT RUN]`
- OQ-BP-006: `CLOSED (technical environment-definition/realization per #167; #158 re-check still required)`

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
`[Trace actual request path in Mini Cloud: HTTP client -> minicloud.httpd -> minicloud.auth -> minicloud.service -> minicloud.store -> SQLite WAL, and response write-back]`

### 2. Data & State Trace
`[Trace actual volatile/durable/config state transitions: request JSON body -> in-memory model -> parameterized SQL in minicloud.store -> SQLite WAL frame committed to disk in project/var/]`

### 3. Control & Authority Trace
`[Trace actual identity, authority, and authorization decisions: Bearer token parsed in minicloud.auth -> caller subject passed to minicloud.service -> owner/share validation -> 404 on unowned item]`

### 4. State Inventory
`[List actual volatile (server sockets, active sessions), durable (project/var/minicloud.db, WAL, backups), and configuration state in minicloud.config; write NONE where truly absent]`

### 5. Invariants & Specifications
`[Record actual invariants: unique usernames, stable item IDs, read-after-write consistency, optimistic version bump (no lost update) enforced in minicloud.store]`

### 6. Trust Boundaries
`[Record actual trust-boundary crossings: untrusted network -> httpd.py -> auth.py token validation -> service.py resource authorization -> store.py parameterized SQL]`

### 7. Isolation Boundaries
`[Record actual process boundary (cli.py serve), filesystem isolation (project/var/), and SQLite transaction isolation (BEGIN IMMEDIATE)]`

### 8. Failure & Risk Walkthrough
`[Walk through actual failure models: indexer dependency timeout reported as ambiguous in minicloud.dependency, process kill -9 recovery via SQLite WAL crash recovery and cli.py backup/restore]`

### 9. Security & Privacy Decisions
`[Record PBKDF2 password hashing in auth.py, token generation, parameterized SQL in store.py, and credential/body redaction in minicloud.observability]`

### 10. Measurements & Performance Evidence
`[Record actual measurement evidence from python -m minicloud.cli bench --rows 2000 --repeats 10, or explicitly NOT MEASURED]`

### 11. Cost & Scale Estimates
`[Record single-process memory RSS, disk growth per item, and napkin math estimates for 10x/100x items in Mini Cloud, or NOT RUN]`

### 12. Alternatives Considered
`[Record actual D-015 alternatives: SQLite WAL single-node vs PostgreSQL, sync HTTP server vs async, custom protocol vs HTTP/JSON]`

### 13. When-Not-To-Use & Rejected Choices
`[Record rejected choices: distributed consensus/Raft rejected due to single-node simplicity, microservices rejected for bounded failure domain]`

### 14. Explicit Unknowns
- `[UNK-01]`: `[Record a real bounded unknown in Mini Cloud, e.g. behavior under extreme write-lock contention with 50+ concurrent writer threads]`
- `[UNK-02]`: `[Record another real bounded unknown, if applicable]`

### 15. Learning Plan
- `[UNK-01]` → `[Record verification/learning action using minicloud.cli race or stress harness]`
- `[UNK-02]` → `[Record verification/learning action]`

### 16. Changed-Constraint Adaptation
`[Record changed assumption from scenario card, affected invariants/evidence in Mini Cloud, candidate adaptation, trade-off, and new evidence required]`

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
