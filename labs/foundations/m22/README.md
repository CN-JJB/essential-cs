# M22 Foundations Activities: Authn/Authz & Secure Composition

This directory contains executable, course-owned fixtures and worked activities for Module M22 (Stage 7, Batch S7-B2).

## Core Boundary Rules & Invariants

- **Standard Library First**: Built strictly on Python standard library modules (`hashlib`, `hmac`, `secrets`, `sqlite3`, `http.server`, `urllib`, `socket`, `threading`, `json`, `base64`).
- **Safe-Target Architecture**: Strictly zero offensive tooling, automated vulnerability scanners, exploit payloads, weaponized attack chains, or public/remote targets.
- **Loopback Only (`127.0.0.1`, Ephemeral Port `0`)**: All network servers bind strictly to `("127.0.0.1", 0)`. Zero listening on `0.0.0.0` or external network interfaces.
- **Fail-Closed Teardown**: Server threads are explicitly joined and listener sockets verified released upon teardown. Teardown failures fail closed.
- **Authentication != Authorization**: Authentication verifies *who* is calling; authorization verifies *what* the authenticated identity is permitted to do on a specific resource.
- **Credential != Identity != Authority**: A credential is an authenticating artifact; an identity is the associated subject; authority is granted by resource policy evaluation.
- **Password Verifiers != Fast General-Purpose Hashes**: Unkeyed fast hashes (e.g. SHA-256) are easily evaluated in parallel by GPUs/ASICs. Password verifiers require per-credential unique salts (>= 32 bits per NIST SP 800-63B-4) and tunable slow compute-hard functions (PBKDF2 per SP 800-132 / RFC 8018) or memory-hard candidates (Argon2id per RFC 9106).
- **Cost Parameters Are Not Timeless Invariants**: KDF work factors and iteration counts are environment and policy-dependent parameters that must increase over time; they are not timeless constants.
- **Constant-Time Comparison**: `hmac.compare_digest` is used to mitigate content-based short-circuiting timing attacks.
- **TeachingProfile-BearerV1**: An educational token profile modeled on RFC 7519 / RFC 8725 BCP. Strictly rejects `alg: "none"`, enforces allowed algorithms, validates signature, temporal validity (`exp`), and audience (`aud`).
- **Stateless Bearer Token Invalidation Boundary**: Purely stateless tokens cannot be revoked before expiration without out-of-band state tracking (revocation lists, epoch bumping, session store lookups).
- **Code != Data**: Vulnerabilities at composition boundaries occur when untrusted data alters the AST of an underlying interpreter.
- **SQL Parameterization**: Driver/API parameter binding (`?` placeholders) compiles query structure before value binding, treating input strictly as literal values. It does not parameterize table or column names.
- **XSS Boundary**: Browser HTML parser and DOM boundary. Defense requires context-aware autoencoding and W3C CSP Level 3 strict nonces.
- **CSRF Boundary**: Cross-origin HTTP request dispatch with ambient cookie authority. Defenses require `SameSite` cookies (noting that `Lax` allows top-level GET navigations), `Origin`/`Referer` validation, and anti-CSRF synchronizer tokens.
- **SSRF Boundary**: Server outbound network egress. Validates URL parsing, enforces scheme allowlists, validates resolved IP addresses against private/loopback/link-local ranges (RFC 1918, RFC 3927), and connects directly to the validated IP to mitigate DNS Rebinding (TOCTOU).
- **The 9-Layer Software Supply Chain Integrity Model**:
  1. Resolution Pinning (exact semantic version)
  2. Expected Digest Ownership (lockfile governed by trusted repository)
  3. Fetched-Byte Integrity (SHA-256 matching)
  4. Build Reproducibility (bit-for-bit identical rebuilds; does not prove source code is safe)
  5. Signature Verification (cryptographic signature verification; signature does not prove trustworthiness)
  6. Signer Identity Binding (key bound to authorized maintainer; digest != publisher identity)
  7. Source/Build Provenance (SLSA v1.2 verifiable provenance binding commit and builder)
  8. Trusted Builder Assumptions (evaluating isolated, hardened build platform)
  9. Verifier Policy Enforcement (deployment gates enforcing compliance)

---

## Files Overview

1. **`activity_l22_01.py`**
   - Implements authentication, password verifiers, and bearer token handling for L22-01:
     - `generate_password_verifier`: PBKDF2-HMAC-SHA256 with unique salt (>= 32 bits per NIST SP 800-63B-4).
     - `verify_password`: Format parsing and constant-time comparison via `hmac.compare_digest`.
     - `TeachingTokenAuthority`: Educational token profile validator enforcing algorithm whitelisting, signature verification, `exp`, `aud`, and rejecting `alg: "none"`.
     - `evaluate_resource_authorization`: Demonstrates that token validity is separate from resource authorization (Authn != Authz).

2. **`activity_l22_02.py`**
   - Implements web security, SQL parameterization, CSRF, and SSRF defenses for L22-02:
     - `query_user_unsafe` vs `query_user_safe`: SQLite in-memory demonstration of string concatenation vs parameterized driver binding.
     - `validate_and_resolve_destination` & `safe_http_fetch_over_socket`: SSRF egress client verifying private/metadata IP ranges and mitigating DNS Rebinding.
     - `SafeLocalhostServer` & `WebSecurityHarnessHandler`: Ephemeral loopback HTTP server demonstrating SameSite cookies, Origin checks, and anti-CSRF synchronizer tokens with fail-closed teardown.

3. **`activity_l22_03.py`**
   - Implements the 9-layer software supply chain integrity model for L22-03:
     - `verify_layer3_byte_integrity`: SHA-256 digest validation against trusted lockfile.
     - `verify_layer4_reproducibility`: Independent rebuild comparison.
     - `verify_layer5_and_6_signature_and_identity`: Signature verification and maintainer registry binding.
     - `verify_layer7_and_8_provenance_and_builder`: SLSA v1.2 provenance attestation verification.
     - `audit_dependency_against_policy`: Verifier policy gate evaluating all 9 layers.

4. **`reset.py`**
   - Fail-closed, idempotent cleanup script removing `.scratch/` and local `__pycache__/`.

5. **`test_m22.py`**
   - Standard library `unittest` suite validating all M22 mechanics, security invariants, and failure modes.

---

## Running the Activities & Tests

```bash
# 1. Run M22 Preflight capability check
python tests/preflight_security_synthesis.py --module M22

# 2. Run Lesson L22-01 activity (Password verifiers, bearer tokens, authn vs authz)
python labs/foundations/m22/activity_l22_01.py

# 3. Run Lesson L22-02 activity (SQL parameterization, CSRF, SSRF, localhost server)
python labs/foundations/m22/activity_l22_02.py

# 4. Run Lesson L22-03 activity (Software supply chain 9-layer audit)
python labs/foundations/m22/activity_l22_03.py

# 5. Run full standard library test suite
python -m unittest labs/foundations/m22/test_m22.py

# 6. Clean up course-owned scratch artifacts
python labs/foundations/m22/reset.py
```
