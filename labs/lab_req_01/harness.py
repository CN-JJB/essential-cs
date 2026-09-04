#!/usr/bin/env python3
"""LAB-REQ-01 Automation Harness.

Orchestrates Origin Server and Intermediary Adapter, then drives the 4-step curl trace:
  Step 1: Direct request to Origin (200 OK + ETag + payload)
  Step 2: Forwarded request via Proxy (200 OK + Via header injection + payload match)
  Step 3: Conditional request via Proxy (304 Not Modified + Via header + 0 body bytes)
  Step 4: Upstream failure via Proxy after Origin termination (502 Bad Gateway)

Guarantees clean process termination and zero orphans.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Tuple


def find_curl_bin() -> str:
    """Locate curl executable or raise RuntimeError."""
    curl_path = shutil.which("curl")
    if not curl_path and sys.platform == "win32":
        # Check standard Windows location
        candidate = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "curl.exe")
        if os.path.exists(candidate):
            curl_path = candidate
    if not curl_path:
        raise RuntimeError("curl executable not found in PATH or System32.")
    return curl_path


def parse_http_raw_response(raw_output: str) -> Tuple[int, Dict[str, str], str]:
    """Parse raw HTTP response from curl -i output into (status_code, headers, body)."""
    # Normalize CRLF to LF
    normalized = raw_output.replace("\r\n", "\n")
    # Split headers from body on double newline
    parts = normalized.split("\n\n", 1)
    header_block = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    lines = header_block.split("\n")
    if not lines or not lines[0].startswith("HTTP/"):
        raise ValueError(f"Invalid HTTP response status line: {lines[:1]}")

    status_line = lines[0]
    # e.g., HTTP/1.1 200 OK
    status_tokens = status_line.split()
    if len(status_tokens) < 2:
        raise ValueError(f"Malformed status line: {status_line}")
    status_code = int(status_tokens[1])

    headers: Dict[str, str] = {}
    for line in lines[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k.strip()] = v.strip()

    return status_code, headers, body


class ProcessManager:
    """Manages subprocess lifecycles with guaranteed cleanup."""

    def __init__(self) -> None:
        self.procs: List[subprocess.Popen] = []

    def spawn(self, args: List[str], cwd: Optional[str] = None) -> subprocess.Popen:
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

    def stop(self, proc: subprocess.Popen, timeout: float = 3.0) -> None:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=timeout)
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

    def cleanup_all(self) -> None:
        for proc in self.procs:
            if proc.poll() is None:
                try:
                    proc.terminate()
                    proc.wait(timeout=1.0)
                except Exception:
                    try:
                        proc.kill()
                        proc.wait(timeout=1.0)
                    except Exception:
                        pass
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
        self.procs.clear()


def wait_for_port_pattern(proc: subprocess.Popen, pattern: str, timeout: float = 5.0) -> int:
    """Read proc.stdout until regex pattern matches, returning the captured integer port."""
    start_time = time.time()
    compiled = re.compile(pattern)
    while time.time() - start_time < timeout:
        if proc.poll() is not None:
            stderr_out = proc.stderr.read() if proc.stderr else ""
            raise RuntimeError(f"Process exited prematurely with code {proc.returncode}: {stderr_out}")
        line = proc.stdout.readline() if proc.stdout else ""
        if line:
            match = compiled.search(line)
            if match:
                return int(match.group(1))
        time.sleep(0.05)
    raise TimeoutError(f"Timed out waiting for pattern '{pattern}' from process.")


def run_lab_req_01_trace() -> Dict[str, Any]:
    """Execute the full 4-step LAB-REQ-01 trace."""
    curl_bin = find_curl_bin()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    origin_script = os.path.join(current_dir, "origin_server.py")
    proxy_script = os.path.join(current_dir, "intermediary_adapter.py")

    pm = ProcessManager()
    trace_results: Dict[str, Any] = {
        "status": "INCOMPLETE",
        "curl_bin": curl_bin,
        "steps": {},
    }

    try:
        # 1. Start Origin Server
        origin_proc = pm.spawn([sys.executable, origin_script], cwd=current_dir)
        origin_port = wait_for_port_pattern(origin_proc, r"ORIGIN_READY_PORT=(\d+)")
        trace_results["origin_port"] = origin_port

        # 2. Start Intermediary Proxy
        proxy_proc = pm.spawn(
            [sys.executable, proxy_script, "--origin-port", str(origin_port)],
            cwd=current_dir,
        )
        proxy_port = wait_for_port_pattern(proxy_proc, r"PROXY_READY_PORT=(\d+)")
        trace_results["proxy_port"] = proxy_port

        # Small delay for listener readiness
        time.sleep(0.2)

        # STEP 1: Direct Request to Origin (No cache)
        # curl -s -i http://127.0.0.1:<origin_port>/resource
        cmd_s1 = [curl_bin, "-s", "-i", f"http://127.0.0.1:{origin_port}/resource"]
        res_s1 = subprocess.run(cmd_s1, capture_output=True, text=True, timeout=5.0)
        status_s1, headers_s1, body_s1 = parse_http_raw_response(res_s1.stdout)

        etag_val = headers_s1.get("ETag")
        assert status_s1 == 200, f"Step 1 expected 200, got {status_s1}"
        assert etag_val, "Step 1 expected ETag header in response"
        assert len(body_s1) > 0, "Step 1 expected non-empty body"

        trace_results["steps"]["step_1_direct_origin"] = {
            "cmd": " ".join(cmd_s1),
            "status_code": status_s1,
            "headers": headers_s1,
            "etag": etag_val,
            "body_bytes_len": len(body_s1),
            "body": body_s1,
            "pass": True,
        }

        # STEP 2: Request via Proxy (Proxy forward & Via injection)
        # curl -s -i http://127.0.0.1:<proxy_port>/resource
        cmd_s2 = [curl_bin, "-s", "-i", f"http://127.0.0.1:{proxy_port}/resource"]
        res_s2 = subprocess.run(cmd_s2, capture_output=True, text=True, timeout=5.0)
        status_s2, headers_s2, body_s2 = parse_http_raw_response(res_s2.stdout)

        via_val = headers_s2.get("Via")
        assert status_s2 == 200, f"Step 2 expected 200, got {status_s2}"
        assert via_val and "essential-cs-intermediary" in via_val, f"Step 2 Via header missing or invalid: {via_val}"
        assert body_s2 == body_s1, "Step 2 body does not match Step 1 body"

        trace_results["steps"]["step_2_proxy_forward"] = {
            "cmd": " ".join(cmd_s2),
            "status_code": status_s2,
            "headers": headers_s2,
            "via": via_val,
            "body_bytes_len": len(body_s2),
            "body": body_s2,
            "pass": True,
        }

        # STEP 3: Conditional Request via Proxy (If-None-Match -> 304 with 0 body)
        # curl -s -i -H 'If-None-Match: "strong-v1"' http://127.0.0.1:<proxy_port>/resource
        cmd_s3 = [
            curl_bin,
            "-s",
            "-i",
            "-H",
            f"If-None-Match: {etag_val}",
            f"http://127.0.0.1:{proxy_port}/resource",
        ]
        res_s3 = subprocess.run(cmd_s3, capture_output=True, text=True, timeout=5.0)
        status_s3, headers_s3, body_s3 = parse_http_raw_response(res_s3.stdout)

        assert status_s3 == 304, f"Step 3 expected 304 Not Modified, got {status_s3}"
        assert headers_s3.get("Via") and "essential-cs-intermediary" in headers_s3.get("Via", ""), "Step 3 Via header missing"
        assert len(body_s3) == 0, f"Step 3 expected 0 body bytes in 304 response, got {len(body_s3)}: {body_s3!r}"

        trace_results["steps"]["step_3_conditional_304"] = {
            "cmd": " ".join(cmd_s3),
            "status_code": status_s3,
            "headers": headers_s3,
            "via": headers_s3.get("Via"),
            "body_bytes_len": len(body_s3),
            "pass": True,
        }

        # STEP 4: Upstream Failure Mapping (Origin Terminated -> 502 Bad Gateway)
        pm.stop(origin_proc)
        time.sleep(0.3)

        cmd_s4 = [curl_bin, "-s", "-i", f"http://127.0.0.1:{proxy_port}/resource"]
        res_s4 = subprocess.run(cmd_s4, capture_output=True, text=True, timeout=5.0)
        status_s4, headers_s4, body_s4 = parse_http_raw_response(res_s4.stdout)

        assert status_s4 == 502, f"Step 4 expected 502 Bad Gateway, got {status_s4}"
        assert headers_s4.get("Via") and "essential-cs-intermediary" in headers_s4.get("Via", ""), "Step 4 Via header missing"
        assert "Bad Gateway" in body_s4, f"Step 4 expected Bad Gateway error body, got: {body_s4}"

        trace_results["steps"]["step_4_upstream_failure_502"] = {
            "cmd": " ".join(cmd_s4),
            "status_code": status_s4,
            "headers": headers_s4,
            "via": headers_s4.get("Via"),
            "body": body_s4,
            "pass": True,
        }

        trace_results["status"] = "ALL_STEPS_PASSED"
        return trace_results

    finally:
        pm.cleanup_all()


def print_human_report(trace: Dict[str, Any]) -> None:
    print("=" * 70)
    print(" LAB-REQ-01 END-TO-END HTTP INTERMEDIARY & CACHING TRACE REPORT")
    print("=" * 70)
    print(f"Overall Status : {trace['status']}")
    print(f"curl binary    : {trace['curl_bin']}")
    print(f"Origin Port    : {trace.get('origin_port')}")
    print(f"Proxy Port     : {trace.get('proxy_port')}")
    print("-" * 70)

    for step_id, step in trace.get("steps", {}).items():
        print(f"\n[STEP] {step_id}:")
        print(f"  Command     : {step['cmd']}")
        print(f"  Status Code : {step['status_code']}")
        if "etag" in step:
            print(f"  ETag        : {step['etag']}")
        if "via" in step:
            print(f"  Via         : {step['via']}")
        print(f"  Body Bytes  : {step.get('body_bytes_len', len(step.get('body', '')))}")
        if step.get("body"):
            preview = step["body"].strip()
            if len(preview) > 120:
                preview = preview[:117] + "..."
            print(f"  Body Preview: {preview}")
        print(f"  Step Pass   : {step['pass']}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LAB-REQ-01 Harness")
    parser.add_argument("--json", action="store_true", help="Output JSON result")
    args = parser.parse_args()

    results = run_lab_req_01_trace()
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_human_report(results)

    if results["status"] != "ALL_STEPS_PASSED":
        sys.exit(1)
