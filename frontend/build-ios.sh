#!/bin/bash
# ══════════════════════════════════════════════════════════════
# 🍎 أذان وحكاية - Azan wa Hikaya
# سكربت تجهيز تطبيق iOS
# ══════════════════════════════════════════════════════════════

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🍎 أذان وحكاية - تجهيز تطبيق iOS${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════${NC}"

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ هذا السكربت يعمل فقط على macOS${NC}"
    echo -e "${YELLOW}   تحتاج Mac مع Xcode لبناء تطبيق iOS${NC}"
    exit 1
fi

# Check prerequisites
echo -e "\n${YELLOW}📋 التحقق من المتطلبات...${NC}"

if ! command -v xcodebuild &> /dev/null; then
    echo -e "${RED}❌ Xcode غير مثبت. يرجى تثبيت Xcode من Mac App Store${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Xcode: $(xcodebuild -version | head -1)${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js غير مثبت${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js: $(node --version)${NC}"

if ! command -v yarn &> /dev/null; then
    echo -e "${RED}❌ yarn غير مثبت${NC}"
    exit 1
fi
echo -e "${GREEN}✅ yarn: $(yarn --version)${NC}"

# Step 1: Install dependencies
echo -e "\n${YELLOW}📦 الخطوة 1: تثبيت التبعيات...${NC}"
cd "$(dirname "$0")"
yarn install --frozen-lockfile 2>/dev/null || yarn install
echo -e "${GREEN}✅ تم تثبيت التبعيات${NC}"

# Step 2: Build the web app
echo -e "\n${YELLOW}🔨 الخطوة 2: بناء تطبيق الويب...${NC}"
yarn build
echo -e "${GREEN}✅ تم بناء تطبيق الويب${NC}"

# Step 3: Add iOS platform if not exists
if [ ! -d "ios" ]; then
    echo -e "\n${YELLOW}📱 الخطوة 3: إضافة منصة iOS...${NC}"
    npx cap add ios
    echo -e "${GREEN}✅ تمت إضافة iOS${NC}"
else
    echo -e "\n${GREEN}✅ منصة iOS موجودة بالفعل${NC}"
fi

# Step 4: Sync with Capacitor
echo -e "\n${YELLOW}🔄 الخطوة 4: مزامنة مع Capacitor...${NC}"
npx cap sync ios
echo -e "${GREEN}✅ تمت المزامنة مع iOS${NC}"

# Step 5: Open Xcode
echo -e "\n${BLUE}══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ المشروع جاهز!${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}الخطوات التالية:${NC}"
echo ""
echo -e "  ${BLUE}1. فتح المشروع في Xcode:${NC}"
echo -e "     npx cap open ios"
echo ""
echo -e "  ${BLUE}2. في Xcode:${NC}"
echo -e "     - اختر Team (حساب Apple Developer)"
echo -e "     - فعّل Push Notifications في Capabilities"
echo -e "     - فعّل Background Modes (Audio, Fetch)"
echo -e "     - تأكد من Bundle Identifier: com.azanwahikaya.app"
echo ""
echo -e "  ${BLUE}3. بناء ورفع:${NC}"
echo -e "     - Product → Archive"
echo -e "     - Distribute App → App Store Connect"
echo ""
echo -e "  ${BLUE}4. في App Store Connect:${NC}"
echo -e "     - https://appstoreconnect.apple.com"
echo -e "     - أنشئ تطبيق جديد"
echo -e "     - أرسل للمراجعة"
echo ""
echo -e "${YELLOW}📝 Info.plist - أذونات مطلوبة:${NC}"
echo -e "   NSLocationWhenInUseUsageDescription: نحتاج موقعك لتحديد مواقيت الصلاة واتجاه القبلة"
echo -e "   NSLocationAlwaysUsageDescription: لإشعارات مواقيت الصلاة"
echo -e "   NSUserTrackingUsageDescription: لتحسين تجربتك"
echo ""
