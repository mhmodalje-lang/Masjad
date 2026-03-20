import { useState, useEffect, useCallback, useRef } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import NoorMascot, { useNoorTTS, getNoorMessage } from '@/components/NoorMascot';
import { Star, Trophy, Mic, MicOff, Volume2, Sparkles, ArrowLeft, Gamepad2, RefreshCw, Zap, Check, X, ChevronRight, Flame, BookOpen, Heart, Gift } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';
const IMG_MOSQUE = 'https://images.unsplash.com/photo-1632218280088-b5bfd400477e?w=600&q=80';
const IMG_QURAN = 'https://images.unsplash.com/photo-1624862302031-013c53df5995?w=600&q=80';
const IMG_STARS = 'https://images.unsplash.com/photo-1669756491628-406a1c5028d8?w=600&q=80';
const IMG_GARDEN = 'https://images.unsplash.com/photo-1650159338301-5564292cb49a?w=600&q=80';

type GameType = 'letter_maze' | 'word_match' | 'tajweed_puzzle' | 'pronunciation';
type GamePhase = 'hub' | 'loading' | 'playing' | 'result' | 'mosque' | 'skills';

interface GameData { game_id: string; game_type: GameType; difficulty: string; time_limit: number; brick_reward: number; xp_reward: number; [key: string]: any; }
interface GameResult { xp_earned: number; bricks_earned: number; total_xp: number; total_bricks: number; difficulty: string; mosque_progress: any; weak_phonemes: number[]; level_up: boolean; }

// ═══ NOOR MESSAGES 10 LANGUAGES ═══
const NOOR_MSG: Record<string, Record<string, string>> = {
  welcome: { ar:'مرحباً يا بطل! هيا نتعلم ونلعب! 🌟', en:"Hey champion! Let's learn & play! 🌟", de:'Hey Champion! Lass uns lernen & spielen! 🌟', 'de-AT':'Servus Champion! Los geht\'s! 🌟', fr:'Salut champion! Apprenons en jouant! 🌟', tr:'Merhaba şampiyon! Öğrenelim ve oynayalım! 🌟', ru:'Привет, чемпион! Давай учиться! 🌟', sv:'Hej mästare! Nu lär vi oss! 🌟', nl:'Hey kampioen! Laten we leren! 🌟', el:'Γεια σου πρωταθλητή! Πάμε! 🌟' },
  brick: { ar:'حصلت على طوبة ذهبية! مسجدك يكبر! 🧱✨', en:'Golden Brick earned! Your mosque grows! 🧱✨', de:'Goldener Ziegel! Deine Moschee wächst! 🧱✨', 'de-AT':'Goldener Ziegel gschafft! 🧱✨', fr:'Brique dorée gagnée! 🧱✨', tr:'Altın Tuğla kazandın! 🧱✨', ru:'Золотой Кирпич! Мечеть растёт! 🧱✨', sv:'Gyllene tegelsten! 🧱✨', nl:'Gouden steen verdiend! 🧱✨', el:'Χρυσό Τούβλο! 🧱✨' },
  wrong: { ar:'لا بأس! كل محاولة تجعلك أقوى! 💪', en:"That's okay! Every try makes you stronger! 💪", de:'Kein Problem! Übung macht den Meister! 💪', 'de-AT':'Passt scho! Übung macht den Meister! 💪', fr:"C'est pas grave! Tu progresses! 💪", tr:'Sorun değil! Her deneme güçlendirir! 💪', ru:'Ничего! Каждая попытка делает сильнее! 💪', sv:'Inga problem! Övning ger färdighet! 💪', nl:'Geen probleem! Oefening baart kunst! 💪', el:'Μην ανησυχείς! Κάθε προσπάθεια μετράει! 💪' },
  speak: { ar:'انطق الكلمة بوضوح! أنت تستطيع! 🎤', en:'Say the word clearly! You can do it! 🎤', de:'Sprich das Wort klar aus! 🎤', 'de-AT':'Sag\'s Wort ganz klar! Du schaffst des! 🎤', fr:'Prononce le mot clairement! 🎤', tr:'Kelimeyi net söyle! Yapabilirsin! 🎤', ru:'Произнеси слово чётко! 🎤', sv:'Säg ordet tydligt! 🎤', nl:'Zeg het woord duidelijk! 🎤', el:'Πες τη λέξη καθαρά! 🎤' },
  quran: { ar:'هيا نتعلم كلمة من القرآن الكريم! 📖', en:"Let's learn a word from the Holy Quran! 📖", de:'Lernen wir ein Wort aus dem Quran! 📖', 'de-AT':'Lernen wir a Wort aus dem Quran! 📖', fr:'Apprenons un mot du Saint Coran! 📖', tr:"Kuran'dan bir kelime öğrenelim! 📖", ru:'Выучим слово из Священного Корана! 📖', sv:'Låt oss lära oss ett ord från Koranen! 📖', nl:'Laten we een woord uit de Koran leren! 📖', el:'Ας μάθουμε μια λέξη από το Κοράνι! 📖' },
};
const getMsg = (k: string, l: string) => NOOR_MSG[k]?.[l] || NOOR_MSG[k]?.en || '';

// ═══ DAILY QURAN WORDS (Embedded for kids) ═══
const DAILY_QURAN = [
  { ar: 'بِسْمِ اللَّهِ', trans: 'Bismillah', meaning_ar: 'باسم الله', meaning_en: 'In the name of Allah', surah: 'الفاتحة 1:1', emoji: '🌙' },
  { ar: 'الرَّحْمَنِ الرَّحِيمِ', trans: 'Ar-Rahman Ar-Raheem', meaning_ar: 'الرحمن الرحيم', meaning_en: 'The Most Gracious, Most Merciful', surah: 'الفاتحة 1:1', emoji: '💛' },
  { ar: 'الْحَمْدُ لِلَّهِ', trans: 'Alhamdulillah', meaning_ar: 'الحمد لله', meaning_en: 'All praise is for Allah', surah: 'الفاتحة 1:2', emoji: '🤲' },
  { ar: 'رَبِّ الْعَالَمِينَ', trans: 'Rabbil Aalameen', meaning_ar: 'رب العالمين', meaning_en: 'Lord of all worlds', surah: 'الفاتحة 1:2', emoji: '🌍' },
  { ar: 'إِيَّاكَ نَعْبُدُ', trans: 'Iyyaka Na\'budu', meaning_ar: 'إياك نعبد', meaning_en: 'You alone we worship', surah: 'الفاتحة 1:5', emoji: '🕌' },
  { ar: 'اهْدِنَا الصِّرَاطَ', trans: 'Ihdinas Sirat', meaning_ar: 'اهدنا الصراط', meaning_en: 'Guide us to the path', surah: 'الفاتحة 1:6', emoji: '✨' },
  { ar: 'قُلْ هُوَ اللَّهُ أَحَدٌ', trans: 'Qul Huwa Allahu Ahad', meaning_ar: 'قل هو الله أحد', meaning_en: 'Say: He is Allah, the One', surah: 'الإخلاص 112:1', emoji: '⭐' },
];

// ═══ KIDS HADITH ═══
const KIDS_HADITH = [
  { ar: 'خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ', en: 'The best of you are those who learn the Quran and teach it', emoji: '📖' },
  { ar: 'طَلَبُ الْعِلْمِ فَرِيضَةٌ عَلَى كُلِّ مُسْلِمٍ', en: 'Seeking knowledge is an obligation upon every Muslim', emoji: '🎓' },
  { ar: 'مَنْ سَلَكَ طَرِيقًا يَلْتَمِسُ فِيهِ عِلْمًا سَهَّلَ اللَّهُ لَهُ طَرِيقًا إِلَى الْجَنَّةِ', en: 'Whoever treads a path seeking knowledge, Allah makes easy for them a path to Paradise', emoji: '🌴' },
  { ar: 'تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ', en: 'Your smile to your brother is charity', emoji: '😊' },
  { ar: 'الْمُسْلِمُ مَنْ سَلِمَ الْمُسْلِمُونَ مِنْ لِسَانِهِ وَيَدِهِ', en: 'A Muslim is one from whose tongue and hand other Muslims are safe', emoji: '🤝' },
];

// ═══ CONFETTI EFFECT ═══
function Confetti({ active }: { active: boolean }) {
  if (!active) return null;
  return (
    <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
      {Array.from({ length: 30 }).map((_, i) => (
        <div
          key={i}
          className="absolute animate-confetti-fall"
          style={{
            left: `${Math.random() * 100}%`,
            top: '-10px',
            animationDelay: `${Math.random() * 2}s`,
            animationDuration: `${2 + Math.random() * 3}s`,
          }}
        >
          <span className="text-2xl">
            {['⭐', '🌟', '✨', '🎉', '🧱', '🕌', '💛', '🌙'][Math.floor(Math.random() * 8)]}
          </span>
        </div>
      ))}
    </div>
  );
}

// ═══ AUDIO WAVEFORM ═══
function AudioWave({ active, accuracy }: { active: boolean; accuracy: number }) {
  return (
    <div className="relative w-full h-20 rounded-2xl overflow-hidden bg-gradient-to-r from-violet-500/10 via-pink-500/10 to-orange-500/10 border-2 border-white/10">
      <div className="absolute inset-0 flex items-end justify-center gap-[3px] p-2">
        {Array.from({ length: 32 }).map((_, i) => (
          <div
            key={i}
            className={cn(
              "w-2 rounded-full transition-all duration-150",
              accuracy > 85 ? "bg-gradient-to-t from-green-400 to-emerald-300" :
              accuracy > 60 ? "bg-gradient-to-t from-amber-400 to-yellow-300" :
              "bg-gradient-to-t from-violet-400 to-pink-300"
            )}
            style={{
              height: active
                ? `${20 + Math.random() * 60}%`
                : `${10 + Math.sin(i * 0.5) * 15}%`,
              transition: active ? 'height 0.15s' : 'height 0.8s',
            }}
          />
        ))}
      </div>
      {/* Star overlay */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className={cn("relative transition-all duration-700", accuracy > 85 ? "scale-125" : "scale-100")}>
          <Star className={cn("w-10 h-10 drop-shadow-lg transition-all duration-500",
            accuracy > 85 ? "text-amber-400 fill-amber-400" :
            accuracy > 60 ? "text-amber-300/70 fill-amber-300/30" :
            "text-white/20"
          )} />
          {accuracy > 85 && <Sparkles className="absolute -top-2 -right-2 w-5 h-5 text-amber-300 animate-pulse" />}
        </div>
      </div>
    </div>
  );
}

// ═══ MOSQUE BUILDER (PREMIUM SVG) ═══
function MosqueBuilder({ stage, progress, bricks, onClick }: { stage: any; progress: number; bricks: number; onClick?: () => void }) {
  const s = stage?.stage || 1;
  return (
    <button onClick={onClick} className="w-full group relative overflow-hidden rounded-3xl">
      {/* Background image */}
      <div className="absolute inset-0">
        <img src={IMG_STARS} alt="" className="w-full h-full object-cover opacity-40" />
        <div className="absolute inset-0 bg-gradient-to-t from-background via-background/80 to-transparent" />
      </div>
      
      <div className="relative p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-base font-bold flex items-center gap-2">🕌 <span className="bg-gradient-to-r from-amber-300 to-amber-500 bg-clip-text text-transparent">{s >= 6 ? '✨' : ''} مسجدي</span></h3>
          <ChevronRight className="h-4 w-4 text-muted-foreground group-hover:translate-x-1 transition-transform" />
        </div>
        
        <svg viewBox="0 0 280 140" className="w-full max-w-[280px] mx-auto drop-shadow-2xl">
          {/* Stars */}
          {[...Array(8)].map((_, i) => (
            <circle key={i} cx={30 + i * 32} cy={10 + (i % 3) * 8} r="1.5" fill="#FFD700" opacity="0.6">
              <animate attributeName="opacity" values="0.3;1;0.3" dur={`${2 + i * 0.3}s`} repeatCount="indefinite" />
            </circle>
          ))}
          
          {/* Ground with grass */}
          <rect x="0" y="120" width="280" height="20" fill="url(#ground)" rx="4" />
          <defs>
            <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#4A7C59" />
              <stop offset="100%" stopColor="#2D5A3D" />
            </linearGradient>
            <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#F5E6C8" />
              <stop offset="100%" stopColor="#D4B896" />
            </linearGradient>
            <linearGradient id="dome" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={s >= 6 ? '#FFD700' : '#4A90D9'} />
              <stop offset="100%" stopColor={s >= 6 ? '#FFA500' : '#2970B8'} />
            </linearGradient>
          </defs>
          
          {/* Foundation */}
          <rect x="60" y="110" width="160" height="12" fill="#C4A882" stroke="#B8956A" strokeWidth="0.5" rx="3">
            {s === 1 && <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite" />}
          </rect>
          
          {/* Walls */}
          {s >= 2 && (
            <g>
              <rect x="70" y="60" width="140" height="50" fill="url(#wall)" stroke="#C4A882" strokeWidth="0.5" rx="2" />
              {/* Door */}
              <rect x="125" y="82" width="30" height="28" fill="#6B4226" rx="15 15 0 0" />
              <circle cx="140" cy="96" r="1.5" fill="#FFD700" />
              {/* Windows */}
              <rect x="82" y="70" width="16" height="22" fill="#87CEEB" rx="8 8 0 0" opacity="0.8" />
              <rect x="182" y="70" width="16" height="22" fill="#87CEEB" rx="8 8 0 0" opacity="0.8" />
            </g>
          )}
          
          {/* Dome */}
          {s >= 3 && (
            <g>
              <ellipse cx="140" cy="58" rx="52" ry="28" fill="url(#dome)" stroke={s >= 6 ? '#FFD700' : '#3A7BC8'} strokeWidth="1" />
              {s >= 6 && <ellipse cx="140" cy="56" rx="48" ry="24" fill="none" stroke="#FFD700" strokeWidth="0.5" opacity="0.5">
                <animate attributeName="opacity" values="0.2;0.8;0.2" dur="3s" repeatCount="indefinite" />
              </ellipse>}
            </g>
          )}
          
          {/* Minaret */}
          {s >= 4 && (
            <g>
              <rect x="218" y="28" width="14" height="84" fill="url(#wall)" stroke="#C4A882" strokeWidth="0.5" rx="2" />
              <ellipse cx="225" cy="28" rx="10" ry="7" fill="url(#dome)" />
              <line x1="225" y1="21" x2="225" y2="10" stroke="#FFD700" strokeWidth="2" />
              <circle cx="225" cy="8" r="3.5" fill="#FFD700">
                <animate attributeName="r" values="3;4;3" dur="2s" repeatCount="indefinite" />
              </circle>
              {/* Left minaret */}
              <rect x="48" y="38" width="12" height="74" fill="url(#wall)" stroke="#C4A882" strokeWidth="0.5" rx="2" />
              <ellipse cx="54" cy="38" rx="9" ry="6" fill="url(#dome)" />
              <line x1="54" y1="32" x2="54" y2="22" stroke="#FFD700" strokeWidth="1.5" />
              <circle cx="54" cy="20" r="3" fill="#FFD700" />
            </g>
          )}
          
          {/* Garden */}
          {s >= 5 && (
            <g>
              <circle cx="25" cy="115" r="10" fill="#228B22" opacity="0.8" />
              <circle cx="20" cy="108" r="7" fill="#32CD32" opacity="0.7" />
              <circle cx="255" cy="115" r="10" fill="#228B22" opacity="0.8" />
              <circle cx="260" cy="108" r="7" fill="#32CD32" opacity="0.7" />
              {/* Flowers */}
              <circle cx="30" cy="118" r="2.5" fill="#FF69B4" />
              <circle cx="250" cy="118" r="2.5" fill="#FF69B4" />
            </g>
          )}
        </svg>
        
        {/* Brick progress bar */}
        <div className="mt-2 flex items-center gap-2">
          <span className="text-lg">🧱</span>
          <div className="flex-1 h-3 bg-black/20 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-amber-400 via-amber-500 to-orange-500 transition-all duration-1000 relative"
              style={{ width: `${Math.min(100, progress)}%` }}
            >
              <div className="absolute inset-0 bg-white/20 animate-pulse rounded-full" />
            </div>
          </div>
          <span className="text-xs font-bold text-amber-400">{bricks}</span>
        </div>
      </div>
    </button>
  );
}

// ═══ MAIN KIDS ZONE ═══
export default function KidsZone() {
  const { t, dir, locale } = useLocale();
  const navigate = useNavigate();
  const { speak } = useNoorTTS();
  
  const [phase, setPhase] = useState<GamePhase>('hub');
  const [gameData, setGameData] = useState<GameData | null>(null);
  const [gameResult, setGameResult] = useState<GameResult | null>(null);
  const [progress, setProgress] = useState<any>(null);
  const [selectedType, setSelectedType] = useState<GameType | null>(null);
  const [noorMsg, setNoorMsg] = useState('');
  const [noorMood, setNoorMood] = useState<'happy' | 'thinking' | 'celebrating' | 'greeting'>('greeting');
  const [userId] = useState(() => localStorage.getItem('kids_user_id') || `kid_${Date.now()}`);
  const [showConfetti, setShowConfetti] = useState(false);
  const [dailyQuranIdx] = useState(() => new Date().getDate() % DAILY_QURAN.length);
  const [dailyHadithIdx] = useState(() => new Date().getDate() % KIDS_HADITH.length);
  const [streak] = useState(() => parseInt(localStorage.getItem('kids_streak') || '1'));
  
  // Game state
  const [matchedPairs, setMatchedPairs] = useState<Set<number>>(new Set());
  const [selectedWord, setSelectedWord] = useState<number | null>(null);
  const [selectedMeaning, setSelectedMeaning] = useState<number | null>(null);
  const [tajweedAnswer, setTajweedAnswer] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [speechResult, setSpeechResult] = useState('');
  const [pronAccuracy, setPronAccuracy] = useState(0);
  const [timeLeft, setTimeLeft] = useState(0);
  const [gameScore, setGameScore] = useState(0);
  const [showCorrect, setShowCorrect] = useState(false);
  const [showWrong, setShowWrong] = useState(false);
  
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => { localStorage.setItem('kids_user_id', userId); }, [userId]);
  useEffect(() => { loadProgress(); setNoorMsg(getMsg('welcome', locale)); }, [locale]);

  const loadProgress = useCallback(async () => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/kids-zone/progress?user_id=${userId}`);
      const d = await r.json();
      if (d.success) setProgress(d);
    } catch {}
  }, [userId]);

  useEffect(() => {
    if (phase === 'playing' && timeLeft > 0) {
      timerRef.current = setTimeout(() => setTimeLeft(v => v - 1), 1000);
      return () => { if (timerRef.current) clearTimeout(timerRef.current); };
    }
    if (phase === 'playing' && timeLeft === 0 && gameData) handleGameEnd(false, gameScore);
  }, [phase, timeLeft]);

  const startGame = useCallback(async (type: GameType) => {
    setPhase('loading');
    setSelectedType(type);
    setNoorMood('thinking');
    try {
      const r = await fetch(`${BACKEND_URL}/api/kids-zone/generate-game?user_id=${userId}&game_type=${type}&locale=${locale}`);
      const d = await r.json();
      if (d.success) {
        setGameData(d.game);
        setPhase('playing');
        setTimeLeft(d.game.time_limit);
        setGameScore(0);
        setMatchedPairs(new Set());
        setSelectedWord(null); setSelectedMeaning(null);
        setTajweedAnswer(null); setSpeechResult(''); setPronAccuracy(0);
        setShowCorrect(false); setShowWrong(false);
        setNoorMood('happy');
        if (type === 'pronunciation') setNoorMsg(getMsg('speak', locale));
        else if (type === 'word_match') setNoorMsg(getMsg('quran', locale));
      }
    } catch { toast.error('Could not load game'); setPhase('hub'); }
  }, [userId, locale]);

  const handleGameEnd = useCallback(async (correct: boolean, score: number) => {
    if (timerRef.current) clearTimeout(timerRef.current);
    setPhase('result');
    if (correct) { setShowConfetti(true); setTimeout(() => setShowConfetti(false), 4000); }
    
    const phonemes = gameData?.target_letter ? [gameData.target_letter.id] : gameData?.letter_id ? [gameData.letter_id] : [];
    try {
      const r = await fetch(`${BACKEND_URL}/api/kids-zone/submit-result`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, game_type: gameData?.game_type, correct, score: score || gameScore, phonemes_tested: phonemes, pronunciation_accuracy: pronAccuracy }),
      });
      const d = await r.json();
      if (d.success) {
        setGameResult(d);
        if (correct) { setNoorMsg(getMsg('brick', locale)); setNoorMood('celebrating'); speak(getNoorMessage('correct', locale)); }
        else { setNoorMsg(getMsg('wrong', locale)); setNoorMood('happy'); speak(getNoorMessage('encourage', locale)); }
        loadProgress();
      }
    } catch {}
  }, [gameData, gameScore, pronAccuracy, userId, locale, speak, loadProgress]);

  // ═══ PRONUNCIATION LOGIC ═══
  const startListening = useCallback(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { toast.error('Speech not supported'); return; }
    const rec = new SR();
    rec.lang = 'ar-SA'; rec.continuous = false; rec.interimResults = false; rec.maxAlternatives = 5;
    rec.onresult = (e: any) => {
      const spoken = e.results[0][0].transcript.trim();
      setSpeechResult(spoken);
      const target = (gameData?.target_word || '').replace(/[\u064B-\u065F\u0670]/g, '');
      const spokenC = spoken.replace(/[\u064B-\u065F\u0670]/g, '');
      let acc = 0;
      if (spokenC === target) acc = 100;
      else if (target.includes(spokenC) || spokenC.includes(target)) acc = 80;
      else { const tc = new Set(target.split('')); const sc = new Set(spokenC.split('')); let o = 0; tc.forEach(c => { if (sc.has(c)) o++; }); acc = Math.round((o / Math.max(tc.size, 1)) * 100); }
      setPronAccuracy(acc); setIsListening(false);
      if (acc >= (gameData?.accuracy_threshold || 85)) { setGameScore(s => s + gameData!.xp_reward); setTimeout(() => handleGameEnd(true, gameData!.xp_reward), 1500); }
    };
    rec.onerror = () => setIsListening(false);
    rec.onend = () => setIsListening(false);
    recognitionRef.current = rec; rec.start(); setIsListening(true); setSpeechResult(''); setPronAccuracy(0);
  }, [gameData, handleGameEnd]);

  const dailyQuran = DAILY_QURAN[dailyQuranIdx];
  const dailyHadith = KIDS_HADITH[dailyHadithIdx];
  const tier = progress?.profile?.difficulty || 'seedling';
  const xp = progress?.profile?.total_xp || 0;
  const bricks = progress?.profile?.golden_bricks || 0;
  const gamesPlayed = progress?.profile?.games_played || 0;

  // ═══════════════════════════
  //        HUB SCREEN
  // ═══════════════════════════
  const renderHub = () => (
    <div className="space-y-5 pb-6">
      {/* XP / Stats bar */}
      <div className="rounded-2xl bg-gradient-to-r from-indigo-600/30 via-violet-600/20 to-pink-600/30 p-3 border border-white/10 backdrop-blur-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Avatar circle */}
            <div className="w-11 h-11 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-xl shadow-lg shadow-amber-500/30">
              {tier === 'forest' ? '🌳' : tier === 'tree' ? '🌲' : tier === 'sapling' ? '🌿' : tier === 'sprout' ? '🌱' : '🌰'}
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <Zap className="h-3.5 w-3.5 text-amber-400" />
                <span className="text-sm font-bold">{xp}</span>
                <span className="text-[10px] text-muted-foreground">XP</span>
              </div>
              <div className="w-24 h-1.5 bg-black/20 rounded-full mt-0.5">
                <div className="h-full rounded-full bg-gradient-to-r from-amber-400 to-amber-500" style={{ width: `${Math.min(100, (xp % 100))}%` }} />
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-orange-500/20 border border-orange-500/30">
              <span className="text-sm">🧱</span>
              <span className="text-sm font-bold text-orange-400">{bricks}</span>
            </div>
            <div className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-red-500/20 border border-red-500/30">
              <Flame className="h-3.5 w-3.5 text-red-400" />
              <span className="text-sm font-bold text-red-400">{streak}</span>
            </div>
          </div>
        </div>
      </div>

      {/* ═══ DAILY QURAN WORD ═══ */}
      <div className="relative rounded-3xl overflow-hidden">
        <img src={IMG_QURAN} alt="" className="absolute inset-0 w-full h-full object-cover opacity-25" />
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-900/80 via-emerald-800/70 to-teal-900/80" />
        <div className="relative p-5">
          <div className="flex items-center gap-2 mb-3">
            <BookOpen className="h-4 w-4 text-emerald-300" />
            <span className="text-xs font-bold text-emerald-300 uppercase tracking-wider">{t('kidsFromQuran')}</span>
            <span className="ml-auto text-lg">{dailyQuran.emoji}</span>
          </div>
          <p className="text-3xl font-bold text-white text-center font-arabic leading-loose mb-2" dir="rtl">
            {dailyQuran.ar}
          </p>
          <p className="text-center text-emerald-200 text-sm italic mb-1">{dailyQuran.trans}</p>
          <p className="text-center text-emerald-100 text-xs">{locale === 'ar' ? dailyQuran.meaning_ar : dailyQuran.meaning_en}</p>
          <p className="text-center text-emerald-400/60 text-[10px] mt-2">{dailyQuran.surah}</p>
          <button
            onClick={() => speak(dailyQuran.ar, 'ar')}
            className="mx-auto mt-3 flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white text-xs transition-all"
          >
            <Volume2 className="h-3.5 w-3.5" /> {t('kidsListen')}
          </button>
        </div>
      </div>

      {/* ═══ GAME CARDS ═══ */}
      <div>
        <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
          <Gamepad2 className="h-5 w-5 text-violet-400" /> {t('kidsChooseGame')}
        </h3>
        <div className="grid grid-cols-2 gap-3">
          {/* Letter Maze */}
          <button onClick={() => startGame('letter_maze')} className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-600 p-4 text-white shadow-lg shadow-blue-500/30 active:scale-95 transition-all group">
            <div className="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
            <span className="text-4xl block mb-2 drop-shadow-lg group-hover:scale-110 transition-transform">🔤</span>
            <p className="text-sm font-bold">{t('kidsLetterMaze')}</p>
            <p className="text-[10px] text-white/70 mt-0.5">{t('kidsFind')}</p>
          </button>
          
          {/* Word Match */}
          <button onClick={() => startGame('word_match')} className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-500 to-green-600 p-4 text-white shadow-lg shadow-emerald-500/30 active:scale-95 transition-all group">
            <div className="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
            <span className="text-4xl block mb-2 drop-shadow-lg group-hover:scale-110 transition-transform">📖</span>
            <p className="text-sm font-bold">{t('kidsWordMatch')}</p>
            <p className="text-[10px] text-white/70 mt-0.5">{t('kidsFromQuran')}</p>
          </button>
          
          {/* Tajweed */}
          <button onClick={() => startGame('tajweed_puzzle')} className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-500 to-violet-600 p-4 text-white shadow-lg shadow-purple-500/30 active:scale-95 transition-all group">
            <div className="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
            <span className="text-4xl block mb-2 drop-shadow-lg group-hover:scale-110 transition-transform">🎯</span>
            <p className="text-sm font-bold">{t('kidsTajweedPuzzle')}</p>
            <p className="text-[10px] text-white/70 mt-0.5">إدغام • إخفاء • قلقلة</p>
          </button>
          
          {/* Pronunciation */}
          <button onClick={() => startGame('pronunciation')} className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-pink-500 to-rose-600 p-4 text-white shadow-lg shadow-pink-500/30 active:scale-95 transition-all group">
            <div className="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
            <span className="text-4xl block mb-2 drop-shadow-lg group-hover:scale-110 transition-transform">🎤</span>
            <p className="text-sm font-bold">{t('kidsPronunciation')}</p>
            <p className="text-[10px] text-white/70 mt-0.5">{t('kidsSayWord')}</p>
          </button>
        </div>
        
        {/* AI Auto-play */}
        <button
          onClick={() => { const types: GameType[] = ['letter_maze','word_match','tajweed_puzzle','pronunciation']; startGame(types[Math.floor(Math.random()*types.length)]); }}
          className="w-full mt-3 py-4 rounded-2xl bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 text-white flex items-center justify-center gap-2 font-bold shadow-lg shadow-orange-500/30 active:scale-[0.98] transition-all"
        >
          <Sparkles className="h-5 w-5 animate-pulse" /> {t('kidsAutoPlay')} ✨
        </button>
      </div>

      {/* ═══ MY MOSQUE ═══ */}
      {progress?.mosque && (
        <MosqueBuilder
          stage={progress.mosque.current_stage}
          progress={progress.mosque.progress_pct}
          bricks={bricks}
          onClick={() => setPhase('mosque')}
        />
      )}

      {/* ═══ SKILL MAP (Letter Grid) ═══ */}
      {progress?.letter_skills && (
        <button onClick={() => setPhase('skills')} className="w-full rounded-3xl bg-gradient-to-br from-indigo-500/10 to-violet-500/10 border border-indigo-500/20 p-4 text-start">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-base font-bold flex items-center gap-2">
              <span className="text-lg">🔤</span> {t('kidsWeakAreas')}
            </h3>
            <ChevronRight className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="flex flex-wrap gap-1.5">
            {progress.letter_skills.slice(0, 14).map((ls: any) => (
              <div
                key={ls.id}
                className={cn(
                  "w-9 h-9 rounded-lg flex items-center justify-center text-lg font-bold transition-all",
                  ls.accuracy >= 80 ? "bg-green-500/20 text-green-400 border border-green-500/30" :
                  ls.accuracy >= 50 ? "bg-amber-500/20 text-amber-400 border border-amber-500/30" :
                  "bg-red-500/20 text-red-400 border border-red-500/30"
                )}
              >
                {ls.letter}
              </div>
            ))}
            <div className="w-9 h-9 rounded-lg flex items-center justify-center text-xs text-muted-foreground bg-muted/30">
              +14
            </div>
          </div>
        </button>
      )}

      {/* ═══ DAILY HADITH ═══ */}
      <div className="relative rounded-2xl overflow-hidden">
        <img src={IMG_GARDEN} alt="" className="absolute inset-0 w-full h-full object-cover opacity-20" />
        <div className="absolute inset-0 bg-gradient-to-r from-amber-900/70 to-orange-900/60" />
        <div className="relative p-4">
          <div className="flex items-center gap-2 mb-2">
            <Heart className="h-3.5 w-3.5 text-amber-300" />
            <span className="text-[10px] font-bold text-amber-300 uppercase tracking-wider">حديث اليوم</span>
            <span className="ml-auto text-base">{dailyHadith.emoji}</span>
          </div>
          <p className="text-base font-bold text-white leading-relaxed font-arabic" dir="rtl">{dailyHadith.ar}</p>
          <p className="text-xs text-amber-200 mt-2 italic">{dailyHadith.en}</p>
        </div>
      </div>
    </div>
  );

  // ═══ GAME SCREENS ═══
  const renderLetterMaze = () => {
    if (!gameData?.grid) return null;
    const tgt = gameData.target_letter;
    return (
      <div className="space-y-4">
        <div className="text-center p-5 rounded-3xl bg-gradient-to-br from-blue-500/20 via-cyan-500/10 to-blue-500/20 border border-blue-500/30">
          <p className="text-xs text-blue-300 mb-2">{t('kidsFind')}</p>
          <div className="flex items-center justify-center gap-4">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/40">
              <span className="text-4xl font-bold text-white">{tgt.letter}</span>
            </div>
            <div className="text-start">
              <p className="text-xl font-bold">{tgt.name_ar}</p>
              <p className="text-sm text-muted-foreground">{tgt.transliteration}</p>
              <button onClick={() => speak(tgt.audio_hint, 'ar')} className="mt-1 flex items-center gap-1 text-xs text-blue-400">
                <Volume2 className="h-3 w-3" /> {tgt.audio_hint}
              </button>
            </div>
          </div>
          {gameData.confusable && (
            <div className="mt-3 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 inline-flex items-center gap-1.5">
              <span className="text-xs text-amber-400">⚠️ {t('kidsConfusable')}</span>
              <span className="text-xl font-bold text-amber-300">{gameData.confusable.letter}</span>
            </div>
          )}
        </div>
        <div className="grid gap-3 max-w-xs mx-auto" style={{ gridTemplateColumns: `repeat(${gameData.grid_size}, 1fr)` }}>
          {gameData.grid.flat().map((cell: any, idx: number) => (
            <button
              key={idx}
              onClick={() => {
                if (cell.is_target) {
                  setShowCorrect(true); setGameScore(s => s + gameData.xp_reward);
                  speak(getNoorMessage('correct', locale));
                  setTimeout(() => handleGameEnd(true, gameData.xp_reward), 1200);
                } else {
                  setShowWrong(true); speak(getNoorMessage('wrong', locale));
                  setTimeout(() => setShowWrong(false), 600);
                }
              }}
              className={cn(
                "aspect-square rounded-2xl text-3xl font-bold flex items-center justify-center border-2 transition-all active:scale-90 shadow-md",
                showCorrect && cell.is_target ? "bg-green-500/30 border-green-400 scale-110 shadow-green-500/40" :
                "bg-card/80 border-white/10 hover:border-blue-400/50 hover:shadow-blue-500/20"
              )}
            >
              {cell.letter}
            </button>
          ))}
        </div>
      </div>
    );
  };

  const renderWordMatch = () => {
    if (!gameData?.words) return null;
    const checkMatch = (wIdx: number, mIdx: number) => {
      const w = gameData.words[wIdx], m = gameData.meanings[mIdx];
      if (w.id === m.id) {
        const nm = new Set(matchedPairs); nm.add(wIdx); setMatchedPairs(nm);
        setGameScore(s => s + 5); speak(getNoorMessage('correct', locale));
        if (nm.size === gameData.words.length) setTimeout(() => handleGameEnd(true, nm.size * 5 + gameData.xp_reward), 800);
      } else { setShowWrong(true); setTimeout(() => setShowWrong(false), 500); }
      setSelectedWord(null); setSelectedMeaning(null);
    };
    return (
      <div className="space-y-4">
        <p className="text-center text-sm font-medium bg-gradient-to-r from-emerald-400 to-green-400 bg-clip-text text-transparent">{t('kidsMatchWords')}</p>
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-2.5">
            {gameData.words.map((w: any, i: number) => (
              <button key={`w-${i}`} onClick={() => { setSelectedWord(i); if (selectedMeaning !== null) checkMatch(i, selectedMeaning); }}
                disabled={matchedPairs.has(i)}
                className={cn("w-full p-3 rounded-2xl border-2 text-center transition-all shadow-md",
                  matchedPairs.has(i) ? "bg-green-500/20 border-green-500/40 opacity-60" :
                  selectedWord === i ? "bg-emerald-500/20 border-emerald-400 scale-105 shadow-emerald-500/30" :
                  "bg-card/80 border-white/10 hover:border-emerald-400/50"
                )}>
                <span className="text-2xl font-bold">{w.word}</span>
                <p className="text-[10px] text-muted-foreground mt-1">{w.transliteration}</p>
              </button>
            ))}
          </div>
          <div className="space-y-2.5">
            {gameData.meanings.map((m: any, i: number) => (
              <button key={`m-${i}`} onClick={() => { setSelectedMeaning(i); if (selectedWord !== null) checkMatch(selectedWord, i); }}
                disabled={matchedPairs.has(gameData.words.findIndex((w: any) => w.id === m.id))}
                className={cn("w-full p-3 rounded-2xl border-2 text-center transition-all shadow-md",
                  matchedPairs.has(gameData.words.findIndex((w: any) => w.id === m.id)) ? "bg-green-500/20 border-green-500/40 opacity-60" :
                  selectedMeaning === i ? "bg-emerald-500/20 border-emerald-400 scale-105 shadow-emerald-500/30" :
                  "bg-card/80 border-white/10 hover:border-emerald-400/50"
                )}>
                <span className="text-sm font-medium">{m.meaning}</span>
                <p className="text-[10px] text-emerald-400 mt-1">📖 {m.surah}</p>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderTajweed = () => {
    if (!gameData?.question_rule) return null;
    const rule = gameData.question_rule;
    return (
      <div className="space-y-4">
        <div className="text-center p-5 rounded-3xl bg-gradient-to-br from-purple-500/20 to-violet-500/20 border border-purple-500/30">
          <p className="text-xs text-purple-300 mb-2">{t('kidsTajweedQ')}</p>
          <p className="text-4xl font-bold text-white mb-2 font-arabic" dir="rtl">{rule.example}</p>
          <div className="flex items-center justify-center gap-2">
            <span className="px-3 py-1 rounded-full bg-purple-500/20 text-sm font-bold text-purple-300">{rule.name_ar}</span>
            <span className="text-xs text-muted-foreground">{rule.name_en}</span>
          </div>
          <button onClick={() => speak(rule.example, 'ar')} className="mt-3 mx-auto flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 text-white text-xs"><Volume2 className="h-3 w-3" /> {t('kidsListen')}</button>
        </div>
        <p className="text-sm text-center text-muted-foreground px-2">{gameData.description}</p>
        <div className="space-y-2.5">
          {gameData.choices.map((ch: string, i: number) => {
            const isSel = tajweedAnswer === ch, isCorr = ch === gameData.correct_answer, done = tajweedAnswer !== null;
            return (
              <button key={i} onClick={() => {
                if (done) return; setTajweedAnswer(ch);
                if (isCorr) { setGameScore(s => s + gameData.xp_reward); speak(getNoorMessage('correct', locale)); setTimeout(() => handleGameEnd(true, gameData.xp_reward), 1500); }
                else { speak(getNoorMessage('wrong', locale)); setTimeout(() => handleGameEnd(false, 0), 1500); }
              }}
              className={cn("w-full p-4 rounded-2xl border-2 flex items-center gap-3 transition-all shadow-md",
                done && isCorr ? "bg-green-500/20 border-green-400 shadow-green-500/20" :
                done && isSel && !isCorr ? "bg-red-500/20 border-red-400" :
                !done ? "bg-card/80 border-white/10 hover:border-purple-400/50 active:scale-[0.97]" :
                "bg-card/40 border-white/5 opacity-40"
              )}>
                <span className={cn("w-9 h-9 rounded-xl flex items-center justify-center text-sm font-bold",
                  done && isCorr ? "bg-green-500 text-white" : done && isSel ? "bg-red-500 text-white" : "bg-white/10"
                )}>{String.fromCharCode(65 + i)}</span>
                <span className="font-medium capitalize flex-1 text-start">{ch.replace(/_/g, ' ')}</span>
                {done && isCorr && <Check className="h-5 w-5 text-green-400" />}
                {done && isSel && !isCorr && <X className="h-5 w-5 text-red-400" />}
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  const renderPronunciation = () => {
    if (!gameData?.target_word) return null;
    const thresh = gameData.accuracy_threshold || 85;
    return (
      <div className="space-y-4">
        <div className="text-center p-6 rounded-3xl bg-gradient-to-br from-pink-500/20 via-rose-500/10 to-pink-500/20 border border-pink-500/30">
          <p className="text-xs text-pink-300 mb-2">{t('kidsSayWord')}</p>
          <div className="w-24 h-24 mx-auto rounded-3xl bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center shadow-lg shadow-pink-500/40 mb-3">
            <span className="text-4xl font-bold text-white">{gameData.target_word}</span>
          </div>
          <p className="text-lg text-pink-200 italic">{gameData.transliteration}</p>
          <p className="text-sm text-foreground/70 mt-1">{gameData.meaning}</p>
          {gameData.source === 'quran' && (
            <span className="inline-flex items-center gap-1 mt-2 text-xs bg-emerald-500/20 text-emerald-300 px-3 py-1 rounded-full">📖 {t('kidsFromQuran')}</span>
          )}
        </div>
        
        <AudioWave active={isListening} accuracy={pronAccuracy} />
        
        <div className="flex gap-3">
          <button onClick={() => speak(gameData.target_word, 'ar')}
            className="flex-1 py-3.5 rounded-2xl bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-blue-300 flex items-center justify-center gap-2 border border-blue-500/30 active:scale-95 transition-all">
            <Volume2 className="h-5 w-5" /> {t('kidsListen')}
          </button>
          <button onClick={isListening ? () => { recognitionRef.current?.stop(); setIsListening(false); } : startListening}
            className={cn("flex-1 py-3.5 rounded-2xl flex items-center justify-center gap-2 border active:scale-95 transition-all",
              isListening ? "bg-red-500/20 text-red-400 border-red-500/30 animate-pulse" : "bg-gradient-to-r from-pink-500/20 to-rose-500/20 text-pink-300 border-pink-500/30"
            )}>
            {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
            {isListening ? t('kidsStop') : t('kidsSpeak')}
          </button>
        </div>
        
        {speechResult && (
          <div className={cn("p-4 rounded-2xl border-2 text-center transition-all shadow-lg",
            pronAccuracy >= thresh ? "bg-green-500/10 border-green-400 shadow-green-500/20" : "bg-amber-500/10 border-amber-400"
          )}>
            <p className="text-xs text-muted-foreground">{t('kidsYouSaid')}:</p>
            <p className="text-2xl font-bold mt-1">{speechResult}</p>
            <div className="flex items-center justify-center gap-2 mt-2">
              <Star className={cn("h-6 w-6", pronAccuracy >= thresh ? "text-amber-400 fill-amber-400" : "text-muted-foreground")} />
              <span className="text-xl font-bold">{pronAccuracy}%</span>
              {pronAccuracy >= thresh && <span className="text-green-400 text-sm font-bold">{t('kidsExcellent')} 🎉</span>}
            </div>
          </div>
        )}
        {speechResult && pronAccuracy < thresh && (
          <button onClick={() => { setSpeechResult(''); setPronAccuracy(0); }}
            className="w-full py-3 rounded-2xl bg-gradient-to-r from-pink-500 to-rose-500 text-white font-bold active:scale-95 transition-all">
            <RefreshCw className="h-4 w-4 inline mr-2" /> {t('kidsTryAgain')}
          </button>
        )}
      </div>
    );
  };

  // ═══ RESULT SCREEN ═══
  const renderResult = () => {
    if (!gameResult) return null;
    const won = gameResult.bricks_earned > 0;
    return (
      <div className="space-y-5 text-center pt-4">
        <div className={cn("text-7xl", won ? "animate-bounce" : "")}>{won ? '🎉' : '💪'}</div>
        <h2 className="text-2xl font-bold bg-gradient-to-r from-amber-300 to-orange-400 bg-clip-text text-transparent">
          {won ? t('kidsWellDone') : t('kidsKeepTrying')}
        </h2>
        
        <div className="flex justify-center gap-4">
          <div className="p-4 rounded-2xl bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/30 shadow-lg shadow-amber-500/10">
            <Zap className="h-7 w-7 text-amber-400 mx-auto" />
            <p className="text-2xl font-bold text-amber-400 mt-1">+{gameResult.xp_earned}</p>
            <p className="text-[10px] text-muted-foreground">XP</p>
          </div>
          <div className="p-4 rounded-2xl bg-gradient-to-br from-orange-500/20 to-red-500/20 border border-orange-500/30 shadow-lg shadow-orange-500/10">
            <span className="text-3xl">🧱</span>
            <p className="text-2xl font-bold text-orange-400 mt-1">+{gameResult.bricks_earned}</p>
            <p className="text-[10px] text-muted-foreground">{t('kidsBricks')}</p>
          </div>
        </div>

        {gameResult.level_up && (
          <div className="p-4 rounded-2xl bg-gradient-to-r from-purple-500/20 via-pink-500/20 to-purple-500/20 border border-purple-500/30 animate-pulse">
            <Trophy className="h-10 w-10 text-purple-400 mx-auto mb-2" />
            <p className="font-bold text-purple-300 text-lg">{t('kidsLevelUp')}!</p>
            <p className="text-sm text-purple-200 capitalize">{gameResult.difficulty}</p>
          </div>
        )}

        {gameResult.mosque_progress && (
          <MosqueBuilder stage={gameResult.mosque_progress.current_stage} progress={gameResult.mosque_progress.progress_pct} bricks={gameResult.total_bricks} />
        )}

        <div className="flex gap-3 pt-2">
          <button onClick={() => startGame(selectedType || 'letter_maze')}
            className="flex-1 py-3.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold shadow-lg shadow-orange-500/30 active:scale-95 transition-all flex items-center justify-center gap-2">
            <RefreshCw className="h-4 w-4" /> {t('kidsPlayAgain')}
          </button>
          <button onClick={() => { setPhase('hub'); setGameData(null); setGameResult(null); }}
            className="flex-1 py-3.5 rounded-2xl bg-white/10 border border-white/10 font-bold active:scale-95 transition-all">
            {t('kidsBackToMenu')}
          </button>
        </div>
      </div>
    );
  };

  // ═══ MOSQUE DETAIL VIEW ═══
  const renderMosqueDetail = () => {
    const m = progress?.mosque;
    if (!m) return null;
    return (
      <div className="space-y-5 text-center">
        <h2 className="text-xl font-bold bg-gradient-to-r from-amber-300 to-orange-400 bg-clip-text text-transparent">🕌 {t('kidsMyMosque')}</h2>
        <MosqueBuilder stage={m.current_stage} progress={m.progress_pct} bricks={bricks} />
        {m.next_stage && (
          <div className="p-4 rounded-2xl bg-gradient-to-r from-amber-500/10 to-orange-500/10 border border-amber-500/20">
            <p className="text-xs text-muted-foreground">{t('kidsNextStage')}</p>
            <p className="text-lg font-bold mt-1">{m.next_stage.emoji} <span className="capitalize">{m.next_stage.name}</span></p>
            <p className="text-sm text-amber-400">🧱 {m.bricks_to_next} {t('kidsBricksNeeded')}</p>
          </div>
        )}
        <div className="space-y-2">
          {m.stages.map((s: any) => (
            <div key={s.stage} className={cn("flex items-center gap-3 px-4 py-3 rounded-2xl border transition-all",
              bricks >= s.bricks_needed ? "bg-green-500/10 border-green-500/30" : "bg-card/50 border-white/5"
            )}>
              <span className="text-2xl">{s.emoji}</span>
              <div className="flex-1 text-start">
                <p className="text-sm font-bold capitalize">{s.name}</p>
                <p className="text-[10px] text-muted-foreground">{s.bricks_needed} {t('kidsBricks')}</p>
              </div>
              {bricks >= s.bricks_needed ? <Check className="h-5 w-5 text-green-400" /> : <span className="text-xs text-muted-foreground">🧱 {s.bricks_needed - bricks}</span>}
            </div>
          ))}
        </div>
        <button onClick={() => setPhase('hub')} className="w-full py-3 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold">{t('kidsBackToMenu')}</button>
      </div>
    );
  };

  // ═══ SKILLS MAP ═══
  const renderSkillsMap = () => {
    if (!progress?.letter_skills) return null;
    return (
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-center">🔤 خريطة الحروف</h2>
        <div className="grid grid-cols-7 gap-2">
          {progress.letter_skills.map((ls: any) => (
            <div key={ls.id} className={cn(
              "aspect-square rounded-xl flex flex-col items-center justify-center border-2 transition-all shadow-md",
              ls.accuracy >= 80 ? "bg-green-500/20 border-green-500/40 shadow-green-500/10" :
              ls.accuracy >= 50 ? "bg-amber-500/20 border-amber-500/40 shadow-amber-500/10" :
              "bg-red-500/20 border-red-500/40 shadow-red-500/10"
            )}>
              <span className="text-xl font-bold">{ls.letter}</span>
              <span className="text-[8px] text-muted-foreground">{ls.accuracy}%</span>
            </div>
          ))}
        </div>
        {progress.confusable_pairs && (
          <div className="space-y-2">
            <h3 className="text-sm font-bold text-amber-400">⚠️ حروف متشابهة</h3>
            <div className="flex flex-wrap gap-2">
              {progress.confusable_pairs.map((p: any, i: number) => (
                <span key={i} className="px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-sm">
                  {p.a} ↔ {p.b}
                </span>
              ))}
            </div>
          </div>
        )}
        <button onClick={() => setPhase('hub')} className="w-full py-3 rounded-2xl bg-white/10 border border-white/10 font-bold">{t('kidsBackToMenu')}</button>
      </div>
    );
  };

  return (
    <div dir={dir} className="min-h-screen bg-background pb-24">
      <Confetti active={showConfetti} />
      
      {/* Header */}
      <div className="sticky top-0 z-30 bg-background/80 backdrop-blur-xl border-b border-white/5 px-4 py-3">
        <div className="flex items-center justify-between max-w-lg mx-auto">
          <button onClick={() => phase === 'hub' ? navigate(-1) : setPhase('hub')} className="p-2 rounded-full hover:bg-white/10 transition-all">
            <ArrowLeft className="h-5 w-5" />
          </button>
          <h1 className="text-lg font-bold flex items-center gap-2">
            <span className="text-xl">🎮</span>
            <span className="bg-gradient-to-r from-violet-400 to-pink-400 bg-clip-text text-transparent">{t('kidsZone')}</span>
          </h1>
          {phase === 'playing' ? (
            <div className={cn("px-3 py-1.5 rounded-full text-sm font-bold",
              timeLeft <= 5 ? "bg-red-500/20 text-red-400 animate-pulse" : "bg-white/10 text-foreground"
            )}>⏱ {timeLeft}s</div>
          ) : <div className="w-10" />}
        </div>
      </div>
      
      <div className="max-w-lg mx-auto px-4 pt-4">
        {/* Noor */}
        <div className="mb-4">
          <NoorMascot message={noorMsg} mood={noorMood} size="sm" autoSpeak={false} />
        </div>
        
        {/* Feedback flashes */}
        {showWrong && <div className="fixed inset-0 bg-red-500/10 z-50 pointer-events-none animate-pulse" />}
        {showCorrect && <div className="fixed inset-0 bg-green-500/10 z-50 pointer-events-none" />}
        
        {phase === 'hub' && renderHub()}
        {phase === 'loading' && (
          <div className="flex flex-col items-center justify-center py-16">
            <div className="w-14 h-14 border-4 border-violet-500 border-t-transparent rounded-full animate-spin" />
            <p className="text-sm text-muted-foreground mt-4 animate-pulse">{t('loading')}...</p>
          </div>
        )}
        {phase === 'playing' && gameData?.game_type === 'letter_maze' && renderLetterMaze()}
        {phase === 'playing' && gameData?.game_type === 'word_match' && renderWordMatch()}
        {phase === 'playing' && gameData?.game_type === 'tajweed_puzzle' && renderTajweed()}
        {phase === 'playing' && gameData?.game_type === 'pronunciation' && renderPronunciation()}
        {phase === 'result' && renderResult()}
        {phase === 'mosque' && renderMosqueDetail()}
        {phase === 'skills' && renderSkillsMap()}
      </div>
    </div>
  );
}
