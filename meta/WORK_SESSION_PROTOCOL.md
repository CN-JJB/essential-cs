# Work Session Protocol

## Web Lead

The Web Lead is the persistent curriculum coordinator, but its chat context is not persistent project memory.

At session start:

1. read root `AGENTS.md`;
2. read `meta/PROJECT_STATUS.md`;
3. read relevant Decisions/Invariants/Open Questions;
4. inspect relevant Blueprint/Research/Concept artifacts;
5. inspect active Issues/PRs for the task;
6. read the latest Web Lead handoff if one exists;
7. determine current phase and highest-priority valid work.

At session end after substantive changes:

- update repository status;
- persist important Decisions/Open Questions;
- update relevant Issues/PRs;
- record verification state;
- write/update a Web Lead handoff when the user asks to switch chats.

## Chat switching

The **user decides when the Web Lead chat is long enough** and asks for a handoff prompt.

The Web Lead should then:

1. make sure important state has been persisted;
2. write a concise repository handoff;
3. generate a directly copyable Web Lead Bootstrap Prompt.

The Bootstrap Prompt is navigation, not authority. The new session must re-read GitHub.

## Local Agent dispatch

The Web Lead generates one or more Task Prompts from current repository state.

Prompts must state dependencies and whether tasks may run in parallel.

Local-agent internal context compression is outside project governance. If a fresh local conversation is needed, generate a new Prompt from current GitHub state.

## State principle

**Conversation is a work session. GitHub is project memory.**
