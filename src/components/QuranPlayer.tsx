import { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import {
  Play, Pause, SkipForward, SkipBack, Repeat, Repeat1,
  X, ChevronDown, Search, Volume2, Moon
} from 'lucide-react';
import { Input } from '@/components/ui/input';

interface Surah {
  number: number;
  name: string;
  englishName: string;
  numberOfAyahs: number;
}

// Reciters using mp3quran.net CDN (reliable full-surah audio)
// Format: https://server{X}.mp3quran.net/{folder}/{surah_number_padded}.mp3
const RECITERS = [
  { id: 'alafasy', name: 'مشاري العفاسي', server: 'https://server8.mp3quran.net/afs' },
  { id: 'sudais', name: 'عبد الرحمن السديس', server: 'https://server11.mp3quran.net/sds' },
  { id: 'shuraym', name: 'سعود الشريم', server: 'https://server7.mp3quran.net/shur' },
  { id: 'abdulbasit', name: 'عبد الباسط عبد الصمد', server: 'https://server7.mp3quran.net/basit/Almusshaf-Al-Mojawwad' },
  { id: 'husary', name: 'محمود خليل الحصري', server: 'https://server13.mp3quran.net/husr' },
  { id: 'minshawi', name: 'محمد صديق المنشاوي', server: 'https://server10.mp3quran.net/minsh' },
  { id: 'ajamy', name: 'أحمد بن علي العجمي', server: 'https://server10.mp3quran.net/ajm' },
  { id: 'maher', name: 'ماهر المعيقلي', server: 'https://server12.mp3quran.net/maher' },
  { id: 'hani', name: 'هاني الرفاعي', server: 'https://server9.mp3quran.net/hani' },
  { id: 'ayyoub', name: 'محمد أيوب', server: 'https://server8.mp3quran.net/ayyub' },
  { id: 'shaatri', name: 'أبو بكر الشاطري', server: 'https://server11.mp3quran.net/shatri' },
  { id: 'hudhaify', name: 'علي بن عبدالرحمن الحذيفي', server: 'https://server11.mp3quran.net/hthfi' },
  { id: 'tablawi', name: 'محمد الطبلاوي', server: 'https://server8.mp3quran.net/tblawi' },
  { id: 'yasser', name: 'ياسر الدوسري', server: 'https://server11.mp3quran.net/yasser' },
  { id: 'nasser', name: 'ناصر القطامي', server: 'https://server6.mp3quran.net/qtm' },
  { id: 'banna', name: 'محمود علي البنا', server: 'https://server8.mp3quran.net/bna' },
  { id: 'fares', name: 'فارس عباد', server: 'https://server8.mp3quran.net/frs_a' },
  { id: 'ghamdi', name: 'سعد الغامدي', server: 'https://server7.mp3quran.net/s_gmd' },
  { id: 'bukhatir', name: 'أحمد بن خاطر', server: 'https://server13.mp3quran.net/bukhtr' },
  { id: 'juhany', name: 'عبدالله الجهني', server: 'https://server11.mp3quran.net/a_jhn' },
];

type RepeatMode = 'none' | 'one' | 'all';

// Strip Arabic diacritics for search
const stripTashkeel = (str: string) =>
  str.replace(/[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED\u0890\u0891\u08D3-\u08FF\u0640]/g, '')
     .replace(/[ٱإأآ]/g, 'ا')
     .replace(/ة/g, 'ه')
     .replace(/ى/g, 'ي')
     .trim();

export default function QuranPlayer() {
  const [isOpen, setIsOpen] = useState(false);
  const [surahs, setSurahs] = useState<Surah[]>([]);
  const [search, setSearch] = useState('');
  const [selectedSurah, setSelectedSurah] = useState<number | null>(null);
  const [reciter, setReciter] = useState(() => localStorage.getItem('quran-reciter') || RECITERS[0].id);
  const [isPlaying, setIsPlaying] = useState(false);
  const [repeatMode, setRepeatMode] = useState<RepeatMode>('none');
  const [loading, setLoading] = useState(false);
  const [showSurahList, setShowSurahList] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const progressInterval = useRef<ReturnType<typeof setInterval>>();

  // Load surahs list
  useEffect(() => {
    fetch('https://api.alquran.cloud/v1/surah')
      .then(r => r.json())
      .then(d => setSurahs(d.data || []))
      .catch(() => {});
  }, []);

  const normalizedSearch = stripTashkeel(search);
  const filteredSurahs = surahs.filter(s => {
    if (!search) return true;
    return stripTashkeel(s.name).includes(normalizedSearch) ||
      s.englishName.toLowerCase().includes(search.toLowerCase()) ||
      String(s.number) === search.trim();
  });

  const getReciter = (id: string) => RECITERS.find(r => r.id === id) || RECITERS[0];

  const getAudioUrl = (surahNum: number, reciterId: string) => {
    const rec = getReciter(reciterId);
    const padded = String(surahNum).padStart(3, '0');
    return `${rec.server}/${padded}.mp3`;
  };

  const playSurah = useCallback((surahNum: number, reciterId?: string) => {
    const rid = reciterId || reciter;
    setSelectedSurah(surahNum);
    setLoading(true);
    setShowSurahList(false);

    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.src = '';
    }

    const audio = new Audio(getAudioUrl(surahNum, rid));
    audioRef.current = audio;

    audio.addEventListener('loadedmetadata', () => {
      setDuration(audio.duration);
      setLoading(false);
    });

    audio.addEventListener('canplay', () => {
      audio.play();
      setIsPlaying(true);
      setLoading(false);
    }, { once: true });

    audio.addEventListener('error', () => {
      setLoading(false);
      setIsPlaying(false);
    });

    // Progress tracking
    if (progressInterval.current) clearInterval(progressInterval.current);
    progressInterval.current = setInterval(() => {
      if (audio && !audio.paused) {
        setCurrentTime(audio.currentTime);
        setProgress(audio.duration ? (audio.currentTime / audio.duration) * 100 : 0);
      }
    }, 500);
  }, [reciter]);

  // Handle ended event
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleEnded = () => {
      if (repeatMode === 'one' && selectedSurah) {
        playSurah(selectedSurah);
      } else if (repeatMode === 'all' && selectedSurah) {
        const nextSurah = selectedSurah >= 114 ? 1 : selectedSurah + 1;
        playSurah(nextSurah);
      } else if (repeatMode === 'none' && selectedSurah) {
        if (selectedSurah < 114) {
          playSurah(selectedSurah + 1);
        } else {
          setIsPlaying(false);
        }
      }
    };

    audio.addEventListener('ended', handleEnded);
    return () => audio.removeEventListener('ended', handleEnded);
  }, [repeatMode, selectedSurah, playSurah]);

  // Auto-switch when reciter changes while a surah is playing
  const handleReciterChange = (newReciterId: string) => {
    setReciter(newReciterId);
    localStorage.setItem('quran-reciter', newReciterId);
    if (selectedSurah) {
      playSurah(selectedSurah, newReciterId);
    }
  };

  const togglePlay = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play();
      setIsPlaying(true);
    }
  };

  const nextSurah = () => {
    if (!selectedSurah) return;
    playSurah(selectedSurah >= 114 ? 1 : selectedSurah + 1);
  };

  const prevSurah = () => {
    if (!selectedSurah) return;
    playSurah(selectedSurah <= 1 ? 114 : selectedSurah - 1);
  };

  const cycleRepeat = () => {
    setRepeatMode(prev =>
      prev === 'none' ? 'all' : prev === 'all' ? 'one' : 'none'
    );
  };

  const seekTo = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!audioRef.current || !duration) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const pct = 1 - (e.clientX - rect.left) / rect.width;
    audioRef.current.currentTime = pct * duration;
  };

  const closePlayer = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.src = '';
      audioRef.current = null;
    }
    if (progressInterval.current) clearInterval(progressInterval.current);
    setIsOpen(false);
    setIsPlaying(false);
    setSelectedSurah(null);
    setProgress(0);
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  const currentSurah = surahs.find(s => s.number === selectedSurah);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (audioRef.current) { audioRef.current.pause(); audioRef.current.src = ''; }
      if (progressInterval.current) clearInterval(progressInterval.current);
    };
  }, []);

  return (
    <>
      {/* Entry card on home */}
      {!isOpen && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.38 }}
          className="px-4 mb-4"
        >
          <button
            onClick={() => setIsOpen(true)}
            className="w-full rounded-3xl bg-card border border-border/50 p-5 text-right shadow-elevated"
          >
            <div className="flex items-center justify-between mb-2">
              <Moon className="h-5 w-5 text-primary" />
              <span className="inline-block rounded-full bg-primary/10 border border-primary/20 px-3 py-1 text-xs font-medium text-primary">
                🎧 استمع وأنت نائم
              </span>
            </div>
            <p className="text-sm font-bold text-foreground mb-1">مشغّل القرآن الكريم</p>
            <p className="text-xs text-muted-foreground">
              شغّل أي سورة مع تكرار أو تشغيل تلقائي — {RECITERS.length} قارئ
            </p>
          </button>
        </motion.div>
      )}

      {/* Player panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="px-4 mb-4"
          >
            <div className="rounded-3xl bg-card border border-border/50 overflow-hidden shadow-elevated">
              {/* Header */}
              <div className="gradient-islamic p-4 flex items-center justify-between relative overflow-hidden">
                <div className="absolute inset-0 islamic-pattern opacity-20" />
                <button onClick={closePlayer} className="p-1.5 rounded-full bg-white/10 relative z-10">
                  <X className="h-4 w-4 text-white" />
                </button>
                <div className="text-right relative z-10">
                  <h3 className="text-sm font-bold text-white">🎧 مشغّل القرآن</h3>
                  {currentSurah && (
                    <p className="text-white/70 text-xs mt-0.5">
                      {currentSurah.number}. {currentSurah.name}
                    </p>
                  )}
                </div>
              </div>

              {/* Reciter selector */}
              <div className="p-4 border-b border-border/50">
                <label className="text-[10px] text-muted-foreground mb-1.5 block text-right">القارئ ({RECITERS.length} قارئ)</label>
                <select
                  value={reciter}
                  onChange={e => handleReciterChange(e.target.value)}
                  className="w-full rounded-2xl bg-muted border-0 p-2.5 text-sm text-foreground text-right"
                  dir="rtl"
                >
                  {RECITERS.map(r => (
                    <option key={r.id} value={r.id}>{r.name}</option>
                  ))}
                </select>
              </div>

              {/* Surah selector */}
              <div className="p-4 border-b border-border/50">
                <button
                  onClick={() => setShowSurahList(!showSurahList)}
                  className="w-full flex items-center justify-between rounded-2xl bg-muted p-3"
                >
                  <ChevronDown className={cn("h-4 w-4 text-muted-foreground transition-transform", showSurahList && "rotate-180")} />
                  <span className="text-sm font-medium text-foreground">
                    {currentSurah ? `${currentSurah.number}. ${currentSurah.name}` : 'اختر سورة'}
                  </span>
                </button>

                <AnimatePresence>
                  {showSurahList && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden"
                    >
                      <div className="pt-3">
                        <div className="relative mb-2">
                          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
                          <Input
                            value={search}
                            onChange={e => setSearch(e.target.value)}
                            placeholder="ابحث عن سورة..."
                            className="pl-8 rounded-2xl text-right text-xs h-9 border-border/50"
                          />
                        </div>
                        <div className="max-h-48 overflow-y-auto space-y-0.5">
                          {filteredSurahs.map(s => (
                            <button
                              key={s.number}
                              onClick={() => playSurah(s.number)}
                              className={cn(
                                "w-full flex items-center justify-between p-2.5 rounded-xl text-right transition-colors",
                                selectedSurah === s.number
                                  ? "bg-primary/10 text-primary"
                                  : "hover:bg-muted"
                              )}
                            >
                              <span className="text-[10px] text-muted-foreground">{s.numberOfAyahs} آية</span>
                              <div className="flex items-center gap-2">
                                <span className="text-xs font-medium text-foreground">{s.name}</span>
                                <span className="text-[10px] text-muted-foreground w-6 text-center">{s.number}</span>
                              </div>
                            </button>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Player controls */}
              {selectedSurah && (
                <div className="p-4">
                  {/* Progress bar */}
                  <div
                    className="w-full h-1.5 rounded-full bg-muted mb-2 cursor-pointer"
                    onClick={seekTo}
                  >
                    <div
                      className="h-full rounded-full bg-primary transition-all duration-300"
                      style={{ width: `${progress}%`, marginRight: 'auto', marginLeft: 0 }}
                    />
                  </div>
                  <div className="flex justify-between text-[10px] text-muted-foreground mb-4 tabular-nums" dir="ltr">
                    <span>{formatTime(currentTime)}</span>
                    <span>{formatTime(duration)}</span>
                  </div>

                  {/* Controls */}
                  <div className="flex items-center justify-center gap-5">
                    <button onClick={cycleRepeat} className="p-2">
                      {repeatMode === 'one' ? (
                        <Repeat1 className="h-5 w-5 text-primary" />
                      ) : (
                        <Repeat className={cn("h-5 w-5", repeatMode === 'all' ? "text-primary" : "text-muted-foreground")} />
                      )}
                    </button>

                    <button onClick={nextSurah} className="p-2">
                      <SkipForward className="h-5 w-5 text-foreground" />
                    </button>

                    <button
                      onClick={selectedSurah && !isPlaying && !audioRef.current ? () => playSurah(selectedSurah) : togglePlay}
                      disabled={loading}
                      className="h-14 w-14 rounded-full bg-primary flex items-center justify-center shadow-lg shadow-primary/20"
                    >
                      {loading ? (
                        <div className="h-5 w-5 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                      ) : isPlaying ? (
                        <Pause className="h-6 w-6 text-primary-foreground" />
                      ) : (
                        <Play className="h-6 w-6 text-primary-foreground mr-[-2px]" />
                      )}
                    </button>

                    <button onClick={prevSurah} className="p-2">
                      <SkipBack className="h-5 w-5 text-foreground" />
                    </button>

                    <div className="p-2">
                      <Volume2 className="h-5 w-5 text-muted-foreground" />
                    </div>
                  </div>

                  <p className="text-center text-[10px] text-muted-foreground mt-3">
                    {repeatMode === 'one' && '🔂 تكرار السورة الحالية'}
                    {repeatMode === 'all' && '🔁 تشغيل جميع السور تلقائياً'}
                    {repeatMode === 'none' && '➡️ الانتقال للسورة التالية تلقائياً'}
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
