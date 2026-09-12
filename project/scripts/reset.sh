#!/usr/bin/env bash
# Mini Cloud reset — idempotent cleanup of generated state.
#
# Removes the project's own scratch directory and Python caches. It never
# touches tracked files and never removes anything outside project/.
set -ueo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd "${script_dir}/.." && pwd)"

echo "MINICLOUD_RESET_BEGIN"
echo "RESET_SCOPE ${project_dir}"

if [ -d "${project_dir}/var" ]; then
  rm -rf "${project_dir}/var"
  echo "RESET_REMOVED ${project_dir}/var"
else
  echo "RESET_NOTHING_TO_DO var"
fi

while IFS= read -r -d '' cache; do
  rm -rf "${cache}"
  echo "RESET_REMOVED ${cache}"
done < <(find "${project_dir}" -type d -name __pycache__ -print0 2>/dev/null)

echo "MINICLOUD_RESET: PASS"
