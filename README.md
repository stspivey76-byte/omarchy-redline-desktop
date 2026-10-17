# Redline Omarchy Desktop

A copy of Steven’s red and black Omarchy theme, crimson Tux wallpaper, custom top bar, and nine user plugins.

![Crimson Tux wallpaper](theme/backgrounds/tux-crimson-eclipse.png)

## Included

- Redline color palette and shell styling.
- Current wallpaper and the original black background.
- Custom Omarchy Eclipse Fastfetch logo and matching red/orange system information layout.
- Taskbar layout, global shell styling, and idle settings (screensaver after 150 seconds; lock after 300).
- Custom bar, workspaces, active window, clock/calendar, weather, resources, playback spectrum, software updates, and media plugins. The media clone is included, but the saved layout uses the built-in media widget.

## Requirements

Omarchy with its Quickshell-based shell and compatible plugin API. This is not a Waybar configuration. Python 3 powers resource meters and update checks. The spectrum needs `pactl` and `parec` (Arch package `libpulse`). Weather needs `curl` and uses Open-Meteo and wttr.in. Update checks use installed tools such as `checkupdates`, `yay`, `mise`, `flatpak`, and `fwupdmgr`.

## Install

Install everything with one command on an existing compatible Omarchy desktop:

```bash
curl -fsSL https://raw.githubusercontent.com/stspivey76-byte/omarchy-redline-desktop/main/download.sh | bash
```

This downloads the latest release ZIP, checks its SHA-256 checksum, and runs the bundled installer. Requires `curl`, `python3`, and `sha256sum` in addition to Omarchy. Run as your normal desktop user, without `sudo`.

Prefer a manual download? Get **[redline-desktop.zip from the latest release](https://github.com/stspivey76-byte/omarchy-redline-desktop/releases/latest)**, extract it, open a terminal in the extracted `redline-desktop` folder, and run:

```bash
bash install.sh
```

The ZIP includes the theme, both wallpapers, all nine plugins, shell configuration, Fastfetch logo/configuration, and installer. No Git checkout is needed.

## Update

Run the same one-command installer again to install the latest release. Each run backs up the configuration it replaces. Updates overwrite local edits to the bundled theme, plugins, Fastfetch configuration, and shell layout; save any custom changes first.

The installer backs up affected configuration first, installs the theme and plugins, applies Redline, and selects the included wallpaper. It replaces your shell layout, idle settings, and Fastfetch configuration. The Fastfetch logo path is set for your own home directory; run `fastfetch` to see it. Fastfetch must already be installed. Backups are saved under `~/.local/state/omarchy/backups/redline-desktop-*`; their paths are printed during installation. To restore, copy the backed-up files and directories to their original locations and reapply your previous theme. Fastfetch backups are in the backup’s `fastfetch/` folder; restore those files to `~/.config/fastfetch/`.

Only the export has been made portable; the source desktop configuration was left untouched. Plugin IDs retain the `steven.*` namespace so the layout continues to match. No weather location, credentials, clipboard history, notifications, caches, or old configuration backups are included.

## Attribution

Several plugins were cloned from Omarchy and retain their original author metadata. Their upstream source is https://github.com/basecamp/omarchy. Existing upstream license terms apply to that code. Wallpaper authorship and redistribution terms have not been established by this export; no new license is asserted for the wallpaper or other included assets.
