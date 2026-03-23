import { Link } from 'react-router-dom';
import PolicyFooter from '@/components/PolicyFooter';
import { ArrowRight, ArrowLeft, Heart, Star, Shield, Users, Globe, Sparkles, Mail, Phone } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';

export default function AboutUs() {
  const { t, dir, isRTL } = useLocale();
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir} data-testid="about-page">
      <div className="sticky top-0 z-50 glass-nav bg-background/80 border-b border-border/10 px-4 h-14 flex items-center gap-3">
        <Link to="/more" className="p-2 rounded-xl bg-muted/50 active:scale-95"><BackArrow className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">{t('aboutUs')}</h1>
      </div>
      <div className="px-5 py-6 space-y-6 max-w-3xl mx-auto">
        {/* App Identity */}
        <div className="text-center mb-8">
          <div className="h-20 w-20 mx-auto rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-4">
            <Sparkles className="h-10 w-10 text-primary" />
          </div>
          <h2 className="text-2xl font-black text-foreground">{t('appName')}</h2>
          <p className="text-sm text-muted-foreground mt-2">{t('yourIslamicApp')}</p>
        </div>

        {/* Mission */}
        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Heart className="h-4 w-4 text-red-500 dark:text-red-400" />
            {t('ourMission')}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {t('ourMissionText')}
          </p>
        </div>

        {/* Features */}
        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Star className="h-4 w-4 text-primary" />
            {t('ourFeatures')}
          </h3>
          <ul className="space-y-3 text-sm text-muted-foreground">
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-500 dark:text-green-400 mt-0.5 shrink-0" />{t('feat_prayer')}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-500 dark:text-green-400 mt-0.5 shrink-0" />{t('feat_quran')}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-500 dark:text-green-400 mt-0.5 shrink-0" />{t('feat_ai')}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-500 dark:text-green-400 mt-0.5 shrink-0" />{t('feat_stories')}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-500 dark:text-green-400 mt-0.5 shrink-0" />{t('feat_duas')}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-500 dark:text-green-400 mt-0.5 shrink-0" />{t('feat_zakat')}</li>
          </ul>
        </div>

        {/* Team */}
        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Users className="h-4 w-4 text-blue-500 dark:text-blue-400" />
            {t('ourTeam')}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {t('ourTeamText')}
          </p>
          <p className="text-sm text-primary font-bold mt-3">
            {t('founder')}: Mohammed Al-Rejab
          </p>
        </div>

        {/* Legal / Impressum */}
        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Globe className="h-4 w-4 text-teal-400" />
            {t('legalInfo')}
          </h3>
          <div className="space-y-2 text-sm text-muted-foreground">
            <p><strong>{t('responsible')}:</strong> Mohammed Al-Rejab</p>
            <p className="flex items-center gap-2">
              <Mail className="h-3.5 w-3.5" />
              <a href="mailto:mohammedalrejab@gmail.com" className="text-primary">mohammedalrejab@gmail.com</a>
            </p>
            <p className="flex items-center gap-2">
              <Phone className="h-3.5 w-3.5" />
              <a href="tel:+4917684034961" className="text-primary" dir="ltr">+49 176 84034961</a>
            </p>
          </div>
        </div>

        {/* Links */}
        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{t('legalLinks')}</h3>
          <div className="space-y-2">
            <Link to="/privacy" className="block text-sm text-primary hover:underline">{t('privacyPolicy')} →</Link>
            <Link to="/terms" className="block text-sm text-primary hover:underline">{t('termsOfService')} →</Link>
          </div>
        </div>

        <p className="text-center text-xs text-muted-foreground/40 pt-4">
          {t('appName')} v2.0 | {t('allRightsReserved')} © {new Date().getFullYear()}
        </p>
      </div>
      <PolicyFooter />
    </div>
  );
}
