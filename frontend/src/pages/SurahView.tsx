import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useLocale } from '@/hooks/useLocale';
import { useAuth } from '@/hooks/useAuth';
import { ArrowLeft, ArrowRight, Play, Pause, Bookmark, BookmarkCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { toast } from 'sonner';
import {
  fetchChapterInfo,
  fetchVersesByChapter,
  getTranslationId,
  getComingSoonLabel,
  type QuranChapter,
  type QuranVerse,
} from '@/lib/quranApi';

/**
 * SurahView — V2026 REBUILD
 * ALL data from Quran.com API v4.
 * Translation per language uses MANDATORY IDs (131, 31, 27, 77, 79, 32, 39, 215, 16).
 * NO alquran.cloud. NO AI translation. NO hardcoded text.
 */

export default function SurahView() {
  const { id } = useParams();
  const { t, isRTL, locale } = useLocale();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [chapter, setChapter] = useState<QuranChapter | null>(null);
  const [verses, setVerses] = useState<QuranVerse[]>([]);
  const [loading, setLoading] = useState(true);
  const [playing, setPlaying] = useState<number | null>(null);
  const [audio] = useState(new Audio());
  const [bookmarked, setBookmarked] = useState(false);

  const chapterNum = parseInt(id || '1');

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        // Fetch chapter info with localized name
        const chInfo = await fetchChapterInfo(chapterNum, locale);
        setChapter(chInfo);

        // Fetch ALL verses in a single call (max surah = 286 ayahs)
        const { verses: allVerses } = await fetchVersesByChapter(
          chapterNum,
          locale,
          1,
          300  // covers all surahs including Al-Baqarah (286)
        );

        setVerses(allVerses);
      } catch (err) {
        console.error('Error loading surah:', err);
      }
      setLoading(false);
    };

    load();

    if (id) {
      const savedBookmarks: number[] = JSON.parse(localStorage.getItem('quran_bookmarks') || '[]');
      setBookmarked(savedBookmarks.includes(chapterNum));
    }

    return () => { audio.pause(); };
  }, [id, locale]);

  const toggleBookmark = async () => {
    const savedBookmarks: number[] = JSON.parse(localStorage.getItem('quran_bookmarks') || '[]');

    if (bookmarked) {
      const updated = savedBookmarks.filter(n => n !== chapterNum);
      localStorage.setItem('quran_bookmarks', JSON.stringify(updated));
      setBookmarked(false);
      toast.success(t('surahRemovedFromFav') || 'Removed from favorites');
    } else {
      const updated = [...savedBookmarks, chapterNum];
      localStorage.setItem('quran_bookmarks', JSON.stringify(updated));
      setBookmarked(true);
      toast.success(t('surahAddedToFav') || 'Added to favorites');
    }
  };

  const playAyah = (verseKey: string, verseNumber: number) => {
    if (playing === verseNumber) {
      audio.pause();
      setPlaying(null);
    } else {
      // Construct audio URL from Quran.com CDN (Alafasy reciter)
      const audioUrl = `https://cdn.islamic.network/quran/audio/128/ar.alafasy/${verses.find(v => v.verse_number === verseNumber)?.id || verseNumber}.mp3`;
      audio.src = audioUrl;
      audio.play().catch(() => {});
      setPlaying(verseNumber);
      audio.onended = () => setPlaying(null);
    }
  };

  const getTranslationText = (verse: QuranVerse): string | null => {
    if (!verse.translations || verse.translations.length === 0) return null;
    const raw = verse.translations[0].text || '';
    // Strip HTML tags from translation text
    return raw.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim();
  };

  const BackIcon = isRTL ? ArrowRight : ArrowLeft;

  const handleBack = () => {
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) {
      window.history.back();
    } else {
      navigate('/quran', { replace: true });
    }
  };

  // Surah display name
  const surahDisplayName = chapter
    ? `${chapter.name_arabic}${locale !== 'ar' ? ` — ${chapter.translated_name?.name || chapter.name_simple}` : ''}`
    : '';

  return (
    <div className="min-h-screen pb-24" dir={isRTL ? 'rtl' : 'ltr'}>
      <div className="gradient-islamic relative px-5 pb-8 pt-safe-header-compact">
        <div className="absolute inset-0 islamic-pattern opacity-20" />
        <div className="flex items-center justify-between relative z-10">
          <div className="flex items-center gap-3">
            <button onClick={handleBack}>
              <BackIcon className="h-5 w-5 text-primary-foreground" />
            </button>
            <h1 className="text-lg font-bold text-primary-foreground font-arabic leading-tight">
              {surahDisplayName}
            </h1>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleBookmark}
            className="text-primary-foreground hover:bg-primary-foreground/10 rounded-xl"
          >
            {bookmarked ? (
              <BookmarkCheck className="h-5 w-5 fill-current" />
            ) : (
              <Bookmark className="h-5 w-5" />
            )}
          </Button>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Bismillah — shown for all surahs except Al-Fatiha (1) and At-Tawba (9) */}
      {chapterNum !== 1 && chapterNum !== 9 && (
        <div className="text-center py-6">
          <p className="text-2xl font-arabic text-foreground">بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ</p>
        </div>
      )}

      {/* Ayahs */}
      <div className="px-5 space-y-4 pb-8">
        {loading ? (
          <div className="text-center py-20 text-muted-foreground">{t('loading')}</div>
        ) : (
          verses.map((verse) => {
            const translationText = getTranslationText(verse);
            const hasTranslation = translationText && translationText !== '';
            const isGreek = locale === 'el';
            const comingSoon = !hasTranslation && locale !== 'ar' && !isGreek && getTranslationId(locale) !== null;
            const comingSoonGreek = isGreek && !hasTranslation;

            return (
              <motion.div
                key={verse.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="rounded-2xl border border-border/10 bg-card p-5 shadow-elevated"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-primary/10 text-primary text-xs font-bold">
                    {verse.verse_number}
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 rounded-xl"
                    onClick={() => playAyah(verse.verse_key, verse.verse_number)}
                  >
                    {playing === verse.verse_number ? (
                      <Pause className="h-4 w-4 text-primary" />
                    ) : (
                      <Play className="h-4 w-4 text-muted-foreground" />
                    )}
                  </Button>
                </div>

                {/* Arabic Verse (always shown) */}
                <p className="text-right text-2xl leading-[2.5] font-arabic text-foreground" dir="rtl">
                  {verse.text_uthmani}
                </p>

                {/* Translation — from Quran.com v4 ONLY */}
                {hasTranslation && (
                  <div className="mt-3 pt-3 border-t border-border/30">
                    <p className="text-xs text-muted-foreground mb-1">
                      {locale === 'ar' ? 'التفسير الميسر' : t('meaningTranslation')}
                    </p>
                    <p className="text-sm text-foreground/80 leading-relaxed" dir="auto">
                      {translationText}
                    </p>
                  </div>
                )}

                {/* Coming Soon label if translation not available */}
                {(comingSoon || comingSoonGreek) && (
                  <div className="mt-3 pt-3 border-t border-border/30">
                    <p className="text-xs text-muted-foreground italic">
                      {getComingSoonLabel(locale)}
                    </p>
                  </div>
                )}
              </motion.div>
            );
          })
        )}
      </div>
    </div>
  );
}
