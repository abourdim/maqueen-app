#!/usr/bin/env python3
"""Generate 10 cockpit-lab_N.html mockups + the gallery picker.

Each file is a SELF-CONTAINED single-page mockup:
  * inline CSS theme variables
  * inline SVG instrument widgets (shared geometry, theme-coloured)
  * subtle animations (radar sweep, annunciator pulse, mic bars)
  * static — no BLE wiring, no telemetry, no scripts to load

Re-run any time to regenerate; previous files are overwritten.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'labs')

# ───────────────────────────────────────────────────────────────────
# 10 themes — palette + identity
# ───────────────────────────────────────────────────────────────────
THEMES = [
    dict(slug='cessna',    name='Aircraft Cockpit',  emoji='🛩',
         bg='#3d352a', panel='#5a4d3d', accent='#fbbf24', dim='#a98864',
         text='#f8efde', glow='#fde68a',
         font="'Courier New', monospace",
         vibe='cream panel · brass screws · analog dials',
         needle='#1c1208', bezel='#2c1f15'),

    dict(slug='f16',       name='Fighter Jet',       emoji='🛫',
         bg='#1a1f1a', panel='#2c322a', accent='#86efac', dim='#4a5a4a',
         text='#bbf7d0', glow='#86efac',
         font="'JetBrains Mono', monospace",
         vibe='military green CRT · amber MFDs · vector lines',
         needle='#fbbf24', bezel='#0a0e0a'),

    dict(slug='airliner',  name='Airliner Glass',    emoji='✈️',
         bg='#0a1828', panel='#13243d', accent='#38bdf8', dim='#1e3a5c',
         text='#e0f2fe', glow='#7dd3fc',
         font="'Inter', sans-serif",
         vibe='Boeing dark blue · big PFD · sleek',
         needle='#ffffff', bezel='#020617'),

    dict(slug='apollo',    name='Apollo Lunar',      emoji='🚀',
         bg='#5d553a', panel='#7a6f4d', accent='#fde047', dim='#a8997a',
         text='#fef9c3', glow='#fde047',
         font="'Courier New', monospace",
         vibe='1960s NASA olive · push buttons · mechanical',
         needle='#1a1408', bezel='#3d3826'),

    dict(slug='lcars',     name='Star Trek LCARS',   emoji='🛸',
         bg='#000000', panel='#0a0a0a', accent='#fb923c', dim='#c084fc',
         text='#fbbf24', glow='#fb923c',
         font="'Antonio', 'Helvetica Neue', sans-serif",
         vibe='asymmetric flat pills · no bezels · 24th century',
         needle='#fbbf24', bezel='#000'),

    dict(slug='ironman',   name='Iron Man HUD',      emoji='🦾',
         bg='#020617', panel='rgba(56,189,248,0.05)', accent='#67e8f9', dim='#0891b2',
         text='#cffafe', glow='#67e8f9',
         font="'Orbitron', 'Helvetica Neue', sans-serif",
         vibe='translucent cyan · holographic rings · floating',
         needle='#67e8f9', bezel='rgba(103,232,249,0.3)'),

    dict(slug='submarine', name='Submarine',         emoji='🚢',
         bg='#1a0808', panel='#3d1a1a', accent='#dc2626', dim='#7f1d1d',
         text='#fee2e2', glow='#fca5a5',
         font="'Courier New', monospace",
         vibe='red dim · brass · sonar tubes',
         needle='#fbbf24', bezel='#5c2c10'),

    dict(slug='alien',     name='Alien Vessel',      emoji='👽',
         bg='#0a1a0a', panel='#0f2818', accent='#a3e635', dim='#65a30d',
         text='#d9f99d', glow='#a3e635',
         font="'Orbitron', monospace",
         vibe='bio-organic · pulsing glyphs · liquid',
         needle='#a3e635', bezel='#1a3a1a'),

    dict(slug='mech',      name='Mech / Pacific Rim',emoji='🤖',
         bg='#1c1c1c', panel='#2d2d2d', accent='#f97316', dim='#7c2d12',
         text='#fed7aa', glow='#f97316',
         font="'JetBrains Mono', monospace",
         vibe='riveted plates · hazard chevrons · oversized',
         needle='#fbbf24', bezel='#0a0a0a'),

    dict(slug='arcade',    name='Retro Arcade',      emoji='👾',
         bg='#0d0221', panel='#1a0942', accent='#f0f', dim='#7c3aed',
         text='#fae8ff', glow='#ff00ff',
         font="'Press Start 2P', 'Courier New', monospace",
         vibe='pixel · neon · chunky · CRT scanlines',
         needle='#00ffff', bezel='#000'),
]

# ───────────────────────────────────────────────────────────────────
# Shared HTML template
# ───────────────────────────────────────────────────────────────────
TEMPLATE = r'''<!doctype html>
<html lang="en" data-theme="cockpit">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{emoji} Cockpit Lab #{idx} — {name}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    background: {bg};
    color: {text};
    font-family: {font};
    min-height: 100vh;
    overflow-x: hidden;
  }}
  body {{ padding: 14px 18px 28px; }}

  /* Scanlines for arcade / CRT vibe */
  {scanlines}

  /* ───── Top bar (nav between mockups) ───── */
  .topbar {{
    display: flex; align-items: center; gap: 10px;
    padding: 8px 14px; margin-bottom: 14px;
    background: {panel};
    border: 1px solid {dim};
    border-radius: 10px;
    flex-wrap: wrap;
  }}
  .topbar h1 {{
    font-size: 15px; font-weight: 700;
    color: {accent};
    letter-spacing: 0.06em;
    margin-right: auto;
  }}
  .topbar h1 .vibe {{ color: {dim}; font-weight: 400; font-size: 11px; margin-left: 8px; }}
  .topbar a, .topbar button {{
    background: transparent; color: {text};
    border: 1px solid {dim}; border-radius: 6px;
    padding: 4px 10px; font-size: 12px;
    text-decoration: none; cursor: pointer;
    font-family: inherit;
  }}
  .topbar a:hover {{ border-color: {accent}; color: {accent}; }}

  /* ───── Cockpit grid layout ───── */
  .cockpit {{
    display: grid;
    grid-template-columns: 1fr 1.4fr 1fr;
    grid-template-rows: auto auto auto;
    gap: 12px;
    max-width: 1200px;
    margin: 0 auto;
  }}
  .cockpit > .full {{ grid-column: 1 / -1; }}
  @media (max-width: 820px) {{
    .cockpit {{ grid-template-columns: 1fr 1fr; }}
  }}
  @media (max-width: 540px) {{
    .cockpit {{ grid-template-columns: 1fr; }}
  }}

  /* ───── Generic instrument card ───── */
  .inst {{
    background: {panel};
    border: 1.5px solid {bezel};
    border-radius: 14px;
    padding: 12px;
    position: relative;
    {extra_inst_style}
  }}
  .inst .lbl {{
    font-size: 10px;
    color: {dim};
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 6px;
    font-weight: 700;
  }}
  .inst .val {{
    color: {accent};
    font-weight: 700;
    font-size: 14px;
  }}

  /* ───── Annunciator panel ───── */
  .annunciator {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }}
  .annunciator .light {{
    padding: 6px 4px;
    text-align: center;
    border-radius: 6px;
    background: rgba(255,255,255,0.03);
    border: 1px solid {dim};
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: {dim};
    transition: all 0.3s;
  }}
  .annunciator .light.on {{
    background: {accent}; color: {bg};
    box-shadow: 0 0 12px {glow};
    animation: annPulse 2.4s ease-in-out infinite;
  }}
  @keyframes annPulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.65; }} }}

  /* ───── MFD log ───── */
  .mfd {{
    background: rgba(0,0,0,0.55);
    border: 1px solid {dim};
    border-radius: 8px;
    padding: 8px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: {accent};
    height: 110px;
    overflow: hidden;
    line-height: 1.5;
  }}
  .mfd .row {{ animation: mfdScroll 6s linear infinite; }}
  @keyframes mfdScroll {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-100%); }} }}

  /* ───── Throttle slider ───── */
  .throttle {{ display: flex; flex-direction: column; align-items: center; gap: 6px; height: 200px; }}
  .throttle .track {{
    width: 32px; flex: 1; background: rgba(0,0,0,0.5);
    border: 1px solid {dim}; border-radius: 16px;
    position: relative;
  }}
  .throttle .knob {{
    position: absolute; left: 50%; transform: translateX(-50%);
    width: 56px; height: 24px;
    bottom: 35%;
    background: {accent}; border-radius: 6px;
    box-shadow: 0 0 10px {glow};
  }}

  /* ───── Yoke ───── */
  .yoke-wrap {{ display: flex; align-items: center; justify-content: center; height: 200px; }}
  .yoke {{
    width: 160px; height: 160px;
    border-radius: 50%;
    border: 4px solid {dim};
    background: radial-gradient(circle at 35% 35%, rgba(255,255,255,0.12), transparent 60%), {panel};
    position: relative;
  }}
  .yoke::before {{
    content: ''; position: absolute; inset: 24px; border-radius: 50%;
    border: 2px solid {accent};
    background: radial-gradient(circle at 50% 50%, {accent}, {bezel} 90%);
    box-shadow: 0 0 20px {glow};
  }}
  .yoke::after {{
    content: '+'; position: absolute; inset: 0; display: grid; place-items: center;
    color: {bg}; font-size: 36px; font-weight: 900; line-height: 1;
  }}

  /* ───── Bars (temp, mic, battery) ───── */
  .bars {{ display: flex; gap: 3px; align-items: flex-end; height: 60px; margin-top: 6px; }}
  .bars .b {{ flex: 1; background: {accent}; border-radius: 2px 2px 0 0; opacity: 0.85;
              animation: barBob 1.4s ease-in-out infinite; }}
  .bars .b:nth-child(1) {{ height: 30%; animation-delay: 0s; }}
  .bars .b:nth-child(2) {{ height: 60%; animation-delay: 0.1s; }}
  .bars .b:nth-child(3) {{ height: 80%; animation-delay: 0.2s; }}
  .bars .b:nth-child(4) {{ height: 50%; animation-delay: 0.3s; }}
  .bars .b:nth-child(5) {{ height: 70%; animation-delay: 0.4s; }}
  .bars .b:nth-child(6) {{ height: 40%; animation-delay: 0.5s; }}
  .bars .b:nth-child(7) {{ height: 65%; animation-delay: 0.6s; }}
  .bars .b:nth-child(8) {{ height: 55%; animation-delay: 0.7s; }}
  @keyframes barBob {{ 0%,100% {{ transform: scaleY(1); }} 50% {{ transform: scaleY(1.4); }} }}

  /* ───── Vbar (battery) ───── */
  .vbar {{ width: 100%; height: 80px; background: rgba(0,0,0,0.5);
           border: 1px solid {dim}; border-radius: 6px; padding: 4px;
           display: flex; flex-direction: column-reverse; gap: 2px; }}
  .vbar .seg {{ flex: 1; background: {accent}; opacity: 0.95;
                box-shadow: 0 0 6px {glow}; border-radius: 1px; }}
  .vbar .seg.off {{ background: {dim}; opacity: 0.3; box-shadow: none; }}

  /* ───── 3D accel ball ───── */
  .accel-stage {{ height: 130px; display: grid; place-items: center;
                  perspective: 400px; }}
  .accel-ball {{
    width: 80px; height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, {glow}, {accent} 50%, {bezel} 100%);
    box-shadow: 0 0 20px {glow}, inset -8px -8px 18px rgba(0,0,0,0.5);
    animation: accelTilt 4s ease-in-out infinite;
    transform-style: preserve-3d;
  }}
  @keyframes accelTilt {{
    0%,100% {{ transform: rotateX(8deg) rotateY(-15deg); }}
    50%     {{ transform: rotateX(-12deg) rotateY(20deg); }}
  }}

  /* ───── Radar sweep ───── */
  .radar svg .sweep {{
    transform-origin: 100px 100px;
    animation: radarSpin 3s linear infinite;
  }}
  @keyframes radarSpin {{ from {{ transform: rotate(0); }} to {{ transform: rotate(360deg); }} }}

  /* ───── Compass needle ───── */
  .compass svg .needle {{
    transform-origin: 100px 100px;
    animation: compassWiggle 6s ease-in-out infinite;
  }}
  @keyframes compassWiggle {{
    0%,100% {{ transform: rotate(-12deg); }}
    50%     {{ transform: rotate(34deg); }}
  }}

  /* ───── Speed needle ───── */
  .speed svg .needle {{
    transform-origin: 100px 100px;
    animation: speedSweep 5s ease-in-out infinite;
  }}
  @keyframes speedSweep {{
    0%,100% {{ transform: rotate(-90deg); }}
    50%     {{ transform: rotate(45deg); }}
  }}

  /* ───── Sound waveform ───── */
  .wave {{ height: 60px; }}
  .wave svg .line {{ animation: wavePulse 1.2s ease-in-out infinite; }}
  @keyframes wavePulse {{ 0%,100% {{ opacity: 0.6; transform: scaleY(0.8); }} 50% {{ opacity: 1; transform: scaleY(1.4); }} }}

  /* ───── Boot light chase ───── */
  @keyframes boot {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .inst {{ animation: boot 0.6s ease-out backwards; }}
  .inst:nth-child(2) {{ animation-delay: 0.06s; }}
  .inst:nth-child(3) {{ animation-delay: 0.12s; }}
  .inst:nth-child(4) {{ animation-delay: 0.18s; }}
  .inst:nth-child(5) {{ animation-delay: 0.24s; }}
  .inst:nth-child(6) {{ animation-delay: 0.30s; }}
  .inst:nth-child(7) {{ animation-delay: 0.36s; }}
  .inst:nth-child(8) {{ animation-delay: 0.42s; }}
  .inst:nth-child(9) {{ animation-delay: 0.48s; }}
  .inst:nth-child(10) {{ animation-delay: 0.54s; }}
  .inst:nth-child(11) {{ animation-delay: 0.60s; }}

  {theme_extras}
</style>
</head>
<body>

<div class="topbar">
  <h1>{emoji} #{idx} · {name} <span class="vibe">{vibe}</span></h1>
  <a href="cockpit-lab.html">⚙ Gallery</a>
  <a href="cockpit-lab_{prev}.html">‹ Prev</a>
  <a href="cockpit-lab_{next}.html">Next ›</a>
  <a href="index.html">🧪 Labs</a>
  <a href="../index.html">🤖 App</a>
</div>

<div class="cockpit">

  <!-- 1. Speed gauge -->
  <div class="inst speed">
    <div class="lbl">⏱ Speed</div>
    <svg viewBox="0 0 200 130" width="100%">
      <circle cx="100" cy="100" r="80" fill="none" stroke="{dim}" stroke-width="2"/>
      <path d="M 30 100 A 70 70 0 0 1 170 100" fill="none" stroke="{accent}" stroke-width="3" opacity="0.7"/>
      <g class="needle">
        <line x1="100" y1="100" x2="100" y2="35" stroke="{needle}" stroke-width="3" stroke-linecap="round"/>
        <circle cx="100" cy="100" r="6" fill="{needle}"/>
      </g>
      <text x="100" y="120" text-anchor="middle" fill="{text}" font-size="14" font-weight="700">42</text>
    </svg>
  </div>

  <!-- 2. Radar / Distance -->
  <div class="inst radar">
    <div class="lbl">📡 Radar · Sonar</div>
    <svg viewBox="0 0 200 200" width="100%">
      <circle cx="100" cy="100" r="90" fill="none" stroke="{dim}" stroke-width="1"/>
      <circle cx="100" cy="100" r="60" fill="none" stroke="{dim}" stroke-width="0.8" opacity="0.6"/>
      <circle cx="100" cy="100" r="30" fill="none" stroke="{dim}" stroke-width="0.6" opacity="0.5"/>
      <g class="sweep">
        <path d="M 100 100 L 100 10 A 90 90 0 0 1 175 65 Z" fill="{accent}" opacity="0.25"/>
        <line x1="100" y1="100" x2="100" y2="10" stroke="{accent}" stroke-width="1.5"/>
      </g>
      <circle cx="135" cy="60" r="3" fill="{glow}"/>
      <circle cx="70" cy="120" r="2" fill="{glow}" opacity="0.7"/>
    </svg>
  </div>

  <!-- 3. Compass -->
  <div class="inst compass">
    <div class="lbl">🧭 Heading</div>
    <svg viewBox="0 0 200 130" width="100%">
      <circle cx="100" cy="100" r="80" fill="{bezel}" stroke="{dim}" stroke-width="2"/>
      <text x="100" y="32" text-anchor="middle" fill="{accent}" font-size="14" font-weight="700">N</text>
      <text x="170" y="105" text-anchor="middle" fill="{dim}" font-size="11">E</text>
      <text x="100" y="178" text-anchor="middle" fill="{dim}" font-size="11">S</text>
      <text x="30" y="105" text-anchor="middle" fill="{dim}" font-size="11">W</text>
      <g class="needle">
        <polygon points="100,30 95,100 105,100" fill="{accent}"/>
        <polygon points="100,170 95,100 105,100" fill="{dim}"/>
        <circle cx="100" cy="100" r="5" fill="{accent}"/>
      </g>
    </svg>
  </div>

  <!-- 4. Temperature -->
  <div class="inst">
    <div class="lbl">🌡 Temperature</div>
    <div style="margin-top:14px; font-size:32px; font-weight:800; color:{accent}; text-align:center; text-shadow:0 0 10px {glow};">23.4 <span style="font-size:14px; color:{dim}">°C</span></div>
    <div style="height:8px; background:rgba(0,0,0,0.4); border-radius:4px; margin-top:14px; overflow:hidden;">
      <div style="height:100%; width:54%; background:linear-gradient(90deg, #38bdf8, {accent}, #f87171); box-shadow:0 0 10px {glow};"></div>
    </div>
    <div style="display:flex; justify-content:space-between; font-size:9px; color:{dim}; margin-top:4px;">
      <span>−10</span><span>+50</span>
    </div>
  </div>

  <!-- 5. Yoke -->
  <div class="inst">
    <div class="lbl">🕹 Yoke</div>
    <div class="yoke-wrap"><div class="yoke"></div></div>
  </div>

  <!-- 6. Accel ball -->
  <div class="inst">
    <div class="lbl">📐 Accelerometer · X·Y·Z</div>
    <div class="accel-stage"><div class="accel-ball"></div></div>
    <div style="display:flex; justify-content:space-around; font-size:10px; color:{dim}; font-family:monospace;">
      <span>X 124</span><span>Y −38</span><span>Z 992</span>
    </div>
  </div>

  <!-- 7. Throttle -->
  <div class="inst">
    <div class="lbl">🎚 Throttle</div>
    <div class="throttle"><div class="track"><div class="knob"></div></div></div>
    <div style="text-align:center; color:{accent}; font-size:14px; font-weight:700;">65%</div>
  </div>

  <!-- 8. Mic level + sound waveform -->
  <div class="inst">
    <div class="lbl">🔊 Sound · mic · alert tones</div>
    <div class="bars">
      <div class="b"></div><div class="b"></div><div class="b"></div>
      <div class="b"></div><div class="b"></div><div class="b"></div>
      <div class="b"></div><div class="b"></div>
    </div>
    <div class="wave" style="margin-top:6px;">
      <svg viewBox="0 0 200 60" width="100%" preserveAspectRatio="none">
        <path class="line" d="M 0 30 Q 25 5 50 30 T 100 30 T 150 30 T 200 30" fill="none" stroke="{accent}" stroke-width="2"/>
      </svg>
    </div>
  </div>

  <!-- 9. Battery -->
  <div class="inst">
    <div class="lbl">🔋 Battery</div>
    <div style="display:flex; gap:12px; align-items:center;">
      <div class="vbar">
        <div class="seg"></div><div class="seg"></div><div class="seg"></div>
        <div class="seg"></div><div class="seg"></div><div class="seg"></div>
        <div class="seg off"></div><div class="seg off"></div>
      </div>
      <div>
        <div style="font-size:24px; font-weight:800; color:{accent}; text-shadow:0 0 8px {glow};">78%</div>
        <div style="font-size:10px; color:{dim};">4.02 V</div>
      </div>
    </div>
  </div>

  <!-- 10. Annunciator -->
  <div class="inst full">
    <div class="lbl">💡 Annunciator panel</div>
    <div class="annunciator">
      <div class="light on">BLE</div>
      <div class="light on">PWR</div>
      <div class="light">ECHO</div>
      <div class="light on">SVO</div>
      <div class="light">LIN</div>
      <div class="light">IR</div>
      <div class="light on">MIC</div>
      <div class="light">ERR</div>
    </div>
  </div>

  <!-- 11. MFD log -->
  <div class="inst full">
    <div class="lbl">📺 MFD · UART trace</div>
    <div class="mfd">
      <div class="row">
        &gt; #41 SRV:1,90<br>
        &lt; ECHO:41 SRV:1,90<br>
        &gt; #42 DIST?<br>
        &lt; DIST:42<br>
        &gt; #43 LINE?<br>
        &lt; LINE:1,1<br>
        &gt; #44 ACC?<br>
        &lt; ACC:124,-38,992<br>
        &gt; #45 SRV:1,90<br>
        &lt; ECHO:45 SRV:1,90<br>
        &gt; #46 DIST?<br>
        &lt; DIST:42<br>
      </div>
    </div>
  </div>

</div>

</body>
</html>
'''

# ───────────────────────────────────────────────────────────────────
# Per-theme extras (textures, decorations, scanlines)
# ───────────────────────────────────────────────────────────────────
def per_theme_extras(theme):
    slug = theme['slug']
    extras = {
        'arcade':  '''body::before { content:''; position:fixed; inset:0; pointer-events:none; z-index:9999; background:repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 3px); }''',
        'submarine': '''body::after { content:''; position:fixed; inset:0; pointer-events:none; background:radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.55)); z-index:9998; }''',
        'lcars': '''.inst { border-radius: 28px 8px 8px 28px !important; } .inst .lbl { background: var(--accent); color: #000; padding: 4px 10px; border-radius: 999px; display: inline-block; }''',
        'ironman': '''.inst { backdrop-filter: blur(10px); }''',
        'alien': '''@keyframes glyph { 0%,100% { letter-spacing: 0.15em; } 50% { letter-spacing: 0.3em; } }
                   .inst .lbl { animation: glyph 4s ease-in-out infinite; }''',
        'mech': '''.inst::before { content:''; position:absolute; top:6px; right:6px; width:8px; height:8px; border-radius:50%; background:#fbbf24; box-shadow: 12px 0 #fbbf24, 24px 0 #fbbf24; }''',
        'apollo': '''.inst { box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05); }''',
        'cessna': '''.inst { box-shadow: inset 0 0 12px rgba(0,0,0,0.3); }
                    .inst::after { content:'•'; position:absolute; top:4px; left:4px; color: #4a3d2a; font-size: 8px; }''',
    }
    if slug in ('arcade', 'submarine'):
        scanlines = extras[slug]
    else:
        scanlines = ''
    theme_extras = extras.get(slug, '')
    if slug in ('arcade', 'submarine'):
        # already used in scanlines slot, don't duplicate
        theme_extras = ''
    return scanlines, theme_extras

# ───────────────────────────────────────────────────────────────────
# Per-theme inst card style adjustments
# ───────────────────────────────────────────────────────────────────
def per_theme_inst_style(theme):
    slug = theme['slug']
    if slug == 'lcars':       return ''  # handled in extras
    if slug == 'ironman':     return 'background: rgba(56,189,248,0.06); border: 1px solid rgba(103,232,249,0.4);'
    if slug == 'arcade':      return 'border-radius: 4px; image-rendering: pixelated;'
    if slug == 'submarine':   return 'background: linear-gradient(135deg, #3d1a1a, #2a0808);'
    if slug == 'mech':        return 'border: 2px dashed #f97316;'
    if slug == 'apollo':      return 'background: linear-gradient(135deg, #7a6f4d, #5d553a);'
    return ''

# ───────────────────────────────────────────────────────────────────
# Render all 10 mockups
# ───────────────────────────────────────────────────────────────────
for i, theme in enumerate(THEMES, 1):
    scanlines, theme_extras = per_theme_extras(theme)
    extra_inst_style = per_theme_inst_style(theme)
    prev_idx = (i - 2) % 10 + 1
    next_idx = i % 10 + 1
    html = TEMPLATE.format(
        idx=i, name=theme['name'], emoji=theme['emoji'],
        bg=theme['bg'], panel=theme['panel'], accent=theme['accent'],
        dim=theme['dim'], text=theme['text'], glow=theme['glow'],
        font=theme['font'], vibe=theme['vibe'],
        needle=theme['needle'], bezel=theme['bezel'],
        scanlines=scanlines, theme_extras=theme_extras,
        extra_inst_style=extra_inst_style,
        prev=prev_idx, next=next_idx,
    )
    out_path = os.path.join(OUT, f'cockpit-lab_{i}.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✓ {os.path.basename(out_path)}  ({theme["name"]})')

# ───────────────────────────────────────────────────────────────────
# Gallery picker
# ───────────────────────────────────────────────────────────────────
gallery = '''<!doctype html>
<html lang="en" data-theme="carbon">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🛸 Cockpit Lab — pick a look</title>
<link rel="stylesheet" href="../workshops/theme.css">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: var(--font-body, system-ui); background: var(--bg, #0a1018); color: var(--text, #e0e6ee); padding: 24px 18px 40px; }
  h1 { font-family: var(--font-display, system-ui); color: var(--neon, #4ade80); font-size: 1.8rem; margin-bottom: 6px; text-align: center; }
  .sub { text-align: center; color: var(--steel, #93a8c4); margin-bottom: 28px; font-size: 0.95rem; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.5; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; max-width: 1200px; margin: 0 auto; }
  .card {
    display: block; text-decoration: none;
    padding: 16px 18px;
    border-radius: 14px;
    border: 1.5px solid var(--border, #1d3556);
    background: var(--bg-card, #142036);
    color: var(--text);
    transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
  }
  .card:hover { transform: translateY(-3px); border-color: var(--neon); box-shadow: 0 8px 22px rgba(74,222,128,0.18); }
  .card .emoji { font-size: 2rem; line-height: 1; margin-bottom: 6px; }
  .card .num { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--steel); }
  .card h3 { font-size: 1.1rem; color: var(--neon); margin: 4px 0 6px; }
  .card .vibe { font-size: 0.84rem; color: var(--text); opacity: 0.85; line-height: 1.45; }
  .card .swatch { display: flex; gap: 4px; margin-top: 10px; }
  .card .sw { width: 18px; height: 18px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); }
  .nav { text-align: center; margin: 24px 0; }
  .nav a { color: var(--steel); text-decoration: none; padding: 6px 12px; border: 1px solid var(--border); border-radius: 999px; font-size: 0.85rem; margin: 0 4px; }
  .nav a:hover { color: var(--neon); border-color: var(--neon); }
</style>
</head>
<body>

<h1>🛸 Cockpit Lab — pick a look</h1>
<p class="sub">10 visual directions for the future <code>labs/cockpit-lab.html</code>. Click any card to preview the static mockup. Same 11 instruments in each (speed · radar · compass · temp · accel · mic · battery · throttle · yoke · annunciators · MFD).</p>

<div class="nav">
  <a href="index.html">🧪 All Labs</a>
  <a href="../index.html">🤖 Robot App</a>
</div>

<div class="grid">
'''

for i, theme in enumerate(THEMES, 1):
    gallery += f'''  <a class="card" href="cockpit-lab_{i}.html">
    <div class="emoji">{theme["emoji"]}</div>
    <div class="num">cockpit-lab_{i}.html</div>
    <h3>{theme["name"]}</h3>
    <div class="vibe">{theme["vibe"]}</div>
    <div class="swatch">
      <div class="sw" style="background:{theme["bg"]}"></div>
      <div class="sw" style="background:{theme["panel"]}"></div>
      <div class="sw" style="background:{theme["accent"]}"></div>
      <div class="sw" style="background:{theme["dim"]}"></div>
      <div class="sw" style="background:{theme["glow"]}"></div>
    </div>
  </a>
'''

gallery += '''
</div>

</body>
</html>
'''
gallery_path = os.path.join(OUT, 'cockpit-lab.html')
with open(gallery_path, 'w', encoding='utf-8') as f:
    f.write(gallery)
print(f'\n  ✓ {os.path.basename(gallery_path)}  (gallery picker)')

print(f'\n✅ Generated 10 mockups + gallery in {os.path.relpath(OUT)}')
