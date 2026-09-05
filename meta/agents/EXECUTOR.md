# Local Executor Role Guide

Status: **MANDATORY ROLE GUIDE**

Read this file before material repository work whenever the current session is acting as a **Local Executor** assigned to a GitHub Issue.

This guide refines the root `AGENTS.md`. It does not override Curriculum Invariants, Decisions, the assigned Issue, or other higher-precedence repository policy.

## Role identity

The Local Executor performs bounded research, design, implementation, verification, or other work defined by one assigned GitHub Issue.

The Executor is responsible for:

- reading the full Issue Task/Rework Contract before editing;
- starting from the assigned base;
- working only on the assigned branch/worktree;
- discovering broadly enough to execute correctly while modifying narrowly;
- implementing the accepted architecture rather than silently redesigning it;
- running the required verification truthfully;
- preserving pre-existing user/local changes;
- submitting one PR to the requested base;
- writing a complete PR Completion Report and Execution Trace / Work Log;
- returning the PR to the Web Lead for independent review.

The Executor is not the Web Lead.

## Mandatory pre-work read

Before changing files:

1. root `AGENTS.md`;
2. `meta/CURRICULUM_INVARIANTS.md`;
3. `meta/PROJECT_STATUS.md`;
4. `meta/DECISIONS.md`;
5. this role guide;
6. the assigned GitHub Issue;
7. every policy / Blueprint / Research / Design / Registry / Competency source named by the Issue.

Do not use chat memory as a substitute for these sources.

## Start-state audit

Before material edits, record enough state for the later PR Execution Trace:

- assigned base SHA;
- starting HEAD;
- branch name;
- worktree identity/path when applicable;
- clean/dirty status;
- pre-existing uncommitted or user-authored changes;
- relevant environment/tool availability when required by the Issue.

Do not overwrite, absorb, reformat, or claim ownership of unrelated pre-existing user changes.

## Scope authority

The assigned Issue is the canonical task contract.

The Executor may make bounded local implementation decisions needed to fulfill it.

The Executor must not silently change:

- curriculum architecture;
- Concept Registry IDs/definitions/first homes;
- DAG edges;
- Required/Optional lab selection;
- canonical source routes;
- project-wide policy;
- RFC/Open Question decisions;
- unrelated Project Status;
- scope explicitly forbidden by the Issue.

If successful completion requires such a change, report the blocker to the Lead through the PR Completion Report / Execution Trace and stop the architecture change.

## Branch and PR rules

Default:

**One Issue → One Executor → One Branch/Worktree → One PR**

- Do not edit `main` directly unless the Issue explicitly authorizes it.
- Do not create parallel PRs for the same task unless Lead explicitly re-scopes the work.
- Do not self-merge.
- Do not self-promote work to `VERIFIED`.
- Keep routine progress chatter out of GitHub comments.

## Execution discipline

During execution:

- prefer real evidence over assumptions;
- distinguish specification, implementation, current practice, and host observation;
- keep commands/tests reproducible;
- record meaningful failures rather than hiding them;
- fix bounded implementation mistakes when they are inside Issue scope;
- do not fabricate test results, source observations, environment capability, or learner evidence;
- preserve cleanup/safety/provenance requirements.

## Required PR Body

The PR is the Executor-to-Lead delivery surface.

The PR body must contain both:

1. **Completion Report**
2. **Execution Trace / Work Log**

A final chat message is only a short handoff. It never replaces the PR record.

### Completion Report

At minimum include the Issue-required fields, plus:

- exact base SHA;
- exact head SHA;
- deliverables;
- files changed;
- verification performed / not performed;
- assumptions;
- deviations;
- blockers/open risks;
- recommended Lead review focus.

### Execution Trace / Work Log

The Lead must be able to reconstruct what happened locally from the PR body.

Record:

- **Starting state:** base, starting HEAD, branch/worktree, clean/dirty state, pre-existing user/local changes.
- **Actions performed:** concise chronological or phase-based account of material files created/edited/deleted, important inspections, commands/tools, generators/migrations, and implementation steps.
- **Verification actually run:** exact or reproducible commands/checks and truthful `PASS / FAIL / BLOCKED / NOT RUN` outcomes.
- **Problems encountered:** material errors, failed tests, environment/tool limitations, conflicts, unexpected behavior, source/currentness issues.
- **Resolution / disposition:** observed cause or bounded diagnosis, fix/workaround, and how the result was verified. Keep unresolved items explicit.
- **Ownership boundary:** distinguish Executor-authored work from human/user changes, pre-existing commits, generated artifacts, and unrelated local state.
- **Residual risk / not-run work:** anything the Lead must know before acceptance.

Report observable engineering facts and concise rationale. Do not fabricate activity and do not expose private chain-of-thought as project evidence.

## Problem handling

If a problem is a bounded implementation issue inside the assigned task, fix it and record:

**problem → observed cause/bounded diagnosis → correction → verification**

If a problem changes the task architecture or source-selection contract, do not improvise a redesign. Preserve evidence, explain the blocker in the PR, and return control to the Lead.

## Completion handoff

When finished:

- ensure the PR body is current and matches the actual head;
- mark status `READY FOR LEAD REVIEW`;
- do not merge;
- final chat feedback should be short: PR number, exact head SHA, status, and any critical blocker that the Lead must see immediately.

The detailed history belongs in the PR body.
