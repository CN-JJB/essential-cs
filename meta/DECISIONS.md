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

## D-031 — Mandatory role-specific agent guides
All repository AI work enters through the root `AGENTS.md`, then must identify the active role before material work. Web Lead / Reviewer sessions must read `meta/agents/WEB_LEAD.md`; Local Executor sessions must read `meta/agents/EXECUTOR.md`. The roles are intentionally separated: the Web Lead owns task contracts, architecture stewardship, review routing, Direct Fixes, acceptance, and merge; the Local Executor owns bounded execution of its assigned Issue, branch/worktree changes, verification, and PR delivery with an auditable Completion Report / Execution Trace, and never self-merges or silently assumes Lead authority. Shared policies still apply to both roles.

## D-032 — First stable environment implementation strategy
The first stable canonical environment will use a **digest-addressed Ubuntu 24.04 LTS (Noble)-based learner/test environment artifact**. Standard GitHub-hosted `ubuntu-24.04` runners may execute that environment, but their moving runner images are infrastructure substrate, not the canonical immutable pin.

Compatibility policy for the first stable environment uses bounded floors rather than universal patch-level locks where exactness is not pedagogically or operationally justified: Python >= 3.12, SQLite engine + `sqlite3` CLI >= 3.45, GCC >= 13 with the required C11 surface, curl >= 8.5, and GDB >= 15.0. **GDB is required** for canonical M03 evidence; a convenience host without GDB may be PARTIAL/BLOCKED but cannot stand in for the stable canonical environment. strace, browser/Chromium, live observability backends, PostgreSQL/psql, Docker/Podman, and arm64 remain capability-gated or optional where the accepted curriculum already treats them that way.

LAB-REQ-02 keeps stricter lane-scoped identity: the xv6 source pin remains exact, and the canonical environment must record the full resolved QEMU/RISC-V distro package identities represented by the validated QEMU 8.2.2 / riscv64-unknown-elf-gcc 13.2.0 candidate. Bare upstream version strings are not sufficient apt locks; refresh requires a real QEMU smoke on the replacement environment.

This Decision selects the **implementation strategy**, not the final realized pin. OQ-BP-006 remains OPEN until the implementation task commits the canonical environment definition, immutable digest, resolved package identities, CI execution matrix, and exact-head runtime evidence sufficient for Web Lead acceptance. No v1.0 / VERIFIED / RELEASED claim follows from this Decision.

**Provenance:** Issue #143 / PR #144; Lead-reviewed final research head `35175095c1a62cb6968221d54d2d3564f4d6f259`; PR #144 merge `07d5550bc7bed1ac9126351688bab7ce70d1357b`.

## D-033 — v1.0 bounded AI-literacy scope
For the first stable v1.0 curriculum, Essential CS will **not** expand the accepted M00–M24 Core spine with an AI/ML/LLM module or new canonical Core thread. The already accepted bounded practice remains: AI-generated code, documentation, configuration, and claims are treated as untrusted hypotheses that require source, test, measurement, and security verification. This is a CURRENT CASE / technical-literacy practice, not a new Core theory obligation.

This decision resolves OQ-BP-001 for v1.0. It does not claim AI literacy is unimportant, and it does not prevent a future post-v1.0 RFC from reopening the question if learner evidence, external audit evidence, or durable systems-practice evidence justifies expansion.

**Provenance:** `meta/rfcs/RFC-CAND-001-bounded-ai-literacy.md`; Issue #155.

## D-034 — v1.0 human-facing-system-boundary scope
For the first stable v1.0 curriculum, Essential CS will **not** add a new canonical HCI/accessibility Core first home or module. The accepted boundary remains the existing system-facing evidence hooks: user-observable denial/error/recovery behavior, privacy/consent interaction, affected-user reasoning, and accessibility consideration where relevant in Mini Cloud P2/P9 and existing browser/security contexts.

This decision resolves OQ-BP-003 for v1.0 while preserving the project's systems focus and avoiding a late new Core concept family and assessment surface. A future post-v1.0 RFC may reopen the question if real learner or external-audit evidence shows the bounded hooks are insufficient.

**Provenance:** `meta/rfcs/RFC-CAND-002-human-facing-boundary.md`; Issue #155.
