import { useState, useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { Cookie, X } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function CookieConsent() {
  const { t, dir } = useLocale();
  const [show, setShow] = useState(false);

  useEffect(() => {
    // Hide in native app mode - cookies are handled by the native wrapper
    try {
      const { Capacitor } = require('@capacitor/core');
      if (Capacitor.isNativePlatform()) return;
    } catch {}
    const consent = localStorage.getItem('cookie-consent');
    if (!consent) {
      // Small delay so it doesn't flash on load
      const timer = setTimeout(() => setShow(true), 1500);
      return () => clearTimeout(timer);
    }
  }, []);

  const accept = () => {
    localStorage.setItem('cookie-consent', 'accepted');
    localStorage.setItem('cookie-consent-date', new Date().toISOString());
    setShow(false);
  };

  const reject = () => {
    localStorage.setItem('cookie-consent', 'rejected');
    localStorage.setItem('cookie-consent-date', new Date().toISOString());
    setShow(false);
  };

  if (!show) return null;

  return (
    <div data-testid="cookie-consent-banner" className="fixed bottom-16 left-0 right-0 z-[55] px-3 pb-2 animate-in slide-in-from-bottom duration-500" dir={dir}>
      <div className="max-w-lg mx-auto bg-card border border-border/60 rounded-2xl p-4 shadow-2xl shadow-black/20 backdrop-blur-xl">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-full bg-primary/10 text-primary shrink-0 mt-0.5">
            <Cookie className="h-4 w-4" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs text-muted-foreground leading-relaxed mb-3">
              {t('cookieConsentMessage')}{' '}
              <Link to="/privacy" className="text-primary underline">{t('privacyPolicy')}</Link>
            </p>
            <div className="flex items-center gap-2">
              <button
                data-testid="cookie-accept-btn"
                onClick={accept}
                className="px-4 py-1.5 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:opacity-90 transition-opacity"
              >
                {t('acceptCookies')}
              </button>
              <button
                data-testid="cookie-reject-btn"
                onClick={reject}
                className="px-4 py-1.5 rounded-xl bg-muted text-muted-foreground text-xs font-medium hover:bg-muted/80 transition-colors"
              >
                {t('rejectCookies')}
              </button>
            </div>
          </div>
          <button data-testid="cookie-dismiss-btn" onClick={reject} className="p-1 rounded-lg text-muted-foreground hover:text-foreground shrink-0">
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
