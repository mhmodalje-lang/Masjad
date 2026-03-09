

## تحليل المشاكل وخطة الإصلاح

### المشاكل المكتشفة

**1. أوقات المساجد لا تتطابق مع الأوقات الحقيقية للمسجد**
- من السجلات: عند البحث عن "Masjid Al Rahman" يتم إرجاع أوقات "Tawba Moschee" وليس المسجد المطلوب. السبب: Mawaqit API تُرجع أقرب مسجد مسجل عندها وليس المسجد المطلوب بالضبط.
- `fetch-mosque-times` يأخذ أول نتيجة من Mawaqit بدون التحقق من تطابق الاسم، فيعرض أوقات مسجد آخر.

**2. Overpass API تنتهي بـ timeout متكرر**
- من السجلات: `AbortError: The signal has been aborted` يتكرر كثيراً مع كلا الـ endpoints. الـ timeout الحالي 25 ثانية لكن edge function تنتهي قبله.

**3. خطأ DOM nesting: button داخل button**
- من Console: `validateDOMNesting: <button> cannot appear as a descendant of <button>` — زر "فحص" (line 711-721) هو `Button` داخل `motion.button`.

**4. خطأ framer-motion ref warning**
- `ref is not a prop` تحذير من `AnimatePresence` + `motion.button` في قائمة المساجد.

**5. `useSavedMosqueTimes` لا يطبق فرق الدقائق (diffs)**
- الهوك يتجاهل الـ `SAVED_DIFFS_PREFIX` المحفوظة ولا يطبق `applyTimeDiff` على الأوقات.

---

### خطة الإصلاح

#### 1. إصلاح `fetch-mosque-times` — التحقق من تطابق اسم المسجد
- في `fetchFromMawaqitAPI`: مقارنة اسم المسجد المُرجع مع الاسم المطلوب. إذا لم يتطابق بشكل معقول، إرجاع `null` بدل استخدام أوقات مسجد آخر.
- إضافة دالة مقارنة أسماء بسيطة (تطابق جزئي) لتجنب عرض أوقات مسجد مختلف تماماً.

#### 2. إصلاح timeout في `search-mosques`
- تقليل timeout من 25 ثانية إلى 12 ثانية لتتناسب مع حدود edge function.
- إعطاء أولوية للـ fallback endpoint بشكل أسرع.

#### 3. إصلاح button داخل button
- تغيير `motion.button` في قائمة المساجد (line 664) إلى `motion.div` مع `role="button"` و `onClick`.
- نقل زر "فحص" ليكون عنصر مستقل.

#### 4. إصلاح تحذير ref في framer-motion
- إضافة `layout` prop أو استخدام `motion.div` بدل `motion.button` لتجنب تحذير ref.

#### 5. إصلاح `useSavedMosqueTimes` لتطبيق فرق الدقائق
- قراءة `SAVED_DIFFS_PREFIX` من localStorage وتطبيق `applyTimeDiff` على الأوقات قبل عرضها.

#### 6. تحسين تجربة التحميل
- إضافة cache يومي لنتائج `fetch-mosque-times` في `MosquePrayerTimes.tsx` لتجنب استدعاء الـ API عند كل دخول للصفحة.

### الملفات المتأثرة
- `supabase/functions/fetch-mosque-times/index.ts`
- `supabase/functions/search-mosques/index.ts`
- `src/pages/MosquePrayerTimes.tsx`
- `src/hooks/useSavedMosqueTimes.tsx`

