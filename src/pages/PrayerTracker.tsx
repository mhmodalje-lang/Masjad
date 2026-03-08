import { useState, useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Check, Flame } from 'lucide-react';

const prayerKeys = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha'];

function getTodayKey() {
  return new Date().toISOString().split('T')[0];
}

export default function PrayerTracker() {
  const { t } = useLocale();
  const todayKey = getTodayKey();

  const [tracked, setTracked] = useState<Record<string, string[]>>(() => {
    const saved = localStorage.getItem('prayer-tracker');
    return saved ? JSON.parse(saved) : {};
  });

  const todayPrayers = tracked[todayKey] || [];

  const togglePrayer = (key: string) => {
    setTracked(prev => {
      const today = prev[todayKey] || [];
      const updated = today.includes(key) ? today.filter(k => k !== key) : [...today, key];
      const next = { ...prev, [todayKey]: updated };
      localStorage.setItem('prayer-tracker', JSON.stringify(next));
      return next;
    });
  };

  // Calculate streak
  const streak = (() => {
    let count = 0;
    const d = new Date();
    d.setDate(d.getDate() - 1); // start from yesterday
    while (true) {
      const key = d.toISOString().split('T')[0];
      if (tracked[key]?.length === 5) {
        count++;
        d.setDate(d.getDate() - 1);
      } else break;
    }
    // Include today if all done
    if (todayPrayers.length === 5) count++;
    return count;
  })();

  const progress = (todayPrayers.length / 5) * 100;

  return (
    <div className="min-h-screen">
      <div className="gradient-islamic px-5 pb-6 pt-12">
        <h1 className="text-2xl font-bold text-primary-foreground">{t('tracker')}</h1>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[50%] bg-background" />
      </div>

      <div className="px-5 pt-4">
        {/* Stats */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          <div className="rounded-xl border border-border bg-card p-4 text-center">
            <p className="text-xs text-muted-foreground mb-1">{t('completed')}</p>
            <p className="text-3xl font-bold text-primary">{todayPrayers.length}/5</p>
          </div>
          <div className="rounded-xl border border-border bg-card p-4 text-center">
            <div className="flex items-center justify-center gap-1.5 mb-1">
              <Flame className="h-3.5 w-3.5 text-accent" />
              <p className="text-xs text-muted-foreground">{t('streak')}</p>
            </div>
            <p className="text-3xl font-bold text-accent">{streak} <span className="text-sm font-normal text-muted-foreground">{t('days')}</span></p>
          </div>
        </div>

        {/* Progress bar */}
        <div className="h-2 w-full rounded-full bg-muted mb-6 overflow-hidden">
          <motion.div
            className="h-full rounded-full bg-primary"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>

        {/* Prayer checklist */}
        <div className="space-y-3">
          {prayerKeys.map((key, i) => {
            const done = todayPrayers.includes(key);
            return (
              <motion.button
                key={key}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.06 }}
                onClick={() => togglePrayer(key)}
                className={cn(
                  'w-full flex items-center justify-between rounded-xl border p-4 transition-all',
                  done
                    ? 'border-primary bg-primary/5'
                    : 'border-border bg-card'
                )}
              >
                <span className={cn('font-semibold', done ? 'text-primary' : 'text-foreground')}>
                  {t(key)}
                </span>
                <div className={cn(
                  'h-7 w-7 rounded-full flex items-center justify-center transition-all',
                  done ? 'bg-primary' : 'border-2 border-muted-foreground/30'
                )}>
                  {done && <Check className="h-4 w-4 text-primary-foreground" />}
                </div>
              </motion.button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
