

# خطة إصلاح RTL للصفحات المتبقية

## الملفات والتغييرات

### 1. `src/pages/Duas.tsx`
- Search icon: `left-3` → `end-3`, `pl-9` → `pe-9`

### 2. `src/pages/Quran.tsx`
- Search icon: `left-3` → `end-3`, `pl-9` → `pe-9`

### 3. `src/pages/Stories.tsx`
- Animation direction: `x: -20` → `x: 20` و `x: 20` → `x: -20` (عكس اتجاه الدخول/الخروج)
- Comment input: ترتيب زر الإرسال والحقل (الزر يسار الحقل في RTL)

### 4. `src/pages/AdminDashboard.tsx`
- `ml-2` → `me-2` على أيقونة Plus

### 5. `src/pages/MosquePrayerTimes.tsx`
- `mr-auto` → `ms-auto`
- `pr-6` → `pe-6`
- `pr-4` → `pe-4`

### 6. `src/pages/PrayerTracker.tsx`
- Animation: `x: -20` → `x: 20` (الدخول من اليمين في RTL)

### 7. `src/pages/Install.tsx`
- لا تغييرات مطلوبة (`left-0 right-0` يغطي كل العرض)

### 8. `src/pages/Qibla.tsx`
- لا تغييرات مطلوبة (يستخدم inline styles للبوصلة)

**إجمالي: 6 ملفات تحتاج تعديل بسيط**

