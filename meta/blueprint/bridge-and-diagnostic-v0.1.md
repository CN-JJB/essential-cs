# Essential CS Bridge and Diagnostic v0.1

Status: **Blueprint v0.1 — LEAD-REVIEWED DRAFT**
Purpose: 为已经具备基础编程能力、但实践技术流畅度不均衡的学习者提供可跳过的入口诊断（diagnostic）与定向补桥（Bridge）。它**不是**隐藏 Stage、先修 Module、Programming 101，也不改变 Core DAG。

## Bridge principle

Bridge 只回答一个入口问题：

> **学习者是否已经能可靠地进入 M00 / L00-02，并使用 Essential CS 的环境、运行、调试与 evidence workflow？**

已经具备这些能力的学习者可以**直接跳过 Bridge，甚至无需执行 diagnostic**。Bridge 的职责仅是修补“运行、阅读、调试、复现、保存证据”的入口缺口，不提前教授 Core 系统概念。

Bridge 的设计原则：

- **skippable**：自评已有能力即可进入 M00；
- **diagnostic, not ranking**：判断可否可靠完成任务，不做速度或命令记忆排名；
- **targeted remediation**：只补实际薄弱项；
- **evidence-oriented**：从入口开始建立 baseline / diff / output / environment record 习惯；
- **no prerequisite creep**：真实学习者卡住时，先改进 Bridge、环境或说明，不轻易提高入学要求。

## Relationship to Core and the DAG

- Bridge **位于 Core Module DAG 之外**。
- Bridge **不创建 H edge**，不改变任何 Stage/Module 顺序。
- M00 L00-02 仍是 technical-investigation workflow、shell/task execution、code/file reading、debugger-light investigation、Git evidence、reproducibility/environment record 的 **canonical first Core home**。
- REQUIRED Labs 的 repository → preflight → baseline → evidence record 仍是 course-discipline entry gate，不是 DAG prerequisite。
- Bridge 只修补进入该 workflow 所需的 practical fluency；它不能抢先成为 M00 的第二套 canonical explanation。
- 具体稳定版本由 **OQ-BP-006** 在实现阶段统一 pin；本文只定义能力与 preflight interface，不固定版本号。

## Diagnostic format

建议使用一个课程提供的小型 repository / fixture，在 canonical one-click environment 中完成 **7 个紧凑任务**。允许查询普通命令帮助；不考 shell trivia、IDE shortcuts、平台熟练度或复杂 Git workflow。

每个任务都要求最少 evidence，而不是只看“最后成功没有”。

### Task 1 — Files and paths

学习者需要：

- 在给定目录结构中找到目标文件；
- 区分 relative path 与 absolute path；
- 查看并做一次小编辑；
- 指出程序输入来自哪里、输出/生成文件写到哪里。

**Evidence:** 使用的路径、一次小 diff、对 input/output location 的一句说明。

**Do not test:** mount、复杂 permissions、symlink trivia、文件系统管理。

### Task 2 — Terminal / shell survival

学习者需要：

- 运行一个提供的命令和一个提供的脚本；
- 在有明确价值时使用一次简单 pipe 或 redirect；
- 查看并解释 success/failure exit status；
- 从输出中指出一个合理的下一步动作。

**Evidence:** command transcript + exit status + 一句解释。

**Do not test:** shell scripting、复杂 quoting、正则技巧、命令百科。

### Task 3 — Small Python program

给定一个仅使用目标学习者已应具备基础概念的短 Python 程序，学习者需要：

- 运行 baseline；
- 做一个受控小改动；
- 解释 output/error 的变化；
- 恢复或保留一个明确 working state。

**Evidence:** baseline output、单一 diff、changed output/error、working-state record。

**Boundary:** Bridge 不教授变量、循环、函数等 Programming 101 内容；若这些基础本身缺失，应转向基础编程资源。

### Task 4 — Read unfamiliar code

给定一个短文件，学习者需要：

- 找到 entry point；
- 追踪一个值经过 2–3 个简单步骤；
- 运行前写出 prediction；
- 运行验证，并在不一致时指出需要重新检查的步骤。

**Evidence:** value trace + prediction + actual observation。

**Do not test:** 大型代码库导航、设计模式、语言高级特性。

### Task 5 — Debugging basics

给定一个小型、单一故障程序，学习者需要：

- 阅读 error / exception；
- 提出一个具体、可检验 hypothesis；
- 做一次 controlled correction；
- 重新运行并验证修复。

**Evidence:** error excerpt、hypothesis、single diff、verification result。

Debugger 在 Bridge 层级可以是可选工具；不要求 breakpoint/watchpoint 等专业技能。核心是证据驱动的最小修正。

### Task 6 — Git survival

在课程提供的 repository 中，学习者需要：

- clone/open repository（已处于 Codespace 等环境时可改为确认 repository 状态）；
- 查看 git status 与一个小 git diff；
- 创建一个小 commit，**或**读取并解释课程提供的短 commit history；
- 对一个小型本地改动执行安全恢复/撤销，并确认 baseline 未被破坏。

**Evidence:** status/diff/commit-or-history record + restore/reset result。

**Do not test:** rebase、复杂 branching、merge conflict workflow、Git internals。

### Task 7 — Environment and reproducibility

学习者需要：

- 运行课程提供的 **preflight interface**；
- 记录当前 Python/tool/environment version 信息；
- 运行一个 baseline command/test；
- 保存足以让自己或他人复现该 baseline 的 evidence packet。

**Evidence packet minimum:**

- environment identifier；
- relevant version output；
- command；
- input/fixture identity；
- baseline result；
- working-tree state（如适用）。

本文不 pin Python、base image、compiler/toolchain 等具体版本；OQ-BP-006 在实现阶段决定 canonical stable environment。

## Diagnostic outcomes

Diagnostic 使用四个 placement 状态，不做分数排名。

### READY

学习者已经具备 7 个任务对应能力，可以直接进入 M00。**不要求为了获得 READY 而实际完成 diagnostic**；已有可靠经验的学习者可以 self-place。

典型表现：

- 能独立运行并修改短程序；
- 能保留 baseline/evidence；
- 遇到小故障会先读错误、提出假设并验证；
- 不因偶尔查命令帮助而失去 READY 资格。

### READY WITH TARGETED REVIEW

只有 1–2 个明确 practical skill 较弱，但不影响基础编程判断。

行动：

- 只完成对应 remediation；
- 用该项 exit evidence 确认恢复；
- 随后进入 M00。

### BRIDGE RECOMMENDED

学习者具备 D-002 的基础编程能力，但在多个 practical entry skills 上还不能可靠完成任务，例如：

- 无法稳定运行/定位文件；
- 无法解释基本错误或做受控修复；
- Git 操作容易破坏 baseline；
- 无法保存可复现 evidence。

行动：按弱项完成 targeted Bridge remediation 后重新执行相关任务，不要求重做全部 7 项。

### PROGRAMMING FOUNDATION NEEDED

学习者尚不能可靠理解或修改包含变量、条件、循环、函数的短程序。

这不属于 Bridge 的修补范围。建议先补齐基础编程，再进入 Essential CS；这只是课程 scope 判断，不是能力价值判断。

## Targeted remediation map

| Weak area | Target capability | Minimal remediation | Exit evidence |
|---|---|---|---|
| Files/paths | 能定位、读取、修改并解释 input/output location | 一个小目录练习 + 相对/绝对路径检查 | 正确路径 + 小 diff + location 说明 |
| Shell | 能运行命令/脚本并读取 exit status | 运行 3–5 个课程提供命令，不扩展成 shell 课程 | transcript + exit-status explanation |
| Python execution | 能运行 baseline、做单一改动、恢复 working state | 一个短程序修改练习 | baseline + diff + rerun |
| Code reading | 能追踪短代码中的一个值 | 一次 entry-point/value-trace 练习 | prediction + actual trace |
| Debugging | 能从 error → hypothesis → correction → verification | 一个单故障 fixture | error + hypothesis + fix verification |
| Git survival | 能安全查看改动并恢复 baseline | status/diff/commit-or-history/restore 最小练习 | clean/expected status + evidence |
| Reproducibility | 能运行 preflight 并保存环境/baseline | 一次 evidence-packet 练习 | environment + command + result packet |

Remediation 的目标是“足够进入 M00”，不是把每项技能教到熟练或专业水平。

## Bridge exit evidence

Bridge 不提供独立证书或 Core 学分。完成 targeted remediation 后，学习者只需证明：

1. 能取得并运行课程 repository / environment；
2. 能对一个小程序做 prediction → run → controlled change → verify；
3. 能读取一个基本 error 并提出可检验 hypothesis；
4. 能使用最小 Git 操作保存/检查/恢复改动；
5. 能记录 environment + baseline + evidence。

这些能力准备学习者进入 M00 L00-02；**真正的 technical-investigation workflow 仍在 M00 首次 canonical 教授和评估。**

## Explicit exclusions

Bridge 明确**不是**：

- Python course；
- shell scripting course；
- Linux administration；
- Git internals / advanced Git workflow；
- IDE tutorial；
- package-management course；
- cloud setup；
- Docker prerequisite；
- C prerequisite；
- math prerequisite；
- Core system-concept preview course。

如果实现阶段发现必须加入上述内容才能让大量目标学习者进入课程，应记录 learner-validation evidence，并通过正式 curriculum review 决定，而不是静默扩大 Bridge。

## Open-question boundaries

- **OQ-BP-001 — bounded AI literacy:** 本 Bridge 不决定 AI literacy 是否成为 Core。AI 输出最多作为“需验证的外部建议”出现，不作为 diagnostic 能力项。
- **OQ-BP-003 — human-facing/accessibility boundary:** 本 Bridge 不把 HCI/accessibility 引入 Core 或 diagnostic。
- **OQ-BP-006 — canonical environment versions:** 本文只要求记录实际环境和通过 preflight；不 pin 具体版本。

## Future implementation notes

Blueprint 之后实现 Bridge 时，应提供：

- 小型 course-owned fixture repository；
- one-click canonical environment；
- deterministic reset；
- 简短 preflight；
- 不依赖网络搜索才能完成的 baseline tasks；
- progressive hints；
- 对 environment failure 与 learner-skill failure 的区分。

这些属于后续实现，不在本 Blueprint artifact 中写成完整教程或 Lab code。

## Canonical references

- meta/DECISIONS.md — D-002 learner, D-008 environment, D-009 teaching loop
- meta/CURRICULUM_MAP.md
- meta/COMPETENCY_MATRIX.md
- meta/blueprint/dependency-graph-v0.1.md
- meta/blueprint/final-reconciliation-v0.1.md
- meta/LAB_DESIGN_POLICY.md
- meta/OPEN_QUESTIONS.md
