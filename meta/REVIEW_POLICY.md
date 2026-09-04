# Review Policy

## Principle

**Review the claim, not the prose.**

Fluent writing is not evidence of correctness.

## Status gate

An author agent cannot self-promote its own work to `VERIFIED`.

Review before VERIFIED considers at least:

1. technical accuracy;
2. pedagogy / mental model quality;
3. lab quality and reproducibility;
4. curriculum/integration consistency.

Human and AI contributions use the same evidence/quality standards.

## Lead review routing

### Direct Fix

The Web Lead should directly repair simple, reliable issues such as:

- terminology consistency;
- prose/structure clarity;
- Markdown/metadata;
- links;
- small factual corrections with strong evidence;
- small code bugs;
- lab instruction clarity;
- provenance gaps;
- duplicate explanations;
- local integration issues.

### Visual

Final visual quality is owned by the Web Lead. Missing, misleading, inconsistent, or weak diagrams should normally be created/revised directly during review.

### Complex Rework

Return/re-dispatch when the task itself is substantially incomplete, e.g.:

- insufficient research;
- classic lab research skipped;
- wrong core mental model;
- experiment needs redesign;
- large rewrite/source investigation required.

A Rework Prompt should distinguish accepted parts, blockers, evidence, required rework, parts not to redo, and new deliverables.

### Architecture Escalation

If review reveals a curriculum/architecture problem, do not silently redesign inside the PR.

Use:

`Open Question → Research → RFC if needed → Decision → New Task`

## Review communication surface

Lead Review must preserve the Issue → PR handoff model:

- the assigned Issue body is the Lead-to-Agent Task/Rework Contract;
- the PR body plus branch commits are the Agent-to-Lead delivery surface;
- when review requires material rework, update/reopen the Issue or create a bounded follow-up Issue before redispatch;
- do not use Issue/PR comments for routine acknowledgements, progress chatter, repeated status reports, or task-contract revisions that belong in the canonical Issue/PR bodies;
- comments are reserved for focused durable findings, external contributor discussion, or exceptional audit context that does not fit the canonical bodies;
- the authoring Agent does not merge its own PR.

## Completion comparison

Review Local Agent work against:

**Task Contract ↔ Completion Report ↔ Actual Diff**

Do not accept “done” or passing prose at face value.

## Released-content errors

Serious technical/pedagogical errors use the Errata & Hotfix policy and require checking downstream contextual revisits of the affected canonical concept.
