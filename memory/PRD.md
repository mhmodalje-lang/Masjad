# المؤذن العالمي - PRD

## Tech Stack
- Frontend: React 18, TypeScript, Vite, Tailwind CSS, Shadcn/ui, Framer Motion
- Backend: FastAPI, Python, MongoDB (motor)
- Auth: JWT + Emergent Google OAuth
- AI: Google Gemini via emergentintegrations

## Deployment Status: READY ✅
- All health checks passed
- No hardcoded URLs or API keys
- MongoDB indexes created for performance
- N+1 query fixed in sohba posts endpoint
- PWA manifest updated to "المؤذن العالمي"
- SEO metadata cleaned (removed old lovable.app URLs)
- CORS configured for production
- Auth redirect uses window.location.origin (portable)

## Implemented Features ✅
- Prayer times (Aladhan API) with instant mosque sync (MosqueService)
- Quran reader + audio player
- Qibla compass, Tasbeeh counter, Duas, Ruqyah
- Zakat calculator, Prayer tracker
- Social platform صُحبة (real MongoDB backend): posts, likes, comments, saves, follows
- 10 Islamic categories, 2-column masonry grid
- Auth: JWT email/password + Emergent Google OAuth + forgot password
- Admin Dashboard (6 tabs)
- Dual theme (emerald+gold) with auto sunrise/sunset
- TopNav with professional theme toggle icon
- 5-tab bottom nav
- PermissionManager (native-like pre-request UI)
- PWA with service worker
- Ramadan features (calendar, challenge, cards, book)

## Backlog
- P0: Real image/video upload for posts, real-time notifications
- P1: Rewards/gold system, digital store, Stripe payments, membership
- P2: Enhanced Qibla, Tasbeeh with rounds, multi-language, Capacitor
