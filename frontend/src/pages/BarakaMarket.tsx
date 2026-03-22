import React, { useState, useEffect, useCallback } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { useAuth } from '@/hooks/useAuth';
import { ArrowLeft, Play, Gift, Users, Shield, TrendingUp, Clock, Star, Coins, Zap, ChevronRight, Settings } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { cn } from '@/lib/utils';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

// ═══ 10-Language Translations ═══
const BARAKA_TRANSLATIONS: Record<string, Record<string, string>> = {
  "baraka_market": { ar: "سوق البركة", en: "Baraka Market", de: "Baraka-Markt", "de-AT": "Baraka-Markt", fr: "Marché Baraka", tr: "Bereket Pazarı", ru: "Рынок Барака", sv: "Baraka-marknaden", nl: "Baraka Markt", el: "Αγορά Μπαράκα" },
  "reward_center": { ar: "مركز المكافآت", en: "Reward Center", de: "Belohnungszentrum", "de-AT": "Belohnungszentrum", fr: "Centre de récompenses", tr: "Ödül Merkezi", ru: "Центр наград", sv: "Belöningscenter", nl: "Beloningscentrum", el: "Κέντρο ανταμοιβών" },
  "blessing_coins": { ar: "عملات البركة", en: "Blessing Coins", de: "Segens-Münzen", "de-AT": "Segens-Münzen", fr: "Pièces de bénédiction", tr: "Bereket Paraları", ru: "Монеты благословения", sv: "Välsignelsemynt", nl: "Zegeningsmunten", el: "Νομίσματα ευλογίας" },
  "golden_bricks": { ar: "الطوب الذهبي", en: "Golden Bricks", de: "Goldene Steine", "de-AT": "Goldene Steine", fr: "Briques dorées", tr: "Altın Tuğlalar", ru: "Золотые кирпичи", sv: "Guldstenar", nl: "Gouden stenen", el: "Χρυσά τούβλα" },
  "watch_video_earn": { ar: "شاهد فيديو واكسب عملات", en: "Watch Video & Earn Coins", de: "Video ansehen & Münzen verdienen", "de-AT": "Video ansehen & Münzen verdienen", fr: "Regarder une vidéo et gagner des pièces", tr: "Video izle & Para kazan", ru: "Смотри видео и зарабатывай", sv: "Se video & tjäna mynt", nl: "Bekijk video & verdien munten", el: "Δες βίντεο & κέρδισε νομίσματα" },
  "watch_short_video": { ar: "شاهد فيديو قصير واحصل على", en: "Watch a short video to get", de: "Sehen Sie ein kurzes Video und erhalten Sie", "de-AT": "Sehen Sie ein kurzes Video und erhalten Sie", fr: "Regardez une courte vidéo pour obtenir", tr: "Kısa bir video izleyerek kazan", ru: "Посмотрите короткое видео и получите", sv: "Se en kort video och få", nl: "Bekijk een korte video en ontvang", el: "Δες ένα σύντομο βίντεο και πάρε" },
  "send_gold_kids": { ar: "أرسل ذهباً للأطفال", en: "Send Gold to Kids", de: "Gold an Kinder senden", "de-AT": "Gold an Kinder senden", fr: "Envoyer de l'or aux enfants", tr: "Çocuklara Altın Gönder", ru: "Отправить золото детям", sv: "Skicka guld till barnen", nl: "Stuur goud naar kinderen", el: "Στείλε χρυσό στα παιδιά" },
  "watch_ad_transfer": { ar: "شاهد إعلاناً وأرسل طوباً ذهبياً لطفلك", en: "Watch an ad & send golden bricks to your child", de: "Sehen Sie eine Anzeige und senden Sie goldene Steine an Ihr Kind", "de-AT": "Sehen Sie eine Anzeige und senden Sie goldene Steine an Ihr Kind", fr: "Regardez une pub et envoyez des briques à votre enfant", tr: "Reklam izle ve çocuğuna altın tuğla gönder", ru: "Посмотри рекламу и отправь золотые кирпичи ребёнку", sv: "Se en annons och skicka guldstenar till ditt barn", nl: "Bekijk een advertentie en stuur gouden stenen naar je kind", el: "Δες μια διαφήμιση και στείλε χρυσά τούβλα στο παιδί σου" },
  "daily_rewards": { ar: "المكافآت اليومية", en: "Daily Rewards", de: "Tägliche Belohnungen", "de-AT": "Tägliche Belohnungen", fr: "Récompenses quotidiennes", tr: "Günlük Ödüller", ru: "Ежедневные награды", sv: "Dagliga belöningar", nl: "Dagelijkse beloningen", el: "Ημερήσιες ανταμοιβές" },
  "ads_remaining": { ar: "المكافآت المتبقية اليوم", en: "Rewards remaining today", de: "Verbleibende Belohnungen heute", "de-AT": "Verbleibende Belohnungen heute", fr: "Récompenses restantes aujourd'hui", tr: "Bugün kalan ödüller", ru: "Осталось наград сегодня", sv: "Belöningar kvar idag", nl: "Resterende beloningen vandaag", el: "Εναπομένουσες ανταμοιβές σήμερα" },
  "watch_now": { ar: "شاهد الآن", en: "Watch Now", de: "Jetzt ansehen", "de-AT": "Jetzt ansehen", fr: "Regarder maintenant", tr: "Şimdi İzle", ru: "Смотреть сейчас", sv: "Se nu", nl: "Nu bekijken", el: "Δες τώρα" },
  "earned": { ar: "مكتسب", en: "Earned", de: "Verdient", "de-AT": "Verdient", fr: "Gagné", tr: "Kazanılan", ru: "Заработано", sv: "Tjänat", nl: "Verdiend", el: "Κερδισμένα" },
  "transferred": { ar: "محوّل", en: "Transferred", de: "Übertragen", "de-AT": "Übertragen", fr: "Transféré", tr: "Aktarılan", ru: "Переведено", sv: "Överfört", nl: "Overgedragen", el: "Μεταφέρθηκαν" },
  "transaction_history": { ar: "سجل المعاملات", en: "Transaction History", de: "Transaktionsverlauf", "de-AT": "Transaktionsverlauf", fr: "Historique des transactions", tr: "İşlem Geçmişi", ru: "История транзакций", sv: "Transaktionshistorik", nl: "Transactiegeschiedenis", el: "Ιστορικό συναλλαγών" },
  "coppa_notice": { ar: "منطقة الأطفال خالية تماماً من الإعلانات", en: "Kids Zone is 100% ad-free", de: "Kinderzone ist 100% werbefrei", "de-AT": "Kinderzone ist 100% werbefrei", fr: "La zone enfants est 100% sans pub", tr: "Çocuk Bölgesi %100 reklamsız", ru: "Детская зона на 100% без рекламы", sv: "Barnzonen är 100% reklamfri", nl: "Kinderzone is 100% advertentievrij", el: "Η παιδική ζώνη είναι 100% χωρίς διαφημίσεις" },
  "ad_simulation": { ar: "جاري تحميل المحتوى", en: "Loading content", de: "Inhalt wird geladen", "de-AT": "Inhalt wird geladen", fr: "Chargement du contenu", tr: "İçerik yükleniyor", ru: "Загрузка контента", sv: "Laddar innehåll", nl: "Inhoud laden", el: "Φόρτωση περιεχομένου" },
  "watching_ad": { ar: "جاري تحميل المكافأة...", en: "Loading reward...", de: "Belohnung wird geladen...", "de-AT": "Belohnung wird geladen...", fr: "Chargement de la récompense...", tr: "Ödül yükleniyor...", ru: "Загрузка награды...", sv: "Laddar belöning...", nl: "Beloning laden...", el: "Φόρτωση ανταμοιβής..." },
  "reward_claimed": { ar: "تم الحصول على المكافأة!", en: "Reward claimed!", de: "Belohnung erhalten!", "de-AT": "Belohnung erhalten!", fr: "Récompense obtenue!", tr: "Ödül alındı!", ru: "Награда получена!", sv: "Belöning mottagen!", nl: "Beloning ontvangen!", el: "Ανταμοιβή παραλήφθηκε!" },
  "leaderboard": { ar: "لوحة المتصدرين", en: "Leaderboard", de: "Bestenliste", "de-AT": "Bestenliste", fr: "Classement", tr: "Liderlik Tablosu", ru: "Таблица лидеров", sv: "Topplista", nl: "Ranglijst", el: "Πίνακας κατάταξης" },
  "total_earned": { ar: "إجمالي المكتسبات", en: "Total Earned", de: "Insgesamt verdient", "de-AT": "Insgesamt verdient", fr: "Total gagné", tr: "Toplam Kazanılan", ru: "Всего заработано", sv: "Totalt tjänat", nl: "Totaal verdiend", el: "Σύνολο κερδισμένων" },
};

export default function BarakaMarket() {
  const { locale, dir } = useLocale();
  const { user } = useAuth();
  const navigate = useNavigate();
  const lang = locale || 'ar';

  const t = useCallback((key: string) => {
    return BARAKA_TRANSLATIONS[key]?.[lang] || BARAKA_TRANSLATIONS[key]?.['en'] || key;
  }, [lang]);

  const [wallet, setWallet] = useState<any>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [adConfig, setAdConfig] = useState<any>(null);
  const [showAd, setShowAd] = useState(false);
  const [adType, setAdType] = useState<'earn' | 'transfer'>('earn');
  const [adProgress, setAdProgress] = useState(0);
  const [showSuccess, setShowSuccess] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [showTx, setShowTx] = useState(false);

  const userId = user?.id || 'guest';

  const loadData = useCallback(async () => {
    try {
      const [w, tx, lb, cfg] = await Promise.all([
        fetch(`${BACKEND_URL}/api/baraka/wallet/${userId}`).then(r => r.json()),
        fetch(`${BACKEND_URL}/api/baraka/transactions/${userId}?limit=10`).then(r => r.json()),
        fetch(`${BACKEND_URL}/api/baraka/leaderboard`).then(r => r.json()),
        fetch(`${BACKEND_URL}/api/admin/ads_config`).then(r => r.json()),
      ]);
      if (w.success) setWallet(w.wallet);
      if (tx.success) setTransactions(tx.transactions);
      if (lb.success) setLeaderboard(lb.leaderboard);
      if (cfg.success) setAdConfig(cfg.config);
    } catch (e) { console.error(e); }
  }, [userId]);

  useEffect(() => { loadData(); }, [loadData]);

  // Auto-sync wallet when app becomes visible (tab switch, phone unlock)
  useEffect(() => {
    const handleVisibility = () => {
      if (document.visibilityState === 'visible') {
        loadData();
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);
    // Also try Capacitor App plugin for native resume
    let appListener: any = null;
    (async () => {
      try {
        const { App } = await import('@capacitor/app');
        appListener = await App.addListener('appStateChange', (state: { isActive: boolean }) => {
          if (state.isActive) loadData();
        });
      } catch {
        // Not in native context — that's fine
      }
    })();
    return () => {
      document.removeEventListener('visibilitychange', handleVisibility);
      if (appListener) appListener.remove();
    };
  }, [loadData]);

  // Simulated ad watching (since this is a web app, not native)
  const watchAd = (type: 'earn' | 'transfer') => {
    setAdType(type);
    setShowAd(true);
    setAdProgress(0);
    const interval = setInterval(() => {
      setAdProgress(p => {
        if (p >= 100) {
          clearInterval(interval);
          completeAd(type);
          return 100;
        }
        return p + 4;
      });
    }, 120); // 3 seconds total
  };

  const completeAd = async (type: 'earn' | 'transfer') => {
    setShowAd(false);
    try {
      if (type === 'earn') {
        const res = await fetch(`${BACKEND_URL}/api/baraka/earn?user_id=${userId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ad_type: 'rewarded_video', placement: 'baraka_market' }),
        }).then(r => r.json());
        if (res.success) {
          // Haptic feedback — makes the reward feel "real"
          if (navigator.vibrate) navigator.vibrate([50, 30, 80]);
          setSuccessMsg(`+${res.earned} ${t('blessing_coins')} 🎉`);
          setShowSuccess(true);
          setTimeout(() => setShowSuccess(false), 3000);
        }
      } else {
        const res = await fetch(`${BACKEND_URL}/api/baraka/transfer?user_id=${userId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ kid_id: `kid_${userId}`, amount: 50 }),
        }).then(r => r.json());
        if (res.success) {
          // Haptic feedback — makes the reward feel "real"
          if (navigator.vibrate) navigator.vibrate([40, 20, 60, 20, 40]);
          setSuccessMsg(`+${res.transferred} ${t('golden_bricks')} 🧱`);
          setShowSuccess(true);
          setTimeout(() => setShowSuccess(false), 3000);
        }
      }
      loadData();
    } catch (e) { console.error(e); }
  };

  const adsRemaining = adConfig ? adConfig.daily_reward_limit - (wallet?.ads_watched_today || 0) : 10;

  return (
    <div dir={dir} className="min-h-screen bg-background text-foreground pb-20">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-background/90 backdrop-blur-xl border-b border-border/30 px-4 py-3">
        <div className="flex items-center gap-3 max-w-2xl mx-auto">
          <button onClick={() => navigate(-1)} className="p-2 rounded-xl hover:bg-muted/50 transition-colors">
            <ArrowLeft className="h-5 w-5"/>
          </button>
          <div className="flex-1">
            <h1 className="text-lg font-bold">{t('baraka_market')} ☪️</h1>
            <p className="text-xs text-foreground/60">{t('reward_center')}</p>
          </div>
          <button onClick={() => setShowTx(!showTx)} className="p-2 rounded-xl hover:bg-muted/50 transition-colors">
            <Clock className="h-5 w-5 text-foreground/60"/>
          </button>
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-4 pt-4 space-y-5">

        {/* Wallet Cards */}
        <div className="grid grid-cols-2 gap-3">
          <div className="p-4 rounded-2xl bg-gradient-to-br from-amber-500/15 to-yellow-500/10 border border-amber-400/30">
            <div className="flex items-center gap-2 mb-2">
              <Coins className="h-5 w-5 text-amber-400"/>
              <span className="text-xs font-bold text-amber-300/80">{t('blessing_coins')}</span>
            </div>
            <p className="text-3xl font-black text-amber-300">{wallet?.blessing_coins || 0}</p>
            <p className="text-xs text-foreground/50 mt-1">{t('total_earned')}: {wallet?.total_earned_coins || 0}</p>
          </div>
          <div className="p-4 rounded-2xl bg-gradient-to-br from-orange-500/15 to-red-500/10 border border-orange-400/30">
            <div className="flex items-center gap-2 mb-2">
              <Star className="h-5 w-5 text-orange-400"/>
              <span className="text-xs font-bold text-orange-300/80">{t('golden_bricks')}</span>
            </div>
            <p className="text-3xl font-black text-orange-300">{wallet?.golden_bricks || 0}</p>
            <p className="text-xs text-foreground/50 mt-1">{t('transferred')}: {wallet?.total_transferred_bricks || 0}</p>
          </div>
        </div>

        {/* Daily Rewards Remaining */}
        <div className="flex items-center justify-between px-4 py-3 rounded-xl bg-muted/20 border border-border/20">
          <div className="flex items-center gap-2">
            <Zap className="h-4 w-4 text-violet-400"/>
            <span className="text-sm font-medium">{t('ads_remaining')}</span>
          </div>
          <span className="text-lg font-bold text-violet-300">{Math.max(0, adsRemaining)}/{adConfig?.daily_reward_limit || 10}</span>
        </div>

        {/* Reward Cards */}
        <div className="space-y-3">
          {/* Card 1: Watch Video Earn Coins */}
          <div className="p-5 rounded-2xl bg-gradient-to-br from-emerald-600/15 via-green-500/10 to-teal-500/10 border border-emerald-400/30 relative overflow-hidden">
            <div className="absolute top-0 end-0 w-32 h-32 bg-emerald-500/5 rounded-full -translate-y-1/2 translate-x-1/2"/>
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500/30 to-green-500/20 flex items-center justify-center">
                  <span className="text-3xl">🌙</span>
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-base">{t('watch_video_earn')}</h3>
                  <p className="text-sm text-foreground/60 mt-0.5">{t('watch_short_video')} <span className="font-bold text-emerald-300">+{adConfig?.rewarded_video_coins || 20}</span> {t('blessing_coins')}</p>
                </div>
              </div>
              <button onClick={() => watchAd('earn')} disabled={adsRemaining <= 0}
                className={cn("w-full py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all",
                  adsRemaining > 0 ? "bg-gradient-to-r from-emerald-600 to-green-600 text-white hover:from-emerald-500 hover:to-green-500 shadow-lg shadow-emerald-500/20" : "bg-muted/30 text-foreground/40 cursor-not-allowed")}>
                <Play className="h-4 w-4"/> {t('watch_now')}
              </button>
            </div>
          </div>

          {/* Card 2: Parent-Kid Transfer */}
          <div className="p-5 rounded-2xl bg-gradient-to-br from-violet-600/15 via-purple-500/10 to-pink-500/10 border border-violet-400/30 relative overflow-hidden">
            <div className="absolute top-0 end-0 w-32 h-32 bg-violet-500/5 rounded-full -translate-y-1/2 translate-x-1/2"/>
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-violet-500/30 to-purple-500/20 flex items-center justify-center">
                  <span className="text-3xl">👨‍👧‍👦</span>
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-base">{t('send_gold_kids')}</h3>
                  <p className="text-sm text-foreground/60 mt-0.5">{t('watch_ad_transfer')}</p>
                </div>
              </div>
              <div className="flex items-center gap-2 mb-3 px-3 py-2 rounded-lg bg-violet-500/10">
                <Gift className="h-4 w-4 text-violet-400"/>
                <span className="text-sm font-bold text-violet-300">+{adConfig?.transfer_bricks_amount || 50} {t('golden_bricks')} 🧱</span>
              </div>
              <button onClick={() => watchAd('transfer')}
                className="w-full py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-violet-600 to-purple-600 text-white hover:from-violet-500 hover:to-purple-500 shadow-lg shadow-violet-500/20 flex items-center justify-center gap-2 transition-all">
                <Users className="h-4 w-4"/> {t('watch_now')}
              </button>
            </div>
          </div>
        </div>

        {/* COPPA Notice */}
        <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-blue-500/10 border border-blue-400/20">
          <Shield className="h-5 w-5 text-blue-400 shrink-0"/>
          <p className="text-sm text-blue-300/80">{t('coppa_notice')} 🛡️</p>
        </div>

        {/* Leaderboard */}
        {leaderboard.length > 0 && (
          <div className="p-4 rounded-2xl bg-card/50 border border-border/30">
            <div className="flex items-center gap-2 mb-3">
              <TrendingUp className="h-5 w-5 text-amber-400"/>
              <h3 className="font-bold">{t('leaderboard')}</h3>
            </div>
            <div className="space-y-2">
              {leaderboard.map((entry: any, i: number) => (
                <div key={i} className="flex items-center gap-3 px-3 py-2 rounded-xl bg-muted/20">
                  <span className={cn("w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold",
                    i === 0 ? "bg-amber-500/20 text-amber-300" : i === 1 ? "bg-gray-400/20 text-gray-300" : i === 2 ? "bg-orange-500/20 text-orange-300" : "bg-muted/30 text-foreground/50")}>
                    {i + 1}
                  </span>
                  <span className="flex-1 text-sm font-medium truncate">{entry.user_id}</span>
                  <span className="text-sm font-bold text-amber-300">{entry.total_earned_coins} 🪙</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Transaction History (toggle) */}
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
                      <p className="text-xs text-foreground/50">{new Date(tx.created_at).toLocaleDateString()}</p>
                    </div>
                  </div>
                  <span className={cn("text-sm font-bold", tx.type === 'earn' || tx.type === 'transfer_in' ? "text-green-400" : "text-amber-300")}>
                    +{tx.amount}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Ad Overlay (Simulated Rewarded Video) */}
      {showAd && (
        <div className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-8">
          <div className="w-full max-w-sm text-center space-y-6">
            <div className="text-6xl animate-pulse">{adType === 'earn' ? '🌙' : '👨‍👧‍👦'}</div>
            <h2 className="text-xl font-bold text-white">{t('watching_ad')}</h2>
            {/* Progress bar */}
            <div className="w-full h-3 bg-white/10 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-emerald-500 to-green-400 rounded-full transition-all duration-100" style={{width: `${adProgress}%`}}/>
            </div>
            <p className="text-4xl font-black text-white">{Math.round(adProgress)}%</p>
          </div>
        </div>
      )}

      {/* Success Toast */}
      {showSuccess && (
        <div className="fixed top-20 inset-x-0 z-50 flex justify-center px-4 animate-in slide-in-from-top">
          <div className="px-6 py-3 rounded-2xl bg-emerald-500/90 backdrop-blur-xl text-white font-bold shadow-2xl shadow-emerald-500/30 flex items-center gap-2">
            <span className="text-2xl">🎉</span>
            <span>{t('reward_claimed')} {successMsg}</span>
          </div>
        </div>
      )}
    </div>
  );
}
