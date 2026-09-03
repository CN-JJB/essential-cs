#!/usr/bin/env python3
"""Write-Ahead Logging (WAL) Ordering and Recovery Model for M09 L09-01.

Demonstrates:
1. WAL is an ordering and recovery strategy, not a magical durability primitive.
2. The Write-Ahead Invariant: log records representing an update must be flushed/synced
   to non-volatile log storage BEFORE the corresponding dirty data page may be flushed
   to persistent disk tables (page_lsn <= flushed_lsn).
3. Teaching-model commit rule: under this model's named crash/log-storage contract, a COMMIT
   is acknowledged only after the relevant log prefix is marked stable by sync_log().
4. Bounded recovery intuition (NOT a full ARIES implementation):
   - Analysis: identify committed vs active transactions in the surviving model log.
   - Redo: this simplified model reconstructs committed changes.
   - Undo: it rolls back surviving uncommitted changes.
   Real ARIES redo uses repeat-history semantics and may redo loser-transaction updates before undo.
"""

import copy
import json
import sys
from dataclasses import asdict, dataclass


@dataclass
class WALRecord:
    lsn: int  # Log Sequence Number (1-indexed, monotonically increasing)
    txn_id: int
    op_type: str  # "BEGIN", "UPDATE", "COMMIT", "ABORT", "CHECKPOINT"
    key: str | None = None
    old_val: str | None = None
    new_val: str | None = None


class WALEngine:
    """Bounded, deterministic Write-Ahead Logging and Recovery Model."""

    def __init__(self):
        self.log_records: list[WALRecord] = []
        self.flushed_lsn: int = 0
        self.checkpoint_lsn: int = 0
        # In-memory buffer pool (volatile RAM state)
        self.buffer_pool: dict[str, str] = {}
        self.page_lsns: dict[str, int] = {}
        # On-disk table (simulated persistent storage)
        self.disk_table: dict[str, str] = {}
        self._next_txn_id: int = 1

    def begin_txn(self) -> int:
        txn_id = self._next_txn_id
        self._next_txn_id += 1
        self._append_record(txn_id, "BEGIN")
        return txn_id

    def update(self, txn_id: int, key: str, new_val: str) -> int:
        # Read existing value from buffer pool or disk
        old_val = self.buffer_pool.get(key, self.disk_table.get(key))
        lsn = self._append_record(txn_id, "UPDATE", key=key, old_val=old_val, new_val=new_val)
        # Update in-memory buffer pool and tag with page LSN
        self.buffer_pool[key] = new_val
        self.page_lsns[key] = lsn
        return lsn

    def commit_txn(self, txn_id: int, sync: bool = True) -> int:
        lsn = self._append_record(txn_id, "COMMIT")
        if sync:
            self.sync_log()
        return lsn

    def abort_txn(self, txn_id: int) -> None:
        self._append_record(txn_id, "ABORT")
        for record in reversed(self.log_records):
            if record.txn_id == txn_id and record.op_type == "UPDATE":
                if record.key is not None:
                    if record.old_val is None:
                        self.buffer_pool.pop(record.key, None)
                        self.page_lsns.pop(record.key, None)
                    else:
                        self.buffer_pool[record.key] = record.old_val
                        self.page_lsns[record.key] = record.lsn
            if record.txn_id == txn_id and record.op_type == "BEGIN":
                break

    def sync_log(self) -> int:
        """Synchronize log buffer to persistent storage, advancing flushed_lsn."""
        self.flushed_lsn = len(self.log_records)
        return self.flushed_lsn

    def flush_page_to_disk(self, key: str, force_wal: bool = True) -> bool:
        """Flush a dirty page from buffer pool to disk table.

        Write-Ahead Invariant: page_lsn <= flushed_lsn.
        If force_wal is True, forces sync_log() if needed before writing page.
        If force_wal is False and page_lsn > flushed_lsn, raises an invariant error.
        """
        p_lsn = self.page_lsns.get(key, 0)
        if p_lsn > self.flushed_lsn:
            if force_wal:
                self.sync_log()
            else:
                raise RuntimeError(
                    f"WAL Invariant Violation: Attempted to write page '{key}' (LSN {p_lsn}) "
                    f"to disk before log was flushed (flushed LSN {self.flushed_lsn})"
                )

        if key in self.buffer_pool:
            self.disk_table[key] = self.buffer_pool[key]
        return True

    def checkpoint(self) -> int:
        """Checkpoint flushes all dirty pages to disk table.

        Strictly enforces the Write-Ahead rule by flushing log first.
        """
        self.sync_log()
        for key in list(self.buffer_pool.keys()):
            self.flush_page_to_disk(key, force_wal=True)
        ckpt_lsn = self._append_record(0, "CHECKPOINT")
        self.sync_log()
        self.checkpoint_lsn = ckpt_lsn
        return ckpt_lsn

    def _append_record(
        self,
        txn_id: int,
        op_type: str,
        key: str | None = None,
        old_val: str | None = None,
        new_val: str | None = None,
    ) -> int:
        lsn = len(self.log_records) + 1
        record = WALRecord(
            lsn=lsn,
            txn_id=txn_id,
            op_type=op_type,
            key=key,
            old_val=old_val,
            new_val=new_val,
        )
        self.log_records.append(record)
        return lsn

    def simulate_crash(self) -> "WALEngine":
        """Simulate a sudden power-loss crash.

        Volatile state destroyed:
        - In-memory buffer pool is lost.
        - Unflushed log records (lsn > flushed_lsn) are lost.
        Persistent state preserved:
        - Flushed log records (lsn <= flushed_lsn).
        - Disk table (data pages actually written to disk).
        """
        recovered = WALEngine()
        recovered.log_records = [copy.deepcopy(r) for r in self.log_records[: self.flushed_lsn]]
        recovered.flushed_lsn = self.flushed_lsn
        recovered.checkpoint_lsn = min(self.checkpoint_lsn, self.flushed_lsn)
        # On disk data survives
        recovered.disk_table = copy.deepcopy(self.disk_table)
        # Buffer pool is initialized from disk table
        recovered.buffer_pool = copy.deepcopy(self.disk_table)
        return recovered

    def recover(self) -> dict:
        """Execute the bounded teaching recovery model (not full ARIES repeat-history)."""
        committed_txns = set()
        aborted_txns = set()
        all_txns = set()

        # 1. Analysis Phase: scan log
        for rec in self.log_records:
            if rec.txn_id != 0:
                all_txns.add(rec.txn_id)
            if rec.op_type == "COMMIT":
                committed_txns.add(rec.txn_id)
            elif rec.op_type == "ABORT":
                aborted_txns.add(rec.txn_id)

        active_txns = all_txns - committed_txns - aborted_txns

        # 2. Simplified teaching Redo: replay committed updates.
        # Full ARIES instead repeats history (including some loser updates) before Undo.
        redo_count = 0
        for rec in self.log_records:
            if rec.op_type == "UPDATE" and rec.txn_id in committed_txns:
                if rec.key is not None and rec.new_val is not None:
                    self.disk_table[rec.key] = rec.new_val
                    self.buffer_pool[rec.key] = rec.new_val
                    self.page_lsns[rec.key] = rec.lsn
                    redo_count += 1

        # 3. Undo Phase: roll back any uncommitted updates that reached disk
        undo_count = 0
        for rec in reversed(self.log_records):
            if rec.op_type == "UPDATE" and rec.txn_id in active_txns:
                if rec.key is not None:
                    if rec.old_val is None:
                        self.disk_table.pop(rec.key, None)
                        self.buffer_pool.pop(rec.key, None)
                    else:
                        self.disk_table[rec.key] = rec.old_val
                        self.buffer_pool[rec.key] = rec.old_val
                    undo_count += 1

        return {
            "analysis_active_uncommitted_txns": sorted(list(active_txns)),
            "analysis_committed_txns": sorted(list(committed_txns)),
            "redone_operations": redo_count,
            "undone_operations": undo_count,
            "recovered_table": copy.deepcopy(self.disk_table),
        }


def run_wal_demonstration() -> dict:
    """Run a structured WAL sequence with committed, uncommitted, and checkpointed transactions."""
    engine = WALEngine()

    # Step 1: Initial state established and checkpointed
    t0 = engine.begin_txn()
    engine.update(t0, "account_A", "100")
    engine.update(t0, "account_B", "200")
    engine.commit_txn(t0, sync=True)
    engine.checkpoint()

    # Step 2: Txn 1 committed and synced, but data pages NOT yet checkpointed to disk table
    t1 = engine.begin_txn()
    engine.update(t1, "account_A", "150")  # A + 50
    engine.commit_txn(t1, sync=True)

    # Step 3: Txn 2 uncommitted in volatile buffer pool when power cuts
    t2 = engine.begin_txn()
    engine.update(t2, "account_B", "999")  # Uncommitted dirty update in buffer pool
    # Note: T2 is NOT committed and NOT synced

    # Simulate sudden crash
    crashed_storage = engine.simulate_crash()

    # Verify disk table before recovery reflects only checkpointed state
    disk_before_recovery = copy.deepcopy(crashed_storage.disk_table)

    # Execute recovery
    recovery_report = crashed_storage.recover()
    rec_table = recovery_report["recovered_table"]

    # Post-recovery verification:
    # Txn 1 committed updates ("account_A" = "150") must be restored via REDO.
    # Txn 2 uncommitted updates ("account_B" = "999") must NOT appear in recovered table.
    is_consistent = (rec_table.get("account_A") == "150") and (rec_table.get("account_B") == "200")

    return {
        "checkpointed_disk_before_recovery": disk_before_recovery,
        "committed_txns": recovery_report["analysis_committed_txns"],
        "uncommitted_txns": recovery_report["analysis_active_uncommitted_txns"],
        "redone_count": recovery_report["redone_operations"],
        "undone_count": recovery_report["undone_operations"],
        "recovered_state": rec_table,
        "consistency_restored": is_consistent,
    }


def main() -> int:
    print("=== Essential CS M09 — Write-Ahead Logging (WAL) Model (L09-01) ===")
    res = run_wal_demonstration()
    print(f"[1] Disk State Before Recovery: {res['checkpointed_disk_before_recovery']}")
    print(f"[2] Crash Recovery Analysis:")
    print(f"    Committed Txns (to Redo):   {res['committed_txns']}")
    print(f"    Uncommitted Txns (Ignored): {res['uncommitted_txns']}")
    print(f"    Redo Operations Applied:    {res['redone_count']}")
    print(f"[3] Recovered State: {res['recovered_state']}")
    print(f"[4] Consistency Check: {'PASS' if res['consistency_restored'] else 'FAIL'}")
    return 0 if res["consistency_restored"] else 1


if __name__ == "__main__":
    sys.exit(main())
