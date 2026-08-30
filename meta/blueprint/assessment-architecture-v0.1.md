# Assessment Architecture v0.1

Status: **Blueprint v0.1 — LEAD-ACCEPTED** (not VERIFIED/released)

本文件回答：

> Essential CS 如何收集足够证据，判断学习者是否真的能够推理现代计算系统？

它**整合**现有 canonical assessment system，不创建新的 Stage、Module、competency、Lab、Mini Cloud App milestone 或数字评分制度。权威边界来自：

- `meta/CURRICULUM_MAP.md`
- `meta/COMPETENCY_MATRIX.md`
- `meta/blueprint/learning-outcomes-v0.1.md`
- `meta/blueprint/lab-source-selection-map-v0.1.md`
- `meta/blueprint/final-reconciliation-v0.1.md`
- `meta/DEFINITION_OF_DONE.md`
- `meta/REVIEW_POLICY.md`
- `meta/LAB_DESIGN_POLICY.md`

若本文与这些 canonical 文件冲突，以 canonical 文件为准并进入 Lead review；本文不自行修复课程架构。

## 1. Assessment purpose

Essential CS 不以“记住多少主题”为主要判断对象，而以**可观察、可复查、可迁移的系统推理证据**为对象。

核心问题不是：

> 学习者是否见过这个术语？

而是：

> 学习者能否在明确假设下，预测系统行为、观察真实机制、解释证据、破坏并定位边界、说明 invariant / failure / uncertainty，并对选择作出可辩护判断？

因此，assessment 必须遵守：

- **evidence > fluent prose**：流畅叙述不能替代观察、实验、来源或可复现路径；
- **mechanism > answer label**：正确结论但没有机制与证据，不能构成充分 competence evidence；
- **short feedback loops**：Lesson/Module 层应快速反馈，不把学习压缩为少数高压考试；
- **no architecture ornament**：组件更多、图更复杂、产品更“现代”不自动增加评价；
- **no single correct architecture**：尤其在 M23/M24，rubric 评价推理与证据质量，而非答案是否匹配参考架构；
- **support is diagnostic**：hint 的使用记录独立性与支撑程度，但不自动等价于失败；
- **author cannot self-VERIFY**：作者只能提交 `READY FOR LEAD REVIEW`；`VERIFIED` 需要独立 multi-role review。

## 2. Assessment modes

### 2.1 Primary modes: Explain / Predict / Break / Judge

四种 primary mode 贯穿 Lesson、Lab、project 与 Stage Checkpoint。

| Mode | 要求学习者做什么 | 合格证据的最低特征 | 不足证据 |
|---|---|---|---|
| **Explain** | 把观察连接到机制、边界、state/data/control path | 明确 claim、机制、证据与适用边界 | 只复述定义、只给类比、只说“因为框架这样做” |
| **Predict** | 在 reveal/run 前写出预期行为及理由 | 可证伪 prediction；必要时给 assumptions / invariant | 运行后倒推“我本来就知道” |
| **Break** | 在安全、受控条件下触发失败或违反前提 | 明确 changed variable、expected/actual observation、reset | 随机破坏、不可复现 crash、未说明 failure boundary |
| **Judge** | 在约束下比较选择并说明复杂性去向 | Problem/Constraints、alternatives、trade-offs、When NOT to use、evidence | feature checklist、“更现代所以更好”、无约束 pros/cons |

一个 assessment item 不必同时使用四种 mode；Required Labs 和高层 checkpoint 应组合其中多种。

### 2.2 Cumulative review modes: Recall / Connect / Transfer

`Recall / Connect / Transfer` 用于累积复习与迁移，不取代四种 primary mode。

| Mode | 作用 | 边界 |
|---|---|---|
| **Recall** | 快速取回少量接口事实、术语、单位、关键 guarantee | 不能成为 Stage exit 的唯一证据；不把课程变成 topic-recall exam |
| **Connect** | 把已学机制连接到新的 layer、failure、project 或 trade-off | 遵守 Teach Once → Revisit Many，不重新教授第二套 canonical definition |
| **Transfer** | 把已形成的 reasoning pattern 应用于不熟悉系统/约束 | 必须能说明哪些旧假设仍成立、哪些需要重新验证 |

优先顺序不是“Recall 越少越好”，而是：**Recall 只承担它擅长的快速检索；competence 的退出证据必须包含 Explain/Predict/Break/Judge 与 Connect/Transfer 中适合该能力的组合。**

## 3. Competency model and `I / P / A`

本文使用且只使用八项 canonical competencies：

1. Trace
2. Explain
3. Observe
4. Diagnose
5. Correctness
6. Judge
7. Estimate
8. Learn-New-Tech

`meta/COMPETENCY_MATRIX.md` 的符号语义保持不变：

- `I` = **Introduce**
- `P` = **Practice**
- `A` = **Assess / exit evidence**

### 3.1 `A` 的 operational meaning

`A` 不表示“这个 topic 已经上过”，而表示：

> **学习者已经产生了具体、可审查的退出证据，证明自己能够在该上下文中执行对应 competency。**

一个 `A` artifact 可以来自 Stage packet、Required Lab、Mini Cloud milestone 或 M24 System Defense；不要求为每个 `A` 重复制作一份新文档。允许**复用同一真实 evidence artifact 来支持多个合理 competency claim**，前提是 reviewer 能明确指出每个 claim 对应哪一段证据。

| Competency | `A` 至少要能观察到什么 |
|---|---|
| **Trace** | 可跟随的 data/control/state path，包含关键 boundary 与 state transition，而非只画静态框图 |
| **Explain** | claim ↔ evidence ↔ mechanism 的连接，并说明模型/抽象的适用边界 |
| **Observe** | 真实工具/系统 observation，带必要 environment/input/version context |
| **Diagnose** | hypothesis → measurement/observation → locate → explanation；区分 symptom、cause 与未排除解释 |
| **Correctness** | specification/invariant/allowed outcomes，展示违反方式或反例，并说明修复为何保持 invariant |
| **Judge** | 在明确 constraints 下比较 alternatives、gains/costs/failure modes、When NOT to use 与 complexity movement |
| **Estimate** | assumptions、单位、数量级、推导与“何时必须改用实测”的边界 |
| **Learn-New-Tech** | authoritative source route、关键 claim 的验证、stable principle / current behavior 区分、unknowns 与 stopping point |

没有某 competency 的 Module/Stage cell，不应为了“覆盖全面”而强行加 assessment。

## 4. Evidence hierarchy

Assessment 使用分层证据，而不是一张总考试卷。

| Layer | 主要目的 | 典型证据 | 形式压力 |
|---|---|---|---|
| Lesson / local check | 快速发现 mental-model 错误 | prediction、短 trace、解释一个 observation、修 misconception | 低 |
| Module-end capability evidence | 证明 named module-end capability 已可执行 | 一个能直接对应 `COMPETENCY_MATRIX.md` Module capability 的 artifact | 低到中；尽量复用已有 evidence |
| Required Lab evidence | 独立观察/破坏真实机制 | 可复现实验记录、invariant/failure、解释与 judgment | 中 |
| Mini Cloud App milestone evidence | 跨概念整合、应用约束 | milestone-specific trace/measurement/failure/trade-off | 中；不能替代 mechanism Lab |
| Stage System Checkpoint | 对该 Stage 的 `A` competencies 做 capability exit | 紧凑 evidence packet | 中；不是统一卷面考试 |
| Final System Defense | 全系统、变化约束下的累计 defense | P9/M24 cumulative packet + oral/written defense | 高，但无单一正确架构 |

**去重原则：** 同一 observation 如果已经在 Required Lab 或 milestone 中产生，可以进入 Module/Stage evidence packet；assessment architecture 不要求为了行政完整性再做一次同样实验。

## 5. Lesson / local checks

Lesson/local check 是最短反馈环。它们不是正式考试，目标是尽早暴露错误模型。

可用形态包括：

- **prediction before reveal**：运行、翻页或展示 trace 前先预测；
- **explain an observation**：对真实输出解释“为什么”；
- **identify an invariant**：指出什么必须始终成立；
- **trace a path**：沿 data/control/state 走过 2–N 个关键 boundary；
- **judge one constrained choice**：在一个明确 constraint 下比较两种足够小的方案；
- **repair a misconception**：给出常见错误解释，让学习者指出其错误边界并改写。

Local check 应尽量满足：

1. 保持短反馈回路（通常是一个小任务、一次 prediction/observation 或一个明确判断点），而非长延迟评分；
2. 给出 expected observation 或解释入口；
3. 能定位“概念错误 / 工具错误 / environment failure”中的哪一类；
4. 不以命令记忆、语法 trivia 或 prose polish 作为 competence proxy。

## 6. Module-end capability evidence

每个 Module 都有 `meta/COMPETENCY_MATRIX.md` 中的 **primary competency + capability by module end**。Module-end assessment 的职责是回答：

> 学习者是否能做出这个 capability，而不是是否完成了所有页面？

规则：

- 每个 Module 的 named capability 必须能由至少一个**已有或近邻** observable artifact 支撑；不要求为每个 Module 额外新建独立 artifact；
- 不要求每个 Module assess 八项 competencies；
- evidence 可以由 local check、Required Lab、Mini Cloud milestone 或 Stage packet 提供；
- Module 如果没有 Required Lab，不因此需要造一个 Lab；
- Module-end evidence 只记录“最小充分证据”，不复制整份学习日志；
- 若 artifact 只能证明工具操作而不能证明 mental model，则不能把它升级为 Explain/Diagnose/Judge 的 `A`。

例：M04 的退出不是“跑过 benchmark”，而是能做 fair measurement、看到 locality effect，并对 inference limit 作出说明；M19 的退出不是“会 Docker/Kubernetes 命令”，而是能解释 artifact/process/config/resource boundary 与 reproducibility/security isolation 的区别。

## 7. Required Lab evidence

以下 5 个 Required Labs 及 assessed competency mapping **原样继承** canonical selection/matrix；本文不重设计 Lab。

| Lab | Canonical home | Assessed competencies | Evidence role |
|---|---|---|---|
| **LAB-REQ-01** | M11（revisit M12） | Trace, Explain, Observe, Correctness, Judge | HTTP origin/intermediary/cache path；prediction + controlled break + reset + constrained judgment |
| **LAB-REQ-02** | M06（short revisit M08） | Trace, Explain, Observe, Diagnose, Learn-New-Tech | user program → syscall route；真实 source route、failure classification、reset evidence |
| **LAB-REQ-03** | M15 | Correctness, Trace, Diagnose, Explain, Judge | defined interleaving/lost update、invariant、mutex/condition repair、deadlock/progress boundary |
| **LAB-REQ-04** | M13（revisit M23） | Observe, Trace, Explain, Correctness, Diagnose, Estimate, Judge | SQLite plan/scan/index、result equivalence、workload/measurement limits、write/space cost |
| **LAB-REQ-05** | M14（revisits M09/M15） | Correctness, Trace, Observe, Diagnose, Explain, Judge, Estimate | SQLite transaction/isolation/rollback/recovery、timeline、guarantee-vs-application claim |

共同规则：

- 每个 Required Lab 先经过 repository + preflight + baseline + evidence record entry gate；
- measurement 遵守 `LAB_DESIGN_POLICY.md` / selection map 的 environment、workload、warmup、repetitions/distribution（适用时）、causal-limit 要求；
- “一次成功运行”不等于 correctness；
- “一次 benchmark 更快”不等于 causal proof；
- reference implementation 的存在不能替代 learner-produced evidence；
- project 中出现同一机制不能替代独立 mechanism Lab。

## 8. Mini Cloud App P0–P9 evidence

Mini Cloud App 是**integration spine**，不是“项目做得越复杂越高分”的 feature contest。

| Milestone | Evidence emphasis | Architecture guardrail |
|---|---|---|
| **P0** | Trace durable-state path；ownership/schema invariant；size estimate；simple alternative | 单进程、单 durable collection；不提前加 HTTP/auth/cache/replica |
| **P1** | boundary crossing、contract vs implementation、malformed/partial diagnosis | interface 最小化；不把 Web framework 作为目标 |
| **P2** | identity→authorization trace、allow/deny、privacy/logging decision | safe fixture；不通过本 milestone 决定 OQ-BP-003 |
| **P3** | socket/protocol observation、timeout ambiguity、safe retry/idempotency | local bounded failure；不从 loopback 推断 Internet behavior |
| **P4** | baseline/workload/query plan/distribution/equivalence、write/space cost、inference limit | 未测量前不加 index/cache |
| **P5** | anomaly/race、invariant、app lock vs DB guarantee、final-state verification | 独立 concurrency Lab 仍保留 |
| **P6** | backup/restore/recovery evidence、state version、loss bound、runbook claim | replica/managed recovery 不是默认升级 |
| **P7** | native vs optional container comparison、config/state/resource boundary、source/version map | native Linux canonical；container optional |
| **P8** | correlate request/failure、signal selection、redaction/missingness/overhead | structured logs/timers first；不要求 vendor stack |
| **P9** | all eight competencies under changed constraints | **拒绝增加组件可以是有效 Judge evidence**；不要求 queue/cache/replica/proxy/container/cloud |

### 8.1 What project evidence can and cannot prove

Project evidence擅长证明：

- 多概念在一个真实系统中的连接；
- requirement/constraint 改变后能否保持 invariant；
- learner 能否说明 selected/rejected alternatives；
- 技术复杂性被移动到了哪里。

Project evidence不能单独替代：

- 独立 Required Lab 对真实机制的观察；
- 受控 failure 的可重复性；
- source/spec verification；
- 在陌生上下文中的 Transfer。

**Architecture complexity itself earns no credit.**

## 9. Stage System Checkpoints

每个 Stage 结束时使用 **Stage System Checkpoint**。它是 capability exit，不是 topic-final exam。

### 9.1 Baseline evidence packet

一个有用的 baseline packet 为：

1. **prediction / specification**；
2. **real observation or controlled break**；
3. **mechanism explanation**；
4. **invariant / failure bound / uncertainty statement**；
5. **judgment or estimate when appropriate**；
6. **Connect / Transfer evidence**。

不同 Stage 可选不同 packet 内容；**不要求七个 Stage 交相同模板**。例如 S4 的重点是 request path/timeout/intermediary/browser observation，S5 的重点是 query/transaction/interleaving/correctness。

### 9.2 Stage exits select only relevant `A` competencies

下表只把 canonical matrix 中已经存在的 `A` 语义集中呈现；不新增 `A`。

| Stage | `A` competencies selected at exit | Representative packet anchors |
|---|---|---|
| **S1** | Trace, Explain, Correctness, Judge, Estimate | representation round-trip；size/complexity estimate；invariant；one data/tool trace |
| **S2** | Trace, Explain, Observe, Diagnose, Estimate, Learn-New-Tech | disassembly/debugger；locality measurement；source→runtime claim verified from docs/source；measurement uncertainty |
| **S3** | Trace, Observe, Diagnose, Judge, Estimate | syscall/process trace；address-space/file observation；durability judgment + loss-bound estimate |
| **S4** | Trace, Explain, Observe, Estimate | packet/socket/request trace；timeout distinction；proxy/cache comparison；browser/origin observation |
| **S5** | Trace, Explain, Observe, Diagnose, Correctness, Estimate | query plan；transaction anomaly；interleaving；invariant-preserving fix；Required DB/concurrency Labs |
| **S6** | Trace, Observe, Diagnose, Judge, Estimate | timeout/retry trace；replication/consistency scenario；delivery judgment；deployment comparison；controlled incident |
| **S7** | Trace, Explain, Observe, Diagnose, Correctness, Judge, Estimate, Learn-New-Tech | trust map；Technology Card；measurement/cost model；M24 complete defense |

`Recall` 可辅助 checkpoint，但不能独立形成 Stage exit。

### 9.3 Stage checkpoint review question

Reviewer 不问“是否答到参考答案”，而问：

- 这个 claim 的 evidence 在哪里？
- observation 是否能支持 causal statement？
- learner 是否区分 guarantee、assumption 与 current behavior？
- failure model 是否具体？
- 如果 constraint 改变，learner 能否指出哪些结论会失效？
- 是否存在 simpler alternative？
- 哪些 uncertainty 仍未解决？

## 10. Final System Defense — M24 / P9

M24 / P9 是累计 assessment。Learner 必须在**变化约束**下 defend system，而不是展示更多 infrastructure。

Defense 至少覆盖：

- **assumptions**：workload、failure、environment、trust、team/operational boundary；
- **system trace**：request/data/control path；
- **state inventory**：transient/process/database/backup/telemetry/credential 等 state；
- **invariants**：必须始终成立什么；
- **architecture**：关键 boundary 与责任；
- **failure model**：完整 failure walkthrough、recovery/degradation；
- **measurements**：environment、workload、baseline、repetition/distribution、uncertainty、causal limits；
- **security/trust decisions**：identity、authorization、secrets、certificate/signature/trust boundary 等适用项；
- **cost/scale estimates**：latency、bandwidth、storage、memory、replication/resource/operational/cloud cost 的数量级判断；
- **selected alternatives**：为什么选；
- **rejected alternatives**：为什么不选，复杂性会移动到哪里；
- **unknowns**：尚未证明什么；
- **investigation plan**：下一步 authoritative evidence、experiment/source route 与 stopping point。

### 10.1 No single correct architecture

M24 不定义唯一“正确架构”。

以下都可能是高质量结果，只要 evidence 与 constraint 支撑：

- 保持单节点 SQLite；
- 拒绝 cache；
- 拒绝 queue；
- 不容器化；
- 选择一个 bounded replica/proxy/queue case；
- 在新约束下改变某一边界但保持其他部分简单。

Rubric 评价的是 reasoning/evidence quality，不是组件数量、云产品数量或图的复杂度。

## 11. Qualitative rubric

不引入复杂 numeric grade。每个 dimension 可用四个 qualitative state：

- **证据不足**：claim 无足够 evidence，或 evidence 与 claim 不匹配；
- **部分可辩护**：有正确方向和局部 evidence，但机制、边界、替代解释或 uncertainty 仍明显缺失；
- **可辩护**：claim、evidence、mechanism、assumptions 与 limits 对齐，能够回答主要 challenge；
- **可迁移**：在陌生约束/上下文中仍能保持 causal restraint、修正假设、比较 alternatives，并形成新的可验证计划。

这些状态描述**证据质量**，不是总分；不同 artifact 可在不同 dimension 上处于不同状态。

### 11.1 Rubric dimensions

| Dimension | Reviewer question |
|---|---|
| **claim ↔ evidence alignment** | 证据是否真的支持该 claim，而非只“看起来相关”？ |
| **mechanism accuracy** | explanation 是否符合机制，是否混淆 abstraction 与 implementation？ |
| **explicit assumptions** | workload/environment/failure/trust 假设是否写明？ |
| **invariant/correctness reasoning** | learner 是否能写出必须保持的条件、allowed outcomes 与 violation？ |
| **failure reasoning** | 是否覆盖 partial/controlled failure、ambiguity、recovery 与 residual risk？ |
| **measurement quality** | metric、baseline、workload、repetition/distribution、environment 与 limits 是否适当？ |
| **causal restraint** | 是否避免把相关、单次 run 或单 benchmark 当成 cause？ |
| **trade-off reasoning** | gains、costs、failure modes、complexity movement 是否成对出现？ |
| **scale/cost awareness** | 是否知道什么 constraint 才值得引入更复杂技术？ |
| **alternative quality** | 是否比较真实可行的 simpler/different alternatives，而非 strawman？ |
| **uncertainty recognition** | 是否明确知道什么还不知道、证据缺口是什么？ |
| **transfer** | 是否能把 pattern 应用于陌生机制/constraint，而不是复制原答案？ |

**Prose polish 不是 rubric dimension。** 表达必须足够清晰让 reviewer 审查，但华丽文字不补偿错误 mental model 或缺失 evidence。

## 12. Progressive disclosure and stuck support

统一 support ladder：

`Question → Hint 1 → Hint 2 → Expected Observation → Full Explanation → reference implementation if needed`

### 12.1 How support affects assessment

Hint 的目的首先是**诊断并继续学习**，不是处罚。

可在 evidence metadata 中轻量记录 support level：

- **Independent**：未使用结构化提示即可完成；
- **Hint 1 / Hint 2**：在越来越具体的 scaffold 下完成；
- **Expected Observation**：知道应该看到什么后能解释或继续调查；
- **Full Explanation / reference implementation**：当前 artifact 主要用于学习与 remediation，不再声称是独立 exit evidence。

规则：

- 使用 Hint 1 **不自动失败**；
- 使用 Hint 2 也不自动取消 competency，只说明 independence 尚需复测；
- 如果 learner 在 support 后形成正确 model，可在后续新上下文做一次短 Transfer check 取得 independent evidence；
- “看过 full explanation 后能复述”不是独立 `A`；
- 若 full explanation 后仍无法执行最小 reasoning step，应回到 prerequisite/misconception diagnosis，而非扣分式惩罚。

Support level 与 rubric quality 是两个维度：一个 artifact 可以“Hint 1 后可辩护”，也可以“Independent 但证据不足”。

## 13. Machine-checkable vs review-required

自动化擅长验证**形式、可运行性、可重复性**；它不能可靠判定 mature technical judgment。

### 13.1 Machine-checkable

CI/tools 可验证，例如：

- code tests / unit/integration/smoke tests；
- exact required files；
- environment/preflight；
- link integrity；
- metadata / unique IDs；
- output shape / schema；
- command exit status；
- deterministic/reset/reproduction checks；
- clean working tree / expected artifact existence；
- no accidental file changes；
- Lab smoke-test path；
- evidence packet required fields 是否存在。

机器检查通过只意味着：

> artifact 在形式和运行条件上满足检查。

它**不意味着 reasoning 已经正确**。

### 13.2 Human / reviewer judgment required

需要 reviewer（可使用 AI 辅助，但不能把 AI 当 authority）判断：

- mental model accuracy；
- mechanism explanation；
- evidence 是否支持 causal claim；
- invariant / correctness argument 是否有效；
- failure assumptions 是否合适；
- measurement design 是否能回答问题；
- architecture trade-off 是否有约束、有替代方案、有 complexity accounting；
- Learn-New-Tech 的 source route 是否权威、是否区分 specification / implementation / current practice；
- Transfer 是否真正发生；
- uncertainty / stopping point 是否成熟；
- Final System Defense 是否形成可辩护整体。

### 13.3 Verification governance

- CI 不能把 pedagogy 或 reasoning 自动标记为 `VERIFIED`；
- author agent 不能 self-mark `VERIFIED`；
- `VERIFIED` 仍依赖 `REVIEW_POLICY.md` / `DEFINITION_OF_DONE.md` 的 independent multi-role review；
- author 的最高任务状态是 **`READY FOR LEAD REVIEW`**。

## 14. Compact assessment provenance

Evidence packet 在适用处保留：

- **environment**；
- **command/input/workload**；
- **version**（实际使用版本，不在本文 pin OQ-BP-006）；
- **observation**；
- **reasoning / claim**；
- **source**；
- **uncertainty / alternative explanation**；
- **reset / reproduction notes**。

目标是让 evidence 能被另一人复查，而不是形成行政 paperwork。

### 14.1 Compact packet shape

推荐最小形态：

```text
Question / claim:
Prediction or specification:
Environment + version:
Command / input / workload:
Observation:
Mechanism explanation:
Invariant / failure / uncertainty:
Judgment / estimate / alternative:
Source:
Reset / reproduce:
Support used (if any):
```

字段按任务裁剪；没有 measurement 的 item 不需要伪造 benchmark 字段，没有 judgment 的 item 不需要硬填 Technology Card。

## 15. Assessment anti-patterns

明确禁止把以下做法当成充分 competence evidence：

- **topic-recall-only exams**；
- **只有“正确最终答案”但没有 reasoning**；
- **fluent prose without evidence**；
- **architecture ornament**；
- **more components = better score**；
- **one benchmark = causal proof**；
- **one successful run = correctness**；
- **copying reference implementation** 后把成功运行当独立 competence；
- **AI-generated explanation treated as evidence**；
- **checklist completion treated as competency**；
- 把 tool/CLI fluency 本身当作 Learn-New-Tech；
- 把 product familiarity 当作 Judge；
- 把 Stage packet 变成统一、重复、庞大的 bureaucratic template；
- **author agent self-marking VERIFIED**。

## 16. Assessment flow by learner experience

正常学习流可概括为：

`local check → module capability evidence → Lab/project integration → Stage System Checkpoint → cumulative Connect/Transfer → M24/P9 Final System Defense`

这不是严格的一次性流水线：Lab/project evidence 可以回流到 Module/Stage packet；Stage checkpoint 暴露的 misconception 可以回到局部练习，再用新上下文重新证明。

最终目标是让 learner 形成可复用的系统推理习惯：

`Predict / Specify → Observe / Break → Explain mechanism → State invariant/failure/uncertainty → Judge / Estimate → Connect / Transfer`

## 17. Architecture preservation

本文没有：

- 改 Stage 名称或顺序；
- 改 Module DAG；
- 增删 Module；
- 重命名或增加 competency；
- 修改 `I / P / A` 语义；
- 重设计 LAB-REQ-01..05；
- 改 P0–P9；
- 创建数字 grade system；
- 允许 author self-VERIFIED；
- 决定 OQ-BP-001、OQ-BP-003 或 pin OQ-BP-006。

Assessment Architecture 的下一步不是增加 grading bureaucracy，而是在 Module/Lab 实现阶段把上述 evidence contracts 变成**短、真实、可复查的任务**。
