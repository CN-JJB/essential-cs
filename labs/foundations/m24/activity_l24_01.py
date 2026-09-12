#!/usr/bin/env python3
"""
activity_l24_01.py — M24 Architecture Defense Structural Activity
=================================================================

Audits an architecture defense dossier against the 16 required trace headings
and 12-evidence-area matrix:
- By default or with `--dossier labs/foundations/m24/sample_dossier.md`, audits
  the course-owned synthetic reference dossier.
- To audit the learner's actual Mini Cloud system defense dossier, specify
  `--dossier course/evidence/foundations-m24-evidence-template.md` (or completed file).

Changed-constraint cards provide only scenario facts and learner questions. They do
not pre-fill the bottleneck, affected invariants, adaptation, or evidence conclusion.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

try:
    from defense_validator import validate_defense_dossier
except ImportError:
    from labs.foundations.m24.defense_validator import validate_defense_dossier


@dataclass(frozen=True)
class ScenarioCard:
    id: str
    title: str
    original_assumption: str
    perturbed_constraint: str
    scenario_facts: List[str]
    learner_questions: List[str]


COMMON_QUESTIONS = [
    "Which original assumption changed?",
    "Which existing invariants or evidence claims are affected, and which remain valid?",
    "What bottleneck or failure mode becomes plausible under the changed constraint?",
    "What architecture change, if any, would you consider and what trade-off would it introduce?",
    "What new measurement, test, inspection, or explicit unknown is needed before making a stronger claim?",
    "What is the exact inference limit of your proposed response?",
]

SCENARIOS: Dict[str, ScenarioCard] = {
    "SCENARIO_01_HIGH_LATENCY": ScenarioCard(
        id="SCENARIO_01_HIGH_LATENCY",
        title="Network-Latency Assumption Shift",
        original_assumption="The synthetic reference case treats same-region network latency as non-dominant.",
        perturbed_constraint="Scenario input: client RTT becomes 200 ms with 1% packet loss.",
        scenario_facts=[
            "The card does not state the learner application's concurrency model.",
            "The card does not assume a reverse proxy, HTTP/2, or a particular worker-pool design exists.",
            "200 ms and 1% are challenge inputs only, not course-wide production targets.",
        ],
        learner_questions=COMMON_QUESTIONS,
    ),
    "SCENARIO_02_100X_DATA": ScenarioCard(
        id="SCENARIO_02_100X_DATA",
        title="100x Working-Set Growth",
        original_assumption="The synthetic reference case assumes the active working set fits comfortably in available memory.",
        perturbed_constraint="Scenario input: active data volume becomes 100 times the baseline.",
        scenario_facts=[
            "No storage engine, cache hit rate, or I/O latency result is pre-supplied.",
            "The learner must use the actual system's data model and prior M23 estimates.",
            "100x is a challenge multiplier, not a universal scaling threshold.",
        ],
        learner_questions=COMMON_QUESTIONS,
    ),
    "SCENARIO_03_MALICIOUS_CLIENT": ScenarioCard(
        id="SCENARIO_03_MALICIOUS_CLIENT",
        title="Client-Trust Assumption Shift",
        original_assumption="The synthetic reference case assumes clients complete requests without intentionally holding resources open.",
        perturbed_constraint="Scenario input: some clients become adversarial and keep many requests incomplete for long periods.",
        scenario_facts=[
            "No attack tool is run and no public target is contacted.",
            "The learner must identify the actual server resource that could be exhausted, if any.",
            "Timeout, proxy, backpressure, and admission-control ideas are candidates only, not preselected answers.",
        ],
        learner_questions=COMMON_QUESTIONS,
    ),
}


def run_scenario_drill(scenario_id: str) -> None:
    card = SCENARIOS.get(scenario_id)
    if card is None:
        print(f"Unknown scenario: {scenario_id}", file=sys.stderr)
        sys.exit(1)

    print("=" * 78)
    print(f"  M24 CHANGED-CONSTRAINT CHALLENGE: {card.id}")
    print("=" * 78)
    print(f"  Title:               {card.title}")
    print(f"  Original Assumption: {card.original_assumption}")
    print(f"  Changed Constraint:  {card.perturbed_constraint}")
    print("-" * 78)
    print("  BOUNDED SCENARIO FACTS:")
    for fact in card.scenario_facts:
        print(f"    - {fact}")
    print("-" * 78)
    print("  LEARNER / REVIEWER QUESTIONS:")
    for idx, question in enumerate(card.learner_questions, start=1):
        print(f"    {idx}. {question}")
    print("-" * 78)
    print("  NOTE: No adaptation or PASS is machine-selected. Record the learner reasoning in the evidence template.")
    print("=" * 78)


def main() -> None:
    parser = argparse.ArgumentParser(description="L24-01 Architecture Defense structural activity")
    parser.add_argument(
        "--dossier",
        help="Path to defense dossier Markdown (default: labs/foundations/m24/sample_dossier.md; pass course/evidence/foundations-m24-evidence-template.md for learner Mini Cloud dossier)",
    )
    parser.add_argument("--scenario", choices=list(SCENARIOS), help="Run one changed-constraint prompt")
    parser.add_argument("--list-scenarios", action="store_true")
    args = parser.parse_args()

    if args.list_scenarios:
        for sid, card in SCENARIOS.items():
            print(f"{sid}: {card.title}")
        return
    if args.scenario:
        run_scenario_drill(args.scenario)
        return

    dossier_path = Path(args.dossier) if args.dossier else Path(__file__).parent / "sample_dossier.md"
    if not dossier_path.exists():
        print(f"ERROR: Dossier file not found: {dossier_path}", file=sys.stderr)
        sys.exit(1)

    report = validate_defense_dossier(
        dossier_path.read_text(encoding="utf-8"),
        str(dossier_path),
    )
    print("=" * 78)
    print(f"  M24 DEFENSE STRUCTURAL AUDIT: {dossier_path.name}")
    print("=" * 78)
    print(f"  Status:          {report.status}")
    print(f"  Traces:          {len(report.traces_found)} / 16")
    print(f"  Evidence Rows:   {report.evidence_rows_valid} / 12")
    print(f"  Claims:          {report.claims_count}")
    print(f"  Unknowns Linked: {len(report.learning_plan_linked_ids)} / {len(report.explicit_unknown_ids)}")
    if report.errors:
        for err in report.errors:
            print(f"    [FAIL] {err}")
    print("-" * 78)
    print(f"  NOTE: {report.disclaimer}")
    print("=" * 78)
    sys.exit(0 if report.is_valid else 1)


if __name__ == "__main__":
    main()
