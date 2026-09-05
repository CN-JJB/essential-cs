#!/usr/bin/env python3
"""
Automated unit tests for M14 Foundations activities.
Verifies L14-01, L14-02, L14-03 and idempotent reset.
"""

import os
import sqlite3
import tempfile
import unittest

try:
    from .activity_l14_01 import run_activity_l14_01, verify_invariant
    from .activity_l14_02 import run_activity_l14_02, EC_CON_014_DEFINITION, EC_CON_014_QUALIFIER
    from .activity_l14_03 import run_activity_l14_03, execute_with_boundary_retry
    from .reset import reset_m14_foundations
except ImportError:
    from activity_l14_01 import run_activity_l14_01, verify_invariant
    from activity_l14_02 import run_activity_l14_02, EC_CON_014_DEFINITION, EC_CON_014_QUALIFIER
    from activity_l14_03 import run_activity_l14_03, execute_with_boundary_retry
    from reset import reset_m14_foundations


class TestM14Foundations(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_m14.db")

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except OSError:
            pass

    def test_l14_01_transaction_rollback_and_commit(self):
        results = run_activity_l14_01(db_path=self.db_path, verbose=False)
        self.assertEqual(results["baseline"], {"A": 600, "B": 400})
        self.assertEqual(results["post_rollback"], {"A": 600, "B": 400})
        self.assertEqual(results["post_commit"], {"A": 500, "B": 500})
        self.assertTrue(verify_invariant(results["post_commit"], 1000))
        self.assertTrue(results["inference_limit_acknowledged"])

    def test_l14_02_concurrent_visibility_and_consistency(self):
        results = run_activity_l14_02(db_path=self.db_path, verbose=False)
        self.assertTrue(results["dirty_read_prevented"])
        self.assertEqual(results["conn1_uncommitted_value"], 500)
        self.assertEqual(results["conn2_observed_value"], 600)
        self.assertTrue(results["writer_conflict"]["conflict_detected"])
        self.assertTrue(results["post_rollback_consistent"])
        self.assertIn("relationship between allowed state transitions", results["ec_con_014_definition"])
        self.assertIn("Qualifier:", results["ec_con_014_qualifier"])

    def test_l14_03_atomic_write_upgrade_and_retry(self):
        results = run_activity_l14_03(db_path=self.db_path, verbose=False)
        self.assertTrue(results["collision_result"]["collision_observed"])
        self.assertEqual(results["first_execution"]["status"], "COMMITTED")
        self.assertEqual(results["idempotent_execution"]["status"], "ALREADY_PROCESSED")
        self.assertEqual(results["final_balances"], {"A": 550, "B": 450})
        self.assertEqual(sum(results["final_balances"].values()), 1000)

    def test_l14_03_non_transient_constraint_fails_fast(self):
        try:
            from .activity_l14_03 import init_database
        except ImportError:
            from activity_l14_03 import init_database
        init_database(self.db_path)
        # Verify business logic validation returns INSUFFICIENT_FUNDS
        res = execute_with_boundary_retry(
            self.db_path,
            from_id="A",
            to_id="B",
            amount=99999,  # exceeds balance 600
            idempotency_token="illegal-overdraft-001",
            max_retries=3,
            verbose=False,
        )
        self.assertEqual(res["status"], "INSUFFICIENT_FUNDS")

        # Verify underlying database constraint CHECK (balance >= 0) raises IntegrityError
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        try:
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("INSERT INTO accounts (id, balance) VALUES ('C', -50);")
        finally:
            conn.close()

    def test_reset_idempotence(self):
        # Create dummy artifacts in temp dir
        test_db = os.path.join(self.temp_dir.name, "dummy.db")
        with open(test_db, "w") as f:
            f.write("data")
        self.assertTrue(os.path.exists(test_db))

        # Reset twice on m14 foundations directory
        count1 = reset_m14_foundations(verbose=False)
        count2 = reset_m14_foundations(verbose=False)
        self.assertEqual(count2, 0)


if __name__ == "__main__":
    unittest.main()
