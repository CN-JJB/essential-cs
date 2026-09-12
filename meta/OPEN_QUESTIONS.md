# Open Questions

Only unresolved questions that can materially affect curriculum architecture, technical truth, or implementation should live here.

## Active — post-Blueprint

Blueprint v0.1 passed the Final Exit Audit in Issue #23 / PR #24 and is closed.

**No post-Blueprint Open Question currently blocks the first stable-release candidate.** Final stable release still remains gated by the explicit verification/audit/learner-validation/release Issues; closing an Open Question does not satisfy those gates.

Closely related but separately tracked: the canonical latency-constant list (R11) and its refresh cadence (CURRENT per Living Curriculum Policy).

## Resolved after Blueprint closure

### OQ-BP-006 — What versions define the first stable environment? (CLOSED — realized pin technically re-verified)

**Strategy decided in D-032:** use a digest-addressed Ubuntu 24.04 LTS (Noble)-based canonical learner/test environment; standard GitHub-hosted `ubuntu-24.04` is only a moving execution substrate, not the immutable pin. Compatibility floors are Python >= 3.12, SQLite engine + `sqlite3` CLI >= 3.45, GCC >= 13/C11, curl >= 8.5, and GDB >= 15.0, with GDB required for canonical M03 evidence. LAB-REQ-02 retains exact xv6 source identity and lane-scoped full QEMU/RISC-V package/image identity. strace, browser/Chromium, PostgreSQL/psql, live observability backends, Docker/Podman, and arm64 remain capability-gated or optional according to the accepted curriculum boundary.

**Realized immutable identity:** Issue #150 / PR #152 produced and Web Lead accepted the committed canonical definition, durable GHCR digest, resolved package identities, least-privilege publication/retrieval workflow, canonical-fast evidence, and real LAB-REQ-02 QEMU evidence:

`ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460`

**Technical re-verification accepted:** Issue #153 v0.2 / PR #165 re-verified that exact durable object against locked base `cd7396cad6ca746c55217968aafc59a8d3dd7369`. Web Lead accepted verifier-owned exact-base canonical-fast and QEMU evidence, fresh digest retrieval/environment capture, package-floor truth, least-privilege/pin-refresh governance, and downloaded artifact digests/inventories. PR #165 merged as `8c1c30a7c20ac8631675e798a3c535cef8bf1c3c`.

Issue #153 v0.2 is explicitly **same-lineage technical re-verification**, not final role-independent evidence. Closing OQ-BP-006 means the environment version/identity question itself is technically decided and realized; it does **not** waive the final independent stable gate. Issue #158 must independently re-check the canonical environment as part of final multi-role verification before v1.0.

**Provenance:** Issue #143 / PR #144 (D-032); Issue #150 / PR #152 (realized pin); Issue #153 v0.2 / PR #165 (accepted technical re-verification); Issue #158 (remaining final independent stable verification gate).

### OQ-BP-001 — Where does bounded AI literacy belong? (CLOSED for v1.0)

**Decision:** For the first stable v1.0 curriculum, do **not** expand the accepted M00–M24 Core spine with an AI/ML/LLM module or new canonical Core thread. Retain the already accepted safe coverage: AI-generated code/document/claim is an untrusted hypothesis checked by source, test, measurement, and security review, with homes such as M00 `L00-02` and M23 `L23-02`. This remains a CURRENT CASE / technical-literacy practice, not a new Core theory obligation.

**Why:** The external audit identified a real modern-literacy consideration, but the RFC candidate also records the bloat, assessment, and durability trade-offs. The current first stable candidate already has a complete reviewed M00–M24 systems spine. A late Core expansion is not justified for v1.0 and would destabilize the accepted architecture without evidence of proportional learning value.

This does not say AI literacy is unimportant and does not freeze the decision forever. Post-v1.0 evidence may reopen the question through the normal Open Question → Research → RFC → Decision process.

**Provenance:** RFC candidate `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md`; Issue #155; D-033.

### OQ-BP-003 — What bounded human-facing system boundary belongs in Core? (CLOSED for v1.0)

**Decision:** For the first stable v1.0 curriculum, do **not** add a new canonical HCI/accessibility Core first home or module. Retain the already accepted human-facing evidence hooks in Mini Cloud P2/P9 and relevant browser/security/privacy lessons: observable denial/error behavior, recovery, consent/privacy interaction, affected-user reasoning, and accessibility consideration where relevant.

**Why:** The gap is legitimate, but the project is a computing-systems curriculum rather than a full HCI course. The accepted project hooks expose the boundary without introducing a late new Core concept family and assessment surface. The RFC's explicit exclusions and bloat-control concern support keeping the first stable scope bounded.

Post-v1.0 learner/external-audit evidence may reopen the question through the normal architecture process.

**Provenance:** RFC candidate `meta/rfcs/RFC-CAND-002-human-facing-boundary.md`; Issue #155; D-034.

### OQ-BP-007 — Must learner validation block each subsequent authoring slice? (CLOSED)

**Decision:** No. Production uses a build-first bounded-batch sequence. Real learner validation remains mandatory before v1.0 / `RELEASED`, but it is non-blocking for continued course authoring.

**Why:** Real learner evidence cannot be truthfully synthesized by an AI-only production pipeline, and the project owner explicitly chose to finish the full course before studying it gradually. The quality risk from delayed learner feedback is mitigated through bounded batches and independent technical/pedagogical/lab/integration review.

**Provenance:** Issue #36; `research/build-first-production-sequencing-v0.1.md`; `meta/rfcs/RFC-003-build-first-production-sequencing.md`; D-027.

## Resolved during Issue #9 reconciliation

### OQ-BP-002 — Applied foundations and toolchain prerequisites (CLOSED)

- Applied measurement/statistics: canonical first home = M04 `L04-02`; revisits M13, M16/M17, M20, M23.
- Toolchain/SDF: explicit learner outcomes at M00 `L00-02` plus REQUIRED-lab entry gate; environment preflight repeated at M03/M06/M13.
- Percentile-of-latency vocabulary is an application at the same M04 home, not new theory.
- Source: `meta/blueprint/audit-to-architecture-disposition-v0.1.md` §4.1–4.2; `core-stage-module-lesson-map-v0.1.md` §4.

### OQ-BP-004 — Default S4/S5 learner narrative (CLOSED)

Default = **request-centric narrative S4-before-S5**; explicitly a pedagogical preference, not a hard dependency. S4/S5 partial independence and the authoritative Module DAG are preserved.

### OQ-BP-005 — Final classic lab adoption/adaptation (CLOSED at Blueprint level)

Resolved by the accepted selection map (`lab-source-selection-map-v0.1.md`, PR #16): 5 Required, 5 Optional, 5 Source Expeditions. Remaining rights/environment/smoke work is implementation/review work rather than an architecture decision.

## Rule

Do not decide major curriculum questions opportunistically while writing a lesson. Record the question, research it, and use an RFC/Decision when it changes Core scope, philosophy, or major technical choices. Escalation path: `Open Question → Research → RFC if needed → Decision → New Task` (see `meta/REVIEW_POLICY.md`).
