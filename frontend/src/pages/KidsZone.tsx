import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { useNoorTTS, getNoorMessage } from '@/components/NoorMascot';
import { Star, Mic, MicOff, Volume2, Sparkles, ArrowLeft, Zap, Check, X, ChevronRight, Flame, Lock, Crown, ChevronDown, BookOpen, Heart, GraduationCap, Calendar, Trophy, Play } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import SalahGuide from '@/components/SalahGuide';

const API = import.meta.env.REACT_APP_BACKEND_URL || '';

/* ═══════ TYPES ═══════ */
interface CurrStage { id:string; emoji:string; color:string; title:string; description:string; day_start:number; day_end:number; total_lessons:number; }
interface LessonSection { type:string; emoji:string; title:string; content:any; }
interface Lesson { day:number; stage:any; lesson_number_in_stage:number; total_in_stage:number; sections:LessonSection[]; title:any; total_sections:number; xp_reward:number; }
type MainTab = 'curriculum' | 'lesson' | 'quran' | 'islam' | 'library';
type IslamSub = 'duas' | 'hadiths' | 'prophets' | 'pillars' | 'wudu' | 'salah';

/* ═══════ TAB CONFIG ═══════ */
const TABS: {id:MainTab;emoji:string;key:string}[] = [
  {id:'quran',emoji:'📖',key:'quran'},
  {id:'islam',emoji:'🕌',key:'islam'},
  {id:'curriculum',emoji:'🎓',key:'curriculum'},
  {id:'lesson',emoji:'📅',key:'todaysLesson'},
  {id:'library',emoji:'📚',key:'learningLibrary'},
];

/* ═══════ CONFETTI ═══════ */
function Confetti({on}:{on:boolean}){
  if(!on)return null;
  return(<div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
    {Array.from({length:40}).map((_,i)=>(<div key={i} className="absolute animate-confetti-fall" style={{left:`${Math.random()*100}%`,top:'-10px',animationDelay:`${Math.random()*2}s`,animationDuration:`${2+Math.random()*3}s`}}>
      <span className="text-2xl">{['⭐','🌟','✨','🌙','🕌','💛','📖','🤲','🕋','☪️'][i%10]}</span></div>))}
  </div>);
}

/* ═══════ LOADING SPINNER ═══════ */
function LoadingSpinner({text}:{text?:string}){
  return(<div className="flex flex-col items-center justify-center py-12 gap-3">
    <div className="relative w-12 h-12">
      <div className="absolute inset-0 rounded-full border-2 border-[#D4AF37]/20"/>
      <div className="absolute inset-0 rounded-full border-2 border-t-[#D4AF37] animate-spin"/>
      <div className="absolute inset-2 rounded-full border-2 border-t-emerald-500 animate-spin" style={{animationDirection:'reverse',animationDuration:'0.8s'}}/>
    </div>
    {text && <p className="text-xs text-muted-foreground">{text}</p>}
  </div>);
}

/* ═══════ QUIZ SECTION WITH VISUAL FEEDBACK ═══════ */
function QuizSection({content:c, t, locale, speak}:{content:any; t:(k:string)=>string; locale:string; speak:(text:string,lang:string)=>void}){
  const [selected, setSelected] = React.useState<string|null>(null);
  const [answered, setAnswered] = React.useState(false);
  const handleAnswer = (opt:string) => {
    if(answered) return;
    setSelected(opt);
    setAnswered(true);
    if(opt===c.correct){
      toast.success(t('correctAnswer'));
      speak(getNoorMessage('correct',locale));
    } else {
      toast.error(t('tryAgain'));
      // Allow retry after 1.5s
      setTimeout(()=>{setSelected(null);setAnswered(false);},1500);
    }
  };
  return(<div className="space-y-2">
    <p className="text-sm font-bold text-center mb-3">{c.question}</p>
    <div className="grid grid-cols-2 gap-2">
      {c.options?.map((opt:string,i:number)=>{
        const isCorrect = answered && opt===c.correct;
        const isWrong = answered && opt===selected && opt!==c.correct;
        return(
        <button key={i} onClick={()=>handleAnswer(opt)} disabled={answered && opt===c.correct && selected===c.correct}
          className={cn("p-3 rounded-xl border-2 transition-all text-center active:scale-95",
            isCorrect ? "animate-quiz-correct bg-green-500/15 border-green-500/50" :
            isWrong ? "animate-quiz-wrong bg-red-500/12 border-red-500/50" :
            "bg-card/60 border-border/30 hover:border-amber-400/40"
          )}>
          <span className="text-2xl font-bold">{opt}</span>
          {isCorrect && <span className="block text-xs text-green-500 dark:text-green-400 font-bold mt-1">✓</span>}
          {isWrong && <span className="block text-xs text-red-500 font-bold mt-1">✗</span>}
        </button>);
      })}
    </div>
  </div>);
}

/* ═══════ SECTION CARD ═══════ */
function SectionCard({emoji,title,children,color="blue",done=false,onDone,doneLabel,completedLabel}:{emoji:string;title:string;children:React.ReactNode;color?:string;done?:boolean;onDone?:()=>void;doneLabel?:string;completedLabel?:string}){
  const colors:Record<string,string>={
    blue:"from-blue-500/15 to-cyan-500/10 border-blue-400/30",
    green:"from-emerald-500/15 to-teal-500/10 border-emerald-400/30",
    amber:"from-amber-500/15 to-orange-500/10 border-amber-400/30",
    purple:"from-purple-500/15 to-violet-500/10 border-purple-400/30",
    pink:"from-pink-500/15 to-rose-500/10 border-pink-400/30",
    indigo:"from-indigo-500/15 to-blue-500/10 border-indigo-400/30",
    teal:"from-teal-500/15 to-emerald-500/10 border-teal-400/30",
    red:"from-red-500/15 to-orange-500/10 border-red-400/30",
  };
  return(<div className={cn("rounded-2xl border p-4 bg-gradient-to-br transition-all",colors[color]||colors.blue,done&&"ring-2 ring-green-400/50")}>
    <div className="flex items-center gap-2 mb-3">
      <span className="text-xl">{emoji}</span>
      <h3 className="font-bold text-base flex-1 text-foreground">{title}</h3>
      {done && <span className="text-green-500 dark:text-green-400 text-xs font-bold flex items-center gap-1"><Check className="h-3 w-3"/>✓</span>}
    </div>
    {children}
    {onDone && !done && <button onClick={onDone} className="w-full mt-3 py-2 rounded-xl bg-muted/30 text-muted-foreground text-sm flex items-center justify-center gap-1 border border-border/30 hover:bg-white/20 transition-all"><Check className="h-3.5 w-3.5"/>{doneLabel || 'Done'}</button>}
    {done && <div className="mt-2 text-center text-xs text-green-500 dark:text-green-400 font-bold">{completedLabel || '✅ Completed!'}</div>}
  </div>);
}

/* ═══════ MAIN COMPONENT ═══════ */
export default function KidsZone() {
  const { t, dir, locale } = useLocale();
  const nav = useNavigate();
  const { speak } = useNoorTTS();
  const isRTL = dir === 'rtl';
  const lang = locale || 'ar';

  const [mainTab, setMainTab] = useState<MainTab>('quran');
  const [userId] = useState(() => localStorage.getItem('kids_user_id') || `kid_${Date.now()}`);
  const [confetti, setConfetti] = useState(false);
  const [showConsent, setShowConsent] = useState(false);
  const [consentChecked, setConsentChecked] = useState(false);
  const [lessonsToday, setLessonsToday] = useState(0);
  const [loading, setLoading] = useState<Record<string,boolean>>({});

  // Curriculum state
  const [stages, setStages] = useState<CurrStage[]>([]);
  const [currProgress, setCurrProgress] = useState<any>(null);
  const [expandedStage, setExpandedStage] = useState<string|null>(null);

  // Lesson state
  const [lesson, setLesson] = useState<Lesson|null>(null);
  const [lessonDay, setLessonDay] = useState(0);
  const [completedSections, setCompletedSections] = useState<Set<number>>(new Set());

  // Quran state
  const [surahs, setSurahs] = useState<any[]>([]);
  const [selectedSurah, setSelectedSurah] = useState<any>(null);

  // Islam state
  const [islamSub, setIslamSub] = useState<IslamSub>('salah');
  const [duas, setDuas] = useState<any[]>([]);
  const [hadiths, setHadiths] = useState<any[]>([]);
  const [prophets, setProphets] = useState<any[]>([]);
  const [pillars, setPillars] = useState<any[]>([]);
  const [wuduSteps, setWuduSteps] = useState<any[]>([]);
  const [salahSteps, setSalahSteps] = useState<any[]>([]);
  const [selectedProphet, setSelectedProphet] = useState<any>(null);

  // Library state
  const [libCats, setLibCats] = useState<any[]>([]);
  const [libItems, setLibItems] = useState<any[]>([]);
  const [selCat, setSelCat] = useState('all');
  const [selItem, setSelItem] = useState<any>(null);

  // Achievements
  const [badges, setBadges] = useState<any[]>([]);

  useEffect(() => { localStorage.setItem('kids_user_id', userId); }, [userId]);

  // ═══ PARENTAL CONSENT CHECK ═══
  useEffect(() => {
    const checkConsent = async () => {
      try {
        const r = await fetch(`${API}/api/parental-consent/check?user_id=${userId}`);
        const d = await r.json();
        if (d.success && d.has_consent) {
          setConsentChecked(true);
        } else {
          setShowConsent(true);
        }
      } catch {
        setConsentChecked(true);
      }
    };
    checkConsent();
  }, [userId]);

  const giveConsent = async () => {
    try {
      await fetch(`${API}/api/parental-consent/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, consent: true }),
      });
      setShowConsent(false);
      setConsentChecked(true);
      toast.success(t('parentalConsentAccepted'));
    } catch {
      toast.error(t('genericError'));
    }
  };

  // ═══ LESSON POINTS (MAX 5/DAY) ═══
  const awardLessonPoint = async () => {
    try {
      const r = await fetch(`${API}/api/points/lesson-complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, mode: 'kids', lesson_id: `day_${lessonDay}` }),
      });
      const d = await r.json();
      if (d.success) {
        setLessonsToday(d.lessons_today);
        toast.success(`${t('lessonPointEarned')} (${d.lessons_today}/5)`);
      } else if (d.message === 'daily_lesson_limit_reached') {
        setLessonsToday(5);
        toast.info(t('dailyLessonLimitReached'));
      }
    } catch {}
  };

  useEffect(() => {
    loadCurrProgress();
    loadBadges();
    if (mainTab === 'curriculum') loadCurriculum();
    if (mainTab === 'lesson') loadLesson();
    if (mainTab === 'quran') loadSurahs();
    if (mainTab === 'islam') loadIslamContent();
    if (mainTab === 'library') loadLibrary();
  }, [mainTab, locale]);

  // ═══ LOADERS ═══
  const setLoad = (key:string,v:boolean) => setLoading(p=>({...p,[key]:v}));
  const loadCurriculum = async () => {
    setLoad('curriculum',true);
    try { const r = await fetch(`${API}/api/kids-learn/curriculum?locale=${lang}`); const d = await r.json(); if(d.success) setStages(d.stages); } catch{ toast.error(t('genericError')); }
    setLoad('curriculum',false);
  };
  const loadCurrProgress = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/curriculum/progress?user_id=${userId}`); const d = await r.json(); if(d.success){ setCurrProgress(d.progress); if(!lessonDay) setLessonDay(d.progress.current_day||1); }} catch{}
  };
  const loadLesson = async (day?:number) => {
    const d = day || lessonDay || 1;
    setLoad('lesson',true);
    try { const r = await fetch(`${API}/api/kids-learn/curriculum/lesson/${d}?locale=${lang}`); const data = await r.json(); if(data.success){setLesson(data.lesson);setLessonDay(d);setCompletedSections(new Set());}} catch{ toast.error(t('genericError')); }
    setLoad('lesson',false);
  };
  const loadSurahs = async () => {
    setLoad('quran',true);
    try { const r = await fetch(`${API}/api/kids-learn/quran/surahs?locale=${lang}`); const d = await r.json(); if(d.success) setSurahs(d.surahs); } catch{ toast.error(t('genericError')); }
    setLoad('quran',false);
  };
  const loadIslamContent = async () => {
    setLoad('islam',true);
    try{const[d1,d2,d3,d4,d5,d6]=await Promise.all([
      fetch(`${API}/api/kids-learn/duas?locale=${lang}`).then(r=>r.json()),
      fetch(`${API}/api/kids-learn/hadiths?locale=${lang}`).then(r=>r.json()),
      fetch(`${API}/api/kids-learn/prophets-full?locale=${lang}`).then(r=>r.json()),
      fetch(`${API}/api/kids-learn/islamic-pillars?locale=${lang}`).then(r=>r.json()),
      fetch(`${API}/api/kids-learn/wudu?locale=${lang}`).then(r=>r.json()),
      fetch(`${API}/api/kids-learn/salah?locale=${lang}`).then(r=>r.json()),
    ]);
    if(d1.success)setDuas(d1.duas);if(d2.success)setHadiths(d2.hadiths);
    if(d3.success)setProphets(d3.prophets);if(d4.success)setPillars(d4.pillars);
    if(d5.success)setWuduSteps(d5.steps);if(d6.success)setSalahSteps(d6.steps);
    }catch{ toast.error(t('genericError')); }
    setLoad('islam',false);
  };
  const loadLibrary = async () => {
    setLoad('library',true);
    try{const[c,i]=await Promise.all([
      fetch(`${API}/api/kids-learn/library/categories?locale=${lang}`).then(r=>r.json()),
      fetch(`${API}/api/kids-learn/library/items?category=all&locale=${lang}`).then(r=>r.json()),
    ]);if(c.success)setLibCats(c.categories);if(i.success)setLibItems(i.items);}catch{ toast.error(t('genericError')); }
    setLoad('library',false);
  };
  const loadLibItems = async(cat:string) => {
    setLoad('libItems',true);
    try{const r=await fetch(`${API}/api/kids-learn/library/items?category=${cat}&locale=${lang}`);const d=await r.json();if(d.success)setLibItems(d.items);}catch{ toast.error(t('genericError')); }
    setLoad('libItems',false);
  };
  const loadBadges = async () => {
    try{const r=await fetch(`${API}/api/kids-learn/achievements?user_id=${userId}`);const d=await r.json();if(d.success)setBadges(d.badges);}catch{}
  };

  const markDone = (idx:number) => setCompletedSections(p => new Set([...p, idx]));

  const completeLesson = async () => {
    if(!lesson) return;
    try{
      await fetch(`${API}/api/kids-learn/curriculum/progress`,{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({user_id:userId,day:lesson.day,sections_done:completedSections.size,total_sections:lesson.total_sections,xp_reward:lesson.xp_reward})});
      setConfetti(true); setTimeout(()=>setConfetti(false),3000);
      toast.success(t('lessonCompleteCongrats'));
      loadCurrProgress(); loadBadges();
      // Award lesson point (max 5/day as in Flutter code)
      await awardLessonPoint();
    }catch{}
  };

  // ═══════ RENDER: CURRICULUM OVERVIEW ═══════
  const renderCurriculum = () => {
    const currentDay = currProgress?.current_day || 1;
    const completedDays = currProgress?.completed_days || [];
    const totalXp = currProgress?.total_xp || 0;
    const streak = currProgress?.streak || 0;

    return(<div className="space-y-4 pb-8">
      {loading.curriculum && <LoadingSpinner/>}
      {/* Hero Stats */}
      <div className="p-5 rounded-3xl bg-gradient-to-br from-violet-600/20 via-purple-500/15 to-pink-500/10 border border-violet-400/20">
        <div className="text-center mb-4">
          <span className="text-5xl">🎓</span>
          <h2 className="text-xl font-bold mt-2 bg-gradient-to-r from-violet-200 to-pink-200 bg-clip-text text-transparent">{t('completeCurriculum')}</h2>
          <p className="text-sm text-foreground/70 mt-1">{t('completeCurriculumDesc')}</p>
        </div>
        <div className="flex gap-3">
          <div className="flex-1 p-3 rounded-xl bg-muted/30 text-center">
            <Calendar className="h-5 w-5 text-blue-500 dark:text-blue-400 mx-auto"/>
            <p className="text-xl font-bold text-blue-200">{currentDay}</p>
            <p className="text-xs text-foreground/60">{t('currentLesson')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-muted/30 text-center">
            <Check className="h-5 w-5 text-green-500 dark:text-green-400 mx-auto"/>
            <p className="text-xl font-bold text-green-200">{completedDays.length}</p>
            <p className="text-xs text-foreground/60">{t('completedLabel')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-muted/30 text-center">
            <Flame className="h-5 w-5 text-orange-500 dark:text-orange-400 mx-auto"/>
            <p className="text-xl font-bold text-orange-200">{streak}</p>
            <p className="text-xs text-foreground/60">{t('streakSmall')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-muted/30 text-center">
            <Zap className="h-5 w-5 text-amber-500 dark:text-amber-400 mx-auto"/>
            <p className="text-xl font-bold text-amber-200">{totalXp}</p>
            <p className="text-xs text-foreground/60">{t('xpLabel') || 'XP'}</p>
          </div>
        </div>
        {/* Overall progress bar */}
        <div className="mt-4">
          <div className="flex justify-between text-sm text-foreground/70 mb-1">
            <span>{t('overallProgress')}</span>
            <span className="font-bold">{stages.length > 0 ? Math.round((completedDays.length / stages.reduce((a:number, s:CurrStage) => a + s.total_lessons, 0)) * 100) : 0}%</span>
          </div>
          <div className="h-3 bg-muted/40 rounded-full overflow-hidden">
            <div className="h-full rounded-full bg-gradient-to-r from-[hsl(var(--mystic-moss))] via-[hsl(var(--islamic-emerald))] to-[#D4AF37] transition-all" style={{width:`${stages.length > 0 ? (completedDays.length / stages.reduce((a:number, s:CurrStage) => a + s.total_lessons, 0)) * 100 : 0}%`}}/>
          </div>
        </div>
      </div>

      {/* Badges Preview */}
      {badges.length>0 && (<div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
        {badges.filter(b=>b.earned).map(b=>(<div key={b.id} className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 shrink-0">
          <span className="text-lg">{b.emoji}</span><span className="text-xs font-bold text-amber-600 dark:text-amber-300">{b[`title_${locale}`] || b.title_ar}</span>
        </div>))}
        {badges.filter(b=>!b.earned).slice(0,3).map(b=>(<div key={b.id} className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/5 border border-border/30 shrink-0 opacity-60">
          <span className="text-lg grayscale">{b.emoji}</span><span className="text-xs text-foreground/50">{b[`title_${locale}`] || b.title_ar}</span>
        </div>))}
      </div>)}

      {/* Quick Start */}
      <button onClick={()=>{setMainTab('lesson');loadLesson(currentDay);}} className="w-full p-4 rounded-[1.5rem] btn-islamic text-white font-bold text-base flex items-center justify-center gap-3">
        <Play className="h-5 w-5 fill-white"/>
        {t('startLessonN').replace('{n}', String(currentDay))}
      </button>

      {/* Stages */}
      {stages.map(s=>{
        const isOpen = expandedStage===s.id;
        const completed = completedDays.filter((d:number)=>d>=s.day_start&&d<=s.day_end).length;
        const pct = Math.round((completed/s.total_lessons)*100);
        const isCurrent = currentDay>=s.day_start && currentDay<=s.day_end;
        const isLocked = currentDay < s.day_start && completed===0;
        return(<div key={s.id} className={cn("rounded-[1.5rem] overflow-hidden border transition-all",isLocked?"opacity-70 border-border/20":"border-border/40")} style={{borderColor:!isLocked?s.color+'40':undefined}}>
          <button onClick={()=>!isLocked&&setExpandedStage(isOpen?null:s.id)} disabled={isLocked}
            className="w-full p-4 flex items-center gap-3" style={{background:`linear-gradient(135deg,${s.color}15,${s.color}08)`}}>
            <div className="w-14 h-14 rounded-[1rem] flex items-center justify-center text-2xl shadow-lg" style={{background:`linear-gradient(135deg,${s.color}30,${s.color}15)`}}>
              {isLocked?<Lock className="h-6 w-6 text-foreground/40"/>:<span>{s.emoji}</span>}
            </div>
            <div className="flex-1 text-start">
              <h3 className="font-bold text-base text-foreground">{s.title}</h3>
              <p className="text-xs text-foreground/60 mt-0.5">{t('nLessons').replace('{n}', String(s.total_lessons))} • {t('dayN').replace('{n}', `${s.day_start}-${s.day_end}`)}</p>
              <div className="flex items-center gap-2 mt-2">
                <div className="flex-1 h-2.5 bg-muted/40 rounded-full"><div className="h-full rounded-full transition-all" style={{width:`${pct}%`,backgroundColor:s.color}}/></div>
                <span className="text-xs font-bold min-w-[32px] text-end" style={{color:s.color}}>{pct}%</span>
              </div>
            </div>
            {isCurrent && <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-600 dark:text-amber-300 animate-pulse shrink-0">{t('nowLabel')}</span>}
            {pct===100 && <span className="text-green-500 dark:text-green-400"><Check className="h-6 w-6"/></span>}
            {!isLocked && <ChevronDown className={cn("h-5 w-5 text-foreground/50 transition-transform shrink-0",isOpen&&"rotate-180")}/>}
          </button>
          {isOpen && (<div className="px-4 pb-4 pt-1">
            <p className="text-sm text-foreground/60 mb-3">{s.description}</p>
            <div className="grid grid-cols-7 gap-1.5">
              {Array.from({length:Math.min(s.total_lessons,42)}).map((_,i)=>{
                const dayNum = s.day_start + i;
                const isDone = completedDays.includes(dayNum);
                const isCurr = dayNum===currentDay;
                return(<button key={i} onClick={()=>{setLessonDay(dayNum);setMainTab('lesson');loadLesson(dayNum);}}
                  className={cn("aspect-square rounded-lg text-xs font-bold flex items-center justify-center transition-all border",
                    isDone?"bg-green-500/20 border-green-500/30 text-green-600 dark:text-green-300":
                    isCurr?"bg-amber-500/20 border-amber-500/40 text-amber-600 dark:text-amber-300 animate-pulse":
                    dayNum<currentDay?"bg-white/10 border-border/30 text-foreground/60":
                    "bg-white/5 border-white/10 text-foreground/30"
                  )}>
                  {isDone?'✓':dayNum<=currentDay?i+1:<Lock className="h-3 w-3"/>}
                </button>);
              })}
            </div>
            {s.total_lessons>42 && <p className="text-xs text-foreground/50 text-center mt-2">+{s.total_lessons-42} {t('moreLessons').replace('{n}', String(s.total_lessons-42))}</p>}
          </div>)}
        </div>);
      })}
    </div>);
  };

  // ═══════ RENDER: STRUCTURED LESSON ═══════
  const renderLesson = () => {
    if(!lesson || loading.lesson) return <LoadingSpinner text={t('todaysLesson')}/>;
    const L=lesson;
    const sectionColors = ['green','blue','amber','purple','pink','indigo','teal','red'];
    return(<div className="space-y-4 pb-8">
      {/* Day nav */}
      <div className="flex items-center justify-between">
        <button onClick={()=>loadLesson(Math.max(1,L.day-1))} className="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 transition-all active:scale-90" aria-label={t('prevBtn')}>
          {isRTL ? <ChevronRight className="h-5 w-5"/> : <ArrowLeft className="h-5 w-5"/>}
        </button>
        <div className="text-center">
          <div className="flex items-center gap-2 justify-center">
            <span className="text-xl">{L.stage.emoji}</span>
            <span className="text-xs px-2 py-0.5 rounded-full font-bold" style={{background:L.stage.color+'20',color:L.stage.color}}>{L.stage.title}</span>
          </div>
          <p className="text-2xl font-bold text-gradient-islamic mt-1">{t('dayN').replace('{n}', String(L.day))}</p>
          <p className="text-xs text-foreground/50">{L.lesson_number_in_stage} / {L.total_in_stage}</p>
        </div>
        <button onClick={()=>loadLesson(Math.min(1000,L.day+1))} className="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 transition-all active:scale-90" aria-label={t('nextBtn')}>
          {isRTL ? <ArrowLeft className="h-5 w-5"/> : <ChevronRight className="h-5 w-5"/>}
        </button>
      </div>

      {/* Lesson Title */}
      <div className="p-4 rounded-[1.5rem] bg-gradient-to-r from-[hsl(var(--mystic-moss))]/10 to-[#D4AF37]/10 border border-[hsl(var(--mystic-moss))]/20 text-center">
        <span className="text-3xl">📚</span>
        <h2 className="text-lg font-bold mt-2">{L.title[locale] || L.title.ar || L.title.en}</h2>
        <p className="text-xs text-muted-foreground mt-1">⭐ {L.xp_reward} {t('xpLabel') || 'XP'}</p>
      </div>

      {/* Progress */}
      <div className="flex items-center gap-2">
        <div className="flex-1 h-2 bg-muted/30 rounded-full"><div className="h-full rounded-full bg-gradient-to-r from-green-400 to-emerald-500 transition-all" style={{width:`${(completedSections.size/L.total_sections)*100}%`}}/></div>
        <span className="text-xs font-bold text-green-500 dark:text-green-400">{completedSections.size}/{L.total_sections}</span>
      </div>

      {/* Sections */}
      {L.sections.map((sec,idx)=>{
        const isDone = completedSections.has(idx);
        const color = sectionColors[idx%sectionColors.length];
        return(<SectionCard key={idx} emoji={sec.emoji} title={sec.title} color={color} done={isDone} onDone={()=>markDone(idx)} doneLabel={t('doneBtn')} completedLabel={t('completedMsg')}>
          {renderSectionContent(sec)}
        </SectionCard>);
      })}

      {/* Complete Button */}
      {completedSections.size >= Math.ceil(L.total_sections * 0.5) && (
        <button onClick={completeLesson} className="w-full py-4 rounded-2xl bg-gradient-to-r from-emerald-500 to-green-500 text-white font-bold text-lg shadow-lg shadow-emerald-500/30 flex items-center justify-center gap-2 hover:scale-[1.02] transition-all">
          <Sparkles className="h-5 w-5"/> {t('completeDayN').replace('{n}', String(L.day))}
        </button>
      )}

      {/* Next / Previous Lesson Navigation */}
      <div className="flex gap-3 pt-2">
        {L.day > 1 && (
          <button onClick={()=>loadLesson(L.day-1)} className="flex-1 py-3 rounded-2xl bg-muted/30 hover:bg-muted/50 text-foreground font-bold text-sm flex items-center justify-center gap-2 transition-all active:scale-95">
            {isRTL ? <ChevronRight className="h-4 w-4"/> : <ArrowLeft className="h-4 w-4"/>}
            {t('prevLessonBtn')}
          </button>
        )}
        {L.day < 1000 && (
          <button onClick={()=>loadLesson(L.day+1)} className="flex-1 py-3 rounded-2xl bg-gradient-to-r from-blue-500 to-indigo-500 text-white font-bold text-sm shadow-lg shadow-blue-500/20 flex items-center justify-center gap-2 hover:scale-[1.02] transition-all active:scale-95">
            {t('nextLessonBtn')}
            {isRTL ? <ArrowLeft className="h-4 w-4"/> : <ChevronRight className="h-4 w-4"/>}
          </button>
        )}
      </div>
    </div>);
  };

  const renderSectionContent = (sec:LessonSection) => {
    const c = sec.content;
    if(!c) return null;

    switch(sec.type){
      case 'learn':
        return(<div className="space-y-2">
          {c.letter && <div className="text-center">
            <button onClick={()=>speak(c.letter,'ar')} className="inline-block">
              <div className="w-24 h-24 mx-auto rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-lg hover:scale-105 transition-all">
                <span className="text-5xl font-bold text-foreground">{c.letter}</span>
              </div>
            </button>
            <p className="text-lg font-bold mt-2">{c.name_ar} ({c.name})</p>
            <p className="text-sm text-muted-foreground">{t('soundLabel')} {c.sound}</p>
            {c.example_word && <div className="mt-2 p-3 rounded-xl bg-muted/20">
              <p className="text-2xl font-bold font-arabic" dir="rtl">{c.example_word}</p>
              <p className="text-sm text-muted-foreground">{c.example_emoji} {c.example_translated}</p>
            </div>}
          </div>}
          {c.letters && <div className="space-y-3">{c.letters.map((lt:any,i:number)=>(
            <div key={i} className="p-3 rounded-xl bg-muted/20 flex items-center gap-4">
              <span className="text-3xl font-bold">{lt.letter}</span>
              <div className="flex gap-2">{lt.forms?.map((f:string,j:number)=><span key={j} className="px-3 py-1 rounded-lg bg-white/10 text-lg font-bold">{f}</span>)}</div>
              <span className="text-xs text-muted-foreground ms-auto">{lt.name}</span>
            </div>
          ))}</div>}
          {c.arabic && !c.letter && <div className="text-center">
            <button onClick={()=>speak(c.arabic,'ar')}>
              <p className="text-2xl font-bold font-arabic leading-loose" dir="rtl">{c.arabic}</p>
            </button>
            {c.translated && <p className="text-sm text-muted-foreground mt-2">{c.translated}</p>}
            {c.emoji && <span className="text-4xl block mt-2">{c.emoji}</span>}
          </div>}
          {c.name_ar && !c.letter && <div className="text-center">
            <p className="text-3xl font-bold">{c.symbol||''}</p>
            <p className="text-lg font-bold">{c.name_ar} ({c.name})</p>
            <p className="text-sm text-muted-foreground">{t('soundLabel')} {c.sound}</p>
            {c.example_word && <p className="text-2xl font-bold mt-2 font-arabic" dir="rtl">{c.example_word}</p>}
            {c.meaning && <p className="text-sm text-muted-foreground">{c.meaning}</p>}
          </div>}
          {c.number!==undefined && <div className="text-center">
            <span className="text-6xl font-bold">{c.display}</span>
            <p className="text-2xl font-bold mt-2">{c.arabic}</p>
            <p className="text-sm text-muted-foreground">{c.translated}</p>
          </div>}
        </div>);

      case 'listen':
        return(<div className="text-center space-y-3">
          <button onClick={()=>speak(c.text,'ar')} className="w-full p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 hover:bg-blue-500/20 transition-all flex items-center justify-center gap-2">
            <Volume2 className="h-5 w-5 text-blue-500 dark:text-blue-400"/>
            <span className="text-2xl font-bold font-arabic" dir="rtl">{c.text}</span>
          </button>
          {c.word && <button onClick={()=>speak(c.word,'ar')} className="w-full p-3 rounded-xl bg-purple-500/10 border border-purple-500/20 hover:bg-purple-500/20 transition-all flex items-center justify-center gap-2">
            <Volume2 className="h-4 w-4 text-purple-500 dark:text-purple-400"/>
            <span className="text-xl font-bold font-arabic" dir="rtl">{c.word}</span>
          </button>}
          {c.tip && <p className="text-xs text-muted-foreground">{c.tip}</p>}
        </div>);

      case 'quiz':
        return(<QuizSection content={c} t={t} locale={locale} speak={speak}/>);

      case 'write':
      case 'connect':
        return(<div className="text-center space-y-2">
          {c.letter && <span className="text-5xl font-bold">{c.letter}</span>}
          {c.word && <p className="text-2xl font-bold font-arabic" dir="rtl">{c.word}</p>}
          {c.word_translated && <p className="text-sm text-muted-foreground">{c.word_translated}</p>}
          {c.sentence && <p className="text-xl font-bold font-arabic" dir="rtl">{c.sentence}</p>}
          {c.tip && <p className="text-xs text-muted-foreground mt-2">{c.tip}</p>}
        </div>);

      case 'practice':
        return(<div className="space-y-2">
          {c.items && <div className="flex flex-wrap gap-2 justify-center">{c.items.map((it:string,i:number)=>(
            <button key={i} onClick={()=>speak(it,'ar')} className="px-4 py-2 rounded-xl bg-card/60 border border-border/30 text-xl font-bold hover:border-amber-400/30 transition-all">{it}</button>
          ))}</div>}
          {c.tip && <p className="text-xs text-muted-foreground text-center">{c.tip}</p>}
        </div>);

      case 'memorize':
        return(<div className="text-center space-y-2">
          {c.text && <button onClick={()=>speak(c.text,'ar')}><p className="text-xl font-bold font-arabic leading-loose" dir="rtl">{c.text}</p></button>}
          {c.tip && <p className="text-xs text-muted-foreground">{c.tip}</p>}
        </div>);

      case 'quran':
        return(<div className="text-center space-y-2">
          <p className="text-xs text-emerald-500 dark:text-emerald-400">{c.surah} - {t('ayahSingle')} {c.ayah_num}</p>
          <button onClick={()=>speak(c.arabic,'ar')}>
            <p className="text-2xl font-bold font-arabic leading-loose py-2" dir="rtl">{c.arabic}</p>
          </button>
          <p className="text-sm text-muted-foreground italic">{c.translation}</p>
        </div>);

      case 'dua':
        return(<div className="space-y-2">
          <button onClick={()=>speak(c.arabic,'ar')} className="w-full text-start">
            <p className="text-xl font-bold font-arabic leading-relaxed" dir="rtl">{c.arabic}</p>
          </button>
          {c.transliteration && <p className="text-xs italic text-blue-600 dark:text-blue-600/60 dark:text-blue-300/60">{c.transliteration}</p>}
          {c.meaning && <p className="text-sm text-muted-foreground">{c.meaning}</p>}
        </div>);

      case 'hadith':
        return(<div className="space-y-2">
          <p className="text-lg font-bold font-arabic leading-relaxed" dir="rtl">{c.arabic}</p>
          {c.translation && <p className="text-sm text-muted-foreground italic">{c.translation}</p>}
          <p className="text-xs text-amber-500 dark:text-amber-400/70">📌 {c.source}</p>
          <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/20"><p className="text-xs font-bold text-amber-600 dark:text-amber-300">💡 {c.lesson}</p></div>
        </div>);

      case 'story':
        return(<div className="space-y-2">
          <p className="text-lg font-bold">{c.name}</p>
          <p className="text-xs" style={{color:lesson?.stage.color}}>{c.title}</p>
          <p className="text-sm leading-relaxed">{c.summary}</p>
          <div className="p-2 rounded-xl bg-purple-500/10 border border-purple-500/20"><p className="text-xs font-bold text-purple-600 dark:text-purple-300">💡 {c.lesson}</p></div>
          <p className="text-xs text-muted-foreground">📖 {c.quran_ref}</p>
        </div>);

      case 'review':
        return(<div className="text-center space-y-2">
          {c.items && <div className="space-y-2">{c.items.map((it:any,i:number)=>(
            <div key={i} className="p-2 rounded-lg bg-card/40 flex items-center gap-3">
              <span className="text-2xl font-bold">{it.symbol||''}</span>
              <span className="text-sm font-bold">{it.name}</span>
              <span className="text-xs text-muted-foreground ms-auto">{it.sound}</span>
            </div>
          ))}</div>}
          {c.tip && <p className="text-sm text-muted-foreground">{c.tip}</p>}
          <span className="text-4xl">🔄</span>
        </div>);

      case 'read':
        return(<div className="text-center space-y-2">
          <button onClick={()=>speak(c.arabic,'ar')} className="inline-block">
            <p className="text-3xl font-bold font-arabic" dir="rtl">{c.arabic}</p>
          </button>
          <p className="text-sm text-muted-foreground">{c.emoji} {c.translated}</p>
        </div>);

      case 'reflect':
      case 'grammar':
        return(<div className="text-center"><p className="text-sm text-muted-foreground">{c.tip}</p></div>);

      default:
        return(<div className="text-center text-sm text-muted-foreground">{c.tip||c.text||JSON.stringify(c).slice(0,100)}</div>);
    }
  };

  // ═══════ RENDER: QURAN ═══════
  const renderQuran = () => {
    if(loading.quran) return <LoadingSpinner/>;
    if(selectedSurah) return(<div className="space-y-4 pb-8">
      <button onClick={()=>setSelectedSurah(null)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"><ArrowLeft className="h-4 w-4"/>{t('returnBack')}</button>
      <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 border border-emerald-400/30">
        <p className="text-3xl font-bold font-arabic">{selectedSurah.name_ar}</p>
        <p className="text-sm text-emerald-500 dark:text-emerald-400 mt-1">{selectedSurah.name_en} - {selectedSurah.total_ayahs} {t('ayahPlural')}</p>
      </div>
      {selectedSurah.ayahs?.map((a:any,i:number)=>(
        <div key={i} className="w-full p-4 rounded-2xl bg-card/60 border border-border/30 hover:border-emerald-400/30 transition-all">
          <button onClick={()=>speak(a.arabic,'ar')} className="w-full text-start">
            <div className="flex items-start gap-3">
              <span className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-xs font-bold text-emerald-500 dark:text-emerald-400 shrink-0">{a.number}</span>
              <div className="flex-1">
                <p className="text-xl font-bold font-arabic leading-loose" dir="rtl">{a.arabic}</p>
                {a.translation && <p className="text-sm text-foreground/60 mt-2">{a.translation}</p>}
              </div>
              <Volume2 className="h-4 w-4 text-emerald-500 dark:text-emerald-400 shrink-0 mt-2"/>
            </div>
          </button>
          {a.tafsir_kids && (
            <div className="mt-3 ms-11 p-3 rounded-xl bg-amber-500/10 border border-amber-400/20">
              <p className="text-[10px] font-bold text-amber-600 dark:text-amber-400 mb-1">💡 {t('kidsTafsirLabel') || 'تفسير مبسّط للأطفال'}</p>
              <p className="text-xs text-foreground/70 leading-relaxed">{a.tafsir_kids}</p>
            </div>
          )}
        </div>
      ))}
    </div>);

    return(<div className="space-y-4 pb-8">
      <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 border border-emerald-400/30">
        <span className="text-4xl">📖</span>
        <h2 className="text-lg font-bold mt-2">{t('quranMemTitle')}</h2>
        <p className="text-sm text-foreground/60 mt-1">{t('shortSurahsWithTranslation')}</p>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {surahs.map(s=>(<button key={s.id} onClick={()=>setSelectedSurah(s)} className="p-4 rounded-2xl bg-card/60 border border-border/30 hover:border-emerald-400/30 transition-all text-start">
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-xs font-bold text-emerald-500 dark:text-emerald-400">{s.number}</span>
            <div><p className="font-bold text-base font-arabic">{s.name_ar}</p><p className="text-xs text-foreground/60">{s.name_en}</p></div>
          </div>
          <p className="text-xs text-foreground/50 mt-2">{s.total_ayahs} {t('ayahPlural')}</p>
        </button>))}
      </div>
    </div>);
  };

  // ═══════ RENDER: ISLAM ═══════
  const renderIslam = () => {
    if(loading.islam) return <LoadingSpinner/>;
    if(selectedProphet) return(<div className="space-y-4 pb-8">
      <button onClick={()=>setSelectedProphet(null)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"><ArrowLeft className="h-4 w-4"/>{t('returnBack')}</button>
      <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-purple-500/15 to-violet-500/10 border border-purple-400/30">
        <span className="text-5xl">{selectedProphet.emoji}</span><h2 className="text-xl font-bold mt-2">{selectedProphet.name}</h2>
        <p className="text-sm text-purple-500 dark:text-purple-400">{selectedProphet.title}</p>
      </div>
      <div className="p-4 rounded-2xl bg-card/60 border border-border/30"><p className="text-sm leading-relaxed">{selectedProphet.summary}</p></div>
      <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20"><p className="text-sm font-bold text-purple-600 dark:text-purple-300">💡 {selectedProphet.lesson}</p></div>
      <p className="text-xs text-muted-foreground text-center">📖 {selectedProphet.quran_ref}</p>
    </div>);

    const subs:{id:IslamSub;label:string;emoji:string;count:number}[] = [
      {id:'salah',label:t('salahTab'),emoji:'🕌',count:salahSteps.length},
      {id:'wudu',label:t('wuduTab'),emoji:'💧',count:wuduSteps.length},
      {id:'pillars',label:t('pillarsTab'),emoji:'🕋',count:pillars.length},
      {id:'prophets',label:t('prophetsTab'),emoji:'📿',count:prophets.length},
      {id:'duas',label:t('duasTab'),emoji:'🤲',count:duas.length},
      {id:'hadiths',label:t('hadithsTab'),emoji:'📜',count:hadiths.length},
    ];

    return(<div className="space-y-4 pb-8">
      <div className="flex gap-1.5 overflow-x-auto pb-1 scrollbar-hide">
        {subs.map(st=>(<button key={st.id} onClick={()=>setIslamSub(st.id)} className={cn("flex items-center gap-1 px-2.5 py-1.5 rounded-[1rem] text-xs font-bold whitespace-nowrap border transition-all shrink-0",
          islamSub===st.id?"bg-gradient-to-r from-[hsl(var(--mystic-moss))]/15 to-[hsl(var(--islamic-emerald))]/10 border-[hsl(var(--mystic-moss))]/30 text-[hsl(var(--mystic-moss))] dark:from-[#D4AF37]/15 dark:to-[#D4AF37]/10 dark:border-[#D4AF37]/30 dark:text-[#D4AF37]":"bg-muted/20 border-border/30 text-muted-foreground")}>
          <span>{st.emoji}</span>{st.label}<span className="text-xs opacity-60">({st.count})</span>
        </button>))}
      </div>

      {islamSub==='duas' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-blue-500/15 to-indigo-500/10 border border-blue-400/30">
          <span className="text-4xl">🤲</span>
          <h3 className="font-bold mt-2 text-lg">{t('dailyDuasTitle')}</h3>
          <p className="text-sm text-foreground/60 mt-1">{t('dailyDuasVerse')}</p>
        </div>
        {duas.map(d=>(<button key={d.id} onClick={()=>speak(d.arabic,'ar')} className="w-full p-4 rounded-2xl bg-gradient-to-r from-blue-500/10 to-indigo-500/5 border border-blue-500/20 text-start hover:border-blue-400/40 transition-all">
          <div className="flex items-center gap-2 mb-2"><span>{d.emoji}</span><span className="text-xs font-bold text-blue-600 dark:text-blue-300">{d.title}</span><Volume2 className="h-3 w-3 text-blue-400 ms-auto"/></div>
          <p className="text-lg font-bold font-arabic leading-relaxed" dir="rtl">{d.arabic}</p>
          {d.transliteration && <p className="text-xs text-blue-600 dark:text-blue-600/70 dark:text-blue-300/70 mt-1 italic">{d.transliteration}</p>}
          {d.meaning && <p className="text-sm text-foreground/60 mt-1">{d.meaning}</p>}
        </button>))}
      </div>)}

      {islamSub==='hadiths' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-amber-500/15 to-orange-500/10 border border-amber-400/30">
          <span className="text-4xl">📜</span>
          <h3 className="font-bold mt-2 text-lg">{t('propheticHadithsTitle')}</h3>
          <p className="text-sm text-foreground/60 mt-1">{t('propheticHadithsSubtitle')}</p>
        </div>
        {hadiths.map(h=>(<div key={h.id} className="p-4 rounded-2xl bg-gradient-to-r from-amber-500/10 to-orange-500/5 border border-amber-500/20">
          <div className="flex items-center gap-2 mb-2"><span className="text-xl">{h.emoji}</span><span className="text-xs font-bold text-amber-600 dark:text-amber-300 capitalize">{h.category}</span></div>
          <p className="text-lg font-bold font-arabic leading-relaxed" dir="rtl">{h.arabic}</p>
          {h.translation && lang!=='ar' && <p className="text-sm text-foreground/60 mt-2 italic">{h.translation}</p>}
          <p className="text-xs text-foreground/50 mt-2">📌 {h.source}</p>
          <div className="mt-2 p-2 rounded-xl bg-amber-500/10 border border-amber-500/20"><p className="text-xs font-bold text-amber-600 dark:text-amber-300">💡 {h.lesson}</p></div>
        </div>))}
      </div>)}

      {islamSub==='prophets' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-purple-500/15 to-violet-500/10 border border-purple-400/30">
          <span className="text-4xl">📿</span>
          <h3 className="font-bold mt-2 text-lg">{t('prophetsStoriesTitle')}</h3>
          <p className="text-sm text-foreground/60 mt-1">{t('prophetsStoriesVerse')}</p>
        </div>
        {prophets.map(p=>(<button key={p.id} onClick={()=>setSelectedProphet(p)} className="w-full p-4 rounded-2xl bg-gradient-to-r from-purple-500/10 to-violet-500/5 border border-purple-500/20 text-start hover:border-purple-400/40 transition-all">
          <div className="flex items-center gap-3"><span className="text-3xl">{p.emoji}</span>
            <div className="flex-1"><p className="font-bold text-purple-600 dark:text-purple-300">{p.number}. {p.name}</p><p className="text-xs text-purple-400/70">{p.title}</p></div>
            <ChevronRight className="h-5 w-5 text-muted-foreground"/>
          </div>
        </button>))}
      </div>)}

      {islamSub==='pillars' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 border border-emerald-400/30">
          <span className="text-4xl">🕋</span>
          <h3 className="font-bold mt-2 text-lg">{t('fivePillarsTitle')}</h3>
          <p className="text-sm text-foreground/60 mt-1">{t('fivePillarsSubtitle')}</p>
        </div>
        {pillars.map(p=>(<div key={p.id} className="p-4 rounded-2xl bg-gradient-to-r from-emerald-500/10 to-teal-500/5 border border-emerald-500/20">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center text-2xl shadow-lg shadow-emerald-500/20">{p.emoji}</div>
          <div className="flex-1"><p className="font-bold text-emerald-600 dark:text-emerald-300">{p.number}. {p.title}</p><p className="text-sm text-foreground/60 mt-1 leading-relaxed">{p.description}</p></div>
        </div>
      </div>))}
      </div>)}

      {islamSub==='wudu' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-blue-500/15 to-cyan-500/10 border border-blue-400/30">
          <span className="text-4xl">💧</span>
          <h3 className="font-bold mt-2 text-lg">{t('wuduStepsTitle')}</h3>
          <p className="text-sm text-foreground/60 mt-1">{t('wuduSubtitle')}</p>
        </div>
        {wuduSteps.map((s:any)=>(<div key={s.step} className="p-3 rounded-xl bg-gradient-to-r from-blue-500/10 to-cyan-500/5 border border-blue-500/20 flex items-start gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-sm font-bold text-white shrink-0 shadow-lg shadow-blue-500/20">{s.step}</div>
          <div className="flex-1">
            <p className="font-bold text-sm text-blue-600 dark:text-blue-300">{s.emoji} {s.title}</p>
            <p className="text-xs text-foreground/50 mt-1 leading-relaxed">{s.description}</p>
          </div>
        </div>))}
        <div className="text-center p-3 rounded-xl bg-white/5 border border-border/30">
          <p className="text-xs text-foreground/50">{t('wuduReference')}</p>
        </div>
      </div>)}

      {islamSub==='salah' && (<SalahGuide steps={salahSteps} />)}
    </div>);
  };

  // ═══════ RENDER: LIBRARY ═══════
  const renderLibrary = () => {
    if(loading.library) return <LoadingSpinner/>;
    if(selItem) return(<div className="space-y-4 pb-8">
      <button onClick={()=>setSelItem(null)} className="flex items-center gap-2 text-sm text-foreground/60 hover:text-foreground"><ArrowLeft className="h-4 w-4"/>{t('returnBack')}</button>
      <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-indigo-500/15 to-blue-500/10 border border-indigo-400/30">
        <span className="text-5xl">{selItem.emoji}</span><h2 className="text-xl font-bold mt-2">{selItem.title}</h2>
        <p className="text-sm text-foreground/60 mt-1">{selItem.age_range}</p>
      </div>
      <div className="p-4 rounded-2xl bg-card/60 border border-border/30"><p className="text-sm leading-relaxed whitespace-pre-line">{selItem.content}</p></div>
      {selItem.lesson && <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20"><p className="text-sm font-bold text-amber-600 dark:text-amber-300">💡 {selItem.lesson}</p></div>}
    </div>);

    return(<div className="space-y-4 pb-8">
      <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-indigo-500/15 to-blue-500/10 border border-indigo-400/30">
        <span className="text-4xl">📚</span><h2 className="text-lg font-bold mt-2">{t('learningLibraryTitle')}</h2>
      </div>
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
        <button onClick={()=>{setSelCat('all');loadLibItems('all');}} className={cn("px-3 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap border transition-all shrink-0",selCat==='all'?"bg-indigo-500/20 border-indigo-400/40 text-indigo-600 dark:text-indigo-300":"bg-white/5 border-border/30 text-muted-foreground")}>{t('allFilter')}</button>
        {libCats.map(c=>(<button key={c.id} onClick={()=>{setSelCat(c.id);loadLibItems(c.id);}} className={cn("flex items-center gap-1 px-3 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap border transition-all shrink-0",selCat===c.id?"bg-indigo-500/20 border-indigo-400/40 text-indigo-600 dark:text-indigo-300":"bg-white/5 border-border/30 text-muted-foreground")}>
          <span>{c.emoji}</span>{c.title}
        </button>))}
      </div>
      {libItems.map(item=>(<button key={item.id} onClick={()=>setSelItem(item)} className="w-full p-4 rounded-2xl bg-card/60 border border-border/30 text-start hover:border-indigo-400/30 transition-all">
        <div className="flex items-center gap-3"><span className="text-3xl">{item.emoji}</span>
          <div className="flex-1"><p className="font-bold text-base text-foreground">{item.title}</p><p className="text-sm text-foreground/60 mt-1 line-clamp-2">{item.content}</p></div>
          <ChevronRight className="h-5 w-5 text-foreground/40"/>
        </div>
      </button>))}
    </div>);
  };

  // ═══════ MAIN RENDER ═══════
  return(<div dir={dir} className="min-h-screen bg-background pb-24">
    <Confetti on={confetti}/>

    {/* ═══ PARENTAL CONSENT DIALOG ═══ */}
    {showConsent && (
      <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
        <div className="w-full max-w-sm rounded-3xl bg-card border border-border p-6 space-y-5 shadow-2xl">
          <div className="text-center">
            <div className="w-16 h-16 rounded-full bg-amber-500/20 flex items-center justify-center mx-auto mb-3">
              <Lock className="h-8 w-8 text-amber-500" />
            </div>
            <h2 className="text-lg font-bold text-foreground">
              {t('parentalConsentTitle')}
            </h2>
            <p className="text-sm text-muted-foreground mt-2 leading-relaxed">
              {t('parentalConsentDesc')}
            </p>
          </div>
          <div className="space-y-2">
            <button
              onClick={giveConsent}
              className="w-full py-3.5 rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold text-sm hover:opacity-90 transition-all flex items-center justify-center gap-2"
            >
              <Check className="h-4 w-4" />
              {t('parentalConsentApprove')}
            </button>
            <button
              onClick={() => { setShowConsent(false); nav(-1); }}
              className="w-full py-3 rounded-2xl bg-muted/50 text-muted-foreground font-medium text-sm hover:bg-muted/70 transition-all"
            >
              {t('parentalConsentBack')}
            </button>
          </div>
          <p className="text-center text-xs text-muted-foreground/60">
            {t('parentalConsentSafety')}
          </p>
        </div>
      </div>
    )}

    {/* Daily Lesson Points Counter */}
    {lessonsToday > 0 && (
      <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 px-4 py-2 rounded-full bg-amber-500/90 text-white text-xs font-bold shadow-lg flex items-center gap-2 animate-in slide-in-from-top">
        <Star className="h-3.5 w-3.5" />
        <span>{t('dailyLessonPoints')} {lessonsToday}/5 {t('dailyLessonPointsFormat')}</span>
      </div>
    )}
    {/* Header - Luxury Glass */}
    <div className="sticky top-0 z-30 glass-nav border-b border-border/20 px-4 py-3" style={{background:'hsl(var(--card) / 0.8)'}}>
      <div className="flex items-center justify-between max-w-lg mx-auto">
        <button onClick={()=>{
          if(selectedSurah){setSelectedSurah(null);return;}
          if(selectedProphet){setSelectedProphet(null);return;}
          if(selItem){setSelItem(null);return;}
          nav(-1);
        }} className="p-2 rounded-full hover:bg-muted/40"><ArrowLeft className="h-5 w-5"/></button>
        <h1 className="text-lg font-bold flex items-center gap-2">
          <span className="text-xl">{TABS.find(t=>t.id===mainTab)?.emoji}</span>
          <span className="text-gradient-islamic">
            {t(TABS.find(tb=>tb.id===mainTab)?.key || mainTab)}
          </span>
        </h1>
        <div className="w-10"/>
      </div>
    </div>

    <div className="max-w-lg mx-auto px-4 pt-2">
      {/* Tab bar - Islamic Luxury */}
      {!selectedSurah && !selectedProphet && !selItem && (
        <div className="flex gap-1.5 overflow-x-auto pb-3 scrollbar-hide mb-1">
          {TABS.map(tab=>(<button key={tab.id} onClick={()=>setMainTab(tab.id)}
            className={cn("flex items-center gap-1.5 px-3.5 py-3 rounded-[1.25rem] text-xs font-bold whitespace-nowrap border transition-all shrink-0 min-h-[44px]",
              mainTab===tab.id
                ? "bg-gradient-to-r from-[hsl(var(--mystic-moss))]/15 to-[hsl(var(--islamic-emerald))]/10 border-[hsl(var(--mystic-moss))]/30 text-[hsl(var(--mystic-moss))] dark:from-[#D4AF37]/15 dark:to-[#D4AF37]/5 dark:border-[#D4AF37]/30 dark:text-[#D4AF37] shadow-lg"
                : "bg-muted/20 border-border/30 text-muted-foreground hover:bg-muted/40"
            )}>
            <span>{tab.emoji}</span><span>{t(tab.key)}</span>
          </button>))}
        </div>
      )}

      {mainTab==='curriculum' && renderCurriculum()}
      {mainTab==='lesson' && renderLesson()}
      {mainTab==='quran' && renderQuran()}
      {mainTab==='islam' && renderIslam()}
      {mainTab==='library' && renderLibrary()}
    </div>
  </div>);
}
