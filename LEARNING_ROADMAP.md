# Essential CS — Resource-First Learning Roadmap

Checked: **2026-09-12**

这是 Essential CS v1.0 的默认学习入口。目标不是把下面列出的整门大学课程、整本书或所有仓库实验全部做完，而是按 **知识点 → 精确资源片段 → checkpoint → 下一模块** 前进。

> **学生使用规则：** 每次只做当前模块列出的 `Core` 片段。看到一个大课程/大书时，只读这里点名的 lecture/chapter/section；没有点名的部分默认先跳过。仓库 Lessons 用于中文导览和跨主题连接，Labs/Mini Cloud 是可选实践。

## 0. 一眼看懂怎么走

`README → 本页索引 → 当前模块 → 知识点/精确资源 → checkpoint → Next`

### M00–M24 一键索引

| Stage | 模块 |
|---|---|
| S1 计算的底座 | [M00 地图/工具](#m00) · [M01 信息与表示](#m01) · [M02 算法与数据结构](#m02) |
| S2 机器 | [M03 ISA/执行](#m03) · [M04 内存层次/测量](#m04) · [M05 语言/运行时/编译](#m05) |
| S3 OS 与持久化 | [M06 进程/系统调用](#m06) · [M07 虚拟内存](#m07) · [M08 文件/文件系统/I/O](#m08) · [M09 存储/耐久性](#m09) |
| S4 网络与浏览器 | [M10 IP/DNS/传输](#m10) · [M11 TLS/HTTP/缓存](#m11) · [M12 浏览器](#m12) |
| S5 数据与并发 | [M13 DB 存储/索引/查询](#m13) · [M14 事务/恢复/隔离](#m14) · [M15 并发](#m15) |
| S6 分布式与现代基础设施 | [M16 部分失败/RPC](#m16) · [M17 复制/一致性/共识](#m17) · [M18 分布式状态/协调](#m18) · [M19 交付/容器/供应链](#m19) · [M20 可观测性/SRE](#m20) |
| S7 安全与判断 | [M21 信任/密码学](#m21) · [M22 认证/授权/安全组合](#m22) · [M23 系统判断](#m23) · [M24 最终系统答辩](#m24) |

### 资源标签

- **Core**：现在就学；这是继续下一模块所需的最小集合。
- **Reference**：遇到疑问时查；不用顺序读完。
- **Optional deep dive**：想深入再做；不阻塞 Core。
- **Repo companion**：仓库自己的中文 Lesson / Lab / Mini Cloud；用于导览、连接和练习，不是强制。

---

<a id="m00"></a>
## M00 — The Map：工具、证据与“计算机里到底发生了什么”

**Repo companion:** [`book/00-the-map/`](book/00-the-map/)

| 知识点 | 精确资源 | 你要带走什么 |
|---|---|---|
| shell、路径、管道、重定向、进程入口 | **Core:** MIT Missing Semester 2026 — **Lecture 1 “Course Overview + Introduction to the Shell”** 与 **Lecture 2 “Command-line Environment”**：<https://missing.csail.mit.edu/2026/> | 能解释 cwd/path/stdin/stdout/stderr，能组合一个小 pipeline |
| debugger / profiler 是“观察工具”而不是魔法 | **Core:** Missing Semester 2026 — **Lecture 4 “Debugging and Profiling”**：<https://missing.csail.mit.edu/2026/> | 先预测，再观察，再解释；区分 observation 与 explanation |
| Git 的 commit / branch / diff | **Core:** Missing Semester 2026 — **Lecture 5 “Version Control and Git”**：<https://missing.csail.mit.edu/2026/> | 能用 diff/commit 作为证据，不需要精通复杂 Git workflow |
| 本课程的问题框架 | **Core:** [`L00-01.md`](book/00-the-map/L00-01.md) + [`L00-02.md`](book/00-the-map/L00-02.md) | 建立 State / Abstraction / Interface / Indirection 四个观察镜头 |

**先跳过：** shell scripting 花活、复杂 Git history surgery、完整 dotfiles 配置。

**Checkpoint:** 给一个你熟悉的程序，写出“输入 → 状态变化 → 输出”，再指出你会用哪个工具验证其中一个判断。

**Next → [M01 信息与表示](#m01)**

---

<a id="m01"></a>
## M01 — Information & Representation：bit、整数、文本、字节与序列化

**Repo companion:** [`book/01-information-representation/`](book/01-information-representation/)

| 知识点 | 精确资源 | 你要带走什么 |
|---|---|---|
| 固定位宽、二进制加法、溢出、ALU 直觉 | **Core:** Nand2Tetris **Project 2: Boolean Arithmetic**：<https://www.nand2tetris.org/project02> | 位模式不是“数字本身”；位宽决定可表示范围 |
| character / code point / code unit / UTF-8 bytes | **Core:** Unicode Core Spec **Chapter 2 §2.4 Code Points and Characters、§2.5 Encoding Forms、§2.5.3 UTF-8、§2.6 Encoding Schemes**：<https://www.unicode.org/versions/latest/core-spec/chapter-2/> | “字符数、code point 数、UTF-8 byte 数”可能不同 |
| UTF-8 的正式字节编码边界 | **Reference:** RFC 3629：<https://www.rfc-editor.org/rfc/rfc3629.html> | 知道何时需要标准而不是凭经验猜 |
| endian、字段宽度、padding、序列化 | **Core:** Python `struct` — **Byte Order, Size, and Alignment**：<https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment> | 序列化协议必须显式定义 byte order/size/alignment |

**先跳过：** Unicode 全部规范、复杂 normalization/collation、自己做完整 CPU。

**Checkpoint:** 任选一个字符串，预测 `len(text)` 与 UTF-8 byte 长度；再用 `encode()` 验证。用 `struct.pack('<I', x)` / `'>I'` 展示同一整数的不同 byte order。

**Next → [M02 算法与数据结构](#m02)**

---

<a id="m02"></a>
## M02 — Computation, Complexity & Data Structures

**Repo companion:** [`book/02-computation-complexity/`](book/02-computation-complexity/)

只取 MIT 6.006 的以下片段，不要求完成整门课：<https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/lecture-notes/>

| 知识点 | 精确资源 | Core 深度 |
|---|---|---|
| 算法模型、渐近复杂度 | **Lecture 1: Introduction** | 会给简单 loop/递归做数量级判断 |
| sequence / dynamic array 与接口成本 | **Lecture 2: Data Structures** | 理解操作集合与代价，不背 API |
| hash table | **Lecture 4: Hashing** | average-case lookup 与 collision 的来源 |
| binary tree / balanced tree / heap | **Lectures 6–8** | 知道 tree/heap 为什么提供不同操作成本 |
| graph traversal | **Lectures 9–10: BFS / DFS** | 能说清 frontier / visited 与 O(V+E) |
| dynamic programming | **Lectures 15–17**，只学“状态 + 子问题 + 转移” | 能识别重复子问题即可，不追求竞赛技巧 |

**Optional deep dive:** Lectures 11–14 shortest paths、18–19 pseudopolynomial/complexity。

**Checkpoint:** 对“查找、插入、取最小值、遍历连接关系”四类任务各选一种结构并解释为什么；给一段代码估算时间与空间数量级。

**Next → [M03 ISA / 执行](#m03)**

---

<a id="m03"></a>
## M03 — Machine：ISA、汇编、CPU 执行与调试

**Repo companion:** [`book/03-machine-isa-execution/`](book/03-machine-isa-execution/)

| 知识点 | 精确资源 | 你要带走什么 |
|---|---|---|
| machine language / assembly / instruction | **Core:** Nand2Tetris **Project 4: Machine Language**：<https://www.nand2tetris.org/project04> | 指令就是编码后的状态转换，不是“CPU 理解源码” |
| CPU、register、memory、fetch/execute | **Core:** Nand2Tetris **Project 5: Computer Architecture**：<https://www.nand2tetris.org/project05> | 能画出 instruction→register/memory 的最小数据流 |
| 真实 machine-level program / stack / control flow | **Reference:** CMU 15-213 schedule 中 **Machine-Level Programming: Basics / Control / Procedures / Data**：<https://www.cs.cmu.edu/~213/schedule.html> | 把教学 ISA 映射到真实 compiled code |
| 用 debugger 验证 | **Repo Core:** M03 Lessons 中的 GDB 路线 | 至少看一次 register/stack/instruction 的真实状态 |

**先跳过：** 自己设计完整 ISA、微架构优化、流水线 hazard 细节。

**Checkpoint:** 找一个小函数的反汇编，指出参数、返回值、一次 load/store、一次 branch，并用 debugger 验证其中一个预测。

**Next → [M04 内存层次与测量](#m04)**

---

<a id="m04"></a>
## M04 — Memory Hierarchy, Locality & Measurement

**Repo companion:** [`book/04-memory-locality-measurement/`](book/04-memory-locality-measurement/)

| 知识点 | 精确资源 | 你要带走什么 |
|---|---|---|
| cache hierarchy、block、locality、miss | **Core:** CMU 15-213 schedule — **The Memory Hierarchy (6.1–6.3)** + **Cache Memories (6.4–6.7)**：<https://www.cs.cmu.edu/~213/schedule.html> | cache 是利用 locality 的近似，不是“更快的 RAM” |
| 如何做可信性能实验 | **Core:** [`L04-02.md`](book/04-memory-locality-measurement/L04-02.md) | baseline、controlled change、重复测量、分布/噪声、推断边界 |
| profiling 选择工具 | **Reference:** Missing Semester 2026 — **Debugging and Profiling**：<https://missing.csail.mit.edu/2026/> | 先问问题，再选计时/profiler，而不是先跑工具 |

**Checkpoint:** 对两种访问模式先预测谁快、为什么；至少重复测量多次，并说明“观察到更快”不等于你已证明唯一原因。

**Next → [M05 语言/运行时/编译](#m05)**

---

<a id="m05"></a>
## M05 — Languages, Runtime & Compiler：源码如何变成执行

**Repo companion:** [`book/05-languages-runtime-compiler/`](book/05-languages-runtime-compiler/)

Crafting Interpreters 不用整本做完，只读对应机制：

| 知识点 | 精确资源 |
|---|---|
| token / scanner | **Core:** Ch.4 [Scanning](https://craftinginterpreters.com/scanning.html) |
| AST / representation | **Core:** Ch.5 [Representing Code](https://craftinginterpreters.com/representing-code.html) |
| parser 与语法结构 | **Core:** Ch.6 [Parsing Expressions](https://craftinginterpreters.com/parsing-expressions.html) |
| interpreter / evaluation | **Core:** Ch.7 [Evaluating Expressions](https://craftinginterpreters.com/evaluating-expressions.html) |
| bytecode / VM 的另一种执行模型 | **Core skim:** Ch.14 [Chunks of Bytecode](https://craftinginterpreters.com/chunks-of-bytecode.html) + Ch.15 [A Virtual Machine](https://craftinginterpreters.com/a-virtual-machine.html) |
| GC | **Optional:** Ch.26 [Garbage Collection](https://craftinginterpreters.com/garbage-collection.html) |

**Checkpoint:** 用一段 `a + b * c` 解释 source → tokens → AST → evaluator/bytecode → machine/runtime，指出每层丢掉和新增了什么信息。

**Next → [M06 进程与系统调用](#m06)**

---

<a id="m06"></a>
## M06 — Processes, Syscalls & Execution Context

**Repo companion:** [`book/06-processes-syscalls-execution-context/`](book/06-processes-syscalls-execution-context/)

OSTEP 只读：**Ch.4 Processes、Ch.5 Process API、Ch.6 Limited Direct Execution**：<https://pages.cs.wisc.edu/~remzi/OSTEP/>

然后查三个真实接口：

- **Core:** [`fork(2)`](https://man7.org/linux/man-pages/man2/fork.2.html) — 进程复制语义。
- **Core:** [`execve(2)`](https://man7.org/linux/man-pages/man2/execve.2.html) — 替换当前 process image。
- **Core:** [`waitpid(2)`](https://man7.org/linux/man-pages/man2/waitpid.2.html) — parent 如何等待/reap child。

**Optional repo practice:** LAB-REQ-02/xv6 syscall，用来把 user→syscall→kernel route 具体化；不做也不阻塞后续阅读。

**Checkpoint:** 准确解释 shell 启动一个命令时 `fork/exec/wait` 分别做什么，以及 system call 为什么需要 privilege transition。

**Next → [M07 虚拟内存](#m07)**

---

<a id="m07"></a>
## M07 — Virtual Memory & Isolation

**Repo companion:** [`book/07-virtual-memory-isolation/`](book/07-virtual-memory-isolation/)

OSTEP 只读：**Ch.13 Address Spaces、Ch.15 Address Translation、Ch.18 Introduction to Paging、Ch.19 TLB、Ch.21 Beyond Physical Memory: Mechanisms**：<https://pages.cs.wisc.edu/~remzi/OSTEP/>

真实接口只查：

- **Core:** [`mmap(2)`](https://man7.org/linux/man-pages/man2/mmap.2.html) — mapping 是什么。
- **Reference:** [`proc_pid_maps(5)`](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html) — 进程地址空间的可观察表面。

**Checkpoint:** 解释 virtual address → page table → physical frame；说明 page fault 可能意味着“合法但尚未映射/载入”，不等于 segfault。

**Next → [M08 文件/文件系统/I/O](#m08)**

---

<a id="m08"></a>
## M08 — Files, Filesystems & I/O

**Repo companion:** [`book/08-files-filesystems-io/`](book/08-files-filesystems-io/)

| 知识点 | 精确资源 |
|---|---|
| fd、目录、inode-like namespace、read/write | **Core:** OSTEP **Ch.39 Files and Directories**：<https://pages.cs.wisc.edu/~remzi/OSTEP/> |
| 文件系统内部 layout / allocation | **Core:** OSTEP **Ch.40 File System Implementation**：<https://pages.cs.wisc.edu/~remzi/OSTEP/> |
| `open/read/write` 的真实契约 | **Reference:** [`open(2)`](https://man7.org/linux/man-pages/man2/open.2.html)、[`read(2)`](https://man7.org/linux/man-pages/man2/read.2.html)、[`write(2)`](https://man7.org/linux/man-pages/man2/write.2.html) |
| rename/unlink 与“名字≠数据” | **Reference:** [`rename(2)`](https://man7.org/linux/man-pages/man2/rename.2.html)、[`unlink(2)`](https://man7.org/linux/man-pages/man2/unlink.2.html) |

**Checkpoint:** 解释一个 pathname 如何最终指向可读 bytes；解释“删除文件名”为什么不等于物理介质上的 bytes 立即消失。

**Next → [M09 存储与耐久性](#m09)**

---

<a id="m09"></a>
## M09 — Storage Engines & Durable Storage

**Repo companion:** [`book/09-storage-engine-durable-storage/`](book/09-storage-engine-durable-storage/)

| 知识点 | 精确资源 |
|---|---|
| device latency / HDD 与 block I/O | **Core:** OSTEP **Ch.36 I/O Devices + Ch.37 Hard Disk Drives**：<https://pages.cs.wisc.edu/~remzi/OSTEP/> |
| crash consistency / journaling | **Core:** OSTEP **Ch.42 FSCK and Journaling**：<https://pages.cs.wisc.edu/~remzi/OSTEP/> |
| SSD 基本差异 | **Core skim:** OSTEP **Ch.44 Flash-based SSDs**：<https://pages.cs.wisc.edu/~remzi/OSTEP/> |
| `fsync` 到底承诺什么 | **Reference:** [`fsync(2)`](https://man7.org/linux/man-pages/man2/fsync.2.html) |
| “数据库原子提交”如何建立在存储机制上 | **Reference:** SQLite [Atomic Commit §1–3](https://www.sqlite.org/atomiccommit.html)；WAL 只读 [§1 Overview、§2 How WAL Works](https://www.sqlite.org/wal.html) |

**Checkpoint:** 分别解释 “write() 返回”“fsync() 返回”“transaction COMMIT 返回”在不同层的含义，不把它们混成同一个 durability 承诺。

**Next → [M10 IP/DNS/传输](#m10)**

---

<a id="m10"></a>
## M10 — Networking：IP、DNS、socket、TCP/UDP

**Repo companion:** [`book/10-networking-ip-dns-transport/`](book/10-networking-ip-dns-transport/)

Beej 不要全读，只读以下段落：<https://beej.us/guide/bgnet/html/index-wide.html>

| 知识点 | 精确资源 |
|---|---|
| name → address | **Core:** Beej **§5.1 `getaddrinfo()`** |
| socket endpoint 与 client/server lifecycle | **Core:** **§5.2–5.7** `socket/bind/connect/listen/accept/send/recv` |
| stream vs datagram | **Core:** **§5.7–5.8 + §6.1–6.3** |
| blocking / multiplexing / partial send | **Reference:** **§7.1–7.5** |
| TCP 内部的 seq/ack/flow-control | **Optional deep dive:** Stanford CS144 **Checkpoint 2 TCP Receiver** 与 **Checkpoint 3 TCP Sender** handouts；课程当前定义见 Stanford CS144 catalog。无需实现完整 TCP stack。 |

**Checkpoint:** 从域名开始，画出 DNS → IP → socket → TCP byte stream → application bytes；说出 packet/datagram 与 TCP stream 为什么不是一回事。

**Next → [M11 TLS/HTTP/缓存](#m11)**

---

<a id="m11"></a>
## M11 — TLS, HTTP, Caches, Proxies & CDNs

**Repo companion:** [`book/11-networking-tls-http-cdn-proxies/`](book/11-networking-tls-http-cdn-proxies/)

| 知识点 | 精确资源 |
|---|---|
| HTTP request routing / target / intermediaries | **Core:** RFC 9110 **§7 Routing HTTP Messages**：<https://www.rfc-editor.org/rfc/rfc9110.html#section-7> |
| method semantics | **Core:** RFC 9110 **§9 Methods**：<https://www.rfc-editor.org/rfc/rfc9110.html#section-9> |
| conditional requests | **Core:** RFC 9110 **§13 Conditional Requests**：<https://www.rfc-editor.org/rfc/rfc9110.html#section-13> |
| status codes | **Reference:** RFC 9110 **§15 Status Codes**：<https://www.rfc-editor.org/rfc/rfc9110.html#section-15> |
| cache freshness / validation | **Core:** RFC 9111 **§4.2 Freshness + §4.3 Validation**：<https://www.rfc-editor.org/rfc/rfc9111.html#section-4.2> |
| TLS 1.3 handshake / authentication | **Core:** RFC 9846 **§2 Protocol Overview + §4 Handshake Protocol**；证书只查 **§4.5.1 Certificate**：<https://www.rfc-editor.org/rfc/rfc9846.html> |

**先跳过：** RFC 中密码套件编码细节、完整 HTTP extension registry。

**Checkpoint:** 解释一次 HTTPS GET 中 TCP/TLS/HTTP 各自解决什么；给出一个 fresh cache hit 和一个 stale→conditional validation 的流程。

**Next → [M12 浏览器](#m12)**

---

<a id="m12"></a>
## M12 — Browser as an Integrated System

**Repo companion:** [`book/12-web-browser-integrated-case/`](book/12-web-browser-integrated-case/)

| 知识点 | 精确资源 |
|---|---|
| event loop / task queue 的执行模型 | **Core:** MDN [JavaScript event loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop) |
| parse → DOM/CSSOM → layout → paint | **Core:** MDN [Critical rendering path](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Critical_rendering_path) |
| origin 与跨源边界 | **Core:** MDN [Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) |
| browser-side state | **Reference:** MDN [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API) |
| 多进程架构 / Site Isolation | **Core:** Chromium [Process Model and Site Isolation](https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md) — 只读 **Goals、Site Isolation、Modes and Availability** |

**Checkpoint:** 任选一个网页，从 URL 到 network response、parse/render、JS event loop、storage、process isolation 画出一条主链，并标出一个性能边界和一个安全边界。

**Next → [M13 DB 存储/索引/查询](#m13)**

---

<a id="m13"></a>
## M13 — Databases：Storage, Indexing & Query Processing

**Repo companion:** [`book/13-databases-storage-indexing/`](book/13-databases-storage-indexing/)

CMU 15-445 **只看 Fall 2026 schedule 中这些 lecture**：<https://15445.courses.cs.cmu.edu/fall2026/schedule.html>

| 知识点 | 精确资源 |
|---|---|
| relational model / declarative query | **Core:** **#01 Relational Model & Algebra** |
| page/storage layout | **Core:** **#03 Database Storage I、#05 Database Storage II**；#04 Memory Management 只 skim |
| hash/index/B+tree | **Core:** **#07 Hash Tables、#08–09 Indexes & Filters I/II** |
| query operators | **Core:** **#11 Sorting & Aggregations、#13 Join Algorithms、#14–15 Query Execution I/II** |
| planner/optimizer | **Core:** **#16–17 Query Planning & Optimization I/II** |
| SQLite 中索引如何实际改变访问路径 | **Core practice/reference:** SQLite Query Planner **§1.1–1.7**（scan→rowid→index→multi-column→covering index）：<https://www.sqlite.org/queryplanner.html> |

**先跳过：** CMU 课程 projects、vector indexes、复杂 DBMS implementation。

**Checkpoint:** 对一个 `WHERE` query 先预测 scan/index 可能性，再看 `EXPLAIN QUERY PLAN`；说明“加 index”为什么既有读收益也有写/空间成本。

**Next → [M14 事务/恢复/隔离](#m14)**

---

<a id="m14"></a>
## M14 — Transactions, Recovery & Isolation

**Repo companion:** [`book/14-databases-transactions-recovery-isolation/`](book/14-databases-transactions-recovery-isolation/)

CMU 15-445 Fall 2026 精确片段：<https://15445.courses.cs.cmu.edu/fall2026/schedule.html>

- **Core:** **#18 Concurrency Control Theory**。
- **Core:** **#19 Two-Phase Locking、#20 Timestamp Ordering、#21 MVCC** — 目标是比较，不要求实现。
- **Core:** **#22 Database Logging、#23 Database Recovery**。

SQLite 用来把抽象机制落到真实单机 DB：

- **Core:** [Transaction](https://www.sqlite.org/lang_transaction.html) — `DEFERRED/IMMEDIATE/EXCLUSIVE`、COMMIT/ROLLBACK、error response。
- **Core:** [File Locking and Concurrency](https://www.sqlite.org/lockingv3.html) — 只读 **§1 Locking、§4 Rollback Journal、§5 Writing、§7 SQL-level transaction control**。
- **Core:** [Atomic Commit](https://www.sqlite.org/atomiccommit.html) — **§1–3** 建立“原子是幻觉如何实现”的直觉。
- **Reference:** [WAL §1–2](https://www.sqlite.org/wal.html) — 与 rollback journal 比较。

**Checkpoint:** 用两个 DB connection 解释 committed visibility / writer conflict；解释 rollback journal 或 WAL 如何帮助 crash recovery，但不要把 process-crash 与 power-loss guarantee 混为一谈。

**Next → [M15 并发](#m15)**

---

<a id="m15"></a>
## M15 — Concurrency：Threads, Races & Synchronization

**Repo companion:** [`book/15-concurrency-threads-races-synchronization/`](book/15-concurrency-threads-races-synchronization/)

OSTEP 只读这些章：<https://pages.cs.wisc.edu/~remzi/OSTEP/>

- **Core:** **Ch.26 Concurrency and Threads**。
- **Core:** **Ch.27 Thread API**，只理解 create/join 基本契约。
- **Core:** **Ch.28 Locks**。
- **Core:** **Ch.30 Condition Variables**，重点是 predicate + `while`。
- **Core:** **Ch.32 Common Concurrency Problems**。
- **Reference:** Ch.31 Semaphores；需要时再读。

**Optional repo practice:** LAB-REQ-03 用真实 C/pthreads 展示 lost update、mutex、condition-variable predicate break。

**Checkpoint:** 写出一个 race 的两个合法 interleaving；说明 mutex 保护的 invariant 是什么；解释为什么 condition variable 通常需要 `while(predicate)` 而不是 `if`。

**Next → [M16 部分失败/RPC](#m16)**

---

<a id="m16"></a>
## M16 — Distributed Systems I：Partial Failure, RPC, Timeouts & Retries

**Repo companion:** [`book/16-distributed-systems-partial-failure-rpc/`](book/16-distributed-systems-partial-failure-rpc/)

| 知识点 | 精确资源 |
|---|---|
| 为什么分布式系统的失败与本地调用不同 | **Core:** MIT 6.5840 Spring 2026 **Lecture 1: Introduction**：<https://pdos.csail.mit.edu/6.824/schedule.html> |
| RPC + concurrency 基本模型 | **Core:** MIT 6.5840 **Lecture 2: RPC and Threads** |
| timeout / retry / exponential backoff / jitter | **Core practitioner:** AWS Builders' Library **“Timeouts, retries, and backoff with jitter”**：<https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/> |
| retry 与副作用 | **Core:** AWS Builders' Library **“Making retries safe with idempotent APIs”**：<https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/> |

**Checkpoint:** 对“客户端 timeout 但服务端可能已经成功”列出至少三种真实状态；说明为什么 retry 必须结合 idempotency/operation identity 才能推理。

**Next → [M17 复制/一致性/共识](#m17)**

---

<a id="m17"></a>
## M17 — Distributed Systems II：Replication, Consistency & Consensus

**Repo companion:** [`book/17-distributed-systems-replication-consistency-consensus/`](book/17-distributed-systems-replication-consistency-consensus/)

MIT 6.5840 Spring 2026 schedule：<https://pdos.csail.mit.edu/6.824/schedule.html>

| 知识点 | 精确资源 |
|---|---|
| replication 为什么既提高可用性又制造一致性问题 | **Core:** **Lecture 3: GFS** + GFS paper preparation |
| consensus 的问题定义与多数派直觉 | **Core:** **Lecture 4: Paxos pseudo-code**；后续 Raft lab/lecture只理解 leader/term/log/majority，不要求完成 lab |
| coordination service / linearizable metadata | **Core:** **Lecture 9: ZooKeeper** + ZooKeeper paper preparation |
| consistency 不是 ACID “C” | **Core:** [`L17-03.md`](book/17-distributed-systems-replication-consistency-consensus/L17-03.md) |

**先跳过：** 自己实现 production consensus、完整 formal proof。

**Checkpoint:** 给三副本系统画出一次 leader/network failure；说明哪些 observation 可能旧、哪些承诺需要 quorum/ordering guarantee，并明确你采用的 consistency guarantee 名称。

**Next → [M18 分布式状态/协调](#m18)**

---

<a id="m18"></a>
## M18 — Distributed State：Transactions, Sharding, Coordination & Delivery Semantics

**Repo companion:** [`book/18-distributed-state-coordination/`](book/18-distributed-state-coordination/)

MIT 6.5840 Spring 2026：<https://pdos.csail.mit.edu/6.824/schedule.html>

- **Core:** **Lecture 11: Distributed Transactions**；指定 preparation 只读 6.033 Ch.9 的课程点名小节。
- **Core:** **Lecture 12: Spanner** — 看 transaction + time/replication 如何组合，不需要掌握整篇所有工程细节。
- **Core:** **Lecture 13: Chain Replication** — 比较另一种 replication/ordering design。
- **Reference:** 后续 sharding/kv-service material，只理解 shard movement/ownership/change 带来的 state coordination 问题。
- **Core judgement:** AWS [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) 的 **Retries and side effects / Semantic equivalence** 两节。

**Checkpoint:** 解释 “exactly once” 为什么通常不是简单网络属性；对一个 payment/order-like operation 设计 operation ID + retry contract，并说明它没解决哪些跨资源 atomicity 问题。

**Next → [M19 交付/容器/供应链](#m19)**

---

<a id="m19"></a>
## M19 — Modern Infrastructure：Isolation, Delivery & Supply Chain

**Repo companion:** [`book/19-modern-infrastructure-delivery/`](book/19-modern-infrastructure-delivery/)

| 知识点 | 精确资源 |
|---|---|
| Linux namespace 到底隔离什么 | **Core:** [`namespaces(7)`](https://man7.org/linux/man-pages/man7/namespaces.7.html) — 先读 overview + namespace type list |
| resource control 与 cgroup v2 | **Core:** [`cgroups(7)`](https://man7.org/linux/man-pages/man7/cgroups.7.html) 的 **CGROUPS VERSION 2**；需要接口细节再查 kernel [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) **Introduction / Terminology** |
| container image 是内容/metadata，不等于 VM | **Reference:** OCI Image Spec `spec.md`：<https://github.com/opencontainers/image-spec/blob/main/spec.md>，只看 image manifest/config/layers 的模型 |
| build provenance / supply-chain trust | **Core:** SLSA v1.2 **Build Track Basics**：<https://slsa.dev/spec/v1.2/build-track-basics>；重点 L1/L2/L3 分别增加什么保证 |

**先跳过：** Kubernetes API 大全、多云产品目录、自己写 container runtime。

**Checkpoint:** 用“namespace + cgroup + filesystem/image + process”解释 container 与 VM 的不同；对一个二进制说明“来自哪个 source/build”为什么需要 provenance。

**Next → [M20 可观测性/SRE](#m20)**

---

<a id="m20"></a>
## M20 — Observability & Reliability Engineering

**Repo companion:** [`book/20-observability-reliability-engineering/`](book/20-observability-reliability-engineering/)

| 知识点 | 精确资源 |
|---|---|
| SLI/SLO 与风险预算 | **Core:** Google SRE **Ch.4 Service Level Objectives**：<https://sre.google/sre-book/service-level-objectives/> |
| white-box/black-box、四个黄金信号 | **Core:** Google SRE **Ch.6 Monitoring Distributed Systems**：<https://sre.google/sre-book/monitoring-distributed-systems/> |
| troubleshooting = hypothesis→test | **Core:** Google SRE **Ch.12 Effective Troubleshooting**：<https://sre.google/sre-book/effective-troubleshooting/> |
| traces / metrics / logs | **Core:** OpenTelemetry [Signals](https://opentelemetry.io/docs/concepts/signals/) — 只读 Traces/Metrics/Logs 的角色与差异 |
| context propagation 的价值与隐私风险 | **Reference:** OpenTelemetry [Baggage](https://opentelemetry.io/docs/concepts/signals/baggage/) — 特别读 **security considerations** |

**Checkpoint:** 给一个“请求变慢”故障先写 2–3 个 hypothesis，再为每个 hypothesis 指定 metric/log/trace 中哪一种证据能区分它们；避免“先收集所有数据”。

**Next → [M21 信任/密码学](#m21)**

---

<a id="m21"></a>
## M21 — Security I：Trust Boundaries & Cryptographic Mechanisms

**Repo companion:** [`book/21-security-synthesis-trust-crypto/`](book/21-security-synthesis-trust-crypto/)

| 知识点 | 精确资源 |
|---|---|
| threat model / data-at-rest crypto 的边界 | **Core:** OWASP [Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) — **Architectural Design、Key Storage** |
| password hashing 与 encryption 不同 | **Core:** OWASP [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) — **Introduction、Background: Hashing vs Encryption** |
| TLS 1.3 提供什么 | **Core:** RFC 9846 **§2 Protocol Overview、§4 Handshake Protocol、§4.5.1 Certificate**：<https://www.rfc-editor.org/rfc/rfc9846.html> |
| 不要自己发明 crypto | **Reference:** repo `L21-*` 的 primitive→property→threat mapping；需要练手时 Cryptopals 只做选题，不作为安全实现指南 |

**Checkpoint:** 对“数据库里的 password、API traffic、disk backup、signing key”分别选择 hash/encryption/TLS/signature/key-management 中的机制，并说出每个机制**不**解决什么。

**Next → [M22 认证/授权/安全组合](#m22)**

---

<a id="m22"></a>
## M22 — Security II：Authentication, Authorization, Sessions & Composition

**Repo companion:** [`book/22-security-synthesis-auth-composition/`](book/22-security-synthesis-auth-composition/)

| 知识点 | 精确资源 |
|---|---|
| authentication lifecycle | **Core:** OWASP [Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) — 重点 re-authentication / transport / generic errors |
| authorization / least privilege / deny by default | **Core:** OWASP [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) |
| session ID/cookie 安全 | **Core:** OWASP [Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — session ID、cookie attributes、TLS |
| OAuth 的现代安全边界 | **Core:** RFC 9700 **§2 Best Practices**；遇到具体 attack 再查 **§4 Attacks and Mitigations**：<https://www.rfc-editor.org/rfc/rfc9700.html> |

**先跳过：** 自己实现 OAuth server、背诵所有 attack 名称。

**Checkpoint:** 画出 user → browser/client → auth service → resource 的 trust map；分别标出 identity proof、session、authorization decision、token scope，并指出一个 confused-deputy/privilege-escalation 风险。

**Next → [M23 系统判断](#m23)**

---

<a id="m23"></a>
## M23 — Systems Thinking & Judgment：测量、成本、风险与技术选择

**Repo companion:** [`book/23-systems-thinking-judgment/`](book/23-systems-thinking-judgment/)

| 知识点 | 精确资源 |
|---|---|
| reliability 是成本/风险 trade-off，不是“越高越好” | **Core:** Google SRE **Ch.3 Embracing Risk**：<https://sre.google/sre-book/embracing-risk/> |
| 简单性本身是可靠性策略 | **Core:** Google SRE **Ch.9 Simplicity**：<https://sre.google/sre-book/simplicity/> |
| hypothesis-driven troubleshooting | **Core revisit:** [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) 的 theory/process |
| 如何评估新技术 | **Core:** [`meta/TECHNOLOGY_EVALUATION_FRAMEWORK.md`](meta/TECHNOLOGY_EVALUATION_FRAMEWORK.md) — 明确 problem、baseline、evidence、failure modes、operational cost、reversibility |

**Checkpoint:** 选一个“是否引入 cache/queue/new DB/container platform”的问题，先写“不引入”的 baseline，再列 benefit、new failure modes、measurement plan、reversibility；没有证据时允许结论是“不加”。

**Next → [M24 最终系统答辩](#m24)**

---

<a id="m24"></a>
## M24 — Final System Defense：把整条系统链说清楚

**Repo companion:** [`book/24-final-system-defense/L24-01.md`](book/24-final-system-defense/L24-01.md) + [`L24-02.md`](book/24-final-system-defense/L24-02.md)

这里不需要再找一门新课。你要把前面资源变成一个一致的 world model。

**Core defense checklist：**

1. **Representation:** 数据以什么 bytes/encoding/schema 表示？
2. **Machine:** CPU/memory hierarchy 在哪里影响行为或成本？
3. **OS:** process/thread/VM/files/system calls 的边界在哪里？
4. **Network:** DNS/IP/TCP/TLS/HTTP 每层承诺什么？
5. **Browser/client:** origin/process/state 如何影响安全与性能？
6. **Data:** index/query/transaction/recovery 的 correctness contract 是什么？
7. **Concurrency/distribution:** race、retry、idempotency、replication/consistency 在哪里出现？
8. **Infrastructure:** isolation/build/provenance 如何影响部署可信度？
9. **Observability:** 哪些 signals 能证伪你的解释？
10. **Security/privacy:** trust boundary、identity、authorization、sensitive data 在哪里？
11. **Judgment:** 哪些复杂度你明确选择**不**加入，为什么？

**Reference when stuck:** 回到本页对应模块的 exact resource，不要继续横向搜更多教程。

**Optional practice:** `project/` Mini Cloud 或你自己的真实小系统；重点是 defense evidence，不要求使用仓库项目。

**Final checkpoint:** 用一张图 + 一页文字回答：“一个真实请求如何穿过整个系统？如果它慢、错、丢、重复、泄露或宕机，我分别从哪一层开始找证据？”如果你能把机制、证据、限制和 trade-off 连起来，Core traversal 完成。

**Next → [回到顶部索引](#m00)**

---

## 结束后的三个方向

1. **深挖系统实现：** 再回头做 Required Labs、Mini Cloud、Nand2Tetris/CS144/6.5840 的更多 project。
2. **面向工作：** 按目标岗位从 M10–M23 选相关链路做真实系统 observation。
3. **保持 current：** 对 RFC、browser、DB、observability、安全最佳实践等 CURRENT 资源优先看官方更新；稳定机制无需为了“新”而换教材。

## 建议节奏

- 每周 **1 个大模块** 或 **2 个轻模块**；M02/M05/M13–M18 可以放慢。
- 每次学习最多：**一个 Core 主资源片段 + 一个 checkpoint**。
- 一个主题卡住超过两次，再打开 Reference/Repo companion；不要同时开五份资料。
- 不以“看完多少小时视频”为进度，而以“能否解释机制 + 做一个正确预测 + 知道去哪查证”为进度。

维护和资源选择标准见 [`meta/RESOURCE_FIRST_CURRICULUM_POLICY.md`](meta/RESOURCE_FIRST_CURRICULUM_POLICY.md)；学生路径验收标准见 [`meta/STUDENT_ROUTE_ACCEPTANCE.md`](meta/STUDENT_ROUTE_ACCEPTANCE.md)。
