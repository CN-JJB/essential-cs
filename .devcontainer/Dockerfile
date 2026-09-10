# Essential CS canonical stable learner/test environment (candidate v0.1)
#
# Task: Issue #145. Governance: D-032. OQ-BP-006 remains OPEN until Web Lead acceptance.
#
# Base digest provenance: manifest-list digest for the `24.04` tag of `library/ubuntu`,
# retrieved 2026-09-10 via the Docker Registry HTTP API
# (GET https://registry-1.docker.io/v2/library/ubuntu/manifests/24.04 with
#  Accept: application/vnd.docker.distribution.manifest.list.v2+json;
#  response header docker-content-digest). Per-arch amd64 image manifest observed the same day:
#  sha256:a61567bd31828687156d735ea8eb01ba4e37636e225dd6a48ba94136a70d9d61
#  (Docker Hub tag metadata, tag_last_pushed 2026-09-09T17:54:13Z).
# Reconstruction: re-query the registry the same way and compare; any change means the
# upstream tag moved and this Dockerfile must be consciously re-pinned (refresh cadence:
# quarterly or on security need, with a real LAB-REQ-02 QEMU re-smoke before acceptance).
FROM ubuntu:24.04@sha256:224a1869083a311ef3f13648a154ba79832fbef6364d31493642ca03082da254

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Layer 1 — canonical required surface (D-032 floors; versions float inside Noble,
# floors are enforced at runtime by scripts/canonical-env-capture.sh).
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    python3 \
    sqlite3 \
    build-essential \
    binutils \
    gdb \
    git \
    curl \
    ca-certificates \
    perl \
    bc \
    bash \
    procps \
    iproute2 \
    file \
    strace \
 && rm -rf /var/lib/apt/lists

# Layer 2 — LAB-REQ-02 lane, version-locked (D-032 lane-scoped exactness).
# These locks are intentional tripwires: if the Noble archive rotates either version,
# this layer fails loudly and forces a conscious refresh + real QEMU re-smoke.
# Do NOT "fix" a lock failure by deleting the version — follow the refresh runbook in
# .devcontainer/CANONICAL_ENVIRONMENT.md.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    qemu-system-misc=1:8.2.2+ds-0ubuntu1.18 \
    gcc-riscv64-unknown-elf=13.2.0-11ubuntu1+12 \
    gcc-riscv64-linux-gnu \
 && rm -rf /var/lib/apt/lists

# Deliberately NOT installed: PostgreSQL server, psql extras beyond need, browsers,
# observability/SaaS backends, Docker-in-Docker, arm64 cross-toolchains.
# Those remain capability-gated or optional per the accepted curriculum boundary.

WORKDIR /work
CMD ["bash"]
