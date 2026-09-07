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
   Systems measurement is designed as a hypothesis-driven empirical discipline. It rejects all arbitrary universal constants (such as mandatory sample sizes of 30 or universal percentile mandates like p99). Workloads must be defined as either open or closed models; measurement runs require mechanism-grounded warm-up phases, explicit defense against coordinated omission, and strict utilization of monotonic clocks (`time.monotonic_ns()`).
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
| **M21** | `L21-02` | What do I use crypto for? | `L21-01` | Cryptographic primitives (Hash, MAC, Digital Signature, AEAD), key lifecycle, salt/nonce invariants, password hashing (NIST SP 800-63B-4), PKI 6-layer model. Strictly crypto use, no primitive implementation. |
| **M22** | `L22-01` | How do I know who is calling? | `L21-02`, `L11-02` (HTTP Protocol) | Authn vs Authz, credentials vs identities, sessions vs bearer tokens, RBAC vs ABAC vs capability models, token validation invariants, OAuth 2.1 & OIDC architecture (RFC 9700). |
| **M22** | `L22-02` | Why is my web app vulnerable? | `L22-01`, `L12-03` (Browser Execution) | Code vs data injection (SQL, OS), context-aware escaping, XSS taxonomy & CSP Level 3, CSRF mechanics & defense (SameSite, tokens, Origin), SSRF anatomy & egress socket binding. |
| **M22** | `L22-03` | Why do I trust my dependencies? | `L22-02` | Software supply chain risks, dependency trees, typosquatting & malicious updates, 6-layer supply-chain separation (pinning, digests, reproducibility, signatures, identity, SLSA v1.2 provenance). |
| **M23** | `L23-01` | How do I measure honestly? | `L20-01` (Observability), `L04-02` (Empirical Measurement) | Question-driven measurement, workload models (open vs closed), coordinated omission, warm-up criteria, distribution reporting (percentiles, median/IQR), monotonic clocks. |
| **M23** | `L23-02` | How do I pick a technology? | `L23-01` | Decision D-015 12 dimensions, evaluating vendor claims, technology rejection as passing outcome, bounded stable trade-offs (caching/Redis case), AI outputs as untrusted hypotheses. |
| **M23** | `L23-03` | What is the cost of my design? | `L23-02` | Systems cost modeling, compute/storage/memory/egress scaling, Fermi back-of-the-envelope estimation, latency vs dollar trade-offs, bottleneck identification & sensitivity analysis. |
| **M24** | `L24-01` | Can I defend an architecture? | `L23-02` | Capstone architecture defense, 16 core architectural traces, 12 evidence areas, structured defense template, handling changed-constraint challenges, trade-off justification. |
| **M24** | `L24-02` | What should I measure before I ship? | `L24-01` | Pre-ship evidence planning, risk-prioritized verification matrix, defining what must be measured vs tested vs inspected vs explicit unknown, failure & rollback readiness. |

---

## 3. Research Findings Adopted, Rejected & Bounded

### 3.1 Adopted Research Findings

The architectural design incorporates all validated findings from `research/security-synthesis-judgment-m21-m24-v0.1.md`:

1. **NIST SP 800-63B-4 Password Storage Standard (Adopted):**
   Adopted the July 2025 Final recommendations:
   - Passwords SHALL be salted with a salt of at least 32 bits (4 bytes) and hashed using an approved one-way function.
   - Passwords SHOULD be hashed using a memory-hard function (Argon2id per RFC 9106, scrypt per RFC 7914, or PBKDF2 per RFC 8018 / SP 800-132).
   - Minimum length requirements: Single-factor passwords SHALL be at least 15 characters; MFA-backed passwords MAY be shorter but SHALL be at least 8 characters. Truncation is forbidden; maximum length SHALL be at least 64 characters.
   - Traditional composition rules (mandatory uppercase, lowercase, numbers, symbols) and periodic forced password rotation are discarded as counter-productive.

2. **RFC 9846 TLS 1.3 Standards Track (Adopted):**
   Adopted RFC 9846 (published July 2026, Standards Track Proposed Standard), which obsoletes RFC 8446, 5246, 5077, 6961, 7627, and 8422. It codifies TLS 1.3 as the definitive modern secure channel, incorporating mandatory forward secrecy, removal of broken static RSA key exchange and obsolete ciphers, encrypted handshakes, and strict certificate validation.

3. **RFC 9525 Service Identity Verification (Adopted):**
   Adopted RFC 9525 (published May 2024), establishing that TLS service identity validation MUST check Subject Alternative Names (`SAN: dNSName` or `SAN: iPAddress`) and MUST NOT fall back to Common Name (`CN`) in the Subject field.

4. **RFC 9700 / BCP 240 & OAuth 2.1 Specification Baseline (Adopted):**
   Adopted RFC 9700 (Best Current Practice 240, published January 2025) and `draft-ietf-oauth-v2-1-15` (March 2026 active Working Group draft):
   - PKCE (Proof Key for Code Exchange, RFC 7636) is a MUST for public clients and RECOMMENDED for confidential clients.
   - Resource Owner Password Credentials Grant (ROPC) is deprecated and MUST NOT be used.
   - Implicit Grant is deprecated and MUST NOT be used.
   - Redirect URI exact string matching is mandatory.

5. **W3C Content Security Policy Level 3 Baseline (Adopted):**
   Adopted W3C CSP3 (Working Draft 13 August 2026):
   - Modern CSP deployment centers on nonce-based policies (`'nonce-{random}'`) and strict-dynamic (`'strict-dynamic'`) for script execution, rather than brittle domain allowlists.

6. **SLSA v1.2 Supply Chain Security Baseline (Adopted):**
   Adopted OpenSSF SLSA v1.2 specification (Approved, September 2024; v1.0 retired), establishing verifiable build provenance, tamper-evident signing, and the separation of source, build, and distribution integrity.

7. **Six-Layer Separation Models (Adopted):**
   - **PKI Architecture:** Explicitly separated into 6 distinct conceptual layers:
     1. *Certificate Credential* (data structure holding public key and subject metadata);
     2. *Path Validation* (cryptographic verification of certificate chain against trust roots per RFC 5280);
     3. *Service Identity Binding* (verification that the certificate matches the intended DNS domain/IP per RFC 9525);
     4. *Proof of Private-Key Possession* (cryptographic challenge-response in TLS handshake proving possession of the private key);
     5. *Authentication* (determining the confirmed identity of the endpoint);
     6. *Authorization* (determining whether the confirmed identity has permission to perform the requested operation).
   - **Software Supply Chain:** Explicitly separated into 6 distinct integrity layers:
     1. *Version Pinning* (specifying semantic versions);
     2. *Cryptographic Hash Pinning* (pinning exact artifact byte hashes);
     3. *Build Reproducibility* (verifying independent byte-for-byte build outputs);
     4. *Signature Verification* (verifying cryptographic signatures over packages);
     5. *Signer Identity Binding* (binding cryptographic keys to authorized human or service identities);
     6. *Provenance Attestation* (verifying authenticated build records under SLSA v1.2).

### 3.2 Rejected Claims & Universal Truth Traps

This design formally rejects the following oversimplifications, false equivalences, and pseudo-standards:

1. **"HTTPS makes an application secure" (Rejected):**
   HTTPS provides confidentiality and integrity for data in transit across network hops. It provides zero protection against application-layer injection (SQLi), cross-site scripting (XSS), cross-site request forgery (CSRF), broken object-level authorization (BOLA), server-side request forgery (SSRF), or compromised server-side databases.

2. **"Encryption and Hashing are interchangeable" (Rejected):**
   Encryption is a two-way transform intended to preserve confidentiality with reversible recovery via a secret key. Hashing is a one-way irreversible compression function intended to produce a fixed-size digest for integrity verification or password verification. Confusing them leads to fatal vulnerabilities (e.g., attempting to "decrypt" a hash or using unkeyed hashes where signatures or MACs are required).

3. **"Base64 is encryption" (Rejected):**
   Base64 is an open, reversible byte-to-text encoding format providing zero confidentiality, zero integrity, and zero security.

4. **"JWTs are inherently secure" (Rejected):**
   Unsigned JWTs (`alg: "none"`) provide zero integrity. Symmetric HMAC tokens signed with weak secrets are vulnerable to offline brute-force. Storing sensitive data in unencrypted JWT payloads leaks data because payloads are merely Base64URL-encoded. JWTs are bearer tokens: anyone in possession of the token has authority unless validated against audience, issuer, expiration, and revocation mechanisms.

5. **"Every system needs 30 benchmark runs and must optimize p99" (Rejected):**
   The "n = 30" heuristic is an introductory statistical rule of thumb that does not guarantee normality or statistical power for heavy-tailed, multimodal distributed systems. Percentile targets must be derived from user expectations and system constraints, not treated as dogmatic universal constants.

6. **"AI-generated code is authoritative or production-ready" (Rejected):**
   AI models generate plausibly structured text based on probabilistic patterns, not verified correctness or invariant preservation. AI-generated code, architectural recommendations, and security advice must be treated as untrusted hypotheses requiring rigorous empirical testing, static inspection, and formal verification.

---

## 4. Recommended S7 Implementation Batches

To ensure focused execution, auditable review boundaries, and minimal blast radius, Stage 7 implementation is structured into **four sequential, bounded implementation batches**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Batch S7-B1: Module M21 (Security Synthesis I: Trust & Crypto Use)     │
│ - L21-01 (Threat Modeling & Boundaries)                                │
│ - L21-02 (Crypto Primitives & Password Hashing)                        │
│ - Activity fixture: activity_l21_02.py (Localhost Crypto/Password)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Batch S7-B2: Module M22 (Security Synthesis II: Authn & Web Security)  │
│ - L22-01 (Authn vs Authz, Sessions & OAuth 2.1)                        │
│ - L22-02 (Web Vulnerabilities: Injection, XSS, CSRF, SSRF)             │
│ - L22-03 (Software Supply Chain Security)                              │
│ - Activity fixture: activity_l22_02.py (Localhost Web Security Fix)   │
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
   - S7-B1 and S7-B2 form the security synthesis block. Splitting them between cryptographic foundations (M21) and application/web/supply-chain composition (M22) keeps the security review surface manageable.
   - S7-B3 introduces the empirical measurement, technology judgment, and cost modeling frameworks. It requires zero network security fixtures and focuses on quantitative reasoning.
   - S7-B4 integrates all preceding stages (S1–S7) into the final capstone defense. It introduces no new code or mechanisms, focusing entirely on synthesis, assessment rubrics, and the reviewer contract.

2. **Reviewable PR Sizes:**
   Dividing S7 into 4 batches prevents massive, unreviewable multi-thousand-line PRs, ensuring that the Web Lead can thoroughly audit code fixtures, test suites, and pedagogical prose at each boundary.

3. **Progressive Test & Fixture Isolation:**
   Each batch delivers exactly its own unit test suite (`test_m21.py`, `test_m22.py`, `test_m23.py`, and `test_m24.py`), ensuring that CI remains green and regress-free across incremental deliveries.

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

5. **Lab Counts Invariance:**
   Lab counts remain strictly:
   - **Required Labs:** 5 (`LAB-01` M04, `LAB-02` M08, `LAB-03` M10, `LAB-04` M13, `LAB-05` M15)
   - **Optional Labs:** 5 (`LAB-OPT-01` M05, `LAB-OPT-02` M16, `LAB-OPT-03` M11, `LAB-OPT-04` M20, `LAB-OPT-05` M14)
   - **Source Expeditions:** 5 (`EXP-01` M06, `EXP-02` M09, `EXP-03` M12, `EXP-04` M20, `EXP-05` M17)
   **Exactly ZERO new Required Labs are created in Stage 7.**


## 6. Module M21 Architecture — Security Synthesis I: Trust & Crypto Use

### 6.1 Module Purpose & Capability Transition

Module M21 marks the transition from functional system construction to adversarial reasoning and cryptographic protection. Prior modules established how networks communicate (M10, M11), how processes isolate memory (M06, M07), how files persist to disk (M09), and how web browsers execute code (M12). M21 synthesizes these concepts under the assumption of an untrusted or adversarial environment.

The core capability transition of M21 is:
- **From:** Assuming endpoints, inputs, and storage are benign and well-behaved.
- **To:** Explicitly mapping trust boundaries, identifying unvalidated inputs, reasoning about attack surfaces, and correctly employing cryptographic primitives (hashes, MACs, digital signatures, AEAD) as opaque security building blocks without attempting to implement cryptographic algorithms.

### 6.2 Module Constraints & Invariants

1. **Crypto-Use Only (Zero Primitive Implementation):**
   Under no circumstances do learners implement cryptographic primitives (e.g., writing custom AES, RSA, SHA-256, or HMAC algorithms). Learners use standard, vetted cryptographic libraries (`hashlib`, `hmac`, `secrets`, and optionally PyCA `cryptography` where available) to compose secure protocols.
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
- `Trace`: Trace data and control flows across hardware, kernel, network, and application boundaries.
- `Diagnose`: Identify missing input validation, implicit trust assumptions, and privilege leaks across boundaries.
- `Judge`: Evaluate system attack surfaces and select appropriate isolation mechanisms (process, container, VM, cryptographic boundary).

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-017 Trust Boundary`: Revisit (First home: M07 `L07-01`). Extended from kernel/user-space memory boundaries to network endpoints, inter-process communication, and API request boundaries.
- `EC-CON-013 Isolation`: Revisit (First home: M07 `L07-01`). Extended from virtual address spaces to multi-tenant service isolation and least privilege.

### 5. Learning Outcomes
- Define and locate trust boundaries across a multi-tier client-server architecture.
- Construct a data-flow threat model identifying untrusted sources, validation checkpoints, and assets.
- Contrast ambient authority (privileges granted automatically by context) with explicit capability-based delegation.
- Apply the principle of least privilege to process execution, filesystem access, and network interfaces.

### 6. Stable Principle
Every byte received across a trust boundary is untrusted input until explicitly parsed, validated, and sanitized against a strict schema. Security boundaries cannot rely on client cooperation.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** Formal isolation boundaries defined by CPU privilege rings (Ring 0 vs Ring 3), OS syscall interfaces, POSIX file permissions, and network protocol specifications.
- **Implementation:** Kernel page table enforcement, namespace isolation in Linux, TLS socket termination, and input validation schemas.
- **Current Practice:** Zero-trust architecture, defense-in-depth, STRIDE threat modeling, and micro-segmentation.

### 8. Required Distinctions / Misconceptions
- *Misconception:* A firewall or TLS connection makes an entire application secure.
  *Reality:* TLS only secures the network transport hop; the application endpoint must still validate all parsed data, enforce authorization, and protect internal state.
- *Misconception:* Internal network traffic (behind the firewall) is inherently trusted.
  *Reality:* Lateral movement and insider threats exploit perimeter-only defenses; modern systems enforce zero-trust verification at internal service boundaries.

### 9. Worked Example
A web application accepts a user profile update containing `{"username": "alice", "avatar_path": "/etc/passwd"}`.
The learner traces how the request crosses:
1. The Network Boundary (TLS terminated at reverse proxy);
2. The Process Boundary (HTTP payload parsed by web worker process);
3. The Filesystem Boundary (Worker attempts to open `avatar_path` using operating system privileges).
The example illustrates that even though the TLS boundary was secure, the application failed to validate the path at the storage boundary, allowing an attacker to breach the isolation boundary via path traversal.

### 10. Bounded Hands-On / Observation
Learners inspect a mini architecture specification consisting of a web front-end, a background worker, and a local SQLite database. Using a structured questionnaire, learners trace three distinct flows (user signup, file upload, admin report generation), mark every trust boundary, list the ambient privileges present at each stage, and identify at least two unvalidated boundary crossings.

### 11. Evidence to Record
- System Boundary Inventory Table (Source component, Destination component, Boundary type, Authority mechanism).
- Dataflow Trace Log identifying the exact line/function where untrusted data is converted to trusted internal domain objects.

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** The learner correctly identifies all trust boundaries, traces dataflow through validation checkpoints, and flags missing boundary validations.
- **BLOCKED:** The learner cannot identify operating system or network privilege distinctions.
- **NOT RUN:** Hands-on review skipped or incomplete.

### 13. Progressive Support
- **Question:** How does a web server determine whether a file path provided in an HTTP query parameter is safe to open?
- **Hint 1:** Consider what happens if the query string contains relative directory navigation characters like `../`.
- **Hint 2:** Examine where the trust boundary lies: the HTTP query is outside the boundary; the local filesystem is inside.
- **Expected Observation:** The learner recognizes that resolving relative paths against an untrusted parameter allows accessing arbitrary filesystem files unless canonically resolved and strictly restricted to an allowed base directory.
- **Full Explanation:** To protect the filesystem boundary, the application must canonically resolve the target path (e.g., using `os.path.realpath` or `pathlib.Path.resolve()`), verify that the resolved path is an exact prefix child of the designated root directory, and reject any path outside that sandbox.

### 14. Required Visuals
- *Visual M21-V1:* Trust Boundary & Authority Map across Network, OS, and Application layers.

### 15. Failure Modes
- Confusing data encoding (e.g., JSON parsing) with security validation.
- Assuming an internal microservice or helper function can implicitly trust its callers.

### 16. Non-Goals
- Performing network penetration testing, port scanning, or using vulnerability assessment tools.
- Implementing low-level kernel security modules (e.g., writing SELinux/AppArmor policies).

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Automated test verifying that path validation utility rejects traversal sequences (`../`, null bytes, absolute paths outside root).
- Reviewer-Required: Manual evaluation of learner's architectural boundary inventory and threat model diagrams.

### 18. Source Grounding with Currentness Classification
- **NIST SP 800-207 (Zero Trust Architecture):** STABLE. Core principles of explicit verification, least privilege, and assumed breach.
- **RFC 9846 (TLS 1.3):** STABLE / CURRENT (July 2026). Definitive transport security standard.

---

## 8. Lesson L21-02 Design — "What do I use crypto for?"

### 1. Target Mental Model
Cryptography is a toolbox of mathematically rigorous primitives designed to enforce specific security properties: **Integrity** (Hash), **Authenticity & Integrity with Shared Secret** (MAC), **Authenticity & Non-Repudiation with Asymmetric Keys** (Digital Signature), and **Confidentiality with Authenticity** (AEAD Symmetric Encryption). Developers must never invent cryptographic algorithms or protocols; their responsibility is to select the correct standard primitive for the required security property, manage key lifecycles securely, ensure nonce/salt uniqueness, and avoid side-channel leaks.

### 2. Prerequisites
- Hard: `L21-01` (Trust Boundaries & Threat Modeling).

### 3. Primary Competencies
- `Explain`: Contrast the security properties and operational requirements of Hashes, MACs, Digital Signatures, and AEAD.
- `Trace`: Trace a cryptographic verification workflow (e.g., verifying a signed token or password hash) and identify failure modes.
- `Correctness`: Select and configure appropriate standard library cryptographic primitives without creating security vulnerabilities.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-008 Invariant`: Revisit (First home: M02 `L02-03`). Cryptographic invariants (e.g., collision resistance, pre-image resistance, nonce uniqueness in AEAD).
- `EC-CON-009 Correctness`: Revisit (First home: M02 `L02-03`). Correctness under active adversarial manipulation.

### 5. Learning Outcomes
- Distinguish between Hash, MAC, Digital Signature, and Symmetric/Asymmetric Encryption based on keys involved and security properties provided.
- Implement secure password storage complying with NIST SP 800-63B-4 using salted, memory-hard hashing functions.
- Explain why constant-time comparison (`hmac.compare_digest`) is required to prevent timing side-channel attacks.
- Deconstruct the 6-layer PKI architecture and explain how digital certificates establish trust in TLS.

### 6. Stable Principle
Never roll your own crypto. Use standard, peer-reviewed primitives from reputable cryptographic libraries; treat primitives as black boxes with strict preconditions (e.g., never reuse a nonce with the same key in AES-GCM; always salt passwords).

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** Mathematical specifications and RFCs: FIPS 180-4 (SHA-2), FIPS 198-1 (HMAC), RFC 9106 (Argon2id), RFC 8439 (ChaCha20-Poly1305), NIST SP 800-38D (AES-GCM), RFC 9846 (TLS 1.3).
- **Implementation:** Standard library implementations: Python `hashlib`, `hmac`, `secrets`, PyCA `cryptography`.
- **Current Practice:** Memory-hard password hashing (Argon2id / scrypt / PBKDF2), deprecation of SHA-1 / MD5 for integrity, requirement of AEAD (unauthenticated CBC mode deprecated).

### 8. Required Distinctions / Misconceptions
- *Misconception:* Hashing a password with SHA-256 makes it secure.
  *Reality:* SHA-256 is designed to be fast on hardware; attackers can test billions of SHA-256 hashes per second using GPUs/ASICs. Passwords require salted, computationally expensive, memory-hard hash algorithms (Argon2id, scrypt, PBKDF2) per NIST SP 800-63B-4.
- *Misconception:* Encryption provides integrity.
  *Reality:* Unauthenticated encryption (e.g., plain AES-CTR or AES-CBC) allows attackers to tamper with ciphertexts (bit-flipping attacks) without detection. Modern cryptography requires Authenticated Encryption with Associated Data (AEAD, e.g., AES-GCM, ChaCha20-Poly1305).
- *Misconception:* Base64 is encryption.
  *Reality:* Base64 is an encoding format for binary data in ASCII text; it has zero secret keys and zero security.

### 9. Worked Example
Learners compare password verification implementations:
1. Vulnerable: `stored_hash == hashlib.sha256(password.encode()).hexdigest()` (Fast hash, unsalted, vulnerable to rainbow tables and fast offline dictionary attacks, timing attack on string comparison `==`).
2. Robust: Using a standard password hashing library with random salt generation (`secrets.token_bytes(16)`), memory-hard Argon2id or PBKDF2-HMAC-SHA256 with 600,000 iterations, and constant-time digest comparison via `hmac.compare_digest`.

### 10. Bounded Hands-On / Observation
Learners interact with `labs/foundations/m21/activity_l21_02.py`:
1. Benchmark SHA-256 vs. PBKDF2 / Argon2 on localhost to observe the computational and memory cost difference.
2. Demonstrate how unsalted hashes result in identical hash values for identical passwords across different user records.
3. Fix a vulnerable authentication function by adding per-user unique random salts and constant-time comparison.

### 11. Evidence to Record
- Cryptographic Primitive Selection Matrix (Problem scenario, Required property, Correct primitive, Incorrect primitive trap).
- Execution timing measurements demonstrating why constant-time comparison prevents timing discrepancies.

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Activity test suite passes; learner refactors password storage to use unique random salts, standard slow hashing, and constant-time verification.
- **BLOCKED:** Missing standard library cryptographic modules.
- **NOT RUN:** Hands-on activity not executed.

### 13. Progressive Support
- **Question:** Why does `hmac.compare_digest(a, b)` take the same amount of time regardless of where the first mismatch occurs, whereas `a == b` returns immediately on the first differing character?
- **Hint 1:** Think about how a standard string equality loop is implemented in C or Python.
- **Hint 2:** An early-return optimization leaks information through execution duration.
- **Expected Observation:** Standard equality `==` terminates as soon as a byte differs, allowing an attacker to deduce the correct signature byte-by-byte by measuring microsecond-level timing differences.
- **Full Explanation:** Early-exit comparisons create a timing side-channel. `hmac.compare_digest` iterates over all bytes unconditionally, accumulating differences using bitwise OR operations, ensuring that the execution time is independent of byte values and early mismatches.

### 14. Required Visuals
- *Visual M21-V2:* Cryptographic Primitives Taxonomy: Hash vs. MAC vs. Digital Signature vs. AEAD.
- *Visual M21-V3:* The 6-Layer PKI Trust and Verification Architecture.

### 15. Failure Modes
- Attempting to implement custom XOR encryption or custom hashing algorithms.
- Reusing initialization vectors (IVs) or nonces in symmetric encryption.

### 16. Non-Goals
- Implementing mathematical number theory for RSA, elliptic curves, or lattice cryptography.
- Conducting live cryptanalysis or side-channel power analysis.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: `pytest labs/foundations/m21/test_m21.py` validating salt generation, slow hash execution, and constant-time comparison.
- Reviewer-Required: Inspection of learner's cryptographic primitive selection rationales.

### 18. Source Grounding with Currentness Classification
- **NIST SP 800-63B-4 §3.1.1.2:** CURRENT (Final July 2025). Normative password storage rules: minimum 15 chars single-factor, 8 chars MFA; salt >= 32 bits; memory-hard functions recommended.
- **RFC 9106 (Argon2):** STABLE. Standard memory-hard password hashing.
- **RFC 9846 (TLS 1.3):** STABLE / CURRENT (July 2026). Mandatory forward secrecy, AEAD ciphers only.
- **FIPS 186-5 / SP 800-38D:** STABLE. Digital signatures and AES-GCM authenticated encryption.

---

## 9. M21 Hands-On Fixture Contract — Localhost Password Hashing & Crypto Primitives (`activity_l21_02.py`)

### 9.1 Purpose & Execution Scope
The fixture `activity_l21_02.py` provides an isolated, localhost-only environment to experiment with cryptographic primitives, password hashing invariants, and timing-safe comparisons. It contains zero external network dependencies and uses standard Python standard library modules (`hashlib`, `hmac`, `secrets`, `time`). If PyCA `cryptography` or `argon2-cffi` is present in the environment, the fixture optionally exposes them via clean capability detection without failing if they are absent.

### 9.2 Fixture File Structure
- Implementation: `labs/foundations/m21/activity_l21_02.py`
- Verification Suite: `labs/foundations/m21/test_m21.py`

### 9.3 Invariants & Interface Contract
1. **Password Storage Schema:**
   The fixture defines a clean, extensible password storage representation:
   ```python
   # Format: algorithm$iterations_or_params$salt_hex$hash_hex
   # Example: pbkdf2_sha256$600000$a1b2c3d4...$e5f6...
   ```
2. **Deterministic Capability Detection:**
   ```python
   HAS_ARGON2 = False
   try:
       import argon2
       HAS_ARGON2 = True
   except ImportError:
       pass
   ```
   If `HAS_ARGON2` is False, the fixture gracefully falls back to standard library `hashlib.pbkdf2_hmac` (SHA-256, >= 600,000 iterations), ensuring 100% test pass rates in stock Python environments.
3. **Safety & Zero-State Guarantees:**
   - Fixture runs in-memory or in an ephemeral `tempfile.TemporaryDirectory()`.
   - All generated mock user records are wiped on teardown.
   - Zero hardcoded real passwords or cryptographic private keys.


## 10. Module M22 Architecture — Security Synthesis II: Authn/Authz & Secure Composition

### 10.1 Module Purpose & Capability Transition

Module M22 addresses the complex challenge of composition in multi-tier applications, web environments, and external dependency ecosystems. Where M21 established trust boundaries and cryptographic tools, M22 applies them to the operational realities of software systems:
- Verifying who is calling and what they are allowed to do (Authentication and Authorization);
- Preventing application-layer composition failures across disparate parsers and interpreters (Injection, XSS, CSRF, SSRF);
- Verifying the integrity and provenance of third-party dependencies composing the modern software supply chain.

The core capability transition of M22 is:
- **From:** Treating authentication as a single login check, assuming client input matches expected formats, and blindly trusting installed third-party libraries.
- **To:** Designing decoupled, defense-in-depth authorization pipelines, eliminating injection vulnerabilities at the AST/syntax boundary, implementing robust web security controls, and auditing dependency graphs with cryptographic pinning and provenance.

### 10.2 Module Constraints & Invariants

1. **Strict Defense-First Fix-and-Verify Stance (Decision D-012):**
   Zero exploit development, zero weaponized payload distribution, and zero offensive scanning. Exercises present bounded, reproducible code vulnerabilities on localhost; learners inspect the failure, apply the structural defensive fix, and verify immunity using automated tests.
2. **Safe Localhost Execution:**
   All web server and client interactions run exclusively on `127.0.0.1` using ephemeral ports.
3. **Normative Source Grounding:**
   Adhere strictly to RFC 9700 (BCP 240, OAuth 2.0 Security Best Current Practice), `draft-ietf-oauth-v2-1-15` (OAuth 2.1), W3C CSP Level 3, and OpenSSF SLSA v1.2.

---

## 11. Lesson L22-01 Design — "How do I know who is calling?"

### 1. Target Mental Model
Security requires separating **Authentication** (Authn: proving *who* an entity is) from **Authorization** (Authz: determining *what* that entity is permitted to do). A credential is an authenticating artifact; an identity is the entity associated with that credential; an authorization policy evaluates the identity, the target resource, and the requested action. In distributed and multi-tier systems, authorization must be verified at every hop, distinguishing between stateful server-side sessions, stateless cryptographically signed bearer tokens, and mutual TLS identity assertions.

### 2. Prerequisites
- Hard: `L21-02` (Cryptographic Primitives & Digital Signatures), `L11-02` (HTTP Protocol & State).

### 3. Primary Competencies
- `Explain`: Differentiate Authn from Authz, stateful sessions from stateless bearer tokens, and RBAC from ABAC.
- `Trace`: Trace an authentication and authorization request decision path through an API gateway, session/token validator, and resource server.
- `Diagnose`: Identify authentication bypasses, broken object-level authorization (BOLA/IDOR), and token validation vulnerabilities.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-017 Trust Boundary`: Revisit (First home: M07 `L07-01`). Examined at API endpoints, identity providers (IdPs), and resource servers.
- `EC-CON-007 Specification`: Revisit (First home: M02 `L02-03`). Token schemas, claims validation, and access control policies.

### 5. Learning Outcomes
- Distinguish Authentication from Authorization across real-world API request lifecycles.
- Contrast stateful server-managed sessions (cookies + database/cache lookup) with stateless cryptographically signed bearer tokens (JWTs), articulating the revocation trade-offs of each.
- Implement comprehensive token validation invariants: signature verification, expiration check (`exp`), issuer check (`iss`), audience check (`aud`), and algorithm restriction (preventing `alg: "none"`).
- Diagram the OAuth 2.1 authorization code flow with PKCE (Proof Key for Code Exchange) per RFC 9700 and explain why PKCE is required for public clients.

### 6. Stable Principle
Never confuse possessing a credential with possessing authority. Every protected endpoint must independently verify both identity and specific resource authorization on every request.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** RFC 6749 (OAuth 2.0 core), RFC 7636 (PKCE), RFC 7519 (JWT), RFC 8725 (JWT BCP), RFC 9700 (BCP 240), `draft-ietf-oauth-v2-1-15` (OAuth 2.1).
- **Implementation:** Python `jwt` / `itsdangerous`, session middleware, API gateway auth interceptors.
- **Current Practice:** OAuth 2.1 deprecation of ROPC (Resource Owner Password Credentials) and Implicit Grant; mandatory PKCE; short-lived access tokens paired with revocable refresh tokens; fine-grained ABAC / Zanzibar-style relationship-based access control.

### 8. Required Distinctions / Misconceptions
- *Misconception:* A valid JWT signature guarantees the user is authorized to perform the action.
  *Reality:* The signature only proves the token was issued by a trusted identity provider; the application must still check if that specific user ID is authorized to access the requested resource (preventing IDOR/BOLA).
- *Misconception:* JWTs are encrypted and secret.
  *Reality:* Standard JWTs (JWS) are signed, not encrypted. The header and payload are Base64URL-encoded JSON, fully readable by anyone who inspects the token. Sensitive data must never be placed in unencrypted JWT payloads.
- *Misconception:* Stateless JWTs can be revoked instantly without server-side state.
  *Reality:* True stateless tokens cannot be revoked before their expiration time without maintaining a centralized revocation list or blocklist, which reintroduces distributed state.

### 9. Worked Example
Learners trace an API request: `GET /api/documents/1042` with header `Authorization: Bearer <jwt>`.
The learner analyzes the 5-step validation pipeline:
1. Parse JWT header and payload;
2. Verify that `alg` strictly matches expected algorithm (e.g., `RS256`), rejecting `none` or unexpected symmetric algorithms (`HS256` key confusion);
3. Cryptographically verify signature against IdP public key;
4. Validate temporal claims (`nbf <= now < exp`), issuer (`iss == trusted_idp`), and audience (`aud == my_api_service`);
5. Authorize action: check whether `jwt.sub` (user ID) has read permission for document `1042` in the database, rejecting access if document `1042` belongs to a different tenant.

### 10. Bounded Hands-On / Observation
Learners inspect a mock API gateway authentication handler in Python. The handler initially accepts unsigned tokens or fails to validate the `aud` claim, allowing tokens intended for another service to grant access. Learners modify the validator to enforce all RFC 8725 JWT BCP checks and write assertions verifying that forged, expired, and mis-targeted tokens are rejected.

### 11. Evidence to Record
- Authentication vs. Authorization Pipeline Trace Table.
- JWT Validation Invariants Checklist showing test outcomes for 5 failure cases (tampered payload, wrong algorithm, expired timestamp, incorrect audience, revoked subject).

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Validator passes all automated unit tests, rejecting all invalid/forged/expired tokens and correctly authorizing valid requests.
- **BLOCKED:** Missing cryptographic dependencies for signature verification.
- **NOT RUN:** Hands-on code exercise omitted.

### 13. Progressive Support
- **Question:** If an attacker intercepts a signed JWT issued for `service-billing.example.com`, why might they be able to use it against `service-internal-admin.example.com` if audience verification is omitted?
- **Hint 1:** Both services trust the same company Identity Provider (IdP) public key.
- **Hint 2:** The signature is completely valid because the IdP signed it. What claim specifies which service the token was issued for?
- **Expected Observation:** Because the signature verifies successfully against the shared IdP key, the admin service accepts the token unless it explicitly verifies that `aud` matches its own service identifier.
- **Full Explanation:** Digital signatures prove that an IdP generated the token, but not that the token was intended for the recipient service. Omitting the `aud` (Audience) check allows token substitution attacks across microservices. The recipient must enforce `aud == expected_service_id`.

### 14. Required Visuals
- *Visual M22-V1:* Authentication vs. Authorization Request Decision Path.
- *Visual M22-V2:* OAuth 2.1 Authorization Code Flow with PKCE Architecture.

### 15. Failure Modes
- Checking user permissions based solely on user-supplied URL parameters without validating against the authenticated identity.
- Treating bearer tokens as confidential secrets inside client-side JavaScript without `HttpOnly` or secure storage safeguards.

### 16. Non-Goals
- Deploying a live identity provider such as Keycloak, Okta, or Active Directory.
- Implementing biometric or hardware FIDO2/WebAuthn authenticators.

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Unit tests asserting token rejection for signature tampering, expiration, wrong audience, and `alg: "none"`.
- Reviewer-Required: Inspection of learner's explanation of stateless token revocation trade-offs.

### 18. Source Grounding with Currentness Classification
- **RFC 9700 / BCP 240:** CURRENT (January 2025). OAuth 2.0 Security Best Current Practice: PKCE MUST for public, RECOMMENDED for confidential; ROPC MUST NOT; redirect URI exact matching.
- **draft-ietf-oauth-v2-1-15:** CURRENT (March 2026 active draft). Consolidated OAuth 2.1 specification.
- **RFC 7519 / RFC 8725:** STABLE. JSON Web Token (JWT) specification and Security Best Current Practices.

---

## 12. Lesson L22-02 Design — "Why is my web app vulnerable?"

### 1. Target Mental Model
Web applications bridge disparate execution environments (browsers, network protocols, web servers, databases, operating system shells). Vulnerabilities arise at **composition boundaries** when data from an untrusted source is concatenated directly into a structured command, markup, or query stream, causing the receiving interpreter to confuse **data** with **code**. Eliminating vulnerabilities requires structural separation: parameterized queries, context-aware output encoding, strict content execution policies, and explicit network egress validation.

### 2. Prerequisites
- Hard: `L22-01` (Authentication & Authorization), `L12-03` (Web & Same-Origin Policy).

### 3. Primary Competencies
- `Diagnose`: Identify code-versus-data mixing in SQL queries, HTML rendering, and network requests.
- `Trace`: Trace the execution path of untrusted input through sanitization, templating, and database queries.
- `Correctness`: Refactor vulnerable code into secure implementations using parameterized APIs, context-aware encoding, and egress socket binding.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-017 Trust Boundary`: Revisit (First home: M07 `L07-01`). The boundary between application business logic and underlying interpreters (SQL engine, HTML parser, OS shell, network stack).
- `EC-CON-009 Correctness`: Revisit (First home: M02 `L02-03`). Correctness under active adversarial payload injection.

### 5. Learning Outcomes
- Explain how SQL Injection occurs via string concatenation and prove why parameterized queries (prepared statements) structurally eliminate SQLi at the Abstract Syntax Tree (AST) layer.
- Classify Cross-Site Scripting (XSS) into Stored, Reflected, and DOM-based types, and specify defenses using context-aware encoding and W3C CSP Level 3 nonce policies.
- Contrast Cross-Site Request Forgery (CSRF) ambient cookie authority with explicit bearer token authority, and implement multi-layered defenses: `SameSite` cookies, Origin/Referer verification, and anti-CSRF synchronizer tokens.
- Deconstruct Server-Side Request Forgery (SSRF) and design a secure HTTP client enforcing URL parsing, IP destination allowlists, DNS rebinding mitigation, and connection socket address binding before sending request bytes.

### 6. Stable Principle
Never concatenate untrusted input into an interpreter stream. Maintain strict structural separation between code instructions and user data at every architectural layer.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** SQL ISO/IEC 9075, W3C Content Security Policy Level 3 (Working Draft 13 August 2026), WHATWG HTML / Fetch Living Standards, RFC 6265bis / layered-cookies draft.
- **Implementation:** Python `sqlite3` parameterized queries (`?`), Jinja2 autoescaping, HTTP response headers (`Content-Security-Policy`, `Set-Cookie: SameSite=Lax; Secure; HttpOnly`).
- **Current Practice:** Nonce-based CSP (`'strict-dynamic'`), automated static analysis (SAST), ORM parameterized abstractions, defense against DNS rebinding via post-resolution socket connection inspection.

### 8. Required Distinctions / Misconceptions
- *Misconception:* Escaping single quotes with regex makes SQL queries safe against injection.
  *Reality:* Ad-hoc blacklists and string replacing fail against alternative encodings, numeric injections, and second-order injections. Only parameterized prepared statements guarantee structural AST separation.
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
- **W3C Content Security Policy Level 3:** CURRENT (Working Draft 13 August 2026). Modern nonce-based script execution.
- **RFC 6265bis / layered-cookies draft:** CURRENT (draft-ietf-httpbis-layered-cookies-02, May 2026). SameSite cookie semantics and ambient authority limits.
- **OWASP Top 10 (2021/2025):** STABLE / CURRENT. Injection, Broken Access Control, SSRF taxonomy.

---

## 13. Lesson L22-03 Design — "Why do I trust my dependencies?"

### 1. Target Mental Model
Modern software applications are composed predominantly of third-party libraries and transitive dependencies. Installing a dependency grants that code the exact same execution privileges, filesystem access, network authority, and memory access as the host application. Securing the **software supply chain** requires moving from blind trust to explicit, cryptographic verification: pinning exact versions and artifact hashes, verifying signatures and provenance attestations (SLSA v1.2), minimizing dependency count, and isolating build/execution environments.

### 2. Prerequisites
- Hard: `L22-02` (Web Application Security & Composition).

### 3. Primary Competencies
- `Explain`: Articulate the risks of transitive dependencies, typosquatting, dependency confusion, and compromised maintainer accounts.
- `Trace`: Trace a dependency resolution tree and identify lockfile pinning mechanisms.
- `Judge`: Evaluate a third-party library's maintenance posture, license obligations, and security attack surface before adoption.

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
- **Full Explanation:** This is the core insight behind SLSA (Supply-chain Levels for Software Artifacts). To establish trust from source to deployment, a system requires verifiable build provenance attestations generated by an isolated, authenticated build platform (SLSA v1.2), binding the specific git commit hash directly to the resulting binary artifact hash.

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
- **OpenSSF SLSA v1.2 Specification:** CURRENT (Approved, September 2024; v1.0 retired). Verifiable build provenance and supply chain maturity.
- **PEP 508 / PEP 440:** STABLE. Python packaging specifications.
- **NIST SP 800-218 (SSDF):** STABLE. Secure Software Development Framework.

---

## 14. M22 Hands-On Fixture Contract — Safe Localhost Web Security & Fix-and-Verify Harness (`activity_l22_02.py`)

### 14.1 Purpose & Execution Scope
The fixture `activity_l22_02.py` implements a self-contained, course-owned localhost web security test harness. It demonstrates code vs. data injection, CSRF validation, and SSRF socket egress controls entirely on `127.0.0.1` using Python's built-in `http.server` and `sqlite3`.

### 14.2 Fixture File Structure
- Implementation: `labs/foundations/m22/activity_l22_02.py`
- Verification Suite: `labs/foundations/m22/test_m22.py`

### 14.3 Safety Guarantees & Network Isolation
1. **Loopback Only:**
   The server binds exclusively to `("127.0.0.1", 0)`, allowing the OS to allocate an ephemeral free port. It NEVER binds to `0.0.0.0` or public network interfaces.
2. **Ephemeral In-Memory Database:**
   All SQL demonstrations use an in-memory SQLite database (`:memory:`) populated with synthetic records (`alice`, `bob`, `charlie`).
3. **SSRF Safe Testing Sandbox:**
   The SSRF exercise tests against a mock internal target running on loopback, demonstrating how IP blocklist checks intercept and abort requests to `127.0.0.1`, `10.0.0.0/8`, `169.254.169.254`, and `192.168.0.0/16`.
4. **Deterministic Teardown & Watchdog:**
   The server runs in a daemon thread and is terminated cleanly via `server.shutdown()` and `server.server_close()` in test teardown blocks. A 5.0-second watchdog timer prevents hanging tests.


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
Benchmarking is a scientific experiment, not a marketing exercise. A benchmark that reports only average throughput or mean latency is actively misleading because real-world systems exhibit heavy-tailed, multimodal latency distributions caused by garbage collection, queueing delays, cache misses, and network jitter. Honest measurement requires: starting with a clear question; defining a realistic workload model (open vs. closed); warming up the system to reach steady-state; capturing full distributions using high-resolution monotonic clocks (`time.monotonic_ns()`); and eliminating **coordinated omission** (where client blocking hides server queuing delays).

### 2. Prerequisites
- Hard: `L20-01` (Observability & Metrics), `L04-02` (Empirical Measurement & Profiling).

### 3. Primary Competencies
- `Observe`: Collect high-resolution, unskewed latency distributions using monotonic timers.
- `Diagnose`: Identify measurement artifacts, coordinated omission, warm-up bias, and misleading statistical summaries.
- `Judge`: Select appropriate statistical representations (percentiles, histograms, median/IQR) matching the workload's empirical distribution.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-009 Correctness`: Revisit (First home: M02 `L02-03`). Correctness of empirical data collection and statistical inference.
- `EC-CON-010 Failure`: Revisit (First home: M03 `L03-03`). Latency spikes and tail-latency failures under load.

### 5. Learning Outcomes
- Formulate a falsifiable measurement hypothesis and define the exact independent and dependent variables.
- Contrast open workload models (requests arrive independently of system completion) with closed workload models (requests wait for prior responses), and explain why closed models mask saturation.
- Identify and eliminate coordinated omission in load generation harnesses.
- Implement steady-state detection, discarding warm-up transients (JIT compilation, cache warming, connection pooling).
- Analyze latency data using percentiles (p50, p90, p99, p99.9) and histograms, demonstrating why mean and standard deviation fail for skewed systems.

### 6. Stable Principle
If you do not measure the time requests spend waiting in the client queue, you are not measuring system latency; you are measuring your benchmark's throttling.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** IEEE 754 floating point arithmetic, POSIX `CLOCK_MONOTONIC`.
- **Implementation:** Python `time.monotonic_ns()`, HdrHistogram, latency tracking data structures.
- **Current Practice:** Continuous benchmarking in CI, distributed tracing span latencies, latency SLOs (p99/p99.9), Gil Tene's coordinated omission corrections in modern load generators (wrk2, k6, Locust).

### 8. Required Distinctions / Misconceptions
- *Misconception:* The mean (average) latency accurately represents what typical users experience.
  *Reality:* Latency distributions are heavily skewed. If 99 requests take 1ms and 1 request takes 1000ms, the mean is 10.99ms—a number that describes neither the fast requests nor the slow request. Percentiles (p50, p99) accurately depict the user experience.
- *Misconception:* Running a test 30 times guarantees statistical validity (Central Limit Theorem).
  *Reality:* The Central Limit Theorem applies to the distribution of sample means, not individual latencies. Heavy-tailed distributions require non-parametric methods, high sample counts, and percentile analysis.
- *Misconception:* `time.time()` is suitable for benchmarking.
  *Reality:* `time.time()` measures wall-clock time and is subject to NTP adjustments, daylight saving steps, and system clock drift. Benchmarking must exclusively use monotonic clocks (`time.monotonic_ns()`).

### 9. Worked Example
Learners analyze a benchmark comparing two queue implementations.
The load generator sends 100 requests in a synchronous loop:
```python
for item in items:
    t0 = time.monotonic_ns()
    process(item)  # When item blocks for 500ms, next request is delayed
    record(time.monotonic_ns() - t0)
```
The learner observes that when `process()` stalls for 500ms, the loop waits. The 50 requests that *should* have arrived during that 500ms window are never generated. Consequently, the benchmark reports a low average latency, completely missing the severe queuing delay that real users would experience (Coordinated Omission).
Learners refactor the harness to use schedule-based arrival times, recording both service time and queuing time.

### 10. Bounded Hands-On / Observation
Learners run `labs/foundations/m23/activity_l23_01.py`:
1. Run a load test against a server that simulates a periodic 200ms garbage collection pause.
2. Compare the output of an uncoordinated synchronous generator versus an arrival-schedule generator; observe how the uncoordinated generator reports a misleadingly optimistic p99.
3. Plot/inspect the full histogram showing the bimodal distribution.

### 11. Evidence to Record
- Measurement Protocol Card (Hypothesis, Workload model, Warm-up criteria, Duration, Clock source).
- Comparative Latency Summary Table (Arrival-scheduled vs Synchronous: min, p50, p90, p99, max).

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Learner correctly identifies coordinated omission in a benchmark script and refactors it to record true scheduled arrival latency.
- **BLOCKED:** Insufficient timer resolution on host environment.
- **NOT RUN:** Hands-on exercise not executed.

### 13. Progressive Support
- **Question:** If an e-commerce page makes 50 distinct microservice requests to render a single user page, why is the page's 99th percentile latency much worse than the 99th percentile latency of an individual microservice?
- **Hint 1:** What is the probability that all 50 requests complete within their respective 99th percentile?
- **Hint 2:** Calculate $(0.99)^{50}$.
- **Expected Observation:** $(0.99)^{50} pprox 0.605$. Only 60.5% of page loads will experience all calls under p99.
- **Full Explanation:** This is the fan-out tail-at-scale effect. When a top-level operation depends on the completion of multiple concurrent operations, the slowest dependency dictates the overall latency. A user making 50 requests has nearly a 40% chance of hitting at least one request in the 99th percentile.

### 14. Required Visuals
- *Visual M23-V1:* Measurement Architecture: Hypothesis → Workload Generator → Monotonic Timers → Histogram vs Percentiles.
- *Visual M23-V2:* Coordinated Omission: How Synchronous Clients Hide Queuing Delays.

### 15. Failure Modes
- Reporting benchmark results from the first 5 seconds of execution before caches or thread pools warm up.
- Comparing benchmarks run on different hardware or background system load.

### 16. Non-Goals
- Complex statistical proofs of heavy-tailed Pareto distributions.
- Kernel-level CPU performance counter tuning (perf/eBPF hardware counters).

### 17. Machine-Checkable vs. Reviewer-Required Gates
- Machine-Checkable: Unit test verifying that arrival-scheduled timer accounts for queued wait time.
- Reviewer-Required: Inspection of learner's measurement protocol and experimental design.

### 18. Source Grounding with Currentness Classification
- **Gil Tene (Coordinated Omission):** STABLE. Foundational methodology for latency measurement in distributed systems.
- **Brendan Gregg (Systems Performance, 2nd Ed.):** STABLE. Methodologies for USE (Utilization, Saturation, Errors) and benchmark evaluation.

---

## 17. Lesson L23-02 Design — "How do I pick a technology?"

### 1. Target Mental Model
Engineering is the art of trade-offs under constraints. There are no universally superior technologies; every technology choice is a package deal that couples benefits with operational overhead, failure modes, consistency trade-offs, and maintenance burdens. Picking a technology requires an objective, multi-dimensional evaluation against explicit requirements rather than industry hype or marketing claims. Critically, **rejecting a technology** and keeping an architecture simpler is often the most mature engineering decision.

### 2. Prerequisites
- Hard: `L23-01` (Honest Measurement).
- Soft: `L22-01` (Authn/Authz), `L17-01` (Replication & Consistency).

### 3. Primary Competencies
- `Judge`: Evaluate competing technologies across the 12 dimensions of Decision D-015.
- `Learn-New-Tech`: Rapidly dissect an unfamiliar technology by analyzing its data model, consistency semantics, failure modes, and operational costs.
- `Explain`: Articulate the explicit trade-offs and rejection criteria for a candidate technology.

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
- `Estimate`: Perform Fermi back-of-the-envelope calculations for storage, memory, bandwidth, and compute requirements.
- `Judge`: Evaluate trade-offs between hardware costs, software complexity, and engineering maintenance time.
- `Diagnose`: Identify system scaling bottlenecks and perform sensitivity analysis on changing workload assumptions.

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
Module M23 provides two focused, non-network-dependent hands-on tools:
1. `activity_l23_01.py`: An empirical measurement and latency distribution workbench. Demonstrates coordinated omission, steady-state detection, and percentiles vs. histograms.
2. `activity_l23_02.py`: A structured Decision D-015 evaluation harness and ADR generator. Validates that proposed architectures are evaluated across all 12 dimensions and checks for explicit trade-off justifications.

### 19.2 Fixture File Structure
- Measurement Harness: `labs/foundations/m23/activity_l23_01.py`
- Evaluation Harness: `labs/foundations/m23/activity_l23_02.py`
- Verification Suite: `labs/foundations/m23/test_m23.py`

### 19.3 Invariants & Interface Contract
- **High-Resolution Timing:** All benchmarks exclusively use `time.monotonic_ns()`.
- **Zero Flakiness:** Benchmarks use controlled synthetic work loops (simulated processing delays) rather than relying on noisy operating system scheduling.
- **Machine-Checkable ADR Schema:** `activity_l23_02.py` exports a JSON schema validator ensuring that learner-submitted ADRs contain non-empty entries for all 12 dimensions of Decision D-015.


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
- `Explain`: Articulate the end-to-end architecture across all layers of the computing stack.
- `Trace`: Trace request, data, state, and authority paths through the integrated system.
- `Judge`: Defend architectural trade-offs, justify rejected alternatives, and adapt to changed constraints.

### 4. Canonical Concept First-Home vs. Revisit
- Revisit of all 18 Canonical Concepts, with primary focus on:
  - `EC-CON-007 Specification` (First home: M02 `L02-03`)
  - `EC-CON-008 Invariant` (First home: M02 `L02-03`)
  - `EC-CON-009 Correctness` (First home: M02 `L02-03`)
  - `EC-CON-010 Failure` (First home: M03 `L03-03`)
  - `EC-CON-013 Isolation` (First home: M07 `L07-01`)
  - `EC-CON-014 Consistency` (First home: M14 `L14-02`)
  - `EC-CON-015 Concurrency` (First home: M15 `L15-01`)
  - `EC-CON-016 Durability` (First home: M09 `L09-01`)
  - `EC-CON-017 Trust Boundary` (First home: M07 `L07-01`)

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

### 9. Worked Example
A learner presents their Mini Cloud App architecture, claiming it provides "high availability and durable storage."
The reviewer challenges this claim with a Changed-Constraint:
*Challenge:* "Your primary database server experiences an ungraceful power loss while writing an append-only log entry. A client receives an HTTP 500 error, retries the request, and connects to your failover replica. What does the client see, and is data corrupted?"
*Learner Defense:*
1. *State Trace:* Traces write-ahead log (WAL) sync semantics (`fsync` vs OS write cache per M09);
2. *Protocol Trace:* Traces idempotency keys used in client retries (M16);
3. *Consistency Proof:* Cites raft/replication log state (M17), demonstrating that the uncommitted entry was either truncated cleanly or replayed deterministically;
4. *Conclusion:* The client receives the correctly committed response on retry with zero state duplication.

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
- `Diagnose`: Identify pre-ship operational blind spots, unmonitored failure modes, and untested rollback paths.
- `Judge`: Prioritize verification effort based on risk severity and blast radius.
- `Correctness`: Establish automated pre-flight release gates and rollback criteria.

### 4. Canonical Concept First-Home vs. Revisit
- `EC-CON-010 Failure`: Revisit (First home: M03 `L03-03`). Failure mitigation, graceful degradation, and disaster recovery.
- `EC-CON-009 Correctness`: Revisit (First home: M02 `L02-03`). Verification gates before production deployment.

### 5. Learning Outcomes
- Construct a Risk-Prioritized Evidence Matrix classifying release checks into: Must Measure, Must Test, Must Inspect, and Acceptable Unknown.
- Verify production operational readiness: telemetry signals (M20), transport security and input sanitization (M21/M22), and resource cost boundaries (M23).
- Design and dry-run a zero-data-loss rollback and database migration reversal procedure.
- Formulate precise Service Level Objectives (SLOs) and Error Budgets governing deployment safety.

### 6. Stable Principle
If you do not have a tested rollback plan and observable health signals, you are not shipping software; you are gambling with your users' data.

### 7. Specification vs. Implementation vs. Current-Practice Boundaries
- **Specification:** Service Level Agreements (SLAs), Service Level Objectives (SLOs), release criteria checklists.
- **Implementation:** CI/CD pipeline automation, health check endpoints (`/healthz`), canary deployment scripts, database migration rollbacks.
- **Current Practice:** Progressive delivery, canary analysis, automated rollback on metric anomaly, Chaos Engineering.

### 8. Required Distinctions / Misconceptions
- *Misconception:* 100% test coverage means software is safe to ship.
  *Reality:* Unit tests verify code paths against developer assumptions. They do not verify network latencies, memory leaks under load, database migration deadlocks, or third-party dependency outages.
- *Misconception:* Rollback simply means redeploying the previous git commit.
  *Reality:* If the new version performed destructive database schema migrations or wrote data in an incompatible format, rolling back code will crash the previous version or corrupt data. Backward-compatible schema evolution is required.

### 9. Worked Example
Learners review a proposed release of a new billing microservice.
The pre-ship verification plan classifies checks:
1. *Must Measure:* Latency distribution under simulated peak load (must satisfy p99 < 50ms); memory stability over a 2-hour soak test (zero memory leaks).
2. *Must Test:* Automated regression suite (100% pass on financial calculation invariants); idempotent transaction retry on network drop.
3. *Must Inspect:* Security review of database connection credentials (must not be committed to Git; must use least-privilege DB user); code review of error handlers (must not leak stack traces to clients).
4. *Acceptable Unknown:* Behavior under a simultaneous total loss of two data centers (accepted business risk for current scale).
5. *Rollback Verification:* Verify that database column additions are nullable so that previous code runs without error if rollback occurs.

### 10. Bounded Hands-On / Observation
Learners execute a pre-ship verification simulation against their Mini Cloud App:
1. Run automated lint, unit, and integration suites.
2. Trigger an automated chaos injection (e.g., simulated slow database queries) and verify that the system emits the expected structured warning logs and degrades gracefully without crashing.
3. Perform a simulated database schema migration forward and execute a verified rollback without losing synthetic user data.

### 11. Evidence to Record
- Pre-Ship Risk-Prioritized Evidence Checklist.
- Rollback Verification Log proving that rolling back to the previous revision leaves data intact and services operational.

### 12. PASS / BLOCKED / NOT RUN Conditions
- **PASS:** Pre-ship checklist completed; rollback verification passes; all critical invariants verified under automated regression tests.
- **BLOCKED:** Failing integration test suite.
- **NOT RUN:** Pre-ship verification omitted.

### 13. Progressive Support
- **Question:** How do you safely alter a database schema (e.g., renaming a column from `full_name` to `display_name`) in production without causing downtime during deployment?
- **Hint 1:** What happens if the database schema changes while the old version of the application is still running?
- **Hint 2:** Think about a phased multi-step migration (Expand and Contract).
- **Expected Observation:** Immediate renames break running application instances that expect the old column name.
- **Full Explanation:** Safe schema evolution requires the Expand-and-Contract (Parallel Run) pattern:
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
- Machine-Checkable: Automated test suite passing 100%; static linting clean; schema migration rollback test exits 0.
- Reviewer-Required: Peer/Lead review of the pre-ship risk prioritization and rollback readiness.

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
In accordance with repository governance, **Open Question `OQ-BP-006` (Canonical Tooling and Library Versions) remains OPEN**. Specific package versions are pinned at implementation time within activity lockfiles. Stage 7 design mandates that all core educational and verification workflows must function completely within a standard Python 3.10+ runtime, treating optional third-party packages strictly via dynamic capability detection and non-breaking fallbacks.

### 24.2 Environment Capabilities Matrix

| Capability Category | Component / Module | Required Core Baseline | Optional Enhancement | Fallback / Degradation Behavior |
|---|---|---|---|---|
| **Runtime Environment** | Python Interpreter | Python 3.10+ (Standard CPython) | Python 3.12+ / 3.13+ | Abort preflight if < 3.10; emit `BLOCKED: Unsupported Python version`. |
| **Networking** | Loopback Interface | OS loopback socket (`127.0.0.1`) with ephemeral port allocation | None required | If loopback binding fails, emit `BLOCKED: Socket bind permission denied`. |
| **Timer / Clock** | Monotonic Clock | POSIX / Windows `time.monotonic_ns()` (nanosecond resolution) | OS high-resolution hardware counters | Fallback to `time.monotonic()` if nanosecond clock is unavailable. |
| **Cryptographic Hashing** | Hash & MAC Primitives | `hashlib` (SHA-256, SHA-512), `hmac`, `secrets` | None required | Standard library is universally present; zero external dependencies. |
| **Password Hashing** | Slow Hashing Functions | `hashlib.pbkdf2_hmac` (SHA-256, >= 600,000 iterations) | `argon2-cffi` (Argon2id per RFC 9106) | If `argon2-cffi` is missing, seamlessly fall back to PBKDF2; test passes. |
| **Symmetric / Asymmetric** | Advanced Crypto | Educational mock primitives using HMAC & RSA stubs | PyCA `cryptography` (>= 42.0.0) | Capability detection: if absent, skip hardware-accelerated AES-GCM tests. |
| **Database** | Relational Storage | `sqlite3` in-memory (`:memory:`) or ephemeral temp files | External PostgreSQL/MySQL | Built-in SQLite requires zero external server processes. |
| **Web Server** | Localhost HTTP | `http.server`, `urllib.parse`, `urllib.request` | FastAPI, Flask, Starlette | Standard library server requires zero pip packages. |
| **Process / Isolation** | Ephemeral Sandboxing | `tempfile.TemporaryDirectory()`, standard process context | Docker / Podman containers | Zero assumption of container runtimes or root privileges. |

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
        "python_version": sys.version_info >= (3, 10),
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

    # Detect optional packages
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

1. **`[PRINCIPLE]`**: Fundamental mathematical, computer science, or system invariants that hold universally across technologies (e.g., "Code and data must be structurally separated to prevent injection", "Hashing is a one-way irreversible compression function").
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
- **Required Security Property:** [Integrity | Authentication | Non-Repudiation | Confidentiality]
- **Selected Standard Primitive:** [Hash | MAC | Digital Signature | AEAD Symmetric | Asymmetric]
- **Normative Specification:** [RFC / NIST Standard]
- **Chosen Implementation:** [Standard library module and function]
- **Invariant Verification:**
  - Nonce / Salt Strategy: [Description of randomness and uniqueness guarantees]
  - Constant-Time Verification: [Function used for comparison]
  - Error Handling & Information Leak Defense: [Exceptions caught, generic error responses]
```

#### Template 2: Empirical Systems Measurement Record
```markdown
### Measurement Protocol & Latency Record: [Workload Name]
- **Experimental Hypothesis:** [Clear statement of expected behavior]
- **Workload Model:** [Open Model (arrival schedule) | Closed Model (synchronous)]
- **Clock Source:** [`time.monotonic_ns()`]
- **Warm-Up Criteria:** [Duration or iterations discarded before recording]
- **Coordinated Omission Mitigation:** [Description of arrival-time tracking]
- **Empirical Results (Learner to Record):**
  - Sample Count ($n$): `[TO BE RECORDED]`
  - Min Latency: `[TO BE RECORDED]`
  - Median (p50): `[TO BE RECORDED]`
  - 90th Percentile (p90): `[TO BE RECORDED]`
  - 99th Percentile (p99): `[TO BE RECORDED]`
  - Max Latency: `[TO BE RECORDED]`
- **Distribution Shape:** [Unimodal | Bimodal | Heavy-Tailed | Multimodal]
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
┌──────────────────┬─────────────────┬─────────────────┬────────────────────────────────┐
│ Primitive Class  │ Key Required    │ Math Transform  │ Security Guarantees            │
├──────────────────┼─────────────────┼─────────────────┼────────────────────────────────┤
│ Hash (SHA-256)   │ None            │ One-Way Digest  │ Integrity (Tamper Detection)   │
│ MAC (HMAC-SHA256)│ 1 Shared Secret │ Keyed Hash      │ Integrity + Authenticity       │
│ Signature (RSA/Ed)│ Keypair (Priv/Pub) Asymmetric Math │ Authenticity + Non-Repudiation │
│ AEAD (AES-GCM)   │ 1 Shared Secret │ Cipher + AuthTag│ Confidentiality + Authenticity │
└──────────────────┴─────────────────┴─────────────────┴────────────────────────────────┘
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
[ Layer 4: Proof of Possession ] ──── Client verifies server possesses private key (TLS Handshake)
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

#### Visual M22-V3: Code vs. Data: AST Parsing Boundary in SQL Queries
- **Purpose:** Contrast vulnerable string concatenation with structural AST separation in parameterized queries.
- **Layout Blueprint:**
```
CONCATENATION:
  "SELECT * FROM users WHERE name = '" + "admin' OR '1'='1" + "'"
  AST Parsed AFTER Concatenation:
  Query ──► WHERE ──► OR ──► BinaryOp (=) ──► True! (Syntax Altered!)

PARAMETERIZED:
  SQL: "SELECT * FROM users WHERE name = ?"  Param: "admin' OR '1'='1"
  AST Parsed BEFORE Parameter Binding:
  Query ──► WHERE ──► Equals (Column: name, LiteralString: "admin' OR '1'='1")
  (Syntax Invariant Preserved; Input Treated Exclusively as Value Data)
```

#### Visual M22-V4: Browser Vulnerabilities & Defensive Boundaries (XSS, CSRF, SSRF)
- **Purpose:** Map the three browser-mediated vulnerabilities and their exact architectural mitigation boundaries.
- **Layout Blueprint:**
```
┌──────────────┬─────────────────────────┬────────────────────────┬─────────────────────────────┐
│ Threat Class │ Execution Boundary      │ Attack Mechanism       │ Definitive Architectural Fix│
├──────────────┼─────────────────────────┼────────────────────────┼─────────────────────────────┤
│ XSS          │ Browser DOM / Engine    │ Script injected in HTML│ Context Encoding + CSP Nonce│
│ CSRF         │ Cross-Origin HTTP Hop   │ Ambient Cookie Hijack  │ SameSite=Lax + Anti-CSRF Tok│
│ SSRF         │ Server Outbound Egress  │ Server tricked into LAN│ URL Policy + Socket Binding │
└──────────────┴─────────────────────────┴────────────────────────┴─────────────────────────────┘
```

#### Visual M22-V5: The 6-Layer Software Supply Chain Integrity Model
- **Purpose:** Structure software supply chain defense into six progressive layers from version to provenance.
- **The 6 Layers:**
```
[ Layer 1: Version Pinning ] ───────── Semantic version lock (`==2.31.0`)
             │
             ▼
[ Layer 2: Cryptographic Hash Pinning ] SHA-256 artifact digest lock (`--require-hashes`)
             │
             ▼
[ Layer 3: Build Reproducibility ] ── Byte-for-byte independent build verification
             │
             ▼
[ Layer 4: Signature Verification ] ── Cryptographic signature check on package artifact
             │
             ▼
[ Layer 5: Signer Identity Binding ] ─ Verifying signing key belongs to trusted maintainer
             │
             ▼
[ Layer 6: Provenance Attestation ] ── SLSA v1.2 authenticated build pipeline record
```

### 27.3 Module M23 Visual Specifications

#### Visual M23-V1: Scientific Systems Measurement Architecture
- **Purpose:** Detail the pipeline from hypothesis to unskewed empirical distribution.
- **Layout Blueprint:**
```
[ Formal Hypothesis ] ──► [ Workload Generator (Open Arrival Model) ]
                                    │
                                    ▼
                         [ System Under Test ]
                                    │
                         (High-Res Monotonic Clock)
                                    ▼
                         [ Discard Warm-Up Transients ]
                                    │
                                    ▼
                         [ Full Latency Histogram ]
                                    │
                                    ▼
                         [ Percentiles: p50, p90, p99, p99.9 ]
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
- **Purpose:** Connect architectural claims directly to admissible evidence types, illustrating evidence sufficiency.
- **Layout Blueprint:**
```
Architectural Claim ──────────► Required Evidence Category ──► Admissible Artifacts
──────────────────────────────────────────────────────────────────────────────────
"High Availability"   ───────► Failure & Recovery Proof    ──► Crash Injection Log / WAL Proof
"Sub-50ms p99 Latency" ──────► Empirical Measurement       ──► Monotonic Arrival Benchmark
"Secure from Injection" ─────► Structural AST Separation   ──► Parameterized API + Tests
"Low Operational Cost" ──────► Fermi Capacity Model        ──► Sizing Math + Cloud Pricing
```

#### Visual M24-V3: Pre-Ship Verification & Risk-Prioritized Release Pipeline
- **Purpose:** Detail the multi-stage pre-flight release gates from regression testing to telemetry verification and rollback assurance.
- **Layout Blueprint:**
```
[ Code Commit ] ──► [ Gate 1: Invariant & Regression Tests (100% Pass) ]
                                    │
                                    ▼
                    [ Gate 2: Security & Dependency Hash Audit ]
                                    │
                                    ▼
                    [ Gate 3: Empirical Performance Baseline Check ]
                                    │
                                    ▼
                    [ Gate 4: Database Migration Rollback Dry-Run ]
                                    │
                                    ▼
                    [ Gate 5: Telemetry & Structured Logging Check ]
                                    │
                                    ▼
                    [ PRODUCTION RELEASE (Canary Deployment) ]
```


## 28. Authoritative Sources, Currentness Recheck & Provenance Register

### 28.1 Normative Source Register & Currentness Audit
All normative claims in Stage 7 are grounded in authoritative technical specifications re-checked at Design execution time (September 2026).

| Source Identifier | Version / Revision | Publication Date | Formal Status | Checked Date | Claim Supported | Boundary / What Source Does Not Prove | Drift Classification | Rights & Licensing Boundary |
|---|---|---|---|---|---|---|---|---|
| **NIST SP 800-63B-4** | Final Revision 4 | July 2025 | Official US Gov Standard | 2026-09-07 | Password storage: salt >= 32 bits, memory-hard recommended; single-factor >= 15 chars, MFA >= 8 chars; composition rules abolished. | Does not endorse specific commercial password managers or hardware tokens. | **CURRENT** | US Gov work; attribution required; non-US copyright protections may apply per D-016. |
| **NIST SP 800-131A Rev. 2 / Rev. 3 IPD** | Rev. 2 (active) / Rev. 3 (Initial Public Draft) | Oct 21, 2024 (draft) | Active Standard / Draft in progress | 2026-09-07 | Transitioning cryptographic algorithms; SHA-1 disallowed for signatures; 112-bit security deprecated. | Rev. 3 is a draft and not yet final normative policy. | **CURRENT / FRONTIER** | US Gov work; subject to public comment revisions. |
| **RFC 9846** | Standards Track | July 2026 | Proposed Standard (Obsoletes RFC 8446, 5246, 5077) | 2026-09-07 | TLS 1.3 protocol specification; mandatory forward secrecy, AEAD only, encrypted handshakes. | Does not prove application-layer security above the TLS transport. | **STABLE / CURRENT** | IETF Trust Legal Provisions (TLP); Code Components under Revised BSD. |
| **RFC 9525** | Standards Track | May 2024 | Proposed Standard (Obsoletes RFC 6125) | 2026-09-07 | Service identity verification in TLS; MUST check SAN, MUST NOT use CN fallback. | Does not validate web application authorization policies. | **STABLE / CURRENT** | IETF TLP; Code Components under Revised BSD. |
| **RFC 9700 / BCP 240** | Best Current Practice 240 | January 2025 | IETF Best Current Practice | 2026-09-07 | OAuth 2.0 Security BCP: PKCE MUST for public, RECOMMENDED for confidential; ROPC MUST NOT; exact redirect matching. | Does not define identity assertion schemas (handled by OpenID Connect). | **CURRENT** | IETF TLP; non-commercial educational citation. |
| **draft-ietf-oauth-v2-1-15** | Working Group Draft | March 2026 | Active Internet-Draft | 2026-09-07 | Consolidated OAuth 2.1 authorization framework incorporating BCP 240. | Draft status; subject to minor text revisions before final RFC publication. | **CURRENT / FRONTIER** | IETF Trust copyright; educational citation only. |
| **W3C CSP Level 3** | Working Draft | 13 August 2026 | W3C Working Draft | 2026-09-07 | Nonce-based Content Security Policy (`'strict-dynamic'`) for script execution. | Does not prevent server-side template injection or DOM clobbering. | **CURRENT** | W3C Document License; freely citeable. |
| **RFC 9106** | Informational | September 2021 | IETF Informational (Argon2) | 2026-09-07 | Memory-hard password hashing algorithm (Argon2id). | Does not replace transport encryption or database security. | **STABLE** | RFC Editor / IETF TLP. |
| **OpenSSF SLSA v1.2** | Specification v1.2 | September 2024 | Approved (v1.0 retired) | 2026-09-07 | Supply chain levels for software artifacts; verifiable build provenance attestations. | Does not guarantee that source code is free of developer-authored bugs. | **CURRENT** | Community Specification License 1.0; open attribution. |
| **PyCA cryptography** | v50.0.1 | August 25, 2026 | Production Python Package | 2026-09-07 | Reference Python cryptographic primitives implementation. | Package is an optional enhancement; not required for Core baseline pass. | **CURRENT** | Dual-licensed Apache 2.0 / BSD 3-Clause. |

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

### 29.3 Canonical Competency Vocabulary
Stage 7 exclusively utilizes the 8 canonical competency verbs defined in `meta/COMPETENCY_MATRIX.md`:
1. `Trace` (跟踪)
2. `Explain` (解释)
3. `Observe` (观察)
4. `Diagnose` (诊断)
5. `Correctness` (正确性证明/保障)
6. `Judge` (权衡与判断)
7. `Estimate` (数量级估算)
8. `Learn-New-Tech` (新技术学习)
Zero non-standard competency terms are used.

---

## 30. Machine-Checkable vs. Reviewer-Required Verification Matrix

| Module | Lesson | Machine-Checkable Gates (Automated Test Suites) | Reviewer-Required Gates (Web Lead / Peer Review) |
|---|---|---|---|
| **M21** | `L21-01` | Path sanitization test (rejecting `../` traversal, null bytes, out-of-sandbox targets). | Evaluation of threat model boundary diagram and asset inventory. |
| **M21** | `L21-02` | `pytest test_m21.py`: Salt randomness, slow hash iterations, constant-time `hmac.compare_digest`. | Review of primitive selection rationale (Hash vs MAC vs Signature vs AEAD). |
| **M22** | `L22-01` | JWT signature verification, expiration check, audience check, rejection of `alg: "none"`. | Review of stateful vs stateless token revocation trade-off analysis. |
| **M22** | `L22-02` | `pytest test_m22.py`: SQL parameterization, CSRF token validation, SSRF IP blocklist checks. | Architectural review of SSRF DNS rebinding socket egress defense. |
| **M22** | `L22-03` | Lockfile parser test validating SHA-256 hash checks and rejecting tampered digests. | Inspection of third-party dependency adoption evaluation criteria. |
| **M23** | `L23-01` | Unit test proving arrival-scheduled benchmark records queued latency under stalls. | Review of measurement protocol, warm-up criteria, and distribution plots. |
| **M23** | `L23-02` | Schema validation of JSON/Markdown ADR ensuring all 12 dimensions are completed. | Qualitative evaluation of technology trade-off reasoning and rejection defense. |
| **M23** | `L23-03` | Numeric calculation verification of storage growth, egress bandwidth, and memory sizing. | Review of stated assumptions, unit conversions, and bottleneck identification. |
| **M24** | `L24-01` | Automated validation of 16-trace completeness in capstone defense document. | In-depth defense review, evidence sufficiency audit, and changed-constraint challenge. |
| **M24** | `L24-02` | Pre-flight test suite pass, schema rollback test execution, health endpoint response. | Review of risk-prioritized pre-ship verification checklist and operational readiness. |

---

## 31. Safety, Watchdogs & Deterministic Cleanup Design

To protect host hardware, ensure reliable CI test runs, and strictly adhere to the Hardware Safety Rules:

1. **Zero Uncontrolled Disk Writes & Debounce Guarantees:**
   - All ephemeral test databases run in-memory (`:memory:`) or within an auto-cleaning `tempfile.TemporaryDirectory()`.
   - Logging and metrics exercises enforce memory buffers with periodic flush intervals (minimum debounce >= 2000ms in interactive tools).
   - Zero physical disk thrashing or repeated full-disk scans.

2. **Deterministic Process & Socket Teardown:**
   - All localhost servers (`http.server` instances in M22) run in daemon threads and are wrapped in Python `try...finally` context managers:
     ```python
     server = HTTPServer(("127.0.0.1", 0), SafeHandler)
     try:
         threading.Thread(target=server.serve_forever, daemon=True).start()
         yield server
     finally:
         server.shutdown()
         server.server_close()
     ```
   - All client socket connections enforce explicit timeouts (`timeout=2.0`).

3. **5.0-Second Watchdog Timers:**
   - Every network activity and benchmark harness includes a 5.0-second safety watchdog thread that forcibly closes sockets and triggers test failure if an unhandled deadlock or infinite loop occurs.

4. **Zero State Pollution:**
   - Ephemeral files, mock lockfiles, and temporary database files are wiped deterministically in pytest fixture teardown routines.

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

Every gate required by the Issue #114 Task Contract has been evaluated and recorded:

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
| **12** | Only canonical competency vocabulary | **PASS** | Section 29.3 uses exclusively the 8 canonical verbs from `COMPETENCY_MATRIX.md`. |
| **13** | M21 crypto-use / no crypto-implementation boundary | **PASS** | Section 6.2 and 8 mandate standard library primitives; zero custom crypto implementations. |
| **14** | PKI/authn/authz layers separated | **PASS** | Section 3.1 and 27.1 define the 6-layer PKI model separating credentials, identity, authn, authz. |
| **15** | M22 authn/authz/session/token/OAuth/OIDC boundaries | **PASS** | Section 11 separates credentials from identities and sessions from bearer tokens. |
| **16** | Password currentness/normative strength source-bounded | **PASS** | Section 3.1 and 8 ground password rules strictly in NIST SP 800-63B-4. |
| **17** | Web-security composition boundaries | **PASS** | Section 12 details structural AST separation for SQLi, CSP3 for XSS, SameSite/tokens for CSRF, socket binding for SSRF. |
| **18** | Supply-chain provenance boundaries | **PASS** | Section 13 and 27.2 establish the 6-layer supply-chain integrity model based on SLSA v1.2. |
| **19** | Safe-target Candidate B explicitly accept/refine/reject | **PASS** | Section 5 explicitly **ACCEPTS AND REFINES Candidate B**. |
| **20** | No new Required Lab ID/count | **PASS** | Section 5.2 confirms Required Labs remain exactly 5, Optional 5, Expeditions 5. Zero new labs. |
| **21** | No public/real target/offensive dependency | **PASS** | Strictly localhost `127.0.0.1` ephemeral testing; zero offensive scanners or remote targets. |
| **22** | Fixture candidate has preflight/reset/cleanup/evidence/safety | **PASS** | Sections 9, 14, 19, 24, 31 define preflight, isolation, watchdogs, and deterministic cleanup. |
| **23** | M23 question-driven measurement / no universal constants | **PASS** | Section 16 rejects dogmatic "n=30" and "p99" rules; establishes question-driven workload design. |
| **24** | D-015 exact 12 dimensions | **PASS** | Section 17 details all 12 dimensions of Decision D-015 for technology evaluation. |
| **25** | AI handling does not resolve OQ-BP-001 | **PASS** | Section 15.2 and 17 treat AI outputs as unverified candidate hypotheses; OQ-BP-001 remains OPEN. |
| **26** | M23 estimate/cost units/assumptions/inference limits | **PASS** | Section 18 details Fermi estimation, units (b vs B), assumptions, and bottleneck sensitivity. |
| **27** | M24 integration only / no new mechanism | **PASS** | Section 20 confirms M24 is purely an integrative evaluation capstone introducing zero new mechanisms. |
| **28** | M24 evidence→claim and changed-constraint design | **PASS** | Section 21 and 23 define the 16 architectural traces, 12 evidence areas, and constraint challenges. |
| **29** | Design owns final assessment contract but no universal scoring formula | **PASS** | Section 23 establishes the binary criteria-gated assessment rubric; rejects point formulas. |
| **30** | STABLE/CURRENT/FRONTIER classification | **PASS** | Section 28 classifies every source into STABLE, CURRENT, or FRONTIER. |
| **31** | Exact current source revisions/dates/statuses recorded | **PASS** | Section 28 records exact publication dates, formal statuses, and checked dates. |
| **32** | Rights/license/provenance recorded | **PASS** | Section 28 details rights and licensing boundaries (NIST, IETF TLP BSD, OpenSSF, PyCA). |
| **33** | OQ-BP-001/003/006 remain OPEN | **PASS** | Section 32.2 explicitly confirms all three open questions remain OPEN and RFC-gated. |
| **34** | Issue #34 remains OPEN / DEFERRED / NON-BLOCKING | **PASS** | Section 32.2 preserves Issue #34 as non-blocking per Decision D-027. |
| **35** | Consensus Registry ID remains deferred | **PASS** | Section 29.2 confirms Consensus Registry ID remains deferred per Decision D-025. |
| **36** | No unrelated S1–S6 churn | **PASS** | Working tree contains zero modifications to Stages 1–6 files. |
| **37** | Implementation-batch recommendation present | **PASS** | Section 4 specifies 4 bounded implementation batches (S7-B1 through S7-B4). |
| **38** | Evidence templates neutral / no fabricated volatile outcomes | **PASS** | Section 25.2 strictly prohibits prefilled volatile numbers, ports, timestamps, or fake PASS. |
| **39** | Visuals specified / no copied third-party diagrams | **PASS** | Section 27 specifies 15 original visual layouts and ASCII blueprints. |
| **40** | `git diff --check` passes cleanly | **PASS** | Verified zero whitespace errors, trailing spaces, or carriage return mismatches. |

---

## 34. Final Recommendation & Readiness Sign-Off

### Final Recommendation: **READY FOR LESSON / ACTIVITY IMPLEMENTATION**

The Stage 7 Design Dossier v0.1 establishes a complete, rigorous, and defensible architectural blueprint for Modules M21–M24. All technical constraints, normative standards, concept registries, safe-target boundaries, and evaluation rubrics are fully specified and reconciled with curriculum invariants.

**Explicit Scope Limitation:**
This design sign-off authorizes the creation of bounded implementation tasks for Batches S7-B1 through S7-B4. It does **NOT** imply that learner lessons have been drafted, that activities are implemented, that learner validation is complete, or that Stage 7 is VERIFIED or RELEASED.

READY FOR LESSON / ACTIVITY IMPLEMENTATION
