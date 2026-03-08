import { useState, useEffect } from 'react';
import { X, Download } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';

interface BeforeInstallPromptEvent extends Event {
  prompt(): Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export default function InstallBanner() {
  const [show, setShow] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);

  useEffect(() => {
    // Don't show if already installed or dismissed
    if (window.matchMedia('(display-mode: standalone)').matches) return;
    if (localStorage.getItem('install-banner-dismissed')) return;

    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
    };
    window.addEventListener('beforeinstallprompt', handler);

    // Show after 3 seconds
    const timer = setTimeout(() => setShow(true), 3000);

    return () => {
      window.removeEventListener('beforeinstallprompt', handler);
      clearTimeout(timer);
    };
  }, []);

  const dismiss = () => {
    setShow(false);
    localStorage.setItem('install-banner-dismissed', 'true');
  };

  const handleInstall = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      if (outcome === 'accepted') dismiss();
      setDeferredPrompt(null);
    }
  };

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 100, opacity: 0 }}
          className="fixed bottom-20 left-3 right-3 z-50 rounded-2xl bg-primary p-4 shadow-lg flex items-center gap-3"
          dir="rtl"
        >
          <img src="/pwa-icon-192.png" alt="تأكد" className="h-12 w-12 rounded-xl shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold text-primary-foreground">أضف تأكد لشاشتك الرئيسية</p>
            <p className="text-xs text-primary-foreground/70 truncate">وصول سريع + يعمل بدون إنترنت</p>
          </div>
          {deferredPrompt ? (
            <button onClick={handleInstall} className="shrink-0 rounded-xl bg-primary-foreground px-3 py-2 text-xs font-bold text-primary">
              تثبيت
            </button>
          ) : (
            <Link to="/install" onClick={dismiss} className="shrink-0 rounded-xl bg-primary-foreground px-3 py-2 text-xs font-bold text-primary">
              تثبيت
            </Link>
          )}
          <button onClick={dismiss} className="shrink-0 p-1">
            <X className="h-4 w-4 text-primary-foreground/60" />
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
