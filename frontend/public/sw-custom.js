/**
 * Custom Service Worker for المؤذن العالمي
 * Handles: Push notifications, Athan audio, PWA caching
 */

const CACHE_NAME = 'almuadhin-v2';
const OFFLINE_PAGE = '/offline.html';
const ATHAN_AUDIO_CACHE = 'athan-audio-v1';

// Core assets to pre-cache
const PRECACHE_ASSETS = [
  '/',
  '/manifest.json',
  '/pwa-icon-192.png',
  '/pwa-icon-512.png',
  '/mecca-hero.webp',
  '/offline.html',
];

// Install
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_ASSETS.filter(Boolean)))
      .then(() => self.skipWaiting())
  );
});

// Activate
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME && k !== ATHAN_AUDIO_CACHE).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

// Fetch - Network first, fallback to cache
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip API calls
  if (url.pathname.startsWith('/api/')) return;

  // Audio files - cache first
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

  // HTML pages - network first
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() =>
        caches.match(request) || caches.match(OFFLINE_PAGE) || new Response('<h1>غير متصل</h1>', { headers: { 'Content-Type': 'text/html; charset=utf-8' } })
      )
    );
    return;
  }

  // Static assets - cache first
  event.respondWith(
    caches.match(request).then(cached =>
      cached || fetch(request).then(response => {
        if (response.ok && !url.pathname.includes('hot-update')) {
          caches.open(CACHE_NAME).then(cache => cache.put(request, response.clone()));
        }
        return response;
      })
    ).catch(() => caches.match(OFFLINE_PAGE))
  );
});

// Push notification received
self.addEventListener('push', (event) => {
  let data = {};
  try {
    data = event.data?.json() || {};
  } catch (_e) {
    data = { title: 'المؤذن العالمي', body: event.data?.text() || '' };
  }

  const title = data.title || '🕌 المؤذن العالمي';
  const options = {
    body: data.body || 'حان وقت الصلاة',
    icon: data.icon || '/pwa-icon-192.png',
    badge: '/pwa-icon-192.png',
    tag: data.tag || 'almuadhin',
    requireInteraction: data.requireInteraction !== false,
    vibrate: data.vibrate || [300, 100, 300, 100, 300],
    data: { url: data.url || '/', prayer: data.prayer, ...data.data },
    actions: data.actions || [
      { action: 'open', title: '📖 فتح التطبيق' },
      { action: 'dismiss', title: 'تجاهل' },
    ],
    // Rich notification
    dir: 'rtl',
    lang: 'ar',
    silent: false,
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification click
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'dismiss') return;

  const url = event.notification.data?.url || '/';
  
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clients => {
      // Focus existing window
      for (const client of clients) {
        if (client.url.includes(self.location.origin)) {
          client.focus();
          client.navigate(url);
          return;
        }
      }
      // Open new window
      return self.clients.openWindow(url);
    })
  );
});

// Background sync for prayer schedules
self.addEventListener('sync', (event) => {
  if (event.tag === 'prayer-sync') {
    event.waitUntil(syncPrayerTimes());
  }
});

async function syncPrayerTimes() {
  try {
    const cache = await caches.open(CACHE_NAME);
    const settingsResponse = await cache.match('/api/settings');
    // Update prayer times in background
  } catch (_e) {}
}

// Message from app
self.addEventListener('message', (event) => {
  if (event.data?.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  if (event.data?.type === 'PRAYER_NOTIFICATION') {
    const { prayer, time } = event.data;
    const delay = new Date(time).getTime() - Date.now();
    if (delay > 0) {
      setTimeout(() => {
        self.registration.showNotification(`🕌 حان وقت صلاة ${prayer}`, {
          body: 'استعد للصلاة • الصلاة خير من النوم',
          icon: '/pwa-icon-192.png',
          badge: '/pwa-icon-192.png',
          tag: `prayer-${prayer}`,
          requireInteraction: true,
          vibrate: [300, 100, 300, 100, 300],
          dir: 'rtl',
        });
      }, delay);
    }
  }
});
