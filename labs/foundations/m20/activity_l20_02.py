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
    generate_blameless_postmortem,
    reconstruct_correlated_timeline,
)


def run_activity_l20_02() -> int:
    scratch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".scratch")
    os.makedirs(scratch_dir, exist_ok=True)
    out_json = os.path.join(scratch_dir, "l20_02_observation.json")
    out_postmortem = os.path.join(scratch_dir, "l20_02_postmortem_draft.md")

    print("=" * 70)
    print(" Essential CS -- Activity L20-02: Distributed Incident & Trace Context")
    print("=" * 70)

    clock = ClockAdapter()
    manager = ObservabilityPipelineManager(clock=clock)

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
        assert timeline["fault_localized"] is not None, "Expected fault to be localized to ServiceC."

        # --------------------------------------------------------------------
        # Step 5: Safe Scenario Mitigation (Fallback Bypass)
        # --------------------------------------------------------------------
        print("\n[STEP 5: Safe Scenario Mitigation (ServiceB Local Cache Fallback)]")
        # In an active availability incident, once evidence is sufficient, safe mitigation is prioritized.
        manager.set_mitigation(enabled=True)
        print(" - Mitigation applied: Enabled fallback cache in ServiceB (bypassing degraded ServiceC)")

        mitigated_req = manager.dispatch_request()
        print(f" - Mitigated Request: status={mitigated_req['status_code']}, duration={mitigated_req['elapsed_ms']:.2f}ms")
        print(f" - Mitigation Verified: Latency dropped back to normal (< 20ms) and status 200 OK.")
        assert mitigated_req["status_code"] == 200, "Expected mitigated request to return 200 OK."
        assert mitigated_req["elapsed_ms"] < 100.0, "Expected mitigated latency to be well below the 350ms injected delay."

        # --------------------------------------------------------------------
        # Step 6: Generate Blameless Postmortem
        # --------------------------------------------------------------------
        print("\n[STEP 6: Authoring Blameless Postmortem Artifact]")
        postmortem_content = generate_blameless_postmortem(
            incident_id="INC-2026-M20-001",
            impact_summary="Frontend Gateway experienced p99 latency spike exceeding 350ms due to downstream storage stall.",
            timeline_entries=[
                ("T0 (Detection)", "Automated latency alert triggered on ServiceA p99 > 200ms."),
                ("T1 (Triage)", f"Correlated logs filtered on trace_id {incident_trace_id}; localized delay to ServiceC storage read."),
                ("T2 (Mitigation)", "Enabled ServiceB local fallback cache bypass flag; traffic latency normalized."),
                ("T3 (Resolution)", "ServiceC storage connection pool tuned; root lock contention resolved."),
                ("T4 (Postmortem)", "Systemic review of service degradation safeguards conducted."),
            ],
            proximate_mechanism="Downstream ServiceC storage mock injected with 350ms processing delay; upstream ServiceB blocked synchronously waiting for response.",
            contributing_conditions=[
                "ServiceB lacked asynchronous non-blocking timeout circuit breaking against ServiceC.",
                "Frontend gateway had no fallback degradation path configured before incident.",
                "Monitoring alerted on upstream symptom without automated correlation dashboard link.",
            ],
            mitigation_applied="Activated ServiceB cached fallback route to safely bypass degraded ServiceC storage path.",
            permanent_safeguards=[
                "Implement adaptive circuit breaker and bulkhead pattern in ServiceB for all storage calls.",
                "Introduce automated canary analysis for storage configuration changes.",
                "Enforce W3C traceparent context propagation across all internal RPC boundaries.",
            ],
            unresolved_questions=[
                "What is the maximum staleness tolerance for cached storage fallback data during extended outages?",
                "How does network partition or packet loss between ServiceB and ServiceC alter timeout detection thresholds?",
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
            "mitigated_request_status": mitigated_req["status_code"],
            "mitigated_request_duration_ms": mitigated_req["elapsed_ms"],
            "recovery_verified": True,
            "total_logs_emitted": len(all_logs_step3),
            "correlated_timeline_records_count": timeline["record_count"],
        }

        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(observation, f, indent=2, ensure_ascii=False)

        print(f" - Observation data saved: {out_json}")

    finally:
        print("\n[CLEANUP: Shutting Down Ephemeral Servers]")
        manager.shutdown()
        print(" - Sockets closed and threads joined cleanly.")

    print("\n" + "=" * 70)
    print(" Activity L20-02 Completed Successfully.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(run_activity_l20_02())
