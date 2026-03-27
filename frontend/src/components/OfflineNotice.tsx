import { useState, useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { WifiOff, Wifi } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function OfflineNotice() {
  const { t, dir } = useLocale();
  const [isOffline, setIsOffline] = useState(!navigator.onLine);
  const [showReconnected, setShowReconnected] = useState(false);
  const [wasOffline, setWasOffline] = useState(false);

  useEffect(() => {
    const onOffline = () => {
      setIsOffline(true);
      setWasOffline(true);
    };
    const onOnline = () => {
      setIsOffline(false);
      if (wasOffline) {
        setShowReconnected(true);
        setTimeout(() => setShowReconnected(false), 3000);
      }
    };
    window.addEventListener('offline', onOffline);
    window.addEventListener('online', onOnline);
    return () => {
      window.removeEventListener('offline', onOffline);
      window.removeEventListener('online', onOnline);
    };
  }, [wasOffline]);

  return (
    <AnimatePresence>
      {isOffline && (
        <motion.div
          initial={{ y: -60, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -60, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 25 }}
          className="fixed top-0 left-0 right-0 z-[70] bg-amber-600 text-white text-center py-2.5 px-4 flex items-center justify-center gap-2 text-xs font-bold shadow-lg"
          dir={dir}
          style={{ paddingTop: 'max(env(safe-area-inset-top, 0px), 8px)' }}
        >
          <WifiOff className="h-3.5 w-3.5 shrink-0 animate-pulse" />
          <span>{t('offlineNotice') || 'غير متصل بالإنترنت - المحتوى المحفوظ متاح'}</span>
        </motion.div>
      )}
      {showReconnected && !isOffline && (
        <motion.div
          initial={{ y: -60, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -60, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 25 }}
          className="fixed top-0 left-0 right-0 z-[70] bg-emerald-600 text-white text-center py-2.5 px-4 flex items-center justify-center gap-2 text-xs font-bold shadow-lg"
          dir={dir}
          style={{ paddingTop: 'max(env(safe-area-inset-top, 0px), 8px)' }}
        >
          <Wifi className="h-3.5 w-3.5 shrink-0" />
          <span>تم استعادة الاتصال ✓</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
