#!/usr/bin/env python3
"""
labs/foundations/m17/activity_l17_02.py

Activity for Lesson L17-02:
Consensus, Raft Election Safety Trace, and the FLP Impossibility Boundary.

Demonstrates:
1. Formal properties of consensus: Agreement, Validity, Termination.
2. The Raft Log Up-To-Date rule:
   lastTerm_cand > lastTerm_voter OR
   (lastTerm_cand == lastTerm_voter AND lastIndex_cand >= lastIndex_voter)
3. 5-node cluster partition (2 | 3):
   - Minority partition {A, B} cannot elect a leader or commit entries.
   - Majority partition {C, D, E} elects Term 2 leader with 3 votes.
   - Out-of-date candidate rejected by voter.
4. Why Majority Overlap alone is NOT the entire Raft safety proof:
   - Majority overlap prevents two leaders in the same term.
   - Leader Completeness requires BOTH majority overlap AND the Log Up-To-Date rule.
5. FLP boundary:
   - Asynchronous network + at least one crash failure => no deterministic consensus can guarantee termination.
   - Randomized election timeouts provide practical liveness under partial synchrony,
     but DO NOT formally disprove or defeat FLP.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from trace_harness import (
    RaftLogEntry,
    RaftNodeRecord,
    RaftTraceValidator,
)


def run_activity() -> int:
    print("=" * 78)
    print(" Essential CS: L17-02 Consensus & Raft Election Trace Activity")
    print("=" * 78)

    # --------------------------------------------------------------------------
    # Part 1: Bounded Raft Partition Trace (5 Nodes: {A,B} | {C,D,E})
    # --------------------------------------------------------------------------
    print("\n[PART 1] 5-Node Partition Scenario ({A, B} minority | {C, D, E} majority)")
    part_res = RaftTraceValidator.evaluate_partition_scenario()

    print(f" -> Cluster Nodes: {part_res['cluster_nodes']}")
    print(f" -> Partition Topology: Minority={part_res['partition']['minority']}, Majority={part_res['partition']['majority']}")
    print(f" -> Can minority partition commit new entries? {part_res['minority_can_commit_new_entries']} (Needs 3/5 votes)")
    print(f" -> Majority candidate {part_res['majority_candidate']} votes granted: {part_res['votes_granted_to_C']}")
    print(f" -> Majority candidate elected: {part_res['majority_candidate_elected']}")

    # --------------------------------------------------------------------------
    # Part 2: Log Up-To-Date Rule Evaluation (§5.4.1)
    # --------------------------------------------------------------------------
    print("\n[PART 2] Raft Log Up-To-Date Voting Rule (§5.4.1)")
    voter_node = RaftNodeRecord(
        node_id="Voter_Y",
        current_term=2,
        voted_for=None,
        log=[
            RaftLogEntry(1, 1, "cmd_1"),
            RaftLogEntry(2, 2, "cmd_2"),  # Voter has last_term=2, last_index=2
        ],
    )

    # Case A: Candidate has older term (cand_term=1, cand_index=5 vs voter term=2)
    # Even though candidate has longer log, its term is strictly older!
    cand_a_ok = RaftTraceValidator.is_candidate_log_up_to_date(
        cand_last_term=1, cand_last_index=5, voter_last_term=2, voter_last_index=2
    )
    granted_a, reason_a = RaftTraceValidator.evaluate_request_vote(
        voter=voter_node,
        candidate_id="Cand_A",
        candidate_term=3,
        cand_last_term=1,
        cand_last_index=5,
    )
    print(f" -> Candidate A (term 1, index 5) vs Voter Y (term 2, index 2):")
    print(f"    Log up-to-date? {cand_a_ok} | Vote granted? {granted_a} ({reason_a})")

    # Case B: Candidate has same term, but shorter log (term=2, index=1 vs voter index=2)
    cand_b_ok = RaftTraceValidator.is_candidate_log_up_to_date(
        cand_last_term=2, cand_last_index=1, voter_last_term=2, voter_last_index=2
    )
    granted_b, reason_b = RaftTraceValidator.evaluate_request_vote(
        voter=voter_node,
        candidate_id="Cand_B",
        candidate_term=3,
        cand_last_term=2,
        cand_last_index=1,
    )
    print(f" -> Candidate B (term 2, index 1) vs Voter Y (term 2, index 2):")
    print(f"    Log up-to-date? {cand_b_ok} | Vote granted? {granted_b} ({reason_b})")

    # Case C: Candidate has strictly higher term (cand_term=3, cand_index=1 vs voter term=2)
    cand_c_ok = RaftTraceValidator.is_candidate_log_up_to_date(
        cand_last_term=3, cand_last_index=1, voter_last_term=2, voter_last_index=2
    )
    granted_c, reason_c = RaftTraceValidator.evaluate_request_vote(
        voter=voter_node,
        candidate_id="Cand_C",
        candidate_term=3,
        cand_last_term=3,
        cand_last_index=1,
    )
    print(f" -> Candidate C (term 3, index 1) vs Voter Y (term 2, index 2):")
    print(f"    Log up-to-date? {cand_c_ok} | Vote granted? {granted_c} ({reason_c})")

    # --------------------------------------------------------------------------
    # Part 3: The Boundary: Majority Alone != Full Safety Proof & FLP
    # --------------------------------------------------------------------------
    print("\n[PART 3] The Boundary: Majority Overlap vs. Leader Completeness & FLP")
    print(f" -> Why majority overlap alone is not the whole proof:")
    print(f"    {part_res['safety_vs_majority_alone']}")
    print(f" -> FLP Impossibility Theorem & Randomized Timeouts:")
    print(f"    {part_res['flp_boundary_notes']}")

    # Save output summary for learner evidence
    out_dir = os.path.dirname(__file__)
    summary_path = os.path.join(out_dir, "l17_02_observation.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "partition_trace": part_res,
                "case_a_stale_term": {"granted": granted_a, "reason": reason_a},
                "case_b_shorter_log": {"granted": granted_b, "reason": reason_b},
                "case_c_higher_term": {"granted": granted_c, "reason": reason_c},
            },
            f,
            indent=2,
        )

    print(f"\n[EVIDENCE] Observation recorded to {summary_path}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(run_activity())
