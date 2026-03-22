import { useState, useEffect, useCallback } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { ArrowLeft, Coins, Star, Clock, Gift, Shield, TrendingUp, Users, BookOpen, Heart, Target, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

/* ═══ Translations ═══ */
const TX: Record<string, Record<string, string>> = {
  "baraka_market": { ar: "مركز البركة", en: "Baraka Center", de: "Baraka-Zentrum", fr: "Centre Baraka", tr: "Baraka Merkezi" },
  "reward_center": { ar: "اكسب المكافآت من خلال العبادات", en: "Earn rewards through worship", de: "Belohnungen durch Anbetung", fr: "Gagnez des récompenses par l'adoration", tr: "İbadet ile ödüller kazanın" },
  "blessing_coins": { ar: "عملات البركة", en: "Blessing Coins", de: "Segensmünzen", fr: "Pièces de bénédiction", tr: "Bereket Paraları" },
  "golden_bricks": { ar: "الطوب الذهبي", en: "Golden Bricks", de: "Goldene Steine", fr: "Briques dorées", tr: "Altın Tuğlalar" },
  "total_earned": { ar: "إجمالي المكسب", en: "Total earned", de: "Gesamt verdient", fr: "Total gagné", tr: "Toplam kazanılan" },
  "transferred": { ar: "تم التحويل", en: "Transferred", de: "Überwiesen", fr: "Transféré", tr: "Transfer edildi" },
  "daily_tasks": { ar: "المهام اليومية", en: "Daily Tasks", de: "Tägliche Aufgaben", fr: "Tâches quotidiennes", tr: "Günlük Görevler" },
  "read_quran": { ar: "اقرأ القرآن", en: "Read Quran", de: "Quran lesen", fr: "Lire le Coran", tr: "Kuran Oku" },
  "read_quran_desc": { ar: "اقرأ صفحة واحدة على الأقل", en: "Read at least one page", de: "Mindestens eine Seite lesen", fr: "Lire au moins une page", tr: "En az bir sayfa oku" },
  "do_tasbeeh": { ar: "سبّح واذكر الله", en: "Do Tasbeeh & Dhikr", de: "Tasbeeh machen", fr: "Faire le Tasbeeh", tr: "Tesbihat Yap" },
  "do_tasbeeh_desc": { ar: "أكمل ٣٣ تسبيحة", en: "Complete 33 counts", de: "33 Zählungen abschließen", fr: "Compléter 33 comptages", tr: "33 sayımı tamamla" },
  "read_hadith": { ar: "اقرأ حديثاً", en: "Read a Hadith", de: "Hadith lesen", fr: "Lire un Hadith", tr: "Hadis Oku" },
  "read_hadith_desc": { ar: "اقرأ حديث اليوم واستفد", en: "Read today's hadith and benefit", de: "Lies den heutigen Hadith", fr: "Lis le hadith du jour", tr: "Bugünün hadisini oku" },
  "make_dua": { ar: "ادعُ الله", en: "Make Dua", de: "Dua machen", fr: "Faire une Dua", tr: "Dua Yap" },
  "make_dua_desc": { ar: "اقرأ دعاء واحد على الأقل", en: "Read at least one dua", de: "Mindestens ein Dua lesen", fr: "Lire au moins un dua", tr: "En az bir dua oku" },
  "complete_lesson": { ar: "أكمل درساً", en: "Complete a lesson", de: "Lektion abschließen", fr: "Terminer une leçon", tr: "Ders tamamla" },
  "complete_lesson_desc": { ar: "أكمل درساً في أكاديمية نور", en: "Complete a Noor Academy lesson", de: "Noor Academy Lektion abschließen", fr: "Terminer une leçon Noor Academy", tr: "Noor Academy dersi tamamla" },
  "go_now": { ar: "ابدأ الآن", en: "Go Now", de: "Jetzt starten", fr: "Commencer", tr: "Şimdi Git" },
  "completed": { ar: "مكتمل ✓", en: "Completed ✓", de: "Abgeschlossen ✓", fr: "Terminé ✓", tr: "Tamamlandı ✓" },
  "coins_reward": { ar: "عملة مكافأة", en: "reward coins", de: "Belohnungsmünzen", fr: "pièces de récompense", tr: "ödül paraları" },
  "send_gold_kids": { ar: "أرسل ذهباً للأطفال", en: "Send Gold to Kids", de: "Gold an Kinder senden", fr: "Envoyer de l'or aux enfants", tr: "Çocuklara Altın Gönder" },
  "send_gold_desc": { ar: "أكمل مهامك اليومية لإرسال طوب ذهبي لطفلك", en: "Complete daily tasks to send golden bricks to your child", de: "Tägliche Aufgaben erledigen um goldene Steine zu senden", fr: "Complétez les tâches pour envoyer des briques à votre enfant", tr: "Günlük görevleri tamamlayarak çocuğunuza tuğla gönderin" },
  "send_bricks": { ar: "أرسل طوباً ذهبياً", en: "Send Golden Bricks", de: "Goldene Steine senden", fr: "Envoyer des briques", tr: "Tuğla Gönder" },
  "coppa_notice": { ar: "منطقة الأطفال خالية تماماً من الإعلانات ومحمية بمعايير COPPA", en: "Kids zone is 100% ad-free and protected by COPPA standards", de: "Kinderzone ist 100% werbefrei und COPPA-geschützt", fr: "Zone enfants 100% sans pub et protégée par COPPA", tr: "Çocuk bölgesi %100 reklamsız ve COPPA korumalı" },
  "leaderboard": { ar: "لوحة المتصدرين", en: "Leaderboard", de: "Bestenliste", fr: "Classement", tr: "Sıralama" },
  "transaction_history": { ar: "سجل المعاملات", en: "Transaction History", de: "Transaktionsverlauf", fr: "Historique", tr: "İşlem Geçmişi" },
  "tasks_completed": { ar: "مهام مكتملة اليوم", en: "Tasks completed today", de: "Heute erledigte Aufgaben", fr: "Tâches terminées aujourd'hui", tr: "Bugün tamamlanan görevler" },
};

interface DailyTask {
  id: string;
  emoji: string;
  titleKey: string;
  descKey: string;
  reward: number;
  path: string;
  color: string;
}

const DAILY_TASKS: DailyTask[] = [
  { id: 'quran', emoji: '📖', titleKey: 'read_quran', descKey: 'read_quran_desc', reward: 10, path: '/quran', color: 'emerald' },
  { id: 'tasbeeh', emoji: '📿', titleKey: 'do_tasbeeh', descKey: 'do_tasbeeh_desc', reward: 5, path: '/tasbeeh', color: 'blue' },
  { id: 'hadith', emoji: '📜', titleKey: 'read_hadith', descKey: 'read_hadith_desc', reward: 5, path: '/explore', color: 'amber' },
  { id: 'dua', emoji: '🤲', titleKey: 'make_dua', descKey: 'make_dua_desc', reward: 5, path: '/duas', color: 'purple' },
  { id: 'lesson', emoji: '🎓', titleKey: 'complete_lesson', descKey: 'complete_lesson_desc', reward: 15, path: '/kids-zone', color: 'pink' },
];

const TASK_COLORS: Record<string, string> = {
  emerald: 'from-emerald-500/15 to-teal-500/10 border-emerald-400/30',
  blue: 'from-blue-500/15 to-cyan-500/10 border-blue-400/30',
  amber: 'from-amber-500/15 to-yellow-500/10 border-amber-400/30',
  purple: 'from-violet-500/15 to-purple-500/10 border-violet-400/30',
  pink: 'from-pink-500/15 to-rose-500/10 border-pink-400/30',
};

export default function BarakaMarket() {
  const { dir, locale } = useLocale();
  const navigate = useNavigate();
  const lang = locale || 'ar';

  const t = useCallback((key: string) => TX[key]?.[lang] || TX[key]?.['en'] || key, [lang]);

  const [userId] = useState(() => localStorage.getItem('auth_user_id') || localStorage.getItem('anon_user_id') || `user_${Date.now()}`);
  const [wallet, setWallet] = useState<any>(null);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [showTx, setShowTx] = useState(false);
  const [completedTasks, setCompletedTasks] = useState<Set<string>>(() => {
    const today = new Date().toDateString();
    const saved = localStorage.getItem(`baraka_tasks_${today}`);
    return saved ? new Set(JSON.parse(saved)) : new Set();
  });

  const loadData = useCallback(async () => {
    try {
      const [w, l, tx] = await Promise.all([
        fetch(`${BACKEND_URL}/api/baraka/wallet?user_id=${userId}`).then(r => r.json()),
        fetch(`${BACKEND_URL}/api/baraka/leaderboard`).then(r => r.json()),
        fetch(`${BACKEND_URL}/api/baraka/transactions?user_id=${userId}`).then(r => r.json()),
      ]);
      if (w.success) setWallet(w.wallet);
      if (l.success) setLeaderboard(l.leaderboard || []);
      if (tx.success) setTransactions(tx.transactions || []);
    } catch {}
  }, [userId]);

  useEffect(() => { loadData(); }, [loadData]);

  const markTaskDone = (taskId: string, reward: number) => {
    const newCompleted = new Set(completedTasks);
    newCompleted.add(taskId);
    setCompletedTasks(newCompleted);
    const today = new Date().toDateString();
    localStorage.setItem(`baraka_tasks_${today}`, JSON.stringify([...newCompleted]));

    // Award coins via backend
    fetch(`${BACKEND_URL}/api/baraka/earn?user_id=${userId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ad_type: 'task_reward', placement: taskId, coins: reward }),
    }).then(() => loadData()).catch(() => {});
  };

  const handleTaskClick = (task: DailyTask) => {
    if (completedTasks.has(task.id)) return;
    // Navigate to the feature page, mark as started
    navigate(task.path);
  };

  const transferToKids = async () => {
    if (completedTasks.size < 3) return; // Need at least 3 tasks done
    try {
      const res = await fetch(`${BACKEND_URL}/api/baraka/transfer?user_id=${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kid_id: `kid_${userId}`, amount: 20 }),
      }).then(r => r.json());
      if (res.success) {
        if (navigator.vibrate) navigator.vibrate([40, 20, 60]);
        loadData();
      }
    } catch {}
  };

  return (
    <div dir={dir} className="min-h-screen bg-background text-foreground pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-background/90 backdrop-blur-xl border-b border-border/30 px-4 py-3">
        <div className="flex items-center gap-3 max-w-2xl mx-auto">
          <button onClick={() => navigate(-1)} className="p-2 rounded-xl hover:bg-muted/50 transition-colors">
            <ArrowLeft className="h-5 w-5"/>
          </button>
          <div className="flex-1">
            <h1 className="text-lg font-bold">{t('baraka_market')} ☪️</h1>
            <p className="text-xs text-muted-foreground">{t('reward_center')}</p>
          </div>
          <button onClick={() => setShowTx(!showTx)} className="p-2 rounded-xl hover:bg-muted/50 transition-colors">
            <Clock className="h-5 w-5 text-muted-foreground"/>
          </button>
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-4 pt-4 space-y-5">

        {/* Wallet Cards */}
        <div className="grid grid-cols-2 gap-3">
          <div className="p-4 rounded-2xl bg-gradient-to-br from-amber-500/15 to-yellow-500/10 border border-amber-400/30">
            <div className="flex items-center gap-2 mb-2">
              <Coins className="h-5 w-5 text-amber-500 dark:text-amber-400"/>
              <span className="text-xs font-bold text-amber-700 dark:text-amber-300">{t('blessing_coins')}</span>
            </div>
            <p className="text-3xl font-black text-amber-600 dark:text-amber-300">{wallet?.blessing_coins || 0}</p>
            <p className="text-xs text-foreground/60 mt-1">{t('total_earned')}: {wallet?.total_earned_coins || 0}</p>
          </div>
          <div className="p-4 rounded-2xl bg-gradient-to-br from-orange-500/15 to-red-500/10 border border-orange-400/30">
            <div className="flex items-center gap-2 mb-2">
              <Star className="h-5 w-5 text-orange-500 dark:text-orange-400"/>
              <span className="text-xs font-bold text-orange-700 dark:text-orange-300">{t('golden_bricks')}</span>
            </div>
            <p className="text-3xl font-black text-orange-600 dark:text-orange-300">{wallet?.golden_bricks || 0}</p>
            <p className="text-xs text-foreground/60 mt-1">{t('transferred')}: {wallet?.total_transferred_bricks || 0}</p>
          </div>
        </div>

        {/* Tasks Progress */}
        <div className="flex items-center justify-between px-4 py-3 rounded-xl bg-primary/10 border border-primary/20">
          <div className="flex items-center gap-2">
            <Target className="h-4 w-4 text-primary"/>
            <span className="text-sm font-medium">{t('tasks_completed')}</span>
          </div>
          <span className="text-lg font-bold text-primary">{completedTasks.size}/{DAILY_TASKS.length}</span>
        </div>

        {/* Daily Tasks — REAL activities, not fake ads */}
        <div>
          <h2 className="text-base font-bold mb-3 flex items-center gap-2">
            <CheckCircle className="h-5 w-5 text-primary"/>
            {t('daily_tasks')}
          </h2>
          <div className="space-y-3">
            {DAILY_TASKS.map((task) => {
              const done = completedTasks.has(task.id);
              return (
                <div key={task.id} className={cn(
                  "p-4 rounded-2xl bg-gradient-to-br border relative overflow-hidden transition-all",
                  TASK_COLORS[task.color],
                  done && "opacity-70"
                )}>
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-card/50 flex items-center justify-center shrink-0">
                      <span className="text-2xl">{task.emoji}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-sm text-foreground">{t(task.titleKey)}</h3>
                      <p className="text-xs text-muted-foreground mt-0.5">{t(task.descKey)}</p>
                      <p className="text-xs font-bold text-primary mt-1">+{task.reward} {t('coins_reward')}</p>
                    </div>
                    {done ? (
                      <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-3 py-1.5 rounded-lg whitespace-nowrap">
                        {t('completed')}
                      </span>
                    ) : (
                      <button
                        onClick={() => handleTaskClick(task)}
                        className="text-xs font-bold text-white bg-primary px-3 py-1.5 rounded-lg hover:opacity-90 transition-all whitespace-nowrap"
                      >
                        {t('go_now')} →
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Send Gold to Kids — requires completing tasks */}
        <div className="p-5 rounded-2xl bg-gradient-to-br from-violet-500/15 via-purple-500/10 to-pink-500/10 border border-violet-400/30">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 rounded-xl bg-violet-500/20 flex items-center justify-center">
              <span className="text-2xl">👨‍👧‍👦</span>
            </div>
            <div className="flex-1">
              <h3 className="font-bold text-sm text-foreground">{t('send_gold_kids')}</h3>
              <p className="text-xs text-muted-foreground mt-0.5">{t('send_gold_desc')}</p>
            </div>
          </div>
          <button
            onClick={transferToKids}
            disabled={completedTasks.size < 3}
            className={cn(
              "w-full py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all",
              completedTasks.size >= 3
                ? "bg-gradient-to-r from-violet-600 to-purple-600 text-white hover:from-violet-500 hover:to-purple-500 shadow-lg"
                : "bg-muted/30 text-muted-foreground cursor-not-allowed"
            )}
          >
            <Gift className="h-4 w-4"/> {t('send_bricks')} ({completedTasks.size}/3 {t('daily_tasks')})
          </button>
        </div>

        {/* COPPA Notice */}
        <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-blue-500/10 border border-blue-400/20">
          <Shield className="h-5 w-5 text-blue-500 dark:text-blue-400 shrink-0"/>
          <p className="text-sm text-blue-700 dark:text-blue-300">{t('coppa_notice')} 🛡️</p>
        </div>

        {/* Leaderboard */}
        {leaderboard.length > 0 && (
          <div className="p-4 rounded-2xl bg-card/50 border border-border/30">
            <div className="flex items-center gap-2 mb-3">
              <TrendingUp className="h-5 w-5 text-amber-500 dark:text-amber-400"/>
              <h3 className="font-bold">{t('leaderboard')}</h3>
            </div>
            <div className="space-y-2">
              {leaderboard.map((entry: any, i: number) => (
                <div key={i} className="flex items-center gap-3 px-3 py-2 rounded-xl bg-muted/20">
                  <span className={cn("w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold",
                    i === 0 ? "bg-amber-500/20 text-amber-600 dark:text-amber-300" : i === 1 ? "bg-gray-400/20 text-gray-600 dark:text-gray-300" : i === 2 ? "bg-orange-500/20 text-orange-600 dark:text-orange-300" : "bg-muted/30 text-foreground/60")}>
                    {i + 1}
                  </span>
                  <span className="flex-1 text-sm font-medium truncate">{entry.user_id}</span>
                  <span className="text-sm font-bold text-amber-600 dark:text-amber-300">{entry.total_earned_coins} 🪙</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Transaction History */}
        {showTx && transactions.length > 0 && (
          <div className="p-4 rounded-2xl bg-card/50 border border-border/30">
            <h3 className="font-bold mb-3 flex items-center gap-2">
              <Clock className="h-4 w-4"/> {t('transaction_history')}
            </h3>
            <div className="space-y-2">
              {transactions.map((tx: any, i: number) => (
                <div key={i} className="flex items-center justify-between px-3 py-2 rounded-lg bg-muted/15">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{tx.type === 'earn' ? '🪙' : tx.type === 'transfer_out' ? '🧱' : '📥'}</span>
                    <div>
                      <p className="text-sm font-medium capitalize">{tx.type.replace('_', ' ')}</p>
                      <p className="text-xs text-foreground/60">{new Date(tx.created_at).toLocaleDateString()}</p>
                    </div>
                  </div>
                  <span className={cn("text-sm font-bold", tx.type === 'earn' || tx.type === 'transfer_in' ? "text-emerald-600 dark:text-emerald-400" : "text-amber-600 dark:text-amber-300")}>
                    +{tx.amount}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
