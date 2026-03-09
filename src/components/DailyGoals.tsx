import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Check, Moon, BookOpen, MessageSquare, RefreshCw } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { supabase } from '@/integrations/supabase/client';
import { isRamadan } from '@/data/islamicOccasions';

interface Goal {
  key: string;
  label: string;
  description: string;
  icon: React.ReactNode;
  color: string;       // ring color
  bgColor: string;     // bg for icon circle
  target: number;
  category: 'prayer' | 'dhikr' | 'quran' | 'general';
}

const defaultGoals: Goal[] = [
  {
    key: 'fasting',
    label: 'صيام رمضان',
    description: 'اليوم من رمضان',
    icon: <Moon className="h-4 w-4" />,
    color: 'text-primary',
    bgColor: 'bg-primary/15',
    target: 1,
    category: 'general',
  },
  {
    key: 'strengthen_faith',
    label: 'قوّي إيمانك',
    description: 'سبحان الله وبحمده',
    icon: <RefreshCw className="h-4 w-4" />,
    color: 'text-accent',
    bgColor: 'bg-accent/15',
    target: 7,
    category: 'dhikr',
  },
  {
    key: 'quran_reward',
    label: 'ثواب ثلث القرآن',
    description: 'قل هو الله أحد',
    icon: <BookOpen className="h-4 w-4" />,
    color: 'text-islamic-purple',
    bgColor: 'bg-islamic-purple/15',
    target: 3,
    category: 'quran',
  },
  {
    key: 'repentance',
    label: 'للتوبة والمغفرة',
    description: 'أستغفر الله العظيم',
    icon: <RefreshCw className="h-4 w-4" />,
    color: 'text-primary',
    bgColor: 'bg-primary/15',
    target: 11,
    category: 'dhikr',
  },
  {
    key: 'listen_quran',
    label: 'استمع إلى القرآن',
    description: '15 دقيقة على الأقل',
    icon: <BookOpen className="h-4 w-4" />,
    color: 'text-islamic-purple',
    bgColor: 'bg-islamic-purple/15',
    target: 1,
    category: 'quran',
  },
  {
    key: 'share_islam',
    label: 'حدّث شخصًا عن الإسلام',
    description: 'انشر الخير',
    icon: <MessageSquare className="h-4 w-4" />,
    color: 'text-islamic-teal',
    bgColor: 'bg-islamic-teal/15',
    target: 1,
    category: 'general',
  },
];

interface GoalProgress {
  [key: string]: { progress: number; completed: boolean };
}

export default function DailyGoals({ hijriMonthNumber }: { hijriMonthNumber: number | null }) {
  const { user } = useAuth();
  const todayKey = new Date().toISOString().split('T')[0];
  const ramadan = isRamadan(hijriMonthNumber);

  const [goals, setGoals] = useState<GoalProgress>(() => {
    const saved = localStorage.getItem(`daily-goals-${todayKey}`);
    return saved ? JSON.parse(saved) : {};
  });

  // Sync from DB on mount if logged in
  useEffect(() => {
    if (!user) return;
    supabase
      .from('daily_goals')
      .select('goal_key, progress, completed')
      .eq('user_id', user.id)
      .eq('date', todayKey)
      .then(({ data }) => {
        if (data && data.length > 0) {
          const dbGoals: GoalProgress = {};
          data.forEach((row: any) => {
            dbGoals[row.goal_key] = { progress: row.progress, completed: row.completed };
          });
          setGoals(dbGoals);
          localStorage.setItem(`daily-goals-${todayKey}`, JSON.stringify(dbGoals));
        }
      });
  }, [user, todayKey]);

  const updateGoal = async (goalKey: string, target: number) => {
    const current = goals[goalKey] || { progress: 0, completed: false };
    const newProgress = current.completed ? 0 : Math.min(current.progress + 1, target);
    const newCompleted = newProgress >= target;

    const updated = {
      ...goals,
      [goalKey]: { progress: newCompleted ? target : newProgress, completed: newCompleted },
    };
    setGoals(updated);
    localStorage.setItem(`daily-goals-${todayKey}`, JSON.stringify(updated));

    if (user) {
      await supabase.from('daily_goals').upsert({
        user_id: user.id,
        date: todayKey,
        goal_key: goalKey,
        progress: newCompleted ? target : newProgress,
        completed: newCompleted,
        target,
      }, { onConflict: 'user_id,date,goal_key' });
    }
  };

  const resetGoal = async (goalKey: string) => {
    const updated = { ...goals, [goalKey]: { progress: 0, completed: false } };
    setGoals(updated);
    localStorage.setItem(`daily-goals-${todayKey}`, JSON.stringify(updated));

    if (user) {
      await supabase.from('daily_goals').upsert({
        user_id: user.id,
        date: todayKey,
        goal_key: goalKey,
        progress: 0,
        completed: false,
        target: 1,
      }, { onConflict: 'user_id,date,goal_key' });
    }
  };

  const visibleGoals = ramadan ? defaultGoals : defaultGoals.filter(g => g.key !== 'fasting');

  return (
    <div className="px-4 mb-5">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-bold text-foreground">الأهداف اليومية</h3>
        <span className="text-xs text-muted-foreground">
          {Object.values(goals).filter(g => g.completed).length}/{visibleGoals.length} مكتمل
        </span>
      </div>
      <div className="space-y-2.5">
        {visibleGoals.map((goal, i) => {
          const state = goals[goal.key] || { progress: 0, completed: false };
          const progressPercent = goal.target > 1 ? (state.progress / goal.target) : (state.completed ? 1 : 0);
          const circleR = 16;
          const circleC = 2 * Math.PI * circleR;
          const offset = circleC * (1 - progressPercent);

          return (
            <motion.div
              key={goal.key}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className={cn(
                'rounded-2xl bg-card border border-border/50 p-4 flex items-center gap-3 transition-all',
                state.completed && 'border-primary/30 bg-primary/5'
              )}
            >
              {/* Circular progress */}
              <button
                onClick={() => state.completed ? resetGoal(goal.key) : updateGoal(goal.key, goal.target)}
                className="relative shrink-0"
              >
                <svg width="40" height="40" viewBox="0 0 40 40">
                  <circle cx="20" cy="20" r={circleR} fill="none" stroke="hsl(var(--border))" strokeWidth="3" />
                  <circle
                    cx="20" cy="20" r={circleR}
                    fill="none"
                    stroke={state.completed ? 'hsl(var(--primary))' : 'hsl(var(--accent))'}
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeDasharray={circleC}
                    strokeDashoffset={offset}
                    transform="rotate(-90 20 20)"
                    className="transition-all duration-500"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  {state.completed ? (
                    <Check className="h-3.5 w-3.5 text-primary" />
                  ) : (
                    <span className="text-[9px] font-bold text-muted-foreground tabular-nums">
                      {state.progress}/{goal.target}
                    </span>
                  )}
                </div>
              </button>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <p className={cn(
                  'text-sm font-bold',
                  state.completed ? 'text-primary line-through' : 'text-foreground'
                )}>
                  {goal.label}
                </p>
                <p className="text-xs text-muted-foreground truncate">{goal.description}</p>
              </div>

              {/* Icon */}
              <div className={cn('h-9 w-9 rounded-xl flex items-center justify-center shrink-0', goal.bgColor)}>
                <span className={goal.color}>{goal.icon}</span>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
