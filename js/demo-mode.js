/* js/demo-mode.js — fake BLE shim for "try without robot" mode.
 *
 * Activates when ANY of:
 *   - URL hash contains demo=1   (?#demo=1, set by share-link.js)
 *   - localStorage 'maqueen.demo' === '1'
 *
 * Replaces:
 *   - window.connect()   → resolves immediately, fakes a connected state
 *   - window.disconnect()→ fakes disconnect
 *   - window.sendLine(s) → echoes back via window.RobiBle.onRxLine()
 *   - window.isConnected → kept in sync with the fake state
 *
 * Plus:
 *   - Floating "🎭 DEMO MODE" badge top-right (click to exit)
 *   - Synthetic responses: every TX → matching `ECHO:N <verb>` RX
 *   - DIST? / LINE? / IR? polls return plausible fake numbers
 *
 * NEVER touches real Web Bluetooth. Safe to load on every page.
 */
(function () {
  'use strict';

  function isDemo() {
    try {
      var hash = (location.hash || '').slice(1);
      var p = new URLSearchParams(hash);
      if (p.get('demo') === '1') return true;
      return localStorage.getItem('maqueen.demo') === '1';
    } catch (e) { return false; }
  }

  if (!isDemo()) return; // not in demo mode → do nothing

  // Persist the demo flag so it survives reloads
  try { localStorage.setItem('maqueen.demo', '1'); } catch (e) {}

  // ───── Visible badge ─────
  function injectBadge() {
    if (document.getElementById('mqDemoBadge')) return;
    var b = document.createElement('div');
    b.id = 'mqDemoBadge';
    b.title = 'Demo mode — no robot needed. Click to exit.';
    b.style.cssText = 'position:fixed;top:10px;right:10px;z-index:99998;'
      + 'background:linear-gradient(90deg,#fb923c,#f97316);color:#0a1018;font-weight:800;'
      + 'padding:6px 14px;border-radius:999px;font-size:13px;box-shadow:0 4px 14px rgba(0,0,0,0.4);'
      + 'cursor:pointer;border:2px solid #0a1018;font-family:ui-monospace,monospace;';
    b.textContent = '🎭 DEMO MODE';
    b.addEventListener('click', function () {
      if (!confirm('Exit demo mode? You will need to connect a real robot.')) return;
      try { localStorage.removeItem('maqueen.demo'); } catch (e) {}
      try {
        var p = new URLSearchParams((location.hash || '').slice(1));
        p.delete('demo');
        var s = p.toString();
        location.hash = s ? '#' + s : '';
      } catch (e) {}
      location.reload();
    });
    document.body.appendChild(b);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectBadge);
  } else {
    injectBadge();
  }

  // ───── State ─────
  var fakeConnected = false;
  var seq = 0;

  // Ensure the RX hook channel exists
  if (!window.RobiBle) window.RobiBle = {};

  function rx(line) {
    try {
      if (typeof window.RobiBle.onRxLine === 'function') window.RobiBle.onRxLine(line);
    } catch (e) {}
    try {
      if (typeof window.RobiBle.onLog === 'function') window.RobiBle.onLog('< ' + line, 'rx');
    } catch (e) {}
  }
  function setStatus(state) {
    fakeConnected = !!state;
    try { window.isConnected = fakeConnected; } catch (e) {}
    try {
      if (typeof window.RobiBle.onStatus === 'function') {
        window.RobiBle.onStatus(fakeConnected, fakeConnected ? 'BBC micro:bit [DEMO]' : null);
      }
    } catch (e) {}
    try {
      if (typeof window.RobiBle.onToast === 'function') {
        window.RobiBle.onToast(fakeConnected ? 'Connected (demo)' : 'Disconnected', 'info');
      }
    } catch (e) {}
    // Mirror the DOM signal that bit-playground uses
    var sig = document.getElementById('connectionSignal');
    if (sig) sig.dataset.connected = fakeConnected ? '1' : '0';
  }

  function fakeConnect() {
    return new Promise(function (resolve) {
      setTimeout(function () {
        setStatus(true);
        rx('HELLO:DEMO');
        resolve(true);
      }, 200);
    });
  }
  function fakeDisconnect() {
    return new Promise(function (resolve) {
      setStatus(false);
      resolve();
    });
  }

  // Synthetic sensor responses for query verbs
  function answerQuery(verb) {
    if (/^DIST\?/.test(verb))  return 'DIST:' + (10 + Math.floor(Math.random() * 80));
    if (/^LINE\?/.test(verb))  return 'LINE:' + (Math.random() > 0.5 ? 1 : 0) + ',' + (Math.random() > 0.5 ? 1 : 0);
    if (/^IR\?/.test(verb))    return 'IR:' + (Math.random() > 0.7 ? 'KEY:OK' : 'NONE');
    if (/^BAT\?/.test(verb))   return 'BAT:' + (60 + Math.floor(Math.random() * 40)) + '%';
    if (/^HELLO/.test(verb))   return 'HELLO:DEMO';
    return null;
  }

  function fakeSendLine(line) {
    if (!fakeConnected) return Promise.reject(new Error('not connected'));
    var s = String(line || '').trim();
    seq++;
    // Echo back in the same format the firmware uses
    setTimeout(function () { rx('ECHO:' + seq + ' ' + s); }, 30);
    var ans = answerQuery(s);
    if (ans) setTimeout(function () { rx(ans); }, 60);
    return Promise.resolve();
  }

  // ───── Install (replace the bare-name globals the labs use) ─────
  try { window.connect    = fakeConnect; }    catch (e) {}
  try { window.disconnect = fakeDisconnect; } catch (e) {}
  try { window.sendLine   = fakeSendLine; }   catch (e) {}
  try { window.isConnected = false; }         catch (e) {}

  // Some labs reach in via window.maqueen.send / window.maqueen.connect
  if (window.maqueen && typeof window.maqueen === 'object') {
    try { window.maqueen.send = fakeSendLine; } catch (e) {}
    try { window.maqueen.connect = fakeConnect; } catch (e) {}
    try { window.maqueen.disconnect = fakeDisconnect; } catch (e) {}
  }

  // Mark the page so CSS / debug tools can react
  document.documentElement.setAttribute('data-mq-demo', '1');

  console.info('[demo-mode] active — fake BLE shim installed; no real robot needed.');
})();
