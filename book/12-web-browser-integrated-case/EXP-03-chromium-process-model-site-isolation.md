# EXP-03｜Chromium 进程模型与站点隔离源码考察 (Source Expedition)

## 考察档案

- **考察标识**：`EXP-03` — Chromium Process Model & Site Isolation Source Expedition
- **所属模块**：`M12`（Web & Browser: The Integrated Case）
- **主要能力**：**Observe** (在真实生产级大型开源系统中定位并观测系统架构落地的代码实证)
- **进阶能力**：**Trace** (追踪从架构设计文档到具体类方法的控制流逻辑), **Explain** (阐明生产实现与教学抽象模型的异同)
- **代码仓库**：[Chromium Gitiles 官方源码树](https://chromium.googlesource.com/chromium/src/+/main/)
- **考察方式**：**在线链接与代码导读（Link-and-Inspection-First）**。严禁下载 100GB 完整仓库，严禁本地编译 Chromium。

---

## 1. 考察背景与教育目标

在课堂与教材中，我们学习了现代浏览器的多进程架构、渲染沙箱与站点隔离（Site Isolation）。这些概念在工业界最顶级的生产级系统软件中究竟长什么样？

Chromium 拥有超过 3500 万行代码，是当今世界上最复杂的大型 C++ 系统之一。直接漫无目的地浏览极其容易迷失在浩瀚的细节汪洋中。
本考察的目的在于通过**严格受控的三点式路径（Three-Anchor Route）**，带你直击 Chromium 内部最核心的三处系统实现：
1. **架构设计文档锚点**：验证站点隔离应对渲染器攻破与 Spectre 硬件漏洞的根本动因；
2. **进程调度选择逻辑锚点**：观测 `SiteInstanceImpl` 如何在运行时决定复用旧进程还是创建新进程；
3. **中央安全策略仲裁锚点**：观测浏览器主进程的 `ChildProcessSecurityPolicyImpl` 如何像操作系统内核一样，阻断被攻破渲染进程对跨站数据的越权访问。

---

## 2. 考察路线与停止规则（Stop Rules）

```
========================================================================================================
EXP-03 BOUNDED SOURCE ROUTE & STOPPING POINTS
========================================================================================================
1. [设计规范/概念宣称]
   "浏览器需要进程隔离防范恶意页面"
         |
         v
   [文档锚点]: docs/process_model_and_site_isolation.md
   * 观测重点: Site Isolation 的安全动机 (Compromised Renderers & Spectre 硬件漏洞)
   * 停止点: 读完 Goals 与 Site Isolation 核心段落即止; 严禁深入 Android WebView 嵌入细节!
         |
         v
2. [进程分配抽象]
   "同一个站点或上下文组如何映射到 OS 进程?"
         |
         v
   [调度代码锚点]: content/browser/site_instance_impl.cc
   * 观测重点: SiteInstanceImpl::GetProcess() -> GetOrCreateProcess() 进程选择与复用逻辑
   * 停止点: 停在 ProcessReusePolicy 判定入口; 严禁向下深挖 Mojo IPC 通道构建或 RenderProcessHost 分配!
         |
         v
3. [浏览器端安全仲裁]
   "如何防止恶意/被攻破渲染进程跨站偷数据?"
         |
         v
   [策略代码锚点]: content/browser/security/cpsp/child_process_security_policy_impl.cc
   * 观测重点: ChildProcessSecurityPolicyImpl::CanAccessDataForOrigin() 进程锁匹配
   * 停止点: 停在 CanAccessOrigin 进程锁校验入口; 严禁追踪遗留 blob/file 兼容分支!
========================================================================================================
```

> **铁律停止规则（Stop Rules）**：
> - **严禁克隆或下载完整 Chromium 仓库**：使用官方网页版代码浏览器（Gitiles）即可完成全部实证；
> - **严禁编译 Chromium**；
> - **严禁漫游泛化调用链**：在到达指定方法后立即停止，绝不顺着头文件或调用关系无限下潜；
> - **严禁代码整段搬运**：本考察以引用与原理解析为主，严格遵守版权与合理使用规范。

---

## 3. 考察任务卡（Bounded Inspection Card）

请跟随指导，依次打开官方代码链接，完成以下 5 项实证任务：

### 任务 1（架构设计诉求）：阅读架构文档

- **目标文件**：[`docs/process_model_and_site_isolation.md`](https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md)
- **检索定位**：检索关键词 `Goals` 以及 `Site Isolation`。
- **考察问题**：
  Chromium 团队在文档中阐述了引入“站点隔离（Site Isolation）”的两大关键安全动机。除了一般的渲染器进程攻破（Compromised Renderers）之外，哪一类**现代微架构硬件漏洞**彻底改变了安全威胁模型，促使必须采用独立的操作系统进程来运行跨站 iframes？
- **实证记录**：
  文档明确指出，现代 Web 的威胁模型不仅要防范渲染进程被攻破，更必须防范像 **Spectre 与 Meltdown** 这类利用处理器推测执行微架构侧信道泄露内存数据的硬件攻击。如果两个不同站点的代码运行在同一个进程内，恶意代码就能借由 Spectre 嗅探该进程内的全部数据，因此必须由操作系统虚拟内存和进程边界（Site Isolation）提供物理隔离。
- **停止确认**：已在 Goals / Motivation 部分停止，未进入平台定制与历史演进章节。

### 任务 2（进程分配调度）：检查 `SiteInstanceImpl`

- **目标文件**：[`content/browser/site_instance_impl.cc`](https://chromium.googlesource.com/chromium/src/+/main/content/browser/site_instance_impl.cc)
- **检索定位**：定位方法 `SiteInstanceImpl::GetProcess()` 及其调用的 `SiteInstanceImpl::GetOrCreateProcess()`。
- **考察问题**：
  当一个页面上下文请求其绑定的渲染进程时，Chromium 是直接无条件执行 `fork()` 创建一个全新进程，还是存在进程复用策略？代码中调用了哪些关键判断条件？
- **实证记录**：
  在 `GetOrCreateProcess` 中，代码首先检查 `has_group()`，并结合 `ShouldUseProcessPerSite()` 更新 `process_reuse_policy_`（如 `ProcessReusePolicy::kProcessPerSite`）；随后评估 `CanPutSiteInstanceInDefaultGroup()` 判断当前上下文是否可以并入默认的站点实例组（Default SiteInstanceGroup）复用现有进程，只有在不满足复用条件时才真正为该组创建独立的进程与 `RenderProcessHost`。
- **停止确认**：已在进程选择与组归属判断处停止，未跟踪 Mojo 管道初始化。

### 任务 3（中心化安全仲裁）：检查 `ChildProcessSecurityPolicy`

- **目标文件**：[`content/browser/security/cpsp/child_process_security_policy_impl.cc`](https://chromium.googlesource.com/chromium/src/+/main/content/browser/security/cpsp/child_process_security_policy_impl.cc)
  *(路径现时性说明：在最新 Chromium 重构中，该文件位于 `content/browser/security/cpsp/` 目录下)*
- **检索定位**：定位方法 `ChildProcessSecurityPolicyImpl::CanAccessDataForOrigin(...)`。
- **考察问题**：
  该方法接收哪些关键参数来判定一个渲染进程是否有权访问某个源的数据？它如何处理不透明源（Opaque Origin）？
- **实证记录**：
  该方法接收子进程标识 `int child_id` 与目标源 `const url::Origin& origin`。它内部调用 `CanAccessOrigin(..., AccessType::kCanAccessDataForCommittedOrigin)`。针对 `origin.opaque()`，它会尝试提取前驱元组（Precursor Tuple）进行 URL 校验，并最终比对该进程在 `process_states_` 中的进程锁（Process Lock）是否与该源匹配。一旦进程已被锁死给 Site A，任何请求 Site B 数据的 IPC 都会被立刻裁定为非法并记录 Crash Keys。
- **停止确认**：已在 origin 锁匹配与 access_type 入口处停止，未跟踪复杂的文件路径特例。

### 任务 4（抽象与实现的差异辨析）：反思“一站一进程”

- **反思问题**：
  为什么不能简单地把 Chromium 的多进程实现宣称为“一个网站严格等于一个操作系统进程”？
- **实证结论**：
  在真实源码与策略中，“一站一进程”只是高配桌面设备上的理想模式。面对移动设备或高负载场景，Chromium 实现了复杂的复用降级策略（Default SiteInstanceGroup、Process-per-site、以及受操作系统全局进程数上限限制时的进程共享）。教学中的“一站一进程”是理解站点隔离的优美心智模型，而工程实现则是安全防御与物理资源开销之间的精密平衡。

### 任务 5（实证版本与元数据记录）：源头版本追踪

- **检查时间**：2026-09-04
- **考察分支**：`refs/heads/main`
- **实际检查 Commit**：`cd4ff71cd07504d87e90484d1bd0d66c2b6180dc`
- **源码访问状态**：`LIVE_CHROMIUM_SOURCE_ACCESSIBLE`（通过官方 Gitiles 接口实时确认）。

---

## 4. 考察总结与概念连接

通过本次 Source Expedition，我们在真实世界最大型系统软件中印证了两个核心理论：
1. **进程（Process，EC-CON-018）是终极隔离屏障**：由于现代 CPU 的硬件推测执行机制无法在同进程内提供微架构隐私，操作系统进程所拥有的独立页表与地址空间，成为了浏览器抗击高级侧信道攻击的唯一有效物理防线；
2. **集中仲裁防范沙箱逃逸（EC-CON-017 信任边界）**：不可信的渲染代码即使在沙箱中被恶意篡改，它发出的所有系统级数据请求依然必须经过 Browser 进程中的 `ChildProcessSecurityPolicyImpl` 集中裁决。这种“内核-用户态”式的权限分离，正是现代安全系统设计的精髓。

---

## 5. 版权与规范声明

- Chromium 源码版权归 The Chromium Authors 所有，遵循 BSD 开源许可证协议；
- 本实验遵循“仅链接与微量导读”原则，不镜像、不分发 Chromium 完整代码。
