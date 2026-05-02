# Checklist de personnalisation — Maqueen Lab

Ce fichier a été généré par `apply-template.mjs`. Le template a substitué
les identifiants (nom produit, URLs, prix, version) mais **pas** le contenu
fonctionnel. Parcours la liste ci-dessous avant de publier.

Lance `node <chemin-template>/verify-clean.mjs` depuis ce dossier à tout
moment pour scanner le vocabulaire template restant. Code de sortie 0 = propre.

---

## 🖨 Imprimables — réécrire le contenu
Chaque fichier commence par un bandeau `<!-- REWRITE PER PRODUCT -->`. Supprime
le bandeau **après** la réécriture. La structure visuelle est à garder ;
seule la copy, les étapes, raccourcis et exemples doivent changer.

- [ ] `etsy-package/classroom-poster.html` — titre + 5 grandes étapes + slogan footer
- [ ] `etsy-package/quickstart-card.html` — séquence d'installation 5 minutes
- [ ] `etsy-package/shortcuts-cheatsheet.html` — raccourcis clavier, actions spécifiques produit
- [ ] `etsy-package/lesson-plan-template.html` — corps de leçon 45 min exemple
- [ ] `etsy-package/sticker-sheet.html` — 30 badges de réussite
- [ ] `etsy-package/README-quickstart.html` — page d'accueil acheteur + "3 premières choses à faire"

## 🖼 Mockups listing — réécrire mockups 2-7

- [ ] `etsy-package/etsy-listing-mockups.html`
   - M1 hero est templaté par identifiants ; seul le screenshot + badge compat doit être ajusté
   - M2 (grille 16 cellules features) — remplacer toutes les cellules par features produit
   - M3 (pitch enseignant) — réécrire pour ton public
   - M4 (pitch enfant) — réécrire copy + emojis
   - M5 (Contenu du ZIP) — coller au contenu réel du ZIP
   - M6 (thèmes / personnalités / variantes)
   - M7 (trilingue ou vie privée ou autre angle qui colle)

## 📌 Pins Pinterest
- [ ] `etsy-package/seller-only/pinterest-pins.html` — 4 pins portrait : hero, pitch public, contenu ZIP, features/langues

## 🛒 Docs vendeur (collés dans Etsy — important)
- [ ] `etsy-package/seller-only/ETSY_LISTING.md` — titre, 13 tags, description, table comparative, FAQ
- [ ] `etsy-package/seller-only/ETSY_LISTING.html` — jumeau HTML du .md (doit matcher)
- [ ] `etsy-package/seller-only/ETSY-1MIN-PLAYBOOK.md` — script vidéo 60s + shot list
- [ ] `etsy-package/seller-only/ETSY_PUBLISH_GUIDE.html` — checklist photos (11 noms de fichier photo souvent à renommer)

## 🎥 Playbook vidéo (FR/AR)
- [ ] `etsy-package/seller-only/etsy-playbook.html` — playbook vidéo EN
- [ ] `etsy-package/seller-only/etsy-playbook-fr.html` — Français
- [ ] `etsy-package/seller-only/etsy-playbook-ar.html` — Arabe (RTL)

## 🎬 Outils production vidéo (tournage 60s)
Ces trois fichiers compagnons transforment le playbook en vrai tournage.
Réécris le contenu de chaque scène par produit ; garde la structure 8 scènes
et les bornes de temps.

- [ ] `etsy-package/seller-only/video-teleprompter.html` — téléprompter HTML
   interactif. Ouvre sur un second moniteur, presse `F` pour fullscreen, `Espace`
   pour countdown 3-2-1 puis avance auto à travers 8 scènes. Affiche grand la
   ligne SAY, indices DO/CLICK en dessous, horloge live, barre de progression
   (rouge passé 55s). Réécris le tableau `SCENES` dans la balise `<script>` inline.
- [ ] `etsy-package/seller-only/video-shoot-card.html` — fiche A4 imprimable.
   Checklist pré-vol + specs Etsy + arc 8 lignes + cheat card sur une page.
   Rendue en PNG par `build-package.js` (vendeur uniquement, pas dans le ZIP).
   Réécris items pré-vol et table arc ; table specs reste.
- [ ] `etsy-package/tools/captions/video-captions-en.srt` — sous-titres burn-in
   pour CapCut/DaVinci. Réécris les 8 blocs sous-titre pour matcher verbatim
   les lignes SAY du téléprompter. Timings (0-3 / 3-10 / 10-20 / 20-30
   / 30-40 / 40-50 / 50-55 / 55-60) doivent matcher les bornes de scène.
- [ ] `etsy-package/tools/captions/video-captions-fr.srt` — jumeau français
- [ ] `etsy-package/tools/captions/video-captions-ar.srt` — jumeau arabe (RTL ;
   les lignes sont préfixées par marqueurs U+200F RLM — préserve-les)
- [ ] `etsy-package/tools/generate-video.mjs` — générateur basé ffmpeg
   qui construit un MP4 1080×1920 9:16 depuis 5 screenshots + captions EN.
   Screen-only v1 — remplace par footage matériel réel après tournage. Requiert
   ffmpeg dans le PATH. Réécris texte titre/CTA dans le tableau `SCENES` si les
   substitutions `Maqueen Lab` / `Every component, live in your browser` ne collent pas.
   Lance : `node etsy-package/tools/generate-video.mjs`

## 📸 Pipeline capture marketing (13 modes + helpers)

Toutes les sorties atterrissent dans `etsy-package/seller-only/screenshots/` et
`etsy-package/output/`. Chaque outil est lançable indépendamment ; le pipeline
complet est :

   capture → (optionnel) annotate → theme-morph → generate-video → visual-regress

- [ ] `capture-screenshots.mjs` — capteur basé Playwright couvrant tous les
   tabs × 2 (standard + état synthétique live), paires before/after, variantes
   thèmes, variantes modèles, preuve offline, annotations callout SVG, et
   sorties multi-aspect (9:16/1:1/2:3/16:9).
   **CONFIG-DRIVEN — n'édite pas le script.** Édite `capture-config.json`
   (même dossier). Référence remplie dans `capture-config.example.json`.
   Le champ `_rewrite` au sommet de la config liste les 10 sections à ajuster
   pour ton DOM produit.
   Modes : `tabs synthetic pairs themes models offline annotated aspects all`.
- [ ] `qr-inject.mjs` — injecte des QR codes UTM-taggés dans chaque imprimable.
   `--preview` par défaut écrit dans `output/printables-with-qr/` ; ajoute
   `--inplace` pour modifier les HTMLs source directement (réversible via git).
- [ ] `theme-morph.mjs` — rend une boucle crossfade 1:1 carrée à travers tes
   captures de thème. MP4 + GIF. Requiert `screenshot-theme-*.png` du mode
   capture themes.
- [ ] `visual-regress.mjs` — check identité md5 + diffs ffmpeg côte à côte.
   Utilise `--baseline` pour snapshotter l'état actuel ; runs ultérieurs sortent
   non-zéro si un screenshot a dérivé. Totalement générique, pas de réécriture.
- [ ] `hero-compose.mjs` + `hero-specs.json` — compositeur image hero A/B
   (thumbnails Etsy 1500×1500). Réécris `hero-specs.json` avec 2-5 variantes
   par public ; l'expérience d'ordre image d'Etsy choisit le gagnant.
- [ ] `generate-gifs.mjs` — GIFs démo 5 secondes pour slots image Etsy +
   Pinterest. **Réécris** l'objet `RECIPES` par produit — la fonction `act(page)`
   de chaque recette anime les features de TON app.
- [ ] `generate-datasets.mjs` — 100 CSVs capteurs synthétiques + README enseignant.
   Convertit produit hardware-requis → hardware-optionnel. **Réécris** l'objet
   `SCENARIOS` pour matcher les types de capteurs de ton produit.
- [ ] `watermark-zip.mjs` — ZIP par-acheteur avec nom acheteur + order ID gravés
   dans README-quickstart.html + LICENSE. Usage :
   `node tools/watermark-zip.mjs --buyer "Alice Smith" --order "12345"`.

**Prérequis pour capture :** `npm i --save-dev @playwright/test qrcode && npx playwright install chromium`.

## 📜 Licence acheteur
- [ ] `etsy-package/LICENSE.txt` — clauses 9 + 10 mentionnent "printable materials" ;
  vérifie que la liste matche tes vrais imprimables. Clause 3 disclaimer marque —
  update si ton produit utilise des marques différentes de BBC micro:bit.

## 📸 Screenshots
- [ ] Capture un vrai screenshot de l'UI principale de ton produit → `assets/app-screenshot.png`
  (référencé par le mockup hero + pin 1)

## ⚙️ Dernières étapes
- [ ] `npm install --save-dev @playwright/test qrcode && npx playwright install chromium`
- [ ] `node etsy-package/build-package.js` — rend tous les mockups + construit le ZIP
- [ ] `node <template-path>/verify-clean.mjs` — doit sortir propre (code 0)
- [ ] (Optionnel) `gh api -X POST "repos/abourdim/maqueen-lab/pages" -f 'source[branch]=main' -f 'source[path]=/'` — active GitHub Pages pour que l'URL démo live du listing marche
- [ ] `git add -A && git commit -m "..." && git push`
- [ ] Suis `etsy-package/seller-only/TODO.md` pour les trois items manuels pré-lancement (vraie photo produit, vidéo 60s, code promo LAUNCH10)

---

## 🔧 Régler le script verify par produit

Si `verify-clean.mjs` flag un terme légitime pour ton produit
(ex. "gamepad" pour une app remote-controller, "led matrix" pour une app
LED painter, "sensors" pour une app sensor-mapping), ajoute-le à
`product.json` :

```json
"ALLOWED_TERMS": ["gamepad", "led matrix"]
```

Re-lance le vérifieur. Les règles flaggées dont le label matche un terme
autorisé sont skippées.
