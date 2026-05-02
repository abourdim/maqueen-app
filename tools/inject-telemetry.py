"""Inject js/telemetry.js into every HTML in the repo (idempotent)."""
import os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SKIP_DIRS = {'.git', 'node_modules', '.claude', 'etsy-package'}

def relpath(html_relpath):
    depth = html_relpath.replace('\\', '/').count('/')
    return ('../' * depth) + 'js/telemetry.js' if depth else 'js/telemetry.js'

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
        if 'telemetry.js' in s or '</body>' not in s:
            skipped += 1; continue
        rp = relpath(rel)
        tag = f'<script src="{rp}" defer></script>'
        new = s.replace('</body>', tag + '\n</body>')
        with open(full, 'w', encoding='utf-8') as fh: fh.write(new)
        print(f'  + {rel}  ({rp})')
        added += 1
print(f'\nAdded telemetry to {added} files, skipped {skipped}.')
