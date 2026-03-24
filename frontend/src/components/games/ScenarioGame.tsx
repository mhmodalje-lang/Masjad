import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Shield, CheckCircle, XCircle, Lightbulb } from 'lucide-react';

interface ScenarioProps { scenario: string; options: string[]; correctIndex: number; explanation: string; xp: number; onComplete: (correct: boolean, xp: number) => void; }

export default function ScenarioGame({ scenario, options, correctIndex, explanation, xp, onComplete }: ScenarioProps) {
  const { t } = useTranslation();
  const [selected, setSelected] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);

  const handleSelect = (idx: number) => {
    if (revealed) return;
    setSelected(idx); setRevealed(true);
    setTimeout(() => onComplete(idx === correctIndex, idx === correctIndex ? xp : 0), 4000);
  };

  return (
    <div className="flex flex-col items-center px-4 py-4 w-full max-w-lg mx-auto">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}
        className="w-full p-5 rounded-3xl bg-gradient-to-br from-violet-500/15 to-indigo-500/10 border border-violet-400/20 mb-5 shadow-lg">
        <div className="flex items-center gap-2 mb-3">
          <Shield className="h-5 w-5 text-violet-400" />
          <span className="text-xs font-bold text-violet-400 uppercase tracking-wider">{t('digitalShieldScenario')}</span>
          <span className="ml-auto text-xs font-bold text-emerald-400">{t('earnedPoints').replace('{xp}', String(xp))}</span>
        </div>
        <div className="flex items-start gap-3">
          <span className="text-3xl">🛡️</span>
          <p className="text-base font-bold text-foreground leading-relaxed flex-1">{scenario}</p>
        </div>
      </motion.div>

      <div className="w-full space-y-3">
        {options.map((opt, idx) => {
          let bgClass = 'bg-white/5 border-white/10 hover:bg-white/10';
          let textClass = 'text-foreground';
          if (revealed) {
            if (idx === correctIndex) { bgClass = 'bg-emerald-500/20 border-emerald-400/40 ring-2 ring-emerald-400/30'; textClass = 'text-emerald-300'; }
            else if (idx === selected) { bgClass = 'bg-red-500/20 border-red-400/40 ring-2 ring-red-400/30'; textClass = 'text-red-300'; }
            else { bgClass = 'bg-gray-800/30 border-gray-700/30'; textClass = 'text-gray-500'; }
          }
          return (
            <motion.button key={idx} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: idx * 0.1 }}
              whileTap={!revealed ? { scale: 0.97 } : {}} onClick={() => handleSelect(idx)} disabled={revealed}
              className={`w-full p-4 rounded-2xl border-2 ${bgClass} ${textClass} font-semibold text-sm text-start transition-all flex items-center gap-3`}>
              <span className="w-8 h-8 rounded-xl bg-white/10 flex items-center justify-center text-xs font-black shrink-0">{String.fromCharCode(65 + idx)}</span>
              <span className="flex-1">{opt}</span>
              {revealed && idx === correctIndex && <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}><CheckCircle className="h-5 w-5 text-emerald-400" /></motion.div>}
              {revealed && idx === selected && idx !== correctIndex && <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}><XCircle className="h-5 w-5 text-red-400" /></motion.div>}
            </motion.button>
          );
        })}
      </div>

      <AnimatePresence>
        {revealed && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
            className="mt-5 w-full p-4 rounded-2xl bg-amber-500/10 border border-amber-400/20">
            <div className="flex items-center gap-2 mb-2"><Lightbulb className="h-4 w-4 text-amber-400" /><span className="text-xs font-bold text-amber-400">{t('explanation')}</span></div>
            <p className="text-sm text-amber-200/80 leading-relaxed">{explanation}</p>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {revealed && (
          <motion.div initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.5 }}
            className={`mt-4 p-3 rounded-2xl text-center font-bold ${selected === correctIndex ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
            {selected === correctIndex ? t('shieldCorrect').replace('{xp}', String(xp)) : t('shieldWrong')}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
