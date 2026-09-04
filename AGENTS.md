# AGENTS.md

## Project identity

Essential CS is a rigorous, self-study-first computer science curriculum for non-CS learners with basic programming experience. Its purpose is to build an accurate modern computing-system world model and independent technical judgment.

## Read before working

1. `meta/CURRICULUM_INVARIANTS.md`
2. `meta/PROJECT_STATUS.md`
3. `meta/DECISIONS.md`
4. `meta/OPEN_QUESTIONS.md`
5. Relevant blueprint, research dossier, concept registry entry, and the assigned GitHub Issue.

GitHub is the source of truth. Do not treat chat history or AI memory as project state.

## Instruction precedence

1. Curriculum Invariants
2. Root `AGENTS.md`
3. `meta/` policies
4. Directory-level instructions
5. Assigned GitHub Issue / explicit Work Claim
6. Agent-local judgment

Lower levels may refine but may not silently override higher levels.

## Working rules

- Accessible, not dumbed-down.
- Principle before product.
- Hands-on exists to create understanding.
- Prefer real mechanisms over fake simulations.
- AI is not a factual authority.
- Evidence and verification outrank fluent prose.
- Complexity must justify itself.
- Modern does not mean trendy.
- Teach once, revisit many times.
- Discover broadly, modify narrowly.
- Improve aggressively inside your task; escalate deliberately outside it.
- Do not make major curriculum decisions while writing a lesson.

## Default workflow

`Curriculum Map → Research Dossier → Module Blueprint → Lesson/Lab Design → Draft → Technical Verification → Learner Validation → Release → Maintenance`

Large-scale lesson writing must not begin until the relevant blueprint/research prerequisites are satisfied.

## Multi-agent work

Default: **One Issue → One Agent → One Branch/Worktree → One PR**.

The assigned GitHub Issue is the canonical task contract. It must contain the full scope, dependencies, allowed/forbidden changes, verification requirements, Completion Report, and stop/escalation conditions needed by the agent. Chat dispatch should be short and point the agent to the Issue; do not depend on a long chat prompt as project state.

### Issue → PR communication contract

- **Web Lead → Local Agent:** dispatch and material rework instructions live in the assigned Issue body. If Lead review changes the task contract, update/reopen the Issue or create the next bounded Issue; do not make comment history or chat history the only source of truth.
- **Local Agent → Web Lead:** implementation/design/research delivery lives in the assigned PR through its branch commits and current PR body / Completion Report.
- Routine acknowledgements, progress notes, repeated status updates, and back-and-forth task chat must **not** use GitHub Issue/PR comments when the same state belongs in the Issue body, PR body, commits, or review state.
- Comments remain available for exceptional durable review value that does not fit the canonical bodies, such as a focused inline finding, external contributor discussion, or audit record. They are not the default agent communication channel.
- Local Agents must not merge their own PRs.

Agents must not directly edit `main` unless explicitly authorized. Shared canonical concepts and curriculum architecture require coordination.

Local agents may identify visual needs, but the Web Lead owns final visual quality.

An author agent may not self-promote work to `VERIFIED`.

## Completion

Every formal local-agent task must report:
- deliverables;
- files changed;
- verification performed/not performed;
- assumptions;
- open questions;
- prompt deviations;
- out-of-scope necessary fixes;
- recommended review focus.
