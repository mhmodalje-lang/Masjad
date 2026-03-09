

# خطة: إصلاح الإشعارات + تحسين شاشة الأذان

## المشكلات
1. **الإشعارات لا تعمل في الخلفية** — النظام الحالي يستخدم `setInterval` في الصفحة الرئيسية، فعندما يُغلق التطبيق يتوقف المؤقت
2. **"ليلة القدر" تظهر خطأ في شاشة الأذان** — نظام المناسبات يكتشف التاريخ الهجري الحالي (رمضان) ويعرض المناسبة، لكن قد يكون التاريخ غير دقيق
3. **تحسين شاشة الأذان** — تجميل الواجهة

## الحل

### الجزء 1: إشعارات تعمل في الخلفية (Push Notifications)

النظام الحالي يعتمد على JavaScript timer داخل الصفحة — هذا يتوقف فور إغلاق التطبيق.

**الحل الصحيح**: استخدام Web Push API مع backend:

1. **إنشاء جدول `push_subscriptions`** في قاعدة البيانات لتخزين اشتراكات Push لكل مستخدم مع إحداثيات موقعه وطريقة الحساب

2. **إنشاء edge function `send-prayer-push`** تقوم بـ:
   - جلب جميع المشتركين من الجدول
   - حساب مواقيت الصلاة لكل مستخدم حسب موقعه باستخدام Aladhan API
   - إرسال Web Push notification عند وقت كل صلاة

3. **جدولة cron job** كل دقيقة لاستدعاء هذه الـ function

4. **تعديل `src/pages/NotificationSettings.tsx`** و `src/pages/Index.tsx`**:
   - عند تفعيل الإشعارات → تسجيل Push subscription + حفظها في قاعدة البيانات مع الموقع
   - طلب إذن الإشعارات + إنشاء VAPID keys

5. **إنشاء VAPID keys** وحفظها كـ secrets (`VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`)

6. **تعديل `public/sw-custom.js`** لاستقبال push events وعرض الإشعار

### الجزء 2: إصلاح مشكلة "ليلة القدر"

- مراجعة `getCurrentOccasion()` — المشكلة أن "ليالي القدر" (أيام 21-30 رمضان) تظهر بدل "رمضان" حتى لو اليوم ليس في هذا النطاق
- إضافة تحقق أدق من التاريخ الهجري الحالي
- التأكد من أن `hijriDay` و `hijriMonthNumber` القادمين من API صحيحين

### الجزء 3: تحسين شاشة الأذان

- إضافة اسم المسجد/المدينة في شاشة الأذان
- إضافة تأثيرات بصرية أجمل (نجوم متلألئة، هلال متحرك)
- ترجمة نصوص الشاشة بـ `t()` حسب لغة المستخدم
- تحسين زر الإغلاق ليكون أوضح

## الملفات المتأثرة
1. **`public/sw-custom.js`** — إضافة `push` event listener
2. **`src/lib/prayerNotifications.ts`** — إضافة Push subscription logic
3. **`src/pages/NotificationSettings.tsx`** — تسجيل Push subscription عند التفعيل
4. **`src/pages/Index.tsx`** — تسجيل Push تلقائياً عند تفعيل الإشعارات
5. **`src/components/OccasionAthanAlert.tsx`** — تحسين التصميم + إصلاح النص
6. **`src/components/AthanAlert.tsx`** — تحسين التصميم
7. **`src/data/islamicOccasions.ts`** — مراجعة logic المناسبات
8. **قاعدة البيانات** — جدول `push_subscriptions` جديد
9. **`supabase/functions/send-prayer-push/index.ts`** — edge function جديدة
10. **Secrets** — `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`

