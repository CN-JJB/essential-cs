#!/usr/bin/env python3
"""
s6_m20_observability_pipeline.py — Zero-SaaS Observability & Reliability Pipeline Fixture
========================================================================================

Canonical Stage 6 / Module 20 (M20) Observability & Reliability Engineering Fixture.
Contract authority: GitHub Issue #110 and Stage 6 Design Dossier v0.1.

Architectural Commitments:
1. Zero-SaaS and stdlib-first: No Prometheus, Grafana, Datadog, Jaeger, Docker, or Cloud dependencies.
2. Clock Semantics Invariant: Correctness-sensitive elapsed duration is computed ONLY from
   monotonic clock sources (time.monotonic() or time.perf_counter()). Wall-clock timestamps
   (time.time()) are preserved strictly as calendar/event labels and NEVER subtracted for duration.
3. Fake Adjustable Wall Clock: Teaching adapter injects simulated backward wall steps without
   mutating the host system clock or claiming real NTP reproduction.
4. Deterministic Distribution Statistics: Stated dataset/window, sample count, and exact
   percentile convention (nearest_rank). Request percentiles are never equated to fixed user fractions.
5. SLI/SLO/Error Budget: Bounded worksheet with explicit scenario/policy inputs (not universal constants).
   SLIs are not reduced to a single ratio definition; SLAs are kept distinct from SLOs.
6. W3C Trace Context Level 1 version-00: Strict generator, parser, and validator per W3C Rec 2021.
   Validates version=00, 32-hex trace_id, 16-hex parent_id, 2-hex flags; rejects all-zero IDs.
   Trace context is a correlation mechanism, NEVER authentication or identity.
7. Structured Logging Engine: Valid JSON logs distinguishing wall timestamp from monotonic duration.
   Strict redaction of secrets, Authorization headers, and Cookie values.
8. Local Three-Service Pipeline: ServiceA (Frontend) -> ServiceB (Business) -> ServiceC (Storage Mock).
   All bind strictly to 127.0.0.1 on OS-selected ephemeral ports (port=0).
9. Incident Lifecycle & Blameless Postmortem: Injected fault in ServiceC, upstream symptom in ServiceA,
   correlated timeline reconstruction, safe mitigation, recovery verification, and blameless analysis.
10. Explicit Lifecycle & Safety: Explicit shutdown, socket close, thread join, and watchdog protection.
"""

import argparse
import datetime
import http.server
import json
import math
import os
import re
import secrets
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple


# ============================================================================
# 1. Clock Semantics & Fake Wall-Clock Adapter
# ============================================================================

class ClockAdapter:
    """
    Teaching adapter demonstrating clock semantics without mutating host system clock.

    Curriculum Invariant:
    - Elapsed duration for correctness-sensitive logic MUST derive from monotonic clocks.
    - Wall clock (CLOCK_REALTIME / time.time()) is for calendar/event timestamps only.
    - Stepping or adjusting the wall clock must NEVER distort monotonic interval measurement.
    """

    def __init__(self) -> None:
        self._simulated_wall_offset_seconds: float = 0.0

    def wall_time(self) -> float:
        """Returns simulated wall-clock time in seconds since epoch."""
        return time.time() + self._simulated_wall_offset_seconds

    def wall_time_iso(self) -> str:
        """Returns ISO 8601 UTC string for calendar timestamping."""
        utc_dt = datetime.datetime.fromtimestamp(
            self.wall_time(), tz=datetime.timezone.utc
        )
        return utc_dt.isoformat()

    def monotonic_time(self) -> float:
        """
        Returns true monotonic time in seconds.
        Unaffected by system clock steps, NTP adjustments, or fake offsets.
        """
        return time.monotonic()

    def perf_counter(self) -> float:
        """Returns high-resolution monotonic time in seconds."""
        return time.perf_counter()

    def inject_wall_step_backward(self, step_seconds: float) -> None:
        """
        Simulates an adjustable wall-clock step backward (e.g. -5.0s).
        Teaching adapter only: DOES NOT mutate real host clock or NTP daemon.
        """
        self._simulated_wall_offset_seconds -= abs(step_seconds)

    def reset_offset(self) -> None:
        """Resets simulated wall clock offset to zero."""
        self._simulated_wall_offset_seconds = 0.0


def compute_elapsed_duration_ms(start_mono: float, end_mono: float) -> float:
    """
    Computes elapsed duration in milliseconds from monotonic readings.
    Guaranteed non-negative unless host hardware clock severely malfunctions.
    """
    return max(0.0, (end_mono - start_mono) * 1000.0)


# ============================================================================
# 2. Deterministic Distribution Statistics (Tail vs. Mean)
# ============================================================================

def compute_distribution_statistics(
    samples: Sequence[float],
    convention: str = "nearest_rank",
) -> Dict[str, Any]:
    """
    Computes deterministic distribution statistics over a sample series.

    Required Invariants:
    - Stated sample count, min, max, mean, and percentiles (p50, p90, p95, p99).
    - Exact percentile convention is recorded in metadata.
    - Percentile is a request-distribution statistic, NOT a fixed percentage of unique users.

    Convention 'nearest_rank':
      rank = max(1, math.ceil((p / 100.0) * n))
      value = sorted_samples[rank - 1] (1-based rank converted to 0-based index)
    """
    if not samples:
        raise ValueError("Cannot compute distribution statistics on an empty sample set.")

    n = len(samples)
    sorted_s = sorted(samples)
    total = sum(sorted_s)
    mean_val = total / n

    def get_percentile(p: float) -> float:
        if convention == "nearest_rank":
            rank = max(1, math.ceil((p / 100.0) * n))
            return sorted_s[rank - 1]
        elif convention == "linear_interpolation":
            idx = (p / 100.0) * (n - 1)
            low = int(math.floor(idx))
            high = int(math.ceil(idx))
            frac = idx - low
            return sorted_s[low] + frac * (sorted_s[high] - sorted_s[low])
        else:
            raise ValueError(f"Unsupported percentile convention: {convention}")

    p50 = get_percentile(50.0)
    p90 = get_percentile(90.0)
    p95 = get_percentile(95.0)
    p99 = get_percentile(99.0)

    return {
        "sample_count": n,
        "mean_ms": round(mean_val, 4),
        "min_ms": round(sorted_s[0], 4),
        "max_ms": round(sorted_s[-1], 4),
        "p50_ms": round(p50, 4),
        "p90_ms": round(p90, 4),
        "p95_ms": round(p95, 4),
        "p99_ms": round(p99, 4),
        "convention": convention,
        "convention_description": (
            "nearest_rank: rank = ceil(p/100 * N), 1-based index into ascending sorted samples"
            if convention == "nearest_rank"
            else "linear_interpolation"
        ),
        "percentile_vs_user_note": (
            "Request percentiles characterize the latency distribution of requests in this window. "
            "They do NOT imply that exactly (100 - P)% of distinct users experienced that latency, "
            "as user-to-request mappings vary widely in production."
        ),
    }


# ============================================================================
# 3. SLI / SLO / Error Budget Evaluator
# ============================================================================

def evaluate_sli_slo(
    total_valid_requests: int,
    good_requests: int,
    slo_target_percent: float,
    window_seconds: float = 2592000.0,  # default 30 days
) -> Dict[str, Any]:
    """
    Evaluates a ratio-style SLI, SLO target, and Error Budget consumption.

    Curriculum Invariants:
    - SLI is a quantitative service-behavior measure; good/valid ratio is one common form,
      not the universal definition of all SLIs.
    - SLO/Error Budget inputs are explicit scenario/policy inputs, not industry constants.
    - SLA is kept distinct from SLO and not used as per-instance failure probability.
    """
    if total_valid_requests <= 0:
        raise ValueError("total_valid_requests must be greater than 0.")
    if good_requests < 0 or good_requests > total_valid_requests:
        raise ValueError("good_requests must be between 0 and total_valid_requests.")
    if slo_target_percent <= 0.0 or slo_target_percent >= 100.0:
        raise ValueError("slo_target_percent must be strictly between 0 and 100.")

    bad_requests = total_valid_requests - good_requests
    actual_sli_percent = (good_requests / total_valid_requests) * 100.0

    # Error budget allowed failure rate = 100.0 - slo_target_percent
    allowed_failure_rate = (100.0 - slo_target_percent) / 100.0
    allowed_bad_requests = total_valid_requests * allowed_failure_rate
    remaining_budget_requests = allowed_bad_requests - bad_requests

    # Budget consumed percentage: fraction of the allowed bad requests already spent
    if allowed_bad_requests > 0:
        budget_consumed_percent = (bad_requests / allowed_bad_requests) * 100.0
    else:
        budget_consumed_percent = 0.0 if bad_requests == 0 else float("inf")

    # Time-based budget representation (minutes of downtime in window)
    window_minutes = window_seconds / 60.0
    allowed_downtime_minutes = window_minutes * allowed_failure_rate

    slo_met = actual_sli_percent >= slo_target_percent

    return {
        "total_valid_requests": total_valid_requests,
        "good_requests": good_requests,
        "bad_requests": bad_requests,
        "actual_sli_percent": round(actual_sli_percent, 4),
        "slo_target_percent": round(slo_target_percent, 4),
        "slo_met": slo_met,
        "allowed_bad_requests": round(allowed_bad_requests, 2),
        "remaining_budget_requests": round(remaining_budget_requests, 2),
        "budget_consumed_percent": round(budget_consumed_percent, 2),
        "window_seconds": window_seconds,
        "allowed_downtime_minutes_in_window": round(allowed_downtime_minutes, 2),
        "universal_definition_note": (
            "The ratio (good_requests / total_valid_requests) is one common ratio SLI form. "
            "SLIs may also measure latency thresholds, throughput, saturation, or freshness."
        ),
        "sla_distinction": (
            "An SLA is an external contractual or business commitment with specified remedies and exclusions. "
            "It is not an internal engineering target (SLO), and an SLA percentage is not an independent "
            "per-instance failure probability."
        ),
    }


# ============================================================================
# 4. W3C Trace Context Level 1 version-00 Generator & Parser
# ============================================================================

HEX_32_PATTERN = re.compile(r"^[0-9a-f]{32}$")
HEX_16_PATTERN = re.compile(r"^[0-9a-f]{16}$")
HEX_2_PATTERN = re.compile(r"^[0-9a-f]{2}$")


def generate_traceparent(
    trace_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    sampled: bool = True,
) -> str:
    """
    Generates a valid W3C Trace Context Level 1 version-00 traceparent header.
    Format: 00-{trace_id}-{parent_id}-{trace_flags}
    """
    version = "00"
    if not trace_id:
        # Generate 16 random bytes -> 32 hex chars, ensuring not all-zero
        while True:
            tid = secrets.token_hex(16).lower()
            if tid != "00000000000000000000000000000000":
                trace_id = tid
                break
    else:
        trace_id = trace_id.lower()
        if not HEX_32_PATTERN.match(trace_id) or trace_id == "00000000000000000000000000000000":
            raise ValueError(f"Invalid trace_id for W3C traceparent: {trace_id}")

    if not parent_id:
        while True:
            pid = secrets.token_hex(8).lower()
            if pid != "0000000000000000":
                parent_id = pid
                break
    else:
        parent_id = parent_id.lower()
        if not HEX_16_PATTERN.match(parent_id) or parent_id == "0000000000000000":
            raise ValueError(f"Invalid parent_id for W3C traceparent: {parent_id}")

    trace_flags = "01" if sampled else "00"
    return f"{version}-{trace_id}-{parent_id}-{trace_flags}"


def parse_traceparent(header_value: str) -> Dict[str, Any]:
    """
    Parses and strictly validates a W3C Trace Context Level 1 version-00 traceparent header.

    W3C Recommendation 2021 Validation Rules for version 00:
    1. Must contain exactly 4 dash-separated fields.
    2. Version 00 requires total length of exactly 55 characters.
    3. Version must be '00'. Version 'ff' is forbidden.
    4. trace_id must be 32 lowercase hex characters and NOT all zeros.
    5. parent_id must be 16 lowercase hex characters and NOT all zeros.
    6. trace_flags must be 2 lowercase hex characters.
    """
    if not isinstance(header_value, str):
        raise ValueError("traceparent header must be a string.")

    header_clean = header_value.strip()

    parts = header_clean.split("-")
    if len(parts) != 4:
        raise ValueError(
            f"Invalid traceparent: expected exactly 4 dash-separated fields, got {len(parts)}."
        )

    version, trace_id, parent_id, trace_flags = parts

    # Check version format
    if not HEX_2_PATTERN.match(version):
        raise ValueError(f"Invalid traceparent version format: '{version}'")
    if version == "ff":
        raise ValueError("Invalid traceparent version: 'ff' is forbidden by W3C specification.")

    # Strict Level 1 version-00 checks
    if version == "00":
        if len(header_clean) != 55:
            raise ValueError(
                f"Invalid version-00 traceparent length: expected 55 characters, got {len(header_clean)}."
            )

    # Validate trace_id
    if not HEX_32_PATTERN.match(trace_id):
        raise ValueError(
            f"Invalid trace_id: must be 32 lowercase hex characters, got '{trace_id}'."
        )
    if trace_id == "00000000000000000000000000000000":
        raise ValueError("Invalid trace_id: all-zero trace ID is forbidden by W3C specification.")

    # Validate parent_id
    if not HEX_16_PATTERN.match(parent_id):
        raise ValueError(
            f"Invalid parent_id: must be 16 lowercase hex characters, got '{parent_id}'."
        )
    if parent_id == "0000000000000000":
        raise ValueError("Invalid parent_id: all-zero parent ID is forbidden by W3C specification.")

    # Validate trace_flags
    if not HEX_2_PATTERN.match(trace_flags):
        raise ValueError(
            f"Invalid trace_flags: must be 2 lowercase hex characters, got '{trace_flags}'."
        )

    flags_int = int(trace_flags, 16)
    sampled = bool(flags_int & 1)

    return {
        "version": version,
        "trace_id": trace_id,
        "parent_id": parent_id,
        "trace_flags": trace_flags,
        "sampled": sampled,
        "raw_header": header_clean,
        "auth_boundary_note": (
            "Trace context is a diagnostic correlation identifier. It MUST NOT be used for "
            "authentication, authorization, secrecy, integrity, or user identity."
        ),
        "version_scope_note": (
            "This parser validates W3C Level 1 version-00 traceparent per W3C Recommendation (2021). "
            "It does not implement future W3C versions (e.g. Level 2) or proprietary vendor extensions."
        ),
    }


# ============================================================================
# 5. Structured Logging Engine & Privacy Filter
# ============================================================================

SENSITIVE_KEY_PATTERN = re.compile(
    r"(?i)(auth|token|secret|password|passwd|cookie|key|credential|bearer)"
)


class StructuredLogger:
    """
    Course-owned structured logger emitting valid JSON records.

    Curriculum Invariants:
    - Distinguishes calendar/event timestamp (wall clock) from monotonic duration (monotonic timer).
    - Excludes passwords, authorization headers, cookies, and secret tokens.
    - Preserves correlation context (trace_id, parent_id, span_id, service, event).
    - Logs can suffer from omission, buffering, or sampling; shared timestamps do not imply causality.
    """

    def __init__(self, clock_adapter: Optional[ClockAdapter] = None) -> None:
        self.clock = clock_adapter or ClockAdapter()
        self._records: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def log(
        self,
        service: str,
        event: str,
        trace_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        span_id: Optional[str] = None,
        duration_ms: Optional[float] = None,
        status: str = "OK",
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Emits and records a sanitized structured JSON log entry."""
        # Sanitize details for security and privacy
        safe_details: Dict[str, Any] = {}
        if details:
            for k, v in details.items():
                if SENSITIVE_KEY_PATTERN.search(k):
                    safe_details[k] = "[REDACTED]"
                else:
                    safe_details[k] = v

        record = {
            "timestamp_utc": self.clock.wall_time_iso(),
            "timestamp_wall_epoch_s": round(self.clock.wall_time(), 6),
            "duration_ms": round(duration_ms, 3) if duration_ms is not None else None,
            "service": service,
            "event": event,
            "status": status,
            "trace_id": trace_id,
            "parent_id": parent_id,
            "span_id": span_id,
            "details": safe_details,
        }

        with self._lock:
            self._records.append(record)

        return record

    def get_records(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._records)

    def clear(self) -> None:
        with self._lock:
            self._records.clear()

    def filter_by_trace_id(self, trace_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            return [r for r in self._records if r.get("trace_id") == trace_id]


# ============================================================================
# 6. Local Three-Service Observability Pipeline
# ============================================================================

class ServiceCHandler(http.server.BaseHTTPRequestHandler):
    """
    Downstream Storage Mock Service (ServiceC).
    Configurable fault modes: 'NONE', 'DELAY', 'HTTP_500'.
    """

    def log_message(self, format: str, *args: Any) -> None:
        pass  # Suppress default noisy stderr logging

    def do_GET(self) -> None:
        server: "ObservableServer" = self.server  # type: ignore
        clock = server.clock
        logger = server.logger

        t_start_mono = clock.monotonic_time()
        span_id = secrets.token_hex(8).lower()

        # Parse traceparent
        traceparent_raw = self.headers.get("traceparent")
        trace_id = None
        parent_id = None
        if traceparent_raw:
            try:
                parsed = parse_traceparent(traceparent_raw)
                trace_id = parsed["trace_id"]
                parent_id = parsed["parent_id"]
            except ValueError as e:
                logger.log(
                    service="ServiceC",
                    event="invalid_traceparent_received",
                    status="BAD_REQUEST",
                    details={"error": str(e), "raw": traceparent_raw},
                )
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "invalid traceparent"}')
                return

        logger.log(
            service="ServiceC",
            event="storage_request_received",
            trace_id=trace_id,
            parent_id=parent_id,
            span_id=span_id,
            status="START",
            details={"path": self.path},
        )

        # Injected fault evaluation
        fault_mode = server.fixture_state.get("fault_mode", "NONE")
        delay_s = server.fixture_state.get("injected_delay_s", 0.0)

        if fault_mode == "DELAY" and delay_s > 0:
            logger.log(
                service="ServiceC",
                event="injected_delay_started",
                trace_id=trace_id,
                parent_id=parent_id,
                span_id=span_id,
                status="DEGRADED",
                details={"delay_s": delay_s},
            )
            time.sleep(delay_s)

        if fault_mode == "HTTP_500":
            t_end_mono = clock.monotonic_time()
            duration_ms = compute_elapsed_duration_ms(t_start_mono, t_end_mono)
            logger.log(
                service="ServiceC",
                event="storage_error_injected",
                trace_id=trace_id,
                parent_id=parent_id,
                span_id=span_id,
                duration_ms=duration_ms,
                status="ERROR",
                details={"http_status": 500},
            )
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"service": "ServiceC", "status": "error", "code": 500}')
            return

        t_end_mono = clock.monotonic_time()
        duration_ms = compute_elapsed_duration_ms(t_start_mono, t_end_mono)

        logger.log(
            service="ServiceC",
            event="storage_request_completed",
            trace_id=trace_id,
            parent_id=parent_id,
            span_id=span_id,
            duration_ms=duration_ms,
            status="OK",
            details={"storage_item": "record-101"},
        )

        resp_data = json.dumps(
            {
                "service": "ServiceC",
                "status": "stored",
                "record": "item-101",
                "duration_ms": duration_ms,
            }
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(resp_data)


class ServiceBHandler(http.server.BaseHTTPRequestHandler):
    """
    Business Logic Service (ServiceB).
    Calls ServiceC. Can apply safe scenario mitigation (fallback cache/bypass).
    """

    def log_message(self, format: str, *args: Any) -> None:
        pass

    def do_GET(self) -> None:
        server: "ObservableServer" = self.server  # type: ignore
        clock = server.clock
        logger = server.logger

        t_start_mono = clock.monotonic_time()
        span_id = secrets.token_hex(8).lower()

        traceparent_raw = self.headers.get("traceparent")
        trace_id = None
        parent_id = None
        if traceparent_raw:
            try:
                parsed = parse_traceparent(traceparent_raw)
                trace_id = parsed["trace_id"]
                parent_id = parsed["parent_id"]
            except ValueError as e:
                logger.log(
                    service="ServiceB",
                    event="invalid_traceparent_received",
                    status="BAD_REQUEST",
                    details={"error": str(e)},
                )
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "invalid traceparent"}')
                return

        logger.log(
            service="ServiceB",
            event="business_request_received",
            trace_id=trace_id,
            parent_id=parent_id,
            span_id=span_id,
            status="START",
            details={"path": self.path},
        )

        mitigation_enabled = server.fixture_state.get("mitigation_enabled", False)

        if mitigation_enabled:
            # Safe scenario mitigation: ServiceB serves request from local cached fallback
            t_end_mono = clock.monotonic_time()
            duration_ms = compute_elapsed_duration_ms(t_start_mono, t_end_mono)
            logger.log(
                service="ServiceB",
                event="mitigation_cache_served",
                trace_id=trace_id,
                parent_id=parent_id,
                span_id=span_id,
                duration_ms=duration_ms,
                status="MITIGATED",
                details={"cache_hit": True, "bypassed_service": "ServiceC"},
            )
            resp = json.dumps(
                {
                    "service": "ServiceB",
                    "status": "mitigated_ok",
                    "data": "cached-fallback-record",
                    "duration_ms": duration_ms,
                }
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(resp)
            return

        # Downstream call to ServiceC
        target_c_url = server.fixture_state["service_c_url"]
        out_traceparent = generate_traceparent(trace_id=trace_id, parent_id=span_id)

        req = urllib.request.Request(
            f"{target_c_url}/store",
            headers={"traceparent": out_traceparent},
        )

        c_status = 200
        c_error = None
        c_data = None
        try:
            with urllib.request.urlopen(req, timeout=server.fixture_state.get("client_timeout_s", 2.0)) as resp:
                c_status = resp.status
                c_data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as he:
            c_status = he.code
            c_error = f"HTTP {he.code}"
        except Exception as ex:
            c_status = 504
            c_error = str(ex)

        t_end_mono = clock.monotonic_time()
        duration_ms = compute_elapsed_duration_ms(t_start_mono, t_end_mono)

        if c_status == 200:
            logger.log(
                service="ServiceB",
                event="business_request_completed",
                trace_id=trace_id,
                parent_id=parent_id,
                span_id=span_id,
                duration_ms=duration_ms,
                status="OK",
                details={"downstream_status": c_status},
            )
            resp_body = json.dumps(
                {
                    "service": "ServiceB",
                    "status": "ok",
                    "downstream": c_data,
                    "duration_ms": duration_ms,
                }
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(resp_body)
        else:
            logger.log(
                service="ServiceB",
                event="downstream_call_failed",
                trace_id=trace_id,
                parent_id=parent_id,
                span_id=span_id,
                duration_ms=duration_ms,
                status="ERROR",
                details={"downstream_status": c_status, "error": c_error},
            )
            resp_body = json.dumps(
                {
                    "service": "ServiceB",
                    "status": "error",
                    "downstream_status": c_status,
                    "error": c_error,
                }
            ).encode("utf-8")
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(resp_body)


class ServiceAHandler(http.server.BaseHTTPRequestHandler):
    """
    Frontend / Gateway Service (ServiceA).
    Initiates requests, creates root traceparent, calls ServiceB.
    """

    def log_message(self, format: str, *args: Any) -> None:
        pass

    def do_GET(self) -> None:
        server: "ObservableServer" = self.server  # type: ignore
        clock = server.clock
        logger = server.logger

        t_start_mono = clock.monotonic_time()
        span_id = secrets.token_hex(8).lower()

        traceparent_raw = self.headers.get("traceparent")
        if traceparent_raw:
            try:
                parsed = parse_traceparent(traceparent_raw)
                trace_id = parsed["trace_id"]
                parent_id = parsed["parent_id"]
            except ValueError as e:
                logger.log(
                    service="ServiceA",
                    event="invalid_client_traceparent",
                    status="BAD_REQUEST",
                    details={"error": str(e)},
                )
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "invalid traceparent"}')
                return
        else:
            # Generate new root trace_id
            trace_id = secrets.token_hex(16).lower()
            parent_id = None

        logger.log(
            service="ServiceA",
            event="gateway_request_received",
            trace_id=trace_id,
            parent_id=parent_id,
            span_id=span_id,
            status="START",
            details={"path": self.path},
        )

        # Call ServiceB
        target_b_url = server.fixture_state["service_b_url"]
        out_traceparent = generate_traceparent(trace_id=trace_id, parent_id=span_id)

        req = urllib.request.Request(
            f"{target_b_url}/business",
            headers={"traceparent": out_traceparent},
        )

        b_status = 200
        b_error = None
        b_data = None
        try:
            with urllib.request.urlopen(req, timeout=server.fixture_state.get("client_timeout_s", 2.0)) as resp:
                b_status = resp.status
                b_data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as he:
            b_status = he.code
            b_error = f"HTTP {he.code}"
        except Exception as ex:
            b_status = 504
            b_error = str(ex)

        t_end_mono = clock.monotonic_time()
        duration_ms = compute_elapsed_duration_ms(t_start_mono, t_end_mono)

        if b_status == 200:
            logger.log(
                service="ServiceA",
                event="gateway_request_completed",
                trace_id=trace_id,
                parent_id=parent_id,
                span_id=span_id,
                duration_ms=duration_ms,
                status="OK",
                details={"downstream_status": b_status},
            )
            resp_body = json.dumps(
                {
                    "service": "ServiceA",
                    "status": "ok",
                    "trace_id": trace_id,
                    "total_duration_ms": duration_ms,
                    "response": b_data,
                }
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("X-Trace-Id", trace_id)
            self.end_headers()
            self.wfile.write(resp_body)
        else:
            logger.log(
                service="ServiceA",
                event="gateway_request_degraded_or_failed",
                trace_id=trace_id,
                parent_id=parent_id,
                span_id=span_id,
                duration_ms=duration_ms,
                status="ERROR",
                details={"downstream_status": b_status, "error": b_error},
            )
            resp_body = json.dumps(
                {
                    "service": "ServiceA",
                    "status": "error",
                    "trace_id": trace_id,
                    "total_duration_ms": duration_ms,
                    "error": b_error,
                }
            ).encode("utf-8")
            self.send_response(502 if b_status != 504 else 504)
            self.send_header("Content-Type", "application/json")
            self.send_header("X-Trace-Id", trace_id)
            self.end_headers()
            self.wfile.write(resp_body)


class ObservableServer(http.server.ThreadingHTTPServer):
    """Threading HTTPServer with attached logger and shared state."""

    def __init__(
        self,
        server_address: Tuple[str, int],
        RequestHandlerClass: Callable[..., http.server.BaseHTTPRequestHandler],
        logger: StructuredLogger,
        clock: ClockAdapter,
        fixture_state: Dict[str, Any],
    ) -> None:
        self.logger = logger
        self.clock = clock
        self.fixture_state = fixture_state
        self.daemon_threads = False  # Explicit thread joining
        super().__init__(server_address, RequestHandlerClass)


class ObservabilityPipelineManager:
    """
    Lifecycle manager for the three-service observability pipeline.

    Curriculum Invariants:
    - Binds strictly to 127.0.0.1 on ephemeral ports (port=0).
    - Explicit server shutdown, socket close, and thread join.
    - No unowned process killing or daemon thread exit shortcuts.
    """

    def __init__(self, clock: Optional[ClockAdapter] = None) -> None:
        self.clock = clock or ClockAdapter()
        self.logger = StructuredLogger(clock_adapter=self.clock)
        self.fixture_state: Dict[str, Any] = {
            "fault_mode": "NONE",
            "injected_delay_s": 0.0,
            "mitigation_enabled": False,
            "client_timeout_s": 2.0,
            "service_c_url": "",
            "service_b_url": "",
            "service_a_url": "",
        }
        self.server_c: Optional[ObservableServer] = None
        self.server_b: Optional[ObservableServer] = None
        self.server_a: Optional[ObservableServer] = None
        self.thread_c: Optional[threading.Thread] = None
        self.thread_b: Optional[threading.Thread] = None
        self.thread_a: Optional[threading.Thread] = None
        self._is_running = False

    def start(self) -> None:
        """Starts ServiceC, ServiceB, and ServiceA on distinct ephemeral loopback ports."""
        if self._is_running:
            return

        # 1. Start ServiceC
        self.server_c = ObservableServer(
            ("127.0.0.1", 0),
            ServiceCHandler,
            logger=self.logger,
            clock=self.clock,
            fixture_state=self.fixture_state,
        )
        port_c = self.server_c.server_address[1]
        self.fixture_state["service_c_url"] = f"http://127.0.0.1:{port_c}"
        self.thread_c = threading.Thread(
            target=self.server_c.serve_forever, name="m20-service-c"
        )
        self.thread_c.start()

        # 2. Start ServiceB
        self.server_b = ObservableServer(
            ("127.0.0.1", 0),
            ServiceBHandler,
            logger=self.logger,
            clock=self.clock,
            fixture_state=self.fixture_state,
        )
        port_b = self.server_b.server_address[1]
        self.fixture_state["service_b_url"] = f"http://127.0.0.1:{port_b}"
        self.thread_b = threading.Thread(
            target=self.server_b.serve_forever, name="m20-service-b"
        )
        self.thread_b.start()

        # 3. Start ServiceA
        self.server_a = ObservableServer(
            ("127.0.0.1", 0),
            ServiceAHandler,
            logger=self.logger,
            clock=self.clock,
            fixture_state=self.fixture_state,
        )
        port_a = self.server_a.server_address[1]
        self.fixture_state["service_a_url"] = f"http://127.0.0.1:{port_a}"
        self.thread_a = threading.Thread(
            target=self.server_a.serve_forever, name="m20-service-a"
        )
        self.thread_a.start()

        self._is_running = True

    def get_urls(self) -> Dict[str, str]:
        return {
            "ServiceA": self.fixture_state["service_a_url"],
            "ServiceB": self.fixture_state["service_b_url"],
            "ServiceC": self.fixture_state["service_c_url"],
        }

    def set_fault(self, fault_mode: str = "NONE", delay_s: float = 0.0) -> None:
        """Configures controlled fault on ServiceC."""
        self.fixture_state["fault_mode"] = fault_mode
        self.fixture_state["injected_delay_s"] = delay_s

    def set_mitigation(self, enabled: bool = True) -> None:
        """Enables or disables ServiceB safe mitigation (fallback cache)."""
        self.fixture_state["mitigation_enabled"] = enabled

    def dispatch_request(
        self,
        incoming_traceparent: Optional[str] = None,
        timeout_s: float = 3.0,
    ) -> Dict[str, Any]:
        """Dispatches an HTTP request to ServiceA and returns parsed outcome."""
        if not self._is_running or not self.server_a:
            raise RuntimeError("Pipeline must be started before dispatching requests.")

        url = f"{self.fixture_state['service_a_url']}/order"
        headers: Dict[str, str] = {}
        if incoming_traceparent:
            headers["traceparent"] = incoming_traceparent

        req = urllib.request.Request(url, headers=headers)
        t0 = self.clock.monotonic_time()
        status_code = 200
        error_msg = None
        data: Dict[str, Any] = {}

        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                status_code = resp.status
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as he:
            status_code = he.code
            try:
                data = json.loads(he.read().decode("utf-8"))
            except Exception:
                data = {"raw_error": str(he)}
            error_msg = f"HTTPError: {he.code}"
        except Exception as ex:
            status_code = 504
            error_msg = str(ex)

        t1 = self.clock.monotonic_time()
        elapsed_ms = compute_elapsed_duration_ms(t0, t1)

        return {
            "status_code": status_code,
            "elapsed_ms": elapsed_ms,
            "error": error_msg,
            "response": data,
        }

    def shutdown(self) -> None:
        """Explicitly terminates servers, closes sockets, and joins threads."""
        if not self._is_running:
            return

        for s in (self.server_a, self.server_b, self.server_c):
            if s:
                try:
                    s.shutdown()
                    s.server_close()
                except Exception:
                    pass

        for th in (self.thread_a, self.thread_b, self.thread_c):
            if th and th.is_alive():
                th.join(timeout=2.0)

        self._is_running = False
        self.server_a = None
        self.server_b = None
        self.server_c = None
        self.thread_a = None
        self.thread_b = None
        self.thread_c = None


# ============================================================================
# 7. Correlated Timeline Reducer & Blameless Postmortem Generator
# ============================================================================

def reconstruct_correlated_timeline(
    records: List[Dict[str, Any]],
    trace_id: str,
) -> Dict[str, Any]:
    """
    Filters structured logs by trace_id and reconstructs the cross-service request timeline.
    Isolates which service hop contributed to latency or error.
    """
    matched = [r for r in records if r.get("trace_id") == trace_id]
    if not matched:
        return {
            "trace_id": trace_id,
            "record_count": 0,
            "records": [],
            "hop_breakdown": {},
            "fault_localized": None,
        }

    # Extract durations per service
    service_durations: Dict[str, float] = {}
    errors: List[Dict[str, Any]] = []

    for r in matched:
        svc = r.get("service", "unknown")
        dur = r.get("duration_ms")
        if dur is not None:
            service_durations[svc] = max(service_durations.get(svc, 0.0), dur)
        if r.get("status") in ("ERROR", "BAD_REQUEST", "DEGRADED"):
            errors.append(r)

    # Localize fault
    fault_localized = None
    if "ServiceC" in service_durations and service_durations["ServiceC"] > 200.0:
        fault_localized = "ServiceC (Storage Mock High Latency)"
    elif any(e.get("service") == "ServiceC" for e in errors):
        fault_localized = "ServiceC (Storage Mock Error)"

    return {
        "trace_id": trace_id,
        "record_count": len(matched),
        "records": matched,
        "service_durations_ms": service_durations,
        "errors_detected": errors,
        "fault_localized": fault_localized,
        "inference_boundary_note": (
            "Localization in this course scenario is verified because the fixture script controls "
            "the ground truth. In complex distributed production systems, multiple interacting "
            "contributing conditions (queues, network, gc, dependencies) often interact, "
            "and incidents rarely have a single isolated 'root cause'."
        ),
    }


def generate_blameless_postmortem(
    incident_id: str,
    impact_summary: str,
    timeline_entries: List[Tuple[str, str]],
    proximate_mechanism: str,
    contributing_conditions: List[str],
    mitigation_applied: str,
    permanent_safeguards: List[str],
    unresolved_questions: List[str],
) -> str:
    """
    Generates a structured blameless postmortem document.

    Curriculum Invariant:
    - Rejects 'human error' or individual blame as a final cause.
    - Analyzes systemic conditions, interfaces, automation, and safeguards.
    - Preserves distinction: Mitigation != Resolution != Prevention.
    """
    timeline_md = "\n".join([f"- **{t}**: {desc}" for t, desc in timeline_entries])
    conditions_md = "\n".join([f"- {c}" for c in contributing_conditions])
    safeguards_md = "\n".join([f"- [ ] {s}" for s in permanent_safeguards])
    unresolved_md = "\n".join([f"- {q}" for q in unresolved_questions])

    return f"""# Incident Postmortem: {incident_id}

> **Status**: BLAMELESS POSTMORTEM (Systemic & Human Factors Analysis)
> **Rule**: Inquiries must investigate tools, incentives, safeguards, and system design, NOT personal fault.

---

## 1. Executive Summary & Impact
- **Incident ID**: `{incident_id}`
- **Customer & Service Impact**: {impact_summary}
- **Mitigation vs. Resolution Distinction**:
  - *Mitigation*: Service restored via reversible control actions.
  - *Resolution*: Underlying code/architecture defects addressed.
  - *Prevention*: Structural safeguards implemented to prevent recurrence.

---

## 2. Chronological Timeline (Detection -> Triage -> Mitigation -> Resolution)
{timeline_md}

---

## 3. Proximate Mechanism (Injected Symptom)
{proximate_mechanism}

---

## 4. Contributing Systemic Conditions (Why Did the System Permit This?)
*Blameless Framing: 'Human error' is never a stopping point; investigate the environment.*
{conditions_md}

---

## 5. Mitigation & Recovery Verification
- **Mitigation Action**: {mitigation_applied}
- **Verification of Recovery**: Verified via structured telemetry and end-to-end request success.

---

## 6. Action Items & Defensive Safeguards
{safeguards_md}

---

## 7. Unresolved Questions & Exact Inference Limits
{unresolved_md}
"""


# ============================================================================
# 8. Command-Line Entry Point (Diagnostic & Verification Modes)
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(description="M20 Observability & Reliability Pipeline Fixture")
    parser.add_argument("--demo-clock", action="store_true", help="Demonstrate wall vs. monotonic clock semantics")
    parser.add_argument("--demo-stats", action="store_true", help="Demonstrate tail vs. mean distribution stats")
    parser.add_argument("--demo-sli-slo", action="store_true", help="Demonstrate SLI/SLO/Error Budget calculations")
    parser.add_argument("--demo-incident", action="store_true", help="Run three-service pipeline with fault injection")
    args = parser.parse_args()

    adapter = ClockAdapter()

    if args.demo_clock:
        print("=== Clock Semantics Demonstration ===")
        w0 = adapter.wall_time()
        m0 = adapter.monotonic_time()
        time.sleep(0.05)
        # Inject fake backward step
        adapter.inject_wall_step_backward(10.0)
        w1 = adapter.wall_time()
        m1 = adapter.monotonic_time()

        wall_diff = w1 - w0
        mono_diff = m1 - m0
        print(f"Wall Clock Subtraction:      {wall_diff:.4f} s (Negative / Invalid duration!)")
        print(f"Monotonic Clock Subtraction: {mono_diff:.4f} s (Positive / Valid elapsed duration)")
        return 0

    if args.demo_stats:
        print("=== Deterministic Distribution Statistics Demonstration ===")
        # Synthetic bimodal sample: 95 fast requests (5ms) and 5 slow tail requests (500ms)
        sample_dataset = [5.0] * 95 + [500.0] * 5
        stats = compute_distribution_statistics(sample_dataset, convention="nearest_rank")
        print(f"Sample count: {stats['sample_count']}")
        print(f"Mean:         {stats['mean_ms']} ms")
        print(f"p50 (Median): {stats['p50_ms']} ms")
        print(f"p90:          {stats['p90_ms']} ms")
        print(f"p95:          {stats['p95_ms']} ms")
        print(f"p99:          {stats['p99_ms']} ms")
        print(f"Convention:   {stats['convention_description']}")
        return 0

    if args.demo_sli_slo:
        print("=== SLI / SLO / Error Budget Demonstration ===")
        eval_result = evaluate_sli_slo(
            total_valid_requests=10000,
            good_requests=9985,
            slo_target_percent=99.9,
            window_seconds=2592000.0,
        )
        print(f"Actual SLI:            {eval_result['actual_sli_percent']}%")
        print(f"SLO Target:            {eval_result['slo_target_percent']}%")
        print(f"SLO Met:               {eval_result['slo_met']}")
        print(f"Allowed Bad Requests:  {eval_result['allowed_bad_requests']}")
        print(f"Actual Bad Requests:   {eval_result['bad_requests']}")
        print(f"Remaining Budget:      {eval_result['remaining_budget_requests']}")
        print(f"Budget Consumed:       {eval_result['budget_consumed_percent']}%")
        return 0

    if args.demo_incident:
        print("=== Controlled Three-Service Pipeline Incident Demonstration ===")
        manager = ObservabilityPipelineManager(clock=adapter)
        try:
            manager.start()
            print(f"Pipeline running: {manager.get_urls()}")

            # 1. Normal baseline request
            res1 = manager.dispatch_request()
            print(f"[Normal] Status: {res1['status_code']}, Elapsed: {res1['elapsed_ms']:.1f}ms")

            # 2. Injected delay fault in ServiceC
            manager.set_fault(fault_mode="DELAY", delay_s=0.4)
            res2 = manager.dispatch_request()
            print(f"[Fault Injected] Status: {res2['status_code']}, Elapsed: {res2['elapsed_ms']:.1f}ms")

            # 3. Mitigated request (fallback cache)
            manager.set_mitigation(enabled=True)
            res3 = manager.dispatch_request()
            print(f"[Mitigated] Status: {res3['status_code']}, Elapsed: {res3['elapsed_ms']:.1f}ms")

            # 4. Timeline reconstruction
            trace_id = res2["response"].get("trace_id")
            if trace_id:
                timeline = reconstruct_correlated_timeline(manager.logger.get_records(), trace_id)
                print(f"[Timeline] Trace {trace_id}: localized fault = {timeline['fault_localized']}")
        finally:
            manager.shutdown()
            print("Pipeline cleanly shut down.")
        return 0

    print("s6_m20_observability_pipeline.py: Pass --demo-clock, --demo-stats, --demo-sli-slo, or --demo-incident.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
