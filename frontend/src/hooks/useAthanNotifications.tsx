import { useEffect } from 'react';
import { PrayerTime } from './usePrayerTimes';
import { schedulePrayerNotifications, setAthanAlertCallback, AthanAlertCallback } from '@/lib/prayerNotifications';

/**
 * Request notification permission (browser native dialog)
 */
export async function requestNotificationPermission(): Promise<boolean> {
  if (!('Notification' in window)) return false;
  if (Notification.permission === 'granted') return true;
  if (Notification.permission === 'denied') return false;
  const result = await Notification.requestPermission();
  return result === 'granted';
}

/**
 * Hook: monitors prayer times and sends real notifications + fullscreen alerts.
 * Reads individual prayer settings from localStorage (notif-enabled-prayers).
 */
export function useAthanNotifications(
  prayers: PrayerTime[],
  enabled: boolean = true,
  onAlert?: AthanAlertCallback
) {
  // Register the alert callback for fullscreen overlay
  useEffect(() => {
    if (enabled && onAlert) {
      setAthanAlertCallback(onAlert);
    }
    return () => {
      setAthanAlertCallback(null);
    };
  }, [enabled, onAlert]);

  // Build a stable key from prayer times to detect real changes
  const prayersKey = prayers.map(p => `${p.key}:${p.time24}`).join(',');

  // Also watch individual prayer settings
  const enabledPrayersStr = typeof window !== 'undefined' 
    ? (localStorage.getItem('notif-enabled-prayers') || '') 
    : '';

  useEffect(() => {
    if (!enabled || prayers.length === 0) return;
    // schedulePrayerNotifications reads enabled prayers from localStorage internally
    schedulePrayerNotifications(prayers);
  }, [prayersKey, enabled, enabledPrayersStr]);
}
