import { useEffect, useState, forwardRef } from 'react';
import { useLocale } from '@/hooks/useLocale';

/**
 * PWA Update Prompt - Shows a user-friendly update banner instead of auto-reloading.
 * Checks for service worker updates but does NOT auto-reload.
 * State is preserved via localStorage.
 */
export const PWAUpdatePrompt = forwardRef<HTMLDivElement>(function PWAUpdatePrompt(_, ref) {
  const [updateAvailable, setUpdateAvailable] = useState(false);

  useEffect(() => {
    if (!('serviceWorker' in navigator)) return;

    let refreshing = false;

    // When new SW takes control, reload once (only when user explicitly clicks update)
    let userInitiatedUpdate = false;
    const onControllerChange = () => {
      if (refreshing || !userInitiatedUpdate) return;
      refreshing = true;
      window.location.reload();
    };
    navigator.serviceWorker.addEventListener('controllerchange', onControllerChange);

    // Check for updates on visibility change only (user returns to app)
    const checkForUpdate = async () => {
      try {
        const reg = await navigator.serviceWorker.getRegistration();
        if (reg) {
          await reg.update();
          if (reg.waiting) {
            setUpdateAvailable(true);
          }
        }
      } catch { /* ignore */ }
    };

    // Handle case where SW installs while page is open
    const handleWaiting = async () => {
      const reg = await navigator.serviceWorker.getRegistration();
      if (!reg) return;

      if (reg.waiting) {
        setUpdateAvailable(true);
      }

      reg.addEventListener('updatefound', () => {
        const newSW = reg.installing;
        if (!newSW) return;
        newSW.addEventListener('statechange', () => {
          if (newSW.state === 'installed' && navigator.serviceWorker.controller) {
            setUpdateAvailable(true);
          }
        });
      });
    };

    handleWaiting();

    // Check on visibility change (user returns to app) - NOT on interval
    const onVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        checkForUpdate();
      }
    };
    document.addEventListener('visibilitychange', onVisibilityChange);

    return () => {
      navigator.serviceWorker.removeEventListener('controllerchange', onControllerChange);
      document.removeEventListener('visibilitychange', onVisibilityChange);
    };
  }, []);

  const handleUpdate = async () => {
    try {
      const reg = await navigator.serviceWorker.getRegistration();
      if (reg?.waiting) {
        // Mark as user-initiated before triggering SW
        (window as any).__userInitiatedSWUpdate = true;
        reg.waiting.postMessage({ type: 'SKIP_WAITING' });
      }
    } catch {
      window.location.reload();
    }
  };

  const handleDismiss = () => {
    setUpdateAvailable(false);
  };

  if (!updateAvailable) return <div ref={ref} style={{ display: 'none' }} />;

  return (
    <div ref={ref} className="fixed bottom-20 left-4 right-4 z-[100] animate-in slide-in-from-bottom-4">
      <div className="rounded-2xl bg-primary/95 backdrop-blur-xl p-4 shadow-2xl flex items-center justify-between gap-3 border border-primary/20">
        <div className="flex-1 min-w-0">
          <p className="text-sm font-bold text-primary-foreground">Update Available</p>
          <p className="text-xs text-primary-foreground/70 mt-0.5">A new version is ready</p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={handleDismiss}
            className="px-3 py-1.5 rounded-xl text-xs font-bold text-primary-foreground/70 hover:text-primary-foreground transition-colors"
          >
            Later
          </button>
          <button
            onClick={handleUpdate}
            className="px-4 py-1.5 rounded-xl bg-white/20 text-xs font-bold text-primary-foreground hover:bg-white/30 transition-colors active:scale-95"
          >
            Update
          </button>
        </div>
      </div>
    </div>
  );
});
