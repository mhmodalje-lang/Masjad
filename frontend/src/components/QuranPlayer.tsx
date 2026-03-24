import { useEffect, useMemo, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import {
  Play,
  Pause,
  SkipForward,
  SkipBack,
  Repeat,
  Repeat1,
  X,
  ChevronDown,
  Search,
  Volume2,
  Moon,
} from 'lucide-react';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';
import { normalizeArabicForSearch } from '@/lib/arabicNormalize';
import { useLocale } from '@/hooks/useLocale';

interface Surah {
  number: number;
  name: string;
  englishName: string;
  numberOfAyahs: number;
}

// Curated working servers (mp3quran) — must point to folders that contain 001.mp3 ... 114.mp3
const reciterKeyMap: Record<string, string> = {
  alafasy: 'reciterAlafasy', sudais: 'reciterSudais', shuraym: 'reciterShuraym',
  abdulbasit: 'reciterAbdulbasit', husary: 'reciterHusary', minshawi: 'reciterMinshawi',
  ajamy: 'reciterAjamy', maher: 'reciterMaher', hani: 'reciterBudair',
  ayyoub: 'reciterAyyoub', shaatri: 'reciterShatri', hudhaify: 'reciterAhmad',
  tablawi: 'reciterTablawi', yasser: 'reciterYasser', nasser: 'reciterNasser',
  banna: 'reciterBanna', fares: 'reciterFares', ghamdi: 'reciterGhamdi',
  bukhatir: 'reciterAkhdar', juhany: 'reciterBasitMurattal',
};

const RECITERS = [
  { id: 'alafasy', nameKey: 'reciterAlafasy', server: 'https://server8.mp3quran.net/afs/' },
  { id: 'sudais', nameKey: 'reciterSudais', server: 'https://server11.mp3quran.net/sds/' },
  { id: 'shuraym', nameKey: 'reciterShuraym', server: 'https://server7.mp3quran.net/shur/' },
  { id: 'abdulbasit', nameKey: 'reciterAbdulbasit', server: 'https://server7.mp3quran.net/basit/Almusshaf-Al-Mojawwad/' },
  { id: 'husary', nameKey: 'reciterHusary', server: 'https://server13.mp3quran.net/husr/' },
  { id: 'minshawi', nameKey: 'reciterMinshawi', server: 'https://server10.mp3quran.net/minsh/' },
  { id: 'ajamy', nameKey: 'reciterAjamy', server: 'https://server10.mp3quran.net/ajm/' },
  { id: 'maher', nameKey: 'reciterMaher', server: 'https://server12.mp3quran.net/maher/' },
  { id: 'hani', nameKey: 'reciterBudair', server: 'https://server6.mp3quran.net/s_bud/' },
  { id: 'ayyoub', nameKey: 'reciterAyyoub', server: 'https://server8.mp3quran.net/ayyub/' },
  { id: 'shaatri', nameKey: 'reciterShatri', server: 'https://server11.mp3quran.net/shatri/' },
  { id: 'hudhaify', nameKey: 'reciterAhmad', server: 'https://server11.mp3quran.net/a_jbr/' },
  { id: 'tablawi', nameKey: 'reciterTablawi', server: 'https://server12.mp3quran.net/tblawi/' },
  { id: 'yasser', nameKey: 'reciterYasser', server: 'https://server11.mp3quran.net/yasser/' },
  { id: 'nasser', nameKey: 'reciterNasser', server: 'https://server6.mp3quran.net/qtm/' },
  { id: 'banna', nameKey: 'reciterBanna', server: 'https://server8.mp3quran.net/bna/' },
  { id: 'fares', nameKey: 'reciterFares', server: 'https://server8.mp3quran.net/frs_a/' },
  { id: 'ghamdi', nameKey: 'reciterGhamdi', server: 'https://server7.mp3quran.net/s_gmd/' },
  { id: 'bukhatir', nameKey: 'reciterAkhdar', server: 'https://server6.mp3quran.net/akdr/' },
  { id: 'juhany', nameKey: 'reciterBasitMurattal', server: 'https://server7.mp3quran.net/basit/' },
] as const;

type ReciterId = (typeof RECITERS)[number]['id'];
type RepeatMode = 'none' | 'one' | 'all';

function getReciterById(id: string) {
  return RECITERS.find(r => r.id === id) || RECITERS[0];
}

function getSurahAudioUrl({ surahNumber, reciterId }: { surahNumber: number; reciterId: string }) {
  const rec = getReciterById(reciterId);
  const padded = String(surahNumber).padStart(3, '0');
  return `${rec.server}${padded}.mp3`;
}

export default function QuranPlayer() {
  const { t } = useLocale();
  const [isOpen, setIsOpen] = useState(false);
  const [surahs, setSurahs] = useState<Surah[]>([]);
  const [search, setSearch] = useState('');
  const [selectedSurah, setSelectedSurah] = useState<number | null>(null);
  const [reciter, setReciter] = useState<ReciterId>(() => {
    const saved = localStorage.getItem('quran-reciter');
    return (saved as ReciterId) || RECITERS[0].id;
  });
  const [isPlaying, setIsPlaying] = useState(false);
  const [repeatMode, setRepeatMode] = useState<RepeatMode>('none');
  const [loading, setLoading] = useState(false);
  const [showSurahList, setShowSurahList] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);

  // Stable audio element (do NOT replace the Audio object; just change src)
  const audioRef = useRef<HTMLAudioElement>(new Audio());

  // Keep latest state for event handlers
  const selectedSurahRef = useRef<number | null>(null);
  const repeatModeRef = useRef<RepeatMode>('none');
  const reciterRef = useRef<ReciterId>(reciter);

  useEffect(() => {
    selectedSurahRef.current = selectedSurah;
  }, [selectedSurah]);

  useEffect(() => {
    repeatModeRef.current = repeatMode;
  }, [repeatMode]);

  useEffect(() => {
    reciterRef.current = reciter;
  }, [reciter]);

  // Load surahs list from Quran.com API v4
  useEffect(() => {
    fetch('https://api.quran.com/api/v4/chapters?language=ar')
      .then(r => r.json())
      .then(d => {
        const chapters = d.chapters || [];
        setSurahs(chapters.map((ch: any) => ({
          number: ch.id,
          name: ch.name_arabic,
          englishName: ch.name_simple,
          numberOfAyahs: ch.verses_count,
        })));
      })
      .catch(() => {});
  }, []);

  // Attach audio listeners once
  useEffect(() => {
    const audio = audioRef.current;
    audio.preload = 'auto';

    const onLoadedMetadata = () => {
      setDuration(Number.isFinite(audio.duration) ? audio.duration : 0);
      setLoading(false);
    };

    const onTimeUpdate = () => {
      setCurrentTime(audio.currentTime || 0);
      setProgress(audio.duration ? (audio.currentTime / audio.duration) * 100 : 0);
    };

    const onEnded = () => {
      const current = selectedSurahRef.current;
      const mode = repeatModeRef.current;
      const rid = reciterRef.current;

      if (!current) {
        setIsPlaying(false);
        return;
      }

      if (mode === 'one') {
        void startSurah(current, rid, { autoplay: true, silentErrors: true });
        return;
      }

      if (mode === 'all') {
        const next = current >= 114 ? 1 : current + 1;
        void startSurah(next, rid, { autoplay: true, silentErrors: true });
        return;
      }

      // none: auto-next to help "sleep listening"
      if (current < 114) {
        void startSurah(current + 1, rid, { autoplay: true, silentErrors: true });
      } else {
        setIsPlaying(false);
      }
    };

    const onError = () => {
      // Only show error if we actually have a src set (avoid spurious errors on reset)
      if (audio.src && audio.src !== window.location.href) {
        setLoading(false);
        setIsPlaying(false);
        const currentReciter = getReciterById(reciterRef.current);
        toast.error(t("audioErrorReciter"));
      }
    };

    audio.addEventListener('loadedmetadata', onLoadedMetadata);
    audio.addEventListener('timeupdate', onTimeUpdate);
    audio.addEventListener('ended', onEnded);
    audio.addEventListener('error', onError);

    return () => {
      audio.removeEventListener('loadedmetadata', onLoadedMetadata);
      audio.removeEventListener('timeupdate', onTimeUpdate);
      audio.removeEventListener('ended', onEnded);
      audio.removeEventListener('error', onError);
      audio.pause();
      audio.src = '';
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const normalizedQuery = useMemo(() => normalizeArabicForSearch(search), [search]);

  const filteredSurahs = useMemo(() => {
    if (!search.trim()) return surahs;

    return surahs.filter(s => {
      if (String(s.number) === search.trim()) return true;
      const nameNorm = normalizeArabicForSearch(s.name);
      const engNorm = normalizeArabicForSearch(s.englishName);
      return nameNorm.includes(normalizedQuery) || engNorm.includes(normalizedQuery);
    });
  }, [surahs, search, normalizedQuery]);

  async function startSurah(
    surahNumber: number,
    reciterId: string,
    opts: { autoplay: boolean; silentErrors?: boolean }
  ) {
    const audio = audioRef.current;

    setSelectedSurah(surahNumber);
    setShowSurahList(false);
    setLoading(true);

    // Stop current audio cleanly
    audio.pause();
    audio.currentTime = 0;

    const url = getSurahAudioUrl({ surahNumber, reciterId });
    audio.src = url;
    audio.load();

    if (!opts.autoplay) {
      setIsPlaying(false);
      setLoading(false);
      return;
    }

    try {
      // IMPORTANT: call play() immediately while still in user gesture (onClick/onChange)
      await audio.play();
      setIsPlaying(true);
    } catch {
      setIsPlaying(false);
      setLoading(false);
      if (!opts.silentErrors) {
        toast.error(t('audioPlayError'));
      }
    }

    // Add error handler for network failures
    audio.onerror = () => {
      setIsPlaying(false);
      setLoading(false);
      if (!opts.silentErrors) {
        toast.error(t('audioNotAvailable'));
      }
    };
  }

  const handleReciterChange = async (newReciterId: ReciterId) => {
    const audio = audioRef.current;
    const wasPlaying = !audio.paused;

    setReciter(newReciterId);
    reciterRef.current = newReciterId;
    localStorage.setItem('quran-reciter', newReciterId);

    // If a surah is selected, reload it with the new reciter.
    if (selectedSurahRef.current) {
      // Unlock audio context immediately within user gesture by calling play() on current src
      if (wasPlaying) {
        try { await audio.play(); } catch { /* expected, just unlocking */ }
      }
      await startSurah(selectedSurahRef.current, newReciterId, { autoplay: wasPlaying });
    }
  };

  const togglePlay = async () => {
    const audio = audioRef.current;
    if (!audio.src) return;

    if (!audio.paused) {
      audio.pause();
      setIsPlaying(false);
      return;
    }

    try {
      await audio.play();
      setIsPlaying(true);
    } catch {
      setIsPlaying(false);
      toast.error(t('audioPlayError'));
    }
  };

  const nextSurah = async () => {
    const current = selectedSurahRef.current;
    if (!current) return;
    const next = current >= 114 ? 1 : current + 1;
    await startSurah(next, reciterRef.current, { autoplay: true, silentErrors: true });
  };

  const prevSurah = async () => {
    const current = selectedSurahRef.current;
    if (!current) return;
    const prev = current <= 1 ? 114 : current - 1;
    await startSurah(prev, reciterRef.current, { autoplay: true, silentErrors: true });
  };

  const cycleRepeat = () => {
    setRepeatMode(prev => (prev === 'none' ? 'all' : prev === 'all' ? 'one' : 'none'));
  };

  const seekTo = (e: React.MouseEvent<HTMLDivElement>) => {
    const audio = audioRef.current;
    if (!audio.duration) return;
    const rect = e.currentTarget.getBoundingClientRect();
    // RTL: right side = 0%, left side = 100%
    const pct = 1 - (e.clientX - rect.left) / rect.width;
    audio.currentTime = Math.max(0, Math.min(audio.duration, pct * audio.duration));
  };

  const closePlayer = () => {
    const audio = audioRef.current;
    audio.pause();
    audio.currentTime = 0;
    // Keep src so reopening keeps current selection; user asked mainly switching reliability
    setIsOpen(false);
    setIsPlaying(false);
    setSelectedSurah(null);
    setProgress(0);
    setCurrentTime(0);
    setDuration(0);
    setSearch('');
    setShowSurahList(false);
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  const currentSurah = surahs.find(s => s.number === selectedSurah);

  return (
    <>
      {!isOpen && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.38 }}
          className="px-4 mb-4"
        >
          <button
            onClick={() => setIsOpen(true)}
            className="w-full glass-mystic rounded-3xl p-5 text-right shadow-elevated"
          >
            <div className="flex items-center justify-between mb-2">
              <Moon className="h-5 w-5 text-primary" />
              <span className="inline-block rounded-full bg-primary/10 border border-primary/20 px-3 py-1 text-xs font-medium text-primary">
                {t('listenWhileSleep')}
              </span>
            </div>
            <p className="text-sm font-bold text-foreground mb-1">{t('quranPlayerTitle')}</p>
            <p className="text-xs text-muted-foreground">
              {t('quranPlayerDesc')} — {RECITERS.length} {t('reciterCount')}
            </p>
          </button>
        </motion.div>
      )}

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="px-4 mb-4"
          >
            <div className="glass-mystic rounded-3xl overflow-hidden shadow-elevated">
              <div className="gradient-islamic p-4 flex items-center justify-between relative overflow-hidden">
                <div className="absolute inset-0 islamic-pattern opacity-20" />
                <button onClick={closePlayer} aria-label={t('closePlayer')} className="p-1.5 rounded-full bg-white/10 relative z-10">
                  <X className="h-4 w-4 text-white" />
                </button>
                <div className="text-right relative z-10">
                  <h3 className="text-sm font-bold text-white">{t('quranPlayerLabel')}</h3>
                  {currentSurah && (
                    <p className="text-white/70 text-xs mt-0.5">
                      {currentSurah.number}. {currentSurah.name}
                    </p>
                  )}
                </div>
              </div>

              <div className="p-4 border-b border-border/10">
                <label className="text-xs text-muted-foreground mb-1.5 block">
                  {t('reciterLabel')} ({RECITERS.length} {t('reciterCount')})
                </label>
                <select
                  value={reciter}
                  onChange={e => void handleReciterChange(e.target.value as ReciterId)}
                  className="w-full rounded-2xl bg-muted border-0 p-2.5 text-sm text-foreground text-right"
                  dir="rtl"
                >
                  {RECITERS.map(r => (
                    <option key={r.id} value={r.id}>
                      {t(r.nameKey)}
                    </option>
                  ))}
                </select>
              </div>

              <div className="p-4 border-b border-border/10">
                <button
                  onClick={() => setShowSurahList(!showSurahList)}
                  className="w-full flex items-center justify-between rounded-2xl bg-muted p-3"
                >
                  <ChevronDown
                    className={cn(
                      'h-4 w-4 text-muted-foreground transition-transform',
                      showSurahList && 'rotate-180'
                    )}
                  />
                  <span className="text-sm font-medium text-foreground">
                    {currentSurah ? `${currentSurah.number}. ${currentSurah.name}` : t('chooseSurah')}
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
                          <Search className="absolute end-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
                          <Input
                            value={search}
                            onChange={e => setSearch(e.target.value)}
                            placeholder={t('searchSurah')}
                            className="pe-8 rounded-2xl text-start text-xs h-9 border-border/10"
                          />
                        </div>
                        <div className="max-h-48 overflow-y-auto space-y-0.5">
                          {filteredSurahs.map(s => (
                            <button
                              key={s.number}
                              onClick={() => void startSurah(s.number, reciterRef.current, { autoplay: true })}
                              className={cn(
                                'w-full flex items-center justify-between p-2.5 rounded-xl text-right transition-colors',
                                selectedSurah === s.number
                                  ? 'bg-primary/10 text-primary'
                                  : 'hover:bg-muted'
                              )}
                            >
                              <span className="text-xs text-muted-foreground">{s.numberOfAyahs} {t('versesCount')}</span>
                              <div className="flex items-center gap-2">
                                <span className="text-xs font-medium text-foreground">{s.name}</span>
                                <span className="text-xs text-muted-foreground w-6 text-center">{s.number}</span>
                              </div>
                            </button>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {selectedSurah && (
                <div className="p-4">
                  <div className="w-full h-1.5 rounded-full bg-muted mb-2 cursor-pointer" onClick={seekTo}>
                    <div
                      className="h-full rounded-full bg-primary transition-all duration-300"
                      style={{ width: `${progress}%`, marginInlineEnd: 'auto', marginInlineStart: 0 }}
                    />
                  </div>
                  <div className="flex justify-between text-xs text-muted-foreground mb-4 tabular-nums" dir="ltr">
                    <span>{formatTime(currentTime)}</span>
                    <span>{formatTime(duration)}</span>
                  </div>

                  <div className="flex items-center justify-center gap-5">
                    <button onClick={cycleRepeat} aria-label={t('changeRepeatMode')} className="p-2">
                      {repeatMode === 'one' ? (
                        <Repeat1 className="h-5 w-5 text-primary" />
                      ) : (
                        <Repeat
                          className={cn(
                            'h-5 w-5',
                            repeatMode === 'all' ? 'text-primary' : 'text-muted-foreground'
                          )}
                        />
                      )}
                    </button>

                    <button onClick={() => void nextSurah()} aria-label={t('nextSurah')} className="p-2">
                      <SkipForward className="h-5 w-5 text-foreground" />
                    </button>

                    <button
                      onClick={() => void togglePlay()}
                      disabled={loading}
                      aria-label={isPlaying ? t('pauseBtn') : t('playBtn')}
                      className="h-14 w-14 rounded-full bg-primary flex items-center justify-center shadow-lg shadow-primary/20"
                    >
                      {loading ? (
                        <div className="h-5 w-5 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                      ) : isPlaying ? (
                        <Pause className="h-6 w-6 text-primary-foreground" />
                      ) : (
                        <Play className="h-6 w-6 text-primary-foreground" />
                      )}
                    </button>

                    <button onClick={() => void prevSurah()} aria-label={t('prevSurah')} className="p-2">
                      <SkipBack className="h-5 w-5 text-foreground" />
                    </button>

                    <div className="p-2">
                      <Volume2 className="h-5 w-5 text-muted-foreground" />
                    </div>
                  </div>

                  <p className="text-center text-xs text-muted-foreground mt-3">
                    {repeatMode === 'one' && t('repeatCurrentSurah')}
                    {repeatMode === 'all' && t('repeatAllSurahs')}
                    {repeatMode === 'none' && t('autoNextSurah')}
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
