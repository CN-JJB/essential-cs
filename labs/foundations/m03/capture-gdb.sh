#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v gdb >/dev/null 2>&1 || { echo 'GDB BLOCKED: gdb not found'; exit 2; }
[[ -x fixture ]] || ./build.sh >/dev/null
mapfile -t sites < <(objdump -d fixture | awk '
  /call.*<helper>/ {gsub(":", "", $1); print $1; want_next=1; next}
  want_next && /^[[:space:]]*[0-9a-f]+:/ {gsub(":", "", $1); print $1; exit}
')
[[ ${#sites[@]} -eq 2 ]] || { echo 'GDB BLOCKED: could not find call/return-site anchors'; exit 2; }
call_site=${sites[0]}
after_site=${sites[1]}
cat > .gdb-trace.cmd <<EOF2
set pagination off
set confirm off
set print pretty off
break *0x${call_site}
break helper
break *0x${after_site}
run
printf "TRACE point=before-call\\n"
printf "TRACE rip=%p rsp=%p rbp=%p\\n", \$rip, \$rsp, \$rbp
printf "TRACE rdi=%ld rsi=%ld rdx=%p\\n", \$rdi, \$rsi, \$rdx
x/gx \$rdx
continue
printf "TRACE point=callee\\n"
printf "TRACE rip=%p rsp=%p rbp=%p\\n", \$rip, \$rsp, \$rbp
printf "TRACE a=%ld b=%ld item=%p item_value=%ld\\n", a, b, item, item->value
next
printf "TRACE local=%ld\\n", local
continue
printf "TRACE point=after-return\\n"
printf "TRACE rip=%p rsp=%p rbp=%p rax=%ld\\n", \$rip, \$rsp, \$rbp, \$rax
continue
EOF2
gdb -q -batch -x .gdb-trace.cmd ./fixture | tee gdb-trace.txt
rm -f .gdb-trace.cmd
for marker in 'TRACE point=before-call' 'TRACE point=callee' 'TRACE point=after-return' 'TRACE local=30'; do
  grep -Fq "$marker" gdb-trace.txt || { echo "GDB CHECK FAIL missing: $marker"; exit 1; }
done
echo 'GDB CHECK result=PASS output=gdb-trace.txt'
