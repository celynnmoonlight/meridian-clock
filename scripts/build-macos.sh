#!/usr/bin/env bash
set -euo pipefail
[[ "$(uname -s)" == Darwin ]] || { echo "Run this script on macOS." >&2; exit 1; }
bash "$(dirname "$0")/build-unix.sh"
