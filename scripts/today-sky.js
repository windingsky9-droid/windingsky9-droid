#!/usr/bin/env node
/* Redraws assets/today-sky.svg: today's moon phase, where every planet sits on the zodiac belt,
   and a fortune of the day. Positions come from scripts/sky.js (my own ephemeris). No APIs.
   Usage: node scripts/today-sky.js [ISO date] [output path] */
const fs = require('fs'), path = require('path');
const Sky = require('./sky.js');

const now = process.argv[2] ? new Date(process.argv[2]) : new Date();
const OUT = process.argv[3] || path.join(__dirname, '..', 'assets', 'today-sky.svg');
const RAD = Math.PI / 180, rev = x => ((x % 360) + 360) % 360, r1 = n => Math.round(n * 10) / 10;
const SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
const ELEM = ['#ff6576', '#71efb7', '#6fe9ff', '#68a8ff'];
const MONO = `font-family="ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"`;

const pos = Sky.positions(now), nxt = Sky.positions(new Date(now.getTime() + 864e5));
const elong = t => { const p = Sky.positions(t); return rev(p.Moon.lon - p.Sun.lon); };
const E = rev(pos.Moon.lon - pos.Sun.lon), lit = (1 - Math.cos(E * RAD)) / 2;
const PHASES = ['New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 'Full Moon', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent'];
const phase = PHASES[Math.floor(rev(E + 22.5) / 45) % 8];
function daysUntil(target) {
  let prev = E;
  for (let h = 1; h <= 24 * 31; h++) {
    const e = elong(new Date(now.getTime() + h * 36e5));
    if (target === 180 ? prev < 180 && e >= 180 : prev > 300 && e < 60) return h / 24;
    prev = e;
  }
  return null;
}
const toFull = daysUntil(180), toNew = daysUntil(0);
const soon = toFull <= toNew ? ['full moon', toFull] : ['new moon', toNew];
const soonText = soon[1] < .75 ? `${soon[0]} tonight` : `${soon[0]} in ${Math.round(soon[1])} day${Math.round(soon[1]) === 1 ? '' : 's'}`;

const FORTUNES = [
  "your bug isn't in the code you're staring at. it's in the code you trust.",
  'ship the ugly version. nobody can fly through a plan.',
  'if it works on the first try, check it again.',
  "mercury isn't retrograde. that bug is yours.",
  "a 320hz monitor can't make a 12fps shader feel fast.",
  'learn the math once. use it forever.',
  'today is a good day to delete something.',
  'every pro was once someone googling the basics at 2am.',
  'make it work. make it right. then make it glow.',
  "if you can't see it, draw it. then you'll get it.",
  'nobody reads the docs. be the one who does.',
  'your future self is your most important user. leave comments.',
  'the sky kept perfect time for 4.5 billion years. your timestamps can use UTC.',
  'commit early. commit often. push before you sleep.',
  'the boring stuff is an automation waiting to happen.',
  "a good error message is a love letter to whoever's next.",
  "ask 'ok but how?' one more time than everyone else.",
  "you don't need permission to build the thing.",
  'refactor like you are moving out: keep only what you use.',
  "today's forecast: 100% chance of npm install.",
  'measure twice, deploy once.',
  'stay curious. stay hydrated. stay in version control.',
  'the camera is the story. frame it.',
  'every API is friendly once you read its errors.',
  'right item, right place, every time. warehouse rules work on code too.',
  "you're not stuck. you're loading.",
  "build the thing you'd stare at.",
  'cinematic is a setting. turn it on.',
  'the best tutorial is the bug you fixed yourself.',
  'one tiny automation today saves a thousand clicks this year.',
  'respect the frame budget. 16.6 ms is all you get.',
  'shaders are just math wearing sunglasses.',
  "today's lucky number: 0.006",
  'your code compiles. the vibes are immaculate.',
  'a full moon is just the sun showing off. you can too.',
  'if the map is wrong, forge a new one.',
  'clutch round? no. clutch commit.',
  'slow is smooth. smooth is fast. fast is shipped.',
  'when in doubt, log it out.',
  'the planets never skip leg day. do your tests.',
  "rest is part of the build. the moon doesn't stay full either.",
  'a blank file is just a sky before the stars load.',
  "it's not a bug, it's an unplanned feature. still fix it.",
  'stack overflow called. it misses you.',
  'one more feature? finish the last one first.',
  'git blame is just astrology for code.',
];
const day = Math.floor(now.getTime() / 864e5);
const fortune = FORTUNES[(day * 17 + 5) % FORTUNES.length];
const wrap = (s, n) => { const out = ['']; for (const w of s.split(' ')) { if ((out[out.length - 1] + ' ' + w).trim().length > n) out.push(w); else out[out.length - 1] = (out[out.length - 1] + ' ' + w).trim(); } return out; };

let seed = day * 9301 + 49297; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
const W = 1200, H = 400;
let s = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Today's sky: ${phase}, ${Math.round(lit * 100)} percent lit, moon in ${SIGNS[Math.floor(pos.Moon.lon / 30)]}. Fortune: ${fortune.replace(/[<&"]/g, '')}"><title>today's sky</title>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1120"/><stop offset=".55" stop-color="#05070b"/><stop offset="1" stop-color="#0b0a18"/></linearGradient>
<radialGradient id="ml" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#fffaf0"/><stop offset=".6" stop-color="#e3dccd"/><stop offset="1" stop-color="#a8a092"/></radialGradient>
<radialGradient id="mg"><stop offset="0" stop-color="#fff4dc" stop-opacity=".9"/><stop offset="1" stop-color="#fff4dc" stop-opacity="0"/></radialGradient>
<filter id="b" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="5"/></filter></defs>
<rect width="${W}" height="${H}" rx="26" fill="url(#bg)"/>`;
for (let i = 0; i < 150; i++) s += `<circle cx="${r1(rnd() * W)}" cy="${r1(rnd() * H)}" r="${r1(.3 + rnd() * .9)}" fill="#fff" opacity="${(.15 + rnd() * .5).toFixed(2)}"/>`;

// header
const WD = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'][now.getUTCDay()], MO = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'][now.getUTCMonth()];
const hh = String(now.getUTCHours()).padStart(2, '0'), mm = String(now.getUTCMinutes()).padStart(2, '0');
s += `<circle cx="47" cy="47" r="5" fill="#b8ff73"/><text x="62" y="52" ${MONO} font-size="14" font-weight="700" letter-spacing="3" fill="#b8ff73">TODAY'S SKY</text>`;
s += `<text x="1160" y="52" text-anchor="end" ${MONO} font-size="13" letter-spacing="2" fill="#93a2b3">${WD} ${now.getUTCDate()} ${MO} ${now.getUTCFullYear()} · ${hh}:${mm} UTC</text>`;

// moon
const mx = 200, my = 196, mr = 84;
const c = Math.cos(E * RAD), tx = Math.abs(c) * mr, waxing = E < 180;
const limb = `M ${mx} ${my - mr} A ${mr} ${mr} 0 0 ${waxing ? 1 : 0} ${mx} ${my + mr}`;
const sweep = waxing ? (E < 90 ? 0 : 1) : (E > 270 ? 1 : 0);
const litPath = `${limb} A ${r1(tx)} ${mr} 0 0 ${sweep} ${mx} ${my - mr} Z`;
s += `<circle cx="${mx}" cy="${my}" r="${mr + 30}" fill="url(#mg)" opacity="${(.05 + .3 * lit).toFixed(2)}"/>`;
s += `<circle cx="${mx}" cy="${my}" r="${mr}" fill="#121a29" stroke="rgba(224,242,255,.16)"/><clipPath id="lc"><path d="${litPath}"/></clipPath>`;
s += `<path d="${litPath}" fill="url(#ml)"/><g clip-path="url(#lc)" fill="#5a5046" opacity=".2">`;
[[-30, -22, 11], [22, 28, 15], [36, -36, 8], [-12, 44, 9], [-46, 14, 7], [8, -4, 6], [48, 6, 5]].forEach(([dx, dy, r]) => { s += `<circle cx="${mx + dx}" cy="${my + dy}" r="${r}"/>`; });
s += `</g>`;
s += `<text x="${mx}" y="318" text-anchor="middle" ${MONO} font-size="18" font-weight="700" fill="#f4f8fc">${phase.toUpperCase()}</text>`;
s += `<text x="${mx}" y="342" text-anchor="middle" ${MONO} font-size="13" fill="#93a2b3">${Math.round(lit * 100)}% lit · moon in ${SIGNS[Math.floor(pos.Moon.lon / 30)]}</text>`;
s += `<text x="${mx}" y="364" text-anchor="middle" ${MONO} font-size="13" fill="#6fe9ff">${soonText}</text>`;

// zodiac belt with every planet
const bx = 400, bw = 760, by = 150, bh = 56, X = lon => bx + lon / 360 * bw;
s += `<rect x="${bx}" y="${by}" width="${bw}" height="${bh}" rx="12" fill="rgba(15,22,31,.78)" stroke="rgba(224,242,255,.14)"/>`;
for (let i = 0; i < 12; i++) {
  const x0 = X(i * 30);
  s += `<rect x="${r1(x0 + 1)}" y="${by + 1}" width="${r1(bw / 12 - 2)}" height="${bh - 2}" rx="${i === 0 || i === 11 ? 11 : 2}" fill="${ELEM[i % 4]}" opacity=".07"/>`;
  if (i) s += `<line x1="${r1(x0)}" y1="${by + 6}" x2="${r1(x0)}" y2="${by + bh - 6}" stroke="rgba(224,242,255,.12)"/>`;
  s += `<text x="${r1(x0 + bw / 24)}" y="${by + 16}" text-anchor="middle" ${MONO} font-size="9.5" letter-spacing="1" fill="#6c7b8c">${SIGNS[i].slice(0, 3).toUpperCase()}</text>`;
}
const BODIES = [['Sun', 9, '#ffc979'], ['Moon', 7, '#ece6da'], ['Mercury', 4.5, '#c9c3ff'], ['Venus', 5.5, '#ff72b0'], ['Mars', 5, '#ff6576'],
  ['Jupiter', 6.5, '#ffb36b'], ['Saturn', 6, '#e9cf8f'], ['Uranus', 5, '#6fe9ff'], ['Neptune', 5, '#68a8ff'], ['Pluto', 3.5, '#a891ff']];
const cy = by + 36;
const marks = BODIES.map(([n, r, col]) => {
  const lon = pos[n].lon, retro = n !== 'Sun' && n !== 'Moon' && rev(nxt[n].lon - lon + 180) - 180 < 0;
  const label = `${n} ${Math.floor(lon % 30)}° ${SIGNS[Math.floor(lon / 30)].slice(0, 3)}${retro ? ' rx' : ''}`;
  return { n, r, col, x: X(lon), label, w: label.length * 7.2 };
}).sort((a, b) => a.x - b.x);
const rows = [{ y: 128, end: -1e9 }, { y: 238, end: -1e9 }, { y: 110, end: -1e9 }, { y: 256, end: -1e9 }];
for (const m of marks) {
  const lx = Math.min(Math.max(m.x - m.w / 2, bx), bx + bw - m.w);
  const row = rows.find(r => lx > r.end + 10) || rows.reduce((a, b) => (a.end < b.end ? a : b));
  row.end = lx + m.w; m.lx = lx; m.ly = row.y;
}
for (const m of marks) {
  const up = m.ly < by;
  s += `<line x1="${r1(m.x)}" y1="${up ? by - 2 : by + bh + 2}" x2="${r1(m.x)}" y2="${up ? m.ly + 5 : m.ly - 13}" stroke="${m.col}" stroke-opacity=".35"/>`;
  s += `<circle cx="${r1(m.x)}" cy="${cy}" r="${m.r * 2.2}" fill="${m.col}" opacity=".35" filter="url(#b)"/><circle cx="${r1(m.x)}" cy="${cy}" r="${m.r}" fill="${m.col}"/>`;
  if (m.n === 'Saturn') s += `<ellipse cx="${r1(m.x)}" cy="${cy}" rx="${m.r * 2}" ry="${m.r * .55}" fill="none" stroke="${m.col}" stroke-width="1.2" transform="rotate(-18 ${r1(m.x)} ${cy})"/>`;
  s += `<text x="${r1(m.lx)}" y="${m.ly}" ${MONO} font-size="12" fill="#93a2b3"><tspan fill="${m.col}" font-weight="700">${m.label.split(' ')[0]}</tspan> ${m.label.split(' ').slice(1).join(' ')}</text>`;
}

// fortune
s += `<text x="${bx}" y="300" ${MONO} font-size="12" font-weight="700" letter-spacing="2.5" fill="#b8ff73">› FORTUNE OF THE DAY</text>`;
wrap(fortune, 62).slice(0, 2).forEach((line, i) => { s += `<text x="${bx}" y="${330 + i * 26}" ${MONO} font-size="18" fill="#f4f8fc">${line.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</text>`; });
s += `<text x="40" y="${H - 16}" ${MONO} font-size="11" fill="#55657a">redrawn every morning by a github action · positions from my own JS ephemeris (Schlyter's method) · no APIs</text>`;
s += `<rect x=".5" y=".5" width="${W - 1}" height="${H - 1}" rx="25.5" fill="none" stroke="rgba(224,242,255,.13)"/></svg>\n`;
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, s);
console.log(`today's sky -> ${OUT} | ${phase} ${Math.round(lit * 100)}% | ${soonText} | ${fortune}`);
