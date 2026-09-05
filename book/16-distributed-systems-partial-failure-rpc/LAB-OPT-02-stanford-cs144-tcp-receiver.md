# LAB-OPT-02: 斯坦福 CS144 TCP 接收端实验导引 (Strictly Optional / Rights-Gated / Link-Only Guide)

> **版权与许可边界严正声明 (Rights & Licensing Boundary)**：
> - 本实验为**完全自愿选修（Strictly Optional）**内容，绝不构成 Essential CS 核心必修课程或 M16 模块的达标依赖；
> - 上游斯坦福大学 CS144（Introduction to Computer Networking, Fall 2025，课程主理人 Philip Levis 与 Keith Winstein）实验材料、作业文本及 Minnow 协议栈框架的公开再分发与改编授权**尚未建立 (Rights Unestablished)**；
> - **严格零源码搬运与纯链接原则 (Zero-Vendoring & Link-Only Protocol)**：本仓库**严禁且未曾包含任何上游实验指导书正文、骨架代码、CMake 构建脚本、测试用例或 Minnow 实现源码**；
> - 核心 M16 模块依赖 Python 3 标准库，**不引入任何隐性 C++ 或 CMake 工具链依赖**；
> - 若学习者因网络环境受限或无意获取外部材料，请直接在实证报告中记录：
>   `OPTIONAL SOURCE UNAVAILABLE / SKIP`，这绝不影响 M16 核心课程的 PASS 评估。

---

## 1. 外部官方源与基准指向 (Canonical External Pointer)

- **课程机构**：Stanford University — CS144: *Introduction to Computer Networking* (Fall 2025)
- **官方主页**：[https://cs144.github.io/](https://cs144.github.io/)
- **实验目标**：Checkpoint 2 — *The TCP Receiver* (`check2.pdf`)
- **外部代码框架**：Minnow TCP implementation (学习者如需参与，需依照斯坦福课程公开指引独立获取上游 Git 仓库)

---

## 2. 教学定位与心智模型连接 (Pedagogical Role)

在 Essential CS 知识图谱中：
- `M10`（IP、DNS 与传输层）建立了 TCP 字节流与序号空间的基本抽象；
- `M16`（部分失效与 RPC）将网络通信推向分布式系统的不确定性前沿。

TCP 作为可靠的面向字节流协议，必须在不可靠、会发生丢包、乱序、重复和延迟的 IP 网络之上，重建连续有序的字节流。`LAB-OPT-02` 引导有精力且具备现代 C++ 基础的学习者深入协议栈接收端底层，理解以下核心机制：
1. **32 位循环序号空间与 64 位绝对索引解包**：TCP 头部仅有 32 位序号（`seqno`），会发生环绕回绕（Wrapping）。接收端必须根据初始序号（`ISN`）和已确认的检查点，将 32 位 `seqno` 正确展开为 64 位的绝对序列号（`absolute seqno`）；
2. **重组缓冲区（StreamReassembler / ByteStream）**：如何暂存提前到达的乱序数据切片，并在前序缺失字节补齐后，按序推入应用层可读取的流缓冲区；
3. **确认号（ACKno）与接收窗口（Window Size）计算**：如何向发送端真实反馈当前期望接收的下一个字节序号，以及接收缓冲区的剩余可用容量，防止接收端缓冲区溢出。

---

## 3. 核心探究问题 (Original Essential CS Inspection Questions)

请在独立获取并配置好外部 CS144 环境的学习者，结合 Minnow 接口定义进行思考：

### 探究问题 1：为什么 TCP 序号必须使用随机初始序号（ISN）？
- 如果每个 TCP 连接都固定从序号 `0` 开始传输，在网络中存在“迟到的历史重复数据报文段”（Zombie Packets）或恶意连接伪造攻击时，会引发什么致命后果？

### 探究问题 2：32 位循环序列空间的最近展开算法（Unwrap）
- 当接收端收到一个 32 位的 `seqno` 时，存在无穷多个相差 $2^{32}$ 整数倍的 64 位绝对序列号。
- 为什么必须以“当前已重组的检查点（Checkpoint）”作为参照点，选择距离检查点最近的那一个 64 位值？

### 探究问题 3：传输层接收 ACK 与应用层业务完成的根本区别
- 审视 TCP 接收端向网络回复 ACK 的时机：数据进入 TCP 接收缓冲区即可回复 ACK。
- 此时用户空间进程是否已经读取了这部分数据？数据库是否已经完成了事务提交？
- 结合 M16 核心课反思：为什么“底层收到 TCP ACK”绝对不能等同于“分布式业务成功提交”？

---

## 4. 受限停止点 (Bounded Stopping Point)

若学习者独立获取了上游授权材料并开展实践：
- **严格停止边界**：仅限完成 Checkpoint 2 中 `TCPReceiver` 的接收逻辑并通过其公开单元测试（`ctest -R "^recv_"`）；
- **禁止前向扩展**：不需要实现后续的 Checkpoint 3（TCP Sender）或路由器逻辑；
- **记录规范**：在个人证据记录中仅标注完成状态与思维答卷，严禁向公开仓库提交上游作业代码。
