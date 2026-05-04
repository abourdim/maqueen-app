#!/usr/bin/env python3
"""Maqueen Kids — 7 kid-friendly cartoon robot mockups.

Same robot base (symmetric chunky wheels, visible motors, googly eyes,
smiley matrix, blush) — 7 different personalities/costumes.

Outputs labs/maqueen-kid.html (picker) + maqueen-kid_1..7.html.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'labs')


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  Shared CSS                                                            ║
# ╚══════════════════════════════════════════════════════════════════════╝
COMMON_CSS = '''
*{box-sizing:border-box;margin:0;padding:0;}
html,body{min-height:100vh;overflow-x:hidden;font-family:'Comic Sans MS','Marker Felt',Arial,sans-serif;
  padding:14px;}
body{position:relative;}
/* sparkle starfield background (kid sky) */
body::before{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:
    radial-gradient(2px 2px at 12% 18%,#fff 50%,transparent 50%),
    radial-gradient(2px 2px at 38% 72%,#fff 50%,transparent 50%),
    radial-gradient(3px 3px at 64% 22%,#fbbf24 50%,transparent 50%),
    radial-gradient(2px 2px at 84% 51%,#fff 50%,transparent 50%),
    radial-gradient(2px 2px at 22% 88%,#22d3ee 50%,transparent 50%),
    radial-gradient(3px 3px at 50% 35%,#fff 50%,transparent 50%),
    radial-gradient(2px 2px at 75% 80%,#f472b6 50%,transparent 50%);
  opacity:0.7;animation:twinkle 4s ease-in-out infinite;}
@keyframes twinkle{0%,100%{opacity:0.4;}50%{opacity:0.95;}}

/* Title bar */
.title-bar{position:relative;z-index:5;display:flex;align-items:center;gap:14px;
  padding:10px 18px;border:3px solid #fff;border-radius:18px;
  margin:0 auto 14px;max-width:1400px;
  background:rgba(255,255,255,0.95);
  box-shadow:0 6px 0 rgba(0,0,0,0.4),0 8px 20px rgba(0,0,0,0.3);}
.title-bar .badge{font-size:18px;font-weight:900;letter-spacing:0.02em;text-shadow:2px 2px 0 rgba(0,0,0,0.15);}
.title-bar .vibe{font-size:13px;color:#7c5a32;}
.title-bar .nav{margin-left:auto;display:flex;gap:6px;}
.title-bar .nav a{text-decoration:none;border:2px solid;border-radius:999px;
  padding:5px 14px;font-size:12px;font-weight:800;
  box-shadow:0 3px 0 rgba(0,0,0,0.2);transition:transform 0.1s;}
.title-bar .nav a:hover{transform:translateY(-2px);}

/* Stage */
.stage{position:relative;z-index:3;max-width:1100px;margin:0 auto;padding:30px 14px;
  display:grid;grid-template-columns:1fr;place-items:center;gap:30px;}
.scene{position:relative;width:100%;max-width:780px;aspect-ratio:5/4;
  border-radius:30px;border:6px solid;
  box-shadow:0 14px 0 rgba(0,0,0,0.3),0 20px 40px rgba(0,0,0,0.5);
  overflow:hidden;}

/* Speech bubble */
.bubble{position:absolute;background:#fff;border:4px solid #000;border-radius:22px;
  padding:10px 18px;font-weight:900;font-size:18px;color:#000;
  box-shadow:5px 5px 0 rgba(0,0,0,0.4);
  z-index:10;animation:bubbleBob 2s ease-in-out infinite;}
@keyframes bubbleBob{0%,100%{transform:translateY(0) rotate(-2deg);}50%{transform:translateY(-4px) rotate(2deg);}}
.bubble::after{content:'';position:absolute;left:30px;bottom:-18px;
  border:10px solid transparent;border-top-color:#000;border-bottom:0;}
.bubble::before{content:'';position:absolute;left:34px;bottom:-12px;
  border:8px solid transparent;border-top-color:#fff;border-bottom:0;z-index:1;}

/* Comic-style sound-effect text */
.boom{position:absolute;font-size:32px;font-weight:900;color:#fff;
  -webkit-text-stroke:3px #000;text-stroke:3px #000;
  text-shadow:4px 4px 0 #000;pointer-events:none;z-index:9;
  animation:boomPulse 1.5s ease-in-out infinite;}
@keyframes boomPulse{0%,100%{transform:scale(1) rotate(-8deg);}50%{transform:scale(1.15) rotate(8deg);}}

/* Animations */
@keyframes spin{to{transform:rotate(360deg);}}
@keyframes blink{0%,55%{opacity:1;}56%,100%{opacity:0.2;}}
@keyframes ledcycle{0%{fill:#ef4444;}25%{fill:#22c55e;}50%{fill:#3b82f6;}75%{fill:#fbbf24;}100%{fill:#ef4444;}}
@keyframes pingring{0%{r:14;opacity:0.85;}100%{r:46;opacity:0;}}
@keyframes sweep{0%,100%{transform:rotate(-18deg);}50%{transform:rotate(18deg);}}
@keyframes bob{0%,100%{transform:translateY(0);}50%{transform:translateY(-6px);}}
@keyframes pupilWiggle{0%,100%{transform:translate(0,0);}25%{transform:translate(-2px,-1px);}50%{transform:translate(2px,1px);}75%{transform:translate(-1px,2px);}}
@keyframes blinkEye{0%,92%,100%{transform:scaleY(1);}95%{transform:scaleY(0.05);}}
@keyframes wagTail{0%,100%{transform:rotate(-12deg);}50%{transform:rotate(12deg);}}
@keyframes sparkle{0%,100%{opacity:0;transform:scale(0.5);}50%{opacity:1;transform:scale(1.2);}}
@keyframes hover{0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}

/* Sparkle particles */
.sparkle{position:absolute;font-size:24px;animation:sparkle 2s ease-in-out infinite;pointer-events:none;}

/* Picker cards */
.picker{max-width:1100px;margin:0 auto;}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;}
.card{display:block;text-decoration:none;padding:20px 22px;border-radius:22px;
  border:4px solid;color:#000;background:#fff;
  transition:transform 0.15s;
  box-shadow:0 6px 0 rgba(0,0,0,0.25),0 10px 24px rgba(0,0,0,0.15);}
.card:hover{transform:translateY(-3px);}
.card .emoji{font-size:3rem;line-height:1;margin-bottom:8px;}
.card h3{font-size:1.2rem;margin:6px 0 8px;font-weight:900;}
.card .vibe{font-size:0.9rem;line-height:1.45;}

/* Readouts */
.read-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;
  width:100%;max-width:780px;}
.rd{background:rgba(255,255,255,0.95);border:3px solid #000;border-radius:14px;padding:8px 10px;
  text-align:center;box-shadow:0 4px 0 rgba(0,0,0,0.25);}
.rd .h{font-size:11px;font-weight:900;letter-spacing:0.05em;}
.rd .v{font-size:14px;font-weight:900;font-family:'Courier New',monospace;color:#000;}
'''


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  ROBOT BASE SVG — symmetric, chunky, kid-friendly                     ║
# ╚══════════════════════════════════════════════════════════════════════╝
def robot_svg(theme):
    """theme = dict with: chassis_color, accent, motor_color, eye_pupil_color,
       face_pattern (list of 5x5 0/1), extra_top_html (e.g. costume hat),
       extra_decals_html (cape, stripes, etc.)"""
    chassis = theme.get('chassis_color', '#1a1f28')
    chassis2 = theme.get('chassis_color2', '#04060a')
    accent = theme.get('accent', '#fbbf24')
    motor_color = theme.get('motor_color', '#fbbf24')
    pupil_color = theme.get('pupil_color', '#000')
    matrix_color = theme.get('matrix_color', '#ef4444')
    deco_color = theme.get('deco_color', accent)

    # 5x5 face pattern — default smiley
    face = theme.get('face', [
        [0,1,0,1,0],
        [0,1,0,1,0],
        [0,0,0,0,0],
        [1,0,0,0,1],
        [0,1,1,1,0],
    ])

    matrix_cells = ''
    for r in range(5):
        for c in range(5):
            if face[r][c]:
                matrix_cells += f'<circle cx="{c*8}" cy="{r*8}" r="3" fill="{matrix_color}" opacity="0.9"><animate attributeName="opacity" values="0.5;1;0.5" dur="1.4s" repeatCount="indefinite" begin="{(r*5+c)*0.04}s"/></circle>'
            else:
                matrix_cells += f'<circle cx="{c*8}" cy="{r*8}" r="3" fill="#1a0500"/>'

    extra_top = theme.get('extra_top_html', '')
    extra_decals = theme.get('extra_decals_html', '')
    extra_under = theme.get('extra_under_html', '')

    return f'''
<svg viewBox="0 0 800 640" style="position:absolute;inset:0;width:100%;height:100%;z-index:2;" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="chassis_{accent[1:]}" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="{chassis}"/>
      <stop offset="100%" stop-color="{chassis2}"/>
    </linearGradient>
    <radialGradient id="rim_{accent[1:]}" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#fde68a"/>
      <stop offset="50%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="#a16207"/>
    </radialGradient>
    <radialGradient id="motor_{accent[1:]}" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#fff"/>
      <stop offset="50%" stop-color="{motor_color}"/>
      <stop offset="100%" stop-color="#7c5a32"/>
    </radialGradient>
    <filter id="puff" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2"/></filter>
  </defs>

  {extra_under}

  <!-- floor shadow -->
  <ellipse cx="400" cy="600" rx="280" ry="22" fill="#000" opacity="0.5"/>

  <!-- ╔ Chunky toy wheel — LEFT (symmetric) ╗ -->
  <g transform="translate(150, 460)" style="transform-origin:150px 460px;animation:bob 1.6s ease-in-out infinite;">
    <!-- speed lines -->
    <g opacity="0.5">
      <line x1="-95" y1="-20" x2="-65" y2="-20" stroke="{accent}" stroke-width="3" stroke-linecap="round"/>
      <line x1="-90" y1="0" x2="-60" y2="0" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
      <line x1="-95" y1="20" x2="-65" y2="20" stroke="{accent}" stroke-width="3" stroke-linecap="round"/>
    </g>
    <!-- tire (chunky black rounded) -->
    <circle r="80" fill="#0a0a0a" stroke="#000" stroke-width="3"/>
    <!-- tire treads -->
    ''' + ''.join(f'<rect x="-82" y="-4" width="14" height="8" fill="#1f2937" transform="rotate({a} 0 0) translate(70 0)"/>' for a in range(0, 360, 30)) + f'''
    <!-- yellow rim, spinning -->
    <g style="transform-origin:center;animation:spin 1.2s linear infinite;">
      <circle r="58" fill="url(#rim_{accent[1:]})" stroke="#000" stroke-width="3"/>
      <!-- 5-pointed star spokes -->
      <g stroke="#000" stroke-width="3" fill="none">
        ''' + ''.join(f'<line x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}"/>' for x, y in [(0,-50),(47.6,-15.5),(29.4,40.5),(-29.4,40.5),(-47.6,-15.5)]) + f'''
      </g>
      <!-- center hub -->
      <circle r="14" fill="#9ca3af" stroke="#000" stroke-width="2"/>
      <circle r="6" fill="#1f2937"/>
    </g>
    <!-- dust puff -->
    <circle cx="0" cy="80" r="10" fill="#fff" opacity="0.4" filter="url(#puff)"><animate attributeName="r" values="6;14;6" dur="0.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;0.1;0.6" dur="0.8s" repeatCount="indefinite"/></circle>
  </g>

  <!-- ╔ Chunky toy wheel — RIGHT (symmetric mirror of left) ╗ -->
  <g transform="translate(650, 460)" style="transform-origin:650px 460px;animation:bob 1.6s ease-in-out infinite;">
    <g opacity="0.5">
      <line x1="65" y1="-20" x2="95" y2="-20" stroke="{accent}" stroke-width="3" stroke-linecap="round"/>
      <line x1="60" y1="0" x2="90" y2="0" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
      <line x1="65" y1="20" x2="95" y2="20" stroke="{accent}" stroke-width="3" stroke-linecap="round"/>
    </g>
    <circle r="80" fill="#0a0a0a" stroke="#000" stroke-width="3"/>
    ''' + ''.join(f'<rect x="-82" y="-4" width="14" height="8" fill="#1f2937" transform="rotate({a} 0 0) translate(70 0)"/>' for a in range(0, 360, 30)) + f'''
    <g style="transform-origin:center;animation:spin 1.2s linear infinite;">
      <circle r="58" fill="url(#rim_{accent[1:]})" stroke="#000" stroke-width="3"/>
      <g stroke="#000" stroke-width="3" fill="none">
        ''' + ''.join(f'<line x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}"/>' for x, y in [(0,-50),(47.6,-15.5),(29.4,40.5),(-29.4,40.5),(-47.6,-15.5)]) + f'''
      </g>
      <circle r="14" fill="#9ca3af" stroke="#000" stroke-width="2"/>
      <circle r="6" fill="#1f2937"/>
    </g>
    <circle cx="0" cy="80" r="10" fill="#fff" opacity="0.4" filter="url(#puff)"><animate attributeName="r" values="6;14;6" dur="0.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;0.1;0.6" dur="0.8s" repeatCount="indefinite"/></circle>
  </g>

  <!-- ╔ Chassis — symmetric rounded body ╗ -->
  <g style="transform-origin:400px 460px;animation:bob 1.6s ease-in-out infinite;">
    <path d="M 230 400
             Q 230 340 290 320
             L 510 320
             Q 570 340 570 400
             L 570 480
             Q 570 510 540 510
             L 260 510
             Q 230 510 230 480
             Z"
          fill="url(#chassis_{accent[1:]})" stroke="#000" stroke-width="4"/>

    {extra_decals}

    <!-- Visible motor housings (yellow gearboxes peeking out sides) -->
    <g transform="translate(220, 450)">
      <rect x="-20" y="-22" width="44" height="44" rx="6" fill="url(#motor_{accent[1:]})" stroke="#000" stroke-width="3"/>
      <!-- gear window -->
      <circle cx="2" cy="0" r="14" fill="#1f2937" stroke="#000" stroke-width="2"/>
      <g style="transform-origin:2px 0;animation:spin 0.6s linear infinite;">
        ''' + ''.join(f'<rect x="-3" y="-13" width="6" height="6" fill="{motor_color}" transform="rotate({a} 2 0)"/>' for a in range(0, 360, 45)) + f'''
        <circle cx="2" cy="0" r="5" fill="#9ca3af"/>
      </g>
      <text y="36" text-anchor="middle" font-size="11" font-weight="900" fill="#000">MOTOR L</text>
    </g>
    <g transform="translate(580, 450)">
      <rect x="-24" y="-22" width="44" height="44" rx="6" fill="url(#motor_{accent[1:]})" stroke="#000" stroke-width="3"/>
      <circle cx="-2" cy="0" r="14" fill="#1f2937" stroke="#000" stroke-width="2"/>
      <g style="transform-origin:-2px 0;animation:spin 0.6s linear infinite;">
        ''' + ''.join(f'<rect x="-3" y="-13" width="6" height="6" fill="{motor_color}" transform="rotate({a} -2 0)"/>' for a in range(0, 360, 45)) + '''
        <circle cx="-2" cy="0" r="5" fill="#9ca3af"/>
      </g>
      <text y="36" text-anchor="middle" font-size="11" font-weight="900" fill="#000">MOTOR R</text>
    </g>

    <!-- 4 RGB LEDs — front edge, evenly spaced -->
    ''' + ''.join(f'''<g transform="translate({320+i*54}, 500)">
      <circle r="20" fill="#{c}" opacity="0.3"><animate attributeName="opacity" values="0.6;0.1;0.6" dur="1.2s" repeatCount="indefinite" begin="{i*0.3}s"/></circle>
      <circle r="11" fill="#{c}" stroke="#000" stroke-width="2.5" style="animation:blink 1.2s infinite {i*0.3}s;filter:drop-shadow(0 0 6px #{c});"/>
      <circle r="4" fill="#fff" opacity="0.7"/>
    </g>''' for i, c in enumerate(['ef4444','22c55e','3b82f6','fbbf24'])) + f'''

    <!-- Acrylic top deck with star -->
    <path d="M 280 320 L 520 320 L 540 360 L 260 360 Z" fill="rgba(229,231,235,0.55)" stroke="#000" stroke-width="3"/>
    <polygon points="400,330 405,346 422,346 408,355 413,371 400,361 387,371 392,355 378,346 395,346" fill="#000" opacity="0.7"/>
    <!-- battery -->
    <g transform="translate(450, 326)">
      <rect x="0" y="0" width="80" height="32" rx="4" fill="#dc2626" stroke="#000" stroke-width="3"/>
      <text x="40" y="14" text-anchor="middle" fill="#fff" font-size="9" font-family="Helvetica" font-weight="900">3.7V Li-Po</text>
      <text x="40" y="26" text-anchor="middle" fill="#fff" font-size="7" font-family="Helvetica">87% ⚡</text>
    </g>

    <!-- micro:bit with smiley face on matrix -->
    <g transform="translate(330, 380)">
      <rect x="0" y="0" width="120" height="100" rx="6" fill="#1a3a5a" stroke="#000" stroke-width="3"/>
      <rect x="0" y="98" width="120" height="8" fill="{accent}" stroke="#000" stroke-width="1"/>
      <text x="60" y="14" text-anchor="middle" fill="#fff" font-size="8" font-weight="900" font-family="Helvetica">micro:bit V2</text>
      <g transform="translate(40, 28)">{matrix_cells}</g>
      <circle cx="14" cy="58" r="8" fill="#000" stroke="#fff" stroke-width="2"/><text x="14" y="62" text-anchor="middle" fill="#fff" font-size="9" font-weight="900">A</text>
      <circle cx="106" cy="58" r="8" fill="#000" stroke="#fff" stroke-width="2"/><text x="106" y="62" text-anchor="middle" fill="#fff" font-size="9" font-weight="900">B</text>
    </g>

    <!-- caster wheel under chassis -->
    <circle cx="400" cy="495" r="11" fill="#fff" stroke="#000" stroke-width="2.5"/>
    <circle cx="400" cy="495" r="5" fill="#9ca3af"/>

    <!-- IR dome (with pink blush below as cheek) -->
    <ellipse cx="400" cy="488" rx="11" ry="6" fill="#0a0a0a" stroke="#000" stroke-width="2"/>
    <circle cx="400" cy="488" r="3" fill="#f472b6"><animate attributeName="opacity" values="1;0.3;1" dur="1.4s" repeatCount="indefinite"/></circle>

    <!-- buzzer with sound waves -->
    <g transform="translate(530, 460)">
      <circle r="10" fill="#0a0a0a" stroke="{accent}" stroke-width="2.5"/>
      <text y="3" text-anchor="middle" fill="{accent}" font-size="11" font-weight="900">♪</text>
      <path d="M 14 -5 Q 22 0 14 5" fill="none" stroke="{accent}" stroke-width="2"><animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></path>
      <path d="M 22 -8 Q 32 0 22 8" fill="none" stroke="{accent}" stroke-width="2"><animate attributeName="opacity" values="0;1;0" dur="1.2s" repeatCount="indefinite"/></path>
    </g>

    <!-- pink blush cheeks on chassis (kid-friendly!) -->
    <ellipse cx="270" cy="455" rx="14" ry="9" fill="#f472b6" opacity="0.65"/>
    <ellipse cx="530" cy="455" rx="14" ry="9" fill="#f472b6" opacity="0.65"/>

    <!-- line sensors under chassis (front-bottom) -->
    <rect x="385" y="510" width="10" height="6" fill="#22d3ee" stroke="#000" stroke-width="1"><animate attributeName="opacity" values="0.5;1;0.5" dur="1.2s" repeatCount="indefinite"/></rect>
    <rect x="405" y="510" width="10" height="6" fill="#22d3ee" stroke="#000" stroke-width="1"><animate attributeName="opacity" values="1;0.5;1" dur="1.2s" repeatCount="indefinite"/></rect>
  </g>

  <!-- ╔ Servo arm + ULTRASONIC HEAD with googly eyes ╗ -->
  <g style="transform-origin:400px 320px;animation:sweep 4s ease-in-out infinite;">
    <!-- arm -->
    <line x1="400" y1="320" x2="400" y2="200" stroke="#000" stroke-width="9"/>
    <line x1="400" y1="320" x2="400" y2="200" stroke="#9ca3af" stroke-width="5"/>
    <!-- servo body -->
    <rect x="380" y="240" width="40" height="50" rx="6" fill="{accent}" stroke="#000" stroke-width="3"/>
    <text x="400" y="270" text-anchor="middle" fill="#000" font-size="10" font-weight="900">SERVO</text>

    <!-- ULTRASONIC head -->
    <g transform="translate(290, 100)">
      <!-- body -->
      <rect x="0" y="0" width="220" height="100" rx="14" fill="#1f2937" stroke="#000" stroke-width="4"/>
      <!-- twin "eye" sensor cones -->
      <circle cx="60" cy="50" r="32" fill="#374151" stroke="#000" stroke-width="3"/>
      <circle cx="160" cy="50" r="32" fill="#374151" stroke="#000" stroke-width="3"/>
      <!-- speaker grill dots -->
      ''' + ''.join(f'<circle cx="{60+dx}" cy="{50+dy}" r="1.5" fill="#000"/>' for dx in [-14,-7,0,7,14] for dy in [-14,-7,0,7,14]) + ''.join(f'<circle cx="{160+dx}" cy="{50+dy}" r="1.5" fill="#000"/>' for dx in [-14,-7,0,7,14] for dy in [-14,-7,0,7,14]) + f'''
      <!-- ping rings -->
      <circle cx="110" cy="50" r="14" fill="none" stroke="#22d3ee" stroke-width="3" opacity="0.85"><animate attributeName="r" values="14;46;14" dur="1.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.85;0;0.85" dur="1.4s" repeatCount="indefinite"/></circle>
      <text x="110" y="92" text-anchor="middle" fill="{accent}" font-size="9" font-family="Helvetica" font-weight="900">DFROBOT</text>

      <!-- ╔ GOOGLY EYES on top — KID-FRIENDLY ╗ -->
      <g transform="translate(0, -38)" style="animation:bob 2.2s ease-in-out infinite;">
        <!-- left googly eye -->
        <circle cx="60" cy="20" r="26" fill="#fff" stroke="#000" stroke-width="4"/>
        <g style="transform-origin:60px 20px;animation:blinkEye 4s infinite;">
          <ellipse cx="60" cy="20" rx="22" ry="22" fill="#fff"/>
          <g style="animation:pupilWiggle 2.5s ease-in-out infinite;">
            <circle cx="60" cy="20" r="11" fill="{pupil_color}"/>
            <circle cx="63" cy="17" r="3" fill="#fff"/>
          </g>
        </g>
        <!-- right googly eye -->
        <circle cx="160" cy="20" r="26" fill="#fff" stroke="#000" stroke-width="4"/>
        <g style="transform-origin:160px 20px;animation:blinkEye 4s infinite;">
          <ellipse cx="160" cy="20" rx="22" ry="22" fill="#fff"/>
          <g style="animation:pupilWiggle 2.5s ease-in-out infinite 0.3s;">
            <circle cx="160" cy="20" r="11" fill="{pupil_color}"/>
            <circle cx="163" cy="17" r="3" fill="#fff"/>
          </g>
        </g>
        <!-- pink blush cheeks below eyes -->
        <ellipse cx="40" cy="44" rx="10" ry="6" fill="#f472b6" opacity="0.7"/>
        <ellipse cx="180" cy="44" rx="10" ry="6" fill="#f472b6" opacity="0.7"/>
      </g>

      {extra_top}
    </g>
  </g>
</svg>'''


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  Page assembly                                                         ║
# ╚══════════════════════════════════════════════════════════════════════╝
def base_html(title, body, extra_css=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{COMMON_CSS}{extra_css}</style>
</head>
<body>{body}</body>
</html>'''


def title_bar(idx, name, emoji, vibe, accent):
    prev_idx = (idx - 2) % 7 + 1
    next_idx = idx % 7 + 1
    return f'''<div class="title-bar">
  <div class="badge" style="color:{accent};">{emoji} #{idx} · {name}</div>
  <div class="vibe">{vibe}</div>
  <div class="nav">
    <a href="maqueen-kid.html" style="color:{accent};border-color:{accent};">⚙ All</a>
    <a href="maqueen-kid_{prev_idx}.html" style="color:{accent};border-color:{accent};">‹ Prev</a>
    <a href="maqueen-kid_{next_idx}.html" style="color:{accent};border-color:{accent};">Next ›</a>
    <a href="index.html" style="color:#7c5a32;border-color:#7c5a32;">🧪 Labs</a>
  </div>
</div>'''


def readouts_strip():
    return '''<div class="read-strip">
  <div class="rd"><div class="h" style="color:#fbbf24;">⟳ MOTOR L</div><div class="v">156 RPM</div></div>
  <div class="rd"><div class="h" style="color:#fbbf24;">⟳ MOTOR R</div><div class="v">158 RPM</div></div>
  <div class="rd"><div class="h" style="color:#22d3ee;">📡 ULTRA</div><div class="v">42 cm</div></div>
  <div class="rd"><div class="h" style="color:#22d3ee;">⤺ SERVO</div><div class="v">90°</div></div>
  <div class="rd"><div class="h" style="color:#f472b6;">◉ IR</div><div class="v">[ ▲ ]</div></div>
  <div class="rd"><div class="h" style="color:#22c55e;">▦ LINE</div><div class="v">L:0 R:0</div></div>
  <div class="rd"><div class="h" style="color:#22c55e;">⚡ BAT</div><div class="v">87%</div></div>
</div>'''


def page(idx, name, emoji, vibe, accent, scene_bg, scene_border, robot_theme,
         bubble_text, bubble_left='6%', bubble_top='4%',
         boom_text=None, boom_pos=None, sparkles=True):
    nav = title_bar(idx, name, emoji, vibe, accent)
    bubble = f'<div class="bubble" style="left:{bubble_left};top:{bubble_top};">{bubble_text}</div>'
    boom = ''
    if boom_text:
        b_left, b_top = boom_pos or ('70%', '12%')
        boom = f'<div class="boom" style="left:{b_left};top:{b_top};color:{accent};">{boom_text}</div>'
    sparkle_html = ''
    if sparkles:
        for i, (x, y, e, dly) in enumerate([
            ('8%','30%','✨','0s'),('92%','22%','✨','0.4s'),
            ('15%','82%','⭐','0.8s'),('85%','78%','⭐','1.2s'),
            ('50%','5%','✨','1.6s'),
        ]):
            sparkle_html += f'<div class="sparkle" style="left:{x};top:{y};animation-delay:{dly};color:{accent};">{e}</div>'
    body = nav + f'''
<div class="stage">
  <div class="scene" style="background:{scene_bg};border-color:{scene_border};">
    {bubble}
    {boom}
    {sparkle_html}
    {robot_svg(robot_theme)}
  </div>
  {readouts_strip()}
</div>'''
    return base_html(f'{emoji} #{idx} {name}', body)


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  7 mockups                                                             ║
# ╚══════════════════════════════════════════════════════════════════════╝

def make_1():
    return page(1, 'Classic Cartoon Pal', '🤖', 'primary colors · big smile · friendly',
        accent='#fbbf24',
        scene_bg='radial-gradient(ellipse at 50% 80%,#3b82f6 0%,#1e3a5a 100%)',
        scene_border='#fbbf24',
        bubble_text='Hi! I\'m Maqueen!',
        robot_theme={
            'accent':'#fbbf24',
            'pupil_color':'#1e40af',
            'face':[[0,1,0,1,0],[0,1,0,1,0],[0,0,0,0,0],[1,0,0,0,1],[0,1,1,1,0]],
        })


def make_2():
    cape = '''
    <!-- Superhero cape behind chassis -->
    <path d="M 230 320 Q 130 360 110 480 L 230 460 Z" fill="#dc2626" stroke="#000" stroke-width="3" opacity="0.95"><animate attributeName="d" values="M 230 320 Q 130 360 110 480 L 230 460 Z;M 230 320 Q 140 380 130 500 L 230 460 Z;M 230 320 Q 130 360 110 480 L 230 460 Z" dur="2s" repeatCount="indefinite"/></path>
    <path d="M 570 320 Q 670 360 690 480 L 570 460 Z" fill="#dc2626" stroke="#000" stroke-width="3" opacity="0.95"><animate attributeName="d" values="M 570 320 Q 670 360 690 480 L 570 460 Z;M 570 320 Q 660 380 670 500 L 570 460 Z;M 570 320 Q 670 360 690 480 L 570 460 Z" dur="2s" repeatCount="indefinite"/></path>
    <!-- M shield on chest -->
    <circle cx="400" cy="430" r="22" fill="#fbbf24" stroke="#000" stroke-width="3"/>
    <text x="400" y="438" text-anchor="middle" fill="#000" font-size="22" font-weight="900">M</text>'''
    mask = '''
    <!-- mask across googly eyes -->
    <path d="M 20 -28 L 200 -28 L 200 -10 L 130 -4 L 90 -4 L 20 -10 Z" fill="#1e3a5a" stroke="#000" stroke-width="3" opacity="0.9"/>'''
    return page(2, 'Superhero Robot', '🦸', 'cape · mask · POW! ZAP!',
        accent='#dc2626',
        scene_bg='radial-gradient(ellipse at 50% 50%,#fef3c7 0%,#fbbf24 60%,#dc2626 100%)',
        scene_border='#1e3a5a',
        bubble_text='To the rescue!',
        boom_text='POW!',
        boom_pos=('72%', '18%'),
        robot_theme={
            'accent':'#fbbf24',
            'pupil_color':'#1e3a5a',
            'face':[[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]],
            'extra_decals_html': cape,
            'extra_top_html': mask,
        })


def make_3():
    ears = '''
    <!-- Floppy dog ears on ultrasonic head -->
    <path d="M -20 -50 Q -40 -10 -20 30 L 20 30 L 20 -50 Z" fill="#8b4513" stroke="#000" stroke-width="3"/>
    <path d="M 240 -50 Q 260 -10 240 30 L 200 30 L 200 -50 Z" fill="#8b4513" stroke="#000" stroke-width="3"/>'''
    tail = '''
    <!-- Wagging tail behind chassis -->
    <g transform="translate(230, 410)" style="transform-origin:230px 410px;animation:wagTail 0.5s ease-in-out infinite;">
      <path d="M 0 0 Q -50 -10 -70 -40 L -55 -50 Q -40 -25 0 -10 Z" fill="#8b4513" stroke="#000" stroke-width="3"/>
    </g>'''
    return page(3, 'Puppy Pet', '🐕', 'floppy ears · wagging tail · Woof!',
        accent='#8b4513',
        scene_bg='radial-gradient(ellipse at 50% 70%,#fef3c7 0%,#86efac 60%,#22c55e 100%)',
        scene_border='#8b4513',
        bubble_text='Woof! Woof!',
        boom_text='♥',
        boom_pos=('75%', '14%'),
        robot_theme={
            'accent':'#8b4513',
            'pupil_color':'#000',
            'face':[[0,1,0,1,0],[1,1,0,1,1],[0,0,0,0,0],[0,1,1,1,0],[0,0,1,0,0]],
            'extra_top_html': ears,
            'extra_decals_html': tail,
        })


def make_4():
    helmet = '''
    <!-- Astronaut helmet bubble around eyes -->
    <ellipse cx="110" cy="0" rx="120" ry="60" fill="#22d3ee" fill-opacity="0.18" stroke="#22d3ee" stroke-width="4"/>
    <ellipse cx="110" cy="-10" rx="100" ry="30" fill="#fff" opacity="0.12"/>
    <!-- antenna on helmet -->
    <line x1="110" y1="-58" x2="110" y2="-90" stroke="#000" stroke-width="3"/>
    <circle cx="110" cy="-94" r="6" fill="#ef4444"><animate attributeName="opacity" values="1;0.3;1" dur="0.8s" repeatCount="indefinite"/></circle>'''
    planets = '''
    <!-- planets in background under everything -->
    <circle cx="100" cy="80" r="40" fill="#f472b6" opacity="0.6"/>
    <circle cx="100" cy="80" r="40" fill="none" stroke="#fff" stroke-width="1" opacity="0.3"/>
    <ellipse cx="100" cy="80" rx="56" ry="10" fill="none" stroke="#fff" stroke-width="2" opacity="0.5" transform="rotate(-15 100 80)"/>
    <circle cx="700" cy="120" r="22" fill="#fbbf24" opacity="0.7"/>'''
    return page(4, 'Astronaut Explorer', '👨‍🚀', 'space helmet · planets · stars',
        accent='#22d3ee',
        scene_bg='radial-gradient(ellipse at 50% 30%,#1e3a5a 0%,#0a0e14 80%)',
        scene_border='#22d3ee',
        bubble_text='Houston, ready!',
        boom_text='🚀',
        boom_pos=('78%', '10%'),
        robot_theme={
            'accent':'#22d3ee',
            'pupil_color':'#1e40af',
            'face':[[0,1,0,1,0],[1,0,1,0,1],[0,1,0,1,0],[1,0,1,0,1],[0,1,0,1,0]],
            'extra_top_html': helmet,
            'extra_under_html': planets,
        })


def make_5():
    helmet = '''
    <!-- Race helmet over eyes -->
    <path d="M -10 -55 Q -10 -10 110 -10 Q 230 -10 230 -55 L 220 -10 L 0 -10 Z" fill="#dc2626" stroke="#000" stroke-width="4"/>
    <rect x="20" y="-30" width="180" height="20" fill="#1e3a5a" stroke="#000" stroke-width="3"/>
    <!-- racing stripe on helmet -->
    <rect x="100" y="-55" width="20" height="45" fill="#fff" stroke="#000" stroke-width="2"/>'''
    flames = '''
    <!-- Flame decals on chassis sides -->
    <path d="M 250 380 Q 270 370 290 385 Q 280 395 270 400 Q 280 408 270 420 Q 250 415 240 405 Q 245 390 250 380 Z" fill="#fbbf24" stroke="#000" stroke-width="2"/>
    <path d="M 250 380 Q 268 372 288 384" fill="none" stroke="#dc2626" stroke-width="3"/>
    <path d="M 550 380 Q 530 370 510 385 Q 520 395 530 400 Q 520 408 530 420 Q 550 415 560 405 Q 555 390 550 380 Z" fill="#fbbf24" stroke="#000" stroke-width="2"/>
    <path d="M 550 380 Q 532 372 512 384" fill="none" stroke="#dc2626" stroke-width="3"/>
    <!-- Big "7" race number on chassis -->
    <circle cx="400" cy="450" r="22" fill="#fff" stroke="#000" stroke-width="3"/>
    <text x="400" y="460" text-anchor="middle" fill="#dc2626" font-size="26" font-weight="900">7</text>'''
    return page(5, 'Race Driver', '🏎️', 'helmet · flames · 3-2-1 GO!',
        accent='#dc2626',
        scene_bg='repeating-linear-gradient(90deg,#1f2937 0px,#1f2937 80px,#0a0a0a 80px,#0a0a0a 160px)',
        scene_border='#fbbf24',
        bubble_text='Vroom! Vroom!',
        boom_text='ZOOM!',
        boom_pos=('72%', '14%'),
        robot_theme={
            'accent':'#dc2626',
            'pupil_color':'#000',
            'face':[[1,0,0,0,1],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[0,1,1,1,0]],
            'extra_top_html': helmet,
            'extra_decals_html': flames,
        })


def make_6():
    hardhat = '''
    <!-- Hard hat over eyes -->
    <path d="M -20 -10 Q -20 -60 110 -60 Q 240 -60 240 -10 Z" fill="#fbbf24" stroke="#000" stroke-width="4"/>
    <rect x="-25" y="-15" width="270" height="10" fill="#fbbf24" stroke="#000" stroke-width="3"/>
    <rect x="100" y="-58" width="20" height="50" fill="#000" opacity="0.3"/>'''
    hazard = '''
    <!-- Hazard tape stripe across chassis bottom -->
    <rect x="240" y="495" width="320" height="14" fill="url(#hazardP)"/>
    <defs><pattern id="hazardP" x="0" y="0" width="40" height="14" patternUnits="userSpaceOnUse">
      <rect width="40" height="14" fill="#fbbf24"/>
      <polygon points="0,0 14,0 0,14" fill="#000"/>
      <polygon points="40,0 26,14 40,14" fill="#000"/>
    </pattern></defs>
    <!-- "WORK ZONE" sign on top deck -->
    <rect x="280" y="335" width="120" height="22" fill="#fbbf24" stroke="#000" stroke-width="3"/>
    <text x="340" y="350" text-anchor="middle" fill="#000" font-size="11" font-weight="900">WORK ZONE</text>'''
    return page(6, 'Construction Worker', '👷', 'hard hat · hazard tape · BEEP BEEP!',
        accent='#fbbf24',
        scene_bg='repeating-linear-gradient(45deg,#fbbf24 0px,#fbbf24 30px,#000 30px,#000 60px)',
        scene_border='#000',
        bubble_text='BEEP BEEP! Working!',
        boom_text='🔧',
        boom_pos=('72%', '14%'),
        sparkles=False,
        robot_theme={
            'accent':'#fbbf24',
            'pupil_color':'#000',
            'face':[[0,1,1,1,0],[1,0,0,0,1],[1,1,1,1,1],[0,0,0,0,0],[0,1,1,1,0]],
            'extra_top_html': hardhat,
            'extra_decals_html': hazard,
        })


def make_7():
    hat = '''
    <!-- Pointed wizard hat -->
    <path d="M 110 -100 L 30 -20 L 190 -20 Z" fill="#7c3aed" stroke="#000" stroke-width="4"/>
    <!-- stars on hat -->
    <text x="110" y="-50" text-anchor="middle" fill="#fbbf24" font-size="20" font-weight="900">⭐</text>
    <text x="80" y="-30" text-anchor="middle" fill="#fff" font-size="12">✨</text>
    <text x="140" y="-30" text-anchor="middle" fill="#fff" font-size="12">✨</text>
    <!-- hat brim -->
    <ellipse cx="110" cy="-18" rx="92" ry="7" fill="#5b21b6" stroke="#000" stroke-width="3"/>'''
    beard = '''
    <!-- Magic glow around chassis -->
    <circle cx="400" cy="430" r="180" fill="none" stroke="#a78bfa" stroke-width="2" stroke-dasharray="4 6" opacity="0.6"><animate attributeName="r" values="160;200;160" dur="3s" repeatCount="indefinite"/></circle>
    <!-- magic stars floating -->
    <text x="280" y="370" fill="#fbbf24" font-size="18">✨</text>
    <text x="510" y="375" fill="#fbbf24" font-size="18">✨</text>'''
    return page(7, 'Wizard', '🧙', 'pointy hat · sparkles · Abracadabra!',
        accent='#7c3aed',
        scene_bg='radial-gradient(ellipse at 50% 60%,#1e1b4b 0%,#0a0414 100%)',
        scene_border='#fbbf24',
        bubble_text='Abracadabra! ✨',
        boom_text='✨',
        boom_pos=('20%', '20%'),
        robot_theme={
            'accent':'#a78bfa',
            'pupil_color':'#7c3aed',
            'face':[[1,0,0,0,1],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,1,1,1,0]],
            'extra_top_html': hat,
            'extra_decals_html': beard,
        })


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  Picker                                                                ║
# ╚══════════════════════════════════════════════════════════════════════╝
def make_picker():
    extra_css = '''
.picker-body{background:radial-gradient(ellipse at 50% 50%,#1e3a5a 0%,#0a0e14 100%);}
h1{text-align:center;color:#fbbf24;font-size:2rem;margin:18px 0 6px;text-shadow:3px 3px 0 #000;}
.intro{text-align:center;color:#fff;font-size:14px;margin-bottom:18px;}
.nav-back{text-align:center;margin:12px 0 24px;}
.nav-back a{color:#fbbf24;text-decoration:none;border:2px solid #fbbf24;border-radius:999px;
  padding:5px 14px;font-weight:800;font-size:13px;margin:0 4px;}
'''
    body = '<div class="picker">'
    body += '<h1>🤖 Maqueen Kids — pick your buddy!</h1>'
    body += '<div class="intro">Same robot, 7 personalities. Tap a card!</div>'
    body += '<div class="nav-back"><a href="index.html">🧪 All Labs</a><a href="maqueen-emu.html">📐 Original Emu</a></div>'
    body += '<div class="cards">'
    cards = [
        (1, '🤖', 'Classic Cartoon Pal', 'big smile · friendly waves', '#fbbf24', '#1e3a5a'),
        (2, '🦸', 'Superhero Robot', 'cape · mask · POW! ZAP!', '#dc2626', '#fbbf24'),
        (3, '🐕', 'Puppy Pet', 'floppy ears · wagging tail', '#8b4513', '#86efac'),
        (4, '👨‍🚀', 'Astronaut Explorer', 'space helmet · planets', '#22d3ee', '#1e3a5a'),
        (5, '🏎️', 'Race Driver', 'helmet · flames · #7', '#dc2626', '#fbbf24'),
        (6, '👷', 'Construction Worker', 'hard hat · hazard tape', '#fbbf24', '#000'),
        (7, '🧙', 'Wizard', 'pointy hat · sparkles · magic', '#7c3aed', '#fbbf24'),
    ]
    for i, e, n, v, c1, c2 in cards:
        body += f'''<a class="card" href="maqueen-kid_{i}.html" style="border-color:{c1};background:linear-gradient(180deg,#fff,{c2}22);">
  <div class="emoji">{e}</div>
  <h3 style="color:{c1};">#{i} · {n}</h3>
  <div class="vibe">{v}</div>
</a>'''
    body += '</div></div>'
    return base_html('🤖 Maqueen Kids — pick your buddy', body, extra_css)


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  GENERATE                                                              ║
# ╚══════════════════════════════════════════════════════════════════════╝
files = [
    ('maqueen-kid.html',   make_picker, 'Picker'),
    ('maqueen-kid_1.html', make_1,      'Classic Cartoon Pal'),
    ('maqueen-kid_2.html', make_2,      'Superhero Robot'),
    ('maqueen-kid_3.html', make_3,      'Puppy Pet'),
    ('maqueen-kid_4.html', make_4,      'Astronaut Explorer'),
    ('maqueen-kid_5.html', make_5,      'Race Driver'),
    ('maqueen-kid_6.html', make_6,      'Construction Worker'),
    ('maqueen-kid_7.html', make_7,      'Wizard'),
]
for fname, fn, label in files:
    out = os.path.join(OUT, fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(fn())
    print(f'  + {fname}  ({label})')
print('Done.')
