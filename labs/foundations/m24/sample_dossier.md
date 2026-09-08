# Synthetic M24 Architecture Defense Reference Fixture

> FIXTURE CLASS: COURSE-OWNED SYNTHETIC REFERENCE SCENARIO
> NOT LEARNER EVIDENCE. NOT A DESCRIPTION OF A REAL REPOSITORY APPLICATION.
> All workload numbers, system components, and behavior statements below are scenario assumptions or structural examples unless a course-owned executable artifact is explicitly cited.
> A learner must replace every scenario assumption with evidence from the actual system under defense.

## Architectural Claim Register

| Claim ID | Architectural Claim Text | Evidence Category | Artifact Reference | Core Assumption | Exact Inference Limit | Validation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CLM-01 | The synthetic scenario distinguishes volatile, durable, and configuration state | E02 / E03 | Trace 2 and Trace 4 | The reference architecture uses one local SQLite database | Course reference only; says nothing about a learner system | COURSE_REFERENCE_ONLY |
| CLM-02 | The synthetic scenario places authentication and resource authorization at separate decision points | E04 / E06 | Trace 3 and Trace 6 | A credential-verification step exists before resource policy | Course reference only; actual auth mechanism must be evidenced by learner | COURSE_REFERENCE_ONLY |
| CLM-03 | No latency or throughput claim is treated as measured until an actual M23 observation is attached | E07 | Trace 10 | Measurement evidence may be absent at dossier-drafting time | Structural honesty only; no performance result is established | UNVERIFIED_MEASUREMENT_REQUIRED |
| CLM-04 | Capacity and cost conclusions must expose their units and assumptions | E08 | Trace 11 | Scenario arithmetic uses explicit inputs rather than current cloud prices | Estimate only; not a host capacity or billing fact | COURSE_REFERENCE_ONLY |
| CLM-05 | The bundled SQLite migration helper can test whether one specified old query still executes after one specified migration | E12 | labs/foundations/m24/preship_validator.py | Python sqlite3 supports the exercised DDL on the host | Proves only the executed DDL/query pair, not whole-application rollback safety | COURSE_FIXTURE_EXECUTABLE |

## 16 Core Architectural Traces

### 1. Request Trace
Synthetic reference: client request enters a local service, crosses a request parser/router, reaches an application handler, may access local storage, then produces a response. The learner must replace this with actual function/protocol/file anchors from the real project.

### 2. Data & State Trace
Synthetic reference: request bytes become temporary process state; application state may be written through SQLite into database or WAL files depending on the actual journal configuration. Durability across process crash and power loss must be separated and tied to the real synchronous/filesystem settings.

### 3. Control & Authority Trace
Synthetic reference: a credential or session context is checked, then a separate resource-authorization decision is made. No concrete token algorithm, role model, or tenant model is asserted for a learner system.

### 4. State Inventory
Synthetic state classes:
- volatile: request objects and connection-local buffers;
- durable: one local database file if the project actually persists data;
- configuration: process startup settings;
- replicated: none in this synthetic single-node reference.
The learner must replace these with the actual state inventory.

### 5. Invariants & Specifications
Reference invariant examples: identifiers are unique where the schema requires it; unauthorized actions are rejected at the resource boundary; acknowledged persistence claims are conditional on the actual storage configuration. No fixed password cost, token lifetime, timeout, or throughput constant is supplied.

### 6. Trust Boundaries
Reference boundaries: untrusted client input to application parsing; application process to filesystem/database API; authenticated identity context to authorization policy. The learner must map actual privileges and residual risks.

### 7. Isolation Boundaries
Reference examples: operating-system process memory separation, filesystem permissions, path confinement where implemented, and database-transaction visibility. SQLite normally provides serializable isolation across connections; WAL permits concurrent readers and a writer with snapshot semantics, while still having one writer at a time.

### 8. Failure & Risk Walkthrough
Reference questions: what happens on process crash, power loss, disk-full condition, and slow/downstream interaction? For SQLite WAL, process-crash consistency and power-loss durability are not the same claim; synchronous mode and storage behavior matter. No zero-data-loss result is supplied.

### 9. Security & Privacy Decisions
Reference questions: where are inputs structurally separated from SQL syntax, where are credentials checked, what sensitive values are excluded from logs, and what transport boundary actually exists? The sample does not claim TLS, a reverse proxy, a particular password cost, or a particular token lifetime exists.

### 10. Measurements & Performance Evidence
Status: NOT MEASURED IN THIS REFERENCE FIXTURE.
A learner must attach actual question-driven M20/M23 evidence before claiming throughput, latency percentiles, clock resolution, memory growth, or saturation. The structural validator intentionally accepts an explicit unmeasured state; the reviewer decides whether that is sufficient for the learner's claim set.

### 11. Cost & Scale Estimates
Synthetic arithmetic example only: if an explicit scenario states N records per day, B bytes per record, R retention days, and a replication/overhead multiplier M, retained bytes are estimated from those declared inputs. No current cloud price, host size, network price, or universal scaling threshold is supplied.

### 12. Alternatives Considered
Reference process: compare at least two feasible alternatives using D-015 dimensions that matter to the actual project. The sample does not preselect SQLite, PostgreSQL, Redis, Kafka, microservices, or cloud services as a universal winner or loser.

### 13. When-Not-To-Use & Rejected Choices
Reference process: state one rejected option, why it does not fit the current requirements, and what changed evidence would cause reconsideration. Rejection quality remains reviewer-required.

### 14. Explicit Unknowns
- UNK-01: Actual power-loss durability is unknown until the learner records the SQLite synchronous mode, filesystem/storage assumptions, and an admissible test or specification boundary.
- UNK-02: Actual high-load latency behavior is unknown until the learner runs a question-driven measurement on the target host and workload.

### 15. Learning Plan
- UNK-01 plan: inspect the actual SQLite configuration and official durability contract, then design a bounded course-owned durability observation appropriate to the project.
- UNK-02 plan: define arrival model, workload, clock, stopping rule, and interference assumptions, then gather actual M23-style evidence on the learner host.

### 16. Changed-Constraint Adaptation
Reference challenge: choose one course scenario card, state which assumption changed, identify affected invariants/evidence, propose an adaptation only if needed, and list new evidence. This sample deliberately does not provide a canonical adaptation answer.

## 12-Evidence-Area Traceability Matrix

| Area ID | Evidence Area Name | Primary Claim ID(s) | Primary Artifact Reference | Evidence Sufficiency Summary | Exact Inference Limit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E01 | End-to-End Request Flow | CLM-01 | Trace 1 | Synthetic trace shows the required evidence shape | Learner must replace it with actual request-flow evidence |
| E02 | State & Data Lifecycle | CLM-01 | Trace 2 | Course reference maps volatile, durable, and configuration state | Synthetic fixture only; learner must replace with actual state evidence |
| E03 | Core Invariants & Specs | CLM-01 | Trace 5 | Reference demonstrates conditional invariant wording | Does not prove any learner invariant |
| E04 | Trust & Isolation Boundaries | CLM-02 | Trace 6 and Trace 7 | Reference separates trust and isolation questions | Actual privileges and controls remain unverified |
| E05 | Failure Domains & Resilience | CLM-01 | Trace 8 | Reference distinguishes crash from power-loss questions | No recovery or durability result is measured |
| E06 | Transport & App Security | CLM-02 | Trace 9 | Reference lists security evidence categories | No TLS, token, or security control is asserted present |
| E07 | Empirical Measurement | CLM-03 | Trace 10 | Explicit NOT MEASURED state prevents fabricated performance | Learner needs actual observation before performance claims |
| E08 | Capacity & Cost Models | CLM-04 | Trace 11 | Reference requires explicit variables and units | No current price or host-capacity result is established |
| E09 | Trade-Off & Alternative Analysis | CLM-04 | Trace 12 and Trace 13 | D-015 process shape is demonstrated | Reviewer must judge decision quality |
| E10 | Explicit Unknowns & Limits | CLM-03 / CLM-04 | Trace 14 and Trace 15 | UNK identifiers are linked to learning actions | Unknown resolution remains future evidence |
| E11 | Changed-Constraint Adaptation | CLM-03 | Trace 16 | Reference identifies the required reasoning fields | No adaptation is machine-selected or graded |
| E12 | Pre-Ship Operational Readiness | CLM-05 | labs/foundations/m24/sample_preship.json | Course fixture shows the risk-matrix structure | Structural fixture does not authorize a real release |

## Reviewer Judgment

> Final evaluation is completed only during an actual learner/reviewer defense session.

- Reviewer Identity: [Unfilled / Reviewer will complete]
- Review Date: [Unfilled / Reviewer will complete]
- Evaluation Disposition: [Unfilled / Reviewer selects PASS / REVISE / FAIL / BLOCKED / NOT RUN]
- Evidence Sufficiency: [Unfilled / Reviewer evaluation]
- Changed-Constraint Coherence: [Unfilled / Reviewer evaluation]
- Mandatory Revision Items: [Unfilled / Reviewer notes]
