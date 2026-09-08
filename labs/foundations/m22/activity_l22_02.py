#!/usr/bin/env python3
"""
labs/foundations/m22/activity_l22_02.py — Safe Localhost Web Security & Composition Fixture
==========================================================================================

Course-owned, synthetic educational harness for L22-02: "Why is my web app vulnerable?"
Uses Python standard library only (http.server, urllib, sqlite3, socket, threading, ipaddress).

Demonstrates:
1. SQL Injection vs Parameterized Driver Binding:
   - In-memory SQLite database (:memory:);
   - Unsafe query concatenation (data enters interpreter as syntax);
   - Safe parameterized binding (? placeholder; driver binds value strictly as literal data).
2. CSRF Defenses & Ambient Authority Boundaries:
   - Cookie-based authentication vs ambient authority;
   - SameSite cookie policies;
   - Origin / Referer header verification;
   - Anti-CSRF synchronizer token verification.
3. SSRF Defenses & Network Egress Boundaries:
   - URL parsing & destination IP validation (RFC 1918, RFC 3927, loopback, link-local);
   - Mitigation of DNS Rebinding (TOCTOU race) via post-resolution socket connection;
   - Synthetic target isolation (zero contact with real cloud metadata or public servers).
4. Lifecycle & Fail-Closed Teardown:
   - Web server binds exclusively to ("127.0.0.1", 0) ephemeral port;
   - Explicit thread ownership and deterministic stop;
   - Fail-closed socket release verification.
"""

from __future__ import annotations

import http.server
import ipaddress
import json
import socket
import sqlite3
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Set, Tuple


# -----------------------------------------------------------------------------
# Part 1: SQL Code-vs-Data Separation (sqlite3 in-memory)
# -----------------------------------------------------------------------------

def setup_synthetic_database() -> sqlite3.Connection:
    """Sets up an in-memory SQLite database populated with synthetic records."""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT NOT NULL,
            account_balance INTEGER NOT NULL
        )
    """)
    cur.executemany("""
        INSERT INTO users (id, username, role, email, account_balance)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, "alice", "admin", "alice@example.local", 5000),
        (2, "bob", "user", "bob@example.local", 120),
        (3, "charlie", "user", "charlie@example.local", 350),
    ])
    conn.commit()
    return conn


def query_user_unsafe(conn: sqlite3.Connection, username_input: str) -> List[Tuple[Any, ...]]:
    """
    VULNERABLE: Direct string concatenation into SQL command stream.

    Flaw:
    Input is concatenated into SQL text before lexing and parsing.
    Quotes close string literal prematurely; injected tokens (OR, --)
    become boolean operators in the query AST.
    """
    cur = conn.cursor()
    query = f"SELECT id, username, role, email, account_balance FROM users WHERE username = '{username_input}'"
    cur.execute(query)
    return cur.fetchall()


def query_user_safe(conn: sqlite3.Connection, username_input: str) -> List[Tuple[Any, ...]]:
    """
    SECURE: Parameterized query using driver/API binding contract.

    Guarantees:
    Query structure is fixed with '?' placeholder. The SQL compiler
    evaluates '?' strictly as a parameter value position. The driver
    passes username_input as literal string data, immune to SQL syntax injection.
    """
    cur = conn.cursor()
    query = "SELECT id, username, role, email, account_balance FROM users WHERE username = ?"
    cur.execute(query, (username_input,))
    return cur.fetchall()


# -----------------------------------------------------------------------------
# Part 2: Safe SSRF Client (URL Validation + Post-Resolution Socket Egress)
# -----------------------------------------------------------------------------

DISALLOWED_IPV4_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),          # RFC 1918 Private
    ipaddress.ip_network("127.0.0.0/8"),         # Loopback
    ipaddress.ip_network("169.254.0.0/16"),      # RFC 3927 Link-Local / Cloud Metadata
    ipaddress.ip_network("172.16.0.0/12"),       # RFC 1918 Private
    ipaddress.ip_network("192.168.0.0/16"),      # RFC 1918 Private
    ipaddress.ip_network("224.0.0.0/4"),         # Multicast
    ipaddress.ip_network("240.0.0.0/4"),         # Reserved
]

DISALLOWED_IPV6_NETWORKS = [
    ipaddress.ip_network("::1/128"),             # Loopback
    ipaddress.ip_network("fc00::/7"),            # Unique Local Address (ULA)
    ipaddress.ip_network("fe80::/10"),           # Link-Local
]


def is_ip_disallowed(ip_str: str, allow_loopback_for_testing: bool = False) -> Tuple[bool, str]:
    """
    Evaluates whether an IP address belongs to private, loopback, or metadata networks.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return True, f"Invalid IP address format: '{ip_str}'"

    if ip.is_loopback:
        if allow_loopback_for_testing:
            return False, "Loopback explicitly allowed for synthetic test harness"
        return True, "Loopback address is forbidden (SSRF risk)"

    if ip.is_private:
        return True, "Private RFC 1918 / ULA address is forbidden (SSRF risk)"
    if ip.is_link_local:
        return True, "Link-local / cloud metadata address (169.254.x.x) is forbidden (SSRF risk)"
    if ip.is_multicast or ip.is_reserved or ip.is_unspecified:
        return True, "Multicast or reserved IP address is forbidden"

    if ip.version == 4:
        for net in DISALLOWED_IPV4_NETWORKS:
            if ip in net:
                if net == ipaddress.ip_network("127.0.0.0/8") and allow_loopback_for_testing:
                    continue
                return True, f"IP belongs to disallowed network {net}"
    elif ip.version == 6:
        for net in DISALLOWED_IPV6_NETWORKS:
            if ip in net:
                if net == ipaddress.ip_network("::1/128") and allow_loopback_for_testing:
                    continue
                return True, f"IP belongs to disallowed network {net}"

    return False, "Destination IP address is permitted"


def validate_and_resolve_destination(
    target_url: str,
    allowed_schemes: Tuple[str, ...] = ("http", "https"),
    allow_loopback_for_testing: bool = False,
) -> Tuple[bool, str, Optional[str], Optional[int], Optional[str]]:
    """
    Parses URL, enforces scheme, resolves DNS, and validates resolved IP.

    Returns:
    (is_valid, message, resolved_ip, port, hostname)
    """
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in allowed_schemes:
        return False, f"Forbidden scheme '{parsed.scheme}'; expected {allowed_schemes}", None, None, None

    hostname = parsed.hostname
    if not hostname:
        return False, "Missing hostname in URL", None, None, None

    port = parsed.port or (443 if parsed.scheme == "https" else 80)

    # Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror as exc:
        return False, f"DNS resolution failed for '{hostname}': {exc}", None, None, None

    if not addr_info:
        return False, f"No IP addresses resolved for '{hostname}'", None, None, None

    # Inspect all resolved IPs; fail closed if any resolved IP is disallowed
    resolved_ip = None
    for item in addr_info:
        sockaddr = item[4]
        ip_candidate = sockaddr[0]
        disallowed, reason = is_ip_disallowed(ip_candidate, allow_loopback_for_testing=allow_loopback_for_testing)
        if disallowed:
            return False, f"Resolution for '{hostname}' returned prohibited IP '{ip_candidate}': {reason}", None, None, None
        if resolved_ip is None:
            resolved_ip = ip_candidate

    return True, "Destination validated", resolved_ip, port, hostname


def safe_http_fetch_over_socket(
    target_url: str,
    allow_loopback_for_testing: bool = True,
    timeout: float = 2.0,
) -> Tuple[bool, int, str]:
    """
    Executes a safe outbound HTTP fetch addressing DNS Rebinding.

    Mitigation:
    1. Resolve DNS and validate IP address;
    2. Open socket connection DIRECTLY to the validated IP;
    3. Send HTTP request specifying the original hostname in the 'Host' header;
    4. Do not allow subsequent DNS resolution to alter the connection target.
    """
    is_valid, msg, validated_ip, port, hostname = validate_and_resolve_destination(
        target_url, allow_loopback_for_testing=allow_loopback_for_testing
    )
    if not is_valid or not validated_ip or not port or not hostname:
        return False, 403, f"SSRF Check Blocked: {msg}"

    parsed = urllib.parse.urlparse(target_url)
    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"

    # Connect socket directly to validated IP (mitigating DNS rebinding TOCTOU)
    try:
        with socket.create_connection((validated_ip, port), timeout=timeout) as sock:
            http_request = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {hostname}:{port}\r\n"
                f"User-Agent: EssentialCS-SafeFetcher/1.0\r\n"
                f"Connection: close\r\n\r\n"
            ).encode("utf-8")
            sock.sendall(http_request)

            # Read response
            response_bytes = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_bytes += chunk
                if len(response_bytes) > 65536:  # Bounded response size
                    break

        # Basic HTTP response parsing
        response_text = response_bytes.decode("utf-8", errors="replace")
        status_line = response_text.split("\r\n", 1)[0]
        status_parts = status_line.split(" ")
        status_code = int(status_parts[1]) if len(status_parts) >= 2 and status_parts[1].isdigit() else 500

        body = ""
        if "\r\n\r\n" in response_text:
            body = response_text.split("\r\n\r\n", 1)[1]

        return True, status_code, body
    except Exception as exc:
        return False, 502, f"Egress connection error to {validated_ip}:{port}: {exc}"


# -----------------------------------------------------------------------------
# Part 3: Localhost HTTP Server with CSRF & SameSite Defenses
# -----------------------------------------------------------------------------

class WebSecurityHarnessHandler(http.server.BaseHTTPRequestHandler):
    """
    Localhost HTTP handler demonstrating CSRF validation and parameterized endpoints.
    """

    # Shared in-memory state
    active_sessions: Dict[str, str] = {}         # session_token -> username
    session_csrf_tokens: Dict[str, str] = {}     # session_token -> csrf_token
    user_emails: Dict[str, str] = {
        "alice": "alice@example.local",
        "bob": "bob@example.local",
    }
    server_origin: str = ""                      # e.g., "http://127.0.0.1:port"

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress default stdout logging for clean test output."""
        return

    def _parse_cookies(self) -> Dict[str, str]:
        cookie_header = self.headers.get("Cookie", "")
        cookies = {}
        for item in cookie_header.split(";"):
            if "=" in item:
                k, v = item.strip().split("=", 1)
                cookies[k] = v
        return cookies

    def _send_json(self, status: int, data: Dict[str, Any], extra_headers: Optional[Dict[str, str]] = None) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if extra_headers:
            for hk, hv in extra_headers.items():
                self.send_header(hk, hv)
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)

        # 1. Endpoint: /login (issues session cookie + anti-CSRF token)
        if parsed_url.path == "/login":
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            username = payload.get("username")
            if username not in ("alice", "bob"):
                self._send_json(401, {"error": "Invalid synthetic credentials"})
                return

            import secrets
            session_id = secrets.token_hex(16)
            csrf_token = secrets.token_hex(16)
            self.active_sessions[session_id] = username
            self.session_csrf_tokens[session_id] = csrf_token

            # Set-Cookie with SameSite=Lax; HttpOnly
            cookie_hdr = f"session_id={session_id}; Path=/; HttpOnly; SameSite=Lax"
            self._send_json(
                200,
                {"status": "logged_in", "username": username, "csrf_token": csrf_token},
                extra_headers={"Set-Cookie": cookie_hdr},
            )
            return

        # 2. Endpoint: /update_email (Demonstrates CSRF defenses)
        if parsed_url.path == "/update_email":
            cookies = self._parse_cookies()
            session_id = cookies.get("session_id")
            if not session_id or session_id not in self.active_sessions:
                self._send_json(401, {"error": "Unauthenticated: Missing or invalid session cookie"})
                return

            username = self.active_sessions[session_id]
            expected_csrf = self.session_csrf_tokens.get(session_id)

            # Defensive Check 1: Origin / Referer validation
            origin_header = self.headers.get("Origin") or self.headers.get("Referer", "")
            if origin_header and self.server_origin:
                if not origin_header.startswith(self.server_origin):
                    self._send_json(
                        403,
                        {"error": "CSRF Blocked: Cross-Origin request rejected by Origin policy", "origin": origin_header},
                    )
                    return

            # Defensive Check 2: Anti-CSRF synchronizer token
            length = int(self.headers.get("Content-Length", 0))
            post_data = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            submitted_csrf = self.headers.get("X-CSRF-Token") or post_data.get("csrf_token")

            if not submitted_csrf or submitted_csrf != expected_csrf:
                self._send_json(
                    403,
                    {"error": "CSRF Blocked: Missing or mismatched Anti-CSRF token"},
                )
                return

            # Validated: Perform state update
            new_email = post_data.get("email", "")
            self.user_emails[username] = new_email
            self._send_json(200, {"status": "email_updated", "user": username, "email": new_email})
            return

        # 3. Synthetic Target Endpoint for SSRF testing: /synthetic_internal
        if parsed_url.path == "/synthetic_internal":
            self._send_json(200, {"message": "Synthetic internal endpoint reached", "secret": "INTERNAL_KEY_9982"})
            return

        self._send_json(404, {"error": "Endpoint not found"})

    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/synthetic_internal":
            self._send_json(200, {"message": "Synthetic internal endpoint reached", "secret": "INTERNAL_KEY_9982"})
            return
        if parsed_url.path == "/status":
            self._send_json(200, {"status": "ok", "time": int(time.time())})
            return
        self._send_json(404, {"error": "Not found"})


class SafeLocalhostServer:
    """
    Managed localhost HTTP server running on an ephemeral port.

    Guarantees:
    - Binds strictly to ("127.0.0.1", 0);
    - Explicit server thread lifecycle;
    - Fail-closed teardown sequence with post-teardown socket verification.
    """

    def __init__(self) -> None:
        self.server: Optional[http.server.HTTPServer] = None
        self.thread: Optional[threading.Thread] = None
        self.port: int = 0
        self.origin: str = ""

    def start(self) -> None:
        # Bind exclusively to 127.0.0.1 on ephemeral port 0
        self.server = http.server.HTTPServer(("127.0.0.1", 0), WebSecurityHarnessHandler)
        self.port = self.server.server_port
        self.origin = f"http://127.0.0.1:{self.port}"
        WebSecurityHarnessHandler.server_origin = self.origin

        self.thread = threading.Thread(target=self.server.serve_forever, daemon=False)
        self.thread.start()

        # Verify listener is active
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe.settimeout(1.0)
        try:
            probe.connect(("127.0.0.1", self.port))
            probe.close()
        except Exception as exc:
            self.stop()
            raise RuntimeError(f"Server failed to bind and listen on port {self.port}: {exc}")

    def stop(self, timeout: float = 2.0) -> None:
        """
        Deterministic fail-closed teardown sequence:
        1. shutdown() stops request processing loop;
        2. server_close() closes listener socket;
        3. join() waits for thread exit;
        4. Verifies listener socket is released.
        """
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=timeout)
            if self.thread.is_alive():
                raise RuntimeError("FAIL / BLOCKED: Server thread failed to terminate within timeout")

        # Verify port release
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_sock.settimeout(0.5)
        try:
            test_sock.connect(("127.0.0.1", self.port))
            test_sock.close()
            raise RuntimeError(f"FAIL / BLOCKED: Port {self.port} remains open after server shutdown")
        except (ConnectionRefusedError, OSError):
            # Port released successfully
            pass
        finally:
            test_sock.close()


# -----------------------------------------------------------------------------
# Self-Test / CLI Demonstration
# -----------------------------------------------------------------------------

def run_demonstration() -> None:
    print("=" * 78)
    print("  L22-02 DEMONSTRATION: SAFE LOCALHOST WEB SECURITY & COMPOSITION")
    print("=" * 78)

    # 1. SQL Injection vs Parameterization
    print("\n[1] Testing SQL Code vs Data Boundary (sqlite3):")
    db = setup_synthetic_database()

    payload = "admin' OR '1'='1"
    print(f"    Payload: {payload}")

    # Unsafe query extracts all records
    leaked_records = query_user_unsafe(db, payload)
    print(f"    Unsafe Query Result: Leaked {len(leaked_records)} user records (INJECTION SUCCESSFUL)")
    assert len(leaked_records) > 1

    # Safe parameterized query returns 0 records
    safe_records = query_user_safe(db, payload)
    print(f"    Safe Query Result:   Returned {len(safe_records)} records (IMMUNE TO INJECTION)")
    assert len(safe_records) == 0

    # Normal user query works correctly
    alice_record = query_user_safe(db, "alice")
    print(f"    Normal Query 'alice': Found {len(alice_record)} record (username={alice_record[0][1]})")
    assert len(alice_record) == 1
    db.close()

    # 2. SSRF Destination Validation
    print("\n[2] Testing SSRF Destination & IP Filtering:")
    disallowed_urls = [
        "http://169.254.169.254/latest/meta-data/",  # Cloud Metadata
        "http://10.0.0.1/admin",                     # RFC 1918 Private
        "http://192.168.1.1/router",                 # RFC 1918 Private
        "http://127.0.0.1:8080/internal",            # Loopback (production policy)
    ]
    for url in disallowed_urls:
        ok, msg, _, _, _ = validate_and_resolve_destination(url, allow_loopback_for_testing=False)
        print(f"    SSRF Check '{url[:30]}...': is_valid={ok} ({msg[:45]}...)")
        assert ok is False

    # 3. Localhost Web Server Lifecycle & CSRF
    print("\n[3] Testing Localhost Server Lifecycle & CSRF Defenses:")
    server = SafeLocalhostServer()
    server.start()
    print(f"    Server bound to ephemeral port {server.port} on 127.0.0.1")

    try:
        # Safe SSRF test against synthetic internal endpoint (loopback allowed for test)
        internal_url = f"{server.origin}/synthetic_internal"
        ok, status, body = safe_http_fetch_over_socket(internal_url, allow_loopback_for_testing=True)
        print(f"    Safe fetch over socket to synthetic target: status={status}, ok={ok}")
        assert ok is True and status == 200

        # Attempt CSRF without token
        # Login first
        login_req = urllib.request.Request(
            f"{server.origin}/login",
            data=json.dumps({"username": "alice"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(login_req) as resp:
            login_data = json.loads(resp.read().decode("utf-8"))
            cookie = resp.headers.get("Set-Cookie")
            csrf_token = login_data["csrf_token"]
        print(f"    Logged in as alice; received session cookie and anti-CSRF token")

        # Malicious cross-origin POST without CSRF token
        bad_req = urllib.request.Request(
            f"{server.origin}/update_email",
            data=json.dumps({"email": "attacker@evil.local"}).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Cookie": cookie,
                "Origin": "http://evil-attacker.local",
            },
        )
        try:
            urllib.request.urlopen(bad_req)
            raise AssertionError("CSRF request should have failed!")
        except urllib.error.HTTPError as err:
            print(f"    Cross-Origin POST without valid Origin/CSRF: Rejected with HTTP {err.code} (PASS)")
            assert err.code == 403

        # Legitimate POST with matching Origin and CSRF token
        good_req = urllib.request.Request(
            f"{server.origin}/update_email",
            data=json.dumps({"email": "alice_new@example.local", "csrf_token": csrf_token}).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Cookie": cookie,
                "Origin": server.origin,
                "X-CSRF-Token": csrf_token,
            },
        )
        with urllib.request.urlopen(good_req) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            print(f"    Legitimate POST with CSRF token: HTTP {resp.status} status={resp_data['status']}")
            assert resp.status == 200

    finally:
        print("    Executing deterministic fail-closed teardown...")
        server.stop()
        print("    Server stopped and listener port release verified.")

    print("\n" + "=" * 78)
    print("  L22-02 ACTIVITY CONTRACT VERIFIED.")
    print("=" * 78)


if __name__ == "__main__":
    run_demonstration()
