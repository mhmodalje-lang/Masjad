import React, { useState, useCallback } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { ChevronLeft, ChevronRight, BookOpen, Search, Star } from 'lucide-react';
import { cn } from '@/lib/utils';
import GlobalQuranVerse from '@/components/GlobalQuranVerse';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

// Surah list - all 114 surahs
const SURAHS = [
  {n:1,ar:"الفاتحة",en:"Al-Fatiha",v:7},{n:2,ar:"البقرة",en:"Al-Baqara",v:286},{n:3,ar:"آل عمران",en:"Ali 'Imran",v:200},
  {n:4,ar:"النساء",en:"An-Nisa",v:176},{n:5,ar:"المائدة",en:"Al-Ma'ida",v:120},{n:6,ar:"الأنعام",en:"Al-An'am",v:165},
  {n:7,ar:"الأعراف",en:"Al-A'raf",v:206},{n:8,ar:"الأنفال",en:"Al-Anfal",v:75},{n:9,ar:"التوبة",en:"At-Tawba",v:129},
  {n:10,ar:"يونس",en:"Yunus",v:109},{n:11,ar:"هود",en:"Hud",v:123},{n:12,ar:"يوسف",en:"Yusuf",v:111},
  {n:13,ar:"الرعد",en:"Ar-Ra'd",v:43},{n:14,ar:"إبراهيم",en:"Ibrahim",v:52},{n:15,ar:"الحجر",en:"Al-Hijr",v:99},
  {n:16,ar:"النحل",en:"An-Nahl",v:128},{n:17,ar:"الإسراء",en:"Al-Isra",v:111},{n:18,ar:"الكهف",en:"Al-Kahf",v:110},
  {n:19,ar:"مريم",en:"Maryam",v:98},{n:20,ar:"طه",en:"Ta-Ha",v:135},{n:21,ar:"الأنبياء",en:"Al-Anbiya",v:112},
  {n:22,ar:"الحج",en:"Al-Hajj",v:78},{n:23,ar:"المؤمنون",en:"Al-Mu'minun",v:118},{n:24,ar:"النور",en:"An-Nur",v:64},
  {n:25,ar:"الفرقان",en:"Al-Furqan",v:77},{n:26,ar:"الشعراء",en:"Ash-Shu'ara",v:227},{n:27,ar:"النمل",en:"An-Naml",v:93},
  {n:28,ar:"القصص",en:"Al-Qasas",v:88},{n:29,ar:"العنكبوت",en:"Al-Ankabut",v:69},{n:30,ar:"الروم",en:"Ar-Rum",v:60},
  {n:31,ar:"لقمان",en:"Luqman",v:34},{n:32,ar:"السجدة",en:"As-Sajda",v:30},{n:33,ar:"الأحزاب",en:"Al-Ahzab",v:73},
  {n:34,ar:"سبأ",en:"Saba",v:54},{n:35,ar:"فاطر",en:"Fatir",v:45},{n:36,ar:"يس",en:"Ya-Sin",v:83},
  {n:37,ar:"الصافات",en:"As-Saffat",v:182},{n:38,ar:"ص",en:"Sad",v:88},{n:39,ar:"الزمر",en:"Az-Zumar",v:75},
  {n:40,ar:"غافر",en:"Ghafir",v:85},{n:41,ar:"فصلت",en:"Fussilat",v:54},{n:42,ar:"الشورى",en:"Ash-Shura",v:53},
  {n:43,ar:"الزخرف",en:"Az-Zukhruf",v:89},{n:44,ar:"الدخان",en:"Ad-Dukhan",v:59},{n:45,ar:"الجاثية",en:"Al-Jathiya",v:37},
  {n:46,ar:"الأحقاف",en:"Al-Ahqaf",v:35},{n:47,ar:"محمد",en:"Muhammad",v:38},{n:48,ar:"الفتح",en:"Al-Fath",v:29},
  {n:49,ar:"الحجرات",en:"Al-Hujurat",v:18},{n:50,ar:"ق",en:"Qaf",v:45},{n:51,ar:"الذاريات",en:"Adh-Dhariyat",v:60},
  {n:52,ar:"الطور",en:"At-Tur",v:49},{n:53,ar:"النجم",en:"An-Najm",v:62},{n:54,ar:"القمر",en:"Al-Qamar",v:55},
  {n:55,ar:"الرحمن",en:"Ar-Rahman",v:78},{n:56,ar:"الواقعة",en:"Al-Waqi'a",v:96},{n:57,ar:"الحديد",en:"Al-Hadid",v:29},
  {n:58,ar:"المجادلة",en:"Al-Mujadila",v:22},{n:59,ar:"الحشر",en:"Al-Hashr",v:24},{n:60,ar:"الممتحنة",en:"Al-Mumtahina",v:13},
  {n:61,ar:"الصف",en:"As-Saff",v:14},{n:62,ar:"الجمعة",en:"Al-Jumu'a",v:11},{n:63,ar:"المنافقون",en:"Al-Munafiqun",v:11},
  {n:64,ar:"التغابن",en:"At-Taghabun",v:18},{n:65,ar:"الطلاق",en:"At-Talaq",v:12},{n:66,ar:"التحريم",en:"At-Tahrim",v:12},
  {n:67,ar:"الملك",en:"Al-Mulk",v:30},{n:68,ar:"القلم",en:"Al-Qalam",v:52},{n:69,ar:"الحاقة",en:"Al-Haqqa",v:52},
  {n:70,ar:"المعارج",en:"Al-Ma'arij",v:44},{n:71,ar:"نوح",en:"Nuh",v:28},{n:72,ar:"الجن",en:"Al-Jinn",v:28},
  {n:73,ar:"المزمل",en:"Al-Muzzammil",v:20},{n:74,ar:"المدثر",en:"Al-Muddaththir",v:56},{n:75,ar:"القيامة",en:"Al-Qiyama",v:40},
  {n:76,ar:"الإنسان",en:"Al-Insan",v:31},{n:77,ar:"المرسلات",en:"Al-Mursalat",v:50},{n:78,ar:"النبأ",en:"An-Naba",v:40},
  {n:79,ar:"النازعات",en:"An-Nazi'at",v:46},{n:80,ar:"عبس",en:"Abasa",v:42},{n:81,ar:"التكوير",en:"At-Takwir",v:29},
  {n:82,ar:"الانفطار",en:"Al-Infitar",v:19},{n:83,ar:"المطففين",en:"Al-Mutaffifin",v:36},{n:84,ar:"الانشقاق",en:"Al-Inshiqaq",v:25},
  {n:85,ar:"البروج",en:"Al-Buruj",v:22},{n:86,ar:"الطارق",en:"At-Tariq",v:17},{n:87,ar:"الأعلى",en:"Al-A'la",v:19},
  {n:88,ar:"الغاشية",en:"Al-Ghashiya",v:26},{n:89,ar:"الفجر",en:"Al-Fajr",v:30},{n:90,ar:"البلد",en:"Al-Balad",v:20},
  {n:91,ar:"الشمس",en:"Ash-Shams",v:15},{n:92,ar:"الليل",en:"Al-Layl",v:21},{n:93,ar:"الضحى",en:"Ad-Duha",v:11},
  {n:94,ar:"الشرح",en:"Ash-Sharh",v:8},{n:95,ar:"التين",en:"At-Tin",v:8},{n:96,ar:"العلق",en:"Al-Alaq",v:19},
  {n:97,ar:"القدر",en:"Al-Qadr",v:5},{n:98,ar:"البينة",en:"Al-Bayyina",v:8},{n:99,ar:"الزلزلة",en:"Az-Zalzala",v:8},
  {n:100,ar:"العاديات",en:"Al-Adiyat",v:11},{n:101,ar:"القارعة",en:"Al-Qari'a",v:11},{n:102,ar:"التكاثر",en:"At-Takathur",v:8},
  {n:103,ar:"العصر",en:"Al-Asr",v:3},{n:104,ar:"الهمزة",en:"Al-Humaza",v:9},{n:105,ar:"الفيل",en:"Al-Fil",v:5},
  {n:106,ar:"قريش",en:"Quraysh",v:4},{n:107,ar:"الماعون",en:"Al-Ma'un",v:7},{n:108,ar:"الكوثر",en:"Al-Kawthar",v:3},
  {n:109,ar:"الكافرون",en:"Al-Kafirun",v:6},{n:110,ar:"النصر",en:"An-Nasr",v:3},{n:111,ar:"المسد",en:"Al-Masad",v:5},
  {n:112,ar:"الإخلاص",en:"Al-Ikhlas",v:4},{n:113,ar:"الفلق",en:"Al-Falaq",v:5},{n:114,ar:"الناس",en:"An-Nas",v:6},
];

// V2026: All Quran verse fetching now goes through GlobalQuranVerse component
// which uses the unified /api/quran/v4/global-verse endpoint.

export default function Tafsir() {
  const { locale, dir, t } = useLocale();

  const [surahNum, setSurahNum] = useState(1);
  const [ayahNum, setAyahNum] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSurahList, setShowSurahList] = useState(true);
  const [favorites, setFavorites] = useState<string[]>(() => {
    try { return JSON.parse(localStorage.getItem('tafsir_favs') || '[]'); } catch { return []; }
  });

  const surah = SURAHS.find(s => s.n === surahNum);

  const prevAyah = () => {
    if (ayahNum > 1) setAyahNum(ayahNum - 1);
    else if (surahNum > 1) {
      const prev = SURAHS.find(s => s.n === surahNum - 1);
      if (prev) { setSurahNum(surahNum - 1); setAyahNum(prev.v); }
    }
  };

  const nextAyah = () => {
    if (surah && ayahNum < surah.v) setAyahNum(ayahNum + 1);
    else if (surahNum < 114) { setSurahNum(surahNum + 1); setAyahNum(1); }
  };

  const toggleFav = () => {
    const key = `${surahNum}:${ayahNum}`;
    const newFavs = favorites.includes(key) ? favorites.filter(f => f !== key) : [...favorites, key];
    setFavorites(newFavs);
    localStorage.setItem('tafsir_favs', JSON.stringify(newFavs));
  };

  const filteredSurahs = searchQuery
    ? SURAHS.filter(s => s.ar.includes(searchQuery) || s.en.toLowerCase().includes(searchQuery.toLowerCase()) || String(s.n).includes(searchQuery))
    : SURAHS;

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
          <div className="grid grid-cols-2 gap-2">
            {filteredSurahs.map(s => (
              <button key={s.n} onClick={() => { setSurahNum(s.n); setAyahNum(1); setShowSurahList(false); }}
                className="p-3 rounded-xl bg-card border border-border/20 hover:border-emerald-500/30 transition-all text-right flex items-center gap-2.5 active:scale-[0.98]">
                <span className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-xs font-bold shrink-0">{s.n}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-foreground truncate">{s.ar}</p>
                  <p className="text-[10px] text-muted-foreground truncate">{s.en} • {s.v} {t('tafsirVerses')}</p>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tafsir Reading — V2026: Uses GlobalQuranVerse */}
      {!showSurahList && (
        <div className="px-4 py-3 space-y-4">
          <div className="flex items-center justify-between gap-2">
            <button onClick={prevAyah} className="p-2.5 rounded-xl bg-card border border-border/20 hover:bg-muted/50 transition-all active:scale-95">
              <ChevronRight className="h-5 w-5 text-foreground" />
            </button>
            <div className="text-center flex-1">
              <p className="text-base font-bold text-foreground">{surah?.ar} ({surah?.en})</p>
              <p className="text-xs text-muted-foreground">{t('tafsirVerse')} {ayahNum} / {surah?.v}</p>
            </div>
            <button onClick={nextAyah} className="p-2.5 rounded-xl bg-card border border-border/20 hover:bg-muted/50 transition-all active:scale-95">
              <ChevronLeft className="h-5 w-5 text-foreground" />
            </button>
          </div>

          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
            {surah && Array.from({ length: Math.min(surah.v, 30) }, (_, i) => i + 1).map(num => (
              <button key={num} onClick={() => setAyahNum(num)}
                className={cn("w-9 h-9 rounded-lg text-xs font-bold shrink-0 transition-all",
                  num === ayahNum ? "bg-emerald-600 text-white shadow-lg" : "bg-card border border-border/20 text-foreground hover:bg-muted/50"
                )}>{num}</button>
            ))}
            {surah && surah.v > 30 && (
              <select value={ayahNum > 30 ? ayahNum : ''} onChange={e => setAyahNum(Number(e.target.value))}
                className="h-9 px-2 rounded-lg text-xs bg-card border border-border/20 text-foreground">
                <option value="" disabled>{t('tafsirMore')}</option>
                {Array.from({ length: surah.v - 30 }, (_, i) => i + 31).map(n => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
            )}
          </div>

          {/* Favorite toggle */}
          <div className="flex justify-end">
            <button onClick={toggleFav} className={cn("flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold transition-all",
              favorites.includes(`${surahNum}:${ayahNum}`)
                ? "bg-amber-500/10 text-amber-500 border border-amber-500/20"
                : "bg-muted/30 text-muted-foreground border border-border/20")}>
              <Star className="h-3 w-3" fill={favorites.includes(`${surahNum}:${ayahNum}`) ? 'currentColor' : 'none'} />
              {favorites.includes(`${surahNum}:${ayahNum}`) ? t('tafsirFavorited') || '★' : t('tafsirFavorite') || '☆'}
            </button>
          </div>

          {/* GlobalQuranVerse — replaces all old scattered fetching */}
          <GlobalQuranVerse
            key={`${surahNum}:${ayahNum}`}
            surahId={surahNum}
            ayahId={ayahNum}
            compact={false}
            showExplanation={true}
            showAudio={true}
            showSurahName={true}
          />
        </div>
      )}
    </div>
  );
}
