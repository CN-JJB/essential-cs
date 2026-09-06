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

import io
import json
import os
import sys
import subprocess
import time
import unittest
from unittest import mock

# Ensure labs/foundations/m20 is in sys.path for direct or root execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from reset import reset_m20_environment
from s6_m20_observability_pipeline import (
    ClockAdapter,
    ObservabilityPipelineManager,
    OwnedSubprocessWatchdog,
    StructuredLogger,
    compute_distribution_statistics,
    compute_elapsed_duration_ms,
    evaluate_request_sli_slo,
    evaluate_sli_slo,
    evaluate_time_availability_sli_slo,
    generate_blameless_postmortem,
    generate_span_id,
    generate_trace_id,
    generate_traceparent,
    parse_traceparent,
    reconstruct_correlated_timeline,
    sanitize_privacy_fields,
)


class TestClockSemantics(unittest.TestCase):
    def test_monotonic_clock_increases_linearly(self) -> None:
        adapter = ClockAdapter()
        t0 = adapter.monotonic_time()
        time.sleep(0.01)
        t1 = adapter.monotonic_time()
        self.assertGreater(t1, t0)
        dur = compute_elapsed_duration_ms(t0, t1)
        self.assertGreater(dur, 0.0)

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
        self.assertGreater(compute_elapsed_duration_ms(m0, m1), 0.0)

    def test_negative_step_validation(self) -> None:
        adapter = ClockAdapter()
        with self.assertRaises(ValueError):
            adapter.inject_wall_step_backward(-5.0)


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


class TestDecoupledSliSloEvaluator(unittest.TestCase):
    def test_request_sli_slo_evaluation_success(self) -> None:
        res = evaluate_request_sli_slo(
            total_valid_requests=10000,
            good_requests=9995,
            slo_target_percent=99.9,
        )
        self.assertEqual(res["sli_dimension"], "request_event")
        self.assertEqual(res["actual_sli_percent"], 99.95)
        self.assertTrue(res["slo_met"])
        self.assertEqual(res["allowed_bad_requests"], 10.0)
        self.assertEqual(res["bad_requests"], 5)
        self.assertEqual(res["remaining_budget_requests"], 5.0)
        self.assertEqual(res["budget_consumed_percent"], 50.0)
        # Ensure request SLI does NOT emit downtime minutes
        self.assertNotIn("allowed_downtime_minutes_in_window", res)
        self.assertNotIn("allowed_downtime_minutes", res)

    def test_request_sli_slo_budget_exhaustion(self) -> None:
        res = evaluate_request_sli_slo(
            total_valid_requests=10000,
            good_requests=9980,
            slo_target_percent=99.9,
        )
        self.assertEqual(res["actual_sli_percent"], 99.8)
        self.assertFalse(res["slo_met"])
        self.assertEqual(res["bad_requests"], 20)
        self.assertEqual(res["budget_consumed_percent"], 200.0)
        self.assertIn("policy_note", res)

    def test_backward_compatible_wrapper(self) -> None:
        res = evaluate_sli_slo(
            total_valid_requests=10000,
            good_requests=9995,
            slo_target_percent=99.9,
        )
        self.assertEqual(res["sli_dimension"], "request_event")
        self.assertEqual(res["actual_sli_percent"], 99.95)
        self.assertNotIn("allowed_downtime_minutes", res)

    def test_time_availability_sli_slo_evaluation(self) -> None:
        # 30-day window = 2,592,000s; 20 min downtime = 1200s downtime; 2,590,800s uptime
        res = evaluate_time_availability_sli_slo(
            total_window_seconds=2592000.0,
            uptime_seconds=2590800.0,
            slo_target_percent=99.9,
        )
        self.assertEqual(res["sli_dimension"], "time_duration")
        self.assertAlmostEqual(res["actual_availability_percent"], 99.9537, places=4)
        self.assertTrue(res["slo_met"])
        self.assertEqual(res["allowed_downtime_minutes"], 43.2)
        self.assertEqual(res["downtime_minutes"], 20.0)
        self.assertEqual(res["remaining_downtime_minutes"], 23.2)
        self.assertAlmostEqual(res["budget_consumed_percent"], 46.3, places=1)

    def test_invalid_parameters_raise(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_request_sli_slo(0, 0, 99.0)
        with self.assertRaises(ValueError):
            evaluate_request_sli_slo(100, 105, 99.0)
        with self.assertRaises(ValueError):
            evaluate_request_sli_slo(100, 90, 105.0)
        with self.assertRaises(ValueError):
            evaluate_time_availability_sli_slo(0.0, 0.0, 99.0)
        with self.assertRaises(ValueError):
            evaluate_time_availability_sli_slo(100.0, 105.0, 99.0)


class TestW3CTraceContextStrict(unittest.TestCase):
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

    def test_unified_trace_id_and_span_id_generators(self) -> None:
        tid = generate_trace_id()
        self.assertEqual(len(tid), 32)
        self.assertNotEqual(tid, "00000000000000000000000000000000")
        int(tid, 16)  # must be valid hex

        sid = generate_span_id()
        self.assertEqual(len(sid), 16)
        self.assertNotEqual(sid, "0000000000000000")
        int(sid, 16)  # must be valid hex

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

    def test_version_not_00_rejected(self) -> None:
        # Version 01 must be rejected (Requirement 4 regression test)
        with self.assertRaises(ValueError) as ctx1:
            parse_traceparent("01-4bf92f3577b34da6a3ce929d0e0e4736-1234567812345678-01")
        self.assertIn("Unsupported or invalid traceparent version", str(ctx1.exception))

        # Version ff must be rejected
        with self.assertRaises(ValueError) as ctx2:
            parse_traceparent("ff-4bf92f3577b34da6a3ce929d0e0e4736-1234567812345678-01")
        self.assertIn("Unsupported or invalid traceparent version", str(ctx2.exception))

    def test_invalid_length_and_characters_rejected(self) -> None:
        # Wrong character count for version 00
        with self.assertRaises(ValueError):
            parse_traceparent("00-4bf92f3577b34da6a3ce929d0e0e4736-1234567812345678-01-extra")

        # Non-hex characters
        with self.assertRaises(ValueError):
            parse_traceparent("00-4bf92f3577b34da6a3ce929d0e0e47zz-1234567812345678-01")


class TestStructuredLoggerAndSink(unittest.TestCase):
    def test_logger_emits_valid_parseable_json_to_sink(self) -> None:
        stream = io.StringIO()
        logger = StructuredLogger(sink_stream=stream)

        trace_id = generate_trace_id()
        span_id = generate_span_id()
        record = logger.log(
            service="TestService",
            event="test_event",
            trace_id=trace_id,
            span_id=span_id,
            duration_ms=12.345,
            status="OK",
            details={"key": "val"},
        )

        emitted_lines = logger.get_emitted_json_lines()
        self.assertEqual(len(emitted_lines), 1)

        # Parse emitted JSON string
        parsed = json.loads(emitted_lines[0])
        self.assertEqual(parsed["service"], "TestService")
        self.assertEqual(parsed["event"], "test_event")
        self.assertEqual(parsed["trace_id"], trace_id)
        self.assertEqual(parsed["span_id"], span_id)
        self.assertEqual(parsed["duration_ms"], 12.345)
        self.assertIn("timestamp_utc", parsed)
        self.assertIn("timestamp_wall_epoch_s", parsed)
        self.assertEqual(parsed["details"], {"key": "val"})

        # Stream sink received matching line
        stream_content = stream.getvalue()
        self.assertTrue(stream_content.endswith("\n"))
        stream_parsed = json.loads(stream_content.strip())
        self.assertEqual(stream_parsed["trace_id"], trace_id)

    def test_logger_file_sink_jsonl(self) -> None:
        scratch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".scratch")
        os.makedirs(scratch_dir, exist_ok=True)
        test_jsonl = os.path.join(scratch_dir, "test_sink_events.jsonl")
        if os.path.exists(test_jsonl):
            os.remove(test_jsonl)

        try:
            logger = StructuredLogger(jsonl_path=test_jsonl)
            trace_id = generate_trace_id()
            logger.log(service="FileSinkService", event="file_event", trace_id=trace_id)

            self.assertTrue(os.path.exists(test_jsonl))
            with open(test_jsonl, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            self.assertEqual(len(lines), 1)
            parsed = json.loads(lines[0])
            self.assertEqual(parsed["service"], "FileSinkService")
            self.assertEqual(parsed["trace_id"], trace_id)
        finally:
            if os.path.exists(test_jsonl):
                os.remove(test_jsonl)

    def test_recursive_privacy_sanitizer(self) -> None:
        # Complex nested structure with case-insensitivity and Bearer values
        raw_data = {
            "user": "alice",
            "PASSWORD": "plaintext_password",
            "Auth_Header": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            "nested": {
                "secret_key": "12345",
                "session_COOKIE": "session=abc",
                "allowed_flag": True,
                "user_token": "secret_token_123",
                "safe_list": ["Bearer secret-token-abc", "normal_string"],
            },
            "services_config": [
                {"db_password": "sql_pass", "db_host": "127.0.0.1"},
                "Bearer standalone_token",
            ],
        }

        sanitized = sanitize_privacy_fields(raw_data)

        self.assertEqual(sanitized["user"], "alice")
        self.assertEqual(sanitized["PASSWORD"], "[REDACTED]")
        self.assertEqual(sanitized["Auth_Header"], "[REDACTED]")
        self.assertEqual(sanitized["nested"]["secret_key"], "[REDACTED]")
        self.assertEqual(sanitized["nested"]["session_COOKIE"], "[REDACTED]")
        self.assertEqual(sanitized["nested"]["user_token"], "[REDACTED]")
        self.assertTrue(sanitized["nested"]["allowed_flag"])
        self.assertEqual(sanitized["nested"]["safe_list"][0], "Bearer [REDACTED]")
        self.assertEqual(sanitized["nested"]["safe_list"][1], "normal_string")
        self.assertEqual(sanitized["services_config"][0]["db_password"], "[REDACTED]")
        self.assertEqual(sanitized["services_config"][0]["db_host"], "127.0.0.1")
        self.assertEqual(sanitized["services_config"][1], "Bearer [REDACTED]")


class TestThreeServicePipelineIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ObservabilityPipelineManager(watchdog_timeout_s=30.0)
        self.manager.start()

    def tearDown(self) -> None:
        if self.manager._is_running:
            self.manager.shutdown()

    def test_normal_end_to_end_request(self) -> None:
        res = self.manager.dispatch_request()
        self.assertEqual(res["status_code"], 200)
        self.assertIn("trace_id", res["response"])

        trace_id = res["response"]["trace_id"]
        records = self.manager.logger.filter_by_trace_id(trace_id)
        services_seen = {r["service"] for r in records}
        self.assertEqual(services_seen, {"ServiceA", "ServiceB", "ServiceC"})

    def test_fault_injection_delay_and_relative_localization(self) -> None:
        # Inject 200ms delay in ServiceC
        self.manager.set_fault(fault_mode="DELAY", delay_s=0.20)
        res = self.manager.dispatch_request()

        self.assertEqual(res["status_code"], 200)

        trace_id = res["response"]["trace_id"]
        timeline = reconstruct_correlated_timeline(
            self.manager.logger.get_records(), trace_id
        )
        # Verify localization uses relative concentration or degraded status, not fixed 200ms
        self.assertIsNotNone(timeline["fault_localized"])
        self.assertEqual(timeline["fault_localized"], "ServiceC")
        self.assertIn("fixture_ground_truth", timeline)
        self.assertIn("production_inference_boundary", timeline)
        self.assertIsNotNone(timeline["diagnostic_inference"])

        # Check injected fault event metadata in correlated records
        c_records = [r for r in timeline["records"] if r.get("service") == "ServiceC"]
        self.assertTrue(len(c_records) >= 1)
        fault_events = [r for r in c_records if r.get("event") == "injected_delay_started"]
        self.assertEqual(len(fault_events), 1)
        self.assertEqual(fault_events[0].get("status"), "DEGRADED")
        self.assertEqual(fault_events[0].get("details", {}).get("delay_s"), 0.20)

        # Causal ordering: ServiceA dispatch -> ServiceB receive -> ServiceC receive
        services_order = [r.get("service") for r in timeline["records"] if r.get("status") == "START"]
        self.assertEqual(services_order, ["ServiceA", "ServiceB", "ServiceC"])

    def test_fault_injection_http_500_mode(self) -> None:
        self.manager.set_fault(fault_mode="HTTP_500")
        res = self.manager.dispatch_request()
        # Without mitigation, ServiceB propagates downstream error to ServiceA
        self.assertIn(res["status_code"], (500, 502))

    def test_fault_injection_parameter_validation(self) -> None:
        # Unknown mode rejected
        with self.assertRaises(ValueError) as ctx1:
            self.manager.set_fault(fault_mode="UNSUPPORTED_MODE")
        self.assertIn("Unsupported fault_mode", str(ctx1.exception))

        # Negative delay rejected
        with self.assertRaises(ValueError) as ctx2:
            self.manager.set_fault(fault_mode="DELAY", delay_s=-0.5)
        self.assertIn("cannot be negative", str(ctx2.exception))

        # Unsafe delay rejected
        with self.assertRaises(ValueError) as ctx3:
            self.manager.set_fault(fault_mode="DELAY", delay_s=10.0)
        self.assertIn("exceeds maximum safety bound", str(ctx3.exception))

    def test_safe_mitigation_recovers_latency(self) -> None:
        self.manager.set_fault(fault_mode="DELAY", delay_s=0.25)
        incident_res = self.manager.dispatch_request()

        self.manager.set_mitigation(enabled=True)
        mitigated_res = self.manager.dispatch_request()

        self.assertEqual(mitigated_res["status_code"], 200)

        # Verify ServiceB cache fallback event is present and ServiceC is absent from mitigated trace
        mitigated_trace_id = mitigated_res["response"]["trace_id"]
        mitigated_records = self.manager.logger.filter_by_trace_id(mitigated_trace_id)
        mitigated_services = {r["service"] for r in mitigated_records}
        self.assertIn("ServiceA", mitigated_services)
        self.assertIn("ServiceB", mitigated_services)
        self.assertNotIn("ServiceC", mitigated_services)

        fallback_events = [r for r in mitigated_records if r.get("event") == "mitigation_cache_served"]
        self.assertEqual(len(fallback_events), 1)

        # Relative latency verification (mitigated faster than degraded without absolute threshold)
        self.assertLess(mitigated_res["elapsed_ms"], incident_res["elapsed_ms"])


class TestLifecycleAndSafety(unittest.TestCase):
    def test_pipeline_shutdown_fails_closed_on_error(self) -> None:
        manager = ObservabilityPipelineManager(watchdog_timeout_s=5.0)
        manager.start()
        self.assertTrue(manager._is_running)

        # Mock server_close on server_c to raise an error
        with mock.patch.object(manager.server_c, "server_close", side_effect=OSError("Simulated socket close failure")):
            with self.assertRaises(RuntimeError) as ctx:
                manager.shutdown()
            self.assertIn("Pipeline shutdown failed", str(ctx.exception))
            self.assertIn("ServiceC server close error", str(ctx.exception))
            # State remains True (fails closed, does not wipe state)
            self.assertTrue(manager._is_running)

        # Clean shutdown without mock
        manager.shutdown()
        self.assertFalse(manager._is_running)


class TestOwnedSubprocessWatchdog(unittest.TestCase):
    def test_child_normal_completion_and_reap(self) -> None:
        watchdog = OwnedSubprocessWatchdog(timeout_s=15.0)
        pipeline_path = os.path.join(_current_dir, "s6_m20_observability_pipeline.py")
        res = watchdog.run([sys.executable, pipeline_path, "--child-fixture"])

        self.assertEqual(res["status"], "PASS")
        self.assertFalse(res["watchdog_triggered"])
        self.assertTrue(res["reaped"])
        self.assertEqual(res["returncode"], 0)
        self.assertIsNone(res["cleanup_failure"])
        self.assertIsNotNone(res["data"])
        self.assertEqual(res["data"]["status"], "PASS")
        # Zero leftover process
        self.assertFalse(OwnedSubprocessWatchdog._is_pid_alive(res["child_pid"]))

    def test_watchdog_timeout_terminates_and_reaps_owned_child(self) -> None:
        watchdog = OwnedSubprocessWatchdog(timeout_s=0.6)
        pipeline_path = os.path.join(_current_dir, "s6_m20_observability_pipeline.py")
        res = watchdog.run([sys.executable, pipeline_path, "--child-fixture", "--simulate-hang"])

        self.assertEqual(res["status"], "TIMEOUT")
        self.assertTrue(res["watchdog_triggered"])
        self.assertTrue(res["reaped"])
        self.assertIsNotNone(res["returncode"])
        # Zero leftover process
        self.assertFalse(OwnedSubprocessWatchdog._is_pid_alive(res["child_pid"]))

    def test_cleanup_failure_is_surfaced(self) -> None:
        watchdog = OwnedSubprocessWatchdog(timeout_s=15.0)
        pipeline_path = os.path.join(_current_dir, "s6_m20_observability_pipeline.py")
        res = watchdog.run([sys.executable, pipeline_path, "--child-fixture", "--simulate-cleanup-failure"])

        self.assertEqual(res["status"], "CLEANUP_FAILURE")
        self.assertFalse(res["watchdog_triggered"])
        self.assertTrue(res["reaped"])
        self.assertIsNotNone(res["cleanup_failure"])
        self.assertIn("Simulated server close error during child cleanup", res["cleanup_failure"])
        # Zero leftover process
        self.assertFalse(OwnedSubprocessWatchdog._is_pid_alive(res["child_pid"]))

    def test_truthful_outcome_reporting(self) -> None:
        watchdog = OwnedSubprocessWatchdog(timeout_s=15.0)
        pipeline_path = os.path.join(_current_dir, "s6_m20_observability_pipeline.py")

        res_blocked = watchdog.run([sys.executable, pipeline_path, "--child-fixture", "--simulate-blocked"])
        self.assertEqual(res_blocked["status"], "BLOCKED")
        self.assertTrue(res_blocked["reaped"])
        self.assertFalse(OwnedSubprocessWatchdog._is_pid_alive(res_blocked["child_pid"]))

        res_not_run = watchdog.run([sys.executable, pipeline_path, "--child-fixture", "--simulate-not-run"])
        self.assertEqual(res_not_run["status"], "NOT RUN")
        self.assertTrue(res_not_run["reaped"])
        self.assertFalse(OwnedSubprocessWatchdog._is_pid_alive(res_not_run["child_pid"]))

    def test_unrelated_process_not_killed(self) -> None:
        # Launch an independent dummy process
        unrelated = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(10)"]
        )
        try:
            self.assertIsNone(unrelated.poll())
            watchdog = OwnedSubprocessWatchdog(timeout_s=0.5)
            pipeline_path = os.path.join(_current_dir, "s6_m20_observability_pipeline.py")
            res = watchdog.run([sys.executable, pipeline_path, "--child-fixture", "--simulate-hang"])
            self.assertEqual(res["status"], "TIMEOUT")
            self.assertTrue(res["reaped"])

            # Verify the unrelated process is STILL running and was NOT killed
            self.assertIsNone(unrelated.poll())
        finally:
            unrelated.kill()
            unrelated.wait()


class TestResetAndCleanup(unittest.TestCase):
    def test_reset_runs_twice_idempotently(self) -> None:
        count1 = reset_m20_environment(verbose=False)
        self.assertIsInstance(count1, int)
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

            if os.path.exists(dummy_file):
                os.remove(dummy_file)


class TestBlamelessPostmortemFormat(unittest.TestCase):
    def test_postmortem_generation_evidence_driven(self) -> None:
        pm = generate_blameless_postmortem(
            incident_id="INC-TEST-001",
            impact_summary="Test outage impact",
            timeline_entries=[
                ("T0 (Fault)", "Fixture injected DELAY 200ms"),
                ("T1 (Mitigation)", "Enabled fallback cache"),
                ("T2 (Resolution)", "NOT PERFORMED / PROPOSED FOLLOW-UP"),
            ],
            proximate_mechanism="Injected delay in storage mock",
            contributing_conditions=["Missing timeout limit", "No fallback cache"],
            mitigation_applied="Activated local fallback bypass",
            recovery_status="PASS",
            recovery_evidence="Mitigated request returned HTTP 200 in 3.5ms",
            resolution_status="NOT PERFORMED / PROPOSED FOLLOW-UP",
            resolution_plan="Proposed database connection pool tuning in production.",
            permanent_safeguards=["Add circuit breaker", "Enforce traceparent"],
            unresolved_questions=["Cache invalidation horizon"],
        )
        self.assertIn("# Incident Postmortem: INC-TEST-001", pm)
        self.assertIn("BLAMELESS POSTMORTEM", pm)
        self.assertIn("Recovery Verification Status**: PASS", pm)
        self.assertIn("Recovery Observable Evidence**: Mitigated request returned HTTP 200 in 3.5ms", pm)
        self.assertIn("Resolution Status**: `NOT PERFORMED / PROPOSED FOLLOW-UP`", pm)
        self.assertNotIn("Bob forgot", pm)
        # Confirm no fabricated facts
        self.assertNotIn("connection pool tuned; root lock contention resolved", pm)

    def test_postmortem_generation_rejects_invalid_recovery_status(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            generate_blameless_postmortem(
                incident_id="INC-TEST-002",
                impact_summary="Test impact",
                timeline_entries=[],
                proximate_mechanism="none",
                contributing_conditions=[],
                mitigation_applied="none",
                recovery_status="INVALID_STATUS",
                recovery_evidence="none",
            )
        self.assertIn("Invalid recovery_status", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
