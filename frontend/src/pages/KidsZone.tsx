import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Star, Flame, Trophy, Coins, ChevronRight, ChevronLeft, Shield, BookOpen,
  Gamepad2, Lock, Play, Zap, TrendingUp, Gift, ArrowLeft, Sparkles, Map,
  User, Crown, CheckCircle, Circle, Volume2,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import QuizGame from '@/components/games/QuizGame';
import MemoryGame from '@/components/games/MemoryGame';
import DragDropGame from '@/components/games/DragDropGame';
import ScenarioGame from '@/components/games/ScenarioGame';

const API = import.meta.env.REACT_APP_BACKEND_URL || '';

// ═══════ TYPES ═══════
interface GameData {
  type: 'quiz' | 'memory' | 'drag_drop' | 'scenario';
  id: string;
  title: string;
  emoji: string;
  xp: number;
  [key: string]: any;
}

interface DailyGames {
  day: number;
  total_xp: number;
  games: GameData[];
  games_count: number;
}

interface KidProfile {
  user_id: string;
  total_xp: number;
  level: number;
  streak_days: number;
  games_completed: number;
  coins: number;
  badges: string[];
}

interface ShieldLesson {
  id: string;
  theme: string;
  icon: string;
  title: string;
  content: string;
  key_lesson: string;
}

// ═══════ TABS ═══════
type MainView = 'home' | 'play' | 'shield' | 'journey' | 'profile';

const GAME_COLORS: Record<string, string> = {
  quiz: 'from-blue-500 to-cyan-400',
  memory: 'from-emerald-500 to-teal-400',
  drag_drop: 'from-orange-500 to-amber-400',
  scenario: 'from-violet-500 to-indigo-400',
};

const GAME_BG: Record<string, string> = {
  quiz: 'from-blue-500/15 to-cyan-500/10 border-blue-400/20',
  memory: 'from-emerald-500/15 to-teal-500/10 border-emerald-400/20',
  drag_drop: 'from-orange-500/15 to-amber-500/10 border-orange-400/20',
  scenario: 'from-violet-500/15 to-indigo-500/10 border-violet-400/20',
};

export default function KidsZone() {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'en';
  const isRTL = ['ar'].includes(lang);

  // ═══════ STATE ═══════
  const [view, setView] = useState<MainView>('home');
  const [dailyGames, setDailyGames] = useState<DailyGames | null>(null);
  const [profile, setProfile] = useState<KidProfile | null>(null);
  const [currentGameIdx, setCurrentGameIdx] = useState(0);
  const [completedGames, setCompletedGames] = useState<Set<string>>(new Set());
  const [earnedXP, setEarnedXP] = useState(0);
  const [loading, setLoading] = useState(false);
  const [shieldLessons, setShieldLessons] = useState<ShieldLesson[]>([]);
  const [shieldFilter, setShieldFilter] = useState('all');
  const [expandedLesson, setExpandedLesson] = useState<string | null>(null);
  const [showReward, setShowReward] = useState(false);
  const [journeyDays, setJourneyDays] = useState<number[]>([]);

  // User ID for tracking
  const userId = useMemo(() => {
    let id = localStorage.getItem('kids_user_id');
    if (!id) {
      id = 'kid_' + Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
      localStorage.setItem('kids_user_id', id);
    }
    return id;
  }, []);

  // ═══════ LOADERS ═══════
  const loadDailyGames = useCallback(async () => {
    setLoading(true);
    try {
      const r = await fetch(`${API}/api/kids-learn/daily-games?locale=${lang}`);
      const d = await r.json();
      if (d.success) setDailyGames(d);
    } catch { toast.error(t('genericError') || 'Something went wrong'); }
    setLoading(false);
  }, [lang, t]);

  const loadProfile = useCallback(async () => {
    try {
      const r = await fetch(`${API}/api/kids-learn/profile/${userId}`);
      const d = await r.json();
      if (d.success) setProfile(d.profile);
    } catch {}
  }, [userId]);

  const loadShieldLessons = useCallback(async () => {
    try {
      const r = await fetch(`${API}/api/kids-learn/digital-shield?locale=${lang}&theme=${shieldFilter}`);
      const d = await r.json();
      if (d.success) setShieldLessons(d.lessons);
    } catch {}
  }, [lang, shieldFilter]);

  useEffect(() => {
    loadDailyGames();
    loadProfile();
  }, [loadDailyGames, loadProfile]);

  useEffect(() => {
    if (view === 'shield') loadShieldLessons();
  }, [view, shieldFilter, loadShieldLessons]);

  // ═══════ GAME COMPLETION ═══════
  const handleGameComplete = async (gameId: string, correct: boolean, xp: number) => {
    setCompletedGames(prev => new Set([...prev, gameId]));
    setEarnedXP(prev => prev + xp);

    // Save result to backend
    try {
      await fetch(`${API}/api/kids-learn/game-result`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          game_id: gameId,
          day: dailyGames?.day || 0,
          score: correct ? 1 : 0,
          max_score: 1,
          xp_earned: xp,
          time_seconds: 0,
        }),
      });
      loadProfile();
    } catch {}

    // Move to next game after delay
    if (dailyGames && currentGameIdx < dailyGames.games.length - 1) {
      setTimeout(() => setCurrentGameIdx(prev => prev + 1), 2500);
    } else if (dailyGames && currentGameIdx === dailyGames.games.length - 1) {
      setTimeout(() => {
        setShowReward(true);
      }, 2500);
    }
  };

  const handleWatchAd = async () => {
    // Simulate watching a reward video ad
    toast.success(t('watchingAd') || 'Watching reward video...');
    await new Promise(r => setTimeout(r, 2000));
    try {
      const r = await fetch(`${API}/api/kids-learn/reward-ad?user_id=${userId}&coins=10`, { method: 'POST' });
      const d = await r.json();
      if (d.success) {
        toast.success(`🪙 +${d.earned} ${t('coinsEarned') || 'coins earned!'}`);
        loadProfile();
      }
    } catch {}
  };

  // ═══════ SHIELD THEME CONFIGS ═══════
  const SHIELD_THEME_COLORS: Record<string, string> = {
    deepfakes: 'from-red-500/15 to-orange-500/10 border-red-400/30',
    privacy: 'from-blue-500/15 to-indigo-500/10 border-blue-400/30',
    social_media: 'from-pink-500/15 to-rose-500/10 border-pink-400/30',
    misinformation: 'from-amber-500/15 to-yellow-500/10 border-amber-400/30',
    ethics: 'from-emerald-500/15 to-teal-500/10 border-emerald-400/30',
    safety: 'from-violet-500/15 to-purple-500/10 border-violet-400/30',
  };
  const SHIELD_EMOJI: Record<string, string> = {
    deepfakes: '🎭', privacy: '🔒', social_media: '📱',
    misinformation: '📰', ethics: '⚖️', safety: '🛡️',
  };

  // ═══════ RENDER: TOP BAR ═══════
  const renderTopBar = () => (
    <div className="flex items-center gap-2 px-4 py-3 bg-gradient-to-r from-indigo-900/40 to-purple-900/30 border-b border-white/5">
      {view !== 'home' && (
        <button onClick={() => { setView('home'); setShowReward(false); }} className="p-2 rounded-xl bg-white/5 hover:bg-white/10 transition-all mr-1">
          <ArrowLeft className="h-4 w-4" />
        </button>
      )}
      {/* Noor Avatar */}
      <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-lg shadow-lg shadow-amber-500/20 border-2 border-amber-300/30">
        ✨
      </div>
      <div className="flex-1 min-w-0">
        <h1 className="text-sm font-black bg-gradient-to-r from-amber-200 to-orange-200 bg-clip-text text-transparent truncate">
          {t('noorAcademy') || 'Noor Academy'}
        </h1>
        <div className="flex items-center gap-1">
          <Crown className="h-3 w-3 text-amber-400" />
          <span className="text-[10px] text-amber-400/80 font-bold">
            {t('level') || 'Level'} {profile?.level || 1}
          </span>
        </div>
      </div>
      {/* Stats */}
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-orange-500/15 border border-orange-400/20">
          <Flame className="h-3.5 w-3.5 text-orange-400" />
          <span className="text-xs font-black text-orange-400">{profile?.streak_days || 0}</span>
        </div>
        <div className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-amber-500/15 border border-amber-400/20">
          <Coins className="h-3.5 w-3.5 text-amber-400" />
          <span className="text-xs font-black text-amber-400">{profile?.coins || 0}</span>
        </div>
        <div className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-emerald-500/15 border border-emerald-400/20">
          <Zap className="h-3.5 w-3.5 text-emerald-400" />
          <span className="text-xs font-black text-emerald-400">{profile?.total_xp || 0}</span>
        </div>
      </div>
    </div>
  );

  // ═══════ RENDER: XP PROGRESS BAR ═══════
  const renderXPBar = () => {
    const xp = profile?.total_xp || 0;
    const level = profile?.level || 1;
    const xpInLevel = xp % 100;
    return (
      <div className="px-4 py-2">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[10px] font-bold text-foreground/40">{t('level') || 'Level'} {level}</span>
          <span className="text-[10px] font-bold text-foreground/40">{xpInLevel}/100 XP</span>
        </div>
        <div className="h-2 rounded-full bg-white/5 overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full"
            animate={{ width: `${xpInLevel}%` }}
            transition={{ type: 'spring', stiffness: 200 }}
          />
        </div>
      </div>
    );
  };

  // ═══════ RENDER: HOME VIEW ═══════
  const renderHome = () => (
    <div className="space-y-4 pb-24">
      {/* XP Bar */}
      {renderXPBar()}

      {/* Welcome Banner */}
      <div className="mx-4 p-5 rounded-3xl bg-gradient-to-br from-indigo-500/20 via-purple-500/15 to-pink-500/10 border border-indigo-400/20 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-amber-400/10 to-transparent rounded-bl-full" />
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative z-10"
        >
          <h2 className="text-xl font-black text-foreground">
            {t('welcomeBack') || 'Welcome Back!'} 👋
          </h2>
          <p className="text-sm text-foreground/60 mt-1">
            {t('readyToLearn') || "Ready for today's adventure?"}
          </p>
          {/* Streak */}
          {(profile?.streak_days || 0) > 0 && (
            <div className="mt-3 flex items-center gap-2 px-3 py-2 rounded-xl bg-orange-500/15 border border-orange-400/20 w-fit">
              <Flame className="h-4 w-4 text-orange-400" />
              <span className="text-xs font-bold text-orange-300">
                {profile?.streak_days} {t('dayStreak') || 'day streak!'} 🔥
              </span>
            </div>
          )}
        </motion.div>
      </div>

      {/* Today's Games Card */}
      <div className="mx-4">
        <motion.button
          whileTap={{ scale: 0.98 }}
          onClick={() => { setView('play'); setCurrentGameIdx(0); setShowReward(false); }}
          className="w-full p-5 rounded-3xl bg-gradient-to-br from-emerald-500/20 to-cyan-500/10 border-2 border-emerald-400/25 shadow-lg shadow-emerald-500/5 text-start transition-all hover:border-emerald-400/40"
        >
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-400 to-cyan-400 flex items-center justify-center text-2xl shadow-lg shadow-emerald-500/30">
              🎮
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-black text-foreground">{t('todaysGames') || "Today's Games"}</h3>
              <p className="text-xs text-foreground/50 mt-0.5">
                {dailyGames?.games_count || 4} {t('gamesAvailable') || 'games'} • {dailyGames?.total_xp || 60} XP
              </p>
              {completedGames.size > 0 && (
                <div className="flex items-center gap-1 mt-1">
                  <CheckCircle className="h-3 w-3 text-emerald-400" />
                  <span className="text-[10px] text-emerald-400 font-bold">
                    {completedGames.size}/{dailyGames?.games_count || 4} {t('completed') || 'completed'}
                  </span>
                </div>
              )}
            </div>
            <div className="p-3 rounded-2xl bg-emerald-500/20">
              <Play className="h-6 w-6 text-emerald-400" />
            </div>
          </div>
          {/* Mini game icons */}
          <div className="flex items-center gap-2 mt-4">
            {dailyGames?.games.map((g, i) => (
              <div key={g.id} className={cn(
                "flex-1 py-2 rounded-xl text-center text-xs font-bold border transition-all",
                completedGames.has(g.id)
                  ? "bg-emerald-500/20 border-emerald-400/30 text-emerald-400"
                  : `bg-gradient-to-r ${GAME_BG[g.type]} text-foreground/70`
              )}>
                <span className="text-base">{g.emoji}</span>
              </div>
            ))}
          </div>
        </motion.button>
      </div>

      {/* Category Cards Grid */}
      <div className="grid grid-cols-2 gap-3 px-4">
        {/* Digital Shield */}
        <motion.button
          whileTap={{ scale: 0.97 }}
          onClick={() => setView('shield')}
          className="p-4 rounded-2xl bg-gradient-to-br from-violet-500/15 to-indigo-500/10 border border-violet-400/20 text-start transition-all hover:border-violet-400/30"
        >
          <span className="text-3xl">🛡️</span>
          <h3 className="text-sm font-bold mt-2 text-foreground">{t('digitalShield')}</h3>
          <p className="text-[10px] text-foreground/40 mt-0.5">30 {t('lessons') || 'lessons'}</p>
        </motion.button>

        {/* Journey Map */}
        <motion.button
          whileTap={{ scale: 0.97 }}
          onClick={() => setView('journey')}
          className="p-4 rounded-2xl bg-gradient-to-br from-amber-500/15 to-orange-500/10 border border-amber-400/20 text-start transition-all hover:border-amber-400/30"
        >
          <span className="text-3xl">🗺️</span>
          <h3 className="text-sm font-bold mt-2 text-foreground">{t('learningJourney') || 'Learning Journey'}</h3>
          <p className="text-[10px] text-foreground/40 mt-0.5">365 {t('days') || 'days'}</p>
        </motion.button>

        {/* Profile */}
        <motion.button
          whileTap={{ scale: 0.97 }}
          onClick={() => setView('profile')}
          className="p-4 rounded-2xl bg-gradient-to-br from-pink-500/15 to-rose-500/10 border border-pink-400/20 text-start transition-all hover:border-pink-400/30"
        >
          <span className="text-3xl">🏆</span>
          <h3 className="text-sm font-bold mt-2 text-foreground">{t('myProgress') || 'My Progress'}</h3>
          <p className="text-[10px] text-foreground/40 mt-0.5">
            {profile?.games_completed || 0} {t('gamesPlayed') || 'games played'}
          </p>
        </motion.button>

        {/* Bonus Coins */}
        <motion.button
          whileTap={{ scale: 0.97 }}
          onClick={handleWatchAd}
          className="p-4 rounded-2xl bg-gradient-to-br from-amber-500/20 to-yellow-500/10 border border-amber-400/25 text-start transition-all hover:border-amber-400/35 relative overflow-hidden"
        >
          <div className="absolute top-1 right-1 px-2 py-0.5 rounded-lg bg-amber-500/30 text-[8px] font-black text-amber-300">{t('bonus') || 'BONUS'}</div>
          <span className="text-3xl">🎬</span>
          <h3 className="text-sm font-bold mt-2 text-foreground">{t('watchForCoins') || 'Watch & Earn'}</h3>
          <p className="text-[10px] text-foreground/40 mt-0.5">+10 🪙 {t('coins') || 'coins'}</p>
        </motion.button>
      </div>

      {/* Quick Stats Row */}
      <div className="mx-4 grid grid-cols-3 gap-2">
        <div className="p-3 rounded-2xl bg-white/5 border border-white/5 text-center">
          <Zap className="h-5 w-5 text-emerald-400 mx-auto" />
          <p className="text-lg font-black text-foreground mt-1">{profile?.total_xp || 0}</p>
          <p className="text-[10px] text-foreground/40">XP</p>
        </div>
        <div className="p-3 rounded-2xl bg-white/5 border border-white/5 text-center">
          <Flame className="h-5 w-5 text-orange-400 mx-auto" />
          <p className="text-lg font-black text-foreground mt-1">{profile?.streak_days || 0}</p>
          <p className="text-[10px] text-foreground/40">{t('streak') || 'Streak'}</p>
        </div>
        <div className="p-3 rounded-2xl bg-white/5 border border-white/5 text-center">
          <Trophy className="h-5 w-5 text-amber-400 mx-auto" />
          <p className="text-lg font-black text-foreground mt-1">{profile?.level || 1}</p>
          <p className="text-[10px] text-foreground/40">{t('level') || 'Level'}</p>
        </div>
      </div>
    </div>
  );

  // ═══════ RENDER: PLAY VIEW (GAME ENGINE) ═══════
  const renderPlay = () => {
    if (!dailyGames || dailyGames.games.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center h-[60vh]">
          <span className="text-5xl mb-4">🎮</span>
          <p className="text-foreground/50">{t('loadingGames') || 'Loading games...'}</p>
        </div>
      );
    }

    // Show reward screen after all games completed
    if (showReward) {
      return (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex flex-col items-center justify-center h-[70vh] px-6 text-center"
        >
          <motion.div
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ repeat: Infinity, duration: 2 }}
            className="text-7xl mb-6"
          >
            🏆
          </motion.div>
          <h2 className="text-2xl font-black bg-gradient-to-r from-amber-200 to-orange-200 bg-clip-text text-transparent">
            {t('allGamesComplete') || 'All Games Complete!'}
          </h2>
          <p className="text-lg font-bold text-foreground/60 mt-2">
            +{earnedXP} XP {t('earned') || 'earned'}
          </p>
          <div className="flex items-center gap-4 mt-6">
            <div className="px-4 py-3 rounded-2xl bg-emerald-500/15 border border-emerald-400/20 text-center">
              <Zap className="h-5 w-5 text-emerald-400 mx-auto" />
              <p className="text-sm font-bold text-emerald-400 mt-1">{earnedXP} XP</p>
            </div>
            <div className="px-4 py-3 rounded-2xl bg-orange-500/15 border border-orange-400/20 text-center">
              <Flame className="h-5 w-5 text-orange-400 mx-auto" />
              <p className="text-sm font-bold text-orange-400 mt-1">{profile?.streak_days || 1} 🔥</p>
            </div>
          </div>
          <div className="flex gap-3 mt-8">
            <button
              onClick={() => { setView('home'); setShowReward(false); }}
              className="px-6 py-3 rounded-2xl bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-bold shadow-lg shadow-indigo-500/20"
            >
              {t('backToHome') || 'Back Home'}
            </button>
            <button
              onClick={handleWatchAd}
              className="px-6 py-3 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold shadow-lg shadow-amber-500/20"
            >
              🎬 +10 🪙
            </button>
          </div>
        </motion.div>
      );
    }

    const game = dailyGames.games[currentGameIdx];
    const progress = ((currentGameIdx) / dailyGames.games.length) * 100;

    return (
      <div className="pb-8">
        {/* Progress Header */}
        <div className="px-4 py-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-foreground/40">
              {t('game') || 'Game'} {currentGameIdx + 1}/{dailyGames.games.length}
            </span>
            <span className="text-xs font-bold text-emerald-400">+{earnedXP} XP</span>
          </div>
          <div className="h-2 rounded-full bg-white/5 overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full"
              animate={{ width: `${progress}%` }}
              transition={{ type: 'spring', stiffness: 200 }}
            />
          </div>
          {/* Game type indicator */}
          <div className="flex items-center gap-2 mt-3">
            {dailyGames.games.map((g, i) => (
              <div key={g.id} className={cn(
                "flex-1 h-1.5 rounded-full transition-all",
                i < currentGameIdx ? "bg-emerald-400" :
                i === currentGameIdx ? `bg-gradient-to-r ${GAME_COLORS[g.type]}` :
                "bg-white/10"
              )} />
            ))}
          </div>
        </div>

        {/* Game Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={game.id}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
          >
            {game.type === 'quiz' && (
              <QuizGame
                question={game.question}
                options={game.options}
                correctIndex={game.correct_index}
                xp={game.xp}
                onComplete={(correct, xp) => handleGameComplete(game.id, correct, xp)}
              />
            )}
            {game.type === 'memory' && (
              <MemoryGame
                cards={game.cards}
                totalPairs={game.total_pairs}
                xp={game.xp}
                onComplete={(correct, xp) => handleGameComplete(game.id, correct, xp)}
              />
            )}
            {game.type === 'drag_drop' && (
              <DragDropGame
                title={game.title}
                items={game.items}
                correctOrder={game.correct_order}
                xp={game.xp}
                onComplete={(correct, xp) => handleGameComplete(game.id, correct, xp)}
              />
            )}
            {game.type === 'scenario' && (
              <ScenarioGame
                scenario={game.scenario}
                options={game.options}
                correctIndex={game.correct_index}
                explanation={game.explanation}
                xp={game.xp}
                onComplete={(correct, xp) => handleGameComplete(game.id, correct, xp)}
              />
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    );
  };

  // ═══════ RENDER: DIGITAL SHIELD ═══════
  const renderShield = () => {
    const themes = ['all', 'deepfakes', 'privacy', 'social_media', 'misinformation', 'ethics', 'safety'];

    return (
      <div className="space-y-4 pb-8 px-4">
        {/* Header */}
        <div className="text-center p-5 rounded-3xl bg-gradient-to-br from-violet-500/15 to-indigo-500/10 border border-violet-400/20">
          <span className="text-5xl">🛡️</span>
          <h2 className="text-xl font-black mt-2 bg-gradient-to-r from-violet-200 to-indigo-200 bg-clip-text text-transparent">{t('digitalShield')}</h2>
          <p className="text-sm text-foreground/60 mt-1">{t('digitalShieldDesc')}</p>
        </div>

        {/* Theme Filters */}
        <div className="flex gap-1.5 overflow-x-auto pb-1 scrollbar-hide">
          {themes.map(th => (
            <button
              key={th}
              onClick={() => setShieldFilter(th)}
              className={cn(
                "flex items-center gap-1 px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap border transition-all shrink-0",
                shieldFilter === th
                  ? "bg-violet-500/20 border-violet-400/40 text-violet-300 shadow-sm"
                  : "bg-white/5 border-border/30 text-muted-foreground hover:bg-muted/20"
              )}
            >
              <span>{th === 'all' ? '✨' : SHIELD_EMOJI[th] || '🛡️'}</span>
              {th === 'all' ? t('allLessons') : t(th)}
            </button>
          ))}
        </div>

        {/* Lesson Cards */}
        <div className="space-y-3">
          {shieldLessons.map((lesson, idx) => {
            const isOpen = expandedLesson === lesson.id;
            const thColor = SHIELD_THEME_COLORS[lesson.theme] || SHIELD_THEME_COLORS.safety;
            const thEmoji = SHIELD_EMOJI[lesson.theme] || '🛡️';

            return (
              <motion.button
                key={lesson.id}
                whileTap={{ scale: 0.98 }}
                onClick={() => setExpandedLesson(isOpen ? null : lesson.id)}
                className={cn(
                  "w-full rounded-2xl border p-4 text-start transition-all duration-300",
                  `bg-gradient-to-br ${thColor}`,
                  isOpen && "ring-2 ring-violet-400/30 shadow-lg"
                )}
              >
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-xl shrink-0 border border-white/10">
                    {thEmoji}
                  </div>
                  <div className="flex-1 min-w-0">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-foreground/50">{t(lesson.theme)} #{idx + 1}</span>
                    <h3 className="font-bold text-sm text-foreground leading-snug">{lesson.title}</h3>
                  </div>
                </div>
                {isOpen && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="mt-3 space-y-3"
                  >
                    <div className="p-3 rounded-xl bg-white/5 border border-white/10">
                      <p className="text-sm leading-relaxed text-foreground/80">{lesson.content}</p>
                    </div>
                    <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
                      <div className="flex items-center gap-2 mb-1">
                        <Star className="h-4 w-4 text-amber-500" />
                        <span className="text-xs font-bold text-amber-600 dark:text-amber-300">{t('keyMoral')}</span>
                      </div>
                      <p className="text-sm font-semibold text-amber-700 dark:text-amber-200">{lesson.key_lesson}</p>
                    </div>
                  </motion.div>
                )}
              </motion.button>
            );
          })}
        </div>
      </div>
    );
  };

  // ═══════ RENDER: JOURNEY MAP ═══════
  const renderJourney = () => {
    const currentDay = new Date().getDate();
    const daysCompleted = profile?.games_completed || 0;
    const totalDays = 30; // Show 30 nodes

    return (
      <div className="pb-8 px-4 space-y-4">
        <div className="text-center p-5 rounded-3xl bg-gradient-to-br from-amber-500/15 to-orange-500/10 border border-amber-400/20">
          <span className="text-5xl">🗺️</span>
          <h2 className="text-xl font-black mt-2 bg-gradient-to-r from-amber-200 to-orange-200 bg-clip-text text-transparent">
            {t('learningJourney') || 'Learning Journey'}
          </h2>
          <p className="text-sm text-foreground/60 mt-1">{t('journeyDesc') || 'Complete daily games to advance on your path!'}</p>
        </div>

        {/* Journey Path */}
        <div className="relative">
          {/* Vertical path line */}
          <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-emerald-400 via-amber-400 to-gray-700" />

          <div className="space-y-3">
            {Array.from({ length: totalDays }, (_, i) => {
              const day = i + 1;
              const isCompleted = day <= daysCompleted;
              const isCurrent = day === daysCompleted + 1;
              const isLocked = day > daysCompleted + 1;
              const categories = ['📖', '🕌', '🛡️', '⚖️', '🤲'];
              const cat = categories[i % categories.length];

              return (
                <motion.div
                  key={day}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.03 }}
                  className="flex items-center gap-4"
                >
                  {/* Node */}
                  <div className={cn(
                    "w-12 h-12 rounded-2xl flex items-center justify-center text-lg z-10 border-2 shrink-0 transition-all",
                    isCompleted ? "bg-emerald-500/30 border-emerald-400/50 shadow-lg shadow-emerald-500/20" :
                    isCurrent ? "bg-amber-500/30 border-amber-400/50 shadow-lg shadow-amber-500/20 animate-pulse" :
                    "bg-gray-800/50 border-gray-700/30"
                  )}>
                    {isCompleted ? <CheckCircle className="h-5 w-5 text-emerald-400" /> :
                     isCurrent ? <span className="text-xl">{cat}</span> :
                     <Lock className="h-4 w-4 text-gray-600" />}
                  </div>

                  {/* Label */}
                  <div className={cn(
                    "flex-1 p-3 rounded-xl border transition-all",
                    isCompleted ? "bg-emerald-500/10 border-emerald-400/20" :
                    isCurrent ? "bg-amber-500/10 border-amber-400/20" :
                    "bg-gray-800/20 border-gray-700/20"
                  )}>
                    <div className="flex items-center justify-between">
                      <span className={cn(
                        "text-sm font-bold",
                        isCompleted ? "text-emerald-400" :
                        isCurrent ? "text-amber-400" :
                        "text-gray-600"
                      )}>
                        {t('day') || 'Day'} {day} {cat}
                      </span>
                      {isCompleted && <span className="text-[10px] text-emerald-400 font-bold">✓ +60 XP</span>}
                      {isCurrent && (
                        <button
                          onClick={() => { setView('play'); setCurrentGameIdx(0); }}
                          className="px-3 py-1 rounded-lg bg-amber-500/20 text-amber-400 text-xs font-bold"
                        >
                          {t('playNow') || 'Play'} ▶
                        </button>
                      )}
                      {isLocked && <Lock className="h-3 w-3 text-gray-700" />}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    );
  };

  // ═══════ RENDER: PROFILE ═══════
  const renderProfile = () => (
    <div className="pb-8 px-4 space-y-4">
      {/* Avatar Card */}
      <div className="text-center p-6 rounded-3xl bg-gradient-to-br from-pink-500/15 to-rose-500/10 border border-pink-400/20">
        <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-4xl mx-auto shadow-xl shadow-amber-500/20 border-2 border-amber-300/30">
          ✨
        </div>
        <h2 className="text-xl font-black mt-3 text-foreground">{t('noorExplorer') || 'Noor Explorer'}</h2>
        <div className="flex items-center justify-center gap-2 mt-1">
          <Crown className="h-4 w-4 text-amber-400" />
          <span className="text-sm font-bold text-amber-400">{t('level') || 'Level'} {profile?.level || 1}</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-3">
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-400/20 text-center">
          <Zap className="h-6 w-6 text-emerald-400 mx-auto" />
          <p className="text-2xl font-black text-foreground mt-2">{profile?.total_xp || 0}</p>
          <p className="text-xs text-foreground/40">{t('totalXP') || 'Total XP'}</p>
        </div>
        <div className="p-4 rounded-2xl bg-orange-500/10 border border-orange-400/20 text-center">
          <Flame className="h-6 w-6 text-orange-400 mx-auto" />
          <p className="text-2xl font-black text-foreground mt-2">{profile?.streak_days || 0}</p>
          <p className="text-xs text-foreground/40">{t('dayStreak') || 'Day Streak'}</p>
        </div>
        <div className="p-4 rounded-2xl bg-blue-500/10 border border-blue-400/20 text-center">
          <Gamepad2 className="h-6 w-6 text-blue-400 mx-auto" />
          <p className="text-2xl font-black text-foreground mt-2">{profile?.games_completed || 0}</p>
          <p className="text-xs text-foreground/40">{t('gamesPlayed') || 'Games Played'}</p>
        </div>
        <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-400/20 text-center">
          <Coins className="h-6 w-6 text-amber-400 mx-auto" />
          <p className="text-2xl font-black text-foreground mt-2">{profile?.coins || 0}</p>
          <p className="text-xs text-foreground/40">{t('coins') || 'Coins'}</p>
        </div>
      </div>

      {/* XP Progress to Next Level */}
      <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-bold text-foreground">{t('nextLevel') || 'Next Level'}</span>
          <span className="text-xs text-emerald-400 font-bold">{(profile?.total_xp || 0) % 100}/100 XP</span>
        </div>
        <div className="h-3 rounded-full bg-white/5 overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full"
            animate={{ width: `${(profile?.total_xp || 0) % 100}%` }}
          />
        </div>
      </div>

      {/* Bonus Section */}
      <motion.button
        whileTap={{ scale: 0.97 }}
        onClick={handleWatchAd}
        className="w-full p-4 rounded-2xl bg-gradient-to-r from-amber-500/20 to-yellow-500/10 border border-amber-400/25 flex items-center gap-3"
      >
        <span className="text-3xl">🎬</span>
        <div className="flex-1 text-start">
          <h3 className="text-sm font-bold text-foreground">{t('watchForCoins') || 'Watch & Earn Coins'}</h3>
          <p className="text-[10px] text-foreground/40">{t('watchAdDesc') || 'Watch a short video to earn bonus coins!'}</p>
        </div>
        <div className="px-3 py-2 rounded-xl bg-amber-500/20 text-amber-400 font-bold text-xs">+10 🪙</div>
      </motion.button>
    </div>
  );

  // ═══════ RENDER: BOTTOM NAV ═══════
  const renderBottomNav = () => {
    if (view === 'play') return null;

    const tabs: { id: MainView; emoji: string; label: string }[] = [
      { id: 'home', emoji: '🏠', label: t('home') || 'Home' },
      { id: 'play', emoji: '🎮', label: t('play') || 'Play' },
      { id: 'shield', emoji: '🛡️', label: t('shield') || 'Shield' },
      { id: 'journey', emoji: '🗺️', label: t('journey') || 'Journey' },
      { id: 'profile', emoji: '🏆', label: t('profile') || 'Profile' },
    ];

    return (
      <div className="fixed bottom-0 left-0 right-0 z-50 bg-gray-950/95 border-t border-white/5 backdrop-blur-xl safe-area-pb">
        <div className="flex items-center justify-around py-2 px-2 max-w-lg mx-auto">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => {
                if (tab.id === 'play') {
                  setView('play');
                  setCurrentGameIdx(0);
                  setShowReward(false);
                } else {
                  setView(tab.id);
                }
              }}
              className={cn(
                "flex flex-col items-center gap-0.5 px-3 py-1.5 rounded-xl transition-all min-w-[52px]",
                view === tab.id ? "bg-white/10" : "opacity-50 hover:opacity-80"
              )}
            >
              <span className="text-lg">{tab.emoji}</span>
              <span className="text-[9px] font-bold">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>
    );
  };

  // ═══════ LOADING SPINNER ═══════
  const LoadingSpinner = () => (
    <div className="flex items-center justify-center h-[50vh]">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
        className="w-10 h-10 border-3 border-emerald-400 border-t-transparent rounded-full"
      />
    </div>
  );

  // ═══════ MAIN RENDER ═══════
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 text-foreground" dir={isRTL ? 'rtl' : 'ltr'}>
      {renderTopBar()}
      <div className="max-w-lg mx-auto">
        {loading && !dailyGames ? <LoadingSpinner /> : (
          <>
            {view === 'home' && renderHome()}
            {view === 'play' && renderPlay()}
            {view === 'shield' && renderShield()}
            {view === 'journey' && renderJourney()}
            {view === 'profile' && renderProfile()}
          </>
        )}
      </div>
      {renderBottomNav()}
    </div>
  );
}
