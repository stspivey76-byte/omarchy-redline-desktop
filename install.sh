#!/usr/bin/env bash
set -euo pipefail
for command in omarchy python3; do
  command -v "$command" >/dev/null || { echo "Missing dependency: $command" >&2; exit 1; }
done
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
config_dir="$HOME/.config/omarchy"
mkdir -p "${XDG_STATE_HOME:-$HOME/.local/state}/omarchy/backups"
backup_dir="$(mktemp -d "${XDG_STATE_HOME:-$HOME/.local/state}/omarchy/backups/redline-desktop-$(date +%Y%m%d-%H%M%S)-XXXXXX")"
mkdir -p "$config_dir/themes" "$config_dir/plugins" "$backup_dir/plugins"
for item in shell.json shell.toml themes/redline; do
  if [[ -e "$config_dir/$item" ]]; then
    mkdir -p "$backup_dir/$(dirname "$item")"
    cp -a "$config_dir/$item" "$backup_dir/$item"
  fi
done
for plugin in "$source_dir"/plugins/*; do
  name="$(basename "$plugin")"
  [[ ! -e "$config_dir/plugins/$name" ]] || cp -a "$config_dir/plugins/$name" "$backup_dir/plugins/"
  mkdir -p "$config_dir/plugins/$name"
  cp -a "$plugin/." "$config_dir/plugins/$name/"
done
mkdir -p "$config_dir/themes/redline"
cp -a "$source_dir/theme/." "$config_dir/themes/redline/"
cp "$source_dir/shell.json" "$source_dir/shell.toml" "$config_dir/"
# Keep the previous Fastfetch configuration and logo alongside the Omarchy backup.
fastfetch_dir="$HOME/.config/fastfetch"
mkdir -p "$fastfetch_dir" "$backup_dir/fastfetch"
for item in config.jsonc omarchy-eclipse.txt; do
  if [[ -e "$fastfetch_dir/$item" ]]; then
    cp -a "$fastfetch_dir/$item" "$backup_dir/fastfetch/$item"
  fi
done
cp "$source_dir/fastfetch/omarchy-eclipse.txt" "$fastfetch_dir/"
python3 - "$source_dir/fastfetch/config.jsonc" "$fastfetch_dir" <<'PYTHON'
import json
from pathlib import Path
import sys
config = json.loads(Path(sys.argv[1]).read_text())
destination = Path(sys.argv[2])
config["logo"]["source"] = str(destination / "omarchy-eclipse.txt")
(destination / "config.jsonc").write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
PYTHON
omarchy theme set redline
omarchy theme bg set "$config_dir/themes/redline/backgrounds/tux-crimson-eclipse.png"
echo "Installed. Previous configuration saved in: $backup_dir"
