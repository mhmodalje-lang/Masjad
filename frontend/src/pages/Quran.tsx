import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLocale } from '@/hooks/useLocale';
import { Book, Search, Star, BookOpen, ChevronLeft, ChevronRight, Loader2 } from 'lucide-react';
import { AdBanner } from '@/components/AdBanner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

// Surah type categories for filtering
const SURAH_TYPES = { all: '', meccan: 'Makkah', medinan: 'Madinah' };

// Multilingual labels for surah types
const TYPE_LABELS: Record<string, Record<string, string>> = {
  all: { ar: 'الكل', en: 'All', de: 'Alle', fr: 'Toutes', tr: 'Tümü', ru: 'Все', sv: 'Alla', nl: 'Alle', el: 'Όλα' },
  meccan: { ar: 'مكية', en: 'Meccan', de: 'Mekkanisch', fr: 'Mecquoise', tr: 'Mekkî', ru: 'Мекканские', sv: 'Meckanska', nl: 'Mekkaans', el: 'Μεκκανά' },
  medinan: { ar: 'مدنية', en: 'Medinan', de: 'Medinensisch', fr: 'Médinoise', tr: 'Medenî', ru: 'Мединские', sv: 'Medinska', nl: 'Medinaans', el: 'Μεδινά' },
};

const SEARCH_PLACEHOLDER: Record<string, string> = {
  ar: 'ابحث عن سورة...', en: 'Search for a surah...', de: 'Suche nach einer Sure...', fr: 'Rechercher une sourate...',
  tr: 'Sûre ara...', ru: 'Поиск суры...', sv: 'Sök efter en sura...', nl: 'Zoek een soera...', el: 'Αναζήτηση σούρας...',
};

const QURAN_TITLE: Record<string, string> = {
  ar: 'القرآن الكريم', en: 'The Noble Quran', de: 'Der Edle Koran', fr: 'Le Noble Coran',
  tr: "Kur'ân-ı Kerîm", ru: 'Благородный Коран', sv: 'Den Ädla Koranen', nl: 'De Edele Koran', el: 'Το Ευγενές Κοράνι',
};

const VERSES_LABEL: Record<string, string> = {
  ar: 'آيات', en: 'verses', de: 'Verse', fr: 'versets',
  tr: 'ayet', ru: 'аятов', sv: 'verser', nl: 'verzen', el: 'εδάφια',
};

interface Chapter {
  id: number;
  name_arabic: string;
  name_simple: string;
  translated_name?: { name: string };
  revelation_place: string;
  verses_count: number;
}

export default function Quran() {
  const navigate = useNavigate();
  const { t, locale, isRTL } = useLocale();
  const lang = useMemo(() => locale?.split('-')[0] || 'ar', [locale]);

  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');
  const [favorites, setFavorites] = useState<number[]>([]);
  const [showFavorites, setShowFavorites] = useState(false);

  // Load chapters
  useEffect(() => {
    setLoading(true);
    fetch(`${BACKEND_URL}/api/quran/v4/chapters?language=${lang}`)
      .then(r => r.json())
      .then(data => {
        setChapters(data.chapters || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [lang]);

  // Load favorites from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem('quran_favorite_surahs');
      if (saved) setFavorites(JSON.parse(saved));
    } catch { /* ignore */ }
  }, []);

  const toggleFavorite = useCallback((id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    setFavorites(prev => {
      const next = prev.includes(id) ? prev.filter(f => f !== id) : [...prev, id];
      localStorage.setItem('quran_favorite_surahs', JSON.stringify(next));
      return next;
    });
  }, []);

  // Filter chapters
  const filtered = useMemo(() => {
    let list = chapters;
    if (showFavorites) {
      list = list.filter(c => favorites.includes(c.id));
    }
    if (activeFilter !== 'all') {
      const typeValue = SURAH_TYPES[activeFilter as keyof typeof SURAH_TYPES];
      list = list.filter(c => c.revelation_place === typeValue);
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      list = list.filter(c =>
        c.name_arabic.includes(q) ||
        c.name_simple.toLowerCase().includes(q) ||
        (c.translated_name?.name || '').toLowerCase().includes(q) ||
        String(c.id) === q
      );
    }
    return list;
  }, [chapters, searchQuery, activeFilter, showFavorites, favorites]);

  const openSurah = useCallback((id: number) => {
    navigate(`/quran/${id}`);
  }, [navigate]);

  const ArrowIcon = isRTL ? ChevronLeft : ChevronRight;

  return (
    <div className={`min-h-screen bg-gradient-to-b from-emerald-50 via-white to-teal-50 dark:from-gray-900 dark:via-gray-950 dark:to-gray-900 ${isRTL ? 'rtl' : 'ltr'}`} dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-700 dark:from-emerald-800 dark:to-teal-900 px-4 py-8 text-center">
        <div className="flex items-center justify-center gap-3 mb-3">
          <BookOpen className="w-8 h-8 text-white/90" />
          <h1 className="text-3xl font-bold text-white">{QURAN_TITLE[lang] || QURAN_TITLE.ar}</h1>
        </div>
        <p className="text-emerald-100 text-sm">114 {t('surahCount')}</p>
      </div>

      <div className="max-w-2xl mx-auto px-4 -mt-6">
        {/* Search */}
        <div className="relative mb-4">
          <Search className={`absolute top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 ${isRTL ? 'right-4' : 'left-4'}`} />
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder={SEARCH_PLACEHOLDER[lang] || SEARCH_PLACEHOLDER.ar}
            className={`w-full ${isRTL ? 'pr-12 pl-4' : 'pl-12 pr-4'} py-3.5 rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-lg text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all`}
          />
        </div>

        {/* Filters */}
        <div className="flex items-center gap-2 mb-6 overflow-x-auto pb-2 scrollbar-hide">
          <button
            onClick={() => setShowFavorites(!showFavorites)}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${showFavorites ? 'bg-amber-500 text-white shadow-md' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700'}`}
          >
            <Star className="w-4 h-4" fill={showFavorites ? 'currentColor' : 'none'} />
            {t('favorites')}
          </button>
          {Object.keys(SURAH_TYPES).map(key => (
            <button
              key={key}
              onClick={() => setActiveFilter(key)}
              className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${activeFilter === key ? 'bg-emerald-600 text-white shadow-md' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700'}`}
            >
              {TYPE_LABELS[key]?.[lang] || TYPE_LABELS[key]?.en || key}
            </button>
          ))}
        </div>

        {/* Loading */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
          </div>
        ) : (
          /* Surah List */
          <div className="space-y-2 pb-24">
            {filtered.length === 0 ? (
              <div className="text-center py-16 text-gray-400">
                <Book className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>{t('noResults')}</p>
              </div>
            ) : (
              filtered.map(chapter => (
                <button
                  key={chapter.id}
                  onClick={() => openSurah(chapter.id)}
                  className="w-full flex items-center gap-3 p-4 bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700/50 shadow-sm hover:shadow-md hover:border-emerald-200 dark:hover:border-emerald-700 transition-all group"
                >
                  {/* Number */}
                  <div className="w-11 h-11 flex-shrink-0 flex items-center justify-center bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 rounded-xl font-bold text-sm">
                    {chapter.id}
                  </div>

                  {/* Info */}
                  <div className={`flex-1 min-w-0 ${isRTL ? 'text-right' : 'text-left'}`}>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-gray-900 dark:text-white text-base">{chapter.name_arabic}</span>
                      {lang !== 'ar' && (
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                          {chapter.translated_name?.name || chapter.name_simple}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-2 text-xs text-gray-400 mt-0.5">
                      <span>{chapter.revelation_place === 'Makkah' ? (TYPE_LABELS.meccan[lang] || 'Meccan') : (TYPE_LABELS.medinan[lang] || 'Medinan')}</span>
                      <span>•</span>
                      <span>{chapter.verses_count} {VERSES_LABEL[lang] || 'verses'}</span>
                    </div>
                  </div>

                  {/* Favorite + Arrow */}
                  <button
                    onClick={(e) => toggleFavorite(chapter.id, e)}
                    className="p-2 rounded-xl hover:bg-amber-50 dark:hover:bg-amber-900/20 transition-colors"
                  >
                    <Star className={`w-5 h-5 ${favorites.includes(chapter.id) ? 'text-amber-500 fill-amber-500' : 'text-gray-300 dark:text-gray-600'}`} />
                  </button>
                  <ArrowIcon className={`w-5 h-5 text-gray-300 dark:text-gray-600 group-hover:text-emerald-500 transition-colors`} />
                </button>
              ))
            )}
          </div>
        )}
      </div>
      <AdBanner position="quran" />
    </div>
  );
}
