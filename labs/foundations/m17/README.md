# M17 Foundations Activities: Replication, Consistency & Consensus

This directory contains executable, course-owned worked-trace harnesses and activities for Module M17.

## Core Boundary Rules

- **Zero distributed service daemons**: No background network services, brokers, or databases.
- **Zero listening ports**: No `socket.bind()` or external open network ports.
- **Zero Docker/cluster requirements**: Logical "nodes" are worksheet and state-machine data records.
- **No Raft or Paxos implementation**: Core focus is on the formal invariants, set-intersection arithmetic, voting restrictions, and real-time precedence orderings.

## Files Overview

1. **`trace_harness.py`** — Core Worked-Trace Harness
   - **Replication Acknowledgment**: Models course-owned `ASYNC`, configurable-threshold `SEMI_SYNC`, `SYNC_ALL`, and `QUORUM_W` acknowledgment scenarios. These are worksheet contracts, not universal product definitions; ack-point replica state and failover assumptions are explicit.
   - **Quorum Set-Intersection Validator**: Verifies Pigeonhole intersection $W + R > N \implies (W+R)-N \ge 1$; provides 3 formal counterexamples proving that **Overlap alone does NOT equal Linearizability or Latest-Value reads** (unversioned stale reads, ambiguous partial writes, and concurrent conflicting writes).
   - **Raft Election Safety Worksheet**: Models a logical 5-node partition ($2 \mid 3$); evaluates the Log Up-To-Date rule (§5.4.1); separates majority-set overlap from the vote/log/commit rules used by Raft safety reasoning; records the FLP boundary without implementing Raft.
   - **Consistency History Evaluator**: Exhaustively checks the small completed single-register histories used by this course against legal sequential register behavior plus real-time precedence. It also provides bounded numeric-version RYW/Monotonic-Read checks. It is a teaching validator, not a production general-purpose linearizability checker.

2. **`activity_l17_01.py`** — Replication Acknowledgment, Quorum Overlap & Overlap != Linearizability
   - Runs interactive demonstration of acknowledgment policies, failover durability, and the 3 quorum counterexamples.
   - Generates `.scratch/l17_01_observation.json`.

3. **`activity_l17_02.py`** — Consensus Invariants, Raft Log Up-To-Date & Partition Scenarios
   - Evaluates RequestVote decisions, majority elections under partition, and the FLP boundary.
   - Generates `.scratch/l17_02_observation.json`.

4. **`activity_l17_03.py`** — Linearizability, Session Guarantees & Real CAP Trade-off
   - Evaluates linearizable vs. non-linearizable histories, Read-Your-Writes, Monotonic Reads, and the three-way distinction between ACID Consistency, Transaction Isolation, and Replicated Linearizability.
   - Generates `.scratch/l17_03_observation.json`.

5. **`reset.py`** — Fail-closed, idempotent cleanup limited to course-owned `.scratch/` and local `__pycache__/`.

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
