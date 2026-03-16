import { Link } from 'react-router-dom';
import { ArrowRight, ArrowLeft, Heart, Star, Shield, Users, Globe, Sparkles, Mail, Phone } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';

export default function AboutUs() {
  const { t, dir, isRTL } = useLocale();
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir} data-testid="about-page">
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center gap-3">
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
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Heart className="h-4 w-4 text-red-400" />
            {isRTL ? 'رسالتنا' : 'Our Mission'}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL
              ? 'نهدف إلى تقديم تجربة إسلامية رقمية متكاملة تجمع بين التكنولوجيا الحديثة والقيم الإسلامية الأصيلة. نسعى لخدمة المسلمين حول العالم بأدوات تساعدهم في عبادتهم وتعلمهم الديني، مع الالتزام الكامل بالخصوصية وحماية البيانات.'
              : 'We aim to provide a comprehensive digital Islamic experience that combines modern technology with authentic Islamic values. We strive to serve Muslims around the world with tools that help them in their worship and religious learning, with full commitment to privacy and data protection.'}
          </p>
        </div>

        {/* Features */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Star className="h-4 w-4 text-primary" />
            {isRTL ? 'مميزاتنا' : 'Our Features'}
          </h3>
          <ul className="space-y-3 text-sm text-muted-foreground">
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />{isRTL ? 'مواقيت صلاة دقيقة مع إشعارات الأذان' : 'Accurate prayer times with Azan notifications'}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />{isRTL ? 'قراءة القرآن الكريم مع التفسير' : 'Holy Quran reading with interpretation'}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />{isRTL ? 'مساعد ذكي مدعوم بالذكاء الاصطناعي' : 'AI-powered smart assistant'}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />{isRTL ? 'حكايات وقصص إسلامية ملهمة' : 'Inspiring Islamic stories'}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />{isRTL ? 'أدعية وأذكار يومية شاملة' : 'Comprehensive daily duas and adhkar'}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />{isRTL ? 'حاسبة الزكاة والتسبيح' : 'Zakat calculator and Tasbeeh'}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />{isRTL ? 'الرقية الشرعية بالفيديو والصوت' : 'Ruqyah with video and audio'}</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />{isRTL ? 'دعم متعدد اللغات (عربي، إنجليزي، ألماني، فرنسي، روسي، تركي)' : 'Multi-language support (Arabic, English, German, French, Russian, Turkish)'}</li>
          </ul>
        </div>

        {/* Team */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Users className="h-4 w-4 text-blue-400" />
            {isRTL ? 'فريقنا' : 'Our Team'}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL
              ? 'تم تطوير هذا التطبيق بحب وإخلاص لخدمة الأمة الإسلامية. نعمل باستمرار على تحسين التطبيق وإضافة ميزات جديدة.'
              : 'This app was developed with love and dedication to serve the Islamic community. We continuously work on improving the app and adding new features.'}
          </p>
          <p className="text-sm text-primary font-bold mt-3">
            {isRTL ? 'المؤسس: محمد الرجب' : 'Founder: Mohammed Al-Rejab'}
          </p>
        </div>

        {/* Legal / Impressum */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Globe className="h-4 w-4 text-teal-400" />
            {isRTL ? 'معلومات قانونية (Impressum)' : 'Legal Information (Impressum)'}
          </h3>
          <div className="space-y-2 text-sm text-muted-foreground">
            <p><strong>{isRTL ? 'المسؤول:' : 'Responsible:'}</strong> {isRTL ? 'محمد الرجب' : 'Mohammed Al-Rejab'}</p>
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
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{isRTL ? 'روابط قانونية' : 'Legal Links'}</h3>
          <div className="space-y-2">
            <Link to="/privacy" className="block text-sm text-primary hover:underline">{t('privacyPolicy')} →</Link>
            <Link to="/terms" className="block text-sm text-primary hover:underline">{t('termsOfService')} →</Link>
          </div>
        </div>

        <p className="text-center text-xs text-muted-foreground/40 pt-4">
          {isRTL ? `أذان وحكاية v2.0 | جميع الحقوق محفوظة © ${new Date().getFullYear()}` : `Azan & Hikaya v2.0 | All rights reserved © ${new Date().getFullYear()}`}
        </p>
      </div>
    </div>
  );
}
