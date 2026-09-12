#!/usr/bin/env bash
# Mini Cloud end-to-end smoke — fail closed.
#
# Starts the real service and the real dependency as separate processes, drives
# real HTTP requests against them, restarts the service to prove durable state
# survives, and then asserts the processes are gone and the evidence exists.
#
# Fail-closed rules:
#   * any missing tool, failed request, or missing evidence line is a FAIL;
#   * the script re-checks the driver's explicit SMOKE_EVIDENCE lines, so a
#     silently-skipped step cannot look green;
#   * the final banner is only printed after every assertion passed.
#
# Usage: project/scripts/smoke.sh [--keep]
set -ueo pipefail

KEEP=0
if [ "${1:-}" = "--keep" ]; then
  KEEP=1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
project_dir="${repo_root}/project"
# shellcheck source=_common.sh
. "${script_dir}/_common.sh"

PY="${PYTHON:-python3}"
driver_native="$(native_path "${project_dir}/scripts/smoke_driver.py")"
export PYTHONPATH="$(native_path "${project_dir}")"

run_dir="${project_dir}/var/smoke-$$"
log_dir="${run_dir}/logs"
mkdir -p "${log_dir}"

indexer_pid=""
service_pid=""
indexer_url=""
base_url=""

fail() {
  echo "MINICLOUD_SMOKE_STATUS: FAIL"
  echo "SMOKE_FAIL_REASON: $*"
  exit 1
}

stop_pid() {
  local pid="${1:-}"
  [ -n "${pid}" ] || return 0
  if kill -0 "${pid}" 2>/dev/null; then
    kill "${pid}" 2>/dev/null || true
    for _ in $(seq 1 50); do
      kill -0 "${pid}" 2>/dev/null || break
      sleep 0.1
    done
    if kill -0 "${pid}" 2>/dev/null; then
      kill -9 "${pid}" 2>/dev/null || true
    fi
  fi
  wait "${pid}" 2>/dev/null || true
}

cleanup() {
  local status=$?
  stop_pid "${service_pid}"
  stop_pid "${indexer_pid}"
  service_pid=""
  indexer_pid=""
  if [ "${KEEP}" -eq 0 ] && [ "${status}" -eq 0 ]; then
    rm -rf "${run_dir}"
  else
    echo "SMOKE_ARTIFACTS ${run_dir}"
  fi
  return "${status}"
}
trap cleanup EXIT

echo "SMOKE_RUN_DIR ${run_dir}"
echo "SMOKE_PYTHON ${PY}"

# --- preflight ------------------------------------------------------------
"${script_dir}/preflight.sh" >"${log_dir}/preflight.log" 2>&1 || fail "preflight failed"
grep -q "MINICLOUD_PREFLIGHT: PASS" "${log_dir}/preflight.log" || fail "preflight did not report PASS"

# --- dependency process ---------------------------------------------------
"${PY}" -m minicloud.cli run-indexer \
  --port-file "$(native_path "${run_dir}/indexer.port")" --fault ok \
  >"${log_dir}/indexer.out" 2>&1 &
indexer_pid=$!
for _ in $(seq 1 100); do
  [ -s "${run_dir}/indexer.port" ] && break
  sleep 0.1
done
[ -s "${run_dir}/indexer.port" ] || fail "indexer did not report a bound port"
indexer_url="http://127.0.0.1:$(cat "${run_dir}/indexer.port")"
echo "SMOKE_INDEXER_URL ${indexer_url}"

export MINICLOUD_DB_PATH="$(native_path "${run_dir}/minicloud.db")"
export MINICLOUD_INDEXER_URL="${indexer_url}"
export MINICLOUD_LOG_PATH="$(native_path "${log_dir}/minicloud.log")"
# PBKDF2 iterations are NOT lowered here: the production default applies unless
# the caller explicitly overrides it. Weakening a credential floor to make a
# smoke test faster would be the wrong trade.
export MINICLOUD_DEP_TIMEOUT_MS="${MINICLOUD_DEP_TIMEOUT_MS:-1500}"

# --- service process ------------------------------------------------------
start_service() {
  rm -f "${run_dir}/service.port"
  "${PY}" -m minicloud.cli serve --port 0 \
    --port-file "$(native_path "${run_dir}/service.port")" \
    >"${log_dir}/service.out" 2>&1 &
  service_pid=$!
  for _ in $(seq 1 100); do
    [ -s "${run_dir}/service.port" ] && break
    sleep 0.1
  done
  [ -s "${run_dir}/service.port" ] || return 1
  base_url="http://127.0.0.1:$(cat "${run_dir}/service.port")"
  # Bounded readiness wait: never assume the socket is accepting immediately.
  for _ in $(seq 1 100); do
    if curl -fsS "${base_url}/health" >/dev/null 2>&1; then
      return 0
    fi
    sleep 0.1
  done
  return 1
}

start_service || fail "service did not become healthy"
echo "SMOKE_BASE_URL ${base_url}"

# --- semantic assertions over real HTTP -----------------------------------
set +e
"${PY}" "${driver_native}" \
  --base-url "${base_url}" \
  --indexer-url "${indexer_url}" \
  --json-out "$(native_path "${run_dir}/smoke.json")" | tee "${log_dir}/smoke-driver.log"
driver_status=${PIPESTATUS[0]}
set -e
[ "${driver_status}" -eq 0 ] || fail "smoke driver reported failure"

# Re-check every required evidence line: a skipped step must not look green.
for required in \
  health create read-back list invalid-request-rejected cross-user-denied \
  share shared-read revoke revoked-denied dependency-indexed \
  dependency-failure-degrades-index degraded-item-durable recovery-reindex \
  observability-metrics; do
  grep -q "SMOKE_EVIDENCE: PASS ${required}$" "${log_dir}/smoke-driver.log" \
    || fail "missing or failing evidence: ${required}"
done

# --- restart persistence --------------------------------------------------
item_id="$("${PY}" - "$(native_path "${run_dir}/smoke.json")" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as handle:
    print(json.load(handle)["item_id"])
PY
)"
[ -n "${item_id}" ] || fail "no item id captured for the restart check"

stop_pid "${service_pid}"
service_pid=""
start_service || fail "service did not restart cleanly"

"${PY}" "${driver_native}" \
  --base-url "${base_url}" \
  --indexer-url "${indexer_url}" \
  --verify-item "${item_id}" \
  --expect-title "smoke-note" | tee -a "${log_dir}/smoke-driver.log" \
  || fail "restart-persistence check failed"
grep -q "SMOKE_EVIDENCE: PASS restart-persistence$" "${log_dir}/smoke-driver.log" \
  || fail "missing restart-persistence evidence"

# --- observability evidence ----------------------------------------------
grep -q '"event": "http.request"' "${log_dir}/minicloud.log" || fail "no structured http.request log lines"
grep -q '"request_id"' "${log_dir}/minicloud.log" || fail "no request correlation ids in logs"
if grep -q "smoke-password" "${log_dir}/minicloud.log"; then
  fail "a password leaked into the structured log"
fi
echo "SMOKE_EVIDENCE: PASS log-redaction"

# --- clean shutdown -------------------------------------------------------
stop_pid "${service_pid}"
service_pid=""
stop_pid "${indexer_pid}"
indexer_pid=""

echo "SMOKE_EVIDENCE: PASS clean-shutdown"
echo "MINICLOUD_SMOKE_STATUS: PASS"
echo "MINICLOUD_SMOKE_OK"
