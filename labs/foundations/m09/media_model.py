#!/usr/bin/env python3
"""HDD vs SSD Physical Mechanics, Write Amplification (WAF), and Media Model for M09 L09-02.

Demonstrates:
1. Pure calculation and illustrative simulation (labeled ILLUSTRATIVE MODEL EVIDENCE).
2. HDD mechanical latency model (seek + rotational delay vs sequential throughput).
3. SSD NAND Flash constraints: page program vs block erase, out-of-place updates,
   FTL mapping, invalidation, garbage collection, and wear leveling.
4. Write Amplification Factor (WAF = bytes written to flash / bytes written by host).
5. Drive endurance (TBW) calculation and inference limits under JEDEC standards.
"""

import json
import sys


def validate_media_model_inputs(
    pages_per_block: int,
    page_size_kb: int,
    valid_pages_in_victim: int,
) -> None:
    """Ensure simulation parameters are strictly bounded and structurally valid."""
    if pages_per_block <= 0 or page_size_kb <= 0:
        raise ValueError("Block geometry parameters must be positive integers")
    if pages_per_block > 4096:
        raise ValueError(f"pages_per_block ({pages_per_block}) exceeds safety limit of 4096")
    if page_size_kb > 64:
        raise ValueError(f"page_size_kb ({page_size_kb}) exceeds safety limit of 64")
    if valid_pages_in_victim < 0 or valid_pages_in_victim >= pages_per_block:
        raise ValueError(
            f"valid_pages_in_victim ({valid_pages_in_victim}) must be between 0 and {pages_per_block - 1}"
        )


def calculate_hdd_latency(
    rpm: int = 7200,
    avg_seek_ms: float = 8.5,
    transfer_mb_s: float = 180.0,
    io_size_bytes: int = 4096,
    is_sequential: bool = False,
) -> dict:
    """Calculate mechanical HDD latency component breakdown for an I/O request.

    Note: Rotational latency and seek time are physical mechanical bounds.
    Essential CS does not assert a single universal constant for all drives.
    """
    if rpm <= 0 or avg_seek_ms < 0 or transfer_mb_s <= 0 or io_size_bytes <= 0:
        raise ValueError("Invalid HDD parameters")

    # Average rotational latency: half a rotation in milliseconds
    # (60 s / RPM) * 0.5 * 1000 ms
    avg_rotational_ms = (30.0 / rpm) * 1000.0

    # Transfer latency in milliseconds
    transfer_sec = (io_size_bytes / (1024 * 1024)) / transfer_mb_s
    transfer_ms = transfer_sec * 1000.0

    if is_sequential:
        # Sequential streaming amortizes seek and rotation across large contiguous tracks
        effective_seek_ms = 0.0
        effective_rot_ms = 0.0
    else:
        effective_seek_ms = avg_seek_ms
        effective_rot_ms = avg_rotational_ms

    total_latency_ms = effective_seek_ms + effective_rot_ms + transfer_ms
    iops = 1000.0 / total_latency_ms if total_latency_ms > 0 else 0.0

    return {
        "model_label": "ILLUSTRATIVE MODEL EVIDENCE",
        "rpm": rpm,
        "is_sequential": is_sequential,
        "io_size_bytes": io_size_bytes,
        "seek_ms": effective_seek_ms,
        "rotational_ms": effective_rot_ms,
        "transfer_ms": round(transfer_ms, 6),
        "total_latency_ms": round(total_latency_ms, 4),
        "estimated_iops": round(iops, 1),
    }


def simulate_ssd_waf_scenario(
    pages_per_block: int = 64,
    page_size_kb: int = 4,
    valid_pages_in_victim: int = 63,
    host_write_pages: int = 1,
) -> dict:
    """Calculate Write Amplification Factor (WAF) under an illustrative GC block reclamation.

    WAF = Total Bytes Written to Flash / Bytes Written by Host

    Illustrative Scenario:
    To reclaim a dirty block, Garbage Collection must:
    1. Read and copy all `valid_pages_in_victim` to a new free block.
    2. Erase the victim block.
    3. The host write of `host_write_pages` is committed into available space.

    Total flash writes = (valid_pages_copied + host_write_pages) * page_size.
    Host writes = host_write_pages * page_size.
    """
    validate_media_model_inputs(pages_per_block, page_size_kb, valid_pages_in_victim)
    if host_write_pages <= 0 or host_write_pages > pages_per_block:
        raise ValueError(f"host_write_pages must be between 1 and {pages_per_block}")

    page_size_bytes = page_size_kb * 1024
    host_bytes_written = host_write_pages * page_size_bytes

    # Garbage collection copies valid pages
    gc_copied_bytes = valid_pages_in_victim * page_size_bytes
    total_flash_bytes_written = gc_copied_bytes + host_bytes_written

    waf = total_flash_bytes_written / host_bytes_written

    return {
        "model_label": "ILLUSTRATIVE MODEL EVIDENCE",
        "pages_per_block": pages_per_block,
        "page_size_kb": page_size_kb,
        "block_size_kb": pages_per_block * page_size_kb,
        "valid_pages_in_victim": valid_pages_in_victim,
        "invalid_pages_reclaimed": pages_per_block - valid_pages_in_victim,
        "host_write_pages": host_write_pages,
        "host_bytes_written": host_bytes_written,
        "gc_copied_bytes": gc_copied_bytes,
        "total_flash_bytes_written": total_flash_bytes_written,
        "waf": round(waf, 4),
        "interpretation": (
            "Illustrative scenario demonstrating that out-of-place updates and block erase granularity "
            "can cause physical flash writes to substantially exceed host writes when reclaiming blocks "
            "with high valid-page residency."
        ),
    }


def estimate_ssd_endurance_tbw(
    drive_capacity_gb: float = 1000.0,
    pe_cycles: int = 3000,
    waf: float = 3.0,
) -> dict:
    """Calculate a simplified host-write budget under parameterized P/E and WAF assumptions.

    Teaching formula:
    Host_Write_Budget_TB = (Capacity_GB * Assumed_PE_Cycles) / (WAF * 1000)

    This is ILLUSTRATIVE MODEL EVIDENCE, not a JESD218 endurance-rating calculation.
    JESD218 defines SSD endurance requirements/test methods and JESD219 defines endurance
    workloads. Manufacturer TBW ratings and warranty limits must be read from the actual
    product specification/warranty and are not interchangeable with this teaching model.
    """
    if drive_capacity_gb <= 0 or pe_cycles <= 0 or waf <= 0:
        raise ValueError("Invalid endurance calculation parameters")
    if drive_capacity_gb > 100_000:
        raise ValueError("drive_capacity_gb exceeds safety calculation bound")

    total_flash_capacity_tb = (drive_capacity_gb * pe_cycles) / 1000.0
    host_tbw = total_flash_capacity_tb / waf

    return {
        "model_label": "ILLUSTRATIVE MODEL EVIDENCE",
        "drive_capacity_gb": drive_capacity_gb,
        "nand_pe_cycles": pe_cycles,
        "assumed_waf": waf,
        "total_flash_endurance_tb": round(total_flash_capacity_tb, 2),
        "estimated_host_tbw": round(host_tbw, 2),
        "inference_boundary_warning": (
            "This host-write budget is an illustrative arithmetic model, NOT a JESD218 endurance rating. "
            "JESD218/JESD219 define endurance requirements/test methods and workloads; actual product TBW "
            "and warranty terms must come from that product's specification. Real endurance also depends on "
            "temperature, retention requirements, controller behavior, workload and over-provisioning."
        ),
    }


def main() -> int:
    print("=== Essential CS M09 — Storage Media Model (L09-02) ===")

    # 1. HDD latency comparison
    hdd_rand = calculate_hdd_latency(rpm=7200, avg_seek_ms=8.5, is_sequential=False)
    hdd_seq = calculate_hdd_latency(rpm=7200, avg_seek_ms=8.5, is_sequential=True)
    print("\n[1] HDD Mechanical Latency Model (7200 RPM, 4 KiB):")
    print(f"    -> Random I/O:     Seek={hdd_rand['seek_ms']} ms, Rot={hdd_rand['rotational_ms']:.2f} ms => Total={hdd_rand['total_latency_ms']} ms (~{hdd_rand['estimated_iops']} IOPS)")
    print(f"    -> Sequential I/O: Seek={hdd_seq['seek_ms']} ms, Rot={hdd_seq['rotational_ms']:.2f} ms => Total={hdd_seq['total_latency_ms']} ms")

    # 2. SSD WAF scenarios
    print("\n[2] SSD Flash Translation & Write Amplification Scenarios (64-page block):")
    waf_worst = simulate_ssd_waf_scenario(pages_per_block=64, page_size_kb=4, valid_pages_in_victim=63, host_write_pages=1)
    waf_mid = simulate_ssd_waf_scenario(pages_per_block=64, page_size_kb=4, valid_pages_in_victim=32, host_write_pages=32)
    print(f"    -> Worst-case victim (63 valid / 1 invalid): WAF = {waf_worst['waf']} (Flash writes: {waf_worst['total_flash_bytes_written']} B for {waf_worst['host_bytes_written']} B host)")
    print(f"    -> Balanced victim (32 valid / 32 invalid): WAF = {waf_mid['waf']} (Flash writes: {waf_mid['total_flash_bytes_written']} B for {waf_mid['host_bytes_written']} B host)")

    # 3. Illustrative endurance arithmetic (not a product TBW/warranty rating)
    endurance = estimate_ssd_endurance_tbw(drive_capacity_gb=1000, pe_cycles=3000, waf=2.5)
    print("\n[3] Illustrative Host-Write Budget (1000 GB, assumed 3000 P/E, WAF=2.5):")
    print(f"    -> Illustrative Host-Write Budget: {endurance['estimated_host_tbw']} TB")
    print(f"    -> Boundary: {endurance['inference_boundary_warning']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
