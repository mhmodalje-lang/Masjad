# المؤذن العالمي - PRD

## Original Problem Statement
Islamic prayer and lifestyle app with social features, real-time prayer times, Quran, and community platform. The app should support real user-generated content, categories, interactions (likes/comments/follows), and be production-ready.

## Tech Stack
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Shadcn/ui, Framer Motion
- **Backend:** FastAPI, Python, MongoDB (motor)
- **Auth:** Custom JWT (email/password) + Google Sign-In (Firebase)
- **AI:** Google Gemini via emergentintegrations
- **State:** React Context (UnifiedPrayer, Auth, Theme)

## Architecture
```
Bottom Nav: الرئيسية | الصلاة | صُحبة | الرسائل | المزيد

Backend APIs:
  /api/auth/*          - JWT auth (login, register, google, me)
  /api/sohba/posts     - CRUD posts with categories  
  /api/sohba/posts/*/like    - Toggle like
  /api/sohba/posts/*/save    - Toggle save
  /api/sohba/posts/*/comments - CRUD comments
  /api/sohba/follow/*  - Toggle follow
  /api/sohba/my-stats  - User statistics
  /api/sohba/pages     - User-created pages
  /api/sohba/categories - 10 Islamic categories
  /api/prayer-times    - Aladhan API
  /api/admin/*         - Admin dashboard
  
MongoDB Collections: users, posts, likes, saves, comments, follows, pages
```

## Implemented Features

### Core (P0)
- [x] MosqueService - instant prayer sync across all pages
- [x] PermissionManager - native-like pre-request UI
- [x] ThemeProvider - auto sunrise/sunset switching
- [x] Auth system (JWT email/password + Google)
- [x] Admin Dashboard (6 tabs)
- [x] Prayer times from Aladhan API

### Social Platform - صُحبة (REAL)
- [x] 10 categories (عام, القرآن, الحديث, رمضان, الدعاء, قصص, الحج, السفر الحلال, الأسرة, الشباب)
- [x] Create/delete posts with category selection
- [x] Like/unlike posts (persisted in MongoDB)
- [x] Save/unsave posts (persisted in MongoDB)
- [x] Comment system (create + view)
- [x] Follow/unfollow users
- [x] User profile stats (posts, followers, following)

### Pages & Navigation
- [x] 5-tab bottom nav (الرئيسية, الصلاة, صُحبة, الرسائل, المزيد)
- [x] More page with profile, 8 tools grid, settings, athan selector
- [x] Messages page with notification tabs
- [x] Home page with prayer times, hadith, Quran player

### Islamic Tools
- [x] Quran reader + player
- [x] Qibla compass
- [x] Tasbeeh counter
- [x] Duas collection
- [x] Ruqyah
- [x] Zakat calculator
- [x] Prayer tracker
- [x] Ramadan features (calendar, challenge, cards)

## Backlog

### P0 - Next
- [ ] Image/video upload for posts (cloud storage)
- [ ] Real-time notifications (WebSocket or push)
- [ ] User search in صُحبة

### P1 - High
- [ ] Rewards & daily tasks system (gold currency, login streak)
- [ ] Digital store (gifts, frames, cards)
- [ ] Stripe payment for gold
- [ ] Membership/subscription (ad-free)

### P2 - Medium
- [ ] Enhanced Qibla (compass + distance)
- [ ] Enhanced Tasbeeh (rounds)
- [ ] Ad-watching for rewards
- [ ] Multi-language (AR, DE, EN)

### P3 - Future
- [ ] Capacitor for native apps
- [ ] Full-screen athan notifications
- [ ] Offline mode
