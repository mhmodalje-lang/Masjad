import { useState, useEffect } from 'react';
import { WifiOff, Wifi } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function OfflineIndicator() {
  const [isOffline, setIsOffline] = useState(!navigator.onLine);
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    const goOffline = () => { setIsOffline(true); setShowBanner(true); };
    const goOnline = () => { 
      setIsOffline(false); 
      setShowBanner(true);
      setTimeout(() => setShowBanner(false), 3000);
    };

    window.addEventListener('offline', goOffline);
    window.addEventListener('online', goOnline);

    return () => {
      window.removeEventListener('offline', goOffline);
      window.removeEventListener('online', goOnline);
    };
  }, []);

  return (
    <AnimatePresence>
      {showBanner && (
        <motion.div
          initial={{ y: -60, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -60, opacity: 0 }}
          className={`fixed top-0 left-0 right-0 z-[9999] px-4 py-2 flex items-center justify-center gap-2 text-xs font-bold ${
            isOffline 
              ? 'bg-amber-500 text-black' 
              : 'bg-green-500 text-white'
          }`}
        >
          {isOffline ? (
            <>
              <WifiOff className="w-3.5 h-3.5" />
              <span>غير متصل بالإنترنت - تستخدم المحتوى المحفوظ</span>
            </>
          ) : (
            <>
              <Wifi className="w-3.5 h-3.5" />
              <span>تم استعادة الاتصال</span>
            </>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
