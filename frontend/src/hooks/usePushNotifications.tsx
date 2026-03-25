import { useState, useEffect, useCallback } from 'react';
import { toast } from 'sonner';
import { useLocale } from './useLocale';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';
const VAPID_PUBLIC_KEY = import.meta.env.VITE_VAPID_PUBLIC_KEY || '';

function urlBase64ToUint8Array(base64: string): Uint8Array {
  const padding = '='.repeat((4 - (base64.length % 4)) % 4);
  const b64 = (base64 + padding).replace(/-/g, '+').replace(/_/g, '/');
  const raw = window.atob(b64);
  return new Uint8Array(Array.from(raw).map(c => c.charCodeAt(0)));
}

export interface PushState {
  supported: boolean;
  permission: NotificationPermission;
  subscribed: boolean;
  loading: boolean;
}

export function usePushNotifications(userId?: string) {
  const { t } = useLocale();
  const [state, setState] = useState<PushState>({
    supported: false,
    permission: 'default',
    subscribed: false,
    loading: false,
  });

  useEffect(() => {
    const supported = 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;
    setState(prev => ({
      ...prev,
      supported,
      permission: Notification.permission,
    }));

    if (supported) {
      checkSubscription().then(subscribed => {
        setState(prev => ({ ...prev, subscribed }));
      });
    }
  }, []);

  const checkSubscription = async (): Promise<boolean> => {
    try {
      const reg = await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.getSubscription();
      return !!sub;
    } catch (_e) {
      return false;
    }
  };

  const subscribe = useCallback(async (lat?: number, lon?: number, method = 4, school = 0): Promise<boolean> => {
    setState(prev => ({ ...prev, loading: true }));
    try {
      const permission = await Notification.requestPermission();
      setState(prev => ({ ...prev, permission }));
      if (permission !== 'granted') {
        toast.error(t('notifAllowRequired'));
        return false;
      }

      const reg = await navigator.serviceWorker.ready;
      let sub = await reg.pushManager.getSubscription();
      if (sub) await sub.unsubscribe();

      sub = await reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
      });

      const json = sub.toJSON();
      if (!json.endpoint || !json.keys) throw new Error('Invalid subscription');

      const res = await fetch(`${BACKEND_URL}/api/push/subscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(localStorage.getItem('auth_token') ? { Authorization: `Bearer ${localStorage.getItem('auth_token')}` } : {}),
        },
        body: JSON.stringify({
          endpoint: json.endpoint,
          p256dh: json.keys.p256dh,
          auth: json.keys.auth,
          latitude: lat,
          longitude: lon,
          method,
          school,
          user_id: userId,
        }),
      });

      if (!res.ok) throw new Error('Failed to save subscription');

      setState(prev => ({ ...prev, subscribed: true }));
      toast.success(t('notifEnabled'));
      return true;
    } catch (err) {
      console.error('Push subscription failed:', err);
      toast.error(t('notifEnableFailed'));
      return false;
    } finally {
      setState(prev => ({ ...prev, loading: false }));
    }
  }, [userId]);

  const unsubscribe = useCallback(async (): Promise<void> => {
    try {
      const reg = await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.getSubscription();
      if (sub) await sub.unsubscribe();
      setState(prev => ({ ...prev, subscribed: false }));
      toast.success(t('notifDisabled'));
    } catch (err) {
      console.error('Unsubscribe failed:', err);
    }
  }, []);

  const sendTest = useCallback(async (): Promise<void> => {
    try {
      const reg = await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.getSubscription();
      if (!sub) { toast.error(t('notifNotSubscribed')); return; }
      const json = sub.toJSON();
      await fetch(`${BACKEND_URL}/api/push/test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ endpoint: json.endpoint }),
      });
      toast.success(t('notifTestSent') + ' ✅');
    } catch (_e) {
      toast.error(t('notifTestFailed'));
    }
  }, []);

  return { ...state, subscribe, unsubscribe, sendTest };
}
