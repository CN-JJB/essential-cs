# RFC Candidate — Human-Facing System Boundary (OQ-BP-003)

**Status:** CANDIDATE — records the question and evidence requirements. **This document does not decide anything.** A decision requires the project's RFC/Decision process, Web Lead review, and, if Core scope changes, a Decision Record.

**Open Question:** `meta/OPEN_QUESTIONS.md` — OQ-BP-003
**Source of the question:** External Curriculum Audit R3 (`external-curriculum-audit-v0.1.md` §5.3) + accepted disposition (`audit-to-architecture-disposition-v0.1.md` §6.1)
**Created:** 2026-08-30 (Issue #9 integration)

## 1. Question

Should an explicit Core requirement for the human-facing system boundary — user goals/mental models, feedback and error recovery, accessibility (keyboard/assistive-technology awareness), consent/privacy interaction, human-facing failure — belong in the first shared traversal, and where is the one canonical first home?

Options:
- (A) M00-anchored spiral: boundary vocabulary at M00, browser-facing accessibility mechanics at M12, evidence hooks at P2/P9, judgment at M23/M24;
- (B) one bounded M12 module with the browser's visible interface;
- (C) project/journal rubric only (current state: P2/P9 evidence hooks, no Core admission);
- (D) CURRENT CASE only.

## 2. Why it matters

Accepting would change what "complete shared modern-system world model" means (Invariants 1 and 9), adding a human-facing dimension absent from the macro spine. Rejecting outright ignores a genuine gap for modern-system judgment: W3C's framing (live-verified 2026-08-30) treats accessibility as a system property that requires knowledgeable human evaluation — no tool alone determines it. Neither choice is a local placement decision, so it is not decided in a disposition table.

## 3. Stable capability at stake (conditional on admission)

- naming user goals and the failure/error-recovery interaction of a system boundary;
- basic keyboard/assistive-technology and perception/operation-awareness reasoning;
- consent/privacy interaction reasoning (explicit, bounded);
- one human-evaluation checkpoint (not tool-only evaluation).

Exclusions if admitted: visual/UX design, interaction history, usability-research methods, design systems, exhaustive WCAG, legal/compliance survey.

## 4. Evidence already gathered

- W3C *Introduction to Web Accessibility* (updated 2026-02-03): accessibility = perceive / understand / navigate / interact.
- W3C *Evaluating Web Accessibility*: tools assist, but knowledgeable human evaluation is required.
- Accepted interim: P2 denial/error/privacy interaction; P9 affected users, accessibility, consent, recovery "where relevant" (Mini Cloud App alignment, Issue #11) — evidence hooks only, no Core admission; #15 assigns no HCI/accessibility/consent IDs.

## 5. Trade-offs

Admission adds a first home and a checkpoint; non-admission risks the reported gap. A spiral avoids new modules but needs an explicit first home to satisfy Teach Once → Revisit Many (Invariant 11). Evidence hooks in the project exist without turning into canonical Core HCI content — that distinction must survive any decision.

## 6. Evidence required before decision

- one canonical first home consistent with the Module DAG (candidate homes use existing edges; no new H edge, no hidden prerequisite for M23/M24);
- one assessed human-facing evidence artifact (e.g., a bounded user-observable failure/error-recovery record);
- the exact list of exclusions (§3);
- bloat-control check.

## 7. Decision owner

Web Lead (architecture process) with reviewer roles per review policy; recorded via Decision Record if Core scope changes.

## 8. Integration status

**Not blocked for other Blueprint work.** Safe interim state retained: evidence hooks at P2/P9 remain without turning them into canonical Core HCI content; no concept ID assigned; no lesson or registry change until the RFC is decided. Security horizontal evidence (R8) does **not** resolve accessibility — this question remains its own.
