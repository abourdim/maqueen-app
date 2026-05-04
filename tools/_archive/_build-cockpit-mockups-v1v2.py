#!/usr/bin/env python3
"""Generate 10 GENUINELY different cockpit-lab mockups + gallery picker.

Each file has its own layout DNA — not the same template recoloured. Each
metaphor (plane, F1, submarine, mech, DJ, studio mixer, smartwatch, etc.)
gets its own HTML structure, grid, instrument geometry, and feel.

Re-runnable; overwrites previous files.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'labs')

# ╔══════════════════════════════════════════════════════════════════╗
# ║  Shared helpers (top-bar nav, base reset)                         ║
# ╚══════════════════════════════════════════════════════════════════╝
def nav_bar(idx, name, emoji, vibe, accent='#fbbf24', dim='#666', text='#fff', bg='#000'):
    prev_idx = (idx - 2) % 10 + 1
    next_idx = idx % 10 + 1
    return f'''<div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:0 0 14px;background:rgba(0,0,0,0.55);border:1px solid {dim};border-radius:10px;flex-wrap:wrap;font-family:'JetBrains Mono',monospace;">
  <div style="font-size:14px;font-weight:700;color:{accent};letter-spacing:0.06em;margin-right:auto;">{emoji} #{idx} · {name} <span style="color:{dim};font-weight:400;font-size:11px;margin-left:8px;">{vibe}</span></div>
  <a href="cockpit-lab_v2.html" style="color:{text};text-decoration:none;border:1px solid {dim};border-radius:6px;padding:4px 10px;font-size:12px;">⚙ Gallery</a>
  <a href="cockpit-lab_v2_{prev_idx}.html" style="color:{text};text-decoration:none;border:1px solid {dim};border-radius:6px;padding:4px 10px;font-size:12px;">‹ Prev</a>
  <a href="cockpit-lab_v2_{next_idx}.html" style="color:{text};text-decoration:none;border:1px solid {dim};border-radius:6px;padding:4px 10px;font-size:12px;">Next ›</a>
</div>'''


def base_html(title, body, bg='#0a0e14', font="'JetBrains Mono', monospace"):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  html,body{{background:{bg};color:#fff;font-family:{font};min-height:100vh;overflow-x:hidden;}}
  body{{padding:14px 18px 32px;}}
  @media(max-width:520px){{html,body{{overflow-x:hidden;}}}}
</style>
</head>
<body>
{body}
</body>
</html>'''


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #1 — PLANE COCKPIT (Cessna twin-yoke + 6-pack + pedestal)        ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_1():
    nav = nav_bar(1, 'Plane Cockpit', '🛩', 'twin yokes · 6-pack · pedestal',
                  accent='#fbbf24', dim='#5c4d2a', text='#fef9c3', bg='#1a1408')
    return base_html('🛩 #1 Plane Cockpit',
        nav + '''
<style>
  .pc-grid{display:grid;grid-template-columns:1fr 2fr 1fr;gap:14px;max-width:1300px;margin:0 auto;}
  @media(max-width:920px){.pc-grid{grid-template-columns:1fr;}}
  .pc-yoke{background:linear-gradient(135deg,#3d2c14,#1a1408);border:2px solid #5c4d2a;border-radius:14px;padding:18px;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:340px;}
  .pc-yoke .wheel{width:160px;height:160px;border-radius:50%;border:8px solid #2a1f10;background:radial-gradient(circle at 35% 30%,#7c5d2a,#3d2c14 70%);box-shadow:inset 0 0 30px rgba(0,0,0,0.7),0 0 18px rgba(251,191,36,0.2);position:relative;}
  .pc-yoke .wheel::before{content:'';position:absolute;inset:35px;border-radius:50%;border:3px solid #fbbf24;background:radial-gradient(circle at 35% 30%,rgba(251,191,36,0.3),transparent 70%);}
  .pc-yoke .wheel::after{content:'M';position:absolute;inset:0;display:grid;place-items:center;color:#fbbf24;font-weight:900;font-size:36px;text-shadow:0 0 10px #fbbf24;}
  .pc-yoke .lbl{margin-top:14px;font-size:11px;color:#a98864;letter-spacing:0.2em;}
  .pc-center{display:flex;flex-direction:column;gap:14px;}
  .pc-6pack{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);gap:6px;background:#0a0804;border:3px solid #2a1f10;border-radius:10px;padding:10px;}
  .pc-gauge{aspect-ratio:1;background:radial-gradient(circle at 50% 50%,#0a0804 60%,#1a1408 100%);border:3px solid #2a1f10;border-radius:50%;position:relative;display:grid;place-items:center;box-shadow:inset 0 0 14px rgba(0,0,0,0.9),0 0 8px rgba(251,191,36,0.15);}
  .pc-gauge .name{position:absolute;top:8px;font-size:7px;color:#a98864;letter-spacing:0.1em;text-align:center;width:100%;font-weight:700;}
  .pc-gauge .val{font-size:14px;color:#fef9c3;font-weight:800;text-shadow:0 0 6px #fbbf24;}
  .pc-gauge .unit{position:absolute;bottom:14%;font-size:7px;color:#a98864;}
  .pc-gauge .needle{position:absolute;width:2px;height:42%;background:#fbbf24;top:8%;left:calc(50% - 1px);transform-origin:bottom center;transform:rotate(45deg);box-shadow:0 0 4px #fbbf24;}
  .pc-gauge .needle.swing{animation:swing 4s ease-in-out infinite;}
  @keyframes swing{0%,100%{transform:rotate(-45deg);}50%{transform:rotate(60deg);}}
  .pc-pedestal{background:#0a0804;border:3px solid #2a1f10;border-radius:8px;padding:10px;display:grid;grid-template-columns:repeat(3,1fr);gap:6px;}
  .pc-radio{background:#000;border:1px solid #2a1f10;padding:6px;font-family:'Courier New',monospace;}
  .pc-radio .freq{color:#22c55e;font-size:14px;font-weight:800;text-shadow:0 0 4px #22c55e;}
  .pc-radio .label{font-size:7px;color:#a98864;letter-spacing:0.1em;}
  .pc-throttle{background:linear-gradient(180deg,#3d2c14 0%,#0a0804 100%);border:2px solid #2a1f10;border-radius:6px;padding:6px;height:120px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;}
  .pc-throttle .lever{width:24px;height:48px;background:linear-gradient(135deg,#fbbf24,#a16207);border-radius:4px 4px 8px 8px;box-shadow:0 0 8px rgba(251,191,36,0.4);}
  .pc-pedals{background:#0a0804;border:2px solid #2a1f10;border-radius:6px;padding:8px;display:flex;justify-content:space-around;}
  .pc-pedal{width:34px;height:30px;background:linear-gradient(135deg,#3d2c14,#1a1408);border:1px solid #5c4d2a;border-radius:3px 3px 0 0;}
</style>
<div class="pc-grid">
  <div class="pc-yoke"><div class="wheel"></div><div class="lbl">YOKE · LEFT</div></div>
  <div class="pc-center">
    <div class="pc-6pack">
      <div class="pc-gauge"><div class="name">AIRSPEED</div><div class="val">42</div><div class="unit">KTS</div><div class="needle swing"></div></div>
      <div class="pc-gauge"><div class="name">ATTITUDE</div><div class="val" style="color:#67e8f9">⏤</div><div class="needle"></div></div>
      <div class="pc-gauge"><div class="name">ALTITUDE</div><div class="val">12.4</div><div class="unit">cm</div><div class="needle" style="transform:rotate(80deg)"></div></div>
      <div class="pc-gauge"><div class="name">TURN COORD</div><div class="val" style="font-size:11px">L • R</div><div class="needle" style="transform:rotate(-15deg)"></div></div>
      <div class="pc-gauge"><div class="name">HEADING</div><div class="val">120°</div><div class="needle" style="transform:rotate(120deg)"></div></div>
      <div class="pc-gauge"><div class="name">VERT SPEED</div><div class="val">+50</div><div class="unit">fpm</div><div class="needle" style="transform:rotate(20deg)"></div></div>
    </div>
    <div class="pc-pedestal">
      <div class="pc-radio"><div class="label">COM 1</div><div class="freq">121.500</div></div>
      <div class="pc-radio"><div class="label">NAV 1</div><div class="freq">110.30</div></div>
      <div class="pc-radio"><div class="label">XPDR</div><div class="freq">7700</div></div>
      <div class="pc-throttle"><div class="lever"></div></div>
      <div class="pc-radio" style="display:flex;flex-direction:column;justify-content:space-around"><div class="label">TEMP</div><div class="freq">23.4°</div><div class="label">MIC</div><div class="freq">▮▮▮▮▯▯</div></div>
      <div class="pc-pedals"><div class="pc-pedal"></div><div class="pc-pedal"></div></div>
    </div>
  </div>
  <div class="pc-yoke"><div class="wheel" style="animation:swing 5s ease-in-out infinite"></div><div class="lbl">YOKE · RIGHT</div></div>
</div>
''',
        bg='#1a1408', font="'Courier New', monospace")


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #2 — GLASS COCKPIT AIRLINER (4 MFDs strip + side-stick)          ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_2():
    nav = nav_bar(2, 'Glass Cockpit (Airliner)', '✈️', '4 MFDs · side-stick · FCU',
                  accent='#38bdf8', dim='#1e3a5c', text='#e0f2fe', bg='#0a1828')
    return base_html('✈️ #2 Glass Cockpit',
        nav + '''
<style>
  .gc-mfd-row{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;}
  @media(max-width:920px){.gc-mfd-row{grid-template-columns:repeat(2,1fr);}}
  .gc-mfd{background:#000814;border:2px solid #1e3a5c;border-radius:10px;padding:10px;aspect-ratio:1.2;position:relative;overflow:hidden;}
  .gc-mfd .header{display:flex;justify-content:space-between;font-size:10px;color:#7dd3fc;letter-spacing:0.1em;border-bottom:1px solid #1e3a5c;padding-bottom:5px;margin-bottom:8px;}
  .gc-mfd .big{font-size:36px;font-weight:800;color:#38bdf8;text-shadow:0 0 12px #38bdf8;text-align:center;letter-spacing:0.05em;}
  .gc-mfd .sub{font-size:10px;color:#7dd3fc;text-align:center;margin-top:4px;}
  .gc-mfd .h-tape{position:absolute;left:0;right:0;top:50%;height:30px;background:repeating-linear-gradient(90deg,transparent 0,transparent 20px,rgba(56,189,248,0.4) 20px,rgba(56,189,248,0.4) 22px);}
  .gc-mfd .att{position:absolute;left:10px;right:10px;top:32px;bottom:30px;background:linear-gradient(180deg,#0c4a6e 50%,#7c2d12 50%);border-radius:6px;display:grid;place-items:center;}
  .gc-mfd .att::before{content:'';position:absolute;left:30%;right:30%;top:48%;height:4%;background:#fbbf24;}
  .gc-mfd .compass-rose{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);width:80px;height:80px;border-radius:50%;border:1.5px solid #38bdf8;}
  .gc-mfd .compass-rose::before{content:'N';position:absolute;top:-2px;left:50%;transform:translateX(-50%);font-size:10px;color:#38bdf8;}
  .gc-bottom{display:grid;grid-template-columns:1fr 2fr 1fr;gap:14px;}
  @media(max-width:920px){.gc-bottom{grid-template-columns:1fr;}}
  .gc-stick{background:linear-gradient(135deg,#13243d,#020617);border:2px solid #1e3a5c;border-radius:14px;padding:18px;display:flex;flex-direction:column;align-items:center;gap:10px;}
  .gc-stick .grip{width:60px;height:140px;background:linear-gradient(180deg,#475569,#1e293b 70%);border-radius:30px 30px 8px 8px;box-shadow:0 0 14px rgba(56,189,248,0.3);position:relative;}
  .gc-stick .grip::before{content:'';position:absolute;top:18px;left:18px;width:24px;height:24px;border-radius:50%;background:radial-gradient(circle,#dc2626,#7f1d1d);box-shadow:0 0 8px #dc2626;}
  .gc-stick .lbl{font-size:10px;color:#7dd3fc;letter-spacing:0.2em;}
  .gc-fcu{background:#0c1827;border:2px solid #1e3a5c;border-radius:10px;padding:14px;}
  .gc-fcu-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;}
  .gc-fcu-item{background:#000;border:1px solid #1e3a5c;border-radius:6px;padding:8px 4px;text-align:center;}
  .gc-fcu-item .l{font-size:9px;color:#7dd3fc;letter-spacing:0.1em;}
  .gc-fcu-item .v{font-size:18px;color:#38bdf8;font-weight:700;text-shadow:0 0 8px #38bdf8;font-family:'JetBrains Mono',monospace;}
  .gc-thrust{background:linear-gradient(135deg,#13243d,#020617);border:2px solid #1e3a5c;border-radius:14px;padding:18px;display:flex;flex-direction:column;align-items:center;gap:8px;}
  .gc-thrust .levers{display:flex;gap:8px;height:140px;align-items:flex-end;}
  .gc-thrust .lever{width:30px;background:linear-gradient(180deg,#38bdf8,#0c4a6e);border-radius:6px 6px 12px 12px;height:65%;box-shadow:0 0 8px rgba(56,189,248,0.4);}
  .gc-thrust .lever:nth-child(2){height:80%;}
</style>
<div class="gc-mfd-row">
  <div class="gc-mfd">
    <div class="header"><span>PFD</span><span>SPD 42</span></div>
    <div class="att"></div>
    <div style="position:absolute;left:14px;top:80px;font-size:14px;color:#fbbf24;font-weight:700;">42</div>
    <div style="position:absolute;right:14px;top:80px;font-size:14px;color:#fbbf24;font-weight:700;">12.4</div>
  </div>
  <div class="gc-mfd">
    <div class="header"><span>ND</span><span>HDG 120°</span></div>
    <div class="compass-rose">
      <svg viewBox="0 0 80 80" style="width:100%;height:100%"><line x1="40" y1="6" x2="40" y2="14" stroke="#fbbf24" stroke-width="2"/><polygon points="40,20 35,40 45,40" fill="#fbbf24"/></svg>
    </div>
    <div class="big" style="margin-top:8px;font-size:24px;">120°</div>
    <div class="sub">MAGNETIC</div>
  </div>
  <div class="gc-mfd">
    <div class="header"><span>EICAS</span><span>ENG</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:6px;">
      <div><div class="sub" style="text-align:left;font-size:9px;">N1 L</div><div class="big" style="font-size:24px;text-align:left;">62%</div></div>
      <div><div class="sub" style="text-align:left;font-size:9px;">N1 R</div><div class="big" style="font-size:24px;text-align:left;">68%</div></div>
      <div><div class="sub" style="text-align:left;font-size:9px;">TEMP</div><div class="big" style="font-size:18px;text-align:left;color:#fbbf24;">23.4°</div></div>
      <div><div class="sub" style="text-align:left;font-size:9px;">FUEL</div><div class="big" style="font-size:18px;text-align:left;">78%</div></div>
    </div>
  </div>
  <div class="gc-mfd">
    <div class="header"><span>MFD · SONAR</span><span>SCAN</span></div>
    <svg viewBox="0 0 200 200" style="width:100%;height:auto;margin-top:6px;">
      <circle cx="100" cy="100" r="86" fill="none" stroke="#1e3a5c" stroke-width="1"/>
      <circle cx="100" cy="100" r="56" fill="none" stroke="#1e3a5c" stroke-width="0.8"/>
      <circle cx="100" cy="100" r="26" fill="none" stroke="#1e3a5c" stroke-width="0.6"/>
      <line x1="100" y1="14" x2="100" y2="186" stroke="#1e3a5c" stroke-width="0.5"/>
      <line x1="14" y1="100" x2="186" y2="100" stroke="#1e3a5c" stroke-width="0.5"/>
      <g style="transform-origin:100px 100px;animation:spin 4s linear infinite;">
        <path d="M 100 100 L 100 14 A 86 86 0 0 1 175 70 Z" fill="#38bdf8" opacity="0.3"/>
      </g>
      <circle cx="135" cy="65" r="3" fill="#fbbf24"/>
    </svg>
  </div>
</div>
<div class="gc-bottom">
  <div class="gc-stick"><div class="grip"></div><div class="lbl">SIDE STICK</div></div>
  <div class="gc-fcu">
    <div style="font-size:11px;color:#7dd3fc;letter-spacing:0.2em;margin-bottom:10px;">⚙ FCU · FLIGHT CONTROL UNIT</div>
    <div class="gc-fcu-grid">
      <div class="gc-fcu-item"><div class="l">SPD</div><div class="v">42</div></div>
      <div class="gc-fcu-item"><div class="l">HDG</div><div class="v">120</div></div>
      <div class="gc-fcu-item"><div class="l">ALT</div><div class="v">12</div></div>
      <div class="gc-fcu-item"><div class="l">VS</div><div class="v">+50</div></div>
      <div class="gc-fcu-item"><div class="l">ECHO</div><div class="v" style="color:#22c55e">●</div></div>
      <div class="gc-fcu-item"><div class="l">A/THR</div><div class="v" style="color:#22c55e;font-size:14px">ARMED</div></div>
      <div class="gc-fcu-item"><div class="l">A/P</div><div class="v" style="color:#fbbf24;font-size:14px">CMD</div></div>
      <div class="gc-fcu-item"><div class="l">FD</div><div class="v" style="color:#22c55e;font-size:14px">ON</div></div>
      <div class="gc-fcu-item"><div class="l">MIC</div><div class="v" style="font-size:14px">▮▮▮▮▯</div></div>
      <div class="gc-fcu-item"><div class="l">BAT</div><div class="v" style="font-size:14px">78%</div></div>
    </div>
  </div>
  <div class="gc-thrust"><div class="levers"><div class="lever"></div><div class="lever"></div></div><div class="lbl" style="font-size:10px;color:#7dd3fc;letter-spacing:0.2em;">THRUST · L · R</div></div>
</div>
<style>@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}</style>
''',
        bg='#0a1828', font="'Inter', sans-serif")


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #3 — FIGHTER JET HUD (green wireframe overlay)                   ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_3():
    nav = nav_bar(3, 'Fighter Jet HUD', '🛫', 'green wireframe · pitch ladder · MFD pages',
                  accent='#86efac', dim='#1f3a1f', text='#bbf7d0', bg='#000300')
    return base_html('🛫 #3 Fighter Jet HUD',
        nav + '''
<style>
  .fj-stage{position:relative;height:520px;background:linear-gradient(180deg,#0a1620 0%,#1a3050 50%,#0c1d10 50%,#000 100%);border:2px solid #1f3a1f;border-radius:10px;overflow:hidden;}
  @media(max-width:540px){.fj-stage{height:360px;}}
  .fj-hud-overlay{position:absolute;inset:0;}
  .fj-tape{position:absolute;width:60px;border:1px solid #86efac;background:rgba(0,30,0,0.4);font-family:'JetBrains Mono',monospace;color:#86efac;text-shadow:0 0 6px #86efac;padding:4px 6px;font-size:11px;}
  .fj-tape .v{font-size:24px;font-weight:800;text-align:center;}
  .fj-tape .l{font-size:9px;text-align:center;letter-spacing:0.1em;}
  .fj-pitch-ladder line{stroke:#86efac;stroke-width:1.2;filter:drop-shadow(0 0 3px #86efac);}
  .fj-pitch-ladder text{fill:#86efac;font-family:'JetBrains Mono',monospace;font-size:10px;text-shadow:0 0 4px #86efac;}
  .fj-reticle{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:100px;height:100px;}
  .fj-reticle line{stroke:#86efac;stroke-width:2;filter:drop-shadow(0 0 4px #86efac);}
  .fj-reticle circle{stroke:#86efac;stroke-width:1.5;fill:none;}
  .fj-bottom{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:10px;}
  @media(max-width:820px){.fj-bottom{grid-template-columns:1fr;}}
  .fj-mfd{background:#000300;border:2px solid #1f3a1f;border-radius:8px;padding:10px;font-family:'JetBrains Mono',monospace;color:#86efac;}
  .fj-mfd .title{font-size:10px;letter-spacing:0.3em;border-bottom:1px solid #1f3a1f;padding-bottom:4px;margin-bottom:8px;color:#fbbf24;}
  .fj-mfd .row{display:flex;justify-content:space-between;font-size:11px;padding:2px 0;}
  .fj-mfd .row .v{color:#bbf7d0;font-weight:700;}
  .fj-throttle{position:absolute;right:10px;bottom:10px;width:50px;height:120px;background:rgba(0,30,0,0.5);border:1px solid #86efac;border-radius:6px;padding:4px;display:flex;flex-direction:column-reverse;}
  .fj-throttle-fill{height:65%;background:linear-gradient(0deg,#86efac,#22c55e);border-radius:3px;box-shadow:0 0 8px #86efac;}
</style>
<div class="fj-stage">
  <!-- "View" — sky over ground horizon -->
  <!-- HUD overlay -->
  <div class="fj-hud-overlay">
    <!-- Top center: heading tape -->
    <div style="position:absolute;left:50%;top:14px;transform:translateX(-50%);width:200px;border:1px solid #86efac;background:rgba(0,30,0,0.5);text-align:center;padding:3px;font-size:11px;color:#86efac;text-shadow:0 0 4px #86efac;letter-spacing:0.2em;">120° — N — 130° — 140°</div>
    <!-- Left tape: airspeed -->
    <div class="fj-tape" style="left:18px;top:50%;transform:translateY(-50%);"><div class="l">SPD</div><div class="v">42</div><div class="l">KTS</div></div>
    <!-- Right tape: altitude -->
    <div class="fj-tape" style="right:80px;top:50%;transform:translateY(-50%);"><div class="l">ALT</div><div class="v">12.4</div><div class="l">cm</div></div>
    <!-- Pitch ladder -->
    <svg class="fj-pitch-ladder" viewBox="0 0 800 520" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;">
      <line x1="280" y1="180" x2="520" y2="180"/>
      <text x="270" y="184" text-anchor="end">10</text>
      <line x1="320" y1="220" x2="480" y2="220"/>
      <line x1="280" y1="260" x2="380" y2="260"/>
      <line x1="420" y1="260" x2="520" y2="260"/>
      <text x="270" y="264" text-anchor="end">5</text>
      <line x1="320" y1="300" x2="480" y2="300"/>
      <line x1="240" y1="340" x2="360" y2="340"/>
      <line x1="440" y1="340" x2="560" y2="340"/>
      <text x="230" y="344" text-anchor="end">−5</text>
    </svg>
    <!-- Center reticle -->
    <div class="fj-reticle">
      <svg viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="20"/>
        <line x1="0" y1="50" x2="30" y2="50"/>
        <line x1="70" y1="50" x2="100" y2="50"/>
        <line x1="50" y1="0" x2="50" y2="20"/>
        <line x1="50" y1="80" x2="50" y2="100"/>
        <circle cx="50" cy="50" r="2" fill="#86efac"/>
      </svg>
    </div>
    <!-- Throttle -->
    <div class="fj-throttle">
      <div class="fj-throttle-fill"></div>
    </div>
    <div style="position:absolute;right:18px;bottom:140px;font-size:9px;color:#86efac;letter-spacing:0.2em;">THR 65%</div>
    <!-- Bottom annunciator strip -->
    <div style="position:absolute;left:14px;bottom:14px;display:flex;gap:8px;font-size:9px;letter-spacing:0.15em;">
      <span style="color:#22c55e;text-shadow:0 0 6px #22c55e;">● BLE</span>
      <span style="color:#22c55e;text-shadow:0 0 6px #22c55e;">● PWR</span>
      <span style="color:#fbbf24;text-shadow:0 0 6px #fbbf24;">● ECHO</span>
      <span style="color:#86efac">○ SVO</span>
      <span style="color:#86efac">○ LIN</span>
      <span style="color:#86efac">○ IR</span>
      <span style="color:#22c55e;text-shadow:0 0 6px #22c55e;">● MIC</span>
    </div>
  </div>
</div>
<div class="fj-bottom">
  <div class="fj-mfd">
    <div class="title">MFD · ENGINES</div>
    <div class="row"><span>N1 LEFT</span><span class="v">62%</span></div>
    <div class="row"><span>N1 RIGHT</span><span class="v">68%</span></div>
    <div class="row"><span>TEMP</span><span class="v">23.4°C</span></div>
    <div class="row"><span>FUEL</span><span class="v">78% · 4.02V</span></div>
    <div class="row"><span>MIC</span><span class="v">▮▮▮▮▯</span></div>
  </div>
  <div class="fj-mfd">
    <div class="title">MFD · NAVIGATION</div>
    <svg viewBox="0 0 200 130" style="width:100%">
      <circle cx="100" cy="80" r="58" fill="none" stroke="#1f3a1f" stroke-width="1"/>
      <circle cx="100" cy="80" r="38" fill="none" stroke="#1f3a1f" stroke-width="0.8"/>
      <circle cx="100" cy="80" r="18" fill="none" stroke="#1f3a1f" stroke-width="0.6"/>
      <g style="transform-origin:100px 80px;animation:spin 3s linear infinite;">
        <path d="M 100 80 L 100 22 A 58 58 0 0 1 150 50 Z" fill="#86efac" opacity="0.25"/>
      </g>
      <circle cx="130" cy="55" r="3" fill="#fbbf24"/>
      <text x="100" y="20" text-anchor="middle" fill="#86efac" font-size="9" font-family="monospace">N</text>
      <text x="100" y="125" text-anchor="middle" fill="#86efac" font-size="8" font-family="monospace">RANGE 2 m</text>
    </svg>
  </div>
  <div class="fj-mfd">
    <div class="title">MFD · UART TRACE</div>
    <pre style="font-size:9px;color:#86efac;line-height:1.4;margin:0;">&gt; #41 SRV:1,90
&lt; ECHO:41 SRV:1,90
&gt; #42 DIST?
&lt; DIST:42
&gt; #43 LINE?
&lt; LINE:1,1
&gt; #44 ACC?
&lt; ACC:124,-38,992
&gt; #45 SRV:1,90</pre>
  </div>
</div>
<style>@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}</style>
''',
        bg='#000300')


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #4 — F1 STEERING WHEEL                                            ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_4():
    nav = nav_bar(4, 'F1 Steering Wheel', '🏎', 'rev lights · gear · sectors · paddles',
                  accent='#dc2626', dim='#3a0a0a', text='#fee2e2', bg='#0a0a0a')
    return base_html('🏎 #4 F1 Wheel',
        nav + '''
<style>
  .f1-rev-bar{display:flex;gap:4px;justify-content:center;margin-bottom:14px;padding:8px;background:#000;border:2px solid #3a0a0a;border-radius:10px;}
  .f1-rev{width:16px;height:18px;border-radius:3px;background:#1a1a1a;}
  .f1-rev.on-1{background:#22c55e;box-shadow:0 0 6px #22c55e;}
  .f1-rev.on-2{background:#86efac;box-shadow:0 0 6px #86efac;}
  .f1-rev.on-3{background:#fbbf24;box-shadow:0 0 6px #fbbf24;}
  .f1-rev.on-4{background:#f97316;box-shadow:0 0 6px #f97316;}
  .f1-rev.on-5{background:#dc2626;box-shadow:0 0 8px #dc2626;animation:flash 0.4s ease-in-out infinite alternate;}
  @keyframes flash{from{opacity:1}to{opacity:0.4}}

  .f1-grid{display:grid;grid-template-columns:1fr 2.2fr 1fr;gap:14px;}
  @media(max-width:920px){.f1-grid{grid-template-columns:1fr;}}

  .f1-side{display:flex;flex-direction:column;gap:10px;}
  .f1-card{background:#1a1a1a;border:2px solid #3a0a0a;border-radius:10px;padding:12px;}
  .f1-card .l{font-size:9px;color:#fca5a5;letter-spacing:0.2em;font-family:'JetBrains Mono',monospace;margin-bottom:6px;}
  .f1-card .v{font-size:32px;font-weight:900;color:#dc2626;text-shadow:0 0 10px #dc2626;font-family:'JetBrains Mono',monospace;}
  .f1-card .v.green{color:#22c55e;text-shadow:0 0 10px #22c55e;}
  .f1-card .v.amber{color:#fbbf24;text-shadow:0 0 10px #fbbf24;}

  .f1-wheel-wrap{background:#000;border:3px solid #1a1a1a;border-radius:14px;padding:20px;display:flex;flex-direction:column;align-items:center;gap:14px;position:relative;}
  .f1-wheel{width:340px;height:340px;max-width:100%;position:relative;background:radial-gradient(circle at 50% 50%,#1a1a1a 30%,#0a0a0a 60%,#000 100%);border:6px solid #2a2a2a;border-radius:50% 50% 30% 30% / 50% 50% 50% 50%;clip-path:path('M 170 0 A 170 170 0 0 1 340 170 L 340 280 Q 340 340 280 340 L 60 340 Q 0 340 0 280 L 0 170 A 170 170 0 0 1 170 0 Z');box-shadow:inset 0 0 40px rgba(0,0,0,0.9),0 0 30px rgba(220,38,38,0.2);}
  .f1-wheel .center-display{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:140px;height:80px;background:#000;border:2px solid #444;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;}
  .f1-wheel .center-display .gear{font-size:42px;font-weight:900;color:#fbbf24;text-shadow:0 0 14px #fbbf24;line-height:1;}
  .f1-wheel .center-display .speed{font-size:14px;color:#22c55e;text-shadow:0 0 6px #22c55e;}
  .f1-wheel .knob{position:absolute;width:34px;height:34px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#444,#0a0a0a);border:2px solid #555;box-shadow:0 0 6px rgba(220,38,38,0.3);}
  .f1-wheel .knob.tl{top:50px;left:42px;}
  .f1-wheel .knob.tr{top:50px;right:42px;}
  .f1-wheel .knob.bl{bottom:50px;left:60px;}
  .f1-wheel .knob.br{bottom:50px;right:60px;}
  .f1-wheel .btn{position:absolute;width:24px;height:24px;border-radius:6px;background:#dc2626;box-shadow:0 0 8px #dc2626;}
  .f1-wheel .btn.t{top:120px;left:50%;transform:translateX(-50%);}
  .f1-wheel .btn.bl{bottom:120px;left:50%;transform:translateX(-80px);background:#22c55e;box-shadow:0 0 8px #22c55e;}
  .f1-wheel .btn.br{bottom:120px;left:50%;transform:translateX(56px);background:#fbbf24;box-shadow:0 0 8px #fbbf24;}

  .f1-paddle{background:linear-gradient(135deg,#444,#1a1a1a);border:2px solid #555;border-radius:6px;padding:14px 20px;font-family:'JetBrains Mono',monospace;font-weight:900;color:#fee2e2;letter-spacing:0.2em;font-size:11px;}
  .f1-paddles{display:flex;justify-content:space-between;width:100%;}

  .f1-sectors{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px;}
  .f1-sector{background:#1a1a1a;border:1px solid #3a0a0a;border-radius:6px;padding:10px;text-align:center;font-family:'JetBrains Mono',monospace;}
  .f1-sector .name{font-size:10px;color:#fca5a5;}
  .f1-sector.s1{border-color:#22c55e;}
  .f1-sector.s2{border-color:#fbbf24;}
  .f1-sector.s3{border-color:#dc2626;}
  .f1-sector .time{font-size:18px;font-weight:800;color:#fee2e2;margin-top:4px;}
</style>
<div class="f1-rev-bar">
  <span class="f1-rev on-1"></span><span class="f1-rev on-1"></span><span class="f1-rev on-1"></span>
  <span class="f1-rev on-2"></span><span class="f1-rev on-2"></span><span class="f1-rev on-2"></span>
  <span class="f1-rev on-3"></span><span class="f1-rev on-3"></span><span class="f1-rev on-3"></span>
  <span class="f1-rev on-4"></span><span class="f1-rev on-4"></span><span class="f1-rev on-4"></span>
  <span class="f1-rev on-5"></span><span class="f1-rev"></span><span class="f1-rev"></span>
  <span class="f1-rev"></span><span class="f1-rev"></span>
</div>
<div class="f1-grid">
  <div class="f1-side">
    <div class="f1-card"><div class="l">⏱ SPEED</div><div class="v">42</div></div>
    <div class="f1-card"><div class="l">📡 DIST · cm</div><div class="v green">12.4</div></div>
    <div class="f1-card"><div class="l">🌡 ENGINE TEMP</div><div class="v amber">23.4°</div></div>
    <div class="f1-card"><div class="l">🔋 BATTERY</div><div class="v green">78%</div></div>
  </div>
  <div class="f1-wheel-wrap">
    <div class="f1-wheel">
      <div class="knob tl"></div><div class="knob tr"></div>
      <div class="knob bl"></div><div class="knob br"></div>
      <div class="btn t"></div>
      <div class="btn bl"></div><div class="btn br"></div>
      <div class="center-display">
        <div class="gear">3</div>
        <div class="speed">42 KPH</div>
      </div>
    </div>
    <div class="f1-paddles">
      <div class="f1-paddle">‹ DOWN</div>
      <div class="f1-paddle">UP ›</div>
    </div>
    <div class="f1-sectors" style="width:100%;">
      <div class="f1-sector s1"><div class="name">S1</div><div class="time">12.34</div></div>
      <div class="f1-sector s2"><div class="name">S2</div><div class="time">14.67</div></div>
      <div class="f1-sector s3"><div class="name">S3</div><div class="time">−.−−</div></div>
    </div>
  </div>
  <div class="f1-side">
    <div class="f1-card"><div class="l">🧭 HEADING</div><div class="v">120°</div></div>
    <div class="f1-card"><div class="l">📐 G-FORCE · X·Y·Z</div><div class="v" style="font-size:14px">0.12 / −0.04 / 0.99</div></div>
    <div class="f1-card"><div class="l">🔊 MIC LEVEL</div><div class="v" style="font-size:18px">▮▮▮▮▯▯▯▯</div></div>
    <div class="f1-card" style="background:#000;"><div class="l">📺 RADIO · TEAM</div><pre style="font-size:9px;color:#fca5a5;line-height:1.4;margin:0;">&gt; BOX BOX
&lt; COPY
&gt; TYRES OK
&lt; CONFIRM</pre></div>
  </div>
</div>
''',
        bg='#0a0a0a')


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #5 — SUBMARINE HELM (periscope + sonar + depth ladder)            ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_5():
    nav = nav_bar(5, 'Submarine Helm', '🚢', 'periscope · sonar · depth · brass',
                  accent='#dc2626', dim='#5c2c10', text='#fca5a5', bg='#0a0202')
    return base_html('🚢 #5 Submarine',
        nav + '''
<style>
  body::after{content:'';position:fixed;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 30%,rgba(0,0,0,0.7));z-index:9998;}
  .sub-grid{display:grid;grid-template-columns:140px 1fr 200px;grid-template-rows:auto auto;gap:14px;max-width:1200px;margin:0 auto;}
  @media(max-width:820px){.sub-grid{grid-template-columns:1fr;}}
  .sub-periscope{grid-column:2;background:radial-gradient(circle at 50% 45%,#1a3a4a 0%,#0a1622 60%,#000 100%);border:6px solid #5c2c10;border-radius:50%;aspect-ratio:1;max-width:480px;margin:0 auto;position:relative;box-shadow:inset 0 0 60px rgba(0,0,0,0.9),0 0 30px rgba(220,38,38,0.2);}
  .sub-periscope::before{content:'';position:absolute;inset:8px;border:2px solid #92400e;border-radius:50%;}
  .sub-periscope .crosshair{position:absolute;inset:0;}
  .sub-periscope .crosshair::before,.sub-periscope .crosshair::after{content:'';position:absolute;background:rgba(220,38,38,0.6);box-shadow:0 0 8px #dc2626;}
  .sub-periscope .crosshair::before{left:50%;top:14%;bottom:14%;width:1.5px;transform:translateX(-50%);}
  .sub-periscope .crosshair::after{top:50%;left:14%;right:14%;height:1.5px;transform:translateY(-50%);}
  .sub-periscope .target{position:absolute;left:62%;top:42%;width:32px;height:32px;border:2px solid #fbbf24;border-radius:4px;animation:targetPulse 2s ease-in-out infinite;}
  @keyframes targetPulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.5;transform:scale(1.15)}}
  .sub-periscope .horizon{position:absolute;left:14%;right:14%;top:50%;height:1px;background:rgba(255,255,255,0.2);}
  .sub-periscope .reading{position:absolute;font-family:'Courier New',monospace;color:#dc2626;font-size:10px;text-shadow:0 0 4px #dc2626;letter-spacing:0.1em;}

  .sub-depth{grid-column:1;grid-row:1;background:linear-gradient(180deg,#3d1a1a,#0a0202);border:3px solid #92400e;border-radius:10px;padding:14px 8px;height:480px;display:flex;flex-direction:column;align-items:center;}
  .sub-depth .lbl{font-size:9px;color:#fca5a5;letter-spacing:0.2em;margin-bottom:8px;font-family:'Courier New',monospace;}
  .sub-depth .ladder{flex:1;width:30px;background:repeating-linear-gradient(0deg,#92400e 0,#92400e 1px,transparent 1px,transparent 16px);border-left:1px solid #5c2c10;border-right:1px solid #5c2c10;position:relative;}
  .sub-depth .needle{position:absolute;left:-8px;right:-8px;height:3px;background:#fbbf24;box-shadow:0 0 6px #fbbf24;top:30%;}
  .sub-depth .val{font-size:20px;color:#fbbf24;font-weight:800;text-shadow:0 0 8px #fbbf24;font-family:'Courier New',monospace;margin-top:6px;}

  .sub-side{grid-column:3;grid-row:1;display:flex;flex-direction:column;gap:8px;}
  .sub-dial{background:radial-gradient(circle,#3d1a1a 60%,#1a0808 100%);border:4px solid #92400e;border-radius:50%;aspect-ratio:1;position:relative;display:grid;place-items:center;box-shadow:inset 0 0 18px rgba(0,0,0,0.9),0 0 8px rgba(220,38,38,0.2);}
  .sub-dial .l{position:absolute;top:8px;font-size:8px;color:#fca5a5;letter-spacing:0.2em;font-family:'Courier New',monospace;font-weight:700;text-align:center;width:100%;}
  .sub-dial .v{font-size:16px;color:#fbbf24;font-weight:800;text-shadow:0 0 6px #fbbf24;font-family:'Courier New',monospace;}
  .sub-dial::before{content:'';position:absolute;width:2px;height:35%;background:#fbbf24;top:12%;left:calc(50% - 1px);transform-origin:bottom center;transform:rotate(45deg);box-shadow:0 0 4px #fbbf24;}

  .sub-sonar{grid-column:1 / -1;background:#000300;border:3px solid #92400e;border-radius:10px;padding:14px;}
  .sub-sonar .title{font-family:'Courier New',monospace;color:#dc2626;font-size:11px;letter-spacing:0.3em;margin-bottom:10px;text-shadow:0 0 6px #dc2626;}
  .sub-sonar svg{display:block;width:100%;max-height:240px;margin:0 auto;}
  .sub-sonar circle{fill:none;stroke:#5c2c10;}
  .sub-sonar .sweep{transform-origin:center;animation:spin 4s linear infinite;}
  .sub-sonar .blip{fill:#fbbf24;filter:drop-shadow(0 0 6px #fbbf24);animation:blipPulse 2s ease-in-out infinite;}
  @keyframes blipPulse{0%,100%{opacity:1}50%{opacity:0.4}}
  @keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}

  .sub-status{grid-column:1 / -1;display:grid;grid-template-columns:repeat(8,1fr);gap:6px;background:#3d1a1a;border:2px solid #92400e;border-radius:8px;padding:10px;}
  .sub-status .light{padding:8px 4px;text-align:center;border-radius:4px;background:rgba(0,0,0,0.4);font-family:'Courier New',monospace;font-size:9px;font-weight:800;letter-spacing:0.1em;color:#5c2c10;border:1px solid #5c2c10;}
  .sub-status .light.on{background:#dc2626;color:#fee2e2;box-shadow:0 0 8px #dc2626;animation:annPulse 2.4s ease-in-out infinite;}
  @keyframes annPulse{0%,100%{opacity:1}50%{opacity:0.65}}
</style>
<div class="sub-grid">
  <div class="sub-depth">
    <div class="lbl">DEPTH · m</div>
    <div class="ladder"><div class="needle"></div></div>
    <div class="val">12.4</div>
  </div>
  <div class="sub-periscope">
    <div class="crosshair"></div>
    <div class="target"></div>
    <div class="horizon"></div>
    <div class="reading" style="left:8%;top:8%;">HDG 120°</div>
    <div class="reading" style="right:8%;top:8%;">SPD 42</div>
    <div class="reading" style="left:8%;bottom:8%;">DIST 12.4 m</div>
    <div class="reading" style="right:8%;bottom:8%;">TEMP 23.4°</div>
  </div>
  <div class="sub-side">
    <div class="sub-dial"><div class="l">SPEED</div><div class="v">42</div></div>
    <div class="sub-dial"><div class="l">HEADING</div><div class="v">120°</div></div>
    <div class="sub-dial"><div class="l">BATTERY</div><div class="v">78%</div></div>
  </div>
  <div class="sub-sonar">
    <div class="title">⎯ SONAR ⎯ SCAN ACTIVE ⎯ MIC ▮▮▮▮▯▯ ⎯ ACC 0.12·−0.04·0.99 ⎯</div>
    <svg viewBox="0 0 800 220" preserveAspectRatio="xMidYMid meet">
      <line x1="0" y1="110" x2="800" y2="110" stroke="#5c2c10" stroke-width="0.5"/>
      <line x1="400" y1="0" x2="400" y2="220" stroke="#5c2c10" stroke-width="0.5"/>
      <ellipse cx="400" cy="110" rx="380" ry="100" stroke-width="1"/>
      <ellipse cx="400" cy="110" rx="280" ry="74" stroke-width="0.8"/>
      <ellipse cx="400" cy="110" rx="180" ry="48" stroke-width="0.6"/>
      <ellipse cx="400" cy="110" rx="80" ry="22" stroke-width="0.4"/>
      <g class="sweep" style="transform-origin:400px 110px">
        <path d="M 400 110 L 400 10 A 380 100 0 0 1 700 70 Z" fill="#dc2626" opacity="0.25"/>
      </g>
      <circle cx="540" cy="74" r="6" class="blip"/>
      <circle cx="280" cy="146" r="4" class="blip" style="animation-delay:0.6s"/>
      <text x="400" y="216" text-anchor="middle" fill="#dc2626" font-family="monospace" font-size="10" letter-spacing="3">⎯ RANGE: 2 m ⎯ BEARING: 045 ⎯ CONTACT: 1 ⎯</text>
    </svg>
  </div>
  <div class="sub-status">
    <div class="light on">BLE</div><div class="light on">PWR</div><div class="light">ECHO</div>
    <div class="light on">SVO</div><div class="light">LIN</div><div class="light">IR</div>
    <div class="light on">MIC</div><div class="light">ALARM</div>
  </div>
</div>
''',
        bg='#0a0202', font="'Courier New', monospace")


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #6 — STARSHIP BRIDGE (LCARS-style asymmetric)                     ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_6():
    nav = nav_bar(6, 'Starship Bridge', '🛸', 'viewscreen · LCARS · stations',
                  accent='#fb923c', dim='#7c3aed', text='#fbbf24', bg='#000000')
    return base_html('🛸 #6 Starship Bridge',
        nav + '''
<style>
  .ss-grid{display:grid;grid-template-columns:80px 1fr 80px;grid-template-rows:auto auto;gap:8px;max-width:1300px;margin:0 auto;}
  .ss-elbow-l{grid-column:1;grid-row:1 / -1;background:linear-gradient(180deg,#fb923c 0%,#fb923c 50%,#7c3aed 50%,#7c3aed 100%);border-radius:40px 0 0 40px;padding:14px 0;display:flex;flex-direction:column;gap:4px;align-items:flex-end;}
  .ss-elbow-r{grid-column:3;grid-row:1 / -1;background:linear-gradient(180deg,#7c3aed 0%,#7c3aed 50%,#fb923c 50%,#fb923c 100%);border-radius:0 40px 40px 0;padding:14px 0;display:flex;flex-direction:column;gap:4px;align-items:flex-start;}
  .ss-pill{height:24px;width:60px;border-radius:0;background:#000;display:flex;align-items:center;justify-content:center;color:#fbbf24;font-size:9px;font-weight:900;font-family:'Antonio',sans-serif;letter-spacing:0.1em;}
  .ss-pill.amber{color:#fb923c}
  .ss-pill.violet{color:#a78bfa}
  .ss-pill.cyan{color:#67e8f9}

  .ss-viewscreen{grid-column:2;grid-row:1;background:radial-gradient(ellipse at 50% 50%,#0a1828 30%,#000 70%);border-radius:0 0 40px 40px;padding:24px 14px 30px;min-height:340px;position:relative;overflow:hidden;}
  .ss-viewscreen::before{content:'⎯ VIEWSCREEN — DEEP SPACE ⎯';position:absolute;left:0;right:0;top:8px;text-align:center;color:#fb923c;font-family:'Antonio',sans-serif;font-size:11px;letter-spacing:0.3em;font-weight:900;}
  .ss-stars{position:absolute;inset:0;background-image:radial-gradient(2px 2px at 20% 30%,#fff,transparent),radial-gradient(1px 1px at 60% 20%,#fff,transparent),radial-gradient(2px 2px at 80% 60%,#67e8f9,transparent),radial-gradient(1px 1px at 30% 80%,#fff,transparent),radial-gradient(2px 2px at 70% 75%,#a78bfa,transparent),radial-gradient(1px 1px at 50% 50%,#fff,transparent);animation:starsDrift 12s linear infinite;}
  @keyframes starsDrift{from{transform:translateX(0)}to{transform:translateX(-100px)}}
  .ss-planet{position:absolute;left:50%;bottom:50px;transform:translateX(-50%);width:140px;height:140px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fb923c 10%,#7c2d12 60%,#000 100%);box-shadow:0 0 40px rgba(251,146,60,0.4);}
  .ss-radar{position:absolute;right:14px;top:34px;width:100px;height:100px;border-radius:50%;border:2px solid #67e8f9;background:rgba(0,0,0,0.6);}
  .ss-radar svg{width:100%;height:100%;}
  .ss-bottom{grid-column:2;grid-row:2;display:grid;grid-template-columns:1fr 1.4fr 1fr;gap:8px;background:#000;border-radius:30px 30px 0 0;padding:18px;}
  .ss-station{background:#0a0a0a;border-radius:8px;padding:10px;}
  .ss-station h3{font-family:'Antonio',sans-serif;font-size:14px;color:#fb923c;letter-spacing:0.2em;margin-bottom:8px;}
  .ss-station h3.violet{color:#a78bfa;}
  .ss-station h3.cyan{color:#67e8f9;}
  .ss-row{display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #1a1a1a;font-family:'Antonio',sans-serif;font-size:11px;}
  .ss-row .l{color:#666;letter-spacing:0.1em;}
  .ss-row .v{color:#fbbf24;font-weight:900;}
  .ss-bar{display:flex;gap:2px;margin-top:6px;}
  .ss-bar .b{flex:1;height:14px;background:#0a0a0a;}
  .ss-bar .b.on{background:#fb923c;box-shadow:0 0 4px #fb923c;}
</style>
<div class="ss-grid">
  <div class="ss-elbow-l">
    <div class="ss-pill">⎯ HELM</div>
    <div class="ss-pill">SCI</div>
    <div class="ss-pill">⎯ ENG</div>
    <div class="ss-pill">TAC</div>
    <div class="ss-pill">⎯ COM</div>
    <div class="ss-pill">MED</div>
  </div>
  <div class="ss-viewscreen">
    <div class="ss-stars"></div>
    <div class="ss-planet"></div>
    <div class="ss-radar">
      <svg viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="46" fill="none" stroke="#67e8f9" stroke-width="0.5"/>
        <circle cx="50" cy="50" r="30" fill="none" stroke="#67e8f9" stroke-width="0.4"/>
        <circle cx="50" cy="50" r="14" fill="none" stroke="#67e8f9" stroke-width="0.3"/>
        <g style="transform-origin:center;animation:spin 3s linear infinite;">
          <path d="M 50 50 L 50 4 A 46 46 0 0 1 88 30 Z" fill="#67e8f9" opacity="0.3"/>
        </g>
        <circle cx="68" cy="32" r="2" fill="#fb923c"/>
      </svg>
    </div>
  </div>
  <div class="ss-elbow-r">
    <div class="ss-pill amber">SPD ⎯</div>
    <div class="ss-pill violet">HDG</div>
    <div class="ss-pill cyan">DIST ⎯</div>
    <div class="ss-pill amber">TEMP</div>
    <div class="ss-pill violet">PWR ⎯</div>
    <div class="ss-pill cyan">MIC</div>
  </div>
  <div class="ss-bottom">
    <div class="ss-station">
      <h3 class="violet">▸ TACTICAL</h3>
      <div class="ss-row"><span class="l">SHIELDS</span><span class="v">100%</span></div>
      <div class="ss-row"><span class="l">PHASERS</span><span class="v" style="color:#22c55e">READY</span></div>
      <div class="ss-row"><span class="l">TORPEDOES</span><span class="v">8</span></div>
      <div class="ss-row"><span class="l">TARGETS</span><span class="v">1</span></div>
    </div>
    <div class="ss-station">
      <h3>▸ HELM · NAVIGATION</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
        <div>
          <div class="ss-row"><span class="l">SPEED</span><span class="v">42 KTS</span></div>
          <div class="ss-row"><span class="l">HEADING</span><span class="v">120°</span></div>
          <div class="ss-row"><span class="l">DIST</span><span class="v">12.4 m</span></div>
        </div>
        <div>
          <div class="ss-row"><span class="l">TEMP</span><span class="v">23.4°C</span></div>
          <div class="ss-row"><span class="l">ACC</span><span class="v" style="font-size:9px">0.12·−.04·.99</span></div>
          <div class="ss-row"><span class="l">MIC</span><span class="v">▮▮▮▮▯</span></div>
        </div>
      </div>
      <div class="ss-bar"><div class="b on"></div><div class="b on"></div><div class="b on"></div><div class="b on"></div><div class="b on"></div><div class="b on"></div><div class="b"></div><div class="b"></div></div>
      <div style="font-size:9px;color:#fb923c;margin-top:4px;letter-spacing:0.2em;">▸ THROTTLE 75%</div>
    </div>
    <div class="ss-station">
      <h3 class="cyan">▸ ENGINEERING</h3>
      <div class="ss-row"><span class="l">WARP CORE</span><span class="v" style="color:#22c55e">STABLE</span></div>
      <div class="ss-row"><span class="l">BATTERY</span><span class="v">78%</span></div>
      <div class="ss-row"><span class="l">BLE LINK</span><span class="v" style="color:#22c55e">●</span></div>
      <div class="ss-row"><span class="l">UART RX</span><span class="v" style="color:#fbbf24">●</span></div>
    </div>
  </div>
</div>
<style>@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}</style>
''',
        bg='#000', font="'Antonio', 'Helvetica Neue', sans-serif")


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #7 — MECH HUD (targeting brackets + weapon tiles)                 ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_7():
    nav = nav_bar(7, 'Mech HUD (Pacific Rim)', '🤖', 'targeting brackets · weapons · threats',
                  accent='#f97316', dim='#7c2d12', text='#fed7aa', bg='#0a0a0a')
    return base_html('🤖 #7 Mech HUD',
        nav + '''
<style>
  .mech-grid{display:grid;grid-template-columns:200px 1fr 200px;gap:10px;max-width:1300px;margin:0 auto;}
  @media(max-width:920px){.mech-grid{grid-template-columns:1fr;}}
  .mech-side{display:flex;flex-direction:column;gap:8px;}
  .mech-tile{background:linear-gradient(135deg,#1a1a1a,#0a0a0a);border:1px solid #f97316;border-radius:0;padding:10px;clip-path:polygon(0 0,100% 0,100% 92%,92% 100%,0 100%);position:relative;}
  .mech-tile::before{content:'';position:absolute;left:0;top:0;width:14px;height:2px;background:#f97316;}
  .mech-tile::after{content:'';position:absolute;left:0;top:0;width:2px;height:14px;background:#f97316;}
  .mech-tile .name{font-family:'JetBrains Mono',monospace;font-size:10px;color:#f97316;letter-spacing:0.2em;font-weight:900;}
  .mech-tile .v{font-family:'JetBrains Mono',monospace;font-size:24px;color:#fed7aa;font-weight:900;text-shadow:0 0 8px #f97316;margin-top:4px;}
  .mech-tile .sub{font-size:9px;color:#7c2d12;letter-spacing:0.1em;margin-top:2px;}
  .mech-tile .bar{height:6px;background:#3a1a0a;margin-top:6px;border:1px solid #7c2d12;}
  .mech-tile .bar-fill{height:100%;background:linear-gradient(90deg,#f97316,#fbbf24);box-shadow:0 0 6px #f97316;}
  .mech-tile.live{animation:tilePulse 3s ease-in-out infinite;}
  @keyframes tilePulse{0%,100%{box-shadow:0 0 0 rgba(249,115,22,0)}50%{box-shadow:0 0 14px rgba(249,115,22,0.5)}}

  .mech-stage{position:relative;height:580px;background:radial-gradient(ellipse at 50% 50%,#1a0a00 0%,#000 80%);border:2px solid #7c2d12;overflow:hidden;}
  @media(max-width:540px){.mech-stage{height:380px;}}
  .mech-bracket{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:340px;height:340px;}
  .mech-bracket .corner{position:absolute;width:60px;height:60px;border:3px solid #f97316;filter:drop-shadow(0 0 6px #f97316);}
  .mech-bracket .tl{top:0;left:0;border-right:none;border-bottom:none;}
  .mech-bracket .tr{top:0;right:0;border-left:none;border-bottom:none;}
  .mech-bracket .bl{bottom:0;left:0;border-right:none;border-top:none;}
  .mech-bracket .br{bottom:0;right:0;border-left:none;border-top:none;}
  .mech-bracket .center{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:60px;height:60px;}
  .mech-bracket .center::before,.mech-bracket .center::after{content:'';position:absolute;background:#f97316;box-shadow:0 0 6px #f97316;}
  .mech-bracket .center::before{left:50%;top:0;bottom:0;width:1.5px;transform:translateX(-50%);}
  .mech-bracket .center::after{top:50%;left:0;right:0;height:1.5px;transform:translateY(-50%);}
  .mech-bracket .target-id{position:absolute;left:100%;top:0;margin-left:14px;font-family:'JetBrains Mono',monospace;color:#f97316;font-size:11px;letter-spacing:0.15em;line-height:1.5;}
  .mech-mech-silhouette{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:120px;height:200px;background:linear-gradient(180deg,rgba(124,45,18,0.5),rgba(0,0,0,0.8));border-radius:30px 30px 8px 8px;animation:targetSway 4s ease-in-out infinite;}
  @keyframes targetSway{0%,100%{transform:translate(-50%,-50%) rotate(-2deg)}50%{transform:translate(-50%,-50%) rotate(2deg)}}

  .mech-overlay-top{position:absolute;left:14px;top:14px;right:14px;display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;color:#f97316;font-size:11px;letter-spacing:0.2em;text-shadow:0 0 4px #f97316;}
  .mech-overlay-bot{position:absolute;left:14px;bottom:14px;right:14px;font-family:'JetBrains Mono',monospace;color:#f97316;font-size:10px;line-height:1.6;text-shadow:0 0 3px #f97316;}
  .mech-chevron{display:inline-block;color:#fbbf24;animation:hazard 1.5s ease-in-out infinite;}
  @keyframes hazard{0%,100%{opacity:1}50%{opacity:0.3}}

  .mech-ann-strip{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;margin-top:10px;background:#0a0a0a;padding:8px;border:1px solid #7c2d12;}
  .mech-ann{padding:6px 4px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:0.1em;font-weight:900;clip-path:polygon(0 0,100% 0,90% 100%,0 100%);}
  .mech-ann.on{background:#f97316;color:#0a0a0a;box-shadow:0 0 8px #f97316;}
  .mech-ann.off{background:#3a1a0a;color:#7c2d12;}
</style>
<div class="mech-grid">
  <div class="mech-side">
    <div class="mech-tile live"><div class="name">▸ MOTOR L</div><div class="v">+62</div><div class="sub">PWM · NOMINAL</div><div class="bar"><div class="bar-fill" style="width:62%"></div></div></div>
    <div class="mech-tile live"><div class="name">▸ MOTOR R</div><div class="v">+68</div><div class="sub">PWM · NOMINAL</div><div class="bar"><div class="bar-fill" style="width:68%"></div></div></div>
    <div class="mech-tile"><div class="name">▸ SERVO 1</div><div class="v">90°</div><div class="sub">LOCKED</div></div>
    <div class="mech-tile"><div class="name">▸ SERVO 2</div><div class="v">45°</div><div class="sub">TRACKING</div></div>
    <div class="mech-tile"><div class="name">▸ TEMP CORE</div><div class="v">23.4°</div><div class="sub" style="color:#22c55e">SAFE</div></div>
  </div>
  <div class="mech-stage">
    <div class="mech-overlay-top">
      <span>▸ DRIFT 73% · NEURAL HANDSHAKE LOCKED</span>
      <span>HDG 120°</span>
    </div>
    <div class="mech-mech-silhouette"></div>
    <div class="mech-bracket">
      <div class="corner tl"></div><div class="corner tr"></div>
      <div class="corner bl"></div><div class="corner br"></div>
      <div class="center"></div>
      <div class="target-id">▸ KAIJU<br>CAT-3<br>RANGE 12.4 m<br>BEARING 045</div>
    </div>
    <div class="mech-overlay-bot">
      <span class="mech-chevron">⚠⚠⚠</span> THREAT DETECTED · ENGAGE WHEN READY · SPEED 42 KPH<br>
      &gt; UART_RX: ECHO:41 SRV:1,90 · ECHO:42 DIST:42 · ACC:124,-38,992 · MIC:5
    </div>
  </div>
  <div class="mech-side">
    <div class="mech-tile"><div class="name">▸ DIST · SONAR</div><div class="v">12.4</div><div class="sub">m · LOCKED</div></div>
    <div class="mech-tile"><div class="name">▸ MIC · SOUND</div><div class="v">▮▮▮▮▯</div><div class="sub">−12 dB</div></div>
    <div class="mech-tile"><div class="name">▸ ACC · X·Y·Z</div><div class="v" style="font-size:11px">0.12·−.04·.99</div><div class="sub">G-FORCE</div></div>
    <div class="mech-tile live"><div class="name">▸ BATTERY</div><div class="v">78%</div><div class="sub">4.02 V · 92 min</div><div class="bar"><div class="bar-fill" style="width:78%"></div></div></div>
    <div class="mech-tile"><div class="name">▸ COMMS · UART</div><div class="v" style="font-size:14px">42 / 41</div><div class="sub">SENT / ECHO</div></div>
  </div>
</div>
<div class="mech-ann-strip">
  <div class="mech-ann on">BLE</div>
  <div class="mech-ann on">PWR</div>
  <div class="mech-ann on">DRIFT</div>
  <div class="mech-ann on">SVO</div>
  <div class="mech-ann off">LIN</div>
  <div class="mech-ann off">IR</div>
  <div class="mech-ann on">MIC</div>
  <div class="mech-ann off">ALERT</div>
</div>
''',
        bg='#0a0a0a')


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #8 — DJ BOOTH (twin turntables + crossfader)                     ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_8():
    nav = nav_bar(8, 'DJ Booth', '🎧', 'twin decks · crossfader · waveforms · neon',
                  accent='#ec4899', dim='#581c87', text='#fbcfe8', bg='#0d0221')
    return base_html('🎧 #8 DJ Booth',
        nav + '''
<style>
  .dj-waveform{height:80px;background:#000;border:1px solid #581c87;border-radius:8px;padding:8px;margin-bottom:14px;display:flex;align-items:center;gap:2px;overflow:hidden;}
  .dj-bar{flex:1;background:linear-gradient(180deg,#ec4899,#7c3aed);min-width:2px;border-radius:1px;animation:waveform 0.8s ease-in-out infinite;}
  .dj-bar:nth-child(2n){animation-delay:0.1s;}
  .dj-bar:nth-child(3n){animation-delay:0.2s;}
  .dj-bar:nth-child(5n){animation-delay:0.3s;}
  @keyframes waveform{0%,100%{height:30%}50%{height:90%}}

  .dj-grid{display:grid;grid-template-columns:1fr 320px 1fr;gap:14px;max-width:1300px;margin:0 auto;}
  @media(max-width:920px){.dj-grid{grid-template-columns:1fr;}}

  .dj-deck{background:linear-gradient(135deg,#1a0942,#0d0221);border:2px solid #581c87;border-radius:14px;padding:18px;display:flex;flex-direction:column;align-items:center;gap:12px;}
  .dj-platter{width:260px;height:260px;border-radius:50%;background:radial-gradient(circle at 50% 50%,#1a1a1a 5%,#000 10%,#1a1a1a 11%,#000 16%,repeating-radial-gradient(circle at 50% 50%,#000 0,#0d0221 1px,#000 2px) 18%,#000 100%);position:relative;border:8px solid #1a0942;box-shadow:0 0 30px rgba(236,72,153,0.3),inset 0 0 30px rgba(0,0,0,0.9);animation:platterSpin 3s linear infinite;}
  .dj-deck.right .dj-platter{animation-duration:4s;animation-direction:reverse;}
  @keyframes platterSpin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
  .dj-platter::before{content:'';position:absolute;inset:50%;width:80px;height:80px;margin:-40px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#ec4899 30%,#7c3aed 70%,#000 100%);box-shadow:0 0 16px #ec4899;}
  .dj-platter::after{content:'';position:absolute;inset:50%;width:8px;height:8px;margin:-4px;border-radius:50%;background:#000;border:2px solid #ec4899;}
  .dj-deck-info{display:flex;justify-content:space-between;width:100%;font-family:'JetBrains Mono',monospace;font-size:11px;}
  .dj-deck-info .l{color:#a78bfa;letter-spacing:0.15em;}
  .dj-deck-info .v{color:#ec4899;font-weight:800;text-shadow:0 0 6px #ec4899;}
  .dj-pitch{width:100%;background:#000;border:1px solid #581c87;border-radius:6px;padding:8px;}
  .dj-pitch-track{width:100%;height:6px;background:#1a0942;border-radius:3px;position:relative;}
  .dj-pitch-track::before{content:'';position:absolute;left:50%;top:-4px;width:14px;height:14px;border-radius:50%;background:#ec4899;transform:translateX(-50%);box-shadow:0 0 8px #ec4899;}

  .dj-mixer{background:linear-gradient(135deg,#1a0942,#0d0221);border:2px solid #581c87;border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:14px;}
  .dj-mixer h3{font-size:11px;color:#ec4899;letter-spacing:0.3em;text-align:center;font-family:'JetBrains Mono',monospace;text-shadow:0 0 6px #ec4899;}
  .dj-eq{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
  .dj-eq-band{display:flex;flex-direction:column;align-items:center;gap:4px;}
  .dj-eq-band .lbl{font-size:8px;color:#a78bfa;letter-spacing:0.15em;font-family:'JetBrains Mono',monospace;}
  .dj-knob{width:48px;height:48px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#444,#0d0221);border:2px solid #ec4899;box-shadow:0 0 8px rgba(236,72,153,0.5);position:relative;}
  .dj-knob::before{content:'';position:absolute;left:50%;top:6px;width:2px;height:14px;background:#ec4899;transform:translateX(-50%) rotate(-45deg);transform-origin:top center;box-shadow:0 0 4px #ec4899;}
  .dj-crossfader{padding:14px 0;background:#000;border:1px solid #581c87;border-radius:8px;}
  .dj-crossfader-track{width:80%;height:6px;margin:0 auto;background:#1a0942;border-radius:3px;position:relative;}
  .dj-crossfader-handle{position:absolute;left:50%;top:-8px;width:32px;height:24px;background:linear-gradient(180deg,#ec4899,#7c3aed);transform:translateX(-50%);border-radius:4px;box-shadow:0 0 12px #ec4899;}
  .dj-crossfader-track::before{content:'A';position:absolute;left:0;top:14px;color:#a78bfa;font-size:11px;font-weight:900;}
  .dj-crossfader-track::after{content:'B';position:absolute;right:0;top:14px;color:#a78bfa;font-size:11px;font-weight:900;}
  .dj-bpm{background:#000;border:1px solid #ec4899;border-radius:8px;padding:8px;text-align:center;}
  .dj-bpm .v{font-family:'JetBrains Mono',monospace;font-size:30px;color:#ec4899;font-weight:900;text-shadow:0 0 12px #ec4899;line-height:1;}
  .dj-bpm .l{font-size:9px;color:#a78bfa;letter-spacing:0.3em;}

  .dj-mfd{margin-top:14px;background:#000;border:1px solid #581c87;border-radius:8px;padding:10px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#ec4899;}
</style>
<div class="dj-waveform">''' + ''.join('<div class="dj-bar"></div>' for _ in range(60)) + '''</div>
<div class="dj-grid">
  <div class="dj-deck left">
    <div class="dj-platter"></div>
    <div class="dj-deck-info"><span class="l">DECK A · MOTOR L</span><span class="v">+62%</span></div>
    <div class="dj-deck-info"><span class="l">SPEED</span><span class="v">42 KPH</span></div>
    <div class="dj-pitch"><div class="dj-pitch-track"></div></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#a78bfa;letter-spacing:0.2em;">PITCH ±8% · KEY LOCK</div>
  </div>

  <div class="dj-mixer">
    <h3>MIXER · MASTER</h3>
    <div class="dj-bpm"><div class="v">120</div><div class="l">BPM</div></div>
    <div class="dj-eq">
      <div class="dj-eq-band"><div class="lbl">HIGH</div><div class="dj-knob"></div></div>
      <div class="dj-eq-band"><div class="lbl">HIGH</div><div class="dj-knob"></div></div>
      <div class="dj-eq-band"><div class="lbl">MID</div><div class="dj-knob"></div></div>
      <div class="dj-eq-band"><div class="lbl">MID</div><div class="dj-knob"></div></div>
      <div class="dj-eq-band"><div class="lbl">LOW</div><div class="dj-knob"></div></div>
      <div class="dj-eq-band"><div class="lbl">LOW</div><div class="dj-knob"></div></div>
    </div>
    <div class="dj-crossfader"><div class="dj-crossfader-track"><div class="dj-crossfader-handle"></div></div></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#a78bfa;text-align:center;letter-spacing:0.2em;">CROSSFADER · BLEND</div>
    <!-- VU meters -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
      <div style="background:#000;border:1px solid #581c87;border-radius:6px;padding:6px;">
        <div style="font-size:8px;color:#a78bfa;letter-spacing:0.2em;font-family:'JetBrains Mono',monospace;">L · MIC</div>
        <div style="font-size:14px;color:#ec4899;font-family:'JetBrains Mono',monospace;text-shadow:0 0 6px #ec4899;">▮▮▮▮▮▯▯▯</div>
      </div>
      <div style="background:#000;border:1px solid #581c87;border-radius:6px;padding:6px;">
        <div style="font-size:8px;color:#a78bfa;letter-spacing:0.2em;font-family:'JetBrains Mono',monospace;">R · MIC</div>
        <div style="font-size:14px;color:#ec4899;font-family:'JetBrains Mono',monospace;text-shadow:0 0 6px #ec4899;">▮▮▮▮▯▯▯▯</div>
      </div>
    </div>
  </div>

  <div class="dj-deck right">
    <div class="dj-platter"></div>
    <div class="dj-deck-info"><span class="l">DECK B · MOTOR R</span><span class="v">+68%</span></div>
    <div class="dj-deck-info"><span class="l">HEADING</span><span class="v">120°</span></div>
    <div class="dj-pitch"><div class="dj-pitch-track"></div></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#a78bfa;letter-spacing:0.2em;">DIST 12.4 m · TEMP 23.4°</div>
  </div>
</div>
<div class="dj-mfd">▸ TRACK 41/100 · UART_RX: ECHO:41 SRV:1,90 · ECHO:42 DIST:42 · ACC:124,-38,992 · BAT 78% · BLE ●</div>
''',
        bg='#0d0221', font="'Inter', sans-serif")


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #9 — STUDIO MIXER (channel strips + faders + VU)                  ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_9():
    nav = nav_bar(9, 'Studio Mixer', '🎚', 'channel strips · faders · VU meters · master',
                  accent='#fbbf24', dim='#374151', text='#fef3c7', bg='#1a1a1a')
    return base_html('🎚 #9 Studio Mixer',
        nav + '''
<style>
  .sm-grid{display:grid;grid-template-columns:repeat(8,1fr) 1.4fr;gap:6px;max-width:1300px;margin:0 auto;}
  @media(max-width:920px){.sm-grid{grid-template-columns:repeat(4,1fr) 1.4fr;}}
  @media(max-width:540px){.sm-grid{grid-template-columns:repeat(2,1fr);}}

  .sm-strip{background:linear-gradient(180deg,#2a2a2a,#1a1a1a);border:1px solid #374151;border-radius:6px;padding:8px 6px;display:flex;flex-direction:column;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;}
  .sm-strip h4{font-size:8px;color:#fbbf24;letter-spacing:0.15em;text-align:center;font-weight:900;}
  .sm-knob{width:30px;height:30px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#666,#1a1a1a);border:1.5px solid #374151;position:relative;}
  .sm-knob::before{content:'';position:absolute;left:50%;top:4px;width:1.5px;height:8px;background:#fbbf24;transform:translateX(-50%) rotate(-30deg);transform-origin:top center;box-shadow:0 0 3px #fbbf24;}
  .sm-pan{font-size:8px;color:#9ca3af;letter-spacing:0.1em;}
  .sm-fader-track{width:14px;height:140px;background:#0a0a0a;border-radius:7px;position:relative;border:1px solid #374151;}
  .sm-fader-handle{position:absolute;left:-6px;width:26px;height:14px;background:linear-gradient(180deg,#fbbf24,#a16207);border-radius:3px;box-shadow:0 0 6px rgba(251,191,36,0.5);}
  .sm-vu{display:flex;flex-direction:column-reverse;gap:1.5px;height:120px;width:8px;border:1px solid #374151;background:#000;padding:1px;}
  .sm-vu .seg{flex:1;background:#22c55e;}
  .sm-vu .seg.med{background:#fbbf24;}
  .sm-vu .seg.hi{background:#dc2626;}
  .sm-vu .seg.off{background:#1a1a1a;}
  .sm-fader-row{display:flex;gap:6px;align-items:flex-start;}
  .sm-mute-solo{display:flex;gap:3px;}
  .sm-btn{padding:2px 5px;border:1px solid #374151;border-radius:3px;font-size:8px;font-weight:900;color:#9ca3af;}
  .sm-btn.active{background:#dc2626;color:#fff;}
  .sm-btn.solo.active{background:#fbbf24;color:#0a0a0a;}
  .sm-name{font-size:8px;color:#fef3c7;letter-spacing:0.1em;border:1px solid #374151;padding:2px 4px;text-align:center;width:100%;background:#0a0a0a;}

  .sm-master{background:linear-gradient(180deg,#3a3a3a,#1a1a1a);border:2px solid #fbbf24;border-radius:8px;padding:14px;display:flex;flex-direction:column;align-items:center;gap:10px;}
  .sm-master h3{font-size:11px;color:#fbbf24;letter-spacing:0.3em;font-weight:900;font-family:'JetBrains Mono',monospace;text-shadow:0 0 4px #fbbf24;}
  .sm-master-vu{display:flex;gap:4px;}
  .sm-master .sm-vu{height:140px;width:14px;}
  .sm-master-fader{display:flex;gap:8px;align-items:center;}
  .sm-master-fader .sm-fader-track{height:160px;width:18px;border-radius:9px;}
  .sm-master-fader .sm-fader-handle{width:34px;height:18px;}
  .sm-master-readout{background:#000;border:1px solid #fbbf24;border-radius:6px;padding:8px 12px;text-align:center;width:100%;font-family:'JetBrains Mono',monospace;}
  .sm-master-readout .v{font-size:18px;color:#fbbf24;font-weight:900;text-shadow:0 0 6px #fbbf24;}
  .sm-master-readout .l{font-size:9px;color:#9ca3af;letter-spacing:0.2em;}
</style>
<div class="sm-grid">'''
        + ''.join(f'''<div class="sm-strip">
  <h4>{name}</h4>
  <div style="font-size:7px;color:#9ca3af;">EQ</div>
  <div class="sm-knob"></div>
  <div class="sm-knob"></div>
  <div class="sm-knob"></div>
  <div class="sm-pan">PAN</div>
  <div class="sm-knob"></div>
  <div class="sm-fader-row">
    <div class="sm-fader-track"><div class="sm-fader-handle" style="bottom:{fader}%"></div></div>
    <div class="sm-vu">
      <div class="seg{' off' if i>level else ''}"></div><div class="seg{' off' if i>level-1 else ''}"></div>
      <div class="seg{' off' if i>level-2 else ''}"></div><div class="seg{' off' if i>level-3 else ''}"></div>
      <div class="seg med{' off' if i>level-4 else ''}"></div><div class="seg med{' off' if i>level-5 else ''}"></div>
      <div class="seg hi{' off' if i>level-6 else ''}"></div><div class="seg hi off"></div>
    </div>
  </div>
  <div class="sm-mute-solo"><span class="sm-btn">M</span><span class="sm-btn solo {sole}">S</span></div>
  <div class="sm-name">{val}</div>
</div>''' for i, (name, fader, level, sole, val) in enumerate([
    ('SPD',   62, 5, '',       '42'),
    ('DIST',  78, 6, 'active', '12.4'),
    ('HDG',   45, 4, '',       '120°'),
    ('TEMP',  60, 3, '',       '23.4°'),
    ('ACC',   55, 5, '',       '0.99'),
    ('MIC',   72, 7, 'active', '−12'),
    ('BAT',   78, 6, '',       '78%'),
    ('SVO',   50, 4, '',       '90°'),
])) +
'''
  <div class="sm-master">
    <h3>▸ MASTER OUT</h3>
    <div class="sm-master-vu"><div class="sm-vu"><div class="seg"></div><div class="seg"></div><div class="seg"></div><div class="seg"></div><div class="seg med"></div><div class="seg med"></div><div class="seg hi"></div><div class="seg hi off"></div></div><div class="sm-vu"><div class="seg"></div><div class="seg"></div><div class="seg"></div><div class="seg"></div><div class="seg med"></div><div class="seg med off"></div><div class="seg hi off"></div><div class="seg hi off"></div></div></div>
    <div class="sm-master-fader"><div class="sm-fader-track"><div class="sm-fader-handle" style="bottom:65%"></div></div></div>
    <div class="sm-master-readout"><div class="v">−6 dB</div><div class="l">PEAK · −2.3 dB</div></div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center;">
      <span style="padding:3px 6px;border:1px solid #22c55e;color:#22c55e;font-size:9px;border-radius:3px;font-family:'JetBrains Mono',monospace;text-shadow:0 0 4px #22c55e;">●BLE</span>
      <span style="padding:3px 6px;border:1px solid #22c55e;color:#22c55e;font-size:9px;border-radius:3px;font-family:'JetBrains Mono',monospace;text-shadow:0 0 4px #22c55e;">●PWR</span>
      <span style="padding:3px 6px;border:1px solid #fbbf24;color:#fbbf24;font-size:9px;border-radius:3px;font-family:'JetBrains Mono',monospace;text-shadow:0 0 4px #fbbf24;">●ECHO</span>
      <span style="padding:3px 6px;border:1px solid #374151;color:#9ca3af;font-size:9px;border-radius:3px;font-family:'JetBrains Mono',monospace;">○ERR</span>
    </div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#9ca3af;text-align:center;letter-spacing:0.15em;">▸ ACC: 0.12·−.04·.99 · UART OK</div>
  </div>
</div>
''',
        bg='#1a1a1a')


# ╔══════════════════════════════════════════════════════════════════╗
# ║  #10 — SMARTWATCH / TABLET (flat tile grid)                        ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_10():
    nav = nav_bar(10, 'Smartwatch / Tablet UI', '⌚', 'flat tiles · cards · minimal · modern',
                  accent='#0ea5e9', dim='#475569', text='#f1f5f9', bg='#0f172a')
    return base_html('⌚ #10 Smartwatch UI',
        nav + '''
<style>
  .sw-status{display:flex;justify-content:space-between;align-items:center;padding:6px 14px;background:rgba(255,255,255,0.04);backdrop-filter:blur(20px);border-radius:14px;margin-bottom:12px;font-family:-apple-system,'Inter',sans-serif;font-size:13px;font-weight:600;}
  .sw-status .left{color:#f1f5f9;}
  .sw-status .right{display:flex;gap:6px;color:#94a3b8;}
  .sw-status .dot{width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block;margin-right:4px;box-shadow:0 0 6px #22c55e;}

  .sw-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;max-width:900px;margin:0 auto;}
  @media(max-width:820px){.sw-grid{grid-template-columns:repeat(3,1fr);}}
  @media(max-width:540px){.sw-grid{grid-template-columns:repeat(2,1fr);}}

  .sw-tile{background:rgba(255,255,255,0.05);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:18px;font-family:-apple-system,'Inter',sans-serif;transition:all 0.2s;cursor:pointer;}
  .sw-tile:hover{background:rgba(255,255,255,0.08);transform:translateY(-2px);}
  .sw-tile h3{font-size:11px;color:#94a3b8;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:8px;display:flex;align-items:center;gap:6px;}
  .sw-tile .icon{font-size:18px;}
  .sw-tile .v{font-size:36px;font-weight:700;color:#f1f5f9;line-height:1;}
  .sw-tile .v small{font-size:14px;color:#94a3b8;font-weight:500;margin-left:2px;}
  .sw-tile .sub{font-size:12px;color:#94a3b8;margin-top:6px;font-weight:500;}
  .sw-tile.tall{grid-row:span 2;}
  .sw-tile.wide{grid-column:span 2;}

  .sw-tile.accent{background:linear-gradient(135deg,#0ea5e9,#0284c7);border:none;color:#fff;}
  .sw-tile.accent h3,.sw-tile.accent .v,.sw-tile.accent .sub{color:#fff;}
  .sw-tile.accent .v small{color:rgba(255,255,255,0.7);}

  .sw-tile.warning{background:linear-gradient(135deg,#f97316,#ea580c);border:none;color:#fff;}
  .sw-tile.warning h3,.sw-tile.warning .v,.sw-tile.warning .sub{color:#fff;}

  .sw-bars{display:flex;gap:3px;align-items:flex-end;height:40px;margin-top:10px;}
  .sw-bars .b{flex:1;background:#0ea5e9;border-radius:2px;animation:swBar 1.4s ease-in-out infinite;}
  .sw-bars .b:nth-child(2){animation-delay:0.1s;}
  .sw-bars .b:nth-child(3){animation-delay:0.2s;}
  .sw-bars .b:nth-child(4){animation-delay:0.3s;}
  .sw-bars .b:nth-child(5){animation-delay:0.4s;}
  .sw-bars .b:nth-child(6){animation-delay:0.5s;}
  .sw-bars .b:nth-child(7){animation-delay:0.6s;}
  @keyframes swBar{0%,100%{height:40%}50%{height:90%}}

  .sw-ring{width:80px;height:80px;border-radius:50%;background:conic-gradient(#0ea5e9 0deg,#0ea5e9 280deg,rgba(255,255,255,0.1) 280deg);position:relative;margin:8px auto 0;}
  .sw-ring::before{content:'';position:absolute;inset:8px;background:rgba(255,255,255,0.05);border-radius:50%;}
  .sw-ring::after{content:'78%';position:absolute;inset:0;display:grid;place-items:center;color:#fff;font-size:18px;font-weight:700;}

  .sw-globe{width:80px;height:80px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fbbf24,#f97316 50%,#7c2d12 100%);margin:8px auto 0;box-shadow:0 4px 20px rgba(251,191,36,0.4);animation:swGlobeRot 8s linear infinite;}
  @keyframes swGlobeRot{from{transform:rotate(0)}to{transform:rotate(360deg)}}

  .sw-mini-radar{width:80px;height:80px;border-radius:50%;border:2px solid rgba(255,255,255,0.2);position:relative;margin:8px auto 0;background:rgba(0,0,0,0.3);}
  .sw-mini-radar svg{width:100%;height:100%;}

  .sw-app-pills{display:flex;gap:6px;flex-wrap:wrap;margin-top:auto;padding-top:14px;}
  .sw-app-pill{padding:6px 12px;border-radius:14px;background:rgba(255,255,255,0.1);font-size:11px;font-weight:600;color:#f1f5f9;}
  .sw-app-pill.on{background:#22c55e;color:#0a0a0a;}
</style>
<div class="sw-status">
  <span class="left">9:41</span>
  <span class="right"><span class="dot"></span>BLE · 78% · ▮▮▮▮▯</span>
</div>
<div class="sw-grid">
  <div class="sw-tile accent wide">
    <h3><span class="icon">⏱</span> Speed</h3>
    <div class="v">42<small> kph</small></div>
    <div class="sub">Throttle · 65%</div>
  </div>

  <div class="sw-tile">
    <h3><span class="icon">🌡</span> Temp</h3>
    <div class="v">23.4°</div>
    <div class="sub">+0.2° · normal</div>
  </div>

  <div class="sw-tile">
    <h3><span class="icon">🔋</span> Battery</h3>
    <div class="sw-ring"></div>
    <div class="sub" style="text-align:center;margin-top:10px;">~92 min left</div>
  </div>

  <div class="sw-tile tall">
    <h3><span class="icon">📡</span> Distance</h3>
    <div class="sw-mini-radar">
      <svg viewBox="0 0 80 80">
        <circle cx="40" cy="40" r="32" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/>
        <circle cx="40" cy="40" r="20" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.4"/>
        <g style="transform-origin:center;animation:spin 3s linear infinite;">
          <path d="M 40 40 L 40 8 A 32 32 0 0 1 64 24 Z" fill="#0ea5e9" opacity="0.5"/>
        </g>
        <circle cx="56" cy="28" r="3" fill="#fbbf24"/>
      </svg>
    </div>
    <div class="v" style="text-align:center;margin-top:14px;">12.4<small> m</small></div>
    <div class="sub" style="text-align:center;">1 contact</div>
  </div>

  <div class="sw-tile">
    <h3><span class="icon">🧭</span> Heading</h3>
    <div class="v">120°</div>
    <div class="sub">east · ESE</div>
  </div>

  <div class="sw-tile">
    <h3><span class="icon">🌍</span> Position</h3>
    <div class="sw-globe"></div>
    <div class="sub" style="text-align:center;margin-top:8px;">2.4 m × 1.8 m</div>
  </div>

  <div class="sw-tile">
    <h3><span class="icon">📐</span> Tilt</h3>
    <div class="v" style="font-size:18px;line-height:1.3;">
      X 0.12<br>Y −0.04<br>Z 0.99
    </div>
  </div>

  <div class="sw-tile wide">
    <h3><span class="icon">🔊</span> Sound · Mic</h3>
    <div class="sw-bars">
      <div class="b"></div><div class="b"></div><div class="b"></div>
      <div class="b"></div><div class="b"></div><div class="b"></div>
      <div class="b"></div><div class="b"></div><div class="b"></div>
      <div class="b"></div><div class="b"></div><div class="b"></div>
    </div>
    <div class="sub">−12 dB · listening</div>
  </div>

  <div class="sw-tile warning">
    <h3 style="color:#fff;"><span class="icon">⚠</span> Echo</h3>
    <div class="v">timeout</div>
    <div class="sub">retry · check link</div>
  </div>

  <div class="sw-tile wide">
    <h3><span class="icon">📺</span> UART trace</h3>
    <pre style="font-size:11px;color:#0ea5e9;font-family:'SF Mono','JetBrains Mono',monospace;line-height:1.5;margin:0;">&gt; #41 SRV:1,90  ✓
&gt; #42 DIST?    ✓ 12.4 m
&gt; #43 LINE?    ✓ 1,1
&gt; #44 ACC?     ✓ X·Y·Z</pre>
  </div>

  <div class="sw-tile">
    <h3><span class="icon">⚙</span> Modes</h3>
    <div class="sw-app-pills">
      <span class="sw-app-pill on">Drive</span>
      <span class="sw-app-pill on">Servo</span>
      <span class="sw-app-pill">LED</span>
      <span class="sw-app-pill">IR</span>
    </div>
  </div>
</div>
<style>@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}</style>
''',
        bg='#0f172a', font="-apple-system, 'Inter', sans-serif")


# ╔══════════════════════════════════════════════════════════════════╗
# ║  GENERATE all 10 + gallery                                         ║
# ╚══════════════════════════════════════════════════════════════════╝
makers = [make_1, make_2, make_3, make_4, make_5, make_6, make_7, make_8, make_9, make_10]
labels = [
    ('🛩', 'Plane Cockpit',           'twin yokes · 6-pack · pedestal'),
    ('✈️', 'Glass Cockpit (Airliner)', '4 MFDs · side-stick · FCU'),
    ('🛫', 'Fighter Jet HUD',         'green wireframe · pitch ladder'),
    ('🏎', 'F1 Steering Wheel',       'rev lights · gear · sectors'),
    ('🚢', 'Submarine Helm',          'periscope · sonar · depth'),
    ('🛸', 'Starship Bridge',         'viewscreen · LCARS · stations'),
    ('🤖', 'Mech HUD',                'targeting · weapons · threats'),
    ('🎧', 'DJ Booth',                'twin decks · crossfader · neon'),
    ('🎚', 'Studio Mixer',            'channel strips · faders · VU'),
    ('⌚', 'Smartwatch / Tablet',     'flat tiles · cards · minimal'),
]

for i, maker in enumerate(makers, 1):
    out = os.path.join(OUT, f'cockpit-lab_v2_{i}.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(maker())
    emoji, name, vibe = labels[i-1]
    print(f'  + cockpit-lab_v2_{i}.html  ({emoji} {name})')

# Gallery
gallery = '''<!doctype html>
<html lang="en" data-theme="carbon">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🛸 Cockpit Lab — pick a look</title>
<link rel="stylesheet" href="../workshops/theme.css">
<style>
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:var(--font-body,system-ui);background:var(--bg,#0a1018);color:var(--text,#e0e6ee);padding:24px 18px 40px;}
  h1{font-family:var(--font-display,system-ui);color:var(--neon,#4ade80);font-size:1.8rem;margin-bottom:6px;text-align:center;}
  .sub{text-align:center;color:var(--steel,#93a8c4);margin-bottom:28px;font-size:0.95rem;max-width:780px;margin-left:auto;margin-right:auto;line-height:1.5;}
  .nav{text-align:center;margin:14px 0 24px;}
  .nav a{color:var(--steel);text-decoration:none;padding:6px 14px;border:1px solid var(--border);border-radius:999px;font-size:0.85rem;margin:0 4px;}
  .nav a:hover{color:var(--neon);border-color:var(--neon);}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;max-width:1300px;margin:0 auto;}
  .card{display:block;text-decoration:none;padding:18px 20px;border-radius:14px;border:1.5px solid var(--border,#1d3556);background:var(--bg-card,#142036);color:var(--text);transition:transform 0.15s,border-color 0.15s,box-shadow 0.15s;}
  .card:hover{transform:translateY(-3px);border-color:var(--neon);box-shadow:0 8px 22px rgba(74,222,128,0.18);}
  .card .emoji{font-size:2.2rem;line-height:1;margin-bottom:8px;}
  .card .num{font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:var(--steel);}
  .card h3{font-size:1.15rem;color:var(--neon);margin:6px 0 8px;}
  .card .vibe{font-size:0.86rem;color:var(--text);opacity:0.85;line-height:1.45;}
  .dna{margin-top:10px;font-size:0.78rem;color:var(--cyan,#38bdf8);font-family:'JetBrains Mono',monospace;}
</style>
</head>
<body>

<h1>🛸 Cockpit Lab — pick a look</h1>
<p class="sub">10 GENUINELY different design directions. Each has its own structure, layout, metaphor, density. Click any card to preview the full mockup.</p>

<div class="nav">
  <a href="index.html">🧪 All Labs</a>
  <a href="../index.html">🤖 Robot App</a>
</div>

<div class="grid">
'''
for i, (emoji, name, vibe) in enumerate(labels, 1):
    gallery += f'''  <a class="card" href="cockpit-lab_v2_{i}.html">
    <div class="emoji">{emoji}</div>
    <div class="num">cockpit-lab_v2_{i}.html</div>
    <h3>{name}</h3>
    <div class="vibe">{vibe}</div>
    <div class="dna">▸ unique layout DNA</div>
  </a>
'''

gallery += '''</div>
</body>
</html>
'''
with open(os.path.join(OUT, 'cockpit-lab_v2.html'), 'w', encoding='utf-8') as f:
    f.write(gallery)
print('\n  + cockpit-lab_v2.html  (gallery)')
print(f'\nDone — 10 mockups + gallery written to {os.path.relpath(OUT)}')
