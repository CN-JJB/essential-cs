# Essential CS

Essential CS is a rigorous, self-study-first **computer science learning roadmap and resource guide** for learners with basic programming experience but no formal CS background.

Its goal is not to compress a four-year degree, maximize implementation, or reproduce every university lab inside this repository. The goal is to build an accurate modern computing-system world model and the ability to trace, explain, observe, diagnose, reason about correctness, judge trade-offs, estimate scale/cost, and independently learn unfamiliar technologies.

## Start here

- **Learner roadmap:** [`LEARNING_ROADMAP.md`](LEARNING_ROADMAP.md)
- **Canonical curriculum map:** [`meta/CURRICULUM_MAP.md`](meta/CURRICULUM_MAP.md)
- **Resource-first scope policy:** [`meta/RESOURCE_FIRST_CURRICULUM_POLICY.md`](meta/RESOURCE_FIRST_CURRICULUM_POLICY.md)
- **Lessons:** [`book/`](book/)

The recommended learning model is:

> **knowledge map → strong external primary resource → bounded observation/practice → explanation/transfer question**

Repo-owned Labs and the Mini Cloud project remain available as **optional guided companions**. They are not mandatory for a learner who prefers stronger external courses, books, standards, or official documentation for a topic.

## What this repository provides

- M00–M24 Core coverage across computation, machines, operating systems, networking, web/browser systems, databases, concurrency, distributed systems, infrastructure, observability, security, and systems judgment;
- a recommended prerequisite/order map;
- concise Chinese-first teaching material with English terminology introduced where useful;
- curated primary/reference/deep-dive resources;
- learning advice, checkpoints, misconceptions, and "what to ignore for now" boundaries;
- optional repo-owned labs, source expeditions, Mini Cloud exercises, and evidence templates;
- provenance/currentness discipline for claims that change over time.

## Resource philosophy

Prefer authoritative and established sources over bespoke reinvention.

Good AI contributions are high-confidence mapping, explanation, source discovery/comparison, currentness checks, and bounded exercise ideas. Large new implementations require a clear pedagogical reason; "we can build it" is not enough.

For current standards, product behavior, or ecosystem practice, verify against current primary sources. For stable mechanisms, focus on durable mental models rather than version trivia.

## Existing implementation assets

The repository already contains substantial optional hands-on material under `labs/`, `project/`, `scripts/`, and `tests/`. These assets are retained and useful, but v1.0 curriculum completeness is defined primarily by **coverage, routing, resource quality, and truthful learning guidance**, not by requiring every learner to reproduce all repository-owned execution evidence.

## Source of truth

GitHub is the persistent project memory. Chat sessions and AI outputs are working contexts, not authoritative project state.

For governance/history, see:

- `AGENTS.md`
- `meta/PROJECT_STATUS.md`
- `meta/CURRICULUM_INVARIANTS.md`
- `meta/DECISIONS.md`
- `meta/OPEN_QUESTIONS.md`
- `meta/blueprint/README.md`

Where older governance text assumes every repo-owned lab/project/verification gate is mandatory for publishing the curriculum, the newer resource-first policy governs the v1.0 learner-product scope; historical records remain historical truth.

## Canonical language

Chinese is the canonical teaching language. Important technical terms include English on first introduction.

## Licensing intent

Original educational content, curriculum design, and original diagrams: **CC BY-SA 4.0**.

Original code, tools, and the Mini Cloud App: **Apache-2.0**.

Third-party material retains its own license. Essential CS links to and summarizes external resources by default rather than vendoring third-party teaching material without clear permission.
