import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Star } from 'lucide-react';

interface Card { id: string; content: string; pair_id: string; type: string; }
interface MemoryProps { cards: Card[]; totalPairs: number; xp: number; onComplete: (correct: boolean, xp: number) => void; }

export default function MemoryGame({ cards, totalPairs, xp, onComplete }: MemoryProps) {
  const { t } = useTranslation();
  const [flipped, setFlipped] = useState<string[]>([]);
  const [matched, setMatched] = useState<string[]>([]);
  const [moves, setMoves] = useState(0);
  const [gameCards] = useState(() => [...cards]);

  const handleFlip = useCallback((cardId: string) => {
    if (flipped.length === 2 || flipped.includes(cardId) || matched.includes(cardId)) return;
    const newFlipped = [...flipped, cardId];
    setFlipped(newFlipped);
    if (newFlipped.length === 2) {
      setMoves(m => m + 1);
      const c1 = gameCards.find(c => c.id === newFlipped[0]);
      const c2 = gameCards.find(c => c.id === newFlipped[1]);
      if (c1 && c2 && c1.pair_id === c2.pair_id) {
        const newMatched = [...matched, newFlipped[0], newFlipped[1]];
        setMatched(newMatched); setFlipped([]);
        if (newMatched.length === gameCards.length) setTimeout(() => onComplete(true, xp), 800);
      } else { setTimeout(() => setFlipped([]), 800); }
    }
  }, [flipped, matched, gameCards, xp, onComplete]);

  const isFlipped = (id: string) => flipped.includes(id) || matched.includes(id);
  const isMatched = (id: string) => matched.includes(id);
  const cardColors = ['from-blue-500 to-cyan-500','from-emerald-500 to-teal-500','from-orange-500 to-amber-500','from-purple-500 to-pink-500','from-rose-500 to-red-500','from-indigo-500 to-violet-500','from-lime-500 to-green-500','from-amber-500 to-yellow-500'];

  return (
    <div className="flex flex-col items-center px-4 py-4 w-full max-w-lg mx-auto">
      <div className="w-full flex items-center justify-between mb-4 px-2">
        <div className="flex items-center gap-2"><Star className="h-5 w-5 text-amber-400" /><span className="text-xs font-bold text-amber-400 uppercase tracking-wider">{t('memoryChallenge')}</span></div>
        <div className="flex items-center gap-3">
          <span className="text-xs text-foreground/50">{t('moves')}: {moves}</span>
          <span className="text-xs font-bold text-emerald-400">{t('earnedPoints').replace('{xp}', String(xp))}</span>
        </div>
      </div>
      <div className="w-full h-2 rounded-full bg-white/10 mb-4 overflow-hidden">
        <motion.div className="h-full bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full" animate={{ width: `${(matched.length / gameCards.length) * 100}%` }} />
      </div>
      <div className="grid grid-cols-4 gap-2 w-full">
        {gameCards.map((card, idx) => (
          <motion.button key={card.id} initial={{ opacity: 0, rotateY: 180 }} animate={{ opacity: 1, rotateY: 0 }} transition={{ delay: idx * 0.05 }}
            whileTap={{ scale: 0.95 }} onClick={() => handleFlip(card.id)} disabled={isFlipped(card.id)} className="relative aspect-square rounded-2xl overflow-hidden">
            <div className={`w-full h-full transition-all duration-500 relative`}>
              <div className={`absolute inset-0 rounded-2xl bg-gradient-to-br ${cardColors[idx % cardColors.length]} flex items-center justify-center border-2 border-white/20 shadow-lg ${isFlipped(card.id) ? 'invisible' : ''}`}>
                <span className="text-2xl text-white/80">❓</span>
              </div>
              <div className={`absolute inset-0 rounded-2xl flex items-center justify-center border-2 shadow-lg ${isMatched(card.id) ? 'bg-emerald-500/20 border-emerald-400/40' : 'bg-gray-900/80 border-white/10'} ${isFlipped(card.id) ? '' : 'invisible'}`}>
                <span className={`${card.type === 'emoji' ? 'text-3xl' : 'text-xs font-bold text-center px-1'}`}>{card.content}</span>
              </div>
            </div>
          </motion.button>
        ))}
      </div>
      {matched.length === gameCards.length && (
        <motion.div initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} className="mt-6 p-4 rounded-2xl bg-emerald-500/20 border border-emerald-400/30 text-center w-full">
          <span className="text-lg font-bold text-emerald-400">{t('matchComplete').replace('{xp}', String(xp))}</span>
          <p className="text-xs text-foreground/50 mt-1">{moves} {t('moves')}</p>
        </motion.div>
      )}
    </div>
  );
}
