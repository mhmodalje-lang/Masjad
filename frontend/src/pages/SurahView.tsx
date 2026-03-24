import { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useLocale } from '@/hooks/useLocale';
import {
  ArrowLeft, ArrowRight, Play, Pause, Bookmark, BookmarkCheck,
  BookOpen, ChevronDown, ChevronUp, Share2, Loader2, MapPin
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

interface SurahInfo {
  id: number;
  name_arabic: string;
  name_simple: string;
  translated_name: string;
  verses_count: number;
  revelation_place: string;
}

// ── Tafsir Cache ──
const TAFSIR_CACHE_PREFIX = 'tafsir_v3_';
const TAFSIR_CACHE_TTL = 7 * 24 * 60 * 60 * 1000;

function getCachedTafsir(verseKey: string, lang: string): TafsirData | null {
  try {
    const raw = localStorage.getItem(`${TAFSIR_CACHE_PREFIX}${lang}_${verseKey}`);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (Date.now() - parsed.ts > TAFSIR_CACHE_TTL) return null;
    return parsed.data;
  } catch { return null; }
}

function setCachedTafsir(verseKey: string, lang: string, data: TafsirData) {
  try {
    localStorage.setItem(`${TAFSIR_CACHE_PREFIX}${lang}_${verseKey}`, JSON.stringify({ ts: Date.now(), data }));
  } catch { /* full */ }
}

// ── Revelation Labels ──
const REV_LABELS: Record<string, Record<string, string>> = {
  makkah: { ar: 'مكية', en: 'Meccan', fr: 'Mecquoise', de: 'Mekkanisch', tr: 'Mekki', ru: 'Мекканская', sv: 'Meckansk', nl: 'Mekkaans', el: 'Μεκκανική' },
  madinah: { ar: 'مدنية', en: 'Medinan', fr: 'Médinoise', de: 'Medinensisch', tr: 'Medeni', ru: 'Мединская', sv: 'Medinsk', nl: 'Medinaans', el: 'Μεδινική' },
};

// ── Share as Image ──
async function shareAyahAsImage(
  ayahText: string, tafsirText: string, surahName: string, verseNum: number, tafsirSource: string, t: (k: string) => string
) {
  const canvas = document.createElement('canvas');
  const w = 1080, h = 1920;
  canvas.width = w; canvas.height = h;
  const ctx = canvas.getContext('2d')!;

  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, '#064E3B'); grad.addColorStop(0.5, '#065F46'); grad.addColorStop(1, '#064E3B');
  ctx.fillStyle = grad; ctx.fillRect(0, 0, w, h);

  ctx.fillStyle = 'rgba(212, 175, 55, 0.3)';
  ctx.fillRect(40, 40, w - 80, 4); ctx.fillRect(40, h - 44, w - 80, 4);
  ctx.fillRect(40, 40, 4, h - 80); ctx.fillRect(w - 44, 40, 4, h - 80);

  ctx.fillStyle = 'rgba(212, 175, 55, 0.8)'; ctx.font = '36px serif'; ctx.textAlign = 'center';
  ctx.fillText('﷽', w / 2, 120);

  ctx.fillStyle = 'rgba(255,255,255,0.7)'; ctx.font = '28px sans-serif';
  ctx.fillText(`${surahName} - ${t('tafsirVerse') || 'Verse'} ${verseNum}`, w / 2, 180);

  ctx.fillStyle = '#FFFFFF'; ctx.font = '44px serif'; ctx.direction = 'rtl';
  const ayahLines = wrapText(ctx, ayahText, w - 160, 44);
  let y = 290;
  for (const line of ayahLines) { ctx.fillText(line, w / 2, y); y += 70; }

  y += 30;
  ctx.fillStyle = 'rgba(212, 175, 55, 0.4)'; ctx.fillRect(80, y, w - 160, 2); y += 40;
  ctx.fillStyle = 'rgba(212, 175, 55, 0.9)'; ctx.font = 'bold 26px sans-serif'; ctx.direction = 'ltr';
  ctx.fillText(`📖 ${tafsirSource}`, w / 2, y); y += 50;

  ctx.fillStyle = 'rgba(255,255,255,0.85)'; ctx.font = '28px sans-serif'; ctx.direction = 'rtl';
  const tafsirLines = wrapText(ctx, tafsirText, w - 160, 28);
  for (let i = 0; i < Math.min(tafsirLines.length, 18); i++) { ctx.fillText(tafsirLines[i], w / 2, y); y += 46; }

  ctx.fillStyle = 'rgba(255,255,255,0.9)'; ctx.font = 'bold 30px sans-serif'; ctx.textAlign = 'center'; ctx.direction = 'ltr';
  ctx.fillText('أذان وحكاية | Athan & Hikaya', w / 2, h - 90);

  canvas.toBlob(async (blob) => {
    if (!blob) return;
    const file = new File([blob], `quran-${surahName}-${verseNum}.png`, { type: 'image/png' });
    if (navigator.share && navigator.canShare?.({ files: [file] })) {
      try { await navigator.share({ files: [file], title: `${surahName} - ${verseNum}` }); return; } catch {}
    }
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = file.name; a.click();
    URL.revokeObjectURL(url);
    toast.success(t('shareAsImage') || 'Image saved!');
  }, 'image/png');
}

function wrapText(ctx: CanvasRenderingContext2D, text: string, maxWidth: number, _fontSize: number): string[] {
  const words = text.split(' ');
  const lines: string[] = [];
  let currentLine = '';
  for (const word of words) {
    const testLine = currentLine ? `${currentLine} ${word}` : word;
    if (ctx.measureText(testLine).width > maxWidth && currentLine) {
      lines.push(currentLine);
      currentLine = word;
    } else { currentLine = testLine; }
  }
  if (currentLine) lines.push(currentLine);
  return lines;
}

// ═══════════════════════════════════════
// AYAH CARD — Arabic + Translation + Tafsir
// ═══════════════════════════════════════
function AyahCard({
  ayah, surahId, surahName, locale, playing, onPlay, t,
}: {
  ayah: Ayah; surahId: string; surahName: string; locale: string;
  playing: number | null; onPlay: (a: Ayah) => void; t: (k: string) => string;
}) {
  const [showTafsir, setShowTafsir] = useState(false);
  const [tafsir, setTafsir] = useState<TafsirData | null>(null);
  const [loadingTafsir, setLoadingTafsir] = useState(false);
  const [sharing, setSharing] = useState(false);
  const verseKey = `${surahId}:${ayah.numberInSurah}`;

  const fetchTafsir = useCallback(async () => {
    if (tafsir) { setShowTafsir(v => !v); return; }
    const cached = getCachedTafsir(verseKey, locale);
    if (cached) { setTafsir(cached); setShowTafsir(true); return; }

    setLoadingTafsir(true); setShowTafsir(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/quran/v4/global-verse/${surahId}/${ayah.numberInSurah}?language=${locale}`);
      const data = await res.json();
      if (data.success && data.tafsir) {
        const td: TafsirData = { text: data.tafsir, tafsir_name: data.tafsir_source || '', is_fallback_language: data.tafsir_is_arabic || false, verse_key: verseKey };
        setTafsir(td);
        setCachedTafsir(verseKey, locale, td);
      } else {
        setTafsir({ text: '', tafsir_name: '', is_fallback_language: false, verse_key: verseKey });
      }
    } catch {
      toast.error(t('tafsirError'));
      setShowTafsir(false);
    } finally { setLoadingTafsir(false); }
  }, [tafsir, verseKey, locale, surahId, ayah.numberInSurah, t]);

  const handleShare = async () => {
    if (!tafsir?.text) return;
    setSharing(true);
    try {
      await shareAyahAsImage(ayah.text, tafsir.text, surahName, ayah.numberInSurah, tafsir.tafsir_name || '', t);
    } catch {} finally { setSharing(false); }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="rounded-2xl border border-border/10 bg-card overflow-hidden shadow-sm">
      {/* Verse Number Bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-emerald-500/5 border-b border-border/10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 text-xs font-bold">
            {ayah.numberInSurah}
          </div>
          <Button variant="ghost" size="icon" className="h-8 w-8 rounded-lg" onClick={() => onPlay(ayah)}>
            {playing === ayah.numberInSurah ? <Pause className="h-4 w-4 text-primary" /> : <Play className="h-4 w-4 text-muted-foreground" />}
          </Button>
        </div>
        <button onClick={fetchTafsir} className="flex items-center gap-1.5 text-[10px] font-bold text-emerald-700 dark:text-emerald-300 hover:underline">
          <BookOpen className="h-3 w-3" />
          {showTafsir ? t('hideExplanation') : t('showExplanation')}
          {loadingTafsir ? <Loader2 className="h-3 w-3 animate-spin" /> : showTafsir ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
        </button>
      </div>

      <div className="p-5">
        {/* Arabic Text — ALWAYS VISIBLE */}
        <p className="text-right text-[22px] leading-[2.5] font-arabic text-foreground mb-4" dir="rtl">
          {ayah.text}
        </p>

        {/* Translation */}
        {ayah.translation && (
          <div className="pt-3 border-t border-border/20">
            <p className="text-[10px] font-bold text-emerald-700 dark:text-emerald-300 mb-1.5 uppercase tracking-wider">
              {t('meaningTranslation')}
            </p>
            <p className="text-sm text-foreground/80 leading-relaxed" dir="auto">
              {ayah.translation}
            </p>
          </div>
        )}

        {/* Tafsir Section */}
        <AnimatePresence>
          {showTafsir && (
            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.3 }} className="overflow-hidden">
              <div className="mt-4 p-4 rounded-xl bg-gradient-to-br from-emerald-500/5 to-teal-500/5 border border-emerald-500/15">
                {loadingTafsir ? (
                  <div className="flex items-center justify-center gap-2 py-6">
                    <Loader2 className="h-5 w-5 animate-spin text-emerald-500" />
                    <span className="text-sm text-muted-foreground">{t('loadingTafsir')}</span>
                  </div>
                ) : tafsir?.text ? (
                  <>
                    <div className="flex items-center gap-2 mb-3">
                      <BookOpen className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
                      <span className="text-xs font-bold text-emerald-700 dark:text-emerald-300">
                        {tafsir.tafsir_name || t('tafsirMuyassar')}
                      </span>
                    </div>

                    {tafsir.is_fallback_language && (
                      <div className="mb-3 p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20">
                        <p className="text-xs text-amber-700 dark:text-amber-300 text-center">
                          📖 {t('arabicTafsirNote')}
                        </p>
                      </div>
                    )}

                    <p className={`text-sm text-foreground/85 leading-[2] whitespace-pre-wrap ${tafsir.is_fallback_language ? 'font-arabic text-right' : ''}`} dir={tafsir.is_fallback_language ? 'rtl' : 'auto'}>
                      {tafsir.text}
                    </p>

                    <div className="mt-4 pt-3 border-t border-emerald-500/10">
                      <button onClick={handleShare} disabled={sharing} className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition-all active:scale-[0.97] disabled:opacity-50">
                        {sharing ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Share2 className="h-3.5 w-3.5" />}
                        {t('shareAsImage')}
                      </button>
                    </div>
                  </>
                ) : (
                  <p className="text-sm text-muted-foreground text-center py-4">{t('tafsirNotAvailable')}</p>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}

// ═══════════════════════════════════════
// MAIN SURAH VIEW
// ═══════════════════════════════════════
export default function SurahView() {
  const { id } = useParams();
  const { t, isRTL, locale } = useLocale();
  const navigate = useNavigate();
  const [ayahs, setAyahs] = useState<Ayah[]>([]);
  const [surahInfo, setSurahInfo] = useState<SurahInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [playing, setPlaying] = useState<number | null>(null);
  const [audio] = useState(new Audio());
  const [bookmarked, setBookmarked] = useState(false);

  const lang = locale?.split('-')[0] || 'ar';
  const surahNum = parseInt(id || '1');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch chapter info
        const chRes = await fetch(`${BACKEND_URL}/api/quran/v4/chapters/${id}?language=${lang}`);
        const chData = await chRes.json();
        const ch = chData.chapter || {};
        setSurahInfo({
          id: ch.id,
          name_arabic: ch.name_arabic || '',
          name_simple: ch.name_simple || '',
          translated_name: ch.translated_name?.name || ch.name_simple || '',
          verses_count: ch.verses_count || 0,
          revelation_place: ch.revelation_place || '',
        });

        // Fetch verses with translations
        const vRes = await fetch(`${BACKEND_URL}/api/quran/v4/verses/by_chapter/${id}?language=${lang}&per_page=300`);
        const vData = await vRes.json();
        const padNum = (n: number) => String(n).padStart(3, '0');
        const ayahsList: Ayah[] = (vData.verses || []).map((v: any) => {
          let tr = '';
          if (v.translations?.[0]?.text) {
            tr = v.translations[0].text.replace(/<sup[^>]*>[\s\S]*?<\/sup>/gi, '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim();
          }
          return {
            number: v.id || v.verse_number,
            text: v.text_uthmani || v.text || '',
            numberInSurah: v.verse_number,
            audio: `https://everyayah.com/data/Alafasy_128kbps/${padNum(surahNum)}${padNum(v.verse_number)}.mp3`,
            translation: lang !== 'ar' ? tr : undefined,
          };
        });
        setAyahs(ayahsList);
      } catch (err) {
        console.error('Fetch error:', err);
        try {
          const r = await fetch(`https://api.alquran.cloud/v1/surah/${id}/ar.alafasy`);
          const d = await r.json();
          setAyahs(d.data.ayahs);
          setSurahInfo({ id: d.data.number, name_arabic: d.data.name, name_simple: d.data.englishName, translated_name: d.data.englishNameTranslation, verses_count: d.data.numberOfAyahs, revelation_place: d.data.revelationType });
        } catch {}
      }
      setLoading(false);
    };
    fetchData();

    const saved: number[] = JSON.parse(localStorage.getItem('quran_bookmarks') || '[]');
    setBookmarked(saved.includes(surahNum));

    return () => { audio.pause(); };
  }, [id, lang, surahNum]);

  const toggleBookmark = () => {
    const saved: number[] = JSON.parse(localStorage.getItem('quran_bookmarks') || '[]');
    const updated = bookmarked ? saved.filter(n => n !== surahNum) : [...saved, surahNum];
    localStorage.setItem('quran_bookmarks', JSON.stringify(updated));
    setBookmarked(!bookmarked);
    toast.success(bookmarked ? t('surahRemovedFromFav') : t('surahAddedToFav'));
  };

  const playAyah = (ayah: Ayah) => {
    if (playing === ayah.numberInSurah) { audio.pause(); setPlaying(null); }
    else { audio.src = ayah.audio; audio.play(); setPlaying(ayah.numberInSurah); audio.onended = () => setPlaying(null); }
  };

  const BackIcon = isRTL ? ArrowRight : ArrowLeft;
  const handleBack = () => {
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) window.history.back();
    else navigate('/quran', { replace: true });
  };

  const getRevLabel = (place: string) => {
    const key = place?.toLowerCase() === 'madinah' ? 'madinah' : 'makkah';
    return REV_LABELS[key]?.[lang] || REV_LABELS[key]?.['en'] || place;
  };

  const displayName = lang === 'ar' ? surahInfo?.name_arabic : surahInfo?.translated_name;

  return (
    <div className="min-h-screen pb-24" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="gradient-islamic relative px-5 pb-12 pt-safe-header-compact">
        <div className="absolute inset-0 islamic-pattern opacity-15" />
        <div className="relative z-10">
          {/* Top Bar */}
          <div className="flex items-center justify-between mb-4">
            <button onClick={handleBack} className="p-2 -ml-2 rounded-xl hover:bg-white/10">
              <BackIcon className="h-5 w-5 text-primary-foreground" />
            </button>
            <Button variant="ghost" size="icon" onClick={toggleBookmark} className="text-primary-foreground hover:bg-white/10 rounded-xl">
              {bookmarked ? <BookmarkCheck className="h-5 w-5 fill-current" /> : <Bookmark className="h-5 w-5" />}
            </Button>
          </div>

          {/* Surah Info */}
          {surahInfo && (
            <div className="text-center">
              <p className="text-3xl font-arabic text-primary-foreground/80 mb-2">﷽</p>
              <h1 className="text-2xl font-bold text-primary-foreground font-arabic mb-1">
                {surahInfo.name_arabic}
              </h1>
              {lang !== 'ar' && (
                <p className="text-lg text-primary-foreground/80 font-medium mb-1">
                  {surahInfo.translated_name}
                </p>
              )}
              <div className="flex items-center justify-center gap-3 mt-2">
                <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                  surahInfo.revelation_place?.toLowerCase() === 'makkah'
                    ? 'bg-amber-500/20 text-amber-200 border border-amber-400/20'
                    : 'bg-blue-500/20 text-blue-200 border border-blue-400/20'
                }`}>
                  <MapPin className="inline h-3 w-3 -mt-0.5 mr-1" />
                  {getRevLabel(surahInfo.revelation_place)}
                </span>
                <span className="text-xs text-primary-foreground/60">
                  {surahInfo.verses_count} {t('ayahs')}
                </span>
              </div>
            </div>
          )}
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Bismillah */}
      {id !== '1' && id !== '9' && (
        <div className="text-center py-6 px-5">
          <p className="text-2xl font-arabic text-foreground leading-loose">بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ</p>
        </div>
      )}

      {/* Ayahs */}
      <div className="px-4 space-y-3 pb-8">
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            <p className="mt-3 text-sm text-muted-foreground">{t('loading')}</p>
          </div>
        ) : (
          ayahs.map(ayah => (
            <AyahCard
              key={ayah.number}
              ayah={ayah}
              surahId={id!}
              surahName={displayName || ''}
              locale={lang}
              playing={playing}
              onPlay={playAyah}
              t={t}
            />
          ))
        )}
      </div>

      {/* Navigation: Prev/Next Surah */}
      <div className="px-5 pb-10 flex gap-3">
        {surahNum > 1 && (
          <button
            onClick={() => navigate(`/quran/${surahNum - 1}`)}
            className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl bg-card border border-border/30 hover:border-primary/30 transition-all active:scale-[0.98]"
          >
            {isRTL ? <ArrowRight className="h-4 w-4 text-muted-foreground" /> : <ArrowLeft className="h-4 w-4 text-muted-foreground" />}
            <span className="text-sm font-medium text-foreground">{t('prevSurah')}</span>
          </button>
        )}
        {surahNum < 114 && (
          <button
            onClick={() => navigate(`/quran/${surahNum + 1}`)}
            className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl bg-card border border-border/30 hover:border-primary/30 transition-all active:scale-[0.98]"
          >
            <span className="text-sm font-medium text-foreground">{t('nextSurah')}</span>
            {isRTL ? <ArrowLeft className="h-4 w-4 text-muted-foreground" /> : <ArrowRight className="h-4 w-4 text-muted-foreground" />}
          </button>
        )}
      </div>
    </div>
  );
}
