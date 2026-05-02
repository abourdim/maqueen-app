"""Inject one or more <script src="…"> tags into every HTML in the repo.

Usage:
    python tools/inject-script.py js/share-link.js
    python tools/inject-script.py js/demo-mode.js js/share-link.js
"""
import os, sys

if len(sys.argv) < 2:
    print('usage: inject-script.py <relpath-from-repo-root> [more...]'); sys.exit(1)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SKIP_DIRS = {'.git', 'node_modules', '.claude', 'etsy-package'}
TARGETS = sys.argv[1:]

def relpath(html_relpath, target):
    depth = html_relpath.replace('\\', '/').count('/')
    return ('../' * depth) + target if depth else target

def already_has(html, target):
    return target in html

added = skipped = 0
for root, dirs, names in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for n in names:
        if not n.endswith('.html'): continue
        full = os.path.join(root, n)
        rel = os.path.relpath(full, ROOT).replace('\\', '/')
        try:
            with open(full, 'r', encoding='utf-8') as fh: s = fh.read()
        except Exception as e:
            print(f'  ! skip {rel}: {e}'); skipped += 1; continue
        if '</body>' not in s:
            skipped += 1; continue
        new_tags = []
        for t in TARGETS:
            if already_has(s, t): continue
            rp = relpath(rel, t)
            new_tags.append(f'<script src="{rp}" defer></script>')
        if not new_tags:
            skipped += 1; continue
        s2 = s.replace('</body>', '\n'.join(new_tags) + '\n</body>')
        with open(full, 'w', encoding='utf-8') as fh: fh.write(s2)
        print(f'  + {rel}: {len(new_tags)} tag(s)')
        added += 1
print(f'\n{added} files updated, {skipped} skipped.')
