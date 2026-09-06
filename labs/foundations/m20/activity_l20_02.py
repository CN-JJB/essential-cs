#!/usr/bin/env python3
"""
activity_l20_02.py — Lesson L20-02 Hands-On Activity
====================================================

Lesson: L20-02 — "How do I debug a production incident?"
Focus:
1. Distributed Trace Context propagation (W3C Level 1 version-00 traceparent) across ServiceA -> ServiceB -> ServiceC.
2. Structured JSON logging with monotonic elapsed durations and correlation identifiers.
3. Uncorrelated noise inspection vs. correlated trace filtering.
4. Controlled incident injection (ServiceC delay fault).
5. Cross-service timeline reconstruction and symptom localization.
6. Safe scenario mitigation (ServiceB fallback cache bypass) and recovery verification.
7. Blameless incident postmortem generation (systemic conditions and defensive safeguards).

Outputs:
- labs/foundations/m20/.scratch/l20_02_observation.json
- labs/foundations/m20/.scratch/l20_02_postmortem_draft.md
"""

import json
import os
import sys

from s6_m20_observability_pipeline import (
    ClockAdapter,
    ObservabilityPipelineManager,
    OwnedSubprocessWatchdog,
    generate_blameless_postmortem,
    reconstruct_correlated_timeline,
)


def _run_child_worker() -> int:
    scratch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".scratch")
    os.makedirs(scratch_dir, exist_ok=True)
    out_json = os.path.join(scratch_dir, "l20_02_observation.json")
    out_postmortem = os.path.join(scratch_dir, "l20_02_postmortem_draft.md")
    jsonl_log_path = os.path.join(scratch_dir, "l20_02_events.jsonl")

    print("=" * 70)
    print(" Essential CS -- Activity L20-02: Distributed Incident & Trace Context")
    print("=" * 70)

    clock = ClockAdapter()
    manager = ObservabilityPipelineManager(clock=clock, jsonl_path=jsonl_log_path)

    try:
        # --------------------------------------------------------------------
        # Step 1: Initialize Three-Service Pipeline
        # --------------------------------------------------------------------
        print("\n[STEP 1: Starting Ephemeral Localhost Pipeline (A -> B -> C)]")
        manager.start()
        urls = manager.get_urls()
        print(f" - ServiceA (Frontend Gateway): {urls['ServiceA']}")
        print(f" - ServiceB (Business Logic):   {urls['ServiceB']}")
        print(f" - ServiceC (Storage Mock):     {urls['ServiceC']}")

        # --------------------------------------------------------------------
        # Step 2: Normal Traffic & Background Noise
        # --------------------------------------------------------------------
        print("\n[STEP 2: Normal Traffic Generation with Context Propagation]")
        # Dispatch 3 background requests to populate log volume
        for i in range(3):
            res = manager.dispatch_request()
            print(f" - Request #{i+1}: status={res['status_code']}, duration={res['elapsed_ms']:.2f}ms")

        all_logs_step2 = manager.logger.get_records()
        print(f" - Total structured log entries accumulated: {len(all_logs_step2)}")

        # --------------------------------------------------------------------
        # Step 3: Injected Failure Mode (Controlled Incident)
        # --------------------------------------------------------------------
        print("\n[STEP 3: Injecting Downstream Fault into ServiceC]")
        injected_delay = 0.35  # 350 ms
        manager.set_fault(fault_mode="DELAY", delay_s=injected_delay)
        print(f" - Fault configured: DELAY {injected_delay * 1000:.0f}ms in ServiceC")

        incident_req = manager.dispatch_request()
        incident_trace_id = incident_req["response"].get("trace_id", "unknown")
        print(f" - Incident Request: status={incident_req['status_code']}, duration={incident_req['elapsed_ms']:.2f}ms")
        print(f" - Incident Trace ID: {incident_trace_id}")

        # Add more background traffic during the degraded period
        for _ in range(2):
            manager.dispatch_request()

        all_logs_step3 = manager.logger.get_records()
        print(f" - Log pool after incident traffic: {len(all_logs_step3)} entries")

        # --------------------------------------------------------------------
        # Step 4: Compare Uncorrelated vs. Correlated Investigation
        # --------------------------------------------------------------------
        print("\n[STEP 4: Diagnostic Triage: Manual Search vs. Correlated Filtering]")
        print(" [Uncorrelated View]: Looking through all log entries without trace_id:")
        sample_uncorrelated = [f"{r['service']}: {r['event']} (status={r['status']})" for r in all_logs_step3[:5]]
        for line in sample_uncorrelated:
            print(f"   * {line}")
        print(f"   ... ({len(all_logs_step3) - 5} more entries across concurrent requests)")

        print(f"\n [Correlated View]: Filtering specifically by trace_id = '{incident_trace_id}':")
        timeline = reconstruct_correlated_timeline(all_logs_step3, incident_trace_id)
        for r in timeline["records"]:
            dur_str = f"{r['duration_ms']:.1f}ms" if r.get("duration_ms") is not None else "instant"
            print(f"   -> [{r['service']}] {r['event']} | status={r['status']} | span={r['span_id']} | parent={r['parent_id']} | dur={dur_str}")

        print(f"\n - Hop Durations:     {timeline['service_durations_ms']}")
        print(f" - Localized Root:    {timeline['fault_localized']}")
        print(f" - Diagnostic Detail: {timeline['diagnostic_inference']}")

        # Explicit validation (no assert)
        if timeline.get("fault_localized") is None:
            raise RuntimeError("Fault localization failed: expected fault localized to ServiceC.")

        # --------------------------------------------------------------------
        # Step 5: Safe Scenario Mitigation (Fallback Bypass)
        # --------------------------------------------------------------------
        print("\n[STEP 5: Safe Scenario Mitigation (ServiceB Local Cache Fallback)]")
        # In an active availability incident, once evidence is sufficient, safe mitigation is prioritized.
        manager.set_mitigation(enabled=True)
        print(" - Mitigation applied: Enabled fallback cache in ServiceB (bypassing degraded ServiceC)")

        mitigated_req = manager.dispatch_request()
        print(f" - Mitigated Request: status={mitigated_req['status_code']}, duration={mitigated_req['elapsed_ms']:.2f}ms")
        print(f" - Mitigation Verified: Latency dropped back to baseline and status 200 OK.")

        # Explicit validation (no assert, relative latency check)
        if mitigated_req["status_code"] != 200:
            raise RuntimeError(f"Mitigated request failed: expected status 200, got {mitigated_req['status_code']}")
        if mitigated_req["elapsed_ms"] >= incident_req["elapsed_ms"]:
            raise RuntimeError(
                f"Mitigation latency anomaly: mitigated duration ({mitigated_req['elapsed_ms']:.1f}ms) "
                f"was not less than degraded incident duration ({incident_req['elapsed_ms']:.1f}ms)."
            )

        recovery_status = "PASS"
        recovery_evidence = (
            f"Mitigated request returned HTTP {mitigated_req['status_code']} in {mitigated_req['elapsed_ms']:.2f}ms "
            f"(relative reduction from degraded latency {incident_req['elapsed_ms']:.2f}ms). "
            "ServiceB served request from local cache, bypassing degraded ServiceC storage mock."
        )

        # --------------------------------------------------------------------
        # Step 6: Generate Blameless Postmortem (Evidence-Driven)
        # --------------------------------------------------------------------
        print("\n[STEP 6: Authoring Blameless Postmortem Artifact (Evidence-Driven)]")
        postmortem_content = generate_blameless_postmortem(
            incident_id="INC-2026-M20-001",
            impact_summary=f"Frontend Gateway experienced elevated request latency ({incident_req['elapsed_ms']:.1f}ms) due to downstream storage mock delay.",
            timeline_entries=[
                ("T0 (Fault Injection)", f"Fixture injected controlled fault DELAY {injected_delay * 1000:.0f}ms into ServiceC; ServiceA request duration elevated to {incident_req['elapsed_ms']:.1f}ms."),
                ("T1 (Triage via Correlation)", f"Correlated structured logs filtered on trace_id '{incident_trace_id}'; relative hop duration localized to ServiceC storage mock ({timeline['service_durations_ms'].get('ServiceC', 0.0):.1f}ms)."),
                ("T2 (Safe Mitigation Applied)", f"Enabled ServiceB fallback cache bypass; verified request duration recovered to {mitigated_req['elapsed_ms']:.1f}ms (HTTP {mitigated_req['status_code']})."),
                ("T3 (Resolution Status)", "NOT PERFORMED / PROPOSED FOLLOW-UP: Underlying storage mock delay remains active in fixture; code/infrastructure defect resolution was not executed in this scenario."),
                ("T4 (Defensive Safeguards)", "Systemic review of service degradation safeguards, non-blocking timeout circuit breakers, and canary checks proposed."),
            ],
            proximate_mechanism=f"Downstream ServiceC storage mock injected with {injected_delay * 1000:.0f}ms delay; upstream ServiceB synchronously awaited storage response.",
            contributing_conditions=[
                "ServiceB lacked asynchronous non-blocking timeout circuit breaking against ServiceC.",
                "Frontend gateway had no fallback degradation path configured before incident.",
                "Telemetry pipeline initially required manual trace correlation rather than automated dependency bottleneck detection.",
            ],
            mitigation_applied="Activated ServiceB cached fallback route to safely bypass degraded ServiceC storage path.",
            recovery_status=recovery_status,
            recovery_evidence=recovery_evidence,
            resolution_status="NOT PERFORMED / PROPOSED FOLLOW-UP",
            resolution_plan="Underlying storage mock delay remains active in fixture; in production, storage concurrency limits and query lock contention would be resolved.",
            permanent_safeguards=[
                "Implement non-blocking timeout circuit breaker in ServiceB for all storage calls",
                "Introduce automated canary verification for storage configuration changes",
                "Enforce W3C traceparent context propagation across all internal RPC boundaries",
            ],
            unresolved_questions=[
                "What is the maximum staleness tolerance for cached storage fallback data during extended outages?",
                "How do network packet loss and partial partitions alter timeout detection thresholds?",
            ],
        )

        with open(out_postmortem, "w", encoding="utf-8") as f:
            f.write(postmortem_content)
        print(f" - Blameless Postmortem saved: {out_postmortem}")

        # --------------------------------------------------------------------
        # Step 7: Record Observation Data
        # --------------------------------------------------------------------
        observation = {
            "activity": "L20-02",
            "ephemeral_ports": urls,
            "incident_trace_id": incident_trace_id,
            "incident_request_status": incident_req["status_code"],
            "incident_request_duration_ms": incident_req["elapsed_ms"],
            "localized_fault": timeline["fault_localized"],
            "diagnostic_inference": timeline["diagnostic_inference"],
            "mitigated_request_status": mitigated_req["status_code"],
            "mitigated_request_duration_ms": mitigated_req["elapsed_ms"],
            "recovery_status": recovery_status,
            "recovery_evidence": recovery_evidence,
            "total_logs_emitted": len(all_logs_step3),
            "correlated_timeline_records_count": timeline["record_count"],
            "jsonl_events_path": jsonl_log_path,
        }

        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(observation, f, indent=2, ensure_ascii=False)

        print(f" - Observation data saved: {out_json}")

    finally:
        print("\n[CLEANUP: Shutting Down Ephemeral Servers]")
        try:
            manager.shutdown()
            print(" - Sockets closed and threads joined cleanly.")
        except Exception as exc:
            err_msg = str(exc)
            print(f"CLEANUP_FAILURE: {err_msg}", file=sys.stderr)
            sys.exit(101)

    print("\n" + "=" * 70)
    print(" Activity L20-02 Child Worker Completed Successfully.")
    print("=" * 70)
    return 0


def run_activity_l20_02(watchdog_timeout_s: float = 30.0) -> int:
    """
    Parent runner supervising Activity L20-02 child execution under watchdog.
    """
    if "--child-worker" in sys.argv:
        return _run_child_worker()

    print("=" * 70)
    print(" Essential CS -- Activity L20-02: Distributed Incident & Trace Context")
    print(" [Parent Runner: Supervising Child Process under Watchdog]")
    print("=" * 70)

    watchdog = OwnedSubprocessWatchdog(timeout_s=watchdog_timeout_s)
    cmd = [sys.executable, "-u", os.path.abspath(__file__), "--child-worker"]

    result = watchdog.run(cmd)

    if result.get("stdout"):
        print(result["stdout"], end="")

    if result["status"] == "PASS":
        print("\n" + "=" * 70)
        print(" Activity L20-02 Completed Successfully under Owned Subprocess Watchdog.")
        print(f" - Child PID:    {result['child_pid']}")
        print(f" - Child Reaped: {result['reaped']}")
        print("=" * 70)
        return 0
    elif result["status"] == "TIMEOUT":
        print(f"\n[WATCHDOG TIMEOUT ERROR]: Child process timed out after {watchdog_timeout_s}s.", file=sys.stderr)
        print(f" - Terminated and reaped owned child PID {result['child_pid']}.", file=sys.stderr)
        return 1
    elif result["status"] == "CLEANUP_FAILURE":
        print(f"\n[CLEANUP FAILURE]: {result['cleanup_failure']}", file=sys.stderr)
        return 1
    else:
        if result.get("stderr"):
            print(result["stderr"], file=sys.stderr)
        print(f"\n[EXECUTION ERROR]: Child process exited with status {result['status']}.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run_activity_l20_02())
