# Changelog

## v0.1.60 — 2026-05-02

Big surface expansion: a `labs/` folder with 8 single-purpose kid labs, draggable cockpit FABs in the main app, brand sweep, and printable workshop artifacts (flyer + poster) with real QR codes.

### Added — Labs surface (`labs/`)

- **8 single-purpose Labs**: Joystick, Distance, Music, Servos, IR, Lights, Vision, Co-Pilot. Each lab connects via the same `js/ble.js`, mounts the live robot, and pins a right-rail **Message Log** faithful to the main app's MESSAGE LOG (TX `> #N VERB` / RX `< ECHO` format).
- `labs/index.html` hub + `labs/wishlist.html` (next-lab vote board).
- `labs/lab-logger.js` + `.css` — pinned right-rail logger with drag-resize, `lockShimHook` via `Object.defineProperty` (un-overridable handler chain), classifyLine() auto-detect of TX/RX/ERR.
- Defensive theme sanitizer in every lab + hub: `if (_validThemes.indexOf(t) === -1) t = 'carbon'` — protects the lab palette (`carbon / forest / steel / paper / pearl`) from cross-surface localStorage propagation accidents.

### Added — Cockpit (main app)

- **Draggable FABs**: CONNECT, LABS, STOP. Pointer-events drag with 8px click-vs-drag threshold; positions persist in localStorage. LABS anchor sets `draggable=false` + `dragstart preventDefault` to defeat HTML5 drag-to-bookmark interception.

### Added — Workshops

- `workshops/flyer.html` + `workshops/poster.html` — kid-attracting v2 (FR, 8 ans+).
  - Comic-book bursts (POW / BAM / ZAP / BOOM via 12-pt clip-path stars).
  - Wave emanations behind mascot, "VROUM VROUM!" speech bubble.
  - Animated SVG illustrations: radar sweep, servo wave, music notes, LED pulse.
  - Real QR code via `js/qrcode.min.js` (qrcode-generator API: `createSvgTag()`).
  - Official `assets/logo.svg` + "MAQUEEN LAB" wordmark in the hero.
  - **Mobile-friendly scale-to-fit**: A4 internal layout preserved; JS sets `transform: scale()` on viewports ≤ 820px and collapses the layout-box height so there's no white tail. Print path untouched (still true A4).

### Fixed — Reliability

- **`sw.js`** — atomic `cache.addAll` was failing on missing assets. Now per-asset `cache.add().catch()`. Removed 5 dead asset entries. Cache renamed `maqueen-lab-v11`.
- **`js/ble-scheduler.js`** — wrapper was swallowing the awaited promise (`return throttledSend(line)`).
- **Joystick lab logger** — DOMContentLoaded handler was inside an IIFE that ran *after* DCL. Fixed with readyState-aware mount.
- **Co-Pilot lab** — both DCL + readyState fallback fired, double-mounting the logger. Added `_copilotMounted` guard.

### Fixed — Theming

- Reverted the `mb_theme → robi.theme` cross-surface unification — main app and labs have **different palettes** (only `forest` overlaps). Each surface owns its own localStorage key.
- Added theme sanitizer to all labs + `labs/index.html` + `labs/wishlist.html`.
- Servo-lab regression: sanitizer ran *before* the localStorage fallback → reset to `carbon` on every visit. Reordered.

### Changed — Brand

- Sweep `ROBI-9 LAB` → `MAQUEEN LAB` across HTML strings *and* CSS / JS comments (`docs/doc-shell.css`, `workshops/theme.css`, `js/voice-picker.js`).

### Docs

- `docs/index.html` + every guide / pinout / plan / schematics page: theme + lang selectors, Robi-9 mascot pill, faithful to `workshops/hub.html`.

## v0.1.55 — 2026-04-27

The Maqueen tab is now the front door. Heavy clean-up of duplicated
controls in the Playground sub-tabs, big BLE-reliability rewrite, and a
bunch of firmware polish.

### Added — UI

- **Two top tabs**: 🤖 **Maqueen** (real-robot UI) and 🧪 **Playground**
  (collapsible group of legacy bit-playground sub-tabs).
- **Maqueen tab cards**: Drive · Servos (with Mechanic-Kit picker:
  Forklift / Loader / Beetle / Push) · Simple LEDs · NeoPixels · Buzzer
  · Ultrasonic · IR remote · Line sensors (Follow-line auto mode now
  lives inside this card).
- **Live sensor strip** across the top: LINE, DIST, IR, ACC, BLE bench
  (sent · echoed · lost · avg ms), three poll buttons, `streams: ON/OFF`
  chip.
- **Streams auto-toggle** on/off when entering/leaving the Sensors /
  Graph / 3D sub-tabs.
- **Hold to drive (release = stop)** option in the Drive panel.
- **DIST/LINE auto-poll rate sliders** (200–2000 ms) and Follow-line
  tick slider (100–1000 ms) — all persisted in localStorage.
- Auto-pollers **pause when leaving the Maqueen tab** to spare BLE
  bandwidth.

### Added — Firmware (now v0.1.55)

- **ACC / LIGHT / SOUND streams** emit a heartbeat ≥ once per
  ~500–1000 ms even when the value hasn't changed, so the Graph never
  looks frozen.
- **`STREAM:on|off`** verb to opt into/out of ACC/LIGHT/SOUND streams
  (off by default to keep the BLE channel free).
- **`LM:HEX`** — 5×5 LED matrix bitmap; the Controls sub-tab can draw
  on the board.
- **`OTHER:*`** verbs from the More tab now show visible micro:bit-screen
  feedback (digits, heart, arrows, switch icons, bar graphs, scrolling
  text) instead of silently acking.
- **`DIST?`** returns `DIST:-` instead of `DIST:500` when no obstacle is
  detected.
- **`HELLO` / `HELLO:<ver>`** confirms connection and reports firmware
  version on the Connect card.

### Fixed — BLE / connectivity

- **Single global write serializer** awaits each `writeValue()` Promise.
  No more `NetworkError: GATT operation already in progress`.
- **One source of truth for connection state** — DOM signal +
  MutationObserver, broadcasts `connected` / `disconnected` events.
- **Pending sends rejected on disconnect** (no more silent hangs).
- **Removed `input.compassHeading()` from auto-stream** — it was
  triggering tilt-game calibration that blocked the BLE handler. Root
  cause of the long-standing "no echo" symptom.

### Removed (duplicates of Maqueen-tab panels)

- Touch P0 / P1 / P2 cards (Maqueen wires P13/P14 to line sensors;
  P0/P1/P2 not exposed for touch).
- Buzzer card from Controls (duplicate of Maqueen Buzzer).
- Servo / LED / Buzzer cards from More (duplicates of Maqueen panels).
- GamePad sub-tab (duplicate of Maqueen Drive).
- Motors sub-tab (duplicate of Maqueen Servos with kit picker).

Net Playground sub-tab count: **8 → 6**.

### Changed — build/version policy

- Pre-commit hook auto-bumps `BUILD_VERSION` **only** when
  `firmware/v1-maqueen-lib.ts` is in the staged change. Docs commits no
  longer bump the version label — the stamp now tracks real firmware
  churn.
- The `.hex` is **not** auto-compiled. Re-build it in MakeCode and
  re-flash when the version changes (see User Guide → "Building the
  firmware .hex").

## v0.1.x — auto-bump enabled

Pre-commit hook (`tools/git-hooks/pre-commit`) now bumps the firmware
patch version + UTC build date on every commit. Set
`SKIP_FW_BUMP=1 git commit ...` to opt out for a specific commit.

## v0.1.0 — 2026-04-26 (in progress)

Initial scaffold. Forked from [bit-playground](https://github.com/abourdim/bit-playground) v1.2.0.

### Added

- Project structure forked from bit-playground.
- Maqueen-specific config (`package.json`, `product.json`, `manifest.json`).
- Maqueen Lite v4 firmware scaffold (`firmware/v1-maqueen-lib.ts`) — BLE UART verbs with sequence + echo confirmation, USB serial mirror, boot banner.
- BLE scheduler wrapper (`js/ble-scheduler.js`) — wraps existing `js/ble.js` with sequence numbers, echo validation, coalescing, rate limiting, animation registry. **Does not modify `js/ble.js`.**
- Servo Explorer (pilot) — visual + calibration + sweep + code panel + auto-demo.

### Removed

- bit-playground's non-Maqueen 3D models (`arm.js`, `balance.js`, `buggy.js`, `weather.js`).
- bit-playground's docs (`docs/`) and Etsy package (will be regenerated for maqueen-app).
- bit-playground's makecode-extension scaffold (replaced with Maqueen-specific firmware).
- bit-playground branding from configs.

### Notes

- `js/ble.js` from bit-playground is reused **unchanged**. New code wraps it; never edits it.
- Firmware uses the `pxt-maqueen` MakeCode extension for hardware access.
- Same BLE UART wire protocol works with future raw-pin firmware (`firmware/v2-raw-pins.ts`).
