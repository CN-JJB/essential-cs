"""Structured local observability (P8).

Three signals, deliberately small and local:

* **Structured logs** — one JSON object per line, always carrying a
  ``request_id`` so a single request can be followed across the HTTP adapter,
  the service core, and the dependency call.
* **Metrics** — bounded-label counters and latency summaries. Labels are the
  *route* and *status class*, never ``item_id``/``user_id``/``request_id``:
  those are unbounded-cardinality and would make the metric store grow with
  traffic (a classic observability cost failure).
* **Redaction** — secret-bearing field names are redacted *before* a record is
  written. Note content is truncated, never logged whole.

Design rule: telemetry must not change user-visible correctness. Logging and
metric failures are swallowed; the request path is never broken by the
instrumentation.
"""

from __future__ import annotations

import json
import os
import threading
import time
import uuid

#: Field names (or substrings) whose values are never emitted verbatim.
_REDACT_EXACT = {
    "password",
    "password_hash",
    "password_salt",
    "token",
    "authorization",
    "secret",
    "cookie",
    "set-cookie",
}
_REDACT_SUBSTRINGS = ("token", "password", "secret", "authorization")

#: Free-text fields are truncated so a log line stays bounded.
_TRUNCATE_KEYS = {"body", "title", "summary", "url", "message"}
_TRUNCATE_AT = 80

REDACTED = "[REDACTED]"


def _should_redact(key: str) -> bool:
    lowered = key.lower()
    if lowered in _REDACT_EXACT:
        return True
    return any(part in lowered for part in _REDACT_SUBSTRINGS)


def redact(value: object, _key: str = "") -> object:
    """Recursively redact/truncate a value so it is safe to persist."""
    if isinstance(value, dict):
        return {k: redact(v, k) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact(v, _key) for v in value]
    if isinstance(value, str) and _key.lower() in _TRUNCATE_KEYS:
        if len(value) > _TRUNCATE_AT:
            return value[:_TRUNCATE_AT] + f"…(+{len(value) - _TRUNCATE_AT})"
    return value


def sanitize_fields(fields: dict) -> dict:
    """Apply redaction rules to a structured record's fields."""
    out: dict = {}
    for key, value in fields.items():
        if _should_redact(key):
            out[key] = REDACTED
        else:
            out[key] = redact(value, key)
    return out


#: Latency histogram upper bounds in milliseconds. Fixed and bounded so the
#: metric store cannot grow with observation count.
_LATENCY_BUCKETS_MS = (5, 10, 25, 50, 100, 250, 500, 1000, 2500)


class Metrics:
    """Thread-safe, bounded-cardinality counters and latency summaries."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: dict[str, int] = {}
        self._latency: dict[str, dict] = {}

    def increment(self, name: str, amount: int = 1) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + amount

    def observe_latency(self, route: str, duration_ms: float) -> None:
        with self._lock:
            entry = self._latency.setdefault(
                route,
                {
                    "count": 0,
                    "total_ms": 0.0,
                    "min_ms": None,
                    "max_ms": None,
                    "buckets": {str(b): 0 for b in _LATENCY_BUCKETS_MS},
                    "overflow": 0,
                },
            )
            entry["count"] += 1
            entry["total_ms"] += duration_ms
            entry["min_ms"] = (
                duration_ms if entry["min_ms"] is None else min(entry["min_ms"], duration_ms)
            )
            entry["max_ms"] = (
                duration_ms if entry["max_ms"] is None else max(entry["max_ms"], duration_ms)
            )
            placed = False
            for bound in _LATENCY_BUCKETS_MS:
                if duration_ms <= bound:
                    entry["buckets"][str(bound)] += 1
                    placed = True
                    break
            if not placed:
                entry["overflow"] += 1

    def snapshot(self) -> dict:
        with self._lock:
            latency = {}
            for route, entry in self._latency.items():
                count = entry["count"] or 1
                latency[route] = {
                    "count": entry["count"],
                    "mean_ms": round(entry["total_ms"] / count, 3),
                    "min_ms": round(entry["min_ms"], 3) if entry["min_ms"] is not None else None,
                    "max_ms": round(entry["max_ms"], 3) if entry["max_ms"] is not None else None,
                    "buckets_le_ms": dict(entry["buckets"]),
                    "overflow_gt_max_bucket": entry["overflow"],
                }
            return {
                "counters": dict(sorted(self._counters.items())),
                "latency_ms": latency,
                "labels": {
                    "route": "bounded request route template",
                    "status_class": "1xx..5xx",
                    "excluded": ["item_id", "user_id", "request_id", "url"],
                    "note": "high-cardinality identifiers are deliberately not metric labels",
                },
            }


class Observability:
    """Combined logger + metrics sink used by the service core and adapter."""

    def __init__(self, *, log_path: str | None = None, echo: bool = False) -> None:
        self.metrics = Metrics()
        self._log_path = log_path
        self._echo = echo
        self._lock = threading.Lock()

    # -- request correlation ------------------------------------------------
    @staticmethod
    def new_request_id() -> str:
        return uuid.uuid4().hex[:16]

    # -- structured logging -------------------------------------------------
    def log(self, event: str, *, request_id: str | None = None, level: str = "info", **fields) -> dict:
        record = {
            "ts": round(time.time(), 6),
            "level": level,
            "event": event,
            "request_id": request_id,
        }
        record.update(sanitize_fields(fields))
        try:
            line = json.dumps(record, sort_keys=True, ensure_ascii=False)
        except (TypeError, ValueError):
            line = json.dumps({"ts": record["ts"], "event": event, "log_error": "unserializable"})
        with self._lock:
            if self._log_path:
                try:
                    parent = os.path.dirname(os.path.abspath(self._log_path))
                    if parent:
                        os.makedirs(parent, exist_ok=True)
                    with open(self._log_path, "a", encoding="utf-8") as handle:
                        handle.write(line + "\n")
                except Exception:  # noqa: BLE001
                    # Telemetry must never break the request path. A bad log path
                    # (missing directory, embedded NUL, permission) is swallowed.
                    pass
            if self._echo:
                try:
                    print(line, flush=True)
                except OSError:
                    pass
        return record

    # -- convenience --------------------------------------------------------
    def observe_request(self, route: str, status: int, duration_ms: float) -> None:
        self.metrics.increment("requests_total")
        self.metrics.increment(f"status_{status // 100}xx_total")
        if status >= 500:
            self.metrics.increment("errors_total")
        self.metrics.observe_latency(route, duration_ms)

    def snapshot(self) -> dict:
        return self.metrics.snapshot()
