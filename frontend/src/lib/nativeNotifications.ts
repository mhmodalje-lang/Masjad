/**
 * Native Notifications - Capacitor LocalNotifications for native builds
 * Schedules prayer notifications that work even when app is closed
 */
import { isNativeApp } from './nativeBridge';

interface PrayerTime {
  key: string;
  time24: string;
  name?: string;
}

const PRAYER_EMOJIS: Record<string, string> = {
  fajr: '🌅', dhuhr: '☀️', asr: '🌤️', maghrib: '🌇', isha: '🌙'
};

/**
 * Schedule native notifications for prayer times (Capacitor only)
 * These work even when the app is fully closed
 */
export async function scheduleNativePrayerNotifications(
  prayers: PrayerTime[],
  enabledPrayers: string[] = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha'],
  reminderMinutes: number = 10
): Promise<boolean> {
  if (!isNativeApp()) return false;
  
  try {
    const { LocalNotifications } = await import('@capacitor/local-notifications');
    
    // Request permission first
    const permResult = await LocalNotifications.requestPermissions();
    if (permResult.display !== 'granted') return false;
    
    // Cancel existing prayer notifications
    const pending = await LocalNotifications.getPending();
    const prayerNotifIds = pending.notifications
      .filter(n => n.id >= 1000 && n.id < 2000)
      .map(n => ({ id: n.id }));
    if (prayerNotifIds.length > 0) {
      await LocalNotifications.cancel({ notifications: prayerNotifIds });
    }
    
    const activePrayers = prayers.filter(p => enabledPrayers.includes(p.key) && p.key !== 'sunrise');
    const notifications: any[] = [];
    const now = new Date();
    let idCounter = 1000;
    
    for (const prayer of activePrayers) {
      const [h, m] = prayer.time24.split(':').map(Number);
      const prayerDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), h, m, 0);
      
      // Only schedule future prayers
      if (prayerDate.getTime() <= now.getTime()) continue;
      
      const emoji = PRAYER_EMOJIS[prayer.key] || '🕌';
      const prayerName = prayer.name || prayer.key;
      
      // Main prayer notification
      notifications.push({
        id: idCounter++,
        title: `${emoji} حان وقت صلاة ${prayerName}`,
        body: 'حيّ على الصلاة • حيّ على الفلاح',
        schedule: { at: prayerDate },
        sound: 'athan_default.mp3',
        smallIcon: 'ic_stat_mosque',
        iconColor: '#10b981',
        actionTypeId: 'PRAYER_ACTION',
        extra: { prayer: prayer.key, type: 'athan' },
      });
      
      // 10-minute reminder
      if (reminderMinutes > 0) {
        const reminderDate = new Date(prayerDate.getTime() - reminderMinutes * 60 * 1000);
        if (reminderDate.getTime() > now.getTime()) {
          notifications.push({
            id: idCounter++,
            title: `⏰ بعد ${reminderMinutes} دقيقة صلاة ${prayerName}`,
            body: 'استعد للصلاة بالوضوء',
            schedule: { at: reminderDate },
            smallIcon: 'ic_stat_mosque',
            iconColor: '#10b981',
            extra: { prayer: prayer.key, type: 'reminder' },
          });
        }
      }
    }
    
    if (notifications.length > 0) {
      await LocalNotifications.schedule({ notifications });
      console.log(`[Native Notif] Scheduled ${notifications.length} notifications`);
    }
    
    return true;
  } catch (e) {
    console.error('[Native Notif] Failed:', e);
    return false;
  }
}

/**
 * Cancel all native prayer notifications
 */
export async function cancelNativePrayerNotifications(): Promise<void> {
  if (!isNativeApp()) return;
  try {
    const { LocalNotifications } = await import('@capacitor/local-notifications');
    const pending = await LocalNotifications.getPending();
    const prayerNotifIds = pending.notifications
      .filter(n => n.id >= 1000 && n.id < 2000)
      .map(n => ({ id: n.id }));
    if (prayerNotifIds.length > 0) {
      await LocalNotifications.cancel({ notifications: prayerNotifIds });
    }
  } catch (e) {
    console.error('[Native Notif] Cancel failed:', e);
  }
}

/**
 * Register notification action listeners
 */
export async function registerNotificationListeners(): Promise<void> {
  if (!isNativeApp()) return;
  try {
    const { LocalNotifications } = await import('@capacitor/local-notifications');
    
    // Register action types
    await LocalNotifications.registerActionTypes({
      types: [
        {
          id: 'PRAYER_ACTION',
          actions: [
            { id: 'open', title: 'فتح التطبيق' },
            { id: 'dismiss', title: 'تجاهل', destructive: true },
          ],
        },
      ],
    });
    
    // Listen for notification actions
    await LocalNotifications.addListener('localNotificationActionPerformed', (action) => {
      if (action.actionId === 'open' || action.actionId === 'tap') {
        // Navigate to prayer times page
        window.location.href = '/prayer-times';
      }
    });
  } catch (e) {
    console.error('[Native Notif] Listener registration failed:', e);
  }
}
