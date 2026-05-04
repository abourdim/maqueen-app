#!/usr/bin/env python3
"""Maqueen Lite v4 robot emulator — 3 views.

A. Photo-real hero (3/4 isometric)
B. Track action (top-down arcade)
C. Exploded diagram (vertical layers + callouts)

Outputs labs/maqueen-emu.html (picker) + maqueen-emu_A/B/C.html.
Static design only (CSS animations, no BLE wiring).
"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'labs')

# ╔════════════════════════════════════════════════════════════════════╗
# ║  Shared CSS                                                          ║
# ╚════════════════════════════════════════════════════════════════════╝
COMMON_CSS = '''
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:#0a1018;color:#e0e6ee;font-family:'JetBrains Mono',monospace;
  min-height:100vh;overflow-x:hidden;padding:14px;}
.title-bar{display:flex;align-items:center;gap:14px;padding:8px 14px;
  background:linear-gradient(180deg,#1a2030,#0a1018);border:1px solid #1e3a5a;
  border-radius:8px;margin:0 auto 14px;max-width:1400px;}
.title-bar .badge{font-size:14px;font-weight:800;color:#22d3ee;letter-spacing:0.05em;}
.title-bar .vibe{font-size:11px;color:#7fa;}
.title-bar .nav{margin-left:auto;display:flex;gap:6px;}
.title-bar .nav a{color:#aff;text-decoration:none;border:1px solid #1e3a5a;border-radius:5px;padding:3px 9px;font-size:11px;}
.title-bar .nav a:hover{border-color:#22d3ee;color:#22d3ee;}
@keyframes spin{to{transform:rotate(360deg);}}
@keyframes pulse{0%,100%{opacity:0.5;transform:scale(1);}50%{opacity:1;transform:scale(1.18);}}
@keyframes blink{0%,55%{opacity:1;}56%,100%{opacity:0.2;}}
@keyframes ledcycle{0%{background:#ef4444;box-shadow:0 0 16px #ef4444;}
                    25%{background:#22c55e;box-shadow:0 0 16px #22c55e;}
                    50%{background:#3b82f6;box-shadow:0 0 16px #3b82f6;}
                    75%{background:#fbbf24;box-shadow:0 0 16px #fbbf24;}
                    100%{background:#ef4444;box-shadow:0 0 16px #ef4444;}}
@keyframes ping{0%{transform:scale(0.4);opacity:0.9;}100%{transform:scale(2.6);opacity:0;}}
@keyframes wave{0%{transform:translateX(0);opacity:0.6;}100%{transform:translateX(40px);opacity:0;}}
@keyframes sweep{0%,100%{transform:rotate(-22deg);}50%{transform:rotate(22deg);}}
@keyframes breathe{0%,100%{opacity:0.5;}50%{opacity:1;}}
@keyframes scrollroad{from{background-position:0 0;}to{background-position:0 200px;}}
@keyframes shake{0%,100%{transform:translateX(0);}25%{transform:translateX(-1px);}75%{transform:translateX(1px);}}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-4px);}}
'''


def base_html(title, body, extra_css=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{COMMON_CSS}{extra_css}</style>
</head>
<body>
{body}
</body>
</html>'''


def title_bar(view, name, vibe, prev_view, next_view):
    return f'''<div class="title-bar">
  <div class="badge">🤖 Maqueen Emulator · View {view} — {name}</div>
  <div class="vibe">{vibe}</div>
  <div class="nav">
    <a href="maqueen-emu.html">⚙ Picker</a>
    <a href="maqueen-emu_{prev_view}.html">‹ Prev</a>
    <a href="maqueen-emu_{next_view}.html">Next ›</a>
    <a href="index.html">🧪 Labs</a>
  </div>
</div>'''


# ╔════════════════════════════════════════════════════════════════════╗
# ║  micro:bit 5×5 matrix (animated heart)                              ║
# ╚════════════════════════════════════════════════════════════════════╝
def matrix_5x5_html(cell=11, gap=3):
    """Heart pattern. Each LED has its own pulse delay for a 'breathe' effect."""
    pat = [[0,1,0,1,0],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]]
    cells = ''
    i = 0
    for r in range(5):
        for c in range(5):
            if pat[r][c]:
                cells += f'<div style="width:{cell}px;height:{cell}px;border-radius:50%;background:#ef4444;box-shadow:0 0 8px #ef4444,inset 0 0 2px rgba(0,0,0,0.6);animation:breathe {1.4+(i%5)*0.12:.2f}s ease-in-out infinite;animation-delay:{i*0.04}s;"></div>'
            else:
                cells += f'<div style="width:{cell}px;height:{cell}px;border-radius:50%;background:#1a0500;box-shadow:inset 0 0 2px #000;"></div>'
            i += 1
    return f'<div style="display:grid;grid-template-columns:repeat(5,{cell}px);gap:{gap}px;">{cells}</div>'


# ╔════════════════════════════════════════════════════════════════════╗
# ║  VIEW A — Photo-real 3/4 isometric hero shot                        ║
# ╚════════════════════════════════════════════════════════════════════╝
def make_A():
    nav = title_bar('A', 'Photo-Real Hero', '3/4 isometric · live readouts · gentle anims', 'C', 'B')

    # Robot SVG: 3/4 isometric, ~700×500 viewBox.
    # Layers (bottom→top): floor shadow, chassis PCB, wheels, top deck (acrylic), micro:bit + battery,
    # servo arm, ultrasonic sensor, RGB LED row.
    robot = '''
<svg viewBox="0 0 700 540" style="width:100%;height:auto;display:block;" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="pcb" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#1a1f28"/>
      <stop offset="100%" stop-color="#04060a"/>
    </linearGradient>
    <linearGradient id="acrylic" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#e5e7eb" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#9ca3af" stop-opacity="0.6"/>
    </linearGradient>
    <radialGradient id="tireGrad" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#1a1a1a"/>
      <stop offset="80%" stop-color="#0a0a0a"/>
      <stop offset="100%" stop-color="#000"/>
    </radialGradient>
    <radialGradient id="rimGrad" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#fde68a"/>
      <stop offset="50%" stop-color="#fbbf24"/>
      <stop offset="100%" stop-color="#a16207"/>
    </radialGradient>
    <linearGradient id="ultraBody" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#1f2937"/>
      <stop offset="100%" stop-color="#0a0a0a"/>
    </linearGradient>
    <linearGradient id="batt" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#dc2626"/>
      <stop offset="100%" stop-color="#7f1d1d"/>
    </linearGradient>
    <radialGradient id="led1g"><stop offset="0%" stop-color="#fff"/><stop offset="40%" stop-color="#f472b6"/><stop offset="100%" stop-color="#5c1a3a"/></radialGradient>
    <radialGradient id="led2g"><stop offset="0%" stop-color="#fff"/><stop offset="40%" stop-color="#22d3ee"/><stop offset="100%" stop-color="#0a3a4a"/></radialGradient>
    <filter id="softshadow"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>

  <!-- floor shadow -->
  <ellipse cx="370" cy="490" rx="220" ry="20" fill="#000" opacity="0.55" filter="url(#softshadow)"/>

  <!-- LEFT WHEEL (back, partially hidden) -->
  <g transform="translate(150, 380)">
    <ellipse cx="0" cy="0" rx="50" ry="60" fill="url(#tireGrad)" stroke="#000" stroke-width="2"/>
    <g style="transform-origin:center;animation:spin 1.6s linear infinite;">
      <ellipse cx="0" cy="0" rx="32" ry="40" fill="url(#rimGrad)" stroke="#000" stroke-width="1.5"/>
      <circle cx="0" cy="0" r="6" fill="#1a1a1a"/>
      <line x1="-32" y1="0" x2="32" y2="0" stroke="#000" stroke-width="2"/>
      <line x1="0" y1="-40" x2="0" y2="40" stroke="#000" stroke-width="2"/>
      <line x1="-22" y1="-28" x2="22" y2="28" stroke="#000" stroke-width="1.5"/>
      <line x1="-22" y1="28" x2="22" y2="-28" stroke="#000" stroke-width="1.5"/>
    </g>
  </g>

  <!-- RIGHT WHEEL (front-right, visible) -->
  <g transform="translate(580, 380) rotate(8)">
    <ellipse cx="0" cy="0" rx="50" ry="62" fill="url(#tireGrad)" stroke="#000" stroke-width="2"/>
    <!-- tire tread -->
    ''' + ''.join(f'<line x1="-50" y1="{y}" x2="50" y2="{y}" stroke="#1f2937" stroke-width="1.4" opacity="0.6"/>' for y in range(-55, 56, 8)) + '''
    <g style="transform-origin:center;animation:spin 1.6s linear infinite;">
      <ellipse cx="0" cy="0" rx="34" ry="42" fill="url(#rimGrad)" stroke="#000" stroke-width="1.5"/>
      <circle cx="0" cy="0" r="7" fill="#1a1a1a" stroke="#000" stroke-width="1"/>
      <line x1="-34" y1="0" x2="34" y2="0" stroke="#000" stroke-width="2"/>
      <line x1="0" y1="-42" x2="0" y2="42" stroke="#000" stroke-width="2"/>
      <line x1="-24" y1="-30" x2="24" y2="30" stroke="#000" stroke-width="1.5"/>
      <line x1="-24" y1="30" x2="24" y2="-30" stroke="#000" stroke-width="1.5"/>
    </g>
  </g>

  <!-- CHASSIS PCB (rounded triangle, perspective-distorted to 3/4) -->
  <path d="M 200 380
           Q 150 360 170 300
           L 250 220
           Q 360 195 470 215
           L 560 290
           Q 580 360 530 380
           Z"
        fill="url(#pcb)" stroke="#000" stroke-width="2" filter="url(#softshadow)"/>
  <!-- PCB silkscreen: white outline + traces -->
  <path d="M 200 380 Q 150 360 170 300 L 250 220 Q 360 195 470 215 L 560 290 Q 580 360 530 380 Z"
        fill="none" stroke="#fff" stroke-width="0.6" opacity="0.4"/>
  <!-- "Maqueen Lite" silkscreen text -->
  <text x="365" y="340" text-anchor="middle" fill="#fff" opacity="0.6" font-size="10" font-family="Helvetica" font-weight="800" letter-spacing="0.1em">MAQUEEN LITE V4</text>
  <text x="365" y="355" text-anchor="middle" fill="#fff" opacity="0.4" font-size="7" font-family="Helvetica">DFROBOT · MICRO:BIT</text>

  <!-- FRONT CASTER WHEEL (white plastic ball) -->
  <ellipse cx="240" cy="395" rx="22" ry="14" fill="#e5e7eb" stroke="#666" stroke-width="1.5"/>
  <ellipse cx="240" cy="392" rx="20" ry="11" fill="#fff" opacity="0.6"/>

  <!-- 4 RGB LEDs row (front edge) -->
  <g transform="translate(220, 365)">
    <circle cx="0"  cy="0" r="11" fill="url(#led1g)" stroke="#000" stroke-width="0.8" style="animation:blink 1.2s infinite;"/>
    <circle cx="42" cy="0" r="11" fill="url(#led2g)" stroke="#000" stroke-width="0.8" style="animation:blink 1.2s infinite 0.3s;"/>
    <circle cx="84" cy="0" r="11" fill="url(#led1g)" stroke="#000" stroke-width="0.8" style="animation:blink 1.2s infinite 0.6s;"/>
    <circle cx="126" cy="0" r="11" fill="url(#led2g)" stroke="#000" stroke-width="0.8" style="animation:blink 1.2s infinite 0.9s;"/>
    <!-- glow halos -->
    <circle cx="0" cy="0" r="20" fill="#f472b6" opacity="0.18"><animate attributeName="opacity" values="0.18;0.05;0.18" dur="1.2s" repeatCount="indefinite"/></circle>
    <circle cx="42" cy="0" r="20" fill="#22d3ee" opacity="0.18"><animate attributeName="opacity" values="0.05;0.18;0.05" dur="1.2s" repeatCount="indefinite"/></circle>
    <circle cx="84" cy="0" r="20" fill="#f472b6" opacity="0.18"><animate attributeName="opacity" values="0.18;0.05;0.18" dur="1.2s" repeatCount="indefinite" begin="0.6s"/></circle>
    <circle cx="126" cy="0" r="20" fill="#22d3ee" opacity="0.18"><animate attributeName="opacity" values="0.05;0.18;0.05" dur="1.2s" repeatCount="indefinite" begin="0.9s"/></circle>
  </g>

  <!-- IR receiver dome (small black bump) -->
  <ellipse cx="365" cy="370" rx="9" ry="6" fill="#0a0a0a" stroke="#000" stroke-width="1"/>
  <circle cx="365" cy="370" r="4" fill="#1f2937"/>
  <circle cx="365" cy="370" r="2" fill="#f472b6" opacity="0.7"><animate attributeName="opacity" values="0.7;0.2;0.7" dur="1.4s" repeatCount="indefinite"/></circle>

  <!-- TOP DECK (acrylic plate, with mounting holes pattern) -->
  <path d="M 240 215
           L 480 215
           L 510 270
           L 220 280
           Z"
        fill="url(#acrylic)" stroke="#666" stroke-width="1.2" opacity="0.85"/>
  <!-- mounting holes -->
  ''' + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="#0a0a0a" stroke="#666" stroke-width="0.5"/>' for x, y in [(280,235),(330,240),(380,240),(430,240),(470,250),(260,265),(490,265)]) + '''
  <!-- decorative star cutout -->
  <polygon points="365,228 369,238 380,238 371,244 374,254 365,248 356,254 359,244 350,238 361,238" fill="#0a0a0a" opacity="0.7"/>

  <!-- micro:bit V2 board (mounted on chassis edge connector, slightly tilted) -->
  <g transform="translate(285, 290) rotate(-3)">
    <rect x="0" y="0" width="100" height="80" rx="3" fill="#1a3a5a" stroke="#000" stroke-width="1.5"/>
    <!-- gold edge fingers -->
    <rect x="0" y="78" width="100" height="6" fill="#fbbf24" stroke="#a16207" stroke-width="0.4"/>
    ''' + ''.join(f'<line x1="{x}" y1="78" x2="{x}" y2="84" stroke="#a16207" stroke-width="0.4"/>' for x in range(4, 100, 4)) + '''
    <!-- 5x5 LED matrix -->
    <g transform="translate(28, 22)">
      ''' + ''.join(f'<circle cx="{c*10}" cy="{r*10}" r="3" fill="#ef4444" opacity="{0.3+0.7*((r*5+c)%3==0)}"><animate attributeName="opacity" values="0.3;1;0.3" dur="{1.2+(r*5+c)%5*0.15:.2f}s" repeatCount="indefinite" begin="{(r*5+c)*0.04}s"/></circle>' for r in range(5) for c in range(5)) + '''
    </g>
    <!-- A and B buttons -->
    <circle cx="14" cy="42" r="6" fill="#000" stroke="#9ca3af" stroke-width="1"/>
    <text x="14" y="46" text-anchor="middle" fill="#fff" font-size="7" font-weight="900" font-family="Helvetica">A</text>
    <circle cx="86" cy="42" r="6" fill="#000" stroke="#9ca3af" stroke-width="1"/>
    <text x="86" y="46" text-anchor="middle" fill="#fff" font-size="7" font-weight="900" font-family="Helvetica">B</text>
    <!-- micro:bit logo -->
    <text x="50" y="14" text-anchor="middle" fill="#fff" font-size="6" font-family="Helvetica" font-weight="800" opacity="0.7">micro:bit V2</text>
  </g>

  <!-- BATTERY PACK (red, with AAs visible) -->
  <g transform="translate(420, 230) rotate(-3)">
    <rect x="0" y="0" width="80" height="40" rx="3" fill="url(#batt)" stroke="#000" stroke-width="1.2"/>
    <text x="40" y="16" text-anchor="middle" fill="#fff" font-size="7" font-family="Helvetica" font-weight="800">3.7V Li-Po</text>
    <rect x="6" y="22" width="22" height="14" rx="1" fill="#9ca3af" stroke="#000" stroke-width="0.5"/>
    <rect x="30" y="22" width="22" height="14" rx="1" fill="#9ca3af" stroke="#000" stroke-width="0.5"/>
    <rect x="54" y="22" width="22" height="14" rx="1" fill="#9ca3af" stroke="#000" stroke-width="0.5"/>
  </g>

  <!-- SERVO ARM (rises from middle of top deck up to ultrasonic) -->
  <g style="transform-origin:365px 240px;animation:sweep 3s ease-in-out infinite;">
    <!-- servo body -->
    <rect x="350" y="170" width="30" height="50" rx="3" fill="#1f2937" stroke="#000" stroke-width="1.2"/>
    <text x="365" y="200" text-anchor="middle" fill="#fbbf24" font-size="6" font-family="Helvetica" font-weight="800">SERVO</text>
    <!-- arm segment up to ultrasonic -->
    <line x1="365" y1="170" x2="365" y2="120" stroke="#9ca3af" stroke-width="6"/>
    <line x1="365" y1="170" x2="365" y2="120" stroke="#1f2937" stroke-width="3"/>

    <!-- ULTRASONIC SENSOR (HC-SR04 with twin silver eyes) -->
    <g transform="translate(310, 60)">
      <rect x="0" y="0" width="110" height="60" rx="6" fill="url(#ultraBody)" stroke="#000" stroke-width="1.5"/>
      <!-- twin eyes -->
      <circle cx="32" cy="30" r="20" fill="#2a2a2a" stroke="#000" stroke-width="1.5"/>
      <circle cx="32" cy="30" r="16" fill="#9ca3af" stroke="#666" stroke-width="0.6"/>
      <circle cx="32" cy="30" r="14" fill="#374151"/>
      <!-- speaker grill pattern -->
      ''' + ''.join(f'<circle cx="{32+dx}" cy="{30+dy}" r="0.8" fill="#000"/>' for dx in [-8,-4,0,4,8] for dy in [-8,-4,0,4,8]) + '''
      <circle cx="78" cy="30" r="20" fill="#2a2a2a" stroke="#000" stroke-width="1.5"/>
      <circle cx="78" cy="30" r="16" fill="#9ca3af" stroke="#666" stroke-width="0.6"/>
      <circle cx="78" cy="30" r="14" fill="#374151"/>
      ''' + ''.join(f'<circle cx="{78+dx}" cy="{30+dy}" r="0.8" fill="#000"/>' for dx in [-8,-4,0,4,8] for dy in [-8,-4,0,4,8]) + '''
      <text x="55" y="55" text-anchor="middle" fill="#22d3ee" font-size="5" font-family="Helvetica" font-weight="800">DFROBOT</text>
    </g>

    <!-- ping rings emanating from sensor -->
    <g transform="translate(365, 90)">
      <circle r="20" fill="none" stroke="#22d3ee" stroke-width="2" opacity="0.7" style="animation:ping 1.4s ease-out infinite;"/>
      <circle r="20" fill="none" stroke="#22d3ee" stroke-width="2" opacity="0.7" style="animation:ping 1.4s ease-out infinite 0.45s;"/>
      <circle r="20" fill="none" stroke="#22d3ee" stroke-width="2" opacity="0.7" style="animation:ping 1.4s ease-out infinite 0.9s;"/>
    </g>
  </g>

  <!-- buzzer speaker icon (small, on PCB) -->
  <g transform="translate(490, 320)">
    <circle r="9" fill="#0a0a0a" stroke="#666" stroke-width="1"/>
    <circle r="6" fill="none" stroke="#fbbf24" stroke-width="0.6"/>
    <text y="2" text-anchor="middle" fill="#fbbf24" font-size="8" font-weight="900">♪</text>
    <!-- sound waves -->
    <path d="M 12 -4 Q 18 0 12 4" fill="none" stroke="#fbbf24" stroke-width="1" opacity="0.7" style="animation:wave 1.4s ease-out infinite;"/>
    <path d="M 18 -7 Q 26 0 18 7" fill="none" stroke="#fbbf24" stroke-width="1" opacity="0.5" style="animation:wave 1.4s ease-out infinite 0.45s;"/>
  </g>

  <!-- line sensors (under chassis, peek out at front-bottom) -->
  <rect x="345" y="378" width="8" height="6" fill="#22d3ee" opacity="0.85"><animate attributeName="opacity" values="0.4;1;0.4" dur="1.3s" repeatCount="indefinite"/></rect>
  <rect x="377" y="378" width="8" height="6" fill="#22d3ee" opacity="0.85"><animate attributeName="opacity" values="1;0.4;1" dur="1.3s" repeatCount="indefinite"/></rect>
</svg>'''

    # Live readouts side panel — each tile is paired (visually) with a robot component
    readouts = '''
<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;font-size:11px;">
  <div class="rd"><div class="rd-h" style="color:#fbbf24;">⟳ MOTOR L</div><div class="rd-v">156 RPM</div><div class="rd-bar"><div style="width:65%;background:#fbbf24;box-shadow:0 0 6px #fbbf24;"></div></div></div>
  <div class="rd"><div class="rd-h" style="color:#fbbf24;">⟳ MOTOR R</div><div class="rd-v">158 RPM</div><div class="rd-bar"><div style="width:67%;background:#fbbf24;box-shadow:0 0 6px #fbbf24;"></div></div></div>
  <div class="rd"><div class="rd-h" style="color:#f472b6;">◐ LED 1</div><div class="rd-v" style="color:#f472b6;">#F472B6</div></div>
  <div class="rd"><div class="rd-h" style="color:#22d3ee;">◐ LED 2</div><div class="rd-v" style="color:#22d3ee;">#22D3EE</div></div>
  <div class="rd"><div class="rd-h" style="color:#f472b6;">◐ LED 3</div><div class="rd-v" style="color:#f472b6;">#F472B6</div></div>
  <div class="rd"><div class="rd-h" style="color:#22d3ee;">◐ LED 4</div><div class="rd-v" style="color:#22d3ee;">#22D3EE</div></div>
  <div class="rd"><div class="rd-h" style="color:#22d3ee;">⤺ SERVO</div><div class="rd-v">90° (sweep)</div></div>
  <div class="rd"><div class="rd-h" style="color:#22d3ee;">📡 ULTRA</div><div class="rd-v">42 cm</div></div>
  <div class="rd"><div class="rd-h" style="color:#ef4444;">▦ MATRIX</div><div class="rd-v">heart · pulse</div></div>
  <div class="rd"><div class="rd-h" style="color:#f472b6;">◉ IR RX</div><div class="rd-v">[ ▲ FWD ]</div></div>
  <div class="rd"><div class="rd-h" style="color:#22c55e;">▦ LINE L/R</div><div class="rd-v">0 / 0 (track)</div></div>
  <div class="rd"><div class="rd-h" style="color:#fbbf24;">♪ BUZZER</div><div class="rd-v">A4 · 440 Hz</div></div>
  <div class="rd"><div class="rd-h" style="color:#a78bfa;">⌘ ACCEL</div><div class="rd-v">X+0.12 Z+0.98</div></div>
  <div class="rd"><div class="rd-h" style="color:#22c55e;">⚡ BATTERY</div><div class="rd-v">87% · 3.78V</div></div>
</div>'''

    css_extra = '''
.stage{max-width:1400px;margin:0 auto;display:grid;grid-template-columns:2.2fr 1fr;gap:18px;align-items:start;}
@media(max-width:980px){.stage{grid-template-columns:1fr;}}
.canvas{background:radial-gradient(ellipse at 50% 70%,#1a2030 0%,#04060a 80%);
  border:1px solid #1e3a5a;border-radius:12px;padding:18px;
  box-shadow:inset 0 0 30px rgba(0,0,0,0.6);}
.panel{background:linear-gradient(180deg,#0e1a2a,#04060a);border:1px solid #1e3a5a;
  border-radius:12px;padding:14px;}
.panel h3{font-size:12px;color:#22d3ee;letter-spacing:0.1em;margin-bottom:10px;
  font-weight:800;border-bottom:1px solid #1e3a5a;padding-bottom:6px;}
.rd{background:#0a1018;border:1px solid #1e3a5a;border-radius:5px;padding:6px 8px;}
.rd-h{font-size:8px;letter-spacing:0.1em;font-weight:800;margin-bottom:3px;}
.rd-v{font-size:12px;color:#fff;font-weight:800;font-family:'Courier New',monospace;}
.rd-bar{height:4px;background:#1e3a5a;border-radius:2px;margin-top:4px;overflow:hidden;}
.rd-bar > div{height:100%;}
'''
    body = nav + f'''
<div class="stage">
  <div class="canvas">{robot}</div>
  <div class="panel">
    <h3>📡 LIVE READOUTS</h3>
    {readouts}
  </div>
</div>'''
    return base_html('🤖 Maqueen Emulator · A — Photo-Real Hero', body, css_extra)


# ╔════════════════════════════════════════════════════════════════════╗
# ║  VIEW B — Track action (top-down arcade)                            ║
# ╚════════════════════════════════════════════════════════════════════╝
def make_B():
    nav = title_bar('B', 'Track Action', 'top-down arcade · driving on track', 'A', 'C')

    # Top-down robot ~140px wide. Sits centered on canvas. Track scrolls behind.
    robot_top = '''
<svg viewBox="0 0 200 220" style="width:200px;height:220px;display:block;" preserveAspectRatio="xMidYMid meet">
  <defs>
    <radialGradient id="rim2" cx="40%" cy="40%" r="60%"><stop offset="0%" stop-color="#fde68a"/><stop offset="60%" stop-color="#fbbf24"/><stop offset="100%" stop-color="#a16207"/></radialGradient>
  </defs>
  <!-- chassis (top-down rounded triangle) -->
  <path d="M 100 30 Q 175 50 175 130 Q 175 180 100 195 Q 25 180 25 130 Q 25 50 100 30 Z"
        fill="#1a1f28" stroke="#000" stroke-width="1.5"/>
  <!-- left wheel -->
  <rect x="5" y="100" width="22" height="50" rx="4" fill="#0a0a0a" stroke="#000" stroke-width="1.2"/>
  <ellipse cx="16" cy="125" rx="6" ry="14" fill="url(#rim2)" stroke="#000" stroke-width="0.8"/>
  <!-- right wheel -->
  <rect x="173" y="100" width="22" height="50" rx="4" fill="#0a0a0a" stroke="#000" stroke-width="1.2"/>
  <ellipse cx="184" cy="125" rx="6" ry="14" fill="url(#rim2)" stroke="#000" stroke-width="0.8"/>
  <!-- caster -->
  <circle cx="100" cy="190" r="8" fill="#e5e7eb" stroke="#666" stroke-width="0.8"/>
  <!-- micro:bit on top (small) -->
  <rect x="65" y="80" width="70" height="55" rx="2" fill="#1a3a5a" stroke="#000" stroke-width="1"/>
  ''' + ''.join(f'<circle cx="{75+c*8}" cy="{92+r*8}" r="2" fill="#ef4444" opacity="{0.4+0.6*((r+c)%2==0)}"><animate attributeName="opacity" values="0.4;1;0.4" dur="1s" repeatCount="indefinite" begin="{(r*5+c)*0.04}s"/></circle>' for r in range(5) for c in range(5)) + '''
  <!-- ultrasonic on front (small) -->
  <rect x="60" y="35" width="80" height="30" rx="4" fill="#1f2937" stroke="#000" stroke-width="1"/>
  <circle cx="80" cy="50" r="11" fill="#374151" stroke="#000" stroke-width="0.8"/>
  <circle cx="120" cy="50" r="11" fill="#374151" stroke="#000" stroke-width="0.8"/>
  <!-- 4 RGB LEDs on front -->
  ''' + ''.join(f'<circle cx="{55+i*30}" cy="195" r="6" fill="#{c}" style="animation:blink 1.2s infinite {i*0.3}s;filter:drop-shadow(0 0 6px #{c});"/>' for i, c in enumerate(['ef4444','22c55e','3b82f6','fbbf24'])) + '''
  <!-- direction arrow -->
  <polygon points="100,15 90,30 110,30" fill="#22d3ee" opacity="0.8"/>
</svg>'''

    css_extra = '''
.arena{position:relative;max-width:1400px;margin:0 auto;height:78vh;min-height:560px;
  border:2px solid #1e3a5a;border-radius:12px;overflow:hidden;
  background:
    repeating-linear-gradient(0deg,#0e1a2a 0px,#0e1a2a 200px,#143050 200px,#143050 220px),
    radial-gradient(ellipse at 50% 50%,#1a2030 0%,#04060a 80%);
  background-size:100% 220px, 100% 100%;
  animation:scrollroad 4s linear infinite;
  box-shadow:inset 0 0 60px rgba(0,0,0,0.7);}
/* line track (curving black band) */
.track{position:absolute;left:50%;transform:translateX(-50%);top:0;bottom:0;width:120px;
  background:repeating-linear-gradient(180deg,
    #000 0,#000 60px,
    transparent 60px,transparent 90px,
    #000 90px,#000 200px,
    transparent 200px,transparent 250px);
  background-size:100% 250px;
  animation:scrollroad 2s linear infinite;
  border-left:2px dashed rgba(34,211,238,0.3);
  border-right:2px dashed rgba(34,211,238,0.3);}
/* white road edges */
.edge-l,.edge-r{position:absolute;top:0;bottom:0;width:6px;background:#fff;opacity:0.85;}
.edge-l{left:30%;}.edge-r{right:30%;}
/* checkered finish flag (slides down periodically) */
.finish{position:absolute;left:50%;transform:translateX(-50%);width:300px;height:30px;
  background:repeating-conic-gradient(#000 0% 25%,#fff 0% 50%);background-size:30px 30px;
  top:-30px;animation:finishline 8s linear infinite;border:2px solid #fbbf24;}
@keyframes finishline{0%,80%{top:-30px;}90%{top:50%;}100%{top:120%;}}
/* obstacle ahead */
.obstacle{position:absolute;left:50%;transform:translateX(-50%);top:18%;
  width:50px;height:50px;background:linear-gradient(135deg,#ef4444,#7f1d1d);
  border:2px solid #000;border-radius:6px;box-shadow:0 0 14px rgba(239,68,68,0.6);
  display:grid;place-items:center;color:#fff;font-weight:900;font-size:24px;
  animation:obspulse 2s ease-in-out infinite;}
@keyframes obspulse{0%,100%{transform:translateX(-50%) scale(1);box-shadow:0 0 14px rgba(239,68,68,0.6);}50%{transform:translateX(-50%) scale(1.08);box-shadow:0 0 24px rgba(239,68,68,0.95);}}
/* robot (centered, bobbing) */
.robot-stage{position:absolute;left:50%;bottom:14%;transform:translateX(-50%);
  animation:float 1s ease-in-out infinite;z-index:5;}
/* ultrasonic cone */
.cone{position:absolute;left:50%;bottom:46%;transform:translateX(-50%);
  width:0;height:0;border-left:60px solid transparent;border-right:60px solid transparent;
  border-bottom:160px solid rgba(34,197,94,0.18);
  animation:conepulse 2s ease-in-out infinite;}
@keyframes conepulse{0%,100%{opacity:0.4;}50%{opacity:0.8;}}
/* HUD */
.hud{position:absolute;top:14px;left:14px;right:14px;display:flex;justify-content:space-between;
  font-family:'JetBrains Mono',monospace;color:#22d3ee;text-shadow:0 0 4px #22d3ee;
  z-index:10;pointer-events:none;}
.hud-tile{background:rgba(2,8,16,0.85);border:1px solid #22d3ee;padding:6px 12px;border-radius:5px;
  font-size:13px;font-weight:800;}
.hud-bar{display:flex;gap:8px;}
.controls{position:absolute;bottom:14px;left:14px;right:14px;display:flex;justify-content:space-between;align-items:end;z-index:10;}
.dpad{display:grid;grid-template-columns:repeat(3,40px);gap:3px;}
.dpad div{background:linear-gradient(180deg,#1f2937,#0a0a0a);border:1px solid #fbbf24;color:#fbbf24;
  font-weight:900;font-size:18px;display:grid;place-items:center;border-radius:5px;height:40px;
  box-shadow:0 2px 4px rgba(0,0,0,0.6);}
.dpad .empty{visibility:hidden;}
.dpad .center{background:#7f1d1d;color:#fff;border-color:#fff;}
.scoreboard{background:rgba(2,8,16,0.85);border:1px solid #fbbf24;padding:8px 14px;border-radius:5px;
  color:#fbbf24;font-family:'JetBrains Mono',monospace;font-weight:800;font-size:14px;text-shadow:0 0 4px #fbbf24;}
'''
    body = nav + f'''
<div class="arena">
  <div class="track"></div>
  <div class="edge-l"></div>
  <div class="edge-r"></div>
  <div class="finish"></div>
  <div class="obstacle">!</div>
  <div class="cone"></div>
  <div class="robot-stage">{robot_top}</div>

  <div class="hud">
    <div class="hud-bar">
      <div class="hud-tile">⚡ 87%</div>
      <div class="hud-tile">⏱ 02:14</div>
      <div class="hud-tile">📡 42 cm</div>
    </div>
    <div class="hud-bar">
      <div class="hud-tile" style="border-color:#22c55e;color:#22c55e;text-shadow:0 0 4px #22c55e;">L:0 R:0 ✓</div>
      <div class="hud-tile" style="border-color:#fbbf24;color:#fbbf24;text-shadow:0 0 4px #fbbf24;">156 / 158 RPM</div>
    </div>
  </div>

  <div class="controls">
    <div class="dpad">
      <div class="empty"></div><div>▲</div><div class="empty"></div>
      <div>◀</div><div class="center">●</div><div>▶</div>
      <div class="empty"></div><div>▼</div><div class="empty"></div>
    </div>
    <div style="display:flex;gap:8px;align-items:end;">
      <div class="scoreboard">SCORE: 1240</div>
      <div class="scoreboard" style="border-color:#22c55e;color:#22c55e;text-shadow:0 0 4px #22c55e;">LAP 2/5</div>
    </div>
  </div>
</div>'''
    return base_html('🤖 Maqueen Emulator · B — Track Action', body, css_extra)


# ╔════════════════════════════════════════════════════════════════════╗
# ║  VIEW C — Exploded diagram (vertical layers + numbered callouts)    ║
# ╚════════════════════════════════════════════════════════════════════╝
def make_C():
    nav = title_bar('C', 'Exploded Diagram', 'parts pulled apart · numbered callouts · educational', 'B', 'A')

    # Layers stacked vertically with gaps. Each is a small SVG. Numbered.
    def layer(num, title, spec, svg, color='#22d3ee'):
        return f'''<div class="layer" style="border-color:{color};">
  <div class="layer-num" style="background:{color};">{num}</div>
  <div class="layer-svg">{svg}</div>
  <div class="layer-info">
    <div class="layer-title" style="color:{color};">{title}</div>
    <div class="layer-spec">{spec}</div>
  </div>
  <div class="layer-conn"></div>
</div>'''

    # 1. Ultrasonic sensor
    s_ultra = '''<svg viewBox="0 0 240 70" style="width:240px;height:70px;"><rect x="0" y="0" width="240" height="60" rx="6" fill="#1f2937" stroke="#000" stroke-width="1.5"/>
<circle cx="60" cy="30" r="22" fill="#374151" stroke="#000" stroke-width="1.5"/><circle cx="60" cy="30" r="16" fill="#9ca3af"/>
<circle cx="180" cy="30" r="22" fill="#374151" stroke="#000" stroke-width="1.5"/><circle cx="180" cy="30" r="16" fill="#9ca3af"/>
<text x="120" y="56" text-anchor="middle" fill="#22d3ee" font-size="7" font-family="Helvetica" font-weight="800">DFROBOT · HC-SR04</text>
<g transform="translate(120,30)"><circle r="6" fill="none" stroke="#22d3ee" stroke-width="1" opacity="0.7"><animate attributeName="r" values="6;30;6" dur="1.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0;0.7" dur="1.4s" repeatCount="indefinite"/></circle></g></svg>'''

    # 2. Servo
    s_servo = '''<svg viewBox="0 0 240 60" style="width:240px;height:60px;"><rect x="80" y="10" width="80" height="40" rx="4" fill="#1f2937" stroke="#000" stroke-width="1.5"/>
<text x="120" y="34" text-anchor="middle" fill="#fbbf24" font-size="9" font-family="Helvetica" font-weight="800">SERVO 9G</text>
<rect x="40" y="22" width="40" height="16" rx="2" fill="#9ca3af" stroke="#000" stroke-width="1"/>
<circle cx="20" cy="30" r="10" fill="#fbbf24" stroke="#000" stroke-width="1.2"><animate attributeName="cx" values="20;30;20" dur="3s" repeatCount="indefinite"/></circle></svg>'''

    # 3. Acrylic top plate
    s_acryl = '''<svg viewBox="0 0 280 50" style="width:280px;height:50px;"><path d="M 20 5 L 260 5 L 270 35 L 10 35 Z" fill="#9ca3af" fill-opacity="0.6" stroke="#666" stroke-width="1.2"/>
''' + ''.join(f'<circle cx="{x}" cy="20" r="3" fill="#0a0a0a"/>' for x in [40, 80, 120, 160, 200, 240]) + '''
<polygon points="140,12 144,22 154,22 146,28 149,38 140,32 131,38 134,28 126,22 136,22" fill="#0a0a0a"/></svg>'''

    # 4. Battery pack
    s_batt = '''<svg viewBox="0 0 240 50" style="width:240px;height:50px;"><rect x="40" y="5" width="160" height="40" rx="4" fill="#dc2626" stroke="#000" stroke-width="1.5"/>
<text x="120" y="22" text-anchor="middle" fill="#fff" font-size="8" font-family="Helvetica" font-weight="800">3.7V Li-Po · 1000mAh</text>
<rect x="50" y="28" width="36" height="12" rx="1" fill="#9ca3af" stroke="#000" stroke-width="0.6"/>
<rect x="92" y="28" width="36" height="12" rx="1" fill="#9ca3af" stroke="#000" stroke-width="0.6"/>
<rect x="134" y="28" width="36" height="12" rx="1" fill="#9ca3af" stroke="#000" stroke-width="0.6"/></svg>'''

    # 5. micro:bit V2
    s_mbit = '''<svg viewBox="0 0 280 110" style="width:280px;height:110px;"><rect x="0" y="0" width="280" height="100" rx="4" fill="#1a3a5a" stroke="#000" stroke-width="1.5"/>
<rect x="0" y="98" width="280" height="10" fill="#fbbf24" stroke="#a16207" stroke-width="0.5"/>
''' + ''.join(f'<line x1="{x}" y1="98" x2="{x}" y2="108" stroke="#a16207" stroke-width="0.5"/>' for x in range(8, 280, 6)) + '''
<g transform="translate(95, 25)">''' + ''.join(f'<circle cx="{c*15}" cy="{r*15}" r="5" fill="#ef4444" opacity="{0.3+0.7*((r*5+c+1)%3==0)}"><animate attributeName="opacity" values="0.3;1;0.3" dur="{1.2+(r*5+c)%5*0.15:.2f}s" repeatCount="indefinite" begin="{(r*5+c)*0.04}s"/></circle>' for r in range(5) for c in range(5)) + '''</g>
<circle cx="30" cy="60" r="11" fill="#000" stroke="#9ca3af" stroke-width="1.2"/><text x="30" y="65" text-anchor="middle" fill="#fff" font-size="11" font-weight="900">A</text>
<circle cx="250" cy="60" r="11" fill="#000" stroke="#9ca3af" stroke-width="1.2"/><text x="250" y="65" text-anchor="middle" fill="#fff" font-size="11" font-weight="900">B</text>
<text x="140" y="14" text-anchor="middle" fill="#fff" font-size="8" font-family="Helvetica" font-weight="800" opacity="0.8">micro:bit V2 · nRF52833</text></svg>'''

    # 6. PCB chassis
    s_pcb = '''<svg viewBox="0 0 320 90" style="width:320px;height:90px;"><path d="M 40 10 Q 40 50 60 75 L 260 75 Q 280 50 280 10 Z" fill="#1a1f28" stroke="#000" stroke-width="1.5"/>
<text x="160" y="40" text-anchor="middle" fill="#fff" font-size="9" font-family="Helvetica" font-weight="800" opacity="0.8">MAQUEEN LITE V4 · PCB</text>
<text x="160" y="54" text-anchor="middle" fill="#fff" font-size="6" font-family="Helvetica" opacity="0.5">DFR0822 · DFROBOT 2024</text>
<!-- 4 LEDs -->
''' + ''.join(f'<circle cx="{105+i*30}" cy="68" r="6" fill="#{c}" style="animation:blink 1.2s infinite {i*0.3}s;"/>' for i, c in enumerate(['ef4444','22c55e','3b82f6','fbbf24'])) + '''
<!-- IR dome -->
<ellipse cx="160" cy="62" rx="6" ry="4" fill="#0a0a0a" stroke="#666" stroke-width="0.5"/>
<!-- buzzer -->
<circle cx="245" cy="52" r="6" fill="#0a0a0a" stroke="#fbbf24" stroke-width="0.6"/></svg>'''

    # 7. Wheels + caster
    s_wheels = '''<svg viewBox="0 0 320 70" style="width:320px;height:70px;"><defs><radialGradient id="rim3" cx="40%" cy="40%" r="60%"><stop offset="0%" stop-color="#fde68a"/><stop offset="60%" stop-color="#fbbf24"/><stop offset="100%" stop-color="#a16207"/></radialGradient></defs>
<g transform="translate(40,35)"><ellipse rx="32" ry="32" fill="#0a0a0a" stroke="#000" stroke-width="1.5"/>
<g style="transform-origin:center;animation:spin 1.6s linear infinite;"><ellipse rx="20" ry="20" fill="url(#rim3)" stroke="#000" stroke-width="1"/><line x1="-20" y1="0" x2="20" y2="0" stroke="#000" stroke-width="1.5"/><line x1="0" y1="-20" x2="0" y2="20" stroke="#000" stroke-width="1.5"/></g></g>
<g transform="translate(160,35)"><circle r="14" fill="#e5e7eb" stroke="#666" stroke-width="1"/><circle r="6" fill="#9ca3af"/><text y="36" text-anchor="middle" fill="#9ca3af" font-size="8" font-family="Helvetica">CASTER</text></g>
<g transform="translate(280,35)"><ellipse rx="32" ry="32" fill="#0a0a0a" stroke="#000" stroke-width="1.5"/>
<g style="transform-origin:center;animation:spin 1.6s linear infinite;"><ellipse rx="20" ry="20" fill="url(#rim3)" stroke="#000" stroke-width="1"/><line x1="-20" y1="0" x2="20" y2="0" stroke="#000" stroke-width="1.5"/><line x1="0" y1="-20" x2="0" y2="20" stroke="#000" stroke-width="1.5"/></g></g></svg>'''

    css_extra = '''
.expl{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:18px;padding-bottom:30px;}
.layer{position:relative;display:grid;grid-template-columns:50px 1fr 220px;gap:18px;align-items:center;
  background:rgba(10,16,24,0.6);border-left:4px solid;border-radius:8px;padding:14px 16px;
  box-shadow:0 4px 12px rgba(0,0,0,0.5);}
.layer-num{width:36px;height:36px;border-radius:50%;color:#000;display:grid;place-items:center;
  font-weight:900;font-size:18px;font-family:Helvetica;
  box-shadow:0 0 12px currentColor;}
.layer-svg{display:flex;justify-content:center;}
.layer-info{display:flex;flex-direction:column;gap:4px;}
.layer-title{font-size:14px;font-weight:800;letter-spacing:0.05em;}
.layer-spec{font-size:10px;color:#7fa;line-height:1.5;font-family:'JetBrains Mono',monospace;}
.layer-conn{position:absolute;left:50%;bottom:-18px;transform:translateX(-50%);width:2px;height:18px;
  background:repeating-linear-gradient(180deg,#22d3ee 0,#22d3ee 4px,transparent 4px,transparent 8px);
  opacity:0.5;}
.layer:last-child .layer-conn{display:none;}
.intro{max-width:900px;margin:0 auto 18px;text-align:center;color:#7fa;font-size:13px;line-height:1.6;}
'''
    body = nav + f'''
<div class="intro">
  Each layer of the Maqueen Lite v4. Numbered top → bottom. Each plate has its own animated component
  (matrix pulse, wheels spin, ultrasonic ping, LEDs cycle).
</div>
<div class="expl">
  {layer(1, 'ULTRASONIC SENSOR', 'HC-SR04 · 2–400 cm range · 40 kHz · 5V', s_ultra, '#22d3ee')}
  {layer(2, 'SERVO MOTOR', '9 g micro servo · 0–180° · 1.5 ms PWM', s_servo, '#fbbf24')}
  {layer(3, 'ACRYLIC TOP PLATE', 'Laser-cut 3 mm · M3 mounting holes · star cutout', s_acryl, '#9ca3af')}
  {layer(4, 'BATTERY PACK', '3.7 V Li-Po · 1000 mAh · ~42 min runtime', s_batt, '#ef4444')}
  {layer(5, 'MICRO:BIT V2', 'nRF52833 ARM · 5×5 LED · A/B buttons · BLE', s_mbit, '#1a3a5a')}
  {layer(6, 'PCB CHASSIS', 'Maqueen Lite V4 · 4×RGB LED · IR · buzzer · line-cam', s_pcb, '#22c55e')}
  {layer(7, 'WHEELS + CASTER', '2× yellow drive wheels · TT motor · 1× caster', s_wheels, '#fbbf24')}
</div>'''
    return base_html('🤖 Maqueen Emulator · C — Exploded Diagram', body, css_extra)


# ╔════════════════════════════════════════════════════════════════════╗
# ║  Picker page                                                         ║
# ╚════════════════════════════════════════════════════════════════════╝
def make_picker():
    css_extra = '''
.picker{max-width:1100px;margin:0 auto;}
.intro-pk{text-align:center;color:#7fa;font-size:14px;line-height:1.6;margin-bottom:24px;max-width:760px;margin-left:auto;margin-right:auto;}
h1{text-align:center;color:#22d3ee;font-size:1.8rem;margin-bottom:8px;text-shadow:0 0 8px #22d3ee;}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;}
.card{display:block;text-decoration:none;padding:20px 22px;border-radius:14px;
  border:1.5px solid #1e3a5a;background:linear-gradient(180deg,#0e1a2a,#04060a);color:#dff;
  transition:all 0.15s;}
.card:hover{transform:translateY(-3px);border-color:#22d3ee;box-shadow:0 8px 22px rgba(34,211,238,0.25);}
.card .emoji{font-size:2.4rem;line-height:1;margin-bottom:8px;}
.card .num{font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#7fa;}
.card h3{font-size:1.2rem;color:#22d3ee;margin:6px 0 8px;}
.card .vibe{font-size:0.86rem;color:#dff;opacity:0.85;line-height:1.45;}
.card .dna{margin-top:10px;font-size:0.78rem;color:#fbbf24;font-family:'JetBrains Mono',monospace;}
.nav-back{text-align:center;margin:14px 0 24px;}
.nav-back a{color:#7fa;text-decoration:none;padding:6px 14px;border:1px solid #1e3a5a;border-radius:999px;font-size:0.85rem;margin:0 4px;}
.nav-back a:hover{color:#22d3ee;border-color:#22d3ee;}
'''
    body = '''
<div class="picker">
  <h1>🤖 Maqueen Emulator</h1>
  <p class="intro-pk">Three views of the Maqueen Lite v4 robot, with all hardware drawn faithfully and animated. Static design — no BLE wiring.</p>
  <div class="nav-back">
    <a href="index.html">🧪 All Labs</a>
    <a href="cockpit-lab.html">🛩 Cockpit Panels</a>
    <a href="../index.html">🏠 Robot App</a>
  </div>
  <div class="cards">
    <a class="card" href="maqueen-emu_A.html">
      <div class="emoji">🤖</div>
      <div class="num">maqueen-emu_A.html</div>
      <h3>A. Photo-Real Hero</h3>
      <div class="vibe">3/4 isometric robot — wheels spin, LEDs cycle, ultrasonic pings, matrix pulses, servo arm sweeps. Side panel with live readouts wired to each component.</div>
      <div class="dna">▸ single hero shot · calm · polished</div>
    </a>
    <a class="card" href="maqueen-emu_B.html">
      <div class="emoji">🏁</div>
      <div class="num">maqueen-emu_B.html</div>
      <h3>B. Track Action</h3>
      <div class="vibe">Top-down arcade — robot driving on a black line track with scrolling road, obstacles, ultrasonic cone, HUD, D-pad, scoreboard, lap counter. Mario-Kart vibes.</div>
      <div class="dna">▸ kinetic · game-like · driving</div>
    </a>
    <a class="card" href="maqueen-emu_C.html">
      <div class="emoji">🔧</div>
      <div class="num">maqueen-emu_C.html</div>
      <h3>C. Exploded Diagram</h3>
      <div class="vibe">7 layers pulled apart vertically — ultrasonic, servo, acrylic, battery, micro:bit, PCB, wheels. Each numbered with spec sheet. Educational manual style.</div>
      <div class="dna">▸ educational · technical · datasheet</div>
    </a>
  </div>
</div>'''
    return base_html('🤖 Maqueen Emulator — pick a view', body, css_extra)


# ╔════════════════════════════════════════════════════════════════════╗
# ║  GENERATE                                                            ║
# ╚════════════════════════════════════════════════════════════════════╝
files = [
    ('maqueen-emu.html',   make_picker, 'Picker'),
    ('maqueen-emu_A.html', make_A,      'A — Photo-Real Hero'),
    ('maqueen-emu_B.html', make_B,      'B — Track Action'),
    ('maqueen-emu_C.html', make_C,      'C — Exploded Diagram'),
]
for fname, fn, label in files:
    out = os.path.join(OUT, fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(fn())
    print(f'  + {fname}  ({label})')
print('Done.')
