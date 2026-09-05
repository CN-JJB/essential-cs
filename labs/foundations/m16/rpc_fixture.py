#!/usr/bin/env python3
"""
Course-owned localhost RPC, Partial-Failure Shim & Idempotency Fixture.
Module M16: Distributed Systems Foundations — Partial Failure & RPC.

Architectural invariants:
1. Localhost only ('127.0.0.1'), ephemeral OS-assigned ports (port=0).
2. Explicit length-prefixed framing (>I + UTF-8 JSON); does NOT rely on TCP recv boundaries.
3. Application-layer fault injection shim (DELAY/DROP request/response); explicitly labeled
   as application behavior, NEVER literal packet loss.
4. Explicit shutdown ownership: server sockets closed, client sockets closed, worker
   threads joined; no daemon-thread-exit-as-cleanup.
5. Configurable harness safety watchdog (not a networking constant).
6. Atomic SQLite-backed idempotency store with dedicated per-transaction connections
   and explicit retention/eviction boundary.
"""

import json
import os
import random
import select
import socket
import sqlite3
import struct
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


def recv_exact(sock: socket.socket, n: int) -> bytes:
    """
    Read exactly n bytes from a TCP socket.
    Guarantees message assembly across arbitrary TCP segmentation and window fragmentation.
    """
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError(
                f"Unexpected EOF reading socket stream: expected {n} bytes, received {len(buf)}"
            )
        buf.extend(chunk)
    return bytes(buf)


def send_msg(sock: socket.socket, payload: dict) -> None:
    """Encode a dict as JSON and send with a 4-byte big-endian length prefix."""
    raw = json.dumps(payload).encode("utf-8")
    header = struct.pack(">I", len(raw))
    sock.sendall(header + raw)


def recv_msg(sock: socket.socket) -> dict:
    """Read a 4-byte big-endian length prefix and decode the JSON payload."""
    header = recv_exact(sock, 4)
    length = struct.unpack(">I", header)[0]
    raw = recv_exact(sock, length)
    return json.loads(raw.decode("utf-8"))


class FaultAction:
    """Application-layer fault injection actions."""
    NONE = "NONE"
    DELAY_REQUEST = "DELAY_REQUEST"
    DROP_REQUEST = "DROP_REQUEST"
    DELAY_RESPONSE = "DELAY_RESPONSE"
    DROP_RESPONSE = "DROP_RESPONSE"


class FaultShim:
    """
    Application-layer fault injection shim.
    Operates strictly in user-space application logic.
    MANDATORY LABEL: APPLICATION-LAYER SIMULATION ONLY, NOT LITERAL PACKET LOSS.
    """

    def __init__(self):
        self._lock = threading.Lock()
        # Rules: request_id -> (action, delay_seconds, trigger_count)
        self._rules: Dict[str, Dict[str, Any]] = {}
        self._rule_call_counts: Dict[str, int] = {}
        self._execution_events: Dict[str, threading.Event] = {}

    def set_rule(
        self,
        request_id: str,
        action: str,
        delay_seconds: float = 0.0,
        max_triggers: int = 1,
    ) -> None:
        with self._lock:
            self._rules[request_id] = {
                "action": action,
                "delay_seconds": delay_seconds,
                "max_triggers": max_triggers,
            }
            self._rule_call_counts[request_id] = 0

    def get_execution_event(self, request_id: str) -> threading.Event:
        with self._lock:
            if request_id not in self._execution_events:
                self._execution_events[request_id] = threading.Event()
            return self._execution_events[request_id]

    def notify_server_executed(self, request_id: str) -> None:
        with self._lock:
            event = self._execution_events.get(request_id)
            if event:
                event.set()

    def check_request_fault(self, request_id: str) -> Tuple[str, float]:
        with self._lock:
            rule = self._rules.get(request_id)
            if not rule:
                return (FaultAction.NONE, 0.0)
            action = rule["action"]
            if action in (FaultAction.DELAY_REQUEST, FaultAction.DROP_REQUEST):
                if self._rule_call_counts[request_id] < rule["max_triggers"]:
                    self._rule_call_counts[request_id] += 1
                    return (action, rule["delay_seconds"])
            return (FaultAction.NONE, 0.0)

    def check_response_fault(self, request_id: str) -> Tuple[str, float]:
        with self._lock:
            rule = self._rules.get(request_id)
            if not rule:
                return (FaultAction.NONE, 0.0)
            action = rule["action"]
            if action in (FaultAction.DELAY_RESPONSE, FaultAction.DROP_RESPONSE):
                if self._rule_call_counts[request_id] < rule["max_triggers"]:
                    self._rule_call_counts[request_id] += 1
                    return (action, rule["delay_seconds"])
            return (FaultAction.NONE, 0.0)


class IdempotencyStore:
    """
    SQLite-backed deduplication store for atomic idempotency operations.
    Enforces atomic key claim and business state mutation in ONE transaction
    with explicit retention/eviction boundary.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        # Dedicated connection per transaction; isolation_level=None enables manual BEGIN IMMEDIATE
        conn = sqlite3.connect(self.db_path, timeout=10.0, isolation_level=None)
        conn.execute("PRAGMA busy_timeout = 10000")
        return conn

    def _init_db(self) -> None:
        conn = self._get_connection()
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS idempotency_keys (
                    key TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    response_json TEXT,
                    created_at REAL NOT NULL,
                    expires_at REAL NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS business_counter (
                    name TEXT PRIMARY KEY,
                    val INTEGER NOT NULL
                )
                """
            )
            # Initialize default counter if not present
            conn.execute(
                """
                INSERT OR IGNORE INTO business_counter (name, val) VALUES ('primary', 0)
                """
            )
        finally:
            conn.close()

    def execute_with_idempotency(
        self,
        key: str,
        mutation_fn: Callable[[sqlite3.Connection], Any],
        ttl_seconds: float = 3600.0,
    ) -> Tuple[Any, bool, bool]:
        """
        Atomically executes mutation_fn if key has not been processed.
        Returns: (result, is_duplicate, was_executed)
        """
        conn = self._get_connection()
        now = time.time()
        expires_at = now + ttl_seconds
        try:
            conn.execute("BEGIN IMMEDIATE")
            cur = conn.cursor()
            cur.execute(
                "SELECT status, response_json, expires_at FROM idempotency_keys WHERE key = ?",
                (key,),
            )
            row = cur.fetchone()

            if row:
                status, cached_json, row_expires = row
                # Check retention boundary
                if now > row_expires:
                    # Expired entry: purge and allow re-execution
                    cur.execute("DELETE FROM idempotency_keys WHERE key = ?", (key,))
                elif status == "COMPLETED":
                    conn.execute("COMMIT")
                    cached_result = json.loads(cached_json) if cached_json else None
                    return (cached_result, True, False)
                elif status == "IN_PROGRESS":
                    conn.execute("ROLLBACK")
                    raise RuntimeError(f"Concurrent in-flight duplicate for key '{key}'")

            # Key claim + business mutation in ONE atomic transaction
            cur.execute(
                """
                INSERT INTO idempotency_keys (key, status, response_json, created_at, expires_at)
                VALUES (?, 'IN_PROGRESS', NULL, ?, ?)
                """,
                (key, now, expires_at),
            )

            # Perform the business mutation passing the open transaction connection
            result = mutation_fn(conn)

            # Mark completed and store response
            res_json = json.dumps(result)
            cur.execute(
                """
                UPDATE idempotency_keys
                SET status = 'COMPLETED', response_json = ?
                WHERE key = ?
                """,
                (res_json, key),
            )
            conn.execute("COMMIT")
            return (result, False, True)
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            raise
        finally:
            conn.close()

    def get_counter_value(self, name: str = "primary") -> int:
        conn = self._get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT val FROM business_counter WHERE name = ?", (name,))
            row = cur.fetchone()
            return row[0] if row else 0
        finally:
            conn.close()

    def increment_counter_raw(self, name: str = "primary", delta: int = 1) -> int:
        """Unsafe business mutation: increments counter directly without idempotency check."""
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE")
            cur = conn.cursor()
            cur.execute(
                "UPDATE business_counter SET val = val + ? WHERE name = ?",
                (delta, name),
            )
            cur.execute("SELECT val FROM business_counter WHERE name = ?", (name,))
            val = cur.fetchone()[0]
            conn.execute("COMMIT")
            return val
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            raise
        finally:
            conn.close()

    def purge_expired(self, current_time: Optional[float] = None) -> int:
        """Purges expired keys past the retention horizon."""
        if current_time is None:
            current_time = time.time()
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE")
            cur = conn.cursor()
            cur.execute("DELETE FROM idempotency_keys WHERE expires_at <= ?", (current_time,))
            count = cur.rowcount
            conn.execute("COMMIT")
            return count
        finally:
            conn.close()


class RPCServer:
    """
    Course-owned localhost RPC server.
    Binds to 127.0.0.1:0 (ephemeral OS port).
    Explicit thread shutdown, socket cleanup, and bounded watchdog.
    """

    def __init__(
        self,
        fault_shim: Optional[FaultShim] = None,
        idempotency_store: Optional[IdempotencyStore] = None,
        watchdog_timeout: float = 15.0,
    ):
        self.fault_shim = fault_shim or FaultShim()
        self.idempotency_store = idempotency_store
        self.watchdog_timeout = watchdog_timeout

        self._server_sock: Optional[socket.socket] = None
        self.host: str = "127.0.0.1"
        self.port: int = 0
        self._stop_event = threading.Event()
        self._listener_thread: Optional[threading.Thread] = None
        self._client_sockets: List[socket.socket] = []
        self._client_threads: List[threading.Thread] = []
        self._lock = threading.Lock()

        # Audit log: records events on server
        self.audit_log: List[Dict[str, Any]] = []

        # Registered business methods: method_name -> Callable[[dict], Any]
        self._methods: Dict[str, Callable[..., Any]] = {}
        self._register_default_methods()

    def _register_default_methods(self) -> None:
        self.register_method("ping", lambda params: "pong")
        self.register_method("unsafe_increment", self._method_unsafe_increment)
        self.register_method("protected_increment", self._method_protected_increment)

    def register_method(self, name: str, handler: Callable[..., Any]) -> None:
        self._methods[name] = handler

    def _method_unsafe_increment(self, params: dict) -> dict:
        delta = params.get("delta", 1)
        name = params.get("name", "primary")
        if self.idempotency_store:
            val = self.idempotency_store.increment_counter_raw(name=name, delta=delta)
        else:
            val = delta
        return {"counter": val, "executed": True, "mode": "UNSAFE"}

    def _method_protected_increment(self, params: dict) -> dict:
        key = params.get("idempotency_key")
        if not key:
            raise ValueError("Protected mutation requires 'idempotency_key'")
        delta = params.get("delta", 1)
        name = params.get("name", "primary")

        if not self.idempotency_store:
            raise RuntimeError("IdempotencyStore not configured on server")

        def _mutate(conn: sqlite3.Connection):
            cur = conn.cursor()
            cur.execute(
                "UPDATE business_counter SET val = val + ? WHERE name = ?",
                (delta, name),
            )
            cur.execute("SELECT val FROM business_counter WHERE name = ?", (name,))
            return cur.fetchone()[0]

        result_val, is_dup, was_exec = self.idempotency_store.execute_with_idempotency(
            key=key,
            mutation_fn=_mutate,
            ttl_seconds=params.get("ttl_seconds", 3600.0),
        )
        return {
            "counter": result_val,
            "is_duplicate": is_dup,
            "executed": was_exec,
            "idempotency_key": key,
            "mode": "PROTECTED",
        }

    def start(self) -> int:
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.bind((self.host, 0))
        self.port = self._server_sock.getsockname()[1]
        self._server_sock.listen(128)
        self._server_sock.settimeout(0.5)

        self._stop_event.clear()
        self._listener_thread = threading.Thread(
            target=self._listen_loop,
            name=f"RPCServer-Listener-{self.port}",
        )
        self._listener_thread.start()
        return self.port

    def _listen_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                client_sock, addr = self._server_sock.accept()
                client_sock.settimeout(5.0)
                with self._lock:
                    self._client_sockets.append(client_sock)
                t = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, addr),
                    name=f"RPCServer-Worker-{addr}",
                )
                with self._lock:
                    self._client_threads.append(t)
                t.start()
            except socket.timeout:
                continue
            except OSError:
                break

    def _handle_client(self, client_sock: socket.socket, addr: Tuple[str, int]) -> None:
        try:
            while not self._stop_event.is_set():
                try:
                    req = recv_msg(client_sock)
                except (ConnectionError, EOFError, socket.timeout):
                    break

                req_id = req.get("request_id", "unknown")
                method_name = req.get("method", "")
                params = req.get("params", {})

                # 1. Fault check on request
                req_action, req_delay = self.fault_shim.check_request_fault(req_id)
                if req_action == FaultAction.DROP_REQUEST:
                    self.audit_log.append({
                        "request_id": req_id,
                        "event": "REQUEST_DROPPED_BY_SHIM",
                        "timestamp": time.time(),
                        "label": "APPLICATION-LAYER SIMULATION ONLY (NOT PACKET LOSS)",
                    })
                    break  # Close socket without processing
                elif req_action == FaultAction.DELAY_REQUEST and req_delay > 0:
                    time.sleep(req_delay)

                # 2. Execute business logic
                handler = self._methods.get(method_name)
                start_exec = time.time()
                try:
                    if handler is None:
                        resp = {
                            "request_id": req_id,
                            "status": "ERROR",
                            "error": f"Method '{method_name}' not found",
                            "server_time": time.time(),
                        }
                    else:
                        res = handler(params)
                        resp = {
                            "request_id": req_id,
                            "status": "OK",
                            "result": res,
                            "server_time": time.time(),
                        }
                except Exception as e:
                    resp = {
                        "request_id": req_id,
                        "status": "ERROR",
                        "error": str(e),
                        "server_time": time.time(),
                    }

                end_exec = time.time()
                self.audit_log.append({
                    "request_id": req_id,
                    "method": method_name,
                    "event": "SERVER_COMPLETED_EXECUTION",
                    "start_time": start_exec,
                    "completion_time": end_exec,
                    "status": resp["status"],
                })

                # Notify synchronization event that server has executed business logic
                self.fault_shim.notify_server_executed(req_id)

                # 3. Fault check on response
                resp_action, resp_delay = self.fault_shim.check_response_fault(req_id)
                if resp_action == FaultAction.DROP_RESPONSE:
                    self.audit_log.append({
                        "request_id": req_id,
                        "event": "RESPONSE_DROPPED_BY_SHIM",
                        "timestamp": time.time(),
                        "label": "APPLICATION-LAYER SIMULATION ONLY (NOT PACKET LOSS)",
                    })
                    break  # Suppress response and close connection
                elif resp_action == FaultAction.DELAY_RESPONSE and resp_delay > 0:
                    time.sleep(resp_delay)

                try:
                    send_msg(client_sock, resp)
                except OSError:
                    break
        finally:
            try:
                client_sock.close()
            except OSError:
                pass
            with self._lock:
                if client_sock in self._client_sockets:
                    self._client_sockets.remove(client_sock)

    def stop(self) -> None:
        """Explicit shutdown: closes all sockets and joins all threads."""
        self._stop_event.set()
        if self._server_sock:
            try:
                self._server_sock.close()
            except OSError:
                pass
        with self._lock:
            for s in list(self._client_sockets):
                try:
                    s.close()
                except OSError:
                    pass
            self._client_sockets.clear()

        if self._listener_thread and self._listener_thread.is_alive():
            self._listener_thread.join(timeout=2.0)

        with self._lock:
            threads = list(self._client_threads)
        for t in threads:
            if t.is_alive():
                t.join(timeout=2.0)
        with self._lock:
            self._client_threads.clear()


class RetryPolicy:
    NO_RETRY = "NO_RETRY"
    DETERMINISTIC = "DETERMINISTIC"
    EXPONENTIAL_JITTER = "EXPONENTIAL_JITTER"


class RPCClient:
    """
    Course-owned localhost RPC client.
    Configurable deadline, strict attempt-budget enforcement, and named retry policies.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 0,
        default_timeout: float = 1.0,
    ):
        self.host = host
        self.port = port
        self.default_timeout = default_timeout
        self.call_traces: List[Dict[str, Any]] = []

    def call(
        self,
        method: str,
        params: dict,
        request_id: Optional[str] = None,
        timeout: Optional[float] = None,
        retry_policy: str = RetryPolicy.NO_RETRY,
        max_attempts: int = 1,
        base_backoff_ms: float = 50.0,
        max_backoff_ms: float = 500.0,
    ) -> dict:
        """
        Executes RPC with strict attempt-budget enforcement.
        Records detailed chronological attempt trace.
        """
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        call_timeout = timeout if timeout is not None else self.default_timeout
        req_id = request_id or f"req-{time.time_ns()}-{random.randint(1000, 9999)}"

        attempts_made = 0
        last_exception: Optional[Exception] = None

        while attempts_made < max_attempts:
            attempts_made += 1
            attempt_start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(call_timeout)

            attempt_record: Dict[str, Any] = {
                "request_id": req_id,
                "attempt": attempts_made,
                "method": method,
                "start_time": attempt_start,
                "timeout_configured": call_timeout,
                "retry_policy": retry_policy,
                "outcome": "UNKNOWN",
            }

            try:
                sock.connect((self.host, self.port))
                req_payload = {
                    "request_id": req_id,
                    "method": method,
                    "params": params,
                    "attempt": attempts_made,
                }
                send_msg(sock, req_payload)
                resp = recv_msg(sock)

                attempt_record["outcome"] = "SUCCESS"
                attempt_record["duration"] = time.time() - attempt_start
                attempt_record["response"] = resp
                self.call_traces.append(attempt_record)

                if resp.get("status") == "OK":
                    return resp
                else:
                    raise RuntimeError(f"RPC Server Error: {resp.get('error')}")

            except (socket.timeout, TimeoutError) as e:
                attempt_record["outcome"] = "TIMEOUT"
                attempt_record["duration"] = time.time() - attempt_start
                attempt_record["error_type"] = "TimeoutError"
                attempt_record["error_detail"] = str(e)
                self.call_traces.append(attempt_record)
                last_exception = TimeoutError(
                    f"Client stopped waiting for request '{req_id}' after {call_timeout}s"
                )

            except (ConnectionError, OSError) as e:
                attempt_record["outcome"] = "CONNECTION_ERROR"
                attempt_record["duration"] = time.time() - attempt_start
                attempt_record["error_type"] = type(e).__name__
                attempt_record["error_detail"] = str(e)
                self.call_traces.append(attempt_record)
                last_exception = e

            finally:
                try:
                    sock.close()
                except OSError:
                    pass

            # If we still have budget, apply backoff before next attempt
            if attempts_made < max_attempts:
                if retry_policy == RetryPolicy.NO_RETRY:
                    break
                elif retry_policy == RetryPolicy.DETERMINISTIC:
                    sleep_sec = base_backoff_ms / 1000.0
                elif retry_policy == RetryPolicy.EXPONENTIAL_JITTER:
                    # Full jitter formula: sleep = Uniform(0, min(max_backoff, base * 2^attempt))
                    cap_ms = min(max_backoff_ms, base_backoff_ms * (2 ** (attempts_made - 1)))
                    sleep_sec = random.uniform(0, cap_ms) / 1000.0
                else:
                    sleep_sec = 0.0

                attempt_record["backoff_applied_sec"] = sleep_sec
                time.sleep(sleep_sec)

        # If budget exhausted without success, raise the last encountered error
        if last_exception:
            raise last_exception
        raise RuntimeError(f"RPC call failed after {attempts_made} attempts without specific exception")
