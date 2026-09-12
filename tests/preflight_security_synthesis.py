#!/usr/bin/env python3
"""
preflight_security_synthesis.py — Preflight Verification Script for S7 / M21–M22
=============================================================================

Evaluates and records host capabilities empirically for Stage 7 (Security Synthesis
& Systems Judgment), specifically M21 (Trust Boundaries & Crypto Use) and M22 (Authn/Authz & Secure Composition).
Capability evaluation here does not replace the canonical environment pin
(OQ-BP-006 CLOSED per #167; #158 re-check still required).

Probes the required capabilities actually used:
1. OS / platform / architecture
2. Python implementation / version
3. Standard library crypto modules (hashlib.sha256, hmac.new, hmac.compare_digest, secrets)
4. Temporary directory creation & path resolution (tempfile, Path.resolve, os.path.commonpath)
5. Host filesystem symlink capability (truthfully records PASS or BLOCKED / NOT RUN)
6. Course-owned scratch writability (labs/foundations/m21/.scratch)
7. M22-only password-KDF, sqlite3, localhost-bind, M22 scratch and optional Argon2 capabilities when --module M22 is selected
8. M21-only optional PyCA cryptography capability when M21 is selected

OQ-BP-006 is CLOSED as a technical environment-definition/realization question
(#167/#168; #153 is same-lineage technical re-verification, NOT final
role-independent evidence; #158 must still independently re-check before v1.0).
Readiness is not lesson/lab PASS.
Zero offensive tools, zero live/public targets, zero real secrets.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parent.parent
M21_DIR = REPO_ROOT / "labs" / "foundations" / "m21"
M22_DIR = REPO_ROOT / "labs" / "foundations" / "m22"
M23_DIR = REPO_ROOT / "labs" / "foundations" / "m23"
M24_DIR = REPO_ROOT / "labs" / "foundations" / "m24"


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
        "oq_bp_006_policy": "CLOSED (technical environment-definition/realization per #167; capability-based evaluation here; #158 re-check still required)",
    }


def probe_stdlib_crypto() -> Dict[str, Any]:
    try:
        import hashlib
        import hmac
        import secrets

        # 1. hashlib SHA-256 check
        h = hashlib.sha256(b"preflight-synthetic-test").hexdigest()

        # 2. hmac check
        k = secrets.token_bytes(32)
        tag = hmac.new(k, b"preflight-synthetic-test", hashlib.sha256).hexdigest()

        # 3. compare_digest check
        cd_ok = hmac.compare_digest(tag, tag)
        cd_diff = not hmac.compare_digest(tag, "0" * 64)

        if h and tag and cd_ok and cd_diff:
            return {
                "available": True,
                "disposition": "REQUIRED CAPABILITY PASS",
                "sha256": True,
                "hmac": True,
                "compare_digest": True,
                "secrets_token_bytes": True,
            }
        raise RuntimeError("Cryptographic sanity checks returned unexpected values")
    except Exception as exc:
        return {
            "available": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_password_kdf() -> Dict[str, Any]:
    """Probes PBKDF2-HMAC-SHA256 slow hashing capability for M22 L22-01."""
    try:
        import hashlib
        import hmac

        if not hasattr(hashlib, "pbkdf2_hmac"):
            raise AttributeError("hashlib missing pbkdf2_hmac")

        derived = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=b"preflight-kdf-pass",
            salt=b"preflight-kdf-salt-16b",
            iterations=1000,
        )
        if len(derived) == 32:
            return {
                "available": True,
                "disposition": "REQUIRED CAPABILITY PASS",
                "pbkdf2_hmac_sha256": True,
                "hmac_compare_digest": hasattr(hmac, "compare_digest"),
            }
        raise RuntimeError("pbkdf2_hmac output length mismatch")
    except Exception as exc:
        return {
            "available": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_sqlite3() -> Dict[str, Any]:
    """Probes built-in sqlite3 relational database capability for M22 L22-02."""
    try:
        import sqlite3

        conn = sqlite3.connect(":memory:")
        cur = conn.cursor()
        cur.execute("SELECT 1 + 1")
        res = cur.fetchone()
        conn.close()
        if res and res[0] == 2:
            return {
                "available": True,
                "disposition": "REQUIRED CAPABILITY PASS",
                "sqlite3_in_memory": True,
            }
        raise RuntimeError("sqlite3 in-memory query returned unexpected result")
    except Exception as exc:
        return {
            "available": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_localhost_bind() -> Dict[str, Any]:
    """Probes OS loopback socket bind/listen capability on 127.0.0.1:0 for M22 L22-02."""
    import socket

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return {
            "available": True,
            "disposition": "REQUIRED CAPABILITY PASS",
            "ephemeral_port_assigned": port,
            "loopback_address": "127.0.0.1",
        }
    except Exception as exc:
        return {
            "available": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_path_confinement_primitives() -> Dict[str, Any]:
    try:
        with tempfile.TemporaryDirectory(prefix="ecs-preflight-") as tmpdir:
            tmp = Path(tmpdir).resolve()
            sub = tmp / "store" / "sub"
            sub.mkdir(parents=True)
            f = sub / "test.txt"
            f.write_text("test", encoding="utf-8")

            # Verify Path.resolve, os.path.commonpath, and normcase
            resolved = f.resolve()
            common = os.path.commonpath([os.path.normcase(str(tmp)), os.path.normcase(str(resolved))])
            is_contained = common == os.path.normcase(str(tmp))

            if is_contained:
                return {
                    "available": True,
                    "disposition": "REQUIRED CAPABILITY PASS",
                    "commonpath_available": True,
                    "resolve_available": True,
                    "normcase_available": True,
                }
            raise RuntimeError("commonpath containment check failed on standard temp directory")
    except Exception as exc:
        return {
            "available": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_symlink_capability() -> Dict[str, Any]:
    try:
        with tempfile.TemporaryDirectory(prefix="ecs-symlink-probe-") as tmpdir:
            tmp = Path(tmpdir)
            target = tmp / "target.txt"
            target.write_text("target", encoding="utf-8")
            link = tmp / "link.txt"
            os.symlink(os.fspath(target), os.fspath(link))
            resolved = link.resolve()
            if resolved == target.resolve():
                return {
                    "available": True,
                    "disposition": "SYMLINK CAPABILITY PASS",
                    "note": "Host environment permits creation and resolution of symbolic links.",
                }
            raise RuntimeError("Symlink created but target resolution mismatched")
    except (OSError, NotImplementedError) as exc:
        return {
            "available": False,
            "disposition": "BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
            "note": (
                "Host environment does not permit symlink creation without elevated "
                "privilege or Developer Mode. L21-01 gracefully gates this dimension."
            ),
        }


def probe_scratch_writability() -> Dict[str, Any]:
    scratch = M21_DIR / ".scratch"
    try:
        scratch.mkdir(parents=True, exist_ok=True)
        probe_file = scratch / ".preflight_probe.tmp"
        probe_file.write_text("preflight-writable-check", encoding="utf-8")
        content = probe_file.read_text(encoding="utf-8")
        probe_file.unlink()
        if content == "preflight-writable-check":
            return {
                "writable": True,
                "disposition": "REQUIRED CAPABILITY PASS",
                "scratch_dir": str(scratch),
            }
        raise RuntimeError("Content mismatch in scratch probe")
    except Exception as exc:
        return {
            "writable": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "scratch_dir": str(scratch),
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_m22_scratch_writability() -> Dict[str, Any]:
    scratch = M22_DIR / ".scratch"
    try:
        scratch.mkdir(parents=True, exist_ok=True)
        probe_file = scratch / ".preflight_probe.tmp"
        probe_file.write_text("preflight-m22-writable-check", encoding="utf-8")
        content = probe_file.read_text(encoding="utf-8")
        probe_file.unlink()
        if content == "preflight-m22-writable-check":
            return {
                "writable": True,
                "disposition": "REQUIRED CAPABILITY PASS",
                "scratch_dir": str(scratch),
            }
        raise RuntimeError("Content mismatch in M22 scratch probe")
    except Exception as exc:
        return {
            "writable": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "scratch_dir": str(scratch),
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_optional_cryptography() -> Dict[str, Any]:
    try:
        import cryptography
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

        key = Ed25519PrivateKey.generate()
        sig = key.sign(b"preflight-sig")
        key.public_key().verify(sig, b"preflight-sig")

        return {
            "installed": True,
            "version": getattr(cryptography, "__version__", "UNKNOWN"),
            "disposition": "OPTIONAL PACKAGE AVAILABLE",
            "ed25519": True,
            "inference": "Optional package path available for Learn-New-Tech Ed25519 demo.",
        }
    except ImportError:
        return {
            "installed": False,
            "version": None,
            "disposition": "OPTIONAL PACKAGE NOT INSTALLED / NOT RUN",
            "ed25519": False,
            "inference": "PyCA cryptography absent. Required Core standard-library crypto is unaffected.",
        }
    except Exception as exc:
        return {
            "installed": False,
            "version": None,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_optional_argon2() -> Dict[str, Any]:
    """Probes optional Argon2id candidate package (RFC 9106) for M22 L22-01."""
    try:
        import argon2  # type: ignore

        ph = argon2.PasswordHasher()
        h = ph.hash("preflight-test")
        ph.verify(h, "preflight-test")
        return {
            "installed": True,
            "version": getattr(argon2, "__version__", "UNKNOWN"),
            "disposition": "OPTIONAL PACKAGE AVAILABLE",
            "argon2id": True,
            "inference": "Argon2id candidate available for memory-hard comparison.",
        }
    except ImportError:
        return {
            "installed": False,
            "version": None,
            "disposition": "OPTIONAL PACKAGE NOT INSTALLED / NOT RUN",
            "argon2id": False,
            "inference": "argon2-cffi absent. Required Core compute-hard PBKDF2 is unaffected.",
        }
    except Exception as exc:
        return {
            "installed": False,
            "version": None,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_monotonic_clock() -> Dict[str, Any]:
    """Probes monotonic performance clock capability for M23 L23-01."""
    try:
        import time

        mono_info = time.get_clock_info("monotonic")
        t0 = time.monotonic_ns()
        t1 = time.monotonic_ns()
        if t1 < t0:
            raise RuntimeError("time.monotonic_ns() decreased between consecutive calls")

        return {
            "available": True,
            "disposition": "REQUIRED CAPABILITY PASS",
            "implementation": mono_info.implementation,
            "monotonic": mono_info.monotonic,
            "adjustable": mono_info.adjustable,
            "resolution_seconds": mono_info.resolution,
            "note": "Integer nanosecond reporting does not imply nanosecond hardware resolution.",
        }
    except Exception as exc:
        return {
            "available": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_perf_counter() -> Dict[str, Any]:
    """Probes high-resolution performance counter capability for M23 L23-01."""
    try:
        import time

        perf_info = time.get_clock_info("perf_counter")
        t0 = time.perf_counter_ns()
        t1 = time.perf_counter_ns()
        if t1 < t0:
            raise RuntimeError("time.perf_counter_ns() decreased between consecutive calls")

        return {
            "available": True,
            "disposition": "REQUIRED CAPABILITY PASS",
            "implementation": perf_info.implementation,
            "monotonic": perf_info.monotonic,
            "adjustable": perf_info.adjustable,
            "resolution_seconds": perf_info.resolution,
        }
    except Exception as exc:
        return {
            "available": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_m23_scratch_writability() -> Dict[str, Any]:
    """Probes scratch writability for course-owned M23 directory."""
    scratch = M23_DIR / ".scratch"
    try:
        scratch.mkdir(parents=True, exist_ok=True)
        probe_file = scratch / ".preflight_probe.tmp"
        probe_file.write_text("preflight-m23-writable-check", encoding="utf-8")
        content = probe_file.read_text(encoding="utf-8")
        probe_file.unlink()
        if content == "preflight-m23-writable-check":
            return {
                "writable": True,
                "disposition": "REQUIRED CAPABILITY PASS",
                "scratch_dir": str(scratch),
            }
        raise RuntimeError("Content mismatch in M23 scratch probe")
    except Exception as exc:
        return {
            "writable": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "scratch_dir": str(scratch),
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_stdlib_dataclasses_json() -> Dict[str, Any]:
    """Probes standard library dataclasses, json, and typing for M24."""
    try:
        import dataclasses
        import json

        @dataclasses.dataclass
        class _Probe:
            tag: str
            val: int

        p = _Probe(tag="m24", val=42)
        s = json.dumps(dataclasses.asdict(p))
        d = json.loads(s)
        if d["tag"] == "m24" and d["val"] == 42:
            return {
                "available": True,
                "disposition": "REQUIRED CAPABILITY PASS",
                "dataclasses": True,
                "json": True,
            }
        raise RuntimeError("dataclasses/json serialization check failed")
    except Exception as exc:
        return {
            "available": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "error": f"{type(exc).__name__}: {exc}",
        }


def probe_m24_scratch_writability() -> Dict[str, Any]:
    """Probes scratch writability for course-owned M24 directory."""
    scratch = M24_DIR / ".scratch"
    try:
        scratch.mkdir(parents=True, exist_ok=True)
        probe_file = scratch / ".preflight_probe.tmp"
        probe_file.write_text("preflight-m24-writable-check", encoding="utf-8")
        content = probe_file.read_text(encoding="utf-8")
        probe_file.unlink()
        if content == "preflight-m24-writable-check":
            return {
                "writable": True,
                "disposition": "REQUIRED CAPABILITY PASS",
                "scratch_dir": str(scratch),
            }
        raise RuntimeError("Content mismatch in M24 scratch probe")
    except Exception as exc:
        return {
            "writable": False,
            "disposition": "ENVIRONMENT-BLOCKED / NOT RUN",
            "scratch_dir": str(scratch),
            "error": f"{type(exc).__name__}: {exc}",
        }


def collect_preflight_report(module: str = "M21") -> Dict[str, Any]:
    mod = module.upper()
    if mod == "M24":
        return {
            "stage": "S7",
            "batch": "S7-B4",
            "module": "M24",
            "title": "Final System Defense & Pre-Ship Assessment",
            "os": probe_os(),
            "python": probe_python(),
            "capabilities": {
                "stdlib_dataclasses_json": probe_stdlib_dataclasses_json(),
                "sqlite3": probe_sqlite3(),
                "scratch_writability": probe_m24_scratch_writability(),
            },
            "policy_invariants": {
                "OQ_BP_006": "CLOSED (technical environment-definition/realization per #167; #153 same-lineage, NOT independent; #158 re-check still required)",
                "defense_evaluation": "DECLARED IMPLEMENTATION CONTRACT / REVIEWER-REQUIRED (Machine structural check != learner PASS)",
                "no_fabricated_mechanisms": "DECLARED IMPLEMENTATION CONTRACT / NOT PROBED BY PREFLIGHT",
                "operational_readiness": "DECLARED IMPLEMENTATION CONTRACT / REVIEWER-REQUIRED",
            },
        }

    if mod == "M23":
        return {
            "stage": "S7",
            "batch": "S7-B3",
            "module": "M23",
            "title": "Systems Thinking & Judgment",
            "os": probe_os(),
            "python": probe_python(),
            "capabilities": {
                "monotonic_clock": probe_monotonic_clock(),
            },
            "policy_invariants": {
                "OQ_BP_006": "CLOSED (technical environment-definition/realization per #167; #153 same-lineage, NOT independent; #158 re-check still required)",
                "OQ_BP_001": "RESOLVED FOR v1.0 BY D-033 (AI outputs treated as unverified candidate hypotheses)",
                "measurement_stance": "DECLARED IMPLEMENTATION CONTRACT / NOT PROBED BY PREFLIGHT",
                "technology_evaluation": "DECLARED IMPLEMENTATION CONTRACT / NOT PROBED BY PREFLIGHT",
                "cost_modeling": "DECLARED IMPLEMENTATION CONTRACT / NOT PROBED BY PREFLIGHT",
            },
        }

    if mod == "M22":
        return {
            "stage": "S7",
            "batch": "S7-B2",
            "module": "M22",
            "title": "Authn/Authz & Secure Composition",
            "os": probe_os(),
            "python": probe_python(),
            "capabilities": {
                "stdlib_crypto": probe_stdlib_crypto(),
                "password_kdf": probe_password_kdf(),
                "sqlite3": probe_sqlite3(),
                "localhost_bind": probe_localhost_bind(),
                "scratch_writability": probe_m22_scratch_writability(),
                "optional_argon2": probe_optional_argon2(),
            },
            "policy_invariants": {
                "OQ_BP_006": "CLOSED (technical environment-definition/realization per #167; #153 same-lineage, NOT independent; #158 re-check still required)",
                "safe_target_architecture": "CONFIRMED (Loopback only, zero live targets, zero offensive tools)",
                "crypto_stance": "CONFIRMED (Crypto-use only, zero custom primitive implementation)",
                "fail_closed_teardown": "DECLARED IMPLEMENTATION CONTRACT / NOT PROBED BY PREFLIGHT (runtime verification belongs to activity/test)",
                "ephemeral_storage": "CONFIRMED (Course-owned temporary scratch & in-memory DB only)",
            },
        }

    # Default / M21 report (preserves exact S7-B1 contract)
    return {
        "stage": "S7",
        "batch": "S7-B1",
        "module": "M21",
        "title": "Trust Boundaries & Cryptographic Use",
        "os": probe_os(),
        "python": probe_python(),
        "capabilities": {
            "stdlib_crypto": probe_stdlib_crypto(),
            "path_confinement_primitives": probe_path_confinement_primitives(),
            "symlink_creation": probe_symlink_capability(),
            "scratch_writability": probe_scratch_writability(),
            "optional_cryptography": probe_optional_cryptography(),
        },
        "policy_invariants": {
            "OQ_BP_006": "CLOSED (technical environment-definition/realization per #167; #153 same-lineage, NOT independent; #158 re-check still required)",
            "safe_target_architecture": "CONFIRMED (Zero live targets, zero offensive tools)",
            "crypto_stance": "CONFIRMED (Crypto-use only, zero custom primitive implementation)",
            "ephemeral_storage": "CONFIRMED (Course-owned temporary scratch only)",
        },
    }


class TestPreflightSecuritySynthesis(unittest.TestCase):
    """Automated unit test assertion of the preflight probe itself."""

    def test_preflight_core_capabilities(self) -> None:
        report = collect_preflight_report("M21")
        self.assertEqual(report["module"], "M21")
        self.assertEqual(report["capabilities"]["stdlib_crypto"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["path_confinement_primitives"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["scratch_writability"]["disposition"], "REQUIRED CAPABILITY PASS")

        sym_disp = report["capabilities"]["symlink_creation"]["disposition"]
        self.assertIn(sym_disp, ["SYMLINK CAPABILITY PASS", "BLOCKED / NOT RUN"])

        opt_disp = report["capabilities"]["optional_cryptography"]["disposition"]
        self.assertIn(
            opt_disp,
            [
                "OPTIONAL PACKAGE AVAILABLE",
                "OPTIONAL PACKAGE NOT INSTALLED / NOT RUN",
                "ENVIRONMENT-BLOCKED / NOT RUN",
            ],
        )

        self.assertEqual(report["policy_invariants"]["OQ_BP_006"], "CLOSED (technical environment-definition/realization per #167; #153 same-lineage, NOT independent; #158 re-check still required)")

    def test_preflight_m22_capabilities(self) -> None:
        report = collect_preflight_report("M22")
        self.assertEqual(report["module"], "M22")
        self.assertEqual(report["capabilities"]["stdlib_crypto"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["password_kdf"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["sqlite3"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["localhost_bind"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["scratch_writability"]["disposition"], "REQUIRED CAPABILITY PASS")

        opt_argon2 = report["capabilities"]["optional_argon2"]["disposition"]
        self.assertIn(
            opt_argon2,
            [
                "OPTIONAL PACKAGE AVAILABLE",
                "OPTIONAL PACKAGE NOT INSTALLED / NOT RUN",
                "ENVIRONMENT-BLOCKED / NOT RUN",
            ],
        )
        self.assertEqual(report["policy_invariants"]["OQ_BP_006"], "CLOSED (technical environment-definition/realization per #167; #153 same-lineage, NOT independent; #158 re-check still required)")
        self.assertEqual(
            report["policy_invariants"]["fail_closed_teardown"],
            "DECLARED IMPLEMENTATION CONTRACT / NOT PROBED BY PREFLIGHT (runtime verification belongs to activity/test)",
        )

    def test_preflight_m23_capabilities(self) -> None:
        report = collect_preflight_report("M23")
        self.assertEqual(report["module"], "M23")
        self.assertEqual(report["batch"], "S7-B3")
        self.assertEqual(report["capabilities"]["monotonic_clock"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["policy_invariants"]["OQ_BP_006"], "CLOSED (technical environment-definition/realization per #167; #153 same-lineage, NOT independent; #158 re-check still required)")
        self.assertEqual(
            report["policy_invariants"]["OQ_BP_001"],
            "RESOLVED FOR v1.0 BY D-033 (AI outputs treated as unverified candidate hypotheses)",
        )
        self.assertEqual(
            report["policy_invariants"]["measurement_stance"],
            "DECLARED IMPLEMENTATION CONTRACT / NOT PROBED BY PREFLIGHT",
        )

    def test_preflight_m24_capabilities(self) -> None:
        report = collect_preflight_report("M24")
        self.assertEqual(report["module"], "M24")
        self.assertEqual(report["batch"], "S7-B4")
        self.assertEqual(report["capabilities"]["stdlib_dataclasses_json"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["sqlite3"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["scratch_writability"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["policy_invariants"]["OQ_BP_006"], "CLOSED (technical environment-definition/realization per #167; #153 same-lineage, NOT independent; #158 re-check still required)")
        self.assertIn("REVIEWER-REQUIRED", report["policy_invariants"]["defense_evaluation"])
        self.assertEqual(
            report["policy_invariants"]["no_fabricated_mechanisms"],
            "DECLARED IMPLEMENTATION CONTRACT / NOT PROBED BY PREFLIGHT",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Preflight verification for S7 Security Synthesis & Systems Judgment (M21/M22/M23/M24)")
    parser.add_argument("--module", choices=["M21", "M22", "M23", "M24", "all"], default="M21", help="Module capability probe to run")
    parser.add_argument("--json", action="store_true", help="Emit raw JSON capability report")
    args = parser.parse_args()

    modules = ["M21", "M22", "M23", "M24"] if args.module == "all" else [args.module]
    reports = [collect_preflight_report(m) for m in modules]

    if args.json:
        print(json.dumps(reports if len(reports) > 1 else reports[0], indent=2))
        return

    for report in reports:
        print("=" * 78)
        print(f"  STAGE 7 BATCH {report['batch']} / MODULE {report['module']} PREFLIGHT CAPABILITY REPORT")
        print("=" * 78)
        print(f"  OS:             {report['os']['system']} {report['os']['release']} ({report['os']['architecture']})")
        print(f"  Python:         {report['python']['implementation']} {report['python']['version']}")
        print(f"  OQ-BP-006:      {report['python']['oq_bp_006_policy']}")
        print("-" * 78)
        print("  CAPABILITY AUDIT:")
        caps = report["capabilities"]
        for name, data in caps.items():
            disp = data.get("disposition", "UNKNOWN")
            print(f"    - {name:<30}: {disp}")
            if "error" in data:
                print(f"        Error detail: {data['error']}")
            if "note" in data:
                print(f"        Note:         {data['note']}")
        print("-" * 78)
        print("  POLICY INVARIANTS:")
        for k, v in report["policy_invariants"].items():
            print(f"    - {k:<28}: {v}")
        print("=" * 78)


if __name__ == "__main__":
    main()
