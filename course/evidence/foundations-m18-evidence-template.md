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
- OQ-BP-006 Environment Policy Status: `CLOSED (technical environment-definition/realization per #167; #158 re-check still required)`

---

## B — Delegation & Delivery Contract

- Scenario ID: `<actual course scenario ID>`
- Queue / Log Abstraction Evaluated: `<actual abstraction used in the scenario>`
- Ordering Scope Named: `<actual ordering scope, if any>`
- Delivery Label Contract: `<actual named delivery/effect contract>`
- Retry / Redelivery Assumptions:
  `<Learner specifies when and why messages are redelivered under this contract>`
- Exact Inference Limit:
  `<Learner explains why a broker delivery label does NOT equal an arbitrary external business-effect guarantee>`

---

## C — Broken Dual-Write Divergence

- Local Database Transaction State: `<actual observed transaction state>`
- Scripted Failure Point: `<actual course failure point exercised>`
- Delivery Buffer / Queue State: `<actual observed delivery-buffer state>`
- Observed State Divergence:
  `<Learner records whether business row exists while queue delivery action is missing>`
- Invariant Judgment:
  `<Learner explains what this failure window proves about uncoordinated multi-system writes, and what it does NOT prove>`

---

## D — Transactional Outbox Atomic Staging

- Local SQLite Transaction Boundary: `BEGIN IMMEDIATE ... COMMIT`
- Orders Table Row State: `<RECORDED_ROW_STATE>`
- Outbox Events Table Row State: `<RECORDED_ROW_STATE>`
- Atomic Commit Disposition: `<actual observed commit/rollback disposition>`
- Exact Atomicity Scope:
  `<Learner explains why the outbox table MUST reside in the exact same SQLite database as the business entities>`

---

## E — Relay Retry & Duplicate Delivery

- Outbox Event ID: `<actual recorded event ID>`
- First Delivery State to Worker: `<actual observed first-attempt state>`
- Scripted Relay Failure Point: `<actual course relay failure point exercised>`
- Outbox `dispatched` Flag After Failure: `<actual recorded value>`
- Observed Redelivery Count on Retry: `<actual count>`
- Final Outbox `dispatched` Flag: `<actual recorded value>`
- Inference Boundary:
  `<Learner explains why this fixture's deliver-before-mark + retry policy permits/produces redelivery, without generalizing it to every at-least-once implementation>`

---

## F — Scoped Duplicate-Safe Worker Deduplication

- Message / Event ID: `<actual message ID>`
- Total Delivery Attempts Recorded: `<actual count>`
- Duplicate Suppressions Recorded: `<actual count>`
- `processed_events` Claim State: `<RECORDED_CLAIM_STATE>`
- Selected Consumer Effect State (`fulfillments` table): `<RECORDED_FULFILLMENT_STATE>`
- Exact One-Transaction Boundary:
  `<Learner explains why claim in processed_events and fulfillment update must happen in ONE SQLite transaction>`
- Duplicate Conflict Path Followed: `<actual conflict/dedup path observed>`
- Exact Guarantee Scope:
  `<Learner defines what duplicate safety is proved here, and why it cannot be called arbitrary end-to-end exactly-once>`

---

## G — Event Log vs. Event Sourcing

- Conceptual Distinction:
  `<Learner explains the difference between an Event Log (storage/messaging structure) and Event Sourcing (architectural pattern)>`
- Is Current M18 Outbox Fixture Event-Sourced? `<learner records judgment from the actual fixture>`
- Mechanical Reason:
  `<Learner justifies whether system state is derived exclusively from replaying events, or stored in mutable tables>`

---

## H — Classic Two-Phase Commit (2PC) Uncertainty

- Coordinator Logged Decision: `<actual recorded coordinator state/decision>`
- Participant Name Evaluated: `<participant name>`
- Participant State under Silence: `<actual recorded participant state>`
- Participant Vote Cast: `<actual vote in the exercised trace>`
- Decision Known to Participant: `<actual participant knowledge state in the trace>`
- Can Unilaterally Commit: `<actual trace result>`
- Can Unilaterally Abort: `<actual trace result>`
- Disposition & Blocking Reason:
  `<Learner explains why this PREPARED/decision-unknown trace cannot choose COMMIT or ABORT from silence alone, and records what recovery/termination information is needed>`
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
    `<Learner explains that the observed state came from already-applied local Saga steps and demonstrates lack of workflow-wide isolation; do not call it a database dirty read unless an uncommitted DB transaction was actually read>`
- Semantic Forward Recovery vs. Physical Rollback:
  `<Learner explains why compensation does not erase time or historical visibility>`

---

## J — Distributed Leases & Storage Fencing Tokens

- Initial Lease Holder & Token: `<holder name, token number>`
- Scripted Client Event: `<actual course client pause/stall scenario>`
- Lease Expiry Disposition: `<actual logical lease state>`
- Newer Lease Holder & Token: `<holder name, token number>`
- Storage `highest_token` Before Stale Write: `<token number>`
- Stale Holder Write Attempt Token: `<token number>`
- Storage Action Recorded: `<actual resource action>`
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
  - `<current product/spec sources actually inspected; include Kafka/SQS only if used>`
