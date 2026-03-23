import { useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { useLocation } from 'react-router-dom';

type SeoData = Record<string, { title: string; description: string }>;

const SEO_AR: SeoData = {
  '/': { title: 'أذان وحكاية - مواقيت الصلاة | القرآن الكريم | أذكار وأدعية', description: 'مواقيت الصلاة الدقيقة، القرآن الكريم، الأذكار والأدعية، حاسبة الزكاة، التسبيح. تطبيق إسلامي شامل.' },
  '/prayer-times': { title: 'مواقيت الصلاة اليوم | أذان وحكاية', description: 'مواقيت الصلاة الدقيقة حسب موقعك.' },
  '/quran': { title: 'القرآن الكريم - قراءة واستماع | أذان وحكاية', description: 'اقرأ واستمع إلى القرآن الكريم كاملاً.' },
  '/qibla': { title: 'اتجاه القبلة | أذان وحكاية', description: 'حدد اتجاه القبلة بدقة من أي مكان.' },
  '/duas': { title: 'الأذكار والأدعية | أذان وحكاية', description: 'مجموعة شاملة من الأذكار والأدعية.' },
  '/tasbeeh': { title: 'التسبيح الإلكتروني | أذان وحكاية', description: 'عداد التسبيح الإلكتروني.' },
  '/zakat': { title: 'حاسبة الزكاة | أذان وحكاية', description: 'احسب زكاة المال بدقة وسهولة.' },
  '/mosque-times': { title: 'أوقات المساجد القريبة | أذان وحكاية', description: 'اعرف أوقات الصلاة في المساجد القريبة.' },
  '/stories': { title: 'قصص إسلامية | أذان وحكاية', description: 'قصص إسلامية ملهمة وعبر.' },
  '/tracker': { title: 'متابعة الصلاة | أذان وحكاية', description: 'تتبع صلواتك اليومية.' },
  '/daily-duas': { title: 'دعاء اليوم | أذان وحكاية', description: 'أدعية يومية متجددة.' },
  '/ruqyah': { title: 'الرقية الشرعية | أذان وحكاية', description: 'الرقية الشرعية من القرآن والسنة.' },
};

const SEO_EN: SeoData = {
  '/': { title: 'Athan & Hikaya - Prayer Times | Quran | Duas', description: 'Accurate prayer times, Quran, Duas, Zakat calculator, Tasbeeh. Complete Islamic app.' },
  '/prayer-times': { title: 'Prayer Times Today | Athan & Hikaya', description: 'Accurate prayer times for your location.' },
  '/quran': { title: 'Holy Quran - Read & Listen | Athan & Hikaya', description: 'Read and listen to the Holy Quran.' },
  '/qibla': { title: 'Qibla Direction | Athan & Hikaya', description: 'Find Qibla direction from anywhere.' },
  '/duas': { title: 'Islamic Duas & Adhkar | Athan & Hikaya', description: 'Complete collection of Islamic duas.' },
  '/tasbeeh': { title: 'Digital Tasbeeh Counter | Athan & Hikaya', description: 'Digital tasbeeh and dhikr counter.' },
  '/zakat': { title: 'Zakat Calculator | Athan & Hikaya', description: 'Calculate your Zakat accurately.' },
  '/mosque-times': { title: 'Nearby Mosque Times | Athan & Hikaya', description: 'Find prayer times at nearby mosques.' },
  '/stories': { title: 'Islamic Stories | Athan & Hikaya', description: 'Inspiring Islamic stories and lessons.' },
  '/tracker': { title: 'Prayer Tracker | Athan & Hikaya', description: 'Track your daily prayers.' },
  '/daily-duas': { title: 'Dua of the Day | Athan & Hikaya', description: 'Daily renewed duas.' },
  '/ruqyah': { title: 'Ruqyah Ash-Shariah | Athan & Hikaya', description: 'Ruqyah from Quran and Sunnah.' },
};

const SEO_DE: SeoData = {
  '/': { title: 'Athan & Hikaya - Gebetszeiten | Quran | Duas', description: 'Genaue Gebetszeiten, Quran, Duas, Zakat-Rechner. Islamische App.' },
  '/prayer-times': { title: 'Gebetszeiten Heute | Athan & Hikaya', description: 'Genaue Gebetszeiten.' },
  '/quran': { title: 'Heiliger Quran | Athan & Hikaya', description: 'Quran lesen und hören.' },
};

const SEO_FR: SeoData = {
  '/': { title: 'Athan & Hikaya - Horaires de Prière | Coran | Duas', description: 'Horaires de prière, Coran, Duas. Application islamique.' },
};

const SEO_MAP: Record<string, SeoData> = { ar: SEO_AR, en: SEO_EN, de: SEO_DE, fr: SEO_FR };

export function useSEO() {
  const location = useLocation();
  const { locale } = useLocale();

  useEffect(() => {
    const seoMap = SEO_MAP[locale] || SEO_EN;
    const seo = seoMap[location.pathname] || seoMap['/'] || SEO_EN['/'];
    document.title = seo.title;

    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) metaDesc.setAttribute('content', seo.description);

    const ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle) ogTitle.setAttribute('content', seo.title);

    const ogDesc = document.querySelector('meta[property="og:description"]');
    if (ogDesc) ogDesc.setAttribute('content', seo.description);

    const twTitle = document.querySelector('meta[name="twitter:title"]');
    if (twTitle) twTitle.setAttribute('content', seo.title);

    const twDesc = document.querySelector('meta[name="twitter:description"]');
    if (twDesc) twDesc.setAttribute('content', seo.description);

    let canonical = document.querySelector('link[rel="canonical"]') as HTMLLinkElement;
    if (canonical) {
      canonical.href = location.pathname;
    }
  }, [location.pathname, locale]);
}
