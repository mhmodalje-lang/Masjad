import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { GripVertical, CheckCircle, XCircle, ArrowUpDown } from 'lucide-react';

interface DragItem {
  id: number;
  text: string;
}

interface DragDropProps {
  title: string;
  items: DragItem[];
  correctOrder: number[];
  xp: number;
  onComplete: (correct: boolean, xp: number) => void;
}

export default function DragDropGame({ title, items, correctOrder, xp, onComplete }: DragDropProps) {
  const { t } = useTranslation();
  const [orderedItems, setOrderedItems] = useState(items);
  const [checked, setChecked] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const checkOrder = () => {
    const currentOrder = orderedItems.map(item => item.id);
    const correct = JSON.stringify(currentOrder) === JSON.stringify(correctOrder);
    setIsCorrect(correct);
    setChecked(true);
    setTimeout(() => {
      onComplete(correct, correct ? xp : Math.floor(xp / 3));
    }, 2000);
  };

  const stepColors = [
    'from-blue-500/20 to-blue-600/10 border-blue-400/30',
    'from-emerald-500/20 to-emerald-600/10 border-emerald-400/30',
    'from-amber-500/20 to-amber-600/10 border-amber-400/30',
    'from-purple-500/20 to-purple-600/10 border-purple-400/30',
    'from-rose-500/20 to-rose-600/10 border-rose-400/30',
    'from-cyan-500/20 to-cyan-600/10 border-cyan-400/30',
    'from-orange-500/20 to-orange-600/10 border-orange-400/30',
    'from-indigo-500/20 to-indigo-600/10 border-indigo-400/30',
  ];

  return (
    <div className="flex flex-col items-center px-4 py-4 w-full max-w-lg mx-auto">
      {/* Header */}
      <div className="w-full p-4 rounded-2xl bg-gradient-to-br from-orange-500/15 to-amber-500/10 border border-orange-400/20 mb-4">
        <div className="flex items-center gap-2 mb-1">
          <ArrowUpDown className="h-5 w-5 text-orange-400" />
          <span className="text-xs font-bold text-orange-400 uppercase tracking-wider">{t('dragDropChallenge') || 'Order the Steps'}</span>
          <span className="ml-auto text-xs font-bold text-emerald-400">+{xp} XP</span>
        </div>
        <p className="text-base font-bold text-foreground">{title}</p>
        <p className="text-xs text-foreground/50 mt-1">{t('dragToReorder') || 'Drag to reorder the steps correctly'}</p>
      </div>

      {/* Reorderable list */}
      <Reorder.Group
        axis="y"
        values={orderedItems}
        onReorder={setOrderedItems}
        className="w-full space-y-2"
      >
        {orderedItems.map((item, idx) => {
          let itemStyle = `bg-gradient-to-r ${stepColors[idx % stepColors.length]}`;
          if (checked) {
            const correctPos = correctOrder.indexOf(item.id);
            if (correctPos === idx) {
              itemStyle = 'bg-emerald-500/20 border-emerald-400/40 ring-1 ring-emerald-400/30';
            } else {
              itemStyle = 'bg-red-500/20 border-red-400/40 ring-1 ring-red-400/30';
            }
          }

          return (
            <Reorder.Item
              key={item.id}
              value={item}
              className={`flex items-center gap-3 p-4 rounded-2xl border-2 ${itemStyle} cursor-grab active:cursor-grabbing transition-all shadow-sm`}
              whileDrag={{ scale: 1.05, boxShadow: '0 10px 30px rgba(0,0,0,0.3)', zIndex: 50 }}
            >
              <GripVertical className="h-5 w-5 text-foreground/30 shrink-0" />
              <span className="w-7 h-7 rounded-lg bg-white/10 flex items-center justify-center text-xs font-black text-foreground/60">{idx + 1}</span>
              <span className="flex-1 font-semibold text-sm text-foreground">{item.text}</span>
              {checked && (
                <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}>
                  {correctOrder.indexOf(item.id) === idx
                    ? <CheckCircle className="h-5 w-5 text-emerald-400" />
                    : <XCircle className="h-5 w-5 text-red-400" />
                  }
                </motion.div>
              )}
            </Reorder.Item>
          );
        })}
      </Reorder.Group>

      {/* Check Button */}
      {!checked && (
        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={checkOrder}
          className="mt-6 w-full py-4 rounded-2xl bg-gradient-to-r from-orange-500 to-amber-500 text-white font-bold text-base shadow-lg shadow-orange-500/20 active:shadow-sm transition-all"
        >
          {t('checkOrder') || 'Check My Order'} ✨
        </motion.button>
      )}

      {/* Result */}
      <AnimatePresence>
        {checked && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={`mt-4 p-4 rounded-2xl text-center w-full font-bold ${
              isCorrect
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-400/30'
                : 'bg-amber-500/20 text-amber-400 border border-amber-400/30'
            }`}
          >
            {isCorrect
              ? `🎉 ${t('perfectOrder') || 'Perfect Order!'} +${xp} XP`
              : `🤔 ${t('almostThere') || 'Almost There!'} +${Math.floor(xp / 3)} XP`
            }
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
