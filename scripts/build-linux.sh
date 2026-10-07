#!/usr/bin/env bash
set -euo pipefail
[[ "$(uname -s)" == Linux ]] || { echo "Run this script on Linux." >&2; exit 1; }
bash "$(dirname "$0")/build-unix.sh"
