# etsy-package 🛒 (slim)

Minimal Etsy-release bundle for **Maqueen Lab**. Slim by design — only
the essentials: the ZIP builder, the buyer-facing printables, the buyer
license, and a single Etsy-listing copy file.

## Layout

```
etsy-package/
├── README.md                 ← you are here
├── LICENSE.txt               ← buyer license
├── USERGUIDE.md              ← buyer-facing usage guide
├── README-quickstart.html    ← buyer welcome page (first thing they see)
├── classroom-poster.html     ← printable A4 (classroom wall)
├── quickstart-card.html      ← printable A4 (5-minute setup card)
├── build-package.js          ← node script that builds the ZIP
└── seller-only/              ← never copied into the ZIP
    ├── ETSY_LISTING.md       ← copy you paste into Etsy
    └── ETSY_LISTING.html     ← rendered preview
```

## Build the ZIP

```bash
node etsy-package/build-package.js
```

The script reads the version from `product.json`, copies the live app
(`index.html`, `js/`, `assets/`, `docs/`, `firmware/`, `labs/`, `workshops/`)
plus the buyer-facing files in this folder, then emits:

```
etsy-package/MaqueenLab-vX.Y.Z.zip
```

`seller-only/` is **never** copied into the ZIP.

## Publish on Etsy (manual steps)

1. Run `node etsy-package/build-package.js` → upload the resulting `.zip`
   as the listing file.
2. Open `seller-only/ETSY_LISTING.md` → paste the title, tags, and
   description into the Etsy listing form.
3. Hero photo: shoot a real micro:bit propped on a laptop running the
   app. Upload as image #1.
4. (Optional) Record a 60-second video showing pairing + driving;
   upload as the listing video.
5. Hit Publish.

That's it. Everything else (Pinterest pins, testimonials, video
teleprompter, multi-lang outreach templates, hero compositors,
visual-regression CI, etc.) was removed in the v0.2.0 slimdown to
keep this folder honest about what's actually shipped.

## Live demo

https://abourdim.github.io/maqueen-lab/
