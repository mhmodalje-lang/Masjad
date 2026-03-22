import { useState, useEffect, useCallback } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { ArrowLeft, Coins, Star, Clock, Gift, Shield, TrendingUp, Users, BookOpen, Heart, Target, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

/* ═══ Translations ═══ */
const TX: Record<string, Record<string, string>> = {
  "baraka_market": { ar: "مركز البركة", en: "Baraka Center", de: "Baraka-Zentrum", fr: "Centre Baraka", tr: "Baraka Merkezi", ru: "Центр Барака", sv: "Baraka-center", nl: "Baraka-centrum", el: "Κέντρο Μπαράκα", ru: "Центр Барака", sv: "Baraka-center", nl: "Baraka-centrum", el: "Κέντρο Μπαράκα" },
  "reward_center": { ar: "اكسب المكافآت من خلال العبادات", en: "Earn rewards through worship", de: "Belohnungen durch Anbetung", fr: "Gagnez des récompenses par l'adoration", tr: "İbadet ile ödüller kazanın", ru: "Получайте награды через поклонение", sv: "Tjäna belöningar genom dyrkan", nl: "Verdien beloningen door aanbidding", el: "Κερδίστε ανταμοιβές μέσω λατρείας", ru: "Получайте награды через поклонение", sv: "Tjäna belöningar genom dyrkan", nl: "Verdien beloningen door aanbidding", el: "Κερδίστε ανταμοιβές μέσω λατρείας" },
  "blessing_coins": { ar: "عملات البركة", en: "Blessing Coins", de: "Segensmünzen", fr: "Pièces de bénédiction", tr: "Bereket Paraları", ru: "Монеты благословения", sv: "Välsignelsemynt", nl: "Zegeningsmunten", el: "Νομίσματα ευλογίας", ru: "Монеты благословения", sv: "Välsignelsemynt", nl: "Zegeningsmunten", el: "Νομίσματα ευλογίας" },
  "golden_bricks": { ar: "الطوب الذهبي", en: "Golden Bricks", de: "Goldene Steine", fr: "Briques dorées", tr: "Altın Tuğlalar", ru: "Золотые кирпичи", sv: "Gyllene tegelstenar", nl: "Gouden stenen", el: "Χρυσά τούβλα", ru: "Золотые кирпичи", sv: "Gyllene tegelstenar", nl: "Gouden stenen", el: "Χρυσά τούβλα" },
  "total_earned": { ar: "إجمالي المكسب", en: "Total earned", de: "Gesamt verdient", fr: "Total gagné", tr: "Toplam kazanılan", ru: "Всего заработано", sv: "Totalt intjänat", nl: "Totaal verdiend", el: "Σύνολο", ru: "Всего заработано", sv: "Totalt intjänat", nl: "Totaal verdiend", el: "Σύνολο" },
  "transferred": { ar: "تم التحويل", en: "Transferred", de: "Überwiesen", fr: "Transféré", tr: "Transfer edildi", ru: "Переведено", sv: "Överfört", nl: "Overgemaakt", el: "Μεταφέρθηκε", ru: "Переведено", sv: "Överfört", nl: "Overgemaakt", el: "Μεταφέρθηκε" },
  "daily_tasks": { ar: "المهام اليومية", en: "Daily Tasks", de: "Tägliche Aufgaben", fr: "Tâches quotidiennes", tr: "Günlük Görevler", ru: "Ежедневные задания", sv: "Dagliga uppgifter", nl: "Dagelijkse taken", el: "Καθημερινές εργασίες", ru: "Ежедневные задания", sv: "Dagliga uppgifter", nl: "Dagelijkse taken", el: "Καθημερινές εργασίες" },
  "read_quran": { ar: "اقرأ القرآن", en: "Read Quran", de: "Quran lesen", fr: "Lire le Coran", tr: "Kuran Oku", ru: "Читать Коран", sv: "Läs Koranen", nl: "Lees de Koran", el: "Διάβασε Κοράνι", ru: "Читать Коран", sv: "Läs Koranen", nl: "Lees de Koran", el: "Διάβασε Κοράνι" },
  "read_quran_desc": { ar: "اقرأ صفحة واحدة على الأقل", en: "Read at least one page", de: "Mindestens eine Seite lesen", fr: "Lire au moins une page", tr: "En az bir sayfa oku", ru: "Прочитайте хотя бы одну страницу", sv: "Läs minst en sida", nl: "Lees minstens één pagina", el: "Διάβασε τουλάχιστον μία σελίδα", ru: "Прочитайте хотя бы одну страницу", sv: "Läs minst en sida", nl: "Lees minstens één pagina", el: "Διάβασε τουλάχιστον μία σελίδα" },
  "do_tasbeeh": { ar: "سبّح واذكر الله", en: "Do Tasbeeh & Dhikr", de: "Tasbeeh machen", fr: "Faire le Tasbeeh", tr: "Tesbihat Yap", ru: "Тасбих и зикр", sv: "Gör Tasbeeh", nl: "Doe Tasbeeh", el: "Κάνε Τασμπίχ", ru: "Тасбих и зикр", sv: "Gör Tasbeeh", nl: "Doe Tasbeeh", el: "Κάνε Τασμπίχ" },
  "do_tasbeeh_desc": { ar: "أكمل ٣٣ تسبيحة", en: "Complete 33 counts", de: "33 Zählungen abschließen", fr: "Compléter 33 comptages", tr: "33 sayımı tamamla", ru: "Завершите 33 подсчёта", sv: "Slutför 33 räkningar", nl: "Voltooi 33 tellingen", el: "Ολοκλήρωσε 33 μετρήσεις", ru: "Завершите 33 подсчёта", sv: "Slutför 33 räkningar", nl: "Voltooi 33 tellingen", el: "Ολοκλήρωσε 33 μετρήσεις" },
  "read_hadith": { ar: "اقرأ حديثاً", en: "Read a Hadith", de: "Hadith lesen", fr: "Lire un Hadith", tr: "Hadis Oku", ru: "Прочитать хадис", sv: "Läs en hadith", nl: "Lees een hadith", el: "Διάβασε χαντίθ", ru: "Прочитать хадис", sv: "Läs en hadith", nl: "Lees een hadith", el: "Διάβασε χαντίθ" },
  "read_hadith_desc": { ar: "اقرأ حديث اليوم واستفد", en: "Read today's hadith and benefit", de: "Lies den heutigen Hadith", fr: "Lis le hadith du jour", tr: "Bugünün hadisini oku", ru: "Прочитайте сегодняшний хадис", sv: "Läs dagens hadith", nl: "Lees de hadith van vandaag", el: "Διάβασε το χαντίθ της ημέρας", ru: "Прочитайте сегодняшний хадис", sv: "Läs dagens hadith", nl: "Lees de hadith van vandaag", el: "Διάβασε το χαντίθ της ημέρας" },
  "make_dua": { ar: "ادعُ الله", en: "Make Dua", de: "Dua machen", fr: "Faire une Dua", tr: "Dua Yap", ru: "Сделать дуа", sv: "Gör Dua", nl: "Maak een Dua", el: "Κάνε Ντουά", ru: "Сделать дуа", sv: "Gör Dua", nl: "Maak een Dua", el: "Κάνε Ντουά" },
  "make_dua_desc": { ar: "اقرأ دعاء واحد على الأقل", en: "Read at least one dua", de: "Mindestens ein Dua lesen", fr: "Lire au moins un dua", tr: "En az bir dua oku", ru: "Прочитайте хотя бы одну дуа", sv: "Läs minst en dua", nl: "Lees minstens één dua", el: "Διάβασε τουλάχιστον μία ντουά", ru: "Прочитайте хотя бы одну дуа", sv: "Läs minst en dua", nl: "Lees minstens één dua", el: "Διάβασε τουλάχιστον μία ντουά" },
  "complete_lesson": { ar: "أكمل درساً", en: "Complete a lesson", de: "Lektion abschließen", fr: "Terminer une leçon", tr: "Ders tamamla", ru: "Завершить урок", sv: "Slutför en lektion", nl: "Voltooi een les", el: "Ολοκλήρωσε μάθημα", ru: "Завершить урок", sv: "Slutför en lektion", nl: "Voltooi een les", el: "Ολοκλήρωσε μάθημα" },
  "complete_lesson_desc": { ar: "أكمل درساً في أكاديمية نور", en: "Complete a Noor Academy lesson", de: "Noor Academy Lektion abschließen", fr: "Terminer une leçon Noor Academy", tr: "Noor Academy dersi tamamla", ru: "Завершите урок в Академии Нур", sv: "Slutför en Noor Academy-lektion", nl: "Voltooi een Noor Academy-les", el: "Ολοκλήρωσε μάθημα Noor Academy", ru: "Завершите урок в Академии Нур", sv: "Slutför en Noor Academy-lektion", nl: "Voltooi een Noor Academy-les", el: "Ολοκλήρωσε μάθημα Noor Academy" },
  "go_now": { ar: "ابدأ الآن", en: "Go Now", de: "Jetzt starten", fr: "Commencer", tr: "Şimdi Git", ru: "Начать", sv: "Gå nu", nl: "Ga nu", el: "Ξεκίνα τώρα", ru: "Начать", sv: "Gå nu", nl: "Ga nu", el: "Ξεκίνα τώρα" },
  "completed": { ar: "مكتمل ✓", en: "Completed ✓", de: "Abgeschlossen ✓", fr: "Terminé ✓", tr: "Tamamlandı ✓", ru: "Выполнено ✓", sv: "Slutfört ✓", nl: "Voltooid ✓", el: "Ολοκληρώθηκε ✓", ru: "Выполнено ✓", sv: "Slutfört ✓", nl: "Voltooid ✓", el: "Ολοκληρώθηκε ✓" },
  "coins_reward": { ar: "عملة مكافأة", en: "reward coins", de: "Belohnungsmünzen", fr: "pièces de récompense", tr: "ödül paraları", ru: "наградные монеты", sv: "belöningsmynt", nl: "beloningsmunte", el: "νομίσματα ανταμοιβής", ru: "наградные монеты", sv: "belöningsmynt", nl: "beloningsmunte", el: "νομίσματα ανταμοιβής" },
  "send_gold_kids": { ar: "أرسل ذهباً للأطفال", en: "Send Gold to Kids", de: "Gold an Kinder senden", fr: "Envoyer de l'or aux enfants", tr: "Çocuklara Altın Gönder", ru: "Отправить золото детям", sv: "Skicka guld till barn", nl: "Stuur goud naar kinderen", el: "Στείλε χρυσό στα παιδιά", ru: "Отправить золото детям", sv: "Skicka guld till barn", nl: "Stuur goud naar kinderen", el: "Στείλε χρυσό στα παιδιά" },
  "send_gold_desc": { ar: "أكمل مهامك اليومية لإرسال طوب ذهبي لطفلك", en: "Complete daily tasks to send golden bricks to your child", de: "Tägliche Aufgaben erledigen um goldene Steine zu senden", fr: "Complétez les tâches pour envoyer des briques à votre enfant", tr: "Günlük görevleri tamamlayarak çocuğunuza tuğla gönderin", ru: "Выполните задания чтобы отправить кирпичи ребёнку", sv: "Slutför uppgifter för att skicka stenar till ditt barn", nl: "Voltooi taken om stenen naar uw kind te sturen", el: "Ολοκλήρωσε εργασίες για να στείλεις τούβλα στο παιδί σου", ru: "Выполните задания чтобы отправить кирпичи ребёнку", sv: "Slutför uppgifter för att skicka stenar till ditt barn", nl: "Voltooi taken om stenen naar uw kind te sturen", el: "Ολοκλήρωσε εργασίες για να στείλεις τούβλα στο παιδί σου" },
  "send_bricks": { ar: "أرسل طوباً ذهبياً", en: "Send Golden Bricks", de: "Goldene Steine senden", fr: "Envoyer des briques", tr: "Tuğla Gönder", ru: "Отправить кирпичи", sv: "Skicka stenar", nl: "Stuur stenen", el: "Στείλε τούβλα", ru: "Отправить кирпичи", sv: "Skicka stenar", nl: "Stuur stenen", el: "Στείλε τούβλα" },
  "coppa_notice": { ar: "منطقة الأطفال خالية تماماً من الإعلانات ومحمية بمعايير COPPA", en: "Kids zone is 100% ad-free and protected by COPPA standards", de: "Kinderzone ist 100% werbefrei und COPPA-geschützt", fr: "Zone enfants 100% sans pub et protégée par COPPA", tr: "Çocuk bölgesi %100 reklamsız ve COPPA korumalı", ru: "Детская зона без рекламы и защищена стандартами COPPA", sv: "Barnzon 100% reklamfri och COPPA-skyddad", nl: "Kinderzone 100% reclamevrij en COPPA-beschermd", el: "Παιδική ζώνη 100% χωρίς διαφημίσεις και προστατευμένη", ru: "Детская зона без рекламы и защищена стандартами COPPA", sv: "Barnzon 100% reklamfri och COPPA-skyddad", nl: "Kinderzone 100% reclamevrij en COPPA-beschermd", el: "Παιδική ζώνη 100% χωρίς διαφημίσεις και προστατευμένη" },
  "leaderboard": { ar: "لوحة المتصدرين", en: "Leaderboard", de: "Bestenliste", fr: "Classement", tr: "Sıralama", ru: "Таблица лидеров", sv: "Topplista", nl: "Ranglijst", el: "Πίνακας κατάταξης", ru: "Таблица лидеров", sv: "Topplista", nl: "Ranglijst", el: "Πίνακας κατάταξης" },
  "transaction_history": { ar: "سجل المعاملات", en: "Transaction History", de: "Transaktionsverlauf", fr: "Historique", tr: "İşlem Geçmişi", ru: "История транзакций", sv: "Transaktionshistorik", nl: "Transactiegeschiedenis", el: "Ιστορικό συναλλαγών", ru: "История транзакций", sv: "Transaktionshistorik", nl: "Transactiegeschiedenis", el: "Ιστορικό συναλλαγών" },
  "tasks_completed": { ar: "مهام مكتملة اليوم", en: "Tasks completed today", de: "Heute erledigte Aufgaben", fr: "Tâches terminées aujourd'hui", tr: "Bugün tamamlanan görevler", ru: "Задания выполнены сегодня", sv: "Uppgifter slutförda idag", nl: "Taken voltooid vandaag", el: "Εργασίες σήμερα", ru: "Задания выполнены сегодня", sv: "Uppgifter slutförda idag", nl: "Taken voltooid vandaag", el: "Εργασίες σήμερα" },
  "rewards_store": { ar: "متجر المكافآت", en: "Rewards Store", de: "Belohnungsshop", fr: "Boutique de récompenses", tr: "Ödül Mağazası", ru: "Магазин наград", sv: "Belöningsbutik", nl: "Beloningswinkel", el: "Κατάστημα ανταμοιβών", ru: "Магазин наград", sv: "Belöningsbutik", nl: "Beloningswinkel", el: "Κατάστημα ανταμοιβών" },
  "redeem_now": { ar: "استبدل الآن", en: "Redeem", de: "Einlösen", fr: "Échanger", tr: "Kullan", ru: "Обменять", sv: "Lösa in", nl: "Inwisselen", el: "Εξαργύρωση", ru: "Обменять", sv: "Lösa in", nl: "Inwisselen", el: "Εξαργύρωση" },
  "already_redeemed": { ar: "تم الاستبدال ✓", en: "Redeemed ✓", de: "Eingelöst ✓", fr: "Échangé ✓", tr: "Kullanıldı ✓", ru: "Обменяно ✓", sv: "Inlöst ✓", nl: "Ingewisseld ✓", el: "Εξαργυρώθηκε ✓", ru: "Обменяно ✓", sv: "Inlöst ✓", nl: "Ingewisseld ✓", el: "Εξαργυρώθηκε ✓" },
  "insufficient_points": { ar: "نقاط غير كافية", en: "Insufficient points", de: "Unzureichende Punkte", fr: "Points insuffisants", tr: "Yetersiz puan", ru: "Недостаточно баллов", sv: "Otillräckliga poäng", nl: "Onvoldoende punten", el: "Ανεπαρκείς πόντοι", ru: "Недостаточно баллов", sv: "Otillräckliga poäng", nl: "Onvoldoende punten", el: "Ανεπαρκείς πόντοι" },
  "redeemed_success": { ar: "تم الاستبدال بنجاح! 🎉", en: "Redeemed successfully! 🎉", de: "Erfolgreich eingelöst! 🎉", fr: "Échangé avec succès! 🎉", tr: "Başarıyla kullanıldı! 🎉", ru: "Успешно обменяно! 🎉", sv: "Framgångsrikt inlöst! 🎉", nl: "Succesvol ingewisseld! 🎉", el: "Επιτυχής εξαργύρωση! 🎉", ru: "Успешно обменяно! 🎉", sv: "Framgångsrikt inlöst! 🎉", nl: "Succesvol ingewisseld! 🎉", el: "Επιτυχής εξαργύρωση! 🎉" },
  "watch_ad_earn": { ar: "شاهد إعلان واحصل على نقاط", en: "Watch Ad & Earn Points", de: "Werbung ansehen & Punkte verdienen", fr: "Regarder une pub & gagner des points", tr: "Reklam izle & Puan kazan", ru: "Смотри рекламу и получай баллы", sv: "Titta på annons och tjäna poäng", nl: "Bekijk advertentie en verdien punten", el: "Δες διαφήμιση και κέρδισε πόντους", ru: "Смотри рекламу и получай баллы", sv: "Titta på annons och tjäna poäng", nl: "Bekijk advertentie en verdien punten", el: "Δες διαφήμιση και κέρδισε πόντους" },
  "points_cost": { ar: "نقطة", en: "pts", de: "Pkt", fr: "pts", tr: "puan", ru: "баллов", sv: "poäng", nl: "punten", el: "πόντοι", ru: "баллов", sv: "poäng", nl: "punten", el: "πόντοι" },
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
  const [redeemItems, setRedeemItems] = useState<any[]>([]);
  const [redeeming, setRedeeming] = useState<string | null>(null);

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

  // Load redeem catalog
  useEffect(() => {
    fetch(`${BACKEND_URL}/api/store/redeem-catalog?user_id=${userId}&locale=${lang}`)
      .then(r => r.json())
      .then(d => { if (d.success) setRedeemItems(d.items || []); })
      .catch(() => {});
  }, [userId, lang]);

  const redeemReward = async (item: any) => {
    setRedeeming(item.id);
    try {
      const r = await fetch(`${BACKEND_URL}/api/store/redeem`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, mode: 'adults', reward_id: item.id, cost: item.cost }),
      });
      const d = await r.json();
      if (d.success) {
        setRedeemItems(prev => prev.map(i => i.id === item.id ? { ...i, redeemed: true } : i));
        loadData(); // Refresh wallet
        // Show success animation
        if (navigator.vibrate) navigator.vibrate([30, 15, 50]);
      } else if (d.message === 'insufficient_points') {
        // No toast needed, we'll show inline
      } else if (d.message === 'already_redeemed') {
        setRedeemItems(prev => prev.map(i => i.id === item.id ? { ...i, redeemed: true } : i));
      }
    } catch {}
    setRedeeming(null);
  };

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

        {/* ═══ REWARDS STORE — Redeem Points for Rewards ═══ */}
        {redeemItems.length > 0 && (
          <div>
            <h2 className="text-base font-bold mb-3 flex items-center gap-2">
              <Gift className="h-5 w-5 text-amber-500 dark:text-amber-400"/>
              {t('rewards_store')} ⭐
            </h2>
            <div className="space-y-3">
              {redeemItems.map((item: any) => (
                <div key={item.id} className={cn(
                  "p-4 rounded-2xl border transition-all overflow-hidden",
                  item.redeemed
                    ? "bg-emerald-500/10 border-emerald-500/30"
                    : "bg-gradient-to-br from-amber-500/10 to-orange-500/5 border-amber-400/20 hover:border-amber-400/40"
                )}>
                  <div className="flex items-start gap-3">
                    <div className="w-14 h-14 rounded-xl bg-card/50 flex items-center justify-center shrink-0 border border-border/20 overflow-hidden">
                      {item.image ? (
                        <img src={item.image} alt="" className="w-full h-full object-cover rounded-xl" />
                      ) : (
                        <span className="text-2xl">{item.emoji}</span>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-sm text-foreground">{item.title}</h3>
                      <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">{item.description}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <span className="text-xs font-bold text-amber-600 dark:text-amber-300 bg-amber-500/15 px-2.5 py-1 rounded-lg">
                          {item.cost} {t('points_cost')}
                        </span>
                        <span className="text-[10px] text-muted-foreground capitalize">{item.type}</span>
                      </div>
                    </div>
                    <div className="shrink-0">
                      {item.redeemed ? (
                        <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-3 py-2 rounded-xl whitespace-nowrap">
                          {t('already_redeemed')}
                        </span>
                      ) : (
                        <button
                          onClick={() => redeemReward(item)}
                          disabled={redeeming === item.id || (wallet?.blessing_coins || 0) < item.cost}
                          className={cn(
                            "text-xs font-bold px-3 py-2 rounded-xl transition-all whitespace-nowrap",
                            (wallet?.blessing_coins || 0) >= item.cost
                              ? "bg-gradient-to-r from-amber-500 to-orange-500 text-white hover:shadow-lg active:scale-95"
                              : "bg-muted/30 text-muted-foreground cursor-not-allowed"
                          )}
                        >
                          {redeeming === item.id ? '...' : (wallet?.blessing_coins || 0) >= item.cost ? t('redeem_now') : t('insufficient_points')}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

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
