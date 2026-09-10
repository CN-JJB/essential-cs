# Stable Environment + CI Matrix Implementation Evidence v0.1

**Task:** Issue #145 — `[Implementation] Canonical stable environment + CI matrix v0.1`  
**Role:** Stable Environment / CI Executor; Web Lead bounded configuration/report corrections recorded below  
**Canonical base:** `main @ e53580fcce2c32d0785cf43f0d42e98ca8a78ea5`  
**Implementation branch:** `implementation/issue-145-stable-environment-ci-v0.1`  
**Governance:** D-032. **OQ-BP-006 remains OPEN.** No v1.0 / VERIFIED / stable RELEASED claim is made.

---

## 1. Delivered scope

The implementation adds only the seven Issue #145 surfaces:

| File | Purpose |
|---|---|
| `.devcontainer/Dockerfile` | Ubuntu 24.04 digest-pinned base input + required tools + QEMU/RISC-V lane package tripwires |
| `.devcontainer/devcontainer.json` | Minimal learner/dev-container entry |
| `.devcontainer/CANONICAL_ENVIRONMENT.md` | Candidate identity, reproducibility boundary, package evidence, refresh/final-pin runbook |
| `scripts/canonical-env-capture.sh` (100755) | x86-64 + D-032 floor gate + exact lane-package checks + version snapshot |
| `.github/workflows/ci-fast.yml` | PR/main fast matrix in the candidate environment; exact revision assertion; no test quarantine |
| `.github/workflows/ci-qemu-lane.yml` | Nightly/manual real-QEMU lane + temporary m20 diagnostic repeats |
| `meta/verification/stable-environment-ci-implementation-v0.1.md` | This evidence record |

No `book/**`, learner-facing `labs/**`, `project/**`, Decisions, Open Questions, Project Status, tags/releases, or Issue #34 learner evidence are changed.

## 2. Candidate environment identity — exact claim boundary

### Immutable base input

`ubuntu:24.04@sha256:224a1869083a311ef3f13648a154ba79832fbef6364d31493642ca03082da254`

The implementer retrieved that manifest-list digest on 2026-09-10 and cross-checked a live pull resolving to the same digest. The Dockerfile therefore does not float on `ubuntu:24.04` or `ubuntu-latest` at its `FROM` boundary.

### Build recipe and package resolution

The Dockerfile intentionally combines:

- D-032 compatibility floors for the general Noble tool surface;
- exact package tripwires for `qemu-system-misc=1:8.2.2+ds-0ubuntu1.18` and `gcc-riscv64-unknown-elf=13.2.0-11ubuntu1+12`;
- captured identities for the rest of the QEMU/RISC-V dependency surface.

General Layer-1 apt packages are resolved from the current Noble repositories at build time. **Therefore the committed recipe plus base digest does not guarantee byte-identical built images across dates/hosts.** This is deliberate floor policy, but it means Issue #145 has implemented a **functional candidate definition**, not yet the final durable built-image pin required to close OQ-BP-006.

### Observed built images

- Implementer-local image ID: `sha256:9b862cb417234bb72e7c1869eb8d33e3cd8c98eda6c9628eb811ba13af907d32`.
- First GitHub Actions build image ID: `sha256:495067c9d967ae892fbaea29c04570b2ad6c8d4975c6a18b0786766ebaf7e2ae`.

The differing IDs are evidence that the current floor-based recipe is not a byte-identical built-image pin. Neither image was published/exported as a durable container artifact. A workflow log containing an image ID is not a retrievable image artifact.

**Pin disposition:** candidate functional environment implemented; **durable/retrievable final built-environment identity still required before OQ-BP-006 closure.**

## 3. Observed tool / package identity

Implementer and first CI build observed the expected D-032 surface: Ubuntu 24.04.x x86-64, CPython 3.12.3, embedded SQLite + CLI 3.45.1, gcc 13.3.0, GDB 15.1, binutils 2.42, git 2.43.0, curl 8.5.0 / OpenSSL 3.0.13, QEMU 8.2.2, riscv64-unknown-elf-gcc 13.2.0, riscv64-linux-gnu-gcc 13.3.0, and strace 6.8.

Key resolved package identities included:

- `qemu-system-misc 1:8.2.2+ds-0ubuntu1.18`
- `gcc-riscv64-unknown-elf 13.2.0-11ubuntu1+12`
- `gcc-riscv64-linux-gnu 4:13.2.0-7ubuntu1`
- `gdb 15.1-1ubuntu1~24.04.1`
- `python3 3.12.3-0ubuntu2.1`
- `sqlite3 3.45.1-1ubuntu2.7`
- `curl 8.5.0-2ubuntu10.13`

After Lead review, `scripts/canonical-env-capture.sh` additionally:

- fail-closes unless architecture is `x86_64`;
- uses version-aware floor comparison rather than independent major/minor tests;
- explicitly checks the two lane exact-package tripwires;
- records a broader QEMU/RISC-V package table.

## 4. Implementer runtime evidence

The Executor ran the candidate definition on an ephemeral LF archive materialization at implementation commit `757aa2d…`. The evidence report was then added at handoff head `d7e1f2063a699ce19121eb3e01db05acf1f062a0`; the report itself did not alter executable course surfaces.

Observed outcomes reported by the implementer:

| Surface | Outcome |
|---|---|
| D-032 floors / package snapshot | PASS |
| Shared preflights | all REQUIRED PASS; strace live probe PASS; REQ-02 RUNNABLE |
| Full Python matrix | 26 suites + preflight discover PASS; M10 10/10; M20 36/36 |
| M03 | preflight/build/baseline/symbol/disassembly/GDB three-point/failure/reset PASS; `SMOKE result=PASS` |
| LAB-REQ-01 | PASS + reset |
| LAB-REQ-02 | **real QEMU smoke PASS** + exact xv6 pin/source route + cleanup truth |
| LAB-REQ-03 | PASS + reset |
| LAB-REQ-04 | PASS + reset |
| LAB-REQ-05 | PASS + reset |
| m20 dedicated trio | 5/5 repeated PASS in candidate container |
| syntax / diff | PASS |

The M03 GDB ASLR-disable warning inside a container was non-fatal; required trace markers were observed.

## 5. M10 / M20 truth

- M10 is **not quarantined**. It passed on candidate canonical non-WSL Linux; historical V-129-02 remains scoped to the WSL relay observation.
- m20 passed in the candidate container (matrix + five repeated trio runs). The earlier WSL failures remain evidence of nondeterministic/environment-correlated behavior, **not proof that a latent repository race is impossible**.
- The normal fast matrix keeps m20 release-relevant. The separate scheduled m20 job is temporary diagnostic accumulation only and cannot count as stable-green evidence by itself.
- Any future canonical-CI m20 failure is a first-class finding requiring bounded triage/repair disposition.

## 6. First GitHub Actions run — useful integration evidence, not exact-head proof

Run `34439909872` (`canonical-fast`) concluded `success`, and raw job logs independently show:

- hosted substrate `ubuntu-24.04`, runner image `20260831.293.1`;
- candidate image build succeeded from the pinned base digest;
- D-032 floor capture PASS;
- shared preflights PASS;
- 26-suite matrix PASS including M10 10/10 and M20 36/36;
- M03 GDB evidence + `SMOKE result=PASS`;
- REQ-01/03/04/05 harnesses PASS;
- hygiene step PASS.

However, Web Lead review found two important CI-method defects in that first run:

1. On `pull_request`, default `actions/checkout` checked out GitHub's synthetic merge ref `80a6873278bf442338331ec899216f0a6c56db4b` (`Merge d7e1f206… into e53580f…`), **not exact PR head `d7e1f206…`**. Therefore run `34439909872` is merge-ref integration evidence, not exact-head evidence.
2. `actions/upload-artifact` warned `No files were found` because `.ci-logs` is hidden and `include-hidden-files` was not enabled. GitHub reported zero artifacts for the run.

Those facts supersede the original PR-body wording that called run `34439909872` exact-head CI proof or implied a retained evidence bundle.

## 7. Web Lead bounded Direct Fixes

The Web Lead kept all fixes inside the allowed environment/CI/report scope; no learner-facing source was touched.

- `b85fcaeec1576c35f2a6e37b5d2e3af695b0e40d` — `ci-fast.yml`: explicitly checkout PR head SHA, assert `HEAD == expected`, check the PR diff rather than only working-tree dirt, use safe QEMU process matching, and upload hidden `.ci-logs`.
- `926bd938a5104824f5c9f8e80eb0ddcc41f5d973` — `ci-qemu-lane.yml`: assert dispatched revision, fix QEMU cleanup self-match, retain hidden evidence logs, and keep candidate/OQ wording bounded.
- `9c2b052bd8c825a725a0012406c8ddfa72e09292` — environment capture: correct version-floor semantics, require x86-64, check lane package identities, broaden package capture.
- `48f9d4946dc1c87c77f3d7e61a13204f14a384bc` — identity document: distinguish immutable base input from the still-unpublished/non-byte-identical built image.
- This report correction records the same evidence boundary.

A new `canonical-fast` run on the resulting final PR head is required before Lead merge. It must show the asserted exact revision and a non-empty `canonical-fast-evidence` artifact.

## 8. QEMU workflow evidence boundary

`canonical-qemu-lane` is intentionally scheduled/manual, so the first PR-triggered `canonical-fast` run did not execute it. The implementer's real-QEMU PASS is therefore **Executor runtime evidence**, not Actions QEMU evidence.

The corrected scheduled/manual workflow now uses the bracket-pattern process check and retains its hidden evidence bundle. A later independent verification must execute real QEMU on the merged candidate environment/definition and inspect the resulting cleanup evidence.

## 9. What remains before OQ-BP-006 can close

Even if the corrected exact-head fast CI run is green, #145 should only advance the environment to independent verification. OQ-BP-006 remains OPEN until Web Lead has evidence for both:

1. **functional verification:** independent build/run of floors, full matrix, M03 GDB, all Required Labs including real QEMU, M10, m20 behavior, cleanup; and
2. **durable pin realization:** a retrievable built-environment digest or an equivalently immutable package snapshot strategy, because the current general apt-floor recipe may produce different image IDs over time.

No workflow log or local Docker image alone satisfies item 2.

## 10. Ownership / non-claims

Executor-authored implementation remains attributed to the Executor. Lead-authored fixes are the bounded commits listed in §7. Host Docker/proxy setup and local image tags are runtime scaffolding, not repository deliverables.

This PR does **not**:

- close OQ-BP-006;
- claim a final durable stable-environment pin;
- claim learner validation;
- claim v1.0 / VERIFIED / stable RELEASED;
- modify learner-facing lessons/labs/tests/preflights to force green.

## 11. Final recommendation

**`STABLE ENVIRONMENT CANDIDATE READY FOR INDEPENDENT VERIFICATION`**, conditional on the corrected `canonical-fast` workflow producing a green **exact-PR-head** run with retained evidence artifact at the final PR head.

This recommendation means the candidate definition and CI implementation are suitable for the next independent verification stage. It does not mean OQ-BP-006 is closed or that the final durable built-image pin already exists.
