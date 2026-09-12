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
- OQ-BP-006 Environment Policy Status: `CLOSED (technical environment-definition/realization per #167; #158 re-check still required)`; evaluation here stays capability-based — no course-wide CPython pin is frozen in learner truth

---

## B — Authn/Authz Request Decision Path

Record the decision path analysis across the authentication and authorization lifecycle:

| Decision Step | Inspected Element | Verification Rule / Check | Outcome if Invalid | Non-Guarantee / What This Step Does NOT Prove |
| :--- | :--- | :--- | :--- | :--- |
| **1. Credential Check** | `[Record incoming token / session]` | `[Record the actual credential authenticator check; for TeachingProfile-BearerV1 this is an HS256 HMAC tag]` | `[Record HTTP 401 response]` | `[Explain why authenticator success != issuer trust != authorization; distinguish HMAC from digital signature]` |
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
- Cost parameter / iterations: `[Record the exact iteration count actually used by this run; do not copy an illustrative production recommendation]`
- Cost parameter rationale: `[Explain why cost is environment/policy-dependent and must increase over time; reject timeless constants]`
- Sensitive-value comparison API: `[Record hmac.compare_digest and explain its documented timing-analysis mitigation; do not claim physical constant-time proof]`
- Verifier record format: `[Record serialized string format: algo$params$salt$hash]`
- What the record does NOT prove: `[Explain why possessing a verifier does not prove the presenter is authorized to perform arbitrary actions]`

---

## D — Teaching-Token Validation Matrix

Record the validation rules enforced for `TeachingProfile-BearerV1` in `labs/foundations/m22/activity_l22_01.py`:

| Token Claim / Field | Status (Required / Optional) | Validation Invariant / Rule | Failure Status & Behavior | Core Non-Guarantee |
| :--- | :--- | :--- | :--- | :--- |
| `alg` (Header) | Required | Must match approved whitelist (`HS256`); reject `alg: "none"` | Rejection / Invalid Token | `[Explain why accepting arbitrary alg header enables bypasses]` |
| `typ` (Header) | Required | Must be `"JWT"` | Rejection / Invalid Token | `[Explain profile type disambiguation]` |
| `profile` (Header) | Required | Must equal `TeachingProfile-BearerV1` | Rejection / Invalid Token | `[Explain why this is a course-owned verifier profile, not universal JWT policy]` |
| `sub` (Payload) | Required | Non-empty string identifying the principal | Rejection / Invalid Token | `[Explain why knowing subject identity does not prove authorization]` |
| `aud` (Payload) | Required | Must strictly match recipient service identifier | Rejection / Invalid Token | `[Explain token substitution across services if aud omitted]` |
| `iss` (Payload) | Required | Must equal the issuer configured by this teaching verifier policy | Rejection / Invalid Token | `[Explain why issuer matching is policy binding, not resource authorization]` |
| `exp` (Payload) | Required | Integer timestamp; must satisfy `exp > current_time` | Rejection / Expired Token | `[Explain why stateless tokens remain valid until exp unless out-of-band state exists]` |
| `iat` (Payload) | Required | Integer timestamp of token creation | Rejection / Invalid Token | `[Explain issued-at ordering checks]` |
| `HMAC authentication tag` | Required | HS256 HMAC over `header.payload` must match under the configured shared secret | Rejection / Tampered Token | `[Explain why HMAC is not a public-key digital signature and cannot uniquely attribute one shared-secret holder]` |

---

## E — Session / Bearer-Token / Revocation Judgment

Compare stateful sessions against stateless bearer tokens across operational and security dimensions:

| Dimension | Stateful Server Sessions (Cookies + Store) | Self-Contained Authenticated Bearer Tokens (JWT / Teaching Profiles) | Architectural Trade-Off Analysis |
| :--- | :--- | :--- | :--- |
| **State Ownership** | `[Record where state is stored, e.g. DB/Redis]` | `[Record where state is stored, e.g. client-held]` | `[Analyze storage overhead vs decentralization]` |
| **Immediate Invalidation** | `[Record mechanism, e.g. delete row in session store]` | `[Record limitation: the self-contained token alone cannot learn new revocation state before exp; record any out-of-band mechanism]`| `[Analyze revocation latency and risk exposure]` |
| **Cross-Domain Delegation** | `[Record ambient cookie domain scoping limits]` | `[Record explicit bearer authorization header dispatch]` | `[Analyze mobile / multi-API architecture fit]` |
| **Ambient Authority Risk** | `[Record CSRF ambient cookie auto-attach vulnerability]`| `[Record explicit header requirement eliminating ambient CSRF]`| `[Explain CSRF vs XSS token theft trade-offs]` |
| **Operational Scaling** | `[Record central store read/write bottlenecks]` | `[Record whether this profile validates locally and what key/policy/revocation state still exists]` | `[Evaluate operational complexity vs security trade-off]` |

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
  - RFC 9700 / BCP 240 (OAuth 2.0 Security BCP, January 2025): `[Record: public clients MUST use PKCE; confidential clients are RECOMMENDED to use PKCE with the RFC's scoped OIDC nonce alternative; ROPC MUST NOT; Implicit SHOULD NOT]`
  - OAuth 2.1 Active Draft: `[Record current active draft revision checked for this evidence; implementation baseline on 2026-09-07 was draft-ietf-oauth-v2-1-16 (3 Sep 2026)]`

---

## G — Code-vs-Data / SQL Parameterization

Record the SQL injection vs parameterized execution observations from `labs/foundations/m22/activity_l22_02.py`:

- Unsafe Query Construction:
  - Concatenation template: `[Record raw SQL query string with formatting]`
  - Malicious payload used: `[Record injection string, e.g. admin' OR '1'='1]`
  - Observed unsafe SQL-text change: `[Explain how concatenation allowed input characters to become SQL syntax in this fixture; do not claim a specific internal AST implementation unless separately observed]`
  - Observed result: `[Record leaked records count and data exposure]`
- Parameterized Query Construction:
  - Parameterized statement: `SELECT id, username, role, email, account_balance FROM users WHERE username = ?`
  - Parameter binding: `(username_input,)`
  - Observed result: `[Record actual result; explain that the SQLite ? value parameter remained separate from the SQL template]`
  - Architectural mechanism: `[Explain the driver/API contract that separates the SQL statement template from bound value parameters; exact parser/bytecode phases are engine-specific]`
- What Parameterization Protects: `[Explain that parameterization protects SQL value positions / data literals]`
- What Parameterization Does NOT Protect: `[Explain that table names, column names, and SQL keywords cannot be parameterized; dynamic schemas require strict allowlisting]`

---

## H — XSS / CSRF / SSRF Defensive Matrix

Record the defensive boundaries evaluated in `labs/foundations/m22/activity_l22_02.py`:

| Vulnerability Class | Threat Boundary Crossing | Bounded Local Failure Mode | Structural Defense Implemented | Residual Assumption / Limit |
| :--- | :--- | :--- | :--- | :--- |
| **XSS** | Browser HTML Parser & DOM | Untrusted text executed as active script in victim session | Context-aware autoencoding + W3C CSP Level 3 strict nonces | CSP does not eliminate DOM clobbering or server-side template injection |
| **CSRF** | Cross-Origin HTTP Request Dispatch | Ambient session cookie auto-attached to state-mutating POST | `SameSite=Lax/Strict` cookies + `Origin` header check + Anti-CSRF synchronizer token | `SameSite=Lax` permits top-level GET navigations; state mutation on GET is vulnerable |
| **SSRF** | Server Outbound Network Egress | Server coerced to fetch prohibited destinations | URL parse + candidate-IP policy + HTTP-only direct connection to a validated IP in this local fixture | Direct binding here removes one second-DNS-lookup path; it does not cover redirects, proxies, HTTPS/TLS identity, connection pools, or other fetch paths |

---

## I — Supply-Chain 9-Layer Audit

Record the software supply chain verification observations from `labs/foundations/m22/activity_l22_03.py`:

| Layer ID | Supply Chain Layer Concern | Verification Mechanism Enforced | Controlled Tampering Observation | Core Non-Guarantee (Inference Boundary) |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1** | Resolution Pinning | Exact semantic version frozen in lockfile | Range operators (`>=`) flagged as unpinned | Pinned version != Pinned digest (upstream can replace unpinned files) |
| **Layer 2** | Expected Digest Ownership | Lockfile records expected cryptographic hash | Missing expected SHA-256 rejected by policy | Digest ownership does not verify whether source code is safe |
| **Layer 3** | Fetched-Byte Integrity | Computed SHA-256 compared with a trusted expected digest | `[Record actual tamper/match observation]` | Digest match depends on expected-digest ownership and hash assumptions; it does NOT prove publisher identity |
| **Layer 4** | Build Reproducibility | Policy compares artifact bytes with supplied independent-rebuild bytes | `[Record actual matching/mismatching rebuild observation]` | Matching rebuilds do not rule out malicious source, shared compromised toolchains, or non-independent builds |
| **Layer 5** | Signature Verification (conceptual layer) | `[Record conceptual public-signature requirement; Core runtime uses a labeled HMAC stand-in only]` | `[Record HMAC stand-in result separately from any real signature evidence]` | HMAC is NOT a digital signature; neither authenticator nor signature proves code trustworthiness |
| **Layer 6** | Signer Identity Binding | `[Record conceptual signer-identity policy; Core uses a synthetic key-id allowlist paired with the HMAC stand-in]` | `[Record actual synthetic policy result]` | Core key-id policy does not prove real-world signer identity |
| **Layer 7** | Build/Source Provenance | Core checks a synthetic subset of SLSA-style metadata (statement/predicate/subject/source/builder) | `[Record actual metadata mismatch result]` | Core does NOT verify a real attestation envelope/signature or certify a SLSA level |
| **Layer 8** | Trusted Builder Assumptions | Synthetic builder id checked against local allowlist | `[Record actual allowlist result]` | A string allowlist does NOT prove real builder isolation, hardening, ephemerality, or attestation authenticity |
| **Layer 9** | Verifier Policy Enforcement| Gate rejects package failing any required layer | Overall verdict: `REJECT` on violation | Verifier policy requires explicit organizational risk judgment |

---

## J — Competencies, Concepts & Reviewer Judgment

### Primary Competencies
- `Judge` (L22-01, L22-02, L22-03): `[Evaluate authentication vs authorization architectures, CSRF vs token trade-offs, and supply chain adoption risk]`
- `Explain` (L22-01, L22-02): `[Explain why authentication != authorization, why parameterized value binding separates data from SQL syntax in supported value positions, and why stateless token revocation requires state]`
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

| Authority / Standard | Specification / Identifier | Date & Formal Status | Checked Date | Claim Bounded by Implementation | Non-Proof / Inference Limit | Rights / Provenance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Password Storage** | NIST SP 800-63B-4 §3.1.1.2 | July 2025 Final | 2026-09-07 | Salt >= 32 bits and chosen to minimize collisions; approved password hashing scheme; cost factor policy/environment dependent | Random salts are not mathematically guaranteed unique; the record does not make weak passwords unguessable | U.S. Government publication; repository foreign-rights caveat |
| **PBKDF2** | NIST SP 800-132 / RFC 8018 | Dec 2010 Final; NIST revision planned | 2026-09-07 | PBKDF2 compute-hard KDF route used by stdlib teaching Core | PBKDF2 is not memory-hard; no universal iteration count or hardware rate | NIST U.S. Government publication + IETF Trust terms for RFC 8018 |
| **Argon2id** | RFC 9106 | Informational RFC, July 2021 | 2026-09-07 | Memory-hard current-practice reference only | Not stdlib Required Core; absence is NOT RUN, not failure | IETF Trust Legal Provisions |
| **OAuth 2.0 Security BCP** | RFC 9700 / BCP 240 | January 2025 Best Current Practice | 2026-09-07 | Public clients MUST use PKCE; confidential clients are recommended with scoped alternatives; ROPC MUST NOT | OAuth authorization delegation != user authentication | IETF Trust Legal Provisions |
| **OAuth 2.1 Draft** | draft-ietf-oauth-v2-1-16 | Active Internet-Draft, 3 Sep 2026 | 2026-09-07 | Current work-in-progress OAuth 2.1 consolidation baseline | Internet-Draft is not a timeless invariant and revision number will drift | IETF Trust Legal Provisions |
| **PKCE** | RFC 7636 | Standards Track | 2026-09-07 | code_verifier / S256 challenge binding under the specified threat model | Does not authenticate client identity or protect a fully compromised client device | IETF Trust Legal Provisions |
| **OpenID Connect** | OpenID Connect Core 1.0 incorporating errata set 2 | Final / Errata, 15 Dec 2023 | 2026-09-07 | Identity layer on top of OAuth 2.0 used only to explain OAuth != authentication | Required Core does not run a live IdP/OIDC flow | OpenID Foundation specification/IPR terms; linked/paraphrased |
| **JSON Web Token** | RFC 7519 / RFC 8725 | Standards Track / BCP | 2026-09-07 | Application-selected algorithms and claims validation; TeachingProfile-BearerV1 itself rejects alg:none | RFC 8725 does not make this course-profile alg:none rule a universal theorem; HS256 is HMAC, not digital signature | IETF Trust Legal Provisions |
| **Content Security Policy** | W3C CSP Level 3 | Working Draft, 29 Jul 2026 | 2026-09-07 | Nonce-based script policy as defense in depth | CSP is not a substitute for context-correct output handling | W3C document license; linked/paraphrased |
| **Cookies** | draft-ietf-httpbis-layered-cookies-02 | Active Internet-Draft, 21 May 2026 | 2026-09-07 | SameSite semantics used as current draft context | Draft may change; SameSite is not universal CSRF immunity | IETF Trust Legal Provisions |
| **Supply Chain Levels** | OpenSSF SLSA v1.2 | Approved, 24 Nov 2025 | 2026-09-07 | Provenance v1 / Build Track concepts; Core only validates synthetic metadata/policy | Core does not verify a real attestation signature or certify a builder/SLSA level | Community Specification License 1.0; linked/paraphrased |
| **Python stdlib** | Python `hashlib`, `hmac`, `sqlite3`, `socket` docs/APIs | Current API family; OQ-BP-006 CLOSED (technical environment-definition/realization per #167; #158 re-check still required) | 2026-09-07 | Required Core mechanisms/capabilities only | Behavior and availability remain host/runtime dependent; no course-wide CPython pin | PSF License v2 for docs; examples additionally Zero-Clause BSD where applicable |

### Deterministic Reset Verification
- Command Run: `[Record exact reset command actually run]`
- Scratch Cleanup Observation: `[Record actual .scratch state/result]`
- Port / Server Teardown Observation: `[Record actual listener/thread result from the activity/test, or NOT RUN if not exercised]`
- Idempotence Observation: `[Record result of a second reset run, or NOT RUN]`
- Disposition: `[PASS / FAIL / BLOCKED / NOT RUN]`
- Inference limit: `[State that reset only owns M22 course scratch/cache; it does not prove unrelated host resources are clean]`
