# RFC Candidate — Human-Facing System Boundary (OQ-BP-003)

**Status:** RESOLVED FOR v1.0 BY D-034 — historical candidate retained for provenance.

**Open Question:** `meta/OPEN_QUESTIONS.md` — OQ-BP-003 (CLOSED for v1.0)
**Source of the question:** External Curriculum Audit R3 (`external-curriculum-audit-v0.1.md` §5.3) + accepted disposition (`audit-to-architecture-disposition-v0.1.md` §6.1)
**Created:** 2026-08-30 (Issue #9 integration)
**Resolved:** 2026-09-12 (Issue #155; D-034)

## Resolution

For the first stable v1.0 curriculum, do **not** add a new canonical HCI/accessibility Core first home or module. Retain the already accepted human-facing evidence hooks in Mini Cloud P2/P9 and relevant browser/security/privacy contexts: observable denial/error behavior, recovery, consent/privacy interaction, affected-user reasoning, and accessibility consideration where relevant.

The question may be reopened post-v1.0 if real learner evidence or final external-audit evidence shows these bounded hooks are insufficient.

## 1. Original question

Should an explicit Core requirement for the human-facing system boundary — user goals/mental models, feedback and error recovery, accessibility, consent/privacy interaction, human-facing failure — belong in the first shared traversal, and where is the canonical first home?

Original options included an M00 spiral, M12 home, project/journal rubric only, or CURRENT CASE only.

## 2. Why it mattered

Accepting a new Core first home would change the shared world model and assessment surface. Rejecting all treatment would ignore a legitimate systems boundary. The accepted project hooks provide a middle path without turning Essential CS into an HCI course.

## 3. Stable capability considered

- naming user goals and user-observable failure/recovery behavior;
- basic accessibility awareness where system behavior makes it relevant;
- bounded consent/privacy interaction reasoning;
- affected-user reasoning in system defense.

Explicit exclusions considered: visual/UX design, interaction history, usability-research methods, design systems, exhaustive WCAG, legal/compliance survey.

## 4. Evidence considered

- W3C accessibility framing and human-evaluation requirement;
- accepted P2 denial/error/privacy interaction hooks;
- accepted P9 affected-user/accessibility/consent/recovery hooks;
- existing browser/security/privacy contexts;
- absence of a need to create a hidden prerequisite or late new concept family for M23/M24.

## 5. Trade-off disposition

The bounded evidence hooks expose the human-facing system boundary sufficiently for the first stable systems curriculum while keeping Core scope coherent. D-034 therefore closes the escalation for v1.0 without claiming the topic is permanently out of scope.
