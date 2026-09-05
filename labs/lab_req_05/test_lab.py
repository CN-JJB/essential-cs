#!/usr/bin/env python3
"""
Unit and integration tests for LAB-REQ-05: SQLite Transactions, Isolation & Recovery.
Tests all five checkpoints, process watchdog and reaping, and idempotent reset.
"""

import os
import sqlite3
import tempfile
import unittest

try:
    from .harness import TransactionLabHarness
    from .reset import reset_lab_req_05
except ImportError:
    from harness import TransactionLabHarness
    from reset import reset_lab_req_05


class TestLabReq05(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_lab_req_05.db")
        self.backup_path = os.path.join(self.temp_dir.name, "test_backup.db")
        self.harness = TransactionLabHarness(db_path=self.db_path, backup_path=self.backup_path)
        self.harness.init_database()

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except OSError:
            pass

    def test_checkpoint_1_committed_visibility(self):
        res = self.harness.run_checkpoint_1_committed_visibility()
        self.assertTrue(res["passed"])
        self.assertFalse(res["dirty_read_detected"])
        self.assertEqual(res["conn1_uncommitted_value"], 500)
        self.assertEqual(res["conn2_observed_value"], 600)

    def test_checkpoint_2_bounded_writer_conflict(self):
        res = self.harness.run_checkpoint_2_bounded_writer_conflict()
        self.assertTrue(res["passed"])
        self.assertTrue(res["conflict_caught"])
        code = res["error_details"]["sqlite_errorcode"]
        name = res["error_details"]["sqlite_errorname"]
        structurally_busy = (
            (isinstance(code, int) and (code & 0xFF) in {
                getattr(sqlite3, "SQLITE_BUSY", 5),
                getattr(sqlite3, "SQLITE_LOCKED", 6),
            })
            or (
                isinstance(name, str)
                and (name.startswith("SQLITE_BUSY") or name.startswith("SQLITE_LOCKED"))
            )
        )
        self.assertTrue(structurally_busy)
        self.assertTrue(res["no_corruption"])
        self.assertEqual(res["post_conflict_balances"], {"A": 600, "B": 400})

    def test_checkpoint_3_explicit_rollback(self):
        res = self.harness.run_checkpoint_3_explicit_rollback()
        self.assertTrue(res["passed"])
        self.assertEqual(res["conn1_balances"], {"A": 600, "B": 400})
        self.assertEqual(res["conn2_balances"], {"A": 600, "B": 400})
        self.assertEqual(res["invariant_total"], 1000)

    def test_checkpoint_4_child_interruption_recovery(self):
        res = self.harness.run_checkpoint_4_child_interruption_recovery(timeout_sec=5.0)
        self.assertTrue(res["passed"])
        self.assertIsNotNone(res["child_pid"])
        self.assertIsNotNone(res["child_reaped_returncode"])
        self.assertEqual(res["recovered_balances"], {"A": 600, "B": 400})
        self.assertEqual(res["invariant_total"], 1000)
        self.assertIn("NOT OS crash survival or physical power-loss durability", res["inference_limit"])

    def test_checkpoint_5_backup_and_storage_boundary(self):
        res = self.harness.run_checkpoint_5_backup_and_storage_boundary()
        self.assertTrue(res["passed"])
        self.assertEqual(res["backup_balances"], {"A": 600, "B": 400})
        self.assertEqual(res["invariant_total"], 1000)
        self.assertGreater(res["backup_file_size_bytes"], 0)

    def test_full_run_all(self):
        full_report = self.harness.run_all(verbose=False)
        self.assertTrue(full_report["overall_passed"])
        self.assertEqual(full_report["meta"]["journal_mode"], "DELETE")

    def test_reset_idempotence(self):
        # Create dummy artifacts
        dummy = os.path.join(self.temp_dir.name, "dummy.db")
        with open(dummy, "w") as f:
            f.write("test")
        self.assertTrue(os.path.exists(dummy))

        count1 = reset_lab_req_05(verbose=False)
        count2 = reset_lab_req_05(verbose=False)
        self.assertEqual(count2, 0)


if __name__ == "__main__":
    unittest.main()
