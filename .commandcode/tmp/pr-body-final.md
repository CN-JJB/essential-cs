# [Implementation] Durable canonical environment artifact + immutable pin v0.1 (#150)

Closes implementation gap **V-147-02** (from Issue #147 / PR #148) under Issue #150.

- **Base:** `main @ d3eabc10e3dc2a330dda0c4ea4b7dc0520eca7ef`
- **Substantive implementation head:** `d2ca8556f4fd086edcf82e0d2b1197571a619dda`
- **Final head:** `c149dfb610205a4a3de5e7254e7497f729f87c02`
- **Recommendation:** `DURABLE CANONICAL ENVIRONMENT PIN READY FOR INDEPENDENT VERIFICATION`

**OQ-BP-006 remains OPEN.** It is not self-closed here and may only be closed by the
Web Lead after genuinely independent verification by a **different verifier/harness**
than this implementation. No learner validation, `v1.0`, `VERIFIED`, or stable
`RELEASED` status is claimed.

---

## 1. What was delivered

A durable, retrievable, immutable canonical environment identity, consumed by both
canonical CI lanes by that same digest:

```text
ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
```

Before this PR both lanes ran `docker build -f .devcontainer/Dockerfile .` on every
run. The Ubuntu base was digest-pinned but general Noble packages resolved from live
apt at build time, so every run produced a different local image ID. That is not a
pin — and it is not merely theoretical: scheduled run `34572559147` on
`main @ d3eabc10` **failed on 2026-09-11 inside the environment build**, before any
course mechanism ran, because `apt-get install` could not fetch `liberror-perl`
(`Unable to connect to archive.ubuntu.com:80 … exit code: 100`). Release-relevant
execution no longer resolves apt at all.

## 2. Files changed

| File | Change |
| --- | --- |
| `.devcontainer/canonical-image.env` | **new** — the pin (`CANONICAL_IMAGE_DIGEST`) + recipe/base + informational provenance |
| `scripts/canonical-image-publish.sh` | **new** — build from committed recipe, push to repository-owned GHCR, capture registry digest; no write path to the pin |
| `scripts/canonical-image-pull.sh` | **new** — digest-only materialization, fail-closed |
| `.github/workflows/publish-canonical-environment.yml` | **new** — least-privilege publication, clean-context retrieval proof, guarded verify-pin |
| `.github/workflows/ci-fast.yml` | `canonical-fast` pulls the committed digest; no build |
| `.github/workflows/ci-qemu-lane.yml` | `canonical-qemu-lane` (qemu-smoke + m20 triage) pulls the **same** digest; no build |
| `.devcontainer/CANONICAL_ENVIRONMENT.md` | rewritten around durable identity + refresh governance |
| `.devcontainer/devcontainer.json` | materializes the pinned digest instead of rebuilding |
| `meta/verification/durable-canonical-environment-pin-implementation-v0.1.md` | **new** — implementation report |

`git diff --check d3eabc10…HEAD` → **PASS**. No `book/**`, learner-facing `labs/**`,
`project/**`, `meta/DECISIONS.md`, `meta/OPEN_QUESTIONS.md`, `meta/PROJECT_STATUS.md`,
release tag, or Issue #34 evidence was modified. `.devcontainer/Dockerfile` was
**not** modified.

## 3. Publication architecture and permission boundary

- Workflow `publish-canonical-environment`, run
  [34673360717](https://github.com/CN-JJB/essential-cs/actions/runs/34673360717),
  `push`, source revision `25804b02cdd89bc3e2ff386aaf60f7c0b41b9032`.
- Permissions: `contents: read`, `packages: write` — nothing else. Repository-owned
  `GITHUB_TOKEN` only. **No paid infrastructure, no new secrets, no new accounts.**
- Build: `docker buildx build --platform linux/amd64 --provenance=false --sbom=false`
  from `.devcontainer/Dockerfile`.
- Digest from buildx publication metadata (`containerimage.digest`), cross-checked by
  `docker buildx imagetools inspect` **and** by a pull on a separate fresh runner.
- Guard step asserts the publication run did not modify the pin file:
  `PUBLISH_DID_NOT_MODIFY_PIN=YES`.
- Guarded trigger: a `push` may publish **only** while the committed pin is the
  all-zero sentinel. Once a real digest is committed, a push can only verify. This
  was exercised — see §6.

**Source recipe:** `.devcontainer/Dockerfile` blob
`51198ea12c3c9ddfa18a2246bddef491ea729559`;
base `ubuntu:24.04@sha256:224a1869083a311ef3f13648a154ba79832fbef6364d31493642ca03082da254`;
platform `linux/amd64`.

## 4. Identity separation (the core requirement)

| Field | Value | Role |
| --- | --- | --- |
| **registry manifest digest** | `sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460` | **THE PIN** |
| config blob digest | `sha256:24a926a0dcc9b98b7298b8728d68417233f15f32a23350bf1273bb26089d7805` | build detail |
| Docker local image ID | `sha256:24a926a0…9d7805` | daemon-local, ephemeral — **NOT the pin** |
| mutable tags | `…canonical:candidate`, `…canonical:sha-25804b02…` | repointable — **NOT the pin** |
| git / workflow SHA | `25804b02…` (publication source) | source revision — **NOT the pin** |
| hosted runner image | `ubuntu-24.04` / `20260907.300.1` | moving substrate — **NOT the pin** |

Deliberate near-collision worth noting for the verifier: the local image ID equals
the **config** digest. That is precisely why the pin is the **manifest** digest
(`766ce07b…`) and not the config digest or the local image ID. Both lanes record the
local image ID in their retained evidence explicitly labelled
`local_image_id_role=NOT-PIN (daemon-local)`.

## 5. Clean retrieval proof

From a fresh runner whose pre-pull image list contains only GitHub's own runner
images:

```text
PULL_BY_DIGEST_REFERENCE=ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
Name:      ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07b…19e460
MediaType: application/vnd.docker.distribution.manifest.v2+json
Digest:    sha256:766ce07b…19e460
Status: Downloaded newer image for ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07b…19e460
RepoDigests: ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07b…19e460
CLEAN_PULL_BY_DIGEST=PASS
```

**Credential-free (anonymous) retrieval, verified outside CI:**

- Anonymous pull token → `GET /v2/cn-jjb/essential-cs/canonical/manifests/sha256:766ce07b…19e460`
  returns `HTTP/1.1 200 OK` with
  `docker-content-digest: sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460`.
- Re-hashing the returned manifest bytes yields
  `766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460` — content
  addressing confirmed end to end.
- Config and layer blobs return `307` (CDN redirect) anonymously.

CI additionally uses repository-owned `GITHUB_TOKEN` with `packages: read`.
No learner credentials required; no new secret introduced.

## 6. Exact-head Actions evidence at the final head `c149dfb6…`

| Lane | Run | Event | Result |
| --- | --- | --- | --- |
| `canonical-fast` | [34673997549](https://github.com/CN-JJB/essential-cs/actions/runs/34673997549) | `pull_request` | **success** |
| `canonical-qemu-lane` | [34673997278](https://github.com/CN-JJB/essential-cs/actions/runs/34673997278) | `workflow_dispatch` | **success** |
| `publish-canonical-environment` (verify-pin) | [34673576341](https://github.com/CN-JJB/essential-cs/actions/runs/34673576341) | `push` | success |

Both lanes at the final head recorded the **identical** consumption identity:

```text
lane=canonical-fast
canonical_image=ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
committed_pin_digest=sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
git_sha=c149dfb610205a4a3de5e7254e7497f729f87c02
DIGEST_CONSUMPTION_ASSERT=PASS   RECIPE_BLOB_MATCH=YES   REPO_DIGESTS_CONTAIN_PIN=YES
```

```text
lane=canonical-qemu-lane
canonical_image=ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
committed_pin_digest=sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
git_sha=c149dfb610205a4a3de5e7254e7497f729f87c02
DIGEST_CONSUMPTION_ASSERT=PASS
```

**Same digest in both lanes — yes**, and the same digest as the committed pin.

### `canonical-fast` outcomes

- 26/26 Python suites `SUITE_PASS`, including `labs/foundations/m10` (M10 normal
  required path) and `labs/foundations/m20`. 0 failures, no quarantine.
- M03 canonical evidence with required GDB trace: `SMOKE result=PASS`,
  `M03_CANONICAL_EVIDENCE_DONE`.
- Required Lab harnesses `01 / 03 / 04 / 05` + resets: `LAB_HARNESSES_DONE`.
- Shared preflights PASS; shell syntax gates `SYNTAX_ALL_OK`.
- Hygiene PASS (`HYGIENE_DONE`) — includes `git diff --check <base>...HEAD`.
- Environment capture inside the pulled digest: `CANONICAL_ENV_CAPTURE result=PASS`.

### `canonical-qemu-lane` outcomes

- Real learner-owned LAB-REQ-02 smoke executed:
  `REQ02_SMOKE_EVIDENCE: FAIL-CLOSED POSTCONDITION PASS`.
- `REQ02_CLEANUP_TRUTH_DONE` (xv6 pin restored, no residue, no strays).
- `QEMU_EVIDENCE_COMPLETE: FAIL-CLOSED GATE PASS` with all six required files
  non-empty.
- Retained `req02-smoke.log` = **41 476 bytes**, containing every required marker:

```text
LAB_REQ_02_OK                        (standalone, line 145)
QEMU_SMOKE_STATUS: PASS
QEMU_REAPED: TRUE
PID_MARKER_CLEAN: YES
=== LAB-REQ-02 Smoke Test PASS ===
```

- m20 diagnostic triage: `TRIO_RUN_1..5=PASS` (non-blocking, **not** cited as
  stable-green evidence).

### #149 contract preserved

The `qemu-smoke` command, the fail-closed postcondition greps, the cleanup-truth
job, and the evidence-completeness gate are byte-identical to the #149 repair. Only
the image-acquisition step changed (`docker build` → `docker pull` by digest). No
evidence gate was weakened.

### The push guard was exercised

Run `34673576341` was a `push` **after** a real digest was committed. It classified
as `verify-pin`, skipped `publish-candidate` entirely, and reported
`COMMITTED_PIN_RETRIEVABLE=PASS`. A push can no longer publish or move the accepted
pin.

## 7. Package / tool identity inside the pinned digest

`scripts/canonical-env-capture.sh` executed **inside the image pulled from the pinned
digest** → `CANONICAL_ENV_CAPTURE result=PASS`, all D-032 floors and both lane
tripwires satisfied:

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

## 8. Retained artifacts (IDs / sizes / digests / inventory)

Final-head lane artifacts:

| Run | Artifact | ID | Size (B) | Digest |
| --- | --- | --- | --- | --- |
| 34673997549 | `canonical-fast-evidence` | 10291940934 | 9645 | `sha256:021f6d01409997fe7886a33ab75e7f8fff170566b4261629c9c44994e3e8105b` |
| 34673997278 | `canonical-qemu-evidence` | 10291752700 | 9514 | `sha256:ffa9028994eac3e4dbdad15c2a07a08a385bc4f56f8d5a959aa63ec62e9a6034` |
| 34673997278 | `canonical-m20-triage` | 10291578408 | 1023 | `sha256:2c13c0e47d9c1014ae8f5d9fc378171c5446ef0235ae5a7175fb8260dcb5c610` |

Publication / retrieval / verify artifacts:

| Run | Artifact | ID | Size (B) | Digest |
| --- | --- | --- | --- | --- |
| 34673360717 | `canonical-publish-evidence` | 10291063296 | 2899 | `sha256:fd8c1ee7997e8cd535ad02b458df71e8b55aeec155932f230a76010b432e30ff` |
| 34673360717 | `canonical-retrieval-evidence` | 10291412766 | 2806 | `sha256:81dd67a5103544cb1775d6ade136ce4110f5c698b14f99e5e3277c85bfa3ec27` |
| 34673576341 | `canonical-pin-verification-evidence` | 10291108604 | 2813 | `sha256:8782c517e109ddbb07dea82827e878081f352cfcc81d26b14c818857d69488d3` |

File inventories (bytes): **fast** — `canonical-digest-consumption.txt` 549,
`canonical-env-snapshot.txt` 3466, `harness-req01.log` 4005, `harness-req03.log` 1138,
`harness-req04.log` 1835, `harness-req05.log` 1217, `m03-smoke.log` 1054,
`preflights.log` 11432, `python-matrix.log` 4843. **qemu** —
`canonical-digest-consumption.txt` 554, `qemu-env-snapshot.txt` 3466,
`qemu-lane-outer.log` 43342, `req02-preflight.log` 576, `req02-setup.log` 388,
`req02-smoke.log` 41476, `req02-source-route.log` 566. **publish** —
`build-metadata.json` 1532, `config-digest.txt` 72, `identity.txt` 1047,
`imagetools-inspect.txt` 268, `registry-digest.txt` 72, `substrate.txt` 484,
`visibility.txt` 498. **retrieval** — `canonical-env-snapshot.txt` 3466,
`pre-pull-image-list.txt` 334, `retrieval-context.txt` 203,
`retrieval-imagetools-inspect.txt` 268, `retrieval-local-image-id.txt` 72,
`retrieval-repodigests.txt` 111.

## 9. Reproducibility boundary — stated honestly

**Not claimed:** that rebuilding `.devcontainer/Dockerfile` from live Noble apt
repositories on a later date produces the same image. It does not, and on 2026-09-11
the recipe could not even be re-built on demand.

**Claimed:** the already-published immutable image is retrievable by digest for as
long as the package exists, and **that retrieval — not recipe replay — is the
stability guarantee**. Every environment a canonical lane executes is that published
digest.

## 10. Pin refresh / update procedure

1. Explicit Dockerfile/source change or intentional refresh decision — never an
   automatic rebuild.
2. Build a candidate (`workflow_dispatch`, `mode: publish-candidate`).
3. Run the required validation against the candidate.
4. Publish to repository-owned GHCR.
5. Capture the immutable registry digest.
6. Update the canonical digest **only through a reviewed PR**, together with
   `CANONICAL_IMAGE_SOURCE_DOCKERFILE_BLOB` if the recipe changed. CI fails closed on
   recipe drift (`RECIPE_BLOB_MATCH`).
7. Independently re-verify with a **different verifier/harness** before the Web Lead
   advances the pin or closes OQ-BP-006.

A mutable-tag rebuild cannot move the accepted digest: the publication workflow has
no write path to the pin file, and both lanes refuse to run unless the committed
digest still resolves to the published content.

## 11. Unresolved / NOT RUN

- **NOT RUN:** independent verification by a different verifier/harness — the
  required next step, outside this author's role.
- **NOT RUN:** learner validation. Not claimed.
- **Not automated:** GHCR package visibility could not be flipped to `public` through
  the REST API from a workflow token (`404` on both candidate endpoints). **Not
  blocking** — anonymous pull already works via the standard GHCR token flow, and CI
  uses `GITHUB_TOKEN` with `packages: read`. Recorded in `visibility.txt`.
- The scheduled `canonical-qemu-lane` failure on `main @ d3eabc10` is cited as
  motivation; it is resolved by `main` consuming the pinned digest after merge.
- `meta/PROJECT_STATUS.md` was deliberately not edited (Issue #150 freshness note);
  its active-task wording may still be stale.
- `meta/OPEN_QUESTIONS.md` was deliberately not edited.

---

# Execution Trace / Work Log

## Starting state

- Assigned base: `main @ d3eabc10e3dc2a330dda0c4ea4b7dc0520eca7ef`, verified both via
  `git ls-remote origin refs/heads/main` and the GitHub ref API.
- Branch: `implementation/durable-canonical-environment-pin-v0.1`, created from
  `origin/main` in the pre-existing worktree `G:/ai_project/research/cs-worktrees/issue-150`.
- Starting HEAD: `d3eabc10…`, worktree clean apart from **two untracked drafts left by
  this same role's earlier session** (`.github/workflows/publish-canonical-environment.yml`,
  `scripts/canonical-image-pull.sh`). No commits, no pushed ref, no PR.
- Issue #150 already carried a claim comment in the exact prescribed wording for this
  role; no competing claim, no open PR referencing #150, and no remote branch work
  existed.

## Actions performed

1. Read Issue #150 in full, its comments, all open PRs, the recommended branch, and
   the required context (D-032, OQ-BP-006, `.devcontainer/**`,
   `scripts/canonical-env-capture.sh`, both CI workflows, prior verification reports).
2. Posted the claim to Issue #150.
3. Designed and wrote the pin file, publication helper, digest-only pull helper, and
   the publication workflow; rewired both CI lanes to pull the committed digest.
4. Pushed `25804b0` → publication run `34673360717` published the image and proved
   clean pull-by-digest on a separate fresh runner.
5. Committed the real digest + rewritten docs → `d2ca855`; the push classified as
   `verify-pin` (run `34673576341`) and proved the committed pin retrievable.
6. Opened PR #152; ran `canonical-fast` `34673666673` and `canonical-qemu-lane`
   `34673676055` green at `d2ca855`.
7. Added the implementation report → `bb5552c`; re-ran both lanes green
   (`34673851886`, `34673855952`).
8. Clarified the implementation-head / final-head relationship in the report →
   `c149dfb`; re-ran both lanes green (`34673997549`, `34673997278`).

## Verification run (PASS / FAIL / BLOCKED / NOT RUN)

- **PASS** `git diff --check d3eabc10…HEAD`.
- **PASS** YAML parse of all three workflows; `bash -n` of both helper scripts.
- **PASS** publication run `34673360717`; `PUBLISH_DID_NOT_MODIFY_PIN=YES`.
- **PASS** clean pull-by-digest on a fresh runner; `CLEAN_PULL_BY_DIGEST=PASS`.
- **PASS** anonymous manifest fetch + manifest re-hash == pinned digest.
- **PASS** `canonical-env-capture.sh` inside the pulled digest
  (`CANONICAL_ENV_CAPTURE result=PASS`).
- **PASS** `verify-pin` run `34673576341` (`COMMITTED_PIN_RETRIEVABLE=PASS`,
  `RECIPE_BLOB_MATCH=YES`).
- **PASS** final-head `canonical-fast` `34673997549` and `canonical-qemu-lane`
  `34673997278`, both consuming the same digest; real QEMU smoke with retained
  `req02-smoke.log`.
- **NOT RUN** independent verification by a different verifier/harness.

## Problems encountered and resolution

1. **`gh workflow run` 404** when passing the workflow *name*
   (`canonical-qemu-lane.yml`) — the file is `ci-qemu-lane.yml`. Resolved by using
   the filename. No repository change needed.
2. **Local git ref writes silently dropped** in this environment when the target ref
   directory did not yet exist (branch appeared "unborn" after a successful commit;
   reflog recorded the commit). Diagnosed by inspecting `.git/logs/refs/...`; resolved
   by pre-creating the ref directory and re-pointing the ref to the reflog's new SHA
   before pushing. Local tooling artefact only — the pushed commits were correct and
   are what GitHub built.
3. **GHCR visibility API returned 404** for both candidate endpoints from a workflow
   token. Diagnosed as a permissions/API-surface limitation for installation tokens,
   not a publication failure. Disposition: recorded as non-blocking; anonymous pull
   was then proven directly against the registry, and CI uses `packages: read`.
4. **Head/evidence circularity** (a commit cannot cite its own run IDs). Resolved by
   making the report state the head relationship explicitly and recording the
   final-head run IDs in this PR body, per the Issue #150 PR contract.

## Ownership boundary

All committed changes were authored by this implementation session on
`implementation/durable-canonical-environment-pin-v0.1`. The two untracked draft files
present at start came from **this same role's earlier session**; they were reviewed,
substantially reworked, and are committed here. No other actor's committed work is
claimed. Nothing was pushed to `main`; nothing was merged.

## Residual risk / not-run work

- The pin is only as durable as the GHCR package's existence. If the package or the
  repository is deleted, the digest becomes unretrievable; the digest itself cannot
  be recreated from the recipe.
- If the repository's `GITHUB_TOKEN` default permissions are ever reduced below
  `packages: read`, the lanes' authenticated pull path would need revisiting;
  anonymous pull would still work while the package remains anonymously readable.
- Independent verification has **not** been performed and is required before
  OQ-BP-006 disposition.

---

## Recommendation

`DURABLE CANONICAL ENVIRONMENT PIN READY FOR INDEPENDENT VERIFICATION`
