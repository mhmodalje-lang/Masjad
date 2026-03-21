import { useState, useEffect, useCallback, useRef } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { useNoorTTS, getNoorMessage } from '@/components/NoorMascot';
import { Star, Mic, MicOff, Volume2, Sparkles, ArrowLeft, Zap, Check, X, ChevronRight, Flame, Lock, Crown, ChevronDown, BookOpen, Heart, GraduationCap, Calendar, ScrollText } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

const API = import.meta.env.REACT_APP_BACKEND_URL || '';

// ═══ TYPES ═══
interface StageNode { id: string; title_ar: string; title_en: string; type: string; unlocked: boolean; completed: boolean; stars: number; is_current: boolean; is_boss: boolean; }
interface World { id: string; title_ar: string; title_en: string; emoji: string; color: string; description_ar: string; description_en: string; stages: StageNode[]; progress: number; total: number; }
interface Activity { phase: string; phase_ar: string; phase_emoji: string; [key: string]: any; }
type MainTab = 'journey' | 'lesson' | 'quran' | 'islam' | 'library';
type View = 'tabs' | 'stage' | 'result' | 'surah_detail' | 'prophet_detail' | 'library_item';

// ═══ NOOR 10-LANG MESSAGES ═══
const N: Record<string, Record<string, string>> = {
  intro: { ar:'شاهد واستمع جيداً! 👁️', en:'Watch and listen! 👁️', de:'Schau und hör zu! 👁️', 'de-AT':'Schau und hör zua! 👁️', fr:'Regarde et écoute! 👁️', tr:'İzle ve dinle! 👁️', ru:'Смотри и слушай! 👁️', sv:'Titta och lyssna! 👁️', nl:'Kijk en luister! 👁️', el:'Κοίτα κι άκου! 👁️' },
  find: { ar:'اعثر على الحرف الصحيح! 🔍', en:'Find the right letter! 🔍', de:'Finde den richtigen Buchstaben! 🔍', 'de-AT':'Find den richtigen Buchstaben! 🔍', fr:'Trouve la bonne lettre! 🔍', tr:'Doğru harfi bul! 🔍', ru:'Найди правильную букву! 🔍', sv:'Hitta rätt bokstav! 🔍', nl:'Vind de juiste letter! 🔍', el:'Βρες το σωστό γράμμα! 🔍' },
  say: { ar:'انطق بصوت واضح! 🎤', en:'Say it clearly! 🎤', de:'Sag es deutlich! 🎤', 'de-AT':'Sag\'s klar und deutlich! 🎤', fr:'Dis-le clairement! 🎤', tr:'Net söyle! 🎤', ru:'Скажи чётко! 🎤', sv:'Säg det tydligt! 🎤', nl:'Zeg het duidelijk! 🎤', el:'Πες το καθαρά! 🎤' },
  done: { ar:'أحسنت! أكملت المرحلة! 🎉', en:'Amazing! Stage complete! 🎉', de:'Toll! Stufe geschafft! 🎉', 'de-AT':'Super! Stufe gschafft! 🎉', fr:'Bravo! Étape terminée! 🎉', tr:'Harika! Aşama tamam! 🎉', ru:'Молодец! Этап пройден! 🎉', sv:'Bra! Stadiet klart! 🎉', nl:'Geweldig! Fase compleet! 🎉', el:'Μπράβο! Στάδιο ολοκληρώθηκε! 🎉' },
  wrong: { ar:'حاول مرة أخرى! أنت قادر! 💪', en:"Try again! You've got this! 💪", de:'Nochmal! Du schaffst das! 💪', 'de-AT':'Nochmal! Du schaffst des! 💪', fr:'Réessaie! Tu peux! 💪', tr:'Tekrar dene! Yapabilirsin! 💪', ru:'Ещё раз! У тебя получится! 💪', sv:'Försök igen! Du kan! 💪', nl:'Probeer nog eens! Je kan het! 💪', el:'Ξαναπροσπάθησε! 💪' },
};
const nm = (k: string, l: string) => N[k]?.[l] || N[k]?.en || '';

// ═══ TAB LABELS ═══
const TAB_LABELS: Record<MainTab, Record<string, string>> = {
  journey: { ar: 'الرحلة', en: 'Journey', de: 'Reise', fr: 'Voyage', tr: 'Yolculuk', ru: 'Путь', sv: 'Resa', nl: 'Reis', el: 'Ταξίδι' },
  lesson: { ar: 'درس اليوم', en: 'Daily Lesson', de: 'Tageslektion', fr: 'Leçon du jour', tr: 'Günlük Ders', ru: 'Урок дня', sv: 'Dagens lektion', nl: 'Dagles', el: 'Μάθημα ημέρας' },
  quran: { ar: 'القرآن', en: 'Quran', de: 'Koran', fr: 'Coran', tr: "Kur'an", ru: 'Коран', sv: 'Koranen', nl: 'Koran', el: 'Κοράνι' },
  islam: { ar: 'الإسلام', en: 'Islam', de: 'Islam', fr: 'Islam', tr: 'İslam', ru: 'Ислам', sv: 'Islam', nl: 'Islam', el: 'Ισλάμ' },
  library: { ar: 'المكتبة', en: 'Library', de: 'Bibliothek', fr: 'Bibliothèque', tr: 'Kütüphane', ru: 'Библиотека', sv: 'Bibliotek', nl: 'Bibliotheek', el: 'Βιβλιοθήκη' },
};
const TAB_ICONS: Record<MainTab, string> = { journey: '🗺️', lesson: '📅', quran: '📖', islam: '🕌', library: '📚' };

// ═══ CONFETTI ═══
function Confetti({ on }: { on: boolean }) {
  if (!on) return null;
  return (
    <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
      {Array.from({ length: 35 }).map((_, i) => (
        <div key={i} className="absolute animate-confetti-fall" style={{ left: `${Math.random()*100}%`, top: '-10px', animationDelay: `${Math.random()*2}s`, animationDuration: `${2+Math.random()*3}s` }}>
          <span className="text-2xl">{['⭐','🌟','✨','🎉','🧱','🕌','💛','🌙'][i%8]}</span>
        </div>
      ))}
    </div>
  );
}

// ═══ JOURNEY MAP NODE ═══
function MapNode({ stage, onClick, isRTL }: { stage: StageNode; onClick: () => void; isRTL: boolean }) {
  const size = stage.is_boss ? 'w-16 h-16' : 'w-14 h-14';
  return (
    <button onClick={onClick} disabled={!stage.unlocked}
      className={cn("relative flex flex-col items-center gap-1 transition-all", !stage.unlocked && "opacity-40", stage.is_current && "scale-110")}>
      <div className={cn(size, "rounded-full flex items-center justify-center text-xl font-bold border-[3px] shadow-lg transition-all",
        stage.completed ? "bg-gradient-to-br from-green-400 to-emerald-500 border-green-300 text-white shadow-green-500/40" :
        stage.is_current ? "bg-gradient-to-br from-amber-400 to-orange-500 border-amber-300 text-white shadow-amber-500/40 animate-pulse" :
        stage.is_boss ? "bg-gradient-to-br from-purple-500 to-violet-600 border-purple-300 text-white shadow-purple-500/30" :
        !stage.unlocked ? "bg-muted border-muted-foreground/20 text-muted-foreground" :
        "bg-gradient-to-br from-blue-400 to-cyan-500 border-blue-300 text-white shadow-blue-500/30"
      )}>
        {!stage.unlocked ? <Lock className="h-5 w-5" /> :
         stage.completed ? <Check className="h-6 w-6" /> :
         stage.is_boss ? <Crown className="h-6 w-6" /> :
         stage.is_current ? <Sparkles className="h-5 w-5" /> :
         <span className="text-base">{stage.title_ar.charAt(0)}</span>}
      </div>
      {stage.completed && (
        <div className="flex gap-0.5">{[1,2,3].map(s => (<Star key={s} className={cn("h-3 w-3", s <= stage.stars ? "text-amber-400 fill-amber-400" : "text-muted-foreground/30")} />))}</div>
      )}
      <span className={cn("text-[10px] font-bold max-w-[70px] text-center leading-tight",
        stage.is_current ? "text-amber-400" : stage.completed ? "text-green-400" : "text-muted-foreground"
      )}>{isRTL ? stage.title_ar : (stage.title_en || stage.title_ar)}</span>
    </button>
  );
}

// ═══ SECTION CARD (for daily lesson sections) ═══
function SectionCard({ emoji, title, children, color = "blue" }: { emoji: string; title: string; children: React.ReactNode; color?: string }) {
  const colors: Record<string, string> = {
    blue: "from-blue-500/15 to-cyan-500/10 border-blue-400/30",
    green: "from-emerald-500/15 to-teal-500/10 border-emerald-400/30",
    amber: "from-amber-500/15 to-orange-500/10 border-amber-400/30",
    purple: "from-purple-500/15 to-violet-500/10 border-purple-400/30",
    pink: "from-pink-500/15 to-rose-500/10 border-pink-400/30",
    indigo: "from-indigo-500/15 to-blue-500/10 border-indigo-400/30",
    teal: "from-teal-500/15 to-emerald-500/10 border-teal-400/30",
  };
  return (
    <div className={cn("rounded-2xl border p-4 bg-gradient-to-br", colors[color] || colors.blue)}>
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">{emoji}</span>
        <h3 className="font-bold text-sm">{title}</h3>
      </div>
      {children}
    </div>
  );
}

// ═══ MAIN COMPONENT ═══
export default function KidsZone() {
  const { t, dir, locale } = useLocale();
  const nav = useNavigate();
  const { speak } = useNoorTTS();
  const isRTL = dir === 'rtl';
  const lang = locale || 'ar';

  // Tab state
  const [mainTab, setMainTab] = useState<MainTab>('lesson');
  const [view, setView] = useState<View>('tabs');

  // Journey state
  const [worlds, setWorlds] = useState<World[]>([]);
  const [xp, setXp] = useState(0);
  const [bricks, setBricks] = useState(0);
  const [mosque, setMosque] = useState<any>(null);
  const [currentStage, setCurrentStage] = useState('');
  const [activeStage, setActiveStage] = useState<any>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [activityIdx, setActivityIdx] = useState(0);
  const [noorText, setNoorText] = useState('');
  const [confetti, setConfetti] = useState(false);
  const [stageResult, setStageResult] = useState<any>(null);
  const [userId] = useState(() => localStorage.getItem('kids_user_id') || `kid_${Date.now()}`);
  const [streak] = useState(() => parseInt(localStorage.getItem('kids_streak') || '1'));
  const [expandedWorld, setExpandedWorld] = useState<string | null>(null);

  // IRS game state
  const [introStep, setIntroStep] = useState(0);
  const [gridAnswer, setGridAnswer] = useState<number | null>(null);
  const [wrongFlash, setWrongFlash] = useState(false);
  const [correctFlash, setCorrectFlash] = useState(false);
  const [sayIdx, setSayIdx] = useState(0);
  const [listening, setListening] = useState(false);
  const [spokenText, setSpokenText] = useState('');
  const [accuracy, setAccuracy] = useState(0);
  const [sayDone, setSayDone] = useState<Set<number>>(new Set());
  const [starsEarned, setStarsEarned] = useState(3);
  const recRef = useRef<any>(null);

  // Learning state
  const [dailyLesson, setDailyLesson] = useState<any>(null);
  const [lessonDay, setLessonDay] = useState(0);
  const [quranSurahs, setQuranSurahs] = useState<any[]>([]);
  const [selectedSurah, setSelectedSurah] = useState<any>(null);
  const [duas, setDuas] = useState<any[]>([]);
  const [hadiths, setHadiths] = useState<any[]>([]);
  const [prophets, setProphets] = useState<any[]>([]);
  const [selectedProphet, setSelectedProphet] = useState<any>(null);
  const [pillars, setPillars] = useState<any[]>([]);
  const [libraryCategories, setLibraryCategories] = useState<any[]>([]);
  const [libraryItems, setLibraryItems] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedLibItem, setSelectedLibItem] = useState<any>(null);
  const [islamSubTab, setIslamSubTab] = useState<'duas' | 'hadiths' | 'prophets' | 'pillars'>('duas');
  const [learnProgress, setLearnProgress] = useState<any>(null);
  const [completedSections, setCompletedSections] = useState<Set<string>>(new Set());

  useEffect(() => { localStorage.setItem('kids_user_id', userId); }, [userId]);
  
  useEffect(() => {
    if (mainTab === 'journey') loadJourney();
    if (mainTab === 'lesson') loadDailyLesson();
    if (mainTab === 'quran') loadQuranSurahs();
    if (mainTab === 'islam') { loadDuas(); loadHadiths(); loadProphets(); loadPillars(); }
    if (mainTab === 'library') loadLibraryCategories();
    loadProgress();
  }, [mainTab, locale]);

  // ═══ DATA LOADERS ═══
  const loadJourney = useCallback(async () => {
    try {
      const r = await fetch(`${API}/api/kids-zone/journey?user_id=${userId}`);
      const d = await r.json();
      if (d.success) {
        setWorlds(d.worlds); setXp(d.total_xp); setBricks(d.golden_bricks); setMosque(d.mosque); setCurrentStage(d.current_stage);
        for (const w of d.worlds) { if (w.stages.some((s: StageNode) => s.is_current)) { setExpandedWorld(w.id); break; } }
      }
    } catch {}
  }, [userId]);

  const loadDailyLesson = async (day?: number) => {
    try {
      const d = day || lessonDay || 0;
      const r = await fetch(`${API}/api/kids-learn/daily-lesson?day=${d}&locale=${lang}`);
      const data = await r.json();
      if (data.success) { setDailyLesson(data.lesson); setLessonDay(data.lesson.day); setCompletedSections(new Set()); }
    } catch {}
  };

  const loadQuranSurahs = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/quran/surahs?locale=${lang}`); const d = await r.json(); if (d.success) setQuranSurahs(d.surahs); } catch {}
  };

  const loadDuas = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/duas?locale=${lang}`); const d = await r.json(); if (d.success) setDuas(d.duas); } catch {}
  };

  const loadHadiths = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/hadiths?locale=${lang}`); const d = await r.json(); if (d.success) setHadiths(d.hadiths); } catch {}
  };

  const loadProphets = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/prophets?locale=${lang}`); const d = await r.json(); if (d.success) setProphets(d.prophets); } catch {}
  };

  const loadPillars = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/islamic-pillars?locale=${lang}`); const d = await r.json(); if (d.success) setPillars(d.pillars); } catch {}
  };

  const loadLibraryCategories = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/library/categories?locale=${lang}`); const d = await r.json(); if (d.success) setLibraryCategories(d.categories); } catch {}
    loadLibraryItems('all');
  };

  const loadLibraryItems = async (cat: string) => {
    try { const r = await fetch(`${API}/api/kids-learn/library/items?category=${cat}&locale=${lang}`); const d = await r.json(); if (d.success) setLibraryItems(d.items); } catch {}
  };

  const loadProgress = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/progress?user_id=${userId}`); const d = await r.json(); if (d.success) setLearnProgress(d.progress); } catch {}
  };

  const markSectionDone = (section: string) => {
    setCompletedSections(prev => new Set([...prev, section]));
  };

  const saveDayProgress = async () => {
    try {
      await fetch(`${API}/api/kids-learn/progress`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, day: lessonDay, sections_completed: Array.from(completedSections) }),
      });
      setConfetti(true); setTimeout(() => setConfetti(false), 3000);
      toast.success(isRTL ? 'أحسنت! أكملت درس اليوم! 🎉' : 'Great job! Lesson complete! 🎉');
      loadProgress();
    } catch {}
  };

  // ═══ JOURNEY FUNCTIONS ═══
  const openStage = useCallback(async (stageId: string) => {
    try {
      const r = await fetch(`${API}/api/kids-zone/stage/${stageId}?user_id=${userId}`);
      const d = await r.json();
      if (d.success) {
        setActiveStage(d.stage); setActivities(d.activities); setActivityIdx(0); setIntroStep(0);
        setGridAnswer(null); setSayIdx(0); setSayDone(new Set()); setSpokenText(''); setAccuracy(0);
        setStarsEarned(3); setView('stage'); setNoorText(nm('intro', locale));
      }
    } catch { toast.error('Error loading stage'); }
  }, [userId, locale]);

  const completeStage = useCallback(async () => {
    if (!activeStage) return;
    try {
      const r = await fetch(`${API}/api/kids-zone/complete-stage`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, stage_id: activeStage.id, stars: starsEarned }),
      });
      const d = await r.json();
      if (d.success) {
        setStageResult(d); setView('result'); setConfetti(true);
        setTimeout(() => setConfetti(false), 4000);
        setNoorText(nm('done', locale)); speak(getNoorMessage('correct', locale));
      }
    } catch {}
  }, [activeStage, starsEarned, userId, locale, speak]);

  const goNextActivity = () => {
    if (activityIdx < activities.length - 1) {
      const nextIdx = activityIdx + 1; setActivityIdx(nextIdx);
      const phase = activities[nextIdx]?.phase;
      if (phase === 'recognize') setNoorText(nm('find', locale));
      else if (phase === 'say') setNoorText(nm('say', locale));
      setGridAnswer(null); setSayIdx(0); setSayDone(new Set()); setSpokenText(''); setAccuracy(0); setIntroStep(0);
    } else { completeStage(); }
  };

  // ═══ SPEECH RECOGNITION ═══
  const startSpeech = useCallback((target: string) => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) { toast.error('Speech not supported'); return; }
    const r = new SR(); r.lang = 'ar-SA'; r.continuous = false; r.interimResults = false;
    r.onresult = (e: any) => {
      const sp = e.results[0][0].transcript.trim(); setSpokenText(sp);
      const tc = target.replace(/[\u064B-\u065F\u0670]/g, '');
      const sc = sp.replace(/[\u064B-\u065F\u0670]/g, '');
      let acc = 0;
      if (sc === tc) acc = 100;
      else if (tc.includes(sc) || sc.includes(tc)) acc = 80;
      else { const ts = new Set(tc.split('')); const ss = new Set(sc.split('')); let o = 0; ts.forEach(c => { if (ss.has(c)) o++; }); acc = Math.round((o / Math.max(ts.size, 1)) * 100); }
      setAccuracy(acc); setListening(false);
      if (acc >= 70) { const ns = new Set(sayDone); ns.add(sayIdx); setSayDone(ns); speak(getNoorMessage('correct', locale)); }
      else { setStarsEarned(s => Math.max(1, s - 1)); speak(getNoorMessage('wrong', locale)); }
    };
    r.onerror = () => setListening(false); r.onend = () => setListening(false);
    recRef.current = r; r.start(); setListening(true); setSpokenText(''); setAccuracy(0);
  }, [sayDone, sayIdx, locale, speak]);

  const act = activities[activityIdx];

  // ═══════════════════ RENDER DAILY LESSON ═══════════════════
  const renderDailyLesson = () => {
    if (!dailyLesson) return <div className="flex items-center justify-center h-40"><div className="animate-spin w-8 h-8 border-2 border-amber-400 border-t-transparent rounded-full" /></div>;
    const L = dailyLesson;
    return (
      <div className="space-y-4 pb-8">
        {/* Day selector & progress */}
        <div className="flex items-center justify-between">
          <button onClick={() => loadDailyLesson(Math.max(1, lessonDay - 1))} className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-sm font-bold">←</button>
          <div className="text-center">
            <p className="text-xs text-muted-foreground">{isRTL ? 'اليوم' : 'Day'}</p>
            <span className="text-2xl font-bold bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">{L.day}</span>
          </div>
          <button onClick={() => loadDailyLesson(lessonDay + 1)} className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-sm font-bold">→</button>
        </div>

        {/* Greeting */}
        <div className="p-4 rounded-2xl bg-gradient-to-r from-violet-500/10 to-pink-500/10 border border-violet-500/20 text-center">
          <span className="text-3xl">🐣</span>
          <p className="text-sm font-medium mt-1">{L.greeting}</p>
        </div>

        {/* Streak & XP */}
        {learnProgress && (
          <div className="flex gap-3">
            <div className="flex-1 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-center">
              <Flame className="h-5 w-5 text-red-400 mx-auto" />
              <p className="text-lg font-bold text-red-400">{learnProgress.streak || 0}</p>
              <p className="text-[10px] text-muted-foreground">{isRTL ? 'أيام متتالية' : 'Day Streak'}</p>
            </div>
            <div className="flex-1 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
              <Zap className="h-5 w-5 text-amber-400 mx-auto" />
              <p className="text-lg font-bold text-amber-400">{learnProgress.xp || 0}</p>
              <p className="text-[10px] text-muted-foreground">XP</p>
            </div>
            <div className="flex-1 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-center">
              <Calendar className="h-5 w-5 text-emerald-400 mx-auto" />
              <p className="text-lg font-bold text-emerald-400">{learnProgress.total_lessons || 0}</p>
              <p className="text-[10px] text-muted-foreground">{isRTL ? 'دروس' : 'Lessons'}</p>
            </div>
          </div>
        )}

        {/* Section 1: Quran */}
        <SectionCard emoji={L.quran.section_emoji} title={L.quran.section_title} color="green">
          <div className="text-center space-y-2">
            <p className="text-xs text-emerald-400">{L.quran.surah_name} - {isRTL ? 'آية' : 'Ayah'} {L.quran.ayah.number}</p>
            <button onClick={() => speak(L.quran.ayah.arabic, 'ar')} className="w-full">
              <p className="text-2xl font-bold font-arabic leading-loose py-3" dir="rtl">{L.quran.ayah.arabic}</p>
            </button>
            {L.quran.ayah.translation && lang !== 'ar' && (
              <p className="text-sm text-muted-foreground italic">{L.quran.ayah.translation}</p>
            )}
            <p className="text-xs text-emerald-400/70">{L.quran.tip}</p>
            <div className="flex gap-2 mt-2">
              <button onClick={() => speak(L.quran.ayah.arabic, 'ar')} className="flex-1 py-2 rounded-xl bg-emerald-500/20 text-emerald-300 text-sm flex items-center justify-center gap-1 border border-emerald-500/30">
                <Volume2 className="h-3.5 w-3.5" /> {isRTL ? 'استمع' : 'Listen'}
              </button>
              <button onClick={() => markSectionDone('quran')} className={cn("flex-1 py-2 rounded-xl text-sm flex items-center justify-center gap-1 border",
                completedSections.has('quran') ? "bg-green-500/20 text-green-300 border-green-500/30" : "bg-white/10 text-white/70 border-white/10"
              )}>
                <Check className="h-3.5 w-3.5" /> {completedSections.has('quran') ? (isRTL ? 'تم ✓' : 'Done ✓') : (isRTL ? 'حفظت' : 'Memorized')}
              </button>
            </div>
          </div>
        </SectionCard>

        {/* Section 2: Dua */}
        <SectionCard emoji={L.dua.section_emoji} title={L.dua.section_title} color="blue">
          <div className="space-y-2">
            <p className="text-xs font-bold text-blue-400">{L.dua.title}</p>
            <button onClick={() => speak(L.dua.arabic, 'ar')} className="w-full text-start">
              <p className="text-xl font-bold font-arabic leading-relaxed" dir="rtl">{L.dua.arabic}</p>
            </button>
            {L.dua.transliteration && <p className="text-sm text-blue-300/60 italic">{L.dua.transliteration}</p>}
            {L.dua.meaning && <p className="text-sm text-muted-foreground">{L.dua.meaning}</p>}
            <button onClick={() => markSectionDone('dua')} className={cn("w-full py-2 rounded-xl text-sm flex items-center justify-center gap-1 border mt-2",
              completedSections.has('dua') ? "bg-green-500/20 text-green-300 border-green-500/30" : "bg-white/10 text-white/70 border-white/10"
            )}>
              <Check className="h-3.5 w-3.5" /> {completedSections.has('dua') ? (isRTL ? 'تم ✓' : 'Done ✓') : (isRTL ? 'حفظت الدعاء' : 'Learned Dua')}
            </button>
          </div>
        </SectionCard>

        {/* Section 3: Hadith */}
        <SectionCard emoji={L.hadith.section_emoji} title={L.hadith.section_title} color="amber">
          <div className="space-y-2">
            <p className="text-lg font-bold font-arabic leading-relaxed" dir="rtl">{L.hadith.arabic}</p>
            {L.hadith.translation && lang !== 'ar' && <p className="text-sm text-muted-foreground italic">{L.hadith.translation}</p>}
            <p className="text-xs text-amber-400/70">📌 {L.hadith.source}</p>
            <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/20 mt-2">
              <p className="text-xs font-bold text-amber-300">💡 {isRTL ? 'الدرس:' : 'Lesson:'} {L.hadith.lesson}</p>
            </div>
            <button onClick={() => markSectionDone('hadith')} className={cn("w-full py-2 rounded-xl text-sm flex items-center justify-center gap-1 border mt-2",
              completedSections.has('hadith') ? "bg-green-500/20 text-green-300 border-green-500/30" : "bg-white/10 text-white/70 border-white/10"
            )}>
              <Check className="h-3.5 w-3.5" /> {completedSections.has('hadith') ? (isRTL ? 'تم ✓' : 'Done ✓') : (isRTL ? 'فهمت الحديث' : 'Understood')}
            </button>
          </div>
        </SectionCard>

        {/* Section 4: Prophet Story */}
        <SectionCard emoji={L.story.section_emoji} title={L.story.section_title} color="purple">
          <div className="space-y-2">
            <p className="text-lg font-bold">{L.story.prophet_name}</p>
            <p className="text-xs text-purple-400">{L.story.title}</p>
            <p className="text-sm leading-relaxed">{L.story.summary}</p>
            <div className="p-2 rounded-xl bg-purple-500/10 border border-purple-500/20">
              <p className="text-xs font-bold text-purple-300">💡 {isRTL ? 'العبرة:' : 'Lesson:'} {L.story.lesson}</p>
            </div>
            <p className="text-xs text-muted-foreground">📖 {L.story.quran_ref}</p>
            <button onClick={() => markSectionDone('story')} className={cn("w-full py-2 rounded-xl text-sm flex items-center justify-center gap-1 border mt-2",
              completedSections.has('story') ? "bg-green-500/20 text-green-300 border-green-500/30" : "bg-white/10 text-white/70 border-white/10"
            )}>
              <Check className="h-3.5 w-3.5" /> {completedSections.has('story') ? (isRTL ? 'تم ✓' : 'Done ✓') : (isRTL ? 'قرأت القصة' : 'Read Story')}
            </button>
          </div>
        </SectionCard>

        {/* Section 5: Islamic Knowledge */}
        <SectionCard emoji={L.islamic_knowledge.section_emoji} title={L.islamic_knowledge.section_title} color="teal">
          <div className="space-y-2">
            <p className="text-lg font-bold">{L.islamic_knowledge.topic}</p>
            <p className="text-sm leading-relaxed">{L.islamic_knowledge.description}</p>
            <button onClick={() => markSectionDone('knowledge')} className={cn("w-full py-2 rounded-xl text-sm flex items-center justify-center gap-1 border mt-2",
              completedSections.has('knowledge') ? "bg-green-500/20 text-green-300 border-green-500/30" : "bg-white/10 text-white/70 border-white/10"
            )}>
              <Check className="h-3.5 w-3.5" /> {completedSections.has('knowledge') ? (isRTL ? 'تم ✓' : 'Done ✓') : (isRTL ? 'تعلمت' : 'Learned')}
            </button>
          </div>
        </SectionCard>

        {/* Section 6: Library Pick */}
        <SectionCard emoji={L.library_pick.section_emoji} title={L.library_pick.section_title} color="indigo">
          <div className="space-y-2">
            <p className="text-lg font-bold">{L.library_pick.title}</p>
            <p className="text-sm leading-relaxed">{L.library_pick.content}</p>
            <button onClick={() => markSectionDone('library')} className={cn("w-full py-2 rounded-xl text-sm flex items-center justify-center gap-1 border mt-2",
              completedSections.has('library') ? "bg-green-500/20 text-green-300 border-green-500/30" : "bg-white/10 text-white/70 border-white/10"
            )}>
              <Check className="h-3.5 w-3.5" /> {completedSections.has('library') ? (isRTL ? 'تم ✓' : 'Done ✓') : (isRTL ? 'قرأت' : 'Read')}
            </button>
          </div>
        </SectionCard>

        {/* Section 7: Activity */}
        <SectionCard emoji={L.activity.emoji} title={L.activity.title} color="pink">
          <p className="text-sm">{L.activity.description}</p>
          <button onClick={() => markSectionDone('activity')} className={cn("w-full py-2 rounded-xl text-sm flex items-center justify-center gap-1 border mt-3",
            completedSections.has('activity') ? "bg-green-500/20 text-green-300 border-green-500/30" : "bg-white/10 text-white/70 border-white/10"
          )}>
            <Check className="h-3.5 w-3.5" /> {completedSections.has('activity') ? (isRTL ? 'أنجزت ✓' : 'Done ✓') : (isRTL ? 'أنجزت النشاط' : 'Completed Activity')}
          </button>
        </SectionCard>

        {/* Complete Day */}
        {completedSections.size >= 3 && (
          <button onClick={saveDayProgress} className="w-full py-4 rounded-2xl bg-gradient-to-r from-emerald-500 to-green-500 text-white font-bold text-lg shadow-lg shadow-emerald-500/30 flex items-center justify-center gap-2">
            <Sparkles className="h-5 w-5" /> {isRTL ? `أكمل درس اليوم ${lessonDay}! 🎉` : `Complete Day ${lessonDay}! 🎉`}
          </button>
        )}
      </div>
    );
  };

  // ═══════════════════ RENDER QURAN ═══════════════════
  const renderQuran = () => {
    if (selectedSurah) {
      return (
        <div className="space-y-4 pb-8">
          <button onClick={() => setSelectedSurah(null)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-white">
            <ArrowLeft className="h-4 w-4" /> {isRTL ? 'العودة' : 'Back'}
          </button>
          <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 border border-emerald-400/30">
            <p className="text-3xl font-bold font-arabic">{selectedSurah.name_ar}</p>
            <p className="text-sm text-emerald-400 mt-1">{selectedSurah.name_en} - {selectedSurah.total_ayahs} {isRTL ? 'آيات' : 'Ayahs'}</p>
          </div>
          {selectedSurah.ayahs?.map((a: any, i: number) => (
            <button key={i} onClick={() => speak(a.arabic, 'ar')}
              className="w-full p-4 rounded-2xl bg-card/60 border border-white/10 text-start hover:border-emerald-400/30 transition-all">
              <div className="flex items-start gap-3">
                <span className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-xs font-bold text-emerald-400 shrink-0">{a.number}</span>
                <div className="flex-1">
                  <p className="text-xl font-bold font-arabic leading-loose" dir="rtl">{a.arabic}</p>
                  {a.translation && <p className="text-sm text-muted-foreground mt-2">{a.translation}</p>}
                </div>
                <Volume2 className="h-4 w-4 text-emerald-400 shrink-0 mt-2" />
              </div>
            </button>
          ))}
        </div>
      );
    }

    return (
      <div className="space-y-4 pb-8">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 border border-emerald-400/30">
          <span className="text-4xl">📖</span>
          <h2 className="text-lg font-bold mt-2">{isRTL ? 'حفظ القرآن الكريم' : 'Quran Memorization'}</h2>
          <p className="text-xs text-muted-foreground mt-1">{isRTL ? 'سور قصيرة للحفظ مع المعنى' : 'Short surahs for memorization with meanings'}</p>
        </div>
        <div className="grid grid-cols-2 gap-3">
          {quranSurahs.map(s => (
            <button key={s.id} onClick={() => setSelectedSurah(s)}
              className="p-4 rounded-2xl bg-card/60 border border-white/10 hover:border-emerald-400/30 transition-all text-start">
              <div className="flex items-center gap-2">
                <span className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-xs font-bold text-emerald-400">{s.number}</span>
                <div>
                  <p className="font-bold text-sm font-arabic">{s.name_ar}</p>
                  <p className="text-[10px] text-muted-foreground">{s.name_en}</p>
                </div>
              </div>
              <p className="text-[10px] text-muted-foreground mt-2">{s.total_ayahs} {isRTL ? 'آيات' : 'ayahs'}</p>
            </button>
          ))}
        </div>
      </div>
    );
  };

  // ═══════════════════ RENDER ISLAM ═══════════════════
  const renderIslam = () => {
    if (selectedProphet) {
      return (
        <div className="space-y-4 pb-8">
          <button onClick={() => setSelectedProphet(null)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-white">
            <ArrowLeft className="h-4 w-4" /> {isRTL ? 'العودة' : 'Back'}
          </button>
          <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-purple-500/15 to-violet-500/10 border border-purple-400/30">
            <span className="text-5xl">{selectedProphet.emoji}</span>
            <h2 className="text-xl font-bold mt-2">{selectedProphet.name}</h2>
            <p className="text-sm text-purple-400">{selectedProphet.title}</p>
          </div>
          <div className="p-4 rounded-2xl bg-card/60 border border-white/10">
            <p className="text-sm leading-relaxed">{selectedProphet.summary}</p>
          </div>
          <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20">
            <p className="text-sm font-bold text-purple-300">💡 {isRTL ? 'العبرة:' : 'Lesson:'} {selectedProphet.lesson}</p>
          </div>
          <p className="text-xs text-muted-foreground text-center">📖 {selectedProphet.quran_ref}</p>
        </div>
      );
    }

    const subTabs = [
      { id: 'duas' as const, label: isRTL ? 'أدعية' : 'Duas', emoji: '🤲' },
      { id: 'hadiths' as const, label: isRTL ? 'أحاديث' : 'Hadiths', emoji: '📜' },
      { id: 'prophets' as const, label: isRTL ? 'أنبياء' : 'Prophets', emoji: '🕌' },
      { id: 'pillars' as const, label: isRTL ? 'أركان' : 'Pillars', emoji: '☪️' },
    ];

    return (
      <div className="space-y-4 pb-8">
        {/* Sub tabs */}
        <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
          {subTabs.map(st => (
            <button key={st.id} onClick={() => setIslamSubTab(st.id)}
              className={cn("flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap border transition-all",
                islamSubTab === st.id ? "bg-gradient-to-r from-emerald-500/20 to-teal-500/20 border-emerald-400/40 text-emerald-300" : "bg-white/5 border-white/10 text-muted-foreground"
              )}>
              <span>{st.emoji}</span> {st.label}
            </button>
          ))}
        </div>

        {/* Duas */}
        {islamSubTab === 'duas' && (
          <div className="space-y-3">
            {duas.map(d => (
              <button key={d.id} onClick={() => speak(d.arabic, 'ar')} className="w-full p-4 rounded-2xl bg-card/60 border border-white/10 text-start hover:border-blue-400/30 transition-all">
                <div className="flex items-center gap-2 mb-2">
                  <span>{d.emoji}</span>
                  <span className="text-xs font-bold text-blue-400">{d.title}</span>
                  <Volume2 className="h-3 w-3 text-blue-400 ms-auto" />
                </div>
                <p className="text-lg font-bold font-arabic leading-relaxed" dir="rtl">{d.arabic}</p>
                {d.transliteration && <p className="text-xs text-blue-300/50 mt-1 italic">{d.transliteration}</p>}
                {d.meaning && <p className="text-sm text-muted-foreground mt-1">{d.meaning}</p>}
              </button>
            ))}
          </div>
        )}

        {/* Hadiths */}
        {islamSubTab === 'hadiths' && (
          <div className="space-y-3">
            {hadiths.map(h => (
              <div key={h.id} className="p-4 rounded-2xl bg-card/60 border border-white/10">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">{h.emoji}</span>
                  <span className="text-xs font-bold text-amber-400 capitalize">{h.category}</span>
                </div>
                <p className="text-lg font-bold font-arabic leading-relaxed" dir="rtl">{h.arabic}</p>
                {h.translation && lang !== 'ar' && <p className="text-sm text-muted-foreground mt-2 italic">{h.translation}</p>}
                <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
                  <span>📌 {h.source}</span>
                  {h.narrator && <span>• {h.narrator}</span>}
                </div>
                <div className="mt-2 p-2 rounded-xl bg-amber-500/10 border border-amber-500/20">
                  <p className="text-xs font-bold text-amber-300">💡 {h.lesson}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Prophets */}
        {islamSubTab === 'prophets' && (
          <div className="space-y-3">
            {prophets.map(p => (
              <button key={p.id} onClick={() => setSelectedProphet(p)}
                className="w-full p-4 rounded-2xl bg-card/60 border border-white/10 text-start hover:border-purple-400/30 transition-all">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{p.emoji}</span>
                  <div className="flex-1">
                    <p className="font-bold">{p.name}</p>
                    <p className="text-xs text-purple-400">{p.title}</p>
                    <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{p.summary}</p>
                  </div>
                  <ChevronRight className="h-5 w-5 text-muted-foreground" />
                </div>
              </button>
            ))}
          </div>
        )}

        {/* Pillars */}
        {islamSubTab === 'pillars' && (
          <div className="space-y-3">
            {pillars.map(p => (
              <div key={p.id} className="p-4 rounded-2xl bg-card/60 border border-white/10">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center text-2xl shadow-lg">{p.emoji}</div>
                  <div className="flex-1">
                    <p className="font-bold">{p.number}. {p.title}</p>
                    <p className="text-sm text-muted-foreground mt-1">{p.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  // ═══════════════════ RENDER LIBRARY ═══════════════════
  const renderLibrary = () => {
    if (selectedLibItem) {
      return (
        <div className="space-y-4 pb-8">
          <button onClick={() => setSelectedLibItem(null)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-white">
            <ArrowLeft className="h-4 w-4" /> {isRTL ? 'العودة' : 'Back'}
          </button>
          <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-indigo-500/15 to-blue-500/10 border border-indigo-400/30">
            <span className="text-5xl">{selectedLibItem.emoji}</span>
            <h2 className="text-xl font-bold mt-2">{selectedLibItem.title}</h2>
            <p className="text-xs text-muted-foreground mt-1">{isRTL ? `الفئة العمرية: ${selectedLibItem.age_range}` : `Ages: ${selectedLibItem.age_range}`}</p>
          </div>
          <div className="p-4 rounded-2xl bg-card/60 border border-white/10">
            <p className="text-sm leading-relaxed whitespace-pre-line">{selectedLibItem.content}</p>
          </div>
          {selectedLibItem.lesson && (
            <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
              <p className="text-sm font-bold text-amber-300">💡 {selectedLibItem.lesson}</p>
            </div>
          )}
          {selectedLibItem.quran_ref && (
            <p className="text-xs text-muted-foreground text-center">📖 {selectedLibItem.quran_ref}</p>
          )}
        </div>
      );
    }

    return (
      <div className="space-y-4 pb-8">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-indigo-500/15 to-blue-500/10 border border-indigo-400/30">
          <span className="text-4xl">📚</span>
          <h2 className="text-lg font-bold mt-2">{isRTL ? 'المكتبة التعليمية' : 'Learning Library'}</h2>
          <p className="text-xs text-muted-foreground mt-1">{isRTL ? 'قصص وعلوم ومعارف للأطفال' : 'Stories, science & knowledge for kids'}</p>
        </div>

        {/* Categories */}
        <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
          <button onClick={() => { setSelectedCategory('all'); loadLibraryItems('all'); }}
            className={cn("px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap border transition-all",
              selectedCategory === 'all' ? "bg-indigo-500/20 border-indigo-400/40 text-indigo-300" : "bg-white/5 border-white/10 text-muted-foreground"
            )}>
            {isRTL ? 'الكل' : 'All'}
          </button>
          {libraryCategories.map(c => (
            <button key={c.id} onClick={() => { setSelectedCategory(c.id); loadLibraryItems(c.id); }}
              className={cn("flex items-center gap-1 px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap border transition-all",
                selectedCategory === c.id ? "bg-indigo-500/20 border-indigo-400/40 text-indigo-300" : "bg-white/5 border-white/10 text-muted-foreground"
              )}>
              <span>{c.emoji}</span> {c.title}
            </button>
          ))}
        </div>

        {/* Items */}
        <div className="space-y-3">
          {libraryItems.map(item => (
            <button key={item.id} onClick={() => setSelectedLibItem(item)}
              className="w-full p-4 rounded-2xl bg-card/60 border border-white/10 text-start hover:border-indigo-400/30 transition-all">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{item.emoji}</span>
                <div className="flex-1">
                  <p className="font-bold text-sm">{item.title}</p>
                  <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{item.content}</p>
                  <div className="flex gap-2 mt-1">
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300">{item.age_range}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-white/5 text-muted-foreground">{item.category.replace(/_/g, ' ')}</span>
                  </div>
                </div>
                <ChevronRight className="h-5 w-5 text-muted-foreground" />
              </div>
            </button>
          ))}
        </div>
      </div>
    );
  };

  // ═══════════════════ RENDER MAP (JOURNEY) ═══════════════════
  const renderMap = () => (
    <div className="space-y-4 pb-8">
      {/* Stats */}
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-lg shadow-lg shadow-amber-500/30">🌟</div>
          <div>
            <div className="flex items-center gap-1"><Zap className="h-3.5 w-3.5 text-amber-400" /><span className="text-sm font-bold">{xp} XP</span></div>
            <div className="w-20 h-1.5 bg-black/20 rounded-full"><div className="h-full rounded-full bg-gradient-to-r from-amber-400 to-amber-500" style={{ width: `${Math.min(100, xp % 100)}%` }} /></div>
          </div>
        </div>
        <div className="flex gap-2">
          <span className="flex items-center gap-1 px-2 py-1 rounded-full bg-orange-500/20 border border-orange-500/30 text-sm">🧱 <b className="text-orange-400">{bricks}</b></span>
          <span className="flex items-center gap-1 px-2 py-1 rounded-full bg-red-500/20 border border-red-500/30 text-sm"><Flame className="h-3.5 w-3.5 text-red-400" /><b className="text-red-400">{streak}</b></span>
        </div>
      </div>
      {mosque && (
        <div className="rounded-2xl bg-gradient-to-br from-indigo-500/10 to-violet-500/10 border border-indigo-500/20 p-3 flex items-center gap-3">
          <span className="text-3xl">{mosque.current_stage?.emoji || '🕌'}</span>
          <div className="flex-1">
            <p className="text-xs text-muted-foreground">{isRTL ? 'مسجدي' : 'My Mosque'}</p>
            <div className="h-2 bg-black/20 rounded-full mt-1"><div className="h-full rounded-full bg-gradient-to-r from-amber-400 to-orange-500 transition-all" style={{ width: `${mosque.progress_pct}%` }} /></div>
          </div>
          <span className="text-xs text-amber-400 font-bold">🧱 {bricks}</span>
        </div>
      )}
      {worlds.map(w => {
        const isOpen = expandedWorld === w.id;
        const hasCurrentStage = w.stages.some(s => s.is_current);
        return (
          <div key={w.id} className="rounded-3xl overflow-hidden border border-white/10 transition-all" style={{ borderColor: w.color + '30' }}>
            <button onClick={() => setExpandedWorld(isOpen ? null : w.id)}
              className="w-full p-4 flex items-center gap-3 transition-all" style={{ background: `linear-gradient(135deg, ${w.color}15, ${w.color}08)` }}>
              <span className="text-3xl">{w.emoji}</span>
              <div className="flex-1 text-start">
                <h3 className="font-bold text-base">{isRTL ? w.title_ar : w.title_en}</h3>
                <p className="text-[10px] text-muted-foreground">{isRTL ? w.description_ar : w.description_en}</p>
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex-1 h-1.5 bg-black/20 rounded-full"><div className="h-full rounded-full transition-all" style={{ width: `${(w.progress / w.total) * 100}%`, backgroundColor: w.color }} /></div>
                  <span className="text-[10px] font-bold" style={{ color: w.color }}>{w.progress}/{w.total}</span>
                </div>
              </div>
              {hasCurrentStage && !isOpen && <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-400 animate-pulse">{isRTL ? 'الآن' : 'NOW'}</span>}
              <ChevronDown className={cn("h-5 w-5 text-muted-foreground transition-transform", isOpen && "rotate-180")} />
            </button>
            {isOpen && (
              <div className="px-4 pb-5 pt-2">
                <div className="flex flex-wrap justify-center gap-x-4 gap-y-5">
                  {w.stages.map((s, i) => (
                    <div key={s.id} className="relative">
                      {i > 0 && <div className="absolute -top-4 left-1/2 w-0.5 h-4 bg-white/10" style={{ transform: 'translateX(-50%)' }} />}
                      <MapNode stage={s} isRTL={isRTL} onClick={() => s.unlocked && openStage(s.id)} />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );

  // ═══════════════════ RENDER STAGE ═══════════════════
  const renderStage = () => {
    if (!act) return null;
    return (
      <div className="space-y-4">
        {/* Progress dots */}
        <div className="flex items-center justify-center gap-2">
          {activities.map((a, i) => (
            <div key={i} className={cn("flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-bold transition-all border",
              i === activityIdx ? "bg-gradient-to-r from-amber-500/30 to-orange-500/30 border-amber-500/50 text-amber-300 scale-105" :
              i < activityIdx ? "bg-green-500/20 border-green-500/30 text-green-400" : "bg-white/5 border-white/10 text-muted-foreground"
            )}><span>{a.phase_emoji}</span><span>{a.phase_ar}</span>{i < activityIdx && <Check className="h-3 w-3" />}</div>
          ))}
        </div>
        {/* Noor bubble */}
        <div className="flex items-start gap-3 p-3 rounded-2xl bg-gradient-to-r from-violet-500/10 to-pink-500/10 border border-violet-500/20">
          <span className="text-3xl">🐣</span><p className="text-sm font-medium flex-1">{noorText}</p>
        </div>

        {/* INTRODUCE */}
        {act.phase === 'introduce' && (
          <div className="space-y-4">
            {act.content ? (
              <>
                <div className="space-y-3">
                  {act.content.map((item: any, i: number) => (
                    <div key={i} className={cn("p-4 rounded-2xl border-2 transition-all",
                      i === introStep ? "bg-gradient-to-br from-blue-500/15 to-cyan-500/10 border-blue-400/40 shadow-lg scale-[1.02]" : "bg-card/50 border-white/5 opacity-60"
                    )}>
                      <div className="flex items-center gap-4">
                        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-lg">
                          <span className="text-3xl font-bold text-white">{item.letter || item.ar || item.display || ''}</span>
                        </div>
                        <div className="flex-1">
                          <p className="text-lg font-bold">{item.name_ar || item.en || item.meaning || item.name_en || ''}</p>
                          <p className="text-sm text-muted-foreground">{item.transliteration || item.trans || item.sound || item.desc || ''}</p>
                          {item.example_word && <p className="text-xs text-blue-400 mt-0.5">{item.example_word} ({item.example_meaning})</p>}
                          {item.example && <p className="text-lg font-bold text-purple-400 mt-1" dir="rtl">{item.example}</p>}
                        </div>
                        <button onClick={() => speak(item.letter || item.ar || item.example_word || '', 'ar')} className="p-2 rounded-full bg-blue-500/20 text-blue-400"><Volume2 className="h-5 w-5" /></button>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="flex gap-2">
                  {introStep > 0 && <button onClick={() => setIntroStep(s => s - 1)} className="flex-1 py-3 rounded-2xl bg-white/10 font-bold">←</button>}
                  {introStep < (act.content.length - 1) ? (
                    <button onClick={() => setIntroStep(s => s + 1)} className="flex-1 py-3 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-bold shadow-lg">{isRTL ? 'التالي →' : 'Next →'}</button>
                  ) : (
                    <button onClick={goNextActivity} className="flex-1 py-3 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold shadow-lg flex items-center justify-center gap-2"><Check className="h-4 w-4" /> {isRTL ? 'فهمت! التالي' : 'Got it! Next'}</button>
                  )}
                </div>
              </>
            ) : act.ayahs ? (
              <div className="space-y-3">
                <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 border border-emerald-400/30"><p className="text-xs text-emerald-400 mb-1">📖 {act.surah_name}</p></div>
                {act.ayahs.map((a: any, i: number) => (
                  <button key={i} onClick={() => speak(a.text, 'ar')} className="w-full p-4 rounded-2xl bg-card/60 border border-white/10 text-start hover:border-emerald-400/30 transition-all">
                    <p className="text-xl font-bold font-arabic leading-loose" dir="rtl">{a.text}</p>
                    <p className="text-xs text-muted-foreground mt-1">{a.meaning}</p>
                    <Volume2 className="h-3.5 w-3.5 text-emerald-400 mt-1" />
                  </button>
                ))}
                <button onClick={goNextActivity} className="w-full py-3 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold shadow-lg flex items-center justify-center gap-2"><Check className="h-4 w-4" /> {isRTL ? 'فهمت! التالي' : 'Got it! Next'}</button>
              </div>
            ) : (
              <button onClick={goNextActivity} className="w-full py-3 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold shadow-lg">{isRTL ? 'التالي' : 'Next'}</button>
            )}
          </div>
        )}

        {/* RECOGNIZE */}
        {act.phase === 'recognize' && (
          <div className="space-y-4">
            {act.game_type === 'find_letter' && act.target && (
              <>
                <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-indigo-500/15 to-violet-500/10 border border-indigo-400/30">
                  <p className="text-xs text-indigo-300 mb-2">{isRTL ? 'جد هذا الحرف:' : 'Find this letter:'}</p>
                  <div className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center shadow-lg"><span className="text-4xl font-bold text-white">{act.target.letter}</span></div>
                  <p className="text-sm font-bold mt-2">{act.target.name_ar}</p>
                  <button onClick={() => speak(act.target.audio_hint, 'ar')} className="mt-2 inline-flex items-center gap-1 text-xs text-indigo-400"><Volume2 className="h-3 w-3" /> {act.target.audio_hint}</button>
                </div>
                <div className="grid gap-3 max-w-[240px] mx-auto" style={{ gridTemplateColumns: `repeat(${act.grid_size}, 1fr)` }}>
                  {act.grid.flat().map((cell: any, idx: number) => (
                    <button key={idx} onClick={() => {
                      if (cell.correct) { setCorrectFlash(true); setTimeout(() => { setCorrectFlash(false); goNextActivity(); }, 1200); speak(getNoorMessage('correct', locale)); }
                      else { setWrongFlash(true); setTimeout(() => setWrongFlash(false), 500); setStarsEarned(s => Math.max(1, s - 1)); }
                    }} className={cn("aspect-square rounded-2xl text-3xl font-bold flex items-center justify-center border-[3px] transition-all active:scale-90 shadow-lg",
                      correctFlash && cell.correct ? "bg-green-500/30 border-green-400 scale-110" : "bg-card/80 border-white/10 hover:border-indigo-400/50"
                    )}>{cell.letter}</button>
                  ))}
                </div>
              </>
            )}
            {(act.game_type === 'match_sound' || act.game_type === 'match_meaning') && act.pairs && (
              <>
                <p className="text-center text-sm font-bold text-emerald-400">{isRTL ? 'طابق كل زوج!' : 'Match each pair!'}</p>
                {act.pairs.map((p: any, i: number) => (
                  <button key={i} onClick={() => speak(p.display || p.answer, 'ar')} className="w-full p-4 rounded-2xl bg-card/60 border-2 border-white/10 flex items-center gap-4 hover:border-emerald-400/40 transition-all">
                    <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-emerald-500 to-green-500 flex items-center justify-center text-2xl font-bold text-white shadow-lg">{p.display}</div>
                    <div className="flex-1"><p className="text-sm font-bold">{p.answer}</p></div>
                    <Volume2 className="h-4 w-4 text-emerald-400" />
                  </button>
                ))}
                <button onClick={goNextActivity} className="w-full py-3 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold shadow-lg flex items-center justify-center gap-2"><Check className="h-4 w-4" /> {isRTL ? 'التالي' : 'Next'}</button>
              </>
            )}
            {(act.game_type === 'identify_rule' || act.game_type === 'order_ayahs') && (
              <>
                {act.example && (
                  <div className="text-center p-5 rounded-2xl bg-gradient-to-br from-purple-500/15 to-violet-500/10 border border-purple-400/30">
                    <p className="text-3xl font-bold font-arabic" dir="rtl">{act.example}</p>
                    {act.rule_name_ar && <p className="text-sm text-purple-300 mt-2">{act.rule_name_ar}</p>}
                  </div>
                )}
                {act.choices?.map((ch: string, i: number) => (
                  <button key={i} onClick={() => {
                    if (ch === act.correct) { setCorrectFlash(true); setTimeout(() => { setCorrectFlash(false); goNextActivity(); }, 1200); speak(getNoorMessage('correct', locale)); }
                    else { setWrongFlash(true); setTimeout(() => setWrongFlash(false), 500); setStarsEarned(s => Math.max(1, s - 1)); }
                  }} className="w-full p-4 rounded-2xl bg-card/60 border-2 border-white/10 flex items-center gap-3 hover:border-purple-400/40 transition-all active:scale-[0.97]">
                    <span className="w-9 h-9 rounded-xl bg-white/10 flex items-center justify-center font-bold text-sm">{String.fromCharCode(65+i)}</span>
                    <span className="font-medium capitalize">{ch.replace(/_/g, ' ')}</span>
                  </button>
                ))}
                {act.shuffled_ayahs && (
                  <>
                    <p className="text-center text-sm text-amber-400">{isRTL ? 'رتّب الآيات' : 'Order the ayahs'}</p>
                    {act.shuffled_ayahs.map((a: any, i: number) => (
                      <button key={i} onClick={() => speak(a.text, 'ar')} className="w-full p-3 rounded-2xl bg-card/60 border-2 border-white/10 text-start hover:border-amber-400/30 transition-all">
                        <p className="text-lg font-arabic font-bold" dir="rtl">{a.text}</p>
                      </button>
                    ))}
                    <button onClick={goNextActivity} className="w-full py-3 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold shadow-lg">{isRTL ? 'التالي' : 'Next'}</button>
                  </>
                )}
              </>
            )}
          </div>
        )}

        {/* SAY (PRONUNCIATION) */}
        {act.phase === 'say' && act.targets && (
          <div className="space-y-4">
            {act.targets.map((tgt: any, i: number) => (
              <div key={i} className={cn("p-4 rounded-2xl border-2 transition-all",
                sayDone.has(i) ? "bg-green-500/10 border-green-400/40 opacity-70" :
                i === sayIdx ? "bg-gradient-to-br from-pink-500/15 to-rose-500/10 border-pink-400/40 shadow-lg" : "bg-card/40 border-white/5 opacity-40"
              )}>
                <div className="flex items-center gap-3">
                  <div className={cn("w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-bold shadow-lg",
                    sayDone.has(i) ? "bg-green-500 text-white" : i === sayIdx ? "bg-gradient-to-br from-pink-500 to-rose-500 text-white" : "bg-muted text-muted-foreground"
                  )}>{sayDone.has(i) ? <Check className="h-6 w-6" /> : (tgt.letter || tgt.word?.charAt(0) || '')}</div>
                  <div className="flex-1">
                    <p className="text-lg font-bold font-arabic" dir="rtl">{tgt.word || tgt.letter}</p>
                    {tgt.transliteration && <p className="text-xs text-muted-foreground">{tgt.transliteration}</p>}
                  </div>
                  <button onClick={() => speak(tgt.word || tgt.letter, 'ar')} className="p-2 rounded-full bg-pink-500/20 text-pink-400"><Volume2 className="h-4 w-4" /></button>
                </div>
                {i === sayIdx && !sayDone.has(i) && (
                  <div className="mt-3 space-y-2">
                    <div className="h-12 rounded-xl bg-black/10 flex items-end justify-center gap-[2px] p-1 overflow-hidden">
                      {Array.from({ length: 24 }).map((_, j) => (
                        <div key={j} className={cn("w-1.5 rounded-full transition-all", accuracy > 70 ? "bg-green-400" : accuracy > 40 ? "bg-amber-400" : "bg-pink-400")}
                          style={{ height: listening ? `${20+Math.random()*70}%` : '15%', transition: listening ? 'height 0.15s' : 'height 0.5s' }} />
                      ))}
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => speak(tgt.word || tgt.letter, 'ar')} className="flex-1 py-2.5 rounded-xl bg-blue-500/20 text-blue-300 flex items-center justify-center gap-1 text-sm border border-blue-500/30"><Volume2 className="h-4 w-4" /> {isRTL ? 'استمع' : 'Listen'}</button>
                      <button onClick={listening ? () => { recRef.current?.stop(); setListening(false); } : () => startSpeech(tgt.word || tgt.letter)}
                        className={cn("flex-1 py-2.5 rounded-xl flex items-center justify-center gap-1 text-sm border",
                          listening ? "bg-red-500/20 text-red-400 border-red-500/30 animate-pulse" : "bg-pink-500/20 text-pink-300 border-pink-500/30"
                        )}>
                        {listening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                        {listening ? (isRTL ? 'أوقف' : 'Stop') : (isRTL ? 'انطق' : 'Speak')}
                      </button>
                    </div>
                    {spokenText && (
                      <div className={cn("p-3 rounded-xl border text-center", accuracy >= 70 ? "bg-green-500/10 border-green-400/40" : "bg-amber-500/10 border-amber-400/40")}>
                        <p className="text-lg font-bold">{spokenText}</p>
                        <div className="flex items-center justify-center gap-1 mt-1">
                          <Star className={cn("h-4 w-4", accuracy >= 70 ? "text-amber-400 fill-amber-400" : "text-muted-foreground")} /><span className="font-bold">{accuracy}%</span>
                          {accuracy >= 70 && <span className="text-green-400 text-xs">{isRTL ? 'ممتاز!' : 'Excellent!'}</span>}
                        </div>
                      </div>
                    )}
                    {spokenText && accuracy < 70 && (
                      <button onClick={() => { setSpokenText(''); setAccuracy(0); }} className="w-full py-2 rounded-xl bg-pink-500/20 text-pink-300 text-sm font-bold">{isRTL ? 'حاول مرة أخرى' : 'Try Again'}</button>
                    )}
                  </div>
                )}
              </div>
            ))}
            {sayDone.size >= act.targets.length && (
              <button onClick={goNextActivity} className="w-full py-3.5 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold shadow-lg flex items-center justify-center gap-2 animate-pulse">
                <Sparkles className="h-5 w-5" /> {activityIdx >= activities.length - 1 ? (isRTL ? 'أكمل المرحلة! 🎉' : 'Complete Stage! 🎉') : (isRTL ? 'التالي' : 'Next')}
              </button>
            )}
            {sayDone.size < act.targets.length && sayDone.has(sayIdx) && (
              <button onClick={() => { setSayIdx(prev => { for (let n = prev + 1; n < act.targets.length; n++) { if (!sayDone.has(n)) return n; } return prev; }); setSpokenText(''); setAccuracy(0); }}
                className="w-full py-3 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold shadow-lg">{isRTL ? 'التالي →' : 'Next →'}</button>
            )}
          </div>
        )}

        {/* BOSS */}
        {act.phase === 'boss' && (
          <div className="text-center space-y-4">
            <div className="text-6xl animate-bounce">🏆</div>
            <h2 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">{isRTL ? 'تحدي النهاية!' : 'Boss Challenge!'}</h2>
            <p className="text-sm text-muted-foreground">{isRTL ? 'اضغط لإنهاء التحدي' : 'Tap to finish'}</p>
            <button onClick={completeStage} className="w-full py-4 rounded-2xl bg-gradient-to-r from-purple-500 via-pink-500 to-red-500 text-white font-bold text-lg shadow-lg">{isRTL ? 'أكمل التحدي! 🏆' : 'Complete! 🏆'}</button>
          </div>
        )}
      </div>
    );
  };

  // ═══════════════════ RENDER RESULT ═══════════════════
  const renderResult = () => (
    <div className="text-center space-y-5 pt-4">
      <div className="text-7xl animate-bounce">🎉</div>
      <h2 className="text-2xl font-bold bg-gradient-to-r from-amber-300 to-orange-400 bg-clip-text text-transparent">{isRTL ? 'أحسنت! أكملت المرحلة!' : 'Stage Complete!'}</h2>
      <div className="flex justify-center gap-2">
        {[1,2,3].map(s => (<Star key={s} className={cn("h-10 w-10 transition-all", s <= starsEarned ? "text-amber-400 fill-amber-400 drop-shadow-lg" : "text-muted-foreground/30")} />))}
      </div>
      <div className="flex justify-center gap-4">
        <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30"><Zap className="h-7 w-7 text-amber-400 mx-auto" /><p className="text-xl font-bold text-amber-400 mt-1">+{stageResult?.xp_earned || 10}</p><p className="text-[10px] text-muted-foreground">XP</p></div>
        <div className="p-4 rounded-2xl bg-orange-500/10 border border-orange-500/30"><span className="text-2xl">🧱</span><p className="text-xl font-bold text-orange-400 mt-1">+{stageResult?.bricks_earned || 1}</p><p className="text-[10px] text-muted-foreground">{isRTL ? 'طوب' : 'Bricks'}</p></div>
      </div>
      <div className="flex gap-3 pt-2">
        {stageResult?.next_stage && (
          <button onClick={() => openStage(stageResult.next_stage)} className="flex-1 py-3.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold shadow-lg flex items-center justify-center gap-2">
            <ChevronRight className="h-5 w-5" /> {isRTL ? 'التالي' : 'Next'}
          </button>
        )}
        <button onClick={() => { setView('tabs'); loadJourney(); }} className="flex-1 py-3.5 rounded-2xl bg-white/10 border border-white/10 font-bold">{isRTL ? 'الخريطة' : 'Map'}</button>
      </div>
    </div>
  );

  return (
    <div dir={dir} className="min-h-screen bg-background pb-24">
      <Confetti on={confetti} />
      {wrongFlash && <div className="fixed inset-0 bg-red-500/15 z-50 pointer-events-none animate-pulse" />}
      {correctFlash && <div className="fixed inset-0 bg-green-500/15 z-50 pointer-events-none" />}
      
      {/* Header */}
      <div className="sticky top-0 z-30 bg-background/80 backdrop-blur-xl border-b border-white/5 px-4 py-3">
        <div className="flex items-center justify-between max-w-lg mx-auto">
          <button onClick={() => {
            if (view === 'stage') setView('tabs');
            else if (view === 'result') { setView('tabs'); loadJourney(); }
            else if (selectedSurah) setSelectedSurah(null);
            else if (selectedProphet) setSelectedProphet(null);
            else if (selectedLibItem) setSelectedLibItem(null);
            else nav(-1);
          }} className="p-2 rounded-full hover:bg-white/10"><ArrowLeft className="h-5 w-5" /></button>
          <h1 className="text-lg font-bold flex items-center gap-2">
            <span className="text-xl">{view === 'stage' ? activeStage?.world_emoji || '📚' : TAB_ICONS[mainTab]}</span>
            <span className="bg-gradient-to-r from-violet-400 to-pink-400 bg-clip-text text-transparent">
              {view === 'stage' ? (isRTL ? activeStage?.title_ar : activeStage?.title_en) : (TAB_LABELS[mainTab]?.[lang] || TAB_LABELS[mainTab]?.en || t('kidsZone'))}
            </span>
          </h1>
          <div className="w-10" />
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-2">
        {/* Tab bar - only show when not in stage/result view */}
        {view === 'tabs' && (
          <div className="flex gap-1.5 overflow-x-auto pb-3 scrollbar-hide mb-2">
            {(['lesson', 'quran', 'islam', 'library', 'journey'] as MainTab[]).map(tab => (
              <button key={tab} onClick={() => setMainTab(tab)}
                className={cn("flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap border transition-all shrink-0",
                  mainTab === tab
                    ? "bg-gradient-to-r from-violet-500/20 to-pink-500/20 border-violet-400/40 text-violet-300 shadow-lg shadow-violet-500/10"
                    : "bg-white/5 border-white/10 text-muted-foreground hover:bg-white/10"
                )}>
                <span>{TAB_ICONS[tab]}</span>
                <span>{TAB_LABELS[tab]?.[lang] || TAB_LABELS[tab]?.en}</span>
              </button>
            ))}
          </div>
        )}

        {/* Content */}
        {view === 'tabs' && mainTab === 'lesson' && renderDailyLesson()}
        {view === 'tabs' && mainTab === 'journey' && renderMap()}
        {view === 'tabs' && mainTab === 'quran' && renderQuran()}
        {view === 'tabs' && mainTab === 'islam' && renderIslam()}
        {view === 'tabs' && mainTab === 'library' && renderLibrary()}
        {view === 'stage' && renderStage()}
        {view === 'result' && renderResult()}
      </div>
    </div>
  );
}
