import { ReactNode, useEffect, useState, useCallback } from 'react';
import { BottomNav } from './BottomNav';
import { TopNav } from './TopNav';
import { PWAUpdatePrompt } from '@/components/PWAUpdatePrompt';
import OfflineIndicator from '@/components/OfflineIndicator';
import FullScreenAthan from '@/components/FullScreenAthan';
import { preloadSelectedAthan } from '@/lib/athanAudio';
import { setAthanAlertCallback } from '@/lib/prayerNotifications';
import { useLocation } from 'react-router-dom';
import { isNativeApp } from '@/lib/nativeBridge';

// Pages that have their own headers (no top nav needed)
const CUSTOM_HEADER_PAGES = ['/auth', '/admin', '/stories', '/explore', '/profile', '/more', '/about', '/privacy', '/contact', '/donations', '/social-profile', '/reels', '/create-post', '/terms', '/delete-data', '/content-policy'];

export function AppLayout({ children }: { children: ReactNode }) {
  const location = useLocation();
  const showTopNav = !CUSTOM_HEADER_PAGES.some(p => location.pathname.startsWith(p));
  const isNative = isNativeApp();
  const [alertPrayer, setAlertPrayer] = useState<{ key: string; time: string } | null>(null);

  // Register global athan alert callback — works from ANY page
  useEffect(() => {
    const callback = (prayerKey: string, prayerTime: string) => {
      setAlertPrayer({ key: prayerKey, time: prayerTime });
    };
    setAthanAlertCallback(callback);

    // Also listen for SW messages
    if ('serviceWorker' in navigator) {
      const handler = (event: MessageEvent) => {
        if (event.data?.type === 'ATHAN_ALERT') {
          setAlertPrayer({ key: event.data.prayer, time: event.data.time });
        }
      };
      navigator.serviceWorker.addEventListener('message', handler);
      return () => {
        setAthanAlertCallback(null);
        navigator.serviceWorker.removeEventListener('message', handler);
      };
    }

    return () => setAthanAlertCallback(null);
  }, []);

  const handleDismissAthan = useCallback(() => {
    setAlertPrayer(null);
  }, []);

  useEffect(() => {
    const handler = () => {
      preloadSelectedAthan(true);
      window.removeEventListener('click', handler);
      window.removeEventListener('touchstart', handler);
    };
    window.addEventListener('click', handler, { once: true });
    window.addEventListener('touchstart', handler, { once: true });
    return () => {
      window.removeEventListener('click', handler);
      window.removeEventListener('touchstart', handler);
    };
  }, []);

  return (
    <div className="min-h-screen w-full overflow-x-hidden bg-background">
      {showTopNav && <TopNav />}
      <main className="w-full overflow-x-hidden pb-20">{children}</main>
      <BottomNav />
      {/* Web-only components - hidden in native app mode */}
      {!isNative && <PWAUpdatePrompt />}
      <OfflineIndicator />
      {/* Full-Screen Athan — works on ALL pages */}
      <FullScreenAthan
        prayerKey={alertPrayer?.key || null}
        prayerTime={alertPrayer?.time || ''}
        onDismiss={handleDismissAthan}
      />
    </div>
  );
}
