# RFC Candidate — Bounded AI Literacy (OQ-BP-001)

**Status:** RESOLVED FOR v1.0 BY D-033 — historical candidate retained for provenance.

**Open Question:** `meta/OPEN_QUESTIONS.md` — OQ-BP-001 (CLOSED for v1.0)
**Source of the question:** External Curriculum Audit R4 (`external-curriculum-audit-v0.1.md` §5.4) + accepted disposition (`audit-to-architecture-disposition-v0.1.md` §6.2)
**Created:** 2026-08-30 (Issue #9 integration)
**Resolved:** 2026-09-12 (Issue #155; D-033)

## Resolution

For the first stable v1.0 curriculum, do **not** add an AI/ML/LLM Core module or a new canonical Core thread. Retain AI-generated-output verification as the already accepted CURRENT CASE / technical-literacy practice: generated code, documentation, configuration, and claims are untrusted hypotheses checked by source, test, measurement, and security review.

The question may be reopened post-v1.0 if learner evidence, final external-audit evidence, or durable systems-practice evidence justifies a Core-scope change.

## 1. Original question

For a 2026 modern computing-system worldview, should bounded AI literacy / data-model judgment be:

- (A) a Core thread spiraled through M02/M13/M20/M21–M23;
- (B) one bounded M23 technology-judgment module;
- (C) a CURRENT CASE only;
- (D) A + C (stable literacy thread + replaceable tool case)?

## 2. Why it mattered

The external audit found a real coverage gap ("generative AI and the curriculum" is an explicit CS2023 component), yet the project Decision states AI/LLM is not automatically a Core topic, and Invariant 10 (modern does not mean trendy) + Invariant 8 (complexity must justify itself) guard against product-driven expansion.

## 3. Stable capability considered

- judging problem suitability versus data/model/evaluation/system failure;
- reading a bounded evaluation (uncertainty, resource cost, privacy/security/impact);
- explicit when-not-to-use reasoning;
- verification of AI-generated claims as a technical-literacy habit.

Explicit exclusions considered: Transformer/ML/LLM architecture theory, gradient math, training infrastructure, prompt-engineering catalogs, vendor/model surveys, fast-decaying API tutorials, AI product development.

## 4. Evidence considered

- CS2023 Final Report basic-AI-literacy component signal;
- NIST AI RMF / GenAI Profile risk and judgment vocabulary;
- MIT Missing Semester 2026 Agentic Coding + Code Quality as current-practice signal;
- accepted existing pattern at M00 `L00-02` and M23 `L23-02`.

## 5. Trade-off disposition

Admission would add first-home ownership and assessment artifacts late in the stable-candidate cycle. The existing bounded verification practice provides durable technical-literacy value without expanding the systems Core. D-033 therefore selects the bounded CURRENT CASE path for v1.0.
