import { useState, useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { Search, BookOpen, Bookmark, BookmarkCheck, X, MapPin, ChevronRight, ChevronLeft, Book } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { normalizeArabicForSearch } from '@/lib/arabicNormalize';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Surah {
  id: number;
  name_arabic: string;
  name_simple: string;
  translated_name: { name: string; language_name: string };
  verses_count: number;
  revelation_place: string;
  number: number;
  name: string;
  englishName: string;
  englishNameTranslation: string;
  numberOfAyahs: number;
}

const JUZ_DATA = [
  { number: 1, name: 'الم', startSurah: 1, endSurah: 2 },
  { number: 2, name: 'سيقول', startSurah: 2, endSurah: 2 },
  { number: 3, name: 'تلك الرسل', startSurah: 2, endSurah: 3 },
  { number: 4, name: 'لن تنالوا', startSurah: 3, endSurah: 4 },
  { number: 5, name: 'والمحصنات', startSurah: 4, endSurah: 4 },
  { number: 6, name: 'لا يحب الله', startSurah: 4, endSurah: 5 },
  { number: 7, name: 'وإذا سمعوا', startSurah: 5, endSurah: 6 },
  { number: 8, name: 'ولو أننا', startSurah: 6, endSurah: 7 },
  { number: 9, name: 'قال الملأ', startSurah: 7, endSurah: 8 },
  { number: 10, name: 'واعلموا', startSurah: 8, endSurah: 9 },
  { number: 11, name: 'يعتذرون', startSurah: 9, endSurah: 11 },
  { number: 12, name: 'وما من دابة', startSurah: 11, endSurah: 12 },
  { number: 13, name: 'وما أبرئ', startSurah: 12, endSurah: 14 },
  { number: 14, name: 'ربما', startSurah: 15, endSurah: 16 },
  { number: 15, name: 'سبحان', startSurah: 17, endSurah: 18 },
  { number: 16, name: 'قال ألم', startSurah: 18, endSurah: 20 },
  { number: 17, name: 'اقترب', startSurah: 21, endSurah: 22 },
  { number: 18, name: 'قد أفلح', startSurah: 23, endSurah: 25 },
  { number: 19, name: 'وقال الذين', startSurah: 25, endSurah: 27 },
  { number: 20, name: 'أمن خلق', startSurah: 27, endSurah: 29 },
  { number: 21, name: 'اتل ما أوحي', startSurah: 29, endSurah: 33 },
  { number: 22, name: 'ومن يقنت', startSurah: 33, endSurah: 36 },
  { number: 23, name: 'وما لي', startSurah: 36, endSurah: 39 },
  { number: 24, name: 'فمن أظلم', startSurah: 39, endSurah: 41 },
  { number: 25, name: 'إليه يرد', startSurah: 41, endSurah: 45 },
  { number: 26, name: 'حم', startSurah: 46, endSurah: 51 },
  { number: 27, name: 'قال فما خطبكم', startSurah: 51, endSurah: 57 },
  { number: 28, name: 'قد سمع', startSurah: 58, endSurah: 66 },
  { number: 29, name: 'تبارك', startSurah: 67, endSurah: 77 },
  { number: 30, name: 'عم', startSurah: 78, endSurah: 114 },
];

const REVELATION_LABELS: Record<string, Record<string, string>> = {
  makkah: { ar: 'مكية', en: 'Meccan', fr: 'Mecquoise', de: 'Mekkanisch', tr: 'Mekki', ru: 'Мекканская', sv: 'Meckansk', nl: 'Mekkaans', el: 'Μεκκανική' },
  madinah: { ar: 'مدنية', en: 'Medinan', fr: 'Médinoise', de: 'Medinensisch', tr: 'Medeni', ru: 'Мединская', sv: 'Medinsk', nl: 'Medinaans', el: 'Μεδινική' },
};

function toArabicNumeral(n: number): string {
  return n.toString().replace(/\d/g, d => '٠١٢٣٤٥٦٧٨٩'[parseInt(d)]);
}

export default function Quran() {
  const { t, locale, isRTL } = useLocale();
  const navigate = useNavigate();
  const [surahs, setSurahs] = useState<Surah[]>([]);
  const [search, setSearch] = useState('');
  const [showSearch, setShowSearch] = useState(false);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<'surah' | 'juz' | 'bookmarks'>('surah');
  const [bookmarks, setBookmarks] = useState<number[]>([]);

  const lang = locale?.split('-')[0] || 'ar';

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/quran/v4/chapters?language=${lang}`)
      .then(r => r.json())
      .then(d => {
        const chapters = (d.chapters || []).map((ch: any) => ({
          ...ch,
          number: ch.id,
          name: ch.name_arabic,
          englishName: ch.name_simple,
          englishNameTranslation: ch.translated_name?.name || ch.name_simple,
          numberOfAyahs: ch.verses_count,
        }));
        setSurahs(chapters);
        setLoading(false);
      })
      .catch(() => {
        fetch('https://api.alquran.cloud/v1/surah')
          .then(r => r.json())
          .then(d => { setSurahs(d.data); setLoading(false); })
          .catch(() => setLoading(false));
      });
  }, [lang]);

  useEffect(() => {
    setBookmarks(JSON.parse(localStorage.getItem('quran_bookmarks') || '[]'));
  }, []);

  const toggleBookmark = (e: React.MouseEvent, num: number) => {
    e.preventDefault();
    e.stopPropagation();
    const updated = bookmarks.includes(num) ? bookmarks.filter(n => n !== num) : [...bookmarks, num];
    setBookmarks(updated);
    localStorage.setItem('quran_bookmarks', JSON.stringify(updated));
    toast.success(bookmarks.includes(num) ? t('removedFromBookmarks') : t('addedToBookmarks'));
  };

  const normalizedQuery = normalizeArabicForSearch(search);
  const filtered = surahs.filter(s => {
    if (!search.trim()) return true;
    if (String(s.number) === search.trim()) return true;
    return (
      normalizeArabicForSearch(s.name).includes(normalizedQuery) ||
      normalizeArabicForSearch(s.englishName).includes(normalizedQuery) ||
      normalizeArabicForSearch(s.englishNameTranslation).includes(normalizedQuery)
    );
  });

  const bookmarkedSurahs = surahs.filter(s => bookmarks.includes(s.number));

  const getRevLabel = (place: string) => {
    const key = place?.toLowerCase() === 'madinah' ? 'madinah' : 'makkah';
    return REVELATION_LABELS[key]?.[lang] || REVELATION_LABELS[key]?.['en'] || place;
  };

  const NavIcon = isRTL ? ChevronLeft : ChevronRight;

  const renderSurahCard = (s: Surah) => (
    <motion.div
      key={s.number}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
    >
      <Link
        to={`/quran/${s.number}`}
        className="flex items-center gap-4 p-4 rounded-2xl bg-card border border-border/30 hover:border-primary/30 hover:bg-primary/5 transition-all duration-300 active:scale-[0.98] group"
      >
        {/* Surah Number */}
        <div className="relative flex-shrink-0">
          <div className="w-12 h-12 flex items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500/15 to-teal-500/15 border border-emerald-500/20 text-emerald-700 dark:text-emerald-300 font-bold text-sm">
            {toArabicNumeral(s.number)}
          </div>
        </div>

        {/* Surah Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-bold text-foreground text-base truncate">
              {lang === 'ar' ? s.name : s.englishNameTranslation}
            </h3>
          </div>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-xs text-muted-foreground font-arabic">
              {s.name}
            </span>
            {lang !== 'ar' && s.englishName && (
              <>
                <span className="text-muted-foreground/30">·</span>
                <span className="text-xs text-muted-foreground">{s.englishName}</span>
              </>
            )}
          </div>
          <div className="flex items-center gap-2 mt-1.5">
            <span className={cn(
              "text-[10px] px-2 py-0.5 rounded-full font-medium",
              s.revelation_place?.toLowerCase() === 'makkah'
                ? "bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20"
                : "bg-blue-500/10 text-blue-700 dark:text-blue-300 border border-blue-500/20"
            )}>
              <MapPin className="inline h-2.5 w-2.5 -mt-0.5 mr-0.5" />
              {getRevLabel(s.revelation_place)}
            </span>
            <span className="text-[10px] text-muted-foreground">
              {s.numberOfAyahs || s.verses_count} {t('ayahs')}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-1">
          <button
            onClick={(e) => toggleBookmark(e, s.number)}
            className="p-2 rounded-xl hover:bg-muted/50 transition-colors"
          >
            {bookmarks.includes(s.number) ? (
              <BookmarkCheck className="h-4 w-4 text-primary fill-primary" />
            ) : (
              <Bookmark className="h-4 w-4 text-muted-foreground" />
            )}
          </button>
          <NavIcon className="h-4 w-4 text-muted-foreground/40 group-hover:text-primary transition-colors" />
        </div>
      </Link>
    </motion.div>
  );

  return (
    <div className="min-h-screen pb-24" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="gradient-islamic relative px-5 pb-10 pt-safe-header-compact">
        <div className="absolute inset-0 islamic-pattern opacity-15" />
        <div className="relative z-10 text-center">
          <p className="text-3xl font-arabic text-primary-foreground/80 mb-1">﷽</p>
          <h1 className="text-2xl font-bold text-primary-foreground mb-1">{t('quran')}</h1>
          <p className="text-sm text-primary-foreground/70">{t('quranSubtitle')}</p>
          <p className="text-xs text-primary-foreground/50 mt-1">114 {t('surah')} · 6236 {t('ayahs')}</p>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Search + Tabs */}
      <div className="px-5 -mt-2 relative z-10">
        {/* Search */}
        <div className="mb-4">
          <div className="relative">
            <Search className={cn("absolute top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground", isRTL ? "right-4" : "left-4")} />
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={t('searchSurah')}
              className={cn("rounded-2xl bg-card border-border/30 h-12 text-sm", isRTL ? "pr-11 pl-4" : "pl-11 pr-4")}
              dir="auto"
            />
            {search && (
              <button onClick={() => setSearch('')} className={cn("absolute top-1/2 -translate-y-1/2", isRTL ? "left-4" : "right-4")}>
                <X className="h-4 w-4 text-muted-foreground" />
              </button>
            )}
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 p-1 bg-muted/50 rounded-2xl mb-5">
          {(['surah', 'juz', 'bookmarks'] as const).map(t_key => (
            <button
              key={t_key}
              onClick={() => setTab(t_key)}
              className={cn(
                "flex-1 py-2.5 px-3 rounded-xl text-xs font-bold transition-all duration-200",
                tab === t_key
                  ? "bg-card text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              {t_key === 'surah' && <Book className="inline h-3.5 w-3.5 mr-1 -mt-0.5" />}
              {t_key === 'juz' && <BookOpen className="inline h-3.5 w-3.5 mr-1 -mt-0.5" />}
              {t_key === 'bookmarks' && <Bookmark className="inline h-3.5 w-3.5 mr-1 -mt-0.5" />}
              {t_key === 'surah' ? t('surah') : t_key === 'juz' ? t('juz') : t('bookmarks')}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="px-5">
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            <p className="mt-3 text-sm text-muted-foreground">{t('loading')}</p>
          </div>
        ) : tab === 'surah' ? (
          <div className="space-y-2">
            {filtered.length === 0 ? (
              <div className="text-center py-16">
                <Search className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
                <p className="text-sm text-muted-foreground">{t('noResults')}</p>
              </div>
            ) : (
              filtered.map(renderSurahCard)
            )}
          </div>
        ) : tab === 'juz' ? (
          <div className="space-y-2">
            {JUZ_DATA.map(juz => (
              <motion.div
                key={juz.number}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="p-4 rounded-2xl bg-card border border-border/30"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 flex items-center justify-center rounded-xl bg-primary/10 text-primary font-bold text-sm">
                      {toArabicNumeral(juz.number)}
                    </div>
                    <div>
                      <h3 className="font-bold text-foreground text-sm">{t('juz')} {juz.number}</h3>
                      <p className="text-xs text-muted-foreground font-arabic mt-0.5">{juz.name}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="text-[10px] text-muted-foreground">
                      {t('surah')} {juz.startSurah}{juz.startSurah !== juz.endSurah ? ` - ${juz.endSurah}` : ''}
                    </span>
                    <button
                      onClick={() => navigate(`/quran/${juz.startSurah}`)}
                      className="p-2 rounded-xl hover:bg-primary/10 transition-colors"
                    >
                      <NavIcon className="h-4 w-4 text-muted-foreground" />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          /* Bookmarks */
          <div className="space-y-2">
            {bookmarkedSurahs.length === 0 ? (
              <div className="text-center py-16">
                <Bookmark className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
                <p className="text-sm text-muted-foreground">{t('noBookmarks') || t('bookmarks')}</p>
              </div>
            ) : (
              bookmarkedSurahs.map(renderSurahCard)
            )}
          </div>
        )}
      </div>
    </div>
  );
}
