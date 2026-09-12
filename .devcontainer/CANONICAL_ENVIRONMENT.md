# Canonical Environment Identity (v0.1 — Issue #150, V-147-02)

Governance: **D-032**. Status: **durable canonical artifact published and pinned; OQ-BP-006 remains OPEN.**

OQ-BP-006 closes only after the Web Lead accepts this pin following **independent
verification by a different verifier/harness than this implementation**. No v1.0 /
`VERIFIED` / stable `RELEASED` claim follows from this document, and no learner
validation is claimed.

---

## 1. What the canonical identity actually is

The canonical environment identity is a **published OCI image manifest digest in
repository-owned GHCR**, committed in `.devcontainer/canonical-image.env`:

```text
ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
```

That reference is content-addressed. Retrieving it returns the same bytes
whenever and wherever it is pulled, for as long as the package exists.

### Identity separation (do not conflate these)

| Thing | Value in this pin | Role |
| --- | --- | --- |
| **Registry manifest digest** | `sha256:766ce07b…19e460` | **THE PIN** — durable, retrievable, content-addressed |
| Config blob digest | `sha256:24a926a0…9d7805` | build output detail; not the pull address |
| Docker local image ID | `sha256:24a926a0…9d7805` | daemon-local and ephemeral; **not** identity |
| Mutable tags | `…canonical:candidate`, `…canonical:sha-<sha>` | convenience labels; may be repointed; **not** identity |
| Git commit / workflow SHA | `25804b02…b9032` (publication source) | source revision; **not** identity |
| Hosted runner image | `ubuntu-24.04` / `20260907.300.1` | moving execution substrate; **not** identity |

A local image ID, a mutable tag, a workflow SHA, a hosted-runner image version, or
a pinned base-image digest **alone** is not a canonical environment identity. The
durable identity is the registry digest.

---

## 2. Retrieval

Pull by digest only — never by tag:

```bash
docker pull --platform linux/amd64 \
  ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
```

The repository helper does the same thing with fail-closed checks:

```bash
scripts/canonical-image-pull.sh
```

It refuses to run if the digest is the unpublished sentinel, malformed, if the
committed Dockerfile no longer matches the recipe the digest was built from, or if
`RepoDigests` do not contain the pinned reference.

**Access:** the package is retrievable **anonymously (credential-free)** via the
standard GHCR token flow — a manifest `GET` with no credentials returns
`docker-content-digest: sha256:766ce07b…19e460`, and re-hashing the returned
manifest bytes reproduces that digest. No learner credentials are required.
Repository CI additionally consumes it with the repository-owned `GITHUB_TOKEN`
(`packages: read`), which is the minimum mechanism and needs no new secrets.

---

## 3. Publication architecture and permission boundary

- Workflow: `.github/workflows/publish-canonical-environment.yml`.
- Permissions: `contents: read`, `packages: write` — nothing else.
- Build: `scripts/canonical-image-publish.sh`, `--platform linux/amd64`, from the
  committed recipe `.devcontainer/Dockerfile` (which itself `FROM`s an immutable
  Ubuntu base digest).
- Registry digest is taken from the publication metadata and cross-checked against
  `docker buildx imagetools inspect` and against a **separate fresh runner's**
  clean pull-by-digest. The builder's local daemon cannot satisfy that proof.
- The workflow **cannot** write `.devcontainer/canonical-image.env`; a guard step
  asserts the pin file is unmodified after publication.
- A push can publish **only** while the committed pin is still the sentinel
  (one-shot bootstrap). Once a real digest is committed, a push can only verify —
  it can never publish or move the pin. Deliberate candidate publication requires
  an explicit `workflow_dispatch` (`mode: publish-candidate`) and still cannot move
  the pin.

---

## 4. Build inputs and the honest reproducibility boundary

- Recipe: `.devcontainer/Dockerfile` (+ `devcontainer.json`), blob
  `51198ea12c3c9ddfa18a2246bddef491ea729559`.
- Base input: `ubuntu:24.04@sha256:224a1869083a311ef3f13648a154ba79832fbef6364d31493642ca03082da254`
  (manifest-list digest for the `24.04` tag of `library/ubuntu`, retrieved
  2026-09-10 via the Docker Registry HTTP API).
- Layer 1 implements D-032 **version floors** from Noble apt repositories
  (python3, sqlite3, build-essential, binutils, gdb, git, curl, ca-certificates,
  perl, bc, bash, procps, iproute2, file, strace).
- Layer 2 keeps lane-scoped exact tripwires: `qemu-system-misc=1:8.2.2+ds-0ubuntu1.18`
  and `gcc-riscv64-unknown-elf=13.2.0-11ubuntu1+12`; `gcc-riscv64-linux-gnu`
  remains a captured fallback identity.
- Deliberately absent: PostgreSQL server, browsers, observability/SaaS backends,
  Docker-in-Docker, arm64 cross-toolchains.
- `LANG=C.UTF-8 LC_ALL=C.UTF-8` so Python uses UTF-8 under the minimal base.

**What is *not* claimed:** rebuilding `.devcontainer/Dockerfile` from live Noble
apt repositories on a later date is **not** byte-for-byte reproducible. Floor-allowed
package updates legitimately change the resulting image. This was directly observed:
repeated builds of the same definition produced different local image IDs, and on
2026-09-11 a per-run build failed outright at `apt-get install` because the archive
was unreachable.

**What *is* claimed:** the already-published immutable image above can be retrieved
by digest indefinitely, and that retrieval — not recipe replay — is the stability
guarantee. Any environment a lane actually executes is that published digest.

---

## 5. Observed identity inside the pinned digest

Captured by running `scripts/canonical-env-capture.sh` inside the image pulled
from the pinned digest (`CANONICAL_ENV_CAPTURE result=PASS`):

```text
os=Ubuntu 24.04.4 LTS        arch=x86_64
python=CPython 3.12.3        sqlite_embedded=3.45.1     sqlite3_cli=3.45.1
gcc=13.3.0                   gdb=15.1                  curl=8.5.0
qemu-system-riscv64=8.2.2 (Debian 1:8.2.2+ds-0ubuntu1.18)
riscv64-unknown-elf-gcc=13.2.0-11ubuntu1+12
riscv64-linux-gnu-gcc=13.3.0 (4:13.2.0-7ubuntu1)
binutils=2.42                 git=2.43.0               bash=5.2.21
strace=present-capability-gated
```

Resolved distro package identities observed in the pinned image:

```text
bash                    5.2.21-2ubuntu4
bc                      1.07.1-3ubuntu4
binutils                2.42-4ubuntu2.10
binutils-riscv64-linux-gnu   2.42-4ubuntu2.10
binutils-riscv64-unknown-elf 2.42-1ubuntu1+6
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
qemu-system-common      1:8.2.2+ds-0ubuntu1.18
qemu-system-data        1:8.2.2+ds-0ubuntu1.18
qemu-system-misc        1:8.2.2+ds-0ubuntu1.18
sqlite3                 3.45.1-1ubuntu2.7
strace                  6.8-0ubuntu2
```

---

## 6. How canonical CI consumes it

Both canonical lanes pull the **same** committed digest and build nothing:

- `canonical-fast` (`.github/workflows/ci-fast.yml`) — `canonical-matrix`.
- `canonical-qemu-lane` (`.github/workflows/ci-qemu-lane.yml`) — `qemu-smoke` and
  the diagnostic `m20-timing-triage`.

Each lane logs `COMMITTED_CANONICAL_DIGEST`, asserts that the reference it consumes
carries that digest, and separately records the hosted-runner image identity as an
explicit non-pin audit field. Environment capture, D-032 floors, and the lane
package tripwires still run **inside** the pulled image. There is no
`ubuntu-latest` assumption anywhere.

The #149 fail-closed QEMU evidence contract is unchanged: a green `qemu-smoke` job
still requires the real learner-owned `./smoke.sh` to have executed and retained a
non-empty `.ci-logs/req02-smoke.log` containing `QEMU_SMOKE_STATUS: PASS`, the
standalone `LAB_REQ_02_OK` marker, the final PASS banner, `QEMU_REAPED: TRUE`, and
`PID_MARKER_CLEAN: YES`.

---

## 7. Pin refresh governance (bounded sequence)

1. **Explicit trigger** — a committed Dockerfile/source change, or an intentional
   refresh decision. Never an automatic rebuild.
2. **Build candidate** — `workflow_dispatch` with `mode: publish-candidate`.
3. **Run required validation** — capture/floors, M10, m20, M03 GDB, the five
   Required Labs, and a real LAB-REQ-02 QEMU smoke against the candidate.
4. **Publish** — push to repository-owned GHCR under `packages: write`.
5. **Capture the immutable registry digest** — the manifest digest, not a tag and
   not a local image ID.
6. **Update the canonical digest only through a reviewed PR** — edit
   `.devcontainer/canonical-image.env` plus `CANONICAL_IMAGE_SOURCE_DOCKERFILE_BLOB`
   if the recipe changed. CI fails closed on recipe drift.
7. **Independently re-verify with a different verifier/harness** before the Web
   Lead advances the pin or closes OQ-BP-006.

A mutable-tag rebuild must never move the accepted canonical digest: the
publication workflow cannot write the pin, and the CI lanes refuse to run unless
the committed digest still resolves to the published content.

---

## 8. devcontainer materialization

`.devcontainer/devcontainer.json` points at the pinned digest directly, so a
devcontainer materializes the durable identity rather than rebuilding a
look-alike. `.devcontainer/Dockerfile` is retained as the **recipe of record** for
the next candidate refresh, not as the canonical identity.
