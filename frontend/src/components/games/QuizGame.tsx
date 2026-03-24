import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { CheckCircle, XCircle, Zap } from 'lucide-react';

interface QuizProps {
  question: string;
  options: string[];
  correctIndex: number;
  xp: number;
  onComplete: (correct: boolean, xp: number) => void;
}

export default function QuizGame({ question, options, correctIndex, xp, onComplete }: QuizProps) {
  const { t } = useTranslation();
  const [selected, setSelected] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);

  const handleSelect = (idx: number) => {
    if (revealed) return;
    setSelected(idx);
    setRevealed(true);
    setTimeout(() => onComplete(idx === correctIndex, idx === correctIndex ? xp : 0), 1800);
  };

  const optionColors = ['from-blue-500 to-cyan-400','from-emerald-500 to-teal-400','from-orange-500 to-amber-400','from-purple-500 to-pink-400'];

  return (
    <div className="flex flex-col items-center px-4 py-6 w-full max-w-lg mx-auto">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}
        className="w-full p-5 rounded-3xl bg-gradient-to-br from-indigo-500/15 to-purple-500/10 border border-indigo-400/20 mb-6 shadow-lg">
        <div className="flex items-center gap-2 mb-2">
          <Zap className="h-5 w-5 text-amber-400" />
          <span className="text-xs font-bold text-amber-400 uppercase tracking-wider">{t('knowledgeChallenge')}</span>
          <span className="ml-auto text-xs font-bold text-emerald-400">{t('earnedPoints').replace('{xp}', String(xp))}</span>
        </div>
        <p className="text-lg font-bold text-foreground leading-relaxed">{question}</p>
      </motion.div>

      <div className="w-full grid grid-cols-1 gap-3">
        {options.map((opt, idx) => {
          const isCorrect = idx === correctIndex;
          const isSelected = idx === selected;
          let bgClass = `bg-gradient-to-r ${optionColors[idx % 4]}`;
          let borderClass = 'border-transparent';
          let textClass = 'text-white';
          if (revealed) {
            if (isCorrect) { bgClass = 'bg-emerald-500'; borderClass = 'border-emerald-300 ring-2 ring-emerald-400/50'; }
            else if (isSelected && !isCorrect) { bgClass = 'bg-red-500/80'; borderClass = 'border-red-300 ring-2 ring-red-400/50'; }
            else { bgClass = 'bg-gray-600/40'; textClass = 'text-gray-400'; }
          }
          return (
            <motion.button key={idx} initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: idx * 0.1 }}
              whileTap={!revealed ? { scale: 0.97 } : {}} onClick={() => handleSelect(idx)} disabled={revealed}
              className={`relative w-full py-4 px-5 rounded-2xl border-2 ${bgClass} ${borderClass} ${textClass} font-bold text-base text-start transition-all shadow-md`}>
              <div className="flex items-center gap-3">
                <span className="w-8 h-8 rounded-xl bg-white/20 flex items-center justify-center text-sm font-black">{String.fromCharCode(65 + idx)}</span>
                <span className="flex-1">{opt}</span>
                <AnimatePresence>
                  {revealed && isCorrect && <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}><CheckCircle className="h-6 w-6 text-white" /></motion.div>}
                  {revealed && isSelected && !isCorrect && <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}><XCircle className="h-6 w-6 text-white" /></motion.div>}
                </AnimatePresence>
              </div>
            </motion.button>
          );
        })}
      </div>

      <AnimatePresence>
        {revealed && (
          <motion.div initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }}
            className={`mt-6 p-4 rounded-2xl text-center font-bold text-lg ${selected === correctIndex ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-400/30' : 'bg-red-500/20 text-red-400 border border-red-400/30'}`}>
            {selected === correctIndex ? t('correctAnswer').replace('{xp}', String(xp)) : t('wrongAnswer')}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
