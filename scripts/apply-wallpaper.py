#!/usr/bin/env python3
"""Reapply a wallpaper in standalone Sway, Hyprland or X11 sessions.

Desktop environments use their native installer adapters instead. No wallpaper
daemon is started or replaced, and no compositor configuration is rewritten.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def run(*command):
    if not shutil.which(command[0]):
        return None
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        if result.returncode:
            return None
        return result.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return None


def apply(wallpaper, profile):
    if profile == "sway":
        if not shutil.which("swaybg"):
            return False
        result = run("swaymsg", "output * bg " + json.dumps(str(wallpaper)) + " fill")
        try:
            responses = json.loads(result or "null")
            return bool(responses) and all(reply.get("success") for reply in responses)
        except (ValueError, TypeError, AttributeError):
            return False
    if profile == "hyprland":
        if run("swww", "query") is not None:
            return run("swww", "img", str(wallpaper)) is not None
        return False
    if profile == "x11":
        return run("feh", "--no-fehbg", "--bg-fill", str(wallpaper)) is not None
    return False


def main():
    config = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "redline-updater/config.json"
    if not config.exists():
        raise SystemExit("Run the Redline installer first")
    profile = json.loads(config.read_text())["profile"]
    wallpaper = config.parent.parent / "redline-desktop/theme/backgrounds/tux-crimson-eclipse.png"
    if not apply(wallpaper, profile):
        raise SystemExit("Wallpaper could not be applied. Start your wallpaper service or select this image in desktop settings: " + str(wallpaper))


if __name__ == "__main__":
    main()
