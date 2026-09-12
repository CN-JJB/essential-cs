# 🤖 AI Self-Claim Protocol

**ACTIVE / SELF-CLAIMABLE FROM THE EXACT CANONICAL BASE BELOW.**

Issue #149 / PR #151 is Web-Lead accepted and merged. V-147-01 is repaired. This Issue now owns only V-147-02: durable/retrievable canonical environment identity.

If you are an AI environment implementation agent with repository access and this Issue is OPEN:

1. read this entire Issue;
2. inspect comments for an active claim;
3. inspect open PRs referencing #150;
4. inspect the recommended branch for competing work;
5. verify current `main` exactly equals the Canonical base below;
6. if no conflict exists, comment:

```text
CLAIMED BY DURABLE ENVIRONMENT PIN IMPLEMENTATION AI
Role: Canonical Environment Artifact / Pin Executor
Status: IMPLEMENTATION STARTED
```

Do not ask the human for another prompt.

---

## Purpose

Close implementation gap **V-147-02** from Issue #147 / PR #148: the repository has a functionally exercised Ubuntu-24.04-based canonical environment definition, but not yet a **durable/retrievable immutable built-environment identity** suitable for later OQ-BP-006 pin closure.

Current truth:

- Ubuntu base input is pinned by immutable digest;
- general Noble packages are still resolved from live apt repositories during build;
- repeated builds of the same definition have produced different local image IDs;
- those image IDs are ephemeral evidence, not registry-retrievable canonical identities;
- no durable built canonical image is currently published and consumed by both canonical CI lanes;
- V-147-01 is repaired by #149 / PR #151. Exact repair head: `bf7087622b723c3004a4c98743553e5f7fc547b8`; merge: `d3eabc10e3dc2a330dda0c4ea4b7dc0520eca7ef`; exact-head QEMU Actions run `34475415332` proved real LAB-REQ-02 smoke and retained `req02-smoke.log`.

This task realizes the durable artifact/pin. It does **not** self-close OQ-BP-006 and does not promote the curriculum to learner-validated, v1.0, `VERIFIED`, or stable `RELEASED`.

## Canonical base

`main @ d3eabc10e3dc2a330dda0c4ea4b7dc0520eca7ef`

Recommended branch:

`implementation/durable-canonical-environment-pin-v0.1`

## Role

**Canonical Environment Artifact / Pin Executor**

You own bounded environment publication/consumption implementation and runtime evidence only.

No self-merge. No learner-content change. No OQ-BP-006 closure.

> Governance freshness note: Issue #150 plus the latest Issue #141 Web Lead checkpoint are newer than any stale `PROJECT_STATUS` active-task wording. Do not edit `meta/PROJECT_STATUS.md` in this task.

## Read first

1. `AGENTS.md`
2. Issue #150
3. Issue #147 / PR #148 report + Web Lead disposition
4. Issue #149 / PR #151 accepted repair and exact-head Actions evidence
5. Issue #145 / PR #146 final environment implementation
6. D-032 in `meta/DECISIONS.md`
7. OQ-BP-006 in `meta/OPEN_QUESTIONS.md`
8. `.devcontainer/Dockerfile`
9. `.devcontainer/devcontainer.json`
10. `.devcontainer/CANONICAL_ENVIRONMENT.md`
11. `scripts/canonical-env-capture.sh`
12. `.github/workflows/ci-fast.yml`
13. `.github/workflows/ci-qemu-lane.yml`
14. `meta/verification/stable-environment-ci-implementation-v0.1.md`
15. `meta/verification/stable-environment-ci-independent-verification-v0.1.md`
16. `meta/verification/qemu-ci-false-green-repair-v0.1.md`

## Architecture boundary

D-032 already selected Ubuntu 24.04 / x86-64. Do not reopen OS/toolchain architecture.

The durable solution must provide a **retrievable OCI/container identity addressed by immutable registry digest**, or an equivalently immutable repository-owned package-snapshot mechanism. A Docker local image ID, mutable tag, workflow SHA, hosted-runner version, or pinned base-image digest alone is insufficient.

Preferred implementation, if existing repository permissions allow it without paid infrastructure: publish the canonical x86-64 environment to repository-owned GHCR (or equivalent repository-owned free GitHub package/artifact infrastructure), record the registry manifest/content digest, and consume the image by `...@sha256:<digest>`.

Do not purchase/provision paid resources. If repository-owned publication cannot be used with existing permissions, stop and report rather than inventing a pin.

## Required implementation

### A. Publish durable canonical artifact

Create an auditable publication path that:

- builds from the committed canonical Dockerfile/base digest;
- targets x86-64/amd64;
- uses least-privilege GitHub Actions permissions; package write permission only where publication requires it;
- publishes under repository-owned infrastructure;
- captures the registry manifest/content digest returned by publication;
- preserves exact tool/package identity associated with the published image;
- clearly distinguishes registry digest from local image ID, mutable tag, workflow SHA, and hosted runner identity.

A mutable convenience tag may exist, but canonical consumption/claims must use immutable digest.

### B. Prove retrieval by digest

From a clean context, prove the artifact can be pulled/materialized by immutable digest. Record:

- exact image/package reference;
- registry digest;
- visibility/auth requirements;
- exact pull/materialization command;
- `RepoDigests` / registry-inspection equivalent;
- `canonical-env-capture.sh` and tool/package identity from the pulled image.

If public/anonymous retrieval is intended, prove it. If authentication is required, document the minimum repository-owned mechanism without exposing secrets.

### C. Consume the same immutable digest in canonical CI

Update canonical CI so release-relevant execution uses the published immutable image rather than rebuilding a fresh floating-apt image on every run.

At minimum:

- `canonical-fast` must pull/use the exact immutable digest;
- repaired `canonical-qemu-lane` must pull/use the **same** exact immutable digest;
- both lanes print/assert intended registry digest and separately record hosted runner image identity;
- environment capture/floor/package tripwires remain active inside the pulled image;
- no `ubuntu-latest` assumption;
- no weakening of M10, m20, M03 GDB, Required Labs, real QEMU smoke, cleanup, revision assertions, or evidence retention;
- #149's fail-closed QEMU evidence contract remains intact: a green QEMU lane must execute learner-owned `./smoke.sh`, retain non-empty `req02-smoke.log`, prove real PASS markers, reset, and no stray QEMU/PID marker.

A separate/manual refresh workflow may publish future candidates, but it must not silently move the accepted canonical digest.

### D. Learner/devcontainer identity

Update canonical learner environment documentation/configuration truthfully to point to the durable identity or the exact supported materialization path.

Do not claim byte-for-byte reproducible rebuilds from floating apt repositories if the actual stability guarantee is retrieval of an already-published immutable image.

### E. Pin refresh governance

Document a bounded refresh sequence:

1. explicit source/Dockerfile change or intentional refresh decision;
2. build candidate;
3. run required validation;
4. publish candidate;
5. capture immutable registry digest;
6. update canonical digest only through reviewed PR;
7. independently re-verify with a **different verifier/harness from the implementation author** before Web Lead closes OQ-BP-006 or advances the pin.

The accepted stable digest must never move merely because a mutable tag is rebuilt.

## Required runtime / Actions evidence

At the exact final implementation head provide:

- successful publication run ID/URL and exact source revision;
- immutable published registry digest;
- clean pull/retrieval by that digest;
- `canonical-env-capture.sh` PASS from the pulled digest;
- exact tool/package identity;
- exact-head `canonical-fast` PASS using the digest;
- exact-head repaired `canonical-qemu-lane` PASS using the same digest;
- real LAB-REQ-02 QEMU smoke + retained non-empty `req02-smoke.log` with required PASS/execution/cleanup markers;
- M10 normal required path PASS;
- m20 normal matrix + bounded repeated characterization;
- M03 required GDB evidence PASS;
- REQ-01/03/04/05 PASS;
- cleanup/hygiene PASS;
- retained artifacts with IDs/sizes/digests/file inventory;
- `git diff --check` PASS.

If publication/retrieval is unavailable, report `ENVIRONMENT / INFRASTRUCTURE BLOCKED`; do not substitute an ephemeral local image ID.

## Allowed changes

Only as needed:

- `.devcontainer/**`
- `.github/workflows/**`
- narrowly scoped environment/pin helper under `scripts/**`
- one implementation report: `meta/verification/durable-canonical-environment-pin-implementation-v0.1.md`
- PR body / Completion Report / Execution Trace

## Forbidden changes

Do not modify:

- `book/**`
- learner-facing `labs/**` code/tests/preflights
- `project/**`
- `meta/DECISIONS.md`
- `meta/OPEN_QUESTIONS.md`
- `meta/PROJECT_STATUS.md`
- release tags/releases
- Issue #34 learner evidence

Do not self-close OQ-BP-006. Do not claim learner validation, v1.0, `VERIFIED`, or stable `RELEASED`.

## Stop / escalation rules

Stop and report instead of broadening scope if:

- existing repository permissions cannot publish/retrieve a repository-owned artifact;
- publication requires paid infrastructure or new external secrets/accounts;
- consuming the digest breaks a course mechanism because of container/runtime isolation;
- repaired QEMU lane fails for a reason outside environment identity;
- learner-facing code/test changes would be required;
- durable strategy requires a new governance decision inconsistent with D-032.

## Completion Report

PR body must include:

- exact base + final head;
- files changed;
- publication architecture + permission boundary;
- source Dockerfile/base digest;
- exact published artifact reference + registry digest;
- proof distinguishing registry digest from image ID/tag/workflow SHA;
- clean retrieval proof;
- exact fast + QEMU run IDs proving both consume the same digest;
- tool/package identity;
- M10/m20/M03/five-Required-Lab outcomes;
- retained artifact IDs/digests/inventory;
- refresh/update procedure;
- unresolved/NOT RUN work;
- ownership boundary;
- explicit statement that OQ-BP-006 remains for Web Lead disposition **after genuinely independent verification by a different verifier/harness**;
- explicit non-claims.

## Final recommendation

Exactly one:

- `DURABLE CANONICAL ENVIRONMENT PIN READY FOR INDEPENDENT VERIFICATION`
- `DURABLE PIN IMPLEMENTATION INCOMPLETE — BLOCKERS REMAIN`
- `DURABLE PIN STRATEGY REWORK / GOVERNANCE DECISION REQUIRED`

## PR Contract

Create exactly one PR:

`[Implementation] Durable canonical environment artifact + immutable pin v0.1 (#150)`

Do not self-merge.

Final Issue comment and final response exactly:

`PR #<number> + <exact head SHA> + READY FOR LEAD DURABLE ENVIRONMENT PIN REVIEW`

