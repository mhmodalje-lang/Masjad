/**
 * Service Worker for أذان وحكاية - Azan wa Hikaya
 * Prayer notification scheduling with periodic checking
 */

const CACHE_NAME = 'azanhikaya-v4';
const ATHAN_AUDIO_CACHE = 'athan-audio-v2';

const PRECACHE_ASSETS = [
  '/',
  '/manifest.json',
  '/pwa-icon-192.png',
  '/pwa-icon-512.png',
  '/mecca-hero.webp',
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
      Promise.all(keys.filter(k => k !== CACHE_NAME && k !== ATHAN_AUDIO_CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
  startPeriodicCheck();
});

// ============ FETCH ============
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (url.pathname.startsWith('/api/')) return;

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

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() =>
        caches.match(request) || caches.match('/') || new Response('<h1 dir="rtl">غير متصل</h1>', { headers: { 'Content-Type': 'text/html; charset=utf-8' } })
      )
    );
    return;
  }

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
