#!/usr/bin/env bash
set -euo pipefail
redline_python="${REDLINE_PYTHON:-python3}"
command -v "$redline_python" >/dev/null || { echo "Python 3.8+ is required. Install Python 3 with your distribution's package manager." >&2; exit 1; }
"$redline_python" -c 'import sys, ssl, zlib; sys.exit(0 if sys.platform == "linux" and sys.version_info >= (3, 8) else "Redline requires Linux and Python 3.8+.")'
export REDLINE_PYTHON="$redline_python"
release_url="https://github.com/stspivey76-byte/omarchy-redline-desktop/releases/latest/download"
work_dir="$(mktemp -d)"
trap 'rm -rf -- "$work_dir"' EXIT
fetch() {
  if command -v curl >/dev/null; then
    curl --fail --location --retry 3 "$1" -o "$2"
  elif command -v wget >/dev/null; then
    wget --tries=3 -O "$2" "$1"
  else
    "$redline_python" - "$1" "$2" <<'PYTHON'
import shutil, sys, urllib.request
with urllib.request.urlopen(sys.argv[1], timeout=60) as response, open(sys.argv[2], 'wb') as output:
    shutil.copyfileobj(response, output)
PYTHON
  fi
}
fetch "$release_url/redline-desktop.zip" "$work_dir/redline-desktop.zip"
fetch "$release_url/SHA256SUMS" "$work_dir/SHA256SUMS"
"$redline_python" - "$work_dir" <<'PYTHON'
import hashlib
from pathlib import Path
import re
import sys
import zipfile
root = Path(sys.argv[1])
archive_path = root / "redline-desktop.zip"
matches = re.findall(r"^([a-fA-F0-9]{64})\s+\*?redline-desktop\.zip$", (root / "SHA256SUMS").read_text(), re.M)
if len(matches) != 1 or hashlib.sha256(archive_path.read_bytes()).hexdigest() != matches[0].lower():
    raise SystemExit("Release ZIP checksum mismatch; nothing installed.")
with zipfile.ZipFile(archive_path) as archive:
    if sum(item.file_size for item in archive.infolist()) > 128 * 1024 * 1024:
        raise SystemExit("Release archive is too large")
    for item in archive.infolist():
        path = Path(item.filename)
        if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != "redline-desktop" or (item.external_attr >> 16) & 0o170000 == 0o120000:
            raise SystemExit("Unsafe release archive entry")
    archive.extractall(root)
print("Release checksum verified.")
PYTHON
bash "$work_dir/redline-desktop/install.sh" "$@"
