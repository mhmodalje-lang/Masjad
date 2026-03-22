import { useLocale } from '@/hooks/useLocale';
import { useState } from 'react';
import { Check, Bell } from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import { cn } from '@/lib/utils';
import { useNavigate } from 'react-router-dom';
import { toast } from '@/hooks/use-toast';
import PageHeader from '@/components/PageHeader';

export default function QuranGoal() {
  const { t, dir } = useLocale();
  const navigate = useNavigate();
  const saved = JSON.parse(localStorage.getItem('quran-goal') || '{}');
  const [selected, setSelected] = useState<number>(saved.duration || 10);
  const [reminder, setReminder] = useState(saved.reminder || false);
  const [time, setTime] = useState(saved.time || '08:00');

  const durations = [
    { label: t('5minutes'), value: 5 },
    { label: t('10minutes'), value: 10 },
    { label: t('20minutes'), value: 20 },
    { label: t('30minutes'), value: 30 },
    { label: t('1hour'), value: 60 },
  ];

  const save = () => {
    localStorage.setItem('quran-goal', JSON.stringify({ duration: selected, reminder, time }));
    toast({ title: t('quranGoalSaved'), description: t('minutesDaily').replace('{count}', String(selected)) });
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-background pb-24" dir={dir}>
      <PageHeader title={t('setQuranGoalTitle')} backTo="/" />

      <div className="px-4 pt-6 space-y-4">
        <p className="text-sm text-muted-foreground text-center mb-2">
          {t('howMuchQuranDaily')}
        </p>

        <div className="space-y-2">
          {durations.map(d => (
            <button
              key={d.value}
              onClick={() => setSelected(d.value)}
              className={cn(
                'w-full rounded-2xl neu-card p-4 flex items-center justify-between',
                selected === d.value && 'border-primary bg-primary/5'
              )}
            >
              <span className={cn('text-sm font-bold', selected === d.value ? 'text-primary' : 'text-foreground')}>
                {d.label}
              </span>
              {selected === d.value && (
                <div className="h-6 w-6 rounded-full bg-primary flex items-center justify-center">
                  <Check className="h-3.5 w-3.5 text-primary-foreground" />
                </div>
              )}
            </button>
          ))}
        </div>

        <div className="rounded-2xl neu-card p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Bell className="h-4 w-4 text-accent" />
              <span className="text-sm font-bold text-foreground">{t('dailyReminder')}</span>
            </div>
            <Switch checked={reminder} onCheckedChange={setReminder} />
          </div>
          {reminder && (
            <input
              type="time"
              value={time}
              onChange={e => setTime(e.target.value)}
              className="w-full rounded-xl border border-border bg-background p-2 text-sm text-foreground"
            />
          )}
        </div>

        <button
          onClick={save}
          className="w-full rounded-2xl bg-primary text-primary-foreground font-bold py-4 text-sm active:scale-[0.98] transition-transform"
        >
          {t('createGoal')}
        </button>
      </div>
    </div>
  );
}
