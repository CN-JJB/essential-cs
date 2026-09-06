# Foundations M17 Evidence Template — Replication, Consistency & Consensus

Use this template for **one actual learner observation**. Do not prefill or copy another learner's replica sets, vote dispositions, timestamps, overlap nodes, violating operation pairs, or test pass markers.

---

## A — Environment Capabilities & Execution Ref

- Execution commit / ref: `<actual HEAD commit SHA>`
- Host Operating System: `<actual OS and architecture>`
- Python Implementation & Version: `<actual Python version>`
- M17 Trace Fixture Version / File: `labs/foundations/m17/trace_harness.py`
- Local Writable Scratch Capability: `<PASS / FAIL / BLOCKED>`
- Preflight Distributed Infra M17 Status: `<READY / BLOCKED>`
- OQ-BP-006 Environment Policy Status: `OPEN / UNRESOLVED`

---

## B — Replication Acknowledgment Policy & Durability

- Evaluated Scenario ID: `<actual scenario ID, e.g. ASYNC_FAILOVER / SEMI_SYNC_CRASH>`
- Configured Acknowledgment Policy: `<ASYNC / SEMI_SYNC / SYNC_ALL / QUORUM_W>`
- Client Success Condition:
  `<Learner specifies when the client receives success under the policy>`
- Replica States at Acknowledgment Time:
  `<Learner records which replicas held the entry when the client was acknowledged>`
- Storage Assumptions: `<VOLATILE_RAM / DURABLE_DISK (fsync)>`
- Failure Model Evaluated: `<Leader crash / follower partition / network delay>`
- Observed Failover Durability Outcome:
  `<Learner records whether data was lost or preserved upon failover to new leader>`
- Learner Durability / Failover Judgment:
  `<Learner explains why replication does not automatically equal durability>`

---

## C — Quorum Overlap & Arithmetic Verification

- Cluster Size ($N$): `<actual replica count>`
- Write Quorum ($W$): `<actual write quorum size>`
- Read Quorum ($R$): `<actual read quorum size>`
- Inequality Verification: $(W + R) - N \ge 1$: `<actual inequality math calculation>`
- Actual Write Set ($S_W$): `<actual replica IDs written>`
- Actual Read Set ($S_R$): `<actual replica IDs read>`
- Observed Overlap Set ($S_W \cap S_R$): `<actual overlapping replica IDs>`
- Write Completion Rule Stated:
  `<Learner specifies what constitutes write completion in this scenario>`
- Version / Conflict Rule Stated:
  `<Learner specifies the version comparison or tie-breaking rule>`
- Overlap Alone vs. Latest-Value Conclusion:
  `<Learner explains why overlap set alone is insufficient without the version rule>`
- Inference Limit:
  `<Learner notes that N, W, R arithmetic proves set intersection, NOT linearizability or disk durability>`

---

## D — Ambiguous & Concurrent Writes

- Scenario Type: `<AMBIGUOUS_PARTIAL_WRITE / CONCURRENT_CONFLICTING_WRITES>`
- Operation Sequence Dispatched:
  `<Learner records the exact sequence of attempted writes and reads>`
- Which Write Completed / Remained Ambiguous:
  `<Learner identifies which write was acknowledged and which timed out or crashed mid-flight>`
- Observed Replica State Across Cluster:
  `<Learner records the value and version on each replica after the operations>`
- Conflict-Resolution Assumptions:
  `<Learner states what rule was used: Last-Write-Wins, Vector Clock, or Unresolved Anomaly>`
- Learner Invariant Judgment:
  `<Learner explains how an ambiguous write can cause successive reads to see values out of real-time order>`

---

## E — Bounded Raft Election & Safety Trace

- Cluster Topology & Partition Evaluated:
  - Minority Partition: `<nodes isolated in minority>`
  - Majority Partition: `<nodes reachable in majority>`
- Candidate Evaluated: `<candidate node ID>`
- Candidate Term & Log Metadata:
  - Candidate Term: `<candidate term>`
  - Candidate Last Log Term: `<last log term>`
  - Candidate Last Log Index: `<last log index>`
- Voter Evaluated: `<voter node ID>`
- Voter Current Term & Log Metadata:
  - Voter Current Term: `<voter term>`
  - Voter Last Log Term: `<voter last term>`
  - Voter Last Log Index: `<voter last index>`
- Log Up-To-Date Rule Check:
  $$\text{lastTerm}_{\text{cand}} > \text{lastTerm}_{\text{voter}} \lor (\text{lastTerm}_{\text{cand}} = \text{lastTerm}_{\text{voter}} \land \text{lastIndex}_{\text{cand}} \ge \text{lastIndex}_{\text{voter}})$$
  - Evaluation Result: `<TRUE / FALSE>`
- Vote Disposition: `<VOTE_GRANTED / DENIED (with specific rule cited)>`
- Majority Reachability Outcome:
  `<Learner records whether candidate obtained >= floor(N/2) + 1 votes>`
- Safety Conclusion:
  `<Learner verifies that Election Safety held (at most one leader per term)>`
- Boundary of Majority Overlap:
  `<Learner explains why majority overlap alone does NOT prove Leader Completeness without the Log Up-To-Date voting rule>`

---

## F — Safety vs. Liveness & The FLP Boundary

- Asynchronous Network Model Assumptions:
  `<Learner states message delay is unbounded and process execution speeds are arbitrary>`
- Crash Failure Assumption:
  `<Learner notes at least one unannounced crash-stop process failure is possible>`
- Safety Property Evaluated:
  `<Learner defines Agreement and Validity under Raft>`
- Liveness / Termination Condition:
  `<Learner states why deterministic termination cannot be guaranteed under asynchronous FLP>`
- Randomized Election Timeouts Disposition:
  `<Learner explains why randomized timeouts improve practical liveness under partial synchrony, but DO NOT formally refute or defeat FLP>`

---

## G — Consistency Histories & Real-Time Precedence

- Evaluated Trace ID: `<Trace 1 / Trace 2 / Trace 3 / Trace 4>`
- Operation Invocations & Responses:
  `<Learner records operation intervals: [inv_time, resp_time] on logical worksheet timeline>`
- Real-Time Precedence Evaluation:
  $$op_1 <_{\text{real-time}} op_2 \iff \text{resp}(op_1) < \text{inv}(op_2)$$
  - Precedence Relation Satisfied: `<YES / NO>`
- Classification Outcome:
  `<LINEARIZABLE / NON_LINEARIZABLE / RYW_VIOLATION / MONOTONIC_READS_VIOLATION>`
- Violating Operation Pair (if any):
  - Operation 1: `<op_id, type, value, interval>`
  - Operation 2: `<op_id, type, value, interval>`
  - Anomaly Reason: `<Learner explains why the observation violates the named guarantee>`
- Wall-Clock Clock-Skew Boundary:
  `<Learner acknowledges that physical machine clocks were NOT used as the ordering oracle>`

---

## H — CAP Trade-off Analysis

- Partition Scenario Evaluated: `<network partition separating client from majority or minority>`
- Named Request Path & Operation: `<Read or Write on specific partition side>`
- Behavior Under Consistency ($C$) Prioritization:
  `<Learner records system returning error or blocking request to preserve linearizability>`
- Behavior Under Availability ($A$) Prioritization:
  `<Learner records system returning local stale/conflicting data to guarantee non-error response>`
- Rejection of "Pick Any Two" Menu:
  `<Learner explicitly writes why P is an environmental fault to tolerate rather than an optional configuration choice>`

---

## I — EXP-05 MIT 6.033 Source Expedition Record

- Lecture 14 URL Inspected:
  `https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/8eb16d3628bbd77ee7e8471b9871ec09_MIT6_033S18lec14.pdf`
- Source Inspection Date: `<actual date>`
- Source Access Disposition: `<LIVE_SOURCE_ACCESSIBLE / OPTIONAL SOURCE RECHECK BLOCKED>`
- Primary-Backup State Tracking Note:
  `<Learner paraphrases primary/backup state from Lecture 14>`
- Failure Detection Ambiguity Note:
  `<Learner records why ping silence cannot distinguish crash from network partition>`
- View Server Coordination Role:
  `<Learner records how view number and primary ACK barrier prevent dual primary>`
- Comparison to Course M17 Raft Trace:
  `<Learner contrasts centralized View Server against decentralized majority quorum>`
- Stopping Point Verified:
  `<Learner confirms stopping at bounded reading card without external code compilation>`

---

## J — Cleanup, Concepts, Competencies, Visuals & Inference Limits

- Primary Competencies Exercised:
  - L17-01: `Judge`, `Explain`
  - L17-02: `Explain`, `Trace`, `Judge`
  - L17-03: `Judge`, `Explain`
- Formal Canonical Concept Revisits Recorded:
  - L17-01: `EC-CON-016 Durability`, `EC-CON-006 Trade-off`, `EC-CON-011 Caching`
  - L17-02: `Consensus` (Registry ID Deferred), `EC-CON-008 Invariant`, `EC-CON-009 Correctness`
  - L17-03: `EC-CON-014 Consistency`, `EC-CON-006 Trade-off`, `EC-CON-013 Isolation`
- Visual Artifacts Inspected:
  - `FIG-M17-01`: Quorum Overlap vs. Linearizability Boundary ("OVERLAP != LINEARIZABILITY")
  - `FIG-M17-02`: Consensus Safety vs. Liveness: Majority Overlap ($2 \mid 3$ partition)
  - `FIG-M17-03`: Linearizability vs. Eventual Consistency Trace Comparison
- Cleanup & Safety Verification:
  - Reset Script Executed: `labs/foundations/m17/reset.py`
  - Reset Idempotence Verified (Ran twice cleanly): `<YES / NO>`
  - Zero Distributed Service Daemons or Background Sockets: `<CONFIRMED>`
- Exact Inference Limits Acknowledged:
  `<Learner acknowledges that quorum overlap does not equal linearizability, that Raft safety does not collapse to majority alone, that randomized timeouts do not defeat FLP, and that CAP is a partition trade-off rather than a pick-two menu>`
