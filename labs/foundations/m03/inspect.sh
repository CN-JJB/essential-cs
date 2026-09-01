#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[[ -x fixture ]] || ./build.sh >/dev/null
nm -n fixture | grep -E ' [Tt] (main|helper)$'
objdump -d -S --no-show-raw-insn fixture > disassembly.txt
objdump -d --no-show-raw-insn fixture > /tmp/m03-plain-disassembly.txt
printf '%s\n' '--- helper disassembly (bounded plain view) ---'
sed -n '/<helper>:/,/^$/p' /tmp/m03-plain-disassembly.txt
printf '%s\n' '--- caller region containing helper call ---'
sed -n '/<main>:/,/^$/p' /tmp/m03-plain-disassembly.txt | grep -B8 -A6 '<helper>' || true
printf '%s\n' '--- source-aware mapping anchors ---'
grep -n -E 'long helper|long local|return local|long result = helper' disassembly.txt || true
printf 'INSPECT source_aware_output=disassembly.txt\n'
