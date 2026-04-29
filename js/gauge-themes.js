// ============================================================
// gauge-themes.js — Dashboard gauge visual themes.
//
// Adds a row of tiny style-picker icons to the .mq-dash-header.
// Selecting a theme sets data-dash-theme on .mq-dash-panel so
// CSS can apply a full visual personality — face colours, glow,
// filters, borders — without touching any JS gauge logic.
//
// Themes:
//   dark   — Default dark cockpit (current look)
//   race   — F1 carbon-fibre, red danger, white ticks
//   retro  — Warm amber VU-meter, mahogany panel
//   cyber  — Neon pink/cyan matrix, glitch text-shadow
//   fun    — Cartoon bright, kid-friendly, rainbow
//   space  — Green phosphor CRT, scanlines
// ============================================================
(function () {
  'use strict';

  const KEY = 'maqueen.gaugeTheme';

  const THEMES = [
    { id: 'dark',  icon: '🌑', label: 'Dark'   },
    { id: 'race',  icon: '🏎️', label: 'Race'   },
    { id: 'retro', icon: '📻', label: 'Retro'  },
    { id: 'cyber', icon: '🌃', label: 'Cyber'  },
    { id: 'fun',   icon: '🎈', label: 'Fun'    },
    { id: 'space', icon: '🚀', label: 'Space'  },
  ];

  function applyTheme(id) {
    const panel = document.querySelector('.mq-dash-panel');
    if (!panel) return;
    panel.dataset.dashTheme = id;
    try { localStorage.setItem(KEY, id); } catch {}
    // Highlight active picker button
    document.querySelectorAll('.mq-gauge-theme-btn').forEach(b => {
      b.classList.toggle('mq-gauge-theme-active', b.dataset.theme === id);
    });
  }

  function buildPicker() {
    const header = document.querySelector('.mq-dash-header');
    if (!header || document.getElementById('mqGaugeThemePicker')) return false;

    const picker = document.createElement('div');
    picker.id = 'mqGaugeThemePicker';
    picker.style.cssText = 'display:flex; align-items:center; gap:3px; margin-left:10px;';

    THEMES.forEach(t => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'mq-gauge-theme-btn';
      btn.dataset.theme = t.id;
      btn.title = t.label;
      btn.textContent = t.icon;
      btn.addEventListener('click', () => applyTheme(t.id));
      picker.appendChild(btn);
    });

    // Insert after the title span (first child of header)
    const titleSpan = header.querySelector('span');
    if (titleSpan && titleSpan.nextSibling) {
      header.insertBefore(picker, titleSpan.nextSibling);
    } else {
      header.appendChild(picker);
    }
    return true;
  }

  function init() {
    let tries = 0;
    const t = setInterval(() => {
      if (buildPicker() || ++tries > 30) {
        clearInterval(t);
        const saved = (() => { try { return localStorage.getItem(KEY); } catch {} })();
        applyTheme(saved && THEMES.some(x => x.id === saved) ? saved : 'dark');
      }
    }, 200);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
