#!/usr/bin/env bash
# Materialize the canonical environment by its immutable registry digest.
#
# Task: Issue #150 (V-147-02). Governance: D-032.
#
# This is the ONLY supported way for release-relevant CI to obtain the canonical
# environment. It never builds. It resolves nothing by tag. It pulls the exact
# content-addressed reference committed in .devcontainer/canonical-image.env.
#
# Identity discipline:
#   registry digest  -> the pin; exported as CANONICAL_IMAGE
#   local image ID   -> recorded for audit only, explicitly NOT the pin
#   mutable tags     -> recorded for audit only, explicitly NOT the pin
#   git SHA          -> recorded for audit only, explicitly NOT the pin
#   runner image     -> recorded for audit only, explicitly NOT the pin
#
# Fail-closed conditions: missing/unset/malformed pin, recipe drift (committed
# Dockerfile no longer matches the blob the digest was built from), pull failure,
# or RepoDigests that do not contain the pinned reference.
set -ueo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
env_file="${repo_root}/.devcontainer/canonical-image.env"

if [ ! -f "${env_file}" ]; then
  echo "FAIL: missing canonical pin file ${env_file}"
  exit 1
fi

set -a
# shellcheck disable=SC1090
. "${env_file}"
set +a

: "${CANONICAL_IMAGE_REF:?CANONICAL_IMAGE_REF missing in canonical-image.env}"
: "${CANONICAL_IMAGE_DIGEST:?CANONICAL_IMAGE_DIGEST missing in canonical-image.env}"

PLATFORM="${CANONICAL_IMAGE_PLATFORM:-linux/amd64}"

if ! printf '%s' "${CANONICAL_IMAGE_REF}" | grep -Eq '^ghcr\.io/cn-jjb/essential-cs/canonical$'; then
  echo "FAIL: unexpected CANONICAL_IMAGE_REF: ${CANONICAL_IMAGE_REF}"
  exit 1
fi

if ! printf '%s' "${CANONICAL_IMAGE_DIGEST}" | grep -Eq '^sha256:[0-9a-f]{64}$'; then
  echo "FAIL: CANONICAL_IMAGE_DIGEST is not sha256:<64 lowercase hex>: ${CANONICAL_IMAGE_DIGEST}"
  exit 1
fi

if printf '%s' "${CANONICAL_IMAGE_DIGEST}" | grep -q '^sha256:0\{64\}$'; then
  echo "FAIL: canonical environment pin is still the unpublished sentinel."
  echo "      No durable canonical image has been published and pinned yet."
  exit 1
fi

# Recipe-drift tripwire: the digest is only meaningful together with the exact
# Dockerfile that produced it. If the recipe changed without a pin refresh, stop.
DOCKERFILE_REL="${CANONICAL_IMAGE_SOURCE_DOCKERFILE:-.devcontainer/Dockerfile}"
if [ -n "${CANONICAL_IMAGE_SOURCE_DOCKERFILE_BLOB:-}" ] && [ -d "${repo_root}/.git" ]; then
  actual_blob="$(git -C "${repo_root}" hash-object "${DOCKERFILE_REL}")"
  echo "RECIPE_DOCKERFILE=${DOCKERFILE_REL}"
  echo "RECIPE_BLOB_COMMITTED=${CANONICAL_IMAGE_SOURCE_DOCKERFILE_BLOB}"
  echo "RECIPE_BLOB_ACTUAL=${actual_blob}"
  if [ "${actual_blob}" != "${CANONICAL_IMAGE_SOURCE_DOCKERFILE_BLOB}" ]; then
    echo "FAIL: recipe drift — committed ${DOCKERFILE_REL} no longer matches the blob"
    echo "      the pinned digest was built from. Refresh the pin through a reviewed PR"
    echo "      (see .devcontainer/CANONICAL_ENVIRONMENT.md section 7)."
    exit 1
  fi
  echo "RECIPE_BLOB_MATCH=YES"
fi

PIN="${CANONICAL_IMAGE_REF}@${CANONICAL_IMAGE_DIGEST}"
GIT_SHA="$(git -C "${repo_root}" rev-parse HEAD 2>/dev/null || echo unset)"

echo "=== CANONICAL IMAGE IDENTITY (pre-pull) ==="
echo "intended_registry_digest=${CANONICAL_IMAGE_DIGEST}"
echo "pull_reference=${PIN}"
echo "platform=${PLATFORM}"
echo "local_image_id=(not yet pulled)"
echo "mutable_tag_candidate=${CANONICAL_IMAGE_REF}:candidate"
echo "source_dockerfile=${DOCKERFILE_REL}"
echo "source_base_digest=${CANONICAL_IMAGE_SOURCE_BASE_DIGEST:-unset}"
echo "git_sha=${GIT_SHA}"
echo "workflow_run_id=${GITHUB_RUN_ID:-unset}"
echo "runner_image_version=${ImageVersion:-unset}"
echo "runner_arch=$(uname -m)"
echo "NOTE: intended_registry_digest is the pin; local image ID, mutable tags,"
echo "      git SHA and runner image version are audit fields, NOT the pin."
echo "==========================================="

docker pull --platform "${PLATFORM}" "${PIN}"

LOCAL_ID="$(docker image inspect "${PIN}" --format '{{.Id}}')"
REPO_DIGESTS="$(docker image inspect "${PIN}" --format '{{range .RepoDigests}}{{.}} {{end}}')"

echo "=== CANONICAL IMAGE IDENTITY (post-pull) ==="
echo "intended_registry_digest=${CANONICAL_IMAGE_DIGEST}"
echo "pull_reference=${PIN}"
echo "platform=${PLATFORM}"
echo "local_image_id=${LOCAL_ID}"
echo "repo_digests_begin"
printf '%s\n' "${REPO_DIGESTS}"
echo "repo_digests_end"
echo "NOTE: local_image_id is a daemon-local identifier produced by this pull;"
echo "      it is NOT durable, NOT retrievable by itself, and NOT the pin."
echo "==========================================="

printf '%s\n' "${REPO_DIGESTS}" | grep -Fq "${PIN}" || {
  echo "FAIL: RepoDigests do not contain the pinned reference ${PIN}"
  exit 1
}
echo "REPO_DIGESTS_CONTAIN_PIN=YES"
echo "INTENDED_REGISTRY_DIGEST=${CANONICAL_IMAGE_DIGEST}"

export CANONICAL_IMAGE="${PIN}"
if [ -n "${GITHUB_ENV:-}" ]; then
  {
    echo "CANONICAL_IMAGE=${PIN}"
    echo "CANONICAL_IMAGE_DIGEST=${CANONICAL_IMAGE_DIGEST}"
    echo "CANONICAL_IMAGE_REF=${CANONICAL_IMAGE_REF}"
  } >> "${GITHUB_ENV}"
fi
if [ -n "${GITHUB_OUTPUT:-}" ]; then
  {
    echo "canonical_image=${PIN}"
    echo "canonical_image_digest=${CANONICAL_IMAGE_DIGEST}"
  } >> "${GITHUB_OUTPUT}"
fi

echo "CANONICAL_IMAGE=${PIN}"
