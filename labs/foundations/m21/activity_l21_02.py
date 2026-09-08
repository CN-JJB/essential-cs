#!/usr/bin/env python3
"""
activity_l21_02.py — Cryptographic Primitive Roles & Misuse Boundaries (L21-02)
===============================================================================

Deterministic hands-on exercise exploring cryptographic primitive roles:
1. Hash (unkeyed integrity detection against a trusted expected digest)
2. MAC (keyed integrity + authenticity under a shared secret)
3. Digital Signature (verification under a specific public key)
4. AEAD (authenticated encryption; confidentiality + authenticity)
5. Key Agreement vs. Peer Authentication
6. Password Verifier distinction (owned by M22/L22-01)

Required Core uses strictly standard library modules: hashlib, hmac, secrets.
No custom cryptographic algorithms are implemented.
No real secrets, private keys, or certificates are used.
Does NOT benchmark software timing to claim physical constant-time proof.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from crypto_roles import (
    SYNTHETIC_MESSAGE,
    SYNTHETIC_TAMPERED,
    compare_digest_contract_probe,
    compute_hmac,
    compute_unkeyed_hash,
    demonstrate_hmac_tamper,
    demonstrate_unkeyed_hash_tamper,
    new_synthetic_mac_key,
    optional_signature_demo,
    primitive_selection_matrix,
    verify_hmac,
    verify_unkeyed_tamper,
)

M21_DIR = Path(__file__).resolve().parent
SCRATCH_DIR = M21_DIR / ".scratch"


def print_banner() -> None:
    print("=" * 78)
    print("  ESSENTIAL CS — FOUNDATIONS M21: TRUST BOUNDARIES & CRYPTO USE")
    print("  L21-02: What Do I Use Crypto For? (Primitive Roles & Misuse Boundaries)")
    print("=" * 78)
    print()


def run_activity(verbose: bool = True) -> Dict[str, Any]:
    if verbose:
        print_banner()

    # Step 1 & 2: Unkeyed Hash vs Active Adversary
    hash_demo = demonstrate_unkeyed_hash_tamper(SYNTHETIC_MESSAGE, SYNTHETIC_TAMPERED)
    if verbose:
        print("[STEP 1 & 2] Unkeyed Hash (SHA-256) vs. Active In-Path Adversary:")
        print(f"  Original Message:  {SYNTHETIC_MESSAGE.decode('ascii')}")
        print(f"  Original Digest:   {hash_demo['original_digest_sha256']}")
        print(f"  Tampered Message:  {SYNTHETIC_TAMPERED.decode('ascii')}")
        print(f"  Recomputed Digest: {hash_demo['tampered_recomputed_digest_sha256']}")
        print()
        print("  Verification Checks:")
        print(f"    - Original message against original digest:    {hash_demo['verify_original_against_original_digest']} (Integrity holds)")
        print(f"    - Tampered message against original digest:    {hash_demo['verify_tampered_against_original_digest']} (Corruption detected)")
        print(f"    - Tampered message against RECOMPUTED digest: {hash_demo['verify_tampered_against_recomputed_digest']} (PASSES! Vulnerable!)")
        print()
        print(f"  Pedagogical Inference:\n    {hash_demo['inference']}")
        print()

    # Step 3 & 4: Keyed MAC (HMAC-SHA-256)
    mac_key = new_synthetic_mac_key()
    hmac_demo = demonstrate_hmac_tamper(mac_key, SYNTHETIC_MESSAGE, SYNTHETIC_TAMPERED)
    if verbose:
        print("[STEP 3 & 4] Keyed Message Authentication Code (HMAC-SHA-256):")
        print(f"  Shared Secret Key: [32 bytes CSPRNG token generated via secrets.token_bytes]")
        print(f"  Generated Tag:     {hmac_demo['mac_hex']}")
        print()
        print("  Verification Checks:")
        print(f"    - Original message + original tag: {hmac_demo['verify_original']} (Authenticity verified)")
        print(f"    - Tampered message + original tag: {hmac_demo['verify_modified_message']} (FORGERY DETECTED)")
        print(f"    - Original message + forged tag:   {hmac_demo['verify_modified_tag']} (FORGERY DETECTED)")
        print()
        print(f"  Pedagogical Inference:\n    {hmac_demo['inference']}")
        print()

    # Step 5: hmac.compare_digest API Contract
    probe = compare_digest_contract_probe()
    if verbose:
        print("[STEP 5] Timing Attack Mitigation via hmac.compare_digest:")
        print(f"  API:                           {probe['api']}")
        print(f"  Matching Strings Equal:        {probe['same_ascii_hex_equal']}")
        print(f"  Different Strings Equal:       {probe['different_ascii_hex_equal']}")
        print(f"  Type Mismatch Exception:       {probe['mixed_str_bytes_error']}")
        print(f"  Physical Constant-Time Claim:  {probe['physical_constant_time_claimed']}")
        print()
        print("  API Contract Distinction:")
        print(f"    {probe['contract']}")
        print()

    # Step 6: Primitive Selection Matrix
    matrix = primitive_selection_matrix()
    if verbose:
        print("[STEP 6] Cryptographic Primitive Selection Matrix:")
        print("-" * 78)
        for idx, row in enumerate(matrix, 1):
            print(f"  Row {idx}: Scenario: {row['scenario']}")
            print(f"    - Required Property:   {row['required_property']}")
            print(f"    - Chosen Primitive:    {row['chosen_primitive']}")
            print(f"    - Incorrect Trap:      {row['incorrect_tempting_primitive']}")
            print(f"    - Major Non-Guarantee: {row['non_guarantee']}")
            print()
        print("-" * 78)
        print()

    # Step 7: Optional Asymmetric Signature Probe (PyCA cryptography)
    sig_demo = optional_signature_demo(SYNTHETIC_MESSAGE)
    if verbose:
        print("[STEP 7] Optional Learn-New-Tech Path (PyCA cryptography / Ed25519):")
        print(f"  Disposition:    {sig_demo['disposition']}")
        if sig_demo.get("version"):
            print(f"  Package:        {sig_demo['package']} v{sig_demo['version']}")
            print(f"  Algorithm:      {sig_demo['algorithm']}")
            print(f"  Matching Key:   {sig_demo['verified_under_matching_public_key']}")
            print(f"  Unrelated Key:  {sig_demo['verified_under_unrelated_public_key']}")
        print(f"  Inference Note: {sig_demo['inference_limit']}")
        print()

    observation_data: Dict[str, Any] = {
        "module": "M21",
        "lesson": "L21-02",
        "hash_tamper_demonstration": hash_demo,
        "hmac_tamper_demonstration": hmac_demo,
        "compare_digest_probe": probe,
        "primitive_selection_matrix": matrix,
        "optional_signature_demonstration": sig_demo,
        "core_invariants": [
            "Hash != Authenticity against active adversary.",
            "MAC != Digital Signature (shared secret vs public verification).",
            "Signature verification != Signer identity (requires key custody & binding).",
            "Signature != Unconditional non-repudiation.",
            "Encryption != Authenticity (AEAD required).",
            "Key Agreement != Peer Authentication.",
            "compare_digest API contract != Physical constant-time proof.",
            "Fast hashes (SHA-256) fail as password verifiers (owned by M22).",
        ],
    }

    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    obs_file = SCRATCH_DIR / "l21_02_observation.json"
    obs_file.write_text(json.dumps(observation_data, indent=2), encoding="utf-8")

    if verbose:
        print(f"[STATUS] Observation written to {obs_file}")
        print("[STATUS] L21-02 Activity Completed Successfully.")

    return observation_data


if __name__ == "__main__":
    try:
        run_activity(verbose=True)
        sys.exit(0)
    except Exception as exc:
        print(f"[FATAL ERROR] Activity failed: {exc}", file=sys.stderr)
        sys.exit(1)
