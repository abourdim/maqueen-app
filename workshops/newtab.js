// workshops-newtab.js
// Force every cross-page link to open in a new tab.
// Same-page anchor links (#op01, #faq, ...) and javascript: links are left alone.
(function () {
  function applyNewTab(root) {
    root.querySelectorAll('a[href]').forEach(function (a) {
      var h = a.getAttribute('href');
      if (!h) return;
      if (h.charAt(0) === '#') return;            // in-page anchor
      if (h.indexOf('javascript:') === 0) return; // js handler
      if (h.indexOf('mailto:') === 0) return;     // mail
      if (h.indexOf('tel:') === 0) return;        // phone
      if (!a.getAttribute('target')) a.setAttribute('target', '_blank');
      var rel = (a.getAttribute('rel') || '').split(/\s+/);
      if (rel.indexOf('noopener') === -1) rel.push('noopener');
      a.setAttribute('rel', rel.filter(Boolean).join(' '));
    });
  }
  function go() { applyNewTab(document); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', go);
  } else {
    go();
  }
  // Re-apply when content is added dynamically (e.g. cert.show, language switch)
  var mo = new MutationObserver(function () { applyNewTab(document); });
  mo.observe(document.body || document.documentElement, { childList: true, subtree: true });
})();
