# Foundations M16 Evidence Template — Distributed Systems Foundations: Partial Failure & RPC

Use this template for **one actual learner observation**. Do not prefill or copy another learner's timeout duration, retry count, port, PID/thread ordering, errno/exception text, backoff delay, number of duplicate attempts, final counter value, idempotency key, SQLite version, or test pass markers.

---

## A — Environment Capabilities

- Execution commit / ref: `<actual HEAD commit SHA>`
- Host Operating System: `<actual OS>`
- Kernel / OS Release: `<actual release / kernel version>`
- Architecture: `<actual CPU architecture>`
- Python Implementation & Version: `<actual Python implementation and version>`
- SQLite Library Version: `<actual sqlite3.sqlite_version>`
- Localhost Ephemeral Port Bind Capability (`127.0.0.1:0`): `<PASS / FAIL / BLOCKED>`
- Course-owned / Writable Temp Directory Capability: `<PASS / FAIL / BLOCKED>`
- Subprocess Watchdog / Reaping Capability: `<PASS / FAIL / BLOCKED>`
- OQ-BP-006 Environment Policy Status: `OPEN / UNRESOLVED`

---

## B — L16-01 Partial-Failure & No-Response Ambiguity Observation

- Request ID: `<actual request ID observed>`
- Localhost Ephemeral Port Bound: `<actual ephemeral port assigned>`
- Configured Client Deadline / Timeout: `<actual configured timeout, e.g. in seconds or ms>`
- Scripted Application-Layer Fault Action: `<actual fault action configured on FaultShim>`
- Client Observed Outcome / Exception: `<actual exception type, e.g. TimeoutError>`
- Client Stopped Waiting Timestamp: `<actual timestamp>`
- Server Execution Completion Timestamp: `<actual timestamp>`
- Server Request ID Completed: `<actual request ID logged by server>`
- Identical Request ID Confirmed: `<YES / NO>`
- Temporal Ordering Relation: `<Learner notes comparing client stopped waiting time vs server completion time>`
- Observed Inference: `<Learner notes explaining that client-side timeout did not stop or undo server execution>`

---

## C — Transport vs. Application vs. Durability Distinction

- What Observed Socket / Transport State Proves:
  `<Learner notes on what TCP connection establishment / byte receipt actually proves>`
- What Observed Socket / Transport State Does NOT Prove:
  `<Learner notes explaining why transport ACK does not prove application processing or durable commitment>`
- Application Fault Shim vs. Literal Packet Loss:
  `<Learner explicitly records the boundary: simulated delay/suppression is in user-space application logic, not physical cable cut or raw packet sniff>`

---

## D — Retry Policy & Amplification Reasoning

- Configured Total-Attempt Budget: `<actual attempt bound, e.g. 1, 2, 3>`
- Actual Dispatched Attempts: `<actual number of attempts made>`
- Retry Policy Name: `<NO_RETRY / DETERMINISTIC / EXPONENTIAL_JITTER>`
- Actual Backoff / Sleep Values Applied: `<actual backoff durations in ms>`
- Total-Attempt Bound Strictly Enforced: `<YES / NO>`
- Retry Amplification Reasoning:
  `<Learner calculates downstream request multiplication across call tree (A -> B -> C -> D) under stated assumptions and explains why unbounded retries cause cascading collapse>`
- Policy Choice vs. Universal Law:
  `<Learner notes that exponential backoff with jitter is an architectural policy option, not a natural law>`

---

## E — Unsafe Duplicate Path (No Idempotency Key)

- Logical Operation Dispatched: `<e.g. unsafe_increment>`
- Client Dispatched Attempts: `<actual number of attempts dispatched>`
- Server Business-Execution Count: `<actual executions logged by server>`
- Initial Counter State: `<actual initial value>`
- Final Counter State: `<actual final value>`
- Duplicate Side-Effect Manifested: `<YES / NO>`
- Observation Summary:
  `<Learner explains why silence caused repeated mutations on non-idempotent endpoint>`

---

## F — Protected Idempotency Path (With Idempotency Key)

- Idempotency Key: `<actual idempotency key string>`
- Client Dispatched Attempts: `<actual number of attempts dispatched>`
- Recorded Server Business-Executions: `<actual number of executions, e.g. 1>`
- Initial Counter State: `<actual initial value>`
- Final Counter State: `<actual final value>`
- Duplicate Invariant Preserved ($f(f(x)) = f(x)$): `<YES / NO>`
- Atomic Transaction Boundary:
  `<Learner describes SQLite BEGIN IMMEDIATE transaction enclosing key claim and business mutation>`
- Duplicate Request Disposition:
  `<Learner explains whether server returned cached response or handled conflict>`
- Exact Scope of the Guarantee:
  `<Learner states the boundary: proven within the local SQLite transaction, NOT across arbitrary uncoordinated external systems>`

---

## G — Deduplication Retention & Eviction Horizon

- Configured Retention Horizon / TTL: `<actual configured duration>`
- Key Purge Action: `IdempotencyStore.purge_expired()`
- Eviction Outcome Observed: `<Learner notes whether expired entry was purged>`
- Re-execution After Eviction:
  `<Learner observes whether late retry arriving after retention window executes again>`
- Systems Trade-off:
  `<Learner notes the memory/storage trade-off of maintaining deduplication history>`

---

## H — Cleanup & Safety Verification

- Localhost Ephemeral Server Sockets Closed: `<YES / NO>`
- All Server & Client Threads Joined (No Daemon Leak): `<YES / NO>`
- Temporary SQLite Database Files Removed (`.db`, `-journal`, `-wal`, `-shm`): `<YES / NO>`
- Reset Script Executed: `labs/foundations/m16/reset.py`
- Reset Idempotence (Passed Twice Without Error): `<YES / NO>`

---

## I — Concepts, Competencies, Visuals & Inference Limits

- Primary Competencies Exercised:
  - L16-01: `Judge`, `Explain`, `Trace`
  - L16-02: `Trace`, `Judge`, `Explain`
- Formal Canonical Concept Revisits Recorded:
  - L16-01: `EC-CON-010 Failure`, `EC-CON-002 Abstraction`, `EC-CON-018 Process`, `EC-CON-015 Concurrency`
  - L16-02: `EC-CON-005 Interface`, `EC-CON-008 Invariant`, `EC-CON-003 Representation`, `EC-CON-007 Specification`
- Visual Artifacts Inspected:
  - `FIG-M16-01`: The Four States of Remote Silence ("SILENCE DOES NOT REVEAL REMOTE STATE")
  - `FIG-M16-02`: Retry Amplification vs. Jittered Backoff & Idempotency
- LAB-OPT-02 (Stanford CS144 Checkpoint 2) Disposition:
  - Status: `<OPTIONAL / RIGHTS-GATED / LINK-ONLY / SKIPPED>`
  - Vendoring Audit: Zero external code or tests copied into Essential CS
- Provenance & Currentness Sources Rechecked:
  - RFC 9110 §9.2 (Idempotent Methods)
  - IETF `draft-ietf-httpapi-idempotency-key-header-07` (Expired Internet-Draft, reference pattern only)
  - AWS Architecture Blog: Marc Brooker (2015), Exponential Backoff And Jitter
- Exact Inference Limits Acknowledged:
  `<Learner acknowledges that local SQLite deduplication does not prove unbounded distributed exactly-once semantics, and that timeout is an erasure of waiting rather than remote cancellation>`
