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
    metadata = assumptions.get("metadata", {})

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
    free_egress_gb = o_tier.get("egress_free_gb_assumed", 0.0)
    billable_egress_gb = max(0.0, egress_gb - free_egress_gb)
    o_egress_cost = billable_egress_gb * o_tier.get("egress_rate_per_gb", 0.0)
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
            "egress_input_gb": egress_gb,
            "egress_free_gb_assumed": free_egress_gb,
            "egress_billable_gb": billable_egress_gb,
            "egress_cost": round(o_egress_cost, 2),
            "total_monthly_cost": round(o_total, 2),
        },
        "assumption_metadata": {
            "status": metadata.get("status"),
            "checked_date": metadata.get("checked_date"),
            "currency": metadata.get("currency"),
            "region": metadata.get("region"),
            "note": metadata.get("note"),
        },
        "explicit_omissions": [
            "provisioned_iops_and_burst_credits",
            "volume_snapshot_storage",
            "multi_region_replication_charges",
            "minimum_object_storage_duration_or_size_padding",
            "cross_availability_zone_interconnect_network_fees",
            "account_wide_free_egress_consumed_by_other_services",
            "tiered_egress_rates_above_the_first_pricing_band",
            "efs_throughput_or_access_charges",
        ],
    }


def evaluate_storage_technology(arch_type: str) -> dict:
    """Apply the Technology Evaluation Framework to a storage architecture."""
    arch = arch_type.lower()
    framework = {
        "block": {
            "architecture": "Block Storage",
            "problem": "Provide low-latency raw block addressing for single-host operating systems and database engines.",
            "constraints": "Workload may require block semantics, predictable synchronization behavior, bounded latency, and explicit volume/service quotas; exact latency is product/workload-specific.",
            "mechanism": "Block-addressed storage exposed locally or over a storage service/protocol; attachment may be single-host or coordinated multi-attach depending on product.",
            "gains": "Provides block semantics suitable for hosting filesystems and storage engines; performance can be provisioned/tuned independently on some products.",
            "costs": "Capacity plus possible IOPS/throughput/snapshot/attachment charges; provisioning and scaling behavior depend on the selected product.",
            "failure_modes": "Device/service loss, attachment failures, filesystem/storage-engine crash recovery, quota exhaustion, and latency variation according to the deployed stack.",
            "when_not_to_use": "Avoid when the primary requirement is shared file semantics across many clients or service-managed object/key access rather than direct block semantics.",
        },
        "file": {
            "architecture": "File Storage",
            "problem": "Provide a concurrent, shared hierarchical directory tree for multiple independent compute nodes.",
            "constraints": "Applications may require hierarchical path/file semantics and multi-client access; exact POSIX/locking/cache semantics depend on protocol and service.",
            "mechanism": "Centralized network filesystem server/cluster exporting POSIX hierarchy over NFS or SMB protocols.",
            "gains": "Hierarchical naming and file-oriented APIs can simplify shared content/workspace use cases across clients.",
            "costs": "Capacity plus possible throughput/access/tiering/network charges; remote filesystems add network/cache/coordination paths whose latency must be measured.",
            "failure_modes": "Network partition hangs (stale NFS mounts), metadata lock deadlocks, metadata bottleneck on millions of tiny files.",
            "when_not_to_use": "Avoid when the workload's correctness/performance assumptions require different block/database semantics, or when API/object delivery fits the data and cost model better than shared file semantics.",
        },
        "object": {
            "architecture": "Object Storage",
            "problem": "Store and serve large collections of unstructured objects through a service API with independently scalable capacity/request handling.",
            "constraints": "Application can use object/key APIs rather than assuming POSIX byte-range mutation, file locks, or local-filesystem latency.",
            "mechanism": "Object/key + metadata API, commonly over HTTP/TLS; updates are typically whole-object replacement/versioning rather than POSIX in-place byte mutation.",
            "gains": "Can offer large-scale managed capacity, service-level durability/availability options, and direct API integration; exact guarantees and costs are product-specific.",
            "costs": "Capacity, request, data-transfer, retrieval/tiering and lifecycle charges may apply; POSIX adapters can add semantic/performance trade-offs.",
            "failure_modes": "Provider/service outages, quota/throttling, consistency/versioning mistakes, request-cost amplification, egress cost, and application assumptions that mismatch object semantics.",
            "when_not_to_use": "Avoid when the application requires boot/block-device semantics, POSIX file locking, in-place byte mutation, or very low predictable random-I/O latency not provided by the chosen object service.",
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
