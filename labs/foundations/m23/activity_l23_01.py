#!/usr/bin/env python3
"""
activity_l23_01.py — Question-Driven Systems Measurement & Coordinated Omission Harness
========================================================================================

Canonical Module: M23 — Systems Thinking & Judgment
Canonical Lesson: L23-01 — How do I measure honestly?

Demonstrates the scientific, question-driven measurement methodology:
1. Formulates a clear measurement question and falsifiable hypothesis.
2. Compares uncoordinated synchronous loops (completion-coupled) against
   an arrival-scheduled single-server accounting model under an open-arrival assumption.
3. Injects explicitly labeled *synthetic* pauses to illustrate coordinated omission
   (without claiming uninstrumented garbage collection observation).
4. Employs monotonic performance timers (time.monotonic_ns()) while explicitly
   recording that integer nanosecond units do not guarantee nanosecond hardware clock resolution.
5. Computes multi-dimensional summary statistics (moments, percentiles, histograms)
   matching the inference goal, without dogmatic universal rules of thumb.

Zero external dependencies (Python standard library only).
Zero network access. Bounded synthetic execution.
"""

from __future__ import annotations

import math
import time
from typing import Any, Dict, List, Optional, Tuple


def get_clock_characteristics() -> Dict[str, Any]:
    """Inspects the system monotonic timer characteristics via Python stdlib."""
    info = time.get_clock_info("monotonic")
    return {
        "monotonic": {
            "implementation": info.implementation,
            "monotonic": info.monotonic,
            "adjustable": info.adjustable,
            "resolution_seconds": info.resolution,
        },
        "inference_boundary": (
            "Integer nanosecond return values from time.monotonic_ns() reflect API units, "
            "not physical hardware timer resolution."
        ),
    }


def calculate_percentile(sorted_samples: List[float], p: float) -> float:
    """Calculates percentile p (0 <= p <= 100) using linear interpolation."""
    if not sorted_samples:
        raise ValueError("Cannot calculate percentile of empty sample list")
    if p < 0 or p > 100:
        raise ValueError(f"Percentile must be between 0 and 100, got {p}")
    if len(sorted_samples) == 1:
        return sorted_samples[0]

    rank = (p / 100.0) * (len(sorted_samples) - 1)
    k = int(rank)
    d = rank - k
    if k + 1 < len(sorted_samples):
        return sorted_samples[k] + d * (sorted_samples[k + 1] - sorted_samples[k])
    return sorted_samples[k]


def calculate_summary_statistics(samples_ms: List[float]) -> Dict[str, float]:
    """
    Computes moments and percentiles for a list of latency samples (in milliseconds).

    Fails closed on empty lists or negative values.
    """
    if not samples_ms:
        raise ValueError("Sample list is empty; cannot compute summary statistics.")
    for val in samples_ms:
        if val < 0:
            raise ValueError(f"Latency samples cannot be negative, got {val}")

    n = len(samples_ms)
    sorted_s = sorted(samples_ms)
    total = sum(sorted_s)
    mean_val = total / n

    if n > 1:
        variance = sum((x - mean_val) ** 2 for x in sorted_s) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        variance = 0.0
        stddev = 0.0

    return {
        "count": float(n),
        "min": sorted_s[0],
        "max": sorted_s[-1],
        "mean": mean_val,
        "stddev": stddev,
        "variance": variance,
        "p50": calculate_percentile(sorted_s, 50.0),
        "p90": calculate_percentile(sorted_s, 90.0),
        "p95": calculate_percentile(sorted_s, 95.0),
        "p99": calculate_percentile(sorted_s, 99.0),
    }


def simulate_measurement_deterministic(
    arrival_interval_ms: float,
    service_time_ms: float,
    stall_index: int,
    stall_duration_ms: float,
    request_count: int,
) -> Tuple[List[float], List[float]]:
    """
    Pure mathematical simulation of request latency comparing:
    1. Naive completion-coupled generator (synchronous loop):
       - Issues request i only after request i-1 completes.
       - Under a stall, subsequent requests are delayed at the client; the client
         records only the service time, omitting the queuing delay incurred by
         the target schedule.
    2. Arrival-scheduled generator (open arrival model):
       - Requests are scheduled to arrive at T_sched[i] = i * arrival_interval_ms.
       - A single-server queue processes requests sequentially.
       - Total latency recorded = T_complete[i] - T_sched[i].
       - Under a stall, requests arriving during the stall accumulate in queue,
         faithfully reflecting coordinated omission.

    Returns:
        (naive_latencies_ms, arrival_scheduled_latencies_ms)
    """
    numeric_values = {
        "arrival_interval_ms": arrival_interval_ms,
        "service_time_ms": service_time_ms,
        "stall_duration_ms": stall_duration_ms,
    }
    if not all(math.isfinite(v) for v in numeric_values.values()):
        raise ValueError("Measurement inputs must be finite numbers")
    if arrival_interval_ms <= 0:
        raise ValueError("Arrival interval must be positive")
    if service_time_ms < 0:
        raise ValueError("Service time cannot be negative")
    if stall_duration_ms < 0:
        raise ValueError("Synthetic stall duration cannot be negative")
    if request_count <= 0:
        raise ValueError("Request count must be positive")
    if stall_index < 0 or stall_index >= request_count:
        raise ValueError("stall_index must identify a request within the modeled request_count")

    # 1. Naive synchronous loop:
    # Client sends request, awaits completion, sleeps until next tick.
    # When stall_index happens, service time expands by stall_duration_ms.
    naive_latencies: List[float] = []
    for i in range(request_count):
        actual_service = service_time_ms + (stall_duration_ms if i == stall_index else 0.0)
        # Naive generator measures only completion - dispatch
        naive_latencies.append(actual_service)

    # 2. Arrival-scheduled generator (Open arrival queue model):
    scheduled_latencies: List[float] = []
    server_free_time: float = 0.0

    for i in range(request_count):
        t_sched = i * arrival_interval_ms
        actual_service = service_time_ms + (stall_duration_ms if i == stall_index else 0.0)

        # Server can only start request when it arrives AND server is free
        t_start = max(t_sched, server_free_time)
        t_complete = t_start + actual_service
        server_free_time = t_complete

        # True latency from intended arrival to completion
        latency = t_complete - t_sched
        scheduled_latencies.append(latency)

    return naive_latencies, scheduled_latencies


def run_live_synthetic_benchmark(
    request_count: int = 30,
    target_rate_req_per_sec: float = 100.0,
    base_service_time_ms: float = 2.0,
    synthetic_stall_index: int = 10,
    synthetic_stall_ms: float = 60.0,
) -> Dict[str, Any]:
    """
    Runs a bounded, course-owned synthetic service-time observation plus arrival-scheduled accounting reconstruction.

    Notice:
    - Synthetic stall is explicitly labeled as synthetic pause injection.
    - Zero external network calls.
    - Nominal requested sleep budget is safety-capped at 1.5 seconds; host scheduling can extend wall-clock runtime.
    """
    numeric_values = {
        "target_rate_req_per_sec": target_rate_req_per_sec,
        "base_service_time_ms": base_service_time_ms,
        "synthetic_stall_ms": synthetic_stall_ms,
    }
    if not all(math.isfinite(v) for v in numeric_values.values()):
        raise ValueError("Live synthetic benchmark inputs must be finite numbers")
    if target_rate_req_per_sec <= 0:
        raise ValueError("Target request rate must be positive")
    if request_count <= 0 or request_count > 200:
        raise ValueError("Request count must be between 1 and 200 for bounded execution")
    if base_service_time_ms < 0 or synthetic_stall_ms < 0:
        raise ValueError("Synthetic service/stall durations cannot be negative")
    if synthetic_stall_index < 0 or synthetic_stall_index >= request_count:
        raise ValueError("synthetic_stall_index must identify a request within request_count")

    nominal_sleep_budget_ms = request_count * base_service_time_ms + synthetic_stall_ms
    if nominal_sleep_budget_ms > 1500.0:
        raise ValueError(
            "Nominal synthetic sleep budget exceeds the course safety cap of 1500 ms; "
            "reduce request_count/service/stall parameters."
        )

    base_service_ns = int(base_service_time_ms * 1_000_000)
    stall_ns = int(synthetic_stall_ms * 1_000_000)

    # Simulated worker that processes work
    def execute_service(req_idx: int) -> int:
        start = time.monotonic_ns()
        work_duration = base_service_ns + (stall_ns if req_idx == synthetic_stall_index else 0)
        # Bounded active wait / sleep to simulate processing
        sleep_sec = work_duration / 1_000_000_000.0
        time.sleep(sleep_sec)
        end = time.monotonic_ns()
        return end - start

    # Run Naive Synchronous Generator
    naive_samples_ms: List[float] = []
    for i in range(request_count):
        t_req_start = time.monotonic_ns()
        _ = execute_service(i)
        t_req_end = time.monotonic_ns()
        naive_samples_ms.append((t_req_end - t_req_start) / 1_000_000.0)

    # Reconstruct an arrival-scheduled single-server queue from the observed service samples.
    # This is a model/accounting reconstruction, not a concurrently issuing live open-load generator.
    scheduled_samples_ms: List[float] = []
    simulated_server_free_ms: float = 0.0
    interval_ms = 1000.0 / target_rate_req_per_sec

    for i in range(request_count):
        t_sched_ms = i * interval_ms
        actual_srv_ms = naive_samples_ms[i]

        t_start_ms = max(t_sched_ms, simulated_server_free_ms)
        t_complete_ms = t_start_ms + actual_srv_ms
        simulated_server_free_ms = t_complete_ms

        latency_ms = t_complete_ms - t_sched_ms
        scheduled_samples_ms.append(latency_ms)

    return {
        "clock_metadata": get_clock_characteristics(),
        "parameters": {
            "request_count": request_count,
            "target_rate_rps": target_rate_req_per_sec,
            "base_service_time_ms": base_service_time_ms,
            "synthetic_stall_index": synthetic_stall_index,
            "synthetic_stall_ms": synthetic_stall_ms,
        },
        "naive_summary": calculate_summary_statistics(naive_samples_ms),
        "scheduled_summary": calculate_summary_statistics(scheduled_samples_ms),
        "naive_samples": naive_samples_ms,
        "scheduled_samples": scheduled_samples_ms,
        "model_boundary": "scheduled samples are reconstructed from observed service times; no live concurrent open-load generator is claimed",
    }


def format_summary_table(naive: Dict[str, float], scheduled: Dict[str, float]) -> str:
    """Formats a comparative markdown table between naive and scheduled measurement."""
    lines = [
        "| Metric | Naive Synchronous Loop (Service Time Only) | Arrival-Scheduled Accounting Model (Queue + Service) | Omission Ratio (Sched / Naive) |",
        "| :--- | :--- | :--- | :--- |",
    ]
    metrics = ["min", "p50", "p90", "p95", "p99", "max", "mean", "stddev"]
    for m in metrics:
        nv = naive[m]
        sv = scheduled[m]
        ratio_str = f"{sv / nv:.2f}x" if nv > 0 else "N/A"
        lines.append(f"| **{m.upper()}** | {nv:.3f} ms | {sv:.3f} ms | {ratio_str} |")
    return "\n".join(lines)


def main() -> None:
    print("=" * 80)
    print("  M23 L23-01: QUESTION-DRIVEN MEASUREMENT & COORDINATED OMISSION HARNESS")
    print("=" * 80)

    clock_info = get_clock_characteristics()
    mono = clock_info["monotonic"]
    print(f"[CLOCK PROBE] Implementation: {mono['implementation']}")
    print(f"[CLOCK PROBE] Monotonic:      {mono['monotonic']}")
    print(f"[CLOCK PROBE] Adjustable:     {mono['adjustable']}")
    print(f"[CLOCK PROBE] Resolution:     {mono['resolution_seconds']:.2e} s")
    print(f"[NOTE]        {clock_info['inference_boundary']}")
    print("-" * 80)

    print("[MEASUREMENT QUESTION]")
    print("  'When a server experiences a 60ms synthetic pause under a 100 req/s arrival schedule,")
    print("   how does completion-coupled sampling distort perceived tail latency compared to")
    print("   arrival-scheduled queue accounting?'")
    print("-" * 80)

    print("[RUNNING BOUNDED SYNTHETIC SERVICE OBSERVATION + QUEUE MODEL] (25 requests, synthetic stall at req #8)...")
    res = run_live_synthetic_benchmark(
        request_count=25,
        target_rate_req_per_sec=100.0,
        base_service_time_ms=2.0,
        synthetic_stall_index=8,
        synthetic_stall_ms=50.0,
    )

    print("\n" + format_summary_table(res["naive_summary"], res["scheduled_summary"]) + "\n")
    print("=" * 80)
    print("[EMPIRICAL OBSERVATION]")
    print("  1. In the naive synchronous loop, the client stopped generating requests during the stall.")
    print("     Requests arriving right after the stall experienced no measured queue wait in the naive run.")
    print("  2. In the arrival-scheduled accounting model, requests scheduled to arrive during the 50ms stall")
    print("     accumulated queue delay, dramatically revealing elevated p90 and p99 tail latencies.")
    print("  3. Coordinated omission is not a universal truth of all benchmarks; it is specifically")
    print("     a property of workloads where requests arrive independently of service completion.")
    print("=" * 80)


if __name__ == "__main__":
    main()
