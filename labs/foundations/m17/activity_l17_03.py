#!/usr/bin/env python3
"""
labs/foundations/m17/activity_l17_03.py

Activity for Lesson L17-03:
Consistency Guarantees, Session Guarantees & the Real CAP Boundary.

Demonstrates:
1. Linearizability classification using real-time invocation/response precedence
   (resp(op1) < inv(op2) => op1 must be serialized before op2).
2. Trace 1: Linearizable history.
3. Trace 2: Non-linearizable execution (stale read anomaly violating real-time precedence).
4. Trace 3: Client-centric Read-Your-Writes (RYW) guarantee violation.
5. Trace 4: Client-centric Monotonic Reads guarantee violation.
6. The CAP boundary:
   - Analyze partition/message-loss executions for a named object/request path.
   - Reject the static product-menu slogan "Pick two of C, A, P".
   - Under the theorem's model, atomic consistency and theorem-defined availability
     cannot both hold for every relevant request in all allowed partition executions.
7. Three-way disambiguation:
   - ACID Consistency = application invariant preservation under a transaction contract.
   - Transaction Isolation = a family of concurrency-visibility guarantees; serializability
     is one strong member.
   - Replicated Linearizability = legal sequential behavior plus real-time precedence.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from trace_harness import (
    ConsistencyEvaluator,
    get_standard_consistency_traces,
)


def run_activity() -> int:
    print("=" * 78)
    print(" Essential CS: L17-03 Consistency Models & Precedence Evaluation")
    print("=" * 78)

    traces = get_standard_consistency_traces()

    # --------------------------------------------------------------------------
    # Part 1: Linearizability Evaluation (Traces 1 & 2)
    # --------------------------------------------------------------------------
    print("\n[PART 1] Linearizability Evaluation (Real-Time Precedence Oracle)")

    # Trace 1: Linearizable
    t1 = traces["Trace_1_Linearizable"]
    t1_lin, t1_msg, t1_viol = ConsistencyEvaluator.check_linearizability_single_register(t1)
    print(f" -> Trace 1 (Sequential alternating reads/writes):")
    print(f"    Linearizable: {t1_lin} ({t1_msg})")

    # Trace 2: Stale Read Anomaly (Non-linearizable)
    t2 = traces["Trace_2_Stale_Read_Non_Linearizable"]
    t2_lin, t2_msg, t2_viol = ConsistencyEvaluator.check_linearizability_single_register(t2)
    print(f" -> Trace 2 (Client B reads stale 0 after Client A write completed):")
    print(f"    Linearizable: {t2_lin}")
    print(f"    Violation:    {t2_msg}")
    print(f"    Violating Op Pair: {t2_viol}")

    # --------------------------------------------------------------------------
    # Part 2: Session Guarantees (Traces 3 & 4)
    # --------------------------------------------------------------------------
    print("\n[PART 2] Client-Centric Session Guarantees")

    # Trace 3: Read-Your-Writes Violation
    t3 = traces["Trace_3_Read_Your_Writes_Violation"]
    t3_ryw, t3_msg, t3_viol = ConsistencyEvaluator.check_read_your_writes(t3)
    print(f" -> Trace 3 (Client A writes 1, then immediately reads lagging replica returning 0):")
    print(f"    RYW Satisfied: {t3_ryw}")
    print(f"    Violation:     {t3_msg}")
    print(f"    Violating Op Pair: {t3_viol}")

    # Trace 4: Monotonic Reads Violation
    t4 = traces["Trace_4_Monotonic_Reads_Violation"]
    t4_mono, t4_msg, t4_viol = ConsistencyEvaluator.check_monotonic_reads(t4)
    print(f" -> Trace 4 (Client B reads v2 from replica 1, then reads v1 from lagging replica 2):")
    print(f"    Monotonic Reads Satisfied: {t4_mono}")
    print(f"    Violation:                 {t4_msg}")
    print(f"    Violating Op Pair:         {t4_viol}")

    # --------------------------------------------------------------------------
    # Part 3: CAP Theorem & Consistency Disambiguation
    # --------------------------------------------------------------------------
    print("\n[PART 3] CAP Theorem & Consistency Disambiguation")
    cap_analysis = {
        "partition_nature": (
            "CAP analyzes executions in which the network may lose messages across a partition; "
            "this is a failure condition to include in the model, not a static product feature menu."
        ),
        "false_menu_rejected": (
            "The slogan 'Pick any two of C, A, P' hides the theorem's quantification over "
            "partition executions and request paths."
        ),
        "theorem_tradeoff": (
            "For the atomic read/write object in the course model, during allowed partition "
            "executions the same request path cannot guarantee both atomic/linearizable "
            "consistency and theorem-defined availability for every request."
        ),
        "three_way_disambiguation": {
            "ACID_Consistency": (
                "Application invariant preservation under the named transaction contract."
            ),
            "Transaction_Isolation": (
                "A family of concurrency-visibility guarantees; serializability is one strong member."
            ),
            "Replicated_Linearizability": (
                "A legal sequential object history that preserves real-time precedence."
            ),
        },
    }
    print(f" -> CAP Partition Reality: {cap_analysis['partition_nature']}")
    print(f" -> Rejected Shortcut:    {cap_analysis['false_menu_rejected']}")
    print(f" -> True Trade-off:       {cap_analysis['theorem_tradeoff']}")

    # Save output summary for learner evidence
    out_dir = os.path.dirname(__file__)
    summary_path = os.path.join(out_dir, "l17_03_observation.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "trace_1_linearizable": {"is_linearizable": t1_lin, "message": t1_msg},
                "trace_2_non_linearizable": {"is_linearizable": t2_lin, "violation": t2_msg, "pair": t2_viol},
                "trace_3_ryw_violation": {"is_satisfied": t3_ryw, "violation": t3_msg, "pair": t3_viol},
                "trace_4_monotonic_violation": {"is_satisfied": t4_mono, "violation": t4_msg, "pair": t4_viol},
                "cap_analysis": cap_analysis,
            },
            f,
            indent=2,
        )

    print(f"\n[EVIDENCE] Observation recorded to {summary_path}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(run_activity())
