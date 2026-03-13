# المؤذن العالمي - PRD (Product Requirements Document)

## Original Problem Statement
Build a world-class, commercial-grade Islamic prayer and lifestyle app. The app is a complete ecosystem with social features, monetization, AI assistant, marketplace, and Islamic tools.

## User Personas
- **Muslim Users**: Daily prayer, Quran, Duas, Tasbeeh, Qibla, Islamic tools
- **Content Creators**: Post content on صُحبة, receive gifts and support
- **Vendors**: List Islamic products in the marketplace
- **Advertisers**: Submit video ads for review by admin
- **Admin**: Manage platform, approve ads, set commissions, receive revenue

## Core Architecture
```
/app
├── backend/server.py          # FastAPI - All APIs
├── backend/.env               # MONGO_URL, STRIPE, EMERGENT_LLM_KEY
├── frontend/src/
│   ├── App.tsx                # Router + Providers
│   ├── pages/                 # All pages
│   ├── components/layout/     # TopNav, BottomNav, AppLayout
│   ├── hooks/useAuth.tsx      # Auth context
│   └── index.css              # Theme (Emerald Gold)
```

## Tech Stack
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Shadcn/ui, Framer Motion
- **Backend**: FastAPI, Python, MongoDB (motor), emergentintegrations
- **AI**: GPT-5.2 via Emergent LLM Key
- **Payments**: Stripe via emergentintegrations
- **Auth**: JWT + Emergent Google Auth

## Implemented Features (as of March 2026)

### Phase 1 - Core Islamic Tools ✅
- Prayer Times (Aladhan API)
- Qibla Compass
- Tasbeeh Counter
- Quran Reader
- Duas Collection
- Ruqyah Player
- Zakat Calculator
- Asma Allah Al-Husna (99 names)
- Prayer Tracker

### Phase 2 - Social Platform (صُحبة) ✅
- Post creation with real image/video uploads
- Like, comment system
- Category filtering
- 2-column masonry grid

### Phase 3 - Monetization ✅
- **Virtual Credits System** (like TikTok coins)
  - GPS-based currency detection (30+ countries)
  - 8 credit packages (0.05€ to 1000€)
  - Credits used for AI questions, gifts
- **Islamic Gift Store** (12 Islamic-themed gifts)
  - 50/50 revenue split (admin/creator)
  - Gifts on posts (lion, crescent, kaaba, etc.)
- **Gold/Rewards System**
  - Daily login rewards, streak bonuses
  - Earn by watching ads, tasbeeh, quran
- **Digital Store** (themes, badges, effects, memberships)
- **Stripe Integration** for real payments

### Phase 4 - Commercial Platform ✅
- **AI Religious Assistant** (GPT-5.2)
  - 5 free questions/day, then credits
  - Max 20 questions/day
  - Islamic-only filtering
  - Session-based conversation
- **Ad Manager**
  - Users submit video ads (YouTube/Facebook embed)
  - Admin approval system
  - Users earn credits watching approved ads
- **Vendor Marketplace**
  - GPS-sorted product listings
  - Category filtering
  - Admin-configurable commission rate
- **User Bank Accounts** for receiving earnings

### Phase 5 - Admin Dashboard ✅
- 8 tabs: Overview, Users, Ads, User Ads, Notifications, Pages, Revenue, Settings
- Admin bank account settings
- Marketplace commission control
- User ad approval/rejection
- Revenue tracking

### Phase 6 - UI/UX ✅
- Emerald Gold theme (dark + light)
- Professional bottom nav with centered indicator
- PWA ready
- RTL Arabic layout

## Key API Endpoints
- Auth: `/api/auth/login`, `/api/auth/register`, `/api/auth/google`
- Social: `/api/sohba/posts`, `/api/sohba/posts/{id}/like`
- Gifts: `/api/gifts/list`, `/api/gifts/send`
- Credits: `/api/credits/packages`, `/api/credits/detect-currency`
- AI: `/api/ai/ask`, `/api/ai/history`
- Ads: `/api/ads/submit`, `/api/ads/approved`, `/api/ads/watch/{id}`
- Marketplace: `/api/marketplace/products`
- Store: `/api/store/items`, `/api/store/buy-gold`
- Rewards: `/api/rewards/balance`, `/api/rewards/claim`
- Payments: `/api/payments/checkout`, `/api/payments/packages`
- Admin: `/api/admin/*`

## P0 Remaining
- None critical

## P1 Backlog
- Lottie animations for page transitions
- Enhanced Qibla compass with calibration
- Multi-language support
- Native notifications (Athan on lock screen)
- Capacitor for mobile app deployment

## P2 Future
- Full Stripe webhook processing
- User withdrawal system (credits to bank)
- Advanced analytics dashboard
- Push notification campaigns
- A/B testing for ads
