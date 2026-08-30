# Essential CS Learning Outcomes v0.1

Status: **Blueprint v0.1 — READY FOR LEAD REVIEW**
Purpose: define what successful Core completion means in observable learner behavior. [`meta/COMPETENCY_MATRIX.md`](../COMPETENCY_MATRIX.md) remains the canonical map of **where** capabilities grow; this document consolidates **what completion demonstrates**.

## Outcome architecture

Essential CS 使用八个且仅八个 canonical competencies：

1. Trace
2. Explain
3. Observe
4. Diagnose
5. Correctness
6. Judge
7. Estimate
8. Learn-New-Tech

毕业标准不是“接触过这些主题”，而是能够在陌生或变化后的约束下，用真实证据完成以下行为。

## 1. Trace

**Graduate outcome**
给定一个真实请求、数据项或控制路径，学习者能够跨越

`source → runtime/compiler → machine → OS → storage/network → server/browser → database → concurrency → distributed/infrastructure`

进行追踪，并指出表示（representation）、状态（state）、时间、延迟、故障和信任边界在哪里发生变化。

**Observable evidence**

- 画出或记录一条 request/data/control trace，并把关键跨层跳转与真实 observation 对应起来。
- 指出状态是 transient、process-local、file/database、replicated、telemetry 或 credential state 中的哪一种，而不是把“数据都在数据库”当作默认答案。
- 给出一个可以确认或反驳该 trace 的下一步观察，例如 syscall、packet、query plan、trace span 或 state inspection。

**Does not count**

- 只背诵 OSI/浏览器/数据库组件列表；
- 画出无法对应真实证据的架构图；
- 把逻辑调用链直接当作真实执行/网络/存储路径。

**Canonical evidence connections**

- **Stage exits:** S1–S6 都要求逐步扩大的 trace evidence；S7/M24 汇总 whole-system trace。
- **Required Labs:** LAB-REQ-01/02/03/04/05 均要求 trace mechanism or state transitions。
- **Mini Cloud App:** P0、P1、P3 逐步扩展；P9 要求完整 whole-system trace。
- **Final System Defense:** 必须提交 request/data/control trace 与 state inventory，并能在 changed constraint 下重新解释路径。

## 2. Explain

**Graduate outcome**
学习者能够解释“为什么抽象表现为所观察到的行为”，把解释连接到机制、规格与证据，并明确当前 mental model 在哪里不再准确。

**Observable evidence**

- 从 observation 回到具体机制，例如 representation boundary、syscall、cache/locality、protocol semantics、transaction isolation、synchronization 或 trust boundary。
- 区分 interface guarantee 与 implementation detail；说明哪些结论来自 specification、哪些来自当前 implementation。
- 对类比或简化模型给出 stopping/breaking point。

**Does not count**

- 用另一个标签替代解释（“因为有缓存”“因为是分布式”）；
- 只复述工具输出；
- 把某个版本/产品的行为说成永恒原理。

**Canonical evidence connections**

- **Stage exits:** S1 mental model、S2 source-to-runtime、S4 protocol/browser、S5 DB/concurrency mechanism 与 S7 defense 都要求 explanation evidence。
- **Required Labs:** 五个 Required Labs 都要求把 observation 解释到机制。
- **Mini Cloud App:** P0/P1/P2/P5/P7 明确要求 contract/mechanism explanation；P9 汇总。
- **Final System Defense:** 每个重要 architecture claim 都必须有 mechanism + evidence + limit，而不是组件命名。

## 3. Observe

**Graduate outcome**
学习者能够选择并使用合适的真实工具，观察通常被抽象隐藏的行为，同时把工具视为测量手段而不是学习目标。

可使用的工具类别包括 debugger/disassembler、process/file tools、network inspection、query planner、tracing/logging/metrics 等；具体产品和命令可以变化。

**Observable evidence**

- 根据问题选择一个能区分候选解释的观察点。
- 保存命令/配置、环境、关键输出或图像，并说明观察对结论的支持范围。
- 识别工具 overhead、missingness、sampling、version 或 environment 对结果的限制。

**Does not count**

- 会背大量 flags 但不知道为什么运行；
- 截图一个工具面板却没有问题、prediction 或 interpretation；
- 把 profiler/tracer 的输出直接当成因果证明。

**Canonical evidence connections**

- **Stage exits:** S2 machine observation、S3 process/file、S4 network/browser、S5 query/transaction、S6 deployment/incident、S7 defense 持续增长。
- **Required Labs:** LAB-REQ-01/02/04/05 直接 Assess Observe。
- **Mini Cloud App:** P4、P6、P7、P8 强化 observation；P9 聚合。
- **Final System Defense:** 至少能为关键 performance/failure/security claim 指出真实 observation record，而不是“根据架构图推测”。

## 4. Diagnose

**Graduate outcome**
面对错误、异常、性能问题或不确定行为，学习者能够使用：

`Observe → Hypothesize → Measure → Locate → Explain → Judge`

形成可更新的诊断过程，并区分 evidence、correlation 与 causal proof。

**Observable evidence**

- 从错误/症状提出至少一个具体、可证伪假设。
- 做一次受控改变或测量，缩小问题位置，而不是同时更改多个变量。
- 在修复后验证原症状、相关 invariant 和新的副作用边界。
- 当证据不足时明确保留 competing explanation。

**Does not count**

- 反复试命令直到“好了”；
- 看到一个相关 metric 就宣布根因；
- 修复后不重新验证或无法说明为何修复有效。

**Canonical evidence connections**

- **Stage exits:** S2 crash/performance、S3 OS/I/O、S5 anomaly/race、S6 timeout/incident、S7 failure walkthrough 是主要 Assess 点。
- **Required Labs:** LAB-REQ-02/03/04/05 Assess Diagnose。
- **Mini Cloud App:** P1/P2/P3/P4/P5/P8 明确练习 diagnosis；P9 总结。
- **Final System Defense:** 能 walkthrough 一个代表性 failure，展示 evidence → hypothesis → localization → bounded conclusion。

## 5. Correctness

**Graduate outcome**
学习者能够在讨论系统“是否正确”前，先陈述：

- specification；
- invariant；
- failure assumptions；
- concurrency assumptions；
- trust assumptions；

并解释这些条件被违反时，允许/禁止的行为如何变化。

**Observable evidence**

- 为数据、transaction、concurrent operation、retry/idempotency 或 authorization 写出可检验 invariant。
- 构造一个违反假设的 counterexample / interleaving / failure scenario。
- 说明修复究竟恢复了哪个保证，以及仍未保证什么。

**Does not count**

- “测试通过所以正确”；
- 把 happy path 或类型检查等同于完整 correctness；
- 在没有 failure/concurrency/trust assumptions 时声称“强一致/安全/可靠”。

**Canonical evidence connections**

- **Stage exits:** S1 首次形成 spec/invariant discipline；S5 transaction/concurrency 是主要成熟点；S7 系统级整合。
- **Required Labs:** LAB-REQ-01/03/04/05 Assess Correctness。
- **Mini Cloud App:** P0、P1、P2、P3、P4、P5、P6、P8 都有 correctness evidence；P9 汇总。
- **Final System Defense:** 必须提交 invariant & failure matrix，并能说明 architecture change 对 guarantees 的影响。

## 6. Judge

**Graduate outcome**
学习者能够对技术/架构选择使用统一判断框架：

`Problem → Constraints → Mechanism → Gains → Costs → Failure Modes → Alternatives → When NOT to use → Scale Threshold → Evidence → Stable Principle`

并接受“不增加组件”或“维持简单方案”作为可正确的结论。

**Observable evidence**

- 在明确 workload、failure、security、team/operations、cost 等约束后比较至少两个可行方案。
- 说明复杂性被移到了哪里，而不只列“优缺点”。
- 给出 When NOT to use 与 scale/constraint threshold。
- 说明证据不足时需要先测量、查规范或做 pilot，而不是凭趋势判断。

**Does not count**

- 产品 feature checklist；
- “更现代/更可扩展/更多组件所以更好”；
- 没有约束的 pros/cons essay；
- 以厂商流行度替代机制和证据。

**Canonical evidence connections**

- **Stage exits:** S1 建立 trade-off language；S3 durability judgment；S6 形成 systematic distributed/infra judgment；S7 Technology Card + defense 完成整合。
- **Required Labs:** LAB-REQ-01/03/04/05 Assess Judge；LAB-REQ-02 不把工具/源码路径选择本身当 judgment assessment。
- **Mini Cloud App:** P2–P8 持续加入 constrained choices；P9 明确允许 rejection of a component。
- **Final System Defense:** 必须说明 selected/rejected alternatives、moved complexity、failure modes、cost 与 stopping point。

## 7. Estimate

**Graduate outcome**
学习者能够对 latency、bandwidth、QPS、memory、storage、replication 与 operational/cloud cost 做足以指导下一步判断的 order-of-magnitude reasoning，并明确粗估的误差与需要真实测量的部分。

**Observable evidence**

- 把问题分解为可估算项，写出单位、数量级与假设。
- 用结果判断某方案是否明显不可行、是否值得进一步 benchmark 或是否需要更精确数据。
- 将估算与 measurement 分开；当实测偏离估算时能检查 workload、cache、concurrency、queueing、environment 等假设。

**Does not count**

- 给出没有单位或假设的单个数字；
- 把“napkin math”写成虚假的高精度预测；
- 用一次本机 benchmark 直接推断生产容量或云成本。

**Canonical evidence connections**

- **Stage exits:** S1 size/complexity，S2 latency，S3 storage，S4 RTT/bandwidth，S5 DB IO，S6 replication/resource cost，S7 whole-system cost model。
- **Required Labs:** LAB-REQ-04/05 直接 Assess Estimate；其他 Labs 可以产生局部估算但不扩大其 canonical assessment claim。
- **Mini Cloud App:** P0、P3、P4、P6 持续练习；P9 完成全局 latency/resource/cost analysis。
- **Final System Defense:** 必须给出关键 scale/cost estimate、假设与“何时需要测量替代粗估”的界线。

## 8. Learn-New-Tech

**Graduate outcome**
面对陌生技术，学习者能够独立建立一个足够准确、可验证的最小模型，使用 official docs、standards/specs、source、papers 与 experiments 调查其机制和边界，并区分 stable principle 与 implementation/current practice。

**Observable evidence**

- 从问题和约束出发选择合适 evidence layer，而不是先搜“最佳产品”。
- 对一个关键 claim 找到 authoritative source，并用源码或实验进行必要交叉验证。
- 写出“不知道什么”、下一步调查计划与 stopping point。
- 对快速变化的产品/实践说明哪些结论可能需要重新检查。

**Does not count**

- 复制 AI/博客总结；
- 只阅读 marketing/README；
- 把会使用一个产品 CLI 当成学会新技术；
- 无法区分 specification guarantee 与 current implementation behavior。

**Canonical evidence connections**

- **Stage exits:** S2 首次用 docs/source 验证 runtime/language claim；S3–S6 持续 practice；S7 M23/M24 系统 Assess。
- **Required Labs:** LAB-REQ-02 明确 Assess Learn-New-Tech（受约束的真实源码路线）；Source Expeditions 提供后续 practice，但不替代 Core outcomes。
- **Mini Cloud App:** P7 明确练习 environment/deployment source/version investigation；P9 要求 unfamiliar constraint/technology investigation。
- **Final System Defense:** 必须列出 unknowns、证据缺口、调查计划与合理 stopping point。

## Integrated graduate outcomes

完成 Essential CS Core 后，学习者应能把上述八项能力组合起来：

1. **Reconstruct a modern system:** 重建 source 到 infrastructure 的主链，并定位 state/data/time/failure/trust。
2. **Explain mechanism, not labels:** 说明观察为何发生，以及抽象何时不再准确。
3. **Observe hidden mechanisms:** 为问题选择真实工具并保存可复现证据，而不把工具熟练度变成目标。
4. **Diagnose systematically:** 以 Observe → Hypothesize → Measure → Locate → Explain → Judge 推进，保留因果不确定性。
5. **Reason about correctness:** 先写 specification/invariant/assumptions，再谈 correctness、安全、可靠性或一致性。
6. **Judge trade-offs:** 用统一 Technology Evaluation 结构比较方案，并明确 When NOT to use。
7. **Estimate:** 用数量级推理缩小决策空间，再用测量校正。
8. **Learn unfamiliar technology:** 依赖权威来源、源码、论文与实验建立可验证模型，而非依赖流畅叙述。

## Stage progression S1–S7

| Stage | Canonical name | Outcome progression |
|---|---|---|
| S1 | 计算的底座 — Foundations of Computation | 建立 representation-level Trace/Explain、基本 specification/invariant/trade-off 与 size/complexity estimate；形成 L00-02 evidence/toolchain discipline。 |
| S2 | 机器 — The Machine (ISA, Execution, Memory Hierarchy, Language→Machine) | 用 debugger/disassembler/measurement 把 source→runtime→machine 变成可观察路径；首次系统 Assess Observe/Diagnose 与 measurement uncertainty。 |
| S3 | 操作系统与持久化 — OS: Processes, Memory, Files (+ Storage) | 跨 process/memory/file/storage 边界 Trace/Diagnose；开始对 durability/failure bound 做 judgment。 |
| S4 | 网络与浏览器 — Networking, the Web, Browser as integrated case | 追踪端到端 request，解释 protocol/browser/intermediary 机制，区分 timeout/failure，并估算网络成本。 |
| S5 | 数据与并发 — Databases, Transactions, Concurrency | 以 query/transaction/interleaving evidence 成熟 Correctness/Diagnose；判断 index/isolation/synchronization trade-offs。 |
| S6 | 分布式与现代基础设施 — Distributed Systems, Cloud, Infrastructure | 在 partial failure、replication、delivery、deployment、observability 下系统化 Judge/Estimate/Diagnose；S4/S5 两条支路在此汇合。 |
| S7 | 安全综合·系统判断·最终答辩 — Security Synthesis, Systems Thinking, Final Defense | 整合 trust/security、measurement、cost、technology evaluation 与全部八项能力，完成 M24 Final System Defense。 |

Stage 名称、顺序与 hard prerequisite 语义以 [`meta/CURRICULUM_MAP.md`](../CURRICULUM_MAP.md) 和 [`dependency-graph-v0.1.md`](./dependency-graph-v0.1.md) 为准；本文件不创建新 Stage 或 DAG 关系。

## Final System Defense completion evidence

最终答辩不是“展示更多基础设施”，而是要求学习者在变化约束下，能为以下内容提供可辩护证据：

- **assumptions**：workload、failure、trust、environment、team/operational boundary；
- **invariants**：系统必须保持什么；
- **architecture**：关键边界和数据/request/control paths；
- **failures**：至少一个完整 failure walkthrough 与恢复/降级逻辑；
- **evidence**：claim 对应的观察、来源、实验与限制；
- **measurement**：环境、workload、baseline、repetitions/distribution/uncertainty 与 causal limit；
- **cost**：latency、resource、storage、bandwidth、replication、operational/cloud cost 的合理估算；
- **trade-offs**：gains/costs/failure modes 与 complexity movement；
- **rejected alternatives**：为什么没有选择某组件或架构；
- **unknowns + investigation plan**：尚未证明什么，下一步用何种 authoritative evidence 调查，何时停止。

P9/M24 的通过标准是**evidence-to-claim relationship 与独立判断**。增加 cache、queue、replica、container、proxy 或 cloud product 从不自动提高成绩；在约束下证明“不需要增加”同样可以是正确答案。

## Canonical references

- [`meta/COMPETENCY_MATRIX.md`](../COMPETENCY_MATRIX.md)
- [`meta/CURRICULUM_MAP.md`](../CURRICULUM_MAP.md)
- [`meta/blueprint/lab-source-selection-map-v0.1.md`](./lab-source-selection-map-v0.1.md)
- [`meta/blueprint/final-reconciliation-v0.1.md`](./final-reconciliation-v0.1.md)
