#!/usr/bin/env bash
set -euo pipefail
redline_python="${REDLINE_PYTHON:-python3}"
command -v "$redline_python" >/dev/null || { echo "Python 3.8+ is required. Install Python 3 with your distribution's package manager." >&2; exit 1; }
"$redline_python" -c 'import sys; sys.exit(0 if sys.platform == "linux" and sys.version_info >= (3, 8) else "Redline requires Linux and Python 3.8+. Set REDLINE_PYTHON to a newer Python executable if needed.")'
export REDLINE_PYTHON="$redline_python"
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec "$redline_python" "$source_dir/scripts/install-desktop.py" "$@"
