#!/usr/bin/env python3
"""M06 Fork, Exec & Lifecycle Fixture.

Demonstrates:
1. fork() parent/child return-value semantics and ordinary variable-copy separation.
2. exec() image replacement while preserving the process PID.
3. Child exit status and parent wait/reap protocol.
4. Controlled zombie-process observation with guaranteed cleanup.
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
    """Executes a bounded fork, ordinary-variable separation test, and wait/reap."""
    if not is_fork_supported():
        return {
            "supported": False,
            "reason": f"os.fork() is not available on {platform.system()}.",
        }

    test_var = 100
    r_pipe, w_pipe = os.pipe()

    pid = os.fork()
    if pid == 0:
        try:
            os.close(r_pipe)
            child_pid = os.getpid()
            parent_pid = os.getppid()
            test_var = 999
            msg = f"CHILD:{child_pid}:{parent_pid}:{test_var}".encode("utf-8")
            os.write(w_pipe, msg)
            os.close(w_pipe)
        finally:
            os._exit(42)

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
        "parent_var_after_fork": test_var,
        "child_var_after_mutation": child_mutated_var,
        "ordinary_variable_copy_separate": (test_var == 100 and child_mutated_var == 999),
        "exit_code": exit_code,
        "exit_code_matches": (exit_code == 42),
    }


def run_exec_lifecycle():
    """Forks, execs a fresh Python image, and verifies PID preservation + wait status."""
    if not is_fork_supported() or not hasattr(os, "execv"):
        return {
            "supported": False,
            "reason": f"fork/execv is not available on {platform.system()}.",
        }

    r_pipe, w_pipe = os.pipe()
    pid = os.fork()

    if pid == 0:
        try:
            os.close(r_pipe)
            os.dup2(w_pipe, 1)
            os.close(w_pipe)
            code = (
                "import os,sys; "
                "print(f'EXEC_PID:{os.getpid()}', flush=True); "
                "sys.exit(7)"
            )
            os.execv(sys.executable, [sys.executable, "-c", code])
        except BaseException:
            os._exit(127)

    os.close(w_pipe)
    with os.fdopen(r_pipe, "rb", closefd=True) as pipe:
        output = pipe.read().decode("utf-8", errors="replace").strip()

    _, wait_status = os.waitpid(pid, 0)
    exit_code = os.WEXITSTATUS(wait_status) if os.WIFEXITED(wait_status) else -1

    exec_pid = None
    if output.startswith("EXEC_PID:"):
        try:
            exec_pid = int(output.split(":", 1)[1])
        except ValueError:
            exec_pid = None

    return {
        "supported": True,
        "fork_child_pid": pid,
        "exec_reported_pid": exec_pid,
        "pid_preserved_across_exec": (exec_pid == pid),
        "exit_code": exit_code,
        "exit_code_matches": (exit_code == 7),
        "output": output,
    }


def observe_controlled_zombie(timeout=1.0):
    """Attempts to observe a temporary Linux zombie, then always reaps it."""
    if not is_fork_supported():
        return {
            "supported": False,
            "reason": f"os.fork() is not available on {platform.system()}.",
        }

    child_pid = os.fork()
    if child_pid == 0:
        os._exit(0)

    zombie_observed = False
    observed_state = "NotObserved"
    deadline = time.monotonic() + timeout

    try:
        proc_stat = Path(f"/proc/{child_pid}/stat")
        while time.monotonic() < deadline:
            if proc_stat.exists():
                try:
                    tokens = proc_stat.read_text(encoding="utf-8").strip().split()
                    if len(tokens) >= 3:
                        observed_state = tokens[2]
                        if observed_state == "Z":
                            zombie_observed = True
                            break
                except OSError:
                    pass
            time.sleep(0.02)
    finally:
        try:
            os.waitpid(child_pid, 0)
            reaped = True
        except ChildProcessError:
            reaped = False

    return {
        "supported": True,
        "child_pid": child_pid,
        "observed_state": observed_state,
        "zombie_observed": zombie_observed,
        "reaped": reaped,
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
    print(
        "Ordinary variable copy separate: "
        f"parent={res['parent_var_after_fork']}, child={res['child_var_after_mutation']} "
        f"({res['ordinary_variable_copy_separate']})"
    )
    print(f"Child reaped exit code: {res['exit_code']} (Matches 42: {res['exit_code_matches']})")
    print()

    print("=== Exec Image Replacement Observation ===")
    eres = run_exec_lifecycle()
    print(f"Fork child PID: {eres['fork_child_pid']}")
    print(f"PID reported after exec: {eres['exec_reported_pid']}")
    print(f"PID preserved across exec: {eres['pid_preserved_across_exec']}")
    print(f"Exec'd image exit code: {eres['exit_code']} (Matches 7: {eres['exit_code_matches']})")
    print()

    print("=== Controlled Zombie Observation ===")
    zres = observe_controlled_zombie()
    print(f"Child PID: {zres['child_pid']}")
    print(f"Observed state before wait(): {zres['observed_state']} (Zombie 'Z': {zres['zombie_observed']})")
    print(f"Reaped in finally block: {zres['reaped']}")
    if not zres["zombie_observed"]:
        print("Observation status: NOT OBSERVED in bounded polling window; cleanup still completed.")
    print()


if __name__ == "__main__":
    main()
