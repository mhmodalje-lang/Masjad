import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import NoorMascot, { useNoorTTS, getNoorMessage } from '@/components/NoorMascot';
import { Star, Trophy, Mic, MicOff, Volume2, Sparkles, ArrowLeft, Gamepad2, RefreshCw, Zap, Brain, BookOpen, MessageSquare, Check, X, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

// ======== TYPES ========
type GameType = 'letter_maze' | 'word_match' | 'tajweed_puzzle' | 'pronunciation';
type GamePhase = 'menu' | 'loading' | 'playing' | 'result' | 'mosque';

interface GameData {
  game_id: string;
  game_type: GameType;
  difficulty: string;
  time_limit: number;
  brick_reward: number;
  xp_reward: number;
  [key: string]: any;
}

interface GameResult {
  xp_earned: number;
  bricks_earned: number;
  total_xp: number;
  total_bricks: number;
  difficulty: string;
  mosque_progress: any;
  weak_phonemes: number[];
  level_up: boolean;
}

interface MosqueStage {
  stage: number;
  name: string;
  bricks_needed: number;
  emoji: string;
}

// ======== NOOR GAME MESSAGES (10 languages) ========
const NOOR_GAME_MSG: Record<string, Record<string, string>> = {
  gameStart: {
    ar: 'هيا نلعب! اختر لعبة ممتعة! 🎮', en: "Let's play! Pick a fun game! 🎮",
    de: 'Los geht\'s! Wähle ein lustiges Spiel! 🎮', 'de-AT': 'Auf geht\'s! Such dir ein Spiel aus! 🎮',
    fr: 'Jouons! Choisis un jeu amusant! 🎮', tr: 'Hadi oynayalım! Eğlenceli bir oyun seç! 🎮',
    ru: 'Давай играть! Выбери весёлую игру! 🎮', sv: 'Nu spelar vi! Välj ett roligt spel! 🎮',
    nl: 'Laten we spelen! Kies een leuk spel! 🎮', el: 'Πάμε να παίξουμε! Διάλεξε παιχνίδι! 🎮',
  },
  brickEarned: {
    ar: 'حصلت على طوبة ذهبية! 🧱✨', en: 'You earned a Golden Brick! 🧱✨',
    de: 'Du hast einen goldenen Ziegel verdient! 🧱✨', 'de-AT': 'Du hast an goldenen Ziegel gschafft! 🧱✨',
    fr: 'Tu as gagné une Brique Dorée! 🧱✨', tr: 'Altın Tuğla kazandın! 🧱✨',
    ru: 'Ты получил Золотой Кирпич! 🧱✨', sv: 'Du fick en Gyllene Tegelsten! 🧱✨',
    nl: 'Je hebt een Gouden Steen verdiend! 🧱✨', el: 'Κέρδισες ένα Χρυσό Τούβλο! 🧱✨',
  },
  tryAgain: {
    ar: 'لا بأس! المحاولة أهم شيء! 💪', en: 'No worries! Trying is what matters! 💪',
    de: 'Kein Problem! Versuchen ist wichtig! 💪', 'de-AT': 'Passt schon! Probieren is wichtig! 💪',
    fr: 'Pas grave! L\'important c\'est d\'essayer! 💪', tr: 'Olsun! Denemek önemli! 💪',
    ru: 'Ничего! Главное — пробовать! 💪', sv: 'Inga problem! Att försöka är viktigt! 💪',
    nl: 'Geen probleem! Proberen is belangrijk! 💪', el: 'Δεν πειράζει! Η προσπάθεια μετράει! 💪',
  },
  speakNow: {
    ar: 'أنصت جيداً ثم انطق الكلمة! 🎤', en: 'Listen carefully then say the word! 🎤',
    de: 'Hör gut zu und sag das Wort! 🎤', 'de-AT': 'Hör gut zua und sag\'s Wort! 🎤',
    fr: 'Écoute bien puis dis le mot! 🎤', tr: 'İyi dinle sonra kelimeyi söyle! 🎤',
    ru: 'Слушай внимательно и скажи слово! 🎤', sv: 'Lyssna noga och säg ordet! 🎤',
    nl: 'Luister goed en zeg het woord! 🎤', el: 'Άκου προσεκτικά και πες τη λέξη! 🎤',
  },
  mosqueGrow: {
    ar: 'مسجدك يكبر! استمر في البناء! 🕌', en: 'Your mosque is growing! Keep building! 🕌',
    de: 'Deine Moschee wächst! Weiterbauen! 🕌', 'de-AT': 'Dei Moschee wachst! Weiterbauen! 🕌',
    fr: 'Ta mosquée grandit! Continue! 🕌', tr: 'Camin büyüyor! İnşaata devam! 🕌',
    ru: 'Твоя мечеть растёт! Строй дальше! 🕌', sv: 'Din moské växer! Fortsätt bygga! 🕌',
    nl: 'Je moskee groeit! Blijf bouwen! 🕌', el: 'Το τζαμί σου μεγαλώνει! Συνέχισε! 🕌',
  },
};

const getGameMsg = (key: string, locale: string): string => {
  return NOOR_GAME_MSG[key]?.[locale] || NOOR_GAME_MSG[key]?.['en'] || '';
};

// ======== GAME TYPE CONFIG ========
const GAME_TYPES: { type: GameType; icon: string; labelKey: string }[] = [
  { type: 'letter_maze', icon: '🔤', labelKey: 'kidsLetterMaze' },
  { type: 'word_match', icon: '🔗', labelKey: 'kidsWordMatch' },
  { type: 'tajweed_puzzle', icon: '📖', labelKey: 'kidsTajweedPuzzle' },
  { type: 'pronunciation', icon: '🎤', labelKey: 'kidsPronunciation' },
];

// ======== DIFFICULTY COLORS ========
const TIER_COLORS: Record<string, string> = {
  seedling: 'from-green-400 to-green-600',
  sprout: 'from-blue-400 to-blue-600',
  sapling: 'from-purple-400 to-purple-600',
  tree: 'from-amber-400 to-amber-600',
  forest: 'from-red-400 to-red-600',
};

// ======== MOSQUE SVG BUILDER ========
function VirtualMosque({ stage, progress, bricks }: { stage: any; progress: number; bricks: number }) {
  const stageNum = stage?.stage || 1;
  
  return (
    <div className="relative w-full max-w-xs mx-auto">
      <svg viewBox="0 0 200 180" className="w-full">
        {/* Ground */}
        <rect x="0" y="150" width="200" height="30" fill="#8B7355" rx="4" opacity="0.3" />
        
        {/* Foundation - always visible */}
        <rect x="30" y="130" width="140" height="20" fill="#D4A574" stroke="#B8956A" strokeWidth="1" rx="2">
          <animate attributeName="opacity" values={stageNum >= 1 ? "0.5;1;0.5" : "0.2"} dur="3s" repeatCount="indefinite" />
        </rect>
        
        {/* Walls */}
        {stageNum >= 2 && (
          <g>
            <rect x="40" y="70" width="120" height="60" fill="#E8D5B7" stroke="#C4A882" strokeWidth="1" rx="2" />
            <rect x="85" y="100" width="30" height="30" fill="#8B6914" rx="4" /> {/* Door */}
            <rect x="55" y="80" width="15" height="20" fill="#87CEEB" rx="2" opacity="0.7" /> {/* Window */}
            <rect x="130" y="80" width="15" height="20" fill="#87CEEB" rx="2" opacity="0.7" /> {/* Window */}
          </g>
        )}
        
        {/* Dome */}
        {stageNum >= 3 && (
          <ellipse cx="100" cy="70" rx="45" ry="30" fill="#4A90D9" stroke="#3A7BC8" strokeWidth="1">
            <animate attributeName="fill" values="#4A90D9;#5AA0E9;#4A90D9" dur="4s" repeatCount="indefinite" />
          </ellipse>
        )}
        
        {/* Minaret */}
        {stageNum >= 4 && (
          <g>
            <rect x="165" y="30" width="12" height="100" fill="#E8D5B7" stroke="#C4A882" strokeWidth="1" />
            <ellipse cx="171" cy="30" rx="8" ry="6" fill="#4A90D9" />
            <line x1="171" y1="24" x2="171" y2="14" stroke="#FFD700" strokeWidth="2" />
            <circle cx="171" cy="12" r="3" fill="#FFD700" />
          </g>
        )}
        
        {/* Garden */}
        {stageNum >= 5 && (
          <g>
            <circle cx="20" cy="145" r="8" fill="#228B22" opacity="0.8" />
            <circle cx="15" cy="140" r="6" fill="#32CD32" opacity="0.6" />
            <circle cx="185" cy="145" r="8" fill="#228B22" opacity="0.8" />
            <circle cx="180" cy="140" r="6" fill="#32CD32" opacity="0.6" />
          </g>
        )}
        
        {/* Golden Dome */}
        {stageNum >= 6 && (
          <g>
            <ellipse cx="100" cy="68" rx="43" ry="28" fill="#FFD700" opacity="0.7">
              <animate attributeName="opacity" values="0.5;0.9;0.5" dur="2s" repeatCount="indefinite" />
            </ellipse>
            <line x1="100" y1="40" x2="100" y2="28" stroke="#FFD700" strokeWidth="2" />
            <circle cx="100" cy="26" r="4" fill="#FFD700">
              <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite" />
            </circle>
          </g>
        )}
      </svg>
      
      {/* Brick counter */}
      <div className="text-center mt-1">
        <span className="text-xs font-bold text-amber-500">🧱 {bricks}</span>
        <div className="w-full bg-muted rounded-full h-2 mt-1">
          <div
            className="bg-gradient-to-r from-amber-400 to-amber-600 h-2 rounded-full transition-all duration-700"
            style={{ width: `${Math.min(100, progress)}%` }}
          />
        </div>
      </div>
    </div>
  );
}

// ======== AUDIO WAVEFORM VISUALIZER ========
function AudioWaveform({ isActive, accuracy }: { isActive: boolean; accuracy: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    if (!isActive) {
      if (animRef.current) cancelAnimationFrame(animRef.current);
      if (streamRef.current) streamRef.current.getTracks().forEach(t => t.stop());
      return;
    }
    
    let mounted = true;
    const start = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        if (!mounted) { stream.getTracks().forEach(t => t.stop()); return; }
        streamRef.current = stream;
        const audioCtx = new AudioContext();
        const src = audioCtx.createMediaStreamSource(stream);
        const analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        src.connect(analyser);
        analyserRef.current = analyser;
        draw();
      } catch { /* mic not available */ }
    };
    
    const draw = () => {
      const canvas = canvasRef.current;
      const analyser = analyserRef.current;
      if (!canvas || !analyser || !mounted) return;
      
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      const bufLen = analyser.frequencyBinCount;
      const data = new Uint8Array(bufLen);
      analyser.getByteFrequencyData(data);
      
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);
      
      const barW = (w / bufLen) * 2.5;
      let x = 0;
      for (let i = 0; i < bufLen; i++) {
        const barH = (data[i] / 255) * h;
        const hue = accuracy > 85 ? 120 : accuracy > 60 ? 60 : 0; // green/yellow/red
        ctx.fillStyle = `hsla(${hue}, 80%, 55%, 0.8)`;
        ctx.fillRect(x, h - barH, barW, barH);
        x += barW + 1;
      }
      
      animRef.current = requestAnimationFrame(draw);
    };
    
    start();
    return () => {
      mounted = false;
      if (animRef.current) cancelAnimationFrame(animRef.current);
      if (streamRef.current) streamRef.current.getTracks().forEach(t => t.stop());
    };
  }, [isActive, accuracy]);
  
  return (
    <div className="relative w-full h-16 rounded-xl overflow-hidden bg-black/10 border border-border/50">
      <canvas ref={canvasRef} width={300} height={64} className="w-full h-full" />
      {/* Star fill overlay based on accuracy */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="relative w-12 h-12">
          <Star className={cn("w-12 h-12 transition-all duration-500", accuracy > 85 ? "text-amber-400 fill-amber-400" : accuracy > 60 ? "text-amber-300 fill-amber-300/50" : "text-muted-foreground")} />
          <div
            className="absolute bottom-0 left-0 right-0 bg-amber-400/40 transition-all duration-300 rounded-b"
            style={{ height: `${Math.min(100, accuracy)}%` }}
          />
        </div>
      </div>
    </div>
  );
}

// ======== MAIN KIDS ZONE COMPONENT ========
export default function KidsZone() {
  const { t, dir, locale } = useLocale();
  const navigate = useNavigate();
  const { speak } = useNoorTTS();
  
  const [phase, setPhase] = useState<GamePhase>('menu');
  const [gameData, setGameData] = useState<GameData | null>(null);
  const [gameResult, setGameResult] = useState<GameResult | null>(null);
  const [progress, setProgress] = useState<any>(null);
  const [selectedType, setSelectedType] = useState<GameType | null>(null);
  const [noorMsg, setNoorMsg] = useState('');
  const [noorMood, setNoorMood] = useState<'happy' | 'thinking' | 'celebrating' | 'greeting'>('greeting');
  const [userId] = useState(() => localStorage.getItem('kids_user_id') || `kid_${Date.now()}`);
  
  // Game-specific state
  const [selectedCell, setSelectedCell] = useState<number | null>(null);
  const [matchedPairs, setMatchedPairs] = useState<Set<number>>(new Set());
  const [selectedWord, setSelectedWord] = useState<number | null>(null);
  const [selectedMeaning, setSelectedMeaning] = useState<number | null>(null);
  const [tajweedAnswer, setTajweedAnswer] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [speechResult, setSpeechResult] = useState('');
  const [pronAccuracy, setPronAccuracy] = useState(0);
  const [timeLeft, setTimeLeft] = useState(0);
  const [gameScore, setGameScore] = useState(0);
  const [showCorrectFeedback, setShowCorrectFeedback] = useState(false);
  const [showWrongFeedback, setShowWrongFeedback] = useState(false);
  
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const recognitionRef = useRef<any>(null);

  // Persist userId
  useEffect(() => {
    localStorage.setItem('kids_user_id', userId);
  }, [userId]);

  // Load progress on mount
  useEffect(() => {
    loadProgress();
    setNoorMsg(getGameMsg('gameStart', locale));
  }, [locale]);

  const loadProgress = useCallback(async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/api/kids-zone/progress?user_id=${userId}`);
      const data = await res.json();
      if (data.success) setProgress(data);
    } catch { /* offline fallback */ }
  }, [userId]);

  // Timer
  useEffect(() => {
    if (phase === 'playing' && timeLeft > 0) {
      timerRef.current = setTimeout(() => setTimeLeft(t => t - 1), 1000);
      return () => { if (timerRef.current) clearTimeout(timerRef.current); };
    }
    if (phase === 'playing' && timeLeft === 0 && gameData) {
      handleGameEnd(false, gameScore);
    }
  }, [phase, timeLeft]);

  // Fetch new game
  const startGame = useCallback(async (type: GameType) => {
    setPhase('loading');
    setSelectedType(type);
    setNoorMsg(getGameMsg('gameStart', locale));
    setNoorMood('thinking');
    
    try {
      const res = await fetch(`${BACKEND_URL}/api/kids-zone/generate-game?user_id=${userId}&game_type=${type}&locale=${locale}`);
      const data = await res.json();
      if (data.success) {
        setGameData(data.game);
        setPhase('playing');
        setTimeLeft(data.game.time_limit);
        setGameScore(0);
        setMatchedPairs(new Set());
        setSelectedWord(null);
        setSelectedMeaning(null);
        setTajweedAnswer(null);
        setSpeechResult('');
        setPronAccuracy(0);
        setShowCorrectFeedback(false);
        setShowWrongFeedback(false);
        setNoorMood('happy');
        
        if (type === 'pronunciation') {
          setNoorMsg(getGameMsg('speakNow', locale));
        }
      }
    } catch {
      toast.error('Could not load game');
      setPhase('menu');
    }
  }, [userId, locale]);

  // Submit game result
  const handleGameEnd = useCallback(async (correct: boolean, score: number) => {
    if (timerRef.current) clearTimeout(timerRef.current);
    setPhase('result');
    
    const phonemes = gameData?.target_letter ? [gameData.target_letter.id] : 
                     gameData?.letter_id ? [gameData.letter_id] : [];
    
    try {
      const res = await fetch(`${BACKEND_URL}/api/kids-zone/submit-result`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          game_type: gameData?.game_type,
          correct,
          score: score || gameScore,
          phonemes_tested: phonemes,
          pronunciation_accuracy: pronAccuracy,
          game_id: gameData?.game_id,
        }),
      });
      const data = await res.json();
      if (data.success) {
        setGameResult(data);
        if (correct) {
          setNoorMsg(getGameMsg('brickEarned', locale));
          setNoorMood('celebrating');
          speak(getNoorMessage('correct', locale));
        } else {
          setNoorMsg(getGameMsg('tryAgain', locale));
          setNoorMood('happy');
          speak(getNoorMessage('encourage', locale));
        }
        loadProgress();
      }
    } catch { /* offline */ }
  }, [gameData, gameScore, pronAccuracy, userId, locale, speak, loadProgress]);

  // ========== LETTER MAZE GAME ==========
  const renderLetterMaze = () => {
    if (!gameData?.grid) return null;
    const target = gameData.target_letter;
    
    return (
      <div className="space-y-4">
        {/* Target display */}
        <div className="text-center p-4 rounded-2xl bg-gradient-to-r from-primary/20 to-primary/10 border border-primary/30">
          <p className="text-sm text-muted-foreground mb-1">{t('kidsFind')}</p>
          <div className="flex items-center justify-center gap-3">
            <span className="text-5xl font-bold text-primary">{target.letter}</span>
            <div className="text-start">
              <p className="text-lg font-bold">{target.name_ar}</p>
              <p className="text-xs text-muted-foreground">{target.transliteration} • {target.audio_hint}</p>
            </div>
          </div>
          {gameData.confusable && (
            <p className="text-xs text-amber-500 mt-2">
              ⚠️ {t('kidsConfusable')}: <span className="text-lg font-bold">{gameData.confusable.letter}</span>
            </p>
          )}
        </div>
        
        {/* Grid */}
        <div
          className="grid gap-2 max-w-xs mx-auto"
          style={{ gridTemplateColumns: `repeat(${gameData.grid_size}, 1fr)` }}
        >
          {gameData.grid.flat().map((cell: any, idx: number) => (
            <button
              key={idx}
              onClick={() => {
                if (cell.is_target) {
                  setShowCorrectFeedback(true);
                  setGameScore(s => s + gameData.xp_reward);
                  speak(getNoorMessage('correct', locale));
                  setTimeout(() => handleGameEnd(true, gameData.xp_reward), 1200);
                } else {
                  setShowWrongFeedback(true);
                  speak(getNoorMessage('wrong', locale));
                  setTimeout(() => setShowWrongFeedback(false), 800);
                }
              }}
              className={cn(
                "aspect-square rounded-xl text-3xl font-bold flex items-center justify-center",
                "border-2 transition-all duration-200 active:scale-95",
                showCorrectFeedback && cell.is_target
                  ? "bg-green-500/30 border-green-500 scale-110"
                  : "bg-card border-border/50 hover:border-primary/50 hover:bg-primary/5"
              )}
            >
              {cell.letter}
            </button>
          ))}
        </div>
        
        {/* Hint */}
        <div className="text-center">
          <button
            onClick={() => speak(target.audio_hint, 'ar')}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm"
          >
            <Volume2 className="h-4 w-4" /> {t('kidsListenHint')}
          </button>
        </div>
      </div>
    );
  };

  // ========== WORD MATCH GAME ==========
  const renderWordMatch = () => {
    if (!gameData?.words) return null;
    
    const handleWordClick = (idx: number) => {
      if (matchedPairs.has(idx)) return;
      setSelectedWord(idx);
      if (selectedMeaning !== null) checkMatch(idx, selectedMeaning);
    };
    
    const handleMeaningClick = (idx: number) => {
      if (matchedPairs.has(idx)) return;
      setSelectedMeaning(idx);
      if (selectedWord !== null) checkMatch(selectedWord, idx);
    };
    
    const checkMatch = (wIdx: number, mIdx: number) => {
      const word = gameData.words[wIdx];
      const meaning = gameData.meanings[mIdx];
      if (word.id === meaning.id) {
        const newMatched = new Set(matchedPairs);
        newMatched.add(wIdx);
        setMatchedPairs(newMatched);
        setGameScore(s => s + 5);
        speak(getNoorMessage('correct', locale));
        
        if (newMatched.size === gameData.words.length) {
          setTimeout(() => handleGameEnd(true, (newMatched.size * 5) + gameData.xp_reward), 800);
        }
      } else {
        setShowWrongFeedback(true);
        setTimeout(() => setShowWrongFeedback(false), 600);
      }
      setSelectedWord(null);
      setSelectedMeaning(null);
    };
    
    return (
      <div className="space-y-4">
        <p className="text-center text-sm text-muted-foreground">{t('kidsMatchWords')}</p>
        
        <div className="grid grid-cols-2 gap-3">
          {/* Words column */}
          <div className="space-y-2">
            {gameData.words.map((w: any, i: number) => (
              <button
                key={`w-${i}`}
                onClick={() => handleWordClick(i)}
                disabled={matchedPairs.has(i)}
                className={cn(
                  "w-full p-3 rounded-xl border-2 text-center transition-all",
                  matchedPairs.has(i) ? "bg-green-500/20 border-green-500 opacity-60" :
                  selectedWord === i ? "bg-primary/20 border-primary scale-105" :
                  "bg-card border-border/50 hover:border-primary/30"
                )}
              >
                <span className="text-2xl font-bold">{w.word}</span>
                <p className="text-[10px] text-muted-foreground mt-1">{w.transliteration}</p>
              </button>
            ))}
          </div>
          
          {/* Meanings column */}
          <div className="space-y-2">
            {gameData.meanings.map((m: any, i: number) => (
              <button
                key={`m-${i}`}
                onClick={() => handleMeaningClick(i)}
                disabled={matchedPairs.has(gameData.words.findIndex((w: any) => w.id === m.id))}
                className={cn(
                  "w-full p-3 rounded-xl border-2 text-center transition-all",
                  matchedPairs.has(gameData.words.findIndex((w: any) => w.id === m.id)) ? "bg-green-500/20 border-green-500 opacity-60" :
                  selectedMeaning === i ? "bg-primary/20 border-primary scale-105" :
                  "bg-card border-border/50 hover:border-primary/30"
                )}
              >
                <span className="text-sm font-medium">{m.meaning}</span>
                <p className="text-[10px] text-muted-foreground mt-1">{m.surah}</p>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // ========== TAJWEED PUZZLE GAME ==========
  const renderTajweedPuzzle = () => {
    if (!gameData?.question_rule) return null;
    const rule = gameData.question_rule;
    
    return (
      <div className="space-y-4">
        {/* Question */}
        <div className="text-center p-4 rounded-2xl bg-gradient-to-r from-purple-500/20 to-purple-500/10 border border-purple-500/30">
          <p className="text-sm text-muted-foreground mb-2">{t('kidsTajweedQ')}</p>
          <p className="text-3xl font-bold text-purple-500 mb-1">{rule.example}</p>
          <p className="text-sm font-medium">{rule.name_ar} — {rule.name_en}</p>
        </div>
        
        <p className="text-sm text-center text-muted-foreground">{gameData.description}</p>
        
        {/* Choices */}
        <div className="space-y-2">
          {gameData.choices.map((choice: string, i: number) => {
            const isSelected = tajweedAnswer === choice;
            const isCorrect = choice === gameData.correct_answer;
            const showResult = tajweedAnswer !== null;
            
            return (
              <button
                key={i}
                onClick={() => {
                  if (tajweedAnswer) return;
                  setTajweedAnswer(choice);
                  if (isCorrect) {
                    setGameScore(s => s + gameData.xp_reward);
                    speak(getNoorMessage('correct', locale));
                    setTimeout(() => handleGameEnd(true, gameData.xp_reward), 1500);
                  } else {
                    speak(getNoorMessage('wrong', locale));
                    setTimeout(() => handleGameEnd(false, 0), 1500);
                  }
                }}
                className={cn(
                  "w-full p-4 rounded-xl border-2 text-start flex items-center gap-3 transition-all",
                  showResult && isCorrect ? "bg-green-500/20 border-green-500" :
                  showResult && isSelected && !isCorrect ? "bg-red-500/20 border-red-500" :
                  !showResult ? "bg-card border-border/50 hover:border-purple-500/50 hover:bg-purple-500/5" :
                  "bg-card border-border/30 opacity-50"
                )}
              >
                <span className="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-sm font-bold">
                  {String.fromCharCode(65 + i)}
                </span>
                <span className="font-medium capitalize">{choice.replace(/_/g, ' ')}</span>
                {showResult && isCorrect && <Check className="h-5 w-5 text-green-500 ms-auto" />}
                {showResult && isSelected && !isCorrect && <X className="h-5 w-5 text-red-500 ms-auto" />}
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  // ========== PRONUNCIATION GAME ==========
  const startListening = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      toast.error('Speech recognition not supported');
      return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.lang = 'ar-SA';
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 5;
    
    recognition.onresult = (event: any) => {
      const results: string[] = [];
      for (let i = 0; i < event.results[0].length; i++) {
        results.push(event.results[0][i].transcript.trim());
      }
      const spoken = results[0] || '';
      setSpeechResult(spoken);
      
      // Calculate accuracy based on similarity
      const target = gameData?.target_word || '';
      const targetClean = target.replace(/[\u064B-\u065F\u0670]/g, ''); // Remove tashkeel
      const spokenClean = spoken.replace(/[\u064B-\u065F\u0670]/g, '');
      
      let acc = 0;
      if (spokenClean === targetClean) acc = 100;
      else if (targetClean.includes(spokenClean) || spokenClean.includes(targetClean)) acc = 80;
      else {
        // Simple character overlap
        const targetChars = new Set(targetClean.split(''));
        const spokenChars = new Set(spokenClean.split(''));
        let overlap = 0;
        targetChars.forEach(c => { if (spokenChars.has(c)) overlap++; });
        acc = Math.round((overlap / Math.max(targetChars.size, 1)) * 100);
      }
      
      setPronAccuracy(acc);
      setIsListening(false);
      
      const threshold = gameData?.accuracy_threshold || 85;
      if (acc >= threshold) {
        setGameScore(s => s + gameData!.xp_reward);
        setTimeout(() => handleGameEnd(true, gameData!.xp_reward), 1500);
      }
    };
    
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    
    recognitionRef.current = recognition;
    recognition.start();
    setIsListening(true);
    setSpeechResult('');
    setPronAccuracy(0);
  }, [gameData, handleGameEnd]);

  const renderPronunciation = () => {
    if (!gameData?.target_word) return null;
    const threshold = gameData.accuracy_threshold || 85;
    
    return (
      <div className="space-y-4">
        {/* Target word */}
        <div className="text-center p-6 rounded-2xl bg-gradient-to-r from-pink-500/20 to-pink-500/10 border border-pink-500/30">
          <p className="text-sm text-muted-foreground mb-2">{t('kidsSayWord')}</p>
          <p className="text-5xl font-bold text-pink-500 mb-2">{gameData.target_word}</p>
          <p className="text-lg text-muted-foreground">{gameData.transliteration}</p>
          <p className="text-sm text-foreground/70 mt-1">{gameData.meaning}</p>
          {gameData.source === 'quran' && (
            <span className="inline-block mt-2 text-xs bg-amber-500/20 text-amber-600 px-2 py-1 rounded-full">
              📖 {t('kidsFromQuran')}
            </span>
          )}
        </div>
        
        {/* Waveform */}
        <AudioWaveform isActive={isListening} accuracy={pronAccuracy} />
        
        {/* Listen/Speak buttons */}
        <div className="flex gap-3">
          <button
            onClick={() => speak(gameData.target_word, 'ar')}
            className="flex-1 py-3 rounded-xl bg-primary/10 text-primary flex items-center justify-center gap-2 border border-primary/20"
          >
            <Volume2 className="h-5 w-5" /> {t('kidsListen')}
          </button>
          
          <button
            onClick={isListening ? () => { recognitionRef.current?.stop(); setIsListening(false); } : startListening}
            className={cn(
              "flex-1 py-3 rounded-xl flex items-center justify-center gap-2 border transition-all",
              isListening
                ? "bg-red-500/20 text-red-500 border-red-500/30 animate-pulse"
                : "bg-pink-500/10 text-pink-500 border-pink-500/20"
            )}
          >
            {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
            {isListening ? t('kidsStop') : t('kidsSpeak')}
          </button>
        </div>
        
        {/* Result display */}
        {speechResult && (
          <div className={cn(
            "p-4 rounded-xl border-2 text-center transition-all",
            pronAccuracy >= threshold ? "bg-green-500/10 border-green-500" : "bg-amber-500/10 border-amber-500"
          )}>
            <p className="text-sm text-muted-foreground">{t('kidsYouSaid')}:</p>
            <p className="text-2xl font-bold mt-1">{speechResult}</p>
            <div className="flex items-center justify-center gap-2 mt-2">
              <Star className={cn("h-5 w-5", pronAccuracy >= threshold ? "text-amber-400 fill-amber-400" : "text-muted-foreground")} />
              <span className="text-lg font-bold">{pronAccuracy}%</span>
              {pronAccuracy >= threshold ? (
                <span className="text-green-500 text-sm font-bold">{t('kidsExcellent')}</span>
              ) : (
                <span className="text-amber-500 text-sm">{t('kidsTryAgain')}</span>
              )}
            </div>
          </div>
        )}
        
        {/* Try again button for failed pronunciation */}
        {speechResult && pronAccuracy < threshold && (
          <button
            onClick={() => { setSpeechResult(''); setPronAccuracy(0); }}
            className="w-full py-3 rounded-xl bg-primary text-primary-foreground flex items-center justify-center gap-2"
          >
            <RefreshCw className="h-4 w-4" /> {t('kidsTryAgain')}
          </button>
        )}
      </div>
    );
  };

  // ========== RESULT SCREEN ==========
  const renderResult = () => {
    if (!gameResult) return null;
    
    return (
      <div className="space-y-4 text-center">
        <div className={cn(
          "text-6xl mb-2",
          gameResult.bricks_earned > 0 ? "animate-bounce" : ""
        )}>
          {gameResult.bricks_earned > 0 ? '🎉' : '💪'}
        </div>
        
        <h2 className="text-xl font-bold">
          {gameResult.bricks_earned > 0 ? t('kidsWellDone') : t('kidsKeepTrying')}
        </h2>
        
        {/* Rewards */}
        <div className="flex justify-center gap-4">
          <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30">
            <Zap className="h-6 w-6 text-amber-500 mx-auto" />
            <p className="text-lg font-bold text-amber-500">+{gameResult.xp_earned}</p>
            <p className="text-[10px] text-muted-foreground">XP</p>
          </div>
          <div className="p-3 rounded-xl bg-orange-500/10 border border-orange-500/30">
            <span className="text-2xl">🧱</span>
            <p className="text-lg font-bold text-orange-500">+{gameResult.bricks_earned}</p>
            <p className="text-[10px] text-muted-foreground">{t('kidsBricks')}</p>
          </div>
        </div>
        
        {/* Level up notification */}
        {gameResult.level_up && (
          <div className="p-3 rounded-xl bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 animate-pulse">
            <Trophy className="h-8 w-8 text-purple-500 mx-auto mb-1" />
            <p className="font-bold text-purple-500">{t('kidsLevelUp')}: {gameResult.difficulty}</p>
          </div>
        )}
        
        {/* Mosque progress */}
        {gameResult.mosque_progress && (
          <VirtualMosque
            stage={gameResult.mosque_progress.current_stage}
            progress={gameResult.mosque_progress.progress_pct}
            bricks={gameResult.total_bricks}
          />
        )}
        
        {/* Action buttons */}
        <div className="flex gap-3 pt-2">
          <button
            onClick={() => startGame(selectedType || 'letter_maze')}
            className="flex-1 py-3 rounded-xl bg-primary text-primary-foreground flex items-center justify-center gap-2"
          >
            <RefreshCw className="h-4 w-4" /> {t('kidsPlayAgain')}
          </button>
          <button
            onClick={() => { setPhase('menu'); setGameData(null); setGameResult(null); }}
            className="flex-1 py-3 rounded-xl bg-muted text-foreground flex items-center justify-center gap-2 border border-border/50"
          >
            {t('kidsBackToMenu')}
          </button>
        </div>
      </div>
    );
  };

  // ========== MENU SCREEN ==========
  const renderMenu = () => {
    const tier = progress?.profile?.difficulty || 'seedling';
    const xp = progress?.profile?.total_xp || 0;
    const bricks = progress?.profile?.golden_bricks || 0;
    const gamesPlayed = progress?.profile?.games_played || 0;
    
    return (
      <div className="space-y-4">
        {/* Stats bar */}
        <div className="flex items-center justify-between p-3 rounded-2xl bg-gradient-to-r from-primary/10 to-primary/5 border border-primary/20">
          <div className="flex items-center gap-2">
            <Zap className="h-4 w-4 text-amber-500" />
            <span className="text-sm font-bold">{xp} XP</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm">🧱</span>
            <span className="text-sm font-bold">{bricks}</span>
          </div>
          <div className="flex items-center gap-1">
            <Gamepad2 className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">{gamesPlayed}</span>
          </div>
          <span className={cn(
            "text-xs font-bold px-2 py-1 rounded-full bg-gradient-to-r text-white",
            TIER_COLORS[tier] || TIER_COLORS.seedling
          )}>
            {t(`kidsTier_${tier}`)}
          </span>
        </div>
        
        {/* Virtual Mosque Preview */}
        {progress?.mosque && (
          <button onClick={() => setPhase('mosque')} className="w-full">
            <div className="rounded-2xl bg-card border border-border/50 p-3 hover:border-primary/30 transition-all">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-bold flex items-center gap-2">🕌 {t('kidsMyMosque')}</h3>
                <ChevronRight className="h-4 w-4 text-muted-foreground" />
              </div>
              <VirtualMosque
                stage={progress.mosque.current_stage}
                progress={progress.mosque.progress_pct}
                bricks={bricks}
              />
            </div>
          </button>
        )}
        
        {/* Game Selection */}
        <h3 className="text-lg font-bold">{t('kidsChooseGame')}</h3>
        <div className="grid grid-cols-2 gap-3">
          {GAME_TYPES.map(g => (
            <button
              key={g.type}
              onClick={() => startGame(g.type)}
              className="p-4 rounded-2xl bg-card border-2 border-border/50 hover:border-primary/50 hover:bg-primary/5 transition-all active:scale-95 text-center"
            >
              <span className="text-3xl block mb-2">{g.icon}</span>
              <p className="text-sm font-bold">{t(g.labelKey)}</p>
            </button>
          ))}
        </div>
        
        {/* Auto-play: AI picks best game */}
        <button
          onClick={() => startGame('letter_maze')}
          className="w-full py-4 rounded-2xl bg-gradient-to-r from-primary to-primary/80 text-primary-foreground flex items-center justify-center gap-2 font-bold shadow-lg"
        >
          <Sparkles className="h-5 w-5" /> {t('kidsAutoPlay')}
        </button>
        
        {/* Weak phonemes indicator */}
        {progress?.profile?.weak_phonemes?.length > 0 && (
          <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
            <p className="text-xs text-amber-600 font-medium mb-2">{t('kidsWeakAreas')}:</p>
            <div className="flex gap-2 flex-wrap">
              {progress.profile.weak_phonemes.slice(0, 6).map((pid: number) => {
                const letter = progress.letter_skills?.find((l: any) => l.id === pid);
                return letter ? (
                  <span key={pid} className="text-lg bg-amber-500/20 px-2 py-1 rounded-lg">{letter.letter}</span>
                ) : null;
              })}
            </div>
          </div>
        )}
      </div>
    );
  };

  // ========== MOSQUE VIEW ==========
  const renderMosqueView = () => {
    const mosque = progress?.mosque;
    if (!mosque) return null;
    
    return (
      <div className="space-y-4 text-center">
        <h2 className="text-xl font-bold">{t('kidsMyMosque')}</h2>
        <VirtualMosque stage={mosque.current_stage} progress={mosque.progress_pct} bricks={progress.profile.golden_bricks} />
        
        <div className="text-sm text-muted-foreground">
          {mosque.current_stage.emoji} {t('kidsStage')}: <span className="font-bold capitalize">{mosque.current_stage.name}</span>
        </div>
        
        {mosque.next_stage && (
          <div className="p-3 rounded-xl bg-primary/5 border border-primary/20">
            <p className="text-xs text-muted-foreground">{t('kidsNextStage')}:</p>
            <p className="font-bold">{mosque.next_stage.emoji} {mosque.next_stage.name}</p>
            <p className="text-sm text-amber-500">🧱 {mosque.bricks_to_next} {t('kidsBricksNeeded')}</p>
          </div>
        )}
        
        {/* All stages progress */}
        <div className="space-y-2">
          {mosque.stages.map((s: MosqueStage) => (
            <div key={s.stage} className="flex items-center gap-3 px-3 py-2 rounded-xl bg-card border border-border/30">
              <span className="text-xl">{s.emoji}</span>
              <div className="flex-1 text-start">
                <p className="text-sm font-medium capitalize">{s.name}</p>
                <p className="text-[10px] text-muted-foreground">{s.bricks_needed} {t('kidsBricks')}</p>
              </div>
              {progress.profile.golden_bricks >= s.bricks_needed ? (
                <Check className="h-5 w-5 text-green-500" />
              ) : (
                <span className="text-xs text-muted-foreground">{s.bricks_needed - progress.profile.golden_bricks}</span>
              )}
            </div>
          ))}
        </div>
        
        <button
          onClick={() => setPhase('menu')}
          className="w-full py-3 rounded-xl bg-primary text-primary-foreground"
        >
          {t('kidsBackToMenu')}
        </button>
      </div>
    );
  };

  return (
    <div dir={dir} className="min-h-screen bg-background pb-24">
      {/* Header */}
      <div className="sticky top-0 z-30 bg-background/95 backdrop-blur border-b border-border/50 px-4 py-3">
        <div className="flex items-center justify-between max-w-lg mx-auto">
          <button onClick={() => phase === 'menu' ? navigate(-1) : setPhase('menu')} className="p-2 rounded-full hover:bg-muted">
            <ArrowLeft className="h-5 w-5" />
          </button>
          <h1 className="text-lg font-bold flex items-center gap-2">
            <Gamepad2 className="h-5 w-5 text-primary" /> {t('kidsZone')}
          </h1>
          {phase === 'playing' && (
            <div className={cn(
              "px-3 py-1 rounded-full text-sm font-bold",
              timeLeft <= 5 ? "bg-red-500/20 text-red-500 animate-pulse" : "bg-muted text-foreground"
            )}>
              ⏱ {timeLeft}s
            </div>
          )}
          {phase !== 'playing' && <div className="w-10" />}
        </div>
      </div>
      
      <div className="max-w-lg mx-auto px-4 pt-4">
        {/* Noor Mascot */}
        <div className="mb-4">
          <NoorMascot message={noorMsg} mood={noorMood} size="sm" autoSpeak={false} />
        </div>
        
        {/* Wrong feedback flash */}
        {showWrongFeedback && (
          <div className="fixed inset-0 bg-red-500/10 z-50 pointer-events-none animate-pulse" />
        )}
        {showCorrectFeedback && (
          <div className="fixed inset-0 bg-green-500/10 z-50 pointer-events-none animate-pulse" />
        )}
        
        {/* Phase renderer */}
        {phase === 'menu' && renderMenu()}
        {phase === 'loading' && (
          <div className="flex flex-col items-center justify-center py-12">
            <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
            <p className="text-sm text-muted-foreground mt-4">{t('loading')}</p>
          </div>
        )}
        {phase === 'playing' && gameData?.game_type === 'letter_maze' && renderLetterMaze()}
        {phase === 'playing' && gameData?.game_type === 'word_match' && renderWordMatch()}
        {phase === 'playing' && gameData?.game_type === 'tajweed_puzzle' && renderTajweedPuzzle()}
        {phase === 'playing' && gameData?.game_type === 'pronunciation' && renderPronunciation()}
        {phase === 'result' && renderResult()}
        {phase === 'mosque' && renderMosqueView()}
      </div>
    </div>
  );
}
