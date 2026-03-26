/**
 * Prayer Notification Scheduler
 * REAL notifications using Web Notification API + Service Worker
 * Reads individual prayer notification settings from localStorage
 */
import { Coordinates, PrayerTimes, CalculationMethod, Madhab, Prayer, Qibla } from 'adhan';
import { stopAthan as stopAthanShared, playAthan as playAthanShared } from './athanAudio';

export type PrayerMethod = 'MuslimWorldLeague' | 'Egyptian' | 'Karachi' | 'UmmAlQura' | 'Dubai' | 'MoonsightingCommittee' | 'NorthAmerica' | 'Kuwait' | 'Qatar' | 'Singapore' | 'Tehran' | 'Turkey';

interface PrayerTimesResult {
  fajr: Date;
  sunrise: Date;
  dhuhr: Date;
  asr: Date;
  maghrib: Date;
  isha: Date;
}

const PRAYER_NAMES_AR: Record<string, string> = {
  fajr: 'الفجر', sunrise: 'الشروق', dhuhr: 'الظهر',
  asr: 'العصر', maghrib: 'المغرب', isha: 'العشاء'
};

const PRAYER_NAMES_EN: Record<string, string> = {
  fajr: 'Fajr', sunrise: 'Sunrise', dhuhr: 'Dhuhr',
  asr: 'Asr', maghrib: 'Maghrib', isha: 'Isha'
};

const PRAYER_EMOJIS: Record<string, string> = {
  fajr: '🌅', dhuhr: '☀️', asr: '🌤️', maghrib: '🌇', isha: '🌙'
};

export function calculatePrayerTimes(lat: number, lon: number, method: PrayerMethod = 'UmmAlQura', school: 'shafi' | 'hanafi' = 'shafi'): PrayerTimesResult {
  const coords = new Coordinates(lat, lon);
  const date = new Date();
  
  const methodMap: Record<PrayerMethod, any> = {
    MuslimWorldLeague: CalculationMethod.MuslimWorldLeague(),
    Egyptian: CalculationMethod.Egyptian(),
    Karachi: CalculationMethod.Karachi(),
    UmmAlQura: CalculationMethod.UmmAlQura(),
    Dubai: CalculationMethod.Dubai(),
    MoonsightingCommittee: CalculationMethod.MoonsightingCommittee(),
    NorthAmerica: CalculationMethod.NorthAmerica(),
    Kuwait: CalculationMethod.Kuwait(),
    Qatar: CalculationMethod.Qatar(),
    Singapore: CalculationMethod.Singapore(),
    Tehran: CalculationMethod.Tehran(),
    Turkey: CalculationMethod.Turkey(),
  };
  
  const params = methodMap[method] || CalculationMethod.UmmAlQura();
  params.madhab = school === 'hanafi' ? Madhab.Hanafi : Madhab.Shafi;
  
  const times = new PrayerTimes(coords, date, params);
  
  return {
    fajr: times.fajr,
    sunrise: times.sunrise,
    dhuhr: times.dhuhr,
    asr: times.asr,
    maghrib: times.maghrib,
    isha: times.isha,
  };
}

export function getNextPrayer(lat: number, lon: number, method: PrayerMethod = 'UmmAlQura'): { name: string; nameAr: string; time: Date; minutesLeft: number } | null {
  try {
    const coords = new Coordinates(lat, lon);
    const params = CalculationMethod.UmmAlQura();
    const times = new PrayerTimes(coords, new Date(), params);
    const nextPrayer = times.nextPrayer();
    
    if (nextPrayer === Prayer.None) return null;
    
    const prayerNames: Record<string, string> = {
      [Prayer.Fajr]: 'fajr', [Prayer.Sunrise]: 'sunrise', [Prayer.Dhuhr]: 'dhuhr',
      [Prayer.Asr]: 'asr', [Prayer.Maghrib]: 'maghrib', [Prayer.Isha]: 'isha'
    };
    
    const name = prayerNames[nextPrayer] || '';
    const time = times.timeForPrayer(nextPrayer);
    const minutesLeft = Math.floor((time.getTime() - Date.now()) / 60000);
    
    return { name, nameAr: PRAYER_NAMES_AR[name] || name, time, minutesLeft };
  } catch (_e) {
    return null;
  }
}

export function calculateQiblaDirection(lat: number, lon: number): number {
  const qibla = new Qibla(new Coordinates(lat, lon));
  return qibla.direction;
}

export function formatPrayerTime(date: Date, is12h = false): string {
  return date.toLocaleTimeString('ar-SA', {
    hour: '2-digit', minute: '2-digit',
    hour12: is12h
  });
}

// ==================== NOTIFICATION SCHEDULER ====================

export type AthanAlertCallback = (prayerKey: string, prayerTime: string) => void;

let scheduledTimers: ReturnType<typeof setTimeout>[] = [];
let athanAlertCallback: AthanAlertCallback | null = null;

export function setAthanAlertCallback(cb: AthanAlertCallback | null) {
  athanAlertCallback = cb;
}

interface PrayerTimeInput {
  key: string;
  time24: string;
  time?: string;
  name?: string;
}

/**
 * Read which prayers user has enabled from localStorage.
 * Default: all 5 prayers enabled.
 */
function getEnabledPrayers(): string[] {
  const masterEnabled = localStorage.getItem('athan-notifications');
  if (masterEnabled === 'false') return [];
  
  // Check individual prayer toggles from NotificationSettings
  const all = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha'];
  
  // If individual prayer settings exist, respect them
  const individualKey = 'notif-enabled-prayers';
  const saved = localStorage.getItem(individualKey);
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed)) return parsed;
    } catch {}
  }
  
  return all; // Default: all enabled
}

/**
 * Check if reminders (10-min before) are enabled
 */
function isReminderEnabled(): boolean {
  const saved = localStorage.getItem('notif-prayer-reminder');
  return saved !== 'false'; // Default: enabled
}

/**
 * Schedule real browser notifications for prayer times.
 * Reads settings from localStorage for individual prayer control.
 */
export function schedulePrayerNotifications(prayers: PrayerTimeInput[], enabledPrayers?: string[], reminderMinutes = 10) {
  clearPrayerSchedule();
  
  try {
    const enabled = enabledPrayers || getEnabledPrayers();
    if (enabled.length === 0) return false;
    
    const activePrayers = prayers.filter(p => enabled.includes(p.key) && p.key !== 'sunrise');
    const showReminders = isReminderEnabled();
    
    // Send prayer times to service worker for persistent background notifications
    sendPrayerTimesToSW(activePrayers);
    
    // Also schedule in main thread (works while app is open)
    for (const prayer of activePrayers) {
      const [h, m] = prayer.time24.split(':').map(Number);
      const now = new Date();
      const prayerDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), h, m, 0);
      const diff = prayerDate.getTime() - now.getTime();
      
      if (diff > 0 && diff < 24 * 60 * 60 * 1000) {
        // Schedule main prayer notification
        const timer = setTimeout(() => {
          showPrayerNotification(prayer.key);
          // Trigger fullscreen alert in-app
          if (athanAlertCallback) {
            athanAlertCallback(prayer.key, prayer.time || prayer.time24);
          }
        }, diff);
        scheduledTimers.push(timer);
        
        // Schedule 10-minute reminder
        if (showReminders && reminderMinutes > 0) {
          const reminderDiff = diff - reminderMinutes * 60 * 1000;
          if (reminderDiff > 0) {
            const reminderTimer = setTimeout(() => {
              showPrayerReminder(prayer.key, reminderMinutes);
            }, reminderDiff);
            scheduledTimers.push(reminderTimer);
          }
        }
      }
    }
    
    // Log scheduled count
    console.log(`[Prayer Notif] Scheduled ${activePrayers.length} prayers, ${scheduledTimers.length} timers`);
    return true;
  } catch (_e) {
    console.error('[Prayer Notif] Scheduling failed:', _e);
    return false;
  }
}

// Send prayer times to service worker for background notifications
async function sendPrayerTimesToSW(prayers: PrayerTimeInput[]) {
  if (!('serviceWorker' in navigator)) return;
  try {
    const reg = await navigator.serviceWorker.ready;
    if (reg.active) {
      const lang = localStorage.getItem('app-language') || 'ar';
      const soundMode = localStorage.getItem('athan-sound-mode') || 'auto';
      reg.active.postMessage({
        type: 'UPDATE_PRAYER_TIMES',
        prayers: prayers.map(p => ({ key: p.key, time24: p.time24, name: p.name })),
        language: lang,
        soundMode: soundMode,
      });
    }
    
    // Register periodic sync if available
    if ('periodicSync' in reg) {
      try {
        // @ts-ignore
        await reg.periodicSync.register('prayer-check', { minInterval: 60 * 1000 });
      } catch (_e) { /* periodic sync not supported */ }
    }
  } catch (_e) { /* Service worker not available */ }
}

/**
 * Send updated sound mode to the service worker
 */
export function updateSoundModeInSW() {
  if (!('serviceWorker' in navigator)) return;
  navigator.serviceWorker.ready.then(reg => {
    if (reg.active) {
      const soundMode = localStorage.getItem('athan-sound-mode') || 'auto';
      reg.active.postMessage({
        type: 'UPDATE_SOUND_MODE',
        soundMode,
      });
    }
  }).catch(() => {});
}

export async function sendTestNotification(): Promise<boolean> {
  if (!('Notification' in window)) return false;
  if (Notification.permission !== 'granted') {
    const result = await Notification.requestPermission();
    if (result !== 'granted') return false;
  }

  if ('serviceWorker' in navigator) {
    try {
      const reg = await navigator.serviceWorker.ready;
      if (reg.active) {
        reg.active.postMessage({ type: 'TEST_NOTIFICATION' });
        return true;
      }
    } catch (_e) {}
  }

  // Fallback to regular notification
  new Notification('🕌 اختبار - أذان وحكاية', {
    body: 'الإشعارات تعمل بنجاح! ✅ Notifications are working!',
    icon: '/pwa-icon-192.png',
  });
  return true;
}

/**
 * Send a test fullscreen athan alert (for testing in-app)
 */
export function sendTestAthanAlert(): boolean {
  if (athanAlertCallback) {
    athanAlertCallback('dhuhr', new Date().toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' }));
    return true;
  }
  return false;
}

export function clearPrayerSchedule() {
  scheduledTimers.forEach(t => clearTimeout(t));
  scheduledTimers = [];
}

function showPrayerNotification(prayer: string) {
  if (!('Notification' in window) || Notification.permission !== 'granted') return;
  
  const isAr = (localStorage.getItem('app-language') || 'ar') === 'ar';
  const prayerName = isAr ? PRAYER_NAMES_AR[prayer] : PRAYER_NAMES_EN[prayer];
  const emoji = PRAYER_EMOJIS[prayer] || '🕌';
  
  const title = isAr 
    ? `${emoji} حان وقت صلاة ${prayerName}` 
    : `${emoji} Time for ${prayerName} prayer`;
  const body = isAr 
    ? 'حيّ على الصلاة • حيّ على الفلاح' 
    : 'Come to prayer • Come to success';

  // Check sound mode to determine notification sound behavior
  const soundMode = localStorage.getItem('athan-sound-mode') || 'auto';
  const isSilentOrVibrate = soundMode === 'silent' || soundMode === 'vibrate';
  
  // Try service worker notification first (persists even after closing app)
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready.then(reg => {
      reg.showNotification(title, {
        body,
        icon: '/pwa-icon-192.png',
        badge: '/pwa-icon-192.png',
        tag: `prayer-${prayer}`,
        requireInteraction: true,
        vibrate: soundMode === 'silent' ? [] : [300, 100, 300, 100, 300],
        // @ts-ignore
        renotify: true,
        silent: isSilentOrVibrate,
        data: { prayer, type: 'athan', url: '/', soundMode },
        actions: [
          { action: 'open', title: isAr ? 'فتح التطبيق' : 'Open App' },
          { action: 'dismiss', title: isAr ? 'تجاهل' : 'Dismiss' },
        ],
      });
    });
  } else {
    new Notification(title, { body, icon: '/pwa-icon-192.png', silent: isSilentOrVibrate });
  }
  
  // Play athan audio (respects sound mode internally)
  playAthan(prayer);
  
  // Store last notification time
  localStorage.setItem(`last_notification_${prayer}`, new Date().toISOString());
}

function showPrayerReminder(prayer: string, minutes: number) {
  if (!('Notification' in window) || Notification.permission !== 'granted') return;
  
  const isAr = (localStorage.getItem('app-language') || 'ar') === 'ar';
  const prayerName = isAr ? PRAYER_NAMES_AR[prayer] : PRAYER_NAMES_EN[prayer];

  // Check sound mode for silent notifications
  const soundMode = localStorage.getItem('athan-sound-mode') || 'auto';
  const isSilentOrVibrate = soundMode === 'silent' || soundMode === 'vibrate';
  
  const title = isAr
    ? `⏰ بعد ${minutes} دقيقة صلاة ${prayerName}`
    : `⏰ ${prayerName} in ${minutes} minutes`;
  const body = isAr 
    ? 'استعد للصلاة بالوضوء' 
    : 'Prepare for prayer with wudu';
  
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready.then(reg => {
      reg.showNotification(title, {
        body,
        icon: '/pwa-icon-192.png',
        tag: `reminder-${prayer}`,
        vibrate: soundMode === 'silent' ? [] : [200, 100, 200],
        silent: isSilentOrVibrate,
        data: { prayer, type: 'reminder', url: '/prayer-times', soundMode },
      });
    });
  }
}

// Athan audio player
export function playAthan(prayer: string) {
  try {
    playAthanShared(prayer);
  } catch (_e) {}
}

export function stopAthan() {
  stopAthanShared();
}

export function getMethodNumber(method: string): number {
  const map: Record<string, number> = {
    MuslimWorldLeague: 3, Egyptian: 5, Karachi: 1, UmmAlQura: 4,
    Dubai: 16, Kuwait: 9, Qatar: 10, Singapore: 11, Turkey: 13,
    Tehran: 7, NorthAmerica: 2, MoonsightingCommittee: 15,
  };
  return map[method] || 4;
}
