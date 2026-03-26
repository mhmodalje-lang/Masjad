import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Star, Flame, Trophy, ChevronRight, ChevronLeft, Shield, BookOpen,
  Lock, Play, Zap, Gift, ArrowLeft, Sparkles, Crown, CheckCircle,
  Volume2, GraduationCap, Globe, Heart,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import QuizGame from '@/components/games/QuizGame';
import MemoryGame from '@/components/games/MemoryGame';
import DragDropGame from '@/components/games/DragDropGame';
import ScenarioGame from '@/components/games/ScenarioGame';

const API = import.meta.env.REACT_APP_BACKEND_URL || '';

// ═══════ TYPES ═══════
interface GameData { type: string; id: string; title: string; emoji: string; xp: number; [k: string]: any; }
interface DailyGames { day: number; total_xp: number; games: GameData[]; games_count: number; }
interface KidProfile { user_id: string; total_xp: number; level: number; streak_days: number; games_completed: number; coins: number; badges: string[]; }
interface ShieldLesson { id: string; theme: string; title: string; content: string; key_lesson: string; }
interface CourseLevel { id: string; name: string; emoji: string; color: string; desc: string; units_count: number; total_lessons: number; units: any[]; }
interface AlphabetLetter { index: number; letter: string; name: string; sound: string; forms: any; emoji: string; word_ar: string; word_en: string; word?: string; }
interface AcademyTrack { id: string; name: string; emoji: string; color: string; description: string; total_lessons: number; levels: any[]; }
interface AcademyOverview { academy_name: string; tracks: AcademyTrack[]; total_lessons: number; }
interface AcademyLesson { id: number; title: string; emoji: string; level: number; lesson: number; method: string; content: any; quiz: any; xp: number; has_next: boolean; has_prev: boolean; level_name?: string; }

type View = 'home' | 'play' | 'course' | 'course_detail' | 'letter_lesson' | 'shield' | 'profile' | 'academy' | 'academy_track' | 'academy_lesson';

const LEVEL_COLORS: Record<string, string> = {
  emerald: 'from-emerald-400 to-green-500', teal: 'from-teal-400 to-cyan-500',
  cyan: 'from-cyan-400 to-blue-500', blue: 'from-blue-400 to-indigo-500',
  indigo: 'from-indigo-400 to-purple-500', amber: 'from-amber-400 to-orange-500',
};
const LEVEL_BG: Record<string, string> = {
  emerald: 'bg-emerald-50 dark:bg-emerald-950/30', teal: 'bg-teal-50 dark:bg-teal-950/30',
  cyan: 'bg-cyan-50 dark:bg-cyan-950/30', blue: 'bg-blue-50 dark:bg-blue-950/30',
  indigo: 'bg-indigo-50 dark:bg-indigo-950/30', amber: 'bg-amber-50 dark:bg-amber-950/30',
};

export default function KidsZone() {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'en';
  const isRTL = ['ar'].includes(lang);

  const [view, setView] = useState<View>('home');
  const [dailyGames, setDailyGames] = useState<DailyGames | null>(null);
  const [profile, setProfile] = useState<KidProfile | null>(null);
  const [currentGameIdx, setCurrentGameIdx] = useState(0);
  const [completedGames, setCompletedGames] = useState<Set<string>>(new Set());
  const [earnedXP, setEarnedXP] = useState(0);
  const [loading, setLoading] = useState(false);
  const [showReward, setShowReward] = useState(false);

  // Course state
  const [courseLevels, setCourseLevels] = useState<CourseLevel[]>([]);
  const [selectedLevel, setSelectedLevel] = useState<CourseLevel | null>(null);
  const [alphabet, setAlphabet] = useState<AlphabetLetter[]>([]);
  const [currentLetterIdx, setCurrentLetterIdx] = useState(0);
  const [letterGames, setLetterGames] = useState<GameData[]>([]);
  const [letterGameIdx, setLetterGameIdx] = useState(0);
  const [showLetterInfo, setShowLetterInfo] = useState(true);

  // Shield state
  const [shieldLessons, setShieldLessons] = useState<ShieldLesson[]>([]);
  const [shieldFilter, setShieldFilter] = useState('all');
  const [expandedLesson, setExpandedLesson] = useState<string | null>(null);

  // Academy state
  const [academyOverview, setAcademyOverview] = useState<AcademyOverview | null>(null);
  const [selectedTrack, setSelectedTrack] = useState<AcademyTrack | null>(null);
  const [currentAcademyLesson, setCurrentAcademyLesson] = useState<AcademyLesson | null>(null);
  const [quizAnswer, setQuizAnswer] = useState<string | null>(null);
  const [quizSubmitted, setQuizSubmitted] = useState(false);

  const userId = useMemo(() => {
    let id = localStorage.getItem('kids_user_id');
    if (!id) { id = 'kid_' + Date.now().toString(36) + Math.random().toString(36).substring(2, 8); localStorage.setItem('kids_user_id', id); }
    return id;
  }, []);

  // ═══════ LOADERS ═══════
  const loadDailyGames = useCallback(async () => {
    try { const r = await fetch(`${API}/api/kids-learn/daily-games?locale=${lang}`); const d = await r.json(); if (d.success) setDailyGames(d); } catch {}
  }, [lang]);

  const loadProfile = useCallback(async () => {
    try { const r = await fetch(`${API}/api/kids-learn/profile/${userId}`); const d = await r.json(); if (d.success) setProfile(d.profile); } catch {}
  }, [userId]);

  const loadCourse = useCallback(async () => {
    try { const r = await fetch(`${API}/api/kids-learn/course/overview?locale=${lang}`); const d = await r.json(); if (d.success) setCourseLevels(d.levels); } catch {}
  }, [lang]);

  const loadAlphabet = useCallback(async () => {
    try { const r = await fetch(`${API}/api/kids-learn/course/alphabet?locale=${lang}`); const d = await r.json(); if (d.success) setAlphabet(d.letters); } catch {}
  }, [lang]);

  const loadLetterGames = useCallback(async (idx: number) => {
    try { const r = await fetch(`${API}/api/kids-learn/course/alphabet/${idx}?locale=${lang}`); const d = await r.json(); if (d.success) { setLetterGames(d.games); setLetterGameIdx(0); setShowLetterInfo(true); } } catch {}
  }, [lang]);

  const loadShield = useCallback(async () => {
    try { const r = await fetch(`${API}/api/kids-learn/digital-shield?locale=${lang}&theme=${shieldFilter}`); const d = await r.json(); if (d.success) setShieldLessons(d.lessons); } catch {}
  }, [lang, shieldFilter]);

  const loadAcademy = useCallback(async () => {
    try { const r = await fetch(`${API}/api/kids-learn/academy/overview?locale=${lang}`); const d = await r.json(); if (d.success) { 
      const tracks = (d.tracks || []).map((t: any) => ({
        id: t.id, name: t.title || t.name, emoji: t.emoji, color: t.color, 
        description: t.description, total_lessons: t.total_lessons || 0, 
        levels: new Array(t.total_levels || 0),
      }));
      setAcademyOverview({ academy_name: d.academy_name, tracks, total_lessons: d.total_lessons }); 
    }} catch {}
  }, [lang]);

  const loadTrack = useCallback(async (trackId: string) => {
    try { const r = await fetch(`${API}/api/kids-learn/academy/track/${trackId}?locale=${lang}`); const d = await r.json(); if (d.success) setSelectedTrack({ id: trackId, name: d.track_name, emoji: d.emoji, color: d.color, description: d.description, total_lessons: d.total_lessons, levels: d.levels }); } catch {}
  }, [lang]);

  const loadAcademyLesson = useCallback(async (trackId: string, lessonId: number) => {
    try { const r = await fetch(`${API}/api/kids-learn/academy/${trackId}/lesson/${lessonId}?locale=${lang}`); const d = await r.json(); if (d.success) { 
      const ls = d.lesson;
      setCurrentAcademyLesson({
        ...ls,
        lesson: ls.lesson_in_level || ls.lesson || lessonId,
        has_next: d.has_next ?? ls.has_next ?? true,
        has_prev: d.has_prev ?? ls.has_prev ?? (lessonId > 1),
        level_name: ls.level_title || ls.level_name || '',
      }); 
      setQuizAnswer(null); setQuizSubmitted(false); 
    } } catch {}
  }, [lang]);

  useEffect(() => { loadDailyGames(); loadProfile(); loadCourse(); loadAlphabet(); loadAcademy(); }, [loadDailyGames, loadProfile, loadCourse, loadAlphabet, loadAcademy]);
  useEffect(() => { if (view === 'shield') loadShield(); }, [view, shieldFilter, loadShield]);

  // ═══════ GAME HANDLERS ═══════
  const handleGameComplete = async (gameId: string, correct: boolean, xp: number) => {
    setCompletedGames(prev => new Set([...prev, gameId]));
    setEarnedXP(prev => prev + xp);
    try {
      await fetch(`${API}/api/kids-learn/game-result`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, game_id: gameId, day: dailyGames?.day || 0, score: correct ? 1 : 0, max_score: 1, xp_earned: xp, time_seconds: 0 }),
      });
      loadProfile();
    } catch {}
    if (dailyGames && currentGameIdx < dailyGames.games.length - 1) {
      setTimeout(() => setCurrentGameIdx(prev => prev + 1), 2500);
    } else if (dailyGames && currentGameIdx === dailyGames.games.length - 1) {
      setTimeout(() => setShowReward(true), 2500);
    }
  };

  const handleLetterGameComplete = async (gameId: string, correct: boolean, xp: number) => {
    setEarnedXP(prev => prev + xp);
    try {
      await fetch(`${API}/api/kids-learn/game-result`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, game_id: gameId, day: 0, score: correct ? 1 : 0, max_score: 1, xp_earned: xp, time_seconds: 0 }),
      });
      loadProfile();
    } catch {}
    if (letterGameIdx < letterGames.length - 1) {
      setTimeout(() => setLetterGameIdx(prev => prev + 1), 2500);
    } else {
      setTimeout(() => {
        if (currentLetterIdx < alphabet.length - 1) {
          toast.success(`✨ ${t('letterComplete')} ${t('earnedPoints').replace('{xp}', String(xp))}`);
          setCurrentLetterIdx(prev => prev + 1);
          loadLetterGames(currentLetterIdx + 1);
        } else {
          toast.success(t('allLettersComplete'));
          setView('course');
        }
      }, 2500);
    }
  };

  const handleWatchAd = async () => {
    toast.success(t('watchingAd'));
    await new Promise(r => setTimeout(r, 2000));
    try { const r = await fetch(`${API}/api/kids-learn/reward-ad?user_id=${userId}&coins=10`, { method: 'POST' }); const d = await r.json(); if (d.success) { toast.success(`🪙 +${d.earned} ${t('coinsEarned')}`); loadProfile(); } } catch {}
  };

  // ═══════ SHARED: BACK BUTTON ═══════
  const BackBtn = ({ to = 'home' as View, label = '' }) => (
    <button onClick={() => { setView(to); setShowReward(false); }}
      className="flex items-center gap-2 px-3 py-2 rounded-2xl bg-white/10 dark:bg-white/5 hover:bg-white/20 transition-all text-sm font-semibold text-foreground/70"
    >
      {isRTL ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
      {label || t('back')}
    </button>
  );

  // ═══════ RENDER: TOP BAR ═══════
  const TopBar = () => (
    <div className="sticky top-0 z-40 backdrop-blur-xl bg-background/80 border-b border-border/50 px-4 py-3 safe-area-pt">
      <div className="flex items-center gap-3 max-w-lg mx-auto">
        {view !== 'home' && <BackBtn to={view === 'letter_lesson' ? 'course_detail' : view === 'course_detail' ? 'course' : view === 'academy_lesson' ? 'academy_track' : view === 'academy_track' ? 'academy' : 'home'} />}
        {view === 'home' && (
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-sm shadow-md border border-amber-300/20">✨</div>
            <div>
              <h1 className="text-sm font-black text-foreground">{t('noorAcademy')}</h1>
              <p className="text-[10px] text-muted-foreground flex items-center gap-1"><Crown className="h-2.5 w-2.5 text-amber-500" />{t('level')} {profile?.level || 1}</p>
            </div>
          </div>
        )}
        <div className="flex-1" />
        <div className="flex items-center gap-1.5">
          <div className="flex items-center gap-1 px-2 py-1 rounded-xl bg-orange-500/10"><Flame className="h-3 w-3 text-orange-500" /><span className="text-[11px] font-black text-orange-500">{profile?.streak_days || 0}</span></div>
          <div className="flex items-center gap-1 px-2 py-1 rounded-xl bg-emerald-500/10"><Zap className="h-3 w-3 text-emerald-500" /><span className="text-[11px] font-black text-emerald-500">{profile?.total_xp || 0}</span></div>
        </div>
      </div>
    </div>
  );

  // ═══════ RENDER: HOME ═══════
  const renderHome = () => (
    <div className="space-y-5 px-4 pb-28 pt-4 max-w-lg mx-auto">
      {/* XP Progress */}
      <div className="flex items-center gap-3 px-1">
        <div className="flex-1 h-2.5 rounded-full bg-muted overflow-hidden">
          <motion.div className="h-full bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full" animate={{ width: `${(profile?.total_xp || 0) % 100}%` }} />
        </div>
        <span className="text-[10px] font-bold text-muted-foreground whitespace-nowrap">{(profile?.total_xp || 0) % 100}/100 {t('xpPoints')}</span>
      </div>

      {/* Today's Games — Big Hero Card */}
      <motion.button whileTap={{ scale: 0.98 }} onClick={() => { setView('play'); setCurrentGameIdx(0); setShowReward(false); setCompletedGames(new Set()); setEarnedXP(0); }}
        className="w-full p-6 rounded-[28px] bg-gradient-to-br from-emerald-500 to-teal-600 text-white text-start shadow-xl shadow-emerald-500/20 active:shadow-md transition-all relative overflow-hidden"
      >
        <div className="absolute -top-8 -right-8 w-32 h-32 bg-white/10 rounded-full blur-2xl" />
        <div className="relative z-10">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-bold text-white/60 uppercase tracking-wider">{t('todaysGames')}</p>
              <h2 className="text-2xl font-black mt-1">{dailyGames?.games_count || 4} {t('gamesAvailable')}</h2>
              <p className="text-sm text-white/70 mt-1">{t('targetXP').replace('{xp}', String(dailyGames?.total_xp || 60))}</p>
            </div>
            <div className="w-16 h-16 rounded-3xl bg-white/20 backdrop-blur flex items-center justify-center shadow-inner">
              <Play className="h-8 w-8 text-white fill-white" />
            </div>
          </div>
          {/* Mini game icons */}
          <div className="flex gap-2 mt-4">
            {dailyGames?.games.map(g => (
              <div key={g.id} className={cn("flex-1 py-2 rounded-2xl bg-white/15 backdrop-blur text-center text-lg", completedGames.has(g.id) && "bg-white/30 ring-2 ring-white/40")}>
                {g.emoji}
              </div>
            ))}
          </div>
        </div>
      </motion.button>

      {/* Course Card */}
      <motion.button whileTap={{ scale: 0.98 }} onClick={() => setView('course')}
        className="w-full p-5 rounded-[24px] bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-start shadow-lg shadow-blue-500/15 active:shadow-md transition-all relative overflow-hidden"
      >
        <div className="absolute -bottom-6 -left-6 w-24 h-24 bg-white/10 rounded-full blur-xl" />
        <div className="relative z-10 flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-white/20 backdrop-blur flex items-center justify-center text-2xl">📖</div>
          <div className="flex-1">
            <p className="text-xs font-bold text-white/60 uppercase tracking-wider">{t('arabicCourse')}</p>
            <h3 className="text-lg font-black mt-0.5">{t('zeroToC1')}</h3>
            <p className="text-xs text-white/60 mt-0.5">6 {t('levels')} • 216 {t('lessons')}</p>
          </div>
          <ChevronRight className="h-6 w-6 text-white/50" />
        </div>
      </motion.button>

      {/* Noor Academy V2 — Islamic Education Card */}
      <motion.button whileTap={{ scale: 0.98 }} onClick={() => setView('academy')}
        className="w-full p-5 rounded-[24px] bg-gradient-to-br from-amber-500 via-orange-500 to-rose-500 text-white text-start shadow-lg shadow-amber-500/20 active:shadow-md transition-all relative overflow-hidden"
      >
        <div className="absolute -top-6 -right-6 w-28 h-28 bg-white/10 rounded-full blur-xl" />
        <div className="relative z-10 flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-white/20 backdrop-blur flex items-center justify-center text-2xl">🕌</div>
          <div className="flex-1">
            <p className="text-xs font-bold text-white/70 uppercase tracking-wider">{lang === 'ar' ? 'أكاديمية نور' : 'Noor Academy'}</p>
            <h3 className="text-lg font-black mt-0.5">{lang === 'ar' ? '5 مسارات تعليمية' : '5 Learning Tracks'}</h3>
            <p className="text-xs text-white/60 mt-0.5">{academyOverview?.total_lessons || 240}+ {t('lessons')} • {lang === 'ar' ? 'نورانية • عقيدة • فقه • سيرة • آداب' : 'Nooraniya • Aqeedah • Fiqh • Seerah • Adab'}</p>
          </div>
          <ChevronRight className="h-6 w-6 text-white/50" />
        </div>
      </motion.button>

      {/* Category Grid — 2x2 */}
      <div className="grid grid-cols-2 gap-3">
        {[
          { emoji: '🛡️', label: t('digitalShield'), sub: '30 ' + (t('lessons')), view: 'shield' as View, gradient: 'from-violet-500 to-purple-600' },
          { emoji: '🏆', label: t('myProgress'), sub: `${profile?.games_completed || 0} ${t('gamesPlayed')}`, view: 'profile' as View, gradient: 'from-amber-500 to-orange-600' },
        ].map(item => (
          <motion.button key={item.view} whileTap={{ scale: 0.97 }} onClick={() => setView(item.view)}
            className={`p-4 rounded-[20px] bg-gradient-to-br ${item.gradient} text-white text-start shadow-lg active:shadow-md transition-all`}
          >
            <span className="text-3xl">{item.emoji}</span>
            <h3 className="text-sm font-bold mt-2">{item.label}</h3>
            <p className="text-[10px] text-white/60 mt-0.5">{item.sub}</p>
          </motion.button>
        ))}
      </div>

      {/* Watch Ad */}
      <motion.button whileTap={{ scale: 0.98 }} onClick={handleWatchAd}
        className="w-full p-4 rounded-[20px] bg-gradient-to-r from-amber-100 to-orange-100 dark:from-amber-900/30 dark:to-orange-900/20 border border-amber-300/30 dark:border-amber-700/30 flex items-center gap-4 text-start"
      >
        <span className="text-3xl">🎬</span>
        <div className="flex-1">
          <h3 className="text-sm font-bold text-foreground">{t('watchForCoins')}</h3>
          <p className="text-[10px] text-muted-foreground">{t('watchAdDesc')}</p>
        </div>
        <div className="px-3 py-1.5 rounded-xl bg-amber-500/15 text-amber-600 dark:text-amber-400 text-xs font-black">+10 🪙</div>
      </motion.button>

      {/* Quick Stats */}
      <div className="grid grid-cols-3 gap-2">
        {[
          { icon: <Zap className="h-5 w-5 text-emerald-500" />, val: profile?.total_xp || 0, label: t('xpPoints') },
          { icon: <Flame className="h-5 w-5 text-orange-500" />, val: profile?.streak_days || 0, label: t('streak') },
          { icon: <Crown className="h-5 w-5 text-amber-500" />, val: profile?.level || 1, label: t('level') },
        ].map((s, i) => (
          <div key={i} className="p-3 rounded-2xl bg-card border border-border text-center">
            <div className="flex justify-center">{s.icon}</div>
            <p className="text-xl font-black mt-1">{s.val}</p>
            <p className="text-[10px] text-muted-foreground">{s.label}</p>
          </div>
        ))}
      </div>
    </div>
  );

  // ═══════ RENDER: PLAY (GAME ENGINE) ═══════
  const renderPlay = () => {
    if (!dailyGames) return <div className="flex items-center justify-center h-[60vh]"><span className="text-4xl animate-bounce">🎮</span></div>;
    if (showReward) return (
      <motion.div initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} className="flex flex-col items-center justify-center h-[70vh] px-8 text-center max-w-lg mx-auto">
        <motion.div animate={{ rotate: [0, 10, -10, 0] }} transition={{ repeat: Infinity, duration: 2 }} className="text-7xl mb-6">🏆</motion.div>
        <h2 className="text-2xl font-black">{t('allGamesComplete')}</h2>
        <p className="text-lg text-muted-foreground mt-2">{t('earnedTotal').replace('{xp}', String(earnedXP))}</p>
        <div className="flex gap-3 mt-8">
          <button onClick={() => { setView('home'); setShowReward(false); }} className="px-6 py-3 rounded-2xl bg-primary text-primary-foreground font-bold shadow-lg">{t('backToHome')}</button>
          <button onClick={handleWatchAd} className="px-6 py-3 rounded-2xl bg-amber-500 text-white font-bold shadow-lg">🎬 +10🪙</button>
        </div>
      </motion.div>
    );
    const game = dailyGames.games[currentGameIdx];
    return (
      <div className="pb-8 max-w-lg mx-auto">
        <div className="px-4 py-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-muted-foreground">{t('gameOf').replace('{c}', String(currentGameIdx + 1)).replace('{t}', String(dailyGames.games.length))}</span>
            <span className="text-xs font-bold text-emerald-500">{t('earnedPoints').replace('{xp}', String(earnedXP))}</span>
          </div>
          <div className="h-2 rounded-full bg-muted overflow-hidden"><motion.div className="h-full bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full" animate={{ width: `${(currentGameIdx / dailyGames.games.length) * 100}%` }} /></div>
        </div>
        <AnimatePresence mode="wait">
          <motion.div key={game.id} initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }}>
            {game.type === 'quiz' && <QuizGame question={game.question} options={game.options} correctIndex={game.correct_index} xp={game.xp} onComplete={(c, x) => handleGameComplete(game.id, c, x)} />}
            {game.type === 'memory' && <MemoryGame cards={game.cards} totalPairs={game.total_pairs} xp={game.xp} onComplete={(c, x) => handleGameComplete(game.id, c, x)} />}
            {game.type === 'drag_drop' && <DragDropGame title={game.title} items={game.items} correctOrder={game.correct_order} xp={game.xp} onComplete={(c, x) => handleGameComplete(game.id, c, x)} />}
            {game.type === 'scenario' && <ScenarioGame scenario={game.scenario} options={game.options} correctIndex={game.correct_index} explanation={game.explanation} xp={game.xp} onComplete={(c, x) => handleGameComplete(game.id, c, x)} />}
          </motion.div>
        </AnimatePresence>
      </div>
    );
  };

  // ═══════ RENDER: COURSE OVERVIEW ═══════
  const renderCourse = () => (
    <div className="space-y-4 px-4 pb-28 pt-4 max-w-lg mx-auto">
      <div className="text-center mb-2">
        <h2 className="text-xl font-black">{t('arabicCourse')}</h2>
        <p className="text-sm text-muted-foreground mt-1">{t('zeroToC1')} • 6 {t('levels')}</p>
      </div>
      {courseLevels.map((lv, i) => (
        <motion.button key={lv.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }} whileTap={{ scale: 0.98 }}
          onClick={() => { setSelectedLevel(lv); setView('course_detail'); }}
          className={cn("w-full p-5 rounded-[24px] text-start shadow-md transition-all border border-border", LEVEL_BG[lv.color])}
        >
          <div className="flex items-center gap-4">
            <div className={cn("w-14 h-14 rounded-2xl bg-gradient-to-br flex items-center justify-center text-2xl shadow-md", LEVEL_COLORS[lv.color])}>
              {lv.emoji}
            </div>
            <div className="flex-1">
              <h3 className="text-base font-black text-foreground">{lv.name}</h3>
              <p className="text-xs text-muted-foreground mt-0.5">{lv.desc}</p>
              <p className="text-[10px] text-muted-foreground mt-1">{lv.units_count} {t('units')} • {lv.total_lessons} {t('lessons')}</p>
            </div>
            <ChevronRight className="h-5 w-5 text-muted-foreground" />
          </div>
        </motion.button>
      ))}
    </div>
  );

  // ═══════ RENDER: COURSE DETAIL (UNITS) ═══════
  const renderCourseDetail = () => {
    if (!selectedLevel) return null;
    const TYPE_ICONS: Record<string, string> = { alphabet: '🔤', vocabulary: '📝', grammar: '📐', quran: '📖', dua: '🤲', islam: '🕌', reading: '📚', conversation: '💬', writing: '✍️', advanced: '🎓' };
    return (
      <div className="space-y-4 px-4 pb-28 pt-4 max-w-lg mx-auto">
        <div className={cn("p-5 rounded-[24px] text-center", LEVEL_BG[selectedLevel.color])}>
          <span className="text-4xl">{selectedLevel.emoji}</span>
          <h2 className="text-xl font-black mt-2">{selectedLevel.name}</h2>
          <p className="text-sm text-muted-foreground mt-1">{selectedLevel.desc}</p>
        </div>
        {selectedLevel.units.map((unit: any, i: number) => (
          <motion.button key={unit.id} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.06 }} whileTap={{ scale: 0.98 }}
            onClick={() => {
              if (unit.type === 'alphabet') {
                setCurrentLetterIdx(0); loadLetterGames(0); setView('letter_lesson');
              } else {
                toast.info(t('comingSoon'));
              }
            }}
            className="w-full p-4 rounded-[20px] bg-card border border-border flex items-center gap-4 text-start shadow-sm hover:shadow-md transition-all"
          >
            <div className="w-12 h-12 rounded-2xl bg-muted flex items-center justify-center text-xl">{TYPE_ICONS[unit.type] || '📚'}</div>
            <div className="flex-1">
              <h3 className="text-sm font-bold text-foreground">{unit.title}</h3>
              <p className="text-[10px] text-muted-foreground mt-0.5">{unit.lessons} {t('lessons')}</p>
            </div>
            {unit.type === 'alphabet' ? (
              <div className="px-3 py-1.5 rounded-xl bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 text-xs font-bold">{t('start')}</div>
            ) : (
              <Lock className="h-4 w-4 text-muted-foreground/30" />
            )}
          </motion.button>
        ))}
      </div>
    );
  };

  // ═══════ RENDER: LETTER LESSON ═══════
  const renderLetterLesson = () => {
    if (alphabet.length === 0) return null;
    const lt = alphabet[currentLetterIdx];
    if (!lt) return null;

    if (showLetterInfo) {
      return (
        <div className="space-y-5 px-4 pb-28 pt-4 max-w-lg mx-auto">
          {/* Letter display */}
          <div className="text-center p-8 rounded-[28px] bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/20 border border-blue-200/30 dark:border-blue-800/30">
            <p className="text-xs font-bold text-muted-foreground mb-2">{t('letterOf').replace('{c}', String(currentLetterIdx + 1)).replace('{t}', '28')}</p>
            <motion.div key={lt.letter} initial={{ scale: 0.5, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="text-8xl font-black text-blue-600 dark:text-blue-400 mb-3" style={{ fontFamily: "'Noto Naskh Arabic', 'Amiri', serif" }}>
              {lt.letter}
            </motion.div>
            <p className="text-xl font-bold text-foreground">{lt.name}</p>
            <p className="text-sm text-muted-foreground">{t('sound')}: <span className="font-bold text-foreground">{lt.sound}</span></p>
          </div>

          {/* Letter forms */}
          <div className="grid grid-cols-4 gap-2">
            {Object.entries(lt.forms).map(([form, char]) => (
              <div key={form} className="p-3 rounded-2xl bg-card border border-border text-center">
                <p className="text-3xl mb-1" style={{ fontFamily: "'Noto Naskh Arabic', 'Amiri', serif" }}>{char as string}</p>
                <p className="text-[10px] text-muted-foreground capitalize">{form === 'isolated' ? (t('isolated')) : form === 'initial' ? (t('initial')) : form === 'medial' ? (t('medial')) : (t('final'))}</p>
              </div>
            ))}
          </div>

          {/* Example word — Arabic + localized translation */}
          <div className="p-4 rounded-[20px] bg-amber-50 dark:bg-amber-950/20 border border-amber-200/30 dark:border-amber-800/30 flex items-center gap-4">
            <span className="text-4xl">{lt.emoji}</span>
            <div className="flex-1">
              <p className="text-2xl font-bold" style={{ fontFamily: "'Noto Naskh Arabic', 'Amiri', serif" }}>{lt.word_ar}</p>
              <p className="text-lg font-semibold text-amber-700 dark:text-amber-300">{lt.word || lt.word_en}</p>
            </div>
          </div>

          {/* Practice button */}
          <motion.button whileTap={{ scale: 0.97 }} onClick={() => setShowLetterInfo(false)}
            className="w-full py-4 rounded-2xl bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-base font-black shadow-lg shadow-blue-500/20"
          >
            {t('practiceNow')} 🎮
          </motion.button>

          {/* Navigate letters */}
          <div className="flex items-center justify-between">
            <button onClick={() => { if (currentLetterIdx > 0) { setCurrentLetterIdx(currentLetterIdx - 1); loadLetterGames(currentLetterIdx - 1); } }}
              disabled={currentLetterIdx === 0} className="px-4 py-2 rounded-xl bg-muted text-sm font-bold disabled:opacity-30">
              {isRTL ? '→' : '←'} {t('prevLesson')}
            </button>
            <span className="text-xs font-bold text-muted-foreground">{currentLetterIdx + 1}/28</span>
            <button onClick={() => { if (currentLetterIdx < 27) { setCurrentLetterIdx(currentLetterIdx + 1); loadLetterGames(currentLetterIdx + 1); } }}
              disabled={currentLetterIdx === 27} className="px-4 py-2 rounded-xl bg-muted text-sm font-bold disabled:opacity-30">
              {t('nextLesson')} {isRTL ? '←' : '→'}
            </button>
          </div>
        </div>
      );
    }

    // Show letter games
    if (letterGames.length === 0) return null;
    const game = letterGames[letterGameIdx];
    return (
      <div className="pb-8 max-w-lg mx-auto">
        <div className="px-4 py-3">
          <div className="flex items-center justify-between mb-2">
            <button onClick={() => setShowLetterInfo(true)} className="text-xs font-bold text-primary">{isRTL ? '→' : '←'} {lt.letter} {lt.name}</button>
            <span className="text-xs font-bold text-emerald-500">{t('gameOf').replace('{c}', String(letterGameIdx + 1)).replace('{t}', String(letterGames.length))}</span>
          </div>
          <div className="h-2 rounded-full bg-muted overflow-hidden"><motion.div className="h-full bg-gradient-to-r from-blue-400 to-indigo-400 rounded-full" animate={{ width: `${(letterGameIdx / letterGames.length) * 100}%` }} /></div>
        </div>
        <AnimatePresence mode="wait">
          <motion.div key={game.id} initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }}>
            {game.type === 'quiz' && <QuizGame question={game.question} options={game.options} correctIndex={game.correct_index} xp={game.xp} onComplete={(c, x) => handleLetterGameComplete(game.id, c, x)} />}
            {game.type === 'memory' && <MemoryGame cards={game.cards} totalPairs={game.total_pairs} xp={game.xp} onComplete={(c, x) => handleLetterGameComplete(game.id, c, x)} />}
          </motion.div>
        </AnimatePresence>
      </div>
    );
  };

  // ═══════ RENDER: DIGITAL SHIELD ═══════
  const SHIELD_EMOJI: Record<string, string> = { deepfakes: '🎭', privacy: '🔒', social_media: '📱', misinformation: '📰', ethics: '⚖️', safety: '🛡️' };
  const renderShield = () => {
    const themes = ['all', 'deepfakes', 'privacy', 'social_media', 'misinformation', 'ethics', 'safety'];
    return (
      <div className="space-y-4 px-4 pb-28 pt-4 max-w-lg mx-auto">
        <div className="text-center p-5 rounded-[24px] bg-violet-50 dark:bg-violet-950/20 border border-violet-200/30 dark:border-violet-800/30">
          <span className="text-4xl">🛡️</span>
          <h2 className="text-xl font-black mt-2">{t('digitalShield')}</h2>
          <p className="text-sm text-muted-foreground mt-1">{t('digitalShieldDesc')}</p>
        </div>
        <div className="flex gap-1.5 overflow-x-auto pb-1 scrollbar-hide">
          {themes.map(th => (
            <button key={th} onClick={() => setShieldFilter(th)} className={cn("px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap border transition-all shrink-0", shieldFilter === th ? "bg-violet-100 dark:bg-violet-900/30 border-violet-300 dark:border-violet-700 text-violet-700 dark:text-violet-300" : "bg-card border-border text-muted-foreground")}>
              {th === 'all' ? '✨' : SHIELD_EMOJI[th]} {th === 'all' ? t('allLessons') : t(th)}
            </button>
          ))}
        </div>
        {shieldLessons.map((lesson, idx) => (
          <motion.button key={lesson.id} whileTap={{ scale: 0.98 }} onClick={() => setExpandedLesson(expandedLesson === lesson.id ? null : lesson.id)}
            className={cn("w-full rounded-[20px] border p-4 text-start bg-card transition-all", expandedLesson === lesson.id && "ring-2 ring-violet-400/30 shadow-lg")}
          >
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 rounded-xl bg-violet-100 dark:bg-violet-900/30 flex items-center justify-center text-lg">{SHIELD_EMOJI[lesson.theme] || '🛡️'}</div>
              <div className="flex-1 min-w-0">
                <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">{t(lesson.theme)} #{idx + 1}</span>
                <h3 className="font-bold text-sm">{lesson.title}</h3>
              </div>
            </div>
            {expandedLesson === lesson.id && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-3 space-y-3">
                <div className="p-3 rounded-xl bg-muted/50"><p className="text-sm leading-relaxed text-foreground/80">{lesson.content}</p></div>
                <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/20 border border-amber-200/20">
                  <div className="flex items-center gap-2 mb-1"><Star className="h-4 w-4 text-amber-500" /><span className="text-xs font-bold text-amber-600 dark:text-amber-400">{t('keyMoral')}</span></div>
                  <p className="text-sm font-semibold text-amber-700 dark:text-amber-200">{lesson.key_lesson}</p>
                </div>
              </motion.div>
            )}
          </motion.button>
        ))}
      </div>
    );
  };

  // ═══════ RENDER: PROFILE ═══════
  const renderProfile = () => (
    <div className="space-y-4 px-4 pb-28 pt-4 max-w-lg mx-auto">
      <div className="text-center p-6 rounded-[28px] bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/10 border border-amber-200/30 dark:border-amber-800/30">
        <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-4xl mx-auto shadow-xl border-2 border-amber-300/30">✨</div>
        <h2 className="text-xl font-black mt-3">{t('noorExplorer')}</h2>
        <div className="flex items-center justify-center gap-2 mt-1"><Crown className="h-4 w-4 text-amber-500" /><span className="text-sm font-bold text-amber-600 dark:text-amber-400">{t('level')} {profile?.level || 1}</span></div>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {[
          { icon: <Zap className="h-6 w-6 text-emerald-500" />, val: profile?.total_xp || 0, label: t('totalXP'), bg: 'bg-emerald-50 dark:bg-emerald-950/20' },
          { icon: <Flame className="h-6 w-6 text-orange-500" />, val: profile?.streak_days || 0, label: t('dayStreak'), bg: 'bg-orange-50 dark:bg-orange-950/20' },
          { icon: <Trophy className="h-6 w-6 text-blue-500" />, val: profile?.games_completed || 0, label: t('gamesPlayed'), bg: 'bg-blue-50 dark:bg-blue-950/20' },
          { icon: <Gift className="h-6 w-6 text-amber-500" />, val: profile?.coins || 0, label: t('coins'), bg: 'bg-amber-50 dark:bg-amber-950/20' },
        ].map((s, i) => (
          <div key={i} className={cn("p-4 rounded-2xl border border-border text-center", s.bg)}>
            <div className="flex justify-center">{s.icon}</div>
            <p className="text-2xl font-black mt-2">{s.val}</p>
            <p className="text-xs text-muted-foreground">{s.label}</p>
          </div>
        ))}
      </div>
      <motion.button whileTap={{ scale: 0.97 }} onClick={handleWatchAd}
        className="w-full p-4 rounded-[20px] bg-gradient-to-r from-amber-100 to-orange-100 dark:from-amber-900/30 dark:to-orange-900/20 border border-amber-300/30 flex items-center gap-3"
      >
        <span className="text-3xl">🎬</span>
        <div className="flex-1 text-start">
          <h3 className="text-sm font-bold">{t('watchForCoins')}</h3>
          <p className="text-[10px] text-muted-foreground">{t('watchAdDesc')}</p>
        </div>
        <div className="px-3 py-1.5 rounded-xl bg-amber-500/15 text-amber-600 dark:text-amber-400 text-xs font-black">+10 🪙</div>
      </motion.button>
    </div>
  );

  // ═══════ RENDER: ACADEMY OVERVIEW ═══════
  const TRACK_GRADIENTS: Record<string, string> = {
    nooraniya: 'from-emerald-500 to-teal-600', aqeedah: 'from-blue-500 to-indigo-600',
    fiqh: 'from-violet-500 to-purple-600', seerah: 'from-amber-500 to-orange-600',
    adab: 'from-rose-500 to-pink-600',
  };
  const TRACK_BG: Record<string, string> = {
    nooraniya: 'bg-emerald-50 dark:bg-emerald-950/20', aqeedah: 'bg-blue-50 dark:bg-blue-950/20',
    fiqh: 'bg-violet-50 dark:bg-violet-950/20', seerah: 'bg-amber-50 dark:bg-amber-950/20',
    adab: 'bg-rose-50 dark:bg-rose-950/20',
  };

  const renderAcademy = () => (
    <div className="space-y-4 px-4 pb-28 pt-4 max-w-lg mx-auto">
      <div className="text-center p-5 rounded-[24px] bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/10 border border-amber-200/30 dark:border-amber-800/30">
        <span className="text-4xl">🕌</span>
        <h2 className="text-xl font-black mt-2">{lang === 'ar' ? 'أكاديمية نور' : 'Noor Academy'}</h2>
        <p className="text-sm text-muted-foreground mt-1">{lang === 'ar' ? 'تعلّم دينك بطريقة ممتعة وتفاعلية' : 'Learn your religion in a fun, interactive way'}</p>
        <p className="text-xs text-muted-foreground mt-1">{academyOverview?.total_lessons || 240}+ {lang === 'ar' ? 'درس' : 'lessons'}</p>
      </div>
      {academyOverview?.tracks.map((track, i) => (
        <motion.button key={track.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }} whileTap={{ scale: 0.98 }}
          onClick={() => { loadTrack(track.id); setView('academy_track'); }}
          className={cn("w-full p-5 rounded-[24px] text-start shadow-md transition-all border border-border", TRACK_BG[track.id] || 'bg-card')}
        >
          <div className="flex items-center gap-4">
            <div className={cn("w-14 h-14 rounded-2xl bg-gradient-to-br flex items-center justify-center text-2xl shadow-md text-white", TRACK_GRADIENTS[track.id] || 'from-gray-400 to-gray-600')}>
              {track.emoji}
            </div>
            <div className="flex-1">
              <h3 className="text-base font-black text-foreground">{track.name}</h3>
              <p className="text-xs text-muted-foreground mt-0.5">{track.description}</p>
              <p className="text-[10px] text-muted-foreground mt-1">{track.total_lessons} {lang === 'ar' ? 'درس' : 'lessons'} • {track.levels?.length || 0} {lang === 'ar' ? 'مستويات' : 'levels'}</p>
            </div>
            <ChevronRight className="h-5 w-5 text-muted-foreground" />
          </div>
        </motion.button>
      ))}
    </div>
  );

  // ═══════ RENDER: ACADEMY TRACK DETAIL ═══════
  const renderAcademyTrack = () => {
    if (!selectedTrack) return <div className="flex items-center justify-center h-[60vh]"><span className="text-4xl animate-spin">⏳</span></div>;
    return (
      <div className="space-y-4 px-4 pb-28 pt-4 max-w-lg mx-auto">
        <div className={cn("p-5 rounded-[24px] text-center border border-border", TRACK_BG[selectedTrack.id] || 'bg-card')}>
          <span className="text-4xl">{selectedTrack.emoji}</span>
          <h2 className="text-xl font-black mt-2">{selectedTrack.name}</h2>
          <p className="text-sm text-muted-foreground mt-1">{selectedTrack.description}</p>
          <p className="text-xs text-muted-foreground mt-1">{selectedTrack.total_lessons} {lang === 'ar' ? 'درس' : 'lessons'}</p>
        </div>
        {selectedTrack.levels.map((level: any, li: number) => (
          <div key={level.level} className="space-y-2">
            <div className="flex items-center gap-2 px-1">
              <span className="text-lg">{level.emoji}</span>
              <h3 className="text-sm font-black text-foreground">{level.name}</h3>
              <span className="text-[10px] text-muted-foreground">({level.lessons_count} {lang === 'ar' ? 'دروس' : 'lessons'})</span>
            </div>
            <div className="space-y-1.5">
              {level.lessons?.map((lesson: any, idx: number) => (
                <motion.button key={lesson.id} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: (li * 0.05) + (idx * 0.02) }} whileTap={{ scale: 0.98 }}
                  onClick={() => { loadAcademyLesson(selectedTrack.id, lesson.id); setView('academy_lesson'); }}
                  className="w-full p-3.5 rounded-[16px] bg-card border border-border flex items-center gap-3 text-start shadow-sm hover:shadow-md transition-all"
                >
                  <div className="w-10 h-10 rounded-xl bg-muted flex items-center justify-center text-lg shrink-0">{lesson.emoji}</div>
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-bold text-foreground truncate">{lesson.title}</h4>
                    <p className="text-[10px] text-muted-foreground">{lang === 'ar' ? `درس ${lesson.lesson}` : `Lesson ${lesson.lesson}`} • {lesson.xp} XP</p>
                  </div>
                  {lesson.content?.placeholder || lesson.content?.status === 'placeholder' ? (
                    <span className="text-[10px] text-muted-foreground/50 px-2 py-1 bg-muted rounded-lg">{lang === 'ar' ? 'قريباً' : 'Soon'}</span>
                  ) : (
                    <div className="px-2.5 py-1 rounded-lg bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 text-[10px] font-bold">{lang === 'ar' ? 'ابدأ' : 'Start'}</div>
                  )}
                </motion.button>
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  };

  // ═══════ RENDER: ACADEMY LESSON VIEWER ═══════
  const renderAcademyLesson = () => {
    if (!currentAcademyLesson) return <div className="flex items-center justify-center h-[60vh]"><span className="text-4xl animate-bounce">📖</span></div>;
    const ls = currentAcademyLesson;
    const content = ls.content;
    const quiz = ls.quiz;
    const isPlaceholder = content?.placeholder || content?.status === 'placeholder';

    const renderContent = () => {
      if (isPlaceholder) {
        return (
          <div className="p-6 rounded-[20px] bg-amber-50 dark:bg-amber-950/20 border border-amber-200/30 text-center">
            <span className="text-4xl">🚧</span>
            <p className="text-sm font-bold mt-2 text-amber-700 dark:text-amber-300">{content?.message || (lang === 'ar' ? 'قريباً — المحتوى قيد الإعداد' : 'Coming Soon')}</p>
          </div>
        );
      }

      const parts: React.ReactNode[] = [];

      // Story or intro
      if (content?.story) {
        const story = typeof content.story === 'string' ? content.story : content.story[lang] || content.story.ar || content.story.en || '';
        if (story) parts.push(<div key="story" className="p-4 rounded-[16px] bg-blue-50 dark:bg-blue-950/20 border border-blue-200/30"><p className="text-sm leading-relaxed">{story}</p></div>);
      }
      if (content?.intro) {
        const intro = typeof content.intro === 'string' ? content.intro : content.intro[lang] || content.intro.ar || content.intro.en || '';
        if (intro) parts.push(<div key="intro" className="p-4 rounded-[16px] bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200/30"><p className="text-sm leading-relaxed">{intro}</p></div>);
      }
      if (content?.verse) {
        const verse = typeof content.verse === 'string' ? content.verse : content.verse[lang] || content.verse.ar || content.verse.en || '';
        if (verse) parts.push(<div key="verse" className="p-4 rounded-[16px] bg-amber-50 dark:bg-amber-950/20 border border-amber-200/30 text-center"><p className="text-base font-semibold leading-relaxed" style={{ fontFamily: "'Noto Naskh Arabic', 'Amiri', serif" }}>{verse}</p></div>);
      }
      if (content?.hadith) {
        const hadith = typeof content.hadith === 'string' ? content.hadith : content.hadith[lang] || content.hadith.ar || content.hadith.en || '';
        if (hadith) parts.push(<div key="hadith" className="p-4 rounded-[16px] bg-green-50 dark:bg-green-950/20 border border-green-200/30"><p className="text-sm leading-relaxed italic">📿 {hadith}</p></div>);
      }
      if (content?.meaning) {
        const meaning = typeof content.meaning === 'string' ? content.meaning : content.meaning[lang] || content.meaning.ar || content.meaning.en || '';
        if (meaning) parts.push(<div key="meaning" className="p-4 rounded-[16px] bg-indigo-50 dark:bg-indigo-950/20 border border-indigo-200/30"><p className="text-sm leading-relaxed">{meaning}</p></div>);
      }
      if (content?.importance) {
        const importance = typeof content.importance === 'string' ? content.importance : content.importance[lang] || content.importance.ar || content.importance.en || '';
        if (importance) parts.push(<div key="imp" className="p-4 rounded-[16px] bg-rose-50 dark:bg-rose-950/20 border border-rose-200/30"><p className="text-sm leading-relaxed">{importance}</p></div>);
      }
      if (content?.definition) {
        const def = typeof content.definition === 'string' ? content.definition : content.definition[lang] || content.definition.ar || content.definition.en || '';
        if (def) parts.push(<div key="def" className="p-4 rounded-[16px] bg-teal-50 dark:bg-teal-950/20 border border-teal-200/30"><p className="text-sm leading-relaxed">{def}</p></div>);
      }

      // List-based content
      const lists = ['types', 'pillars', 'names', 'steps', 'events', 'examples', 'qualities', 'etiquettes', 'practices', 'nullifiers', 'conditions', 'sunnahs', 'virtues', 'duties', 'blessings', 'categories', 'lessons', 'allowed', 'prohibitions', 'names_intro', 'first_muslims', 'ulul_azm', 'angels', 'books', 'stages', 'levels', 'aspects'];
      lists.forEach(key => {
        const list = content?.[key];
        if (Array.isArray(list) && list.length > 0) {
          parts.push(
            <div key={key} className="space-y-2">
              <h4 className="text-xs font-bold text-muted-foreground uppercase tracking-wider px-1">{key === 'names_intro' ? (lang === 'ar' ? 'أسماء' : 'Names') : key === 'first_muslims' ? (lang === 'ar' ? 'أوائل المسلمين' : 'First Muslims') : ''}</h4>
              {list.map((item: any, idx: number) => {
                const text = typeof item === 'string' ? item : item[lang] || item.ar || item.en || item.name?.[lang] || item.name?.ar || item.name?.en || item.action?.[lang] || item.action?.ar || item.action?.en || (typeof item.name === 'string' ? item.name : '') || (typeof item.action === 'string' ? item.action : '') || '';
                const detail = item.meaning?.[lang] || item.meaning?.ar || item.meaning?.en || item.detail?.[lang] || item.detail?.ar || item.detail?.en || item.ruling?.[lang] || item.ruling?.ar || item.ruling?.en || item.method?.[lang] || item.method?.ar || item.method?.en || item.story?.[lang] || item.story?.ar || item.story?.en || item.task?.[lang] || item.task?.ar || item.task?.en || item.desc?.[lang] || item.desc?.ar || item.desc?.en || item.example?.[lang] || item.example?.ar || item.example?.en || item.removal?.[lang] || item.removal?.ar || item.removal?.en || item.virtue?.[lang] || item.virtue?.ar || item.virtue?.en || item.status?.[lang] || item.status?.ar || item.status?.en || item.prophet?.[lang] || item.prophet?.ar || item.prophet?.en || item.time?.[lang] || item.time?.ar || item.time?.en || item.nisab?.[lang] || item.nisab?.ar || item.nisab?.en || item.rate?.[lang] || item.rate?.ar || item.rate?.en || '';
                return (
                  <div key={idx} className="p-3 rounded-[14px] bg-card border border-border flex items-start gap-3">
                    <span className="text-sm mt-0.5">{item.emoji || item.num ? `${item.num}.` : `${idx + 1}.`}</span>
                    <div className="flex-1">
                      <p className="text-sm font-semibold">{text}</p>
                      {detail && <p className="text-xs text-muted-foreground mt-0.5">{detail}</p>}
                    </div>
                  </div>
                );
              })}
            </div>
          );
        }
      });

      // Nested objects with specific content like five_prayers
      if (content?.five_prayers) {
        parts.push(
          <div key="prayers" className="space-y-2">
            {content.five_prayers.map((p: any, i: number) => (
              <div key={i} className="p-3 rounded-[14px] bg-card border border-border flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-muted flex items-center justify-center text-sm font-bold">{p.rakaat}</div>
                <div className="flex-1">
                  <p className="text-sm font-bold">{p.name?.[lang] || p.name?.ar || p.name?.en}</p>
                  <p className="text-[10px] text-muted-foreground">{p.time?.[lang] || p.time?.ar || p.time?.en}</p>
                </div>
              </div>
            ))}
          </div>
        );
      }

      // Context, balance, tip, reaction, impact, etc.
      ['context', 'balance', 'tip', 'reaction', 'impact', 'nature', 'quran', 'belief', 'entry', 'warning', 'protection', 'torments', 'rule', 'love', 'fear', 'ruling', 'amount', 'time', 'condition', 'expiation', 'oath', 'distribution', 'dua', 'practice'].forEach(key => {
        const val = content?.[key];
        if (val && typeof val === 'object' && (val[lang] || val.ar || val.en)) {
          const text = val[lang] || val.ar || val.en || '';
          if (text) parts.push(<div key={key} className="p-3 rounded-[14px] bg-muted/50 border border-border/50"><p className="text-xs text-muted-foreground mb-0.5 font-bold capitalize">{key}</p><p className="text-sm">{text}</p></div>);
        }
      });

      if (parts.length === 0) {
        // Fallback: render raw content as formatted text
        parts.push(<div key="raw" className="p-4 rounded-[16px] bg-muted/30 border border-border"><pre className="text-xs whitespace-pre-wrap">{JSON.stringify(content, null, 2)}</pre></div>);
      }

      return <div className="space-y-3">{parts}</div>;
    };

    const renderQuiz = () => {
      if (!quiz || quiz.type === 'placeholder') return null;
      const question = typeof quiz.question === 'string' ? quiz.question : quiz.question?.[lang] || quiz.question?.ar || quiz.question?.en || '';
      if (!question) return null;

      if (quiz.type === 'true_false') {
        const trueLabel = lang === 'ar' ? 'صحيح ✅' : 'True ✅';
        const falseLabel = lang === 'ar' ? 'خطأ ❌' : 'False ❌';
        const correctVal = quiz.correct === true ? 'true' : 'false';
        return (
          <div className="p-5 rounded-[20px] bg-indigo-50 dark:bg-indigo-950/20 border border-indigo-200/30 space-y-3">
            <h4 className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase">{lang === 'ar' ? '❓ اختبر نفسك' : '❓ Quiz'}</h4>
            <p className="text-sm font-bold">{question}</p>
            <div className="grid grid-cols-2 gap-2">
              {[{ val: 'true', label: trueLabel }, { val: 'false', label: falseLabel }].map(opt => (
                <button key={opt.val} onClick={() => { if (!quizSubmitted) { setQuizAnswer(opt.val); setQuizSubmitted(true); } }}
                  className={cn("p-3 rounded-xl border-2 text-sm font-bold transition-all",
                    !quizSubmitted ? "border-border hover:border-indigo-300 bg-card" :
                    opt.val === correctVal ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/20 text-emerald-700" :
                    opt.val === quizAnswer ? "border-red-500 bg-red-50 dark:bg-red-950/20 text-red-700" : "border-border bg-card opacity-50"
                  )}
                >{opt.label}</button>
              ))}
            </div>
            {quizSubmitted && (
              <p className={cn("text-sm font-bold text-center", quizAnswer === correctVal ? "text-emerald-600" : "text-red-600")}>
                {quizAnswer === correctVal ? (lang === 'ar' ? '🎉 إجابة صحيحة!' : '🎉 Correct!') : (lang === 'ar' ? `❌ الإجابة الصحيحة: ${correctVal === 'true' ? 'صحيح' : 'خطأ'}` : `❌ Correct: ${correctVal === 'true' ? 'True' : 'False'}`)}
              </p>
            )}
          </div>
        );
      }

      // Select quiz
      if (quiz.type === 'select' && quiz.options) {
        const correctStr = typeof quiz.correct === 'string' ? quiz.correct : quiz.correct?.[lang] || quiz.correct?.ar || quiz.correct?.en || '';
        return (
          <div className="p-5 rounded-[20px] bg-indigo-50 dark:bg-indigo-950/20 border border-indigo-200/30 space-y-3">
            <h4 className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase">{lang === 'ar' ? '❓ اختبر نفسك' : '❓ Quiz'}</h4>
            <p className="text-sm font-bold">{question}</p>
            <div className="space-y-2">
              {quiz.options.map((opt: any, i: number) => {
                const optText = typeof opt === 'string' ? opt : opt[lang] || opt.ar || opt.en || '';
                const isCorrect = optText === correctStr;
                return (
                  <button key={i} onClick={() => { if (!quizSubmitted) { setQuizAnswer(optText); setQuizSubmitted(true); } }}
                    className={cn("w-full p-3 rounded-xl border-2 text-sm font-semibold text-start transition-all",
                      !quizSubmitted ? "border-border hover:border-indigo-300 bg-card" :
                      isCorrect ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/20 text-emerald-700" :
                      optText === quizAnswer ? "border-red-500 bg-red-50 dark:bg-red-950/20 text-red-700" : "border-border bg-card opacity-50"
                    )}
                  >{optText}</button>
                );
              })}
            </div>
            {quizSubmitted && (
              <p className={cn("text-sm font-bold text-center", quizAnswer === correctStr ? "text-emerald-600" : "text-red-600")}>
                {quizAnswer === correctStr ? (lang === 'ar' ? '🎉 إجابة صحيحة!' : '🎉 Correct!') : (lang === 'ar' ? `❌ الإجابة: ${correctStr}` : `❌ Correct: ${correctStr}`)}
              </p>
            )}
          </div>
        );
      }

      // Sequence quiz
      if (quiz.type === 'sequence' && quiz.correct_order) {
        return (
          <div className="p-5 rounded-[20px] bg-indigo-50 dark:bg-indigo-950/20 border border-indigo-200/30 space-y-3">
            <h4 className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase">{lang === 'ar' ? '🔢 رتّب' : '🔢 Arrange'}</h4>
            <p className="text-sm font-bold">{question}</p>
            <div className="space-y-1.5">
              {quiz.correct_order.map((item: any, i: number) => {
                const text = typeof item === 'string' ? item : item[lang] || item.ar || item.en || '';
                return <div key={i} className="p-2.5 rounded-lg bg-card border border-border text-sm font-semibold flex items-center gap-2"><span className="w-6 h-6 rounded-full bg-indigo-500 text-white text-xs flex items-center justify-center font-bold">{i + 1}</span>{text}</div>;
              })}
            </div>
          </div>
        );
      }

      return null;
    };

    return (
      <div className="space-y-4 px-4 pb-28 pt-4 max-w-lg mx-auto">
        {/* Lesson header */}
        <div className={cn("p-5 rounded-[24px] text-center border border-border", TRACK_BG[selectedTrack?.id || ''] || 'bg-card')}>
          <span className="text-4xl">{ls.emoji}</span>
          <h2 className="text-lg font-black mt-2">{ls.title}</h2>
          <div className="flex items-center justify-center gap-2 mt-1">
            {ls.level_name && <span className="text-xs text-muted-foreground">{ls.level_name}</span>}
            <span className="text-xs text-muted-foreground">•</span>
            <span className="text-xs text-muted-foreground">{lang === 'ar' ? `درس ${ls.lesson}` : `Lesson ${ls.lesson}`}</span>
            <span className="text-xs text-muted-foreground">•</span>
            <span className="text-xs font-bold text-emerald-500">{ls.xp} XP</span>
          </div>
        </div>

        {/* Lesson content */}
        {renderContent()}

        {/* Quiz */}
        {renderQuiz()}

        {/* Navigation */}
        <div className="flex items-center justify-between pt-2">
          <button onClick={() => { if (ls.has_prev && selectedTrack) loadAcademyLesson(selectedTrack.id, ls.id - 1); }}
            disabled={!ls.has_prev}
            className="px-4 py-2.5 rounded-xl bg-muted text-sm font-bold disabled:opacity-30 transition-all"
          >
            {isRTL ? '→' : '←'} {lang === 'ar' ? 'السابق' : 'Previous'}
          </button>
          <span className="text-xs font-bold text-muted-foreground">{ls.id}</span>
          <button onClick={() => { if (ls.has_next && selectedTrack) loadAcademyLesson(selectedTrack.id, ls.id + 1); }}
            disabled={!ls.has_next}
            className="px-4 py-2.5 rounded-xl bg-primary text-primary-foreground text-sm font-bold disabled:opacity-30 transition-all"
          >
            {lang === 'ar' ? 'التالي' : 'Next'} {isRTL ? '←' : '→'}
          </button>
        </div>
      </div>
    );
  };

  // ═══════ MAIN RENDER ═══════
  return (
    <div className="min-h-screen bg-background text-foreground" dir={isRTL ? 'rtl' : 'ltr'}>
      <TopBar />
      {view === 'home' && renderHome()}
      {view === 'play' && renderPlay()}
      {view === 'course' && renderCourse()}
      {view === 'course_detail' && renderCourseDetail()}
      {view === 'letter_lesson' && renderLetterLesson()}
      {view === 'shield' && renderShield()}
      {view === 'profile' && renderProfile()}
      {view === 'academy' && renderAcademy()}
      {view === 'academy_track' && renderAcademyTrack()}
      {view === 'academy_lesson' && renderAcademyLesson()}
    </div>
  );
}
