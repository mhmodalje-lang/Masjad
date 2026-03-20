import { useState, useEffect, useCallback, useMemo } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import NoorMascot, { useNoorTTS, getNoorMessage } from '@/components/NoorMascot';
import { ChevronLeft, Star, Trophy, BookOpen, Gamepad2, Volume2, Check, X, Lock, Sparkles, ArrowLeft, ArrowRight, GraduationCap, Baby, School } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface ArabicLetter {
  id: number;
  letter: string;
  name_ar: string;
  name_en: string;
  transliteration: string;
  form_isolated: string;
  form_initial: string;
  form_medial: string;
  form_final: string;
  example_word: string;
  example_meaning: string;
  audio_hint: string;
}

interface QuranWord {
  id: number;
  word: string;
  transliteration: string;
  meaning: string;
  surah: string;
  ayah: number;
}

interface Progress {
  completed_letters: number[];
  completed_vocab: number[];
  completed_levels: number[];
  stars: number;
  streak: number;
  total_xp: number;
  level: number;
  golden_bricks: number;
}

type Tab = 'curriculum' | 'letters' | 'vocab' | 'quiz';

// Curriculum levels
function getCurriculumLevels(t: (k: string) => string) {
  return [
    {
      id: 1, titleKey: 'level1Title', descKey: 'level1Desc', icon: '🌱', color: 'from-green-500/20 to-emerald-500/10',
      letterRange: [1, 7], xpRequired: 0, skills: ['level1Skill1', 'level1Skill2', 'level1Skill3']
    },
    {
      id: 2, titleKey: 'level2Title', descKey: 'level2Desc', icon: '🌿', color: 'from-blue-500/20 to-cyan-500/10',
      letterRange: [8, 14], xpRequired: 50, skills: ['level2Skill1', 'level2Skill2', 'level2Skill3']
    },
    {
      id: 3, titleKey: 'level3Title', descKey: 'level3Desc', icon: '🌳', color: 'from-purple-500/20 to-violet-500/10',
      letterRange: [15, 21], xpRequired: 120, skills: ['level3Skill1', 'level3Skill2', 'level3Skill3']
    },
    {
      id: 4, titleKey: 'level4Title', descKey: 'level4Desc', icon: '⭐', color: 'from-amber-500/20 to-orange-500/10',
      letterRange: [22, 28], xpRequired: 200, skills: ['level4Skill1', 'level4Skill2', 'level4Skill3']
    },
    {
      id: 5, titleKey: 'level5Title', descKey: 'level5Desc', icon: '🏆', color: 'from-yellow-500/20 to-amber-500/10',
      letterRange: [0, 0], xpRequired: 300, skills: ['level5Skill1', 'level5Skill2', 'level5Skill3']
    },
  ];
}

export default function ArabicAcademy() {
  const { t, dir, locale } = useLocale();
  const navigate = useNavigate();
  const { speak } = useNoorTTS();

  const [activeTab, setActiveTab] = useState<Tab>('curriculum');
  const [letters, setLetters] = useState<ArabicLetter[]>([]);
  const [vocab, setVocab] = useState<QuranWord[]>([]);
  const [selectedLetter, setSelectedLetter] = useState<ArabicLetter | null>(null);
  const [activeLevelId, setActiveLevelId] = useState<number | null>(null);
  const [progress, setProgress] = useState<Progress>({
    completed_letters: [],
    completed_vocab: [],
    completed_levels: [],
    stars: 0,
    streak: 0,
    total_xp: 0,
    level: 1,
    golden_bricks: 0,
  });
  const [quizState, setQuizState] = useState<{
    letter: ArabicLetter | null;
    options: { letter: string; name_ar: string; name_en: string; correct: boolean }[];
    answered: boolean;
    correct: boolean;
    score: number;
    total: number;
  } | null>(null);
  const [noorMood, setNoorMood] = useState<'happy' | 'thinking' | 'celebrating' | 'greeting'>('greeting');
  const [noorMsg, setNoorMsg] = useState('');
  const [loading, setLoading] = useState(true);

  const curriculumLevels = getCurriculumLevels(t);

  useEffect(() => {
    async function loadData() {
      try {
        const [lettersRes, vocabRes] = await Promise.all([
          fetch(`${BACKEND_URL}/api/arabic-academy/letters`),
          fetch(`${BACKEND_URL}/api/arabic-academy/vocab`),
        ]);
        const lettersData = await lettersRes.json();
        const vocabData = await vocabRes.json();
        if (lettersData.success) setLetters(lettersData.letters);
        if (vocabData.success) setVocab(vocabData.words);
      } catch (e) {
        console.error('Failed to load academy data:', e);
      }
      const saved = localStorage.getItem('arabic-academy-progress');
      if (saved) {
        try { setProgress(JSON.parse(saved)); } catch {}
      }
      setLoading(false);
    }
    loadData();
  }, []);

  const saveProgress = useCallback((newProgress: Progress) => {
    setProgress(newProgress);
    localStorage.setItem('arabic-academy-progress', JSON.stringify(newProgress));
  }, []);

  const completeLetter = useCallback((letterId: number) => {
    if (progress.completed_letters.includes(letterId)) return;
    const newProgress = {
      ...progress,
      completed_letters: [...progress.completed_letters, letterId],
      stars: progress.stars + 1,
      total_xp: progress.total_xp + 10,
      golden_bricks: progress.golden_bricks + 1,
      level: Math.floor((progress.total_xp + 10) / 50) + 1,
    };
    saveProgress(newProgress);
    setNoorMood('celebrating');
    setNoorMsg(getNoorMessage('correct', locale));
    toast.success(`⭐ +1 ${t('star')}! +10 XP`);
  }, [progress, saveProgress, locale, t]);

  const completeVocab = useCallback((wordId: number) => {
    if (progress.completed_vocab.includes(wordId)) return;
    const newProgress = {
      ...progress,
      completed_vocab: [...progress.completed_vocab, wordId],
      total_xp: progress.total_xp + 5,
      level: Math.floor((progress.total_xp + 5) / 50) + 1,
    };
    saveProgress(newProgress);
  }, [progress, saveProgress]);

  const startQuiz = useCallback(async (levelLetters?: ArabicLetter[]) => {
    const pool = levelLetters || letters;
    if (pool.length === 0) return;
    const letter = pool[Math.floor(Math.random() * pool.length)];
    try {
      const res = await fetch(`${BACKEND_URL}/api/arabic-academy/quiz/${letter.id}`);
      const data = await res.json();
      if (data.success) {
        setQuizState({
          letter: data.quiz.question_letter,
          options: data.quiz.options,
          answered: false,
          correct: false,
          score: quizState?.score || 0,
          total: (quizState?.total || 0),
        });
        setNoorMood('thinking');
        setNoorMsg(getNoorMessage('letterIntro', locale));
        setActiveTab('quiz');
      }
    } catch (e) {
      console.error('Quiz error:', e);
    }
  }, [letters, locale, quizState]);

  const answerQuiz = useCallback((isCorrect: boolean) => {
    if (!quizState) return;
    setQuizState({
      ...quizState,
      answered: true,
      correct: isCorrect,
      score: isCorrect ? quizState.score + 1 : quizState.score,
      total: quizState.total + 1,
    });
    if (isCorrect) {
      completeLetter(quizState.letter!.id);
      setNoorMood('celebrating');
      setNoorMsg(getNoorMessage('correct', locale));
    } else {
      setNoorMood('happy');
      setNoorMsg(getNoorMessage('wrong', locale));
    }
  }, [quizState, completeLetter, locale]);

  const pronounceLetter = useCallback((letter: ArabicLetter) => {
    speak(letter.name_ar, 'ar');
  }, [speak]);

  const levelProgress = useMemo(() => {
    const xpForLevel = progress.total_xp % 50;
    return (xpForLevel / 50) * 100;
  }, [progress.total_xp]);

  const getLevelLetters = (level: typeof curriculumLevels[0]) => {
    if (level.letterRange[0] === 0) return [];
    return letters.filter(l => l.id >= level.letterRange[0] && l.id <= level.letterRange[1]);
  };

  const getLevelCompletion = (level: typeof curriculumLevels[0]) => {
    const levelLetters = getLevelLetters(level);
    if (levelLetters.length === 0) return 0;
    const completed = levelLetters.filter(l => progress.completed_letters.includes(l.id)).length;
    return Math.round((completed / levelLetters.length) * 100);
  };

  const isLevelUnlocked = (level: typeof curriculumLevels[0]) => {
    return progress.total_xp >= level.xpRequired;
  };

  const tabs: { key: Tab; icon: any; labelKey: string }[] = [
    { key: 'curriculum', icon: GraduationCap, labelKey: 'curriculum' },
    { key: 'letters', icon: BookOpen, labelKey: 'arabicLetters' },
    { key: 'vocab', icon: Sparkles, labelKey: 'quranVocab' },
    { key: 'quiz', icon: Gamepad2, labelKey: 'quiz' },
  ];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-28 bg-gradient-to-b from-amber-50/50 via-background to-background dark:from-amber-950/20" dir={dir}>
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center justify-between">
        <button onClick={() => navigate(-1)} className="p-2 rounded-xl hover:bg-muted/50">
          {dir === 'rtl' ? <ArrowRight className="h-5 w-5" /> : <ArrowLeft className="h-5 w-5" />}
        </button>
        <h1 className="text-base font-black text-foreground flex items-center gap-2">
          <span>👶</span> {t('arabicAcademy')}
        </h1>
        <div className="flex items-center gap-1">
          <span className="text-sm font-bold text-amber-500">⭐ {progress.stars}</span>
        </div>
      </div>

      {/* Noor Mascot */}
      <div className="px-4 pt-3 pb-1 flex justify-center">
        <NoorMascot
          message={noorMsg || getNoorMessage('greeting', locale)}
          mood={noorMood}
          size="sm"
        />
      </div>

      {/* Progress Bar */}
      <div className="px-4 mb-3">
        <div className="bg-card rounded-2xl border border-border/30 p-3">
          <div className="flex items-center justify-between mb-1.5">
            <div className="flex items-center gap-2">
              <Trophy className="w-4 h-4 text-amber-500" />
              <span className="text-xs font-bold">{t('level')} {progress.level}</span>
            </div>
            <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
              <span>🧱 {progress.golden_bricks}</span>
              <span>⚡ {progress.total_xp} XP</span>
            </div>
          </div>
          <div className="w-full h-2.5 bg-muted rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-amber-400 to-orange-500 rounded-full transition-all duration-500" style={{ width: `${levelProgress}%` }} />
          </div>
          <div className="flex justify-between mt-1 text-[9px] text-muted-foreground">
            <span>{progress.completed_letters.length}/28 {t('lettersCompleted')}</span>
            <span>{progress.completed_vocab.length}/20 {t('wordsLearned')}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="px-4 mb-3 flex gap-1.5">
        {tabs.map(tab => (
          <button
            key={tab.key}
            onClick={() => {
              if (tab.key === 'quiz') startQuiz();
              else { setActiveTab(tab.key); setSelectedLetter(null); setActiveLevelId(null); }
            }}
            className={cn(
              'flex-1 flex items-center justify-center gap-1 py-2 rounded-xl text-[11px] font-bold transition-all',
              activeTab === tab.key
                ? 'bg-primary text-primary-foreground shadow-lg'
                : 'bg-card border border-border/30 text-muted-foreground hover:text-foreground'
            )}
          >
            <tab.icon className="w-3.5 h-3.5" />
            {t(tab.labelKey)}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="px-4">

        {/* ===================== CURRICULUM TAB ===================== */}
        {activeTab === 'curriculum' && !activeLevelId && (
          <div className="space-y-3">
            <div className="text-center mb-2">
              <h2 className="text-sm font-bold text-foreground">{t('learningPath')}</h2>
              <p className="text-[10px] text-muted-foreground">{t('learningPathDesc')}</p>
            </div>
            {curriculumLevels.map((level, idx) => {
              const unlocked = isLevelUnlocked(level);
              const completion = getLevelCompletion(level);
              return (
                <button
                  key={level.id}
                  disabled={!unlocked}
                  onClick={() => {
                    if (level.id === 5) {
                      setActiveTab('vocab');
                    } else {
                      setActiveLevelId(level.id);
                    }
                  }}
                  className={cn(
                    'w-full p-4 rounded-2xl border transition-all text-start relative overflow-hidden',
                    unlocked
                      ? 'bg-card border-border/30 hover:border-primary/30 active:scale-[0.98]'
                      : 'bg-muted/30 border-border/10 opacity-60'
                  )}
                >
                  {/* Background gradient */}
                  <div className={cn('absolute inset-0 bg-gradient-to-r opacity-30', level.color)} />
                  
                  <div className="relative flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-background/80 flex items-center justify-center text-2xl shrink-0">
                      {unlocked ? level.icon : <Lock className="w-5 h-5 text-muted-foreground" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-0.5">
                        <span className="text-sm font-bold text-foreground">{t(level.titleKey)}</span>
                        {completion === 100 && <Check className="w-4 h-4 text-green-500" />}
                      </div>
                      <p className="text-[10px] text-muted-foreground line-clamp-1">{t(level.descKey)}</p>
                      {unlocked && level.id !== 5 && (
                        <div className="mt-1.5 flex items-center gap-2">
                          <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                            <div className="h-full bg-primary rounded-full transition-all" style={{ width: `${completion}%` }} />
                          </div>
                          <span className="text-[9px] font-bold text-primary">{completion}%</span>
                        </div>
                      )}
                      {!unlocked && (
                        <p className="text-[9px] text-amber-500 mt-1">🔒 {t('requiresXP')}: {level.xpRequired} XP</p>
                      )}
                    </div>
                  </div>

                  {/* Skills preview */}
                  {unlocked && (
                    <div className="relative flex gap-1.5 mt-2 flex-wrap">
                      {level.skills.map((sk, i) => (
                        <span key={i} className="text-[9px] px-2 py-0.5 bg-primary/10 text-primary rounded-full font-medium">
                          {t(sk)}
                        </span>
                      ))}
                    </div>
                  )}
                </button>
              );
            })}

            {/* Connection lines */}
            <div className="flex justify-center">
              <div className="h-2 w-0.5 bg-border/30" />
            </div>
          </div>
        )}

        {/* ===================== LEVEL DETAIL ===================== */}
        {activeTab === 'curriculum' && activeLevelId && !selectedLetter && (() => {
          const level = curriculumLevels.find(l => l.id === activeLevelId);
          if (!level) return null;
          const levelLetters = getLevelLetters(level);
          return (
            <div className="animate-fade-in">
              <button onClick={() => setActiveLevelId(null)} className="flex items-center gap-1 text-sm text-primary mb-3 font-bold">
                {dir === 'rtl' ? <ArrowRight className="w-4 h-4" /> : <ArrowLeft className="w-4 h-4" />}
                {t('backToCurriculum')}
              </button>

              <div className="bg-card rounded-2xl border border-border/30 p-4 mb-4 text-center">
                <span className="text-3xl">{level.icon}</span>
                <h2 className="text-lg font-black mt-2">{t(level.titleKey)}</h2>
                <p className="text-xs text-muted-foreground">{t(level.descKey)}</p>
              </div>

              <div className="grid grid-cols-4 gap-2.5">
                {levelLetters.map(letter => {
                  const isCompleted = progress.completed_letters.includes(letter.id);
                  return (
                    <button
                      key={letter.id}
                      onClick={() => { setSelectedLetter(letter); pronounceLetter(letter); }}
                      className={cn(
                        'relative flex flex-col items-center justify-center gap-1 p-3 rounded-2xl border transition-all active:scale-95',
                        isCompleted
                          ? 'bg-gradient-to-br from-green-500/20 to-emerald-500/10 border-green-500/30'
                          : 'bg-card border-border/30 hover:border-primary/30 hover:shadow-md'
                      )}
                    >
                      {isCompleted && (
                        <div className="absolute -top-1 -right-1 w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
                          <Check className="w-3 h-3 text-white" />
                        </div>
                      )}
                      <span className="text-3xl font-bold text-foreground" dir="rtl">{letter.letter}</span>
                      <span className="text-[10px] text-muted-foreground">{letter.name_en}</span>
                    </button>
                  );
                })}
              </div>

              {/* Level quiz */}
              <button
                onClick={() => startQuiz(levelLetters)}
                className="w-full mt-4 py-3 bg-primary text-primary-foreground rounded-2xl font-bold text-sm flex items-center justify-center gap-2 active:scale-[0.98]"
              >
                <Gamepad2 className="w-4 h-4" /> {t('levelQuiz')}
              </button>
            </div>
          );
        })()}

        {/* ===================== LETTER DETAIL (shared) ===================== */}
        {(activeTab === 'letters' || activeTab === 'curriculum') && selectedLetter && (
          <div className="animate-fade-in">
            <button
              onClick={() => setSelectedLetter(null)}
              className="flex items-center gap-1 text-sm text-primary mb-4 font-bold"
            >
              {dir === 'rtl' ? <ArrowRight className="w-4 h-4" /> : <ArrowLeft className="w-4 h-4" />}
              {t('backToLetters')}
            </button>

            <div className="bg-card rounded-3xl border border-border/30 p-6 text-center mb-4">
              <div className="w-28 h-28 mx-auto rounded-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-4">
                <span className="text-7xl font-bold" dir="rtl">{selectedLetter.letter}</span>
              </div>
              <h2 className="text-2xl font-black text-foreground mb-1" dir="rtl">{selectedLetter.name_ar}</h2>
              <p className="text-sm text-muted-foreground mb-2">{selectedLetter.name_en} ({selectedLetter.transliteration})</p>
              <button
                onClick={() => pronounceLetter(selectedLetter)}
                className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-bold hover:bg-primary/20 transition-all"
              >
                <Volume2 className="w-4 h-4" /> {t('listenPronunciation')}
              </button>
            </div>

            <div className="bg-card rounded-2xl border border-border/30 p-4 mb-4">
              <h3 className="text-sm font-bold mb-3">{t('letterForms')}</h3>
              <div className="grid grid-cols-4 gap-2">
                {[
                  { label: t('isolated'), form: selectedLetter.form_isolated },
                  { label: t('initial'), form: selectedLetter.form_initial },
                  { label: t('medial'), form: selectedLetter.form_medial },
                  { label: t('final'), form: selectedLetter.form_final },
                ].map((f, i) => (
                  <div key={i} className="flex flex-col items-center gap-1 p-2 bg-muted/30 rounded-xl">
                    <span className="text-2xl font-bold" dir="rtl">{f.form}</span>
                    <span className="text-[9px] text-muted-foreground">{f.label}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-card rounded-2xl border border-border/30 p-4 mb-4">
              <h3 className="text-sm font-bold mb-2">{t('exampleWord')}</h3>
              <div className="flex items-center justify-center gap-4">
                <span className="text-4xl font-bold text-primary" dir="rtl">{selectedLetter.example_word}</span>
                <span className="text-sm text-muted-foreground">= {selectedLetter.example_meaning}</span>
              </div>
            </div>

            {!progress.completed_letters.includes(selectedLetter.id) ? (
              <button
                onClick={() => { completeLetter(selectedLetter.id); setSelectedLetter(null); }}
                className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-2xl font-bold text-sm flex items-center justify-center gap-2 active:scale-[0.98] transition-transform"
              >
                <Check className="w-4 h-4" /> {t('markAsLearned')} (+10 XP ⭐)
              </button>
            ) : (
              <div className="w-full py-3 bg-green-500/10 text-green-500 rounded-2xl font-bold text-sm flex items-center justify-center gap-2">
                <Check className="w-4 h-4" /> {t('alreadyLearned')} ✅
              </div>
            )}
          </div>
        )}

        {/* ===================== ALL LETTERS TAB ===================== */}
        {activeTab === 'letters' && !selectedLetter && (
          <div className="grid grid-cols-4 gap-2.5">
            {letters.map(letter => {
              const isCompleted = progress.completed_letters.includes(letter.id);
              return (
                <button
                  key={letter.id}
                  onClick={() => { setSelectedLetter(letter); pronounceLetter(letter); }}
                  className={cn(
                    'relative flex flex-col items-center justify-center gap-1 p-3 rounded-2xl border transition-all active:scale-95',
                    isCompleted
                      ? 'bg-gradient-to-br from-green-500/20 to-emerald-500/10 border-green-500/30'
                      : 'bg-card border-border/30 hover:border-primary/30 hover:shadow-md'
                  )}
                >
                  {isCompleted && (
                    <div className="absolute -top-1 -right-1 w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
                      <Check className="w-3 h-3 text-white" />
                    </div>
                  )}
                  <span className="text-3xl font-bold text-foreground" dir="rtl">{letter.letter}</span>
                  <span className="text-[10px] text-muted-foreground">{letter.name_en}</span>
                </button>
              );
            })}
          </div>
        )}

        {/* ===================== VOCAB TAB ===================== */}
        {activeTab === 'vocab' && (
          <div className="space-y-2">
            {vocab.map(word => {
              const isCompleted = progress.completed_vocab.includes(word.id);
              return (
                <button
                  key={word.id}
                  onClick={() => { speak(word.word, 'ar'); completeVocab(word.id); }}
                  className={cn(
                    'w-full flex items-center gap-4 p-4 rounded-2xl border transition-all active:scale-[0.98]',
                    isCompleted
                      ? 'bg-gradient-to-r from-green-500/10 to-emerald-500/5 border-green-500/30'
                      : 'bg-card border-border/30 hover:border-primary/30'
                  )}
                >
                  <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                    <span className="text-xl font-bold text-primary" dir="rtl">{word.word.slice(0, 2)}</span>
                  </div>
                  <div className="flex-1 text-start">
                    <p className="text-lg font-bold text-foreground" dir="rtl">{word.word}</p>
                    <p className="text-xs text-muted-foreground">{word.transliteration} — {word.meaning}</p>
                    {word.surah !== 'Various' && (
                      <p className="text-[10px] text-primary/70">📖 {word.surah}:{word.ayah}</p>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <Volume2 className="w-4 h-4 text-primary" />
                    {isCompleted && <Check className="w-4 h-4 text-green-500" />}
                  </div>
                </button>
              );
            })}
          </div>
        )}

        {/* ===================== QUIZ TAB ===================== */}
        {activeTab === 'quiz' && quizState && (
          <div className="animate-fade-in">
            {/* Score */}
            {quizState.total > 0 && (
              <div className="text-center mb-3">
                <span className="text-xs font-bold text-primary bg-primary/10 px-3 py-1 rounded-full">
                  {t('score')}: {quizState.score}/{quizState.total}
                </span>
              </div>
            )}

            <div className="bg-card rounded-3xl border border-border/30 p-6 text-center mb-6">
              <p className="text-sm text-muted-foreground mb-4">{t('whatIsThisLetter')}</p>
              <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-4">
                <span className="text-8xl font-bold" dir="rtl">{quizState.letter?.letter}</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 mb-4">
              {quizState.options.map((opt, i) => {
                const isCorrectOpt = opt.correct;
                const showResult = quizState.answered;
                return (
                  <button
                    key={i}
                    onClick={() => !quizState.answered && answerQuiz(isCorrectOpt)}
                    disabled={quizState.answered}
                    className={cn(
                      'p-4 rounded-2xl border text-center transition-all active:scale-95',
                      showResult && isCorrectOpt && 'bg-green-500/20 border-green-500',
                      showResult && !isCorrectOpt && 'bg-red-500/10 border-red-500/30 opacity-50',
                      !showResult && 'bg-card border-border/30 hover:border-primary/40 hover:shadow-md'
                    )}
                  >
                    <span className="text-2xl font-bold block mb-1" dir="rtl">{opt.name_ar}</span>
                    <span className="text-xs text-muted-foreground">{opt.name_en}</span>
                    {showResult && isCorrectOpt && <Check className="w-5 h-5 text-green-500 mx-auto mt-1" />}
                    {showResult && !isCorrectOpt && <X className="w-5 h-5 text-red-400 mx-auto mt-1" />}
                  </button>
                );
              })}
            </div>

            {quizState.answered && (
              <button
                onClick={() => startQuiz()}
                className="w-full py-3 bg-primary text-primary-foreground rounded-2xl font-bold text-sm flex items-center justify-center gap-2 active:scale-[0.98]"
              >
                <Gamepad2 className="w-4 h-4" /> {t('nextQuestion')}
              </button>
            )}
          </div>
        )}

        {activeTab === 'quiz' && !quizState && (
          <div className="text-center py-12">
            <Gamepad2 className="w-16 h-16 text-muted-foreground/30 mx-auto mb-4" />
            <p className="text-sm text-muted-foreground mb-4">{t('quizDescription')}</p>
            <button
              onClick={() => startQuiz()}
              className="px-8 py-3 bg-primary text-primary-foreground rounded-2xl font-bold text-sm active:scale-[0.98]"
            >
              {t('startQuiz')}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
