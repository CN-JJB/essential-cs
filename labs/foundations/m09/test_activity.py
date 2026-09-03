#!/usr/bin/env python3
"""Automated machine-checkable test suite for M09 lab packet.

Verifies:
- L09-01: Durability observer measurement, repeated raw samples, sync call counts,
          canonical EC-CON-016 definition and named failure bounds, safety caps,
          and WAL ordering & crash recovery model.
- L09-02: Media mechanics model (HDD latency calculation, SSD WAF calculation,
          parameter visibility, illustrative model labeling, and TBW endurance inference limits).
- L09-03: Storage economics cost model parameterization, arithmetic consistency,
          explicit omissions, Technology Evaluation Framework with when-not-to-use,
          and capability-gated network observation truthfulness.
- Cleanup & reset verification: leaves zero generated files behind.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add current directory to path
HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from durability_observer import (
    demonstrate_file_and_directory_sync,
    get_canonical_durability_concept,
    measure_sync_vs_buffered,
    validate_workload_bounds,
)
from media_model import (
    calculate_hdd_latency,
    estimate_ssd_endurance_tbw,
    simulate_ssd_waf_scenario,
    validate_media_model_inputs,
)
from reset import reset_m09_workspace
from storage_economics import (
    estimate_monthly_storage_cost,
    evaluate_storage_technology,
    load_reference_assumptions,
    probe_public_http_object,
)
from wal_model import WALEngine, run_wal_demonstration


class TestL0901DurabilityAndWAL(unittest.TestCase):
    """L09-01: Durability concept definition, synchronization boundaries, and WAL."""

    def test_canonical_concept_definition(self):
        concept = get_canonical_durability_concept()
        self.assertEqual(concept["concept_id"], "EC-CON-016")
        self.assertEqual(concept["first_home_module"], "M09")
        self.assertEqual(concept["first_home_lesson"], "L09-01")
        self.assertEqual(
            concept["canonical_definition"],
            "A committed state survives a named restart or failure bound.",
        )
        self.assertIn("process_crash", concept["named_failure_bounds"])
        self.assertIn("sudden_power_loss", concept["named_failure_bounds"])

    def test_workload_safety_caps(self):
        # Valid workload passes
        validate_workload_bounds(num_records=50, record_size=64)

        # Exceeding record count
        with self.assertRaises(ValueError):
            validate_workload_bounds(num_records=1000, record_size=64)

        # Exceeding record size
        with self.assertRaises(ValueError):
            validate_workload_bounds(num_records=10, record_size=4096)

        # Exceeding total payload
        with self.assertRaises(ValueError):
            validate_workload_bounds(num_records=500, record_size=1024)

    def test_sync_vs_buffered_measurement(self):
        num_records = 20
        record_size = 64
        trials = 3
        res = measure_sync_vs_buffered(
            num_records=num_records,
            record_size=record_size,
            trials=trials,
        )

        # Machine checks
        self.assertEqual(res["total_logical_bytes"], num_records * record_size)
        self.assertEqual(len(res["buffered_samples_ns"]), trials)
        self.assertEqual(len(res["synced_samples_ns"]), trials)
        self.assertEqual(res["total_sync_calls_executed"], trials * num_records)
        self.assertIsInstance(res["buffered_mean_ms"], float)
        self.assertIsInstance(res["synced_mean_ms"], float)
        # Note: Do NOT assert synced_mean_ms > buffered_mean_ms as an immutable universal,
        # but assert that values are valid positive floats
        self.assertGreater(res["buffered_mean_ms"], 0.0)
        self.assertGreater(res["synced_mean_ms"], 0.0)

    def test_file_and_directory_sync(self):
        report = demonstrate_file_and_directory_sync()
        self.assertTrue(report["file_data_synced"])
        self.assertIn(report["parent_dir_sync_disposition"], ["PASS", "ENVIRONMENT_LIMITED"])
        if report["parent_dir_sync_disposition"] == "PASS":
            self.assertTrue(report["parent_dir_synced"])
        else:
            self.assertFalse(report["parent_dir_synced"])
            self.assertIn("parent_dir_sync_error", report)

    def test_wal_model_ordering_and_recovery(self):
        engine = WALEngine()

        # Checkpoint initial accounts
        t0 = engine.begin_txn()
        engine.update(t0, "user_A", "500")
        engine.update(t0, "user_B", "1000")
        engine.commit_txn(t0, sync=True)
        engine.checkpoint()
        self.assertEqual(engine.disk_table["user_A"], "500")

        # Txn 1 committed and synced
        t1 = engine.begin_txn()
        engine.update(t1, "user_A", "600")
        engine.commit_txn(t1, sync=True)

        # Txn 2: In-flight active transaction whose log records were flushed, but NOT committed
        t2 = engine.begin_txn()
        engine.update(t2, "user_B", "9999")
        engine.sync_log()  # Log record reached disk before crash, but no COMMIT record

        # Txn 3: In-flight active transaction whose log was NOT flushed (completely lost)
        t3 = engine.begin_txn()
        engine.update(t3, "user_C", "8888")

        # Simulate crash
        crashed = engine.simulate_crash()
        # In crashed state before recovery, unflushed updates to user_C are lost
        self.assertNotIn("user_C", crashed.disk_table)

        # Execute recovery
        rec_report = crashed.recover()
        rec_table = rec_report["recovered_table"]

        # Txn 1 committed changes restored via Redo
        self.assertEqual(rec_table["user_A"], "600")
        # Txn 2 active uncommitted changes identified and undone
        self.assertEqual(rec_table["user_B"], "1000")
        self.assertIn(t1, rec_report["analysis_committed_txns"])
        self.assertIn(t2, rec_report["analysis_active_uncommitted_txns"])
        # Txn 3 never reached persistent log, so not in log analysis
        self.assertNotIn(t3, rec_report["analysis_active_uncommitted_txns"])

    def test_wal_run_demonstration_helper(self):
        demo = run_wal_demonstration()
        self.assertTrue(demo["consistency_restored"])


class TestL0902MediaMechanics(unittest.TestCase):
    """L09-02: HDD mechanical latency, SSD WAF calculation, and endurance."""

    def test_media_model_safety_caps(self):
        validate_media_model_inputs(pages_per_block=64, page_size_kb=4, valid_pages_in_victim=32)

        with self.assertRaises(ValueError):
            validate_media_model_inputs(pages_per_block=5000, page_size_kb=4, valid_pages_in_victim=10)

        with self.assertRaises(ValueError):
            validate_media_model_inputs(pages_per_block=64, page_size_kb=128, valid_pages_in_victim=10)

        with self.assertRaises(ValueError):
            validate_media_model_inputs(pages_per_block=64, page_size_kb=4, valid_pages_in_victim=64)

    def test_hdd_latency_calculation(self):
        res_rand = calculate_hdd_latency(rpm=7200, avg_seek_ms=8.5, is_sequential=False)
        self.assertEqual(res_rand["model_label"], "ILLUSTRATIVE MODEL EVIDENCE")
        self.assertAlmostEqual(res_rand["rotational_ms"], 4.1667, places=3)
        self.assertEqual(res_rand["seek_ms"], 8.5)
        self.assertGreater(res_rand["total_latency_ms"], 12.0)

        res_seq = calculate_hdd_latency(rpm=7200, avg_seek_ms=8.5, is_sequential=True)
        self.assertEqual(res_seq["seek_ms"], 0.0)
        self.assertEqual(res_seq["rotational_ms"], 0.0)
        self.assertLess(res_seq["total_latency_ms"], 1.0)

    def test_ssd_waf_arithmetic(self):
        # Scenario 1: 63 valid pages copied for 1 host write page in a 64-page block
        # Flash writes = (63 + 1) * 4 KiB = 256 KiB; Host writes = 1 * 4 KiB = 4 KiB
        # WAF = 256 / 4 = 64.0
        s1 = simulate_ssd_waf_scenario(pages_per_block=64, page_size_kb=4, valid_pages_in_victim=63, host_write_pages=1)
        self.assertEqual(s1["model_label"], "ILLUSTRATIVE MODEL EVIDENCE")
        self.assertEqual(s1["waf"], 64.0)
        self.assertEqual(s1["host_bytes_written"], 4 * 1024)
        self.assertEqual(s1["total_flash_bytes_written"], 256 * 1024)

        # Scenario 2: 32 valid pages copied for 32 host write pages
        # Flash writes = (32 + 32) * 4 KiB = 256 KiB; Host writes = 32 * 4 KiB = 128 KiB
        # WAF = 256 / 128 = 2.0
        s2 = simulate_ssd_waf_scenario(pages_per_block=64, page_size_kb=4, valid_pages_in_victim=32, host_write_pages=32)
        self.assertEqual(s2["waf"], 2.0)

        # Scenario 3: 0 valid pages copied (completely obsolete block)
        s3 = simulate_ssd_waf_scenario(pages_per_block=64, page_size_kb=4, valid_pages_in_victim=0, host_write_pages=64)
        self.assertEqual(s3["waf"], 1.0)

    def test_ssd_endurance_tbw(self):
        # 1000 GB, 3000 PE, WAF=3.0 -> TBW = (1000 * 3000) / (3.0 * 1000) = 1000 TBW
        res = estimate_ssd_endurance_tbw(drive_capacity_gb=1000.0, pe_cycles=3000, waf=3.0)
        self.assertEqual(res["model_label"], "ILLUSTRATIVE MODEL EVIDENCE")
        self.assertEqual(res["estimated_host_tbw"], 1000.0)
        self.assertIn("JESD218", res["inference_boundary_warning"])


class TestL0903StorageEconomics(unittest.TestCase):
    """L09-03: Storage architecture comparison, cost parameterization, and technology evaluation."""

    def test_reference_assumptions_loaded(self):
        assumptions = load_reference_assumptions()
        self.assertEqual(assumptions["metadata"]["currency"], "USD")
        self.assertEqual(assumptions["metadata"]["region"], "us-east-1")
        self.assertIn("checked_date", assumptions["metadata"])
        self.assertIn("block_storage", assumptions["tiers"])
        self.assertIn("file_storage", assumptions["tiers"])
        self.assertIn("object_storage", assumptions["tiers"])

    def test_cost_calculation_arithmetic(self):
        # 1000 GB, 10,000 writes, 50,000 reads, 10 GB egress
        res = estimate_monthly_storage_cost(
            capacity_gb=1000.0,
            write_requests=10000,
            read_requests=50000,
            egress_gb=10.0,
        )

        # Verify Block: 1000 * 0.08 = 80.00
        self.assertEqual(res["block_storage"]["total_monthly_cost"], 80.0)

        # Verify File: 1000 * 0.30 = 300.00
        self.assertEqual(res["file_storage"]["total_monthly_cost"], 300.0)

        # Verify Object:
        # Storage: 1000 * 0.023 = 23.00
        # Writes: (10000 / 1000) * 0.005 = 0.05
        # Reads: (50000 / 1000) * 0.0004 = 0.02
        # Egress: 10 * 0.09 = 0.90
        # Total: 23.00 + 0.05 + 0.02 + 0.90 = 23.97
        self.assertAlmostEqual(res["object_storage"]["total_monthly_cost"], 23.97, places=2)

        # Verify explicit omissions listed
        self.assertIn("provisioned_iops_and_burst_credits", res["explicit_omissions"])
        self.assertIn("volume_snapshot_storage", res["explicit_omissions"])

    def test_cost_calculation_safety_cap(self):
        with self.assertRaises(ValueError):
            estimate_monthly_storage_cost(capacity_gb=50_000_000)

    def test_technology_evaluation_framework(self):
        for arch in ["block", "file", "object"]:
            eval_dict = evaluate_storage_technology(arch)
            self.assertIn("problem", eval_dict)
            self.assertIn("constraints", eval_dict)
            self.assertIn("mechanism", eval_dict)
            self.assertIn("gains", eval_dict)
            self.assertIn("costs", eval_dict)
            self.assertIn("failure_modes", eval_dict)
            self.assertIn("when_not_to_use", eval_dict)
            self.assertTrue(len(eval_dict["when_not_to_use"]) > 10)

    def test_network_probe_capability_gating(self):
        probe = probe_public_http_object()
        self.assertIn(probe["status"], ["PASS", "SKIP"])
        if probe["status"] == "SKIP":
            self.assertEqual(probe["disposition"], "NO LIVE NETWORK OBSERVATION")
            self.assertIn("No fabricated network transcript", probe["confirmation"])


class TestResetAndWorkspace(unittest.TestCase):
    """Workspace cleanup and reset verification."""

    def test_reset_cleans_workspace(self):
        ret = reset_m09_workspace()
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
