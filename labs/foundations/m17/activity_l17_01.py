#!/usr/bin/env python3
"""
labs/foundations/m17/activity_l17_01.py

Activity for Lesson L17-01:
Replication Acknowledgment Semantics, Quorum Intersections &
Why Overlap != Linearizability.

Demonstrates:
1. Synchronous vs. Asynchronous vs. Semi-Sync replication acknowledgment policies.
2. The ambiguous write case: leader crashed post-replication before returning ACK.
3. Failover data-loss analysis under async replication.
4. Quorum arithmetic: W + R > N (Pigeonhole set intersection).
5. Counterexamples proving Overlap Alone is NOT Linearizability or Latest Value:
   - Stale read under unversioned quorum read.
   - Ambiguous/partial write causing non-linearizable history.
   - Concurrent conflicting writes without a named version/order/conflict-resolution rule.
"""

import json
import os
import sys

# Add parent directory to path so we can import trace_harness
sys.path.insert(0, os.path.dirname(__file__))

from trace_harness import AckPolicy, QuorumValidator, ReplicationAckTrace


def run_activity() -> int:
    print("=" * 78)
    print(" Essential CS: L17-01 Replication Acknowledgment & Quorum Overlap Activity")
    print("=" * 78)

    # --------------------------------------------------------------------------
    # Part 1: Replication Acknowledgment Policies & Durability
    # --------------------------------------------------------------------------
    print("\n[PART 1] Replication Acknowledgment Semantics (N=3, Leader=node_1)")

    # 1. Async replication
    async_trace = ReplicationAckTrace.simulate_write(
        policy=AckPolicy.ASYNC,
        cluster_size=3,
        leader_id="node_1",
        unreachable_replicas={"node_2", "node_3"},  # All followers slow/unreachable
    )
    print(f" -> ASYNC (followers unreachable): client_acked={async_trace.client_acked}")
    failover_async = async_trace.evaluate_failover_loss("node_2")
    print(f"    Failover to un-replicated follower node_2: {failover_async['durability_verdict']}")

    # 2. Semi-sync replication
    semi_trace_ok = ReplicationAckTrace.simulate_write(
        policy=AckPolicy.SEMI_SYNC,
        cluster_size=3,
        leader_id="node_1",
        unreachable_replicas={"node_3"},  # 1 follower reachable (node_2)
    )
    print(f" -> SEMI-SYNC (node_2 reachable, node_3 down): client_acked={semi_trace_ok.client_acked}")
    failover_semi = semi_trace_ok.evaluate_failover_loss("node_2")
    print(f"    Failover to synced follower node_2: {failover_semi['durability_verdict']}")

    # 3. Semi-sync failure
    semi_trace_fail = ReplicationAckTrace.simulate_write(
        policy=AckPolicy.SEMI_SYNC,
        cluster_size=3,
        leader_id="node_1",
        unreachable_replicas={"node_2", "node_3"},  # zero followers reachable
    )
    print(f" -> SEMI-SYNC (all followers down): client_acked={semi_trace_fail.client_acked}, error={semi_trace_fail.ack_error}")

    # 4. Ambiguous write: leader crashed post-replication before returning ACK
    ambiguous_trace = ReplicationAckTrace.simulate_write(
        policy=AckPolicy.QUORUM_W,
        cluster_size=3,
        leader_id="node_1",
        unreachable_replicas=set(),
        crashed_after_write_leader=True,
        w_quorum=2,
    )
    print(f" -> AMBIGUOUS WRITE (Leader crashed post-replication): client_acked={ambiguous_trace.client_acked}, error={ambiguous_trace.ack_error}")
    print(f"    Replicas holding entry: {[k for k, v in ambiguous_trace.replicas.items() if v.log]}")

    # --------------------------------------------------------------------------
    # Part 2: Quorum Set-Intersection Validator
    # --------------------------------------------------------------------------
    print("\n[PART 2] Quorum Set Intersection (N=3, W=2, R=2)")
    qv = QuorumValidator(cluster_size=3, write_quorum=2, read_quorum=2)
    is_valid = qv.is_quorum_valid()
    min_overlap = qv.min_overlap_count()
    print(f" -> W + R > N check (2 + 2 > 3): {is_valid} (guaranteed min overlap = {min_overlap} node)")

    write_set = {"node_1", "node_2"}
    read_set = {"node_2", "node_3"}
    overlap_res = qv.evaluate_overlap(write_set, read_set)
    print(f"    Write Quorum: {overlap_res['write_set']}")
    print(f"    Read Quorum:  {overlap_res['read_set']}")
    print(f"    Intersection: {overlap_res['overlap_nodes']} (Overlap verified: {overlap_res['has_overlap']})")

    # --------------------------------------------------------------------------
    # Part 3: Why Overlap Alone != Linearizability (The 3 Proofs)
    # --------------------------------------------------------------------------
    print("\n[PART 3] Overlap != Linearizability (Essential Invariant Proofs)")

    # Counterexample 1: Stale read under unversioned quorum read
    ce1 = QuorumValidator.demonstrate_counterexample_unversioned_stale_read()
    print(f" -> Counterexample 1 (Unversioned Read):")
    print(f"    Overlap exists at {ce1['overlap']}, but blind read observed: {ce1['blind_first_response_value']}")
    print(f"    Versioned read required to get: {ce1['version_resolved_value']}")
    print(f"    Stale read manifested: {ce1['stale_read_manifested']}")

    # Counterexample 2: Ambiguous partial write causes non-linearizable history
    ce2 = QuorumValidator.demonstrate_counterexample_ambiguous_partial_write()
    print(f" -> Counterexample 2 (Ambiguous Partial Write):")
    print(f"    Reader 1 {ce2['reader_1_quorum']} observed: {ce2['reader_1_observed']}")
    print(f"    Later Reader 2 {ce2['reader_2_quorum']} observed: {ce2['reader_2_observed']}")
    print(f"    Later read returned older value than earlier read!")
    print(f"    Linearizability violated: {ce2['linearizability_violated']}")

    # Counterexample 3: Concurrent conflicting writes
    ce3 = QuorumValidator.demonstrate_counterexample_concurrent_conflicting_writes()
    print(f" -> Counterexample 3 (Concurrent Conflicting Writes):")
    print(f"    Client A wrote to {ce3['client_A_quorum']}, Client B wrote to {ce3['client_B_quorum']}")
    print(
        f"    Overlap node {ce3['overlap_node']} has conflicting arrival/order state; "
        "set overlap alone supplies no winner."
    )
    print(f"    Disjoint readers observation anomaly: {ce3['disjoint_readers_anomaly']}")

    # Save output summary for learner evidence
    out_dir = os.path.dirname(__file__)
    summary_path = os.path.join(out_dir, "l17_01_observation.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "async_failover": failover_async,
                "semi_sync_failover": failover_semi,
                "ambiguous_write": ambiguous_trace.ack_error,
                "quorum_overlap": overlap_res,
                "ce1_unversioned": ce1,
                "ce2_partial_write": ce2,
                "ce3_concurrent_writes": ce3,
            },
            f,
            indent=2,
        )

    print(f"\n[EVIDENCE] Observation recorded to {summary_path}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(run_activity())
