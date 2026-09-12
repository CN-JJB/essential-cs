# Resource-First Curriculum Policy

Status: **ACTIVE — Web Lead scope decision for v1.0**
Date: 2026-09-12

## Purpose

Essential CS is a self-study roadmap, not a requirement to reproduce a university, operating system, database, cloud platform, browser, or distributed-systems lab stack inside this repository.

The project therefore adopts a **resource-first** completion model for v1.0.

The repository's primary job is to give a learner:

1. a coherent map of the important computer-science and computer-systems concepts;
2. a recommended learning order and prerequisite structure;
3. high-confidence explanations of the mechanism-level ideas that connect those concepts;
4. authoritative or well-established external resources for deeper study;
5. bounded learning advice: what to observe, what to ask, what to practice, and what not to over-focus on yet;
6. currentness/provenance notes where facts materially change over time.

## Product boundary

For v1.0, **coverage + routing + resource quality** are the required product. Large repo-owned implementations are not required merely to prove that a topic exists.

Existing Lessons, Required Labs, Optional Labs, Source Expeditions, canonical CI assets, and the Mini Cloud implementation are retained because they are useful optional companions and historical evidence. They are **not required learning dependencies** for a learner who prefers external primary resources.

A learner may satisfy a module by using the recommended external resource and doing an equivalent bounded observation/exercise. The repository should not imply that its own implementation is uniquely canonical when a stronger external teaching resource exists.

## AI authoring rule

AI should preferentially contribute where confidence is high:

- map concepts and prerequisites;
- summarize stable mechanisms;
- locate and compare authoritative resources;
- distinguish stable fundamentals from current practice;
- propose bounded exercises, observation prompts, and transfer questions;
- explain trade-offs and common misconceptions;
- periodically re-check time-sensitive sources and links.

AI should **not** expand the curriculum by inventing large bespoke systems merely for completeness when the pedagogical value is uncertain. When a high-quality external course, textbook, standard, or official documentation already teaches the mechanism better, link to it and explain how to use it.

## v1.0 acceptance standard

The curriculum is content-complete when all of the following hold:

- M00–M24 remain covered by the accepted Core map;
- every Core Module has a clear learner goal, prerequisite context, and stopping point;
- every Core Module has at least one recommended primary resource or authoritative source route;
- important topics with materially different teaching styles have an optional secondary/deep-dive resource;
- resource roles are explicit: `PRIMARY`, `REFERENCE`, `DEEP DIVE`, or `CURRENT PRACTICE`;
- volatile resources or claims carry a currentness note/check date where useful;
- resource/licensing boundaries are respected: link-and-summarize by default, no unauthorized vendoring;
- the roadmap tells learners what to learn from a source rather than merely dumping links;
- existing repo-owned labs/projects are clearly marked as optional companions unless a learner deliberately chooses that path;
- no critical factual, routing, broken-link, provenance, or lifecycle contradiction remains in the active learner surface.

## What is no longer a v1.0 release blocker

Under this policy, the following are useful quality-improvement activities but are **not required to declare the resource-first curriculum complete**:

- completing every repo-owned Required Lab on every learner machine;
- requiring the Mini Cloud project as the universal final project;
- requiring a fresh independent multi-role execution of all repo-owned CI artifacts solely as a curriculum-completeness condition;
- requiring a real-human M00–M01 pilot before publishing the roadmap;
- requiring learners to use the canonical container/image rather than an external course's supported environment.

These activities may continue after v1.0 as optional validation, maintenance, or teaching research.

## Stability and uncertainty

Essential CS should be assertive about stable fundamentals and modest about uncertain pedagogy.

Use the following mental model:

- **STABLE** — mechanism or concept unlikely to change materially (e.g. virtual memory, transactions, asymptotic analysis);
- **CURRENT** — implementation practice, protocol status, tool version, or ecosystem convention that should be periodically re-checked;
- **FRONTIER** — actively changing or unsettled material; teach the durable principle and point to current sources rather than freezing one answer.

The repository should explicitly say when a recommendation is a design judgment rather than a proven optimal learning sequence.

## Maintenance model

Maintenance focuses on:

1. broken links;
2. obsolete standards/current-practice references;
3. resource replacements when a better public source becomes available;
4. missing concept coverage or prerequisite routing;
5. misleading summaries or overclaims;
6. licensing/provenance changes.

Large new code surfaces require a clear pedagogical reason. "We can build it" is not sufficient justification.

## Lifecycle note

This policy supersedes the earlier stable-gate assumption that repository-owned execution, independent multi-role verification, and a real learner pilot are mandatory prerequisites for publishing the **resource-first curriculum** as v1.0.

Historical audits, CI runs, Labs, Mini Cloud work, and v0.9 records remain valid historical project evidence; this policy does not rewrite or invalidate them.
