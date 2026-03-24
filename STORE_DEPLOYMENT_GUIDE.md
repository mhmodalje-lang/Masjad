# دليل نشر التطبيق على المتاجر - أذان وحكاية
# Complete Store Deployment Guide - Azan & Hikaya

## ✅ التغييرات المطبقة لقبول المتاجر (Applied Changes for Store Acceptance)

### ❌ أسباب الرفض السابق (Previous Rejection Reasons)
- التطبيق كان يبدو كموقع ويب مغلف (Web Wrapper)
- عدم وجود ميزات أصلية (Native Features)

### ✅ الحلول المطبقة (Applied Solutions)

#### 1. تجربة أصلية (Native Experience)
- ✅ **Page Transitions**: انتقالات بين الصفحات مثل التطبيقات الأصلية (fade animations)
- ✅ **Pull to Refresh**: سحب لتحديث المحتوى
- ✅ **Haptic Feedback**: اهتزاز عند الضغط على الأزرار (via @capacitor/haptics)
- ✅ **Native Back Button**: التعامل مع زر الرجوع في أندرويد (double-tap to exit)
- ✅ **No Overscroll Bounce**: منع الارتداد عند التمرير (يُظهر أنه موقع ويب)
- ✅ **No Scrollbars**: إخفاء شريط التمرير
- ✅ **No Text Selection on UI**: منع تحديد النص على العناصر التفاعلية
- ✅ **No Tap Highlight**: إزالة تأثير الضغط الأزرق
- ✅ **No Context Menu**: منع القائمة المنبثقة عند الضغط المطول
- ✅ **Keyboard Handling**: التعامل مع لوحة المفاتيح بشكل أصلي
- ✅ **Status Bar Integration**: تكامل مع شريط الحالة
- ✅ **Safe Area Support**: دعم المنطقة الآمنة للأجهزة ذات النوتش

#### 2. Capacitor Native Plugins
- ✅ `@capacitor/haptics` - Haptic feedback
- ✅ `@capacitor/share` - Native share sheet
- ✅ `@capacitor/keyboard` - Keyboard handling
- ✅ `@capacitor/network` - Network status
- ✅ `@capacitor/preferences` - Native storage
- ✅ `@capacitor/geolocation` - GPS location
- ✅ `@capacitor/local-notifications` - Prayer time notifications
- ✅ `@capacitor/app` - App lifecycle, back button
- ✅ `@capacitor/status-bar` - Status bar control
- ✅ `@capacitor/splash-screen` - Native splash screen
- ✅ `@capacitor/browser` - In-app browser
- ✅ `@capacitor/device` - Device info

#### 3. إخفاء عناصر الويب في وضع التطبيق (Web Elements Hidden in Native Mode)
- ✅ Install Banner — مخفي
- ✅ PWA Update Prompt — مخفي
- ✅ Cookie Consent — مخفي (ليس مطلوب في التطبيقات الأصلية)
- ✅ Service Worker — لا يُسجل في الوضع الأصلي

#### 4. الامتثال للسياسات (Policy Compliance)
- ✅ **GDPR** — نافذة موافقة تلقائية + إدارة من لوحة الأدمن
- ✅ **Age Gate** — التحقق من العمر (COPPA + GDPR)
- ✅ **Privacy Policy** — صفحة سياسة الخصوصية `/privacy`
- ✅ **Terms of Service** — شروط الاستخدام `/terms`
- ✅ **Data Deletion** — صفحة حذف البيانات `/delete-data`
- ✅ **Content Policy** — سياسة المحتوى `/content-policy`
- ✅ **App Tracking Transparency** — iOS 14.5+ ATT compliance
- ✅ **Rate App Prompt** — طلب تقييم (بعد 5 جلسات و 3 أيام)

---

## 📱 خطوات النشر على Google Play Store

### المتطلبات:
1. حساب Google Play Developer ($25 رسم التسجيل لمرة واحدة)
2. Android Studio مثبت
3. Java/JDK 17+
4. Node.js 18+

### الخطوات:
```bash
# 1. بناء المشروع
cd frontend
yarn build

# 2. مزامنة Capacitor مع Android
npx cap sync android

# 3. فتح المشروع في Android Studio
npx cap open android
```

### في Android Studio:
4. **AndroidManifest.xml** — أضف الأذونات:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.VIBRATE" />
<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

<application
    android:allowBackup="true"
    android:hardwareAccelerated="true"
    android:usesCleartextTraffic="false">

    <!-- AdMob App ID (replace with your actual ID) -->
    <meta-data
        android:name="com.google.android.gms.ads.APPLICATION_ID"
        android:value="ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY"/>
</application>
```

5. **app/build.gradle** — إضافة التبعيات:
```gradle
dependencies {
    implementation 'com.google.android.gms:play-services-ads:23.0.0'
    implementation 'com.google.android.gms:play-services-location:21.0.1'
}
```

6. **إنشاء Signed APK/AAB**:
   - Build → Generate Signed Bundle / APK
   - اختر Android App Bundle (AAB) — مطلوب من Google
   - أنشئ Keystore جديد أو استخدم واحد موجود

7. **رفع على Google Play Console**:
   - الذهاب إلى https://play.google.com/console
   - إنشاء تطبيق جديد
   - رفع AAB في Production
   - ملء معلومات المتجر (الوصف، Screenshots، إلخ)

### معلومات المتجر المقترحة:
- **App Name**: أذان وحكاية - Azan & Hikaya
- **Category**: Lifestyle
- **Content Rating**: Everyone
- **Privacy Policy URL**: https://your-domain.com/privacy
- **Target Age**: 13+

---

## 🍎 خطوات النشر على Apple App Store

### المتطلبات:
1. Apple Developer Account ($99/سنة)
2. Mac مع Xcode مثبت
3. Apple Developer certificates
4. Node.js 18+

### الخطوات:
```bash
# 1. بناء المشروع
cd frontend
yarn build

# 2. إضافة iOS platform (إذا لم تكن موجودة)
npx cap add ios

# 3. مزامنة Capacitor مع iOS
npx cap sync ios

# 4. فتح المشروع في Xcode
npx cap open ios
```

### في Xcode:
5. **Info.plist** — أضف الأذونات:
```xml
<!-- Location -->
<key>NSLocationWhenInUseUsageDescription</key>
<string>نحتاج موقعك لتحديد اتجاه القبلة ومواقيت الصلاة</string>
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>نحتاج موقعك لإشعارات مواقيت الصلاة</string>

<!-- Camera -->
<key>NSCameraUsageDescription</key>
<string>لتصوير المنشورات والصور الشخصية</string>

<!-- Photo Library -->
<key>NSPhotoLibraryUsageDescription</key>
<string>لاختيار الصور للمنشورات</string>

<!-- Notifications -->
<key>NSUserNotificationsUsageDescription</key>
<string>لإشعارات مواقيت الصلاة والتذكيرات</string>

<!-- App Tracking Transparency -->
<key>NSUserTrackingUsageDescription</key>
<string>نستخدم بياناتك لتقديم إعلانات مخصصة وتحسين تجربتك</string>

<!-- AdMob -->
<key>GADApplicationIdentifier</key>
<string>ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY</string>

<!-- SKAdNetwork -->
<key>SKAdNetworkItems</key>
<array>
    <dict>
        <key>SKAdNetworkIdentifier</key>
        <string>cstr6suwn9.skadnetwork</string>
    </dict>
</array>

<!-- Background Modes -->
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
    <string>fetch</string>
    <string>remote-notification</string>
</array>
```

6. **Signing & Capabilities**:
   - اختر Team (حسابك Apple Developer)
   - فعّل Push Notifications
   - فعّل Background Modes (Audio, Fetch, Remote Notifications)
   - فعّل Associated Domains (إذا تريد Deep Linking)

7. **Archive & Upload**:
   - Product → Archive
   - Distribute App → App Store Connect
   - Upload

8. **App Store Connect**:
   - الذهاب إلى https://appstoreconnect.apple.com
   - إنشاء تطبيق جديد
   - ملء المعلومات
   - إرسال للمراجعة

---

## 🔐 الامتثال للسياسات (Policy Compliance)

### GDPR (European Policy)
- ✅ Cookie Consent popup
- ✅ GDPR Ad Consent
- ✅ Data deletion page (/delete-data)
- ✅ Privacy Policy page (/privacy)
- ✅ Right to access data
- ✅ Right to delete data

### COPPA (Children's Protection)
- ✅ Age Gate verification
- ✅ Parental consent for 13-16
- ✅ Kids-only mode for under 13

### App Tracking Transparency (iOS)
- ✅ ATT prompt before any tracking
- ✅ Respects user choice

### Content Policy
- ✅ Content moderation system
- ✅ Report system for inappropriate content
- ✅ Content Policy page (/content-policy)

---

## 📋 ملاحظات مهمة

1. **قبل الإرسال للمراجعة**:
   - تأكد من أن جميع الروابط تعمل (Privacy, Terms, Delete Data)
   - تأكد من أن التطبيق يعمل بدون إنترنت (offline mode)
   - تأكد من أن جميع الأذونات لها وصف واضح
   - اختبر على أجهزة حقيقية (ليس محاكي فقط)

2. **لتجنب الرفض كـ "Web Wrapper"**:
   - التطبيق يستخدم ميزات أصلية (Haptics, Share, Notifications, GPS)
   - لا يوجد شريط تمرير (scrollbar) ظاهر
   - لا يوجد ارتداد عند التمرير (overscroll bounce)
   - الانتقالات بين الصفحات سلسة ومتحركة
   - لوحة المفاتيح تتعامل بشكل أصلي
   - زر الرجوع يعمل بشكل أصلي في أندرويد

3. **Screenshots المطلوبة**:
   - Google Play: حد أدنى 2، أقصى 8 (حجم 1080x1920)
   - App Store: حجم لكل نوع شاشة (iPhone 6.7", 6.5", 5.5", iPad)
