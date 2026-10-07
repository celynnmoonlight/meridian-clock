#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync --locked
uv run python -m unittest discover -s tests -v
uv run pyinstaller --noconfirm packaging/meridian.spec
case "$(uname -s)" in
  Darwin)
    hdiutil create -volname "Meridian Clock" -srcfolder "dist/Meridian Clock.app" \
      -ov -format UDZO "dist/MeridianClock-macOS.dmg"
    ;;
  Linux)
    tar -czf dist/MeridianClock-linux.tar.gz -C dist MeridianClock
    ;;
  *) echo "Use scripts/build-windows.ps1 on Windows." >&2; exit 1 ;;
esac
