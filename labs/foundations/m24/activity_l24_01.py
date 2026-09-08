#!/usr/bin/env python3
"""
activity_l24_01.py — Hands-on Activity for Lesson L24-01 (Architecture Defense)
================================================================================

Provides the runnable harness for defending a computer systems architecture:
1. Audits learner-supplied or sample 16-Trace Defense Dossier against the 12 Evidence Areas.
2. Injects randomized or selectable Changed-Constraint Challenge scenario cards:
   - SCENARIO_01_HIGH_LATENCY: Client network RTT increases by 200x (WAN conditions)
   - SCENARIO_02_100X_DATA: Working set expands 100x, exceeding available RAM
   - SCENARIO_03_MALICIOUS_CLIENT: Hostile client network attempting Slowloris connection pool exhaustion
3. Evaluates structural invariants and emits a structured verification report.

Standard Library Only (PEP 557 dataclasses, json, argparse, pathlib).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

# Import sibling defense validator
try:
    from defense_validator import validate_defense_dossier
except ImportError:
    from labs.foundations.m24.defense_validator import validate_defense_dossier


@dataclass
class ScenarioCard:
    id: str
    title: str
    original_assumption: str
    perturbed_constraint: str
    threatened_invariants: List[str]
    system_bottleneck: str
    required_adaptations: List[str]
    new_evidence_required: str


SCENARIOS: Dict[str, ScenarioCard] = {
    "SCENARIO_01_HIGH_LATENCY": ScenarioCard(
        id="SCENARIO_01_HIGH_LATENCY",
        title="Transatlantic Network Latency Shift",
        original_assumption="Clients communicate over low-latency local network (RTT < 2ms); synchronous TCP request-response.",
        perturbed_constraint="Client network latency jumps to 200ms RTT with 1% packet loss over international WAN links.",
        threatened_invariants=[
            "Request processing throughput >= 200 req/s",
            "Worker thread pool availability (pool exhausted by slow socket writes)",
        ],
        system_bottleneck="Worker thread pool saturation due to high bandwidth-delay product and blocking socket writes.",
        required_adaptations=[
            "Deploy non-blocking reverse proxy (e.g. nginx/caddy) to terminate slow client TCP and buffer responses.",
            "Enable HTTP/2 multiplexing on edge proxy to eliminate per-request connection handshakes.",
            "Tune TCP keepalive and socket send buffer sizes for high-latency connections.",
        ],
        new_evidence_required="Re-run arrival-scheduled latency benchmark through network traffic simulator (e.g. tc netem delay 200ms).",
    ),
    "SCENARIO_02_100X_DATA": ScenarioCard(
        id="SCENARIO_02_100X_DATA",
        title="100x Data Working-Set Expansion",
        original_assumption="Full database working-set (~500MB) fits entirely within host OS page cache and RAM.",
        perturbed_constraint="Total active data expands to 50GB, exceeding available 4GB system RAM by over 12x.",
        threatened_invariants=[
            "Sub-millisecond index lookup latency",
            "Single-process memory footprint <= 1GB RSS",
        ],
        system_bottleneck="Random disk I/O seek thrashing replacing in-memory B-Tree page lookups.",
        required_adaptations=[
            "Verify all query paths utilize covering indexes (M13) to avoid secondary table lookups.",
            "Partition hot recent data from cold historical archives into separate SQLite files.",
            "Configure explicit SQLite cache size limits (PRAGMA cache_size) to prevent OS paging thrash.",
        ],
        new_evidence_required="Empirical benchmark with 50GB synthetic database measuring disk read IOPS and query latencies.",
    ),
    "SCENARIO_03_MALICIOUS_CLIENT": ScenarioCard(
        id="SCENARIO_03_MALICIOUS_CLIENT",
        title="Slowloris Connection Pool Exhaustion Attack",
        original_assumption="Clients send complete HTTP requests promptly upon establishing TCP connections.",
        perturbed_constraint="Adversarial clients open 500 concurrent connections and transmit 1 byte every 4.9 seconds.",
        threatened_invariants=[
            "Service availability for legitimate users (DoS defense)",
            "Maximum concurrent connection limit compliance",
        ],
        system_bottleneck="Application worker threads held hostage by incomplete, slow-reading HTTP request headers.",
        required_adaptations=[
            "Configure strict header read timeout (e.g. 2.0s total allowed for complete header receipt).",
            "Enforce minimum throughput threshold (e.g. drop connections transferring < 100 bytes/sec).",
            "Place event-driven edge proxy in front of application to absorb slow connections.",
        ],
        new_evidence_required="Automated Slowloris attack simulation test confirming malicious connections are dropped within 2 seconds.",
    ),
}


def run_scenario_drill(scenario_id: str) -> None:
    card = SCENARIOS.get(scenario_id)
    if not card:
        print(f"Unknown scenario '{scenario_id}'. Available: {', '.join(SCENARIOS.keys())}")
        sys.exit(1)

    print("=" * 78)
    print(f"  M24 CHANGED-CONSTRAINT CHALLENGE DRILL: {card.id}")
    print("=" * 78)
    print(f"  Title:                {card.title}")
    print(f"  Original Assumption:  {card.original_assumption}")
    print(f"  Perturbed Constraint: {card.perturbed_constraint}")
    print("-" * 78)
    print("  DIAGNOSTIC ANALYSIS:")
    print(f"    - Primary Bottleneck: {card.system_bottleneck}")
    print("    - Threatened Invariants:")
    for inv in card.threatened_invariants:
        print(f"        * {inv}")
    print("    - Required Architectural Adaptations:")
    for adapt in card.required_adaptations:
        print(f"        * {adapt}")
    print(f"    - New Evidence Required: {card.new_evidence_required}")
    print("=" * 78)


def main() -> None:
    parser = argparse.ArgumentParser(description="L24-01 Architecture Defense Activity & Drill Harness")
    parser.add_argument("--dossier", help="Path to defense dossier Markdown file to audit")
    parser.add_argument("--scenario", choices=list(SCENARIOS.keys()), help="Run a Changed-Constraint challenge drill")
    parser.add_argument("--list-scenarios", action="store_true", help="List available scenario cards")
    args = parser.parse_args()

    if args.list_scenarios:
        print("Available Changed-Constraint Scenario Cards:")
        for sid, sc in SCENARIOS.items():
            print(f"  - {sid}: {sc.title}")
        return

    if args.scenario:
        run_scenario_drill(args.scenario)
        return

    # Default to auditing sample dossier if no argument provided
    dossier_path = Path(args.dossier) if args.dossier else Path(__file__).parent / "sample_dossier.md"
    if not dossier_path.exists():
        print(f"ERROR: Dossier file not found: {dossier_path}", file=sys.stderr)
        sys.exit(1)

    content = dossier_path.read_text(encoding="utf-8")
    report = validate_defense_dossier(content, str(dossier_path))

    print("=" * 78)
    print(f"  M24 L24-01 ARCHITECTURE DEFENSE AUDIT: {dossier_path.name}")
    print("=" * 78)
    print(f"  Status:               {report.status}")
    print(f"  Traces Found:         {len(report.traces_found)} / 16")
    print(f"  Evidence Areas:       {len(report.evidence_areas_found)} / 12")
    print(f"  Declared Claims:      {report.claims_count}")
    print(f"  Placeholders:         {len(report.placeholders_detected)}")
    print("-" * 78)

    if report.is_valid:
        print("  [SUCCESS] All 16 traces and 12 evidence areas are structurally complete.")
        print("  [SUCCESS] Zero unresolved placeholders detected.")
    else:
        print("  [FAILED] Structural completeness requirements not satisfied:")
        for err in report.errors:
            print(f"    - {err}")

    print("-" * 78)
    print(f"  NOTE: {report.disclaimer}")
    print("=" * 78)

    sys.exit(0 if report.is_valid else 1)


if __name__ == "__main__":
    main()
