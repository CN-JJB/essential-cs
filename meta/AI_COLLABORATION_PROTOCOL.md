# AI Collaboration Protocol

## Roles

### Web Lead

The Web Lead is the Curriculum Architect, Task Dispatcher, Lead Reviewer, Visual Editor, and Final Quality Gate.

It owns:

- curriculum architecture and invariants;
- Core/Deep Dive boundaries;
- task decomposition and dependency coordination;
- final review;
- direct simple fixes;
- final visual quality;
- RFC/Decision escalation.

The Web Lead persists state through GitHub, not through assumed permanent chat memory.

### Local Agents

Local agents may perform research, writing, lab implementation, verification, maintenance, or independent review depending on capability.

Maintain a lightweight Agent Capability Registry when multiple local agents are used.

## Work unit

Default:

**One Issue → One Agent → One Branch/Worktree → One PR**

Local agents do not directly modify `main` unless explicitly authorized.

## Bounded autonomy

**Improve aggressively inside your task; escalate deliberately outside it.**

- Within task scope: make high-quality local decisions.
- Important cross-Lesson/Module changes: propose first.
- Curriculum architecture/Invariants/Core boundary/licensing/release-gate/canonical-environment changes: require RFC/Decision.

## Semantic coordination

Git conflicts are not enough. Use lightweight Work Claims for:

- files;
- canonical concepts;
- module/project areas.

Shared canonical concepts and architecture may require exclusive/coordinated ownership.

## Scope discipline

**Discover broadly, modify narrowly.**

Out-of-scope discoveries belong in the Completion Report / Issue. Only minimal necessary out-of-scope fixes that block correctness of the assigned task may be included, and they must be declared.

## Stale branches

If a branch is substantially stale or conflicts semantically with new `main`, do not force an agent to guess through extensive conflicts. The Web Lead may abandon it and issue a new Rework Prompt against current `main`, preserving only still-valid work.

## Visual work

Local agents may mark visual needs or propose simple diagrams. The Web Lead owns final visual design and should directly generate/revise visuals during review.

## Completion Report

Every formal Local Agent task reports:

- task/status;
- deliverables;
- changed files;
- verification run/not run;
- assumptions;
- open questions;
- prompt deviations;
- out-of-scope necessary fixes;
- recommended review focus.
