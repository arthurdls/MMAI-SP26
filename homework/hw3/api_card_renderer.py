"""
NOTE: The following code was created with AI assistance. I had the idea in mind for
how to render the API cards, but I didn't know how to implement it.
It would've taken a lot longer and would've removed my focus from the goal of
the assignment.


api_card_renderer.py
Renders a ToolBench API list as a dark code-card JPG for VLM fine-tuning.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Constants — colors (hex → RGB tuples)
# ---------------------------------------------------------------------------
BG          = (13,  17,  23)   # #0d1117  canvas background
CARD_BG     = (22,  27,  34)   # #161b22  card background
CARD_BORDER = (48,  54,  61)   # #30363d  card border
ACCENT      = (88, 166, 255)   # #58a6ff  left accent bar + header
NAME_COLOR  = (121, 192, 255)  # #79c0ff  API name text
DESC_COLOR  = (139, 148, 158)  # #8b949e  description text
REQ_BG      = (183,  28,  28)  # #b71c1c  required pill background
REQ_FG      = (255, 205, 210)  # #ffcdd2  required pill text
OPT_BG      = ( 31,  58, 110)  # #1f3a6e  optional pill background
OPT_FG      = (202, 232, 255)  # #cae8ff  optional pill text
META_COLOR  = ( 74,  85, 104)  # #4a5568  footer/meta text

CANVAS_W    = 800
ACCENT_BAR  = 3   # px width of left accent bar on each card
CARD_PAD    = 12  # px inner padding inside each card
CARD_GAP    = 8   # px vertical gap between cards
HEADER_H    = 48  # px height reserved for header
TOP_PAD     = 16  # px padding above header

_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
]

# ---------------------------------------------------------------------------
# Font loading
# ---------------------------------------------------------------------------

def load_font(size: int) -> ImageFont.FreeTypeFont:
    """Load a monospace TrueType font at *size* pt; fall back to PIL default."""
    for path in _FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()

# ---------------------------------------------------------------------------
# Description cleaning
# ---------------------------------------------------------------------------
_DESC_MAX = 90
_RE_INNER = re.compile(
    r'The description of this function is:\s*["\'](.+?)["\']',
    re.DOTALL,
)
_RE_TOOL = re.compile(r'This is the subfunction for tool "([^"]+)"')


def clean_description(raw: str) -> str:
    """Extract meaningful text from ToolBench's verbose description field."""
    if not raw or not raw.strip():
        return "(no description)"

    m = _RE_INNER.search(raw)
    if m:
        text = m.group(1).strip()
        if len(text) > _DESC_MAX:
            text = text[:_DESC_MAX] + "…"
        return text

    m2 = _RE_TOOL.search(raw)
    if m2:
        return f"(subfunction of {m2.group(1)})"

    return "(no description)"

# ---------------------------------------------------------------------------
# Parameter pill extraction
# ---------------------------------------------------------------------------
_MAX_PILLS = 6


def get_param_pills(
    params: dict | None,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Return (required_pills, optional_pills) as lists of (name, type) tuples.

    Types are lower-cased. Total pill count is capped at _MAX_PILLS (required first).
    Returns ([], []) for APIs with no parameters.
    """
    if not params or not isinstance(params, dict):
        return [], []

    props = params.get("properties") or {}
    required_names = params.get("required") or []
    optional_names = params.get("optional") or []

    def _pill(name: str) -> tuple[str, str]:
        ptype = props.get(name, {}).get("type", "any")
        return (name, str(ptype).lower())

    req_pills = [_pill(n) for n in required_names]
    opt_pills = [_pill(n) for n in optional_names]

    total = len(req_pills) + len(opt_pills)
    if total > _MAX_PILLS:
        if len(req_pills) >= _MAX_PILLS:
            req_pills = req_pills[:_MAX_PILLS]
            opt_pills = []
        else:
            opt_pills = opt_pills[: _MAX_PILLS - len(req_pills)]

    return req_pills, opt_pills

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def _text_size(text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    """Return (width, height) of *text* rendered in *font*. Requires Pillow >= 8."""
    bbox = font.getbbox(text)   # (left, top, right, bottom)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _draw_pill(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    bg: tuple[int, int, int],
    fg: tuple[int, int, int],
    font: ImageFont.FreeTypeFont,
) -> int:
    """Draw a rounded-rectangle pill at (x, y). Returns the pill width."""
    pad_x, pad_y, radius = 6, 2, 4
    tw, th = _text_size(text, font)
    pill_w = tw + 2 * pad_x
    pill_h = th + 2 * pad_y
    draw.rounded_rectangle(
        [x, y, x + pill_w, y + pill_h],
        radius=radius,
        fill=bg,
    )
    draw.text((x + pad_x, y + pad_y), text, fill=fg, font=font)
    return pill_w


# ---------------------------------------------------------------------------
# Main renderer
# ---------------------------------------------------------------------------

def _choose_font_size(n_apis: int) -> int:
    if n_apis <= 5:
        return 12
    if n_apis <= 10:
        return 10
    return 9


def _canvas_height(n_apis: int) -> int:
    return max(900, 120 + 100 * n_apis)


def render_one_example(row: Any, out_path: str | Path) -> None:
    """Render the API list from *row* as a dark code-card JPG saved to *out_path*.

    Args:
        row: dict-like with key ``api_list_json`` (JSON string of API list).
        out_path: destination file path (created/overwritten).
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # --- parse API list ---
    raw_json = row.get("api_list_json", "[]") if hasattr(row, "get") else getattr(row, "api_list_json", "[]")
    try:
        api_list: list[dict] = json.loads(raw_json)
    except (json.JSONDecodeError, TypeError):
        api_list = []

    # Defensive: filter non-dicts and the Finish sentinel
    api_list = [a for a in api_list if isinstance(a, dict) and a.get("name") != "Finish"]

    n = len(api_list)
    font_size = _choose_font_size(n)
    canvas_h  = _canvas_height(n)

    img  = Image.new("RGB", (CANVAS_W, canvas_h), color=BG)
    draw = ImageDraw.Draw(img)

    name_font   = load_font(font_size + 1)   # slightly larger for API name
    body_font   = load_font(font_size)
    pill_font   = load_font(max(font_size - 2, 7))
    header_font = load_font(font_size + 1)

    # --- header ---
    hdr_text  = "API Reference"
    meta_text = f"{n} APIs"
    draw.text((16, TOP_PAD), hdr_text,  fill=ACCENT,      font=header_font)
    draw.text((CANVAS_W - 16 - _text_size(meta_text, body_font)[0], TOP_PAD),
              meta_text, fill=META_COLOR, font=body_font)
    line_y = TOP_PAD + HEADER_H - 8
    draw.line([(16, line_y), (CANVAS_W - 16, line_y)], fill=CARD_BORDER, width=1)

    if n == 0:
        draw.text((16, line_y + 20), "(no APIs available)", fill=META_COLOR, font=body_font)
        img.save(out_path, "JPEG", quality=90)
        return

    # --- cards ---
    cursor_y = line_y + 12

    for api in api_list:
        name = str(api.get("name", "(unnamed)"))
        desc = clean_description(str(api.get("description", "")))
        req_pills, opt_pills = get_param_pills(api.get("parameters"))

        # Truncate name at 60 chars per spec
        if len(name) > 60:
            name = name[:60] + "…"

        # Compute overflow before pills were capped
        params_raw = api.get("parameters", {}) or {}
        total_params = len(params_raw.get("required") or []) + len(params_raw.get("optional") or [])
        overflow = max(0, total_params - len(req_pills) - len(opt_pills))

        # Estimate card height
        _, name_h = _text_size(name, name_font)
        _, desc_h = _text_size(desc, body_font)
        _, pill_h = _text_size("Ag", pill_font)
        has_params = bool(req_pills or opt_pills or overflow)
        pill_row_h = (pill_h + 4 + 4) if has_params else 0
        card_h = (
            CARD_PAD
            + name_h + 4
            + desc_h + (6 if pill_row_h else 0)
            + pill_row_h
            + CARD_PAD
        )

        # card background + border
        card_x0, card_x1 = 16, CANVAS_W - 16
        draw.rectangle([card_x0, cursor_y, card_x1, cursor_y + card_h], fill=CARD_BG)
        draw.rectangle([card_x0, cursor_y, card_x1, cursor_y + card_h], outline=CARD_BORDER, width=1)
        # left accent bar
        draw.rectangle([card_x0, cursor_y, card_x0 + ACCENT_BAR, cursor_y + card_h], fill=ACCENT)

        # text origin (inside padding, after accent bar)
        tx = card_x0 + ACCENT_BAR + CARD_PAD
        ty = cursor_y + CARD_PAD

        # API name
        _, name_h = _text_size(name, name_font)
        draw.text((tx, ty), name, fill=NAME_COLOR, font=name_font)
        ty += name_h + 4

        # Description
        _, desc_h = _text_size(desc, body_font)
        draw.text((tx, ty), desc, fill=DESC_COLOR, font=body_font)
        ty += desc_h

        # Param pills
        if req_pills or opt_pills or overflow:
            ty += 6
            px = tx
            pill_gap = 4
            for pname, ptype in req_pills:
                label = f"{pname}: {ptype} · REQ"
                pw = _draw_pill(draw, px, ty, label, REQ_BG, REQ_FG, pill_font)
                px += pw + pill_gap
            for pname, ptype in opt_pills:
                label = f"{pname}: {ptype}"
                pw = _draw_pill(draw, px, ty, label, OPT_BG, OPT_FG, pill_font)
                px += pw + pill_gap
            if overflow:
                overflow_label = f"+{overflow} more"
                draw.text((px, ty), overflow_label, fill=META_COLOR, font=pill_font)

        cursor_y += card_h + CARD_GAP

    img.save(out_path, "JPEG", quality=90)

# ---------------------------------------------------------------------------
# Text utilities (used by HW3 notebook)
# ---------------------------------------------------------------------------

def truncate_text(text: str | None, max_chars: int) -> str:
    """Truncate *text* to *max_chars* characters, appending '...' if cut."""
    if text is None:
        return ""
    text = str(text)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."
