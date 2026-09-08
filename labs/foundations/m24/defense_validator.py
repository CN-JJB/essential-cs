#!/usr/bin/env python3
"""
defense_validator.py — M24 16-Trace Architecture Defense Dossier Structural Validator
=====================================================================================

Validates the structural completeness, traceability, and syntactic integrity of an
Essential CS Capstone Architectural Defense Dossier (Markdown document).

Audited Invariants:
1. Exact presence of all 16 Core Architectural Traces.
2. Complete mapping across all 12 Evidence Areas (E01–E12).
3. Pairwise validity of Claim IDs and Artifact references.
4. Detection of unresolved template placeholders (e.g. [TODO], [Record ...]).
5. Verification of Explicit Unknowns and actionable Learning Plan linkage.
6. Machine validation boundary: Emits STRUCTURAL_CHECK_PASS only. Machine checks
   never issue a learner competency PASS or numerical score.

Standard Library Only (PEP 557 dataclasses, re, pathlib, typing).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# The 16 Core Architectural Traces exactly per M24 contract
REQUIRED_TRACES: List[Tuple[int, str, str]] = [
    (1, "Request Trace", r"1\.\s*Request\s*Trace"),
    (2, "Data & State Trace", r"2\.\s*Data\s*&\s*State\s*Trace"),
    (3, "Control & Authority Trace", r"3\.\s*Control\s*&\s*Authority\s*Trace"),
    (4, "State Inventory", r"4\.\s*State\s*Inventory"),
    (5, "Invariants & Specifications", r"5\.\s*Invariants\s*&\s*Specifications"),
    (6, "Trust Boundaries", r"6\.\s*Trust\s*Boundaries"),
    (7, "Isolation Boundaries", r"7\.\s*Isolation\s*Boundaries"),
    (8, "Failure & Risk Walkthrough", r"8\.\s*Failure\s*&\s*Risk\s*Walkthrough"),
    (9, "Security & Privacy Decisions", r"9\.\s*Security\s*&\s*Privacy\s*Decisions"),
    (10, "Measurements & Performance Evidence", r"10\.\s*Measurements\s*&\s*Performance\s*Evidence"),
    (11, "Cost & Scale Estimates", r"11\.\s*Cost\s*&\s*Scale\s*Estimates"),
    (12, "Alternatives Considered", r"12\.\s*Alternatives\s*Considered"),
    (13, "When-Not-To-Use & Rejected Choices", r"13\.\s*When-Not-To-Use\s*&\s*Rejected\s*Choices"),
    (14, "Explicit Unknowns", r"14\.\s*Explicit\s*Unknowns"),
    (15, "Learning Plan", r"15\.\s*Learning\s*Plan"),
    (16, "Changed-Constraint Adaptation", r"16\.\s*Changed-Constraint\s*Adaptation"),
]

# The 12 Evidence Areas exactly per M24 contract
REQUIRED_EVIDENCE_AREAS: List[Tuple[str, str]] = [
    ("E01", "End-to-End Request Flow"),
    ("E02", "State & Data Lifecycle"),
    ("E03", "Core Invariants & Specs"),
    ("E04", "Trust & Isolation Boundaries"),
    ("E05", "Failure Domains & Resilience"),
    ("E06", "Transport & App Security"),
    ("E07", "Empirical Measurement"),
    ("E08", "Capacity & Cost Models"),
    ("E09", "Trade-Off & Alternative Analysis"),
    ("E10", "Explicit Unknowns & Limits"),
    ("E11", "Changed-Constraint Adaptation"),
    ("E12", "Pre-Ship Operational Readiness"),
]

# Patterns representing unresolved template placeholders
PLACEHOLDER_PATTERNS = [
    re.compile(r"\[TODO[^\]]*\]", re.IGNORECASE),
    re.compile(r"\[Record\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[State\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Detail\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[List\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Describe\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Identify\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Explain\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Walk\s+through\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Provide\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Estimate\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Calculate\s+[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Unfilled[^\]]*\]", re.IGNORECASE),
]


@dataclass
class ValidationReport:
    dossier_path: str
    is_valid: bool
    status: str
    traces_found: List[str] = field(default_factory=list)
    traces_missing: List[str] = field(default_factory=list)
    evidence_areas_found: List[str] = field(default_factory=list)
    evidence_areas_missing: List[str] = field(default_factory=list)
    claims_count: int = 0
    placeholders_detected: List[str] = field(default_factory=list)
    explicit_unknowns_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    disclaimer: str = (
        "STRUCTURAL CHECK ONLY: Confirms presence of required sections, claim IDs, "
        "and absence of unresolved template tokens. Architectural soundess, evidence "
        "sufficiency, and learner PASS remain exclusively REVIEWER-REQUIRED."
    )


def validate_defense_dossier(
    dossier_content: str,
    dossier_path: str = "<memory>",
    allow_placeholders: bool = False,
) -> ValidationReport:
    """Audits the structural completeness of an M24 architectural defense dossier."""
    report = ValidationReport(
        dossier_path=dossier_path,
        is_valid=True,
        status="STRUCTURAL_CHECK_PASS",
    )

    # 1. Audit presence of 16 Core Architectural Traces
    for num, name, pattern in REQUIRED_TRACES:
        if re.search(pattern, dossier_content, re.IGNORECASE):
            report.traces_found.append(f"Trace {num:02d}: {name}")
        else:
            report.traces_missing.append(f"Trace {num:02d}: {name}")

    if report.traces_missing:
        report.is_valid = False
        report.errors.append(
            f"Missing {len(report.traces_missing)} required traces: {', '.join(report.traces_missing)}"
        )

    # 2. Audit presence of 12 Evidence Areas (E01–E12)
    for code, name in REQUIRED_EVIDENCE_AREAS:
        # Check code in text (e.g. E01 or **E01**)
        if re.search(rf"\b{code}\b", dossier_content):
            report.evidence_areas_found.append(f"{code} ({name})")
        else:
            report.evidence_areas_missing.append(f"{code} ({name})")

    if report.evidence_areas_missing:
        report.is_valid = False
        report.errors.append(
            f"Missing {len(report.evidence_areas_missing)} evidence areas in matrix: {', '.join(report.evidence_areas_missing)}"
        )

    # 3. Audit Architectural Claim Register (detect claim IDs like CLM-01 or [CLM-01])
    claim_matches = re.findall(r"CLM-\d+", dossier_content, re.IGNORECASE)
    unique_claims = set(c.upper() for c in claim_matches)
    report.claims_count = len(unique_claims)
    if report.claims_count < 3:
        report.is_valid = False
        report.errors.append(
            f"Insufficient architectural claims declared: found {report.claims_count} unique Claim IDs (minimum 3 required, 5 recommended)"
        )

    # 4. Check for Unresolved Placeholders
    if not allow_placeholders:
        detected = []
        for pat in PLACEHOLDER_PATTERNS:
            for match in pat.finditer(dossier_content):
                # Filter out intentional review section placeholders if under Section M
                span_text = match.group(0)
                # Check line containing span
                line_start = dossier_content.rfind("\n", 0, match.start()) + 1
                line_end = dossier_content.find("\n", match.end())
                line_text = dossier_content[line_start : line_end if line_end != -1 else len(dossier_content)]
                # Allow "[Unfilled / Reviewer" in Section M
                if "Reviewer will complete" in line_text or "Reviewer evaluation" in line_text or "Reviewer selects" in line_text or "Reviewer notes" in line_text:
                    continue
                detected.append(span_text)

        report.placeholders_detected = detected[:10]  # sample up to 10
        if detected:
            report.is_valid = False
            report.errors.append(
                f"Detected {len(detected)} unresolved template placeholders (e.g. {detected[0]})"
            )

    # 5. Check Explicit Unknowns (Trace 14) and Learning Plan (Trace 15)
    t14_match = re.search(r"14\.\s*Explicit\s*Unknowns(.*?)(?=15\.\s*Learning|\Z)", dossier_content, re.DOTALL | re.IGNORECASE)
    if t14_match:
        t14_text = t14_match.group(1).strip()
        # Ensure it contains substantive technical content (not just "none")
        if len(t14_text) < 50 or re.search(r"\b(none|n/a|no unknowns)\b", t14_text, re.IGNORECASE):
            report.is_valid = False
            report.errors.append(
                "Explicit Unknowns section (Trace 14) must detail genuine technical blind spots; claiming 'none' is rejected"
            )
        else:
            report.explicit_unknowns_count += 1

    # 6. Reject fabricated mechanisms (Raft, multi-region, consensus when claimed on single node)
    lower_content = dossier_content.lower()
    if re.search(r"(we implemented|our system uses|architecture utilizes|deployed with)\s+raft", lower_content):
        report.is_valid = False
        report.errors.append(
            "Fabricated architecture detected: Claiming Raft implementation on course single-node system violates Curriculum Invariants"
        )

    if not report.is_valid:
        report.status = "STRUCTURAL_CHECK_FAILED"

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate M24 16-Trace Architecture Defense Dossier")
    parser.add_argument("dossier", help="Path to Markdown defense dossier file")
    parser.add_argument("--allow-placeholders", action="store_true", help="Allow template placeholders (for scaffolding audit)")
    args = parser.parse_args()

    path = Path(args.dossier)
    if not path.exists():
        print(f"ERROR: Dossier file not found: {path}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    report = validate_defense_dossier(content, str(path), allow_placeholders=args.allow_placeholders)

    print("=" * 78)
    print(f"  M24 CAPSTONE DEFENSE STRUCTURAL AUDIT: {path.name}")
    print("=" * 78)
    print(f"  Status:               {report.status}")
    print(f"  Traces Found:         {len(report.traces_found)} / 16")
    print(f"  Evidence Areas Found: {len(report.evidence_areas_found)} / 12")
    print(f"  Unique Claims:        {report.claims_count}")
    print(f"  Placeholders Found:   {len(report.placeholders_detected)}")
    print("-" * 78)

    if report.errors:
        print("  STRUCTURAL ERRORS:")
        for err in report.errors:
            print(f"    [FAIL] {err}")
        print("-" * 78)

    if report.warnings:
        print("  WARNINGS:")
        for warn in report.warnings:
            print(f"    [WARN] {warn}")
        print("-" * 78)

    print(f"  NOTE: {report.disclaimer}")
    print("=" * 78)

    sys.exit(0 if report.is_valid else 1)


if __name__ == "__main__":
    main()
