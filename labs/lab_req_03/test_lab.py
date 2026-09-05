#!/usr/bin/env python3
"""
Unit and integration test suite for LAB-REQ-03.
Tests all five checkpoints, compiler integration, watchdog execution, and reset idempotence.
"""

import os
import unittest

try:
    from .harness import ConcurrencyLabHarness
    from .reset import reset_lab_req_03
except ImportError:
    from harness import ConcurrencyLabHarness
    from reset import reset_lab_req_03


class TestLabReq03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.harness = ConcurrencyLabHarness()
        compile_res = cls.harness.compile_all()
        assert compile_res["passed"], f"Compilation failed: {compile_res.get('error')}"

    def test_compilation(self):
        res = self.harness.compile_all()
        self.assertTrue(res["passed"])
        self.assertEqual(len(res["build_log"]), 4)

    def test_checkpoint_1_deterministic_lost_update(self):
        res = self.harness.run_checkpoint_1_deterministic_lost_update()
        self.assertTrue(res["passed"])
        self.assertEqual(res["rounds"], 5)
        self.assertEqual(res["expected_serial"], 10)
        self.assertEqual(res["actual_value"], 5)
        self.assertEqual(res["lost_updates"], 5)
        self.assertFalse(res["ub_present"])
        self.assertIn("PASSED", res["safety_audit"])

    def test_checkpoint_2_supplemental_scheduler_observation(self):
        res = self.harness.run_checkpoint_2_supplemental_scheduler_observation(iterations=2000)
        self.assertTrue(res["passed"])
        self.assertIn("inference_limit", res)
        self.assertEqual(res["iterations_per_thread"], 2000)

    def test_checkpoint_3_mutex_repair(self):
        res = self.harness.run_checkpoint_3_mutex_repair(iterations=5000)
        self.assertTrue(res["passed"])
        self.assertTrue(res["invariant_preserved"])
        self.assertEqual(res["actual"], 10000)
        self.assertEqual(res["lost_updates"], 0)

    def test_checkpoint_4_cond_rendezvous(self):
        res = self.harness.run_checkpoint_4_cond_rendezvous()
        self.assertTrue(res["passed"])
        self.assertEqual(res["final_data"], 42)
        self.assertTrue(res["predicate_recheck_verified"])
        self.assertGreaterEqual(res["predicate_eval_count"], 2)

    def test_checkpoint_5_deadlock_preconditions(self):
        res = self.harness.run_checkpoint_5_deadlock_preconditions(timeout_sec=1.5)
        self.assertTrue(res["passed"])
        self.assertTrue(res["watchdog_triggered"])
        self.assertTrue(res["preconditions_proven"])
        self.assertEqual(res["first_locks_acquired"], ["A", "B"])
        self.assertEqual(res["second_locks_attempted"], ["A", "B"])
        self.assertIsNotNone(res["child_reaped_returncode"])

    def test_run_all(self):
        report = self.harness.run_all(verbose=False)
        self.assertTrue(report["overall_passed"])
        self.assertEqual(len(report["checkpoints"]), 5)

    def test_reset_idempotence(self):
        # Recompile
        self.harness.compile_all()

        # Run reset twice
        count1 = reset_lab_req_03(verbose=False)
        self.assertGreater(count1, 0)
        count2 = reset_lab_req_03(verbose=False)
        self.assertEqual(count2, 0)

        # Restore compiled binaries for clean state
        self.harness.compile_all()


if __name__ == "__main__":
    unittest.main()
