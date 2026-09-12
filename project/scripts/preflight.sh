#!/usr/bin/env bash
# Mini Cloud preflight — fail closed.
#
# Verifies the environment the Mini Cloud actually requires, and refuses to
# report success if any floor is missing. A missing tool is a FAIL, not a skip.
set -ueo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
project_dir="${repo_root}/project"
# shellcheck source=_common.sh
. "${script_dir}/_common.sh"

PY="${PYTHON:-python3}"
project_dir_native="$(native_path "${project_dir}")"
export PYTHONPATH="${project_dir_native}"

echo "MINICLOUD_PREFLIGHT_BEGIN"

if ! command -v "${PY}" >/dev/null 2>&1; then
  echo "PREFLIGHT_FAIL: interpreter not found: ${PY}"
  exit 1
fi
echo "TOOL_PRESENT python=${PY}"

# curl is required: the smoke drives real HTTP.
if ! command -v curl >/dev/null 2>&1; then
  echo "PREFLIGHT_FAIL: required tool not found: curl"
  exit 1
fi
echo "TOOL_PRESENT curl=$(command -v curl)"

# The sqlite3 CLI is part of the canonical environment (D-032) and is used for
# learner inspection, not by the smoke assertions themselves. It is required by
# default. A developer on a non-canonical host may opt out EXPLICITLY; the
# environment is then labelled non-canonical rather than silently accepted.
if command -v sqlite3 >/dev/null 2>&1; then
  echo "TOOL_PRESENT sqlite3=$(command -v sqlite3)"
elif [ "${MINICLOUD_PREFLIGHT_ALLOW_MISSING_SQLITE_CLI:-0}" = "1" ]; then
  echo "TOOL_MISSING sqlite3=ALLOWED_BY_EXPLICIT_OVERRIDE"
  echo "ENVIRONMENT_NOT_CANONICAL: sqlite3 CLI absent (override in effect)"
else
  echo "PREFLIGHT_FAIL: required tool not found: sqlite3"
  echo "                  set MINICLOUD_PREFLIGHT_ALLOW_MISSING_SQLITE_CLI=1 to run non-canonically"
  exit 1
fi

# Capability floors, checked by the same code the service uses.
"${PY}" - "${project_dir_native}" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
from minicloud.config import environment_report
report = environment_report()
for key in ("python_version", "python_floor", "sqlite_version", "sqlite_floor"):
    print(f"{key}={report[key]}")
if not report["python_ok"]:
    print("PREFLIGHT_FAIL: python below floor")
    sys.exit(1)
if not report["sqlite_ok"]:
    print("PREFLIGHT_FAIL: sqlite below floor")
    sys.exit(1)
PY

# Shell syntax gates for this project's own scripts.
for f in "${project_dir}"/scripts/*.sh; do
  if ! bash -n "${f}"; then
    echo "PREFLIGHT_FAIL: shell syntax error in ${f}"
    exit 1
  fi
done
echo "SHELL_SYNTAX_OK"

# Source must parse and the package must import (no __pycache__ artifacts written).
"${PY}" - "${project_dir_native}" <<'PY'
import ast
import os
import sys

project_dir = sys.argv[1]
for root, _dirs, files in os.walk(project_dir):
    if "__pycache__" in root:
        continue
    for name in files:
        if not name.endswith(".py"):
            continue
        path = os.path.join(root, name)
        with open(path, "rb") as handle:
            ast.parse(handle.read(), filename=path)
print("PYTHON_SOURCE_OK")
sys.path.insert(0, project_dir)
import minicloud  # noqa: F401
from minicloud import cli, httpd, indexer, service, store  # noqa: F401
print("PACKAGE_IMPORT_OK")
PY

echo "MINICLOUD_PREFLIGHT: PASS"
