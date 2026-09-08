# Foundations M21 Evidence Template — Trust Boundaries & Cryptographic Use

Use this template for **one actual learner observation**. Do not prefill or copy another learner's runtime values, candidate paths, digests, tags, or PASS/FAIL evaluations.

---

## A — Environment Capabilities & Preflight

- Execution commit / ref: `[Record actual HEAD commit SHA]`
- Host Operating System / kernel / platform: `[Record actual OS, release, architecture]`
- Python Implementation & Version: `[Record actual Python implementation and version]`
- Standard Library Cryptography (`hashlib`, `hmac`, `secrets`): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- Path Confinement Primitives (`os.path.commonpath`, `Path.resolve`, `os.path.normcase`): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- Filesystem Symlink Creation Capability: `[Record SYMLINK CAPABILITY PASS or BLOCKED / NOT RUN]`
- Course-Owned Scratch Writability (`labs/foundations/m21/.scratch`): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- Optional PyCA `cryptography` Disposition: `[Record OPTIONAL PACKAGE AVAILABLE (with version) or OPTIONAL PACKAGE NOT INSTALLED / NOT RUN]`
- OQ-BP-006 Environment Policy Status: `OPEN / UNRESOLVED (Capability-based evaluation; no course-wide CPython pin frozen in learner truth)`

---

## B — L21-01 Threat Boundary & Authority Map

Record the architectural boundary inventory for the evaluated storage system worked example:

| Dimension | System Element | Learner Boundary Analysis |
| :--- | :--- | :--- |
| **Asset** | `[Record protected asset, e.g. synthetic user files / host files]` | `[Explain sensitivity and risk of unauthorized read/write]` |
| **Actor** | `[Record acting principal, e.g. untrusted remote client]` | `[Explain adversary assumptions and motivations]` |
| **Authority** | `[Record execution privilege, e.g. daemon process permissions]` | `[Identify ambient tokens vs required rights]` |
| **Boundary Crossing** | `[Record crossing point, e.g. untrusted path string -> POSIX open]` | `[Identify transition between untrusted input and trusted execution]` |
| **Verification Obligation** | `[Record verification check, e.g. commonpath containment]` | `[Explain exact validation invariant required before open]` |
| **Least Privilege** | `[Record privilege minimization control]` | `[Explain how daemon authority is bounded to storage root]` |
| **Defense in Depth** | `[Record layered safeguards]` | `[List API check, daemon confinement, and OS permission bits]` |
| **Residual Assumption** | `[Record uneliminated assumption]` | `[Articulate TOCTOU and intermediate directory trust assumptions]` |

---

## C — Path-Confinement Cases & Observations

Evaluate the standard candidate cases using `labs/foundations/m21/activity_l21_01.py`:

| Case ID | Candidate Input | Learner Prediction (Allow/Deny) | Actual Decision (ALLOWED / DENIED / BLOCKED) | Mechanism Observed | What This Result Does NOT Prove |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `contained-relative` | `notes/hello.txt` | `[Allow / Deny]` | `[Record observed decision]` | `[Record mechanism]` | `[Explain inference limits]` |
| `dotdot-contained` | `notes/../notes/hello.txt` | `[Allow / Deny]` | `[Record observed decision]` | `[Record mechanism]` | `[Explain why rejecting '..' alone is flawed]` |
| `parent-traversal` | `../outside.txt` | `[Allow / Deny]` | `[Record observed decision]` | `[Record mechanism]` | `[Explain why syntactic checks miss semantic paths]` |
| `absolute-outside` | `<abs_path>/outside.txt` | `[Allow / Deny]` | `[Record observed decision]` | `[Record mechanism]` | `[Explain why relative join rules can be subverted]` |
| `sibling-prefix` | `<abs_path>/store-evil/secret.txt` | `[Allow / Deny]` | `[Record observed decision]` | `[Record mechanism]` | `[Explain sibling-prefix confusion failure of startswith]` |
| `embedded-nul` | `notes/hello.txt\x00../outside.txt` | `[Allow / Deny]` | `[Record observed decision]` | `[Record mechanism]` | `[Explain why NUL must be rejected before any syscall]` |
| `symlink-escape` | `escape_link` | `[Allow / Deny]` | `[Record observed decision]` | `[Record mechanism]` | `[Explain symlink resolution and host capability status]` |

---

## D — Bounded Adversary Threat Model (STRIDE)

- Bounded Adversary Capabilities: `[Record what the attacker can control, e.g. path parameter strings via API]`
- Explicitly Excluded Capabilities: `[Record what is outside model, e.g. root privilege, physical RAM tampering, kernel exploits]`
- STRIDE Category Mapping (at Storage Boundary):
  - Category: `[Select one: Spoofing / Tampering / Repudiation / Information Disclosure / Denial of Service / Elevation of Privilege]`
  - Specific Threat: `[Describe threat, e.g. Elevation of Privilege via path traversal reading outside files]`
  - Bounded Mitigation: `[Describe mitigation, e.g. Canonical ancestry verification via os.path.commonpath]`
- Residual Risk: `[Explain residual vulnerability, e.g. TOCTOU symlink swap race if storage directory is shared writable]`

---

## E — L21-02 Cryptographic Primitive Selection Matrix

Fill in the primitive selection matrix evaluated in `labs/foundations/m21/activity_l21_02.py`:

| Scenario | Required Security Property | Chosen Primitive | Incorrect Tempting Trap | Major Non-Guarantee (Inference Boundary) |
| :--- | :--- | :--- | :--- | :--- |
| **1. File integrity against accidental corruption** | `[Record required property]` | `[Record chosen primitive]` | `[Record incorrect trap]` | `[Explain why unkeyed hash != authenticity]` |
| **2. Two-party message tamper detection** | `[Record required property]` | `[Record chosen primitive]` | `[Record incorrect trap]` | `[Explain why MAC != digital signature]` |
| **3. Multi-verifier public log verification** | `[Record required property]` | `[Record chosen primitive]` | `[Record incorrect trap]` | `[Explain why signature != unconditional non-repudiation]` |
| **4. Confidential payload on untrusted transport** | `[Record required property]` | `[Record chosen primitive]` | `[Record incorrect trap]` | `[Explain why encryption != authenticity; AEAD role]` |
| **5. Ephemeral TLS traffic key establishment** | `[Record required property]` | `[Record chosen primitive]` | `[Record incorrect trap]` | `[Explain key agreement != peer authentication; FS mode scope]` |
| **6. User credential storage verifier (M22 preview)** | `[Record required property]` | `[Record chosen primitive]` | `[Record incorrect trap]` | `[Explain why fast hashes fail as password verifiers]` |

---

## F — Unkeyed Hash vs. Keyed MAC Experimental Evidence

Record the actual experimental outputs from `labs/foundations/m21/activity_l21_02.py`:

- Synthetic Input Identifier: `[Record message identity, e.g. SYNTHETIC_MESSAGE]`
- Original Message Text: `[Record message string]`
- Original SHA-256 Digest: `[Record 64-hex digest or observation hash]`
- Tampered Message Text: `[Record modified message string]`
- Recomputed SHA-256 Digest: `[Record recomputed 64-hex digest]`
- Unkeyed Verification Results:
  - Original message against original digest: `[Record True / False]`
  - Tampered message against original digest: `[Record True / False (detects corruption)]`
  - Tampered message against recomputed digest: `[Record True / False (PASSES! Shows lack of authenticity)]`
- Keyed HMAC-SHA-256 Verification Results:
  - Shared Secret Key Material: `[Record key generation method: secrets.token_bytes(32)]`
  - Original HMAC Tag: `[Record 64-hex tag]`
  - Original message + original tag: `[Record True / False (verifies)]`
  - Tampered message + original tag: `[Record True / False (forgery detected)]`
  - Original message + forged tag: `[Record True / False (forgery detected)]`
- Core Mechanism Inference:
  `[Learner explains why an active in-path adversary can defeat unkeyed hashing by updating both data and digest, whereas HMAC resists forgery without knowledge of the shared secret]`

---

## G — Timing Attack Mitigation (`hmac.compare_digest`)

- Standard Library API Tested: `hmac.compare_digest`
- Behavior on Matching Strings: `[Record True / False]`
- Behavior on Non-Matching Strings: `[Record True / False]`
- Behavior on Type Mismatch (e.g. `str` vs `bytes`): `[Record exception raised, e.g. TypeError]`
- Documented API Contract:
  `[Learner summarizes Python documentation: designed to avoid content-based short-circuiting timing leaks]`
- Non-Proof Boundary:
  `[Learner articulates why software-level compare_digest does not constitute a physical constant-time proof on shared hardware/OS]`

---

## H — PKI / TLS 6-Layer Synthesis & Scoped Forward Secrecy

Explain the distinctions across the 6 verification layers in modern transport security:

1. **Certificate Credential**: `[Explain what the ASN.1 / X.509 structure asserts]`
2. **Path Validation to Trust Anchor**: `[Explain cryptographic chain validation to root store]`
3. **Service Identity Matching**: `[Explain SAN matching per RFC 9525]`
4. **Private-Key Possession**: `[Explain live proof of possession in the handshake]`
5. **Authentication**: `[Explain verification that the peer controls the claimed identity]`
6. **Authorization**: `[Explain why authenticating an identity does not confer arbitrary access rights]`

### Forward Secrecy Mode Boundary (RFC 9846 / TLS 1.3)
- (EC)DHE Key Exchange: `[Explain why ephemeral Diffie-Hellman provides forward secrecy]`
- PSK-Only (`psk_ke`): `[Explain why pure PSK mode lacks ephemeral forward secrecy if PSK is compromised]`
- 0-RTT Early Data: `[Explain why early data has weaker replay and secrecy properties]`

---

## I — Competency Alignment & Conceptual Grounding

### Primary Competencies Demonstrated
- **L21-01 `Judge`**: `[Record evaluation of storage service attack surface and isolation boundary]`
- **L21-01 `Explain`**: `[Record explanation of why security resides in boundaries rather than physical perimeters]`
- **L21-01 `Diagnose`**: `[Record diagnosis of sibling-prefix confusion and symlink escape failures]`
- **L21-02 `Explain`**: `[Record differentiation between Hash, MAC, Digital Signature, and AEAD]`
- **L21-02 `Judge`**: `[Record selection of primitives and rejection of fast hashes for password storage]`
- **L21-02 `Learn-New-Tech`**: `[Record navigation of standard crypto library APIs and Ed25519 signature probe]`

### Canonical Concepts Revisited (Zero First-Home Moves)
- **`EC-CON-017 Trust Boundary`**: Revisit from M07 `L07-01` (First Home). Applied across user/kernel, client/server, and crypto channels.
- **`EC-CON-013 Isolation`**: Revisit from M07 `L07-01` (First Home). Applied to process privilege confinement and temporary directories.
- **`EC-CON-007 Specification`**: Revisit from M02 `L02-03` (First Home). Applied to exact cryptographic algorithms and protocol standards.

---

## J — Provenance, Currentness & Cleanup Audit

### Authoritative Normative Sources Inspected
| Source Reference | Status / Date | Supported Claim | Non-Proof / Boundary |
| :--- | :--- | :--- | :--- |
| **Saltzer & Schroeder (1975)** | STABLE | Principles of Least Privilege & Complete Mediation | Does not specify modern OS system call implementations |
| **NIST SP 800-207** | STABLE / CURRENT (Aug 2020) | Zero Trust Architecture (no implicit perimeter trust) | Does not specify code-level input sanitization algorithms |
| **FIPS 198-1 / NIST SP 800-224** | CURRENT / UPDATING (June 2024 draft / June 2025 proposal) | HMAC algorithm specification and transition status | Mathematical spec; does not guarantee side-channel freedom |
| **FIPS 186-5** | STABLE / CURRENT (Feb 2023) | Digital Signature Standard (Ed25519, ECDSA, RSA) | Signature verification does not prove human identity |
| **NIST SP 800-38D** | STABLE | AES-GCM Authenticated Encryption with Associated Data | Nonce reuse catastrophically destroys authenticity |
| **RFC 9846** | STABLE / CURRENT (July 2026) | TLS 1.3 protocol specification; obsoletes RFC 8446 | Forward secrecy scoped to DHE/ECDHE; PSK-only differs |
| **Python hmac Docs** | CURRENT (v3.13/v3.14) | `compare_digest` timing mitigation contract | Mitigation API; not physical constant-time hardware proof |

### Cleanup & Idempotence Verification
- Execution of `python labs/foundations/m21/reset.py`: `[Record execution output and removed item count]`
- Verification that `.scratch/` was cleanly removed: `[Record True / False]`
- Second execution of `reset.py` (Idempotence check): `[Record True / False (zero errors)]`
- Unresolved Uncertainty: `[Record any environment limitation, unresolved question, or state NONE]`
