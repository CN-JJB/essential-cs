# RFC Candidate — Bounded AI Literacy (OQ-BP-001)

**Status:** CANDIDATE — records the question and evidence requirements. **This document does not decide anything.** A decision requires the project's RFC/Decision process, Developer Lead review, and, if Core scope changes, a Decision Record.

**Open Question:** `meta/OPEN_QUESTIONS.md` — OQ-BP-001
**Source of the question:** External Curriculum Audit R4 (`external-curriculum-audit-v0.1.md` §5.4) + accepted disposition (`audit-to-architecture-disposition-v0.1.md` §6.2)
**Created:** 2026-08-30 (Issue #9 integration)

## 1. Question

For a 2026 modern computing-system worldview, should bounded AI literacy / data-model judgment be:

- (A) a Core thread spiraled through M02/M13/M20/M21–M23;
- (B) one bounded M23 technology-judgment module;
- (C) a CURRENT CASE only;
- (D) A + C (stable literacy thread + replaceable tool case)?

## 2. Why it matters

The external audit found a real coverage gap ("generative AI and the curriculum" is an explicit CS2023 component), yet the project Decision states AI/LLM is not automatically a Core topic, and Invariant 10 (modern does not mean trendy) + Invariant 8 (complexity must justify itself) guard against product-driven expansion. Deciding the placement changes what "complete modern computing-system world model" (Invariant 9) means.

## 3. Stable capability at stake

- judging problem suitability versus data/model/evaluation/system failure;
- reading a bounded evaluation (uncertainty, resource cost, privacy/security/impact);
- explicit when-not-to-use reasoning;
- verification of AI-generated claims as a technical-literacy habit (already accepted as CURRENT CASE under R5).

Explicit exclusions if admitted: Transformer/ML/LLM architecture theory, gradient math, training infrastructure, prompt-engineering catalogs, vendor/model surveys, fast-decaying API tutorials, AI product development.

## 4. Evidence already gathered

- CS2023 Final Report: basic-AI-literacy component index (live-verified in the audit's register, 2026-08-30).
- NIST AI RMF 1.0 (Jan 2023), GenAI Profile NIST-AI-600-1 (Jul 2024), RMF under revision; critical-infrastructure concept note (2026-04-07) — supports risk/judgment vocabulary, not a curriculum shape.
- MIT Missing Semester 2026 Agentic Coding + Code Quality lectures — current-practice signal.
- The safe interim pattern is already accepted: generated code/config/claim = untrusted hypothesis verified via source/test/measurement/security review (M00 `L00-02`, M23 `L23-02`).

## 5. Trade-offs

Admission adds first-home ownership and evidence artifacts; non-admission risks a reported coverage gap. A thread-only placement avoids new modules but makes the capability harder to assess; a module placement centers it but risks vocabulary-heavy assessment if not evidence-bound.

## 6. Evidence required before decision

- one bounded learner capability statement (what a learner can *do*, not what they can name);
- first-home choice consistent with the Module DAG (candidate homes use existing edges only — no new H edge);
- one evidence artifact per assessment point;
- review cadence (the 6–12 month current-practice recheck already required by R5);
- explicit list of excluded content (see §3);
- bloat-control check: what existing content shrinks or stays.

## 7. Decision owner

Web Lead (architecture process) with reviewer roles per review policy; recorded via Decision Record if Core scope changes.

## 8. Integration status

**Not blocked for other Blueprint work.** Safe interim state retained: AI-generated output verification = CURRENT CASE / technical-literacy practice; no AI/ML/LLM Core module. No concept ID assigned; no lesson or registry change until the RFC is decided.
