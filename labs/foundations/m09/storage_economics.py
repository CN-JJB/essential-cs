#!/usr/bin/env python3
"""Storage Economics, Architecture Comparison, and Evaluation Framework for M09 L09-03.

Demonstrates:
1. Architecture and interface comparison: Block vs File vs Object storage.
2. Parameterized cost estimation modeling (capacity * rate + requests * rate + egress * rate).
3. Explicit listing of what the cost model omits (snapshot, provisioned IOPS, replication, padding).
4. Application of the Technology Evaluation Framework (Problem, Constraints, Mechanism,
   Gains, Costs, Failure Modes, When-not-to-use).
5. Network capability gating: optional observation with truthful SKIP / NO LIVE NETWORK OBSERVATION
   when network is unavailable or restricted.
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


def load_reference_assumptions(file_path: str | Path | None = None) -> dict:
    """Load committed reference assumptions from JSON file."""
    if file_path is None:
        file_path = Path(__file__).parent / "reference_assumptions.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def estimate_monthly_storage_cost(
    capacity_gb: float,
    write_requests: int = 0,
    read_requests: int = 0,
    egress_gb: float = 0.0,
    custom_assumptions: dict | None = None,
) -> dict:
    """Calculate parameterized monthly cost across Block, File, and Object storage tiers.

    Formula:
    Total Cost = (Capacity_GB * Storage_Rate) +
                 (Write_Requests / 1000 * Write_Rate) +
                 (Read_Requests / 1000 * Read_Rate) +
                 (Egress_GB * Egress_Rate)

    Omissions:
    This model explicitly OMITS: provisioned IOPS over baseline, volume snapshots,
    cross-region replication bandwidth, minimum object size padding (e.g. 128 KiB),
    and API error charges.
    """
    if capacity_gb < 0 or write_requests < 0 or read_requests < 0 or egress_gb < 0:
        raise ValueError("Workload numbers must be non-negative")
    if capacity_gb > 10_000_000:
        raise ValueError(f"capacity_gb ({capacity_gb}) exceeds safety bound")

    assumptions = custom_assumptions or load_reference_assumptions()
    tiers = assumptions["tiers"]

    # 1. Block Storage (EBS gp3 baseline)
    b_tier = tiers["block_storage"]
    b_storage_cost = capacity_gb * b_tier["storage_rate_per_gb_month"]
    # Block storage attached to compute incurs direct storage volume fees
    b_total = b_storage_cost

    # 2. File Storage (EFS Standard baseline)
    f_tier = tiers["file_storage"]
    f_storage_cost = capacity_gb * f_tier["storage_rate_per_gb_month"]
    f_total = f_storage_cost

    # 3. Object Storage (S3 Standard baseline)
    o_tier = tiers["object_storage"]
    o_storage_cost = capacity_gb * o_tier["storage_rate_per_gb_month"]
    o_write_cost = (write_requests / 1000.0) * o_tier.get("request_rate_per_1k_write", 0.0)
    o_read_cost = (read_requests / 1000.0) * o_tier.get("request_rate_per_1k_read", 0.0)
    o_egress_cost = egress_gb * o_tier.get("egress_rate_per_gb", 0.0)
    o_total = o_storage_cost + o_write_cost + o_read_cost + o_egress_cost

    return {
        "inputs": {
            "capacity_gb": capacity_gb,
            "write_requests": write_requests,
            "read_requests": read_requests,
            "egress_gb": egress_gb,
        },
        "block_storage": {
            "name": b_tier["name"],
            "storage_cost": round(b_storage_cost, 2),
            "total_monthly_cost": round(b_total, 2),
        },
        "file_storage": {
            "name": f_tier["name"],
            "storage_cost": round(f_storage_cost, 2),
            "total_monthly_cost": round(f_total, 2),
        },
        "object_storage": {
            "name": o_tier["name"],
            "storage_cost": round(o_storage_cost, 2),
            "write_request_cost": round(o_write_cost, 4),
            "read_request_cost": round(o_read_cost, 4),
            "egress_cost": round(o_egress_cost, 2),
            "total_monthly_cost": round(o_total, 2),
        },
        "explicit_omissions": [
            "provisioned_iops_and_burst_credits",
            "volume_snapshot_storage",
            "multi_region_replication_charges",
            "minimum_object_storage_duration_or_size_padding",
            "cross_availability_zone_interconnect_network_fees",
        ],
    }


def evaluate_storage_technology(arch_type: str) -> dict:
    """Apply the Technology Evaluation Framework to a storage architecture."""
    arch = arch_type.lower()
    framework = {
        "block": {
            "architecture": "Block Storage",
            "problem": "Provide low-latency raw block addressing for single-host operating systems and database engines.",
            "constraints": "Strict sub-millisecond random I/O latency requirements; fixed disk volume bounds.",
            "mechanism": "LBA sectors mapped over NVMe/SCSI or virtual SAN protocols to a single attached compute node.",
            "gains": "Maximum random I/O throughput, POSIX compatibility, in-place byte overwriting, direct filesystem hosting.",
            "costs": "Highest cost per GB-month (~$0.08 - $0.12/GB), non-elastic capacity provisioning, single-instance attachment.",
            "failure_modes": "Filesystem corruption on hard crash, volume unmount on hypervisor fault, noisy-neighbor shared SAN latency.",
            "when_not_to_use": "Do NOT use for shared multi-client read/write assets, distributed media archives, or massive petabyte-scale unstructured logs.",
        },
        "file": {
            "architecture": "File Storage",
            "problem": "Provide a concurrent, shared hierarchical directory tree for multiple independent compute nodes.",
            "constraints": "Standard POSIX file semantics (open, read, write, lock) required across multiple clients simultaneously.",
            "mechanism": "Centralized network filesystem server/cluster exporting POSIX hierarchy over NFS or SMB protocols.",
            "gains": "Seamless multi-instance sharing, automatic directory tree semantics, transparent client mounting.",
            "costs": "Medium-to-high cost (~$0.30/GB), network protocol roundtrip overhead (1-5 ms latency), lock contention bottlenecks.",
            "failure_modes": "Network partition hangs (stale NFS mounts), metadata lock deadlocks, metadata bottleneck on millions of tiny files.",
            "when_not_to_use": "Do NOT use for high-IOPS random transactional databases (e.g. database data directory) or massive internet-scale static assets.",
        },
        "object": {
            "architecture": "Object Storage",
            "problem": "Store and serve massive, petabyte-scale unstructured binary assets with elastic capacity at minimal cost.",
            "constraints": "High HTTP latency acceptable (20-100 ms); data accessed via keys rather than directory hierarchy.",
            "mechanism": "Flat key-value namespace; immutable binary blobs accessed via REST API (GET, PUT, DELETE) over HTTP/TLS.",
            "gains": "Lowest cost per GB (~$0.02/GB), infinite elastic scale, built-in multi-datacenter durability, global web URL access.",
            "costs": "Per-request charges (PUT/GET API fees), high egress bandwidth costs, no in-place mutation (must replace whole object).",
            "failure_modes": "Eventual consistency propagation delays (on older stores), high API request bills on small-file micro-access, egress bill shock.",
            "when_not_to_use": "Do NOT use as a boot volume, for low-latency random database read/writes, or for applications requiring POSIX file locks or in-place updates.",
        },
    }

    if arch not in framework:
        raise ValueError(f"Unknown architecture '{arch_type}'. Choose 'block', 'file', or 'object'.")
    return framework[arch]


def probe_public_http_object(target_url: str = "https://example.com", timeout: float = 3.0) -> dict:
    """Capability-gated HTTP observation. Truthfully reports SKIP if network is unavailable."""
    try:
        req = urllib.request.Request(
            target_url,
            method="HEAD",
            headers={"User-Agent": "Essential-CS-M09-Probe/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            headers = dict(resp.headers)
            return {
                "status": "PASS",
                "disposition": "LIVE_NETWORK_OBSERVATION",
                "url": target_url,
                "status_code": resp.status,
                "etag": headers.get("ETag"),
                "content_length": headers.get("Content-Length"),
                "content_type": headers.get("Content-Type"),
            }
    except Exception as e:
        return {
            "status": "SKIP",
            "disposition": "NO LIVE NETWORK OBSERVATION",
            "reason": f"Live network probe failed or network unavailable: {type(e).__name__}: {e}",
            "confirmation": "No fabricated network transcript generated.",
        }


def main() -> int:
    print("=== Essential CS M09 — Storage Economics & Evaluation (L09-03) ===")

    # 1. Parameterized Cost Estimation
    # Scenario: 10,000 GB (10 TB) capacity, 50,000 writes, 1,000,000 reads, 200 GB egress
    cost = estimate_monthly_storage_cost(
        capacity_gb=10000.0,
        write_requests=50000,
        read_requests=1000000,
        egress_gb=200.0,
    )
    print("\n[1] Monthly Cost Estimation (10 TB storage, 1M reads, 50K writes, 200 GB egress):")
    print(f"    -> Block Storage ({cost['block_storage']['name']}):   ${cost['block_storage']['total_monthly_cost']:.2f}")
    print(f"    -> File Storage  ({cost['file_storage']['name']}):    ${cost['file_storage']['total_monthly_cost']:.2f}")
    print(f"    -> Object Store  ({cost['object_storage']['name']}):   ${cost['object_storage']['total_monthly_cost']:.2f} (Storage=${cost['object_storage']['storage_cost']}, Requests=${cost['object_storage']['write_request_cost'] + cost['object_storage']['read_request_cost']:.2f}, Egress=${cost['object_storage']['egress_cost']})")
    print(f"    -> Explicit Omissions: {', '.join(cost['explicit_omissions'])}")

    # 2. Technology Evaluation Framework
    obj_eval = evaluate_storage_technology("object")
    print("\n[2] Technology Evaluation Framework (Object Storage Sample):")
    print(f"    -> Problem:         {obj_eval['problem']}")
    print(f"    -> Gains:           {obj_eval['gains']}")
    print(f"    -> When NOT to use: {obj_eval['when_not_to_use']}")

    # 3. Network Probe
    probe = probe_public_http_object()
    print("\n[3] Optional Network Probe Status:")
    print(f"    -> Disposition: {probe['disposition']}")
    if probe["status"] == "PASS":
        print(f"    -> ETag: {probe.get('etag')}, Status: {probe.get('status_code')}")
    else:
        print(f"    -> Reason: {probe.get('reason')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
