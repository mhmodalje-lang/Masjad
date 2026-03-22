import { useState, useEffect, useCallback } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { useAuth } from '@/hooks/useAuth';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Flame, Trophy, Star, Gift, Play, Lock, ShieldCheck,
  TrendingUp, Crown, Sparkles, ChevronRight, ArrowLeft,
  Zap, Building2, Target, Award, Eye
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

// Stage/Rank translation key maps
const STAGE_KEY_MAP: Record<string, string> = {
  foundation: 'stageFoundation', walls: 'stageWalls', pillars: 'stagePillars',
  dome_base: 'stageDomeBase', dome: 'stageDome', minaret: 'stageMinaret',
  garden: 'stageGarden', golden_dome: 'stageGoldenDome', complete: 'stageComplete',
};
const STAGE_EMOJI: Record<string, string> = {
  foundation: '🧱', walls: '🏗️', pillars: '🏛️', dome_base: '⛪',
  dome: '🕌', minaret: '🗼', garden: '🌳', golden_dome: '✨', complete: '🕋',
};
const RANK_KEY_MAP: Record<string, string> = {
  seeker: 'rankSeeker', learner: 'rankLearner', devoted: 'rankDevoted',
  steadfast: 'rankSteadfast', knowledgeable: 'rankKnowledgeable', hafiz: 'rankHafiz',
  mumin: 'rankMumin', muhsin: 'rankMuhsin', muttaqin: 'rankMuttaqin',
};
const RANK_EMOJI: Record<string, string> = {
  seeker: '🌱', learner: '📖', devoted: '🤲', steadfast: '⭐',
  knowledgeable: '🌟', hafiz: '📜', mumin: '💎', muhsin: '🌙', muttaqin: '☀️',
};

interface ParentalChallenge { challenge_id: string; question: string; }

export default function PointsBalance() {
  const { t, dir } = useLocale();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [mode, setMode] = useState<'kids' | 'adults'>('adults');
  const [balance, setBalance] = useState<any>(null);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [history, setHistory] = useState<any[]>([]);
  const [catalog, setCatalog] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'balance' | 'leaderboard' | 'history' | 'shop'>('balance');
  const [showParentalGate, setShowParentalGate] = useState(false);
  const [challenge, setChallenge] = useState<ParentalChallenge | null>(null);
  const [gateAnswer, setGateAnswer] = useState('');
  const [gatePass, setGatePass] = useState<string | null>(null);
  const [pendingAction, setPendingAction] = useState<(() => void) | null>(null);

  const userId = user?.id || 'guest_' + (typeof window !== 'undefined' ? window.navigator.userAgent.slice(-8) : 'x');

  const fetchAll = useCallback(async () => {
    setLoading(true);
    try {
      const [bal, lb, hist, cat] = await Promise.all([
        fetch(`${BACKEND_URL}/api/points/balance?user_id=${userId}&mode=${mode}`).then(r => r.json()),
        fetch(`${BACKEND_URL}/api/points/leaderboard?mode=${mode}&limit=10`).then(r => r.json()),
        fetch(`${BACKEND_URL}/api/points/history?user_id=${userId}&mode=${mode}&limit=20`).then(r => r.json()),
        fetch(`${BACKEND_URL}/api/rewards/premium-catalog?mode=${mode}`).then(r => r.json()),
      ]);
      setBalance(bal);
      setLeaderboard(lb.leaderboard || []);
      setHistory(hist.transactions || []);
      setCatalog(cat.catalog || []);
    } catch (e) { console.error(e); }
    setLoading(false);
  }, [mode, userId]);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  // Translate a mosque stage name
  const tStage = (stage: string) => t(STAGE_KEY_MAP[stage] || stage);
  // Translate a spiritual rank name
  const tRank = (rank: string) => t(RANK_KEY_MAP[rank] || rank);

  // Parental Gate
  const requestParentalGate = async (onPass: () => void) => {
    if (mode !== 'kids') { onPass(); return; }
    if (gatePass) {
      try {
        const res = await fetch(`${BACKEND_URL}/api/parental-gate/check-pass?user_id=${userId}&token=${gatePass}`);
        const d = await res.json();
        if (d.valid) { onPass(); return; }
      } catch {}
    }
    try {
      const res = await fetch(`${BACKEND_URL}/api/parental-gate/challenge?user_id=${userId}`);
      const d = await res.json();
      setChallenge(d);
      setPendingAction(() => onPass);
      setShowParentalGate(true);
      setGateAnswer('');
    } catch { toast.error(t('verificationFailed')); }
  };

  const verifyGate = async () => {
    if (!challenge) return;
    try {
      const res = await fetch(`${BACKEND_URL}/api/parental-gate/verify`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, challenge_id: challenge.challenge_id, answer: parseInt(gateAnswer) }),
      });
      const d = await res.json();
      if (d.passed) {
        setGatePass(d.pass_token);
        setShowParentalGate(false);
        toast.success(t('accessGranted'));
        if (pendingAction) pendingAction();
      } else {
        toast.error(d.message === 'too_many_attempts' ? t('tooManyAttempts') : t('wrongAnswer').replace('{n}', d.attempts_remaining));
        if (d.message === 'too_many_attempts') setShowParentalGate(false);
      }
    } catch { toast.error(t('verificationFailed')); }
  };

  const watchAd = () => {
    const doWatch = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/rewards/ad-watched`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId, mode, ad_type: 'rewarded' }),
        });
        const d = await res.json();
        if (d.success) {
          toast.success(`+${d.points_earned} ${mode === 'kids' ? t('goldenBricksTitle') : t('blessingPointsTitle')}!`);
          fetchAll();
        } else {
          toast.error(d.message === 'daily_ad_limit_reached' ? t('dailyLimitReached').replace('{n}', String(d.max_daily)) : t('adFailed'));
        }
      } catch { toast.error(t('adFailed')); }
    };
    mode === 'kids' ? requestParentalGate(doWatch) : doWatch();
  };

  const pts = mode === 'kids' ? (balance?.golden_bricks || 0) : (balance?.blessing_points || 0);
  const streak = balance?.streak || 0;
  const mosqueStage = balance?.mosque?.current?.stage || 'foundation';
  const rankName = balance?.rank?.current?.rank || 'seeker';
  const progressPercent = mode === 'kids' ? (balance?.mosque?.progress_percent || 0) : (balance?.rank?.progress_percent || 0);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}>
          <Sparkles className="h-8 w-8 text-primary" />
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pb-24 pt-2 px-4" dir={dir}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <button onClick={() => navigate(-1)} className="p-2 rounded-xl neu-card">
          <ArrowLeft className="h-5 w-5 text-foreground" />
        </button>
        <h1 className="text-lg font-bold text-foreground">
          {mode === 'kids' ? `🧱 ${t('goldenBricksTitle')}` : `🤲 ${t('blessingPointsTitle')}`}
        </h1>
        <div className="flex gap-1 p-1 rounded-xl bg-muted/50 border border-border/30">
          <button onClick={() => setMode('kids')} className={cn("px-4 py-2.5 rounded-lg text-xs font-bold transition-all min-h-[44px]", mode === 'kids' ? "bg-amber-500 text-white" : "text-muted-foreground")}>{t('pointsKids')}</button>
          <button onClick={() => setMode('adults')} className={cn("px-4 py-2.5 rounded-lg text-xs font-bold transition-all min-h-[44px]", mode === 'adults' ? "bg-emerald-600 text-white" : "text-muted-foreground")}>{t('pointsAdults')}</button>
        </div>
      </div>

      {/* Points Card */}
      <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
        className={cn("rounded-3xl p-6 text-white relative overflow-hidden mb-4",
          mode === 'kids' ? "bg-gradient-to-br from-amber-500 via-orange-500 to-red-500" : "bg-gradient-to-br from-emerald-600 via-teal-600 to-cyan-700"
        )}>
        <div className="absolute -top-10 -right-10 w-40 h-40 rounded-full bg-white/10" />
        <div className="absolute -bottom-8 -left-8 w-32 h-32 rounded-full bg-white/5" />
        <div className="relative z-10">
          <div className="text-5xl font-black mb-1">{pts.toLocaleString()}</div>
          <p className="text-sm font-medium opacity-90 mb-4">{mode === 'kids' ? t('goldenBricksTitle') : t('blessingPointsTitle')}</p>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <Flame className="h-4 w-4 text-yellow-300" />
              <span className="text-sm font-bold">{t('dayStreak').replace('{n}', String(streak))}</span>
            </div>
            <div className="flex items-center gap-1.5">
              {mode === 'kids' ? (
                <><span className="text-lg">{STAGE_EMOJI[mosqueStage] || '🧱'}</span><span className="text-sm font-bold">{tStage(mosqueStage)}</span></>
              ) : (
                <><span className="text-lg">{RANK_EMOJI[rankName] || '🌱'}</span><span className="text-sm font-bold">{tRank(rankName)}</span></>
              )}
            </div>
          </div>
          <div className="mt-3">
            <div className="h-2 rounded-full bg-white/20 overflow-hidden">
              <motion.div initial={{ width: 0 }} animate={{ width: `${progressPercent}%` }} transition={{ duration: 1.5, ease: 'easeOut' }} className="h-full rounded-full bg-white/80" />
            </div>
            <p className="text-xs mt-1 opacity-75">
              {mode === 'kids'
                ? (balance?.mosque?.next ? t('percentToNext').replace('{p}', String(progressPercent)).replace('{next}', tStage(balance.mosque.next.stage)) : t('completeStr'))
                : (balance?.rank?.next ? t('percentToNext').replace('{p}', String(progressPercent)).replace('{next}', tRank(balance.rank.next.rank)) : t('maxRank'))
              }
            </p>
          </div>
        </div>
      </motion.div>

      {/* Watch Ad */}
      <motion.button whileTap={{ scale: 0.97 }} onClick={watchAd}
        className={cn("w-full rounded-2xl p-4 flex items-center gap-3 mb-4 border",
          mode === 'kids' ? "bg-gradient-to-r from-purple-500/20 to-pink-500/20 border-purple-500/30" : "bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border-blue-500/30"
        )}>
        <div className={cn("p-2 rounded-xl", mode === 'kids' ? "bg-purple-500/20" : "bg-blue-500/20")}>
          <Play className={cn("h-5 w-5", mode === 'kids' ? "text-purple-400" : "text-blue-400")} />
        </div>
        <div className="flex-1 text-start">
          <p className="text-sm font-bold text-foreground">{t('watchAdEarn')}</p>
          <p className="text-xs text-muted-foreground">
            {mode === 'kids' ? t('bricksPerAd').replace('{n}', '25') : t('pointsPerAd').replace('{n}', '15')}
          </p>
        </div>
        {mode === 'kids' && <div className="p-1.5 rounded-lg bg-amber-500/20"><Lock className="h-4 w-4 text-amber-500" /></div>}
        <ChevronRight className="h-4 w-4 text-muted-foreground" />
      </motion.button>

      {/* Tabs */}
      <div className="flex gap-1 mb-4 p-1 rounded-2xl bg-muted/30 border border-border/30">
        {([
          { key: 'balance', label: t('tabOverview'), icon: Target },
          { key: 'leaderboard', label: t('tabLeaders'), icon: Trophy },
          { key: 'history', label: t('tabHistory'), icon: TrendingUp },
          { key: 'shop', label: t('tabShop'), icon: Gift },
        ] as const).map(tab => (
          <button key={tab.key} onClick={() => setActiveTab(tab.key)}
            className={cn("flex-1 flex items-center justify-center gap-1 py-3 rounded-xl text-xs font-bold transition-all min-h-[44px]",
              activeTab === tab.key ? "bg-primary text-primary-foreground" : "text-muted-foreground"
            )}>
            <tab.icon className="h-3.5 w-3.5" />{tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        {activeTab === 'balance' && (
          <motion.div key="balance" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-3">
            {mode === 'kids' && balance?.mosque && (
              <div className="rounded-2xl neu-card p-4">
                <h3 className="text-sm font-bold text-foreground mb-3 flex items-center gap-2"><Building2 className="h-4 w-4 text-amber-500"/>{t('mosqueProgress')}</h3>
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-4xl">{STAGE_EMOJI[balance.mosque.current?.stage] || '🧱'}</span>
                  <div>
                    <p className="text-sm font-bold text-foreground">{tStage(balance.mosque.current?.stage || 'foundation')}</p>
                    {balance.mosque.next && (
                      <p className="text-xs text-muted-foreground">{t('nextStage').replace('{name}', tStage(balance.mosque.next.stage)).replace('{n}', String(balance.mosque.next.bricks_needed))}</p>
                    )}
                  </div>
                </div>
              </div>
            )}
            {mode === 'adults' && balance?.rank && (
              <div className="rounded-2xl neu-card p-4">
                <h3 className="text-sm font-bold text-foreground mb-3 flex items-center gap-2"><Crown className="h-4 w-4 text-emerald-500"/>{t('spiritualRank')}</h3>
                <div className="flex items-center gap-3">
                  <span className="text-4xl">{RANK_EMOJI[balance.rank.current?.rank] || '🌱'}</span>
                  <div>
                    <p className="text-sm font-bold text-foreground">{tRank(balance.rank.current?.rank || 'seeker')}</p>
                    {balance.rank.next && (
                      <p className="text-xs text-muted-foreground">{t('nextRank').replace('{name}', tRank(balance.rank.next.rank)).replace('{n}', String(balance.rank.next.points_needed))}</p>
                    )}
                  </div>
                </div>
              </div>
            )}
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-2xl neu-card p-4 text-center">
                <Zap className="h-6 w-6 text-amber-500 mx-auto mb-1" />
                <p className="text-xl font-bold text-foreground">{balance?.total_earned || 0}</p>
                <p className="text-xs text-muted-foreground">{t('totalEarned')}</p>
              </div>
              <div className="rounded-2xl neu-card p-4 text-center">
                <Eye className="h-6 w-6 text-purple-500 mx-auto mb-1" />
                <p className="text-xl font-bold text-foreground">{balance?.ads_watched || 0}</p>
                <p className="text-xs text-muted-foreground">{t('adsWatched')}</p>
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === 'leaderboard' && (
          <motion.div key="leaderboard" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-2">
            {leaderboard.length === 0 && <p className="text-center text-sm text-muted-foreground py-8">{t('noLeadersYet')}</p>}
            {leaderboard.map((entry: any, i: number) => (
              <div key={i} className={cn("rounded-2xl border p-3 flex items-center gap-3",
                i === 0 ? "bg-amber-500/10 border-amber-500/30" : i === 1 ? "bg-muted/30 border-muted-foreground/30" : i === 2 ? "bg-orange-500/10 border-orange-500/30" : "bg-card border-border/30"
              )}>
                <span className={cn("text-lg font-black w-8 text-center",
                  i === 0 ? "text-amber-500" : i === 1 ? "text-muted-foreground" : i === 2 ? "text-orange-500" : "text-muted-foreground"
                )}>{i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `#${i + 1}`}</span>
                <div className="flex-1">
                  <p className="text-sm font-bold text-foreground">{entry.display_name}</p>
                  <p className="text-xs text-muted-foreground">
                    {mode === 'kids' ? `${entry.golden_bricks} ${t('bricks')}` : `${entry.blessing_points} ${t('points')}`}
                    {entry.streak > 0 && ` | ${t('dayStreak').replace('{n}', String(entry.streak))}`}
                  </p>
                </div>
                {mode === 'kids' && <span className="text-lg">{STAGE_EMOJI[entry.mosque_stage] || '🧱'}</span>}
                {mode === 'adults' && <span className="text-lg">{RANK_EMOJI[entry.spiritual_rank] || '🌱'}</span>}
              </div>
            ))}
          </motion.div>
        )}

        {activeTab === 'history' && (
          <motion.div key="history" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-2">
            {history.length === 0 && <p className="text-center text-sm text-muted-foreground py-8">{t('noActivityYet')}</p>}
            {history.map((tx: any, i: number) => (
              <div key={i} className="rounded-2xl neu-card p-3 flex items-center gap-3">
                <div className={cn("p-2 rounded-xl", tx.points > 0 ? "bg-green-500/20" : "bg-red-500/20")}>
                  {tx.points > 0 ? <TrendingUp className="h-4 w-4 text-green-500" /> : <Award className="h-4 w-4 text-red-500" />}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-bold text-foreground">{t(tx.type || 'unknown') !== (tx.type || 'unknown') ? t(tx.type) : (tx.type || '').replace(/_/g, ' ')}</p>
                  <p className="text-xs text-muted-foreground">{tx.created_at?.substring(0, 16)}</p>
                </div>
                <span className={cn("text-sm font-bold", tx.points > 0 ? "text-green-500" : "text-red-500")}>
                  {tx.points > 0 ? '+' : ''}{tx.points}
                </span>
              </div>
            ))}
          </motion.div>
        )}

        {activeTab === 'shop' && (
          <motion.div key="shop" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-2">
            {catalog.map((item: any, i: number) => {
              const isUnlocked = (balance?.unlocked_content || []).includes(item.id);
              return (
                <div key={i} className={cn("rounded-2xl border p-4 space-y-2", isUnlocked ? "bg-green-500/10 border-green-500/30" : "bg-card border-border/30")}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-bold text-foreground">{t(item.title_key) !== item.title_key ? t(item.title_key) : (item.title_key || '').replace(/_/g, ' ')}</p>
                      <p className="text-xs text-muted-foreground">{t(item.type) !== item.type ? t(item.type) : (item.type || '').replace(/_/g, ' ')}</p>
                    </div>
                    {isUnlocked ? (
                      <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-500 text-xs font-bold">{t('unlocked')}</span>
                    ) : (
                      <div className="flex gap-2">
                        {item.unlock_via_ad && (
                          <Button size="sm" variant="outline" className="rounded-xl text-xs gap-1" onClick={() => requestParentalGate(watchAd)}>
                            <Play className="h-3 w-3" />{t('adBtn')}
                          </Button>
                        )}
                        <span className="px-3 py-1 rounded-full bg-amber-500/20 text-amber-500 text-xs font-bold">
                          {mode === 'kids' ? `${item.cost_bricks} 🧱` : `${item.cost_points} ✨`}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Parental Gate Modal */}
      <AnimatePresence>
        {showParentalGate && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
            <motion.div initial={{ scale: 0.9, y: 20 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.9, y: 20 }}
              className="w-full max-w-sm rounded-3xl bg-card border border-border p-6 space-y-4">
              <div className="text-center">
                <ShieldCheck className="h-12 w-12 text-amber-500 mx-auto mb-2" />
                <h2 className="text-lg font-bold text-foreground">{t('parentalSafetyGate')}</h2>
                <p className="text-xs text-muted-foreground mt-1">{t('askParentsSolve')}</p>
              </div>
              <div className="text-center py-4">
                <p className="text-3xl font-black text-primary">{challenge?.question}</p>
              </div>
              <input type="number" className="w-full rounded-2xl bg-background border-2 border-primary/30 px-4 py-3 text-center text-2xl font-bold text-foreground focus:border-primary outline-none"
                placeholder="?" value={gateAnswer} onChange={e => setGateAnswer(e.target.value)} onKeyDown={e => e.key === 'Enter' && verifyGate()} autoFocus />
              <div className="flex gap-2">
                <Button onClick={verifyGate} className="flex-1 rounded-2xl py-3 bg-green-600 hover:bg-green-700 text-white font-bold">
                  <ShieldCheck className="h-4 w-4 mr-1" />{t('verify')}
                </Button>
                <Button onClick={() => setShowParentalGate(false)} variant="outline" className="rounded-2xl py-3">{t('cancel')}</Button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
