import { useState, useEffect, useMemo, useCallback } from 'react';
import { BookOpen, Share2, Sparkles, ChevronLeft, ChevronRight, Heart, RefreshCw } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface DailyContent {
  hadith: { text: string; narrator: string; source: string; arabic_text?: string } | null;
  verse: { text: string; surah: string; ayah: number; surah_number: number; translation?: string } | null;
  dua: { arabic: string; translationKey: string; subtitleKey: string; referenceKey: string } | null;
}

// ============ 30 Daily Duas Collection ============
const DAILY_DUAS = [
  { arabic: 'اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ', subtitleKey: 'duaSubtitleProtection', translationKey: 'duaTranslationAyatKursi', referenceKey: 'refBaqarah255' },
  { arabic: 'اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحُزْنِ، وَالْعَجْزِ وَالْكَسَلِ، وَالْبُخْلِ وَالْجُبْنِ، وَضَلَعِ الدَّيْنِ وَغَلَبَةِ الرِّجَالِ', subtitleKey: 'duaSubtitleRemoveWorry', translationKey: 'duaTranslationAnxiety', referenceKey: 'refBukhari' },
  { arabic: 'اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ', subtitleKey: 'duaSubtitleBestIstighfar', translationKey: 'duaTranslationSayyidIstighfar', referenceKey: 'refBukhari' },
  { arabic: 'اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا، وَرِزْقًا طَيِّبًا، وَعَمَلًا مُتَقَبَّلًا', subtitleKey: 'duaSubtitleRizqBlessing', translationKey: 'duaTranslationRizq', referenceKey: 'refIbnMajah' },
  { arabic: 'اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ', subtitleKey: 'duaSubtitleGoToPrayer', translationKey: 'duaTranslationEnterMosque', referenceKey: 'refMuslim' },
  { arabic: 'بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ', subtitleKey: 'duaSubtitleLeavingHome', translationKey: 'duaTranslationTawakkul', referenceKey: 'refAbuDawud' },
  { arabic: 'اللَّهُمَّ رَبَّ النَّاسِ أَذْهِبِ الْبَأسَ اشْفِهِ وَأَنْتَ الشَّافِي لَا شِفَاءَ إِلَّا شِفَاؤُكَ شِفَاءً لَا يُغَادِرُ سَقَمًا', subtitleKey: 'duaSubtitleForSick', translationKey: 'duaTranslationHealing', referenceKey: 'refBukhariMuslim' },
  { arabic: 'رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ', subtitleKey: 'dailyDua8Sub', translationKey: 'dailyDua8Trans', referenceKey: 'refBaqarah201' },
  { arabic: 'رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي وَاحْلُلْ عُقْدَةً مِنْ لِسَانِي يَفْقَهُوا قَوْلِي', subtitleKey: 'dailyDua9Sub', translationKey: 'dailyDua9Trans', referenceKey: 'refTaha2528' },
  { arabic: 'لَا إِلَٰهَ إِلَّا أَنتَ سُبْحَانَكَ إِنِّي كُنتُ مِنَ الظَّالِمِينَ', subtitleKey: 'dailyDua10Sub', translationKey: 'dailyDua10Trans', referenceKey: 'refAnbiya87' },
  { arabic: 'حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ', subtitleKey: 'dailyDua11Sub', translationKey: 'dailyDua11Trans', referenceKey: 'refAlImran173' },
  { arabic: 'اللَّهُمَّ إِنِّي أَسْأَلُكَ الْهُدَىٰ وَالتُّقَىٰ وَالْعَفَافَ وَالْغِنَىٰ', subtitleKey: 'dailyDua12Sub', translationKey: 'dailyDua12Trans', referenceKey: 'refMuslim' },
  { arabic: 'اللَّهُمَّ أَصْلِحْ لِي دِينِي الَّذِي هُوَ عِصْمَةُ أَمْرِي، وَأَصْلِحْ لِي دُنْيَايَ الَّتِي فِيهَا مَعَاشِي، وَأَصْلِحْ لِي آخِرَتِي الَّتِي فِيهَا مَعَادِي', subtitleKey: 'dailyDua13Sub', translationKey: 'dailyDua13Trans', referenceKey: 'refMuslim' },
  { arabic: 'رَبِّ زِدْنِي عِلْمًا', subtitleKey: 'dailyDua14Sub', translationKey: 'dailyDua14Trans', referenceKey: 'refTaha114' },
  { arabic: 'اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ عِلْمٍ لَا يَنْفَعُ، وَمِنْ قَلْبٍ لَا يَخْشَعُ، وَمِنْ نَفْسٍ لَا تَشْبَعُ، وَمِنْ دَعْوَةٍ لَا يُسْتَجَابُ لَهَا', subtitleKey: 'dailyDua15Sub', translationKey: 'dailyDua15Trans', referenceKey: 'refMuslim' },
  { arabic: 'يَا مُقَلِّبَ الْقُلُوبِ ثَبِّتْ قَلْبِي عَلَى دِينِكَ', subtitleKey: 'dailyDua16Sub', translationKey: 'dailyDua16Trans', referenceKey: 'refTirmidhi' },
  { arabic: 'اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ', subtitleKey: 'dailyDua17Sub', translationKey: 'dailyDua17Trans', referenceKey: 'refAbuDawud' },
  { arabic: 'رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا', subtitleKey: 'dailyDua18Sub', translationKey: 'dailyDua18Trans', referenceKey: 'refFurqan74' },
  { arabic: 'اللَّهُمَّ اغْفِرْ لِي ذَنْبِي كُلَّهُ، دِقَّهُ وَجِلَّهُ، وَأَوَّلَهُ وَآخِرَهُ، وَعَلَانِيَتَهُ وَسِرَّهُ', subtitleKey: 'dailyDua19Sub', translationKey: 'dailyDua19Trans', referenceKey: 'refMuslim' },
  { arabic: 'رَبِّ أَوْزِعْنِي أَنْ أَشْكُرَ نِعْمَتَكَ الَّتِي أَنْعَمْتَ عَلَيَّ وَعَلَىٰ وَالِدَيَّ وَأَنْ أَعْمَلَ صَالِحًا تَرْضَاهُ', subtitleKey: 'dailyDua20Sub', translationKey: 'dailyDua20Trans', referenceKey: 'refNaml19' },
  { arabic: 'اللَّهُمَّ إِنِّي أَسْأَلُكَ الْجَنَّةَ وَأَعُوذُ بِكَ مِنَ النَّارِ', subtitleKey: 'dailyDua21Sub', translationKey: 'dailyDua21Trans', referenceKey: 'refAbuDawud' },
  { arabic: 'اللَّهُمَّ اكْفِنِي بِحَلَالِكَ عَنْ حَرَامِكَ، وَأَغْنِنِي بِفَضْلِكَ عَمَّنْ سِوَاكَ', subtitleKey: 'dailyDua22Sub', translationKey: 'dailyDua22Trans', referenceKey: 'refTirmidhi' },
  { arabic: 'اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي', subtitleKey: 'dailyDua23Sub', translationKey: 'dailyDua23Trans', referenceKey: 'refTirmidhi' },
  { arabic: 'رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِنْ لَدُنْكَ رَحْمَةً إِنَّكَ أَنْتَ الْوَهَّابُ', subtitleKey: 'dailyDua24Sub', translationKey: 'dailyDua24Trans', referenceKey: 'refAlImran8' },
  { arabic: 'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ سُبْحَانَ اللَّهِ الْعَظِيمِ', subtitleKey: 'dailyDua25Sub', translationKey: 'dailyDua25Trans', referenceKey: 'refBukhariMuslim' },
  { arabic: 'لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ', subtitleKey: 'dailyDua26Sub', translationKey: 'dailyDua26Trans', referenceKey: 'refBukhariMuslim' },
  { arabic: 'اللَّهُمَّ بَارِكْ لَنَا فِيمَا رَزَقْتَنَا وَقِنَا عَذَابَ النَّارِ', subtitleKey: 'dailyDua27Sub', translationKey: 'dailyDua27Trans', referenceKey: 'refMuslim' },
  { arabic: 'اللَّهُمَّ آتِ نَفْسِي تَقْوَاهَا وَزَكِّهَا أَنْتَ خَيْرُ مَنْ زَكَّاهَا أَنْتَ وَلِيُّهَا وَمَوْلَاهَا', subtitleKey: 'dailyDua28Sub', translationKey: 'dailyDua28Trans', referenceKey: 'refMuslim' },
  { arabic: 'رَبَّنَا اغْفِرْ لِي وَلِوَالِدَيَّ وَلِلْمُؤْمِنِينَ يَوْمَ يَقُومُ الْحِسَابُ', subtitleKey: 'dailyDua29Sub', translationKey: 'dailyDua29Trans', referenceKey: 'refIbrahim41' },
  { arabic: 'اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ', subtitleKey: 'dailyDua30Sub', translationKey: 'dailyDua30Trans', referenceKey: 'refAbuDawud' },
];

type Tab = 'hadith' | 'verse' | 'dua';

export default function DailyInspiration() {
  const { t, locale, isRTL } = useLocale();
  const [activeTab, setActiveTab] = useState<Tab>('hadith');
  const [content, setContent] = useState<DailyContent>({ hadith: null, verse: null, dua: null });
  const [loading, setLoading] = useState(true);

  // Get today's day number for rotation
  const dayOfYear = useMemo(() => {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 0);
    const diff = now.getTime() - start.getTime();
    return Math.floor(diff / 86400000);
  }, []);

  // Today's dua from expanded collection
  const todayDua = useMemo(() => DAILY_DUAS[dayOfYear % DAILY_DUAS.length], [dayOfYear]);

  // Format hijri date for display
  const todayStr = useMemo(() => new Date().toLocaleDateString(locale === 'ar' ? 'ar-SA' : locale, { weekday: 'long', day: 'numeric', month: 'long' }), [locale]);

  const fetchContent = useCallback(async () => {
    setLoading(true);
    const today = new Date().toISOString().split('T')[0];
    const cacheKey = `daily_inspiration_${today}_${locale}`;
    const cached = localStorage.getItem(cacheKey);

    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        setContent(parsed);
        setLoading(false);
        return;
      } catch {}
    }

    const newContent: DailyContent = { hadith: null, verse: null, dua: todayDua };

    try {
      const [hadithRes, verseRes] = await Promise.allSettled([
        fetch(`${BACKEND_URL}/api/daily-hadith?language=${locale}`).then(r => r.json()),
        fetch(`${BACKEND_URL}/api/ai/verse-of-day?language=${locale}`).then(r => r.json()),
      ]);

      if (hadithRes.status === 'fulfilled' && hadithRes.value.success) {
        newContent.hadith = hadithRes.value.hadith;
      }
      if (verseRes.status === 'fulfilled' && verseRes.value.verse) {
        newContent.verse = verseRes.value.verse;
      }
    } catch {}

    newContent.dua = todayDua;
    setContent(newContent);
    localStorage.setItem(cacheKey, JSON.stringify(newContent));
    setLoading(false);
  }, [locale, todayDua]);

  useEffect(() => { fetchContent(); }, [fetchContent]);

  const tabs: { key: Tab; emoji: string; labelKey: string }[] = [
    { key: 'hadith', emoji: '📿', labelKey: 'hadithOfDay' },
    { key: 'verse', emoji: '📖', labelKey: 'verseOfDay' },
    { key: 'dua', emoji: '🤲', labelKey: 'duaOfDay' },
  ];

  const handleShare = async () => {
    let shareText = '';
    if (activeTab === 'hadith' && content.hadith) {
      shareText = `📿 ${t('hadithOfDay')}\n\n«${content.hadith.arabic_text || content.hadith.text}»\n\n${content.hadith.narrator} - ${content.hadith.source}\n\n— ${t('appName')}`;
    } else if (activeTab === 'verse' && content.verse) {
      shareText = `📖 ${t('verseOfDay')}\n\n${content.verse.text}\n\n${content.verse.surah} : ${content.verse.ayah}\n\n— ${t('appName')}`;
    } else if (activeTab === 'dua' && content.dua) {
      shareText = `🤲 ${t('duaOfDay')}\n\n${content.dua.arabic}\n\n— ${t('appName')}`;
    }
    if (navigator.share) {
      await navigator.share({ text: shareText }).catch(() => {});
    } else if (shareText) {
      await navigator.clipboard.writeText(shareText).catch(() => {});
    }
  };

  if (loading) {
    return (
      <div className="px-4 mb-5">
        <div className="rounded-3xl bg-card border border-border/30 p-6 animate-pulse">
          <div className="h-4 bg-muted/40 rounded-full w-32 mb-4" />
          <div className="h-6 bg-muted/30 rounded-full w-full mb-3" />
          <div className="h-6 bg-muted/30 rounded-full w-3/4 mx-auto" />
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 mb-5">
      <div className="rounded-3xl glass-mystic relative overflow-hidden shadow-card">
        {/* Decorative backgrounds */}
        <div className="absolute -top-10 -right-10 w-40 h-40 bg-[hsl(var(--islamic-green)/0.04)] rounded-full blur-3xl" />
        <div className="absolute -bottom-8 -left-8 w-32 h-32 bg-[hsl(var(--islamic-gold)/0.04)] rounded-full blur-2xl" />

        {/* Header with date */}
        <div className="px-5 pt-5 pb-3 relative z-10">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-[hsl(var(--mystic-amber))]" />
              <span className="text-[11px] font-bold text-[hsl(var(--mystic-amber))] uppercase tracking-wider">
                {t('dailyInspirationTitle')}
              </span>
            </div>
            <button onClick={handleShare} className="p-2 rounded-xl hover:bg-muted/50 transition-all active:scale-90">
              <Share2 className="h-4 w-4 text-muted-foreground" />
            </button>
          </div>

          {/* Date indicator */}
          <p className="text-[10px] text-muted-foreground/70 mb-3">{todayStr}</p>

          {/* Tab switcher */}
          <div className="flex items-center gap-1.5 bg-muted/30 rounded-2xl p-1">
            {tabs.map(tab => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={cn(
                  "flex-1 flex items-center justify-center gap-1.5 py-2 rounded-xl text-[11px] font-bold transition-all",
                  activeTab === tab.key
                    ? "bg-card shadow-sm text-foreground"
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                <span>{tab.emoji}</span>
                <span className="hidden sm:inline">{t(tab.labelKey)}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Content area */}
        <div className="px-5 pb-5 pt-2 relative z-10 min-h-[140px]">
          {/* Hadith */}
          {activeTab === 'hadith' && content.hadith && (
            <div className="space-y-3">
              <p className="text-[10px] text-muted-foreground uppercase tracking-wide font-medium">{t('prophetSaid')}</p>
              {content.hadith.arabic_text && (
                <p className="text-[16px] font-arabic text-foreground leading-[2.4] text-center" dir="rtl">
                  «{content.hadith.arabic_text}»
                </p>
              )}
              {content.hadith.arabic_text && content.hadith.text !== content.hadith.arabic_text && (
                <>
                  <div className="w-12 h-[1px] mx-auto bg-gradient-to-r from-transparent via-border to-transparent" />
                  <p className="text-sm text-muted-foreground leading-relaxed text-center" dir="auto">
                    «{content.hadith.text}»
                  </p>
                </>
              )}
              {!content.hadith.arabic_text && (
                <p className="text-[16px] font-arabic text-foreground leading-[2.4] text-center" dir="auto">
                  «{content.hadith.text}»
                </p>
              )}
              <div className="flex items-center justify-between text-[10px] text-muted-foreground/60 pt-2 border-t border-border/20">
                <span className="flex items-center gap-1">
                  <BookOpen className="h-3 w-3" />
                  {content.hadith.narrator}
                </span>
                <span>{content.hadith.source}</span>
              </div>
            </div>
          )}

          {/* Verse */}
          {activeTab === 'verse' && content.verse && (
            <div className="space-y-3">
              <p className="text-[16px] font-arabic text-foreground leading-[2.4] text-center" dir="rtl">
                {content.verse.text}
              </p>
              {content.verse.translation && locale !== 'ar' && (
                <>
                  <div className="w-12 h-[1px] mx-auto bg-gradient-to-r from-transparent via-border to-transparent" />
                  <p className="text-sm text-muted-foreground leading-relaxed text-center" dir="auto">
                    {content.verse.translation}
                  </p>
                </>
              )}
              <p className="text-[10px] text-center text-muted-foreground/60 pt-2 border-t border-border/20">
                📖 {content.verse.surah} — {t('verse')} {content.verse.ayah}
              </p>
            </div>
          )}

          {/* Dua */}
          {activeTab === 'dua' && content.dua && (
            <div className="space-y-3">
              <p className="text-xs font-bold text-foreground">{t(content.dua.subtitleKey)}</p>
              <p className="text-[16px] font-arabic text-foreground leading-[2.4] text-center" dir="rtl">
                {content.dua.arabic}
              </p>
              {locale !== 'ar' && content.dua.translationKey && (
                <>
                  <div className="w-12 h-[1px] mx-auto bg-gradient-to-r from-transparent via-border to-transparent" />
                  <p className="text-sm text-muted-foreground leading-relaxed text-center" dir="auto">
                    {t(content.dua.translationKey)}
                  </p>
                </>
              )}
              <p className="text-[10px] text-center text-muted-foreground/60 pt-2 border-t border-border/20">
                📚 {t(content.dua.referenceKey)}
              </p>
            </div>
          )}

          {/* Fallback if no content */}
          {activeTab === 'hadith' && !content.hadith && (
            <div className="text-center py-4 text-muted-foreground text-sm">{t('loading')}</div>
          )}
          {activeTab === 'verse' && !content.verse && (
            <div className="text-center py-4 text-muted-foreground text-sm">{t('loading')}</div>
          )}
        </div>
      </div>
    </div>
  );
}
