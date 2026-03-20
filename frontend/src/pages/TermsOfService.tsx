import { Link } from 'react-router-dom';
import { ArrowRight, ArrowLeft, FileText, AlertCircle, ShieldCheck, Ban, Scale, Globe } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';

export default function TermsOfService() {
  const { t, dir, isRTL } = useLocale();
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir} data-testid="terms-page">
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center gap-3">
        <Link to="/more" className="p-2 rounded-xl bg-muted/50 active:scale-95"><BackArrow className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">{t('termsOfService')}</h1>
      </div>
      <div className="px-5 py-6 space-y-5 max-w-3xl mx-auto">

        <p className="text-xs text-muted-foreground text-center">{t('termsLastUpdated')}</p>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <FileText className="h-4 w-4 text-primary" />
            {t('termsIntroTitle')}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{t('termsIntroText')}</p>
        </div>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Globe className="h-4 w-4 text-blue-400" />
            {t('termsServiceTitle')}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{t('termsServiceText')}</p>
        </div>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-green-400" />
            {t('termsAccountsTitle')}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>{t('termsAccount1')}</li>
            <li>{t('termsAccount2')}</li>
            <li>{t('termsAccount3')}</li>
            <li>{t('termsAccount4')}</li>
          </ul>
        </div>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <FileText className="h-4 w-4 text-purple-400" />
            {t('termsUGCTitle')}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>{t('termsUGC1')}</li>
            <li>{t('termsUGC2')}</li>
            <li>{t('termsUGC3')}</li>
            <li>{t('termsUGC4')}</li>
          </ul>
        </div>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Scale className="h-4 w-4 text-yellow-500" />
            {t('termsEmbedTitle')}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed mb-2">{t('termsEmbedText')}</p>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>{t('termsEmbed1')}</li>
            <li>{t('termsEmbed2')}</li>
            <li>{t('termsEmbed3')}</li>
          </ul>
        </div>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Ban className="h-4 w-4 text-red-400" />
            {t('termsProhibitedTitle')}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>{t('termsProhibited1')}</li>
            <li>{t('termsProhibited2')}</li>
            <li>{t('termsProhibited3')}</li>
            <li>{t('termsProhibited4')}</li>
            <li>{t('termsProhibited5')}</li>
          </ul>
        </div>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <AlertCircle className="h-4 w-4 text-orange-400" />
            {t('termsDisclaimerTitle')}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>{t('termsDisclaimer1')}</li>
            <li>{t('termsDisclaimer2')}</li>
            <li>{t('termsDisclaimer3')}</li>
            <li>{t('termsDisclaimer4')}</li>
          </ul>
        </div>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{t('termsGovLawTitle')}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{t('termsGovLawText')}</p>
        </div>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{t('termsChangesTitle')}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{t('termsChangesText')}</p>
        </div>

        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{t('termsContactTitle')}</h3>
          <p className="text-sm text-muted-foreground">{t('termsContactText')}</p>
          <p className="text-sm text-primary mt-1"><a href="mailto:mohammedalrejab@gmail.com">mohammedalrejab@gmail.com</a></p>
        </div>

        <p className="text-center text-xs text-muted-foreground/40 pt-2">{t('termsLastUpdated')}</p>
      </div>
    </div>
  );
}
