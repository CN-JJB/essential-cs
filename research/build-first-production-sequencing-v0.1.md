# Build-First Production Sequencing — Internal Evidence Review v0.1

**Issue:** #36  
**Question:** Must learner validation block the next learner-facing slice, or can course authoring continue after independent verification while learner validation is deferred to the release gate?

## Evidence reviewed

- D-022 requires Blueprint before bulk lesson drafting.
- D-023 originally states a stage-by-stage sequence ending in Learner Test.
- D-024 separately requires learner validation for v1.0.
- Definition of Done defines `VERIFIED` through independent multi-role review; it does not require learner validation for every draft before additional authoring can begin.
- Issue #29 / PR #30 showed that Lead review can find and repair learner-facing defects before merge.
- Issue #31 / PR #33 independently reproduced the M00–M01 technical contract and produced a real-pilot observation template.
- Issue #34 demonstrated a practical dependency: real learner validation requires an actual learner and cannot be completed by an AI-only production pipeline.
- The project owner has explicitly selected a build-first workflow: complete the full course first, then study it gradually and provide learner feedback later.

## Options

### A. Per-slice learner validation blocks further authoring

Benefit: shortest pedagogical feedback loop.

Cost: the entire production pipeline becomes dependent on synchronous access to a real learner. This prevents the stated build-first objective even when Research, Design, implementation, and independent Verification are ready.

### B. Build-first after independent verification; learner validation deferred

Benefit: allows continuous authoring while preserving factual, technical, integration, lab, and visual quality gates.

Risk: pedagogical problems may accumulate across more material before real learner evidence arrives.

Mitigation:
- keep bounded module/slice implementation rather than one uncontrolled bulk PR;
- retain independent Lead/multi-role review and reproducibility checks;
- keep learner-validation artifacts truthful and open rather than simulated;
- treat learner validation as mandatory before v1.0 / RELEASED status;
- when later learner evidence finds defects, route SIMPLE FIX / COMPLEX REWORK / ARCHITECTURE normally.

## Finding

Option B best matches the owner's explicit production objective without weakening the truthfulness of learner-validation evidence.

The important distinction is:

**authoring progression** may continue after independent verification;  
**release readiness** still requires real learner validation.

This changes production sequencing, not curriculum scope, Module DAG, concept homes, competencies, Lab selection, or technical claims.

## Recommendation

Adopt build-first production. Supersede the blocking interpretation of D-023 while preserving D-024.

Issue #34 remains OPEN but DEFERRED / NON-BLOCKING until real learning begins.
