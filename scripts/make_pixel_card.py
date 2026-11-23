"""Generate assets/pixel-card.svg: an animated pixel-art portrait + typing terminal.

Usage: python3 scripts/make_pixel_card.py path/to/photo.png
Needs Pillow. Output is a self-contained SVG (CSS animations only) that GitHub
renders inside <img>.
"""
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageEnhance

GRID = 56          # pixels per side of the portrait
PX = 5             # rendered size of one pixel
COLORS = 40        # palette size after quantisation
CYCLE = 12         # seconds per animation loop
W, H = 860, 340
PORTRAIT_X, PORTRAIT_Y = 30, 26

random.seed(7)

src = Image.open(sys.argv[1]).convert("RGB")
w, h = src.size
# Crop to head + upper jacket (the photo is a centred 460x460 avatar).
L, T, S = 0.14, 0.0, 0.72  # crop box: left, top, side (fractions of photo)
crop = src.crop((int(w * L), int(h * T), int(w * (L + S)), int(h * (T + S))))
crop = ImageEnhance.Contrast(crop).enhance(1.2)
crop = ImageEnhance.Sharpness(crop).enhance(1.6)
small = crop.resize((GRID, GRID), Image.LANCZOS)
q = small.quantize(colors=COLORS, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
pal = q.getpalette()[: COLORS * 3]
idx = list(q.getdata())

# Mask out the flat grey border of the avatar (outside the dark circle).
cx_src, cy_src = w / 2, h / 2
radius = w * 0.43


def inside(col, row):
    sx = w * L + (col + 0.5) / GRID * (w * S)
    sy = h * T + (row + 0.5) / GRID * (h * S)
    return math.hypot(sx - cx_src, sy - cy_src) <= radius


# Bucket pixels by (delay class, colour) so each bucket is one <path>.
buckets = defaultdict(list)
for row in range(GRID):
    for col in range(GRID):
        if not inside(col, row):
            continue
        # Assemble bottom-up with jitter.
        delay = (GRID - row) / GRID * 1.8 + random.random() * 0.7
        d = round(delay * 10)  # 0.1s buckets
        buckets[(d, idx[row * GRID + col])].append((col, row))

delays = sorted({d for d, _ in buckets})


def hexcol(i):
    r, g, b = pal[i * 3 : i * 3 + 3]
    return f"#{r:02x}{g:02x}{b:02x}"


paths = []
for (d, ci), cells in sorted(buckets.items()):
    dpath = "".join(f"M{c} {r}h1v1h-1z" for c, r in cells)
    paths.append(f'<path class="d{d}" fill="{hexcol(ci)}" d="{dpath}"/>')

delay_css = "\n".join(f".d{d}{{animation-delay:{d/10:.1f}s}}" for d in delays)

# ---- Terminal --------------------------------------------------------------
TX, TY = 360, 26
TW, TH = 470, 288
FS = 15
CW = FS * 0.61  # approx monospace char width
lines = [
    ("$ ", "whoami", "#38bdf8"),
    ("", "laksh baweja · builder · new delhi", "#e5e7eb"),
    ("$ ", "cat interests.txt", "#38bdf8"),
    ("", "ai/ml · full-stack · social impact", "#e5e7eb"),
    ("$ ", "./ship --hackathon --time=3am", "#38bdf8"),
    ("", "✔ deployed. coffee levels: critical ☕", "#4ade80"),
]
term = []
clips = []
css_lines = []
t = 0.4
for i, (prompt, text, color) in enumerate(lines):
    y = TY + 70 + i * 34
    full = prompt + text
    n = len(full)
    width = n * CW + 6
    typing = n * 0.045 if prompt else 0.25
    start, end = t, t + typing
    # keyframe percentages within CYCLE
    p0, p1 = start / CYCLE * 100, end / CYCLE * 100
    clips.append(
        f'<clipPath id="c{i}"><rect class="l{i}" x="{TX+22}" y="{y-FS}" height="{FS+8}" width="{width:.0f}"/></clipPath>'
    )
    css_lines.append(
        f"@keyframes k{i}{{0%,{p0:.2f}%{{transform:scaleX(0)}}{p1:.2f}%,92%{{transform:scaleX(1)}}96%,100%{{transform:scaleX(0)}}}}"
        f".l{i}{{transform-origin:{TX+22}px 0;animation:k{i} {CYCLE}s steps({max(n,1)}) infinite}}"
    )
    spans = ""
    if prompt:
        spans += f'<tspan fill="#a78bfa">{prompt}</tspan>'
    spans += f'<tspan fill="{color}">{text}</tspan>'
    term.append(f'<text x="{TX+22}" y="{y}" clip-path="url(#c{i})">{spans}</text>')
    t = end + 0.35

cursor_y = TY + 70 + len(lines) * 34
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Pixel-art portrait of Laksh Baweja next to an animated terminal">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#111827"/>
  </linearGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#38bdf8" stop-opacity="0"/>
    <stop offset=".5" stop-color="#38bdf8" stop-opacity=".35"/>
    <stop offset="1" stop-color="#38bdf8" stop-opacity="0"/>
  </linearGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="2" fill="#000" opacity=".22"/>
  </pattern>
  <clipPath id="portrait"><rect x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{GRID*PX}" height="{GRID*PX}" rx="18"/></clipPath>
  {''.join(clips)}
</defs>
<style>
  text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;font-size:{FS}px}}
  .px path{{transform-box:fill-box;transform-origin:center;opacity:0;animation:drop {CYCLE}s cubic-bezier(.2,.9,.3,1.2) infinite both}}
  @keyframes drop{{
    0%{{opacity:0;transform:translateY(-14px) scale(.2)}}
    6%{{opacity:1;transform:none}}
    82%{{opacity:1;transform:none}}
    84%{{opacity:1;transform:translateX(3px)}}
    85%{{opacity:1;transform:translateX(-3px)}}
    86%{{opacity:1;transform:none}}
    92%{{opacity:0;transform:translateY(10px) scale(.4)}}
    100%{{opacity:0}}
  }}
{delay_css}
  .sweep{{animation:sweep 3.2s linear infinite}}
  @keyframes sweep{{from{{transform:translateY(-60px)}}to{{transform:translateY({GRID*PX+60}px)}}}}
  .cursor{{animation:blink 1s steps(1) infinite}}
  @keyframes blink{{50%{{opacity:0}}}}
  .glow{{animation:glow 4s ease-in-out infinite}}
  @keyframes glow{{50%{{opacity:.35}}}}
  .float{{animation:float 6s ease-in-out infinite}}
  @keyframes float{{50%{{transform:translateY(-6px)}}}}
  {''.join(css_lines)}
</style>
<rect width="{W}" height="{H}" rx="22" fill="url(#bg)"/>
<!-- portrait -->
<rect class="glow" x="{PORTRAIT_X-4}" y="{PORTRAIT_Y-4}" width="{GRID*PX+8}" height="{GRID*PX+8}" rx="22" fill="none" stroke="#38bdf8" stroke-opacity=".7" stroke-width="2"/>
<g clip-path="url(#portrait)">
  <rect x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{GRID*PX}" height="{GRID*PX}" fill="#0f172a"/>
  <g class="px" transform="translate({PORTRAIT_X} {PORTRAIT_Y}) scale({PX})" shape-rendering="crispEdges">
    {''.join(paths)}
  </g>
  <rect x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{GRID*PX}" height="{GRID*PX}" fill="url(#scan)"/>
  <rect class="sweep" x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{GRID*PX}" height="40" fill="url(#sweep)"/>
</g>
<!-- terminal -->
<g class="float">
  <rect x="{TX}" y="{TY}" width="{TW}" height="{TH}" rx="14" fill="#0d1117" stroke="#1f2937"/>
  <circle cx="{TX+22}" cy="{TY+22}" r="6" fill="#f87171"/>
  <circle cx="{TX+42}" cy="{TY+22}" r="6" fill="#fbbf24"/>
  <circle cx="{TX+62}" cy="{TY+22}" r="6" fill="#4ade80"/>
  <text x="{TX+TW/2}" y="{TY+27}" text-anchor="middle" fill="#6b7280" style="font-size:12px">laksh@delhi: ~</text>
  {''.join(term)}
  <rect class="cursor" x="{TX+22}" y="{cursor_y-FS+2}" width="9" height="{FS+2}" fill="#38bdf8"/>
</g>
</svg>
"""

out = Path(__file__).resolve().parent.parent / "assets" / "pixel-card.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(svg)
print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB, {len(paths)} paths)")
