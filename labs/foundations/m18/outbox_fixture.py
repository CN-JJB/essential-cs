#!/usr/bin/env python3
"""
Broker-Neutral Transactional Outbox & Worker Deduplication Fixture for M18.

Demonstrates:
1. Broken Dual-Write Divergence: Local DB commit followed by an uncoordinated failure
   before enqueue leaves business state committed while delivery action is missing.
2. Transactional Outbox Pattern: Local DB business state and outbox event table are
   committed within the EXACT SAME SQLite transaction (BEGIN IMMEDIATE ... COMMIT).
3. Outbox Relay with At-Least-Once Delivery: Relay scans undispatched outbox events.
   Scripted deliver-before-mark failure leaves dispatched=0, inducing duplicate delivery
   on subsequent relay attempts.
4. Scoped Duplicate-Safe Worker: Worker uses a single SQLite transaction to claim
   processed_events(msg_id) and apply the consumer fulfillment business effect.
   Duplicate messages follow an explicit conflict/deduplication path without reapplying
   the business effect.

Scope Proved:
Duplicate-safe selected local SQLite effect under this local transaction/dedup contract.
This does NOT prove an unbounded or arbitrary external exactly-once guarantee.
"""

import datetime
import json
import os
import sqlite3
from typing import Any, Dict, List, Optional, Tuple


class DualWriteCrashError(RuntimeError):
    """Simulated crash or partition between local DB commit and message enqueue."""
    pass


class RelayCrashBeforeMarkError(RuntimeError):
    """Simulated crash after delivering to worker but before marking event as dispatched."""
    pass


def init_database(db_path: str) -> None:
    """Initialize SQLite database with business, outbox, dedup, and fulfillment tables."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    customer TEXT NOT NULL,
                    item TEXT NOT NULL,
                    amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS outbox_events (
                    id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    dispatched INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    dispatched_at TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_events (
                    msg_id TEXT PRIMARY KEY,
                    processed_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS fulfillments (
                    order_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
    finally:
        conn.close()


class DeliveryBuffer:
    """
    In-memory message transport buffer representing an uncoordinated broker/queue.
    Used to demonstrate dual-write divergence and message transport.
    """

    def __init__(self) -> None:
        self.messages: List[Dict[str, Any]] = []

    def enqueue(self, message: Dict[str, Any]) -> None:
        self.messages.append(message)

    def size(self) -> int:
        return len(self.messages)

    def clear(self) -> None:
        self.messages.clear()


def produce_broken_dual_write(
    db_path: str,
    order_id: str,
    customer: str,
    item: str,
    amount: float,
    buffer: DeliveryBuffer,
    fail_before_enqueue: bool = True,
) -> Dict[str, Any]:
    """
    Demonstrates the uncoordinated dual-write problem.

    Step 1: Commit local SQLite business mutation (orders table).
    Step 2: Attempt separate delivery action into the delivery buffer.
    If fail_before_enqueue is True, a crash occurs between the two uncoordinated operations.
    """
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = sqlite3.connect(db_path)
    try:
        # Step 1: Commit local database mutation independently
        with conn:
            conn.execute(
                "INSERT INTO orders (id, customer, item, amount, status, created_at) "
                "VALUES (?, ?, ?, ?, 'PLACED', ?)",
                (order_id, customer, item, amount, now),
            )
    finally:
        conn.close()

    # Injected crash point: local DB write succeeded and committed, but enqueue has not happened
    if fail_before_enqueue:
        raise DualWriteCrashError(
            f"CRASH_BETWEEN_DB_AND_QUEUE: Order '{order_id}' committed in SQLite, "
            "but process crashed before message could be enqueued to buffer."
        )

    # Step 2: Uncoordinated enqueue action
    msg = {
        "event_id": f"evt-{order_id}",
        "event_type": "OrderPlaced",
        "order_id": order_id,
        "customer": customer,
        "item": item,
        "amount": amount,
        "timestamp": now,
    }
    buffer.enqueue(msg)
    return {"order_id": order_id, "enqueued": True, "msg": msg}


def produce_transactional_outbox(
    db_path: str,
    order_id: str,
    customer: str,
    item: str,
    amount: float,
    event_id: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Demonstrates the Transactional Outbox pattern.

    Business mutation (orders row) and outbound event staging (outbox_events row)
    are executed within the EXACT SAME SQLite transaction using BEGIN IMMEDIATE.
    Both rows commit atomically, or neither commits.
    """
    if event_id is None:
        event_id = f"evt-{order_id}"

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    payload = json.dumps(
        {
            "order_id": order_id,
            "customer": customer,
            "item": item,
            "amount": amount,
            "created_at": now,
        }
    )

    conn = sqlite3.connect(db_path)
    try:
        # Explicit local SQLite transaction boundary
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            "INSERT INTO orders (id, customer, item, amount, status, created_at) "
            "VALUES (?, ?, ?, ?, 'PLACED', ?)",
            (order_id, customer, item, amount, now),
        )
        conn.execute(
            "INSERT INTO outbox_events (id, event_type, payload, dispatched, created_at) "
            "VALUES (?, 'OrderPlaced', ?, 0, ?)",
            (event_id, payload, now),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    return order_id, event_id


class Worker:
    """
    Course-owned worker applying a selected consumer business effect (fulfillments).
    Uses ONE local SQLite transaction to atomically claim processed_events(msg_id)
    and insert/update fulfillments.
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.delivery_attempts = 0
        self.applied_effects = 0
        self.duplicate_suppressions = 0

    def process_message(self, msg_id: str, payload_json: str) -> Dict[str, Any]:
        """
        Processes an event under the transactional deduplication contract.

        Atomically inside a single SQLite transaction:
        1. Checks/claims msg_id in processed_events.
        2. If duplicate, rolls back and skips applying fulfillment.
        3. If new, inserts processed_events claim and creates fulfillment record.
        """
        self.delivery_attempts += 1
        payload = json.loads(payload_json)
        order_id = payload["order_id"]
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("BEGIN IMMEDIATE")

            # Explicit existing-key check inside the same transaction
            cur = conn.execute(
                "SELECT 1 FROM processed_events WHERE msg_id = ?", (msg_id,)
            )
            if cur.fetchone() is not None:
                conn.rollback()
                self.duplicate_suppressions += 1
                return {
                    "status": "DUPLICATE_IGNORED",
                    "msg_id": msg_id,
                    "order_id": order_id,
                    "applied": False,
                    "reason": "MSG_ID_ALREADY_PROCESSED",
                }

            # Attempt insert into processed_events (also catch unique constraint conflicts)
            try:
                conn.execute(
                    "INSERT INTO processed_events (msg_id, processed_at) VALUES (?, ?)",
                    (msg_id, now),
                )
            except sqlite3.IntegrityError:
                conn.rollback()
                self.duplicate_suppressions += 1
                return {
                    "status": "DUPLICATE_IGNORED",
                    "msg_id": msg_id,
                    "order_id": order_id,
                    "applied": False,
                    "reason": "INTEGRITY_CONFLICT",
                }

            # Apply selected consumer-side business effect
            conn.execute(
                "INSERT INTO fulfillments (order_id, status, updated_at) "
                "VALUES (?, 'FULFILLED', ?)",
                (order_id, now),
            )

            conn.commit()
            self.applied_effects += 1
            return {
                "status": "PROCESSED",
                "msg_id": msg_id,
                "order_id": order_id,
                "applied": True,
                "fulfillment_status": "FULFILLED",
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


class OutboxRelay:
    """
    Independent relay polling outbox_events and dispatching to a Worker.
    Provides a scripted failure hook to demonstrate at-least-once duplicate delivery:
    worker receives and processes event, but relay crashes before marking dispatched=1.
    """

    def __init__(self, db_path: str, worker: Worker) -> None:
        self.db_path = db_path
        self.worker = worker

    def relay_pending(
        self,
        simulate_crash_on_event_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Polls undispatched events (dispatched = 0) in FIFO creation order.
        For each event:
        1. Delivers to worker.
        2. If simulate_crash_on_event_id matches, raises RelayCrashBeforeMarkError
           WITHOUT updating dispatched=1 in outbox_events.
        3. Otherwise, updates outbox_events SET dispatched = 1.
        """
        conn = sqlite3.connect(self.db_path)
        dispatches: List[Dict[str, Any]] = []
        try:
            cur = conn.execute(
                "SELECT id, event_type, payload FROM outbox_events "
                "WHERE dispatched = 0 ORDER BY created_at ASC"
            )
            pending_rows = cur.fetchall()

            for row in pending_rows:
                event_id, event_type, payload = row
                # Deliver to worker
                worker_result = self.worker.process_message(event_id, payload)

                # Scripted failure point: delivered to worker, but relay crashes before recording mark
                if simulate_crash_on_event_id == event_id:
                    raise RelayCrashBeforeMarkError(
                        f"RELAY_CRASH_BEFORE_MARK: Event '{event_id}' delivered to worker, "
                        "but relay process crashed before setting dispatched=1 in SQLite."
                    )

                # Mark event as dispatched in outbox
                now = datetime.datetime.now(datetime.timezone.utc).isoformat()
                with conn:
                    conn.execute(
                        "UPDATE outbox_events SET dispatched = 1, dispatched_at = ? "
                        "WHERE id = ?",
                        (now, event_id),
                    )

                dispatches.append(
                    {
                        "event_id": event_id,
                        "worker_result": worker_result,
                        "dispatched": True,
                    }
                )
        finally:
            conn.close()

        return dispatches
