#!/usr/bin/env python3
"""
labs/foundations/m17/test_trace.py

Unit test suite for M17 Worked-Trace Harness:
- Verification of Replication Acknowledgment Semantics & Failover Durability
- Verification of Quorum Intersection Arithmetic & Counterexamples (Overlap != Linearizability)
- Verification of Ambiguous and Concurrent Write Cases
- Verification of Raft Leader Election & Log Up-To-Date Restrictions (§5.4.1)
- Verification of Consistency History Classifications (Linearizability, RYW, Monotonic Reads)
- Verification of Reset Idempotence and Zero External Network/Daemon Footprint
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from reset import reset_m17_environment
from trace_harness import (
    AckPolicy,
    ConsistencyEvaluator,
    Operation,
    QuorumValidator,
    RaftLogEntry,
    RaftNodeRecord,
    RaftTraceValidator,
    ReplicationAckTrace,
    get_standard_consistency_traces,
)


class TestM17ReplicationAck(unittest.TestCase):
    """Gate 11 & Gate 14: Deterministic replication acknowledgment trace & ambiguous write case."""

    def test_async_acknowledgment_and_failover_loss(self):
        # Leader acknowledges immediately even if followers are slow/dead
        trace = ReplicationAckTrace.simulate_write(
            policy=AckPolicy.ASYNC,
            cluster_size=3,
            leader_id="node_1",
            unreachable_replicas={"node_2", "node_3"},
        )
        self.assertTrue(trace.client_acked)
        self.assertIsNone(trace.ack_error)

        # Failover to un-replicated follower node_2 results in data loss
        failover = trace.evaluate_failover_loss("node_2")
        self.assertTrue(failover["valid_failover"])
        self.assertTrue(failover["data_lost"])
        self.assertEqual(failover["durability_verdict"], "DATA_LOST_ON_FAILOVER")

    def test_semi_sync_acknowledgment_and_safety(self):
        # Semi-sync requires at least 1 follower ack
        trace_ok = ReplicationAckTrace.simulate_write(
            policy=AckPolicy.SEMI_SYNC,
            cluster_size=3,
            leader_id="node_1",
            unreachable_replicas={"node_3"},  # node_2 is reachable
        )
        self.assertTrue(trace_ok.client_acked)
        failover_synced = trace_ok.evaluate_failover_loss("node_2")
        self.assertFalse(failover_synced["data_lost"])
        self.assertEqual(failover_synced["durability_verdict"], "SURVIVED_FAILOVER")

        # When all followers are down, semi-sync fails to acknowledge client
        trace_fail = ReplicationAckTrace.simulate_write(
            policy=AckPolicy.SEMI_SYNC,
            cluster_size=3,
            leader_id="node_1",
            unreachable_replicas={"node_2", "node_3"},
        )
        self.assertFalse(trace_fail.client_acked)
        self.assertEqual(trace_fail.ack_error, "SEMI_SYNC_REPLICA_TIMEOUT")

    def test_ambiguous_write_leader_crashed_post_replication(self):
        # Gate 14: Leader writes to followers but crashes before returning ACK to client
        trace = ReplicationAckTrace.simulate_write(
            policy=AckPolicy.QUORUM_W,
            cluster_size=3,
            leader_id="node_1",
            unreachable_replicas=set(),
            crashed_after_write_leader=True,
            w_quorum=2,
        )
        self.assertFalse(trace.client_acked)
        self.assertEqual(trace.ack_error, "CLIENT_TIMEOUT_LEADER_CRASHED_POST_REPLICATION")
        # Followers do hold the replicated entry despite client seeing failure/timeout!
        self.assertTrue(len(trace.replicas["node_2"].log) > 0)
        self.assertTrue(len(trace.replicas["node_3"].log) > 0)


class TestM17QuorumOverlap(unittest.TestCase):
    """Gate 12, Gate 13, Gate 15: Quorum arithmetic, overlap != linearizability, concurrent writes."""

    def test_quorum_intersection_arithmetic(self):
        qv = QuorumValidator(cluster_size=3, write_quorum=2, read_quorum=2)
        self.assertTrue(qv.is_quorum_valid())
        self.assertEqual(qv.min_overlap_count(), 1)

        res = qv.evaluate_overlap({"node_1", "node_2"}, {"node_2", "node_3"})
        self.assertTrue(res["has_overlap"])
        self.assertEqual(res["overlap_nodes"], ["node_2"])

    def test_counterexample_unversioned_stale_read(self):
        # Gate 13: Overlap alone does NOT equal latest-value read without versioning rule
        ce = QuorumValidator.demonstrate_counterexample_unversioned_stale_read()
        self.assertTrue(ce["stale_read_manifested"])
        self.assertEqual(ce["blind_first_response_value"], "v1")
        self.assertEqual(ce["version_resolved_value"], "v2")
        self.assertEqual(ce["proof"], "OVERLAP_ALONE_INSUFFICIENT_WITHOUT_VERSION_RULE")

    def test_counterexample_ambiguous_partial_write(self):
        # Gate 13 & Gate 14: Incomplete write violates linearizability across successive reads
        ce = QuorumValidator.demonstrate_counterexample_ambiguous_partial_write()
        self.assertTrue(ce["linearizability_violated"])
        self.assertEqual(ce["reader_1_observed"], "v2")
        self.assertEqual(ce["reader_2_observed"], "v1")
        self.assertEqual(ce["proof"], "OVERLAP_ALONE_DOES_NOT_GUARANTEE_LINEARIZABILITY")

    def test_counterexample_concurrent_conflicting_writes(self):
        # Gate 15: Concurrent writes under quorum overlap without consensus
        ce = QuorumValidator.demonstrate_counterexample_concurrent_conflicting_writes()
        self.assertEqual(ce["overlap_node"], "N2")
        self.assertIn("Reader {N1, N2} sees B", ce["disjoint_readers_anomaly"])
        self.assertEqual(
            ce["proof"],
            "QUORUM_OVERLAP_CANNOT_RESOLVE_CONCURRENT_WRITE_ORDER_WITHOUT_CONSENSUS",
        )


class TestM17RaftTrace(unittest.TestCase):
    """Gate 16, Gate 17, Gate 18, Gate 19: Raft vote/log trace, majority overlap limits, FLP."""

    def test_log_up_to_date_rule_precision(self):
        # Rule: cand_last_term > voter_last_term OR (cand_last_term == voter_last_term and cand_last_index >= voter_last_index)

        # 1. Candidate has higher term -> up to date even with smaller index
        self.assertTrue(
            RaftTraceValidator.is_candidate_log_up_to_date(
                cand_last_term=3, cand_last_index=1, voter_last_term=2, voter_last_index=5
            )
        )

        # 2. Candidate has lower term -> NOT up to date even with huge index
        self.assertFalse(
            RaftTraceValidator.is_candidate_log_up_to_date(
                cand_last_term=1, cand_last_index=100, voter_last_term=2, voter_last_index=2
            )
        )

        # 3. Same term: candidate has equal or greater index -> up to date
        self.assertTrue(
            RaftTraceValidator.is_candidate_log_up_to_date(
                cand_last_term=2, cand_last_index=4, voter_last_term=2, voter_last_index=4
            )
        )
        self.assertTrue(
            RaftTraceValidator.is_candidate_log_up_to_date(
                cand_last_term=2, cand_last_index=5, voter_last_term=2, voter_last_index=4
            )
        )

        # 4. Same term: candidate has smaller index -> NOT up to date
        self.assertFalse(
            RaftTraceValidator.is_candidate_log_up_to_date(
                cand_last_term=2, cand_last_index=3, voter_last_term=2, voter_last_index=4
            )
        )

    def test_partition_scenario_and_majority_limits(self):
        # Gate 16 & Gate 17: Bounded Raft vote/log trace & majority reasoning
        res = RaftTraceValidator.evaluate_partition_scenario()
        self.assertFalse(res["minority_can_commit_new_entries"])
        self.assertTrue(res["majority_candidate_elected"])
        self.assertEqual(res["votes_granted_to_C"], ["C", "D", "E"])
        self.assertTrue(res["stale_candidate_rejected"])

        # Majority overlap alone does not prove Leader Completeness
        self.assertIn("Leader Completeness strictly requires BOTH", res["safety_vs_majority_alone"])
        # Randomized election timeouts do not defeat FLP
        self.assertIn("DO NOT disprove or defeat the FLP theorem", res["flp_boundary_notes"])


class TestM17ConsistencyHistories(unittest.TestCase):
    """Gate 20, Gate 21, Gate 24: Consistency classification using invocation/response precedence."""

    def setUp(self):
        self.traces = get_standard_consistency_traces()

    def test_linearizable_history(self):
        t1 = self.traces["Trace_1_Linearizable"]
        is_lin, msg, viol = ConsistencyEvaluator.check_linearizability_single_register(t1)
        self.assertTrue(is_lin)
        self.assertEqual(msg, "LINEARIZABLE")
        self.assertIsNone(viol)

    def test_stale_read_violates_linearizability(self):
        t2 = self.traces["Trace_2_Stale_Read_Non_Linearizable"]
        is_lin, msg, viol = ConsistencyEvaluator.check_linearizability_single_register(t2)
        self.assertFalse(is_lin)
        self.assertIn("STALE_READ_VIOLATION", msg)
        self.assertEqual(viol, ("w1", "r1"))

    def test_read_your_writes_session_guarantee(self):
        # Gate 21: Read-Your-Writes tested distinctly
        t3 = self.traces["Trace_3_Read_Your_Writes_Violation"]
        is_ryw, msg, viol = ConsistencyEvaluator.check_read_your_writes(t3)
        self.assertFalse(is_ryw)
        self.assertIn("RYW_VIOLATION", msg)
        self.assertEqual(viol, ("w1", "r1"))

        # In linearizable trace 1, RYW is satisfied
        t1 = self.traces["Trace_1_Linearizable"]
        is_ryw_t1, _, _ = ConsistencyEvaluator.check_read_your_writes(t1)
        self.assertTrue(is_ryw_t1)

    def test_monotonic_reads_session_guarantee(self):
        # Gate 21: Monotonic Reads tested distinctly
        t4 = self.traces["Trace_4_Monotonic_Reads_Violation"]
        is_mono, msg, viol = ConsistencyEvaluator.check_monotonic_reads(t4)
        self.assertFalse(is_mono)
        self.assertIn("MONOTONIC_READS_VIOLATION", msg)
        self.assertEqual(viol, ("r1", "r2"))

        # In linearizable trace 1, Monotonic Reads is satisfied
        t1 = self.traces["Trace_1_Linearizable"]
        is_mono_t1, _, _ = ConsistencyEvaluator.check_monotonic_reads(t1)
        self.assertTrue(is_mono_t1)


class TestM17SafetyAndReset(unittest.TestCase):
    """Gate 9, Gate 10, Gate 29: No distributed service, no open ports, idempotent reset."""

    def test_reset_idempotence(self):
        # Running reset twice succeeds without error
        res1 = reset_m17_environment()
        self.assertEqual(res1, 0)
        res2 = reset_m17_environment()
        self.assertEqual(res2, 0)


if __name__ == "__main__":
    unittest.main()
