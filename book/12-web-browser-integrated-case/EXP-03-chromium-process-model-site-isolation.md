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

Chromium 是一个规模巨大、持续快速演进的 C++ 系统；代码规模本身会随统计方式与版本变化。本考察不依赖固定代码行数，而依赖严格的三锚点与停止规则避免漫游。
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
> - **严禁代码整段搬运**：本考察以官方链接、learner 自己的定位记录与释义为主。若未来确需摘录，先检查**所摘录具体文件的 header/license/NOTICE/第三方许可**并保持最小范围；不依赖一条笼统的“合理使用”结论。

---

## 3. 考察任务卡（Bounded Inspection Card）

请跟随指导，依次打开官方代码链接，完成以下 5 项实证任务：

### 任务 1（架构设计诉求）：阅读架构文档

- **目标文件**：[`docs/process_model_and_site_isolation.md`](https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md)
- **检索定位**：检索关键词 `Goals` 以及 `Site Isolation`。
- **考察问题**：
  Chromium 当前文档把 Site Isolation 与哪些安全威胁联系起来？除 compromised renderer 之外，哪一类**现代微架构攻击**显著改变了同进程跨站数据的威胁模型，并推动 Chromium 使用更强的跨站进程/数据隔离？
- **实证记录**：
  当前 Chromium process-model 文档把**被攻破的 Renderer** 与 **Spectre-like speculative-execution threats** 作为 Site Isolation 的核心安全动机之一。其目标是尽量避免把其他 site 的敏感数据放进攻击者可执行代码所在的同一进程/可达数据面，并通过 process locks 与浏览器侧策略强化隔离。课程不把这扩展成“任何同进程脚本都能读全部数据”或“进程边界能彻底消灭所有侧信道”。
- **停止确认**：已在 Goals / Motivation 部分停止，未进入平台定制与历史演进章节。

### 任务 2（进程分配调度）：检查 `SiteInstanceImpl`

- **目标文件**：[`content/browser/site_instance_impl.cc`](https://chromium.googlesource.com/chromium/src/+/main/content/browser/site_instance_impl.cc)
- **检索定位**：定位方法 `SiteInstanceImpl::GetProcess()` 及其调用的 `SiteInstanceImpl::GetOrCreateProcess()`。
- **考察问题**：
  当一个页面上下文请求其绑定的渲染进程时，Chromium 是直接无条件执行 `fork()` 创建一个全新进程，还是存在进程复用策略？代码中调用了哪些关键判断条件？
- **实证记录**：
  当前源码显示 `GetProcess()` / `GetOrCreateProcess()` 并不是“每次导航无条件新建 Renderer”：它会结合 SiteInstanceGroup、process reuse policy、`ShouldUseProcessPerSite()`、`CanPutSiteInstanceInDefaultGroup()` 等当前实现状态决定获取/复用进程。具体函数与分支名属于该 revision 的 Chromium implementation evidence；本考察在这些入口条件处停止，不追踪 `RenderProcessHost` 初始化。
- **停止确认**：已在进程选择与组归属判断处停止，未跟踪 Mojo 管道初始化。

### 任务 3（中心化安全仲裁）：检查 `ChildProcessSecurityPolicy`

- **目标文件**：[`content/browser/security/cpsp/child_process_security_policy_impl.cc`](https://chromium.googlesource.com/chromium/src/+/main/content/browser/security/cpsp/child_process_security_policy_impl.cc)
  *(路径现时性说明：在最新 Chromium 重构中，该文件位于 `content/browser/security/cpsp/` 目录下)*
- **检索定位**：定位方法 `ChildProcessSecurityPolicyImpl::CanAccessDataForOrigin(...)`。
- **考察问题**：
  该方法接收哪些关键参数来判定一个渲染进程是否有权访问某个源的数据？它如何处理不透明源（Opaque Origin）？
- **实证记录**：
  在本次检查 revision 中，`CanAccessDataForOrigin(child_id, origin)` 把 calling child/process identity 与目标 origin 送入浏览器侧 origin/data-access policy 路径；当前源码还包含 opaque-origin precursor 与 process-lock/current security state 相关检查。结论只限这条**选定的 browser-side policy path**，不能说 Chromium 所有 Cookie、文件、网络响应或 IPC 权限都由这一个函数统一裁决。
- **停止确认**：已在 origin 锁匹配与 access_type 入口处停止，未跟踪复杂的文件路径特例。

### 任务 4（抽象与实现的差异辨析）：反思“一站一进程”

- **反思问题**：
  为什么不能简单地把 Chromium 的多进程实现宣称为“一个网站严格等于一个操作系统进程”？
- **实证结论**：
  **Full Site Isolation 也不等于“一 site 只有一个 process”。** 更准确的心智是：跨 site 内容需要满足更强的 process/site-lock separation，而一个 site 可以对应多个进程，多个 SiteInstance 也可能按当前策略发生 process reuse。Partial/No Site Isolation 与资源/平台策略会进一步改变拓扑，因此 Tab、site、SiteInstance 和 OS process 都不是固定一一映射。

### 任务 5（实证版本与元数据记录）：源头版本追踪

作者在 **2026-09-04** 对这条三锚点路线做过 currentness recheck；该作者快照只证明“当时路线可用”，**不是 learner 应复制的 revision**。

学习者每次考察都必须自行记录：
- **实际检查时间**：`<your actual timestamp>`
- **考察分支/ref**：例如 `refs/heads/main`
- **实际检查 Commit**：`<your exact Chromium revision>`
- **源码访问状态**：`LIVE_CHROMIUM_SOURCE_ACCESSIBLE` 或 `NO LIVE CHROMIUM SOURCE RECHECK`

若无法访问官方 Gitiles，不得沿用作者旧 commit 冒充 live inspection；此时只能把仓库内 Research/Design 作为 **REFERENCE EVIDENCE ONLY**。

---

## 4. 考察总结与概念连接

通过本次 Source Expedition，我们在真实世界最大型系统软件中印证了两个核心理论：
1. **进程（Process，EC-CON-018）提供重要的 OS 地址空间隔离边界**：Chromium Site Isolation 利用进程边界与 process locks，把不同 site 的敏感数据更强地分离，降低 Renderer compromise 与 Spectre-like 风险面；它与 sandbox、browser-side validation、network/data plumbing 等共同构成纵深防御，而不是“唯一有效防线”。
2. **浏览器侧仲裁体现 Trust Boundary（EC-CON-017）**：`ChildProcessSecurityPolicyImpl` 是 Chromium browser-side security reference-monitor 体系的一部分，为选定的 child permissions / origin-data access 做检查。其他资源还有各自 policy/subsystem，不能概括成“所有系统级请求都经过一个函数”。

---

## 5. 版权与规范声明

- Chromium 主项目包含 BSD-style licensed code，也包含带独立 license/notice 的第三方内容；不能用一条 blanket license 结论覆盖整棵源码树。
- 本实验采取 link-and-inspection-first：不镜像、不分发 Chromium 源码。任何实际摘录都必须针对**具体文件**重新核对 license/header/notice 与 attribution 要求。
