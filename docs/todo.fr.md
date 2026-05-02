# Maqueen Lab — Feuille de route

> **La Phase 1 (10 + 10 = 20 items) est complète depuis v0.1.60.** La Phase 2 ci-dessous
> déplace l'attention des *fonctionnalités* → *portée, robustesse, profondeur*. Choisis le
> bloc qui convient à la prochaine session — chaque item est autonome.

---

## ✅ Phase 1 — Livré (v0.1.0 → v0.1.60)

Les "20 trucs à livrer ensuite : 10 améliorations app + 10 jeux éducatifs"
d'origine — **tous cochés**. Ouvre le [Changelog](CHANGELOG.html) pour le détail
release par release. Ouvre la [wishlist labs](../labs/wishlist.html) pour voter
sur de nouvelles idées ; le prochain lot est curé là-bas.

### Améliorations app (10/10) — fait

- [x] 1. Commandes vocales · [x] 2. Pilotage par inclinaison · [x] 3. Résumé IA de session ·
  [x] 4. Export time-lapse · [x] 5. Pilote auto par tracé ·
  [x] 6. Overlay AR webcam · [x] 7. Personnalités robot ·
  [x] 8. Indicateur batterie · [x] 9. Export télémétrie · [x] 10. Appairage 2 robots

### Jeux éducatifs (10/10) — fait

- [x] 1. SLAM la pièce · [x] 2. Chasse à l'écho · [x] 3. Maze Runner ·
  [x] 4. Buzz the Tune · [x] 5. Simon Says NeoPixel ·
  [x] 6. Maths la distance · [x] 7. Robot Soccer ·
  [x] 8. Course suiveur de ligne · [x] 9. PWM Lab · [x] 10. Décodeur Morse

### Bonus livré pendant la Phase 1

- [x] **8 Labs mono-thèmes** (`labs/`) : Joystick · Distance · Musique ·
  Servos · IR · Lumières · Vision · Co-Pilote
- [x] **Journal de messages** à droite dans chaque Lab, fidèle au format
  `> #N VERB` / `< ECHO` de l'app principale
- [x] **FABs cockpit déplaçables** (Connect / Labs / Stop) avec persistance
  de position en localStorage
- [x] **Surface workshops** : manuel bilingue, livret, cartes mémo,
  animations, hub
- [x] **Flyer + poster pour enfants** (FR, 8 ans+) avec étoiles BD,
  vrais QR codes, mise à l'échelle mobile
- [x] **Nettoyage de marque** `ROBI-9 LAB → MAQUEEN LAB` dans HTML/CSS/JS
- [x] **HTML auto-rendu pour chaque `.md`** (`docs/_md-render.js`)
- [x] **Sanitiseur défensif de thème** dans chaque lab + hub

---

## 🎯 Phase 2A — Portée (transformer le produit en adoption)

L'app est super ; presque personne ne sait qu'elle existe.

| # | Item | Pourquoi maintenant |
|---|------|---------------------|
| 1 | **Parité i18n du cockpit principal** (FR + AR) | Docs et workshops sont trilingues ; pas le cockpit. Bloque les écoles francophones/arabophones. ~1 jour avec le pattern `T={en,fr,ar}` existant. |
| 2 | **Pack Etsy v1 prêt-à-lister** | `etsy-package/` est à moitié cuit. Finir : photos hero, copy listing verrouillée, carte démarrage. C'est ta distribution. |
| 3 | **Kit enseignant** — 1 fiche pédago + grille par Lab | 8 labs × 1 fiche = 8 pages. Vendable aux écoles instantanément. |
| 4 | **Export PDF flyer/poster** qualité impression | Ajouter un CTA "Save as PDF" + aperçu A4 vérifié. Là, les profs doivent connaître Ctrl+P. |
| 5 | **Set de défis alignés programme** (Cycle 3/4 FR · K-8 EN) | Cartographier Labs/jeux existants vers objectifs d'apprentissage formels. Les profs en ont besoin verbatim. |

### Checklist
- [ ] 1. Parité i18n — cockpit principal (FR + AR)
- [ ] 2. Pack Etsy v1 — prêt-à-lister
- [ ] 3. Kit enseignant — 8 fiches pédago + grilles
- [ ] 4. Export PDF depuis flyer/poster
- [ ] 5. Cartographie programme (cycles FR + grades EN)

---

## 🛠 Phase 2B — Robustesse (pour que ça pourrisse pas)

| # | Item | Pourquoi maintenant |
|---|------|---------------------|
| 6 | **Tests smoke** (Playwright headless) | 8 labs + app principale = beaucoup de surface. Une PR peut casser un Lab silencieusement. ~200 LdC couvrent 80% des régressions. |
| 7 | **Découper `maqueen-tab.js` (4580 LdC)** | Un fichier, un accident. Modulariser par carte (Drive, Servos, LEDs, etc.). Pré-condition à tout futur travail sur l'app principale. |
| 8 | **GitHub Actions CI** — lint + tests + déploiement Pages | Là, chaque push est de l'espoir. Workflow de 30 lignes. |
| 9 | **Passe a11y** — clavier, anneaux focus, ARIA sur FABs/labs | Accessibilité enfants handicapés = vrai argument de vente et vrai bug (FABs pas atteignables au clavier). |
| 10 | **Budget perf** — mesurer first-paint + bundle JS sur les Labs | Les Labs sont rapides sur desktop, lents sur tablettes Android cheap (matériel école). Budget : ≤ 1.5 s LCP sur tablette à 100 €. |

### Checklist
- [ ] 6. Tests smoke pour les 8 labs + chemin connect/disconnect principal
- [ ] 7. `js/maqueen-tab.js` → `js/maqueen/{drive,servos,leds,...}.js`
- [ ] 8. Workflow CI (lint, tests, déploiement au vert)
- [ ] 9. Audit a11y — nav clavier, ARIA, contraste
- [ ] 10. Budget perf + Lighthouse CI

---

## 🚀 Phase 2C — Profondeur (approfondir ce qui marche déjà)

| # | Item | Pourquoi maintenant |
|---|------|---------------------|
| 11 | **3 nouveaux labs depuis `wishlist.html`** (top votés) | Canaliser les nouvelles idées via la wishlist que tu viens de construire. Choisir 3, livrer un milestone "Labs v2". |
| 12 | **Lab Multi-robot** (WebRTC peer-to-peer) | Phase 1 #10 cochée mais la démo n'est pas first-class. Deux Maqueens qui dansent = viral. |
| 13 | **Badges progression / passeport enfant** | Suit quels Labs ils ont complétés. localStorage seul — pas de backend. Gros motivateur. |
| 14 | **Framework add-on** (capteurs Gravity + accessoires I2C) | Espace de noms verbe stubbé dans le firmware. Débloque "qu'est-ce que je peux brancher d'autre ?". |
| 15 | **Firmware Phase 2** (`firmware/v2-raw-pins.ts`) | Même protocole fil, appels `pins.*` bruts au lieu de la lib `maqueen.*` — pour apprenants avancés. |

### Checklist
- [ ] 11. Top 3 labs wishlist livrés
- [ ] 12. Démo multi-robot dance (lab first-class)
- [ ] 13. Passeport / badges enfant
- [ ] 14. Framework add-on + premier accessoire I2C
- [ ] 15. Firmware v2-raw-pins

---

## ⚡ Multiplicateurs — petit effort, grand levier

- [ ] **"Démo sans robot" en un clic** — un shim BLE factice dans chaque Lab
  pour que les enfants/profs puissent essayer l'app *avant* d'acheter le matériel.
  Levier de conversion.
- [ ] **Liens partage `/share`** — encoder config robot + thème + langue dans le
  hash URL pour qu'un prof puisse partager "exactement cette config Lab" en un lien.
- [ ] **Télémétrie locale uniquement** — heatmap `localStorage` de "quel Lab j'ai
  ouvert le plus" pour informer les investissements futurs. Zéro coût vie privée.

---

## ⚠️ Anti-patterns à éviter

- **Pas de nouvelle fonctionnalité avant la découpe `maqueen-tab.js`** (Phase 2B #7).
  Chaque nouvelle carte aggrave le fichier de 4580 lignes.
- **Pas de nouveau Lab sans tests smoke** pour lui. Bugs récurrents (mount logger
  joystick, double-mount co-pilot) le prouvent.
- **Ne traduis pas le cockpit principal à la main** — câble-le au même pattern
  `T={en,fr,ar}` que `workshops/manual` et laisse-le passer à l'échelle.

---

## Comment utiliser ce fichier

- Nouvelles idées → vont dans [labs/wishlist.html](../labs/wishlist.html), pas ici.
- Prendre un item → coche-le (`- [x]`), commit avec le numéro d'item dans
  le message (ex. `feat(2B-7): découpe maqueen-tab.js`).
- Une sous-section Phase 2 est "fait" quand sa checklist est entièrement cochée —
  bump le milestone (ex. v0.2.0 = Phase 2A complète).
