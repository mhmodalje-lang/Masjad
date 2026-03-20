import { useState, useMemo } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { motion, AnimatePresence } from 'framer-motion';
import { Search, X, Heart, ChevronDown } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

const NAMES = [
  { num: 1, ar: 'الرَّحْمَنُ', en: 'Ar-Rahman', meaning: 'الذي وسعت رحمته كل شيء', meaningEn: 'The Most Gracious' },
  { num: 2, ar: 'الرَّحِيمُ', en: 'Ar-Raheem', meaning: 'الذي يرحم عباده المؤمنين', meaningEn: 'The Most Merciful' },
  { num: 3, ar: 'المَلِكُ', en: 'Al-Malik', meaning: 'المالك لكل شيء، المتصرف في خلقه', meaningEn: 'The King, The Sovereign' },
  { num: 4, ar: 'القُدُّوسُ', en: 'Al-Quddus', meaning: 'المنزه عن كل عيب ونقص', meaningEn: 'The Most Holy' },
  { num: 5, ar: 'السَّلَامُ', en: 'As-Salam', meaning: 'السالم من كل عيب وآفة', meaningEn: 'The Source of Peace' },
  { num: 6, ar: 'المُؤْمِنُ', en: 'Al-Mu'min', meaning: 'الذي يُصَدِّق عباده ويؤمنهم من عذابه', meaningEn: 'The Guardian of Faith' },
  { num: 7, ar: 'المُهَيْمِنُ', en: 'Al-Muhaymin', meaning: 'الشاهد على خلقه، المسيطر عليهم', meaningEn: 'The Protector' },
  { num: 8, ar: 'العَزِيزُ', en: 'Al-Aziz', meaning: 'الغالب الذي لا يُغلب', meaningEn: 'The Almighty' },
  { num: 9, ar: 'الجَبَّارُ', en: 'Al-Jabbar', meaning: 'الذي يجبر كسر عباده ويُصلح أحوالهم', meaningEn: 'The Compeller' },
  { num: 10, ar: 'المُتَكَبِّرُ', en: 'Al-Mutakabbir', meaning: 'المتعالي عن صفات الخلق', meaningEn: 'The Supreme' },
  { num: 11, ar: 'الخَالِقُ', en: 'Al-Khaliq', meaning: 'الذي أوجد الأشياء من العدم', meaningEn: 'The Creator' },
  { num: 12, ar: 'البَارِئُ', en: 'Al-Bari', meaning: 'الذي خلق الخلق لا على مثال سابق', meaningEn: 'The Originator' },
  { num: 13, ar: 'المُصَوِّرُ', en: 'Al-Musawwir', meaning: 'الذي صوّر جميع المخلوقات', meaningEn: 'The Fashioner' },
  { num: 14, ar: 'الغَفَّارُ', en: 'Al-Ghaffar', meaning: 'الذي يغفر الذنوب مرة بعد مرة', meaningEn: 'The Forgiving' },
  { num: 15, ar: 'القَهَّارُ', en: 'Al-Qahhar', meaning: 'الذي قهر جميع المخلوقات', meaningEn: 'The Subduer' },
  { num: 16, ar: 'الوَهَّابُ', en: 'Al-Wahhab', meaning: 'الذي يهب النعم بلا عوض', meaningEn: 'The Bestower' },
  { num: 17, ar: 'الرَّزَّاقُ', en: 'Ar-Razzaq', meaning: 'الذي يرزق جميع المخلوقات', meaningEn: 'The Provider' },
  { num: 18, ar: 'الفَتَّاحُ', en: 'Al-Fattah', meaning: 'الذي يفتح أبواب الرزق والرحمة', meaningEn: 'The Opener' },
  { num: 19, ar: 'العَلِيمُ', en: 'Al-Aleem', meaning: 'الذي يعلم كل شيء ظاهره وباطنه', meaningEn: 'The All-Knowing' },
  { num: 20, ar: 'القَابِضُ', en: 'Al-Qabid', meaning: 'الذي يقبض الأرزاق والأرواح', meaningEn: 'The Restrainer' },
  { num: 21, ar: 'البَاسِطُ', en: 'Al-Basit', meaning: 'الذي يبسط الرزق لمن يشاء', meaningEn: 'The Expander' },
  { num: 22, ar: 'الخَافِضُ', en: 'Al-Khafid', meaning: 'الذي يخفض من يشاء', meaningEn: 'The Abaser' },
  { num: 23, ar: 'الرَّافِعُ', en: 'Ar-Rafi', meaning: 'الذي يرفع من يشاء بالعز والطاعة', meaningEn: 'The Exalter' },
  { num: 24, ar: 'المُعِزُّ', en: 'Al-Mu'izz', meaning: 'الذي يهب العزة لمن يشاء', meaningEn: 'The Bestower of Honor' },
  { num: 25, ar: 'المُذِلُّ', en: 'Al-Mudhill', meaning: 'الذي يذل من يشاء من الطغاة', meaningEn: 'The Humiliator' },
  { num: 26, ar: 'السَّمِيعُ', en: 'As-Sami', meaning: 'الذي يسمع كل شيء', meaningEn: 'The All-Hearing' },
  { num: 27, ar: 'البَصِيرُ', en: 'Al-Basir', meaning: 'الذي يرى كل شيء', meaningEn: 'The All-Seeing' },
  { num: 28, ar: 'الحَكَمُ', en: 'Al-Hakam', meaning: 'الحاكم العدل بين خلقه', meaningEn: 'The Judge' },
  { num: 29, ar: 'العَدْلُ', en: 'Al-Adl', meaning: 'العادل الذي لا يظلم أحداً', meaningEn: 'The Just' },
  { num: 30, ar: 'اللَّطِيفُ', en: 'Al-Latif', meaning: 'الرفيق بعباده الذي يوصل لهم مصالحهم', meaningEn: 'The Subtle One' },
  { num: 31, ar: 'الخَبِيرُ', en: 'Al-Khabir', meaning: 'العالم بحقائق الأشياء وبواطنها', meaningEn: 'The All-Aware' },
  { num: 32, ar: 'الحَلِيمُ', en: 'Al-Haleem', meaning: 'الذي لا يعاجل بالعقوبة', meaningEn: 'The Forbearing' },
  { num: 33, ar: 'العَظِيمُ', en: 'Al-Azeem', meaning: 'ذو العظمة المطلقة في ذاته وصفاته', meaningEn: 'The Magnificent' },
  { num: 34, ar: 'الغَفُورُ', en: 'Al-Ghafur', meaning: 'الذي يكثر من المغفرة', meaningEn: 'The Forgiving' },
  { num: 35, ar: 'الشَّكُورُ', en: 'Ash-Shakur', meaning: 'الذي يشكر اليسير من العمل ويثيب عليه', meaningEn: 'The Grateful' },
  { num: 36, ar: 'العَلِيُّ', en: 'Al-Ali', meaning: 'المتعالي فوق خلقه بذاته وصفاته', meaningEn: 'The Most High' },
  { num: 37, ar: 'الكَبِيرُ', en: 'Al-Kabir', meaning: 'ذو الكبرياء والعظمة', meaningEn: 'The Greatest' },
  { num: 38, ar: 'الحَفِيظُ', en: 'Al-Hafiz', meaning: 'الذي يحفظ كل شيء', meaningEn: 'The Preserver' },
  { num: 39, ar: 'المُقِيتُ', en: 'Al-Muqit', meaning: 'الذي يقيت الخلائق ويوصل لهم أرزاقهم', meaningEn: 'The Nourisher' },
  { num: 40, ar: 'الحَسِيبُ', en: 'Al-Hasib', meaning: 'الكافي الذي يحاسب عباده', meaningEn: 'The Reckoner' },
  { num: 41, ar: 'الجَلِيلُ', en: 'Al-Jalil', meaning: 'ذو الجلال والعظمة', meaningEn: 'The Majestic' },
  { num: 42, ar: 'الكَرِيمُ', en: 'Al-Karim', meaning: 'الكثير الخير الجواد المعطي', meaningEn: 'The Generous' },
  { num: 43, ar: 'الرَّقِيبُ', en: 'Ar-Raqib', meaning: 'المطلع على ما أكنّته الصدور', meaningEn: 'The Watchful' },
  { num: 44, ar: 'المُجِيبُ', en: 'Al-Mujib', meaning: 'الذي يجيب دعاء الداعي', meaningEn: 'The Responsive' },
  { num: 45, ar: 'الوَاسِعُ', en: 'Al-Wasi', meaning: 'الذي وسع رزقه جميع خلقه', meaningEn: 'The All-Encompassing' },
  { num: 46, ar: 'الحَكِيمُ', en: 'Al-Hakim', meaning: 'الذي يضع كل شيء في موضعه', meaningEn: 'The Wise' },
  { num: 47, ar: 'الوَدُودُ', en: 'Al-Wadud', meaning: 'المحب لعباده المؤمنين', meaningEn: 'The Loving' },
  { num: 48, ar: 'المَجِيدُ', en: 'Al-Majid', meaning: 'ذو المجد والشرف العظيم', meaningEn: 'The Glorious' },
  { num: 49, ar: 'البَاعِثُ', en: 'Al-Ba'ith', meaning: 'الذي يبعث الخلق يوم القيامة', meaningEn: 'The Resurrector' },
  { num: 50, ar: 'الشَّهِيدُ', en: 'Ash-Shahid', meaning: 'المطلع على كل شيء لا يغيب عنه شيء', meaningEn: 'The Witness' },
  { num: 51, ar: 'الحَقُّ', en: 'Al-Haqq', meaning: 'الموجود حقاً الثابت بلا شك', meaningEn: 'The Truth' },
  { num: 52, ar: 'الوَكِيلُ', en: 'Al-Wakil', meaning: 'الذي يتولى أمور خلقه', meaningEn: 'The Trustee' },
  { num: 53, ar: 'القَوِيُّ', en: 'Al-Qawi', meaning: 'التام القدرة الذي لا يعجزه شيء', meaningEn: 'The Strong' },
  { num: 54, ar: 'المَتِينُ', en: 'Al-Matin', meaning: 'شديد القوة الذي لا يلحقه ضعف', meaningEn: 'The Firm' },
  { num: 55, ar: 'الوَلِيُّ', en: 'Al-Wali', meaning: 'الناصر لعباده المؤمنين', meaningEn: 'The Protecting Friend' },
  { num: 56, ar: 'الحَمِيدُ', en: 'Al-Hamid', meaning: 'المحمود المستحق للحمد', meaningEn: 'The Praiseworthy' },
  { num: 57, ar: 'المُحْصِي', en: 'Al-Muhsi', meaning: 'الذي أحصى كل شيء عدداً', meaningEn: 'The Counter' },
  { num: 58, ar: 'المُبْدِئُ', en: 'Al-Mubdi', meaning: 'الذي بدأ خلق الأشياء', meaningEn: 'The Originator' },
  { num: 59, ar: 'المُعِيدُ', en: 'Al-Mu'id', meaning: 'الذي يعيد الخلق بعد الموت', meaningEn: 'The Restorer' },
  { num: 60, ar: 'المُحْيِي', en: 'Al-Muhyi', meaning: 'الذي يحيي الموتى ويهب الحياة', meaningEn: 'The Giver of Life' },
  { num: 61, ar: 'المُمِيتُ', en: 'Al-Mumit', meaning: 'الذي يميت الأحياء', meaningEn: 'The Taker of Life' },
  { num: 62, ar: 'الحَيُّ', en: 'Al-Hayy', meaning: 'الحي الذي لا يموت', meaningEn: 'The Ever Living' },
  { num: 63, ar: 'القَيُّومُ', en: 'Al-Qayyum', meaning: 'القائم بذاته المقيم لغيره', meaningEn: 'The Self-Subsisting' },
  { num: 64, ar: 'الوَاجِدُ', en: 'Al-Wajid', meaning: 'الغني الذي لا يفتقر لشيء', meaningEn: 'The Finder' },
  { num: 65, ar: 'المَاجِدُ', en: 'Al-Majid', meaning: 'التام الكمال ذو الشرف والسلطان', meaningEn: 'The Noble' },
  { num: 66, ar: 'الوَاحِدُ', en: 'Al-Wahid', meaning: 'المنفرد بذاته وصفاته وأفعاله', meaningEn: 'The One' },
  { num: 67, ar: 'الصَّمَدُ', en: 'As-Samad', meaning: 'الذي يصمد إليه في الحوائج', meaningEn: 'The Eternal' },
  { num: 68, ar: 'القَادِرُ', en: 'Al-Qadir', meaning: 'الذي يقدر على ما يشاء', meaningEn: 'The All-Powerful' },
  { num: 69, ar: 'المُقْتَدِرُ', en: 'Al-Muqtadir', meaning: 'التام القدرة الذي لا يمتنع عليه شيء', meaningEn: 'The Powerful' },
  { num: 70, ar: 'المُقَدِّمُ', en: 'Al-Muqaddim', meaning: 'الذي يقدم من يشاء', meaningEn: 'The Expediter' },
  { num: 71, ar: 'المُؤَخِّرُ', en: 'Al-Mu'akhkhir', meaning: 'الذي يؤخر من يشاء', meaningEn: 'The Delayer' },
  { num: 72, ar: 'الأَوَّلُ', en: 'Al-Awwal', meaning: 'الذي ليس قبله شيء', meaningEn: 'The First' },
  { num: 73, ar: 'الآخِرُ', en: 'Al-Akhir', meaning: 'الذي ليس بعده شيء', meaningEn: 'The Last' },
  { num: 74, ar: 'الظَّاهِرُ', en: 'Az-Zahir', meaning: 'الذي ظهر فوق كل شيء', meaningEn: 'The Manifest' },
  { num: 75, ar: 'البَاطِنُ', en: 'Al-Batin', meaning: 'المحتجب عن أبصار الخلق', meaningEn: 'The Hidden' },
  { num: 76, ar: 'الوَالِي', en: 'Al-Wali', meaning: 'المالك لكل شيء المتصرف فيه', meaningEn: 'The Governor' },
  { num: 77, ar: 'المُتَعَالِي', en: 'Al-Muta'ali', meaning: 'المتعالي عن صفات المخلوقين', meaningEn: 'The Most Exalted' },
  { num: 78, ar: 'البَرُّ', en: 'Al-Barr', meaning: 'العطوف الرحيم بعباده', meaningEn: 'The Source of Goodness' },
  { num: 79, ar: 'التَّوَّابُ', en: 'At-Tawwab', meaning: 'الذي يقبل التوبة عن عباده', meaningEn: 'The Acceptor of Repentance' },
  { num: 80, ar: 'المُنْتَقِمُ', en: 'Al-Muntaqim', meaning: 'الذي ينتقم من المجرمين بعدله', meaningEn: 'The Avenger' },
  { num: 81, ar: 'العَفُوُّ', en: 'Al-Afuw', meaning: 'الذي يعفو عن الذنوب', meaningEn: 'The Pardoner' },
  { num: 82, ar: 'الرَّؤُوفُ', en: 'Ar-Ra'uf', meaning: 'ذو الرأفة والرحمة الشديدة', meaningEn: 'The Compassionate' },
  { num: 83, ar: 'مَالِكُ المُلْكِ', en: 'Malik-ul-Mulk', meaning: 'المالك لجميع الأملاك', meaningEn: 'Owner of Sovereignty' },
  { num: 84, ar: 'ذُو الجَلَالِ وَالإِكْرَامِ', en: 'Dhul-Jalal-wal-Ikram', meaning: 'المستحق للتعظيم والإكرام', meaningEn: 'Lord of Majesty and Generosity' },
  { num: 85, ar: 'المُقْسِطُ', en: 'Al-Muqsit', meaning: 'العادل في حكمه', meaningEn: 'The Equitable' },
  { num: 86, ar: 'الجَامِعُ', en: 'Al-Jami', meaning: 'الذي يجمع الخلائق يوم القيامة', meaningEn: 'The Gatherer' },
  { num: 87, ar: 'الغَنِيُّ', en: 'Al-Ghani', meaning: 'المستغني عن كل شيء', meaningEn: 'The Self-Sufficient' },
  { num: 88, ar: 'المُغْنِي', en: 'Al-Mughni', meaning: 'الذي يغني من يشاء من خلقه', meaningEn: 'The Enricher' },
  { num: 89, ar: 'المَانِعُ', en: 'Al-Mani', meaning: 'الذي يمنع العطاء عمن يشاء لحكمة', meaningEn: 'The Preventer' },
  { num: 90, ar: 'الضَّارُّ', en: 'Ad-Darr', meaning: 'الذي يقدر الضر على من يشاء', meaningEn: 'The Distresser' },
  { num: 91, ar: 'النَّافِعُ', en: 'An-Nafi', meaning: 'الذي يقدر النفع لمن يشاء', meaningEn: 'The Propitious' },
  { num: 92, ar: 'النُّورُ', en: 'An-Nur', meaning: 'نور السماوات والأرض', meaningEn: 'The Light' },
  { num: 93, ar: 'الهَادِي', en: 'Al-Hadi', meaning: 'الذي يهدي عباده للحق', meaningEn: 'The Guide' },
  { num: 94, ar: 'البَدِيعُ', en: 'Al-Badi', meaning: 'الذي أبدع الخلق بلا مثال', meaningEn: 'The Originator' },
  { num: 95, ar: 'البَاقِي', en: 'Al-Baqi', meaning: 'الدائم الذي لا يفنى', meaningEn: 'The Everlasting' },
  { num: 96, ar: 'الوَارِثُ', en: 'Al-Warith', meaning: 'الباقي بعد فناء خلقه', meaningEn: 'The Inheritor' },
  { num: 97, ar: 'الرَّشِيدُ', en: 'Ar-Rashid', meaning: 'المرشد لعباده إلى ما فيه صلاحهم', meaningEn: 'The Guide to the Right Path' },
  { num: 98, ar: 'الصَّبُورُ', en: 'As-Sabur', meaning: 'الذي لا يعاجل العصاة بالعقوبة', meaningEn: 'The Patient' },
  { num: 99, ar: 'اللَّهُ', en: 'Al-Ahad', meaning: 'الاسم الأعظم الجامع لجميع الأسماء والصفات', meaningEn: 'The Unique' },
];

const COLORS = [
  'from-emerald-500/15 to-teal-500/5 border-emerald-500/20',
  'from-blue-500/15 to-cyan-500/5 border-blue-500/20',
  'from-amber-500/15 to-orange-500/5 border-amber-500/20',
  'from-purple-500/15 to-violet-500/5 border-purple-500/20',
  'from-rose-500/15 to-pink-500/5 border-rose-500/20',
  'from-teal-500/15 to-green-500/5 border-teal-500/20',
];

export default function AsmaAlHusna() {
  const { t, dir, locale } = useLocale();
  const isAr = locale === 'ar';
  const [search, setSearch] = useState('');
  const [showSearch, setShowSearch] = useState(false);
  const [expanded, setExpanded] = useState<number | null>(null);
  const [favorites, setFavorites] = useState<number[]>(() =>
    JSON.parse(localStorage.getItem('asma_favorites') || '[]')
  );

  const toggleFav = (num: number) => {
    setFavorites(prev => {
      const updated = prev.includes(num) ? prev.filter(n => n !== num) : [...prev, num];
      localStorage.setItem('asma_favorites', JSON.stringify(updated));
      return updated;
    });
  };

  const filtered = useMemo(() => {
    if (!search.trim()) return NAMES;
    const q = search.trim();
    return NAMES.filter(n =>
      n.ar.includes(q) || n.meaning.includes(q) || (n.en && n.en.toLowerCase().includes(q.toLowerCase())) || (n.meaningEn && n.meaningEn.toLowerCase().includes(q.toLowerCase())) || String(n.num) === q
    );
  }, [search]);

  return (
    <div className="min-h-screen pb-24" dir={dir} data-testid="asma-al-husna-page">
      {/* Header */}
      <div className="relative bg-gradient-to-br from-emerald-900 via-teal-900 to-green-900 px-4 pb-14 pt-safe-header text-center overflow-hidden">
        <div className="absolute inset-0 opacity-[0.06]" style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'80\' height=\'80\' viewBox=\'0 0 80 80\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M40 0L50 15H30zM0 40L15 50V30zM80 40L65 30V50zM40 80L30 65H50z\' fill=\'%23fff\' fill-opacity=\'.3\'/%3E%3C/svg%3E")' }} />
        <div className="relative pt-4">
          <div className="h-16 w-16 mx-auto mb-3 rounded-2xl bg-white/10 backdrop-blur-sm flex items-center justify-center">
            <span className="text-3xl font-arabic text-white font-bold">99</span>
          </div>
          <h1 className="text-2xl font-bold text-white font-arabic mb-1">{t('namesOfAllahTitle')}</h1>
          <p className="text-white/60 text-sm">{t('namesOfAllahVerse')}</p>
          <button
            onClick={() => setShowSearch(!showSearch)}
            className="mt-3 inline-flex items-center gap-2 bg-white/10 rounded-full px-4 py-2 text-white/80 text-sm"
            data-testid="asma-search-toggle"
          >
            {showSearch ? <X className="h-4 w-4" /> : <Search className="h-4 w-4" />}
            {showSearch ? t('hideSearch') : t('searchLabel')}
          </button>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Search */}
      <AnimatePresence>
        {showSearch && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="px-5 pt-2 mb-4 overflow-hidden">
            <Input placeholder={t('searchByNameOrMeaning')} value={search} onChange={e => setSearch(e.target.value)} className="rounded-2xl bg-card" autoFocus data-testid="asma-search-input" />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Counter */}
      <div className="px-5 mb-4">
        <p className="text-xs text-muted-foreground text-center">{filtered.length} {t('nameCount')}</p>
      </div>

      {/* Names Grid */}
      <div className="px-4 grid grid-cols-2 sm:grid-cols-3 gap-3">
        {filtered.map((name, i) => {
          const colorClass = COLORS[name.num % COLORS.length];
          const isExpanded = expanded === name.num;
          const isFav = favorites.includes(name.num);

          return (
            <motion.div
              key={name.num}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: Math.min(i * 0.02, 0.5) }}
              className={cn(
                'rounded-2xl border bg-gradient-to-br overflow-hidden transition-all cursor-pointer active:scale-[0.97]',
                colorClass
              )}
              onClick={() => setExpanded(isExpanded ? null : name.num)}
              data-testid={`asma-name-${name.num}`}
            >
              <div className="p-4 text-center">
                <div className="flex items-center justify-between mb-2">
                  <button
                    onClick={(e) => { e.stopPropagation(); toggleFav(name.num); }}
                    className="p-1"
                  >
                    <Heart className={cn('h-3.5 w-3.5', isFav ? 'fill-rose-500 text-rose-500' : 'text-muted-foreground/40')} />
                  </button>
                  <span className="text-[10px] font-bold text-muted-foreground bg-background/50 rounded-full px-2 py-0.5">
                    {name.num}
                  </span>
                </div>
                <p className="text-xl font-arabic font-bold text-foreground leading-relaxed mb-1">
                  {isAr ? name.ar : (name.en || name.ar)}
                </p>
                <AnimatePresence>
                  {isExpanded && (
                    <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }}>
                      <p className="text-xs text-muted-foreground leading-relaxed mt-2 border-t border-border/30 pt-2">
                        {isAr ? name.meaning : (name.meaningEn || name.meaning)}
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
                {!isExpanded && (
                  <ChevronDown className="h-3 w-3 text-muted-foreground/30 mx-auto mt-1" />
                )}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Hadith footer */}
      <div className="px-5 mt-6 mb-4">
        <div className="rounded-2xl bg-muted/50 border border-border/30 p-4 text-center">
          <p className="text-sm text-foreground leading-relaxed">
            {isAr ? 'قال رسول الله صلى الله عليه وسلم: "إنّ لله تسعة وتسعين اسماً مائة إلا واحداً من أحصاها دخل الجنة"' : 'The Prophet ﷺ said: "Allah has ninety-nine names, one hundred minus one, whoever memorizes them will enter Paradise"'}
          </p>
          <p className="text-[10px] text-muted-foreground mt-2">{isAr ? 'رواه البخاري ومسلم' : 'Bukhari & Muslim'}</p>
        </div>
      </div>
    </div>
  );
}
