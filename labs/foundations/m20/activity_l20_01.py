#!/usr/bin/env python3
"""
activity_l20_01.py — Lesson L20-01 Hands-On Activity
====================================================

Lesson: L20-01 — "How do I know the system is OK?"
Focus:
1. Clock Semantics: Monotonic elapsed duration vs. adjustable wall-clock timestamps.
2. Distribution Statistics: Mean vs. Tail Latency (p50, p90, p95, p99) under nearest_rank convention.
   (Understanding that request latency percentile != percentage of users).
3. Decoupled SLI / SLO / Error Budget Evaluation:
   - Request-event SLI generates request-count error budget (never downtime minutes).
   - Time-based availability SLI is evaluated as an independent duration scenario.
   - Error budget exhaustion is a mathematical status; operational action depends on team policy.
4. Structured Logging with real JSON sink emission to scratch JSONL.

Outputs:
- labs/foundations/m20/.scratch/l20_01_observation.json
- labs/foundations/m20/.scratch/l20_01_events.jsonl
"""

import json
import os
import sys
import time

from s6_m20_observability_pipeline import (
    ClockAdapter,
    StructuredLogger,
    compute_distribution_statistics,
    compute_elapsed_duration_ms,
    evaluate_request_sli_slo,
    evaluate_time_availability_sli_slo,
    generate_trace_id,
)


def run_activity_l20_01() -> int:
    scratch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".scratch")
    os.makedirs(scratch_dir, exist_ok=True)
    out_file = os.path.join(scratch_dir, "l20_01_observation.json")
    jsonl_log_path = os.path.join(scratch_dir, "l20_01_events.jsonl")

    print("=" * 70)
    print(" Essential CS -- Activity L20-01: Clock Semantics & Telemetry Foundations")
    print("=" * 70)

    # ------------------------------------------------------------------------
    # Part 1: Clock Semantics & Simulated Wall-Clock Adjustment
    # ------------------------------------------------------------------------
    print("\n[STEP 1: Clock Semantics & Interval Timing Invariant]")
    adapter = ClockAdapter()

    t_wall_0 = adapter.wall_time()
    t_mono_0 = adapter.monotonic_time()

    # Small elapsed interval for relative timing
    time.sleep(0.03)

    # Inject backward adjustment into teaching wall-clock adapter
    injected_wall_step = 5.0
    adapter.inject_wall_step_backward(injected_wall_step)

    t_wall_1 = adapter.wall_time()
    t_mono_1 = adapter.monotonic_time()

    wall_duration_s = t_wall_1 - t_wall_0
    mono_duration_ms = compute_elapsed_duration_ms(t_mono_0, t_mono_1)

    print(f" - Wall Time T0:            {t_wall_0:.4f}")
    print(f" - Wall Time T1:            {t_wall_1:.4f} (Adjusted by -{injected_wall_step}s)")
    print(f" - Wall Subtraction Result: {wall_duration_s:.4f}s (NEGATIVE / INVALID DURATION!)")
    print(f" - Monotonic Duration:      {mono_duration_ms:.2f}ms (POSITIVE / VALID DURATION)")

    # Explicit runtime gates (no assert)
    if wall_duration_s >= 0:
        raise RuntimeError(
            f"Invariant violation: wall duration expected negative under backward adjustment, got {wall_duration_s}"
        )
    if mono_duration_ms <= 0:
        raise RuntimeError(
            f"Invariant violation: monotonic duration must remain strictly positive, got {mono_duration_ms}"
        )

    # ------------------------------------------------------------------------
    # Part 2: Distribution Statistics (Tail vs. Mean)
    # ------------------------------------------------------------------------
    print("\n[STEP 2: Request Distribution Statistics (Tail vs. Mean)]")
    # Workload: 95 typical requests (4-6 ms) and 5 queuing tail requests (200-500 ms)
    synthetic_workload = [
        4.2, 4.5, 4.8, 5.0, 5.1, 4.9, 5.2, 4.7, 5.3, 5.0,
        4.6, 5.1, 4.8, 5.2, 5.0, 4.9, 4.7, 5.3, 5.1, 4.8,
        5.0, 4.9, 5.2, 4.6, 5.1, 4.8, 5.0, 5.3, 4.7, 5.2,
        4.9, 5.0, 4.8, 5.1, 4.6, 5.2, 5.0, 4.9, 4.7, 5.3,
        5.1, 4.8, 5.0, 4.9, 5.2, 4.6, 5.1, 4.8, 5.0, 5.3,
        4.7, 5.2, 4.9, 5.0, 4.8, 5.1, 4.6, 5.2, 5.0, 4.9,
        4.7, 5.3, 5.1, 4.8, 5.0, 4.9, 5.2, 4.6, 5.1, 4.8,
        5.0, 5.3, 4.7, 5.2, 4.9, 5.0, 4.8, 5.1, 4.6, 5.2,
        5.0, 4.9, 4.7, 5.3, 5.1, 4.8, 5.0, 4.9, 5.2, 4.6,
        5.1, 4.8, 5.0, 5.3, 4.7,
        210.0, 245.0, 320.0, 410.0, 495.0,  # 5 tail requests
    ]

    stats = compute_distribution_statistics(synthetic_workload, convention="nearest_rank")
    print(f" - Sample Count:            {stats['sample_count']}")
    print(f" - Mean Latency:            {stats['mean_ms']} ms")
    print(f" - Median (p50):            {stats['p50_ms']} ms")
    print(f" - 90th Percentile (p90):   {stats['p90_ms']} ms")
    print(f" - 95th Percentile (p95):   {stats['p95_ms']} ms")
    print(f" - 99th Percentile (p99):   {stats['p99_ms']} ms (Tail Latency Divergence)")
    print(f" - Percentile Note:         Request percentile != user percentage (power-users issue more requests)")

    # ------------------------------------------------------------------------
    # Part 3: Decoupled SLI / SLO & Error Budget Evaluation
    # ------------------------------------------------------------------------
    print("\n[STEP 3: Decoupled SLI / SLO & Error Budget Worksheets]")

    # Scenario A: Request-based Event SLI (discrete requests only)
    scenario_requests_total = 50000
    scenario_requests_good = 49910
    scenario_requests_slo_target = 99.9

    req_sli_eval = evaluate_request_sli_slo(
        total_valid_requests=scenario_requests_total,
        good_requests=scenario_requests_good,
        slo_target_percent=scenario_requests_slo_target,
    )

    print(" [Scenario A: Request-based Event SLI]")
    print(f"   * Valid Requests:         {req_sli_eval['total_valid_requests']}")
    print(f"   * Good Requests:          {req_sli_eval['good_requests']}")
    print(f"   * Actual SLI (Ratio):     {req_sli_eval['actual_sli_percent']}%")
    print(f"   * Target SLO:             {req_sli_eval['slo_target_percent']}%")
    print(f"   * SLO Objective Met?:     {req_sli_eval['slo_met']}")
    print(f"   * Allowed Bad Requests:   {req_sli_eval['allowed_bad_requests']}")
    print(f"   * Actual Bad Requests:    {req_sli_eval['bad_requests']}")
    print(f"   * Remaining Budget:       {req_sli_eval['remaining_budget_requests']} requests")
    print(f"   * Budget Consumed:        {req_sli_eval['budget_consumed_percent']}%")
    print(f"   * Dimensional Note:       {req_sli_eval['dimensional_boundary']}")
    print(f"   * Policy Status Note:     {req_sli_eval['policy_note']}")

    # Scenario B: Time-based Availability SLI (independent duration model)
    scenario_window_days = 30
    scenario_window_seconds = scenario_window_days * 24 * 3600.0  # 2,592,000s
    scenario_uptime_seconds = scenario_window_seconds - 1200.0   # 20 minutes downtime
    scenario_time_slo_target = 99.9

    time_sli_eval = evaluate_time_availability_sli_slo(
        total_window_seconds=scenario_window_seconds,
        uptime_seconds=scenario_uptime_seconds,
        slo_target_percent=scenario_time_slo_target,
    )

    print("\n [Scenario B: Time-based Availability SLI (Independent Scenario)]")
    print(f"   * Total Window Seconds:   {time_sli_eval['total_window_seconds']}s (30 days)")
    print(f"   * Actual Uptime Seconds:  {time_sli_eval['uptime_seconds']}s")
    print(f"   * Actual Availability:    {time_sli_eval['actual_availability_percent']}%")
    print(f"   * Target SLO:             {time_sli_eval['slo_target_percent']}%")
    print(f"   * Allowed Downtime:       {time_sli_eval['allowed_downtime_minutes']} minutes")
    print(f"   * Actual Downtime:        {time_sli_eval['downtime_minutes']} minutes")
    print(f"   * Remaining Time Budget:  {time_sli_eval['remaining_downtime_minutes']} minutes")
    print(f"   * Time Budget Consumed:   {time_sli_eval['budget_consumed_percent']}%")

    # ------------------------------------------------------------------------
    # Part 4: Structured Logger & Real JSON Sink Demonstration
    # ------------------------------------------------------------------------
    print("\n[STEP 4: Structured JSON Logger & Sink Verification]")
    logger = StructuredLogger(service_name="l20_01_service", jsonl_path=jsonl_log_path)
    sample_trace_id = generate_trace_id()
    logger.log(
        service="l20_01_service",
        event="telemetry_initialized",
        trace_id=sample_trace_id,
        duration_ms=mono_duration_ms,
        status="OK",
        details={
            "authorization_header": "Bearer secret-demo-token",
            "p99_ms": stats["p99_ms"],
            "request_budget_consumed_percent": req_sli_eval["budget_consumed_percent"],
        },
    )

    # Verify JSON sink emitted valid parseable JSON lines
    emitted_lines = logger.get_emitted_json_lines()
    if not emitted_lines:
        raise RuntimeError("StructuredLogger failed to emit JSON lines to sink.")
    parsed_record = json.loads(emitted_lines[-1])
    if parsed_record.get("trace_id") != sample_trace_id:
        raise RuntimeError(f"JSON sink trace_id mismatch: {parsed_record.get('trace_id')} != {sample_trace_id}")
    if parsed_record["details"].get("authorization_header") != "[REDACTED]":
        raise RuntimeError("StructuredLogger failed to redact sensitive authorization_header in JSON sink.")
    print(f" - JSON Sink Verified: {len(emitted_lines)} line(s) emitted to {jsonl_log_path}")
    print(f" - Sample JSON Sink Record: {emitted_lines[-1]}")

    # ------------------------------------------------------------------------
    # Save Final Observation Record
    # ------------------------------------------------------------------------
    observation = {
        "activity": "L20-01",
        "clock_semantics": {
            "wall_t0": t_wall_0,
            "wall_t1": t_wall_1,
            "injected_wall_step_s": injected_wall_step,
            "wall_subtraction_s": round(wall_duration_s, 6),
            "monotonic_duration_ms": round(mono_duration_ms, 4),
            "wall_is_negative": wall_duration_s < 0,
            "monotonic_is_positive": mono_duration_ms > 0,
            "clock_source_labels": {
                "wall_time": "time.time() (adjustable system clock)",
                "monotonic_time": "time.monotonic() (steady, cannot go backwards)",
            },
        },
        "distribution_statistics": stats,
        "request_sli_slo_evaluation": req_sli_eval,
        "time_availability_sli_slo_evaluation": time_sli_eval,
        "structured_json_sink": {
            "jsonl_path": jsonl_log_path,
            "emitted_lines_count": len(emitted_lines),
            "sample_record": parsed_record,
        },
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(observation, f, indent=2, ensure_ascii=False)

    print(f"\n[EVIDENCE] Observation recorded in: {out_file}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(run_activity_l20_01())
