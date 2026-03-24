import { ReactNode, useEffect, useCallback, useState } from 'react';
import { BottomNav } from './BottomNav';
import { TopNav } from './TopNav';
import InstallBanner from '@/components/InstallBanner';
import { PopUnderLoader } from '@/components/AdBanner';
import { useDailyReminders } from '@/hooks/useDailyReminders';
import { PWAUpdatePrompt } from '@/components/PWAUpdatePrompt';
import { preloadSelectedAthan } from '@/lib/athanAudio';
import { useLocation } from 'react-router-dom';
import { isNativeApp } from '@/lib/nativeBridge';
import { PullToRefresh } from '@/components/PullToRefresh';

// Pages that have their own headers (no top nav needed)
const CUSTOM_HEADER_PAGES = ['/auth', '/admin', '/stories', '/explore', '/profile', '/more', '/about', '/privacy', '/contact', '/donations', '/social-profile', '/reels', '/create-post', '/terms', '/delete-data', '/content-policy'];

export function AppLayout({ children }: { children: ReactNode }) {
  useDailyReminders();
  const location = useLocation();
  const showTopNav = !CUSTOM_HEADER_PAGES.some(p => location.pathname.startsWith(p));
  const isNative = isNativeApp();

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

  // Pull-to-refresh handler
  const handleRefresh = useCallback(async () => {
    // Reload current page data by dispatching a custom event
    document.dispatchEvent(new CustomEvent('pull-refresh'));
    // Small delay for visual feedback
    await new Promise(resolve => setTimeout(resolve, 800));
  }, []);

  return (
    <div className="min-h-screen w-full overflow-x-hidden bg-background native-app-container">
      {showTopNav && <TopNav />}
      <PullToRefresh onRefresh={handleRefresh}>
        <main className="w-full overflow-x-hidden pb-safe-nav">{children}</main>
      </PullToRefresh>
      <BottomNav />
      {/* Web-only components - hidden in native app mode */}
      {!isNative && <InstallBanner />}
      {!isNative && <PopUnderLoader />}
      {!isNative && <PWAUpdatePrompt />}
    </div>
  );
}
