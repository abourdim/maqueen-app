#!/usr/bin/env python3
"""Cockpit Lab v4 — anatomical vehicle cutaways with sci-fi ambiance.

Each mockup = recognizable vehicle silhouette (SVG) with all Maqueen
hardware drawn IN PLACE on the actual body parts: motors at engines,
LEDs at nav lights, line sensors at the bumper, etc. Holographic
callouts connect each body part to a glowing readout panel.

Background: starfield, neon outline, scanner sweep, HUD corner brackets.

Static design only. Re-runnable. Old v1/v2/v3 untouched.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'labs')

# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Shared sci-fi ambiance helpers                                     ║
# ╚═════════════════════════════════════════════════════════════════════╝

GLOBAL_CSS = '''
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:#02040a;color:#dff;font-family:'JetBrains Mono',monospace;min-height:100vh;overflow-x:hidden;}
body{padding:8px 10px 24px;position:relative;}

/* ─── starfield ─── */
.stars,.stars2,.stars3{position:fixed;inset:0;pointer-events:none;z-index:0;}
.stars{background-image:radial-gradient(1px 1px at 12% 18%,#fff 50%,transparent 50%),
                       radial-gradient(1px 1px at 38% 72%,#fff 50%,transparent 50%),
                       radial-gradient(1.4px 1.4px at 64% 22%,#dff 50%,transparent 50%),
                       radial-gradient(1px 1px at 84% 51%,#fff 50%,transparent 50%),
                       radial-gradient(1px 1px at 22% 88%,#dff 50%,transparent 50%),
                       radial-gradient(1.6px 1.6px at 50% 35%,#fff 50%,transparent 50%),
                       radial-gradient(1px 1px at 75% 80%,#fff 50%,transparent 50%);
       background-size:100% 100%;opacity:0.85;animation:twinkle 4s ease-in-out infinite;}
.stars2{background-image:radial-gradient(1px 1px at 8% 55%,#aff 50%,transparent 50%),
                        radial-gradient(1px 1px at 30% 30%,#fff 50%,transparent 50%),
                        radial-gradient(2px 2px at 56% 78%,#fff 50%,transparent 50%),
                        radial-gradient(1px 1px at 90% 12%,#dff 50%,transparent 50%),
                        radial-gradient(1px 1px at 46% 60%,#fff 50%,transparent 50%);
        opacity:0.55;animation:twinkle 6s ease-in-out infinite alternate;}
.stars3{background-image:radial-gradient(1px 1px at 18% 38%,#a5f3fc 50%,transparent 50%),
                        radial-gradient(1px 1px at 72% 65%,#f0abfc 50%,transparent 50%),
                        radial-gradient(1.5px 1.5px at 42% 12%,#fde68a 50%,transparent 50%);
        opacity:0.75;animation:twinkle 8s ease-in-out infinite;}
@keyframes twinkle{0%,100%{opacity:0.4;}50%{opacity:0.95;}}

/* ─── HUD corner brackets ─── */
.hud-frame{position:fixed;inset:6px;pointer-events:none;z-index:1;}
.hud-frame .b{position:absolute;width:32px;height:32px;border:2px solid #22d3ee;filter:drop-shadow(0 0 4px #22d3ee);}
.hud-frame .tl{top:0;left:0;border-right:none;border-bottom:none;}
.hud-frame .tr{top:0;right:0;border-left:none;border-bottom:none;}
.hud-frame .bl{bottom:0;left:0;border-right:none;border-top:none;}
.hud-frame .br{bottom:0;right:0;border-left:none;border-top:none;}
.hud-frame .tick-h{position:absolute;top:50%;left:0;right:0;border-top:1px dashed rgba(34,211,238,0.18);}
.hud-frame .tick-v{position:absolute;left:50%;top:0;bottom:0;border-left:1px dashed rgba(34,211,238,0.18);}

/* ─── scanner sweep ─── */
.scanner{position:fixed;top:0;bottom:0;left:-30%;width:30%;
  background:linear-gradient(90deg,transparent 0%,rgba(34,211,238,0.06) 50%,transparent 100%);
  pointer-events:none;z-index:2;animation:scan 8s linear infinite;}
@keyframes scan{from{left:-30%;}to{left:100%;}}

/* ─── stage where vehicle lives ─── */
.stage{position:relative;z-index:3;max-width:1500px;margin:0 auto;padding:14px;}
.title{display:flex;align-items:center;gap:14px;padding:8px 14px;background:rgba(2,6,16,0.72);border:1px solid #1e3a5a;border-radius:8px;margin-bottom:14px;backdrop-filter:blur(6px);}
.title .badge{font-size:13px;font-weight:800;color:#22d3ee;letter-spacing:0.08em;text-shadow:0 0 6px #22d3ee;}
.title .vibe{font-size:10px;color:#7fa;opacity:0.75;}
.title .nav{margin-left:auto;display:flex;gap:6px;}
.title .nav a{color:#aff;text-decoration:none;border:1px solid #1e3a5a;border-radius:5px;padding:3px 9px;font-size:11px;}
.title .nav a:hover{border-color:#22d3ee;color:#22d3ee;}

/* ─── animations ─── */
@keyframes pulse{0%,100%{opacity:0.4;transform:scale(1);}50%{opacity:1;transform:scale(1.4);}}
@keyframes pulsefast{0%,100%{opacity:0.5;transform:scale(0.9);}50%{opacity:1;transform:scale(1.3);}}
@keyframes flicker{0%,100%{opacity:1;}48%{opacity:0.85;}52%{opacity:1;}}
@keyframes blink{0%,55%{opacity:1;}56%,100%{opacity:0.18;}}
@keyframes spin{to{transform:rotate(360deg);}}
@keyframes wiggle{0%,100%{transform:rotate(-12deg);}50%{transform:rotate(12deg);}}
@keyframes propspin{to{transform:rotate(360deg);}}

/* ─── callout panels ─── */
.callout{position:absolute;background:linear-gradient(180deg,rgba(2,18,30,0.92),rgba(2,8,16,0.92));
  border:1px solid #22d3ee;border-radius:6px;padding:6px 9px;
  box-shadow:0 0 14px rgba(34,211,238,0.35),inset 0 0 8px rgba(34,211,238,0.08);
  font-family:'JetBrains Mono',monospace;font-size:10px;color:#dff;
  backdrop-filter:blur(4px);min-width:90px;}
.callout.amber{border-color:#fbbf24;box-shadow:0 0 14px rgba(251,191,36,0.35),inset 0 0 8px rgba(251,191,36,0.08);}
.callout.magenta{border-color:#f472b6;box-shadow:0 0 14px rgba(244,114,182,0.35),inset 0 0 8px rgba(244,114,182,0.08);}
.callout.green{border-color:#22c55e;box-shadow:0 0 14px rgba(34,197,94,0.35),inset 0 0 8px rgba(34,197,94,0.08);}
.callout.violet{border-color:#a78bfa;box-shadow:0 0 14px rgba(167,139,250,0.35),inset 0 0 8px rgba(167,139,250,0.08);}
.callout .h{font-size:8px;letter-spacing:0.16em;text-transform:uppercase;color:#22d3ee;font-weight:800;margin-bottom:3px;display:flex;align-items:center;gap:5px;}
.callout.amber .h{color:#fbbf24;}
.callout.magenta .h{color:#f472b6;}
.callout.green .h{color:#22c55e;}
.callout.violet .h{color:#a78bfa;}
.callout .v{font-size:14px;font-weight:800;color:#fff;text-shadow:0 0 4px currentColor;}
.callout .h::before{content:'';width:6px;height:6px;border-radius:50%;background:currentColor;box-shadow:0 0 6px currentColor;animation:flicker 2s infinite;}

/* ─── pulse dot anchored on a body part ─── */
.dot{position:absolute;width:14px;height:14px;border-radius:50%;background:#22d3ee;
  box-shadow:0 0 12px #22d3ee,0 0 24px #22d3ee;transform:translate(-50%,-50%);
  animation:pulse 1.6s ease-in-out infinite;}
.dot.amber{background:#fbbf24;box-shadow:0 0 12px #fbbf24,0 0 24px #fbbf24;}
.dot.magenta{background:#f472b6;box-shadow:0 0 12px #f472b6,0 0 24px #f472b6;}
.dot.green{background:#22c55e;box-shadow:0 0 12px #22c55e,0 0 24px #22c55e;}
.dot.violet{background:#a78bfa;box-shadow:0 0 12px #a78bfa,0 0 24px #a78bfa;}
'''


def base_html(title, body, extra_css=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{GLOBAL_CSS}{extra_css}</style>
</head>
<body>
<div class="stars"></div>
<div class="stars2"></div>
<div class="stars3"></div>
<div class="hud-frame"><div class="b tl"></div><div class="b tr"></div><div class="b bl"></div><div class="b br"></div><div class="tick-h"></div><div class="tick-v"></div></div>
<div class="scanner"></div>
{body}
</body>
</html>'''


def title_bar(idx, name, emoji, vibe):
    prev_idx = (idx - 2) % 10 + 1
    next_idx = idx % 10 + 1
    return f'''<div class="title">
  <div class="badge">{emoji} v4 #{idx} · {name}</div>
  <div class="vibe">{vibe}</div>
  <div class="nav">
    <a href="cockpit-lab_v4.html">⚙ Gallery</a>
    <a href="cockpit-lab_v4_{prev_idx}.html">‹ Prev</a>
    <a href="cockpit-lab_v4_{next_idx}.html">Next ›</a>
  </div>
</div>'''


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  #1 — PLANE TOP-DOWN (twin-engine airliner cutaway)                 ║
# ╚═════════════════════════════════════════════════════════════════════╝
def make_1():
    nav = title_bar(1, 'Plane · Top-Down Cutaway', '✈', 'twin engine · nav lights · cockpit cluster')

    # SVG plane silhouette in 1500x900 stage. Top-down, nose up.
    # Anchors are SVG coords; callouts placed via percentages around them.
    plane_svg = '''
<svg viewBox="0 0 1500 900" style="position:absolute;inset:0;width:100%;height:100%;z-index:1;" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="hull" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.04"/>
      <stop offset="50%" stop-color="#22d3ee" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0.04"/>
    </linearGradient>
    <radialGradient id="cockpit" cx="50%" cy="20%" r="50%">
      <stop offset="0%" stop-color="#fff" stop-opacity="0.35"/>
      <stop offset="60%" stop-color="#22d3ee" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="3"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>

  <!-- FUSELAGE (long oval) -->
  <ellipse cx="750" cy="450" rx="80" ry="370" fill="url(#hull)" stroke="#22d3ee" stroke-width="2.2" filter="url(#glow)"/>

  <!-- WINGS (swept-back) -->
  <path d="M 670 470  L 220 580  L 250 620  L 690 540  Z" fill="url(#hull)" stroke="#22d3ee" stroke-width="2" filter="url(#glow)"/>
  <path d="M 830 470  L 1280 580  L 1250 620  L 810 540  Z" fill="url(#hull)" stroke="#22d3ee" stroke-width="2" filter="url(#glow)"/>

  <!-- TAIL HORIZONTAL stab -->
  <path d="M 700 760  L 560 800  L 580 820  L 720 790  Z" fill="url(#hull)" stroke="#22d3ee" stroke-width="2" filter="url(#glow)"/>
  <path d="M 800 760  L 940 800  L 920 820  L 780 790  Z" fill="url(#hull)" stroke="#22d3ee" stroke-width="2" filter="url(#glow)"/>

  <!-- VERTICAL FIN (drawn as small triangle at tail) -->
  <path d="M 740 730  L 760 730  L 760 700  L 740 700 Z" fill="url(#hull)" stroke="#22d3ee" stroke-width="1.5"/>

  <!-- COCKPIT WINDOW (nose) -->
  <ellipse cx="750" cy="120" rx="42" ry="55" fill="url(#cockpit)" stroke="#22d3ee" stroke-width="1.6"/>
  <line x1="710" y1="140" x2="790" y2="140" stroke="#22d3ee" stroke-width="0.8" opacity="0.6"/>

  <!-- ENGINES (oval pods under wings) -->
  <ellipse cx="430" cy="600" rx="36" ry="62" fill="rgba(0,0,0,0.6)" stroke="#fbbf24" stroke-width="2" filter="url(#glow)"/>
  <circle cx="430" cy="568" r="12" fill="none" stroke="#fbbf24" stroke-width="1.2"/>
  <circle cx="430" cy="568" r="4" fill="#fbbf24"/>
  <ellipse cx="1070" cy="600" rx="36" ry="62" fill="rgba(0,0,0,0.6)" stroke="#fbbf24" stroke-width="2" filter="url(#glow)"/>
  <circle cx="1070" cy="568" r="12" fill="none" stroke="#fbbf24" stroke-width="1.2"/>
  <circle cx="1070" cy="568" r="4" fill="#fbbf24"/>

  <!-- WINGTIP NAV LIGHTS -->
  <circle cx="225" cy="595" r="9" fill="#ef4444" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="1275" cy="595" r="9" fill="#22c55e" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>

  <!-- TAIL LIGHTS -->
  <circle cx="565" cy="803" r="6" fill="#fff" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0.3;1" dur="0.9s" repeatCount="indefinite"/>
  </circle>
  <circle cx="935" cy="803" r="6" fill="#fff" filter="url(#glow)">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="0.9s" repeatCount="indefinite"/>
  </circle>

  <!-- CENTERLINE (cockpit-to-tail dashed) -->
  <line x1="750" y1="180" x2="750" y2="700" stroke="#22d3ee" stroke-width="0.5" stroke-dasharray="4 6" opacity="0.35"/>

  <!-- CALLOUT LINES (thin lines from body parts to callout boxes) -->
  <!-- left engine to callout -->
  <line x1="394" y1="600" x2="170" y2="660" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <!-- right engine -->
  <line x1="1106" y1="600" x2="1330" y2="660" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <!-- left wingtip -->
  <line x1="225" y1="595" x2="100" y2="510" stroke="#ef4444" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <!-- right wingtip -->
  <line x1="1275" y1="595" x2="1400" y2="510" stroke="#22c55e" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <!-- nose / cockpit cluster -->
  <line x1="750" y1="65" x2="350" y2="100" stroke="#22d3ee" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="750" y1="65" x2="1150" y2="100" stroke="#22d3ee" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="708" y1="120" x2="500" y2="220" stroke="#a78bfa" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="792" y1="120" x2="1000" y2="220" stroke="#a78bfa" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <!-- fuselage mid (battery) -->
  <line x1="690" y1="400" x2="170" y2="380" stroke="#22c55e" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <!-- belly line sensors (just under nose) -->
  <line x1="750" y1="200" x2="750" y2="290" stroke="#22d3ee" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="750" y1="290" x2="1330" y2="320" stroke="#22d3ee" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <!-- tail / matrix -->
  <line x1="750" y1="730" x2="1330" y2="780" stroke="#f472b6" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <!-- mid fuselage IR antenna (top) -->
  <line x1="750" y1="380" x2="170" y2="240" stroke="#f472b6" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <!-- buzzer in cockpit -->
  <line x1="745" y1="160" x2="170" y2="100" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>

  <!-- BELLY LINE SENSORS (drawn under nose: 2 small squares) -->
  <rect x="730" y="195" width="10" height="10" fill="#22d3ee" stroke="#0ff" stroke-width="0.5" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0.5;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>
  <rect x="760" y="195" width="10" height="10" fill="#22d3ee" stroke="#0ff" stroke-width="0.5" filter="url(#glow)">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="1.2s" repeatCount="indefinite"/>
  </rect>

  <!-- IR ANTENNA on top of fuselage -->
  <line x1="750" y1="370" x2="750" y2="350" stroke="#f472b6" stroke-width="2"/>
  <circle cx="750" cy="345" r="4" fill="#f472b6" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0.3;1" dur="0.8s" repeatCount="indefinite"/>
  </circle>

  <!-- TAIL MATRIX panel (small grid) -->
  <rect x="735" y="710" width="30" height="22" fill="#1a0a14" stroke="#f472b6" stroke-width="1"/>
</svg>'''

    # Animated propeller overlays (HTML divs over SVG engines, so we can use CSS spin)
    props = '''
<div style="position:absolute;left:28.7%;top:62%;width:60px;height:60px;transform:translate(-50%,-50%);z-index:2;">
  <div style="width:100%;height:100%;border-radius:50%;background:conic-gradient(rgba(251,191,36,0.7) 0 8%,transparent 8% 50%,rgba(251,191,36,0.7) 50% 58%,transparent 58% 100%);animation:propspin 0.18s linear infinite;opacity:0.7;"></div>
</div>
<div style="position:absolute;left:71.3%;top:62%;width:60px;height:60px;transform:translate(-50%,-50%);z-index:2;">
  <div style="width:100%;height:100%;border-radius:50%;background:conic-gradient(rgba(251,191,36,0.7) 0 8%,transparent 8% 50%,rgba(251,191,36,0.7) 50% 58%,transparent 58% 100%);animation:propspin 0.18s linear infinite reverse;opacity:0.7;"></div>
</div>'''

    # Callout boxes anchored by absolute % of stage
    # Stage uses position:relative, height calc to mirror SVG aspect (1500x900 ≈ 1.66:1)
    callouts = '''
<!-- LEFT WINGTIP NAV LIGHT -->
<div class="callout magenta" style="left:1%;top:52%;width:130px;">
  <div class="h">◐ NAV·LIGHT·L · LED 1</div>
  <div style="display:flex;align-items:center;gap:6px;"><div style="width:14px;height:14px;border-radius:50%;background:#ef4444;box-shadow:0 0 12px #ef4444;animation:blink 1.5s infinite;"></div><div class="v" style="color:#ef4444;">RED</div></div>
</div>

<!-- RIGHT WINGTIP NAV LIGHT -->
<div class="callout green" style="right:1%;top:52%;width:130px;">
  <div class="h">◐ NAV·LIGHT·R · LED 2</div>
  <div style="display:flex;align-items:center;gap:6px;"><div style="width:14px;height:14px;border-radius:50%;background:#22c55e;box-shadow:0 0 12px #22c55e;animation:blink 1.5s infinite 0.3s;"></div><div class="v" style="color:#22c55e;">GREEN</div></div>
</div>

<!-- LEFT ENGINE = MOTOR L -->
<div class="callout amber" style="left:1%;top:70%;width:140px;">
  <div class="h">⊕ ENGINE·L · MOTOR L</div>
  <div class="v">182 <span style="font-size:9px;color:#bba;">RPM·u</span></div>
  <div style="height:5px;background:#1a1408;border-radius:2px;margin-top:4px;overflow:hidden;"><div style="width:72%;height:100%;background:linear-gradient(90deg,#fbbf24,#fff);box-shadow:0 0 6px #fbbf24;"></div></div>
  <div style="font-size:8px;color:#bba;margin-top:3px;">FWD · 72%</div>
</div>

<!-- RIGHT ENGINE = MOTOR R -->
<div class="callout amber" style="right:1%;top:70%;width:140px;">
  <div class="h">⊕ ENGINE·R · MOTOR R</div>
  <div class="v">175 <span style="font-size:9px;color:#bba;">RPM·u</span></div>
  <div style="height:5px;background:#1a1408;border-radius:2px;margin-top:4px;overflow:hidden;"><div style="width:68%;height:100%;background:linear-gradient(90deg,#fbbf24,#fff);box-shadow:0 0 6px #fbbf24;"></div></div>
  <div style="font-size:8px;color:#bba;margin-top:3px;">FWD · 68%</div>
</div>

<!-- COCKPIT — speed/altitude on left of nose -->
<div class="callout" style="left:14%;top:8%;width:130px;">
  <div class="h">► AIRSPEED · MIC</div>
  <div class="v" style="color:#22d3ee;">42 <span style="font-size:9px;color:#bba;">km/h</span></div>
  <div style="display:flex;gap:1px;height:14px;margin-top:4px;background:#000;padding:1px;">''' + ''.join(f'<div style="flex:1;background:linear-gradient(180deg,#22d3ee,#000);height:{30+(i*13)%65}%;align-self:flex-end;"></div>' for i in range(20)) + '''</div>
</div>

<!-- COCKPIT — heading/compass on right of nose -->
<div class="callout" style="right:14%;top:8%;width:130px;">
  <div class="h">⊙ HEADING · COMPASS</div>
  <div class="v" style="color:#22d3ee;">072° <span style="font-size:9px;color:#bba;">N</span></div>
  <div style="text-align:center;margin-top:4px;"><svg width="60" height="60" viewBox="0 0 60 60"><circle cx="30" cy="30" r="26" fill="none" stroke="#1e3a5a" stroke-width="1"/>''' + ''.join(f'<line x1="30" y1="6" x2="30" y2="{10 if i%3==0 else 8}" stroke="#22d3ee" stroke-width="0.5" transform="rotate({i*30} 30 30)"/>' for i in range(12)) + '''<text x="30" y="14" text-anchor="middle" fill="#22d3ee" font-size="6">N</text><line x1="30" y1="30" x2="30" y2="10" stroke="#fbbf24" stroke-width="2" transform="rotate(72 30 30)" style="filter:drop-shadow(0 0 2px #fbbf24);"/></svg></div>
</div>

<!-- COCKPIT WINDOW left = ATTITUDE/ACCEL -->
<div class="callout violet" style="left:30%;top:22%;width:130px;">
  <div class="h">⌘ ATTITUDE · ACCEL</div>
  <div style="position:relative;width:90px;height:50px;margin:0 auto;background:linear-gradient(180deg,#3b82f6 50%,#92400e 50%);border:1px solid #1e3a5a;border-radius:3px;overflow:hidden;"><div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);"><svg width="50" height="14"><line x1="0" y1="7" x2="18" y2="7" stroke="#fbbf24" stroke-width="2"/><line x1="32" y1="7" x2="50" y2="7" stroke="#fbbf24" stroke-width="2"/><circle cx="25" cy="7" r="2.5" fill="#fbbf24"/></svg></div></div>
  <div style="font-size:8px;color:#a78bfa;margin-top:3px;text-align:center;">X+0.12 Y−0.04 Z+0.98</div>
</div>

<!-- COCKPIT WINDOW right = TEMPERATURE -->
<div class="callout violet" style="right:30%;top:22%;width:130px;">
  <div class="h">℃ CABIN TEMP</div>
  <div class="v" style="color:#a78bfa;">22.4 <span style="font-size:9px;color:#bba;">°C</span></div>
  <div style="display:flex;align-items:center;gap:5px;margin-top:4px;">
    <div style="width:8px;height:36px;background:linear-gradient(180deg,#ef4444,#fbbf24,#22d3ee);border:1px solid #444;border-radius:4px;position:relative;"><div style="position:absolute;left:-3px;right:-3px;bottom:55%;height:3px;background:#fff;box-shadow:0 0 4px #fff;"></div></div>
    <div style="font-size:8px;color:#a78bfa;font-family:monospace;">▸ NOMINAL<br>▸ HVAC OK</div>
  </div>
</div>

<!-- BUZZER in cockpit (left side, very top) -->
<div class="callout amber" style="left:1%;top:8%;width:130px;">
  <div class="h">♪ BUZZER · TONE</div>
  <div class="v" style="color:#fbbf24;">A4 <span style="font-size:9px;color:#bba;">440 Hz</span></div>
  <div style="display:flex;gap:1px;height:18px;margin-top:4px;background:#000;padding:1px;">''' + ''.join(f'<div style="flex:1;background:linear-gradient(180deg,#fbbf24,#000);height:{30+(i*17)%70}%;align-self:flex-end;animation:flicker {1.0+(i%5)*0.2}s ease-in-out infinite;animation-delay:{i*0.05}s;"></div>' for i in range(18)) + '''</div>
</div>

<!-- IR antenna callout (top mid, also left) -->
<div class="callout magenta" style="left:1%;top:24%;width:130px;">
  <div class="h">◉ IR ANTENNA · 38kHz</div>
  <div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;border-radius:50%;background:radial-gradient(circle,#fff,#f472b6 60%);box-shadow:0 0 8px #f472b6;animation:pulsefast 1.4s infinite;"></div><div class="v" style="color:#f472b6;font-size:13px;">[ OK ]</div></div>
  <div style="font-size:8px;color:#bba;margin-top:3px;">▸ Last key 1.2s ago</div>
</div>

<!-- BATTERY (mid fuselage) -->
<div class="callout green" style="left:1%;top:38%;width:130px;">
  <div class="h">⚡ BATTERY · LiPo</div>
  <div class="v" style="color:#22c55e;">87% <span style="font-size:9px;color:#bba;">3.78V</span></div>
  <div style="height:8px;background:#000;border:1px solid #14532d;display:flex;gap:1px;padding:1px;margin-top:4px;">''' + ''.join(f'<div style="flex:1;background:{"linear-gradient(180deg,#22c55e,#16a34a)" if i<8 else "#0a1808"};box-shadow:{"0 0 3px #22c55e" if i<8 else "none"};"></div>' for i in range(10)) + '''</div>
  <div style="font-size:8px;color:#bba;margin-top:3px;">▸ ~42 min remain</div>
</div>

<!-- LINE SENSORS (under nose, callout on right) -->
<div class="callout" style="right:1%;top:31%;width:140px;">
  <div class="h">▦ LINE-CAM · L/R</div>
  <div style="display:flex;gap:4px;height:30px;margin-top:3px;">
    <div style="flex:1;background:#fff;border:1px solid #444;position:relative;"><div style="position:absolute;top:0;left:35%;width:8px;height:100%;background:#000;"></div><div style="position:absolute;bottom:0;left:1px;font-size:7px;color:#22c55e;font-weight:800;">L:0</div></div>
    <div style="flex:1;background:#fff;border:1px solid #444;position:relative;"><div style="position:absolute;top:0;left:55%;width:8px;height:100%;background:#000;"></div><div style="position:absolute;bottom:0;left:1px;font-size:7px;color:#22c55e;font-weight:800;">R:0</div></div>
  </div>
  <div style="font-size:8px;color:#22d3ee;margin-top:3px;">▸ TRACK LOCKED</div>
</div>

<!-- TAIL MATRIX 5x5 -->
<div class="callout magenta" style="right:1%;top:82%;width:130px;">
  <div class="h">▦ TAIL MATRIX 5×5</div>
  <div style="display:grid;grid-template-columns:repeat(5,9px);gap:2px;justify-content:center;margin-top:3px;">''' + ''.join(f'<div style="width:9px;height:9px;border-radius:50%;background:{"#f472b6" if v else "#1a0a14"};box-shadow:{"0 0 4px #f472b6" if v else "none"};"></div>' for v in [0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,1,0,0]) + '''</div>
  <div style="font-size:8px;color:#bba;margin-top:3px;text-align:center;">▸ HEART · BLINK</div>
</div>

<!-- SERVO = RUDDER (tail callout, lower-left) -->
<div class="callout" style="left:1%;top:82%;width:130px;">
  <div class="h">⤺ RUDDER · SERVO</div>
  <div class="v" style="color:#22d3ee;">90° <span style="font-size:9px;color:#bba;">CENTER</span></div>
  <div style="text-align:center;margin-top:4px;"><svg width="80" height="40" viewBox="0 0 80 40"><path d="M 5 35 A 35 35 0 0 1 75 35" fill="none" stroke="#1e3a5a" stroke-width="1"/>''' + ''.join(f'<line x1="40" y1="5" x2="40" y2="{9 if i%3==0 else 7}" stroke="#22d3ee" stroke-width="0.5" transform="rotate({-90+i*15} 40 35)"/>' for i in range(13)) + '''<line x1="40" y1="35" x2="40" y2="5" stroke="#22d3ee" stroke-width="2" style="filter:drop-shadow(0 0 2px #22d3ee);"/><circle cx="40" cy="35" r="3" fill="#22d3ee"/></svg></div>
</div>'''

    # Stage container with calculated aspect
    body = f'''<div class="stage">
  {nav}
  <div style="position:relative;width:100%;aspect-ratio:1500/900;min-height:560px;">
    {plane_svg}
    {props}
    {callouts}
  </div>
</div>'''
    return base_html('✈ v4 #1 Plane Top-Down Cutaway', body)


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Stubs for #2..#10                                                  ║
# ╚═════════════════════════════════════════════════════════════════════╝
def _stub(idx, name, emoji, vibe):
    return base_html(f'{emoji} v4 #{idx} {name}',
        f'''<div class="stage">{title_bar(idx, name, emoji, vibe)}
        <div style="margin:80px auto;text-align:center;padding:50px;border:2px dashed #1e3a5a;border-radius:14px;max-width:600px;">
          <div style="font-size:64px;margin-bottom:14px;filter:drop-shadow(0 0 12px #22d3ee);">{emoji}</div>
          <div style="font-size:18px;color:#22d3ee;letter-spacing:0.05em;">{name}</div>
          <div style="font-size:11px;color:#7fa;margin-top:8px;">v4 cutaway · awaiting design pass</div>
        </div></div>''')

# ╔═════════════════════════════════════════════════════════════════════╗
# ║  #2 — CAR SIDE-VIEW CUTAWAY (rally hatchback silhouette)            ║
# ╚═════════════════════════════════════════════════════════════════════╝
def make_2():
    nav = title_bar(2, 'Car · Side-View Cutaway', '🚗', 'rally car · headlights · taillights · steering · road')

    # SVG side-view car. 1500x900 stage, car horizontal, ground line at y=720.
    car_svg = '''
<svg viewBox="0 0 1500 900" style="position:absolute;inset:0;width:100%;height:100%;z-index:1;" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="body2" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.06"/>
      <stop offset="50%" stop-color="#fbbf24" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#fbbf24" stop-opacity="0.04"/>
    </linearGradient>
    <linearGradient id="glass2" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0.05"/>
    </linearGradient>
    <radialGradient id="head2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fff" stop-opacity="1"/>
      <stop offset="40%" stop-color="#fef3c7" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#fbbf24" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="tail2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fff" stop-opacity="0.8"/>
      <stop offset="40%" stop-color="#ef4444" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#7f1d1d" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow2"><feGaussianBlur stdDeviation="3"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>

  <!-- ROAD with center line stripe (animated would be JS; we do dashed) -->
  <line x1="0" y1="720" x2="1500" y2="720" stroke="#22d3ee" stroke-width="1.5" opacity="0.6"/>
  <line x1="0" y1="730" x2="1500" y2="730" stroke="#22d3ee" stroke-width="0.4" stroke-dasharray="20 16" opacity="0.45"/>
  <line x1="0" y1="745" x2="1500" y2="745" stroke="#22d3ee" stroke-width="0.4" stroke-dasharray="40 30" opacity="0.25"/>
  <!-- ground glow -->
  <rect x="0" y="720" width="1500" height="180" fill="url(#body2)" opacity="0.4"/>

  <!-- CAR BODY shape: hatchback rally silhouette pointing right.
       Path runs: lower-front-bumper → up to hood → windshield rake →
       roof → rear hatch slope → rear bumper → wheel arches → back to start. -->
  <path d="M 380 700
           L 370 660
           Q 360 645 360 625
           L 380 605
           Q 410 588 460 580
           L 510 460
           Q 530 430 575 415
           L 720 408
           Q 800 405 870 415
           Q 920 425 950 460
           L 1010 580
           Q 1060 588 1090 605
           L 1115 625
           Q 1115 645 1105 660
           L 1095 700
           Z"
        fill="url(#body2)" stroke="#fbbf24" stroke-width="2.4" filter="url(#glow2)"/>

  <!-- WINDSHIELD + WINDOWS (one big greenhouse shape) -->
  <path d="M 540 460
           L 590 425
           Q 720 415 870 425
           L 920 460
           L 880 470
           Q 720 460 580 470 Z"
        fill="url(#glass2)" stroke="#22d3ee" stroke-width="1.4"/>
  <!-- B-pillar -->
  <line x1="730" y1="425" x2="730" y2="460" stroke="#fbbf24" stroke-width="1.6" opacity="0.7"/>
  <!-- Door line -->
  <line x1="730" y1="475" x2="730" y2="600" stroke="#fbbf24" stroke-width="0.8" opacity="0.55"/>
  <!-- Hood line -->
  <line x1="475" y1="582" x2="540" y2="468" stroke="#fbbf24" stroke-width="0.6" opacity="0.4"/>

  <!-- WHEEL WELLS (cut-outs on body) -->
  <circle cx="510" cy="700" r="68" fill="#02040a" stroke="#fbbf24" stroke-width="1.2"/>
  <circle cx="960" cy="700" r="68" fill="#02040a" stroke="#fbbf24" stroke-width="1.2"/>

  <!-- TIRES -->
  <circle cx="510" cy="700" r="58" fill="#0a0a0a" stroke="#3a3328" stroke-width="2"/>
  <circle cx="960" cy="700" r="58" fill="#0a0a0a" stroke="#3a3328" stroke-width="2"/>
  <!-- WHEEL HUBS w/ spokes (will spin via CSS overlay div) -->
  <circle cx="510" cy="700" r="32" fill="#1a1a1a" stroke="#666" stroke-width="1.5"/>
  <circle cx="960" cy="700" r="32" fill="#1a1a1a" stroke="#666" stroke-width="1.5"/>

  <!-- HEADLIGHT (front, 2 stacked) -->
  <ellipse cx="380" cy="615" rx="20" ry="14" fill="url(#head2)" stroke="#fbbf24" stroke-width="1.4" filter="url(#glow2)">
    <animate attributeName="opacity" values="1;0.7;1" dur="2s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="380" cy="645" rx="14" ry="10" fill="url(#head2)" stroke="#fbbf24" stroke-width="1" filter="url(#glow2)"/>
  <!-- headlight beam cone -->
  <path d="M 360 615 L 230 560 L 230 670 Z" fill="#fbbf24" opacity="0.13" filter="url(#glow2)"/>

  <!-- TAILLIGHT (rear) -->
  <ellipse cx="1115" cy="615" rx="18" ry="12" fill="url(#tail2)" stroke="#ef4444" stroke-width="1.4" filter="url(#glow2)">
    <animate attributeName="opacity" values="0.6;1;0.6" dur="1.4s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="1115" cy="645" rx="12" ry="8" fill="url(#tail2)" stroke="#ef4444" stroke-width="1"/>

  <!-- HOOD: small horn icon (buzzer) -->
  <circle cx="450" cy="595" r="6" fill="none" stroke="#fbbf24" stroke-width="1.2"/>
  <path d="M 446 593 L 454 593 M 446 597 L 454 597" stroke="#fbbf24" stroke-width="1"/>

  <!-- ROOF ANTENNA (IR receiver) -->
  <line x1="800" y1="408" x2="800" y2="362" stroke="#f472b6" stroke-width="2"/>
  <circle cx="800" cy="358" r="5" fill="#f472b6" filter="url(#glow2)">
    <animate attributeName="opacity" values="1;0.3;1" dur="0.9s" repeatCount="indefinite"/>
  </circle>

  <!-- LICENSE PLATE / 5x5 MATRIX on rear hatch -->
  <rect x="1030" y="495" width="60" height="40" fill="#0a0408" stroke="#f472b6" stroke-width="1.2"/>

  <!-- LINE SENSORS under chassis (just under front wheel) -->
  <rect x="430" y="750" width="14" height="14" fill="#22d3ee" stroke="#0ff" stroke-width="0.6" filter="url(#glow2)">
    <animate attributeName="opacity" values="1;0.5;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>
  <rect x="450" y="750" width="14" height="14" fill="#22d3ee" stroke="#0ff" stroke-width="0.6" filter="url(#glow2)">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="1.2s" repeatCount="indefinite"/>
  </rect>
  <!-- track patch on road -->
  <rect x="425" y="765" width="44" height="8" fill="#000" opacity="0.85"/>

  <!-- CALLOUT LINES -->
  <line x1="380" y1="610" x2="170" y2="500" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="1130" y1="615" x2="1340" y2="500" stroke="#ef4444" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="510" y1="700" x2="170" y2="780" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="960" y1="700" x2="1340" y2="780" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="800" y1="356" x2="170" y2="200" stroke="#f472b6" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="660" y1="430" x2="1340" y2="200" stroke="#22d3ee" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="730" y1="430" x2="170" y2="350" stroke="#a78bfa" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="850" y1="430" x2="1340" y2="350" stroke="#a78bfa" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="450" y1="588" x2="170" y2="60" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="1060" y1="515" x2="1340" y2="60" stroke="#f472b6" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="450" y1="780" x2="1340" y2="855" stroke="#22d3ee" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
  <line x1="1010" y1="582" x2="170" y2="855" stroke="#22c55e" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
</svg>'''

    # Spinning wheel hubs (HTML overlays so we can use CSS spin)
    hubs = '''
<div style="position:absolute;left:34%;top:77.7%;width:50px;height:50px;transform:translate(-50%,-50%);z-index:2;">
  <div style="width:100%;height:100%;border-radius:50%;background:conic-gradient(#fbbf24 0 6%,transparent 6% 50%,#fbbf24 50% 56%,transparent 56% 100%);animation:propspin 0.4s linear infinite;opacity:0.85;filter:drop-shadow(0 0 4px #fbbf24);"></div>
</div>
<div style="position:absolute;left:64%;top:77.7%;width:50px;height:50px;transform:translate(-50%,-50%);z-index:2;">
  <div style="width:100%;height:100%;border-radius:50%;background:conic-gradient(#fbbf24 0 6%,transparent 6% 50%,#fbbf24 50% 56%,transparent 56% 100%);animation:propspin 0.4s linear infinite;opacity:0.85;filter:drop-shadow(0 0 4px #fbbf24);"></div>
</div>'''

    callouts = '''
<!-- HEADLIGHT = LED 1 -->
<div class="callout amber" style="left:1%;top:54%;width:140px;">
  <div class="h">◐ HEADLIGHT · LED 1</div>
  <div style="display:flex;align-items:center;gap:6px;"><div style="width:14px;height:14px;border-radius:50%;background:#fbbf24;box-shadow:0 0 12px #fbbf24,0 0 24px #fef3c7;animation:flicker 2s infinite;"></div><div class="v" style="color:#fbbf24;">HIGH</div></div>
  <div style="font-size:8px;color:#bba;margin-top:3px;">▸ FRONT BEAM · 100%</div>
</div>

<!-- TAILLIGHT = LED 2 -->
<div class="callout magenta" style="right:1%;top:54%;width:140px;">
  <div class="h">◐ TAILLIGHT · LED 2</div>
  <div style="display:flex;align-items:center;gap:6px;"><div style="width:14px;height:14px;border-radius:50%;background:#ef4444;box-shadow:0 0 12px #ef4444;animation:blink 1.4s infinite;"></div><div class="v" style="color:#ef4444;">BRAKE</div></div>
  <div style="font-size:8px;color:#bba;margin-top:3px;">▸ REAR · pulse</div>
</div>

<!-- FRONT WHEEL = MOTOR L -->
<div class="callout amber" style="left:1%;top:84%;width:150px;">
  <div class="h">⟳ FRONT WHEEL · MOTOR L</div>
  <div class="v">156 <span style="font-size:9px;color:#bba;">RPM</span></div>
  <div style="height:5px;background:#1a1408;border-radius:2px;margin-top:4px;overflow:hidden;"><div style="width:65%;height:100%;background:linear-gradient(90deg,#fbbf24,#fff);box-shadow:0 0 6px #fbbf24;"></div></div>
  <div style="font-size:8px;color:#bba;margin-top:3px;">FWD · 65% · 4WD-LOCK</div>
</div>

<!-- REAR WHEEL = MOTOR R -->
<div class="callout amber" style="right:1%;top:84%;width:150px;">
  <div class="h">⟳ REAR WHEEL · MOTOR R</div>
  <div class="v">158 <span style="font-size:9px;color:#bba;">RPM</span></div>
  <div style="height:5px;background:#1a1408;border-radius:2px;margin-top:4px;overflow:hidden;"><div style="width:67%;height:100%;background:linear-gradient(90deg,#fbbf24,#fff);box-shadow:0 0 6px #fbbf24;"></div></div>
  <div style="font-size:8px;color:#bba;margin-top:3px;">FWD · 67%</div>
</div>

<!-- ROOF ANTENNA = IR -->
<div class="callout magenta" style="left:1%;top:18%;width:140px;">
  <div class="h">◉ ROOF ANTENNA · IR 38kHz</div>
  <div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;border-radius:50%;background:radial-gradient(circle,#fff,#f472b6 60%);box-shadow:0 0 8px #f472b6;animation:pulsefast 1.4s infinite;"></div><div class="v" style="color:#f472b6;font-size:13px;">[ ▲ ]</div></div>
  <div style="font-size:8px;color:#bba;margin-top:3px;">▸ FORWARD command</div>
</div>

<!-- WINDSHIELD HUD: speed/compass -->
<div class="callout" style="right:1%;top:18%;width:140px;">
  <div class="h">► HUD · SPEED · HDG</div>
  <div class="v" style="color:#22d3ee;">42 <span style="font-size:9px;color:#bba;">km/h</span></div>
  <div style="display:flex;justify-content:space-between;font-size:9px;color:#22d3ee;margin-top:3px;font-family:monospace;"><span>HDG 072°</span><span>↑ N</span></div>
</div>

<!-- DASHBOARD LEFT: ACCEL -->
<div class="callout violet" style="left:1%;top:36%;width:140px;">
  <div class="h">⌘ G-METER · ACCEL</div>
  <div style="position:relative;width:90px;height:50px;margin:0 auto;background:radial-gradient(circle,#0a0a14,#000);border:1px solid #1e3a5a;border-radius:3px;overflow:hidden;"><div style="position:absolute;top:50%;left:0;right:0;border-top:1px dashed #1e3a5a;"></div><div style="position:absolute;left:50%;top:0;bottom:0;border-left:1px dashed #1e3a5a;"></div><div style="position:absolute;width:12px;height:12px;border-radius:50%;background:#a78bfa;box-shadow:0 0 8px #a78bfa;top:42%;left:55%;"></div></div>
  <div style="font-size:8px;color:#a78bfa;margin-top:3px;text-align:center;">X+0.3g  Z+0.98g</div>
</div>

<!-- DASHBOARD RIGHT: TEMP -->
<div class="callout violet" style="right:1%;top:36%;width:140px;">
  <div class="h">℃ ENGINE TEMP</div>
  <div class="v" style="color:#a78bfa;">22.4 <span style="font-size:9px;color:#bba;">°C</span></div>
  <div style="display:flex;align-items:center;gap:5px;margin-top:4px;">
    <div style="flex:1;height:6px;background:linear-gradient(90deg,#22d3ee,#fbbf24,#ef4444);border-radius:3px;position:relative;"><div style="position:absolute;left:30%;top:-2px;bottom:-2px;width:2px;background:#fff;box-shadow:0 0 4px #fff;"></div></div>
  </div>
  <div style="font-size:8px;color:#a78bfa;margin-top:2px;">▸ COOL · OK</div>
</div>

<!-- HORN = BUZZER (top left, line from hood) -->
<div class="callout amber" style="left:1%;top:3%;width:140px;">
  <div class="h">♪ HORN · BUZZER</div>
  <div class="v" style="color:#fbbf24;">A4 <span style="font-size:9px;color:#bba;">440 Hz</span></div>
  <div style="display:flex;gap:1px;height:14px;margin-top:4px;background:#000;padding:1px;">''' + ''.join(f'<div style="flex:1;background:linear-gradient(180deg,#fbbf24,#000);height:{30+(i*17)%70}%;align-self:flex-end;animation:flicker {1.0+(i%5)*0.2}s ease-in-out infinite;animation-delay:{i*0.05}s;"></div>' for i in range(16)) + '''</div>
</div>

<!-- LICENSE PLATE = MATRIX 5x5 (top right) -->
<div class="callout magenta" style="right:1%;top:3%;width:140px;">
  <div class="h">▦ DISPLAY · 5×5 MATRIX</div>
  <div style="display:grid;grid-template-columns:repeat(5,9px);gap:2px;justify-content:center;margin-top:3px;">''' + ''.join(f'<div style="width:9px;height:9px;border-radius:50%;background:{"#f472b6" if v else "#1a0a14"};box-shadow:{"0 0 4px #f472b6" if v else "none"};"></div>' for v in [1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1]) + '''</div>
  <div style="font-size:8px;color:#bba;margin-top:3px;text-align:center;">▸ "X" · ALERT</div>
</div>

<!-- LINE-CAM (under chassis) -->
<div class="callout" style="right:1%;top:96%;width:160px;transform:translateY(-100%);">
  <div class="h">▦ LINE SENSORS · L/R</div>
  <div style="display:flex;gap:4px;height:30px;margin-top:3px;">
    <div style="flex:1;background:#fff;border:1px solid #444;position:relative;"><div style="position:absolute;top:0;left:35%;width:8px;height:100%;background:#000;"></div><div style="position:absolute;bottom:0;left:1px;font-size:7px;color:#22c55e;font-weight:800;">L:0</div></div>
    <div style="flex:1;background:#fff;border:1px solid #444;position:relative;"><div style="position:absolute;top:0;left:55%;width:8px;height:100%;background:#000;"></div><div style="position:absolute;bottom:0;left:1px;font-size:7px;color:#22c55e;font-weight:800;">R:0</div></div>
  </div>
  <div style="font-size:8px;color:#22d3ee;margin-top:3px;">▸ TRACK LOCKED</div>
</div>

<!-- BATTERY (under hood) — anchored bottom-left -->
<div class="callout green" style="left:1%;top:96%;width:160px;transform:translateY(-100%);">
  <div class="h">⚡ BATTERY · LiPo</div>
  <div class="v" style="color:#22c55e;">87% <span style="font-size:9px;color:#bba;">3.78V</span></div>
  <div style="height:8px;background:#000;border:1px solid #14532d;display:flex;gap:1px;padding:1px;margin-top:4px;">''' + ''.join(f'<div style="flex:1;background:{"linear-gradient(180deg,#22c55e,#16a34a)" if i<8 else "#0a1808"};box-shadow:{"0 0 3px #22c55e" if i<8 else "none"};"></div>' for i in range(10)) + '''</div>
</div>

<!-- SERVO = STEERING (floating bubble centred above the front wheel) -->
<div class="callout" style="left:24%;top:62%;width:130px;">
  <div class="h">⤺ STEERING · SERVO</div>
  <div class="v" style="color:#22d3ee;">90° <span style="font-size:9px;color:#bba;">CENTER</span></div>
  <div style="text-align:center;margin-top:4px;"><svg width="80" height="40" viewBox="0 0 80 40"><path d="M 5 35 A 35 35 0 0 1 75 35" fill="none" stroke="#1e3a5a" stroke-width="1"/>''' + ''.join(f'<line x1="40" y1="5" x2="40" y2="{9 if i%3==0 else 7}" stroke="#22d3ee" stroke-width="0.5" transform="rotate({-90+i*15} 40 35)"/>' for i in range(13)) + '''<line x1="40" y1="35" x2="40" y2="5" stroke="#22d3ee" stroke-width="2" style="filter:drop-shadow(0 0 2px #22d3ee);"/><circle cx="40" cy="35" r="3" fill="#22d3ee"/></svg></div>
</div>

<!-- DRIVER MIC (bubble centred above driver seat) -->
<div class="callout violet" style="right:24%;top:62%;width:130px;">
  <div class="h">▣ COCKPIT MIC</div>
  <div class="v" style="color:#a78bfa;">−18 <span style="font-size:9px;color:#bba;">dB</span></div>
  <div style="display:flex;gap:1px;height:14px;margin-top:4px;background:#000;padding:1px;">''' + ''.join(f'<div style="flex:1;background:linear-gradient(180deg,{"#ef4444" if i>14 else "#fbbf24" if i>10 else "#a78bfa"},#000);height:{40+(i*17)%55}%;align-self:flex-end;animation:flicker {1.0+(i%5)*0.2}s ease-in-out infinite;animation-delay:{i*0.04}s;"></div>' for i in range(18)) + '''</div>
</div>'''

    body = f'''<div class="stage">
  {nav}
  <div style="position:relative;width:100%;aspect-ratio:1500/900;min-height:560px;">
    {car_svg}
    {hubs}
    {callouts}
  </div>
</div>'''
    return base_html('🚗 v4 #2 Car Side-View Cutaway', body)
def make_3():  return _stub(3, 'UFO Saucer · Top-Down', '🛸', 'ring of lights · core glow')
def make_4():  return _stub(4, 'Rocket · Vertical Cutaway', '🚀', 'multi-stage · payload · fins')
def make_5():  return _stub(5, 'Submarine · Side Cutaway', '🚢', 'pressure hull · sonar')
def make_6():  return _stub(6, 'Mech · Front Standing', '🤖', 'humanoid · arm cannons')
def make_7():  return _stub(7, 'F1 · Top-Down', '🏎', 'open cockpit · sidepods')
def make_8():  return _stub(8, 'Helicopter · Side', '🛩', 'rotor · tail · skids')
def make_9():  return _stub(9, 'Drone Quad · Top-Down', '🚁', '4 props · X-frame')
def make_10(): return _stub(10, 'Space Probe · Voyager-style', '🛰', 'dish · booms · RTG')


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  GENERATE                                                            ║
# ╚═════════════════════════════════════════════════════════════════════╝
makers = [make_1, make_2, make_3, make_4, make_5, make_6, make_7, make_8, make_9, make_10]
labels = [
    ('✈', 'Plane · Top-Down Cutaway',     'twin engine · nav lights · cockpit cluster'),
    ('🚗', 'Car · Side-View Cutaway',     'rally car · headlights · IR antenna'),
    ('🛸', 'UFO Saucer · Top-Down',       'ring of lights · core glow'),
    ('🚀', 'Rocket · Vertical Cutaway',   'multi-stage · payload · fins'),
    ('🚢', 'Submarine · Side Cutaway',    'pressure hull · sonar'),
    ('🤖', 'Mech · Front Standing',       'humanoid · arm cannons'),
    ('🏎', 'F1 · Top-Down',               'open cockpit · sidepods'),
    ('🛩', 'Helicopter · Side',           'rotor · tail · skids'),
    ('🚁', 'Drone Quad · Top-Down',       '4 props · X-frame'),
    ('🛰', 'Space Probe · Voyager-style', 'dish · booms · RTG'),
]

for i, maker in enumerate(makers, 1):
    out = os.path.join(OUT, f'cockpit-lab_v4_{i}.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(maker())
    emoji, name, _ = labels[i-1]
    print(f'  + cockpit-lab_v4_{i}.html  ({emoji} {name})')

# Gallery
gallery = '''<!doctype html>
<html lang="en" data-theme="carbon">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🛸 Cockpit Lab v4 — vehicle cutaways</title>
<link rel="stylesheet" href="../workshops/theme.css">
<style>
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:var(--font-body,system-ui);background:#02040a;color:#dff;padding:24px 18px 40px;position:relative;min-height:100vh;}
  body::before{content:'';position:fixed;inset:0;background-image:radial-gradient(1px 1px at 20% 30%,#fff 50%,transparent 50%),radial-gradient(1px 1px at 70% 60%,#fff 50%,transparent 50%),radial-gradient(1.5px 1.5px at 50% 80%,#dff 50%,transparent 50%);opacity:0.5;animation:tw 5s ease-in-out infinite;z-index:0;}
  @keyframes tw{0%,100%{opacity:0.3;}50%{opacity:0.7;}}
  h1{color:#22d3ee;font-size:1.8rem;margin-bottom:6px;text-align:center;text-shadow:0 0 8px #22d3ee;position:relative;z-index:1;}
  .sub{text-align:center;color:#7fa;margin-bottom:24px;font-size:0.95rem;max-width:780px;margin-left:auto;margin-right:auto;line-height:1.5;position:relative;z-index:1;}
  .nav{text-align:center;margin:14px 0 24px;position:relative;z-index:1;}
  .nav a{color:#7fa;text-decoration:none;padding:6px 14px;border:1px solid #1e3a5a;border-radius:999px;font-size:0.85rem;margin:0 4px;}
  .nav a:hover{color:#22d3ee;border-color:#22d3ee;}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;max-width:1300px;margin:0 auto;position:relative;z-index:1;}
  .card{display:block;text-decoration:none;padding:18px 20px;border-radius:14px;border:1.5px solid #1e3a5a;background:rgba(2,18,30,0.6);color:#dff;transition:all 0.15s;backdrop-filter:blur(4px);}
  .card:hover{transform:translateY(-3px);border-color:#22d3ee;box-shadow:0 8px 22px rgba(34,211,238,0.25);}
  .card .emoji{font-size:2.4rem;line-height:1;margin-bottom:8px;filter:drop-shadow(0 0 8px #22d3ee);}
  .card .num{font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#7fa;}
  .card h3{font-size:1.1rem;color:#22d3ee;margin:6px 0 8px;}
  .card .vibe{font-size:0.86rem;color:#dff;opacity:0.85;line-height:1.45;}
  .dna{margin-top:10px;font-size:0.78rem;color:#fbbf24;font-family:'JetBrains Mono',monospace;}
  .stub{opacity:0.5;}
  .stub .dna{color:#888;}
</style>
</head>
<body>
<h1>🛸 Cockpit Lab v4 — vehicle cutaways</h1>
<p class="sub">Each design = a recognizable vehicle silhouette with all Maqueen hardware drawn ON the actual body parts. Holographic callouts, neon glow, starfield, scanner sweep — sci-fi ambiance.</p>
<div class="nav">
  <a href="index.html">🧪 All Labs</a>
  <a href="cockpit-lab.html">v1</a>
  <a href="cockpit-lab_v2.html">v2</a>
  <a href="cockpit-lab_v3.html">v3</a>
  <a href="../index.html">🤖 Robot App</a>
</div>
<div class="grid">
'''
DONE = {1, 2}
for i, (emoji, name, vibe) in enumerate(labels, 1):
    klass = 'card' if i in DONE else 'card stub'
    tag = '▸ CUTAWAY READY' if i in DONE else '◇ stub · pending'
    gallery += f'''  <a class="{klass}" href="cockpit-lab_v4_{i}.html">
    <div class="emoji">{emoji}</div>
    <div class="num">cockpit-lab_v4_{i}.html</div>
    <h3>{name}</h3>
    <div class="vibe">{vibe}</div>
    <div class="dna">{tag}</div>
  </a>
'''
gallery += '''</div>
</body>
</html>
'''
with open(os.path.join(OUT, 'cockpit-lab_v4.html'), 'w', encoding='utf-8') as f:
    f.write(gallery)
print('\n  + cockpit-lab_v4.html  (gallery)')
print(f'\nDone — written to {os.path.relpath(OUT)}')
