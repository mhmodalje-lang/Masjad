import { ReactNode, useEffect } from 'react';
import { BottomNav } from './BottomNav';
import { TopNav } from './TopNav';
import InstallBanner from '@/components/InstallBanner';
import { PopUnderLoader } from '@/components/AdBanner';
import { useDailyReminders } from '@/hooks/useDailyReminders';
import { PWAUpdatePrompt } from '@/components/PWAUpdatePrompt';
import { preloadSelectedAthan } from '@/lib/athanAudio';
import { useLocation } from 'react-router-dom';

// Pages that have their own headers (no top nav needed)
const CUSTOM_HEADER_PAGES = ['/auth', '/admin'];

export function AppLayout({ children }: { children: ReactNode }) {
  useDailyReminders();
  const location = useLocation();
  const showTopNav = !CUSTOM_HEADER_PAGES.some(p => location.pathname.startsWith(p));

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
      <main className="w-full overflow-x-hidden pb-safe">{children}</main>
      <BottomNav />
      <InstallBanner />
      <PopUnderLoader />
      <PWAUpdatePrompt />
    </div>
  );
}
