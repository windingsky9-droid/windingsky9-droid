#!/usr/bin/env python3
"""Draw the cards that do not change daily: assets/about.svg and assets/skills.svg.

Run by hand after editing the text below:  python scripts/build_static_art.py
Needs Pillow (for the ASCII planet).
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

from svgkit import C, MONO, SANS, SERIF, card_close, card_open, esc, label, stars, text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ABOUT = [  # key, value: keep it short and true
    ("Role", "Python & API dev who also draws planets"),
    ("Stack", "Python · Flask · REST/JSON · pytest"),
    ("Render", "three.js r170 · WebGL2 · GLSL · bloom"),
    ("Sky", "3,232 real stars, placed by my own math"),
    ("Accuracy", "Sun 0.006° · Moon 0.028° vs PyEphem"),
    ("Tests", "15 passing on Market Observatory"),
    ("Chess", "WindingSkyy · 2,000+ games · 76% accuracy"),
    ("Cooking", "a 3D configurator, a duo display, more"),
    ("Status", "open to junior, contract & project work"),
    ("Rate", "Flask/API fixes from $40, scope first"),
    ("Motto", "if it renders, it ships"),
]


def ascii_planet(cols=44, rows=24):
    """A ringed planet as coloured ASCII. Returns rows of (char, colour) cells."""
    W, H = cols * 10, rows * 21
    S = 4
    img = Image.new("L", (W * S, H * S), 0)
    mat = Image.new("L", (W * S, H * S), 0)  # 1 = planet, 2 = ring
    d, dm = ImageDraw.Draw(img), ImageDraw.Draw(mat)
    cx, cy, r = W * S * 0.5, H * S * 0.52, H * S * 0.29
    ring = lambda a, b, fill, width: d.ellipse([cx - a, cy - b, cx + a, cy + b], outline=fill, width=width)
    # back half of the ring
    for k, (a, w, lum) in enumerate([(r * 1.95, 9 * S, 150), (r * 1.72, 7 * S, 230), (r * 1.52, 6 * S, 190)]):
        d.arc([cx - a, cy - a * 0.27, cx + a, cy + a * 0.27], 180, 360, fill=lum, width=w)
        dm.arc([cx - a, cy - a * 0.27, cx + a, cy + a * 0.27], 180, 360, fill=2, width=w)
    # planet with light from the upper left
    px = Image.new("L", img.size, 0)
    pd = ImageDraw.Draw(px)
    for i in range(60, 0, -1):
        f = i / 60
        lum = int(255 * (0.18 + 0.82 * (1 - f) ** 0.7))
        rr = r * f
        ox, oy = -r * 0.35 * (1 - f), -r * 0.35 * (1 - f)
        pd.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr], fill=lum)
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(px, (0, 0), mask)
    mat.paste(1, (0, 0), mask)
    # front half of the ring, over the planet
    for a, w, lum in [(r * 1.95, 9 * S, 150), (r * 1.72, 7 * S, 230), (r * 1.52, 6 * S, 190)]:
        d.arc([cx - a, cy - a * 0.27, cx + a, cy + a * 0.27], 0, 180, fill=lum, width=w)
        dm.arc([cx - a, cy - a * 0.27, cx + a, cy + a * 0.27], 0, 180, fill=2, width=w)
    img = img.filter(ImageFilter.GaussianBlur(S * 1.2)).resize((cols, rows), Image.BOX)
    mat = mat.resize((cols, rows), Image.NEAREST)
    ramp = " .:-=+*#%@"
    rnd = random.Random(4)
    out = []
    for y in range(rows):
        row = []
        for x in range(cols):
            v = img.getpixel((x, y)) / 255
            m = mat.getpixel((x, y))
            ch = ramp[min(len(ramp) - 1, int(v * len(ramp)))]
            if ch == " " and rnd.random() < 0.025:
                ch, col = rnd.choice(".·*"), "#cfd8ff"
            elif m == 2:
                col = C["mint"] if (x + y) % 7 else C["sky"]
            else:
                t = y / rows
                col = "#ffe7b8" if t < 0.42 else (C["gold"] if t < 0.6 else C["amber"])
            row.append((ch, col))
        out.append(row)
    return out


def about_svg():
    W, H = 1280, 640
    s = [card_open(W, H, "About Sushir, as a terminal",
                   "; ".join(f"{k}: {v}" for k, v in ABOUT), radius=24)]
    # window chrome
    s.append(f'<rect width="{W}" height="54" fill="rgba(255,255,255,.04)"/>')
    s.append(f'<line x1="0" y1="54" x2="{W}" y2="54" stroke="{C["line"]}"/>')
    for i, col in enumerate([C["coral"], C["gold"], C["mint"]]):
        s.append(f'<circle cx="{34 + i * 26}" cy="27" r="7.5" fill="{col}"/>')
    s.append(text(W / 2, 34, "sushi@windingsky: ~/about", 17, C["muted"], MONO, 500, "middle"))
    # ascii planet, each row stretched to the same width so every font lines up
    grid = ascii_planet()
    x0, y0, cw, lh = 46, 104, 10, 21
    for r, row in enumerate(grid):
        spans = []
        run_col, run = None, ""
        for ch, col in row + [(None, None)]:
            if col != run_col and run:
                spans.append(f'<tspan fill="{run_col}">{esc(run)}</tspan>')
                run = ""
            if ch is None:
                break
            run_col = col
            run += ch
        s.append(f'<text x="{x0}" y="{y0 + r * lh}" font-family="{MONO}" font-size="17" xml:space="preserve" '
                 f'textLength="{len(row) * cw}" lengthAdjust="spacingAndGlyphs">{"".join(spans)}</text>')
    # neofetch-style info
    ix, iy = 530, 110
    s.append(f'<text x="{ix}" y="{iy}" font-family="{MONO}" font-size="24" font-weight="700">'
             f'<tspan fill="{C["gold"]}">sushi</tspan><tspan fill="{C["muted"]}">@</tspan><tspan fill="{C["mint"]}">windingsky</tspan></text>')
    s.append(f'<line x1="{ix}" y1="{iy + 14}" x2="{ix + 330}" y2="{iy + 14}" stroke="{C["muted"]}" stroke-dasharray="3 5"/>')
    for i, (k, v) in enumerate(ABOUT):
        y = iy + 52 + i * 37
        s.append(text(ix, y, k, 21, C["gold"], MONO, 600))
        s.append(text(ix + 140, y, v, 21, C["ink"], MONO, 400))
    # colour blocks
    for i, col in enumerate([C["bg1"], C["coral"], C["gold"], C["mint"], C["sky"], C["lav"], C["rose"], C["ink"]]):
        s.append(f'<rect x="{ix + i * 44}" y="{iy + 52 + len(ABOUT) * 37 - 8}" width="40" height="22" rx="4" fill="{col}" stroke="rgba(255,255,255,.15)"/>')
    s.append(f'<rect x="{ix + 8 * 44 + 10}" y="{iy + 52 + len(ABOUT) * 37 - 6}" width="11" height="19" fill="{C["ink"]}" class="blink"/>')
    s.append(card_close(W, H, radius=24))
    out = "\n".join(s).replace("<style>", "<style>.blink{animation:bl 1.1s steps(1) infinite}@keyframes bl{50%{opacity:0}}")
    open(os.path.join(ROOT, "assets", "about.svg"), "w").write(out)


SKY = [
    ("The Backend", "Python does the boring parts reliably.", C["gold"], (60, 230, 560, 250), [
        ("Python", 11, .08, .45), ("Flask", 9, .32, .18), ("REST / JSON", 8, .58, .40), ("pytest", 7, .80, .14),
        ("Gunicorn", 5, .62, .86), ("Docker", 5, .30, .80)], [(0, 1), (1, 2), (2, 3), (2, 4), (4, 5), (5, 0)]),
    ("The Renderer", "Pixels with physics behind them.", C["mint"], (680, 230, 540, 250), [
        ("three.js", 11, .06, .34), ("WebGL2", 9, .34, .64), ("GLSL", 8, .56, .16), ("JavaScript", 9, .92, .40),
        ("HDR bloom", 6, .62, .92), ("HTML / CSS", 7, .14, .92)], [(0, 1), (1, 2), (2, 3), (1, 4), (4, 3), (1, 5)]),
    ("The Automaton", "Robots that check my work.", C["sky"], (60, 560, 560, 220), [
        ("GitHub Actions", 9, .10, .30), ("Playwright", 8, .42, .14), ("CI checks", 6, .70, .38),
        ("AI / MCP APIs", 8, .40, .78), ("CodeQL", 5, .90, .80)], [(0, 1), (1, 2), (2, 4), (0, 3), (3, 2)]),
    ("The Astrolabe", "Where the planets are, to the arcminute.", C["coral"], (680, 560, 540, 220), [
        ("Zodiac math", 11, .10, .62), ("Ephemerides", 9, .30, .12), ("Kepler orbits", 7, .62, .30),
        ("PyEphem checks", 6, .92, .62), ("Real star catalogue", 6, .55, .95)], [(0, 1), (1, 2), (2, 3), (2, 4), (4, 0)]),
]


def skills_svg():
    W, H = 1280, 820
    desc = "; ".join(f"{name}: " + ", ".join(st[0] for st in stars_) for name, _, _, _, stars_, _ in SKY)
    glow = "".join(f'<radialGradient id="g{i}"><stop offset="0" stop-color="{col}" stop-opacity=".75"/>'
                   f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>'
                   for i, (_, _, col, _, _, _) in enumerate(SKY))
    css = ".ln{stroke-dasharray:6 7;animation:dash 14s linear infinite}@keyframes dash{to{stroke-dashoffset:-260}}"
    s = [card_open(W, H, "My skill sky: what I know, drawn as constellations", desc, glow, css)]
    s.append(stars(W, H, 260, seed=11))
    s.append(label(56, 70, "What I know  ·  drawn as constellations", 17))
    s.append(text(54, 130, "My skill sky", 52, C["ink"], SERIF))
    s.append(text(56, 172, "Bigger star = I reach for it more. Lines = things I use together.", 21, C["muted"]))
    for gi, (name, cap, col, (bx, by, bw, bh), pts, links) in enumerate(SKY):
        P = [(bx + 20 + fx * (bw - 40), by + 30 + fy * (bh - 60)) for _, _, fx, fy in pts]
        s.append(text(bx, by - 6, name, 30, col, SERIF, 400, "start", 'font-style="italic"'))
        s.append(text(bx + bw, by - 8, cap, 17, C["dim"], SANS, 400, "end"))
        for a, b in links:
            s.append(f'<line x1="{P[a][0]:.1f}" y1="{P[a][1]:.1f}" x2="{P[b][0]:.1f}" y2="{P[b][1]:.1f}" stroke="{col}" stroke-opacity=".5" stroke-width="1.6" class="ln"/>')
        for (lab, size, fx, fy), (x, y) in zip(pts, P):
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size * 3.2:.1f}" fill="url(#g{gi})" class="s s{1 + int(size) % 4}"/>')
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size * 0.55:.1f}" fill="#fffaf0"/>')
            right = fx < 0.75
            s.append(text(x + (size + 10) * (1 if right else -1), y + 7, lab, 21 if size >= 8 else 19, C["ink"], SANS,
                          600 if size >= 9 else 500, "start" if right else "end"))
    s.append(card_close(W, H))
    open(os.path.join(ROOT, "assets", "skills.svg"), "w").write("\n".join(s))


if __name__ == "__main__":
    about_svg()
    skills_svg()
    print("wrote assets/about.svg and assets/skills.svg")
