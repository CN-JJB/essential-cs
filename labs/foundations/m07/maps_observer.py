#!/usr/bin/env python3
"""maps_observer.py - Essential CS M07 Virtual Memory Mapping Observer.

Parses and inspects /proc/self/maps on Linux hosts to examine virtual memory
regions, permission bits, and mapping types without hardcoding addresses.

Educational Invariant:
- /proc/self/maps reveals VIRTUAL address space intervals and permission flags.
- It does NOT expose physical page frame numbers (PFN).
- It does NOT prove physical RAM allocation (residency).
- Same virtual addresses in separate processes do NOT imply same physical RAM.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MappingEntry:
    start_addr: int
    end_addr: int
    perms: str
    is_readable: bool
    is_writable: bool
    is_executable: bool
    is_private: bool
    is_shared: bool
    offset: int
    dev: str
    inode: int
    pathname: str
    is_anonymous: bool

    @property
    def size_bytes(self) -> int:
        return self.end_addr - self.start_addr

    @property
    def size_kb(self) -> float:
        return self.size_bytes / 1024.0


# Regex pattern for a single line in /proc/<pid>/maps
# Example: 55ea1b65e000-55ea1b685000 r--p 00000000 08:02 1048602 /usr/bin/python3.12
MAPS_LINE_RE = re.compile(
    r"^([0-9a-fA-F]+)-([0-9a-fA-F]+)\s+"  # address range
    r"([r-][w-][x-][ps])\s+"              # permissions
    r"([0-9a-fA-F]+)\s+"                  # offset
    r"([0-9a-fA-F]+:[0-9a-fA-F]+)\s+"     # dev
    r"(\d+)"                               # inode
    r"(?:\s+(.*))?$"                       # pathname (optional)
)


def parse_maps_line(line: str) -> Optional[MappingEntry]:
    line = line.strip()
    if not line:
        return None
    match = MAPS_LINE_RE.match(line)
    if not match:
        return None

    start_str, end_str, perms, offset_str, dev, inode_str, path = match.groups()
    start_addr = int(start_str, 16)
    end_addr = int(end_str, 16)
    offset = int(offset_str, 16)
    inode = int(inode_str, 10)
    pathname = (path or "").strip()

    is_anon = not pathname or pathname.startswith("[anon")

    return MappingEntry(
        start_addr=start_addr,
        end_addr=end_addr,
        perms=perms,
        is_readable=perms[0] == "r",
        is_writable=perms[1] == "w",
        is_executable=perms[2] == "x",
        is_private=perms[3] == "p",
        is_shared=perms[3] == "s",
        offset=offset,
        dev=dev,
        inode=inode,
        pathname=pathname,
        is_anonymous=is_anon,
    )


def read_maps(maps_path: str = "/proc/self/maps") -> List[MappingEntry]:
    """Reads and parses mapping entries from the given procfs maps file."""
    if not os.path.exists(maps_path):
        raise FileNotFoundError(
            f"Maps file '{maps_path}' not found. "
            "This activity requires a Linux procfs environment."
        )

    entries: List[MappingEntry] = []
    with open(maps_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            entry = parse_maps_line(line)
            if entry:
                entries.append(entry)
    return entries


def summarize_mappings(entries: List[MappingEntry]) -> dict:
    total_count = len(entries)
    total_virtual_bytes = sum(e.size_bytes for e in entries)

    exec_entries = [e for e in entries if e.is_executable]
    writable_entries = [e for e in entries if e.is_writable]
    shared_entries = [e for e in entries if e.is_shared]
    anon_entries = [e for e in entries if e.is_anonymous]

    perms_set = sorted({e.perms for e in entries})

    return {
        "total_mappings": total_count,
        "total_virtual_kb": total_virtual_bytes / 1024.0,
        "distinct_permissions": perms_set,
        "executable_count": len(exec_entries),
        "writable_count": len(writable_entries),
        "shared_count": len(shared_entries),
        "anonymous_count": len(anon_entries),
    }


def main() -> int:
    print("=== M07 Virtual Memory Mapping Observer ===")
    print(f"Process PID: {os.getpid()}")
    print(f"Platform: {sys.platform}")

    maps_file = "/proc/self/maps"
    if not os.path.exists(maps_file):
        print(f"ERROR: {maps_file} is not available on this host.")
        print("Note: Linux procfs is required for live memory map inspection.")
        return 1

    try:
        entries = read_maps(maps_file)
    except Exception as exc:
        print(f"ERROR reading {maps_file}: {exc}")
        return 1

    summary = summarize_mappings(entries)
    print(f"\nTotal mappings parsed: {summary['total_mappings']}")
    print(f"Total virtual address space spanned: {summary['total_virtual_kb']:.1f} KiB")
    print(f"Distinct permissions observed: {', '.join(summary['distinct_permissions'])}")

    print("\n--- Sample Executable Mappings (e.g. code segments) ---")
    exec_samples = [e for e in entries if e.is_executable][:3]
    for e in exec_samples:
        path_desc = e.pathname if e.pathname else "[anonymous code]"
        print(f"  0x{e.start_addr:012x}-0x{e.end_addr:012x} {e.perms} {e.size_kb:8.1f} KiB  {path_desc}")

    print("\n--- Sample Writable Mappings (e.g. heap / data / stack) ---")
    writable_samples = [e for e in entries if e.is_writable][:3]
    for e in writable_samples:
        path_desc = e.pathname if e.pathname else "[anonymous data]"
        print(f"  0x{e.start_addr:012x}-0x{e.end_addr:012x} {e.perms} {e.size_kb:8.1f} KiB  {path_desc}")

    print("\n--- Evidence Boundary Checklist ---")
    print("[*] Virtual addresses shown above are process-local virtual intervals.")
    print("[*] Permissions (r/w/x/p/s) are enforced by CPU MMU during address translation.")
    print("[*] IMPORTANT: /proc/self/maps does NOT prove physical RAM frame occupancy.")
    print("[*] IMPORTANT: Another process may have identical numbers mapping to DIFFERENT physical RAM.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
