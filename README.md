<a href="https://sushir-3d-studio.floot.app"><img src="assets/hero.svg" width="100%" alt="SUSHIR: i build 3D you can fly through. i make APIs behave. i automate the boring stuff with n8n. i check my code against the actual sky."></a>

<p align="center">
  <a href="https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/celestial-observatory-cinematic.html"><b>▶ fly through my observatory</b></a> &nbsp;·&nbsp;
  <a href="https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/sky-wheel.html"><b>▶ spin the sky wheel</b></a> &nbsp;·&nbsp;
  <a href="https://sushir-3d-studio.floot.app">my studio</a> &nbsp;·&nbsp;
  <a href="https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/index.html">portfolio</a> &nbsp;·&nbsp;
  <a href="https://github.com/windingsky9-droid/Ssushhii/issues/new?template=service-request.yml">hire me</a>
  <br><br>
  <img src="https://komarev.com/ghpvc/?username=windingsky9-droid&label=people%20who%20scrolled%20this%20far&color=b8ff73&style=flat-square" alt="visitor count">
</p>

### hey, i'm sushir. sushi for short.

i build stuff you can **fly through**: real-time 3D, live star charts, and little machines that explain themselves.<br>
self-taught. i came up picking orders in warehouses and taught myself to code by building the things i wanted to stare at.<br>
i learn in pictures. if i can't see it, i don't get it, so i build the picture first.

> [!TIP]
> **open to work:** AI automation · implementation · solutions engineering · creative / data-viz dev. remote is perfect.
> [let's talk →](https://github.com/windingsky9-droid/Ssushhii/issues/new?template=service-request.yml)

<img src="assets/achievements.svg" width="100%" alt="Achievements unlocked: 0.006° Club, Star Cartographer, Event Horizon, Green Across the Board, Featured Forger, Any% Self-Taught, Headshot Machine">

<img src="assets/orbit.svg" width="100%" alt="My stack as a solar system. three.js and WebGL are the sun; JavaScript and GLSL orbit closest, then Python, Flask and REST APIs, then n8n, PyTorch and Blender Python, then Playwright, pytest, GitHub Actions and Canvas/SVG.">

## stuff i built 🛰️

<table>
  <tr>
    <td width="58%" valign="top">
      <a href="https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/celestial-observatory-cinematic.html"><img src="assets/celestial-observatory-v14-hero.jpg" alt="Celestial Observatory: a ringed giant and its sign tiles in front of a real star field"></a>
    </td>
    <td valign="top">
      <h3>celestial observatory</h3>
      <b>in plain words:</b> a little universe in your browser. six planets, one sun, 3,232 real stars, and a black hole you can fly up to.<br><br>
      <b>the hard part:</b> making <b>EREBUS</b>, the black hole, bend light into a real Einstein ring while everything still runs live.<br><br>
      <a href="https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/celestial-observatory-cinematic.html"><b>▶ launch it</b></a> · jump to
      <a href="https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/celestial-observatory-cinematic.html?shot=erebus">the black hole</a>,
      <a href="https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/celestial-observatory-cinematic.html?shot=pulsar">the pulsar</a>,
      <a href="https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/celestial-observatory-cinematic.html?shot=sky">the real sky</a> or
      <a href="https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/celestial-observatory-cinematic.html?tour">the narrated tour</a>
    </td>
  </tr>
</table>

<p align="center">
  <img src="assets/erebus-loop.gif" width="32%" alt="EREBUS: the accretion disk bends over the shadow into an Einstein ring">
  <img src="assets/celestial-observatory-v15-sky.jpg" width="32%" alt="The real sky behind the observatory: Leo behind its sign tile">
  <img src="assets/celestial-observatory-v14-wheel.jpg" width="32%" alt="The observatory HUD with its chart wheel">
</p>

### [sky wheel](https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/sky-wheel.html)

<img align="right" width="320" src="assets/sky-wheel-card.jpg" alt="Sky Wheel: a chart of the real sky with stars and constellations behind the zodiac">

**in plain words:** pick any moment from 1800 to 2050 and see exactly where the sun, moon and every planet were, on top of the real constellations. it has a compare mode for two moments and makes a 2400×3200 print poster.

**the hard part:** being *right*. here's how it works:

```mermaid
flowchart LR
  A["📅 any date + place"] --> B["🧮 my ephemeris<br/>pure JS, no APIs"]
  B --> C["🪐 where every planet is"]
  C --> D["🎡 the wheel + 3,232 real stars"]
  B -.->|checked 240×| E["🔭 PyEphem"]
```

**[▶ open it](https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/sky-wheel.html)** · [moon landing vs. today](https://rawcdn.githack.com/windingsky9-droid/Ssushhii/577dedc7c30d6bafe16ef8f09178a832e075afe0/portfolio/demos/sky-wheel.html?cmp=1&d=1969-07-20T15:17&tz=America/Chicago&place=Houston&n1=Moon%20landing&n2=Today) · [source](https://github.com/windingsky9-droid/Ssushhii/blob/main/portfolio/demos/sky-wheel.html)

<br clear="right">

### [halo tactical command center](https://github.com/windingsky9-droid/Ssushhii/tree/main/showcase)

**in plain words:** a 3D war room for Halo matches: replay a round, see the routes, and hit director mode for the cinematic cut.<br>
<sub>tactical values are modeled demo values, not official Halo telemetry.</sub>

### [market observatory](https://github.com/windingsky9-droid/Ssushhii)

**in plain words:** a stock research dashboard you can try for free, because demo mode runs on built-in sample data.<br>
**the boring-but-important part:** a clean provider boundary, JSON endpoints, 15 automated tests on every push, and desktop + mobile checked in a real browser.

<img src="assets/brain.svg" width="100%" alt="How my brain works: see something cool, ask ok but how, find the math, build the ugly version, make it cinematic, check it against reality, ship it, then see something cooler.">

## proof, not vibes 📏

| what | the number | how i checked |
|---|---|---|
| sun position | **0.006°** RMS error | vs PyEphem at 240 dates |
| moon position | **0.028°** RMS error | same test |
| every planet | **under 0.1°** | same test |
| birth-chart engine | **≤ 0.16°** off | vs independently verified charts |
| 3D detail pass | **98 → 148** meshes | framerate unchanged |
| market observatory | **15 / 15** tests | pytest in CI on every push |

## today's sky 🌙

<img src="assets/today-sky.svg" width="100%" alt="Today's moon phase, where every planet sits on the zodiac belt, and a fortune of the day">
<sub>a GitHub Action wakes up every morning, runs my own ephemeris (pure JS, no APIs) and redraws this card. come back tomorrow: new moon phase, new fortune.</sub>

<details>
<summary><b>🌀 click for silly mode</b></summary>
<br>

- **"sushir"** started as a halo reach roleplay name. i played a saxon. my friends never let it go.
- i'm credited as a **forger** on halo waypoint's *Forge Features*. i build maps when i'm not building skies.
- **76% headshots** in halo infinite, last time i checked. my css is less accurate.
- i own a **blue '03 strat**. it has spent more time in pieces than my side projects.
- my monitor does **320hz**. my shaders do 60fps. we don't talk about it.
- i think out loud. half my best code started as me talking to myself.
- favorite debugging move: turn the bug into a 3D scene so i can actually *see* it.
- i once checked planet positions against an astronomy library 240 times. for fun.

</details>

## in the lab 🧪

- **forward pass:** a neural net you can watch think, in 3D. every layer lights up as it decides.
- **two skies:** two people's birth charts as glowing 3D rings, with a thread for every connection between them.
- **today's sky, but huge:** the card above, as a full live scene.

## hire me for small stuff 🔧

- **flask / REST API fixes** from **$40**, once we confirm the exact issue → [open a brief](https://github.com/windingsky9-droid/Ssushhii/issues/new?template=service-request.yml)
- **n8n automations:** your apps talking to each other so the boring stuff runs itself
- **a chart, a dashboard, or a whole 3D scene** for your data

<p align="center"><img src="assets/divider.svg" width="100%" alt=""></p>
<p align="center"><sub>made at 2am with a 320hz monitor and way too many tabs open. thanks for scrolling this far 🫡</sub></p>
