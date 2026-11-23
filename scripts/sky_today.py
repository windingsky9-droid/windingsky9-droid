#!/usr/bin/env python3
"""Draw the real sky for today as a zodiac wheel: assets/sky-today.svg.

The workflow in .github/workflows/sky-today.yml runs this every morning and
commits the new picture. Positions come from Astronomy Engine
(pip install astronomy-engine): geocentric, tropical zodiac, true ecliptic
of date. They agree with the Sky Wheel demo to a few arcminutes.

Usage: python scripts/sky_today.py [YYYY-MM-DDTHH:MM]   (UTC, default: now)
"""
import datetime as dt
import math
import os
import sys

import astronomy as ae

from svgkit import (C, ELEMENT, ELEMENT_COLOR, MONO, SANS, SERIF, SIGN_NAMES, SIGNS,
                    card_close, card_open, esc, glyph, label, polar, stars, text)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "sky-today.svg")

BODIES = [
    ("sun", "Sun", ae.Body.Sun, C["gold"]),
    ("moon", "Moon", ae.Body.Moon, "#e8ecff"),
    ("mercury", "Mercury", ae.Body.Mercury, C["sky"]),
    ("venus", "Venus", ae.Body.Venus, C["mint"]),
    ("mars", "Mars", ae.Body.Mars, C["coral"]),
    ("jupiter", "Jupiter", ae.Body.Jupiter, C["amber"]),
    ("saturn", "Saturn", ae.Body.Saturn, "#e6c27a"),
    ("uranus", "Uranus", ae.Body.Uranus, "#7fe3ff"),
    ("neptune", "Neptune", ae.Body.Neptune, "#8fa8ff"),
    ("pluto", "Pluto", ae.Body.Pluto, C["lav"]),
]
ASPECTS = [  # name, angle, orb, symbol word, colour
    ("conjunction", 0, 8, "teams up with", C["gold"]),
    ("sextile", 60, 4, "opens a door for", C["mint"]),
    ("square", 90, 6, "pushes against", C["coral"]),
    ("trine", 120, 6, "flows with", C["mint"]),
    ("opposition", 180, 8, "pulls against", C["coral"]),
]
PHASES = ["New Moon", "Waxing crescent", "First quarter", "Waxing gibbous",
          "Full Moon", "Waning gibbous", "Last quarter", "Waning crescent"]


def lon(body, t):
    if body == ae.Body.Sun:
        return ae.SunPosition(t).elon % 360
    if body == ae.Body.Moon:
        return ae.EclipticGeoMoon(t).lon % 360
    return ae.Ecliptic(ae.GeoVector(body, t, True)).elon % 360


def signed(d):
    return (d + 180) % 360 - 180


def dms(l):
    d = l % 30
    deg, mins = int(d), int(round((d - int(d)) * 60))
    if mins == 60:
        deg, mins = deg + 1, 0
    return f"{deg}°{mins:02d}′"


def spread(angles, min_sep):
    """Nudge display angles apart so glyphs never overlap (keeps order)."""
    order = sorted(range(len(angles)), key=lambda i: angles[i])
    disp = [angles[i] for i in order]
    n = len(disp)
    for _ in range(400):
        moved = False
        for k in range(n):
            a, b = disp[k], disp[(k + 1) % n] + (360 if k == n - 1 else 0)
            gap = b - a
            if gap < min_sep:
                push = (min_sep - gap) / 2 + 0.01
                disp[k] -= push
                disp[(k + 1) % n] += push
                moved = True
        if not moved:
            break
    res = [0.0] * n
    for k, i in enumerate(order):
        res[i] = disp[k] % 360
    return res


def compute(when):
    t = ae.Time.Make(when.year, when.month, when.day, when.hour, when.minute, 0)
    rows = []
    for key, name, body, col in BODIES:
        l0 = lon(body, t)
        speed = signed(lon(body, t.AddDays(0.5)) - lon(body, t.AddDays(-0.5)))
        rows.append({"key": key, "name": name, "lon": l0, "speed": speed, "col": col,
                     "sign": int(l0 // 30), "retro": speed < 0})
    phase = ae.MoonPhase(t)
    illum = ae.Illumination(ae.Body.Moon, t).phase_fraction
    full = ae.SearchMoonPhase(180, t, 40)
    new = ae.SearchMoonPhase(0, t, 40)
    sun_next = (int(rows[0]["lon"] // 30) + 1) % 12
    ingress = ae.SearchSunLongitude(sun_next * 30, t, 40)
    aspects = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            sep = abs(signed(rows[i]["lon"] - rows[j]["lon"]))
            for name, ang, orb, word, col in ASPECTS:
                extra = 2 if rows[i]["key"] in ("sun", "moon") or rows[j]["key"] in ("sun", "moon") else 0
                if abs(sep - ang) <= orb + extra:
                    aspects.append({"a": i, "b": j, "name": name, "word": word, "col": col, "orb": abs(sep - ang)})
    aspects.sort(key=lambda a: a["orb"])
    return {"t": t, "when": when, "rows": rows, "phase": phase, "illum": illum, "full": full, "new": new,
            "ingress": ingress, "ingress_sign": sun_next, "aspects": aspects}


def days_until(t_from, t_to):
    d = t_to.ut - t_from.ut
    if d < 1:
        return "in under a day"
    n = round(d)
    return f"in {n} day" + ("s" if n != 1 else "")


def moon_disk(cx, cy, r, phase_deg):
    """Moon drawn by its phase angle: 0 new, 90 first quarter, 180 full."""
    p = math.radians(phase_deg)
    k = math.cos(p)  # +1 new ... -1 full
    lit = "#f3f1e6"
    dark = "#1a2140"
    waxing = phase_deg < 180
    # lit half: right side while waxing (northern-hemisphere view)
    sweep_half = 1 if waxing else 0
    rx = abs(k) * r
    # terminator ellipse bulges toward the dark side when crescent, the lit side when gibbous
    term_sweep = (0 if k > 0 else 1) if waxing else (1 if k > 0 else 0)
    d = (f"M {cx} {cy - r} A {r} {r} 0 0 {sweep_half} {cx} {cy + r} "
         f"A {rx:.2f} {r} 0 0 {term_sweep} {cx} {cy - r} Z")
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{dark}" stroke="rgba(255,255,255,.25)"/>'
            f'<path d="{d}" fill="{lit}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="none" stroke="{C["gold"]}" stroke-opacity=".25"/>')


def draw(data):
    W, H = 1280, 960
    t = data["t"]
    when = data["when"]
    rows = data["rows"]
    sun, moon = rows[0], rows[1]
    cx, cy, R1, R2, RP, RA = 372, 548, 292, 228, 182, 132

    css = (".spin{transform-origin:%dpx %dpx;animation:spin 240s linear infinite}"
           "@keyframes spin{to{transform:rotate(-360deg)}}"
           ".pulse{animation:pulse 3.2s ease-in-out infinite alternate}"
           "@keyframes pulse{from{opacity:.35}to{opacity:.9}}" % (cx, cy))
    defs = (f'<radialGradient id="sunglow"><stop offset="0" stop-color="{C["gold"]}" stop-opacity=".9"/>'
            f'<stop offset="1" stop-color="{C["gold"]}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="core" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#18245a"/>'
            f'<stop offset="1" stop-color="#070b1f"/></radialGradient>')
    title = f"The sky right now: Sun in {SIGN_NAMES[sun['sign']]}, Moon in {SIGN_NAMES[moon['sign']]}"
    desc = "; ".join(f"{r['name']} {dms(r['lon'])} {SIGN_NAMES[r['sign']]}{' retrograde' if r['retro'] else ''}" for r in rows)
    s = [card_open(W, H, title, desc, defs, css)]
    def busy(x, y):  # keep stars off the wheel and out of every text block
        return ((x - cx) ** 2 + (y - cy) ** 2 < (R1 + 24) ** 2 or (y < 190 and x < 1020)
                or (x > 712 and 222 < y < 850) or y > 868)
    s.append(stars(W, H, 230, seed=when.toordinal(), avoid=busy))

    # header
    s.append(label(56, 70, "The sky right now  ·  redrawn every morning", 17))
    s.append(text(54, 132, f"Sun in {SIGN_NAMES[sun['sign']]}, Moon in {SIGN_NAMES[moon['sign']]}", 50, C["ink"], SERIF, 400))
    s.append(text(56, 176, when.strftime("%A %d %B %Y").replace(" 0", " ") + "  ·  " + when.strftime("%H:%M") +
                  " UTC  ·  real positions, computed by this repo's GitHub Action", 21, C["muted"]))

    # wheel: sign band (rotates very slowly), ticks, glyph ring
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R1 + 18}" fill="none" stroke="{C["gold"]}" stroke-opacity=".12"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R2}" fill="url(#core)"/>')
    band = []
    for i, sg in enumerate(SIGNS):
        col = ELEMENT_COLOR[ELEMENT[i % 4]]
        a0, a1 = i * 30, (i + 1) * 30
        p0o, p1o = polar(cx, cy, R1, a0), polar(cx, cy, R1, a1)
        p1i, p0i = polar(cx, cy, R2, a1), polar(cx, cy, R2, a0)
        band.append(f'<path d="M {p0o[0]:.1f} {p0o[1]:.1f} A {R1} {R1} 0 0 0 {p1o[0]:.1f} {p1o[1]:.1f} '
                    f'L {p1i[0]:.1f} {p1i[1]:.1f} A {R2} {R2} 0 0 1 {p0i[0]:.1f} {p0i[1]:.1f} Z" '
                    f'fill="{col}" fill-opacity="{0.16 if i % 2 == 0 else 0.10}" stroke="rgba(255,255,255,.12)"/>')
        gx, gy = polar(cx, cy, (R1 + R2) / 2, a0 + 15)
        band.append(glyph(sg, gx, gy, 40, col))
    s.append("\n".join(band))
    ticks = []
    for d in range(360):
        L = 14 if d % 10 == 0 else (9 if d % 5 == 0 else 5)
        x0, y0 = polar(cx, cy, R2, d)
        x1, y1 = polar(cx, cy, R2 - L, d)
        ticks.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="rgba(226,233,255,{0.55 if L > 5 else 0.28})" stroke-width="{1.4 if L > 9 else 1}"/>')
    s.append("\n".join(ticks))

    # aspect web
    for a in data["aspects"]:
        p, q = rows[a["a"]], rows[a["b"]]
        x0, y0 = polar(cx, cy, RA, p["lon"])
        x1, y1 = polar(cx, cy, RA, q["lon"])
        dash = ' stroke-dasharray="6 6"' if a["name"] in ("sextile",) else ""
        s.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{a["col"]}" stroke-opacity=".75" stroke-width="2"{dash}/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{RA}" fill="none" stroke="rgba(226,233,255,.18)"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#9fd0ff"/><circle cx="{cx}" cy="{cy}" r="13" fill="none" stroke="#9fd0ff" stroke-opacity=".35"/>')

    # planets
    disp = spread([r["lon"] for r in rows], 11.5)
    for r, da in zip(rows, disp):
        tx, ty = polar(cx, cy, R2 - 16, r["lon"])
        ex, ey = polar(cx, cy, RP + 22, da)
        gx, gy = polar(cx, cy, RP, da)
        s.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{r["col"]}" stroke-opacity=".6" stroke-width="1.4"/>')
        s.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="3.2" fill="{r["col"]}"/>')
        if r["key"] == "sun":
            s.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="34" fill="url(#sunglow)" class="pulse"/>')
        s.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="21" fill="#0a1030" stroke="{r["col"]}" stroke-opacity=".8" stroke-width="1.6"/>')
        s.append(glyph(r["key"], gx, gy, 27, r["col"]))
        lx, ly = polar(cx, cy, RP - 40, da)
        s.append(text(lx, ly + 6, dms(r["lon"]), 15, C["muted"], MONO, 500, "middle"))

    # right panel: ephemeris table
    x0 = 732
    s.append(label(x0, 250, "Where everything is", 16, C["gold"], 3))
    s.append(f'<line x1="{x0}" y1="266" x2="1224" y2="266" stroke="{C["line"]}"/>')
    y = 304
    for r in rows:
        s.append(glyph(r["key"], x0 + 16, y - 8, 24, r["col"]))
        s.append(text(x0 + 46, y, r["name"], 22, C["ink"]))
        s.append(glyph(SIGNS[r["sign"]], x0 + 190, y - 8, 22, ELEMENT_COLOR[ELEMENT[r["sign"] % 4]]))
        s.append(text(x0 + 214, y, SIGN_NAMES[r["sign"]], 22, C["ink"]))
        s.append(text(x0 + 352, y, dms(r["lon"]), 21, C["muted"], MONO, 500))
        if r["retro"]:
            s.append(text(1224, y, "retro", 16, C["coral"], MONO, 600, "end"))
        s.append(f'<line x1="{x0}" y1="{y + 14}" x2="1224" y2="{y + 14}" stroke="{C["line"]}" stroke-opacity=".6"/>')
        y += 40

    # aspects in plain words
    y += 26
    s.append(label(x0, y, "Tightest aspects", 16, C["gold"], 3))
    y += 34
    for a in data["aspects"][:3]:
        p, q = rows[a["a"]], rows[a["b"]]
        s.append(f'<circle cx="{x0 + 7}" cy="{y - 7}" r="6" fill="{a["col"]}"/>')
        s.append(text(x0 + 24, y, f"{p['name']} {a['word']} {q['name']}", 21, C["ink"]))
        s.append(text(1224, y, f"{a['name']} · {a['orb']:.1f}°", 16, C["dim"], MONO, 500, "end"))
        y += 34

    # moon phase + what's next
    ph = data["phase"]
    name = PHASES[int(((ph + 22.5) % 360) // 45)]
    s.append(f'<line x1="56" y1="872" x2="1224" y2="872" stroke="{C["line"]}"/>')
    s.append(moon_disk(86, 914, 26, ph))
    s.append(text(134, 908, f"{name}, {data['illum'] * 100:.0f}% lit", 22, C["ink"]))
    nxt_full, nxt_new = data["full"], data["new"]
    upcoming = (f"Full Moon {days_until(t, nxt_full)}" if nxt_full.ut < nxt_new.ut else f"New Moon {days_until(t, nxt_new)}")
    s.append(text(134, 936, f"{upcoming}  ·  Sun enters {SIGN_NAMES[data['ingress_sign']]} {days_until(t, data['ingress'])}", 18, C["muted"]))
    s.append(text(1224, 936, "Astronomy Engine · tropical zodiac · geocentric", 15, C["dim"], MONO, 500, "end"))
    s.append(card_close(W, H))
    return "\n".join(s)


def main():
    if len(sys.argv) > 1:
        when = dt.datetime.fromisoformat(sys.argv[1]).replace(tzinfo=dt.timezone.utc)
    else:
        when = dt.datetime.now(dt.timezone.utc).replace(second=0, microsecond=0)
    svg = draw(compute(when))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("wrote", OUT, when.isoformat())


if __name__ == "__main__":
    main()
