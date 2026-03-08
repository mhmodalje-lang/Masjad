// Service Worker notification helper for prayer times
// This file is injected into the SW via vite-plugin-pwa's injectManifest or
// used alongside the generated SW to schedule notifications.

const PRAYER_NAMES: Record<string, string> = {
  fajr: '🌅 الفجر',
  dhuhr: '🌞 الظهر',
  asr: '🌤️ العصر',
  maghrib: '🌅 المغرب',
  isha: '🌙 العشاء',
};

/**
 * Register the SW and schedule prayer notifications using setTimeout
 * so they fire even when the app tab is inactive (SW stays alive briefly).
 * For true background push we'd need a push server, but this approach
 * leverages the periodic SW wake + Notification API which works well for PWAs.
 */
export async function schedulePrayerNotifications(
  prayers: { key: string; time24: string; time: string }[]
) {
  if (!('serviceWorker' in navigator)) return;
  if (Notification.permission !== 'granted') return;

  const reg = await navigator.serviceWorker.ready;

  // Cancel any previously scheduled notifications
  const existingTimers = (window as any).__prayerTimers as number[] | undefined;
  if (existingTimers) {
    existingTimers.forEach(clearTimeout);
  }
  const timers: number[] = [];

  const now = new Date();
  const currentMs = now.getTime();

  for (const prayer of prayers) {
    if (prayer.key === 'sunrise') continue;

    const [h, m] = prayer.time24.split(':').map(Number);
    const prayerDate = new Date(now);
    prayerDate.setHours(h, m, 0, 0);

    const diff = prayerDate.getTime() - currentMs;
    if (diff <= 0) continue; // Already passed

    const timer = window.setTimeout(() => {
      reg.showNotification('حان وقت الصلاة 🕌', {
        body: `${PRAYER_NAMES[prayer.key] || prayer.key} - ${prayer.time}`,
        icon: '/pwa-icon-192.png',
        badge: '/pwa-icon-192.png',
        tag: `prayer-${prayer.key}`,
        requireInteraction: true,
        data: { url: '/' },
      } as NotificationOptions);
    }, diff) as unknown as number;

    timers.push(timer);

    // Also schedule a 15-min reminder before prayer
    const reminderDiff = diff - 15 * 60 * 1000;
    if (reminderDiff > 0) {
      const reminderTimer = window.setTimeout(() => {
        reg.showNotification('تذكير بالصلاة 🔔', {
          body: `${PRAYER_NAMES[prayer.key] || prayer.key} بعد 15 دقيقة`,
          icon: '/pwa-icon-192.png',
          badge: '/pwa-icon-192.png',
          tag: `prayer-reminder-${prayer.key}`,
          silent: false,
          data: { url: '/' },
        } as NotificationOptions);
      }, reminderDiff) as unknown as number;

      timers.push(reminderTimer);
    }
  }

  (window as any).__prayerTimers = timers;
}
