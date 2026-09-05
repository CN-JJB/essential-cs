# EXP-02｜PostgreSQL 查询规划器与缓冲池路径源码考察 (Source Expedition)

## 考察档案

- **考察标识**：`EXP-02` — PostgreSQL Planner & Buffer Route Source Expedition
- **所属模块**：`M13`（Databases, Storage Engines & Indexing）
- **主要能力**：**Observe** (在工业级关系型数据库源码中观测查询代价模型与缓冲池系统实现)
- **进阶能力**：**Trace** (追踪从代价估算公式到缓冲页置换策略的逻辑脉络), **Explain** (阐明工业级实现与教学概念模型的异同)
- **官方源码库**：[PostgreSQL 官方 Git 源码树](https://git.postgresql.org/gitweb/?p=postgresql.git) / [GitHub 镜像](https://github.com/postgres/postgres)
- **课程基准考察版本记录 (Course Inspection Baseline)**：
  - **考察核验日期**：`2026-09-04`
  - **基准提交哈希 (Commit SHA)**：`7344937cbe640cd8c5304cefe7d6b726187ad4ab`
  - **所在分支**：`master`（开发分支；注：PostgreSQL 18.6 为当前独立的稳定发布与文档分支）
- **考察方式**：**在线链接与受限导读（Link-and-Inspection-First）**。严禁克隆完整仓库，严禁本地编译 PostgreSQL，严禁复制代码搬运。

---

## 1. 考察背景与教育目标

在概念学习中，我们了解了数据库根据物理访问路径选择全表扫描（Sequential Scan）或索引扫描（Index Scan），以及存储引擎通过缓冲池（Buffer Pool）在内存中缓存磁盘数据页。这些机制在最具代表性的生产级开源关系型数据库 PostgreSQL 中究竟是如何落地的？

PostgreSQL 经过数十年的演进，拥有极其清晰的系统架构。本考察通过**严格受控的三锚点路径（Three-Anchor Route）**，带领学习者直击 PostgreSQL 内部两处核心机制：
1. **计划器与路径代价估算锚点**：观测物理访问路径的代价计算公式，探究为什么随机 I/O（`random_page_cost`）与顺序 I/O（`seq_page_cost`）的权重设置会直接影响扫描策略的选择；
2. **缓冲池管理锚点**：观测数据页如何在共享内存中通过缓冲描述符（Buffer Descriptor）、引用固定（Pinning）以及时钟扫描算法（Clock Sweep）实现缓存与置换。

---

## 2. 考察路线与停止规则（Stop Rules）

```
========================================================================================================
EXP-02 BOUNDED SOURCE ROUTE & STOPPING POINTS
========================================================================================================
1. [计划生成文档锚点]
   "PostgreSQL 的 Plan 阶段如何组织与历史演进?"
         │
         ▼
   [计划器文档锚点]: src/backend/optimizer/plan/README
   * 观测重点: 计划生成的核心职责以及关于子查询（Subselect）处理的历史演进脉络
   * Target 1 关键警示: 在当前核验版本中，该文档主要聚焦于子查询规划的历史细节，而非通用的 Path->Plan 宏观架构
   * 停止点: 读完文档引言与子查询演进说明即止; 严禁追踪复杂的递归子查询展开逻辑!
         │
         ▼
2. [物理访问路径代价估算]
   "优化器如何量化全表扫描与索引扫描的成本?"
         │
         ▼
   [代价计算代码锚点]: src/backend/optimizer/path/costsize.c
   * 观测重点: cost_seqscan() 与 cost_index() 函数中如何结合 page I/O 与 CPU tuple 代价
   * 停止点: 停在基础代价值相加的返回处; 严禁深入复杂的 JIT 编译代价与几何索引评估!
         │
         ▼
3. [存储引擎缓冲池管理]
   "从磁盘读取的数据页如何在内存中组织、锁定与置换?"
         │
         ▼
   [缓冲池文档锚点]: src/backend/storage/buffer/README
   * 观测重点: 共享缓冲池结构、BufferAlloc() 分配、Pinning 引用固定与 Clock Sweep 页面淘汰
   * 停止点: 停在 Clock Sweep 算法描述处; 严禁下潜到底层锁实现与 WAL 恢复重放!
========================================================================================================
```

> **铁律停止规则（Stop Rules）**：
> - **严禁克隆或下载完整 PostgreSQL 仓库**：使用官方网页代码浏览器或 GitHub 页面即可完成全部观测；
> - **严禁编译 PostgreSQL**；
> - **严禁无边界代码漫游**：到达指定文件入口与核心逻辑后立即停止，不顺着头文件无限深挖；
> - **严禁代码整段搬运**：本考察以官方链接与学习者自己的总结释义为主。遵循 PostgreSQL License，不复制代码到课程库中。

---

## 3. 考察任务卡（Bounded Inspection Card）

请跟随指导，依次打开官方代码链接，完成以下各项实证任务：

### 任务 1（计划生成与历史演进）：阅读 `src/backend/optimizer/plan/README`

- **目标文件**：[`src/backend/optimizer/plan/README`](https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/backend/optimizer/plan/README)
- **Target 1 关键警示（Historical Caveat）**：
  在课程基准核验版本（commit `7344937cbe640cd8c5304cefe7d6b726187ad4ab`）中，`src/backend/optimizer/plan/README` **并不是一份通用的“Path 到 Plan 整体架构概览”，而是一份聚焦于子查询与子计划（Subselect / Subplan Planning）处理历史与特定算法演进的文档（始于 1998 年）**。
  *(审阅背景补充注：上级目录的 `src/backend/optimizer/README` 提供了优化器宏观阶段综述，但该文件仅作为审阅者的补充背景参考，绝非第四个学习者步骤，亦不替代本任务的受限实证。)*
- **考察问题**：
  该文档开篇阐述了什么主题？它如何描述子查询是作为独立子计划处理还是扁平化并入主查询？
- **实证记录**：
  该文件详细阐述了子查询计划的转换机制与历史约束。它指出计划器需要权衡子查询被当作独立子计划执行、还是扁平化（Flatten）并入主查询树中。这印证了：工业级优化器的代码树中往往包含特定历史演进的痕迹，不能盲目假设每个命名为 `README` 的文件都是全局教科书式的概述。
- **停止确认**：已在概览与引言部分停止，未深入复杂的参数传递（param propagation）实现。

### 任务 2（代价估算模型）：检查 `src/backend/optimizer/path/costsize.c`

- **目标文件**：[`src/backend/optimizer/path/costsize.c`](https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/backend/optimizer/path/costsize.c)
- **检索定位**：定位函数 `cost_seqscan()` 与 `cost_index()`。
- **考察问题**：
  1. 在 `cost_seqscan()` 中，PostgreSQL 是如何结合磁盘页面数（`baserel->pages`）与元组数（`baserel->tuples`）计算启动代价（`startup_cost`）与总代价（`total_cost`）的？涉及了哪些系统参数（如 `seq_page_cost`、`cpu_tuple_cost`）？
  2. 在 `cost_index()` 中，为什么要区分索引树自身的遍历代价与回表访问数据页的代价？为什么 `random_page_cost` 的默认设定值通常高于 `seq_page_cost`？
- **实证记录**：
  1. `cost_seqscan` 核心公式将 I/O 代价与 CPU 代价相加：总代价 $\approx \text{pages} \times \text{seq\_page\_cost} + \text{tuples} \times \text{cpu\_tuple\_cost}$（外加操作符过滤评估代价）。启动代价通常为 0，因为顺序扫描无需提前构建中间树结构。
  2. `cost_index` 计算了遍历索引页面的 I/O、评估索引元组的 CPU 代价，以及根据选择率估算回表读取数据页的随机 I/O 代价。当过滤选择率较差时，大量的随机 I/O 导致估算代价骤增，使得优化器转而倾向全表顺序扫描。
- **停止确认**：已在基础代价相加与返回处停止，未跟踪特定硬件平台的并行扫描修正分支。

### 任务 3（缓冲池管理与置换）：检查 `src/backend/storage/buffer/README`

- **目标文件**：[`src/backend/storage/buffer/README`](https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/backend/storage/buffer/README)
- **检索定位**：检索章节 `BufferAlloc`、`Buffer Descriptors` 以及 `Clock Sweep`。
- **考察问题**：
  1. PostgreSQL 缓冲池如何使用缓冲描述符（Buffer Descriptor）跟踪内存缓冲页的状态？
  2. 什么是“固定”（Pinning）？为什么在持有页面内容时必须保持引用计数（`refcount`）大于 0？
  3. PostgreSQL 使用什么算法寻找置换受害页（Victim Page）？时钟扫描（Clock Sweep）中的 `usage_count` 扮演什么角色？
- **实证记录**：
  1. 缓冲池由固定数量的共享内存页与一一对应的 Buffer Descriptor 数组构成。每个描述符记录了磁盘块标识（`BufferTag`）、状态标志（Dirty、Valid 等）以及引用计数。
  2. **Pinning（固定）** 通过原子递增 `refcount` 保证该缓冲页在被当前后端进程读取或修改期间，绝不会被其他并发进程驱逐置换到磁盘。
  3. **Clock Sweep 算法**：维护一个循环指针扫描描述符数组。如果当前缓冲页未被固定（`refcount == 0`），且其使用计数（`usage_count`）大于 0，则递减该计数并继续步进；只有当遇到 `refcount == 0` 且 `usage_count == 0` 的页面时，才将其选为淘汰受害页。
- **停止确认**：已在时钟扫描置换逻辑描述处停止，未追踪磁盘刷盘（BufferSync）与崩溃恢复逻辑。

### 任务 4（概念模型与工程现实辨析）：反思“代价与绝对速度”

- **反思问题**：
  为什么 PostgreSQL 优化器计算出的 `cost` 是无量纲的“代价值”，而不是具体的“执行毫秒数”？
- **实证结论**：
  **代价是一个经验启发式模型，不是物理时间预测器。** 磁盘延迟、操作系统缓存（Page Cache）、SSD 固态闪存并发读写特性以及硬件内存在不同机器上差异巨大。PostgreSQL 优化器的目的不是准确预测耗时，而是**在多个候选执行路径中，正确选出相对更优的那一个**。把优化器代价值当作绝对性能指标在系统工程上是认知偏差。

---

## 4. 考察总结与概念连接

通过本次 Source Expedition，我们在工业级数据库内核中印证了核心系统规律：
1. **权衡取舍（EC-CON-006 Trade-off）与局部性（EC-CON-012 Locality）**：`costsize.c` 中 `seq_page_cost` 与 `random_page_cost` 的比例映射了顺序 I/O 局部性与随机 I/O 的本质差异；
2. **抽象与接口边界（EC-CON-005 Interface）**：查询执行器只需调用存储层接口获取元组，优化器通过代价抽象屏蔽了物理存储布局的微观细节；
3. **缓存机制（EC-CON-011 Caching）**：缓冲池利用引用固定（Pinning）与 Clock Sweep 策略，在有限内存与并发安全性之间达成平衡。

---

## 5. 版权与规范声明

- PostgreSQL 源码受 [PostgreSQL License](https://www.postgresql.org/about/licence/)（宽松型类 BSD 开源协议）管辖。
- 本考察采取 **Link-and-Inspection-First** 原则：不镜像、不分发、不修改任何 PostgreSQL 源码。所有实证均基于官方代码树的受限查阅与学习者自己的总结释义。
