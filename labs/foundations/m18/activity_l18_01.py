#!/usr/bin/env python3
"""
Activity L18-01: How Do Services Delegate Work?
Demonstrates:
- Part 1: Broken Dual-Write divergence under uncoordinated crash.
- Part 2: Transactional Outbox atomic staging in a single SQLite transaction.
- Part 3: Relay crash-before-mark fault injection causing duplicate delivery on retry.
- Part 4: Scoped duplicate-safe worker deduplication transaction.
"""

import datetime
import json
import os
import sqlite3
import sys

from outbox_fixture import (
    DeliveryBuffer,
    DualWriteCrashError,
    OutboxRelay,
    RelayCrashBeforeMarkError,
    Worker,
    init_database,
    produce_broken_dual_write,
    produce_transactional_outbox,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = os.path.join(BASE_DIR, ".scratch")
DB_PATH = os.path.join(SCRATCH_DIR, "m18_outbox.db")
OBSERVATION_FILE = os.path.join(SCRATCH_DIR, "l18_01_observation.json")


def run_activity_l18_01() -> dict:
    os.makedirs(SCRATCH_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except OSError:
            pass

    init_database(DB_PATH)
    observation = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "activity": "L18-01",
    }

    print("=" * 80)
    print(" ESSENTIAL CS — ACTIVITY L18-01: TRANSACTIONAL OUTBOX & DEDUPLICATION")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # PART 1: The Broken Dual-Write Divergence
    # -------------------------------------------------------------------------
    print("\n--- PART 1: Broken Dual-Write (DB Commit, Crash Pre-Enqueue) ---")
    buffer = DeliveryBuffer()
    dual_write_order_id = "ord-broken-101"
    divergence_detected = False

    try:
        produce_broken_dual_write(
            db_path=DB_PATH,
            order_id=dual_write_order_id,
            customer="Alice",
            item="Mechanical Keyboard",
            amount=149.99,
            buffer=buffer,
            fail_before_enqueue=True,
        )
    except DualWriteCrashError as exc:
        print(f" [INJECTED CRASH] {exc}")

    # Inspect SQLite database vs delivery buffer
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, customer, amount, status FROM orders WHERE id = ?", (dual_write_order_id,))
    db_order_row = cur.fetchone()
    conn.close()

    buffer_count = buffer.size()
    if db_order_row is not None and buffer_count == 0:
        divergence_detected = True
        print(" [OBSERVATION] State Divergence Manifested!")
        print(f"   Database State:        Order '{dual_write_order_id}' is COMMITTED in orders table.")
        print("   Delivery Buffer State: 0 messages enqueued (delivery action missing).")
        print("   Consequence:           Customer is charged/recorded, but fulfillment/notification is LOST.")

    observation["part1_broken_dual_write"] = {
        "order_id": dual_write_order_id,
        "db_row_committed": db_order_row is not None,
        "buffer_messages_count": buffer_count,
        "divergence_manifested": divergence_detected,
    }

    # -------------------------------------------------------------------------
    # PART 2: Transactional Outbox Atomic Staging
    # -------------------------------------------------------------------------
    print("\n--- PART 2: Transactional Outbox Atomic Staging (BEGIN IMMEDIATE) ---")
    outbox_order_id = "ord-outbox-202"
    event_id = "evt-ord-202"

    order_res, evt_res = produce_transactional_outbox(
        db_path=DB_PATH,
        order_id=outbox_order_id,
        customer="Bob",
        item="4K Monitor",
        amount=399.00,
        event_id=event_id,
    )
    print(f" [ATOMIC COMMIT] Staged order '{order_res}' and outbox event '{evt_res}' in same transaction.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, status FROM orders WHERE id = ?", (outbox_order_id,))
    outbox_order_row = cur.fetchone()
    cur.execute("SELECT id, event_type, dispatched FROM outbox_events WHERE id = ?", (event_id,))
    outbox_event_row = cur.fetchone()
    conn.close()

    print(f"   Orders Table:   {outbox_order_row}")
    print(f"   Outbox Table:   {outbox_event_row} (dispatched=0, pending relay)")

    observation["part2_transactional_outbox"] = {
        "order_id": outbox_order_id,
        "event_id": event_id,
        "order_committed": outbox_order_row is not None,
        "outbox_committed": outbox_event_row is not None,
        "dispatched_flag": outbox_event_row[2] if outbox_event_row else None,
    }

    # -------------------------------------------------------------------------
    # PART 3: Relay Deliver-Before-Mark Failure (Inducing Redelivery)
    # -------------------------------------------------------------------------
    print("\n--- PART 3: Relay Crash-Before-Mark (At-Least-Once Redelivery) ---")
    worker = Worker(db_path=DB_PATH)
    relay = OutboxRelay(db_path=DB_PATH, worker=worker)

    relay_crash_occurred = False
    try:
        relay.relay_pending(simulate_crash_on_event_id=event_id)
    except RelayCrashBeforeMarkError as exc:
        relay_crash_occurred = True
        print(f" [INJECTED CRASH] {exc}")

    # Verify worker received and applied effect, but outbox row still has dispatched=0
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT dispatched FROM outbox_events WHERE id = ?", (event_id,))
    dispatched_status_after_crash = cur.fetchone()[0]
    cur.execute("SELECT status FROM fulfillments WHERE order_id = ?", (outbox_order_id,))
    fulfillment_status_after_first = cur.fetchone()
    conn.close()

    print(f"   Worker Delivery Attempts:     {worker.delivery_attempts}")
    print(f"   Worker Applied Effects:       {worker.applied_effects}")
    print(f"   Outbox dispatched status:     {dispatched_status_after_crash} (remains 0 due to crash!)")
    print(f"   Fulfillments table status:    {fulfillment_status_after_first}")

    observation["part3_relay_crash"] = {
        "relay_crash_occurred": relay_crash_occurred,
        "worker_delivery_attempts": worker.delivery_attempts,
        "worker_applied_effects": worker.applied_effects,
        "outbox_dispatched_flag": dispatched_status_after_crash,
    }

    # -------------------------------------------------------------------------
    # PART 4: Worker Deduplication on Relay Retry
    # -------------------------------------------------------------------------
    print("\n--- PART 4: Relay Retry & Scoped Worker Deduplication ---")
    # Relay restarts and scans undispatched events again
    dispatches = relay.relay_pending(simulate_crash_on_event_id=None)
    print(f" [RELAY RECOVERED] Successfully processed {len(dispatches)} events.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT dispatched FROM outbox_events WHERE id = ?", (event_id,))
    final_dispatched = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM fulfillments WHERE order_id = ?", (outbox_order_id,))
    fulfillment_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM processed_events WHERE msg_id = ?", (event_id,))
    processed_count = cur.fetchone()[0]
    conn.close()

    print(f"   Total Delivery Attempts:      {worker.delivery_attempts} (attempted 2 times)")
    print(f"   Duplicate Suppressions:       {worker.duplicate_suppressions} (suppressed 1 duplicate)")
    print(f"   Total Applied Effects:        {worker.applied_effects} (exactly 1 fulfillment effect applied)")
    print(f"   Fulfillments Row Count:       {fulfillment_count}")
    print(f"   Processed Events Row Count:   {processed_count}")
    print(f"   Outbox dispatched final:      {final_dispatched}")

    dedup_successful = (
        worker.delivery_attempts == 2
        and worker.duplicate_suppressions == 1
        and worker.applied_effects == 1
        and fulfillment_count == 1
    )

    if dedup_successful:
        print("\n [VERIFICATION PASS] Deduplication contract held!")
        print("   Worker claim + business effect were executed in ONE transaction.")
        print("   Duplicate delivery was safely suppressed without duplicate fulfillment.")

    observation["part4_worker_dedup"] = {
        "total_delivery_attempts": worker.delivery_attempts,
        "duplicate_suppressions": worker.duplicate_suppressions,
        "total_applied_effects": worker.applied_effects,
        "fulfillment_count": fulfillment_count,
        "processed_count": processed_count,
        "final_dispatched_flag": final_dispatched,
        "dedup_contract_held": dedup_successful,
    }

    # Save observation JSON
    with open(OBSERVATION_FILE, "w", encoding="utf-8") as f:
        json.dump(observation, f, indent=2, ensure_ascii=False)

    print(f"\nSaved observation record to: {OBSERVATION_FILE}")
    print("=" * 80)
    return observation


if __name__ == "__main__":
    run_activity_l18_01()
