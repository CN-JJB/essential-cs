# LAB-OPT-03 — PostgreSQL EXPLAIN & Isolation Comparison (Strictly Optional Guide)

> **Status: STRICTLY OPTIONAL GUIDE**
>
> - **Core Requirement Status**: Neither PostgreSQL nor Docker is a Required dependency for Module M14 or LAB-REQ-05.
> - **Tool Availability Rule**: If PostgreSQL or Docker is not installed or available locally, this lab is classified as **`OPTIONAL TOOL UNAVAILABLE / SKIP`** without any penalty.
> - **Safety Rule**: Any `EXPLAIN ANALYZE` statement that executes data mutation (`INSERT`, `UPDATE`, `DELETE`) **MUST be wrapped inside a transaction and explicitly rolled back** (`BEGIN; ... ROLLBACK;`) to prevent persistent side effects.
> - **No Remote / Production Access**: Strictly forbidden to connect to remote, cloud, or production databases. Use only bounded, course-owned local test instances.

---

## 1. 指南目标与架构定位 (Objective & Architecture Placement)

在 M14 核心课程中，我们以嵌入式单文件数据库 SQLite 为基准，实测了回滚日志（Rollback Journal）与锁状态机在单机文件锁模型下的事务隔离与崩溃恢复机制。

本可选实验（LAB-OPT-03）面向希望拓展视野的学习者，通过客户端/服务端架构的代表性开源企业级数据库 **PostgreSQL**，对比观察：
1. **多版本并发控制 (MVCC)** 架构下的查询执行与物理缓冲池交互 (`EXPLAIN (ANALYZE, BUFFERS)`)；
2. **PostgreSQL 隔离级别对比**：观察同一并发更新在 Read Committed 与 Repeatable Read 下的不同处理：Read Committed 等待当前 updater 后会基于更新后的行版本重新检查并继续；Repeatable Read 若发现目标行在本事务快照之后已被并发事务实际更新并提交，则会终止当前事务并要求从事务边界重试。

---

## 2. 环境准备与跳过规则 (Prerequisites & Safe Skip)

运行本指南前，请先运行 Stage 5 环境预检：

```bash
python tests/preflight_data_concurrency.py
```

- 如果输出显示 `psql Client: REQUIRED CAPABILITY PASS` 或具备本地 Docker 容器环境，可继续尝试本指南；
- 如果输出显示 `psql Client: OPTIONAL TOOL UNAVAILABLE / SKIP`，**直接跳过本指南**，不影响 M14 Core 或 LAB-REQ-05 的任何通过判定。

---

## 3. 实验 A：物理访问与缓冲池实测 — EXPLAIN (ANALYZE, BUFFERS)

在 SQLite 中，`EXPLAIN QUERY PLAN` 仅报告高层逻辑计划。而在 PostgreSQL 中，`EXPLAIN (ANALYZE, BUFFERS)` 会真正执行查询，并精确测量实际毫秒耗时与共享缓冲池（Shared Buffers）的命中情况。

### 安全操作规程：包装只读与变动查询
对于只读查询，可以直接执行：
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, balance FROM accounts WHERE id = 'A';
```

对于任何包含变动的测量，**必须强制包裹在事务回滚块中**：
```sql
-- 绝对安全的不变式防护模式：测量真实修改开销后立即撤销
BEGIN;
EXPLAIN (ANALYZE, BUFFERS)
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
ROLLBACK;
```

### 输出结构解读（占位形状，不是课程固定实测值）：
```text
Update on accounts  (...actual planner estimates...) (...actual execution statistics...)
  Buffers: shared hit=<actual> read=<actual> dirtied=<actual> written=<actual>
  ->  <actual child plan node>
Planning Time: <actual>
Execution Time: <actual>
```
- **shared hit**：该次 PostgreSQL shared-buffer 访问在需要该 block 时已命中缓存，因此避免了为该 block 发起一次 shared-buffer read；不要把它扩大成“整条语句绝无任何物理 I/O”的证明；
- **dirtied**：表示这条查询把此前未修改的 shared block 标为 dirty；它之后可能由 backend、background writer 或 checkpoint 等路径写出，单凭 `dirtied` 不能断言具体写出者与时刻；
- **written**：表示当前 backend 在该查询处理期间写出了此前已 dirty 的 block；
- **Planning / Execution Time**：必须记录本机实际值；具体数字与计划形状会随数据、版本与环境变化。

---

## 4. 实验 B：MVCC 隔离级别与并发更新冲突实测

在 SQLite 回滚日志架构下，写操作通过互斥锁串行化，第二写者遭遇 `SQLITE_BUSY`。而在 PostgreSQL 的 MVCC 架构下：

### (1) Read Committed 模式下的并发更新
1. **会话 1**：
   ```sql
   BEGIN;
   UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
   -- 保持事务打开，尚未 COMMIT
   ```
2. **会话 2**：
   ```sql
   BEGIN;
   UPDATE accounts SET balance = balance + 50 WHERE id = 'A';
   -- 会话 2 尝试获取行级互斥锁，进入阻塞等待（Wait）
   ```
3. **会话 1** 提交：
   ```sql
   COMMIT;
   ```
4. **会话 2** 表现：
   - 会话 2 被唤醒并检测到行已被会话 1 更新并提交；
   - 在 Read Committed 级别下，会话 2 重新读取该行最新已提交的版本，并在新版本上执行更新；
   - 最终两笔修改均生效。

### (2) Repeatable Read 模式下的快照隔离冲突
1. **会话 1**：
   ```sql
   BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
   UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
   ```
2. **会话 2**：
   ```sql
   BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
   UPDATE accounts SET balance = balance + 50 WHERE id = 'A';
   -- 同样进入行级等待
   ```
3. **会话 1** 提交：
   ```sql
   COMMIT;
   ```
4. **会话 2** 表现：
   - 此时会话 2 **不再静默覆盖**，而是立即报错抛出并发序列化异常：
     ```text
     ERROR: could not serialize access due to concurrent update
     ```
   - **机理剖析**：在 Repeatable Read 快照隔离契约下，会话 2 承诺只能看到其事务开启时的初始快照。但会话 1 的提交修改了目标行，若会话 2 继续更新，就会产生基于过期快照的写冲突。PostgreSQL 主动中止会话 2，要求应用捕获该错误并从事务边界重新开始。

---

## 5. 系统推论边界与总结 (Inference Limits & Summary)

| 维度 | SQLite (Rollback Journal Baseline) | PostgreSQL (MVCC Baseline) |
| :--- | :--- | :--- |
| **并发读者与写者** | 读者可并发读旧页；写者必须独占文件互斥锁 | 读不阻塞写，写不阻塞读；基于元组多版本维护快照 |
| **写冲突时机** | rollback-journal 下只允许一个 writer；竞争可能在写事务启动或 read-to-write 升级时以 busy 类结果暴露，具体等待取决于 busy handler/timeout | 并发更新会等待当前 updater；Read Committed 可在其提交后基于新版本继续，Repeatable Read 则在目标行已被并发更新并提交时中止当前事务并报告 serialization failure |
| **物理 I/O 观察** | EQP 仅报告逻辑 `SCAN` / `SEARCH` 路径 | `EXPLAIN (ANALYZE, BUFFERS)` 报告真实缓冲池命中有脏页数 |
| **核心启示** | 锁与冲突是具名引擎的机制产物，不可把某一种引擎的并发报错外推为所有数据库的通用标准 |

---

## 6. 出处与版权归属 (Provenance & License)

- **PostgreSQL License**: 本指南对 PostgreSQL 官方文档中的查询分析技术进行了教学式归纳，代码与文字完全遵循开源许可。
- **PostgreSQL Documentation**: *Chapter 14: Performance Tips - Using EXPLAIN*, *Chapter 13: Concurrency Control*, PostgreSQL Global Development Group, 2026.
