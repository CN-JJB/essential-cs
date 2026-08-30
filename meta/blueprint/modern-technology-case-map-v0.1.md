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
| JavaScript | browser/runtime boundary 与 event-driven execution | event loop、async callbacks/promises、dynamic runtime、browser interface | M05/M12/M15 | Web/runtime language case | CURRENT CASE | CURRENT | 连接 browser integrated case 与 async/runtime | 不变成前端开发课；framework 不入 Core | 非 browser/async 问题时 | spec/official docs + DevTools observation | 6–12 个月 |
| Bytecode / VM / JIT / GC | 在可移植性、启动、吞吐、memory safety 间做 runtime trade-off | intermediate representation、dynamic compilation、memory reclamation | M05 | Stable runtime mechanism family | STABLE CORE MECHANISM | STABLE | 即使具体语言消失仍保留 runtime world model | 具体 VM tier/collector 名称只是 case | 无需解释 managed runtime 行为时 | spec/docs/source for chosen case + mechanism trace | 18–24 个月 |
| Linux | canonical systems execution environment | process/syscall/VM/files/network/resource controls are observable OS mechanisms | D-008；M03/M06–M10/M15/M19/M20 | Canonical environment, not certification | CURRENT CASE | CURRENT | 提供一致且真实的 systems surface | 不教 Linux administration；发行版/命令细节不是课程目标 | 机制在更小 teaching OS/portable API 更清楚时 | kernel/man-page/tool output + environment record | 6–12 个月；exact base/version 由 OQ-BP-006 |
| xv6 | 以小型真实内核暴露 syscall/source route | user/kernel boundary、dispatch、process/filesystem mechanisms | M06；LAB-REQ-02；EXP-01 | Bounded teaching/source case | CURRENT CASE | CURRENT | 真实源码足够小，可做 Source Expedition 与 syscall trace | 不是 OS curriculum 本体；不做 full kernel implementation in Core | 若 Linux observation 已足够且源码路径不增加理解时 | checked source revision + bounded route + stop point | 6–12 个月；pin 留给 Lab dossier |
| x86-64 / ARM / RISC-V; QEMU | 观察 ISA/ABI 与真实 machine execution | ISA abstraction、registers/instructions/calls/memory；emulation as controlled environment | M03/M04；LAB-REQ-02 uses RISC-V/QEMU | Representative ISA/emulator cases | CURRENT CASE | CURRENT | 多 ISA 防止把一个 encoding 当计算本身；QEMU 提供可复现 case | 不要求三种 ISA mastery；QEMU 不是硬件现实的全部 | 一个 ISA 已能清楚证明目标时，不为 breadth 增负担 | ISA manuals + disassembly/emulator record | 6–12 个月；exact toolchain 由 OQ-BP-006 |
| pthreads / C11 atomics | 共享内存并发、同步、进度 | interleaving、atomicity、happens-before/synchronization、invariant | M15；LAB-REQ-03 | Required concurrency mechanism surface | STABLE CORE MECHANISM | STABLE | 用 defined behavior 观察 race-like lost update 与 repair | 不进入 lock-free specialization；不使用 UB data race 作 canonical evidence | async/DB isolation 更适合目标问题时 | C/POSIX specs/toolchain + repeatable interleaving evidence | 18–24 个月；toolchain current behavior 6–12 |
| Async / event loop | 大量等待型工作下避免 thread-per-waiting-work 的某些成本 | cooperative scheduling、callbacks/futures、backpressure、state machine | M15/M16/M20 | Concurrency model | STABLE CORE MECHANISM | STABLE | 与 threads 对照 responsibility/failure/cancellation | 不把 async framework syntax 当机制 | 并发度低、阻塞模型更简单可靠时 | runtime docs + timeline/queue/backpressure observation | 18–24 个月 |
| Database isolation | 并发 transaction 保持 application invariants | serialization/isolation levels、anomalies、retry/conflict handling | M14；LAB-REQ-05；P5 | Correctness mechanism | STABLE CORE MECHANISM | STABLE | 把并发 correctness 与 DB guarantees 接起来 | 不等同于“ACID 记忆”；实现差异用 SQLite/PostgreSQL case | 无并发 state 或 invariant 时 | transaction timeline + official DB semantics + invariant | 18–24 个月；implementation case 6–12 |
| Consensus concept; Raft/Paxos as cases | 多副本在 failure/partition 下对决定/日志达成一致 | quorum、leader/election/log agreement、safety/liveness trade-offs | M17；EXP-05；M23/M24 | Core concept with bounded worked cases | STABLE CORE MECHANISM | STABLE | accepted boundary: learner must know what consensus buys/costs | Raft/Paxos 名称/implementation 非 prerequisite；概念可换案例 | 单节点或不需要共同决定/strong coordination 时 | paper/spec/trace + partition scenario + guarantee/cost judgment | 18–24 个月 |
| Full Raft/Paxos implementation | 完整实现 election/log replication/reconfiguration | 同上，但实现 breadth 大、debug surface 高 | Deep Dive after M17 | Specialization | DEEP DIVE | STABLE | 可提供深度，但不应消耗 shared Core traversal | 不能反向成为理解 consensus 的先修 | 只需概念/判断，不需要构建 protocol engine 时 | paper + implementation tests/model checking as Deep Dive | 18–24 个月 |
| Leader/follower replication + quorum systems | 提高 availability/read locality/durability，协调多副本 | replication lag、quorum intersection、failover、stale/conflicting state | M17/M23/M24 | Core distributed mechanism | STABLE CORE MECHANISM | STABLE | 直接支撑 consistency/availability/cost 判断 | 具体 DB/broker implementation 可替换 | 单副本 failure model 已足够，或复制成本大于收益时 | scenario trace + failure assumptions + state/lag evidence | 18–24 个月 |
| Kafka / RabbitMQ / Redis Streams / cloud queues | 异步 handoff、buffering、durable work、producer/consumer decoupling | queue/log、ack/ownership transfer、delivery semantics、ordering/backpressure | M18；P9 scenario | Replaceable messaging cases | CURRENT CASE | CURRENT | 用于比较 sync call / durable job table / broker，不暗设产品先修 | 任何 broker/vendor API 都可替换；先教 delivery semantics | 工作可同步完成、无 durability/backpressure/decoupling need 时 | official semantics docs + duplicate/order/failure evidence + simpler alternative | 6–12 个月 |
| Container / OCI-style image/runtime concepts | 可复现 packaging、process isolation/resource boundary | process isolation、namespaces/cgroups、image/artifact、shared-kernel boundary | M19；P7 optional comparison | Core mechanism family | STABLE CORE MECHANISM | STABLE | stable concept survives Docker/Kubernetes changes | Core 不要求 Docker command set；image ≠ running process ≠ VM | native process/script 已充分可复现且 container 会遮蔽 OS 机制时 | OCI specs + process/mount/resource observation | 18–24 个月 |
| Docker | 易用 container/image build/run implementation | container runtime/image workflow over stable OS/OCI mechanisms | M19；P7 optional | Replaceable implementation case | CURRENT CASE | CURRENT | 可用来观察 stable container boundary，但不成为课程身份 | Dockerfile/CLI/Compose mastery 不进 Core | native/OCI-level case 更简单，或环境负担过大时 | official docs + compare native/container processes/state | 6–12 个月 |
| Virtual machines | 隔离 guest OS/kernel 与资源 | hardware virtualization、guest kernel boundary、image/snapshot/resource trade-offs | M19; revisit M07 | Contrast to containers | STABLE CORE MECHANISM | STABLE | 解释 container vs VM 的 isolation/dependency boundary | 不训练 hypervisor administration | 无需 guest-kernel isolation/不同 OS 时 | architecture docs + bounded process/kernel/state comparison | 18–24 个月 |
| Kubernetes | 多主机 container workload orchestration、desired state、scheduling/recovery | control loop、desired vs observed state、scheduling、service discovery、resource management | M19/M23; optional case only | Bounded orchestration case; admin depth excluded | CURRENT CASE | CURRENT | 现实中可用于解释 orchestration complexity，但不是“现代性”徽章 | Kubernetes commands/resources/operator ecosystem 不成为 Core prerequisite；admin track = Deep Dive | 单主机/少量进程、无 orchestration problem、team ops capacity 不匹配时 | official concepts docs + explicit orchestration constraint + simpler alternative | 6–12 个月 |
| Commercial cloud compute/storage/database primitives | 按需资源、managed boundaries、elastic billing | virtualized resource abstraction、durability/availability contracts、shared responsibility、cost metering | M19/M23/M24 | Vendor-neutral reality cases | CURRENT CASE | CURRENT | 让 cost/operational responsibility 接触现实而不做 vendor syllabus | AWS/Azure/GCP 等 API/name 可替换；不得要求付费账号 | local/single-node case 已满足教学目标，或 vendor setup 超过收益时 | official service architecture/SLA/pricing only when needed + cost assumptions | 6–12 个月 |
| Structured logs / metrics / traces | 知道系统发生了什么、在哪里变慢/失败 | signals answer different questions; correlation/context; sampling/cardinality/missingness | M20；P8/M24 | Core observability mechanisms | STABLE CORE MECHANISM | STABLE | 先教 signal/mechanism/judgment，再接工具 | dashboard/product 不是 observability 本身 | 问题可由直接 local observation 回答时不堆 telemetry | question→signal→observation→limit；privacy/redaction/overhead evidence | 18–24 个月 |
| OpenTelemetry | vendor-neutral instrumentation/telemetry model | context propagation、spans/traces/metrics/logs、instrument/export separation | M20；LAB-OPT-04；EXP-04 | Optional/current implementation case | CURRENT CASE | CURRENT | 为 stable observability concepts 提供可替换标准化 case | 不要求 collector/backend stack；OTel API version 不是 timeless curriculum | structured local logs/timers 已足够时 | official spec/docs + local bounded trace; record version/overhead/missingness | 6–12 个月 |
| Prometheus / Grafana-style / vendor observability stacks | 时序指标存储、查询、可视化、告警/分析 | time-series model、labels/cardinality、aggregation、visualization ≠ causality | M20/M23 | Comparison cases | CURRENT CASE | CURRENT | 展示 backend choices 与 cardinality/retention/ops cost | PromQL/dashboard/vendor UX 不成为 Core requirement | 没有持续 metrics/retention/query need 时 | official docs + bounded signal question + cost/cardinality limit | 6–12 个月 |
| Git | 版本化 source/evidence、可审计 change history | content/history graph、diff/provenance、reproducible change boundary | M00 L00-02；Bridge support | Canonical evidence tool | CURRENT CASE | CURRENT | 支持课程 evidence workflow 与安全恢复 | 不教 Git internals/advanced workflow 作为 Core | 简单临时练习不需要历史时仍可最小使用，不做 workflow bureaucracy | status/diff/commit/history evidence；actual version only as environment metadata | 6–12 个月；tool semantics stable but workflow can evolve |
| GitHub | 共享 repository、Issue/PR/review/CI hosting | collaboration/review/provenance concepts independent of hosting product | Project governance / learner workflow context | Current collaboration case | CURRENT CASE | CURRENT | 项目本身使用 GitHub，但学习目标是可审查协作与 evidence | GitHub UI/features 不成为 CS competency | 离线/local Git 足以完成机制目标时 | official docs only for current workflow behavior | 6–12 个月 |
| Make / build systems | 从 source/dependencies 生成 artifacts | dependency graph、incremental rebuild、deterministic/reproducible build | M00/M05/M19 | Build mechanism case | CURRENT CASE | CURRENT | 用成熟工具暴露 build dependency，而非 workflow bureaucracy | Make syntax 不是 Core；可换 Ninja/CMake/language build tool | 单文件/单命令构建且 dependency graph 不构成问题时 | official manual + input→artifact dependency evidence | 6–12 个月 |
| Lockfiles / package managers / language registries | 解析/固定依赖、获取 artifacts、复现环境 | dependency graph、version constraint、integrity/provenance、supply-chain boundary | M00/M19/M21/M23 | Current tooling family | CURRENT CASE | CURRENT | 连接 reproducibility 与 supply-chain trust | npm/pip/cargo registry 命令可替换；不把 package workflow 当 Core topic | 无外部依赖或固定 vendored fixture 时 | official format/docs + resolved dependency/provenance evidence | 6–12 个月 |
| GitHub Actions / CI | 自动重复 build/test/check | automation as executable evidence gate; environment reproducibility; fail-fast feedback | M19；repo production workflow | CI current case | CURRENT CASE | CURRENT | 具体实现可展示 machine-checkable boundary | Actions YAML/marketplace mastery 不进 Core；可替换其他 CI | 手工一次性实验、无 repeated check need 时 | official docs + reproducible workflow/smoke output; reasoning still reviewer-required | 6–12 个月 |
| OLTP vs OLAP; row vs column; batch vs stream; warehouse/lake; ETL/ELT | 不同 workload/data lifecycle 需要不同 layout/processing | workload shapes storage/layout/execution; derived data/provenance; latency vs throughput trade-offs | M13/M18/M23 | Moderate Core data/analytics framing | STABLE CORE MECHANISM | STABLE | 形成现代 data-system world model但不扩成 Data Engineering course | 概念先于平台；不要求构建 lakehouse/streaming platform | 没有 analytical/derived-data workload 时不引入额外 pipeline | workload + data path + latency/freshness/cost + provenance; simpler alternative | 18–24 个月 |
| DuckDB / ClickHouse | 列式分析、本地或 server OLAP | columnar layout、vectorized/scan-heavy execution、compression/locality trade-offs | M13/M23 optional comparison | Analytical engine cases | CURRENT CASE | CURRENT | 用具体引擎对照 row-oriented OLTP baseline | 不要求命令/部署；任一 case 可替换 | 数据规模/查询形态不需要 analytical engine 时 | official docs + representative scan/aggregation workload + row/column explanation | 6–12 个月 |
| Apache Spark | 大规模 batch/stream distributed processing | partitioned computation、shuffle、fault recovery、batch/stream trade-offs | M18/M23 Deep-Dive-adjacent case | Current analytics case, not a Core platform | CURRENT CASE | CURRENT | 可用于说明何时单机分析不够，但不把 Core 变成 Spark 课 | Spark API/cluster ops 不成为 prerequisite | 单机 SQL/DuckDB/DB 已满足数据量与时限时 | official docs + explicit scale/partition/shuffle constraint | 6–12 个月 |
| BigQuery / Snowflake | managed analytical warehouse、separate/elastic compute/storage 等产品 abstraction | columnar/MPP analytics、managed operations、resource metering/cost | M19/M23/M24 optional case | Commercial current cases | CURRENT CASE | CURRENT | 展示 managed analytics 如何移动运维与成本责任 | 具体 vendor feature/SQL extension/account 不成为 Core | local/open analytical engine 已回答问题，或无 warehouse-scale constraint 时 | official architecture/pricing docs when used + workload/cost assumptions | 6–12 个月 |
| AI-generated claim/code/config verification practice | 开发中会遇到生成式输出，但其正确性未知 | untrusted hypothesis → source/test/measurement/security verification | M00 L00-02；M23 L23-02 per OQ-BP-001 safe interim | Verification practice only | CURRENT CASE | CURRENT | 已接受的 current-practice 边界；强化 evidence discipline | 不把 AI fluency、prompt skill 或 model knowledge当 competency | 任务无需 AI 时无需引入；任何生成结果都不能替代证据 | 保留 generated claim 与 independent authoritative/test evidence；标 uncertainty | 6–12 个月 |
| LLM architecture / transformer theory / prompt engineering / AI app development | 快速变化的 AI 系统与应用方法 | —；**不由本 map 决定 stable Core principle** | None; OQ-BP-001 | Excluded pending RFC/Decision | REJECT / NOT CORE | FRONTIER | OQ-BP-001 未决；本 map 无权把它们静默纳入 Core | 不得通过 technology case 侧门建立 AI Core track | 除未来 RFC 明确改变 scope 外，不进入 Core | 若研究 OQ，只用 current primary/paper evidence；本 v0.1 无 assessment claim | 3–6 个月仅用于 OQ/frontier reassessment |
| HCI / accessibility product or browser-feature training | human-facing feedback/accessibility/consent/recovery | —；existing P2/P9 evidence hooks 不等于 settled Core track | P2/P9 hooks only; OQ-BP-003 | Excluded from admission by this map | REJECT / NOT CORE | STABLE | OQ-BP-003 未决；browser case 不能静默扩张 HCI Core | 保留现有 evidence hooks；任何新增 canonical HCI content 需 RFC/Decision | 除 existing hooks 或未来 RFC 决定外，不扩展 | 若未来评估 OQ，使用 standards/primary accessibility evidence；本 map 不创建 rubric | 18–24 个月或 OQ 状态变化 |

## 3. Classification summary

本 v0.1 map 共记录 **52** 个 technology cases / families：

| Curriculum classification | Count | Interpretation |
|---|---:|---|
| STABLE CORE MECHANISM | 21 | 机制/协议/模型属于 shared world model；具体实现仍可替换 |
| CURRENT CASE | 28 | 现实、持续使用且有教学价值的实现/产品案例；必须定期复核 |
| FRONTIER | 0 | 本版本没有把任何 fast-moving product case 直接纳入 curriculum role |
| DEEP DIVE | 1 | full consensus implementation；不进入 shared Core traversal |
| REJECT / NOT CORE | 2 | LLM/prompt/AI-app track 与 HCI/accessibility product track 均不得由本 map 静默入 Core |

Time class 为：**23 STABLE / 28 CURRENT / 1 FRONTIER**。这里唯一 `FRONTIER` time-class row 是被排除的 LLM/prompt/AI-app family；这不等于 curriculum classification `FRONTIER` admission。

## 4. Family-level boundaries

### 4.1 Data / databases

Accepted boundary 保持：

- **SQLite remains the Required mechanism baseline** for M13/M14 database Labs；
- **PostgreSQL remains Optional / Current comparison**；
- Redis / in-memory KV、distributed SQL、managed DB 可以出现为 constrained cases，但都不是 hidden prerequisite；
- learner 先证明 workload/invariant/failure/cost constraint，再讨论 server DB、cache、replica 或 distributed DB；
- `EXPLAIN`/query-plan output 属 implementation evidence，不应当作跨版本固定字符串；
- database choice 必须能回答：“为什么简单单节点方案不够？”

Scale Threshold 采用**约束阈值**而非伪造 universal number：

- cache：先有 measured repeated-read latency/bandwidth problem 与 staleness policy；
- replica：先有 availability/read-locality/failure constraint；
- distributed DB：先证明 single-node limit 或 availability/geography constraint；
- server DB：先有 concurrent/server-managed state 或具体 workload reason。

### 4.2 Networking / Web

稳定教学对象是 protocol semantics、transport、name resolution、security、intermediary/failure boundary。

Evolution lens：

- HTTP/1.1 multi-connection/pipelining limits → HTTP/2 multiplexed streams → fewer application-layer concurrency costs，但引入 framing/flow-control state；
- TCP-based HTTP transport constraints → QUIC over UDP + HTTP/3 → stream/failure/handshake behavior 改变，同时把更多 transport complexity 移到 QUIC implementation；
- plain HTTP → TLS-protected HTTP → confidentiality/integrity/authentication gains，同时引入 certificate/trust/handshake/operations；
- direct origin → reverse proxy / load balancer / CDN → routing/cache/policy/distribution gains，同时增加 intermediary state、trust、failure 与 cache correctness。

“新协议”不自动比旧协议更好；选择取决于 compatibility、network path、implementation maturity、operational constraints 与 measurement。

### 4.3 Browser

M12 教 browser as integrated system：

- process model；
- renderer/browser boundary；
- origin/site isolation；
- event/render/request path；
- runtime/GC/JIT as supporting mechanism；
- DevTools as observation surface。

Chromium / Firefox / V8 / SpiderMonkey 是**现实案例**，不是 browser-product syllabus。UI、菜单、具体 optimization tier、release-specific process policy 都不能写成 timeless Core fact。

**OQ-BP-003 remains unresolved.** Browser case 不得借“现代浏览器”之名新增 HCI/accessibility Core track。已接受 P2/P9 evidence hooks 可以继续存在，但本 map 不扩大它们。

### 4.4 PL / runtime

Stable layer：

- source → representation → runtime → machine；
- bytecode / VM；
- JIT；
- GC；
- type/ownership/invariant；
- event loop / async execution。

Case layer：

- Python 是 canonical main lab language；
- C 用于暴露 low-level memory/syscall/concurrency；
- Rust 用于 ownership/concurrency comparison；
- Java/JVM 用于 managed runtime comparison；
- JavaScript/V8/SpiderMonkey 用于 browser/runtime integration。

课程不以语言 syntax breadth、framework、package ecosystem mastery 作为目标。

### 4.5 OS / machine

- Linux = canonical real systems environment，不是 Linux administration certification；
- xv6 = bounded mechanism/source case，不是 OS curriculum 本体；
- x86-64 / ARM / RISC-V = representative ISA cases；不要求多 ISA mastery；
- QEMU = reproducibility/emulation case；不等于 physical hardware behavior 的全部。

OQ-BP-006 继续拥有 exact Linux/base image/compiler/QEMU/RISC-V/Python/DB/browser/tool versions；本 map **不 pin 具体版本**。

### 4.6 Concurrency

Core 保持在可迁移机制：

- interleaving；
- atomicity；
- synchronization；
- invariant；
- progress/deadlock boundary；
- async/event-loop；
- database isolation / serialization。

LAB-REQ-03 继续使用 POSIX threads + C11 atomics 的 **defined behavior** 路径。Rust ownership 是 comparison case；课程不变成 lock-free / memory-model specialization。

### 4.7 Distributed systems

Accepted boundary：

> **Consensus concept is Core; full consensus implementation is Deep Dive.**

Core 要 learner 能解释：

- partial failure / ambiguity；
- leader/follower replication；
- quorum / agreement 的基本作用；
- consistency / availability / latency / cost trade-off；
- duplicate/order/delivery semantics；
- when coordination is unnecessary。

Raft/Paxos 是可替换案例；Kafka/RabbitMQ/Redis Streams/cloud queues 是可替换 messaging cases。它们不得变成 M18/P9 的强制组件。

Queue 的 scale threshold 不是“到多少 QPS”，而是：

- work duration 与 request latency budget 冲突；
- producer/consumer rates 需要 buffering/backpressure；
- work 必须 durable/retryable；
- asynchronous ownership transfer 的 semantics 值得额外 state/operator complexity。

### 4.8 Infrastructure

Stable concepts：

- artifact vs process；
- isolation；
- image/config/state/resource boundary；
- reproducibility；
- deployment；
- desired/observed state & control loop（bounded）；
- cost/resource economics；
- supply-chain/provenance。

Case layer：

- OCI specifications help keep container teaching product-neutral；
- Docker = optional Current Case；
- Kubernetes = Current Case only when orchestration constraint is explicit；administration breadth is Deep Dive/job-specific；
- commercial cloud primitives = Current Cases used for responsibility/cost/managed-boundary judgment。

Scale threshold examples：

- container before Docker: ask whether reproducibility/isolation problem exists；
- Kubernetes before orchestration: ask whether multiple deployable workloads, scheduling/reconciliation, failure recovery and operational team constraints justify a cluster control plane；
- cloud managed service before vendor account: ask whether managed boundary teaches something not visible in local/open case。

### 4.9 Observability

Core 顺序：

`Question → choose signal → instrument/observe → correlate → state missingness/overhead/privacy → explain cautiously`

而不是：

`buy dashboard → search graph → declare cause`

Stable Core teaches structured logs / metrics / traces and correlation. OpenTelemetry、Prometheus/Grafana、vendor stacks 只作为 Current Cases。P8 仍坚持 local structured logs/timers first；不需要 backend 才能获得合格 evidence。

### 4.10 Build / package / source

Core concern 是：

- dependency graph；
- reproducible artifact；
- provenance；
- version constraint；
- integrity；
- reviewable change；
- automated evidence gates。

Git、GitHub、Make、package managers、registries、GitHub Actions 都只是实现/case。不要把 M00/M19 变成 workflow bureaucracy 或 vendor CI training。

### 4.11 Data / analytics

Accepted Core scope 保持**moderate**：

- OLTP vs OLAP；
- row vs column；
- batch vs stream；
- warehouse/lake；
- ETL/ELT；
- derived data / provenance；
- workload → layout/execution/cost judgment。

DuckDB/ClickHouse/Spark/BigQuery/Snowflake/Kafka 可作为 cases，但本课程不是 Data Engineering platform course。

Evolution lens：

`row-oriented OLTP baseline → analytical scan/aggregation constraint → columnar/vectorized or distributed/managed analytical abstraction → throughput/compression/scale gains → new freshness, shuffle, operations, vendor/cost complexity`

优先使用更简单、可本地观察的 case；只有 constraint 要求时才升级到 distributed/managed example。

## 5. AI / LLM boundary

**OQ-BP-001 remains unresolved.**

本 map 只承认已经 safe 的 current-practice statement：

> **AI-generated claim/code/configuration is an untrusted hypothesis requiring verification.**

因此：

- AI-generated output verification = **CURRENT CASE / verification practice**；
- LLM architecture = **not admitted**；
- transformer theory = **not admitted**；
- prompt engineering = **not admitted**；
- AI app development = **not admitted**；
- 本 map 不为它们创建 competency、Concept ID、Module home 或 Core requirement。

如果未来 OQ-BP-001 通过 RFC/Decision 改变 scope，再更新本 map；不能反过来用本 map 预先决定 RFC。

## 6. HCI / accessibility boundary

**OQ-BP-003 remains unresolved.**

- existing P2 denial/error/privacy interaction hooks 保留；
- existing P9 affected-user/accessibility/consent/recovery hooks 保留；
- browser/product cases 不新增 canonical HCI/accessibility teaching track；
- 若 OQ-BP-003 未来被决定，再通过 architecture task 更新，而不是在 M12/product case 中顺手扩 scope。

## 7. Technology Evolution Lens

重要 case 应明确：

`old approach → limitation → new abstraction → gains → new costs`

代表性 lens：

| Evolution | Limitation addressed | Gains | New costs / moved complexity |
|---|---|---|---|
| process → VM / container | environment/isolation/reproducibility boundary | stronger/repeatable execution boundary | image/runtime/guest/host dependency、state confusion、ops |
