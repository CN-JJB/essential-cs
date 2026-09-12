# Essential CS

Essential CS is a rigorous, self-study-first **computer science learning roadmap and resource guide** for learners with basic programming experience but no formal CS background.

Its goal is not to compress a four-year degree, maximize implementation, or reproduce every university lab inside this repository. The goal is to build an accurate modern computing-system world model and the ability to trace, explain, observe, diagnose, reason about correctness, judge trade-offs, estimate scale/cost, and independently learn unfamiliar technologies.

## 第一次来？只做这 4 步

1. **打开 [`LEARNING_ROADMAP.md`](LEARNING_ROADMAP.md)。** 不要先翻 `meta/`，也不要从 `labs/` 开始。
2. 在顶部 **M00–M24 一键索引**中进入当前模块。
3. 当前模块只学习它点名的 **Core lecture / chapter / RFC section / manual page**；不要默认把整门外部课程或整本书学完。
4. 完成该模块的 **Checkpoint**，然后点页面里的 **Next → Mxx**。能解释机制、做出一个正确预测并知道去哪里查证，就可以继续。

> 默认路线：**M00 → M01 → … → M24**。仓库 Lessons 是中文导览/综合材料；Labs 与 Mini Cloud 是可选实践，不是继续路线的硬门槛。

- **唯一默认学习入口：** [`LEARNING_ROADMAP.md`](LEARNING_ROADMAP.md)
- **学生路径验收规则：** [`meta/STUDENT_ROUTE_ACCEPTANCE.md`](meta/STUDENT_ROUTE_ACCEPTANCE.md)
- **课程架构地图（需要全局结构时再看）：** [`meta/CURRICULUM_MAP.md`](meta/CURRICULUM_MAP.md)
- **Resource-first policy：** [`meta/RESOURCE_FIRST_CURRICULUM_POLICY.md`](meta/RESOURCE_FIRST_CURRICULUM_POLICY.md)
- **中文 Lessons：** [`book/`](book/)

## 学习模型

> **具体知识点 → 精确外部资源片段 → bounded observation/practice → checkpoint → 下一模块**

路线图中的资源必须明确到具体 lecture、chapter、RFC section、manual page 或官方文档小节。只写“学 MIT 6.006”“读 OSTEP”“看 15-445”“读官方文档”是不够的。

Repo-owned Labs and the Mini Cloud project remain available as **optional guided companions**. They are useful when you想多做一次受控实践，但不要求每个学习者重复仓库的全部工程验证。

## What this repository provides

- M00–M24 Core coverage across computation, machines, operating systems, networking, web/browser systems, databases, concurrency, distributed systems, infrastructure, observability, security, and systems judgment;
- a direct M00–M24 route with explicit `Next` navigation;
- a knowledge-point-to-resource mapping precise enough to tell you **which part** of a larger course/book/standard to use;
- concise Chinese-first teaching material with English terminology introduced where useful;
- `Core / Reference / Optional deep dive / Repo companion` resource levels;
- module checkpoints and “what to ignore for now” boundaries;
- optional repo-owned labs, source expeditions, Mini Cloud exercises, and evidence templates;
- provenance/currentness discipline for claims that change over time.

## Resource philosophy

Prefer authoritative and established sources over bespoke reinvention.

Good AI contributions are high-confidence mapping, explanation, source discovery/comparison, currentness checks, and bounded exercise ideas. Large new implementations require a clear pedagogical reason; “we can build it” is not enough.

For current standards, product behavior, or ecosystem practice, verify against current primary sources. For stable mechanisms, focus on durable mental models rather than version trivia.

## Existing implementation assets

The repository already contains substantial optional hands-on material under `labs/`, `project/`, `scripts/`, and `tests/`. These assets are retained and useful, but v1.0 curriculum completeness is defined primarily by **coverage, routing, resource quality, and truthful learning guidance**, not by requiring every learner to reproduce all repository-owned execution evidence.

## Source of truth / governance history

GitHub is the persistent project memory. Chat sessions and AI outputs are working contexts, not authoritative project state.

For governance/history, see `AGENTS.md`, `meta/PROJECT_STATUS.md`, `meta/CURRICULUM_INVARIANTS.md`, `meta/DECISIONS.md`, `meta/OPEN_QUESTIONS.md`, and `meta/blueprint/README.md`.

Where older governance text assumes every repo-owned lab/project/verification gate is mandatory for publishing the curriculum, the newer resource-first policy governs the v1.0 learner-product scope; historical records remain historical truth.

## Canonical language

Chinese is the canonical teaching language. Important technical terms include English on first introduction.

## Licensing intent

Original educational content, curriculum design, and original diagrams: **CC BY-SA 4.0**.

Original code, tools, and the Mini Cloud App: **Apache-2.0**.

Third-party material retains its own license. Essential CS links to and summarizes external resources by default rather than vendoring third-party teaching material without clear permission.
