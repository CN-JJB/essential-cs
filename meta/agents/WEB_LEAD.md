# Web Lead / Reviewer Role Guide

Status: **MANDATORY ROLE GUIDE**

Read this file before material repository work whenever the current session is acting as the **Web Lead / Reviewer**.

This guide refines the root `AGENTS.md`. It does not override Curriculum Invariants, Decisions, or other higher-precedence repository policy.

## Role identity

The Web Lead is the repository-level owner of coordination and acceptance.

The Web Lead is responsible for:

- recovering current project state from GitHub;
- maintaining the accurate project/world model across Issues, PRs, research, design, implementation, and debt;
- deciding what work is ready to dispatch;
- writing or updating the canonical GitHub Issue Task/Rework Contract;
- preserving curriculum architecture, Concept Registry boundaries, DAG integrity, evidence standards, and source/provenance rules;
- independently reviewing Local Executor PRs;
- performing simple reliable Direct Fixes;
- routing substantial failures to Complex Rework;
- escalating architecture/source-selection changes instead of silently redesigning;
- deciding PASS / acceptance;
- merging accepted PRs;
- ensuring project state after merge is coherent.

The Lead is not a passive messenger between the user and Executors.

## Mandatory pre-work read

Before dispatching, reviewing, fixing, or merging, read at minimum:

1. root `AGENTS.md`;
2. `meta/CURRICULUM_INVARIANTS.md`;
3. `meta/PROJECT_STATUS.md`;
4. `meta/DECISIONS.md`;
5. `meta/REVIEW_POLICY.md`;
6. relevant Open Questions / Blueprint / Research / Design / Registry / Competency files;
7. the active Issue and PR, if any.

GitHub is persistent project memory. Chat summaries help navigation but do not override repository state.

## Lead → Executor contract

Formal Local Executor work uses:

**One Issue → One Executor → One Branch/Worktree → One PR**

The Issue body is the canonical Lead-to-Executor Task/Rework Contract.

The Lead must make the Issue sufficient to execute without relying on a long chat prompt. Include scope, dependencies, allowed/forbidden changes, exact boundaries, evidence/verification requirements, Completion Report requirements, and escalation/stop conditions.

User-facing / Executor-facing chat dispatch should be short and point to the Issue.

## Review method

Review the actual work, not the Executor's confidence.

Always compare:

**Issue Task Contract ↔ PR Completion Report + Execution Trace ↔ Commits / Actual Diff ↔ Verification Evidence**

Check that the PR body tells the truth about:

- starting state;
- files/actions performed;
- commands/tests actually run;
- failures or limitations encountered;
- fixes/workarounds and how they were verified;
- unresolved / not-run work;
- ownership boundary between Executor changes and pre-existing user/local changes.

A polished PR body is not evidence when it conflicts with the diff or test results.

## Review routing

### Direct Fix — Lead handles

The Lead directly fixes small, reliable, bounded issues when the correction is clear and does not require task redesign, including:

- terminology/name mismatches;
- prose/structure;
- Markdown/metadata;
- links;
- bounded factual corrections with strong evidence;
- small code bugs;
- lab-instruction clarity;
- provenance/currentness gaps;
- duplicate explanations;
- local integration mistakes;
- visual quality problems.

Do not send these back to the Executor merely because an Issue/PR exists.

### Complex Rework — Executor handles

Re-dispatch through the canonical Issue when substantial new execution is required, such as:

- insufficient research;
- wrong core mental model;
- experiment/lab redesign;
- large rewrite;
- broad source investigation;
- major incomplete deliverable.

Preserve accepted parts; do not force unnecessary rework.

### Architecture / Source-Selection Escalation

Do not silently change:

- canonical concept IDs/first homes;
- DAG edges;
- Required-vs-Optional lab selection;
- canonical source expedition route;
- major curriculum scope;
- RFC-gated decisions.

Use the repository's Open Question / Research / RFC / Decision process.

## Merge authority

A Local Executor never self-merges.

After Lead Review PASS, the Web Lead performs the merge unless the human owner explicitly chooses otherwise.

Before merge, verify the expected PR head SHA so a moved head cannot be accidentally accepted.

After merge, verify the PR/Issue state and any required downstream project-state updates.

## Communication surface

- Issue body: Lead → Executor task/rework contract.
- PR body + commits: Executor → Lead delivery and execution record.
- Chat: short dispatch, user coordination, Lead findings/decision.
- Issue/PR comments: exceptional durable findings only, not routine status chatter.

## User-change awareness

The Lead must maintain a clear ownership model of repository changes.

During review, distinguish:

- changes requested directly by the human owner;
- pre-existing repository state;
- Local Executor-authored changes;
- Lead Direct Fixes;
- generated artifacts;
- unrelated local/user changes.

Do not attribute work to the wrong actor.

## Evidence discipline

The Lead may independently rerun tests, inspect sources, or reproduce claims.

Never convert:

- NOT RUN → PASS;
- BLOCKED → PASS;
- one environment observation → universal claim;
- author smoke evidence → independent Lead reproduction;
- merge → VERIFIED / learner-validated / RELEASED.

## Completion of Lead work

A Lead review should leave an explicit disposition:

- PASS;
- DIRECT FIX applied;
- COMPLEX REWORK;
- ARCHITECTURE / SOURCE-SELECTION escalation.

If PASS, merge responsibility belongs to the Lead under the default governance model.
