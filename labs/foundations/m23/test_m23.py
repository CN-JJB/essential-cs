#!/usr/bin/env python3
"""
test_m23.py — Standard Library Unit Test Suite for Stage 7 Module M23
====================================================================

Canonical Module: M23 — Systems Thinking & Judgment
Verification Target:
- activity_l23_01.py (Question-Driven Measurement & Coordinated Omission)
- activity_l23_02.py (Decision D-015 12-Dimension Evaluation Framework)
- fermi_cost.py (Bounded Capacity Planning, Fermi Estimation & TCO)
- reset.py (Fail-Closed, Idempotent Scratch Cleanup)

Zero external dependencies (Python standard library unittest only).
Zero flaky timing dependencies: tests assert mathematical and deterministic invariants.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure labs/foundations/m23 is in sys.path for direct or test-runner execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from activity_l23_01 import (
    calculate_percentile,
    calculate_summary_statistics,
    get_clock_characteristics,
    run_live_synthetic_benchmark,
    simulate_measurement_deterministic,
)
from activity_l23_02 import (
    D015_DIMENSIONS,
    VALID_DECISIONS,
    build_scenario_a_redis_rejection,
    build_scenario_b_kafka_outbox,
    build_scenario_c_ai_hypothesis,
    validate_technology_evaluation_card,
)
from fermi_cost import (
    calculate_tco,
    convert_storage,
    estimate_memory_cache_fit,
    estimate_network_egress,
    estimate_storage_capacity,
    run_sensitivity_analysis,
)
from reset import reset_m23_environment


class TestActivityL23_01(unittest.TestCase):
    """Tests for measurement methodology and coordinated omission simulation."""

    def test_clock_characteristics_structure(self) -> None:
        info = get_clock_characteristics()
        self.assertIn("monotonic", info)
        mono = info["monotonic"]
        self.assertTrue(mono["monotonic"], "Monotonic clock must report monotonic=True")
        self.assertFalse(mono["adjustable"], "Monotonic clock must not be adjustable by NTP/time-of-day")
        self.assertGreater(mono["resolution_seconds"], 0.0)

    def test_calculate_summary_statistics_deterministic(self) -> None:
        samples = [10.0, 20.0, 30.0, 40.0, 50.0]
        stats = calculate_summary_statistics(samples)
        self.assertEqual(stats["count"], 5.0)
        self.assertEqual(stats["min"], 10.0)
        self.assertEqual(stats["max"], 50.0)
        self.assertEqual(stats["mean"], 30.0)
        self.assertAlmostEqual(stats["p50"], 30.0)
        self.assertAlmostEqual(stats["p90"], 46.0)

    def test_summary_statistics_empty_and_negative_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            calculate_summary_statistics([])

        with self.assertRaises(ValueError):
            calculate_summary_statistics([1.0, -2.5, 3.0])

    def test_percentile_boundary_conditions(self) -> None:
        samples = [5.0, 10.0, 15.0, 20.0]
        self.assertEqual(calculate_percentile(samples, 0.0), 5.0)
        self.assertEqual(calculate_percentile(samples, 100.0), 20.0)
        with self.assertRaises(ValueError):
            calculate_percentile(samples, -1.0)
        with self.assertRaises(ValueError):
            calculate_percentile(samples, 105.0)

    def test_simulate_measurement_deterministic_coordinated_omission(self) -> None:
        # Schedule: requests arrive every 10ms (t=0, 10, 20, 30, 40, 50, 60, 70, 80, 90)
        # Normal service time = 2ms
        # Injected stall at index 3 of 50ms (so service time = 52ms)
        interval_ms = 10.0
        service_ms = 2.0
        stall_idx = 3
        stall_ms = 50.0
        count = 10

        naive, scheduled = simulate_measurement_deterministic(
            arrival_interval_ms=interval_ms,
            service_time_ms=service_ms,
            stall_index=stall_idx,
            stall_duration_ms=stall_ms,
            request_count=count,
        )

        self.assertEqual(len(naive), count)
        self.assertEqual(len(scheduled), count)

        # Naive generator records only service time
        self.assertEqual(naive[0], 2.0)
        self.assertEqual(naive[1], 2.0)
        self.assertEqual(naive[2], 2.0)
        self.assertEqual(naive[3], 52.0)
        self.assertEqual(naive[4], 2.0)
        self.assertEqual(naive[5], 2.0)

        # Invariant 1: Scheduled latency is always >= naive latency
        for i in range(count):
            self.assertGreaterEqual(
                scheduled[i],
                naive[i],
                f"At index {i}, scheduled latency ({scheduled[i]}) must be >= naive service ({naive[i]})",
            )

        # Invariant 2: Requests arriving during the stall accumulate queue backlog
        # Req 3 arrived at t=30, started at t=30, completed at t=82. Latency = 52ms.
        self.assertEqual(scheduled[3], 52.0)
        # Req 4 arrived at t=40, server busy until t=82, started at t=82, completed at t=84.
        # Queue wait = 42ms. Total latency = 84 - 40 = 44ms!
        self.assertEqual(scheduled[4], 44.0)
        # Req 5 arrived at t=50, started at t=84, completed at t=86. Total latency = 36ms!
        self.assertEqual(scheduled[5], 36.0)

        # Invariant 3: Statistical summary demonstrates coordinated omission
        naive_stats = calculate_summary_statistics(naive)
        sched_stats = calculate_summary_statistics(scheduled)

        self.assertGreater(
            sched_stats["mean"],
            naive_stats["mean"],
            "Arrival-scheduled mean latency must exceed naive mean under open arrival backlog",
        )
        self.assertGreater(
            sched_stats["p90"],
            naive_stats["p90"],
            "Arrival-scheduled tail latency (p90) must reveal queuing backlog hidden by naive loop",
        )

    def test_simulate_measurement_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            simulate_measurement_deterministic(0.0, 2.0, 1, 10.0, 5)
        with self.assertRaises(ValueError):
            simulate_measurement_deterministic(10.0, -1.0, 1, 10.0, 5)
        with self.assertRaises(ValueError):
            simulate_measurement_deterministic(10.0, 2.0, 1, 10.0, 0)
        with self.assertRaises(ValueError):
            simulate_measurement_deterministic(10.0, 2.0, -1, 10.0, 5)
        with self.assertRaises(ValueError):
            simulate_measurement_deterministic(10.0, 2.0, 5, 10.0, 5)
        with self.assertRaises(ValueError):
            simulate_measurement_deterministic(10.0, 2.0, 1, -1.0, 5)

    def test_live_synthetic_budget_is_safety_capped(self) -> None:
        with self.assertRaises(ValueError):
            run_live_synthetic_benchmark(
                request_count=200,
                target_rate_req_per_sec=100.0,
                base_service_time_ms=10.0,
                synthetic_stall_index=10,
                synthetic_stall_ms=100.0,
            )


class TestActivityL23_02(unittest.TestCase):
    """Tests for Decision D-015 Technology Evaluation Framework."""

    def test_all_12_dimensions_present(self) -> None:
        self.assertEqual(len(D015_DIMENSIONS), 12, "Decision D-015 requires exactly 12 dimensions.")
        keys = [k for k, _ in D015_DIMENSIONS]
        expected_keys = [
            "problem_fit",
            "data_model",
            "guarantees",
            "operational_complexity",
            "performance_boundaries",
            "observability",
            "security_isolation",
            "ecosystem_longevity",
            "licensing_governance",
            "cost_model",
            "reversibility",
            "alternatives_rejection",
        ]
        self.assertEqual(keys, expected_keys)

    def test_scenario_a_redis_rejection_passes_validation(self) -> None:
        card = build_scenario_a_redis_rejection()
        res = validate_technology_evaluation_card(card)
        self.assertTrue(res.is_valid, f"Scenario A should be valid, errors: {res.errors}")
        self.assertEqual(res.decision, "REJECT")
        self.assertEqual(res.coverage_percent, 100.0)
        self.assertEqual(len(res.missing_dimensions), 0)
        self.assertEqual(len(res.placeholder_dimensions), 0)

    def test_scenario_b_kafka_outbox_rejection_passes_validation(self) -> None:
        card = build_scenario_b_kafka_outbox()
        res = validate_technology_evaluation_card(card)
        self.assertTrue(res.is_valid, f"Scenario B should be valid, errors: {res.errors}")
        self.assertEqual(res.decision, "REJECT")
        self.assertEqual(res.coverage_percent, 100.0)

    def test_scenario_c_ai_hypothesis_rejection_passes_validation(self) -> None:
        card = build_scenario_c_ai_hypothesis()
        res = validate_technology_evaluation_card(card)
        self.assertTrue(res.is_valid, f"Scenario C should be valid, errors: {res.errors}")
        self.assertEqual(res.decision, "REJECT")
        self.assertEqual(res.coverage_percent, 100.0)

    def test_missing_dimension_fails_validation(self) -> None:
        card = build_scenario_a_redis_rejection()
        del card["dimensions"]["cost_model"]
        res = validate_technology_evaluation_card(card)
        self.assertFalse(res.is_valid)
        self.assertIn("10. Cost Model — Infrastructure & Human", res.missing_dimensions)
        self.assertLess(res.coverage_percent, 100.0)

    def test_placeholder_text_fails_validation(self) -> None:
        card = build_scenario_a_redis_rejection()
        card["dimensions"]["reversibility"] = "TODO"
        res = validate_technology_evaluation_card(card)
        self.assertFalse(res.is_valid)
        self.assertIn("11. Migration & Reversibility / Exit Strategy", res.placeholder_dimensions)

    def test_invalid_decision_fails_validation(self) -> None:
        card = build_scenario_a_redis_rejection()
        card["decision"] = "MAYBE"
        res = validate_technology_evaluation_card(card)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Invalid decision" in err for err in res.errors))

    def test_machine_schema_accepts_adopt_category_without_grading_semantics(self) -> None:
        card = build_scenario_a_redis_rejection()
        card["decision"] = "ADOPT"
        res = validate_technology_evaluation_card(card)
        # Structural lint intentionally does not decide semantic judgment quality.
        # A reviewer must reject contradictory ADOPT/REJECT rationale if a learner submits it.
        self.assertTrue(res.is_valid)
        self.assertEqual(res.decision, "ADOPT")
        self.assertEqual(res.coverage_percent, 100.0)


class TestFermiCost(unittest.TestCase):
    """Tests for capacity estimation, Fermi math, unit tracking, and TCO."""

    def test_storage_unit_conversions(self) -> None:
        # Bit vs Byte
        self.assertEqual(convert_storage(8.0, "b", "bytes"), 1.0)
        self.assertEqual(convert_storage(1.0, "bytes", "b"), 8.0)
        self.assertEqual(convert_storage(1.0, "Mb", "kB"), 125.0)

        # Decimal (SI, 1000)
        self.assertEqual(convert_storage(1.0, "kB", "bytes"), 1000.0)
        self.assertEqual(convert_storage(1.0, "MB", "kB"), 1000.0)
        self.assertEqual(convert_storage(1.0, "TB", "bytes"), 1e12)

        # Binary (IEC, 1024)
        self.assertEqual(convert_storage(1.0, "KiB", "bytes"), 1024.0)
        self.assertEqual(convert_storage(1.0, "MiB", "KiB"), 1024.0)
        self.assertEqual(convert_storage(1.0, "GiB", "bytes"), 1073741824.0)

        # Cross decimal/binary
        one_gib_in_gb = convert_storage(1.0, "GiB", "GB")
        self.assertAlmostEqual(one_gib_in_gb, 1.073741824)

    def test_storage_conversions_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            convert_storage(-5.0, "mb", "gb")
        with self.assertRaises(ValueError):
            convert_storage(10.0, "invalid_unit", "GB")
        with self.assertRaises(ValueError):
            convert_storage(1.0, "KB", "bytes")
        with self.assertRaises(ValueError):
            convert_storage(1.0, "mb", "bytes")

    def test_storage_capacity_estimation(self) -> None:
        # Synthetic assumptions: 100,000 items/day, 10,000 B each, 3x replication, 90-day retention
        res = estimate_storage_capacity(
            items_per_day=100_000,
            avg_item_bytes=10_000,  # 10 kB
            replication_factor=3.0,
            indexing_overhead_ratio=0.10,  # 10% indexing
            retention_days=90,
        )
        # daily logical = 100_000 * 10_000 = 1,000,000,000 bytes (1 GB)
        self.assertEqual(res["daily_logical_bytes"], 1_000_000_000.0)
        self.assertEqual(res["daily_logical_gb"], 1.0)
        # daily physical = 1 GB * 3 * 1.1 = 3.3 GB
        self.assertAlmostEqual(res["daily_physical_gb"], 3.3)
        # 90-day total = 3.3 GB * 90 = 297 GB = 0.297 TB
        self.assertAlmostEqual(res["total_retained_gb"], 297.0)
        self.assertAlmostEqual(res["total_retained_tb"], 0.297)

    def test_network_egress_estimation(self) -> None:
        # 86,400 requests/day, 100,000 bytes payload
        # 86,400 sec in day -> avg 1 request/sec -> avg 100,000 Bytes/sec -> 800,000 bps
        res = estimate_network_egress(
            requests_per_day=86_400,
            avg_payload_bytes=100_000,
            peak_to_avg_ratio=2.5,
        )
        self.assertAlmostEqual(res["avg_bytes_per_sec"], 100_000.0)
        self.assertAlmostEqual(res["avg_bits_per_sec"], 800_000.0)
        self.assertAlmostEqual(res["peak_bytes_per_sec"], 250_000.0)
        self.assertAlmostEqual(res["peak_bits_per_sec"], 2_000_000.0)
        self.assertAlmostEqual(res["peak_mbps"], 2.0)

    def test_memory_cache_fit(self) -> None:
        # 10,000,000 rows * 200 bytes = 2,000,000,000 bytes (~2 GB)
        # Synthetic assumption: server has 16 GiB RAM; learner-selected usable fraction 0.75 -> 12 GiB.
        res = estimate_memory_cache_fit(
            active_items=10_000_000,
            avg_item_bytes=200,
            installed_ram_bytes=16 * 1024**3,  # 16 GiB
            max_cache_fraction=0.75,
        )
        self.assertTrue(res["fits_in_memory"])
        self.assertLess(res["usable_ram_utilization_pct"], 25.0)

        # Massive dataset does NOT fit
        res_overflow = estimate_memory_cache_fit(
            active_items=100_000_000,
            avg_item_bytes=2000,  # synthetic row-size assumption
            installed_ram_bytes=16 * 1024**3,
            max_cache_fraction=0.75,
        )
        self.assertFalse(res_overflow["fits_in_memory"])

    def test_calculate_tco(self) -> None:
        # Infra $200/mo, Human 5 hrs/mo @ $100/hr = $500/mo
        # Total = $700/mo
        res = calculate_tco(
            infra_monthly_cost=200.0,
            human_hours_per_month=5.0,
            human_hourly_rate=100.0,
        )
        self.assertEqual(res["infra_monthly_cost"], 200.0)
        self.assertEqual(res["human_monthly_cost"], 500.0)
        self.assertEqual(res["total_monthly_cost"], 700.0)
        self.assertAlmostEqual(res["infra_percentage"], (200 / 700) * 100.0)
        self.assertAlmostEqual(res["human_percentage"], (500 / 700) * 100.0)

    def test_sensitivity_analysis(self) -> None:
        baseline = {
            "items_per_day": 10_000,
            "avg_item_bytes": 1000,
            "replication_factor": 1.0,
            "indexing_overhead_ratio": 0.0,
            "requests_per_day": 100_000,
            "avg_egress_bytes": 2000,
            "peak_to_avg_ratio": 1.0,
            "retention_days": 30,
        }
        variations = {
            "10x_traffic": {"requests_per_day": 1_000_000},
            "1_year_retention": {"retention_days": 365},
        }
        res = run_sensitivity_analysis(baseline, variations)
        self.assertIn("baseline", res)
        self.assertIn("variations", res)

        v10x = res["variations"]["10x_traffic"]
        self.assertAlmostEqual(v10x["deltas_from_baseline"]["daily_egress_gb"]["multiplier"], 10.0)

        v_ret = res["variations"]["1_year_retention"]
        self.assertAlmostEqual(
            v_ret["deltas_from_baseline"]["retained_tb"]["multiplier"],
            365.0 / 30.0,
            places=3,
        )

        zero_baseline = dict(baseline)
        zero_baseline["requests_per_day"] = 0
        zero_variation = run_sensitivity_analysis(
            zero_baseline,
            {"traffic_starts": {"requests_per_day": 1000}},
        )
        zero_delta = zero_variation["variations"]["traffic_starts"]["deltas_from_baseline"]["daily_egress_gb"]
        self.assertIsNone(zero_delta["multiplier"])
        self.assertEqual(zero_delta["multiplier_status"], "UNDEFINED_FROM_ZERO_BASELINE")

        missing_assumption = dict(baseline)
        del missing_assumption["peak_to_avg_ratio"]
        with self.assertRaises(ValueError):
            run_sensitivity_analysis(missing_assumption, {})


class TestResetM23(unittest.TestCase):
    """Tests for idempotent, fail-closed scratch cleanup."""

    def test_reset_m23_idempotent(self) -> None:
        m23_dir = Path(__file__).resolve().parent
        scratch_dir = m23_dir / ".scratch"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        probe_file = scratch_dir / "test_scratch.tmp"
        probe_file.write_text("test content", encoding="utf-8")

        # First run: cleans probe file
        removed = reset_m23_environment(verbose=False)
        self.assertGreaterEqual(removed, 1)
        self.assertFalse(probe_file.exists())

        # Second run: idempotent, returns 0 without error
        removed_second = reset_m23_environment(verbose=False)
        self.assertEqual(removed_second, 0)


if __name__ == "__main__":
    unittest.main()
