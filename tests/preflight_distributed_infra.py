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
    "lecture_19_view_server_url": "https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/mit6_033s18lec19/",
    "lecture_19_outline_url": "https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/pages/week-11/lecture-19-outline/",
    "source_correction": "View Server/Primary-Backup availability material is Lecture 19, not Lecture 14",
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
            "disposition": (
                "REQUIRED CAPABILITY PASS"
                if writable
                else "ENVIRONMENT-BLOCKED / NOT RUN"
            ),
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
        "disposition": "SOURCE EXPEDITION / LINK-AND-PARAPHRASE",
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
        record["reachability"] = (
            f"SOURCE RECHECK BLOCKED / CONTINUE WITH COURSE-OWNED TRACE ({e})"
        )

    return record


def probe_m18_coordination_capabilities() -> Dict[str, Any]:
    """
    Probe only capabilities actually required by M18 Core:
    file-backed SQLite commit/rollback behavior in a writable local directory.
    The M18 implementation does not require Python threads.
    """
    try:
        with tempfile.TemporaryDirectory(prefix="essential_cs_m18_probe_") as tmpdir:
            probe_db = os.path.join(tmpdir, "probe_m18.db")
            conn = sqlite3.connect(probe_db, isolation_level=None)
            try:
                conn.execute("CREATE TABLE probe_orders (id TEXT PRIMARY KEY, val TEXT)")

                conn.execute("BEGIN IMMEDIATE")
                conn.execute(
                    "INSERT INTO probe_orders (id, val) VALUES (?, ?)",
                    ("committed_order", "committed"),
                )
                conn.execute("COMMIT")
                committed = conn.execute(
                    "SELECT val FROM probe_orders WHERE id = ?",
                    ("committed_order",),
                ).fetchone()

                conn.execute("BEGIN IMMEDIATE")
                conn.execute(
                    "INSERT INTO probe_orders (id, val) VALUES (?, ?)",
                    ("rolled_back_order", "should_not_persist"),
                )
                conn.execute("ROLLBACK")
                rolled_back = conn.execute(
                    "SELECT val FROM probe_orders WHERE id = ?",
                    ("rolled_back_order",),
                ).fetchone()
            finally:
                conn.close()

        functional = committed == ("committed",) and rolled_back is None
        return {
            "available": functional,
            "sqlite_file_tx": functional,
            "commit_functional": committed == ("committed",),
            "rollback_functional": rolled_back is None,
            "disposition": (
                "REQUIRED CAPABILITY PASS"
                if functional
                else "ENVIRONMENT-BLOCKED / NOT RUN"
            ),
        }
    except Exception as e:
        return {
            "available": False,
            "sqlite_file_tx": False,
            "commit_functional": False,
            "rollback_functional": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": str(e),
        }


def probe_m19_linux_capabilities() -> Dict[str, Any]:
    """
    Probe capabilities required by M19 Core:
    read-only Linux namespace and cgroup observation in /proc and /sys/fs/cgroup.
    Non-Linux hosts report ENVIRONMENT-BLOCKED / NOT RUN truthfully without mutation.
    Docker/Podman and unshare are NOT required for Core readiness.
    """
    is_linux = platform.system() == "Linux"
    if not is_linux:
        return {
            "available": False,
            "is_canonical_linux": False,
            "proc_ns_readable": False,
            "proc_cgroup_readable": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "reason": (
                f"Non-Linux host ({platform.system()} {platform.release()}). "
                "M19 Core baseline requires canonical Linux environment with /proc/self/ns "
                "and /proc/self/cgroup access (e.g. native Linux, WSL2, or Linux VM)."
            ),
        }

    proc_ns_readable = os.path.exists("/proc/self/ns") and os.access("/proc/self/ns", os.R_OK)
    proc_cgroup_readable = os.path.exists("/proc/self/cgroup") and os.access("/proc/self/cgroup", os.R_OK)

    available = proc_ns_readable and proc_cgroup_readable
    return {
        "available": available,
        "is_canonical_linux": True,
        "proc_ns_readable": proc_ns_readable,
        "proc_cgroup_readable": proc_cgroup_readable,
        "disposition": (
            "REQUIRED CAPABILITY PASS"
            if available
            else "ENVIRONMENT-BLOCKED / NOT RUN"
        ),
        "reason": (
            "Canonical Linux read-only inspection baseline accessible."
            if available
            else "Linux host detected, but /proc/self/ns or /proc/self/cgroup is not readable."
        ),
    }


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
    m18_coord_info = probe_m18_coordination_capabilities()
    m19_linux_info = probe_m19_linux_capabilities()

    m16_core_ready = (
        sock_info["available"]
        and bind_info["bound"]
        and sqlite_info["available"]
        and temp_info["writable"]
        and watchdog_info["watchdog_usable"]
    )

    m17_core_ready = m17_trace_info["available"] and temp_info["writable"]

    m18_core_ready = (
        sqlite_info["available"]
        and temp_info["writable"]
        and m18_coord_info["available"]
    )

    m19_core_ready = (
        m19_linux_info["available"]
        and temp_info["writable"]
    )

    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "oq_bp_006_status": "OPEN / UNRESOLVED",
        "m16_core_status": "READY" if m16_core_ready else "BLOCKED",
        "m17_core_status": "READY" if m17_core_ready else "BLOCKED",
        "m18_core_status": "READY" if m18_core_ready else "BLOCKED",
        "m19_core_status": "READY" if m19_core_ready else "BLOCKED",
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
            "11_m18_coordination_capabilities": m18_coord_info,
            "12_m19_linux_capabilities": m19_linux_info,
        },
        "notes": (
            "Readiness is not lesson/lab PASS. "
            "M16, M17, and M18 use standard Python stdlib capabilities which are cross-platform. "
            "M19 requires canonical Linux read-only observation (/proc/self/ns and /proc/self/cgroup). "
            "OQ-BP-006 remains open for the wider course curriculum."
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
        dims = report["dimensions"]

        expected_status = (
            "READY"
            if (
                dims["9_m17_trace_capabilities"]["available"]
                and dims["6_writable_temp"]["writable"]
            )
            else "BLOCKED"
        )
        self.assertEqual(report["m17_core_status"], expected_status)
        self.assertIn(
            dims["9_m17_trace_capabilities"]["disposition"],
            {"REQUIRED CAPABILITY PASS", "ENVIRONMENT-BLOCKED / NOT RUN"},
        )
        self.assertEqual(
            dims["10_optional_mit_6033_source"]["disposition"],
            "SOURCE EXPEDITION / LINK-AND-PARAPHRASE",
        )
        self.assertEqual(
            dims["10_optional_mit_6033_source"]["vendoring"],
            "ZERO VENDORED SOURCE",
        )

    def test_m18_core_capabilities_report_truthfully(self):
        report = run_preflight()
        dims = report["dimensions"]

        expected_status = (
            "READY"
            if (
                dims["5_embedded_sqlite"]["available"]
                and dims["6_writable_temp"]["writable"]
                and dims["11_m18_coordination_capabilities"]["available"]
            )
            else "BLOCKED"
        )
        self.assertEqual(report["m18_core_status"], expected_status)
        self.assertIn(
            dims["11_m18_coordination_capabilities"]["disposition"],
            {"REQUIRED CAPABILITY PASS", "ENVIRONMENT-BLOCKED / NOT RUN"},
        )

    def test_m19_core_capabilities_report_truthfully(self):
        report = run_preflight()
        dims = report["dimensions"]
        m19_info = dims["12_m19_linux_capabilities"]

        self.assertIn(
            m19_info["disposition"],
            {"REQUIRED CAPABILITY PASS", "ENVIRONMENT-BLOCKED / NOT RUN"},
        )
        if m19_info["available"]:
            self.assertEqual(report["m19_core_status"], "READY")
            self.assertTrue(m19_info["is_canonical_linux"])
            self.assertTrue(m19_info["proc_ns_readable"])
            self.assertTrue(m19_info["proc_cgroup_readable"])
        else:
            self.assertEqual(report["m19_core_status"], "BLOCKED")


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight verification for Stage 6 Distributed Infra")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--check-cs144-source", action="store_true", help="Probe Stanford CS144 reachability")
    parser.add_argument("--check-mit-source", action="store_true", help="Probe MIT 6.033 reachability")
    parser.add_argument(
        "--module",
        choices=("m16", "m17", "m18", "m19", "all"),
        default="m16",
        help=(
            "Select which Core readiness status controls the exit code. "
            "Default m16 preserves the pre-existing M16 preflight behavior."
        ),
    )
    args = parser.parse_args()

    report = run_preflight(check_cs144=args.check_cs144_source, check_mit=args.check_mit_source)

    selected_ready = {
        "m16": report["m16_core_status"] == "READY",
        "m17": report["m17_core_status"] == "READY",
        "m18": report["m18_core_status"] == "READY",
        "m19": report["m19_core_status"] == "READY",
        "all": (
            report["m16_core_status"] == "READY"
            and report["m17_core_status"] == "READY"
            and report["m18_core_status"] == "READY"
            and report["m19_core_status"] == "READY"
        ),
    }[args.module]

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if selected_ready else 1

    print("=" * 70)
    print(" Essential CS: Distributed Infrastructure Preflight Capability Report")
    print("=" * 70)
    print(f" Timestamp:                 {report['timestamp']}")
    print(f" OQ-BP-006 Status:          {report['oq_bp_006_status']}")
    print(f" Selected Exit Gate:        {args.module}")
    print(f" M16 Core Status:           {report['m16_core_status']}")
    print(f" M17 Core Status:           {report['m17_core_status']}")
    print(f" M18 Core Status:           {report['m18_core_status']}")
    print(f" M19 Core Status:           {report['m19_core_status']}")
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
    print(f" [M18 Coordination]:        {report['dimensions']['11_m18_coordination_capabilities']['disposition']}")
    print(f" [M19 Linux Read-Only]:     {report['dimensions']['12_m19_linux_capabilities']['disposition']}")
    if not report['dimensions']['12_m19_linux_capabilities']['available']:
        print(f"   Reason:                  {report['dimensions']['12_m19_linux_capabilities']['reason']}")
    print("=" * 70)

    return 0 if selected_ready else 1


if __name__ == "__main__":
    sys.exit(main())
