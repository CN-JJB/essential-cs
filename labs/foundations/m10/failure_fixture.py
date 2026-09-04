#!/usr/bin/env python3
"""
M10 Lesson 3 Activity: Controlled Network Failure Fixture.

Demonstrates:
1. Active loopback refusal on verified unbound port (no port scanning, records actual host disposition).
2. Accepted-but-silent server triggering client read timeout (bounded deadline with outer watchdog).
3. Capability-gated DNS resolution failure observation using RFC 2606 reserved .invalid name.
4. Partial-failure ambiguity: client timeout vs remote execution uncertainty.

Adheres strictly to Essential CS invariants:
- No hardcoded errno acceptance value or fixed refusal exception class.
- No fixed latency or timeout ratio assertions.
- No fabricated error strings.
"""

import argparse
import json
import socket
import sys
import threading
import time


def observe_loopback_refusal():
    """
    Finds a verified unbound ephemeral port on 127.0.0.1 and attempts to connect.
    Records the actual connect_ex result or runtime exception, plus elapsed host evidence.
    """
    # Find an ephemeral port by binding to 0 and immediately closing
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.bind(("127.0.0.1", 0))
    _, unbound_port = probe.getsockname()
    probe.close()

    record = {
        "target": f"127.0.0.1:{unbound_port}",
        "disposition": None,
        "exception_type": None,
        "errno": None,
        "strerror": None,
        "elapsed_ms": None,
        "success": False,
    }

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(2.0)
    t0 = time.perf_counter()
    try:
        connect_result = client.connect_ex(("127.0.0.1", unbound_port))
        t1 = time.perf_counter()
        record["elapsed_ms"] = round((t1 - t0) * 1000.0, 3)
        record["connect_ex_result"] = connect_result
        if connect_result == 0:
            # Race: another local process acquired the just-released port.
            record["disposition"] = "UNEXPECTED_CONNECTION_SUCCESS"
        else:
            record["disposition"] = "UNBOUND_LOOPBACK_CONNECT_FAILURE_OBSERVED"
            record["success"] = True
    except Exception as exc:
        t1 = time.perf_counter()
        record["elapsed_ms"] = round((t1 - t0) * 1000.0, 3)
        record["disposition"] = "UNBOUND_LOOPBACK_CONNECT_EXCEPTION_OBSERVED"
        record["exception_type"] = type(exc).__name__
        record["errno"] = getattr(exc, "errno", None)
        record["strerror"] = str(exc)
        record["success"] = True
    finally:
        client.close()

    return record


def observe_read_timeout(client_deadline_s=0.25, harness_watchdog_s=3.0):
    """
    Starts an accepted-but-silent server on loopback port 0.
    The server accepts the TCP handshake but sends zero application bytes.
    The client sets a read deadline and records the runtime's timeout disposition.
    An outer harness watchdog is configured strictly to prevent hangs.
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.settimeout(harness_watchdog_s)
    server_sock.bind(("127.0.0.1", 0))
    server_sock.listen(1)
    bound_host, bound_port = server_sock.getsockname()

    record = {
        "target": f"{bound_host}:{bound_port}",
        "configured_read_deadline_s": client_deadline_s,
        "harness_watchdog_s": harness_watchdog_s,
        "disposition": None,
        "exception_type": None,
        "elapsed_ms": None,
        "success": False,
        "error": None,
    }

    server_shutdown_event = threading.Event()
    server_client_conn = []

    def silent_server_worker():
        try:
            conn, _ = server_sock.accept()
            server_client_conn.append(conn)
            # Deliberately withhold application bytes until shutdown signaled
            server_shutdown_event.wait(timeout=harness_watchdog_s)
        except Exception:
            pass
        finally:
            for c in server_client_conn:
                try:
                    c.close()
                except Exception:
                    pass

    srv_thread = threading.Thread(target=silent_server_worker, daemon=False)
    srv_thread.start()

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect is accepted by the server
        client_sock.connect((bound_host, bound_port))
        # Set the client-side read deadline
        client_sock.settimeout(client_deadline_s)

        t0 = time.perf_counter()
        try:
            # Client attempts to read from accepted but silent stream
            client_sock.recv(1024)
            record["disposition"] = "UNEXPECTED_BYTES_RECEIVED"
        except (TimeoutError, socket.timeout) as exc:
            t1 = time.perf_counter()
            record["disposition"] = "READ_TIMEOUT_OBSERVED"
            record["exception_type"] = type(exc).__name__
            record["elapsed_ms"] = round((t1 - t0) * 1000.0, 3)
            record["success"] = True
        except Exception as exc:
            record["disposition"] = "UNEXPECTED_EXCEPTION"
            record["exception_type"] = type(exc).__name__
            record["error"] = str(exc)
    except Exception as exc:
        record["error"] = f"Connect failure: {type(exc).__name__}: {exc}"
    finally:
        server_shutdown_event.set()
        try:
            client_sock.close()
        except Exception:
            pass
        try:
            server_sock.close()
        except Exception:
            pass
        srv_thread.join(timeout=min(harness_watchdog_s, 1.0))
        record["server_thread_reaped"] = not srv_thread.is_alive()
        if not record["server_thread_reaped"]:
            record["success"] = False
            record["error"] = "Silent-server worker did not terminate under teardown watchdog"

    return record


def observe_dns_failure(test_hostname="m10-lookup-test.invalid"):
    """
    Capability-gated DNS resolution failure observation using RFC 2606 .invalid TLD.
    Truthfully records live gaierror or reports NO LIVE DNS FAILURE OBSERVATION.
    """
    record = {
        "query_hostname": test_hostname,
        "disposition": None,
        "exception_type": None,
        "errno": None,
        "strerror": None,
        "success": False,
    }

    try:
        socket.getaddrinfo(test_hostname, 80, socket.AF_INET, socket.SOCK_STREAM)
        record["disposition"] = "UNEXPECTED_RESOLUTION_SUCCESS"
    except socket.gaierror as exc:
        record["disposition"] = "LIVE_DNS_FAILURE_OBSERVED"
        record["exception_type"] = type(exc).__name__
        record["errno"] = getattr(exc, "errno", None)
        record["strerror"] = str(exc)
        record["success"] = True
    except Exception as exc:
        record["disposition"] = "NO_LIVE_DNS_FAILURE_OBSERVATION"
        record["exception_type"] = type(exc).__name__
        record["strerror"] = str(exc)

    return record


def run_all_failure_observations():
    refusal = observe_loopback_refusal()
    timeout = observe_read_timeout()
    dns = observe_dns_failure()

    return {
        "refusal_observation": refusal,
        "read_timeout_observation": timeout,
        "dns_failure_observation": dns,
        "partial_failure_doctrine": {
            "ambiguity": "A client-visible timeout proves only that the client's local read timer expired before bytes were received. The remote server may have (1) never received the request, (2) received and crashed mid-execution, or (3) completed execution successfully while the response was lost.",
            "retry_judgment": "A timeout does not by itself authorize a retry. Retry safety requires an application-level contract appropriate to the operation, such as naturally idempotent semantics, a unique operation identifier with deduplication, or an explicit query/reconciliation step.",
        },
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="M10 Network Failure Fixture")
    parser.add_argument("--json", action="store_true", help="Output observation in JSON format")
    args = parser.parse_args()

    results = run_all_failure_observations()

    if args.json:
        print(json.dumps(results, indent=2))
        return 0 if (results["refusal_observation"]["success"] and results["read_timeout_observation"]["success"]) else 1

    print("=" * 60)
    print(" M10-03 Controlled Network Failure Fixture")
    print("=" * 60)
    print(" [Case 1: Controlled Loopback Refusal]")
    r = results["refusal_observation"]
    print(f"   Target:         {r['target']}")
    print(f"   Disposition:    {r['disposition']}")
    print(f"   Exception:      {r['exception_type']} (Errno: {r['errno']})")
    print(f"   Error Message:  {r['strerror']}")
    print(f"   Elapsed Sample: {r['elapsed_ms']} ms")
    print("-" * 60)
    print(" [Case 2: Accepted-but-Silent Read Timeout]")
    t = results["read_timeout_observation"]
    print(f"   Target:         {t['target']}")
    print(f"   Deadline:       {t['configured_read_deadline_s']} s (Watchdog: {t['harness_watchdog_s']} s)")
    print(f"   Disposition:    {t['disposition']}")
    print(f"   Exception:      {t['exception_type']}")
    print(f"   Elapsed Sample: {t['elapsed_ms']} ms")
    print("-" * 60)
    print(" [Case 3: Capability-Gated DNS Failure Observation]")
    d = results["dns_failure_observation"]
    print(f"   Hostname:       {d['query_hostname']}")
    print(f"   Disposition:    {d['disposition']}")
    print(f"   Exception:      {d['exception_type']} (Errno: {d['errno']})")
    print(f"   Details:        {d['strerror']}")
    print("-" * 60)
    print(" [Partial Failure & Retry Doctrine]")
    print("   Remote Ambiguity: Timeout leaves server outcome uncertain.")
    print("   Retry Judgment:   Retry only under an explicit application-level contract.")
    print("=" * 60)

    return 0 if (r["success"] and t["success"]) else 1


if __name__ == "__main__":
    sys.exit(main())
