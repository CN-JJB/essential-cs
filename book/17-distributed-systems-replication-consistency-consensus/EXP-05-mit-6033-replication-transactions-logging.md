# EXP-05｜MIT 6.033 复制、事务与日志容错源码考察 (Source Expedition)

## 考察档案

- **考察标识**：`EXP-05` — MIT 6.033 Replication, Transactions & Logging Source Expedition
- **所属模块**：`M17`（Replication, Consistency & Consensus）
- **主要能力**：**Observe** (在权威高校经典讲义中定位并审视主备复制与视图服务器的架构设计)
- **进阶能力**：**Explain** (阐明集中式视图服务器协调与去中心化 Raft 多数派选举的本质差异), **Judge** (评估网络分区对心跳故障检测造成的根本歧义)
- **采纳状态**：**ADOPT — LINK AND PARAPHRASE ONLY**（官方链接与释义导读，零代码/图表搬运）
- **官方来源**：MIT OpenCourseWare, 6.033 Computer System Engineering, Spring 2018
- **版权规范**：MIT OCW CC BY-NC-SA 4.0（遵循第三方知识产权保留条款）。Essential CS 严格执行**零抄录、零搬运（Zero Vendoring）**：不复制 MIT 原版幻灯片、不搬运原始课件图表、不截取原书段落、不搬运作业题。仅提供官方权威外链、引导性思考框架与学习者原创读书卡。

---

## 1. 考察背景与教育目标

在单机系统中，我们通过事务与预写日志（WAL, M14）实现了单崩溃域内的原子性与持久性。跨越网络之后，为了抵御整台物理主机的崩溃，系统必须将状态复制到多个独立机器上。

MIT 经典的系统工程课程 **6.033 (Computer System Engineering)** 在容错（Fault Tolerance）模块中提供了一条极为精炼的系统认知进阶链：
1. **Lecture 14（复制与主备切换）**：如何利用Primary-Backup模型提高系统可靠性？当主节点静默时，为什么引入第三方的“视图服务器（View Server）”能够打破双主分脑（Split-Brain）？
2. **Lecture 15（事务模型引论）**：回顾单机原子性（All-or-Nothing）与隔离性（Before-or-After）如何为并发故障恢复奠定契约；
3. **Lecture 16（基于日志的原子性恢复）**：回顾预写日志与恢复演算法，为分布式节点重启重放提供微观基石。

本考察的目的在于通过**严格受控的三锚点阅读路径（Three-Anchor Route）**，指导学习者研读 MIT 6.033 Lecture 14 的核心机制，对比集中式视图协调与去中心化多数派共识（Raft）的心智模型。

---

## 2. 权威来源官方导航与三锚点链接 (Three-Anchor Route)

学习者应直接访问 MIT OpenCourseWare 官方公开讲义（PDF）：

1. **锚点 1（核心阅读：主备复制与视图服务器）**：
   - 讲义：Lecture 14 — *Fault Tolerance: Reliability via Replication*
   - 官方链接：[MIT 6.033 Spring 2018 Lecture 14 PDF](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/8eb16d3628bbd77ee7e8471b9871ec09_MIT6_033S18lec14.pdf)
   - 讲义目录总索引：[MIT 6.033 Spring 2018 Lecture Notes Index](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/lecture-notes/)
   - 研读重点：State Machine Replication 概念、Primary/Backup 状态同步流程、Ping/Ack 心跳机制的局限性、View Server 如何维护单调递增的视图编号（View Number）。

2. **锚点 2（对比阅读：事务原子性与隔离性边界）**：
   - 讲义：Lecture 15 — *Fault Tolerance: Introduction to Transactions*
   - 官方链接：[MIT 6.033 Spring 2018 Lecture 15 PDF](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/df1526408e3ec6f7e43aadfa1ce5f944_MIT6_033S18lec15.pdf)
   - 研读重点：回顾事务的 All-or-Nothing（原子性）与 Before-or-After（隔离性）属性，建立与分布式复制一致性的明确心智防火墙。

3. **锚点 3（对比阅读：日志与崩溃恢复）**：
   - 讲义：Lecture 16 — *Atomicity via Logging*
   - 官方链接：[MIT 6.033 Spring 2018 Lecture 16 PDF](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/76fa216e8e5a4c4722c315a84b8e09a8c_MIT6_033S18lec16.pdf)
   - 研读重点：Write-Ahead Logging 规则与 Checkpoint 机制，观察节点在重启重放阶段如何恢复内存状态。

---

## 3. 考察任务卡与停止规则 (Stop Rules)

```
========================================================================================================
EXP-05 BOUNDED SOURCE ROUTE & STOPPING RULES
========================================================================================================
1. [主备复制与心跳检测]
   "如何用 Backup 容忍 Primary 宕机?"
         │
         v
   [MIT 6.033 Lecture 14 第 1-4 页]:
   * 观察重点: 状态机复制 (Deterministic State Machine)、同步复制 (State Transfer)
   * 核心思考: 心跳超时到底能证明什么? (证明不了宕机, 只能证明不可达!)
         │
         v
2. [视图服务器协调]
   "谁有权决定谁是主节点?"
         │
         v
   [MIT 6.033 Lecture 14 第 5-8 页]:
   * 观察重点: View Server 规则 (View Number, Primary, Backup)
   * 核心机制: View Server 为什么要求 Primary 显式 ACK 当前 View 才能推进到下一个 View?
   * 停止点: 读完 View Server 切换规则即止; 严禁深入完整 6.824 Lab 2/3 Go 代码工程!
         │
         v
3. [跨系统模型对比]
   "MIT View Server vs. Raft 多数派选举"
   * 集中式仲裁器 (View Server 是单点依赖) vs. 去中心化法定人数 (Raft 多数派无单点)
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

1. **主备状态追踪**：
   在 MIT 6.033 的主备模型中，Primary 与 Backup 分别跟踪维护了哪些状态？客户端的读写请求由谁直接处理？
2. **故障检测的根本局限**：
   当 Primary 停止向 View Server 发送心跳 Ping 时，View Server 能够断定 Primary 物理断电了吗？如果仅仅是网络链路拥塞，而 Primary 仍在继续处理客户端请求，会发生什么灾难性后果？
3. **视图推进的同步屏障（Sync Barrier）**：
   View Server 为何规定：**“在收到当前 View 的 Primary 确认之前，严禁单方面推进到下一个 View”**？这条规则如何防止脑裂（Split-Brain）？
4. **架构对比：View Server vs. Raft**：
   - MIT 6.033 的 View Server 是一个集中式的权威仲裁器（Coordinator）。如果 View Server 自身宕机了，整个集群的状态推进会怎样？
   - 课程中学习的 Raft 协议是如何利用**多数派重叠（Majority Quorum）**打破对单个仲裁节点的依赖的？

---

## 5. 达标产出与实证模板 (Deliverables)

完成本考察后，学习者须在 `course/evidence/exp-05-evidence-template.md`（或 `foundations-m17-evidence-template.md` Section I）中如实填报：
- 讲义外链访问记录与现时性核查日期；
- 四个核心问题的原创释义回答；
- 一张学习者原创标注的主备视图切换时序图；
- 单机方案 vs. 主备视图模型 vs. Raft 共识模型的权衡判断。
