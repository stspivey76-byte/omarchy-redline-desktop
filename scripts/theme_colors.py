"""Read the flat string-only palette format without external TOML dependencies.

Theme palettes contain named hex colors and a light/dark mode, not general TOML.
Keeping this reader small allows the installer and updater to run on Python 3.8.
"""
import json
from pathlib import Path
import re


def read_colors(path):
    colors = {}
    for number, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r'\s*([a-z_]+)\s*=\s*("[^"\\]*")\s*(?:#.*)?', line)
        if not match:
            raise ValueError("Invalid palette entry at {}:{}".format(path, number))
        key, value = match[1], json.loads(match[2])
        if key in colors or (key == "mode" and value not in ("dark", "light")) or (key != "mode" and not re.fullmatch(r"#[0-9a-fA-F]{6}", value)):
            raise ValueError("Invalid or duplicate palette color: " + key)
        colors[key] = value
    if not {"accent", "background", "foreground"}.issubset(colors):
        raise ValueError("Palette is missing required colors")
    return colors
