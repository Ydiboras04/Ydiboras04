#!/usr/bin/env python3
"""Generate assets/header.svg — an animated terminal-style banner for the profile README.

Edit NAME / LINES below, then run:  python3 scripts/gen_header.py
"""
from pathlib import Path
import random

NAME = "YDIBORAS"
LINES = [
    "Hi, I'm Nomeny — developer from Madagascar",
    "I build with Rust, TypeScript & Python",
    "I design games, mechanics & worlds",
    "Always learning something new...",
]

W, H = 900, 300
FS = 20                 # typing font size
CW = FS * 0.6           # monospace char width
X0 = 64                 # typing text x
Y_TYPE = 236
SLOT = 4.5              # seconds per line
TYPE_T, HOLD_END, DEL_T = 2.0, 3.6, 0.5
TOTAL = SLOT * len(LINES)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def keyframes():
    """Return list of (time, width, line_index) — discrete per-character steps."""
    kf = [(0.0, 0.0, 0)]
    for i, line in enumerate(LINES):
        o, n = i * SLOT, len(line)
        for k in range(1, n + 1):
            kf.append((o + 0.15 + k * TYPE_T / n, k * CW, i))
        for k in range(n - 1, -1, -1):
            kf.append((o + HOLD_END + (n - k) * DEL_T / n, k * CW, i))
        if i + 1 < len(LINES):
            kf.append(((i + 1) * SLOT, 0.0, i + 1))
    return kf


def anim(attr, values, times):
    kt = ";".join(f"{t / TOTAL:.5f}" for t in times)
    vs = ";".join(values)
    return (f'<animate attributeName="{attr}" dur="{TOTAL}s" repeatCount="indefinite" '
            f'calcMode="discrete" keyTimes="{kt}" values="{vs}"/>')


def main():
    kf = keyframes()
    times = [t for t, _, _ in kf]
    widths = [f"{w:.1f}" for _, w, _ in kf]
    cursor_x = [f"{X0 + w + 2:.1f}" for _, w, _ in kf]

    texts = []
    for i, line in enumerate(LINES):
        op = ["1" if li == i else "0" for _, _, li in kf]
        texts.append(
            f'<text x="{X0}" y="{Y_TYPE}" class="type" opacity="{1 if i == 0 else 0}">'
            f'{esc(line)}{anim("opacity", op, times)}</text>')

    rnd = random.Random(4)
    particles = []
    for _ in range(26):
        x = rnd.uniform(20, W - 20)
        r = rnd.uniform(0.8, 2.2)
        d = rnd.uniform(6, 14)
        b = rnd.uniform(0, d)
        c = rnd.choice(["#7aa2f7", "#bb9af7", "#7dcfff", "#9ece6a"])
        particles.append(
            f'<circle cx="{x:.0f}" cy="{H}" r="{r:.1f}" fill="{c}">'
            f'<animate attributeName="cy" from="{H + 10}" to="40" dur="{d:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.9;0" dur="{d:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
            f'</circle>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME} — animated banner">
  <title>{NAME}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#1a1b27"/>
    </linearGradient>
    <linearGradient id="shine2" x1="0" y1="0" x2="1" y2="0" spreadMethod="repeat">
      <stop offset="0" stop-color="#7aa2f7"/>
      <stop offset="0.33" stop-color="#bb9af7"/>
      <stop offset="0.66" stop-color="#7dcfff"/>
      <stop offset="1" stop-color="#7aa2f7"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="1 0" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="#7aa2f7" stroke-opacity="0.06"/>
      <animateTransform attributeName="patternTransform" type="translate" from="0 0" to="0 32" dur="4s" repeatCount="indefinite"/>
    </pattern>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
    <clipPath id="typeclip"><rect x="{X0}" y="{Y_TYPE - FS}" height="{FS + 8}" width="0">{anim("width", widths, times)}</rect></clipPath>
    <style>
      .mono {{ font-family: 'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace; }}
      .type {{ font-family: 'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace; font-size: {FS}px; fill: #c0caf5; }}
      .name {{ font-family: 'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif; font-weight: 900; font-size: 84px; letter-spacing: 14px; }}
    </style>
  </defs>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#grid)"/>
    {"".join(particles)}

    <!-- title bar -->
    <rect width="{W}" height="40" fill="#16161e"/>
    <circle cx="26" cy="20" r="6" fill="#f7768e"/><circle cx="46" cy="20" r="6" fill="#e0af68"/><circle cx="66" cy="20" r="6" fill="#9ece6a"/>
    <text x="{W / 2}" y="25" text-anchor="middle" class="mono" font-size="13" fill="#565f89">nomeny@madagascar: ~/profile</text>

    <!-- name -->
    <g filter="url(#glow)">
      <text x="{W / 2}" y="158" text-anchor="middle" class="name" fill="url(#shine2)" opacity="0">{NAME}
        <animate attributeName="opacity" from="0" to="1" dur="1.2s" fill="freeze"/>
        <animate attributeName="y" values="180;158" dur="1.2s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
      </text>
    </g>
    <rect x="{W / 2 - 160}" y="178" height="3" rx="1.5" width="320" fill="url(#shine2)">
      <animate attributeName="width" values="0;320" dur="1.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
      <animate attributeName="x" values="{W / 2};{W / 2 - 160}" dur="1.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
    </rect>

    <!-- typing line -->
    <text x="{X0 - 26}" y="{Y_TYPE}" class="type" fill="#9ece6a" style="fill:#9ece6a">❯</text>
    <g clip-path="url(#typeclip)">
      {"".join(texts)}
    </g>
    <rect x="{X0 + 2}" y="{Y_TYPE - FS + 2}" width="11" height="{FS + 2}" fill="#7aa2f7">
      {anim("x", cursor_x, times)}
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#7aa2f7" stroke-opacity="0.25"/>
</svg>
'''
    out = Path(__file__).resolve().parent.parent / "assets" / "header.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"wrote {out} ({len(svg)} bytes, {TOTAL}s cycle)")


if __name__ == "__main__":
    main()
