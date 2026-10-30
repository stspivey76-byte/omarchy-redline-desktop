#!/usr/bin/env python3
"""Install the bundled Starship prompt, preserving replaced files for restore."""
import argparse
import json
import os
from pathlib import Path
import shutil
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--restore', type=Path, help='Restore a backup directory printed by an earlier install')
args = parser.parse_args()
config = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
if args.restore:
    backup = args.restore.resolve()
    for entry in json.loads((backup / 'manifest.json').read_text()):
        target = config / entry['path']
        if target.is_symlink() or target.is_file():
            target.unlink()
        if entry['existed']:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup / entry['path'], target, follow_symlinks=False)
    print('Terminal settings restored. Open a new terminal window.')
    raise SystemExit
source = Path(__file__).resolve().parents[1] / 'terminal'
state = Path(os.environ.get('XDG_STATE_HOME', str(Path.home() / '.local/state')))
backup = state / 'redline-desktop/terminal-backups' / str(time.time_ns())
backup.mkdir(parents=True)
entries = []
for file in sorted(source.rglob('*')):
    if not file.is_file():
        continue
    relative = file.relative_to(source)
    target = config / relative
    existed = target.exists() or target.is_symlink()
    if existed:
        saved = backup / relative
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, saved, follow_symlinks=False)
    entries.append({'path': str(relative), 'existed': existed})
    (backup / 'manifest.json').write_text(json.dumps(entries, indent=2) + '\n')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        target.unlink()
    shutil.copy2(file, target)
print(f'Starship prompt installed. Backup: {backup}')
print(f'Restore: python3 {Path(__file__).resolve()} --restore {backup}')
print('Open a new terminal window to apply. Requires Starship and a Nerd Font.')
print('Omarchy initializes Starship automatically. Other systems: see https://starship.rs/guide/#step-2-set-up-your-shell-to-use-starship')
print('If STARSHIP_CONFIG is set, point it to the installed starship.toml.')
