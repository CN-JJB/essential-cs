#!/usr/bin/env python3
"""
activity_l19_03.py
Essential CS: Stage 6 Module 19 (M19) Activity L19-03.

Hands-on activity: Deployment Strategies, Version Skew, and Expand-Contract Migrations.
Executes deterministic simulations of:
1. A rolling deployment with an uncoordinated schema rename causing version-skew crashes.
2. The Expand-Contract (Parallel Run) migration pattern preventing version-skew errors across
   transition, coexistence dual-writes, and post-contract phases.
3. Mutable tag references vs. immutable content digest identity and cryptographic trust boundaries.
"""

import hashlib
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CURRENT_DIR = Path(__file__).resolve().parent


# ==============================================================================
# PART 1: SERVICE INSTANCE & DATABASE SIMULATION
# ==============================================================================

class SimulatedDatabase:
    """
    In-memory SQLite database simulating a shared relational database.
    """

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE orders (
                    order_id TEXT PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
                """
            )
            self.conn.execute(
                "INSERT INTO orders (order_id, customer_name, phone) VALUES (?, ?, ?)",
                ("ORD-1001", "Alice Chen", "555-0101"),
            )
            self.conn.execute(
                "INSERT INTO orders (order_id, customer_name, phone) VALUES (?, ?, ?)",
                ("ORD-1002", "Bob Smith", "555-0102"),
            )

    def execute_raw(self, sql: str, params: Tuple = ()):
        with self.conn:
            return self.conn.execute(sql, params)

    def query_row(self, sql: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        cur = self.conn.cursor()
        try:
            cur.execute(sql, params)
            return cur.fetchone()
        finally:
            cur.close()

    def close(self):
        if hasattr(self, "conn") and self.conn:
            self.conn.close()
            self.conn = None

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass


class ServiceInstanceV1:
    """
    Version 1 application code: reads and writes the legacy 'phone' column.
    """

    def __init__(self, instance_id: str, db: SimulatedDatabase):
        self.instance_id = instance_id
        self.version = "v1.0"
        self.db = db

    def handle_get_order(self, order_id: str) -> Dict[str, Any]:
        try:
            row = self.db.query_row(
                "SELECT order_id, customer_name, phone FROM orders WHERE order_id = ?",
                (order_id,),
            )
            if not row:
                return {"status": 404, "error": "Order not found", "instance": self.instance_id, "version": self.version}
            return {
                "status": 200,
                "order_id": row["order_id"],
                "customer": row["customer_name"],
                "phone": row["phone"],
                "instance": self.instance_id,
                "version": self.version,
            }
        except Exception as e:
            return {
                "status": 500,
                "error": f"Internal Database Error: {type(e).__name__} ({e})",
                "instance": self.instance_id,
                "version": self.version,
            }

    def handle_create_order(self, order_id: str, customer_name: str, phone: str) -> Dict[str, Any]:
        try:
            self.db.execute_raw(
                "INSERT INTO orders (order_id, customer_name, phone) VALUES (?, ?, ?)",
                (order_id, customer_name, phone),
            )
            return {"status": 200, "order_id": order_id, "instance": self.instance_id, "version": self.version}
        except Exception as e:
            return {
                "status": 500,
                "error": f"Internal Database Error: {type(e).__name__} ({e})",
                "instance": self.instance_id,
                "version": self.version,
            }


class ServiceInstanceV2Broken:
    """
    Version 2 broken application code: expects 'contact_phone' column exclusively.
    """

    def __init__(self, instance_id: str, db: SimulatedDatabase):
        self.instance_id = instance_id
        self.version = "v2.0-broken"
        self.db = db

    def handle_get_order(self, order_id: str) -> Dict[str, Any]:
        try:
            row = self.db.query_row(
                "SELECT order_id, customer_name, contact_phone FROM orders WHERE order_id = ?",
                (order_id,),
            )
            if not row:
                return {"status": 404, "error": "Order not found", "instance": self.instance_id, "version": self.version}
            return {
                "status": 200,
                "order_id": row["order_id"],
                "customer": row["customer_name"],
                "phone": row["contact_phone"],
                "instance": self.instance_id,
                "version": self.version,
            }
        except Exception as e:
            return {
                "status": 500,
                "error": f"Internal Database Error: {type(e).__name__} ({e})",
                "instance": self.instance_id,
                "version": self.version,
            }


class ServiceInstanceV2Transition:
    """
    Version 2 Transition application code (used during coexistence Phase 2):
    - Reads 'contact_phone' if present, falls back to 'phone' if older rows lack it.
    - Writes BOTH 'phone' and 'contact_phone' (dual-write) so coexisting V1 instances can read newly created rows.
    """

    def __init__(self, instance_id: str, db: SimulatedDatabase):
        self.instance_id = instance_id
        self.version = "v2.0-transition"
        self.db = db

    def handle_get_order(self, order_id: str) -> Dict[str, Any]:
        try:
            row = self.db.query_row(
                "SELECT order_id, customer_name, phone, contact_phone FROM orders WHERE order_id = ?",
                (order_id,),
            )
            if not row:
                return {"status": 404, "error": "Order not found", "instance": self.instance_id, "version": self.version}
            phone_val = row["contact_phone"] if row["contact_phone"] is not None else row["phone"]
            return {
                "status": 200,
                "order_id": row["order_id"],
                "customer": row["customer_name"],
                "phone": phone_val,
                "instance": self.instance_id,
                "version": self.version,
            }
        except Exception as e:
            return {
                "status": 500,
                "error": f"Internal Database Error: {type(e).__name__} ({e})",
                "instance": self.instance_id,
                "version": self.version,
            }

    def handle_create_order(self, order_id: str, customer_name: str, phone: str) -> Dict[str, Any]:
        try:
            # Dual-write: write both legacy phone and new contact_phone
            self.db.execute_raw(
                "INSERT INTO orders (order_id, customer_name, phone, contact_phone) VALUES (?, ?, ?, ?)",
                (order_id, customer_name, phone, phone),
            )
            return {"status": 200, "order_id": order_id, "instance": self.instance_id, "version": self.version}
        except Exception as e:
            return {
                "status": 500,
                "error": f"Internal Database Error: {type(e).__name__} ({e})",
                "instance": self.instance_id,
                "version": self.version,
            }


class ServiceInstanceV2Final:
    """
    Version 2 Final application code (used in Phase 3/4 after Contract):
    - Completely decoupled from legacy 'phone' column.
    - Queries and inserts ONLY 'contact_phone'.
    """

    def __init__(self, instance_id: str, db: SimulatedDatabase):
        self.instance_id = instance_id
        self.version = "v2.0-final"
        self.db = db

    def handle_get_order(self, order_id: str) -> Dict[str, Any]:
        try:
            row = self.db.query_row(
                "SELECT order_id, customer_name, contact_phone FROM orders WHERE order_id = ?",
                (order_id,),
            )
            if not row:
                return {"status": 404, "error": "Order not found", "instance": self.instance_id, "version": self.version}
            return {
                "status": 200,
                "order_id": row["order_id"],
                "customer": row["customer_name"],
                "phone": row["contact_phone"],
                "instance": self.instance_id,
                "version": self.version,
            }
        except Exception as e:
            return {
                "status": 500,
                "error": f"Internal Database Error: {type(e).__name__} ({e})",
                "instance": self.instance_id,
                "version": self.version,
            }

    def handle_create_order(self, order_id: str, customer_name: str, phone: str) -> Dict[str, Any]:
        try:
            self.db.execute_raw(
                "INSERT INTO orders (order_id, customer_name, contact_phone) VALUES (?, ?, ?)",
                (order_id, customer_name, phone),
            )
            return {"status": 200, "order_id": order_id, "instance": self.instance_id, "version": self.version}
        except Exception as e:
            return {
                "status": 500,
                "error": f"Internal Database Error: {type(e).__name__} ({e})",
                "instance": self.instance_id,
                "version": self.version,
            }


# ==============================================================================
# PART 2: SIMULATING THE BREAKING ROLLING DEPLOYMENT
# ==============================================================================

def simulate_breaking_rolling_deployment() -> Dict[str, Any]:
    """
    Simulates a 3-node service pool undergoing a rolling update with an uncoordinated schema rename.
    Demonstrates version skew causing request failures.
    """
    db = SimulatedDatabase()

    pool: List[Any] = [
        ServiceInstanceV1("node-1", db),
        ServiceInstanceV1("node-2", db),
        ServiceInstanceV1("node-3", db),
    ]

    pre_results = [pool[i % 3].handle_get_order("ORD-1001") for i in range(3)]

    # BREAKING CHANGE IN DATABASE:
    db.execute_raw("ALTER TABLE orders RENAME COLUMN phone TO contact_phone")

    # Rolling update starts: node-1 is replaced with V2Broken
    pool[0] = ServiceInstanceV2Broken("node-1", db)

    # Traffic during version-skew window (6 customer requests distributed round-robin)
    skew_results = []
    for i in range(6):
        node = pool[i % 3]
        resp = node.handle_get_order("ORD-1001")
        skew_results.append({
            "request_idx": i + 1,
            "routed_node": node.instance_id,
            "node_version": node.version,
            "status": resp["status"],
            "error": resp.get("error"),
        })

    failures = [r for r in skew_results if r["status"] == 500]
    successes = [r for r in skew_results if r["status"] == 200]

    return {
        "scenario": "Breaking Rolling Update (Version Skew)",
        "pre_rollout_statuses": [r["status"] for r in pre_results],
        "version_skew_window_requests": skew_results,
        "total_requests": len(skew_results),
        "successful_requests": len(successes),
        "failed_requests": len(failures),
        "failure_rate_pct": round(len(failures) / len(skew_results) * 100.0, 2),
        "root_cause": (
            "Database column 'phone' was renamed to 'contact_phone' immediately. "
            "During the rolling deployment, surviving v1 instances continued querying 'SELECT phone', "
            "triggering fatal SQL errors (no such column: phone) on live customer traffic."
        ),
    }


# ==============================================================================
# PART 3: SIMULATING THE PROTECTED EXPAND-CONTRACT DEPLOYMENT
# ==============================================================================

def simulate_expand_contract_deployment() -> Dict[str, Any]:
    """
    Simulates the safe three-phase Expand-Contract pattern for database schema evolution:
    - Phase 1: Expand (add nullable contact_phone, backfill from phone).
    - Phase 2: Transition / Coexistence (V2Transition deployed with fallback-read and dual-write).
               Demonstrates deterministic write/read cross-compatibility between V1 and V2Transition.
    - Phase 3: Contract (all nodes upgraded to V2Final, drop legacy phone column).
    - Phase 4: Post-Contract requests evaluated and included in invariant calculations.
    """
    db = SimulatedDatabase()

    pool: List[Any] = [
        ServiceInstanceV1("node-1", db),
        ServiceInstanceV1("node-2", db),
        ServiceInstanceV1("node-3", db),
    ]

    all_evaluated_requests: List[Dict[str, Any]] = []

    # -------------------------------------------------------------
    # PHASE 1: EXPAND
    # Add new column 'contact_phone' as nullable.
    # -------------------------------------------------------------
    db.execute_raw("ALTER TABLE orders ADD COLUMN contact_phone TEXT")
    db.execute_raw("UPDATE orders SET contact_phone = phone")

    # -------------------------------------------------------------
    # PHASE 2: TRANSITION & COEXISTENCE
    # Step 2a: node-1 updated to V2Transition (1/3 V2, 2/3 V1)
    # -------------------------------------------------------------
    pool[0] = ServiceInstanceV2Transition("node-1", db)
    for i in range(3):
        node = pool[i % 3]
        resp = node.handle_get_order("ORD-1001")
        all_evaluated_requests.append({
            "phase": "Phase 2 (Coexistence 1/3 V2)",
            "routed_node": node.instance_id,
            "version": node.version,
            "op": "GET",
            "status": resp["status"],
        })

    # Deterministic write/read compatibility test during coexistence:
    # 1. V1 writes legacy record (only 'phone' populated, 'contact_phone' is NULL)
    v1_node = pool[1]  # node-2 running V1
    w1_resp = v1_node.handle_create_order("ORD-V1-NEW", "Charlie Day", "555-0103")
    all_evaluated_requests.append({
        "phase": "Phase 2 (Coexistence Write)",
        "routed_node": v1_node.instance_id,
        "version": v1_node.version,
        "op": "CREATE",
        "status": w1_resp["status"],
    })

    # 2. V2Transition reads V1's record: fallback/COALESCE handles NULL contact_phone
    v2_node = pool[0]  # node-1 running V2Transition
    r_v2_resp = v2_node.handle_get_order("ORD-V1-NEW")
    all_evaluated_requests.append({
        "phase": "Phase 2 (Coexistence Cross-Read: V2 reads V1 write)",
        "routed_node": v2_node.instance_id,
        "version": v2_node.version,
        "op": "GET",
        "status": r_v2_resp["status"],
    })

    # 3. V2Transition writes new record with dual-write (both phone and contact_phone populated)
    w2_resp = v2_node.handle_create_order("ORD-V2-NEW", "Diana Prince", "555-0104")
    all_evaluated_requests.append({
        "phase": "Phase 2 (Coexistence Write: V2 Dual-Write)",
        "routed_node": v2_node.instance_id,
        "version": v2_node.version,
        "op": "CREATE",
        "status": w2_resp["status"],
    })

    # 4. V1 reads V2Transition's record: legacy SELECT phone succeeds because V2 dual-wrote
    r_v1_resp = v1_node.handle_get_order("ORD-V2-NEW")
    all_evaluated_requests.append({
        "phase": "Phase 2 (Coexistence Cross-Read: V1 reads V2 dual-write)",
        "routed_node": v1_node.instance_id,
        "version": v1_node.version,
        "op": "GET",
        "status": r_v1_resp["status"],
    })

    # Step 2b: node-2 updated to V2Transition (2/3 V2, 1/3 V1)
    pool[1] = ServiceInstanceV2Transition("node-2", db)
    for i in range(3):
        node = pool[i % 3]
        resp = node.handle_get_order("ORD-1001")
        all_evaluated_requests.append({
            "phase": "Phase 2 (Coexistence 2/3 V2)",
            "routed_node": node.instance_id,
            "version": node.version,
            "op": "GET",
            "status": resp["status"],
        })

    # Step 2c: node-3 updated to V2Transition (3/3 V2Transition)
    pool[2] = ServiceInstanceV2Transition("node-3", db)
    for i in range(3):
        node = pool[i % 3]
        resp = node.handle_get_order("ORD-1001")
        all_evaluated_requests.append({
            "phase": "Phase 2 (100% V2Transition)",
            "routed_node": node.instance_id,
            "version": node.version,
            "op": "GET",
            "status": resp["status"],
        })

    # Backfill any remaining null contact_phone entries
    db.execute_raw("UPDATE orders SET contact_phone = phone WHERE contact_phone IS NULL")

    # Step 2d: All nodes upgraded to V2Final (decoupled from 'phone' column)
    pool = [
        ServiceInstanceV2Final("node-1", db),
        ServiceInstanceV2Final("node-2", db),
        ServiceInstanceV2Final("node-3", db),
    ]

    # -------------------------------------------------------------
    # PHASE 3: CONTRACT
    # Drop legacy 'phone' column
    # -------------------------------------------------------------
    db.execute_raw("ALTER TABLE orders DROP COLUMN phone")

    # -------------------------------------------------------------
    # PHASE 4: POST-CONTRACT VERIFICATION
    # Execute and tally post-contract read and write requests against V2Final
    # -------------------------------------------------------------
    post_contract_requests = []
    # Read existing orders
    for oid in ("ORD-1001", "ORD-V1-NEW", "ORD-V2-NEW"):
        for i in range(3):
            node = pool[i % 3]
            resp = node.handle_get_order(oid)
            item = {
                "phase": "Phase 4 (Post-Contract Read)",
                "routed_node": node.instance_id,
                "version": node.version,
                "op": f"GET {oid}",
                "status": resp["status"],
            }
            post_contract_requests.append(item)
            all_evaluated_requests.append(item)

    # Write new order post-contract
    post_write_resp = pool[0].handle_create_order("ORD-FINAL-1", "Eve Polastri", "555-0105")
    pw_item = {
        "phase": "Phase 4 (Post-Contract Write)",
        "routed_node": pool[0].instance_id,
        "version": pool[0].version,
        "op": "CREATE ORD-FINAL-1",
        "status": post_write_resp["status"],
    }
    post_contract_requests.append(pw_item)
    all_evaluated_requests.append(pw_item)

    # Read the newly written order post-contract
    post_read_resp = pool[1].handle_get_order("ORD-FINAL-1")
    pr_item = {
        "phase": "Phase 4 (Post-Contract Read New)",
        "routed_node": pool[1].instance_id,
        "version": pool[1].version,
        "op": "GET ORD-FINAL-1",
        "status": post_read_resp["status"],
    }
    post_contract_requests.append(pr_item)
    all_evaluated_requests.append(pr_item)

    failures = [r for r in all_evaluated_requests if r["status"] != 200]
    successes = [r for r in all_evaluated_requests if r["status"] == 200]
    failure_rate_pct = round(len(failures) / len(all_evaluated_requests) * 100.0, 2)

    return {
        "scenario": "Expand-Contract (Parallel Run) Deployment",
        "phase_1_expand": "Added contact_phone nullable, backfilled from phone",
        "phase_2_coexistence_requests": len(all_evaluated_requests) - len(post_contract_requests),
        "phase_3_contract": "Dropped legacy column phone after 100% v2 adoption",
        "phase_4_post_contract_requests": len(post_contract_requests),
        "all_requests": all_evaluated_requests,
        "total_requests": len(all_evaluated_requests),
        "successful_requests": len(successes),
        "failed_requests": len(failures),
        "failure_rate_pct": failure_rate_pct,
        "invariant_satisfied": (len(failures) == 0),
        "inference_limit": (
            "The Expand-Contract pattern prevents version-skew crashes under the contract "
            "that old and new versions remain mutually compatible with intermediate schema state. "
            "This fixture confirms 0 errors for this deterministic scenario, but does NOT constitute "
            "a universal zero-downtime guarantee for arbitrary network, hardware, or state failures."
        ),
    }


# ==============================================================================
# PART 4: MUTABLE TAG VS. CONTENT DIGEST & CRYPTOGRAPHIC TRUST
# ==============================================================================

def simulate_tag_vs_digest() -> Dict[str, Any]:
    """
    Demonstrates:
    1. Mutable tag references pointing to manifest digests.
    2. Content digest immutability under cryptographic hash algorithms (SHA-256 baseline;
       OCI Image Spec v1.1 also registers SHA-512 and BLAKE3).
    3. Content verification requirement: calculating hash and comparing with expected digest
       communicated over a secure channel.
    4. The fundamental 4-part boundary:
       digest identity/integrity evidence != signature verification != provenance/attestation != trust policy decision.
    """
    build_a_content = b"#!/bin/sh\necho 'Payment Service v1.0.0 (commit: a1b2c3d)'\n"
    digest_a = "sha256:" + hashlib.sha256(build_a_content).hexdigest()

    build_b_content = b"#!/bin/sh\necho 'Payment Service v1.0.0-patched (commit: e5f6a7b)'\n"
    digest_b = "sha256:" + hashlib.sha256(build_b_content).hexdigest()

    registry_tag_at_t0 = digest_a
    registry_tag_at_t1 = digest_b

    tag_was_mutated = (registry_tag_at_t0 != registry_tag_at_t1)

    return {
        "build_a": {
            "description": "Initial release commit a1b2c3d",
            "digest": digest_a,
        },
        "build_b": {
            "description": "Repointed release commit e5f6a7b",
            "digest": digest_b,
        },
        "tag_demonstration": {
            "tag_name": "payment-service:v1.0",
            "target_at_t0": registry_tag_at_t0,
            "target_at_t1": registry_tag_at_t1,
            "tag_repointed_and_mutable": tag_was_mutated,
            "policy_note": (
                "OCI registries allow tag mutability by default, though specific registries or "
                "repository policies may enforce tag immutability. Tags remain mutable references "
                "unless an explicit policy prevents modification."
            ),
        },
        "trust_boundary_analysis": {
            "digest_identity_evidence": (
                "A content digest (e.g. sha256:..., sha512:..., or blake3:...) identifies exact content "
                "bits under that hash function. Verification requires recalculating the digest and comparing "
                "it to an expected digest received over a secure/trusted channel."
            ),
            "signature_verification": (
                "Digital signatures (e.g. Cosign / Sigstore) prove that a specific cryptographic identity "
                "or key signed the artifact digest. It does NOT prove the code is benign or defect-free."
            ),
            "provenance_attestation": (
                "Provenance (e.g. SLSA attestations) provides verifiable evidence about build materials, "
                "source repository, builder identity, and environment. Provenance is evidence to be evaluated, "
                "not automatic proof of trustworthiness."
            ),
            "trust_policy_decision": (
                "An organization's admission control / runtime policy must evaluate signatures, identities, "
                "and provenance claims against defined trust roots and rules. Trust is a policy decision."
            ),
            "four_part_boundary_formula": (
                "digest identity/integrity evidence != signature verification != provenance/attestation != trust policy decision"
            ),
        },
    }


def run_activity(save_scratch: bool = True) -> int:
    print("=" * 76)
    print(" ESSENTIAL CS -- ACTIVITY L19-03: DEPLOYMENT STRATEGIES & VERSION SKEW")
    print(" Focus: Rolling Updates, Expand-Contract Migrations, & Trust Boundaries")
    print("=" * 76)

    # 1. Breaking Rolling Update Simulation
    print("\n[PART 1: The Broken Path -- Rolling Update with Immediate Column Rename]")
    breaking = simulate_breaking_rolling_deployment()
    print(f" Scenario:                   {breaking['scenario']}")
    print(f" Requests in Skew Window:    {breaking['total_requests']}")
    print(f" Successful Requests (200):  {breaking['successful_requests']}")
    print(f" Failed Requests (500):      {breaking['failed_requests']} ({breaking['failure_rate_pct']}% error spike)")
    print(" Trace of Requests During Version-Skew Window:")
    for r in breaking["version_skew_window_requests"]:
        status_symbol = "OK" if r["status"] == 200 else "FAIL"
        print(f"   [{status_symbol}] Req #{r['request_idx']}: routed to {r['routed_node']} ({r['node_version']}) -> HTTP {r['status']}")
        if r.get("error"):
            print(f"       Crash Reason: {r['error']}")
    print(f" Lesson: {breaking['root_cause']}")

    # 2. Protected Expand-Contract Deployment Simulation
    print("\n[PART 2: The Protected Path -- Expand-Contract (Parallel Run) Migration]")
    protected = simulate_expand_contract_deployment()
    print(f" Phase 1 (Expand):           {protected['phase_1_expand']}")
    print(f" Phase 2 (Coexistence):      {protected['phase_2_coexistence_requests']} requests (reads & dual-writes)")
    print(f" Phase 3 (Contract):         {protected['phase_3_contract']}")
    print(f" Phase 4 (Post-Contract):    {protected['phase_4_post_contract_requests']} requests (reads & writes on contracted schema)")
    print(f" Total Requests Evaluated:   {protected['total_requests']}")
    print(f" Total Failures Observed:    {protected['failed_requests']} (Observed Error Rate: {protected['failure_rate_pct']}%)")
    print(f" Invariant Satisfied:        {protected['invariant_satisfied']}")
    print(f" Inference Scope:            Scoped to this deterministic scenario; not a universal zero-downtime guarantee.")

    # 3. Content Digest vs Mutable Tag
    print("\n[PART 3: Content Digest vs. Mutable Tag & Cryptographic Trust]")
    trust = simulate_tag_vs_digest()
    tag_demo = trust["tag_demonstration"]
    print(f" Tag Tested:                 {tag_demo['tag_name']}")
    print(f" Tag Target at T0:           {tag_demo['target_at_t0'][:32]}...")
    print(f" Tag Target at T1:           {tag_demo['target_at_t1'][:32]}... (Repointed: {tag_demo['tag_repointed_and_mutable']})")
    print(f" Tag Policy Note:            {tag_demo['policy_note']}")

    tb = trust["trust_boundary_analysis"]
    print("\n Cryptographic Trust Boundary Formula:")
    print(f" -> {tb['four_part_boundary_formula']}")
    print(f" 1. Digest Evidence:         {tb['digest_identity_evidence'][:90]}...")
    print(f" 2. Signature Verification:  {tb['signature_verification'][:90]}...")
    print(f" 3. Provenance Attestation:  {tb['provenance_attestation'][:90]}...")
    print(f" 4. Trust Policy Decision:   {tb['trust_policy_decision'][:90]}...")

    # 4. Save scratch artifact
    if save_scratch:
        scratch_dir = CURRENT_DIR / ".scratch"
        try:
            scratch_dir.mkdir(parents=True, exist_ok=True)
            out_file = scratch_dir / "l19_03_deployment.json"
            combined_report = {
                "breaking_simulation": breaking,
                "expand_contract_simulation": protected,
                "trust_demonstration": trust,
            }
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(combined_report, f, indent=2, ensure_ascii=False)
            print(f"\n[Artifact Saved]: {out_file.relative_to(CURRENT_DIR)}")
        except Exception as e:
            print(f"\n[Notice]: Could not write scratch artifact: {e}")

    print("=" * 76)
    return 0


if __name__ == "__main__":
    sys.exit(run_activity())
