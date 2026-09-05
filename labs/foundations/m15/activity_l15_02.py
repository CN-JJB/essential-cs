#!/usr/bin/env python3
"""
Activity L15-02: How do I make it right?
Demonstrates mutual exclusion with POSIX mutexes, condition-variable rendezvous
with mandatory predicate recheck guards, and controlled circular deadlock verification.

Revisits:
EC-CON-001 State, EC-CON-007 Specification, EC-CON-008 Invariant, EC-CON-009 Correctness
"""

import json
import os
import platform
import shutil
import subprocess
import sys


def run_activity_l15_02(verbose=True):
    """
    Executes L15-02 hands-on activity:
    1. Mutex repair: restores state transition invariant
    2. Condition variable rendezvous: verifies predicate recheck loop guard
    3. Controlled deadlock: child process circular wait preconditions + watchdog reaping
    """
    this_dir = os.path.dirname(os.path.abspath(__file__))
    lab_req_03_dir = os.path.abspath(os.path.join(this_dir, "..", "..", "lab_req_03"))

    try:
        from ...lab_req_03.harness import ConcurrencyLabHarness
        harness = ConcurrencyLabHarness(lab_dir=lab_req_03_dir)
    except Exception:
        sys.path.insert(0, lab_req_03_dir)
        from harness import ConcurrencyLabHarness
        harness = ConcurrencyLabHarness(lab_dir=lab_req_03_dir)

    mutex_res = harness.run_checkpoint_3_mutex_repair(iterations=10000)
    cond_res = harness.run_checkpoint_4_cond_rendezvous()
    deadlock_res = harness.run_checkpoint_5_deadlock_preconditions(timeout_sec=1.5)

    result = {
        "mutex_repair": mutex_res,
        "cond_rendezvous": cond_res,
        "controlled_deadlock": deadlock_res,
        "predicate_recheck_mandate": (
            "POSIX IEEE Std 1003.1-2024 permits spurious wakeups and multiprocessor reordering. "
            "Returning from pthread_cond_wait does NOT imply that the predicate is true. "
            "The predicate MUST be re-evaluated under mutex protection (the while (!predicate) pattern)."
        ),
        "mutex_fairness_inference_limit": (
            "Passing a mutex-protected counter test proves mutual exclusion for the critical section, "
            "but does NOT prove FIFO lock fairness or absence of thread starvation under high concurrency."
        ),
        "deadlock_watchdog_inference_limit": (
            "A timeout alone proves only that progress stalled within the allotted time. "
            "Deadlock is proven because circular wait preconditions (both workers holding first lock and "
            "attempting the other's lock) were verified before timeout occurred."
        ),
    }

    if verbose:
        print("=" * 68)
        print(" Activity L15-02: Mutex, Condition Rendezvous & Deadlock Boundaries")
        print("=" * 68)
        print(" [Part 1: POSIX Mutex Repair]")
        mr = result["mutex_repair"]
        print(f"   Status:              {'PASS' if mr.get('passed') else 'FAIL'}")
        print(f"   Expected Invariant:  {mr.get('expected')}")
        print(f"   Actual Count:        {mr.get('actual')}")
        print(f"   Invariant Preserved: {mr.get('invariant_preserved')}")
        print(f"   Inference Limit:     {result['mutex_fairness_inference_limit']}")

        print("\n [Part 2: Condition-Variable Rendezvous]")
        cr = result["cond_rendezvous"]
        print(f"   Status:              {'PASS' if cr.get('passed') else 'FAIL'}")
        print(f"   Consumed Value:      {cr.get('final_data')}")
        print(f"   Predicate Evals:     {cr.get('predicate_eval_count')}")
        print(f"   Predicate Guard:     {cr.get('predicate_recheck_verified')}")
        print(f"   Mandate:             {result['predicate_recheck_mandate']}")

        print("\n [Part 3: Controlled Deadlock & Watchdog]")
        dl = result["controlled_deadlock"]
        print(f"   Status:              {'PASS' if dl.get('passed') else 'FAIL'}")
        print(f"   Child PID:           {dl.get('child_pid')}")
        print(f"   Preconditions:       First: {dl.get('first_locks_acquired')}, Second: {dl.get('second_locks_attempted')}")
        print(f"   Watchdog Timeout:    {dl.get('watchdog_timeout_sec')}s (Triggered: {dl.get('watchdog_triggered')})")
        print(f"   Child Reaped:        Returncode {dl.get('child_reaped_returncode')}")
        print(f"   Inference Limit:     {result['deadlock_watchdog_inference_limit']}")
        print("=" * 68)

    return result


if __name__ == "__main__":
    run_activity_l15_02(verbose=True)
