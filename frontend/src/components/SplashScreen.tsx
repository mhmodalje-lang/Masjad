import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import i18n from '@/lib/i18nConfig';

export default function SplashScreen({ onComplete }: { onComplete: () => void }) {
  const [visible, setVisible] = useState(true);
  const isDark = document.documentElement.classList.contains('dark');

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      setTimeout(onComplete, 300);
    }, 600);
    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-[9999] flex flex-col items-center justify-center"
          style={{ background: isDark
            ? 'linear-gradient(135deg, #0f1520 0%, #1a2332 40%, #0d1b2a 100%)'
            : 'linear-gradient(135deg, #f5f0e8 0%, #e8e0d0 40%, #f0ead8 100%)'
          }}
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3, ease: 'easeInOut' }}
        >
          <div className="absolute inset-0 islamic-pattern opacity-20" />

          <motion.div
            className="absolute w-72 h-72 rounded-full"
            style={{
              background: isDark
                ? 'radial-gradient(circle, rgba(16,185,129,0.2) 0%, transparent 70%)'
                : 'radial-gradient(circle, rgba(16,185,129,0.15) 0%, transparent 70%)',
            }}
            animate={{ scale: [1, 1.3, 1], opacity: [0.3, 0.6, 0.3] }}
            transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
          />

          <div className="relative z-10 mb-6">
            <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
              <path
                d="M40 4C22.3 4 8 18.3 8 36s14.3 32 32 32c6.2 0 12-1.8 16.9-4.8C50.4 67 42 72 32.5 72 16.2 72 3 58.8 3 42.5S16.2 13 32.5 13c3.5 0 6.8.5 10 1.5C39.8 8.5 35.5 4 40 4z"
                fill="#10b981"
              />
              <circle cx="58" cy="18" r="4" fill="#eab308" />
            </svg>
          </div>

          <h1 className={`relative z-10 text-3xl font-bold mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>{i18n.t('appTitle')}</h1>
          <p className={`relative z-10 text-sm ${isDark ? 'text-white/60' : 'text-gray-500'}`}>{i18n.t('appSubtitle')}</p>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
