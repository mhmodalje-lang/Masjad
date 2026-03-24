/**
 * GlobalQuranVerse — V2026 Architecture Overhaul
 * ================================================
 * SINGLE reusable component for displaying Quran verses across ALL pages.
 * Used in: Home Page, Noor Academy, Stories, Main Quran Reader, Tafsir page.
 *
 * Props:
 *   surahId   - Surah number (1-114)
 *   ayahId    - Ayah number within the surah
 *   compact   - Smaller layout for inline usage (default: false)
 *   showExplanation - Show "Tafsir/Explanation" button (default: true)
 *   showAudio - Show audio play button (default: true)
 *   showSurahName - Show surah name header (default: true)
 *   className - Additional CSS classes
 *
 * Auto-detects language from i18n context (useLocale hook).
 * Fetches from: /api/quran/v4/global-verse/{surah_id}/{ayah_id}?language={lang}
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { BookOpen, Volume2, VolumeX, ChevronDown, ChevronUp } from 'lucide-react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface GlobalVerseData {
  arabic_text: string;
  translation: string;
  tafsir: string;
  tafsir_source: string;
  surah_name: string;
  surah_name_translated: string;
  verse_number: number;
  audio_url: string;
  verse_key: string;
}

interface GlobalQuranVerseProps {
  surahId: number;
  ayahId: number;
  compact?: boolean;
  showExplanation?: boolean;
  showAudio?: boolean;
  showSurahName?: boolean;
  className?: string;
  onLoaded?: (data: GlobalVerseData) => void;
}

// Local cache to avoid refetching the same verse
const verseCache = new Map<string, GlobalVerseData>();

export default function GlobalQuranVerse({
  surahId,
  ayahId,
  compact = false,
  showExplanation = true,
  showAudio = true,
  showSurahName = true,
  className = '',
  onLoaded,
}: GlobalQuranVerseProps) {
  const { locale, t } = useLocale();
  const [data, setData] = useState<GlobalVerseData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [explanationOpen, setExplanationOpen] = useState(false);
  const [playing, setPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const isAr = locale === 'ar';

  const fetchVerse = useCallback(async () => {
    const cacheKey = `${locale}_${surahId}_${ayahId}`;

    // Check in-memory cache first
    if (verseCache.has(cacheKey)) {
      const cached = verseCache.get(cacheKey)!;
      setData(cached);
      setLoading(false);
      onLoaded?.(cached);
      return;
    }

    setLoading(true);
    setError(false);

    try {
      const res = await fetch(
        `${BACKEND_URL}/api/quran/v4/global-verse/${surahId}/${ayahId}?language=${locale}`
      );
      if (!res.ok) throw new Error('API error');
      const json = await res.json();

      if (json.success) {
        const verseData: GlobalVerseData = {
          arabic_text: json.arabic_text || '',
          translation: json.translation || '',
          tafsir: json.tafsir || '',
          tafsir_source: json.tafsir_source || '',
          surah_name: json.surah_name || '',
          surah_name_translated: json.surah_name_translated || '',
          verse_number: json.verse_number || ayahId,
          audio_url: json.audio_url || '',
          verse_key: json.verse_key || `${surahId}:${ayahId}`,
        };
        verseCache.set(cacheKey, verseData);
        setData(verseData);
        onLoaded?.(verseData);
      } else {
        setError(true);
      }
    } catch {
      setError(true);
    }
    setLoading(false);
  }, [surahId, ayahId, locale, onLoaded]);

  useEffect(() => {
    fetchVerse();
  }, [fetchVerse]);

  // Audio controls
  const toggleAudio = useCallback(() => {
    if (!data?.audio_url) return;

    if (playing && audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setPlaying(false);
      return;
    }

    const audio = new Audio(data.audio_url);
    audioRef.current = audio;
    audio.play().catch(() => {});
    setPlaying(true);
    audio.onended = () => setPlaying(false);
    audio.onerror = () => setPlaying(false);
  }, [data, playing]);

  // Cleanup audio on unmount
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  // ─── LOADING STATE ───
  if (loading) {
    return (
      <div className={`animate-pulse rounded-2xl bg-card/60 border border-border/20 ${compact ? 'p-3' : 'p-4'} ${className}`}>
        <div className="h-6 bg-muted/30 rounded-lg w-3/4 mx-auto mb-3" />
        <div className="h-4 bg-muted/20 rounded-lg w-1/2 mx-auto" />
      </div>
    );
  }

  // ─── ERROR STATE ───
  if (error || !data) {
    return (
      <div className={`rounded-2xl bg-card/60 border border-red-500/20 ${compact ? 'p-3' : 'p-4'} text-center ${className}`}>
        <p className="text-xs text-red-400">{t('verseLoadError') || 'Unable to load verse'}</p>
        <button onClick={fetchVerse} className="text-xs text-primary mt-1 underline">{t('retry') || 'Retry'}</button>
      </div>
    );
  }

  // ─── COMPACT MODE ───
  if (compact) {
    return (
      <div className={`rounded-xl bg-card/60 border border-border/20 p-3 ${className}`}>
        {/* Arabic text */}
        <p
          className="text-base font-arabic text-foreground leading-[2] text-center"
          dir="rtl"
          style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}
        >
          ﴿{data.arabic_text}﴾
        </p>

        {/* Translation (non-Arabic) */}
        {!isAr && data.translation && (
          <p className="text-xs text-muted-foreground leading-relaxed text-center mt-1.5 border-t border-border/20 pt-1.5" dir="auto">
            {data.translation}
          </p>
        )}

        {/* Surah reference */}
        {showSurahName && (
          <p className="text-[10px] text-muted-foreground/60 text-center mt-1" dir="auto">
            {data.surah_name_translated || data.surah_name} — {t('ayahLabel') || 'Ayah'} {data.verse_number}
          </p>
        )}
      </div>
    );
  }

  // ─── FULL MODE ───
  return (
    <div className={`rounded-2xl bg-card border border-primary/10 overflow-hidden ${className}`}>
      {/* Surah Header */}
      {showSurahName && (
        <div className="px-4 py-2.5 bg-gradient-to-r from-emerald-600/10 to-teal-600/10 border-b border-primary/10 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-emerald-500/20 flex items-center justify-center text-[10px] font-bold text-emerald-500">
              {data.verse_number}
            </span>
            <div>
              <p className="text-sm font-bold font-arabic text-foreground">{data.surah_name}</p>
              {!isAr && data.surah_name_translated && (
                <p className="text-[10px] text-muted-foreground">{data.surah_name_translated}</p>
              )}
            </div>
          </div>

          {/* Audio button */}
          {showAudio && (
            <button
              onClick={toggleAudio}
              className={`w-8 h-8 rounded-full flex items-center justify-center transition-all ${
                playing
                  ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                  : 'bg-muted/30 text-muted-foreground hover:bg-emerald-500/20 hover:text-emerald-500'
              }`}
            >
              {playing ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
            </button>
          )}
        </div>
      )}

      {/* Verse Content */}
      <div className="p-4">
        {/* Arabic text */}
        <p
          className="text-xl font-arabic text-foreground leading-[2.4] text-center"
          dir="rtl"
          style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}
        >
          ﴿{data.arabic_text}﴾
        </p>

        {/* Divider */}
        <div className="w-16 h-[1px] mx-auto my-3 bg-gradient-to-r from-transparent via-primary/20 to-transparent" />

        {/* Translation */}
        {!isAr && data.translation && (
          <p className="text-sm text-muted-foreground leading-relaxed text-center px-2" dir="auto">
            {data.translation}
          </p>
        )}

        {/* Explanation / Tafsir toggle */}
        {showExplanation && data.explanation && data.explanation !== data.translation && (
          <div className="mt-3">
            <button
              onClick={() => setExplanationOpen(!explanationOpen)}
              className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-amber-500/10 border border-amber-400/20 hover:bg-amber-500/15 transition-all"
            >
              <BookOpen className="h-3.5 w-3.5 text-amber-600 dark:text-amber-400" />
              <span className="text-xs font-bold text-amber-700 dark:text-amber-400">
                {t('showExplanation') || t('tafsirButton') || 'Show Explanation'}
              </span>
              {explanationOpen
                ? <ChevronUp className="h-3 w-3 text-amber-500" />
                : <ChevronDown className="h-3 w-3 text-amber-500" />
              }
            </button>

            {explanationOpen && (
              <div className="mt-2 p-3 rounded-xl bg-amber-500/5 border border-amber-400/10">
                <p className="text-sm text-foreground/80 leading-relaxed" dir="auto">
                  {data.explanation}
                </p>
                {data.explanation_source && (
                  <p className="text-[10px] text-muted-foreground/50 mt-2 text-end" dir="auto">
                    — {data.explanation_source}
                  </p>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Export cache clear utility for when language changes
 */
export function clearVerseCache() {
  verseCache.clear();
}
