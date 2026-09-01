#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
rm -f fixture failure disassembly.txt gdb-trace.txt failure-gdb.txt core core.*
printf 'RESET result=clean\n'
