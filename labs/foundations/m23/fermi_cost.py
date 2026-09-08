#!/usr/bin/env python3
"""
fermi_cost.py — Bounded Capacity Planning, Fermi Estimation & Cost Modeling Helper
===================================================================================

Canonical Module: M23 — Systems Thinking & Judgment
Canonical Lesson: L23-03 — What is the cost of my design?

Provides deterministic, assumption-first arithmetic for systems capacity planning:
1. Unit conversions distinguishing bits (b) vs. Bytes (B), and decimal (SI) vs. binary (IEC) prefixes.
2. Storage growth and bounded retention models (with replication factors and indexing overhead).
3. Network egress bandwidth estimation distinguishing average vs. peak traffic.
4. In-memory working set cache-fit calculations under explicit memory safety margins.
5. Multi-dimensional Total Cost of Ownership (TCO) separating hardware/cloud infrastructure
   from human operational maintenance (without asserting that one is universally 'highest').
6. Sensitivity analysis modeling how a 10x traffic surge or changed retention alters bottleneck resources.

Zero external dependencies (Python standard library only).
Fails closed on negative values, zero durations, and invalid unit strings.
"""

from __future__ import annotations

import math
from typing import Any, Callable, Dict, List, Optional, Tuple

def get_storage_factor_to_bytes(unit_str: str) -> float:
    """Returns the multiplier to convert 1 unit of `unit_str` to Bytes."""
    raw = unit_str.strip()
    if not raw:
        raise ValueError("Unit string cannot be empty")

    # Strict bit vs Byte distinction
    if raw == "b" or raw.lower() in ("bit", "bits"):
        return 1.0 / 8.0
    if raw == "B" or raw.lower() in ("byte", "bytes"):
        return 1.0

    lower = raw.lower()
    # Explicit bit names
    bit_units = {
        "kbit": 1_000.0 / 8.0,
        "mbit": 1_000_000.0 / 8.0,
        "gbit": 1_000_000_000.0 / 8.0,
        "tbit": 1_000_000_000_000.0 / 8.0,
        "pbit": 1_000_000_000_000_000.0 / 8.0,
        "kibit": 1_024.0 / 8.0,
        "mibit": 1_048_576.0 / 8.0,
        "gibit": 1_073_741_824.0 / 8.0,
    }
    if lower in bit_units:
        return bit_units[lower]

    # Byte units (Decimal SI, base 1000)
    decimal_units = {
        "kb": 1_000.0,
        "mb": 1_000_000.0,
        "gb": 1_000_000_000.0,
        "tb": 1_000_000_000_000.0,
        "pb": 1_000_000_000_000_000.0,
    }
    if lower in decimal_units:
        return decimal_units[lower]

    # Byte units (Binary IEC, base 1024)
    binary_units = {
        "kib": 1_024.0,
        "mib": 1_048_576.0,
        "gib": 1_073_741_824.0,
        "tib": 1_099_511_627_776.0,
        "pib": 1_125_899_906_842_624.0,
    }
    if lower in binary_units:
        return binary_units[lower]

    raise ValueError(f"Unrecognized storage unit: '{unit_str}'. Supported: b, B, KB, KiB, MB, MiB, GB, GiB, TB, TiB, PB, PiB, kbit, mbit, gbit")


def convert_storage(value: float, from_unit: str, to_unit: str) -> float:
    """
    Converts storage quantity between units with rigorous bit/Byte and decimal/binary tracking.

    Rejects negative values or unrecognized unit strings.
    """
    if value < 0:
        raise ValueError(f"Storage value cannot be negative, got {value}")

    f_factor = get_storage_factor_to_bytes(from_unit)
    t_factor = get_storage_factor_to_bytes(to_unit)

    bytes_val = value * f_factor
    return bytes_val / t_factor


def estimate_storage_capacity(
    items_per_day: float,
    avg_item_bytes: float,
    replication_factor: float = 1.0,
    indexing_overhead_ratio: float = 0.0,
    retention_days: Optional[float] = None,
) -> Dict[str, float]:
    """
    Calculates storage capacity requirements.

    Parameters:
    - items_per_day: Number of new records created daily.
    - avg_item_bytes: Average raw payload size of each record.
    - replication_factor: Copies stored for durability/HA (must be >= 1.0).
    - indexing_overhead_ratio: Extra storage for indexes/metadata (e.g. 0.25 for 25%).
    - retention_days: If set, storage bounds to a rolling retention window.
                      If None, calculates perpetual daily growth rate.

    Returns dictionary with logical and physical storage numbers in Bytes and GB/TB.
    """
    if items_per_day < 0:
        raise ValueError("items_per_day cannot be negative")
    if avg_item_bytes < 0:
        raise ValueError("avg_item_bytes cannot be negative")
    if replication_factor < 1.0:
        raise ValueError("replication_factor must be >= 1.0")
    if indexing_overhead_ratio < 0.0:
        raise ValueError("indexing_overhead_ratio cannot be negative")
    if retention_days is not None and retention_days <= 0:
        raise ValueError("retention_days must be positive when specified")

    daily_logical_bytes = items_per_day * avg_item_bytes
    overhead_multiplier = 1.0 + indexing_overhead_ratio
    daily_physical_bytes = daily_logical_bytes * replication_factor * overhead_multiplier

    res: Dict[str, float] = {
        "daily_logical_bytes": daily_logical_bytes,
        "daily_physical_bytes": daily_physical_bytes,
        "daily_logical_gb": daily_logical_bytes / 1e9,
        "daily_physical_gb": daily_physical_bytes / 1e9,
        "daily_physical_gib": daily_physical_bytes / (1024.0**3),
    }

    if retention_days is not None:
        retained_physical_bytes = daily_physical_bytes * retention_days
        res["retention_days"] = retention_days
        res["total_retained_bytes"] = retained_physical_bytes
        res["total_retained_gb"] = retained_physical_bytes / 1e9
        res["total_retained_tb"] = retained_physical_bytes / 1e12
        res["total_retained_tib"] = retained_physical_bytes / (1024.0**4)
    else:
        # Annualized unconstrained growth
        res["annual_physical_bytes"] = daily_physical_bytes * 365.25
        res["annual_physical_tb"] = (daily_physical_bytes * 365.25) / 1e12

    return res


def estimate_network_egress(
    requests_per_day: float,
    avg_payload_bytes: float,
    peak_to_avg_ratio: float = 1.0,
) -> Dict[str, float]:
    """
    Estimates daily egress data volume and bandwidth requirements.

    Parameters:
    - requests_per_day: Outbound response count per day.
    - avg_payload_bytes: Average outbound response size in Bytes.
    - peak_to_avg_ratio: Multiplier for peak load burst (must be >= 1.0).

    Returns:
    - total_egress_bytes_per_day
    - avg_bytes_per_sec, avg_bits_per_sec (bps)
    - peak_bytes_per_sec, peak_bits_per_sec (bps)
    """
    if requests_per_day < 0:
        raise ValueError("requests_per_day cannot be negative")
    if avg_payload_bytes < 0:
        raise ValueError("avg_payload_bytes cannot be negative")
    if peak_to_avg_ratio < 1.0:
        raise ValueError("peak_to_avg_ratio must be >= 1.0")

    total_bytes_day = requests_per_day * avg_payload_bytes
    seconds_in_day = 86400.0

    avg_Bps = total_bytes_day / seconds_in_day
    avg_bps = avg_Bps * 8.0

    peak_Bps = avg_Bps * peak_to_avg_ratio
    peak_bps = avg_bps * peak_to_avg_ratio

    return {
        "daily_egress_bytes": total_bytes_day,
        "daily_egress_gb": total_bytes_day / 1e9,
        "daily_egress_gib": total_bytes_day / (1024.0**3),
        "avg_bytes_per_sec": avg_Bps,
        "avg_bits_per_sec": avg_bps,
        "avg_mbps": avg_bps / 1e6,
        "peak_bytes_per_sec": peak_Bps,
        "peak_bits_per_sec": peak_bps,
        "peak_mbps": peak_bps / 1e6,
        "peak_to_avg_ratio": peak_to_avg_ratio,
    }


def estimate_memory_cache_fit(
    active_items: float,
    avg_item_bytes: float,
    installed_ram_bytes: float,
    max_cache_fraction: float = 0.75,
) -> Dict[str, Any]:
    """
    Evaluates whether an active dataset fits in single-node RAM without paging.

    Rejects the myth that 'a 16GB server can trivially hold everything' without doing the math.
    """
    if active_items < 0:
        raise ValueError("active_items cannot be negative")
    if avg_item_bytes < 0:
        raise ValueError("avg_item_bytes cannot be negative")
    if installed_ram_bytes <= 0:
        raise ValueError("installed_ram_bytes must be positive")
    if max_cache_fraction <= 0 or max_cache_fraction >= 1.0:
        raise ValueError("max_cache_fraction must be between 0.0 and 1.0 (e.g. 0.75)")

    dataset_bytes = active_items * avg_item_bytes
    usable_ram_bytes = installed_ram_bytes * max_cache_fraction
    fits = dataset_bytes <= usable_ram_bytes
    utilization_pct = (dataset_bytes / usable_ram_bytes) * 100.0

    return {
        "dataset_bytes": dataset_bytes,
        "dataset_gb": dataset_bytes / 1e9,
        "dataset_gib": dataset_bytes / (1024.0**3),
        "usable_ram_bytes": usable_ram_bytes,
        "usable_ram_gib": usable_ram_bytes / (1024.0**3),
        "fits_in_memory": fits,
        "usable_ram_utilization_pct": utilization_pct,
    }


def calculate_tco(
    infra_monthly_cost: float,
    human_hours_per_month: float,
    human_hourly_rate: float,
) -> Dict[str, float]:
    """
    Calculates Total Cost of Ownership (TCO) combining direct infrastructure billing
    and human engineering operational friction.

    Does not bias towards claiming human cost is always higher or lower; computes
    the exact distribution from declared assumptions.
    """
    if infra_monthly_cost < 0:
        raise ValueError("infra_monthly_cost cannot be negative")
    if human_hours_per_month < 0:
        raise ValueError("human_hours_per_month cannot be negative")
    if human_hourly_rate < 0:
        raise ValueError("human_hourly_rate cannot be negative")

    human_monthly_cost = human_hours_per_month * human_hourly_rate
    total_monthly_cost = infra_monthly_cost + human_monthly_cost

    if total_monthly_cost > 0:
        infra_pct = (infra_monthly_cost / total_monthly_cost) * 100.0
        human_pct = (human_monthly_cost / total_monthly_cost) * 100.0
    else:
        infra_pct = 0.0
        human_pct = 0.0

    return {
        "infra_monthly_cost": infra_monthly_cost,
        "human_monthly_cost": human_monthly_cost,
        "total_monthly_cost": total_monthly_cost,
        "infra_percentage": infra_pct,
        "human_percentage": human_pct,
    }


def run_sensitivity_analysis(
    baseline_params: Dict[str, Any],
    variations: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Performs sensitivity analysis comparing baseline capacity/cost against
    variations (e.g. 10x traffic, retention window adjustment, payload compression).
    """
    results: Dict[str, Any] = {}

    def compute_model(p: Dict[str, Any]) -> Dict[str, float]:
        st = estimate_storage_capacity(
            items_per_day=p.get("items_per_day", 100_000),
            avg_item_bytes=p.get("avg_item_bytes", 2048),
            replication_factor=p.get("replication_factor", 3.0),
            retention_days=p.get("retention_days", 90),
        )
        eg = estimate_network_egress(
            requests_per_day=p.get("requests_per_day", 1_000_000),
            avg_payload_bytes=p.get("avg_egress_bytes", 4096),
            peak_to_avg_ratio=p.get("peak_to_avg_ratio", 2.5),
        )
        return {
            "retained_tb": st.get("total_retained_tb", 0.0),
            "daily_egress_gb": eg["daily_egress_gb"],
            "peak_mbps": eg["peak_mbps"],
        }

    baseline_metrics = compute_model(baseline_params)
    results["baseline"] = {
        "params": baseline_params,
        "metrics": baseline_metrics,
    }

    variations_res: Dict[str, Any] = {}
    for var_name, var_overrides in variations.items():
        merged = dict(baseline_params)
        merged.update(var_overrides)
        var_metrics = compute_model(merged)

        deltas = {}
        for k, v in var_metrics.items():
            b_val = baseline_metrics[k]
            ratio = (v / b_val) if b_val > 0 else 1.0
            deltas[k] = {
                "val": v,
                "multiplier": ratio,
            }

        variations_res[var_name] = {
            "overrides": var_overrides,
            "metrics": var_metrics,
            "deltas_from_baseline": deltas,
        }

    results["variations"] = variations_res
    return results


def main() -> None:
    print("=" * 80)
    print("  M23 L23-03: BOUNDED FERMI ESTIMATION & CAPACITY MODELING HARNESS")
    print("=" * 80)

    # Example: Photo sharing service
    # 1M DAU, 2 uploads/day (1MB each), 50 views/day (1MB each), 3x replication, 90-day retention
    dau = 1_000_000
    uploads_day = dau * 2
    views_day = dau * 50
    photo_size_bytes = 1_000_000  # 1 MB

    print("\n[SCENARIO: PHOTO SHARING SERVICE CAPACITY MODEL]")
    print(f"  DAU:              {dau:,}")
    print(f"  Uploads/day:      {uploads_day:,} (avg {photo_size_bytes / 1e6:.1f} MB)")
    print(f"  Views/day:        {views_day:,} (avg {photo_size_bytes / 1e6:.1f} MB)")
    print("  Replication:      3.0x")
    print("  Retention:        90 days (hot storage)")
    print("  Peak-to-avg ratio: 3.0x")
    print("-" * 80)

    storage = estimate_storage_capacity(
        items_per_day=uploads_day,
        avg_item_bytes=photo_size_bytes,
        replication_factor=3.0,
        retention_days=90,
    )
    print(f"  Daily Logical Ingestion:  {storage['daily_logical_gb']:.1f} GB/day ({storage['daily_logical_bytes']/1e12:.2f} TB/day)")
    print(f"  Daily Physical Ingestion: {storage['daily_physical_gb']:.1f} GB/day (3x replication)")
    print(f"  90-Day Retained Storage:  {storage['total_retained_tb']:.2f} TB ({storage['total_retained_tib']:.2f} TiB)")

    egress = estimate_network_egress(
        requests_per_day=views_day,
        avg_payload_bytes=photo_size_bytes,
        peak_to_avg_ratio=3.0,
    )
    print(f"  Daily Network Egress:     {egress['daily_egress_gb']:.1f} GB/day ({egress['daily_egress_bytes']/1e12:.2f} TB/day)")
    print(f"  Average Egress Bandwidth: {egress['avg_mbps']:.1f} Mbps ({egress['avg_mbps']/1000:.2f} Gbps)")
    print(f"  Peak Egress Bandwidth:    {egress['peak_mbps']:.1f} Mbps ({egress['peak_mbps']/1000:.2f} Gbps)")

    print("-" * 80)
    print("[BOTTLENECK CONCLUSION]")
    print("  This system is overwhelmingly NETWORK EGRESS and STORAGE bound.")
    print("  Peak egress is ~13.9 Gbps. Direct server serving would saturate network interfaces.")
    print("  Caching at CDN edge and image optimization (WebP/AVIF compression) are mandatory.")
    print("=" * 80)


if __name__ == "__main__":
    main()
