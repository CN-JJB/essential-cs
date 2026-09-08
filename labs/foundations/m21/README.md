# M21 Foundations Activities: Trust Boundaries & Cryptographic Use

This directory contains executable, course-owned fixtures and worked activities for Module M21 (Stage 7, Batch S7-B1).

## Core Boundary Rules & Invariants

- **Standard Library First**: Built strictly on Python standard library modules (`hashlib`, `hmac`, `secrets`, `tempfile`, `os`, `pathlib`).
- **Crypto-Use Only (Zero Primitive Implementation)**: Learners do not implement cryptographic primitives (no custom AES, RSA, SHA-256, or HMAC). All crypto is used as opaque building blocks via standard vetted APIs.
- **Safe-Target Architecture**: Strictly zero offensive tooling, automated vulnerability scanners, exploit payloads, weaponized attack chains, or public/remote targets.
- **Synthetic Disposable Storage**: All filesystem boundary exercises run inside ephemeral `tempfile.TemporaryDirectory` trees owned by the process. Zero host-sensitive paths (e.g. `/etc`, `C:\Windows`) are accessed.
- **Syntactic Check Inadequacy**: Rejecting `"../"` is proven insufficient against symlink escape or absolute path injection.
- **Prefix startswith Inadequacy**: `str.startswith(base)` is proven flawed due to sibling-prefix confusion (`store` vs `store-evil`). Confinement must be proven via resolved path ancestry (`os.path.commonpath`).
- **TOCTOU Inference Limit**: A path resolution check before a subsequent `open()` does not eliminate time-of-check to time-of-use races on shared filesystems.
- **Authentication != Validated Input**: Authenticating the identity of a client does not make client-supplied path strings trustworthy.
- **Hash != Authenticity**: An unkeyed cryptographic hash provides integrity detection only against a trusted expected digest. An active in-path modifier can replace both message and unkeyed digest.
- **MAC != Digital Signature**: A MAC (HMAC) provides integrity and authenticity under a shared symmetric secret, but cannot prove which key holder created the tag and cannot be verified by untrusted third parties without sharing the secret.
- **Signature Verification != Signer Identity**: Mathematical verification under a public key proves key possession at signing time; binding to a human/organization requires key custody and verifier trust policy.
- **Signature != Unconditional Non-Repudiation**: Non-repudiation is a system/legal property, not an intrinsic mathematical guarantee of a primitive.
- **Encryption != Authenticity**: Confidentiality (encryption) without authenticity is malleable. Network protocols require AEAD (e.g. AES-GCM) or Encrypt-then-MAC.
- **Key Agreement != Peer Authentication**: Diffie-Hellman establishes shared secret traffic keys but does not authenticate endpoint identity on its own.
- **compare_digest API Contract**: `hmac.compare_digest` is used per language documentation to mitigate content-based short-circuiting timing attacks; it does not claim physical constant-time hardware execution.
- **Zero Real Secrets**: All keys, nonces, and messages are synthetic in-memory byte strings.
- **Password Hashing Boundary**: Fast hashes (SHA-256) fail as password verifiers. Password verifiers and slow/memory-hard hashing schemas belong to Module M22 (`L22-01`).

---

## Files Overview

1. **`path_confinement.py`**
   - Implements course-owned path resolution and containment helpers for L21-01:
     - `SyntheticTree`: Disposable test filesystem fixture.
     - `naive_string_looks_safe`: Incomplete syntactic check rejecting `..`, absolute paths, and NUL bytes.
     - `prefix_startswith_looks_contained`: Demonstrates the sibling-prefix confusion flaw (`store` vs `store-evil`).
     - `is_resolved_contained`: Resolved path ancestry verification via `os.path.commonpath`.
     - `classify_candidate`: Evaluates candidate inputs against all mechanisms and records decisions.
     - `evaluate_standard_cases`: Evaluates 7 deterministic teaching cases without touching host files.

2. **`crypto_roles.py`**
   - Implements standard-library cryptographic use helpers for L21-02:
     - `compute_unkeyed_hash` & `verify_unkeyed_tamper`: Demonstrates unkeyed SHA-256 integrity check.
     - `demonstrate_unkeyed_hash_tamper`: Proves how an active modifier replaces both message and digest.
     - `compute_hmac` & `verify_hmac`: Keyed MAC verification using `hmac.compare_digest`.
     - `demonstrate_hmac_tamper`: Proves HMAC tamper resistance under a CSPRNG shared secret.
     - `compare_digest_contract_probe`: Tests API behavior and clarifies timing mitigation vs physical proof.
     - `primitive_selection_matrix`: 6-scenario reference table covering Hash, MAC, Signature, AEAD, Key Agreement, and Password Verifier boundaries.
     - `optional_signature_demo`: Capability-gated Ed25519 demonstration via PyCA `cryptography`. Absence reports `NOT RUN / CAPABILITY ABSENT` cleanly.

3. **`activity_l21_01.py`**
   - Interactive / executable CLI activity for Lesson L21-01:
     - Initializes synthetic tree.
     - Evaluates standard path candidates against naive string, prefix startswith, and resolved ancestry checks.
     - Analyzes security failure modes and outputs the Threat Boundary & Authority Map.
     - Writes observation record to `.scratch/l21_01_observation.json`.
     - Ensures disposable tree cleanup.

4. **`activity_l21_02.py`**
   - Interactive / executable CLI activity for Lesson L21-02:
     - Executes 6-step teaching chain from unkeyed hash to HMAC, timing mitigation, and primitive selection matrix.
     - Probes optional PyCA `cryptography` signature capability.
     - Writes observation record to `.scratch/l21_02_observation.json`.

5. **`reset.py`**
   - Fail-closed, idempotent cleanup script removing `.scratch/` and local `__pycache__/`.
   - Verified idempotent across repeated executions.

6. **`test_m21.py`**
   - Standard library `unittest` suite validating all M21 mechanics, invariants, and activity outcomes.

---

## Running the Activities & Tests

```bash
# 1. Run M21 / S7 Preflight capability check
python tests/preflight_security_synthesis.py

# 2. Run Lesson L21-01 hands-on activity (Path confinement & boundary map)
python labs/foundations/m21/activity_l21_01.py

# 3. Run Lesson L21-02 hands-on activity (Crypto primitive roles & misuse boundaries)
python labs/foundations/m21/activity_l21_02.py

# 4. Run standard library test suite
python -m unittest labs/foundations/m21/test_m21.py

# 5. Clean up course-owned scratch artifacts
python labs/foundations/m21/reset.py
```
