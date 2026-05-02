/* js/telemetry.js — local-only privacy-preserving usage telemetry.
 *
 * Stores aggregated counts in localStorage under `maqueen.telemetry.*`.
 * NEVER sends data anywhere — no fetch, no beacon, no analytics SDK.
 * Single purpose: inform self-roadmap "which Lab did I open most?".
 *
 * Public API (window.MqTelemetry):
 *   bump(key)              → increment a counter
 *   set(key, value)        → set a value (last-write-wins, e.g. 'lang=fr')
 *   get(key)               → read a counter or value (number | string | null)
 *   all()                  → { key: value, ... } full snapshot
 *   reset()                → clear all maqueen.telemetry.* keys
 *
 * Auto-fired events (zero wiring needed in pages that load this script):
 *   maqueen.telemetry.visit.<surface>      → +1 per page load
 *   maqueen.telemetry.theme.<theme>        → +1 each time theme is read from storage
 *   maqueen.telemetry.lang.<lang>          → +1 each time lang is read from storage
 *   maqueen.telemetry.firstVisit           → epoch ms, set once
 *   maqueen.telemetry.lastVisit            → epoch ms, updated each load
 *
 * Surface inferred from pathname:
 *   / or /index.html        → 'app'
 *   /labs/<x>-lab.html      → 'lab.<x>'
 *   /labs/index.html        → 'lab.hub'
 *   /docs/lessons/<x>.html  → 'lesson.<x>'
 *   /docs/...               → 'doc.<basename>'
 *   /workshops/...          → 'workshop.<basename>'
 *
 * Telemetry is OFF if user sets localStorage 'maqueen.telemetry.optout' = '1'.
 * Toggle in the viewer at docs/telemetry.html.
 */
(function () {
  'use strict';
  var PFX = 'maqueen.telemetry.';

  function read(k) {
    try { return localStorage.getItem(PFX + k); } catch (e) { return null; }
  }
  function write(k, v) {
    try { localStorage.setItem(PFX + k, String(v)); } catch (e) {}
  }
  function isOptedOut() {
    return read('optout') === '1';
  }

  var api = {
    bump: function (key) {
      if (isOptedOut()) return;
      var n = parseInt(read(key), 10);
      if (!isFinite(n)) n = 0;
      write(key, n + 1);
    },
    set: function (key, value) {
      if (isOptedOut()) return;
      write(key, value);
    },
    get: function (key) {
      var v = read(key);
      if (v == null) return null;
      var n = parseInt(v, 10);
      // Return as number if it parses cleanly (plain integers); else as string.
      return (String(n) === v) ? n : v;
    },
    all: function () {
      var out = {};
      try {
        for (var i = 0; i < localStorage.length; i++) {
          var k = localStorage.key(i);
          if (k && k.indexOf(PFX) === 0) {
            out[k.slice(PFX.length)] = localStorage.getItem(k);
          }
        }
      } catch (e) {}
      return out;
    },
    reset: function () {
      try {
        var keys = [];
        for (var i = 0; i < localStorage.length; i++) {
          var k = localStorage.key(i);
          if (k && k.indexOf(PFX) === 0) keys.push(k);
        }
        keys.forEach(function (k) { localStorage.removeItem(k); });
      } catch (e) {}
    },
    optout: function (yes) {
      try {
        if (yes) localStorage.setItem(PFX + 'optout', '1');
        else     localStorage.removeItem(PFX + 'optout');
      } catch (e) {}
    },
    optedOut: isOptedOut
  };

  // ───── Auto-fire on load ─────
  if (!isOptedOut()) {
    var path = location.pathname.toLowerCase();
    var surface = 'unknown';
    var m;
    if (path === '/' || /\/index\.html?$/.test(path) && !/\/labs\//.test(path) && !/\/docs\//.test(path) && !/\/workshops\//.test(path)) {
      surface = 'app';
    } else if ((m = path.match(/\/labs\/([a-z0-9_-]+)-lab\.html?$/))) {
      surface = 'lab.' + m[1];
    } else if (/\/labs\/index\.html?$/.test(path)) {
      surface = 'lab.hub';
    } else if (/\/labs\/wishlist\.html?$/.test(path)) {
      surface = 'lab.wishlist';
    } else if ((m = path.match(/\/docs\/lessons\/([a-z0-9_-]+)-lab\.html?$/))) {
      surface = 'lesson.' + m[1];
    } else if (/\/docs\/lessons\/index\.html?$/.test(path)) {
      surface = 'lesson.hub';
    } else if ((m = path.match(/\/docs\/([a-z0-9_.-]+)\.html?$/i))) {
      surface = 'doc.' + m[1].replace(/\./g, '_');
    } else if ((m = path.match(/\/workshops\/([a-z0-9_.-]+)\.html?$/i))) {
      surface = 'workshop.' + m[1].replace(/\./g, '_');
    }
    api.bump('visit.' + surface);
    api.bump('visit.total');
    var now = Date.now();
    if (!read('firstVisit')) write('firstVisit', now);
    write('lastVisit', now);

    // Mirror current theme + lang choice from common storage keys (best-effort).
    try {
      var theme = localStorage.getItem('robi.theme') || localStorage.getItem('mb_theme');
      if (theme) api.bump('theme.' + theme);
      var lang = localStorage.getItem('robi.lang') || localStorage.getItem('mb_lang');
      if (lang) api.bump('lang.' + lang);
    } catch (e) {}
  }

  window.MqTelemetry = api;
})();
