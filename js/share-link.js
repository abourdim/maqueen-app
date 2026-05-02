/* js/share-link.js — encode current view state into URL hash for one-click sharing.
 *
 * State packed into the hash (URLSearchParams style):
 *   theme=carbon         (CSS theme on this surface)
 *   lang=fr              (UI language)
 *   demo=1               (demo-mode flag — used by demo-mode.js)
 *   ext=...              (free-form key the page can read with MqShare.get('ext'))
 *
 * Auto-applies on page load:
 *   - data-theme + localStorage('robi.theme')
 *   - lang attribute + localStorage('robi.lang') + dir for AR
 *
 * Public API (window.MqShare):
 *   get(key)             → string | null   (read a hash param)
 *   set(key, value)      → updates hash + localStorage where applicable
 *   url()                → full sharable URL with current state encoded
 *   copy()               → copy url() to clipboard, returns Promise<boolean>
 *   addButton(parent, opts) → inject a "🔗 Share this view" button
 *
 * Designed to coexist with the existing T={en,fr,ar} tables in workshops/labs:
 * setting `lang` here triggers a `mq:lang` CustomEvent on window so pages can
 * re-render without a full reload.
 */
(function () {
  'use strict';

  function readHash() {
    var h = location.hash || '';
    if (h.startsWith('#')) h = h.slice(1);
    return new URLSearchParams(h);
  }
  function writeHash(params) {
    var s = params.toString();
    if (s) location.hash = '#' + s;
    else history.replaceState(null, '', location.pathname + location.search);
  }

  var api = {
    get: function (key) {
      var v = readHash().get(key);
      return (v == null) ? null : v;
    },
    set: function (key, value) {
      var p = readHash();
      if (value == null || value === '') p.delete(key);
      else p.set(key, String(value));
      writeHash(p);
      // Mirror well-known keys to localStorage and DOM so reload is consistent
      try {
        if (key === 'theme') {
          localStorage.setItem('robi.theme', value);
          document.documentElement.setAttribute('data-theme', value);
        } else if (key === 'lang') {
          localStorage.setItem('robi.lang', value);
          document.documentElement.lang = value;
          document.documentElement.dir = (value === 'ar') ? 'rtl' : 'ltr';
          window.dispatchEvent(new CustomEvent('mq:lang', { detail: { lang: value } }));
        } else if (key === 'demo') {
          if (value === '1') localStorage.setItem('maqueen.demo', '1');
          else localStorage.removeItem('maqueen.demo');
        }
      } catch (e) {}
    },
    url: function () {
      // Recompute the hash from currently applied state so the link is accurate
      var p = readHash();
      try {
        var theme = localStorage.getItem('robi.theme');
        if (theme) p.set('theme', theme);
        var lang = localStorage.getItem('robi.lang');
        if (lang) p.set('lang', lang);
        var demo = localStorage.getItem('maqueen.demo');
        if (demo === '1') p.set('demo', '1');
      } catch (e) {}
      var s = p.toString();
      return location.origin + location.pathname + location.search + (s ? '#' + s : '');
    },
    copy: function () {
      var u = api.url();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(u).then(function () { return true; }).catch(function () { return false; });
      }
      // Fallback: hidden textarea + execCommand
      try {
        var ta = document.createElement('textarea');
        ta.value = u; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        return Promise.resolve(ok);
      } catch (e) { return Promise.resolve(false); }
    },
    addButton: function (parent, opts) {
      opts = opts || {};
      if (!parent) return null;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = opts.label || '🔗 Share view';
      btn.title = opts.title || 'Copy a sharable link to this view';
      btn.style.cssText = 'background:var(--bg-soft,#1a2230);color:var(--text,#fff);border:1px solid var(--border,#445);'
                       + 'border-radius:6px;padding:5px 10px;font-size:13px;cursor:pointer;font-weight:600;';
      btn.addEventListener('click', function () {
        api.copy().then(function (ok) {
          var orig = btn.textContent;
          btn.textContent = ok ? '✅ Copied!' : '⚠ Copy failed';
          setTimeout(function () { btn.textContent = orig; }, 1500);
        });
      });
      parent.appendChild(btn);
      return btn;
    }
  };

  // ───── Auto-apply hash on load (theme + lang + demo flag) ─────
  function autoApply() {
    var p = readHash();
    var theme = p.get('theme');
    if (theme && /^(carbon|forest|steel|paper|pearl|cosmos|workshop|sky|mint|night|arctic|blaze)$/.test(theme)) {
      document.documentElement.setAttribute('data-theme', theme);
      try { localStorage.setItem('robi.theme', theme); } catch (e) {}
    }
    var lang = p.get('lang');
    if (lang && /^(en|fr|ar)$/.test(lang)) {
      document.documentElement.lang = lang;
      document.documentElement.dir = (lang === 'ar') ? 'rtl' : 'ltr';
      try { localStorage.setItem('robi.lang', lang); } catch (e) {}
      // Notify pages that build their own T tables
      window.dispatchEvent(new CustomEvent('mq:lang', { detail: { lang: lang } }));
    }
    var demo = p.get('demo');
    if (demo === '1') {
      try { localStorage.setItem('maqueen.demo', '1'); } catch (e) {}
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoApply);
  } else {
    autoApply();
  }

  window.MqShare = api;
})();
