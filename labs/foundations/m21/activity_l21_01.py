#!/usr/bin/env python3
"""
activity_l21_01.py — Hands-On Filesystem Boundary & Path Confinement (L21-01)
=============================================================================

Course-owned, localhost/local, synthetic, disposable filesystem boundary exercise.
Demonstrates why syntactic string checks and prefix matching fail to enforce
containment boundaries, and shows how resolved ancestry verification works.

All paths and files are synthetic and confined to a temporary directory created
and cleaned up during execution. No host-sensitive files are accessed.

Learning Invariants:
- Rejecting "../" is NOT sufficient to guarantee boundary containment.
- str.startswith(base) does NOT prove containment (sibling-prefix confusion).
- One resolve() / realpath() does NOT eliminate subsequent TOCTOU races.
- Authenticating an actor does NOT make raw input strings trustworthy.
- Canonicalization alone does NOT solve all concurrent filesystem races.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from path_confinement import (
    MECHANISM_LABEL,
    SyntheticTree,
    build_synthetic_tree,
    evaluate_standard_cases,
)

M21_DIR = Path(__file__).resolve().parent
SCRATCH_DIR = M21_DIR / ".scratch"


def print_banner() -> None:
    print("=" * 78)
    print("  ESSENTIAL CS — FOUNDATIONS M21: TRUST BOUNDARIES & CRYPTO USE")
    print("  L21-01: Where Are the Boundaries I Must Protect? (Path Confinement)")
    print("=" * 78)
    print()


def print_threat_boundary_map() -> None:
    print("-" * 78)
    print("THREAT BOUNDARY & AUTHORITY MAP (L21-01 WORKED ARCHITECTURE)")
    print("-" * 78)
    table = [
        ("Asset", "Synthetic user storage data (notes/hello.txt); host privacy"),
        ("Actor", "Untrusted client / caller supplying raw path parameters"),
        ("Authority", "Process ambient authority (POSIX/OS file access permissions)"),
        ("Boundary Crossing", "External input string -> Internal POSIX open() call"),
        ("Verification Obligation", "Resolve candidate path; verify commonpath ancestry before open"),
        ("Least Privilege", "Constrain daemon UID/GID to dedicated store root; minimal ambient tokens"),
        ("Defense in Depth", "Boundary check at API layer + containment at storage daemon + OS mode bits"),
        ("Residual Assumption", "No concurrent untrusted symlink manipulation in store directory (TOCTOU)"),
    ]
    for key, val in table:
        print(f"  {key:<24}: {val}")
    print("-" * 78)
    print()


def run_activity(verbose: bool = True) -> Dict[str, Any]:
    if verbose:
        print_banner()
        print_threat_boundary_map()

    tree: SyntheticTree = build_synthetic_tree()
    try:
        if verbose:
            print("[PHASE 1] Synthetic Course-Owned Tree Initialized:")
            print(f"  Root:            {tree.root}")
            print(f"  Authorized Root: {tree.authorized_root}")
            print(f"  Allowed File:    {tree.allowed_file.name}")
            print(f"  Outside File:    {tree.outside_file.name}")
            print(f"  Sibling Evil:    {tree.sibling_evil_file.parent.name}/{tree.sibling_evil_file.name}")
            print(f"  Symlink Status:  {tree.symlink_disposition}")
            if tree.symlink_error:
                print(f"  Symlink Note:    {tree.symlink_error}")
            print()

        verdicts = evaluate_standard_cases(tree, read_if_allowed=True)

        if verbose:
            print("[PHASE 2] Evaluating Path Candidates Against Containment Mechanisms:")
            header = f"{'Case ID':<26} | {'Naive Check':<11} | {'startswith':<11} | {'Ancestry':<10} | {'Decision':<18}"
            print("-" * len(header))
            print(header)
            print("-" * len(header))

            for v in verdicts:
                naive_str = "SAFE" if v.naive_string_safe else "UNSAFE"
                prefix_str = "N/A" if v.prefix_startswith_contained is None else ("CONTAINED" if v.prefix_startswith_contained else "OUTSIDE")
                ancestry_str = "CONTAINED" if v.resolved_contained else "OUTSIDE"
                print(f"{v.case_id:<26} | {naive_str:<11} | {prefix_str:<11} | {ancestry_str:<10} | {v.decision:<18}")

            print("-" * len(header))
            print()

            print("[PHASE 3] Detailed Security Analysis of Failure Modes:")
            for v in verdicts:
                print(f"  * Case [{v.case_id}]: candidate={v.candidate!r}")
                print(f"    - Naive string check:        {'Pass (looks safe)' if v.naive_string_safe else 'Rejected'}")
                print(f"    - prefix.startswith check:   {v.prefix_startswith_contained}")
                print(f"    - Resolved ancestry check:   {'Contained' if v.resolved_contained else 'Not Contained'}")
                print(f"    - Final Decision:            {v.decision}")
                print(f"    - Notes:                     {v.notes}")
                print()

            print("[PHASE 4] Explicit Engineering Inference Limits:")
            print("  1. Syntactic check failure: Rejecting '../' does not prevent symlink escape or absolute paths.")
            print("  2. Prefix startswith failure: 'store-evil' starts with 'store', confusing string checks.")
            print("  3. TOCTOU boundary: Path.resolve() verifies current filesystem state; it does not")
            print("     prevent a concurrent process from swapping symlinks before a subsequent open().")
            print("  4. Authentication boundary: An authenticated client identity does not make an unvalidated")
            print("     filename parameter safe to open.")
            print("  5. Disposable boundary: All activity was conducted in course-owned temporary scratch;")
            print("     zero host-sensitive files were touched.")
            print()

        observation_data: Dict[str, Any] = {
            "module": "M21",
            "lesson": "L21-01",
            "mechanism": MECHANISM_LABEL,
            "symlink_disposition": tree.symlink_disposition,
            "cases_evaluated": [v.as_dict() for v in verdicts],
            "inference_limits": [
                "Rejecting '../' is not sufficient.",
                "str.startswith(base) does not prove containment.",
                "One resolve() does not eliminate subsequent TOCTOU races.",
                "Authentication does not make filenames trustworthy.",
                "Canonicalization does not solve all filesystem races.",
            ],
        }

        SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
        obs_file = SCRATCH_DIR / "l21_01_observation.json"
        obs_file.write_text(json.dumps(observation_data, indent=2), encoding="utf-8")
        if verbose:
            print(f"[STATUS] Observation written to {obs_file}")
            print("[STATUS] L21-01 Activity Completed Successfully.")

        return observation_data

    finally:
        tree.cleanup()
        if verbose:
            print("[CLEANUP] Disposable synthetic tree removed.")


if __name__ == "__main__":
    try:
        run_activity(verbose=True)
        sys.exit(0)
    except Exception as exc:
        print(f"[FATAL ERROR] Activity failed: {exc}", file=sys.stderr)
        sys.exit(1)
