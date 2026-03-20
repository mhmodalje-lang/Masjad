import { useState, useCallback, useRef, useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { Mic, MicOff, Volume2, Check, X, RotateCcw } from 'lucide-react';
import { useNoorTTS, getNoorMessage } from '@/components/NoorMascot';

interface PronunciationCheckProps {
  targetWord: string;
  targetTransliteration: string;
  onResult: (correct: boolean) => void;
  className?: string;
}

// Extend Window for SpeechRecognition
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

export default function PronunciationCheck({ targetWord, targetTransliteration, onResult, className }: PronunciationCheckProps) {
  const { t, locale } = useLocale();
  const { speak } = useNoorTTS();
  const [isListening, setIsListening] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [supported, setSupported] = useState(true);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSupported(false);
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'ar-SA';
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 5;

    recognition.onresult = (event: any) => {
      const results: string[] = [];
      for (let i = 0; i < event.results[0].length; i++) {
        results.push(event.results[0][i].transcript.trim());
      }
      const spokenText = results.join(' | ');
      setResult(spokenText);
      
      // Check if any result matches the target
      const normalized = (s: string) => s.replace(/[\u064B-\u065F\u0670]/g, '').replace(/\s+/g, '').toLowerCase();
      const targetNorm = normalized(targetWord);
      const match = results.some(r => {
        const rNorm = normalized(r);
        return rNorm.includes(targetNorm) || targetNorm.includes(rNorm) || 
               levenshteinDistance(rNorm, targetNorm) <= Math.max(2, Math.floor(targetNorm.length * 0.3));
      });
      
      setIsCorrect(match);
      onResult(match);
      
      if (match) {
        speak(getNoorMessage('correct', locale), locale);
      } else {
        speak(getNoorMessage('wrong', locale), locale);
      }
      setIsListening(false);
    };

    recognition.onerror = () => {
      setIsListening(false);
      setResult(null);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  }, [targetWord, locale, onResult, speak]);

  const startListening = useCallback(() => {
    if (!recognitionRef.current) return;
    setResult(null);
    setIsCorrect(null);
    setIsListening(true);
    try {
      recognitionRef.current.start();
    } catch (e) {
      setIsListening(false);
    }
  }, []);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsListening(false);
  }, []);

  const listenToTarget = useCallback(() => {
    speak(targetWord, 'ar');
  }, [speak, targetWord]);

  const reset = useCallback(() => {
    setResult(null);
    setIsCorrect(null);
  }, []);

  if (!supported) {
    return (
      <div className={cn('text-center p-4 bg-amber-500/10 rounded-2xl border border-amber-500/20', className)}>
        <p className="text-xs text-amber-600">{t('speechNotSupported')}</p>
        <p className="text-[10px] text-muted-foreground mt-1">{t('useChromeForSpeech')}</p>
      </div>
    );
  }

  return (
    <div className={cn('flex flex-col items-center gap-3', className)}>
      {/* Listen to correct pronunciation */}
      <button
        onClick={listenToTarget}
        className="flex items-center gap-2 px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-bold hover:bg-primary/20"
      >
        <Volume2 className="w-4 h-4" />
        {t('listenFirst')}
      </button>

      {/* Target word display */}
      <div className="text-center">
        <p className="text-3xl font-bold" dir="rtl">{targetWord}</p>
        <p className="text-xs text-muted-foreground mt-1">{targetTransliteration}</p>
      </div>

      {/* Microphone button */}
      <button
        onClick={isListening ? stopListening : startListening}
        className={cn(
          'w-20 h-20 rounded-full flex items-center justify-center transition-all shadow-lg active:scale-95',
          isListening
            ? 'bg-red-500 text-white animate-pulse shadow-red-500/40'
            : isCorrect === true
            ? 'bg-green-500 text-white shadow-green-500/40'
            : isCorrect === false
            ? 'bg-amber-500 text-white shadow-amber-500/40'
            : 'bg-primary text-primary-foreground shadow-primary/40 hover:shadow-xl'
        )}
      >
        {isListening ? (
          <MicOff className="w-8 h-8" />
        ) : isCorrect === true ? (
          <Check className="w-8 h-8" />
        ) : isCorrect === false ? (
          <X className="w-8 h-8" />
        ) : (
          <Mic className="w-8 h-8" />
        )}
      </button>

      <p className="text-xs text-muted-foreground">
        {isListening ? t('listening') : isCorrect === null ? t('tapToSpeak') : ''}
      </p>

      {/* Result */}
      {result !== null && (
        <div className={cn(
          'w-full p-3 rounded-xl text-center text-sm font-bold',
          isCorrect ? 'bg-green-500/10 text-green-500' : 'bg-amber-500/10 text-amber-600'
        )}>
          {isCorrect ? (
            <p>✅ {t('excellentPronunciation')}</p>
          ) : (
            <p>💪 {t('tryAgainSoftly')}</p>
          )}
          {!isCorrect && (
            <button onClick={reset} className="mt-2 flex items-center gap-1 mx-auto text-xs text-primary">
              <RotateCcw className="w-3 h-3" /> {t('tryAgain')}
            </button>
          )}
        </div>
      )}
    </div>
  );
}

function levenshteinDistance(a: string, b: string): number {
  const m = a.length, n = b.length;
  const dp: number[][] = Array.from({length: m + 1}, () => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i-1] === b[j-1] ? dp[i-1][j-1] : 1 + Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
    }
  }
  return dp[m][n];
}
