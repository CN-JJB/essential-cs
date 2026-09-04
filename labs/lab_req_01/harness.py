#!/usr/bin/env python3
"""LAB-REQ-01 bounded automation harness.

Runs the accepted four-step localhost trace with the host's real curl:
1. direct origin;
2. forwarded intermediary;
3. conditional 304;
4. course-owned upstream failure -> 502.

The harness records verbose curl evidence, owns/reaps child processes, and
checks that old course endpoints no longer accept connections after cleanup.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import queue
import re
import shlex
import shutil
import socket
import subprocess
import sys
import threading
import time
from typing import Any


LAB_BLOCKED_STATUS = "ENVIRONMENT_BLOCKED_NOT_RUN"


def probe_curl() -> dict[str, Any]:
    path = shutil.which("curl")
    if not path and sys.platform == "win32":
        candidate = os.path.join(
            os.environ.get("SystemRoot", r"C:\Windows"), "System32", "curl.exe"
        )
        if os.path.exists(candidate):
            path = candidate

    if not path:
        return {
            "available": False,
            "path": None,
            "version_output": [],
            "reason": "TOOL MISSING: curl is required for LAB-REQ-01",
        }

    try:
        proc = subprocess.run(
            [path, "--version"],
            capture_output=True,
            text=True,
            timeout=3.0,
        )
    except Exception as exc:
        return {
            "available": False,
            "path": path,
            "version_output": [],
            "reason": f"curl --version could not execute: {type(exc).__name__}: {exc}",
        }

    output = (proc.stdout or proc.stderr).splitlines()
    if proc.returncode != 0 or not output:
        return {
            "available": False,
            "path": path,
            "version_output": output[:8],
            "reason": f"curl --version failed with exit code {proc.returncode}",
        }

    return {
        "available": True,
        "path": path,
        "version_output": output[:8],
        "reason": None,
    }


def parse_http_raw_response(raw_output: str) -> tuple[int, dict[str, str], str]:
    """Parse one final HTTP/1.x response emitted by this localhost fixture."""
    normalized = raw_output.replace("\r\n", "\n")
    parts = normalized.split("\n\n", 1)
    header_block = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    lines = header_block.split("\n")
    if not lines or not lines[0].startswith("HTTP/"):
        raise ValueError(f"Invalid HTTP response status line: {lines[:1]}")

    status_tokens = lines[0].split()
    if len(status_tokens) < 2:
        raise ValueError(f"Malformed status line: {lines[0]}")
    status_code = int(status_tokens[1])

    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

    return status_code, headers, body


def header_value(headers: dict[str, str], name: str) -> str | None:
    target = name.lower()
    for key, value in headers.items():
        if key.lower() == target:
            return value
    return None


def probe_endpoint_not_accepting(host: str, port: int, timeout_s: float = 0.5) -> dict[str, Any]:
    """Record whether a new TCP connection can be established to an old course endpoint."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_s)
    try:
        result = sock.connect_ex((host, port))
        return {
            "host": host,
            "port": port,
            "connection_established": result == 0,
            "connect_ex_result": result,
            "disposition": (
                "UNEXPECTED_CONNECTION_ESTABLISHED"
                if result == 0
                else "OLD_COURSE_ENDPOINT_NOT_ACCEPTING"
            ),
        }
    except Exception as exc:
        return {
            "host": host,
            "port": port,
            "connection_established": False,
            "connect_ex_result": None,
            "disposition": "PROBE_EXCEPTION_NO_CONNECTION_ESTABLISHED",
            "exception_type": type(exc).__name__,
            "details": str(exc),
        }
    finally:
        sock.close()


def health_check(port: int, timeout_s: float = 1.0) -> dict[str, Any]:
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=timeout_s)
    try:
        conn.request("GET", "/health")
        resp = conn.getresponse()
        body = resp.read()
        return {
            "status": resp.status,
            "body": body.decode("utf-8", errors="replace"),
            "ready": resp.status == 200,
        }
    finally:
        conn.close()


class ProcessManager:
    def __init__(self) -> None:
        self.procs: list[subprocess.Popen[str]] = []

    def spawn(self, args: list[str], cwd: str | None = None) -> subprocess.Popen[str]:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            text=True,
            bufsize=1,
        )
        self.procs.append(proc)
        return proc

    def stop(self, proc: subprocess.Popen[str], timeout_s: float = 3.0) -> dict[str, Any]:
        record: dict[str, Any] = {
            "pid": proc.pid,
            "already_exited": proc.poll() is not None,
            "terminate_requested": False,
            "kill_escalation": False,
            "reaped": False,
            "returncode": proc.poll(),
        }

        if proc.poll() is None:
            record["terminate_requested"] = True
            proc.terminate()
            try:
                proc.wait(timeout=timeout_s)
            except subprocess.TimeoutExpired:
                record["kill_escalation"] = True
                proc.kill()
                proc.wait(timeout=timeout_s)

        record["reaped"] = proc.poll() is not None
        record["returncode"] = proc.poll()
        return record

    def cleanup_all(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for proc in self.procs:
            try:
                records.append(self.stop(proc))
            except Exception as exc:
                records.append(
                    {
                        "pid": proc.pid,
                        "reaped": proc.poll() is not None,
                        "cleanup_error": f"{type(exc).__name__}: {exc}",
                    }
                )
            finally:
                if proc.stdout:
                    proc.stdout.close()
                if proc.stderr:
                    proc.stderr.close()
        self.procs.clear()
        return records


def wait_for_port_pattern(
    proc: subprocess.Popen[str], pattern: str, timeout_s: float = 5.0
) -> int:
    """Wait under a real watchdog without blocking the deadline on readline()."""
    if proc.stdout is None:
        raise RuntimeError("child stdout pipe unavailable")

    line_queue: queue.Queue[str | None] = queue.Queue()

    def reader() -> None:
        try:
            for line in proc.stdout:
                line_queue.put(line)
        finally:
            line_queue.put(None)

    threading.Thread(target=reader, daemon=True).start()

    compiled = re.compile(pattern)
    deadline = time.monotonic() + timeout_s
    while True:
        if proc.poll() is not None:
            stderr_out = proc.stderr.read() if proc.stderr else ""
            raise RuntimeError(
                f"Process exited before readiness with code {proc.returncode}: {stderr_out}"
            )

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"Timed out waiting for readiness pattern {pattern!r}")

        try:
            line = line_queue.get(timeout=min(remaining, 0.1))
        except queue.Empty:
            continue

        if line is None:
            continue
        match = compiled.search(line)
        if match:
            return int(match.group(1))


def run_curl(
    curl_path: str, url: str, extra_headers: list[str] | None = None
) -> dict[str, Any]:
    cmd = [curl_path, "-sS", "-v", "-i", "--http1.1", "--max-time", "5"]
    for header in extra_headers or []:
        cmd.extend(["-H", header])
    cmd.append(url)

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=8.0)
    if proc.returncode != 0:
        raise RuntimeError(
            f"curl failed with exit code {proc.returncode}: {proc.stderr.strip()}"
        )

    status, headers, body = parse_http_raw_response(proc.stdout)
    return {
        "cmd_argv": cmd,
        "cmd_display": shlex.join(cmd),
        "returncode": proc.returncode,
        "status_code": status,
        "headers": headers,
        "body": body,
        "body_bytes_len": len(body.encode("utf-8")),
        "verbose_trace": proc.stderr,
    }


def run_lab_req_01_trace() -> dict[str, Any]:
    curl = probe_curl()
    if not curl["available"]:
        return {
            "status": LAB_BLOCKED_STATUS,
            "lab_req_01_status": "TOOL_MISSING_CURL",
            "curl": curl,
            "steps": {},
            "cleanup": {"not_started": True},
        }

    curl_path = str(curl["path"])
    current_dir = os.path.dirname(os.path.abspath(__file__))
    origin_script = os.path.join(current_dir, "origin_server.py")
    proxy_script = os.path.join(current_dir, "intermediary_adapter.py")

    pm = ProcessManager()
    origin_port: int | None = None
    proxy_port: int | None = None
    origin_stop_record: dict[str, Any] | None = None

    trace: dict[str, Any] = {
        "status": "INCOMPLETE",
        "curl": curl,
        "steps": {},
        "readiness": {},
    }

    try:
        origin_proc = pm.spawn([sys.executable, origin_script], cwd=current_dir)
        origin_port = wait_for_port_pattern(origin_proc, r"ORIGIN_READY_PORT=(\d+)")
        trace["origin_port"] = origin_port
        trace["readiness"]["origin"] = health_check(origin_port)
        if not trace["readiness"]["origin"]["ready"]:
            raise RuntimeError("origin health check did not reach READY")

        proxy_proc = pm.spawn(
            [sys.executable, proxy_script, "--origin-port", str(origin_port)],
            cwd=current_dir,
        )
        proxy_port = wait_for_port_pattern(proxy_proc, r"PROXY_READY_PORT=(\d+)")
        trace["proxy_port"] = proxy_port
        trace["readiness"]["proxy"] = health_check(proxy_port)
        if not trace["readiness"]["proxy"]["ready"]:
            raise RuntimeError("intermediary health check did not reach READY")

        # Step 1: direct origin.
        s1 = run_curl(curl_path, f"http://127.0.0.1:{origin_port}/resource")
        etag = header_value(s1["headers"], "ETag")
        assert s1["status_code"] == 200
        assert etag
        assert s1["body_bytes_len"] > 0
        assert header_value(s1["headers"], "Via") is None
        s1["etag"] = etag
        s1["pass"] = True
        trace["steps"]["step_1_direct_origin"] = s1

        # Step 2: forwarded.
        s2 = run_curl(curl_path, f"http://127.0.0.1:{proxy_port}/resource")
        via2 = header_value(s2["headers"], "Via")
        assert s2["status_code"] == 200
        assert via2 and "1.1 essential-cs-intermediary" in via2
        assert s2["body"] == s1["body"]
        s2["via"] = via2
        s2["pass"] = True
        trace["steps"]["step_2_proxy_forward"] = s2

        # Step 3: conditional validation.
        s3 = run_curl(
            curl_path,
            f"http://127.0.0.1:{proxy_port}/resource",
            [f"If-None-Match: {etag}"],
        )
        via3 = header_value(s3["headers"], "Via")
        assert s3["status_code"] == 304
        assert via3 and "1.1 essential-cs-intermediary" in via3
        assert s3["body_bytes_len"] == 0
        s3["via"] = via3
        s3["pass"] = True
        trace["steps"]["step_3_conditional_304"] = s3

        # Step 4: stop the course origin and verify that old endpoint no longer accepts.
        origin_stop_record = pm.stop(origin_proc)
        origin_closed_probe = probe_endpoint_not_accepting("127.0.0.1", origin_port)
        if not origin_stop_record["reaped"] or origin_closed_probe["connection_established"]:
            raise RuntimeError(
                f"origin teardown failed: stop={origin_stop_record}, probe={origin_closed_probe}"
            )
        trace["origin_stop"] = origin_stop_record
        trace["origin_closed_probe"] = origin_closed_probe

        s4 = run_curl(curl_path, f"http://127.0.0.1:{proxy_port}/resource")
        via4 = header_value(s4["headers"], "Via")
        assert s4["status_code"] == 502
        assert via4 and "1.1 essential-cs-intermediary" in via4
        assert "Bad Gateway" in s4["body"]
        s4["via"] = via4
        s4["pass"] = True
        trace["steps"]["step_4_upstream_failure_502"] = s4

        trace["status"] = "ALL_STEPS_PASSED"

    finally:
        trace["cleanup"] = {
            "processes": pm.cleanup_all(),
        }
        if origin_port is not None:
            trace["cleanup"]["origin_endpoint"] = probe_endpoint_not_accepting(
                "127.0.0.1", origin_port
            )
        if proxy_port is not None:
            trace["cleanup"]["proxy_endpoint"] = probe_endpoint_not_accepting(
                "127.0.0.1", proxy_port
            )

        process_records = trace["cleanup"].get("processes", [])
        trace["cleanup"]["all_owned_processes_reaped"] = all(
            record.get("reaped", False) for record in process_records
        )
        endpoint_records = [
            value
            for key, value in trace["cleanup"].items()
            if key.endswith("_endpoint") and isinstance(value, dict)
        ]
        trace["cleanup"]["old_endpoints_not_accepting"] = all(
            not record.get("connection_established", True)
            for record in endpoint_records
        )

    return trace


def print_human_report(trace: dict[str, Any]) -> None:
    print("=" * 72)
    print(" LAB-REQ-01 HTTP ORIGIN / INTERMEDIARY TRACE")
    print("=" * 72)
    print(f"Overall Status : {trace['status']}")

    curl = trace.get("curl", {})
    print(f"curl binary    : {curl.get('path')}")
    if curl.get("version_output"):
        print(f"curl version   : {curl['version_output'][0]}")

    if trace["status"] == LAB_BLOCKED_STATUS:
        print(f"Disposition    : {curl.get('reason')}")
        print("=" * 72)
        return

    print(f"Origin Port    : {trace.get('origin_port')}")
    print(f"Proxy Port     : {trace.get('proxy_port')}")

    for step_id, step in trace.get("steps", {}).items():
        print("-" * 72)
        print(f"{step_id}")
        print(f"  Command      : {step['cmd_display']}")
        print(f"  Status Code  : {step['status_code']}")
        print(f"  Via          : {step.get('via')}")
        print(f"  Body Bytes   : {step['body_bytes_len']}")
        print("  curl -v trace:")
        for line in step.get("verbose_trace", "").splitlines():
            print(f"    {line}")

    print("-" * 72)
    print(
        "Cleanup       : "
        f"reaped={trace.get('cleanup', {}).get('all_owned_processes_reaped')} "
        f"old_endpoints_closed={trace.get('cleanup', {}).get('old_endpoints_not_accepting')}"
    )
    print("=" * 72)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LAB-REQ-01 harness")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = run_lab_req_01_trace()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_human_report(result)

    if result["status"] == LAB_BLOCKED_STATUS:
        sys.exit(2)
    sys.exit(0 if result["status"] == "ALL_STEPS_PASSED" else 1)
