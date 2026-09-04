#!/usr/bin/env python3
"""
M10 Lesson 1 Activity: Endpoint, Addressing, and Socket Observer.

Demonstrates:
1. Dynamic port allocation using port 0 on 127.0.0.1 (kernel ephemeral port selection).
2. Distinction between host IP, transport port, OS socket, and application process.
3. Bounded loopback data exchange (16-byte payload).
4. Optional system inspection (ss, ip route) with truthful fallback.
"""

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time


def inspect_host_tools():
    """
    Checks optional host routing and socket inspection tools (ss, ip route).
    Reports truthful TOOL UNAVAILABLE when missing.
    """
    results = {}

    ss_path = shutil.which("ss")
    if ss_path:
        try:
            res = subprocess.run([ss_path, "-tan"], capture_output=True, text=True, timeout=2)
            results["ss"] = {
                "available": True,
                "output_sample": res.stdout[:200].strip(),
            }
        except Exception as e:
            results["ss"] = {"available": False, "reason": str(e)}
    else:
        results["ss"] = {"available": False, "reason": "TOOL UNAVAILABLE (iproute2 ss not installed or non-Linux)"}

    ip_path = shutil.which("ip")
    if ip_path:
        try:
            res = subprocess.run([ip_path, "route"], capture_output=True, text=True, timeout=2)
            results["ip_route"] = {
                "available": True,
                "output_sample": res.stdout[:200].strip(),
            }
        except Exception as e:
            results["ip_route"] = {"available": False, "reason": str(e)}
    else:
        results["ip_route"] = {"available": False, "reason": "TOOL UNAVAILABLE (iproute2 ip not installed or non-Linux)"}

    return results


def run_endpoint_observation(payload_bytes=b"CS-ESSENTIAL-M10"):
    """
    Binds a listening socket on ('127.0.0.1', 0), extracts the assigned ephemeral port,
    and runs a bounded client-server echo exchange.
    """
    if len(payload_bytes) != 16:
        raise ValueError("Payload must be exactly 16 bytes for bounded M10 observation.")

    current_pid = os.getpid()

    # 1. Create server socket and bind to port 0
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set timeout to prevent hangs
    server_sock.settimeout(3.0)
    server_sock.bind(("127.0.0.1", 0))
    server_sock.listen(1)

    bound_host, bound_port = server_sock.getsockname()
    if bound_port == 0:
        server_sock.close()
        raise RuntimeError("Kernel failed to allocate a dynamic non-zero port for port 0.")

    exchange_record = {
        "process_id": current_pid,
        "bind_requested": ("127.0.0.1", 0),
        "assigned_endpoint": {
            "host": bound_host,
            "port": bound_port,
        },
        "payload_sent": payload_bytes.decode("ascii", errors="replace"),
        "payload_received": None,
        "exchange_success": False,
        "error": None,
    }

    server_error = []

    def server_worker():
        conn = None
        try:
            conn, client_addr = server_sock.accept()
            conn.settimeout(3.0)
            data = bytearray()
            while len(data) < len(payload_bytes):
                chunk = conn.recv(len(payload_bytes) - len(data))
                if not chunk:
                    break
                data.extend(chunk)
            exchange_record["payload_received"] = bytes(data).decode("ascii", errors="replace")
            # Echo back
            conn.sendall(data)
        except Exception as exc:
            server_error.append(exc)
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

    srv_thread = threading.Thread(target=server_worker, daemon=True)
    srv_thread.start()

    # 2. Client socket connects to server's dynamic port
    client_sock = None
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.settimeout(3.0)
        client_sock.connect(("127.0.0.1", bound_port))
        client_local_endpoint = client_sock.getsockname()
        exchange_record["client_local_endpoint"] = {
            "host": client_local_endpoint[0],
            "port": client_local_endpoint[1],
        }

        # Send 16 bytes
        client_sock.sendall(payload_bytes)

        # Receive echo
        echo_buf = bytearray()
        while len(echo_buf) < len(payload_bytes):
            chunk = client_sock.recv(len(payload_bytes) - len(echo_buf))
            if not chunk:
                break
            echo_buf.extend(chunk)

        srv_thread.join(timeout=2.0)

        if bytes(echo_buf) == payload_bytes:
            exchange_record["exchange_success"] = True
        else:
            exchange_record["error"] = f"Echo mismatch: expected {payload_bytes}, got {bytes(echo_buf)}"
    except Exception as exc:
        exchange_record["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if client_sock:
            try:
                client_sock.close()
            except Exception:
                pass
        try:
            server_sock.close()
        except Exception:
            pass

    if server_error and not exchange_record["error"]:
        exchange_record["error"] = f"Server error: {server_error[0]}"

    return exchange_record


def main():
    parser = argparse.ArgumentParser(description="M10 Endpoint and Socket Observer")
    parser.add_argument("--json", action="store_true", help="Output observation in JSON format")
    args = parser.parse_args()

    record = run_endpoint_observation()
    tools = inspect_host_tools()
    full_output = {
        "observation": record,
        "host_tools": tools,
    }

    if args.json:
        print(json.dumps(full_output, indent=2))
        return 0 if record["exchange_success"] else 1

    print("=" * 60)
    print(" M10-01 Local Endpoint & Socket Observer")
    print("=" * 60)
    print(f" Current Process PID:        {record['process_id']}")
    print(f" Bind Requested:             {record['bind_requested']}")
    print(f" OS Assigned Endpoint:       {record['assigned_endpoint']['host']}:{record['assigned_endpoint']['port']}")
    if "client_local_endpoint" in record:
        print(f" Client Local Endpoint:      {record['client_local_endpoint']['host']}:{record['client_local_endpoint']['port']}")
    print(f" 16-Byte Payload Sent:       {record['payload_sent']}")
    print(f" 16-Byte Payload Received:   {record['payload_received']}")
    print(f" Loopback Exchange Status:   {'SUCCESS' if record['exchange_success'] else 'FAILED'}")
    if record["error"]:
        print(f" Error:                      {record['error']}")
    print("-" * 60)
    print(" [Optional Host Tools Disposition]")
    for tool_name, t_info in tools.items():
        if t_info["available"]:
            print(f"   {tool_name:10}: AVAILABLE")
        else:
            print(f"   {tool_name:10}: {t_info['reason']}")
    print("=" * 60)

    return 0 if record["exchange_success"] else 1


if __name__ == "__main__":
    sys.exit(main())
