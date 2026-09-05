# Decisions

This file records durable project decisions. It is not a transcript of the Requirements interview.

## D-001 — Project objective
Essential CS optimizes for an accurate modern computing-system world model and independent technical judgment, not degree compression, competitive programming, framework training, or maximal hand implementation.

## D-002 — Learner
Primary learner: adult/educated learner with basic programming ability (variables, loops, functions, can run simple Python/JS) and no formal CS background. High-school mathematics is assumed; additional theory is introduced just in time.

## D-003 — Organization
Visible narrative: real systems and system journeys. Hidden coverage backbone: traditional CS disciplines.

## D-004 — No global time ceiling
Earlier 80–120 hour ideas are void. Scope is constrained by educational value, not clock time. Core/Deep Dive separation remains strict.

## D-005 — Canonical teaching language
Chinese is canonical; important terms include English on first introduction. Concepts use stable IDs and one primary translation.

## D-006 — Main project
A simple multi-user Mini Cloud App evolves across the course. It integrates concepts without turning the course into web-development training. Final assessment is a System Defense.

## D-007 — Macro Core spine
The Map → Information → Computation → Machine → PL/Runtime/Compiler → OS → Storage → Network → Web/Browser → Database → Concurrency → Distributed Systems → Modern Infrastructure → Security Synthesis → Systems Thinking/Judgment → Final System Defense.

## D-008 — Tool/language baseline
Python is the main lab language; SQL and Shell are Core tools; minimal C/Assembly is used where it reveals lower layers. Linux is the canonical systems environment, with Dev Container/Codespace and WSL/macOS convenience paths.

## D-009 — Teaching loop
Default lesson loop: Question → Mental Model → Mechanism → Observe → Build → Break → Explain → Judge → Project, with misconceptions, temporary-ignore guidance, checkpoints, and exit criteria.

## D-010 — Spiral curriculum
Use Canonical Explanation + Contextual Revisit: teach definitions/core mechanisms once, revisit through application, connection, failure, trade-offs, and deeper contexts.

## D-011 — Research and evidence
AI may write and research but is never a factual authority. Important modules require Research Dossiers. Distinguish principle/specification/implementation/current practice and explicitly mark uncertainty.

## D-012 — Lab strategy
Prefer classic, proven, real mechanisms and high-quality university/textbook/open-source/official experiments. Apply Adopt → Adapt → Build. Avoid shallow AI-generated demos.

## D-013 — Living curriculum
Distinguish STABLE / CURRENT / FRONTIER. Review cadence depends on time sensitivity. Technology may transition ACTIVE → LEGACY → HISTORICAL → RETIRED.

## D-014 — Core horizontal threads
Correctness/invariants, failure, debugging, measurement, performance, security, concurrency, cost/resource economics, technical literacy, and privacy/data responsibility recur across the Core.

## D-015 — Modern technology cases
Use a Technology Evaluation Framework: Problem, Constraints, Mechanism, Gains, Costs, Failure Modes, Alternatives, When-not-to-use, Scale Threshold, Evidence, Evolution, Stable Principle.

## D-016 — Licensing
Original educational content/curriculum/original diagrams: CC BY-SA 4.0. Original code/tools/Mini Cloud App: Apache-2.0. Third-party provenance and attribution are mandatory.

## D-017 — Repository form
Markdown-first canonical educational source. `book/` teaches, `course/` guides, `labs/` builds intuition, `project/` integrates, `research/` stores dossiers, `meta/` stores curriculum engineering state/policies.

## D-018 — Multi-agent governance
Web Lead owns curriculum architecture, dispatch, final review, simple fixes, and final visual quality. Local agents work One Issue → One Agent → One Branch/Worktree → One PR with bounded autonomy and semantic coordination.

## D-019 — Review routing
Lead Review routes to Direct Fix / Complex Rework / Architecture Escalation. Visual work and simple reliable fixes are done directly by the Web Lead; major research/design failures are re-dispatched.

## D-020 — Session continuity
GitHub is persistent project memory. User decides when to switch Web Lead chats and asks for a handoff prompt. New chats recover state from GitHub. Local-agent chat context is not project-governed.

## D-021 — Prompt dispatch
Formal prompt templates live under `meta/prompts/`. The Web Lead generates current, self-contained Task/Rework Prompts from repository state. Actual prompts are not archived by default.

## D-022 — Blueprint before bulk lessons
Requirements are complete. Curriculum Blueprint v0.1 must establish architecture, maps, policies, review/release system, and external audit before large-scale lesson drafting.

## D-023 — Construction after Blueprint
After Blueprint, build stage-by-stage vertical slices: Research → Design → Lesson → Lab → Project → Verification → Learner Test.

## D-024 — v1.0 gate
v1.0 requires complete Core spine, complete Mini Cloud App, runnable REQUIRED labs, provenance/licensing, multi-role verification, learner validation, coverage audit, functioning maintenance, and no critical blockers.

## D-025 — External contributions
Humans, AI-assisted contributors, instructors, and institutions may contribute under the same Issue/PR/evidence/DoD quality gates.

## D-026 — Stable release repair
Serious released-content errors use an Errata/Hotfix process; stable tags are not rewritten. Revert and patch releases are allowed.

## D-027 — Build-first production; learner validation deferred
After the initial verified M00–M01 slice, course production proceeds in bounded batches through Research → Design → Lesson/Lab/Project implementation → independent Verification/Lead Review, then continues to the next ready batch. Real learner validation is non-blocking for continued authoring and may be completed later as the learner studies the course. D-024 remains unchanged: real learner validation is still required before v1.0 / `RELEASED`. AI simulation is never learner-validation evidence. This decision supersedes only the interpretation of D-023 that Learner Test must block the next authoring slice; it does not weaken technical, pedagogical, lab, integration, provenance, or visual review gates.

## D-028 — Issue-first Local Agent dispatch
For Local Agent work, the GitHub Issue is the canonical current Task/Rework Contract. Before dispatch, the Web Lead puts the full AI task there: dependencies, scope, allowed/forbidden changes, evidence/verification requirements, Completion Report, and stop/escalation rules. The user-facing/new-agent dispatch is intentionally short: identify the repository and Issue, tell the agent to claim/read/execute that Issue, work on its assigned branch/worktree, and submit a PR without merging. Long generated chat prompts are no longer the normal dispatch surface. Reusable templates under `meta/prompts/` remain scaffolding only. This supersedes D-021 only where D-021 implied that the current task contract should live primarily in a generated chat prompt.

## D-029 — Issue → PR handoff; no comment-stream workflow
Formal Local Agent communication uses a directional Issue/PR contract. The Web Lead dispatches the current task and any material rework through the canonical GitHub Issue body; the Local Agent delivers through the corresponding branch, commits, and PR body / Completion Report. Routine acknowledgements, progress chatter, repeated status updates, and rework back-and-forth must not turn GitHub Issue/PR comments into a chat stream when that information belongs in the Issue body, PR body, commits, or review state. Comments remain available for exceptional durable review value that does not fit those canonical surfaces. If Lead review materially changes the task contract, update/reopen the existing Issue or create the next bounded Issue before redispatch. Agents do not self-merge. This strengthens D-018 and D-028 without changing GitHub's role as source of truth.

## D-030 — Auditable Local Agent execution trace in PRs
Every formal Local Agent delivery must make its execution history reviewable from the PR itself. In addition to the normal Completion Report, the PR body must contain an Execution Trace / Work Log covering the starting branch/worktree state, material files/actions/commands, verification actually run and outcomes, meaningful problems encountered, their observed cause or bounded diagnosis, fixes/workarounds and verification, unresolved or not-run work, residual risks, and the ownership boundary between agent-authored changes and pre-existing user/local changes. Chat completion feedback is only a summary and cannot replace this PR record. The purpose is to let the Web Lead reconstruct what the agent actually did and maintain an accurate model of project state without relying on the agent's local session. The record must contain observable engineering facts and concise rationale, not fabricated activity or private chain-of-thought.
