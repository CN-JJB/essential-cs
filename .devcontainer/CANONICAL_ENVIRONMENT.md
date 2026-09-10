# Canonical Environment Identity (candidate v0.1 — Issue #145)

Governance: **D-032**. Status: **candidate definition, not the final realized pin**.
OQ-BP-006 remains OPEN until Web Lead acceptance after independent verification and a durable/retrievable built-environment identity is established.
No v1.0 / VERIFIED / RELEASED claim follows from this document.

## 1. Base image reference (immutable input)

- Reference: `ubuntu:24.04@sha256:224a1869083a311ef3f13648a154ba79832fbef6364d31493642ca03082da254`
- What the digest is: manifest-list digest for the `24.04` tag of `library/ubuntu`.
- Retrieved: 2026-09-10 via the Docker Registry HTTP API
  (`GET /v2/library/ubuntu/manifests/24.04`, `Accept: manifest.list.v2+json`,
  `docker-content-digest` response header).
- Cross-checked the same day: `docker pull ubuntu:24.04` resolved to the identical digest.
- Observed per-arch amd64 image manifest the same day:
  `sha256:a61567bd31828687156d735ea8eb01ba4e37636e225dd6a48ba94136a70d9d61`.
- The `FROM ...@sha256:` reference is immutable. Re-querying the moving `ubuntu:24.04` tag is a **refresh check**, not reconstruction of a previously built Essential CS image.
- Never float on `ubuntu-latest`, and never treat the moving GitHub-hosted runner image as the canonical pin.

## 2. Build inputs and reproducibility boundary

- Definition: `.devcontainer/Dockerfile` (+ `devcontainer.json`) at the implementation head.
- Build command: `docker build -f .devcontainer/Dockerfile -t <name>:<tag> .`
- Layer 1 intentionally implements D-032 **version floors** from Noble apt repositories: python3, sqlite3, build-essential, binutils, gdb, git, curl, ca-certificates, perl, bc, bash, procps, iproute2, file, strace.
- Layer 2 has lane-scoped exact package tripwires for `qemu-system-misc=1:8.2.2+ds-0ubuntu1.18` and `gcc-riscv64-unknown-elf=13.2.0-11ubuntu1+12`; `gcc-riscv64-linux-gnu` remains a captured fallback package identity.
- Deliberately absent: PostgreSQL server, browsers, observability/SaaS backends, Docker-in-Docker, arm64 cross-toolchains.
- `LANG=C.UTF-8 LC_ALL=C.UTF-8` is set so Python uses UTF-8 under the minimal base.

**Important boundary:** the base digest is fixed, but general apt packages allowed by D-032 floors are resolved at build time. Therefore this committed definition is reproducible as a **policy/configuration recipe**, but it does **not** guarantee a byte-identical built image across dates or hosts. A future Noble package update that remains above the floors may legitimately change the image ID. Exact package identities must be captured for each evidence run.

## 3. Observed candidate build identities (not durable pins)

### Implementer-local build

- Image ID: `sha256:9b862cb417234bb72e7c1869eb8d33e3cd8c98eda6c9628eb811ba13af907d32`
- Local tag: `essential-cs-canonical:v0.1-issue145`
- Platform: amd64/linux; approximately 1.53 GB.
- Not published; not independently retrievable by this ID after the local daemon is gone.

### First GitHub Actions build

- Run: `34439909872` (`canonical-fast`).
- Built image ID: `sha256:495067c9d967ae892fbaea29c04570b2ad6c8d4975c6a18b0786766ebaf7e2ae`.
- This differs from the implementer-local image ID, which is direct evidence that the current floor-based recipe is not a byte-identical built-image pin.
- The image itself was not published/exported as a container artifact. A workflow log recording an image ID is evidence about that ephemeral build, not a retrievable image pin.

No repository-owned durable container/package artifact exists yet. **OQ-BP-006 therefore remains OPEN.** The next independent verification may accept the functional candidate, but final Web Lead pin closure requires a durable/retrievable built-environment digest (or an equivalently immutable package snapshot strategy) plus accepted runtime evidence.

## 4. Resolved package identities observed in the first candidate builds

The implementer-local build recorded:

```text
bash                    5.2.21-2ubuntu4
bc                      1.07.1-3ubuntu4
binutils                2.42-4ubuntu2.10
build-essential         12.10ubuntu1
ca-certificates         20260601~24.04.1
curl                    8.5.0-2ubuntu10.13
gcc-riscv64-linux-gnu   4:13.2.0-7ubuntu1
gcc-riscv64-unknown-elf 13.2.0-11ubuntu1+12
gdb                     15.1-1ubuntu1~24.04.1
git                     1:2.43.0-1ubuntu7.3
make                    4.3-4.1build2
perl                    5.38.2-3.2ubuntu0.4
python3                 3.12.3-0ubuntu2.1
qemu-system-misc        1:8.2.2+ds-0ubuntu1.18
sqlite3                 3.45.1-1ubuntu2.7
strace                  6.8-0ubuntu2
```

The first Actions build independently observed the same headline floor versions and exact QEMU/unknown-elf package tripwires. `scripts/canonical-env-capture.sh` now fail-closes the x86-64 architecture, D-032 floors, and the two lane exact-package tripwires while recording a broader QEMU/RISC-V dependency table.

Observed tool surface: CPython 3.12.3, embedded SQLite 3.45.1, gcc 13.3.0, GDB 15.1, QEMU 8.2.2, riscv64-unknown-elf-gcc 13.2.0, riscv64-linux-gnu-gcc 13.3.0, git 2.43.0, curl 8.5.0 / OpenSSL 3.0.13, Ubuntu 24.04.4 LTS, x86_64.

## 5. CI identity discipline

- Standard GitHub-hosted `ubuntu-24.04` is a moving execution substrate. Its runner image version is recorded separately and is never the pin.
- On `pull_request`, `canonical-fast` explicitly checks out and asserts the PR **head SHA**, rather than accepting GitHub's synthetic merge ref as exact-head evidence.
- Evidence logs are retained as workflow artifacts; those logs document the observed build and runtime but are not the built container image itself.
- Scheduled/manual QEMU work similarly asserts its dispatched revision before producing evidence.

## 6. Refresh / final-pin runbook

- Re-check the upstream Ubuntu tag/base digest quarterly or on security need. Any base change requires an explicit Dockerfile re-pin and full re-verification.
- If a lane lock stops resolving, do not delete the exact version. Deliberately update the package identity and run a real LAB-REQ-02 QEMU smoke before acceptance.
- Floor-allowed package updates may change the built image. Capture those identities every run and treat any behavior change as evidence requiring disposition.
- Before OQ-BP-006 closes, establish and record a **durable/retrievable final built-environment digest or equivalent immutable package snapshot**, then independently run the required matrix against that realized identity.
- `main` may forward-test newer toolchains without silently moving the accepted stable pin.
