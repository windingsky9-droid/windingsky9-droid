#!/usr/bin/env python3
"""Draw a chess card from the public chess.com API: assets/chess.svg.

Runs every morning in .github/workflows/profile-live.yml. Only public data
is read (ratings, results, openings); no login is involved.
"""
import collections
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.request

from svgkit import C, MONO, SANS, SERIF, card_close, card_open, esc, label, stars, text

ACCOUNTS = ["windingsky", "ssushhii"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "chess.svg")
UA = {"User-Agent": "github-profile-chess-card/1.0"}
DRAWS = {"agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"}


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 + 3 * i)


NICE = {"Van t Kruijs": "Van 't Kruijs", "Queens Pawn": "Queen's Pawn", "Kings Pawn": "King's Pawn",
        "Bishops Opening": "Bishop's Opening", "Queens Gambit": "Queen's Gambit", "Kings Gambit": "King's Gambit",
        "Kings Indian": "King's Indian", "Queens Indian": "Queen's Indian", "Owens Defense": "Owen's Defense"}


def family(eco_url):
    """Opening family: 'Scandinavian Defense Mieses Kotrc Variation' -> 'Scandinavian Defense'."""
    if not eco_url:
        return None
    name = re.split(r"\s\d", eco_url.rsplit("/", 1)[-1].replace("-", " "))[0].strip()
    m = re.search(r"\b(Opening|Defense|Game|Gambit|Attack|System)\b", name)
    if m:
        name = name[: m.end()]
    for k, v in NICE.items():
        name = name.replace(k, v)
    return name


def collect():
    games, stats = [], {}
    for acct in ACCOUNTS:
        stats[acct] = get(f"https://api.chess.com/pub/player/{acct}/stats")
        for arc in get(f"https://api.chess.com/pub/player/{acct}/games/archives")["archives"]:
            for g in get(arc).get("games", []):
                if g.get("rules") != "chess":
                    continue
                color = "white" if g["white"]["username"].lower() == acct else "black"
                mine, opp = g[color], g["black" if color == "white" else "white"]
                res = mine["result"]
                outcome = "W" if res == "win" else ("D" if res in DRAWS else "L")
                games.append({"acct": acct, "end": g["end_time"], "tc": g["time_class"], "rating": mine.get("rating"),
                              "opp": opp.get("rating"), "out": outcome, "fam": family(g.get("eco")), "rated": g.get("rated", True)})
    games.sort(key=lambda x: x["end"])
    return games, stats


def sparkline(vals, x, y, w, h, col):
    if len(vals) < 2:
        return ""
    lo, hi = min(vals), max(vals)
    span = max(hi - lo, 1)
    pts = [(x + w * i / (len(vals) - 1), y + h - h * (v - lo) / span) for i, v in enumerate(vals)]
    d = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = f"{x:.1f},{y + h:.1f} " + d + f" {x + w:.1f},{y + h:.1f}"
    return (f'<polygon points="{area}" fill="{col}" fill-opacity=".10"/>'
            f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4.5" fill="{col}"/>')


def draw(games, stats):
    W, H = 1280, 640
    total = len(games)
    rec = collections.Counter(g["out"] for g in games)
    tiles = []  # (account, time class) with the most games first, up to four
    by = collections.defaultdict(list)
    for g in games:
        if g["rated"] and g["rating"] and g["tc"] in ("rapid", "blitz", "bullet"):
            by[(g["acct"], g["tc"])].append(g["rating"])
    keys = sorted(by, key=lambda k: (k[0] != ACCOUNTS[0], -len(by[k])))[:4]
    for k in keys:
        series = by[k]
        st = stats[k[0]].get(f"chess_{k[1]}", {})
        cur = st.get("last", {}).get("rating", series[-1])
        best = max(series)  # chess.com's "best" can be the default starting rating
        tiles.append((k, cur, best, series[-80:]))
    main_series = by.get(keys[0], []) if keys else []
    climbing = len(main_series) > 10 and main_series[-1] > main_series[max(0, len(main_series) - 40)]
    title = f"{total} games in. " + ("My rapid is climbing." if climbing and keys and keys[0][1] == "rapid" else "Still grinding.")

    s = [card_open(W, H, "Chess card: " + title, f"{rec['W']} wins, {rec['L']} losses, {rec['D']} draws on chess.com")]
    s.append(stars(W, H, 90, seed=7, avoid=lambda x, y: y < 200 or (200 < y < 600)))
    s.append(label(56, 70, "Chess  ·  pulled from chess.com every morning", 17))
    s.append(text(54, 130, title, 48, C["ink"], SERIF))
    s.append(text(56, 172, f"{' + '.join(ACCOUNTS)}  ·  {rec['W']} wins, {rec['L']} losses, {rec['D']} draws  ·  rapid, blitz and bullet", 21, C["muted"]))

    cols = [C["mint"], C["gold"], C["sky"], C["coral"]]
    tw, gap, x, y0 = 281, 15, 56, 206
    for i, ((acct, tc), cur, best, series) in enumerate(tiles):
        tx = x + i * (tw + gap)
        s.append(f'<rect x="{tx}" y="{y0}" width="{tw}" height="190" rx="18" fill="{C["panel"]}" stroke="{C["line"]}"/>')
        s.append(label(tx + 22, y0 + 34, f"{tc} · {acct}", 14, cols[i], 2))
        s.append(text(tx + 20, y0 + 96, str(cur), 56, C["ink"], SERIF))
        s.append(text(tx + tw - 22, y0 + 96, f"peak {best}", 18, C["muted"], MONO, 500, "end"))
        s.append(sparkline(series, tx + 22, y0 + 116, tw - 44, 52, cols[i]))

    # last ten results
    s.append(label(56, 450, "Last 10 games", 15, C["gold"], 3))
    for i, g in enumerate(games[-10:]):
        col = {"W": C["mint"], "L": C["coral"], "D": C["gold"]}[g["out"]]
        px = 56 + i * 54
        s.append(f'<rect x="{px}" y="468" width="46" height="46" rx="12" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-opacity=".7"/>')
        s.append(text(px + 23, 499, g["out"], 22, col, MONO, 700, "middle"))
    upset = max((g for g in games if g["out"] == "W" and g["opp"] and g["rating"]), key=lambda g: g["opp"] - g["rating"], default=None)
    if upset and upset["opp"] > upset["rating"]:
        s.append(text(56, 566, f"Best upset: beat a {upset['opp']} while rated {upset['rating']} (+{upset['opp'] - upset['rating']}).", 20, C["muted"]))

    # go-to openings
    fams = collections.defaultdict(list)
    for g in games:
        if g["fam"] and g["fam"] != "Undefined":
            fams[g["fam"]].append(g["out"])
    top = sorted(fams.items(), key=lambda kv: -len(kv[1]))[:4]
    ox = 700
    s.append(label(ox, 450, "Go-to openings · win rate", 15, C["gold"], 3))
    for i, (name, outs) in enumerate(top):
        yy = 486 + i * 32
        pct = round(100 * outs.count("W") / len(outs))
        s.append(text(ox, yy, f"{name}", 19, C["ink"]))
        s.append(text(ox + 330, yy, f"{len(outs)} games", 15, C["dim"], MONO, 500, "end"))
        bw = 150
        s.append(f'<rect x="{ox + 350}" y="{yy - 13}" width="{bw}" height="12" rx="6" fill="rgba(255,255,255,.08)"/>')
        s.append(f'<rect x="{ox + 350}" y="{yy - 13}" width="{bw * pct / 100:.1f}" height="12" rx="6" fill="{C["mint"] if pct >= 50 else C["coral"]}"/>')
        s.append(text(ox + 524, yy, f"{pct}%", 17, C["ink"], MONO, 600, "end"))
    s.append(text(W - 56, 612, "updated " + dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y"), 15, C["dim"], MONO, 500, "end"))
    s.append(card_close(W, H))
    return "\n".join(s)


def main():
    games, stats = collect()
    svg = draw(games, stats)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("wrote", OUT, len(games), "games")


if __name__ == "__main__":
    sys.exit(main())
