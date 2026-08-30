# Essential CS Learner Profile v0.1

Status: **Blueprint v0.1 — READY FOR LEAD REVIEW**
Purpose: define the learner/course entry contract precisely. This document elaborates D-002 without widening prerequisites.

## Primary learner

Essential CS 面向有基础编程经验、希望建立现代计算系统整体理解与技术判断的成人/受教育学习者。**不要求正式 CS 教育背景。**

进入课程时，学习者应大致能够：

- 理解变量、条件、循环、函数与基本数据流；
- 阅读一个短小的 Python 或 JavaScript 程序；
- 运行一个小程序并根据输出做简单修改；
- 用自然语言说明一段小程序大致在做什么。

这些要求定义的是“能进入系统课程”最低编程基础，不是对语言熟练度、工程经验或算法训练的要求。

## What is not assumed

课程**不假定**学习者已经学过或熟练掌握：

- algorithms coursework；
- discrete mathematics；
- C 或 assembly；
- Linux 管理或日常 Linux 使用；
- networking；
- databases；
- operating systems；
- shell fluency；
- Git expertise；
- cloud platforms；
- professional software engineering。

如果某个 Core 机制需要上述知识，课程必须在合适的 canonical home 中引入，而不能把它悄悄变成前置条件。

## Mathematics

默认数学背景约为**高中数学**。课程需要的离散、概率、统计或数量级推理按实际问题 **just in time** 引入。

例如，测量中的重复实验、分布、median/percentile、variation、uncertainty 与 inference limit 在 M04 `L04-02` 首次系统落地；可靠性概率在 M16/M17 按需出现。课程不设置独立数学 Gate，也不因为教学方便而要求学习者先完成离散数学、微积分或统计学课程。

## Practical-computing variation

目标学习者可能“会写程序”，却仍缺少稳定的实践技术流畅度。常见薄弱项包括：

- 文件、目录与相对/绝对路径；
- terminal / shell 基本生存能力；
- 环境初始化、运行脚本与调用工具；
- 根据错误信息进行最小调试；
- 阅读陌生的短代码；
- Git 的最小安全使用；
- 记录环境、基线、命令、输出与可复现证据。

这种差异**不是扩大 Core 前置要求的理由**，而是 [`bridge-and-diagnostic-v0.1.md`](./bridge-and-diagnostic-v0.1.md) 存在的原因。Bridge 是 optional preparation + diagnostic；已有这些能力的学习者应直接跳过。

## Environment model

- **Canonical systems environment:** Linux。
- 所有 REQUIRED Labs 必须能在 canonical Linux 环境中可复现运行。
- **Standard one-click path:** Dev Container / Codespace，用于把环境摩擦控制在课程可支持范围内。
- 本地 Linux、macOS、Windows + WSL 可以作为 convenience paths，但不是 Core 技术真相的第二套标准。
- 学习者需要会在该环境中运行、观察、修改和保存证据；**不需要成为 Linux administrator**。
- 具体 Python、SQLite、compiler/toolchain、Linux base image 等稳定版本由 **OQ-BP-006** 在实现阶段统一 pin；本 Learner Profile 不绑定版本号。

课程允许某些 REQUIRED Labs 需要额外的已声明工具（例如 canonical Lab map 中的 QEMU/RISC-V toolchain、`gcc -pthread`、`sqlite3`、`curl`），但这些应由 Lab setup/preflight 提供和验证，而不是假定学习者预先会安装、管理或排错复杂工具链。

## Learner responsibilities

学习者需要主动参与证据式学习，而不是只复制命令。最低责任包括：

1. **先预测，再实验。** 在可行时写下预期结果、规格或假设。
2. **保存证据。** 保留关键命令、环境信息、输入、输出、差异、失败现象与恢复结果。
3. **尝试诊断。** 遇到问题时先读错误、形成假设、做受控改动，而不是只寻找“正确命令”。
4. **区分 observation 与 explanation。** “我看到了 X”不等于“X 的原因已经被证明”。
5. **批判性使用来源。** 文档、规范、源码、实验与 AI 输出的证据地位不同；AI 生成内容默认需要验证。
6. **报告环境摩擦。** 如果 canonical path 无法复现，应记录环境和失败信息，而不是默默换一个不可追踪的路径。
7. **做累积复习。** 后续 Stage 会反复调用先前概念；学习者应通过回看 canonical explanation 和旧证据完成 revisit。

## Course responsibilities

作为交换，课程必须承担以下责任：

- **Self-contained:** 核心解释不能藏在外部链接中；外部资料用于证据与深化，不替代教学。
- **Explicit prerequisites:** 每个学习单元说明真正需要的前置知识，不制造隐藏前置。
- **Canonical environment:** 提供可复现 Linux 路径、preflight、baseline 与 reset/cleanup 约定。
- **Progressive hints:** 卡点支持从提示到定位逐步展开，而不是直接给最终命令或答案。
- **Expected observations:** Lab/实验说明应该看到什么、哪些差异是合理的、哪些结果表示环境异常。
- **Mechanism explanation:** 不止告诉学习者“做什么”，还要解释为什么观察会发生及模型在哪里失效。
- **What can be ignored—for now:** 主动标出当前无需掌握的细节，降低非必要认知负担。
- **Core reproducibility:** REQUIRED Labs 在 canonical environment 中可运行，并有适当 smoke tests / evidence gates。
- **Terminology consistency:** canonical concepts 使用一致中英文术语与 Concept Registry first-home / revisit 纪律。
- **No prerequisite creep:** 如果真实学习者持续卡在入口，应优先改进 Bridge、环境或教学，不应轻易把问题转化成更高的入学门槛。

## Likely misconceptions and friction

课程设计需要主动防范以下高频误区，而不把它们变成额外“知识清单”：

| Misconception / friction | Design implication |
|---|---|
| “代码跑通 = 正确” | 要求规格、不变量、边界输入与失败条件，不把一次成功当证明。 |
| “这次更快 = 这个方案更快” | 要求环境、workload、baseline、重复测量、variation 与 causal limit。 |
| “container = VM” | 在 M19 回到 process / namespace / resource / filesystem 边界。 |
| “database 只是把表存起来” | 用 query plan、index、transaction、recovery 与 durability 暴露机制。 |
| “timeout = 请求失败且没有发生” | 在网络/分布式阶段区分未收到响应与未发生/未提交。 |
| “加密 = 系统安全” | 安全综合必须同时讨论 trust boundary、identity、authorization、composition、privacy。 |
| “现代 = 更多组件” | 任何组件都必须给出约束、收益、成本、failure mode、When NOT to use；拒绝组件可通过答辩。 |
| 工具/环境摩擦或害怕读真实源码 | Bridge + preflight + constrained Source Expedition 提供最小可达路径与明确 stopping point。 |

## Learner validation target

未来 pilot / learner validation 应优先招募符合以下教育特征的学习者：

- 有上述基础编程能力；
- 没有通过正式 CS 学位路径建立完整系统知识；
- 主要处于 self-study 或低教师依赖环境；
- 实践工具经验有足够差异：既包括 shell/Git 较弱者，也包括日常工具较熟但系统知识薄弱者。

这种多样性用于暴露 Bridge、环境、说明与隐藏前置问题；不应为了“样本整齐”引入与学习目标无关的人口学条件。

## Entry boundary

如果学习者已经具备 Bridge diagnostic 所检查的能力（无论是否实际执行 diagnostic），应直接进入 M00。若自检或 diagnostic 只暴露一两个实践技能薄弱点，使用 targeted Bridge remediation 后进入即可。若学习者尚不能理解基本变量、函数和控制流，推荐先补齐基础编程；Essential CS Bridge 不承担 Programming 101 的职责。

## Canonical references

- [`meta/DECISIONS.md`](../DECISIONS.md) — D-002, D-005, D-008, D-009
- [`meta/CURRICULUM_MAP.md`](../CURRICULUM_MAP.md)
- [`meta/blueprint/dependency-graph-v0.1.md`](./dependency-graph-v0.1.md)
- [`meta/blueprint/lab-source-selection-map-v0.1.md`](./lab-source-selection-map-v0.1.md)
- [`meta/LAB_DESIGN_POLICY.md`](../LAB_DESIGN_POLICY.md)
- [`bridge-and-diagnostic-v0.1.md`](./bridge-and-diagnostic-v0.1.md)
