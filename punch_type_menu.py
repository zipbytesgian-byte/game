"""Animated ASCII main menu for PUNCH TYPE.

Use it from the game:

    from punch_type_menu import run_main_menu
    choice1 = run_main_menu(gold)      # returns 1 (START), 2 (SHOP), 3 (EXIT), or 110 (cheat)

Controls: W/S or Up/Down move, Enter selects, 1/2/3 jump to a button,
Q / Esc quit (returns 3). Type 110 then Enter for your cheat code.

Animations: title wipes in then shimmers with fire colors, marquee border,
spinning gold coin, gold counts up, pulsing >> << arrows on the selected
button, the fighter bobs, blinks and throws a punch when you confirm.

Needs a real terminal (cmd / PowerShell / Windows Terminal / Terminal) at
least 80x28. Anywhere else it falls back to the plain static menu.
"""
from __future__ import annotations

import os
import shutil
import sys
import time
from contextlib import contextmanager

WIDTH = 78            # updated to the terminal width when the game starts
INNER = WIDTH - 2     # width between the left and right borders
HEIGHT = 26           # minimum content height
FPS = 30

# --------------------------------------------------------------------------
# Block-letter title (5 rows tall). Add letters here to change the title.
# --------------------------------------------------------------------------
FONT = {
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "U": ["#   #", "#   #", "#   #", "#   #", " ### "],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    "C": [" ####", "#    ", "#    ", "#    ", " ####"],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #"],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    "E": ["#####", "#    ", "#### ", "#    ", "#####"],
    " ": ["   ", "   ", "   ", "   ", "   "],
}
TITLE = "PUNCH TYPE"


def block_text(text):
    """Turn text into 5 rows of block letters, one blank column between letters."""
    return [" ".join(FONT[ch][row] for ch in text) for row in range(5)]


# --------------------------------------------------------------------------
# Character portrait frames (each row fits a 22-wide box)
# --------------------------------------------------------------------------
PORTRAIT_W = 22

FRAME_IDLE = [
    "     .-\"\"\"\"\"-.      ",
    "    /  ,   ,  \\     ",
    "   |  (o) (o)  |    ",
    "    \\    ^    /     ",
    "     \\  ===  /      ",
    "  (@)==\\_____/==(@)  ",
    "      /|  *  |\\      ",
    "     / |     | \\     ",
    "       |_____|       ",
]
FRAME_GUARD = [
    "     .-\"\"\"\"\"-.      ",
    "    /  ,   ,  \\     ",
    " (@)|  (o) (o)  |(@) ",
    "    \\    ^    /     ",
    "     \\  ===  /      ",
    "     /\\_____/\\      ",
    "      /|  *  |\\      ",
    "     / |     | \\     ",
    "       |_____|       ",
]
FRAME_PUNCH = [
    "     .-\"\"\"\"\"-.      ",
    "    /  ,   ,  \\     ",
    "   |  (>) (<)  |    ",
    "    \\    O    /     ",
    "     \\  ===  /      ",
    "  (@)=\\_____/=====(@)",
    "      /|  *  |\\      ",
    "     / |     | \\     ",
    "       |_____|       ",
]


def portrait_art(t=0.0, punching=False):
    """Pick the portrait frame for time t (idle bob, blink, shadow-punch)."""
    if punching or 5.0 <= (t % 6.0) < 5.3:
        frame = FRAME_PUNCH
    else:
        frame = FRAME_IDLE if int(t * 2) % 2 == 0 else FRAME_GUARD
        if (t % 3.2) < 0.15:  # blink
            frame = [l.replace("(o) (o)", "(-) (-)") for l in frame]
    return [l.center(PORTRAIT_W)[:PORTRAIT_W] for l in frame]


def portrait_box(title="FIGHTER", art=None):
    art = art or portrait_art()
    top = "+" + f" {title} ".center(PORTRAIT_W, "-") + "+"
    return [top, *["|" + l + "|" for l in art], "+" + "-" * PORTRAIT_W + "+"]


# --------------------------------------------------------------------------
# Buttons
# --------------------------------------------------------------------------
BUTTONS = [("1", "START"), ("2", "SHOP"), ("3", "EXIT")]
BUTTON_W = 19


def button_text(index, kind):
    """kind 0 = top border, 1 = label row, 2 = bottom border."""
    num, name = BUTTONS[index]
    if kind == 1:
        return "|" + f"{num}  [ {name:^7} ]".center(BUTTON_W) + "|"
    return "+" + "=" * BUTTON_W + "+"


# --------------------------------------------------------------------------
# Static (plain) screen - also the fallback when animation isn't possible
# --------------------------------------------------------------------------
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
    portrait = portrait_box()

    right_margin = 4
    left_w = INNER - PORTRAIT_W - 2 - right_margin
    for b, p in zip(buttons, portrait):
        lines.append(row(b.center(left_w) + p.ljust(PORTRAIT_W + 2) + " " * right_margin))

    lines += [row(), row(stars), row("Type 1, 2 or 3 and press ENTER".center(INNER)), border]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Terminal helpers
# --------------------------------------------------------------------------
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
HOME = "\x1b[H"
CLEAR = "\x1b[2J"
CLEAR_EOL = "\x1b[K"

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


# --------------------------------------------------------------------------
# Animated rendering
# --------------------------------------------------------------------------
EDGE = c(208) + "|" + RESET


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
    """Build one full frame as a string. t = seconds since the menu opened."""
    def visible(start):
        return (not intro) or t >= start

    lines = [c(208) + "+" + "=" * INNER + "+" + RESET]

    # gold row with a spinning coin
    coin = ["[o]", "[O]", "[0]", "[O]"][int(t * 5) % 4]
    lines.append(_row([("  GOLD: ", c(220) + BOLD), (str(int(shown_gold)), c(226) + BOLD),
                       (" ", ""), (coin, c(220) + BOLD)]))
    lines.append(_row([]))

    # title: wipes in left-to-right, then fire shimmer sweeps across it
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

    # marquee divider
    def stars():
        shift = int(t * 10)
        return _row([("*", c(220) + BOLD) if (i + shift) % 4 == 0 else (".", c(240))
                     for i in range(INNER)])

    lines += [_row([]), stars(), _row([])]

    # middle: buttons (left) + portrait (right)
    right_margin = 4
    left_w = INNER - PORTRAIT_W - 2 - right_margin
    box_left = (left_w - (BUTTON_W + 2)) // 2
    pulse = int(t * 3) % 2
    portrait = portrait_box(art=portrait_art(t, punching))

    for k in range(11):
        j, kind = divmod(k, 4)
        if kind == 3 or not visible(1.0 + 0.15 * j):
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
            p = portrait[k]
            border_style = c(45)
            if k in (0, len(portrait) - 1):
                right = [(p, border_style)]
            else:
                right = [(p[0], border_style), (p[1:-1], c(252)), (p[-1], border_style)]
        else:
            right = [(" " * (PORTRAIT_W + 2), "")]
        lines.append(_row(left + right + [(" " * right_margin, "")]))

    lines += [_row([]), stars()]
    hint = "W/S or UP/DOWN to move   ENTER to select   or press 1 2 3"
    lines.append(_row([(" " * ((INNER - len(hint)) // 2), ""), (hint, c(245))]))
    lines.append(c(208) + "+" + "=" * INNER + "+" + RESET)

    # Use the available terminal height too: keep the artwork centered vertically.
    term_rows = shutil.get_terminal_size((WIDTH, HEIGHT + 2)).lines
    target_rows = max(len(lines), term_rows - 1)
    extra = target_rows - len(lines)
    if extra > 0:
        top = extra // 2
        lines = ([""] * top) + lines + ([""] * (extra - top))

    return HOME + "".join(l + CLEAR_EOL + "\n" for l in lines)


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------
_intro_done = False      # the title wipe only plays the first time
_shown_gold = 0.0        # gold counter remembers where it left off
_note_shown = False


_reason = ""


def _try_resize(cols=100, rows=35):
    """Ask the terminal window to grow (works in cmd/PowerShell and many others)."""
    try:
        if os.name == "nt":
            os.system(f"mode con: cols={cols} lines={rows}")
        else:
            sys.stdout.write(f"\x1b[8;{rows};{cols}t")
            sys.stdout.flush()
        time.sleep(0.2)
    except Exception:
        pass


def _can_animate():
    """Use the real terminal dimensions instead of forcing a fixed-size window."""
    global _reason, WIDTH, INNER
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        _reason = ("this is not a real terminal (IDLE, Thonny, an IDE 'Run' panel or piped "
                   "input can't redraw the screen). Open Command Prompt / PowerShell / "
                   "Windows Terminal and run:  python punch_type.py")
        return False

    size = shutil.get_terminal_size((80, 28))
    if size.columns < 80 or size.lines < HEIGHT + 2:
        _reason = (f"your terminal is {size.columns}x{size.lines}; the animated menu needs "
                   f"at least 80x{HEIGHT + 2}. Maximize the terminal or reduce its font size, then restart.")
        return False

    # Fill the available width. Keep at least the original 78-character frame.
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
        return 0          # game ignores 0 and shows the menu again
    except EOFError:
        return 3


def run_main_menu(gold=0):
    """Show the animated menu and return 1, 2, 3 (or 110 for the cheat code)."""
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
                key = poll_key()

                if key == "up":
                    sel, typed = (sel - 1) % len(BUTTONS), ""
                elif key == "down":
                    sel, typed = (sel + 1) % len(BUTTONS), ""
                elif key.isdigit():
                    typed = (typed + key)[-3:]
                    if key in "123":
                        sel = int(key) - 1
                elif key == "quit":
                    result = 3
                    break
                elif key == "enter":
                    result = 110 if typed.endswith("110") else sel + 1
                    for i in range(8):       # confirm: flash + punch
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


if __name__ == "__main__":
    print("You chose:", run_main_menu(500))