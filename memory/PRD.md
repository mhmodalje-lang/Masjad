# المؤذن العالمي - PRD

## Tech Stack
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Shadcn/ui, Framer Motion
- **Backend:** FastAPI, Python, MongoDB (motor)
- **Auth:** JWT (email/password) + Emergent-managed Google OAuth
- **AI:** Google Gemini via emergentintegrations

## Architecture
```
Bottom Nav: الرئيسية | الصلاة | صُحبة | الرسائل | المزيد

Backend APIs:
  /api/auth/login          - Email/password login
  /api/auth/register       - User registration
  /api/auth/google         - Emergent Google OAuth session exchange
  /api/auth/forgot-password - Password reset request
  /api/auth/me             - Get current user
  /api/sohba/posts         - CRUD posts (2-column masonry grid)
  /api/sohba/posts/*/like  - Toggle like
  /api/sohba/posts/*/save  - Toggle save
  /api/sohba/posts/*/comments - CRUD comments
  /api/sohba/follow/*      - Toggle follow
  /api/sohba/my-stats      - User stats
  /api/sohba/categories    - 10 Islamic categories
  /api/sohba/pages         - User-created pages
  /api/prayer-times        - Aladhan API
  /api/admin/*             - Admin dashboard
```

## Implemented ✅

### Auth
- [x] Email/password login + registration
- [x] Emergent Google OAuth (any Google account)
- [x] Forgot password page
- [x] JWT token-based auth
- [x] Admin route protection

### Social Platform - صُحبة
- [x] 2-column masonry grid layout (like reference app)
- [x] Image + video thumbnails with play icons
- [x] 10 Islamic categories
- [x] Create/delete posts with category
- [x] Like/unlike, save, comment (all MongoDB)
- [x] Post detail modal with comments
- [x] Follow/unfollow system
- [x] Create post FAB with media buttons

### Navigation & UI
- [x] 5-tab bottom nav (الرئيسية, الصلاة, صُحبة, الرسائل, المزيد)
- [x] More page: profile + 8 tools grid + settings + athan
- [x] Theme toggle (dark/light/auto) properly styled
- [x] ThemeProvider with sunrise/sunset auto-switch
- [x] PermissionManager (native pre-request UI)
- [x] MosqueService (instant prayer sync)

### Islamic Tools
- [x] Prayer times, Quran, Qibla, Tasbeeh, Duas, Ruqyah, Zakat, Tracker, Ramadan

## Backlog

### P0
- [ ] Real image/video upload for posts
- [ ] Real-time notifications
- [ ] User search

### P1
- [ ] Rewards & gold system
- [ ] Digital store
- [ ] Stripe payments
- [ ] Membership/subscription

### P2
- [ ] Enhanced Qibla compass
- [ ] Enhanced Tasbeeh with rounds
- [ ] Multi-language (AR, DE, EN)
- [ ] Capacitor for native apps
