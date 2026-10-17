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
omarchy theme set redline
omarchy theme bg set "$config_dir/themes/redline/backgrounds/tux-crimson-eclipse.png"
echo "Installed. Previous configuration saved in: $backup_dir"
