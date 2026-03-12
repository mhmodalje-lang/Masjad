# المؤذن العالمي - PRD (Product Requirements Document)

## Original Problem Statement
Build a world-class Islamic prayer and lifestyle app named "المؤذن العالمي" (The Global Muezzin) with social features inspired by "أنا مسلم" app. Full feature set includes prayer times, Quran, community (صُحبة), rewards, store, messaging, profile, and more.

## Tech Stack
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Shadcn/ui, Framer Motion
- **Backend:** FastAPI, Python, MongoDB (motor)
- **Auth:** Custom JWT (email/password) + Google Sign-In (Firebase)
- **AI:** Google Gemini via emergentintegrations
- **State:** React Context (UnifiedPrayer, Auth, Theme)

## Core Architecture
```
/app
├── backend/
│   ├── server.py          # FastAPI main app with all routes
│   ├── .env               # MONGO_URL, DB_NAME, API keys
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx                    # Router + providers
│   │   ├── components/
│   │   │   ├── ThemeProvider.tsx       # Dual theme with auto sunrise/sunset
│   │   │   ├── PermissionManager.tsx  # Native-like permission UI
│   │   │   ├── ThemeToggle.tsx        # Theme cycle button
│   │   │   └── layout/
│   │   │       ├── AppLayout.tsx
│   │   │       └── BottomNav.tsx      # 5-tab navigation
│   │   ├── hooks/
│   │   │   ├── useUnifiedPrayer.tsx   # Prayer times context + MosqueService
│   │   │   └── useAuth.tsx            # Auth context
│   │   ├── lib/
│   │   │   └── MosqueService.ts       # Instant mosque state propagation
│   │   ├── pages/
│   │   │   ├── Index.tsx              # Home page
│   │   │   ├── PrayerTimes.tsx        # Prayer times
│   │   │   ├── Sohba.tsx             # Community/social feed (NEW)
│   │   │   ├── Messages.tsx          # Notifications/messages (NEW)
│   │   │   ├── Profile.tsx           # User profile (NEW)
│   │   │   ├── Auth.tsx              # Login/Register
│   │   │   ├── AdminDashboard.tsx    # Admin panel
│   │   │   └── ... (20+ more pages)
│   │   └── styles/
│   │       └── index.css              # Theme CSS variables
│   └── .env
```

## What's Been Implemented

### Phase 0 (Previous sessions)
- [x] FastAPI/MongoDB backend with JWT auth
- [x] Admin Dashboard (6 tabs: overview, users, ads, notifications, pages, settings)
- [x] Gemini AI integration for daily athkar
- [x] PWA with service worker
- [x] Dual theme (light/dark) with CSS variables
- [x] Full rebranding to "المؤذن العالمي"
- [x] Prayer times from Aladhan API
- [x] Quran, Duas, Tasbeeh, Qibla, Zakat calculator
- [x] Ramadan features (calendar, challenge, cards, book)

### P0 Features (Session 2 - Mar 12, 2026)
- [x] MosqueService.ts - Instant prayer time propagation across all pages
- [x] PermissionManager.tsx - Native-like pre-request UI for Location & Notifications
- [x] ThemeProvider.tsx - Auto sunrise/sunset theme switching
- [x] Auth page improvements - Better error handling, Arabic messages
- [x] Enhanced UnifiedPrayerContext - Integrated with MosqueService

### Phase 1 (Session 2 - Mar 12, 2026)
- [x] New 5-tab bottom navigation: الرئيسية, الصلاة, صُحبة, الرسائل, حسابي
- [x] Profile page with stats, membership card, quick links, theme toggle
- [x] Sohba (صُحبة) community page with social feed, tabs, trending tags
- [x] Messages page with notifications, messages, activity tabs

## MOCKED Features (No Backend Yet)
- Sohba posts/likes/comments/shares (frontend state only)
- Messages/notifications (frontend sample data only)
- Profile stats (hardcoded zeros)
- Rewards/gold system (not started)
- Store (not started)

## Prioritized Backlog

### P0 - Critical (Next)
- [ ] Backend APIs for Sohba (posts CRUD, likes, comments, follows)
- [ ] Backend APIs for Messages (notifications, messaging)
- [ ] Image/video upload for Sohba posts
- [ ] Real-time profile stats from backend

### P1 - High Priority
- [ ] Rewards & daily tasks system (gold currency, login streak, daily missions)
- [ ] Store (digital gifts, frames, cards, backgrounds)
- [ ] Stripe payment integration for gold purchases
- [ ] Membership/subscription system (ad-free + daily gold)

### P2 - Medium Priority
- [ ] Enhanced Ramadan calendar (Laylat al-Qadr countdown, Eid countdown)
- [ ] Interactive Qibla compass (129° display, distance to Makkah)
- [ ] Enhanced Tasbeeh counter with rounds system
- [ ] Ad-watching for gold rewards

### P3 - Future
- [ ] Multi-language support (Arabic, German, English)
- [ ] Advanced settings (night mode, font size)
- [ ] Friend invitation system
- [ ] App rating integration
- [ ] Capacitor for Google Play / App Store
