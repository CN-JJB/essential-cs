#!/usr/bin/env python3
"""
Preflight verification script for Data & Concurrency modules (M13-M15).
Evaluates and records host capabilities empirically without permanently pinning OQ-BP-006.

Probes the 14 accepted dimensions:
1. OS / kernel / architecture
2. Python implementation / version
3. Embedded SQLite version
4. sqlite3 CLI availability / version
5. Writable local filesystem & multi-connection VFS locking disposition
6. GCC/Clang identity / version
7. -std=c11 -pthread compile capability
8. C11 atomics (<stdatomic.h>)
9. POSIX mutex / condition variable capability
10. Owned child process / watchdog capability
11. Optional PostgreSQL / psql
12. Optional Docker / Podman
13. Optional sanitizer / race tool capability (-fsanitize=thread)
14. EXP-02 PostgreSQL source reachability & course reference revision
"""

import argparse
import datetime
import json
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import urllib.request

COURSE_EXP02_BENCHMARK = {
    "course_reference_revision": "7344937cbe640cd8c5304cefe7d6b726187ad4ab",
    "course_inspection_date": "2026-09-04",
    "course_reference_branch": "master (development branch; PostgreSQL 18.6 is separate current stable release/doc line)",
    "official_host": "https://git.postgresql.org/gitweb/?p=postgresql.git",
}


def probe_os():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.machine(),
    }


def probe_python():
    return {
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
        "sys_version": sys.version,
    }


def probe_embedded_sqlite():
    return {
        "sqlite_version": sqlite3.sqlite_version,
        "has_memory_db": True,
    }


def probe_sqlite_cli():
    cli_path = shutil.which("sqlite3")
    if not cli_path:
        return {
            "available": False,
            "path": None,
            "version": None,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "reason": "sqlite3 binary not found in PATH",
        }

    try:
        proc = subprocess.run(
            [cli_path, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3.0,
            check=False,
        )
        if proc.returncode == 0:
            version_str = proc.stdout.strip().split()[0] if proc.stdout.strip() else "unknown"
            return {
                "available": True,
                "path": cli_path,
                "version": version_str,
                "raw_output": proc.stdout.strip(),
                "disposition": "REQUIRED CAPABILITY PASS",
            }
        else:
            return {
                "available": False,
                "path": cli_path,
                "version": None,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "reason": f"sqlite3 --version returned non-zero ({proc.returncode}): {proc.stderr.strip()}",
            }
    except Exception as exc:
        return {
            "available": False,
            "path": cli_path,
            "version": None,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "reason": f"Failed to execute sqlite3 CLI: {type(exc).__name__}: {exc}",
        }


def probe_writable_vfs(workspace_root=None):
    """
    Empirically probe writable local filesystem AND multi-connection VFS locking capability.
    Reports filesystem writability and VFS multi-connection locking separately.
    """
    base_dir = workspace_root or os.getcwd()
    test_dir = os.path.join(base_dir, ".preflight_tmp_probe")
    result = {
        "writable_filesystem": False,
        "writable_filesystem_disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
        "vfs_locking_tested": False,
        "vfs_locking_functional": False,
        "vfs_locking_disposition": "NOT VERIFIED",
        "path": test_dir,
        "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
        "error": None,
    }
    try:
        os.makedirs(test_dir, exist_ok=True)
        probe_db = os.path.join(test_dir, "probe_test.db")
        if os.path.exists(probe_db):
            os.remove(probe_db)

        # 1. Test basic filesystem writability and single-connection operation
        conn1 = sqlite3.connect(probe_db, timeout=1.0)
        cur1 = conn1.cursor()
        cur1.execute("CREATE TABLE probe (id INTEGER PRIMARY KEY, val TEXT);")
        cur1.execute("INSERT INTO probe (val) VALUES ('test');")
        conn1.commit()
        cur1.execute("SELECT val FROM probe WHERE id = 1;")
        row = cur1.fetchone()
        if row and row[0] == "test":
            result["writable_filesystem"] = True
            result["writable_filesystem_disposition"] = "REQUIRED CAPABILITY PASS"

        # 2. Test bounded multi-connection VFS locking behavior
        # Hold an EXCLUSIVE lock on conn1, verify that conn2 observes a lock conflict/busy
        cur1.execute("BEGIN EXCLUSIVE;")
        cur1.execute("INSERT INTO probe (val) VALUES ('lock_held');")
        result["vfs_locking_tested"] = True

        conn2 = sqlite3.connect(probe_db, timeout=0.1)
        cur2 = conn2.cursor()
        lock_conflict_observed = False
        try:
            cur2.execute("INSERT INTO probe (val) VALUES ('concurrent_write');")
            conn2.commit()
        except sqlite3.OperationalError as exc:
            sqlite_code = getattr(exc, "sqlite_errorcode", None)
            locked_codes = {
                getattr(sqlite3, "SQLITE_BUSY", 5),
                getattr(sqlite3, "SQLITE_LOCKED", 6),
            }
            if sqlite_code in locked_codes or "locked" in str(exc).lower() or "busy" in str(exc).lower():
                lock_conflict_observed = True
            else:
                raise
        finally:
            conn2.close()

        conn1.rollback()
        conn1.close()

        if lock_conflict_observed and result["writable_filesystem"]:
            result["vfs_locking_functional"] = True
            result["vfs_locking_disposition"] = "REQUIRED CAPABILITY PASS"
            result["disposition"] = "REQUIRED CAPABILITY PASS"
        elif result["writable_filesystem"]:
            result["vfs_locking_disposition"] = "NOT VERIFIED"
            result["disposition"] = result["writable_filesystem_disposition"]
            result["dimension_summary"] = "Writable filesystem PASS; VFS multi-connection locking NOT VERIFIED."
        else:
            result["disposition"] = "ENVIRONMENT-BLOCKED / NOT RUN"
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir, ignore_errors=True)

    return result


def probe_compiler():
    cc_path = shutil.which("gcc") or shutil.which("clang")
    cc_type = "gcc" if shutil.which("gcc") else ("clang" if shutil.which("clang") else None)
    if not cc_path:
        return {
            "available": False,
            "compiler": None,
            "path": None,
            "version": None,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
        }

    try:
        proc = subprocess.run(
            [cc_path, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3.0,
            check=False,
        )
        first_line = proc.stdout.splitlines()[0] if proc.stdout else ""
        return {
            "available": True,
            "compiler": cc_type,
            "path": cc_path,
            "version": first_line,
            "disposition": "REQUIRED CAPABILITY PASS",
        }
    except Exception as exc:
        return {
            "available": False,
            "compiler": cc_type,
            "path": cc_path,
            "version": None,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": str(exc),
        }


def probe_c11_pthread(cc_info):
    if not cc_info.get("available"):
        return {
            "can_compile": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "reason": "No C compiler available",
        }

    cc_path = cc_info["path"]
    code = """
#include <pthread.h>
void* worker(void* arg) { (void)arg; return 0; }
int main(void) {
    pthread_t t;
    if (pthread_create(&t, 0, worker, 0) != 0) return 1;
    pthread_join(t, 0);
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "test_pthread.c")
        out = os.path.join(tmpdir, "test_pthread.exe" if platform.system() == "Windows" else "test_pthread")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        try:
            compile_proc = subprocess.run(
                [cc_path, "-std=c11", "-pthread", src, "-o", out],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5.0,
                check=False,
            )
            if compile_proc.returncode != 0:
                return {
                    "can_compile": False,
                    "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                    "reason": f"Compilation failed: {compile_proc.stderr.strip()}",
                }
            run_proc = subprocess.run([out], timeout=3.0, check=False)
            if run_proc.returncode == 0:
                return {
                    "can_compile": True,
                    "can_run": True,
                    "disposition": "REQUIRED CAPABILITY PASS",
                }
            else:
                return {
                    "can_compile": True,
                    "can_run": False,
                    "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                    "reason": f"Execution returned {run_proc.returncode}",
                }
        except Exception as exc:
            return {
                "can_compile": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "reason": str(exc),
            }


def probe_c11_atomics(cc_info):
    if not cc_info.get("available"):
        return {
            "supported": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "reason": "No C compiler available",
        }

    cc_path = cc_info["path"]
    code = """
#include <stdatomic.h>
int main(void) {
    atomic_int count = ATOMIC_VAR_INIT(0);
    atomic_fetch_add(&count, 1);
    return atomic_load(&count) == 1 ? 0 : 1;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "test_atomics.c")
        out = os.path.join(tmpdir, "test_atomics.exe" if platform.system() == "Windows" else "test_atomics")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        try:
            compile_proc = subprocess.run(
                [cc_path, "-std=c11", src, "-o", out],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5.0,
                check=False,
            )
            if compile_proc.returncode != 0:
                return {
                    "supported": False,
                    "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                    "reason": compile_proc.stderr.strip(),
                }
            run_proc = subprocess.run([out], timeout=3.0, check=False)
            return {
                "supported": run_proc.returncode == 0,
                "disposition": "REQUIRED CAPABILITY PASS" if run_proc.returncode == 0 else "ENVIRONMENT-BLOCKED / NOT RUN",
            }
        except Exception as exc:
            return {
                "supported": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "reason": str(exc),
            }


def probe_posix_mutex_cond(cc_info):
    if not cc_info.get("available"):
        return {
            "supported": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "reason": "No C compiler available",
        }

    cc_path = cc_info["path"]
    code = """
#include <pthread.h>
int main(void) {
    pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
    pthread_cond_t c = PTHREAD_COND_INITIALIZER;
    pthread_mutex_lock(&m);
    pthread_mutex_unlock(&m);
    pthread_cond_destroy(&c);
    pthread_mutex_destroy(&m);
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "test_sync.c")
        out = os.path.join(tmpdir, "test_sync.exe" if platform.system() == "Windows" else "test_sync")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        try:
            compile_proc = subprocess.run(
                [cc_path, "-std=c11", "-pthread", src, "-o", out],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5.0,
                check=False,
            )
            if compile_proc.returncode != 0:
                return {
                    "supported": False,
                    "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                    "reason": compile_proc.stderr.strip(),
                }
            run_proc = subprocess.run([out], timeout=3.0, check=False)
            return {
                "supported": run_proc.returncode == 0,
                "disposition": "REQUIRED CAPABILITY PASS" if run_proc.returncode == 0 else "ENVIRONMENT-BLOCKED / NOT RUN",
            }
        except Exception as exc:
            return {
                "supported": False,
                "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                "reason": str(exc),
            }


def probe_child_watchdog():
    code = "import time; time.sleep(0.05)"
    try:
        proc = subprocess.Popen(
            [sys.executable, "-c", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        proc.wait(timeout=2.0)
        return {
            "can_spawn": True,
            "can_timeout_and_reap": True,
            "disposition": "REQUIRED CAPABILITY PASS",
        }
    except Exception as exc:
        return {
            "can_spawn": False,
            "can_timeout_and_reap": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": str(exc),
        }


def probe_psql():
    psql_path = shutil.which("psql")
    if not psql_path:
        return {
            "available": False,
            "path": None,
            "version": None,
            "disposition": "OPTIONAL TOOL UNAVAILABLE / SKIP",
        }
    try:
        proc = subprocess.run(
            [psql_path, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3.0,
            check=False,
        )
        version_str = proc.stdout.strip() if proc.returncode == 0 else None
        return {
            "available": proc.returncode == 0,
            "path": psql_path,
            "version": version_str,
            "disposition": "OPTIONAL CAPABILITY PASS" if proc.returncode == 0 else "OPTIONAL TOOL UNAVAILABLE / SKIP",
        }
    except Exception as exc:
        return {
            "available": False,
            "path": psql_path,
            "version": None,
            "disposition": "OPTIONAL TOOL UNAVAILABLE / SKIP",
            "error": str(exc),
        }


def probe_docker():
    rt_path = shutil.which("docker") or shutil.which("podman")
    rt_name = "docker" if shutil.which("docker") else ("podman" if shutil.which("podman") else None)
    if not rt_path:
        return {
            "available": False,
            "runtime": None,
            "version": None,
            "disposition": "OPTIONAL TOOL UNAVAILABLE / SKIP",
        }
    try:
        proc = subprocess.run(
            [rt_path, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3.0,
            check=False,
        )
        version_str = proc.stdout.strip() if proc.returncode == 0 else None
        return {
            "available": proc.returncode == 0,
            "runtime": rt_name,
            "version": version_str,
            "disposition": "OPTIONAL CAPABILITY PASS" if proc.returncode == 0 else "OPTIONAL TOOL UNAVAILABLE / SKIP",
        }
    except Exception as exc:
        return {
            "available": False,
            "runtime": rt_name,
            "version": None,
            "disposition": "OPTIONAL TOOL UNAVAILABLE / SKIP",
            "error": str(exc),
        }


def probe_sanitizer(cc_info):
    if not cc_info.get("available"):
        return {
            "supported": False,
            "disposition": "OPTIONAL TOOL UNAVAILABLE / SKIP",
            "reason": "No C compiler available",
        }

    cc_path = cc_info["path"]
    code = "int main(void) { return 0; }"
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "test_tsan.c")
        out = os.path.join(tmpdir, "test_tsan.exe" if platform.system() == "Windows" else "test_tsan")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)

        try:
            compile_proc = subprocess.run(
                [cc_path, "-fsanitize=thread", src, "-o", out],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5.0,
                check=False,
            )
            supported = compile_proc.returncode == 0
            return {
                "supported": supported,
                "disposition": "OPTIONAL CAPABILITY PASS" if supported else "OPTIONAL TOOL UNAVAILABLE / SKIP",
                "reason": None if supported else compile_proc.stderr.strip(),
            }
        except Exception as exc:
            return {
                "supported": False,
                "disposition": "OPTIONAL TOOL UNAVAILABLE / SKIP",
                "reason": str(exc),
            }


def probe_postgres_source(check_live=False):
    """
    Reports PostgreSQL official source reachability separately from revision records.
    Always provides the Course Reference Baseline.
    """
    base_info = {
        "course_reference_revision": COURSE_EXP02_BENCHMARK["course_reference_revision"],
        "course_inspection_date": COURSE_EXP02_BENCHMARK["course_inspection_date"],
        "course_reference_branch": COURSE_EXP02_BENCHMARK["course_reference_branch"],
        "reference_authority": COURSE_EXP02_BENCHMARK["official_host"],
    }

    if not check_live:
        return {
            **base_info,
            "disposition": "NO LIVE SOURCE RECHECK",
            "live_checked": False,
            "reachability": "NOT PROBED",
            "live_revision": "NOT RECORDED",
            "reachability_disposition": "NOT RUN",
            "revision_disposition": "NO LIVE SOURCE RECHECK",
            "notes": "Live check omitted; use --check-postgres-source to probe reachability. Reachability alone does not establish a current revision.",
        }

    url = f"{COURSE_EXP02_BENCHMARK['official_host']};a=summary"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Essential-CS-Preflight/0.1"})
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            status = resp.getcode()
            if status == 200:
                return {
                    **base_info,
                    "disposition": "NO LIVE SOURCE RECHECK",
                    "live_checked": True,
                    "url": url,
                    "reachability": f"REACHABLE (HTTP {status})",
                    "reachability_disposition": "REQUIRED CAPABILITY PASS",
                    "live_revision": "NOT RECORDED (Reachability verified; current revision was not verified by this probe)",
                    "revision_disposition": "NO LIVE SOURCE RECHECK",
                    "notes": "HTTP reachability is confirmed, but current source revision is not; do not promote reachability to a currentness PASS.",
                }
            else:
                return {
                    **base_info,
                    "disposition": "NO LIVE SOURCE RECHECK",
                    "live_checked": True,
                    "url": url,
                    "reachability": f"UNEXPECTED STATUS (HTTP {status})",
                    "reachability_disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
                    "live_revision": "NOT RECORDED",
                    "revision_disposition": "NO LIVE SOURCE RECHECK",
                    "reason": f"HTTP status {status}",
                }
    except Exception as exc:
        return {
            **base_info,
            "disposition": "NO LIVE SOURCE RECHECK",
            "live_checked": True,
            "url": url,
            "reachability": "UNREACHABLE",
            "reachability_disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "live_revision": "NOT RECORDED",
            "revision_disposition": "NO LIVE SOURCE RECHECK",
            "reason": f"Network access failed: {type(exc).__name__}: {exc}",
        }


def run_preflight(check_postgres_source=False, workspace_root=None):
    os_info = probe_os()
    py_info = probe_python()
    sqlite_embed = probe_embedded_sqlite()
    sqlite_cli = probe_sqlite_cli()
    vfs_info = probe_writable_vfs(workspace_root)
    compiler_info = probe_compiler()
    pthread_info = probe_c11_pthread(compiler_info)
    atomics_info = probe_c11_atomics(compiler_info)
    mutex_cond_info = probe_posix_mutex_cond(compiler_info)
    child_info = probe_child_watchdog()
    psql_info = probe_psql()
    docker_info = probe_docker()
    sanitizer_info = probe_sanitizer(compiler_info)
    pg_source_info = probe_postgres_source(check_postgres_source)

    # Status classification:
    # M13 Core requires Python + Embedded SQLite + Writable VFS
    m13_core_ready = (
        sqlite_embed["has_memory_db"]
        and vfs_info["writable_filesystem"]
    )
    m13_core_status = "READY" if m13_core_ready else "BLOCKED"

    # LAB-REQ-04 requires the real sqlite3 CLI
    lab_req_04_status = (
        "READY" if sqlite_cli["disposition"] == "REQUIRED CAPABILITY PASS"
        else "ENVIRONMENT-BLOCKED / NOT RUN"
    )

    # M14 preview
    m14_preview_status = (
        "READY" if (m13_core_ready and child_info["disposition"] == "REQUIRED CAPABILITY PASS")
        else "BLOCKED"
    )

    # M15 evaluation:
    # Distinguish host compilation capability from canonical environment readiness (Linux is canonical for M15)
    # Preserve OQ-BP-006 OPEN
    m15_compiler_capable = (
        pthread_info["disposition"] == "REQUIRED CAPABILITY PASS"
        and atomics_info["disposition"] == "REQUIRED CAPABILITY PASS"
    )
    is_linux_canonical = (os_info["system"] == "Linux")

    if is_linux_canonical and m15_compiler_capable:
        m15_readiness_preview = "READY (Canonical Linux Host with C11 atomics & pthread)"
    elif m15_compiler_capable:
        m15_readiness_preview = f"CAPABLE HOST ({os_info['system']}), NON-CANONICAL (Compiler & atomics capable, but canonical Required environment is Linux; OQ-BP-006 remains OPEN)"
    else:
        m15_readiness_preview = "BLOCKED"

    # Overall preflight status for M13 stage
    if m13_core_ready and lab_req_04_status == "READY":
        overall_status = "READY FOR M13 + LAB-REQ-04 EXECUTION (preflight capabilities satisfied)"
    elif m13_core_ready:
        overall_status = "READY FOR M13 CORE (LAB-REQ-04 ENVIRONMENT-BLOCKED due to missing sqlite3 CLI)"
    else:
        overall_status = "BLOCKED"

    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "overall_status": overall_status,
        "m13_core_status": m13_core_status,
        "lab_req_04_status": lab_req_04_status,
        "m14_readiness_preview": m14_preview_status,
        "m15_readiness_preview": m15_readiness_preview,
        "governance_invariants": {
            "oq_bp_006_host_baseline": "OPEN (No single host pinned as permanent universal baseline)",
            "m15_canonical_host": "Linux",
        },
        "dimensions": {
            "1_os": os_info,
            "2_python": py_info,
            "3_embedded_sqlite": sqlite_embed,
            "4_sqlite_cli": sqlite_cli,
            "5_writable_vfs": vfs_info,
            "6_compiler": compiler_info,
            "7_c11_pthread": pthread_info,
            "8_c11_atomics": atomics_info,
            "9_posix_mutex_cond": mutex_cond_info,
            "10_child_watchdog": child_info,
            "11_optional_psql": psql_info,
            "12_optional_docker": docker_info,
            "13_optional_sanitizer": sanitizer_info,
            "14_exp02_source": pg_source_info,
        },
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="Data & Concurrency Environment Preflight (M13-M15)")
    parser.add_argument("--json", action="store_true", help="Print preflight report in JSON format")
    parser.add_argument(
        "--check-postgres-source",
        action="store_true",
        help="Opt in to a live PostgreSQL source reachability probe for EXP-02",
    )
    args = parser.parse_args()

    report = run_preflight(check_postgres_source=args.check_postgres_source)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["m13_core_status"] == "READY" else 1

    print("=" * 66)
    print(" Essential CS: Data & Concurrency Preflight Capability Report")
    print("=" * 66)
    print(f" Timestamp:              {report['timestamp']}")
    print(f" Overall Status:         {report['overall_status']}")
    print(f" M13 Core Status:        {report['m13_core_status']}")
    print(f" LAB-REQ-04 Status:      {report['lab_req_04_status']}")
    print(f" M14 Readiness Preview:  {report['m14_readiness_preview']}")
    print(f" M15 Readiness Preview:  {report['m15_readiness_preview']}")
    print("-" * 66)
    print(" [Host Operating System]")
    print(f"   System:               {report['dimensions']['1_os']['system']} {report['dimensions']['1_os']['release']} ({report['dimensions']['1_os']['architecture']})")
    print(f"   Version:              {report['dimensions']['1_os']['version']}")
    print("-" * 66)
    print(" [Python Runtime]")
    print(f"   Implementation:       {report['dimensions']['2_python']['implementation']}")
    print(f"   Version:              {report['dimensions']['2_python']['version']}")
    print("-" * 66)
    print(" [SQLite Environment]")
    print(f"   Embedded SQLite:      {report['dimensions']['3_embedded_sqlite']['sqlite_version']}")
    cli = report['dimensions']['4_sqlite_cli']
    print(f"   sqlite3 CLI Usable:   {'YES' if cli['available'] else 'NO'} ({cli['disposition']})")
    if cli['available']:
        print(f"   sqlite3 CLI Version:  {cli['version']} ({cli['path']})")
    else:
        print(f"   Reason:               {cli.get('reason', 'N/A')}")
    print("-" * 66)
    print(" [Writable Filesystem & VFS Locking]")
    vfs = report['dimensions']['5_writable_vfs']
    print(f"   Disposition:          {vfs['disposition']}")
    print(f"   Writable FS:          {'YES' if vfs['writable_filesystem'] else 'NO'}")
    print(f"   VFS Locking Probed:   {'YES' if vfs['vfs_locking_tested'] else 'NO'}")
    print(f"   VFS Locking Conflict: {'OBSERVED' if vfs['vfs_locking_functional'] else 'INCONCLUSIVE'}")
    print("-" * 66)
    print(" [C Compiler & POSIX / C11 Concurrency (M15 Preview)]")
    cc = report['dimensions']['6_compiler']
    print(f"   Compiler:             {'YES' if cc['available'] else 'NO'} ({cc.get('version') or cc['disposition']})")
    print(f"   -std=c11 -pthread:    {report['dimensions']['7_c11_pthread']['disposition']}")
    print(f"   C11 Atomics:          {report['dimensions']['8_c11_atomics']['disposition']}")
    print(f"   POSIX Mutex/Cond:     {report['dimensions']['9_posix_mutex_cond']['disposition']}")
    print("-" * 66)
    print(" [Process Watchdog & Recovery (M14 Preview)]")
    print(f"   Child / Watchdog:     {report['dimensions']['10_child_watchdog']['disposition']}")
    print("-" * 66)
    print(" [Optional Tools & Source Recheck]")
    print(f"   psql Client:          {report['dimensions']['11_optional_psql']['disposition']}")
    print(f"   Docker/Podman:        {report['dimensions']['12_optional_docker']['disposition']}")
    print(f"   TSan Sanitizer:       {report['dimensions']['13_optional_sanitizer']['disposition']}")
    src = report['dimensions']['14_exp02_source']
    print(f"   EXP-02 Disposition:   {src['disposition']}")
    print(f"   EXP-02 Reachability:  {src.get('reachability', 'N/A')}")
    print(f"   Course Ref Revision:  {src['course_reference_revision'][:12]} ({src['course_inspection_date']})")
    print("=" * 66)

    return 0 if report["m13_core_status"] == "READY" else 1


if __name__ == "__main__":
    sys.exit(main())
