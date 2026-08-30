# Open Questions

Only unresolved questions that can materially affect curriculum architecture, technical truth, or implementation should live here.

## Active — post-Blueprint

Blueprint v0.1 passed the Final Exit Audit in Issue #23 / PR #24 and is closed. The following remain **open** after Blueprint closure — each is either a Core-scope escalation (requires RFC/Decision) or an implementation-time pin deliberately deferred to the first affected vertical slice / implementation work. Their open status does not by itself reopen Blueprint.

### OQ-BP-001 — Where does bounded AI literacy belong? (OPEN — Core-scope escalation)

**Question:** For a 2026 modern computing-system worldview, should bounded AI literacy be a Core thread/module, a Current Case, or another explicitly justified placement?

The stable capability candidates: problem suitability vs data/model/evaluation failure; uncertainty; resource cost; security/privacy/impact; when-not-to-use reasoning. The external audit found a real coverage gap, but CS2023 inclusion alone is not sufficient reason to expand Essential CS Core.

**Safe interim state (already accepted, do not weaken):** AI-generated output verification = Current Case / technical-literacy practice (R5: generated code/doc/claim is an untrusted hypothesis checked by source, test, measurement, security review — homes M00 `L00-02`, M23 `L23-02`); **no AI/ML/LLM Core module yet**.

**Escalation:** Core-scope change requires RFC/Decision. RFC candidate: `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md` (candidate only — it does not decide the question).

### OQ-BP-003 — What bounded human-facing system boundary belongs in Core? (OPEN — Core-scope escalation)

**Question:** Where should user mental models, feedback/error recovery, accessibility, consent/privacy interaction, and human-facing failure enter the system journey?

The goal is not a full HCI course. Evidence hooks (denial/error/privacy interaction at P2; affected users, accessibility, consent, recovery where relevant at P9) are already accepted and remain **without** turning them into canonical Core HCI content.

**Escalation:** Core-scope change requires RFC/Decision. RFC candidate: `meta/rfcs/RFC-CAND-002-human-facing-boundary.md` (candidate only — does not decide the question).

### OQ-BP-006 — What versions define the first stable environment? (OPEN — implementation-time pin)

Exact Python, SQLite/PostgreSQL case version, Linux/dev-container base, compiler/toolchain (incl. QEMU/RISC-V cross-toolchain for LAB-REQ-02), browser, and optional container/observability versions remain to be pinned when the first module dossier and lab implementation require them. Closely related but separately tracked: the canonical latency-constant list (R11) and its refresh cadence (CURRENT per Living Curriculum Policy).

## Resolved during Issue #9 reconciliation (closed, for provenance)

### OQ-BP-002 — Applied foundations and toolchain prerequisites (CLOSED)

- Applied measurement/statistics: canonical first home = M04 `L04-02` (R1: repeated measurements, distributions, median/percentiles when useful, uncertainty/variation, inference limits, order-of-magnitude reasoning; pattern = question/hypothesis → baseline → controlled change → metric/environment/workload → repetitions/distribution → observation → competing explanation → bounded conclusion). Revisits: M13, M16/M17 (reliability/failure probability just-in-time), M20, M23 (consolidation). No standalone mathematics Module; no math gate before M01.
- Toolchain/SDF: explicit learner outcomes at M00 `L00-02` (shell/task execution, code/file reading, debugger-light investigation, Git evidence, reproducibility/version/environment record, baseline + evidence preservation) + REQUIRED-lab entry gate (course discipline, not a DAG edge); environment preflight repeated at M03/M06/M13.
- The open sub-note (whether the M04 bridge also carries percentile-of-latency vocabulary) is answered by the same home: yes as application, no new theory.
- Source: `meta/blueprint/audit-to-architecture-disposition-v0.1.md` §4.1–4.2; `core-stage-module-lesson-map-v0.1.md` §4 (M00/M04).

### OQ-BP-004 — Default S4/S5 learner narrative (CLOSED)

Default = **request-centric narrative S4-before-S5**; explicitly labeled pedagogical preference, **not** a hard dependency. S4/S5 partial independence preserved; Module DAG authoritative; a state-centric path (M13–M15 after S3, then M10–M12) is equally supported. No Stage names changed.

### OQ-BP-005 — Final classic lab adoption/adaptation (CLOSED at Blueprint level)

Resolved by the accepted selection map (`lab-source-selection-map-v0.1.md`, PR #16): 5 Required (LAB-REQ-01..05), 5 Optional (LAB-OPT-01..05), 5 Source Expeditions (EXP-01..05). Remaining items are **not** architecture decisions: optional-rights gates (CS:APP, CS144, OSTEP link-only), environment setup validation, and per-lab dossier smoke tests.

## Rule

Do not decide major curriculum questions opportunistically while writing a lesson. Record the question, research it, and use an RFC/Decision when it changes Core scope, philosophy, or major technical choices. Escalation path: `Open Question → Research → RFC if needed → Decision → New Task` (see `meta/REVIEW_POLICY.md`).
