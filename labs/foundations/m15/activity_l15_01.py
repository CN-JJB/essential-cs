#!/usr/bin/env python3
"""
Activity L15-01: Why is my threaded code wrong?
Anchors EC-CON-015 and runs real UB-free C11/pthread evidence only when
the canonical Linux + GCC Required environment is available.
"""

import os
import sys

EC_CON_015_DEFINITION = (
    "Overlapping progress or interleaving of operations, whether or not they execute "
    "simultaneously on hardware. Concurrency creates ordering and shared-state obligations."
)

DISAMBIGUATION_MANDATE = {
    "concurrency_vs_parallelism": (
        "Concurrency is overlapping progress/interleaving; parallelism is physical "
        "simultaneous execution on hardware."
    ),
    "single_core_concurrency": (
        "Concurrency can occur on one CPU core through time-slicing/interleaving; exact "
        "switch points are runtime observations, not source-line guarantees."
    ),
    "logical_race_vs_c_data_race": (
        "A logical race condition is an ordering flaw; a C data race is Undefined Behavior. "
        "The Required fixture uses defined C11 atomic counter accesses instead of relying on a data race."
    ),
}


def _load_harness():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    lab_dir = os.path.abspath(os.path.join(this_dir, "..", "..", "lab_req_03"))
    if lab_dir not in sys.path:
        sys.path.insert(0, lab_dir)
    from harness import ConcurrencyLabHarness
    return ConcurrencyLabHarness(lab_dir=lab_dir)


def run_activity_l15_01(verbose=True):
    harness = _load_harness()
    gate = harness.canonical_environment_status()
    base = {
        "ec_con_015_definition": EC_CON_015_DEFINITION,
        "disambiguation": DISAMBIGUATION_MANDATE,
        "environment_gate": gate,
        "inference_limit_acknowledged": (
            "The coordinated relaxed-atomic fixture demonstrates a non-atomic compound "
            "read-compute-store transition. It does not prove a memory-ordering defect, "
            "cache-coherency failure, or a universal scheduler manifestation rate."
        ),
    }

    if not gate["ready"]:
        result = {
            **base,
            "execution_disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "deterministic_result": None,
            "phase_trace": [],
            "ub_free_audit_passed": None,
        }
        if verbose:
            print("=" * 68)
            print(" Activity L15-01: Concurrency Definition & Lost-Update Verification")
            print("=" * 68)
            print(f' [EC-CON-015 Definition]: "{EC_CON_015_DEFINITION}"')
            print(" [Execution]: ENVIRONMENT-BLOCKED / NOT RUN")
            print(f" [Reason]: {gate.get('reason')}")
            print(" No empirical lost-update trace has been synthesized.")
            print("=" * 68)
        return result

    cp1 = harness.run_checkpoint_1_deterministic_lost_update()
    deterministic_result = None
    if cp1.get("passed"):
        deterministic_result = {
            "rounds": cp1.get("rounds"),
            "expected_serial": cp1.get("expected_serial"),
            "actual_value": cp1.get("actual_value"),
            "lost_updates": cp1.get("lost_updates"),
            "ub_present": cp1.get("ub_present"),
        }

    result = {
        **base,
        "execution_disposition": "PASS" if cp1.get("passed") else "FAIL",
        "deterministic_result": deterministic_result,
        "phase_trace": cp1.get("phase_trace", []),
        "ub_free_audit_passed": (not cp1.get("ub_present", True)) if cp1.get("passed") else False,
        "checkpoint": cp1,
    }

    if verbose:
        print("=" * 68)
        print(" Activity L15-01: Concurrency Definition & Lost-Update Verification")
        print("=" * 68)
        print(f' [EC-CON-015 Definition]: "{EC_CON_015_DEFINITION}"')
        print(f" [Execution]: {result['execution_disposition']}")
        if deterministic_result:
            print(f"   Rounds:          {deterministic_result.get('rounds')}")
            print(f"   Expected Serial: {deterministic_result.get('expected_serial')}")
            print(f"   Actual Count:    {deterministic_result.get('actual_value')}")
            print(f"   Lost Updates:    {deterministic_result.get('lost_updates')}")
        else:
            print(f"   Error: {cp1.get('error', 'deterministic checkpoint failed')}")
        print(f" [Inference Limit]: {base['inference_limit_acknowledged']}")
        print("=" * 68)
    return result


if __name__ == "__main__":
    run_activity_l15_01(verbose=True)
