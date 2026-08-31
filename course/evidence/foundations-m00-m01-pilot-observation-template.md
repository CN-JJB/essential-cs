# Foundations M00–M01 First-Pilot Observation Template

> Human-observer template for the first M00–M01 pilot. This sheet prepares learner validation; a blank template is **not** learner-validation evidence. Record only what was actually observed. Do not invent learner identities, quotations, timings, outcomes, success rates, or transfer results.

## 1. Session / activity reference

- Observation/session reference:
- Date:
- Module:
- Lesson:
- Activity point / command / checkpoint:
- Observer:
- Repository commit / working-tree context:

## 2. Environment / preflight

- OS / environment:
- CPU architecture:
- Python version:
- Git version:
- Relevant shell/runtime:
- Preflight result: `PASS / BLOCKED / PARTIAL`
- If not PASS, exact blocking behavior:
- Environment reference/evidence:

**Did tooling/environment behave as the activity specification expected?**

- [ ] Yes
- [ ] Partly
- [ ] No
- Evidence / note:

> Environment/preflight problems are observational context. Do not score them as learner competency failures.

## 3. Task attempt and support

- Task / question attempted:
- Learner action attempted:
- Outcome before support:

**Highest support level used — choose exactly one:**

- [ ] Independent
- [ ] Hint 1
- [ ] Hint 2
- [ ] Expected Observation
- [ ] Full Explanation

If `Full Explanation` was used, treat this attempt as remediation evidence. Use a short new-context transfer check before making an independent-competence claim.

## 4. Prediction before reveal / run

- Learner prediction, recorded before reveal/run:
- What would have falsified that prediction?
- Prediction quality note: `clear / partial / absent / not applicable`
- Observer evidence for that note:

## 5. Evidence actually produced

Record the smallest reproducible evidence that matters.

- Command / action:
- Output / diff / bytes / diagram / explanation actually produced:
- Was the evidence consistent with the activity specification? `yes / partly / no`
- What the evidence supports:
- What the evidence does **not** establish:

## 6. Misconception / error category

Choose or describe the best-fitting observed category; do not infer one without evidence.

- [ ] Observation treated as explanation
- [ ] Information / representation conflation
- [ ] Code point / UTF-8 byte / visible-character conflation
- [ ] Byte-order interpretation error
- [ ] Two's-complement representation overgeneralized to arithmetic semantics
- [ ] Round-trip overclaim
- [ ] Later retrieval overclaimed as durability
- [ ] Incidental shell/Git/debugger syntax/tool discovery
- [ ] Environment/preflight/tooling failure
- [ ] Other:
- [ ] No misconception/error observed at this point

Evidence / exact behavior:

## 7. Mechanism explanation after observation

After the observation, could the learner explain the intended mechanism within the Lesson's stated boundary?

- [ ] Yes, independently
- [ ] Yes, with bounded support
- [ ] Partly
- [ ] No
- [ ] Not checked

What explanation was demonstrated:

What claim boundary or uncertainty did the learner preserve:

## 8. Short transfer check

Use a small new-context check, especially after `Full Explanation`.

- Transfer prompt/context:
- Result: `succeeded / partly succeeded / did not succeed / not run`
- Highest support used on transfer:
- Evidence produced:
- Observer note:

Do not convert one successful transfer item into a broad validation claim.

## 9. Time/context note

Record only enough timing context to distinguish tooling friction from reasoning friction.

- Approx. time lost to tooling/environment:
- Approx. time spent on conceptual reasoning:
- Main source of delay:
- Context note:

> These times are observational context only. They are not a grade, completion target, or success metric.

## 10. Observer routing judgment

Choose the best current routing **candidate**, not a final design verdict.

- [ ] No routing candidate yet
- [ ] **Design candidate**
- [ ] **Environment candidate**
- [ ] **Support candidate**

Reason/evidence:

Confidence:

- [ ] Low
- [ ] Medium
- [ ] High

Has the same signal repeated across learners or sessions?

- [ ] Yes
- [ ] No
- [ ] Unknown / insufficient observations

Related observation/session references, if any:

## 11. Routing contract

### Design revision signal

Use a **Design candidate** when the environment works and reasonable support exists, but **repeated** learners/sessions still form the wrong mental model, systematically conflate claim layers, or overclaim what evidence proves.

Examples in this slice include repeated inability to distinguish observation from explanation, repeated information/representation conflation, repeated durability overclaim despite the explicit boundary, or a visual that repeatedly induces the wrong model.

Do **not** turn one anecdote into a design verdict. Do not try to repair a repeated mechanism-level failure merely by adding more commands or hints.

### Environment / preflight repair signal

Use an **Environment candidate** when tooling, version, hosted policy, reset behavior, repository access, or the observation surface blocks the intended conceptual work.

Examples include preflight/version mismatch, a debugger path that does not stop/inspect as specified, unwritable reset/evidence paths, or a supposedly deterministic activity that cannot reproduce its baseline.

These are not learner competency failures and do not raise prerequisites.

### Hint / support improvement signal

Use a **Support candidate** when the concept/mechanism is sound but learners repeatedly stall on incidental syntax, vocabulary orientation, or tool discovery and then reason correctly once bounded support is provided.

Support changes must preserve:

`Question → Hint 1 → Hint 2 → Expected Observation → Full Explanation`

and must not reveal the assessed conclusion before the learner has made a prediction.

## 12. End-of-observation note

- Strongest evidence from this observation:
- Main uncertainty still open:
- Recommended next observation/check:
- Any privacy/sensitivity concern in the note:
- Observer sign-off / reference:

> A single observation is evidence, not a design verdict. Review repeated patterns, common-mode environment failures, and support-sensitive versus support-insensitive misconceptions before routing curriculum changes.
