#!/usr/bin/env python3
"""M06 Scheduler & Process State Fixture.

Demonstrates:
1. Process state classification (Running/Runnable 'R' vs Sleeping/Waiting 'S').
2. CPU sharing intuition: CPU-bound loop vs I/O/timer wait.
3. Safe polling and guaranteed process cleanup without leaked workers.
"""

import os
import platform
import signal
import sys
import time
from pathlib import Path


def is_procfs_supported():
    return Path("/proc/self/stat").exists()


def run_scheduler_observation(sample_duration=1.5):
    """Spawns one CPU-active worker and one sleeping worker, sampling states."""
    if not hasattr(os, "fork") or not is_procfs_supported():
        return {
            "supported": False,
            "reason": f"fork or /proc not supported on {platform.system()}.",
        }

    pids_to_clean = []

    # 1. Spawn CPU-active child
    cpu_pid = os.fork()
    if cpu_pid == 0:
        try:
            end_time = time.time() + 5.0  # Safe upper timeout
            while time.time() < end_time:
                pass  # Burn CPU cycles
        finally:
            os._exit(0)

    pids_to_clean.append(cpu_pid)

    # 2. Spawn sleeping child
    sleep_pid = os.fork()
    if sleep_pid == 0:
        try:
            time.sleep(5.0)  # Waiting on kernel timer
        finally:
            os._exit(0)

    pids_to_clean.append(sleep_pid)

    cpu_states = set()
    sleep_states = set()

    try:
        # Sample states periodically for sample_duration seconds
        start = time.time()
        while time.time() - start < sample_duration:
            # Sample cpu child
            stat_file_cpu = Path(f"/proc/{cpu_pid}/stat")
            if stat_file_cpu.exists():
                try:
                    with open(stat_file_cpu, "r", encoding="utf-8") as f:
                        parts = f.read().strip().split()
                        if len(parts) >= 3:
                            cpu_states.add(parts[2])
                except Exception:
                    pass

            # Sample sleep child
            stat_file_sleep = Path(f"/proc/{sleep_pid}/stat")
            if stat_file_sleep.exists():
                try:
                    with open(stat_file_sleep, "r", encoding="utf-8") as f:
                        parts = f.read().strip().split()
                        if len(parts) >= 3:
                            sleep_states.add(parts[2])
                except Exception:
                    pass

            time.sleep(0.05)

    finally:
        # GUARANTEED CLEANUP: Terminate and reap all spawned children
        for pid in pids_to_clean:
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass
            try:
                os.waitpid(pid, 0)
            except OSError:
                pass

    return {
        "supported": True,
        "cpu_pid": cpu_pid,
        "sleep_pid": sleep_pid,
        "observed_cpu_states": sorted(list(cpu_states)),
        "observed_sleep_states": sorted(list(sleep_states)),
        "cpu_showed_running": ("R" in cpu_states),
        "sleep_showed_sleeping": ("S" in sleep_states),
    }


def main():
    print("=== M06 Scheduler & Process State Observation ===")
    res = run_scheduler_observation(sample_duration=1.0)
    if not res["supported"]:
        print(f"SKIPPED: {res['reason']}")
        return

    print(f"CPU-active worker (PID {res['cpu_pid']}) observed states: {res['observed_cpu_states']}")
    print(f"Sleeping worker (PID {res['sleep_pid']}) observed states: {res['observed_sleep_states']}")
    print(f"CPU worker showed 'R' (Running/Runnable): {res['cpu_showed_running']}")
    print(f"Sleeping worker showed 'S' (Interruptible Sleep): {res['sleep_showed_sleeping']}")
    print()


if __name__ == "__main__":
    main()
