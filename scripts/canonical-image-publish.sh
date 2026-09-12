#!/usr/bin/env bash
# Publish a candidate canonical environment image to repository-owned GHCR and
# record its immutable OCI registry digest.
#
# Task: Issue #150 (V-147-02). Governance: D-032.
#
# This script builds from the committed recipe (.devcontainer/Dockerfile, which
# itself FROMs an immutable Ubuntu base digest) and pushes to repository-owned
# GHCR. It records the registry manifest digest returned by publication.
#
# It NEVER writes the committed canonical pin (.devcontainer/canonical-image.env).
# Moving the accepted pin requires a reviewed PR (CANONICAL_ENVIRONMENT.md §7).
#
# Identity discipline:
#   registry digest  -> the durable, retrievable identity (published by this script)
#   local image ID   -> daemon-local and ephemeral; NOT identity
#   mutable tags     -> convenience labels (:candidate, :sha-<sha>); NOT identity
#   git SHA          -> source revision; NOT identity
#   runner image     -> moving execution substrate; NOT identity
#
# Usage: scripts/canonical-image-publish.sh
# Env:   CANONICAL_IMAGE_REF          (default ghcr.io/cn-jjb/essential-cs/canonical)
#        CANONICAL_IMAGE_PLATFORM     (default linux/amd64)
#        CANONICAL_PUBLISH_EVIDENCE_DIR (default /tmp/canonical-publish)
set -ueo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

CANONICAL_IMAGE_REF="${CANONICAL_IMAGE_REF:-ghcr.io/cn-jjb/essential-cs/canonical}"
PLATFORM="${CANONICAL_IMAGE_PLATFORM:-linux/amd64}"
DOCKERFILE_REL=".devcontainer/Dockerfile"
EVIDENCE_DIR="${CANONICAL_PUBLISH_EVIDENCE_DIR:-/tmp/canonical-publish}"

mkdir -p "${EVIDENCE_DIR}"

GIT_SHA="$(git -C "${repo_root}" rev-parse HEAD 2>/dev/null || echo unset)"
DOCKERFILE_BLOB="$(git -C "${repo_root}" hash-object "${DOCKERFILE_REL}" 2>/dev/null || echo unset)"

{
  echo "publish_kind=CANDIDATE"
  echo "recipe_dockerfile=${DOCKERFILE_REL}"
  echo "recipe_dockerfile_blob=${DOCKERFILE_BLOB}"
  echo "platform=${PLATFORM}"
  echo "source_revision=${GIT_SHA}"
  echo "workflow_run_id=${GITHUB_RUN_ID:-unset}"
  echo "workflow_run_url=${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-CN-JJB/essential-cs}/actions/runs/${GITHUB_RUN_ID:-0}"
  echo "runner_image_version=${ImageVersion:-unset}"
  echo "runner_arch=$(uname -m)"
  echo "runner_os_release_begin"
  head -n 3 /etc/os-release || true
  echo "runner_os_release_end"
} | tee "${EVIDENCE_DIR}/substrate.txt"

echo "=== BUILDING CANDIDATE (recipe is NOT the pin) ==="
docker buildx version
docker buildx build \
  --platform "${PLATFORM}" \
  --file "${repo_root}/${DOCKERFILE_REL}" \
  --provenance=false \
  --sbom=false \
  --label "org.opencontainers.image.source=https://github.com/${GITHUB_REPOSITORY:-CN-JJB/essential-cs}" \
  --label "org.opencontainers.image.revision=${GIT_SHA}" \
  --label "org.opencontainers.image.title=essential-cs-canonical" \
  --tag "${CANONICAL_IMAGE_REF}:candidate" \
  --tag "${CANONICAL_IMAGE_REF}:sha-${GIT_SHA}" \
  --metadata-file "${EVIDENCE_DIR}/build-metadata.json" \
  --push \
  "${repo_root}"

python3 - "${EVIDENCE_DIR}" <<'PY'
import json, os, re, sys

evidence_dir = sys.argv[1]
meta = json.load(open(os.path.join(evidence_dir, "build-metadata.json")))

digest = str(meta.get("containerimage.digest", ""))
config_digest = str(meta.get("containerimage.config.digest", ""))
manifest_descriptor = meta.get("containerimage.descriptor", {})

if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
    print(f"FAIL: publication did not return a well-formed registry digest: {digest!r}")
    raise SystemExit(1)

with open(os.path.join(evidence_dir, "registry-digest.txt"), "w") as fh:
    fh.write(digest + "\n")
with open(os.path.join(evidence_dir, "config-digest.txt"), "w") as fh:
    fh.write(config_digest + "\n")

print("PUBLISHED_REGISTRY_DIGEST=" + digest)
print("PUBLISHED_CONFIG_DIGEST=" + config_digest)
if manifest_descriptor:
    print("PUBLISHED_DESCRIPTOR_MEDIA_TYPE=" + str(manifest_descriptor.get("mediaType", "")))
    print("PUBLISHED_DESCRIPTOR_SIZE=" + str(manifest_descriptor.get("size", "")))
print("METADATA_IDENTITY_KEYS=" + ",".join(sorted(k for k in meta if "digest" in k.lower())))
PY

REGISTRY_DIGEST="$(tr -d '[:space:]' < "${EVIDENCE_DIR}/registry-digest.txt")"
PIN="${CANONICAL_IMAGE_REF}@${REGISTRY_DIGEST}"

echo "=== REGISTRY-SIDE INSPECTION (independent of the local daemon) ==="
docker buildx imagetools inspect "${PIN}" | tee "${EVIDENCE_DIR}/imagetools-inspect.txt"

echo "=== LOCAL DAEMON IDENTITY (audit only, explicitly NOT the pin) ==="
LOCAL_ID="$(docker image inspect "${CANONICAL_IMAGE_REF}:candidate" --format '{{.Id}}')"
{
  echo "=== IDENTITY SEPARATION TABLE ==="
  echo "registry_ref=${CANONICAL_IMAGE_REF}"
  echo "registry_digest=${REGISTRY_DIGEST}"
  echo "registry_digest_role=PIN (durable, content-addressed, retrievable)"
  echo "pull_reference=${PIN}"
  echo "config_digest=${CONFIG_DIGEST:-$(cat "${EVIDENCE_DIR}/config-digest.txt" 2>/dev/null || echo unknown)}"
  echo "local_image_id=${LOCAL_ID}"
  echo "local_image_id_role=NOT-PIN (daemon-local, ephemeral, not retrievable)"
  echo "mutable_tag_candidate=${CANONICAL_IMAGE_REF}:candidate"
  echo "mutable_tag_sha=${CANONICAL_IMAGE_REF}:sha-${GIT_SHA}"
  echo "mutable_tag_role=NOT-PIN (labels that may be repointed)"
  echo "git_sha=${GIT_SHA}"
  echo "git_sha_role=NOT-PIN (source revision)"
  echo "runner_image_version=${ImageVersion:-unset}"
  echo "runner_image_role=NOT-PIN (moving execution substrate)"
  echo "================================="
} | tee "${EVIDENCE_DIR}/identity.txt"

echo "=== PIN IMMUTABILITY GUARD ==="
if git -C "${repo_root}" diff --quiet -- .devcontainer/canonical-image.env; then
  echo "PUBLISH_DID_NOT_MODIFY_PIN=YES"
else
  echo "FAIL: publication modified the committed canonical pin; that is forbidden."
  exit 1
fi

echo "CANDIDATE_PUBLISHED_REGISTRY_DIGEST=${REGISTRY_DIGEST}"
echo "CANDIDATE_PUBLISHED_REFERENCE=${PIN}"
