#!/usr/bin/env python3
"""
preship_validator.py — M24 Pre-Ship Verification & Risk-Prioritized Matrix Validator
=====================================================================================

Validates the pre-ship verification plan, risk-prioritized evidence matrix, and database
schema migration compatibility for candidate releases.

Audited Invariants:
1. Complete classification across all 4 mandatory risk classes:
   - Must Measure
   - Must Test
   - Must Inspect
   - Acceptable Unknown
2. Rejection of naive overclaims:
   - "100% test coverage = ship safety proof"
   - Universal unqualified "zero data loss" claims
   - Empty or "none" Acceptable Unknown declarations
3. Deployment compatibility & recovery strategy analysis:
   - Separation of application code rollback from database schema evolution
   - Permissibility of code rollback vs requirement of roll-forward or migration reversal
   - Stated data-loss bound requirement
4. Built-in SQLite schema migration compatibility simulation:
   - Tests additive nullable changes (safe rollback) vs destructive changes (broken rollback)

Standard Library Only (sqlite3, json, dataclasses, typing).
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MANDATORY_RISK_CLASSES = [
    "Must Measure",
    "Must Test",
    "Must Inspect",
    "Acceptable Unknown",
]

NAIVE_PHRASES = [
    "100% test coverage means safe to ship",
    "100% coverage ensures zero bugs",
    "guarantees zero data loss in all circumstances",
    "zero data loss under any failure",
    "no unknowns",
    "unknowns: none",
]


@dataclass
class PreShipValidationReport:
    matrix_source: str
    is_valid: bool
    status: str
    classes_found: List[str] = field(default_factory=list)
    classes_missing: List[str] = field(default_factory=list)
    item_counts: Dict[str, int] = field(default_factory=dict)
    reversal_strategy: Optional[str] = None
    stated_data_loss_bound: Optional[str] = None
    migration_simulation_result: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    disclaimer: str = (
        "PRE-SHIP VERIFICATION AUDIT: Confirms presence of mandatory risk-prioritized "
        "evidence classes, deployment recovery rationale, and rejects naive overclaims. "
        "Final candidate release decision remains strictly REVIEWER-REQUIRED."
    )


def validate_risk_matrix_data(data: Dict[str, Any], source_label: str = "<memory>") -> PreShipValidationReport:
    """Validates pre-ship risk matrix JSON/dictionary structure."""
    report = PreShipValidationReport(
        matrix_source=source_label,
        is_valid=True,
        status="PRE_SHIP_VALIDATION_PASS",
    )

    # 1. Audit mandatory risk classes
    matrix = data.get("risk_matrix", {})
    raw_text = json.dumps(data).lower()

    for cls_name in MANDATORY_RISK_CLASSES:
        key = cls_name.lower().replace(" ", "_")
        items = matrix.get(key) or matrix.get(cls_name)
        if items and isinstance(items, list) and len(items) > 0:
            report.classes_found.append(cls_name)
            report.item_counts[cls_name] = len(items)
        else:
            report.classes_missing.append(cls_name)
            report.item_counts[cls_name] = 0

    if report.classes_missing:
        report.is_valid = False
        report.errors.append(
            f"Missing mandatory risk classes: {', '.join(report.classes_missing)}"
        )

    # 2. Check for naive overclaims
    for phrase in NAIVE_PHRASES:
        if phrase in raw_text:
            report.is_valid = False
            report.errors.append(
                f"Naive overclaim detected ('{phrase}'). Curriculum Invariants reject universal "
                "safety claims and unqualified zero-data-loss assertions."
            )

    # 3. Check Acceptable Unknown substantiation
    au_key = "acceptable_unknown"
    au_items = matrix.get(au_key) or matrix.get("Acceptable Unknown", [])
    if au_items:
        for idx, item in enumerate(au_items):
            desc = item.get("description", "") if isinstance(item, dict) else str(item)
            if len(desc.strip()) < 15 or desc.strip().lower() in ["none", "n/a", "no unknowns"]:
                report.is_valid = False
                report.errors.append(
                    f"Acceptable Unknown entry {idx+1} is empty or trivial ('{desc}'). "
                    "Must state an explicit, bounded technical uncertainty outside current scope."
                )

    # 4. Check Deployment Compatibility & Recovery Strategy
    deploy = data.get("deployment_compatibility", {})
    report.reversal_strategy = deploy.get("chosen_recovery_strategy")
    report.stated_data_loss_bound = deploy.get("stated_data_loss_bound")

    valid_strategies = ["Code Rollback", "Roll-Forward", "Migration Reversal", "Snapshot Recovery"]
    if not report.reversal_strategy or report.reversal_strategy not in valid_strategies:
        report.is_valid = False
        report.errors.append(
            f"Invalid or missing recovery strategy '{report.reversal_strategy}'. "
            f"Must be one of: {', '.join(valid_strategies)}"
        )

    if not report.stated_data_loss_bound or len(report.stated_data_loss_bound.strip()) < 10:
        report.is_valid = False
        report.errors.append(
            "Missing explicit stated data-loss bound. Systems must clearly state the maximum "
            "data-loss window under failure (e.g., 'zero loss for committed WAL frames, un-fsynced writes aborted')."
        )

    # 5. Schema compatibility logic check
    schema_compat = deploy.get("schema_compatibility_type")
    if schema_compat == "Destructive" and report.reversal_strategy == "Code Rollback":
        report.is_valid = False
        report.errors.append(
            "Fatal deployment strategy mismatch: Schema change is marked 'Destructive', but chosen "
            "recovery strategy is 'Code Rollback'. Rolling back code against destructive schema changes "
            "causes runtime exceptions. Requires Roll-Forward, Migration Reversal, or Snapshot Recovery."
        )

    if not report.is_valid:
        report.status = "PRE_SHIP_VALIDATION_FAILED"

    return report


def simulate_sqlite_schema_evolution(
    initial_ddl: str,
    initial_insert: str,
    migration_ddl: str,
    old_code_query: str,
) -> Tuple[bool, str]:
    """
    Simulates a database schema evolution and checks whether old application code
    can still execute its baseline queries after the migration (backward compatibility check).
    """
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    try:
        # Step 1: Initial schema
        cur.executescript(initial_ddl)
        cur.executescript(initial_insert)
        conn.commit()

        # Step 2: Apply candidate migration
        try:
            cur.executescript(migration_ddl)
            conn.commit()
        except sqlite3.OperationalError as exc:
            return False, f"Migration DDL failed to execute: {exc}"

        # Step 3: Simulate old code running against migrated schema
        try:
            cur.execute(old_code_query)
            rows = cur.fetchall()
            return True, f"Backward compatible: Old code query succeeded, retrieved {len(rows)} rows."
        except sqlite3.OperationalError as exc:
            return False, f"Backward incompatibility detected! Old code failed with: {exc}"

    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate M24 Pre-Ship Verification Matrix and Migration Compatibility")
    parser.add_argument("--matrix", help="Path to JSON pre-ship verification matrix")
    parser.add_argument("--simulate-migration", action="store_true", help="Run SQLite migration compatibility demonstration")
    args = parser.parse_args()

    if args.simulate_migration:
        print("=" * 78)
        print("  M24 SQLITE SCHEMA MIGRATION COMPATIBILITY SIMULATION")
        print("=" * 78)

        # Simulation 1: Additive nullable column (Backward compatible -> Code rollback safe)
        print("\n[SCENARIO 1] Additive Nullable Column (Expand Phase)")
        ok1, msg1 = simulate_sqlite_schema_evolution(
            initial_ddl="CREATE TABLE docs (id INTEGER PRIMARY KEY, title TEXT, body TEXT);",
            initial_insert="INSERT INTO docs (title, body) VALUES ('First Doc', 'Hello world');",
            migration_ddl="ALTER TABLE docs ADD COLUMN tags TEXT;",
            old_code_query="SELECT id, title, body FROM docs WHERE id = 1;",
        )
        print(f"  Result: {'PASS' if ok1 else 'FAIL'} — {msg1}")
        print("  Inference: Additive changes allow safe application code rollback.")

        # Simulation 2: Destructive column rename (Incompatible -> Code rollback breaks)
        print("\n[SCENARIO 2] Destructive Column Rename")
        ok2, msg2 = simulate_sqlite_schema_evolution(
            initial_ddl="CREATE TABLE docs (id INTEGER PRIMARY KEY, title TEXT, body TEXT);",
            initial_insert="INSERT INTO docs (title, body) VALUES ('First Doc', 'Hello world');",
            migration_ddl="ALTER TABLE docs RENAME COLUMN title TO doc_title;",
            old_code_query="SELECT id, title, body FROM docs WHERE id = 1;",
        )
        print(f"  Result: {'PASS (Expected Incompatibility)' if not ok2 else 'UNEXPECTED'} — {msg2}")
        print("  Inference: Destructive changes break code rollback; requires Roll-Forward or Migration Reversal.")

        # Simulation 3: Destructive NOT NULL without default (DDL fails immediately)
        print("\n[SCENARIO 3] Destructive NOT NULL Column without Default")
        ok3, msg3 = simulate_sqlite_schema_evolution(
            initial_ddl="CREATE TABLE docs (id INTEGER PRIMARY KEY, title TEXT, body TEXT);",
            initial_insert="INSERT INTO docs (title, body) VALUES ('First Doc', 'Hello world');",
            migration_ddl="ALTER TABLE docs ADD COLUMN version INTEGER NOT NULL;",
            old_code_query="SELECT id, title, body FROM docs WHERE id = 1;",
        )
        print(f"  Result: {'PASS (Expected DDL Failure)' if not ok3 else 'UNEXPECTED'} — {msg3}")
        print("  Inference: Adding NOT NULL columns to populated tables without defaults fails closed.")
        print("=" * 78)
        return

    if not args.matrix:
        parser.print_help()
        sys.exit(1)

    path = Path(args.matrix)
    if not path.exists():
        print(f"ERROR: Matrix file not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: Failed to parse matrix JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    report = validate_risk_matrix_data(data, str(path))

    print("=" * 78)
    print(f"  M24 PRE-SHIP RISK MATRIX AUDIT: {path.name}")
    print("=" * 78)
    print(f"  Status:               {report.status}")
    print(f"  Classes Found:        {len(report.classes_found)} / 4")
    for cls_name, count in report.item_counts.items():
        print(f"    - {cls_name:<20}: {count} items")
    print(f"  Recovery Strategy:    {report.reversal_strategy}")
    print(f"  Data-Loss Bound:      {report.stated_data_loss_bound}")
    print("-" * 78)

    if report.errors:
        print("  VALIDATION ERRORS:")
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
