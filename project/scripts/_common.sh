#!/usr/bin/env bash
# Shared helpers for the Mini Cloud scripts.
#
# On a Linux host (including the canonical image) these are the identity. On
# Git Bash / Windows they matter: a native python.exe does not understand
# "/g/ai_project/..." and silently resolves it as the drive-relative path
# "G:\g\ai_project\...". Any path handed to Python must therefore be converted.

native_path() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w -- "$1"
  else
    printf '%s' "$1"
  fi
}
