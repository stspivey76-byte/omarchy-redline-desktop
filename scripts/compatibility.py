"""Distribution-neutral prerequisites and read-only installation diagnostics."""
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import sys


def distro_name(path=Path("/etc/os-release")):
    values = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                try:
                    values[key] = shlex.split(value)[0]
                except (ValueError, IndexError):
                    pass
    return values.get("PRETTY_NAME", values.get("NAME", "Linux"))


def check(desktop):
    tools = {
        "omarchy": ("omarchy",), "gnome": ("gsettings",), "budgie": ("gsettings",),
        "cinnamon": ("gsettings",), "mate": ("gsettings",),
        "kde": ("plasma-apply-colorscheme", "plasma-apply-wallpaperimage"),
        "xfce": ("xfconf-query",), "lxqt": ("pcmanfm-qt",), "lxde": ("pcmanfm",),
        "sway": ("swaymsg", "swaybg"), "hyprland": ("swww",), "x11": ("feh",),
    }.get(desktop, ())
    result = {
        "distribution": distro_name(), "architecture": platform.machine(),
        "python": platform.python_version(), "desktop": desktop,
        "session_type": os.environ.get("XDG_SESSION_TYPE", "unknown"),
        "tools": {name: shutil.which(name) for name in tools},
        "native_adapter": desktop != "generic",
        "missing_tools": [name for name in tools if not shutil.which(name)],
        "portable_assets": ["wallpapers", "GTK 3/4 colors", "KDE/Qt scheme", "named palette"],
        "configuration": str(Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))),
        "requires_systemd": False, "requires_root": False,
    }
    print(json.dumps(result, indent=2))
    return 0 if sys.version_info >= (3, 8) and sys.platform == "linux" else 1
