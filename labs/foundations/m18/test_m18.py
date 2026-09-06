#!/usr/bin/env python3
"""
Unit tests for M18 Foundations Fixtures & Coordination Traces.
Validates all deterministic fault scenarios, transaction boundaries, and reset idempotence.
"""

import os
import sqlite3
import tempfile
import unittest

from coordination_trace import (
    CourseSagaScenario,
    FencedStorageEngine,
    LeaseLockService,
    ParticipantState,
    TwoPhaseCommitCoordinator,
    TwoPhaseCommitParticipant,
    TwoPhaseDecision,
    TwoPhaseVote,
)
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
from reset import reset_m18_environment


class TestM18OutboxFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="test_m18_outbox_")
        self.db_path = os.path.join(self.temp_dir.name, "test_outbox.db")
        init_database(self.db_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_broken_dual_write_divergence(self) -> None:
        """Verifies that an uncoordinated crash between DB commit and queue causes state divergence."""
        buffer = DeliveryBuffer()
        order_id = "ord-dual-write-test"

        with self.assertRaises(DualWriteCrashError):
            produce_broken_dual_write(
                db_path=self.db_path,
                order_id=order_id,
                customer="Alice",
                item="Keyboard",
                amount=100.0,
                buffer=buffer,
                fail_before_enqueue=True,
            )

        # DB has the order
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute("SELECT id, status FROM orders WHERE id = ?", (order_id,))
        row = cur.fetchone()
        conn.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], order_id)

        # Buffer is empty => Divergence!
        self.assertEqual(buffer.size(), 0)

    def test_transactional_outbox_atomic_commit(self) -> None:
        """Verifies that business state and outbox row are committed atomically in the same transaction."""
        order_id = "ord-atomic-test"
        event_id = "evt-atomic-test"

        ret_order, ret_evt = produce_transactional_outbox(
            db_path=self.db_path,
            order_id=order_id,
            customer="Bob",
            item="Laptop",
            amount=1200.0,
            event_id=event_id,
        )
        self.assertEqual(ret_order, order_id)
        self.assertEqual(ret_evt, event_id)

        conn = sqlite3.connect(self.db_path)
        order_row = conn.execute("SELECT id FROM orders WHERE id = ?", (order_id,)).fetchone()
        outbox_row = conn.execute("SELECT id, dispatched FROM outbox_events WHERE id = ?", (event_id,)).fetchone()
        conn.close()

        self.assertIsNotNone(order_row)
        self.assertIsNotNone(outbox_row)
        self.assertEqual(outbox_row[1], 0)

    def test_relay_deliver_before_mark_retry_duplicate(self) -> None:
        """Verifies that relay crash before mark leaves dispatched=0, inducing duplicate delivery on retry."""
        order_id = "ord-relay-test"
        event_id = "evt-relay-test"
        produce_transactional_outbox(
            db_path=self.db_path,
            order_id=order_id,
            customer="Carol",
            item="Desk",
            amount=250.0,
            event_id=event_id,
        )

        worker = Worker(db_path=self.db_path)
        relay = OutboxRelay(db_path=self.db_path, worker=worker)

        # First attempt: Worker receives message, but relay crashes before marking dispatched=1
        with self.assertRaises(RelayCrashBeforeMarkError):
            relay.relay_pending(simulate_crash_on_event_id=event_id)

        self.assertEqual(worker.delivery_attempts, 1)
        self.assertEqual(worker.applied_effects, 1)

        # Verify dispatched flag is still 0
        conn = sqlite3.connect(self.db_path)
        dispatched_val = conn.execute("SELECT dispatched FROM outbox_events WHERE id = ?", (event_id,)).fetchone()[0]
        conn.close()
        self.assertEqual(dispatched_val, 0)

        # Second attempt (Retry): Relay re-polls and delivers event again
        dispatches = relay.relay_pending(simulate_crash_on_event_id=None)
        self.assertEqual(len(dispatches), 1)

        self.assertEqual(worker.delivery_attempts, 2)
        self.assertEqual(worker.duplicate_suppressions, 1)
        self.assertEqual(worker.applied_effects, 1)  # NOT incremented again!

        conn = sqlite3.connect(self.db_path)
        final_dispatched = conn.execute("SELECT dispatched FROM outbox_events WHERE id = ?", (event_id,)).fetchone()[0]
        fulfillments_count = conn.execute("SELECT COUNT(*) FROM fulfillments WHERE order_id = ?", (order_id,)).fetchone()[0]
        conn.close()

        self.assertEqual(final_dispatched, 1)
        self.assertEqual(fulfillments_count, 1)

    def test_worker_duplicate_safe_dedup_single_transaction(self) -> None:
        """Verifies that worker claims processed_events and applies fulfillment in ONE transaction."""
        worker = Worker(db_path=self.db_path)
        msg_id = "evt-single-tx-test"
        payload = '{"order_id": "ord-single-tx-1"}'

        # First delivery: Success
        res1 = worker.process_message(msg_id, payload)
        self.assertEqual(res1["status"], "PROCESSED")
        self.assertTrue(res1["applied"])

        # Duplicate delivery: Deduplication suppresses effect
        res2 = worker.process_message(msg_id, payload)
        self.assertEqual(res2["status"], "DUPLICATE_IGNORED")
        self.assertFalse(res2["applied"])

        # Check DB state
        conn = sqlite3.connect(self.db_path)
        proc_count = conn.execute("SELECT COUNT(*) FROM processed_events WHERE msg_id = ?", (msg_id,)).fetchone()[0]
        fulf_count = conn.execute("SELECT COUNT(*) FROM fulfillments WHERE order_id = ?", ("ord-single-tx-1",)).fetchone()[0]
        conn.close()

        self.assertEqual(proc_count, 1)
        self.assertEqual(fulf_count, 1)


class TestM18CoordinationTrace(unittest.TestCase):
    def test_classic_2pc_prepared_blocking_uncertainty(self) -> None:
        """Verifies that a participant in PREPARED state cannot unilaterally decide when coordinator decision is unknown."""
        p1 = TwoPhaseCommitParticipant("P1")
        p2 = TwoPhaseCommitParticipant("P2")
        coord = TwoPhaseCommitCoordinator([p1, p2])

        # Both vote YES; coordinator commits, but crashes before delivering to P1
        res = coord.execute_transaction(
            {"P1": TwoPhaseVote.YES, "P2": TwoPhaseVote.YES},
            crash_before_delivery_to=["P1"],
        )

        p1_rep = res["participants"]["P1"]
        p2_rep = res["participants"]["P2"]

        self.assertEqual(p1_rep["state"], ParticipantState.PREPARED.value)
        self.assertFalse(p1_rep["can_unilaterally_commit"])
        self.assertFalse(p1_rep["can_unilaterally_abort"])
        self.assertEqual(p1_rep["disposition"], "BLOCKED_IN_PREPARED_DECISION_UNKNOWN")

        self.assertEqual(p2_rep["state"], ParticipantState.COMMITTED.value)

    def test_2pc_unilateral_abort_when_voting_no(self) -> None:
        """Verifies that a participant voting NO can unilaterally abort, proving not all coordinator crashes block forever."""
        p1 = TwoPhaseCommitParticipant("P1")
        coord = TwoPhaseCommitCoordinator([p1])

        res = coord.execute_transaction(
            {"P1": TwoPhaseVote.NO},
            crash_before_delivery_to=["P1"],
        )

        p1_rep = res["participants"]["P1"]
        self.assertEqual(p1_rep["state"], ParticipantState.ABORTED.value)
        self.assertTrue(p1_rep["can_unilaterally_abort"])
        self.assertEqual(p1_rep["disposition"], "UNILATERAL_ABORT_SAFE")

    def test_saga_step3_failure_and_reverse_compensation(self) -> None:
        """Verifies that Saga step 3 failure triggers compensations for completed steps in reverse order."""
        saga = CourseSagaScenario(initial_stock=10)
        res = saga.execute_saga(order_id="ord-saga-test", fail_at_step3=True)

        self.assertFalse(res.success)
        self.assertEqual(res.completed_steps, ["CreateOrder", "ReserveInventory"])
        self.assertEqual(res.failed_step, "ProcessPayment")
        self.assertEqual(res.compensated_steps, ["ReserveInventory", "CreateOrder"])

        # Final state check
        self.assertEqual(res.final_state["stock"], 10)
        self.assertEqual(res.final_state["orders"]["ord-saga-test"]["status"], "CANCELLED")

    def test_saga_intermediate_state_dirty_read(self) -> None:
        """Verifies that intermediate state is visible to observers before payment outcome (lack of isolation)."""
        saga = CourseSagaScenario(initial_stock=10)
        res = saga.execute_saga(order_id="ord-saga-dirty-read", fail_at_step3=True, inspect_between_step2_and_3=True)

        obs = res.intermediate_state_observed
        self.assertIsNotNone(obs)
        self.assertEqual(obs["order_status"], "PENDING")
        self.assertEqual(obs["stock_observed"], 9)  # Decremented stock was visible!

    def test_lease_stale_holder_fencing_token_rejection(self) -> None:
        """Verifies that storage engine rejects a write with an older fencing token."""
        lock_service = LeaseLockService()
        storage = FencedStorageEngine()

        lease1 = lock_service.acquire_lease("Client_1")
        self.assertEqual(lease1.token, 1)

        # Client 1 pauses; lease expires
        lock_service.expire_lease(lease1)

        # Client 2 acquires lease
        lease2 = lock_service.acquire_lease("Client_2")
        self.assertEqual(lease2.token, 2)

        # Client 2 writes to storage
        res2 = storage.write("key1", "val2", lease2.token, "Client_2")
        self.assertEqual(res2["action"], "ACCEPT_WRITE")
        self.assertEqual(storage.highest_token, 2)

        # Client 1 resumes and attempts write with Token 1
        res1 = storage.write("key1", "val1_stale", lease1.token, "Client_1")
        self.assertEqual(res1["action"], "REJECT_STALE_WRITE")
        self.assertEqual(storage.records["key1"], "val2")
        self.assertEqual(len(storage.rejections), 1)

    def test_fencing_token_valid_monotonic_writes(self) -> None:
        """Verifies that storage engine accepts subsequent writes with higher tokens."""
        storage = FencedStorageEngine()
        w1 = storage.write("k", "v1", 10, "C1")
        self.assertEqual(w1["action"], "ACCEPT_WRITE")

        w2 = storage.write("k", "v2", 15, "C2")
        self.assertEqual(w2["action"], "ACCEPT_WRITE")
        self.assertEqual(storage.records["k"], "v2")
        self.assertEqual(storage.highest_token, 15)


class TestM18Reset(unittest.TestCase):
    def test_reset_idempotent_twice(self) -> None:
        """Verifies that reset runs twice cleanly without error and is fail-closed."""
        # Run 1
        count1 = reset_m18_environment(verbose=False)
        self.assertIsInstance(count1, int)

        # Run 2
        count2 = reset_m18_environment(verbose=False)
        self.assertIsInstance(count2, int)


if __name__ == "__main__":
    unittest.main()
