#!/usr/bin/env python3
"""
Preflight verification script for Stage 6 Distributed Systems & Modern Infrastructure (M16-M20).
Evaluates and records host capabilities empirically without permanently pinning OQ-BP-006.

Probes the required Stage 6 dimensions:
1. OS / kernel / architecture
2. Python implementation / version
3. stdlib socket capability
4. Localhost bind to ephemeral port (127.0.0.1:0)
5. Embedded SQLite version and transactional capabilities
6. Writable temporary directory
7. Subprocess watchdog / termination / reaping capability
8. Optional external source reachability (Stanford CS144 LAB-OPT-02)

OQ-BP-006 remains OPEN.
Readiness is not lesson/lab PASS.
"""

import argparse
import datetime
import json
import os
import platform
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
from typing import Any, Dict

CS144_BENCHMARK = {
    "course": "Stanford CS144 (Introduction to Computer Networking)",
    "term": "Fall 2025",
    "assignment": "Checkpoint 2 (TCP Receiver)",
    "course_url": "https://cs144.github.io/",
    "official_url": "https://cs144.github.io/assignments/check2.pdf",
    "course_inspection_date": "2026-09-05",
    "rights_status": "UNESTABLISHED (zero vendored code, link-only)",
}

MIT_6033_BENCHMARK = {
    "course": "MIT OpenCourseWare 6.033 (Computer System Engineering)",
    "term": "Spring 2018",
    "expedition": "EXP-05 (Replication, Transactions, Logging)",
    "course_index_url": "https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/lecture-notes/",
    "lecture_14_url": "https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/8eb16d3628bbd77ee7e8471b9871ec09_MIT6_033S18lec14.pdf",
    "lecture_15_url": "https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/df1526408e3ec6f7e43aadfa1ce5f944_MIT6_033S18lec15.pdf",
    "lecture_16_url": "https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/76fa216e8e5a4c4722c315a84b8e09a8c_MIT6_033S18lec16.pdf",
    "course_inspection_date": "2026-09-05",
    "rights_status": "CC BY-NC-SA 4.0 (link-and-paraphrase only, zero vendored slides/code)",
}


def probe_os() -> Dict[str, Any]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.machine(),
    }


def probe_python() -> Dict[str, Any]:
    return {
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
        "sys_version": sys.version,
    }


def probe_stdlib_socket() -> Dict[str, Any]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.close()
        return {
            "available": True,
            "disposition": "REQUIRED CAPABILITY PASS",
        }
    except Exception as e:
        return {
            "available": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": str(e),
        }


def probe_localhost_ephemeral_bind() -> Dict[str, Any]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.listen(1)
        s.close()
        return {
            "bound": True,
            "sample_ephemeral_port": port,
            "disposition": "REQUIRED CAPABILITY PASS",
        }
    except Exception as e:
        return {
            "bound": False,
            "sample_ephemeral_port": None,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": str(e),
        }


def probe_embedded_sqlite() -> Dict[str, Any]:
    try:
        ver = sqlite3.sqlite_version
        with tempfile.TemporaryDirectory(prefix="essential_cs_s6_sqlite_") as tmpdir:
            db_path = os.path.join(tmpdir, "preflight.db")
            conn = sqlite3.connect(db_path, timeout=1.0, isolation_level=None)
            try:
                conn.execute("BEGIN IMMEDIATE")
                conn.execute("CREATE TABLE test (id INT PRIMARY KEY, val TEXT)")
                conn.execute("INSERT INTO test VALUES (1, 'ok')")
                conn.execute("COMMIT")
                row = conn.execute("SELECT val FROM test WHERE id = 1").fetchone()
            finally:
                conn.close()
        functional = row == ("ok",)
        return {
            "available": functional,
            "sqlite_version": ver,
            "file_backed_transaction_functional": functional,
            "disposition": (
                "REQUIRED CAPABILITY PASS"
                if functional
                else "ENVIRONMENT-BLOCKED / NOT RUN"
            ),
        }
    except Exception as e:
        return {
            "available": False,
            "sqlite_version": None,
            "file_backed_transaction_functional": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": str(e),
        }


def probe_writable_temp() -> Dict[str, Any]:
    try:
        with tempfile.TemporaryDirectory(prefix="essential_cs_s6_") as tmpdir:
            test_file = os.path.join(tmpdir, "probe.tmp")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("probe")
            with open(test_file, "r", encoding="utf-8") as f:
                content = f.read()
            writable = (content == "probe")
        return {
            "writable": writable,
            "disposition": "REQUIRED CAPABILITY PASS" if writable else "FAIL",
        }
    except Exception as e:
        return {
            "writable": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": str(e),
        }


def probe_subprocess_watchdog() -> Dict[str, Any]:
    try:
        # Spawn a python process that would sleep 10s, then terminate and reap it
        proc = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(10)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(0.1)
        proc.terminate()
        try:
            proc.wait(timeout=2.0)
            reaped = True
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=2.0)
            reaped = True

        if proc.stdout:
            proc.stdout.close()
        if proc.stderr:
            proc.stderr.close()

        return {
            "watchdog_usable": True,
            "reaped": reaped,
            "exit_code": proc.returncode,
            "disposition": "REQUIRED CAPABILITY PASS",
        }
    except Exception as e:
        return {
            "watchdog_usable": False,
            "reaped": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": str(e),
        }


def probe_optional_cs144_source(live_probe: bool = False) -> Dict[str, Any]:
    record: Dict[str, Any] = {
        "course_benchmark": CS144_BENCHMARK,
        "disposition": "OPTIONAL / RIGHTS-GATED / LINK-ONLY",
        "vendoring": "ZERO VENDORED SOURCE",
    }
    if not live_probe:
        record["reachability"] = "SKIPPED (use --check-cs144-source to probe live)"
        return record

    try:
        req = urllib.request.Request(
            CS144_BENCHMARK["official_url"],
            headers={"User-Agent": "Essential-CS-Preflight-Probe/1.0"},
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            record["reachability"] = f"REACHABLE (HTTP {resp.status})"
    except Exception as e:
        record["reachability"] = f"OPTIONAL SOURCE UNAVAILABLE / SKIP ({e})"

    return record


def probe_m17_trace_capabilities() -> Dict[str, Any]:
    try:
        # Verify that json, dataclasses, typing, and local trace evaluation are functional
        import dataclasses
        import json

        test_data = {"N": 3, "W": 2, "R": 2}
        encoded = json.dumps(test_data)
        decoded = json.loads(encoded)
        functional = (decoded["W"] + decoded["R"] > decoded["N"])

        return {
            "available": functional,
            "json_and_dataclass_functional": functional,
            "disposition": (
                "REQUIRED CAPABILITY PASS"
                if functional
                else "ENVIRONMENT-BLOCKED / NOT RUN"
            ),
        }
    except Exception as e:
        return {
            "available": False,
            "json_and_dataclass_functional": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": str(e),
        }


def probe_optional_mit_6033_source(live_probe: bool = False) -> Dict[str, Any]:
    record: Dict[str, Any] = {
        "course_benchmark": MIT_6033_BENCHMARK,
        "disposition": "OPTIONAL / RIGHTS-GATED / LINK-ONLY",
        "vendoring": "ZERO VENDORED SOURCE",
    }
    if not live_probe:
        record["reachability"] = "SKIPPED (use --check-mit-source to probe live)"
        return record

    try:
        req = urllib.request.Request(
            MIT_6033_BENCHMARK["course_index_url"],
            headers={"User-Agent": "Essential-CS-Preflight-Probe/1.0"},
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            record["reachability"] = f"REACHABLE (HTTP {resp.status})"
    except Exception as e:
        record["reachability"] = f"OPTIONAL SOURCE UNAVAILABLE / SKIP ({e})"

    return record


def run_preflight(check_cs144: bool = False, check_mit: bool = False) -> Dict[str, Any]:
    os_info = probe_os()
    py_info = probe_python()
    sock_info = probe_stdlib_socket()
    bind_info = probe_localhost_ephemeral_bind()
    sqlite_info = probe_embedded_sqlite()
    temp_info = probe_writable_temp()
    watchdog_info = probe_subprocess_watchdog()
    cs144_info = probe_optional_cs144_source(live_probe=check_cs144)
    m17_trace_info = probe_m17_trace_capabilities()
    mit_info = probe_optional_mit_6033_source(live_probe=check_mit)

    m16_core_ready = (
        sock_info["available"]
        and bind_info["bound"]
        and sqlite_info["available"]
        and temp_info["writable"]
        and watchdog_info["watchdog_usable"]
    )

    m17_core_ready = m17_trace_info["available"] and temp_info["writable"]

    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "oq_bp_006_status": "OPEN / UNRESOLVED",
        "m16_core_status": "READY" if m16_core_ready else "BLOCKED",
        "m17_core_status": "READY" if m17_core_ready else "BLOCKED",
        "dimensions": {
            "1_os": os_info,
            "2_python": py_info,
            "3_stdlib_socket": sock_info,
            "4_localhost_ephemeral_bind": bind_info,
            "5_embedded_sqlite": sqlite_info,
            "6_writable_temp": temp_info,
            "7_subprocess_watchdog": watchdog_info,
            "8_optional_cs144_source": cs144_info,
            "9_m17_trace_capabilities": m17_trace_info,
            "10_optional_mit_6033_source": mit_info,
        },
        "notes": (
            "Readiness is not lesson/lab PASS. "
            "M16 and M17 use standard Python stdlib capabilities which are cross-platform, "
            "but OQ-BP-006 remains open for the wider course curriculum."
        ),
    }


class TestPreflightDistributedInfra(unittest.TestCase):
    def test_m16_core_capabilities_report_truthfully(self):
        report = run_preflight(check_cs144=False)
        self.assertEqual(report["oq_bp_006_status"], "OPEN / UNRESOLVED")

        dims = report["dimensions"]
        required_facts = [
            dims["3_stdlib_socket"]["available"],
            dims["4_localhost_ephemeral_bind"]["bound"],
            dims["5_embedded_sqlite"]["available"],
            dims["6_writable_temp"]["writable"],
            dims["7_subprocess_watchdog"]["watchdog_usable"],
        ]
        expected_status = "READY" if all(required_facts) else "BLOCKED"
        self.assertEqual(report["m16_core_status"], expected_status)

        allowed = {
            "REQUIRED CAPABILITY PASS",
            "ENVIRONMENT-BLOCKED / NOT RUN",
        }
        for key in (
            "3_stdlib_socket",
            "4_localhost_ephemeral_bind",
            "5_embedded_sqlite",
            "6_writable_temp",
            "7_subprocess_watchdog",
        ):
            self.assertIn(dims[key]["disposition"], allowed)

        self.assertEqual(
            dims["8_optional_cs144_source"]["disposition"],
            "OPTIONAL / RIGHTS-GATED / LINK-ONLY",
        )

    def test_m17_core_capabilities_report_truthfully(self):
        report = run_preflight(check_mit=False)
        self.assertEqual(report["m17_core_status"], "READY")

        dims = report["dimensions"]
        self.assertEqual(
            dims["9_m17_trace_capabilities"]["disposition"],
            "REQUIRED CAPABILITY PASS",
        )
        self.assertEqual(
            dims["10_optional_mit_6033_source"]["disposition"],
            "OPTIONAL / RIGHTS-GATED / LINK-ONLY",
        )
        self.assertEqual(
            dims["10_optional_mit_6033_source"]["vendoring"],
            "ZERO VENDORED SOURCE",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight verification for Stage 6 Distributed Infra")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--check-cs144-source", action="store_true", help="Probe Stanford CS144 reachability")
    parser.add_argument("--check-mit-source", action="store_true", help="Probe MIT 6.033 reachability")
    args = parser.parse_args()

    report = run_preflight(check_cs144=args.check_cs144_source, check_mit=args.check_mit_source)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if (report["m16_core_status"] == "READY" and report["m17_core_status"] == "READY") else 1

    print("=" * 70)
    print(" Essential CS: Distributed Infrastructure Preflight Capability Report")
    print("=" * 70)
    print(f" Timestamp:                 {report['timestamp']}")
    print(f" OQ-BP-006 Status:          {report['oq_bp_006_status']}")
    print(f" M16 Core Status:           {report['m16_core_status']}")
    print(f" M17 Core Status:           {report['m17_core_status']}")
    print("-" * 70)
    print(f" [Host OS]:                 {report['dimensions']['1_os']['system']} {report['dimensions']['1_os']['release']} ({report['dimensions']['1_os']['architecture']})")
    print(f" [Python Runtime]:          {report['dimensions']['2_python']['implementation']} {report['dimensions']['2_python']['version']}")
    print(f" [Stdlib Socket]:           {report['dimensions']['3_stdlib_socket']['disposition']}")
    print(f" [Localhost Bind (0)]:      {report['dimensions']['4_localhost_ephemeral_bind']['disposition']} (Port: {report['dimensions']['4_localhost_ephemeral_bind']['sample_ephemeral_port']})")
    print(f" [Embedded SQLite]:         {report['dimensions']['5_embedded_sqlite']['disposition']} (v{report['dimensions']['5_embedded_sqlite']['sqlite_version']})")
    print(f" [Writable Temp Dir]:       {report['dimensions']['6_writable_temp']['disposition']}")
    print(f" [Subprocess Watchdog]:     {report['dimensions']['7_subprocess_watchdog']['disposition']}")
    print(f" [LAB-OPT-02 CS144]:        {report['dimensions']['8_optional_cs144_source']['disposition']}")
    print(f"   Reachability:            {report['dimensions']['8_optional_cs144_source']['reachability']}")
    print(f" [M17 Trace Capability]:    {report['dimensions']['9_m17_trace_capabilities']['disposition']}")
    print(f" [EXP-05 MIT 6.033]:        {report['dimensions']['10_optional_mit_6033_source']['disposition']}")
    print(f"   Reachability:            {report['dimensions']['10_optional_mit_6033_source']['reachability']}")
    print("=" * 70)

    return 0 if (report["m16_core_status"] == "READY" and report["m17_core_status"] == "READY") else 1


if __name__ == "__main__":
    sys.exit(main())
