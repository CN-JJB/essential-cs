# Durable Canonical Environment Pin — Technical Re-Verification v0.2

**Task:** Issue #153 — `[Verification] Durable canonical environment pin re-verification v0.2`
**Role:** Durable Environment Pin Technical Verifier (verification-only)
**Verification base (`VERIFICATION_BASE`):** `cd7396cad6ca746c55217968aafc59a8d3dd7369`
**Verification branch:** `verification/issue-153-durable-canonical-environment-pin-reverification-v0.2`
**Date (UTC):** 2026-09-12
**Status:** `READY FOR LEAD DURABLE PIN TECHNICAL RE-VERIFICATION REVIEW` (report only)

## 1. Same-lineage disclosure (read first)

This is a **`same-lineage technical re-verification`**, explicitly **not** an
independent verification.

- Issue #153 v0.2 permits the existing local implementation harness to execute this
  task directly; the earlier `INDEPENDENCE NOT SATISFIED` disposition belongs to the
  superseded v0.1 contract and is not a blocker here.
- The harness that produced this report is the same lineage that previously executed
  Issues #145 / #149 / #150. Nothing in this report may be presented as
  role-independent evidence.
- Final role independence is preserved at **Issue #158**, which must re-check the
  canonical environment independently before v1.0.
- This report may support Web Lead **OQ-BP-006** disposition after exact-head review.
  It does **not** itself close OQ-BP-006, and it does **not** satisfy final stable
  multi-role independence.

## 2. Claim and base lock

- Issue #153 body (v0.2) and both Issue comments were read; Issue #141 latest state
  was read.
- At claim time there was **no competing #153 claim comment** and **no open PR
  referencing #153** (only the two pre-existing Lead comments existed).
- `git fetch origin` was run; `origin/main` / `refs/heads/main` both resolved to
  `cd7396cad6ca746c55217968aafc59a8d3dd7369`, which was locked as
  `VERIFICATION_BASE`.
- Claim comment posted:
  `https://github.com/CN-JJB/essential-cs/issues/153#issuecomment-5644557300`
  ```
  CLAIMED BY DURABLE PIN VERIFIER
  Role: Durable Environment Pin Technical Verifier
  Harness lineage: SAME-LINEAGE ALLOWED BY ISSUE #153 v0.2
  Verification base: cd7396cad6ca746c55217968aafc59a8d3dd7369
  Status: TECHNICAL RE-VERIFICATION STARTED
  ```
- No historical hard-coded base was used. All verifier-owned runs and this report are
  scoped to `cd7396cad6ca746c55217968aafc59a8d3dd7369`.

Accepted immutable object under verification (unchanged):

```text
ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
```

## 3. A — Identity / provenance

| # | Check | Observed | Verdict |
|---|---|---|---|
| A1 | Committed pin in `.devcontainer/canonical-image.env` | `CANONICAL_IMAGE_DIGEST=sha256:766ce07b…19e460` | PASS |
| A2 | Registry-side digest (anonymous `docker buildx imagetools inspect`) | `Digest: sha256:766ce07b…19e460` | PASS |
| A3 | Media type / shape | `application/vnd.docker.distribution.manifest.v2+json`, single-arch (`schemaVersion 2`, no `manifests[]`) | PASS |
| A4 | OS / architecture | `architecture=amd64`, `os=linux` (config blob and `docker image inspect` agree) | PASS |
| A5 | Recipe provenance | `git hash-object .devcontainer/Dockerfile` = `51198ea12c3c9ddfa18a2246bddef491ea729559` = committed `CANONICAL_IMAGE_SOURCE_DOCKERFILE_BLOB` | PASS |
| A6 | Base input | Dockerfile `FROM ubuntu:24.04@sha256:224a1869083a311ef3f13648a154ba79832fbef6364d31493642ca03082da254` | PASS |
| A7 | Manifest ↔ config separation | manifest digest `766ce07b…`; config digest `sha256:24a926a0dcc9b98b7298b8728d68417233f15f32a23350bf1273bb26089d7805` (size 2723) | PASS |
| A8 | Layers | `ef852a65…` 30 628 175 B; `facb0d65…` 145 901 261 B; `5affce2c…` 214 049 979 B; `818d662c…` 94 B | INFO |
| A9 | Mutable candidate tag cannot move the accepted pin | `:candidate` currently resolves to the pin digest, but is only a repointable label; no lane and no script resolves the canonical environment by tag | PASS |
| A10 | Git SHA / runner version are not identity | recorded as audit fields only, never used to resolve the image | PASS |

Identity separation is intact: the **only** canonical identity is the registry
manifest digest committed in `.devcontainer/canonical-image.env`. The local image ID,
mutable tags, git SHA and the hosted runner image version are all explicitly not the
pin.

Notable observation: the committed pin file's blob is `97ca660e9da2ab3668ffd599dedd49bd07d4db20`
(at this base). It is a plain identity/provenance file and is never written by any
workflow (see §8).

## 4. B — Fresh retrieval

Performed on a **fresh, verifier-owned Docker context** (Docker Desktop daemon,
x86_64 host), with the pre-pull image list confirmed to contain **no**
`essential-cs/canonical` image.

| # | Observation | Result |
|---|---|---|
| B1 | Pre-pull canonical image present? | NO (fresh context) |
| B2 | Anonymous registry inspection (`imagetools inspect`, no credentials) | PASS — digest matches the pin |
| B3 | Anonymous pull by exact digest (`docker pull --platform linux/amd64 <pin>`, **no `docker login`**) | PASS — `Status: Downloaded newer image for …@sha256:766ce07b…19e460` |
| B4 | RepoDigests contain the pinned reference | PASS — `ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07b…19e460` |
| B5 | OS / architecture of pulled image | `linux/amd64`, `Size=390 583 393` B |
| B6 | Local image ID role | **NOT-PIN** (daemon-local) |

Auth/visibility behavior (truthful): the canonical package is retrievable
**credential-free** in this context. `docker buildx imagetools inspect` and
`docker pull` both succeeded with no `docker login`. CI additionally uses the
repository-owned `GITHUB_TOKEN` with `packages: read`; both paths resolve the same
content-addressed digest. No learner credentials and no new secret are involved.

Engine-dependence of the "local image ID" (a direct demonstration that it is not a
canonical identity):

| Context | Storage engine | Local image `Id` |
|---|---|---|
| This verifier's Docker Desktop | containerd store (`overlayfs`) | `sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460` (**equals the manifest digest**) |
| GitHub-hosted `canonical-fast` / `canonical-qemu-lane` | classic graphdriver | `sha256:24a926a0dcc9b98b7298b8728d68417233f15f32a23350bf1273bb26089d7805` (**equals the config digest**) |

Two engines, two different local IDs, one identical pin. The local image ID must never
be treated as identity.

## 5. C — Environment capture

`scripts/canonical-env-capture.sh` was run inside the container started from the
exact pulled digest (mounted LF tree materialized from `VERIFICATION_BASE` via
`git -c core.autocrlf=false archive`).

Local verifier run:

```text
CANONICAL_ENV_CAPTURE version=2
os=Ubuntu 24.04.4 LTS
arch=x86_64
FLOOR PASS canonical-arch=x86_64
CPython 3.12.3            FLOOR PASS python>=3.12
sqlite engine 3.45.1      FLOOR PASS sqlite-engine>=3.45
sqlite3 CLI 3.45.1        FLOOR PASS sqlite3-cli>=3.45
gcc 13.3.0 (C11 OK)       FLOOR PASS gcc>=13 + gcc-c11-surface
curl 8.5.0                FLOOR PASS curl>=8.5
gdb 15.1                  FLOOR PASS gdb>=15.0 REQUIRED-present
qemu-system-misc 1:8.2.2+ds-0ubuntu1.18     FLOOR PASS exact package identity
gcc-riscv64-unknown-elf 13.2.0-11ubuntu1+12 FLOOR PASS exact package identity
CANONICAL_ENV_CAPTURE result=PASS
```

Resolved package identities observed inside the digest (identical to the CI lanes):
`bash 5.2.21-2ubuntu4`, `bc 1.07.1-3ubuntu4`, `binutils 2.42-4ubuntu2.10`,
`binutils-riscv64-linux-gnu 2.42-4ubuntu2.10`,
`binutils-riscv64-unknown-elf 2.42-1ubuntu1+6`, `build-essential 12.10ubuntu1`,
`ca-certificates 20260601~24.04.1`, `curl 8.5.0-2ubuntu10.13`,
`gcc-riscv64-linux-gnu 4:13.2.0-7ubuntu1`,
`gcc-riscv64-unknown-elf 13.2.0-11ubuntu1+12`, `gdb 15.1-1ubuntu1~24.04.1`,
`git 1:2.43.0-1ubuntu7.3`, `make 4.3-4.1build2`, `perl 5.38.2-3.2ubuntu0.4`,
`python3 3.12.3-0ubuntu2.1`, `qemu-system-common/-data/-misc 1:8.2.2+ds-0ubuntu1.18`,
`sqlite3 3.45.1-1ubuntu2.7`, `strace 6.8-0ubuntu2`.

The CI-run snapshot (`canonical-env-snapshot.txt` / `qemu-env-snapshot.txt`, both
3466 B) is byte-for-byte identical to the local capture **except the kernel line**:

| Substrate | `kernel=` |
|---|---|
| GitHub-hosted runner (CI lanes) | `6.17.0-1022-azure` |
| Local Docker Desktop (this verifier) | `6.18.33.2-microsoft-standard-WSL2` |

Substrate honesty: the local verifier runs use the Docker Desktop / WSL2 kernel, which
is **not** the canonical execution substrate. The canonical substrate is the
GitHub-hosted `ubuntu-24.04` runner used by the CI lanes. Local results are
corroborative only and are not presented as canonical-substrate evidence.

## 6. D — Exact-base `canonical-fast`

Verifier-dispatched (`workflow_dispatch`) against the locked base.

| Field | Value |
|---|---|
| Workflow | `canonical-fast` |
| Run | [34681730339](https://github.com/CN-JJB/essential-cs/actions/runs/34681730339) |
| Event / head | `workflow_dispatch` / `cd7396cad6ca746c55217968aafc59a8d3dd7369` |
| Conclusion | **success** (job `canonical-matrix`, 07:49:47→07:50:45Z) |
| Artifact | `canonical-fast-evidence` id `10293264011` |

Exact-revision / digest assertions read from the run log:

```text
EXPECTED_REVISION=cd7396cad6ca746c55217968aafc59a8d3dd7369
ACTUAL_REVISION=cd7396cad6ca746c55217968aafc59a8d3dd7369
RECIPE_BLOB_MATCH=YES
REPO_DIGESTS_CONTAIN_PIN=YES
CONSUMED_CANONICAL_IMAGE=ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07b…19e460
DIGEST_CONSUMPTION_ASSERT=PASS
CONSUMED_LOCAL_IMAGE_ID=sha256:24a926a0dcc9b98b7298b8728d68417233f15f32a23350bf1273bb26089d7805 ARCH=amd64 OS=linux
runner_image_version=20260907.300.1
runner_arch=x86_64
```

Step-level timing (from the run log) shows genuine execution, not a vacuous green:
digest pull `07:49:50.317→07:50:06.607`; floor gate/capture `0.5 s`; preflights
`1.1 s`; shell syntax gates `0.2 s`; **full Python matrix `07:50:08.625→07:50:37.583`
(≈ 29 s)**; M03 `0.7 s`; harnesses `2.9 s`; hygiene; upload.

Surface verdicts:

| Surface | Verdict |
|---|---|
| Canonical floor gate + version snapshot | PASS (`result=PASS`) |
| Shared preflights (network/data-concurrency/distributed/security synthesis/M05–M09) | PASS (all REQUIRED) |
| Shell syntax gates | PASS (`SYNTAX_ALL_OK`) |
| Full Python matrix — 26 suites, no quarantine | **26/26 `SUITE_PASS`** (incl. `labs/foundations/m10` **10/10** and `labs/foundations/m20` **36/36**) |
| M03 canonical evidence incl. real GDB (REQUIRED) | PASS — `SMOKE baseline=PASS value=37`, `SMOKE symbol=PASS helper`, `SMOKE disassembly=PASS helper`, `SMOKE gdb=PASS`, `SMOKE result=PASS`; `M03_CANONICAL_EVIDENCE_DONE` |
| Required Lab harnesses 01/03/04/05 + resets | PASS — `LAB_HARNESSES_DONE` |
| Hygiene (`git diff --check`, no stray QEMU, no PID marker) | PASS — `HYGIENE_DONE` |
| Retained evidence bundle uploaded | PASS |

Local corroboration (non-canonical substrate, same digest): the same 26-suite surface
was re-run inside the pulled digest from the `VERIFICATION_BASE` LF tree and returned
**26/26 `SUITE_PASS` with identical per-suite test counts** (`LOCAL_MATRIX_DONE fail=0`).
Per-suite counts (both CI and local agree): m00-m01 8, m02 9, m05 9, m06 7, m07 4,
m08 12, m09 16, **m10 10**, m11 4, m12 6, m13 4, m14 5, m15 4, m16 5, m17 15, m18 14,
m19 20, **m20 36**, m21 15, m22 20, m23 23, m24 23, lab_req_01 6, lab_req_03 8,
lab_req_04 6, lab_req_05 7.

**M10 note:** M10 is not pre-quarantined — it runs as a normal member of the required
matrix (`SUITE_PASS labs/foundations/m10`, 10 tests, no skip/relay language).

## 7. E — Exact-base `canonical-qemu-lane`

Verifier-dispatched (`workflow_dispatch`) against the same locked base.

| Field | Value |
|---|---|
| Workflow | `canonical-qemu-lane` |
| Run | [34681732423](https://github.com/CN-JJB/essential-cs/actions/runs/34681732423) |
| Event / head | `workflow_dispatch` / `cd7396cad6ca746c55217968aafc59a8d3dd7369` |
| Conclusion | **success** — jobs `qemu-smoke` (07:49:50→07:50:18Z) and `m20-timing-triage` (07:49:49→07:50:35Z) |
| Artifacts | `canonical-qemu-evidence` id `10294255624`; `canonical-m20-triage` id `10294435275` |

Exact-revision / digest assertions and fail-closed postconditions read from the run log:

```text
EXPECTED_REVISION=cd7396cad6ca746c55217968aafc59a8d3dd7369
ACTUAL_REVISION=cd7396cad6ca746c55217968aafc59a8d3dd7369
RECIPE_BLOB_MATCH=YES
REPO_DIGESTS_CONTAIN_PIN=YES
DIGEST_CONSUMPTION_ASSERT=PASS
CONSUMED_LOCAL_IMAGE_ID=sha256:24a926a0…9d7805 ARCH=amd64 OS=linux
REQ02_SMOKE_EVIDENCE: FAIL-CLOSED POSTCONDITION PASS
REQ02_CLEANUP_TRUTH_DONE
EVIDENCE_OK: qemu-env-snapshot.txt (3466 bytes)
EVIDENCE_OK: req02-preflight.log (576 bytes)
EVIDENCE_OK: req02-setup.log (388 bytes)
EVIDENCE_OK: req02-source-route.log (566 bytes)
EVIDENCE_OK: req02-smoke.log (41476 bytes)
EVIDENCE_OK: qemu-lane-outer.log (43342 bytes)
QEMU_EVIDENCE_COMPLETE: FAIL-CLOSED GATE PASS
```

Required content of the **downloaded and inspected** `req02-smoke.log`:

| Required item | Observation |
|---|---|
| Learner-owned `./smoke.sh` really executes | PASS — real xv6 tree build with `riscv64-unknown-elf-gcc`, `mkfs fs.img … user/_sleep …`, real kernel link |
| Exact xv6 pin | PASS — `req02-setup.log`: `[+] Pinned xv6 worktree: 35b088427ef37611c38afdeed5a52a278cae38f9` |
| Source route | PASS — `req02-source-route.log`: `SYS_pause == 13`, dispatcher `[SYS_pause] -> sys_pause`, `sys_pause(void)`, `int pause(int)`, `ecall`, `uservec entry present` |
| Non-empty `req02-smoke.log` | PASS — 41 476 bytes |
| Standalone `LAB_REQ_02_OK` | PASS — line 145, produced by `$ echo LAB_REQ_02_OK` inside the guest shell |
| `QEMU_SMOKE_STATUS: PASS` | PASS |
| `QEMU_REAPED: TRUE` | PASS |
| `PID_MARKER_CLEAN: YES` | PASS |
| Final LAB-REQ-02 PASS banner | PASS — `=== LAB-REQ-02 Smoke Test PASS ===` |
| Fail-closed postconditions | PASS (in-step postcondition + separate completeness gate) |
| Reset to exact clean xv6 pin | PASS — cleanup-truth step asserts `worktree` HEAD == pin and empty status |
| No stray QEMU / PID marker | PASS — cleanup truth + `HYGIENE`/bracket-trick `pgrep` |
| Artifact actually downloaded and inspected | PASS (inventory in §9) |

Direct evidence that the QEMU run is real and not a fixture echo:

```text
[+] Step 3: Marker predicate self-check (echo-only must not PASS)...
MARKER_SELF_CHECK: PASS
...
qemu-system-riscv64 -machine virt -bios none -kernel kernel/kernel -m 128M -smp 3 -nographic …
xv6 kernel is booting
hart 1 starting
hart 2 starting
init: starting sh
$ sleep
Usage: sleep ticks
$ sleep 10
$ echo LAB_REQ_02_OK
LAB_REQ_02_OK
$
QEMU_SMOKE_STATUS: PASS
USAGE_OUTPUT_OBSERVED: YES
SLEEP10_RETURNED: YES
EXECUTION_MARKER_OBSERVED: YES
QEMU_REAPED: TRUE
PID_MARKER_CLEAN: YES
=== LAB-REQ-02 Smoke Test PASS ===
```

### M20 five-run characterization (diagnostic only)

`m20-timing-triage` ran 5 repeats of `TestThreeServicePipelineIntegration`:
`TRIO_RUN_1..5=PASS`, `TRIAGE_REPEATS_DONE`. Each run log is a real unittest summary
(`Ran 5 tests in ~5 s / OK`). This is characterized as **diagnostic only**; it is not
cited as stable-green Gate evidence and is not a substitute for the normal matrix
(which independently reported `m20` 36/36).

## 8. F — Permissions / governance

| # | Claim | Observed | Verdict |
|---|---|---|---|
| F1 | classify: contents read only | `permissions: contents: read` at workflow level; job inherits it | PASS |
| F2 | publication: packages write only where required | only `publish-candidate` adds `packages: write`; default remains `contents: read` | PASS |
| F3 | retrieve/verify: packages read | `retrieve-by-digest` and `verify-pin` = `contents: read` + `packages: read` | PASS |
| F4 | canonical lanes read-only | `ci-fast.yml`, `ci-qemu-lane.yml`, `ci-mini-cloud.yml` = `contents: read` + `packages: read` | PASS |
| F5 | no workflow can write the committed pin | every reference to `.devcontainer/canonical-image.env` in `.github/**` is a read (`sed -n 's/^CANONICAL_IMAGE_DIGEST=//p'`); no redirect/`sed -i`/`tee` write exists | PASS |
| F6 | publication guard | publish script asserts `PUBLISH_DID_NOT_MODIFY_PIN=YES`; pin update has no automated write path | PASS |
| F7 | mutable candidate publication cannot silently advance the pin | lanes consume the compiled-in digest only; `DIGEST_CONSUMPTION_ASSERT=PASS` + `REPO_DIGESTS_CONTAIN_PIN=YES` fail closed otherwise; `:candidate`/`:sha-*` are never used to resolve the environment | PASS |
| F8 | refresh requires reviewed digest update + later verification | documented in `.devcontainer/CANONICAL_ENVIRONMENT.md` §7 (steps 6–7); a push observed a real digest ⇒ classified `verify-pin`, never `publish` | PASS |

No `contents: write` appears anywhere in `.github/workflows/**`. No new secret or
elevated scope was introduced by this task.

## 9. G — Artifact truth

All three artifacts were **actually downloaded** and inspected. GitHub-reported
artifact digest equals the SHA-256 of the locally downloaded ZIP in every case.

| Run | Artifact | ID | Size (B) | GitHub digest | Local ZIP SHA-256 | Match |
|---|---|---|---|---|---|---|
| 34681730339 | `canonical-fast-evidence` | 10293264011 | 9656 | `sha256:1b9353ca1062c6dadffe0071f62853b130fbf5e9a12dd6e1bb35934c2b8be6d0` | `1b9353ca…b8be6d0` | YES |
| 34681732423 | `canonical-qemu-evidence` | 10294255624 | 9513 | `sha256:6c4bc605b80a42d85b72f7897b24deaf8d277e9bb9d9d9beb21573c0456c2fb9` | `6c4bc605…456c2fb9` | YES |
| 34681732423 | `canonical-m20-triage` | 10294435275 | 1023 | `sha256:a62de0d65d06bbf92d300bc157d7adac13f2e2eb51ad67f1f841840054609d89` | `a62de0d6…4609d89` | YES |

Complete expanded inventories (uncompressed bytes):

- `canonical-fast-evidence` (9 files): `canonical-digest-consumption.txt` 549,
  `canonical-env-snapshot.txt` 3466, `harness-req01.log` 4005, `harness-req03.log` 1138,
  `harness-req04.log` 1835, `harness-req05.log` 1217, `m03-smoke.log` 1054,
  `preflights.log` 11432, `python-matrix.log` 4843.
- `canonical-qemu-evidence` (7 files): `canonical-digest-consumption.txt` 554,
  `qemu-env-snapshot.txt` 3466, `qemu-lane-outer.log` 43342, `req02-preflight.log` 576,
  `req02-setup.log` 388, `req02-smoke.log` 41476, `req02-source-route.log` 566.
- `canonical-m20-triage` (6 files): `m20-trio-run1.log`…`m20-trio-run5.log` 103 each,
  `m20-trio-summary.txt` 100.

Both lanes' `canonical-digest-consumption.txt` record the identical consumption
identity and `git_sha=cd7396cad6ca746c55217968aafc59a8d3dd7369`.

## 10. No-repair / object-unchanged statement

- No repair was attempted. `HEAD` remained `cd7396cad6ca746c55217968aafc59a8d3dd7369`
  throughout, and `git diff --name-only <base> HEAD` is empty before the report commit.
- Nothing under `.devcontainer/**`, `.github/workflows/**`, `scripts/**`, `book/**`,
  `labs/**`, `project/**`, `meta/DECISIONS.md`, `meta/OPEN_QUESTIONS.md`,
  `meta/PROJECT_STATUS.md`, tags/releases or Issue #34 evidence was modified.
- No CI/test/preflight/workflow weakening, no threshold change, no fixture edit.
- No defect requiring repair was found in this re-verification.

## 11. Findings

**None blocking.** No repair route is required from this re-verification.

Non-blocking observations recorded for the Lead:

- **O-153-01 (informational).** Local image ID is engine-dependent: containerd store
  reports the manifest digest, classic store reports the config digest. This is
  expected and reinforces the NOT-PIN rule; it is not a defect.
- **O-153-02 (informational).** `:candidate` currently points at the accepted pin
  digest. It remains a mutable label that no lane consumes; a future
  `publish-candidate` run may repoint it without moving the pin.
- **O-153-03 (carry-forward, unchanged).** Recipe replay from live Noble apt is not
  byte-reproducible; the durable guarantee is retrieval of the published digest, as
  documented in `.devcontainer/CANONICAL_ENVIRONMENT.md` §4.

## 12. Residual risk / NOT RUN

- **Same-lineage:** this report cannot substitute for Issue #158's independent
  environment re-check. NOT RUN here by design.
- **Canonical substrate for local corroboration:** local runs used Docker Desktop /
  WSL2 (`kernel 6.18.33.2-microsoft-standard-WSL2`), not bare-metal Linux; CI lanes
  used the canonical GitHub-hosted substrate (`kernel 6.17.0-1022-azure`).
- **learner validation** (Issue #34): NOT RUN; not claimed.
- **#157 external curriculum/coverage audit, #158 final multi-role verification,
  #161 release gate:** NOT RUN (out of scope).
- **arm64**, live browser/OTel/psql/argon2, strace-beyond-probe: NOT RUN (optional by
  design/scope, unchanged).
- Latent m20 load-sensitive race cannot be proven absent from bounded repeats; the
  diagnostic lane keeps accumulating statistics and the normal matrix reported
  36/36 here.

## 13. Final recommendation — exactly one

**`DURABLE PIN TECHNICAL RE-VERIFICATION PASS — READY FOR WEB LEAD OQ-BP-006 DISPOSITION`**

Rationale: at the locked base `cd7396cad6ca746c55217968aafc59a8d3dd7369`, the durable
pin identity is internally consistent and retrievable by digest (anonymous and
token-based); both canonical lanes executed at that exact revision consuming the
identical immutable digest `sha256:766ce07b…19e460`; the full 26-suite surface
(including M10 10/10 and m20 36/36), M03 with real GDB, the four Required Lab
harnesses, preflights, syntax gates and hygiene all passed; the LAB-REQ-02 lane
executed the real learner-owned `./smoke.sh` against the exact xv6 pin with all
fail-closed markers, cleanup truth, and a downloaded/inspected artifact; M20 was
characterized 5/5 as diagnostic only; least-privilege governance holds and no
workflow can write or silently move the committed pin; and no repair was needed.

## 14. Explicit non-claims

- This is `same-lineage technical re-verification`, **not** independent verification.
- **OQ-BP-006 remains OPEN** and is not self-closed.
- No `VERIFIED`, `RELEASED`, v1.0, learner-validation, or lifecycle status is claimed.
- No claim that a mutable tag, local image ID, git SHA, or hosted runner image version
  is a canonical identity.
- No historical PASS is relabeled as a current-run result; every PASS above is tied to
  the recorded runs/artifacts at `cd7396cad6ca746c55217968aafc59a8d3dd7369`.
