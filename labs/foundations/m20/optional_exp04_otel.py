#!/usr/bin/env python3
"""
optional_exp04_otel.py — Strictly Optional OpenTelemetry Route (LAB-OPT-04 & EXP-04)
===================================================================================

Status: STRICTLY OPTIONAL / SOURCE EXPEDITION & OPTIONAL LAB.
Authority: GitHub Issue #110 and Stage 6 Design Dossier v0.1.

Core Curriculum Invariant:
- Core M20 observability requires ZERO external packages and runs entirely on Python stdlib.
- If opentelemetry-api and opentelemetry-sdk are absent, the outcome is truthfully recorded
  as OPTIONAL BLOCKED / NOT RUN, with ZERO curriculum progression loss.
- Default SDK span timestamps use imported time_ns() (system epoch time), which is NOT
  time.monotonic_ns(). EXP-04 is NOT evidence for the Core monotonic-duration invariant!

Pinned Release Route:
- Repository: open-telemetry/opentelemetry-python
- Git Release Tag: v1.44.0 (Checked date: 2026-07-16 / rechecked 2026-09-05)
- License: Apache-2.0
- API Boundary: opentelemetry-api/src/opentelemetry/trace/span.py
- SDK Boundary: opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py
"""

import sys
from typing import Any, Dict


EXP_04_SOURCE_CARD = {
    "expedition": "EXP-04",
    "status": "STRICTLY OPTIONAL / SOURCE EXPEDITION",
    "repository": "open-telemetry/opentelemetry-python",
    "git_release_tag": "v1.44.0",
    "release_date": "2026-07-16",
    "recheck_date": "2026-09-06",
    "license": "Apache-2.0",
    "canonical_paths": {
        "api_path": "opentelemetry-api/src/opentelemetry/trace/span.py",
        "sdk_path": "opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py",
    },
    "pinned_source_inspection": {
        "api_focus": (
            "Span abstract base class and SpanContext structure. Inspects how trace_id (128-bit int) "
            "and span_id (64-bit int) are immutable context components."
        ),
        "sdk_focus": (
            "In opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py: "
            "Lines show imported 'from time import time_ns'. "
            "Inside _Span.__init__ and _Span.end: "
            "'self._start_time = start_time if start_time is not None else time_ns()' "
            "'self._end_time = end_time if end_time is not None else time_ns()' "
            "Followed by invoking self._span_processor.on_end(self)."
        ),
        "critical_clock_distinction": (
            "IMPORTANT: Pinned OpenTelemetry SDK default timestamps use system epoch time_ns(), "
            "NOT time.monotonic_ns(). Therefore, OpenTelemetry span start/end timestamps are epoch-aligned "
            "for cross-machine correlation, and are NOT evidence for the Core monotonic-duration rule. "
            "Core elapsed durations must continue to use monotonic timers."
        ),
        "confirmed_claim": (
            "The OpenTelemetry Python SDK v1.44.0 implements a modular SpanProcessor pipeline, "
            "dispatching completed _Span records to on_end() upon calling span.end()."
        ),
        "conditional_claim": (
            "Span durations derived from start_time and end_time represent system epoch wall timestamps; "
            "they are subject to NTP adjustments or system clock steps if those occur during span execution."
        ),
    },
}


def run_exp04_source_reading() -> Dict[str, Any]:
    """Prints and returns the EXP-04 source expedition reading card."""
    print("=" * 70)
    print(" Essential CS -- EXP-04: OpenTelemetry Python Span Lifecycle (v1.44.0)")
    print("=" * 70)
    print(f" Repository:  {EXP_04_SOURCE_CARD['repository']}")
    print(f" Tag:         {EXP_04_SOURCE_CARD['git_release_tag']} ({EXP_04_SOURCE_CARD['release_date']})")
    print(f" API Path:    {EXP_04_SOURCE_CARD['canonical_paths']['api_path']}")
    print(f" SDK Path:    {EXP_04_SOURCE_CARD['canonical_paths']['sdk_path']}")
    print("-" * 70)
    print(" [Inspection Notes]:")
    print(f"   * API: {EXP_04_SOURCE_CARD['pinned_source_inspection']['api_focus']}")
    print(f"   * SDK: {EXP_04_SOURCE_CARD['pinned_source_inspection']['sdk_focus']}")
    print(f"   * Clock Distinction: {EXP_04_SOURCE_CARD['pinned_source_inspection']['critical_clock_distinction']}")
    print(f"   * Confirmed Claim:   {EXP_04_SOURCE_CARD['pinned_source_inspection']['confirmed_claim']}")
    print(f"   * Conditional Claim: {EXP_04_SOURCE_CARD['pinned_source_inspection']['conditional_claim']}")
    print("=" * 70)
    return EXP_04_SOURCE_CARD


def run_optional_lab_opt_04() -> int:
    """
    Executes LAB-OPT-04 if OpenTelemetry packages are installed.
    If absent, reports truthfully and exits 0 with zero Core curriculum loss.
    """
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
    except ImportError:
        print("\n[LAB-OPT-04 DISPOSITION: OPTIONAL BLOCKED / NOT RUN]")
        print(" OpenTelemetry SDK packages (opentelemetry-api, opentelemetry-sdk) are not installed.")
        print(" Core zero-SaaS curriculum is 100% complete using standard library structured logging.")
        print(" To run this optional comparison: pip install opentelemetry-api==1.44.0 opentelemetry-sdk==1.44.0")
        return 0

    print("\n[LAB-OPT-04: Running Local OpenTelemetry Tracer Comparison]")
    provider = TracerProvider()
    processor = SimpleSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("essential-cs-m20-optional")

    # Simple two-hop trace demonstration
    with tracer.start_as_current_span("parent_gateway_span") as parent:
        parent.set_attribute("http.method", "GET")
        parent.set_attribute("http.target", "/order")
        with tracer.start_as_current_span("child_storage_span") as child:
            child.set_attribute("db.system", "mock_storage")
            child.set_attribute("db.statement", "SELECT record_101")

    print("\n[LAB-OPT-04: Observed Span Parent-Child Linkage in Emitted JSON Above]")
    return 0


def main() -> int:
    run_exp04_source_reading()
    run_optional_lab_opt_04()
    return 0


if __name__ == "__main__":
    sys.exit(main())
