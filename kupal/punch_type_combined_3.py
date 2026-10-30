import math
import os
import random
import shutil
import sys
import time
from contextlib import contextmanager

import pygame

try:
    from PIL import Image
except ImportError:
    Image = None

ASSET_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_FOLDER = os.path.join(ASSET_DIR, "assets")

# Every image the game uses. Each key lists the accepted file names (first match wins).
# Files are looked up in the "assets" folder next to this script, then next to the script itself.
ASSET_NAMES = {
    "fighter":     ("fighter_icon.png",),
    "glove_none":  ("no_gloves_pair.png", "no_gloves_pair.webp"),
    "glove_red":   ("red_gloves_pair.png", "red_gloves_pair.webp"),
    "glove_black": ("black_gloves_pair.png", "black_gloves_pair.webp"),
    "glove_spiky": ("spiky_gloves_pair.png", "spiky_gloves_pair_1.webp", "spiky_gloves_pair.webp"),
    "boss_idle":   ("enemy_idle.png", "enemy_idle__1_.png", "enemy_idle.webp"),
    "boss_punch":  ("enemy_punch.png", "enemy_punch_1.png", "enemy_punch_1.webp", "enemy_punch.webp"),
    "boss_block":  ("enemy_block.png", "enemy_block__1_.png", "enemy_block.webp"),
    "bg_1":        ("bridge_fp_bg.png", "bridge_fp_bg.webp"),
    "bg_2":        ("subway_fp_bg.png", "subway_fp_bg.webp"),
    "bg_3":        ("ring_fp_bg.png", "ring_fp_bg.webp"),
}

def asset_path(*names):
    for folder in (ASSET_FOLDER, ASSET_DIR):
        for name in names:
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                return path
    return None

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

pygame.init()
pygame.mixer.init()


criit = pygame.mixer.Sound("crit.wav")
chet = pygame.mixer.Sound("cheat.wav")
bg = pygame.mixer.Sound("Energizing Game.wav")
back = pygame.mixer.Sound("back.wav")
bell = pygame.mixer.Sound("bell.wav")
buy = pygame.mixer.Sound("buy.wav")
denied = pygame.mixer.Sound("denied.wav")
hurt = pygame.mixer.Sound("hurt.wav")  
lose = pygame.mixer.Sound("ko_lose.wav")
win = pygame.mixer.Sound("ko_win.wav")
tick = pygame.mixer.Sound("tick.wav")
select = pygame.mixer.Sound("select.wav")
move = pygame.mixer.Sound("move.wav")
punch = pygame.mixer.Sound("punch.wav") 
roar = pygame.mixer.Sound("roar.wav")
ult1 = pygame.mixer.Sound("ult.wav")
ult2 = pygame.mixer.Sound("ult_berserk.wav")
ult3 = pygame.mixer.Sound("ult_bloodlust.wav")
ult4 = pygame.mixer.Sound("ult_lava.wav")
stret= pygame.mixer.Sound("street.mp3")
m1= pygame.mixer.Sound("well timed.wav")
m2= pygame.mixer.Sound("nice.wav")
m3= pygame.mixer.Sound("ayan.wav")
m4= pygame.mixer.Sound("ngawngaw.wav")
m5= pygame.mixer.Sound("aray.wav")
m6= pygame.mixer.Sound("uy bagsak.wav")
m7= pygame.mixer.Sound("unstoppable.wav")
m8= pygame.mixer.Sound("wow.wav")
m9= pygame.mixer.Sound("good job.wav")
m10= pygame.mixer.Sound("whoo.wav")

voiceline={
    "WELL TIMED!": m1,
    "NICE!": m2,
    "AYAAAAAN NAAAA": m3,
    "NGAWNGAW": m4, 
    "ARAYKUPOOOOO": m5,
    "UY BAGSAK!!": m6,
    "UNSTOPPABLE!!!": m7,
    "WOOOOOOW!!!!": m8,
    "GOOD JOB!": m9,
    "WHOOOOOO!!!!": m10
    
}





stret.set_volume(0.10)
bg.set_volume(0.05)







WIDTH = 78
INNER = WIDTH - 2
MENU_HEIGHT = 28
FPS = 30

FONT = {
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "U": ["#   #", "#   #", "#   #", "#   #", " ### "],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    "C": [" ####", "#    ", "#    ", "#    ", " ####"],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #"],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    "E": ["#####", "#    ", "#### ", "#    ", "#####"],
    "A": [" ### ", "#   #", "#####", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", " ### "],
    "K": ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    "W": ["#   #", "#   #", "# # #", "## ##", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "#####"],

    "L": ["#    ", "#    ", "#    ", "#    ", "#####"],
    "S": [" ####", "#    ", " ### ", "    #", "#### "],

    "M": ["#   #", "## ##", "# # #", "#   #", "#   #"],
    "Q": [" ### ", "#   #", "# # #", "#  ##", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#### "],
    "F": ["#####", "#    ", "#### ", "#    ", "#    "],
    " ": ["   ", "   ", "   ", "   ", "   "],
}
TITLE = "PUNCH TYPE"

def block_text(text):
    return [" ".join(FONT[ch][row] for ch in text) for row in range(5)]

PORTRAIT_W = 24
PORTRAIT_ART_ROWS = 11
PBOX_H = PORTRAIT_ART_ROWS + 2
PBOX_PAD = (PBOX_H - 11) // 2

FRAME_IDLE = [
    "     .-\"\"\"\"\"-.      ",
    "    /  ,   ,  \\     ",
    "   |  (o) (o)  |    ",
    "    \\    ^    /     ",
    "     \\  ===  /      ",
    "  (@)==\\_____/==(@)  ",
    "       |  *  |     ",
    "       |     |     ",
    "        |_____|       ",
]
FRAME_GUARD = [
    "     .-\"\"\"\"\"-.      ",
    "    /  ,   ,  \\     ",
    " (@)|  (o) (o)  |(@) ",
    "    \\    ^    /     ",
    "     \\  ===  /      ",
    "      \\_____/      ",
    "       |  *  |      ",
    "       |     |      ",
    "       |_____|       ",
]
FRAME_PUNCH = [
    "     .-\"\"\"\"\"-.      ",
    "    /  ,   ,  \\     ",
    "   |  (>) (<)  |    ",
    "    \\    O    /     ",
    "     \\  ===  /      ",
    "  (@)=\\_____/=====(@)",
    "       |  *  |      ",
    "       |     |      ",
    "       |_____|       ",
]

def portrait_art_text(t=0.0, punching=False):
    if punching or 5.0 <= (t % 6.0) < 5.3:
        frame = FRAME_PUNCH
    else:
        frame = FRAME_IDLE if int(t * 2) % 2 == 0 else FRAME_GUARD
        if (t % 3.2) < 0.15:
            frame = [l.replace("(o) (o)", "(-) (-)") for l in frame]
    return [l.center(PORTRAIT_W)[:PORTRAIT_W] for l in frame]

def portrait_box_text(title="FIGHTER", art=None):
    art = art or portrait_art_text()
    top = "+" + f" {title} ".center(PORTRAIT_W, "-") + "+"
    return [top, *["|" + l + "|" for l in art], "+" + "-" * PORTRAIT_W + "+"]

# ---------------------------------------------------------------- pixel-art images (Pillow)
_image_cache = {}

def load_image(key):
    """Open one of the game's images as RGBA. Returns None when Pillow or the file is missing."""
    if Image is None:
        return None
    if key not in _image_cache:
        path = asset_path(*ASSET_NAMES.get(key, ()))
        try:
            _image_cache[key] = Image.open(path).convert("RGBA") if path else None
        except Exception:
            _image_cache[key] = None
    return _image_cache[key]

def solid_bbox(im):
    return im.getchannel("A").point(lambda a: 255 if a >= 128 else 0).getbbox()

def image_pixels(im, th, tw=None):
    """RGBA image -> rows of (r, g, b) or None (transparent). th = pixel rows (2 per terminal row).
    Nearest-neighbour keeps pixel art crisp; when shrinking by more than 2x it switches to box
    averaging, because dropping most pixels would erase the details."""
    sw, sh = im.size
    if tw is None:
        tw = max(1, round(sw * th / sh))
    if (tw, th) != (sw, sh):
        method = Image.NEAREST if (th * 2 >= sh and tw * 2 >= sw) else Image.BOX
        im = im.resize((tw, th), method)
    data = list(im.getdata())
    return [[(p[0], p[1], p[2]) if p[3] >= 128 else None for p in data[y * tw:(y + 1) * tw]]
            for y in range(th)]

def fit_pixels(im, max_cols, max_rows):
    sw, sh = im.size
    th = max_rows * 2
    tw = max(1, round(sw * th / sh))
    if tw > max_cols:
        tw = max_cols
        th = max(2, int(sh * tw / sw) // 2 * 2)
    return image_pixels(im, th, tw)

def pixels_to_parts(pixels):
    """Pixel grid -> terminal rows of (text, ansi style) runs using half blocks.
    Transparent pixels stay unstyled so the terminal background shows through."""
    rows = []
    for r in range(0, len(pixels), 2):
        top_row = pixels[r]
        bottom_row = pixels[r + 1] if r + 1 < len(pixels) else [None] * len(top_row)
        runs = []
        for a, b in zip(top_row, bottom_row):
            if a is None and b is None:
                ch, style = " ", ""
            elif a == b:
                ch, style = "\u2588", px_fg(a)
            elif a is not None and b is not None:
                ch, style = "\u2580", px_fg(a) + px_bg(b)
            elif a is not None:
                ch, style = "\u2580", px_fg(a)
            else:
                ch, style = "\u2584", px_fg(b)
            if runs and runs[-1][1] == style:
                runs[-1] = (runs[-1][0] + ch, style)
            else:
                runs.append((ch, style))
        rows.append(runs)
    return rows

# ---- player fighter portrait (fighter_icon.png, 32x32) -----------------------------------
FIGHTER_CROP = (4, 0, 28, 22)          # head + shoulders, shown 1:1 (24x22 px = 24 cols x 11 rows)
_SKIN_SHADE = (180, 120, 86, 255)
_INK = (44, 32, 28, 255)

def fighter_pixels(t=0.0, punching=False, mood="idle"):
    src = load_image("fighter")
    if src is None:
        return None
    im = src.copy()
    px = im.load()
    if mood == "ko":                                   # X eyes
        for cx in (13, 18):
            for dx, dy in ((-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)):
                px[cx + dx, 12 + dy] = _INK
    elif mood == "angry":                              # heavy brows over the eyes
        for x in (12, 13, 18, 19):
            px[x, 11] = _INK
    elif (t % 3.2) < 0.15:                             # blink
        for x in (12, 13, 18, 19):
            px[x, 12] = _SKIN_SHADE
    dx, off = 0, 0
    if mood == "ko":
        dx = int(t * 2) % 2
    elif punching:
        dx, off = 1, 1
    else:
        off = int(t * 2) % 2                           # gentle breathing bob
    x0, y0, x1, y1 = FIGHTER_CROP
    pixels = image_pixels(im.crop((x0 + dx, y0 + off, x1 + dx, y1 + off)), y1 - y0, x1 - x0)
    tint = None
    if mood == "ko":
        tint = ((120, 120, 130), 0.35)
    elif punching:
        tint = ((255, 255, 255), 0.25)
    if tint:
        pixels = [[tint_color(p, *tint) if p is not None else None for p in row] for row in pixels]
    return pixels

def portrait_art(t=0.0, punching=False, mood="idle"):
    """Rows for the portrait box: pixel-art runs when the image is available, ASCII otherwise."""
    pixels = fighter_pixels(t, punching, mood)
    if pixels is not None:
        return pixels_to_parts(pixels)
    if mood == "ko":
        art = _defeat_art(t)
    else:
        art = portrait_art_text(t, punching)
        if mood == "angry":
            art = [l.replace("(o) (o)", "(>) (<)").replace("(-) (-)", "(>) (<)") for l in art]
    return [" " * PORTRAIT_W] + art + [" " * PORTRAIT_W] * (PORTRAIT_ART_ROWS - len(art) - 1)

def portrait_box(title="FIGHTER", art=None, edge=None, ink=None):
    """Framed portrait as rows of (text, style) parts, PBOX_H rows tall and PORTRAIT_W + 2 wide."""
    edge = edge or c(45)
    ink = ink or c(252)
    art = art if art is not None else portrait_art()
    rows = [[("+" + f" {title} ".center(PORTRAIT_W, "-") + "+", edge)]]
    for row in art:
        if isinstance(row, str):
            row = [(row.ljust(PORTRAIT_W)[:PORTRAIT_W], ink)]
        rows.append([("|", edge)] + row + [("|", edge)])
    rows.append([("+" + "-" * PORTRAIT_W + "+", edge)])
    return rows

BUTTONS = [("1", "START"), ("2", "SHOP"), ("3", "EXIT")]
BUTTON_W = 19

def button_text(index, kind):
    num, name = BUTTONS[index]
    if kind == 1:
        return "|" + f"{num}  [ {name:^7} ]".center(BUTTON_W) + "|"
    return "+" + "=" * BUTTON_W + "+"

def draw_main_menu(gold=0):
    def row(text=""):
        return "|" + text.ljust(INNER)[:INNER] + "|"

    border = "+" + "=" * INNER + "+"
    stars = "*" * INNER

    lines = [border, row(f"  GOLD: {gold} [o]"), row()]
    lines += [row(l.center(INNER)) for l in block_text(TITLE)]
    lines += [row(), row(stars), row()]

    buttons = []
    for i in range(len(BUTTONS)):
        buttons += [button_text(i, 0), button_text(i, 1), button_text(i, 2)]
        if i < len(BUTTONS) - 1:
            buttons.append("")
    portrait = portrait_box_text()

    right_margin = 4
    left_w = INNER - PORTRAIT_W - 2 - right_margin
    for b, p in zip(buttons, portrait):
        lines.append(row(b.center(left_w) + p.ljust(PORTRAIT_W + 2) + " " * right_margin))

    lines += [row(), row(stars), row("Type 1, 2 or 3 and press ENTER".center(INNER)), border]
    return "\n".join(lines)

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
HOME = "\x1b[H"
CLEAR = "\x1b[2J"
CLEAR_EOL = "\x1b[K"
CLEAR_DOWN = "\x1b[J"

FIRE = [196, 202, 208, 214, 220, 226, 220, 214, 208, 202]

def c(n):
    return f"\x1b[38;5;{n}m"

def enable_ansi_on_windows():
    if os.name != "nt":
        return
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        handle = k32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if k32.GetConsoleMode(handle, ctypes.byref(mode)):
            k32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        os.system("")

def _normalize(ch):
    ch = ch.lower()
    if ch.isdigit():
        return ch
    return {"w": "up", "s": "down", "\r": "enter", "\n": "enter",
            "q": "quit", "\x03": "quit", "\x04": "quit"}.get(ch, "")

if os.name == "nt":
    import msvcrt

    @contextmanager
    def raw_input_mode():
        yield

    def poll_key():
        if not msvcrt.kbhit():
            return ""
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            return {"H": "up", "P": "down"}.get(msvcrt.getwch(), "")
        if ch == "\x1b":
            return "quit"
        return _normalize(ch)

    def read_key():
        if not msvcrt.kbhit():
            return ""
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            msvcrt.getwch()
            return ""
        return ch.upper()

    def flush_keys():
        while msvcrt.kbhit():
            msvcrt.getwch()

else:
    import select
    import termios
    import tty

    @contextmanager
    def raw_input_mode():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            yield
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def _ready():
        return bool(select.select([sys.stdin], [], [], 0)[0])

    def poll_key():
        if not _ready():
            return ""
        ch = os.read(sys.stdin.fileno(), 1).decode(errors="ignore")
        if ch == "\x1b":
            seq = ""
            time.sleep(0.01)
            while _ready() and len(seq) < 2:
                seq += os.read(sys.stdin.fileno(), 1).decode(errors="ignore")
            if not seq:
                return "quit"
            return {"[A": "up", "[B": "down"}.get(seq, "")
        return _normalize(ch)

    def read_key():
        if not select.select([sys.stdin], [], [], 0)[0]:
            return ""
        data = os.read(sys.stdin.fileno(), 32).decode(errors="ignore")
        if not data or data[0] == "\x1b":
            return ""
        return data[0].upper()

    def flush_keys():
        try:
            termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
        except Exception:
            pass

EDGE = c(208) + "|" + RESET

_last_size = None

def _sync_size():
    global WIDTH, INNER
    size = shutil.get_terminal_size((80, 28))
    WIDTH = max(78, size.columns)
    INNER = WIDTH - 2
    return size

def _too_small(out, min_rows=None):
    global _last_size
    size = shutil.get_terminal_size((80, 28))
    if size != _last_size:
        _last_size = size
        out.write(CLEAR)
    need = min_rows or MENU_HEIGHT + 2
    if size.columns >= 80 and size.lines >= need:
        return False
    out.write(HOME + f"TERMINAL TOO SMALL: NEED 80x{need}, YOU HAVE "
              f"{size.columns}x{size.lines}. ENLARGE THE WINDOW." + CLEAR_EOL)
    out.flush()
    time.sleep(0.2)
    return True

def _plain_len(parts):
    return sum(len(text) for text, _ in parts)

def _fit(parts, width):
    extra = width - _plain_len(parts)
    return parts + [(" " * extra, "")] if extra > 0 else parts

def _paint(parts):
    return "".join(f"{style}{text}{RESET}" if style and text else text for text, style in parts)

def _row(parts):
    return EDGE + _paint(_fit(parts, INNER)) + EDGE

def _render(t, intro, sel, shown_gold, flash, punching):
    def visible(start):
        return (not intro) or t >= start

    size = _sync_size()
    lines = [c(208) + "+" + "=" * INNER + "+" + RESET]

    coin = ["[o]", "[O]", "[0]", "[O]"][int(t * 5) % 4]
    lines.append(_row([("  GOLD: ", c(220) + BOLD), (str(int(shown_gold)), c(226) + BOLD),
                       (" ", ""), (coin, c(220) + BOLD)]))
    lines.append(_row([]))

    rows = block_text(TITLE)
    tw = len(rows[0])
    reveal = tw if not intro else min(tw, int(t / 0.9 * tw))
    pad = (INNER - tw) // 2
    for r, text in enumerate(rows):
        parts = [(" " * pad, "")]
        for i, ch in enumerate(text):
            if ch == "#" and i < reveal:
                shade = FIRE[(i // 2 + r - int(t * 12)) % len(FIRE)]
                parts.append(("#", c(shade) + BOLD))
            else:
                parts.append((" ", ""))
        lines.append(_row(parts))

    title_end = len(lines)

    def stars():
        shift = int(t * 10)
        return _row([("*", c(220) + BOLD) if (i + shift) % 4 == 0 else (".", c(240))
                     for i in range(INNER)])

    lines += [_row([]), stars(), _row([])]

    left_w = min(INNER - PORTRAIT_W - 2 - 4, 46)
    lead = max(0, (INNER - left_w - PORTRAIT_W - 2) // 2)
    right_margin = max(0, INNER - lead - left_w - PORTRAIT_W - 2)
    box_left = (left_w - (BUTTON_W + 2)) // 2
    pulse = int(t * 3) % 2
    portrait = portrait_box(art=portrait_art(t, punching))

    for k in range(PBOX_H):
        kk = k - PBOX_PAD
        j, kind = divmod(kk, 4)
        if not 0 <= kk <= 10 or kind == 3 or not visible(1.0 + 0.15 * j):
            left = []
        else:
            text = button_text(j, kind)
            active = j == sel
            style = (c(15) + BOLD if flash else c(226) + BOLD) if active else c(245)
            if active and kind == 1:
                a = box_left - 4 + pulse
                arrow = c(196) + BOLD
                left = [(" " * a, ""), (">>", arrow), (" " * (2 - pulse), ""),
                        (text, style), (" " * (2 - pulse), ""), ("<<", arrow)]
            else:
                left = [(" " * box_left, ""), (text, style)]
        left = _fit(left, left_w)

        if visible(1.5):
            right = portrait[k]
        else:
            right = [(" " * (PORTRAIT_W + 2), "")]
        lines.append(_row([(" " * lead, "")] + left + right + [(" " * right_margin, "")]))

    mid_end = len(lines)
    lines += [_row([]), stars()]
    hint = "W/S or UP/DOWN to move   ENTER to select   or press 1 2 3"
    lines.append(_row([(" " * ((INNER - len(hint)) // 2), ""), (hint, c(245))]))
    lines.append(c(208) + "+" + "=" * INNER + "+" + RESET)

    extra = size.lines - 1 - len(lines)
    if extra > 0:
        blank = _row([])
        gap_top = extra // 4
        gap_title = extra // 4
        gap_mid = extra - gap_top - gap_title
        lines = (lines[:3] + [blank] * gap_top + lines[3:title_end] + [blank] * gap_title
                 + lines[title_end:mid_end] + [blank] * gap_mid + lines[mid_end:])

    return HOME + "".join(l + CLEAR_EOL + "\n" for l in lines)

_intro_done = False
_shown_gold = 0.0
_note_shown = False

_reason = ""

def _can_animate():
    global _reason, WIDTH, INNER
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        _reason = ("this is not a real terminal (IDLE, Thonny, an IDE 'Run' panel or piped "
                   "input can't redraw the screen). Open Command Prompt / PowerShell / "
                   "Windows Terminal and run:  python punch_type_combined.py")
        return False

    size = shutil.get_terminal_size((80, 28))
    if size.columns < 80 or size.lines < MENU_HEIGHT + 2:
        _reason = (f"your terminal is {size.columns}x{size.lines}; the animated menu needs "
                   f"at least 80x{MENU_HEIGHT + 2}. Maximize the terminal or reduce its font size, then restart.")
        return False

    WIDTH = max(78, size.columns)
    INNER = WIDTH - 2
    return True

def _static_menu(gold):
    global _note_shown
    print(draw_main_menu(gold))
    if not _note_shown:
        _note_shown = True
        print(f"(Animation is off: {_reason})")
    try:
        return int(input("ENTER CHOICE: "))
    except ValueError:
        return 0
    except EOFError:
        return 3

def run_main_menu(gold=0):
    bg.stop()
    bg.play()
    global _intro_done, _shown_gold
    enable_ansi_on_windows()
    if not _can_animate():
        return _static_menu(gold)

    intro = not _intro_done
    shown = float(gold) if _shown_gold > gold else _shown_gold
    rate = max(1.0, (gold - shown) / 0.8)
    sel, typed, result = 0, "", 3
    out = sys.stdout
    out.write(HIDE_CURSOR + CLEAR)
    out.flush()
    t0 = last = time.monotonic()
    try:
        with raw_input_mode():
            while True:
                now = time.monotonic()
                dt, last, t = now - last, now, now - t0
                if _too_small(out):
                    continue
                key = poll_key()

                if key == "up":
                    move.play()
                    sel, typed = (sel - 1) % len(BUTTONS), ""
                    
                elif key == "down":
                    move.play()
                    sel, typed = (sel + 1) % len(BUTTONS), ""
                   
                elif key.isdigit():
                
                    typed = (typed + key)[-3:]
                    if key in "123":
                        move.play()
                        sel = int(key) - 1

                elif key == "quit":
                    move.play()
                    result = 3
                    break
                elif key == "enter":
                    select.play()
                    result = 110 if typed.endswith("110") else sel + 1
                    for i in range(8):
                        out.write(_render(t + i * 0.05, intro, sel, shown, i % 2 == 0, True))
                        out.flush()
                        time.sleep(0.05)
                    break

                if shown < gold:
                    shown = min(float(gold), shown + rate * dt)
                out.write(_render(t, intro, sel, shown, False, False))
                out.flush()

                spare = 1.0 / FPS - (time.monotonic() - now)
                if spare > 0:
                    time.sleep(spare)
    except KeyboardInterrupt:
        result = 3
    finally:
        _intro_done = True
        _shown_gold = float(gold)
        out.write(RESET + SHOW_CURSOR + CLEAR + HOME)
        out.flush()
    return result

def _render_exit(t, punching):
    size = _sync_size()
    lines = [c(208) + "+" + "=" * INNER + "+" + RESET, _row([]), _row([])]

    rows = block_text("THANK YOU")
    tw = len(rows[0])
    reveal = min(tw, int(t / 0.7 * tw))
    pad = (INNER - tw) // 2
    for r, text in enumerate(rows):
        parts = [(" " * pad, "")]
        for i, ch in enumerate(text):
            if ch == "#" and i < reveal:
                shade = FIRE[(i // 2 + r - int(t * 12)) % len(FIRE)]
                parts.append(("#", c(shade) + BOLD))
            else:
                parts.append((" ", ""))
        lines.append(_row(parts))

    title_end = len(lines)

    def stars():
        shift = int(t * 10)
        return _row([("*", c(220) + BOLD) if (i + shift) % 4 == 0 else (".", c(240))
                     for i in range(INNER)])

    lines += [_row([]), stars(), _row([])]

    left_w = min(INNER - PORTRAIT_W - 2 - 4, 46)
    lead = max(0, (INNER - left_w - PORTRAIT_W - 2) // 2)
    right_margin = max(0, INNER - lead - left_w - PORTRAIT_W - 2)
    box_left = (left_w - (BUTTON_W + 2)) // 2
    pulse = int(t * 3) % 2
    portrait = portrait_box(art=portrait_art(t, punching))
    texts = {1: ("FOR PLAYING!", c(15) + BOLD),
             3: ("SEE YOU NEXT TIME,", c(250)),
             4: ("FIGHTER!", c(226) + BOLD)}

    for k in range(PBOX_H):
        kk = k - PBOX_PAD
        left = []
        if kk in texts:
            text, style = texts[kk]
            left = [(" " * ((left_w - len(text)) // 2), ""), (text, style)]
        elif 6 <= kk <= 8:
            kind = kk - 6
            if kind == 1:
                text = "|" + "PRESS ENTER".center(BUTTON_W) + "|"
            else:
                text = "+" + "=" * BUTTON_W + "+"
            style = c(226) + BOLD
            if kind == 1:
                a = box_left - 4 + pulse
                arrow = c(196) + BOLD
                left = [(" " * a, ""), (">>", arrow), (" " * (2 - pulse), ""),
                        (text, style), (" " * (2 - pulse), ""), ("<<", arrow)]
            else:
                left = [(" " * box_left, ""), (text, style)]
        left = _fit(left, left_w)

        right = portrait[k]
        lines.append(_row([(" " * lead, "")] + left + right + [(" " * right_margin, "")]))

    mid_end = len(lines)
    lines += [_row([]), stars()]
    hint = "THANK YOU FOR PLAYING!   PRESS ENTER TO EXIT"
    lines.append(_row([(" " * ((INNER - len(hint)) // 2), ""), (hint, c(245))]))
    lines.append(c(208) + "+" + "=" * INNER + "+" + RESET)

    extra = size.lines - 1 - len(lines)
    if extra > 0:
        blank = _row([])
        gap_top = extra // 4
        gap_title = extra // 4
        gap_mid = extra - gap_top - gap_title
        lines = (lines[:3] + [blank] * gap_top + lines[3:title_end] + [blank] * gap_title
                 + lines[title_end:mid_end] + [blank] * gap_mid + lines[mid_end:])

    return HOME + "".join(l + CLEAR_EOL + "\n" for l in lines)

VICTORY_BUTTONS = [("1", "RETRY"), ("2", "MENU"), ("3", "EXIT")]

def _victory_button(index, kind):
    num, name = VICTORY_BUTTONS[index]
    if kind == 1:
        return "|" + f"{num}  [ {name:^7} ]".center(BUTTON_W) + "|"
    return "+" + "=" * BUTTON_W + "+"

def _render_victory(t, sel, flash, punching, info):
    size = _sync_size()
    lines = [c(208) + "+" + "=" * INNER + "+" + RESET]

    grow = min(1.0, max(0.0, (t - 0.8) / 1.0))
    shown_gold = info["gold"] - info["earned"] + int(info["earned"] * grow)
    coin = ["[o]", "[O]", "[0]", "[O]"][int(t * 5) % 4]
    lines.append(_row([("  GOLD: ", c(220) + BOLD), (str(shown_gold), c(226) + BOLD),
                       (" ", ""), (coin, c(220) + BOLD)]))

    rows = block_text("YOU WIN")
    tw = len(rows[0])
    reveal = min(tw, int(t / 0.7 * tw))
    pad = (INNER - tw) // 2
    for r, text in enumerate(rows):
        parts = [(" " * pad, "")]
        for i, ch in enumerate(text):
            if ch == "#" and i < reveal:
                shade = FIRE[(i // 2 + r - int(t * 12)) % len(FIRE)]
                parts.append(("#", c(shade) + BOLD))
            else:
                parts.append((" ", ""))
        lines.append(_row(parts))
    title_end = len(lines)

    def stars():
        shift = int(t * 10)
        return _row([("*", c(220) + BOLD) if (i + shift) % 4 == 0 else (".", c(240))
                     for i in range(INNER)])

    note = info["note"]
    if note and t >= 1.0:
        style = c(FIRE[int(t * 8) % len(FIRE)]) + BOLD
        lines.append(_row([(" " * ((INNER - len(note)) // 2), ""), (note, style)]))
    else:
        lines.append(_row([]))
    lines.append(stars())

    count = min(1.0, max(0.0, (t - 1.0) / 0.8))
    stats = [("HITS GIVEN", info["phit"], 46), ("HITS TAKEN", info["ehit"], 196),
             ("CRITICAL HITS", info["crits"], 208), ("GOLD EARNED", info["earned"], 226)]
    cell = INNER // 4
    label_parts = []
    value_parts = []
    for i, (label, value, color) in enumerate(stats):
        width = cell if i < 3 else INNER - 3 * cell
        text = str(int(value * count))
        if label == "GOLD EARNED":
            text = "+" + text + " G"
        label_parts.append((label.center(width), c(250)))
        value_parts.append((text.center(width), c(color) + BOLD))
    lines.append(_row(label_parts))
    lines.append(_row(value_parts))
    lines.append(stars())

    left_w = min(INNER - PORTRAIT_W - 2 - 4, 46)
    lead = max(0, (INNER - left_w - PORTRAIT_W - 2) // 2)
    right_margin = max(0, INNER - lead - left_w - PORTRAIT_W - 2)
    box_left = (left_w - (BUTTON_W + 2)) // 2
    pulse = int(t * 3) % 2
    portrait = portrait_box(title="WINNER", art=portrait_art(t, punching))

    for k in range(PBOX_H):
        kk = k - PBOX_PAD
        j, kind = divmod(kk, 4)
        if not 0 <= kk <= 10 or kind == 3 or t < 1.0 + 0.15 * j:
            left = []
        else:
            text = _victory_button(j, kind)
            active = j == sel
            style = (c(15) + BOLD if flash else c(226) + BOLD) if active else c(245)
            if active and kind == 1:
                a = box_left - 4 + pulse
                arrow = c(196) + BOLD
                left = [(" " * a, ""), (">>", arrow), (" " * (2 - pulse), ""),
                        (text, style), (" " * (2 - pulse), ""), ("<<", arrow)]
            else:
                left = [(" " * box_left, ""), (text, style)]
        left = _fit(left, left_w)

        if t >= 1.2:
            right = portrait[k]
        else:
            right = [(" " * (PORTRAIT_W + 2), "")]
        lines.append(_row([(" " * lead, "")] + left + right + [(" " * right_margin, "")]))
    mid_end = len(lines)

    lines += [_row([]), stars()]
    hint = "W/S or UP/DOWN to move   ENTER to select   or press 1 2 3"
    lines.append(_row([(" " * ((INNER - len(hint)) // 2), ""), (hint, c(245))]))
    lines.append(c(208) + "+" + "=" * INNER + "+" + RESET)

    extra = size.lines - 1 - len(lines)
    if extra > 0:
        blank = _row([])
        gap_top = extra // 4
        gap_title = extra // 4
        gap_mid = extra - gap_top - gap_title
        lines = (lines[:2] + [blank] * gap_top + lines[2:title_end] + [blank] * gap_title
                 + lines[title_end:mid_end] + [blank] * gap_mid + lines[mid_end:])

    return HOME + "".join(l + CLEAR_EOL + "\n" for l in lines)

def run_victory_screen(gold, earned, phit, ehit, crits, note=""):
    stret.stop()
    win.play()
    bg.play()
    
    enable_ansi_on_windows()
    if not _can_animate():
        return None
    info = {"gold": gold, "earned": earned, "phit": phit, "ehit": ehit,
            "crits": crits, "note": note}
    sel, result = 0, 3
    out = sys.stdout
    out.write(HIDE_CURSOR + CLEAR)
    out.flush()
    t0 = time.monotonic()
    try:
        with raw_input_mode():
            while True:
                now = time.monotonic()
                t = now - t0
                if _too_small(out):
                    continue
                key = poll_key()

                if key == "up":
                    sel = (sel - 1) % len(VICTORY_BUTTONS)
                    move.play()
                elif key == "down":
                    move.play()
                    sel = (sel + 1) % len(VICTORY_BUTTONS)
                elif key in ("1", "2", "3"):
                    move.play()
                    sel = int(key) - 1
                elif key == "quit":
                    move.play()
                    result = 3
                    break
                elif key == "enter":
                    select.play()
                    result = sel + 1
                    for i in range(8):
                        out.write(_render_victory(t + i * 0.05, sel, i % 2 == 0, True, info))
                        out.flush()
                        time.sleep(0.05)
                    break

                out.write(_render_victory(t, sel, False, False, info))
                out.flush()

                spare = 1.0 / FPS - (time.monotonic() - now)
                if spare > 0:
                    time.sleep(spare)
    except KeyboardInterrupt:
        result = 3
    finally:
        out.write(RESET + SHOW_CURSOR + CLEAR + HOME)
        out.flush()
    return result

DEFEAT_BUTTONS = [("1", "RETRY"), ("2", "MENU")]
DEFEAT_RED = [196, 160, 124, 160]

def _defeat_button(index, kind):
    num, name = DEFEAT_BUTTONS[index]
    if kind == 1:
        return "|" + f"{num}  [ {name:^7} ]".center(BUTTON_W) + "|"
    return "+" + "=" * BUTTON_W + "+"

def _defeat_art(t):
    art = [l.replace("(o) (o)", "(x) (x)").replace("(>) (<)", "(x) (x)") for l in FRAME_IDLE]
    art[3] = art[3].replace("^", "~")
    art[5] = art[5].replace("(@)==", "(@)  ").replace("==(@)", "  (@)")
    if int(t * 2) % 2 == 1:
        art = [" " + l[:-1] for l in art]
    return [l.ljust(PORTRAIT_W)[:PORTRAIT_W] for l in art]

def _render_defeat(t, sel, flash, info):
    size = _sync_size()
    lines = [c(196) + "+" + "=" * INNER + "+" + RESET]

    coin = ["[o]", "[O]", "[0]", "[O]"][int(t * 5) % 4]
    lines.append(_row([("  GOLD: ", c(220) + BOLD), (str(info["gold"]), c(226) + BOLD),
                       (" ", ""), (coin, c(220) + BOLD)]))

    rows = block_text("YOU LOSE")
    tw = len(rows[0])
    reveal = min(tw, int(t / 0.7 * tw))
    pad = (INNER - tw) // 2
    for r, text in enumerate(rows):
        parts = [(" " * pad, "")]
        for i, ch in enumerate(text):
            if ch == "#" and i < reveal:
                shade = DEFEAT_RED[(i // 2 + r - int(t * 6)) % len(DEFEAT_RED)]
                parts.append(("#", c(shade) + BOLD))
            else:
                parts.append((" ", ""))
        lines.append(_row(parts))
    title_end = len(lines)

    def dots():
        shift = int(t * 6)
        return _row([("x", c(196) + BOLD) if (i + shift) % 6 == 0 else (".", c(238))
                     for i in range(INNER)])

    msg = "DON'T GIVE UP, FIGHTER!"
    if t >= 1.0:
        lines.append(_row([(" " * ((INNER - len(msg)) // 2), ""), (msg, c(250) + BOLD)]))
    else:
        lines.append(_row([]))
    lines.append(dots())

    count = min(1.0, max(0.0, (t - 1.0) / 0.8))
    stats = [("HITS GIVEN", info["phit"], 46), ("HITS TAKEN", info["ehit"], 196),
             ("CRITICAL HITS", info["crits"], 208), ("GOLD EARNED", info["earned"], 226)]
    cell = INNER // 4
    label_parts = []
    value_parts = []
    for i, (label, value, color) in enumerate(stats):
        width = cell if i < 3 else INNER - 3 * cell
        text = str(int(value * count))
        if label == "GOLD EARNED":
            text = "+" + text + " G"
        label_parts.append((label.center(width), c(250)))
        value_parts.append((text.center(width), c(color) + BOLD))
    lines.append(_row(label_parts))
    lines.append(_row(value_parts))
    lines.append(dots())

    left_w = min(INNER - PORTRAIT_W - 2 - 4, 46)
    lead = max(0, (INNER - left_w - PORTRAIT_W - 2) // 2)
    right_margin = max(0, INNER - lead - left_w - PORTRAIT_W - 2)
    box_left = (left_w - (BUTTON_W + 2)) // 2
    pulse = int(t * 3) % 2
    portrait = portrait_box(title="KNOCKED OUT", art=portrait_art(t, mood="ko"), edge=c(196), ink=c(250))

    for k in range(PBOX_H):
        kk = k - PBOX_PAD
        j, kind = divmod(kk, 4)
        if not 0 <= kk <= 10 or kind == 3 or j >= len(DEFEAT_BUTTONS) or t < 1.0 + 0.15 * j:
            left = []
        else:
            text = _defeat_button(j, kind)
            active = j == sel
            style = (c(15) + BOLD if flash else c(196) + BOLD) if active else c(245)
            if active and kind == 1:
                a = box_left - 4 + pulse
                arrow = c(226) + BOLD
                left = [(" " * a, ""), (">>", arrow), (" " * (2 - pulse), ""),
                        (text, style), (" " * (2 - pulse), ""), ("<<", arrow)]
            else:
                left = [(" " * box_left, ""), (text, style)]
        left = _fit(left, left_w)

        if t >= 1.2:
            right = portrait[k]
        else:
            right = [(" " * (PORTRAIT_W + 2), "")]
        lines.append(_row([(" " * lead, "")] + left + right + [(" " * right_margin, "")]))
    mid_end = len(lines)

    lines += [_row([]), dots()]
    hint = "W/S or UP/DOWN to move   ENTER to select   or press 1 2"
    lines.append(_row([(" " * ((INNER - len(hint)) // 2), ""), (hint, c(245))]))
    lines.append(c(196) + "+" + "=" * INNER + "+" + RESET)

    extra = size.lines - 1 - len(lines)
    if extra > 0:
        blank = _row([])
        gap_top = extra // 4
        gap_title = extra // 4
        gap_mid = extra - gap_top - gap_title
        lines = (lines[:2] + [blank] * gap_top + lines[2:title_end] + [blank] * gap_title
                 + lines[title_end:mid_end] + [blank] * gap_mid + lines[mid_end:])

    return HOME + "".join(l + CLEAR_EOL + "\n" for l in lines)

def run_defeat_screen(gold, earned, phit, ehit, crits):
    stret.stop()
    lose.play()
    bg.play()
    enable_ansi_on_windows()
    if not _can_animate():
        return None
    info = {"gold": gold, "earned": earned, "phit": phit, "ehit": ehit, "crits": crits}
    sel, result = 0, 2
    out = sys.stdout
    out.write(HIDE_CURSOR + CLEAR)
    out.flush()
    t0 = time.monotonic()
    try:
        with raw_input_mode():
            while True:
                now = time.monotonic()
                t = now - t0
                if _too_small(out):
                    continue
                key = poll_key()

                if key == "up":
                    move.play()
                    
                    sel = (sel - 1) % len(DEFEAT_BUTTONS)
                elif key == "down":
                    move.play()
                    sel = (sel + 1) % len(DEFEAT_BUTTONS)
                elif key in ("1", "2"):
                    move.play()
                    sel = int(key) - 1
                elif key == "quit":
                    move.play()
                    result = 2
                    break
                elif key == "enter":
                    select.play()
                    result = sel + 1
                    for i in range(8):
                        out.write(_render_defeat(t + i * 0.05, sel, i % 2 == 0, info))
                        out.flush()
                        time.sleep(0.05)
                    break

                out.write(_render_defeat(t, sel, False, info))
                out.flush()

                spare = 1.0 / FPS - (time.monotonic() - now)
                if spare > 0:
                    time.sleep(spare)
    except KeyboardInterrupt:
        result = 2
    finally:
        out.write(RESET + SHOW_CURSOR + CLEAR + HOME)
        out.flush()
    return result

def _static_exit():
    print("+" + "-" * 44 + "+")
    print("|" + "THANK YOU FOR PLAYING!".center(44) + "|")
    print("|" + "SEE YOU NEXT TIME, FIGHTER!".center(44) + "|")
    print("+" + "-" * 44 + "+")
    try:
        input("Press ENTER to exit...")
    except (EOFError, KeyboardInterrupt):
        pass

def run_exit_screen():
    enable_ansi_on_windows()
    if not _can_animate():
        _static_exit()
        return
    out = sys.stdout
    out.write(HIDE_CURSOR + CLEAR)
    out.flush()
    t0 = time.monotonic()
    try:
        with raw_input_mode():
            while True:
                now = time.monotonic()
                t = now - t0
                if _too_small(out):
                    continue
                key = poll_key()
                if key in ("enter", "quit"):
                    for i in range(8):
                        out.write(_render_exit(t + i * 0.05, True))
                        out.flush()
                        time.sleep(0.05)
                    break
                out.write(_render_exit(t, False))
                out.flush()
                spare = 1.0 / FPS - (time.monotonic() - now)
                if spare > 0:
                    time.sleep(spare)
    except KeyboardInterrupt:
        pass
    finally:
        out.write(RESET + SHOW_CURSOR + CLEAR + HOME)
        out.flush()

SHOP_HEIGHT = 28

MAPS = [
    ("STREET", 208,
     ["|##| /||\\ |##|", "|##|/ || \\|##|"]),
    ("UNDERGROUND", 245,
     ["==|========|==", "  \\\\  ||  //  "]),
    ("BOXING RING", 196,
     ["+==+==+==+==+", "|  _[__]_   |"]),
]

ITEMS = [
    ("none", "NO GLOVES", 0,
     ["  .--.      .--.  ", " ( () )    ( () ) ", "  '--'      '--'  "], 250),
    ("spiked", "SPIKED GLOVES", 2500,
     [" ^ ^ ^      ^ ^ ^ ", " (@@@@@)    (@@@@@)", "  '---'      '---' "], 252),
    ("bomb", "BOMB GLOVES", 5000,
     ["  .--.   *   .--. ", " (@@@@) (o) (@@@@)", "  '--'       '--' "], 214),
    ("lava", "LAVA GLOVES", 10000,
     ["  ~^~^~     ~^~^~ ", " (@@@@@)   (@@@@@)", "  ~'~'~     ~'~'~ "], 202),
]

DESCRIPTIONS = {
    "none": "NO GLOVES: BASE DAMAGE | TWIN PUNCH ULT: 3 HITS = DOUBLE DAMAGE",
    "spiked": "SPIKED: 20% CRIT RATE | BERSERK ULT: 3 HITS = +250% BASE DAMAGE",
    "bomb": "BOMB: +200% BASE DAMAGE | BLOODLUST BANG ULT: 3 HITS = +500% DAMAGE",
    "lava": "LAVA: +150% DAMAGE, +30% CRIT | MULTXXXXX ULT: 5 HITS = STACKING +30%",
}

LOCK_MSG = [
    "",
    "MAP NOT UNLOCKED YET, DEFEAT THE HARD DIFFICULTY OF THE 1ST MAP",
    "MAP NOT UNLOCKED YET, DEFEAT THE HARD DIFFICULTY OF THE 2ND MAP",
]

_shop_reason = ""

def _header(t, shown, title):
    _sync_size()
    coin = ["[o]", "[O]", "[0]", "[O]"][int(t * 5) % 4]
    lines = [
        c(208) + "+" + "=" * INNER + "+" + RESET,
        _row([("  GOLD: ", c(220) + BOLD), (str(int(round(shown))), c(226) + BOLD),
              (" ", ""), (coin, c(220) + BOLD)]),
        _row([]),
    ]
    rows = block_text(title)
    tw = len(rows[0])
    reveal = min(tw, int(t / 0.7 * tw))
    pad = (INNER - tw) // 2
    for r, text in enumerate(rows):
        parts = [(" " * pad, "")]
        for i, ch in enumerate(text):
            if ch == "#" and i < reveal:
                parts.append(("#", c(FIRE[(i // 2 + r - int(t * 12)) % len(FIRE)]) + BOLD))
            else:
                parts.append((" ", ""))
        lines.append(_row(parts))
    lines.append(_row([]))
    return lines

def _stars(t):
    shift = int(t * 10)
    return _row([("*", c(220) + BOLD) if (i + shift) % 4 == 0 else (".", c(240))
                 for i in range(INNER)])

def _footer(t, msg, msg_style, hint):
    return [
        _stars(t),
        _row([(msg.center(INNER), msg_style)] if msg else []),
        _row([(hint.center(INNER), c(245))]),
        c(208) + "+" + "=" * INNER + "+" + RESET,
    ]

def _portrait_rows(t, punching):
    return portrait_box(art=portrait_art(t, punching))

def _portrait_parts(box, k):
    return box[k]

def _shop_frame(lines):
    size = _sync_size()
    extra = size.lines - 1 - len(lines)
    if extra > 0:
        blank = _row([])
        top = extra // 4
        middle = extra // 4
        lines = (lines[:2] + [blank] * top + lines[2:9] + [blank] * middle + lines[9:-4]
                 + [blank] * (extra - top - middle) + lines[-4:])
    return HOME + "".join(l + CLEAR_EOL + "\n" for l in lines)

MAP_W = 44

def _map_cell(j, kind, st, t):
    name, color, scene = MAPS[j]
    locked = not st["unlocked"][j]
    active = j == st["sel"]
    flash = t < st.get("flash_until", 0)
    bs = (c(15) + BOLD if flash else c(226) + BOLD) if active else c(240)
    ls = c(15) + BOLD if active else c(250)
    if locked:
        color = 240
        ls = c(196) + BOLD if active else c(240)
    if kind in (0, 3):
        return [("+" + "=" * (MAP_W - 2) + "+", bs)]
    art = scene[kind - 1].center(16)[:16]
    label = (("LOCKED" if locked else "MAP") if kind == 1 else name).center(25)[:25]
    return [("|", bs), (art, c(color)), ("|", bs), (label, ls), ("|", bs)]

def _render_maps(st, t):
    lines = _header(t, st["shown"], "CHOOSE MAP")
    box = _portrait_rows(t, t < st.get("flash_until", 0))
    pulse = int(t * 3) % 2
    for k in range(15):
        j, kind = divmod(k, 5)
        if kind == 4 or j >= len(MAPS):
            left = [(" " * (3 + MAP_W), "")]
            gap = [("   ", "")]
        else:
            active = j == st["sel"]
            arrow = c(196) + BOLD
            show = active and kind in (1, 2)
            lead = [((">> " if pulse else " >>"), arrow)] if show else [("   ", "")]
            left = lead + _map_cell(j, kind, st, t)
            gap = [(("<< " if pulse else " <<"), arrow)] if show else [("   ", "")]
        pk = k - 1
        right = _portrait_parts(box, pk) if 0 <= pk < len(box) else [(" " * (PORTRAIT_W + 2), "")]
        lines.append(_row([(" " * max(0, (INNER - (50 + PORTRAIT_W + 2)) // 2), "")] + left + gap + right))
    hint = "W/S or UP/DOWN to move   ENTER to select   ESC to go back"
    if t < st.get("msg_until", 0):
        lines += _footer(t, st["msg"], c(196) + BOLD, hint)
    else:
        lines += _footer(t, "", "", hint)
    return _shop_frame(lines)

def _handle_maps(st, key, t):
    if "done_at" in st:
        return
    if key == "up":
        move.play()
        st["sel"] = (st["sel"] - 1) % len(MAPS)
    elif key == "down":
        move.play()
        st["sel"] = (st["sel"] + 1) % len(MAPS)
    elif key.isdigit() and key in "123":
        move.play()
        st["sel"] = int(key) - 1
    elif key == "quit":
        move.play()
        st["result"] = 0
        st["done_at"] = t
    elif key == "enter":
        select.play()
        if not st["unlocked"][st["sel"]]:
            denied.play()
            st["msg"] = LOCK_MSG[st["sel"]]
            st["msg_until"] = t + 2.5
        else:
            st["result"] = st["sel"] + 1
            st["flash_until"] = t + 0.4
            st["done_at"] = t + 0.4

CARD_W = 21
CARD_ART_ROWS = 4
CARD_ROWS = CARD_ART_ROWS + 4

def _glove_card_rows(gid, t):
    """Shop picture of a glove pair: CARD_ART_ROWS terminal rows of (text, style) runs, or None."""
    num = GLOVE_NUMBER.get(gid)
    halves = glove_pair_image(num)
    if halves is None:
        return None
    pixels = _card_pixels_cache.get(gid)
    if pixels is None:
        pixels = _card_pixels_cache[gid] = fit_pixels(halves, CARD_W - 2, CARD_ART_ROWS)
    if gid == "lava":                                  # pulsing heat glow on the lava gloves
        glow = 0.10 + 0.12 * (1 + math.sin(t * 6)) / 2
        pixels = [[tint_color(p, (255, 120, 0), glow) if p is not None else None for p in row]
                  for row in pixels]
    width = len(pixels[0])
    left = (CARD_W - 2 - width) // 2
    rows = pixels_to_parts(pixels)
    return [[(" " * left, "")] + row + [(" " * (CARD_W - 2 - left - width), "")] for row in rows]

_card_pixels_cache = {}

def _card_cell(k, local, st, t):
    gid, label, price, art, base = ITEMS[k]
    active = k == st["sel"]
    flash = t < st.get("flash_until", 0)
    bs = (c(15) + BOLD if flash else c(226) + BOLD) if active else c(240)
    if local in (0, CARD_ROWS - 1):
        return [("+" + "-" * (CARD_W - 2) + "+", bs)]
    if 1 <= local <= CARD_ART_ROWS:
        picture = _glove_card_rows(gid, t)
        if picture is not None:
            return [("|", bs)] + picture[local - 1] + [("|", bs)]
        color = c(FIRE[(int(t * 8) + local + k) % len(FIRE)]) if gid == "lava" else c(base)
        text = art[local - 1] if local <= len(art) else ""
        return [("|", bs), (text.center(CARD_W - 2)[:CARD_W - 2], color), ("|", bs)]
    if local == CARD_ART_ROWS + 1:
        style = c(15) + BOLD if active else c(250)
        return [("|", bs), (f"[ {label} ]".center(CARD_W - 2)[:CARD_W - 2], style), ("|", bs)]
    if st["equipped"] == gid:
        txt, style = "EQUIPPED", c(46) + BOLD
    elif gid in st["owned"]:
        txt, style = "OWNED", c(51)
    elif st["mode"] == "pick":
        txt, style = "LOCKED", c(196)
    else:
        txt = f"{price} G"
        style = c(226) + BOLD if st["gold"] >= price else c(196)
    return [("|", bs), (txt.center(CARD_W - 2), style), ("|", bs)]

def _render_shop(st, t):
    lines = _header(t, st["shown"], "SHOP" if st["mode"] == "shop" else "EQUIPMENTS")
    box = _portrait_rows(t, t < st.get("flash_until", 0))
    def cell(col, kr):
        # the two card rows share one border line, so 2 cards of CARD_ROWS rows fit in 2*CARD_ROWS-1 rows
        if kr == CARD_ROWS - 1:
            lower = 2 + col
            if st["sel"] == lower:
                return _card_cell(lower, 0, st, t)
            return _card_cell(col, CARD_ROWS - 1, st, t)
        if kr < CARD_ROWS - 1:
            return _card_cell(col, kr, st, t)
        return _card_cell(2 + col, kr - (CARD_ROWS - 1), st, t)
    for kr in range(2 * CARD_ROWS - 1):
        left = [("   ", "")] + cell(0, kr) + [("  ", "")] + cell(1, kr)
        pk = kr - 1
        right = _portrait_parts(box, pk) if 0 <= pk < len(box) else [(" " * (PORTRAIT_W + 2), "")]
        lines.append(_row([(" " * max(0, (INNER - 76) // 2), "")] + left + [("   ", "")] + right))
    if t < st.get("msg_until", 0):
        msg, msg_style = st["msg"], st.get("msg_style", "")
    else:
        msg, msg_style = DESCRIPTIONS.get(ITEMS[st["sel"]][0], ""), c(250)
    hint = ("W/S or UP/DOWN to move   1-4 jump   ENTER equip   ESC back" if st["mode"] == "pick"
            else "W/S or UP/DOWN to move   1-4 jump   ENTER buy   ESC back")
    lines += _footer(t, msg, msg_style, hint)
    return _shop_frame(lines)

def _try_buy(st, t):
    gid, label, price, _, _ = ITEMS[st["sel"]]
    if st["mode"] == "pick":
        if gid in st["owned"]:
            buy.play()
            st["equipped"] = gid
            st["flash_until"] = t + 0.4
            st["done_at"] = t + 0.4
            st["msg"], st["msg_style"] = f"{label} EQUIPPED", c(46) + BOLD
        else:
            st["msg"], st["msg_style"] = "YOU DONT HAVE THAT YET", c(196) + BOLD
            denied.play()
    elif gid in st["owned"]:
        st["equipped"] = gid
        st["msg"], st["msg_style"] = f"{label} EQUIPPED", c(46) + BOLD
    elif st["gold"] >= price:
        st["gold"] -= price
        st["owned"].add(gid)
        st["equipped"] = gid
        st["flash_until"] = t + 0.4
        st["msg"], st["msg_style"] = f"PURCHASED {label}!  -{price} GOLD", c(226) + BOLD
        buy.play()
    else:
        st["msg"], st["msg_style"] = "NOT ENOUGH GOLD!", c(196) + BOLD
        denied.play()
    st["msg_until"] = t + 2.0

def _handle_shop(st, key, t):
    if "done_at" in st:
        return
    if key == "up":
        move.play()
        st["sel"] = (st["sel"] - 1) % len(ITEMS)
    elif key == "down":
        move.play()
        st["sel"] = (st["sel"] + 1) % len(ITEMS)
    elif key.isdigit() and key in "1234":
        move.play()
        st["sel"] = int(key) - 1
    elif key == "quit":
        select.play()
        if st["mode"] == "pick":
            st["equipped"] = None
        st["done_at"] = t
    elif key == "enter":
        select.play()
        _try_buy(st, t)

def _shop_can_animate():
    global _shop_reason
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        _shop_reason = ("this is not a real terminal. Open Command Prompt / PowerShell / "
                   "Windows Terminal and run:  python punch_type_combined.py")
        return False
    size = shutil.get_terminal_size((80, 30))
    if size.columns < 80 or size.lines < SHOP_HEIGHT + 2:
        _shop_reason = (f"your terminal is {size.columns}x{size.lines}; this screen needs at least "
                   f"80x{SHOP_HEIGHT + 2}. Maximize the terminal or reduce its font size, then restart.")
        return False

    _sync_size()
    return True

def _animate(st, render, handle):
    out = sys.stdout
    out.write(HIDE_CURSOR + CLEAR)
    out.flush()
    t0 = last = time.monotonic()
    try:
        with raw_input_mode():
            while True:
                now = time.monotonic()
                dt, last, t = now - last, now, now - t0
                if _too_small(out, SHOP_HEIGHT + 2):
                    continue
                handle(st, poll_key(), t)
                if "done_at" in st and t >= st["done_at"]:
                    break
                if st["shown"] != st["gold"]:
                    step = max(60.0, abs(st["shown"] - st["gold"]) / 0.5) * dt
                    if st["shown"] > st["gold"]:
                        st["shown"] = max(float(st["gold"]), st["shown"] - step)
                    else:
                        st["shown"] = min(float(st["gold"]), st["shown"] + step)
                out.write(render(st, t))
                out.flush()
                spare = 1.0 / FPS - (time.monotonic() - now)
                if spare > 0:
                    time.sleep(spare)
    except KeyboardInterrupt:
        st.setdefault("result", 0)
    finally:
        out.write(RESET + SHOW_CURSOR + CLEAR + HOME)
        out.flush()

def _static_maps(gold, unlocked):
    print("=== CHOOSE MAP ===    GOLD:", gold)
    for i, (name, _, _) in enumerate(MAPS, 1):
        print(f"  {i}. MAP {name}" + ("" if unlocked[i - 1] else "   [LOCKED]"))
    print(f"(Animation is off: {_shop_reason})")
    while True:
        try:
            n = int(input("ENTER CHOICE (0 = back): "))
        except (ValueError, EOFError):
            return 0
        if not 1 <= n <= len(MAPS):
            return 0
        if unlocked[n - 1]:
            return n
        print(LOCK_MSG[n - 1])

def _static_shop(gold, owned, equipped, mode="shop"):
    print(f"(Animation is off: {_shop_reason})")
    while True:
        print(f"\n=== CHOOSE EQUIPMENTS ===    GOLD: {gold}")
        for i, (gid, label, price, _, _) in enumerate(ITEMS, 1):
            tag = ("EQUIPPED" if gid == equipped else "OWNED" if gid in owned
                   else "LOCKED" if mode == "pick" else f"{price} G")
            print(f"  {i}. {label:<14} {tag}")
        try:
            n = int(input("BUY / EQUIP (0 = back): "))
        except (ValueError, EOFError):
            return equipped, gold, owned
        if n == 0:
            return (None if mode == "pick" else equipped), gold, owned
        if 1 <= n <= len(ITEMS):
            gid, label, price, _, _ = ITEMS[n - 1]
            if mode == "pick":
                if gid in owned:
                    return gid, gold, owned
                print("YOU DONT HAVE THAT YET")
            elif gid in owned:
                equipped = gid
            elif gold >= price:
                gold -= price
                owned.add(gid)
                equipped = gid
                print(f"Purchased {label}!")
            else:
                print("NOT ENOUGH GOLD!")

def run_map_select(gold=0, unlocked=(1, 1, 1)):
    enable_ansi_on_windows()
    unlocked = [bool(u) for u in unlocked] + [True] * len(MAPS)
    unlocked = unlocked[:len(MAPS)]
    if not _shop_can_animate():
        return _static_maps(gold, unlocked)
    st = {"sel": 0, "gold": gold, "shown": float(gold), "result": 0, "unlocked": unlocked}
    _animate(st, _render_maps, _handle_maps)
    return st["result"]

def run_shop(gold=0, owned=None, equipped="none", mode="shop"):
    enable_ansi_on_windows()
    owned = set(owned or ()) | {"none"}
    if not _shop_can_animate():
        return _static_shop(gold, owned, equipped, mode)
    sel = next((i for i, it in enumerate(ITEMS) if it[0] == equipped), 0)
    st = {"sel": sel, "gold": gold, "shown": float(gold), "owned": owned,
          "equipped": equipped, "msg": "", "mode": mode}
    _animate(st, _render_shop, _handle_shop)
    return st["equipped"], st["gold"], st["owned"]

DIFF_HEIGHT = 26

DIFFICULTIES = [
    {"name": "EASY", "stars": "*", "color": 46, "hp": 500, "dmg": 10, "time": "3s", "win": 500,
     "keys": "QWERTY"},
    {"name": "MEDIUM", "stars": "**", "color": 220, "hp": 1000, "dmg": 25, "time": "2s", "win": 800,
     "keys": "QWERTYASDFGH"},
    {"name": "HARD", "stars": "***", "color": 196, "hp": 1500, "dmg": 50, "time": "1.5s", "win": 1000,
     "keys": "QWERTYASDFGHZXCVB"},
]
DIFF_BTN_W = 31
BACK_BTN_W = 15

_diff_reason = ""

def _diff_button(label, stars, inner, kind):
    if kind != 1:
        return "+" + "-" * inner + "+"
    if stars:
        text = (" " + stars.ljust(3)).ljust(4) + label.center(inner - 8) + " " * 4
    else:
        text = label.center(inner)
    return "|" + text + "|"

def _button_parts(text, style, active, kind, box_left, pulse, arrow_color):
    if active and kind == 1:
        a = box_left - 4 + pulse
        arrow = arrow_color + BOLD
        return [(" " * a, ""), (">>", arrow), (" " * (2 - pulse), ""),
                (text, style), (" " * (2 - pulse), ""), ("<<", arrow)]
    return [(" " * box_left, ""), (text, style)]

def _diff_frame(lines):
    size = _sync_size()
    extra = size.lines - 1 - len(lines)
    if extra > 0:
        blank = _row([])
        top = extra // 4
        middle = extra // 4
        lines = (lines[:2] + [blank] * top + lines[2:8] + [blank] * middle + lines[8:-3]
                 + [blank] * (extra - top - middle) + lines[-3:])
    return HOME + "".join(l + CLEAR_EOL + "\n" for l in lines)

def _render_difficulty(t, sel, flash, punching):
    _sync_size()
    inner = INNER
    lines = [c(208) + "+" + "=" * inner + "+" + RESET]

    label = "S E L E C T"
    lines.append(_row([(" " * ((inner - len(label)) // 2), ""), (label, c(250) + BOLD)]))

    rows = block_text("DIFFICULTY")
    tw = len(rows[0])
    reveal = min(tw, int(t / 0.5 * tw))
    pad = (inner - tw) // 2
    sweep = int(t * 30) % (tw + 30) - 10
    for r, text in enumerate(rows):
        parts = [(" " * pad, "")]
        for i, ch in enumerate(text):
            if ch == "#" and i < reveal:
                hot = 0 <= (i - sweep + r) < 5
                parts.append(("#", (c(196) if hot else c(255)) + BOLD))
            else:
                parts.append((" ", ""))
        lines.append(_row(parts))

    uline = []
    for i in range(tw):
        hot = 0 <= (i - sweep) < 8
        uline.append(("=" if i < reveal else " ", c(196) + BOLD if hot else c(250)))
    lines.append(_row([(" " * pad, "")] + uline))

    left_w = min(inner - PORTRAIT_W - 2 - 4, 46)
    lead = max(0, (inner - left_w - PORTRAIT_W - 2) // 2)
    right_margin = max(0, inner - lead - left_w - PORTRAIT_W - 2)
    pulse = int(t * 3) % 2
    art = portrait_art(t, punching, mood="angry" if sel == 2 else "idle")
    portrait = portrait_box(art=art)

    for k in range(15):
        j, kind = divmod(k, 4)
        left = []
        if k <= 10 and kind != 3 and t >= 0.5 + 0.12 * j:
            d = DIFFICULTIES[j]
            box_left = (left_w - (DIFF_BTN_W + 2)) // 2
            text = _diff_button(d["name"], d["stars"], DIFF_BTN_W, kind)
            active = j == sel
            if active:
                if kind != 1:
                    text = "+" + "=" * DIFF_BTN_W + "+"
                style = (c(15) if flash else c(d["color"])) + BOLD
            else:
                style = c(240)
            left = _button_parts(text, style, active, kind, box_left, pulse, c(d["color"]))
        elif k >= 12 and t >= 0.5 + 0.12 * 3:
            kind = k - 12
            box_left = (left_w - (BACK_BTN_W + 2)) // 2
            text = _diff_button("<- BACK", "", BACK_BTN_W, kind)
            active = sel == 3
            if active:
                if kind != 1:
                    text = "+" + "=" * BACK_BTN_W + "+"
                style = (c(15) if flash else c(250)) + BOLD
            else:
                style = c(240)
            left = _button_parts(text, style, active, kind, box_left, pulse, c(250))
        left = _fit(left, left_w)

        if k < len(portrait) and t >= 0.8:
            right = portrait[k]
        else:
            right = [(" " * (PORTRAIT_W + 2), "")]
        lines.append(_row([(" " * lead, "")] + left + right + [(" " * right_margin, "")]))

    if sel < 3:
        d = DIFFICULTIES[sel]
        info = f"HP {d['hp']} | DMG {d['dmg']} | REACT {d['time']} | WIN +{d['win']} G | KEYS {d['keys']}"
        info_style = c(d["color"]) + BOLD
    else:
        info = "Return to the main menu"
        info_style = c(250)
    lines.append(_row([(" " * ((inner - len(info)) // 2), ""), (info, info_style)]))

    hint = "W/S or UP/DOWN to move   ENTER to select   1 2 3 pick   4 or ESC back"
    lines.append(_row([(" " * ((inner - len(hint)) // 2), ""), (hint, c(245))]))
    lines.append(c(208) + "+" + "=" * inner + "+" + RESET)
    return _diff_frame(lines)

def _diff_can_animate():
    global _diff_reason, WIDTH, INNER
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        _diff_reason = ("this is not a real terminal. Open Command Prompt / PowerShell / "
                   "Windows Terminal and run:  python punch_type_combined.py")
        return False
    size = shutil.get_terminal_size((80, 30))
    if size.columns < 80 or size.lines < DIFF_HEIGHT + 2:
        _diff_reason = (f"your terminal is {size.columns}x{size.lines}; this screen needs at least "
                   f"80x{DIFF_HEIGHT + 2}. Maximize the terminal or reduce its font size, then restart.")
        return False
    WIDTH = max(78, size.columns)
    INNER = WIDTH - 2
    return True

def _static_difficulty():
    print(f"(Animation is off: {_diff_reason})")
    print("CONTROLS FOR EASY MODE IS QWERTY. FOR MEDIUM AND HARD, MORE LETTERS ARE ADDED.")
    print("=====================")
    print("Select Difficulty")
    print("1.EASY")
    print("2.MEDIUM")
    print("3.HARD")
    print("4.BACK")
    print("=====================")
    try:
        return int(input())
    except ValueError:
        return 0
    except EOFError:
        return 4

def run_difficulty_menu():
    enable_ansi_on_windows()
    if not _diff_can_animate():
        return _static_difficulty()

    sel, result = 0, 4
    out = sys.stdout
    out.write(HIDE_CURSOR + CLEAR)
    out.flush()
    t0 = time.monotonic()
    try:
        with raw_input_mode():
            while True:
                now = time.monotonic()
                t = now - t0
                if _too_small(out, DIFF_HEIGHT + 2):
                    continue
                key = poll_key()

                if key == "up":
                    sel = (sel - 1) % 4
                    move.play()
                elif key == "down":
                    move.play()
                    sel = (sel + 1) % 4
                elif key in ("1", "2", "3", "4"):
                    move.play()
                    sel = int(key) - 1
                elif key == "quit":
                    move.play()
                    result = 4
                    break
                elif key == "enter":
                    select.play()
                    result = sel + 1
                    for i in range(8):
                        out.write(_render_difficulty(t + i * 0.05, sel, i % 2 == 0, sel < 3))
                        out.flush()
                        time.sleep(0.05)
                    break

                out.write(_render_difficulty(t, sel, False, False))
                out.flush()

                spare = 1.0 / FPS - (time.monotonic() - now)
                if spare > 0:
                    time.sleep(spare)
    except KeyboardInterrupt:
        result = 4
    finally:
        out.write(RESET + SHOW_CURSOR + CLEAR + HOME)
        out.flush()
    return result

W = 78
H = 27
MIN_COLS = W + 2
MIN_ROWS = H + 2

REASON = ""

ENEMY_NAMES = {1: "STREET THUG", 2: "IRON MIKE", 3: "THE CHAMPION"}
DIFF_NAMES = {1: "EASY", 2: "MEDIUM", 3: "HARD"}
HIT_WORDS = [ "GOOD JOB!", "NICE!", "WELL TIMED!"]
ESAY = ["AYAAAAAN NAAAA", "NGAWNGAW", "ARAYKUPOOOOO"]
SAY = ["WOOOOOOW!!!!", "UNSTOPPABLE!!!", "UY BAGSAK!!","WHOOOOOO!!!!"]

class Canvas:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.ch = [[" "] * w for _ in range(h)]
        self.st = [[""] * w for _ in range(h)]
        self.bg = [[""] * w for _ in range(h)]

    def put(self, x, y, text, style=""):
        if not 0 <= y < self.h:
            return
        for i, ch in enumerate(text):
            if 0 <= x + i < self.w:
                self.ch[y][x + i] = ch
                self.st[y][x + i] = style

    def panel(self, x, y, w, h, border="", fill=(12, 10, 16)):
        """Solid dark box (optional +-| border) so text stays readable on top of the picture."""
        bg = px_bg(fill)
        for yy in range(y, y + h):
            if 0 <= yy < self.h:
                for xx in range(max(0, x), min(self.w, x + w)):
                    self.ch[yy][xx] = " "
                    self.st[yy][xx] = ""
                    self.bg[yy][xx] = bg
        if border and w >= 2 and h >= 2:
            self.put(x, y, "+" + "-" * (w - 2) + "+", border)
            self.put(x, y + h - 1, "+" + "-" * (w - 2) + "+", border)
            for yy in range(y + 1, y + h - 1):
                self.put(x, yy, "|", border)
                self.put(x + w - 1, yy, "|", border)

    def tag(self, x, y, text, style, fill=(12, 10, 16)):
        """Text with a dark 1-cell padding behind it (floating numbers, combo counter)."""
        bg = px_bg(fill)
        for xx in range(x - 1, x + len(text) + 1):
            if 0 <= xx < self.w and 0 <= y < self.h:
                self.ch[y][xx] = " "
                self.st[y][xx] = ""
                self.bg[y][xx] = bg
        self.put(x, y, text, style)

    def put_solid(self, x, y, text, style):
        left = len(text) - len(text.lstrip())
        right = len(text.rstrip())
        for i in range(left, right):
            ch = text[i]
            s = style(ch) if callable(style) else style
            self.put(x + i, y, ch, s)

    def lines(self):
        out = []
        for y in range(self.h):
            row = []
            start = 0
            chs, sts, bgs = self.ch[y], self.st[y], self.bg[y]
            for x in range(1, self.w + 1):
                if x == self.w or sts[x] != sts[start] or bgs[x] != bgs[start]:
                    text = "".join(chs[start:x])
                    style = bgs[start] + sts[start]
                    row.append(style + text + RESET if style else text)
                    start = x
            out.append("".join(row))
        return out

LEVELS = [(6, 3), (4, 2), (3, 2), (2, 1), (1, 1)]
SX = 1
SY = 1
FLOOR = 15

def scale_art(rows, sx, sy):
    out = []
    for row in rows:
        out += ["".join(ch * sx for ch in row)] * sy
    return out

def set_layout(cols, rows):
    global W, H, SX, SY, FLOOR
    W = cols - 1
    H = rows - 1
    SX, SY = 1, 1
    for sx, sy in LEVELS:
        if ENEMY_W * sx + 16 <= W and 17 * sy <= H - 10:
            SX, SY = sx, sy
            break
    FLOOR = H - 6 - 6 * SY

def _sprite(w, h, parts):
    grid = [[" "] * w for _ in range(h)]
    for x, y, text in parts:
        for i, ch in enumerate(text):
            grid[y][x + i] = ch
    return ["".join(row) for row in grid]

ENEMY_W = 32
ENEMY_H = 11

ENEMY_IDLE = _sprite(ENEMY_W, ENEMY_H, [
    (11, 0, ".---------."),
    (9, 1, "/   ,     ,   \\"),
    (1, 2, ".---."), (8, 2, "|   (O)   (O)   |"), (26, 2, ".---."),
    (0, 3, "(@@@@@)"), (8, 3, "|       >       |"), (25, 3, "(@@@@@)"),
    (0, 4, "(@@@@@)"), (10, 4, "\\    ===    /"), (25, 4, "(@@@@@)"),
    (1, 5, "'---'"), (12, 5, "'-.___.-'"), (26, 5, "'---'"),
    (9, 6, "/|     #     |\\"),
    (8, 7, "/ |     #     | \\"),
    (7, 8, "/  |     #     |  \\"),
    (9, 9, "|_______#_______|"),
    (10, 10, "/ |   | |   | \\"),
])

def _swap_eyes(rows, left, right):
    return [r.replace("(O)", left, 1).replace("(O)", right, 1) for r in rows]

ENEMY_WINDUP = _swap_eyes(ENEMY_IDLE, "(>)", "(<)")
ENEMY_HURT = _swap_eyes(ENEMY_IDLE, "(X)", "(X)")

FIST_BIG = [
    r"   .-~~~~~~-.   ",
    r"  / @@@@@@@@ \  ",
    r" | @@@@@@@@@@ | ",
    r" | @@@@@@@@@@ | ",
    r"  \ @@@@@@@@ /  ",
    r"   '-.____.-'   ",
]

GLOVE_W = 14
GLOVE = [
    r"   .------.   ",
    r"  /  ,--,  \  ",
    r" |  ( () )  | ",
    r" |   '--'   | ",
    r"  \  ====  /  ",
    r"   '------'   ",
]
GLOVE_TOP = {
    2: r"  ^ ^ ^ ^ ^   ",
    3: r"   .--**--.   ",
    4: r"  ~^~^~^~^~   ",
}
GLOVE_COLOR = {1: 196, 2: 252, 3: 214}

# which picture belongs to which glove (1 none, 2 spiked, 3 bomb, 4 lava)
GLOVE_IMAGE = {1: "glove_none", 2: "glove_spiky", 3: "glove_black", 4: "glove_red"}
_glove_cache = {}
_glove_cols_now = None

def glove_pair_image(num):
    """The shop picture: the left+right pair image, cropped to its visible pixels."""
    key = GLOVE_IMAGE.get(num)
    pair = load_image(key) if key else None
    if pair is None:
        return None
    box = solid_bbox(pair)
    return pair.crop(box) if box else None

def glove_halves(num):
    """(left glove, right glove) cropped to the same height, from the pair image."""
    key = GLOVE_IMAGE.get(num)
    pair = load_image(key) if key else None
    if pair is None:
        return None
    half = pair.width // 2
    left = pair.crop((0, 0, half, pair.height))
    right = pair.crop((half, 0, pair.width, pair.height))
    boxes = [solid_bbox(left), solid_bbox(right)]
    if None in boxes:
        return None
    y0, y1 = min(b[1] for b in boxes), max(b[3] for b in boxes)
    return (left.crop((boxes[0][0], y0, boxes[0][2], y1)),
            right.crop((boxes[1][0], y0, boxes[1][2], y1)))

def glove_sprites(num, rows):
    key = (num, rows)
    if key not in _glove_cache:
        halves = glove_halves(num)
        _glove_cache[key] = None if halves is None else {
            "L": image_pixels(halves[0], rows * 2), "R": image_pixels(halves[1], rows * 2)}
    return _glove_cache[key]

ULT_NAMES = {1: "TWIN PUNCH", 2: "BERSERK", 3: "BLOODLUST BANG", 4: "LAVA MULTXXXX"}

SPRITE_PALETTE = {
    "A": "8c1822",
    "B": "1c424e",
    "C": "2e6470",
    "D": "1a1820",
    "E": "605c6a",
    "a": "120e18",
    "b": "221c2e",
    "c": "4e4268",
    "d": "f0c098",
    "e": "f0f0e8",
    "f": "ce9672",
    "g": "b05454",
    "h": "1c1e34",
    "i": "2a2e4c",
    "j": "c83238",
    "k": "424870",
    "l": "f4cc3c",
    "m": "16141c",
    "n": "5a5664",
    "o": "2c201c",
    "p": "503e34",
    "q": "f4625c",
    "r": "ce2a32",
    "s": "dea476",
    "t": "b03838",
    "u": "804e78",
    "v": "b47856",
    "w": "969aaa",
    "x": "707484",
    "y": "323442",
    "z": "4c5060",
}
SPRITE_RGB = {k: (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)) for k, v in SPRITE_PALETTE.items()}

SPRITES = {
    "street": {
        "idle": [
            "...........aaaaaaaaaaa..........",
            "..........abbbbbbbbbbba.........",
            ".........aabccccbbbbbbaa........",
            "........abbbccccbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            ".........aabbdbdbdbdbbaa........",
            "..........abbdddddddbba.........",
            ".........adbdbbdddbbdbda........",
            ".........adddeadddaeddda........",
            ".........adddffeeeffddda........",
            "..........addddefeddgda.........",
            "..........addddaaaddgda.........",
            "..........adddadddaddda.........",
            "..........afffffffffffa.........",
            "...........aaafffffaaa..........",
            "...........ahiifffiiha..........",
            "........aaaahiifffiihaaaa.......",
            ".....aaaiiiihiijjjiihiiiiaaa....",
            "....aiiiiiiiiiijjjiiiiiiiiiia...",
            "....aikiiiiiiiiijiiiiiiiiiiia...",
            "....ahkiiiikkiiihiiiiiiiiiiha...",
            "....ahkiiiikkiiiliiiiiiiiiiha...",
            "....ahkiiiikkiiihiiiiiiiiiiha...",
            "....ahkiiiikkiiihiiiiiiiiiiha...",
            "....ahkiiiikkiiiliiiiiiiiiiha...",
            "....ahkiiiikkiiihiiiiiiiiiiha...",
            "....ahkiiihhhiiihiiihhhiiiiha...",
            "....ahiiiiiiiiiiliiiiiiiiiiha...",
            "....ahhhhiiiiiiihiiiiiiihhhha...",
            "....addddiiiiiiihiiiiiiidddda...",
            "....adffdhhhhhhhhhhhhhhhdffda...",
            "....addddhhhhhhhhhhhhhhhdddda...",
            "....affffhhiihhhhhhiihhhffffa...",
            ".....aaaahhiihhhhhhiihhhaaaa....",
            "........ahhiihhhhhhiihhha.......",
            "........ahhiihhhahhiihhha.......",
            "........ahhiihhhahhiihhha.......",
            "........ahhiihhhahhiihhha.......",
            "........ahhiihhhahhiihhha.......",
            ".......ahhhhhhhhahhhhhhhha......",
            ".......ahhhhhhhhahhhhhhhha......",
            "......ammmmmmmmmammmmmmmmma.....",
            "......annnnnnnnnannnnnnnnna.....",
            ".......aaaaaaaaa.aaaaaaaaa......",
        ],
        "punch": [
            "...........aaaaaaaaaaa..........",
            "..........abbbbbbbbbbba.........",
            ".........aabccccbbbbbbaa........",
            "........abbbccccbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            "........abbbbbbbbbbbbbbba.......",
            ".........aabbdbdbdbdbbaa........",
            "..........abbdddddddbba.........",
            ".........adbdbbdddbbdbda........",
            ".........adddeadddaeddda........",
            ".........adddffeeeffddda........",
            "..........addddefeddgda.........",
            "..........adddaeeeadgda.........",
            "..........adddaaaaaddda.........",
            "..........afffffffffffa.........",
            "...........aaafffffaaa..........",
            "...........ahiifffiiha..........",
            "........aaaahiifffiihaaaa.......",
            ".....aaaiiiihiijjjiihiiiiaaa....",
            "....aiiiiiiiffffffffiiiiiiiia...",
            "....aikiiiiiddfdfdfdiiiiiiiia...",
            "....ahkiiiikddfdfdfdiiiikkiia...",
            "....akkkkkikddfdfdfdiiiiiiiia...",
            "....ahkiiiikddfdfdffiiiiiiiia...",
            "....ahkiiiikfffddddfiiiiiiiia...",
            "...akkkkkiikfffddddfiiiiiiaa....",
            "....ahkiiiikfffddddfiiiiiia.....",
            "....ahkiiihhffffffffhhhiiia.....",
            "....ahkkkkiiiiiiliiiiiiiaa......",
            "....ahhhhiiiiiiihiiiiiiia.......",
            "....addddiiiiiiihiiiiiiia.......",
            "....adffdhhhhhhhhhhhhhhha.......",
            "....addddhhhhhhhhhhhhhhha.......",
            "....affffhhiihhhhhhiihhha.......",
            ".....aaaahhiihhhhhhiihhha.......",
            "........ahhiihhhhhhiihhha.......",
            "........ahhiihhhahhiihhha.......",
            "........ahhiihhhahhiihhha.......",
            "........ahhiihhhahhiihhha.......",
            "........ahhiihhhahhiihhha.......",
            ".......ahhhhhhhhahhhhhhhha......",
            ".......ahhhhhhhhahhhhhhhha......",
            "......ammmmmmmmmammmmmmmmma.....",
            "......annnnnnnnnannnnnnnnna.....",
            ".......aaaaaaaaa.aaaaaaaaa......",
        ],
    },
    "underground": {
        "idle": [
            "................................",
            "..........aaaaaaaaaaaaa.........",
            ".........aoooooooooooooa........",
            ".........aooppppoooooooa........",
            ".........aoooooooooooooa........",
            ".........aoooooooooooooa........",
            ".........aoooooooooooooa........",
            ".........aoqqqqqqqqqqqoaa.......",
            ".........aorrrrrrrrrrrorra......",
            ".........aosssssssssosorra......",
            ".........assooosssotossrra......",
            ".........assseasssaesssaa.......",
            ".........asssuusssvvsssa........",
            "..........asuuusvsssssa.........",
            "..........assssvvvssssa.........",
            "..........asssssssasssa.........",
            "..........assssaaassssa.........",
            "..........avvvvvvvvvvva.........",
            "..........aaaavvvvvaaaa.........",
            ".........awwwwvvvvvwwwwa........",
            ".........axxxxvvvvvxxxxa........",
            ".....aaaaaxxxxyyyyyxxxxaaaaa....",
            "....azxxxxxxxxxxxxxxxxxxxxxza...",
            "....azxxxxxxxxexxxexxxxxxxxza...",
            "....azxxxxxwwxexxxexxxxxxxxza...",
            "....azxzxxxwwxexxxexxxxxzxzxa...",
            "....avsssxxwwxxxxxxxxxxxsssva...",
            "....avsssxxwwxxxxxxxxxxxsssva...",
            "...aavsssxxwwxxxxxxxxxxxsssvaa..",
            "..aeeeeeexxxxxxxxxxxxxxxeeeeeea.",
            "..arqqrrAxxxzzzzxzzzzxxxrqqrrAa.",
            "..arqrrrAxxxzzzzxzzzzxxxrqrrrAa.",
            "..arrrrrAxxxzzzzxzzzzxxxrrrrrAa.",
            "..arrrrrAxxxzzzzxzzzzxxxrrrrrAa.",
            "..aAAAAAAzzzzzzzzzzzzzzzAAAAAAa.",
            "...aaaaaazzzzzzzzzzzzzzzaaaaaa..",
            ".........aBBBBBBBBBBBBBa........",
            ".........aCBBBBBBBBBBBCa........",
            ".........aCBBBBBBBBBBBCa........",
            ".........aCBBBBBaBBBBBCa........",
            ".........aCBBBBBaBBBBBCa........",
            ".........aCBBBBBaBBBBBCa........",
            ".........aassssa.assssaa........",
            "........aDDDDDDDaDDDDDDDa.......",
            "........aDDDeDDDaDDDeDDDa.......",
            ".......aDDDDeDDDaDDDeDDDDa......",
            ".......aEEEEEEEEaEEEEEEEEa......",
            "........aaaaaaaa.aaaaaaaa.......",
        ],
        "punch": [
            "................................",
            "..........aaaaaaaaaaaaa.........",
            ".........aoooooooooooooa........",
            ".........aooppppoooooooa........",
            ".........aoooooooooooooa........",
            ".........aoooooooooooooa........",
            ".........aoooooooooooooa........",
            ".........aoqqqqqqqqqqqoaa.......",
            ".........aorrrrrrrrrrrorra......",
            ".........aosssssssssosorra......",
            ".........assooosssotossrra......",
            ".........assseasssaesssaa.......",
            ".........asssuusssvvsssa........",
            "..........asuuusvsssssa.........",
            "..........assssvvvssssa.........",
            "..........asssaeeeasssa.........",
            "..........asssaaaaasssa.........",
            "..........avvvvvvvvvvva.........",
            "..........aaaavvvvvaaaa.........",
            ".........awwwwvvvvvwwwwa........",
            ".........axxxxvvvvvxxxxa........",
            ".....aaaaaxrrrrrrrrrAxxaaaaa....",
            "....azxxxxxrqqqrrrrrAxxxxxxza...",
            "....azxxxxxrqqqrArArAxxxxxxza...",
            "...awwwwwwxrrrrrArArAxxxxxxza...",
            "....azxzxxxrrrrrArArAssssssxa...",
            "...aavsssxxrrrrrArArAssssssa....",
            "..awwwwwwxxrAAArrrrrAssssssa....",
            "...aavsssxxrAAArrrrrAssssssa....",
            "..aeeeeeexxrAAArrrrrAssssssa....",
            "..arqqrrAxxrAAArrrrrAvvvvvva....",
            "..arqwwwwwxAAAAAAAAAAxxxaaa.....",
            "..arrrrrAxxxzzzzxzzzzxxxa.......",
            "..arrrrrAxxxzzzzxzzzzxxxa.......",
            "..aAAAAAAzzzzzzzzzzzzzzza.......",
            "...aaaaaazzzzzzzzzzzzzzza.......",
            ".........aBBBBBBBBBBBBBa........",
            ".........aCBBBBBBBBBBBCa........",
            ".........aCBBBBBBBBBBBCa........",
            ".........aCBBBBBaBBBBBCa........",
            ".........aCBBBBBaBBBBBCa........",
            ".........aCBBBBBaBBBBBCa........",
            ".........aassssa.assssaa........",
            "........aDDDDDDDaDDDDDDDa.......",
            "........aDDDeDDDaDDDeDDDa.......",
            ".......aDDDDeDDDaDDDeDDDDa......",
            ".......aEEEEEEEEaEEEEEEEEa......",
            "........aaaaaaaa.aaaaaaaa.......",
        ],
        "block": [
            "................................",
            "..........aaaaaaaaaaaaa.........",
            ".........aoooooooooooooa........",
            ".........aooppppoooooooa........",
            ".........aoooooooooooooa........",
            ".........aoooooooooooooa........",
            ".........aoooooooooooooa........",
            ".........aoqqqqqqqqqqqoaa.......",
            ".........aorrrrrrrrrrrorra......",
            ".........aosssssssssosorra......",
            ".........assooosssotossrra......",
            "........aassseasssaesssaa.......",
            ".......arrrrAuusssvvrrrrAa......",
            ".......arqqrAuusvsssrqqrAa......",
            ".......arqrrAssvvvssrqrrAa......",
            ".......arrrrAsssssasrrrrAa......",
            ".......arrrrAssaaassrrrrAa......",
            ".......arrrrAvvvvvvvrrrrAa......",
            ".......aeeeeeavvvvvaeeeeea......",
            "........avssswvvvvvwsssva.......",
            "........avsssxvvvvvxsssva.......",
            ".....aaaavsssxyyyyyxsssvaaaa....",
            "....azxxxvsssxxxxxxxsssvxxxza...",
            "....azxxxvsssxexxxexsssvxxxza...",
            "....azxxxvsssxexxxexsssvxxxza...",
            "....azxzxvsssxexxxexsssvzxzxa...",
            "....avsssvsssxxxxxxxsssvsssva...",
            "....avsssvsssxxxxxxxsssvsssva...",
            "....avsssvsssxxxxxxxsssvsssva...",
            "....avsssxxxxxxxxxxxxxxxsssva...",
            ".....aaaaxxxzzzzxzzzzxxxaaaa....",
            "........axxxzzzzxzzzzxxxa.......",
            "........axxxzzzzxzzzzxxxa.......",
            "........axxxzzzzxzzzzxxxa.......",
            "........azzzzzzzzzzzzzzza.......",
            "........azzzzzzzzzzzzzzza.......",
            ".........aBBBBBBBBBBBBBa........",
            ".........aCBBBBBBBBBBBCa........",
            ".........aCBBBBBBBBBBBCa........",
            ".........aCBBBBBaBBBBBCa........",
            ".........aCBBBBBaBBBBBCa........",
            ".........aCBBBBBaBBBBBCa........",
            ".........aassssa.assssaa........",
            "........aDDDDDDDaDDDDDDDa.......",
            "........aDDDeDDDaDDDeDDDa.......",
            ".......aDDDDeDDDaDDDeDDDDa......",
            ".......aEEEEEEEEaEEEEEEEEa......",
            "........aaaaaaaa.aaaaaaaa.......",
        ],
    },
}

MAP_SPRITE = {1: "street", 2: "underground"}
MAP_ENEMY_NAMES = {1: "STREET THUG", 2: "UNDERGROUND BOXER", 3: "THE CHAMPION"}
POSE_FRAME = {
    "street": {"idle": "idle", "windup": "idle", "punch": "punch", "hurt": "idle"},
    "underground": {"idle": "idle", "windup": "idle", "punch": "punch", "hurt": "block"},
    "champion": {"idle": "idle", "windup": "idle", "punch": "punch", "hurt": "block"},
}
SPRITE_MAX_ROWS = 24
BG_REGION = None
SPRITE_TRUECOLOR = os.environ.get("TERM_PROGRAM") != "Apple_Terminal"

_sprite_cache = {}
_xterm_cache = {}

def _xterm_index(rgb):
    key = tuple(rgb)
    if key not in _xterm_cache:
        levels = (0, 95, 135, 175, 215, 255)
        near = [min(range(6), key=lambda i: abs(levels[i] - v)) for v in key]
        cube = tuple(levels[i] for i in near)
        gray_step = max(0, min(23, round((sum(key) / 3 - 8) / 10)))
        gray = 8 + 10 * gray_step
        dist_cube = sum((a - b) ** 2 for a, b in zip(key, cube))
        dist_gray = sum((a - gray) ** 2 for a in key)
        if dist_gray < dist_cube:
            _xterm_cache[key] = 232 + gray_step
        else:
            _xterm_cache[key] = 16 + 36 * near[0] + 6 * near[1] + near[2]
    return _xterm_cache[key]

def px_fg(rgb):
    if SPRITE_TRUECOLOR:
        return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    return c(_xterm_index(rgb))

def px_bg(rgb):
    if SPRITE_TRUECOLOR:
        return f"\x1b[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    return f"\x1b[48;5;{_xterm_index(rgb)}m"

def tint_color(rgb, target, amount):
    return tuple(int(round(a + (b - a) * amount)) for a, b in zip(rgb, target))

PNG_SPRITES = {
    "champion": {"idle": "boss_idle", "punch": "boss_punch", "block": "boss_block"},
}
_png_frames = {}

def _png_files_exist(name):
    return Image is not None and all(
        asset_path(*ASSET_NAMES[key]) for key in PNG_SPRITES[name].values())

def _load_png_frames(name):
    if name in _png_frames:
        return _png_frames[name]
    ims = {k: Image.open(asset_path(*ASSET_NAMES[key])).convert("RGBA")
           for k, key in PNG_SPRITES[name].items()}
    box = None
    for im in ims.values():
        b = im.getchannel("A").point(lambda a: 255 if a >= 128 else 0).getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                         max(box[2], b[2]), max(box[3], b[3]))
    if box:
        ims = {k: im.crop(box) for k, im in ims.items()}
    _png_frames[name] = ims
    return ims

SPRITE_OUTLINE = (14, 10, 16)       # dark 1-pixel outline around PNG enemies (None = off)

def outline_pixels(pixels, color):
    h, w = len(pixels), len(pixels[0])
    out = [[None] * (w + 2) for _ in range(h + 2)]
    for y in range(h):
        for x in range(w):
            if pixels[y][x] is not None:
                out[y + 1][x + 1] = pixels[y][x]
    for y in range(h):
        for x in range(w):
            if pixels[y][x] is None:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                if out[y + 1 + dy][x + 1 + dx] is None:
                    out[y + 1 + dy][x + 1 + dx] = color
    return out

def _png_sprite_pixels(name, frame, th):
    im = _load_png_frames(name)[frame]
    sw, sh = im.size
    tw = max(1, round(sw * th / sh))
    im = im.resize((tw, th), Image.NEAREST)
    data = list(im.getdata())
    rows = []
    for y in range(th):
        line = []
        for x in range(tw):
            r, g, b, a = data[y * tw + x]
            line.append((r, g, b) if a >= 128 else None)
        rows.append(line)
    return rows

def _sprite_pixels_raw(name, frame, th):
    key = (name, frame, th)
    if key in _sprite_cache:
        return _sprite_cache[key]
    if name in PNG_SPRITES:
        rows = _png_sprite_pixels(name, frame, th)
        _sprite_cache[key] = rows
        return rows
    grid = SPRITES[name][frame]
    sh, sw = len(grid), len(grid[0])
    tw = max(1, round(sw * th / sh))
    freq = {}
    for row in grid:
        for ch in row:
            freq[ch] = freq.get(ch, 0) + 1
    rows = []
    for ty in range(th):
        y0, y1 = ty * sh / th, (ty + 1) * sh / th
        line = []
        for tx in range(tw):
            x0, x1 = tx * sw / tw, (tx + 1) * sw / tw
            weight = {}
            for sy in range(int(y0), min(sh, math.ceil(y1))):
                wy = min(y1, sy + 1) - max(y0, sy)
                for sx in range(int(x0), min(sw, math.ceil(x1))):
                    wx = min(x1, sx + 1) - max(x0, sx)
                    ch = grid[sy][sx]
                    weight[ch] = weight.get(ch, 0) + wx * wy
            solid = {k: v for k, v in weight.items() if k != "."}
            if sum(solid.values()) < 0.5 * (x1 - x0) * (y1 - y0):
                line.append(None)
                continue
            best = max(solid.values())
            tied = [k for k, v in solid.items() if v > best - 1e-9]
            line.append(SPRITE_RGB[min(tied, key=lambda k: freq[k])])
        rows.append(line)
    _sprite_cache[key] = rows
    return rows

def _sprite_pixels(name, frame, th):
    """Enemy sprite pixels with a dark outline (same total height as before)."""
    if not SPRITE_OUTLINE:
        return _sprite_pixels_raw(name, frame, th)
    key = ("outlined", name, frame, th)
    if key not in _sprite_cache:
        _sprite_cache[key] = outline_pixels(_sprite_pixels_raw(name, frame, th - 2), SPRITE_OUTLINE)
    return _sprite_cache[key]

def draw_sprite(cv, x0, y0, pixels, tint=None):
    for row in range(0, len(pixels), 2):
        top_row = pixels[row]
        bottom_row = pixels[row + 1] if row + 1 < len(pixels) else [None] * len(top_row)
        for col in range(len(top_row)):
            top, bottom = top_row[col], bottom_row[col]
            if tint:
                top = tint_color(top, *tint) if top is not None else None
                bottom = tint_color(bottom, *tint) if bottom is not None else None
            if top is None and bottom is None:
                continue
            x, y = x0 + col, y0 + row // 2
            if BG_REGION is not None:
                if top is None:
                    top = _bg_pixel(x, y, 0)
                if bottom is None:
                    bottom = _bg_pixel(x, y, 1)
            if top is not None and top == bottom:
                cv.put(x, y, "\u2588", px_fg(top))
            elif top is not None and bottom is not None:
                cv.put(x, y, "\u2580", px_fg(top) + px_bg(bottom))
            elif top is not None:
                cv.put(x, y, "\u2580", px_fg(top))
            else:
                cv.put(x, y, "\u2584", px_fg(bottom))

if _png_files_exist("champion"):
    MAP_SPRITE[3] = "champion"

def sprite_rows(name=None):
    if name == "champion":                             # the final boss is drawn bigger than the others
        return min(SPRITE_MAX_ROWS + 6, max(6, FLOOR - 4))
    return min(SPRITE_MAX_ROWS, max(6, FLOOR - 4))

def enemy_height(st):
    if st["map"] in MAP_SPRITE:
        return sprite_rows(MAP_SPRITE[st["map"]])
    return ENEMY_H * SY

def draw_sprite_enemy(cv, s, gt, st):
    name = MAP_SPRITE[st["map"]]
    pose = current_pose(s, gt)
    rows = sprite_rows(name)
    pixels = _sprite_pixels(name, POSE_FRAME[name][pose], rows * 2)
    width = len(pixels[0])
    dx = [-1, 0, 1, 0][int(gt * 3) % 4]
    dy = 0
    tint = None
    if pose == "windup":
        dx = (int(gt * 25) % 3) - 1
        tint = ((255, 40, 40), 0.25)
    elif pose == "punch":
        dx, dy = 0, 1
    elif pose == "hurt":
        if s["phase"] == "end":
            dx = 0
            tint = ((0, 0, 0), 0.35)
        else:
            flick = int(gt * 24) % 2
            dx = 2 if flick else -2
            tint = ((255, 255, 255), 0.55) if flick else None
    if name == "champion" and tint is None:            # slow red menace glow on the boss
        tint = ((255, 0, 0), 0.04 + 0.06 * (1 + math.sin(gt * 3)) / 2)
    x0 = (W - width) // 2 + dx
    y0 = FLOOR - rows + dy
    draw_sprite(cv, x0, y0, pixels, tint)
    cx = x0 + width // 2
    if pose == "windup":
        cv.put(cx - 2, y0 - 1, "! ! !", c(196) + BOLD)
    elif pose == "hurt":
        cv.put(x0 + 1, y0 + 2, "*", c(226) + BOLD)
        cv.put(x0 + width - 2, y0 + 4, "*", c(226) + BOLD)
        cv.put(cx - 1, y0 - 1, "x x", c(226) + BOLD)

def enemy_style(ch):
    return c(196) + BOLD if ch == "@" else c(180)

crowd_cache = {}

def crowd_rows(width):
    if width not in crowd_cache:
        rng = random.Random(7)
        crowd_cache[width] = ["".join(rng.choice("oO.o.") for _ in range(width)) for _ in range(3)]
    return crowd_cache[width]

def _bricks(cv, x0, x1, y0, y1):
    for y in range(y0, y1 + 1):
        offset = 0 if y % 2 == 0 else 2
        cv.put(x0, y, ("|###" * 20)[offset:offset + (x1 - x0 + 1)], c(238))

def _bg_street(cv, gt):
    bw = 10 + (W - 78) // 4
    _bricks(cv, 1, bw, 3, FLOOR - 1)
    _bricks(cv, W - 1 - bw, W - 2, 3, FLOOR - 1)
    sign_y = 3 + (FLOOR - 3) // 3
    cv.put(2, sign_y, "PUNCH", c(124) + BOLD)
    cv.put(2, sign_y + 1, "TYPE!", c(124) + BOLD)
    lamp_x = bw + 5
    lamp = c(226) + BOLD if int(gt * 7) % 23 else c(94)
    cv.put(lamp_x, 4, ".(*).", lamp)
    for y in range(5, FLOOR):
        cv.put(lamp_x + 2, y, "|", c(240))
    trash_x = W - bw - 15
    cv.put(trash_x, FLOOR - 3, ".-----------.", c(240))
    cv.put(trash_x, FLOOR - 2, "|   TRASH   |", c(240))
    cv.put(trash_x, FLOOR - 1, "'-----------'", c(240))

def _bg_underground(cv, gt):
    cv.put(1, 3, "=" * (W - 2), c(240))
    cv.put(1, 4, "=" * (W - 2), c(238))
    for x in (W * 12 // 78, W - 15):
        for y in range(5, FLOOR):
            cv.put(x, y, "[]", c(240))
    for x in (W * 22 // 78, W - 24):
        cv.put(x, 5, "|", c(240))
        cv.put(x - 1, 6, "(o)", c(226) + BOLD)
    cv.put(W * 32 // 78, 5 + int(gt * 8) % (FLOOR - 6), "'", c(39))

def _bg_ring(cv):
    for i, row in enumerate(crowd_rows(W - 2)):
        cv.put(1, 3 + i, row, c(238 + i))
    for x in (3, W - 6):
        for y in range(6, FLOOR):
            cv.put(x, y, "[#]", c(240))
    for y, color in ((FLOOR - 7, 196), (FLOOR - 5, 255), (FLOOR - 3, 33)):
        cv.put(1, y, "=" * (W - 2), c(color))

BG_FILES = {1: "bg_1", 2: "bg_2", 3: "bg_3"}
_bg_cache = {}

def _bg_pixel(x, y, half):
    bx, by, px = BG_REGION
    r = (y - by) * 2 + half
    col = x - bx
    if 0 <= r < len(px) and 0 <= col < len(px[0]):
        return px[r][col]
    return None

BG_VIGNETTE = 0.40       # 0 = off, 0.4 = corners 40% darker

def _build_bg(map_id, cols, rows):
    path = asset_path(*ASSET_NAMES.get(BG_FILES.get(map_id, ""), ()))
    if Image is None or not path:
        return None
    img = Image.open(path).convert("RGB")
    ph = rows * 2
    scale = max(cols / img.width, ph / img.height)
    nw, nh = max(cols, round(img.width * scale)), max(ph, round(img.height * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - cols) // 2, (nh - ph) // 2
    img = img.crop((left, top, left + cols, top + ph))
    img = img.quantize(colors=24, dither=0).convert("RGB")
    data = list(img.getdata())
    pixels = [data[y * cols:(y + 1) * cols] for y in range(ph)]
    if BG_VIGNETTE:                                      # darker toward the edges, in 6 steps
        for y in range(ph):                              # (stepped, so it keeps the pixel-art look)
            dy = (y - ph / 2) / (ph / 2)
            row = []
            for x in range(cols):
                dx = (x - cols / 2) / (cols / 2)
                d = min(1.0, math.sqrt(0.8 * dx * dx + 0.6 * dy * dy))
                k = 1.0 - BG_VIGNETTE * int(d * d * 6) / 5
                p = pixels[y][x]
                row.append((int(p[0] * k), int(p[1] * k), int(p[2] * k)))
            pixels[y] = row
    chs, sts, bgs = [], [], []
    for r in range(rows):
        top_row, bot_row = pixels[r * 2], pixels[r * 2 + 1]
        chs.append(["\u2580"] * cols)
        sts.append([px_fg(t) + px_bg(b) for t, b in zip(top_row, bot_row)])
        bgs.append([px_bg(tuple((t[i] + b[i]) // 2 for i in range(3)))
                    for t, b in zip(top_row, bot_row)])
    return pixels, chs, sts, bgs

def _draw_image_bg(cv, map_id):
    global BG_REGION
    BG_REGION = None
    cols, rows = W - 2, H - 8
    if cols < 2 or rows < 2:
        return False
    key = (map_id, cols, rows, SPRITE_TRUECOLOR)
    if key not in _bg_cache:
        _bg_cache[key] = _build_bg(map_id, cols, rows)
    built = _bg_cache[key]
    if built is None:
        return False
    pixels, chs, sts, bgs = built
    for r in range(rows):
        y = 3 + r
        cv.ch[y][1:1 + cols] = chs[r]
        cv.st[y][1:1 + cols] = sts[r]
        cv.bg[y][1:1 + cols] = bgs[r]
    BG_REGION = (1, 3, pixels)
    return True

def draw_background(cv, map_id, gt):
    if _draw_image_bg(cv, map_id):
        return
    cv.put(1, FLOOR, "_" * (W - 2), c(240))
    for y in range(FLOOR + 1, H - 5):
        for x in range(1 + (y % 2) * 2, W - 1, 4):
            cv.put(x, y, ".", c(238))
    if map_id == 2:
        _bg_underground(cv, gt)
    elif map_id == 3:
        _bg_ring(cv)
    else:
        _bg_street(cv, gt)

def _lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

def hp_bar(cv, x, y, shown, maximum, width=30, kind="player", real=None, flash=False):
    """Block bar with a gradient. `shown` is the eased value; cells between `real` and `shown`
    are drawn orange (the 'chip' of recent damage). `flash` turns the bar white for a moment."""
    frac = max(0.0, min(1.0, shown / maximum)) if maximum else 0.0
    fill = int(frac * width + 0.5)
    if shown > 0 and fill == 0:
        fill = 1
    real_fill = fill
    if real is not None and maximum:
        real_fill = int(max(0.0, min(1.0, real / maximum)) * width + 0.5)
        if real > 0 and real_fill == 0:
            real_fill = 1
        real_fill = min(real_fill, fill)
    if kind == "player":                                   # green -> yellow -> red as HP drops
        base = (60, 220, 90) if frac > 0.5 else ((240, 210, 60) if frac > 0.25 else (235, 55, 55))
    cv.put(x, y, "[", c(240))
    for i in range(width):
        if i < fill:
            if i >= real_fill:
                rgb = (255, 165, 50)
            elif kind == "enemy":                          # dark red -> bright red along the bar
                rgb = _lerp((150, 20, 25), (255, 75, 60), i / max(1, width - 1))
            else:
                rgb = base
            if flash:
                rgb = _lerp(rgb, (255, 255, 255), 0.65)
            cv.put(x + 1 + i, y, "\u2588", px_fg(rgb))
        else:
            cv.put(x + 1 + i, y, "\u2591", px_fg((70, 70, 82)))
    cv.put(x + width + 1, y, "]", c(240))

BIG_FONT = {
    "A": " ### |#   #|#####|#   #|#   #", "B": "#### |#   #|#### |#   #|#### ",
    "C": " ####|#    |#    |#    | ####", "D": "#### |#   #|#   #|#   #|#### ",
    "E": "#####|#    |#### |#    |#####", "F": "#####|#    |#### |#    |#    ",
    "G": " ####|#    |# ###|#   #| ####", "H": "#   #|#   #|#####|#   #|#   #",
    "I": "#####|  #  |  #  |  #  |#####", "J": "  ###|    #|    #|#   #| ### ",
    "K": "#   #|#  # |###  |#  # |#   #", "L": "#    |#    |#    |#    |#####",
    "M": "#   #|## ##|# # #|#   #|#   #", "N": "#   #|##  #|# # #|#  ##|#   #",
    "O": " ### |#   #|#   #|#   #| ### ", "P": "#### |#   #|#### |#    |#    ",
    "Q": " ### |#   #|# # #|#  ##| ####", "R": "#### |#   #|#### |#  # |#   #",
    "S": " ####|#    | ### |    #|#### ", "T": "#####|  #  |  #  |  #  |  #  ",
    "U": "#   #|#   #|#   #|#   #| ### ", "V": "#   #|#   #|#   #| # # |  #  ",
    "W": "#   #|#   #|# # #|## ##|#   #", "X": "#   #| # # |  #  | # # |#   #",
    "Y": "#   #| # # |  #  |  #  |  #  ", "Z": "#####|   # |  #  | #   |#####",
}

def big_letter_rows(ch):
    """A key as 5 rows of 10 columns (each font pixel is 2 cells wide so it looks square)."""
    glyph = BIG_FONT.get(ch.upper())
    if glyph is None:
        return [" " * 10] * 2 + [(" " + ch + " ").center(10)] + [" " * 10] * 2
    return ["".join("\u2588\u2588" if px == "#" else "  " for px in row) for row in glyph.split("|")]

def number(v):
    return str(int(round(v)))

def hp_text(v, m):
    return f"{max(0, int(v + 0.999))}/{int(m)}"

def current_pose(s, gt):
    phase = s["phase"]
    if phase == "prompt":
        left = s["window"] - (gt - s["t0"])
        return "windup" if left <= s["window"] * 0.35 else "idle"
    if phase == "anim":
        p = (gt - s["t0"]) / s["dur"]
        if s["kind"] == "enemy":
            return "punch"
        return "hurt" if p >= 0.3 else "idle"
    if phase == "end" and s["won"]:
        return "hurt"
    return "idle"

def draw_enemy(cv, s, gt, st):
    if st["map"] in MAP_SPRITE:
        draw_sprite_enemy(cv, s, gt, st)
        return
    pose = current_pose(s, gt)
    rows = ENEMY_IDLE
    dx = [-1, 0, 1, 0][int(gt * 3) % 4]
    dy = 0
    if pose == "windup":
        rows = ENEMY_WINDUP
        dx = (int(gt * 25) % 3) - 1
    elif pose == "punch":
        rows = ENEMY_WINDUP
        dx, dy = 0, 1
    elif pose == "hurt":
        rows = ENEMY_HURT
        dx = 0 if s["phase"] == "end" else (2 if int(gt * 24) % 2 else -2)
    x0 = (W - ENEMY_W * SX) // 2 + dx * SX
    y0 = FLOOR - ENEMY_H * SY + dy * SY
    for i, row in enumerate(scale_art(rows, SX, SY)):
        cv.put_solid(x0, y0 + i, row, enemy_style)
    if pose == "windup":
        cv.put(x0 + 14 * SX, y0 - 1, "! ! !", c(196) + BOLD)
    elif pose == "hurt":
        cv.put(x0 + 3 * SX, y0 + SY, "*", c(226) + BOLD)
        cv.put(x0 + 28 * SX, y0 + 2 * SY, "*", c(226) + BOLD)
        cv.put(x0 + 14 * SX, y0 - 1, "x x", c(226) + BOLD)
    elif pose == "punch":
        p = (gt - s["t0"]) / s["dur"]
        if p > 0.15:
            fist = scale_art(FIST_BIG, SX, SY)
            fx = (W - len(fist[0])) // 2
            fy = FLOOR - ENEMY_H * SY + 6 * SY
            for i, row in enumerate(fist):
                cv.put_solid(fx, fy + i, row, enemy_style)

def draw_gloves_ascii(cv, s, gt, st):
    if st["glove"] == 4:
        style = c(FIRE[int(gt * 8) % len(FIRE)]) + BOLD
    else:
        style = c(GLOVE_COLOR.get(st["glove"], 196)) + BOLD
    art = list(GLOVE)
    if st["glove"] in GLOVE_TOP:
        art[0] = GLOVE_TOP[st["glove"]]
    art = scale_art(art, SX, SY)
    gw = GLOVE_W * SX
    cx = W // 2
    top = FLOOR - enemy_height(st)

    pos = {"L": (3, FLOOR + int(gt * 2) % 2), "R": (W - 3 - gw, FLOOR + (int(gt * 2) + 1) % 2)}
    punching = None
    if s["phase"] == "anim" and s["kind"] == "player":
        p = (gt - s["t0"]) / s["dur"]
        if p < 0.4:
            t = p / 0.4
        elif p < 0.6:
            t = 1.0
        else:
            t = max(0.0, 1.0 - (p - 0.6) / 0.4)
        side = s["side"]
        rx, ry = pos[side]
        tx, ty = (cx - gw - 1, top + 2 * SY) if side == "L" else (cx + 1, top + 2 * SY)
        pos[side] = (int(rx + (tx - rx) * t), int(ry + (ty - ry) * t))
        punching = side
        if 0.3 <= p <= 0.75:
            word = "CRIT!" if s["crit"] else "POW!"
            cv.put(cx - 4, top - 1, f"* {word} *", c(226) + BOLD)
            cv.put(cx - 9, top + SY, "\\ | /", c(226))
            cv.put(cx + 7, top + 3 * SY, "* !", c(226))
    elif s["phase"] == "anim" and s["kind"] == "enemy":
        p = (gt - s["t0"]) / s["dur"]
        if 0.2 <= p <= 0.7:
            pos["L"] = (pos["L"][0] - 2 * SX, pos["L"][1])
            pos["R"] = (pos["R"][0] + 2 * SX, pos["R"][1])

    for side in ("L", "R"):
        if side == punching:
            continue
        for i, row in enumerate(art):
            cv.put_solid(pos[side][0], pos[side][1] + i, row, style)
    if punching:
        x, y = pos[punching]
        for i, row in enumerate(art):
            cv.put_solid(x, y + i, row, style)

def draw_gloves(cv, s, gt, st):
    global _glove_cols_now
    rows = 6 * SY + 3
    sprites = glove_sprites(st["glove"], rows)
    if sprites is None:                                # images missing: keep the old ASCII gloves
        _glove_cols_now = None
        draw_gloves_ascii(cv, s, gt, st)
        return
    gw = {side: len(sprites[side][0]) for side in "LR"}
    _glove_cols_now = max(gw.values())
    tint = None
    if st["glove"] == 4:
        tint = ((255, 120, 0), 0.10 + 0.10 * (1 + math.sin(gt * 6)) / 2)
    cx = W // 2
    top = FLOOR - enemy_height(st)
    base_y = FLOOR + 6 * SY - rows

    pos = {"L": (6, base_y + int(gt * 2) % 2), "R": (W - 6 - gw["R"], base_y + (int(gt * 2) + 1) % 2)}
    punching = None
    if s["phase"] == "anim" and s["kind"] == "player":
        p = (gt - s["t0"]) / s["dur"]
        if p < 0.4:
            t = p / 0.4
        elif p < 0.6:
            t = 1.0
        else:
            t = max(0.0, 1.0 - (p - 0.6) / 0.4)
        side = s["side"]
        rx, ry = pos[side]
        tx, ty = (cx - gw["L"] - 1, top + 2 * SY) if side == "L" else (cx + 1, top + 2 * SY)
        pos[side] = (int(rx + (tx - rx) * t), int(ry + (ty - ry) * t))
        punching = side
        if 0.3 <= p <= 0.75:
            word = "CRIT!" if s["crit"] else "POW!"
            cv.put(cx - 4, top - 1, f"* {word} *", c(226) + BOLD)
            cv.put(cx - 9, top + SY, "\\ | /", c(226))
            cv.put(cx + 7, top + 3 * SY, "* !", c(226))
    elif s["phase"] == "anim" and s["kind"] == "enemy":
        p = (gt - s["t0"]) / s["dur"]
        if 0.2 <= p <= 0.7:
            pos["L"] = (pos["L"][0] - 2 * SX, pos["L"][1])
            pos["R"] = (pos["R"][0] + 2 * SX, pos["R"][1])

    for side in ("L", "R"):
        if side != punching:
            draw_sprite(cv, pos[side][0], pos[side][1], sprites[side], tint)
    if punching:
        draw_sprite(cv, pos[punching][0], pos[punching][1], sprites[punching], tint)

def centered(cv, y, text, style):
    cv.put((W - len(text)) // 2, y, text, style)

_tip_done = False        # the "how to play" line disappears after the first fight

def draw_prompt(cv, s, gt, st):
    if s["phase"] == "prompt":
        left_t = max(0.0, s["window"] - (gt - s["t0"]))
        frac = left_t / s["window"] if s["window"] else 0.0
        color = 46 if frac > 0.5 else (226 if frac > 0.25 else 196)
        pw, ph = 22, 9
        enemy_half = 14 if st["map"] in MAP_SPRITE else (ENEMY_W * SX) // 2
        x = max(W - 3 - pw, W // 2 + enemy_half + 2)
        pw = min(pw, W - 2 - x)
        if pw >= 16:
            y = max(3, FLOOR - 3 - ph)
            cv.panel(x, y, pw, ph, c(color))
            cv.put(x + (pw - 7) // 2, y, " PRESS ", c(245) + BOLD)
            urgent = frac < 0.25 and int(gt * 8) % 2
            for i, row in enumerate(big_letter_rows(s["letter"])):
                cv.put(x + (pw - 10) // 2, y + 1 + i, row, c(15 if urgent else color) + BOLD)
            label = f"{left_t:.1f} sec"
            cv.put(x + (pw - len(label)) // 2, y + 6, label, c(color) + BOLD)
            bw = pw - 4
            fill = int(frac * bw + 0.5)
            cv.put(x + 2, y + 7, "\u2588" * fill, c(color))
            cv.put(x + 2 + fill, y + 7, "\u2591" * (bw - fill), c(238))
            return
        # terminal too narrow for the side panel: small centred prompt
        y0 = FLOOR + 2 * SY
        cv.panel((W - 26) // 2, y0 - 1, 26, 4, c(color))
        centered(cv, y0, f"[ {s['letter']} ]   {left_t:.1f} sec", c(color) + BOLD)
        bw = 20
        fill = int(frac * bw + 0.5)
        centered(cv, y0 + 1, "\u2588" * fill + "\u2591" * (bw - fill), c(color))
    elif gt < s["msg_until"]:
        y0 = FLOOR + 2 * SY
        width = min(W - 4, max(len(s["msg"]), len(s["msg2"])) + 6)
        cv.panel((W - width) // 2, y0 - 1, width, 5 if s["msg2"] else 3, c(240))
        centered(cv, y0, s["msg"], s["msg_style"])
        if s["msg2"]:
            centered(cv, y0 + 2, s["msg2"], c(250))

def add_floater(s, gt, text, kind, color, dx=0, life=1.0):
    s.setdefault("floaters", []).append(
        {"text": text, "kind": kind, "color": color, "dx": dx, "t0": gt, "life": life})

def draw_floaters(cv, s, gt, st):
    """Damage numbers that rise and fade: over the enemy for hits, over the HUD for hits taken."""
    keep = []
    for f in s.get("floaters", []):
        age = gt - f["t0"]
        if age > f["life"]:
            continue
        keep.append(f)
        rise = int(age * 9)
        if f["kind"] == "enemy":
            y = max(4, FLOOR - enemy_height(st) - 2) - rise
        else:
            y = H - 7 - rise
        y = max(3, y)
        style = c(f["color"]) + BOLD if age < f["life"] * 0.7 else c(245)
        cv.tag(W // 2 + f["dx"] - len(f["text"]) // 2, y, f["text"], style)
    s["floaters"] = keep

def draw_combo(cv, s, gt):
    combo = s.get("combo", 0)
    if combo < 2:
        return
    color = 15 if combo < 5 else (226 if combo < 10 else (208 if combo < 15 else 196))
    bump = gt - s.get("combo_t", -9.0) < 0.15            # tiny flash each time it goes up
    cv.tag(4, 4, f" COMBO x{combo} ", c(15 if bump else color) + BOLD)

def shake_canvas(cv, d):
    """Slide the fight picture 1 column left/right (the frame and HUD stay put)."""
    for y in range(3, H - 5):
        for arr in (cv.ch[y], cv.st[y], cv.bg[y]):
            inner = arr[1:W - 1]
            k = d % len(inner)
            if k:
                arr[1:W - 1] = inner[-k:] + inner[:-k]

def put_segments(cv, y, segs):
    x = (W - sum(len(t) for t, _ in segs)) // 2
    for text, style in segs:
        cv.put(x, y, text, style)
        x += len(text)

def draw_end_box(cv, s, gt, st):
    won = s["won"]
    color = c(46) + BOLD if won else c(196) + BOLD
    lines = ["+------------------------+",
             "|        K . O .         |",
             "|" + ("YOU WIN!" if won else "YOU LOSE!").center(24) + "|",
             "|" + ("PRESS ENTER" if gt - s["t0"] > 1.0 else "").center(24) + "|",
             "+------------------------+"]
    top = FLOOR - enemy_height(st) + 3 * SY
    for i, line in enumerate(lines):
        cv.put((W - len(line)) // 2, top + i, line, color)

def draw_frame(cv, border):
    cv.put(0, 0, "+" + "=" * (W - 2) + "+", border)
    cv.put(0, H - 1, "+" + "=" * (W - 2) + "+", border)
    for y in (2, H - 5):
        cv.put(0, y, "+" + "-" * (W - 2) + "+", c(240))
        cv.put(0, y, "+", border)
        cv.put(W - 1, y, "+", border)
    for y in range(1, H - 1):
        cv.put(0, y, "|", border)
        cv.put(W - 1, y, "|", border)

def render(s, st, gt, size):
    global _tip_done
    cols, rows = size
    set_layout(cols, rows)
    cv = Canvas(W, H)
    draw_background(cv, st["map"], gt)
    draw_enemy(cv, s, gt, st)
    draw_gloves(cv, s, gt, st)
    if gt < s.get("shake_until", 0.0):
        shake_canvas(cv, 1 if int(gt * 30) % 2 else -1)
    draw_prompt(cv, s, gt, st)
    draw_floaters(cv, s, gt, st)
    draw_combo(cv, s, gt)
    if s["phase"] == "end":
        _tip_done = True
        draw_end_box(cv, s, gt, st)

    bar_w = max(30, W - 48)
    cv.put(2, 1, ("FINAL BOSS: " if st["map"] == 3 and MAP_SPRITE.get(3) == "champion" else "ENEMY: ") + (MAP_ENEMY_NAMES.get(st["map"]) or ENEMY_NAMES.get(st["difficulty"], "ENEMY")), c(15) + BOLD)
    hp_bar(cv, 30, 1, s["shown_e"], st["enemy_max"], bar_w, "enemy", st["enemy"], gt < s.get("flash_e", 0.0))
    cv.put(33 + bar_w, 1, hp_text(s["shown_e"], st["enemy_max"]), c(250))

    cv.put(2, H - 4, "PLAYER: PIPOO", c(15) + BOLD)
    hp_bar(cv, 30, H - 4, s["shown_p"], st["player_max"], bar_w, "player", st["player"], gt < s.get("flash_p", 0.0))
    cv.put(33 + bar_w, H - 4, hp_text(s["shown_p"], st["player_max"]), c(250))

    label, dim = c(245), c(250)
    segs = [("HITS ", label), (str(st["phit"]), c(46) + BOLD),
            ("   TAKEN ", label), (str(st["ehit"]), c(196) + BOLD if st["ehit"] else dim),
            ("   COMBO ", label), (f"x{s.get('combo', 0)}", c(226) + BOLD),
            ("   CRITS ", label), (str(st["crits"]), c(214) + BOLD)]
    if s["wrong"]:
        segs += [("   WRONG ", label), (str(s["wrong"]), c(196) + BOLD)]
    if s["slow"]:
        segs += [("   SLOW ", label), (str(s["slow"]), c(196) + BOLD)]
    segs += [("   LAST ", label), (s["last"], dim)]
    put_segments(cv, H - 3, segs)
    if not _tip_done:
        centered(cv, H - 2, "Press the letter shown before the timer runs out! Wrong key = you get hit.",
                 c(240))

    flash = gt < s["flash_until"]
    draw_frame(cv, c(196) + BOLD if flash else c(208))

    diff = DIFF_NAMES.get(st["difficulty"], "")
    cv.put(3, 2, f" {diff}  KEYS: {st['keys']} ", c(245))
    need = st["ult_need"]
    ready = st["ult"] >= need
    have = min(st["ult"], need)
    meter = "\u2588" * have + "\u2591" * max(0, need - have)
    pulse = ready and int(gt * 4) % 2
    cv.put(W - 22, H - 5, " ULT [", c(245))
    cv.put(W - 16, H - 5, meter, (c(15 if pulse else 226) + BOLD) if ready else (c(214) if have else c(240)))
    cv.put(W - 16 + len(meter), H - 5, "] " + ("READY!" if ready else ""),
           (c(15 if pulse else 226) + BOLD) if ready else c(245))

    return HOME + (CLEAR_EOL + "\n").join(cv.lines()) + CLEAR_EOL + CLEAR_DOWN

def new_scene(st):
    return {
        "phase": "intro", "t0": 0.0, "until": 0.0, "dur": 0.4, "kind": "", "side": "R",
        "letter": "", "last_letter": "", "window": 2.0, "landed": 0,
        "msg": ("FINAL BOSS!  GET READY!" if st["map"] == 3 and MAP_SPRITE.get(3) == "champion" else "GET READY!"), "msg_style": c(250) + BOLD, "msg2": "", "msg_until": 99.0,
        "flash_until": 0.0, "wrong": 0, "slow": 0, "last": "-", "crit": False, "won": False,
        "shown_e": float(st["enemy"]), "shown_p": float(st["player"]),
        "combo": 0, "best_combo": 0, "combo_t": -9.0, "floaters": [],
        "shake_until": 0.0, "flash_e": 0.0, "flash_p": 0.0,
    }

def set_msg(s, gt, text, style, msg2="", seconds=1.2):
    s["msg"] = text
    s["msg_style"] = style
    s["msg2"] = msg2
    s["msg_until"] = gt + seconds

def reaction_window(st, landed):
    base = st["react"]
    return max(base * 0.7, base * (1 - 0.02 * landed))

def start_gap(s, gt):
    s["phase"] = "gap"
    s["until"] = gt + random.uniform(0.5, 0.9)

def start_prompt(s, st, gt):
    pool = [ch for ch in st["keys"] if ch != s["last_letter"]] or list(st["keys"])
    s["letter"] = random.choice(pool)
    s["last_letter"] = s["letter"]
    s["window"] = reaction_window(st, s["landed"])
    s["phase"] = "prompt"
    s["t0"] = gt
    s["msg_until"] = 0.0
    flush_keys()

def do_hit(hooks, s, gt):
    res = hooks["player_hit"]()
    dmg = number(res["damage"])
    punch.play()
    s["landed"] += 1
    s["last"] = "-" + dmg
    s["crit"] = res["crit"]
    s["combo"] = s.get("combo", 0) + 1
    s["best_combo"] = max(s.get("best_combo", 0), s["combo"])
    s["combo_t"] = gt
    s["flash_e"] = gt + 0.18
    add_floater(s, gt, (f"-{dmg}!" if res["crit"] else f"-{dmg}"), "enemy",
                226 if (res["crit"] or res["ult"]) else 231, dx=random.randint(-5, 5), life=1.0)
    if res["crit"] or res["ult"]:
        s["shake_until"] = gt + 0.25
    s["side"] = "L" if s["side"] == "R" else "R"
    s["phase"], s["kind"], s["t0"], s["dur"] = "anim", "player", gt, 0.4

    if res["ult"]:
        extra = "+5 HP!" if res["heal"] else random.choice(SAY)
        if extra in voiceline:
            voiceline[extra].play()
        set_msg(s, gt, f"ULT: {res['ult']}!  -{dmg}", c(201) + BOLD, extra)
    elif res["crit"]:
        set_msg(s, gt, f"CRITICAL HIT!  -{dmg}", c(226) + BOLD)
    else:
       word = random.choice(HIT_WORDS)

       if word in voiceline:
        voiceline[word].play()

       set_msg(s, gt, f"{word}  -{dmg}", c(46) + BOLD)

def do_miss(hooks, s, gt, reason):
    res = hooks["enemy_hit"]()
    dmg = number(res["damage"])
    if reason == "wrong":
        s["wrong"] += 1
        text = "MISSED!  YOU GOT HIT!"
        hurt.play()
    else:
        hurt.play()
        s["slow"] += 1
        text = "TOO SLOW!  YOU GOT HIT!"
    s["last"] = "+" + dmg + " taken"
    s["phase"], s["kind"], s["t0"], s["dur"] = "anim", "enemy", gt, 0.45
    s["flash_until"] = gt + 0.35
    s["combo"] = 0
    s["flash_p"] = gt + 0.2
    s["shake_until"] = gt + 0.2
    add_floater(s, gt, f"-{dmg}", "player", 196, dx=random.randint(-6, 6), life=1.0)
    

    extra = random.choice(ESAY) if res["enraged"] else ""

    if extra in voiceline:
        voiceline[extra].play()

    set_msg(s, gt, f"{text}  -{dmg}", c(196) + BOLD, extra)

    

def update(hooks, s, gt, key):
    st = hooks["state"]()
    phase = s["phase"]
    bg.stop()
    if phase == "intro":
        if gt > 0.7:
            if not s.get("bell"):
                bell.play()
                s["bell"] = True
            set_msg(s, gt, "FIGHT!", c(226) + BOLD, "", 1.0)
        if gt > 1.2:
            start_gap(s, gt)
    elif phase == "gap":
        if gt >= s["until"]:
            start_prompt(s, st, gt)
    elif phase == "prompt":
        left = s["window"] - (gt - s["t0"])
        if 0 < left <= s["window"] * 0.35 and not s.get("ticked"):
            s["ticked"] = True
        if left <= 0:
            do_miss(hooks, s, gt, "slow")
        elif len(key) == 1 and key.isalpha():
            if key == s["letter"]:
            
                do_hit(hooks, s, gt)
            else:
                do_miss(hooks, s, gt, "wrong")
    elif phase == "anim":
        if gt - s["t0"] >= s["dur"]:
            st = hooks["state"]()
            if st["enemy"] <= 0 or st["player"] <= 0:
                s["phase"] = "end"
                s["won"] = st["enemy"] <= 0
                s["t0"] = gt
                flush_keys()
            else:
                if not s.get("roared") and st["enemy"] <= st["enemy_max"] * 0.25:
                    s["roared"] = True
                start_gap(s, gt)
    elif phase == "end":
        if gt - s["t0"] > 1.0 and key in ("\r", "\n"):
            s["phase"] = "done"

def ease_bars(s, st, dt):
    k = min(1.0, dt * 12)
    for name, real in (("shown_e", st["enemy"]), ("shown_p", st["player"])):
        s[name] += (real - s[name]) * k
        if abs(real - s[name]) < 0.5:
            s[name] = float(real)

def too_small(size):
    return size[0] < MIN_COLS or size[1] < MIN_ROWS

def fight_loop(hooks, s, out):
    last = time.monotonic()
    gt = 0.0
    size = None
    while True:
        now = time.monotonic()
        dt = min(now - last, 0.1)
        last = now

        new_size = tuple(shutil.get_terminal_size((MIN_COLS, MIN_ROWS)))
        if new_size != size:
            size = new_size
            out.write(CLEAR)
        if too_small(size):
            out.write(HOME + f"TERMINAL TOO SMALL - NEED {MIN_COLS}x{MIN_ROWS}, "
                      f"YOU HAVE {size[0]}x{size[1]}. FIGHT IS PAUSED." + CLEAR_EOL)
            out.flush()
            flush_keys()
            time.sleep(0.2)
            continue

        gt += dt
        key = read_key()
        if key == "\x03":
            raise KeyboardInterrupt
        update(hooks, s, gt, key)
        if s["phase"] == "done":
            return
        st = hooks["state"]()
        ease_bars(s, st, dt)
        out.write(render(s, st, gt, size))
        out.flush()

        spare = 1.0 / FPS - (time.monotonic() - now)
        if spare > 0:
            time.sleep(spare)

def can_animate():
    global REASON
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        REASON = ("this is not a real terminal. Open Command Prompt / PowerShell / "
                  "Windows Terminal and run:  python punch_type_combined.py")
        return False
    size = shutil.get_terminal_size((MIN_COLS, MIN_ROWS))
    if too_small(size):
        REASON = (f"your terminal is {size.columns}x{size.lines}; the fight needs at least "
                  f"{MIN_COLS}x{MIN_ROWS}. Maximize the window or reduce the font size.")
        return False
    return True

def run_combat(hooks):
    if not can_animate():
        return False
    enable_ansi_on_windows()
    s = new_scene(hooks["state"]())
    out = sys.stdout
    interrupted = False
    out.write(HIDE_CURSOR + CLEAR)
    out.flush()
    try:
        with raw_input_mode():
            flush_keys()
            fight_loop(hooks, s, out)
    except KeyboardInterrupt:
        interrupted = True
    finally:
        out.write(RESET + SHOW_CURSOR + CLEAR + HOME)
        out.flush()
        flush_keys()
    if interrupted:
        raise SystemExit
    return True

ult = 0
gold = 0
pdamage = 20
pdmg = 30

player = 100
ehit = 0
phit = 0
x = 1
has_spiked = 0
has_bomb = 0
has_lava = 0
crits = 0
map2 = 0
map3 = 0
choice4 = 0

def retry():
    global gold
    global gg
    global x
    global player
    global enemy
    global pdmg
    global map2
    global map3

    if enemy <= 0:
        if choice2 == 1:
            gol = 500
            gold += 500

        elif choice2 == 2:
            gol = 800
            gold += 800
        elif choice2 == 3:
            gol = 1000
            gold += 1000

        note = ""
        if choice2 == 3:
            if choice4 == 1:
                map2 = 1
                note = "CONGRATULATIONS, YOU'VE UNLOCKED UNDERGROUND MAP"
            elif choice4 == 2:
                map3 = 1
                note = "CONGRATULATIONS, YOU'VE UNLOCKED BOXING RING MAP"
            elif choice4 == 3:
                note = "CONGRATULATIONS, YOU ARE THE CHAMPION!!!"

        lamon = victory_screen(gol, note)
        match lamon:
            case 1:
                gg = 1
                player = 100
                enemy = hp
                pdmg = 30

            case 2:
                x = 1
                gg = 0
                player= 100
                enemy=hp
                pdmg=30
                return

            case 3:
                exit_screen()
                sys.exit()

    if player <= 0:
        if choice2 == 1:
            gol=150
            gold += 150
        elif choice2 == 2:
            gol = 300
            gold += 300
        elif choice2 == 3:
            gol = 450
            gold += 450
        gold += 50

        ulit = defeat_screen(gol)
        match ulit:
            case 1:
                gg = 1
                player = 100
                enemy = hp
                pdmg = 30
            case 2:
                x = 1
                gg = 0
                player = 100
                enemy = hp
                pdmg = 30
                return

def owned_set():
    owned = {"none"}
    if has_spiked == 1:
        owned.add("spiked")
    if has_bomb == 1:
        owned.add("bomb")
    if has_lava == 1:
        owned.add("lava")
    return owned

def shop():
    global gold
    global has_spiked
    global has_bomb
    global has_lava
    _, gold, owned = run_shop(gold, owned_set(), "none", mode="shop")
    has_spiked = 1 if "spiked" in owned else 0
    has_bomb = 1 if "bomb" in owned else 0
    has_lava = 1 if "lava" in owned else 0

GLOVE_NUMBER = {"none": 1, "spiked": 2, "bomb": 3, "lava": 4}
DIFFICULTY_STATS = {1: (500, 10), 2: (1000, 25), 3: (1500, 50)}

def prepare_fight():
    global gg
    global x
    global choice4
    global choice6
    while True:
        picked_map = run_map_select(gold, (1, map2, map3))
        if picked_map == 0:
            return False
        choice4 = picked_map
        picked, _, _ = run_shop(gold, owned_set(), "none", mode="pick")
        if picked is not None:
            choice6 = GLOVE_NUMBER[picked]
            gg = 1
            x = 0
            return True

def gamemenu():
    global x
    global enemy
    global hp
    global dmg
    global edmg
    global choice2
    global gg

    gg = 0
    if choice1 != 1:
        return
    while True:
        choice2 = run_difficulty_menu()
        if choice2 not in (1, 2, 3):
            return
        hp, dmg = DIFFICULTY_STATS[choice2]
        enemy = hp
        edmg = dmg
        if prepare_fight():
            return

def fight_classic():
    global ult
    global ehit
    global phit

    ult = 0
    ehit = 0
    phit = 0
    d = DIFFICULTIES[choice2 - 1]
    window = float(d["time"].rstrip("s"))
    while player > 0 and enemy > 0 and gg == 1:
        letter = random.choice(d["keys"])
        print("ENEMY:", enemy, "| PLAYER:", player)
        print(d["name"])
        print(letter)
        start = time.time()
        answer = input().strip().upper()
        if time.time() - start <= window and answer == letter:
            res = combat_player_hit()
            if res["ult"]:
                print("ULT ACTIVATED -", res["ult"])
            print("CRITICAL!!!" if res["crit"] else "NICE!", "-", number(res["damage"]))
        else:
            res = combat_enemy_hit()
            print("MISSED -", number(res["damage"]))
        print()

ULT_NEED = {1: 3, 2: 3, 3: 3, 4: 5}

def combat_state():
    d = DIFFICULTIES[choice2 - 1]
    return {"player": player, "player_max": 100, "enemy": enemy, "enemy_max": hp,
            "ult": ult, "ult_need": ULT_NEED[choice6], "phit": phit, "ehit": ehit,
            "crits": crits, "difficulty": choice2, "map": choice4, "glove": choice6,
            "keys": d["keys"], "react": float(d["time"].rstrip("s"))}

def combat_player_hit():
    global ult
    global enemy
    global player
    global phit
    global pdamage
    global pdmg
    global crits

    crit = random.randint(1, 100)
    crit_hit = False
    ult_name = ""
    heal = 0

    if choice6 == 1:
        pdamage = 20
        if ult >= 3:
            ult_name = ULT_NAMES[1]
            pdamage *= 2
            ult1.play()
            

    elif choice6 == 2:
        pdamage = 20
        if crit <= 25:
            pdamage *= 3
            crit_hit = True
            criit.play()
            
        if ult >= 3:
            ult_name = ULT_NAMES[2]
            pdamage *= 2.5
            ult = 2
            ult2.play()
            

            
    elif choice6 == 3:
        pdamage = 20 * 2
        if ult >= 3:
            ult_name = ULT_NAMES[3]
            pdamage *= 5
            ult = 0
            player += 5
            heal = 5
            ult3.play()
    elif choice6 == 4:
        pdamage = 20 * 1.5
        if crit <= 30:
            pdamage = pdmg * 3
            crit_hit = True
            criit.play()
        if ult >= 5:
            ult_name = ULT_NAMES[4]
            pdmg += 30 * .30
            ult = 4
            ult4.play()

    ult += 1
    if choice6 == 4 and ult >= 5 and not crit_hit:
        damage = pdmg
    else:
        damage = pdamage
    if crit_hit:
        crits += 1
    enemy -= damage
    phit += 1
    return {"damage": damage, "crit": crit_hit, "ult": ult_name, "heal": heal}

def combat_enemy_hit():
    global player
    global ehit
    global ult
    global pdmg

    dmg = edmg
    enraged = enemy <= hp * 0.25
    if enraged:
        dmg = edmg * 2
    player -= dmg
    ehit += 1
    ult = 0
    pdmg = 30
    return {"damage": dmg, "enraged": enraged}

COMBAT_HOOKS = {"state": combat_state, "player_hit": combat_player_hit,
                "enemy_hit": combat_enemy_hit}

def fight():
    global ult
    global ehit
    global phit

    ult = 0
    ehit = 0
    phit = 0

    if choice4==1:
        stret.play()
    if not run_combat(COMBAT_HOOKS):
        print("(First-person view is off: " + REASON + ")")
        fight_classic()

def clear_screen():
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")

def show_centered(lines, extra=0):
    size = shutil.get_terminal_size((80, 24))
    width = max(len(line) for line in lines)
    left = max(0, (size.columns - width) // 2)
    top = max(0, (size.lines - len(lines) - extra) // 2)
    clear_screen()
    print("\n" * top, end="")
    for line in lines:
        print((" " * left + line)[:size.columns - 1])
    return left

def box_row(text, width):
    return "|" + text[:width].center(width) + "|"

def stat_row(label, value, width):
    indent = max(0, (width - 26) // 2)
    text = " " * indent + label.ljust(16) + str(value).rjust(10)
    return "|" + text.ljust(width)[:width] + "|"

def victory_screen(earned, note):
    animated = run_victory_screen(gold, earned, phit, ehit, crits, note)
    if animated is not None:
        return animated
    trophy = [
        "   .-=======-.   ",
        "  ( |  K.O.  | )  ",
        "   '-.     .-'   ",
        "      |   |      ",
        "     _|___|_     ",
        "    |_______|    ",
    ]
    message = ""
    while True:
        size = shutil.get_terminal_size((80, 24))
        width = max(30, min(52, size.columns - 2))
        border = "+" + "-" * width + "+"
        lines = [border, box_row("Y O U   W I N !", width)]
        if size.lines >= 26:
            lines += [box_row(row.ljust(19), width) for row in trophy]
        lines += [box_row(note, width), border]
        lines += [stat_row("HITS GIVEN", phit, width),
                  stat_row("HITS TAKEN", ehit, width),
                  stat_row("CRITICAL HITS", crits, width),
                  stat_row("GOLD EARNED", "+" + str(earned) + " G", width),
                  border]
        lines += [box_row("1. RETRY", width), box_row("2. MENU", width),
                  box_row("3. EXIT", width), border]
        lines += [box_row(message, width), border]
        left = show_centered(lines, 2)
        try:
            answer = input(" " * left + "ENTER CHOICE: ").strip()
        except (EOFError, KeyboardInterrupt):
            return 3
        if answer in ("1", "2", "3"):
            return int(answer)
        message = "INVALID CHOICE. TYPE 1, 2 OR 3."

def defeat_screen(earned):
    lose.play()
    animated = run_defeat_screen(gold, earned, phit, ehit, crits)
    if animated is not None:
        return animated
    print("YOU LOSE!")
    print("1.RETRY  HITS TAKEN: ", ehit)
    print("2. MENU   HITS GAVE: ", phit)
    print("YOU'VE EARNED ", earned, " GOLD       CRITS: ", crits)
    while True:
        try:
            answer = input("ENTER CHOICE: ").strip()
        except (EOFError, KeyboardInterrupt):
            return 2
        if answer in ("1", "2"):
            return int(answer)

def exit_screen():
    run_exit_screen()

if __name__ == "__main__":
    while x == 1:
        choice1 = run_main_menu(gold)
        if choice1 == 2:
            shop()
        if choice1 == 1:

            gamemenu()
            while gg == 1:
                print("FIGHT!")
                fight()
                retry()

        if choice1 == 3:
            exit_screen()
            break
        if choice1 == 110:
            chet.play()
            bg.stop()

            print("YOU'VE UNLOCKED ALL GLOVES AND MAPS!")
            has_spiked = 1
            has_bomb = 1
            has_lava = 1
            map2 = 1
            map3 = 1