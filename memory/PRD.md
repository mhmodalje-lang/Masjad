# المؤذن العالمي (The Global Muezzin) - PRD

## Original Problem Statement
Build an Islamic prayer and lifestyle app named "المؤذن العالمي" with:
- Accurate prayer times via Aladhan.com API
- Quran text and audio from Alquran.cloud
- Ruqyah content, Daily Hadith
- AI-powered Athkar and smart reminders via Gemini
- Persistent push notifications for Athan
- Islamic UI with manual Dark/Light mode toggle
- PWA installation for mobile users
- Full Admin Dashboard with ads management, page management, notification scheduling
- Google Play Store readiness

## Tech Stack
- Frontend: React 18, TypeScript, Vite, Tailwind CSS, Shadcn/UI
- Backend: FastAPI, Python 3.11, MongoDB (Motor)
- AI: Gemini 2.0 Flash via Emergent LLM Key
- PWA: Service Worker with periodic prayer check

## Admin Dashboard (6 Tabs)
- **Overview**: Stats (users, subscribers, ads)
- **Users**: List/delete users
- **Ads**: CRUD for 11 platforms (Google AdSense, AdMob, ExoClick, PopAds, Clickadu, HilltopAds, Monetag, Adsterra, ySense, YouTube, Custom)
- **Notifications**: Instant send + scheduled notifications
- **Pages**: Custom page management (for Ruqyah sub-pages etc.)
- **Settings**: Maintenance mode, announcements

Admin email: mhmd321324t@gmail.com / password: admin123

## Implemented Features (March 12, 2026)
- [x] Prayer times via Aladhan.com API (unified across all pages)
- [x] Daily Hadith (30 curated, rotating daily)
- [x] AI Athkar + Smart Reminders via Gemini
- [x] Quran page (114 surahs from Alquran.cloud)
- [x] Ruqyah page with 6 categories
- [x] Prayer tracker (localStorage)
- [x] Manual Dark/Light theme toggle
- [x] PWA manifest + new app icons
- [x] Service Worker with periodic prayer check (30s interval)
- [x] Admin Dashboard with 6 tabs
- [x] Ad management system (11 platforms)
- [x] Custom pages management
- [x] Scheduled notifications
- [x] Story moderation API
- [x] Auth (email/password)
- [x] All branding updated to "المؤذن العالمي"
- [x] Backend: 30+ API endpoints tested
- [x] Frontend: All pages rendering correctly

## Backlog
### P0
- [ ] Test notifications on real device with Athan audio
- [ ] Full-screen Athan overlay at prayer time

### P1
- [ ] Google social login
- [ ] Quran audio from Mp3Quran.net
- [ ] Qibla compass
- [ ] Sunnah.com API integration

### P2
- [ ] Google Play Store publishing
- [ ] YouTube videos section
- [ ] Offline mode
