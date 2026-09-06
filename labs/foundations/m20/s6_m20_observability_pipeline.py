#!/usr/bin/env python3
"""
s6_m20_observability_pipeline.py — Zero-SaaS Observability & Reliability Pipeline Fixture
========================================================================================

Canonical Stage 6 / Module 20 (M20) Observability & Reliability Engineering Fixture.
Contract authority: GitHub Issue #110, S6 Design Dossier v0.1, and Lead Review Rework.

Architectural Commitments:
1. Zero-SaaS and stdlib-first: No Prometheus, Grafana, Datadog, Jaeger, Docker, or Cloud dependencies.
2. Clock Semantics Invariant: Correctness-sensitive elapsed duration is computed ONLY from
   monotonic clock sources (time.monotonic() or time.perf_counter()). Wall-clock timestamps
   (time.time()) are preserved strictly as calendar/event labels and NEVER subtracted for duration.
   Python monotonic clock abstraction: cannot go backwards, unaffected by system clock updates;
   reference point of the returned value is undefined.
3. Fake Adjustable Wall Clock: Teaching adapter injects simulated backward wall steps without
   mutating the host system clock or claiming real NTP reproduction.
4. Deterministic Distribution Statistics: Stated dataset/window, sample count, and exact
   percentile convention (nearest_rank). Request percentiles are never equated to fixed user fractions.
5. SLI/SLO/Error Budget Dimensional Discipline:
   - Request-based SLIs evaluate event ratios and yield event/request budgets.
   - Time-based availability SLIs evaluate uptime/downtime durations over an explicit time window.
   - These are decoupled into independent scenarios; request percentiles are never converted into downtime minutes.
   - Budget exhaustion is a mathematical status; team response is governed by team policy.
   - SLAs are kept distinct from SLOs.
6. W3C Trace Context Level 1 version-00 STRICT: Validates version==00, 32-hex trace_id, 16-hex parent_id,
   2-hex flags; rejects all-zero IDs, version!=00 (including 01 and ff), wrong lengths, non-hex chars.
   Trace context is a correlation mechanism, NEVER authentication, secrecy, or identity.
7. Structured Logging Engine: Valid JSON output with recursive privacy sanitization redacting
   passwords, authorization headers, cookies, tokens, and secrets across nested dicts and lists.
   Distinguishes wall timestamp from monotonic duration.
8. Local Three-Service Pipeline: ServiceA (Frontend) -> ServiceB (Business) -> ServiceC (Storage Mock).
   All bind strictly to 127.0.0.1 on OS-selected ephemeral ports (port=0).
9. Incident Lifecycle & Blameless Postmortem: Evidence-driven postmortem recording actual observations,
   actual mitigation, explicit recovery status, and unexecuted resolution marked NOT PERFORMED / PROPOSED FOLLOW-UP.
10. Lifecycle Safety & Fail-Closed Shutdown: Explicit shutdown, socket close, thread join verification,
    and owned-subprocess watchdog protection (no fake threading.Timer watchdog).
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
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union


# ============================================================================
# 1. Clock Semantics & Fake Wall-Clock Adapter
# ============================================================================

class ClockAdapter:
    """
    Teaching adapter demonstrating clock semantics without mutating host system clock.

    Curriculum Invariant:
    - Elapsed duration for correctness-sensitive logic MUST derive from monotonic clocks.
    - Python monotonic clock abstraction: cannot go backwards, unaffected by system clock updates;
      the reference point of the returned value is undefined.
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
        Returns monotonic time in seconds using Python's time.monotonic().
        Guaranteed non-decreasing and unaffected by system clock adjustments.
        """
        return time.monotonic()

    def perf_counter(self) -> float:
        """Returns high-resolution monotonic time in seconds."""
        return time.perf_counter()

    def inject_wall_step_backward(self, step_seconds: float) -> None:
        """
        Injects a backward adjustment into the teaching wall-clock adapter.
        Teaching adapter only: DOES NOT mutate real host clock or claim real NTP reproduction.
        """
        if step_seconds < 0:
            raise ValueError("step_seconds must be non-negative.")
        self._simulated_wall_offset_seconds -= step_seconds

    def reset_offset(self) -> None:
        """Resets simulated wall clock offset to zero."""
        self._simulated_wall_offset_seconds = 0.0


def compute_elapsed_duration_ms(start_mono: float, end_mono: float) -> float:
    """
    Computes elapsed duration in milliseconds from monotonic readings.
    Guaranteed non-negative under the Python monotonic clock invariant.
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
        "percentile_vs_user_boundary": (
            "Request percentiles characterize the latency distribution of requests in this window. "
            "They do NOT imply that exactly (100 - P)% of distinct users experienced that latency, "
            "as request frequency per user is generally non-uniform."
        ),
    }


# ============================================================================
# 3. Decoupled SLI / SLO / Error Budget Evaluator
# ============================================================================

def evaluate_request_sli_slo(
    total_valid_requests: int,
    good_requests: int,
    slo_target_percent: float,
) -> Dict[str, Any]:
    """
    Evaluates a request-based event ratio SLI, SLO target, and Request Error Budget.

    Dimensional Rule:
    - Request-based SLIs evaluate event counts and derive an event error budget.
    - They CANNOT be converted into downtime minutes without a separate time-based availability model.
    - Budget exhaustion is a mathematical status; team response is governed by team policy.
    """
    if total_valid_requests <= 0:
        raise ValueError("total_valid_requests must be greater than 0.")
    if good_requests < 0 or good_requests > total_valid_requests:
        raise ValueError("good_requests must be between 0 and total_valid_requests.")
    if slo_target_percent <= 0.0 or slo_target_percent >= 100.0:
        raise ValueError("slo_target_percent must be strictly between 0 and 100.")

    bad_requests = total_valid_requests - good_requests
    actual_sli_percent = (good_requests / total_valid_requests) * 100.0

    allowed_failure_rate = (100.0 - slo_target_percent) / 100.0
    allowed_bad_requests = total_valid_requests * allowed_failure_rate
    remaining_budget_requests = allowed_bad_requests - bad_requests

    if allowed_bad_requests > 0:
        budget_consumed_percent = (bad_requests / allowed_bad_requests) * 100.0
    else:
        budget_consumed_percent = 0.0 if bad_requests == 0 else float("inf")

    slo_met = actual_sli_percent >= slo_target_percent

    return {
        "sli_dimension": "request_event",
        "total_valid_requests": total_valid_requests,
        "good_requests": good_requests,
        "bad_requests": bad_requests,
        "actual_sli_percent": round(actual_sli_percent, 4),
        "slo_target_percent": round(slo_target_percent, 4),
        "slo_met": slo_met,
        "allowed_bad_requests": round(allowed_bad_requests, 2),
        "remaining_budget_requests": round(remaining_budget_requests, 2),
        "budget_consumed_percent": round(budget_consumed_percent, 2),
        "dimensional_boundary": (
            "Request-based SLIs evaluate event counts and yield an event error budget in requests. "
            "They do not define or translate to downtime minutes."
        ),
        "policy_note": (
            "Budget exhaustion is a mathematical calculation. Any operational action (such as release gates, "
            "review policies, or reliability sprints) depends on the service/team's error-budget policy."
        ),
        "sla_distinction": (
            "An SLA is an external contractual or business commitment with specified remedies and exclusions. "
            "It is not an internal engineering target (SLO), and an SLA percentage is not an independent "
            "per-instance failure probability."
        ),
    }


def evaluate_time_availability_sli_slo(
    total_window_seconds: float,
    uptime_seconds: float,
    slo_target_percent: float,
) -> Dict[str, Any]:
    """
    Evaluates an independent time-based availability SLI, SLO target, and Downtime Budget.

    Dimensional Rule:
    - Time-based availability SLIs evaluate uptime/downtime durations over an explicit time window.
    - This is an independent SLI scenario from request-event counting.
    """
    if total_window_seconds <= 0.0:
        raise ValueError("total_window_seconds must be greater than 0.")
    if uptime_seconds < 0.0 or uptime_seconds > total_window_seconds:
        raise ValueError("uptime_seconds must be between 0 and total_window_seconds.")
    if slo_target_percent <= 0.0 or slo_target_percent >= 100.0:
        raise ValueError("slo_target_percent must be strictly between 0 and 100.")

    downtime_seconds = total_window_seconds - uptime_seconds
    actual_availability_percent = (uptime_seconds / total_window_seconds) * 100.0

    allowed_downtime_rate = (100.0 - slo_target_percent) / 100.0
    allowed_downtime_seconds = total_window_seconds * allowed_downtime_rate
    remaining_downtime_seconds = allowed_downtime_seconds - downtime_seconds

    if allowed_downtime_seconds > 0:
        budget_consumed_percent = (downtime_seconds / allowed_downtime_seconds) * 100.0
    else:
        budget_consumed_percent = 0.0 if downtime_seconds == 0.0 else float("inf")

    slo_met = actual_availability_percent >= slo_target_percent

    return {
        "sli_dimension": "time_duration",
        "total_window_seconds": total_window_seconds,
        "total_window_minutes": round(total_window_seconds / 60.0, 2),
        "uptime_seconds": uptime_seconds,
        "downtime_seconds": round(downtime_seconds, 2),
        "downtime_minutes": round(downtime_seconds / 60.0, 2),
        "actual_availability_percent": round(actual_availability_percent, 4),
        "slo_target_percent": round(slo_target_percent, 4),
        "slo_met": slo_met,
        "allowed_downtime_minutes": round(allowed_downtime_seconds / 60.0, 2),
        "remaining_downtime_minutes": round(remaining_downtime_seconds / 60.0, 2),
        "budget_consumed_percent": round(budget_consumed_percent, 2),
        "dimensional_boundary": (
            "Time-based availability SLIs evaluate duration (seconds/minutes) of availability. "
            "This is independent of request volume or request error rates."
        ),
    }


def evaluate_sli_slo(
    total_valid_requests: int,
    good_requests: int,
    slo_target_percent: float,
) -> Dict[str, Any]:
    """
    Convenience backward-compatible wrapper for request-based SLI evaluation.
    Enforces that request SLIs do not output downtime minutes.
    """
    return evaluate_request_sli_slo(
        total_valid_requests=total_valid_requests,
        good_requests=good_requests,
        slo_target_percent=slo_target_percent,
    )


# ============================================================================
# 4. W3C Trace Context Level 1 version-00 STRICT Generator & Parser
# ============================================================================

HEX_32_PATTERN = re.compile(r"^[0-9a-f]{32}$")
HEX_16_PATTERN = re.compile(r"^[0-9a-f]{16}$")
HEX_2_PATTERN = re.compile(r"^[0-9a-f]{2}$")


def generate_trace_id() -> str:
    """Generates a valid, non-all-zero 32-hex lowercase W3C trace ID."""
    while True:
        tid = secrets.token_hex(16).lower()
        if tid != "00000000000000000000000000000000":
            return tid


def generate_span_id() -> str:
    """Generates a valid, non-all-zero 16-hex lowercase W3C span/parent ID."""
    while True:
        sid = secrets.token_hex(8).lower()
        if sid != "0000000000000000":
            return sid


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
        trace_id = generate_trace_id()
    else:
        trace_id = trace_id.lower()
        if not HEX_32_PATTERN.match(trace_id) or trace_id == "00000000000000000000000000000000":
            raise ValueError(f"Invalid trace_id for W3C traceparent: '{trace_id}'. Must be 32 non-zero hex chars.")

    if not parent_id:
        parent_id = generate_span_id()
    else:
        parent_id = parent_id.lower()
        if not HEX_16_PATTERN.match(parent_id) or parent_id == "0000000000000000":
            raise ValueError(f"Invalid parent_id for W3C traceparent: '{parent_id}'. Must be 16 non-zero hex chars.")

    trace_flags = "01" if sampled else "00"
    return f"{version}-{trace_id}-{parent_id}-{trace_flags}"


def parse_traceparent(header_value: str) -> Dict[str, Any]:
    """
    Parses and strictly validates a W3C Trace Context Level 1 version-00 traceparent header.

    W3C Recommendation 2021 Strict version-00 Validation Rules:
    1. Must contain exactly 4 dash-separated fields.
    2. Version MUST be exactly '00'. Any other version (including '01' and 'ff') MUST BE REJECTED.
    3. Version 00 requires total header length of EXACTLY 55 characters.
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

    # Strict version-00 check: reject anything other than "00"
    if version != "00":
        raise ValueError(
            f"Unsupported or invalid traceparent version: '{version}'. "
            "This parser strictly implements W3C Level 1 version-00 only. "
            "Future versions (e.g. '01') or invalid versions (e.g. 'ff') are rejected."
        )

    # Version 00 requires exact 55 characters
    if len(header_clean) != 55:
        raise ValueError(
            f"Invalid version-00 traceparent length: expected exactly 55 characters, got {len(header_clean)}."
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
            "This parser strictly validates W3C Level 1 version-00 traceparent per W3C Recommendation (2021). "
            "It does not implement future W3C versions (e.g. Level 2) or proprietary vendor extensions."
        ),
    }


# ============================================================================
# 5. Structured Logging Engine & Recursive Privacy Sanitizer
# ============================================================================

SENSITIVE_KEY_PATTERN = re.compile(
    r"(?i)(authorization|auth|token|secret|password|passwd|cookie|credential|bearer|api_key|secret_key|private_key)"
)


def sanitize_privacy_fields(val: Any) -> Any:
    """
    Recursively sanitizes data structures to redact sensitive information.
    Operates on nested dicts, lists, tuples, and detects Bearer tokens in strings.
    """
    if isinstance(val, dict):
        sanitized_dict: Dict[str, Any] = {}
        for k, v in val.items():
            k_str = str(k)
            if SENSITIVE_KEY_PATTERN.search(k_str):
                sanitized_dict[k_str] = "[REDACTED]"
            else:
                sanitized_dict[k_str] = sanitize_privacy_fields(v)
        return sanitized_dict
    elif isinstance(val, (list, tuple)):
        return [sanitize_privacy_fields(item) for item in val]
    elif isinstance(val, str):
        if val.strip().lower().startswith("bearer "):
            return "Bearer [REDACTED]"
        return val
    else:
        return val


class StructuredLogger:
    """
    Course-owned structured logger emitting valid, parsable JSON records.

    Curriculum Invariants:
    - Emits valid JSON to memory AND to an actual JSON sink (file / stream).
    - Distinguishes calendar/event timestamp (wall clock) from monotonic duration (monotonic timer).
    - Recursively redacts passwords, authorization headers, cookies, and secret tokens.
    - Preserves correlation context (trace_id, parent_id, span_id, service, event).
    - Logs can suffer from omission, buffering, or sampling; shared timestamps do not imply causality.
    """

    def __init__(
        self,
        clock_adapter: Optional[ClockAdapter] = None,
        jsonl_path: Optional[str] = None,
        sink_stream: Optional[Any] = None,
        service_name: Optional[str] = None,
    ) -> None:
        self.clock = clock_adapter or ClockAdapter()
        self.jsonl_path = jsonl_path
        self.sink_stream = sink_stream
        self.default_service_name = service_name
        self._records: List[Dict[str, Any]] = []
        self._emitted_json_lines: List[str] = []
        self._lock = threading.Lock()

        if self.jsonl_path:
            os.makedirs(os.path.dirname(os.path.abspath(self.jsonl_path)), exist_ok=True)

    def log(
        self,
        service: str = "",
        event: str = "",
        trace_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        span_id: Optional[str] = None,
        duration_ms: Optional[float] = None,
        status: str = "OK",
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Emits and records a sanitized structured JSON log entry."""
        svc = service or self.default_service_name or "unknown_service"
        safe_details = sanitize_privacy_fields(details) if details is not None else {}

        record = {
            "timestamp_utc": self.clock.wall_time_iso(),
            "timestamp_wall_epoch_s": round(self.clock.wall_time(), 6),
            "duration_ms": round(duration_ms, 3) if duration_ms is not None else None,
            "service": svc,
            "event": event,
            "status": status,
            "trace_id": trace_id,
            "parent_id": parent_id,
            "span_id": span_id,
            "details": safe_details,
        }

        # Real JSON serialization validation
        json_line = json.dumps(record, ensure_ascii=False)

        with self._lock:
            self._records.append(record)
            self._emitted_json_lines.append(json_line)

            if self.sink_stream:
                try:
                    self.sink_stream.write(json_line + "\n")
                    if hasattr(self.sink_stream, "flush"):
                        self.sink_stream.flush()
                except Exception:
                    pass

            if self.jsonl_path:
                try:
                    with open(self.jsonl_path, "a", encoding="utf-8") as f:
                        f.write(json_line + "\n")
                except Exception:
                    pass

        return record

    def get_records(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._records)

    def get_emitted_json_lines(self) -> List[str]:
        with self._lock:
            return list(self._emitted_json_lines)

    def clear(self) -> None:
        with self._lock:
            self._records.clear()
            self._emitted_json_lines.clear()

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
        pass  # Suppress default stderr noise

    def do_GET(self) -> None:
        server: "ObservableServer" = self.server  # type: ignore
        clock = server.clock
        logger = server.logger

        t_start_mono = clock.monotonic_time()
        span_id = generate_span_id()

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
        span_id = generate_span_id()

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
    Initiates requests, creates validated root traceparent, calls ServiceB.
    """

    def log_message(self, format: str, *args: Any) -> None:
        pass

    def do_GET(self) -> None:
        server: "ObservableServer" = self.server  # type: ignore
        clock = server.clock
        logger = server.logger

        t_start_mono = clock.monotonic_time()
        span_id = generate_span_id()

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
            # Unified validated root trace ID generation
            trace_id = generate_trace_id()
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
        self.daemon_threads = False  # Explicit thread joining required
        super().__init__(server_address, RequestHandlerClass)


class ObservabilityPipelineManager:
    """
    Lifecycle manager for the three-service observability pipeline.

    Curriculum Invariants:
    - Binds strictly to 127.0.0.1 on ephemeral ports (port=0).
    - Explicit server shutdown, socket close, and verified thread join.
    - Shutdown fails closed: collects errors and verifies threads are terminated.
    - No unowned process killing or daemon thread exit shortcuts.
    """

    def __init__(
        self,
        clock: Optional[ClockAdapter] = None,
        jsonl_path: Optional[str] = None,
        watchdog_timeout_s: float = 30.0,
    ) -> None:
        self.clock = clock or ClockAdapter()
        self.logger = StructuredLogger(clock_adapter=self.clock, jsonl_path=jsonl_path)
        self.watchdog_timeout_s = watchdog_timeout_s
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
        """
        Configures controlled fault on ServiceC with strict input validation.
        Supported modes: 'NONE', 'DELAY', 'HTTP_500'.
        """
        valid_modes = {"NONE", "DELAY", "HTTP_500"}
        if fault_mode not in valid_modes:
            raise ValueError(
                f"Unsupported fault_mode '{fault_mode}'. Must be one of {sorted(valid_modes)}."
            )
        if not isinstance(delay_s, (int, float)):
            raise ValueError("delay_s must be a numeric value.")
        if delay_s < 0.0:
            raise ValueError(f"delay_s cannot be negative, got {delay_s}.")
        if delay_s > 5.0:
            raise ValueError(f"delay_s {delay_s} exceeds maximum safety bound of 5.0 seconds.")

        self.fixture_state["fault_mode"] = fault_mode
        self.fixture_state["injected_delay_s"] = float(delay_s)

    def set_mitigation(self, enabled: bool = True) -> None:
        """Enables or disables ServiceB safe mitigation (fallback cache)."""
        self.fixture_state["mitigation_enabled"] = bool(enabled)

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
        """
        Explicitly terminates servers, closes sockets, and verifies thread termination.
        Fails closed: collects any errors and verifies threads are not hanging.
        """
        if not self._is_running:
            return

        shutdown_errors: List[str] = []

        # 1. Shutdown and close sockets for each server
        servers = [
            ("ServiceA", self.server_a),
            ("ServiceB", self.server_b),
            ("ServiceC", self.server_c),
        ]
        for name, s in servers:
            if s:
                try:
                    s.shutdown()
                    s.server_close()
                except Exception as e:
                    shutdown_errors.append(f"{name} server close error: {e}")

        # 2. Join server threads and verify they are terminated
        threads = [
            ("ServiceA", self.thread_a),
            ("ServiceB", self.thread_b),
            ("ServiceC", self.thread_c),
        ]
        for name, th in threads:
            if th and th.is_alive():
                th.join(timeout=3.0)
                if th.is_alive():
                    shutdown_errors.append(f"{name} thread {th.name} failed to terminate within timeout")

        if shutdown_errors:
            raise RuntimeError(f"Pipeline shutdown failed: {'; '.join(shutdown_errors)}")

        self._is_running = False
        self.server_a = None
        self.server_b = None
        self.server_c = None
        self.thread_a = None
        self.thread_b = None
        self.thread_c = None


# ============================================================================
# 6b. Owned Subprocess Watchdog & Child Fixture Runner
# ============================================================================

class OwnedSubprocessWatchdog:
    """
    Process-boundary watchdog manager for course-owned child fixtures.

    Architecture (Curriculum Contract #110):
    Parent runner
      -> owned child process
        -> child owns ServiceA / ServiceB / ServiceC / server threads

    Invariants:
    1. Configurable watchdog timeout (timeout_s).
    2. Child normal execution: child performs graceful service shutdown before exiting.
    3. Watchdog timeout: parent terminates/kills ONLY its own created child process.
    4. Parent must wait and reap the child process handle (zero leftover processes).
    5. Parent never kills unrelated host processes.
    6. Child cleanup failures are explicitly surfaced, never swallowed.
    7. Truthful outcomes: PASS, BLOCKED, NOT RUN, TIMEOUT, CLEANUP_FAILURE.
    """

    def __init__(self, timeout_s: float = 30.0) -> None:
        if not isinstance(timeout_s, (int, float)) or timeout_s <= 0:
            raise ValueError(f"Watchdog timeout_s must be a positive number, got {timeout_s}")
        self.timeout_s = float(timeout_s)

    def run(
        self,
        cmd: List[str],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Executes the child command under parent watchdog supervision.
        Returns structured execution dictionary with truthful status.
        """
        child_env = os.environ.copy()
        if env:
            child_env.update(env)

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            env=child_env,
            text=True,
        )
        child_pid = proc.pid
        watchdog_triggered = False
        stdout_str = ""
        stderr_str = ""
        reaped = False

        timeout_cleanup_errors: List[str] = []
        try:
            stdout_str, stderr_str = proc.communicate(timeout=self.timeout_s)
            reaped = True
        except subprocess.TimeoutExpired:
            watchdog_triggered = True
            # Timeout: terminate/kill ONLY the owned child process.
            # Any failure to confirm termination + reap is a cleanup failure,
            # not a successful TIMEOUT cleanup.
            try:
                proc.kill()
            except Exception as exc:
                timeout_cleanup_errors.append(f"kill failed: {exc}")
            try:
                stdout_str, stderr_str = proc.communicate(timeout=5.0)
            except Exception as exc:
                timeout_cleanup_errors.append(f"post-kill communicate/reap failed: {exc}")
            reaped = proc.poll() is not None

        # Verify whether child process has been reaped and is dead.
        still_alive = self._is_pid_alive(child_pid)

        # Parse outcome.
        if watchdog_triggered:
            cleanup_confirmed = reaped and not still_alive
            if not cleanup_confirmed:
                if still_alive:
                    timeout_cleanup_errors.append("owned child process is still alive after watchdog cleanup")
                if not reaped:
                    timeout_cleanup_errors.append("owned child process handle was not reaped")
                cleanup_failure = "; ".join(timeout_cleanup_errors) or (
                    "watchdog timeout cleanup could not confirm owned child termination and reap"
                )
                return {
                    "status": "CLEANUP_FAILURE",
                    "watchdog_triggered": True,
                    "child_pid": child_pid,
                    "reaped": False,
                    "returncode": proc.returncode,
                    "cleanup_failure": cleanup_failure,
                    "stdout": stdout_str,
                    "stderr": stderr_str,
                    "data": None,
                }

            return {
                "status": "TIMEOUT",
                "watchdog_triggered": True,
                "child_pid": child_pid,
                "reaped": True,
                "returncode": proc.returncode,
                "cleanup_failure": None,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "data": None,
            }

        # Inspect stdout for structured JSON outcome emitted by child
        data: Optional[Dict[str, Any]] = None
        for line in reversed(stdout_str.splitlines()):
            line_s = line.strip()
            if line_s.startswith("{") and line_s.endswith("}"):
                try:
                    parsed = json.loads(line_s)
                    if isinstance(parsed, dict) and "status" in parsed:
                        data = parsed
                        break
                except Exception:
                    continue

        # Check for cleanup failure in returncode, data, or stderr
        cleanup_failure_msg: Optional[str] = None
        if data and data.get("status") == "CLEANUP_FAILURE":
            cleanup_failure_msg = data.get("cleanup_failure", "Child reported cleanup failure")
        elif "CLEANUP_FAILURE:" in stderr_str or "CLEANUP_FAILURE:" in stdout_str:
            for text in (stderr_str, stdout_str):
                for line in text.splitlines():
                    if "CLEANUP_FAILURE:" in line:
                        cleanup_failure_msg = line.split("CLEANUP_FAILURE:", 1)[1].strip()
                        break
                if cleanup_failure_msg:
                    break
        elif proc.returncode == 101:
            cleanup_failure_msg = "Child exited with code 101 indicating cleanup failure"

        if cleanup_failure_msg is not None:
            return {
                "status": "CLEANUP_FAILURE",
                "watchdog_triggered": False,
                "child_pid": child_pid,
                "reaped": reaped and not still_alive,
                "returncode": proc.returncode,
                "cleanup_failure": cleanup_failure_msg,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "data": data,
            }

        # Check for BLOCKED or NOT RUN
        if data and data.get("status") in ("BLOCKED", "NOT RUN"):
            return {
                "status": data["status"],
                "watchdog_triggered": False,
                "child_pid": child_pid,
                "reaped": reaped and not still_alive,
                "returncode": proc.returncode,
                "cleanup_failure": None,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "data": data,
            }

        # Normal completion
        if proc.returncode == 0:
            return {
                "status": "PASS",
                "watchdog_triggered": False,
                "child_pid": child_pid,
                "reaped": reaped and not still_alive,
                "returncode": 0,
                "cleanup_failure": None,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "data": data,
            }

        return {
            "status": "FAIL",
            "watchdog_triggered": False,
            "child_pid": child_pid,
            "reaped": reaped and not still_alive,
            "returncode": proc.returncode,
            "cleanup_failure": None,
            "stdout": stdout_str,
            "stderr": stderr_str,
            "data": data,
        }

    @staticmethod
    def _is_pid_alive(pid: int) -> bool:
        """Checks whether an owned process ID is still alive on the host."""
        if pid <= 0:
            return False
        if sys.platform == "win32":
            try:
                import ctypes
                PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
                handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
                if not handle:
                    return False
                exit_code = ctypes.c_ulong()
                res = ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
                ctypes.windll.kernel32.CloseHandle(handle)
                STILL_ACTIVE = 259
                return bool(res and exit_code.value == STILL_ACTIVE)
            except Exception:
                pass
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False


def run_child_fixture(
    simulate_hang: bool = False,
    simulate_cleanup_failure: bool = False,
    simulate_blocked: bool = False,
    simulate_not_run: bool = False,
) -> int:
    """
    Executes the three-service pipeline within an owned child process.
    Normal path: starts services, runs requests, performs graceful shutdown, reports PASS.
    Simulated modes support regression tests for watchdog timeout, cleanup failure, and disposition.
    """
    if simulate_blocked:
        payload = {"status": "BLOCKED", "reason": "Precondition missing in fixture environment"}
        print(json.dumps(payload))
        return 0

    if simulate_not_run:
        payload = {"status": "NOT RUN", "reason": "Execution skipped by test harness"}
        print(json.dumps(payload))
        return 0

    if simulate_hang:
        # Intentionally sleep past parent watchdog timeout to trigger watchdog reap
        time.sleep(60.0)
        return 0

    adapter = ClockAdapter()
    manager = ObservabilityPipelineManager(clock=adapter)
    manager.start()

    res1 = manager.dispatch_request()
    manager.set_fault(fault_mode="DELAY", delay_s=0.20)
    res2 = manager.dispatch_request()
    manager.set_mitigation(enabled=True)
    res3 = manager.dispatch_request()

    # Graceful shutdown with explicit cleanup failure surfacing
    try:
        if simulate_cleanup_failure:
            def _failing_close() -> None:
                raise OSError("Simulated server close error during child cleanup")
            if manager.server_c:
                manager.server_c.server_close = _failing_close  # type: ignore[assignment]
        manager.shutdown()
    except Exception as exc:
        err_msg = str(exc)
        print(json.dumps({"status": "CLEANUP_FAILURE", "cleanup_failure": err_msg}))
        print(f"CLEANUP_FAILURE: {err_msg}", file=sys.stderr)
        return 101

    payload = {
        "status": "PASS",
        "urls": manager.get_urls(),
        "trace_id": res2["response"].get("trace_id"),
        "records_count": len(manager.logger.get_records()),
        "mitigated_status": res3["status_code"],
    }
    print(json.dumps(payload))
    return 0


# ============================================================================
# 7. Correlated Timeline Reducer & Blameless Postmortem Generator
# ============================================================================

def reconstruct_correlated_timeline(
    records: List[Dict[str, Any]],
    trace_id: str,
    fault_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Filters structured logs by trace_id and reconstructs the cross-service request timeline.

    Diagnostic Rule:
    - Does NOT use a fixed arbitrary latency threshold (like 200ms) to judge fault.
    - Localizes based on:
      1) Services emitting error or DEGRADED status events;
      2) Relative duration concentration (hop accounting for dominant share of total duration);
      3) Fixture ground truth cross-reference.
    - Distinguishes fixture ground truth from production diagnostic inference.
    """
    matched = [r for r in records if r.get("trace_id") == trace_id]
    if not matched:
        return {
            "trace_id": trace_id,
            "record_count": 0,
            "records": [],
            "hop_breakdown": {},
            "fault_localized": None,
            "diagnostic_inference": "No records matched trace ID",
        }

    service_durations: Dict[str, float] = {}
    degraded_services: List[str] = []
    errors: List[Dict[str, Any]] = []

    for r in matched:
        svc = r.get("service", "unknown")
        dur = r.get("duration_ms")
        if dur is not None:
            service_durations[svc] = max(service_durations.get(svc, 0.0), dur)
        if r.get("status") in ("ERROR", "BAD_REQUEST", "DEGRADED"):
            degraded_services.append(svc)
            errors.append(r)

    # Calculate total duration from gateway (ServiceA) or maximum observed hop
    total_dur = service_durations.get("ServiceA", max(service_durations.values()) if service_durations else 0.0)

    # Localize bottleneck through relative duration concentration and status events
    fault_localized = None
    inference_detail = None

    if "ServiceC" in degraded_services:
        fault_localized = "ServiceC"
        inference_detail = "ServiceC emitted DEGRADED / ERROR events during storage execution"
    elif total_dur > 0 and "ServiceC" in service_durations and (service_durations["ServiceC"] / total_dur) >= 0.70:
        fault_localized = "ServiceC"
        share_pct = (service_durations["ServiceC"] / total_dur) * 100.0
        inference_detail = f"ServiceC accounted for {share_pct:.1f}% of total request duration"
    elif errors:
        fault_localized = errors[0].get("service", "unknown")
        inference_detail = f"First error observed at {fault_localized}"

    return {
        "trace_id": trace_id,
        "record_count": len(matched),
        "records": matched,
        "service_durations_ms": service_durations,
        "total_request_duration_ms": total_dur,
        "errors_detected": errors,
        "fault_localized": fault_localized,
        "diagnostic_inference": inference_detail,
        "fixture_ground_truth": fault_metadata or {
            "injected_target": "ServiceC",
            "note": "Fixture owns ground truth of injected fault",
        },
        "production_inference_boundary": (
            "In real production incidents, correlation evidence indicates where duration or errors "
            "concentrated, but multiple interacting conditions (queues, network, GC, dependencies) "
            "often coexist; do not assume a universal single root cause."
        ),
    }


def generate_blameless_postmortem(
    incident_id: str,
    impact_summary: str,
    timeline_entries: List[Tuple[str, str]],
    proximate_mechanism: str,
    contributing_conditions: List[str],
    mitigation_applied: str,
    recovery_status: str,
    recovery_evidence: str,
    resolution_status: str = "NOT PERFORMED / PROPOSED FOLLOW-UP",
    resolution_plan: str = "",
    permanent_safeguards: Optional[List[str]] = None,
    unresolved_questions: Optional[List[str]] = None,
) -> str:
    """
    Generates a structured, evidence-driven blameless postmortem document.

    Curriculum Invariants:
    - Output is strictly evidence-driven: recovery status and evidence are passed explicitly.
    - Output recovery_status is strictly validated against {'PASS', 'BLOCKED', 'NOT RUN'}.
    - Does NOT fabricate unobserved facts (e.g. fake p99 alerts or unexecuted code fixes).
    - Distinguishes Mitigation from Resolution; unexecuted resolution is explicitly marked
      NOT PERFORMED / PROPOSED FOLLOW-UP.
    - Rejects 'human error' or personal fault as a final cause; investigates tools and safeguards.
    """
    valid_recovery_statuses = {"PASS", "BLOCKED", "NOT RUN"}
    if recovery_status not in valid_recovery_statuses:
        raise ValueError(
            f"Invalid recovery_status '{recovery_status}'. Must be one of {sorted(valid_recovery_statuses)}."
        )

    timeline_md = "\n".join([f"- **{t}**: {desc}" for t, desc in timeline_entries])
    conditions_md = "\n".join([f"- {c}" for c in contributing_conditions])
    safeguards_list = permanent_safeguards or [
        "Implement non-blocking timeout circuit breaker in ServiceB for storage calls",
        "Add automated canary verification for backend storage configuration updates",
        "Enforce W3C traceparent propagation across all internal RPC boundaries",
    ]
    safeguards_md = "\n".join([f"- [ ] {s}" for s in safeguards_list])
    unresolved_list = unresolved_questions or [
        "What is the maximum acceptable cache staleness during extended downstream degradation?",
        "How do network packet loss and partial partitions alter timeout detection thresholds?",
    ]
    unresolved_md = "\n".join([f"- {q}" for q in unresolved_list])

    return f"""# Incident Postmortem: {incident_id}

> **Status**: BLAMELESS POSTMORTEM (Systemic & Human Factors Analysis)
> **Rule**: Inquiries must investigate tools, incentives, safeguards, and system design, NOT personal fault.

---

## 1. Executive Summary & Impact
- **Incident ID**: `{incident_id}`
- **Customer & Service Impact**: {impact_summary}
- **Mitigation vs. Resolution Distinction**:
  - *Mitigation*: Service restored via reversible control actions.
  - *Resolution*: Underlying code/architecture defects permanently addressed.
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
- **Recovery Verification Status**: {recovery_status}
- **Recovery Observable Evidence**: {recovery_evidence}

---

## 6. Resolution Status & Defensive Safeguards
- **Resolution Status**: `{resolution_status}`
- **Proposed Resolution Plan**: {resolution_plan or "Engineering follow-up to address underlying dependency contention."}
- **Defensive Safeguards (Proposed)**:
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
    parser.add_argument("--demo-sli-slo", action="store_true", help="Demonstrate decoupled SLI/SLO calculations")
    parser.add_argument("--demo-incident", action="store_true", help="Run three-service pipeline with fault injection")
    parser.add_argument("--child-fixture", action="store_true", help="Execute three-service pipeline in child process mode under watchdog")
    parser.add_argument("--simulate-hang", action="store_true", help="Simulate child hanging indefinitely")
    parser.add_argument("--simulate-cleanup-failure", action="store_true", help="Simulate child shutdown failure")
    parser.add_argument("--simulate-blocked", action="store_true", help="Simulate BLOCKED status in child")
    parser.add_argument("--simulate-not-run", action="store_true", help="Simulate NOT RUN status in child")
    args = parser.parse_args()

    if args.child_fixture:
        return run_child_fixture(
            simulate_hang=args.simulate_hang,
            simulate_cleanup_failure=args.simulate_cleanup_failure,
            simulate_blocked=args.simulate_blocked,
            simulate_not_run=args.simulate_not_run,
        )

    adapter = ClockAdapter()

    if args.demo_clock:
        print("=== Clock Semantics Demonstration ===")
        w0 = adapter.wall_time()
        m0 = adapter.monotonic_time()
        time.sleep(0.05)
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
        print("=== SLI / SLO / Error Budget Decoupled Demonstration ===")
        req_eval = evaluate_request_sli_slo(
            total_valid_requests=10000,
            good_requests=9985,
            slo_target_percent=99.9,
        )
        print("[1. Request-Based SLI]:")
        print(f"  Actual SLI:            {req_eval['actual_sli_percent']}%")
        print(f"  SLO Target:            {req_eval['slo_target_percent']}%")
        print(f"  SLO Met:               {req_eval['slo_met']}")
        print(f"  Allowed Bad Requests:  {req_eval['allowed_bad_requests']}")
        print(f"  Actual Bad Requests:   {req_eval['bad_requests']}")
        print(f"  Remaining Budget:      {req_eval['remaining_budget_requests']}")
        print(f"  Budget Consumed:       {req_eval['budget_consumed_percent']}%")

        time_eval = evaluate_time_availability_sli_slo(
            total_window_seconds=2592000.0,  # 30 days
            uptime_seconds=2591000.0,
            slo_target_percent=99.9,
        )
        print("\n[2. Time-Based Availability SLI (Independent Scenario)]:")
        print(f"  Actual Availability:   {time_eval['actual_availability_percent']}%")
        print(f"  SLO Target:            {time_eval['slo_target_percent']}%")
        print(f"  Allowed Downtime:      {time_eval['allowed_downtime_minutes']} minutes")
        print(f"  Actual Downtime:       {time_eval['downtime_minutes']} minutes")
        print(f"  Remaining Downtime:    {time_eval['remaining_downtime_minutes']} minutes")
        return 0

    if args.demo_incident:
        print("=== Controlled Three-Service Pipeline Incident Demonstration ===")
        manager = ObservabilityPipelineManager(clock=adapter)
        try:
            manager.start()
            print(f"Pipeline running: {manager.get_urls()}")

            res1 = manager.dispatch_request()
            print(f"[Normal] Status: {res1['status_code']}, Elapsed: {res1['elapsed_ms']:.1f}ms")

            manager.set_fault(fault_mode="DELAY", delay_s=0.4)
            res2 = manager.dispatch_request()
            print(f"[Fault Injected] Status: {res2['status_code']}, Elapsed: {res2['elapsed_ms']:.1f}ms")

            manager.set_mitigation(enabled=True)
            res3 = manager.dispatch_request()
            print(f"[Mitigated] Status: {res3['status_code']}, Elapsed: {res3['elapsed_ms']:.1f}ms")

            trace_id = res2["response"].get("trace_id")
            if trace_id:
                timeline = reconstruct_correlated_timeline(manager.logger.get_records(), trace_id)
                print(f"[Timeline] Trace {trace_id}: localized fault = {timeline['fault_localized']}")
                print(f"           Diagnostic inference: {timeline['diagnostic_inference']}")
        finally:
            manager.shutdown()
            print("Pipeline cleanly shut down.")
        return 0

    print("s6_m20_observability_pipeline.py: Pass --demo-clock, --demo-stats, --demo-sli-slo, or --demo-incident.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
