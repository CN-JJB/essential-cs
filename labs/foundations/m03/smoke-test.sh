#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./reset.sh >/dev/null
preflight=PASS
if ! ./preflight.sh; then preflight=PARTIAL; fi
./build.sh
baseline=$(./fixture)
[[ "$baseline" == 'result=37' ]] || { echo "SMOKE FAIL baseline=$baseline"; exit 1; }
nm -n fixture | grep -Eq ' [Tt] helper$'
objdump -d -S fixture > /tmp/m03-smoke-disassembly.txt
grep -q '<helper>:' /tmp/m03-smoke-disassembly.txt
./inspect.sh >/dev/null
set +e
./failure >/tmp/m03-failure.stdout 2>/tmp/m03-failure.stderr
failure_rc=$?
set -e
[[ $failure_rc -eq 139 ]] || { echo "SMOKE FAIL direct failure rc=$failure_rc"; exit 1; }
gdb_status=BLOCKED
if command -v gdb >/dev/null 2>&1; then
  ./capture-gdb.sh >/dev/null
  ./observe-failure.sh >/dev/null
  gdb_status=PASS
fi
printf 'SMOKE baseline=PASS value=37\n'
printf 'SMOKE symbol=PASS helper\n'
printf 'SMOKE disassembly=PASS helper\n'
printf 'SMOKE direct_failure=OBSERVED exit=%d (hosted observation only)\n' "$failure_rc"
printf 'SMOKE gdb=%s\n' "$gdb_status"
printf 'SMOKE preflight=%s\n' "$preflight"
if [[ "$gdb_status" == PASS && "$preflight" == PASS ]]; then
  echo 'SMOKE result=PASS'
else
  echo 'SMOKE result=PARTIAL'
fi
