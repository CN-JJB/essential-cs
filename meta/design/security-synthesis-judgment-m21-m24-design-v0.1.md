# S7 M21–M24 Security Synthesis & Systems Judgment Design Dossier v0.1

## 1. Executive Design Decision & Readiness

### Recommendation: **READY FOR LESSON / ACTIVITY IMPLEMENTATION**

This dossier establishes the authoritative pedagogical, technical, and structural design contract for Stage 7 (S7) of the Essential CS curriculum, encompassing:
- **Module M21 — Security Synthesis I: Trust & Crypto Use**
- **Module M22 — Security Synthesis II: Authn/Authz & Secure Composition**
- **Module M23 — Systems Thinking & Judgment**
- **Module M24 — Final System Defense**

The curriculum design adheres strictly to the fundamental principles established in `meta/CURRICULUM_INVARIANTS.md`, the architectural precedents of Stages 1–6, and the authoritative research compiled in `research/security-synthesis-judgment-m21-m24-v0.1.md`.

### Core Architectural Commitments

1. **Design-Only Scope Boundary:**
   This dossier specifies the complete instructional, technical, empirical, and evaluation contracts for all 10 lessons across Modules M21–M24. Strictly zero learner-facing markdown lessons are drafted, zero executable lab/activity fixtures in `labs/` or `project/` are created, and zero production/infrastructure code is added. Formal learner implementation is gated to downstream execution tasks.

2. **Absolute Module DAG Invariance:**
   The Stage 7 dependency topology is preserved without modification:
   - **M21:** Hard inputs `M11` (Network Applications, TLS/HTTP), `M07` (Virtual Memory & Isolation), `M12` (Web & Browser); Soft input `M09` (Storage & Durability).
   - **M22:** Hard inputs `M21` (Security Synthesis I), `M11`, `M12`; Soft input `M19` (Modern Infrastructure & Deployment).
   - **M23:** Hard inputs `M20` (Observability & Reliability), `M21`; Soft inputs `M22` (Security Synthesis II), `M17` (Replication & Consistency).
   - **M24:** Hard input `M23` (Systems Thinking & Judgment); Soft input `M20` (Observability & Incident Debugging).
   No new hard prerequisite edges are introduced; no implicit stage-wide prerequisites are imposed.

3. **Concept Registry & Competency Precision:**
   - Total canonical concepts remain exactly **18** (`meta/CONCEPT_REGISTRY.md`). Exactly zero new Concept IDs are introduced.
   - First-home invariants remain inviolate: `EC-CON-017 Trust Boundary` (信任边界) and `EC-CON-013 Isolation` (隔离) maintain their canonical first home in **M07 `L07-01`**. Modules M21 and M22 perform holistic synthesis and contextual revisit; they do not claim first-home ownership.
   - All other canonical concepts (`EC-CON-007 Specification`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness` in M02; `EC-CON-010 Failure` in M03; `EC-CON-016 Durability` in M09; `EC-CON-014 Consistency` in M14; `EC-CON-015 Concurrency` in M15; `EC-CON-018 Process` in M06) are strictly respected.
   - The concept `Consensus` remains deliberately deferred as a canonical Registry ID per Decision D-025.
   - Only the canonical 8 competencies are utilized: `Trace`, `Explain`, `Observe`, `Diagnose`, `Correctness`, `Judge`, `Estimate`, `Learn-New-Tech`.

4. **Defense-First Security Stance & Safe-Target Architecture (Candidate B Accepted):**
   In strict conformance with Decision D-012, all offensive tooling, automated vulnerability scanners, exploit payloads, weaponized attack chains, and public or unauthorized remote targets are absolutely forbidden.
   This design formally **accepts and refines Candidate B**:
   - Hands-on security education is delivered entirely via self-contained, course-owned localhost test fixtures embedded within standard activity modules (`activity_l21_02.py` and `activity_l22_02.py`), paired with architectural security reviews of the learner's own Mini Cloud App codebase (at milestones P2, P8, and P9).
   - All data used in exercises is synthetic, non-sensitive, and generated on ephemeral localhost loopback sockets (`127.0.0.1`).
   - The pedagogical stance is strictly **fix-and-verify**: learners diagnose architectural failure boundaries, inspect broken security invariants, apply robust defensive remediations, and execute automated regression assertions.
   - **Lab Counts Invariance:** Required Labs remain exactly 5, Optional Labs remain 5, and Source Expeditions remain 5. Exactly zero new Required Labs are created.

5. **Scientific Systems Measurement & Honest Judgment (M23):**
   Systems measurement is designed as a question-driven empirical discipline. It rejects all arbitrary universal constants (such as mandatory sample sizes of 30 or universal percentile mandates like p99). Workloads are matched to open or closed arrival models based on the specific engineering question; warm-up phases are applied conditionally only when the underlying mechanism or question requires it (e.g., cache or JIT warming vs. cold-start CLI benchmarking); coordinated-omission handling is evaluated when the arrival model specifies arrivals independent of service completion; and elapsed-duration measurement utilizes an appropriate monotonic or performance clock while recognizing that integer reporting units do not imply equivalent hardware clock resolution.
   Technology selection is governed by the 12 dimensions of Decision D-015. Recommending against adopting a technology ("do not add this technology") is explicitly designed as a fully valid, high-scoring engineering judgment.

6. **Capstone Defense Contract & Evidence Sufficiency (M24):**
   Module M24 serves purely as an integrative synthesis and architectural defense capstone. It introduces zero new core computing mechanisms. Learners defend their full-stack systems through 16 structured architectural traces and artifacts, supported by a 12-area evidence taxonomy. Evidence sufficiency is rigorously separated from naive benchmarking; formal specifications, source proofs, automated assertions, and reasoned uncertainty are recognized as valid engineering evidence.

---

## 2. Canonical Constraints & DAG Architecture

### 2.1 Stage 7 Structural DAG

```
                      [ M07 Virtual Memory / Isolation ]
                                    │
                                    ▼ (hard)
   [ M11 TLS / HTTP ] ────────► [ M21 Security I: Trust & Crypto ] ◄──────── [ M12 Web / Browser ]
          │          (hard)                │            (hard)                     │
          │                                │ (hard)                                │
          │                                ▼                                       │
          └─────────────────────► [ M22 Security II: Authn & Web ] ◄───────────────┘
                                           │
                                           │ (soft)
                                           ▼
   [ M20 Observability ] ───────► [ M23 Systems Thinking & Judgment ] ◄───── [ M17 Replication ] (soft)
          │          (hard)                │
          │                                │ (hard)
          ▼ (soft)                         ▼
   [                                M24 Final System Defense                                 ]
```

### 2.2 Reconciled Lesson Inventory (10 Lessons)

The 10 canonical lessons of Stage 7, their direct predecessor links, and their driving learner questions are defined as follows:

| Module | Lesson ID | Lesson Title / Driving Learner Question | Direct Predecessor Lessons | Core Pedagogical Focus |
|---|---|---|---|---|
| **M21** | `L21-01` | Where are the boundaries I must protect? | `L11-01` (TLS/HTTP), `L07-01` (Isolation), `L12-03` (Same-Origin) | Attack surfaces, threat modeling (STRIDE/dataflow), least privilege, ambient authority vs capability, system boundary inventory. |
| **M21** | `L21-02` | What do I use crypto for? | `L21-01` | Cryptographic primitives (Hash, MAC, Digital Signature, AEAD), symmetric vs asymmetric roles, key lifecycles, salt/nonce invariants, why plain fast hashes fail as password verifiers, PKI 6-layer model. Strictly crypto use, no primitive implementation. |
| **M22** | `L22-01` | How do I know who is calling? | `L21-02`, `L11-02` (HTTP Protocol) | Authn vs Authz, credentials vs identities, password hashing & verifiers (NIST SP 800-63B-4, RFC 9106, compute-hard PBKDF2), sessions vs bearer tokens, TeachingProfile-BearerV1 validation invariants, out-of-band token invalidation, OAuth 2.1 & OIDC architecture (RFC 9700 BCP). |
| **M22** | `L22-02` | Why is my web app vulnerable? | `L22-01`, `L12-03` (Browser Execution) | Code vs data injection (SQL, OS), parameterized API/driver contract, context-aware escaping, XSS taxonomy & CSP Level 3, CSRF mechanics & scenario-specific defense, SSRF anatomy & egress socket binding. |
| **M22** | `L22-03` | Why do I trust my dependencies? | `L22-02` | Software supply chain risks, dependency trees, typosquatting & malicious updates, 9-layer supply-chain separation (pinning, digest ownership, fetched-byte integrity, reproducibility, signatures, identity, SLSA v1.2 provenance). |
| **M23** | `L23-01` | How do I measure honestly? | `L20-01` (Observability), `L04-02` (Empirical Measurement) | Question-driven measurement, workload models (open vs closed), coordinated omission, warm-up criteria, distribution reporting (percentiles, median/IQR, mean/std when appropriate), monotonic clocks. |
| **M23** | `L23-02` | How do I pick a technology? | `L23-01` | Decision D-015 12 dimensions, evaluating vendor claims, technology rejection as passing outcome, bounded stable trade-offs (caching/Redis case), AI outputs as untrusted hypotheses. |
| **M23** | `L23-03` | What is the cost of my design? | `L23-02` | Systems cost modeling, compute/storage/memory/egress scaling, Fermi back-of-the-envelope estimation, latency vs dollar trade-offs, bottleneck identification & sensitivity analysis. |
| **M24** | `L24-01` | Can I defend an architecture? | `L23-02` | Capstone architecture defense conditional on actual system, 16 core architectural traces, 12 evidence areas, structured defense template, handling changed-constraint challenges, trade-off justification. |
| **M24** | `L24-02` | What should I measure before I ship? | `L24-01` | Pre-ship evidence planning, risk-prioritized verification matrix, defining what must be measured vs tested vs inspected vs explicit unknown, failure & rollback readiness with scenario cards. |

---

## 3. Research Findings Adopted, Rejected & Bounded

### 3.1 Adopted Research Findings

The architectural design incorporates all validated findings from `research/security-synthesis-judgment-m21-m24-v0.1.md` with strict normative grounding:

1. **NIST SP 800-63B-4 Password Storage Standard (Adopted):**
   Adopted the July 2025 Final recommendations (§3.1.1.2) with strict adherence to normative keyword levels:
   - Passwords SHALL be salted and hashed using a suitable password hashing scheme.
   - Salt SHALL be at least 32 bits (4 bytes) in length and chosen to minimize collisions. (Per NIST SP 800-63B-4, ordinary per-password salts are required to minimize collisions; they are not normatively specified as "unguessable" secrets).
   - Cost factor SHOULD be as high as practical without negatively impacting verifier performance and increased over time.
   - An approved scheme in the latest SP 800-132 or updated NIST password-hashing guidance SHOULD be used. Note: Current NIST SP 800-132 remains the December 2010 Final and specifies PBKDF2 (RFC 8018 / SP 800-132), which is compute-hard / time-hard, **NOT memory-hard**. While NIST decided in 2023 to revise SP 800-132 to add an additional memory-hard scheme, that revision is not yet a Final standard; modern memory-hard functions (such as Argon2id per RFC 9106 and scrypt per RFC 7914) are classified as RFC/industry current-practice candidates rather than a finalized NIST SP 800-63B-4 normative SHOULD.
   - Verifiers SHOULD permit a maximum password length of at least 64 characters (SHOULD, not SHALL). Truncation is forbidden. Single-factor passwords SHALL be at least 15 characters; MFA-backed passwords MAY be shorter but SHALL be at least 8 characters.
   - Traditional composition rules (mandatory uppercase, lowercase, numbers, symbols) and periodic forced password rotation are discarded as counter-productive.
   - Normative separation: Design maintains clear boundaries between the NIST baseline (normative SHALL/SHOULD requirements), RFC 9106 / RFC 7914 algorithm specifications and current-practice candidates, time-sensitive OWASP point-in-time practice recommendations, and library default settings. Iteration counts and memory costs are treated as configurable policy inputs with environment/workload rationale, eliminating any frozen universal design constant (e.g., 600,000 iterations).

2. **RFC 9846 TLS 1.3 Standards Track (Adopted):**
   Adopted RFC 9846 (published July 2026, Standards Track Proposed Standard), which obsoletes six RFCs (RFC 5077, RFC 5246, RFC 6961, RFC 7627, RFC 8422, and RFC 8446) and updates two RFCs (RFC 5705 and RFC 6066). It codifies TLS 1.3 as the modern secure channel:
   - Forward secrecy is scoped strictly to asymmetric key exchange modes (DHE / ECDHE) and PSK with (EC)DHE (`psk_dhe_ke`); PSK-only mode (`psk_ke`) does **not** provide forward secrecy, and 0-RTT early data does not provide general forward secrecy.
   - Removal of static RSA key exchange and obsolete ciphers, encrypted handshakes, and AEAD-only ciphersuites.
   - Strict certificate path validation when certificates are used (distinguishing certificate-based handshakes from pre-shared key handshakes).

3. **RFC 9525 Service Identity Verification (Adopted):**
   Adopted RFC 9525 (published **November 2023**, Standards Track Proposed Standard, obsoletes RFC 6125), establishing that TLS service identity validation MUST check Subject Alternative Names (`SAN: dNSName` or `SAN: iPAddress`) and MUST NOT fall back to Common Name (`CN`) in the Subject field.

4. **RFC 9700 / BCP 240 & OAuth 2.1 Specification Baseline (Adopted):**
   Adopted RFC 9700 (Best Current Practice 240, published January 2025) and `draft-ietf-oauth-v2-1-15` (March 2026 active Working Group draft):
   - PKCE (Proof Key for Code Exchange, RFC 7636) is a MUST for public clients and RECOMMENDED for confidential clients.
   - Resource Owner Password Credentials Grant (ROPC) is deprecated and MUST NOT be used.
   - Clients **SHOULD NOT** use the Implicit Grant except under the specific mitigation conditions outlined in BCP 240. (This preserves the exact BCP normative strength, distinguishing it from the draft OAuth 2.1 specification which completely omits the Implicit Grant).
   - Exact redirect URI string matching is mandatory.

5. **W3C Content Security Policy Level 3 Baseline (Adopted):**
   Adopted W3C CSP3 (Working Draft 29 July 2026):
   - Modern CSP deployment centers on nonce-based policies (`'nonce-{random}'`) and strict-dynamic (`'strict-dynamic'`) for script execution, rather than brittle domain allowlists.

6. **SLSA v1.2 Supply Chain Security Baseline (Adopted):**
   Adopted OpenSSF SLSA v1.2 specification (Approved, **24 November 2025**; v1.0 retired), establishing verifiable build provenance, tamper-evident signing, and the separation of source, build, and distribution integrity.

7. **Multi-Layer Separation Models (Adopted):**
   - **PKI Architecture:** Explicitly separated into 6 distinct conceptual layers:
     1. *Certificate Credential* (data structure holding public key and subject metadata);
     2. *Path Validation* (cryptographic verification of certificate chain against trust roots per RFC 5280);
     3. *Service Identity Binding* (verification that the certificate matches the intended DNS domain/IP per RFC 9525);
     4. *Proof of Private-Key Possession* (cryptographic challenge-response in TLS handshake proving possession of the private key);
     5. *Authentication* (determining the confirmed identity of the endpoint);
     6. *Authorization* (determining whether the confirmed identity has permission to perform the requested operation).
   - **Software Supply Chain:** Explicitly separated into 9 distinct integrity layers:
     1. *Resolution Pinning* (freezing dependency graph version ranges);
     2. *Expected Digest Ownership* (governing and storing trusted hashes in course or project lockfiles);
     3. *Fetched-Byte Integrity* (verifying downloaded payload hashes against trusted expected digests);
     4. *Signing Key Verification* (verifying cryptographic signatures over package archives);
     5. *Signer Identity Binding* (binding signing keys to authorized maintainer identities);
     6. *Build/Source Provenance* (recording the exact repository commit and builder identity);
     7. *Attestation Predicate* (evaluating the structured SLSA provenance attestation);
     8. *Trusted Builder* (evaluating the isolation and integrity of the build platform);
     9. *Verifier Policy* (determining whether an artifact meets deployment release gates).
     *Critical Boundary:* A cryptographic hash only detects mismatch against a trusted expected digest. If the expected digest or lockfile itself is maliciously modified, hash checking does not prevent package substitution.

### 3.2 Rejected Claims & Universal Truth Traps

This design formally rejects the following oversimplifications, false equivalences, and pseudo-standards:

1. **"HTTPS makes an application secure" (Rejected):**
   HTTPS provides confidentiality and integrity for data in transit across network hops. It provides zero protection against application-layer injection (SQLi), cross-site scripting (XSS), cross-site request forgery (CSRF), broken object-level authorization (BOLA), server-side request forgery (SSRF), or compromised server-side databases.

2. **"Encryption and Hashing are interchangeable" (Rejected):**
   Encryption is a two-way cryptographic transform intended to preserve confidentiality with reversible plaintext recovery via a secret key. A cryptographic hash function is a deterministic one-way mapping designed to satisfy preimage resistance, second-preimage resistance, and collision resistance, producing a fixed-size digest for integrity verification against a trusted expected digest. An unkeyed hash does not provide authenticity against an active adversary who can recompute the hash. Confusing them leads to fatal vulnerabilities (e.g., attempting to "decrypt" a hash or using unkeyed hashes where signatures or MACs are required).

3. **"Base64 is encryption" (Rejected):**
   Base64 is an open, reversible byte-to-text encoding format providing zero confidentiality, zero integrity, and zero security.

4. **"JWTs are inherently secure" (Rejected):**
   Unsigned JWTs (`alg: "none"`) provide zero integrity. Symmetric HMAC tokens signed with weak secrets are vulnerable to offline brute-force. Storing sensitive data in unencrypted JWT payloads leaks data because payloads are merely Base64URL-encoded. JWTs are bearer tokens: anyone in possession of the token has authority unless validated against audience, issuer, expiration, and revocation mechanisms.

5. **"Every system needs 30 benchmark runs and must optimize p99" (Rejected):**
   The "n = 30" heuristic is an introductory statistical rule of thumb that does not guarantee normality or statistical power for heavy-tailed, multimodal distributed systems. Percentile targets must be derived from user expectations and system constraints, not treated as dogmatic universal constants.

6. **"AI-generated code is authoritative or production-ready" (Rejected):**
   AI models generate plausibly structured text based on probabilistic patterns, not verified correctness or invariant preservation. AI-generated code, architectural recommendations, and security advice must be treated as untrusted hypotheses requiring rigorous empirical testing, static inspection, and formal verification.

7. **"Digital signatures provide absolute non-repudiation" (Rejected):**
   A digital signature only proves mathematical verification under a specific public key. Identity binding, key custody, host security, verifier policy, and operational context are required to make legal or procedural claims. Treating signature verification as equivalent to human identity attribution is a security flaw.

8. **"Software timer benchmarks prove constant-time code execution" (Rejected):**
   Hosted software timers on preemptible, cached, speculative operating systems cannot reliably prove constant-time execution or absence of micro-architectural side channels. The design mandates algorithmic timing mitigation (e.g., Python `hmac.compare_digest`, which is designed to prevent timing analysis by avoiding content-based short-circuiting while recognizing that length or type differences may still theoretically leak), not unverified claims of physical constant-time proof.

---

## 4. Recommended S7 Implementation Batches

To ensure focused execution, auditable review boundaries, and minimal blast radius, Stage 7 implementation is structured into **four sequential, bounded implementation batches**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Batch S7-B1: Module M21 (Security Synthesis I: Trust & Crypto Use)     │
│ - L21-01 (Threat Modeling & Boundaries)                                │
│ - L21-02 (Crypto Primitives & Roles: Hash, MAC, Signature, AEAD)       │
│ - Activity fixture: activity_l21_02.py (Localhost Crypto Roles & Misuse)│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Batch S7-B2: Module M22 (Security Synthesis II: Authn & Web Security)  │
│ - L22-01 (Authn vs Authz, Password Hashing & Verifiers, Sessions, OAuth)│
│ - L22-02 (Web Vulnerabilities: Injection, XSS, CSRF, SSRF)             │
│ - L22-03 (Software Supply Chain Security)                              │
│ - Activity fixtures: activity_l22_01.py & activity_l22_02.py           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Batch S7-B3: Module M23 (Systems Thinking & Judgment)                  │
│ - L23-01 (Honest Measurement, Open/Closed Workloads, Monotonic Clocks) │
│ - L23-02 (D-015 Technology Selection & Rejection)                      │
│ - L23-03 (Systems Cost & Scaling Estimation)                           │
│ - Activity fixtures: activity_l23_01.py & activity_l23_02.py           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Batch S7-B4: Module M24 (Final System Defense & Pre-Ship Assessment)   │
│ - L24-01 (Architectural Defense & Changed Constraints)                 │
│ - L24-02 (Pre-Ship Verification & Risk-Prioritized Evidence)           │
│ - Capstone Defense Rubric, Assessment Templates & Reviewer Contract    │
└────────────────────────────────────────────────────────────────────────┘
```

### Rationale for Four Batches

1. **Natural Architectural Separation:**
   - S7-B1 and S7-B2 form the security synthesis block. Splitting them between cryptographic foundations and primitive roles (M21) and credential verifiers, sessions, web composition, and supply chain (M22) keeps the security review surface manageable.
   - S7-B3 introduces empirical measurement, technology judgment, and cost modeling frameworks. It requires zero network security fixtures and focuses on quantitative reasoning.
   - S7-B4 integrates all preceding stages (S1–S7) into the final capstone defense. It introduces no new code or mechanisms, focusing entirely on synthesis, assessment rubrics, and the reviewer contract.

2. **Reviewable PR Sizes:**
   Dividing S7 into 4 batches prevents massive, unreviewable multi-thousand-line PRs, ensuring that the Web Lead can thoroughly audit code fixtures, test suites, and pedagogical prose at each boundary.

3. **Progressive Test & Fixture Isolation:**
   Each batch delivers exactly its own standard library `unittest` suite (`test_m21.py`, `test_m22.py`, `test_m23.py`, and `test_m24.py`), ensuring that CI remains green and regress-free across incremental deliveries.

---

## 5. Safe-Target Architecture Decision (Candidate B Acceptance & Refinement)

### 5.1 Architectural Evaluation & Formal Acceptance

In the S7 Research Dossier (`research/security-synthesis-judgment-m21-m24-v0.1.md`), two candidate hands-on approaches were evaluated:
- **Candidate A:** Pure static code review and conceptual vulnerability audits (zero running code).
- **Candidate B:** Bounded, course-owned localhost security test fixtures embedded inside standard lesson activity modules, paired with defense-focused security reviews of the Mini Cloud App.

**Decision: Candidate B is formally ACCEPTED AND REFINED.**

### 5.2 Safe-Target Refinement & Safety Bounds

To ensure strict compliance with Decision D-012, Candidate B is refined with the following non-negotiable boundaries:

1. **Course-Owned Localhost Fixtures Only:**
   - All executable security activities run strictly on local loopback sockets (`127.0.0.1` / `localhost`) using ephemeral, dynamically allocated OS ports.
   - No external network requests are permitted. No cloud environments, third-party sandboxes, or remote testbeds are contacted.

2. **Synthetic, Non-Sensitive Data Only:**
   - All credentials, tokens, cookies, database entries, and payloads used in hands-on activities are entirely synthetic, hardcoded strings (e.g., `"alice_test"`, `"password_synthetic_123"`, `"mock_jwt_token"`).
   - Zero real user secrets, production keys, or private certificates are ever utilized or stored.

3. **Strict Fix-and-Verify Pedagogical Stance:**
   - Activities NEVER ask learners to write offensive exploits, craft weaponized payloads, or execute attack automation.
   - Learners are provided with a minimally vulnerable localhost fixture (e.g., an unescaped SQL query string, an unvalidated redirect, or an unpinned hash check).
   - The learner's task is strictly:
     1. Observe the failure of the security invariant via an automated test assertion;
     2. Identify the root architectural flaw;
     3. Refactor the implementation to enforce defensive invariants (e.g., parameterize the SQL query, validate URL destinations, bind socket egress);
     4. Execute the verification suite to prove the vulnerability is mitigated without breaking functional specifications.

4. **Mini Cloud App Security Review Checkpoints:**
   Rather than introducing a separate, disjoint "vulnerable app" lab, security principles are integrated directly into the learner's longitudinal Mini Cloud App project at existing milestone checkpoints:
   - **Checkpoint P2 (Storage & Serialization Review):** Audit file storage permissions, path traversal risks, and data serialization integrity.
   - **Checkpoint P8 (RPC & Network Boundary Review):** Audit transport encryption, endpoint authentication, request size limits, and timeout protections.
   - **Checkpoint P9 (Deployment & Supply Chain Review):** Audit environment variable secrets handling, dependency version pinning, and container execution privileges.

5. **Canonical Lab and Expedition Map Invariance:**
   Lab and Expedition selections strictly audit against and preserve the accepted canonical architecture in `meta/blueprint/lab-source-selection-map-v0.1.md`:
   - **Required Labs (5):**
     - `LAB-REQ-01` — HTTP interface, origin, and intermediary trace — Module M11
     - `LAB-REQ-02` — xv6 `sleep`: user program through syscall entry — Module M06
     - `LAB-REQ-03` — POSIX threads race, rendezvous, and progress boundaries — Module M15
     - `LAB-REQ-04` — SQLite query plans, indexing, and workload evidence — Module M13
     - `LAB-REQ-05` — SQLite transactions, isolation, rollback, and recovery boundary — Module M14
   - **Optional Labs (5):**
     - `LAB-OPT-01` — CS:APP Data Lab, narrowed bit-representation slice — Module M01
     - `LAB-OPT-02` — Stanford CS144 Checkpoint 2, TCP receiver slice — Module M10
     - `LAB-OPT-03` — PostgreSQL `EXPLAIN` and transaction-isolation comparison — Modules M13/M14
     - `LAB-OPT-04` — Local OpenTelemetry trace and signal comparison — Module M20
     - `LAB-OPT-05` — OSTEP semaphore rendezvous, learner-directed external exercise — Module M15
   - **Source Expeditions (5):**
     - `EXP-01` — MIT PDOS xv6 utility-to-kernel path — Module M06
     - `EXP-02` — PostgreSQL planner and buffer route — Modules M13/M14
     - `EXP-03` — Chromium process and site-isolation path — Module M12
     - `EXP-04` — OpenTelemetry trace object path — Module M20
     - `EXP-05` — MIT 6.033 replication, transactions, and logging case — Modules M17/M18 (revisit M23)
   **Exactly ZERO new Required Labs are created in Stage 7.** Candidate B activities are strictly standard lesson hands-on exercises and Mini Cloud App review checkpoints.

---

## 6. Module M21 Architecture — Security Synthesis I: Trust & Crypto Use

### 6.1 Module Purpose & Capability Transition

Module M21 marks the transition from functional system construction to adversarial reasoning and cryptographic protection. Prior modules established how networks communicate (M10, M11), how processes isolate memory (M06, M07), how files persist to disk (M09), and how web browsers execute code (M12). M21 synthesizes these concepts under the assumption of an untrusted or adversarial environment.

The core capability transition of M21 is:
- **From:** Assuming endpoints, inputs, and storage are benign and well-behaved.
- **To:** Explicitly mapping trust boundaries, identifying unvalidated inputs, reasoning about attack surfaces, and correctly employing cryptographic primitives (hashes, MACs, digital signatures, AEAD) as opaque security building blocks without attempting to implement cryptographic algorithms.

### 6.2 Module Constraints & Invariants

1. **Crypto-Use Only (Zero Primitive Implementation & Zero Mock Stubs):**
   Under no circumstances do learners implement cryptographic primitives (e.g., writing custom AES, RSA, SHA-256, or HMAC algorithms). Learners use standard, vetted cryptographic libraries (`hashlib`, `hmac`, `secrets`, `ssl`, and optionally PyCA `cryptography` where available) to compose secure protocols. The design strictly prohibits educational mock RSA stubs or toy cipher implementations; where high-level primitives are unavailable, lessons rely on reference evidence and conceptual tracing.
2. **Concept Invariance:**
   `EC-CON-017 Trust Boundary` and `EC-CON-013 Isolation` maintain their first home in **M07 `L07-01`**. M21 conducts an adversarial revisit and synthesis across network, OS, and application boundaries.
3. **No Network Exploits:**
   Zero port scanning, packet sniffing, or remote penetration testing. All hands-on observation occurs on localhost loopback sockets with synthetic test data.

---

## 7. Lesson L21-01 Design — "Where are the boundaries I must protect?"

### 1. Target Mental Model
A computer system is not a monolith with a single perimeter; it is a composition of interacting components separated by distinct **trust boundaries**. A trust boundary exists wherever data, control, or execution crosses between domains of differing privilege, authority, or physical control. Security is not a property added at the end; it is the discipline of identifying every boundary, validating every incoming payload across that boundary, and minimizing the ambient authority granted to any single component.

### 2. Prerequisites
- Hard: `L11-01` (TLS & Transport Security), `L07-01` (Virtual Memory & Isolation Boundaries), `L12-03` (Web & Same-Origin Policy).
- Soft: `L09-01` (Filesystem Storage & Durability).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Judge, Explain, Diagnose`
- `Judge`: Evaluate system attack surfaces, privilege levels, and appropriate isolation mechanisms (process, container, VM, cryptographic boundary).
- `Explain`: Articulate the concept of a trust boundary and explain why security mechanisms must align with boundaries where authority, trust assumptions, or enforcement responsibility changes.
- `Diagnose`: Identify unvalidated inputs crossing boundaries, implicit trust assumptions, and privilege leakage.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-017 Trust Boundary`: Revisit (First home: M07 `L07-01`). Extended from OS memory isolation to network endpoints, inter-process communication, and multi-tenant applications.
- `EC-CON-013 Isolation`: Revisit (First home: M07 `L07-01`). Defense-in-depth mechanisms enforcing separation.

### 5. Learning Outcomes
- Identify and map trust boundaries across a multi-tier systems architecture (Hardware, OS Kernel, User Process, Network Transport, Application Logic, Browser Client).
- Classify threats using the STRIDE model (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) at specific boundary crossings.
- Contrast Ambient Authority with Capability-Based Security and Least Privilege.
- Audit data flow across a boundary and identify unvalidated inputs, canonicalization errors, and confused-deputy vulnerabilities.

### 6. Stable Principle
Never trust data across an authority boundary without explicit cryptographic or structural validation. Security resides in boundaries, not perimeters.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** Saltzer and Schroeder's *The Protection of Information in Computer Systems* (1975); Principle of Least Privilege, Economy of Mechanism, Complete Mediation, Open Design.
- **Implementation:** Linux process boundaries, file permission bits (`mode_t`), system call argument sanitization, POSIX `chroot` vs. Linux namespaces/cgroups.
- **Current Practice:** Zero Trust Architecture (NIST SP 800-207), Threat Modeling (STRIDE), Attack Surface Minimization, Sandboxing (gVisor, Firecracker, WebAssembly).

### 8. Required Distinctions / Misconceptions
- *Misconception:* Trust boundaries are identical to physical network boundaries (e.g., the firewall perimeter).
  *Reality:* Modern systems contain dozens of internal trust boundaries within the same physical machine, process, or local network (e.g., user space vs. kernel space, different microservices in the same subnet, tenant data in a shared database).
- *Misconception:* Authenticating an endpoint means all data from that endpoint is inherently safe.
  *Reality:* Authentication verifies identity; it does not validate that incoming payloads are semantically correct, un-tampered, or non-malicious. Validation must occur at every boundary crossing regardless of authentication status.
- *Misconception:* Encryption creates an impassable trust boundary on its own.
  *Reality:* Encryption protects confidentiality and integrity across untrusted transports, but endpoints possessing decryption keys must still enforce boundary validation on decrypted plaintext.

### 9. Worked Example
Learners examine a file storage service:
```
Client (Browser) ──[HTTP POST]──► API Gateway ──[Internal RPC]──► Storage Daemon ──[POSIX I/O]──► Disk
```
1. *Boundary Identification:*
   - Boundary 1: Client to API Gateway (Untrusted public network to DMZ).
   - Boundary 2: API Gateway to Storage Daemon (DMZ to internal service network).
   - Boundary 3: Storage Daemon to OS Kernel (User space to kernel space).
2. *Vulnerability Analysis:* The API Gateway authenticates the client but passes the filename parameter verbatim: `filename = request.json['path']`.
3. *Adversarial Payload:* A malicious client submits `filename = "../../etc/shadow"`.
4. *Failure Mode:* The Storage Daemon opens the path directly using POSIX `open()`. A path traversal vulnerability occurs because the trust boundary between the API Gateway and the Storage Daemon lacked input canonicalization and path confinement (`os.path.realpath` checking against an allowed base directory).

### 10. Bounded Hands-On / Observation
Learners analyze an architectural diagram and corresponding skeleton code in `labs/foundations/m21/activity_l21_01.py`:
1. Trace data flow from untrusted client input down to persistent storage.
2. Identify missing trust boundary enforcement points.
3. Add a path sanitization and boundary-check function that strictly rejects directory traversal (`../`), null-byte injection, and symlink escapes.
4. Run automated test cases asserting that attempts to escape the designated data directory raise handled security violations.

### 11. Evidence to Record
- Threat Model & Boundary Map: A Markdown table inventorying all system boundaries, data crossing each boundary, associated STRIDE threats, and mitigating controls.
- Trace log of path validation showing rejection of traversal payloads.

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Learner produces a complete boundary map and all automated test assertions in `activity_l21_01.py` pass.
- **BLOCKED:** Missing Python runtime or file permission errors in the temporary test directory.
- **NOT RUN:** Activity file not executed.

### 13. Progressive Support
- **Question:** If the API Gateway validates that `filename` does not contain `../`, why might the Storage Daemon still access an unauthorized file if the filesystem contains a symbolic link?
- **Hint 1:** When does symbolic link resolution happen?
- **Hint 2:** Does string validation on the filename detect what the underlying filesystem points to?
- **Expected Observation:** String checks only inspect syntax; `os.path.realpath()` resolves the actual target inode, revealing if a symlink escapes the boundary.
- **Full Explanation:** Syntactic validation of strings does not protect against filesystem-level indirection. Resolving paths to their canonical form (`realpath`) and ensuring the canonical path starts with the authorized base prefix is required to prevent symlink traversal attacks.

### 14. Required Visuals
- *Visual M21-V1:* Trust Boundary & Authority Map across Layers (Hardware, Kernel, Process, Network, Application, Storage).

### 15. Failure Modes
- Relying on client-side validation alone.
- Blacklisting specific malicious characters instead of whitelisting strict character sets.

### 16. Non-Goals
- Performing penetration testing against live networks or remote servers.
- Writing kernel exploit code or binary buffer overflows.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Standard library `unittest` suite checking that path sanitization blocks traversal attempts.
- Reviewer-Required: Inspection of learner's completed Threat Model & Boundary Map table.

### 18. Source Grounding with Currentness Classification
- **Saltzer & Schroeder (1975):** STABLE. Foundational principles of information protection.
- **NIST SP 800-207 (Zero Trust Architecture):** STABLE / CURRENT (August 2020). Core concepts of implicit trust zone elimination.
- **OWASP Threat Modeling Guidance:** CURRENT. STRIDE methodology.

---

## 8. Lesson L21-02 Design — "What do I use crypto for?"

### 1. Target Mental Model
Cryptography is not magic pixie dust that "makes data secure"; it is a set of specialized mathematical tools with precise, narrow guarantees. Encryption provides **confidentiality** (hiding plaintext from unauthorized observers). Cryptographic hashes provide **data integrity detection against a trusted expected digest** (detecting accidental corruption or verified against an out-of-band digest; plain unkeyed hashes do NOT authenticate against an active attacker who can recompute the hash). MACs provide **message authenticity and integrity** under a shared secret. Digital signatures provide **verification under a specific public key** (with identity attribution and non-repudiation depending on key custody, binding, and verifier policy). AEAD combines confidentiality and authenticity. Misusing cryptography (e.g., using fast unkeyed hashes for passwords, encrypting without authenticating, or reusing nonces) introduces catastrophic vulnerabilities.

### 2. Prerequisites
- Hard: `L21-01` (Trust Boundaries & Threat Modeling).
- Soft: `L11-01` (TLS & Transport Layer Security).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Explain, Judge, Learn-New-Tech`
- `Explain`: Differentiate the fundamental roles and guarantees of Hash, MAC, Digital Signature, and AEAD; explain why plain hashes lack authenticity and why unkeyed fast hashes fail as password verifiers.
- `Judge`: Select the correct cryptographic primitive for a given security requirement and reject dangerous misuse patterns (e.g., encrypt-without-authenticate, unkeyed hash for tamper detection against an active attacker, symmetric secret in client distribution).
- `Learn-New-Tech`: Navigate and evaluate modern cryptographic APIs (standard library `hashlib`, `hmac`, `secrets`, PyCA `cryptography`) adhering strictly to crypto-use and standard parameters.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-017 Trust Boundary`: Revisit (First home: M07 `L07-01`). Cryptographic mechanisms as transportable trust boundaries across untrusted channels.
- `EC-CON-007 Specification`: Revisit (First home: M02 `L02-03`). Cryptographic algorithms as mathematical specifications requiring exact adherence.

### 5. Learning Outcomes
- Classify cryptographic primitives into Hash, MAC, Digital Signature, and AEAD, defining the exact guarantees, inputs, keys, and failure modes of each.
- Explain why a cryptographic hash only detects corruption against a trusted expected digest, and prove that an active in-path adversary can recompute both data and unkeyed hash unless protected by a secret key (MAC) or private key (Digital Signature).
- Contrast symmetric cryptography (shared secret, fast, key distribution challenge) with asymmetric cryptography (keypair, public verification, private signing/decryption), analyzing forward secrecy per RFC 9846 (achieved in DHE/ECDHE handshake modes; absent in PSK-only modes).
- Explain why unkeyed fast hashes (e.g. SHA-256) are fundamentally inappropriate for password verification (rapid parallel evaluation on GPU/ASIC hardware) and explain why password verifiers require salts and tunable slow functions—separating compute-hard functions (like PBKDF2) from memory-hard functions (like Argon2id)—establishing the foundation for L22-01.
- Explain the role of `hmac.compare_digest` in mitigating timing analysis by avoiding content-based short-circuiting, noting that type and length differences may still theoretically leak under the Python API contract.

### 6. Stable Principle
Never roll your own crypto. Use standard, peer-reviewed primitives from reputable cryptographic libraries; in network protocol and application messaging contexts requiring confidentiality, pair encryption with authenticity (e.g., using AEAD or Encrypt-then-MAC) to prevent ciphertext malleability.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** FIPS 180-4 (SHA-2), FIPS 198-1 (HMAC, July 2008 Final; noting active NIST proposal to withdraw dated 23 June 2025 and transition to SP 800-224 Initial Public Draft of 28 June 2024), FIPS 186-5 (Digital Signatures), SP 800-38D (AES-GCM), RFC 9846 (TLS 1.3).
- **Implementation:** Python standard library `hashlib`, `hmac`, `secrets`, `ssl`; optional candidate package PyCA `cryptography`.
- **Current Practice:** Widespread adoption of AEAD ciphersuites (such as AES-GCM and ChaCha20-Poly1305) for modern transport and application payload encryption, ephemeral Diffie-Hellman key exchange for forward secrecy, deprecation of SHA-1 for signatures (NIST SP 800-131A Rev 2/3).

### 8. Required Distinctions / Misconceptions
- *Misconception:* An unkeyed SHA-256 hash proves that a message came from a trusted sender.
  *Reality:* An unkeyed hash provides zero sender authenticity. An attacker intercepting a message can modify the payload, recompute the SHA-256 digest, and send both to the recipient. Authenticity requires a secret: symmetric (HMAC) or asymmetric (Digital Signature).
- *Misconception:* Encryption guarantees that data has not been modified in transit.
  *Reality:* Unauthenticated ciphers (e.g., CBC or CTR mode without HMAC) are malleable; an attacker can manipulate ciphertext bits to alter plaintext without knowing the key. Authenticity requires AEAD (AES-GCM) or Encrypt-then-MAC.
- *Misconception:* Digital signatures provide unconditional non-repudiation.
  *Reality:* A digital signature proves mathematical verification under a specific public key. Proving who held the private key depends on key custody, binding, verifier trust policy, and system security.
- *Misconception:* Fast hashes like SHA-256 are suitable for storing passwords if salted.
  *Reality:* SHA-256 is designed for high-throughput stream processing; specialized parallel hardware (GPUs/ASICs) can evaluate massive candidate search spaces at negligible per-hash cost. Passwords require specialized slow functions—either compute-hard (such as PBKDF2) or memory-hard (such as Argon2id)—to impose significant computational and resource costs on offline dictionary and brute-force attacks (detailed in L22-01).

### 9. Worked Example
Learners evaluate integrity and authenticity mechanisms for an audit log pipeline:
1. *Unkeyed Hash:* The client computes `hashlib.sha256(log_entry).hexdigest()`. Vulnerability: An adversary modifying the log simply recomputes the digest. The receiver's hash check passes, falsely indicating integrity.
2. *Keyed MAC:* The client and server share a secret key; the client transmits `log_entry` along with `hmac.new(key, log_entry, hashlib.sha256).hexdigest()`. The adversary cannot forge a valid MAC without the key.
3. *Asymmetric Signature:* When multiple independent verifiers must validate log integrity without possessing the ability to create logs, the client signs with a private key (e.g., Ed25519) and verifiers check against the corresponding public key.

### 10. Bounded Hands-On / Observation
Learners run `labs/foundations/m21/activity_l21_02.py`:
1. Execute an unkeyed hash check; demonstrate that modifying the message and updating the digest passes verification, proving unkeyed hashes lack authenticity against active adversaries.
2. Verify message authenticity with HMAC; observe that tampering with the message or the MAC causes `verify_hmac()` to fail.
3. Inspect `hmac.compare_digest` usage for timing-safe comparison, observing that standard library APIs avoid content-based short-circuiting comparison loops without relying on noisy hosted software timers to claim physical constant-time proof.

### 11. Evidence to Record
- Cryptographic Primitive Selection Matrix (Scenario, Required security property, Correct primitive, Incorrect primitive trap, Non-guarantees).
- Adversary Model Trace comparing unkeyed Hash vs. HMAC under an active man-in-the-middle modification scenario.

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Activity test suite passes; learner correctly classifies primitive roles and demonstrates HMAC authentication over unkeyed hashes.
- **BLOCKED:** Missing standard library cryptographic modules.
- **NOT RUN:** Hands-on activity not executed.

### 13. Progressive Support
- **Question:** If Alice sends Bob a file along with its SHA-256 hash, under what exact conditions does Bob know the file was NOT modified in transit?
- **Hint 1:** Can Mallory modify both the file and the hash if they travel over the same untrusted channel?
- **Hint 2:** What if Bob received the expected hash over an authenticated out-of-band channel (e.g., in person or via HTTPS to a verified site)?
- **Expected Observation:** The hash only detects modification if Bob possesses a trusted expected digest obtained over an authenticated channel that Mallory could not modify.
- **Full Explanation:** An unkeyed cryptographic hash provides integrity detection strictly relative to a trusted expected digest. If the digest travels over the same untrusted channel as the message without authentication, an active attacker can replace both. Proving authenticity across an untrusted channel requires a keyed primitive (MAC or Digital Signature).

### 14. Required Visuals
- *Visual M21-V2:* Cryptographic Primitives Taxonomy: Hash vs. MAC vs. Digital Signature vs. AEAD (Axes: Keys, Transform, Security Guarantees, Non-Guarantees).
- *Visual M21-V3:* The 6-Layer PKI Trust and Verification Architecture (annotating scoped forward secrecy under RFC 9846).

### 15. Failure Modes
- Attempting to implement custom XOR encryption or custom hashing algorithms.
- Reusing nonces in symmetric AEAD encryption.

### 16. Non-Goals
- Implementing mathematical number theory for RSA, elliptic curves, or lattice cryptography.
- Conducting live cryptanalysis or side-channel power analysis.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Standard library `unittest` suite (`test_m21.py`) validating HMAC tamper detection, unkeyed hash tamper demonstration, and `compare_digest` integration.
- Reviewer-Required: Inspection of learner's Cryptographic Primitive Selection Matrix.

### 18. Source Grounding with Currentness Classification
- **FIPS 198-1 (July 2008 Final) / NIST SP 800-224 (Initial Public Draft 28 June 2024):** STABLE / CURRENT. The Keyed-Hash Message Authentication Code (HMAC), noting NIST's 23 June 2025 proposal to withdraw FIPS 198-1 and transition HMAC to SP 800-224.
- **FIPS 186-5 / SP 800-38D:** STABLE. Digital signatures and AES-GCM authenticated encryption.
- **RFC 9846 (TLS 1.3):** STABLE / CURRENT (July 2026). Obsoletes RFC 8446, 5246, 5077, 6961, 7627, 8422; updates RFC 5705, 6066. Forward secrecy scoped to DHE/ECDHE key exchange.

---

## 9. M21 Hands-On Fixture Contract — Localhost Cryptographic Roles & Misuse Boundaries (`activity_l21_02.py`)

### 9.1 Purpose & Execution Scope
The fixture `activity_l21_02.py` provides an isolated, localhost-only environment to experiment with cryptographic primitive roles (Hash vs. MAC vs. Signature vs. AEAD) and timing-safe comparisons. It contains zero external network dependencies and uses standard Python standard library modules (`hashlib`, `hmac`, `secrets`). (Password hashing storage schemas and verifiers are owned by M22 `L22-01`).

### 9.2 Fixture File Structure
- Implementation: `labs/foundations/m21/activity_l21_02.py`
- Verification Suite: `labs/foundations/m21/test_m21.py` (Standard library `unittest` suite; capability-gates `pytest`)

### 9.3 Invariants & Interface Contract
1. **Cryptographic Roles Contract:**
   The fixture provides explicit verification helpers:
   ```python
   def compute_unkeyed_hash(data: bytes) -> str:
       return hashlib.sha256(data).hexdigest()

   def verify_unkeyed_tamper(data: bytes, expected_hash: str) -> bool:
       return compute_unkeyed_hash(data) == expected_hash

   def compute_hmac(key: bytes, data: bytes) -> str:
       return hmac.new(key, data, hashlib.sha256).hexdigest()

   def verify_hmac(key: bytes, data: bytes, expected_mac: str) -> bool:
       computed = compute_hmac(key, data)
       return hmac.compare_digest(computed, expected_mac)
   ```
2. **Timing-Safe Comparison Contract:**
   The fixture uses `hmac.compare_digest` to avoid content-based short-circuiting in MAC comparisons. It explicitly notes that software benchmarks on shared OS kernels cannot prove physical constant-time execution and that type/length differences may still theoretically leak; the learning goal is adhering to the language runtime's timing-mitigation API contract.
3. **Safety & Ephemeral Guarantees:**
   - Operates entirely in memory with synthetic test byte strings.
   - Zero hardcoded real secrets, private keys, or certificates.

---

## 10. Module M22 Architecture — Security Synthesis II: Authn/Authz & Secure Composition

### 10.1 Module Purpose & Capability Transition

Module M22 addresses the complex challenge of composition in multi-tier applications, web environments, and external dependency ecosystems. Where M21 established trust boundaries and cryptographic tools, M22 applies them to the operational realities of software systems:
- Verifying who is calling and what they are allowed to do (Authentication, Password Verifiers, and Authorization);
- Preventing application-layer composition failures across disparate parsers and interpreters (Injection, XSS, CSRF, SSRF);
- Verifying the integrity and provenance of third-party dependencies composing the modern software supply chain.

The core capability transition of M22 is:
- **From:** Treating authentication as a single login check, assuming client input matches expected formats, and blindly trusting installed third-party libraries.
- **To:** Designing decoupled, defense-in-depth authorization pipelines, eliminating injection vulnerabilities at the API/driver interface layer, implementing robust web security controls, and auditing dependency graphs with cryptographic pinning and provenance.

### 10.2 Module Constraints & Invariants

1. **Strict Defense-First Fix-and-Verify Stance (Decision D-012):**
   Zero exploit development, zero weaponized payload distribution, and zero offensive scanning. Exercises present bounded, reproducible code vulnerabilities on localhost; learners inspect the failure, apply the structural defensive fix, and verify immunity using automated tests.
2. **Safe Localhost Execution & Fail-Closed Teardown:**
   All web server and client interactions run exclusively on `127.0.0.1` using ephemeral ports. Fixture teardowns must explicitly join threads and verify that listener sockets are released.
3. **Normative Source Grounding:**
   Adhere strictly to NIST SP 800-63B-4, RFC 9700 (BCP 240, OAuth 2.0 Security Best Current Practice: ROPC MUST NOT, Implicit SHOULD NOT), `draft-ietf-oauth-v2-1-15` (OAuth 2.1), W3C CSP Level 3, and OpenSSF SLSA v1.2.

---

## 11. Lesson L22-01 Design — "How do I know who is calling?"

### 1. Target Mental Model
Security requires separating **Authentication** (Authn: proving *who* an entity is) from **Authorization** (Authz: determining *what* that entity is permitted to do). A credential is an authenticating artifact; an identity is the entity associated with that credential; an authorization policy evaluates the identity, the target resource, and the requested action. In application systems, credentials begin with password verifiers (where servers verify secret knowledge without storing plaintext passwords) and transition to session identifiers or cryptographically signed bearer tokens. Authorization must be verified independently at every resource boundary, distinguishing between stateful server-side sessions, stateless bearer tokens, and OAuth authorization delegations.

### 2. Prerequisites
- Hard: `L21-02` (Cryptographic Primitives & Digital Signatures), `L11-02` (HTTP Protocol & State).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Judge, Explain`
- `Judge`: Evaluate authentication and authorization architectures (password storage policies, stateful sessions vs. signed bearer tokens, RBAC vs. ABAC) against operational complexity, revocation latency, and security trade-offs.
- `Explain`: Clearly explain the distinction between Authentication (verifying identity) and Authorization (evaluating authority); explain the mechanics of password verifier storage, token validation profiles, and OAuth 2.1 authorization flows.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-017 Trust Boundary`: Revisit (First home: M07 `L07-01`). Examined at credential verifiers, API gateways, identity providers (IdPs), and resource servers.
- `EC-CON-007 Specification`: Revisit (First home: M02 `L02-03`). Token schemas, claims validation profiles, and password storage standards.

### 5. Learning Outcomes
- Distinguish Authentication from Authorization across real-world request lifecycles.
- Design and evaluate secure password verifiers complying with NIST SP 800-63B-4: enforce salts (>= 32 bits, chosen to minimize collisions per NIST SHALL), evaluate compute-hard functions (PBKDF2 per RFC 8018 / SP 800-132 Final 2010; revision planned) and memory-hard current-practice candidates (Argon2id per RFC 9106, scrypt per RFC 7914), format verifier records (`algo$params$salt$hash`), and mitigate timing attacks using `hmac.compare_digest` to avoid content-based short-circuiting.
- Contrast stateful server-managed sessions (cookies + database/cache lookup) with stateless cryptographically signed bearer tokens, articulating why stateless token invalidation requires out-of-band state changes (short lifespans, revocation lists, epoch bumping, session store lookup).
- Implement token validation against a named profile (`TeachingProfile-BearerV1`): enforce required claims (`alg`, `exp`, `sub`), reject `alg: "none"`, verify signatures under configured verifier policy, and validate `aud` to prevent token substitution across services.
- Diagram the OAuth 2.1 authorization code flow with PKCE per RFC 9700 (BCP 240) and explain why PKCE is required for public clients.

### 6. Stable Principle
Never confuse possessing a credential with possessing authority. Every protected endpoint must independently verify both identity and specific resource authorization on every request.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** NIST SP 800-63B-4 (Password Storage), NIST SP 800-132 (PBKDF2, Dec 2010 Final; revision planned), RFC 9106 (Argon2), RFC 7914 (scrypt), RFC 8018 (PKCS #5 / PBKDF2), RFC 6749 (OAuth 2.0 core), RFC 7636 (PKCE), RFC 7519 (JWT), RFC 8725 (JWT BCP), RFC 9700 (BCP 240), `draft-ietf-oauth-v2-1-15` (OAuth 2.1).
- **Implementation:** Python standard library `hashlib`, `hmac`, `secrets`, `base64`, `json`; session middleware, API gateway auth interceptors.
- **Current Practice:** OAuth 2.1 deprecation of ROPC (MUST NOT) and Implicit Grant (BCP 240: SHOULD NOT; OAuth 2.1 draft: removed); mandatory PKCE; industry adoption of memory-hard password hashing (Argon2id per RFC 9106) alongside compute-hard PBKDF2; short-lived access tokens paired with revocable refresh tokens; fine-grained ABAC / Zanzibar-style relationship-based access control.

### 8. Required Distinctions / Misconceptions
- *Misconception:* Hashing a password with SHA-256 makes it secure for storage.
  *Reality:* SHA-256 is an unkeyed fast hash designed for high-throughput data integrity. Massively parallel GPU/ASIC hardware can evaluate fast hashes at high rates; the exact rate depends on the algorithm, implementation, hardware, and date. Password verifiers require salts (>= 32 bits and chosen to minimize collisions under the current NIST baseline) and tunable slow functions: compute-hard functions such as PBKDF2 per SP 800-132, or memory-hard current-practice candidates such as Argon2id per RFC 9106.
- *Misconception:* PBKDF2 is a memory-hard password hashing function.
  *Reality:* PBKDF2 is compute-hard (iteration-hard), but requires minimal memory, allowing parallelized ASIC implementation. True memory-hard functions (Argon2id per RFC 9106, scrypt per RFC 7914) require significant RAM per evaluation, resisting hardware acceleration.
- *Misconception:* A valid JWT signature proves the token was issued by a trusted IdP and that the user is authorized.
  *Reality:* A valid signature only proves mathematical verification under a key selected by verifier policy. Trust and issuer identity binding require explicit verifier validation (`iss`, `aud`, key-pinning policy). Furthermore, the application must still check resource authorization (preventing IDOR/BOLA).
- *Misconception:* Stateless JWTs can be revoked instantly without server-side state.
  *Reality:* Stateless tokens cannot be revoked before expiration without out-of-band verification state (revocation lists, epoch bumping, or session store lookups).

### 9. Worked Example
Learners trace two authentication and authorization mechanisms:
1. *Password Verifier Lifecycle:*
   - Registration: System generates a per-credential salt (at least 32 bits to minimize collisions, e.g., `secrets.token_bytes(16)`) and derives hash via slow KDF; stores formatted string: `pbkdf2_sha256$iterations=200000$salt_hex$hash_hex`.
   - Authentication: Server extracts salt and iterations from stored verifier, computes hash of candidate password, and compares using `hmac.compare_digest`.
2. *Token Profile Validation (`TeachingProfile-BearerV1`):*
   - Incoming request: `GET /api/documents/1042` with header `Authorization: Bearer <token>`.
   - Pipeline:
     1. Unpack token; reject if `alg == "none"` or mismatched from expected profile algorithm (`HS256` reference or `RS256`);
     2. Cryptographically verify signature against verifier's trusted key;
     3. Validate temporal claim: `exp > now`;
     4. Validate audience: `aud == "document-service"`;
     5. Authorization check: Query authorization policy to verify whether `sub` (authenticated user) has `read` permission on document `1042`.

### 10. Bounded Hands-On / Observation
Learners interact with `labs/foundations/m22/activity_l22_01.py`:
1. Implement a password verifier formatting and validation routine with unique salt generation and `hmac.compare_digest`.
2. Implement `TeachingProfile-BearerV1` validator in pure Python standard library (`hmac`, `hashlib`, `json`, `base64`), enforcing required claims (`alg`, `exp`, `sub`, `aud`).
3. Verify that forged signatures, expired tokens, wrong audiences, and `alg: "none"` are deterministically rejected.

### 11. Evidence to Record
- Password Storage Compliance Record (Salt source, Salt length >= 32 bits, Hash algorithm, Cost parameter rationale, Timing comparison API).
- Token Profile Validation Matrix (`TeachingProfile-BearerV1`: claim name, required vs. optional, validation rule, failure status code).

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Validator passes automated unit tests, rejecting all invalid/forged/expired tokens and password verifier mismatches.
- **BLOCKED:** Missing standard library cryptographic modules.
- **NOT RUN:** Hands-on code exercise omitted.

### 13. Progressive Support
- **Question:** If an attacker intercepts a signed token issued for `service-billing.example.com`, why might they be able to use it against `service-admin.example.com` if audience verification is omitted?
- **Hint 1:** Both services trust the same identity provider signing key.
- **Hint 2:** The signature is mathematically valid. What claim specifies which service the token was issued for?
- **Expected Observation:** Because the signature verifies successfully under the shared key, the admin service accepts the token unless it explicitly verifies that `aud` matches its own service identifier.
- **Full Explanation:** Signature verification only proves that the token was signed by the holder of the private/shared key. Omitting the `aud` (Audience) check allows token substitution attacks across services. The recipient must enforce `aud == expected_service_id`.

### 14. Required Visuals
- *Visual M22-V1:* Authentication vs. Authorization Request Decision Path.
- *Visual M22-V2:* OAuth 2.1 Authorization Code Flow with PKCE Architecture.

### 15. Failure Modes
- Checking user permissions based solely on user-supplied URL parameters without validating against the authenticated identity.
- Storing unsalted password hashes or using fast unkeyed hashes for password verification.

### 16. Non-Goals
- Deploying a live identity provider such as Keycloak, Okta, or Active Directory.
- Implementing biometric or hardware FIDO2/WebAuthn authenticators.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Standard library `unittest` suite asserting password verifier correctness, salt uniqueness, timing-mitigation comparison (`hmac.compare_digest`), and token profile rejection for tampering, expiration, wrong audience, and `alg: "none"`.
- Reviewer-Required: Inspection of learner's explanation of stateless token revocation trade-offs and password storage policy rationale.

### 18. Source Grounding with Currentness Classification
- **NIST SP 800-63B-4 §3.1.1.2:** CURRENT (Final July 2025). Passwords SHALL be salted (salt >= 32 bits chosen to minimize collisions) and hashed using an approved scheme per SP 800-132 (currently PBKDF2 compute-hard; revision planned) or updated NIST guidance; cost factor SHOULD be as high as practical and increased over time; verifiers SHOULD permit max length >= 64 characters without truncation; single-factor min 15 chars, MFA min 8 chars; Argon2id (RFC 9106) evaluated as an IETF/industry current-practice candidate.
- **NIST SP 800-132:** CURRENT (December 2010 Final; revision planned). Recommendation for Password-Based Key Derivation (PBKDF2 compute-hard).
- **RFC 9106 (Argon2):** STABLE. Standard memory-hard password hashing (current-practice candidate).
- **RFC 9700 / BCP 240:** CURRENT (January 2025). OAuth 2.0 Security BCP: PKCE MUST for public, RECOMMENDED for confidential; ROPC MUST NOT; Implicit Grant SHOULD NOT; redirect URI exact matching.
- **draft-ietf-oauth-v2-1-15:** CURRENT (March 2026 active draft). Consolidated OAuth 2.1 specification.
- **RFC 7519 / RFC 8725:** STABLE. JSON Web Token (JWT) specification and Security Best Current Practices.

---

## 12. Lesson L22-02 Design — "Why is my web app vulnerable?"

### 1. Target Mental Model
Web applications bridge disparate execution environments (browsers, network protocols, web servers, databases, operating system shells). Vulnerabilities arise at **composition boundaries** when data from an untrusted source is concatenated directly into a structured command, markup, or query stream, causing the receiving interpreter to confuse **data** with **code**. Eliminating vulnerabilities requires structural separation: parameterized queries, context-aware output encoding, strict content execution policies, and explicit network egress validation.

### 2. Prerequisites
- Hard: `L22-01` (Authentication & Authorization), `L12-03` (Web & Same-Origin Policy).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Diagnose, Judge, Explain`
- `Diagnose`: Identify code-versus-data mixing in SQL queries, HTML rendering, and network egress calls.
- `Judge`: Evaluate trade-offs between mitigation strategies (parameterized queries vs. ORMs; CSP nonces vs. hashes; SameSite cookie attributes vs. anti-CSRF synchronizer tokens; network egress socket binding vs. proxy allowlists).
- `Explain`: Explain why string concatenation across composition boundaries fails, and explain how structural separation prevents injection at the API/driver interface layer.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-017 Trust Boundary`: Revisit (First home: M07 `L07-01`). The boundary between application business logic and underlying interpreters (SQL engine, HTML parser, OS shell, network stack).
- `EC-CON-009 Correctness`: Revisit (First home: M02 `L02-03`). Correctness under active adversarial payload injection.

### 5. Learning Outcomes
- Explain how SQL Injection occurs via string concatenation and prove why parameterized queries (prepared statements) structurally eliminate SQLi by using driver/API contracts that treat parameters strictly as value literals, separating data from syntax (noting that specific AST and bytecode compilation mechanics depend on the database engine).
- Classify Cross-Site Scripting (XSS) into Stored, Reflected, and DOM-based types, and specify defenses using context-aware encoding and W3C CSP Level 3 nonce policies.
- Contrast Cross-Site Request Forgery (CSRF) ambient cookie authority with explicit bearer token authority, and implement multi-layered defenses: `SameSite` cookies, Origin/Referer verification, and anti-CSRF synchronizer tokens.
- Deconstruct Server-Side Request Forgery (SSRF) and design a secure HTTP client enforcing URL parsing, IP destination allowlists, DNS rebinding mitigation, and connection socket address binding before sending request bytes.

### 6. Stable Principle
Never concatenate untrusted input into an interpreter stream. Maintain strict structural separation between code instructions and user data at every architectural layer.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** SQL ISO/IEC 9075, W3C Content Security Policy Level 3 (Working Draft 29 July 2026; active working draft), WHATWG HTML / Fetch Living Standards, RFC 6265bis / `draft-ietf-httpbis-layered-cookies-02` (May 2026 active Internet-Draft).
- **Implementation:** Python `sqlite3` parameterized queries (`?`), Jinja2 autoescaping, HTTP response headers (`Content-Security-Policy`, `Set-Cookie: SameSite=Lax; Secure; HttpOnly`).
- **Current Practice:** Nonce-based CSP (`'strict-dynamic'`), automated static analysis (SAST), ORM parameterized abstractions, defense against DNS rebinding via post-resolution socket connection inspection.

### 8. Required Distinctions / Misconceptions
- *Misconception:* Escaping single quotes with regex makes SQL queries safe against injection.
  *Reality:* Ad-hoc blacklists and string replacing fail against alternative encodings, numeric injections, and second-order injections. Only parameterized prepared statements guarantee that user input is handled strictly as data literals by the driver and database engine.
- *Misconception:* An application using `SameSite=Lax` cookies is completely immune to CSRF.
  *Reality:* `SameSite=Lax` allows cookies on top-level GET navigations. If a server performs state mutations on GET requests, it remains vulnerable to CSRF. Furthermore, older browsers or misconfigured subdomains can bypass `Lax`. Defense-in-depth requires checking `Origin`/`Referer` headers or using anti-CSRF tokens.
- *Misconception:* Validating that a URL begins with `https://api.example.com` protects against SSRF.
  *Reality:* Attackers exploit URL parser ambiguities (e.g., `https://api.example.com@169.254.169.254` or userinfo tricks), DNS rebinding (where the domain resolves to an internal IP on the second lookup), or redirect following.

### 9. Worked Example
Learners examine a vulnerable Python web handler:
```python
# Vulnerable SQL Concatenation:
cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'")
```
Learners observe how an input like `admin' --` truncates the SQL statement, bypassing password verification.
Learners refactor the code to use parameterized execution:
```python
# Secure Parameterized Query:
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_hash))
```
The database engine parses the SQL syntax and builds the AST *before* binding the parameters, treating the input strictly as a literal string value regardless of its contents.

### 10. Bounded Hands-On / Observation
Learners run `labs/foundations/m22/activity_l22_02.py`, hosting an ephemeral localhost HTTP server:
1. **Part 1 (SQLi):** Inspect a failing query test where malicious input extracts unauthorized records; refactor to parameterized queries and verify test passes.
2. **Part 2 (CSRF):** Inspect a state-changing POST endpoint that relies only on session cookies; add `SameSite=Lax`, verify the `Origin` header, and implement an anti-CSRF token verification check.
3. **Part 3 (SSRF):** Inspect a webhook fetcher; implement a safe fetcher that resolves DNS, validates that the destination IP is not private/loopback/link-local (RFC 1918 / RFC 3927), and connects directly to the validated IP.

### 11. Evidence to Record
- Vulnerability Mitigation Matrix (Vulnerability class, Root cause mechanism, Broken invariant, Structural fix, Verification assertion).
- Automated test output proving all 3 defensive refactorings pass regression checks.

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** All unit and integration tests in `test_m22.py` pass; learner demonstrates correct parameterization, CSRF protection, and SSRF socket egress validation.
- **BLOCKED:** Localhost port binding failure.
- **NOT RUN:** Hands-on activity omitted.

### 13. Progressive Support
- **Question:** Why is resolving a hostname to check its IP address before calling `urllib.request.urlopen(url)` insufficient to prevent SSRF against internal cloud metadata services?
- **Hint 1:** What happens between the time your code resolves the DNS name and the time `urlopen()` opens the TCP socket?
- **Hint 2:** Could a malicious DNS server return a public IP for the first query and `169.254.169.254` for the second query?
- **Expected Observation:** This is a Time-of-Check to Time-of-Use (TOCTOU) race condition called DNS Rebinding.
- **Full Explanation:** If the DNS record has a TTL of 0, the operating system or HTTP library will perform a second DNS resolution when establishing the actual socket connection. To prevent DNS rebinding, the application must resolve DNS once, validate the resulting IP against an IP blocklist, and open the socket directly to that validated IP address, passing the original domain name only in the HTTP `Host` header and TLS SNI.

### 14. Required Visuals
- *Visual M22-V3:* Code vs. Data: AST Parsing Boundary in SQL Queries.
- *Visual M22-V4:* Browser Vulnerabilities & Defensive Boundaries (XSS, CSRF, SSRF).

### 15. Failure Modes
- Attempting to sanitize input by removing `<script>` tags using regular expressions (easily bypassed by `<img src=x onerror=...>`).
- Relying on client-side JavaScript validation for security enforcement.

### 16. Non-Goals
- Exploiting live web servers or running penetration testing tools (sqlmap, Burp Suite, Zap).
- Writing complex browser exploit chains or zero-day memory corruptions.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: `pytest labs/foundations/m22/test_m22.py` validating SQL parameterization, CSRF token validation, and SSRF IP blocking.
- Reviewer-Required: Inspection of learner's architectural description of SSRF DNS rebinding defense.

### 18. Source Grounding with Currentness Classification
- **W3C Content Security Policy Level 3:** CURRENT / FRONTIER (Working Draft 29 July 2026; active working draft). Modern nonce-based script execution.
- **draft-ietf-httpbis-layered-cookies-02 / RFC 6265bis:** CURRENT / FRONTIER (active Internet-Draft, May 2026). SameSite cookie semantics (`Strict`, `Lax`, `None`) and layered cookie boundaries limiting ambient authority; distinguishes draft churn from stable browser mechanisms.
- **OWASP Top 10 (2021/2025):** STABLE / CURRENT. Injection, Broken Access Control, SSRF taxonomy.

---

## 13. Lesson L22-03 Design — "Why do I trust my dependencies?"

### 1. Target Mental Model
Modern software applications are composed predominantly of third-party libraries and transitive dependencies. Installing a dependency grants that code the exact same execution privileges, filesystem access, network authority, and memory access as the host application. Securing the **software supply chain** requires moving from blind trust to explicit, cryptographic verification: pinning exact versions and artifact hashes, verifying signatures and provenance attestations (SLSA v1.2), minimizing dependency count, and isolating build/execution environments.

### 2. Prerequisites
- Hard: `L22-02` (Web Application Security & Composition).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Learn-New-Tech, Judge`
- `Learn-New-Tech`: Master dependency management tools, lockfile specifications, cryptographic hash pinning, and SLSA v1.2 provenance formats.
- `Judge`: Evaluate risk-versus-utility of external dependencies, assess supply-chain attack surfaces, and formulate dependency adoption/retention policies.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-017 Trust Boundary`: Revisit (First home: M07 `L07-01`). The boundary between developer code and external third-party open-source code.
- `EC-CON-008 Invariant`: Revisit (First home: M02 `L02-03`). Immutability of pinned cryptographic digests.

### 5. Learning Outcomes
- Analyze how dependency trees expand attack surfaces through transitive dependencies and ambient execution hooks (e.g., `setup.py` / post-install scripts).
- Deconstruct supply-chain attack vectors: typosquatting, dependency confusion (internal vs. public package names), account takeovers, and unmaintained vulnerabilities.
- Implement the 6-layer supply-chain separation model: Version Pinning, Cryptographic Hash Pinning, Build Reproducibility, Signature Verification, Signer Identity Binding, and Provenance Attestation (SLSA v1.2).
- Inspect a lockfile (`poetry.lock`, `package-lock.json`, or `requirements.txt` with `--require-hashes`) and prove how hash pinning defeats upstream package substitution.

### 6. Stable Principle
Every dependency added to a project is code you run with full process privileges. Do not import code whose integrity, source, and maintenance you cannot verify.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** OpenSSF SLSA v1.2 (Approved, September 2024), PEP 508 (Dependency specification for Python), PEP 440 (Version identification).
- **Implementation:** `pip` hash-checking mode (`--require-hashes`), `pip-audit`, CycloneDX / SPDX SBOM generators.
- **Current Practice:** Automated vulnerability scanning (Dependabot/Renovate), Sigstore keyless signing (cosign), verifiable SLSA build provenance attestations, isolated ephemeral CI build runners.

### 8. Required Distinctions / Misconceptions
- *Misconception:* Version pinning (e.g., `requests==2.31.0`) guarantees the exact same code is installed every time.
  *Reality:* Version numbers in public package repositories can be yanked, re-uploaded (in unmanaged repos), or vulnerable to dependency confusion. Only cryptographic SHA-256 digest pinning guarantees byte-for-byte immutability.
- *Misconception:* Open-source software is safe because "many eyeballs make all bugs shallow."
  *Reality:* Most open-source libraries are maintained by volunteers; obscure or deeply nested transitive dependencies receive minimal auditing, making them prime targets for malicious takeovers.
- *Misconception:* Running `pip install` only executes code when the library is imported.
  *Reality:* Legacy build tools and package setup scripts (like `setup.py`) execute arbitrary Python code *during* the installation process.

### 9. Worked Example
Learners inspect an incident where an internal private package named `company-auth-utils` is installed by CI.
If the package index configuration does not strictly separate private indices from the public PyPI index, an attacker can register `company-auth-utils` on public PyPI with a higher version number (`99.0.0`), causing `pip` to prioritize and download the malicious public package (Dependency Confusion).
Learners trace how strict package index pinning, private namespace scoping, and cryptographic hash verification prevent this vulnerability.

### 10. Bounded Hands-On / Observation
Learners analyze a small project directory containing a `requirements.txt` and a lockfile:
1. Identify unpinned and loosely pinned dependencies (e.g., `pkg >= 1.0`).
2. Run a script that simulates package tampering by modifying a single byte in a mock package archive; demonstrate that standard unhashed installs accept the corrupted file, while `--require-hashes` immediately aborts the installation.
3. Construct an SBOM (Software Bill of Materials) inventory for a minimal project.

### 11. Evidence to Record
- Dependency Risk Audit Table (Direct dependency, Transitive count, Hash pinning status, Known vulnerabilities, Maintenance status).
- Verification log demonstrating `pip --require-hashes` rejecting a mismatched digest.

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Learner successfully constructs a hash-pinned dependency specification and proves that tampered digests are rejected.
- **BLOCKED:** Missing file permission to create temporary virtual environments.
- **NOT RUN:** Hands-on exercise skipped.

### 13. Progressive Support
- **Question:** Why does signing a Git commit with a developer's GPG/SSH key fail to prove that the resulting binary package on PyPI matches that source code?
- **Hint 1:** Where does the binary package get built and uploaded?
- **Hint 2:** Can a developer's laptop or CI runner build something different from what was committed to Git?
- **Expected Observation:** Source signatures only attest to the text in Git; they do not attest to the integrity of the build pipeline, the build dependencies, or the uploaded artifact.
- **Full Explanation:** This is the core insight behind SLSA (Supply-chain Levels for Software Artifacts). To establish trust from source to deployment, a system requires verifiable build provenance attestations generated by an isolated, authenticated build platform (SLSA v1.2), binding the specific source revision and builder identity to the resulting artifact digest. Note that cryptographic hashes only verify integrity against trusted expected digests; if the expected digest in a lockfile is itself compromised, hash checks cannot detect the malicious origin.

### 14. Required Visuals
- *Visual M22-V5:* The 6-Layer Software Supply Chain Integrity Model (Pinning → Digests → Reproducibility → Signatures → Identities → Provenance).

### 15. Failure Modes
- Adding heavy third-party packages for trivial tasks (e.g., left-pad syndrome).
- Disabling hash checks or certificate checks to bypass installation warnings.

### 16. Non-Goals
- Implementing a full package registry or mirrors.
- Writing custom cryptographic signature formats.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Automated test verifying that lockfile parser validates SHA-256 hashes.
- Reviewer-Required: Inspection of learner's dependency risk evaluation methodology.

### 18. Source Grounding with Currentness Classification
- **OpenSSF SLSA v1.2 Specification:** CURRENT (Approved, **24 November 2025**; v1.0 retired). Verifiable build provenance and supply chain maturity.
- **PEP 508 / PEP 440:** STABLE. Python packaging specifications.
- **NIST SP 800-218 (SSDF):** STABLE. Secure Software Development Framework.

---

## 14. M22 Hands-On Fixture Contract — Safe Localhost Auth & Web Security Harness (`activity_l22_01.py`, `activity_l22_02.py`)

### 14.1 Purpose & Execution Scope
Module M22 delivers two bounded, course-owned localhost fixtures:
1. `activity_l22_01.py`: Password verifier formatting (`algo$params$salt$hash`), `hmac.compare_digest` validation, and `TeachingProfile-BearerV1` token validation (pure standard library).
2. `activity_l22_02.py`: Web security harness demonstrating SQL parameterization, CSRF token verification, and SSRF socket egress binding entirely on `127.0.0.1` using Python's built-in `http.server` and `sqlite3`.

### 14.2 Fixture File Structure
- Implementation: `labs/foundations/m22/activity_l22_01.py` & `labs/foundations/m22/activity_l22_02.py`
- Verification Suite: `labs/foundations/m22/test_m22.py` (Standard library `unittest` suite; capability-gates `pytest`)

### 14.3 Safety Guarantees, Fail-Closed Teardown & Lifecycle Contract
1. **Loopback Only:**
   The web server binds exclusively to `("127.0.0.1", 0)`, allowing the OS to allocate an ephemeral free port. It NEVER binds to `0.0.0.0` or external network interfaces.
2. **Ephemeral In-Memory Database:**
   All SQL demonstrations use an in-memory SQLite database (`:memory:`) populated with synthetic records (`alice`, `bob`, `charlie`).
3. **SSRF Bounded Testing Sandbox:**
   The SSRF exercise tests against bounded loopback endpoints, evaluating destination validation, DNS rebinding mitigations, and post-resolution socket connection binding.
4. **Deterministic Fail-Closed Thread Teardown & Listener Verification:**
   To guarantee deterministic cleanup and prevent lingering background processes:
   - Server threads are explicitly owned (non-daemon thread with dedicated stop event).
   - Teardown sequence executes:
     1. `server.shutdown()` to halt the request processing loop;
     2. `server.server_close()` to close the underlying socket;
     3. `thread.join(timeout=cleanup_timeout)` where `cleanup_timeout` is a configurable fixture policy parameter (default 2.0s);
     4. **Post-cleanup listener verification:** The test harness immediately attempts a probe connection or socket bind to verify the port has been released and no listener remains active.
     5. **Fail-Closed Disposition:** If the thread fails to join within the timeout or the port remains active, the fixture emits `FAIL / BLOCKED: Teardown verification failed; lingering listener detected`. It NEVER silently passes.

---

## 15. Module M23 Architecture — Systems Thinking & Judgment

### 15.1 Module Purpose & Capability Transition

Module M23 shifts the learner's focus from mechanics to engineering judgment, scientific measurement, and architectural trade-off evaluation. Throughout Stages 1–6, learners constructed individual components: virtual memory, file systems, network stacks, databases, distributed consensus, and observability pipelines. In M23, learners step back to evaluate how these components behave as a cohesive system under real-world constraints.

The core capability transition of M23 is:
- **From:** Accepting marketing claims, running naive benchmarks, and treating technologies as binary "good or bad" choices.
- **To:** Designing hypothesis-driven empirical measurement pipelines, defending against benchmarking pitfalls (coordinated omission, skewed latency distributions), rigorously evaluating technologies across the 12 dimensions of Decision D-015, and calculating multi-dimensional system costs (compute, memory, network egress, operational complexity).

### 15.2 Module Constraints & Invariants

1. **Rejection as a Passing Outcome:**
   In technology evaluation exercises, concluding that a proposed technology should **NOT** be adopted ("do not add Redis", "do not migrate to microservices") is explicitly recognized and graded as a fully valid, passing engineering outcome when supported by rigorous trade-off analysis.
2. **Rejection of Universal Constants:**
   Arbitrary rules of thumb (e.g., "always run 30 iterations", "every service must meet 10ms p99") are forbidden. Sample sizes, warm-up periods, and percentile targets must be derived from system dynamics, distribution characteristics, and service-level objectives (SLOs).
3. **AI Claim Verification Policy (Preserving OQ-BP-001 OPEN):**
   AI-generated architectural advice, code snippets, and benchmark interpretations are treated strictly as unverified hypotheses. They must be validated against empirical measurements, formal specifications, or source code before adoption. This policy maintains `OQ-BP-001` as OPEN and RFC-gated.

---

## 16. Lesson L23-01 Design — "How do I measure honestly?"

### 1. Target Mental Model
Benchmarking is a scientific experiment, not a marketing exercise. Measurement must always be **question-driven**: the choice of workload model, sample size, warm-up criteria, and summary statistics depends on the specific engineering question being asked. A benchmark that reports only average throughput or mean latency can be misleading for skewed distributions, but mean and standard deviation remain essential for resource capacity and cost modeling. Real-world systems exhibit multimodal, heavy-tailed latency distributions caused by background pauses, queueing, cache effects, and network variance. Honest measurement requires: matching the workload model (open vs. closed) to the system question; understanding when coordinated omission matters (when arrivals occur independently of completion); choosing appropriate summary metrics (percentiles, histograms, or moments); and using monotonic clocks while understanding that integer nanosecond units do not guarantee nanosecond hardware clock resolution.

### 2. Prerequisites
- Hard: `L20-01` (Observability & Metrics), `L04-02` (Empirical Measurement & Profiling).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Estimate, Judge, Diagnose`
- `Estimate`: Estimate latency and throughput characteristics across workloads and calculate confidence bounds for empirical observations.
- `Judge`: Select question-driven measurement methodologies, appropriate workload models (open vs. closed), and suitable summary statistics matching the data distribution and inference goal.
- `Diagnose`: Identify measurement artifacts, coordinated omission, warm-up transients, and misleading statistical summaries.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-009 Correctness`: Revisit (First home: M02 `L02-03`). Correctness of empirical data collection and statistical inference.
- `EC-CON-010 Failure`: Revisit (First home: M03 `L03-03`). Latency degradation and tail-latency failures under load.

### 5. Learning Outcomes
- Formulate a falsifiable measurement hypothesis and define the exact independent and dependent variables.
- Contrast open workload models (requests arrive according to an independent arrival process) with closed workload models (fixed concurrent clients waiting for prior responses before issuing new requests), articulating which question each model legitimately answers.
- Explain coordinated omission and identify scenarios where synchronous client generators distort latency measurements by coupling arrival generation to service completion.
- Evaluate warm-up criteria based on mechanism and question (e.g., JIT compilation or cache warming vs. cold-start CLI benchmarking).
- Select summary statistics matched to data distributions and engineering goals: percentiles and histograms for tail latencies and SLOs; mean and total counts for capacity planning and cloud cost calculations.

### 6. Stable Principle
Select measurement methods and statistical representations that directly answer your engineering question; never let your benchmark harness inadvertently reshape the workload you intend to measure.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** IEEE 754 floating point arithmetic, POSIX `CLOCK_MONOTONIC`.
- **Implementation:** Python `time.monotonic_ns()` (returns integer nanoseconds, but underlying OS timer tick resolution may be microseconds or milliseconds), latency histograms.
- **Current Practice:** Continuous benchmarking in CI, distributed tracing span latencies, latency SLOs (p99/p99.9), coordinated omission correction in open load generators (wrk2, k6, Locust).

### 8. Required Distinctions / Misconceptions
- *Misconception:* Mean and standard deviation are universally "wrong" for systems measurement.
  *Reality:* Mean is inappropriate as a sole proxy for typical user experience in skewed distributions (where percentiles like p50/p99 excel). However, mean is indispensable for calculating total work, aggregated throughput, energy consumption, and cloud infrastructure costs. Summary statistics must be chosen based on the inference goal.
- *Misconception:* Closed workload models are inherently invalid or "mask saturation."
  *Reality:* Closed workload models accurately represent systems with a fixed, bounded client population (e.g., a fixed pool of batch worker threads or interactive desktop users waiting for a response). Open workload models represent independent arrivals (e.g., public web traffic). Neither is universally superior; each answers a different engineering question.
- *Misconception:* `time.time()` jumps whenever daylight saving time changes.
  *Reality:* Unix epoch `time.time()` measures seconds since the epoch and is not affected by local civil-time daylight saving offset changes. However, it is subject to NTP slews, steps, and manual system clock adjustments. Benchmarking uses `time.monotonic_ns()` because monotonic clocks guarantee non-decreasing counts.
- *Misconception:* `time.monotonic_ns()` provides true nanosecond precision.
  *Reality:* `monotonic_ns()` returns integer nanosecond units, but the underlying clock resolution is bounded by the host OS kernel and hardware timer frequency (e.g., HPET, TSC, or Windows interrupt tick).

### 9. Worked Example
Learners evaluate a benchmark comparing queue processing under a specified arrival process:
- Scenario: Target arrival rate is set to 100 requests/second (scheduled inter-arrival time = 10 ms).
- Execution trace:
  - The load generator issues requests in a synchronous loop.
  - A synthetic 500 ms processing stall occurs on request #10.
  - In an uncoordinated synchronous generator, the loop blocks for 500 ms. The subsequent 50 requests that were scheduled to arrive during that 500 ms window (at 100 req/s) are delayed at the generator.
  - The uncoordinated benchmark records only service time for completed requests, reporting an artificially low latency profile.
  - In an arrival-scheduled generator, the arrival timestamp $T_{\text{sched}}$ is tracked independently; the total latency is recorded as $T_{\text{complete}} - T_{\text{sched}}$, accurately capturing queuing delay under this open arrival assumption.

### 10. Bounded Hands-On / Observation
Learners run `labs/foundations/m23/activity_l23_01.py`:
1. Run a load test against a server with an injected synthetic 200 ms stall (explicitly designated as a synthetic pause, not claimed to be actual GC observation unless GC is instrumented).
2. Compare the output of an uncoordinated synchronous generator versus an arrival-scheduled generator under a specified target arrival rate.
3. Inspect the resulting latency distributions and summary statistics. Note: The fixture does not promise "Zero Flakiness"; variability and noise are documented as empirical realities.

### 11. Evidence to Record
- Measurement Protocol Card (Hypothesis, Workload model open/closed rationale, Warm-up criteria, Arrival schedule assumptions, Clock source and observed resolution).
- Comparative Latency Summary Table (Min, Mean, p50, p90, p99, Max, along with stated sample size and inference limits).

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Learner designs a valid measurement protocol, explains open vs. closed workload applicability, and demonstrates arrival-scheduled latency recording under stated arrival assumptions.
- **BLOCKED:** Host environment lacks monotonic timer support.
- **NOT RUN:** Hands-on exercise not executed.

### 13. Progressive Support
- **Question:** If an e-commerce page makes 50 serial or parallel microservice calls to render a single page, what assumptions are required before you can calculate the probability of all calls completing within p99 using $(0.99)^{50} \approx 0.605$?
- **Hint 1:** What does $(P_1 \times P_2 \times \dots \times P_n)$ assume about the statistical relationship between the events?
- **Hint 2:** Are microservice calls in a shared cluster truly independent if they share database instances or network switches?
- **Expected Observation:** The $(0.99)^{50}$ calculation strictly assumes that all 50 calls are statistically independent and that their latency distributions are identically bounded.
- **Full Explanation:** The formula demonstrates the fan-out tail effect under the explicit assumption of independent, uncorrelated latencies. In real production systems, requests often share common bottlenecks (database locks, network links, or host CPU), meaning latencies are correlated and the true failure probability may be higher or lower depending on cascade dynamics. Learners must always state independence assumptions when presenting probabilistic tail estimates.

### 14. Required Visuals
- *Visual M23-V1:* Scientific Systems Measurement Architecture (Question/Hypothesis → Workload Model Selection → Monotonic Timing → Multimodal Distribution Analysis).
- *Visual M23-V2:* Coordinated Omission: Comparing Service Time vs. Scheduled Arrival Latency under Open Workload Assumptions.

### 15. Failure Modes
- Universalizing rules of thumb (e.g., claiming all benchmarks must use p99 or that mean is never useful).
- Ignoring background system activity during local performance benchmarks.

### 16. Non-Goals
- Formal statistical proofs of heavy-tailed Pareto distributions.
- Kernel-level CPU performance counter tuning (perf/eBPF hardware counters).

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Standard library `unittest` suite verifying that arrival-scheduled timer accounts for scheduled wait time under simulated stalls.
- Reviewer-Required: Web Lead review of learner's Measurement Protocol Card, stated assumptions, and metric selection rationale.

### 18. Source Grounding with Currentness Classification
- **Gil Tene (Coordinated Omission):** STABLE. Foundational methodology for latency measurement in open systems.
- **Brendan Gregg (Systems Performance, 2nd Ed.):** STABLE. Methodologies for USE (Utilization, Saturation, Errors) and benchmark evaluation.

---

## 17. Lesson L23-02 Design — "How do I pick a technology?"

### 1. Target Mental Model
Engineering is the art of trade-offs under constraints. There are no universally superior technologies; every technology choice is a package deal that couples benefits with operational overhead, failure modes, consistency trade-offs, and maintenance burdens. Picking a technology requires an objective, multi-dimensional evaluation against explicit requirements rather than industry hype or marketing claims. Critically, **rejecting a technology** and keeping an architecture simpler is often the most mature engineering decision.

### 2. Prerequisites
- Hard: `L23-01` (Honest Measurement).
- Soft: `L22-01` (Authn/Authz), `L17-01` (Replication & Consistency).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Judge, Learn-New-Tech, Explain`
- `Judge`: Evaluate candidate technologies against the 12 dimensions of Decision D-015, weigh architectural trade-offs, and defend technology rejection as a valid engineering outcome.
- `Learn-New-Tech`: Rapidly dissect new technology claims, inspect architectural documentation, and separate stable principles from marketing buzzwords.
- `Explain`: Articulate the operational, consistency, and maintenance costs of introducing a new dependency.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-007 Specification`: Revisit (First home: M02 `L02-03`). System requirements vs. vendor specifications.
- `EC-CON-010 Failure`: Revisit (First home: M03 `L03-03`). Operational failure modes of candidate technologies.

### 5. Learning Outcomes
- Apply the 12 evaluation dimensions of Decision D-015 to evaluate candidate technologies.
- Distinguish between marketing/vendor claims, documentation promises, and observable runtime reality.
- Conduct a structured case study on caching (e.g., evaluating Redis vs. in-memory cache vs. relational query optimization), defending whether to adopt or reject it.
- Evaluate AI-generated technical recommendations as untrusted hypotheses requiring verification.
- Write a formal Architecture Decision Record (ADR) detailing context, alternatives considered, chosen decision, and trade-offs accepted.

### 6. Stable Principle
Every technology you add is a new way for your system to fail and a new dependency your team must operate, monitor, patch, and debug. A technology must justify its operational existence.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** Formal protocol and storage specifications (e.g., Redis RESP protocol, SQL standards, ACID guarantees).
- **Implementation:** Concrete software packages (PostgreSQL, Redis, Kafka, SQLite).
- **Current Practice:** Architecture Decision Records (ADRs), Technology Radars (Adopt, Trial, Assess, Hold), vendor due diligence, open-source license audits.

### 8. Required Distinctions / Misconceptions
- *Misconception:* "We need Redis because our database is slow."
  *Reality:* Adding Redis introduces cache invalidation complexity, cache stampede risks, split-brain scenarios, and synchronization bugs. In many cases, adding a missing database index or optimizing query plans solves the problem with zero added infrastructure.
- *Misconception:* Following industry consensus (what big tech companies use) is the safest choice.
  *Reality:* Large tech companies operate under radically different scale, staffing, and organizational constraints. Adopting their solutions prematurely incurs massive accidental complexity.
- *Misconception:* AI assistants can decide the optimal technology stack for your project.
  *Reality:* AI models reproduce common web tropes and frequently hallucinate capabilities or overlook operational failure modes. AI recommendations must be treated as hypotheses to be tested against project constraints.

### 9. Worked Example: The Redis Evaluation Case Study
A team building a content management system proposes adding Redis to cache article lookups because page loads are slow.
Learners evaluate the proposal across Decision D-015:
1. *Problem Definition:* Read latency is 80ms; target is <20ms.
2. *Root Cause:* Database query performs a full table scan due to a missing index on `slug`. Adding the index drops query time to 4ms.
3. *Redis Trade-Off Analysis:*
   - Benefits: In-memory sub-millisecond lookups.
   - Costs: Dedicated Redis instance, RAM cost, connection pooling, network hop, cache invalidation logic, risk of stale reads, memory limits and eviction policies.
4. *Decision:* **REJECT REDIS.** Adding the SQL index satisfies the SLO with zero new infrastructure, zero operational overhead, and zero cache invalidation bugs.

### 10. Bounded Hands-On / Observation
Learners utilize `labs/foundations/m23/activity_l23_02.py`:
1. Receive three realistic architectural scenarios (e.g., job queuing, session storage, full-text search).
2. Complete a Decision D-015 Evaluation Card for each scenario, scoring candidate technologies against project requirements.
3. In at least one scenario, explicitly defend a **REJECTION** decision, demonstrating why the proposed technology is unwarranted.

### 11. Evidence to Record
- D-015 Technology Evaluation Card covering all 12 dimensions:
  1. Problem & Requirement Clarity
  2. Data Model & Access Pattern Fit
  3. Consistency & Durability Guarantees
  4. Failure Modes & Operational Complexity
  5. Performance & Scalability Boundaries
  6. Observability & Debuggability
  7. Security, Trust & Isolation
  8. Ecosystem, Maintenance & Longevity
  9. Licensing & Governance
  10. Cost Model (Infrastructure & Human)
  11. Migration & Reversibility (Exit Strategy)
  12. Alternatives Considered & Explicit Rejection Rationale
- Formal Architecture Decision Record (ADR).

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Learner provides a rigorous, multi-dimensional ADR that evaluates constraints objectively and successfully defends a technology decision (including valid rejection).
- **BLOCKED:** None (conceptual evaluation supported by test harness).
- **NOT RUN:** Evaluation exercise omitted.

### 13. Progressive Support
- **Question:** When is adopting a specialized message broker (e.g., RabbitMQ or Kafka) justified over using an existing relational database transactional outbox table with polling?
- **Hint 1:** Consider the operational cost of managing a separate distributed cluster versus the throughput limits of database polling.
- **Hint 2:** Look at message volume: 100 messages per second vs. 100,000 messages per second.
- **Expected Observation:** At low to moderate throughput (e.g., <500 msg/sec), a database outbox table provides transactional atomicity with the business data without any new operational dependencies.
- **Full Explanation:** The transactional outbox pattern in PostgreSQL/MySQL avoids dual-write consistency bugs because the message and business mutation commit in the same ACID transaction. A dedicated broker is only justified when message throughput exceeds database write capacity, or when complex routing, long-term event retention, or massive fan-out is strictly required.

### 14. Required Visuals
- *Visual M23-V3:* The Decision D-015 12-Dimension Technology Evaluation Framework.

### 15. Failure Modes
- Choosing a technology solely because it is trending on social media or in developer surveys.
- Failing to define an exit strategy or migration path before adopting a proprietary cloud service.

### 16. Non-Goals
- Memorizing feature matrices of specific proprietary cloud vendors (AWS vs. Azure vs. GCP).
- Conducting formal procurement or commercial contract negotiations.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Automated schema validation of learner's JSON/Markdown ADR artifact ensuring all 12 dimensions are completed.
- Reviewer-Required: Lead review evaluating the depth, realism, and objectivity of the trade-off analysis.

### 18. Source Grounding with Currentness Classification
- **Decision D-015 (Technology Evaluation Framework):** STABLE / CANONICAL. Core curriculum policy for technology adoption and rejection.
- **Michael Nygard (Release It!, 2nd Ed.):** STABLE. Stability patterns and architectural anti-patterns.
- **OQ-BP-001 (AI Literacy Policy):** OPEN / RFC-GATED. AI outputs treated as unverified candidate hypotheses.

---

## 18. Lesson L23-03 Design — "What is the cost of my design?"

### 1. Target Mental Model
Every architectural design incurs costs across multiple non-fungible currencies: **hardware resources** (CPU cores, RAM gigabytes, disk IOPS/storage), **network egress bandwidth**, **financial cloud billing**, and **human operational overhead** (cognitive load, on-call fatigue, maintenance friction). Systems thinking requires modeling these costs quantitatively before building. Using back-of-the-envelope Fermi estimates, capacity planning, and bottleneck sensitivity analysis, an engineer can predict how a system's cost curves scale with user growth and identify which resource will exhaust first.

### 2. Prerequisites
- Hard: `L23-02` (Technology Selection & Judgment).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Estimate, Judge`
- `Estimate`: Perform Fermi back-of-the-envelope calculations for compute, memory, storage, and network egress; track units precisely (bits vs Bytes, decimal vs binary prefixes) and make all assumptions explicit.
- `Judge`: Balance monetary costs against latency, reliability, and operational complexity trade-offs; identify critical cost bottlenecks and evaluate sensitivity to scaling assumptions.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-010 Failure`: Revisit (First home: M03 `L03-03`). Resource exhaustion and scaling cliffs as failure modes.
- `EC-CON-016 Durability`: Revisit (First home: M09 `L09-01`). Storage cost scaling of long-term durable logs.

### 5. Learning Outcomes
- Perform back-of-the-envelope Fermi calculations to estimate daily storage growth, network bandwidth, and compute sizing from basic business metrics (DAU, requests/user/day, payload size).
- Calculate total cost of ownership (TCO) including infrastructure billing and operational maintenance overhead.
- Identify the primary bottleneck resource (CPU-bound, memory-bound, disk-I/O-bound, network-bound) in a multi-tier architecture.
- Conduct sensitivity analysis: determine how a 10x surge in data volume or a 5x increase in read/write ratio shifts the architectural bottleneck.

### 6. Stable Principle
If you cannot estimate the resource requirements of your design within an order of magnitude on a napkin, you do not understand its operational scaling behavior.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** Dimensional analysis, unit conversions (bytes, bits, seconds, IOPS), latency numbers every programmer should know (Jeff Dean / Peter Norvig).
- **Implementation:** Cloud pricing APIs, resource allocation limits (cgroup memory/cpu limits), database capacity calculators.
- **Current Practice:** FinOps (cloud financial operations), capacity planning models, auto-scaling threshold tuning, ingress/egress cost optimization.

### 8. Required Distinctions / Misconceptions
- *Misconception:* Cloud computing means infinite resources and no need for capacity planning.
  *Reality:* Cloud resources are bounded by financial budgets, API rate limits, and network egress costs. Unplanned scaling can bankrupt a project.
- *Misconception:* Network egress is negligible compared to compute and storage costs.
  *Reality:* Major cloud providers charge premium rates for internet egress. Architectures that transfer uncompressed or redundant data across availability zones or to the public internet frequently incur unexpected billing shocks.
- *Misconception:* Human engineering time is free compared to server hardware.
  *Reality:* Spending months of senior developer time building a custom distributed caching cluster to save $50/month in server costs is an engineering failure.

### 9. Worked Example
Learners calculate the resource requirements for a photo-sharing service:
- Users: 1,000,000 Daily Active Users (DAU).
- Actions: Each user uploads 2 photos/day and views 50 photos/day.
- Photo size: Average compressed photo is 1 MB.
- *Storage Estimate:* $1,000,000 	imes 2 	imes 1	ext{ MB} = 2	ext{ TB/day} pprox 730	ext{ TB/year}$. With 3x replication: $2.19	ext{ PB/year}$.
- *Egress Bandwidth Estimate:* $1,000,000 	imes 50 	imes 1	ext{ MB} = 50	ext{ TB/day}$.
  $50	ext{ TB} / 86,400	ext{ sec} pprox 578	ext{ MB/sec} = 4.6	ext{ Gbps}$ average bandwidth.
  Peak bandwidth (assuming 3x peak-to-average ratio): $pprox 13.8	ext{ Gbps}$.
Learners deduce that this service is overwhelmingly **network-egress and storage-bound**, not CPU-bound. Caching and CDN edge termination are critical architectural necessities.

### 10. Bounded Hands-On / Observation
Learners run a capacity modeling script in Python:
1. Input parameters for their Mini Cloud App (requests/sec, storage/item, retention period).
2. The script computes projected resource utilization over 1, 6, and 12 months.
3. Learners modify parameters (e.g., introducing data compression, changing retention from indefinite to 30 days) to observe the dramatic reduction in storage and egress costs.

### 11. Evidence to Record
- Fermi Back-of-the-Envelope Calculation Sheet (Units clearly labeled, step-by-step arithmetic, assumptions stated).
- Bottleneck Identification & Sensitivity Matrix (Resource, Baseline utilization, 10x load projection, Saturation threshold, Mitigation).

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Calculations are mathematically sound, units are correct (differentiating bits from bytes), assumptions are explicit, and the primary bottleneck is correctly identified.
- **BLOCKED:** None.
- **NOT RUN:** Calculation exercise omitted.

### 13. Progressive Support
- **Question:** If you have 10,000,000 rows in a database table and each row has an average size of 200 bytes, how much memory is needed to hold the entire table in RAM?
- **Hint 1:** Multiply row count by row size: $10^7 	imes 200	ext{ bytes}$.
- **Hint 2:** Convert bytes to megabytes and gigabytes ($1	ext{ GB} pprox 10^9	ext{ bytes}$).
- **Expected Observation:** $10,000,000 	imes 200	ext{ bytes} = 2,000,000,000	ext{ bytes} pprox 2	ext{ GB}$.
- **Full Explanation:** The entire table fits comfortably into 2 GB of RAM. Therefore, before considering sharding or a distributed database, a simple single-node database server with 16 GB of RAM can easily cache the entire active dataset in memory, achieving microsecond lookup performance with zero distributed systems overhead.

### 14. Required Visuals
- *Visual M23-V4:* System Cost & Bottleneck Hierarchy: Compute vs Memory vs Storage vs Network Egress vs Human Operations.

### 15. Failure Modes
- Mixing up bits (b) and bytes (B) in bandwidth calculations.
- Ignoring network egress costs and availability-zone data transfer fees in cloud estimates.

### 16. Non-Goals
- Memorizing specific cloud SKU prices or promotional discount tiers.
- Building complex enterprise enterprise accounting or tax depreciation models.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Unit tests validating numeric calculation outputs within reasonable bounds (order of magnitude check).
- Reviewer-Required: Lead review of stated assumptions and bottleneck reasoning.

### 18. Source Grounding with Currentness Classification
- **Jeff Dean (Numbers Every Programmer Should Know):** STABLE. Classical latency and throughput hierarchy.
- **FinOps Foundation Framework:** CURRENT. Modern cloud cost governance and architectural accountability.

---

## 19. M23 Hands-On Fixture & Technology Evaluation Contract (`activity_l23_01.py`, `activity_l23_02.py`)

### 19.1 Purpose & Execution Scope
Module M23 provides two hands-on artifacts:
1. `activity_l23_01.py`: An empirical latency measurement harness comparing uncoordinated synchronous loops against arrival-scheduled generators under question-driven open arrival models.
2. `activity_l23_02.py`: A structured Decision D-015 Technology Evaluation validation schema and evaluator that audits Technology Decision Records for completeness across all 12 dimensions.

### 19.2 Fixture File Structure
- Implementation: `labs/foundations/m23/activity_l23_01.py`, `labs/foundations/m23/activity_l23_02.py`
- Verification Suite: `labs/foundations/m23/test_m23.py` (Standard library `unittest` suite; capability-gates `pytest`)

### 19.3 Invariants & Interface Contract
1. **Timing Accuracy & Units:**
   Uses `time.monotonic_ns()` for duration measurements, explicitly documenting that integer nanosecond units do not imply nanosecond hardware clock resolution.
2. **Synthetic Pause Injections:**
   Harness tests use explicitly labeled synthetic pause injections rather than claiming uninstrumented garbage collection observation. (The fixture does not overpromise "zero flakiness"; platform variance and jitter are treated as empirical realities).
3. **Structured ADR Schema:**
   The D-015 evaluator validates that all 12 dimensions are addressed and specifically checks for substantive justifications in Dimension 10 (Operational Burden) and Dimension 12 (When Not to Use).

---

## 20. Module M24 Architecture — Final System Defense (Integration & Judgment Capstone)

### 20.1 Module Purpose & Capability Transition

Module M24 represents the ultimate synthesis and capstone milestone of the entire Essential CS curriculum. It introduces **zero new computing mechanisms, zero new protocols, and zero new infrastructure**. Instead, it challenges the learner to step into the role of a lead systems architect and defend their end-to-end system design (exemplified by their longitudinal Mini Cloud App project built across Stages 1–7) under rigorous technical scrutiny.

The core capability transition of M24 is:
- **From:** Building individual components to satisfy modular assignments and isolated unit tests.
- **To:** Presenting an integrated architectural defense, tracing invariants across all physical and logical layers, proving claims with verifiable empirical and formal evidence, handling sudden constraint changes, and defining pre-ship verification criteria.

### 20.2 Module Constraints & Invariants

1. **Integration and Assessment Only:**
   M24 introduces no new algorithms or libraries. It is purely an evaluative and synthesis capstone.
2. **Design-Owned Assessment Contract:**
   Design explicitly owns the learner/reviewer contract, defense rubric, pass thresholds, and evidence sufficiency criteria. No universal arbitrary scoring formula (e.g., "must score 85%") is permitted; evaluation is grounded in constraint satisfaction, invariant preservation, and evidence sufficiency.
3. **Changed-Constraint Challenge:**
   A core requirement of the defense is demonstrating resilience under changed assumptions (e.g., "What if data volume increases 100x?", "What if the network connection between node A and B has 200ms latency?", "What if the client environment is malicious?").

---

## 21. Lesson L24-01 Design — "Can I defend an architecture?"

### 1. Target Mental Model
Defending an architecture is not an exercise in persuasion or polished slides; it is the discipline of mapping claims to evidence. A defensible architecture possesses complete visibility into its internal state transitions, data flows, and failure domains. When challenged, an architect does not say "it just works"; they trace the request across network boundaries, demonstrate where trust is verified, cite the formal invariants governing state, provide empirical measurements for performance claims, acknowledge explicit trade-offs and unknowns, and adapt the design coherently when real-world constraints change.

### 2. Prerequisites
- Hard: `L23-02` (Technology Selection & Systems Judgment).
- Integrative: Complete mastery of Stages 1–6 (OS, Networks, Storage, Distributed Systems, Web, Security).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Judge, Explain, Diagnose, Estimate`
- `Judge`: Defend architectural trade-offs, justify rejected alternatives, and adapt to changed constraints.
- `Explain`: Articulate end-to-end request, state, control, and failure traces across the actual system architecture.
- `Diagnose`: Identify points of failure, unmitigated risks, and broken invariants under adversarial challenge.
- `Estimate`: Quantify the resource, capacity, and cost limits of the proposed architecture.

### 4. Canonical Concept First-Home vs. Revisit
Revisit strictly those canonical concepts that have an active, demonstrable evidence role in the learner's actual system architecture:
- `EC-CON-007 Specification` (First home: M02 `L02-03`): Stated invariants and API contracts.
- `EC-CON-008 Invariant` (First home: M02 `L02-03`): Safety and liveness invariants maintained under failure.
- `EC-CON-009 Correctness` (First home: M02 `L02-03`): Test verification and assertion evidence.
- `EC-CON-010 Failure` (First home: M03 `L03-03`): Crash recovery boundaries and unhandled failure modes.
- `EC-CON-013 Isolation` (First home: M07 `L07-01`): Process, memory, and database isolation.
- `EC-CON-016 Durability` (First home: M09 `L09-01`): Filesystem `fsync` and database WAL durability boundaries.
- `EC-CON-017 Trust Boundary` (First home: M07 `L07-01`): Transport, endpoint, and process authority perimeters.

### 5. Learning Outcomes
- Construct the 16 Core Architectural Traces and Artifacts for the capstone system.
- Provide sufficient evidence across all 12 Evidence Areas without relying on unsubstantiated assertions.
- Successfully respond to an adversarial "Changed-Constraint Challenge" by diagnosing new bottlenecks, identifying broken invariants, and proposing reasoned adaptations.
- Distinguish between proven claims, empirical observations, explicit assumptions, and honest unknowns.

### 6. Stable Principle
An architectural claim without verifiable evidence is merely an opinion. A real system architect knows exactly where their design breaks and what it costs.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** System requirements, API contracts, RFCs, consistency models (linearizable, eventual, sequential).
- **Implementation:** Working Mini Cloud App codebase, unit and integration test suites, configuration files.
- **Current Practice:** Production Readiness Reviews (PRRs), Architecture Review Boards (ARBs), RFC design proposals, threat modeling reviews.

### 8. Required Distinctions / Misconceptions
- *Misconception:* A good architecture defense proves the system has no flaws and can scale infinitely.
  *Reality:* Every architecture has limits and trade-offs. A mature defense clearly defines the system's operational boundaries, known failure modes, and resource limits.
- *Misconception:* Evidence sufficiency means every single claim requires a live benchmark.
  *Reality:* Evidence takes multiple valid forms: formal specifications, authoritative RFCs, automated test assertions, mathematical capacity models, and explicit documented assumptions.

### 9. Worked Example (Scenario Card Conditional on Actual Architecture)
A learner defends their actual single-node Mini Cloud App architecture (utilizing an embedded SQLite database in WAL mode on a local filesystem):
*Claim:* The application provides durable storage for committed user records and recovers cleanly from sudden process termination.
*Reviewer Changed-Constraint Challenge:* "The host process crashes abruptly (e.g. `kill -9` or power loss) while executing an HTTP transaction that updates two related tables. On restart, what state does a querying client observe, what happens to the uncommitted transaction, and does your single-node design provide any availability guarantee while the host is down?"
*Learner Defense:*
1. *State & Durability Trace:* Traces SQLite Write-Ahead Logging (WAL) and `fsync` boundaries per M09/M14. If `PRAGMA synchronous = NORMAL` or `FULL` was configured, committed transactions prior to the crash are durable in the WAL file; uncommitted frames in the transaction are not committed.
2. *Recovery Mechanics:* On restart, SQLite's recovery routine inspects the WAL header, detects that the interrupted transaction lacked a commit frame, and rolls it back, leaving the database in a consistent pre-transaction state without partial corruption.
3. *Availability Boundary:* The learner explicitly acknowledges that their single-node architecture does **NOT** provide high availability or automatic failover. While the process is down, availability is zero. The learner defends this trade-off: for the target scale and operational complexity budget, single-node simplicity was chosen over the massive operational burden of a distributed consensus cluster (M17/M18). No fake failover replicas or fabricated Raft state are claimed.

### 10. Bounded Hands-On / Observation
Learners complete their comprehensive Capstone System Defense Dossier, detailing the 16 Architectural Traces:
1. Request Trace (End-to-end packet and function path)
2. Data & State Trace (Lifecycle of a record from memory to persistent disk)
3. Control & Authority Trace (Authentication and permission evaluation)
4. State Inventory (Volatile vs Durable vs Replicated state)
5. Invariants & Specifications (Explicit guarantees maintained under all conditions)
6. Trust Boundaries (Hardware, kernel, network, and application perimeters)
7. Isolation Boundaries (Process, container, memory, and database isolation)
8. Failure & Risk Walkthrough (Single points of failure, network partitions, cascading failures)
9. Security & Privacy Decisions (Crypto use, token handling, sanitization, data retention)
10. Measurements & Performance Evidence (Empirical distributions, latency profiles)
11. Cost & Scale Estimates (Fermi models for CPU, RAM, storage, and egress bandwidth)
12. Alternatives Considered (Alternative technologies and architectures evaluated)
13. When-Not-To-Use & Rejected Choices (Explicit justifications for rejecting complex options)
14. Explicit Unknowns (Unmeasured areas, unverified edge cases, known limitations)
15. Learning Plan (How the team will investigate and resolve unknowns)
16. Changed-Constraint Adaptation (Response to a randomized constraint perturbation)

### 11. Evidence to Record
- The Capstone System Defense Dossier (Markdown document satisfying all 16 traces).
- Traceability Matrix mapping every architectural claim to its corresponding evidence type.

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Dossier satisfies all 16 traces; all claims are supported by sufficient evidence; changed-constraint challenge is resolved coherently without hand-waving.
- **BLOCKED:** Mini Cloud App project incomplete or failing core integration tests.
- **NOT RUN:** Defense dossier not submitted.

### 13. Progressive Support
- **Question:** If you claim your service handles 10,000 requests per second, what three independent pieces of evidence must you provide to make this claim defensible?
- **Hint 1:** Consider compute capacity, network capacity, and empirical measurement.
- **Hint 2:** Does your benchmark account for coordinated omission and realistic payload sizes?
- **Expected Observation:** A defensible claim requires: 1) A hardware sizing model proving that 10,000 requests/sec does not exceed CPU core or NIC bandwidth limits; 2) An empirical load test methodology demonstrating this throughput under steady state with arrival-rate scheduling; 3) A latency distribution showing acceptable percentiles during the run.
- **Full Explanation:** Merely asserting a number or citing a single-threaded loop benchmark is unacceptable. An architect must pair empirical load test logs with a resource saturation model (CPU, RAM, network) and an explicit statement of the test environment's constraints.

### 14. Required Visuals
- *Visual M24-V1:* The 16 Core Architectural Traces Matrix.
- *Visual M24-V2:* The Evidence-to-Claim Mapping Framework.

### 15. Failure Modes
- Hand-waving answers when asked how data is recovered after a crash.
- Claiming zero latency or zero cost for distributed operations.

### 16. Non-Goals
- Deploying a commercial multi-region cloud cluster.
- Building marketing presentation decks or sales pitches.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Automated validation script checking completeness of all 16 trace sections and evidence citations.
- Reviewer-Required: In-depth peer review / Web Lead evaluation of the architectural defense and changed-constraint response.

### 18. Source Grounding with Currentness Classification
- **Google SRE Book (Production Environment & Architecture):** STABLE. Foundations of system architecture, resilience, and operational defense.
- **SEI / CMU Architecture Tradeoff Analysis Method (ATAM):** STABLE. Structured methodology for software architecture evaluation.

---

## 22. Lesson L24-02 Design — "What should I measure before I ship?"

### 1. Target Mental Model
Shipping software to production is a controlled release of risk. An engineer does not simply test that the "happy path" works; they construct a **risk-prioritized pre-ship verification plan**. This plan establishes what must be measured empirically, what must be verified by automated tests, what must be manually inspected, and what can safely remain an explicit unknown. Furthermore, shipping requires operational readiness: verifying observability telemetry, establishing safe rollback procedures, and proving that the system fails gracefully under resource exhaustion or downstream failure.

### 2. Prerequisites
- Hard: `L24-01` (Architectural Defense).

### 3. Primary Competencies
Canonical Blueprint primary mapping (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`): `Judge, Diagnose`
- `Judge`: Prioritize pre-ship verification effort based on risk severity, blast radius, and system criticality; define explicit boundaries for acceptable unknowns.
- `Diagnose`: Identify pre-ship operational blind spots, unmonitored failure modes, and compatibility risks in deployment/rollback paths.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-010 Failure`: Revisit (First home: M03 `L03-03`). Failure mitigation, graceful degradation, and disaster recovery.
- `EC-CON-009 Correctness`: Revisit (First home: M02 `L02-03`). Verification gates before production deployment.

### 5. Learning Outcomes
- Construct a Risk-Prioritized Evidence Matrix classifying release checks into: Must Measure, Must Test, Must Inspect, and Acceptable Unknown, grounded in the system's actual architecture and risk profile.
- Verify production operational readiness: telemetry signals (M20), transport security and input sanitization (M21/M22), and resource cost boundaries (M23).
- Design and dry-run a deployment compatibility and rollback/roll-forward strategy, stating explicit data-loss bounds rather than assuming universal zero loss.
- Formulate precise Service Level Objectives (SLOs) and Error Budgets governing release criteria.

### 6. Stable Principle
If you do not have an explicit failure recovery or deployment compatibility strategy (whether rollback, roll-forward, or migration reversal) and observable health signals, you are not shipping software; you are gambling with your users' data.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** Service Level Agreements (SLAs), Service Level Objectives (SLOs), release criteria checklists.
- **Implementation:** CI/CD pipeline automation, health check endpoints (`/healthz`), canary deployment scripts, database migration rollbacks.
- **Current Practice:** Progressive delivery, canary analysis, automated rollback on metric anomaly, Chaos Engineering.

### 8. Required Distinctions / Misconceptions
- *Misconception:* 100% test coverage means software is safe to ship.
  *Reality:* Unit tests verify code paths against developer assumptions. They do not verify network latencies, memory leaks under load, database migration deadlocks, or third-party dependency outages.
- *Misconception:* Rollback simply means redeploying the previous git commit.
  *Reality:* If the new version performed destructive database schema migrations or wrote data in an incompatible format, rolling back code will crash the previous version or corrupt data. Backward-compatible schema evolution is required.

### 9. Worked Example (Scenario Card: Web Service Release)
Learners evaluate a pre-ship verification plan using explicit scenario-card parameters (numbers represent scenario-specific targets, not universal course rules):
- *Scenario Card Context:* Internal document-indexing service release (target throughput 500 req/s, single database instance).
- *Must Measure (Scenario Card Targets):* Latency distribution under simulated steady-state arrival load (scenario target: p95 < 150 ms under 500 req/s open arrival); process RSS memory growth during a 30-minute test run to verify bounded memory usage.
- *Must Test:* Automated regression suite with all mandatory document-parsing and access-control invariant gates passing; idempotent retry handling on client disconnect.
- *Must Inspect:* Credential handling (environment variables vs. committed secrets); structured error response sanitization (preventing stack trace leakage to clients).
- *Acceptable Unknown:* System behavior under an unannounced multi-hour cloud zone network partition (explicitly documented as an unmitigated operational risk outside current project scope).
- *Deployment Compatibility Strategy:* Analyze migration trade-offs: if a column addition is backward-compatible (nullable), a rollback to previous code is safe; if a migration is destructive, a roll-forward or snapshot recovery strategy is required, with stated data-loss bounds.

### 10. Bounded Hands-On / Observation
Learners execute a pre-ship verification audit against their Mini Cloud App:
1. Run the applicable automated test suites and require every mandatory core invariant gate in the selected scenario to pass.
2. Verify observability and error-handling readiness: simulate a missing database or unresponsive loopback port and verify that structured error logs with context are emitted.
3. Audit the database schema migration plan for the project's actual database (e.g., SQLite table alter or schema version bump), verifying whether the planned change is backward-compatible and documenting the rollback or recovery procedure.

### 11. Evidence to Record
- Pre-Ship Risk-Prioritized Evidence Checklist.
- Deployment Compatibility & Reversal Strategy Record proving that failure during deployment or schema change leaves data intact and services operational (via rollback, roll-forward, or explicit migration reversal).

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Pre-ship checklist completed; deployment compatibility and reversal plan verified; all critical invariants verified under automated regression tests.
- **BLOCKED:** Failing integration test suite.
- **NOT RUN:** Pre-ship verification omitted.

### 13. Progressive Support
- **Question:** How do you safely alter a database schema (e.g., renaming a column from `full_name` to `display_name`) in production without causing downtime during deployment?
- **Hint 1:** What happens if the database schema changes while the old version of the application is still running?
- **Hint 2:** Think about a phased multi-step migration (Expand and Contract).
- **Expected Observation:** Immediate renames break running application instances that expect the old column name.
- **Full Explanation:** Under continuous-deployment or multi-instance rolling upgrade constraints where old and new application versions run concurrently against a shared database, safe schema evolution commonly employs the Expand-and-Contract (Parallel Run) pattern to maintain forward and backward compatibility (rather than as a universal requirement for single-instance or maintenance-window deployments):
  1. *Phase 1 (Expand):* Add `display_name` as a new nullable column; update application code to write to both columns and read from `display_name` if present, falling back to `full_name`.
  2. *Phase 2 (Backfill):* Run a background script copying existing data from `full_name` to `display_name`.
  3. *Phase 3 (Contract):* Deploy code reading and writing exclusively to `display_name`.
  4. *Phase 4 (Cleanup):* Drop the legacy `full_name` column in a future maintenance release.

### 14. Required Visuals
- *Visual M24-V3:* Pre-Ship Verification & Risk-Prioritized Release Gate Pipeline.

### 15. Failure Modes
- Deploying schema migrations that take exclusive table locks on large production tables during peak traffic.
- Shipping without correlation IDs in structured logs, making production incident triage impossible.

### 16. Non-Goals
- Implementing automated continuous deployment pipelines to commercial cloud infrastructure.
- Building complex multi-tenant billing systems.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Automated test suite passing for the target release; static linting clean; schema migration and rollback or roll-forward compatibility assertions pass.
- Reviewer-Required: Peer/Lead review of the pre-ship risk prioritization and deployment recovery readiness.

### 18. Source Grounding with Currentness Classification
- **Google SRE Book (Release Engineering & Canarying):** STABLE. Standard patterns for safe deployment and risk mitigation.
- **Martin Fowler (Evolutionary Database Design):** STABLE. Patterns for non-breaking schema migrations and expand-contract lifecycles.

---

## 23. M24 Capstone Defense Rubric & Assessment Contract

### 23.1 Purpose & Governance Authority
In accordance with the Stage 7 Task Contract, **Design owns the final learner/reviewer contract, scoring rubric, pass thresholds, and evidence sufficiency rules**. Module M24 is an integrative synthesis capstone; its assessment evaluates the learner's systems thinking, technical judgment, and architectural integrity.

### 23.2 Rejection of Arbitrary Universal Scoring Formulas
This curriculum rejects arbitrary numerical point aggregations (e.g., "earning 82 out of 100 points"). In real-world software systems, an application that scores 100% on performance but stores passwords in plaintext or corrupts data on power loss is **NOT** an 80% passing system—it is a catastrophic failure. Assessment is strictly binary and criteria-gated: all mandatory invariants must be preserved, and claims must be supported by sufficient evidence.

### 23.3 The 12 Evidence Areas & Sufficiency Criteria

To achieve a **PASS** in M24, the learner's capstone defense must provide adequate evidence across all 12 areas:

| Area | Evidence Dimension | Minimum Sufficiency Criterion | Valid Evidence Types |
|---|---|---|---|
| **E01** | End-to-End Request Flow | Complete trace from client action through network, OS, application, and storage back to client. | Architecture diagram, code walkthrough, network trace. |
| **E02** | State & Data Lifecycle | Explicit differentiation of volatile memory, durable storage, and replication state. | Dataflow schema, state machine specification, disk sync contract. |
| **E03** | Core Invariants & Specs | Explicit list of system invariants (data integrity, security boundaries, correctness guarantees). | Formal specifications, automated invariant assertion tests. |
| **E04** | Trust & Isolation Boundaries | Explicit mapping of where data crosses privilege domains; defense against ambient authority. | Threat model diagram, least-privilege configuration, sandbox rules. |
| **E05** | Failure Domains & Resilience | Analysis of single points of failure, crash recovery, network partitions, and cascading failure defense. | Failure mode effect analysis (FMEA), crash-recovery test logs. |
| **E06** | Transport & App Security | Defense against injection, transport snooping, unauthorized access, and supply-chain tampering. | TLS configuration, parameterized queries, CSRF/SSRF controls, lockfile hashes. |
| **E07** | Empirical Measurement | Question-driven performance profile under defined workload; defense against coordinated omission. | Monotonic timer logs, percentile distributions, steady-state detection. |
| **E08** | Capacity & Cost Models | Fermi back-of-the-envelope calculations for compute, RAM, storage, and egress bandwidth. | Mathematical calculations with explicit units and labeled assumptions. |
| **E09** | Trade-Off & Alternative Analysis | Structured evaluation of competing technologies using D-015; defense of at least one rejection. | D-015 Evaluation Card, formal Architecture Decision Record (ADR). |
| **E10** | Explicit Unknowns & Limits | Clear articulation of system limits, unmeasured edge cases, and areas requiring future study. | Documented limits section, bounded uncertainty statements. |
| **E11** | Changed-Constraint Adaptation | Coherent, reasoned redesign of system components in response to an adversarial constraint shift. | Written response analyzing new bottlenecks and modified invariants. |
| **E12** | Pre-Ship Operational Readiness | Verifiable rollback plan, health telemetry, and risk-prioritized verification checklist. | Migration rollback verification log, structured log schema, SLO definitions. |

### 23.4 Reviewer Evaluation Contract & Pass/Fail Determination
- **PASS:** The learner satisfies all 12 evidence areas; zero fatal security or data integrity flaws are present; the changed-constraint challenge is resolved with sound systems reasoning; all claims are backed by admissible evidence.
- **REVISE:** One or more evidence areas lack sufficient substantiation, or an architectural trade-off is hand-waved without quantitative or structural justification. The learner receives specific, actionable critique and resubmits the defense.
- **FAIL / BLOCKED:** The system exhibits critical invariant violations (e.g., plaintext password storage, unescaped SQL concatenation, unhandled crash corruption) or the learner fails to trace basic request lifecycles.


## 24. S7 Shared Preflight & Environment Capabilities Matrix (Preserving OQ-BP-006 OPEN)

### 24.1 Governance & Open Question Invariant
In accordance with repository governance, **Open Question `OQ-BP-006` (Canonical Tooling and Library Versions) remains OPEN in substance and policy**. Rather than freezing arbitrary language versions or package ranges in Design (e.g. mandating `cryptography >= 42.0.0`), Stage 7 specifies required **language and runtime capabilities**. All Required Core educational and verification workflows must function completely using standard library capabilities (`hashlib`, `hmac`, `secrets`, `socket`, `http.server`, `sqlite3`, `unittest`), treating third-party packages strictly as optional candidates detected at implementation time with exact version recheck.

### 24.2 Environment Capabilities Matrix

| Capability Category | Component / Module | Required Core Baseline Capability | Optional Candidate Enhancement | Fallback / Degradation Behavior |
|---|---|---|---|---|
| **Runtime Environment** | Python Interpreter | Standard CPython with modern typing, `dataclasses`, and `secrets` support | Latest stable CPython release | Preflight checks required module capabilities; emits `BLOCKED` if capability missing. |
| **Test Verification** | Test Framework | Python standard library `unittest` (Required Core test runner) | `pytest` test runner | Capability detection: if `pytest` is present, it may be used; otherwise `unittest` executes. Tests must not claim equivalent pass if an underlying mechanism is skipped. |
| **Networking** | Loopback Interface | OS loopback socket (`127.0.0.1`) with ephemeral dynamic port allocation | None required | If loopback binding fails, emit `BLOCKED: Socket bind permission denied`. |
| **Timer / Clock** | Monotonic Clock | `time.monotonic_ns()` (integer nanosecond units) | OS high-resolution hardware counters | Fallback to `time.monotonic()` if `monotonic_ns` is absent. Integer nanosecond units do not imply nanosecond clock resolution. |
| **Cryptographic Hashing** | Hash & MAC Primitives | `hashlib` (SHA-256), `hmac`, `secrets` | None required | Standard library universally present; zero external dependencies. |
| **Password Verifier** | Slow Hashing Functions | `hashlib.pbkdf2_hmac` (compute-hard, configurable iterations per policy) | `argon2-cffi` (Argon2id memory-hard per RFC 9106) | If `argon2-cffi` is missing, tests evaluate compute-hard PBKDF2; test reports truthful mechanism used. No fallback may claim memory-hard verification occurred if PBKDF2 was run. |
| **Token Profiles** | Token Validation | Course-owned bounded reference fixture using `hmac` + `hashlib` + `base64` + `json` for `TeachingProfile-BearerV1` | `pyjwt`, PyCA `cryptography` (e.g. current 50.0.1 candidate) | Capability detection: advanced asymmetric token tests run only when package is present; otherwise reported as `NOT RUN / CAPABILITY ABSENT`. |
| **Database** | Relational Storage | Built-in `sqlite3` in-memory (`:memory:`) or ephemeral temp files | External database server | Standard library SQLite requires zero external server processes. |
| **Web Server** | Localhost HTTP | Built-in `http.server`, `urllib.parse`, `urllib.request` | External ASGI/WSGI servers | Standard library server requires zero third-party packages. |
| **Process / Isolation** | Ephemeral Sandboxing | `tempfile.TemporaryDirectory()`, standard process context | Container runtimes | Zero assumption of container runtimes or root privileges. |

### 24.3 Prohibited Environmental Assumptions
Under no circumstances may any S7 activity or test suite assume:
1. Availability of the OpenSSL command-line utility (`openssl`);
2. Availability of `curl`, `wget`, or external HTTP CLI tools;
3. Availability of a graphical user interface (GUI) web browser;
4. Availability of Docker, Podman, or container virtualization runtimes;
5. Mandatory installation of third-party Python wheels (all activities run on standard library);
6. Active internet connectivity or remote cloud account credentials.

### 24.4 Preflight Verification Routine
Every test runner in S7 executes a lightweight preflight probe before test execution:
```python
def run_s7_preflight() -> dict:
    capabilities = {
        "python_capabilities": hasattr(hashlib, "pbkdf2_hmac") and hasattr(secrets, "token_bytes"),
        "loopback_bind": False,
        "monotonic_ns": hasattr(time, "monotonic_ns"),
        "has_argon2": False,
        "has_cryptography": False,
    }
    # Test loopback bind
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        capabilities["loopback_bind"] = True
        s.close()
    except Exception:
        pass

    # Detect optional candidate packages
    try:
        import argon2
        capabilities["has_argon2"] = True
    except ImportError:
        pass

    try:
        import cryptography
        capabilities["has_cryptography"] = True
    except ImportError:
        pass

    return capabilities
```

---

## 25. S7 Evidence Architecture & Template Contracts

### 25.1 The Six-Layer Evidence Taxonomy
To ensure rigorous epistemic hygiene, all architectural claims, student assignments, and evaluation artifacts in Stage 7 must explicitly categorize statements into one of six distinct evidence layers:

1. **`[PRINCIPLE]`**: Fundamental mathematical, computer science, or system invariants that hold universally across technologies (e.g., "Code and data must be structurally separated to prevent injection", "Cryptographic hash functions provide preimage resistance, second-preimage resistance, and collision resistance").
2. **`[SPECIFICATION / OFFICIAL CONTRACT]`**: Explicit requirements, RFCs, and formal standards published by authoritative governance bodies (e.g., NIST SP 800-63B-4, RFC 9846, RFC 9700, W3C CSP3, OpenSSF SLSA v1.2).
3. **`[IMPLEMENTATION]`**: Concrete code, libraries, syntax, and system interfaces realizing a specification (e.g., Python `hashlib.pbkdf2_hmac`, SQLite parameterized queries `?`, `hmac.compare_digest`).
4. **`[CURRENT PRACTICE]`**: Prevailing industry consensus, threat landscape realities, and contemporary operational patterns (e.g., deprecating SMS 2FA, enforcing OAuth 2.1 PKCE for public clients, nonce-based CSP).
5. **`[HOST / LEARNER OBSERVATION]`**: Verifiable empirical data collected on the learner's local machine (e.g., latency percentiles measured via monotonic timers, automated test output logs).
6. **`[COURSE REFERENCE EVIDENCE]`**: Canonical fixtures, benchmark baselines, and test assertions provided by the course repository.

### 25.2 Prohibition of Prefilled Volatile Values
Evidence collection templates provided to learners must be **strictly neutral**. Under no circumstances may an evidence template prefill volatile, host-dependent, or falsifiable values, including:
- Concrete timing values, milliseconds, or CPU cycle counts;
- Localhost ephemeral port numbers or operating system PIDs;
- Generated session tokens, cryptographic nonces, or random salts;
- Cryptographic hashes, digital signatures, or HMAC digests;
- Environment library version strings or host platform names;
- Benchmark "winners" or predetermined performance conclusions;
- Pre-filled `PASS` or success indicators.

### 25.3 Canonical Evidence Template Formats

#### Template 1: Cryptographic Primitive & Invariant Audit
```markdown
### Primitive Audit Record: [Scenario Name]
- **Required Security Property:** [Integrity (detection against trusted expected digest) | Authenticity | Confidentiality | Contextual Non-Repudiation (requiring key custody, identity binding, and verifier policy assumptions)]
- **Selected Standard Primitive:** [Hash | MAC | Digital Signature | AEAD Symmetric | Asymmetric]
- **Normative Specification:** [RFC / NIST Standard]
- **Chosen Implementation:** [Standard library module and function]
- **Invariant Verification:**
  - Nonce / Salt Strategy: [Description of randomness and collision-resistance / uniqueness guarantees]
  - Timing Mitigation API: [Function used for comparison to avoid content-based short-circuiting, e.g. hmac.compare_digest]
  - Error Handling & Information Leak Defense: [Exceptions caught, generic error responses]
```

#### Template 2: Empirical Systems Measurement Record
```markdown
### Measurement Protocol & Latency Record: [Workload Name]
- **Experimental Hypothesis:** [Clear statement of expected behavior]
- **Workload Model:** [Open Model (arrival schedule) | Closed Model (synchronous)]
- **Clock Source:** [Appropriate monotonic or performance clock, e.g., `time.monotonic_ns()` with noted resolution]
- **Warm-Up Criteria:** [Duration or iterations discarded before recording, or None if evaluating cold-start]
- **Coordinated Omission Handling:** [Arrival-time tracking if open arrival model, or N/A if closed model]
- **Empirical Results (Learner to Record):**
  - Sample Count ($n$): `[TO BE RECORDED]`
  - Summary Metrics (Percentiles, Mean/Std, or Histogram as appropriate to question): `[TO BE RECORDED]`
- **Distribution Shape:** [Unimodal | Bimodal | Heavy-Tailed | Multimodal | Symmetric]
- **Inference & Decision:** [Conclusions supported strictly by the data above]
```

---

## 26. Progressive-Support Contract & Strict Rules

### 26.1 Mandatory Pedagogical Scaffolding Hierarchy
Every lesson in Stage 7 must provide structured scaffolding for challenging exercises. Scaffolding must strictly adhere to the five-stage progressive disclosure contract:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Driving Question                                         │
│    Framed around a real-world engineering or security challenge
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Hint 1: Conceptual Direction                             │
│    Points the learner to the relevant boundary or invariant │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Hint 2: Mechanism / Structural Pointer                   │
│    Identifies the underlying parser, timer, or data flow    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Expected Observation                                     │
│    Describes the relationship or pattern to look for        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Full Explanation                                         │
│    Comprehensive technical breakdown of root cause and fix  │
└─────────────────────────────────────────────────────────────┘
```

### 26.2 Strict Formatting & Integrity Rules
1. **No `<details open>`:**
   HTML disclosure tags (`<details>`) must NEVER include the `open` attribute by default. Solutions must remain collapsed until deliberately opened by the learner.
2. **Relationship-Based Expected Observations:**
   Expected observations must describe qualitative relationships, failure patterns, or structural behaviors (e.g., "Observe that the synchronous benchmark reports a p99 lower than the injected stall duration", "Observe that the SQL parser treats `admin' --` as a comment delimiter"). They must NEVER contain pre-filled fake numbers, hardcoded timestamps, or simulated benchmark victories.
3. **No Skipping Steps:**
   Lessons must never jump straight from a question to the full code solution. Hints 1 and 2 must scaffold independent learner deduction.

---

## 27. Visual Design Specifications (15 Visuals)

To guide visual asset production without generating raw binary files prematurely, the following 15 visual specifications define the structure, conceptual layers, flows, and ASCII layout blueprints for Stage 7.

### 27.1 Module M21 Visual Specifications

#### Visual M21-V1: Trust Boundary & Authority Map across Layers
- **Purpose:** Illustrate where trust boundaries divide components and show how ambient authority is restricted.
- **Layers:** Client Browser → Reverse Proxy (TLS Termination) → Web Worker (Process Sandbox) → OS Kernel & Filesystem.
- **Layout Blueprint:**
```
[ UNTRUSTED CLIENT ]
        │  (Untrusted Network Data)
════════╪═════════════════════════════════════════════════════════ [ NETWORK TRUST BOUNDARY ]
        ▼
[ REVERSE PROXY / TLS TERMINATION ]
        │  (Plain HTTP Stream / Parsed Headers)
════════╪═════════════════════════════════════════════════════════ [ PROCESS TRUST BOUNDARY ]
        ▼
[ APPLICATION WORKER (Least Privilege User) ]
        │  (Sanitized Path / Parameterized Query)
════════╪═════════════════════════════════════════════════════════ [ KERNEL / STORAGE BOUNDARY ]
        ▼
[ SECURE FILESYSTEM / DATABASE STORAGE ]
```

#### Visual M21-V2: Cryptographic Primitives Taxonomy
- **Purpose:** Provide a clear mental model distinguishing Hash, MAC, Digital Signature, and AEAD.
- **Axes:** Keys Involved (None vs Shared Secret vs Keypair) vs Operational Goal (Integrity vs Authenticity vs Confidentiality).
- **Layout Blueprint:**
```
┌──────────────────┬─────────────────┬─────────────────┬────────────────────────────────┬────────────────────────────────┐
│ Primitive Class  │ Key Required    │ Math Transform  │ Security Guarantees            │ Non-Guarantees / Boundaries    │
├──────────────────┼─────────────────┼─────────────────┼────────────────────────────────┼────────────────────────────────┤
│ Hash (SHA-256)   │ None            │ One-Way Digest  │ Integrity vs Expected Digest   │ No authenticity against active │
│                  │                 │                 │ (Detects accidental corruption)│ adversary (attacker recomputes)│
│ MAC (HMAC-SHA256)│ 1 Shared Secret │ Keyed Hash      │ Integrity + Authenticity       │ Both parties share secret;     │
│                  │                 │                 │ (Proves key holder created it) │ cannot distinguish sender/recv │
│ Signature (Ed/EC)│ Keypair (Priv/Pub) Asymmetric Math │ Verifiable under Public Key    │ Non-repudiation depends on key │
│                  │                 │                 │ (Only private key can sign)    │ custody, binding & verifier pol│
│ AEAD (AES-GCM)   │ 1 Shared Secret │ Cipher + AuthTag│ Confidentiality + Authenticity │ Nonce must NEVER be reused;    │
│                  │                 │                 │ (Plaintext hidden & untampered)│ no public verification         │
└──────────────────┴─────────────────┴─────────────────┴────────────────────────────────┴────────────────────────────────┘
```

#### Visual M21-V3: The 6-Layer PKI Trust and Verification Architecture
- **Purpose:** Demystify how TLS establishes verified trust without circular reasoning.
- **The 6 Layers:**
```
[ Layer 1: Certificate Credential ] ── Public key + Subject metadata (X.509)
              │
              ▼
[ Layer 2: Path Validation ] ──────── Cryptographic chain of signatures to trusted root (RFC 5280)
              │
              ▼
[ Layer 3: Service Identity Binding ]  SAN check: hostname matches certificate subject (RFC 9525)
              │
              ▼
[ Layer 4: Proof of Possession ] ──── Client verifies server possesses private key (TLS Handshake; RFC 9846 forward secrecy via DHE/ECDHE)
              │
              ▼
[ Layer 5: Authentication ] ───────── Verified identity of endpoint confirmed
              │
              ▼
[ Layer 6: Authorization ] ────────── Permissions evaluated for confirmed identity
```

### 27.2 Module M22 Visual Specifications

#### Visual M22-V1: Authentication vs. Authorization Request Decision Path
- **Purpose:** Contrast identifying *who* is calling with deciding *what* they can do.
- **Layout Blueprint:**
```
[ Incoming Request + Bearer Token ]
                │
                ▼
      { Valid Signature? } ─────────── NO ──► [ HTTP 401 Unauthorized ]
                │ YES
                ▼
      { Token Expired / Revoked? } ─── YES ──► [ HTTP 401 Unauthorized ]
                │ NO
        [ Authenticated Identity: User #42 ]
                │
                ▼
      { User #42 Allowed on Resource? } ── NO ──► [ HTTP 403 Forbidden ]
                │ YES
        [ Execute Business Logic ] ────────────► [ HTTP 200 OK ]
```

#### Visual M22-V2: OAuth 2.1 Authorization Code Flow with PKCE Architecture
- **Purpose:** Map the modern OAuth 2.1 standard flow per RFC 9700, showing PKCE protection for public clients.
- **Layout Blueprint:**
```
Learner App (Client)          Browser / User             Authorization Server (IdP)
       │                            │                               │
       │ 1. Generate code_verifier  │                               │
       │    and code_challenge      │                               │
       │ 2. Redirect with challenge ───────────────────────────────►│
       │                            │ 3. User Authenticates & Grants│
       │◄───────────────────────────── 4. Redirect with auth code ──│
       │                                                            │
       │ 5. POST /token (code + code_verifier) ────────────────────►│
       │    (IdP verifies SHA256(code_verifier) == code_challenge)   │
       │◄───────────────────────────── 6. Return access token ──────│
```

#### Visual M22-V3: Code vs. Data: Parameterized API / Driver Boundary in SQL Queries
- **Purpose:** Contrast vulnerable SQL string construction with the parameterized API/driver contract that keeps value data separate from SQL syntax; exact parser/bytecode mechanics remain engine-specific.
- **Layout Blueprint:**
```
CONCATENATION:
  "SELECT * FROM users WHERE name = '" + "admin' OR '1'='1" + "'"
  AST Parsed AFTER Concatenation:
  Query ──► WHERE ──► OR ──► BinaryOp (=) ──► True! (Syntax Altered!)

PARAMETERIZED (Driver / API Contract Separation):
  SQL: "SELECT * FROM users WHERE name = ?"  Param: "admin' OR '1'='1"
  API Contract Enforces Separation:
  Driver/Engine compiles query structure treating '?' strictly as a parameter value placeholder.
  User input is bound directly as data literal, never evaluated as SQL syntax.
  (Exact mechanism is engine-specific: SQLite compiles bytecode placeholders; PostgreSQL uses server-side prepared statements).
```

#### Visual M22-V4: Browser Vulnerabilities & Defensive Boundaries (XSS, CSRF, SSRF)
- **Purpose:** Map the three browser-mediated vulnerabilities and their exact architectural mitigation boundaries.
- **Layout Blueprint:**
```
┌──────────────┬─────────────────────────┬────────────────────────┬─────────────────────────────┬─────────────────────────────┐
│ Threat Class │ Execution Boundary      │ Attack Mechanism       │ Mechanism & Enforcement Pt  │ Non-Guarantees / Limits     │
├──────────────┼─────────────────────────┼────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ XSS          │ Browser DOM / Parser    │ Script injected in HTML│ Context-aware autoencoding; │ Does not stop server-side   │
│              │                         │ execution context      │ W3C CSP3 strict nonces      │ template injection or clobbr│
│ CSRF         │ Cross-Origin HTTP Hop   │ Ambient credential     │ SameSite cookies; explicit  │ SameSite=Lax allows GET nav;│
│              │                         │ (cookie) auto-attach   │ Authorization headers; token│ mutation on GET remains vul │
│ SSRF         │ Server Outbound Egress  │ Server coerced to fetch│ Parsed IP destination check;│ URL regex allowlists fail;  │
│              │                         │ internal resource      │ post-resolve socket bind    │ DNS rebinding bypasses check│
└──────────────┴─────────────────────────┴────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

#### Visual M22-V5: The 9-Layer Software Supply Chain Integrity Model
- **Purpose:** Structure software supply chain defense into nine progressive concerns from resolution to verifier policy.
- **The 9 Layers:**
```
[ Layer 1: Resolution Pinning ] ────── Semantic version ranges frozen in lockfile
             │
             ▼
[ Layer 2: Expected Digest Ownership ] Trusted lockfile/repository governing expected hashes
             │
             ▼
[ Layer 3: Fetched-Byte Integrity ] ── Cryptographic SHA-256 check against expected digest
             │
             ▼
[ Layer 4: Build Reproducibility ] ── Byte-for-byte independent build verification
             │
             ▼
[ Layer 5: Signature Verification ] ── Cryptographic signature check on package archive
             │
             ▼
[ Layer 6: Signer Identity Binding ] ─ Verifying signing key belongs to authorized maintainer
             │
             ▼
[ Layer 7: Build/Source Provenance ] ─ Binding git commit and builder identity
             │
             ▼
[ Layer 8: Trusted Builder ] ───────── Evaluating isolated, authenticated build platform
             │
             ▼
[ Layer 9: Verifier Policy ] ───────── Enforcing that attestation satisfies deployment gates
```

### 27.3 Module M23 Visual Specifications

#### Visual M23-V1: Scientific Systems Measurement Architecture
- **Purpose:** Detail the pipeline from hypothesis to unskewed empirical distribution.
- **Layout Blueprint:**
```
[ Formal Hypothesis ] ──► [ Workload Generator (Open or Closed Model per Question) ]
                                            │
                                            ▼
                                 [ System Under Test ]
                                            │
                                 (Monotonic / Performance Clock)
                                            ▼
                                 [ Discard Warm-Up Transients (When Applicable) ]
                                            │
                                            ▼
                                 [ Latency Distribution & Histogram ]
                                            │
                                            ▼
                                 [ Summary Metrics: Appropriate Percentiles, Moments, or Histograms ]
```

#### Visual M23-V2: Coordinated Omission: How Synchronous Clients Hide Queuing Delays
- **Purpose:** Demonstrate visually why synchronous benchmark loops report false low latencies during server stalls.
- **Layout Blueprint:**
```
REAL ARRIVAL SCHEDULE:
Req 1 (t=0)   Req 2 (t=10)  Req 3 (t=20)  Req 4 (t=30)  Req 5 (t=40)
───┼─────────────┼─────────────┼─────────────┼─────────────┼───────► Time (ms)

SERVER STALLS FOR 50ms AT t=5:
Synchronous Loop Behavior:
Req 1 sent at t=0, blocks until t=55. (Recorded: 55ms)
Req 2 sent at t=55, finishes at t=60. (Recorded: 5ms!)
Req 3, 4, 5 were NEVER SENT during the stall!
Result: Benchmark records [55ms, 5ms] -> Average = 30ms.
REALITY: Req 2 waited 45ms in queue! Real p99 was devastated!
```

#### Visual M23-V3: Decision D-015 12-Dimension Technology Evaluation Framework
- **Purpose:** Display the 12 comprehensive dimensions of technology evaluation in a structured radar/card layout.
- **Dimensions:** Problem Fit, Data Model, Guarantees, Failure Modes, Scalability, Observability, Security, Maintenance, Licensing, Cost, Reversibility, Alternatives/Rejection.

#### Visual M23-V4: Systems Cost & Resource Bottleneck Hierarchy
- **Purpose:** Map the trade-offs between physical hardware, network bandwidth, cloud financial billing, and human engineering friction.
- **Layout Blueprint:**
```
                  ▲
                 ╱ ╲   Human Cognitive Load & On-Call Maintenance
                ╱   ╲  (Highest long-term operational cost)
               ╱─────╲
              ╱       ╲  Network Egress & Inter-Region Bandwidth
             ╱         ╲ (Variable financial multiplier)
            ╱───────────╲
           ╱             ╲ Compute (CPU Cores) & Dynamic Memory (RAM)
          ╱               ╲ (High-frequency resource bottlenecks)
         ╱─────────────────╲
        ╱                   ╲ Durable Storage & Block IOPS
       ╱─────────────────────╲ (Persistent capacity baseline)
```

### 27.4 Module M24 Visual Specifications

#### Visual M24-V1: The 16 Core Architectural Traces Matrix
- **Purpose:** Provide a structural grid showing how an architect traces an entire system across logical and physical domains.
- **Grid Categories:** Flow Traces (Request, Data, Control), Structural Inventories (State, Invariants, Boundaries), Resilience Analyses (Failures, Security, Performance), Decision Rationale (Costs, Alternatives, Unknowns).

#### Visual M24-V2: The Evidence-to-Claim Mapping Framework
- **Purpose:** Connect architectural claims directly to admissible evidence types, illustrating evidence sufficiency across scenario examples.
- **Layout Blueprint:**
```
Architectural Claim (Example) ──► Required Evidence Category ──► Admissible Artifacts (Examples)
─────────────────────────────────────────────────────────────────────────────────────────────
"Crash-Resilient State"   ────► Failure & Recovery Proof    ──► Crash Injection Log / WAL Invariant Proof
"Service SLO (Scenario Target)► Empirical Measurement       ──► Monotonic Arrival Benchmark & Distribution
"Secure from Injection"   ────► Parameterized API Contract  ──► Prepared Statement Driver Calls + Tests
"Cost / Resource Budget"  ────► Capacity / Cost Model       ──► Fermi Sizing Bounds + Hardware/Host Pricing
```

#### Visual M24-V3: Pre-Ship Verification & Risk-Prioritized Candidate Release Gate Pipeline
- **Purpose:** Detail a risk-driven candidate structure for release verification whose specific checks depend on the actual learner system architecture and operational constraints.
- **Layout Blueprint:**
```
[ Candidate Code/System ] ──► [ Risk-Prioritized Candidate Gate 1: Core Invariant & Regression Tests ]
                                            │
                                            ▼
                              [ Candidate Gate 2: Security Boundaries & Dependency Integrity Audit ]
                                            │
                                            ▼
                              [ Candidate Gate 3: Empirical Workload / Baseline Check (When Required) ]
                                            │
                                            ▼
                              [ Candidate Gate 4: Evolution & Reversal Strategy (Rollback / Roll-Forward Check) ]
                                            │
                                            ▼
                              [ Candidate Gate 5: Telemetry, Observability & Structured Logging Check ]
                                            │
                                            ▼
                              [ RELEASE DECISION (e.g., Staged/Canary Rollout or Direct Cutover per Architecture) ]
```


## 28. Authoritative Sources, Currentness Recheck & Provenance Register

### 28.1 Normative Source Register & Currentness Audit
All normative claims in Stage 7 are grounded in authoritative technical specifications re-checked at Design execution time (September 2026).

| Source Identifier | Version / Revision | Publication Date | Formal Status | Checked Date | Claim Supported | Boundary / What Source Does Not Prove | Drift Classification | Rights & Licensing Boundary |
|---|---|---|---|---|---|---|---|---|
| **NIST SP 800-63B-4** | Final Revision 4 (§3.1.1.2) | July 2025 | Official US Gov Standard | 2026-09-07 | Password storage: passwords SHALL be salted (salt >= 32 bits chosen to minimize collisions) and hashed; cost factor SHOULD be as high as practical without negatively impacting verifier performance and increased over time; approved scheme in latest SP 800-132 (currently PBKDF2; revision planned) or updated guidance SHOULD be used; verifier SHOULD permit max length >= 64 chars without truncation; single-factor >= 15 chars, MFA >= 8 chars; composition rules abolished. | Does not mandate Argon2id (RFC 9106 is IETF candidate); does not endorse commercial password managers or hardware tokens. | **CURRENT** | US Gov work; not subject to copyright protection within the United States; foreign rights may apply per D-016; attribution required. |
| **NIST SP 800-132** | Recommendation for Password-Based Key Derivation | December 2010 | Official US Gov Standard (Revision Planned) | 2026-09-07 | Specifies PBKDF2 as an approved compute-hard / time-hard key derivation and password hashing scheme. NIST announced decision in 2023 to revise SP 800-132 to add an additional memory-hard scheme; current Final remains December 2010 PBKDF2. | PBKDF2 is compute-hard, NOT memory-hard; does not specify Argon2id (revision not yet finalized). | **CURRENT** | US Gov work; not subject to copyright protection within the United States; foreign rights may apply per D-016. |
| **FIPS 198-1** | Federal Information Processing Standard 198-1 | **July 2008** (Supersedes FIPS 198, March 2002) | Active Federal Standard (NIST proposal to withdraw dated 23 June 2025) | 2026-09-07 | The Keyed-Hash Message Authentication Code (HMAC) specification. Notes NIST planning note (23 June 2025) proposing to withdraw FIPS 198-1 and transition HMAC to SP 800-224. | Does not prove confidentiality or contextual non-repudiation. | **STABLE / CURRENT** | US Gov work; not subject to copyright protection within the United States; foreign rights may apply per D-016. |
| **NIST SP 800-224 (draft)** | Initial Public Draft | **28 June 2024** | Initial Public Draft (Draft successor to FIPS 198-1) | 2026-09-07 | Draft successor specification for HMAC and related keyed-hash mechanisms under NIST 23 June 2025 transition plan. | Initial public draft; not yet a final approved standard. | **CURRENT / FRONTIER** | US Gov work; not subject to copyright protection within the United States; foreign rights may apply per D-016. |
| **NIST SP 800-131A Rev. 2 / Rev. 3 IPD** | Rev. 2 (active) / Rev. 3 (Initial Public Draft) | Oct 21, 2024 (draft) | Active Standard / Draft in progress | 2026-09-07 | Transitioning cryptographic algorithms; SHA-1 disallowed for signatures; 112-bit security deprecated. | Rev. 3 is a draft and not yet final normative policy. | **CURRENT / FRONTIER** | US Gov work; not subject to copyright protection within the United States; foreign rights may apply per D-016. |
| **RFC 9846** | Standards Track | July 2026 | Proposed Standard (Obsoletes RFC 5077, 5246, 6961, 7627, 8422, 8446; updates RFC 5705, 6066) | 2026-09-07 | TLS 1.3 protocol specification; forward secrecy scoped to DHE/ECDHE key exchange; AEAD only; encrypted handshakes. | Does not provide forward secrecy in PSK-only mode (`psk_ke`) or 0-RTT early data. | **STABLE / CURRENT** | IETF Trust Legal Provisions (TLP) Section 4/5; Code Components under BSD 3-Clause. |
| **RFC 9525** | Standards Track | **November 2023** | Proposed Standard (Obsoletes RFC 6125) | 2026-09-07 | Service identity verification in TLS; MUST check SAN, MUST NOT use CN fallback. | Does not validate application-layer authorization policies. | **STABLE / CURRENT** | IETF TLP Section 4/5; Code Components under BSD 3-Clause. |
| **RFC 9700 / BCP 240** | Best Current Practice 240 | January 2025 | IETF Best Current Practice | 2026-09-07 | OAuth 2.0 Security BCP: PKCE MUST for public, RECOMMENDED for confidential; ROPC MUST NOT; Implicit Grant SHOULD NOT; exact redirect matching. | Does not define identity assertion schemas (handled by OpenID Connect). | **CURRENT** | IETF TLP Section 4/5; Code Components under BSD 3-Clause. |
| **draft-ietf-oauth-v2-1-15** | Working Group Draft | March 2026 | Active Internet-Draft | 2026-09-07 | Consolidated OAuth 2.1 authorization framework incorporating BCP 240; removes Implicit Grant. | Draft status; subject to minor text revisions before final RFC publication. | **CURRENT / FRONTIER** | IETF Trust copyright under TLP. |
| **draft-ietf-httpbis-layered-cookies-02** | Internet-Draft (Revision 02) | **21 May 2026** | Active Internet-Draft (IETF HTTPbis WG) | 2026-09-07 | SameSite cookie semantics (`Strict`, `Lax`, `None`), cookie prefixes (`__Host-`, `__Secure-`), and layered cookie architecture bounding ambient authority. | Active draft subject to revision and draft churn; does not replace CSRF tokens or transport security; browser implementations vary. | **CURRENT / FRONTIER** | IETF Trust Legal Provisions (TLP) Section 4/5; Code Components under BSD 3-Clause. |
| **W3C CSP Level 3** | Working Draft | 29 July 2026 | W3C Working Draft (Active Current Source) | 2026-09-07 | Nonce-based Content Security Policy (`'strict-dynamic'`) for script execution. | Does not prevent server-side template injection or DOM clobbering; working draft subject to ongoing refinement. | **CURRENT / FRONTIER** | W3C Document License; freely citeable. |
| **RFC 9106** | Informational | September 2021 | IETF Informational (Argon2) | 2026-09-07 | Memory-hard password hashing algorithm (Argon2id). | Does not replace transport encryption or database security. | **STABLE** | RFC Editor / IETF TLP Section 4/5. |
| **OpenSSF SLSA v1.2** | Specification v1.2 | **24 November 2025** | Approved (v1.0 retired) | 2026-09-07 | Supply chain levels for software artifacts; verifiable build provenance attestations. | Does not guarantee that source code is free of developer-authored bugs. | **CURRENT** | Community Specification License 1.0; open attribution. |
| **PyCA cryptography** | v50.0.1 (candidate) | August 25, 2026 | Production Python Package | 2026-09-07 | Candidate reference Python cryptographic library with capability detection. | Package is an optional candidate enhancement; not required for Required Core baseline pass. | **CURRENT** | Dual-licensed Apache 2.0 / BSD 3-Clause. |

---

## 29. Concept & Competency Audit (18 Concepts, 8 Competencies)

### 29.1 Total Canonical Concept Preservation
The total number of canonical concepts across the entire curriculum remains **exactly 18**, as defined in `meta/CONCEPT_REGISTRY.md`. **Exactly ZERO new Concept IDs are introduced in Stage 7.**

### 29.2 First-Home Invariant Audit
All concept first-home assignments remain inviolate:
- `EC-CON-017 Trust Boundary` (信任边界): First home remains **M07 `L07-01`**. Modules M21 and M22 perform architectural synthesis and contextual revisits; they do not claim first-home ownership.
- `EC-CON-013 Isolation` (隔离): First home remains **M07 `L07-01`**.
- `EC-CON-007 Specification` (规约): First home remains **M02 `L02-03`**.
- `EC-CON-008 Invariant` (不变式): First home remains **M02 `L02-03`**.
- `EC-CON-009 Correctness` (正确性): First home remains **M02 `L02-03`**.
- `EC-CON-010 Failure` (失效与故障): First home remains **M03 `L03-03`**.
- `EC-CON-016 Durability` (持久性): First home remains **M09 `L09-01`**.
- `EC-CON-014 Consistency` (一致性): First home remains **M14 `L14-02`**.
- `EC-CON-015 Concurrency` (并发): First home remains **M15 `L15-01`**.
- `EC-CON-018 Process` (进程): First home remains **M06 `L06-01`**.
- `Consensus`: Registry ID remains deliberately deferred per Decision D-025.

### 29.3 Canonical Competency Vocabulary & Per-Lesson Mapping
Stage 7 exclusively utilizes the 8 canonical competency verbs defined in `meta/COMPETENCY_MATRIX.md`:
`Trace`, `Explain`, `Observe`, `Diagnose`, `Correctness`, `Judge`, `Estimate`, `Learn-New-Tech`.

Every lesson's primary competency assignment matches the accepted canonical Blueprint row (`meta/blueprint/core-stage-module-lesson-map-v0.1.md`):

| Lesson ID | Module | Lesson Title / Driving Question | Canonical Blueprint Primary Competencies |
|---|---|---|---|
| `L21-01` | M21 | "Where are the boundaries I must protect?" | `Judge, Explain, Diagnose` |
| `L21-02` | M21 | "What do I use crypto for?" | `Explain, Judge, Learn-New-Tech` |
| `L22-01` | M22 | "How do I know who is calling?" | `Judge, Explain` |
| `L22-02` | M22 | "Why is my web app vulnerable?" | `Diagnose, Judge, Explain` |
| `L22-03` | M22 | "Why do I trust my dependencies?" | `Learn-New-Tech, Judge` |
| `L23-01` | M23 | "How do I measure honestly?" | `Estimate, Judge, Diagnose` |
| `L23-02` | M23 | "How do I pick a technology?" | `Judge, Learn-New-Tech, Explain` |
| `L23-03` | M23 | "What is the cost of my design?" | `Estimate, Judge` |
| `L24-01` | M24 | "Can I defend an architecture?" | `Judge, Explain, Diagnose, Estimate` |
| `L24-02` | M24 | "What should I measure before I ship?" | `Judge, Diagnose` |

---

## 30. Machine-Checkable vs. Reviewer-Required Verification Matrix

Verification gates map directly to canonical primary competencies across all 10 lessons. Machine-checkable suites run via Python standard library `unittest` for Required Core (capability-gating `pytest` when present):

| Module | Lesson | Primary Competencies | Machine-Checkable Gates (Automated Test Suites: `unittest`) | Reviewer-Required Gates (Web Lead / Peer Review) |
|---|---|---|---|---|
| **M21** | `L21-01` | `Judge, Explain, Diagnose` | Path sanitization assertion (rejecting `../` traversal, null bytes, out-of-sandbox targets). | Evaluation of threat model boundary diagram, privilege assessment, and asset inventory (`Judge`, `Explain`). |
| **M21** | `L21-02` | `Explain, Judge, Learn-New-Tech` | `python -m unittest labs/foundations/m21/test_m21.py`: HMAC authentication failure on tamper, unkeyed hash tamper demonstration, `compare_digest` usage. | Review of Primitive Selection Matrix and explanation of crypto roles/misuse boundaries (`Explain`, `Judge`). |
| **M22** | `L22-01` | `Judge, Explain` | `python -m unittest labs/foundations/m22/test_m22.py`: Password verifier salt uniqueness and slow hash execution; token profile rejection for forged signature, expired timestamp, wrong audience, and `alg: "none"`. | Review of password storage policy rationale, token profile boundaries, and stateful vs stateless revocation trade-offs (`Judge`, `Explain`). |
| **M22** | `L22-02` | `Diagnose, Judge, Explain` | Parameterized query execution verifying syntax preservation; CSRF token validation; SSRF post-resolve socket destination check. | Architectural review of code vs data separation, context-aware escaping, and egress socket binding (`Diagnose`, `Judge`). |
| **M22** | `L22-03` | `Learn-New-Tech, Judge` | Lockfile parser test validating SHA-256 hash checks and rejecting tampered digests. | Inspection of 9-layer supply chain evaluation and third-party dependency adoption policy (`Learn-New-Tech`, `Judge`). |
| **M23** | `L23-01` | `Estimate, Judge, Diagnose` | Unit test proving arrival-scheduled benchmark records scheduled queuing delay under synthetic stalls. | Review of Measurement Protocol Card, stated arrival assumptions, and question-driven metric selection (`Estimate`, `Judge`). |
| **M23** | `L23-02` | `Judge, Learn-New-Tech, Explain` | Schema validation of ADR ensuring all 12 dimensions of Decision D-015 are completed. | Qualitative evaluation of technology trade-off reasoning and defense of technology rejection (`Judge`, `Explain`). |
| **M23** | `L23-03` | `Estimate, Judge` | Numeric calculation verification of storage growth, egress bandwidth, and memory sizing. | Review of stated Fermi assumptions, unit consistency (b vs B), and bottleneck sensitivity analysis (`Estimate`, `Judge`). |
| **M24** | `L24-01` | `Judge, Explain, Diagnose, Estimate` | Automated validation of 16-trace completeness in capstone defense document. | In-depth architectural defense evaluation, evidence sufficiency audit, and response to changed-constraint challenge on actual system (`Judge`, `Explain`, `Diagnose`, `Estimate`). |
| **M24** | `L24-02` | `Judge, Diagnose` | Pre-flight test suite pass, schema migration compatibility check, structured health check response. | Review of scenario-card release criteria, stated data-loss bounds, and operational readiness (`Judge`, `Diagnose`). |

---

## 31. Safety, Watchdogs & Deterministic Cleanup Design

To protect host hardware, ensure reliable CI test runs, and strictly adhere to the Hardware Safety Rules:

1. **Zero Uncontrolled Disk Writes & Debounce Guarantees:**
   - All ephemeral test databases run in-memory (`:memory:`) or within an auto-cleaning `tempfile.TemporaryDirectory()`.
   - Logging and metrics exercises enforce memory buffers with periodic flush intervals (minimum debounce >= 2000ms in interactive tools).
   - Zero physical disk thrashing or repeated full-disk scans.

2. **Deterministic Fail-Closed Process & Socket Teardown:**
   - All localhost servers (`http.server` instances in M22) run in explicitly owned, non-daemon threads with dedicated lifecycle management:
     ```python
     server = HTTPServer(("127.0.0.1", 0), SafeHandler)
     server_thread = threading.Thread(target=server.serve_forever)
     server_thread.start()
     try:
         yield server
     finally:
         server.shutdown()
         server.server_close()
         server_thread.join(timeout=2.0)
         if server_thread.is_alive():
             raise RuntimeError("FAIL: Server thread failed to terminate cleanly")
         # Post-cleanup listener verification
         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
             probe.settimeout(0.2)
             if probe.connect_ex(("127.0.0.1", server.server_address[1])) == 0:
                 raise RuntimeError("FAIL: Lingering listener detected on test port")
     ```
   - All client socket connections enforce explicit timeouts (`timeout=2.0`).
   - Cleanup failure surfaces as `FAIL / BLOCKED`, never silent pass.

3. **Bounded Configurable Watchdogs:**
   - Network activities and benchmark harnesses include configurable, bounded watchdog timers (justified as fixture policy, not hidden universal constants) that terminate blocking sockets and fail closed if a deadlock occurs.

4. **Zero State Pollution:**
   - Ephemeral files, mock lockfiles, and temporary database files are wiped deterministically in fixture teardown routines.

---

## 32. Implementation Handoff, Mini Cloud App Security Review Checkpoints & Non-Blocking Risks

### 32.1 Mini Cloud App Security Review Checkpoints
Rather than treating security as an isolated theoretical topic, Stage 7 integrates security reviews directly into the learner's longitudinal Mini Cloud App project:

- **Checkpoint P2 (Data Storage & Serialization Review — M21):**
  - Verify that database storage enforces parameterized queries;
  - Verify that file storage enforces strict path sandboxing;
  - Audit password hashing implementation against NIST SP 800-63B-4.
- **Checkpoint P8 (Transport & Endpoint Authentication Review — M22):**
  - Verify that API endpoints separate authentication from authorization;
  - Verify that JWTs or session cookies enforce audience, expiration, and `SameSite` flags;
  - Audit webhook and egress HTTP requests against SSRF.
- **Checkpoint P9 (Deployment & Supply Chain Review — M22 / M24):**
  - Audit `requirements.txt` or lockfile for cryptographic hash pinning;
  - Verify that process environment secrets are not committed to source control;
  - Document the 16 core architectural traces for the final capstone defense.

### 32.2 Governance Status & Non-Blocking Known Risks
- **`OQ-BP-001` (AI Literacy & Bounded AI Use):** Remains **OPEN / RFC-GATED**. AI outputs are treated as unverified hypotheses. Core scope is preserved without premature AI expansion.
- **`OQ-BP-003` (Human-Facing Curriculum Boundary):** Remains **OPEN / RFC-GATED**.
- **`OQ-BP-006` (Canonical Tooling Versions):** Remains **OPEN**. Pinned at implementation time.
- **Issue #34 (Real Learner Validation):** Remains **OPEN / DEFERRED / NON-BLOCKING** per Decision D-027.
- **Historical Runtime Debts:** M03 GDB platform availability debt on Windows and M06 course-fork grader NOT RUN debt remain preserved as documented non-blocking baselines.

---

## 33. 40-Gate Verification Audit Table

Every gate required by the Issue #114 Task Contract has been audited and evaluated truthfully against the Round 1 rework:

| Gate # | Verification Gate Description | Status | Evidence / Architectural Location |
|---|---|---|---|
| **01** | Exact canonical-base ancestry | **PASS** | Branch branched directly from `main @ 35fe098416709255b295099e9e1703942c84b482`. |
| **02** | Design-only scope | **PASS** | Zero markdown lessons drafted; zero lab fixtures implemented in `labs/` or `project/`. |
| **03** | Exactly one primary Design dossier | **PASS** | Exactly one file: `meta/design/security-synthesis-judgment-m21-m24-design-v0.1.md`. |
| **04** | M21–M24 all covered | **PASS** | Complete structural and pedagogical specifications for M21, M22, M23, and M24. |
| **05** | Exact Module DAG | **PASS** | Section 2.1 preserves exact inputs (M21: M11+M07+M12/M09; M22: M21+M11+M12/M19; M23: M20+M21/M22+M17; M24: M23/M20). |
| **06** | Exactly 10 Lesson IDs/questions | **PASS** | Section 2.2 lists all 10 canonical lessons with exact driving questions. |
| **07** | No new hard edges | **PASS** | Verified DAG introduces zero new hard prerequisite dependencies. |
| **08** | All 10 Lessons have complete 18-point Design contract | **PASS** | Sections 7, 8, 11, 12, 13, 16, 17, 18, 21, 22 provide all 18 specifications per lesson. |
| **09** | No new Concept IDs | **PASS** | Section 29.1 confirms total canonical concepts remain exactly 18. |
| **10** | No Concept first-home moves | **PASS** | Section 29.2 confirms all first-home assignments remain strictly unaltered. |
| **11** | Trust Boundary remains M07/L07-01 | **PASS** | `EC-CON-017 Trust Boundary` first home is preserved in M07 `L07-01`; M21/M22 are revisits. |
| **12** | Only canonical competency vocabulary & exact Blueprint primaries | **PASS** | Section 29.3 and Section 30 restore exact canonical Blueprint primary mappings across all 10 lessons (L21-01: Judge/Explain/Diagnose; L21-02: Explain/Judge/Learn-New-Tech; L22-01: Judge/Explain; L22-02: Diagnose/Judge/Explain; L22-03: Learn-New-Tech/Judge; L23-01: Estimate/Judge/Diagnose; L23-02: Judge/Learn-New-Tech/Explain; L23-03: Estimate/Judge; L24-01: Judge/Explain/Diagnose/Estimate; L24-02: Judge/Diagnose). Evidence mapped directly to primaries. |
| **13** | M21 crypto-use / no crypto-implementation boundary | **PASS** | Sections 6.2, 8, 9 strictly enforce crypto-use with standard library primitives (`hashlib`, `hmac`, `secrets`); educational mock RSA stubs eliminated; password hashing implementation moved to M22 L22-01. |
| **14** | PKI/authn/authz layers separated & scoped forward secrecy | **PASS** | Section 3.1 and 27.1 define 6-layer PKI model; RFC 9846 forward secrecy properly scoped to DHE/ECDHE key exchange; PSK-only lack of forward secrecy stated. |
| **15** | M22 authn/authz/session/token/OAuth/OIDC boundaries | **PASS** | Section 11 separates credentials from identities and sessions from bearer tokens; defines `TeachingProfile-BearerV1`; preserves RFC 9700 BCP strength (ROPC MUST NOT, Implicit SHOULD NOT); frames invalidation out-of-band. |
| **16** | Password currentness/normative strength source-bounded | **PASS** | Sections 3.1, 11, 24, 28 ground password rules in NIST SP 800-63B-4 §3.1.1.2 (passwords SHALL be salted and hashed; salt SHALL be >= 32 bits chosen to minimize collisions; cost factor SHOULD be as high as practical and increased over time; approved scheme in latest SP 800-132 [PBKDF2 compute-hard; revision planned] or updated guidance SHOULD be used; verifier SHOULD permit max length >= 64 chars without truncation; single-factor >= 15 chars, MFA >= 8 chars; composition rules abolished); classifies Argon2id (RFC 9106) and scrypt (RFC 7914) as RFC/industry current-practice candidates rather than NIST SP 800-63B-4 normative SHOULD; removes unguessable secret claim for salts; eliminates frozen 600,000 constant; prohibits fake equivalent fallback. |
| **17** | Web-security composition boundaries | **PASS** | Section 12 establishes parameterized API/driver contract separating data from syntax; scenario-specific CSRF credential models; bounded SSRF socket egress controls. |
| **18** | Supply-chain provenance boundaries | **PASS** | Sections 13, 27.2 establish 9-layer supply-chain separation; clarifies hash checks verify against expected digest but do not defeat compromised lockfile; SLSA v1.2 date corrected to 24 November 2025. |
| **19** | Safe-target Candidate B explicitly accept/refine/reject | **PASS** | Section 5 explicitly **ACCEPTS AND REFINES Candidate B** with loopback, non-sensitive data, and fix-and-verify stance. |
| **20** | Canonical Lab architecture truth preserved | **PASS** | Section 5.2 audits against canonical `meta/blueprint/lab-source-selection-map-v0.1.md` preserving exact 5 Required Labs (`LAB-REQ-01` M11, `LAB-REQ-02` M06, `LAB-REQ-03` M15, `LAB-REQ-04` M13, `LAB-REQ-05` M14), 5 Optional Labs, and 5 Source Expeditions. |
| **21** | No public/real target/offensive dependency | **PASS** | Strictly localhost `127.0.0.1` ephemeral testing; zero offensive scanners or remote targets. |
| **22** | Fixture candidate has preflight/reset/cleanup/evidence/safety | **PASS** | Sections 9, 14, 19, 24, 31 establish fail-closed teardown, owned-thread lifecycle, bounded join, post-cleanup listener verification, and configurable watchdogs. |
| **23** | M23 question-driven measurement / no universal constants | **PASS** | Executive §1, Section 16, Section 25.3, Section 27.3 consistently enforce question-driven methodology; open vs closed workloads both valid per question; warm-up applied conditionally only when mechanism requires it; coordinated omission evaluated when arrival process is independent; monotonic clocks utilized without freezing a single Python API as universal; summary metrics matched to inference goal. |
| **24** | D-015 exact 12 dimensions | **PASS** | Section 17 details all 12 dimensions of Decision D-015 for technology evaluation. |
| **25** | AI handling does not resolve OQ-BP-001 | **PASS** | Section 15.2 and 17 treat AI outputs as unverified candidate hypotheses; OQ-BP-001 remains OPEN. |
| **26** | M23 estimate/cost units/assumptions/inference limits | **PASS** | Section 18 details Fermi estimation, units (b vs B), explicit assumptions, and bottleneck sensitivity. |
| **27** | M24 integration only / no new mechanism | **PASS** | Section 20 confirms M24 is purely an integrative evaluation capstone introducing zero new mechanisms. |
| **28** | M24 evidence→claim on actual system / changed constraints | **PASS** | Sections 21, 22, 23, 27.4 ground defense on learner's actual system (no fabricated Raft/consensus); scenario cards conditional on architecture; parameterized API contracts replace AST mandates; rollback / roll-forward / migration reversal / canary treated as conditional strategies; stated data-loss bounds. |
| **29** | Design owns final assessment contract but no universal scoring formula | **PASS** | Section 23 establishes the binary criteria-gated assessment rubric; rejects point formulas. |
| **30** | STABLE/CURRENT/FRONTIER classification | **PASS** | Section 28 classifies every source into STABLE, CURRENT, or FRONTIER. |
| **31** | Exact current source revisions/dates/statuses recorded | **PASS** | Section 28.1 records exact dates and statuses: NIST SP 800-63B-4 July 2025 Final; NIST SP 800-132 Dec 2010 Final (revision planned); FIPS 198-1 July 2008 Final (supersedes March 2002 FIPS 198; NIST withdrawal proposal 23 June 2025); NIST SP 800-224 Initial Public Draft 28 June 2024; RFC 9846 July 2026; RFC 9525 Nov 2023; RFC 9700 Jan 2025; draft-ietf-oauth-v2-1-15 March 2026; draft-ietf-httpbis-layered-cookies-02 21 May 2026; W3C CSP3 Working Draft 29 July 2026; RFC 9106 Sept 2021; SLSA v1.2 24 Nov 2025. |
| **32** | Rights/license/provenance recorded | **PASS** | Section 28.1 records rights under IETF TLP Section 4/5 (Code Components under BSD 3-Clause), US Gov works not subject to US copyright protection with foreign rights preserved per D-016 (unqualified worldwide public domain eliminated), W3C Document License, Community Specification License 1.0 (SLSA), and PyCA dual Apache-2.0/BSD-3-Clause. |
| **33** | OQ-BP-001/003/006 remain OPEN in substance | **PASS** | Section 24 and 32.2 specify runtime capabilities, configurable policy inputs, and candidate packages with capability detection, removing frozen constants or versions. |
| **34** | Issue #34 remains OPEN / DEFERRED / NON-BLOCKING | **PASS** | Section 32.2 preserves Issue #34 as non-blocking per Decision D-027. |
| **35** | Consensus Registry ID remains deferred | **PASS** | Section 29.2 confirms Consensus Registry ID remains deferred per Decision D-025. |
| **36** | No unrelated S1–S6 churn | **PASS** | Working tree contains zero modifications to Stages 1–6 files. |
| **37** | Implementation-batch recommendation present | **PASS** | Section 4 specifies 4 bounded implementation batches (S7-B1 through S7-B4). |
| **38** | Evidence templates neutral / no fabricated volatile outcomes | **PASS** | Section 25.1 defines 6-layer taxonomy with rigorous cryptographic hash properties (preimage and collision resistance, not irreversible compression function); Section 25.2 strictly prohibits prefilled volatile numbers, ports, timestamps, or fake PASS; Section 25.3 templates frame non-repudiation as contextual assurance and timing mitigation per library API contracts. |
| **39** | Visuals specified / no copied third-party diagrams | **PASS** | Section 27 specifies 15 original visual layouts with accurate boundaries. |
| **40** | `git diff --check` passes cleanly | **PASS** | Verified zero whitespace errors, trailing spaces, or carriage return mismatches. |

---

## 34. Final Recommendation & Readiness Sign-Off

### Final Recommendation: **READY FOR LESSON / ACTIVITY IMPLEMENTATION**

The Stage 7 Design Dossier v0.1 establishes a complete, rigorous, and defensible architectural blueprint for Modules M21–M24. All technical constraints, normative standards, concept registries, safe-target boundaries, and evaluation rubrics are fully specified and reconciled with curriculum invariants.

**Explicit Scope Limitation:**
This design sign-off authorizes the creation of bounded implementation tasks for Batches S7-B1 through S7-B4. It does **NOT** imply that learner lessons have been drafted, that activities are implemented, that learner validation is complete, or that Stage 7 is VERIFIED or RELEASED.

READY FOR LESSON / ACTIVITY IMPLEMENTATION
