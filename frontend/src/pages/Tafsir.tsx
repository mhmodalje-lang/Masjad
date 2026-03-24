import React, { useState, useEffect, useCallback } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { ChevronLeft, ChevronRight, BookOpen, Search, Star, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import {
  fetchChapters,
  fetchVerseUthmani,
  fetchTafsir,
  fetchVerseTranslation,
  getComingSoonLabel,
  QURAN_TAFSIR_IDS,
  QURAN_TRANSLATION_IDS,
  type QuranChapter,
} from '@/lib/quranApi';

/**
 * Tafsir Page — V2026 REBUILD
 * ALL data from Quran.com API v4.
 * Translation uses MANDATORY IDs per language.
 * Tafsir uses Ibn Kathir (169) or Al-Muyassar (16).
 * NO AI translation. NO hardcoded text.
 */

export default function Tafsir() {
  const { locale, dir, t } = useLocale();
  const isAr = locale === 'ar';

  const [chapters, setChapters] = useState<QuranChapter[]>([]);
  const [surahNum, setSurahNum] = useState(1);
  const [ayahNum, setAyahNum] = useState(1);
  const [loading, setLoading] = useState(false);
  const [chaptersLoading, setChaptersLoading] = useState(true);
  const [ayahText, setAyahText] = useState('');
  const [tafsirText, setTafsirText] = useState('');
  const [translationText, setTranslationText] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [showSurahList, setShowSurahList] = useState(true);
  const [favorites, setFavorites] = useState<string[]>(() => {
    try { return JSON.parse(localStorage.getItem('tafsir_favs') || '[]'); } catch { return []; }
  });

  // Load chapters from Quran.com v4 with localized names
  useEffect(() => {
    setChaptersLoading(true);
    fetchChapters(locale).then(data => {
      setChapters(data);
      setChaptersLoading(false);
    }).catch(() => setChaptersLoading(false));
  }, [locale]);

  const currentChapter = chapters.find(c => c.id === surahNum);
  const versesCount = currentChapter?.verses_count || 7;

  const loadTafsir = useCallback(async (sNum: number, aNum: number) => {
    setLoading(true);
    setShowSurahList(false);
    const verseKey = `${sNum}:${aNum}`;

    try {
      // 1. Fetch Arabic text (Uthmani)
      const arabicText = await fetchVerseUthmani(verseKey);
      setAyahText(arabicText || '');

      // 2. Fetch Tafsir (Ibn Kathir Arabic)
      const tafsir = await fetchTafsir(verseKey, QURAN_TAFSIR_IDS.ibn_kathir_ar);
      setTafsirText(tafsir || '');

      // 3. Fetch translation for current language
      if (!isAr) {
        const transId = QURAN_TRANSLATION_IDS[locale];
        if (transId) {
          const trans = await fetchVerseTranslation(verseKey, locale);
          if (trans) {
            setTranslationText(trans);
          } else {
            setTranslationText(getComingSoonLabel(locale));
          }
        } else {
          setTranslationText(getComingSoonLabel(locale));
        }
      } else {
        // For Arabic, show Al-Muyassar explanation
        const muyassarText = await fetchTafsir(verseKey, QURAN_TAFSIR_IDS.muyassar);
        setTranslationText(muyassarText || '');
      }
    } catch (e) {
      console.error('Tafsir fetch error:', e);
      setTafsirText(t('tafsirError'));
    }
    setLoading(false);
  }, [isAr, locale, t]);

  useEffect(() => {
    if (!showSurahList && chapters.length > 0) {
      loadTafsir(surahNum, ayahNum);
    }
  }, [surahNum, ayahNum, showSurahList, loadTafsir, chapters.length]);

  const prevAyah = () => {
    if (ayahNum > 1) setAyahNum(ayahNum - 1);
    else if (surahNum > 1) {
      const prevCh = chapters.find(c => c.id === surahNum - 1);
      if (prevCh) { setSurahNum(surahNum - 1); setAyahNum(prevCh.verses_count); }
    }
  };

  const nextAyah = () => {
    if (ayahNum < versesCount) setAyahNum(ayahNum + 1);
    else if (surahNum < 114) { setSurahNum(surahNum + 1); setAyahNum(1); }
  };

  const toggleFav = () => {
    const key = `${surahNum}:${ayahNum}`;
    const newFavs = favorites.includes(key) ? favorites.filter(f => f !== key) : [...favorites, key];
    setFavorites(newFavs);
    localStorage.setItem('tafsir_favs', JSON.stringify(newFavs));
  };

  const filteredChapters = searchQuery
    ? chapters.filter(c =>
        c.name_arabic.includes(searchQuery) ||
        c.name_simple.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (c.translated_name?.name || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
        String(c.id).includes(searchQuery)
      )
    : chapters;

  // Display name for surah header
  const surahDisplayName = currentChapter
    ? isAr
      ? currentChapter.name_arabic
      : `${currentChapter.name_arabic} (${currentChapter.translated_name?.name || currentChapter.name_simple})`
    : '';

  return (
    <div dir={dir} className="min-h-screen bg-background pb-24">
      {/* Header */}
      <div className="sticky top-0 z-30 bg-background/95 backdrop-blur-md border-b border-border/30 px-4 py-3.5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-emerald-500" />
            <h1 className="text-lg font-bold text-foreground">{t('tafsirTitle')}</h1>
          </div>
          {!showSurahList && (
            <button onClick={() => setShowSurahList(true)}
              className="text-xs px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold">
              {t('tafsirSurahs')}
            </button>
          )}
        </div>
      </div>

      {/* Surah List */}
      {showSurahList && (
        <div className="px-4 py-3 space-y-3">
          <div className="relative">
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input type="text" value={searchQuery} onChange={e => setSearchQuery(e.target.value)}
              placeholder={t('tafsirSearchSurah')}
              className="w-full py-3 pr-10 pl-4 rounded-2xl bg-card border border-border/30 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-emerald-500/30" />
          </div>
          <div className="p-4 rounded-2xl bg-gradient-to-br from-emerald-500/10 to-teal-500/5 border border-emerald-500/20">
            <p className="text-sm text-foreground/80 leading-relaxed">{t('tafsirDescription')}</p>
          </div>

          {chaptersLoading ? (
            <div className="flex justify-center py-10">
              <Loader2 className="h-6 w-6 animate-spin text-emerald-500" />
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-2">
              {filteredChapters.map(ch => (
                <button key={ch.id} onClick={() => { setSurahNum(ch.id); setAyahNum(1); setShowSurahList(false); }}
                  className="p-3 rounded-xl bg-card border border-border/20 hover:border-emerald-500/30 transition-all text-right flex items-center gap-2.5 active:scale-[0.98]">
                  <span className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-xs font-bold shrink-0">{ch.id}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-foreground truncate">{ch.name_arabic}</p>
                    <p className="text-[10px] text-muted-foreground truncate">
                      {isAr ? ch.name_simple : ch.translated_name?.name || ch.name_simple} • {ch.verses_count} {t('tafsirVerses')}
                    </p>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Tafsir Reading */}
      {!showSurahList && (
        <div className="px-4 py-3 space-y-4">
          <div className="flex items-center justify-between gap-2">
            <button onClick={prevAyah} className="p-2.5 rounded-xl bg-card border border-border/20 hover:bg-muted/50 transition-all active:scale-95">
              <ChevronRight className="h-5 w-5 text-foreground" />
            </button>
            <div className="text-center flex-1">
              <p className="text-base font-bold text-foreground">{surahDisplayName}</p>
              <p className="text-xs text-muted-foreground">{t('tafsirVerse')} {ayahNum} / {versesCount}</p>
            </div>
            <button onClick={nextAyah} className="p-2.5 rounded-xl bg-card border border-border/20 hover:bg-muted/50 transition-all active:scale-95">
              <ChevronLeft className="h-5 w-5 text-foreground" />
            </button>
          </div>

          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
            {Array.from({ length: Math.min(versesCount, 30) }, (_, i) => i + 1).map(num => (
              <button key={num} onClick={() => setAyahNum(num)}
                className={cn("w-9 h-9 rounded-lg text-xs font-bold shrink-0 transition-all",
                  num === ayahNum ? "bg-emerald-600 text-white shadow-lg" : "bg-card border border-border/20 text-foreground hover:bg-muted/50"
                )}>{num}</button>
            ))}
            {versesCount > 30 && (
              <select value={ayahNum > 30 ? ayahNum : ''} onChange={e => setAyahNum(Number(e.target.value))}
                className="h-9 px-2 rounded-lg text-xs bg-card border border-border/20 text-foreground">
                <option value="" disabled>{t('tafsirMore')}</option>
                {Array.from({ length: versesCount - 30 }, (_, i) => i + 31).map(n => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
            )}
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-16 gap-3">
              <Loader2 className="h-8 w-8 animate-spin text-emerald-500" />
              <p className="text-sm text-muted-foreground">{t('tafsirLoading')}</p>
            </div>
          ) : (
            <>
              {/* Arabic Verse */}
              <div className="p-5 rounded-2xl bg-gradient-to-br from-emerald-500/10 to-teal-500/5 border border-emerald-500/20 text-center">
                <p className="text-2xl leading-[2.2] font-arabic text-foreground" dir="rtl">{ayahText || '...'}</p>
                <div className="flex items-center justify-center gap-3 mt-3">
                  <span className="text-xs text-muted-foreground">{currentChapter?.name_arabic} - {t('tafsirVerse')} {ayahNum}</span>
                  <button onClick={toggleFav} className={cn("p-1.5 rounded-full transition-all",
                    favorites.includes(`${surahNum}:${ayahNum}`) ? "text-amber-500" : "text-muted-foreground/40")}>
                    <Star className="h-4 w-4" fill={favorites.includes(`${surahNum}:${ayahNum}`) ? 'currentColor' : 'none'} />
                  </button>
                </div>
              </div>

              {/* Translation — from Quran.com API v4 with correct ID */}
              {translationText && (
                <div className="p-4 rounded-2xl bg-card border border-border/20">
                  <p className="text-xs font-bold text-muted-foreground mb-2 uppercase">
                    {isAr ? 'التفسير الميسر' : t('meaningTranslation') || 'Translation'}
                  </p>
                  <p className="text-sm text-foreground/80 leading-relaxed" dir={isAr ? 'rtl' : 'auto'}>
                    {translationText}
                  </p>
                </div>
              )}

              {/* Ibn Kathir Tafsir */}
              <div className="p-5 rounded-2xl bg-card border border-border/20">
                <div className="flex items-center gap-2 mb-3">
                  <BookOpen className="h-4 w-4 text-amber-500" />
                  <p className="text-sm font-bold text-foreground">{t('tafsirIbnKathir')}</p>
                </div>
                <p className="text-sm text-foreground/80 leading-[2] whitespace-pre-wrap" dir="rtl">
                  {tafsirText || t('tafsirSelectVerse')}
                </p>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
