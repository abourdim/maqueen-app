/**
 * Maqueen Lab — Etsy Package Builder (slim)
 *
 * Slim version: zero Playwright/screenshots. Just gathers the essentials
 * (app + docs + 2 printables + license + buyer README) into a versioned ZIP.
 *
 * Output: etsy-package/MaqueenLab-v0.X.Y.zip
 *
 * Usage:
 *   node etsy-package/build-package.js
 *
 * Requires: nothing. Uses node + the host's `zip` (POSIX) or PowerShell
 *   `Compress-Archive` (Windows). If neither is available, the staging
 *   folder is kept for manual zipping.
 */

import { execSync } from 'child_process';
import { mkdirSync, existsSync, copyFileSync, readdirSync, rmSync, statSync, writeFileSync, readFileSync } from 'fs';
import { resolve, join, dirname, relative } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname  = dirname(__filename);

// Pull version from product.json (single source of truth)
const PRODUCT_PATH = resolve(__dirname, '..', 'product.json');
const product = JSON.parse(readFileSync(PRODUCT_PATH, 'utf8'));
const VERSION  = 'v' + (product.version || '0.0.0').replace(/^v/, '');
const PRODUCT_SLUG = 'MaqueenLab';

const REPO_ROOT = resolve(__dirname, '..');
const PKG_DIR   = __dirname;
const STAGE     = resolve(__dirname, `${PRODUCT_SLUG}-${VERSION}`);
const OUTPUT    = `${STAGE}.zip`;

console.log(`📦 Building ${PRODUCT_SLUG}-${VERSION}`);

// ───────── 1. Wipe + recreate staging ─────────
if (existsSync(STAGE)) rmSync(STAGE, { recursive: true, force: true });
if (existsSync(OUTPUT)) rmSync(OUTPUT);
mkdirSync(STAGE, { recursive: true });

// ───────── 2. Copy the app (everything serveable) ─────────
const APP_INCLUDE = [
  'index.html', 'manifest.json', 'sw.js', 'styles.css', 'delight.css',
  'product.json', 'build-info.json', 'start.html', 'README.md', 'LICENSE',
  'assets', 'js', 'docs', 'firmware', 'labs', 'workshops',
];
const APP_SKIP_DIRS = new Set(['node_modules', '.git', '.claude', 'etsy-package', 'tools']);

function copyTree(src, dst) {
  if (!existsSync(src)) return;
  const st = statSync(src);
  if (st.isDirectory()) {
    const rel = relative(REPO_ROOT, src);
    if (APP_SKIP_DIRS.has(rel)) return;
    mkdirSync(dst, { recursive: true });
    for (const child of readdirSync(src)) copyTree(join(src, child), join(dst, child));
  } else {
    copyFileSync(src, dst);
  }
}

console.log('  → copying app + docs + labs + workshops + firmware');
for (const item of APP_INCLUDE) {
  copyTree(join(REPO_ROOT, item), join(STAGE, item));
}

// ───────── 3. Copy the buyer-facing etsy bits (no seller-only) ─────────
console.log('  → copying buyer-facing printables + license');
const ETSY_BUYER = [
  'LICENSE.txt',
  'README.md',
  'README-quickstart.html',
  'USERGUIDE.md',
  'classroom-poster.html',
  'quickstart-card.html',
];
for (const f of ETSY_BUYER) {
  const src = join(PKG_DIR, f);
  if (existsSync(src)) copyFileSync(src, join(STAGE, f));
  else console.warn(`  ⚠ missing ${f}`);
}

// ───────── 4. Drop a top-level BUILD-INFO stamp ─────────
const stamp = `Maqueen Lab — ${VERSION}\nBuilt: ${new Date().toISOString()}\nLive demo: https://abourdim.github.io/maqueen-lab/\nLicense: MIT\n`;
writeFileSync(join(STAGE, 'BUILD-INFO.txt'), stamp);

// ───────── 5. Zip ─────────
console.log(`  → zipping → ${relative(process.cwd(), OUTPUT)}`);
const isWin = process.platform === 'win32';
try {
  if (isWin) {
    execSync(`powershell -NoProfile -Command "Compress-Archive -Force -Path '${STAGE}\\*' -DestinationPath '${OUTPUT}'"`, { stdio: 'inherit' });
  } else {
    execSync(`cd "${dirname(STAGE)}" && zip -qr "${OUTPUT}" "${PRODUCT_SLUG}-${VERSION}"`, { stdio: 'inherit' });
  }
  const sizeMb = (statSync(OUTPUT).size / 1024 / 1024).toFixed(2);
  console.log(`✅ Done — ${OUTPUT}  (${sizeMb} MB)`);
} catch (e) {
  console.warn(`⚠ Zip step failed (${e.message}). Staging folder kept at:\n   ${STAGE}\nYou can zip it manually.`);
}
