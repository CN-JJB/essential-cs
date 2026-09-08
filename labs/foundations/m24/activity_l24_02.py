#!/usr/bin/env python3
"""
activity_l24_02.py — M24 Pre-Ship Structural Activity
=====================================================

Validates a risk-prioritized evidence matrix and runs bounded SQLite DDL/query
compatibility examples. The SQLite examples do not prove whole-application rollback
safety and do not prescribe a universal recovery strategy.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from preship_validator import simulate_sqlite_schema_evolution, validate_risk_matrix_data
except ImportError:
    from labs.foundations.m24.preship_validator import (
        simulate_sqlite_schema_evolution,
        validate_risk_matrix_data,
    )


def run_migration_simulations() -> None:
    scenarios = [
        (
            "Add nullable column",
            "CREATE TABLE documents (id INTEGER PRIMARY KEY, title TEXT, content TEXT);",
            "INSERT INTO documents (title, content) VALUES ('Doc 1', 'Content 1');",
            "ALTER TABLE documents ADD COLUMN summary TEXT;",
            "SELECT id, title, content FROM documents WHERE id = 1;",
        ),
        (
            "Rename a column referenced by the old query",
            "CREATE TABLE documents (id INTEGER PRIMARY KEY, title TEXT, content TEXT);",
            "INSERT INTO documents (title, content) VALUES ('Doc 1', 'Content 1');",
            "ALTER TABLE documents RENAME COLUMN content TO body_text;",
            "SELECT id, title, content FROM documents WHERE id = 1;",
        ),
        (
            "Add NOT NULL column without default to populated table",
            "CREATE TABLE documents (id INTEGER PRIMARY KEY, title TEXT, content TEXT);",
            "INSERT INTO documents (title, content) VALUES ('Doc 1', 'Content 1');",
            "ALTER TABLE documents ADD COLUMN priority INTEGER NOT NULL;",
            "SELECT id, title, content FROM documents WHERE id = 1;",
        ),
    ]

    print("=" * 78)
    print("  M24 SQLITE DDL / OLD-QUERY COMPATIBILITY EXAMPLES")
    print("=" * 78)
    for title, initial_ddl, initial_insert, migration_ddl, old_query in scenarios:
        ok, message = simulate_sqlite_schema_evolution(
            initial_ddl=initial_ddl,
            initial_insert=initial_insert,
            migration_ddl=migration_ddl,
            old_code_query=old_query,
        )
        label = "QUERY_COMPATIBLE" if ok else "QUERY_INCOMPATIBLE_OR_DDL_BLOCKED"
        print(f"  - {title}: {label}")
        print(f"      {message}")
    print("-" * 78)
    print("  NOTE: Results apply only to the exact SQLite DDL/query pairs above.")
    print("  Whole-application recovery strategy remains project- and reviewer-dependent.")
    print("=" * 78)


def main() -> None:
    parser = argparse.ArgumentParser(description="L24-02 pre-ship structural activity")
    parser.add_argument("--matrix", help="Path to pre-ship risk matrix JSON")
    parser.add_argument("--simulate-migration", action="store_true")
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
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Failed to parse matrix JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    report = validate_risk_matrix_data(data, str(matrix_path))
    print("=" * 78)
    print(f"  M24 PRE-SHIP STRUCTURAL AUDIT: {matrix_path.name}")
    print("=" * 78)
    print(f"  Status:             {report.status}")
    print(f"  Risk Classes:       {len(report.classes_found)} / 4")
    print(f"  Recovery Strategy:  {report.recovery_strategy}")
    print(f"  Data-Loss Bound:    {report.stated_data_loss_bound or 'NOT APPLICABLE / SEE RATIONALE'}")
    if report.errors:
        print("-" * 78)
        for error in report.errors:
            print(f"    [FAIL] {error}")
    print("-" * 78)
    print(f"  NOTE: {report.disclaimer}")
    print("=" * 78)
    sys.exit(0 if report.is_valid else 1)


if __name__ == "__main__":
    main()
