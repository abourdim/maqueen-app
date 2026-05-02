"""Check that every asset referenced from a given HTML actually exists on disk."""
import os, re, sys

target = sys.argv[1] if len(sys.argv) > 1 else 'labs/distance-lab.html'
with open(target, 'r', encoding='utf-8') as f:
    s = f.read()

# Strip HTML comments so commented-out examples don't false-positive.
s = re.sub(r'<!--[\s\S]*?-->', '', s)

base = os.path.dirname(target)
pat = re.compile(r'''(?:src|href)\s*=\s*["']([^"'#?]+\.(?:js|css|png|svg|jpg|jpeg|webp))(?:[#?][^"']*)?["']''', re.I)
refs = []
for m in pat.finditer(s):
    refs.append(m.group(1))

missing = []
for r in sorted(set(refs)):
    if r.startswith(('http:', 'https:', '//', 'data:')):
        continue
    full = os.path.normpath(os.path.join(base, r))
    if not os.path.exists(full):
        missing.append((r, full))

print(f'Asset refs scanned in {target}: {len(set(refs))}')
print(f'Missing: {len(missing)}')
for r, full in missing:
    print(f'  MISSING: {r}  (expected at {full})')
sys.exit(1 if missing else 0)
