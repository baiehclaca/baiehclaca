#!/usr/bin/env python3
"""
Animated header.svg — Teodor Walter Vido / Sinoussi.

Design reference: chameleon-circle video.
- Two solid particle discs. Left: monochrome white. Right: iridescent.
- Dense, painterly particulate. Brightness blooms in lower-right quadrant.
- A shimmering bridge connects them.
- Identity text sits below. Apple-grade restraint.

Pure SVG + SMIL + inline CSS. No JS. GitHub-compatible as <img>.
"""

import math
import random

random.seed(11)

# ---- Canvas ----
W, H = 1600, 820
CX1, CY1 = 500, 310
CX2, CY2 = 1100, 310
R  = 255

# ---- Chameleon palette ----
CHAMELEON = [
    "#FF3DA8", "#FF7A1A", "#FFE94A", "#55FF9E",
    "#29E6FF", "#5B6BFF", "#B84DFF", "#FF3DA8",
]

def disc_particles(cx, cy, n):
    """Dense disc. brightness = lower-right-bias glow factor in [0..1]."""
    out = []
    while len(out) < n:
        # uniform disc sampling (sqrt for even distribution)
        theta = random.random() * 2 * math.pi
        rr = R * math.sqrt(random.random())
        x = cx + rr * math.cos(theta)
        y = cy + rr * math.sin(theta)
        # brightness: strong in lower-right, dim in upper-left (like video)
        bx = (x - cx) / R      # -1..1
        by = (y - cy) / R      # -1..1
        # dot with (0.55, 0.75) direction — bright toward down-right
        g = 0.5 + 0.55 * bx + 0.70 * by
        glow = max(0.0, min(1.0, g))
        # accept with probability proportional to glow^0.35 so sparse side still
        # has some particles but dense side wins
        p = glow ** 0.4 * 0.95 + 0.05
        if random.random() > p:
            continue
        out.append((x, y, rr / R, glow))
    return out

def bridge_particles(n):
    out = []
    for _ in range(n):
        t = random.random()
        x0 = CX1 + R * 0.7
        x1 = CX2 - R * 0.7
        x = x0 + (x1 - x0) * t
        amp = 60 * math.sin(math.pi * t)
        y = CY1 + amp * math.sin(t * 6 + 0.8) + random.uniform(-20, 20)
        out.append((x, y, t))
    return out

parts = []
parts.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Teodor Walter Vido">
<title>Teodor Walter Vido — builder, architect, protocol designer</title>

<defs>
  <radialGradient id="bg" cx="50%" cy="40%" r="75%">
    <stop offset="0%"  stop-color="#0a0a0d"/>
    <stop offset="70%" stop-color="#030304"/>
    <stop offset="100%" stop-color="#000000"/>
  </radialGradient>

  <filter id="bloom" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="1.2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>

  <filter id="softbloom" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="8" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>

  <!-- strong glow disc under the monochrome cluster (lower-right hotspot) -->
  <radialGradient id="mono-glow" cx="65%" cy="70%" r="55%">
    <stop offset="0%"  stop-color="#ffffff" stop-opacity="0.55"/>
    <stop offset="40%" stop-color="#ffffff" stop-opacity="0.12"/>
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
  </radialGradient>

  <radialGradient id="chrom-glow" cx="65%" cy="70%" r="55%">
    <stop offset="0%"  stop-color="#ffffff" stop-opacity="0.4"/>
    <stop offset="40%" stop-color="#ffffff" stop-opacity="0.08"/>
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
  </radialGradient>

  <style><![CDATA[
    .bg     {{ fill: url(#bg); }}
    .corner {{ stroke: #ffffff33; stroke-width: 1.2; fill: none; }}
    .label  {{ fill: #ffffff88; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; letter-spacing: 0.24em; }}
    .name   {{ fill: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Inter, Arial, sans-serif; font-weight: 200; font-size: 56px; letter-spacing: -0.015em; }}
    .tag    {{ fill: #ffffffcc; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Inter, Arial, sans-serif; font-weight: 300; font-size: 20px; letter-spacing: 0.02em; }}
    .dim    {{ fill: #ffffff55; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; letter-spacing: 0.28em; }}

    @keyframes spinSlow {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    @keyframes spinRev  {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(-360deg); }} }}

    .mono-spin  {{ transform-origin: {CX1}px {CY1}px; animation: spinSlow 120s linear infinite; }}
    .chrom-spin {{ transform-origin: {CX2}px {CY2}px; animation: spinRev 140s linear infinite; }}
  ]]></style>
</defs>

<rect class="bg" x="0" y="0" width="{W}" height="{H}"/>

<g class="corner">
  <path d="M 28 28 L 52 28 M 28 28 L 28 52"/>
  <path d="M {W-28} 28 L {W-52} 28 M {W-28} 28 L {W-28} 52"/>
  <path d="M 28 {H-28} L 52 {H-28} M 28 {H-28} L 28 {H-52}"/>
  <path d="M {W-28} {H-28} L {W-52} {H-28} M {W-28} {H-28} L {W-28} {H-52}"/>
</g>

<text class="dim" x="56" y="48">BAIEHCLACA · TEODORWALTERV</text>
<text class="dim" x="{W-56}" y="48" text-anchor="end">SLOVAKIA · EARTH</text>
''')

# ---- SOFT GLOW DISCS (under particles) ----
parts.append(f'<circle cx="{CX1}" cy="{CY1}" r="{R}" fill="url(#mono-glow)" filter="url(#softbloom)"/>')
parts.append(f'<circle cx="{CX2}" cy="{CY2}" r="{R}" fill="url(#chrom-glow)" filter="url(#softbloom)"/>')

# ---- MONO CLUSTER ----
mono_pts = disc_particles(CX1, CY1, n=2400)
parts.append(f'<g class="mono-spin" filter="url(#bloom)">')
for i, (x, y, d, glow) in enumerate(mono_pts):
    # size driven by glow — bigger/brighter in hot quadrant, tiny at the faint edge
    s = 1.0 + 2.8 * glow + random.uniform(0, 1.4)
    op = round(max(0.08, min(1.0, 0.25 + 0.75 * glow * random.uniform(0.55, 1.0))), 3)
    op_lo = round(max(0.03, op * 0.25), 3)
    dur = round(2.6 + random.random() * 4.2, 2)
    phase = round(random.random() * dur, 2)
    parts.append(
        f'<rect fill="#ffffff" x="{x:.1f}" y="{y:.1f}" width="{s:.2f}" height="{s:.2f}" opacity="{op}">'
        f'<animate attributeName="opacity" values="{op};{op_lo};{op}" dur="{dur}s" '
        f'begin="-{phase}s" repeatCount="indefinite"/></rect>'
    )
parts.append('</g>')

# ---- CHAMELEON CLUSTER ----
chrom_pts = disc_particles(CX2, CY2, n=2400)
parts.append(f'<g class="chrom-spin" filter="url(#bloom)">')
for i, (x, y, d, glow) in enumerate(chrom_pts):
    s = 1.2 + 3.0 * glow + random.uniform(0, 1.6)
    start_idx = i % len(CHAMELEON)
    cycled = CHAMELEON[start_idx:] + CHAMELEON[:start_idx]
    vals = ";".join(cycled + [cycled[0]])
    dur_c = round(4.5 + (i % 19) * 0.35, 2)
    phase_c = round((i * 0.031) % dur_c, 2)
    op = round(max(0.15, min(1.0, 0.35 + 0.65 * glow * random.uniform(0.6, 1.0))), 3)
    op_lo = round(max(0.08, op * 0.35), 3)
    dur_o = round(2.4 + random.random() * 3.6, 2)
    phase_o = round(random.random() * dur_o, 2)
    parts.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.2f}" height="{s:.2f}" '
        f'fill="{cycled[0]}" opacity="{op}" shape-rendering="crispEdges">'
        f'<animate attributeName="fill" values="{vals}" dur="{dur_c}s" '
        f'begin="-{phase_c}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="{op};{op_lo};{op}" dur="{dur_o}s" '
        f'begin="-{phase_o}s" repeatCount="indefinite"/>'
        f'</rect>'
    )
parts.append('</g>')

# ---- BRIDGE ----
bridge_pts = bridge_particles(n=360)
parts.append('<g filter="url(#bloom)">')
for i, (x, y, t) in enumerate(bridge_pts):
    s = 1.6 + random.uniform(0, 2.6)
    if t < 0.38:
        fill = "#ffffff"
    elif t > 0.62:
        fill = CHAMELEON[i % len(CHAMELEON)]
    else:
        fill = random.choice(["#ffffff", "#ffffff", CHAMELEON[i % len(CHAMELEON)]])
    op = round(0.4 + random.random() * 0.55, 3)
    op_lo = round(max(0.02, op * 0.1), 3)
    dur = round(1.4 + random.random() * 2.6, 2)
    phase = round(random.random() * dur, 2)
    dx = random.uniform(-14, 20)
    dy = random.uniform(-10, 10)
    parts.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.2f}" height="{s:.2f}" fill="{fill}" opacity="{op}">'
        f'<animate attributeName="opacity" values="{op_lo};{op};{op_lo}" dur="{dur}s" '
        f'begin="-{phase}s" repeatCount="indefinite"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 0;{dx:.1f} {dy:.1f};0 0" dur="{dur*2:.2f}s" repeatCount="indefinite"/>'
        f'</rect>'
    )
parts.append('</g>')

# ---- TEXT ----
# Static-visible at opacity=1. SMIL plays a gentle intro in browsers; static renderers see final state.
parts.append(f'''
<text class="name" x="{W/2}" y="692" text-anchor="middle">Teodor Walter Vido</text>
<text class="tag"  x="{W/2}" y="732" text-anchor="middle">Builder. Architect. Protocol designer.</text>
<text class="label" x="{W/2}" y="772" text-anchor="middle">1,000,000,000+  TOKENS / MONTH   ·   ALWAYS  SHIPPING</text>

<circle cx="{CX1}" cy="{CY1 + R + 34}" r="3" fill="#ffffff">
  <animate attributeName="opacity" values="0.25;1;0.25" dur="3s" repeatCount="indefinite"/>
</circle>
<circle cx="{CX2}" cy="{CY2 + R + 34}" r="3" fill="{CHAMELEON[0]}">
  <animate attributeName="fill" values="{";".join(CHAMELEON)}" dur="6s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.25;1;0.25" dur="3s" begin="-1.5s" repeatCount="indefinite"/>
</circle>

</svg>''')

svg = "".join(parts)
with open("/tmp/baiehclaca/header.svg", "w") as f:
    f.write(svg)
print(f"SVG written — {len(svg):,} bytes, {len(mono_pts)+len(chrom_pts)+len(bridge_pts)} particles.")
