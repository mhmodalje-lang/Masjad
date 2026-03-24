import { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useLocale } from '@/hooks/useLocale';
import { useAuth } from '@/hooks/useAuth';
import {
  ArrowLeft, ArrowRight, Play, Pause, Bookmark, BookmarkCheck,
  BookOpen, ChevronDown, ChevronUp, Share2, Download, Loader2, Info
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Ayah {
  number: number;
  text: string;
  numberInSurah: number;
  audio: string;
  translation?: string;
}

interface TafsirData {
  text: string;
  tafsir_name: string;
  is_fallback_language: boolean;
  verse_key: string;
}

// V2026: Legacy alquran.cloud edition identifiers (audio fallback only)
const quranTranslationEditions: Record<string, string> = {
  en: 'en.sahih',
  fr: 'fr.hamidullah',
  de: 'de.bubenheim',
  'de-AT': 'de.bubenheim',
  tr: 'tr.diyanet',
  ru: 'ru.abuadel',
  sv: 'sv.bernstrom',
  nl: 'nl.siregar',
  el: 'el.rwwad',
};

// === TAFSIR LOCAL CACHE HELPERS ===
const TAFSIR_CACHE_PREFIX = 'tafsir_v3_';
const TAFSIR_CACHE_TTL = 7 * 24 * 60 * 60 * 1000; // 7 days in ms

function getCachedTafsir(verseKey: string, lang: string): TafsirData | null {
  try {
    const key = `${TAFSIR_CACHE_PREFIX}${lang}_${verseKey}`;
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (Date.now() - parsed.ts > TAFSIR_CACHE_TTL) {
      localStorage.removeItem(key);
      return null;
    }
    return parsed.data;
  } catch { return null; }
}

function setCachedTafsir(verseKey: string, lang: string, data: TafsirData) {
  try {
    const key = `${TAFSIR_CACHE_PREFIX}${lang}_${verseKey}`;
    localStorage.setItem(key, JSON.stringify({ ts: Date.now(), data }));
  } catch { /* Storage full - non-critical */ }
}

// === SHARE AS IMAGE ===
async function shareAyahAsImage(
  ayahText: string,
  tafsirText: string,
  surahName: string,
  verseNum: number,
  tafsirSource: string,
  t: (k: string) => string,
) {
  const canvas = document.createElement('canvas');
  const w = 1080;
  const h = 1920;
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d')!;

  // Background gradient
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#064E3B');
  grad.addColorStop(0.5, '#065F46');
  grad.addColorStop(1, '#064E3B');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // Decorative top & bottom borders
  ctx.fillStyle = 'rgba(212, 175, 55, 0.3)';
  ctx.fillRect(40, 40, w - 80, 4);
  ctx.fillRect(40, h - 44, w - 80, 4);
  ctx.fillRect(40, 40, 4, h - 80);
  ctx.fillRect(w - 44, 40, 4, h - 80);

  // Bismillah
  ctx.fillStyle = 'rgba(212, 175, 55, 0.8)';
  ctx.font = '36px serif';
  ctx.textAlign = 'center';
  ctx.fillText('﷽', w / 2, 120);

  // Surah name & verse number
  ctx.fillStyle = 'rgba(255,255,255,0.7)';
  ctx.font = '28px sans-serif';
  ctx.fillText(`${surahName} - ${t('tafsirVerse') || 'Verse'} ${verseNum}`, w / 2, 180);

  // Divider
  ctx.fillStyle = 'rgba(212, 175, 55, 0.4)';
  ctx.fillRect(w / 2 - 100, 210, 200, 2);

  // Ayah text (Arabic - RTL)
  ctx.fillStyle = '#FFFFFF';
  ctx.font = '44px serif';
  ctx.textAlign = 'center';
  ctx.direction = 'rtl';
  const ayahLines = wrapText(ctx, ayahText, w - 160, 44);
  let y = 290;
  for (const line of ayahLines) {
    ctx.fillText(line, w / 2, y);
    y += 70;
  }

  // Tafsir divider
  y += 30;
  ctx.fillStyle = 'rgba(212, 175, 55, 0.4)';
  ctx.fillRect(80, y, w - 160, 2);
  y += 40;

  // Tafsir label
  ctx.fillStyle = 'rgba(212, 175, 55, 0.9)';
  ctx.font = 'bold 26px sans-serif';
  ctx.textAlign = 'center';
  ctx.direction = 'ltr';
  ctx.fillText(`📖 ${tafsirSource}`, w / 2, y);
  y += 50;

  // Tafsir text
  ctx.fillStyle = 'rgba(255,255,255,0.85)';
  ctx.font = '28px sans-serif';
  ctx.direction = 'rtl';
  const tafsirLines = wrapText(ctx, tafsirText, w - 160, 28);
  const maxTafsirLines = Math.min(tafsirLines.length, 18);
  for (let i = 0; i < maxTafsirLines; i++) {
    ctx.fillText(tafsirLines[i], w / 2, y);
    y += 46;
  }
  if (tafsirLines.length > maxTafsirLines) {
    ctx.fillText('...', w / 2, y);
    y += 46;
  }

  // App branding at bottom
  ctx.fillStyle = 'rgba(212, 175, 55, 0.4)';
  ctx.fillRect(80, h - 140, w - 160, 2);
  ctx.fillStyle = 'rgba(255,255,255,0.9)';
  ctx.font = 'bold 30px sans-serif';
  ctx.textAlign = 'center';
  ctx.direction = 'ltr';
  ctx.fillText('أذان وحكاية | Athan & Hikaya', w / 2, h - 90);
  ctx.fillStyle = 'rgba(212, 175, 55, 0.8)';
  ctx.font = '22px sans-serif';
  ctx.fillText(t('downloadApp') || 'Download the App', w / 2, h - 55);

  // Convert to blob and share
  canvas.toBlob(async (blob) => {
    if (!blob) return;
    const file = new File([blob], `quran-tafsir-${surahName}-${verseNum}.png`, { type: 'image/png' });

    if (navigator.share && navigator.canShare?.({ files: [file] })) {
      try {
        await navigator.share({
          files: [file],
          title: `${surahName} - ${t('tafsirVerse') || 'Verse'} ${verseNum}`,
          text: `${t('downloadApp') || 'Download Athan & Hikaya App'}`,
        });
        return;
      } catch { /* User cancelled or share failed */ }
    }

    // Fallback: Download the image
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `quran-tafsir-${surahName}-${verseNum}.png`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success(t('shareAsImage') || 'Image saved!');
  }, 'image/png');
}

function wrapText(ctx: CanvasRenderingContext2D, text: string, maxWidth: number, fontSize: number): string[] {
  const words = text.split(' ');
  const lines: string[] = [];
  let currentLine = '';

  for (const word of words) {
    const testLine = currentLine ? `${currentLine} ${word}` : word;
    const metrics = ctx.measureText(testLine);
    if (metrics.width > maxWidth && currentLine) {
      lines.push(currentLine);
      currentLine = word;
    } else {
      currentLine = testLine;
    }
  }
  if (currentLine) lines.push(currentLine);
  return lines;
}

// === AYAH CARD WITH TAFSIR ===
function AyahCard({
  ayah,
  surahId,
  surahName,
  locale,
  playing,
  onPlay,
  t,
  showArabic,
}: {
  ayah: Ayah;
  surahId: string;
  surahName: string;
  locale: string;
  playing: number | null;
  onPlay: (ayah: Ayah) => void;
  t: (k: string) => string;
  showArabic: boolean;
}) {
  const [showTafsir, setShowTafsir] = useState(false);
  const [tafsir, setTafsir] = useState<TafsirData | null>(null);
  const [loadingTafsir, setLoadingTafsir] = useState(false);
  const [sharing, setSharing] = useState(false);

  const verseKey = `${surahId}:${ayah.numberInSurah}`;

  const fetchTafsir = useCallback(async () => {
    if (tafsir) {
      setShowTafsir(!showTafsir);
      return;
    }

    // Check localStorage cache first
    const cached = getCachedTafsir(verseKey, locale);
    if (cached) {
      setTafsir(cached);
      setShowTafsir(true);
      return;
    }

    setLoadingTafsir(true);
    setShowTafsir(true);

    try {
      // V2026: Use global-verse endpoint for consistent concise explanations
      const res = await fetch(`${BACKEND_URL}/api/quran/v4/global-verse/${surahId}/${ayah.numberInSurah}?language=${locale}`);
      if (!res.ok) throw new Error('Failed to fetch');
      const data = await res.json();

      if (data.success && (data.tafsir || data.explanation)) {
        const tafsirData: TafsirData = {
          text: data.tafsir || data.explanation || '',
          tafsir_name: data.tafsir_source || data.explanation_source || '',
          is_fallback_language: data.tafsir_is_arabic || false,
          verse_key: verseKey,
        };
        setTafsir(tafsirData);
        setCachedTafsir(verseKey, locale, tafsirData);
      } else {
        setTafsir({ text: '', tafsir_name: '', is_fallback_language: false, verse_key: verseKey });
      }
    } catch {
      toast.error(t('tafsirError') || 'Error loading tafsir');
      setShowTafsir(false);
    } finally {
      setLoadingTafsir(false);
    }
  }, [tafsir, showTafsir, verseKey, locale, t, surahId, ayah.numberInSurah]);

  const handleShare = async () => {
    if (!tafsir?.text) return;
    setSharing(true);
    try {
      await shareAyahAsImage(
        ayah.text,
        tafsir.text,
        surahName,
        ayah.numberInSurah,
        tafsir.tafsir_name || t('tafsirMuyassar'),
        t
      );
    } catch {
      toast.error('Share failed');
    } finally {
      setSharing(false);
    }
  };

  const tafsirSourceLabel = tafsir?.tafsir_name || (locale === 'ar' ? t('tafsirMuyassar') : t('tafsirAbridged'));

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="rounded-2xl border border-border/10 bg-card p-5 shadow-elevated"
    >
      {/* Top bar: verse number + play */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-primary/10 text-primary text-xs font-bold">
          {ayah.numberInSurah}
        </div>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8 rounded-xl"
          onClick={() => onPlay(ayah)}
        >
          {playing === ayah.numberInSurah ? (
            <Pause className="h-4 w-4 text-primary" />
          ) : (
            <Play className="h-4 w-4 text-muted-foreground" />
          )}
        </Button>
      </div>

      {/* Ayah Arabic text — hidden by default for non-Arabic users */}
      {showArabic && (
        <p className="text-right text-2xl leading-[2.5] font-arabic text-foreground" dir="rtl">
          {ayah.text}
        </p>
      )}

      {/* Translation */}
      {ayah.translation && (
        <div className="mt-3 pt-3 border-t border-border/30">
          <p className="text-xs text-muted-foreground mb-1">{t('meaningTranslation')}</p>
          <p className="text-sm text-foreground/80 leading-relaxed" dir="auto">
            {ayah.translation}
          </p>
        </div>
      )}

      {/* Show Explanation (Tafsir) Button */}
      <div className="mt-4 pt-3 border-t border-border/20">
        <button
          onClick={fetchTafsir}
          data-testid="show-explanation-button"
          className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl
            bg-gradient-to-r from-emerald-500/10 to-teal-500/10
            hover:from-emerald-500/20 hover:to-teal-500/20
            border border-emerald-500/20 hover:border-emerald-500/30
            transition-all duration-300 active:scale-[0.98] group"
        >
          <BookOpen className="h-4 w-4 text-emerald-600 dark:text-emerald-400 group-hover:scale-110 transition-transform" />
          <span className="text-sm font-bold text-emerald-700 dark:text-emerald-300">
            {showTafsir ? t('hideExplanation') : t('showExplanation')}
          </span>
          {loadingTafsir ? (
            <Loader2 className="h-3.5 w-3.5 animate-spin text-emerald-500" />
          ) : showTafsir ? (
            <ChevronUp className="h-3.5 w-3.5 text-emerald-500" />
          ) : (
            <ChevronDown className="h-3.5 w-3.5 text-emerald-500" />
          )}
        </button>

        {/* Tafsir Content */}
        <AnimatePresence>
          {showTafsir && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3, ease: 'easeInOut' }}
              className="overflow-hidden"
            >
              <div className="mt-3 p-4 rounded-xl bg-gradient-to-br from-emerald-500/5 to-teal-500/5 border border-emerald-500/15">
                {loadingTafsir ? (
                  <div className="flex items-center justify-center gap-2 py-6">
                    <Loader2 className="h-5 w-5 animate-spin text-emerald-500" />
                    <span className="text-sm text-muted-foreground">{t('loadingTafsir')}</span>
                  </div>
                ) : tafsir?.text ? (
                  <>
                    {/* Tafsir source badge */}
                    <div className="flex items-center gap-2 mb-3">
                      <BookOpen className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
                      <span className="text-xs font-bold text-emerald-700 dark:text-emerald-300">
                        {tafsirSourceLabel}
                      </span>
                    </div>

                    {/* Arabic tafsir notice for non-Arabic users */}
                    {tafsir.is_fallback_language && (
                      <div className="mb-3 p-2 rounded-lg bg-amber-500/10 border border-amber-500/20">
                        <p className="text-xs text-amber-700 dark:text-amber-300 text-center">
                          📖 {t('arabicTafsirNote') || 'This is the Arabic scholarly explanation (التفسير الميسر) — no native tafsir available for this language'}
                        </p>
                      </div>
                    )}

                    {/* Tafsir text */}
                    <p className={`text-sm text-foreground/85 leading-[2] whitespace-pre-wrap ${tafsir.is_fallback_language ? 'font-arabic text-right' : ''}`} dir={tafsir.is_fallback_language ? 'rtl' : 'auto'}>
                      {tafsir.text}
                    </p>

                    {/* Share as Image button */}
                    <div className="mt-4 pt-3 border-t border-emerald-500/10 flex gap-2">
                      <button
                        onClick={handleShare}
                        disabled={sharing}
                        className="flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg
                          bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold
                          transition-all duration-200 active:scale-[0.97] disabled:opacity-50"
                      >
                        {sharing ? (
                          <Loader2 className="h-3.5 w-3.5 animate-spin" />
                        ) : (
                          <Share2 className="h-3.5 w-3.5" />
                        )}
                        {t('shareAsImage')}
                      </button>
                    </div>
                  </>
                ) : (
                  <p className="text-sm text-muted-foreground text-center py-4">
                    {t('tafsirNotAvailable')}
                  </p>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}

// === MAIN SURAH VIEW ===
export default function SurahView() {
  const { id } = useParams();
  const { t, isRTL, locale } = useLocale();
  const { user } = useAuth();
  const [ayahs, setAyahs] = useState<Ayah[]>([]);
  const [surahName, setSurahName] = useState('');
  const [loading, setLoading] = useState(true);
  const [playing, setPlaying] = useState<number | null>(null);
  const [audio] = useState(new Audio());
  const [bookmarked, setBookmarked] = useState(false);
  
  // V2026: Arabic text visibility — OFF by default for foreign languages
  const isArabicLocale = locale === 'ar';
  const [showArabic, setShowArabic] = useState(isArabicLocale);

  useEffect(() => {
    const fetchAyahs = async () => {
      try {
        const baseLocale = locale.split('-')[0];
        const apiLang = baseLocale || 'ar';

        // Fetch chapter info (for localized name)
        const chapterRes = await fetch(`${BACKEND_URL}/api/quran/v4/chapters/${id}?language=${apiLang}`);
        const chapterData = await chapterRes.json();
        const chapterInfo = chapterData.chapter || {};
        const translatedName = chapterInfo.translated_name?.name || chapterInfo.name_simple || '';
        const arabicName = chapterInfo.name_arabic || '';
        // Show translated name for non-Arabic, Arabic name for Arabic
        if (apiLang === 'ar') {
          setSurahName(arabicName);
        } else {
          setSurahName(translatedName || arabicName);
        }

        // Fetch verses with translations from Quran.com v4 via our backend
        // Use per_page=300 to get all verses at once (longest surah is 286 ayahs)
        const versesRes = await fetch(
          `${BACKEND_URL}/api/quran/v4/verses/by_chapter/${id}?language=${apiLang}&per_page=300`
        );
        const versesData = await versesRes.json();
        const verses = versesData.verses || [];

        // Build audio URL helper: uses EveryAyah CDN with Alafasy recitation
        const padNum = (n: number, len: number = 3) => String(n).padStart(len, '0');

        const ayahsList: Ayah[] = verses.map((v: any) => {
          const surahNum = parseInt(id || '1');
          const verseNum = v.verse_number || v.id;
          const audioUrl = `https://everyayah.com/data/Alafasy_128kbps/${padNum(surahNum)}${padNum(verseNum)}.mp3`;

          // Extract translation text (remove HTML tags like <sup> and footnotes)
          let translationText = '';
          if (v.translations && v.translations.length > 0) {
            translationText = v.translations[0].text || '';
            // Remove <sup> footnote tags and their content first
            translationText = translationText.replace(/<sup[^>]*>[\s\S]*?<\/sup>/gi, '');
            // Clean remaining HTML tags from translation
            translationText = translationText.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim();
          }

          return {
            number: v.id || verseNum,
            text: v.text_uthmani || v.text || '',
            numberInSurah: v.verse_number || verseNum,
            audio: audioUrl,
            translation: (locale !== 'ar' && translationText) ? translationText : undefined,
          };
        });

        setAyahs(ayahsList);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching ayahs:', err);
        // Fallback to legacy API if backend fails
        try {
          const arabicRes = await fetch(`https://api.alquran.cloud/v1/surah/${id}/ar.alafasy`);
          const arabicData = await arabicRes.json();
          let ayahsList: Ayah[] = arabicData.data.ayahs;
          setSurahName(arabicData.data.name);
          setAyahs(ayahsList);
        } catch {
          // Both failed
        }
        setLoading(false);
      }
    };
    fetchAyahs();

    if (id) {
      const savedBookmarks: number[] = JSON.parse(localStorage.getItem('quran_bookmarks') || '[]');
      setBookmarked(savedBookmarks.includes(parseInt(id)));
    }

    return () => { audio.pause(); };
  }, [id, user, locale]);

  const toggleBookmark = async () => {
    const surahNum = parseInt(id!);
    const savedBookmarks: number[] = JSON.parse(localStorage.getItem('quran_bookmarks') || '[]');

    if (bookmarked) {
      const updated = savedBookmarks.filter(n => n !== surahNum);
      localStorage.setItem('quran_bookmarks', JSON.stringify(updated));
      setBookmarked(false);
      toast.success(t('surahRemovedFromFav') || 'Surah removed from favorites');
    } else {
      const updated = [...savedBookmarks, surahNum];
      localStorage.setItem('quran_bookmarks', JSON.stringify(updated));
      setBookmarked(true);
      toast.success(t('surahAddedToFav') || 'Surah added to favorites ❤️');
    }
  };

  const playAyah = (ayah: Ayah) => {
    if (playing === ayah.numberInSurah) {
      audio.pause();
      setPlaying(null);
    } else {
      audio.src = ayah.audio;
      audio.play();
      setPlaying(ayah.numberInSurah);
      audio.onended = () => setPlaying(null);
    }
  };

  const BackIcon = isRTL ? ArrowRight : ArrowLeft;
  const navigate = useNavigate();

  const handleBack = () => {
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) {
      window.history.back();
    } else {
      navigate('/quran', { replace: true });
    }
  };

  return (
    <div className="min-h-screen pb-24" dir="rtl">
      <div className="gradient-islamic relative px-5 pb-8 pt-safe-header-compact">
        <div className="absolute inset-0 islamic-pattern opacity-20" />
        <div className="flex items-center justify-between relative z-10">
          <div className="flex items-center gap-3">
            <button onClick={handleBack}>
              <BackIcon className="h-5 w-5 text-primary-foreground" />
            </button>
            <h1 className="text-xl font-bold text-primary-foreground font-arabic">{surahName}</h1>
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

      {/* Show Arabic Toggle — for non-Arabic users */}
      {!isArabicLocale && (
        <div className="px-5 pt-2 pb-1 flex justify-center">
          <button
            onClick={() => setShowArabic(!showArabic)}
            data-testid="arabic-toggle-button"
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs font-bold transition-all duration-300 ${
              showArabic 
                ? 'bg-primary/20 text-primary border border-primary/30' 
                : 'bg-muted/50 text-muted-foreground border border-border/30 hover:bg-muted'
            }`}
          >
            <span className="font-arabic text-sm">ع</span>
            <span>{showArabic ? (t('hideArabic') || 'Hide Arabic') : (t('showArabic') || 'Show Original Arabic')}</span>
          </button>
        </div>
      )}

      {/* Bismillah — show only when Arabic text is visible */}
      {showArabic && id !== '1' && id !== '9' && (
        <div className="text-center py-6">
          <p className="text-2xl font-arabic text-foreground">بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ</p>
        </div>
      )}

      {/* Ayahs */}
      <div className="px-5 space-y-4 pb-8">
        {loading ? (
          <div className="text-center py-20 text-muted-foreground">{t('loading')}</div>
        ) : (
          ayahs.map((ayah) => (
            <AyahCard
              key={ayah.number}
              ayah={ayah}
              surahId={id!}
              surahName={surahName}
              locale={locale}
              playing={playing}
              onPlay={playAyah}
              t={t}
              showArabic={showArabic}
            />
          ))
        )}
      </div>
    </div>
  );
}
