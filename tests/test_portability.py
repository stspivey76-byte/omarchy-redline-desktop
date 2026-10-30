"""Compatibility checks, downloader fallbacks and desktop backend failures."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from theme_colors import read_colors
from compatibility import distro_name

spec = importlib.util.spec_from_file_location("wallpaper", ROOT / "scripts/apply-wallpaper.py")
wallpaper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wallpaper)


class PortabilityTests(unittest.TestCase):
    def test_check_is_read_only_and_distro_independent(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = dict(os.environ, HOME=tmp, XDG_CONFIG_HOME=tmp + "/config", XDG_DATA_HOME=tmp + "/data", XDG_STATE_HOME=tmp + "/state")
            result = subprocess.run(["bash", str(ROOT / "install.sh"), "--check", "--desktop", "generic"], env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["desktop"], "generic")
            self.assertFalse(report["requires_systemd"])
            self.assertFalse(report["requires_root"])
            self.assertEqual(list(home.iterdir()), [])
            for name in ("Ubuntu", "Debian GNU/Linux", "Fedora Linux", "openSUSE", "Alpine Linux", "Arch Linux"):
                release = home / "os-release"
                release.write_text('PRETTY_NAME=' + json.dumps(name) + '\n')
                self.assertEqual(distro_name(release), name)

    def test_palettes_validate_without_tomllib(self):
        for path in (ROOT / "theme").rglob("colors.toml"):
            self.assertRegex(read_colors(path)["accent"], r"^#[0-9a-f]{6}$")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "colors.toml"
            for contents in ('accent = "red"', 'accent = "#ff0000"\naccent = "#000000"', '[unexpected]\naccent = "#000000"'):
                path.write_text(contents)
                with self.assertRaises(ValueError):
                    read_colors(path)

    def test_wallpaper_backend_failures_are_not_reported_as_success(self):
        with patch.object(wallpaper.shutil, "which", return_value="/bin/tool"), patch.object(wallpaper, "run", return_value='[{"success":false}]'):
            self.assertFalse(wallpaper.apply(Path("/tmp/image.png"), "sway"))
        with patch.object(wallpaper, "run", return_value=None):
            self.assertFalse(wallpaper.apply(Path("/tmp/image.png"), "hyprland"))
            self.assertFalse(wallpaper.apply(Path("/tmp/image.png"), "x11"))

    def test_downloader_supports_curl_wget_and_rejects_bad_payloads(self):
        for backend, broken in (("curl", None), ("wget", None), ("curl", "checksum"), ("wget", "traversal")):
            with self.subTest(backend=backend, broken=broken), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                fixtures = root / "fixtures"
                fixtures.mkdir()
                archive = fixtures / "redline-desktop.zip"
                with zipfile.ZipFile(archive, "w") as zipped:
                    zipped.writestr("redline-desktop/install.sh", 'printf installed > "$REDLINE_TEST_MARKER"\n')
                    if broken == "traversal":
                        zipped.writestr("../escaped", "unsafe")
                digest = "0" * 64 if broken == "checksum" else hashlib.sha256(archive.read_bytes()).hexdigest()
                (fixtures / "SHA256SUMS").write_text(digest + "  redline-desktop.zip\n")
                binary = root / "bin"
                binary.mkdir()
                for command in ("bash", "mktemp", "rm"):
                    (binary / command).symlink_to(shutil.which(command))
                (binary / "python3").symlink_to(sys.executable)
                fetch = binary / backend
                fetch.write_text('#!' + sys.executable + '\nimport os,sys,shutil\nfrom pathlib import Path\na=sys.argv[1:]\nout=a[a.index("-o" if "-o" in a else "-O")+1]\nurl=next(v for v in a if v.startswith("https://"))\nshutil.copy2(Path(os.environ["FIXTURES"])/url.rsplit("/",1)[1],out)\n')
                fetch.chmod(0o755)
                marker = root / "installed"
                env = dict(os.environ, PATH=str(binary), REDLINE_PYTHON=str(binary / "python3"), FIXTURES=str(fixtures), REDLINE_TEST_MARKER=str(marker))
                result = subprocess.run([str(binary / "bash"), str(ROOT / "download.sh")], env=env, text=True, capture_output=True)
                self.assertEqual(result.returncode == 0, broken is None, result.stdout + result.stderr)
                self.assertEqual(marker.exists(), broken is None)
                if broken:
                    self.assertIn("checksum mismatch" if broken == "checksum" else "Unsafe release archive", result.stdout + result.stderr)
                self.assertFalse((root / "escaped").exists())
