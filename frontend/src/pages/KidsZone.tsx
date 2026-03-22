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

/* ═══════ SECTION CARD ═══════ */
function SectionCard({emoji,title,children,color="blue",done=false,onDone}:{emoji:string;title:string;children:React.ReactNode;color?:string;done?:boolean;onDone?:()=>void}){
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
      <h3 className="font-bold text-sm flex-1">{title}</h3>
      {done && <span className="text-green-400 text-xs font-bold flex items-center gap-1"><Check className="h-3 w-3"/>✓</span>}
    </div>
    {children}
    {onDone && !done && <button onClick={onDone} className="w-full mt-3 py-2 rounded-xl bg-muted/30 text-muted-foreground text-sm flex items-center justify-center gap-1 border border-border/30 hover:bg-white/20 transition-all"><Check className="h-3.5 w-3.5"/>Done</button>}
    {done && <div className="mt-2 text-center text-xs text-green-400 font-bold">✅ Completed!</div>}
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
  const loadCurriculum = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/curriculum?locale=${lang}`); const d = await r.json(); if(d.success) setStages(d.stages); } catch{}
  };
  const loadCurrProgress = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/curriculum/progress?user_id=${userId}`); const d = await r.json(); if(d.success){ setCurrProgress(d.progress); if(!lessonDay) setLessonDay(d.progress.current_day||1); }} catch{}
  };
  const loadLesson = async (day?:number) => {
    const d = day || lessonDay || 1;
    try { const r = await fetch(`${API}/api/kids-learn/curriculum/lesson/${d}?locale=${lang}`); const data = await r.json(); if(data.success){setLesson(data.lesson);setLessonDay(d);setCompletedSections(new Set());}} catch{}
  };
  const loadSurahs = async () => {
    try { const r = await fetch(`${API}/api/kids-learn/quran/surahs?locale=${lang}`); const d = await r.json(); if(d.success) setSurahs(d.surahs); } catch{}
  };
  const loadIslamContent = async () => {
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
    }catch{}
  };
  const loadLibrary = async () => {
    try{const[c,i]=await Promise.all([
      fetch(`${API}/api/kids-learn/library/categories?locale=${lang}`).then(r=>r.json()),
      fetch(`${API}/api/kids-learn/library/items?category=all&locale=${lang}`).then(r=>r.json()),
    ]);if(c.success)setLibCats(c.categories);if(i.success)setLibItems(i.items);}catch{}
  };
  const loadLibItems = async(cat:string) => {
    try{const r=await fetch(`${API}/api/kids-learn/library/items?category=${cat}&locale=${lang}`);const d=await r.json();if(d.success)setLibItems(d.items);}catch{}
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
    }catch{}
  };

  // ═══════ RENDER: CURRICULUM OVERVIEW ═══════
  const renderCurriculum = () => {
    const currentDay = currProgress?.current_day || 1;
    const completedDays = currProgress?.completed_days || [];
    const totalXp = currProgress?.total_xp || 0;
    const streak = currProgress?.streak || 0;

    return(<div className="space-y-4 pb-8">
      {/* Hero Stats */}
      <div className="p-5 rounded-3xl bg-gradient-to-br from-violet-600/20 via-purple-500/15 to-pink-500/10 border border-violet-400/20">
        <div className="text-center mb-4">
          <span className="text-5xl">🎓</span>
          <h2 className="text-xl font-bold mt-2 bg-gradient-to-r from-violet-300 to-pink-300 bg-clip-text text-transparent">{t('completeCurriculum')}</h2>
          <p className="text-xs text-muted-foreground mt-1">{t('completeCurriculumDesc')}</p>
        </div>
        <div className="flex gap-3">
          <div className="flex-1 p-3 rounded-xl bg-muted/30 text-center">
            <Calendar className="h-5 w-5 text-blue-400 mx-auto"/>
            <p className="text-lg font-bold text-blue-300">{currentDay}</p>
            <p className="text-[9px] text-muted-foreground">{t('currentLesson')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-muted/30 text-center">
            <Check className="h-5 w-5 text-green-400 mx-auto"/>
            <p className="text-lg font-bold text-green-300">{completedDays.length}</p>
            <p className="text-[9px] text-muted-foreground">{t('completedLabel')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-muted/30 text-center">
            <Flame className="h-5 w-5 text-red-400 mx-auto"/>
            <p className="text-lg font-bold text-red-300">{streak}</p>
            <p className="text-[9px] text-muted-foreground">{t('streakSmall')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-muted/30 text-center">
            <Zap className="h-5 w-5 text-amber-400 mx-auto"/>
            <p className="text-lg font-bold text-amber-300">{totalXp}</p>
            <p className="text-[9px] text-muted-foreground">{t('xpLabel') || 'XP'}</p>
          </div>
        </div>
        {/* Overall progress bar */}
        <div className="mt-4">
          <div className="flex justify-between text-xs text-muted-foreground mb-1">
            <span>{t('overallProgress')}</span>
            <span>{Math.round((completedDays.length/1000)*100)}%</span>
          </div>
          <div className="h-3 bg-muted/40 rounded-full overflow-hidden">
            <div className="h-full rounded-full bg-gradient-to-r from-[#064E3B] via-[#0A6B52] to-[#D4AF37] transition-all" style={{width:`${(completedDays.length/1000)*100}%`}}/>
          </div>
        </div>
      </div>

      {/* Badges Preview */}
      {badges.length>0 && (<div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
        {badges.filter(b=>b.earned).map(b=>(<div key={b.id} className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 shrink-0">
          <span className="text-lg">{b.emoji}</span><span className="text-[10px] font-bold text-amber-300">{b[`title_${locale}`] || b.title_ar}</span>
        </div>))}
        {badges.filter(b=>!b.earned).slice(0,3).map(b=>(<div key={b.id} className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/5 border border-border/30 shrink-0 opacity-50">
          <span className="text-lg grayscale">{b.emoji}</span><span className="text-[10px] text-muted-foreground">{b[`title_${locale}`] || b.title_ar}</span>
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
        return(<div key={s.id} className={cn("rounded-[1.5rem] overflow-hidden border transition-all",isLocked?"opacity-50 border-border/10":"border-border/30")} style={{borderColor:!isLocked?s.color+'30':undefined}}>
          <button onClick={()=>!isLocked&&setExpandedStage(isOpen?null:s.id)} disabled={isLocked}
            className="w-full p-4 flex items-center gap-3" style={{background:`linear-gradient(135deg,${s.color}10,${s.color}05)`}}>
            <div className="w-12 h-12 rounded-[1rem] flex items-center justify-center text-2xl shadow-lg" style={{background:`linear-gradient(135deg,${s.color}25,${s.color}12)`}}>
              {isLocked?<Lock className="h-5 w-5 text-muted-foreground"/>:<span>{s.emoji}</span>}
            </div>
            <div className="flex-1 text-start">
              <h3 className="font-bold text-sm">{s.title}</h3>
              <p className="text-[10px] text-muted-foreground mt-0.5">{t('nLessons').replace('{n}', String(s.total_lessons))} • {t('dayN').replace('{n}', `${s.day_start}-${s.day_end}`)}</p>
              <div className="flex items-center gap-2 mt-1.5">
                <div className="flex-1 h-2 bg-muted/30 rounded-full"><div className="h-full rounded-full transition-all" style={{width:`${pct}%`,backgroundColor:s.color}}/></div>
                <span className="text-[10px] font-bold" style={{color:s.color}}>{pct}%</span>
              </div>
            </div>
            {isCurrent && <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-400 animate-pulse shrink-0">{t('nowLabel')}</span>}
            {pct===100 && <span className="text-green-400"><Check className="h-5 w-5"/></span>}
            {!isLocked && <ChevronDown className={cn("h-4 w-4 text-muted-foreground transition-transform shrink-0",isOpen&&"rotate-180")}/>}
          </button>
          {isOpen && (<div className="px-4 pb-4 pt-1">
            <p className="text-xs text-muted-foreground mb-3">{s.description}</p>
            <div className="grid grid-cols-7 gap-1.5">
              {Array.from({length:Math.min(s.total_lessons,42)}).map((_,i)=>{
                const dayNum = s.day_start + i;
                const isDone = completedDays.includes(dayNum);
                const isCurr = dayNum===currentDay;
                return(<button key={i} onClick={()=>{setLessonDay(dayNum);setMainTab('lesson');loadLesson(dayNum);}}
                  className={cn("aspect-square rounded-lg text-[10px] font-bold flex items-center justify-center transition-all border",
                    isDone?"bg-green-500/20 border-green-500/30 text-green-400":
                    isCurr?"bg-amber-500/20 border-amber-500/40 text-amber-400 animate-pulse":
                    dayNum<currentDay?"bg-white/5 border-border/30 text-muted-foreground":
                    "bg-white/3 border-white/5 text-muted-foreground/50"
                  )}>
                  {isDone?'✓':dayNum<=currentDay?i+1:<Lock className="h-2.5 w-2.5"/>}
                </button>);
              })}
            </div>
            {s.total_lessons>42 && <p className="text-[10px] text-muted-foreground text-center mt-2">+{s.total_lessons-42} {t('moreLessons').replace('{n}', String(s.total_lessons-42))}</p>}
          </div>)}
        </div>);
      })}
    </div>);
  };

  // ═══════ RENDER: STRUCTURED LESSON ═══════
  const renderLesson = () => {
    if(!lesson) return <div className="flex items-center justify-center h-40"><div className="animate-spin w-8 h-8 border-2 border-amber-400 border-t-transparent rounded-full"/></div>;
    const L=lesson;
    const sectionColors = ['green','blue','amber','purple','pink','indigo','teal','red'];
    return(<div className="space-y-4 pb-8">
      {/* Day nav */}
      <div className="flex items-center justify-between">
        <button onClick={()=>loadLesson(Math.max(1,L.day-1))} className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-lg font-bold">←</button>
        <div className="text-center">
          <div className="flex items-center gap-2 justify-center">
            <span className="text-xl">{L.stage.emoji}</span>
            <span className="text-xs px-2 py-0.5 rounded-full font-bold" style={{background:L.stage.color+'20',color:L.stage.color}}>{L.stage.title}</span>
          </div>
          <p className="text-2xl font-bold text-gradient-islamic mt-1">{t('dayN').replace('{n}', String(L.day))}</p>
          <p className="text-[10px] text-muted-foreground">{L.lesson_number_in_stage} / {L.total_in_stage}</p>
        </div>
        <button onClick={()=>loadLesson(Math.min(1000,L.day+1))} className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-lg font-bold">→</button>
      </div>

      {/* Lesson Title */}
      <div className="p-4 rounded-[1.5rem] bg-gradient-to-r from-[#064E3B]/10 to-[#D4AF37]/10 border border-[#064E3B]/20 text-center">
        <span className="text-3xl">📚</span>
        <h2 className="text-lg font-bold mt-2">{L.title[locale] || L.title.ar || L.title.en}</h2>
        <p className="text-xs text-muted-foreground mt-1">⭐ {L.xp_reward} {t('xpLabel') || 'XP'}</p>
      </div>

      {/* Progress */}
      <div className="flex items-center gap-2">
        <div className="flex-1 h-2 bg-muted/30 rounded-full"><div className="h-full rounded-full bg-gradient-to-r from-green-400 to-emerald-500 transition-all" style={{width:`${(completedSections.size/L.total_sections)*100}%`}}/></div>
        <span className="text-xs font-bold text-green-400">{completedSections.size}/{L.total_sections}</span>
      </div>

      {/* Sections */}
      {L.sections.map((sec,idx)=>{
        const isDone = completedSections.has(idx);
        const color = sectionColors[idx%sectionColors.length];
        return(<SectionCard key={idx} emoji={sec.emoji} title={sec.title} color={color} done={isDone} onDone={()=>markDone(idx)}>
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
          <button onClick={()=>loadLesson(L.day-1)} className="flex-1 py-3 rounded-2xl bg-muted/30 hover:bg-muted/50 text-foreground font-bold text-sm flex items-center justify-center gap-2 transition-all">
            ← {t('prevLessonBtn')}
          </button>
        )}
        {L.day < 1000 && (
          <button onClick={()=>loadLesson(L.day+1)} className="flex-1 py-3 rounded-2xl bg-gradient-to-r from-blue-500 to-indigo-500 text-white font-bold text-sm shadow-lg shadow-blue-500/20 flex items-center justify-center gap-2 hover:scale-[1.02] transition-all">
            {t('nextLessonBtn')} →
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
            <Volume2 className="h-5 w-5 text-blue-400"/>
            <span className="text-2xl font-bold font-arabic" dir="rtl">{c.text}</span>
          </button>
          {c.word && <button onClick={()=>speak(c.word,'ar')} className="w-full p-3 rounded-xl bg-purple-500/10 border border-purple-500/20 hover:bg-purple-500/20 transition-all flex items-center justify-center gap-2">
            <Volume2 className="h-4 w-4 text-purple-400"/>
            <span className="text-xl font-bold font-arabic" dir="rtl">{c.word}</span>
          </button>}
          {c.tip && <p className="text-xs text-muted-foreground">{c.tip}</p>}
        </div>);

      case 'quiz':
        return(<div className="space-y-2">
          <p className="text-sm font-bold text-center mb-3">{c.question}</p>
          <div className="grid grid-cols-2 gap-2">
            {c.options?.map((opt:string,i:number)=>(
              <button key={i} onClick={()=>{
                if(opt===c.correct){toast.success(t('correctAnswer'));speak(getNoorMessage('correct',locale));}
                else{toast.error(t('tryAgain'));}
              }} className="p-3 rounded-xl bg-card/60 border-2 border-border/30 hover:border-amber-400/40 transition-all text-center">
                <span className="text-2xl font-bold">{opt}</span>
              </button>
            ))}
          </div>
        </div>);

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
          <p className="text-xs text-emerald-400">{c.surah} - {t('ayahSingle')} {c.ayah_num}</p>
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
          {c.transliteration && <p className="text-xs italic text-blue-300/60">{c.transliteration}</p>}
          {c.meaning && <p className="text-sm text-muted-foreground">{c.meaning}</p>}
        </div>);

      case 'hadith':
        return(<div className="space-y-2">
          <p className="text-lg font-bold font-arabic leading-relaxed" dir="rtl">{c.arabic}</p>
          {c.translation && <p className="text-sm text-muted-foreground italic">{c.translation}</p>}
          <p className="text-xs text-amber-400/70">📌 {c.source}</p>
          <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/20"><p className="text-xs font-bold text-amber-300">💡 {c.lesson}</p></div>
        </div>);

      case 'story':
        return(<div className="space-y-2">
          <p className="text-lg font-bold">{c.name}</p>
          <p className="text-xs" style={{color:lesson?.stage.color}}>{c.title}</p>
          <p className="text-sm leading-relaxed">{c.summary}</p>
          <div className="p-2 rounded-xl bg-purple-500/10 border border-purple-500/20"><p className="text-xs font-bold text-purple-300">💡 {c.lesson}</p></div>
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
    if(selectedSurah) return(<div className="space-y-4 pb-8">
      <button onClick={()=>setSelectedSurah(null)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"><ArrowLeft className="h-4 w-4"/>{t('returnBack')}</button>
      <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 border border-emerald-400/30">
        <p className="text-3xl font-bold font-arabic">{selectedSurah.name_ar}</p>
        <p className="text-sm text-emerald-400 mt-1">{selectedSurah.name_en} - {selectedSurah.total_ayahs} {t('ayahPlural')}</p>
      </div>
      {selectedSurah.ayahs?.map((a:any,i:number)=>(
        <button key={i} onClick={()=>speak(a.arabic,'ar')} className="w-full p-4 rounded-2xl bg-card/60 border border-border/30 text-start hover:border-emerald-400/30 transition-all">
          <div className="flex items-start gap-3">
            <span className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-xs font-bold text-emerald-400 shrink-0">{a.number}</span>
            <div className="flex-1">
              <p className="text-xl font-bold font-arabic leading-loose" dir="rtl">{a.arabic}</p>
              {a.translation && <p className="text-sm text-muted-foreground mt-2">{a.translation}</p>}
            </div>
            <Volume2 className="h-4 w-4 text-emerald-400 shrink-0 mt-2"/>
          </div>
        </button>
      ))}
    </div>);

    return(<div className="space-y-4 pb-8">
      <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 border border-emerald-400/30">
        <span className="text-4xl">📖</span>
        <h2 className="text-lg font-bold mt-2">{t('quranMemTitle')}</h2>
        <p className="text-xs text-muted-foreground mt-1">{t('shortSurahsWithTranslation')}</p>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {surahs.map(s=>(<button key={s.id} onClick={()=>setSelectedSurah(s)} className="p-4 rounded-2xl bg-card/60 border border-border/30 hover:border-emerald-400/30 transition-all text-start">
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-xs font-bold text-emerald-400">{s.number}</span>
            <div><p className="font-bold text-sm font-arabic">{s.name_ar}</p><p className="text-[10px] text-muted-foreground">{s.name_en}</p></div>
          </div>
          <p className="text-[10px] text-muted-foreground mt-2">{s.total_ayahs} {t('ayahPlural')}</p>
        </button>))}
      </div>
    </div>);
  };

  // ═══════ RENDER: ISLAM ═══════
  const renderIslam = () => {
    if(selectedProphet) return(<div className="space-y-4 pb-8">
      <button onClick={()=>setSelectedProphet(null)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"><ArrowLeft className="h-4 w-4"/>{t('returnBack')}</button>
      <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-purple-500/15 to-violet-500/10 border border-purple-400/30">
        <span className="text-5xl">{selectedProphet.emoji}</span><h2 className="text-xl font-bold mt-2">{selectedProphet.name}</h2>
        <p className="text-sm text-purple-400">{selectedProphet.title}</p>
      </div>
      <div className="p-4 rounded-2xl bg-card/60 border border-border/30"><p className="text-sm leading-relaxed">{selectedProphet.summary}</p></div>
      <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20"><p className="text-sm font-bold text-purple-300">💡 {selectedProphet.lesson}</p></div>
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
        {subs.map(st=>(<button key={st.id} onClick={()=>setIslamSub(st.id)} className={cn("flex items-center gap-1 px-2.5 py-1.5 rounded-[1rem] text-[11px] font-bold whitespace-nowrap border transition-all shrink-0",
          islamSub===st.id?"bg-gradient-to-r from-[#064E3B]/15 to-[#0A6B52]/10 border-[#064E3B]/30 text-[#064E3B] dark:from-[#D4AF37]/15 dark:to-[#D4AF37]/10 dark:border-[#D4AF37]/30 dark:text-[#D4AF37]":"bg-muted/20 border-border/30 text-muted-foreground")}>
          <span>{st.emoji}</span>{st.label}<span className="text-[9px] opacity-60">({st.count})</span>
        </button>))}
      </div>

      {islamSub==='duas' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-blue-500/15 to-indigo-500/10 border border-blue-400/30">
          <span className="text-4xl">🤲</span>
          <h3 className="font-bold mt-2 text-lg">{dir==='rtl' ? 'أدعية يومية للمسلم الصغير' : 'Daily Duas for Young Muslims'}</h3>
          <p className="text-xs text-muted-foreground mt-1">{dir==='rtl' ? 'وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ' : '"Call upon Me; I will respond to you" - Quran 40:60'}</p>
        </div>
        {duas.map(d=>(<button key={d.id} onClick={()=>speak(d.arabic,'ar')} className="w-full p-4 rounded-2xl bg-gradient-to-r from-blue-500/10 to-indigo-500/5 border border-blue-500/20 text-start hover:border-blue-400/40 transition-all">
          <div className="flex items-center gap-2 mb-2"><span>{d.emoji}</span><span className="text-xs font-bold text-blue-300">{d.title}</span><Volume2 className="h-3 w-3 text-blue-400 ms-auto"/></div>
          <p className="text-lg font-bold font-arabic leading-relaxed" dir="rtl">{d.arabic}</p>
          {d.transliteration && <p className="text-xs text-blue-300/50 mt-1 italic">{d.transliteration}</p>}
          {d.meaning && <p className="text-sm text-muted-foreground mt-1">{d.meaning}</p>}
        </button>))}
      </div>)}

      {islamSub==='hadiths' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-amber-500/15 to-orange-500/10 border border-amber-400/30">
          <span className="text-4xl">📜</span>
          <h3 className="font-bold mt-2 text-lg">{dir==='rtl' ? 'أحاديث نبوية للأطفال' : 'Prophetic Hadiths for Children'}</h3>
          <p className="text-xs text-muted-foreground mt-1">{dir==='rtl' ? 'من كلام النبي محمد ﷺ' : 'From the words of Prophet Muhammad ﷺ'}</p>
        </div>
        {hadiths.map(h=>(<div key={h.id} className="p-4 rounded-2xl bg-gradient-to-r from-amber-500/10 to-orange-500/5 border border-amber-500/20">
          <div className="flex items-center gap-2 mb-2"><span className="text-xl">{h.emoji}</span><span className="text-xs font-bold text-amber-300 capitalize">{h.category}</span></div>
          <p className="text-lg font-bold font-arabic leading-relaxed" dir="rtl">{h.arabic}</p>
          {h.translation && lang!=='ar' && <p className="text-sm text-muted-foreground mt-2 italic">{h.translation}</p>}
          <p className="text-xs text-muted-foreground mt-2">📌 {h.source}</p>
          <div className="mt-2 p-2 rounded-xl bg-amber-500/10 border border-amber-500/20"><p className="text-xs font-bold text-amber-300">💡 {h.lesson}</p></div>
        </div>))}
      </div>)}

      {islamSub==='prophets' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-purple-500/15 to-violet-500/10 border border-purple-400/30">
          <span className="text-4xl">📿</span>
          <h3 className="font-bold mt-2 text-lg">{dir==='rtl' ? 'قصص الأنبياء عليهم السلام' : 'Stories of the Prophets (Peace be upon them)'}</h3>
          <p className="text-xs text-muted-foreground mt-1">{dir==='rtl' ? 'نَحْنُ نَقُصُّ عَلَيْكَ أَحْسَنَ الْقَصَصِ — يوسف:٣' : '"We relate to you the best of stories" — Yusuf:3'}</p>
        </div>
        {prophets.map(p=>(<button key={p.id} onClick={()=>setSelectedProphet(p)} className="w-full p-4 rounded-2xl bg-gradient-to-r from-purple-500/10 to-violet-500/5 border border-purple-500/20 text-start hover:border-purple-400/40 transition-all">
          <div className="flex items-center gap-3"><span className="text-3xl">{p.emoji}</span>
            <div className="flex-1"><p className="font-bold text-purple-300">{p.number}. {p.name}</p><p className="text-xs text-purple-400/70">{p.title}</p></div>
            <ChevronRight className="h-5 w-5 text-muted-foreground"/>
          </div>
        </button>))}
      </div>)}

      {islamSub==='pillars' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-emerald-500/15 to-teal-500/10 border border-emerald-400/30">
          <span className="text-4xl">🕋</span>
          <h3 className="font-bold mt-2 text-lg">{dir==='rtl' ? 'أركان الإسلام الخمسة' : 'The Five Pillars of Islam'}</h3>
          <p className="text-xs text-muted-foreground mt-1">{dir==='rtl' ? 'بُنِيَ الإسلامُ على خمس' : 'Islam is built upon five pillars'}</p>
        </div>
        {pillars.map(p=>(<div key={p.id} className="p-4 rounded-2xl bg-gradient-to-r from-emerald-500/10 to-teal-500/5 border border-emerald-500/20">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center text-2xl shadow-lg shadow-emerald-500/20">{p.emoji}</div>
          <div className="flex-1"><p className="font-bold text-emerald-300">{p.number}. {p.title}</p><p className="text-sm text-muted-foreground mt-1 leading-relaxed">{p.description}</p></div>
        </div>
      </div>))}
      </div>)}

      {islamSub==='wudu' && (<div className="space-y-3">
        <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-blue-500/15 to-cyan-500/10 border border-blue-400/30">
          <span className="text-4xl">💧</span>
          <h3 className="font-bold mt-2 text-lg">{t('wuduStepsTitle')}</h3>
          <p className="text-xs text-muted-foreground mt-1">{dir==='rtl' ? 'تعلّم الوضوء خطوة بخطوة • الطهارة مفتاح الصلاة' : 'Learn Wudu Step by Step • Purity is the Key to Prayer'}</p>
        </div>
        {wuduSteps.map((s:any)=>(<div key={s.step} className="p-3 rounded-xl bg-gradient-to-r from-blue-500/10 to-cyan-500/5 border border-blue-500/20 flex items-start gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-sm font-bold text-white shrink-0 shadow-lg shadow-blue-500/20">{s.step}</div>
          <div className="flex-1">
            <p className="font-bold text-sm text-blue-300">{s.emoji} {s.title}</p>
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{s.description}</p>
          </div>
        </div>))}
        <div className="text-center p-3 rounded-xl bg-white/5 border border-border/30">
          <p className="text-[10px] text-muted-foreground">{dir==='rtl' ? '📚 المرجع: صفة وضوء النبي ﷺ — البخاري ومسلم' : '📚 Reference: The Prophet\'s Wudu ﷺ — Bukhari & Muslim'}</p>
        </div>
      </div>)}

      {islamSub==='salah' && (<SalahGuide steps={salahSteps} />)}
    </div>);
  };

  // ═══════ RENDER: LIBRARY ═══════
  const renderLibrary = () => {
    if(selItem) return(<div className="space-y-4 pb-8">
      <button onClick={()=>setSelItem(null)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"><ArrowLeft className="h-4 w-4"/>{t('returnBack')}</button>
      <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-indigo-500/15 to-blue-500/10 border border-indigo-400/30">
        <span className="text-5xl">{selItem.emoji}</span><h2 className="text-xl font-bold mt-2">{selItem.title}</h2>
        <p className="text-xs text-muted-foreground mt-1">{selItem.age_range}</p>
      </div>
      <div className="p-4 rounded-2xl bg-card/60 border border-border/30"><p className="text-sm leading-relaxed whitespace-pre-line">{selItem.content}</p></div>
      {selItem.lesson && <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20"><p className="text-sm font-bold text-amber-300">💡 {selItem.lesson}</p></div>}
    </div>);

    return(<div className="space-y-4 pb-8">
      <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-indigo-500/15 to-blue-500/10 border border-indigo-400/30">
        <span className="text-4xl">📚</span><h2 className="text-lg font-bold mt-2">{t('learningLibraryTitle')}</h2>
      </div>
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
        <button onClick={()=>{setSelCat('all');loadLibItems('all');}} className={cn("px-3 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap border transition-all shrink-0",selCat==='all'?"bg-indigo-500/20 border-indigo-400/40 text-indigo-300":"bg-white/5 border-border/30 text-muted-foreground")}>{t('allFilter')}</button>
        {libCats.map(c=>(<button key={c.id} onClick={()=>{setSelCat(c.id);loadLibItems(c.id);}} className={cn("flex items-center gap-1 px-3 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap border transition-all shrink-0",selCat===c.id?"bg-indigo-500/20 border-indigo-400/40 text-indigo-300":"bg-white/5 border-border/30 text-muted-foreground")}>
          <span>{c.emoji}</span>{c.title}
        </button>))}
      </div>
      {libItems.map(item=>(<button key={item.id} onClick={()=>setSelItem(item)} className="w-full p-4 rounded-2xl bg-card/60 border border-border/30 text-start hover:border-indigo-400/30 transition-all">
        <div className="flex items-center gap-3"><span className="text-3xl">{item.emoji}</span>
          <div className="flex-1"><p className="font-bold text-sm">{item.title}</p><p className="text-xs text-muted-foreground mt-1 line-clamp-2">{item.content}</p></div>
          <ChevronRight className="h-5 w-5 text-muted-foreground"/>
        </div>
      </button>))}
    </div>);
  };

  // ═══════ MAIN RENDER ═══════
  return(<div dir={dir} className="min-h-screen bg-background pb-24">
    <Confetti on={confetti}/>
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
                ? "bg-gradient-to-r from-[#064E3B]/15 to-[#0A6B52]/10 border-[#064E3B]/30 text-[#064E3B] dark:from-[#D4AF37]/15 dark:to-[#D4AF37]/5 dark:border-[#D4AF37]/30 dark:text-[#D4AF37] shadow-lg"
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
