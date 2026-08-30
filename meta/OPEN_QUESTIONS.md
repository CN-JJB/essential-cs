# Open Questions

Only unresolved questions that can materially affect curriculum architecture, technical truth, or implementation should live here.

## Current — Blueprint reconciliation

Requirements-phase governance questions are complete. The following Blueprint questions are active inputs to Issue #9.

### OQ-BP-001 — Where does bounded AI literacy belong?

**Question:** For a 2026 modern computing-system worldview, should bounded AI literacy be a Core thread/module, a Current Case, or another explicitly justified placement?

The external audit found a real coverage gap, but CS2023 inclusion alone is not sufficient reason to expand Essential CS Core. The decision must identify the stable mechanism/judgment learners need (problem suitability, data/model/evaluation failure, uncertainty, resource cost, security/privacy/impact) without turning the curriculum into an AI course or a fast-decaying product survey.

**Escalation:** Core-scope change requires RFC/Decision.

### OQ-BP-002 — How explicit should applied foundations and toolchain prerequisites be?

**Question:** What are the canonical first homes and minimum Core depth for:

- just-in-time discrete/probability/statistical reasoning needed for complexity, measurement, uncertainty, reliability and evaluation;
- shell, code reading, debugging/profiling, Git, testing, packaging and reproducibility?

Issue #1 already places basic tooling in M00 and flags statistics as a hidden prerequisite; Issue #2 argues these capabilities need more explicit outcomes and assessment. Reconciliation must strengthen prerequisites without importing a standalone degree-style mathematics or software-engineering sequence by default.

**Escalation:** RFC only if the resolution materially changes Core scope/structure; otherwise Issue #9 may integrate explicit outcomes into existing Modules/threads.

### OQ-BP-003 — What bounded human-facing system boundary belongs in Core?

**Question:** Where should user mental models, feedback/error recovery, accessibility, consent/privacy interaction, and human-facing failure enter the system journey?

The goal is not a full HCI course. The question is whether a bounded human/accessibility boundary is necessary for accurate modern-system judgment and where its canonical teaching home should be (for example M00, Browser/Web, Mini Cloud App, Systems Judgment, or a spiral with one primary home).

**Escalation:** Core-scope change requires RFC/Decision.

### OQ-BP-004 — What is the default S4/S5 learner narrative?

The corrected dependency graph establishes that S4 (Network/Web) and S5 (Data/Concurrency) are partially independent after S3 and both feed S6. The remaining question is pedagogical narrative: Network/Web first (request-centric journey) vs Data/Concurrency first (state-centric journey), plus final Stage naming/granularity.

This is **not** a hard-dependency question.

### OQ-BP-005 — Which classic labs are finally Adopted or Adapted?

Issue #4 produced candidates, not final Labs. Final selection must resolve license/provenance, canonical Linux reproducibility, setup burden, cognitive load, safety, smoke tests, cleanup/reset, exact stopping points, and project overlap.

### OQ-BP-006 — What versions define the first stable environment?

Exact Python, SQLite/PostgreSQL case version, Linux/dev-container base, compiler/toolchain, browser, and optional container/observability versions remain to be pinned only when Blueprint architecture and required Labs make the dependency necessary.

## Rule

Do not decide major curriculum questions opportunistically while writing a lesson. Record the question, research it, and use an RFC/Decision when it changes Core scope, philosophy, or major technical choices.
