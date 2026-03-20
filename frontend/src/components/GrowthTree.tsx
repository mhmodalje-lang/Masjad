import { useState, useEffect, useCallback, useRef } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';

interface GrowthTreeProps {
  level: number; // 1-10
  totalXp: number;
  className?: string;
}

const TREE_STAGES = [
  { minXp: 0, name: 'seed', emoji: '🌱', label: 'Seed' },
  { minXp: 30, name: 'sprout', emoji: '🌿', label: 'Sprout' },
  { minXp: 80, name: 'sapling', emoji: '🪴', label: 'Sapling' },
  { minXp: 150, name: 'young', emoji: '🌲', label: 'Young Tree' },
  { minXp: 250, name: 'growing', emoji: '🌳', label: 'Growing Tree' },
  { minXp: 400, name: 'fruiting', emoji: '🍃', label: 'Fruiting Tree' },
  { minXp: 600, name: 'majestic', emoji: '🌴', label: 'Majestic Palm' },
  { minXp: 800, name: 'golden', emoji: '✨', label: 'Golden Tree' },
];

export default function GrowthTree({ level, totalXp, className }: GrowthTreeProps) {
  const { t } = useLocale();
  
  const currentStage = TREE_STAGES.reduce((acc, stage) => 
    totalXp >= stage.minXp ? stage : acc, TREE_STAGES[0]);
  
  const nextStage = TREE_STAGES.find(s => s.minXp > totalXp);
  const progress = nextStage 
    ? ((totalXp - currentStage.minXp) / (nextStage.minXp - currentStage.minXp)) * 100
    : 100;

  const stageIndex = TREE_STAGES.indexOf(currentStage);

  return (
    <div className={cn('flex flex-col items-center', className)}>
      {/* Tree visual */}
      <div className="relative w-full max-w-[200px] h-[180px] flex flex-col items-center justify-end">
        {/* Sky background */}
        <div className="absolute inset-0 bg-gradient-to-b from-sky-200/20 to-transparent rounded-3xl" />
        
        {/* Stars for high levels */}
        {stageIndex >= 5 && (
          <div className="absolute top-2 w-full flex justify-around">
            {Array.from({length: Math.min(stageIndex - 4, 3)}).map((_, i) => (
              <span key={i} className="text-xs animate-pulse" style={{animationDelay: `${i * 0.4}s`}}>⭐</span>
            ))}
          </div>
        )}
        
        {/* The tree */}
        <div className="relative z-10 flex flex-col items-center">
          {/* Crown/Leaves - grows with level */}
          {stageIndex >= 2 && (
            <div className={cn(
              'transition-all duration-1000',
              stageIndex >= 6 ? 'text-5xl' : stageIndex >= 4 ? 'text-4xl' : 'text-3xl'
            )}>
              {stageIndex >= 7 ? '🌟' : stageIndex >= 6 ? '🌴' : stageIndex >= 4 ? '🌳' : '🌲'}
            </div>
          )}
          
          {/* Trunk - gets thicker with level */}
          <div className={cn(
            'bg-gradient-to-b from-amber-700 to-amber-900 rounded-b-lg transition-all duration-1000',
            stageIndex >= 4 ? 'w-4 h-12' : stageIndex >= 2 ? 'w-3 h-8' : stageIndex >= 1 ? 'w-2 h-5' : 'w-1 h-2'
          )} />
          
          {/* Seed/Sprout for early stages */}
          {stageIndex < 2 && (
            <span className={cn(
              'transition-all duration-500',
              stageIndex === 0 ? 'text-2xl' : 'text-3xl'
            )}>
              {currentStage.emoji}
            </span>
          )}
        </div>
        
        {/* Ground */}
        <div className="relative z-0 w-full h-6 bg-gradient-to-t from-amber-800/40 to-amber-600/20 rounded-b-3xl flex items-center justify-center">
          <div className="w-16 h-2 bg-green-700/30 rounded-full" />
        </div>
        
        {/* Fruits/rewards scattered around */}
        {stageIndex >= 5 && (
          <>
            <span className="absolute left-4 top-12 text-sm animate-bounce" style={{animationDuration: '3s'}}>🍎</span>
            <span className="absolute right-6 top-14 text-sm animate-bounce" style={{animationDuration: '2.5s', animationDelay: '1s'}}>🍊</span>
          </>
        )}
      </div>
      
      {/* Progress info */}
      <div className="w-full mt-2 text-center">
        <p className="text-sm font-bold text-foreground">{currentStage.emoji} {t(`tree_${currentStage.name}`) || currentStage.label}</p>
        {nextStage && (
          <>
            <div className="w-full h-2 bg-muted rounded-full overflow-hidden mt-1.5 mx-auto max-w-[160px]">
              <div 
                className="h-full bg-gradient-to-r from-green-400 to-emerald-500 rounded-full transition-all duration-700"
                style={{ width: `${Math.min(progress, 100)}%` }}
              />
            </div>
            <p className="text-[9px] text-muted-foreground mt-1">
              {totalXp}/{nextStage.minXp} XP → {nextStage.emoji}
            </p>
          </>
        )}
      </div>
    </div>
  );
}
