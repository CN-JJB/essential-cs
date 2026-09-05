#!/usr/bin/env python3
"""
LAB-REQ-05: SQLite Transactions, Isolation, Rollback & Recovery Boundary Harness

Implements the five canonical checkpoints:
1. Invariant Definition & Committed Visibility (dual connection, no dirty read)
2. Bounded Writer Conflict (actual SQLITE_BUSY / exception capture without fixed string)
3. Explicit Rollback (invariant preservation across connections)
4. Owned Child Interruption & Reopen Recovery (watchdog, reap, recovery observation, inference limits)
5. Backup & Storage Boundary (online backup API, clean destination verification, cleanup)
"""

import os
import platform
import queue
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
from typing import Any, Dict, Optional, Tuple

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(LAB_DIR, "lab_req_05.db")
DEFAULT_BACKUP_PATH = os.path.join(LAB_DIR, "lab_req_05_backup.db")
CHILD_WORKER_PATH = os.path.join(LAB_DIR, "child_worker.py")


def _is_busy_conflict(exc: sqlite3.Error) -> bool:
    """Classify SQLite BUSY/LOCKED structurally, without matching driver message text."""
    code = getattr(exc, "sqlite_errorcode", None)
    name = getattr(exc, "sqlite_errorname", None)
    primary_codes = {
        getattr(sqlite3, "SQLITE_BUSY", 5),
        getattr(sqlite3, "SQLITE_LOCKED", 6),
    }
    if isinstance(code, int) and (code & 0xFF) in primary_codes:
        return True
    if isinstance(name, str) and (name.startswith("SQLITE_BUSY") or name.startswith("SQLITE_LOCKED")):
        return True
    return False


class TransactionLabHarness:
    def __init__(self, db_path: str = DEFAULT_DB_PATH, backup_path: str = DEFAULT_BACKUP_PATH):
        self.db_path = db_path
        self.backup_path = backup_path
        self.journal_path = db_path + "-journal"
        self.meta: Dict[str, Any] = {}

    def init_database(self) -> Dict[str, Any]:
        """Initializes database under DELETE rollback journal mode with initial invariant state."""
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass
        if os.path.exists(self.journal_path):
            try:
                os.remove(self.journal_path)
            except OSError:
                pass

        conn = sqlite3.connect(self.db_path, isolation_level=None)
        cursor = conn.cursor()

        cursor.execute("PRAGMA journal_mode = DELETE;")
        actual_journal_mode = cursor.fetchone()[0]

        cursor.execute("PRAGMA synchronous = NORMAL;")
        cursor.execute("PRAGMA synchronous;")
        actual_synchronous = cursor.fetchone()[0]

        cursor.execute("""
            CREATE TABLE accounts (
                id TEXT PRIMARY KEY,
                balance INTEGER NOT NULL CHECK (balance >= 0)
            );
        """)
        cursor.execute("INSERT INTO accounts (id, balance) VALUES ('A', 600), ('B', 400);")
        conn.close()

        self.meta = {
            "platform": f"{platform.system()} {platform.release()} ({platform.machine()})",
            "python_version": platform.python_version(),
            "sqlite_version": sqlite3.sqlite_version,
            "journal_mode": actual_journal_mode.upper(),
            "synchronous": str(actual_synchronous),
            "db_path": self.db_path,
        }
        return self.meta

    def run_checkpoint_1_committed_visibility(self) -> Dict[str, Any]:
        """
        Checkpoint 1: Dual connection committed-only visibility.
        Conn 1 updates Account A in an uncommitted transaction.
        Conn 2 reads Account A and must observe only the committed balance (600).
        """
        conn1 = sqlite3.connect(self.db_path, timeout=0.0, isolation_level=None)
        conn2 = sqlite3.connect(self.db_path, timeout=0.0, isolation_level=None)

        try:
            cur1 = conn1.cursor()
            cur2 = conn2.cursor()

            cur1.execute("BEGIN IMMEDIATE;")
            cur1.execute("UPDATE accounts SET balance = 500 WHERE id = 'A';")

            cur1.execute("SELECT balance FROM accounts WHERE id = 'A';")
            conn1_val = cur1.fetchone()[0]

            cur2.execute("SELECT balance FROM accounts WHERE id = 'A';")
            conn2_val = cur2.fetchone()[0]

            dirty_read = (conn2_val == conn1_val)
            passed = (conn2_val == 600 and not dirty_read)

            return {
                "checkpoint": 1,
                "name": "Invariant Definition & Committed Visibility",
                "passed": passed,
                "conn1_uncommitted_value": conn1_val,
                "conn2_observed_value": conn2_val,
                "dirty_read_detected": dirty_read,
                "guarantee": "SQLite committed-only visibility under declared local locking/journal baseline",
            }
        finally:
            conn1.close()
            conn2.close()

    def run_checkpoint_2_bounded_writer_conflict(self) -> Dict[str, Any]:
        """
        Checkpoint 2: Competing-writer conflict without fixed exception string matching.
        While Conn 1 holds write intent, Conn 2 attempts a write transaction.
        """
        conn1 = sqlite3.connect(self.db_path, timeout=0.0, isolation_level=None)
        conn2 = sqlite3.connect(self.db_path, timeout=0.0, isolation_level=None)

        try:
            cur1 = conn1.cursor()
            cur2 = conn2.cursor()

            cur1.execute("BEGIN IMMEDIATE;")
            cur1.execute("UPDATE accounts SET balance = 500 WHERE id = 'A';")

            conflict_caught = False
            error_details: Dict[str, Any] = {
                "error_type": None,
                "error_message": None,
                "sqlite_errorcode": None,
                "sqlite_errorname": None,
            }

            try:
                cur2.execute("BEGIN IMMEDIATE;")
                cur2.execute("UPDATE accounts SET balance = 999 WHERE id = 'B';")
            except sqlite3.OperationalError as e:
                error_details["error_type"] = type(e).__name__
                error_details["error_message"] = str(e)
                error_details["sqlite_errorcode"] = getattr(e, "sqlite_errorcode", None)
                error_details["sqlite_errorname"] = getattr(e, "sqlite_errorname", None)
                if _is_busy_conflict(e):
                    conflict_caught = True
                else:
                    raise
            except sqlite3.Error:
                raise

            # Rollback conn 1 to restore clean state
            cur1.execute("ROLLBACK;")

            # Verify no corruption occurred
            cur1.execute("SELECT id, balance FROM accounts ORDER BY id ASC;")
            current_balances = dict(cur1.fetchall())
            total = sum(current_balances.values())
            no_corruption = (current_balances == {"A": 600, "B": 400} and total == 1000)

            return {
                "checkpoint": 2,
                "name": "Bounded Writer Conflict",
                "passed": conflict_caught and no_corruption,
                "conflict_caught": conflict_caught,
                "error_details": error_details,
                "no_corruption": no_corruption,
                "post_conflict_balances": current_balances,
            }
        finally:
            conn1.close()
            conn2.close()

    def run_checkpoint_3_explicit_rollback(self) -> Dict[str, Any]:
        """
        Checkpoint 3: Explicit rollback restoration.
        """
        conn1 = sqlite3.connect(self.db_path, timeout=0.0, isolation_level=None)
        conn2 = sqlite3.connect(self.db_path, timeout=0.0, isolation_level=None)

        try:
            cur1 = conn1.cursor()
            cur2 = conn2.cursor()

            # Mutate both rows
            cur1.execute("BEGIN IMMEDIATE;")
            cur1.execute("UPDATE accounts SET balance = balance - 200 WHERE id = 'A';")
            cur1.execute("UPDATE accounts SET balance = balance + 200 WHERE id = 'B';")

            # Rollback explicitly
            cur1.execute("ROLLBACK;")

            # Verify on both connections
            cur1.execute("SELECT id, balance FROM accounts ORDER BY id ASC;")
            b1 = dict(cur1.fetchall())
            cur2.execute("SELECT id, balance FROM accounts ORDER BY id ASC;")
            b2 = dict(cur2.fetchall())

            passed = (b1 == {"A": 600, "B": 400} and b2 == {"A": 600, "B": 400})
            return {
                "checkpoint": 3,
                "name": "Explicit Rollback Restoration",
                "passed": passed,
                "conn1_balances": b1,
                "conn2_balances": b2,
                "invariant_total": sum(b1.values()),
            }
        finally:
            conn1.close()
            conn2.close()

    def run_checkpoint_4_child_interruption_recovery(self, timeout_sec: float = 5.0) -> Dict[str, Any]:
        """
        Checkpoint 4: Owned-child interruption and reopen recovery.
        Parent spawns child worker, waits for uncommitted mutation, terminates child via kill(),
        reaps process handle, reopens DB, and verifies automatic rollback recovery.
        """
        child_cmd = [sys.executable, CHILD_WORKER_PATH, self.db_path]
        proc = subprocess.Popen(
            child_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        child_pid = proc.pid
        line_queue = queue.Queue(maxsize=1)

        def _read_handshake_line() -> None:
            try:
                line_queue.put(proc.stdout.readline() if proc.stdout else "")
            except BaseException as exc:
                line_queue.put(exc)

        reader = threading.Thread(target=_read_handshake_line, daemon=True)
        reader.start()

        try:
            # Keep the watchdog deadline on the parent thread. A silent child can block
            # readline() on the helper thread without defeating this timeout.
            try:
                handshake = line_queue.get(timeout=timeout_sec)
            except queue.Empty:
                proc.kill()
                proc.wait(timeout=2.0)
                raise RuntimeError("Child process failed to report readiness within watchdog timeout.")

            if isinstance(handshake, BaseException):
                raise RuntimeError(f"Child handshake reader failed: {type(handshake).__name__}: {handshake}")
            if str(handshake).strip() != "CHILD_MUTATED":
                proc.kill()
                proc.wait(timeout=2.0)
                raise RuntimeError(f"Unexpected child handshake: {str(handshake).strip()!r}")

            # Record journal status during uncommitted child write
            journal_exists_during_write = os.path.exists(self.journal_path)

            # Terminate the owned child abruptly
            proc.kill()
            reap_exitcode = proc.wait(timeout=timeout_sec)

            # Reopen database with fresh connection to trigger recovery
            conn = sqlite3.connect(self.db_path, isolation_level=None)
            cur = conn.cursor()
            cur.execute("SELECT id, balance FROM accounts ORDER BY id ASC;")
            recovered_balances = dict(cur.fetchall())
            conn.close()

            # Observe post-recovery journal status
            journal_exists_after_recovery = os.path.exists(self.journal_path)

            passed = (recovered_balances == {"A": 600, "B": 400} and sum(recovered_balances.values()) == 1000)

            return {
                "checkpoint": 4,
                "name": "Owned Child Interruption & Reopen Recovery",
                "passed": passed,
                "child_pid": child_pid,
                "child_reaped_returncode": reap_exitcode,
                "journal_during_write": journal_exists_during_write,
                "journal_after_recovery": journal_exists_after_recovery,
                "recovered_balances": recovered_balances,
                "invariant_total": sum(recovered_balances.values()),
                "inference_limit": (
                    "Client process kill proves client crash recovery via rollback journal, "
                    "NOT OS crash survival or physical power-loss durability."
                ),
            }

        finally:
            if proc.stdout:
                try:
                    proc.stdout.close()
                except Exception:
                    pass
            if proc.stderr:
                try:
                    proc.stderr.close()
                except Exception:
                    pass
            if proc.poll() is None:
                try:
                    proc.kill()
                    proc.wait(timeout=1.0)
                except Exception:
                    pass

    def run_checkpoint_5_backup_and_storage_boundary(self) -> Dict[str, Any]:
        """
        Checkpoint 5: Online backup API and storage boundary verification.
        Uses SQLite online backup API to copy DB to clean destination and verifies invariant.
        """
        if os.path.exists(self.backup_path):
            try:
                os.remove(self.backup_path)
            except OSError:
                pass

        src_conn = sqlite3.connect(self.db_path, isolation_level=None)
        dst_conn = sqlite3.connect(self.backup_path, isolation_level=None)

        try:
            # Execute online backup
            src_conn.backup(dst_conn, pages=0)
            dst_conn.close()
            src_conn.close()

            # Reopen backup destination
            verify_conn = sqlite3.connect(self.backup_path, isolation_level=None)
            cur = verify_conn.cursor()
            cur.execute("SELECT id, balance FROM accounts ORDER BY id ASC;")
            backup_balances = dict(cur.fetchall())
            verify_conn.close()

            backup_file_size = os.path.getsize(self.backup_path) if os.path.exists(self.backup_path) else 0
            passed = (backup_balances == {"A": 600, "B": 400} and sum(backup_balances.values()) == 1000)

            return {
                "checkpoint": 5,
                "name": "Backup & Storage Boundary Verification",
                "passed": passed,
                "backup_path": self.backup_path,
                "backup_file_size_bytes": backup_file_size,
                "backup_balances": backup_balances,
                "invariant_total": sum(backup_balances.values()),
            }

        finally:
            # Cleanup backup file after verification
            if os.path.exists(self.backup_path):
                try:
                    os.remove(self.backup_path)
                except OSError:
                    pass

    def run_all(self, verbose: bool = True) -> Dict[str, Any]:
        """Executes all 5 checkpoints end-to-end and returns full structured report."""
        meta = self.init_database()
        if verbose:
            print("=" * 68)
            print(" LAB-REQ-05: SQLite Transactions, Isolation & Recovery")
            print("=" * 68)
            print(f" Host: {meta['platform']}")
            print(f" Python: {meta['python_version']} | Embedded SQLite: {meta['sqlite_version']}")
            print(f" Journal Mode: {meta['journal_mode']} | Synchronous: {meta['synchronous']}")
            print("-" * 68)

        cp1 = self.run_checkpoint_1_committed_visibility()
        if verbose:
            print(f" [CP 1] {cp1['name']}: {'PASS' if cp1['passed'] else 'FAIL'}")
            print(f"        Conn 1 uncommitted: {cp1['conn1_uncommitted_value']}, Conn 2 observed: {cp1['conn2_observed_value']}")

        cp2 = self.run_checkpoint_2_bounded_writer_conflict()
        if verbose:
            print(f" [CP 2] {cp2['name']}: {'PASS' if cp2['passed'] else 'FAIL'}")
            print(f"        Conflict caught: {cp2['conflict_caught']} ({cp2['error_details']['error_type']}: {cp2['error_details']['error_message']})")

        cp3 = self.run_checkpoint_3_explicit_rollback()
        if verbose:
            print(f" [CP 3] {cp3['name']}: {'PASS' if cp3['passed'] else 'FAIL'}")
            print(f"        Post-rollback balances: {cp3['conn1_balances']}, Invariant Sum: {cp3['invariant_total']}")

        cp4 = self.run_checkpoint_4_child_interruption_recovery()
        if verbose:
            print(f" [CP 4] {cp4['name']}: {'PASS' if cp4['passed'] else 'FAIL'}")
            print(f"        Child PID: {cp4['child_pid']}, Reaped exitcode: {cp4['child_reaped_returncode']}")
            print(f"        Recovered balances: {cp4['recovered_balances']}, Total: {cp4['invariant_total']}")
            print(f"        Inference limit: {cp4['inference_limit']}")

        cp5 = self.run_checkpoint_5_backup_and_storage_boundary()
        if verbose:
            print(f" [CP 5] {cp5['name']}: {'PASS' if cp5['passed'] else 'FAIL'}")
            print(f"        Backup balances: {cp5['backup_balances']}, Total: {cp5['invariant_total']}")
            print("=" * 68)

        all_passed = all([cp1["passed"], cp2["passed"], cp3["passed"], cp4["passed"], cp5["passed"]])
        return {
            "meta": meta,
            "overall_passed": all_passed,
            "checkpoints": {
                "cp1": cp1,
                "cp2": cp2,
                "cp3": cp3,
                "cp4": cp4,
                "cp5": cp5,
            },
        }
