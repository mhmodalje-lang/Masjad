# المؤذن العالمي - PRD (Product Requirements Document)

## Original Problem Statement
Build a world-class, commercial-grade Islamic prayer and lifestyle app - a complete ecosystem with TikTok-style social features, managed e-commerce marketplace, monetization via virtual credits, AI Islamic assistant, and comprehensive admin dashboard.

## User Personas
- **Muslim Users**: Prayer times, Quran, Duas, Tasbeeh, Qibla, Islamic tools
- **Content Creators**: Post on صُحبة, receive gifts (50/50 revenue), earn credits
- **Vendors**: Register shop, list products (admin-approved), sell with auto-commission
- **Advertisers**: Submit video ads, get approved by admin, earn views
- **Admin**: Full control - bank account, broadcast, vendor approval, ad review, commission rates

## Architecture
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Shadcn/ui, Framer Motion, Lottie-React
- **Backend**: FastAPI, Python, MongoDB (motor), emergentintegrations
- **AI**: GPT-5.2 via Emergent LLM Key (5 free/day, then credits, max 20/day)
- **Payments**: Stripe via emergentintegrations
- **Auth**: JWT + Emergent Google Auth

## All Implemented Features

### Social Platform - صُحبة (TikTok-Style) ✅
- Full-screen vertical scroll feed
- Real image/video uploads (unlimited size via multipart streaming)
- Like, Comment sheets with real-time display
- Gift buttons on every post (12 Islamic gifts)
- User Profile sheets (posts, followers, following stats)
- Category filtering (عام, القرآن, الحديث, رمضان, etc.)
- 50/50 revenue split on gifts (admin/creator)

### Managed E-Commerce Marketplace ✅
- Vendor registration with admin approval
- Products only listed after admin approves vendor
- GPS-based product sorting (nearest first)
- Category filtering
- Admin-configurable commission rate

### Virtual Credits System ✅
- GPS-based currency detection (30+ countries)
- 8 credit packages (0.05€ to 1000€)
- Credits for AI questions, gifts, ad rewards
- Stripe checkout integration

### AI Religious Assistant (GPT-5.2) ✅
- 5 free questions/day, then credits
- Max 20 questions/day, auto-locks
- Islamic-only filtering with system prompt
- Session-based conversation history
- Earn credits by watching ads

### Admin Dashboard (10 Tabs) ✅
1. نظرة عامة (Overview) - Stats, users, ads count
2. البث (Broadcast) - Publish announcements to all users on homepage
3. المستخدمين (Users) - User management
4. الإعلانات (Ads) - Manage banner ads
5. إعلانات القنوات (Channel Ads) - Approve/reject user video ads
6. البائعين (Vendors) - Approve/reject vendor registrations
7. الإشعارات (Notifications) - Push notification scheduling
8. الصفحات (Pages) - Custom pages
9. الإيرادات (Revenue) - Gift revenue tracking, Stripe summary
10. الإعدادات (Settings) - IBAN bank account, maintenance mode, commission rate

### Homepage Announcements ✅
- Admin publishes broadcast → shows immediately on homepage for ALL users
- Dismissible by users
- Types: info, warning, promo

### Islamic Tools (All Functional) ✅
- Prayer Times, Qibla Compass, Tasbeeh Counter, Quran Reader
- Duas Collection, Ruqyah Player, Zakat Calculator
- Prayer Tracker, Asma Allah Al-Husna (99 names)

### Rewards System ✅
- Daily login rewards with streak bonuses
- Gold currency + Virtual credits
- Store with themes, badges, effects, memberships
- Transaction history

### File Uploads ✅
- Multipart streaming (unlimited size)
- Base64 for small files
- Supports images + videos
- Served via /api/uploads/{filename}

### UI/UX ✅
- Islamic Gold + Deep Emerald theme (dark + light)
- Animated backgrounds (CSS + Lottie-ready)
- Bottom nav with centered Spring indicator
- RTL Arabic layout throughout
- PWA ready

## Key API Endpoints
Auth, Social, Gifts, Credits, AI, Ads, Marketplace, Store, Rewards, Payments, Admin, Announcements, Vendors, Bank Accounts, Upload (multipart + base64)

## P1 Backlog
- Full Stripe Connect for real bank transfers
- User withdrawal system (credits → bank)
- Advanced analytics dashboard
- Multi-language support
- Capacitor for mobile app deployment
- Native Athan notifications on lock screen
