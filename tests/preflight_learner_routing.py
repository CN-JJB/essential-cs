#!/usr/bin/env python3
"""
preflight_learner_routing.py — Static regression gate for Issue #166 repair.

Verifies that learner-facing routing and governance truth cannot silently drift
again ("files exist but learners cannot reach them"):

A. Required Lab routes — book/ must visibly route to all five Required Labs.
B. Mini Cloud route — staged P0-P9 project connections exist and M24 defends
   the real Mini Cloud (synthetic sample explicitly non-final).
C. Governance truth — OQ-BP-001/OQ-BP-003/OQ-BP-006 lifecycle labels match the
   accepted Decisions (#155/D-033/D-034, #167/OQ-BP-006 CLOSED), while the
   #158 independent re-check requirement is preserved.
D. Hygiene — root .gitignore blocks local-agent state dirs and none are tracked.

Static only: reads committed text, runs nothing. Usable as a preflight script
(exit 0 on PASS) and as a unittest suite (CI: discover -s tests -p "preflight*.py").
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _contains(rel: str, *needles: str) -> tuple[bool, str]:
    try:
        text = _read(rel)
    except FileNotFoundError:
        return False, f"missing file {rel}"
    for needle in needles:
        if needle not in text:
            return False, f"{rel} lacks {needle!r}"
    return True, "ok"


# ---------------------------------------------------------------------------
# A. Required Lab routes: (home lesson, canonical ID, lab path, required mark)
# ---------------------------------------------------------------------------
REQUIRED_LAB_ROUTES = [
    ("book/11-networking-tls-http-cdn-proxies/L11-03.md", "LAB-REQ-01", "labs/lab_req_01", "Required"),
    ("book/06-processes-syscalls-execution-context/L06-01.md", "LAB-REQ-02", "labs/lab-req-02-xv6-syscall", "Required"),
    ("book/15-concurrency-threads-races-synchronization/L15-01.md", "LAB-REQ-03", "labs/lab_req_03", "Required"),
    ("book/13-databases-storage-indexing/L13-01.md", "LAB-REQ-04", "labs/lab_req_04", "Required"),
    ("book/14-databases-transactions-recovery-isolation/L14-01.md", "LAB-REQ-05", "labs/lab_req_05", "Required"),
]

# ---------------------------------------------------------------------------
# B. Mini Cloud staged route: (lesson, milestone marker, project path)
# ---------------------------------------------------------------------------
MINICLOUD_ROUTES = [
    ("book/00-the-map/L00-02.md", "P0", "project/README.md"),
    ("book/06-processes-syscalls-execution-context/L06-03.md", "P1", "project/minicloud"),
    ("book/10-networking-ip-dns-transport/L10-03.md", "P3", "project/minicloud"),
    ("book/13-databases-storage-indexing/L13-03.md", "P4", "project/minicloud/bench.py"),
    ("book/14-databases-transactions-recovery-isolation/L14-03.md", "P5", "project/minicloud"),
    ("book/19-modern-infrastructure-delivery/L19-03.md", "P7", "project/minicloud"),
    ("book/20-observability-reliability-engineering/L20-02.md", "P8", "project/minicloud"),
    ("book/22-security-synthesis-auth-composition/L22-03.md", "P2", "project/minicloud"),
    ("book/23-systems-thinking-judgment/L23-03.md", "P9", "project/minicloud/walkthrough.py"),
    ("book/24-final-system-defense/L24-01.md", "Mini Cloud", "project/minicloud"),
    ("book/24-final-system-defense/L24-02.md", "Mini Cloud", "project/minicloud"),
]


def check_required_lab_routes() -> list[str]:
    failures = []
    for lesson, lab_id, lab_path, _required_mark in REQUIRED_LAB_ROUTES:
        ok, why = _contains(lesson, lab_id, lab_path)
        if not ok:
            failures.append(why)
            continue
        text = _read(lesson)
        if "Required" not in text and "必修" not in text:
            failures.append(f"{lesson} routes {lab_id} but never marks it Required/必修 vs foundation")
    return failures


def _has_concrete_project_ref(text: str) -> bool:
    """Concrete project reference, not just the words 'Mini Cloud'."""
    if "project/minicloud" in text:
        return True
    has_minicloud_path = ("minicloud/" in text) or ("minicloud." in text)
    return has_minicloud_path and ("project/" in text)


def check_minicloud_routes() -> list[str]:
    failures = []
    for lesson, marker, project_path in MINICLOUD_ROUTES:
        try:
            text = _read(lesson)
        except FileNotFoundError:
            failures.append(f"missing file {lesson}")
            continue
        if marker not in text:
            failures.append(f"{lesson} lacks {marker!r}")
        elif project_path == "project/minicloud":
            if not _has_concrete_project_ref(text):
                failures.append(f"{lesson} lacks a concrete Mini Cloud project reference")
        elif project_path not in text:
            failures.append(f"{lesson} lacks {project_path!r}")
    # M24 must defend the REAL Mini Cloud, with the synthetic sample fenced off.
    for rel in (
        "book/24-final-system-defense/L24-01.md",
        "book/24-final-system-defense/L24-02.md",
        "labs/foundations/m24/README.md",
    ):
        try:
            text = _read(rel)
        except FileNotFoundError:
            failures.append(f"missing file {rel}")
            continue
        if not _has_concrete_project_ref(text):
            failures.append(f"{rel} does not route final defense to the real Mini Cloud")
    ok, why = _contains("book/24-final-system-defense/L24-01.md", "synthetic")
    if not ok:
        failures.append(why)
    # LAB-REQ-03 accepted predicate-break surface must exist and be wired.
    for rel, needle in (
        ("labs/lab_req_03/cond_predicate_break.c", "predicate"),
        ("labs/lab_req_03/harness.py", "cond_predicate_break"),
        ("labs/lab_req_03/test_lab.py", "predicate"),
        ("labs/lab_req_03/README.md", "cond_predicate_break"),
    ):
        ok, why = _contains(rel, needle)
        if not ok:
            failures.append(why)
    # LAB-REQ-04 two-size learner evidence surface must exist and be documented.
    for rel, needle in (
        ("labs/lab_req_04/harness.py", "run_lab_req_04_compare"),
        ("labs/lab_req_04/harness.py", "--compare-sizes"),
        ("labs/lab_req_04/README.md", "--compare-sizes"),
        ("course/evidence/lab-req-04-evidence-template.md", "--compare-sizes"),
    ):
        ok, why = _contains(rel, needle)
        if not ok:
            failures.append(why)
    return failures


def check_governance_truth() -> list[str]:
    failures = []
    expected = [
        ("tests/preflight_security_synthesis.py", "RESOLVED FOR v1.0 BY D-033"),
        ("meta/CURRICULUM_MAP.md", "D-033"),
        ("meta/CONCEPT_REGISTRY.md", "D-033"),
        ("book/00-the-map/L00-02.md", "D-033"),
        ("book/23-systems-thinking-judgment/L23-02.md", "D-033"),
        ("meta/CONCEPT_REGISTRY.md", "D-034"),
        ("meta/CURRICULUM_MAP.md", "D-034"),
        # OQ-BP-006 CLOSED as technical question; #153 same-lineage; #158 pending.
        ("tests/preflight_security_synthesis.py", "CLOSED (technical environment-definition/realization per #167"),
        ("meta/OPEN_QUESTIONS.md", "CLOSED — realized pin technically re-verified"),
        ("meta/OPEN_QUESTIONS.md", "#158 must independently re-check"),
        ("tests/preflight_security_synthesis.py", "#158 re-check still required"),
    ]
    for rel, needle in expected:
        ok, why = _contains(rel, needle)
        if not ok:
            failures.append(why)
    # No learner/test surface may still assert the pre-decision lifecycle states.
    stale = [
        ("tests/preflight_security_synthesis.py", '"OQ_BP_006": "OPEN / UNRESOLVED"'),
        ("tests/preflight_security_synthesis.py", '"OQ_BP_001": "OPEN / RFC-GATED'),
        ("tests/preflight_security_synthesis.py", "OQ_BP_001 == \"OPEN / RFC-GATED"),
        ("book/00-the-map/L00-02.md", "does not close that Open Question"),
        ("book/23-systems-thinking-judgment/L23-02.md", "RFC-GATED"),
        ("course/evidence/foundations-m24-evidence-template.md", "OPEN / UNRESOLVED"),
    ]
    for rel, needle in stale:
        try:
            text = _read(rel)
        except FileNotFoundError:
            failures.append(f"missing file {rel}")
            continue
        if needle in text:
            failures.append(f"{rel} still asserts stale lifecycle {needle!r}")
    return failures


def check_hygiene() -> list[str]:
    failures = []
    ok, why = _contains(".gitignore", "/.commandcode", "/.workbuddy-ai")
    if not ok:
        failures.append(why)
        return failures
    try:
        proc = subprocess.run(
            ["git", "ls-files", ".commandcode/**", ".workbuddy-ai/**"],
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        failures.append(f"git ls-files unavailable: {exc}")
        return failures
    tracked = [line for line in proc.stdout.splitlines() if line.strip()]
    if tracked:
        failures.append(f"tracked local-agent state must be empty, found: {tracked[:5]}")
    return failures


def collect_report() -> dict:
    return {
        "required_lab_routes": check_required_lab_routes(),
        "minicloud_routes": check_minicloud_routes(),
        "governance_truth": check_governance_truth(),
        "hygiene": check_hygiene(),
    }


class TestLearnerRoutingRegressions(unittest.TestCase):
    def test_required_lab_routes(self):
        self.assertEqual(check_required_lab_routes(), [])

    def test_minicloud_routes(self):
        self.assertEqual(check_minicloud_routes(), [])

    def test_governance_truth(self):
        self.assertEqual(check_governance_truth(), [])

    def test_hygiene(self):
        self.assertEqual(check_hygiene(), [])


def main() -> int:
    report = collect_report()
    failed = False
    for section, problems in report.items():
        if problems:
            failed = True
            print(f"FAIL {section}:")
            for problem in problems:
                print(f"  - {problem}")
        else:
            print(f"PASS {section}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
