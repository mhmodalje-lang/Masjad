import { useState, useMemo } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { motion, AnimatePresence } from 'framer-motion';
import { Search, X, Heart, ChevronDown } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

const NAMES = [
  { num: 1, ar: 'الرَّحْمَنُ', meaning: 'الذي وسعت رحمته كل شيء' },
  { num: 2, ar: 'الرَّحِيمُ', meaning: 'الذي يرحم عباده المؤمنين' },
  { num: 3, ar: 'المَلِكُ', meaning: 'المالك لكل شيء، المتصرف في خلقه' },
  { num: 4, ar: 'القُدُّوسُ', meaning: 'المنزه عن كل عيب ونقص' },
  { num: 5, ar: 'السَّلَامُ', meaning: 'السالم من كل عيب وآفة' },
  { num: 6, ar: 'المُؤْمِنُ', meaning: 'الذي يُصَدِّق عباده ويؤمنهم من عذابه' },
  { num: 7, ar: 'المُهَيْمِنُ', meaning: 'الشاهد على خلقه، المسيطر عليهم' },
  { num: 8, ar: 'العَزِيزُ', meaning: 'الغالب الذي لا يُغلب' },
  { num: 9, ar: 'الجَبَّارُ', meaning: 'الذي يجبر كسر عباده ويُصلح أحوالهم' },
  { num: 10, ar: 'المُتَكَبِّرُ', meaning: 'المتعالي عن صفات الخلق' },
  { num: 11, ar: 'الخَالِقُ', meaning: 'الذي أوجد الأشياء من العدم' },
  { num: 12, ar: 'البَارِئُ', meaning: 'الذي خلق الخلق لا على مثال سابق' },
  { num: 13, ar: 'المُصَوِّرُ', meaning: 'الذي صوّر جميع المخلوقات' },
  { num: 14, ar: 'الغَفَّارُ', meaning: 'الذي يغفر الذنوب مرة بعد مرة' },
  { num: 15, ar: 'القَهَّارُ', meaning: 'الذي قهر جميع المخلوقات' },
  { num: 16, ar: 'الوَهَّابُ', meaning: 'الذي يهب النعم بلا عوض' },
  { num: 17, ar: 'الرَّزَّاقُ', meaning: 'الذي يرزق جميع المخلوقات' },
  { num: 18, ar: 'الفَتَّاحُ', meaning: 'الذي يفتح أبواب الرزق والرحمة' },
  { num: 19, ar: 'العَلِيمُ', meaning: 'الذي يعلم كل شيء ظاهره وباطنه' },
  { num: 20, ar: 'القَابِضُ', meaning: 'الذي يقبض الأرزاق والأرواح' },
  { num: 21, ar: 'البَاسِطُ', meaning: 'الذي يبسط الرزق لمن يشاء' },
  { num: 22, ar: 'الخَافِضُ', meaning: 'الذي يخفض من يشاء' },
  { num: 23, ar: 'الرَّافِعُ', meaning: 'الذي يرفع من يشاء بالعز والطاعة' },
  { num: 24, ar: 'المُعِزُّ', meaning: 'الذي يهب العزة لمن يشاء' },
  { num: 25, ar: 'المُذِلُّ', meaning: 'الذي يذل من يشاء من الطغاة' },
  { num: 26, ar: 'السَّمِيعُ', meaning: 'الذي يسمع كل شيء' },
  { num: 27, ar: 'البَصِيرُ', meaning: 'الذي يرى كل شيء' },
  { num: 28, ar: 'الحَكَمُ', meaning: 'الحاكم العدل بين خلقه' },
  { num: 29, ar: 'العَدْلُ', meaning: 'العادل الذي لا يظلم أحداً' },
  { num: 30, ar: 'اللَّطِيفُ', meaning: 'الرفيق بعباده الذي يوصل لهم مصالحهم' },
  { num: 31, ar: 'الخَبِيرُ', meaning: 'العالم بحقائق الأشياء وبواطنها' },
  { num: 32, ar: 'الحَلِيمُ', meaning: 'الذي لا يعاجل بالعقوبة' },
  { num: 33, ar: 'العَظِيمُ', meaning: 'ذو العظمة المطلقة في ذاته وصفاته' },
  { num: 34, ar: 'الغَفُورُ', meaning: 'الذي يكثر من المغفرة' },
  { num: 35, ar: 'الشَّكُورُ', meaning: 'الذي يشكر اليسير من العمل ويثيب عليه' },
  { num: 36, ar: 'العَلِيُّ', meaning: 'المتعالي فوق خلقه بذاته وصفاته' },
  { num: 37, ar: 'الكَبِيرُ', meaning: 'ذو الكبرياء والعظمة' },
  { num: 38, ar: 'الحَفِيظُ', meaning: 'الذي يحفظ كل شيء' },
  { num: 39, ar: 'المُقِيتُ', meaning: 'الذي يقيت الخلائق ويوصل لهم أرزاقهم' },
  { num: 40, ar: 'الحَسِيبُ', meaning: 'الكافي الذي يحاسب عباده' },
  { num: 41, ar: 'الجَلِيلُ', meaning: 'ذو الجلال والعظمة' },
  { num: 42, ar: 'الكَرِيمُ', meaning: 'الكثير الخير الجواد المعطي' },
  { num: 43, ar: 'الرَّقِيبُ', meaning: 'المطلع على ما أكنّته الصدور' },
  { num: 44, ar: 'المُجِيبُ', meaning: 'الذي يجيب دعاء الداعي' },
  { num: 45, ar: 'الوَاسِعُ', meaning: 'الذي وسع رزقه جميع خلقه' },
  { num: 46, ar: 'الحَكِيمُ', meaning: 'الذي يضع كل شيء في موضعه' },
  { num: 47, ar: 'الوَدُودُ', meaning: 'المحب لعباده المؤمنين' },
  { num: 48, ar: 'المَجِيدُ', meaning: 'ذو المجد والشرف العظيم' },
  { num: 49, ar: 'البَاعِثُ', meaning: 'الذي يبعث الخلق يوم القيامة' },
  { num: 50, ar: 'الشَّهِيدُ', meaning: 'المطلع على كل شيء لا يغيب عنه شيء' },
  { num: 51, ar: 'الحَقُّ', meaning: 'الموجود حقاً الثابت بلا شك' },
  { num: 52, ar: 'الوَكِيلُ', meaning: 'الذي يتولى أمور خلقه' },
  { num: 53, ar: 'القَوِيُّ', meaning: 'التام القدرة الذي لا يعجزه شيء' },
  { num: 54, ar: 'المَتِينُ', meaning: 'شديد القوة الذي لا يلحقه ضعف' },
  { num: 55, ar: 'الوَلِيُّ', meaning: 'الناصر لعباده المؤمنين' },
  { num: 56, ar: 'الحَمِيدُ', meaning: 'المحمود المستحق للحمد' },
  { num: 57, ar: 'المُحْصِي', meaning: 'الذي أحصى كل شيء عدداً' },
  { num: 58, ar: 'المُبْدِئُ', meaning: 'الذي بدأ خلق الأشياء' },
  { num: 59, ar: 'المُعِيدُ', meaning: 'الذي يعيد الخلق بعد الموت' },
  { num: 60, ar: 'المُحْيِي', meaning: 'الذي يحيي الموتى ويهب الحياة' },
  { num: 61, ar: 'المُمِيتُ', meaning: 'الذي يميت الأحياء' },
  { num: 62, ar: 'الحَيُّ', meaning: 'الحي الذي لا يموت' },
  { num: 63, ar: 'القَيُّومُ', meaning: 'القائم بذاته المقيم لغيره' },
  { num: 64, ar: 'الوَاجِدُ', meaning: 'الغني الذي لا يفتقر لشيء' },
  { num: 65, ar: 'المَاجِدُ', meaning: 'التام الكمال ذو الشرف والسلطان' },
  { num: 66, ar: 'الوَاحِدُ', meaning: 'المنفرد بذاته وصفاته وأفعاله' },
  { num: 67, ar: 'الصَّمَدُ', meaning: 'الذي يصمد إليه في الحوائج' },
  { num: 68, ar: 'القَادِرُ', meaning: 'الذي يقدر على ما يشاء' },
  { num: 69, ar: 'المُقْتَدِرُ', meaning: 'التام القدرة الذي لا يمتنع عليه شيء' },
  { num: 70, ar: 'المُقَدِّمُ', meaning: 'الذي يقدم من يشاء' },
  { num: 71, ar: 'المُؤَخِّرُ', meaning: 'الذي يؤخر من يشاء' },
  { num: 72, ar: 'الأَوَّلُ', meaning: 'الذي ليس قبله شيء' },
  { num: 73, ar: 'الآخِرُ', meaning: 'الذي ليس بعده شيء' },
  { num: 74, ar: 'الظَّاهِرُ', meaning: 'الذي ظهر فوق كل شيء' },
  { num: 75, ar: 'البَاطِنُ', meaning: 'المحتجب عن أبصار الخلق' },
  { num: 76, ar: 'الوَالِي', meaning: 'المالك لكل شيء المتصرف فيه' },
  { num: 77, ar: 'المُتَعَالِي', meaning: 'المتعالي عن صفات المخلوقين' },
  { num: 78, ar: 'البَرُّ', meaning: 'العطوف الرحيم بعباده' },
  { num: 79, ar: 'التَّوَّابُ', meaning: 'الذي يقبل التوبة عن عباده' },
  { num: 80, ar: 'المُنْتَقِمُ', meaning: 'الذي ينتقم من المجرمين بعدله' },
  { num: 81, ar: 'العَفُوُّ', meaning: 'الذي يعفو عن الذنوب' },
  { num: 82, ar: 'الرَّؤُوفُ', meaning: 'ذو الرأفة والرحمة الشديدة' },
  { num: 83, ar: 'مَالِكُ المُلْكِ', meaning: 'المالك لجميع الأملاك' },
  { num: 84, ar: 'ذُو الجَلَالِ وَالإِكْرَامِ', meaning: 'المستحق للتعظيم والإكرام' },
  { num: 85, ar: 'المُقْسِطُ', meaning: 'العادل في حكمه' },
  { num: 86, ar: 'الجَامِعُ', meaning: 'الذي يجمع الخلائق يوم القيامة' },
  { num: 87, ar: 'الغَنِيُّ', meaning: 'المستغني عن كل شيء' },
  { num: 88, ar: 'المُغْنِي', meaning: 'الذي يغني من يشاء من خلقه' },
  { num: 89, ar: 'المَانِعُ', meaning: 'الذي يمنع العطاء عمن يشاء لحكمة' },
  { num: 90, ar: 'الضَّارُّ', meaning: 'الذي يقدر الضر على من يشاء' },
  { num: 91, ar: 'النَّافِعُ', meaning: 'الذي يقدر النفع لمن يشاء' },
  { num: 92, ar: 'النُّورُ', meaning: 'نور السماوات والأرض' },
  { num: 93, ar: 'الهَادِي', meaning: 'الذي يهدي عباده للحق' },
  { num: 94, ar: 'البَدِيعُ', meaning: 'الذي أبدع الخلق بلا مثال' },
  { num: 95, ar: 'البَاقِي', meaning: 'الدائم الذي لا يفنى' },
  { num: 96, ar: 'الوَارِثُ', meaning: 'الباقي بعد فناء خلقه' },
  { num: 97, ar: 'الرَّشِيدُ', meaning: 'المرشد لعباده إلى ما فيه صلاحهم' },
  { num: 98, ar: 'الصَّبُورُ', meaning: 'الذي لا يعاجل العصاة بالعقوبة' },
  { num: 99, ar: 'اللَّهُ', meaning: 'الاسم الأعظم الجامع لجميع الأسماء والصفات' },
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
  const { t, dir } = useLocale();
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
      n.ar.includes(q) || n.meaning.includes(q) || String(n.num) === q
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
          <h1 className="text-2xl font-bold text-white font-arabic mb-1">أسماء الله الحسنى</h1>
          <p className="text-white/60 text-sm">وللّه الأسماء الحسنى فادعوه بها</p>
          <button
            onClick={() => setShowSearch(!showSearch)}
            className="mt-3 inline-flex items-center gap-2 bg-white/10 rounded-full px-4 py-2 text-white/80 text-sm"
            data-testid="asma-search-toggle"
          >
            {showSearch ? <X className="h-4 w-4" /> : <Search className="h-4 w-4" />}
            {showSearch ? 'إخفاء البحث' : 'بحث'}
          </button>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Search */}
      <AnimatePresence>
        {showSearch && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="px-5 pt-2 mb-4 overflow-hidden">
            <Input placeholder="ابحث بالاسم أو المعنى أو الرقم..." value={search} onChange={e => setSearch(e.target.value)} className="rounded-2xl bg-card" autoFocus data-testid="asma-search-input" />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Counter */}
      <div className="px-5 mb-4">
        <p className="text-xs text-muted-foreground text-center">{filtered.length} اسم</p>
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
                  {name.ar}
                </p>
                <AnimatePresence>
                  {isExpanded && (
                    <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }}>
                      <p className="text-xs text-muted-foreground leading-relaxed mt-2 border-t border-border/30 pt-2">
                        {name.meaning}
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
          <p className="text-sm font-arabic text-foreground leading-relaxed">
            قال رسول الله صلى الله عليه وسلم: "إنّ لله تسعة وتسعين اسماً مائة إلا واحداً من أحصاها دخل الجنة"
          </p>
          <p className="text-[10px] text-muted-foreground mt-2">رواه البخاري ومسلم</p>
        </div>
      </div>
    </div>
  );
}
