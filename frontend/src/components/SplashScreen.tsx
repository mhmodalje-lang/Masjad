import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import i18n from '@/lib/i18nConfig';
import { isRTL } from '@/lib/i18nConfig';
import { isNativeApp } from '@/lib/nativeBridge';

export default function SplashScreen({ onComplete }: { onComplete: () => void }) {
  const [visible, setVisible] = useState(true);
  const isDark = document.documentElement.classList.contains('dark');
  const currentLang = i18n.language || 'ar';
  const rtl = isRTL(currentLang);
  const isNative = isNativeApp();

  useEffect(() => {
    // Much shorter splash - get user to content ASAP
    const duration = isNative ? 200 : 350;
    const timer = setTimeout(() => {
      setVisible(false);
      setTimeout(onComplete, 150);
    }, duration);
    return () => clearTimeout(timer);
  }, [onComplete, isNative]);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-[9999] flex flex-col items-center justify-center"
          dir={rtl ? 'rtl' : 'ltr'}
          style={{ 
            background: isDark
              ? 'linear-gradient(135deg, #071a12 0%, #0d2a1c 40%, #051410 100%)'
              : 'linear-gradient(135deg, #F9FAFB 0%, #F0F5F0 40%, #F9FAFB 100%)',
            // Ensure it covers safe areas on notched devices
            paddingTop: 'env(safe-area-inset-top, 0px)',
            paddingBottom: 'env(safe-area-inset-bottom, 0px)',
          }}
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3, ease: 'easeInOut' }}
        >
          <div className="absolute inset-0 islamic-pattern opacity-20" />

          {/* Ambient glow */}
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

          {/* App Icon */}
          <motion.div 
            className="relative z-10 mb-6"
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: 'spring', stiffness: 200, damping: 15 }}
          >
            <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
              <path
                d="M40 4C22.3 4 8 18.3 8 36s14.3 32 32 32c6.2 0 12-1.8 16.9-4.8C50.4 67 42 72 32.5 72 16.2 72 3 58.8 3 42.5S16.2 13 32.5 13c3.5 0 6.8.5 10 1.5C39.8 8.5 35.5 4 40 4z"
                fill="hsl(var(--mystic-moss))"
              />
              <circle cx="58" cy="18" r="4" fill="#D4AF37" />
            </svg>
          </motion.div>

          {/* App Name with slide-up animation */}
          <motion.h1 
            className={`relative z-10 text-3xl font-bold mb-3 text-center px-8 ${isDark ? 'text-white' : 'text-gray-900'}`}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.1, duration: 0.4 }}
          >
            {i18n.t('appTitle')}
          </motion.h1>

          {/* Subtitle */}
          <motion.p 
            className={`relative z-10 text-sm text-center px-10 max-w-[320px] leading-relaxed ${isDark ? 'text-white/60' : 'text-gray-500'}`}
            initial={{ y: 15, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.4 }}
          >
            {i18n.t('appSubtitle')}
          </motion.p>

          {/* Version number (native apps show this) */}
          <motion.p
            className={`absolute bottom-8 text-xs ${isDark ? 'text-white/30' : 'text-gray-400'}`}
            style={{ paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            v1.0.0
          </motion.p>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
