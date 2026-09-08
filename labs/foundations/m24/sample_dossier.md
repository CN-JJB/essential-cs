# Mini Cloud App Capstone Architectural Defense Dossier

> **Author**: Sample Essential CS Learner
> **Target System**: Single-Node Mini Cloud App (SQLite WAL persistence, loopback HTTP service)
> **Canonical Module**: M24 — Final System Defense & Pre-Ship Assessment

---

## Architectural Claim Register

| Claim ID | Architectural Claim Text | Evidence Category (E01–E12) | Artifact Reference (Path/Symbol) | Core Assumption | Exact Inference Limit | Validation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `CLM-01` | Committed transactions survive sudden process termination without data corruption | E05 / E02 | `labs/foundations/m09/test_m09.py:test_wal_recovery` | Host OS and disk honor fsync barrier | Single-node crash consistency only; zero automated multi-region failover | VERIFIED_BY_TEST |
| `CLM-02` | User input fields are structurally protected from SQL injection vulnerabilities | E06 | `app/db.py:execute_query_parameterized` | DB driver utilizes native prepared statements | Parameter binding verified; does not eliminate application logic authorization flaws | VERIFIED_BY_INSPECTION |
| `CLM-03` | Steady-state arrival throughput meets scenario target (200 req/s) within 50ms p95 latency budget | E07 | `labs/foundations/m23/activity_l23_01.py` | Open arrival rate <= 200 req/s; CPU cores unthrottled | Valid for tested concurrency on host hardware; not a universal cloud scale guarantee | EMPIRICALLY_MEASURED |
| `CLM-04` | Disk capacity consumption remains bounded under 30-day retention and regular vacuuming | E08 | `labs/foundations/m23/fermi_cost.py` | Mutation rate <= 10,000 writes/day; retention active | Requires cron vacuum; unbounded disk growth if retention script fails | BOUNDED_BY_MODEL |
| `CLM-05` | Additive schema migrations permit safe, immediate application code rollback | E12 | `labs/foundations/m24/preship_validator.py` | New columns are nullable or provide defaults | Applies to additive schema changes; destructive drops require roll-forward | VERIFIED_BY_SIMULATION |

---

## 16 Core Architectural Traces

### 1. Request Trace
- *Entry Point*: Client issues an HTTP POST `/api/v1/documents` to loopback IP `127.0.0.1:8080`. The OS kernel delivers the TCP SYN, completes the 3-way handshake (M10), and places the connection into the socket accept queue.
- *Transport & Framing*: The application worker accepts the connection and reads raw bytes. The HTTP parser validates RFC 9110 compliant request framing, headers, and Content-Length (M11).
- *Handler Routing*: The router matches `/api/v1/documents`, extracts the Authorization bearer token, calls authentication middleware, and dispatches to `handle_create_document`.
- *Execution & Response*: The handler parses JSON, binds parameters into a prepared SQL INSERT, commits via SQLite WAL (M14), serializes the created document ID to JSON, writes the 201 Created response to the socket, and returns the worker thread to the pool.

### 2. Data & State Trace
- *Ingress*: Raw request payload bytes are copied from socket kernel buffers into user-space memory via `recv()`. The JSON deserializer creates transient Python dictionary structures.
- *Buffer & Cache*: Document attributes are mapped to SQLite internal page buffers in user memory. Modified pages are marked dirty in the SQLite cache.
- *Disk Persistence*: SQLite appends transaction frames to the Write-Ahead Log (`app.db-wal`). Upon commit, SQLite calls `fsync()` on the WAL file descriptor to ensure non-volatile disk persistence before returning success.
- *Egress*: Query reads consult the WAL index shared memory (`app.db-shm`) to read recent uncheckpointed frames, format JSON, and stream response chunks through the TCP send buffer.

### 3. Control & Authority Trace
- *Call Graph*: HTTP listener loop → Dispatcher → AuthMiddleware → DocumentController → DatabaseLayer → SQLite C-API binding.
- *Identity Verification*: AuthMiddleware extracts the `Authorization: Bearer <token>` header, verifies the HMAC-SHA256 signature using `secrets.compare_digest`, and checks that the expiration timestamp has not elapsed.
- *Authorization Decision*: The handler verifies that the authenticated user subject owns the target tenant or document folder; unauthenticated or unauthorized requests fail closed immediately with HTTP 401 or 403 without touching storage.
- *Privilege Boundaries*: The application process runs as a standard unprivileged user without root capabilities, isolated within its designated working directory.

### 4. State Inventory
- *Volatile State*: In-memory LRU query cache (16MB max), connection pool handles, and ephemeral socket buffers. Lost cleanly upon process termination.
- *Durable State*: Primary SQLite database (`app.db`), Write-Ahead Log (`app.db-wal`), and uploaded user assets stored in `./data/uploads/`.
- *Replicated State*: NONE. This system is explicitly a single-node architecture; zero replicated state is present or claimed.
- *Configuration State*: Environment variables (`APP_PORT`, `DB_PATH`, `JWT_SECRET`) loaded read-only at process startup.

### 5. Invariants & Specifications
- *Data Integrity Invariants*: Document IDs are unique 64-bit monotonically increasing integers; document title is non-empty; foreign keys enforced via `PRAGMA foreign_keys = ON`.
- *Concurrency Invariants*: SQLite configured in WAL mode (`PRAGMA journal_mode = WAL`); multiple concurrent readers never block a single writer, and writer never blocks readers.
- *Security Invariants*: Passwords hashed with PBKDF2-HMAC-SHA256 (100,000 iterations); session tokens expire in exactly 3600 seconds; zero plaintext secrets in storage.
- *Liveness & Safety Specs*: HTTP read/write socket timeouts set to 5.0 seconds; database busy timeout set to 5000ms to prevent instant transaction aborts under brief write concurrency.

### 6. Trust Boundaries
- *Network Perimeter*: Boundary separating public client networks from the localhost loopback adapter; external traffic must pass through a reverse proxy terminating TLS 1.3 (M11/M21).
- *Process Perimeter*: Boundary separating the Python application runtime from the host operating system kernel and filesystem permissions.
- *Authority Crossing*: Untrusted HTTP request bodies pass through a strict JSON schema validator before parameters are extracted; ambient authority is rejected.
- *Residual Perimeter Risk*: Physical or root compromise of the host server compromises the local database file; mitigation is OS-level disk encryption.

### 7. Isolation Boundaries
- *Memory Isolation*: OS virtual memory management (M07) isolates application heap and stack from other host processes.
- *Filesystem Confinement*: Application file access is restricted using `os.path.commonpath` and `Path.resolve` (M21) to prevent directory traversal attacks outside `./data/`.
- *Transaction Isolation*: SQLite transactions execute under Read Committed / Serialized write isolation; uncommitted dirty frames remain isolated inside the WAL.
- *Tenant Isolation*: Every database query enforces explicit `WHERE tenant_id = ?` scoping to maintain logical multi-tenant isolation.

### 8. Failure & Risk Walkthrough
- *Process Crash (`kill -9`)*: Process halts abruptly. Upon restart, SQLite opens `app.db` and `app.db-wal`, detects uncheckpointed valid frames, rolls back incomplete transactions, and restores consistency.
- *Sudden Power Loss*: OS buffer cache dropped. Because SQLite committed transactions called `fsync()` on WAL, committed data is intact; uncommitted transactions are discarded without database corruption.
- *Disk Full (ENOSPC)*: SQLite throws `sqlite3.OperationalError: disk I/O error`. The application catches the exception, logs an alert, rejects incoming writes with 503, but continues serving reads from memory/disk.
- *Downstream Timeout*: Slow client connections are terminated after 5.0s by socket timeout, preventing worker thread exhaustion.

### 9. Security & Privacy Decisions
- *Cryptographic Primitives*: Uses Python standard library `hashlib`, `hmac`, and `secrets`. Uses `hmac.compare_digest` to prevent timing attacks.
- *Injection Mitigations*: All SQL queries use DB-API 2.0 parameterized placeholders (`?`). String interpolation (`%` or f-strings) in SQL queries is banned by static linting.
- *Transport Protection*: TLS 1.3 with forward secrecy; secure cookie flags `HttpOnly; Secure; SameSite=Strict`.
- *Privacy & Logging*: Passwords, bearer tokens, and session keys are explicitly stripped before emitting structured JSON logs.

### 10. Measurements & Performance Evidence
- *Experiment Design*: Benchmarked steady-state response latency under open-arrival scheduling to avoid coordinated omission (M23).
- *Arrival Workload Model*: Synthetic open arrival at 200 req/s with Poisson inter-arrival intervals over 10 minutes.
- *Latency Distribution*:
  - Min: 1.8 ms
  - p50: 4.2 ms
  - p90: 12.5 ms
  - p95: 22.1 ms
  - p99: 44.8 ms
  - Max: 68.3 ms
- *Hardware & Measurement Limits*: Measured on 4-core x86-64 host using `time.monotonic_ns()`. Valid for local single-node; does not predict behavior over transatlantic network hops.

### 11. Cost & Scale Estimates
- *Compute Sizing*: At 200 req/s with 4.2ms median CPU time, required CPU core capacity is $200 \times 0.0042 = 0.84$ cores. A 2-core host provides >2x headroom.
- *Memory Footprint*: Baseline process RSS is 38 MB; 16 MB SQLite cache + 50 MB connection buffers yields a steady-state footprint of ~105 MB RAM.
- *Storage Capacity*: 10,000 documents/day @ 2 KB/doc = 20 MB/day. With 30-day retention and indexes, steady-state storage is bounded under 1.5 GB.
- *Network Egress*: 200 req/s @ 1.5 KB average response = 300 KB/s = 2.4 Mbps outbound. Monthly egress ~780 GB ($70/mo at standard cloud pricing).

### 12. Alternatives Considered
- *Evaluated Frameworks/DBs*: Compared SQLite WAL vs PostgreSQL 16 (D-015 framework).
- *Decision Factors*: Evaluated operational burden, memory overhead, latency, and single-node simplicity.
- *Outcome*: Selected SQLite WAL for single-instance simplicity, sub-millisecond local in-process queries, and zero background daemon maintenance.

### 13. When-Not-To-Use & Rejected Choices
- *Rejected Technology 1*: Rejected Redis distributed caching. In-process LRU cache satisfies read latency without introducing network hops or cache-invalidation bugs.
- *Rejected Technology 2*: Rejected Apache Kafka message queue. The single-node system has no distributed consumer groups; an in-memory queue or SQLite outbox is sufficient.
- *Rejected Architecture*: Rejected microservices. Decomposition into 5 services would multiply operational complexity by 10x with zero scaling benefit at 200 req/s.
- *Reconsideration Threshold*: We will reconsider PostgreSQL and Redis if write concurrency exceeds 1,500 writes/sec or multi-node redundancy becomes a hard requirement.

### 14. Explicit Unknowns
- *Technical Blind Spot 1*: SQLite query planner performance when table rows exceed 10,000,000 records under low available RAM (untested paging degradation).
- *Technical Blind Spot 2*: Long-tail latency distribution when host filesystem executes a background TRIM operation on SSD under heavy concurrent write load.
- *Boundary Acknowledgment*: These two areas are acknowledged uncertainties where empirical measurements have not yet been performed.

### 15. Learning Plan
- *Investigation Action 1*: Write a synthetic generation script to populate 10M rows in a scratch database and benchmark VDBE B-Tree traversal times across varied RAM cache limits.
- *Investigation Action 2*: Set up an isolated Linux test fixture, trigger manual `fstrim` during a continuous 200 req/s write test, and record latency percentiles.
- *Reporting Milestone*: Results will be documented in the M25 systems evaluation log before major version release.

### 16. Changed-Constraint Adaptation
- *Assigned Scenario Card*: `SCENARIO_01_HIGH_LATENCY` (Client network RTT jumps from 1ms to 200ms with 1% packet loss).
- *Broken Invariants / Bottlenecks*: In the baseline design, synchronous request-response over persistent TCP connections causes HTTP worker threads to remain blocked waiting for network ACK packets. Under 200ms RTT, a 50-thread worker pool saturates at only $50 / 0.200 = 250$ active requests, leading to connection refusals.
- *Sound Architectural Adaptation*:
  1. Decouple connection termination from request processing by placing a non-blocking reverse proxy in front of the application to buffer slow network client writes (M11/M19).
  2. Enable HTTP/2 multiplexing on the reverse proxy to eliminate connection-per-request overhead over high-latency links.
  3. Increase socket keep-alive idle timeouts and tune TCP receive window sizes.
- *New Evidence Needed*: Re-run arrival-scheduled latency benchmark through a network traffic control emulator (`tc netem delay 200ms`) and confirm throughput does not collapse.

---

## 12-Evidence-Area Traceability Matrix

| Area ID | Evidence Area Name | Primary Claim ID(s) | Primary Artifact Reference | Evidence Sufficiency Summary |
| :--- | :--- | :--- | :--- | :--- |
| E01 | End-to-End Request Flow | CLM-01, CLM-03 | `Trace 1; app/server.py` | Complete unbroken trace from socket to disk and back |
| E02 | State & Data Lifecycle | CLM-01, CLM-04 | `Trace 2; app/db.py` | Volatile memory vs WAL vs persistent disk clearly separated |
| E03 | Core Invariants & Specs | CLM-01, CLM-02 | `Trace 5; schema.sql` | ACID WAL invariants and relational constraints documented |
| E04 | Trust & Isolation Boundaries | CLM-02 | `Trace 6, 7; app/auth.py` | Path confinement and ambient authority rejection verified |
| E05 | Failure Domains & Resilience | CLM-01 | `Trace 8; labs/foundations/m09` | Process crash recovery verified; single-node limits stated |
| E06 | Transport & App Security | CLM-02 | `Trace 9; app/auth.py` | Parameterized SQL and HMAC token verification verified |
| E07 | Empirical Measurement | CLM-03 | `Trace 10; labs/foundations/m23` | Open arrival schedule with p50/p90/p99 latency distribution |
| E08 | Capacity & Cost Models | CLM-04 | `Trace 11; fermi_cost.py` | Napkin math CPU/RAM/disk sizing with explicit units |
| E09 | Trade-Off & Alternative Analysis | CLM-01, CLM-03 | `Trace 12, 13; D-015 card` | SQLite vs PostgreSQL/Redis trade-off with rejected options |
| E10 | Explicit Unknowns & Limits | CLM-03, CLM-04 | `Trace 14, 15` | Documented 10M-row memory limit and SSD TRIM unknowns |
| E11 | Changed-Constraint Adaptation | CLM-03 | `Trace 16` | Coherent response to 200ms WAN latency challenge |
| E12 | Pre-Ship Operational Readiness | CLM-05 | `labs/foundations/m24/sample_preship.json` | Risk-prioritized matrix and migration compatibility verified |

---

## Reviewer Judgment

> **Note**: Final evaluation is exclusively completed by the technical reviewer / Web Lead.

- Reviewer Identity: `[Unfilled / Reviewer will complete]`
- Review Date: `[Unfilled / Reviewer will complete]`
- Evaluation Disposition: `[Unfilled / Reviewer selects PASS / REVISE / FAIL / BLOCKED / NOT RUN]`
- Architectural Defense Feedback:
  - 16-Trace Quality & Causality: `[Unfilled / Reviewer evaluation]`
  - Evidence Sufficiency: `[Unfilled / Reviewer evaluation]`
  - Changed-Constraint Coherence: `[Unfilled / Reviewer evaluation]`
  - Pre-Ship Risk Prioritization & Recovery: `[Unfilled / Reviewer evaluation]`
- Mandatory Revision Items (if REVISE): `[Unfilled / Reviewer notes]`
