#!/usr/bin/env python3
"""
Activity L15-02: How do I make it right?
Runs Required synchronization evidence only on the canonical Linux + GCC baseline.
"""

import os
import sys


def _load_harness():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    lab_dir = os.path.abspath(os.path.join(this_dir, "..", "..", "lab_req_03"))
    if lab_dir not in sys.path:
        sys.path.insert(0, lab_dir)
    from harness import ConcurrencyLabHarness
    return ConcurrencyLabHarness(lab_dir=lab_dir)


def run_activity_l15_02(verbose=True, iterations=10000, timeout_sec=1.5):
    harness = _load_harness()
    gate = harness.canonical_environment_status()
    base = {
        "environment_gate": gate,
        "predicate_recheck_mandate": (
            "POSIX permits spurious wakeups and a condition-wait return does not imply the "
            "shared predicate is true. The predicate must be re-evaluated under mutex "
            "protection; Essential CS uses the idiomatic while (!predicate) loop."
        ),
        "mutex_fairness_inference_limit": (
            "A passing mutex-protected counter proves mutual exclusion for that critical "
            "section, not FIFO fairness or starvation freedom."
        ),
        "deadlock_watchdog_inference_limit": (
            "A timeout alone proves only a bounded stall. Circular deadlock evidence also "
            "requires both first-lock ownership events and both second-lock-attempt events."
        ),
    }

    if not gate["ready"]:
        result = {
            **base,
            "execution_disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "mutex_repair": None,
            "cond_rendezvous": None,
            "controlled_deadlock": None,
        }
        if verbose:
            print("=" * 68)
            print(" Activity L15-02: Mutex, Condition Rendezvous & Deadlock Boundaries")
            print("=" * 68)
            print(" [Execution]: ENVIRONMENT-BLOCKED / NOT RUN")
            print(f" [Reason]: {gate.get('reason')}")
            print("=" * 68)
        return result

    mutex_res = harness.run_checkpoint_3_mutex_repair(iterations=iterations)
    cond_res = harness.run_checkpoint_4_cond_rendezvous()
    deadlock_res = harness.run_checkpoint_5_deadlock_preconditions(timeout_sec=timeout_sec)
    all_passed = all(x.get("passed") for x in (mutex_res, cond_res, deadlock_res))
    result = {
        **base,
        "execution_disposition": "PASS" if all_passed else "FAIL",
        "mutex_repair": mutex_res,
        "cond_rendezvous": cond_res,
        "controlled_deadlock": deadlock_res,
    }

    if verbose:
        print("=" * 68)
        print(" Activity L15-02: Mutex, Condition Rendezvous & Deadlock Boundaries")
        print("=" * 68)
        print(f" [Execution]: {result['execution_disposition']}")
        print(f" [Mutex]     {mutex_res}")
        print(f" [Condition] {cond_res}")
        print(f" [Deadlock]  {deadlock_res}")
        print("=" * 68)
    return result


if __name__ == "__main__":
    run_activity_l15_02(verbose=True)
