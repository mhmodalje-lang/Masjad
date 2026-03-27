# 🕌 دليل النشر الشامل - أذان وحكاية
# Complete Deployment Guide - Azan & Hikaya

---

## 📋 الحالة الحالية (Current Status)

| العنصر | الحالة | ملاحظات |
|--------|--------|---------|
| manifest.json | ✅ جاهز | جميع الأيقونات (48-512px) |
| Service Worker | ✅ جاهز | Offline + Prayer Notifications + API Caching |
| Capacitor Config | ✅ جاهز | Android + iOS settings |
| Android Project | ✅ جاهز | Icons, Splash, Permissions, Build Config |
| iOS Project | ⏳ يحتاج Mac | Run `npx cap add ios` on Mac |
| HTTPS | ✅ | مُفعل عبر Kubernetes |
| Native Features | ✅ 12 إضافة | Haptics, Share, GPS, Notifications... |

---

## 📱 أيقونات PWA (جميعها جاهزة)

| الحجم | الملف | الاستخدام |
|-------|--------|-----------|
| 48x48 | pwa-icon-48.png | Android notification |
| 72x72 | pwa-icon-72.png | Android homescreen |
| 96x96 | pwa-icon-96.png | Android splash |
| 128x128 | pwa-icon-128.png | Chrome Web Store |
| 144x144 | pwa-icon-144.png | Windows tiles |
| 152x152 | pwa-icon-152.png | iPad |
| 167x167 | pwa-icon-167.png | iPad Pro |
| 180x180 | pwa-icon-180.png | iPhone (apple-touch-icon) |
| 192x192 | pwa-icon-192.png | Android PWA standard |
| 384x384 | pwa-icon-384.png | Android splash large |
| 512x512 | pwa-icon-512.png | PWA install & splash |
| 512x512 | pwa-icon-maskable.png | Android adaptive icon |

---

## 🤖 بناء تطبيق Android (APK / AAB)

### المتطلبات:
1. **Android Studio** (تحميل: https://developer.android.com/studio)
2. **JDK 17+** (يأتي مع Android Studio)
3. **Node.js 18+** و **yarn**

### الخطوات:

#### الطريقة 1: استخدام السكربت الآلي (الأسهل)
```bash
cd frontend
chmod +x build-android.sh
./build-android.sh
```

#### الطريقة 2: يدوياً

```bash
# 1. تثبيت التبعيات
cd frontend
yarn install

# 2. بناء تطبيق الويب
yarn build

# 3. مزامنة مع Android
npx cap sync android

# 4. فتح في Android Studio
npx cap open android
```

#### في Android Studio:

**لبناء APK تجريبي (للاختبار):**
- Build → Build Bundle(s) / APK(s) → Build APK(s)
- الملف: `android/app/build/outputs/apk/debug/app-debug.apk`

**لبناء AAB للنشر على Google Play:**

1. **أنشئ Keystore (مرة واحدة فقط):**
```bash
keytool -genkey -v -keystore azanhikaya.keystore -alias azanhikaya -keyalg RSA -keysize 2048 -validity 10000
```

2. **عدّل `android/app/build.gradle`:**
   - فعّل قسم `signingConfigs` وأدخل بيانات Keystore

3. **ابنِ AAB:**
   - Build → Generate Signed Bundle / APK
   - اختر Android App Bundle
   - اختر Keystore
   - الملف: `android/app/build/outputs/bundle/release/app-release.aab`

#### من سطر الأوامر:
```bash
cd android

# APK تجريبي
./gradlew assembleDebug

# APK إنتاجي
./gradlew assembleRelease

# AAB لـ Google Play (مطلوب)
./gradlew bundleRelease
```

---

## 🍎 بناء تطبيق iOS

### المتطلبات:
1. **Mac** مع **Xcode 15+**
2. **حساب Apple Developer** ($99/سنة)
3. **Node.js 18+** و **yarn**
4. **CocoaPods**: `sudo gem install cocoapods`

### الخطوات:

#### الطريقة 1: استخدام السكربت الآلي
```bash
cd frontend
chmod +x build-ios.sh
./build-ios.sh
```

#### الطريقة 2: يدوياً

```bash
# 1. تثبيت التبعيات
cd frontend
yarn install

# 2. بناء تطبيق الويب
yarn build

# 3. إضافة iOS (مرة واحدة)
npx cap add ios

# 4. مزامنة
npx cap sync ios

# 5. فتح Xcode
npx cap open ios
```

#### في Xcode:

1. **Signing & Capabilities:**
   - اختر Team (حسابك Apple Developer)
   - Bundle Identifier: `com.azanwahikaya.app`

2. **أضف Capabilities:**
   - Push Notifications
   - Background Modes (Audio, Fetch, Remote Notifications)
   - Associated Domains (اختياري للـ Deep Linking)

3. **Info.plist - أذونات:**
```xml
<!-- الموقع -->
<key>NSLocationWhenInUseUsageDescription</key>
<string>نحتاج موقعك لتحديد اتجاه القبلة ومواقيت الصلاة</string>
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>نحتاج موقعك لإشعارات مواقيت الصلاة</string>

<!-- الإشعارات -->
<key>NSUserNotificationsUsageDescription</key>
<string>لإشعارات مواقيت الصلاة والتذكيرات اليومية</string>

<!-- تتبع الإعلانات (iOS 14.5+) -->
<key>NSUserTrackingUsageDescription</key>
<string>نستخدم بياناتك لتقديم إعلانات مناسبة وتحسين تجربتك</string>
```

4. **Archive & Upload:**
   - Product → Archive
   - Distribute App → App Store Connect
   - Upload

---

## 🏪 النشر على Google Play Store

### 1. إنشاء حساب مطور ($25 مرة واحدة)
- اذهب إلى: https://play.google.com/console
- أنشئ حساب جديد
- ادفع رسم التسجيل

### 2. إنشاء التطبيق
- اضغط "Create app"
- أدخل المعلومات:

| الحقل | القيمة |
|-------|--------|
| App name | أذان وحكاية - Azan & Hikaya |
| Default language | Arabic (ar) |
| App or game | App |
| Free or paid | Free |

### 3. ملء بيانات المتجر (Store Listing)

**الوصف القصير (80 حرف):**
```
مواقيت الصلاة، القرآن، القبلة، الأذكار، حكايات إسلامية - تطبيق شامل ومجاني
```

**الوصف الكامل (4000 حرف):**
```
🕌 أذان وحكاية - رفيقك الروحي اليومي

تطبيق إسلامي شامل ومجاني يجمع كل ما يحتاجه المسلم في مكان واحد:

⏰ مواقيت الصلاة الدقيقة
• تحديد تلقائي للموقع
• إشعارات الأذان لكل صلاة
• دعم جميع مدن العالم
• تنبيه قبل 10 دقائق من كل صلاة

📖 القرآن الكريم
• قراءة جميع السور
• تفسير الآيات
• آية اليوم

🧭 اتجاه القبلة
• بوصلة دقيقة باستخدام GPS
• تعمل في أي مكان بالعالم

🤲 الأدعية والأذكار
• أذكار الصباح والمساء
• أدعية متنوعة
• الرقية الشرعية

📿 المسبحة الإلكترونية
• عداد التسبيح
• أهداف يومية

💰 حاسبة الزكاة
• حساب زكاة المال
• دعم عملات متعددة

📚 حكايات إسلامية
• قصص الأنبياء والصحابة
• حكايات للأطفال
• محتوى بلغات متعددة

🕌 المساجد القريبة
• البحث عن أقرب مسجد
• أوقات صلاة المساجد

🌙 ميزات إضافية
• صُحبة - منصة اجتماعية إسلامية
• مساعد ذكي للأسئلة الدينية
• متجر بركة - منتجات إسلامية
• منطقة الأطفال - محتوى آمن ومفيد
• تقويم هجري
• دعم RTL كامل
• يعمل بدون إنترنت

🌍 متوفر بـ 10 لغات: العربية، الإنجليزية، الألمانية، الفرنسية، التركية، الروسية، السويدية، الهولندية، اليونانية، النمساوية
```

### 4. Screenshots المطلوبة
- **الحد الأدنى**: 2 صور
- **الموصى**: 6-8 صور
- **الحجم**: 1080x1920 بكسل (phone)
- **المحتوى المقترح**: مواقيت الصلاة، القرآن، القبلة، الأذكار، الحكايات، صُحبة

### 5. إعدادات المتجر

| الإعداد | القيمة |
|---------|--------|
| Category | Lifestyle |
| Content Rating | IARC - Everyone |
| Target Audience | 13+ |
| Privacy Policy | https://YOUR_DOMAIN/privacy |
| Contains Ads | Yes |
| In-App Purchases | Yes |

### 6. رفع AAB
- Production → Create new release
- Upload AAB file
- Submit for review

---

## 🍎 النشر على Apple App Store

### 1. إنشاء حساب مطور ($99/سنة)
- اذهب إلى: https://developer.apple.com
- سجل حساب Apple Developer

### 2. App Store Connect
- اذهب إلى: https://appstoreconnect.apple.com
- أنشئ تطبيق جديد:
  - Bundle ID: `com.azanwahikaya.app`
  - Name: `أذان وحكاية`
  - Primary Language: Arabic

### 3. ملء البيانات
- نفس الوصف أعلاه
- Screenshots لكل حجم شاشة:
  - iPhone 6.7" (1290x2796)
  - iPhone 6.5" (1242x2688)
  - iPhone 5.5" (1242x2208)
  - iPad 12.9" (2048x2732) (إذا يدعم iPad)

### 4. رفع ومراجعة
- Archive من Xcode
- Upload إلى App Store Connect
- Submit for Review
- الانتظار (1-7 أيام عادة)

---

## ⚠️ نصائح لتجنب الرفض

### Google Play:
1. ✅ لا تستخدم أسماء علامات تجارية محمية
2. ✅ أضف وصف خصوصية واضح (Privacy Policy)
3. ✅ تأكد من أن التطبيق لا يتعطل
4. ✅ أضف Content Rating (IARC)
5. ✅ التطبيق يستخدم ميزات أصلية (ليس مجرد WebView)

### Apple App Store:
1. ✅ التطبيق يقدم قيمة فوق الموقع (Native features)
2. ✅ جميع الروابط تعمل
3. ✅ لا يوجد محتوى مخالف
4. ✅ ATT Dialog قبل التتبع
5. ✅ دعم الـ Safe Area (notch)
6. ✅ لا يظهر كـ "Web Wrapper" (الميزات الأصلية مُفعلة)

### الميزات الأصلية المُفعلة (لتجنب رفض "Web Wrapper"):
- ✅ Haptic Feedback (اهتزاز)
- ✅ Native Share Sheet
- ✅ GPS Location
- ✅ Local Notifications (إشعارات الصلاة)
- ✅ Native Back Button (Android)
- ✅ Status Bar Integration
- ✅ Splash Screen
- ✅ Pull to Refresh
- ✅ No Overscroll Bounce
- ✅ Keyboard Handling
- ✅ Page Transitions (animations)

---

## 🔧 تحديث URL الباكند (عند الحاجة)

عندما يكون لديك سيرفر إنتاج:

1. عدّل `/frontend/.env`:
```
REACT_APP_BACKEND_URL=https://api.azanwahikaya.com
```

2. أعد البناء:
```bash
cd frontend
yarn build
npx cap sync android  # أو ios
```

---

## 📝 ملخص الملفات المهمة

| الملف | الغرض |
|-------|--------|
| `frontend/public/manifest.json` | إعدادات PWA |
| `frontend/public/sw-custom.js` | Service Worker |
| `frontend/capacitor.config.ts` | إعدادات Capacitor |
| `frontend/android/app/src/main/AndroidManifest.xml` | أذونات Android |
| `frontend/android/app/build.gradle` | إعدادات البناء |
| `frontend/build-android.sh` | سكربت بناء Android |
| `frontend/build-ios.sh` | سكربت بناء iOS |

---

*آخر تحديث: يوليو 2025*
