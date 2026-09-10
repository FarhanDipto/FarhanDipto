#!/usr/bin/env python3
"""
Regenerates every hand-made SVG in this folder: the hero banner, the section
headings (dark and light variants), the profile card, and the footer.

All text is converted to outlines, so the page looks identical on every OS
and device instead of falling back to whatever font the viewer has installed.

Edit the CONTENT and PALETTE blocks, then run:

    pip install fonttools uharfbuzz
    python3 assets/build_svgs.py

The two typefaces (Space Grotesk and JetBrains Mono, both under the SIL Open
Font License) are downloaded once into ~/.cache/profile-svgs/ and reused.
"""

from __future__ import annotations

import io
import math
import os
import re
import sys
import urllib.request
from pathlib import Path

try:
    import uharfbuzz as hb
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
except ImportError:
    sys.exit("Missing dependencies. Run: pip install fonttools uharfbuzz")

# --------------------------------------------------------------------------
# CONTENT: the strings baked into the images. Change these and re-run.
# --------------------------------------------------------------------------

NAME = "Farhan Abid Ahmed"
ROLE_LINE = "AI Engineer at Gakk Media, Dhaka"
TAGLINE = "Systems that turn a sentence into something real."

# The profile card is rendered as JSON because that is how the systems on this
# page work: a model writes a spec, code renders it.
CARD_FILENAME = "profile.json"
CARD_JSON = """{
  "role": "AI Engineer",
  "team": "Gakk Media (BD) Limited",
  "base": "Dhaka, Bangladesh",
  "degree": "CSE, AUST",
  "prev": "Federated learning, AISIP Lab",
  "builds": ["OneAI", "deckforge", "xlsx_gen"]
}"""

HEADINGS = [
    ("about", "About"),
    ("building", "What I'm building"),
    ("stack", "Tech stack"),
    ("stats", "GitHub stats"),
    ("activity", "Contribution graph"),
    ("connect", "Connect"),
]

FOOTER_LINE = "Thanks for stopping by."

# --------------------------------------------------------------------------
# PALETTE: keep in sync with the badge and card colors in README.md
# --------------------------------------------------------------------------

NAVY = "#0B0E23"       # page background
INDIGO = "#271F4D"     # raised surfaces, borders
CYAN = "#4DD0E1"       # primary accent
VIOLET = "#9B5DE5"     # secondary accent
LAVENDER = "#C9B8FF"   # secondary text
INK = "#E8E8F0"        # primary text on dark
MUTED = "#6C6C89"      # tertiary text
PANEL = "#10142F"      # small panels inside the hero

# --------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------

FONT_URLS = {
    "SpaceGrotesk.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",
    "JetBrainsMono.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}

CACHE = Path(os.environ.get("PROFILE_SVG_FONT_DIR", Path.home() / ".cache" / "profile-svgs"))
OUT = Path(__file__).resolve().parent


def font_path(filename: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    target = CACHE / filename
    if not target.exists():
        print(f"downloading {filename} ...")
        urllib.request.urlretrieve(FONT_URLS[filename], target)
    return target


def fmt(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


class Face:
    """A static instance of a variable font that can shape text and emit SVG paths."""

    def __init__(self, filename: str, wght: int):
        tt = TTFont(font_path(filename))
        if "fvar" in tt:
            tt = instantiateVariableFont(tt, {"wght": wght})
        self.upem = tt["head"].unitsPerEm
        self.glyphs = tt.getGlyphSet()
        self.order = tt.getGlyphOrder()
        buf = io.BytesIO()
        tt.save(buf)
        self.font = hb.Font(hb.Face(buf.getvalue()))
        self.font.scale = (self.upem, self.upem)

    def _shape(self, text: str):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions

    def width(self, text: str, size: float, tracking: float = 0) -> float:
        infos, positions = self._shape(text)
        adv = sum(p.x_advance for p in positions) * size / self.upem
        return adv + tracking * max(len(infos) - 1, 0)

    def path(self, text: str, size: float, x: float, y: float,
             tracking: float = 0, anchor: str = "start") -> tuple[str, float]:
        """Returns (svg path data, advance width). y is the baseline."""
        infos, positions = self._shape(text)
        s = size / self.upem
        total = sum(p.x_advance for p in positions) * s + tracking * max(len(infos) - 1, 0)
        if anchor == "middle":
            x -= total / 2
        elif anchor == "end":
            x -= total
        cx = x
        parts = []
        for info, pos in zip(infos, positions):
            name = self.order[info.codepoint]
            pen = SVGPathPen(self.glyphs, ntos=fmt)
            tpen = TransformPen(pen, (s, 0, 0, -s, cx + pos.x_offset * s, y - pos.y_offset * s))
            self.glyphs[name].draw(tpen)
            d = pen.getCommands()
            if d:
                parts.append(d)
            cx += pos.x_advance * s + tracking
        return " ".join(parts), total


def text(face: Face, s: str, size: float, x: float, y: float, fill: str,
         tracking: float = 0, anchor: str = "start", extra: str = "") -> tuple[str, float]:
    d, w = face.path(s, size, x, y, tracking, anchor)
    return f'<path d="{d}" fill="{fill}"{extra}/>', w


# --------------------------------------------------------------------------
# Shared pieces
# --------------------------------------------------------------------------

def surface_defs(prefix: str, w: int, h: int) -> str:
    """Background gradient, glows, and dot grid shared by the hero and footer."""
    return f"""
  <clipPath id="{prefix}-clip"><rect width="{w}" height="{h}" rx="20"/></clipPath>
  <linearGradient id="{prefix}-bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{NAVY}"/>
    <stop offset="0.55" stop-color="#191545"/>
    <stop offset="1" stop-color="{NAVY}"/>
  </linearGradient>
  <radialGradient id="{prefix}-glow-v" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.42"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="{prefix}-glow-c" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0.32"/>
    <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="{prefix}-dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1.2" fill="{LAVENDER}"/>
  </pattern>
  <linearGradient id="{prefix}-fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.45" stop-color="#fff" stop-opacity="0"/>
    <stop offset="1" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="{prefix}-dotmask"><rect width="{w}" height="{h}" fill="url(#{prefix}-fade)"/></mask>
  <linearGradient id="{prefix}-rule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/>
    <stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>"""


def rule_gradient(id_: str, fade_out: bool) -> str:
    end = f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>' if fade_out else \
          f'<stop offset="1" stop-color="{VIOLET}"/>'
    mid = f'<stop offset="0.55" stop-color="{VIOLET}"/>' if fade_out else ""
    return f"""<linearGradient id="{id_}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/>{mid}{end}
  </linearGradient>"""


# --------------------------------------------------------------------------
# Hero
# --------------------------------------------------------------------------

PERIOD = "4s"  # one full "sentence in, artifacts out" cycle


def pulse(path_d: str, t0: float, t1: float) -> str:
    """A small light travelling along path_d between t0 and t1 (fractions of PERIOD)."""
    if t0 <= 0:
        opacity_values, opacity_times = "1;1;0;0", f"0;{t1 - 0.005:.3f};{t1:.3f};1"
        key_points, key_times = "0;1;1", f"0;{t1:.3f};1"
    else:
        opacity_values = "0;0;1;1;0;0"
        opacity_times = f"0;{t0 - 0.005:.3f};{t0:.3f};{t1 - 0.005:.3f};{t1:.3f};1"
        key_points, key_times = "0;0;1;1", f"0;{t0:.3f};{t1:.3f};1"
    return f"""<g opacity="0">
    <circle r="7" fill="{CYAN}" opacity="0.28"/>
    <circle r="3.2" fill="{CYAN}"/>
    <animate attributeName="opacity" values="{opacity_values}" keyTimes="{opacity_times}" dur="{PERIOD}" repeatCount="indefinite"/>
    <animateMotion path="{path_d}" calcMode="linear" keyPoints="{key_points}" keyTimes="{key_times}" dur="{PERIOD}" repeatCount="indefinite"/>
  </g>"""


def flash(t: float, low: str = "0.45") -> str:
    """Opacity animation that brightens briefly when a pulse arrives at time t."""
    return (f'<animate attributeName="opacity" values="{low};{low};1;{low};{low}" '
            f'keyTimes="0;{t:.3f};{t + 0.04:.3f};{t + 0.18:.3f};1" dur="{PERIOD}" repeatCount="indefinite"/>')


def panel(x: float, y: float, w: float = 104, h: float = 64) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{PANEL}" '
            f'stroke="{LAVENDER}" stroke-opacity="0.32" stroke-width="1.5"/>')


def slide_panel(x: float, y: float, t: float) -> str:
    bars = "".join(
        f'<rect x="{x + 62 + i * 10}" y="{y + 48 - hgt}" width="6" height="{hgt}" rx="1.5"/>'
        for i, hgt in enumerate((12, 22, 16, 28))
    )
    return f"""{panel(x, y)}
    <rect x="{x + 12}" y="{y + 12}" width="40" height="5" rx="2.5" fill="{LAVENDER}" opacity="0.75"/>
    <rect x="{x + 12}" y="{y + 27}" width="34" height="3" rx="1.5" fill="{LAVENDER}" opacity="0.32"/>
    <rect x="{x + 12}" y="{y + 35}" width="28" height="3" rx="1.5" fill="{LAVENDER}" opacity="0.32"/>
    <rect x="{x + 12}" y="{y + 43}" width="32" height="3" rx="1.5" fill="{LAVENDER}" opacity="0.32"/>
    <g fill="{CYAN}" opacity="0.45">{bars}{flash(t)}</g>"""


def sheet_panel(x: float, y: float, t: float) -> str:
    gx, gy, cw, ch = x + 10, y + 10, 21, 11
    lines = "".join(
        f'<line x1="{gx}" y1="{gy + r * ch}" x2="{gx + 4 * cw}" y2="{gy + r * ch}"/>' for r in range(1, 4)
    ) + "".join(
        f'<line x1="{gx + c * cw}" y1="{gy}" x2="{gx + c * cw}" y2="{gy + 4 * ch}"/>' for c in range(1, 4)
    )
    return f"""{panel(x, y)}
    <rect x="{gx}" y="{gy}" width="{4 * cw}" height="{ch}" rx="2" fill="{VIOLET}" opacity="0.55"/>
    <rect x="{gx}" y="{gy}" width="{4 * cw}" height="{4 * ch}" rx="3" fill="none" stroke="{LAVENDER}" stroke-opacity="0.35"/>
    <g stroke="{LAVENDER}" stroke-opacity="0.22" stroke-width="1">{lines}</g>
    <g fill="{CYAN}" opacity="0.45">
      <rect x="{gx + 3 * cw + 1}" y="{gy + ch + 1}" width="{cw - 2}" height="{3 * ch - 2}" rx="2"/>
      {flash(t)}
    </g>"""


def doc_panel(x: float, y: float, t: float) -> str:
    widths = (66, 56, 60, 48, 62)
    rows = []
    for i, wd in enumerate(widths):
        yy = y + 13 + i * 9
        if i == 2:
            rows.append(f'<g fill="{CYAN}" opacity="0.45"><rect x="{x + 12}" y="{yy}" width="{wd}" height="4" rx="2"/>'
                        f'<rect x="{x + 84}" y="{yy - 2}" width="8" height="8" rx="2"/>{flash(t)}</g>')
        else:
            rows.append(f'<rect x="{x + 12}" y="{yy}" width="{wd}" height="4" rx="2" fill="{LAVENDER}" opacity="0.32"/>')
    return panel(x, y) + "\n    " + "\n    ".join(rows)


def illustration() -> str:
    """A sentence goes into the hub, three artifacts come out. Drawn in its own
    coordinate space (about 742..1134 x 78..294) so the layouts can move it."""
    hx, hy = 905, 176
    px, py = 742, 150                # prompt panel
    ox = 1030                        # artifact panels column
    sy, gy, dy = 78, 154, 230        # slide, sheet, doc panel tops
    p_in = f"M{px + 82} {hy} L{hx - 40} {hy}"
    p_top = f"M{hx + 40} {hy} C 990 {hy}, 985 {sy + 32}, {ox} {sy + 32}"
    p_mid = f"M{hx + 40} {hy} C 985 {hy}, 985 {gy + 32}, {ox} {gy + 32}"
    p_bot = f"M{hx + 40} {hy} C 990 {hy}, 985 {dy + 32}, {ox} {dy + 32}"

    satellites = []
    for k in range(5):
        a = math.radians(-90 + k * 72)
        nx, ny = hx + 36 * math.cos(a), hy + 36 * math.sin(a)
        satellites.append(
            f'<line x1="{hx}" y1="{hy}" x2="{fmt(nx)}" y2="{fmt(ny)}" stroke="{LAVENDER}" stroke-opacity="0.3" stroke-width="1.2"/>'
            f'<circle cx="{fmt(nx)}" cy="{fmt(ny)}" r="3.6" fill="{LAVENDER if k % 2 else VIOLET}"/>'
        )

    return f"""<!-- connections -->
    <g fill="none" stroke="{LAVENDER}" stroke-opacity="0.24" stroke-width="1.5">
      <path d="{p_in}"/><path d="{p_top}"/><path d="{p_mid}"/><path d="{p_bot}"/>
    </g>

    <!-- the sentence -->
    <rect x="{px}" y="{py}" width="82" height="52" rx="12" fill="{PANEL}" stroke="{LAVENDER}" stroke-opacity="0.32" stroke-width="1.5"/>
    <rect x="{px + 14}" y="{py + 19}" width="44" height="4" rx="2" fill="{LAVENDER}" opacity="0.75"/>
    <rect x="{px + 14}" y="{py + 30}" width="30" height="4" rx="2" fill="{LAVENDER}" opacity="0.45"/>
    <rect x="{px + 48}" y="{py + 27}" width="2" height="10" rx="1" fill="{CYAN}"/>

    <!-- the hub -->
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 {hx} {hy}" to="360 {hx} {hy}" dur="36s" repeatCount="indefinite"/>
      <circle cx="{hx}" cy="{hy}" r="36" fill="none" stroke="{VIOLET}" stroke-opacity="0.7" stroke-width="1.4" stroke-dasharray="2 6" stroke-linecap="round"/>
      {"".join(satellites)}
    </g>
    <circle cx="{hx}" cy="{hy}" r="24" fill="url(#hero-core)">
      <animate attributeName="opacity" values="0.55;0.55;1;0.55;0.55" keyTimes="0;0.3;0.34;0.46;1" dur="{PERIOD}" repeatCount="indefinite"/>
    </circle>
    <circle cx="{hx}" cy="{hy}" r="12" fill="{CYAN}">
      <animate attributeName="r" values="12;12;15;12;12" keyTimes="0;0.3;0.34;0.44;1" dur="{PERIOD}" repeatCount="indefinite"/>
    </circle>
    <circle cx="{hx}" cy="{hy}" r="4" fill="{NAVY}" opacity="0.7"/>

    <!-- the artifacts -->
    {slide_panel(ox, sy, 0.68)}
    {sheet_panel(ox, gy, 0.72)}
    {doc_panel(ox, dy, 0.76)}

    <!-- the traffic -->
    {pulse(p_in, 0.0, 0.30)}
    {pulse(p_top, 0.36, 0.68)}
    {pulse(p_mid, 0.40, 0.72)}
    {pulse(p_bot, 0.44, 0.76)}"""


def hero(display_bold: Face, display_medium: Face, display_regular: Face, mobile: bool = False) -> str:
    if mobile:
        # Stacked: type on top, illustration below. Scales well down to phone widths.
        W, H = 600, 430
        name, _ = text(display_bold, NAME, 44, 40, 82, "url(#hero-name)", tracking=-0.4)
        role, _ = text(display_medium, ROLE_LINE, 19, 40, 118, CYAN)
        tagline, _ = text(display_regular, TAGLINE, 16, 40, 150, LAVENDER)
        art = f'<g transform="translate(-638 108)">{illustration()}</g>'
        glows = f"""<ellipse cx="300" cy="300" rx="330" ry="170" fill="url(#hero-glow-v)"/>
    <ellipse cx="560" cy="20" rx="200" ry="130" fill="url(#hero-glow-c)"/>
    <ellipse cx="20" cy="60" rx="220" ry="120" fill="url(#hero-glow-c)" opacity="0.5"/>"""
    else:
        W, H = 1200, 340
        size = 64
        while display_bold.width(NAME, size, tracking=-0.5) > 640 and size > 40:
            size -= 2
        name, _ = text(display_bold, NAME, size, 64, 152, "url(#hero-name)", tracking=-0.5)
        role, _ = text(display_medium, ROLE_LINE, 22, 64, 197, CYAN)
        tagline, _ = text(display_regular, TAGLINE, 19, 64, 238, LAVENDER)
        art = illustration()
        glows = f"""<ellipse cx="960" cy="176" rx="320" ry="200" fill="url(#hero-glow-v)"/>
    <ellipse cx="1140" cy="30" rx="230" ry="150" fill="url(#hero-glow-c)"/>
    <ellipse cx="60" cy="350" rx="280" ry="130" fill="url(#hero-glow-c)" opacity="0.55"/>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="hero-title">
  <title id="hero-title">{NAME}. {ROLE_LINE}. {TAGLINE}</title>
  <defs>{surface_defs("hero", W, H)}
  <linearGradient id="hero-name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#F6F5FC"/>
    <stop offset="1" stop-color="{LAVENDER}"/>
  </linearGradient>
  <radialGradient id="hero-core" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0.85"/>
    <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
  </radialGradient>
  </defs>
  <g clip-path="url(#hero-clip)">
    <rect width="{W}" height="{H}" fill="url(#hero-bg)"/>
    {glows}
    <rect width="{W}" height="{H}" fill="url(#hero-dots)" opacity="0.2" mask="url(#hero-dotmask)"/>

    {name}
    {role}
    {tagline}

    {art}

    <rect x="0" y="{H - 4}" width="{W}" height="4" fill="url(#hero-rule)"/>
  </g>
</svg>
"""


# --------------------------------------------------------------------------
# Section headings
# --------------------------------------------------------------------------

def heading(display_semibold: Face, title: str, dark: bool, mobile: bool = False) -> str:
    W, H, size, baseline, rule_y, gap = (600, 62, 26, 44, 34.5, 18) if mobile else (1200, 78, 34, 56, 44, 26)
    fill = INK if dark else NAVY
    path, w = text(display_semibold, title, size, 0, baseline, fill, tracking=-0.3)
    x0 = w + gap
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}">
  <defs>
  {rule_gradient("h-rule", fade_out=True)}
  </defs>
  {path}
  <rect x="{fmt(x0)}" y="{rule_y}" width="{fmt(W - x0)}" height="3" rx="1.5" fill="url(#h-rule)"/>
</svg>
"""


# --------------------------------------------------------------------------
# Profile card
# --------------------------------------------------------------------------

TOKEN = re.compile(r'("[^"]*")(\s*:)?|([^"]+)')


def card_tokens(line: str):
    """Yields (text, color) pairs for one line of JSON."""
    for m in TOKEN.finditer(line):
        quoted, colon, rest = m.groups()
        if quoted is not None:
            yield quoted, (CYAN if colon else LAVENDER)
            if colon:
                yield colon, MUTED
        elif rest:
            yield rest, MUTED


def profile_card(mono: Face) -> str:
    PAD = 24                       # transparent gutter so text can wrap around it
    W, CW = 440 + PAD, 440
    lines = CARD_JSON.splitlines()
    size, lh, top = 14, 25, 88
    H = top + lh * (len(lines) - 1) + 34

    body = []
    for i, line in enumerate(lines):
        x = PAD + 26
        y = top + i * lh
        for chunk, color in card_tokens(line):
            p, w = text(mono, chunk, size, x, y, color)
            body.append(p)
            x += w
    tab, _ = text(mono, CARD_FILENAME, 13, PAD + 26, 35, MUTED)

    label = "Profile card: " + " ".join(l.strip() for l in lines).replace('"', "")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
  <defs>
  {rule_gradient("card-rule", fade_out=False)}
  </defs>
  <rect x="{PAD}" y="1" width="{CW - 1}" height="{H - 2}" rx="16" fill="{NAVY}" stroke="{INDIGO}" stroke-width="1.5"/>
  {tab}
  <line x1="{PAD + 1}" y1="52" x2="{W - 1}" y2="52" stroke="{INDIGO}" stroke-width="1.5"/>
  <rect x="{PAD + 26}" y="50" width="{mono.width(CARD_FILENAME, 13):.1f}" height="2" rx="1" fill="url(#card-rule)"/>
  {"".join(body)}
</svg>
"""


# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------

def footer(display_medium: Face, mobile: bool = False) -> str:
    W, H, size = (600, 96, 18) if mobile else (1200, 120, 21)
    line, _ = text(display_medium, FOOTER_LINE, size, W / 2, H / 2 + size * 0.36, LAVENDER, anchor="middle")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{FOOTER_LINE}">
  <defs>{surface_defs("foot", W, H)}</defs>
  <g clip-path="url(#foot-clip)">
    <rect width="{W}" height="{H}" fill="url(#foot-bg)"/>
    <ellipse cx="{W * 0.85}" cy="{H / 2}" rx="{W * 0.3}" ry="{H}" fill="url(#foot-glow-v)"/>
    <ellipse cx="{W * 0.1}" cy="{H}" rx="{W * 0.25}" ry="{H * 0.9}" fill="url(#foot-glow-c)" opacity="0.6"/>
    <rect width="{W}" height="{H}" fill="url(#foot-dots)" opacity="0.2" mask="url(#foot-dotmask)"/>
    <rect x="0" y="0" width="{W}" height="4" fill="url(#foot-rule)"/>
    {line}
  </g>
</svg>
"""


# --------------------------------------------------------------------------

def main() -> None:
    bold = Face("SpaceGrotesk.ttf", 700)
    semibold = Face("SpaceGrotesk.ttf", 600)
    medium = Face("SpaceGrotesk.ttf", 500)
    regular = Face("SpaceGrotesk.ttf", 400)
    mono = Face("JetBrainsMono.ttf", 400)

    files = {
        "hero.svg": hero(bold, medium, regular),
        "hero-mobile.svg": hero(bold, medium, regular, mobile=True),
        "profile-card.svg": profile_card(mono),
        "footer.svg": footer(medium),
        "footer-mobile.svg": footer(medium, mobile=True),
    }
    for slug, title in HEADINGS:
        for theme in ("dark", "light"):
            files[f"heading-{slug}-{theme}.svg"] = heading(semibold, title, dark=theme == "dark")
            files[f"heading-{slug}-{theme}-mobile.svg"] = heading(semibold, title, dark=theme == "dark", mobile=True)

    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote {name} ({len(svg) // 1024} KB)")


if __name__ == "__main__":
    main()
