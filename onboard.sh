#!/usr/bin/env bash
set -euo pipefail
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python="$root/.venv/bin/python"
# Help/status/preview remain available before installing the robot environment.
if [[ ! -x "$python" ]]; then
  case "${1:-}" in --help|-h|--status|--dry-run) python=python3 ;;
    *) echo 'Run ./install.sh first to create the locked robot environment.' >&2; exit 1 ;;
  esac
fi
cd -- "$root"
exec "$python" -B "$root/scripts/onboard.py" "$@"
