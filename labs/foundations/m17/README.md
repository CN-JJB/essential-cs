# M17 Foundations Activities: Replication, Consistency & Consensus

This directory contains executable, course-owned worked-trace harnesses and activities for Module M17.

## Core Boundary Rules

- **Zero distributed service daemons**: No background network services, brokers, or databases.
- **Zero listening ports**: No `socket.bind()` or external open network ports.
- **Zero Docker/cluster requirements**: Logical "nodes" are worksheet and state-machine data records.
- **No Raft or Paxos implementation**: Core focus is on the formal invariants, set-intersection arithmetic, voting restrictions, and real-time precedence orderings.

## Files Overview

1. **`trace_harness.py`** — Core Worked-Trace Harness
   - **Replication Acknowledgment**: Models `ASYNC`, `SEMI_SYNC`, `SYNC_ALL`, and `QUORUM_W` acknowledgment semantics; models ambiguous write states (leader crash post-replication) and failover data loss.
   - **Quorum Set-Intersection Validator**: Verifies Pigeonhole intersection $W + R > N \implies (W+R)-N \ge 1$; provides 3 formal counterexamples proving that **Overlap alone does NOT equal Linearizability or Latest-Value reads** (unversioned stale reads, ambiguous partial writes, and concurrent conflicting writes).
   - **Raft Election Safety Worksheet**: Models logical 5-node cluster partition ($2 \mid 3$); evaluates the Log Up-To-Date voting rule (§5.4.1); enforces the boundary between majority overlap and full Leader Completeness; formalizes the FLP impossibility boundary.
   - **Consistency History Evaluator**: Classifies multi-client execution histories based on real-time invocation/response precedence ($op_1 <_{\text{real-time}} op_2 \iff \text{resp}(op_1) < \text{inv}(op_2)$); detects stale reads, Read-Your-Writes violations, and Monotonic Reads violations without using unsynchronized physical machine clocks.

2. **`activity_l17_01.py`** — Replication Acknowledgment, Quorum Overlap & Overlap != Linearizability
   - Runs interactive demonstration of acknowledgment policies, failover durability, and the 3 quorum counterexamples.
   - Generates `l17_01_observation.json`.

3. **`activity_l17_02.py`** — Consensus Invariants, Raft Log Up-To-Date & Partition Scenarios
   - Evaluates RequestVote decisions, majority elections under partition, and the FLP boundary.
   - Generates `l17_02_observation.json`.

4. **`activity_l17_03.py`** — Linearizability, Session Guarantees & Real CAP Trade-off
   - Evaluates linearizable vs. non-linearizable histories, Read-Your-Writes, Monotonic Reads, and the three-way distinction between ACID Consistency, Transaction Isolation, and Replicated Linearizability.
   - Generates `l17_03_observation.json`.

5. **`reset.py`** — Idempotent cleanup script removing generated JSON observations and temporary logs.

6. **`test_trace.py`** — Automated unit test suite verifying all 4 trace families and reset idempotence.

## Running the Activities

```bash
# Run each activity
python labs/foundations/m17/activity_l17_01.py
python labs/foundations/m17/activity_l17_02.py
python labs/foundations/m17/activity_l17_03.py

# Run unit tests
python -m unittest discover -s labs/foundations/m17 -p "test_*.py"

# Clean up temporary artifacts (idempotent, safe to run repeatedly)
python labs/foundations/m17/reset.py
```
