# RFC-003 — Build-First Course Production; Learner Validation Deferred to Release Gate

**Issue:** #36  
**Status:** ACCEPTED by project-owner direction, pending repository integration

## Context

D-023 described post-Blueprint construction as:

`Research → Design → Lesson → Lab → Project → Verification → Learner Test`

The initial M00–M01 slice reached independent Verification successfully, but the next step required a real learner. The project owner has now explicitly chosen to finish the entire course first and study it gradually afterward.

Requiring a real learner before every subsequent learner-facing slice would make human availability a production dependency unrelated to whether the next content has adequate Research, Design, implementation, and independent review.

## Decision

Adopt a **build-first, bounded-batch production sequence**:

`Research → Design → Lesson/Lab/Project Implementation → Independent Verification/Lead Review → Next bounded batch`

Learner Validation is **deferred and non-blocking for continued authoring**.

Before v1.0 / `RELEASED`, the project must still perform real learner validation and disposition material findings. D-024 remains unchanged.

## Consequences

- Issue #34 remains truthful and open, but is DEFERRED / NON-BLOCKING.
- No AI simulation may be recorded as learner evidence.
- Subsequent course content may be authored without waiting for #34.
- Each implementation batch still requires the existing technical, pedagogical, lab/reproducibility, curriculum-integration, provenance, and visual review gates.
- `merge ≠ learner validation`.
- Learner validation remains a release-quality gate and can trigger later repair/rework/architecture escalation.
- This RFC does not alter Core scope, Module DAG, competencies, concepts, Mini Cloud App architecture, or existing Open Questions.

## Risks and mitigations

The main risk is delayed discovery of pedagogy/usability problems. Mitigate it through bounded batches, independent review, consistent lesson structure, progressive support, technical verification, and later real learner evidence before release.

## Supersession

This RFC does not erase D-023. A new durable Decision clarifies that D-023's Learner Test is no longer a mandatory stop between authoring slices; D-024 remains the binding v1.0 learner-validation requirement.
