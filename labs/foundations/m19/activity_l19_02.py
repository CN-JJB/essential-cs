#!/usr/bin/env python3
"""
activity_l19_02.py
Essential CS: Stage 6 Module 19 (M19) Activity L19-02.

Hands-on activity: Cloud Topology, Availability Math, and Failure Domains.
Evaluates availability calculations, parallel redundancy math, physical latency floors,
and provider SLA contractual limits.
"""

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

CURRENT_DIR = Path(__file__).resolve().parent

MINUTES_PER_YEAR = 365 * 24 * 60  # 525,600 minutes


def calculate_annual_downtime(availability_pct: float) -> float:
    """
    Calculates allowable downtime in minutes per year for a given availability percentage.
    Example: 99.9% -> 525.6 minutes.
    """
    if not (0.0 <= availability_pct <= 100.0):
        raise ValueError(f"Availability percentage must be between 0.0 and 100.0, got {availability_pct}")
    downtime_fraction = (100.0 - availability_pct) / 100.0
    return round(MINUTES_PER_YEAR * downtime_fraction, 4)


def calculate_parallel_availability(a1: float, a2: float) -> float:
    """
    Calculates theoretical parallel redundancy availability:
    A = 1 - (1 - a1) * (1 - a2)
    NOTE: Holds ONLY under the assumption of mutually independent failures!
    """
    if not (0.0 <= a1 <= 1.0) or not (0.0 <= a2 <= 1.0):
        raise ValueError("Availability probabilities a1 and a2 must be in range [0.0, 1.0]")
    return round(1.0 - (1.0 - a1) * (1.0 - a2), 8)


def calculate_serial_availability(components: List[float]) -> float:
    """
    Calculates series system availability:
    A = prod(c_i)
    In a series dependency chain, overall availability is strictly less than
    the least available component.
    """
    total = 1.0
    for c in components:
        if not (0.0 <= c <= 1.0):
            raise ValueError(f"Component availability must be in range [0.0, 1.0], got {c}")
        total *= c
    return round(total, 8)


def calculate_fiber_propagation_floor(distance_km: float) -> Dict[str, Any]:
    """
    Calculates the physical speed-of-light propagation floor in single-mode optical fiber.
    Speed of light in vacuum c = 299,792 km/s.
    Refractive index of silica optical fiber n ≈ 1.468 (approx 1.5).
    Effective propagation velocity v = c / n ≈ 204,200 km/s ≈ 200 km/ms ≈ 5 µs/km.
    """
    if distance_km < 0:
        raise ValueError("Distance must be non-negative")
    c_km_s = 299792.458
    n_fiber = 1.4682
    v_fiber_km_s = c_km_s / n_fiber
    v_fiber_km_ms = v_fiber_km_s / 1000.0  # ~204.2 km/ms

    one_way_ms = distance_km / v_fiber_km_ms
    rtt_floor_ms = 2.0 * one_way_ms

    return {
        "distance_km": distance_km,
        "fiber_propagation_speed_km_s": round(v_fiber_km_s, 2),
        "fiber_propagation_delay_per_km_us": round(1000.0 / v_fiber_km_ms, 2),
        "one_way_propagation_floor_ms": round(one_way_ms, 4),
        "rtt_propagation_floor_ms": round(rtt_floor_ms, 4),
        "real_network_overhead_factors": [
            "Fiber route tortuosity (cable follows roads/railways, not straight line geodesic: 1.2x - 1.5x distance)",
            "Optical amplifiers (EDFA) and dispersion compensation modules",
            "Router/switch store-and-forward latency and serialization delay",
            "Queuing delay under network buffer congestion",
            "Host operating system kernel network stack interrupt and packet processing",
        ],
    }


def evaluate_cloud_architecture(scenario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates availability, physical constraints, and omitted shared dependencies
    for a multi-tier cloud topology.
    """
    web_a = scenario.get("web_instance_availability", 0.99)
    db_primary_a = scenario.get("db_primary_availability", 0.999)
    db_standby_a = scenario.get("db_standby_availability", 0.999)
    lb_a = scenario.get("load_balancer_availability", 0.9999)
    inter_az_distance_km = scenario.get("inter_az_distance_km", 30.0)
    inter_region_distance_km = scenario.get("inter_region_distance_km", 3800.0)

    # 1. Parallel Web Tier (2 independent instances)
    web_tier_a = calculate_parallel_availability(web_a, web_a)

    # 2. Parallel Database Standby (with automated failover)
    db_tier_a = calculate_parallel_availability(db_primary_a, db_standby_a)

    # 3. Overall Series Pipeline: Load Balancer * Web Tier * DB Tier
    system_theoretical_a = calculate_serial_availability([lb_a, web_tier_a, db_tier_a])

    # 4. Latency floors
    az_latency = calculate_fiber_propagation_floor(inter_az_distance_km)
    region_latency = calculate_fiber_propagation_floor(inter_region_distance_km)

    return {
        "inputs": scenario,
        "web_tier_redundant_availability": web_tier_a,
        "db_tier_redundant_availability": db_tier_a,
        "theoretical_system_availability": system_theoretical_a,
        "theoretical_annual_downtime_minutes": calculate_annual_downtime(system_theoretical_a * 100.0),
        "inter_az_propagation_rtt_floor_ms": az_latency["rtt_propagation_floor_ms"],
        "inter_region_propagation_rtt_floor_ms": region_latency["rtt_propagation_floor_ms"],
        "critical_shared_dependencies_omitted": [
            "DNS provider resolution failure (Single Point of Failure)",
            "Shared Cloud IAM / Control Plane outage preventing failover or scaling",
            "Shared VPC router / software-defined overlay network routing drop",
            "Correlated software defects deployed simultaneously across instances",
            "Database replication lag / split-brain during failover window",
            "Metropolitan-scale catastrophic events impacting all AZs in one region (power grid, flood)",
        ],
        "sla_distinction": (
            "Provider SLA is a legal/commercial liability contract defining billing refunds. "
            "It does NOT equal physical failure probability for any single virtual machine."
        ),
    }


def run_activity(save_scratch: bool = True) -> int:
    print("=" * 76)
    print(" ESSENTIAL CS -- ACTIVITY L19-02: CLOUD TOPOLOGY & AVAILABILITY MATH")
    print(" Focus: Availability Formulas, Latency Lower-Bounds, & Shared Dependencies")
    print("=" * 76)

    # 1. The Numbers Behind "Nines"
    print("\n[PART 1: The Harsh Reality of Availability 'Nines']")
    print(" " + "-" * 64)
    print(f" | {'Availability':<14} | {'Annual Downtime (Minutes)':<26} | {'Equivalent':<16} |")
    print(" | :------------- | :------------------------- | :--------------- |")
    benchmarks = [
        (99.0, "3.65 days"),
        (99.9, "8.76 hours"),
        (99.95, "4.38 hours"),
        (99.99, "52.56 minutes"),
        (99.999, "5.26 minutes"),
    ]
    for pct, equiv in benchmarks:
        mins = calculate_annual_downtime(pct)
        print(f" | {pct:<13}% | {mins:<26.2f} | {equiv:<16} |")
    print(" " + "-" * 64)

    # 2. Redundancy Math & Common-Mode Failures
    print("\n[PART 2: Parallel Redundancy Math vs. Shared Dependencies]")
    a_single = 0.99  # 99% availability per instance
    a_parallel = calculate_parallel_availability(a_single, a_single)
    print(f" Single Instance Availability:         {a_single * 100.0:.1f}% ({calculate_annual_downtime(a_single * 100.0):.1f} min downtime/yr)")
    print(f" Two Independent Parallel Instances:   {a_parallel * 100.0:.2f}% ({calculate_annual_downtime(a_parallel * 100.0):.1f} min downtime/yr)")
    print("\n WARNING: The formula A = 1 - (1-a1)(1-a2) assumes ZERO shared dependencies!")
    print(" If both instances share a Load Balancer with 99.9% availability,")
    print(" overall system availability can NEVER exceed 99.9% (Series dependency rule).")

    # 3. Speed of Light & Geographic Topology
    print("\n[PART 3: Fiber Optic Propagation Floors (Speed of Light in Silica)]")
    distances = [
        ("Adjacent Availability Zones (Metro)", 30.0),
        ("Cross-Zone Edge (Region boundary)", 100.0),
        ("Cross-Continent (Virginia <-> California)", 3800.0),
        ("Trans-Atlantic (New York <-> London)", 5500.0),
        ("Trans-Pacific (California <-> Tokyo)", 8700.0),
    ]
    print(" " + "-" * 72)
    print(f" | {'Path Description':<38} | {'Dist (km)':<10} | {'RTT Floor (ms)':<14} |")
    print(" | :------------------------------------- | :--------- | :------------- |")
    for desc, dist in distances:
        lat = calculate_fiber_propagation_floor(dist)
        print(f" | {desc:<38} | {dist:<10.0f} | {lat['rtt_propagation_floor_ms']:<14.2f} |")
    print(" " + "-" * 72)
    print(" Invariant: No cloud provider or network protocol can beat 5 microseconds per km in fiber.")
    print(" Multi-Region synchronous consensus is physically bounded by trans-continental RTT.")

    # 4. Multi-tier Cloud Architecture Evaluation
    print("\n[PART 4: Cloud Architecture Evaluation]")
    scenario = {
        "scenario_name": "Multi-AZ Web Application",
        "web_instance_availability": 0.99,
        "db_primary_availability": 0.999,
        "db_standby_availability": 0.999,
        "load_balancer_availability": 0.9999,
        "inter_az_distance_km": 30.0,
        "inter_region_distance_km": 3800.0,
    }
    eval_result = evaluate_cloud_architecture(scenario)
    print(f" Web Tier (2x Parallel):               {eval_result['web_tier_redundant_availability']*100.0:.4f}%")
    print(f" Database Tier (Primary + Standby):     {eval_result['db_tier_redundant_availability']*100.0:.4f}%")
    print(f" System Theoretical Availability:      {eval_result['theoretical_system_availability']*100.0:.4f}%")
    print(f" Theoretical Annual Downtime:          {eval_result['theoretical_annual_downtime_minutes']:.2f} minutes")
    print(f" Inter-AZ Round-Trip Propagation Floor:{eval_result['inter_az_propagation_rtt_floor_ms']:.2f} ms")
    print(f" Inter-Region Round-Trip Floor:        {eval_result['inter_region_propagation_rtt_floor_ms']:.2f} ms")

    # 5. Save scratch artifact
    if save_scratch:
        scratch_dir = CURRENT_DIR / ".scratch"
        try:
            scratch_dir.mkdir(parents=True, exist_ok=True)
            out_file = scratch_dir / "l19_02_worksheet.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(eval_result, f, indent=2, ensure_ascii=False)
            print(f"\n[Artifact Saved]: {out_file.relative_to(CURRENT_DIR)}")
        except Exception as e:
            print(f"\n[Notice]: Could not write scratch artifact: {e}")

    print("=" * 76)
    return 0


if __name__ == "__main__":
    sys.exit(run_activity())
