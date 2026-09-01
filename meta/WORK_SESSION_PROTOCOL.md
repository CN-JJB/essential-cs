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

The Web Lead first creates or updates a GitHub Issue so the **Issue body is the complete current task contract**. It must contain the dependencies, scope, assigned branch/worktree, allowed/forbidden changes, evidence and verification requirements, Completion Report, and stop/escalation conditions.

After the Issue is ready, chat dispatch is deliberately short. Normal form:

`认领 CN-JJB/essential-cs Issue #N，完整阅读并按 Issue 执行；使用 Issue 指定分支，完成后提交 PR，禁止自行 merge。`

Do not send a second long prompt that can drift from the Issue. If rework is needed, update the Issue or create an explicit Rework Issue first, then send another short dispatch.

Local-agent internal context compression is outside project governance. A fresh local conversation recovers its task from GitHub Issue state.

## State principle

**Conversation is a work session. GitHub is project memory.**
