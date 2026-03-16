import { useLocale } from '@/hooks/useLocale';
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { Coins, TrendingUp, Calendar, Gift, ArrowUp, ArrowDown, Flame } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { Link } from 'react-router-dom';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

const REWARD_TYPES = [
  { type: 'daily_login', label: 'تسجيل يومي', icon: Calendar, gold: 10, description: 'سجّل دخولك يومياً واحصل على مكافأة' },
  { type: 'tasbeeh_100', label: 'تسبيح 100', icon: Gift, gold: 3, description: 'أكمل 100 تسبيحة' },
  { type: 'quran_page', label: 'صفحة قرآن', icon: Gift, gold: 5, description: 'اقرأ صفحة من القرآن' },
];

interface Transaction { type: string; amount: number; created_at: string; description?: string; }

export default function Rewards() {
  const { user, getToken } = useAuth();
  const [gold, setGold] = useState(0);
  const [totalEarned, setTotalEarned] = useState(0);
  const [streak, setStreak] = useState(0);
  const [history, setHistory] = useState<Transaction[]>([]);
  const [claiming, setClaiming] = useState('');

  const load = () => {
    if (!user) return;
    const token = getToken();
    Promise.all([
      fetch(`${BACKEND_URL}/api/rewards/balance`, { headers: { Authorization: `Bearer ${token}` } }).then(r => r.json()),
      fetch(`${BACKEND_URL}/api/rewards/history`, { headers: { Authorization: `Bearer ${token}` } }).then(r => r.json()),
    ]).then(([balance, hist]) => {
      setGold(balance.gold || 0);
      setTotalEarned(balance.total_earned || 0);
      setStreak(balance.streak || 0);
      setHistory(hist.transactions || []);
    });
  };

  useEffect(load, [user]);

  const claim = async (type: string) => {
    if (!user) { toast.error('يجب تسجيل الدخول'); return; }
    setClaiming(type);
    try {
      const res = await fetch(`${BACKEND_URL}/api/rewards/claim`, {
        method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` },
        body: JSON.stringify({ reward_type: type }),
      });
      const data = await res.json();
      if (data.earned > 0) {
        toast.success(data.message);
        setGold(data.gold);
        if (data.streak !== undefined) setStreak(data.streak);
        load();
      } else {
        toast.info(data.message);
      }
    } catch { toast.error('حدث خطأ'); }
    setClaiming('');
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center pb-24" dir="rtl" data-testid="rewards-page">
        <div className="text-center">
          <Coins className="h-12 w-12 mx-auto mb-3 text-amber-400" />
          <h2 className="text-lg font-bold text-foreground mb-2">المكافآت</h2>
          <p className="text-sm text-muted-foreground mb-4">سجّل دخولك لجمع الذهب</p>
          <Link to="/auth"><Button data-testid="rewards-login-btn">تسجيل الدخول</Button></Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="rewards-page">
      {/* Header */}
      <div className="bg-gradient-to-br from-amber-900 via-yellow-900 to-orange-900 px-5 pb-14 pt-safe-header overflow-hidden relative">
        <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 60% 30%, rgba(255,215,0,0.4), transparent 50%)' }} />
        <div className="relative pt-4 text-center">
          <Coins className="h-10 w-10 mx-auto mb-2 text-amber-300" />
          <h1 className="text-2xl font-bold text-white mb-3">المكافآت</h1>
          
          <div className="flex items-center justify-center gap-6">
            <div className="text-center">
              <span className="text-3xl font-bold text-amber-300 tabular-nums">{gold}</span>
              <p className="text-amber-300/60 text-[10px]">رصيدك</p>
            </div>
            <div className="h-8 w-px bg-white/20" />
            <div className="text-center">
              <div className="flex items-center gap-1 justify-center">
                <Flame className="h-4 w-4 text-orange-400" />
                <span className="text-xl font-bold text-orange-300 tabular-nums">{streak}</span>
              </div>
              <p className="text-orange-300/60 text-[10px]">سلسلة أيام</p>
            </div>
            <div className="h-8 w-px bg-white/20" />
            <div className="text-center">
              <span className="text-xl font-bold text-emerald-300 tabular-nums">{totalEarned}</span>
              <p className="text-emerald-300/60 text-[10px]">إجمالي</p>
            </div>
          </div>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Claim Rewards */}
      <div className="px-4 mt-2 mb-6">
        <h2 className="text-sm font-bold text-foreground mb-3">اجمع المكافآت</h2>
        <div className="space-y-3">
          {REWARD_TYPES.map(reward => (
            <motion.div key={reward.type} className="rounded-2xl border border-border/40 bg-card p-4 flex items-center gap-4"
              initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}>
              <div className="h-12 w-12 rounded-2xl bg-amber-500/10 flex items-center justify-center shrink-0">
                <reward.icon className="h-5 w-5 text-amber-500" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-bold text-foreground">{reward.label}</p>
                <p className="text-[11px] text-muted-foreground">{reward.description}</p>
              </div>
              <div className="text-center shrink-0">
                <div className="flex items-center gap-1 mb-1 justify-center">
                  <Coins className="h-3 w-3 text-amber-500" />
                  <span className="text-xs font-bold text-amber-500">+{reward.gold}</span>
                </div>
                <Button size="sm" variant="outline" className="rounded-xl h-7 text-[10px] px-3"
                  onClick={() => claim(reward.type)} disabled={claiming === reward.type}
                  data-testid={`claim-${reward.type}`}>
                  {claiming === reward.type ? '...' : 'استلم'}
                </Button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Go to Store */}
      <div className="px-4 mb-6">
        <Link to="/store" data-testid="go-to-store-link">
          <div className="rounded-2xl bg-gradient-to-l from-primary/10 to-accent/10 border border-primary/20 p-4 flex items-center gap-3 active:scale-[0.98] transition-transform">
            <div className="h-10 w-10 rounded-xl bg-primary/15 flex items-center justify-center">
              <Gift className="h-5 w-5 text-primary" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-bold text-foreground">المتجر</p>
              <p className="text-[10px] text-muted-foreground">اشترِ عناصر مميزة بالذهب</p>
            </div>
            <TrendingUp className="h-4 w-4 text-primary" />
          </div>
        </Link>
      </div>

      {/* History */}
      <div className="px-4">
        <h2 className="text-sm font-bold text-foreground mb-3">السجل</h2>
        {history.length === 0 ? (
          <p className="text-center text-muted-foreground text-sm py-8">لا توجد معاملات بعد</p>
        ) : (
          <div className="space-y-2">
            {history.map((tx, i) => (
              <div key={i} className="flex items-center gap-3 py-2.5 border-b border-border/20 last:border-0">
                <div className={cn('h-8 w-8 rounded-xl flex items-center justify-center',
                  tx.amount > 0 ? 'bg-emerald-500/10' : 'bg-red-500/10')}>
                  {tx.amount > 0 ? <ArrowUp className="h-4 w-4 text-emerald-500" /> : <ArrowDown className="h-4 w-4 text-red-500" />}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-semibold text-foreground">{tx.description || tx.type}</p>
                  <p className="text-[10px] text-muted-foreground">{new Date(tx.created_at).toLocaleDateString('ar')}</p>
                </div>
                <span className={cn('text-sm font-bold tabular-nums', tx.amount > 0 ? 'text-emerald-500' : 'text-red-500')}>
                  {tx.amount > 0 ? '+' : ''}{tx.amount}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
