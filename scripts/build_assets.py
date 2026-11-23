"""Build the animated SVGs used in the profile README.

    python3 scripts/build_assets.py

Writes assets/hero.svg, assets/arrivals.svg, assets/footer.svg and
assets/pass-*.svg. Everything is pure SVG + CSS/SMIL animation (no scripts,
no web fonts, no external requests) so GitHub renders it inside <img>.
Content mirrors js/content.js on laksh.codes — edit the DATA section below.
"""
import random
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- palette ---
CORAL, LIME, PAPER, PAPER_DK, INK = "#ff4d2e", "#c6ff3d", "#f0ece2", "#e2ddd0", "#0a0a0a"
NIGHT, TILE, MUTED, SKY, MINT = "#0e0e0e", "#1b1a18", "#8a8578", "#8fd3ff", "#34d399"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#*+"

# ------------------------------------------------------------------- DATA ---
NAME = "LAKSH BAWEJA"
ROLE = "AI/ML ENGINEER"
TAGLINES = [
    "multimodal AI & video understanding",
    "LLM fine-tuning · QLoRA · GRPO",
    "audio deepfake forensics",
    "RAG systems that actually ship",
]
ROUTE = [  # (code, year, label)
    ("DEL", "2023", "first commit"),
    ("MAA", "2024", "SRM IST · CSE (AI/ML)"),
    ("JSC", "2025", "NASA Space Apps · 1st"),
    ("BLR", "2026", "Samsung R&D + Introspect"),
]
PASSES = [
    dict(slug="deepshield", code="DSH", title="DeepShield", cat="AUDIO FORENSICS", where="Samsung R&D Institute Bangalore",
         gate="S1", seat="1A", accent=CORAL, band_ink=PAPER, stamp="IN PRODUCTION",
         tag="Is this voice real — and why does the model think so? Explainable deepfake-speech detection.",
         stats=[("93.2%", "ACCURACY"), ("10+", "MODELS"), ("SHAP", "EXPLAINABLE")]),
    dict(slug="janrakshak", code="JNR", title="JanRakshak", cat="CIVIC AI", where="Smart India Hackathon",
         gate="F2", seat="2A", accent="#2f6bff", band_ink=PAPER, stamp="LIVE",
         tag="AI flood prediction, early warnings and safe evacuation routes for at-risk communities.",
         stats=[("16K+", "LINES"), ("85%", "TEST COVERAGE"), ("11 m", "CLUSTERING")]),
    dict(slug="hindsight", code="HDS", title="Hindsight", cat="AI AGENT", where="Live on Vercel",
         gate="H3", seat="1C", accent="#7c5cff", band_ink=PAPER, stamp="LIVE",
         tag="A search agent that remembers what it told you, and when — then checks whether it still holds.",
         stats=[("DATED", "MEMORY"), ("19", "TESTS"), ("HONO", "STACK")]),
    dict(slug="daedalus", code="DDL", title="DAEDALUS", cat="RL × LLMs", where="Hugging Face Space",
         gate="H4", seat="2C", accent="#ffb020", band_ink=INK, stamp="GRPO",
         tag="An LLM learns to design auction rules that survive eight adversarial bidders.",
         stats=[("2.8×", "REWARD"), ("5→43%", "VALID JSON"), ("1×L4", "GPU")]),
    dict(slug="bionaut", code="BNT", title="BioNaut", cat="LLM + RAG", where="NASA Space Apps",
         gate="N5", seat="1F", accent=LIME, band_ink=INK, stamp="1ST PLACE",
         tag="A knowledge engine for NASA's space-biology research. Global Nominee.",
         stats=[("1ST", "LOCAL CHAPTER"), ("10K+", "NODES"), ("−35%", "LATENCY")]),
    dict(slug="kavach", code="KVC", title="Kavach", cat="INSURTECH AI", where="Gig-worker income protection",
         gate="K6", seat="3A", accent=MINT, band_ink=INK, stamp="LIVE",
         tag="Rain day? Still get paid. Zero-touch UPI payouts for delivery riders in under four minutes.",
         stats=[("<4 min", "PAYOUT"), ("3", "ML MODELS"), ("RN", "WORKER APP")]),
]
WINS = [  # (result, event, organiser, status)
    ("1ST", "NASA SPACE APPS", "Aarush · Global Nominee", "gold"),
    ("1ST", "HACKTRIX & AGENTIC AI", "Techvantage.ai", "gold"),
    ("1ST", "CINTEL IDEATHON", "SRM IST", "gold"),
    ("1ST", "TECHSHARK", "SIMATS", "gold"),
    ("1ST", "TECHKNOW · BEST PROJECT", "SRM IST", "gold"),
    ("2ND", "INNOVATEX HACKGRID 1.0", "ACM SIGAI", "silver"),
    ("3RD", "BEYOND HACK", "SRM IST", "bronze"),
    ("TOP4", "IISF HACKATHON", "Govt. of India", "finalist"),
]

# ------------------------------------------------------------ split-flap ---
_keyframes: dict = {}


def flap(x, y, w, h, ch, fs, color, delay, n=6, cycle=14.0, flip=1.1, tile=TILE, weight=800, rng=random):
    """One split-flap tile that scrambles through n-1 random glyphs onto `ch`."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{max(2, w * .08):.1f}" fill="{tile}"/>']
    if ch.strip():
        key = (h, n, cycle, flip)
        if key not in _keyframes:
            name = f"f{len(_keyframes)}"
            p = flip / cycle * 100
            dist = (n - 1) * h
            _keyframes[key] = name, (
                f"@keyframes {name}{{0%{{transform:translateY(0);animation-timing-function:steps({n - 1},end)}}"
                f"{p:.2f}%,100%{{transform:translateY(-{dist}px)}}}}"
                f".{name}{{animation:{name} {cycle}s infinite both}}"
            )
        name = _keyframes[key][0]
        seq = [rng.choice(GLYPHS) for _ in range(n - 1)] + [ch]
        base = h * 0.5 + fs * 0.36
        glyphs = "".join(
            f'<text x="{w / 2}" y="{i * h + base:.1f}">{escape(g)}</text>' for i, g in enumerate(seq)
        )
        out.append(
            f'<svg x="{x}" y="{y}" width="{w}" height="{h}" overflow="hidden">'
            f'<g class="{name}" style="animation-delay:{delay:.2f}s" fill="{color}" font-size="{fs}" '
            f'font-weight="{weight}" text-anchor="middle">{glyphs}</g></svg>'
        )
    # the hinge line across the middle of every tile
    if tile != "none":
        out.append(f'<rect x="{x}" y="{y + h / 2 - .75}" width="{w}" height="1.5" fill="#000" opacity=".55"/>')
    return "".join(out)


def flap_css():
    css = "".join(v[1] for v in _keyframes.values())
    _keyframes.clear()
    return css


def svg(w, h, body, css, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(label)}">\n<style>text{{font-family:{MONO}}}.sans{{font-family:{SANS}}}{css}</style>\n'
        f"{body}\n</svg>\n"
    )


def plane(fill, scale=1.0):
    """Small top-down airliner pointing +x, centred on the origin."""
    return (
        f'<g transform="scale({scale})" fill="{fill}">'
        '<path d="M-13 -1.6 L9 -1.6 Q14 -1.2 15 0 Q14 1.2 9 1.6 L-13 1.6 Z"/>'
        '<path d="M1 -1.5 L-5 -12 L-1.5 -12 L7 -1.5 Z"/><path d="M1 1.5 L-5 12 L-1.5 12 L7 1.5 Z"/>'
        '<path d="M-10 -1.4 L-13.5 -6 L-11.5 -6 L-7 -1.4 Z"/><path d="M-10 1.4 L-13.5 6 L-11.5 6 L-7 1.4 Z"/>'
        "</g>"
    )


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + (1 if cur else 0) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    return lines + [cur] if cur else lines


# ------------------------------------------------------------------ hero ---
def build_hero():
    rng = random.Random(718)
    W, H = 1000, 470
    b = [f'<rect width="{W}" height="{H}" rx="22" fill="{NIGHT}"/>']
    b.append(
        '<defs><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">'
        '<path d="M28 0H0V28" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern>'
        f'<radialGradient id="glow" cx=".5" cy=".32" r=".6"><stop offset="0" stop-color="{CORAL}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{CORAL}" stop-opacity="0"/></radialGradient></defs>'
        f'<rect width="{W}" height="{H}" rx="22" fill="url(#grid)"/><rect width="{W}" height="{H}" rx="22" fill="url(#glow)"/>'
    )
    # twinkling stars
    for _ in range(55):
        sx, sy, r = rng.uniform(20, W - 20), rng.uniform(15, H - 15), rng.choice([.7, .9, 1.2, 1.6])
        b.append(f'<circle class="tw" cx="{sx:.0f}" cy="{sy:.0f}" r="{r}" fill="{PAPER}" '
                 f'style="animation-delay:-{rng.uniform(0, 5):.1f}s;animation-duration:{rng.uniform(2.5, 5.5):.1f}s"/>')
    # top status bar
    b.append(
        f'<g font-size="13" letter-spacing="2">'
        f'<circle class="blink" cx="44" cy="40" r="5" fill="{LIME}"/>'
        f'<text x="58" y="45" fill="{LIME}">NOW BOARDING</text>'
        f'<text x="{W / 2}" y="45" fill="{MUTED}" text-anchor="middle">FLIGHT LK718 · DEL → ∞</text>'
        f'<text x="{W - 40}" y="45" fill="{MUTED}" text-anchor="end">GATE 2026 · SEAT 1A</text></g>'
        f'<line x1="40" y1="64" x2="{W - 40}" y2="64" stroke="{PAPER}" stroke-opacity=".08"/>'
    )
    # split-flap name
    cw, ch, gap = 64, 88, 7
    total = len(NAME) * (cw + gap) - gap
    x0, y0 = (W - total) / 2, 92
    for i, c in enumerate(NAME):
        color = CORAL if i > 5 else PAPER
        b.append(flap(x0 + i * (cw + gap), y0, cw, ch, c, 64, color, .25 + i * .09, n=8, cycle=16, flip=1.4,
                      rng=rng, tile="#191816" if c.strip() else "none"))
    # role + rotating taglines
    b.append(f'<text x="{W / 2}" y="232" text-anchor="middle" font-size="20" letter-spacing="7" fill="{LIME}" '
             f'font-weight="700">{ROLE}</text>')
    n = len(TAGLINES)
    for i, t in enumerate(TAGLINES):
        b.append(f'<text class="rot" style="animation-delay:{i * 3}s" x="{W / 2}" y="268" text-anchor="middle" '
                 f'font-size="17" fill="{SKY}"><tspan fill="{CORAL}">› </tspan>{escape(t)}</text>')
    b.append(f'<text x="{W / 2}" y="296" text-anchor="middle" font-size="12" letter-spacing="2" fill="{MUTED}">'
             f"SRM IST '28 · CGPA 9.5 · 5× FIRST PLACE · 3 INTERNSHIPS</text>")
    # flight route with waypoints
    pts = [(90, 400), (350, 372), (630, 382), (870, 352)]
    d = "M90 400 C 180 330, 270 330, 350 372 S 540 430, 630 382 S 790 300, 870 352"
    b.append(f'<path d="{d}" fill="none" stroke="{PAPER}" stroke-opacity=".18" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>')
    b.append(f'<path class="trail" d="{d}" pathLength="1000" fill="none" stroke="{CORAL}" stroke-width="2.5" '
             f'stroke-dasharray="1000" stroke-linecap="round"/>')
    for i, ((px, py), (code, yr, lab)) in enumerate(zip(pts, ROUTE)):
        ty = py - 34 if i % 2 == 0 else py + 30  # alternate labels above / below the route
        b.append(
            f'<circle class="ring" style="animation-delay:{i * 1.9:.1f}s" cx="{px}" cy="{py}" r="7" fill="none" stroke="{LIME}"/>'
            f'<circle cx="{px}" cy="{py}" r="5" fill="{NIGHT}" stroke="{LIME}" stroke-width="2"/>'
            f'<text x="{px}" y="{ty}" text-anchor="middle" font-size="14" font-weight="700" fill="{PAPER}">{code}'
            f'<tspan fill="{CORAL}" font-weight="400"> {yr}</tspan></text>'
            f'<text x="{px}" y="{ty + 16}" text-anchor="middle" font-size="11" fill="{MUTED}">{escape(lab)}</text>'
        )
    b.append(f'<g>{plane(PAPER, 1.25)}<animateMotion dur="8s" repeatCount="indefinite" rotate="auto" '
             f'keyPoints="0;1;1" keyTimes="0;.85;1" calcMode="linear" path="{d}"/></g>')
    css = (
        flap_css()
        + ".tw{animation:tw 4s ease-in-out infinite}@keyframes tw{50%{opacity:.15}}"
        + ".blink{animation:bl 1.2s steps(1) infinite}@keyframes bl{50%{opacity:.15}}"
        + f".rot{{opacity:0;animation:rot {n * 3}s infinite}}"
        + f"@keyframes rot{{0%{{opacity:0;transform:translateY(8px)}}3%,{100 / n - 3:.1f}%{{opacity:1;transform:none}}"
        + f"{100 / n:.1f}%,100%{{opacity:0;transform:translateY(-8px)}}}}"
        + ".trail{animation:tr 8s linear infinite}@keyframes tr{0%{stroke-dashoffset:1000}85%,100%{stroke-dashoffset:0}}"
        + ".ring{transform-box:fill-box;transform-origin:center;animation:ring 2.4s ease-out infinite}"
        + "@keyframes ring{0%{transform:scale(1);opacity:.9}100%{transform:scale(3.2);opacity:0}}"
    )
    (OUT / "hero.svg").write_text(svg(W, H, "".join(b), css, "Laksh Baweja — AI/ML Engineer. Flight LK718 now boarding."))


# ---------------------------------------------------------- boarding pass ---
def build_pass(p, idx):
    rng = random.Random(idx + 7)
    W, H = 520, 260
    STUB = 400  # x of perforation
    acc, band_ink = p["accent"], p["band_ink"]
    b = [
        '<defs>'
        f'<mask id="notch"><rect width="{W}" height="{H}" rx="16" fill="#fff"/>'
        f'<circle cx="{STUB}" cy="0" r="11" fill="#000"/><circle cx="{STUB}" cy="{H}" r="11" fill="#000"/></mask>'
        '<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
        '</defs>',
        f'<g mask="url(#notch)">',
        f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
        f'<rect width="{W}" height="42" fill="{acc}"/>',
        f'<g transform="translate(26 21)">{plane(band_ink, .75)}</g>',
        f'<text x="44" y="26" font-size="12" font-weight="700" letter-spacing="2.5" fill="{band_ink}">LK718 · BOARDING PASS</text>',
        f'<text x="{STUB - 16}" y="26" text-anchor="end" font-size="11" letter-spacing="1.5" fill="{band_ink}" opacity=".85">{escape(p["cat"])}</text>',
        f'<text x="{STUB + 16}" y="26" font-size="11" font-weight="700" letter-spacing="2" fill="{band_ink}">STUB</text>',
    ]
    # FROM / TO row
    b.append(
        f'<text x="24" y="66" font-size="9.5" letter-spacing="1.5" fill="{MUTED}">FROM</text>'
        f'<text x="24" y="98" font-size="34" font-weight="800" fill="{INK}">DEL</text>'
        f'<text x="{STUB - 24}" y="66" text-anchor="end" font-size="9.5" letter-spacing="1.5" fill="{MUTED}">TO</text>'
        f'<text x="{STUB - 24}" y="98" text-anchor="end" font-size="34" font-weight="800" fill="{acc if band_ink == PAPER else INK}">{p["code"]}</text>'
        f'<line x1="108" y1="86" x2="{STUB - 108}" y2="86" stroke="{INK}" stroke-opacity=".3" stroke-dasharray="3 5"/>'
        f'<g class="fly"><g transform="translate(108 86)">{plane(INK, .85)}</g></g>'
    )
    # title + where
    b.append(
        f'<text class="sans" x="24" y="134" font-size="23" font-weight="800" fill="{INK}">{escape(p["title"])}</text>'
        f'<text x="24" y="152" font-size="10.5" fill="{MUTED}">{escape(p["where"])}</text>'
    )
    for i, line in enumerate(wrap(p["tag"], 56)[:2]):
        b.append(f'<text class="sans" x="24" y="{174 + i * 16}" font-size="12.5" fill="#3a3833">{escape(line)}</text>')
    # stats
    for i, (v, lab) in enumerate(p["stats"]):
        sx = 24 + i * 122
        b.append(
            f'<rect x="{sx}" y="204" width="112" height="40" rx="8" fill="{PAPER_DK}"/>'
            f'<text x="{sx + 10}" y="223" font-size="15" font-weight="800" fill="{INK}">{escape(v)}</text>'
            f'<text x="{sx + 10}" y="237" font-size="8.5" letter-spacing="1" fill="{MUTED}">{escape(lab)}</text>'
        )
    # perforation + stub
    b.append(f'<line x1="{STUB}" y1="14" x2="{STUB}" y2="{H - 14}" stroke="{INK}" stroke-opacity=".35" stroke-dasharray="4 5"/>')
    sx = STUB + 18
    b.append(
        f'<text x="{sx}" y="66" font-size="9.5" letter-spacing="1.5" fill="{MUTED}">GATE</text>'
        f'<text x="{sx}" y="92" font-size="24" font-weight="800" fill="{INK}">{p["gate"]}</text>'
        f'<text x="{sx + 52}" y="66" font-size="9.5" letter-spacing="1.5" fill="{MUTED}">SEAT</text>'
        f'<text x="{sx + 52}" y="92" font-size="24" font-weight="800" fill="{INK}">{p["seat"]}</text>'
    )
    bx = sx
    bars = []
    while bx < W - 18:
        bw = rng.choice([1, 1, 2, 3])
        bars.append(f'<rect x="{bx}" y="112" width="{bw}" height="66" fill="{INK}"/>')
        bx += bw + rng.choice([1, 2, 2, 3])
    b.append("".join(bars))
    b.append(f'<g class="blink"><text x="{sx}" y="204" font-size="10" font-weight="700" letter-spacing="1.5" fill="{INK}">TAP TO</text>'
             f'<text x="{sx}" y="219" font-size="10" font-weight="700" letter-spacing="1.5" fill="{INK}">BOARD ↗</text></g>')
    # stamp
    st = p["stamp"]
    stw = len(st) * 9.6 + 22
    b.append(
        f'<g transform="translate({STUB - 28 - stw / 2:.0f} 128) rotate(-8)"><g class="stamp">'
        f'<rect x="{-stw / 2}" y="-15" width="{stw}" height="30" rx="5" fill="none" stroke="{CORAL}" stroke-width="2.5"/>'
        f'<text x="0" y="5.5" text-anchor="middle" font-size="15" font-weight="800" letter-spacing="1.5" fill="{CORAL}">{escape(st)}</text>'
        f"</g></g>"
    )
    # shine sweep
    b.append(f'<g clip-path="url(#card)"><rect class="shine" x="-200" y="-40" width="120" height="{H + 80}" fill="url(#shine)" transform="skewX(-18)"/></g>')
    b.append("</g>")
    d = idx * .35
    css = (
        f".fly{{animation:fly 4.5s ease-in-out {d}s infinite}}@keyframes fly{{0%{{transform:translateX(0);opacity:0}}10%{{opacity:1}}"
        f"80%{{transform:translateX({STUB - 216}px);opacity:1}}90%,100%{{transform:translateX({STUB - 216}px);opacity:0}}}}"
        ".blink{animation:bl 1.4s steps(1) infinite}@keyframes bl{50%{opacity:.25}}"
        f".stamp{{transform-origin:center;transform-box:fill-box;animation:stamp 7s cubic-bezier(.2,1.6,.4,1) {d + .6:.2f}s infinite both}}"
        "@keyframes stamp{0%{transform:scale(2.6);opacity:0}6%{transform:scale(1);opacity:.92}92%{transform:scale(1);opacity:.92}100%{transform:scale(1);opacity:0}}"
        f".shine{{animation:shine 6s ease-in-out {d + 1:.2f}s infinite}}@keyframes shine{{0%{{transform:skewX(-18deg) translateX(0)}}25%,100%{{transform:skewX(-18deg) translateX({W + 400}px)}}}}"
    )
    (OUT / f"pass-{p['slug']}.svg").write_text(
        svg(W, H, "".join(b), css, f"Boarding pass: {p['title']} — {p['tag']}")
    )


# -------------------------------------------------------------- arrivals ---
def build_arrivals():
    rng = random.Random(42)
    W = 1000
    cw, ch, g = 20, 30, 2
    row_h = 44
    top = 112
    H = top + len(WINS) * row_h + 26
    b = [f'<rect width="{W}" height="{H}" rx="20" fill="#121110"/>',
         f'<rect x="10" y="10" width="{W - 20}" height="{H - 20}" rx="14" fill="none" stroke="{PAPER}" stroke-opacity=".06"/>']
    # header
    b.append(
        f'<g transform="translate(46 46) rotate(18)">{plane(LIME, 1.15)}</g>'
        f'<text x="72" y="54" font-size="26" font-weight="800" letter-spacing="6" fill="{LIME}">ARRIVALS</text>'
        f'<text x="268" y="54" font-size="13" letter-spacing="2" fill="{MUTED}">TROPHY CABINET</text>'
        f'<text x="{W - 36}" y="54" text-anchor="end" font-size="13" letter-spacing="2" fill="{PAPER}">'
        f'<tspan fill="{CORAL}" font-weight="800">5×</tspan> FIRST PLACE<tspan class="blink" fill="{LIME}"> ●</tspan></text>'
    )
    cols = [(36, "RESULT"), (150, "EVENT"), (692, "ORGANISER"), (880, "STATUS")]
    for x, lab in cols:
        b.append(f'<text x="{x}" y="94" font-size="11" letter-spacing="2" fill="{MUTED}">{lab}</text>')
    b.append(f'<line x1="30" y1="102" x2="{W - 30}" y2="102" stroke="{PAPER}" stroke-opacity=".1"/>')
    status_style = {"gold": ("WON ★", LIME), "silver": ("SILVER", PAPER), "bronze": ("BRONZE", "#e0a370"), "finalist": ("FINALIST", SKY)}
    for r, (res, event, org, st) in enumerate(WINS):
        y = top + r * row_h
        res_color = LIME if res == "1ST" else PAPER
        for i, c in enumerate(res.ljust(4)):
            b.append(flap(36 + i * (cw + g), y, cw, ch, c, 19, res_color, .3 + r * .18 + i * .04, n=5, cycle=15, flip=.9, rng=rng))
        for i, c in enumerate(event.ljust(24)):
            b.append(flap(150 + i * (cw + g), y, cw, ch, c, 19, PAPER, .4 + r * .18 + i * .035, n=5, cycle=15, flip=.9, rng=rng))
        b.append(f'<text x="692" y="{y + 20}" font-size="12.5" fill="{MUTED}">{escape(org)}</text>')
        label, color = status_style[st]
        b.append(f'<circle class="blink" style="animation-delay:{r * .2:.1f}s" cx="884" cy="{y + 15}" r="4" fill="{color}"/>'
                 f'<text x="896" y="{y + 20}" font-size="13" font-weight="700" fill="{color}">{label}</text>')
    css = flap_css() + ".blink{animation:bl 1.3s steps(1) infinite}@keyframes bl{50%{opacity:.2}}"
    (OUT / "arrivals.svg").write_text(svg(W, H, "".join(b), css, "Arrivals board of hackathon results: five first places, a second, a third and a top-four finish."))


# ---------------------------------------------------------------- footer ---
def build_footer():
    W, H = 1000, 230
    b = [f'<rect width="{W}" height="{H}" rx="22" fill="{NIGHT}"/>']
    # runway
    b.append(f'<rect x="0" y="176" width="{W}" height="34" fill="#171614"/>')
    for i in range(24):
        b.append(f'<rect class="lt" style="animation-delay:{i * .08:.2f}s" x="{14 + i * 42}" y="191" width="20" height="4" rx="2" fill="{LIME}"/>')
    b.append(f'<rect x="0" y="210" width="{W}" height="20" fill="{NIGHT}"/><rect x="0" y="210" width="{W}" height="20" rx="0" fill="none"/>')
    b.append(f'<path d="M0 210 H{W} V208 Q{W} 230 {W - 22} 230 H22 Q0 230 0 208 Z" fill="{NIGHT}"/>')
    # plane takeoff
    b.append(f'<g class="to"><g transform="translate(0 182)">{plane(PAPER, 1.6)}</g></g>')
    b.append(
        f'<text class="sans" x="{W / 2}" y="88" text-anchor="middle" font-size="38" font-weight="800" fill="{PAPER}">'
        f'Thanks for flying <tspan fill="{CORAL}">LK718</tspan>.</text>'
        f'<text x="{W / 2}" y="122" text-anchor="middle" font-size="14" fill="{MUTED}">'
        "Please collect all your belongings — and maybe my résumé.</text>"
    )
    css = (
        ".lt{animation:lt 1.9s linear infinite;opacity:.15}@keyframes lt{0%,30%{opacity:.15}10%{opacity:1}}"
        ".to{animation:to 6s cubic-bezier(.5,0,.8,.6) infinite}"
        "@keyframes to{0%{transform:translate(-60px,0) rotate(0)}45%{transform:translate(430px,0) rotate(0)}"
        "100%{transform:translate(1100px,-200px) rotate(-14deg)}}"
    )
    (OUT / "footer.svg").write_text(svg(W, H, "".join(b), css, "Thanks for flying LK718."))


if __name__ == "__main__":
    build_hero()
    for i, p in enumerate(PASSES):
        build_pass(p, i)
    build_arrivals()
    build_footer()
    for f in sorted(OUT.glob("*.svg")):
        print(f"{f.name:28} {f.stat().st_size / 1024:6.1f} KB")
