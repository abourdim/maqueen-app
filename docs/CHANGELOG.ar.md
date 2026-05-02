# سجلّ التغييرات

## v0.1.60 — 2026-05-02

توسُّع كبير في السطح : مجلَّد `labs/` يحوي 8 مختبرات مركَّزة للأطفال، أزرار FAB قابلة للسحب في كوكبيت التطبيق الرئيسي، تحديث للعلامة، ومواد workshop قابلة للطباعة (منشور + ملصق) مع QR حقيقيّة.

### مُضاف — سطح Labs (`labs/`)

- **8 مختبرات مركَّزة** : Joystick، Distance، Music، Servos، IR، Lights، Vision، Co-Pilot. كلّ مختبر يتّصل عبر نفس `js/ble.js`، يربط الروبوت المباشر، ويثبِّت على اليمين **سجلّ رسائل** أمينًا لـMESSAGE LOG في التطبيق الرئيسي (TX `> #N VERB` / RX `< ECHO`).
- مركز `labs/index.html` + `labs/wishlist.html` (لوحة تصويت للمختبر القادم).
- `labs/lab-logger.js` + `.css` — مسجِّل مثبَّت يمينًا مع مقبض drag-resize، `lockShimHook` عبر `Object.defineProperty` (سلسلة handlers غير قابلة للكتابة فوقها)، classifyLine() يكتشف TX/RX/ERR تلقائيًّا.
- مُعقِّم مظهر دفاعيّ في كلّ مختبر + مركز : `if (_validThemes.indexOf(t) === -1) t = 'carbon'` — يحمي لوحة المختبرات (`carbon / forest / steel / paper / pearl`) من حوادث انتشار localStorage بين الأسطح.

### مُضاف — كوكبيت (التطبيق الرئيسي)

- **أزرار FAB قابلة للسحب** : CONNECT، LABS، STOP. سحب pointer-events بعتبة click-vs-drag 8 بكسل ؛ المواقع تُحفظ في localStorage. مرساة LABS تضبط `draggable=false` + `dragstart preventDefault` لإبطال اعتراض drag-to-bookmark في HTML5.

### مُضاف — Workshops

- `workshops/flyer.html` + `workshops/poster.html` — v2 جذّابة للأطفال (FR، 8 سنوات+).
  - انفجارات قصصيّة (POW / BAM / ZAP / BOOM عبر نجوم 12 نقطة بـclip-path).
  - انبعاثات موجات خلف المسكوت، فقّاعة كلام "VROUM VROUM!".
  - رسوم SVG متحرّكة : مسح الرادار، موجة السيرفو، نوتات الموسيقى، نبضة LED.
  - QR code حقيقي عبر `js/qrcode.min.js` (واجهة qrcode-generator : `createSvgTag()`).
  - `assets/logo.svg` الرسمي + wordmark "MAQUEEN LAB" في hero.
  - **تحجيم تلقائي على الجوّال** : التخطيط الداخلي A4 محفوظ ؛ JS يضع `transform: scale()` على viewports ≤ 820 بكسل ويُقلّص ارتفاع layout-box كي لا يكون هناك ذيل أبيض. مسار الطباعة لم يُمَسّ (لا يزال A4 حقيقيًّا).

### مُصلَح — الموثوقيّة

- **`sw.js`** — `cache.addAll` الذرّي كان يفشل على assets مفقودة. الآن `cache.add().catch()` لكلّ asset. حُذفت 5 إدخالات asset ميّتة. أُعيد تسمية الكاش `maqueen-lab-v11`.
- **`js/ble-scheduler.js`** — الـwrapper كان يبتلع الوعد المنتظَر (`return throttledSend(line)`).
- **مسجِّل مختبر Joystick** — handler الـDOMContentLoaded كان داخل IIFE تشغَّل *بعد* DCL. أُصلح بـmount يدرك readyState.
- **مختبر Co-Pilot** — DCL + احتياطي readyState شُغِّلا معًا، فضوعف mount المسجِّل. أُضيف حارس `_copilotMounted`.

### مُصلَح — المظاهر

- عُكِس توحيد `mb_theme → robi.theme` بين الأسطح — التطبيق الرئيسي والمختبرات لها **لوحات مختلفة** (فقط `forest` يتقاطع). كلّ سطح يملك مفتاح localStorage الخاصّ به.
- أُضيف مُعقِّم المظهر إلى كلّ المختبرات + `labs/index.html` + `labs/wishlist.html`.
- انحدار مختبر Servo : كان المُعقِّم يعمل *قبل* احتياطي localStorage → reset إلى `carbon` في كلّ زيارة. أُعيد ترتيبه.

### مُغيَّر — العلامة

- Sweep `ROBI-9 LAB` → `MAQUEEN LAB` عبر سلاسل HTML *و* تعليقات CSS / JS (`docs/doc-shell.css`، `workshops/theme.css`، `js/voice-picker.js`).

### الوثائق

- `docs/index.html` + كلّ صفحة guide / pinout / plan / schematics : مُحدِّدات مظهر + لغة، شارة مسكوت Maqueen، أمينة لـ`workshops/hub.html`.

## v0.1.55 — 2026-04-27

تبويب Maqueen صار البوّابة الأماميّة. تنظيف ضخم لعناصر التحكّم المكرَّرة في
تبويبات Playground الفرعيّة، إعادة كتابة كبيرة لموثوقيّة BLE، وكميّة من
صقل البرنامج الثابت.

### مُضاف — UI

- **تبويبان علويّان** : 🤖 **Maqueen** (UI الروبوت الحقيقي) و 🧪 **Playground**
  (مجموعة قابلة للطيّ من تبويبات bit-playground الفرعيّة القديمة).
- **بطاقات تبويب Maqueen** : Drive · Servos (مع مُحدِّد Mechanic-Kit :
  Forklift / Loader / Beetle / Push) · LEDs بسيطة · NeoPixels · Buzzer
  · Ultrasonic · جهاز تحكّم IR · مستشعرات الخطّ (وضع Follow-line التلقائي يعيش
  داخل هذه البطاقة الآن).
- **شريط مستشعرات مباشر** عرضيًّا : LINE، DIST، IR، ACC، BLE bench
  (مُرسَل · مُصدى · مفقود · ms متوسّط)، ثلاثة أزرار سبر، رقاقة
  `streams: ON/OFF`.
- **Toggle تلقائي للـstreams** on/off عند دخول/خروج التبويبات
  Sensors / Graph / 3D.
- خيار **Hold to drive (إفلات = توقّف)** في لوحة Drive.
- **شرائح معدّل auto-poll DIST/LINE** (200–2000 مللي ثانية) وشريحة
  tick Follow-line (100–1000 مللي ثانية) — كلّها محفوظة في localStorage.
- الموسوبات التلقائيّة **تتوقَّف عند مغادرة تبويب Maqueen** لتوفير
  عرض BLE.

### مُضاف — البرنامج الثابت (الآن v0.1.55)

- **streams ACC / LIGHT / SOUND** تُرسل نبضة قلب ≥ مرّة كلّ
  ~500–1000 مللي ثانية حتّى لو لم تتغيّر القيمة، كي لا يبدو Graph مجمَّدًا.
- فعل **`STREAM:on|off`** للاشتراك/إلغاء الاشتراك في streams ACC/LIGHT/SOUND
  (مغلق افتراضيًّا للحفاظ على قناة BLE حرّة).
- **`LM:HEX`** — bitmap مصفوفة LED 5×5 ؛ التبويب الفرعي Controls يستطيع الرسم
  على اللوحة.
- أفعال **`OTHER:*`** من تبويب More تُظهر الآن استجابة مرئيّة على شاشة micro:bit
  (أرقام، قلب، أسهم، أيقونات switch، رسوم أعمدة، نصّ متحرّك) بدل ack صامت.
- **`DIST?`** يُرجع `DIST:-` بدل `DIST:500` المزيَّف عندما لا توجد عقبة.
- **`HELLO` / `HELLO:<ver>`** يؤكّد الاتّصال ويُبلِّغ نسخة البرنامج الثابت
  على بطاقة Connect.

### مُصلَح — BLE / الاتّصال

- **مُسلسِل عالميّ واحد للكتابة** ينتظر كلّ وعد `writeValue()`.
  لا مزيد من `NetworkError: GATT operation already in progress`.
- **مصدر حقيقة واحد لحالة الاتّصال** — إشارة DOM +
  MutationObserver، يبثّ events `connected` / `disconnected`.
- **الإرسالات المعلَّقة تُرفض عند الانفصال** (لا مزيد من تعلُّقات صامتة).
- **حُذف `input.compassHeading()` من auto-stream** — كان يُطلق
  معايرة tilt-game التي تحجب handler الـBLE. السبب الجذري لعَرَض
  "no echo" الذي دام طويلاً.

### محذوف (تكرارات لوحات تبويب Maqueen)

- بطاقات Touch P0 / P1 / P2 (Maqueen يصل P13/P14 لمستشعرات الخطّ ؛
  P0/P1/P2 غير معرَّضة للتلامس).
- بطاقة Buzzer من Controls (تكرار لـMaqueen Buzzer).
- بطاقات Servo / LED / Buzzer من More (تكرارات للوحات Maqueen).
- التبويب الفرعي GamePad (تكرار لـMaqueen Drive).
- التبويب الفرعي Motors (تكرار لـMaqueen Servos مع مُحدِّد kit).

عدد صافي للتبويبات الفرعيّة Playground : **8 → 6**.

### مُغيَّر — سياسة build/version

- خطّاف pre-commit يرفع `BUILD_VERSION` تلقائيًّا **فقط** عندما يكون
  `firmware/v1-maqueen-lib.ts` ضمن التغيير المهيَّأ. لم تعد commits الوثائق
  وحدها ترفع لافتة النسخة — صار الختم يتتبَّع تغييرات البرنامج الثابت الحقيقيّة.
- ملفّ `.hex` **لا** يُترجَم تلقائيًّا. أعِد بناءه في MakeCode وأعِد الفلش
  عند تغيير النسخة (انظر الدليل → "Building the firmware .hex").

## v0.1.x — auto-bump مفعَّل

خطّاف pre-commit (`tools/git-hooks/pre-commit`) يرفع الآن نسخة patch البرنامج
الثابت + تاريخ build بـUTC في كلّ commit. اضبط
`SKIP_FW_BUMP=1 git commit ...` للانسحاب لـcommit محدَّد.

## v0.1.0 — 2026-04-26 (قيد التقدّم)

هيكل أوّلي. fork من [bit-playground](https://github.com/abourdim/bit-playground) v1.2.0.

### مُضاف

- بنية المشروع مُشتقّة من bit-playground.
- إعدادات خاصّة بـMaqueen (`package.json`، `product.json`، `manifest.json`).
- هيكل البرنامج الثابت لـMaqueen Lite v4 (`firmware/v1-maqueen-lib.ts`) — أفعال BLE UART مع تسلسل + تأكيد بالصدى، مرآة USB التسلسليّة، لافتة الإقلاع.
- Wrapper جدولة BLE (`js/ble-scheduler.js`) — يُغلِّف `js/ble.js` الموجود مع أرقام تسلسل، التحقّق من الصدى، coalescing، rate limiting، سجلّ الرسوم المتحرّكة. **لا يُعدِّل `js/ble.js`.**
- Servo Explorer (تجريبي) — مرئي + معايرة + مسح + لوحة كود + auto-demo.

### محذوف

- نماذج 3D غير Maqueen من bit-playground (`arm.js`، `balance.js`، `buggy.js`، `weather.js`).
- وثائق (`docs/`) وحزمة Etsy لـbit-playground (ستُولَّد من جديد لـmaqueen-app).
- هيكل makecode-extension لـbit-playground (مُستبدل ببرنامج ثابت خاصّ بـMaqueen).
- هويّة bit-playground من الإعدادات.

### ملاحظات

- `js/ble.js` من bit-playground مُعاد استخدامه **بدون تغيير**. الكود الجديد يُغلِّفه ؛ لا يُعدِّله أبدًا.
- البرنامج الثابت يستخدم امتداد MakeCode `pxt-maqueen` للوصول إلى العتاد.
- نفس بروتوكول السلك BLE UART سيعمل مع البرنامج الثابت raw-pin المستقبليّ (`firmware/v2-raw-pins.ts`).
