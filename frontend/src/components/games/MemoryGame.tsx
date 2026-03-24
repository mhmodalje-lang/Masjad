import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Star, RotateCcw } from 'lucide-react';

interface Card {
  id: string;
  content: string;
  pair_id: string;
  type: string;
}

interface MemoryProps {
  cards: Card[];
  totalPairs: number;
  xp: number;
  onComplete: (correct: boolean, xp: number) => void;
}

export default function MemoryGame({ cards, totalPairs, xp, onComplete }: MemoryProps) {
  const { t } = useTranslation();
  const [flipped, setFlipped] = useState<string[]>([]);
  const [matched, setMatched] = useState<string[]>([]);
  const [moves, setMoves] = useState(0);
  const [gameCards] = useState(() => [...cards]);

  const handleFlip = useCallback((cardId: string) => {
    if (flipped.length === 2) return;
    if (flipped.includes(cardId)) return;
    if (matched.includes(cardId)) return;

    const newFlipped = [...flipped, cardId];
    setFlipped(newFlipped);

    if (newFlipped.length === 2) {
      setMoves(m => m + 1);
      const [first, second] = newFlipped;
      const c1 = gameCards.find(c => c.id === first);
      const c2 = gameCards.find(c => c.id === second);

      if (c1 && c2 && c1.pair_id === c2.pair_id) {
        const newMatched = [...matched, first, second];
        setMatched(newMatched);
        setFlipped([]);
        if (newMatched.length === gameCards.length) {
          setTimeout(() => onComplete(true, xp), 800);
        }
      } else {
        setTimeout(() => setFlipped([]), 800);
      }
    }
  }, [flipped, matched, gameCards, xp, onComplete]);

  const isFlipped = (id: string) => flipped.includes(id) || matched.includes(id);
  const isMatched = (id: string) => matched.includes(id);

  const cardColors = ['from-blue-500 to-cyan-500', 'from-emerald-500 to-teal-500', 'from-orange-500 to-amber-500', 'from-purple-500 to-pink-500', 'from-rose-500 to-red-500', 'from-indigo-500 to-violet-500', 'from-lime-500 to-green-500', 'from-amber-500 to-yellow-500'];

  return (
    <div className="flex flex-col items-center px-4 py-4 w-full max-w-lg mx-auto">
      {/* Header */}
      <div className="w-full flex items-center justify-between mb-4 px-2">
        <div className="flex items-center gap-2">
          <Star className="h-5 w-5 text-amber-400" />
          <span className="text-xs font-bold text-amber-400 uppercase tracking-wider">{t('memoryChallenge') || 'Memory Challenge'}</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs text-foreground/50">{t('moves') || 'Moves'}: {moves}</span>
          <span className="text-xs font-bold text-emerald-400">+{xp} XP</span>
        </div>
      </div>

      {/* Progress */}
      <div className="w-full h-2 rounded-full bg-white/10 mb-4 overflow-hidden">
        <motion.div
          className="h-full bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full"
          animate={{ width: `${(matched.length / gameCards.length) * 100}%` }}
          transition={{ type: 'spring', stiffness: 300 }}
        />
      </div>

      {/* Cards Grid */}
      <div className="grid grid-cols-4 gap-2 w-full">
        {gameCards.map((card, idx) => (
          <motion.button
            key={card.id}
            initial={{ opacity: 0, rotateY: 180 }}
            animate={{ opacity: 1, rotateY: 0 }}
            transition={{ delay: idx * 0.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleFlip(card.id)}
            disabled={isFlipped(card.id)}
            className="relative aspect-square rounded-2xl overflow-hidden"
            style={{ perspective: '600px' }}
          >
            <div className={`w-full h-full transition-all duration-500 relative preserve-3d ${
              isFlipped(card.id) ? 'rotate-y-180' : ''
            }`}>
              {/* Card Back */}
              <div className={`absolute inset-0 backface-hidden rounded-2xl bg-gradient-to-br ${cardColors[idx % cardColors.length]} flex items-center justify-center border-2 border-white/20 shadow-lg ${
                isFlipped(card.id) ? 'invisible' : ''
              }`}>
                <span className="text-2xl text-white/80">❓</span>
              </div>
              {/* Card Front */}
              <div className={`absolute inset-0 backface-hidden rounded-2xl flex items-center justify-center border-2 shadow-lg ${
                isMatched(card.id)
                  ? 'bg-emerald-500/20 border-emerald-400/40 ring-2 ring-emerald-400/30'
                  : 'bg-gray-900/80 border-white/10'
              } ${isFlipped(card.id) ? '' : 'invisible'}`}>
                <span className={`${card.type === 'emoji' ? 'text-3xl' : 'text-xs font-bold text-center px-1'}`}>
                  {card.content}
                </span>
              </div>
            </div>
          </motion.button>
        ))}
      </div>

      {/* Completion */}
      {matched.length === gameCards.length && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="mt-6 p-4 rounded-2xl bg-emerald-500/20 border border-emerald-400/30 text-center w-full"
        >
          <span className="text-lg font-bold text-emerald-400">🎉 {t('allMatched') || 'All Matched!'} +{xp} XP</span>
          <p className="text-xs text-foreground/50 mt-1">{moves} {t('moves') || 'moves'}</p>
        </motion.div>
      )}
    </div>
  );
}
