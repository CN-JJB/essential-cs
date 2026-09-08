#!/usr/bin/env python3
"""
activity_l24_02.py — Hands-on Activity for Lesson L24-02 (Pre-Ship Verification)
================================================================================

Provides the runnable harness for evaluating candidate software releases before shipping:
1. Validates risk-prioritized pre-ship evidence matrices (Must Measure, Must Test,
   Must Inspect, Acceptable Unknown).
2. Simulates SQLite database schema migrations to verify backward compatibility and
   test rollback safety vs roll-forward necessity.
3. Audits stated data-loss bounds and ensures zero naive overclaims.

Standard Library Only (PEP 557 dataclasses, json, sqlite3, argparse, pathlib).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Import sibling preship validator
try:
    from preship_validator import (
        simulate_sqlite_schema_evolution,
        validate_risk_matrix_data,
    )
except ImportError:
    from labs.foundations.m24.preship_validator import (
        simulate_sqlite_schema_evolution,
        validate_risk_matrix_data,
    )


def run_migration_simulations() -> None:
    print("=" * 78)
    print("  M24 L24-02 DATABASE SCHEMA MIGRATION & REVERSAL SIMULATIONS")
    print("=" * 78)

    # Simulation 1: Expand phase (Additive column)
    print("\n[SIMULATION 1] Additive Column Migration (Expand Phase)")
    print("  Scenario: Candidate release adds nullable 'summary' column to 'documents' table.")
    ok1, msg1 = simulate_sqlite_schema_evolution(
        initial_ddl="CREATE TABLE documents (id INTEGER PRIMARY KEY, title TEXT, content TEXT);",
        initial_insert="INSERT INTO documents (title, content) VALUES ('Doc 1', 'Content 1');",
        migration_ddl="ALTER TABLE documents ADD COLUMN summary TEXT;",
        old_code_query="SELECT id, title, content FROM documents WHERE id = 1;",
    )
    print(f"  Execution Status: {'PASS' if ok1 else 'FAIL'}")
    print(f"  Old Code Query:   {msg1}")
    print("  Architecture Insight: Old application code ignores new nullable column. Safe to roll back code!")

    # Simulation 2: Destructive rename
    print("\n[SIMULATION 2] Destructive Column Rename Migration")
    print("  Scenario: Candidate release renames 'content' to 'body_text'.")
    ok2, msg2 = simulate_sqlite_schema_evolution(
        initial_ddl="CREATE TABLE documents (id INTEGER PRIMARY KEY, title TEXT, content TEXT);",
        initial_insert="INSERT INTO documents (title, content) VALUES ('Doc 1', 'Content 1');",
        migration_ddl="ALTER TABLE documents RENAME COLUMN content TO body_text;",
        old_code_query="SELECT id, title, content FROM documents WHERE id = 1;",
    )
    print(f"  Execution Status: {'BLOCKED (Expected Incompatibility)' if not ok2 else 'UNEXPECTED'}")
    print(f"  Old Code Query:   {msg2}")
    print("  Architecture Insight: Old application code crashes immediately. Code rollback alone is FORBIDDEN!")
    print("                        Must execute roll-forward fix or explicit migration reversal.")

    # Simulation 3: Destructive NOT NULL without default
    print("\n[SIMULATION 3] Destructive NOT NULL Column without Default")
    print("  Scenario: Candidate release adds 'priority INTEGER NOT NULL' without default value to populated table.")
    ok3, msg3 = simulate_sqlite_schema_evolution(
        initial_ddl="CREATE TABLE documents (id INTEGER PRIMARY KEY, title TEXT, content TEXT);",
        initial_insert="INSERT INTO documents (title, content) VALUES ('Doc 1', 'Content 1');",
        migration_ddl="ALTER TABLE documents ADD COLUMN priority INTEGER NOT NULL;",
        old_code_query="SELECT id, title, content FROM documents WHERE id = 1;",
    )
    print(f"  Execution Status: {'FAIL-CLOSED (Expected DDL Failure)' if not ok3 else 'UNEXPECTED'}")
    print(f"  Migration Output: {msg3}")
    print("  Architecture Insight: SQLite refuses to add non-null columns without defaults to existing rows.")
    print("                        Protects relational integrity at deployment time.")
    print("=" * 78)


def main() -> None:
    parser = argparse.ArgumentParser(description="L24-02 Pre-Ship Verification & Migration Activity Harness")
    parser.add_argument("--matrix", help="Path to pre-ship risk matrix JSON file to audit")
    parser.add_argument("--simulate-migration", action="store_true", help="Execute schema migration compatibility simulations")
    args = parser.parse_args()

    if args.simulate_migration:
        run_migration_simulations()
        return

    matrix_path = Path(args.matrix) if args.matrix else Path(__file__).parent / "sample_preship.json"
    if not matrix_path.exists():
        print(f"ERROR: Matrix file not found: {matrix_path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(matrix_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: Failed to parse matrix JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    report = validate_risk_matrix_data(data, str(matrix_path))

    print("=" * 78)
    print(f"  M24 L24-02 PRE-SHIP RISK MATRIX AUDIT: {matrix_path.name}")
    print("=" * 78)
    print(f"  Status:               {report.status}")
    print(f"  Risk Classes Found:   {len(report.classes_found)} / 4")
    for cls_name, count in report.item_counts.items():
        print(f"    - {cls_name:<20}: {count} items")
    print(f"  Chosen Strategy:      {report.reversal_strategy}")
    print(f"  Stated Data-Loss:     {report.stated_data_loss_bound}")
    print("-" * 78)

    if report.is_valid:
        print("  [SUCCESS] All 4 risk classes are present and populated.")
        print("  [SUCCESS] Reversal strategy is aligned with schema compatibility.")
        print("  [SUCCESS] Stated data-loss bound is explicitly declared.")
    else:
        print("  [FAILED] Pre-ship matrix validation failed:")
        for err in report.errors:
            print(f"    - {err}")

    print("-" * 78)
    print(f"  NOTE: {report.disclaimer}")
    print("=" * 78)

    sys.exit(0 if report.is_valid else 1)


if __name__ == "__main__":
    main()
