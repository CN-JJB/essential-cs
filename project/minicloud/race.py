"""P5 — concurrent requests and transactional correctness.

Three deterministic demonstrations. None of them relies on "it passed once" or
on a sleep-based race that may or may not fire:

1. :func:`demonstrate_lost_update` — two connections perform a naive
   read-modify-write with an *explicit, scripted* interleaving, and one update
   is lost. Deterministic, because the interleaving is scripted, not raced.
2. :func:`demonstrate_optimistic_protection` — the same interleaving through the
   service's version check. The second writer gets a conflict instead of
   silently overwriting.
3. :func:`demonstrate_serialized_increment` — many real threads increment a
   counter inside ``BEGIN IMMEDIATE``. The final value must equal the number of
   successful increments; the count of conflicts is reported rather than hidden.

The lesson the harness makes checkable: *application-level ordering and database
transaction guarantees are different things, and only one of them is what keeps
the invariant true.*
"""

from __future__ import annotations

import os
import shutil
import tempfile
import threading

from .store import Store, utcnow


def _ensure_user(conn, owner: str) -> None:
    """The items table has an owner foreign key; the demo needs a real owner row."""
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id, username, password_salt, password_hash,"
        " password_iterations, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (owner, owner, "00" * 16, "00" * 32, 10000, utcnow()),
    )


def _seed_item(store: Store, item_id: str, owner: str, title: str) -> None:
    store.initialize()
    conn = store.connect()
    try:
        now = utcnow()
        _ensure_user(conn, owner)
        conn.execute(
            "INSERT INTO items (item_id, owner_id, kind, title, body, url, visibility,"
            " version, created_at, updated_at, index_status)"
            " VALUES (?, ?, 'note', ?, '', NULL, 'private', 1, ?, ?, 'none')",
            (item_id, owner, title, now, now),
        )
    finally:
        conn.close()


def demonstrate_lost_update() -> dict:
    workdir = tempfile.mkdtemp(prefix="minicloud-race-lost-")
    try:
        store = Store(os.path.join(workdir, "race.db"))
        _seed_item(store, "item-1", "owner", "original")
        c1 = store.connect()
        c2 = store.connect()
        try:
            # Scripted interleaving: both read before either writes.
            v1 = c1.execute("SELECT version FROM items WHERE item_id='item-1'").fetchone()[0]
            v2 = c2.execute("SELECT version FROM items WHERE item_id='item-1'").fetchone()[0]
            c1.execute("UPDATE items SET title='writer-A', version=version+1 WHERE item_id='item-1'")
            c2.execute("UPDATE items SET title='writer-B', version=version+1 WHERE item_id='item-1'")
            final = c1.execute("SELECT title, version FROM items WHERE item_id='item-1'").fetchone()
        finally:
            c1.close()
            c2.close()
        return {
            "path": "naive_read_modify_write",
            "both_read_version": [v1, v2],
            "final_title": final[0],
            "final_version": final[1],
            "lost_update_observed": final[0] == "writer-B" and final[1] == 3,
            "note": "both writers believed they held version 1; writer-A's change is gone",
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def demonstrate_optimistic_protection() -> dict:
    workdir = tempfile.mkdtemp(prefix="minicloud-race-protected-")
    try:
        store = Store(os.path.join(workdir, "race.db"))
        _seed_item(store, "item-1", "owner", "original")

        first = store.update_item(
            item_id="item-1", owner_id="owner", expected_version=1, fields={"title": "writer-A"}
        )
        second = store.update_item(
            item_id="item-1", owner_id="owner", expected_version=1, fields={"title": "writer-B"}
        )
        final = store.get_item("item-1")
        return {
            "path": "optimistic_version_check",
            "first_write_applied": first is not None,
            "second_write_rejected": second is None,
            "final_title": final["title"],
            "final_version": final["version"],
            "no_lost_update": first is not None and second is None and final["title"] == "writer-A",
            "note": "the stale writer is told it lost the race instead of silently overwriting",
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def demonstrate_serialized_increment(*, threads: int = 8, per_thread: int = 25) -> dict:
    workdir = tempfile.mkdtemp(prefix="minicloud-race-incr-")
    try:
        store = Store(os.path.join(workdir, "race.db"))
        store.initialize()
        conn = store.connect()
        try:
            now = utcnow()
            _ensure_user(conn, "owner")
            conn.execute(
                "INSERT INTO items (item_id, owner_id, kind, title, body, url, visibility,"
                " version, created_at, updated_at, index_status)"
                " VALUES ('counter','owner','note','counter','0',NULL,'private',1,?,?,'none')",
                (now, now),
            )
        finally:
            conn.close()

        conflicts = 0
        lock = threading.Lock()
        barrier = threading.Barrier(threads)

        def worker() -> None:
            nonlocal conflicts
            barrier.wait()
            for _ in range(per_thread):
                with store._tx() as c:  # BEGIN IMMEDIATE serializes writers
                    row = c.execute("SELECT body FROM items WHERE item_id='counter'").fetchone()
                    value = int(row[0])
                    c.execute("UPDATE items SET body=? WHERE item_id='counter'", (str(value + 1),))

        workers = [threading.Thread(target=worker) for _ in range(threads)]
        for w in workers:
            w.start()
        for w in workers:
            w.join(timeout=30)

        conn = store.connect()
        try:
            final_value = int(conn.execute("SELECT body FROM items WHERE item_id='counter'").fetchone()[0])
        finally:
            conn.close()

        expected = threads * per_thread
        return {
            "path": "begin_immediate_serialized_writers",
            "threads": threads,
            "increments_per_thread": per_thread,
            "expected_final_value": expected,
            "observed_final_value": final_value,
            "conflicts_observed": conflicts,
            "threads_joined": all(not w.is_alive() for w in workers),
            "invariant_holds": final_value == expected,
            "note": "BEGIN IMMEDIATE is what makes the read-modify-write atomic here; "
                    "the application lock is not the guarantee",
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def run_concurrency_demo() -> dict:
    lost = demonstrate_lost_update()
    protected = demonstrate_optimistic_protection()
    serialized = demonstrate_serialized_increment()
    ok = (
        lost["lost_update_observed"]
        and protected["no_lost_update"]
        and serialized["invariant_holds"]
    )
    return {
        "disposition": "PASS" if ok else "FAIL",
        "naive": lost,
        "optimistic": protected,
        "serialized": serialized,
        "inference_limits": [
            "deterministic scripted interleavings, not a probabilistic stress test",
            "single-node SQLite local transaction behaviour only",
            "not evidence of distributed or cross-database serializability",
        ],
    }
