#!/usr/bin/env python3
"""
activity_l20_01.py — Lesson L20-01 Hands-On Activity
====================================================

Lesson: L20-01 — "How do I know the system is OK?"
Focus:
1. Clock Semantics: Monotonic elapsed duration vs. adjustable wall-clock timestamps.
2. Distribution Statistics: Mean vs. Tail Latency (p50, p90, p95, p99) under nearest_rank convention.
3. SLI / SLO / Error Budget Evaluation from explicit scenario inputs.

Outputs:
- labs/foundations/m20/.scratch/l20_01_observation.json
"""

import json
import os
import sys
import time

from s6_m20_observability_pipeline import (
    ClockAdapter,
    compute_distribution_statistics,
    compute_elapsed_duration_ms,
    evaluate_sli_slo,
)


def run_activity_l20_01() -> int:
    scratch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".scratch")
    os.makedirs(scratch_dir, exist_ok=True)
    out_file = os.path.join(scratch_dir, "l20_01_observation.json")

    print("=" * 70)
    print(" Essential CS -- Activity L20-01: Clock Semantics & Telemetry Foundations")
    print("=" * 70)

    # ------------------------------------------------------------------------
    # Part 1: Clock Semantics & Fake Wall-Clock Adjustment
    # ------------------------------------------------------------------------
    print("\n[STEP 1: Clock Semantics & Interval Timing Invariant]")
    adapter = ClockAdapter()

    t_wall_0 = adapter.wall_time()
    t_mono_0 = adapter.monotonic_time()

    # Emulate a small real elapsed interval
    time.sleep(0.04)

    # Inject fake wall-clock adjustment (e.g. stepping backward by 5 seconds)
    # Note: Host system clock is untouched; this is a simulated adapter step.
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

    # Assert invariant in learner runtime
    assert wall_duration_s < 0, "Expected wall duration subtraction to be negative under backward adjustment."
    assert mono_duration_ms > 0, "Expected monotonic duration to remain strictly positive."

    # ------------------------------------------------------------------------
    # Part 2: Distribution Statistics (Tail vs. Mean)
    # ------------------------------------------------------------------------
    print("\n[STEP 2: Request Distribution Statistics (Tail vs. Mean)]")
    # Configurable deterministic course workload:
    # 95 typical requests (around 4-6 ms) and 5 queuing tail requests (200-500 ms)
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
    print(f" - Percentile Convention:   {stats['convention_description']}")

    # ------------------------------------------------------------------------
    # Part 3: SLI / SLO / Error Budget Evaluation
    # ------------------------------------------------------------------------
    print("\n[STEP 3: SLI / SLO & Error Budget Worksheet]")
    # Scenario: 50,000 valid requests in 30-day window, 49,910 successful requests, 99.9% SLO target
    scenario_total_requests = 50000
    scenario_good_requests = 49910
    scenario_slo_target = 99.9

    sli_eval = evaluate_sli_slo(
        total_valid_requests=scenario_total_requests,
        good_requests=scenario_good_requests,
        slo_target_percent=scenario_slo_target,
    )

    print(f" - Valid Events:            {sli_eval['total_valid_requests']}")
    print(f" - Good Events:             {sli_eval['good_requests']}")
    print(f" - Actual SLI (Ratio):      {sli_eval['actual_sli_percent']}%")
    print(f" - Target SLO:              {sli_eval['slo_target_percent']}%")
    print(f" - SLO Objective Met?:      {sli_eval['slo_met']}")
    print(f" - Allowed Bad Events:      {sli_eval['allowed_bad_requests']}")
    print(f" - Actual Bad Events:       {sli_eval['bad_requests']}")
    print(f" - Remaining Budget:        {sli_eval['remaining_budget_requests']} requests")
    print(f" - Budget Consumed:         {sli_eval['budget_consumed_percent']}%")
    print(f" - Allowed Downtime (30d):  {sli_eval['allowed_downtime_minutes_in_window']} minutes")

    # ------------------------------------------------------------------------
    # Save Observation Record
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
                "wall_time": "CLOCK_REALTIME / time.time() (adjustable)",
                "monotonic_time": "CLOCK_MONOTONIC / time.monotonic() (steady)",
            },
        },
        "distribution_statistics": stats,
        "sli_slo_evaluation": sli_eval,
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(observation, f, indent=2, ensure_ascii=False)

    print(f"\n[EVIDENCE] Observation recorded in: {out_file}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(run_activity_l20_01())
