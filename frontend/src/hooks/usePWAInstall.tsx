import { useState, useEffect, useRef } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export function usePWAInstall() {
  const [canInstall, setCanInstall] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);
  const [showBanner, setShowBanner] = useState(false);
  const promptRef = useRef<BeforeInstallPromptEvent | null>(null);

  useEffect(() => {
    // Check if already installed
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    const isIOSStandalone = (navigator as any).standalone === true;

    if (isStandalone || isIOSStandalone) {
      setIsInstalled(true);
      return;
    }

    // Check if already dismissed
    const dismissed = sessionStorage.getItem('pwa_install_dismissed');
    const dismissedTime = parseInt(localStorage.getItem('pwa_install_dismissed_time') || '0');
    const DAY_MS = 24 * 60 * 60 * 1000;
    if (dismissed && Date.now() - dismissedTime < DAY_MS) return;

    const handler = (e: Event) => {
      e.preventDefault();
      promptRef.current = e as BeforeInstallPromptEvent;
      setCanInstall(true);
      // Show banner immediately
      setTimeout(() => setShowBanner(true), 2000);
    };

    window.addEventListener('beforeinstallprompt', handler as EventListener);

    // iOS doesn't fire beforeinstallprompt — show manual instructions
    if (isIOS && !isIOSStandalone) {
      setTimeout(() => { setShowBanner(true); setCanInstall(true); }, 3000);
    }

    return () => window.removeEventListener('beforeinstallprompt', handler as EventListener);
  }, []);

  const install = async (): Promise<boolean> => {
    if (!promptRef.current) return false;
    try {
      await promptRef.current.prompt();
      const { outcome } = await promptRef.current.userChoice;
      if (outcome === 'accepted') {
        setIsInstalled(true);
        setShowBanner(false);
        setCanInstall(false);
        promptRef.current = null;
        return true;
      }
    } catch (_e) { /* ignore */ }
    return false;
  };

  const dismiss = () => {
    setShowBanner(false);
    sessionStorage.setItem('pwa_install_dismissed', '1');
    localStorage.setItem('pwa_install_dismissed_time', String(Date.now()));
  };

  return { canInstall, isInstalled, showBanner, install, dismiss };
}
