#!/usr/bin/env python3
"""M06 Fork, Exec & Lifecycle Fixture.

Demonstrates:
1. Two-stage process creation (fork clones context; parent/child separate memory).
2. Child exit status and parent wait/reap protocol.
3. Controlled zombie process observation with guaranteed cleanup.
"""

import os
import platform
import sys
import time
from pathlib import Path


def is_fork_supported():
    """Checks whether os.fork is supported on current platform."""
    return hasattr(os, "fork")


def run_fork_lifecycle():
    """Executes a bounded fork, variable isolation test, and wait/exit reap."""
    if not is_fork_supported():
        return {
            "supported": False,
            "reason": f"os.fork() is not available on {platform.system()}.",
        }

    # Variable to test memory isolation
    test_var = 100

    r_pipe, w_pipe = os.pipe()

    pid = os.fork()
    if pid == 0:
        # Child process execution
        try:
            os.close(r_pipe)
            child_pid = os.getpid()
            parent_pid = os.getppid()
            test_var = 999  # Mutate in child address space

            # Send child observations to parent via pipe
            msg = f"CHILD:{child_pid}:{parent_pid}:{test_var}".encode("utf-8")
            os.write(w_pipe, msg)
            os.close(w_pipe)
        finally:
            os._exit(42)  # Controlled exit status 42

    # Parent process execution
    os.close(w_pipe)
    raw_data = os.read(r_pipe, 1024).decode("utf-8")
    os.close(r_pipe)

    _, wait_status = os.waitpid(pid, 0)
    exit_code = os.WEXITSTATUS(wait_status) if os.WIFEXITED(wait_status) else -1

    child_info = raw_data.split(":")
    child_observed_pid = int(child_info[1])
    child_observed_parent = int(child_info[2])
    child_mutated_var = int(child_info[3])

    return {
        "supported": True,
        "parent_pid": os.getpid(),
        "fork_returned_pid": pid,
        "child_pid": child_observed_pid,
        "child_reported_parent": child_observed_parent,
        "parent_var_after_fork": test_var,  # Must remain 100
        "child_var_after_mutation": child_mutated_var,  # 999
        "memory_isolated": (test_var == 100 and child_mutated_var == 999),
        "exit_code": exit_code,
        "exit_code_matches": (exit_code == 42),
    }


def observe_controlled_zombie():
    """Demonstrates a temporary zombie process with deterministic reaping."""
    if not is_fork_supported():
        return {
            "supported": False,
            "reason": f"os.fork() is not available on {platform.system()}.",
        }

    child_pid = os.fork()
    if child_pid == 0:
        # Child terminates immediately
        os._exit(0)

    zombie_observed = False
    observed_state = "Unknown"

    try:
        # Give kernel brief moment to mark child terminated while parent does not call wait()
        time.sleep(0.1)

        proc_stat = Path(f"/proc/{child_pid}/stat")
        if proc_stat.exists():
            with open(proc_stat, "r", encoding="utf-8") as f:
                tokens = f.read().strip().split()
                # Field index 2 in /proc/<pid>/stat is state
                if len(tokens) >= 3:
                    observed_state = tokens[2]
                    zombie_observed = (observed_state == "Z")
        else:
            observed_state = "ProcfsEntryGone"
    finally:
        # GUARANTEED REAP: Never leave a zombie process behind!
        os.waitpid(child_pid, 0)

    return {
        "supported": True,
        "child_pid": child_pid,
        "observed_state": observed_state,
        "zombie_observed": zombie_observed,
        "reaped": True,
    }


def main():
    print("=== M06 Fork & Process Lifecycle Fixture ===")
    if not is_fork_supported():
        print(f"SKIPPED: os.fork() not supported on {platform.system()}.")
        return

    res = run_fork_lifecycle()
    print(f"Parent PID: {res['parent_pid']}")
    print(f"Fork returned child PID: {res['fork_returned_pid']}")
    print(f"Child reported PID: {res['child_pid']}")
    print(f"Memory unshared: Parent var={res['parent_var_after_fork']}, Child mutated var={res['child_var_after_mutation']} (Isolated: {res['memory_isolated']})")
    print(f"Child reaped exit code: {res['exit_code']} (Matches 42: {res['exit_code_matches']})")
    print()

    print("=== Controlled Zombie Observation ===")
    zres = observe_controlled_zombie()
    print(f"Child PID: {zres['child_pid']}")
    print(f"Observed state in /proc prior to wait(): {zres['observed_state']} (Zombie 'Z': {zres['zombie_observed']})")
    print(f"Reaped in finally block: {zres['reaped']}")
    print()


if __name__ == "__main__":
    main()
