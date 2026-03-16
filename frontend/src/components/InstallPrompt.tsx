import { useState, useEffect } from 'react';
import { X, Download, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function InstallPrompt() {
  const [show, setShow] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);

  useEffect(() => {
    // Check if already dismissed or installed
    const dismissed = localStorage.getItem('install_prompt_dismissed');
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
    
    if (dismissed || isStandalone) return;

    // Show after 3 seconds delay for better UX
    const timer = setTimeout(() => {
      setShow(true);
    }, 3000);

    // Listen for beforeinstallprompt
    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };
    window.addEventListener('beforeinstallprompt', handler);

    return () => {
      clearTimeout(timer);
      window.removeEventListener('beforeinstallprompt', handler);
    };
  }, []);

  const handleInstall = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      if (outcome === 'accepted') {
        localStorage.setItem('install_prompt_dismissed', 'true');
        setShow(false);
      }
    } else {
      // For iOS/Safari - show instructions
      const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
      if (isIOS) {
        alert('لتثبيت التطبيق:\n1. اضغط على زر المشاركة 📤\n2. اختر "إضافة إلى الشاشة الرئيسية"');
      } else {
        // Navigate to install page
        window.location.href = '/install';
      }
    }
  };

  const handleDismiss = () => {
    localStorage.setItem('install_prompt_dismissed', 'true');
    setShow(false);
  };

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 100, opacity: 0 }}
          transition={{ type: 'spring', damping: 20, stiffness: 300 }}
          className="fixed bottom-20 left-3 right-3 z-[999]"
          dir="rtl"
        >
          <div className="bg-gradient-to-r from-primary/95 to-amber-600/95 backdrop-blur-xl rounded-2xl shadow-2xl shadow-primary/30 p-4 border border-primary/20">
            <button onClick={handleDismiss} className="absolute top-2 left-2 p-1.5 rounded-full bg-white/20 text-white">
              <X className="h-3.5 w-3.5" />
            </button>
            <div className="flex items-center gap-3">
              <div className="h-12 w-12 rounded-xl bg-white/20 flex items-center justify-center shrink-0">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-bold text-white">ثبّت أذان وحكاية</p>
                <p className="text-[11px] text-white/70 mt-0.5">احصل على إشعارات الأذان والتذكيرات اليومية</p>
              </div>
              <button onClick={handleInstall}
                className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-white text-primary text-xs font-bold shrink-0 active:scale-95 transition-transform shadow-md">
                <Download className="h-3.5 w-3.5" />
                تثبيت
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
