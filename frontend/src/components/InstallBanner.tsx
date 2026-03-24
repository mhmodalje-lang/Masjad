import { useState, useEffect } from 'react';
import { X, Download } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLocale } from '@/hooks/useLocale';

interface BeforeInstallPromptEvent extends Event {
  prompt(): Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

function isInStandaloneMode() {
  return window.matchMedia('(display-mode: standalone)').matches ||
    (navigator as any).standalone === true;
}

const DISMISSED_KEY = 'install-banner-dismissed';

export default function InstallBanner() {
  const { t, dir } = useLocale();
  const [show, setShow] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);

  useEffect(() => {
    // Hide in native app mode (Capacitor) - not needed
    try {
      const { Capacitor } = require('@capacitor/core');
      if (Capacitor.isNativePlatform()) return;
    } catch {}
    if (isInStandaloneMode()) return;
    if (localStorage.getItem(DISMISSED_KEY)) return;

    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      setShow(true);
    };
    window.addEventListener('beforeinstallprompt', handler);

    return () => {
      window.removeEventListener('beforeinstallprompt', handler);
    };
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === 'accepted') {
      setShow(false);
    }
    setDeferredPrompt(null);
  };

  const dismiss = () => {
    localStorage.setItem(DISMISSED_KEY, '1');
    setShow(false);
  };

  if (typeof window !== 'undefined' && isInStandaloneMode()) {
    return null;
  }

  return (
    <AnimatePresence>
      {show && deferredPrompt && (
        <motion.div
          key="install-banner"
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 100, opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          className="fixed bottom-20 left-4 right-4 z-[70] rounded-2xl bg-card border border-border p-4 shadow-2xl"
          dir={dir}
        >
          <button
            onClick={dismiss}
            className="absolute top-3 start-3 p-1 rounded-full hover:bg-muted transition-colors"
          >
            <X className="h-4 w-4 text-muted-foreground" />
          </button>

          <div className="flex items-center gap-3">
            <img src="/pwa-icon-192.png" alt="Athan & Hikaya" className="h-12 w-12 rounded-xl shadow" />
            <div className="flex-1 min-w-0">
              <h3 className="text-sm font-bold text-foreground">{t('installAppTitle')}</h3>
              <p className="text-xs text-muted-foreground mt-0.5">{t('installAppSubtitle')}</p>
            </div>
            <button
              onClick={handleInstall}
              className="shrink-0 rounded-xl bg-primary px-4 py-2.5 text-sm font-bold text-primary-foreground shadow active:scale-95 transition-transform flex items-center gap-1.5"
            >
              <Download className="h-4 w-4" />
              {t('installBtn')}
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
