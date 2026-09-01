#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")"
status=0
need() {
  if command -v "$1" >/dev/null 2>&1; then
    printf 'PREFLIGHT %-12s PASS %s\n' "$1" "$(command -v "$1")"
  else
    printf 'PREFLIGHT %-12s BLOCKED missing\n' "$1"
    status=2
  fi
}
printf 'PREFLIGHT os=%s\n' "$(uname -a)"
arch=$(uname -m)
printf 'PREFLIGHT arch=%s\n' "$arch"
if [[ "$arch" != "x86_64" ]]; then
  printf 'PREFLIGHT architecture BLOCKED / NON-CANONICAL ENVIRONMENT\n'
  status=2
fi
for tool in cc objdump nm gdb git; do need "$tool"; done
if command -v cc >/dev/null 2>&1; then printf 'PREFLIGHT compiler=%s\n' "$(cc --version | head -n 1)"; fi
if command -v objdump >/dev/null 2>&1; then printf 'PREFLIGHT objdump=%s\n' "$(objdump --version | head -n 1)"; fi
if command -v gdb >/dev/null 2>&1; then printf 'PREFLIGHT gdb=%s\n' "$(gdb --version | head -n 1)"; fi
printf 'PREFLIGHT git=%s\n' "$(git --version 2>/dev/null || printf missing)"
printf 'PREFLIGHT python=%s\n' "$(python3 --version 2>&1 || printf missing)"
printf 'PREFLIGHT shell=%s\n' "$(bash --version | head -n 1)"
if (( status == 0 )); then printf 'PREFLIGHT result=PASS\n'; else printf 'PREFLIGHT result=BLOCKED\n'; fi
exit "$status"
