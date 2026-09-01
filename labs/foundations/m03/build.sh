#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
CC=${CC:-cc}
CFLAGS=(-std=c11 -Wall -Wextra -Wpedantic -g3 -O0 -fno-omit-frame-pointer -fno-inline -no-pie)
"$CC" "${CFLAGS[@]}" fixture.c -o fixture
"$CC" "${CFLAGS[@]}" failure.c -o failure
printf 'BUILD compiler=%s\n' "$($CC --version | head -n 1)"
printf 'BUILD flags=%s\n' "${CFLAGS[*]}"
