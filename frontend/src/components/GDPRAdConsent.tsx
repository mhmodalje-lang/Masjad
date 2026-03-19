import { useState, useEffect } from 'react';
import { useAdConfig } from '@/hooks/useAdConfig';
import { Shield, X } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';

export default function GDPRAdConsent() {
  const adConfig = useAdConfig();
  const { t, dir } = useLocale();
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (!adConfig.gdpr_consent_required) return;
    const consent = localStorage.getItem('gdpr-ad-consent');
    if (!consent) {
      const timer = setTimeout(() => setShow(true), 2500);
      return () => clearTimeout(timer);
    }
  }, [adConfig.gdpr_consent_required]);

  const handleConsent = (accepted: boolean) => {
    localStorage.setItem('gdpr-ad-consent', accepted ? 'accepted' : 'rejected');
    localStorage.setItem('gdpr-ad-consent-date', new Date().toISOString());
    if (accepted) {
      localStorage.setItem('personalized-ads', 'true');
    } else {
      localStorage.setItem('personalized-ads', 'false');
    }
    setShow(false);
  };

  if (!show) return null;

  return (
    <div data-testid="gdpr-consent-overlay" className="fixed inset-x-0 bottom-0 z-[9999] flex items-end justify-center p-4 animate-in fade-in duration-300" dir={dir}>
      <div className="w-full max-w-lg bg-card border border-border/60 rounded-2xl p-5 shadow-2xl animate-in slide-in-from-bottom duration-500">
        <div className="flex items-start gap-3 mb-4">
          <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-500 shrink-0">
            <Shield className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <h3 className="text-sm font-bold text-foreground mb-1">{t('gdprTitle')}</h3>
            <p className="text-xs text-muted-foreground leading-relaxed">
              {t('gdprDesc')}
            </p>
          </div>
          <button data-testid="gdpr-dismiss-btn" onClick={() => handleConsent(false)} className="p-1 rounded-lg text-muted-foreground hover:text-foreground shrink-0">
            <X className="h-4 w-4" />
          </button>
        </div>
        
        <div className="space-y-2 mb-4 text-xs text-muted-foreground bg-muted/30 rounded-xl p-3">
          <p className="font-medium text-foreground">{t('gdprCollect')}</p>
          <ul className="space-y-1 list-disc list-inside">
            <li>{t('gdprCollect1')}</li>
            <li>{t('gdprCollect2')}</li>
            <li>{t('gdprCollect3')}</li>
          </ul>
        </div>

        <div className="flex gap-2">
          <button
            data-testid="gdpr-accept-btn"
            onClick={() => handleConsent(true)}
            className="flex-1 px-4 py-2.5 rounded-xl bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-700 transition-colors"
          >
            {t('gdprAccept')}
          </button>
          <button
            data-testid="gdpr-reject-btn"
            onClick={() => handleConsent(false)}
            className="flex-1 px-4 py-2.5 rounded-xl bg-muted text-muted-foreground text-xs font-medium hover:bg-muted/80 transition-colors"
          >
            {t('gdprReject')}
          </button>
        </div>
        
        <p className="text-[10px] text-muted-foreground/60 text-center mt-3">
          {t('gdprChangeNote')}
        </p>
      </div>
    </div>
  );
}
