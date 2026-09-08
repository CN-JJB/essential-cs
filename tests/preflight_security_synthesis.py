#!/usr/bin/env python3
"""
preflight_security_synthesis.py — Preflight Verification Script for S7 / M21
=============================================================================

Evaluates and records host capabilities empirically for Stage 7 (Security Synthesis
& Systems Judgment), specifically Module M21 (Trust Boundaries & Crypto Use),
without permanently pinning OQ-BP-006.

Probes the required capabilities actually used:
1. OS / platform / architecture
2. Python implementation / version
3. Standard library crypto modules (hashlib.sha256, hmac.new, hmac.compare_digest, secrets)
4. Temporary directory creation & path resolution (tempfile, Path.resolve, os.path.commonpath)
5. Host filesystem symlink capability (truthfully records PASS or BLOCKED / NOT RUN)
6. Course-owned scratch writability (labs/foundations/m21/.scratch)
7. Optional candidate PyCA cryptography package (truthful capability gating)

OQ-BP-006 remains OPEN.
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
import unittest
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parent.parent
M21_DIR = REPO_ROOT / "labs" / "foundations" / "m21"


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
        "oq_bp_006_policy": "OPEN / UNRESOLVED (capability-based evaluation; no course-wide pin)",
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
    """
    Empirically probes whether the host OS and user environment permit symlink creation.
    On Windows without Developer Mode or non-admin privilege, os.symlink raises OSError.
    This is truthfully reported and never faked as PASS.
    """
    try:
        with tempfile.TemporaryDirectory(prefix="ecs-symlink-probe-") as tmpdir:
            tmp = Path(tmpdir)
            target = tmp / "target.txt"
            target.write_text("target", encoding="utf-8")
            link = tmp / "link.txt"
            os.symlink(os.fspath(target), os.fspath(link))
            # Verify reading link
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


def collect_preflight_report() -> Dict[str, Any]:
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
            "OQ_BP_006": "OPEN / UNRESOLVED",
            "safe_target_architecture": "CONFIRMED (Zero live targets, zero offensive tools)",
            "crypto_stance": "CONFIRMED (Crypto-use only, zero custom primitive implementation)",
            "ephemeral_storage": "CONFIRMED (Course-owned temporary scratch only)",
        },
    }


class TestPreflightSecuritySynthesis(unittest.TestCase):
    """Automated unit test assertion of the preflight probe itself."""

    def test_preflight_core_capabilities(self) -> None:
        report = collect_preflight_report()
        self.assertEqual(report["module"], "M21")
        # Required core capabilities must pass in standard python 3 environment
        self.assertEqual(report["capabilities"]["stdlib_crypto"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["path_confinement_primitives"]["disposition"], "REQUIRED CAPABILITY PASS")
        self.assertEqual(report["capabilities"]["scratch_writability"]["disposition"], "REQUIRED CAPABILITY PASS")

        # Symlink capability may be PASS or BLOCKED / NOT RUN, but must be truthful
        sym_disp = report["capabilities"]["symlink_creation"]["disposition"]
        self.assertIn(sym_disp, ["SYMLINK CAPABILITY PASS", "BLOCKED / NOT RUN"])

        # Optional package is either AVAILABLE or NOT INSTALLED / NOT RUN
        opt_disp = report["capabilities"]["optional_cryptography"]["disposition"]
        self.assertIn(opt_disp, ["OPTIONAL PACKAGE AVAILABLE", "OPTIONAL PACKAGE NOT INSTALLED / NOT RUN"])

        # Policy invariants
        self.assertEqual(report["policy_invariants"]["OQ_BP_006"], "OPEN / UNRESOLVED")


def main() -> None:
    parser = argparse.ArgumentParser(description="Preflight verification for S7 M21 Trust & Crypto Use")
    parser.add_argument("--json", action="store_true", help="Emit raw JSON capability report")
    args = parser.parse_args()

    report = collect_preflight_report()

    if args.json:
        print(json.dumps(report, indent=2))
        return

    print("=" * 78)
    print("  STAGE 7 BATCH S7-B1 / MODULE M21 PREFLIGHT CAPABILITY REPORT")
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
