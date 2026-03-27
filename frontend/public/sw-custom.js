/**
 * Service Worker for أذان وحكاية - Azan wa Hikaya
 * Prayer notification scheduling with periodic checking
 */

const CACHE_NAME = 'azanhikaya-v6';
const ATHAN_AUDIO_CACHE = 'athan-audio-v2';
const API_CACHE = 'api-cache-v2';

// API endpoints that should be cached for offline use
const CACHEABLE_API_PATTERNS = [
  '/api/prayer-times',
  '/api/ai/verse-of-day',
  '/api/ai/hadith-of-day',
  '/api/ai/daily-dua',
  '/api/stories/list',
  '/api/stories/categories',
  '/api/duas/',
  '/api/quran/',
  '/api/stories/moderation-status',
  '/api/ad-config',
  '/api/ads/active',
  '/api/ruqyah/',
  '/api/daily-content',
  '/api/health',
  '/api/',
];

const PRECACHE_ASSETS = [
  '/',
  '/manifest.json',
  '/pwa-icon-48.png',
  '/pwa-icon-72.png',
  '/pwa-icon-96.png',
  '/pwa-icon-192.png',
  '/pwa-icon-512.png',
  '/pwa-icon-maskable.png',
  '/apple-touch-icon.png',
  '/mecca-hero.webp',
  '/favicon.ico',
];

const PRAYER_NAMES = {
  ar: { fajr: 'الفجر', dhuhr: 'الظهر', asr: 'العصر', maghrib: 'المغرب', isha: 'العشاء' },
  en: { fajr: 'Fajr', dhuhr: 'Dhuhr', asr: 'Asr', maghrib: 'Maghrib', isha: 'Isha' },
  de: { fajr: 'Fajr', dhuhr: 'Dhuhr', asr: 'Asr', maghrib: 'Maghrib', isha: 'Ischa' },
  'de-AT': { fajr: 'Fajr', dhuhr: 'Dhuhr', asr: 'Asr', maghrib: 'Maghrib', isha: 'Ischa' },
  fr: { fajr: 'Fajr', dhuhr: 'Dhouhr', asr: 'Asr', maghrib: 'Maghrib', isha: 'Isha' },
  tr: { fajr: 'İmsak', dhuhr: 'Öğle', asr: 'İkindi', maghrib: 'Akşam', isha: 'Yatsı' },
  ru: { fajr: 'Фаджр', dhuhr: 'Зухр', asr: 'Аср', maghrib: 'Магриб', isha: 'Иша' },
  sv: { fajr: 'Fajr', dhuhr: 'Dhuhr', asr: 'Asr', maghrib: 'Maghrib', isha: 'Isha' },
  nl: { fajr: 'Fajr', dhuhr: 'Dhoehr', asr: 'Asr', maghrib: 'Maghrib', isha: 'Isha' },
  el: { fajr: 'Φατζρ', dhuhr: 'Ντουχρ', asr: 'Ασρ', maghrib: 'Μαγκρίμπ', isha: 'Ίσα' },
};

const NOTIF_STRINGS = {
  ar: { timeFor: 'حان وقت صلاة', prepare: 'حيّ على الصلاة • حيّ على الفلاح', inMinutes: 'بعد 10 دقائق صلاة', prepareWudu: 'استعد للصلاة بالوضوء', open: 'فتح التطبيق', dismiss: 'تجاهل' },
  en: { timeFor: 'Time for', prepare: 'Come to prayer • Come to success', inMinutes: 'in 10 minutes', prepareWudu: 'Prepare for prayer with wudu', open: 'Open App', dismiss: 'Dismiss' },
  de: { timeFor: 'Zeit für', prepare: 'Komm zum Gebet • Komm zum Erfolg', inMinutes: 'in 10 Minuten', prepareWudu: 'Bereite dich mit Wudu auf das Gebet vor', open: 'App öffnen', dismiss: 'Schließen' },
  'de-AT': { timeFor: 'Zeit für', prepare: 'Komm zum Gebet • Komm zum Erfolg', inMinutes: 'in 10 Minuten', prepareWudu: 'Bereite dich mit Wudu vor', open: 'App öffnen', dismiss: 'Schließen' },
  fr: { timeFor: "L'heure de", prepare: 'Venez à la prière • Venez au succès', inMinutes: 'dans 10 minutes', prepareWudu: 'Préparez-vous avec le wudu', open: "Ouvrir l'app", dismiss: 'Fermer' },
  tr: { timeFor: 'Vakit geldi:', prepare: 'Haydi namaza • Haydi felaha', inMinutes: '10 dakika sonra', prepareWudu: 'Abdest alarak namaza hazırlanın', open: 'Uygulamayı aç', dismiss: 'Kapat' },
  ru: { timeFor: 'Время намаза', prepare: 'Спешите на молитву • Спешите к успеху', inMinutes: 'через 10 минут', prepareWudu: 'Подготовьтесь к молитве', open: 'Открыть', dismiss: 'Закрыть' },
  sv: { timeFor: 'Dags för', prepare: 'Kom till bönen • Kom till framgång', inMinutes: 'om 10 minuter', prepareWudu: 'Förbered dig med wudu', open: 'Öppna app', dismiss: 'Stäng' },
  nl: { timeFor: 'Tijd voor', prepare: 'Kom tot het gebed • Kom tot het succes', inMinutes: 'over 10 minuten', prepareWudu: 'Bereid je voor met wudu', open: 'Open app', dismiss: 'Sluiten' },
  el: { timeFor: 'Ώρα για', prepare: 'Ελάτε στην προσευχή', inMinutes: 'σε 10 λεπτά', prepareWudu: 'Ετοιμαστείτε με wudu', open: 'Άνοιγμα', dismiss: 'Κλείσιμο' },
};

// ============ PRAYER TIME STORAGE ============
let storedPrayerTimes = [];
let notifiedToday = {};
let checkInterval = null;
let userLanguage = 'ar';
let athanSoundMode = 'auto'; // 'sound' | 'vibrate' | 'silent' | 'auto'

function loadPrayerData() {
  // IndexedDB would be better, but for simplicity use global state + message passing
}

function isPrayerTime(prayerTime24, nowH, nowM) {
  const [h, m] = prayerTime24.split(':').map(Number);
  return h === nowH && m === nowM;
}

function checkAndNotify() {
  if (!storedPrayerTimes || storedPrayerTimes.length === 0) return;

  const now = new Date();
  const nowH = now.getHours();
  const nowM = now.getMinutes();
  const todayKey = now.toISOString().split('T')[0];

  // Reset notifications at midnight
  if (notifiedToday._date !== todayKey) {
    notifiedToday = { _date: todayKey };
  }

  for (const prayer of storedPrayerTimes) {
    if (prayer.key === 'sunrise') continue;
    const notifKey = `${todayKey}-${prayer.key}`;

    if (notifiedToday[notifKey]) continue;

    if (isPrayerTime(prayer.time24, nowH, nowM)) {
      notifiedToday[notifKey] = true;
      const names = PRAYER_NAMES[userLanguage] || PRAYER_NAMES.ar;
      const strings = NOTIF_STRINGS[userLanguage] || NOTIF_STRINGS.ar;
      const name = names[prayer.key] || prayer.key;
      const isRTL = userLanguage === 'ar';

      const isSilentOrVibrate = athanSoundMode === 'silent' || athanSoundMode === 'vibrate';

      self.registration.showNotification(`🕌 ${strings.timeFor} ${name}`, {
        body: strings.prepare,
        icon: '/pwa-icon-192.png',
        badge: '/pwa-icon-192.png',
        tag: `athan-${prayer.key}`,
        requireInteraction: true,
        vibrate: athanSoundMode === 'silent' ? [] : [300, 100, 300, 100, 300, 100, 300],
        renotify: true,
        silent: isSilentOrVibrate,
        dir: isRTL ? 'rtl' : 'ltr',
        lang: userLanguage,
        data: { prayer: prayer.key, type: 'athan', url: '/', soundMode: athanSoundMode },
        actions: [
          { action: 'open', title: strings.open },
          { action: 'dismiss', title: strings.dismiss },
        ],
      });
    }

    // 10-minute reminder
    const [ph, pm] = prayer.time24.split(':').map(Number);
    let remH = ph, remM = pm - 10;
    if (remM < 0) { remM += 60; remH -= 1; }
    if (remH < 0) remH += 24;
    const remKey = `${todayKey}-rem-${prayer.key}`;

    if (!notifiedToday[remKey] && nowH === remH && nowM === remM) {
      notifiedToday[remKey] = true;
      const names = PRAYER_NAMES[userLanguage] || PRAYER_NAMES.ar;
      const strings = NOTIF_STRINGS[userLanguage] || NOTIF_STRINGS.ar;
      const name = names[prayer.key] || prayer.key;
      const isRTL = userLanguage === 'ar';
      const isSilentOrVibrate = athanSoundMode === 'silent' || athanSoundMode === 'vibrate';
      self.registration.showNotification(`⏰ ${name} ${strings.inMinutes}`, {
        body: strings.prepareWudu,
        icon: '/pwa-icon-192.png',
        badge: '/pwa-icon-192.png',
        tag: `reminder-${prayer.key}`,
        vibrate: athanSoundMode === 'silent' ? [] : [200, 100, 200],
        silent: isSilentOrVibrate,
        dir: isRTL ? 'rtl' : 'ltr',
        lang: userLanguage,
        data: { prayer: prayer.key, type: 'reminder', url: '/prayer-times' },
      });
    }
  }
}

function startPeriodicCheck() {
  if (checkInterval) clearInterval(checkInterval);
  checkInterval = setInterval(checkAndNotify, 30000); // Check every 30 seconds
  checkAndNotify(); // Immediate check
}

// ============ INSTALL ============
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_ASSETS.filter(Boolean)))
      .then(() => self.skipWaiting())
  );
});

// ============ ACTIVATE ============
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME && k !== ATHAN_AUDIO_CACHE && k !== API_CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
  startPeriodicCheck();
});

// ============ FETCH ============
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle cacheable API requests (network-first, cache-fallback)
  if (url.pathname.startsWith('/api/')) {
    const isCacheable = CACHEABLE_API_PATTERNS.some(p => url.pathname.startsWith(p));
    if (isCacheable && request.method === 'GET') {
      event.respondWith(
        caches.open(API_CACHE).then(async cache => {
          try {
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
              cache.put(request, networkResponse.clone());
            }
            return networkResponse;
          } catch (err) {
            const cached = await cache.match(request);
            if (cached) return cached;
            return new Response(JSON.stringify({ error: 'offline', message: 'غير متصل بالإنترنت' }), {
              status: 503,
              headers: { 'Content-Type': 'application/json' }
            });
          }
        })
      );
      return;
    }
    // Non-cacheable API: pass through (POST, PUT, DELETE etc.)
    return;
  }

  // Handle audio files
  if (url.pathname.includes('/audio/')) {
    event.respondWith(
      caches.open(ATHAN_AUDIO_CACHE).then(async cache => {
        const cached = await cache.match(request);
        if (cached) return cached;
        const response = await fetch(request).catch(() => null);
        if (response?.ok) cache.put(request, response.clone());
        return response || new Response('', { status: 404 });
      })
    );
    return;
  }

  // Handle navigation (app shell)
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() =>
        caches.match(request) || caches.match('/') || new Response(OFFLINE_HTML, { headers: { 'Content-Type': 'text/html; charset=utf-8' } })
      )
    );
    return;
  }

  // Handle static assets (cache-first)
  event.respondWith(
    caches.match(request).then(cached =>
      cached || fetch(request).then(response => {
        if (response.ok && !url.pathname.includes('hot-update')) {
          caches.open(CACHE_NAME).then(cache => cache.put(request, response.clone()));
        }
        return response;
      })
    ).catch(() => caches.match('/'))
  );
});

// ============ OFFLINE HTML ============
const OFFLINE_HTML = `<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>أذان وحكاية - غير متصل</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, 'IBM Plex Sans Arabic', system-ui, sans-serif; background: linear-gradient(135deg, #071a12 0%, #0d2a1c 40%, #051410 100%); color: #e2e8f0; min-height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px; padding-top: env(safe-area-inset-top, 20px); padding-bottom: env(safe-area-inset-bottom, 20px); }
    .container { max-width: 380px; }
    .icon-wrap { width: 80px; height: 80px; border-radius: 24px; background: rgba(16,185,129,0.15); display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; }
    .icon { font-size: 40px; }
    h1 { font-size: 22px; margin-bottom: 8px; color: #10b981; font-weight: 700; }
    .subtitle { font-size: 14px; color: #94a3b8; line-height: 1.8; margin-bottom: 24px; }
    .features { list-style: none; text-align: right; margin: 0 0 24px; padding: 16px; background: rgba(255,255,255,0.03); border-radius: 16px; border: 1px solid rgba(255,255,255,0.06); }
    .features li { padding: 10px 0; font-size: 14px; color: #cbd5e1; display: flex; align-items: center; gap: 10px; }
    .features li:not(:last-child) { border-bottom: 1px solid rgba(255,255,255,0.05); }
    .features li .emoji { font-size: 18px; flex-shrink: 0; }
    .retry-btn { display: inline-flex; align-items: center; gap: 8px; padding: 14px 36px; background: linear-gradient(135deg, #10b981, #059669); color: white; border-radius: 16px; font-weight: 700; text-decoration: none; font-size: 15px; border: none; cursor: pointer; transition: transform 0.2s; }
    .retry-btn:active { transform: scale(0.96); }
    .pulse { animation: pulse 2s ease-in-out infinite; }
    @keyframes pulse { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
  </style>
</head>
<body>
  <div class="container">
    <div class="icon-wrap pulse">
      <span class="icon">📡</span>
    </div>
    <h1>غير متصل بالإنترنت</h1>
    <p class="subtitle">لا يوجد اتصال بالإنترنت حالياً. يمكنك الاستمرار باستخدام المحتوى المحفوظ:</p>
    <ul class="features">
      <li><span class="emoji">⏰</span> أوقات الصلاة المحفوظة</li>
      <li><span class="emoji">📖</span> القرآن الكريم</li>
      <li><span class="emoji">📚</span> القصص والحكايات المحفوظة</li>
      <li><span class="emoji">🤲</span> الأدعية والأذكار</li>
      <li><span class="emoji">📿</span> المسبحة الإلكترونية</li>
      <li><span class="emoji">🎧</span> الرقية الشرعية</li>
    </ul>
    <button class="retry-btn" onclick="location.reload()">
      🔄 إعادة المحاولة
    </button>
  </div>
</body>
</html>`;

// ============ PUSH ============
self.addEventListener('push', (event) => {
  let data = {};
  try { data = event.data?.json() || {}; } catch (_e) { data = { title: 'Azan wa Hikaya', body: event.data?.text() || '' }; }
  const strings = NOTIF_STRINGS[userLanguage] || NOTIF_STRINGS.ar;
  const isRTL = userLanguage === 'ar';

  event.waitUntil(
    self.registration.showNotification(data.title || '🕌 Azan wa Hikaya', {
      body: data.body || strings.prepare,
      icon: '/pwa-icon-192.png',
      badge: '/pwa-icon-192.png',
      tag: data.tag || 'almuadhin',
      requireInteraction: true,
      vibrate: [300, 100, 300, 100, 300],
      dir: isRTL ? 'rtl' : 'ltr',
      lang: userLanguage,
      data: { url: data.url || '/', ...data.data },
      actions: [
        { action: 'open', title: strings.open },
        { action: 'dismiss', title: strings.dismiss },
      ],
    })
  );
});

// ============ NOTIFICATION CLICK ============
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  if (event.action === 'dismiss') return;

  const url = event.notification.data?.url || '/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clients => {
      for (const client of clients) {
        if (client.url.includes(self.location.origin)) {
          client.focus();
          client.navigate(url);
          return;
        }
      }
      return self.clients.openWindow(url);
    })
  );
});

// ============ MESSAGE FROM APP ============
self.addEventListener('message', (event) => {
  if (event.data?.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  // Receive prayer times from the app
  if (event.data?.type === 'UPDATE_PRAYER_TIMES') {
    storedPrayerTimes = event.data.prayers || [];
    if (event.data.language) userLanguage = event.data.language;
    if (event.data.soundMode) athanSoundMode = event.data.soundMode;
    startPeriodicCheck();

    // Respond back
    if (event.ports && event.ports[0]) {
      event.ports[0].postMessage({ status: 'ok', count: storedPrayerTimes.length });
    }
  }

  // Update language preference
  if (event.data?.type === 'UPDATE_LANGUAGE') {
    userLanguage = event.data.language || 'ar';
  }

  // Update sound mode
  if (event.data?.type === 'UPDATE_SOUND_MODE') {
    athanSoundMode = event.data.soundMode || 'auto';
  }

  // Test notification
  if (event.data?.type === 'TEST_NOTIFICATION') {
    const strings = NOTIF_STRINGS[userLanguage] || NOTIF_STRINGS.ar;
    const isRTL = userLanguage === 'ar';
    self.registration.showNotification('🕌 Test - Azan wa Hikaya', {
      body: strings.prepare,
      icon: '/pwa-icon-192.png',
      badge: '/pwa-icon-192.png',
      tag: 'test-notification',
      requireInteraction: true,
      vibrate: [300, 100, 300, 100, 300],
      dir: isRTL ? 'rtl' : 'ltr',
      lang: userLanguage,
    });
  }
});

// Keep alive via periodic sync
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'prayer-check') {
    event.waitUntil(checkAndNotify());
  }
});
