# Redline Theme

Steven’s black and red theme with Tux/eclipse wallpapers and a terminal color picker. Choose from **six classic colors and 15 holiday themes**, each with a Tux wallpaper and matching desktop colors.

![Redline wallpaper](theme/backgrounds/tux-crimson-eclipse.png)

## Install or change colors

Run in a terminal as your normal user:

```bash
curl -fsSL https://raw.githubusercontent.com/stspivey76-byte/omarchy-redline-desktop/main/download.sh | bash
```

The installer downloads the latest release, verifies its SHA-256 checksum, opens the 21-option menu, and backs up affected theme files/settings. Requires Linux, Bash, and Python 3.8+. The downloader uses curl, wget, or Python HTTPS and verifies SHA-256 with Python; no pip packages, pacman, or systemd are required. It does not install packages.

The main installer contains **the theme and color picker only**: wallpapers, Omarchy palette and theme styling, GTK 3/4 colors, a KDE color scheme, and theme update/restore helpers. Your existing plugins, taskbar layout, idle settings, terminal configuration, Fastfetch layout, and shell startup files are preserved. Omarchy applies the chosen palette to its normal theme-aware applications and widgets; custom plugins with fixed colors control their own appearance. The theme includes rounded window corners, shadows, borders and spacing on Omarchy.

Want Steven’s plugins, taskbar and terminal setup too? Use [Redline Rice](https://github.com/stspivey76-byte/omarchy-redline-rice).

## Optional terminal prompt

Steven’s new Powerline Starship prompt uses an crimson username, muted rose directory, dark rose/black separators, a 24-hour clock, and a second-line command indicator. Its colors stay fixed independently of the desktop color picker.

Install it separately from the theme, using an extracted release ZIP or a clone:

```bash
git clone https://github.com/stspivey76-byte/omarchy-redline-desktop.git
cd omarchy-redline-desktop
python3 scripts/install-terminal.py
```

Requires Starship and a Nerd Font. Omarchy already initializes Starship. On other systems, follow [Starship’s shell setup](https://starship.rs/guide/#step-2-set-up-your-shell-to-use-starship). If you set `STARSHIP_CONFIG`, point it to `~/.config/starship.toml` (or your XDG config path). Open a new terminal afterward.

The prompt installer backs up your previous config and prints a restore command. It does not change terminal emulator settings or shell startup files. The normal theme installer and updater leave your prompt untouched. Restore it separately using the printed command; the theme uninstaller does not restore the optional prompt.

## Upgrading from the old desktop bundle

Version 2.0.0 separates the theme from the full desktop rice. Run the install command above once to replace the older updater with the theme-only updater. Older updaters expect the old bundle format and cannot migrate automatically.

Existing plugins and taskbar settings from older releases are left in place. This release does not remove them or recover your previous layout automatically. Use your saved backups if you want to restore an earlier layout. The two repositories share Redline theme files and the updater; choose one distribution to manage your installation.

## Desktop support

| Desktop | Theme integration |
| --- | --- |
| Omarchy | Theme palette, wallpaper, GTK colors, window appearance, generated application colors |
| GNOME / Budgie | GTK colors, dark preference, wallpaper |
| KDE Plasma | Qt/KDE color scheme, GTK colors, wallpaper |
| Xfce / Cinnamon / MATE | GTK colors, dark preference, wallpaper |
| LXQt / LXDE | GTK colors and wallpaper through PCManFM; Qt appearance may need manual setup |
| Standalone Hyprland | GTK colors, exported palette/Qt scheme, wallpaper through an already running swww daemon |
| Sway | GTK colors, exported palette/Qt scheme, wallpaper through swaymsg + swaybg |
| i3 / bspwm / Openbox / Awesome / Qtile / Fluxbox / IceWM (X11) | GTK colors, exported palette/Qt scheme, wallpaper through feh |
| Other desktops (including COSMIC, Deepin and Enlightenment) | Portable GTK colors, KDE/Qt scheme, palette and wallpaper files; apply native desktop appearance manually |

Native adapters require the desktop’s settings tools and active session services. Missing integrations are reported as notices. Only Omarchy has been visually checked; other adapters have isolated automated coverage. GTK applications may need reopening. Existing custom CSS may override the chosen colors. No icon packs, desktop environments, or terminal profiles are installed.

Preview desktop detection without changes:

```bash
bash install.sh --detect
bash install.sh --check
```

Manual installation: download `redline-desktop.zip` from [Releases](https://github.com/stspivey76-byte/omarchy-redline-desktop/releases/latest), extract it, and run `bash install.sh`. Use `--desktop kde` (or another supported profile) to override detection. Run again to change color.

## Linux distribution compatibility

The same installer runs on Ubuntu, Debian, Linux Mint, Pop!_OS, Fedora, openSUSE, Arch/Manjaro/EndeavourOS, Alpine, and other Linux distributions with Bash and Python 3.8+. It writes to your home directory and uses the active desktop's tools. It requires neither a particular package manager nor systemd; immutable distributions can use the same per-user installation. Install missing prerequisites with your distribution's package manager first.

If curl is unavailable, use wget:

```bash
wget -qO- https://raw.githubusercontent.com/stspivey76-byte/omarchy-redline-desktop/main/download.sh | bash
```

You can also download the release in a browser, extract it, and run `bash install.sh`. If your distribution has several Python versions, use `REDLINE_PYTHON=python3.11 bash install.sh` to choose a compatible interpreter. Python must include its standard SSL and zlib modules.

`bash install.sh --check` is read-only: it prints the distribution, Python version, desktop adapter, missing desktop tools, and configuration directory. Install and change themes as your normal desktop user in an active graphical session.

### What works in each environment

Desktop integration follows the desktop environment, not the distribution: GNOME on Ubuntu and GNOME on Fedora use the same GNOME adapter. The table above distinguishes automatic adapters from portable assets. This does **not** claim identical or automatic appearance on every Linux desktop: GNOME Shell panels, COSMIC/EFL applications, Qt applications that ignore KDE schemes, sandboxed Flatpak/Snap apps, and custom widgets can require separate native setup. No global sandbox permissions are changed.

For unsupported desktops, the installer still exports the selected palette and wallpaper under `${XDG_DATA_HOME:-~/.local/share}/redline-desktop/theme/` and a selectable KDE/Qt scheme under `${XDG_DATA_HOME:-~/.local/share}/color-schemes/Redline.colors`. GTK 3/4 applications load the per-user color overrides. The installer reports any wallpaper or appearance integration it could not apply.

Standalone WMs receive `~/.local/bin/redline-wallpaper`. Add this command to the WM's existing startup configuration if you want its wallpaper reapplied at login (after starting swww in Hyprland). The installer preserves existing WM configs and wallpaper daemons. On restore/uninstall, log out and back in so the original startup configuration restores the prior live wallpaper.

### Validation

The Linux compatibility workflow runs the installer/adapters/updater/restore tests inside Ubuntu 22.04, Debian 12 Bookworm, Fedora 43, openSUSE Tumbleweed, Alpine 3.22 (musl), and Arch containers. These check real distro runtimes; desktop settings services are mocked inside the containers. They do not constitute visual tests of every desktop. The Python 3.8 minimum is also checked locally with an isolated interpreter.

## Updates and backups

When upgrading from v2.4.0 or earlier, rerun the install command once: older updaters reject GitHub’s `v`-prefixed release tag when the bundled VERSION omits that prefix. This release accepts both forms.

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

Run `python3 -m unittest discover -s tests -v`. Checks cover desktop adapters, 21-option selection, theme-only payloads, preservation of personal plugins/taskbar/terminal/Fastfetch files, backup/restore, updater checksums, offline repair and rollback. Desktop tools are mocked in isolated test homes.

The full rice was separated into its own repository. Historical releases before 2.0.0 still contain the previous desktop bundle. Wallpaper redistribution terms have not been independently established; no new asset license is asserted. See [wallpaper notes](docs/wallpaper-color-prompts.md).

### Halloween vibe

Choose **7 — Halloween** (or type `halloween`) in the installer picker for pumpkin-orange accents, deep-purple surfaces, and Tux beside glowing jack-o’-lanterns under an orange eclipse. The updater remembers this choice. The original six colors remain available. Your plugins and taskbar layout are preserved; custom widgets with fixed colors keep their own styling.

![Halloween Tux wallpaper](theme/backgrounds/tux-halloween-eclipse.png)

### Thanksgiving and Christmas vibes

Choose **8 — Thanksgiving** for amber-gold accents, warm brown surfaces, autumn leaves, and Tux beside harvest pumpkins. Choose **9 — Christmas** (or type `xmas`) for festive red accents, evergreen surfaces, snowy mountains, and Tux wearing a Santa hat beside a decorated tree. These choices are remembered by the updater, just like Halloween.

![Thanksgiving Tux wallpaper](theme/backgrounds/tux-thanksgiving-eclipse.png)

![Christmas Tux wallpaper](theme/backgrounds/tux-christmas-eclipse.png)

### More holiday vibes

Every holiday option pairs a dedicated Tux/eclipse wallpaper with matching theme, GTK, KDE, and theme-aware shell colors. Type a listed number or holiday name; names such as `Valentine's Day`, `St. Patrick's Day`, `Mother's Day`, and `July 4th` also work. The updater remembers your selection.

| Option | Holiday | Matching colors |
| --- | --- | --- |
| 10 | [New Year's Day](theme/backgrounds/tux-new-year-eclipse.png) | midnight navy, champagne gold and silver |
| 11 | [Valentine's Day](theme/backgrounds/tux-valentines-eclipse.png) | rose pink, burgundy and lavender |
| 12 | [St. Patrick's Day](theme/backgrounds/tux-st-patricks-eclipse.png) | emerald green, deep forest green and warm gold |
| 13 | [Easter](theme/backgrounds/tux-easter-eclipse.png) | pastel lavender, mint green and soft gold |
| 14 | [Earth Day](theme/backgrounds/tux-earth-day-eclipse.png) | forest green, ocean teal and sky blue |
| 15 | [Mother's Day](theme/backgrounds/tux-mothers-day-eclipse.png) | blush pink, warm ivory and lavender |
| 16 | [Memorial Day](theme/backgrounds/tux-memorial-day-eclipse.png) | solemn navy blue, muted crimson and ivory |
| 17 | [Father's Day](theme/backgrounds/tux-fathers-day-eclipse.png) | denim blue, navy and warm amber |
| 18 | [Juneteenth](theme/backgrounds/tux-juneteenth-eclipse.png) | deep red, rich blue, white and gold |
| 19 | [Independence Day](theme/backgrounds/tux-independence-day-eclipse.png) | red, white and navy blue |
| 20 | [Labor Day](theme/backgrounds/tux-labor-day-eclipse.png) | copper gold, slate blue and warm charcoal |
| 21 | [Veterans Day](theme/backgrounds/tux-veterans-day-eclipse.png) | navy blue, muted gold and ivory |

These popular celebrations expand the original Halloween, Thanksgiving, and Christmas options. The existing menu numbers 1–9 stay the same.
