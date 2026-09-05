#!/usr/bin/env python3
"""
Unit tests for M15 Foundations activities (L15-01, L15-02, L15-03) and reset idempotence.
"""

import os
import unittest

try:
    from .activity_l15_01 import run_activity_l15_01, EC_CON_015_DEFINITION
    from .activity_l15_02 import run_activity_l15_02
    from .activity_l15_03 import run_activity_l15_03, EVALUATION_LABEL
    from .reset import reset_m15_foundations
except ImportError:
    from activity_l15_01 import run_activity_l15_01, EC_CON_015_DEFINITION
    from activity_l15_02 import run_activity_l15_02
    from activity_l15_03 import run_activity_l15_03, EVALUATION_LABEL
    from reset import reset_m15_foundations


class TestM15Foundations(unittest.TestCase):
    def tearDown(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        lab_dir = os.path.abspath(os.path.join(this_dir, "..", "..", "lab_req_03"))
        import sys
        if lab_dir not in sys.path:
            sys.path.insert(0, lab_dir)
        from reset import reset_lab_req_03
        reset_lab_req_03(lab_dir=lab_dir, verbose=False)

    def test_activity_l15_01_concurrency_definition_and_lost_update(self):
        res = run_activity_l15_01(verbose=False)
        self.assertIn("Overlapping progress or interleaving of operations", res["ec_con_015_definition"])
        self.assertEqual(res["ec_con_015_definition"], EC_CON_015_DEFINITION)
        if res["execution_disposition"] == "ENVIRONMENT-BLOCKED / NOT RUN":
            self.assertIsNone(res["deterministic_result"])
            self.assertEqual(res["phase_trace"], [])
            self.assertIsNone(res["ub_free_audit_passed"])
            return
        self.assertEqual(res["execution_disposition"], "PASS")
        self.assertTrue(res["ub_free_audit_passed"])
        dr = res["deterministic_result"]
        self.assertEqual(dr["expected_serial"], 10)
        self.assertEqual(dr["actual_value"], 5)
        self.assertEqual(dr["lost_updates"], 5)
        self.assertFalse(dr["ub_present"])

    def test_activity_l15_02_mutex_and_cond_rendezvous(self):
        res = run_activity_l15_02(verbose=False)
        if res["execution_disposition"] == "ENVIRONMENT-BLOCKED / NOT RUN":
            self.assertIsNone(res["mutex_repair"])
            self.assertIsNone(res["cond_rendezvous"])
            self.assertIsNone(res["controlled_deadlock"])
            return
        self.assertEqual(res["execution_disposition"], "PASS")
        mr = res["mutex_repair"]
        self.assertTrue(mr["passed"])
        self.assertTrue(mr["invariant_preserved"])
        self.assertEqual(mr["actual"], mr["expected"])

        cr = res["cond_rendezvous"]
        self.assertTrue(cr["passed"])
        self.assertEqual(cr["final_data"], 42)
        self.assertTrue(cr["predicate_recheck_verified"])

        dl = res["controlled_deadlock"]
        self.assertTrue(dl["passed"])
        self.assertTrue(dl["watchdog_triggered"])
        self.assertTrue(dl["preconditions_proven"])

    def test_activity_l15_03_execution_models_and_bytecode(self):
        res = run_activity_l15_03(verbose=False)
        rt = res["runtime_info"]
        self.assertEqual(rt["implementation"].lower(), "cpython")

        dis_info = res["disassembly"]
        self.assertGreaterEqual(dis_info["opcode_count"], 3)
        self.assertFalse(dis_info["is_single_instruction"])

        async_info = res["async_demo"]
        self.assertTrue(async_info["cooperative_interleaving_observed"])
        self.assertIn("Completed blocking task", async_info["delegated_blocking_result"])

        matrix = res["architectural_matrix"]
        self.assertEqual(matrix["label"], EVALUATION_LABEL)
        self.assertIn("NO UNIVERSAL WINNER", matrix["label"])
        self.assertIn("OS Preemptive Threads", matrix["models"])
        self.assertIn("Cooperative Async Event Loop", matrix["models"])

    def test_reset_idempotence(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        dummy = os.path.join(this_dir, "dummy_test.tmp")
        with open(dummy, "w") as f:
            f.write("temporary")

        count1 = reset_m15_foundations(foundations_dir=this_dir, verbose=False)
        self.assertGreaterEqual(count1, 1)

        count2 = reset_m15_foundations(foundations_dir=this_dir, verbose=False)
        self.assertEqual(count2, 0)


if __name__ == "__main__":
    unittest.main()
