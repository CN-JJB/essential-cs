#!/usr/bin/env python3
"""
activity_l19_01.py
Essential CS: Stage 6 Module 19 (M19) Activity L19-01.

Hands-on activity: Deconstructing "Containers" into Kernel Namespaces & Cgroups.
Executes the canonical inspector and guides the learner through inspecting
the process isolation boundary.
"""

import json
import os
import sys
from pathlib import Path

# Add current directory to sys.path so we can import the inspector directly
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import s6_m19_ns_cgroup_inspector as inspector


def run_activity(save_scratch: bool = True) -> int:
    print("=" * 76)
    print(" ESSENTIAL CS -- ACTIVITY L19-01: CONTAINER DECONSTRUCTION")
    print(" Focus: Namespaces (View Partitioning) vs. Cgroups (Resource Quotas)")
    print("=" * 76)

    # 1. Run canonical inspection
    report = inspector.inspect_system(run_optional_probe=False)
    pre = report["os_preflight"]
    ns = report["namespace_inspection"]
    cg = report["cgroup_inspection"]
    ps = report["process_status_inspection"]
    sig = report["capability_signals"]

    # 2. Print Step 1: Host & Preflight
    print("\n[STEP 1: Host Environment & Preflight]")
    print(f" Host OS:                 {pre['platform_system']} {pre['platform_release']} ({pre['architecture']})")
    print(f" Canonical Linux:         {pre['is_canonical_linux']}")
    print(f" Core Preflight:          {pre['disposition']}")
    if not pre["is_canonical_linux"]:
        print(f" Notice:                  {pre['reason']}")
        print(" -> In non-Linux environments, Linux /proc/self/ns and cgroup interfaces")
        print("    are not natively present. To record Required Core evidence, run inside")
        print("    a canonical Linux environment (native Linux, WSL2, or a Linux VM).")

    # 3. Print Step 2: Namespace View Partitioning
    print("\n[STEP 2: Linux Namespaces -- View Partitioning (EC-CON-013 Isolation)]")
    if ns["available"]:
        print(f" Detected {ns['namespace_count']} active namespace types for current process:")
        for name, data in ns["namespaces_present"].items():
            inode_str = f"inode {data['inode']}" if data["inode"] is not None else "inode unreadable"
            print(f"   * {name:<18} -> {data.get('raw_target') or 'restricted'} ({inode_str})")
        print("\n Invariant: A process belongs to exactly one instance of each namespace type.")
        print(" Inode numbers represent the kernel's internal identifier for each namespace.")
    else:
        print(f" Status: {ns['disposition']}")
        print(f" Reason: {ns.get('reason')}")

    # 4. Print Step 3: Cgroups Resource Quotas
    print("\n[STEP 3: Linux Cgroups -- Resource Quotas & Accounting]")
    if cg["available"]:
        print(f" Cgroup Arrangement:      {cg['arrangement']}")
        print(f" Available v2 Controllers: {', '.join(cg['cgroup_v2_controllers']) or 'none'}")
        print(f" Mounted v1 Controllers:  {', '.join(cg['cgroup_v1_controllers']) or 'none'}")
        if cg["proc_self_cgroup_lines"]:
            print(" Current Process Cgroup Membership:")
            for line in cg["proc_self_cgroup_lines"]:
                print(f"   {line}")
        print("\n Invariant: Cgroups control HOW MUCH resource a process can consume;")
        print(" Namespaces control WHAT RESOURCES a process can see.")
    else:
        print(f" Status: {cg['disposition']}")
        print(f" Reason: {cg.get('reason')}")

    # 5. Print Step 4: Process Status and Limits
    print("\n[STEP 4: Process Credentials & Limits (Read-Only Status)]")
    if ps["available"]:
        print(f" Status:                  {ps['disposition']}")
        print(f" Uid / Gid:               {ps['status_fields'].get('Uid', 'N/A')} / {ps['status_fields'].get('Gid', 'N/A')}")
        for lk, lv in ps["limits_fields"].items():
            print(f" {lk:<24}: {lv}")
    else:
        print(f" Status:                  {ps['disposition']}")
        print(f" Reason:                  {ps.get('reason')}")

    # 6. Step 5: Mental Model Synthesis
    print("\n[STEP 5: Architectural Boundaries: Process vs. Container vs. VM]")
    print(" " + "-" * 74)
    print(" | Dimension         | Ordinary Process        | Containerized Process   | VM (conventional)   |")
    print(" | :---------------- | :---------------------- | :---------------------- | :------------------ |")
    print(" | Kernel Boundary   | Current host kernel     | Same host kernel        | Guest-kernel boundary|")
    print(" | Visibility (View) | Actual namespace/creds  | Configured namespaces   | Guest OS view       |")
    print(" | Resource Controls | May also use cgroups/rlimits | Configured cgroups/rlimits | VM/runtime config |")
    print(" | Security Evidence | Depends on actual controls | Shared-kernel trust boundary | Different boundary; not proof |")
    print(" " + "-" * 74)
    print(" Key Takeaway: 'Containers are just processes.' They are not lightweight VMs.")
    print(" Container security boundaries are bounded by the shared Linux kernel attack surface.")

    # 7. Overall Mechanism Status
    overall_status = (
        "REQUIRED CAPABILITY PASS"
        if (pre["is_canonical_linux"] and ns["available"] and cg["available"] and ps["available"])
        else "ENVIRONMENT-BLOCKED / NOT RUN"
    )
    print("-" * 76)
    print(f" Overall L19-01 Mechanism Status: {overall_status}")
    if overall_status != "REQUIRED CAPABILITY PASS":
        print(" Note: Host lacks canonical Linux interfaces. On non-Linux hosts (e.g. Windows),")
        print(" mechanism observation must be reported as ENVIRONMENT-BLOCKED / NOT RUN truthfully.")
    print("-" * 76)

    # 8. Save scratch report if writable
    if save_scratch:
        scratch_dir = CURRENT_DIR / ".scratch"
        try:
            scratch_dir.mkdir(parents=True, exist_ok=True)
            out_file = scratch_dir / "l19_01_observation.json"
            report["overall_status"] = overall_status
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n[Artifact Saved]: {out_file.relative_to(CURRENT_DIR)}")
        except Exception as e:
            print(f"\n[Notice]: Could not write scratch artifact: {e}")

    print("=" * 76)
    return 0 if overall_status == "REQUIRED CAPABILITY PASS" else 1


if __name__ == "__main__":
    sys.exit(run_activity())
