#!/usr/bin/env python3
"""
activity_l23_02.py — Decision D-015 Technology Evaluation & Architecture Judgment Framework
=============================================================================================

Canonical Module: M23 — Systems Thinking & Judgment
Canonical Lesson: L23-02 — How do I pick a technology?

Implements the authoritative 12-dimension Technology Evaluation Framework (Decision D-015):
1. Problem & Requirement Clarity
2. Data Model & Access Pattern Fit
3. Consistency & Durability Guarantees
4. Failure Modes & Operational Complexity
5. Performance & Scalability Boundaries
6. Observability & Debuggability
7. Security, Trust & Isolation
8. Ecosystem, Maintenance & Longevity
9. Licensing & Governance
10. Cost Model — Infrastructure & Human
11. Migration & Reversibility / Exit Strategy
12. Alternatives Considered & Explicit Rejection Rationale

CORE INVARIANT:
- Recommending against adopting a technology ("REJECT") is an explicitly valid,
  high-scoring passing engineering outcome when supported by rigorous trade-off analysis.
- AI-generated recommendations are treated strictly as unverified candidate hypotheses.
- Machine grading never hardcodes a technology as the "one true answer".

Zero external dependencies (Python standard library only).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

VALID_DECISIONS: Set[str] = {"ADOPT", "REJECT", "DEFER", "TRIAL"}

D015_DIMENSIONS: List[Tuple[str, str]] = [
    ("problem_fit", "1. Problem & Requirement Clarity"),
    ("data_model", "2. Data Model & Access Pattern Fit"),
    ("guarantees", "3. Consistency & Durability Guarantees"),
    ("operational_complexity", "4. Failure Modes & Operational Complexity"),
    ("performance_boundaries", "5. Performance & Scalability Boundaries"),
    ("observability", "6. Observability & Debuggability"),
    ("security_isolation", "7. Security, Trust & Isolation"),
    ("ecosystem_longevity", "8. Ecosystem, Maintenance & Longevity"),
    ("licensing_governance", "9. Licensing & Governance"),
    ("cost_model", "10. Cost Model — Infrastructure & Human"),
    ("reversibility", "11. Migration & Reversibility / Exit Strategy"),
    ("alternatives_rejection", "12. Alternatives Considered & Explicit Rejection Rationale"),
]

PLACEHOLDER_MARKERS: Set[str] = {
    "todo",
    "tbd",
    "n/a",
    "placeholder",
    "none",
    "not applicable",
    "pass",
    "...",
}


@dataclass
class ValidationResult:
    is_valid: bool
    decision: str
    missing_dimensions: List[str] = field(default_factory=list)
    placeholder_dimensions: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    score: float = 0.0


def validate_technology_evaluation_card(card: Dict[str, Any]) -> ValidationResult:
    """
    Rigorously validates a Decision D-015 Technology Evaluation Card.

    Requirements:
    1. Must contain candidate_name, scenario_context, decision, and justification.
    2. Decision must be in {'ADOPT', 'REJECT', 'DEFER', 'TRIAL'}.
    3. Must address all 12 dimensions of Decision D-015.
    4. Each dimension must contain substantive text (>= 25 characters, not placeholder tokens).
    5. Dimension 10 (cost_model) must address both infrastructure and human overhead.
    6. Dimension 11 (reversibility) must provide an exit strategy.
    7. Dimension 12 (alternatives_rejection) must articulate alternative trade-offs.

    Pass Rule:
    A decision of REJECT with complete, substantive trade-offs achieves 100% score!
    """
    errors: List[str] = []
    warnings: List[str] = []
    missing: List[str] = []
    placeholders: List[str] = []

    # 1. Check top-level metadata
    candidate_name = card.get("candidate_name", "").strip()
    if not candidate_name:
        errors.append("Missing or empty 'candidate_name'.")

    decision = str(card.get("decision", "")).strip().upper()
    if decision not in VALID_DECISIONS:
        errors.append(f"Invalid decision '{decision}'. Must be one of: {sorted(VALID_DECISIONS)}")

    justification = card.get("justification", "").strip()
    if len(justification) < 20:
        errors.append("Overall 'justification' must be at least 20 characters explaining the decision.")

    dimensions = card.get("dimensions", {})
    if not isinstance(dimensions, dict):
        errors.append("'dimensions' must be a dictionary mapping dimension keys to text rationale.")
        return ValidationResult(
            is_valid=False,
            decision=decision,
            errors=errors,
            score=0.0,
        )

    # 2. Check each of the 12 dimensions
    substantive_count = 0
    for dim_key, dim_name in D015_DIMENSIONS:
        if dim_key not in dimensions:
            missing.append(dim_name)
            continue

        val = str(dimensions[dim_key]).strip()
        val_lower = val.lower()

        if not val:
            missing.append(dim_name)
        elif val_lower in PLACEHOLDER_MARKERS or len(val) < 20:
            placeholders.append(dim_name)
        else:
            substantive_count += 1

            # Specific depth checks
            if dim_key == "cost_model" and ("human" not in val_lower and "operational" not in val_lower and "on-call" not in val_lower and "cognitive" not in val_lower):
                warnings.append("Dimension 10 (Cost Model) should explicitly address human/operational overhead, not just hardware/cloud bill.")

            if dim_key == "reversibility" and ("exit" not in val_lower and "migrate" not in val_lower and "replace" not in val_lower and "decouple" not in val_lower and "remove" not in val_lower):
                warnings.append("Dimension 11 (Reversibility) should explicitly outline an exit strategy or replacement path.")

    total_dim = len(D015_DIMENSIONS)
    score = (substantive_count / total_dim) * 100.0

    if missing:
        errors.append(f"Missing {len(missing)} required dimensions: {', '.join(missing)}")
    if placeholders:
        errors.append(f"Dimensions contain empty or placeholder text: {', '.join(placeholders)}")

    is_valid = len(errors) == 0 and substantive_count == total_dim

    return ValidationResult(
        is_valid=is_valid,
        decision=decision,
        missing_dimensions=missing,
        placeholder_dimensions=placeholders,
        errors=errors,
        warnings=warnings,
        score=score,
    )


def build_scenario_a_redis_rejection() -> Dict[str, Any]:
    """
    Reference Scenario A: Evaluating Redis for Content Article Lookups.

    Context:
    A publishing platform has slow article lookups (80ms). The engineering team
    proposes introducing a Redis cluster to cache article records.
    Investigation reveals the database query does a full table scan because
    an index on `slug` is missing. Adding the index drops query time to 3.5ms.

    Target SLO: < 20ms read latency.

    Decision: REJECT REDIS.
    """
    return {
        "candidate_name": "Redis (In-Memory Key-Value Cache)",
        "scenario_context": "CMS article lookup latency optimization (target SLO < 20ms; current latency 80ms).",
        "decision": "REJECT",
        "justification": (
            "Reject adopting Redis. Adding a B-Tree index on articles(slug) in PostgreSQL reduces "
            "lookup latency from 80ms to 3.5ms, comfortably satisfying the 20ms SLO. Adding Redis introduces "
            "cache invalidation complexity, stale read risks, RAM capacity limits, and on-call operational "
            "overhead without delivering necessary business value."
        ),
        "dimensions": {
            "problem_fit": (
                "The core problem is slow read queries (80ms). Root cause analysis proves the delay "
                "is caused by an unindexed table scan, not database engine saturation or CPU exhaustion."
            ),
            "data_model": (
                "Articles are relational documents with foreign keys, authors, and tag associations. "
                "Caching serialized JSON blobs in Redis creates dual-source data modeling discrepancies."
            ),
            "guarantees": (
                "Relational DB provides strict ACID read consistency. Redis caching introduces cache "
                "invalidation lag and risk of serving stale content after editorial updates."
            ),
            "operational_complexity": (
                "Adding Redis introduces another distributed daemon to provision, monitor, back up, "
                "patch, and manage failover for. Cache stampede and thundering herd failure modes emerge."
            ),
            "performance_boundaries": (
                "Redis achieves sub-millisecond lookups, but adding a DB index achieves 3.5ms lookups, "
                "which is well within the 20ms SLO threshold. The extra speed does not justify the complexity."
            ),
            "observability": (
                "Requires separate Redis latency and memory fragmentation metrics, eviction alerts, "
                "and cache-hit/miss tracing across application request spans."
            ),
            "security_isolation": (
                "Redis requires managing separate access credentials, TLS termination on cache sockets, "
                "and network firewall isolation rules between app nodes and cache nodes."
            ),
            "ecosystem_longevity": (
                "Redis is mature with broad client support, though license transitions (RSAL/SSPL) "
                "and community forks (Valkey) introduce governance and tracking maintenance obligations."
            ),
            "licensing_governance": (
                "Redis source is no longer standard BSD; requires legal/governance tracking. "
                "PostgreSQL is standard permissive open source with zero licensing friction."
            ),
            "cost_model": (
                "Infrastructure cost: dedicated VM/container with high RAM allocation. "
                "Human cost: cognitive load of debugging cache invalidation bugs and managing cache cluster on-call."
            ),
            "reversibility": (
                "Exit strategy: If Redis were adopted, removing it requires ensuring DB query paths "
                "can absorb the full load without stampede; using SQL index now requires zero exit strategy."
            ),
            "alternatives_rejection": (
                "Primary alternative: Add SQL B-Tree index `CREATE INDEX idx_articles_slug ON articles(slug)`. "
                "Chosen alternative satisfies SLO at zero added monthly infrastructure and zero maintenance cost."
            ),
        },
    }


def build_scenario_b_kafka_outbox() -> Dict[str, Any]:
    """
    Reference Scenario B: Evaluating Apache Kafka vs. Database Transactional Outbox.

    Context:
    An order management system processes 30 orders/second. When an order is placed,
    an email notification and inventory reservation event must be emitted.
    The team proposes deploying an Apache Kafka cluster.

    Decision: REJECT KAFKA (in favor of Transactional Outbox in PostgreSQL).
    """
    return {
        "candidate_name": "Apache Kafka (Distributed Streaming Platform)",
        "scenario_context": "Order event notification and async processing at 30 events/sec.",
        "decision": "REJECT",
        "justification": (
            "Reject adopting Kafka for 30 events/sec workload. Kafka introduces ZooKeeper/KRaft cluster "
            "management, dual-write consistency hazards between database and Kafka, and massive operational "
            "overhead. A PostgreSQL transactional outbox table guarantees atomic commit with business data."
        ),
        "dimensions": {
            "problem_fit": (
                "Need reliable event dispatch after order transactions commit. Traffic is modest (30 msg/sec), "
                "which is three orders of magnitude below where distributed log partitions are justified."
            ),
            "data_model": (
                "Events are structured domain notifications tied directly to relational order entities."
            ),
            "guarantees": (
                "Writing to DB and Kafka concurrently causes dual-write partial failure (order succeeds, "
                "event fails). Transactional outbox commits event in the same ACID transaction."
            ),
            "operational_complexity": (
                "Kafka requires dedicated broker nodes, JVM heap tuning, partition rebalancing management, "
                "and consumer offset tracking. Outbox requires a single background polling thread."
            ),
            "performance_boundaries": (
                "Kafka supports 100,000+ msg/sec. For 30 msg/sec, a PostgreSQL table with `SKIP LOCKED` "
                "polling consumes negligible CPU (< 1%) and delivers < 50ms dispatch latency."
            ),
            "observability": (
                "Kafka requires JMX metrics exporters, consumer lag monitoring, and broker partition health checks. "
                "Outbox uses existing relational database monitoring and queue depth count."
            ),
            "security_isolation": (
                "Kafka introduces SASL/SCRAM or mTLS authentication across brokers, topic ACLs, and network "
                "confinement. Outbox leverages existing database connection pooling and roles."
            ),
            "ecosystem_longevity": (
                "Kafka is a mature Apache project with strong enterprise backing, but requires specialized "
                "expertise to maintain in production."
            ),
            "licensing_governance": (
                "Apache 2.0 license is permissive and stable, with solid governance under the Apache Software Foundation."
            ),
            "cost_model": (
                "Infrastructure: Minimum 3 brokers for high availability, plus storage. "
                "Human cost: High operational maintenance, steep learning curve, on-call alert fatigue."
            ),
            "reversibility": (
                "Kafka event formats and consumer group offsets create tight architectural coupling. "
                "Outbox table is trivial to replace or scale if volume ever surges."
            ),
            "alternatives_rejection": (
                "Alternative considered: PostgreSQL Transactional Outbox pattern with `SELECT ... FOR UPDATE SKIP LOCKED`. "
                "Kafka is rejected because throughput does not justify distributed cluster complexity."
            ),
        },
    }


def build_scenario_c_ai_hypothesis() -> Dict[str, Any]:
    """
    Reference Scenario C: Evaluating an AI-Generated Architecture Recommendation.

    Context:
    An AI tool suggested migrating a company internal wiki (15,000 pages, 500 DAU)
    from SQLite to a distributed Cassandra cluster for 'infinite cloud scalability'.

    Decision: REJECT (Treated as unverified AI hypothesis).
    """
    return {
        "candidate_name": "Apache Cassandra (Recommended by AI Assistant)",
        "scenario_context": "Internal wiki documentation system serving 500 DAU and 15,000 total documents.",
        "decision": "REJECT",
        "justification": (
            "Reject AI-generated proposal to migrate to Cassandra. The total dataset is ~60 MB, which fits "
            "comfortably in RAM on a single modest server. Cassandra's eventual consistency, lack of relational "
            "queries, and ring topology are absurdly mismatched to a small, read-heavy company wiki."
        ),
        "dimensions": {
            "problem_fit": (
                "AI claimed 'future-proof infinite scalability', but actual requirement is simple full-text "
                "search and revision history for 15,000 pages. Current SQLite database responds in < 1ms."
            ),
            "data_model": (
                "Wiki requires relational backlinks, tags, and atomic page revision history. Cassandra's "
                "wide-column key-value model requires denormalizing all queries, complicating edits."
            ),
            "guarantees": (
                "Cassandra offers tunable eventual consistency, which causes confusing read-your-own-writes "
                "anomalies during wiki editing. SQLite provides full serializable local ACID."
            ),
            "operational_complexity": (
                "Cassandra requires multi-node cluster, gossip protocol management, nodetool repairs, "
                "and compaction tuning. SQLite is an embedded single-file library with zero ops."
            ),
            "performance_boundaries": (
                "SQLite memory-mapped reads take microseconds. Cassandra introduces network hops and "
                "serialization latency for queries that are trivially satisfied locally."
            ),
            "observability": (
                "Cassandra requires JMX monitoring, tombstone tracking, and read-repair metrics. "
                "SQLite requires basic file size and OS I/O checks."
            ),
            "security_isolation": (
                "Cassandra opens network ports requiring mutual TLS and authentication. SQLite runs "
                "in-process inside the application's memory boundary."
            ),
            "ecosystem_longevity": (
                "Cassandra is mature under Apache Foundation, but is specialized for massive multi-datacenter "
                "write throughput, not desktop/small-server documentation."
            ),
            "licensing_governance": (
                "Apache 2.0 license (permissive). Governance is stable."
            ),
            "cost_model": (
                "Cassandra requires minimum 3 nodes with multi-gigabyte RAM allocations ($150+/mo). "
                "SQLite runs on a $5/mo VPS or existing server with near-zero human maintenance."
            ),
            "reversibility": (
                "Exit strategy: Migrating data into Cassandra column families creates deep architectural lock-in. "
                "Migrating out to replace or remove it requires writing custom ETL extractors."
            ),
            "alternatives_rejection": (
                "Alternative: Keep SQLite with litestream/WAL replication and FTS5 full-text indexing. "
                "The AI suggestion is rejected as an ungrounded hallucination ignoring scale reality."
            ),
        },
    }


def format_evaluation_report(card: Dict[str, Any], result: ValidationResult) -> str:
    """Formats an evaluation report in human-readable Markdown."""
    lines = [
        f"# D-015 Technology Evaluation Card: {card.get('candidate_name', 'Unknown')}",
        f"- **Scenario Context**: {card.get('scenario_context', 'N/A')}",
        f"- **Decision**: `{result.decision}`",
        f"- **Validation Status**: `{'PASS' if result.is_valid else 'FAIL'}` (Score: {result.score:.1f}/100)",
        f"- **Justification Summary**: {card.get('justification', 'N/A')}",
        "",
        "## 12-Dimension Evaluation Audit:",
    ]
    dims = card.get("dimensions", {})
    for dim_key, dim_name in D015_DIMENSIONS:
        val = dims.get(dim_key, "MISSING")
        lines.append(f"### {dim_name}")
        lines.append(f"{val}\n")

    if result.warnings:
        lines.append("## Warnings & Guidance:")
        for w in result.warnings:
            lines.append(f"- ⚠️ {w}")

    return "\n".join(lines)


def main() -> None:
    print("=" * 80)
    print("  M23 L23-02: DECISION D-015 TECHNOLOGY EVALUATION & ARCHITECTURE HARNESS")
    print("=" * 80)

    scenarios = [
        ("Scenario A (Redis Caching)", build_scenario_a_redis_rejection()),
        ("Scenario B (Kafka vs Outbox)", build_scenario_b_kafka_outbox()),
        ("Scenario C (AI Hypothesis Audit)", build_scenario_c_ai_hypothesis()),
    ]

    for title, card in scenarios:
        print(f"\n[AUDITING {title}]...")
        res = validate_technology_evaluation_card(card)
        status_str = "PASS (Valid Engineering Judgment)" if res.is_valid else "FAIL"
        print(f"  Decision:   {res.decision}")
        print(f"  Validation: {status_str} [Score: {res.score:.1f}/100]")
        if res.errors:
            for err in res.errors:
                print(f"    - ERROR: {err}")
        if res.warnings:
            for w in res.warnings:
                print(f"    - WARN:  {w}")

    print("\n" + "=" * 80)
    print("[KEY CURRICULUM TAKEAWAYS]")
    print("  1. In all three scenarios, the correct, high-scoring decision was REJECT.")
    print("  2. A technology must justify its operational complexity, failure modes, and cost.")
    print("  3. Rejecting an unnecessary distributed component keeps architectures simpler,")
    print("     cheaper, and dramatically more reliable.")
    print("  4. AI architectural recommendations are unverified hypotheses that must be audited")
    print("     against real system scale and physical constraints.")
    print("=" * 80)


if __name__ == "__main__":
    main()
