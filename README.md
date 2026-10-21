# Redline Theme

Steven’s black and red theme with Tux/eclipse wallpapers and a terminal color picker. Choose **red, blue, green, yellow, pink, or purple**.

![Redline wallpaper](theme/backgrounds/tux-crimson-eclipse.png)

## Install or change colors

Run in a terminal as your normal user:

```bash
curl -fsSL https://raw.githubusercontent.com/stspivey76-byte/omarchy-redline-desktop/main/download.sh | bash
```

The installer downloads the latest release, verifies its SHA-256 checksum, opens the six-color menu, and backs up affected theme files/settings. Requires Linux, Bash, Python 3.11+, curl, and sha256sum. It does not install packages.

This repository contains **the theme and color picker only**: wallpapers, Omarchy palette and theme styling, GTK 3/4 colors, a KDE color scheme, and theme update/restore helpers. Your existing plugins, taskbar layout, idle settings, terminal configuration, Fastfetch layout, and shell startup files are preserved. Omarchy applies the chosen palette to its normal theme-aware applications and widgets; custom plugins with fixed colors control their own appearance. The theme includes rounded window corners, shadows, borders and spacing on Omarchy.

Want Steven’s plugins, taskbar and terminal setup too? Use [Redline Rice](https://github.com/stspivey76-byte/omarchy-redline-rice).

## Upgrading from the old desktop bundle

Version 2.0.0 separates the theme from the full desktop rice. Run the install command above once to replace the older updater with the theme-only updater. Older updaters expect the old bundle format and cannot migrate automatically.

Existing plugins and taskbar settings from older releases are left in place. This release does not remove them or recover your previous layout automatically. Use your saved backups if you want to restore an earlier layout. The two repositories share Redline theme files and the updater; choose one distribution to manage your installation.

## Desktop support

| Desktop | Theme integration |
| --- | --- |
| Omarchy / Hyprland | Theme palette, wallpaper, GTK colors, window appearance, generated application colors |
| GNOME / Budgie | GTK colors, dark preference, wallpaper |
| KDE Plasma | Qt/KDE color scheme, GTK colors, wallpaper |
| Xfce / Cinnamon / MATE | GTK colors, dark preference, wallpaper |
| LXQt / LXDE | GTK colors and wallpaper through PCManFM; Qt appearance may need manual setup |
| Other desktops | GTK colors and wallpaper files for manual selection |

Native adapters require the desktop’s settings tools and active session services. Missing integrations are reported as notices. Only Omarchy has been visually checked; other adapters have isolated automated coverage. GTK applications may need reopening. Existing custom CSS may override the chosen colors. No icon packs, desktop environments, or terminal profiles are installed.

Preview desktop detection without changes:

```bash
bash install.sh --detect
```

Manual installation: download `redline-desktop.zip` from [Releases](https://github.com/stspivey76-byte/omarchy-redline-desktop/releases/latest), extract it, and run `bash install.sh`. Use `--desktop kde` (or another supported profile) to override detection. Run again to change color.

## Updates and backups

The installer enables hourly release checks and five-minute managed theme-file repairs by default. Updates and repairs retain your selected color. They manage theme assets, GTK imports and updater files; they do not manage taskbar layouts or plugins. Theme repairs can overwrite edits to bundled theme files. To keep personal theme edits, disable repair or automatic updates.

```bash
~/.local/bin/redline-update --status
~/.local/bin/redline-update --check
~/.local/bin/redline-update --updates-only
~/.local/bin/redline-update --disable
```

Install without automatic updates:

```bash
curl -fsSL https://raw.githubusercontent.com/stspivey76-byte/omarchy-redline-desktop/main/download.sh | bash -s -- --no-auto-update
```

Installer backups are stored under `${XDG_STATE_HOME:-~/.local/state}/redline-desktop/backups/`. Each installation prints an exact `python3 /path/to/backup/restore.py` restore command. Updater cache/config live under `${XDG_DATA_HOME:-~/.local/share}/redline-updater/`; logs and snapshots live under `${XDG_STATE_HOME:-~/.local/state}/redline-updater/`.

`redline-uninstall` restores recorded installation backups, newest first, after confirmation. New edits to managed files are replaced. Backups from older full-desktop installations may include plugins, taskbar and Fastfetch; uninstalling that history can restore those older settings too. Keep backups. On Plasma/LXQt/LXDE restore from a text console after logging out; on other desktops restore in the original session and log out/in afterward.

## Validation and attribution

Run `python3 -m unittest discover -s tests -v`. Checks cover desktop adapters, six-color selection, theme-only payloads, preservation of personal plugins/taskbar/terminal/Fastfetch files, backup/restore, updater checksums, offline repair and rollback. Desktop tools are mocked in isolated test homes.

The full rice was separated into its own repository. Historical releases before 2.0.0 still contain the previous desktop bundle. Wallpaper redistribution terms have not been independently established; no new asset license is asserted. See [wallpaper notes](docs/wallpaper-color-prompts.md).
