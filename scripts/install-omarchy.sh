#!/usr/bin/env bash
set -euo pipefail
for command in omarchy python3; do
  command -v "$command" >/dev/null || { echo "Missing dependency: $command" >&2; exit 1; }
done
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
config_dir="$HOME/.config/omarchy"
mkdir -p "${XDG_STATE_HOME:-$HOME/.local/state}/omarchy/backups"
backup_dir="$(mktemp -d "${XDG_STATE_HOME:-$HOME/.local/state}/omarchy/backups/redline-desktop-$(date +%Y%m%d-%H%M%S)-XXXXXX")"
mkdir -p "$config_dir/themes"
if [[ -e "$config_dir/themes/redline" ]]; then
  mkdir -p "$backup_dir/themes"
  cp -a "$config_dir/themes/redline" "$backup_dir/themes/redline"
fi
mkdir -p "$config_dir/themes/redline"
cp -a "$source_dir/theme/." "$config_dir/themes/redline/"
# Preserve GTK files and any previous Redline hook before enabling color overrides.
for version in 3.0 4.0; do
  gtk_dir="$HOME/.config/gtk-$version"
  if [[ -e "$gtk_dir/gtk.css" || -L "$gtk_dir/gtk.css" ]]; then
    mkdir -p "$backup_dir/gtk-$version"
    cp -a "$gtk_dir/gtk.css" "$backup_dir/gtk-$version/"
  fi
done
hook_path="$config_dir/hooks/theme-set.d/redline-gtk"
if [[ -e "$hook_path" ]]; then
  mkdir -p "$backup_dir/hooks/theme-set.d"
  cp -a "$hook_path" "$backup_dir/hooks/theme-set.d/"
fi
omarchy hook install theme-set "$source_dir/hooks/redline-gtk"
omarchy theme set redline
# Also apply explicitly for environments that defer theme hooks.
bash "$hook_path" redline
omarchy theme bg set "$config_dir/themes/redline/backgrounds/tux-crimson-eclipse.png"
echo "Installed. Previous configuration saved in: $backup_dir"
