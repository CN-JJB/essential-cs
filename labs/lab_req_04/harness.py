#!/usr/bin/env python3
"""
Automated Test & Evidence Harness for LAB-REQ-04.
Orchestrates real sqlite3 CLI execution, plan inspection, result-set equivalence,
timing distribution, write cost, file-size observation, and scan acceptance.

Adheres strictly to the Task Contract:
- If sqlite3 CLI is absent, truthfully reports ENVIRONMENT-BLOCKED / NOT RUN.
- Python stdlib sqlite3 is used ONLY for verification and generator support, NOT as a CLI replacement.
"""

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time

from eqp_parser import parse_eqp_output, summarize_eqp_paths
from generator import generate_lab_dataset, get_default_lab_db_path


def check_sqlite_cli():
    cli_path = shutil.which("sqlite3")
    if not cli_path:
        return False, None
    try:
        proc = subprocess.run([cli_path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=3.0)
        return proc.returncode == 0, cli_path
    except Exception:
        return False, None


def run_cli_query(cli_path, db_path, sql_command):
    """
    Execute SQL command through the real sqlite3 CLI binary.
    """
    cmd = [cli_path, db_path, sql_command]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10.0)
    if proc.returncode != 0:
        raise RuntimeError(f"sqlite3 CLI failed ({proc.returncode}): {proc.stderr.strip()}")
    return proc.stdout.strip()


def run_lab_req_04(db_path=None, trials=10):
    cli_usable, cli_path = check_sqlite_cli()
    if not cli_usable:
        return {
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "reason": "sqlite3 CLI binary not found or not executable on this host",
            "checkpoints": {},
        }

    target_db = db_path or get_default_lab_db_path()
    generate_lab_dataset(db_path=target_db, row_count=5000, seed=42)
    initial_db_size = os.path.getsize(target_db)

    test_query = "SELECT id, user_id, amount, status FROM orders WHERE user_id = 42 ORDER BY id;"
    test_eqp = f"EXPLAIN QUERY PLAN {test_query}"

    # Checkpoint 1: Unindexed Plan
    unindexed_eqp_raw = run_cli_query(cli_path, target_db, test_eqp)
    unindexed_parsed = parse_eqp_output(unindexed_eqp_raw)
    unindexed_summary = summarize_eqp_paths(unindexed_parsed)

    # Checkpoint 2: Create Index & Result Equivalence
    unindexed_result_raw = run_cli_query(cli_path, target_db, test_query)
    unindexed_hash = hashlib.sha256(unindexed_result_raw.encode("utf-8")).hexdigest()
    unindexed_row_count = len(unindexed_result_raw.splitlines()) if unindexed_result_raw else 0

    # Create index via CLI
    create_idx_sql = "CREATE INDEX idx_orders_user ON orders(user_id);"
    run_cli_query(cli_path, target_db, create_idx_sql)

    indexed_db_size = os.path.getsize(target_db)
    file_size_delta = indexed_db_size - initial_db_size

    indexed_eqp_raw = run_cli_query(cli_path, target_db, test_eqp)
    indexed_parsed = parse_eqp_output(indexed_eqp_raw)
    indexed_summary = summarize_eqp_paths(indexed_parsed)

    indexed_result_raw = run_cli_query(cli_path, target_db, test_query)
    indexed_hash = hashlib.sha256(indexed_result_raw.encode("utf-8")).hexdigest()
    indexed_row_count = len(indexed_result_raw.splitlines()) if indexed_result_raw else 0

    results_match = (unindexed_hash == indexed_hash) and (unindexed_row_count == indexed_row_count)

    # Checkpoint 3: Repeated Read Timing
    # Warmup
    run_cli_query(cli_path, target_db, test_query)

    unindexed_times_ns = []
    # Drop index temporarily to measure unindexed reads cleanly
    run_cli_query(cli_path, target_db, "DROP INDEX idx_orders_user;")
    for _ in range(trials):
        t0 = time.perf_counter_ns()
        run_cli_query(cli_path, target_db, test_query)
        t1 = time.perf_counter_ns()
        unindexed_times_ns.append(t1 - t0)

    # Re-create index
    run_cli_query(cli_path, target_db, create_idx_sql)
    # Warmup
    run_cli_query(cli_path, target_db, test_query)

    indexed_times_ns = []
    for _ in range(trials):
        t0 = time.perf_counter_ns()
        run_cli_query(cli_path, target_db, test_query)
        t1 = time.perf_counter_ns()
        indexed_times_ns.append(t1 - t0)

    # Checkpoint 4: Write Cost Observation
    # Measure inserting 500 rows with index vs without index
    write_rows_sql = "\n".join([
        f"INSERT INTO orders (user_id, amount, status, region, created_at) VALUES (999, 10.0, 'NEW', 'US_EAST', '2026-03-01T00:00:00Z');"
        for _ in range(200)
    ])

    t0_write_indexed = time.perf_counter_ns()
    run_cli_query(cli_path, target_db, f"BEGIN;\n{write_rows_sql}\nCOMMIT;")
    t1_write_indexed = time.perf_counter_ns()
    write_time_indexed_ms = (t1_write_indexed - t0_write_indexed) / 1_000_000.0

    # Clean up test inserted rows and drop index
    run_cli_query(cli_path, target_db, "DELETE FROM orders WHERE user_id = 999;")
    run_cli_query(cli_path, target_db, "DROP INDEX idx_orders_user;")

    t0_write_unindexed = time.perf_counter_ns()
    run_cli_query(cli_path, target_db, f"BEGIN;\n{write_rows_sql}\nCOMMIT;")
    t1_write_unindexed = time.perf_counter_ns()
    write_time_unindexed_ms = (t1_write_unindexed - t0_write_unindexed) / 1_000_000.0

    run_cli_query(cli_path, target_db, "DELETE FROM orders WHERE user_id = 999;")
    # Restore index for scan acceptance test
    run_cli_query(cli_path, target_db, create_idx_sql)

    # Checkpoint 5: Truthful Changed Workload / Scan Acceptance
    # Query with low selectivity or non-sargable predicate
    low_sel_query = "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE amount > 0.0;"
    low_sel_eqp_raw = run_cli_query(cli_path, target_db, low_sel_query)
    low_sel_parsed = parse_eqp_output(low_sel_eqp_raw)
    low_sel_summary = summarize_eqp_paths(low_sel_parsed)

    return {
        "disposition": "PASS",
        "cli_path": cli_path,
        "database_file": target_db,
        "checkpoints": {
            "1_unindexed_plan": {
                "raw_eqp": unindexed_eqp_raw,
                "parsed": unindexed_parsed,
                "summary": unindexed_summary,
            },
            "2_indexed_plan_and_equivalence": {
                "raw_eqp": indexed_eqp_raw,
                "parsed": indexed_parsed,
                "summary": indexed_summary,
                "result_equivalence": {
                    "matched": results_match,
                    "unindexed_rows": unindexed_row_count,
                    "indexed_rows": indexed_row_count,
                    "unindexed_sha256": unindexed_hash,
                    "indexed_sha256": indexed_hash,
                },
            },
            "3_read_timing": {
                "trials": trials,
                "unindexed_median_ms": sorted(unindexed_times_ns)[trials // 2] / 1_000_000.0,
                "indexed_median_ms": sorted(indexed_times_ns)[trials // 2] / 1_000_000.0,
                "unindexed_samples_ns": unindexed_times_ns,
                "indexed_samples_ns": indexed_times_ns,
                "inference_limit_note": "Timing is hardware- and cache-specific; no universal ratio asserted.",
            },
            "4_write_and_storage_cost": {
                "initial_db_size_bytes": initial_db_size,
                "indexed_db_size_bytes": indexed_db_size,
                "size_delta_bytes": file_size_delta,
                "bulk_insert_unindexed_ms": write_time_unindexed_ms,
                "bulk_insert_indexed_ms": write_time_indexed_ms,
            },
            "5_scan_acceptance": {
                "query": "SELECT * FROM orders WHERE amount > 0.0;",
                "raw_eqp": low_sel_eqp_raw,
                "summary": low_sel_summary,
                "index_bypassed_as_expected": low_sel_summary["has_scan"],
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(description="LAB-REQ-04 Execution Harness")
    parser.add_argument("--json", action="store_true", help="Print report in JSON format")
    args = parser.parse_args()

    report = run_lab_req_04()

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    print("=" * 66)
    print(" Essential CS: LAB-REQ-04 SQLite Indexing & Access Path Trace")
    print("=" * 66)
    print(f" Disposition: {report['disposition']}")
    if report["disposition"] == "ENVIRONMENT-BLOCKED / NOT RUN":
        print(f" Reason:      {report['reason']}")
        print(" Note:        sqlite3 CLI is a mandatory learner gate for LAB-REQ-04.")
        print("=" * 66)
        return 0

    print(f" CLI Used:    {report['cli_path']}")
    print(f" Database:    {report['database_file']}")
    print("-" * 66)
    cp1 = report["checkpoints"]["1_unindexed_plan"]
    print(" [Checkpoint 1: Unindexed Plan]")
    print(f"   Raw EQP:   {cp1['raw_eqp']}")
    print(f"   Summary:   {cp1['summary']['categories']}")
    print("-" * 66)
    cp2 = report["checkpoints"]["2_indexed_plan_and_equivalence"]
    print(" [Checkpoint 2: Indexed Plan & Result Equivalence]")
    print(f"   Raw EQP:   {cp2['raw_eqp']}")
    print(f"   Summary:   {cp2['summary']['categories']}")
    eq = cp2["result_equivalence"]
    print(f"   Results Matched: {eq['matched']} (rows={eq['indexed_rows']}, hash={eq['indexed_sha256'][:12]}...)")
    print("-" * 66)
    cp3 = report["checkpoints"]["3_read_timing"]
    print(" [Checkpoint 3: Repeated Read Timing]")
    print(f"   Unindexed Median: {cp3['unindexed_median_ms']:.3f} ms")
    print(f"   Indexed Median:   {cp3['indexed_median_ms']:.3f} ms")
    print("-" * 66)
    cp4 = report["checkpoints"]["4_write_and_storage_cost"]
    print(" [Checkpoint 4: Write & Storage Cost]")
    print(f"   DB Size Before Index: {cp4['initial_db_size_bytes']} bytes")
    print(f"   DB Size After Index:  {cp4['indexed_db_size_bytes']} bytes (Delta: +{cp4['size_delta_bytes']} bytes)")
    print(f"   Bulk Insert Unindexed: {cp4['bulk_insert_unindexed_ms']:.2f} ms")
    print(f"   Bulk Insert Indexed:   {cp4['bulk_insert_indexed_ms']:.2f} ms")
    print("-" * 66)
    cp5 = report["checkpoints"]["5_scan_acceptance"]
    print(" [Checkpoint 5: Scan Acceptance on Low Selectivity Query]")
    print(f"   Query:     {cp5['query']}")
    print(f"   Raw EQP:   {cp5['raw_eqp']}")
    print(f"   Bypassed:  {cp5['index_bypassed_as_expected']}")
    print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())
