# Modern Technology Case Map v0.1

Status: **Blueprint v0.1 — Issue #21 draft; READY FOR LEAD REVIEW, not VERIFIED**

本文件回答：

> Essential CS 中哪些现代技术会出现？为什么出现？它们在教授什么不会随产品消失的 stable principle？

它不是“必须掌握的产品清单”，不新增 Stage/Module/DAG/Concept/Lab/P0–P9，也不通过 technology case 静默解决 Open Questions。

Canonical authority / constraints：

- `meta/CURRICULUM_INVARIANTS.md`
- `meta/DECISIONS.md`（尤其 D-008 / D-013 / D-015）
- `meta/CURRICULUM_MAP.md`
- `meta/COMPETENCY_MATRIX.md`
- `meta/OPEN_QUESTIONS.md`
- `meta/TECHNOLOGY_EVALUATION_FRAMEWORK.md`
- `meta/LIVING_CURRICULUM_POLICY.md`
- `meta/RESEARCH_AND_SOURCE_POLICY.md`
- `meta/blueprint/lab-source-selection-map-v0.1.md`
- `meta/blueprint/audit-to-architecture-disposition-v0.1.md`
- `meta/blueprint/final-reconciliation-v0.1.md`

## 1. Reading the map

### 1.1 Technology Admission Test

每个重要 technology case 必须先回答：

1. **What problem does it solve?**
2. **What stable principle is underneath?**
3. **What trade-off does it make?**
4. **Is its use sufficiently real/sustained for this teaching role?**
5. **If the product disappears, is the lesson still useful?**
6. **Is a simpler/classic case pedagogically better?**

Curriculum classification 使用：

- **STABLE CORE MECHANISM**
- **CURRENT CASE**
- **FRONTIER**
- **DEEP DIVE**
- **REJECT / NOT CORE**

Living Curriculum time class 使用：

- **STABLE**
- **CURRENT**
- **FRONTIER**

这两套标签回答不同问题：

- **Curriculum classification**：它在课程中承担什么 pedagogical role？
- **Time class**：关于它的事实多久需要重检？

因此，一个技术可以是 `CURRENT CASE + CURRENT`；一个协议可以是 `STABLE CORE MECHANISM + STABLE`；一个被排除的快速变化领域也可以是 `REJECT / NOT CORE + FRONTIER`。

### 1.2 Core mechanism ≠ Core product

反复使用以下边界：

> **Core 可以包含技术机制，而不把某个产品变成 Core prerequisite。**

例：

- relational query planning / transactions = stable Core mechanism；
- SQLite = Required teaching implementation / baseline；
- PostgreSQL = Optional / Current comparison；
- cache validity = stable mechanism；
- Redis = replaceable Current Case；
- process/container isolation = stable Core mechanism；
- Docker = replaceable Current Case；
- orchestration/control-loop concepts 可作为 bounded case；
- Kubernetes product administration 不成为 Core；
- observability signals = stable Core mechanism；
- OpenTelemetry / Prometheus / Grafana = Current Cases；
- consensus concept = Core；
- full Raft/Paxos implementation = Deep Dive。

### 1.3 Technology Card fields

Module-level Research Dossier 若采用某个重要 case，应扩展为完整 Technology Card：

`Problem → Constraints → Core Mechanism → Gains → Costs → Failure Modes → Alternatives → When NOT to use → Scale Threshold → Evidence → Evolution → Stable Principle`

本 map 只保留足以约束 admission 的 compact fields；它不替代后续 Module research。

## 2. Technology Case Map

表中 `Canonical home` 只引用现有 Module/Lab/Project home；它不创建新的依赖或 first-introduction。

| Technology / family | Problem | Stable principle | Canonical home | Teaching role | Curriculum classification | Time class | Why included | Product-neutral boundary | When NOT to use | Evidence expectation | Review cadence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SQLite | 单节点持久状态、SQL 查询/事务 | 声明式查询；索引/页访问；transaction/invariant；durability boundary | M13/M14；LAB-REQ-04/05；P0/P4/P5/P6 | Required teaching implementation / mechanism baseline | STABLE CORE MECHANISM | STABLE | 以真实、低运维负担引擎暴露 query plan、index、transaction、recovery | Core 是关系机制与证据；不要求 SQLite 产品熟练度 | 当任务只需内存/文件机制，或约束明确要求 server/distributed DB 时 | 记录版本、schema/workload、plan、result equivalence、transaction timeline、recovery limits | 18–24 个月或 planner/transaction 行为重大变化；Lab 持续 smoke test |
| PostgreSQL | server DB、并发客户端、MVCC/更丰富 planner/isolation 对照 | 同一关系/transaction 原理在不同实现中的取舍 | M13/M14；LAB-OPT-03；EXP-02 | Optional comparison | CURRENT CASE | CURRENT | 对照 SQLite，观察 server/MVCC/EXPLAIN/isolation 的实现差异 | 不得替代 Required SQLite baseline；不得变成 DBA/product training | 没有明确并发/server/MVCC 教学约束时 | current official docs + local bounded comparison；记录 version/config/workload | 6–12 个月；实现/版本行为变化时 |
| Redis / in-memory key-value systems | 低延迟内存数据、cache、计数、stream 等 | state placement；cache validity；persistence/replication trade-off；data-structure semantics | M13/M18/M23；P9 scenario only | Replaceable comparison / constrained case | CURRENT CASE | CURRENT | 可展示内存状态、cache/stream/persistence 的取舍，但不是默认答案 | Redis 命令、模块、集群形态不是 Core；先教 stable mechanism | 无测得 latency/cache 问题、无异步/stream 约束、不能接受其 failure/durability model 时 | official docs + workload/failure evidence；必须说明 persistence/replication limits | 6–12 个月 |
| Distributed SQL / managed database examples | 单节点限制、复制、全球/托管运维约束 | replication/consistency/partitioning；managed service moves operations, not physics | M17/M19/M23/M24 | Architecture comparison only | CURRENT CASE | CURRENT | 用于回答“何时单节点不够”与 managed abstraction 的复杂性转移 | 任何具体 vendor/API/feature 都可替换；不成为 cloud account prerequisite | 单节点 DB 已满足 workload/failure/cost 时 | official architecture/consistency docs + explicit constraint/cost model | 6–12 个月 |
| HTTP/1.1 | 应用层 request/response、intermediary、cache semantics | HTTP semantics、message framing、connection reuse、cache/interface contracts | M11；LAB-REQ-01；P1/P3 | Protocol mechanism baseline | STABLE CORE MECHANISM | STABLE | 是可观察的 Web/interface baseline，便于解释代理、cache 与 failure | 不训练某 server/client 产品；语义与 wire implementation 分开 | 非 HTTP 系统或更简单 local interface 足够时 | RFC 9110/9112 + packet/request trace | 18–24 个月或 RFC 重大更新 |
| HTTP/2 | 同一 HTTP semantics 下减少多连接与应用层 HOL 等成本 | multiplexed streams、header compression、flow control；semantics 与 transport expression 分离 | M11/M12 | Modern protocol comparison | STABLE CORE MECHANISM | STABLE | 展示“同一语义，不同 transport expression”的演化 | 不要求调优具体浏览器/server H2 stack | 没有并发请求/协议比较目标时 | RFC 9113 + DevTools/trace 对照；避免把一次 benchmark 当原因 | 18–24 个月或规范重大更新 |
| HTTP/3 | 在 QUIC 上表达 HTTP，改变 connection/stream failure 与 handshake cost | HTTP semantics 与 transport 解耦；QUIC stream multiplexing | M10/M11/M12 | Modern protocol case | STABLE CORE MECHANISM | STABLE | 把 HTTP evolution 与 QUIC/TLS/UDP 连接起来 | 不把 browser/vendor H3 implementation 当 timeless fact | 只需要 HTTP semantics、无 transport comparison 目标时 | RFC 9114 + RFC 9000；current implementation claims 单独标 CURRENT | 18–24 个月；implementation claim 6–12 个月复核 |
| TCP | 可靠有序 byte stream | sequencing、retransmission、flow/congestion interaction、connection state | M10 | Transport baseline | STABLE CORE MECHANISM | STABLE | 是 request path、timeout/partial failure 推理的基础 | 不要求实现完整 TCP stack | 不需要可靠 byte-stream abstraction 的协议场景 | RFC 9293 + socket/packet evidence | 18–24 个月或规范重大更新 |
| UDP | datagram transport、最小传输服务 | message boundary、best-effort datagram、application responsibility | M10 | Contrast mechanism | STABLE CORE MECHANISM | STABLE | 与 TCP/QUIC 对照责任边界 | 不把“UDP=不可靠所以简单”当完整模型 | 应用需要可靠 byte stream 且无自定义协议理由时 | RFC 768/相关现行更新 + packet observation | 18–24 个月 |
| QUIC | 在 UDP 上提供安全、多路复用 transport，减少跨-stream HOL 等限制 | user-space transport、streams、loss recovery、integrated TLS security | M10/M11 | Modern transport mechanism | STABLE CORE MECHANISM | STABLE | 解释 HTTP/3 与 transport evolution，不以“更新=更好”叙述 | 不训练某 QUIC library；实现优化属于 CURRENT | 没有 transport-evolution/stream failure 教学问题时 | RFC 9000 + related QUIC RFCs；trace current implementation separately | 18–24 个月；实现细节 6–12 个月 |
| TLS | 不可信网络上的机密性、完整性与 peer authentication | authenticated key establishment、certificates/trust roots、record protection | M11/M21 | Security/network mechanism | STABLE CORE MECHANISM | STABLE | 连接 network path、trust boundary 与 certificate evidence | 不训练 CA/vendor dashboard；不把 TLS 等同于整体应用安全 | local isolated demo 无需真实 TLS，或 threat model 不要求时 | RFC 8446 + certificate/handshake observation | 18–24 个月或规范/BCP 重大变化 |
| DNS | 名称到资源/地址的分布式解析 | hierarchical naming、delegation、caching、TTL、failure/consistency boundaries | M10 | Naming mechanism | STABLE CORE MECHANISM | STABLE | 解释 request path 中 name resolution、cache 与 failure | 不训练某 DNS provider console | 固定本地地址且名称解析不是问题时 | DNS RFCs + bounded resolver observation | 18–24 个月；resolver/provider practice 6–12 个月 |
| Reverse proxy / load balancer / CDN | 入口路由、policy、流量分配、内容复用/就近交付 | intermediary、indirection、cache validity、failure/trust boundary、load distribution | M11/M19/M23；P9 optional | Mechanism family; optional case | STABLE CORE MECHANISM | STABLE | 展示 abstraction 如何改变 path/state/trust/failure 位置 | Nginx/Envoy/CDN vendor 配置可替换；proxy 不成为 project prerequisite | 直接 origin 足够、无 routing/cache/policy/availability 约束时 | request trace + headers/cache/failure evidence + constraint threshold | 18–24 个月；具体产品 6–12 个月 |
| Chromium / Firefox browser architecture | 不可信内容、并行页面、渲染与多 subsystem 集成 | process isolation、event loop/render pipeline、origin/security boundaries | M12；EXP-03 | Integrated real-system case | STABLE CORE MECHANISM | STABLE | 浏览器是跨 OS/network/runtime/security 的真实综合案例 | Chromium/Firefox 只是可替换实现；不教 browser product mastery | 若问题仅是 HTTP 或 JS 语法，避免引入完整 browser complexity | official architecture/source docs + DevTools/process observation | 18–24 个月；implementation details 6–12 个月 |
| V8 / SpiderMonkey | JavaScript 执行、优化、GC 的真实 runtime | bytecode/VM/JIT/GC、dynamic optimization、runtime representation | M05/M12 | Runtime implementation case | CURRENT CASE | CURRENT | 把 VM/JIT/GC stable mechanism 落到真实 runtime | 具体 tier 名称/优化 pipeline 不成为 Core fact | 无需 runtime implementation 对照时 | official engine docs/source + version-scoped observation | 6–12 个月 |
| Browser DevTools | 观察 request、render、runtime、storage | instrumentation exposes hidden mechanisms; observation ≠ explanation | M11/M12/M20 | Observation tool | CURRENT CASE | CURRENT | 为真实 browser mechanism 提供低门槛 evidence | UI layout/按钮位置不是学习目标；工具可替换 | CLI/trace 已更直接回答问题时 | 保存 observation + browser/version + claim limits | 6–12 个月 |
| Python | 低认知负担实现 Labs/project | source→runtime、objects/state、library abstraction | D-008 baseline；跨 Modules | Canonical lab language, not a PL certification | CURRENT CASE | CURRENT | 作为主要实验语言降低 incidental load | 语法/框架不是 Core；机制可用 C/JS/SQL/Shell 对照 | 当低层 representation/syscall/atomics 需要更直接语言时 | official docs + actual runtime/tool evidence where behavior matters | 6–12 个月；exact version 留给 OQ-BP-006 |
| C | 暴露 memory、ABI、syscall、threads/atomics | explicit memory representation、ABI/interface、low-level concurrency | M03/M06/M15；LAB-REQ-03 | Mechanism-revealing language case | CURRENT CASE | CURRENT | 在低层边界减少 runtime 隐藏 | 不变成 C programming course；避免 undefined behavior 作为教学捷径 | 高层机制可由 Python/SQL 更清楚表达时 | standard/toolchain docs + defined-behavior experiment | 6–12 个月；exact compiler/version 不 pin |
| Rust ownership / concurrency | 用 type/ownership 约束 aliasing 与并发错误 | ownership/aliasing invariants；compile-time enforcement；Send/Sync boundaries | M05/M15/M23 | Comparative language case | CURRENT CASE | CURRENT | 展示 language design 如何移动 correctness burden | 不把 Rust 语法/生态变成 prerequisite；不是 lock-free specialization | 如果 ownership 机制不比更简单 C/Python 对照增加理解时 | official Rust Book/reference + small bounded comparison | 6–12 个月 |
| Java / JVM | managed runtime、bytecode、GC/JIT 的成熟案例 | VM abstraction、bytecode、GC、JIT、runtime profiling | M05 | Comparative runtime case | CURRENT CASE | CURRENT | 提供与 Python/JS/C 不同的 runtime boundary | 不训练 Java framework；具体 collector/JIT flags 非 Core | 已有更简单 runtime case 足够时 | official JVM/spec/docs；version-scoped implementation details | 6–12 个月 |
