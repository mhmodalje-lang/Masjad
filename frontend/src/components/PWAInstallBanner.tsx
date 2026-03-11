import { motion, AnimatePresence } from 'framer-motion';
import { Download, X, Share, ArrowDown } from 'lucide-react';
import { usePWAInstall } from '@/hooks/usePWAInstall';

export function PWAInstallBanner() {
  const { showBanner, canInstall, isInstalled, install, dismiss } = usePWAInstall();
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);

  if (isInstalled || !showBanner) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 100, opacity: 0 }}
        transition={{ type: 'spring', damping: 25 }}
        className="fixed bottom-24 left-4 right-4 z-50 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-2xl shadow-2xl p-4"
        dir="rtl"
      >
        <button
          onClick={dismiss}
          className="absolute top-3 start-3 h-7 w-7 rounded-full bg-white/20 flex items-center justify-center"
        >
          <X className="h-4 w-4 text-white" />
        </button>

        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-2xl bg-white/20 flex items-center justify-center shrink-0">
            <img src="/pwa-icon-192.png" alt="أيقونة" className="h-10 w-10 rounded-xl" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-white font-bold text-sm font-arabic">المؤذن العالمي</p>
            <p className="text-white/80 text-xs">ثبّت التطبيق للوصول السريع وإشعارات الأذان</p>
          </div>
        </div>

        {isIOS ? (
          <div className="mt-3 p-3 bg-white/10 rounded-xl">
            <p className="text-white text-xs text-center font-arabic">
              اضغط على <Share className="inline h-4 w-4" /> ثم "إضافة إلى الشاشة الرئيسية"
            </p>
          </div>
        ) : (
          <button
            onClick={install}
            className="mt-3 w-full bg-white text-emerald-700 font-bold rounded-xl py-2.5 text-sm flex items-center justify-center gap-2"
          >
            <Download className="h-4 w-4" />
            تثبيت التطبيق مجاناً
          </button>
        )}
      </motion.div>
    </AnimatePresence>
  );
}
