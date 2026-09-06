#!/usr/bin/env python3
"""
Activity L18-02: Do I Need a Distributor?
Demonstrates:
- Part 1: Classic Two-Phase Commit (2PC) blocking uncertainty in PREPARED state,
          plus proof that voting NO allows safe unilateral abort.
- Part 2: Saga 3-step scenario failure, intermediate dirty-read observation,
          and configured reverse-order compensating transactions.
- Part 3: Distributed lease expiry during client pause and fencing token rejection
          at the protected resource boundary.
"""

import datetime
import json
import os
import sys

from coordination_trace import (
    CourseSagaScenario,
    FencedStorageEngine,
    LeaseLockService,
    TwoPhaseCommitCoordinator,
    TwoPhaseCommitParticipant,
    TwoPhaseDecision,
    TwoPhaseVote,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = os.path.join(BASE_DIR, ".scratch")
OBSERVATION_FILE = os.path.join(SCRATCH_DIR, "l18_02_observation.json")


def run_activity_l18_02() -> dict:
    os.makedirs(SCRATCH_DIR, exist_ok=True)
    observation = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "activity": "L18-02",
    }

    print("=" * 80)
    print(" ESSENTIAL CS — ACTIVITY L18-02: 2PC, SAGAS & FENCING TOKENS")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # PART 1: Classic Two-Phase Commit (2PC)
    # -------------------------------------------------------------------------
    print("\n--- PART 1: Two-Phase Commit (2PC) Prepared Participant Uncertainty ---")
    p1 = TwoPhaseCommitParticipant("Bank_A")
    p2 = TwoPhaseCommitParticipant("Bank_B")
    coord = TwoPhaseCommitCoordinator([p1, p2])

    # Both vote YES; Coordinator decides COMMIT, but crashes before delivering to Bank_A
    votes = {"Bank_A": TwoPhaseVote.YES, "Bank_B": TwoPhaseVote.YES}
    trace_res = coord.execute_transaction(votes, crash_before_delivery_to=["Bank_A"])

    p1_report = trace_res["participants"]["Bank_A"]
    p2_report = trace_res["participants"]["Bank_B"]

    print(f" Coordinator Durable Decision: {trace_res['durable_log_decision']}")
    print(f" Delivery status:              {trace_res['delivered']}")
    print(f" Bank_B (Received decision):   State={p2_report['state']}, Disposition={p2_report['disposition']}")
    print(f" Bank_A (Decision missing):    State={p1_report['state']}")
    print(f"   Can unilaterally commit?    {p1_report['can_unilaterally_commit']}")
    print(f"   Can unilaterally abort?     {p1_report['can_unilaterally_abort']}")
    print(f"   Disposition:                {p1_report['disposition']}")
    print(f"   Reason:                     {p1_report['reason']}")

    # Contrast scenario: If Bank_A votes NO, can it abort unilaterally?
    p_no = TwoPhaseCommitParticipant("Bank_Rejecter")
    coord_no = TwoPhaseCommitCoordinator([p_no])
    res_no = coord_no.execute_transaction({"Bank_Rejecter": TwoPhaseVote.NO}, crash_before_delivery_to=["Bank_Rejecter"])
    p_no_report = res_no["participants"]["Bank_Rejecter"]

    print("\n [CONTRAST CASE: Participant Votes NO]")
    print(f"   Bank_Rejecter State:        {p_no_report['state']}")
    print(f"   Can unilaterally abort?     {p_no_report['can_unilaterally_abort']}")
    print(f"   Disposition:                {p_no_report['disposition']}")
    print("   Takeaway:                   Not every coordinator crash blocks everyone forever;")
    print("                               a participant that voted NO can abort safely.")

    observation["part1_2pc"] = {
        "scenario_1_prepared_uncertainty": {
            "participant": "Bank_A",
            "state": p1_report["state"],
            "can_unilaterally_commit": p1_report["can_unilaterally_commit"],
            "can_unilaterally_abort": p1_report["can_unilaterally_abort"],
            "disposition": p1_report["disposition"],
        },
        "scenario_2_vote_no_abort": {
            "participant": "Bank_Rejecter",
            "state": p_no_report["state"],
            "can_unilaterally_abort": p_no_report["can_unilaterally_abort"],
            "disposition": p_no_report["disposition"],
        },
    }

    # -------------------------------------------------------------------------
    # PART 2: Saga Pattern & Lack of Isolation
    # -------------------------------------------------------------------------
    print("\n--- PART 2: Saga Pattern (3 Steps, Failure at Step 3 & Intermediate Visibility) ---")
    saga = CourseSagaScenario(initial_stock=10)
    saga_res = saga.execute_saga(order_id="ord-saga-303", fail_at_step3=True, inspect_between_step2_and_3=True)

    print(f" Completed Steps:              {saga_res.completed_steps}")
    print(f" Failed Step:                  {saga_res.failed_step} ({saga_res.failure_reason})")
    print(f" Compensations Executed:       {saga_res.compensated_steps} (in reverse order: Step 2 -> Step 1)")
    print(f" Final System State:           {saga_res.final_state}")

    print("\n [INTERMEDIATE STATE ANOMALY (DIRTY READ)]")
    obs_dict = saga_res.intermediate_state_observed
    print(f"   Checkpoint:                 {obs_dict['checkpoint']}")
    print(f"   Order Status Observed:      {obs_dict['order_status']}")
    print(f"   Stock Observed:             {obs_dict['stock_observed']} (decremented from 10 to 9 before payment failed!)")
    print(f"   Explanation:                {obs_dict['explanation']}")
    print("   Takeaway:                   Sagas lack Isolation (I in ACID). Later compensation")
    print("                               does not erase the fact that intermediate state was observed.")

    observation["part2_saga"] = {
        "completed_steps": saga_res.completed_steps,
        "failed_step": saga_res.failed_step,
        "failure_reason": saga_res.failure_reason,
        "compensated_steps": saga_res.compensated_steps,
        "intermediate_observation": obs_dict,
        "final_state": saga_res.final_state,
    }

    # -------------------------------------------------------------------------
    # PART 3: Distributed Leases & Monotonically Increasing Fencing Tokens
    # -------------------------------------------------------------------------
    print("\n--- PART 3: Distributed Leases & Storage Fencing Tokens ---")
    lock_service = LeaseLockService()
    storage = FencedStorageEngine()

    # Step 1: Client 1 acquires lease
    lease_c1 = lock_service.acquire_lease(holder="Client_1")
    print(f" 1. Client 1 acquires lock lease: Token = {lease_c1.token}")

    # Step 2: Client 1 pauses (GC pause / network stall)
    print(" 2. Client 1 enters simulated 15s GC pause...")

    # Step 3: Lease expires in lock service
    lock_service.expire_lease(lease_c1)
    print(" 3. Lock service expires Client 1's lease after TTL.")

    # Step 4: Client 2 acquires lease
    lease_c2 = lock_service.acquire_lease(holder="Client_2")
    print(f" 4. Client 2 acquires lock lease: Token = {lease_c2.token}")

    # Step 5: Client 2 writes to storage with Token 2
    c2_write = storage.write(
        key="config/primary_node",
        value="node-2.cluster.local",
        presented_token=lease_c2.token,
        client_id="Client_2",
    )
    print(f" 5. Client 2 writes to storage: Action = {c2_write['action']}, Highest Token = {c2_write['highest_token']}")

    # Step 6: Client 1 wakes up from pause and attempts write with Token 1
    print(f" 6. Client 1 wakes up, assumes lease still valid, attempts write with Token = {lease_c1.token}...")
    c1_write = storage.write(
        key="config/primary_node",
        value="node-1.cluster.local (STALE OVERWRITE)",
        presented_token=lease_c1.token,
        client_id="Client_1",
    )
    print(f" 7. Storage evaluation for Client 1: Action = {c1_write['action']}")
    print(f"    Reason: {c1_write.get('reason')}")

    fencing_passed = (
        c2_write["action"] == "ACCEPT_WRITE"
        and c1_write["action"] == "REJECT_STALE_WRITE"
        and storage.records.get("config/primary_node") == "node-2.cluster.local"
    )

    if fencing_passed:
        print("\n [VERIFICATION PASS] Fencing token protected storage against split-brain stale write!")
        print("   Storage rejected token 1 because highest_token was already 2.")
        print("   Takeaway: Fencing tokens move validation to the resource boundary.")

    observation["part3_fencing"] = {
        "client_1_token": lease_c1.token,
        "client_2_token": lease_c2.token,
        "client_2_write_action": c2_write["action"],
        "client_1_write_action": c1_write["action"],
        "storage_highest_token": storage.highest_token,
        "final_storage_value": storage.records.get("config/primary_node"),
        "fencing_invariant_held": fencing_passed,
    }

    # Save observation JSON
    with open(OBSERVATION_FILE, "w", encoding="utf-8") as f:
        json.dump(observation, f, indent=2, ensure_ascii=False)

    print(f"\nSaved observation record to: {OBSERVATION_FILE}")
    print("=" * 80)
    return observation


if __name__ == "__main__":
    run_activity_l18_02()
