#!/usr/bin/env python3
"""Generate cockpit-lab v3 — DENSE, REAL cockpit mockups.

v3 rules:
  - Every page packed: ~40-60 visible controls
  - All Maqueen hardware visible: 2 motors, 4 RGB LEDs, servo, buzzer,
    2 line sensors, IR receiver, 5x5 matrix, accel/compass/temp/mic/batt
  - Kid-pleaser visuals: blinking annunciators, swinging needles, hazard
    tape, knurled knobs, glowing buttons, switch covers, stickers
  - Static design only (CSS animations OK, no BLE wiring)

Re-runnable. Writes labs/cockpit-lab_v3_N.html + cockpit-lab_v3.html.
Old v1 and v2 untouched.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'labs')

# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Shared helpers — small, dense fragments used across mockups        ║
# ╚═════════════════════════════════════════════════════════════════════╝

def base_html(title, body, bg='#0a0e14', font="'JetBrains Mono', monospace", extra_css=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  html,body{{background:{bg};color:#fff;font-family:{font};min-height:100vh;overflow-x:hidden;}}
  body{{padding:10px 12px 28px;}}
  .lbl{{font-size:8px;letter-spacing:0.14em;text-transform:uppercase;opacity:0.75;}}
  .scr{{font-family:'Courier New',monospace;}}
  @keyframes blink{{0%,55%{{opacity:1;}}56%,100%{{opacity:0.18;}}}}
  @keyframes blinkfast{{0%,40%{{opacity:1;}}41%,100%{{opacity:0.2;}}}}
  @keyframes spin{{to{{transform:rotate(360deg);}}}}
  @keyframes sweep{{from{{transform:rotate(0);}}to{{transform:rotate(360deg);}}}}
  @keyframes swing{{0%,100%{{transform:rotate(-30deg);}}50%{{transform:rotate(45deg);}}}}
  @keyframes pulse{{0%,100%{{opacity:0.5;transform:scale(1);}}50%{{opacity:1;transform:scale(1.08);}}}}
  @keyframes wave{{0%{{height:20%;}}50%{{height:90%;}}100%{{height:35%;}}}}
  @keyframes scroll{{from{{transform:translateY(0);}}to{{transform:translateY(-50%);}}}}
  @keyframes flicker{{0%,100%{{opacity:1;}}48%{{opacity:0.85;}}52%{{opacity:1;}}}}
  {extra_css}
</style>
</head>
<body>
{body}
</body>
</html>'''


def nav_bar(idx, name, emoji, vibe, accent='#fbbf24', dim='#3a3328', text='#fff'):
    prev_idx = (idx - 2) % 10 + 1
    next_idx = idx % 10 + 1
    return f'''<div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:0 0 10px;background:rgba(0,0,0,0.6);border:1px solid {dim};border-radius:8px;flex-wrap:wrap;">
  <div style="font-size:13px;font-weight:800;color:{accent};letter-spacing:0.05em;margin-right:auto;">{emoji} v3 #{idx} · {name} <span style="color:#888;font-weight:400;font-size:10px;margin-left:6px;">{vibe}</span></div>
  <a href="cockpit-lab_v3.html" style="color:{text};text-decoration:none;border:1px solid {dim};border-radius:5px;padding:3px 9px;font-size:11px;">⚙ Gallery</a>
  <a href="cockpit-lab_v3_{prev_idx}.html" style="color:{text};text-decoration:none;border:1px solid {dim};border-radius:5px;padding:3px 9px;font-size:11px;">‹ Prev</a>
  <a href="cockpit-lab_v3_{next_idx}.html" style="color:{text};text-decoration:none;border:1px solid {dim};border-radius:5px;padding:3px 9px;font-size:11px;">Next ›</a>
</div>'''


# ── Round analog gauge with ticks, needle, label, numeric readout ─────
def gauge(name, val, unit, color='#fbbf24', dial_bg='#0a0804', face='#1a1408',
          needle_deg=45, swing=False, big=False):
    size = 110 if big else 78
    ticks = ''.join(
        f'<line x1="50" y1="6" x2="50" y2="{12 if i%5==0 else 9}" stroke="#aaa" stroke-width="{1.4 if i%5==0 else 0.6}" '
        f'transform="rotate({i*12} 50 50)"/>'
        for i in range(31)
    )
    nums = ''.join(
        f'<text x="50" y="20" text-anchor="middle" fill="#bba" font-size="6" font-family="monospace" '
        f'transform="rotate({i*60} 50 50) rotate({-i*60} 50 20)">{i*2}</text>'
        for i in range(6)
    )
    swing_class = 'gswing' if swing else ''
    return f'''<div class="g" style="width:{size}px;height:{size}px;background:radial-gradient(circle at 50% 40%,{face} 55%,{dial_bg} 100%);border:3px solid #2a1f10;border-radius:50%;position:relative;box-shadow:inset 0 0 12px rgba(0,0,0,0.9),0 0 6px rgba(0,0,0,0.5);display:grid;place-items:center;">
  <svg viewBox="0 0 100 100" style="position:absolute;inset:0;width:100%;height:100%;">
    {ticks}
    {nums}
    <line class="{swing_class}" x1="50" y1="50" x2="50" y2="14" stroke="{color}" stroke-width="2.4" stroke-linecap="round" transform="rotate({needle_deg} 50 50)" style="filter:drop-shadow(0 0 2px {color});transform-origin:50px 50px;"/>
    <circle cx="50" cy="50" r="3.5" fill="{color}"/>
  </svg>
  <div style="position:absolute;top:6px;left:0;right:0;text-align:center;font-size:6px;color:#bba;letter-spacing:0.15em;font-weight:700;">{name}</div>
  <div style="position:absolute;bottom:18%;left:0;right:0;text-align:center;">
    <div style="font-size:{14 if big else 11}px;color:#fff;font-weight:800;text-shadow:0 0 4px {color};font-family:monospace;">{val}</div>
    <div style="font-size:6px;color:#bba;letter-spacing:0.1em;">{unit}</div>
  </div>
</div>'''


# ── 4 RGB LEDs row, glowing ───────────────────────────────────────────
def led_bank(colors=('#ef4444', '#22c55e', '#3b82f6', '#f59e0b'), label='RGB LED BANK'):
    leds = ''.join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;">'
        f'<div style="width:22px;height:22px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,{c} 50%,{c}cc 80%);box-shadow:0 0 14px {c},0 0 4px #fff inset;animation:flicker 2.{i}s infinite;"></div>'
        f'<div style="font-size:7px;color:#bba;font-family:monospace;">L{i+1}</div>'
        f'</div>'
        for i, c in enumerate(colors)
    )
    return f'''<div style="background:linear-gradient(180deg,#1a1408,#0a0804);border:1.5px solid #3a3328;border-radius:6px;padding:8px 10px;">
  <div class="lbl" style="color:#bba;margin-bottom:6px;">{label}</div>
  <div style="display:flex;gap:14px;justify-content:space-around;">{leds}</div>
</div>'''


# ── Toggle switch row ─────────────────────────────────────────────────
def switch_row(items, on_color='#fbbf24'):
    sw = ''.join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;">'
        f'<div style="width:18px;height:30px;background:linear-gradient(180deg,#2a2218,#0a0804);border:1px solid #5c4d2a;border-radius:3px;position:relative;">'
        f'<div style="position:absolute;top:{2 if on else 16}px;left:2px;right:2px;height:12px;background:linear-gradient(135deg,{on_color if on else "#666"},#888);border-radius:2px;box-shadow:0 1px 2px rgba(0,0,0,0.6);"></div>'
        f'</div>'
        f'<div style="font-size:6.5px;color:#bba;font-family:monospace;letter-spacing:0.05em;text-align:center;">{lbl}</div>'
        f'</div>'
        for lbl, on in items
    )
    return f'<div style="display:flex;gap:6px;flex-wrap:wrap;">{sw}</div>'


# ── Round knurled knob with tick mark ─────────────────────────────────
def knob(label, value='', size=44, accent='#fbbf24', deg=120):
    bands = ''.join(
        f'<div style="position:absolute;top:50%;left:50%;width:1px;height:{size//2}px;background:#3a2818;transform-origin:0 0;transform:rotate({i*30}deg);"></div>'
        for i in range(12)
    )
    return f'''<div style="display:flex;flex-direction:column;align-items:center;gap:3px;">
  <div style="width:{size}px;height:{size}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#888,#1a1408 75%);border:2px solid #0a0804;position:relative;box-shadow:0 2px 6px rgba(0,0,0,0.7),inset 0 1px 2px rgba(255,255,255,0.15);">
    {bands}
    <div style="position:absolute;top:50%;left:50%;width:2px;height:{size//2-3}px;background:{accent};transform-origin:0 0;transform:rotate({deg}deg) translateX(-1px);box-shadow:0 0 4px {accent};"></div>
    <div style="position:absolute;inset:30%;border-radius:50%;background:radial-gradient(circle at 35% 30%,#444,#0a0804);border:1px solid #000;"></div>
  </div>
  <div style="font-size:7px;color:#bba;font-family:monospace;letter-spacing:0.05em;text-align:center;font-weight:700;">{label}</div>
  {f'<div style="font-size:8px;color:{accent};font-family:monospace;font-weight:800;">{value}</div>' if value else ''}
</div>'''


# ── Servo dial: big rotary with degree scale 0-180 ────────────────────
def servo_dial(angle=90, size=130, accent='#22d3ee'):
    ticks = ''.join(
        f'<line x1="50" y1="8" x2="50" y2="{14 if i%3==0 else 11}" stroke="#bba" stroke-width="{1.2 if i%3==0 else 0.5}" '
        f'transform="rotate({-90+i*10} 50 50)"/>'
        for i in range(19)
    )
    nums = ''.join(
        f'<text x="50" y="22" text-anchor="middle" fill="#bba" font-size="5.5" font-family="monospace" '
        f'transform="rotate({-90+i*45} 50 50) rotate({90-i*45} 50 22)">{i*45}</text>'
        for i in range(5)
    )
    return f'''<div style="background:linear-gradient(180deg,#102030,#0a0e14);border:2px solid #1e3a5a;border-radius:8px;padding:10px;">
  <div class="lbl" style="color:{accent};margin-bottom:6px;text-align:center;">SERVO · 0–180°</div>
  <div style="width:{size}px;height:{size}px;margin:0 auto;position:relative;">
    <svg viewBox="0 0 100 100" style="width:100%;height:100%;">
      <circle cx="50" cy="50" r="44" fill="none" stroke="#1e3a5a" stroke-width="1"/>
      <circle cx="50" cy="50" r="38" fill="#0a0e14" stroke="#0e1a2a" stroke-width="2"/>
      {ticks}{nums}
      <path d="M 6 50 A 44 44 0 0 1 94 50" fill="none" stroke="{accent}" stroke-width="0.6" opacity="0.4"/>
      <line x1="50" y1="50" x2="50" y2="12" stroke="{accent}" stroke-width="3" stroke-linecap="round" transform="rotate({-90+angle} 50 50)" style="filter:drop-shadow(0 0 3px {accent});"/>
      <circle cx="50" cy="50" r="4" fill="{accent}"/>
      <circle cx="50" cy="50" r="2" fill="#0a0e14"/>
    </svg>
    <div style="position:absolute;bottom:6px;left:0;right:0;text-align:center;font-family:monospace;font-size:14px;color:{accent};font-weight:800;text-shadow:0 0 6px {accent};">{angle}°</div>
  </div>
</div>'''


# ── 5x5 micro:bit LED matrix ──────────────────────────────────────────
def matrix5(pattern=None, accent='#ef4444'):
    if pattern is None:
        pattern = [
            [0,1,0,1,0],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [0,1,1,1,0],
            [0,0,1,0,0],
        ]
    cells = ''
    for r in range(5):
        for c in range(5):
            on = pattern[r][c]
            cells += f'<div style="width:14px;height:14px;border-radius:50%;background:{accent if on else "#1a0a08"};box-shadow:{"0 0 6px "+accent if on else "inset 0 0 2px #000"};"></div>'
    return f'''<div style="background:#0a0804;border:2px solid #2a1f10;border-radius:6px;padding:8px;display:inline-block;">
  <div class="lbl" style="color:#bba;margin-bottom:5px;">5×5 LED · ❤</div>
  <div style="display:grid;grid-template-columns:repeat(5,14px);gap:3px;">{cells}</div>
</div>'''


# ── IR receiver indicator with last-key bubble ────────────────────────
def ir_panel():
    return '''<div style="background:linear-gradient(180deg,#1a0814,#0a0408);border:1.5px solid #5c1a3a;border-radius:6px;padding:8px 10px;">
  <div class="lbl" style="color:#f472b6;margin-bottom:6px;">IR RECEIVER</div>
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="width:18px;height:18px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#f472b6 50%,#5c1a3a 100%);box-shadow:0 0 8px #f472b6;animation:blinkfast 1.4s infinite;"></div>
    <div style="font-family:monospace;font-size:11px;color:#f472b6;font-weight:800;">▶ KEY: <span style="color:#fff;">[OK]</span></div>
    <div style="font-family:monospace;font-size:9px;color:#888;margin-left:auto;">38kHz</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3px;margin-top:6px;">
    ''' + ''.join(
        f'<div style="background:#2a0814;border:1px solid #5c1a3a;color:#f472b6;font-family:monospace;font-size:9px;padding:3px 4px;text-align:center;font-weight:700;">{k}</div>'
        for k in ['↑','OK','↓','◄','■','►','1','2','3']
    ) + '''
  </div>
</div>'''


# ── Line-cam strip: shows L/R sensor view of track ────────────────────
def line_cam():
    return '''<div style="background:linear-gradient(180deg,#0a0e14,#000);border:1.5px solid #1e3a5a;border-radius:6px;padding:8px 10px;">
  <div class="lbl" style="color:#22d3ee;margin-bottom:6px;display:flex;justify-content:space-between;"><span>LINE-CAM · L/R</span><span style="color:#22c55e;">● TRACK</span></div>
  <div style="display:flex;gap:6px;height:42px;">
    <div style="flex:1;background:#fff;border:1px solid #444;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:35%;width:14px;height:100%;background:#000;"></div>
      <div style="position:absolute;bottom:1px;left:1px;font-size:8px;color:#22c55e;font-family:monospace;font-weight:800;">L:0</div>
    </div>
    <div style="flex:1;background:#fff;border:1px solid #444;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:55%;width:14px;height:100%;background:#000;"></div>
      <div style="position:absolute;bottom:1px;left:1px;font-size:8px;color:#22c55e;font-family:monospace;font-weight:800;">R:0</div>
    </div>
  </div>
</div>'''


# ── Throttle quadrant: 2 motors as levers ─────────────────────────────
def throttle_quadrant(left_pct=72, right_pct=68, accent='#fbbf24'):
    def lever(p, lbl):
        return f'''<div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
  <div style="width:34px;height:120px;background:linear-gradient(180deg,#1a1408 0%,#0a0804 100%);border:2px solid #2a1f10;border-radius:6px;position:relative;box-shadow:inset 0 0 8px rgba(0,0,0,0.8);">
    <div style="position:absolute;left:50%;width:1px;height:100%;background:repeating-linear-gradient(180deg,#3a2818 0,#3a2818 4px,transparent 4px,transparent 10px);transform:translateX(-50%);"></div>
    <div style="position:absolute;left:-6px;right:-6px;bottom:{p}%;height:18px;background:linear-gradient(135deg,{accent},#a16207);border:1px solid #000;border-radius:3px;box-shadow:0 0 6px {accent}66;"></div>
  </div>
  <div style="font-size:8px;color:#bba;font-family:monospace;letter-spacing:0.1em;font-weight:700;">{lbl}</div>
  <div style="font-size:11px;color:{accent};font-family:monospace;font-weight:800;">{p}%</div>
</div>'''
    return f'''<div style="background:linear-gradient(180deg,#1a1408,#0a0804);border:2px solid #2a1f10;border-radius:8px;padding:10px 14px;">
  <div class="lbl" style="color:#bba;margin-bottom:6px;text-align:center;">THROTTLE · MOTOR L/R</div>
  <div style="display:flex;gap:18px;justify-content:center;">{lever(left_pct,'L')}{lever(right_pct,'R')}</div>
</div>'''


# ── Annunciator panel: grid of warning lights ─────────────────────────
def annunciator(items):
    cells = ''.join(
        f'<div style="background:{bg};border:1px solid #000;color:{fg};font-family:monospace;font-size:8px;font-weight:900;letter-spacing:0.05em;padding:6px 4px;text-align:center;text-shadow:0 0 3px {fg};box-shadow:inset 0 0 4px rgba(0,0,0,0.6);{anim}">{lbl}</div>'
        for lbl, bg, fg, anim in items
    )
    return f'''<div style="background:#0a0804;border:2px solid #2a1f10;border-radius:6px;padding:5px;">
  <div class="lbl" style="color:#bba;margin:2px 4px 5px;">CAUTION & WARNING</div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3px;">{cells}</div>
</div>'''


# ── Compass tape strip ────────────────────────────────────────────────
def compass_tape(heading=72, accent='#22d3ee'):
    pts = list(range(-60, 61, 10))
    marks = ''.join(
        f'<div style="position:absolute;left:calc(50% + {p*1.1}%);top:0;bottom:0;border-left:1px solid #1e3a5a;display:flex;align-items:center;justify-content:center;width:30px;transform:translateX(-50%);font-size:9px;color:#bba;font-family:monospace;">{(heading+p)%360:03d}°</div>'
        for p in pts
    )
    return f'''<div style="background:linear-gradient(180deg,#0a0e14,#000);border:1.5px solid #1e3a5a;border-radius:4px;padding:6px 8px;">
  <div class="lbl" style="color:{accent};margin-bottom:4px;">HDG TAPE</div>
  <div style="position:relative;height:26px;background:#000;border:1px solid #1e3a5a;overflow:hidden;">
    {marks}
    <div style="position:absolute;left:50%;top:-2px;bottom:-2px;width:0;border-left:2px solid {accent};box-shadow:0 0 6px {accent};"></div>
    <div style="position:absolute;left:50%;top:-6px;transform:translateX(-50%);width:0;height:0;border:4px solid transparent;border-top-color:{accent};"></div>
  </div>
  <div style="text-align:center;font-family:monospace;font-size:13px;color:{accent};font-weight:800;text-shadow:0 0 4px {accent};margin-top:3px;">{heading:03d}°</div>
</div>'''


# ── Buzzer/piano keys ─────────────────────────────────────────────────
def buzzer_keys():
    keys = ''
    for i in range(8):
        keys += f'<div style="flex:1;height:46px;background:linear-gradient(180deg,#fff 0%,#ddd 95%,#888 100%);border:1px solid #333;border-radius:0 0 3px 3px;position:relative;{"box-shadow:inset 0 -8px 6px rgba(251,191,36,0.4);" if i==2 else ""}"></div>'
    blacks = ''
    positions = [13, 27, 55, 69, 83]
    for i, pos in enumerate(positions):
        blacks += f'<div style="position:absolute;left:{pos}%;top:0;width:8%;height:30px;background:linear-gradient(180deg,#1a1a1a,#000);border:1px solid #000;border-radius:0 0 2px 2px;"></div>'
    return f'''<div style="background:linear-gradient(180deg,#1a1408,#0a0804);border:1.5px solid #3a3328;border-radius:6px;padding:8px 10px;">
  <div class="lbl" style="color:#bba;margin-bottom:5px;display:flex;justify-content:space-between;"><span>BUZZER · TONE</span><span style="color:#22c55e;">♪ A4 440Hz</span></div>
  <div style="position:relative;display:flex;gap:1px;">{keys}{blacks}</div>
  <div style="display:flex;gap:2px;height:14px;margin-top:4px;background:#000;padding:1px;">
    ''' + ''.join(f'<div style="flex:1;background:linear-gradient(180deg,#22c55e,#16a34a);height:{20+(i*7)%80}%;align-self:flex-end;"></div>' for i in range(28)) + '''
  </div>
</div>'''


# ── Accel ball + tilt ─────────────────────────────────────────────────
def accel_ball(accent='#22d3ee'):
    return f'''<div style="background:linear-gradient(180deg,#0a0e14,#000);border:1.5px solid #1e3a5a;border-radius:6px;padding:8px;">
  <div class="lbl" style="color:{accent};margin-bottom:5px;">ACCEL · 3-AXIS</div>
  <div style="position:relative;width:90px;height:90px;margin:0 auto;background:radial-gradient(circle at 50% 50%,#001220 0,#000 100%);border-radius:50%;border:2px solid #1e3a5a;overflow:hidden;">
    <div style="position:absolute;inset:0;background:repeating-radial-gradient(circle,transparent 0,transparent 12px,#0e1a2a 12px,#0e1a2a 13px);"></div>
    <div style="position:absolute;top:50%;left:0;right:0;border-top:1px dashed #1e3a5a;"></div>
    <div style="position:absolute;left:50%;top:0;bottom:0;border-left:1px dashed #1e3a5a;"></div>
    <div style="position:absolute;width:14px;height:14px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,{accent} 70%);box-shadow:0 0 8px {accent};top:42%;left:55%;"></div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3px;margin-top:5px;font-family:monospace;font-size:9px;">
    <div style="background:#000;border:1px solid #1e3a5a;color:{accent};padding:2px 4px;">X:+0.12</div>
    <div style="background:#000;border:1px solid #1e3a5a;color:{accent};padding:2px 4px;">Y:-0.04</div>
    <div style="background:#000;border:1px solid #1e3a5a;color:{accent};padding:2px 4px;">Z:+0.98</div>
  </div>
</div>'''


# ── Battery panel ─────────────────────────────────────────────────────
def battery_panel():
    return '''<div style="background:linear-gradient(180deg,#0a0e14,#000);border:1.5px solid #1e3a5a;border-radius:6px;padding:8px 10px;">
  <div class="lbl" style="color:#22c55e;margin-bottom:5px;display:flex;justify-content:space-between;"><span>BATTERY · 3.7V Li</span><span>◐ 87%</span></div>
  <div style="height:14px;background:#000;border:1px solid #1e3a5a;border-radius:2px;display:flex;gap:1px;padding:1px;">
    ''' + ''.join(f'<div style="flex:1;background:{"linear-gradient(180deg,#22c55e,#16a34a)" if i<8 else "#0a1808"};box-shadow:{"0 0 4px #22c55e" if i<8 else "none"};"></div>' for i in range(10)) + '''
  </div>
  <div style="display:flex;justify-content:space-between;font-family:monospace;font-size:9px;color:#22c55e;margin-top:3px;font-weight:700;">
    <span>3.78V</span><span>−0.12A</span><span>~42min</span>
  </div>
</div>'''


# ── Mic VU + waveform ─────────────────────────────────────────────────
def mic_vu():
    return '''<div style="background:linear-gradient(180deg,#0a0e14,#000);border:1.5px solid #1e3a5a;border-radius:6px;padding:8px 10px;">
  <div class="lbl" style="color:#a78bfa;margin-bottom:5px;display:flex;justify-content:space-between;"><span>MIC · LEVEL</span><span>−18dB</span></div>
  <div style="display:flex;gap:1px;height:24px;background:#000;padding:1px;border:1px solid #1e3a5a;">
    ''' + ''.join(f'<div style="flex:1;background:linear-gradient(180deg,{"#ef4444" if i>22 else "#fbbf24" if i>16 else "#22c55e"},#000);height:{40+(i*11)%55}%;align-self:flex-end;animation:wave {1.0+(i%6)*0.15:.2f}s ease-in-out infinite;animation-delay:{i*0.04}s;"></div>' for i in range(28)) + '''
  </div>
</div>'''


# ── Hazard tape stripe ────────────────────────────────────────────────
def hazard_stripe(height=8):
    return f'<div style="height:{height}px;background:repeating-linear-gradient(45deg,#fbbf24 0,#fbbf24 10px,#000 10px,#000 20px);border-radius:2px;"></div>'


# ── Big circular gauge w/ ARC progress (for speed/RPM) ────────────────
def arc_gauge(name, val, unit, pct, color='#fbbf24', size=140):
    # arc from -135deg to +135deg (270deg total)
    deg_per_pct = 270 / 100
    end_angle = -135 + pct * deg_per_pct
    import math
    a1 = math.radians(-135)
    a2 = math.radians(end_angle)
    x1 = 50 + 38*math.cos(a1)
    y1 = 50 + 38*math.sin(a1)
    x2 = 50 + 38*math.cos(a2)
    y2 = 50 + 38*math.sin(a2)
    large = 1 if pct > 50 else 0
    ticks = ''.join(
        f'<line x1="50" y1="6" x2="50" y2="{14 if i%5==0 else 10}" stroke="#bba" stroke-width="{1.4 if i%5==0 else 0.6}" '
        f'transform="rotate({-135+i*9} 50 50)"/>'
        for i in range(31)
    )
    nums = ''.join(
        f'<text x="50" y="22" text-anchor="middle" fill="#bba" font-size="6" font-family="monospace" '
        f'transform="rotate({-135+i*54} 50 50) rotate({135-i*54} 50 22)">{i*2}</text>'
        for i in range(6)
    )
    return f'''<div style="width:{size}px;height:{size}px;background:radial-gradient(circle at 50% 40%,#1a1408 55%,#0a0804 100%);border:3px solid #2a1f10;border-radius:50%;position:relative;box-shadow:inset 0 0 14px rgba(0,0,0,0.9),0 0 8px rgba(0,0,0,0.5);">
  <svg viewBox="0 0 100 100" style="position:absolute;inset:0;width:100%;height:100%;">
    <path d="M {50+38*math.cos(math.radians(-135)):.2f} {50+38*math.sin(math.radians(-135)):.2f} A 38 38 0 1 1 {50+38*math.cos(math.radians(135)):.2f} {50+38*math.sin(math.radians(135)):.2f}" fill="none" stroke="#1a1408" stroke-width="6"/>
    <path d="M {x1:.2f} {y1:.2f} A 38 38 0 {large} 1 {x2:.2f} {y2:.2f}" fill="none" stroke="{color}" stroke-width="6" stroke-linecap="round" style="filter:drop-shadow(0 0 4px {color});"/>
    {ticks}{nums}
    <line x1="50" y1="50" x2="50" y2="14" stroke="{color}" stroke-width="2.5" stroke-linecap="round" transform="rotate({end_angle+90} 50 50)" style="filter:drop-shadow(0 0 3px {color});"/>
    <circle cx="50" cy="50" r="4" fill="{color}"/>
  </svg>
  <div style="position:absolute;top:14px;left:0;right:0;text-align:center;font-size:8px;color:#bba;letter-spacing:0.15em;font-weight:700;">{name}</div>
  <div style="position:absolute;bottom:24%;left:0;right:0;text-align:center;">
    <div style="font-size:22px;color:#fff;font-weight:800;text-shadow:0 0 6px {color};font-family:monospace;">{val}</div>
    <div style="font-size:8px;color:#bba;letter-spacing:0.1em;">{unit}</div>
  </div>
</div>'''


# ── Screw decoration in corner ────────────────────────────────────────
SCREW = '<div style="position:absolute;width:8px;height:8px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#888,#222);box-shadow:0 1px 1px rgba(0,0,0,0.6);"></div>'

def screws():
    return f'''<div style="position:absolute;inset:0;pointer-events:none;">
  <div style="position:absolute;top:6px;left:6px;">{SCREW}</div>
  <div style="position:absolute;top:6px;right:6px;">{SCREW}</div>
  <div style="position:absolute;bottom:6px;left:6px;">{SCREW}</div>
  <div style="position:absolute;bottom:6px;right:6px;">{SCREW}</div>
</div>'''


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  #1 — PLANE COCKPIT (DENSE: 6-pack + radio + breakers + quadrant)   ║
# ╚═════════════════════════════════════════════════════════════════════╝
def make_1():
    nav = nav_bar(1, 'Plane Cockpit', '🛩', 'dense 6-pack · radio · breakers',
                  accent='#fbbf24', dim='#3a2818')

    # 6-pack
    six_pack = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;background:#0a0804;border:3px solid #2a1f10;border-radius:8px;padding:8px;">'
    for n, v, u, d, sw in [
        ('AIRSPEED','42','KM/H',-30,True),
        ('ATTITUDE','-3°','PITCH',5,False),
        ('ALTITUDE','12','M',60,False),
        ('TURN','L','COORD',-15,False),
        ('HEADING','072','MAG',0,False),
        ('VS','+0.2','M/S',20,True),
    ]:
        six_pack += gauge(n, v, u, color='#fbbf24', needle_deg=d, swing=sw)
    six_pack += '</div>'

    # Radio stack
    radio = '<div style="background:#0a0804;border:2px solid #2a1f10;border-radius:6px;padding:8px;">'
    radio += '<div class="lbl" style="color:#bba;margin-bottom:5px;">COM/NAV STACK</div>'
    for lbl, freq, color in [
        ('COM1','118.350','#22c55e'),('COM2','121.500','#22c55e'),
        ('NAV1','110.30','#fbbf24'),('NAV2','115.60','#fbbf24'),
        ('XPDR','7000','#f472b6'),('ADF ','335','#a78bfa'),
    ]:
        radio += f'<div style="display:flex;justify-content:space-between;align-items:center;background:#000;border:1px solid #2a1f10;padding:4px 8px;margin-bottom:3px;font-family:\'Courier New\',monospace;"><span style="font-size:9px;color:#bba;font-weight:700;">{lbl}</span><span style="font-size:13px;color:{color};font-weight:800;text-shadow:0 0 4px {color};">{freq}</span></div>'
    radio += '</div>'

    # Annunciator
    ann = annunciator([
        ('MASTER','linear-gradient(180deg,#7f1d1d,#450a0a)','#fca5a5','animation:blink 1s infinite;'),
        ('OIL','linear-gradient(180deg,#78350f,#451a03)','#fbbf24',''),
        ('FUEL','linear-gradient(180deg,#78350f,#451a03)','#fbbf24',''),
        ('GEAR','linear-gradient(180deg,#14532d,#052e16)','#86efac',''),
        ('STARTER','#1a1408','#666',''),
        ('PITOT','linear-gradient(180deg,#78350f,#451a03)','#fbbf24',''),
        ('STALL','#1a1408','#666',''),
        ('AP','linear-gradient(180deg,#14532d,#052e16)','#86efac',''),
        ('NAV','linear-gradient(180deg,#14532d,#052e16)','#86efac',''),
        ('LIGHTS','linear-gradient(180deg,#14532d,#052e16)','#86efac',''),
        ('PROP','#1a1408','#666',''),
        ('GEN','linear-gradient(180deg,#14532d,#052e16)','#86efac',''),
    ])

    # Circuit breaker / switch row
    breakers = '<div style="background:#0a0804;border:2px solid #2a1f10;border-radius:6px;padding:8px;">'
    breakers += '<div class="lbl" style="color:#bba;margin-bottom:6px;">SWITCH PANEL</div>'
    breakers += switch_row([
        ('BAT',True),('ALT',True),('AVN',True),('FUEL',True),
        ('BCN',True),('NAV',True),('STRB',False),('LDG',False),
        ('TAXI',False),('PITOT',True),('PROP',False),('AP',False),
    ])
    breakers += '</div>'

    body = nav + f'''
<div style="max-width:1400px;margin:0 auto;display:grid;grid-template-columns:1fr 2fr 1fr;gap:8px;">

  <!-- LEFT panel -->
  <div style="display:flex;flex-direction:column;gap:8px;">
    {throttle_quadrant(72,68,'#fbbf24')}
    {servo_dial(135, accent='#fbbf24')}
    {led_bank(label='NAV LIGHTS · 4 RGB')}
  </div>

  <!-- CENTER -->
  <div style="display:flex;flex-direction:column;gap:8px;">
    {six_pack}
    {ann}
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
      {compass_tape(72,'#fbbf24')}
      {accel_ball('#fbbf24')}
    </div>
    {breakers}
    {buzzer_keys()}
  </div>

  <!-- RIGHT panel -->
  <div style="display:flex;flex-direction:column;gap:8px;">
    {radio}
    {matrix5(accent='#ef4444')}
    {ir_panel()}
    {line_cam()}
    {mic_vu()}
    {battery_panel()}
    {hazard_stripe()}
  </div>

</div>
'''
    return base_html('🛩 v3 #1 Plane Cockpit', body, bg='#0d0a04')


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Stubs for #2..#10 — will be filled in next iterations              ║
# ╚═════════════════════════════════════════════════════════════════════╝
def _stub(idx, name, emoji, vibe):
    return base_html(f'{emoji} v3 #{idx} {name}',
        nav_bar(idx, name, emoji, vibe) +
        f'<div style="max-width:900px;margin:60px auto;text-align:center;padding:40px;border:2px dashed #444;border-radius:14px;"><div style="font-size:48px;margin-bottom:14px;">{emoji}</div><div style="font-size:18px;color:#888;">{name}</div><div style="font-size:12px;color:#555;margin-top:8px;">v3 dense build · coming next</div></div>')

# ╔═════════════════════════════════════════════════════════════════════╗
# ║  #2 — GLASS COCKPIT AIRLINER (PFD/ND/EICAS/SYS + FCU + overhead)    ║
# ╚═════════════════════════════════════════════════════════════════════╝
def make_2():
    nav = nav_bar(2, 'Glass Cockpit (Airliner)', '✈️', '4 MFDs · FCU · overhead',
                  accent='#22d3ee', dim='#1e3a5a')

    # PFD (Primary Flight Display) — artificial horizon + speed/alt tapes
    pfd = '''<div style="background:#000;border:2px solid #1e3a5a;border-radius:6px;padding:6px;height:280px;position:relative;overflow:hidden;">
  <div class="lbl" style="color:#22d3ee;margin-bottom:4px;">PFD · PRIMARY FLIGHT</div>
  <!-- horizon -->
  <div style="position:absolute;top:24px;left:60px;right:60px;bottom:30px;background:linear-gradient(180deg,#3b82f6 0%,#3b82f6 48%,#92400e 52%,#451a03 100%);overflow:hidden;border:1px solid #1e3a5a;">
    <!-- pitch ladder -->
    <div style="position:absolute;top:50%;left:0;right:0;height:1px;background:#fff;"></div>
    ''' + ''.join(f'<div style="position:absolute;top:calc(50% + {p*8}px);left:25%;right:25%;height:1px;background:#fff;opacity:0.7;"><span style="position:absolute;left:-18px;top:-6px;color:#fff;font-size:8px;font-family:monospace;">{abs(p)*5:02d}</span></div>' for p in range(-3,4) if p!=0) + '''
    <!-- aircraft symbol -->
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);">
      <svg width="60" height="20"><line x1="0" y1="10" x2="22" y2="10" stroke="#fbbf24" stroke-width="3"/><line x1="38" y1="10" x2="60" y2="10" stroke="#fbbf24" stroke-width="3"/><circle cx="30" cy="10" r="3" fill="#fbbf24"/></svg>
    </div>
    <!-- bank pointer top -->
    <div style="position:absolute;top:4px;left:50%;transform:translateX(-50%);width:0;height:0;border:6px solid transparent;border-bottom-color:#fbbf24;"></div>
  </div>
  <!-- speed tape left -->
  <div style="position:absolute;top:24px;left:6px;width:50px;bottom:30px;background:#0a0e14;border:1px solid #1e3a5a;font-family:monospace;font-size:9px;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;">
    <div style="opacity:0.5;">220</div><div style="opacity:0.7;">200</div><div style="opacity:0.85;">180</div>
    <div style="background:#fbbf24;color:#000;font-weight:800;font-size:13px;padding:2px 6px;margin:2px 0;border:1px solid #fff;">160</div>
    <div style="opacity:0.85;">140</div><div style="opacity:0.7;">120</div><div style="opacity:0.5;">100</div>
    <div class="lbl" style="color:#22d3ee;margin-top:3px;">KTS</div>
  </div>
  <!-- alt tape right -->
  <div style="position:absolute;top:24px;right:6px;width:50px;bottom:30px;background:#0a0e14;border:1px solid #1e3a5a;font-family:monospace;font-size:9px;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;">
    <div style="opacity:0.5;">8500</div><div style="opacity:0.7;">8000</div><div style="opacity:0.85;">7500</div>
    <div style="background:#22c55e;color:#000;font-weight:800;font-size:11px;padding:2px 4px;margin:2px 0;border:1px solid #fff;">7000</div>
    <div style="opacity:0.85;">6500</div><div style="opacity:0.7;">6000</div><div style="opacity:0.5;">5500</div>
    <div class="lbl" style="color:#22d3ee;margin-top:3px;">FT</div>
  </div>
  <!-- HDG bottom -->
  <div style="position:absolute;bottom:4px;left:50%;transform:translateX(-50%);background:#000;border:1px solid #fbbf24;color:#fbbf24;font-family:monospace;font-size:13px;font-weight:800;padding:2px 12px;text-shadow:0 0 4px #fbbf24;">072</div>
</div>'''

    # ND (Navigation Display) — compass rose + waypoints
    nd = '''<div style="background:#000;border:2px solid #1e3a5a;border-radius:6px;padding:6px;height:280px;position:relative;overflow:hidden;">
  <div class="lbl" style="color:#22d3ee;margin-bottom:4px;">ND · NAVIGATION</div>
  <svg viewBox="0 0 200 240" style="width:100%;height:calc(100% - 16px);">
    <!-- compass rose -->
    <circle cx="100" cy="180" r="120" fill="none" stroke="#1e3a5a" stroke-width="0.5"/>
    <circle cx="100" cy="180" r="100" fill="none" stroke="#1e3a5a" stroke-width="1"/>
    <circle cx="100" cy="180" r="80" fill="none" stroke="#1e3a5a" stroke-width="0.5"/>
    <circle cx="100" cy="180" r="60" fill="none" stroke="#1e3a5a" stroke-width="0.5"/>
    ''' + ''.join(f'<line x1="100" y1="60" x2="100" y2="{72 if i%3==0 else 68}" stroke="#fff" stroke-width="{1.4 if i%3==0 else 0.6}" transform="rotate({i*10} 100 180)"/>' for i in range(36)) + '''
    ''' + ''.join(f'<text x="100" y="56" text-anchor="middle" fill="#fff" font-size="9" font-family="monospace" transform="rotate({i*30} 100 180) rotate({-i*30} 100 56)">{i*3 if i*3<10 else i*3 if i!=0 else "N"}</text>' for i in range(12)) + '''
    <!-- aircraft symbol -->
    <polygon points="100,180 92,196 100,192 108,196" fill="#fbbf24" stroke="#fff" stroke-width="0.5"/>
    <!-- track line -->
    <line x1="100" y1="180" x2="100" y2="80" stroke="#22ff88" stroke-width="1.5" stroke-dasharray="4 2"/>
    <!-- waypoints -->
    <circle cx="100" cy="120" r="4" fill="none" stroke="#a78bfa" stroke-width="1.5"/>
    <text x="108" y="124" fill="#a78bfa" font-size="9" font-family="monospace">WP1</text>
    <circle cx="115" cy="80" r="4" fill="none" stroke="#a78bfa" stroke-width="1.5"/>
    <text x="123" y="84" fill="#a78bfa" font-size="9" font-family="monospace">WP2</text>
    <!-- range rings -->
    <text x="100" y="78" text-anchor="middle" fill="#22d3ee" font-size="7" font-family="monospace">10</text>
    <text x="100" y="98" text-anchor="middle" fill="#22d3ee" font-size="7" font-family="monospace">20</text>
  </svg>
  <div style="position:absolute;top:8px;right:8px;background:#000;border:1px solid #22c55e;color:#22c55e;font-family:monospace;font-size:9px;padding:2px 6px;font-weight:800;">GS 142kt</div>
  <div style="position:absolute;top:8px;left:60px;background:#000;border:1px solid #fbbf24;color:#fbbf24;font-family:monospace;font-size:9px;padding:2px 6px;font-weight:800;">TRK 075</div>
</div>'''

    # EICAS (Engine Indicating)
    eicas = '<div style="background:#000;border:2px solid #1e3a5a;border-radius:6px;padding:8px;">'
    eicas += '<div class="lbl" style="color:#22d3ee;margin-bottom:6px;">EICAS · ENGINES</div>'
    eicas += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">'
    for n, val, unit, pct, c in [('N1·L','82','%RPM',82,'#22c55e'),('N1·R','78','%RPM',78,'#22c55e'),('EGT·L','580','°C',60,'#fbbf24'),('EGT·R','572','°C',58,'#fbbf24'),('FF·L','1.2','T/H',45,'#22d3ee'),('FF·R','1.18','T/H',44,'#22d3ee')]:
        eicas += f'''<div style="background:#0a0e14;border:1px solid #1e3a5a;padding:5px 6px;">
  <div style="display:flex;justify-content:space-between;align-items:baseline;"><span style="font-size:9px;color:#bba;font-family:monospace;">{n}</span><span style="font-size:7px;color:#bba;">{unit}</span></div>
  <div style="font-size:18px;color:{c};font-weight:800;font-family:monospace;text-shadow:0 0 4px {c};">{val}</div>
  <div style="height:4px;background:#1e3a5a;border-radius:2px;overflow:hidden;margin-top:2px;"><div style="width:{pct}%;height:100%;background:{c};box-shadow:0 0 4px {c};"></div></div>
</div>'''
    eicas += '</div></div>'

    # SYS (System) display: hydraulics/elec/fuel mini schematic
    sys = '<div style="background:#000;border:2px solid #1e3a5a;border-radius:6px;padding:8px;">'
    sys += '<div class="lbl" style="color:#22d3ee;margin-bottom:6px;">SYS · ECAM</div>'
    sys += '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4px;font-family:monospace;font-size:9px;">'
    for n, val, c in [('HYD·G','3000PSI','#22c55e'),('HYD·B','2980PSI','#22c55e'),('HYD·Y','3010PSI','#22c55e'),('AC·1','115V','#22c55e'),('AC·2','115V','#22c55e'),('DC·BAT','27.8V','#fbbf24'),('FUEL·1','420kg','#22c55e'),('FUEL·2','418kg','#22c55e')]:
        sys += f'<div style="background:#0a0e14;border:1px solid #1e3a5a;padding:4px;text-align:center;"><div style="color:#bba;font-size:7px;">{n}</div><div style="color:{c};font-size:10px;font-weight:800;text-shadow:0 0 3px {c};">{val}</div></div>'
    sys += '</div></div>'

    # FCU (Flight Control Unit) — autopilot panel
    fcu = '<div style="background:linear-gradient(180deg,#1a1f2a,#0a0e14);border:2px solid #1e3a5a;border-radius:6px;padding:8px;">'
    fcu += '<div class="lbl" style="color:#22d3ee;margin-bottom:6px;">FCU · AUTOPILOT</div>'
    fcu += '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;font-family:monospace;">'
    for n, v in [('SPD','160'),('HDG','072'),('ALT','7000'),('V/S','+200')]:
        fcu += f'<div style="background:#000;border:1px solid #1e3a5a;padding:5px;text-align:center;"><div style="font-size:7px;color:#bba;">{n}</div><div style="font-size:14px;color:#fbbf24;font-weight:800;text-shadow:0 0 4px #fbbf24;">{v}</div></div>'
    fcu += '</div>'
    fcu += '<div style="display:flex;gap:5px;margin-top:6px;flex-wrap:wrap;">'
    for k in ['AP1','AP2','A/THR','LOC','APPR','EXPED']:
        fcu += f'<button style="background:linear-gradient(180deg,#1a3a1a,#0a1a0a);border:1px solid #22c55e;color:#22c55e;font-family:monospace;font-size:9px;font-weight:800;padding:4px 8px;letter-spacing:0.05em;cursor:pointer;text-shadow:0 0 3px #22c55e;">{k}</button>'
    fcu += '</div></div>'

    # Overhead panel (lots of switches)
    overhead = '<div style="background:linear-gradient(180deg,#2a2a2a,#1a1a1a);border:2px solid #444;border-radius:6px;padding:8px;">'
    overhead += '<div class="lbl" style="color:#bba;margin-bottom:6px;">OVERHEAD · 32 SWITCHES</div>'
    overhead += '<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:4px;">'
    sw_labels = ['BAT1','BAT2','GEN1','GEN2','APU','EXT','GALY','XFR',
                 'F·PMP1','F·PMP2','XFEED','BLEED','PACK1','PACK2','ANTI·ICE','PROBE',
                 'NAV','LOGO','BCN','STRB','LDG·L','LDG·R','TAXI','RWY',
                 'CAB·SGN','SEAT','EMER','OXY','ENG·1·STR','ENG·2·STR','IGN','MASTER']
    sw_states = [True,True,True,True,False,False,False,False,
                 True,True,False,True,True,True,False,True,
                 True,True,True,False,False,False,True,False,
                 True,True,False,False,False,False,False,True]
    for lbl, on in zip(sw_labels, sw_states):
        color = '#22c55e' if on else '#444'
        overhead += f'''<div style="display:flex;flex-direction:column;align-items:center;gap:2px;background:#0a0e14;border:1px solid #1e3a5a;padding:3px 1px;">
  <div style="width:14px;height:22px;background:linear-gradient(180deg,#1a1a1a,#000);border:1px solid #333;border-radius:2px;position:relative;">
    <div style="position:absolute;top:{2 if on else 12}px;left:1px;right:1px;height:8px;background:linear-gradient(135deg,{color},#666);border-radius:1px;"></div>
  </div>
  <div style="font-size:6px;color:#bba;font-family:monospace;letter-spacing:0;text-align:center;">{lbl}</div>
</div>'''
    overhead += '</div></div>'

    # Thrust levers (motor L/R)
    thrust = '<div style="background:linear-gradient(180deg,#1a1f2a,#0a0e14);border:2px solid #1e3a5a;border-radius:6px;padding:10px;">'
    thrust += '<div class="lbl" style="color:#22d3ee;margin-bottom:6px;text-align:center;">THRUST · MOTOR L/R</div>'
    thrust += '<div style="display:flex;gap:14px;justify-content:center;">'
    for lbl, p in [('L',82),('R',78)]:
        thrust += f'''<div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
  <div style="width:30px;height:140px;background:linear-gradient(180deg,#0a0e14 0%,#000 100%);border:2px solid #1e3a5a;border-radius:4px;position:relative;">
    <div style="position:absolute;left:50%;width:1px;height:100%;background:repeating-linear-gradient(180deg,#1e3a5a 0,#1e3a5a 4px,transparent 4px,transparent 12px);transform:translateX(-50%);"></div>
    <div style="position:absolute;left:-5px;right:-5px;bottom:{p}%;height:18px;background:linear-gradient(135deg,#fbbf24,#a16207);border:1px solid #000;border-radius:2px;box-shadow:0 0 6px rgba(251,191,36,0.5);"></div>
    <div style="position:absolute;left:-30px;top:5%;font-size:7px;color:#22c55e;font-family:monospace;">CLB</div>
    <div style="position:absolute;left:-30px;top:25%;font-size:7px;color:#bba;font-family:monospace;">FLX</div>
    <div style="position:absolute;left:-30px;top:75%;font-size:7px;color:#bba;font-family:monospace;">IDL</div>
  </div>
  <div style="font-size:9px;color:#bba;font-family:monospace;font-weight:700;">{lbl}</div>
  <div style="font-size:12px;color:#fbbf24;font-family:monospace;font-weight:800;text-shadow:0 0 4px #fbbf24;">{p}%</div>
</div>'''
    thrust += '</div></div>'

    # Side stick + rudder
    sidestick = '<div style="background:linear-gradient(180deg,#1a1f2a,#0a0e14);border:2px solid #1e3a5a;border-radius:6px;padding:8px;text-align:center;">'
    sidestick += '<div class="lbl" style="color:#22d3ee;margin-bottom:6px;">SIDE-STICK · F/O</div>'
    sidestick += '''<div style="position:relative;width:80px;height:80px;margin:0 auto;background:radial-gradient(circle at 50% 50%,#0a0e14 0,#000 100%);border:2px solid #1e3a5a;border-radius:50%;">
  <div style="position:absolute;top:50%;left:0;right:0;border-top:1px dashed #1e3a5a;"></div>
  <div style="position:absolute;left:50%;top:0;bottom:0;border-left:1px dashed #1e3a5a;"></div>
  <div style="position:absolute;width:18px;height:18px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,#22d3ee 70%);box-shadow:0 0 10px #22d3ee;top:42%;left:48%;"></div>
</div>
<div style="font-family:monospace;font-size:9px;color:#22d3ee;margin-top:5px;">PITCH:+2° ROLL:−4°</div>'''
    sidestick += '</div>'

    body = nav + f'''
<div style="max-width:1500px;margin:0 auto;display:grid;grid-template-columns:1fr 2.5fr 1fr;gap:8px;">

  <!-- LEFT -->
  <div style="display:flex;flex-direction:column;gap:8px;">
    {thrust}
    {sidestick}
    {servo_dial(110, accent='#22d3ee')}
    {led_bank(label='WING NAV LIGHTS · 4 RGB', colors=('#ef4444','#22c55e','#fff','#fbbf24'))}
  </div>

  <!-- CENTER MAIN PANEL -->
  <div style="display:flex;flex-direction:column;gap:8px;">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
      {pfd}
      {nd}
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
      {eicas}
      {sys}
    </div>
    {fcu}
    {overhead}
  </div>

  <!-- RIGHT -->
  <div style="display:flex;flex-direction:column;gap:8px;">
    {compass_tape(72,'#22d3ee')}
    {accel_ball('#22d3ee')}
    {matrix5(accent='#fbbf24', pattern=[[0,1,1,1,0],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[0,1,1,1,0]])}
    {ir_panel()}
    {line_cam()}
    {mic_vu()}
    {battery_panel()}
    {buzzer_keys()}
    {hazard_stripe()}
  </div>

</div>
'''
    return base_html('✈️ v3 #2 Glass Cockpit (Airliner)', body, bg='#06090f')
def make_3():  return _stub(3, 'Fighter Jet HUD', '🛫', 'HUD · MFCDs · HOTAS')
def make_4():  return _stub(4, 'F1 Steering Wheel', '🏎', '24 buttons · ERS · sectors')
def make_5():  return _stub(5, 'Submarine Helm', '🚢', 'periscope · sonar · ballast')
def make_6():  return _stub(6, 'Starship Bridge', '🛸', 'LCARS · viewscreen · tactical')
def make_7():  return _stub(7, 'Mech HUD', '🤖', 'targeting · ammo · heat')
def make_8():  return _stub(8, 'DJ Booth', '🎧', 'twin decks · 4ch mixer · pads')
def make_9():  return _stub(9, 'Studio Mixer', '🎚', '16 strips · master · rack')
def make_10(): return _stub(10, 'Smartwatch / Tablet', '⌚', 'bento · cards · widgets')


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  GENERATE all 10 + gallery                                           ║
# ╚═════════════════════════════════════════════════════════════════════╝
makers = [make_1, make_2, make_3, make_4, make_5, make_6, make_7, make_8, make_9, make_10]
labels = [
    ('🛩', 'Plane Cockpit',           'dense 6-pack · radio · breakers'),
    ('✈️', 'Glass Cockpit (Airliner)', '4 MFDs · FCU · overhead'),
    ('🛫', 'Fighter Jet HUD',         'HUD · MFCDs · HOTAS'),
    ('🏎', 'F1 Steering Wheel',       '24 buttons · ERS · sectors'),
    ('🚢', 'Submarine Helm',          'periscope · sonar · ballast'),
    ('🛸', 'Starship Bridge',         'LCARS · viewscreen · tactical'),
    ('🤖', 'Mech HUD',                'targeting · ammo · heat'),
    ('🎧', 'DJ Booth',                'twin decks · 4ch mixer · pads'),
    ('🎚', 'Studio Mixer',            '16 strips · master · rack'),
    ('⌚', 'Smartwatch / Tablet',     'bento · cards · widgets'),
]

for i, maker in enumerate(makers, 1):
    out = os.path.join(OUT, f'cockpit-lab_v3_{i}.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(maker())
    emoji, name, _ = labels[i-1]
    print(f'  + cockpit-lab_v3_{i}.html  ({emoji} {name})')

# Gallery
gallery = '''<!doctype html>
<html lang="en" data-theme="carbon">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🛸 Cockpit Lab v3 — dense, real cockpits</title>
<link rel="stylesheet" href="../workshops/theme.css">
<style>
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:var(--font-body,system-ui);background:var(--bg,#0a1018);color:var(--text,#e0e6ee);padding:24px 18px 40px;}
  h1{font-family:var(--font-display,system-ui);color:var(--neon,#4ade80);font-size:1.8rem;margin-bottom:6px;text-align:center;}
  .sub{text-align:center;color:var(--steel,#93a8c4);margin-bottom:24px;font-size:0.95rem;max-width:780px;margin-left:auto;margin-right:auto;line-height:1.5;}
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
  .stub{opacity:0.55;}
  .stub .dna{color:#fbbf24;}
</style>
</head>
<body>

<h1>🛸 Cockpit Lab v3 — dense, real</h1>
<p class="sub">Packed cockpits with all Maqueen hardware visible: 2 motors, 4 RGB LEDs, servo, buzzer, line sensors, IR, 5×5 matrix, accel, compass, temp, mic, battery. Animations + warning lights + switches. Static design, no BLE.</p>

<div class="nav">
  <a href="index.html">🧪 All Labs</a>
  <a href="cockpit-lab.html">v1</a>
  <a href="cockpit-lab_v2.html">v2</a>
  <a href="../index.html">🤖 Robot App</a>
</div>

<div class="grid">
'''
DONE = {1, 2}  # which mockups have full v3 build
for i, (emoji, name, vibe) in enumerate(labels, 1):
    klass = 'card' if i in DONE else 'card stub'
    tag = '▸ DENSE BUILD' if i in DONE else '◇ stub · pending'
    gallery += f'''  <a class="{klass}" href="cockpit-lab_v3_{i}.html">
    <div class="emoji">{emoji}</div>
    <div class="num">cockpit-lab_v3_{i}.html</div>
    <h3>{name}</h3>
    <div class="vibe">{vibe}</div>
    <div class="dna">{tag}</div>
  </a>
'''

gallery += '''</div>
</body>
</html>
'''
with open(os.path.join(OUT, 'cockpit-lab_v3.html'), 'w', encoding='utf-8') as f:
    f.write(gallery)
print('\n  + cockpit-lab_v3.html  (gallery)')
print(f'\nDone — 10 mockups + gallery written to {os.path.relpath(OUT)}')
