#!/usr/bin/env python3
"""
s6_m19_ns_cgroup_inspector.py
Essential CS: Stage 6 Module 19 (M19) Canonical Inspector.

Performs read-only observation of Linux namespaces, cgroups, and optional
capability boundaries without mutating host system state or requiring root/Docker.

Components:
1. OSPreflight: Confirms execution inside canonical Linux environment.
2. NamespaceInspector: Dynamic observation of /proc/self/ns/* symlinks.
3. CgroupInspector: Classifies cgroup arrangement (v2, v1, hybrid) and controllers.
4. CapabilityGate: Safe capability-gated unshare probe in an owned child process.
"""

import argparse
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class OSPreflight:
    """
    Confirms execution inside canonical Linux environment.
    Non-Linux hosts report ENVIRONMENT-BLOCKED / NOT RUN truthfully.
    """

    @staticmethod
    def inspect() -> Dict[str, Any]:
        system_name = platform.system()
        is_linux = (system_name == "Linux")
        proc_ns_path = Path("/proc/self/ns")
        proc_cgroup_path = Path("/proc/self/cgroup")

        proc_ns_readable = is_linux and proc_ns_path.exists() and os.access(str(proc_ns_path), os.R_OK)
        proc_cgroup_readable = is_linux and proc_cgroup_path.exists() and os.access(str(proc_cgroup_path), os.R_OK)

        core_available = is_linux and proc_ns_readable and proc_cgroup_readable

        return {
            "platform_system": system_name,
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "is_canonical_linux": is_linux,
            "proc_ns_readable": proc_ns_readable,
            "proc_cgroup_readable": proc_cgroup_readable,
            "disposition": (
                "REQUIRED CAPABILITY PASS"
                if core_available
                else "ENVIRONMENT-BLOCKED / NOT RUN"
            ),
            "reason": (
                "Canonical Linux /proc inspection interfaces accessible."
                if core_available
                else f"Non-Linux or restricted environment ({system_name}). Requires Linux with /proc access."
            ),
        }


class NamespaceInspector:
    """
    Dynamically discovers and inspects namespaces from /proc/self/ns/* symlinks.
    Does NOT freeze a timeless namespace count.
    Compares with parent process where readable.
    Zero mutation of any namespace.
    """

    @staticmethod
    def parse_ns_symlink(target_str: str) -> Tuple[Optional[str], Optional[int]]:
        """
        Parses namespace symlink targets like 'net:[4026531992]' or 'ipc:[4026531839]'.
        Returns (ns_type, inode_number).
        """
        match = re.match(r"^([a-z_]+):\[(\d+)\]$", target_str)
        if match:
            return match.group(1), int(match.group(2))
        return None, None

    @classmethod
    def inspect(cls, proc_dir: str = "/proc") -> Dict[str, Any]:
        ns_dir = Path(proc_dir) / "self" / "ns"
        if not ns_dir.exists() or not os.access(str(ns_dir), os.R_OK):
            return {
                "available": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "namespaces_present": {},
                "namespace_count": 0,
                "parent_comparison": {},
                "reason": f"Namespace directory {ns_dir} unreadable or absent.",
            }

        namespaces_present: Dict[str, Dict[str, Any]] = {}
        try:
            entries = sorted(os.listdir(str(ns_dir)))
        except Exception as e:
            return {
                "available": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "namespaces_present": {},
                "namespace_count": 0,
                "parent_comparison": {},
                "reason": f"Failed to list {ns_dir}: {e}",
            }

        for entry in entries:
            entry_path = ns_dir / entry
            try:
                raw_target = os.readlink(str(entry_path))
                ns_type, inode = cls.parse_ns_symlink(raw_target)
                namespaces_present[entry] = {
                    "entry_name": entry,
                    "raw_target": raw_target,
                    "parsed_type": ns_type or entry,
                    "inode": inode,
                }
            except OSError as err:
                namespaces_present[entry] = {
                    "entry_name": entry,
                    "raw_target": None,
                    "parsed_type": entry,
                    "inode": None,
                    "error": str(err),
                }

        # Compare with parent process if possible
        parent_comparison: Dict[str, Any] = {}
        try:
            ppid = os.getppid()
            parent_ns_dir = Path(proc_dir) / str(ppid) / "ns"
            if parent_ns_dir.exists() and os.access(str(parent_ns_dir), os.R_OK):
                for entry, data in namespaces_present.items():
                    p_entry = parent_ns_dir / entry
                    if p_entry.exists():
                        try:
                            p_target = os.readlink(str(p_entry))
                            _, p_inode = cls.parse_ns_symlink(p_target)
                            is_shared = (p_inode is not None and p_inode == data.get("inode"))
                            parent_comparison[entry] = {
                                "parent_inode": p_inode,
                                "self_inode": data.get("inode"),
                                "shares_parent_namespace": is_shared,
                            }
                        except OSError as p_err:
                            parent_comparison[entry] = {
                                "error": f"Parent readlink failed: {p_err}",
                                "shares_parent_namespace": "UNKNOWN / RESTRICTED",
                            }
            else:
                parent_comparison["_status"] = f"Parent /proc/{ppid}/ns unreadable or permission denied"
        except Exception as ppid_err:
            parent_comparison["_status"] = f"Parent comparison skipped: {ppid_err}"

        return {
            "available": True,
            "disposition": "REQUIRED CAPABILITY PASS",
            "namespaces_present": namespaces_present,
            "namespace_count": len(namespaces_present),
            "parent_comparison": parent_comparison,
            "inference_limit": (
                "Namespace IDs (inodes) identify kernel isolation boundaries for this process. "
                "Namespaces partition resources and visibility, but do NOT provide complete security isolation "
                "or independent kernels (unlike hardware virtualization)."
            ),
        }


class CgroupInspector:
    """
    Inspects cgroup hierarchy and available controllers without modifying any state.
    Classifies arrangement: cgroup_v2, cgroup_v1, hybrid, or unavailable.
    Zero writes to /sys/fs/cgroup.
    """

    @classmethod
    def inspect(cls, proc_dir: str = "/proc", sys_dir: str = "/sys") -> Dict[str, Any]:
        cgroup_file = Path(proc_dir) / "self" / "cgroup"
        mounts_file = Path(proc_dir) / "mounts"
        sys_cgroup_dir = Path(sys_dir) / "fs" / "cgroup"

        if not cgroup_file.exists() or not os.access(str(cgroup_file), os.R_OK):
            return {
                "available": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "arrangement": "unavailable",
                "proc_self_cgroup_lines": [],
                "cgroup_v2_controllers": [],
                "cgroup_v1_controllers": [],
                "reason": f"{cgroup_file} unreadable or absent.",
            }

        proc_lines: List[str] = []
        try:
            with open(str(cgroup_file), "r", encoding="utf-8") as f:
                proc_lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            return {
                "available": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "arrangement": "unavailable",
                "proc_self_cgroup_lines": [],
                "reason": f"Failed reading {cgroup_file}: {e}",
            }

        # Inspect mounts for cgroup/cgroup2
        has_v1_mount = False
        has_v2_mount = False
        v1_controllers_mounted: List[str] = []

        if mounts_file.exists() and os.access(str(mounts_file), os.R_OK):
            try:
                with open(str(mounts_file), "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 3:
                            fstype = parts[2]
                            mountpoint = parts[1]
                            if fstype == "cgroup2":
                                has_v2_mount = True
                            elif fstype == "cgroup":
                                has_v1_mount = True
                                base_name = os.path.basename(mountpoint)
                                if base_name and base_name not in v1_controllers_mounted:
                                    v1_controllers_mounted.append(base_name)
            except Exception:
                pass

        # Check /proc/self/cgroup format
        has_v2_line = any(line.startswith("0::") for line in proc_lines)
        has_v1_lines = any(not line.startswith("0::") and ":" in line for line in proc_lines)

        # Classify arrangement
        if (has_v2_line or has_v2_mount) and not (has_v1_lines or has_v1_mount):
            arrangement = "cgroup_v2"
        elif (has_v1_lines or has_v1_mount) and not (has_v2_line or has_v2_mount):
            arrangement = "cgroup_v1"
        elif (has_v2_line or has_v2_mount) and (has_v1_lines or has_v1_mount):
            arrangement = "hybrid"
        else:
            arrangement = "unknown"

        # Check controllers available under cgroup v2
        v2_controllers: List[str] = []
        v2_controllers_file = sys_cgroup_dir / "cgroup.controllers"
        if v2_controllers_file.exists() and os.access(str(v2_controllers_file), os.R_OK):
            try:
                with open(str(v2_controllers_file), "r", encoding="utf-8") as f:
                    v2_controllers = f.read().strip().split()
            except Exception:
                pass

        return {
            "available": True,
            "disposition": "REQUIRED CAPABILITY PASS",
            "arrangement": arrangement,
            "proc_self_cgroup_lines": proc_lines,
            "cgroup_v2_controllers": sorted(v2_controllers),
            "cgroup_v1_controllers": sorted(v1_controllers_mounted),
            "read_only_verified": True,
            "inference_limit": (
                "Cgroups meter, allocate, and constrain host physical resources (CPU, memory, IO, PIDs). "
                "Cgroups do NOT isolate namespace visibility or create an independent operating system kernel."
            ),
        }


class CapabilityGate:
    """
    Handles optional capability-gated extensions (unshare probe) safely in an owned child process.
    Never uses sudo. Never runs unshare in the parent process.
    Reaps child processes cleanly.
    Distro sysctls are treated as signals only, not conclusive proof.
    """

    @staticmethod
    def inspect_signals(proc_dir: str = "/proc") -> Dict[str, Any]:
        sysctl_path = Path(proc_dir) / "sys" / "kernel" / "unprivileged_userns_clone"
        value = None
        readable = False
        if sysctl_path.exists() and os.access(str(sysctl_path), os.R_OK):
            try:
                with open(str(sysctl_path), "r", encoding="utf-8") as f:
                    value = f.read().strip()
                readable = True
            except Exception:
                pass

        return {
            "unprivileged_userns_clone_present": sysctl_path.exists(),
            "unprivileged_userns_clone_readable": readable,
            "unprivileged_userns_clone_value": value,
            "signal_note": (
                "Distro sysctl /proc/sys/kernel/unprivileged_userns_clone is a heuristic signal only. "
                "Absence of this file does NOT prove user namespaces are unsupported (many modern kernels "
                "enable unprivileged user namespaces at build time without this Debian/Ubuntu-specific sysctl)."
            ),
        }

    @classmethod
    def probe_unshare_capability(cls, timeout_sec: float = 2.0) -> Dict[str, Any]:
        """
        Runs an owned child process testing unshare -U true (unprivileged user namespace clone).
        Reaps child cleanly.
        Reports PASS or ENVIRONMENT-BLOCKED / NOT RUN.
        """
        if platform.system() != "Linux":
            return {
                "available": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "returncode": None,
                "reason": f"Non-Linux platform ({platform.system()}). unshare probe cannot run.",
            }

        # Check if unshare command exists
        unshare_path = None
        for candidate in ("/usr/bin/unshare", "/bin/unshare"):
            if os.path.exists(candidate) and os.access(candidate, os.X_OK):
                unshare_path = candidate
                break

        if not unshare_path:
            return {
                "available": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "returncode": None,
                "reason": "unshare executable not found in /usr/bin or /bin.",
            }

        # Execute bounded child probe
        proc = None
        try:
            proc = subprocess.Popen(
                [unshare_path, "-U", "true"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout_bytes, stderr_bytes = proc.communicate(timeout=timeout_sec)
            code = proc.returncode
            reaped = True
        except subprocess.TimeoutExpired:
            if proc:
                proc.kill()
                proc.communicate()
            return {
                "available": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "returncode": -1,
                "reason": "unshare probe timed out and child was reaped.",
            }
        except Exception as e:
            return {
                "available": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "returncode": None,
                "reason": f"Subprocess execution failed: {e}",
            }

        if code == 0:
            return {
                "available": True,
                "disposition": "CAPABILITY PASS",
                "returncode": 0,
                "reason": "Unprivileged user namespace unshare succeeded in child process.",
            }
        else:
            err_msg = stderr_bytes.decode("utf-8", errors="replace").strip()
            return {
                "available": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "returncode": code,
                "error_output": err_msg,
                "reason": f"unshare returned non-zero ({code}): {err_msg}",
            }


def inspect_system(run_optional_probe: bool = False) -> Dict[str, Any]:
    """
    Aggregates full M19 inspection report.
    """
    preflight = OSPreflight.inspect()
    ns_info = NamespaceInspector.inspect()
    cgroup_info = CgroupInspector.inspect()
    signals = CapabilityGate.inspect_signals()

    report: Dict[str, Any] = {
        "os_preflight": preflight,
        "namespace_inspection": ns_info,
        "cgroup_inspection": cgroup_info,
        "capability_signals": signals,
    }

    if run_optional_probe:
        report["optional_unshare_probe"] = CapabilityGate.probe_unshare_capability()
    else:
        report["optional_unshare_probe"] = {
            "available": False,
            "disposition": "OPTIONAL / NOT RUN",
            "reason": "Use --run-optional-unshare to trigger bounded child probe.",
        }

    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Essential CS S6-M19 Canonical Linux Namespace & Cgroup Inspector"
    )
    parser.add_argument("--json", action="store_true", help="Print structured JSON report")
    parser.add_argument(
        "--run-optional-unshare",
        action="store_true",
        help="Run bounded optional unshare probe in an owned child process",
    )
    args = parser.parse_args()

    report = inspect_system(run_optional_probe=args.run_optional_unshare)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["os_preflight"]["is_canonical_linux"] else 1

    print("=" * 72)
    print(" Essential CS S6-M19: Canonical Linux Namespace & Cgroup Inspector")
    print("=" * 72)
    pre = report["os_preflight"]
    print(f" Platform OS:             {pre['platform_system']} {pre['platform_release']} ({pre['architecture']})")
    print(f" Canonical Linux:         {pre['is_canonical_linux']}")
    print(f" Core Preflight:          {pre['disposition']}")
    if not pre["is_canonical_linux"]:
        print(f" Note:                    {pre['reason']}")
    print("-" * 72)

    ns = report["namespace_inspection"]
    print(f" [Namespaces Detected]:   {ns['namespace_count']} active types")
    print(f" Disposition:             {ns['disposition']}")
    if ns["available"]:
        for name, data in ns["namespaces_present"].items():
            print(f"   - {name:<20}: {data.get('raw_target') or 'unreadable'} (inode: {data.get('inode')})")
    else:
        print(f"   Reason:                {ns.get('reason')}")
    print("-" * 72)

    cg = report["cgroup_inspection"]
    print(f" [Cgroup Hierarchy]:      {cg['arrangement']}")
    print(f" Disposition:             {cg['disposition']}")
    if cg["available"]:
        print(f"   v2 Controllers:        {', '.join(cg['cgroup_v2_controllers']) or 'none detected'}")
        print(f"   v1 Controllers:        {', '.join(cg['cgroup_v1_controllers']) or 'none detected'}")
        print(f"   Self Cgroup Path:      {cg['proc_self_cgroup_lines'][0] if cg['proc_self_cgroup_lines'] else 'none'}")
    else:
        print(f"   Reason:                {cg.get('reason')}")
    print("-" * 72)

    un = report["optional_unshare_probe"]
    print(f" [Optional Unshare Probe]: {un['disposition']}")
    print(f"   Reason:                {un['reason']}")
    print("=" * 72)

    return 0 if pre["is_canonical_linux"] else 1


if __name__ == "__main__":
    sys.exit(main())
