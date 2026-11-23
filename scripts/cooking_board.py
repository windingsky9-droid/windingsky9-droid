#!/usr/bin/env python3
"""Draw the 'shipped vs cooking' board: assets/board.svg.

Shipped is a hand-kept list. Cooking is read live from the open pull
requests in the project repo, so the board shows what is actually being
built this week. Runs every morning in .github/workflows/profile-live.yml.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

from svgkit import C, MONO, SANS, SERIF, card_close, card_open, esc, label, stars, text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "board.svg")
REPO = "windingsky9-droid/Ssushhii"

SHIPPED = [
    ("Celestial Observatory V15", "WebGL2 solar system. The black hole bends light.", "live"),
    ("Sky Wheel", "Real planets 1800–2050, checked at 240 dates", "live"),
    ("Halo Tactical Command Center V12", "3D replays that explain the angles", "v12"),
    ("Market Observatory", "Flask research dashboard, demo mode, 15 tests", "mvp"),
    ("Cargo Profit Engine", "Live lead-intel funnel: 8 accounts scored", "live"),
    ("Sushir 3D Studio", "Portfolio site with two live WebGL demos", "site"),
]


def open_prs():
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/pulls?state=open&per_page=50&sort=updated&direction=desc",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-board"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def age(iso):
    d = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).days
    if d < 1:
        return "today"
    if d < 14:
        return f"{d}d"
    if d < 60:
        return f"{d // 7}w"
    return f"{d // 30}mo"


def clip(s, n):
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def draw(prs):
    cooking = [p for p in prs if not p.get("title", "").lower().startswith(("bump ", "build(deps"))][:7]
    W = 1280
    rows = max(len(SHIPPED), len(cooking))
    H = 236 + rows * 92 + 40
    s = [card_open(W, H, "What I've shipped and what's cooking",
                   "Shipped: " + ", ".join(t for t, _, _ in SHIPPED) + ". Cooking: " + "; ".join(p["title"] for p in cooking))]
    s.append(stars(W, H, 60, seed=3, avoid=lambda x, y: y > 180))
    s.append(label(56, 70, "Work board  ·  cooking column reads my open pull requests", 17))
    s.append(text(54, 130, "Shipped, and still cooking", 48, C["ink"], SERIF))
    s.append(text(56, 172, f"{len(prs)} open pull requests in {REPO.split('/')[1]} right now. Updated every morning.", 21, C["muted"]))

    colw, x1, x2, top = 566, 56, 658, 206
    s.append(f'<circle cx="{x1 + 9}" cy="{top + 4}" r="8" fill="{C["mint"]}"/>')
    s.append(label(x1 + 28, top + 10, "Shipped", 17, C["mint"], 3))
    s.append(f'<circle cx="{x2 + 9}" cy="{top + 4}" r="8" fill="{C["coral"]}" class="s s2"/>')
    s.append(label(x2 + 28, top + 10, "Cooking", 17, C["coral"], 3))
    for i, (title, line, tag) in enumerate(SHIPPED):
        y = top + 30 + i * 92
        s.append(f'<rect x="{x1}" y="{y}" width="{colw}" height="78" rx="16" fill="{C["panel"]}" stroke="{C["line"]}"/>')
        s.append(f'<rect x="{x1}" y="{y}" width="5" height="78" rx="2.5" fill="{C["mint"]}"/>')
        s.append(text(x1 + 24, y + 33, title, 23, C["ink"], SANS, 600))
        s.append(text(x1 + 24, y + 60, line, 18, C["muted"]))
        s.append(text(x1 + colw - 20, y + 33, tag, 15, C["mint"], MONO, 600, "end"))
    for i, p in enumerate(cooking):
        y = top + 30 + i * 92
        draft = p.get("draft")
        s.append(f'<rect x="{x2}" y="{y}" width="{colw}" height="78" rx="16" fill="{C["panel"]}" stroke="{C["line"]}"/>')
        s.append(f'<rect x="{x2}" y="{y}" width="5" height="78" rx="2.5" fill="{C["coral"] if draft else C["gold"]}"/>')
        s.append(text(x2 + 24, y + 33, clip(p["title"], 44), 21, C["ink"], SANS, 600))
        s.append(text(x2 + 24, y + 60, f"#{p['number']} · {'draft' if draft else 'ready for review'} · opened {age(p['created_at'])} ago", 17, C["muted"], MONO))
    s.append(card_close(W, H))
    return "\n".join(s)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    prs = json.load(open(src)) if src else open_prs()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(draw(prs))
    print("wrote", OUT, len(prs), "open PRs")


if __name__ == "__main__":
    main()
