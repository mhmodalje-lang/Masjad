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
  '/': { title: 'Azan & Hikaya - Prayer Times | Quran | Duas', description: 'Accurate prayer times, Quran, Duas, Zakat calculator, Tasbeeh. Complete Islamic app.' },
  '/prayer-times': { title: 'Prayer Times Today | Azan & Hikaya', description: 'Accurate prayer times for your location.' },
  '/quran': { title: 'Holy Quran - Read & Listen | Azan & Hikaya', description: 'Read and listen to the Holy Quran.' },
  '/qibla': { title: 'Qibla Direction | Azan & Hikaya', description: 'Find Qibla direction from anywhere.' },
  '/duas': { title: 'Islamic Duas & Adhkar | Azan & Hikaya', description: 'Complete collection of Islamic duas.' },
  '/tasbeeh': { title: 'Digital Tasbeeh Counter | Azan & Hikaya', description: 'Digital tasbeeh and dhikr counter.' },
  '/zakat': { title: 'Zakat Calculator | Azan & Hikaya', description: 'Calculate your Zakat accurately.' },
  '/mosque-times': { title: 'Nearby Mosque Times | Azan & Hikaya', description: 'Find prayer times at nearby mosques.' },
  '/stories': { title: 'Islamic Stories | Azan & Hikaya', description: 'Inspiring Islamic stories and lessons.' },
  '/tracker': { title: 'Prayer Tracker | Azan & Hikaya', description: 'Track your daily prayers.' },
  '/daily-duas': { title: 'Dua of the Day | Azan & Hikaya', description: 'Daily renewed duas.' },
  '/ruqyah': { title: 'Ruqyah Ash-Shariah | Azan & Hikaya', description: 'Ruqyah from Quran and Sunnah.' },
};

const SEO_DE: SeoData = {
  '/': { title: 'Azan & Hikaya - Gebetszeiten | Quran | Duas', description: 'Genaue Gebetszeiten, Quran, Duas, Zakat-Rechner. Islamische App.' },
  '/prayer-times': { title: 'Gebetszeiten Heute | Azan & Hikaya', description: 'Genaue Gebetszeiten für Ihren Standort.' },
  '/quran': { title: 'Heiliger Quran - Lesen & Hören | Azan & Hikaya', description: 'Heiligen Quran lesen und hören.' },
  '/qibla': { title: 'Qibla-Richtung | Azan & Hikaya', description: 'Qibla-Richtung von überall finden.' },
  '/duas': { title: 'Islamische Duas & Adhkar | Azan & Hikaya', description: 'Umfassende Sammlung islamischer Duas.' },
  '/tasbeeh': { title: 'Digitaler Tasbeeh-Zähler | Azan & Hikaya', description: 'Digitaler Tasbeeh- und Dhikr-Zähler.' },
  '/zakat': { title: 'Zakat-Rechner | Azan & Hikaya', description: 'Berechnen Sie Ihre Zakat genau.' },
  '/mosque-times': { title: 'Moschee-Gebetszeiten | Azan & Hikaya', description: 'Gebetszeiten in nahen Moscheen.' },
  '/stories': { title: 'Islamische Geschichten | Azan & Hikaya', description: 'Inspirierende islamische Geschichten.' },
  '/tracker': { title: 'Gebets-Tracker | Azan & Hikaya', description: 'Tägliche Gebete verfolgen.' },
  '/daily-duas': { title: 'Dua des Tages | Azan & Hikaya', description: 'Tägliche erneuerte Duas.' },
  '/ruqyah': { title: 'Ruqyah Ash-Shariah | Azan & Hikaya', description: 'Ruqyah aus Quran und Sunnah.' },
};

const SEO_FR: SeoData = {
  '/': { title: 'Azan & Hikaya - Horaires de Prière | Coran | Duas', description: 'Horaires de prière, Coran, Duas, calculateur de Zakat. Application islamique complète.' },
  '/prayer-times': { title: 'Horaires de Prière | Azan & Hikaya', description: 'Horaires de prière précis pour votre emplacement.' },
  '/quran': { title: 'Saint Coran - Lire & Écouter | Azan & Hikaya', description: 'Lisez et écoutez le Saint Coran.' },
  '/qibla': { title: 'Direction de la Qibla | Azan & Hikaya', description: 'Trouvez la direction de la Qibla.' },
  '/duas': { title: 'Duas & Adhkar | Azan & Hikaya', description: 'Collection complète de duas islamiques.' },
  '/tasbeeh': { title: 'Compteur Tasbeeh | Azan & Hikaya', description: 'Compteur numérique de Tasbeeh.' },
  '/zakat': { title: 'Calculateur de Zakat | Azan & Hikaya', description: 'Calculez votre Zakat avec précision.' },
  '/mosque-times': { title: 'Horaires des Mosquées | Azan & Hikaya', description: 'Horaires de prière dans les mosquées proches.' },
  '/stories': { title: 'Histoires Islamiques | Azan & Hikaya', description: 'Histoires islamiques inspirantes.' },
  '/tracker': { title: 'Suivi de Prière | Azan & Hikaya', description: 'Suivez vos prières quotidiennes.' },
  '/daily-duas': { title: 'Dua du Jour | Azan & Hikaya', description: 'Duas quotidiennes renouvelées.' },
  '/ruqyah': { title: 'Ruqyah Ash-Shariah | Azan & Hikaya', description: 'Ruqyah du Coran et de la Sunnah.' },
};

const SEO_TR: SeoData = {
  '/': { title: 'Azan & Hikaya - Namaz Vakitleri | Kuran | Dualar', description: 'Doğru namaz vakitleri, Kuran, dualar, zekat hesaplayıcı, tesbih. Kapsamlı İslami uygulama.' },
  '/prayer-times': { title: 'Bugünün Namaz Vakitleri | Azan & Hikaya', description: 'Konumunuza göre doğru namaz vakitleri.' },
  '/quran': { title: 'Kuran-ı Kerim - Oku & Dinle | Azan & Hikaya', description: 'Kuran-ı Kerim okuyun ve dinleyin.' },
  '/qibla': { title: 'Kıble Yönü | Azan & Hikaya', description: 'Her yerden kıble yönünü bulun.' },
  '/duas': { title: 'İslami Dualar & Zikirler | Azan & Hikaya', description: 'Kapsamlı İslami dua koleksiyonu.' },
  '/tasbeeh': { title: 'Dijital Tesbih Sayacı | Azan & Hikaya', description: 'Dijital tesbih ve zikir sayacı.' },
  '/zakat': { title: 'Zekat Hesaplayıcı | Azan & Hikaya', description: 'Zekatınızı doğru hesaplayın.' },
  '/mosque-times': { title: 'Yakın Cami Vakitleri | Azan & Hikaya', description: 'Yakındaki camilerdeki namaz vakitleri.' },
  '/stories': { title: 'İslami Hikayeler | Azan & Hikaya', description: 'İlham verici İslami hikayeler.' },
  '/tracker': { title: 'Namaz Takibi | Azan & Hikaya', description: 'Günlük namazlarınızı takip edin.' },
  '/daily-duas': { title: 'Günün Duası | Azan & Hikaya', description: 'Günlük yenilenen dualar.' },
  '/ruqyah': { title: 'Rukye-i Şerife | Azan & Hikaya', description: 'Kuran ve Sünnetten rukye.' },
};

const SEO_NL: SeoData = {
  '/': { title: 'Azan & Hikaya - Gebetstijden | Koran | Duas', description: 'Nauwkeurige gebetstijden, Koran, Duas, Zakat-calculator. Islamitische app.' },
  '/prayer-times': { title: 'Gebetstijden Vandaag | Azan & Hikaya', description: 'Nauwkeurige gebetstijden voor uw locatie.' },
  '/quran': { title: 'Heilige Koran - Lezen & Luisteren | Azan & Hikaya', description: 'Lees en luister naar de Heilige Koran.' },
  '/qibla': { title: 'Qibla Richting | Azan & Hikaya', description: 'Vind de Qibla richting overal.' },
  '/duas': { title: 'Islamitische Duas & Adhkar | Azan & Hikaya', description: 'Complete verzameling islamitische duas.' },
  '/zakat': { title: 'Zakat Calculator | Azan & Hikaya', description: 'Bereken uw Zakat nauwkeurig.' },
};

const SEO_SV: SeoData = {
  '/': { title: 'Azan & Hikaya - Bönetider | Koranen | Duas', description: 'Exakta bönetider, Koranen, Duas, Zakat-kalkylator. Islamisk app.' },
  '/prayer-times': { title: 'Bönetider Idag | Azan & Hikaya', description: 'Exakta bönetider för din plats.' },
  '/quran': { title: 'Heliga Koranen - Läs & Lyssna | Azan & Hikaya', description: 'Läs och lyssna på Heliga Koranen.' },
  '/qibla': { title: 'Qibla Riktning | Azan & Hikaya', description: 'Hitta Qibla riktningen var som helst.' },
  '/duas': { title: 'Islamiska Duas & Adhkar | Azan & Hikaya', description: 'Komplett samling av islamiska duas.' },
  '/zakat': { title: 'Zakat Kalkylator | Azan & Hikaya', description: 'Beräkna din Zakat noggrant.' },
};

const SEO_EL: SeoData = {
  '/': { title: 'Azan & Hikaya - Ώρες Προσευχής | Κοράνι | Ντουά', description: 'Ακριβείς ώρες προσευχής, Κοράνι, Ντουά, υπολογιστής Ζακάτ. Ισλαμική εφαρμογή.' },
  '/prayer-times': { title: 'Ώρες Προσευχής Σήμερα | Azan & Hikaya', description: 'Ακριβείς ώρες προσευχής για την τοποθεσία σας.' },
  '/quran': { title: 'Ιερό Κοράνι | Azan & Hikaya', description: 'Διαβάστε και ακούστε το Ιερό Κοράνι.' },
};

const SEO_RU: SeoData = {
  '/': { title: 'Азан и Хикая - Время молитвы | Коран | Дуа', description: 'Точное время молитвы, Коран, Дуа, калькулятор Закята. Исламское приложение.' },
  '/prayer-times': { title: 'Время молитвы сегодня | Азан и Хикая', description: 'Точное время молитвы для вашего местоположения.' },
  '/quran': { title: 'Священный Коран | Азан и Хикая', description: 'Читайте и слушайте Священный Коран.' },
};

const SEO_MAP: Record<string, SeoData> = {
  ar: SEO_AR, en: SEO_EN, de: SEO_DE, 'de-AT': SEO_DE,
  fr: SEO_FR, tr: SEO_TR, nl: SEO_NL, sv: SEO_SV,
  el: SEO_EL, ru: SEO_RU,
};

export function useSEO() {
  const location = useLocation();
  const { locale } = useLocale();

  useEffect(() => {
    const seoMap = SEO_MAP[locale] || SEO_MAP[locale.split('-')[0]] || SEO_EN;
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

    const canonical = document.querySelector('link[rel="canonical"]') as HTMLLinkElement;
    if (canonical) {
      canonical.href = location.pathname;
    }
  }, [location.pathname, locale]);
}
