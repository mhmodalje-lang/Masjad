import { useState } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { Link } from 'react-router-dom';
import { ChevronLeft, ChevronRight, BookOpen, Search, Check, RotateCcw } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

// The 40 Nawawi Hadiths - Arabic text is always shown, translations via i18n
const HADITHS = [
  { id: 1, arabic: 'إنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى', narrator: 'عمر بن الخطاب', source: 'البخاري ومسلم', key: 'nawawiH1' },
  { id: 2, arabic: 'بَيْنَمَا نَحْنُ جُلُوسٌ عِنْدَ رَسُولِ اللَّهِ ﷺ ذَاتَ يَوْمٍ، إذْ طَلَعَ عَلَيْنَا رَجُلٌ شَدِيدُ بَيَاضِ الثِّيَابِ', narrator: 'عمر بن الخطاب', source: 'مسلم', key: 'nawawiH2' },
  { id: 3, arabic: 'بُنِيَ الإِسْلامُ عَلَى خَمْسٍ: شَهَادَةِ أَنْ لا إلَهَ إلا اللَّهُ وَأَنَّ مُحَمَّدًا رَسُولُ اللَّهِ', narrator: 'عبد الله بن عمر', source: 'البخاري ومسلم', key: 'nawawiH3' },
  { id: 4, arabic: 'إنَّ أَحَدَكُمْ يُجْمَعُ خَلْقُهُ فِي بَطْنِ أُمِّهِ أَرْبَعِينَ يَوْمًا نُطْفَةً', narrator: 'عبد الله بن مسعود', source: 'البخاري ومسلم', key: 'nawawiH4' },
  { id: 5, arabic: 'مَنْ أَحْدَثَ فِي أَمْرِنَا هَذَا مَا لَيْسَ مِنْهُ فَهُوَ رَدٌّ', narrator: 'عائشة أم المؤمنين', source: 'البخاري ومسلم', key: 'nawawiH5' },
  { id: 6, arabic: 'إنَّ الْحَلالَ بَيِّنٌ، وَإِنَّ الْحَرَامَ بَيِّنٌ، وَبَيْنَهُمَا أُمُورٌ مُشْتَبِهَاتٌ', narrator: 'النعمان بن بشير', source: 'البخاري ومسلم', key: 'nawawiH6' },
  { id: 7, arabic: 'الدِّينُ النَّصِيحَةُ. قُلْنَا: لِمَنْ؟ قَالَ: لِلَّهِ وَلِكِتَابِهِ وَلِرَسُولِهِ وَلأَئِمَّةِ الْمُسْلِمِينَ وَعَامَّتِهِمْ', narrator: 'تميم الداري', source: 'مسلم', key: 'nawawiH7' },
  { id: 8, arabic: 'أُمِرْتُ أَنْ أُقَاتِلَ النَّاسَ حَتَّى يَشْهَدُوا أَنْ لا إلَهَ إلا اللَّهُ وَأَنَّ مُحَمَّدًا رَسُولُ اللَّهِ', narrator: 'عبد الله بن عمر', source: 'البخاري ومسلم', key: 'nawawiH8' },
  { id: 9, arabic: 'مَا نَهَيْتُكُمْ عَنْهُ فَاجْتَنِبُوهُ، وَمَا أَمَرْتُكُمْ بِهِ فَأْتُوا مِنْهُ مَا اسْتَطَعْتُمْ', narrator: 'أبو هريرة', source: 'البخاري ومسلم', key: 'nawawiH9' },
  { id: 10, arabic: 'إنَّ اللَّهَ طَيِّبٌ لا يَقْبَلُ إلا طَيِّبًا', narrator: 'أبو هريرة', source: 'مسلم', key: 'nawawiH10' },
  { id: 11, arabic: 'دَعْ مَا يَرِيبُك إلَى مَا لا يَرِيبُك', narrator: 'الحسن بن علي', source: 'الترمذي والنسائي', key: 'nawawiH11' },
  { id: 12, arabic: 'مِنْ حُسْنِ إسْلامِ الْمَرْءِ تَرْكُهُ مَا لا يَعْنِيهِ', narrator: 'أبو هريرة', source: 'الترمذي', key: 'nawawiH12' },
  { id: 13, arabic: 'لا يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ', narrator: 'أنس بن مالك', source: 'البخاري ومسلم', key: 'nawawiH13' },
  { id: 14, arabic: 'لا يَحِلُّ دَمُ امْرِئٍ مُسْلِمٍ إلا بِإِحْدَى ثَلاثٍ', narrator: 'عبد الله بن مسعود', source: 'البخاري ومسلم', key: 'nawawiH14' },
  { id: 15, arabic: 'مَنْ كَانَ يُؤْمِنُ بِاَللَّهِ وَالْيَوْمِ الآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ', narrator: 'أبو هريرة', source: 'البخاري ومسلم', key: 'nawawiH15' },
  { id: 16, arabic: 'لا تَغْضَبْ، فَرَدَّدَ مِرَارًا، قَالَ: لا تَغْضَبْ', narrator: 'أبو هريرة', source: 'البخاري', key: 'nawawiH16' },
  { id: 17, arabic: 'إنَّ اللَّهَ كَتَبَ الإِحْسَانَ عَلَى كُلِّ شَيْءٍ', narrator: 'شداد بن أوس', source: 'مسلم', key: 'nawawiH17' },
  { id: 18, arabic: 'اتَّقِ اللَّهَ حَيْثُمَا كُنْت، وَأَتْبِعِ السَّيِّئَةَ الْحَسَنَةَ تَمْحُهَا، وَخَالِقِ النَّاسَ بِخُلُقٍ حَسَنٍ', narrator: 'أبو ذر وَمعاذ', source: 'الترمذي', key: 'nawawiH18' },
  { id: 19, arabic: 'يَا غُلامُ، إنِّي أُعَلِّمُك كَلِمَاتٍ: احْفَظِ اللَّهَ يَحْفَظْك', narrator: 'عبد الله بن عباس', source: 'الترمذي', key: 'nawawiH19' },
  { id: 20, arabic: 'إنَّ مِمَّا أَدْرَكَ النَّاسُ مِنْ كَلامِ النُّبُوَّةِ الأُولَى: إذَا لَمْ تَسْتَحِ فَاصْنَعْ مَا شِئْت', narrator: 'أبو مسعود', source: 'البخاري', key: 'nawawiH20' },
  { id: 21, arabic: 'قُلْ آمَنْت بِاَللَّهِ ثُمَّ اسْتَقِمْ', narrator: 'سفيان بن عبد الله', source: 'مسلم', key: 'nawawiH21' },
  { id: 22, arabic: 'أَرَأَيْتَ إذَا صَلَّيْتُ الْمَكْتُوبَاتِ، وَصُمْتُ رَمَضَانَ، وَأَحْلَلْتُ الْحَلالَ، وَحَرَّمْت الْحَرَامَ، أَأَدْخُلُ الْجَنَّةَ؟ قَالَ: نَعَمْ', narrator: 'أبو عبد الله جابر', source: 'مسلم', key: 'nawawiH22' },
  { id: 23, arabic: 'الطُّهُورُ شَطْرُ الإِيمَانِ، وَالْحَمْدُ لِلَّهِ تَمْلأُ الْمِيزَانَ', narrator: 'أبو مالك الأشعري', source: 'مسلم', key: 'nawawiH23' },
  { id: 24, arabic: 'يَا عِبَادِي، إنِّي حَرَّمْت الظُّلْمَ عَلَى نَفْسِي وَجَعَلْتُهُ بَيْنَكُمْ مُحَرَّمًا فَلا تَظَالَمُوا', narrator: 'أبو ذر الغفاري', source: 'مسلم', key: 'nawawiH24' },
  { id: 25, arabic: 'إنَّ بِكُلِّ تَسْبِيحَةٍ صَدَقَةً، وَكُلِّ تَكْبِيرَةٍ صَدَقَةً، وَكُلِّ تَحْمِيدَةٍ صَدَقَةً', narrator: 'أبو ذر', source: 'مسلم', key: 'nawawiH25' },
  { id: 26, arabic: 'كُلُّ سُلامَى مِنَ النَّاسِ عَلَيْهِ صَدَقَةٌ، كُلَّ يَوْمٍ تَطْلُعُ فِيهِ الشَّمْسُ', narrator: 'أبو هريرة', source: 'البخاري ومسلم', key: 'nawawiH26' },
  { id: 27, arabic: 'الْبِرُّ حُسْنُ الْخُلُقِ، وَالإِثْمُ مَا حَاكَ فِي صَدْرِك وَكَرِهْتَ أَنْ يَطَّلِعَ عَلَيْهِ النَّاسُ', narrator: 'النواس بن سمعان', source: 'مسلم', key: 'nawawiH27' },
  { id: 28, arabic: 'أُوصِيكُمْ بِتَقْوَى اللَّهِ، وَالسَّمْعِ وَالطَّاعَةِ وَإِنْ تَأَمَّرَ عَلَيْكُمْ عَبْدٌ', narrator: 'أبو نجيح العرباض', source: 'أبو داود والترمذي', key: 'nawawiH28' },
  { id: 29, arabic: 'يَا رَسُولَ اللَّهِ، أَخْبِرْنِي بِعَمَلٍ يُدْخِلُنِي الْجَنَّةَ وَيُبَاعِدُنِي عَنِ النَّارِ', narrator: 'معاذ بن جبل', source: 'الترمذي', key: 'nawawiH29' },
  { id: 30, arabic: 'إنَّ اللَّهَ فَرَضَ فَرَائِضَ فَلا تُضَيِّعُوهَا، وَحَدَّ حُدُودًا فَلا تَعْتَدُوهَا', narrator: 'أبو ثعلبة الخشني', source: 'الدارقطني', key: 'nawawiH30' },
  { id: 31, arabic: 'ازْهَدْ فِي الدُّنْيَا يُحِبَّك اللَّهُ، وَازْهَدْ فِيمَا عِنْدَ النَّاسِ يُحِبَّك النَّاسُ', narrator: 'سهل بن سعد', source: 'ابن ماجه', key: 'nawawiH31' },
  { id: 32, arabic: 'لا ضَرَرَ وَلا ضِرَارَ', narrator: 'أبو سعيد الخدري', source: 'ابن ماجه والدارقطني', key: 'nawawiH32' },
  { id: 33, arabic: 'لَوْ يُعْطَى النَّاسُ بِدَعْوَاهُمْ لادَّعَى رِجَالٌ أَمْوَالَ قَوْمٍ وَدِمَاءَهُمْ', narrator: 'عبد الله بن عباس', source: 'البيهقي', key: 'nawawiH33' },
  { id: 34, arabic: 'مَنْ رَأَى مِنْكُمْ مُنْكَرًا فَلْيُغَيِّرْهُ بِيَدِهِ، فَإِنْ لَمْ يَسْتَطِعْ فَبِلِسَانِهِ', narrator: 'أبو سعيد الخدري', source: 'مسلم', key: 'nawawiH34' },
  { id: 35, arabic: 'لا تَحَاسَدُوا، وَلا تَنَاجَشُوا، وَلا تَبَاغَضُوا، وَلا تَدَابَرُوا', narrator: 'أبو هريرة', source: 'مسلم', key: 'nawawiH35' },
  { id: 36, arabic: 'مَنْ نَفَّسَ عَنْ مُؤْمِنٍ كُرْبَةً مِنْ كُرَبِ الدُّنْيَا نَفَّسَ اللَّهُ عَنْهُ كُرْبَةً مِنْ كُرَبِ يَوْمِ الْقِيَامَةِ', narrator: 'أبو هريرة', source: 'مسلم', key: 'nawawiH36' },
  { id: 37, arabic: 'إنَّ اللَّهَ كَتَبَ الْحَسَنَاتِ وَالسَّيِّئَاتِ ثُمَّ بَيَّنَ ذَلِكَ', narrator: 'عبد الله بن عباس', source: 'البخاري ومسلم', key: 'nawawiH37' },
  { id: 38, arabic: 'مَنْ عَادَى لِي وَلِيًّا فَقَدْ آذَنْتُهُ بِالْحَرْبِ', narrator: 'أبو هريرة', source: 'البخاري', key: 'nawawiH38' },
  { id: 39, arabic: 'إنَّ اللَّهَ تَجَاوَزَ لِي عَنْ أُمَّتِي الْخَطَأَ وَالنِّسْيَانَ وَمَا اسْتُكْرِهُوا عَلَيْهِ', narrator: 'عبد الله بن عباس', source: 'ابن ماجه والبيهقي', key: 'nawawiH39' },
  { id: 40, arabic: 'كُنْ فِي الدُّنْيَا كَأَنَّك غَرِيبٌ أَوْ عَابِرُ سَبِيلٍ', narrator: 'عبد الله بن عمر', source: 'البخاري', key: 'nawawiH40' },
];

export default function FortyNawawi() {
  const { t, isRTL, locale } = useLocale();
  const [searchQuery, setSearchQuery] = useState('');
  const [memorized, setMemorized] = useState<Set<number>>(() => {
    const saved = localStorage.getItem('nawawi-memorized');
    return saved ? new Set(JSON.parse(saved)) : new Set();
  });

  const toggleMemorized = (id: number) => {
    const updated = new Set(memorized);
    if (updated.has(id)) {
      updated.delete(id);
    } else {
      updated.add(id);
    }
    setMemorized(updated);
    localStorage.setItem('nawawi-memorized', JSON.stringify([...updated]));
  };

  const resetAll = () => {
    setMemorized(new Set());
    localStorage.removeItem('nawawi-memorized');
  };

  const filtered = HADITHS.filter(h =>
    searchQuery === '' ||
    h.arabic.includes(searchQuery) ||
    h.narrator.includes(searchQuery) ||
    String(h.id).includes(searchQuery) ||
    t(h.key + 'Title').toLowerCase().includes(searchQuery.toLowerCase())
  );

  const progress = (memorized.size / 40) * 100;

  return (
    <div className="min-h-screen pb-24 bg-background" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="sticky top-0 z-50 glass-nav bg-background/80 border-b border-border/10 px-4 h-12 flex items-center gap-3">
        <Link to="/" className="p-1.5 rounded-xl hover:bg-muted/50">
          {isRTL ? <ChevronRight className="h-5 w-5 text-foreground" /> : <ChevronLeft className="h-5 w-5 text-foreground" />}
        </Link>
        <div className="flex-1 min-w-0">
          <h1 className="text-base font-black text-foreground truncate">{t('fortyNawawiTitle')}</h1>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-[10px] font-bold text-primary bg-primary/10 px-2 py-0.5 rounded-full">
            {memorized.size}/40
          </span>
        </div>
      </div>

      {/* Hero Card */}
      <div className="px-4 pt-4 pb-2">
        <div className="rounded-3xl bg-gradient-to-br from-red-500/10 to-amber-500/5 border border-red-500/20 p-5 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-red-500/10 to-transparent rounded-bl-full" />
          <div className="flex items-center gap-3 mb-3">
            <span className="text-3xl">📕</span>
            <div>
              <h2 className="text-lg font-black text-foreground">{t('fortyNawawiTitle')}</h2>
              <p className="text-xs text-muted-foreground">{t('fortyNawawiSubtitle')}</p>
            </div>
          </div>
          {/* Progress bar */}
          <div className="flex items-center gap-3 mt-3">
            <div className="flex-1 h-2 bg-border/30 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-red-500 to-amber-500 rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
            <span className="text-[11px] font-bold text-foreground tabular-nums">{Math.round(progress)}%</span>
            {memorized.size > 0 && (
              <button onClick={resetAll} className="p-1.5 rounded-lg hover:bg-muted/50">
                <RotateCcw className="h-3.5 w-3.5 text-muted-foreground" />
              </button>
            )}
          </div>
          <p className="text-[11px] text-muted-foreground mt-2">{t('fortyNawawiProgress')}</p>
        </div>
      </div>

      {/* Search */}
      <div className="px-4 py-3">
        <div className="relative">
          <Search className="absolute top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" style={{ [isRTL ? 'right' : 'left']: '12px' }} />
          <input
            type="text"
            placeholder={t('fortyNawawiSearch')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full h-10 rounded-2xl bg-muted/30 border border-border/30 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-primary/30 transition-colors"
            style={{ [isRTL ? 'paddingRight' : 'paddingLeft']: '40px', [isRTL ? 'paddingLeft' : 'paddingRight']: '16px' }}
          />
        </div>
      </div>

      {/* Hadiths List */}
      <div className="px-4 space-y-3 pb-4">
        {filtered.map((hadith, i) => {
          const isMemorized = memorized.has(hadith.id);
          return (
            <motion.div
              key={hadith.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.02 }}
              className={cn(
                'rounded-2xl border p-4 transition-all',
                isMemorized
                  ? 'border-primary/30 bg-primary/5'
                  : 'border-border/40 bg-card'
              )}
            >
              {/* Hadith number and memorize button */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className={cn(
                    'h-8 w-8 rounded-full flex items-center justify-center text-xs font-black',
                    isMemorized
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-red-500/10 text-red-500'
                  )}>
                    {hadith.id}
                  </span>
                  <span className="text-[11px] text-muted-foreground font-medium">
                    {t('fortyNawawiHadithLabel')} #{hadith.id}
                  </span>
                </div>
                <button
                  onClick={() => toggleMemorized(hadith.id)}
                  className={cn(
                    'h-8 px-3 rounded-xl flex items-center gap-1.5 text-[11px] font-bold transition-all active:scale-95',
                    isMemorized
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted/50 text-muted-foreground hover:bg-primary/10 hover:text-primary'
                  )}
                >
                  <Check className="h-3.5 w-3.5" />
                  {isMemorized ? t('fortyNawawiMemorized') : t('fortyNawawiMarkMemorized')}
                </button>
              </div>

              {/* Arabic text - always shown */}
              <p className="text-base font-arabic text-foreground leading-[2.2] mb-3" dir="rtl">
                «{hadith.arabic}»
              </p>

              {/* Translation (if not Arabic) */}
              {locale !== 'ar' && (
                <p className="text-sm text-muted-foreground leading-relaxed mb-3" dir="auto">
                  {t(hadith.key + 'Title')}
                </p>
              )}

              {/* Narrator and source */}
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-[10px] font-bold text-primary bg-primary/10 px-2 py-0.5 rounded-full">
                  {t('fortyNawawiNarrator')}: {hadith.narrator}
                </span>
                <span className="text-[10px] font-medium text-muted-foreground bg-muted/50 px-2 py-0.5 rounded-full">
                  {hadith.source}
                </span>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
