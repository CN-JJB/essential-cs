#!/usr/bin/env python3
"""
test_m20.py — Complete Unit & Integration Test Suite for Stage 6 Module 20
========================================================================

Verifies all Core M20 invariants:
1. Clock Semantics & Monotonic Timing.
2. Deterministic Distribution Statistics & Tail Divergence.
3. SLI / SLO / Error Budget Calculations.
4. W3C Trace Context Level 1 version-00 Generator, Parser & Strict Validation.
5. Structured Logger & Privacy Redaction.
6. Local Three-Service Lifecycle, Fault Injection, Timeline Correlation & Safe Mitigation.
7. Reset Idempotence & Fail-Closed Cleanup Regression.
"""

import json
import os
import time
import unittest
from unittest import mock

from reset import reset_m20_environment
from s6_m20_observability_pipeline import (
    ClockAdapter,
    ObservabilityPipelineManager,
    StructuredLogger,
    compute_distribution_statistics,
    compute_elapsed_duration_ms,
    evaluate_sli_slo,
    generate_blameless_postmortem,
    generate_traceparent,
    parse_traceparent,
    reconstruct_correlated_timeline,
)


class TestClockSemantics(unittest.TestCase):
    def test_monotonic_clock_increases_linearly(self) -> None:
        adapter = ClockAdapter()
        t0 = adapter.monotonic_time()
        time.sleep(0.01)
        t1 = adapter.monotonic_time()
        self.assertGreater(t1, t0)
        dur = compute_elapsed_duration_ms(t0, t1)
        self.assertGreaterEqual(dur, 8.0)

    def test_fake_wall_clock_step_does_not_mutate_monotonic(self) -> None:
        adapter = ClockAdapter()
        w0 = adapter.wall_time()
        m0 = adapter.monotonic_time()

        time.sleep(0.01)
        # Inject fake backward step of 15 seconds
        adapter.inject_wall_step_backward(15.0)

        w1 = adapter.wall_time()
        m1 = adapter.monotonic_time()

        wall_diff = w1 - w0
        mono_diff = m1 - m0

        # Wall clock subtraction becomes negative due to simulated backward step
        self.assertLess(wall_diff, -10.0)
        # Monotonic clock duration remains positive and valid
        self.assertGreater(mono_diff, 0.0)
        self.assertGreaterEqual(compute_elapsed_duration_ms(m0, m1), 8.0)


class TestDistributionStatistics(unittest.TestCase):
    def test_nearest_rank_percentiles(self) -> None:
        # 100 samples: 1 to 100
        samples = [float(i) for i in range(1, 101)]
        stats = compute_distribution_statistics(samples, convention="nearest_rank")

        self.assertEqual(stats["sample_count"], 100)
        self.assertEqual(stats["min_ms"], 1.0)
        self.assertEqual(stats["max_ms"], 100.0)
        self.assertEqual(stats["mean_ms"], 50.5)
        self.assertEqual(stats["p50_ms"], 50.0)
        self.assertEqual(stats["p90_ms"], 90.0)
        self.assertEqual(stats["p95_ms"], 95.0)
        self.assertEqual(stats["p99_ms"], 99.0)

    def test_tail_divergence_bimodal_distribution(self) -> None:
        # 95 samples of 5.0ms, 5 samples of 500.0ms
        samples = [5.0] * 95 + [500.0] * 5
        stats = compute_distribution_statistics(samples, convention="nearest_rank")

        self.assertEqual(stats["p50_ms"], 5.0)
        self.assertEqual(stats["p90_ms"], 5.0)
        self.assertEqual(stats["p95_ms"], 5.0)
        self.assertEqual(stats["p99_ms"], 500.0)
        self.assertAlmostEqual(stats["mean_ms"], 29.75, places=2)

    def test_empty_samples_rejected(self) -> None:
        with self.assertRaises(ValueError):
            compute_distribution_statistics([])


class TestSliSloEvaluator(unittest.TestCase):
    def test_sli_slo_evaluation_success(self) -> None:
        # 10,000 requests, 9,995 good, 99.9% SLO
        res = evaluate_sli_slo(
            total_valid_requests=10000,
            good_requests=9995,
            slo_target_percent=99.9,
            window_seconds=2592000.0,
        )
        self.assertEqual(res["actual_sli_percent"], 99.95)
        self.assertTrue(res["slo_met"])
        self.assertEqual(res["allowed_bad_requests"], 10.0)
        self.assertEqual(res["bad_requests"], 5)
        self.assertEqual(res["remaining_budget_requests"], 5.0)
        self.assertEqual(res["budget_consumed_percent"], 50.0)

    def test_sli_slo_budget_exhaustion(self) -> None:
        res = evaluate_sli_slo(
            total_valid_requests=10000,
            good_requests=9980,
            slo_target_percent=99.9,
        )
        self.assertEqual(res["actual_sli_percent"], 99.8)
        self.assertFalse(res["slo_met"])
        self.assertEqual(res["bad_requests"], 20)
        self.assertEqual(res["budget_consumed_percent"], 200.0)

    def test_invalid_parameters_raise(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_sli_slo(0, 0, 99.0)
        with self.assertRaises(ValueError):
            evaluate_sli_slo(100, 105, 99.0)
        with self.assertRaises(ValueError):
            evaluate_sli_slo(100, 90, 105.0)


class TestW3CTraceContext(unittest.TestCase):
    def test_generate_and_parse_valid_traceparent(self) -> None:
        tp = generate_traceparent(sampled=True)
        self.assertEqual(len(tp), 55)
        self.assertTrue(tp.startswith("00-"))
        self.assertTrue(tp.endswith("-01"))

        parsed = parse_traceparent(tp)
        self.assertEqual(parsed["version"], "00")
        self.assertEqual(len(parsed["trace_id"]), 32)
        self.assertEqual(len(parsed["parent_id"]), 16)
        self.assertEqual(parsed["trace_flags"], "01")
        self.assertTrue(parsed["sampled"])

    def test_all_zero_trace_id_rejected(self) -> None:
        bad_header = "00-00000000000000000000000000000000-1234567812345678-01"
        with self.assertRaises(ValueError) as ctx:
            parse_traceparent(bad_header)
        self.assertIn("all-zero trace ID", str(ctx.exception))

    def test_all_zero_parent_id_rejected(self) -> None:
        bad_header = "00-4bf92f3577b34da6a3ce929d0e0e4736-0000000000000000-01"
        with self.assertRaises(ValueError) as ctx:
            parse_traceparent(bad_header)
        self.assertIn("all-zero parent ID", str(ctx.exception))

    def test_invalid_version_length_and_characters_rejected(self) -> None:
        # Version 'ff' forbidden
        with self.assertRaises(ValueError):
            parse_traceparent("ff-4bf92f3577b34da6a3ce929d0e0e4736-1234567812345678-01")

        # Wrong character count for version 00
        with self.assertRaises(ValueError):
            parse_traceparent("00-4bf92f3577b34da6a3ce929d0e0e4736-1234567812345678-01-extra")

        # Non-hex characters
        with self.assertRaises(ValueError):
            parse_traceparent("00-4bf92f3577b34da6a3ce929d0e0e47zz-1234567812345678-01")


class TestStructuredLoggerPrivacy(unittest.TestCase):
    def test_logger_redacts_passwords_and_tokens(self) -> None:
        logger = StructuredLogger()
        entry = logger.log(
            service="ServiceA",
            event="user_login",
            trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
            details={
                "username": "alice",
                "auth_header": "Bearer secret_token_123",
                "password": "super_secret_password",
                "cookie": "session_id=xyz",
                "item_id": 42,
            },
        )
        self.assertEqual(entry["details"]["username"], "alice")
        self.assertEqual(entry["details"]["item_id"], 42)
        self.assertEqual(entry["details"]["auth_header"], "[REDACTED]")
        self.assertEqual(entry["details"]["password"], "[REDACTED]")
        self.assertEqual(entry["details"]["cookie"], "[REDACTED]")


class TestThreeServicePipelineIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ObservabilityPipelineManager()
        self.manager.start()

    def tearDown(self) -> None:
        self.manager.shutdown()

    def test_normal_end_to_end_request(self) -> None:
        res = self.manager.dispatch_request()
        self.assertEqual(res["status_code"], 200)
        self.assertIn("trace_id", res["response"])

        trace_id = res["response"]["trace_id"]
        records = self.manager.logger.filter_by_trace_id(trace_id)
        services_seen = {r["service"] for r in records}
        self.assertEqual(services_seen, {"ServiceA", "ServiceB", "ServiceC"})

    def test_fault_injection_and_timeline_localization(self) -> None:
        # Inject 250ms delay in ServiceC
        self.manager.set_fault(fault_mode="DELAY", delay_s=0.25)
        res = self.manager.dispatch_request()

        self.assertEqual(res["status_code"], 200)
        self.assertGreaterEqual(res["elapsed_ms"], 240.0)

        trace_id = res["response"]["trace_id"]
        timeline = reconstruct_correlated_timeline(
            self.manager.logger.get_records(), trace_id
        )
        self.assertIsNotNone(timeline["fault_localized"])
        self.assertIn("ServiceC", timeline["fault_localized"])
        self.assertGreaterEqual(timeline["service_durations_ms"]["ServiceC"], 240.0)

    def test_safe_mitigation_recovers_latency(self) -> None:
        # Under delay fault
        self.manager.set_fault(fault_mode="DELAY", delay_s=0.3)
        # Apply mitigation
        self.manager.set_mitigation(enabled=True)

        res = self.manager.dispatch_request()
        self.assertEqual(res["status_code"], 200)
        # Should be served via fallback cache in ServiceB without calling ServiceC
        self.assertLess(res["elapsed_ms"], 50.0)


class TestResetAndCleanup(unittest.TestCase):
    def test_reset_runs_twice_idempotently(self) -> None:
        # First run
        count1 = reset_m20_environment(verbose=False)
        self.assertIsInstance(count1, int)
        # Second run immediately following
        count2 = reset_m20_environment(verbose=False)
        self.assertEqual(count2, 0)

    def test_reset_fails_closed_on_os_error(self) -> None:
        with mock.patch("os.remove", side_effect=OSError("Permission Denied (Simulated)")):
            scratch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".scratch")
            os.makedirs(scratch_dir, exist_ok=True)
            dummy_file = os.path.join(scratch_dir, "dummy_test.json")
            with open(dummy_file, "w") as f:
                f.write("{}")

            with self.assertRaises(RuntimeError) as ctx:
                reset_m20_environment(verbose=False)
            self.assertIn("M20 cleanup incomplete", str(ctx.exception))

            # Clean up dummy file manually
            if os.path.exists(dummy_file):
                os.remove(dummy_file)


class TestBlamelessPostmortemFormat(unittest.TestCase):
    def test_postmortem_generation_contains_required_sections(self) -> None:
        pm = generate_blameless_postmortem(
            incident_id="INC-TEST-001",
            impact_summary="Test outage impact",
            timeline_entries=[("T0", "Alert triggered"), ("T1", "Mitigated")],
            proximate_mechanism="Injected delay in storage mock",
            contributing_conditions=["Missing timeout limit", "No fallback cache"],
            mitigation_applied="Activated local fallback bypass",
            permanent_safeguards=["Add circuit breaker", "Enforce traceparent"],
            unresolved_questions=["Cache invalidation horizon"],
        )
        self.assertIn("# Incident Postmortem: INC-TEST-001", pm)
        self.assertIn("BLAMELESS POSTMORTEM", pm)
        self.assertIn("Contributing Systemic Conditions", pm)
        self.assertIn("Mitigation vs. Resolution Distinction", pm)
        self.assertIn("Exact Inference Limits", pm)
        self.assertNotIn("Bob forgot", pm)


if __name__ == "__main__":
    unittest.main()
