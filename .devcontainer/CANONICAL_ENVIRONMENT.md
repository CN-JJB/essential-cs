# Canonical Environment Identity (candidate v0.1 — Issue #145)

Governance: **D-032**. Status: **candidate, not the final pin**.
OQ-BP-006 remains OPEN until Web Lead acceptance of the realized pin.
No v1.0 / VERIFIED / RELEASED claim follows from this document.

## 1. Base image reference (immutable)

- Reference: `ubuntu:24.04@sha256:224a1869083a311ef3f13648a154ba79832fbef6364d31493642ca03082da254`
- What the digest is: manifest-list digest for the `24.04` tag of `library/ubuntu`.
- Retrieved: 2026-09-10 via the Docker Registry HTTP API
  (`GET /v2/library/ubuntu/manifests/24.04`, `Accept: manifest.list.v2+json`,
  `docker-content-digest` response header).
- Cross-checked the same day: `docker pull ubuntu:24.04` resolved to the identical digest.
- Observed per-arch amd64 image manifest the same day:
  `sha256:a61567bd31828687156d735ea8eb01ba4e37636e225dd6a48ba94136a70d9d61`
  (Docker Hub tag metadata, `tag_last_pushed 2026-09-09T17:54:13Z`).
- Reconstruction: re-query the registry the same way and compare byte-for-byte.
  Any difference means the upstream tag moved and this file + the Dockerfile must be
  consciously re-pinned (refresh cadence below). Never float on `ubuntu-latest`, and never
  treat the moving GitHub-hosted runner image as this pin.

## 2. Build inputs

- Definition: `.devcontainer/Dockerfile` (+ `devcontainer.json`) at the implementation head.
- Build command (reproducible): `docker build -f .devcontainer/Dockerfile -t <name>:<tag> .`
- Layer 1 (floors, Noble-floating): python3, sqlite3, build-essential, binutils, gdb, git,
  curl, ca-certificates, perl, bc, bash, procps, iproute2, file, strace.
- Layer 2 (lane locks, intentional tripwires): `qemu-system-misc=1:8.2.2+ds-0ubuntu1.18`,
  `gcc-riscv64-unknown-elf=13.2.0-11ubuntu1+12`; plus unlocked `gcc-riscv64-linux-gnu`
  (preflight fallback prefix).
- Deliberately absent: PostgreSQL server, browsers, observability/SaaS backends,
  Docker-in-Docker, arm64 cross-toolchains (capability-gated/optional per curriculum boundary).
- `LANG=C.UTF-8 LC_ALL=C.UTF-8` is set so Python uses UTF-8 mode under the minimal base.

## 3. Locally built candidate identity (2026-09-10, implementer runtime)

- Built image ID: `sha256:9b862cb417234bb72e7c1869eb8d33e3cd8c98eda6c9628eb811ba13af907d32`
  (local tag `essential-cs-canonical:v0.1-issue145`, amd64/linux, 1.53 GB).
- This local tag is **not published** and therefore not durable: it is reproducible evidence,
  not the pin. The durable pin is the base digest in §1 plus this definition; the first
  CI build on hosted infrastructure produces the first independently retrievable build record.
- No container/package artifact was published (only repository-free infrastructure is permitted
  and none was needed for this candidate stage). Nothing below claims a published artifact.

## 4. Resolved package identities (inside the §3 build)

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

Observed tool surface (same build): CPython 3.12.3, embedded SQLite 3.45.1,
gcc 13.3.0, GDB 15.1, QEMU 8.2.2, riscv64-unknown-elf-gcc 13.2.0,
riscv64-linux-gnu-gcc 13.3.0, git 2.43.0, curl 8.5.0 / OpenSSL 3.0.13,
Ubuntu 24.04.4 LTS, x86_64. All D-032 floors met (see `scripts/canonical-env-capture.sh`).

## 5. Refresh runbook

- Re-pin quarterly or on security need: re-query the registry, rebuild, re-run the full matrix
  including a real LAB-REQ-02 QEMU smoke, then route the new digest for Lead acceptance.
- If a lane lock (`qemu-system-misc=…`, `gcc-riscv64-unknown-elf=…`) stops resolving because the
  Noble archive rotated, do NOT delete the version — update it deliberately and re-run the QEMU
  lane before acceptance (D-032: refresh requires a real QEMU smoke).
- `main` may forward-test newer toolchains without moving this candidate's contract.
