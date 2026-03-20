import { useState, useCallback } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { Check, X, RotateCcw, Sparkles } from 'lucide-react';

interface SentenceBuilderProps {
  wordsAr: string[];
  wordsEn: string[];
  correctSentenceAr: string;
  correctSentenceEn: string;
  onComplete: (correct: boolean) => void;
  className?: string;
}

export default function SentenceBuilder({ wordsAr, wordsEn, correctSentenceAr, correctSentenceEn, onComplete, className }: SentenceBuilderProps) {
  const { t, dir } = useLocale();
  const [shuffledWords] = useState(() => {
    const indexed = wordsAr.map((w, i) => ({ ar: w, en: wordsEn[i] || '', idx: i }));
    return indexed.sort(() => Math.random() - 0.5);
  });
  const [selectedOrder, setSelectedOrder] = useState<number[]>([]);
  const [isChecked, setIsChecked] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const availableWords = shuffledWords.filter(w => !selectedOrder.includes(w.idx));
  const selectedWords = selectedOrder.map(idx => shuffledWords.find(w => w.idx === idx)!);

  const addWord = useCallback((idx: number) => {
    if (isChecked) return;
    setSelectedOrder(prev => [...prev, idx]);
  }, [isChecked]);

  const removeWord = useCallback((idx: number) => {
    if (isChecked) return;
    setSelectedOrder(prev => prev.filter(i => i !== idx));
  }, [isChecked]);

  const checkAnswer = useCallback(() => {
    const builtSentence = selectedOrder.map(idx => wordsAr[idx]).join(' ');
    const correct = builtSentence === correctSentenceAr;
    setIsCorrect(correct);
    setIsChecked(true);
    onComplete(correct);
  }, [selectedOrder, wordsAr, correctSentenceAr, onComplete]);

  const reset = useCallback(() => {
    setSelectedOrder([]);
    setIsChecked(false);
    setIsCorrect(false);
  }, []);

  return (
    <div className={cn('space-y-4', className)}>
      {/* Instruction */}
      <div className="text-center">
        <p className="text-sm font-bold text-foreground">{t('buildSentence')}</p>
        <p className="text-xs text-muted-foreground">{t('buildSentenceHint')}</p>
        {/* Show English meaning as hint */}
        <p className="text-xs text-primary mt-1">💡 {correctSentenceEn}</p>
      </div>

      {/* Drop zone - where sentence is built */}
      <div className={cn(
        'min-h-[60px] p-3 rounded-2xl border-2 border-dashed transition-all flex flex-wrap gap-2 justify-center items-center',
        isChecked && isCorrect ? 'border-green-500 bg-green-500/5' :
        isChecked && !isCorrect ? 'border-red-500 bg-red-500/5' :
        selectedOrder.length > 0 ? 'border-primary/50 bg-primary/5' :
        'border-border/30 bg-muted/20'
      )} dir="rtl">
        {selectedWords.length === 0 ? (
          <p className="text-xs text-muted-foreground">{t('tapWordsToArrange')}</p>
        ) : (
          selectedWords.map((word, i) => (
            <button
              key={`sel-${word.idx}-${i}`}
              onClick={() => removeWord(word.idx)}
              disabled={isChecked}
              className={cn(
                'px-3 py-2 rounded-xl text-sm font-bold transition-all',
                isChecked && isCorrect ? 'bg-green-500 text-white' :
                isChecked && !isCorrect ? 'bg-red-400 text-white' :
                'bg-primary text-primary-foreground hover:bg-primary/80 active:scale-95'
              )}
            >
              {word.ar}
            </button>
          ))
        )}
      </div>

      {/* Available words pool */}
      <div className="flex flex-wrap gap-2 justify-center" dir="rtl">
        {availableWords.map((word) => (
          <button
            key={`avail-${word.idx}`}
            onClick={() => addWord(word.idx)}
            disabled={isChecked}
            className={cn(
              'px-3 py-2 rounded-xl text-sm font-bold border transition-all',
              'bg-card border-border/40 text-foreground hover:border-primary/40 hover:bg-primary/5 active:scale-95'
            )}
          >
            <span>{word.ar}</span>
            <span className="block text-[9px] text-muted-foreground font-normal">{word.en}</span>
          </button>
        ))}
      </div>

      {/* Result */}
      {isChecked && (
        <div className={cn(
          'p-3 rounded-xl text-center',
          isCorrect ? 'bg-green-500/10' : 'bg-amber-500/10'
        )}>
          {isCorrect ? (
            <div className="flex items-center justify-center gap-2 text-green-500 font-bold text-sm">
              <Sparkles className="w-4 h-4" /> {t('perfectSentence')} ⭐
            </div>
          ) : (
            <div>
              <p className="text-amber-600 font-bold text-sm mb-1">{t('almostThere')}</p>
              <p className="text-xs text-muted-foreground" dir="rtl">{t('correctAnswer')}: {correctSentenceAr}</p>
            </div>
          )}
        </div>
      )}

      {/* Action buttons */}
      <div className="flex gap-2">
        {!isChecked && selectedOrder.length === wordsAr.length && (
          <button
            onClick={checkAnswer}
            className="flex-1 py-3 bg-primary text-primary-foreground rounded-xl font-bold text-sm flex items-center justify-center gap-2 active:scale-[0.98]"
          >
            <Check className="w-4 h-4" /> {t('checkAnswer')}
          </button>
        )}
        {(isChecked || selectedOrder.length > 0) && (
          <button
            onClick={reset}
            className={cn(
              'py-3 px-4 rounded-xl font-bold text-sm flex items-center justify-center gap-2 active:scale-[0.98]',
              isChecked ? 'flex-1 bg-primary text-primary-foreground' : 'bg-muted text-foreground'
            )}
          >
            <RotateCcw className="w-4 h-4" /> {isChecked ? t('tryAgain') : t('reset')}
          </button>
        )}
      </div>
    </div>
  );
}
