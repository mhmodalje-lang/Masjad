import { Link } from 'react-router-dom';
import { useLocale } from '@/hooks/useLocale';

/**
 * PolicyFooter - Shows privacy/terms/contact links at bottom of policy & public pages
 * Required for Google Ads compliance and App Store review
 */
export default function PolicyFooter() {
  const { t, dir } = useLocale();

  return (
    <footer className="w-full border-t border-border/10 bg-muted/30 mt-8" dir={dir}>
      <div className="max-w-3xl mx-auto px-5 py-6">
        <div className="flex flex-wrap items-center justify-center gap-4 text-xs text-muted-foreground">
          <Link to="/privacy" className="hover:text-primary transition-colors">{t('privacyPolicy')}</Link>
          <span className="text-border">|</span>
          <Link to="/terms" className="hover:text-primary transition-colors">{t('termsOfService')}</Link>
          <span className="text-border">|</span>
          <Link to="/about" className="hover:text-primary transition-colors">{t('aboutUs')}</Link>
          <span className="text-border">|</span>
          <Link to="/contact" className="hover:text-primary transition-colors">{t('contactUs')}</Link>
          <span className="text-border">|</span>
          <Link to="/content-policy" className="hover:text-primary transition-colors">{t('contentPolicyLink')}</Link>
          <span className="text-border">|</span>
          <Link to="/delete-data" className="hover:text-primary transition-colors">{t('dataDeletionTitle')}</Link>
        </div>
        <p className="text-center text-[10px] text-muted-foreground/50 mt-3">
          © {new Date().getFullYear()} أذان وحكاية - Azan wa Hikaya. {t('allRightsReserved')}
        </p>
      </div>
    </footer>
  );
}
