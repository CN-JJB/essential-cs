#!/usr/bin/env python3
"""residency_fixture.py - Essential CS M07 Virtual Reservation vs Physical Residency.

Demonstrates the distinction between address-space reservation (virtual)
and physical memory commitment (resident set) via bounded demand paging.

Educational Invariants:
- Reserving virtual address space (via mmap) expands virtual address space (VmSize).
- It does NOT immediately allocate equal physical RAM frames.
- Writing to pages triggers CPU page faults (minor faults in Linux accounting)
  that prompt the OS kernel to bind real physical page frames (increasing VmRSS).
- Tests must assert directional relationships, not brittle exact numerical ratios.
"""

from __future__ import annotations

import mmap
import os
import sys
from dataclasses import dataclass
from typing import Optional

# Optional resource module (available on Unix/Linux)
try:
    import resource
except ImportError:
    resource = None  # type: ignore


PAGE_SIZE = 4096
# Bounded allocation size: 16 MiB = 4096 pages of 4 KiB
DEFAULT_ALLOC_BYTES = 16 * 1024 * 1024


@dataclass
class MemoryMetrics:
    vm_size_kb: Optional[int]
    vm_rss_kb: Optional[int]
    minor_faults: Optional[int]


def read_proc_status_field(field_name: str) -> Optional[int]:
    """Reads a numeric KiB field from /proc/self/status (e.g. 'VmSize:', 'VmRSS:')."""
    status_path = "/proc/self/status"
    if not os.path.exists(status_path):
        return None

    prefix = f"{field_name}:"
    with open(status_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith(prefix):
                parts = line.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    return int(parts[1])
    return None


def get_current_metrics() -> MemoryMetrics:
    vmsize = read_proc_status_field("VmSize")
    vmrss = read_proc_status_field("VmRSS")

    minflt = None
    if resource is not None:
        try:
            rusage = resource.getrusage(resource.RUSAGE_SELF)
            minflt = rusage.ru_minflt
        except Exception:
            minflt = None

    return MemoryMetrics(vm_size_kb=vmsize, vm_rss_kb=vmrss, minor_faults=minflt)


def run_residency_experiment(alloc_bytes: int = DEFAULT_ALLOC_BYTES) -> dict:
    """Runs the bounded reservation and incremental touch experiment."""
    total_pages = alloc_bytes // PAGE_SIZE
    half_pages = total_pages // 2

    # Step 0: Baseline
    baseline = get_current_metrics()

    # Step 1: Reserve virtual memory via anonymous mmap (no writes yet)
    # On Linux, mmap(-1, length) creates MAP_PRIVATE | MAP_ANONYMOUS
    mm = mmap.mmap(-1, alloc_bytes, flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS, prot=mmap.PROT_READ | mmap.PROT_WRITE)
    reserved = get_current_metrics()

    # Step 2: Touch first half of the pages (writing 1 byte per page)
    for page_idx in range(half_pages):
        mm[page_idx * PAGE_SIZE] = 0x42
    half_touched = get_current_metrics()

    # Step 3: Touch remaining pages
    for page_idx in range(half_pages, total_pages):
        mm[page_idx * PAGE_SIZE] = 0x42
    fully_touched = get_current_metrics()

    # Step 4: Cleanup
    mm.close()
    cleaned = get_current_metrics()

    return {
        "alloc_bytes": alloc_bytes,
        "total_pages": total_pages,
        "half_pages": half_pages,
        "baseline": baseline,
        "reserved": reserved,
        "half_touched": half_touched,
        "fully_touched": fully_touched,
        "cleaned": cleaned,
    }


def format_metric(val: Optional[int], unit: str = "KiB") -> str:
    if val is None:
        return "N/A"
    return f"{val:,} {unit}"


def main() -> int:
    print("=== M07 Virtual Reservation vs Physical Residency Fixture ===")
    print(f"Process PID: {os.getpid()}")
    print(f"Page Size: {PAGE_SIZE} bytes")
    print(f"Allocation Target: {DEFAULT_ALLOC_BYTES // (1024 * 1024)} MiB ({DEFAULT_ALLOC_BYTES // PAGE_SIZE} pages)")

    if not os.path.exists("/proc/self/status"):
        print("NOTICE: /proc/self/status not available. Metrics will rely on resource module if available.")

    results = run_residency_experiment()

    print("\n--- Experimental Stages & Observations ---")
    headers = f"{'Stage':<18} | {'VmSize':<14} | {'VmRSS':<14} | {'Minor Faults':<14}"
    print(headers)
    print("-" * len(headers))

    stages = [
        ("0. Baseline", results["baseline"]),
        ("1. Reserved", results["reserved"]),
        ("2. Half Touched", results["half_touched"]),
        ("3. Full Touched", results["fully_touched"]),
        ("4. Cleaned Up", results["cleaned"]),
    ]

    for name, m in stages:
        vsz_s = format_metric(m.vm_size_kb, "KiB")
        rss_s = format_metric(m.vm_rss_kb, "KiB")
        flt_s = format_metric(m.minor_faults, "faults")
        print(f"{name:<18} | {vsz_s:<14} | {rss_s:<14} | {flt_s:<14}")

    print("\n--- Mechanism Verifications ---")
    b = results["baseline"]
    r = results["reserved"]
    h = results["half_touched"]
    f = results["fully_touched"]

    if r.vm_size_kb is not None and b.vm_size_kb is not None:
        vsz_delta = r.vm_size_kb - b.vm_size_kb
        print(f"[*] Reservation VmSize Delta: +{vsz_delta} KiB (Virtual address space successfully reserved)")

    if r.vm_rss_kb is not None and b.vm_rss_kb is not None:
        rss_res_delta = r.vm_rss_kb - b.vm_rss_kb
        print(f"[*] Reservation VmRSS Delta: +{rss_res_delta} KiB (Physical RAM remains largely uncommitted before touch)")

    if f.vm_rss_kb is not None and r.vm_rss_kb is not None:
        rss_touch_delta = f.vm_rss_kb - r.vm_rss_kb
        print(f"[*] Touching Pages VmRSS Delta: +{rss_touch_delta} KiB (Physical frames allocated upon first write)")

    if f.minor_faults is not None and r.minor_faults is not None:
        fault_delta = f.minor_faults - r.minor_faults
        print(f"[*] Touching Pages Minor Fault Delta: +{fault_delta} faults (Demand paging traps resolved by OS)")

    print("\n--- Inference Limitations ---")
    print("[*] Demand-paging behavior observed here is specific to Linux/POSIX virtual memory policy.")
    print("[*] Exact RSS increase and fault counts vary by OS page size, zero-page optimizations, and runtime state.")
    print("[*] Never assume a universal fixed ratio between malloc bytes and resident physical RAM.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
