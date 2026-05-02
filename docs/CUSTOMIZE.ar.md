# قائمة التخصيص — Maqueen Lab

هذا الملفّ مُولَّد بواسطة `apply-template.mjs`. القالب استبدل
المعرِّفات (اسم المنتج، URLs، الأسعار، النسخة) لكن **ليس** المحتوى
الوظيفي. مرّ على القائمة أدناه قبل النشر.

شغِّل `node <مسار-القالب>/verify-clean.mjs` من هذا المجلَّد في أيّ
وقت لمسح المفردات المتبقّية من القالب. كود الخروج 0 = نظيف.

---

## 🖨 موادّ قابلة للطباعة — أعِد كتابة المحتوى
كلّ ملفّ يبدأ بشريط `<!-- REWRITE PER PRODUCT -->`. احذف الشريط
**بعد** إعادة الكتابة. البنية البصريّة لك أن تبقيها ؛
فقط النصّ والخطوات والاختصارات والأمثلة تحتاج تغييرًا.

- [ ] `etsy-package/classroom-poster.html` — العنوان + 5 خطوات كبيرة + شعار التذييل
- [ ] `etsy-package/quickstart-card.html` — تسلسل إعداد 5 دقائق
- [ ] `etsy-package/shortcuts-cheatsheet.html` — اختصارات لوحة المفاتيح، إجراءات خاصّة بالمنتج
- [ ] `etsy-package/lesson-plan-template.html` — جسم درس عيّنة 45 دقيقة
- [ ] `etsy-package/sticker-sheet.html` — 30 شارة إنجاز
- [ ] `etsy-package/README-quickstart.html` — صفحة ترحيب المشتري + "أوّل 3 أشياء تفعلها"

## 🖼 mockups القائمة — أعِد كتابة mockups 2-7

- [ ] `etsy-package/etsy-listing-mockups.html`
   - M1 hero مُعرَّف بقالب ؛ فقط screenshot + شارة التوافق تحتاج لتعديل خاصّ بالمنتج
   - M2 (شبكة 16 خليّة ميزات) — استبدل كلّ الخلايا بميزات المنتج
   - M3 (نداء المعلِّم) — أعِد الكتابة لجمهورك
   - M4 (نداء الطفل) — أعِد كتابة النصّ + الإيموجي
   - M5 (محتوى الـZIP) — اجعله يطابق محتوى ZIP الفعلي
   - M6 (مظاهر / شخصيّات / متغيِّرات)
   - M7 (ثلاثي اللغة أو خصوصيّة أو أيّ زاوية مناسبة)

## 📌 Pinterest pins
- [ ] `etsy-package/seller-only/pinterest-pins.html` — 4 pins عمودي : hero، نداء الجمهور، محتوى ZIP، ميزات/لغات

## 🛒 وثائق البائع (تُلصَق في Etsy — مهمّ)
- [ ] `etsy-package/seller-only/ETSY_LISTING.md` — العنوان، 13 وسم، الوصف، جدول المقارنة، FAQ
- [ ] `etsy-package/seller-only/ETSY_LISTING.html` — توأم HTML للـ.md (يجب أن يطابق)
- [ ] `etsy-package/seller-only/ETSY-1MIN-PLAYBOOK.md` — سيناريو فيديو 60 ث + قائمة لقطات
- [ ] `etsy-package/seller-only/ETSY_PUBLISH_GUIDE.html` — قائمة صور (11 اسم ملفّ صورة غالبًا تحتاج إعادة تسمية)

## 🎥 دليل الفيديو (FR/AR)
- [ ] `etsy-package/seller-only/etsy-playbook.html` — دليل فيديو EN
- [ ] `etsy-package/seller-only/etsy-playbook-fr.html` — فرنسي
- [ ] `etsy-package/seller-only/etsy-playbook-ar.html` — عربي (RTL)

## 🎬 أدوات إنتاج الفيديو (تصوير 60 ث)
هذه الملفّات الثلاثة المُرافقة تحوِّل الدليل إلى تصوير فعلي. أعِد كتابة محتوى
كلّ مشهد لكلّ منتج ؛ احتفظ ببنية الـ8 مشاهد وحدود الزمن.

- [ ] `etsy-package/seller-only/video-teleprompter.html` — تيليبرومتر HTML
   تفاعلي. افتحه على شاشة ثانية، اضغط `F` لـfullscreen، `Space`
   لـcountdown 3-2-1 ثمّ تقدّم تلقائي عبر 8 مشاهد. يعرض سطر SAY بحجم كبير،
   تلميحات DO/CLICK تحته، ساعة مباشرة، شريط تقدّم (يصير أحمر بعد 55 ث).
   أعِد كتابة مصفوفة `SCENES` في وسم `<script>` المضمَّن.
- [ ] `etsy-package/seller-only/video-shoot-card.html` — ورقة A4 جاهزة للطباعة.
   قائمة قبل الطيران + مواصفات Etsy + جدول 8 صفوف + بطاقة سريعة على صفحة واحدة.
   تُحوَّل إلى PNG بـ`build-package.js` (للبائع فقط، ليست في ZIP).
   أعِد كتابة عناصر قبل الطيران وجدول الأقواس ؛ جدول المواصفات يبقى.
- [ ] `etsy-package/tools/captions/video-captions-en.srt` — مسار ترجمة burn-in
   لـCapCut/DaVinci. أعِد كتابة الـ8 كتل ترجمة لتطابق حرفيًّا أسطر SAY في
   التيليبرومتر. التوقيتات (0-3 / 3-10 / 10-20 / 20-30
   / 30-40 / 40-50 / 50-55 / 55-60) يجب أن تطابق حدود المشاهد.
- [ ] `etsy-package/tools/captions/video-captions-fr.srt` — توأم فرنسي
- [ ] `etsy-package/tools/captions/video-captions-ar.srt` — توأم عربي (RTL ؛
   الأسطر مسبوقة بمعالم U+200F RLM — احتفظ بها)
- [ ] `etsy-package/tools/generate-video.mjs` — مُولِّد قائم على ffmpeg
   يبني MP4 1080×1920 9:16 من 5 screenshots + captions EN.
   v1 شاشة فقط — استبدلها بفيديو عتاد حقيقي بعد التصوير. يتطلَّب
   ffmpeg في PATH. أعِد كتابة نصّ العنوان/CTA في مصفوفة `SCENES` إن لم تتناسب
   البدائل `Maqueen Lab` / `Every component, live in your browser`.
   شغِّل : `node etsy-package/tools/generate-video.mjs`

## 📸 خطّ التقاط التسويق (13 وضعًا + مساعدات)

كلّ المخرجات تنزل في `etsy-package/seller-only/screenshots/` و
`etsy-package/output/`. كلّ أداة قابلة للتشغيل بشكل مستقلّ ؛ الخطّ
الكامل هو :

   capture → (اختياري) annotate → theme-morph → generate-video → visual-regress

- [ ] `capture-screenshots.mjs` — لاقط قائم على Playwright يغطّي كلّ
   التبويبات × 2 (قياسي + حالة اصطناعيّة تبدو live)، أزواج before/after،
   متغيِّرات المظاهر، متغيِّرات النماذج، إثبات offline، تعليقات callout SVG،
   ومخرجات متعدّدة الأبعاد (9:16/1:1/2:3/16:9).
   **مدفوع بالإعدادات — لا تُعدِّل السكريبت.** عدِّل `capture-config.json`
   (نفس المجلَّد). مرجع مملوء في `capture-config.example.json`.
   حقل `_rewrite` في أعلى الإعدادات يسرد الـ10 أقسام التي تحتاج تعديلها
   لـDOM منتجك.
   الأوضاع : `tabs synthetic pairs themes models offline annotated aspects all`.
- [ ] `qr-inject.mjs` — يحقن QR codes موسومة بـUTM في كلّ مادّة قابلة للطباعة.
   `--preview` الافتراضي يكتب في `output/printables-with-qr/` ؛ أضف
   `--inplace` لتعديل HTMLs المصدر مباشرة (قابل للعكس عبر git).
- [ ] `theme-morph.mjs` — يُصيِّر حلقة crossfade مربّعة 1:1 عبر التقاطات
   مظاهرك. MP4 + GIF. يتطلَّب `screenshot-theme-*.png` من وضع التقاط
   themes.
- [ ] `visual-regress.mjs` — فحص هويّة md5 + diffs ffmpeg جنبًا إلى جنب.
   استخدم `--baseline` لالتقاط الحالة الحاليّة ؛ التشغيلات اللاحقة تخرج
   بقيمة غير صفرية إن انحرف أيّ screenshot. عام بالكامل، لا حاجة لإعادة كتابة.
- [ ] `hero-compose.mjs` + `hero-specs.json` — مُركِّب صور hero A/B
   (thumbnails Etsy 1500×1500). أعِد كتابة `hero-specs.json` بـ2-5 متغيِّرات
   لكلّ جمهور ؛ تجربة ترتيب الصور في Etsy تختار الفائز.
- [ ] `generate-gifs.mjs` — GIFs عرض 5 ثوانٍ لـslots صور Etsy +
   Pinterest. **أعِد كتابة** كائن `RECIPES` لكلّ منتج — دالّة `act(page)` لكلّ
   وصفة تحرِّك ميزات تطبيقك أنت.
- [ ] `generate-datasets.mjs` — 100 CSVs مستشعرات اصطناعيّة + README للمعلِّم.
   يحوِّل المنتج المتطلِّب للعتاد → اختياري العتاد. **أعِد كتابة** كائن
   `SCENARIOS` ليطابق أنواع مستشعرات منتجك.
- [ ] `watermark-zip.mjs` — ZIP لكلّ مشترٍ مع اسم المشتري + order ID مطبوعَين
   في README-quickstart.html + LICENSE. الاستخدام :
   `node tools/watermark-zip.mjs --buyer "Alice Smith" --order "12345"`.

**شرط مسبق للالتقاط :** `npm i --save-dev @playwright/test qrcode && npx playwright install chromium`.

## 📜 ترخيص المشتري
- [ ] `etsy-package/LICENSE.txt` — البندان 9 + 10 يذكران "printable materials" ؛
  تأكَّد من أنّ القائمة تطابق المواد القابلة للطباعة الفعلية لديك. البند 3 إخلاء
  المسؤوليّة عن العلامة التجاريّة — حدِّث إن كان منتجك يستخدم علامات تجاريّة
  مختلفة عن BBC micro:bit.

## 📸 Screenshots
- [ ] التقط screenshot حقيقي لـUI الرئيسي لمنتجك → `assets/app-screenshot.png`
  (مُشار إليه من mockup الـhero + pin 1)

## ⚙️ الخطوات الأخيرة
- [ ] `npm install --save-dev @playwright/test qrcode && npx playwright install chromium`
- [ ] `node etsy-package/build-package.js` — يُصيِّر كلّ الـmockups + يبني ZIP
- [ ] `node <template-path>/verify-clean.mjs` — يجب أن يخرج نظيفًا (كود 0)
- [ ] (اختياري) `gh api -X POST "repos/abourdim/maqueen-lab/pages" -f 'source[branch]=main' -f 'source[path]=/'` — يفعِّل GitHub Pages كي يعمل URL العرض المباشر في القائمة فعلاً
- [ ] `git add -A && git commit -m "..." && git push`
- [ ] اتبع `etsy-package/seller-only/TODO.md` للعناصر اليدويّة الثلاثة قبل الإطلاق (صورة منتج حقيقيّة، فيديو 60 ث، رمز ترويج LAUNCH10)

---

## 🔧 ضبط سكريبت verify لكلّ منتج

إن وضع `verify-clean.mjs` علَمًا على مصطلح مشروع لمنتجك
(مثل "gamepad" لتطبيق remote-controller، "led matrix" لتطبيق LED
painter، "sensors" لتطبيق sensor-mapping)، أضِفه إلى
`product.json` :

```json
"ALLOWED_TERMS": ["gamepad", "led matrix"]
```

أعِد تشغيل المتحقِّق. القواعد الموسومة التي يطابق عنوانها مصطلحًا
مسموحًا تُتجاوَز.
