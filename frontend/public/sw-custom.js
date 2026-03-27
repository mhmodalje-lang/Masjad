/**
 * ═══════════════════════════════════════════════════════
 * 🕌 أذان وحكاية - Advanced Service Worker
 * ═══════════════════════════════════════════════════════
 * Offline-First PWA with:
 * - App Shell: Cache-first
 * - API: Network-first with IndexedDB + Cache API fallback
 * - Images/Fonts: Cache-first with network update
 * - Background Sync for failed POST requests
 * - Prayer notification scheduling
 */

const APP_SHELL_CACHE = 'app-shell-v7';
const API_CACHE = 'api-cache-v3';
const IMAGE_CACHE = 'images-v2';
const FONT_CACHE = 'fonts-v1';
const AUDIO_CACHE = 'athan-audio-v2';

// ═══ App Shell: Pre-cached on install ═══
const APP_SHELL_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  '/pwa-icon-48.png',
  '/pwa-icon-72.png',
  '/pwa-icon-96.png',
  '/pwa-icon-128.png',
  '/pwa-icon-144.png',
  '/pwa-icon-152.png',
  '/pwa-icon-192.png',
  '/pwa-icon-384.png',
  '/pwa-icon-512.png',
  '/pwa-icon-maskable.png',
  '/apple-touch-icon.png',
  '/mecca-hero.webp',
];

// ═══ API routes to cache ═══
const CACHEABLE_API_PATTERNS = [
  '/api/prayer-times',
  '/api/quran/v4/chapters',
  '/api/quran/v4/verses',
  '/api/quran/v4/juzs',
  '/api/ruqyah',
  '/api/stories/list',
  '/api/stories/categories',
  '/api/daily-hadith',
  '/api/ai/verse-of-day',
  '/api/ai/hadith-of-day',
  '/api/ai/daily-dua',
  '/api/live-streams',
  '/api/ad-config',
  '/api/ads/active',
  '/api/daily-content',
  '/api/localization',
  '/api/announcements',
  '/api/kids-learn',
  '/api/arabic-academy',
  '/api/health',
  '/api/',
];

// ═══ Routes to serve index.html (SPA navigation) ═══
const SPA_ROUTES = [
  '/prayer-times', '/quran', '/ruqyah', '/stories', '/duas',
  '/qibla', '/tasbeeh', '/explore', '/live', '/kids',
  '/admin', '/auth', '/profile', '/settings', '/notifications',
  '/privacy', '/terms', '/delete-data', '/content-policy',
  '/about', '/marketplace', '/social', '/messages',
  '/forty-nawawi', '/surah', '/tafsir', '/daily-duas',
  '/ramadan', '/asma-al-husna', '/prayer-tracker',
  '/arabic-academy', '/video-reels', '/noor-academy',
  '/mosque-prayer-times', '/islamic-calendar',
];

// ═══ Offline HTML Fallback ═══
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
    .retry-btn { display: inline-flex; align-items: center; gap: 8px; padding: 14px 36px; background: linear-gradient(135deg, #10b981, #059669); color: white; border-radius: 16px; font-weight: 700; font-size: 15px; border: none; cursor: pointer; transition: transform 0.2s; }
    .retry-btn:active { transform: scale(0.96); }
    .pulse { animation: pulse 2s ease-in-out infinite; }
    @keyframes pulse { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
  </style>
</head>
<body>
  <div class="container">
    <div class="icon-wrap pulse"><span class="icon">📡</span></div>
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
    <button class="retry-btn" onclick="location.reload()">🔄 إعادة المحاولة</button>
  </div>
</body>
</html>`;

// ═══════════════════════════════════════════
// INSTALL: Pre-cache App Shell
// ═══════════════════════════════════════════
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(APP_SHELL_CACHE).then(async (cache) => {
      console.log('[SW] Pre-caching app shell');
      // Cache files one by one to avoid failing all
      for (const file of APP_SHELL_FILES) {
        try {
          await cache.add(file);
        } catch (e) {
          console.warn(`[SW] Failed to cache: ${file}`, e);
        }
      }
      // Also cache the offline page
      const offlineResponse = new Response(OFFLINE_HTML, {
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
      });
      await cache.put('/offline.html', offlineResponse);
    })
  );
  self.skipWaiting();
});

// ═══════════════════════════════════════════
// ACTIVATE: Clean old caches
// ═══════════════════════════════════════════
self.addEventListener('activate', (event) => {
  const currentCaches = [APP_SHELL_CACHE, API_CACHE, IMAGE_CACHE, FONT_CACHE, AUDIO_CACHE];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => !currentCaches.includes(name))
          .map((name) => {
            console.log(`[SW] Deleting old cache: ${name}`);
            return caches.delete(name);
          })
      );
    }).then(() => self.clients.claim())
  );
});

// ═══════════════════════════════════════════
// FETCH: Smart routing strategies
// ═══════════════════════════════════════════
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests (except API caching)
  if (request.method !== 'GET') {
    // Queue POST/PUT/DELETE for background sync when offline
    if (!navigator.onLine && request.url.includes('/api/')) {
      event.respondWith(
        new Response(JSON.stringify({ queued: true, message: 'سيتم الإرسال عند عودة الاتصال' }), {
          status: 202,
          headers: { 'Content-Type': 'application/json' },
        })
      );
    }
    return;
  }

  // Chrome extensions, analytics, etc.
  if (!url.protocol.startsWith('http')) return;
  if (url.hostname.includes('google-analytics') || url.hostname.includes('googletagmanager')) return;

  // ── Strategy 1: API calls → Network-first with cache fallback ──
  if (url.pathname.startsWith('/api/') || url.hostname.includes('api.aladhan.com') || url.hostname.includes('api.quran.com')) {
    event.respondWith(networkFirstWithCache(request, API_CACHE));
    return;
  }

  // ── Strategy 2: Fonts → Cache-first ──
  if (url.hostname.includes('fonts.googleapis.com') || url.hostname.includes('fonts.gstatic.com')) {
    event.respondWith(cacheFirstWithNetwork(request, FONT_CACHE, 30 * 24 * 60 * 60 * 1000));
    return;
  }

  // ── Strategy 3: Images → Cache-first with network update ──
  if (request.destination === 'image' || /\.(png|jpg|jpeg|webp|gif|svg|ico)$/i.test(url.pathname)) {
    event.respondWith(cacheFirstWithNetwork(request, IMAGE_CACHE, 7 * 24 * 60 * 60 * 1000));
    return;
  }

  // ── Strategy 4: Audio → Cache-first ──
  if (request.destination === 'audio' || /\.(mp3|wav|ogg|aac)$/i.test(url.pathname)) {
    event.respondWith(cacheFirstWithNetwork(request, AUDIO_CACHE, 30 * 24 * 60 * 60 * 1000));
    return;
  }

  // ── Strategy 5: SPA navigation → Cache-first with network update ──
  if (request.mode === 'navigate' || request.destination === 'document') {
    event.respondWith(handleNavigationRequest(request));
    return;
  }

  // ── Strategy 6: JS/CSS (hashed assets) → Cache-first ──
  if (url.pathname.startsWith('/assets/') || /\.(js|css)$/i.test(url.pathname)) {
    event.respondWith(cacheFirstWithNetwork(request, APP_SHELL_CACHE, 30 * 24 * 60 * 60 * 1000));
    return;
  }

  // ── Default: Network-first ──
  event.respondWith(networkFirstWithCache(request, APP_SHELL_CACHE));
});

// ═══════════════════════════════════════════
// Caching Strategies
// ═══════════════════════════════════════════

/**
 * Network-first: Try network, fallback to cache
 */
async function networkFirstWithCache(request, cacheName) {
  try {
    const networkResponse = await fetch(request, { signal: AbortSignal.timeout(8000) });
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) return cachedResponse;
    
    // For API calls, return empty JSON
    if (request.url.includes('/api/')) {
      return new Response(JSON.stringify({ offline: true, data: null }), {
        status: 503,
        headers: { 'Content-Type': 'application/json' },
      });
    }
    return new Response('Offline', { status: 503 });
  }
}

/**
 * Cache-first: Use cache, update from network in background
 */
async function cacheFirstWithNetwork(request, cacheName, maxAge = 86400000) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    // Check if still fresh
    const dateHeader = cachedResponse.headers.get('date') || cachedResponse.headers.get('sw-cached-at');
    if (dateHeader) {
      const age = Date.now() - new Date(dateHeader).getTime();
      if (age > maxAge) {
        // Stale - update in background
        updateCache(request, cacheName);
      }
    }
    return cachedResponse;
  }

  // Not in cache - fetch from network
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch {
    return new Response('Offline', { status: 503 });
  }
}

/**
 * Update cache in background (don't block response)
 */
function updateCache(request, cacheName) {
  fetch(request)
    .then(response => {
      if (response.ok) {
        caches.open(cacheName).then(cache => cache.put(request, response));
      }
    })
    .catch(() => {}); // Silently fail
}

/**
 * Handle SPA navigation requests
 */
async function handleNavigationRequest(request) {
  const url = new URL(request.url);

  // Check if this is a known SPA route
  const isSPARoute = SPA_ROUTES.some(route => url.pathname.startsWith(route)) || url.pathname === '/';

  if (isSPARoute) {
    // Try network first for HTML
    try {
      const networkResponse = await fetch(request, { signal: AbortSignal.timeout(6000) });
      if (networkResponse.ok) {
        const cache = await caches.open(APP_SHELL_CACHE);
        cache.put('/', networkResponse.clone());
        return networkResponse;
      }
    } catch {}

    // Fallback to cached index.html
    const cachedIndex = await caches.match('/');
    if (cachedIndex) return cachedIndex;

    const cachedIndexHtml = await caches.match('/index.html');
    if (cachedIndexHtml) return cachedIndexHtml;
  }

  // Last resort: offline page
  const offlinePage = await caches.match('/offline.html');
  if (offlinePage) return offlinePage;

  return new Response(OFFLINE_HTML, {
    headers: { 'Content-Type': 'text/html; charset=utf-8' },
  });
}

// ═══════════════════════════════════════════
// BACKGROUND SYNC
// ═══════════════════════════════════════════
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-pending-requests') {
    event.waitUntil(processPendingRequests());
  }
  if (event.tag === 'sync-prayer-notifications') {
    event.waitUntil(checkAndNotify());
  }
});

async function processPendingRequests() {
  // Process any queued API calls from IndexedDB sync_queue
  try {
    const db = await openIDB();
    const tx = db.transaction('sync_queue', 'readwrite');
    const store = tx.objectStore('sync_queue');
    const items = await idbGetAll(store);
    
    for (const item of items) {
      try {
        await fetch(item.url, {
          method: item.method,
          headers: item.headers,
          body: item.body,
        });
        store.delete(item.id);
      } catch {
        // Will retry next sync
      }
    }
  } catch (e) {
    console.error('[SW] Background sync failed:', e);
  }
}

// Simple IDB helper for SW context
function openIDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open('azanhikaya_offline', 5);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

function idbGetAll(store) {
  return new Promise((resolve, reject) => {
    const req = store.getAll();
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

// ═══════════════════════════════════════════
// PRAYER NOTIFICATION SCHEDULING
// ═══════════════════════════════════════════

const PRAYER_NAMES = {
  ar: { fajr: 'الفجر', dhuhr: 'الظهر', asr: 'العصر', maghrib: 'المغرب', isha: 'العشاء' },
  en: { fajr: 'Fajr', dhuhr: 'Dhuhr', asr: 'Asr', maghrib: 'Maghrib', isha: 'Isha' },
};

const PRAYER_EMOJIS = { fajr: '🌅', dhuhr: '☀️', asr: '🌤️', maghrib: '🌇', isha: '🌙' };

async function checkAndNotify() {
  try {
    // Read prayer times from IndexedDB
    const db = await openIDB();
    const tx = db.transaction('prayer_times', 'readonly');
    const store = tx.objectStore('prayer_times');
    const allTimes = await idbGetAll(store);
    
    if (!allTimes.length) return;
    
    // Get latest cached prayer times
    const latest = allTimes.sort((a, b) => (b.cached_at || 0) - (a.cached_at || 0))[0];
    if (!latest || !latest.times) return;
    
    const now = new Date();
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    const lang = 'ar';
    const names = PRAYER_NAMES[lang] || PRAYER_NAMES.ar;
    
    const prayerEntries = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha'];
    
    for (const key of prayerEntries) {
      const timeStr = latest.times[key];
      if (!timeStr) continue;
      
      const [h, m] = timeStr.split(':').map(Number);
      const prayerMinutes = h * 60 + m;
      
      // Notify if within 1 minute window
      if (Math.abs(currentMinutes - prayerMinutes) <= 1) {
        const emoji = PRAYER_EMOJIS[key] || '🕌';
        const prayerName = names[key] || key;
        
        await self.registration.showNotification(
          `${emoji} حان وقت صلاة ${prayerName}`,
          {
            body: 'حيّ على الصلاة • حيّ على الفلاح',
            icon: '/pwa-icon-192.png',
            badge: '/pwa-icon-72.png',
            tag: `prayer-${key}`,
            renotify: true,
            vibrate: [200, 100, 200, 100, 200],
            data: { prayer: key, type: 'athan', url: '/prayer-times' },
            actions: [
              { action: 'open', title: 'فتح التطبيق' },
              { action: 'dismiss', title: 'تجاهل' },
            ],
          }
        );
      }
      
      // 10-minute reminder
      if (prayerMinutes - currentMinutes === 10) {
        const prayerName = names[key] || key;
        await self.registration.showNotification(
          `⏰ بعد 10 دقائق صلاة ${prayerName}`,
          {
            body: 'استعد للصلاة بالوضوء',
            icon: '/pwa-icon-192.png',
            badge: '/pwa-icon-72.png',
            tag: `reminder-${key}`,
            data: { prayer: key, type: 'reminder', url: '/prayer-times' },
          }
        );
      }
    }
  } catch (e) {
    console.error('[SW] Notification check failed:', e);
  }
}

// ═══ Check prayer times every 30 seconds ═══
let notifInterval = null;
function startNotificationChecker() {
  if (notifInterval) return;
  notifInterval = setInterval(checkAndNotify, 30000);
  checkAndNotify(); // Run immediately
}

// Start checker when SW activates
self.addEventListener('activate', () => {
  startNotificationChecker();
});

// ═══ Notification click handler ═══
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'dismiss') return;
  
  const url = event.notification.data?.url || '/';
  
  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then((clients) => {
      for (const client of clients) {
        if (client.url.includes(self.registration.scope)) {
          client.navigate(url);
          return client.focus();
        }
      }
      return self.clients.openWindow(url);
    })
  );
});

// ═══ Periodic sync (if supported) ═══
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'check-prayer-times') {
    event.waitUntil(checkAndNotify());
  }
});

// ═══ Push notification handler ═══
self.addEventListener('push', (event) => {
  let data = {};
  try {
    data = event.data?.json() || {};
  } catch {
    data = { title: 'أذان وحكاية', body: event.data?.text() || 'إشعار جديد' };
  }
  
  event.waitUntil(
    self.registration.showNotification(data.title || '🕌 أذان وحكاية', {
      body: data.body || '',
      icon: '/pwa-icon-192.png',
      badge: '/pwa-icon-72.png',
      data: data,
      vibrate: [200, 100, 200],
    })
  );
});

// ═══ Message handler for main thread communication ═══
self.addEventListener('message', (event) => {
  if (event.data?.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  if (event.data?.type === 'CHECK_PRAYERS') {
    checkAndNotify();
  }
  if (event.data?.type === 'CACHE_URLS') {
    const urls = event.data.urls || [];
    caches.open(APP_SHELL_CACHE).then(cache => {
      urls.forEach(url => cache.add(url).catch(() => {}));
    });
  }
});
