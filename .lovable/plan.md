

# إضافة صور بانر لكل صفحة

## التعديل

### 1. `src/components/PageHeader.tsx`
إضافة prop اختياري `image?: string`. عند وجوده:
- عرض `<img>` بـ `absolute inset-0 object-cover w-full h-full`
- overlay: `bg-gradient-to-b from-black/60 via-black/30 to-background`
- إزالة `gradient-islamic` و `islamic-pattern` واستبدالها بالصورة
- عند عدم وجود صورة: يبقى السلوك الحالي كما هو

### 2. إضافة صور Unsplash لكل صفحة

| الصفحة | `image` prop |
|--------|-------------|
| القرآن (`Quran.tsx`) | مصحف مفتوح |
| القصص (`Stories.tsx`) | مسجد تاريخي / كتب |
| الأدعية (`Duas.tsx`) | يدين مرفوعتين بالدعاء |
| المسبحة (`Tasbeeh.tsx`) | سبحة صلاة |
| مواقيت الصلاة (`PrayerTimes.tsx`) | مسجد عند الغروب |
| القبلة (`Qibla.tsx`) | الكعبة المشرفة |
| حاسبة الزكاة (`ZakatCalculator.tsx`) | عملات / صدقة |
| متابعة الصلاة (`PrayerTracker.tsx`) | مصلّي في مسجد |
| حسابي (`Account.tsx`) | زخرفة إسلامية |

### 3. الملفات المعدّلة
- `src/components/PageHeader.tsx` — إضافة دعم `image`
- 9 صفحات — إضافة `image="https://images.unsplash.com/..."` فقط

تغيير بصري فقط، لا تعديل على أي منطق.

