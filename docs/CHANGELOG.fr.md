# Changelog

## v0.1.60 — 2026-05-02

Grosse expansion de surface : un dossier `labs/` avec 8 labos mono-thèmes pour enfants, FABs cockpit déplaçables dans l'app principale, nettoyage de marque, et supports workshop imprimables (flyer + poster) avec vrais QR codes.

### Ajouté — Surface Labs (`labs/`)

- **8 Labs mono-thèmes** : Joystick, Distance, Musique, Servos, IR, Lumières, Vision, Co-Pilote. Chaque labo se connecte via le même `js/ble.js`, monte le robot live, et épingle à droite un **journal de messages** fidèle au MESSAGE LOG de l'app principale (TX `> #N VERB` / RX `< ECHO`).
- Hub `labs/index.html` + `labs/wishlist.html` (tableau de vote pour le prochain labo).
- `labs/lab-logger.js` + `.css` — logger épinglé à droite avec poignée drag-resize, `lockShimHook` via `Object.defineProperty` (chaîne de handlers non-écrasable), classifyLine() auto-détecte TX/RX/ERR.
- Sanitiseur de thème défensif dans chaque labo + hub : `if (_validThemes.indexOf(t) === -1) t = 'carbon'` — protège la palette labs (`carbon / forest / steel / paper / pearl`) des accidents de propagation localStorage cross-surface.

### Ajouté — Cockpit (app principale)

- **FABs déplaçables** : CONNECT, LABS, STOP. Drag pointer-events avec seuil click-vs-drag de 8 px ; positions persistées en localStorage. L'ancre LABS définit `draggable=false` + `dragstart preventDefault` pour neutraliser l'interception drag-to-bookmark de HTML5.

### Ajouté — Workshops

- `workshops/flyer.html` + `workshops/poster.html` — v2 attractive pour enfants (FR, 8 ans+).
  - Étoiles BD (POW / BAM / ZAP / BOOM via étoiles 12 pts en clip-path).
  - Émanations d'ondes derrière le mascot, bulle de parole "VROUM VROUM!".
  - Illustrations SVG animées : balayage radar, vague servo, notes musicales, pulsation LED.
  - Vrai QR code via `js/qrcode.min.js` (API qrcode-generator : `createSvgTag()`).
  - `assets/logo.svg` officiel + wordmark "MAQUEEN LAB" dans le hero.
  - **Mise à l'échelle mobile** : layout interne A4 préservé ; JS pose `transform: scale()` sur les viewports ≤ 820 px et collapse la hauteur de la layout-box pour qu'il n'y ait pas de queue blanche. Le chemin impression reste intact (toujours vrai A4).

### Corrigé — Fiabilité

- **`sw.js`** — `cache.addAll` atomique échouait sur des assets manquants. Maintenant `cache.add().catch()` par asset. 5 entrées d'asset mortes supprimées. Cache renommé `maqueen-lab-v11`.
- **`js/ble-scheduler.js`** — le wrapper avalait la promesse attendue (`return throttledSend(line)`).
- **Logger labo Joystick** — le handler DOMContentLoaded était dans une IIFE qui tournait *après* DCL. Corrigé avec un mount aware de readyState.
- **Labo Co-Pilote** — DCL + fallback readyState se déclenchaient tous les deux, double-mountant le logger. Ajout d'un guard `_copilotMounted`.

### Corrigé — Theming

- Reverté l'unification cross-surface `mb_theme → robi.theme` — l'app principale et les labs ont **des palettes différentes** (seul `forest` se chevauche). Chaque surface possède sa propre clé localStorage.
- Ajout du sanitiseur de thème dans tous les labs + `labs/index.html` + `labs/wishlist.html`.
- Régression labo Servo : le sanitiseur tournait *avant* le fallback localStorage → reset à `carbon` à chaque visite. Réordonné.

### Changé — Marque

- Sweep `ROBI-9 LAB` → `MAQUEEN LAB` à travers les chaînes HTML *et* les commentaires CSS / JS (`docs/doc-shell.css`, `workshops/theme.css`, `js/voice-picker.js`).

### Docs

- `docs/index.html` + chaque page guide / pinout / plan / schematics : sélecteurs thème + langue, pill mascot Maqueen, fidèle à `workshops/hub.html`.

## v0.1.55 — 2026-04-27

L'onglet Maqueen est désormais la porte d'entrée. Gros nettoyage des contrôles
dupliqués dans les sous-onglets Playground, grosse réécriture de fiabilité BLE,
et un paquet de polish firmware.

### Ajouté — UI

- **Deux onglets du haut** : 🤖 **Maqueen** (UI robot réel) et 🧪 **Playground**
  (groupe pliable des sous-onglets historiques bit-playground).
- **Cartes onglet Maqueen** : Drive · Servos (avec sélecteur Mechanic-Kit :
  Forklift / Loader / Beetle / Push) · LEDs simples · NeoPixels · Buzzer
  · Ultrason · Télécommande IR · Capteurs ligne (le mode Follow-line auto vit
  désormais dans cette carte).
- **Bandeau capteurs live** en haut : LINE, DIST, IR, ACC, BLE bench
  (envoyés · écho · perdus · ms moy), trois boutons de sondage, puce
  `streams: ON/OFF`.
- **Toggle auto des streams** on/off à l'entrée/sortie des sous-onglets
  Sensors / Graph / 3D.
- Option **Hold to drive (lâche = stop)** dans le panneau Drive.
- **Sliders de fréquence auto-poll DIST/LINE** (200–2000 ms) et slider
  tick Follow-line (100–1000 ms) — tous persistés en localStorage.
- Les sondes auto **se mettent en pause à la sortie de l'onglet Maqueen**
  pour préserver la bande BLE.

### Ajouté — Firmware (maintenant v0.1.55)

- **Streams ACC / LIGHT / SOUND** émettent un battement ≥ une fois par
  ~500–1000 ms même si la valeur n'a pas changé, pour que le Graph n'ait
  jamais l'air figé.
- Verbe **`STREAM:on|off`** pour opt-in/out des streams ACC/LIGHT/SOUND
  (off par défaut pour garder le canal BLE libre).
- **`LM:HEX`** — bitmap matrice LED 5×5 ; le sous-onglet Controls peut dessiner
  sur la carte.
- Les verbes **`OTHER:*`** de l'onglet More montrent désormais un retour visible
  à l'écran micro:bit (chiffres, cœur, flèches, icônes switch, bargraphs, texte
  défilant) au lieu d'ack silencieux.
- **`DIST?`** retourne `DIST:-` au lieu du `DIST:500` bidon quand aucun obstacle
  n'est détecté.
- **`HELLO` / `HELLO:<ver>`** confirme la connexion et reporte la version firmware
  sur la carte Connect.

### Corrigé — BLE / connectivité

- **Sérialiseur global d'écriture** attend chaque promesse `writeValue()`.
  Plus de `NetworkError: GATT operation already in progress`.
- **Une source de vérité pour l'état de connexion** — signal DOM +
  MutationObserver, broadcast events `connected` / `disconnected`.
- **Envois en attente rejetés à la déconnexion** (plus de hangs silencieux).
- **Suppression de `input.compassHeading()` du auto-stream** — il déclenchait
  la calibration tilt-game qui bloquait le handler BLE. Cause racine du symptôme
  "no echo" qui durait depuis longtemps.

### Supprimé (doublons des panneaux onglet Maqueen)

- Cartes Touch P0 / P1 / P2 (Maqueen câble P13/P14 aux capteurs ligne ;
  P0/P1/P2 pas exposés au touch).
- Carte Buzzer dans Controls (doublon du Buzzer Maqueen).
- Cartes Servo / LED / Buzzer dans More (doublons des panneaux Maqueen).
- Sous-onglet GamePad (doublon du Drive Maqueen).
- Sous-onglet Motors (doublon du Servos Maqueen avec sélecteur kit).

Compte net sous-onglets Playground : **8 → 6**.

### Changé — politique build/version

- Le hook pre-commit auto-incrémente `BUILD_VERSION` **uniquement** quand
  `firmware/v1-maqueen-lib.ts` fait partie du commit. Les commits docs n'incrémentent
  plus le label de version — le tampon suit désormais les vrais changements firmware.
- Le `.hex` n'est **pas** compilé automatiquement. Reconstruis-le dans MakeCode
  et reflashe quand la version change (voir Guide → "Building the firmware .hex").

## v0.1.x — auto-bump activé

Le hook pre-commit (`tools/git-hooks/pre-commit`) incrémente désormais la version
patch firmware + la date build UTC à chaque commit. Définis
`SKIP_FW_BUMP=1 git commit ...` pour opt-out sur un commit spécifique.

## v0.1.0 — 2026-04-26 (en cours)

Squelette initial. Fork depuis [bit-playground](https://github.com/abourdim/bit-playground) v1.2.0.

### Ajouté

- Structure projet forkée depuis bit-playground.
- Config spécifique Maqueen (`package.json`, `product.json`, `manifest.json`).
- Squelette firmware Maqueen Lite v4 (`firmware/v1-maqueen-lib.ts`) — verbes BLE UART avec séquence + confirmation par écho, miroir USB série, bannière de boot.
- Wrapper scheduler BLE (`js/ble-scheduler.js`) — enrobe le `js/ble.js` existant avec numéros de séquence, validation d'écho, coalescing, rate limiting, registre d'animations. **Ne modifie pas `js/ble.js`.**
- Explorateur Servo (pilote) — visuel + calibration + balayage + panneau code + auto-démo.

### Supprimé

- Modèles 3D non-Maqueen de bit-playground (`arm.js`, `balance.js`, `buggy.js`, `weather.js`).
- Docs (`docs/`) et pack Etsy de bit-playground (seront régénérés pour maqueen-app).
- Squelette makecode-extension de bit-playground (remplacé par firmware spécifique Maqueen).
- Branding bit-playground des configs.

### Notes

- `js/ble.js` de bit-playground est réutilisé **inchangé**. Le nouveau code l'enrobe ; ne l'édite jamais.
- Le firmware utilise l'extension MakeCode `pxt-maqueen` pour l'accès matériel.
- Le même protocole fil BLE UART marchera avec le futur firmware raw-pin (`firmware/v2-raw-pins.ts`).
