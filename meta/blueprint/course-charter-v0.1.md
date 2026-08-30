# Essential CS Course Charter v0.1

Status: **Blueprint v0.1 — READY FOR LEAD REVIEW**
Purpose: define the durable course promise and boundary. Constitutional rules remain in [`meta/CURRICULUM_INVARIANTS.md`](../CURRICULUM_INVARIANTS.md); this document does not replace them.

## Mission

Essential CS 的最高目标是帮助学习者建立**准确的现代计算系统世界模型（modern computing-system world model）与独立技术判断（independent technical judgment）**。

完成 Core 后，学习者应能把一个现代系统连成一条可解释、可观察、可质疑的链：

`source → runtime/compiler → machine → OS → storage → network → browser/server → database → concurrency → distributed systems → infrastructure → security/reliability/performance/cost`

学习者不仅要知道这些层“叫什么”，还要能说明数据、状态、时间、故障与信任边界在哪里变化，以及需要什么证据才能支持或推翻自己的解释。

## Target learner

主要学习者是有基础编程经验、但没有正式 CS 教育背景的成人/受教育学习者。课程假定其理解变量、条件、循环、函数，并能运行一个小型 Python 或 JavaScript 程序；约高中数学水平足够进入课程。算法课程、离散数学、C、Linux、网络、数据库、操作系统、Shell、Git、云与职业软件工程经验都不是入门前提。

更精确的学习者契约见 [`learner-profile-v0.1.md`](./learner-profile-v0.1.md)。

## Graduate capability

毕业能力由八个 canonical competencies 定义，而不是由“看完多少主题”定义：

- **Trace**：跨层追踪数据、控制与状态。
- **Explain**：用机制解释观察结果，并说明模型的适用边界。
- **Observe**：用真实工具观察被抽象隐藏的行为。
- **Diagnose**：基于证据形成假设、测量、定位与解释问题。
- **Correctness**：陈述规格（specification）、不变量（invariant）与假设，并推理其被破坏时的后果。
- **Judge**：比较方案的约束、收益、代价、故障模式、替代项与“不该使用”的情形。
- **Estimate**：进行有用的数量级估算，而不把粗估伪装成精确测量。
- **Learn-New-Tech**：使用权威资料、源码与实验独立调查陌生技术，区分稳定原理与当前实现/实践。

可观察的毕业标准见 [`learning-outcomes-v0.1.md`](./learning-outcomes-v0.1.md) 与 [`meta/COMPETENCY_MATRIX.md`](../COMPETENCY_MATRIX.md)。

## Scope philosophy

Essential CS **没有全局课程时长上限**。范围由教育价值控制，而不是由“必须压缩到多少小时”控制。

Core / Deep Dive 边界保持严格：Core 必须给出完整的共享计算世界观；Deep Dive 才承担专业化、完整实现或更深理论。Core 不是“压缩版 CS 学位”，也不以覆盖传统课程目录为目标。与此同时，“现代”不等于“新潮”：坚持 **principle before product**，产品、框架与当前实践只有在能暴露稳定机制、真实约束或重要判断时才进入教学，并且必须允许被替换或淘汰。

课程可以很长，但反馈回路必须短：每个 learner-visible Stage 都应产生明确 capability gain、checkpoint、project evidence 与 exit criteria。

## Teaching philosophy

课程坚持 **accessible, not dumbed-down**：减少偶然认知负担，但不删除关键技术事实。

默认教学循环是：

`Question → Mental Model → Mechanism → Observe → Build → Break → Explain → Judge → Project`

Lab/实践优先使用：

- `Build → Observe → Break → Explain`
- `Reveal → Use → Inspect`

当真实机制可以安全、清晰地被观察时，优先真实机制而不是假模拟。动手的目的不是最大化实现量，而是制造可检验的理解。Lab 选择遵循 **Adopt → Adapt → Build**：先寻找经典、成熟、可验证的实验，必要时适配，只有现有方案不足时才自建。

课程采用 **Teach Once → Revisit Many**：canonical definition/mechanism 只有一个主要教学 home，后续通过应用、连接、故障与权衡 revisit，而不是重复讲第二套定义。课程以 **self-study first** 为设计前提：重要解释、边界、预期观察、卡点支持与退出标准不能依赖教师现场补救。

## Mini Cloud App role

Mini Cloud App 是贯穿课程的**整合脊柱（integrative spine）**，不是课程主题本身。它使用刻意简单的业务域，让系统复杂性来自被学习的机制，而不是来自产品需求。

P0–P9 每次只在有明确约束与学习收益时增加复杂度。缓存、队列、容器、代理、副本等组件都不能因为“现代系统看起来应该有”而加入；**拒绝一个组件可以是正确且合格的工程判断**。

项目必须配合 Beyond-the-Project 例子，把同一机制连接到 CLI、编译器、批处理、桌面/移动软件、数据系统或基础设施等场景，防止课程滑向 Web 开发训练。Canonical P0–P9 映射见 [`final-reconciliation-v0.1.md`](./final-reconciliation-v0.1.md) §6。

## Research, evidence, and AI

AI 可以辅助搜索、草拟、综合、维护与审查，但**从不构成事实权威**。技术主张应受标准/规范、官方文档、经典教材、论文、大学课程、成熟源码与可复现实验约束。重要 Module 在大规模 Lesson drafting 前需要 Research Dossier；先研究，再进行重要写作。

课程仍必须自包含：外部来源用于约束和深化教学，而不能把课程变成链接列表。重要主张应保留适当 provenance，区分 principle / specification / implementation / current practice，并明确不确定性与验证边界。

OQ-BP-001 仍未决定 AI literacy 是否成为 Core 内容。当前安全实践仅是：AI 生成的 claim/code/configuration 是**不受信任的假设**，需要来源、测试、测量或安全审查来验证。

## Language, format, and licensing

- **Canonical teaching language:** 中文；重要技术术语首次重要出现时保留英文。
- **Source format:** Markdown-first；网站是未来可生成的视图，不替代 canonical source。
- **Original educational content / diagrams:** 采用 CC BY-SA 4.0 的许可意图。
- **Original code / tools / Mini Cloud App:** 采用 Apache-2.0 的许可意图。
- 第三方材料必须保留 provenance、许可与 attribution；本 Charter 不复制许可正文。

## What Essential CS is NOT

Essential CS 明确不是：

- 竞赛编程或刷题训练；
- 前端、框架或 Web 开发职业训练；
- 云厂商、容器编排或产品认证课程；
- “所有东西都从零实现一遍”的课程；
- 以产品热度、架构装饰或基础设施数量衡量“现代性”的课程；
- 自动扩张为 AI/ML/LLM 课程；OQ-BP-001 仍需正式架构决策；
- 把外部链接、视频或文档列表当成教学本体的课程；
- 压缩版 CS 学位或完整传统学科目录的替代品。

## What v1.0 means

**v1.0 means teachable, not merely written.**

只有在完整 Core spine 可教学、Mini Cloud App 演化完整、所有 REQUIRED Labs 可运行且有文档、provenance/licensing 到位、内容通过多角色独立验证、目标学习者验证关键 Core 路径、外部覆盖审计完成、维护/复核流程实际运行、且不存在 critical blockers 时，项目才达到 v1.0 gate。

这意味着“文稿写完”不是发布条件；学习者能否稳定进入、运行、观察、诊断、解释、判断并完成 Final System Defense 才是发布条件。

## Canonical references

- [`meta/CURRICULUM_INVARIANTS.md`](../CURRICULUM_INVARIANTS.md)
- [`meta/DECISIONS.md`](../DECISIONS.md)
- [`meta/CURRICULUM_MAP.md`](../CURRICULUM_MAP.md)
- [`meta/COMPETENCY_MATRIX.md`](../COMPETENCY_MATRIX.md)
- [`meta/RESEARCH_AND_SOURCE_POLICY.md`](../RESEARCH_AND_SOURCE_POLICY.md)
- [`meta/LAB_DESIGN_POLICY.md`](../LAB_DESIGN_POLICY.md)
- [`meta/RELEASE_AND_MAINTENANCE_POLICY.md`](../RELEASE_AND_MAINTENANCE_POLICY.md)
