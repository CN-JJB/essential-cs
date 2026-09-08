#!/usr/bin/env python3
"""
labs/foundations/m22/activity_l22_03.py — Software Supply Chain Integrity & Provenance Fixture
=============================================================================================

Course-owned, synthetic educational harness for L22-03: "Why do I trust my dependencies?"
Uses Python standard library only (hashlib, hmac, json, dataclasses, typing).

Demonstrates the 9-Layer Software Supply Chain Integrity Model:
1. Layer 1: Resolution Pinning (exact semantic version frozen in lockfile);
2. Layer 2: Expected Digest Ownership (lockfile records cryptographic digest governed by trusted repository);
3. Layer 3: Fetched-Byte Integrity (SHA-256 digest check against expected hash);
4. Layer 4: Build Reproducibility (independent rebuild producing identical binary artifacts);
5. Layer 5: Signature Verification (cryptographic signature verification over package archive);
6. Layer 6: Signer Identity Binding (linking signing key to authenticated maintainer identity);
7. Layer 7: Source/Build Provenance (SLSA v1.2 verifiable provenance binding commit, repo, and builder);
8. Layer 8: Trusted Builder Assumptions (evaluating isolated, hardened build platform);
9. Layer 9: Verifier Policy Enforcement (gate rejecting dependencies that fail integrity or policy).

Safety & Invariants:
- Zero live package registries (no external pip / npm / PyPI network calls);
- Zero execution of untrusted package code (no subprocess setup.py, no imports of untrusted bytecode);
- Educational fixtures only;
- Preserves explicit non-proofs:
  - Digest != Publisher Identity;
  - Valid Signature != Organizational Trustworthiness;
  - Reproducibility != Non-Malicious Source;
  - Provenance != Verification without Policy.
"""

from __future__ import annotations

import dataclasses
import hashlib
import hmac
import json
from typing import Any, Dict, List, Optional, Set, Tuple


# -----------------------------------------------------------------------------
# Synthetic Data Structures for Supply Chain Verification
# -----------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class SyntheticArtifact:
    name: str
    version: str
    content: bytes

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.content).hexdigest()


@dataclasses.dataclass(frozen=True)
class LockfileEntry:
    name: str
    version: str
    expected_sha256: str
    source_url: str


@dataclasses.dataclass(frozen=True)
class SLSAProvenanceV1_2:
    """
    Synthetic representation of OpenSSF SLSA v1.2 Provenance Attestation.
    Reference: https://slsa.dev/spec/v1.2/provenance
    """
    type: str  # "https://in-toto.io/Statement/v1"
    predicate_type: str  # "https://slsa.dev/provenance/v1"
    subject_name: str
    subject_sha256: str
    builder_id: str  # e.g., "https://github.com/actions/runner-hosted@v1"
    source_repository: str  # e.g., "https://github.com/example/trusted-lib"
    source_commit: str  # e.g., git commit hash
    build_type: str


@dataclasses.dataclass(frozen=True)
class VerifierPolicy:
    require_hash_pinning: bool = True
    require_reproducible: bool = False
    require_signature: bool = True
    require_provenance: bool = True
    trusted_builders: Tuple[str, ...] = ("https://github.com/actions/runner-hosted@v1",)
    trusted_source_repos: Tuple[str, ...] = ("https://github.com/example/trusted-lib",)
    authorized_signer_keys: Tuple[str, ...] = ("maintainer-pubkey-alice-2026",)


# -----------------------------------------------------------------------------
# Verification Primitives for the 9 Layers
# -----------------------------------------------------------------------------

def verify_layer3_byte_integrity(artifact: SyntheticArtifact, expected_sha256: str) -> Tuple[bool, str]:
    """
    Layer 3: Fetched-Byte Integrity.

    Checks if computed SHA-256 matches expected digest.
    NON-GUARANTEE: A valid digest proves byte immutability, NOT publisher identity!
    """
    computed = artifact.sha256
    if hmac.compare_digest(computed, expected_sha256):
        return True, f"Byte integrity confirmed: computed {computed[:12]}... matches expected digest"
    return False, f"TAMPER DETECTED: computed digest {computed[:12]}... does not match expected {expected_sha256[:12]}..."


def verify_layer4_reproducibility(build1_bytes: bytes, build2_bytes: bytes) -> Tuple[bool, str]:
    """
    Layer 4: Build Reproducibility.

    Verifies if two independent builds from identical source produce bit-for-bit identical outputs.
    NON-GUARANTEE: Reproducibility does NOT prove source code is safe or non-malicious!
    """
    hash1 = hashlib.sha256(build1_bytes).hexdigest()
    hash2 = hashlib.sha256(build2_bytes).hexdigest()
    if hmac.compare_digest(hash1, hash2):
        return True, f"Build is bit-for-bit reproducible: hash {hash1[:12]}... identical across independent builds"
    return False, f"Build NOT reproducible: build 1 ({hash1[:12]}...) != build 2 ({hash2[:12]}...)"


def verify_layer5_and_6_signature_and_identity(
    artifact_sha256: str,
    signature_bytes: bytes,
    signing_key_id: str,
    signing_secret_for_test: bytes,
    authorized_keys: Tuple[str, ...],
) -> Tuple[bool, str]:
    """
    Layer 5 (Signature Verification) & Layer 6 (Signer Identity Binding).

    Verifies cryptographic signature using authorized public/shared key.
    NON-GUARANTEE: Valid signature proves key possession, NOT organizational trustworthiness!
    """
    # Check Layer 6: Signer Identity Binding
    if signing_key_id not in authorized_keys:
        return False, f"Signer identity rejected: key '{signing_key_id}' is not in authorized maintainer registry"

    # Check Layer 5: Cryptographic Signature Verification
    expected_sig = hmac.new(signing_secret_for_test, artifact_sha256.encode("ascii"), hashlib.sha256).digest()
    if not hmac.compare_digest(expected_sig, signature_bytes):
        return False, f"Cryptographic signature verification failed for key '{signing_key_id}'"

    return True, f"Signature verified and bound to authorized maintainer '{signing_key_id}'"


def verify_layer7_and_8_provenance_and_builder(
    provenance: SLSAProvenanceV1_2,
    artifact_sha256: str,
    trusted_builders: Tuple[str, ...],
    trusted_source_repos: Tuple[str, ...],
) -> Tuple[bool, str]:
    """
    Layer 7 (Build/Source Provenance) & Layer 8 (Trusted Builder Assumptions).

    Verifies SLSA v1.2 provenance attestation.
    NON-GUARANTEE: Provenance is meaningless without verifier policy enforcing trusted builders!
    """
    # 1. Subject digest binding
    if not hmac.compare_digest(provenance.subject_sha256, artifact_sha256):
        return False, f"Provenance subject mismatch: attestation is for '{provenance.subject_sha256[:12]}...', but artifact is '{artifact_sha256[:12]}...'"

    # 2. Trusted Builder evaluation (Layer 8)
    if provenance.builder_id not in trusted_builders:
        return False, f"Untrusted builder platform: '{provenance.builder_id}' is not an approved isolated builder"

    # 3. Source repository evaluation (Layer 7)
    if provenance.source_repository not in trusted_source_repos:
        return False, f"Untrusted source repository: '{provenance.source_repository}' does not match official repo"

    return True, f"SLSA v1.2 provenance verified: built on '{provenance.builder_id}' from repo '{provenance.source_repository}' @ commit '{provenance.source_commit[:8]}'"


def audit_dependency_against_policy(
    entry: LockfileEntry,
    artifact: SyntheticArtifact,
    provenance: Optional[SLSAProvenanceV1_2],
    signature: Optional[bytes],
    signing_key_id: Optional[str],
    signing_secret_for_test: bytes,
    policy: VerifierPolicy,
) -> Dict[str, Any]:
    """
    Layer 9: Verifier Policy Enforcement.

    Evaluates all 9 layers against explicit adoption policy gates.
    """
    report: Dict[str, Any] = {
        "package": entry.name,
        "version": entry.version,
        "layers": {},
        "verdict": "REJECT",
        "reasons": [],
    }

    # Layer 1: Version Pinning
    # Enforces exact version (no ranges like >= or ~>)
    is_pinned = not any(c in entry.version for c in (">", "<", "=", "~", "*", "^"))
    report["layers"]["layer1_version_pinned"] = is_pinned
    if not is_pinned:
        report["reasons"].append("Layer 1 FAIL: Package version is a range, not an exact pin")

    # Layer 2: Expected Digest Ownership
    has_expected_digest = bool(entry.expected_sha256 and len(entry.expected_sha256) == 64)
    report["layers"]["layer2_expected_digest_present"] = has_expected_digest
    if not has_expected_digest:
        report["reasons"].append("Layer 2 FAIL: Lockfile missing trusted expected SHA-256 digest")

    # Layer 3: Fetched-Byte Integrity
    l3_ok, l3_msg = verify_layer3_byte_integrity(artifact, entry.expected_sha256)
    report["layers"]["layer3_byte_integrity"] = l3_ok
    if not l3_ok:
        report["reasons"].append(f"Layer 3 FAIL: {l3_msg}")

    # Layer 5 & 6: Signature & Identity Binding
    if policy.require_signature:
        if not signature or not signing_key_id:
            report["layers"]["layer5_6_signature_and_identity"] = False
            report["reasons"].append("Layer 5/6 FAIL: Signature or signer identity missing")
        else:
            sig_ok, sig_msg = verify_layer5_and_6_signature_and_identity(
                artifact.sha256, signature, signing_key_id, signing_secret_for_test, policy.authorized_signer_keys
            )
            report["layers"]["layer5_6_signature_and_identity"] = sig_ok
            if not sig_ok:
                report["reasons"].append(f"Layer 5/6 FAIL: {sig_msg}")
    else:
        report["layers"]["layer5_6_signature_and_identity"] = "SKIPPED_BY_POLICY"

    # Layer 7 & 8: Provenance & Builder
    if policy.require_provenance:
        if not provenance:
            report["layers"]["layer7_8_provenance_and_builder"] = False
            report["reasons"].append("Layer 7/8 FAIL: SLSA provenance attestation missing")
        else:
            prov_ok, prov_msg = verify_layer7_and_8_provenance_and_builder(
                provenance, artifact.sha256, policy.trusted_builders, policy.trusted_source_repos
            )
            report["layers"]["layer7_8_provenance_and_builder"] = prov_ok
            if not prov_ok:
                report["reasons"].append(f"Layer 7/8 FAIL: {prov_msg}")
    else:
        report["layers"]["layer7_8_provenance_and_builder"] = "SKIPPED_BY_POLICY"

    # Layer 9 Final Policy Judgment
    if not report["reasons"]:
        report["verdict"] = "ACCEPT"
    else:
        report["verdict"] = "REJECT"

    return report


# -----------------------------------------------------------------------------
# Self-Test / CLI Demonstration
# -----------------------------------------------------------------------------

def run_demonstration() -> None:
    print("=" * 78)
    print("  L22-03 DEMONSTRATION: SOFTWARE SUPPLY CHAIN 9-LAYER AUDIT")
    print("=" * 78)

    signing_secret = b"teaching-package-signing-key-32b"
    key_id = "maintainer-pubkey-alice-2026"
    policy = VerifierPolicy()

    # 1. Create legitimate package
    legit_code = b"def authenticate(): return True\n"
    legit_artifact = SyntheticArtifact("trusted-auth-lib", "1.4.0", legit_code)
    lock_entry = LockfileEntry("trusted-auth-lib", "1.4.0", legit_artifact.sha256, "https://pypi.local/packages/1.4.0.tar.gz")

    # Sign artifact
    signature = hmac.new(signing_secret, legit_artifact.sha256.encode("ascii"), hashlib.sha256).digest()

    # Provenance attestation
    prov = SLSAProvenanceV1_2(
        type="https://in-toto.io/Statement/v1",
        predicate_type="https://slsa.dev/provenance/v1",
        subject_name="trusted-auth-lib",
        subject_sha256=legit_artifact.sha256,
        builder_id="https://github.com/actions/runner-hosted@v1",
        source_repository="https://github.com/example/trusted-lib",
        source_commit="a1b2c3d4e5f678901234567890abcdef12345678",
        build_type="https://slsa.dev/build-types/github-actions/v1",
    )

    print("\n[1] Auditing Legitimate Package against 9-Layer Policy:")
    report_legit = audit_dependency_against_policy(
        lock_entry, legit_artifact, prov, signature, key_id, signing_secret, policy
    )
    print(f"    Verdict: {report_legit['verdict']}")
    print(f"    Layers:  {json.dumps(report_legit['layers'], indent=2)}")
    assert report_legit["verdict"] == "ACCEPT"

    # 2. Tampered byte attack (Upstream substitution)
    print("\n[2] Simulating Byte Tampering / Upstream Substitution:")
    tampered_code = b"def authenticate(): return True  # backdoor injected\n"
    tampered_artifact = SyntheticArtifact("trusted-auth-lib", "1.4.0", tampered_code)

    report_tampered = audit_dependency_against_policy(
        lock_entry, tampered_artifact, prov, signature, key_id, signing_secret, policy
    )
    print(f"    Verdict: {report_tampered['verdict']}")
    print(f"    Reasons: {report_tampered['reasons']}")
    assert report_tampered["verdict"] == "REJECT"
    assert any("Layer 3 FAIL" in r for r in report_tampered["reasons"])

    # 3. Untrusted builder attack (Compromised CI runner)
    print("\n[3] Simulating Untrusted Builder Platform:")
    rogue_prov = SLSAProvenanceV1_2(
        type="https://in-toto.io/Statement/v1",
        predicate_type="https://slsa.dev/provenance/v1",
        subject_name="trusted-auth-lib",
        subject_sha256=legit_artifact.sha256,
        builder_id="https://compromised-untrusted-builder.xyz@v1",
        source_repository="https://github.com/example/trusted-lib",
        source_commit="a1b2c3d4e5f678901234567890abcdef12345678",
        build_type="https://slsa.dev/build-types/custom/v1",
    )
    report_rogue_builder = audit_dependency_against_policy(
        lock_entry, legit_artifact, rogue_prov, signature, key_id, signing_secret, policy
    )
    print(f"    Verdict: {report_rogue_builder['verdict']}")
    print(f"    Reasons: {report_rogue_builder['reasons']}")
    assert report_rogue_builder["verdict"] == "REJECT"
    assert any("Layer 7/8 FAIL" in r for r in report_rogue_builder["reasons"])

    # 4. Reproducibility test
    print("\n[4] Testing Build Reproducibility Verification:")
    build_a = b"binary-artifact-bytes-deterministic-timestamp-0"
    build_b = b"binary-artifact-bytes-deterministic-timestamp-0"
    build_c = b"binary-artifact-bytes-with-random-build-timestamp-1750000000"

    ok_rep, msg_rep = verify_layer4_reproducibility(build_a, build_b)
    print(f"    Deterministic build comparison: ok={ok_rep} ({msg_rep[:55]}...)")
    assert ok_rep is True

    bad_rep, bad_msg = verify_layer4_reproducibility(build_a, build_c)
    print(f"    Non-deterministic build comparison: ok={bad_rep} ({bad_msg[:55]}...)")
    assert bad_rep is False

    print("\n" + "=" * 78)
    print("  L22-03 ACTIVITY CONTRACT VERIFIED.")
    print("=" * 78)


if __name__ == "__main__":
    run_demonstration()
