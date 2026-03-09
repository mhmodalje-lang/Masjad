import { useEffect, forwardRef } from 'react';
import { toast } from 'sonner';

export const PWAUpdatePrompt = forwardRef<HTMLDivElement>(function PWAUpdatePrompt(_, ref) {
  useEffect(() => {
    if (!('serviceWorker' in navigator)) return;

    const checkForUpdate = async () => {
      const reg = await navigator.serviceWorker.getRegistration();
      if (reg) {
        reg.update().catch(() => {});
      }
    };

    const interval = setInterval(checkForUpdate, 30 * 60 * 1000);

    let refreshing = false;
    const onControllerChange = () => {
      if (refreshing) return;
      refreshing = true;
      window.location.reload();
    };

    navigator.serviceWorker.addEventListener('controllerchange', onControllerChange);

    const detectWaiting = async () => {
      const reg = await navigator.serviceWorker.getRegistration();
      if (!reg) return;

      const showUpdateToast = () => {
        toast('🔄 تحديث جديد متوفر', {
          description: 'اضغط لتحديث التطبيق الآن',
          duration: Infinity,
          action: {
            label: 'تحديث الآن',
            onClick: () => {
              reg.waiting?.postMessage({ type: 'SKIP_WAITING' });
            },
          },
        });
      };

      if (reg.waiting) {
        showUpdateToast();
      }

      reg.addEventListener('updatefound', () => {
        const newSW = reg.installing;
        if (!newSW) return;
        newSW.addEventListener('statechange', () => {
          if (newSW.state === 'installed' && navigator.serviceWorker.controller) {
            showUpdateToast();
          }
        });
      });
    };

    detectWaiting();

    return () => {
      clearInterval(interval);
      navigator.serviceWorker.removeEventListener('controllerchange', onControllerChange);
    };
  }, []);

  return <div ref={ref} style={{ display: 'none' }} />;
});
