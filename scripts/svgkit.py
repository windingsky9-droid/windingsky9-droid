"""Small helpers shared by the profile art scripts.

Everything here writes plain SVG strings. Glyph outlines come from
glyphs.json (DejaVu Sans), so zodiac and planet symbols render the same on
every device without relying on the viewer's fonts.
"""
import json
import math
import os
import random
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
_G = json.load(open(os.path.join(HERE, "glyphs.json")))
UPM = _G["unitsPerEm"]

SERIF = "Georgia, 'Times New Roman', 'DejaVu Serif', serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, 'DejaVu Sans', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

# One palette for every card: deep navy space, warm gold, mint, coral.
C = {
    "bg0": "#0d1536", "bg1": "#02040c",
    "ink": "#eef2ff", "muted": "#aab4d6", "dim": "#6f7aa3",
    "gold": "#ffd88a", "amber": "#f5b94a", "mint": "#5ef0c8", "coral": "#ff906c",
    "sky": "#7cc4ff", "lav": "#b9a6ff", "rose": "#ff8fb8",
    "line": "rgba(226,233,255,0.14)", "panel": "rgba(255,255,255,0.045)",
}
ELEMENT = ["fire", "earth", "air", "water"]
ELEMENT_COLOR = {"fire": C["coral"], "earth": C["gold"], "air": C["sky"], "water": C["mint"]}
SIGNS = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
         "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
SIGN_NAMES = [s.capitalize() for s in SIGNS]


def esc(s):
    return escape(str(s), quote=True)


def glyph(name, x, y, size, fill="currentColor", extra=""):
    """A glyph path centred on (x, y), drawn `size` px tall per em."""
    g = _G["glyphs"][name]
    k = size / UPM
    x0, y0, x1, y1 = g["bounds"]
    tx = x - (x0 + x1) / 2 * k
    ty = y + (y0 + y1) / 2 * k
    return (f'<path d="{g["d"]}" transform="translate({tx:.2f} {ty:.2f}) scale({k:.5f} {-k:.5f})" '
            f'fill="{fill}" {extra}/>')


def polar(cx, cy, r, deg):
    """Chart-wheel polar: 0 deg of Aries at 9 o'clock, longitude counter-clockwise."""
    a = math.radians(180 + deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def stars(w, h, n, seed, rmax=1.6, avoid=None):
    """Seeded star field with four twinkle speeds (classes s1..s4)."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        if avoid and avoid(x, y):
            continue
        r = rnd.random() ** 3 * rmax + 0.35
        op = 0.35 + rnd.random() * 0.6
        tint = rnd.choice(["#ffffff"] * 6 + ["#ffe7c4", "#cfe3ff", "#ffd88a"])
        cls = f"s s{1 + i % 4}" if rnd.random() < 0.55 else ""
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{tint}" opacity="{op:.2f}" class="{cls}"/>')
    return "\n".join(out)


TWINKLE_CSS = """
.s{animation:tw 3s ease-in-out infinite alternate}
.s1{animation-duration:2.2s}.s2{animation-duration:3.5s;animation-delay:-1.1s}
.s3{animation-duration:4.7s;animation-delay:-2.3s}.s4{animation-duration:2.9s;animation-delay:-.6s}
@keyframes tw{from{opacity:.15}to{opacity:1}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


def card_open(w, h, title, desc, extra_defs="", extra_css="", radius=28):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title>
<desc id="d">{esc(desc)}</desc>
<defs>
<radialGradient id="bg" cx="68%" cy="30%" r="95%"><stop offset="0" stop-color="{C['bg0']}"/><stop offset="1" stop-color="{C['bg1']}"/></radialGradient>
<clipPath id="card"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>
{extra_defs}
<style>{TWINKLE_CSS}{extra_css}</style>
</defs>
<g clip-path="url(#card)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>
"""


def card_close(w, h, radius=28):
    return f"""</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{radius}" fill="none" stroke="rgba(255,255,255,0.10)"/>
</svg>
"""


def text(x, y, s, size, fill=None, family=SANS, weight=400, anchor="start", extra=""):
    fill = fill or C["ink"]
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def label(x, y, s, size=17, fill=None, spacing=4, anchor="start"):
    """Small letter-spaced mono caps label."""
    return text(x, y, s.upper(), size, fill or C["gold"], MONO, 500, anchor, f'letter-spacing="{spacing}"')
