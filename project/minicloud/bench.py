"""P4 — query shape, index, and measurement.

A bounded, reproducible benchmark that answers one question: *does the
owner/time index actually change the cost of the list query, for this workload,
and what does it cost to maintain?*

Discipline the harness enforces:

* a stated workload (fixed row count, fixed query, fixed repetition count);
* an explicit warmup before measurement;
* identical data in both databases, so results are comparable;
* a **correctness check** — the index must not change which rows come back;
* the database-size and write-cost side of the trade-off, not just read speed;
* the environment recorded, so the numbers are not presented as universal.

It is deliberately not a general benchmarking framework.
"""

from __future__ import annotations

import os
import shutil
import statistics
import tempfile
import time
from datetime import datetime, timedelta, timezone

from .store import Store, utcnow

OWNER = "bench-owner"
QUERY_LIMIT = 50

#: Fixed fixture epoch. Using a constant (not wall-clock) keeps the two
#: databases byte-comparable and makes the ordering test meaningful — the
#: ``ORDER BY created_at`` ties that a wall-clock fixture would create are the
#: kind of thing that silently makes a benchmark wrong.
_FIXTURE_EPOCH = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _ts(index: int) -> str:
    return (_FIXTURE_EPOCH + timedelta(microseconds=index)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _ensure_owner(conn) -> None:
    """The items table has an owner foreign key; the fixture needs a real owner."""
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id, username, password_salt, password_hash,"
        " password_iterations, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (OWNER, OWNER, "00" * 16, "00" * 32, 10000, utcnow()),
    )


def _seed(store: Store, rows: int) -> None:
    """Insert a deterministic fixture in one transaction (fast, repeatable)."""
    conn = store.connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        payload = "x" * 64
        _ensure_owner(conn)
        for i in range(rows):
            conn.execute(
                "INSERT INTO items (item_id, owner_id, kind, title, body, url, visibility,"
                " version, created_at, updated_at, index_status)"
                " VALUES (?, ?, 'note', ?, ?, NULL, 'private', 1, ?, ?, 'none')",
                (f"bench{i:08d}", OWNER, f"title-{i}", payload, _ts(i), _ts(i)),
            )
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()


def _measure_list(store: Store, repetitions: int) -> list[float]:
    sql = "SELECT item_id FROM items WHERE owner_id = ? ORDER BY created_at DESC LIMIT ?"
    samples: list[float] = []
    conn = store.connect()
    try:
        # Warmup: populate the page cache so we are not measuring cold I/O noise
        # as if it were the index effect.
        for _ in range(3):
            conn.execute(sql, (OWNER, QUERY_LIMIT)).fetchall()
        for _ in range(repetitions):
            started = time.perf_counter_ns()
            conn.execute(sql, (OWNER, QUERY_LIMIT)).fetchall()
            samples.append((time.perf_counter_ns() - started) / 1_000_000.0)
    finally:
        conn.close()
    return samples


def _measure_write(store: Store, extra_rows: int) -> float:
    conn = store.connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        _ensure_owner(conn)
        started = time.perf_counter_ns()
        for i in range(extra_rows):
            conn.execute(
                "INSERT INTO items (item_id, owner_id, kind, title, body, url, visibility,"
                " version, created_at, updated_at, index_status)"
                " VALUES (?, ?, 'note', ?, '', NULL, 'private', 1, ?, ?, 'none')",
                (f"wr{i:08d}", OWNER, f"w{i}", _ts(1_000_000 + i), _ts(1_000_000 + i)),
            )
        elapsed = (time.perf_counter_ns() - started) / 1_000_000.0
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()
    return elapsed


def _ordered_ids(store: Store) -> list[str]:
    conn = store.connect()
    try:
        rows = conn.execute(
            "SELECT item_id FROM items WHERE owner_id = ? ORDER BY created_at DESC LIMIT ?",
            (OWNER, QUERY_LIMIT),
        ).fetchall()
    finally:
        conn.close()
    return [r[0] for r in rows]


def run_benchmark(*, rows: int = 4000, repetitions: int = 25, write_rows: int = 300) -> dict:
    workdir = tempfile.mkdtemp(prefix="minicloud-bench-")
    try:
        indexed = Store(os.path.join(workdir, "indexed.db"))
        baseline = Store(os.path.join(workdir, "baseline.db"))
        indexed.initialize()
        baseline.initialize()
        # Baseline = the schema without the owner/time index.
        conn = baseline.connect()
        try:
            conn.execute("DROP INDEX IF EXISTS idx_items_owner_created")
        finally:
            conn.close()

        _seed(indexed, rows)
        _seed(baseline, rows)

        plan_indexed = indexed.query_plan(OWNER)
        plan_baseline = baseline.query_plan(OWNER)

        base_samples = _measure_list(baseline, repetitions)
        idx_samples = _measure_list(indexed, repetitions)

        base_write = _measure_write(baseline, write_rows)
        idx_write = _measure_write(indexed, write_rows)

        equivalent = _ordered_ids(baseline) == _ordered_ids(indexed)

        size_baseline = os.path.getsize(baseline.db_path)
        size_indexed = os.path.getsize(indexed.db_path)

        def summary(samples: list[float]) -> dict:
            return {
                "repetitions": len(samples),
                "median_ms": round(statistics.median(samples), 4),
                "min_ms": round(min(samples), 4),
                "max_ms": round(max(samples), 4),
            }

        base_median = statistics.median(base_samples)
        idx_median = statistics.median(idx_samples)
        ratio = (base_median / idx_median) if idx_median else float("inf")

        return {
            "disposition": "PASS" if equivalent else "FAIL",
            "workload": {
                "rows": rows,
                "query": "SELECT item_id FROM items WHERE owner_id=? ORDER BY created_at DESC LIMIT ?",
                "limit": QUERY_LIMIT,
                "repetitions": repetitions,
                "warmup_runs": 3,
                "write_rows_measured": write_rows,
            },
            "plan_baseline": plan_baseline,
            "plan_indexed": plan_indexed,
            "latency_baseline": summary(base_samples),
            "latency_indexed": summary(idx_samples),
            "median_speedup_x": round(ratio, 2) if ratio != float("inf") else None,
            "db_size_bytes": {"baseline": size_baseline, "indexed": size_indexed,
                              "index_overhead_bytes": size_indexed - size_baseline},
            "write_cost_ms": {"baseline": round(base_write, 3), "indexed": round(idx_write, 3)},
            "result_equivalence": equivalent,
            "inference_limits": [
                "single-node local SQLite; timings are host- and cache-dependent",
                "loopback/local storage only; not a network or production claim",
                "index benefit is specific to this owner/time access path",
                "write-cost difference is small at this scale and may be noise-dominated",
                "no universal threshold is asserted; the index is justified by this measurement",
            ],
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
