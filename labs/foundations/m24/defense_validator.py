#!/usr/bin/env python3
"""
defense_validator.py — M24 Architecture Defense Dossier Structural Validator
=============================================================================

Machine-checkable scope only:
1. Exact Markdown headings for all 16 Core Architectural Traces.
2. A Claim Register with substantive claim/evidence/artifact/assumption/inference fields.
3. A 12-row E01–E12 traceability matrix whose claim references resolve.
4. Explicit Unknown IDs linked to Learning Plan entries.
5. Unresolved placeholder detection.

The validator intentionally does NOT decide whether an architecture, evidence artifact,
technology choice, or changed-constraint response is semantically correct. It does not
blacklist mechanism names. Only a reviewer can judge whether a claimed mechanism is
actually present in the learner's system.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

REQUIRED_TRACES: List[Tuple[int, str]] = [
    (1, "Request Trace"),
    (2, "Data & State Trace"),
    (3, "Control & Authority Trace"),
    (4, "State Inventory"),
    (5, "Invariants & Specifications"),
    (6, "Trust Boundaries"),
    (7, "Isolation Boundaries"),
    (8, "Failure & Risk Walkthrough"),
    (9, "Security & Privacy Decisions"),
    (10, "Measurements & Performance Evidence"),
    (11, "Cost & Scale Estimates"),
    (12, "Alternatives Considered"),
    (13, "When-Not-To-Use & Rejected Choices"),
    (14, "Explicit Unknowns"),
    (15, "Learning Plan"),
    (16, "Changed-Constraint Adaptation"),
]

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

PLACEHOLDER_PATTERNS = [
    re.compile(r"\[TODO[^\]]*\]", re.IGNORECASE),
    re.compile(r"\[(?:Record|State|Detail|List|Describe|Identify|Explain|Provide|Estimate|Calculate)[^\]]+\]", re.IGNORECASE),
    re.compile(r"\[Unfilled[^\]]*\]", re.IGNORECASE),
    re.compile(r"\[待[^\]]*\]", re.IGNORECASE),
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
    evidence_rows_valid: int = 0
    dangling_claim_refs: List[str] = field(default_factory=list)
    explicit_unknown_ids: List[str] = field(default_factory=list)
    learning_plan_linked_ids: List[str] = field(default_factory=list)
    placeholders_detected: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    disclaimer: str = (
        "STRUCTURAL CHECK ONLY: validates required headings and traceability fields. "
        "Architecture quality, artifact truth, evidence sufficiency, changed-constraint "
        "reasoning, and learner PASS remain exclusively REVIEWER-REQUIRED."
    )


def _table_cells(line: str) -> List[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _substantive(value: str, minimum: int = 3) -> bool:
    stripped = value.strip().strip(chr(96))
    if len(stripped) < minimum:
        return False
    if re.fullmatch(r"(?:n/?a|none|unknown|tbd|-)", stripped, re.IGNORECASE):
        return False
    return True


def _trace_section(content: str, number: int, next_number: int | None) -> str:
    start = re.search(rf"(?im)^###\s+{number}\.\s+[^\n]+$", content)
    if not start:
        return ""
    if next_number is None:
        return content[start.end():]
    tail = content[start.end():]
    end = re.search(rf"(?im)^###\s+{next_number}\.\s+[^\n]+$", tail)
    return tail[: end.start()] if end else tail


def _claim_register_section(content: str) -> str:
    """Return only the `## Architectural Claim Register` section (up to the next peer `##` heading)."""
    start = re.search(r"(?im)^##\s+Architectural Claim Register\s*$", content)
    if not start:
        return ""
    tail = content[start.end():]
    end = re.search(r"(?m)^##\s+", tail)
    return tail[: end.start()] if end else tail


def validate_defense_dossier(
    dossier_content: str,
    dossier_path: str = "<memory>",
    allow_placeholders: bool = False,
) -> ValidationReport:
    report = ValidationReport(dossier_path=dossier_path, is_valid=True, status="STRUCTURAL_CHECK_PASS")

    for num, name in REQUIRED_TRACES:
        pattern = rf"(?im)^###\s+{num}\.\s*{re.escape(name)}\s*$"
        if re.search(pattern, dossier_content):
            report.traces_found.append(f"Trace {num:02d}: {name}")
        else:
            report.traces_missing.append(f"Trace {num:02d}: {name}")
    if report.traces_missing:
        report.is_valid = False
        report.errors.append("Missing required trace headings: " + ", ".join(report.traces_missing))

    claim_rows: Dict[str, List[str]] = {}
    register_section = _claim_register_section(dossier_content)
    for line in register_section.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        match = re.search(r"\bCLM-\d+\b", line, re.IGNORECASE)
        if not match:
            continue
        cells = _table_cells(line)
        claim_id = match.group(0).upper()
        if len(cells) < 7:
            report.is_valid = False
            report.errors.append(f"{claim_id} claim row has fewer than 7 required columns")
            continue
        claim_rows[claim_id] = cells
        for idx, label in (
            (1, "claim"),
            (2, "evidence category"),
            (3, "artifact reference"),
            (4, "assumption"),
            (5, "inference limit"),
            (6, "status"),
        ):
            minimum = 5 if idx in (1, 4, 5) else 2
            if not _substantive(cells[idx], minimum):
                report.is_valid = False
                report.errors.append(f"{claim_id} has empty/trivial {label}")

    report.claims_count = len(claim_rows)
    if report.claims_count < 5:
        report.is_valid = False
        report.errors.append(
            f"Architectural Claim Register contains {report.claims_count} claims; L24-01 requires at least 5 substantive claims"
        )

    evidence_rows: Dict[str, List[str]] = {}
    known_claims: Set[str] = set(claim_rows)
    expected_codes = {code for code, _ in REQUIRED_EVIDENCE_AREAS}
    for line in dossier_content.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        match = re.match(r"^\s*\|\s*\*?\*?(E\d{2})\*?\*?\s*\|", line, re.IGNORECASE)
        if not match:
            continue
        area = match.group(1).upper()
        if area not in expected_codes:
            continue
        cells = _table_cells(line)
        if len(cells) < 6:
            report.is_valid = False
            report.errors.append(f"{area} traceability row has fewer than 6 required columns")
            continue
        evidence_rows[area] = cells
        claim_refs = {c.upper() for c in re.findall(r"CLM-\d+", cells[2], re.IGNORECASE)}
        if not claim_refs:
            report.is_valid = False
            report.errors.append(f"{area} does not reference any Claim ID")
        dangling = sorted(claim_refs - known_claims)
        if dangling:
            report.is_valid = False
            report.dangling_claim_refs.extend(dangling)
            report.errors.append(f"{area} references unknown claim IDs: {', '.join(dangling)}")
        if not _substantive(cells[3], 3):
            report.is_valid = False
            report.errors.append(f"{area} is missing an artifact/reference field")
        if not _substantive(cells[4], 8):
            report.is_valid = False
            report.errors.append(f"{area} is missing a substantive evidence-sufficiency summary")
        if not _substantive(cells[5], 8):
            report.is_valid = False
            report.errors.append(f"{area} is missing an explicit inference limit")

    report.evidence_areas_found = [
        f"{code} ({name})" for code, name in REQUIRED_EVIDENCE_AREAS if code in evidence_rows
    ]
    report.evidence_areas_missing = [
        f"{code} ({name})" for code, name in REQUIRED_EVIDENCE_AREAS if code not in evidence_rows
    ]
    report.evidence_rows_valid = len(evidence_rows)
    if report.evidence_areas_missing:
        report.is_valid = False
        report.errors.append("Missing evidence matrix rows: " + ", ".join(report.evidence_areas_missing))

    unknown_text = _trace_section(dossier_content, 14, 15)
    plan_text = _trace_section(dossier_content, 15, 16)
    unknown_ids = sorted({u.upper() for u in re.findall(r"UNK-\d+", unknown_text, re.IGNORECASE)})
    plan_ids = sorted({u.upper() for u in re.findall(r"UNK-\d+", plan_text, re.IGNORECASE)})
    report.explicit_unknown_ids = unknown_ids
    report.learning_plan_linked_ids = sorted(set(unknown_ids) & set(plan_ids))
    if not unknown_ids:
        report.is_valid = False
        report.errors.append("Trace 14 must declare at least one explicit unknown with an UNK-xx identifier")
    unlinked = sorted(set(unknown_ids) - set(plan_ids))
    if unlinked:
        report.is_valid = False
        report.errors.append("Learning Plan does not link these explicit unknown IDs: " + ", ".join(unlinked))

    if not allow_placeholders:
        detected: List[str] = []
        for pat in PLACEHOLDER_PATTERNS:
            for match in pat.finditer(dossier_content):
                line_start = dossier_content.rfind("\n", 0, match.start()) + 1
                line_end = dossier_content.find("\n", match.end())
                line_text = dossier_content[line_start: line_end if line_end != -1 else len(dossier_content)]
                if any(token in line_text for token in (
                    "Reviewer will complete",
                    "Reviewer evaluation",
                    "Reviewer selects",
                    "Reviewer notes",
                )):
                    continue
                detected.append(match.group(0))
        report.placeholders_detected = detected[:10]
        if detected:
            report.is_valid = False
            report.errors.append(
                f"Detected {len(detected)} unresolved learner/template placeholders (e.g. {detected[0]})"
            )

    if not report.is_valid:
        report.status = "STRUCTURAL_CHECK_FAILED"
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate M24 Architecture Defense Dossier structure and traceability")
    parser.add_argument("dossier", help="Path to Markdown defense dossier file")
    parser.add_argument("--allow-placeholders", action="store_true", help="Allow learner placeholders for scaffolding audit")
    args = parser.parse_args()

    path = Path(args.dossier)
    if not path.exists():
        print(f"ERROR: Dossier file not found: {path}", file=sys.stderr)
        sys.exit(1)

    report = validate_defense_dossier(path.read_text(encoding="utf-8"), str(path), args.allow_placeholders)
    print("=" * 78)
    print(f"  M24 CAPSTONE DEFENSE STRUCTURAL AUDIT: {path.name}")
    print("=" * 78)
    print(f"  Status:               {report.status}")
    print(f"  Traces Found:         {len(report.traces_found)} / 16")
    print(f"  Evidence Rows:        {report.evidence_rows_valid} / 12")
    print(f"  Unique Claims:        {report.claims_count}")
    print(f"  Unknowns Linked:      {len(report.learning_plan_linked_ids)} / {len(report.explicit_unknown_ids)}")
    print(f"  Placeholders Found:   {len(report.placeholders_detected)}")
    if report.errors:
        print("-" * 78)
        for err in report.errors:
            print(f"    [FAIL] {err}")
    print("-" * 78)
    print(f"  NOTE: {report.disclaimer}")
    print("=" * 78)
    sys.exit(0 if report.is_valid else 1)


if __name__ == "__main__":
    main()
