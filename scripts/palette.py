"""Color picker and deterministic recoloring of the theme text assets."""
import colorsys
from contextlib import ExitStack
from functools import lru_cache
import os
from pathlib import Path
import re
import shutil
import tomllib

COLORS = {"red": "#d51b36", "blue": "#1b62d5", "green": "#59d51b", "yellow": "#d5af1b", "pink": "#d51b94", "purple": "#891bd5", "halloween": "#ff8c24", "thanksgiving": "#e6a03c", "christmas": "#e5484d"}
COLORS.update({
    'new-year': '#e8c76a',
    'valentines': '#f26b9b',
    'st-patricks': '#58c783',
    'easter': '#c196ed',
    'earth-day': '#70c79b',
    'mothers-day': '#ed91b3',
    'memorial-day': '#7aa8df',
    'fathers-day': '#7daee7',
    'juneteenth': '#e95c67',
    'independence-day': '#eb6473',
    'labor-day': '#e8ad65',
    'veterans-day': '#89acdb',
})
SEASONAL = tuple(COLORS)[6:]
LABELS = {
    'new-year': "New Year's Day",
    'valentines': "Valentine's Day",
    'st-patricks': "St. Patrick's Day",
    'easter': 'Easter',
    'earth-day': 'Earth Day',
    'mothers-day': "Mother's Day",
    'memorial-day': 'Memorial Day',
    'fathers-day': "Father's Day",
    'juneteenth': 'Juneteenth',
    'independence-day': 'Independence Day',
    'labor-day': 'Labor Day',
    'veterans-day': 'Veterans Day',
}
HEX = re.compile(r"#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b")
ANSI = re.compile(r"(38;2;)(\d+);(\d+);(\d+)")
RGB_LINE = re.compile(r"(?m)^(\w+=)(\d+),(\d+),(\d+)$")
PAYLOAD = ("VERSION", "install.sh", "scripts", "theme", "hooks")


@lru_cache(maxsize=4096)
def recolor_rgb(rgb, color):
    if color in SEASONAL:
        root = Path(__file__).resolve().parent.parent / "theme"
        base = tomllib.loads((root / "colors.toml").read_text())
        festive = tomllib.loads((root / "variants" / color / "colors.toml").read_text())
        for key, original in base.items():
            if key == "mode":
                continue
            if tuple(int(original[i:i + 2], 16) for i in (1, 3, 5)) == tuple(rgb):
                return tuple(int(festive[key][i:i + 2], 16) for i in (1, 3, 5))
    _, saturation, value = colorsys.rgb_to_hsv(*(channel / 255 for channel in rgb))
    if saturation < 0.06:
        return tuple(rgb)  # Preserve neutral text, black, white and alpha.
    seed = COLORS[color].lstrip("#")
    hue = colorsys.rgb_to_hsv(*(int(seed[i:i + 2], 16) / 255 for i in (0, 2, 4)))[0]
    return tuple(round(channel * 255) for channel in colorsys.hsv_to_rgb(hue, saturation, value))


def recolor_text(text, color):
    def hex_color(match):
        raw = match.group()[1:]
        alpha, raw = (raw[:2], raw[2:]) if len(raw) == 8 else ("", raw)
        rgb = recolor_rgb(tuple(int(raw[i:i + 2], 16) for i in (0, 2, 4)), color)
        return "#" + alpha + "".join(f"{channel:02x}" for channel in rgb)
    text = HEX.sub(hex_color, text)
    text = ANSI.sub(lambda m: m[1] + ";".join(map(str, recolor_rgb(tuple(map(int, m.group(2, 3, 4))), color))), text)
    return RGB_LINE.sub(lambda m: m[1] + ",".join(map(str, recolor_rgb(tuple(map(int, m.group(2, 3, 4))), color))), text)


def stage(source, destination, color):
    destination.mkdir(parents=True, exist_ok=True)
    for name in PAYLOAD:
        origin = source / name
        if origin.is_dir():
            shutil.copytree(origin, destination / name, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(origin, destination / name)
    for path in destination.rglob("*"):
        if destination / "theme/variants" in path.parents:
            continue
        if path.is_file() and path.suffix in (".toml", ".qml", ".css", ".colors", ".jsonc", ".txt", ".lua"):
            text = recolor_text(path.read_text(), color)
            if color in ("green", "yellow") and path.suffix == ".css":
                text = text.replace("@define-color accent_fg_color #ffffff;", "@define-color accent_fg_color #080406;").replace("--accent-fg-color: #ffffff;", "--accent-fg-color: #080406;")
                text = text.replace("@define-color theme_selected_fg_color #ffffff;", "@define-color theme_selected_fg_color #080406;")
            if color in ("green", "yellow") and path.suffix == ".colors":
                text = re.sub(r"(\[Colors:Selection\][\s\S]*?ForegroundNormal=)[^\n]*", r"\g<1>8,4,6", text)
            path.write_text(text)
    if color in SEASONAL:
        variant = source / "theme/variants" / color
        shutil.copytree(variant, destination / "theme", dirs_exist_ok=True)
    # Stable selected filename keeps existing theme hooks/background paths compatible.
    wallpaper = "tux-crimson-eclipse.png" if color == "red" else f"tux-{color}-eclipse.png"
    shutil.copy2(source / "theme/backgrounds" / wallpaper, destination / "theme/backgrounds/tux-crimson-eclipse.png")
    return destination


def picker(default, desktop, terminal):
    seed = COLORS[default]
    channels = tuple(int(seed[i:i + 2], 16) for i in (1, 3, 5))
    accent = "\033[38;2;" + ";".join(map(str, channels)) + "m"
    reset, bright, dim = "\033[0m", "\033[1;97m", "\033[38;2;145;145;155m"
    tux = [r"      .--.      ", r"     |o_o |     ", r"     |:_/ |     ",
           r"    //   \ \    ", r"   (|     | )   ", r"  /'\_   _/`\   ", r"  \___)=(___/   "]
    eclipse = ["         ·         .-========-.     ✦", "   ✦             .'           `.   ░",
               "                /               \\ ▒", "        ·      |                 |▓█",
               "                \\               / ▓", "    ✦            `.           .'  ▒",
               "             ·     `-=======-'   ░"]
    terminal.write("\n" + accent + "  ╭" + "─" * 62 + "╮\n" + reset)
    terminal.write(accent + "  │" + bright + "R E D L I N E   ·   D E S K T O P".center(62) + accent + "│\n" + reset)
    terminal.write(accent + "  ╰" + "─" * 62 + "╯\n\n" + reset)
    for penguin, moon in zip(tux, eclipse):
        terminal.write("   " + bright + penguin + accent + moon + reset + "\n")
    terminal.write(dim + "\n           Tux. Eclipse. Your color. Your atmosphere.\n" + reset)
    terminal.write(f"  {dim}DESKTOP{reset}  {bright}{desktop}{reset}\n")
    terminal.write(f"  {dim}MATCHES{reset}  wallpaper · theme colors · GTK\n\n")
    entries = []
    for index, (name, rgb) in enumerate(COLORS.items(), 1):
        channels = tuple(int(rgb[i:i + 2], 16) for i in (1, 3, 5))
        swatch = "\033[38;2;" + ";".join(map(str, channels)) + "m●\033[0m"
        selected = name == default
        entries.append(f"{'›' if selected else ' '} {index:>2}  {swatch}  {bright if selected else ''}{LABELS.get(name, name.title()):<20}{reset}" + (accent + "CURRENT" + reset if selected else "       "))
    for entry in entries:
        terminal.write("  " + entry + "\n")
    terminal.write(dim + "  Settings backed up · Updates remember your color\n" + reset)
    while True:
        terminal.write(f"\n  Choose 1–{len(COLORS)} or a color name [Enter: {default}, q: cancel]: ")
        terminal.flush()
        line = terminal.readline()
        if not line:
            raise SystemExit("Installation cancelled (terminal closed).")
        answer = line.strip().lower()
        aliases = {"xmas": "christmas", "valentine": "valentines", "valentines-day": "valentines", "july-4th": "independence-day", "july-4": "independence-day", "4th-of-july": "independence-day", "new-years": "new-year", "st-patricks-day": "st-patricks"}
        normalize = lambda value: re.sub(r"[^a-z0-9]+", "-", value.lower().replace("'", "").replace("’", "")).strip("-")
        labels = {normalize(label): name for name, label in LABELS.items()}
        answer = normalize(answer)
        answer = aliases.get(answer, labels.get(answer, answer))
        if answer in ("q", "quit", "cancel"):
            raise SystemExit("Installation cancelled.")
        if not answer:
            return default
        if answer in COLORS:
            return answer
        if answer in tuple(map(str, range(1, len(COLORS) + 1))):
            return tuple(COLORS)[int(answer) - 1]
        terminal.write("  Please choose a listed number, color, or holiday name.\n")


def choose_color(default, desktop):
    if os.environ.get("REDLINE_UPDATER_RUNNING"):
        saved = os.environ.get("REDLINE_SELECTED_COLOR", default)
        return saved if saved in COLORS else default
    # curl | bash consumes stdin, so use the controlling terminal directly.
    with ExitStack() as stack:
        try:
            reader = stack.enter_context(open("/dev/tty", "r"))
            writer = stack.enter_context(open("/dev/tty", "w", buffering=1))
        except OSError:
            raise SystemExit("Open a terminal and run the installer to choose your color from the menu.")
        class Terminal:
            readline = reader.readline
            write = writer.write
            flush = writer.flush
        return picker(default, desktop, Terminal())
