# دليل نشر التطبيق - أذان وحكاية
# App Store Deployment Guide

## ✅ الملفات الجاهزة (Ready Files)

### الويب (Web)
- ✅ `public/manifest.json` - PWA manifest كامل
- ✅ `public/app-ads.txt` - ملف التحقق من الإعلانات (يحتاج تحديث Publisher ID)
- ✅ `public/robots.txt` - لمحركات البحث
- ✅ `public/sitemap.xml` - خريطة الموقع
- ✅ `index.html` - SEO meta tags, Open Graph, Twitter Cards, JSON-LD
- ✅ `public/sw-custom.js` - Service Worker للعمل offline
- ✅ Privacy Policy صفحة (`/privacy`)
- ✅ Terms of Service صفحة (`/terms`)

### أندرويد (Android - Google Play Store)
- ✅ `capacitor.config.ts` - App ID: `com.azanwahikaya.app`

#### خطوات النشر على Google Play:
1. بناء المشروع: `yarn build`
2. مزامنة Capacitor: `npx cap sync android`
3. فتح في Android Studio: `npx cap open android`
4. في `android/app/src/main/AndroidManifest.xml` أضف:
```xml
<meta-data
    android:name="com.google.android.gms.ads.APPLICATION_ID"
    android:value="ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY"/>
```
5. في `android/app/build.gradle` أضف:
```gradle
implementation 'com.google.android.gms:play-services-ads:23.0.0'
implementation 'com.google.firebase:firebase-analytics'
```
6. بناء APK/AAB: Build > Generate Signed Bundle
7. رفع على Google Play Console

### آيفون (iOS - Apple App Store)
- ✅ `capacitor.config.ts` - iOS config جاهز

#### خطوات النشر على App Store:
1. بناء المشروع: `yarn build`
2. مزامنة Capacitor: `npx cap sync ios`
3. فتح في Xcode: `npx cap open ios`
4. في `Podfile` أضف:
```ruby
pod 'Google-Mobile-Ads-SDK'
```
5. في `Info.plist` أضف:
```xml
<key>GADApplicationIdentifier</key>
<string>ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY</string>
<key>SKAdNetworkItems</key>
<array>
  <dict>
    <key>SKAdNetworkIdentifier</key>
    <string>cstr6suwn9.skadnetwork</string>
  </dict>
</array>
```
6. Archive و Upload في Xcode
7. رفع على App Store Connect

## 🔧 إعدادات مطلوبة (Required Configuration)

### 1. معرفات الإعلانات (Ad IDs)
- **AdMob App ID**: يُضاف في لوحة التحكم > الإعدادات
- **AdSense Publisher ID**: يُضاف في لوحة التحكم > الإعدادات
- **app-ads.txt**: تحديث `public/app-ads.txt` بمعرف الناشر

### 2. Firebase
- ✅ Analytics مُفعّل (تتبع تلقائي للصفحات)
- ✅ Authentication (Google Sign-In)
- ✅ Push Notifications (VAPID keys)

### 3. GDPR Consent
- ✅ نافذة موافقة تلقائية للمستخدمين
- ✅ قابلة للتحكم من لوحة الأدمن

### 4. لوحة التحكم (Admin Dashboard)
- ✅ تفعيل/تعطيل الإعلانات
- ✅ كتم صوت الفيديو
- ✅ تفعيل/تعطيل GDPR
- ✅ تحكم بأنواع الإعلانات (بانر، بين الصفحات، مكافآت)
- ✅ إحصائيات التحليلات

## 📱 الأيقونات المطلوبة للمتاجر

### Google Play
- 512x512 (High-res icon) ✅ `/public/pwa-icon-512.png`
- Feature graphic: 1024x500
- Screenshots: حد أدنى 2، أقصى 8

### App Store
- 1024x1024 (App Store icon)
- Screenshots لكل حجم شاشة (iPhone, iPad)

## 🔐 الأمان
- ✅ JWT Authentication
- ✅ CORS configured
- ✅ HTTPS enforced
- ✅ GDPR compliant
- ✅ Privacy Policy
- ✅ Terms of Service
