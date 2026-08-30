# Release & Maintenance Policy

## Versions

Planned progression:

- `v0.1` — Curriculum Blueprint
- `v0.2–v0.x` — construction and pilots
- `v0.9` — release candidate / first full Core traversal
- `v1.0` — first stable curriculum

## v1.0 gate

Do not call the project v1.0 until:

- the complete Core spine is teachable;
- the Mini Cloud App evolution is complete;
- all REQUIRED labs are runnable and documented;
- provenance and licenses are in order;
- content has passed multi-role verification;
- target learners have validated key Core paths;
- an external curriculum/coverage audit is complete;
- maintenance/review workflows are actually operating;
- no critical blockers remain.

## Stable environment

Stable releases should pin a reproducible canonical lab environment and key software versions.

`main` may forward-test newer versions.

Tests should prefer invariants/trends over brittle exact command output where versions legitimately differ.

## Errata & Hotfix

A serious released technical/pedagogical error is a **Critical Content Bug**.

Process:

1. confirm error and impact scope;
2. identify the canonical concept/lesson and contextual revisits;
3. fix `main`;
4. issue a patch release when Stable users are affected;
5. record Errata and release notes;
6. notify learners when the error materially changes understanding or lab behavior.

Do not rewrite historical release tags.

Revert and patch releases such as `v1.0.1` are allowed.

## Learner validation

AI-simulated learners do not replace real target learners. Stable v1.0 requires evidence from learners with basic programming experience and no formal CS background, including friction, misconceptions, environment failures, timing, and transfer observations.
