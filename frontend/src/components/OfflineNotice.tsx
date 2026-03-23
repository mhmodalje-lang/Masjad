import { useState, useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { WifiOff } from 'lucide-react';

export default function OfflineNotice() {
  const { t, dir } = useLocale();
  const [isOffline, setIsOffline] = useState(!navigator.onLine);

  useEffect(() => {
    const onOffline = () => setIsOffline(true);
    const onOnline = () => setIsOffline(false);
    window.addEventListener('offline', onOffline);
    window.addEventListener('online', onOnline);
    return () => {
      window.removeEventListener('offline', onOffline);
      window.removeEventListener('online', onOnline);
    };
  }, []);

  if (!isOffline) return null;

  return (
    <div className="fixed top-0 left-0 right-0 z-[70] bg-amber-600 text-white text-center py-2 px-4 flex items-center justify-center gap-2 text-xs font-bold shadow-lg" dir={dir}>
      <WifiOff className="h-3.5 w-3.5 shrink-0" />
      <span>{t('offlineNotice')}</span>
    </div>
  );
}
