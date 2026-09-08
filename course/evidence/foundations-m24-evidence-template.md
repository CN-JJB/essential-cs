# Foundations M24 Evidence Template — Final System Defense & Pre-Ship Assessment

Use this template for **one actual learner capstone defense and pre-ship assessment observation**. Do not prefill or copy another learner's runtime values, candidate timings, percentiles, claim IDs, data-loss numbers, or PASS/FAIL evaluations.

> **Evaluation Invariant**: Machine PASS != learner competency PASS. Automated checks prove only structural completeness and syntactic traceability of documents and fixtures. Learner competency, evidence sufficiency, architectural defense quality, and final M24 PASS remain strictly **REVIEWER-REQUIRED** judgment.

---

## A — Environment / Execution Identity

- Execution commit / ref: `[Record actual HEAD commit SHA under defense]`
- Exact command(s) actually executed: `[Record command text exactly, e.g. python tests/preflight_security_synthesis.py --module M24 && python labs/foundations/m24/activity_l24_01.py]`
- Exact runtime disposition for each command: `[Record PASS / FAIL / BLOCKED / NOT RUN; never infer PASS from capability absence]`
- Actual project / system under defense: `[State the actual learner system under defense, e.g. Single-node Mini Cloud App with SQLite WAL persistence and loopback HTTP service]`
- Host Operating System / kernel / platform: `[Record actual OS, release, architecture]`
- Python Implementation & Version: `[Record actual Python implementation and version]`
- Course-Owned Scratch Directory Writability: `[Record PASS / BLOCKED / NOT RUN]`
- OQ-BP-006 Environment Policy Status: `OPEN / UNRESOLVED (Capability-based evaluation; no course-wide CPython pin frozen in learner truth)`

---

## B — Architectural Claim Register

Register at least five core architectural claims grounded in the actual system:

| Claim ID | Architectural Claim Text | Evidence Category (E01–E12) | Artifact Reference (Path/Symbol) | Core Assumption | Exact Inference Limit | Validation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[CLM-01]` | `[e.g., Committed data survives sudden process crash without corruption]` | `[E05 / E02]` | `[labs/foundations/m09 WAL recovery tests / sqlite3 pragma synchronous]` | `[Filesystem respects fsync barrier]` | `[Single-node process crash only; zero multi-region HA claimed]` | `[VERIFIED_BY_TEST / UNVERIFIED]` |
| `[CLM-02]` | `[e.g., SQL queries are structurally immune to parameter injection]` | `[E06]` | `[Parameterized query calls in app/db.py + security tests]` | `[Database driver uses prepared statements]` | `[Proves parameter isolation; does not prevent application logic flaws]` | `[VERIFIED_BY_INSPECTION / UNVERIFIED]` |
| `[CLM-03]` | `[e.g., Baseline steady-state throughput meets scenario target within latency budget]` | `[E07]` | `[labs/foundations/m23 arrival-scheduled latency histogram]` | `[Arrival load bounded to scenario rate; CPU not oversubscribed]` | `[Valid for tested concurrency on host hardware; not a universal cloud claim]` | `[EMPIRICALLY_MEASURED / UNVERIFIED]` |
| `[CLM-04]` | `[e.g., Storage growth remains bounded under configured retention policy]` | `[E08]` | `[Fermi storage model + vacuum/cleanup job config]` | `[Daily mutation rate <= 50,000 records; 30-day retention]` | `[Assumes regular purge runs; disk full if retention disabled]` | `[BOUNDED_BY_MODEL / UNVERIFIED]` |
| `[CLM-05]` | `[e.g., Additive schema migrations permit safe backward code rollback]` | `[E12]` | `[labs/foundations/m24 migration rollback simulation log]` | `[New columns are nullable or have defaults]` | `[Applies to additive schema changes; destructive drops require roll-forward]` | `[VERIFIED_BY_SIMULATION / UNVERIFIED]` |

---

## C — 16-Trace Defense Dossier

Complete substantive analysis for all 16 core traces. Do not omit any trace and do not leave placeholder text:

### 1. Request Trace
- *Entry Point*: `[Trace HTTP request arrival at OS socket, ephemeral port bind, and event-loop dispatch]`
- *Transport & Framing*: `[Trace parsing of HTTP/1.1 headers, Content-Length/chunked framing per M11]`
- *Handler Routing*: `[Trace URL path matching, middleware execution, and route handler dispatch]`
- *Execution & Response*: `[Trace database interaction, response serialization, status code generation, and socket flush]`

### 2. Data & State Trace
- *Ingress*: `[Trace request payload parsing and deserialization in memory]`
- *Buffer & Cache*: `[Trace page buffer mutation, dirty page marking, and OS page cache transition]`
- *Disk Persistence*: `[Trace WAL append, flushed_lsn vs page_lsn invariant per M09, and explicit fsync boundary]`
- *Egress*: `[Trace query fetch from persistent storage back to client response buffer]`

### 3. Control & Authority Trace
- *Call Graph*: `[Trace synchronous and asynchronous invocation paths across application modules]`
- *Identity Verification*: `[Trace bearer token / session cookie parsing and signature/HMAC verification per M22]`
- *Authorization Decision*: `[Trace permission evaluation against authenticated subject; verify ambient authority is rejected]`
- *Privilege Boundaries*: `[Trace unprivileged execution context and denial fail-closed return]`

### 4. State Inventory
- *Volatile State*: `[List in-memory caches, connection pools, socket buffers, and transient metrics with lifecycle bounds]`
- *Durable State*: `[List SQLite primary database file, WAL file, and local filesystem uploads with durability guarantees]`
- *Replicated State*: `[State explicitly: "NONE — Single-node architecture; zero replicated state claimed", or list actual state if present]`
- *Configuration State*: `[List environment variables, secret mounts, and immutable launch configurations]`

### 5. Invariants & Specifications
- *Data Integrity Invariants*: `[List explicit relational integrity rules, foreign keys, unique constraints, and schema versions]`
- *Concurrency Invariants*: `[List transaction isolation level (e.g. SQLite WAL multi-reader single-writer) and locking semantics]`
- *Security Invariants*: `[List password hashing work factor, token expiration, and CSRF token binding invariants]`
- *Liveness & Safety Specs*: `[List timeout bounds, retry maximums, and circuit breaker tripping conditions]`

### 6. Trust Boundaries
- *Network Perimeter*: `[Identify untrusted client network vs localhost loopback interface boundary]`
- *Process Perimeter*: `[Identify OS process boundary separating application from database process or host daemon]`
- *Authority Crossing*: `[Detail how inputs are validated, sanitized, and type-checked before crossing into privileged storage]`
- *Residual Perimeter Risk*: `[Document unmitigated risk at the perimeter (e.g., local host root compromise)]`

### 7. Isolation Boundaries
- *Memory Isolation*: `[Detail virtual memory page protection (M07) preventing inter-process memory snooping]`
- *Filesystem Confinement*: `[Detail directory confinement (M21 commonpath/resolve) preventing path traversal]`
- *Transaction Isolation*: `[Detail ACID isolation level preventing dirty reads and non-repeatable reads per M14]`
- *Tenant Isolation*: `[Detail row-level tenant_id filtering and logical data separation]`

### 8. Failure & Risk Walkthrough
- *Process Crash (`kill -9`)*: `[Walk through immediate death: WAL recovery replay on restart, uncommitted transaction rollback, zero corruption]`
- *Power Cut / Host Reset*: `[Walk through dirty page loss bounded to last fsync; verify database file consistency]`
- *Disk Full (ENOSPC)*: `[Walk through fail-closed write refusal, read-only mode degradation, and operator alert]`
- *Downstream Timeout*: `[Walk through network partition or slow dependency: bounded timeout, error budget deduction, no thread exhaustion]`

### 9. Security & Privacy Decisions
- *Cryptographic Primitives*: `[List PBKDF2/Argon2id for passwords, HMAC-SHA256 for tokens, CSPRNG secrets.token_bytes]`
- *Injection Mitigations*: `[Detail parameterized SQL query binding; zero string concatenation in queries]`
- *Transport Protection*: `[Detail TLS 1.3 configuration, cipher suite restriction, and certificate validation per M11/M21]`
- *Data Privacy & Logging*: `[Detail redaction of passwords, tokens, and PII from application and access logs]`

### 10. Measurements & Performance Evidence
- *Experiment Design*: `[State specific engineering question driving the performance benchmark]`
- *Arrival Workload Model*: `[Detail open-arrival schedule model and justification; contrast with closed loop]`
- *Latency Distribution*: `[Record empirical percentiles: Min, p50, p90, p95, p99, Max under modeled load]`
- *Hardware & Measurement Limits*: `[State monotonic clock source, timer resolution, and host hardware environment limits]`

### 11. Cost & Scale Estimates
- *Compute Sizing*: `[Provide Fermi estimation for CPU cores needed to sustain peak request volume]`
- *Memory Footprint*: `[Estimate process RSS, connection pool buffers, and OS page cache sizing]`
- *Storage Capacity*: `[Calculate daily WAL volume, steady-state DB size, and 1-year disk requirement with retention]`
- *Network Egress*: `[Calculate peak and average outbound bandwidth in Mbps and monthly cloud egress cost estimate]`

### 12. Alternatives Considered
- *Evaluated Frameworks/DBS*: `[Record structured D-015 comparison between SQLite and client-server DB (PostgreSQL) or flat files]`
- *Evaluated Concurrency Models*: `[Record comparison between multi-threaded worker pool vs async event loop vs multi-process]`
- *Decision Factors*: `[Detail latency, operational simplicity, cost, and developer cognitive budget weights]`

### 13. When-Not-To-Use & Rejected Choices
- *Rejected Technology 1*: `[e.g., Rejected Redis distributed cache — justified by low working-set size and avoiding network hop]`
- *Rejected Technology 2*: `[e.g., Rejected Kafka message broker — justified by single-node simplicity and avoiding JVM/Zookeeper operational overhead]`
- *Rejected Architecture*: `[e.g., Rejected microservices decomposition — justified by team size and in-process call efficiency]`
- *Condition for Reconsideration*: `[State the exact scale or latency threshold that would trigger revisiting the rejected choice]`

### 14. Explicit Unknowns
- *Technical Blind Spot 1*: `[Record specific unmeasured edge case, e.g. SQLite performance when DB size exceeds RAM by 10x]`
- *Technical Blind Spot 2*: `[Record specific unmeasured edge case, e.g. System behavior under sustained 80% packet loss on client link]`
- *Boundary Acknowledgment*: `[Explicitly confirm: Unknowns are acknowledged as technical realities, not concealed]`

### 15. Learning Plan
- *Investigation Action 1*: `[Detail synthetic test harness to simulate 50GB SQLite database and measure VDBE latency]`
- *Investigation Action 2*: `[Detail network link emulator test using tc/netem to measure client timeout behavior under high packet loss]`
- *Milestone / Deliverable*: `[State timeline or milestone when findings will be reported to the architecture log]`

### 16. Changed-Constraint Adaptation
- *Assigned Scenario Card*: `[Record scenario ID, e.g. SCENARIO_01_HIGH_LATENCY or SCENARIO_02_100X_DATA]`
- *Perturbed Assumption*: `[Identify exactly what assumption changed: data volume, network RTT, client hostility, etc.]`
- *Broken Invariants / Bottlenecks*: `[Diagnose which data structures, thread pools, or queries become invalid or saturated]`
- *Sound Architectural Adaptation*: `[Formulate concrete design adaptations preserving system correctness without hand-waving]`
- *New Evidence Needed*: `[Specify the empirical measurements or tests required to validate the adapted architecture]`

---

## D — 12-Evidence-Area Traceability Matrix

Map all 12 evidence areas (E01–E12) to Claim IDs and physical evidence artifacts:

| Area ID | Evidence Area Name | Primary Claim ID(s) | Primary Artifact Reference (Path & Identifier) | Evidence Sufficiency Summary |
| :--- | :--- | :--- | :--- | :--- |
| **E01** | End-to-End Request Flow | `[CLM-01, ...]` | `[book/24-final-system-defense/visuals/FIG-M24-01-..., app/server.py]` | `[Trace unbroken from socket to disk and back]` |
| **E02** | State & Data Lifecycle | `[CLM-01]` | `[app/db.py, sqlite3 WAL pragma config]` | `[Volatile vs durable boundaries clearly distinguished]` |
| **E03** | Core Invariants & Specs | `[CLM-01, CLM-02]`| `[tests/test_invariants.py, schema.sql]` | `[Relational constraints and crash rollback verified]` |
| **E04** | Trust & Isolation Boundaries | `[CLM-02]` | `[app/auth.py, tests/test_security.py]` | `[Zero ambient authority; path confinement verified]` |
| **E05** | Failure Domains & Resilience | `[CLM-01]` | `[labs/foundations/m09 WAL crash tests, failure walkthrough]` | `[Crash recovery verified; SPOF explicitly documented]` |
| **E06** | Transport & App Security | `[CLM-02]` | `[app/auth.py, tests/test_auth.py, CSP headers]` | `[Parameterized SQL + token HMAC verified]` |
| **E07** | Empirical Measurement | `[CLM-03]` | `[labs/foundations/m23 arrival latency distribution]` | `[Open arrival schedule; p50/p90/p99 recorded]` |
| **E08** | Capacity & Cost Models | `[CLM-04]` | `[labs/foundations/m23/fermi_cost.py calculation card]` | `[Fermi compute/memory/disk bounds with units]` |
| **E09** | Trade-Off & Alternative Analysis | `[CLM-01, ...]` | `[labs/foundations/m23/activity_l23_02.py ADR record]` | `[D-015 evaluation with at least 1 rejected choice]` |
| **E10** | Explicit Unknowns & Limits | `[CLM-03, ...]` | `[Section C Trace 14 & 15 documentation]` | `[Explicit technical blind spots with learning plan]` |
| **E11** | Changed-Constraint Adaptation | `[CLM-03, ...]` | `[Section C Trace 16 & Section J adaptation report]` | `[Coherent redesign under perturbed scenario]` |
| **E12** | Pre-Ship Operational Readiness | `[CLM-05]` | `[labs/foundations/m24/activity_l24_02.py, Section K/L]` | `[Risk matrix, rollback strategy, healthz verified]` |

---

## E — Invariant / Specification Register

| Invariant ID | System Invariant Text | Formal Spec / RFC Authority | Implementation Code Point | Failure Mode if Broken | Verification Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[INV-01]` | `[User email must be unique across all active accounts]` | `[Relational Spec]` | `[schema.sql: UNIQUE(email)]` | `[Account collision / duplicate identity]` | `[tests/test_db.py: test_duplicate_email_rejected]` |
| `[INV-02]` | `[Token signature valid for <= 3600 seconds from issuance]` | `[TeachingProfile-BearerV1]`| `[app/auth.py: verify_token]` | `[Replay attack with stale token]` | `[tests/test_auth.py: test_expired_token_rejected]` |
| `[INV-03]` | `[Committed transaction flushed to WAL before client ACK]` | `[ACID Durability / M09]` | `[app/db.py: commit + fsync]` | `[Acknowledged write lost on crash]` | `[labs/foundations/m09/test_m09.py: test_wal_durability]` |

---

## F — Trust / Isolation / Security Boundary Audit

| Boundary Identifier | Privilege Domain A (Source) | Privilege Domain B (Target) | Crossing Data & Authority | Protective Control Mechanism | Residual Risk / Inference Limit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[BND-01]` | Untrusted Client Browser | Localhost HTTP Worker | Raw HTTP Request & Form Data | HTTP parser size limits + method allowlist | DoS via malformed packet flood at socket layer |
| `[BND-02]` | Anonymous Public Endpoint | Authenticated User Session | Authorization Bearer Header | HMAC-SHA256 constant-time verification | Stolen token used before expiration |
| `[BND-03]` | Application Worker | Local SQLite File Engine | SQL Query & Parameters | PreparedStatement binding (Zero string concat) | Zero defense if local SQLite library has binary 0-day |

---

## G — Failure / Recovery Walkthrough

| Failure Scenario | Detection Mechanism | Immediate System State | Recovery Procedure | Stated Availability Bound | Stated Data-Loss Bound | Known Unknowns |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[Host Process Crash]` | OS supervisor / PID death | Process terminated, socket closed | OS restarts process; SQLite replays WAL | 0% availability for ~2.5s restart window | Zero loss for committed WAL frames; uncommitted aborted | Exact memory state of in-flight connection lost |
| `[Sudden Power Outage]` | Host reboot init scripts | OS cold boot, dirty cache dropped | SQLite recovery cleans uncommitted frames | 0% availability until host reboots | Loss strictly bounded to un-fsynced OS write cache | Hardware controller write-cache persistence |
| `[Disk Full Error]` | `sqlite3.OperationalError` | Writes fail with ENOSPC; reads succeed | Application rejects mutations; triggers alert | Read-only availability; 0% write availability | Zero corruption; new writes rejected cleanly | Rate of log disk consumption by background tasks |

---

## H — Measurement / Capacity / Cost Evidence

Record empirical and Fermi model evidence from M20/M23 or newly measured on actual system (zero fabricated data):

- Workload Benchmark Command: `[Record exact command, e.g. python labs/foundations/m23/activity_l23_01.py]`
- Empirical Latency Profile (at modeled scenario load):
  - Sample Count: `[Record N]`
  - Min: `[Record ms]`
  - p50 (Median): `[Record ms]`
  - p90: `[Record ms]`
  - p95: `[Record ms]`
  - p99: `[Record ms]`
  - Max: `[Record ms]`
- Capacity Sizing (Napkin Math from M23):
  - Peak Concurrent Connections: `[Record connections, e.g. 50]`
  - Target Throughput: `[Record req/sec, e.g. 200 req/s]`
  - Steady-State RAM Usage (RSS): `[Record MB, e.g. 45 MB]`
  - Annual Storage Growth: `[Record GB/year with explicit retention assumptions]`
  - Monthly Egress Bandwidth: `[Record GB/month and estimated host egress cost]`

---

## I — Alternatives / Rejections / Unknowns / Learning Plan

- D-015 Evaluated Alternatives: `[Record candidate comparison, e.g. SQLite WAL vs PostgreSQL 16 vs RedisJSON]`
- Rejected Technology & Justification: `[State rejected candidate and explain why, e.g. Rejected Redis: adds second network failure domain, out-of-core memory risk, and unnecessary operational burden for target 200 req/s workload]`
- Prioritized Unknowns:
  - Unknown 1: `[Describe technical blind spot]` → Plan: `[Describe verification experiment]`
  - Unknown 2: `[Describe technical blind spot]` → Plan: `[Describe verification experiment]`

---

## J — Changed-Constraint Challenge

- Selected Scenario Card ID: `[Record Scenario Card ID, e.g. SCENARIO_01_HIGH_LATENCY or SCENARIO_02_100X_DATA]`
- Original Baseline Assumption: `[State original assumption, e.g. Database size fits entirely in RAM; client latency < 5ms]`
- Perturbed Constraint: `[State new constraint, e.g. Database size grows to 100GB (exceeding 8GB RAM by 12x); client latency = 200ms]`
- Impact on Invariants: `[Identify which invariants remain intact and which are threatened]`
- Identified Bottlenecks: `[Identify the primary bottleneck shift, e.g. From CPU-bound VDBE execution to disk I/O seek thrashing]`
- Concrete Architectural Adaptation: `[Describe specific architectural evolution, e.g. Introduce index covering, partition tables, separate archival storage]`
- Verification Strategy for Adapted Architecture: `[Detail tests/measurements required to prove adaptation validity]`

---

## K — Pre-Ship Risk-Prioritized Evidence Matrix

Classify pre-ship verification items across the four mandatory classes:

| Class | Item Identifier | Specific Verification Target | Methodology / Command | Success Threshold (Scenario-Specific) | Blast Radius if Omitted |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Must Measure** | `[MM-01]` | Memory RSS leak under sustained load | 30-minute burn-in loop | Memory growth <= 5% over 10,000 requests | Worker OOM crash after 48h production run |
| **Must Measure** | `[MM-02]` | Latency distribution under open arrival | `labs/foundations/m23/activity_l23_01.py` | Scenario target: p99 < 150ms at 100 req/s | Unexpected customer timeouts under load |
| **Must Test** | `[MT-01]` | Authentication & token expiration | `tests/test_auth.py` | All expired/tampered tokens return 401 | Critical authentication bypass |
| **Must Test** | `[MT-02]` | Atomic rollback on multi-table write | `tests/test_db_transactions.py` | Crash midway leaves DB in pre-tx state | Partial record orphan / data corruption |
| **Must Inspect** | `[MI-01]` | Secret key presence in repository | `git grep -i "secret_key" && config audit` | Zero private credentials in commit tree | Key compromise via source leak |
| **Must Inspect** | `[MI-02]` | Database migration backward compatibility | `labs/foundations/m24/activity_l24_02.py` | New columns nullable or have defaults | Production crash upon rollback to old code |
| **Acceptable Unknown** | `[AU-01]` | Multi-hour host datacenter power loss | Explicitly documented out-of-scope risk | N/A — Single-node SLA constraint | Service down until power restored (accepted) |

---

## L — Deployment Compatibility / Recovery Strategy

- Application Code Compatibility: `[State whether candidate code introduces breaking API changes; verify client backward compatibility]`
- Database Schema Compatibility:
  - Migration Type: `[Additive (Nullable column/new table) / Destructive (Column drop/rename/type alter)]`
  - Backward Compatibility Audit: `[Explain whether old application code runs safely against the new schema]`
- Chosen Recovery Strategy: `[Select exactly one: Code Rollback / Roll-Forward / Migration Reversal / Snapshot Recovery]`
  - Recovery Justification: `[Explain why chosen strategy is optimal given the schema compatibility nature]`
  - Stated Data-Loss Bound: `[State explicit data-loss bound, e.g. "Committed transactions: Zero loss. In-flight requests: Bounded to maximum connection timeout (10s)."]`
  - Reversal Verification Evidence: `[Reference simulation log from labs/foundations/m24/activity_l24_02.py verifying recovery steps]`

---

## M — Reviewer Judgment

> **Important**: This section MUST remain unfilled by the learner and automated tools. The final evaluation is exclusively completed by the technical reviewer / Web Lead.

- Reviewer Identity: `[Unfilled / Reviewer will complete]`
- Review Date: `[Unfilled / Reviewer will complete]`
- Evaluation Disposition: `[Unfilled — Reviewer selects PASS / REVISE / FAIL / BLOCKED / NOT RUN]`
- Architectural Defense Feedback:
  - 16-Trace Quality & Causality: `[Unfilled / Reviewer evaluation]`
  - Evidence Sufficiency: `[Unfilled / Reviewer evaluation]`
  - Changed-Constraint Coherence: `[Unfilled / Reviewer evaluation]`
  - Pre-Ship Risk Prioritization & Recovery: `[Unfilled / Reviewer evaluation]`
- Mandatory Revision Items (if REVISE): `[Unfilled / Reviewer notes]`

---

## N — Currentness / Provenance / Rights / Cleanup

- Standard & Citation Recheck:
  - Google SRE Book (Production Environment, PRR, Canarying): Rechecked STABLE (2026-09)
  - SEI/CMU ATAM Architecture Evaluation: Rechecked STABLE (2026-09)
  - Martin Fowler Evolutionary Database Design: Rechecked STABLE (2026-09)
  - Python Standard Library (PEP 557 dataclasses, sqlite3, unittest): Rechecked CURRENT (2026-09-08)
- Rights & Provenance Affirmation: All evidence templates, risk matrices, and defense traces are original Essential CS engineering synthesis. Zero proprietary assessment rubrics copied.
- Environment Cleanup Verification: Course-owned `.scratch` directories created during validation have been cleaned up via `python labs/foundations/m24/reset.py`.
