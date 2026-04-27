// ============================================================
// log-rail.js — Move the MESSAGE LOG into its own permanent
// right sidebar, structurally independent of the main app.
//
// At init we restructure the DOM:
//
//   <body>                        <body>
//     <div class="app">             <div class="app-shell">
//       ... CONNECT ...      →        <div class="app">
//       ... col-right ...                ... CONNECT (now spans col-right) ...
//         ... LOG CARD ...               ... (no log here anymore)
//       ... tabs ...                     ... tabs ...
//     </div>                          </div>
//                                     <aside id="logRailAside">
//                                       <div class="card log-card">
//                                         ... MESSAGE LOG ...
//                                       </div>
//                                     </aside>
//                                   </div>
//                                 </body>
//
// The shell is a CSS grid (1fr | --log-rail-w). Below 1100 px the
// grid collapses to a single column and the rail is hidden — log
// visibility on tiny screens is sacrificed for content space (the
// raw UART log is rarely useful on a phone anyway).
//
// State persisted in localStorage:
//   maqueen.logRailWidth  integer px, clamped 280..620
// ============================================================

(function () {
  'use strict';

  const WIDTH_KEY    = 'maqueen.logRailWidth';
  const MIN_W        = 280;
  const MAX_W        = 620;
  const DEFAULT_W    = 380;

  function getStoredWidth() {
    let w;
    try { w = +localStorage.getItem(WIDTH_KEY) || 0; } catch { w = 0; }
    if (!w) return DEFAULT_W;
    return Math.max(MIN_W, Math.min(MAX_W, w));
  }
  function applyWidth(w) {
    w = Math.max(MIN_W, Math.min(MAX_W, w));
    document.documentElement.style.setProperty('--log-rail-w', w + 'px');
    try { localStorage.setItem(WIDTH_KEY, String(w)); } catch {}
    return w;
  }

  // Move the .log-card out of its inline parent into a dedicated
  // <aside> rail at the layout level. Idempotent — safe to call twice.
  function relocateCard() {
    const card = document.querySelector('.log-card');
    const app  = document.querySelector('.app');
    if (!card || !app) return null;
    // Already moved? Done.
    let aside = document.getElementById('logRailAside');
    if (aside && aside.contains(card)) return aside;

    // Wrap .app in a shell if not already
    let shell = document.getElementById('appShell');
    if (!shell) {
      shell = document.createElement('div');
      shell.id = 'appShell';
      shell.className = 'app-shell';
      // Put the shell where .app was, then move .app inside.
      app.parentNode.insertBefore(shell, app);
      shell.appendChild(app);
    }

    // Create rail aside if not present
    if (!aside) {
      aside = document.createElement('aside');
      aside.id = 'logRailAside';
      aside.className = 'log-rail';
      shell.appendChild(aside);
    }

    // Move the log card into the rail. Detaching from col-right means
    // the activity-card (beginner-only) gets the column to itself,
    // which is the cleaner mental model anyway.
    aside.appendChild(card);
    return aside;
  }

  // ---- DRAG-TO-RESIZE -----------------------------------------
  // Insert a transparent vertical strip on the LEFT edge of the rail.
  // Pointer drag updates --log-rail-w → CSS grid recomputes the
  // column widths → main app shrinks/grows in real time.
  function initDrag(aside) {
    if (!aside || document.getElementById('logRailHandle')) return;
    const handle = document.createElement('div');
    handle.id = 'logRailHandle';
    handle.className = 'log-rail-handle';
    handle.setAttribute('aria-hidden', 'true');
    handle.title = 'Drag to resize. Double-click to reset width.';
    aside.appendChild(handle);

    let dragging = false;
    let startX   = 0;
    let startW   = 0;
    handle.addEventListener('pointerdown', (e) => {
      dragging = true;
      startX = e.clientX;
      startW = getStoredWidth();
      handle.classList.add('dragging');
      try { handle.setPointerCapture(e.pointerId); } catch {}
      e.preventDefault();
    });
    handle.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      // Handle is on the LEFT edge of the rail. Moving LEFT (negative
      // dx) → wider rail. New width = startW - dx.
      const dx = e.clientX - startX;
      applyWidth(startW - dx);
    });
    function endDrag(e) {
      if (!dragging) return;
      dragging = false;
      handle.classList.remove('dragging');
      try { handle.releasePointerCapture(e.pointerId); } catch {}
    }
    handle.addEventListener('pointerup',     endDrag);
    handle.addEventListener('pointercancel', endDrag);
    handle.addEventListener('dblclick', () => { applyWidth(DEFAULT_W); });
  }

  // The old per-card 'Pin' button is now meaningless (the rail is
  // permanent). Leave it in the DOM but hide it gracefully so any
  // existing references / event listeners don't break.
  function hidePinButton() {
    const btn = document.getElementById('logPinBtn');
    if (btn) btn.style.display = 'none';
  }

  function init() {
    const aside = relocateCard();
    if (!aside) return;
    applyWidth(getStoredWidth());
    initDrag(aside);
    hidePinButton();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
