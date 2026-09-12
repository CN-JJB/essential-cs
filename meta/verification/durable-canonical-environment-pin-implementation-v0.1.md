# Durable Canonical Environment Artifact + Immutable Pin — Implementation v0.1

**Task:** Issue #150 (closes gap **V-147-02** from Issue #147 / PR #148).
**Role:** Canonical Environment Artifact / Pin Executor.
**Governance:** D-032. **OQ-BP-006 remains OPEN.**

> This report is an implementation-author artifact. It is **not** independent
> verification. OQ-BP-006 may be closed only by the Web Lead after verification by a
> **different verifier/harness** than this implementation. No learner validation,
> v0.1.0/`v1.0`, `VERIFIED`, or stable `RELEASED` status is claimed anywhere here.

## 1. Result

A durable, retrievable, immutable canonical environment identity now exists and is
what both canonical CI lanes execute:

```text
ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
```

It is a single-architecture (`application/vnd.docker.distribution.manifest.v2+json`)
linux/amd64 image, published from this repository's own recipe into this
repository's own GHCR package, retrievable **without credentials**, and consumed by
`canonical-fast` and `canonical-qemu-lane` by that same digest.

## 2. Why the previous model could not be called a pin

Before this change both lanes ran `docker build -f .devcontainer/Dockerfile .` on
every run. The base image was digest-pinned, but general Noble packages were resolved
from live apt repositories at build time, so each run produced a different local
image ID. Those IDs are daemon-local and vanish with the runner.

That is not a theoretical concern. The scheduled `canonical-qemu-lane` run
`34572559147` on `main @ d3eabc10` **failed on 2026-09-11 before reaching any course
mechanism**, because the per-run build could not fetch a package:

```text
#6 521.3 E: Failed to fetch http://archive.ubuntu.com/ubuntu/pool/main/libe/liberror-perl/liberror-perl_0.17029-2_all.deb
            Unable to connect to archive.ubuntu.com:80: [IP: 185.125.190.83 80]
#6 ERROR: process "/bin/sh -c apt-get update && apt-get install -y --no-install-recommends ..." did not complete successfully: exit code: 100
```

A lane that must build its environment from the live network before it can test
anything has no durable identity and no reliable gate. This change removes build-time
apt resolution from release-relevant execution entirely.

## 3. Files changed

| File | Change |
| --- | --- |
| `.devcontainer/canonical-image.env` | **new** — the pin: `CANONICAL_IMAGE_DIGEST` plus recipe/base provenance and informational publication provenance |
| `scripts/canonical-image-publish.sh` | **new** — build from the committed recipe, push to repository-owned GHCR, capture the registry digest; cannot write the pin |
| `scripts/canonical-image-pull.sh` | **new** — materialize the canonical environment by digest only, fail-closed |
| `.github/workflows/publish-canonical-environment.yml` | **new** — least-privilege publication + clean-context retrieval proof + guarded verify-pin |
| `.github/workflows/ci-fast.yml` | both lanes' `canonical-fast` now pulls the committed digest instead of building |
| `.github/workflows/ci-qemu-lane.yml` | `canonical-qemu-lane` (qemu-smoke + m20 triage) pulls the **same** digest instead of building |
| `.devcontainer/CANONICAL_ENVIRONMENT.md` | rewritten around the durable identity, retrieval, and refresh governance |
| `.devcontainer/devcontainer.json` | materializes the pinned digest instead of rebuilding |

No `book/**`, learner-facing `labs/**`, `project/**`, `meta/DECISIONS.md`,
`meta/OPEN_QUESTIONS.md`, `meta/PROJECT_STATUS.md`, release tag, or Issue #34
evidence was touched. `.devcontainer/Dockerfile` was **not** modified: the published
digest was built from the committed recipe exactly as it stood.

## 4. Publication architecture and permission boundary

- Workflow `publish-canonical-environment`, run
  [34673360717](https://github.com/CN-JJB/essential-cs/actions/runs/34673360717),
  event `push`, source revision `25804b02cdd89bc3e2ff386aaf60f7c0b41b9032`.
- Permissions: `contents: read`, `packages: write`. Nothing else. No new secrets,
  accounts, or paid infrastructure; publication uses the repository-owned
  `GITHUB_TOKEN`.
- Build: `docker buildx build --platform linux/amd64 --provenance=false --sbom=false`
  from `.devcontainer/Dockerfile`; labels record the source repository and revision.
- Registry digest taken from buildx publication metadata
  (`containerimage.digest`) and cross-checked against
  `docker buildx imagetools inspect`.
- A **separate job on a fresh runner** (`retrieve-by-digest`) performed the
  clean pull-by-digest proof. The builder's local daemon cannot satisfy it.
- A guard step asserts the publication run did **not** modify
  `.devcontainer/canonical-image.env` (`PUBLISH_DID_NOT_MODIFY_PIN=YES`).

### Source recipe

- Dockerfile: `.devcontainer/Dockerfile`, git blob `51198ea12c3c9ddfa18a2246bddef491ea729559`.
- Base input: `ubuntu:24.04@sha256:224a1869083a311ef3f13648a154ba79832fbef6364d31493642ca03082da254`.
- Platform: `linux/amd64`.

### Identity separation (the point of the task)

| Field | Value | Role |
| --- | --- | --- |
| `registry_digest` | `sha256:766ce07b…19e460` | **THE PIN** — durable, content-addressed, retrievable |
| `config_digest` | `sha256:24a926a0…9d7805` | build output detail |
| `local_image_id` | `sha256:24a926a0…9d7805` | daemon-local, ephemeral — **NOT the pin** |
| mutable tags | `:candidate`, `:sha-25804b02…` | repointable labels — **NOT the pin** |
| `git_sha` | `25804b02cdd89bc3e2ff386aaf60f7c0b41b9032` | source revision — **NOT the pin** |
| `runner_image_version` | `20260907.300.1` | moving substrate — **NOT the pin** |

Note the deliberate near-collision: the local image ID happens to equal the config
blob digest. That is exactly why the pin is the **manifest** digest
(`766ce07b…`) and not the config digest or the local image ID.

## 5. Clean retrieval proof

From a fresh runner with no prior local images (`pre-pull-image-list.txt` contains
only GitHub's own runner images):

```text
PULL_BY_DIGEST_REFERENCE=ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
Name:      ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07b…19e460
MediaType: application/vnd.docker.distribution.manifest.v2+json
Digest:    sha256:766ce07b…19e460
Status: Downloaded newer image for ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07b…19e460
RepoDigests: ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07b…19e460
CLEAN_PULL_BY_DIGEST=PASS
```

### Credential-free (anonymous) retrieval

Verified independently of CI, with **no credentials**:

- `GET https://ghcr.io/v2/cn-jjb/essential-cs/canonical/manifests/sha256:766ce07b…19e460`
  with an anonymous pull token → `HTTP/1.1 200 OK`,
  `docker-content-digest: sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460`.
- Re-hashing the returned manifest bytes gives
  `766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460` — content
  addressing confirmed end to end.
- Config blob and layer blobs return `307` (CDN redirect) without credentials.

CI additionally uses the repository-owned `GITHUB_TOKEN` with `packages: read`.
No learner credentials are required, and no new secret was introduced.

## 6. Package / tool identity inside the pinned digest

`scripts/canonical-env-capture.sh` run **inside the image pulled from the pinned
digest** returned `CANONICAL_ENV_CAPTURE result=PASS` with every D-032 floor and both
lane tripwires satisfied:

```text
os=Ubuntu 24.04.4 LTS   arch=x86_64
CPython 3.12.3 | sqlite engine 3.45.1 | sqlite3 CLI 3.45.1 | gcc 13.3.0 (C11 OK)
gdb 15.1 (REQUIRED) | curl 8.5.0
qemu-system-misc 1:8.2.2+ds-0ubuntu1.18 | gcc-riscv64-unknown-elf 13.2.0-11ubuntu1+12
riscv64-linux-gnu-gcc 4:13.2.0-7ubuntu1 | binutils 2.42 | git 2.43.0 | bash 5.2.21
strace 6.8-0ubuntu2 (capability-gated)
```

Full resolved distro identity: `bash 5.2.21-2ubuntu4`, `bc 1.07.1-3ubuntu4`,
`binutils 2.42-4ubuntu2.10`, `binutils-riscv64-linux-gnu 2.42-4ubuntu2.10`,
`binutils-riscv64-unknown-elf 2.42-1ubuntu1+6`, `build-essential 12.10ubuntu1`,
`ca-certificates 20260601~24.04.1`, `curl 8.5.0-2ubuntu10.13`,
`gcc-riscv64-linux-gnu 4:13.2.0-7ubuntu1`, `gcc-riscv64-unknown-elf 13.2.0-11ubuntu1+12`,
`gdb 15.1-1ubuntu1~24.04.1`, `git 1:2.43.0-1ubuntu7.3`, `make 4.3-4.1build2`,
`perl 5.38.2-3.2ubuntu0.4`, `python3 3.12.3-0ubuntu2.1`,
`qemu-system-common/-data/-misc 1:8.2.2+ds-0ubuntu1.18`, `sqlite3 3.45.1-1ubuntu2.7`,
`strace 6.8-0ubuntu2`.

## 7. Exact-head lane evidence

### Head relationship

Two heads are relevant and they must not be confused:

- **Substantive implementation head `d2ca8556f4fd086edcf82e0d2b1197571a619dda`** — all
  executable content (pin file, helper scripts, publication workflow, both CI lanes,
  devcontainer docs/config). The runs cited immediately below were produced here.
- **Final head** — the commit that adds this report file. It changes **markdown only**
  (`meta/verification/durable-canonical-environment-pin-implementation-v0.1.md`); it
  alters no executable behaviour, no CI definition, and no pin. Both lanes were
  re-run green at that final head.

The final head's own run IDs cannot be cited *inside* the commit that precedes their
existence, so per the Issue #150 PR contract they are recorded in the PR body
("Exact-head Actions evidence at the final head"). Both heads consumed the identical
digest `sha256:766ce07b…19e460`.

### Runs at the substantive implementation head

Both lanes ran at `d2ca8556f4fd086edcf82e0d2b1197571a619dda` and consumed the
**same** digest:

| Lane | Run | Event | Result |
| --- | --- | --- | --- |
| `canonical-fast` | [34673666673](https://github.com/CN-JJB/essential-cs/actions/runs/34673666673) | `pull_request` | success |
| `canonical-qemu-lane` | [34673676055](https://github.com/CN-JJB/essential-cs/actions/runs/34673676055) | `workflow_dispatch` | success |
| `publish-canonical-environment` (verify-pin) | [34673576341](https://github.com/CN-JJB/essential-cs/actions/runs/34673576341) | `push` | success |

Both lanes' retained evidence bundles record the identical consumption identity:

```text
COMMITTED_CANONICAL_DIGEST=sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
CONSUMED_CANONICAL_IMAGE=ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07b…19e460
DIGEST_CONSUMPTION_ASSERT=PASS
RECIPE_BLOB_MATCH=YES
REPO_DIGESTS_CONTAIN_PIN=YES
```

`canonical-fast` outcomes: 26/26 Python suites `SUITE_PASS` (including
`labs/foundations/m10` and `labs/foundations/m20`), M03 canonical evidence with
required GDB trace (`SMOKE result=PASS`), Required Lab harnesses 01/03/04/05 with
resets, shared preflights PASS, shell syntax gates PASS, hygiene PASS
(includes `git diff --check <base>...HEAD`).

`canonical-qemu-lane` outcomes: real learner-owned LAB-REQ-02 smoke,
`REQ02_SMOKE_EVIDENCE: FAIL-CLOSED POSTCONDITION PASS`, `REQ02_CLEANUP_TRUTH_DONE`,
`QEMU_EVIDENCE_COMPLETE: FAIL-CLOSED GATE PASS`. Retained `req02-smoke.log` is
**41 476 bytes** and contains every required marker:

```text
LAB_REQ_02_OK                       (standalone line 145)
QEMU_SMOKE_STATUS: PASS
QEMU_REAPED: TRUE
PID_MARKER_CLEAN: YES
=== LAB-REQ-02 Smoke Test PASS ===
```

The m20 diagnostic triage characterized the trio 5/5 `PASS`
(`TRIO_RUN_1..5=PASS`); it remains non-blocking and is not cited as stable-green
evidence.

The #149 fail-closed QEMU contract was not weakened: the smoke command, the
postcondition greps, the cleanup-truth job, and the evidence-completeness gate are
byte-identical to the #149 repair; only the image-acquisition step changed.

### The push guard was exercised

Run `34673576341` was a `push` **after** a real digest was committed. It classified
as `verify-pin`, skipped `publish-candidate` entirely, and produced
`COMMITTED_PIN_RETRIEVABLE=PASS`. A push can therefore no longer publish or move the
accepted pin.

## 8. Retained artifacts

| Run | Artifact | ID | Size (B) | Digest |
| --- | --- | --- | --- | --- |
| 34673360717 | `canonical-publish-evidence` | 10291063296 | 2899 | `sha256:fd8c1ee7997e8cd535ad02b458df71e8b55aeec155932f230a76010b432e30ff` |
| 34673360717 | `canonical-retrieval-evidence` | 10291412766 | 2806 | `sha256:81dd67a5103544cb1775d6ade136ce4110f5c698b14f99e5e3277c85bfa3ec27` |
| 34673576341 | `canonical-pin-verification-evidence` | 10291108604 | 2813 | `sha256:8782c517e109ddbb07dea82827e878081f352cfcc81d26b14c818857d69488d3` |
| 34673666673 | `canonical-fast-evidence` | 10291338272 | 9658 | `sha256:e6ba90c2ed2e1e82b3ddb395088212baebb6c4c6d3cfa967a47d7da7c9cf6649` |
| 34673676055 | `canonical-qemu-evidence` | 10291343217 | 9514 | `sha256:b57ee4e63a99c42b06d818bc4d2b6fea5706a7e134466ca6d668279bf4f0bbad` |
| 34673676055 | `canonical-m20-triage` | 10291537924 | 1023 | `sha256:13aeb60bacf50ff69b6181c83105ed96891c0c4436013e08c11f68a34841c192` |

File inventories (bytes): publish bundle — `build-metadata.json` 1532,
`config-digest.txt` 72, `identity.txt` 1047, `imagetools-inspect.txt` 268,
`registry-digest.txt` 72, `substrate.txt` 484, `visibility.txt` 498; retrieval
bundle — `canonical-env-snapshot.txt` 3466, `pre-pull-image-list.txt` 334,
`retrieval-context.txt` 203, `retrieval-imagetools-inspect.txt` 268,
`retrieval-local-image-id.txt` 72, `retrieval-repodigests.txt` 111; fast bundle —
`canonical-digest-consumption.txt` 549, `canonical-env-snapshot.txt` 3466,
`harness-req01.log` 4005, `harness-req03.log` 1138, `harness-req04.log` 1835,
`harness-req05.log` 1217, `m03-smoke.log` 1054, `preflights.log` 11432,
`python-matrix.log` 4843; qemu bundle — `canonical-digest-consumption.txt` 554,
`qemu-env-snapshot.txt` 3466, `qemu-lane-outer.log` 43342, `req02-preflight.log` 576,
`req02-setup.log` 388, `req02-smoke.log` 41476, `req02-source-route.log` 566.

## 9. Reproducibility boundary (stated honestly)

**Not claimed:** that rebuilding `.devcontainer/Dockerfile` from live Noble apt
repositories on a later date yields the same image. It does not, and the 2026-09-11
build failure above shows the recipe is not even reliably re-buildable on demand.

**Claimed:** the published immutable image can be retrieved by digest for as long as
the package exists, and that retrieval is the canonical stability guarantee. Every
environment a canonical lane executes is that published digest.

## 10. Pin refresh governance

1. Explicit Dockerfile/source change or an intentional refresh decision — never an
   automatic rebuild.
2. Build a candidate (`workflow_dispatch`, `mode: publish-candidate`).
3. Run the required validation against the candidate.
4. Publish to repository-owned GHCR.
5. Capture the immutable registry digest.
6. Update the canonical digest **only through a reviewed PR**, together with
   `CANONICAL_IMAGE_SOURCE_DOCKERFILE_BLOB` if the recipe changed. CI fails closed on
   recipe drift.
7. Independently re-verify with a **different verifier/harness** before the Web Lead
   advances the pin or closes OQ-BP-006.

A mutable-tag rebuild cannot move the accepted digest: the publication workflow has
no write path to the pin file, and both lanes refuse to run unless the committed
digest still resolves to the published content.

## 11. Unresolved / not run

- **NOT RUN:** independent verification by a different verifier/harness. That is the
  next step and is explicitly outside this author's role.
- **NOT RUN:** learner validation. Not claimed.
- **Not automated:** GHCR package visibility could not be flipped to public through
  the REST API from a workflow token (`404` on both candidate endpoints). This is
  **not blocking**: anonymous pull already works through the standard GHCR token
  flow, and repository CI uses `GITHUB_TOKEN` with `packages: read`. Recorded in
  `visibility.txt`.
- **Not addressed:** the scheduled `canonical-qemu-lane` failure on `main @ d3eabc10`
  is cited as motivation, not repaired by this PR — it is repaired by consuming the
  pinned digest on `main` after merge.
- `meta/PROJECT_STATUS.md` was deliberately not edited (Issue #150 freshness note).
  Its active-task wording may still be stale.

## 12. Ownership boundary

All changes in this PR were authored by this implementation session on branch
`implementation/durable-canonical-environment-pin-v0.1`, based on
`main @ d3eabc10e3dc2a330dda0c4ea4b7dc0520eca7ef`. Two files
(`publish-canonical-environment.yml`, `canonical-image-pull.sh`) existed as
uncommitted drafts left in the pre-existing worktree by this same role's earlier
session; they were reviewed, substantially reworked, and committed here. No other
actor's committed work is claimed. Nothing was merged or pushed to `main`.

## 13. Non-claims

- OQ-BP-006 remains **OPEN** and is **not** self-closed.
- No learner validation is claimed.
- No `v1.0`, `VERIFIED`, or stable `RELEASED` status is claimed.
- No claim that a mutable tag, local image ID, workflow SHA, or runner image version
  is a canonical identity.
