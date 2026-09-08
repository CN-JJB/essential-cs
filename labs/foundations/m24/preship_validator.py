#!/usr/bin/env python3
"""
preship_validator.py — M24 Pre-Ship Risk-Matrix Structural Validator
====================================================================

Machine-checkable scope:
- all four risk classes exist;
- each item records severity, criticality, evidence gap, and blast radius;
- deployment compatibility and recovery-analysis fields are substantive;
- a data-loss bound is stated when applicable, or an explicit not-applicable rationale exists;
- naive universal claims are rejected;
- SQLite migration examples test only the exact DDL/query pair they execute.

The validator does not prescribe a universal recovery strategy or decide release readiness.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MANDATORY_RISK_CLASSES = ["Must Measure", "Must Test", "Must Inspect", "Acceptable Unknown"]
NAIVE_PHRASES = [
    "100% test coverage means safe to ship",
    "100% coverage ensures zero bugs",
    "guarantees zero data loss in all circumstances",
    "zero data loss under any failure",
    "no unknowns",
    "unknowns: none",
]
COMMON_RISK_FIELDS = ("id", "severity", "criticality", "evidence_gap", "blast_radius_if_omitted")
ACTION_RISK_FIELDS = ("target", "methodology", "success_criterion")
UNKNOWN_RISK_FIELDS = ("description", "justification")


@dataclass
class PreShipValidationReport:
    matrix_source: str
    is_valid: bool
    status: str
    classes_found: List[str] = field(default_factory=list)
    classes_missing: List[str] = field(default_factory=list)
    item_counts: Dict[str, int] = field(default_factory=dict)
    recovery_strategy: Optional[str] = None
    stated_data_loss_bound: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    disclaimer: str = (
        "STRUCTURAL PRE-SHIP CHECK ONLY: confirms risk-class fields and recovery-analysis "
        "inputs. Risk priority, recovery-strategy adequacy, evidence sufficiency, and the "
        "candidate release decision remain REVIEWER-REQUIRED."
    )


def _substantive(value: Any, minimum: int = 3) -> bool:
    if value is None:
        return False
    text = str(value).strip()
    if len(text) < minimum:
        return False
    return text.lower() not in {"none", "n/a", "tbd", "-", "unknown"}


def _validate_item_fields(
    report: PreShipValidationReport,
    class_name: str,
    item: Any,
    index: int,
) -> None:
    if not isinstance(item, dict):
        report.is_valid = False
        report.errors.append(f"{class_name} item {index} must be an object with explicit risk fields")
        return
    required = list(COMMON_RISK_FIELDS)
    required.extend(UNKNOWN_RISK_FIELDS if class_name == "Acceptable Unknown" else ACTION_RISK_FIELDS)
    for field_name in required:
        if not _substantive(item.get(field_name), 2 if field_name == "id" else 5):
            report.is_valid = False
            report.errors.append(f"{class_name} item {index} is missing or trivial field '{field_name}'")


def validate_risk_matrix_data(data: Dict[str, Any], source_label: str = "<memory>") -> PreShipValidationReport:
    report = PreShipValidationReport(
        matrix_source=source_label,
        is_valid=True,
        status="PRE_SHIP_STRUCTURAL_CHECK_PASS",
    )

    matrix = data.get("risk_matrix", {})
    raw_text = json.dumps(data, sort_keys=True).lower()

    for class_name in MANDATORY_RISK_CLASSES:
        key = class_name.lower().replace(" ", "_")
        items = matrix.get(key)
        if not isinstance(items, list) or not items:
            report.classes_missing.append(class_name)
            report.item_counts[class_name] = 0
            continue
        report.classes_found.append(class_name)
        report.item_counts[class_name] = len(items)
        for idx, item in enumerate(items, start=1):
            _validate_item_fields(report, class_name, item, idx)

    if report.classes_missing:
        report.is_valid = False
        report.errors.append("Missing mandatory risk classes: " + ", ".join(report.classes_missing))

    for phrase in NAIVE_PHRASES:
        if phrase in raw_text:
            report.is_valid = False
            report.errors.append(
                f"Naive universal overclaim detected ('{phrase}'); structure cannot convert it into ship-safety evidence"
            )

    deploy = data.get("deployment_compatibility", {})
    for field_name in (
        "app_code_compatibility",
        "schema_compatibility_analysis",
        "chosen_recovery_strategy",
        "recovery_justification",
        "reversal_verification_evidence",
    ):
        if not _substantive(deploy.get(field_name), 10):
            report.is_valid = False
            report.errors.append(f"deployment_compatibility is missing substantive '{field_name}'")

    report.recovery_strategy = deploy.get("chosen_recovery_strategy")

    data_loss_applicable = deploy.get("data_loss_applicable")
    if not isinstance(data_loss_applicable, bool):
        report.is_valid = False
        report.errors.append("deployment_compatibility.data_loss_applicable must be true or false")
    elif data_loss_applicable:
        report.stated_data_loss_bound = deploy.get("stated_data_loss_bound")
        if not _substantive(report.stated_data_loss_bound, 12):
            report.is_valid = False
            report.errors.append("Data loss is applicable but no substantive stated_data_loss_bound is provided")
    elif not _substantive(deploy.get("data_loss_not_applicable_reason"), 12):
        report.is_valid = False
        report.errors.append(
            "Data loss is marked not applicable but data_loss_not_applicable_reason is missing or trivial"
        )

    if not report.is_valid:
        report.status = "PRE_SHIP_STRUCTURAL_CHECK_FAILED"
    return report


def simulate_sqlite_schema_evolution(
    initial_ddl: str,
    initial_insert: str,
    migration_ddl: str,
    old_code_query: str,
) -> Tuple[bool, str]:
    """Run one bounded SQLite migration and test one explicit old-code query afterward."""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    try:
        cur.executescript(initial_ddl)
        cur.executescript(initial_insert)
        conn.commit()
        try:
            cur.executescript(migration_ddl)
            conn.commit()
        except sqlite3.Error as exc:
            return False, f"Migration statement failed in this SQLite fixture: {exc}"
        try:
            cur.execute(old_code_query)
            rows = cur.fetchall()
            return True, (
                f"Fixture query remained compatible after this migration; retrieved {len(rows)} rows. "
                "This does not prove whole-application rollback safety."
            )
        except sqlite3.Error as exc:
            return False, f"Fixture old-code query became incompatible after migration: {exc}"
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate M24 pre-ship risk matrix structure")
    parser.add_argument("--matrix", help="Path to JSON pre-ship verification matrix")
    parser.add_argument("--simulate-migration", action="store_true", help="Run bounded SQLite compatibility examples")
    args = parser.parse_args()

    if args.simulate_migration:
        scenarios = [
            (
                "Add nullable column",
                "CREATE TABLE docs (id INTEGER PRIMARY KEY, title TEXT, body TEXT);",
                "INSERT INTO docs (title, body) VALUES ('First Doc', 'Hello world');",
                "ALTER TABLE docs ADD COLUMN tags TEXT;",
                "SELECT id, title, body FROM docs WHERE id = 1;",
            ),
            (
                "Rename a column used by old query",
                "CREATE TABLE docs (id INTEGER PRIMARY KEY, title TEXT, body TEXT);",
                "INSERT INTO docs (title, body) VALUES ('First Doc', 'Hello world');",
                "ALTER TABLE docs RENAME COLUMN title TO doc_title;",
                "SELECT id, title, body FROM docs WHERE id = 1;",
            ),
            (
                "Add NOT NULL column without default to populated table",
                "CREATE TABLE docs (id INTEGER PRIMARY KEY, title TEXT, body TEXT);",
                "INSERT INTO docs (title, body) VALUES ('First Doc', 'Hello world');",
                "ALTER TABLE docs ADD COLUMN version INTEGER NOT NULL;",
                "SELECT id, title, body FROM docs WHERE id = 1;",
            ),
        ]
        print("=" * 78)
        print("  M24 SQLITE MIGRATION COMPATIBILITY EXAMPLES")
        print("=" * 78)
        for title, ddl, insert, migration, old_query in scenarios:
            ok, msg = simulate_sqlite_schema_evolution(ddl, insert, migration, old_query)
            print(f"  - {title}: {'QUERY_COMPATIBLE' if ok else 'QUERY_INCOMPATIBLE_OR_DDL_BLOCKED'}")
            print(f"      {msg}")
        print("  NOTE: These examples test only the listed DDL/query pairs; they do not prescribe a universal recovery strategy.")
        return

    if not args.matrix:
        parser.error("--matrix is required unless --simulate-migration is used")
    path = Path(args.matrix)
    if not path.exists():
        print(f"ERROR: Matrix file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Failed to parse matrix JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    report = validate_risk_matrix_data(data, str(path))
    print("=" * 78)
    print(f"  M24 PRE-SHIP STRUCTURAL AUDIT: {path.name}")
    print("=" * 78)
    print(f"  Status:             {report.status}")
    print(f"  Risk Classes:       {len(report.classes_found)} / 4")
    print(f"  Recovery Strategy:  {report.recovery_strategy}")
    print(f"  Data-Loss Bound:    {report.stated_data_loss_bound or 'NOT APPLICABLE / SEE RATIONALE'}")
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
