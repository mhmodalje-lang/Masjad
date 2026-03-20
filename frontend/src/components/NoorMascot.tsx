import { useState, useCallback, useEffect, useRef } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { Volume2, VolumeX } from 'lucide-react';

interface NoorMascotProps {
  message?: string;
  mood?: 'happy' | 'thinking' | 'celebrating' | 'greeting' | 'sleeping';
  size?: 'sm' | 'md' | 'lg';
  autoSpeak?: boolean;
  className?: string;
  onClick?: () => void;
  storyLanguage?: string; // Override language for story sync
}

const NOOR_MESSAGES: Record<string, Record<string, string>> = {
  greeting: {
    ar: 'مرحباً! أنا نور، صديقك في تعلم العربية!',
    en: 'Hello! I am Noor, your Arabic learning friend!',
    de: 'Hallo! Ich bin Noor, dein Arabisch-Lernfreund!',
    ru: 'Привет! Я Нур, твой друг в изучении арабского!',
    fr: 'Bonjour! Je suis Noor, ton ami pour apprendre l\'arabe!',
    tr: 'Merhaba! Ben Noor, Arapça öğrenme arkadaşın!',
    sv: 'Hej! Jag är Noor, din arabiska-lärande kompis!',
    nl: 'Hallo! Ik ben Noor, je Arabisch leervriend!',
    el: 'Γεια! Είμαι ο Νουρ, ο φίλος σου στην εκμάθηση αραβικών!',
  },
  correct: {
    ar: 'أحسنت! إجابة صحيحة! ⭐',
    en: 'Great job! Correct answer! ⭐',
    de: 'Toll gemacht! Richtige Antwort! ⭐',
    ru: 'Молодец! Правильный ответ! ⭐',
    fr: 'Bravo! Bonne réponse! ⭐',
    tr: 'Aferin! Doğru cevap! ⭐',
    sv: 'Bra jobbat! Rätt svar! ⭐',
    nl: 'Goed gedaan! Juist antwoord! ⭐',
    el: 'Μπράβο! Σωστή απάντηση! ⭐',
  },
  wrong: {
    ar: 'لا بأس، حاول مرة أخرى! 💪',
    en: 'No worries, try again! 💪',
    de: 'Keine Sorge, versuch es nochmal! 💪',
    ru: 'Не переживай, попробуй ещё раз! 💪',
    fr: 'Pas de souci, réessaie! 💪',
    tr: 'Sorun değil, tekrar dene! 💪',
    sv: 'Inga problem, försök igen! 💪',
    nl: 'Geen zorgen, probeer het opnieuw! 💪',
    el: 'Μην ανησυχείς, δοκίμασε ξανά! 💪',
  },
  encourage: {
    ar: 'استمر! أنت تتعلم بسرعة! 🌟',
    en: 'Keep going! You are learning fast! 🌟',
    de: 'Weiter so! Du lernst schnell! 🌟',
    ru: 'Продолжай! Ты быстро учишься! 🌟',
    fr: 'Continue! Tu apprends vite! 🌟',
    tr: 'Devam et! Hızlı öğreniyorsun! 🌟',
    sv: 'Fortsätt! Du lär dig snabbt! 🌟',
    nl: 'Ga door! Je leert snel! 🌟',
    el: 'Συνέχισε! Μαθαίνεις γρήγορα! 🌟',
  },
  letterIntro: {
    ar: 'هيا نتعلم حرفاً جديداً!',
    en: 'Let\'s learn a new letter!',
    de: 'Lass uns einen neuen Buchstaben lernen!',
    ru: 'Давай выучим новую букву!',
    fr: 'Apprenons une nouvelle lettre!',
    tr: 'Yeni bir harf öğrenelim!',
    sv: 'Låt oss lära oss en ny bokstav!',
    nl: 'Laten we een nieuwe letter leren!',
    el: 'Ας μάθουμε ένα νέο γράμμα!',
  },
};

// TTS language map
const TTS_LANG_MAP: Record<string, string> = {
  ar: 'ar-SA',
  en: 'en-US',
  de: 'de-DE',
  ru: 'ru-RU',
  fr: 'fr-FR',
  tr: 'tr-TR',
  sv: 'sv-SE',
  nl: 'nl-NL',
  el: 'el-GR',
};

export function useNoorTTS() {
  const { locale } = useLocale();
  const [isSpeaking, setIsSpeaking] = useState(false);
  const synthRef = useRef<SpeechSynthesis | null>(null);

  useEffect(() => {
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      synthRef.current = window.speechSynthesis;
    }
  }, []);

  const speak = useCallback((text: string, lang?: string) => {
    if (!synthRef.current) return;
    synthRef.current.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const targetLang = lang || locale;
    utterance.lang = TTS_LANG_MAP[targetLang] || 'ar-SA';
    utterance.rate = 0.85;
    utterance.pitch = 1.2;
    
    // Try to find a native voice for the target language
    const voices = synthRef.current.getVoices();
    const langCode = TTS_LANG_MAP[targetLang] || 'ar-SA';
    const nativeVoice = voices.find(v => v.lang === langCode) || voices.find(v => v.lang.startsWith(targetLang));
    if (nativeVoice) utterance.voice = nativeVoice;
    
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    synthRef.current.speak(utterance);
  }, [locale]);

  const stop = useCallback(() => {
    if (synthRef.current) {
      synthRef.current.cancel();
      setIsSpeaking(false);
    }
  }, []);

  return { speak, stop, isSpeaking };
}

export function getNoorMessage(key: string, locale: string): string {
  return NOOR_MESSAGES[key]?.[locale] || NOOR_MESSAGES[key]?.['en'] || '';
}

export default function NoorMascot({ message, mood = 'happy', size = 'md', autoSpeak = false, className, onClick, storyLanguage }: NoorMascotProps) {
  const { locale } = useLocale();
  const { speak, stop, isSpeaking } = useNoorTTS();
  const [isAnimating, setIsAnimating] = useState(false);
  const effectiveLang = storyLanguage || locale;
  const displayMessage = message || getNoorMessage('greeting', effectiveLang);

  useEffect(() => {
    if (autoSpeak && displayMessage) {
      const timer = setTimeout(() => speak(displayMessage, effectiveLang), 500);
      return () => clearTimeout(timer);
    }
  }, [autoSpeak, displayMessage, speak, effectiveLang]);

  const handleClick = () => {
    setIsAnimating(true);
    setTimeout(() => setIsAnimating(false), 600);
    if (onClick) onClick();
    else if (displayMessage) speak(displayMessage, effectiveLang);
  };

  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24',
    lg: 'w-32 h-32',
  };

  const moodEmoji = {
    happy: '😊',
    thinking: '🤔',
    celebrating: '🎉',
    greeting: '👋',
    sleeping: '😴',
  };

  // Eye states based on mood
  const eyeStyle = mood === 'sleeping' ? 'scale-y-[0.1]' : mood === 'celebrating' ? 'scale-110' : '';

  return (
    <div className={cn('flex flex-col items-center gap-2', className)}>
      {/* Speech bubble */}
      {displayMessage && (
        <div className="relative max-w-[250px] animate-fade-in">
          <div className="bg-white dark:bg-slate-800 rounded-2xl px-4 py-2.5 shadow-lg border border-primary/20 text-sm leading-relaxed text-foreground">
            <p dir="auto" className="text-center">{displayMessage}</p>
          </div>
          <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-white dark:bg-slate-800 border-b border-r border-primary/20 rotate-45" />
        </div>
      )}
      
      {/* Noor character */}
      <button
        onClick={handleClick}
        className={cn(
          'relative cursor-pointer transition-transform select-none',
          sizeClasses[size],
          isAnimating && 'animate-bounce',
          'hover:scale-105 active:scale-95'
        )}
        aria-label="Noor mascot"
      >
        {/* Body - Glowing star shape */}
        <div className="absolute inset-0 rounded-full bg-gradient-to-br from-amber-300 via-yellow-400 to-orange-400 shadow-lg shadow-amber-400/40 animate-pulse" style={{ animationDuration: '3s' }}>
          {/* Inner glow */}
          <div className="absolute inset-2 rounded-full bg-gradient-to-br from-amber-200 to-yellow-300">
            {/* Face */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              {/* Eyes */}
              <div className="flex gap-2 mb-1">
                <div className={cn('w-2 h-2 rounded-full bg-slate-800 transition-transform', eyeStyle)} />
                <div className={cn('w-2 h-2 rounded-full bg-slate-800 transition-transform', eyeStyle)} />
              </div>
              {/* Mouth */}
              <div className={cn(
                'transition-all',
                mood === 'happy' || mood === 'celebrating' ? 'w-4 h-2 border-b-2 border-slate-800 rounded-b-full' :
                mood === 'thinking' ? 'w-2 h-2 rounded-full border-2 border-slate-800' :
                mood === 'sleeping' ? 'w-3 h-0.5 bg-slate-800 rounded-full' :
                'w-4 h-2 border-b-2 border-slate-800 rounded-b-full'
              )} />
            </div>
          </div>
          {/* Star points decoration */}
          <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-3 h-3 bg-amber-300 rotate-45" />
          <div className="absolute -left-1 top-1/2 -translate-y-1/2 w-3 h-3 bg-amber-300 rotate-45" />
          <div className="absolute -right-1 top-1/2 -translate-y-1/2 w-3 h-3 bg-amber-300 rotate-45" />
        </div>

        {/* Sparkles around character */}
        {mood === 'celebrating' && (
          <>
            <span className="absolute -top-2 -right-2 text-xs animate-ping">✨</span>
            <span className="absolute -top-1 -left-3 text-xs animate-ping" style={{ animationDelay: '0.3s' }}>⭐</span>
            <span className="absolute -bottom-2 right-0 text-xs animate-ping" style={{ animationDelay: '0.6s' }}>🌟</span>
          </>
        )}
      </button>

      {/* TTS button */}
      <button
        onClick={(e) => { e.stopPropagation(); isSpeaking ? stop() : speak(displayMessage); }}
        className={cn(
          'flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold transition-all',
          isSpeaking
            ? 'bg-red-500/10 text-red-500 border border-red-500/30'
            : 'bg-primary/10 text-primary border border-primary/30 hover:bg-primary/20'
        )}
      >
        {isSpeaking ? <VolumeX className="w-3 h-3" /> : <Volume2 className="w-3 h-3" />}
        {isSpeaking ? '⏹' : '🔊'}
      </button>
    </div>
  );
}
