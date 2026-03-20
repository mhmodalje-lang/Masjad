import { useState, useEffect, useCallback, useMemo } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import NoorMascot, { useNoorTTS, getNoorMessage } from '@/components/NoorMascot';
import GrowthTree from '@/components/GrowthTree';
import PronunciationCheck from '@/components/PronunciationCheck';
import SentenceBuilder from '@/components/SentenceBuilder';
import { Star, Trophy, BookOpen, Gamepad2, Volume2, Check, X, Sparkles, ArrowLeft, ArrowRight, GraduationCap, Play, TreePine, Mic, Hash, Type, MessageSquare, ChevronDown, ChevronUp, Lock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Progress {
  completed_days: number[];
  completed_letters: number[];
  completed_numbers: number[];
  completed_vocab: string[];
  completed_sentences: string[];
  stars: number;
  total_xp: number;
  golden_bricks: number;
  tree_level: number;
  streak: number;
}

type MainTab = 'daily' | 'curriculum' | 'practice' | 'tree';

// Video IDs for educational content by language
const DAILY_VIDEOS: Record<string, string[]> = {
  ar: ['dSgQFkFx2JI', 'Y6gGn-3pSbA', 'XJvOfBGN8lc', 'D5SjkflFMHU'],
  en: ['LsoLEjrDogU', 'OF_rTq4btOk', 'poNBnm08jas', 'VqGJSTcz-G0'],
  de: ['5YG4JHWxLbI', 'v4jQoOYP5L8', 'RjGkBh5cL_0', 'dSgQFkFx2JI'],
  fr: ['UKUiJhFwuMg', 'OF_rTq4btOk', 'LsoLEjrDogU', 'dSgQFkFx2JI'],
  tr: ['dSgQFkFx2JI', 'OF_rTq4btOk', 'XJvOfBGN8lc', 'D5SjkflFMHU'],
  ru: ['dSgQFkFx2JI', 'OF_rTq4btOk', 'LsoLEjrDogU', 'Y6gGn-3pSbA'],
  sv: ['dSgQFkFx2JI', 'OF_rTq4btOk', 'XJvOfBGN8lc', 'LsoLEjrDogU'],
  nl: ['dSgQFkFx2JI', 'OF_rTq4btOk', 'Y6gGn-3pSbA', 'LsoLEjrDogU'],
  el: ['dSgQFkFx2JI', 'OF_rTq4btOk', 'LsoLEjrDogU', 'XJvOfBGN8lc'],
};

const NOOR_DAILY_MESSAGES: Record<string, string[]> = {
  ar: ['صباح الخير! اليوم سنتعلم حرفاً جديداً ✨', 'مرحباً يا بطل! هل أنت مستعد للدرس؟ 🌟', 'أهلاً! لنبدأ مغامرة التعلم اليومية! 📚'],
  en: ['Good morning! Today we learn a new letter ✨', 'Hello champion! Ready for today\'s lesson? 🌟', 'Hi! Let\'s start our daily learning adventure! 📚'],
  de: ['Guten Morgen! Heute lernen wir einen neuen Buchstaben ✨', 'Hallo Champion! Bereit für die heutige Lektion? 🌟', 'Hallo! Starten wir unser tägliches Lernabenteuer! 📚'],
  fr: ['Bonjour! Aujourd\'hui on apprend une nouvelle lettre ✨', 'Salut champion! Prêt pour la leçon du jour? 🌟', 'Coucou! Commençons notre aventure quotidienne! 📚'],
  tr: ['Günaydın! Bugün yeni bir harf öğreneceğiz ✨', 'Merhaba şampiyon! Bugünkü derse hazır mısın? 🌟', 'Selam! Günlük öğrenme maceramıza başlayalım! 📚'],
  ru: ['Доброе утро! Сегодня выучим новую букву ✨', 'Привет чемпион! Готов к уроку? 🌟', 'Привет! Начнём наше ежедневное путешествие! 📚'],
};

export default function ArabicAcademy() {
  const { t, dir, locale } = useLocale();
  const navigate = useNavigate();
  const { speak } = useNoorTTS();

  const [mainTab, setMainTab] = useState<MainTab>('daily');
  const [curriculum, setCurriculum] = useState<any[]>([]);
  const [letters, setLetters] = useState<any[]>([]);
  const [numbers, setNumbers] = useState<any[]>([]);
  const [vocabCategories, setVocabCategories] = useState<string[]>([]);
  const [vocab, setVocab] = useState<any[]>([]);
  const [sentences, setSentences] = useState<any[]>([]);
  const [selectedDay, setSelectedDay] = useState<number | null>(null);
  const [dayContent, setDayContent] = useState<any>(null);
  const [selectedLetter, setSelectedLetter] = useState<any>(null);
  const [activeVocabCat, setActiveVocabCat] = useState('animals');
  const [showVideo, setShowVideo] = useState(false);
  const [expandedLevel, setExpandedLevel] = useState<number | null>(1);
  const [practiceMode, setPracticeMode] = useState<'letters' | 'numbers' | 'vocab' | 'sentences'>('letters');
  const [noorMsg, setNoorMsg] = useState('');
  const [noorMood, setNoorMood] = useState<'happy' | 'thinking' | 'celebrating' | 'greeting'>('greeting');
  const [loading, setLoading] = useState(true);

  const [progress, setProgress] = useState<Progress>({
    completed_days: [], completed_letters: [], completed_numbers: [],
    completed_vocab: [], completed_sentences: [],
    stars: 0, total_xp: 0, golden_bricks: 0, tree_level: 1, streak: 0,
  });

  // Daily greeting
  useEffect(() => {
    const msgs = NOOR_DAILY_MESSAGES[locale] || NOOR_DAILY_MESSAGES['en'];
    const dayIdx = new Date().getDate() % msgs.length;
    setNoorMsg(msgs[dayIdx]);
  }, [locale]);

  // Load all data
  useEffect(() => {
    async function loadAll() {
      try {
        const [currRes, letRes, numRes, vocRes, sentRes] = await Promise.all([
          fetch(`${BACKEND_URL}/api/arabic-academy/curriculum`),
          fetch(`${BACKEND_URL}/api/arabic-academy/letters`),
          fetch(`${BACKEND_URL}/api/arabic-academy/numbers`),
          fetch(`${BACKEND_URL}/api/arabic-academy/vocabulary`),
          fetch(`${BACKEND_URL}/api/arabic-academy/sentences`),
        ]);
        const [currData, letData, numData, vocData, sentData] = await Promise.all([
          currRes.json(), letRes.json(), numRes.json(), vocRes.json(), sentRes.json()
        ]);
        if (currData.success) setCurriculum(currData.curriculum);
        if (letData.success) setLetters(letData.letters);
        if (numData.success) setNumbers(numData.numbers);
        if (vocData.success) { setVocab(vocData.words); setVocabCategories(vocData.categories); }
        if (sentData.success) setSentences(sentData.sentences);
      } catch (e) { console.error('Load error:', e); }
      const saved = localStorage.getItem('academy-progress-v2');
      if (saved) try { setProgress(JSON.parse(saved)); } catch {}
      setLoading(false);
    }
    loadAll();
  }, []);

  const saveProgress = useCallback((p: Progress) => {
    setProgress(p);
    localStorage.setItem('academy-progress-v2', JSON.stringify(p));
  }, []);

  const addXP = useCallback((xp: number) => {
    const np = { ...progress, total_xp: progress.total_xp + xp, stars: progress.stars + (xp >= 10 ? 1 : 0), golden_bricks: progress.golden_bricks + (xp >= 10 ? 1 : 0), tree_level: Math.floor((progress.total_xp + xp) / 100) + 1 };
    saveProgress(np);
    toast.success(`⚡ +${xp} XP`);
  }, [progress, saveProgress]);

  const completeDay = useCallback((day: number) => {
    if (progress.completed_days.includes(day)) return;
    const np = { ...progress, completed_days: [...progress.completed_days, day] };
    saveProgress(np);
    addXP(10);
    setNoorMood('celebrating');
    setNoorMsg(getNoorMessage('correct', locale));
  }, [progress, saveProgress, addXP, locale]);

  const completeLetter = useCallback((id: number) => {
    if (progress.completed_letters.includes(id)) return;
    saveProgress({ ...progress, completed_letters: [...progress.completed_letters, id] });
    addXP(10);
  }, [progress, saveProgress, addXP]);

  const completeVocab = useCallback((id: string) => {
    if (progress.completed_vocab.includes(id)) return;
    saveProgress({ ...progress, completed_vocab: [...progress.completed_vocab, id] });
    addXP(5);
  }, [progress, saveProgress, addXP]);

  // Load day content
  const loadDay = useCallback(async (day: number) => {
    setSelectedDay(day);
    try {
      const res = await fetch(`${BACKEND_URL}/api/arabic-academy/curriculum/day/${day}`);
      const data = await res.json();
      if (data.success) setDayContent(data);
    } catch (e) { console.error(e); }
  }, []);

  // Daily video
  const todayVideo = useMemo(() => {
    const videos = DAILY_VIDEOS[locale] || DAILY_VIDEOS['en'];
    return videos[new Date().getDate() % videos.length];
  }, [locale]);

  // Current curriculum day
  const currentDay = useMemo(() => {
    const last = Math.max(0, ...progress.completed_days);
    return Math.min(last + 1, 90);
  }, [progress.completed_days]);

  // Get vocab meaning in user's language
  const getVocabMeaning = (word: any) => {
    const key = `meaning_${locale}`;
    return word[key] || word.meaning_en || '';
  };

  const levelDays = useMemo(() => ({
    1: curriculum.filter(d => d.level === 1),
    2: curriculum.filter(d => d.level === 2),
    3: curriculum.filter(d => d.level === 3),
    4: curriculum.filter(d => d.level === 4),
  }), [curriculum]);

  const LEVEL_INFO = [
    { id: 1, titleKey: 'level1Title', icon: '🌱', color: 'from-green-500', days: '1-30', type: 'letter' },
    { id: 2, titleKey: 'level2Title_num', icon: '🔢', color: 'from-blue-500', days: '31-42', type: 'number' },
    { id: 3, titleKey: 'level3Title_vocab', icon: '📖', color: 'from-purple-500', days: '43-78', type: 'vocab' },
    { id: 4, titleKey: 'level4Title_sent', icon: '✍️', color: 'from-amber-500', days: '79-90', type: 'sentence' },
  ];

  const tabs: { key: MainTab; icon: any; labelKey: string }[] = [
    { key: 'daily', icon: Play, labelKey: 'dailyClass' },
    { key: 'curriculum', icon: GraduationCap, labelKey: 'curriculum' },
    { key: 'practice', icon: Mic, labelKey: 'practice' },
    { key: 'tree', icon: TreePine, labelKey: 'growthTree' },
  ];

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
    </div>
  );

  return (
    <div className="min-h-screen pb-28 bg-gradient-to-b from-amber-50/50 via-background to-background dark:from-amber-950/20" dir={dir}>
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center justify-between">
        <button onClick={() => navigate(-1)} className="p-2 rounded-xl hover:bg-muted/50">
          {dir === 'rtl' ? <ArrowRight className="h-5 w-5" /> : <ArrowLeft className="h-5 w-5" />}
        </button>
        <h1 className="text-sm font-black text-foreground flex items-center gap-1.5">
          <span>👶</span> {t('arabicAcademy')}
        </h1>
        <div className="flex items-center gap-1.5 text-xs">
          <span className="font-bold text-amber-500">⭐{progress.stars}</span>
          <span className="font-bold text-primary">⚡{progress.total_xp}</span>
        </div>
      </div>

      {/* Mini Noor + Progress */}
      <div className="px-4 pt-3 flex items-center gap-3">
        <NoorMascot message={noorMsg} mood={noorMood} size="sm" className="shrink-0" />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <Trophy className="w-3.5 h-3.5 text-amber-500" />
            <span className="text-[11px] font-bold">{t('day')} {currentDay}/90</span>
            <span className="text-[10px] text-muted-foreground">🧱{progress.golden_bricks}</span>
          </div>
          <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-amber-400 to-orange-500 rounded-full transition-all" style={{ width: `${(progress.completed_days.length / 90) * 100}%` }} />
          </div>
          <p className="text-[9px] text-muted-foreground mt-0.5">{progress.completed_letters.length}/28 {t('lettersCompleted')} · {progress.completed_vocab.length} {t('wordsLearned')}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="px-4 my-3 flex gap-1">
        {tabs.map(tab => (
          <button key={tab.key} onClick={() => { setMainTab(tab.key); setSelectedDay(null); setSelectedLetter(null); }}
            className={cn('flex-1 flex items-center justify-center gap-1 py-2 rounded-xl text-[10px] font-bold transition-all',
              mainTab === tab.key ? 'bg-primary text-primary-foreground shadow-lg' : 'bg-card border border-border/30 text-muted-foreground'
            )}>
            <tab.icon className="w-3.5 h-3.5" />
            {t(tab.labelKey)}
          </button>
        ))}
      </div>

      <div className="px-4">
        {/* ========== DAILY CLASSROOM ========== */}
        {mainTab === 'daily' && !selectedDay && (
          <div className="space-y-4 animate-fade-in">
            {/* Daily Video */}
            <div className="bg-card rounded-2xl border border-border/30 overflow-hidden">
              <div className="p-3 flex items-center justify-between">
                <h3 className="text-sm font-bold flex items-center gap-1.5">🎬 {t('dailyClassroom')}</h3>
                <span className="text-[10px] text-muted-foreground">{t('day')} {currentDay}</span>
              </div>
              {showVideo ? (
                <div className="aspect-video bg-black">
                  <iframe src={`https://www.youtube.com/embed/${todayVideo}?autoplay=1&rel=0&modestbranding=1`}
                    className="w-full h-full" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
                </div>
              ) : (
                <button onClick={() => setShowVideo(true)} className="w-full aspect-video bg-gradient-to-br from-primary/20 to-primary/5 flex flex-col items-center justify-center gap-3 hover:from-primary/30 transition-all">
                  <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center">
                    <Play className="w-8 h-8 text-primary fill-primary" />
                  </div>
                  <p className="text-sm font-bold text-foreground">{t('watchTodayLesson')}</p>
                </button>
              )}
            </div>

            {/* Today's lesson card */}
            {curriculum[currentDay - 1] && (
              <button onClick={() => loadDay(currentDay)}
                className="w-full bg-gradient-to-r from-primary/10 to-primary/5 rounded-2xl border border-primary/20 p-4 text-start active:scale-[0.98]">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center text-2xl shrink-0">
                    {curriculum[currentDay - 1].level === 1 ? '📝' : curriculum[currentDay - 1].level === 2 ? '🔢' : curriculum[currentDay - 1].level === 3 ? '📖' : '✍️'}
                  </div>
                  <div>
                    <p className="text-sm font-bold">{t('todayLesson')}: {t('day')} {currentDay}</p>
                    <p className="text-xs text-muted-foreground">{locale === 'ar' ? curriculum[currentDay - 1].title_ar : curriculum[currentDay - 1].title_en}</p>
                    <span className="text-[10px] text-primary font-bold">+{curriculum[currentDay - 1].xp} XP</span>
                  </div>
                  <ArrowRight className="w-5 h-5 text-primary ms-auto" />
                </div>
              </button>
            )}

            {/* Quick Stats */}
            <div className="grid grid-cols-3 gap-2">
              {[
                { label: t('streak'), value: `🔥 ${progress.streak}`, color: 'from-orange-500/20' },
                { label: t('level'), value: `⭐ ${progress.tree_level}`, color: 'from-amber-500/20' },
                { label: t('goldenBricks'), value: `🧱 ${progress.golden_bricks}`, color: 'from-yellow-500/20' },
              ].map((s, i) => (
                <div key={i} className={cn('bg-gradient-to-br to-transparent rounded-xl p-3 text-center border border-border/20', s.color)}>
                  <p className="text-lg font-black">{s.value}</p>
                  <p className="text-[9px] text-muted-foreground">{s.label}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========== DAY LESSON DETAIL ========== */}
        {mainTab === 'daily' && selectedDay && dayContent && (
          <div className="animate-fade-in space-y-4">
            <button onClick={() => { setSelectedDay(null); setDayContent(null); setSelectedLetter(null); }} className="flex items-center gap-1 text-sm text-primary font-bold">
              {dir === 'rtl' ? <ArrowRight className="w-4 h-4" /> : <ArrowLeft className="w-4 h-4" />} {t('back')}
            </button>

            <div className="bg-card rounded-2xl border border-border/30 p-4 text-center">
              <span className="text-3xl">{dayContent.lesson.level === 1 ? '📝' : dayContent.lesson.level === 2 ? '🔢' : dayContent.lesson.level === 3 ? '📖' : '✍️'}</span>
              <h2 className="text-lg font-black mt-2">{t('day')} {selectedDay}</h2>
              <p className="text-xs text-muted-foreground">{locale === 'ar' ? dayContent.lesson.title_ar : dayContent.lesson.title_en}</p>
            </div>

            {/* Letter content */}
            {dayContent.lesson.type === 'letter' && dayContent.content && (
              <div className="space-y-3">
                <div className="bg-card rounded-2xl border border-border/30 p-6 text-center">
                  <div className="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-3">
                    <span className="text-6xl font-bold" dir="rtl">{dayContent.content.letter}</span>
                  </div>
                  <h3 className="text-xl font-black" dir="rtl">{dayContent.content.name_ar}</h3>
                  <p className="text-sm text-muted-foreground">{dayContent.content.name_en} ({dayContent.content.transliteration})</p>
                  <button onClick={() => speak(dayContent.content.name_ar, 'ar')} className="mt-2 inline-flex items-center gap-1.5 px-3 py-1.5 bg-primary/10 text-primary rounded-full text-xs font-bold">
                    <Volume2 className="w-3.5 h-3.5" /> {t('listenPronunciation')}
                  </button>
                </div>

                {/* Forms */}
                <div className="bg-card rounded-2xl border border-border/30 p-3">
                  <h4 className="text-xs font-bold mb-2">{t('letterForms')}</h4>
                  <div className="grid grid-cols-4 gap-1.5">
                    {[{l: t('isolated'), f: dayContent.content.form_isolated}, {l: t('initial'), f: dayContent.content.form_initial}, {l: t('medial'), f: dayContent.content.form_medial}, {l: t('final'), f: dayContent.content.form_final}].map((x, i) => (
                      <div key={i} className="text-center p-2 bg-muted/30 rounded-lg">
                        <span className="text-xl font-bold" dir="rtl">{x.f}</span>
                        <p className="text-[8px] text-muted-foreground">{x.l}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Pronunciation Check */}
                <div className="bg-card rounded-2xl border border-border/30 p-4">
                  <h4 className="text-xs font-bold mb-3 flex items-center gap-1.5"><Mic className="w-3.5 h-3.5 text-primary" /> {t('pronunciationCheck')}</h4>
                  <PronunciationCheck
                    targetWord={dayContent.content.name_ar}
                    targetTransliteration={dayContent.content.transliteration}
                    onResult={(correct) => { if (correct) { setNoorMood('celebrating'); setNoorMsg(getNoorMessage('correct', locale)); } }}
                  />
                </div>

                {/* Example */}
                <div className="bg-card rounded-2xl border border-border/30 p-3 text-center">
                  <h4 className="text-xs font-bold mb-1">{t('exampleWord')}</h4>
                  <span className="text-3xl font-bold text-primary" dir="rtl">{dayContent.content.example_word}</span>
                  <p className="text-xs text-muted-foreground">= {dayContent.content.example_meaning}</p>
                </div>
              </div>
            )}

            {/* Number content */}
            {dayContent.lesson.type === 'number' && dayContent.content && (
              <div className="bg-card rounded-2xl border border-border/30 p-6 text-center space-y-3">
                <div className="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-blue-500/20 to-blue-500/5 flex items-center justify-center">
                  <span className="text-5xl font-bold text-blue-500">{dayContent.content.arabic}</span>
                </div>
                <h3 className="text-xl font-black" dir="rtl">{dayContent.content.word_ar}</h3>
                <p className="text-sm text-muted-foreground">{dayContent.content.word_en} ({dayContent.content.transliteration})</p>
                <button onClick={() => speak(dayContent.content.word_ar, 'ar')} className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-500/10 text-blue-500 rounded-full text-xs font-bold">
                  <Volume2 className="w-3.5 h-3.5" /> {t('listenPronunciation')}
                </button>
                <PronunciationCheck targetWord={dayContent.content.word_ar} targetTransliteration={dayContent.content.transliteration} onResult={() => {}} />
              </div>
            )}

            {/* Vocab content */}
            {dayContent.lesson.type === 'vocab' && dayContent.content && (
              <div className="bg-card rounded-2xl border border-border/30 p-6 text-center space-y-3">
                <span className="text-4xl">{dayContent.content.emoji}</span>
                <div className="w-20 h-20 mx-auto rounded-full bg-gradient-to-br from-purple-500/20 to-purple-500/5 flex items-center justify-center">
                  <span className="text-2xl font-bold" dir="rtl">{dayContent.content.word}</span>
                </div>
                <p className="text-sm text-muted-foreground">{dayContent.content.transliteration} — {getVocabMeaning(dayContent.content)}</p>
                <button onClick={() => speak(dayContent.content.word, 'ar')} className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-purple-500/10 text-purple-500 rounded-full text-xs font-bold">
                  <Volume2 className="w-3.5 h-3.5" /> {t('listenPronunciation')}
                </button>
                <PronunciationCheck targetWord={dayContent.content.word} targetTransliteration={dayContent.content.transliteration} onResult={(ok) => { if (ok) completeVocab(dayContent.content.id); }} />
              </div>
            )}

            {/* Sentence content */}
            {dayContent.lesson.type === 'sentence' && dayContent.content && (
              <div className="bg-card rounded-2xl border border-border/30 p-4">
                <SentenceBuilder
                  wordsAr={dayContent.content.words_ar}
                  wordsEn={dayContent.content.words_en}
                  correctSentenceAr={dayContent.content.sentence_ar}
                  correctSentenceEn={dayContent.content.sentence_en}
                  onComplete={(ok) => { if (ok) { completeDay(selectedDay); setNoorMood('celebrating'); } }}
                />
              </div>
            )}

            {/* Complete button */}
            {!progress.completed_days.includes(selectedDay) ? (
              <button onClick={() => completeDay(selectedDay)} className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-2xl font-bold text-sm flex items-center justify-center gap-2 active:scale-[0.98]">
                <Check className="w-4 h-4" /> {t('completeLesson')} (+10 XP)
              </button>
            ) : (
              <div className="w-full py-3 bg-green-500/10 text-green-500 rounded-2xl font-bold text-sm flex items-center justify-center gap-2">
                <Check className="w-4 h-4" /> {t('lessonCompleted')} ✅
              </div>
            )}
          </div>
        )}

        {/* ========== CURRICULUM MAP ========== */}
        {mainTab === 'curriculum' && (
          <div className="space-y-3 animate-fade-in">
            {LEVEL_INFO.map(lvl => {
              const days = levelDays[lvl.id as keyof typeof levelDays] || [];
              const completedInLevel = days.filter(d => progress.completed_days.includes(d.day)).length;
              const pct = days.length > 0 ? Math.round((completedInLevel / days.length) * 100) : 0;
              const isExpanded = expandedLevel === lvl.id;

              return (
                <div key={lvl.id} className="bg-card rounded-2xl border border-border/30 overflow-hidden">
                  <button onClick={() => setExpandedLevel(isExpanded ? null : lvl.id)} className="w-full p-4 flex items-center gap-3 text-start">
                    <div className={cn('w-10 h-10 rounded-xl bg-gradient-to-br to-transparent flex items-center justify-center text-lg', lvl.color + '/20')}>
                      {lvl.icon}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold">{t(lvl.titleKey)}</span>
                        {pct === 100 && <Check className="w-4 h-4 text-green-500" />}
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                          <div className={cn('h-full rounded-full bg-gradient-to-r', lvl.color, 'to-transparent')} style={{ width: `${pct}%` }} />
                        </div>
                        <span className="text-[10px] font-bold text-muted-foreground">{pct}%</span>
                      </div>
                    </div>
                    {isExpanded ? <ChevronUp className="w-4 h-4 text-muted-foreground" /> : <ChevronDown className="w-4 h-4 text-muted-foreground" />}
                  </button>

                  {isExpanded && (
                    <div className="px-4 pb-4 grid grid-cols-5 gap-1.5">
                      {days.map(d => {
                        const isDone = progress.completed_days.includes(d.day);
                        const isCurrent = d.day === currentDay;
                        const isLocked = d.day > currentDay + 3;
                        return (
                          <button key={d.day} disabled={isLocked} onClick={() => loadDay(d.day)}
                            className={cn('relative p-2 rounded-lg text-center transition-all text-xs',
                              isDone ? 'bg-green-500/20 text-green-500 font-bold' :
                              isCurrent ? 'bg-primary/20 text-primary font-bold ring-2 ring-primary/40' :
                              isLocked ? 'bg-muted/30 text-muted-foreground/30' :
                              'bg-muted/50 text-foreground hover:bg-primary/10'
                            )}>
                            {isLocked ? <Lock className="w-3 h-3 mx-auto" /> : isDone ? '✅' : d.day}
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* ========== PRACTICE TAB ========== */}
        {mainTab === 'practice' && !selectedLetter && (
          <div className="space-y-3 animate-fade-in">
            {/* Practice mode selector */}
            <div className="flex gap-1.5 overflow-x-auto no-scrollbar">
              {([
                { key: 'letters' as const, icon: '📝', label: t('arabicLetters') },
                { key: 'numbers' as const, icon: '🔢', label: t('numbers') },
                { key: 'vocab' as const, icon: '📖', label: t('quranVocab') },
                { key: 'sentences' as const, icon: '✍️', label: t('sentenceBuilder') },
              ]).map(m => (
                <button key={m.key} onClick={() => setPracticeMode(m.key)}
                  className={cn('flex items-center gap-1 px-3 py-2 rounded-xl text-[10px] font-bold whitespace-nowrap shrink-0',
                    practiceMode === m.key ? 'bg-primary text-primary-foreground' : 'bg-card border border-border/30 text-muted-foreground'
                  )}>
                  {m.icon} {m.label}
                </button>
              ))}
            </div>

            {/* Letters practice */}
            {practiceMode === 'letters' && (
              <div className="grid grid-cols-4 gap-2">
                {letters.map(l => {
                  const done = progress.completed_letters.includes(l.id);
                  return (
                    <button key={l.id} onClick={() => { setSelectedLetter(l); speak(l.name_ar, 'ar'); }}
                      className={cn('relative flex flex-col items-center gap-0.5 p-2.5 rounded-xl border transition-all active:scale-95',
                        done ? 'bg-green-500/15 border-green-500/30' : 'bg-card border-border/30 hover:border-primary/30'
                      )}>
                      {done && <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center"><Check className="w-2.5 h-2.5 text-white" /></div>}
                      <span className="text-2xl font-bold" dir="rtl">{l.letter}</span>
                      <span className="text-[9px] text-muted-foreground">{l.name_en}</span>
                    </button>
                  );
                })}
              </div>
            )}

            {/* Numbers practice */}
            {practiceMode === 'numbers' && (
              <div className="grid grid-cols-3 gap-2">
                {numbers.map(n => (
                  <button key={n.id} onClick={() => speak(n.word_ar, 'ar')}
                    className="flex flex-col items-center gap-1 p-3 rounded-xl bg-card border border-border/30 hover:border-blue-500/30 active:scale-95">
                    <span className="text-3xl font-bold text-blue-500">{n.arabic}</span>
                    <span className="text-sm font-bold" dir="rtl">{n.word_ar}</span>
                    <span className="text-[10px] text-muted-foreground">{n.word_en}</span>
                  </button>
                ))}
              </div>
            )}

            {/* Vocab practice */}
            {practiceMode === 'vocab' && (
              <div className="space-y-3">
                <div className="flex gap-1.5 overflow-x-auto no-scrollbar">
                  {vocabCategories.map(cat => (
                    <button key={cat} onClick={() => setActiveVocabCat(cat)}
                      className={cn('px-3 py-1.5 rounded-lg text-[10px] font-bold whitespace-nowrap shrink-0',
                        activeVocabCat === cat ? 'bg-purple-500 text-white' : 'bg-card border border-border/30'
                      )}>
                      {t(`cat_${cat}`)}
                    </button>
                  ))}
                </div>
                <div className="space-y-2">
                  {vocab.filter(w => w.category === activeVocabCat).map(w => {
                    const done = progress.completed_vocab.includes(w.id);
                    return (
                      <button key={w.id} onClick={() => { speak(w.word, 'ar'); completeVocab(w.id); }}
                        className={cn('w-full flex items-center gap-3 p-3 rounded-xl border transition-all active:scale-[0.98]',
                          done ? 'bg-green-500/10 border-green-500/30' : 'bg-card border-border/30'
                        )}>
                        <span className="text-2xl">{w.emoji}</span>
                        <div className="flex-1 text-start">
                          <p className="text-base font-bold" dir="rtl">{w.word}</p>
                          <p className="text-[10px] text-muted-foreground">{w.transliteration} — {getVocabMeaning(w)}</p>
                        </div>
                        <Volume2 className="w-4 h-4 text-primary shrink-0" />
                        {done && <Check className="w-4 h-4 text-green-500 shrink-0" />}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Sentences practice */}
            {practiceMode === 'sentences' && (
              <div className="space-y-4">
                {sentences.map((s: any) => (
                  <div key={s.id} className="bg-card rounded-2xl border border-border/30 p-4">
                    <SentenceBuilder
                      wordsAr={s.words_ar}
                      wordsEn={s.words_en}
                      correctSentenceAr={s.sentence_ar}
                      correctSentenceEn={s.sentence_en}
                      onComplete={(ok) => { if (ok) addXP(15); }}
                    />
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Letter detail in practice */}
        {mainTab === 'practice' && selectedLetter && (
          <div className="animate-fade-in space-y-3">
            <button onClick={() => setSelectedLetter(null)} className="flex items-center gap-1 text-sm text-primary font-bold">
              {dir === 'rtl' ? <ArrowRight className="w-4 h-4" /> : <ArrowLeft className="w-4 h-4" />} {t('backToLetters')}
            </button>
            <div className="bg-card rounded-2xl border border-border/30 p-5 text-center">
              <div className="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-3">
                <span className="text-6xl font-bold" dir="rtl">{selectedLetter.letter}</span>
              </div>
              <h3 className="text-xl font-black" dir="rtl">{selectedLetter.name_ar}</h3>
              <p className="text-sm text-muted-foreground">{selectedLetter.name_en} ({selectedLetter.transliteration})</p>
            </div>
            <div className="bg-card rounded-2xl border border-border/30 p-3">
              <div className="grid grid-cols-4 gap-1.5">
                {[{l: t('isolated'), f: selectedLetter.form_isolated}, {l: t('initial'), f: selectedLetter.form_initial}, {l: t('medial'), f: selectedLetter.form_medial}, {l: t('final'), f: selectedLetter.form_final}].map((x, i) => (
                  <div key={i} className="text-center p-2 bg-muted/30 rounded-lg">
                    <span className="text-xl font-bold" dir="rtl">{x.f}</span>
                    <p className="text-[8px] text-muted-foreground">{x.l}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-card rounded-2xl border border-border/30 p-4">
              <h4 className="text-xs font-bold mb-3 flex items-center gap-1.5"><Mic className="w-3.5 h-3.5 text-primary" /> {t('pronunciationCheck')}</h4>
              <PronunciationCheck targetWord={selectedLetter.name_ar} targetTransliteration={selectedLetter.transliteration}
                onResult={(ok) => { if (ok) completeLetter(selectedLetter.id); }} />
            </div>
            {!progress.completed_letters.includes(selectedLetter.id) ? (
              <button onClick={() => { completeLetter(selectedLetter.id); setSelectedLetter(null); }}
                className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-2xl font-bold text-sm flex items-center justify-center gap-2 active:scale-[0.98]">
                <Check className="w-4 h-4" /> {t('markAsLearned')} (+10 XP)
              </button>
            ) : (
              <div className="w-full py-3 bg-green-500/10 text-green-500 rounded-2xl font-bold text-sm flex items-center justify-center gap-2">
                <Check className="w-4 h-4" /> {t('alreadyLearned')} ✅
              </div>
            )}
          </div>
        )}

        {/* ========== GROWTH TREE ========== */}
        {mainTab === 'tree' && (
          <div className="animate-fade-in space-y-4">
            <div className="bg-card rounded-2xl border border-border/30 p-6">
              <GrowthTree level={progress.tree_level} totalXp={progress.total_xp} />
            </div>
            {/* Achievements */}
            <div className="bg-card rounded-2xl border border-border/30 p-4">
              <h3 className="text-sm font-bold mb-3 flex items-center gap-1.5">🏆 {t('achievements')}</h3>
              <div className="space-y-2">
                {[
                  { label: t('firstLetter'), done: progress.completed_letters.length >= 1, emoji: '📝' },
                  { label: t('fiveLetters'), done: progress.completed_letters.length >= 5, emoji: '✋' },
                  { label: t('halfAlphabet'), done: progress.completed_letters.length >= 14, emoji: '🌟' },
                  { label: t('fullAlphabet'), done: progress.completed_letters.length >= 28, emoji: '🏅' },
                  { label: t('tenWords'), done: progress.completed_vocab.length >= 10, emoji: '📖' },
                  { label: t('thirtyDays'), done: progress.completed_days.length >= 30, emoji: '📅' },
                  { label: t('sixtyDays'), done: progress.completed_days.length >= 60, emoji: '🎯' },
                  { label: t('ninetyDays'), done: progress.completed_days.length >= 90, emoji: '👑' },
                ].map((a, i) => (
                  <div key={i} className={cn('flex items-center gap-3 p-2.5 rounded-xl', a.done ? 'bg-amber-500/10' : 'bg-muted/30 opacity-50')}>
                    <span className="text-xl">{a.emoji}</span>
                    <span className={cn('text-xs font-bold', a.done ? 'text-foreground' : 'text-muted-foreground')}>{a.label}</span>
                    {a.done && <Check className="w-4 h-4 text-amber-500 ms-auto" />}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
