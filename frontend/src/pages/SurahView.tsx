import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useLocale } from '@/hooks/useLocale';
import { ArrowLeft, ArrowRight, Play, Pause, Bookmark, BookmarkCheck, ChevronDown, ChevronUp } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { toast } from 'sonner';
import {
  fetchChapterInfo,
  fetchVersesByChapter,
  fetchChapterTafsir,
  getTranslationId,
  getComingSoonLabel,
  getTafsirLabel,
  getTranslationLabel,
  type QuranChapter,
  type QuranVerse,
} from '@/lib/quranApi';

/**
 * SurahView — V2026 FINAL
 * Layout per language:
 *   1. Arabic verse (small reference)
 *   2. Translation in user's language (PROMINENT — this IS the surah in their language)
 *   3. Tafsir/Explanation below (from API: en=169, ru=170, ar=16, others=16 Arabic fallback)
 * NO AI translation. ALL data from Quran.com API v4.
 */

export default function SurahView() {
  const { id } = useParams();
  const { t, isRTL, locale } = useLocale();
  const navigate = useNavigate();

  const [chapter, setChapter] = useState<QuranChapter | null>(null);
  const [verses, setVerses] = useState<QuranVerse[]>([]);
  const [tafsirMap, setTafsirMap] = useState<Map<string, string>>(new Map());
  const [loading, setLoading] = useState(true);
  const [playing, setPlaying] = useState<number | null>(null);
  const [audio] = useState(new Audio());
  const [bookmarked, setBookmarked] = useState(false);
  const [expandedTafsir, setExpandedTafsir] = useState<Set<number>>(new Set());

  const chapterNum = parseInt(id || '1');
  const isAr = locale === 'ar';

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setExpandedTafsir(new Set());
      try {
        // 1. Fetch chapter info with localized name
        const chInfo = await fetchChapterInfo(chapterNum, locale);
        setChapter(chInfo);

        // 2. Fetch ALL verses with translation (per_page=300 covers all surahs)
        const { verses: allVerses } = await fetchVersesByChapter(chapterNum, locale, 1, 300);
        setVerses(allVerses);

        // 3. Fetch tafsir for the chapter (in user's language if available, else Arabic)
        const tafsirs = await fetchChapterTafsir(chapterNum, locale);
        setTafsirMap(tafsirs);
      } catch (err) {
        console.error('Error loading surah:', err);
      }
      setLoading(false);
    };

    load();

    const savedBookmarks: number[] = JSON.parse(localStorage.getItem('quran_bookmarks') || '[]');
    setBookmarked(savedBookmarks.includes(chapterNum));

    return () => { audio.pause(); };
  }, [id, locale]);

  const toggleBookmark = () => {
    const saved: number[] = JSON.parse(localStorage.getItem('quran_bookmarks') || '[]');
    if (bookmarked) {
      localStorage.setItem('quran_bookmarks', JSON.stringify(saved.filter(n => n !== chapterNum)));
      setBookmarked(false);
      toast.success(t('surahRemovedFromFav') || 'Removed');
    } else {
      localStorage.setItem('quran_bookmarks', JSON.stringify([...saved, chapterNum]));
      setBookmarked(true);
      toast.success(t('surahAddedToFav') || 'Added');
    }
  };

  const playAyah = (verseNumber: number) => {
    if (playing === verseNumber) {
      audio.pause();
      setPlaying(null);
    } else {
      const verse = verses.find(v => v.verse_number === verseNumber);
      if (verse) {
        audio.src = `https://cdn.islamic.network/quran/audio/128/ar.alafasy/${verse.id}.mp3`;
        audio.play().catch(() => {});
        setPlaying(verseNumber);
        audio.onended = () => setPlaying(null);
      }
    }
  };

  const toggleTafsirExpand = (verseNum: number) => {
    setExpandedTafsir(prev => {
      const next = new Set(prev);
      if (next.has(verseNum)) next.delete(verseNum);
      else next.add(verseNum);
      return next;
    });
  };

  const getTranslationText = (verse: QuranVerse): string | null => {
    if (!verse.translations || verse.translations.length === 0) return null;
    const raw = verse.translations[0].text || '';
    return raw.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim() || null;
  };

  const BackIcon = isRTL ? ArrowRight : ArrowLeft;

  const handleBack = () => {
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) window.history.back();
    else navigate('/quran', { replace: true });
  };

  // Surah display name in user's language
  const surahName = chapter
    ? isAr
      ? chapter.name_arabic
      : `${chapter.name_arabic} — ${chapter.translated_name?.name || chapter.name_simple}`
    : '';

  const translationLabel = getTranslationLabel(locale);
  const tafsirLabel = getTafsirLabel(locale);
  const hasTafsir = tafsirMap.size > 0;

  return (
    <div className="min-h-screen pb-24" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="gradient-islamic relative px-5 pb-8 pt-safe-header-compact">
        <div className="absolute inset-0 islamic-pattern opacity-20" />
        <div className="flex items-center justify-between relative z-10">
          <div className="flex items-center gap-3">
            <button onClick={handleBack}>
              <BackIcon className="h-5 w-5 text-primary-foreground" />
            </button>
            <h1 className="text-lg font-bold text-primary-foreground font-arabic leading-tight">
              {surahName}
            </h1>
          </div>
          <Button variant="ghost" size="icon" onClick={toggleBookmark}
            className="text-primary-foreground hover:bg-primary-foreground/10 rounded-xl">
            {bookmarked ? <BookmarkCheck className="h-5 w-5 fill-current" /> : <Bookmark className="h-5 w-5" />}
          </Button>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Bismillah */}
      {chapterNum !== 1 && chapterNum !== 9 && (
        <div className="text-center py-6">
          <p className="text-2xl font-arabic text-foreground">بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ</p>
        </div>
      )}

      {/* Ayahs */}
      <div className="px-4 space-y-4 pb-8">
        {loading ? (
          <div className="text-center py-20 text-muted-foreground">{t('loading')}</div>
        ) : (
          verses.map((verse) => {
            const translationText = getTranslationText(verse);
            const tafsirText = tafsirMap.get(verse.verse_key);
            const isTafsirExpanded = expandedTafsir.has(verse.verse_number);
            const hasTranslation = translationText && translationText.trim() !== '';

            return (
              <motion.div
                key={verse.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="rounded-2xl border border-border/10 bg-card overflow-hidden shadow-elevated"
              >
                {/* Verse Number + Audio */}
                <div className="flex items-center justify-between px-4 py-2.5 bg-primary/5 border-b border-border/10">
                  <div className="flex items-center gap-2">
                    <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary/15 text-primary text-xs font-bold">
                      {verse.verse_number}
                    </span>
                    <span className="text-[10px] text-muted-foreground">{verse.verse_key}</span>
                  </div>
                  <Button variant="ghost" size="icon" className="h-7 w-7 rounded-lg"
                    onClick={() => playAyah(verse.verse_number)}>
                    {playing === verse.verse_number
                      ? <Pause className="h-3.5 w-3.5 text-primary" />
                      : <Play className="h-3.5 w-3.5 text-muted-foreground" />}
                  </Button>
                </div>

                <div className="p-4 space-y-3">
                  {/* ═══ 1. Arabic Verse (always shown) ═══ */}
                  <div className="text-center pb-3 border-b border-border/10">
                    <p className="text-2xl leading-[2.5] font-arabic text-foreground" dir="rtl">
                      {verse.text_uthmani}
                    </p>
                  </div>

                  {/* ═══ 2. Translation in User's Language (PROMINENT) ═══ */}
                  {hasTranslation && (
                    <div className="pt-1">
                      <p className="text-[10px] font-bold text-primary/70 uppercase tracking-wider mb-1.5">
                        {translationLabel}
                      </p>
                      <p className="text-[15px] text-foreground leading-relaxed font-medium" dir="auto">
                        {translationText}
                      </p>
                    </div>
                  )}

                  {/* Coming Soon for languages without translation */}
                  {!hasTranslation && !isAr && (
                    <p className="text-xs text-muted-foreground italic pt-1">
                      {getComingSoonLabel(locale)}
                    </p>
                  )}

                  {/* ═══ 3. Tafsir/Explanation (expandable) ═══ */}
                  {tafsirText && (
                    <div className="pt-2 border-t border-border/10">
                      <button
                        onClick={() => toggleTafsirExpand(verse.verse_number)}
                        className="flex items-center justify-between w-full text-start group"
                      >
                        <p className="text-[10px] font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider">
                          📖 {tafsirLabel}
                        </p>
                        {isTafsirExpanded
                          ? <ChevronUp className="h-3.5 w-3.5 text-amber-500" />
                          : <ChevronDown className="h-3.5 w-3.5 text-muted-foreground group-hover:text-amber-500" />}
                      </button>
                      {isTafsirExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          className="mt-2 p-3 rounded-xl bg-amber-500/5 border border-amber-500/10"
                        >
                          <p className="text-sm text-foreground/80 leading-[1.9] whitespace-pre-wrap"
                            dir={locale === 'en' || locale === 'ru' ? 'ltr' : isRTL ? 'rtl' : 'ltr'}>
                            {tafsirText}
                          </p>
                        </motion.div>
                      )}
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })
        )}
      </div>
    </div>
  );
}
