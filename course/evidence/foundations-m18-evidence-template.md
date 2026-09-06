# Foundations M18 Evidence Template — Distributed State & Coordination

Use this template for **one actual learner observation**. Do not prefill or copy another learner's timestamps, event IDs, retry counts, token numbers, vote dispositions, compensation steps, or test pass markers.

---

## A — Environment Capabilities & Execution Ref

- Execution commit / ref: `<actual HEAD commit SHA>`
- Host Operating System: `<actual OS and architecture>`
- Python Implementation & Version: `<actual Python version>`
- Embedded SQLite Library Version: `<actual sqlite3.sqlite_version>`
- Local Writable Scratch Capability: `<PASS / FAIL / BLOCKED>`
- Preflight Distributed Infra M18 Status: `<READY / BLOCKED>`
- OQ-BP-006 Environment Policy Status: `OPEN / UNRESOLVED`

---

## B — Delegation & Delivery Contract

- Scenario ID: `<actual course scenario ID>`
- Queue / Log Abstraction Evaluated: `<WORK_QUEUE_COMPETING_CONSUMERS / PARTITIONED_EVENT_LOG>`
- Ordering Scope Named: `<QUEUE_FIFO / PARTITION_KEY_ORDER / NONE / OTHER>`
- Delivery Label Contract: `<AT_MOST_ONCE / AT_LEAST_ONCE / EXACTLY_ONCE_SCOPED>`
- Retry / Redelivery Assumptions:
  `<Learner specifies when and why messages are redelivered under this contract>`
- Exact Inference Limit:
  `<Learner explains why a broker delivery label does NOT equal an arbitrary external business-effect guarantee>`

---

## C — Broken Dual-Write Divergence

- Local Database Transaction State: `<COMMITTED / ROLLED_BACK / NONE>`
- Scripted Failure Point: `<POST_DB_COMMIT_PRE_QUEUE_ENQUEUE>`
- Delivery Buffer / Queue State: `<EMPTY / ENQUEUED>`
- Observed State Divergence:
  `<Learner records whether business row exists while queue delivery action is missing>`
- Invariant Judgment:
  `<Learner explains what this failure window proves about uncoordinated multi-system writes, and what it does NOT prove>`

---

## D — Transactional Outbox Atomic Staging

- Local SQLite Transaction Boundary: `BEGIN IMMEDIATE ... COMMIT`
- Orders Table Row State: `<RECORDED_ROW_STATE>`
- Outbox Events Table Row State: `<RECORDED_ROW_STATE>`
- Atomic Commit Disposition: `<COMMITTED_TOGETHER / FAILED>`
- Exact Atomicity Scope:
  `<Learner explains why the outbox table MUST reside in the exact same SQLite database as the business entities>`

---

## E — Relay Retry & Duplicate Delivery

- Outbox Event ID: `<actual recorded event ID>`
- First Delivery State to Worker: `<DELIVERED / FAILED>`
- Scripted Relay Failure Point: `<POST_WORKER_DELIVERY_PRE_DISPATCH_MARK>`
- Outbox `dispatched` Flag After Crash: `<0 / 1>`
- Observed Redelivery Count on Retry: `<actual count>`
- Final Outbox `dispatched` Flag: `<0 / 1>`
- Inference Boundary:
  `<Learner explains why at-least-once delivery is an inevitable consequence of deliver-before-mark crash recovery>`

---

## F — Scoped Duplicate-Safe Worker Deduplication

- Message / Event ID: `<actual message ID>`
- Total Delivery Attempts Recorded: `<actual count>`
- Duplicate Suppressions Recorded: `<actual count>`
- `processed_events` Claim State: `<RECORDED_CLAIM_STATE>`
- Selected Consumer Effect State (`fulfillments` table): `<RECORDED_FULFILLMENT_STATE>`
- Exact One-Transaction Boundary:
  `<Learner explains why claim in processed_events and fulfillment update must happen in ONE SQLite transaction>`
- Duplicate Conflict Path Followed: `<EXISTING_KEY_CHECK / INTEGRITY_CONFLICT>`
- Exact Guarantee Scope:
  `<Learner defines what duplicate safety is proved here, and why it cannot be called arbitrary end-to-end exactly-once>`

---

## G — Event Log vs. Event Sourcing

- Conceptual Distinction:
  `<Learner explains the difference between an Event Log (storage/messaging structure) and Event Sourcing (architectural pattern)>`
- Is Current M18 Outbox Fixture Event-Sourced? `<YES / NO>`
- Mechanical Reason:
  `<Learner justifies whether system state is derived exclusively from replaying events, or stored in mutable tables>`

---

## H — Classic Two-Phase Commit (2PC) Uncertainty

- Coordinator Logged Decision: `<COMMIT / ABORT / NONE>`
- Participant Name Evaluated: `<participant name>`
- Participant State under Silence: `<PREPARED / COMMITTED / ABORTED>`
- Participant Vote Cast: `<YES / NO>`
- Decision Known to Participant: `<TRUE / FALSE>`
- Can Unilaterally Commit: `<TRUE / FALSE>`
- Can Unilaterally Abort: `<TRUE / FALSE>`
- Disposition & Blocking Reason:
  `<Learner explains why a prepared participant cannot guess the outcome and must block>`
- Contrast Case (Vote NO):
  `<Learner records whether a participant that voted NO can abort unilaterally, proving not every coordinator crash blocks everyone forever>`
- Recovery Information Needed to Terminate:
  `<Learner identifies coordinator recovery log or cooperative participant termination protocol>`

---

## I — Saga Pattern: Compensations & Isolation Anomaly

- Configured Scenario Steps: `<Step 1 -> Step 2 -> Step 3>`
- Completed Forward Steps: `<actual completed steps>`
- Injected Failure Step: `<actual failed step>`
- Triggered Compensation Chain: `<actual compensation steps executed in order>`
- Final State of Business Entities: `<final orders, inventory, and payment states>`
- Intermediate State Observed by Concurrent Reader:
  - Checkpoint: `<checkpoint name>`
  - Intermediate Observation: `<actual inventory/order state observed>`
  - Isolation Anomaly Identified:
    `<Learner explains why concurrent observation of intermediate uncommitted state violates Isolation (I in ACID)>`
- Semantic Forward Recovery vs. Physical Rollback:
  `<Learner explains why compensation does not erase time or historical visibility>`

---

## J — Distributed Leases & Storage Fencing Tokens

- Initial Lease Holder & Token: `<holder name, token number>`
- Scripted Client Event: `<GC_PAUSE / NETWORK_STALL>`
- Lease Expiry Disposition: `<EXPIRED_IN_LOCK_SERVICE>`
- Newer Lease Holder & Token: `<holder name, token number>`
- Storage `highest_token` Before Stale Write: `<token number>`
- Stale Holder Write Attempt Token: `<token number>`
- Storage Action Recorded: `<ACCEPT_WRITE / REJECT_STALE_WRITE>`
- Invariant Evaluated: `presented_token < highest_token => REJECT`
- Resource-Boundary Inference Limit:
  `<Learner explains why fencing tokens require validation at the protected resource boundary, and why fencing is one mitigation pattern rather than the only valid lock design>`

---

## K — Cleanup, Concepts, Competencies, Visuals & Currentness

- Scratch Directory Cleaned: `<PASS / FAIL>`
- Double-Reset Verification: `<PASS / FAIL>`
- Concept Revisits Verified:
  - `EC-CON-010 Failure`
  - `EC-CON-009 Correctness`
  - `EC-CON-014 Consistency`
  - `EC-CON-006 Trade-off`
  - `EC-CON-015 Concurrency`
- Competencies Demonstrated:
  - `Judge`: `<Learner reflection on architecture selection>`
  - `Explain`: `<Learner reflection on mechanisms & trade-offs>`
  - `Trace`: `<Learner reflection on outbox & 2PC execution flow>`
  - `Correctness`: `<Learner reflection on deduplication & fencing invariants>`
- Visual References Checked:
  - `FIG-M18-01` (Dual-Write Failure vs. Transactional Outbox)
  - `FIG-M18-02` (2PC vs. Saga & Fencing Tokens)
- Source / Currentness Audit:
  - Gray (1978) 2PC
  - Garcia-Molina & Salem (1987) Sagas
  - Kleppmann (2016) Fencing Tokens
  - Current Broker Delivery Semantics (Kafka, SQS FIFO, AMQP/JMS)
