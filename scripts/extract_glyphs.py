"""One-off: copy zodiac and planet glyph outlines out of DejaVu Sans.

The daily sky script draws these paths directly, so the wheel looks the
same on every device and the GitHub Action needs no fonts installed.
DejaVu fonts are free to embed (Bitstream Vera license, changes public domain).
"""
import json
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONT = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CHARS = {
    "aries": "♈", "taurus": "♉", "gemini": "♊", "cancer": "♋",
    "leo": "♌", "virgo": "♍", "libra": "♎", "scorpio": "♏",
    "sagittarius": "♐", "capricorn": "♑", "aquarius": "♒", "pisces": "♓",
    "sun": "☉", "moon": "☽", "mercury": "☿", "venus": "♀", "mars": "♂",
    "jupiter": "♃", "saturn": "♄", "uranus": "♅", "neptune": "♆", "pluto": "♇",
    "retrograde": "℞",
}

font = TTFont(FONT)
cmap = font.getBestCmap()
gs = font.getGlyphSet()
upm = font["head"].unitsPerEm
out = {"unitsPerEm": upm, "source": "DejaVu Sans", "license": "Bitstream Vera Fonts license; DejaVu changes are public domain", "glyphs": {}}
for name, ch in CHARS.items():
    gname = cmap.get(ord(ch))
    if not gname:
        print("missing", name, file=sys.stderr)
        continue
    pen = SVGPathPen(gs)
    gs[gname].draw(pen)
    bp = BoundsPen(gs)
    gs[gname].draw(bp)
    out["glyphs"][name] = {"d": pen.getCommands(), "bounds": bp.bounds}
json.dump(out, open("scripts/glyphs.json", "w"), separators=(",", ":"))
print(len(out["glyphs"]), "glyphs, upm", upm)
