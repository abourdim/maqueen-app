# Maqueen Lab

**Laboratoire BLE web pour le DFRobot Maqueen Lite v4 + kits mécaniques.**

Chaque actionneur et capteur du Maqueen Lite est accessible depuis une carte de l'onglet **🤖 Maqueen** — pilote les roues, positionne les servomoteurs, allume les LEDs et NeoPixels, fais sonner le buzzer, mesure avec l'ultrason, lis la télécommande IR, suis une ligne. Un second onglet **🧪 Playground** garde les sous-onglets historiques de bit-playground (Controls, Sensors, Graph, 3D, Bench, More) pour des expériences libres avec micro:bit. Tout passe par BLE UART ; chaque commande porte un numéro de séquence et est confirmée par écho.

Le dépôt fournit aussi :

- **`labs/`** — 8 **Labos** mono-thèmes pour enfants, chacun centré sur une capacité (Joystick, Distance, Musique, Servos, IR, Lumières, Vision, Co-Pilote). Chaque labo épingle à droite un **journal de messages** fidèle au format TX/RX de l'app principale, avec thèmes/langues alignés sur la documentation (`carbon / forest / steel / paper / pearl`).
- **`docs/`** — Guide utilisateur, Brochage, Plan, Schémas (variantes FR / EN / AR de chacun).
- **`workshops/`** — supports imprimables A4 qualité PDF : **manuel** bilingue, **livret**, **cartes mémo**, **animations**, **hub**, plus un **flyer** et un **poster** attractifs pour enfants (FR, 8 ans+, étoiles BD, vrai QR code → app live, mise à l'échelle mobile).

> **État :** v0.1.60 — onglet Maqueen complet ; surface Labs (8 labos) livrée ; FABs cockpit déplaçables ; nettoyage de marque `ROBI-9 LAB → MAQUEEN LAB` ; flyer + poster v2 avec QR codes. Voir [CHANGELOG.md](docs/CHANGELOG.md) pour les évolutions récentes, [plan.md](docs/plan.md) pour le plan de construction d'origine.

**En ligne :** https://abourdim.github.io/maqueen-lab/

---

## Matériel

DFRobot Maqueen Lite v4 (ROB0148) — robot pédagogique basé sur micro:bit. Kits mécaniques optionnels : Forklift (ROB0156-F), Loader (ROB0156-L), Beetle gripper (ROB0156-B), Push (ROB0156-P).

### Carte des broches (référence rapide)

| Broche | Utilisée par | Notes |
|---|---|---|
| P0 | Buzzer | Broche `music` par défaut |
| P1 | Ultrason TRIG | Conflit : port Gravity |
| P2 | Ultrason ECHO | Conflit : port Gravity |
| P8 | LED Gauche (simple) | Numérique ON/OFF |
| P12 | LED Droite (simple) | Numérique ON/OFF |
| P13 | Capteur ligne Gauche | Numérique 0/1 |
| P14 | Capteur ligne Droite | Numérique 0/1 |
| P19/P20 | Bus I2C | Moteur + RGB + Servos à l'adresse **0x10** |

### Carte des registres I2C 0x10

| Registre | Fonction |
|---|---|
| `0x00` | Moteur M1 (gauche) |
| `0x02` | Moteur M2 (droite) |
| `0x14` | Servo S1 |
| `0x15` | Servo S2 |
| `0x32` | Données 4× LEDs RGB |

Brochage complet, alertes de conflit et spécification du protocole dans [docs/USER_GUIDE.md](docs/USER_GUIDE.md).

---

## Démarrage rapide

1. Flashe `firmware/v1-maqueen-lib.ts` sur ton micro:bit (colle dans [makecode.microbit.org](https://makecode.microbit.org), ajoute l'extension `pxt-maqueen`, télécharge le `.hex`).
2. Allume le Maqueen Lite.
3. Ouvre l'app web dans Chrome / Edge (Web Bluetooth requis).
4. Clique sur **Connect**, associe avec `BBC micro:bit [xxxxx]`.
5. Choisis un Explorateur de Composant et joue.

---

## Lancer en local

**Bref — ne double-clique pas sur `index.html`.** Les règles CORS de Chromium bloquent
`fetch()` de `manifest.json` / `product.json` / `build-info.json` depuis le
protocole `file://`. L'app dégrade proprement (pas d'impact fonctionnel) mais
la console DevTools se remplit d'erreurs rouges, l'invite d'installation PWA
ne s'affiche pas et le Service Worker ne s'enregistre pas.

Choisis le lanceur que tu as sous la main — tous servent `http://localhost:8000` :

| Plateforme | Commande | Notes |
|---|---|---|
| **Windows** | double-clic `serve.bat` | essaie Python, sinon `npx serve` |
| **macOS / Linux** | `./serve.sh` | essaie Python, sinon `npx serve` |
| **Tout système avec Python 3.7+** | `python tools/serve.py` | stdlib seule, pas d'install |
| **Tout système avec Node** | `npm run serve` | utilise `npx serve` (one-shot CDN) |
| **Python via npm** | `npm run serve:py` | lance `tools/serve.py` |

Le lanceur Python accepte un port personnalisé (`python tools/serve.py 8765`)
et ouvre ton navigateur par défaut sauf si `MAQUEEN_NO_BROWSER=1` est défini.

---

## Surfaces

| Surface | Chemin | Rôle |
|---|---|---|
| **App principale** | `index.html` | Cockpit complet Maqueen + Playground (BLE réel) |
| **Labs** | `labs/index.html` | 8 expériences mono-thèmes pour enfants |
| **Docs** | `docs/index.html` | Guide, Brochage, Plan, Schémas (EN/FR/AR) |
| **Workshops** | `workshops/hub.html` | Manuel A4 imprimable, livret, cartes mémo, flyer, poster |

Les **8 Labs** (chacun se connecte via le même `js/ble.js` et monte un journal de messages fidèle à l'app principale) :

| Labo | Ce qu'il enseigne |
|---|---|
| **Joystick** | Pilote le robot avec un stick virtuel ; modes vitesse + char |
| **Distance** | Radar ultrason en direct ; aide au parking, alarme, thérémine |
| **Musique** | Notes au buzzer, piano, séquenceur 8 pas, danse |
| **Servos** | Sliders S1/S2, enregistrement/replay de chorégraphie |
| **IR** | Touches télécommande IR, aperçu de la paire IR du suivi de ligne |
| **Lumières** | 4× ambiances NeoPixel, peintre, suivi de ligne IR avec LEDs |
| **Vision** | Pilote le robot avec ta webcam (visage / posture) |
| **Co-Pilote** | Commandes vocales → mouvements du robot |

---

## Architecture

- **App web** : JS + SVG + CSS purs. Pas de framework. Installable en PWA.
- **BLE** : Web Bluetooth → service Bluetooth UART du micro:bit. Un sérialiseur global d'écriture attend chaque promesse `writeValue()` — plus de `NetworkError: GATT operation already in progress`. L'état de connexion est diffusé via signal DOM + MutationObserver ; les envois en attente sont rejetés à la déconnexion.
- **Protocole** : chaque commande porte un numéro de séquence. Le micro:bit répond `ECHO:N <verb>`. L'app web affiche envoyés / écho / perdus / latence-moy sur la puce BLE bench du bandeau capteurs. `HELLO`/`HELLO:<ver>` rapporte la version du firmware sur la carte Connect.
- **Flux capteurs** : ACC / LIGHT / SOUND streament en continu avec un battement (≥ une fois par ~500–1000 ms) pour que le Graph n'ait jamais l'air figé. Désactivés par défaut — bascule la puce `streams: ON/OFF` dans le bandeau, ou entre dans Sensors / Graph / 3D et ils s'arment automatiquement. DIST / LINE / IR sont sondés à la demande avec sliders de fréquence (200–2000 ms, persistés en localStorage). Les sondes auto se mettent en pause quand on quitte l'onglet Maqueen pour préserver la bande BLE.
- **Firmware** : reste bête. L'app web pilote toutes les animations (balayage, clignotement, arc-en-ciel, tick suivi de ligne) via commandes streamées.
- **Miroir USB série** à 115200 baud — bannière de boot, log RX/TX, commandes exécutées. Utile pour déboguer sans l'app web.

### Version build / firmware

Le hook pre-commit auto-incrémente `BUILD_VERSION` **uniquement** quand `firmware/v1-maqueen-lib.ts` fait partie du commit. Les commits docs-seuls n'incrémentent plus la version — le tampon suit désormais les vrais changements firmware. Le `.hex` n'est **pas** compilé automatiquement ; reconstruis-le dans MakeCode et reflashe quand la version change (voir la section "Building the firmware .hex" du Guide utilisateur).

Voir [plan.md](docs/plan.md) pour le plan complet.

---

## Fork de

Ce projet est un fork de [bit-playground](https://github.com/abourdim/bit-playground) v1.2.0 — sa couche BLE, son moteur de graphe capteurs et sa machinerie i18n sont réutilisés tels quels. **La couche BLE (`js/ble.js`) est traitée comme une dépendance stable et n'est pas modifiée dans ce fork.**

---

## Licence

MIT
