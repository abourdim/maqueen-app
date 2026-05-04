#!/usr/bin/env python3
"""Cockpit Lab v5 — photo-realistic skeuomorphic flight-sim panel.

Matches the workshop poster aesthetic: brushed-metal gray panel, chrome
bezel round gauges, real throttle levers, knurled knobs, switches with
depth shadows, wooden biplane silhouette on top. All Maqueen hardware
mapped onto a single real-looking cockpit panel.

Static design only. Re-runnable.
"""
import os, math

OUT = os.path.join(os.path.dirname(__file__), '..', 'labs')


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Skeuomorphic gauge SVG — chrome bezel, glass face, white needle    ║
# ╚═════════════════════════════════════════════════════════════════════╝
def gauge(name, val, unit, needle_deg=45, size=170, face='#0a1018', accent='#fbbf24',
          range_arc=(-135,135), range_labels=None, swing=False, danger_zone=None):
    """range_labels: list of (deg, text) for tick numbers. swing: animate needle."""
    if range_labels is None:
        range_labels = [(range_arc[0]+i*(range_arc[1]-range_arc[0])/6, str(i*2)) for i in range(7)]
    span = range_arc[1] - range_arc[0]
    # major + minor ticks
    ticks = ''
    for i in range(31):
        ang = range_arc[0] + (i/30)*span
        long_t = i % 5 == 0
        ticks += f'<line x1="50" y1="6" x2="50" y2="{12 if long_t else 9}" stroke="{"#e5e7eb" if long_t else "#9ca3af"}" stroke-width="{1.4 if long_t else 0.6}" transform="rotate({ang} 50 50)"/>'
    # numbers
    nums = ''
    for d, t in range_labels:
        nums += f'<text x="50" y="22" text-anchor="middle" fill="#e5e7eb" font-size="6.5" font-family="Helvetica,Arial,sans-serif" font-weight="700" transform="rotate({d} 50 50) rotate({-d} 50 22)">{t}</text>'
    # danger arc (red/yellow band)
    danger = ''
    if danger_zone:
        a1 = math.radians(range_arc[0] + danger_zone[0]*span/100 - 90)
        a2 = math.radians(range_arc[0] + danger_zone[1]*span/100 - 90)
        x1, y1 = 50 + 36*math.cos(a1), 50 + 36*math.sin(a1)
        x2, y2 = 50 + 36*math.cos(a2), 50 + 36*math.sin(a2)
        large = 1 if (danger_zone[1]-danger_zone[0]) > 50 else 0
        danger = f'<path d="M {x1:.2f} {y1:.2f} A 36 36 0 {large} 1 {x2:.2f} {y2:.2f}" fill="none" stroke="#ef4444" stroke-width="3" opacity="0.85"/>'
    swing_attr = '<animateTransform attributeName="transform" type="rotate" values="-30 50 50;45 50 50;-30 50 50" dur="4s" repeatCount="indefinite"/>' if swing else ''
    return f'''<div class="gauge" style="width:{size}px;height:{size}px;">
  <!-- outer chrome bezel ring -->
  <div class="bezel">
    <!-- glass face -->
    <div class="face" style="background:radial-gradient(circle at 50% 30%,#1f2937 0%,{face} 60%,#000 100%);">
      <svg viewBox="0 0 100 100" style="width:100%;height:100%;">
        {danger}
        {ticks}
        {nums}
        <!-- needle -->
        <g>
          <line x1="50" y1="55" x2="50" y2="14" stroke="#fff" stroke-width="2.4" stroke-linecap="round" transform="rotate({needle_deg} 50 50)" style="filter:drop-shadow(0 1px 2px rgba(0,0,0,0.8));">
            {swing_attr}
          </line>
          <circle cx="50" cy="55" r="4" fill="#9ca3af" stroke="#000" stroke-width="0.5"/>
        </g>
        <!-- center hub -->
        <circle cx="50" cy="50" r="2.5" fill="#fff" opacity="0.9"/>
        <!-- name plate at bottom -->
      </svg>
      <div class="name">{name}</div>
      <div class="readout"><span class="val">{val}</span><span class="unit">{unit}</span></div>
      <!-- glass reflection -->
      <div class="reflection"></div>
    </div>
  </div>
</div>'''


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Skeuomorphic knurled knob — chrome with grip ridges                ║
# ╚═════════════════════════════════════════════════════════════════════╝
def knob(label, value='', size=70, deg=120, accent='#fbbf24'):
    ridges = ''.join(
        f'<line x1="50" y1="14" x2="50" y2="20" stroke="rgba(0,0,0,0.6)" stroke-width="1.2" transform="rotate({i*15} 50 50)"/>'
        for i in range(24)
    )
    return f'''<div class="knob-wrap" style="width:{size+10}px;">
  <div class="knob" style="width:{size}px;height:{size}px;">
    <svg viewBox="0 0 100 100" style="width:100%;height:100%;position:absolute;inset:0;">
      <!-- shadow on panel -->
      <ellipse cx="50" cy="92" rx="36" ry="6" fill="rgba(0,0,0,0.55)"/>
      <!-- base ring -->
      <circle cx="50" cy="50" r="44" fill="#0a0a0a"/>
      <!-- knob body w/ chrome gradient -->
      <defs>
        <radialGradient id="kg{deg}" cx="35%" cy="30%" r="70%">
          <stop offset="0%" stop-color="#fafafa"/>
          <stop offset="35%" stop-color="#9ca3af"/>
          <stop offset="75%" stop-color="#374151"/>
          <stop offset="100%" stop-color="#0a0a0a"/>
        </radialGradient>
      </defs>
      <circle cx="50" cy="50" r="40" fill="url(#kg{deg})"/>
      {ridges}
      <!-- top dish -->
      <circle cx="50" cy="50" r="22" fill="radial-gradient(circle,#1f2937,#000)" stroke="#000" stroke-width="0.6"/>
      <circle cx="50" cy="50" r="22" fill="url(#kg{deg})" opacity="0.65"/>
      <!-- pointer line -->
      <line x1="50" y1="50" x2="50" y2="14" stroke="{accent}" stroke-width="3" stroke-linecap="round" transform="rotate({deg} 50 50)" style="filter:drop-shadow(0 0 2px {accent});"/>
      <circle cx="50" cy="50" r="3" fill="#000"/>
      <!-- highlight -->
      <ellipse cx="38" cy="32" rx="14" ry="6" fill="rgba(255,255,255,0.35)"/>
    </svg>
  </div>
  <div class="lbl-tag">{label}</div>
  {f'<div class="val-tag" style="color:{accent};">{value}</div>' if value else ''}
</div>'''


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Throttle lever — chrome metal stick on slot                         ║
# ╚═════════════════════════════════════════════════════════════════════╝
def throttle(label, pct=72, color='#000', height=180):
    return f'''<div class="throttle-wrap">
  <div class="throttle-slot" style="height:{height}px;">
    <div class="slot-rail"></div>
    <div class="lever" style="bottom:{pct*0.85}%;">
      <div class="lever-stick"></div>
      <div class="lever-grip" style="background:radial-gradient(circle at 30% 25%,#fff,#9ca3af 35%,#374151 75%,#0a0a0a 100%);">
        <div class="lever-cap" style="background:radial-gradient(circle at 30% 25%,#fff,{color} 60%,#000 100%);"></div>
      </div>
    </div>
    <div class="slot-mark" style="top:5%;">FULL</div>
    <div class="slot-mark" style="top:30%;">CLB</div>
    <div class="slot-mark" style="top:60%;">CRZ</div>
    <div class="slot-mark" style="top:90%;">IDLE</div>
  </div>
  <div class="lever-label">{label}</div>
  <div class="lever-pct">{pct}%</div>
</div>'''


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Toggle switch (real metal flip switch with red guard cover)        ║
# ╚═════════════════════════════════════════════════════════════════════╝
def toggle(label, on=False, guarded=False):
    cover = ''
    if guarded:
        cover = '<div class="guard"></div>'
    return f'''<div class="toggle-wrap">
  {cover}
  <div class="toggle-base">
    <div class="toggle-stick" style="transform:translateX(-50%) rotate({-25 if on else 25}deg);">
      <div class="toggle-ball"></div>
    </div>
  </div>
  <div class="toggle-label">{label}</div>
</div>'''


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Indicator LED (real bulb with dome)                                 ║
# ╚═════════════════════════════════════════════════════════════════════╝
def indicator(label, color='#22c55e', on=True, size=28):
    on_css = f'background:radial-gradient(circle at 30% 25%,#fff 0%,{color} 35%,{color} 70%,#000 100%);box-shadow:0 0 16px {color},inset 0 -2px 6px rgba(0,0,0,0.4);'
    off_css = f'background:radial-gradient(circle at 30% 25%,#374151 0%,#1f2937 60%,#000 100%);box-shadow:inset 0 -2px 4px rgba(0,0,0,0.6);'
    return f'''<div class="ind-wrap">
  <div class="ind-bezel" style="width:{size+8}px;height:{size+8}px;">
    <div class="ind-bulb" style="width:{size}px;height:{size}px;{on_css if on else off_css}"></div>
  </div>
  <div class="ind-label">{label}</div>
</div>'''


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Wooden biplane silhouette on top of panel (decorative)             ║
# ╚═════════════════════════════════════════════════════════════════════╝
def biplane():
    return '''<div class="biplane">
  <svg viewBox="0 0 280 160" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
    <defs>
      <linearGradient id="wood" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#d4a574"/>
        <stop offset="40%" stop-color="#b8864e"/>
        <stop offset="100%" stop-color="#7c5a32"/>
      </linearGradient>
      <linearGradient id="wood2" x1="0" x2="1" y1="0" y2="0">
        <stop offset="0%" stop-color="#a87a4a"/>
        <stop offset="50%" stop-color="#d4a574"/>
        <stop offset="100%" stop-color="#a87a4a"/>
      </linearGradient>
    </defs>
    <!-- lower wing -->
    <rect x="20" y="92" width="240" height="14" rx="2" fill="url(#wood2)" stroke="#5c3f1e" stroke-width="1"/>
    <!-- upper wing -->
    <rect x="20" y="42" width="240" height="14" rx="2" fill="url(#wood2)" stroke="#5c3f1e" stroke-width="1"/>
    <!-- struts between wings -->
    <line x1="60" y1="56" x2="60" y2="92" stroke="#5c3f1e" stroke-width="2.5"/>
    <line x1="220" y1="56" x2="220" y2="92" stroke="#5c3f1e" stroke-width="2.5"/>
    <line x1="100" y1="56" x2="100" y2="92" stroke="#5c3f1e" stroke-width="1.5"/>
    <line x1="180" y1="56" x2="180" y2="92" stroke="#5c3f1e" stroke-width="1.5"/>
    <!-- fuselage -->
    <path d="M 90 70 L 230 70 L 250 78 L 250 82 L 230 90 L 90 90 L 80 86 L 80 74 Z" fill="url(#wood)" stroke="#5c3f1e" stroke-width="1"/>
    <!-- propeller -->
    <ellipse cx="76" cy="80" rx="3" ry="22" fill="#5c3f1e" opacity="0.7"/>
    <!-- tail -->
    <path d="M 250 78 L 270 70 L 270 90 L 250 82 Z" fill="url(#wood)" stroke="#5c3f1e" stroke-width="1"/>
    <path d="M 248 70 L 256 50 L 264 70 Z" fill="url(#wood)" stroke="#5c3f1e" stroke-width="1"/>
    <!-- wing ribs (decorative cross-cuts) -->
    ''' + ''.join(f'<line x1="{x}" y1="42" x2="{x}" y2="56" stroke="#5c3f1e" stroke-width="0.5" opacity="0.5"/><line x1="{x}" y1="92" x2="{x}" y2="106" stroke="#5c3f1e" stroke-width="0.5" opacity="0.5"/>' for x in [40,80,120,160,200,240]) + '''
    <!-- wheels -->
    <circle cx="120" cy="120" r="10" fill="#1a1a1a" stroke="#5c3f1e" stroke-width="1.5"/>
    <circle cx="170" cy="120" r="10" fill="#1a1a1a" stroke="#5c3f1e" stroke-width="1.5"/>
    <line x1="120" y1="110" x2="120" y2="92" stroke="#5c3f1e" stroke-width="2"/>
    <line x1="170" y1="110" x2="170" y2="92" stroke="#5c3f1e" stroke-width="2"/>
  </svg>
</div>'''


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  CSS for the whole panel                                             ║
# ╚═════════════════════════════════════════════════════════════════════╝
PANEL_CSS = '''
*{box-sizing:border-box;margin:0;padding:0;}
html,body{
  background:
    radial-gradient(ellipse at 50% 100%, #2a2018 0%, #0a0805 65%, #000 100%),
    linear-gradient(180deg,#1a1410 0%,#000 100%);
  color:#e5e7eb;font-family:Helvetica,Arial,sans-serif;
  min-height:100vh;overflow-x:hidden;padding:14px;
}

/* ─── Workshop bench background blur ─── */
body::before{content:'';position:fixed;inset:0;background-image:
  radial-gradient(2px 2px at 20% 30%, rgba(251,191,36,0.4) 50%, transparent 50%),
  radial-gradient(3px 3px at 80% 60%, rgba(251,191,36,0.3) 50%, transparent 50%),
  radial-gradient(2px 2px at 50% 80%, rgba(255,255,255,0.2) 50%, transparent 50%);
  filter:blur(40px);opacity:0.5;pointer-events:none;z-index:0;}

/* ─── Title bar ─── */
.title-bar{position:relative;z-index:5;display:flex;align-items:center;gap:14px;
  padding:10px 18px;background:linear-gradient(180deg,#3a2818,#1a1208);
  border:1px solid #5c3f1e;border-radius:10px;margin:0 auto 16px;max-width:1400px;
  box-shadow:0 4px 12px rgba(0,0,0,0.6);}
.title-bar .badge{font-size:14px;font-weight:800;color:#fbbf24;letter-spacing:0.05em;
  text-shadow:0 1px 2px rgba(0,0,0,0.8);}
.title-bar .vibe{font-size:11px;color:#d4a574;opacity:0.9;}
.title-bar .nav{margin-left:auto;display:flex;gap:6px;}
.title-bar .nav a{color:#fbbf24;text-decoration:none;border:1px solid #5c3f1e;
  border-radius:5px;padding:4px 10px;font-size:11px;background:rgba(0,0,0,0.4);}

/* ─── The big panel (brushed metal) ─── */
.panel{position:relative;z-index:2;max-width:1400px;margin:0 auto;
  background:
    repeating-linear-gradient(90deg,
      rgba(255,255,255,0.04) 0px,
      rgba(255,255,255,0.04) 1px,
      transparent 1px,
      transparent 3px),
    linear-gradient(180deg,#5c6370 0%,#3a4250 25%,#2a313c 70%,#1a1f28 100%);
  border:3px solid #1a1f28;
  border-radius:14px;
  padding:80px 26px 26px;
  box-shadow:
    0 20px 60px rgba(0,0,0,0.85),
    inset 0 1px 0 rgba(255,255,255,0.18),
    inset 0 -2px 4px rgba(0,0,0,0.7);
}

/* ─── Panel screws in the corners ─── */
.screw{position:absolute;width:14px;height:14px;border-radius:50%;
  background:radial-gradient(circle at 30% 30%,#9ca3af,#1f2937 75%);
  box-shadow:inset 0 -1px 2px rgba(0,0,0,0.6),0 1px 1px rgba(0,0,0,0.4);}
.screw::before{content:'';position:absolute;inset:3px;
  background:linear-gradient(45deg,transparent 45%,#000 45%,#000 55%,transparent 55%);}
.s-tl{top:10px;left:10px;}.s-tr{top:10px;right:10px;}
.s-bl{bottom:10px;left:10px;}.s-br{bottom:10px;right:10px;}
.s-mtl{top:10px;left:50%;transform:translateX(-50%);}
.s-mbl{bottom:10px;left:50%;transform:translateX(-50%);}

/* ─── Biplane perched on top of panel ─── */
.biplane{position:absolute;top:-90px;right:50px;width:280px;height:160px;z-index:6;
  animation:float 4s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0) rotate(-1deg);}50%{transform:translateY(-6px) rotate(1deg);}}

/* ─── Gauge cluster ─── */
.gauge-cluster{display:grid;gap:10px;margin-bottom:20px;}
.gauge-row-top{grid-template-columns:repeat(3,1fr) 2fr repeat(2,1fr);align-items:center;}
.gauge{position:relative;}
.bezel{width:100%;height:100%;border-radius:50%;
  background:
    radial-gradient(circle at 30% 25%, #f3f4f6 0%, #d1d5db 8%, #6b7280 30%, #1f2937 70%, #0a0a0a 100%);
  padding:6px;
  box-shadow:
    0 6px 14px rgba(0,0,0,0.85),
    inset 0 2px 3px rgba(255,255,255,0.5),
    inset 0 -2px 3px rgba(0,0,0,0.7);
}
.face{width:100%;height:100%;border-radius:50%;position:relative;overflow:hidden;
  box-shadow:inset 0 4px 10px rgba(0,0,0,0.8);}
.face .name{position:absolute;top:60%;left:0;right:0;text-align:center;
  font-size:8px;color:#9ca3af;letter-spacing:0.18em;font-weight:700;font-family:Helvetica,sans-serif;}
.face .readout{position:absolute;top:72%;left:0;right:0;text-align:center;}
.face .readout .val{font-size:14px;color:#fbbf24;font-weight:800;font-family:'Courier New',monospace;
  text-shadow:0 0 4px rgba(251,191,36,0.6);}
.face .readout .unit{font-size:7px;color:#9ca3af;margin-left:3px;letter-spacing:0.1em;}
.face .reflection{position:absolute;top:0;left:5%;right:5%;height:40%;
  background:linear-gradient(180deg,rgba(255,255,255,0.18) 0%,transparent 80%);
  border-radius:50% 50% 0 0/100% 100% 0 0;pointer-events:none;}

/* ─── Center MEGA gauge (the orange/blue dial) ─── */
.gauge.mega{margin:0 auto;}

/* ─── Throttle levers ─── */
.throttle-bank{display:flex;gap:30px;justify-content:center;align-items:flex-end;}
.throttle-wrap{display:flex;flex-direction:column;align-items:center;gap:8px;}
.throttle-slot{position:relative;width:50px;
  background:linear-gradient(180deg,#0a0a0a 0%,#1a1a1a 100%);
  border:2px solid #000;border-radius:6px;
  box-shadow:inset 0 0 10px rgba(0,0,0,0.9),0 2px 4px rgba(255,255,255,0.05);}
.slot-rail{position:absolute;top:8px;bottom:8px;left:50%;width:6px;
  background:linear-gradient(90deg,#000,#1a1a1a 30%,#000);
  border-radius:3px;transform:translateX(-50%);
  box-shadow:inset 0 0 6px rgba(0,0,0,1);}
.slot-mark{position:absolute;left:-30px;font-size:8px;color:#fbbf24;font-weight:700;
  font-family:Helvetica,sans-serif;letter-spacing:0.05em;}
.slot-mark::after{content:'';position:absolute;left:24px;top:50%;width:8px;height:1px;background:#fbbf24;}
.lever{position:absolute;left:50%;transform:translate(-50%,50%);width:50px;height:36px;
  display:flex;flex-direction:column;align-items:center;}
.lever-stick{width:5px;height:18px;
  background:linear-gradient(90deg,#374151,#9ca3af 40%,#fff 50%,#9ca3af 60%,#374151);
  border-radius:2px;}
.lever-grip{width:36px;height:18px;border-radius:50%;
  border:1px solid #000;
  box-shadow:0 4px 8px rgba(0,0,0,0.7),inset 0 -2px 4px rgba(0,0,0,0.5);
  position:relative;display:flex;align-items:center;justify-content:center;}
.lever-cap{width:14px;height:14px;border-radius:50%;border:1px solid #000;
  box-shadow:inset 0 -1px 2px rgba(0,0,0,0.6);}
.lever-label{font-size:11px;color:#fbbf24;font-weight:800;letter-spacing:0.1em;
  text-shadow:0 1px 2px rgba(0,0,0,0.8);}
.lever-pct{font-size:14px;color:#fff;font-weight:800;font-family:'Courier New',monospace;
  background:#000;border:1px solid #fbbf24;padding:2px 8px;border-radius:3px;
  text-shadow:0 0 4px #fbbf24;box-shadow:inset 0 1px 3px rgba(251,191,36,0.4);}

/* ─── Knobs ─── */
.knob-bank{display:flex;gap:12px;justify-content:center;align-items:flex-start;flex-wrap:wrap;}
.knob-wrap{display:flex;flex-direction:column;align-items:center;gap:4px;}
.knob{position:relative;}
.lbl-tag{font-size:9px;color:#d1d5db;font-weight:700;letter-spacing:0.05em;
  font-family:Helvetica,sans-serif;text-shadow:0 1px 1px rgba(0,0,0,0.8);}
.val-tag{font-size:10px;font-family:'Courier New',monospace;font-weight:800;
  background:#000;padding:1px 5px;border-radius:2px;border:1px solid #fbbf24;}

/* ─── Toggle switches ─── */
.toggle-bank{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;
  background:linear-gradient(180deg,#1f2937,#0a0e14);
  border:2px solid #000;border-radius:6px;padding:14px 18px;
  box-shadow:inset 0 0 12px rgba(0,0,0,0.7);}
.toggle-wrap{display:flex;flex-direction:column;align-items:center;gap:5px;position:relative;}
.toggle-base{width:30px;height:36px;
  background:radial-gradient(circle at 50% 30%,#9ca3af,#1f2937 70%,#000);
  border:1px solid #000;border-radius:4px;
  box-shadow:0 2px 4px rgba(0,0,0,0.7),inset 0 1px 1px rgba(255,255,255,0.3);
  position:relative;}
.toggle-stick{position:absolute;top:6px;left:50%;width:6px;height:24px;
  background:linear-gradient(180deg,#fff,#9ca3af 40%,#374151);
  border-radius:3px;transform-origin:50% 100%;
  box-shadow:0 1px 2px rgba(0,0,0,0.6);}
.toggle-ball{position:absolute;top:-4px;left:-3px;width:12px;height:12px;border-radius:50%;
  background:radial-gradient(circle at 30% 30%,#fff,#9ca3af 50%,#1f2937);
  box-shadow:0 1px 2px rgba(0,0,0,0.7);}
.toggle-label{font-size:8px;color:#fbbf24;font-weight:800;letter-spacing:0.05em;text-align:center;}
.guard{position:absolute;top:-2px;left:50%;width:36px;height:24px;
  background:linear-gradient(180deg,#dc2626,#7f1d1d);
  border:1px solid #000;border-radius:4px 4px 0 0;
  transform:translateX(-50%) rotateX(35deg);transform-origin:bottom;
  box-shadow:0 2px 4px rgba(0,0,0,0.6);z-index:1;opacity:0.85;}

/* ─── Indicator LEDs ─── */
.ind-bank{display:flex;gap:10px;justify-content:center;
  background:linear-gradient(180deg,#1f2937,#0a0e14);
  border:2px solid #000;border-radius:6px;padding:10px 14px;
  box-shadow:inset 0 0 12px rgba(0,0,0,0.7);}
.ind-wrap{display:flex;flex-direction:column;align-items:center;gap:4px;}
.ind-bezel{border-radius:50%;
  background:radial-gradient(circle at 30% 25%,#6b7280,#1f2937 70%);
  display:grid;place-items:center;
  box-shadow:0 1px 2px rgba(0,0,0,0.7),inset 0 -1px 2px rgba(0,0,0,0.5);}
.ind-bulb{border-radius:50%;}
.ind-label{font-size:8px;color:#d1d5db;font-weight:700;letter-spacing:0.05em;}

/* ─── Joystick / control stick ─── */
.stick-wrap{display:flex;flex-direction:column;align-items:center;gap:8px;}
.stick-base{width:90px;height:30px;border-radius:50%;
  background:radial-gradient(ellipse at 50% 30%,#6b7280,#1f2937 60%,#000);
  border:2px solid #000;
  box-shadow:0 4px 8px rgba(0,0,0,0.8),inset 0 1px 1px rgba(255,255,255,0.2);}
.stick{position:relative;width:18px;height:130px;margin-top:-16px;
  background:linear-gradient(90deg,#374151,#9ca3af 40%,#fff 50%,#9ca3af 60%,#374151);
  border-radius:9px;
  box-shadow:0 4px 10px rgba(0,0,0,0.6);}
.stick-grip{position:absolute;top:-30px;left:50%;width:54px;height:60px;
  transform:translateX(-50%);
  background:linear-gradient(180deg,#1f2937 0%,#0a0a0a 100%);
  border-radius:14px 14px 8px 8px;
  border:1px solid #000;
  box-shadow:0 4px 10px rgba(0,0,0,0.8),inset 0 1px 2px rgba(255,255,255,0.15);}
.stick-button{position:absolute;top:8px;left:50%;width:20px;height:20px;
  border-radius:50%;transform:translateX(-50%);
  background:radial-gradient(circle at 30% 25%,#fef3c7,#dc2626 50%,#7f1d1d);
  border:1px solid #000;
  box-shadow:0 0 10px rgba(220,38,38,0.6),inset 0 -1px 2px rgba(0,0,0,0.5);
  animation:btnpulse 1.6s ease-in-out infinite;}
@keyframes btnpulse{0%,100%{box-shadow:0 0 10px rgba(220,38,38,0.6),inset 0 -1px 2px rgba(0,0,0,0.5);}50%{box-shadow:0 0 18px rgba(220,38,38,0.95),inset 0 -1px 2px rgba(0,0,0,0.5);}}
.stick-trigger{position:absolute;top:30px;left:-2px;width:8px;height:14px;
  background:linear-gradient(90deg,#374151,#9ca3af);border:1px solid #000;border-radius:2px 0 0 2px;}

/* ─── Display screen (matrix / line-cam) ─── */
.screen-bank{display:flex;gap:12px;justify-content:center;}
.screen{background:#000;border:2px solid #000;border-radius:4px;padding:8px;
  box-shadow:inset 0 0 16px rgba(0,0,0,1),0 0 0 4px #1f2937,0 0 0 5px #6b7280,0 4px 8px rgba(0,0,0,0.6);}
.screen .scr-label{font-size:8px;color:#22c55e;font-family:'Courier New',monospace;
  font-weight:700;letter-spacing:0.1em;margin-bottom:4px;text-shadow:0 0 4px #22c55e;}

/* ─── Speaker grill (buzzer) ─── */
.speaker{width:90px;height:90px;border-radius:50%;
  background:
    radial-gradient(circle, #000 1px, transparent 1.5px) 0 0/8px 8px,
    radial-gradient(circle at 30% 25%, #6b7280, #1f2937 70%, #000);
  border:3px solid #1f2937;
  box-shadow:0 4px 8px rgba(0,0,0,0.7),inset 0 -2px 4px rgba(0,0,0,0.6);
  display:grid;place-items:center;position:relative;}
.speaker::after{content:'♪';font-size:20px;color:#fbbf24;text-shadow:0 0 8px #fbbf24;
  animation:flicker 1.4s ease-in-out infinite;}
@keyframes flicker{0%,100%{opacity:1;}50%{opacity:0.5;}}

/* ─── Common ─── */
@keyframes blink{0%,55%{opacity:1;}56%,100%{opacity:0.2;}}
@keyframes pulse{0%,100%{opacity:0.6;}50%{opacity:1;}}

/* ─── Layout grid for the panel ─── */
.row{display:grid;gap:14px;align-items:center;margin-bottom:14px;}
.row-gauges{grid-template-columns:repeat(3,170px) 220px repeat(3,170px);justify-content:center;}
@media(max-width:1100px){.row-gauges{grid-template-columns:repeat(4,1fr);}}
.row-controls{grid-template-columns:auto 1fr auto;gap:30px;align-items:end;justify-content:space-between;}
.row-bottom{grid-template-columns:1fr 1fr 1fr;gap:14px;}

/* ─── Section divider plate ─── */
.divider{height:6px;background:linear-gradient(90deg,transparent 0%,#000 20%,#000 80%,transparent 100%);
  margin:14px 0;border-radius:3px;
  box-shadow:0 1px 0 rgba(255,255,255,0.1);}

/* ─── Tag plate (engraved label) ─── */
.tag-plate{display:inline-block;background:linear-gradient(180deg,#000,#1a1a1a);
  border:1px solid #fbbf24;color:#fbbf24;padding:3px 10px;font-size:10px;font-weight:800;
  letter-spacing:0.15em;border-radius:3px;text-shadow:0 0 4px rgba(251,191,36,0.6);
  box-shadow:inset 0 1px 2px rgba(0,0,0,0.7);}
'''


def base_html(title, body, theme='steel'):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{PANEL_CSS}{THEME_CSS.get(theme,'')}</style>
</head>
<body>
{body}
</body>
</html>'''


def title_bar(idx, name, emoji, vibe, accent='#fbbf24', dim='#5c3f1e'):
    prev_idx = (idx - 2) % 10 + 1
    next_idx = idx % 10 + 1
    return f'''<div class="title-bar">
  <div class="badge" style="color:{accent};">{emoji} v5 #{idx} · {name}</div>
  <div class="vibe">{vibe}</div>
  <div class="nav">
    <a href="cockpit-lab.html" style="color:{accent};border-color:{dim};">⚙ Gallery</a>
    <a href="cockpit-lab_{prev_idx}.html" style="color:{accent};border-color:{dim};">‹ Prev</a>
    <a href="cockpit-lab_{next_idx}.html" style="color:{accent};border-color:{dim};">Next ›</a>
  </div>
</div>'''


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Theme CSS variants — different panel materials                     ║
# ╚═════════════════════════════════════════════════════════════════════╝
THEME_CSS = {
    # Default brushed gray steel (matches #1 baseline)
    'steel': '',
    # Race car: black carbon panel + red accents
    'carbon': '''
    body{background:radial-gradient(ellipse at 50% 100%,#1a0000 0%,#000 80%),linear-gradient(180deg,#0a0000 0%,#000 100%);}
    .panel{background:repeating-linear-gradient(45deg,#1a1a1a 0,#1a1a1a 4px,#0a0a0a 4px,#0a0a0a 8px),linear-gradient(180deg,#2a2a2a 0%,#0a0a0a 100%);border-color:#7f1d1d;}
    .title-bar{background:linear-gradient(180deg,#3a0000,#1a0000);border-color:#7f1d1d;}
    ''',
    # Submarine: olive + brass
    'sub': '''
    body{background:radial-gradient(ellipse at 50% 100%,#0a1410 0%,#000 80%),linear-gradient(180deg,#0a1410 0%,#000 100%);}
    .panel{background:repeating-linear-gradient(90deg,rgba(0,0,0,0.04) 0px,rgba(0,0,0,0.04) 1px,transparent 1px,transparent 3px),linear-gradient(180deg,#3d4a32 0%,#2a3422 30%,#1a1f12 100%);border-color:#7c5a32;}
    .title-bar{background:linear-gradient(180deg,#3d4a32,#1a1f12);border-color:#7c5a32;}
    ''',
    # Spaceship: white plastic clinical + cyan accents
    'space': '''
    body{background:radial-gradient(ellipse at 50% 100%,#0a1828 0%,#000 80%),linear-gradient(180deg,#001428 0%,#000 100%);}
    .panel{background:repeating-linear-gradient(90deg,rgba(0,0,0,0.04) 0px,rgba(0,0,0,0.04) 1px,transparent 1px,transparent 3px),linear-gradient(180deg,#e5e7eb 0%,#9ca3af 35%,#4b5563 100%);border-color:#1e3a5a;}
    .title-bar{background:linear-gradient(180deg,#1e3a5a,#0a1828);border-color:#22d3ee;}
    ''',
    # Locomotive / steam: rich wood + brass
    'wood': '''
    body{background:radial-gradient(ellipse at 50% 100%,#1a0e04 0%,#000 80%),linear-gradient(180deg,#1a0e04 0%,#000 100%);}
    .panel{background:repeating-linear-gradient(90deg,rgba(255,255,255,0.04) 0px,rgba(255,255,255,0.04) 2px,transparent 2px,transparent 6px),linear-gradient(180deg,#7c5a32 0%,#5c3f1e 35%,#2a1a08 100%);border-color:#1a0e04;}
    .title-bar{background:linear-gradient(180deg,#5c3f1e,#2a1a08);border-color:#fbbf24;}
    ''',
    # Helicopter: military olive
    'olive': '''
    body{background:radial-gradient(ellipse at 50% 100%,#0a1408 0%,#000 80%),linear-gradient(180deg,#0a1408 0%,#000 100%);}
    .panel{background:repeating-linear-gradient(0deg,rgba(0,0,0,0.04) 0px,rgba(0,0,0,0.04) 1px,transparent 1px,transparent 3px),linear-gradient(180deg,#4a5328 0%,#3a4220 30%,#1a1f0e 100%);border-color:#1a1f0e;}
    .title-bar{background:linear-gradient(180deg,#3a4220,#1a1f0e);border-color:#86a232;}
    ''',
    # Sailboat: varnished mahogany + brass
    'mahogany': '''
    body{background:radial-gradient(ellipse at 50% 100%,#1a0808 0%,#000 80%),linear-gradient(180deg,#0a0404 0%,#000 100%);}
    .panel{background:repeating-linear-gradient(0deg,rgba(255,255,255,0.05) 0px,rgba(255,255,255,0.05) 1px,transparent 1px,transparent 5px),linear-gradient(180deg,#7c2818 0%,#3a0e08 60%,#1a0404 100%);border-color:#fbbf24;}
    .title-bar{background:linear-gradient(180deg,#5c1a0e,#1a0404);border-color:#fbbf24;}
    ''',
    # Excavator: hazard yellow + black
    'hazard': '''
    body{background:radial-gradient(ellipse at 50% 100%,#1a1408 0%,#000 80%),linear-gradient(180deg,#0a0804 0%,#000 100%);}
    .panel{background:repeating-linear-gradient(45deg,#fbbf24 0,#fbbf24 12px,#000 12px,#000 24px);border-color:#000;border-width:6px;}
    .panel::after{content:'';position:absolute;inset:14px;background:linear-gradient(180deg,#3a3a3a 0%,#1a1a1a 100%);border:2px solid #000;border-radius:8px;z-index:-1;}
    .title-bar{background:linear-gradient(180deg,#fbbf24,#a16207);border-color:#000;}
    .title-bar .badge,.title-bar .vibe,.title-bar .nav a{color:#000 !important;border-color:#000 !important;}
    ''',
    # Mech: military green + hex pattern overlay
    'mech': '''
    body{background:radial-gradient(ellipse at 50% 100%,#0a1810 0%,#000 80%),linear-gradient(180deg,#0a1810 0%,#000 100%);}
    .panel{background:linear-gradient(180deg,#1a3320 0%,#0e1f12 50%,#040a06 100%);border-color:#22c55e;}
    .panel::before{content:'';position:absolute;inset:0;background-image:radial-gradient(circle at 50% 50%,rgba(34,197,94,0.06) 1px,transparent 1.5px);background-size:18px 18px;pointer-events:none;border-radius:14px;}
    .title-bar{background:linear-gradient(180deg,#1a3320,#040a06);border-color:#22c55e;}
    ''',
    # Rally: vintage cream + dark brown
    'rally': '''
    body{background:radial-gradient(ellipse at 50% 100%,#1a0e04 0%,#000 80%),linear-gradient(180deg,#1a0e04 0%,#000 100%);}
    .panel{background:repeating-linear-gradient(0deg,rgba(0,0,0,0.05) 0px,rgba(0,0,0,0.05) 1px,transparent 1px,transparent 4px),linear-gradient(180deg,#d4a574 0%,#a87a4a 40%,#5c3f1e 100%);border-color:#2a1a08;}
    .title-bar{background:linear-gradient(180deg,#5c3f1e,#2a1a08);border-color:#fbbf24;}
    ''',
}


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Vehicle silhouettes (each ≈ 280×160 wooden craft model)            ║
# ╚═════════════════════════════════════════════════════════════════════╝

def vehicle_race_car():
    return '''<div class="biplane"><svg viewBox="0 0 280 140" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="rc" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#dc2626"/><stop offset="100%" stop-color="#7f1d1d"/></linearGradient></defs>
<!-- body -->
<path d="M 30 90 L 50 70 L 100 60 L 180 55 L 230 65 L 250 75 L 250 100 L 30 100 Z" fill="url(#rc)" stroke="#000" stroke-width="1.5"/>
<!-- cockpit canopy -->
<path d="M 110 60 L 130 40 L 170 40 L 180 55 Z" fill="#1f2937" opacity="0.7" stroke="#000" stroke-width="1"/>
<!-- front wing -->
<path d="M 220 90 L 270 90 L 270 100 L 220 100" fill="#000" stroke="#000" stroke-width="1"/>
<!-- rear wing -->
<path d="M 10 60 L 35 60 L 35 100 L 10 100" fill="#000" stroke="#000" stroke-width="1"/>
<!-- wheels -->
<circle cx="80" cy="105" r="14" fill="#0a0a0a" stroke="#666" stroke-width="1.5"/><circle cx="80" cy="105" r="6" fill="#9ca3af"/>
<circle cx="200" cy="105" r="14" fill="#0a0a0a" stroke="#666" stroke-width="1.5"/><circle cx="200" cy="105" r="6" fill="#9ca3af"/>
<!-- racing number -->
<text x="140" y="82" text-anchor="middle" fill="#fff" font-size="18" font-family="Helvetica" font-weight="900">7</text>
</svg></div>'''

def vehicle_submarine():
    return '''<div class="biplane"><svg viewBox="0 0 280 120" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="sb" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#a87a4a"/><stop offset="100%" stop-color="#5c3f1e"/></linearGradient></defs>
<!-- hull -->
<ellipse cx="140" cy="80" rx="120" ry="22" fill="url(#sb)" stroke="#2a1a08" stroke-width="1.5"/>
<!-- conning tower -->
<rect x="120" y="50" width="40" height="32" rx="3" fill="url(#sb)" stroke="#2a1a08" stroke-width="1.5"/>
<!-- periscope -->
<line x1="140" y1="50" x2="140" y2="20" stroke="#5c3f1e" stroke-width="3"/>
<rect x="135" y="14" width="14" height="8" fill="#1a1a1a" stroke="#000" stroke-width="0.8"/>
<!-- propeller -->
<circle cx="20" cy="80" r="14" fill="none" stroke="#5c3f1e" stroke-width="2"/>
<line x1="6" y1="80" x2="34" y2="80" stroke="#5c3f1e" stroke-width="3"/>
<line x1="20" y1="66" x2="20" y2="94" stroke="#5c3f1e" stroke-width="3"/>
<!-- portholes -->
''' + ''.join(f'<circle cx="{x}" cy="80" r="4" fill="#fbbf24" stroke="#2a1a08" stroke-width="0.8"><animate attributeName="opacity" values="1;0.6;1" dur="{1.5+i*0.2}s" repeatCount="indefinite"/></circle>' for i, x in enumerate([60,90,180,220])) + '''
</svg></div>'''

def vehicle_rocket():
    return '''<div class="biplane"><svg viewBox="0 0 200 240" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="rk" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#fff"/><stop offset="100%" stop-color="#9ca3af"/></linearGradient></defs>
<!-- nose cone -->
<path d="M 100 10 L 130 70 L 70 70 Z" fill="#dc2626" stroke="#000" stroke-width="1.5"/>
<!-- body -->
<rect x="70" y="70" width="60" height="120" fill="url(#rk)" stroke="#000" stroke-width="1.5"/>
<!-- USA stripe -->
<rect x="70" y="100" width="60" height="3" fill="#dc2626"/>
<rect x="70" y="106" width="60" height="3" fill="#1e3a5a"/>
<text x="100" y="135" text-anchor="middle" fill="#000" font-size="11" font-family="Helvetica" font-weight="900">M-Q</text>
<!-- fins -->
<path d="M 70 160 L 40 220 L 70 200 Z" fill="#dc2626" stroke="#000" stroke-width="1.5"/>
<path d="M 130 160 L 160 220 L 130 200 Z" fill="#dc2626" stroke="#000" stroke-width="1.5"/>
<!-- nozzle -->
<path d="M 80 190 L 120 190 L 130 220 L 70 220 Z" fill="#1f2937" stroke="#000" stroke-width="1.5"/>
<!-- flame -->
<path d="M 80 220 L 100 240 L 120 220 Z" fill="#fbbf24"><animate attributeName="opacity" values="1;0.6;1" dur="0.3s" repeatCount="indefinite"/></path>
</svg></div>'''

def vehicle_locomotive():
    return '''<div class="biplane"><svg viewBox="0 0 280 140" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="lo" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#7f1d1d"/><stop offset="100%" stop-color="#3a0a0a"/></linearGradient></defs>
<!-- boiler -->
<rect x="50" y="50" width="180" height="50" rx="25" fill="url(#lo)" stroke="#000" stroke-width="1.5"/>
<!-- cab -->
<rect x="200" y="30" width="60" height="60" fill="#1a1a1a" stroke="#000" stroke-width="1.5"/>
<rect x="210" y="40" width="40" height="20" fill="#fbbf24" opacity="0.7"/>
<!-- chimney -->
<rect x="80" y="20" width="22" height="35" fill="#1a1a1a" stroke="#000" stroke-width="1"/>
<rect x="76" y="14" width="30" height="8" fill="#1a1a1a" stroke="#000" stroke-width="1"/>
<!-- steam -->
<circle cx="91" cy="10" r="6" fill="#e5e7eb" opacity="0.7"><animate attributeName="cy" values="10;-10;10" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0;0.7" dur="2s" repeatCount="indefinite"/></circle>
<!-- dome -->
<rect x="130" y="40" width="20" height="14" rx="3" fill="#fbbf24" stroke="#000" stroke-width="1"/>
<!-- headlight -->
<circle cx="46" cy="70" r="8" fill="#fef3c7" stroke="#000" stroke-width="1"><animate attributeName="opacity" values="1;0.7;1" dur="2s" repeatCount="indefinite"/></circle>
<!-- wheels -->
''' + ''.join(f'<circle cx="{x}" cy="110" r="14" fill="#1a1a1a" stroke="#666" stroke-width="1.5"/><circle cx="{x}" cy="110" r="6" fill="#9ca3af"/>' for x in [80, 130, 180, 230]) + '''
<line x1="80" y1="110" x2="230" y2="110" stroke="#1a1a1a" stroke-width="3"/>
</svg></div>'''

def vehicle_helicopter():
    return '''<div class="biplane"><svg viewBox="0 0 280 140" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="hl" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#3a4220"/><stop offset="100%" stop-color="#1a1f0e"/></linearGradient></defs>
<!-- main rotor (animated) -->
<g style="transform-origin:130px 30px;animation:propspin 0.15s linear infinite;">
<rect x="20" y="28" width="220" height="4" fill="#0a0a0a" stroke="#000" stroke-width="0.5"/>
</g>
<!-- mast -->
<line x1="130" y1="32" x2="130" y2="55" stroke="#0a0a0a" stroke-width="3"/>
<!-- body -->
<ellipse cx="100" cy="75" rx="60" ry="22" fill="url(#hl)" stroke="#000" stroke-width="1.5"/>
<!-- canopy -->
<path d="M 70 60 L 100 50 L 130 55 L 130 75 L 60 75 Z" fill="#22d3ee" opacity="0.4" stroke="#000" stroke-width="1"/>
<!-- tail boom -->
<path d="M 155 70 L 240 70 L 240 80 L 155 80 Z" fill="url(#hl)" stroke="#000" stroke-width="1"/>
<!-- tail rotor -->
<g style="transform-origin:240px 75px;animation:propspin 0.1s linear infinite;">
<rect x="232" y="55" width="3" height="40" fill="#0a0a0a"/>
</g>
<!-- skids -->
<line x1="55" y1="105" x2="155" y2="105" stroke="#0a0a0a" stroke-width="3"/>
<line x1="80" y1="95" x2="80" y2="105" stroke="#0a0a0a" stroke-width="2"/>
<line x1="130" y1="95" x2="130" y2="105" stroke="#0a0a0a" stroke-width="2"/>
<!-- nav lights -->
<circle cx="50" cy="75" r="3" fill="#22c55e"><animate attributeName="opacity" values="1;0.3;1" dur="1.4s" repeatCount="indefinite"/></circle>
<circle cx="155" cy="75" r="3" fill="#ef4444"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.4s" repeatCount="indefinite"/></circle>
</svg></div>'''

def vehicle_sailboat():
    return '''<div class="biplane"><svg viewBox="0 0 240 200" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="hu" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#5c3f1e"/><stop offset="100%" stop-color="#2a1a08"/></linearGradient></defs>
<!-- mast -->
<line x1="120" y1="20" x2="120" y2="160" stroke="#5c3f1e" stroke-width="4"/>
<!-- main sail -->
<path d="M 120 25 L 120 145 L 200 130 Z" fill="#fafafa" stroke="#9ca3af" stroke-width="1.5"/>
<!-- jib -->
<path d="M 120 35 L 120 130 L 60 145 Z" fill="#fafafa" stroke="#9ca3af" stroke-width="1.5"/>
<!-- hull -->
<path d="M 30 160 Q 120 195 210 160 L 200 175 Q 120 200 40 175 Z" fill="url(#hu)" stroke="#000" stroke-width="1.5"/>
<!-- waterline -->
<line x1="20" y1="180" x2="220" y2="180" stroke="#22d3ee" stroke-width="1" stroke-dasharray="6 4" opacity="0.6"/>
<!-- pennant -->
<path d="M 120 18 L 145 14 L 120 22 Z" fill="#dc2626"><animate attributeName="d" values="M 120 18 L 145 14 L 120 22 Z;M 120 18 L 145 22 L 120 14 Z;M 120 18 L 145 14 L 120 22 Z" dur="2s" repeatCount="indefinite"/></path>
</svg></div>'''

def vehicle_excavator():
    return '''<div class="biplane"><svg viewBox="0 0 280 160" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="ex" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#fbbf24"/><stop offset="100%" stop-color="#a16207"/></linearGradient></defs>
<!-- tracks -->
<rect x="40" y="120" width="180" height="22" rx="11" fill="#1a1a1a" stroke="#000" stroke-width="1.5"/>
<!-- track wheels -->
''' + ''.join(f'<circle cx="{x}" cy="131" r="9" fill="#0a0a0a" stroke="#666" stroke-width="1"/>' for x in [55, 90, 130, 170, 205]) + '''
<!-- cab -->
<rect x="80" y="60" width="80" height="60" rx="6" fill="url(#ex)" stroke="#000" stroke-width="1.5"/>
<rect x="92" y="72" width="38" height="32" fill="#22d3ee" opacity="0.5" stroke="#000" stroke-width="1"/>
<!-- boom -->
<path d="M 160 70 L 220 30 L 235 35 L 175 80 Z" fill="url(#ex)" stroke="#000" stroke-width="1.5"/>
<!-- arm + bucket -->
<path d="M 220 30 L 260 70 L 250 80 L 215 40 Z" fill="url(#ex)" stroke="#000" stroke-width="1.5"/>
<path d="M 250 70 Q 270 80 270 95 L 245 95 Z" fill="#1a1a1a" stroke="#000" stroke-width="1.5"/>
<!-- safety light -->
<circle cx="120" cy="56" r="5" fill="#fbbf24" stroke="#000" stroke-width="1"><animate attributeName="opacity" values="1;0.3;1" dur="0.8s" repeatCount="indefinite"/></circle>
</svg></div>'''

def vehicle_mech():
    return '''<div class="biplane"><svg viewBox="0 0 200 240" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="mc" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#3a4a32"/><stop offset="100%" stop-color="#1a2418"/></linearGradient></defs>
<!-- head -->
<rect x="80" y="20" width="40" height="30" rx="3" fill="url(#mc)" stroke="#000" stroke-width="1.5"/>
<rect x="86" y="28" width="28" height="10" fill="#22c55e" opacity="0.8"><animate attributeName="opacity" values="1;0.4;1" dur="1.5s" repeatCount="indefinite"/></rect>
<!-- antenna -->
<line x1="100" y1="20" x2="100" y2="6" stroke="#666" stroke-width="2"/>
<circle cx="100" cy="5" r="2" fill="#ef4444"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></circle>
<!-- torso -->
<path d="M 60 50 L 140 50 L 150 130 L 50 130 Z" fill="url(#mc)" stroke="#000" stroke-width="1.5"/>
<!-- chest reactor -->
<circle cx="100" cy="85" r="14" fill="#22c55e" opacity="0.8" stroke="#000" stroke-width="1.5"><animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite"/></circle>
<circle cx="100" cy="85" r="6" fill="#fff"/>
<!-- arms -->
<rect x="30" y="60" width="22" height="80" rx="6" fill="url(#mc)" stroke="#000" stroke-width="1.5"/>
<rect x="148" y="60" width="22" height="80" rx="6" fill="url(#mc)" stroke="#000" stroke-width="1.5"/>
<!-- weapons (arm cannons) -->
<rect x="22" y="135" width="38" height="14" fill="#1a1a1a" stroke="#000" stroke-width="1"/>
<rect x="140" y="135" width="38" height="14" fill="#1a1a1a" stroke="#000" stroke-width="1"/>
<!-- legs -->
<rect x="65" y="130" width="28" height="80" rx="4" fill="url(#mc)" stroke="#000" stroke-width="1.5"/>
<rect x="107" y="130" width="28" height="80" rx="4" fill="url(#mc)" stroke="#000" stroke-width="1.5"/>
<!-- feet -->
<rect x="58" y="205" width="42" height="12" rx="2" fill="#0a0a0a" stroke="#000" stroke-width="1"/>
<rect x="100" y="205" width="42" height="12" rx="2" fill="#0a0a0a" stroke="#000" stroke-width="1"/>
</svg></div>'''

def vehicle_rally():
    return '''<div class="biplane"><svg viewBox="0 0 280 140" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="ra" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#1e40af"/><stop offset="100%" stop-color="#0a1834"/></linearGradient></defs>
<!-- body (rally hatchback) -->
<path d="M 30 95 L 50 65 L 220 65 L 250 80 L 250 105 L 30 105 Z" fill="url(#ra)" stroke="#000" stroke-width="1.5"/>
<!-- rally stripes -->
<rect x="100" y="65" width="6" height="40" fill="#fff"/>
<rect x="170" y="65" width="6" height="40" fill="#fff"/>
<!-- windows -->
<path d="M 60 65 L 90 35 L 200 35 L 220 65 Z" fill="#0a0a0a" opacity="0.7" stroke="#000" stroke-width="1"/>
<!-- roof rack -->
<rect x="80" y="30" width="130" height="6" fill="#1a1a1a" stroke="#000" stroke-width="1"/>
<rect x="80" y="22" width="130" height="3" fill="#fbbf24"/>
<!-- light pod (rally lights) -->
''' + ''.join(f'<circle cx="{x}" cy="22" r="6" fill="#fef3c7" stroke="#000" stroke-width="1"/>' for x in [95, 115, 175, 195]) + '''
<!-- wheels (oversized rally) -->
<circle cx="80" cy="115" r="18" fill="#0a0a0a" stroke="#9ca3af" stroke-width="2"/><circle cx="80" cy="115" r="9" fill="#9ca3af"/><circle cx="80" cy="115" r="4" fill="#fbbf24"/>
<circle cx="200" cy="115" r="18" fill="#0a0a0a" stroke="#9ca3af" stroke-width="2"/><circle cx="200" cy="115" r="9" fill="#9ca3af"/><circle cx="200" cy="115" r="4" fill="#fbbf24"/>
<!-- racing number circle -->
<circle cx="140" cy="85" r="14" fill="#fff"/><text x="140" y="91" text-anchor="middle" fill="#000" font-size="16" font-weight="900" font-family="Helvetica">42</text>
</svg></div>'''

def vehicle_spaceship():
    return '''<div class="biplane"><svg viewBox="0 0 280 140" style="width:100%;height:100%;filter:drop-shadow(0 8px 14px rgba(0,0,0,0.7));">
<defs><linearGradient id="ss" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#e5e7eb"/><stop offset="100%" stop-color="#6b7280"/></linearGradient><radialGradient id="ssg" cx="50%" cy="40%" r="50%"><stop offset="0%" stop-color="#22d3ee" stop-opacity="0.6"/><stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/></radialGradient></defs>
<!-- saucer -->
<ellipse cx="140" cy="85" rx="120" ry="20" fill="url(#ss)" stroke="#000" stroke-width="1.5"/>
<!-- dome -->
<path d="M 100 85 Q 140 30 180 85" fill="url(#ssg)" stroke="#22d3ee" stroke-width="1.5"/>
<ellipse cx="140" cy="50" rx="20" ry="10" fill="#1f2937" opacity="0.8" stroke="#22d3ee" stroke-width="0.8"/>
<!-- ring of lights -->
''' + ''.join(f'<circle cx="{30+i*23}" cy="92" r="3.5" fill="#{"22c55e" if i%2==0 else "fbbf24"}"><animate attributeName="opacity" values="1;0.3;1" dur="{1.0+i*0.1}s" repeatCount="indefinite"/></circle>' for i in range(10)) + '''
<!-- tractor beam -->
<path d="M 100 100 L 70 140 L 210 140 L 180 100 Z" fill="url(#ssg)" opacity="0.4"/>
<!-- center antenna -->
<line x1="140" y1="40" x2="140" y2="20" stroke="#666" stroke-width="2"/>
<circle cx="140" cy="18" r="3" fill="#ef4444"><animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/></circle>
</svg></div>'''


# Default biplane is already defined above; alias for clarity
vehicle_biplane = biplane


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  #1 — FLIGHT-SIM PANEL (matches workshop poster aesthetic)          ║
# ╚═════════════════════════════════════════════════════════════════════╝
def make_1():
    nav = title_bar(1, 'Flight Simulator Panel', '🛩', 'brushed metal · chrome bezels · wooden biplane')

    # Top gauge cluster: 3 small + 1 mega + 3 small
    gauges_left = (
        gauge('AIRSPEED', '42', 'KM/H', needle_deg=-30, size=140, accent='#fbbf24', danger_zone=(85,100)) +
        gauge('ATTITUDE', '−3°', 'PITCH', needle_deg=8, size=140, accent='#22d3ee') +
        gauge('ALTITUDE', '12', 'M', needle_deg=70, size=140, accent='#fbbf24')
    )
    gauges_right = (
        gauge('HEADING', '072', 'MAG', needle_deg=72, size=140, accent='#22d3ee', face='#001020') +
        gauge('VS', '+0.2', 'M/S', needle_deg=20, size=140, accent='#22c55e', swing=True) +
        gauge('TURN', 'L', 'COORD', needle_deg=-15, size=140, accent='#fbbf24')
    )
    mega_gauge = gauge('MOTOR · DUAL RPM', '156', 'RPM', needle_deg=45, size=200, accent='#fbbf24',
                       face='#1a0a08', danger_zone=(80,100))

    # Throttle bank — 2 motors L/R as real metal levers
    throttles = throttle('MOTOR L', 72, '#000') + throttle('MOTOR R', 68, '#000')

    # Joystick (control stick)
    joystick = '''<div class="stick-wrap">
  <div class="stick-base"></div>
  <div class="stick">
    <div class="stick-grip">
      <div class="stick-button"></div>
      <div class="stick-trigger"></div>
    </div>
  </div>
  <div class="tag-plate">CONTROL STICK</div>
</div>'''

    # Knob bank — servo + 4 RGB LED color knobs
    knobs_html = (
        knob('SERVO\nRUDDER', '90°', size=80, deg=0, accent='#22d3ee') +
        knob('LED·1\nRED', 'FF', size=60, deg=120, accent='#ef4444') +
        knob('LED·2\nGRN', '88', size=60, deg=-30, accent='#22c55e') +
        knob('LED·3\nBLU', 'CC', size=60, deg=60, accent='#3b82f6') +
        knob('LED·4\nAMB', '40', size=60, deg=-90, accent='#fbbf24') +
        knob('TRIM\nELEV', '0°', size=60, deg=0, accent='#fbbf24') +
        knob('TRIM\nAILE', '+5', size=60, deg=20, accent='#fbbf24') +
        knob('MIXTURE', '85%', size=60, deg=80, accent='#fbbf24')
    )

    # Toggle bank — 8 switches
    toggles_html = (
        toggle('BAT', True) + toggle('AVN', True) + toggle('BCN', True) + toggle('NAV', True) +
        toggle('PITOT', False) + toggle('STRT', False, guarded=True) +
        toggle('FUEL', True) + toggle('AP', False)
    )

    # Indicator LEDs (the 4 RGB LEDs as actual physical bulbs on the panel)
    indicators_html = (
        indicator('LED 1', '#ef4444', True) + indicator('LED 2', '#22c55e', True) +
        indicator('LED 3', '#3b82f6', True) + indicator('LED 4', '#fbbf24', True) +
        indicator('IR RX', '#f472b6', True) + indicator('GEAR', '#22c55e', True) +
        indicator('STALL', '#ef4444', False) + indicator('OIL', '#fbbf24', False)
    )

    # Bottom screens: 5x5 matrix + line-cam L/R
    matrix_html = '<div class="screen"><div class="scr-label">5×5 MATRIX</div><div style="display:grid;grid-template-columns:repeat(5,11px);gap:2.5px;">' + ''.join(
        f'<div style="width:11px;height:11px;border-radius:50%;background:{"#ef4444" if v else "#1a0500"};box-shadow:{"0 0 5px #ef4444" if v else "inset 0 0 2px #000"};"></div>'
        for v in [0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,1,0,0]
    ) + '</div></div>'

    linecam_html = '''<div class="screen"><div class="scr-label">LINE SENSORS · L / R</div>
<div style="display:flex;gap:5px;height:48px;">
  <div style="width:60px;background:#fff;border:1px solid #444;position:relative;"><div style="position:absolute;top:0;left:35%;width:10px;height:100%;background:#000;"></div><div style="position:absolute;bottom:1px;left:1px;font-size:8px;color:#22c55e;font-weight:800;font-family:monospace;">L:0</div></div>
  <div style="width:60px;background:#fff;border:1px solid #444;position:relative;"><div style="position:absolute;top:0;left:55%;width:10px;height:100%;background:#000;"></div><div style="position:absolute;bottom:1px;left:1px;font-size:8px;color:#22c55e;font-weight:800;font-family:monospace;">R:0</div></div>
</div></div>'''

    ir_html = '''<div class="screen"><div class="scr-label">IR · 38 kHz</div>
<div style="display:flex;align-items:center;gap:10px;height:48px;">
  <div style="width:22px;height:22px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#fff,#f472b6 60%,#5c1a3a);box-shadow:0 0 12px #f472b6;animation:flicker 1.4s infinite;"></div>
  <div style="font-family:monospace;color:#f472b6;font-size:14px;font-weight:800;text-shadow:0 0 4px #f472b6;">[ ▲ FWD ]</div>
</div></div>'''

    # Right column: speaker (buzzer) + battery + temp + accel as tag-plates
    sidebar_extras = '''<div style="display:flex;flex-direction:column;gap:14px;align-items:center;">
  <div class="speaker"></div>
  <div class="tag-plate">BUZZER · A4</div>
  <div style="background:#000;border:2px solid #fbbf24;border-radius:4px;padding:8px 12px;text-align:center;box-shadow:inset 0 0 8px rgba(251,191,36,0.2);">
    <div style="font-size:8px;color:#fbbf24;letter-spacing:0.15em;font-weight:700;">BATTERY</div>
    <div style="font-size:18px;color:#22c55e;font-weight:800;font-family:monospace;text-shadow:0 0 4px #22c55e;">87%</div>
    <div style="font-size:8px;color:#22c55e;font-family:monospace;">3.78V · 42min</div>
    <div style="height:8px;background:#1a1a1a;display:flex;gap:1px;padding:1px;margin-top:4px;border:1px solid #000;">''' + ''.join(f'<div style="flex:1;background:{"#22c55e" if i<8 else "#0a1a0a"};box-shadow:{"0 0 3px #22c55e" if i<8 else "none"};"></div>' for i in range(10)) + '''</div>
  </div>
  <div style="background:#000;border:2px solid #a78bfa;border-radius:4px;padding:8px 12px;text-align:center;">
    <div style="font-size:8px;color:#a78bfa;letter-spacing:0.15em;font-weight:700;">CABIN TEMP</div>
    <div style="font-size:18px;color:#a78bfa;font-weight:800;font-family:monospace;text-shadow:0 0 4px #a78bfa;">22.4°C</div>
  </div>
  <div style="background:#000;border:2px solid #22d3ee;border-radius:4px;padding:8px;text-align:center;">
    <div style="font-size:8px;color:#22d3ee;letter-spacing:0.15em;font-weight:700;">ACCEL XYZ</div>
    <div style="position:relative;width:80px;height:60px;background:radial-gradient(circle,#001020,#000);border:1px solid #1e3a5a;margin:4px auto;">
      <div style="position:absolute;top:50%;left:0;right:0;border-top:1px dashed #1e3a5a;"></div>
      <div style="position:absolute;left:50%;top:0;bottom:0;border-left:1px dashed #1e3a5a;"></div>
      <div style="position:absolute;width:10px;height:10px;border-radius:50%;background:#22d3ee;box-shadow:0 0 8px #22d3ee;top:42%;left:55%;"></div>
    </div>
    <div style="font-size:8px;color:#22d3ee;font-family:monospace;">X+0.12 Z+0.98</div>
  </div>
  <div style="background:#000;border:2px solid #a78bfa;border-radius:4px;padding:8px 12px;text-align:center;">
    <div style="font-size:8px;color:#a78bfa;letter-spacing:0.15em;font-weight:700;">MIC LEVEL</div>
    <div style="display:flex;gap:1px;height:24px;margin-top:4px;background:#0a0a0a;padding:1px;border:1px solid #1f2937;width:120px;">''' + ''.join(f'<div style="flex:1;background:linear-gradient(180deg,{"#ef4444" if i>14 else "#fbbf24" if i>10 else "#a78bfa"},#000);height:{40+(i*17)%55}%;align-self:flex-end;animation:flicker {1.0+(i%5)*0.2}s ease-in-out infinite;animation-delay:{i*0.04}s;"></div>' for i in range(18)) + '''</div>
    <div style="font-size:9px;color:#a78bfa;font-family:monospace;margin-top:3px;">−18 dB</div>
  </div>
</div>'''

    body = nav + f'''
<div class="panel">
  <!-- screws in corners + middle -->
  <div class="screw s-tl"></div><div class="screw s-tr"></div>
  <div class="screw s-bl"></div><div class="screw s-br"></div>
  <div class="screw s-mtl"></div><div class="screw s-mbl"></div>

  <!-- Wooden biplane perched on top -->
  {biplane()}

  <!-- TOP: gauge cluster (3 + mega + 3) -->
  <div class="row row-gauges">
    {gauges_left}
    <div style="display:grid;place-items:center;">{mega_gauge}</div>
    {gauges_right}
  </div>

  <div class="divider"></div>

  <!-- MIDDLE: throttles + joystick + sidebar extras -->
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:30px;align-items:start;">
    <div class="throttle-bank">{throttles}</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:18px;">
      {joystick}
      <div style="display:flex;gap:14px;align-items:center;">
        <div class="screen-bank">{ir_html}{linecam_html}{matrix_html}</div>
      </div>
    </div>
    {sidebar_extras}
  </div>

  <div class="divider"></div>

  <!-- BOTTOM: knobs row -->
  <div style="display:flex;justify-content:center;align-items:flex-start;gap:14px;flex-wrap:wrap;background:linear-gradient(180deg,#1a1f28,#0a0e14);border:2px solid #000;border-radius:8px;padding:14px;box-shadow:inset 0 0 12px rgba(0,0,0,0.6);">
    {knobs_html}
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;">
    <!-- Toggle bank -->
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
      <div class="tag-plate">SWITCH PANEL</div>
      <div class="toggle-bank">{toggles_html}</div>
    </div>
    <!-- Indicator bank -->
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
      <div class="tag-plate">INDICATOR LIGHTS</div>
      <div class="ind-bank">{indicators_html}</div>
    </div>
  </div>
</div>
'''
    return base_html('🛩 v5 #1 Flight Simulator Panel', body, theme='steel')


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Shared panel body assembler — reused by make_2..make_10            ║
# ╚═════════════════════════════════════════════════════════════════════╝
def assemble_panel(idx, name, emoji, vibe, theme, accent,
                   gauge_specs, mega_spec, throttle_l_label, throttle_r_label,
                   knob_specs, toggle_labels, ind_specs, vehicle_html,
                   stick_label='CONTROL STICK', mega_face='#1a0a08'):
    """gauge_specs: list of 6 dicts {name,val,unit,deg,accent}
       mega_spec: dict
       knob_specs: list of dicts {label,value,deg,accent,size}
       toggle_labels: list of (lbl, on, guarded)
       ind_specs: list of (lbl, color, on)
    """
    nav = title_bar(idx, name, emoji, vibe, accent=accent)

    g_left = ''.join(gauge(s['name'], s['val'], s['unit'], needle_deg=s.get('deg',45),
                          size=140, accent=s.get('accent', accent),
                          face=s.get('face','#0a1018'),
                          danger_zone=s.get('danger'), swing=s.get('swing', False))
                     for s in gauge_specs[:3])
    g_right = ''.join(gauge(s['name'], s['val'], s['unit'], needle_deg=s.get('deg',45),
                           size=140, accent=s.get('accent', accent),
                           face=s.get('face','#0a1018'),
                           danger_zone=s.get('danger'), swing=s.get('swing', False))
                      for s in gauge_specs[3:6])
    mega = gauge(mega_spec['name'], mega_spec['val'], mega_spec['unit'],
                 needle_deg=mega_spec.get('deg',45), size=200,
                 accent=mega_spec.get('accent', accent), face=mega_face,
                 danger_zone=mega_spec.get('danger',(80,100)))

    throttles = throttle(throttle_l_label, 72, '#000') + throttle(throttle_r_label, 68, '#000')

    joystick = f'''<div class="stick-wrap">
  <div class="stick-base"></div>
  <div class="stick">
    <div class="stick-grip">
      <div class="stick-button"></div>
      <div class="stick-trigger"></div>
    </div>
  </div>
  <div class="tag-plate">{stick_label}</div>
</div>'''

    knobs_html = ''.join(knob(k['label'], k.get('value',''), size=k.get('size',60),
                              deg=k.get('deg',0), accent=k.get('accent', accent))
                         for k in knob_specs)

    toggles_html = ''.join(toggle(t[0], t[1], t[2] if len(t)>2 else False)
                           for t in toggle_labels)

    indicators_html = ''.join(indicator(s[0], s[1], s[2]) for s in ind_specs)

    matrix_html = '<div class="screen"><div class="scr-label">5×5 MATRIX</div><div style="display:grid;grid-template-columns:repeat(5,11px);gap:2.5px;">' + ''.join(
        f'<div style="width:11px;height:11px;border-radius:50%;background:{"#ef4444" if v else "#1a0500"};box-shadow:{"0 0 5px #ef4444" if v else "inset 0 0 2px #000"};"></div>'
        for v in [0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,1,0,0]
    ) + '</div></div>'

    linecam_html = '''<div class="screen"><div class="scr-label">LINE SENSORS · L / R</div>
<div style="display:flex;gap:5px;height:48px;">
  <div style="width:60px;background:#fff;border:1px solid #444;position:relative;"><div style="position:absolute;top:0;left:35%;width:10px;height:100%;background:#000;"></div><div style="position:absolute;bottom:1px;left:1px;font-size:8px;color:#22c55e;font-weight:800;font-family:monospace;">L:0</div></div>
  <div style="width:60px;background:#fff;border:1px solid #444;position:relative;"><div style="position:absolute;top:0;left:55%;width:10px;height:100%;background:#000;"></div><div style="position:absolute;bottom:1px;left:1px;font-size:8px;color:#22c55e;font-weight:800;font-family:monospace;">R:0</div></div>
</div></div>'''

    ir_html = '''<div class="screen"><div class="scr-label">IR · 38 kHz</div>
<div style="display:flex;align-items:center;gap:10px;height:48px;">
  <div style="width:22px;height:22px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#fff,#f472b6 60%,#5c1a3a);box-shadow:0 0 12px #f472b6;animation:flicker 1.4s infinite;"></div>
  <div style="font-family:monospace;color:#f472b6;font-size:14px;font-weight:800;text-shadow:0 0 4px #f472b6;">[ ▲ FWD ]</div>
</div></div>'''

    sidebar_extras = '''<div style="display:flex;flex-direction:column;gap:14px;align-items:center;">
  <div class="speaker"></div>
  <div class="tag-plate">BUZZER · A4</div>
  <div style="background:#000;border:2px solid #fbbf24;border-radius:4px;padding:8px 12px;text-align:center;box-shadow:inset 0 0 8px rgba(251,191,36,0.2);">
    <div style="font-size:8px;color:#fbbf24;letter-spacing:0.15em;font-weight:700;">BATTERY</div>
    <div style="font-size:18px;color:#22c55e;font-weight:800;font-family:monospace;text-shadow:0 0 4px #22c55e;">87%</div>
    <div style="font-size:8px;color:#22c55e;font-family:monospace;">3.78V · 42min</div>
    <div style="height:8px;background:#1a1a1a;display:flex;gap:1px;padding:1px;margin-top:4px;border:1px solid #000;">''' + ''.join(f'<div style="flex:1;background:{"#22c55e" if i<8 else "#0a1a0a"};box-shadow:{"0 0 3px #22c55e" if i<8 else "none"};"></div>' for i in range(10)) + '''</div>
  </div>
  <div style="background:#000;border:2px solid #a78bfa;border-radius:4px;padding:8px 12px;text-align:center;">
    <div style="font-size:8px;color:#a78bfa;letter-spacing:0.15em;font-weight:700;">CABIN TEMP</div>
    <div style="font-size:18px;color:#a78bfa;font-weight:800;font-family:monospace;text-shadow:0 0 4px #a78bfa;">22.4°C</div>
  </div>
  <div style="background:#000;border:2px solid #22d3ee;border-radius:4px;padding:8px;text-align:center;">
    <div style="font-size:8px;color:#22d3ee;letter-spacing:0.15em;font-weight:700;">ACCEL XYZ</div>
    <div style="position:relative;width:80px;height:60px;background:radial-gradient(circle,#001020,#000);border:1px solid #1e3a5a;margin:4px auto;">
      <div style="position:absolute;top:50%;left:0;right:0;border-top:1px dashed #1e3a5a;"></div>
      <div style="position:absolute;left:50%;top:0;bottom:0;border-left:1px dashed #1e3a5a;"></div>
      <div style="position:absolute;width:10px;height:10px;border-radius:50%;background:#22d3ee;box-shadow:0 0 8px #22d3ee;top:42%;left:55%;"></div>
    </div>
    <div style="font-size:8px;color:#22d3ee;font-family:monospace;">X+0.12 Z+0.98</div>
  </div>
  <div style="background:#000;border:2px solid #a78bfa;border-radius:4px;padding:8px 12px;text-align:center;">
    <div style="font-size:8px;color:#a78bfa;letter-spacing:0.15em;font-weight:700;">MIC LEVEL</div>
    <div style="display:flex;gap:1px;height:24px;margin-top:4px;background:#0a0a0a;padding:1px;border:1px solid #1f2937;width:120px;">''' + ''.join(f'<div style="flex:1;background:linear-gradient(180deg,{"#ef4444" if i>14 else "#fbbf24" if i>10 else "#a78bfa"},#000);height:{40+(i*17)%55}%;align-self:flex-end;animation:flicker {1.0+(i%5)*0.2}s ease-in-out infinite;animation-delay:{i*0.04}s;"></div>' for i in range(18)) + '''</div>
    <div style="font-size:9px;color:#a78bfa;font-family:monospace;margin-top:3px;">−18 dB</div>
  </div>
</div>'''

    body = nav + f'''
<div class="panel">
  <div class="screw s-tl"></div><div class="screw s-tr"></div>
  <div class="screw s-bl"></div><div class="screw s-br"></div>
  <div class="screw s-mtl"></div><div class="screw s-mbl"></div>
  {vehicle_html}
  <div class="row row-gauges">
    {g_left}
    <div style="display:grid;place-items:center;">{mega}</div>
    {g_right}
  </div>
  <div class="divider"></div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:30px;align-items:start;">
    <div class="throttle-bank">{throttles}</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:18px;">
      {joystick}
      <div style="display:flex;gap:14px;align-items:center;">
        <div class="screen-bank">{ir_html}{linecam_html}{matrix_html}</div>
      </div>
    </div>
    {sidebar_extras}
  </div>
  <div class="divider"></div>
  <div style="display:flex;justify-content:center;align-items:flex-start;gap:14px;flex-wrap:wrap;background:linear-gradient(180deg,#1a1f28,#0a0e14);border:2px solid #000;border-radius:8px;padding:14px;box-shadow:inset 0 0 12px rgba(0,0,0,0.6);">
    {knobs_html}
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;">
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
      <div class="tag-plate">SWITCH PANEL</div>
      <div class="toggle-bank">{toggles_html}</div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
      <div class="tag-plate">INDICATOR LIGHTS</div>
      <div class="ind-bank">{indicators_html}</div>
    </div>
  </div>
</div>
'''
    return base_html(f'{emoji} v5 #{idx} {name}', body, theme=theme)


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  #2 — RACE CAR DASHBOARD (carbon black + red, F1 wheel feel)        ║
# ╚═════════════════════════════════════════════════════════════════════╝
def make_2():
    return assemble_panel(2, 'Race Car Dashboard', '🏎', 'carbon panel · F1 tach · pit-lane vibes',
        theme='carbon', accent='#ef4444',
        gauge_specs=[
            {'name':'TACH','val':'9800','unit':'RPM','deg':110,'accent':'#ef4444','danger':(85,100)},
            {'name':'SPEED','val':'238','unit':'KM/H','deg':80,'accent':'#fbbf24'},
            {'name':'BOOST','val':'1.4','unit':'BAR','deg':60,'accent':'#22d3ee'},
            {'name':'OIL P','val':'5.2','unit':'BAR','deg':30,'accent':'#22c55e'},
            {'name':'WATER','val':'92','unit':'°C','deg':45,'accent':'#fbbf24','danger':(75,100)},
            {'name':'FUEL','val':'24','unit':'L','deg':-50,'accent':'#fbbf24'},
        ],
        mega_spec={'name':'MOTOR · DUAL RPM','val':'9800','unit':'RPM','deg':110,'accent':'#ef4444','danger':(85,100)},
        throttle_l_label='MOTOR L', throttle_r_label='MOTOR R',
        knob_specs=[
            {'label':'SERVO\nFRONT','value':'90°','size':80,'deg':0,'accent':'#22d3ee'},
            {'label':'LED·1\nHEAD','value':'FF','accent':'#fbbf24'},
            {'label':'LED·2\nBRK','value':'FF','accent':'#ef4444'},
            {'label':'LED·3\nIND','value':'80','accent':'#fbbf24'},
            {'label':'LED·4\nREV','value':'00','accent':'#fff'},
            {'label':'BRAKE\nBIAS','value':'56F','deg':30,'accent':'#ef4444'},
            {'label':'DIFF\nMID','value':'7','deg':-20,'accent':'#fbbf24'},
            {'label':'TC','value':'4','deg':50,'accent':'#22d3ee'},
        ],
        toggle_labels=[('IGN',True),('FUEL',True),('PIT·L',False),('DRS',False),
                       ('ABS',True),('MAP',True),('STR',False,True),('KILL',False,True)],
        ind_specs=[('HEAD','#fbbf24',True),('BRAKE','#ef4444',True),('IND·L','#fbbf24',False),('REV·W','#fff',False),
                   ('IR·RX','#f472b6',True),('PIT','#22c55e',False),('DRS','#22c55e',False),('OIL','#ef4444',False)],
        vehicle_html=vehicle_race_car(),
        stick_label='STEERING WHEEL',
        mega_face='#1a0000')


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  #3 — SUBMARINE HELM (olive + brass, periscope vibes)                ║
# ╚═════════════════════════════════════════════════════════════════════╝
def make_3():
    return assemble_panel(3, 'Submarine Helm', '🚢', 'olive panel · brass dials · sonar',
        theme='sub', accent='#fbbf24',
        gauge_specs=[
            {'name':'DEPTH','val':'42','unit':'M','deg':80,'accent':'#fbbf24','danger':(85,100)},
            {'name':'O2','val':'21','unit':'%','deg':0,'accent':'#22c55e'},
            {'name':'BALLAST','val':'60','unit':'%','deg':40,'accent':'#22d3ee'},
            {'name':'COMPASS','val':'072','unit':'MAG','deg':72,'accent':'#fbbf24','face':'#001020'},
            {'name':'TRIM','val':'+2','unit':'°','deg':10,'accent':'#22c55e','swing':True},
            {'name':'SONAR','val':'PING','unit':'ACT','deg':-30,'accent':'#22d3ee'},
        ],
        mega_spec={'name':'PROPELLER · DRIVE','val':'180','unit':'RPM','deg':45,'accent':'#fbbf24','danger':(80,100)},
        throttle_l_label='SCREW L', throttle_r_label='SCREW R',
        knob_specs=[
            {'label':'SERVO\nRUDDER','value':'90°','size':80,'deg':0,'accent':'#22d3ee'},
            {'label':'LED·1\nNAV','value':'GR','accent':'#22c55e'},
            {'label':'LED·2\nALT','value':'AM','accent':'#fbbf24'},
            {'label':'LED·3\nSUB','value':'RD','accent':'#ef4444'},
            {'label':'LED·4\nTOP','value':'WT','accent':'#fff'},
            {'label':'DIVE\nPLANE','value':'5°','deg':30,'accent':'#fbbf24'},
            {'label':'BUOY\nBALL','value':'6','deg':-20,'accent':'#22d3ee'},
            {'label':'PINGER','value':'12kHz','deg':50,'accent':'#22d3ee'},
        ],
        toggle_labels=[('MAIN',True),('AUX',True),('PERI',False),('SONAR',True),
                       ('BLOW',False,True),('PURGE',False,True),('SILENT',False),('ASCND',False)],
        ind_specs=[('NAV·L','#22c55e',True),('NAV·R','#22c55e',True),('ALT','#fbbf24',True),('TOP','#fff',True),
                   ('IR·RX','#f472b6',True),('LEAK','#ef4444',False),('PING','#22d3ee',True),('OXY','#22c55e',True)],
        vehicle_html=vehicle_submarine(),
        stick_label='HELM YOKE',
        mega_face='#0a1410')


makers = [make_1, make_2, make_3]
labels = [
    ('🛩', 'Flight Simulator Panel',     'brushed metal · chrome bezels · wooden biplane'),
    ('🏎', 'Race Car Dashboard',         'carbon panel · F1 tach · pit-lane vibes'),
    ('🚢', 'Submarine Helm',             'olive panel · brass dials · sonar'),
]


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  GENERATE                                                            ║
# ╚═════════════════════════════════════════════════════════════════════╝
# Stubs for #4..#10 — populated next pass
def _stub(idx, name, emoji, vibe, theme='steel', accent='#fbbf24', vehicle_html=''):
    nav = title_bar(idx, name, emoji, vibe, accent=accent)
    body = nav + f'''<div class="panel">
  <div class="screw s-tl"></div><div class="screw s-tr"></div><div class="screw s-bl"></div><div class="screw s-br"></div>
  {vehicle_html}
  <div style="margin:80px 20px 40px;text-align:center;padding:60px 30px;border:2px dashed #5c3f1e;border-radius:14px;">
    <div style="font-size:64px;margin-bottom:14px;">{emoji}</div>
    <div style="font-size:20px;color:{accent};font-weight:800;">{name}</div>
    <div style="font-size:11px;color:#d4a574;margin-top:8px;">v5 panel · awaiting design pass</div>
  </div>
</div>'''
    return base_html(f'{emoji} v5 #{idx} {name}', body, theme=theme)

def make_4():
    return assemble_panel(4, 'Spaceship Console', '🚀', 'white plastic + cyan · holo gauges',
        theme='space', accent='#22d3ee',
        gauge_specs=[
            {'name':'VELOCITY','val':'7.8','unit':'KM/S','deg':60,'accent':'#22d3ee'},
            {'name':'O2 PRESS','val':'101','unit':'KPA','deg':10,'accent':'#22c55e'},
            {'name':'SHIELD','val':'92','unit':'%','deg':80,'accent':'#a78bfa'},
            {'name':'ATTITUDE','val':'+0','unit':'°','deg':0,'accent':'#22d3ee','face':'#001020'},
            {'name':'FUEL','val':'68','unit':'%','deg':30,'accent':'#fbbf24','swing':True},
            {'name':'COMMS','val':'LINK','unit':'OK','deg':-30,'accent':'#22c55e'},
        ],
        mega_spec={'name':'ION DRIVE · DUAL','val':'1.2','unit':'kN','deg':60,'accent':'#22d3ee','danger':(85,100)},
        throttle_l_label='THRUST L', throttle_r_label='THRUST R',
        knob_specs=[
            {'label':'SERVO\nGIMBAL','value':'90°','size':80,'deg':0,'accent':'#22d3ee'},
            {'label':'LED·1\nNAV','value':'CY','accent':'#22d3ee'},
            {'label':'LED·2\nDOCK','value':'GR','accent':'#22c55e'},
            {'label':'LED·3\nWARN','value':'AM','accent':'#fbbf24'},
            {'label':'LED·4\nEMER','value':'RD','accent':'#ef4444'},
            {'label':'WARP\nFACT','value':'2.4','deg':40,'accent':'#a78bfa'},
            {'label':'O2 MIX','value':'21%','deg':0,'accent':'#22c55e'},
            {'label':'GRAV','value':'1g','deg':30,'accent':'#22d3ee'},
        ],
        toggle_labels=[('LIFE',True),('NAV',True),('DOCK',False),('SHLD',True),
                       ('LASER',False,True),('LAUNCH',False,True),('AP',True),('COMM',True)],
        ind_specs=[('NAV','#22d3ee',True),('DOCK','#22c55e',True),('WARN','#fbbf24',False),('EMER','#ef4444',False),
                   ('IR·RX','#f472b6',True),('LIFE','#22c55e',True),('SHLD','#a78bfa',True),('FUEL','#fbbf24',True)],
        vehicle_html=vehicle_spaceship(),
        stick_label='YOKE · 6 DOF',
        mega_face='#001020')

def make_5():
    return assemble_panel(5, 'Steam Locomotive Cab', '🚂', 'wood + brass · throttle · firebox',
        theme='wood', accent='#fbbf24',
        gauge_specs=[
            {'name':'BOILER','val':'8.4','unit':'BAR','deg':70,'accent':'#fbbf24','danger':(85,100)},
            {'name':'WATER','val':'68','unit':'%','deg':20,'accent':'#22d3ee'},
            {'name':'SPEED','val':'62','unit':'KM/H','deg':50,'accent':'#fbbf24'},
            {'name':'STEAM T','val':'342','unit':'°C','deg':80,'accent':'#ef4444','danger':(80,100)},
            {'name':'COAL','val':'72','unit':'%','deg':30,'accent':'#fbbf24'},
            {'name':'BRAKE','val':'0','unit':'BAR','deg':-90,'accent':'#22c55e'},
        ],
        mega_spec={'name':'DRIVING WHEELS','val':'420','unit':'RPM','deg':50,'accent':'#fbbf24','danger':(85,100)},
        throttle_l_label='REGULATOR', throttle_r_label='REVERSER',
        knob_specs=[
            {'label':'SERVO\nVALVE','value':'90°','size':80,'deg':0,'accent':'#fbbf24'},
            {'label':'LED·1\nLAMP','value':'AM','accent':'#fbbf24'},
            {'label':'LED·2\nFIRE','value':'RD','accent':'#ef4444'},
            {'label':'LED·3\nMARK','value':'WT','accent':'#fff'},
            {'label':'LED·4\nTAIL','value':'RD','accent':'#ef4444'},
            {'label':'WHISTLE','value':'A4','deg':30,'accent':'#fbbf24'},
            {'label':'SAND','value':'OFF','deg':-60,'accent':'#fbbf24'},
            {'label':'INJCTR','value':'ON','deg':30,'accent':'#22c55e'},
        ],
        toggle_labels=[('FIRE',True),('WATER',True),('STEAM',True),('SAND',False),
                       ('BLOWR',False),('BRAKE',False,True),('WHIST',False),('LAMP',True)],
        ind_specs=[('LAMP','#fbbf24',True),('FIRE','#ef4444',True),('MARK','#fff',True),('TAIL','#ef4444',True),
                   ('IR·RX','#f472b6',True),('STEAM','#fbbf24',True),('LOW W','#ef4444',False),('OK','#22c55e',True)],
        vehicle_html=vehicle_locomotive(),
        stick_label='REGULATOR LEVER',
        mega_face='#1a0e04')

def make_6():
    return assemble_panel(6, 'Helicopter Console', '🚁', 'olive · cyclic + collective · MFDs',
        theme='olive', accent='#86a232',
        gauge_specs=[
            {'name':'ROTOR N1','val':'104','unit':'%','deg':70,'accent':'#86a232','danger':(85,100)},
            {'name':'TORQUE','val':'68','unit':'%','deg':30,'accent':'#fbbf24'},
            {'name':'V/S','val':'+200','unit':'FPM','deg':40,'accent':'#22c55e','swing':True},
            {'name':'HEADING','val':'072','unit':'MAG','deg':72,'accent':'#86a232','face':'#001020'},
            {'name':'ALT','val':'48','unit':'M','deg':50,'accent':'#fbbf24'},
            {'name':'OAT','val':'+18','unit':'°C','deg':10,'accent':'#22d3ee'},
        ],
        mega_spec={'name':'MAIN ROTOR · DUAL','val':'104','unit':'%','deg':70,'accent':'#86a232','danger':(85,100)},
        throttle_l_label='COLLECTIVE', throttle_r_label='THROTTLE',
        knob_specs=[
            {'label':'SERVO\nTAIL R','value':'90°','size':80,'deg':0,'accent':'#86a232'},
            {'label':'LED·1\nNAV·G','value':'GR','accent':'#22c55e'},
            {'label':'LED·2\nNAV·R','value':'RD','accent':'#ef4444'},
            {'label':'LED·3\nANTI','value':'WT','accent':'#fff'},
            {'label':'LED·4\nLAND','value':'AM','accent':'#fbbf24'},
            {'label':'TRIM\nCYC','value':'0','deg':0,'accent':'#86a232'},
            {'label':'GOV','value':'AUTO','deg':30,'accent':'#22c55e'},
            {'label':'PITOT','value':'ON','deg':-30,'accent':'#fbbf24'},
        ],
        toggle_labels=[('BAT',True),('GEN',True),('FUEL',True),('ANTI',True),
                       ('SLING',False,True),('FIRE',False,True),('SAR',False),('AP',False)],
        ind_specs=[('NAV·G','#22c55e',True),('NAV·R','#ef4444',True),('ANTI','#fff',True),('LAND','#fbbf24',False),
                   ('IR·RX','#f472b6',True),('FUEL','#22c55e',True),('CHIP','#fbbf24',False),('FIRE','#ef4444',False)],
        vehicle_html=vehicle_helicopter(),
        stick_label='CYCLIC STICK',
        mega_face='#0a1408')

def make_7():
    return assemble_panel(7, 'Sailboat Helm', '⛵', 'mahogany + brass · ship wheel · compass',
        theme='mahogany', accent='#fbbf24',
        gauge_specs=[
            {'name':'WIND SPD','val':'14','unit':'KT','deg':40,'accent':'#22d3ee'},
            {'name':'WIND DIR','val':'45','unit':'°','deg':45,'accent':'#fbbf24','face':'#0a0404'},
            {'name':'BOAT SPD','val':'6.2','unit':'KT','deg':30,'accent':'#22c55e'},
            {'name':'COMPASS','val':'072','unit':'MAG','deg':72,'accent':'#fbbf24','face':'#0a0404'},
            {'name':'DEPTH','val':'18','unit':'M','deg':-60,'accent':'#22d3ee'},
            {'name':'HEEL','val':'+8','unit':'°','deg':8,'accent':'#fbbf24','swing':True},
        ],
        mega_spec={'name':'AUX MOTOR · DUAL','val':'1100','unit':'RPM','deg':30,'accent':'#fbbf24','danger':(80,100)},
        throttle_l_label='AUX MOTOR', throttle_r_label='WINCH',
        knob_specs=[
            {'label':'SERVO\nRUDDER','value':'90°','size':80,'deg':0,'accent':'#fbbf24'},
            {'label':'LED·1\nMAST','value':'WT','accent':'#fff'},
            {'label':'LED·2\nPORT','value':'RD','accent':'#ef4444'},
            {'label':'LED·3\nSTB','value':'GR','accent':'#22c55e'},
            {'label':'LED·4\nSTRN','value':'WT','accent':'#fff'},
            {'label':'TRIM','value':'+5','deg':30,'accent':'#fbbf24'},
            {'label':'AUTOPI','value':'OFF','deg':-90,'accent':'#22d3ee'},
            {'label':'BILGE','value':'AUTO','deg':30,'accent':'#22c55e'},
        ],
        toggle_labels=[('NAV',True),('MAST',True),('CABIN',False),('VHF',True),
                       ('AIS',True),('GPS',True),('FOG',False),('ANCHOR',False)],
        ind_specs=[('MAST','#fff',True),('PORT','#ef4444',True),('STB','#22c55e',True),('STRN','#fff',True),
                   ('IR·RX','#f472b6',True),('BILGE','#22c55e',True),('AIS','#22d3ee',True),('GPS','#22c55e',True)],
        vehicle_html=vehicle_sailboat(),
        stick_label='SHIP WHEEL',
        mega_face='#1a0808')

def make_8():
    return assemble_panel(8, 'Excavator Operator', '🚜', 'hazard yellow · joysticks · hydraulic',
        theme='hazard', accent='#000',
        gauge_specs=[
            {'name':'HYD PRES','val':'320','unit':'BAR','deg':70,'accent':'#fbbf24','danger':(85,100)},
            {'name':'OIL T','val':'82','unit':'°C','deg':40,'accent':'#fbbf24','danger':(80,100)},
            {'name':'FUEL','val':'68','unit':'%','deg':30,'accent':'#22c55e'},
            {'name':'SWING','val':'042','unit':'°','deg':42,'accent':'#000','face':'#fbbf24'},
            {'name':'BOOM','val':'+45','unit':'°','deg':45,'accent':'#fbbf24'},
            {'name':'BUCKET','val':'+30','unit':'°','deg':30,'accent':'#fbbf24'},
        ],
        mega_spec={'name':'TRACKS · DRIVE L/R','val':'42','unit':'%','deg':30,'accent':'#fbbf24','danger':(85,100)},
        throttle_l_label='TRACK L', throttle_r_label='TRACK R',
        knob_specs=[
            {'label':'SERVO\nSWING','value':'90°','size':80,'deg':0,'accent':'#fbbf24'},
            {'label':'LED·1\nWORK','value':'AM','accent':'#fbbf24'},
            {'label':'LED·2\nBEACN','value':'AM','accent':'#fbbf24'},
            {'label':'LED·3\nREV','value':'WT','accent':'#fff'},
            {'label':'LED·4\nALARM','value':'RD','accent':'#ef4444'},
            {'label':'IDLE','value':'1200','deg':-30,'accent':'#fbbf24'},
            {'label':'POWER','value':'H','deg':30,'accent':'#000'},
            {'label':'FLOW','value':'80%','deg':10,'accent':'#fbbf24'},
        ],
        toggle_labels=[('IGN',True),('WORK',True),('BEAC',True),('TRACK',True),
                       ('LOCK',True,True),('HORN',False),('AC',True),('REV',False)],
        ind_specs=[('WORK','#fbbf24',True),('BEACN','#fbbf24',True),('REV','#fff',False),('ALARM','#ef4444',False),
                   ('IR·RX','#f472b6',True),('LOW F','#ef4444',False),('TEMP','#fbbf24',False),('OK','#22c55e',True)],
        vehicle_html=vehicle_excavator(),
        stick_label='RIGHT JOYSTICK',
        mega_face='#1a1408')

def make_9():
    return assemble_panel(9, 'Mech Pilot Console', '🤖', 'mil-green · hex grid · weapons',
        theme='mech', accent='#22c55e',
        gauge_specs=[
            {'name':'CORE','val':'94','unit':'%','deg':70,'accent':'#22c55e','danger':(85,100)},
            {'name':'HEAT','val':'42','unit':'%','deg':-20,'accent':'#ef4444','danger':(75,100)},
            {'name':'AMMO','val':'320','unit':'RDS','deg':30,'accent':'#fbbf24'},
            {'name':'SHIELD','val':'82','unit':'%','deg':50,'accent':'#22d3ee'},
            {'name':'TARGET','val':'LCKD','unit':'OK','deg':80,'accent':'#22c55e','face':'#0a1810'},
            {'name':'STRIDE','val':'+1.2','unit':'M/S','deg':20,'accent':'#22c55e','swing':True},
        ],
        mega_spec={'name':'LEG ACTUATORS · L/R','val':'2.8','unit':'M/S','deg':50,'accent':'#22c55e','danger':(80,100)},
        throttle_l_label='LEG L', throttle_r_label='LEG R',
        knob_specs=[
            {'label':'SERVO\nTORSO','value':'90°','size':80,'deg':0,'accent':'#22c55e'},
            {'label':'LED·1\nEYE','value':'GR','accent':'#22c55e'},
            {'label':'LED·2\nARM·L','value':'CY','accent':'#22d3ee'},
            {'label':'LED·3\nARM·R','value':'CY','accent':'#22d3ee'},
            {'label':'LED·4\nALARM','value':'RD','accent':'#ef4444'},
            {'label':'WPN·L','value':'AUTO','deg':30,'accent':'#22c55e'},
            {'label':'WPN·R','value':'BURST','deg':-20,'accent':'#22c55e'},
            {'label':'COOL','value':'MAX','deg':80,'accent':'#22d3ee'},
        ],
        toggle_labels=[('REACTOR',True),('SHLD',True),('SENSOR',True),('COOL',True),
                       ('WPN·L',False,True),('WPN·R',False,True),('EJCT',False,True),('AP',False)],
        ind_specs=[('EYE','#22c55e',True),('ARM·L','#22d3ee',True),('ARM·R','#22d3ee',True),('ALARM','#ef4444',False),
                   ('IR·RX','#f472b6',True),('SHLD','#22d3ee',True),('OVRHT','#ef4444',False),('TGT','#22c55e',True)],
        vehicle_html=vehicle_mech(),
        stick_label='HOTAS GRIP',
        mega_face='#0a1810')

def make_10():
    return assemble_panel(10, 'Rally Car Dashboard', '🏁', 'vintage rally · stopwatch · maps',
        theme='rally', accent='#fbbf24',
        gauge_specs=[
            {'name':'TACH','val':'7400','unit':'RPM','deg':80,'accent':'#fbbf24','danger':(85,100)},
            {'name':'SPEED','val':'128','unit':'KM/H','deg':50,'accent':'#fbbf24'},
            {'name':'OIL T','val':'92','unit':'°C','deg':45,'accent':'#fbbf24','danger':(75,100)},
            {'name':'STOPWAT','val':'02:14','unit':'M:S','deg':40,'accent':'#fbbf24','face':'#1a0e04'},
            {'name':'TRIP','val':'42.6','unit':'KM','deg':30,'accent':'#22c55e'},
            {'name':'ODO','val':'18342','unit':'KM','deg':-50,'accent':'#22d3ee'},
        ],
        mega_spec={'name':'4WD · DUAL DRIVE','val':'7400','unit':'RPM','deg':80,'accent':'#fbbf24','danger':(85,100)},
        throttle_l_label='HND BRK', throttle_r_label='THROTTLE',
        knob_specs=[
            {'label':'SERVO\nDIFF','value':'90°','size':80,'deg':0,'accent':'#fbbf24'},
            {'label':'LED·1\nHEAD','value':'WT','accent':'#fff'},
            {'label':'LED·2\nFOG','value':'AM','accent':'#fbbf24'},
            {'label':'LED·3\nROOF','value':'WT','accent':'#fff'},
            {'label':'LED·4\nBRK','value':'RD','accent':'#ef4444'},
            {'label':'WIPER','value':'2','deg':30,'accent':'#22d3ee'},
            {'label':'HEAT','value':'4','deg':-20,'accent':'#ef4444'},
            {'label':'INTRC','value':'OFF','deg':-90,'accent':'#22c55e'},
        ],
        toggle_labels=[('IGN',True),('FUEL',True),('PUMP',True),('FOG',False),
                       ('ROOF',False),('LIM',True),('NAV',True),('CO',False)],
        ind_specs=[('HEAD','#fff',True),('FOG','#fbbf24',False),('ROOF','#fff',False),('BRK','#ef4444',False),
                   ('IR·RX','#f472b6',True),('NAV','#22c55e',True),('OIL','#ef4444',False),('OK','#22c55e',True)],
        vehicle_html=vehicle_rally(),
        stick_label='STAGE NOTES',
        mega_face='#1a0e04')

makers = [make_1, make_2, make_3, make_4, make_5, make_6, make_7, make_8, make_9, make_10]
labels = [
    ('🛩', 'Flight Simulator Panel',  'brushed metal · chrome bezels · wooden biplane'),
    ('🏎', 'Race Car Dashboard',      'carbon panel · F1 tach · pit-lane vibes'),
    ('🚢', 'Submarine Helm',          'olive panel · brass dials · sonar'),
    ('🚀', 'Spaceship Console',       'white plastic + cyan · holo gauges'),
    ('🚂', 'Steam Locomotive Cab',    'wood + brass · throttle · firebox'),
    ('🚁', 'Helicopter Console',      'olive · cyclic + collective'),
    ('⛵', 'Sailboat Helm',           'mahogany + brass · ship wheel'),
    ('🚜', 'Excavator Operator',      'hazard yellow · joysticks'),
    ('🤖', 'Mech Pilot Console',      'mil-green · hex grid · weapons'),
    ('🏁', 'Rally Car Dashboard',     'vintage rally · stopwatch · maps'),
]

DONE = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
for i, maker in enumerate(makers, 1):
    out = os.path.join(OUT, f'cockpit-lab_{i}.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(maker())
    emoji, name, _ = labels[i-1]
    print(f'  + cockpit-lab_{i}.html  ({emoji} {name})')

# Tiny gallery (just 1 entry for now)
gallery = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🛩 Cockpit Lab v5 — flight simulator panel</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:Helvetica,Arial,sans-serif;
  background:linear-gradient(180deg,#1a1410,#000);
  color:#e5e7eb;padding:30px 20px 50px;min-height:100vh;}
h1{color:#fbbf24;font-size:1.8rem;margin-bottom:6px;text-align:center;text-shadow:0 1px 2px #000;}
.sub{text-align:center;color:#d4a574;margin-bottom:24px;font-size:0.95rem;max-width:780px;margin-left:auto;margin-right:auto;line-height:1.5;}
.nav{text-align:center;margin:14px 0 28px;}
.nav a{color:#d4a574;text-decoration:none;padding:6px 14px;border:1px solid #5c3f1e;border-radius:999px;font-size:0.85rem;margin:0 4px;}
.nav a:hover{color:#fbbf24;border-color:#fbbf24;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px;max-width:900px;margin:0 auto;}
.card{display:block;text-decoration:none;padding:20px 22px;border-radius:14px;
  border:1.5px solid #5c3f1e;background:linear-gradient(180deg,#3a2818,#1a1208);color:#e5e7eb;
  box-shadow:0 6px 18px rgba(0,0,0,0.7);transition:transform 0.15s,border-color 0.15s;}
.card:hover{transform:translateY(-3px);border-color:#fbbf24;}
.card .emoji{font-size:2.4rem;line-height:1;margin-bottom:8px;}
.card .num{font-family:'Courier New',monospace;font-size:0.7rem;color:#d4a574;}
.card h3{font-size:1.15rem;color:#fbbf24;margin:6px 0 8px;}
.card .vibe{font-size:0.86rem;color:#e5e7eb;opacity:0.85;line-height:1.45;}
.dna{margin-top:10px;font-size:0.78rem;color:#22d3ee;font-family:'Courier New',monospace;}
</style>
</head>
<body>
<h1>🛩 Cockpit Lab v5 — flight simulator panel</h1>
<p class="sub">Photo-realistic skeuomorphic cockpit. Brushed metal panel, chrome-bezel gauges, real throttle levers, knurled knobs, switches with shadow depth, wooden biplane perched on top — like the workshop poster.</p>
<div class="nav">
  <a href="index.html">🧪 All Labs</a>
  <a href="../index.html">🤖 Robot App</a>
  <a href="_archive/cockpit-lab/v1/gallery.html" style="opacity:0.5;">archive: v1 v2 v3 v4</a>
</div>
<div class="grid">
'''
for i, (emoji, name, vibe) in enumerate(labels, 1):
    klass = 'card' if i in DONE else 'card'
    tag = '▸ panel ready' if i in DONE else '◇ stub · pending design'
    op = '' if i in DONE else 'opacity:0.6;'
    gallery += f'''  <a class="{klass}" href="cockpit-lab_{i}.html" style="{op}">
    <div class="emoji">{emoji}</div>
    <div class="num">cockpit-lab_{i}.html</div>
    <h3>{name}</h3>
    <div class="vibe">{vibe}</div>
    <div class="dna">{tag}</div>
  </a>
'''
gallery += '''</div>
</body>
</html>
'''
with open(os.path.join(OUT, 'cockpit-lab.html'), 'w', encoding='utf-8') as f:
    f.write(gallery)
print('  + cockpit-lab.html  (gallery)')
print('Done.')
