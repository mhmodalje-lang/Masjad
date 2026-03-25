import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useLocale } from '@/hooks/useLocale';
import { ArrowLeft, ArrowRight, Play, Pause, Volume2, BookOpen, ChevronDown, ChevronUp, Loader2, BookMarked } from 'lucide-react';

const BACKEND = import.meta.env.REACT_APP_BACKEND_URL || '';

const L: Record<string, Record<string, string>> = {
  tafsir: { ar: 'التفسير', en: 'Tafsir', de: 'Tafsir', fr: 'Tafsir', tr: 'Tefsir', ru: 'Тафсир', sv: 'Tafsir', nl: 'Tafsir', el: 'Τάφσιρ' },
  verse: { ar: 'آية', en: 'Verse', de: 'Vers', fr: 'Verset', tr: 'Ayet', ru: 'Аят', sv: 'Vers', nl: 'Vers', el: 'Εδάφιο' },
  loading: { ar: 'جاري التحميل...', en: 'Loading...', de: 'Laden...', fr: 'Chargement...', tr: 'Yükleniyor...', ru: 'Загрузка...', sv: 'Laddar...', nl: 'Laden...', el: 'Φόρτωση...' },
  show_tafsir: { ar: 'التفسير', en: 'Tafsir', de: 'Tafsir', fr: 'Tafsir', tr: 'Tefsir', ru: 'Тафсир', sv: 'Tafsir', nl: 'Tafsir', el: 'Τάφσιρ' },
  source: { ar: 'المصدر', en: 'Source', de: 'Quelle', fr: 'Source', tr: 'Kaynak', ru: 'Источник', sv: 'Källa', nl: 'Bron', el: 'Πηγή' },
  next: { ar: 'التالية', en: 'Next', de: 'Nächste', fr: 'Suivante', tr: 'Sonraki', ru: 'Далее', sv: 'Nästa', nl: 'Volgende', el: 'Επόμενη' },
  prev: { ar: 'السابقة', en: 'Previous', de: 'Vorherige', fr: 'Précédente', tr: 'Önceki', ru: 'Назад', sv: 'Föregående', nl: 'Vorige', el: 'Προηγούμενη' },
  listen: { ar: 'استمع', en: 'Listen', de: 'Anhören', fr: 'Écouter', tr: 'Dinle', ru: 'Слушать', sv: 'Lyssna', nl: 'Luisteren', el: 'Ακούστε' },
};
const l = (k: string, lang: string) => L[k]?.[lang] || L[k]?.en || k;

interface Verse { verse_key: string; verse_number: number; text: string; audio_url: string; }
interface Tafsir { tafsir: string; tafsir_source: string; }

export default function SurahView() {
  const { id } = useParams<{ id: string }>();
  const sid = parseInt(id || '1');
  const nav = useNavigate();
  const { locale, isRTL } = useLocale();
  const lang = useMemo(() => locale?.split('-')[0] || 'ar', [locale]);

  const [info, setInfo] = useState<any>(null);
  const [verses, setVerses] = useState<Verse[]>([]);
  const [loading, setLoading] = useState(true);
  const [playing, setPlaying] = useState<number | null>(null);
  const [tafsirs, setTafsirs] = useState<Record<number, Tafsir | null>>({});
  const [tLoading, setTLoading] = useState<Record<number, boolean>>({});
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    fetch(`${BACKEND}/api/quran/v4/chapters/${sid}?language=${lang}`)
      .then(r => r.json())
      .then(d => setInfo(d.chapter || null))
      .catch(() => {});
  }, [sid, lang]);

  useEffect(() => {
    setLoading(true); setVerses([]); setTafsirs({});
    const cnt = info?.verses_count || 7;
    fetch(`${BACKEND}/api/quran/v4/global-verse/bulk/${sid}?language=${lang}&from_ayah=1&to_ayah=${cnt}`)
      .then(r => r.json())
      .then(d => { setVerses(d.verses || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [sid, lang, info?.verses_count]);

  const playAudio = useCallback((v: Verse) => {
    if (audioRef.current) audioRef.current.pause();
    if (playing === v.verse_number) { setPlaying(null); return; }
    const a = new Audio(v.audio_url);
    audioRef.current = a;
    a.play().catch(() => {});
    setPlaying(v.verse_number);
    a.onended = () => setPlaying(null);
  }, [playing]);

  const toggleTafsir = useCallback(async (vn: number) => {
    if (tafsirs[vn] !== undefined) {
      setTafsirs(p => { const n = { ...p }; delete n[vn]; return n; });
      return;
    }
    setTLoading(p => ({ ...p, [vn]: true }));
    try {
      const r = await fetch(`${BACKEND}/api/quran/v4/global-verse/${sid}/${vn}?language=${lang}`);
      const d = await r.json();
      setTafsirs(p => ({ ...p, [vn]: { tafsir: d.tafsir || '', tafsir_source: d.tafsir_source || '' } }));
    } catch {
      setTafsirs(p => ({ ...p, [vn]: { tafsir: '', tafsir_source: '' } }));
    }
    setTLoading(p => ({ ...p, [vn]: false }));
  }, [tafsirs, sid, lang]);

  const Back = isRTL ? ArrowRight : ArrowLeft;
  const Next = isRTL ? ArrowLeft : ArrowRight;
  const isAr = lang === 'ar';
  const surahName = isAr ? (info?.name_arabic || '') : (info?.translated_name?.name || info?.name_simple || '');

  return (
    <div className={`min-h-screen bg-gradient-to-b from-emerald-50 via-white to-teal-50 dark:from-gray-900 dark:via-gray-950 dark:to-gray-900`} dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-700 dark:from-emerald-800 dark:to-teal-900 px-4 py-6">
        <div className="max-w-2xl mx-auto">
          <button onClick={() => nav('/quran')} className="flex items-center gap-2 text-white/80 hover:text-white mb-3">
            <Back className="w-5 h-5" />
          </button>
          {info && (
            <div className="text-center">
              <h1 className="text-3xl font-bold text-white mb-1">{surahName}</h1>
              <p className="text-emerald-200/70 text-sm mt-1">
                {info.verses_count} {l('verse', lang)} • {sid}
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-4 py-6">
        {loading ? (
          <div className="flex flex-col items-center py-20 gap-3">
            <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
            <span className="text-gray-400 text-sm">{l('loading', lang)}</span>
          </div>
        ) : (
          <div className="space-y-3 pb-8">
            {verses.map(v => {
              const tf = tafsirs[v.verse_number];
              const isOpen = tf !== undefined;
              const isLoadingTf = tLoading[v.verse_number];

              return (
                <div key={v.verse_key} className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700/50 shadow-sm overflow-hidden">
                  {/* Header bar */}
                  <div className="flex items-center justify-between px-4 py-2 bg-emerald-50/50 dark:bg-emerald-900/10 border-b border-emerald-100/50 dark:border-emerald-800/20">
                    <span className="w-8 h-8 flex items-center justify-center bg-emerald-600 text-white rounded-lg text-sm font-bold">
                      {v.verse_number}
                    </span>
                    <div className="flex items-center gap-1">
                      <button onClick={() => playAudio(v)}
                        className={`p-2 rounded-xl transition-all ${playing === v.verse_number ? 'bg-emerald-600 text-white' : 'hover:bg-emerald-100 dark:hover:bg-emerald-900/20 text-emerald-600'}`}>
                        {playing === v.verse_number ? <Pause className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                      </button>
                      <button onClick={() => toggleTafsir(v.verse_number)}
                        className={`flex items-center gap-1 px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${isOpen ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700' : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500'}`}>
                        <BookMarked className="w-3.5 h-3.5" />
                        <span>{l('show_tafsir', lang)}</span>
                        {isOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                      </button>
                    </div>
                  </div>

                  {/* Verse text — ONLY in user's language */}
                  <div className={`px-5 py-5 ${isRTL ? 'text-right' : 'text-left'}`}>
                    <p className={`leading-relaxed text-gray-900 dark:text-white ${isAr ? 'text-2xl' : 'text-[16px]'}`}
                       style={isAr ? { fontFamily: "'Amiri', 'Traditional Arabic', serif", lineHeight: '2.2' } : { lineHeight: '1.9' }}>
                      {v.text}
                      {isAr && <span className="inline-block text-emerald-600 dark:text-emerald-400 text-lg mx-1">﴿{v.verse_number}﴾</span>}
                    </p>
                  </div>

                  {/* Tafsir — ONLY in user's language */}
                  {isLoadingTf && (
                    <div className="px-5 pb-4 flex items-center gap-2 text-gray-400">
                      <Loader2 className="w-4 h-4 animate-spin" /><span className="text-sm">{l('loading', lang)}</span>
                    </div>
                  )}
                  {isOpen && tf?.tafsir && (
                    <div className={`px-5 pb-4 border-t border-amber-100 dark:border-amber-800/20 pt-3 bg-amber-50/30 dark:bg-amber-900/5 ${isRTL ? 'text-right' : 'text-left'}`}>
                      <div className="flex items-center gap-2 mb-2">
                        <BookOpen className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                        <span className="text-xs font-medium text-amber-600 dark:text-amber-400">{l('tafsir', lang)}</span>
                      </div>
                      <p className="text-[14px] leading-relaxed text-gray-700 dark:text-gray-300">{tf.tafsir}</p>
                      {tf.tafsir_source && (
                        <p className="mt-2 text-[11px] text-gray-400 italic">{l('source', lang)}: {tf.tafsir_source}</p>
                      )}
                    </div>
                  )}
                  {isOpen && !tf?.tafsir && !isLoadingTf && (
                    <div className="px-5 pb-4 text-sm text-gray-400 italic">
                      {lang === 'ar' ? 'لا يوجد تفسير' : lang === 'tr' ? 'Tefsir mevcut değil' : lang === 'fr' ? 'Tafsir non disponible' : 'Tafsir not available'}
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
            {sid > 1 ? (
              <button onClick={() => nav(`/quran/${sid - 1}`)} className="flex items-center gap-2 px-4 py-2.5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md text-sm text-gray-700 dark:text-gray-300">
                <Back className="w-4 h-4" />{l('prev', lang)}
              </button>
            ) : <div />}
            {sid < 114 ? (
              <button onClick={() => nav(`/quran/${sid + 1}`)} className="flex items-center gap-2 px-4 py-2.5 bg-emerald-600 text-white rounded-xl shadow-sm hover:bg-emerald-700 text-sm">
                {l('next', lang)}<Next className="w-4 h-4" />
              </button>
            ) : <div />}
          </div>
        )}
      </div>
    </div>
  );
}
