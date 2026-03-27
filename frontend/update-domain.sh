#!/bin/bash
# ══════════════════════════════════════════════════════════════
# 🌐 تحديث دومين الإنتاج - Update Production Domain
# ══════════════════════════════════════════════════════════════
#
# استخدم هذا السكربت لتحديث رابط الباكند عندما يكون لديك دومين جديد
# Usage: ./update-domain.sh https://api.azanwahikaya.com
#
# ══════════════════════════════════════════════════════════════

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}❌ يرجى إدخال الدومين الجديد${NC}"
    echo ""
    echo "الاستخدام:"
    echo "  ./update-domain.sh https://api.azanwahikaya.com"
    echo ""
    echo "أمثلة:"
    echo "  ./update-domain.sh https://api.azanwahikaya.com"
    echo "  ./update-domain.sh https://backend.myapp.com"
    exit 1
fi

NEW_URL="$1"
ENV_FILE="$(dirname "$0")/.env"

echo -e "${YELLOW}🔄 تحديث رابط الباكند...${NC}"
echo -e "   الرابط الجديد: ${GREEN}${NEW_URL}${NC}"

# Update .env file
if [ -f "$ENV_FILE" ]; then
    # Replace existing REACT_APP_BACKEND_URL
    sed -i "s|^REACT_APP_BACKEND_URL=.*|REACT_APP_BACKEND_URL=${NEW_URL}|" "$ENV_FILE"
    echo -e "${GREEN}✅ تم تحديث .env${NC}"
else
    echo "REACT_APP_BACKEND_URL=${NEW_URL}" >> "$ENV_FILE"
    echo -e "${GREEN}✅ تم إنشاء .env${NC}"
fi

echo ""
echo -e "${YELLOW}📋 الخطوات التالية:${NC}"
echo -e "  1. أعد بناء المشروع: ${GREEN}yarn build${NC}"
echo -e "  2. زامن مع Android: ${GREEN}npx cap sync android${NC}"
echo -e "  3. زامن مع iOS: ${GREEN}npx cap sync ios${NC}"
echo ""
echo -e "${GREEN}✅ تم تحديث الدومين بنجاح!${NC}"
