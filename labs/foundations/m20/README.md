# M20 Foundations Activities: Observability & Reliability Engineering

This directory contains executable, course-owned fixtures and worked activities for Module M20.

## Core Boundary Rules

- **Zero-SaaS Core**: Strictly no Prometheus, Grafana, Datadog, Jaeger, OpenTelemetry backend, Docker, Kubernetes, or cloud accounts required by Core.
- **Python stdlib First**: Built on standard library modules (`http.server`, `urllib.request`, `json`, `time`, `threading`, `secrets`, `uuid`).
- **Clock Semantics Invariant**: Correctness-sensitive elapsed durations derive exclusively from monotonic clock sources (`time.monotonic()` or `time.perf_counter()`). Wall-clock time (`time.time()`) is reserved for calendar/event timestamps and never subtracted for elapsed duration.
- **Fake Wall-Clock Adapter**: Injects simulated backward wall-clock adjustments for pedagogical demonstration without mutating the real host clock or claiming real NTP reproduction.
- **Deterministic Distributions**: Samples, windows, sample counts, and the exact percentile convention (`nearest_rank`) are explicitly stated. Request percentiles are never equated to fixed unique-user percentages.
- **W3C Trace Context Level 1 version-00**: Standard `traceparent` generation and strict validation per W3C Recommendation 2021. Trace IDs are diagnostic correlation mechanisms, never authentication, authorization, secrecy, or user identity.
- **Log Privacy & Redaction**: Passwords, authorization headers, cookies, and secret tokens are strictly excluded from structured logs.
- **Ephemeral Localhost Only**: Services bind strictly to `127.0.0.1` on OS-selected ephemeral ports (`port=0`).
- **Blameless Postmortem Framing**: Systemic conditions and defensive safeguards are analyzed; "human error" is rejected as an incident conclusion.
- **Strictly Optional OpenTelemetry**: OpenTelemetry package comparison (`LAB-OPT-04` & `EXP-04`) is strictly optional. Package absence never impedes Core completion.

---

## Files Overview

1. **`s6_m20_observability_pipeline.py`**
   - Central Core fixture implementing:
     - `ClockAdapter`: Monotonic duration vs. simulated adjustable wall clock.
     - `compute_distribution_statistics`: Deterministic mean and percentiles ($p50, p90, p95, p99$) under `nearest_rank` convention.
     - `evaluate_sli_slo`: Explicit scenario-based SLI, SLO target, and Error Budget consumption calculation.
     - `generate_traceparent` & `parse_traceparent`: W3C Level 1 version-00 compliance, format validation, and all-zero identifier rejection.
     - `StructuredLogger`: Valid JSON event logging with monotonic durations and secret redaction.
     - `ServiceA`, `ServiceB`, `ServiceC`: In-process three-service pipeline on localhost ephemeral ports.
     - `ObservabilityPipelineManager`: Explicit lifecycle management (start, dispatch, fault injection, mitigation, shutdown).
     - `reconstruct_correlated_timeline`: Hop-by-hop latency and status breakdown filtered by `trace_id`.
     - `generate_blameless_postmortem`: Markdown postmortem generator focusing on systemic conditions and safeguards.

2. **`activity_l20_01.py`**
   - Runs Lesson L20-01 hands-on activity:
     - Clock semantics: verifies negative wall subtraction vs. positive monotonic elapsed duration under simulated step.
     - Distribution statistics: demonstrates tail divergence ($p99$ vs. mean) on a deterministic sample set.
     - SLI/SLO/Error Budget worksheet evaluation.
     - Generates `.scratch/l20_01_observation.json`.

3. **`activity_l20_02.py`**
   - Runs Lesson L20-02 hands-on activity:
     - Starts ephemeral three-service pipeline ($A \to B \to C$).
     - Demonstrates W3C `traceparent` propagation across all hops.
     - Injects ServiceC delay fault (350ms).
     - Compares uncorrelated log inspection with correlated `trace_id` filtering.
     - Reconstructs request-hop timeline and localizes downstream bottleneck to ServiceC.
     - Applies safe mitigation (ServiceB fallback cache) and verifies recovery ($< 20$ms).
     - Generates blameless postmortem draft `.scratch/l20_02_postmortem_draft.md`.
     - Generates observation record `.scratch/l20_02_observation.json`.
     - Cleanly shuts down ephemeral servers and joins threads.

4. **`optional_exp04_otel.py`**
   - Strictly Optional Source Expedition (`EXP-04`) and optional lab (`LAB-OPT-04`):
     - Pinned release: `open-telemetry/opentelemetry-python` tag `v1.44.0` (2026-07-16).
     - API path: `opentelemetry-api/src/opentelemetry/trace/span.py`
     - SDK path: `opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py`
     - Reading card documents that SDK default span timestamps use `time_ns()` (system epoch time), which is NOT `time.monotonic_ns()`.
     - If packages are installed, demonstrates console span exporter; if absent, reports `OPTIONAL BLOCKED / NOT RUN` gracefully.

5. **`reset.py`**
   - Fail-closed, idempotent cleanup script removing `.scratch/` and local `__pycache__/`.
   - Safe to run repeatedly; verified idempotent across double execution.

6. **`test_m20.py`**
   - Comprehensive unit and integration test suite covering all 19 verification dimensions.

---

## Running the Activities

```bash
# 1. Run M20 Core preflight capability check
python tests/preflight_distributed_infra.py --module m20

# 2. Run Lesson L20-01 hands-on activity (Clock semantics, distributions, SLI/SLO)
python labs/foundations/m20/activity_l20_01.py

# 3. Run Lesson L20-02 hands-on activity (Trace Context, incident, mitigation, postmortem)
python labs/foundations/m20/activity_l20_02.py

# 4. Run optional OpenTelemetry source reading & comparison (Strictly Optional)
python labs/foundations/m20/optional_exp04_otel.py

# 5. Run full M20 automated test suite
python labs/foundations/m20/test_m20.py

# 6. Clean up temporary scratch files (idempotent, safe to run repeatedly)
python labs/foundations/m20/reset.py
```
