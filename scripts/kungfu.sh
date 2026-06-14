#!/usr/bin/env bash
# Brandon's Kung Fu — thin wrapper. Calls the Python CLI only.
# Contains NO install logic; all safety checks live in scripts/kungfu.py.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null 2>&1 || PY="python"
exec "$PY" "$HERE/kungfu.py" "$@"
