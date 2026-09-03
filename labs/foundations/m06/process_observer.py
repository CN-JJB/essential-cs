#!/usr/bin/env python3
"""M06 Process Observer.

Inspects:
1. Process Identity (PID) via os.getpid() and /proc/self/status.
2. Process State and Memory Footprint from procfs.
3. System call observation via strace (with graceful fallback if unavailable).
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def get_process_identity():
    """Returns basic process identity metadata."""
    return {
        "pid": os.getpid(),
        "ppid": os.getppid() if hasattr(os, "getppid") else None,
        "platform": platform.system(),
        "python_exe": sys.executable,
    }


def inspect_procfs():
    """Inspects /proc/self on Linux environments."""
    proc_status_path = Path("/proc/self/status")
    proc_stat_path = Path("/proc/self/stat")

    if not proc_status_path.exists():
        return {
            "procfs_available": False,
            "reason": "Not a Linux system or /proc filesystem unmounted.",
        }

    status_data = {}
    with open(proc_status_path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, val = line.split(":", 1)
                status_data[key.strip()] = val.strip()

    stat_tokens = []
    if proc_stat_path.exists():
        with open(proc_stat_path, "r", encoding="utf-8") as f:
            stat_tokens = f.read().strip().split()

    extracted_pid = int(status_data.get("Pid", -1))
    actual_pid = os.getpid()

    return {
        "procfs_available": True,
        "pid_matches": (extracted_pid == actual_pid),
        "status_pid": extracted_pid,
        "actual_pid": actual_pid,
        "name": status_data.get("Name", "Unknown"),
        "state": status_data.get("State", "Unknown"),
        "ppid": status_data.get("PPid", "Unknown"),
        "vmsize": status_data.get("VmSize", "Unknown"),
        "fdsize": status_data.get("FDSize", "Unknown"),
        "stat_raw_excerpt": " ".join(stat_tokens[:8]) if stat_tokens else "None",
    }


def observe_syscall():
    """Observes system calls via strace, or provides graceful fallback."""
    strace_bin = shutil.which("strace")
    if not strace_bin:
        return {
            "strace_tested": False,
            "status": "UNAVAILABLE",
            "reason": "strace binary not found in PATH.",
            "fallback_trace": (
                "# Fallback deterministic Linux strace excerpt for getpid() & write():\n"
                "getpid() = 42001\n"
                "write(1, \"Hello from syscall\\n\", 19) = 19"
            ),
        }

    # Verify if strace actually works (containers may block ptrace via seccomp/Yama)
    probe = subprocess.run(
        [strace_bin, "true"],
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        return {
            "strace_tested": True,
            "status": "RESTRICTED",
            "reason": f"strace blocked by environment ptrace policy (code {probe.returncode}).",
            "fallback_trace": (
                "# Fallback deterministic Linux strace excerpt (ptrace restricted):\n"
                "getpid() = 42001\n"
                "write(1, \"Hello from syscall\\n\", 19) = 19"
            ),
        }

    # Execute a safe trace on a tiny inline python command
    cmd = [
        strace_bin,
        "-e",
        "trace=write,getpid",
        sys.executable,
        "-c",
        "import os; os.getpid(); os.write(1, b'SYSCALL_PROBE_OK\\n')",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)

    return {
        "strace_tested": True,
        "status": "PASS",
        "stdout": res.stdout.strip(),
        "stderr_trace": res.stderr.strip(),
    }


def run_observer():
    print("=== M06 Process Observer ===")
    ident = get_process_identity()
    print(f"Current Process ID (os.getpid()): {ident['pid']}")
    print(f"Parent Process ID (os.getppid()): {ident['ppid']}")
    print(f"Platform: {ident['platform']}")
    print()

    print("=== Procfs Inspection (/proc/self) ===")
    proc = inspect_procfs()
    if proc["procfs_available"]:
        print(f"Status PID: {proc['status_pid']} (Matches getpid(): {proc['pid_matches']})")
        print(f"Process Name: {proc['name']}")
        print(f"State: {proc['state']}")
        print(f"Parent PID: {proc['ppid']}")
        print(f"Virtual Memory Size (VmSize): {proc['vmsize']}")
        print(f"FD Table Size (FDSize): {proc['fdsize']}")
        print(f"Stat Raw Excerpt: {proc['stat_raw_excerpt']}")
    else:
        print(f"Procfs unavailable: {proc['reason']}")
    print()

    print("=== System Call Observation ===")
    sc = observe_syscall()
    print(f"strace status: {sc['status']}")
    if sc["status"] == "PASS":
        print("Observed system calls (stderr):")
        print(sc["stderr_trace"])
    else:
        print(f"Reason: {sc['reason']}")
        print(sc["fallback_trace"])
    print()


if __name__ == "__main__":
    run_observer()
