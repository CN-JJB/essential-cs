# Foundations M22 Evidence Template — Authn/Authz & Secure Composition

Use this template for **one actual learner observation**. Do not prefill or copy another learner's runtime values, candidate hashes, salts, tokens, timing values, versions, or PASS/FAIL evaluations.

> **Evaluation Invariant**: Machine PASS != learner competency PASS. Automated checks prove mechanical correctness of code fixtures; learner competency requires conceptual mastery, honest boundary analysis, and sound architectural judgment.

---

## A — Environment Capabilities & Preflight

- Execution commit / ref: `[Record actual HEAD commit SHA]`
- Exact command(s) actually run: `[Record command text exactly]`
- Exact runtime disposition for each command: `[Record PASS / FAIL / BLOCKED / NOT RUN; never infer PASS from capability absence]`
- Host Operating System / kernel / platform: `[Record actual OS, release, architecture]`
- Python Implementation & Version: `[Record actual Python implementation and version]`
- Standard Library Cryptography (`hashlib`, `hmac`, `secrets`): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- Password KDF Interface (`hashlib.pbkdf2_hmac`, `hmac.compare_digest`): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- Relational Database Interface (`sqlite3` in-memory): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- Loopback Networking Capability (`127.0.0.1:0` bind/listen): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- Course-Owned Scratch Writability (`labs/foundations/m22/.scratch`): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- Optional `argon2-cffi` Disposition: `[Record OPTIONAL PACKAGE AVAILABLE (with version) or OPTIONAL PACKAGE NOT INSTALLED / NOT RUN]`
- Optional PyCA `cryptography` Disposition: `[Record OPTIONAL PACKAGE AVAILABLE (with version) or OPTIONAL PACKAGE NOT INSTALLED / NOT RUN]`
- OQ-BP-006 Environment Policy Status: `OPEN / UNRESOLVED (Capability-based evaluation; no course-wide CPython pin frozen in learner truth)`

---

## B — Authn/Authz Request Decision Path

Record the decision path analysis across the authentication and authorization lifecycle:

| Decision Step | Inspected Element | Verification Rule / Check | Outcome if Invalid | Non-Guarantee / What This Step Does NOT Prove |
| :--- | :--- | :--- | :--- | :--- |
| **1. Credential Check** | `[Record incoming token / session]` | `[Record signature / MAC check]` | `[Record HTTP 401 response]` | `[Explain why signature != issuer trust or authorization]` |
| **2. Temporal Validity** | `[Record exp claim / session expiry]` | `[Record exp > now validation]` | `[Record HTTP 401 response]` | `[Explain stateless token revocation latency]` |
| **3. Audience Restriction** | `[Record aud claim]` | `[Record aud == this_service]` | `[Record HTTP 401 response]` | `[Explain why aud check is required to prevent token substitution]` |
| **4. Authenticated Identity** | `[Record sub claim / principal]` | `[Record identity establishment]` | `[Record rejection]` | `[Explain why Identity != Authority]` |
| **5. Resource Authorization** | `[Record action and target resource]` | `[Record policy rule: action:resource]`| `[Record HTTP 403 response]` | `[Explain why authn alone does not protect against IDOR/BOLA]` |
| **6. Trust Boundary & Residuals**| `[Record architectural boundary]`| `[Record verification obligation]` | `[Record failure mode]` | `[Articulate residual assumptions across caller and service]` |

---

## C — Password-Verifier Record

Record the password verifier schema and parameters evaluated in `labs/foundations/m22/activity_l22_01.py`:

- Exact algorithm / profile used: `[Record algorithm, e.g. pbkdf2_sha256 per SP 800-132 / SP 800-63B-4]`
- Salt source: `[Record salt generation API, e.g. secrets.token_bytes]`
- Salt length: `[Record salt length in bytes/bits; must be >= 32 bits per NIST SP 800-63B-4]`
- Cost parameter / iterations: `[Record iteration count used, e.g. 100,000]`
- Cost parameter rationale: `[Explain why cost is environment/policy-dependent and must increase over time; reject timeless constants]`
- Constant-time comparison API: `[Record comparison API, e.g. hmac.compare_digest, and explain timing attack mitigation]`
- Verifier record format: `[Record serialized string format: algo$params$salt$hash]`
- What the record does NOT prove: `[Explain why possessing a verifier does not prove the presenter is authorized to perform arbitrary actions]`

---

## D — Teaching-Token Validation Matrix

Record the validation rules enforced for `TeachingProfile-BearerV1` in `labs/foundations/m22/activity_l22_01.py`:

| Token Claim / Field | Status (Required / Optional) | Validation Invariant / Rule | Failure Status & Behavior | Core Non-Guarantee |
| :--- | :--- | :--- | :--- | :--- |
| `alg` (Header) | Required | Must match approved whitelist (`HS256`); reject `alg: "none"` | Rejection / Invalid Token | `[Explain why accepting arbitrary alg header enables bypasses]` |
| `typ` (Header) | Required | Must be `"JWT"` | Rejection / Invalid Token | `[Explain profile type disambiguation]` |
| `sub` (Payload) | Required | Non-empty string identifying the principal | Rejection / Invalid Token | `[Explain why knowing subject identity does not prove authorization]` |
| `aud` (Payload) | Required | Must strictly match recipient service identifier | Rejection / Invalid Token | `[Explain token substitution across services if aud omitted]` |
| `exp` (Payload) | Required | Integer timestamp; must satisfy `exp > current_time` | Rejection / Expired Token | `[Explain why stateless tokens remain valid until exp unless out-of-band state exists]` |
| `iat` (Payload) | Required | Integer timestamp of token creation | Rejection / Invalid Token | `[Explain issued-at ordering checks]` |
| `signature` | Required | HMAC-SHA256 computed over `header.payload` matching expected | Rejection / Tampered Token | `[Explain why signature proves key possession, not author trustworthiness]` |

---

## E — Session / Bearer-Token / Revocation Judgment

Compare stateful sessions against stateless bearer tokens across operational and security dimensions:

| Dimension | Stateful Server Sessions (Cookies + Store) | Stateless Signed Bearer Tokens (JWT / Profiles) | Architectural Trade-Off Analysis |
| :--- | :--- | :--- | :--- |
| **State Ownership** | `[Record where state is stored, e.g. DB/Redis]` | `[Record where state is stored, e.g. client-held]` | `[Analyze storage overhead vs decentralization]` |
| **Immediate Invalidation** | `[Record mechanism, e.g. delete row in session store]` | `[Record limitation: impossible without out-of-band state]`| `[Analyze revocation latency and risk exposure]` |
| **Cross-Domain Delegation** | `[Record ambient cookie domain scoping limits]` | `[Record explicit bearer authorization header dispatch]` | `[Analyze mobile / multi-API architecture fit]` |
| **Ambient Authority Risk** | `[Record CSRF ambient cookie auto-attach vulnerability]`| `[Record explicit header requirement eliminating ambient CSRF]`| `[Explain CSRF vs XSS token theft trade-offs]` |
| **Operational Scaling** | `[Record central store read/write bottlenecks]` | `[Record distributed verification without DB lookup]` | `[Evaluate operational complexity vs security trade-off]` |

---

## F — OAuth 2.1 / PKCE Synthesis

Record the architectural analysis of OAuth 2.1 Authorization Code Flow with PKCE per RFC 9700 (BCP 240) and RFC 7636:

- Primary OAuth Roles:
  - Resource Owner: `[Identify role, e.g. User]`
  - Client: `[Identify role, e.g. SPA / Mobile App]`
  - Authorization Server: `[Identify role, e.g. Identity Provider / AS]`
  - Resource Server: `[Identify role, e.g. Backend API]`
- Authorization vs Authentication Boundary:
  - `[Explain why OAuth 2.0/2.1 is an AUTHORIZATION delegation framework, NOT an authentication protocol by itself]`
  - `[Identify what additional identity layer (e.g. OpenID Connect Core 1.0) is required to authenticate user identity]`
- PKCE (Proof Key for Code Exchange) Binding:
  - `code_verifier` creation: `[Record entropy source and character set per RFC 7636]`
  - `code_challenge` derivation: `[Record S256 formula: BASE64URL(SHA256(code_verifier))]`
  - How PKCE binds code exchange: `[Explain why an attacker intercepting the authorization code cannot exchange it without the code_verifier]`
- Exact Current Authority Citation:
  - RFC 9700 / BCP 240 (OAuth 2.0 Security BCP, January 2025): `[Record key mandates: PKCE MUST for public, ROPC MUST NOT, Implicit SHOULD NOT]`
  - OAuth 2.1 Active Draft: `[Record current active draft revision checked at implementation time, e.g. draft-ietf-oauth-v2-1-15]`

---

## G — Code-vs-Data / SQL Parameterization

Record the SQL injection vs parameterized execution observations from `labs/foundations/m22/activity_l22_02.py`:

- Unsafe Query Construction:
  - Concatenation template: `[Record raw SQL query string with formatting]`
  - Malicious payload used: `[Record injection string, e.g. admin' OR '1'='1]`
  - Observed AST alteration: `[Explain how quotes closed early and OR turned user data into SQL boolean syntax]`
  - Observed result: `[Record leaked records count and data exposure]`
- Parameterized Query Construction:
  - Parameterized statement: `SELECT id, username, role, email, account_balance FROM users WHERE username = ?`
  - Parameter binding: `(username_input,)`
  - Observed result: `[Record result: 0 records returned; syntax structure remained immutable]`
  - Architectural mechanism: `[Explain how the driver/API contract separates query compilation from value literal binding]`
- What Parameterization Protects: `[Explain that parameterization protects SQL value positions / data literals]`
- What Parameterization Does NOT Protect: `[Explain that table names, column names, and SQL keywords cannot be parameterized; dynamic schemas require strict allowlisting]`

---

## H — XSS / CSRF / SSRF Defensive Matrix

Record the defensive boundaries evaluated in `labs/foundations/m22/activity_l22_02.py`:

| Vulnerability Class | Threat Boundary Crossing | Bounded Local Failure Mode | Structural Defense Implemented | Residual Assumption / Limit |
| :--- | :--- | :--- | :--- | :--- |
| **XSS** | Browser HTML Parser & DOM | Untrusted text executed as active script in victim session | Context-aware autoencoding + W3C CSP Level 3 strict nonces | CSP does not eliminate DOM clobbering or server-side template injection |
| **CSRF** | Cross-Origin HTTP Request Dispatch | Ambient session cookie auto-attached to state-mutating POST | `SameSite=Lax/Strict` cookies + `Origin` header check + Anti-CSRF synchronizer token | `SameSite=Lax` permits top-level GET navigations; state mutation on GET is vulnerable |
| **SSRF** | Server Outbound Network Egress | Server coerced to fetch private/metadata resources (`169.254.x.x`, `10.x.x.x`) | URL parse + IP blocklist + post-resolution direct socket binding | URL regex string checks fail against DNS rebinding (TOCTOU) and open redirects |

---

## I — Supply-Chain 9-Layer Audit

Record the software supply chain verification observations from `labs/foundations/m22/activity_l22_03.py`:

| Layer ID | Supply Chain Layer Concern | Verification Mechanism Enforced | Controlled Tampering Observation | Core Non-Guarantee (Inference Boundary) |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1** | Resolution Pinning | Exact semantic version frozen in lockfile | Range operators (`>=`) flagged as unpinned | Pinned version != Pinned digest (upstream can replace unpinned files) |
| **Layer 2** | Expected Digest Ownership | Lockfile records expected cryptographic hash | Missing expected SHA-256 rejected by policy | Digest ownership does not verify whether source code is safe |
| **Layer 3** | Fetched-Byte Integrity | Computed SHA-256 matches expected digest | Tampered byte rejected with `TAMPER DETECTED` | Digest verifies byte immutability, NOT publisher identity |
| **Layer 4** | Build Reproducibility | Independent rebuilds produce bit-for-bit identical hashes | Non-deterministic build flagged as unverified | Reproducibility does NOT prove source code is non-malicious |
| **Layer 5** | Signature Verification | Cryptographic signature over archive verified | Forged or invalid signature rejected | Valid signature proves key possession, NOT trustworthiness |
| **Layer 6** | Signer Identity Binding | Public key mapped to authorized maintainer registry | Unauthorized key rejected by policy | Identity proves who signed, NOT that build was untampered |
| **Layer 7** | Build/Source Provenance | SLSA v1.2 attestation binding git commit and builder | Subject hash mismatch rejected | Provenance without builder verification is merely unverified metadata |
| **Layer 8** | Trusted Builder Assumptions| Builder identity checked against approved list | Untrusted / compromised builder rejected | Hardened builder cannot prevent compromised upstream source commits |
| **Layer 9** | Verifier Policy Enforcement| Gate rejects package failing any required layer | Overall verdict: `REJECT` on violation | Verifier policy requires explicit organizational risk judgment |

---

## J — Competencies, Concepts & Reviewer Judgment

### Primary Competencies
- `Judge` (L22-01, L22-02, L22-03): `[Evaluate authentication vs authorization architectures, CSRF vs token trade-offs, and supply chain adoption risk]`
- `Explain` (L22-01, L22-02): `[Explain why authentication != authorization, why SQL parameterization eliminates injection, and why stateless token revocation requires state]`
- `Diagnose` (L22-02): `[Diagnose injection points at composition boundaries and identify ambient authority flaws]`
- `Learn-New-Tech` (L22-03): `[Inspect lockfile specifications, SLSA v1.2 provenance formats, and hash-checking modes]`

### Concept Revisits
- `EC-CON-017 Trust Boundary` (First Home: M07 `L07-01`): `[Explain how trust boundaries operate at credential verifiers, database drivers, web origins, and external package imports]`
- `EC-CON-007 Specification` (First Home: M02 `L02-03`): `[Explain how specifications govern token profiles, password hashing schemas, and OAuth 2.1 flows]`
- `EC-CON-009 Correctness` (First Home: M02 `L02-03`): `[Explain correctness under active adversarial payload injection at composition boundaries]`
- `EC-CON-008 Invariant` (First Home: M02 `L02-03`): `[Explain immutability invariants enforced by cryptographic digests in software supply chains]`

### Reviewer Gate (Human / Lead Review Required)
- Reviewer Evaluation: `[Record PASS / NEEDS REVISION]`
- Reviewer Signature / Identifier: `[Record reviewer name / handle]`
- Date Reviewed: `[YYYY-MM-DD]`
- Reviewer Notes: `[Record qualitative review of learner trade-off explanations]`

---

## K — Currentness, Provenance, Rights & Cleanup

Record the implementation-time authority audit for all standards cited:

| Authority / Standard | Specification / Identifier | Date & Formal Status | Checked Date | Claim Bounded by Implementation | Non-Proof / Inference Limit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Password Storage** | NIST SP 800-63B-4 §3.1.1.2 | July 2025 Final | 2026-09-07 | Salt >= 32 bits; approved KDF (PBKDF2 compute-hard); cost factor policy-dependent | Does not prove password cannot be cracked if short/predictable |
| **PBKDF2** | NIST SP 800-132 / RFC 8018 | Dec 2010 Final (revision planned) | 2026-09-07 | Compute-hard iteration-based KDF | PBKDF2 is not memory-hard; ASIC acceleration possible |
| **Argon2id** | RFC 9106 | STABLE | 2026-09-07 | Memory-hard password hashing (current-practice reference) | Not present in standard library; requires capability gating |
| **OAuth 2.0 Security BCP** | RFC 9700 / BCP 240 | January 2025 Best Current Practice | 2026-09-07 | PKCE MUST for public; ROPC MUST NOT; exact redirect matching | OAuth authorization delegation != user authentication |
| **OAuth 2.1 Draft** | draft-ietf-oauth-v2-1-15 | Active Internet-Draft (March 2026) | 2026-09-07 | Consolidated OAuth 2.1 specification | Internet-Draft is work in progress; not timeless invariant |
| **PKCE** | RFC 7636 | STABLE Standards Track | 2026-09-07 | code_verifier and code_challenge S256 binding | Does not protect against client device compromise |
| **JSON Web Token** | RFC 7519 / RFC 8725 | STABLE Standards Track / BCP | 2026-09-07 | Claims validation, reject alg: none, aud enforcement | Valid signature != issuer trust != resource authorization |
| **Content Security Policy**| W3C CSP Level 3 | Working Draft (29 July 2026) | 2026-09-07 | Strict nonce-based script execution policy | CSP is defense-in-depth; not substitute for output encoding |
| **Cookies** | draft-ietf-httpbis-layered-cookies-02 | Active Internet-Draft (21 May 2026) | 2026-09-07 | Layered cookie semantics; SameSite Lax/Strict | Internet-Draft work in progress; SameSite Lax allows GET nav |
| **Supply Chain Levels** | OpenSSF SLSA v1.2 | Approved (24 November 2025) | 2026-09-07 | Verifiable build provenance schema binding commit & builder | Provenance does not verify source code is bug-free |
| **Python stdlib** | CPython 3.13 stdlib (`hashlib`, `hmac`, `sqlite3`, `socket`) | Python Standard Library | 2026-09-07 | Parameterized queries, loopback socket binding, fail-closed teardown | Standard library behavior depends on host OS capabilities |

### Deterministic Reset Verification
- Command Run: `python labs/foundations/m22/reset.py`
- Scratch Cleaned: `labs/foundations/m22/.scratch/` deleted
- Port Release Verified: Listener socket closed and probe connection refused
- Idempotence Verified: Second consecutive run completed with 0 errors
- Disposition: `PASS`
