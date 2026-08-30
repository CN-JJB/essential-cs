# Lab Design Policy

## Purpose

Hands-on work exists to create understanding, not to maximize implementation.

## Default strategy

**Adopt → Adapt → Build**

1. Search for classic, proven experiments/projects from strong university courses, textbooks, official examples, and mature open-source projects.
2. Adopt directly when it fits.
3. Adapt when teaching scope, reproducibility, safety, or cognitive load requires it.
4. Build custom only when existing options are insufficient.

Do not create a shallow custom demo merely because AI can generate one quickly.

## Teaching loop

Prefer:

- Build → Observe → Break → Explain
- Reveal → Use → Inspect

Reveal the minimum mechanism needed, use a mature real tool, then inspect what the abstraction hides.

## Real mechanisms

When a real mechanism can be safely and clearly observed, prefer it to a fake simulation.

Core labs must be reproducible in the canonical Linux environment. Other platforms are convenience support.

## Required lab qualities

A Core lab should, where applicable, define:

- learning objective;
- prerequisites;
- prediction/checkpoint;
- environment and data;
- commands/code;
- expected observation;
- explanation;
- controlled failure/break step;
- cleanup/reset;
- exit criteria;
- provenance/license;
- relation to concepts, competencies, and Mini Cloud App.

## Security labs

Use **Real mechanism, safe target**:

- local;
- sandbox;
- course-owned vulnerable app;
- explicitly authorized target.

Teach security defense-first and mechanism-aware. This is not penetration-testing training.

## Measurement

Benchmarks/measurements must state target metric, environment/data scale, warmup/steady state, repetitions/distribution when relevant, and distinguish microbenchmarks from real workloads. A benchmark does not by itself prove cause.

## Source Expeditions

Use short, constrained real-source excursions after principles:

- identify 1–3 relevant locations;
- compare reality with the mental model;
- state what can be ignored;
- include an explicit stopping point.
