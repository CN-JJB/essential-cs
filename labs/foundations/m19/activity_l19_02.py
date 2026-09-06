#!/usr/bin/env python3
"""
activity_l19_02.py
Essential CS: Stage 6 Module 19 (M19) Activity L19-02.

Hands-on activity: Cloud Topology, Availability Math, and Failure Domains.
Evaluates scenario-specific availability calculations, parallel redundancy math,
physical propagation lower bounds, and provider SLA contractual limits.
"""

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CURRENT_DIR = Path(__file__).resolve().parent

MINUTES_PER_YEAR = 365 * 24 * 60  # 525,600 minutes (standard non-leap calendar year)


def calculate_annual_downtime(availability_pct: float) -> float:
    """
    Calculates allowable downtime in minutes per year for a given availability percentage.
    Formula: 525,600 * (1 - availability_pct / 100)
    Example: 99.9% -> 525.6 minutes per year.
    """
    if not (0.0 <= availability_pct <= 100.0):
        raise ValueError(f"Availability percentage must be between 0.0 and 100.0, got {availability_pct}")
    downtime_fraction = (100.0 - availability_pct) / 100.0
    return round(MINUTES_PER_YEAR * downtime_fraction, 4)


def calculate_parallel_availability(a1: float, a2: float) -> float:
    """
    Calculates parallel redundancy availability for two components:
    A = 1 - (1 - a1) * (1 - a2)

    CRITICAL MODEL ASSUMPTIONS:
    1. Failure independence: Failures of component 1 and component 2 are mutually independent.
       (Invalidated by common-mode failures such as shared power, top-of-rack switches, or poison messages).
    2. Substitutable capacity: Either component alone satisfies the workload under the modeled success criteria.
    3. Transparent failover: Health-checking, routing, and failover mechanisms introduce no unmodeled failure.
    """
    if not (0.0 <= a1 <= 1.0) or not (0.0 <= a2 <= 1.0):
        raise ValueError("Availability probabilities a1 and a2 must be in range [0.0, 1.0]")
    return round(1.0 - (1.0 - a1) * (1.0 - a2), 8)


def calculate_serial_availability(components: List[float]) -> float:
    """
    Calculates series system availability:
    A_system = prod(c_i)

    Under the stated independence and serial dependency model, overall availability
    satisfies: A_system <= min(c_i).
    """
    total = 1.0
    for c in components:
        if not (0.0 <= c <= 1.0):
            raise ValueError(f"Component availability must be in range [0.0, 1.0], got {c}")
        total *= c
    return round(total, 8)


def calculate_fiber_propagation_floor(
    distance_km: float,
    speed_km_s: float = 200000.0,
) -> Dict[str, Any]:
    """
    Calculates the physical speed-of-light propagation floor in optical fiber
    for an illustrative geometric path length.

    Simplified teaching model:
    - Speed of light in vacuum: c ≈ 299,792 km/s
    - Single-mode silica fiber refractive index: n ≈ 1.4682
    - Propagation speed in silica glass: v = c / n ≈ 204,190 km/s (modeled here at ~200,000 km/s)
    - One-way propagation delay: ~5 µs per km (~0.005 ms/km)
    - Round-trip time (RTT) floor: ~10 µs per km (~0.010 ms/km)

    NOTE: Modeled path length is an illustrative lower-bound input, not an actual provider distance.
    Real network RTT depends on the actual optical route plus link equipment, switching/routing,
    serialization, queuing, protocol processing, and endpoint behavior. This course does not
    freeze a universal route-inflation multiplier or device-latency constant.
    """
    if distance_km < 0:
        raise ValueError("Distance must be non-negative")
    if speed_km_s <= 0:
        raise ValueError("Propagation speed must be positive")

    one_way_ms = (distance_km / speed_km_s) * 1000.0
    rtt_floor_ms = 2.0 * one_way_ms

    return {
        "modeled_distance_km": distance_km,
        "modeled_propagation_speed_km_s": speed_km_s,
        "one_way_propagation_delay_per_km_us": round(1000000.0 / speed_km_s, 2),
        "one_way_propagation_floor_ms": round(one_way_ms, 4),
        "rtt_propagation_floor_ms": round(rtt_floor_ms, 4),
        "real_network_overhead_factors": [
            "Actual optical route length differs from simple geometric distance; no universal multiplier is assumed",
            "Optical dispersion compensation modules and repeaters/amplifiers",
            "Router/switch queuing delay, packet serialization, and bufferbloat under congestion",
            "Software network stack interrupt processing and context switching in host operating systems",
        ],
    }


def evaluate_cloud_architecture(scenario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates availability, physical constraints, and omitted shared dependencies
    for an illustrative multi-tier cloud topology.
    """
    web_a = scenario.get("web_instance_availability", 0.99)
    db_primary_a = scenario.get("db_primary_availability", 0.999)
    db_standby_a = scenario.get("db_standby_availability", 0.999)
    lb_a = scenario.get("load_balancer_availability", 0.9999)
    inter_zone_distance_km = scenario.get("inter_zone_modeled_distance_km", 30.0)
    inter_region_distance_km = scenario.get("inter_region_modeled_distance_km", 3800.0)

    # 1. Parallel Web Tier (2 modeled independent instances)
    web_tier_a = calculate_parallel_availability(web_a, web_a)

    # 2. Parallel Database Tier (Primary + Standby under assumed automatic failover)
    db_tier_a = calculate_parallel_availability(db_primary_a, db_standby_a)

    # 3. Overall Series Pipeline: Load Balancer * Web Tier * DB Tier
    system_theoretical_a = calculate_serial_availability([lb_a, web_tier_a, db_tier_a])

    # 4. Physical propagation floors
    zone_latency = calculate_fiber_propagation_floor(inter_zone_distance_km)
    region_latency = calculate_fiber_propagation_floor(inter_region_distance_km)

    return {
        "scenario_name": scenario.get("scenario_name", "Illustrative Multi-Zone Architecture"),
        "inputs": scenario,
        "modeled_availability": {
            "web_tier_parallel_availability": web_tier_a,
            "db_tier_parallel_availability": db_tier_a,
            "system_theoretical_availability": system_theoretical_a,
            "theoretical_annual_downtime_minutes": calculate_annual_downtime(system_theoretical_a * 100.0),
        },
        "modeled_propagation_floors": {
            "inter_zone_rtt_floor_ms": zone_latency["rtt_propagation_floor_ms"],
            "inter_region_rtt_floor_ms": region_latency["rtt_propagation_floor_ms"],
        },
        "stated_scenario_assumptions": [
            "Component failure probabilities are mutually independent.",
            "Each redundant component provides 100% substitutable capacity for the modeled workload.",
            "Failover and load balancing mechanisms operate instantaneously and introduce no unmodeled failure.",
        ],
        "omitted_shared_dependencies": [
            "External DNS / name-resolution dependency, if shared by the scenario",
            "Cloud provider control plane / IAM service outage preventing failover or autoscaling",
            "Shared software-defined overlay network routing drops or BGP flapping",
            "Correlated application defects or poisoned configuration deployed across all instances",
            "Database replication lag, lock contention, or split-brain during failover window",
            "Metropolitan utility grid or power transmission corridor shared across physical sites",
        ],
        "provider_sla_boundary": (
            "A provider/service SLA is an external contractual commitment whose measurement window, scope, "
            "exclusions, and remedies (if any) are specific to that named agreement. Its percentage is NOT "
            "automatically an independent physical failure probability for an individual instance. "
            "The availability values in this evaluator are course-authored scenario inputs, not provider SLA facts."
        ),
    }


def run_activity(save_scratch: bool = True) -> int:
    print("=" * 76)
    print(" ESSENTIAL CS -- ACTIVITY L19-02: CLOUD TOPOLOGY & AVAILABILITY MATH")
    print(" Focus: Availability Formulas, Latency Lower-Bounds, & Shared Dependencies")
    print("=" * 76)

    # 1. The Numbers Behind "Nines"
    print("\n[PART 1: Availability Percentages and Allowable Annual Downtime]")
    print(" (Basis: 365-day non-leap calendar year = 525,600 minutes)")
    print(" " + "-" * 66)
    print(f" | {'Availability %':<16} | {'Annual Downtime (Minutes)':<26} | {'Time Unit Approx':<16} |")
    print(" | :--------------- | :------------------------- | :--------------- |")
    benchmarks = [
        (99.0, "3.65 days"),
        (99.9, "8.76 hours"),
        (99.95, "4.38 hours"),
        (99.99, "52.56 minutes"),
        (99.999, "5.26 minutes"),
    ]
    for pct, equiv in benchmarks:
        mins = calculate_annual_downtime(pct)
        print(f" | {pct:<15.3f}% | {mins:<26.2f} | {equiv:<16} |")
    print(" " + "-" * 66)
    print(" Invariant: Each added 'nine' reduces allowable downtime by a factor of 10.")

    # 2. Redundancy Math & Common-Mode Failures
    print("\n[PART 2: Parallel Redundancy Math vs. Shared Dependencies]")
    a_single = 0.99  # 99% modeled availability per instance
    a_parallel = calculate_parallel_availability(a_single, a_single)
    print(f" Single Instance Modeled Availability:       {a_single * 100.0:.1f}% ({calculate_annual_downtime(a_single * 100.0):.1f} min downtime/yr)")
    print(f" Two Independent Parallel Instances:         {a_parallel * 100.0:.2f}% ({calculate_annual_downtime(a_parallel * 100.0):.1f} min downtime/yr)")
    print("\n IMPORTANT MODEL ASSUMPTIONS:")
    print(" - This course formula assumes independent failures, substitutable capacity, and successful routing/failover.")
    print(" - If both instances share a modeled Load Balancer with 99.9% availability,")
    print("   overall system availability CANNOT exceed 99.9% (A_system <= min(A_i) series rule).")

    # 3. Speed of Light & Geographic Topology
    print("\n[PART 3: Fiber Optic Propagation Floors (Speed of Light in Silica Glass)]")
    print(" (Teaching Model: v ~ 200,000 km/s in silica fiber; ~5 us/km one-way delay)")
    scenarios = [
        ("Illustrative Metro-scale path", 30.0),
        ("Illustrative Regional-scale path", 100.0),
        ("Illustrative Trans-continental path", 3800.0),
        ("Illustrative Trans-oceanic path (Atlantic)", 5500.0),
        ("Illustrative Trans-oceanic path (Pacific)", 8700.0),
    ]
    print(" " + "-" * 72)
    print(f" | {'Illustrative Path Description':<40} | {'Dist (km)':<10} | {'RTT Floor (ms)':<14} |")
    print(" | :--------------------------------------- | :--------- | :------------- |")
    for desc, dist in scenarios:
        lat = calculate_fiber_propagation_floor(dist)
        print(f" | {desc:<40} | {dist:<10.0f} | {lat['rtt_propagation_floor_ms']:<14.2f} |")
    print(" " + "-" * 72)
    print(" Invariant: Fiber propagation speed creates a physical lower bound on network latency.")
    print(" Multi-region synchronous consensus protocols are physically bounded by RTT.")

    # 4. Multi-tier Cloud Architecture Evaluation
    print("\n[PART 4: Illustrative Cloud Architecture Evaluation]")
    scenario = {
        "scenario_name": "Illustrative Multi-Zone Web Application",
        "web_instance_availability": 0.99,
        "db_primary_availability": 0.999,
        "db_standby_availability": 0.999,
        "load_balancer_availability": 0.9999,
        "inter_zone_modeled_distance_km": 30.0,
        "inter_region_modeled_distance_km": 3800.0,
    }
    eval_result = evaluate_cloud_architecture(scenario)
    avail = eval_result["modeled_availability"]
    floors = eval_result["modeled_propagation_floors"]
    print(f" Web Tier (2x Parallel Modeled):             {avail['web_tier_parallel_availability']*100.0:.4f}%")
    print(f" Database Tier (Primary + Standby Modeled):   {avail['db_tier_parallel_availability']*100.0:.4f}%")
    print(f" System Theoretical Availability:            {avail['system_theoretical_availability']*100.0:.4f}%")
    print(f" Theoretical Annual Downtime:                {avail['theoretical_annual_downtime_minutes']:.2f} minutes")
    print(f" Modeled Inter-Zone RTT Propagation Floor:   {floors['inter_zone_rtt_floor_ms']:.2f} ms")
    print(f" Modeled Inter-Region RTT Floor:             {floors['inter_region_rtt_floor_ms']:.2f} ms")
    print("\n Omitted Critical Shared Dependencies:")
    for dep in eval_result["omitted_shared_dependencies"][:4]:
        print(f"   ! {dep}")
    print(f"\n Provider SLA Boundary: {eval_result['provider_sla_boundary']}")

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
