# EXP-05｜MIT 6.033 复制、事务与日志容错源码考察 (Source Expedition)

## 考察档案

- **考察标识**：`EXP-05` — MIT 6.033 Replication, Transactions & Logging Source Expedition
- **所属模块**：`M17`（Replication, Consistency & Consensus）
- **主要能力**：**Observe** (在权威高校经典讲义中定位并审视主备复制与视图服务器的架构设计)
- **进阶能力**：**Explain** (阐明集中式视图服务器协调与去中心化 Raft 多数派选举的本质差异), **Judge** (评估网络分区对心跳故障检测造成的根本歧义)
- **采纳状态**：**ADOPT — LINK AND PARAPHRASE ONLY**（官方链接与释义导读，零代码/图表搬运）
- **官方来源**：MIT OpenCourseWare, 6.033 Computer System Engineering, Spring 2018
- **版权规范**：MIT OCW 当前 Terms 页面标示 CC BY-NC-SA 4.0；第三方材料仍可能有独立权利限制。Essential CS 默认只做**链接 + attribution + 原创问题/释义**：不复制 MIT 幻灯片、图表、讲义正文、作业题或代码。Lead 于 **2026-09-05** 重新核对来源与许可页。

---

## 1. 考察背景与教育目标

在单机系统中，我们通过事务与预写日志（WAL, M14）实现了单崩溃域内的原子性与持久性。跨越网络之后，为了抵御整台物理主机的崩溃，系统必须将状态复制到多个独立机器上。

MIT 6.033 Spring 2018 的官方索引把这些材料分开安排：
1. **Lecture 14 — Reliability via Replication**：可靠性、冗余与复制基础；
2. **Lecture 15 — Introduction to Transactions**：事务原子性/隔离性边界；
3. **Lecture 16 — Atomicity via Logging**：日志与崩溃恢复；
4. **Lecture 19 — Availability via Replication**：Replicated State Machines、Primary/Backup、View Server、网络分区、centralization，以及随后引出的 distributed consensus / Raft。

因此，EXP-05 继续保留 Blueprint 接受的 **L14/L15/L16 三锚点**来连接 replication / transactions / logging；而 Issue #103 已要求的 **View Server ↔ Raft 比较**使用官方 **Lecture 19** 作为窄范围的 Lead provenance correction。不要把 Lecture 19 的内容错误归到 Lecture 14。

---

## 2. 权威来源官方导航与三锚点链接 (Three-Anchor Route)

学习者应直接访问 MIT OpenCourseWare 官方公开讲义（PDF）：

1. **锚点 1（复制可靠性基础）**：
   - 讲义：Lecture 14 — *Fault Tolerance: Reliability via Replication*
   - 官方链接：[MIT 6.033 Spring 2018 Lecture 14 PDF](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/8eb16d3628bbd77ee7e8471b9871ec09_MIT6_033S18lec14.pdf)
   - 讲义目录总索引：[MIT 6.033 Spring 2018 Lecture Notes Index](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/lecture-notes/)
   - 研读重点：reliability metrics、redundancy/replication，以及复制在**所声明故障域**中的收益与成本。不要从该讲错误提取 View Server 规则。

2. **锚点 2（对比阅读：事务原子性与隔离性边界）**：
   - 讲义：Lecture 15 — *Fault Tolerance: Introduction to Transactions*
   - 官方链接：[MIT 6.033 Spring 2018 Lecture 15 PDF](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/df1526408e3ec6f7e43aadfa1ce5f944_MIT6_033S18lec15.pdf)
   - 研读重点：回顾事务的 All-or-Nothing（原子性）与 Before-or-After（隔离性）属性，建立与分布式复制一致性的明确心智防火墙。

3. **锚点 3（对比阅读：日志与崩溃恢复）**：
   - 讲义：Lecture 16 — *Atomicity via Logging*
   - 官方链接：[MIT 6.033 Spring 2018 Lecture 16 PDF](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/76fa216e8e5a4c4722c315a84b8e09a8c_MIT6_033S18lec16.pdf)
   - 研读重点：Write-Ahead Logging 规则与 Checkpoint 机制，观察节点在重启重放阶段如何恢复内存状态。

4. **Lead provenance correction（仅用于既有 View Server ↔ Raft 比较）**：
   - 讲义：Lecture 19 — *Availability via Replication*
   - 官方资源页：[MIT 6.033 Spring 2018 Lecture 19](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/mit6_033s18lec19/)
   - 官方详细提纲：[Lecture 19 Outline](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/pages/week-11/lecture-19-outline/)
   - 只检查：Primary/Backup、View Server、ping-based failure detection、partition handling、centralization，以及该讲末尾从 View Server central point of failure 引向 distributed consensus / Raft 的桥接。

---

## 3. 考察任务卡与停止规则 (Stop Rules)

```
========================================================================================================
EXP-05 BOUNDED SOURCE ROUTE & STOPPING RULES
========================================================================================================
1. Lecture 14:
   * reliability / replication foundations
   * name the failure domain and what replication does NOT automatically prove

2. Lectures 15–16:
   * bounded comparison only: transaction atomicity/isolation and logging/recovery
   * do not turn EXP-05 into a full transaction/recovery course

3. Lecture 19 (Lead provenance correction for the already-required comparison):
   * Primary / Backup + View Server
   * ping-based failure detection cannot distinguish every crash vs partition case
   * identify the View Server's centralized dependency
   * stop after the course-owned comparison to the bounded M17 Raft majority/election trace

NO external code compilation.
NO MIT diagram/text vendoring.
NO complete-course reading.
========================================================================================================
```

> **铁律停止规则（Stop Rules）**：
> - **严禁编译或运行外部代码**：本考察不包含任何外部代码工程；
> - **严禁全课无边界漫游**：专注于 Lecture 14，以理解视图切换与故障歧义为主；
> - **严禁抄录课件图表**：学习者必须在自己原创的读书卡中，手绘或使用纯文本标注一张主备协调时序图；
> - **若外链由于网络原因无法访问**：在实证报告中如实记录 `OPTIONAL / SOURCE RECHECK BLOCKED`，严禁编造访问结果。

---

## 4. 核心研读问题框架 (Guiding Questions)

学习者在阅读 Lecture 14 时，需在读书卡中独立回答以下四个核心问题：

1. **Lecture 14 — replication foundation**：复制提高的究竟是哪一种 reliability/availability 属性？它依赖哪些独立故障假设，又不能自动证明什么？
2. **Lecture 19 — 主备与 View Server**：Primary/Backup/View Server 各自维护什么角色/状态？ping-based failure detection 的观测为什么不能简单等同于“远端物理死亡”？
3. **Lecture 19 — partition / centralization**：View Server 在分区时用了哪些规则来约束 Primary/Backup 行为？官方提纲为什么把 View Server 描述为 central point of failure / possible bottleneck？
4. **课程对比 — View Server vs bounded Raft trace**：一个集中式 authority service 与一个 replicated voting protocol 的 failure/coordination assumptions 有何不同？只比较课程已经学习的 majority-set overlap + vote/log/commit 义务；不要说“Raft 没有任何单点依赖”或把多数派重叠单独当成完整安全证明。

---

## 5. 达标产出与实证模板 (Deliverables)

完成本考察后，学习者须在 `course/evidence/exp-05-evidence-template.md`（或 `foundations-m17-evidence-template.md` Section I）中如实填报：
- 讲义外链访问记录与现时性核查日期；
- 四个核心问题的原创释义回答；
- 一张学习者原创标注的主备视图切换时序图；
- Lecture 14 replication foundation、Lecture 19 Primary/Backup + View Server、以及课程 bounded Raft trace 的**模型/故障边界比较**。
- Source audit 明确记录：View Server 内容来自 Lecture 19，而非 Lecture 14。
