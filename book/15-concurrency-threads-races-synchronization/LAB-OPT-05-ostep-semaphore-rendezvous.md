# LAB-OPT-05: OSTEP 信号量会合实验导引 (Strictly Optional / Link-Only Guide)

> **声明与版权边界 (Rights & Licensing Boundary)**：
> - 本实验为**完全自愿选修（Strictly Optional）**内容，不构成 Essential CS 核心必修课程或 `LAB-REQ-03` 的达标依赖；
> - 上游 OSTEP（Operating Systems: Three Easy Pieces）配套作业代码仓库在项目调研记录中缺乏明确的开源再分发授权；
> - **纯链接引用原则（Link-Only Protocol）**：本仓库**严禁且未曾复制、分发、改编或包含任何上游作业的源码、骨架、测试用例或文字段落**；
> - 若学习者网络不可达或未克隆该外部仓库，请直接标记为：`OPTIONAL TOOL/SOURCE UNAVAILABLE / SKIP`，这不会影响任何核心课程评估。

---

## 1. 经典文献与外部源码指向 (External Canonical Pointer)

- **权威教材**：Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, *Operating Systems: Three Easy Pieces* (OSTEP), Chapter 31: *Semaphores*.
- **外部代码仓库**：`https://github.com/remzi-arpacidusseau/ostep-homework`
- **核准审查 Commit**：`afb36ca8ddbf81d847d18f6bd18a87f0a18667f2`
- **目标源码路径**：`threads-sema/rendezvous.c`

---

## 2. 核心探究问题与背景 (Original Essential CS Inspection Questions)

在核心实验 `LAB-REQ-03` 中，我们掌握了基于 POSIX 互斥锁（Mutex）与条件变量（Condition Variable）的事件会合模式。经典操作系统理论中，Edsger Dijkstra 提出了另一种优雅的同步原语——**信号量（Semaphore）**。

请在外部已克隆的 OSTEP 官方仓库环境中，打开 `threads-sema/rendezvous.c` 进行独立阅读与思考：

### 探究问题 1：信号量初始值的物理意义
- 在双线程会合问题（Rendezvous Problem）中，要求线程 A 的“前置代码”（Child 1: before）与线程 B 的“前置代码”（Child 2: before）都必须在任何一个线程执行“后置代码”（after）之前完成。
- 为什么用于会合控制的信号量初始值必须设置为 `0`，而不是 `1`？如果初始值为 `1`，系统的不变式将被如何破坏？

### 探究问题 2：`sem_wait()` 与 `sem_post()` 的对称性
- 观察两线程各自调用 `sem_post()` 与 `sem_wait()` 的前后相对次序；
- 为什么必须是“先发信号通知对方我已到达，再等待对方到达的信号”，而不是相反？如果把调用颠倒为“先 wait 再 post”，系统会陷入哪种经典故障？（提示：回顾 L15-02 中的 Coffman 死锁条件）。

### 探究问题 3：信号量 vs 条件变量
- 比较信号量与条件变量在状态记忆机制上的本质差异：
  - 条件变量是“纯信令”（Stateless Signaling）：如果发送 `pthread_cond_signal` 时没有任何线程在等待，该信号会凭空消失；
  - 信号量是“有状态的计数器”（Stateful Counter）：如果先执行了 `sem_post`，信号量计数递增，后续到来的 `sem_wait` 不会挂起，而是直接扣减并通行。
- 这种状态记忆特性对避免竞态时序窗口（Race Window）带来了什么优势与心智负担？

---

## 3. 本地审查与安全确认

学习者在独立查阅外部代码后，可在个人笔记中记录：
1. 外部源仓库 Git Commit 确认：`afb36ca8ddbf81d847d18f6bd18a87f0a18667f2`；
2. 确认仅进行只读查阅与思维推演，未向本仓库引入任何未经许可的第三方源码；
3. 若外部环境缺失：直接标记 `OPTIONAL TOOL/SOURCE UNAVAILABLE / SKIP`。
