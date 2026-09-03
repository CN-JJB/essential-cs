#!/usr/bin/env python3
"""M06 Scheduler & Process State Fixture.

Demonstrates bounded Linux procfs observations for:
1. CPU-active work (often observed as R: running/runnable).
2. A sleeping process (often observed as S: interruptible sleep).
3. Safe polling and guaranteed child cleanup.

The exact sampled state letters are Linux implementation evidence, not a universal scheduler contract.
"""

import os
import platform
import signal
import time
from pathlib import Path


def is_procfs_supported():
    return Path("/proc/self/stat").exists()


def run_scheduler_observation(sample_duration=1.5):
    """Spawns one CPU-active worker and one sleeping worker, then samples Linux states."""
    if not hasattr(os, "fork") or not is_procfs_supported():
        return {
            "supported": False,
            "reason": f"fork or /proc not supported on {platform.system()}.",
        }

    pids_to_clean = []

    cpu_pid = os.fork()
    if cpu_pid == 0:
        try:
            end_time = time.monotonic() + 5.0
            while time.monotonic() < end_time:
                pass
        finally:
            os._exit(0)
    pids_to_clean.append(cpu_pid)

    sleep_pid = os.fork()
    if sleep_pid == 0:
        try:
            time.sleep(5.0)
        finally:
            os._exit(0)
    pids_to_clean.append(sleep_pid)

    cpu_states = set()
    sleep_states = set()

    try:
        deadline = time.monotonic() + sample_duration
        while time.monotonic() < deadline:
            for pid, bucket in ((cpu_pid, cpu_states), (sleep_pid, sleep_states)):
                stat_file = Path(f"/proc/{pid}/stat")
                if stat_file.exists():
                    try:
                        parts = stat_file.read_text(encoding="utf-8").strip().split()
                        if len(parts) >= 3:
                            bucket.add(parts[2])
                    except OSError:
                        pass
            time.sleep(0.03)
    finally:
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
        "observed_cpu_states": sorted(cpu_states),
        "observed_sleep_states": sorted(sleep_states),
        "cpu_showed_running_or_runnable": ("R" in cpu_states),
        "sleep_showed_interruptible_sleep": ("S" in sleep_states),
    }


def main():
    print("=== M06 Scheduler & Process State Observation ===")
    res = run_scheduler_observation(sample_duration=1.0)
    if not res["supported"]:
        print(f"SKIPPED: {res['reason']}")
        return

    print(f"CPU-active worker (PID {res['cpu_pid']}) observed states: {res['observed_cpu_states']}")
    print(f"Sleeping worker (PID {res['sleep_pid']}) observed states: {res['observed_sleep_states']}")
    print(f"Observed Linux 'R' for CPU worker: {res['cpu_showed_running_or_runnable']}")
    print(f"Observed Linux 'S' for sleeping worker: {res['sleep_showed_interruptible_sleep']}")
    if not res["cpu_showed_running_or_runnable"] or not res["sleep_showed_interruptible_sleep"]:
        print("Observation note: expected sample relation was NOT OBSERVED in this bounded window; do not invent it.")
    print()


if __name__ == "__main__":
    main()
