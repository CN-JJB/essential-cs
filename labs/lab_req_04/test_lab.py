#!/usr/bin/env python3
"""
Unit and integration tests for LAB-REQ-04.
Verifies generator, semantic EQP parser, result equivalence logic,
harness missing-CLI disposition handling, and reset idempotence.
"""

import os
import sqlite3
import tempfile
import unittest

from eqp_parser import (
    normalize_eqp_line,
    parse_eqp_output,
    parse_semantic_access_path,
    summarize_eqp_paths,
)
from generator import generate_lab_dataset
from harness import check_sqlite_cli, run_lab_req_04
from reset import reset_lab_req_04


class TestLabReq04(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_generator_deterministic_output(self):
        db1 = os.path.join(self.tmp_dir.name, "lab1.db")
        db2 = os.path.join(self.tmp_dir.name, "lab2.db")

        generate_lab_dataset(db_path=db1, row_count=100, seed=42)
        generate_lab_dataset(db_path=db2, row_count=100, seed=42)

        conn1 = sqlite3.connect(db1)
        rows1 = conn1.execute("SELECT id, user_id, amount, status FROM orders ORDER BY id;").fetchall()
        conn1.close()

        conn2 = sqlite3.connect(db2)
        rows2 = conn2.execute("SELECT id, user_id, amount, status FROM orders ORDER BY id;").fetchall()
        conn2.close()

        self.assertEqual(len(rows1), 100)
        self.assertEqual(rows1, rows2)

    def test_semantic_eqp_parser_various_formats(self):
        # 1. Pipe format (sqlite3 CLI default tabular)
        pipe_scan = "0|0|0|SCAN orders"
        parsed = parse_semantic_access_path(pipe_scan)
        self.assertEqual(parsed["category"], "SCAN")
        self.assertEqual(parsed["table"], "orders")

        # 2. ASCII tree format with SEARCH USING INDEX
        tree_idx = "`--SEARCH orders USING INDEX idx_orders_user (user_id=?)"
        parsed_idx = parse_semantic_access_path(tree_idx)
        self.assertEqual(parsed_idx["category"], "SEARCH_INDEX")
        self.assertEqual(parsed_idx["table"], "orders")
        self.assertEqual(parsed_idx["index_name"], "idx_orders_user")
        self.assertFalse(parsed_idx["is_covering"])

        # 3. Covering index
        cov_idx = "|--SEARCH orders USING COVERING INDEX idx_orders_cov (user_id=?)"
        parsed_cov = parse_semantic_access_path(cov_idx)
        self.assertEqual(parsed_cov["category"], "COVERING_INDEX")
        self.assertEqual(parsed_cov["table"], "orders")
        self.assertEqual(parsed_cov["index_name"], "idx_orders_cov")
        self.assertTrue(parsed_cov["is_covering"])

        # 4. Multi-line plan parsing & summary
        multi_plan = """
        |--SCAN users
        `--SEARCH orders USING INDEX idx_orders_user (user_id=?)
        """
        records = parse_eqp_output(multi_plan)
        summary = summarize_eqp_paths(records)
        self.assertTrue(summary["has_scan"])
        self.assertTrue(summary["has_search_index"])
        self.assertFalse(summary["has_covering_index"])

    def test_result_equivalence_check(self):
        db_path = os.path.join(self.tmp_dir.name, "equiv.db")
        generate_lab_dataset(db_path=db_path, row_count=50, seed=1)

        conn = sqlite3.connect(db_path)
        q = "SELECT id, user_id, amount FROM orders WHERE user_id = 10 ORDER BY id;"
        res_before = conn.execute(q).fetchall()

        # Add index
        conn.execute("CREATE INDEX idx_test ON orders(user_id);")
        conn.commit()
        res_after = conn.execute(q).fetchall()
        conn.close()

        # Result equivalence invariant: result sets must be identical
        self.assertEqual(res_before, res_after)
        self.assertEqual(len(res_before), len(res_after))

    def test_harness_missing_cli_behavior(self):
        # On this Windows host, sqlite3 CLI is absent; verify harness returns truthful ENVIRONMENT-BLOCKED
        cli_available, _ = check_sqlite_cli()
        if not cli_available:
            report = run_lab_req_04()
            self.assertEqual(report["disposition"], "ENVIRONMENT-BLOCKED / NOT RUN")
            self.assertIn("not found", report["reason"].lower())

    def test_reset_idempotence(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        dummy = os.path.join(base_dir, "test_dummy_req04.db")
        with open(dummy, "w") as f:
            f.write("data")

        cleaned1 = reset_lab_req_04()
        self.assertIn("test_dummy_req04.db", cleaned1)
        self.assertFalse(os.path.exists(dummy))

        cleaned2 = reset_lab_req_04()
        self.assertNotIn("test_dummy_req04.db", cleaned2)


if __name__ == "__main__":
    unittest.main()
