#!/bin/bash
# ══════════════════════════════════════════════════════════════
# 🕌 أذان وحكاية - Azan wa Hikaya
# سكربت بناء تطبيق Android (APK/AAB)
# ══════════════════════════════════════════════════════════════

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🕌 أذان وحكاية - بناء تطبيق Android${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════${NC}"

# Check prerequisites
echo -e "\n${YELLOW}📋 التحقق من المتطلبات...${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js غير مثبت. يرجى تثبيت Node.js 18+${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js: $(node --version)${NC}"

# Check yarn
if ! command -v yarn &> /dev/null; then
    echo -e "${RED}❌ yarn غير مثبت. يرجى تثبيت yarn${NC}"
    exit 1
fi
echo -e "${GREEN}✅ yarn: $(yarn --version)${NC}"

# Check if Android Studio / SDK is available
if [ -z "$ANDROID_HOME" ] && [ -z "$ANDROID_SDK_ROOT" ]; then
    echo -e "${YELLOW}⚠️  ANDROID_HOME غير محدد. ستحتاج Android Studio لبناء APK.${NC}"
    echo -e "${YELLOW}   يمكنك تحميله من: https://developer.android.com/studio${NC}"
fi

# Step 1: Install dependencies
echo -e "\n${YELLOW}📦 الخطوة 1: تثبيت التبعيات...${NC}"
cd "$(dirname "$0")"
yarn install --frozen-lockfile 2>/dev/null || yarn install
echo -e "${GREEN}✅ تم تثبيت التبعيات${NC}"

# Step 2: Build the web app
echo -e "\n${YELLOW}🔨 الخطوة 2: بناء تطبيق الويب...${NC}"
yarn build
echo -e "${GREEN}✅ تم بناء تطبيق الويب بنجاح${NC}"

# Step 3: Sync with Capacitor
echo -e "\n${YELLOW}🔄 الخطوة 3: مزامنة مع Capacitor...${NC}"
npx cap sync android
echo -e "${GREEN}✅ تمت المزامنة مع Android${NC}"

# Step 4: Check if we should open Android Studio or build directly
echo -e "\n${BLUE}══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ المشروع جاهز!${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}الخطوات التالية:${NC}"
echo ""
echo -e "  ${BLUE}الخيار 1: فتح في Android Studio (مُوصى به)${NC}"
echo -e "    npx cap open android"
echo -e "    ثم: Build → Generate Signed Bundle / APK"
echo ""
echo -e "  ${BLUE}الخيار 2: بناء APK مباشرة من سطر الأوامر${NC}"
echo -e "    cd android"
echo -e "    ./gradlew assembleDebug    # لبناء APK تجريبي"
echo -e "    ./gradlew assembleRelease  # لبناء APK إنتاجي"
echo -e "    ./gradlew bundleRelease    # لبناء AAB (مطلوب لـ Google Play)"
echo ""
echo -e "  ${BLUE}مكان ملف APK بعد البناء:${NC}"
echo -e "    android/app/build/outputs/apk/debug/app-debug.apk"
echo -e "    android/app/build/outputs/apk/release/app-release.apk"
echo -e "    android/app/build/outputs/bundle/release/app-release.aab"
echo ""
echo -e "${YELLOW}📝 ملاحظة: لبناء AAB للنشر على Google Play:${NC}"
echo -e "   1. أنشئ Keystore: keytool -genkey -v -keystore azanhikaya.keystore -alias azanhikaya -keyalg RSA -keysize 2048 -validity 10000"
echo -e "   2. عدّل android/app/build.gradle وأضف إعدادات التوقيع"
echo -e "   3. ابنِ: cd android && ./gradlew bundleRelease"
echo ""
