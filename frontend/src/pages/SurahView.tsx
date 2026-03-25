import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useLocale } from '@/hooks/useLocale';
import { ArrowLeft, ArrowRight, Play, Pause, Volume2, BookOpen, ChevronDown, ChevronUp, Loader2, BookMarked } from 'lucide-react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

// Multilingual labels
const LABELS: Record<string, Record<string, string>> = {
  translation: { ar: 'الترجمة', en: 'Translation', de: 'Übersetzung', fr: 'Traduction', tr: 'Tercüme', ru: 'Перевод', sv: 'Översättning', nl: 'Vertaling', el: 'Μετάφραση' },
  tafsir: { ar: 'التفسير', en: 'Tafsir', de: 'Tafsir', fr: 'Tafsir', tr: 'Tefsir', ru: 'Тафсир', sv: 'Tafsir', nl: 'Tafsir', el: 'Τάφσιρ' },
  arabic_tafsir: { ar: 'تفسير عربي', en: 'Arabic Tafsir', de: 'Arabischer Tafsir', fr: 'Tafsir en arabe', tr: 'Arapça Tefsir', ru: 'Арабский тафсир', sv: 'Arabisk Tafsir', nl: 'Arabische Tafsir', el: 'Αραβικό Τάφσιρ' },
  verse: { ar: 'آية', en: 'Verse', de: 'Vers', fr: 'Verset', tr: 'Ayet', ru: 'Аят', sv: 'Vers', nl: 'Vers', el: 'Εδάφιο' },
  loading: { ar: 'جاري التحميل...', en: 'Loading...', de: 'Laden...', fr: 'Chargement...', tr: 'Yükleniyor...', ru: 'Загрузка...', sv: 'Laddar...', nl: 'Laden...', el: 'Φόρτωση...' },
  show_tafsir: { ar: 'عرض التفسير', en: 'Show Tafsir', de: 'Tafsir anzeigen', fr: 'Afficher le Tafsir', tr: 'Tefsiri Göster', ru: 'Показать тафсир', sv: 'Visa Tafsir', nl: 'Tafsir tonen', el: 'Εμφάνιση Τάφσιρ' },
  hide_tafsir: { ar: 'إخفاء التفسير', en: 'Hide Tafsir', de: 'Tafsir ausblenden', fr: 'Masquer le Tafsir', tr: 'Tefsiri Gizle', ru: 'Скрыть тафсир', sv: 'Dölj Tafsir', nl: 'Tafsir verbergen', el: 'Απόκρυψη Τάφσιρ' },
  source: { ar: 'المصدر', en: 'Source', de: 'Quelle', fr: 'Source', tr: 'Kaynak', ru: 'Источник', sv: 'Källa', nl: 'Bron', el: 'Πηγή' },
  next_surah: { ar: 'السورة التالية', en: 'Next Surah', de: 'Nächste Sure', fr: 'Sourate suivante', tr: 'Sonraki Sûre', ru: 'Следующая сура', sv: 'Nästa sura', nl: 'Volgende soera', el: 'Επόμενη σούρα' },
  prev_surah: { ar: 'السورة السابقة', en: 'Previous Surah', de: 'Vorherige Sure', fr: 'Sourate précédente', tr: 'Önceki Sûre', ru: 'Предыдущая сура', sv: 'Föregående sura', nl: 'Vorige soera', el: 'Προηγούμενη σούρα' },
};

function getLabel(key: string, lang: string): string {
  return LABELS[key]?.[lang] || LABELS[key]?.en || key;
}

interface Verse {
  verse_key: string;
  verse_number: number;
  arabic_text: string;
  translation: string;
  audio_url: string;
}

interface TafsirData {
  tafsir: string;
  tafsir_source: string;
  tafsir_is_arabic: boolean;
}

export default function SurahView() {
  const { id } = useParams<{ id: string }>();
  const surahId = parseInt(id || '1');
  const navigate = useNavigate();
  const { locale, isRTL } = useLocale();
  const lang = useMemo(() => locale?.split('-')[0] || 'ar', [locale]);

  const [surahInfo, setSurahInfo] = useState<any>(null);
  const [verses, setVerses] = useState<Verse[]>([]);
  const [loading, setLoading] = useState(true);
  const [playingVerse, setPlayingVerse] = useState<number | null>(null);
  const [expandedTafsir, setExpandedTafsir] = useState<Record<number, TafsirData | null>>({});
  const [loadingTafsir, setLoadingTafsir] = useState<Record<number, boolean>>({});
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Fetch surah info
  useEffect(() => {
    fetch(`${BACKEND_URL}/api/quran/v4/chapters/${surahId}?language=${lang}`)
      .then(r => r.json())
      .then(data => setSurahInfo(data.chapter || null))
      .catch(() => {});
  }, [surahId, lang]);

  // Fetch verses
  useEffect(() => {
    setLoading(true);
    setVerses([]);
    setExpandedTafsir({});
    const versesCount = surahInfo?.verses_count || 7;
    fetch(`${BACKEND_URL}/api/quran/v4/global-verse/bulk/${surahId}?language=${lang}&from_ayah=1&to_ayah=${versesCount}`)
      .then(r => r.json())
      .then(data => {
        setVerses(data.verses || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [surahId, lang, surahInfo?.verses_count]);

  // Play audio
  const playAudio = useCallback((verse: Verse) => {
    if (audioRef.current) {
      audioRef.current.pause();
    }
    if (playingVerse === verse.verse_number) {
      setPlayingVerse(null);
      return;
    }
    const audio = new Audio(verse.audio_url);
    audioRef.current = audio;
    audio.play().catch(() => {});
    setPlayingVerse(verse.verse_number);
    audio.onended = () => setPlayingVerse(null);
  }, [playingVerse]);

  // Fetch tafsir for a verse
  const fetchTafsir = useCallback(async (verseNumber: number) => {
    if (expandedTafsir[verseNumber] !== undefined) {
      setExpandedTafsir(prev => {
        const next = { ...prev };
        if (next[verseNumber] !== undefined) {
          delete next[verseNumber];
        }
        return next;
      });
      return;
    }
    setLoadingTafsir(prev => ({ ...prev, [verseNumber]: true }));
    try {
      const r = await fetch(`${BACKEND_URL}/api/quran/v4/global-verse/${surahId}/${verseNumber}?language=${lang}`);
      const data = await r.json();
      setExpandedTafsir(prev => ({
        ...prev,
        [verseNumber]: {
          tafsir: data.tafsir || '',
          tafsir_source: data.tafsir_source || '',
          tafsir_is_arabic: data.tafsir_is_arabic || false,
        }
      }));
    } catch {
      setExpandedTafsir(prev => ({ ...prev, [verseNumber]: { tafsir: '', tafsir_source: '', tafsir_is_arabic: false } }));
    }
    setLoadingTafsir(prev => ({ ...prev, [verseNumber]: false }));
  }, [expandedTafsir, surahId, lang]);

  const BackArrow = isRTL ? ArrowRight : ArrowLeft;
  const NextArrow = isRTL ? ArrowLeft : ArrowRight;

  return (
    <div className={`min-h-screen bg-gradient-to-b from-emerald-50 via-white to-teal-50 dark:from-gray-900 dark:via-gray-950 dark:to-gray-900 ${isRTL ? 'rtl' : 'ltr'}`} dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-700 dark:from-emerald-800 dark:to-teal-900 px-4 py-6">
        <div className="max-w-2xl mx-auto">
          <button onClick={() => navigate('/quran')} className="flex items-center gap-2 text-white/80 hover:text-white mb-3 transition-colors">
            <BackArrow className="w-5 h-5" />
            <span className="text-sm">{lang === 'ar' ? 'القرآن الكريم' : "Quran"}</span>
          </button>
          {surahInfo && (
            <div className="text-center">
              <h1 className="text-3xl font-bold text-white mb-1">{surahInfo.name_arabic}</h1>
              {lang !== 'ar' && (
                <p className="text-emerald-100 text-lg">{surahInfo.translated_name?.name || surahInfo.name_simple}</p>
              )}
              <p className="text-emerald-200/70 text-sm mt-1">
                {surahInfo.verses_count} {getLabel('verse', lang)} • {surahInfo.revelation_place === 'Makkah' ? (lang === 'ar' ? 'مكية' : 'Meccan') : (lang === 'ar' ? 'مدنية' : 'Medinan')}
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-4 py-6">
        {/* Bismillah (except for Surah 1 and 9) */}
        {surahId !== 1 && surahId !== 9 && (
          <div className="text-center py-6 mb-4">
            <p className="text-2xl font-arabic text-emerald-800 dark:text-emerald-300" style={{ fontFamily: "'Amiri', 'Traditional Arabic', serif" }}>
              بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ
            </p>
          </div>
        )}

        {/* Loading */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
            <span className="text-gray-400 text-sm">{getLabel('loading', lang)}</span>
          </div>
        ) : (
          /* Verses */
          <div className="space-y-4 pb-8">
            {verses.map(verse => {
              const tafsirData = expandedTafsir[verse.verse_number];
              const isTafsirLoading = loadingTafsir[verse.verse_number];
              const isExpanded = tafsirData !== undefined;

              return (
                <div key={verse.verse_key} className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700/50 shadow-sm overflow-hidden">
                  {/* Verse Header */}
                  <div className="flex items-center justify-between px-4 py-2.5 bg-emerald-50/50 dark:bg-emerald-900/10 border-b border-emerald-100/50 dark:border-emerald-800/20">
                    <div className="flex items-center gap-2">
                      <span className="w-8 h-8 flex items-center justify-center bg-emerald-600 text-white rounded-lg text-sm font-bold">
                        {verse.verse_number}
                      </span>
                      <span className="text-xs text-gray-400">{verse.verse_key}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      {/* Audio Button */}
                      <button
                        onClick={() => playAudio(verse)}
                        className={`p-2 rounded-xl transition-all ${playingVerse === verse.verse_number ? 'bg-emerald-600 text-white' : 'hover:bg-emerald-100 dark:hover:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400'}`}
                      >
                        {playingVerse === verse.verse_number ? <Pause className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                      </button>
                      {/* Tafsir Button */}
                      <button
                        onClick={() => fetchTafsir(verse.verse_number)}
                        className={`flex items-center gap-1 px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${isExpanded ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400' : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 dark:text-gray-400'}`}
                      >
                        <BookMarked className="w-3.5 h-3.5" />
                        {isExpanded ? (
                          <><span>{getLabel('hide_tafsir', lang)}</span><ChevronUp className="w-3 h-3" /></>
                        ) : (
                          <><span>{getLabel('show_tafsir', lang)}</span><ChevronDown className="w-3 h-3" /></>
                        )}
                      </button>
                    </div>
                  </div>

                  {/* Arabic Text */}
                  <div className="px-5 py-5" dir="rtl">
                    <p className="text-2xl leading-[2.2] text-gray-900 dark:text-white text-right" style={{ fontFamily: "'Amiri', 'Traditional Arabic', serif", lineHeight: '2.2' }}>
                      {verse.arabic_text}
                      <span className="inline-block text-emerald-600 dark:text-emerald-400 text-lg mx-1">﴿{verse.verse_number}﴾</span>
                    </p>
                  </div>

                  {/* Translation */}
                  {lang !== 'ar' && verse.translation && (
                    <div className={`px-5 pb-4 border-t border-gray-100 dark:border-gray-700/30 pt-3 ${isRTL ? 'text-right' : 'text-left'}`}>
                      <p className="text-xs font-medium text-emerald-600 dark:text-emerald-400 mb-1.5">{getLabel('translation', lang)}</p>
                      <p className="text-[15px] leading-relaxed text-gray-700 dark:text-gray-300">
                        {verse.translation}
                      </p>
                    </div>
                  )}

                  {/* Tafsir */}
                  {isTafsirLoading && (
                    <div className="px-5 pb-4 flex items-center gap-2 text-gray-400">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span className="text-sm">{getLabel('loading', lang)}</span>
                    </div>
                  )}
                  {isExpanded && tafsirData?.tafsir && (
                    <div className={`px-5 pb-4 border-t border-amber-100 dark:border-amber-800/20 pt-3 bg-amber-50/30 dark:bg-amber-900/5 ${tafsirData.tafsir_is_arabic ? 'text-right' : isRTL ? 'text-right' : 'text-left'}`} dir={tafsirData.tafsir_is_arabic ? 'rtl' : isRTL ? 'rtl' : 'ltr'}>
                      <div className="flex items-center gap-2 mb-2">
                        <BookOpen className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                        <span className="text-xs font-medium text-amber-600 dark:text-amber-400">
                          {tafsirData.tafsir_is_arabic ? getLabel('arabic_tafsir', lang) : getLabel('tafsir', lang)}
                        </span>
                      </div>
                      <p className="text-[14px] leading-relaxed text-gray-700 dark:text-gray-300" style={tafsirData.tafsir_is_arabic ? { fontFamily: "'Amiri', serif" } : {}}>
                        {tafsirData.tafsir}
                      </p>
                      {tafsirData.tafsir_source && (
                        <p className="mt-2 text-[11px] text-gray-400 dark:text-gray-500 italic">
                          {getLabel('source', lang)}: {tafsirData.tafsir_source}
                        </p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Navigation */}
        {!loading && (
          <div className="flex items-center justify-between pb-24 pt-4">
            {surahId > 1 ? (
              <button onClick={() => navigate(`/quran/${surahId - 1}`)} className="flex items-center gap-2 px-4 py-2.5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-all text-sm text-gray-700 dark:text-gray-300">
                <BackArrow className="w-4 h-4" />
                {getLabel('prev_surah', lang)}
              </button>
            ) : <div />}
            {surahId < 114 ? (
              <button onClick={() => navigate(`/quran/${surahId + 1}`)} className="flex items-center gap-2 px-4 py-2.5 bg-emerald-600 text-white rounded-xl shadow-sm hover:shadow-md hover:bg-emerald-700 transition-all text-sm">
                {getLabel('next_surah', lang)}
                <NextArrow className="w-4 h-4" />
              </button>
            ) : <div />}
          </div>
        )}
      </div>
    </div>
  );
}
