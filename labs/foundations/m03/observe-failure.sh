#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v gdb >/dev/null 2>&1 || { echo 'FAILURE GDB BLOCKED: gdb not found'; exit 2; }
[[ -x failure ]] || ./build.sh >/dev/null
cat > .gdb-failure.cmd <<'EOF2'
set pagination off
set confirm off
run
printf "FAILURE point=stopped\\n"
info program
printf "FAILURE rip=%p rsp=%p rbp=%p\\n", $rip, $rsp, $rbp
x/i $rip
bt 3
EOF2
set +e
gdb -q -batch -x .gdb-failure.cmd ./failure 2>&1 | tee failure-gdb.txt
rc=${PIPESTATUS[0]}
set -e
rm -f .gdb-failure.cmd
grep -Eq 'Program received signal SIGSEGV|stopped with signal SIGSEGV' failure-gdb.txt || {
  echo "FAILURE CHECK unexpected debugger result (gdb rc=$rc)"
  exit 1
}
echo 'FAILURE CHECK observed=SIGSEGV-under-this-hosted-build output=failure-gdb.txt'
