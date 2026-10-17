# Redline Desktop

Steven’s red and black desktop theme, crimson Tux wallpapers, custom Fastfetch logo, and Omarchy shell plugins. The installer detects your active desktop and applies the supported settings for that desktop.

![Crimson Tux wallpaper](theme/backgrounds/tux-crimson-eclipse.png)

## Install or update

Run this from a terminal in your normal desktop session, without `sudo`:

```bash
curl -fsSL https://raw.githubusercontent.com/stspivey76-byte/omarchy-redline-desktop/main/download.sh | bash
```

Requires Linux, Bash, Python 3, `curl`, and `sha256sum`. It downloads the latest release ZIP, checks its SHA-256 checksum, backs up affected files/settings, and installs the matching profile. It does not install desktop environments or packages. Fastfetch must already be installed to display the bundled logo and layout.

For a manual install, download [redline-desktop.zip from the latest release](https://github.com/stspivey76-byte/omarchy-redline-desktop/releases/latest), extract it, and run `bash install.sh` inside the extracted `redline-desktop` directory. No Git checkout is needed.

Run the same command again to update. Updates replace the bundled theme, Fastfetch layout, and (on Omarchy) plugins/shell layout. Save custom changes first. Existing GTK CSS rules are preserved after the managed Redline import and can override its colors.

## Desktop detection and support

Detection uses `XDG_CURRENT_DESKTOP`, `XDG_SESSION_DESKTOP`, and `DESKTOP_SESSION`. Omarchy is selected for an active Hyprland session with Omarchy installed. Having Omarchy installed while logged into another desktop does not select its profile.

| Active desktop/profile | Applied automatically |
| --- | --- |
| Omarchy on Hyprland | Full original theme, wallpaper, nine shell plugins, bar layout, idle settings, GTK colors, Fastfetch |
| GNOME / Budgie | GTK colors, dark preference, wallpaper (including GNOME dark variant), Fastfetch |
| KDE Plasma | Native Redline color scheme for Plasma/Qt apps such as Dolphin, wallpaper, GTK colors, Fastfetch |
| Xfce | GTK colors, dark GTK theme, wallpaper for existing monitor/workspace properties, Fastfetch |
| Cinnamon | GTK colors, dark GTK theme, wallpaper, Fastfetch |
| MATE | GTK colors, dark GTK theme, wallpaper, Fastfetch |
| LXQt / LXDE | GTK colors, wallpaper through PCManFM-Qt/PCManFM, Fastfetch |
| Other desktops/window managers | GTK colors, Fastfetch, and persistent wallpaper files; select the wallpaper manually |

This makes the shared assets usable outside Hyprland; it does **not** translate Omarchy plugins into GNOME extensions, Plasma widgets, or other desktop panels. Omarchy’s bar, plugins, lock/idle settings, and shell styling remain specific to Omarchy’s Quickshell shell. Other desktop panels, window decorations, login screens, and icon themes retain their own configuration. LXQt’s Qt widget colors need separate configuration in Appearance settings; its GTK apps receive Redline colors. Unknown desktops receive the shared assets and an explicit notice about manual wallpaper selection.

Native adapters require their desktop’s normal settings tools (`gsettings`, Plasma apply utilities, `xfconf-query`, or the running PCManFM desktop manager). Missing tools, settings, or session services are reported as skipped, rather than silently claiming full application. A profile with notices may need manual steps. Flatpak sandbox permissions are not changed.

To preview detection without changing anything:

```bash
bash install.sh --detect
```

To override detection, for example on KDE:

```bash
bash install.sh --desktop kde
```

Or pass the profile directly to the download command:

```bash
curl -fsSL https://raw.githubusercontent.com/stspivey76-byte/omarchy-redline-desktop/main/download.sh | bash -s -- --desktop kde
```

Profiles: `auto`, `omarchy`, `gnome`, `kde`, `xfce`, `cinnamon`, `mate`, `budgie`, `lxqt`, `lxde`, `generic`. Select the profile for your current session. Generic mode applies only the shared assets and is useful when no native adapter matches your desktop.

## Included

- Redline GTK 3 and GTK 4/libadwaita styling: near-black file views, crimson headers/sidebar, red selections, light text.
- Native `Redline.colors` scheme for KDE Plasma/Qt apps.
- Crimson Tux wallpaper and the original black background.
- Custom Omarchy Eclipse Fastfetch logo and red/orange information layout. Outside Omarchy, its Omarchy-specific probes are replaced with portable Fastfetch modules.
- Omarchy color palette, shell styling, top bar, and idle settings (screensaver at 150 seconds, lock at 300).
- Nine Omarchy plugins: bar, workspaces, active window, clock/calendar, weather, resources, spectrum, updates, and media. The saved Omarchy layout uses the built-in media widget.

For the full Omarchy profile, use a compatible Quickshell-based Omarchy shell/plugin API. Python 3 powers resource meters and update checks. Spectrum needs `pactl` and `parec` (Arch package `libpulse`). Weather uses `curl`, Open-Meteo, and wttr.in. Update checks use installed tools such as `checkupdates`, `yay`, `mise`, `flatpak`, and `fwupdmgr`.

## Backups and restore

On non-Omarchy desktops, the installer respects `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, and `XDG_STATE_HOME`. Shared theme/wallpaper files live under `${XDG_DATA_HOME:-~/.local/share}/redline-desktop/`. The printed backup directory lives under `${XDG_STATE_HOME:-~/.local/state}/redline-desktop/backups/` and contains a restore script plus saved files and native settings. To undo an installation, run the exact command printed by that installation:

```bash
python3 /path/to/printed/backup/restore.py
```

Restore updates in reverse order. For GNOME, Budgie, Cinnamon, MATE, and Xfce, restore in the original desktop session, then log out and back in so cached settings reload. For Plasma, LXQt, and LXDE, log out first and run the restore command from a text console so the desktop cannot overwrite restored configuration; then log back in. Restore replaces affected files with their saved versions, so save any newer edits first.

The Omarchy profile keeps its original backup layout at `~/.local/state/omarchy/backups/redline-desktop-*` (or under `XDG_STATE_HOME`). Restore `shell.json`, `shell.toml`, `themes/redline`, and plugins to `~/.config/omarchy/`; restore `fastfetch/`, `gtk-3.0/`, and `gtk-4.0/` to their respective directories under `~/.config/`. The saved Redline hook, if present, belongs at `~/.config/omarchy/hooks/theme-set.d/redline-gtk`. If a replaced file had no previous version, remove the installed file to undo it. Reapply your previous Omarchy theme. Omarchy itself expects the standard `~/.config` directory.

## GTK styling

Close and reopen GTK apps after installing or changing styling. The imports in `gtk-3.0/gtk.css` and `gtk-4.0/gtk.css` layer Redline colors over the apps’ base styles; existing custom CSS can take precedence. Icons are unchanged.

On Omarchy, a `theme-set` hook enables the imports for Redline and removes them when switching themes. Disable them manually with:

```bash
bash ~/.config/omarchy/hooks/theme-set.d/redline-gtk disabled
```

On other desktops, disable them with:

```bash
bash "${XDG_DATA_HOME:-$HOME/.local/share}/redline-desktop/gtk-style.sh" disabled
```

Reinstall to re-enable, or on a non-Omarchy desktop run:

```bash
bash "${XDG_DATA_HOME:-$HOME/.local/share}/redline-desktop/gtk-style.sh" redline "${XDG_DATA_HOME:-$HOME/.local/share}/redline-desktop/theme"
```

## Validation

GNOME Files 50.3.1 styling was visually verified on Omarchy/Hyprland, including dark views, crimson headers/sidebar, and red selected files. The temporary Files installation and its dependencies were removed afterward.

Desktop detection, native command routing, custom XDG paths, symlink/CSS preservation, repeat installs, and portable restore are tested with isolated homes and mocked desktop tools. Other desktop sessions have **not** been visually tested; automated adapter coverage does not establish identical rendering on every desktop/version.

Run the checks with `python3 -m unittest discover -s tests -v`.

Native settings references: [GNOME background settings](https://help.gnome.org/system-admin-guide/desktop-background.html), [Xfconf CLI](https://docs.xfce.org/xfce/xfconf/xfconf-query), [Plasma color utility](https://github.com/KDE/plasma-workspace/blob/master/kcms/colors/plasma-apply-colorscheme.cpp), [Plasma wallpaper utility](https://github.com/KDE/plasma-workspace/blob/master/wallpapers/image/plasma-apply-wallpaperimage.cpp), and [PCManFM-Qt options](https://github.com/lxqt/pcmanfm-qt/blob/master/pcmanfm/application.cpp).

## Attribution

Several plugins were cloned from Omarchy and retain their original author metadata. Their upstream source is https://github.com/basecamp/omarchy. Existing upstream license terms apply to that code. Wallpaper authorship and redistribution terms have not been established by this export; no new license is asserted for the wallpaper or other included assets. No weather location, credentials, clipboard history, notifications, caches, or old desktop configuration backups are included.
