#!/usr/bin/env python3
"""
Unit and integration tests for M13 laboratory activities.
Tests deterministic generation, access path semantic classification,
sargability breakdown, schema evolution expand-contract, and reset idempotence.
"""

import os
import sqlite3
import tempfile
import unittest

from fixture_l13 import (
    classify_eqp_detail,
    compare_sargability,
    generate_synthetic_data,
    inspect_eqp,
)
from reset import reset_m13_fixtures
from schema_evolution import (
    demonstrate_controlled_break,
    execute_backfill_phase,
    execute_expand_phase,
    recompute_derived_view,
    setup_initial_database,
)


class TestM13Activity(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_synthetic_data_generation_and_eqp(self):
        db_path = os.path.join(self.tmp_dir.name, "test_fixture.db")
        generate_synthetic_data(db_path=db_path, user_count=50, order_count=200, seed=123)
        self.assertTrue(os.path.exists(db_path))

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users;")
        self.assertEqual(cur.fetchone()[0], 50)

        cur.execute("SELECT COUNT(*) FROM orders;")
        self.assertEqual(cur.fetchone()[0], 200)

        # Before index: query by user_id should scan
        q = "SELECT * FROM orders WHERE user_id = 10;"
        eqp_before = inspect_eqp(conn, q)
        classes_before = [classify_eqp_detail(r[3]) for r in eqp_before]
        self.assertIn("TABLE_SCAN", classes_before)

        # Add index
        conn.execute("CREATE INDEX idx_orders_user ON orders(user_id);")
        conn.commit()

        # After index: query by user_id should search using index
        eqp_after = inspect_eqp(conn, q)
        classes_after = [classify_eqp_detail(r[3]) for r in eqp_after]
        self.assertTrue(
            any(c in ("INDEX_SEARCH", "COVERING_INDEX_SEARCH") for c in classes_after),
            f"Expected index search, got: {classes_after}",
        )
        conn.close()

    def test_sargability_breakdown(self):
        db_path = os.path.join(self.tmp_dir.name, "test_sarg.db")
        generate_synthetic_data(db_path=db_path, user_count=30, order_count=50, seed=99)
        conn = sqlite3.connect(db_path)

        res = compare_sargability(conn)
        # Sargable query on UNIQUE username uses index/search
        sarg_classes = res["sargable"]["classifications"]
        self.assertTrue(
            any("SEARCH" in c or "INDEX" in c for c in sarg_classes),
            f"Expected search/index for sargable, got: {sarg_classes}",
        )

        # Non-sargable query with UPPER() forces scan
        nonsarg_classes = res["non_sargable"]["classifications"]
        self.assertIn(
            "TABLE_SCAN",
            nonsarg_classes,
            f"Expected TABLE_SCAN for non-sargable, got: {nonsarg_classes}",
        )
        conn.close()

    def test_schema_evolution_expand_contract_and_break(self):
        db_path = os.path.join(self.tmp_dir.name, "test_evo.db")
        setup_initial_database(db_path=db_path)

        # Controlled break: adding NOT NULL column without DEFAULT fails
        break_res = demonstrate_controlled_break(db_path=db_path)
        self.assertTrue(break_res["break_observed"])
        self.assertIsNotNone(break_res["error_message"])

        # Expand phase: adding column with DEFAULT succeeds
        expand_res = execute_expand_phase(db_path=db_path)
        self.assertEqual(expand_res["status"], "EXPAND_COMPLETE")
        self.assertEqual(len(expand_res["rows"]), 3)
        for row in expand_res["rows"]:
            self.assertEqual(row[2], "PENDING_VERIFICATION")

        # Backfill phase: updates legacy rows
        backfill_res = execute_backfill_phase(db_path=db_path)
        self.assertEqual(backfill_res["status"], "BACKFILL_COMPLETE")
        self.assertGreater(backfill_res["updated_count"], 0)

        # Derived view recomputation from Source of Truth
        derived_res = recompute_derived_view(db_path=db_path)
        self.assertEqual(derived_res["recomputed_count"], 3)
        # Check that user 1 has correct aggregate from orders
        # (user 1 had orders: 45.50 + 15.00 + 100.00 = 160.50, count = 3)
        u1_row = [r for r in derived_res["rows"] if r[0] == 1][0]
        self.assertEqual(u1_row[1], 3)
        self.assertAlmostEqual(u1_row[2], 160.50)

    def test_reset_idempotence(self):
        # Create a dummy file in the m13 directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        test_file = os.path.join(base_dir, "test_dummy_cleanup.db")
        with open(test_file, "w") as f:
            f.write("dummy")

        # First run removes it
        cleaned1 = reset_m13_fixtures()
        self.assertIn("test_dummy_cleanup.db", cleaned1)
        self.assertFalse(os.path.exists(test_file))

        # Second run is safe and clean
        cleaned2 = reset_m13_fixtures()
        self.assertNotIn("test_dummy_cleanup.db", cleaned2)


if __name__ == "__main__":
    unittest.main()
