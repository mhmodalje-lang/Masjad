import { useState } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { RotateCcw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';

const dhikrOptions = [
  { key: 'subhanAllah', arabic: 'سُبْحَانَ اللّهِ', target: 33 },
  { key: 'alhamdulillah', arabic: 'الْحَمْدُ لِلّهِ', target: 33 },
  { key: 'allahuAkbar', arabic: 'اللّهُ أَكْبَرُ', target: 34 },
];

export default function Tasbeeh() {
  const { t } = useLocale();
  const [selected, setSelected] = useState(0);
  const [count, setCount] = useState(0);
  const [total, setTotal] = useState(() => {
    const saved = localStorage.getItem('tasbeeh-total');
    return saved ? parseInt(saved) : 0;
  });

  const dhikr = dhikrOptions[selected];

  const handleTap = () => {
    setCount(prev => prev + 1);
    const newTotal = total + 1;
    setTotal(newTotal);
    localStorage.setItem('tasbeeh-total', String(newTotal));

    // Vibrate if available
    if (navigator.vibrate) navigator.vibrate(30);
  };

  const handleReset = () => setCount(0);

  const progress = Math.min((count / dhikr.target) * 100, 100);

  return (
    <div className="min-h-screen">
      <div className="gradient-islamic px-5 pb-6 pt-12">
        <h1 className="text-2xl font-bold text-primary-foreground">{t('tasbeeh')}</h1>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[50%] bg-background" />
      </div>

      <div className="px-5 pt-4">
        {/* Dhikr selector */}
        <div className="flex gap-2 mb-8 overflow-x-auto scrollbar-hide">
          {dhikrOptions.map((opt, i) => (
            <button
              key={opt.key}
              onClick={() => { setSelected(i); setCount(0); }}
              className={cn(
                'whitespace-nowrap rounded-full px-4 py-2 text-sm font-medium transition-all',
                selected === i
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary text-secondary-foreground'
              )}
            >
              {t(opt.key)}
            </button>
          ))}
        </div>

        {/* Counter */}
        <div className="flex flex-col items-center">
          <p className="text-3xl font-arabic text-foreground mb-8">{dhikr.arabic}</p>

          {/* Circular counter */}
          <div className="relative mb-6">
            <svg className="w-56 h-56 -rotate-90" viewBox="0 0 200 200">
              <circle cx="100" cy="100" r="90" fill="none" className="stroke-muted" strokeWidth="6" />
              <circle
                cx="100" cy="100" r="90" fill="none"
                className="stroke-primary transition-all duration-300"
                strokeWidth="6"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 90}`}
                strokeDashoffset={`${2 * Math.PI * 90 * (1 - progress / 100)}`}
              />
            </svg>
            <motion.button
              className="absolute inset-0 flex flex-col items-center justify-center"
              onClick={handleTap}
              whileTap={{ scale: 0.95 }}
            >
              <AnimatePresence mode="popLayout">
                <motion.span
                  key={count}
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: -20, opacity: 0 }}
                  className="text-5xl font-bold text-foreground"
                >
                  {count}
                </motion.span>
              </AnimatePresence>
              <span className="text-sm text-muted-foreground">/ {dhikr.target}</span>
            </motion.button>
          </div>

          {/* Reset */}
          <Button variant="outline" size="sm" onClick={handleReset} className="gap-2 mb-6">
            <RotateCcw className="h-4 w-4" />
            {t('reset')}
          </Button>

          {/* Total */}
          <div className="rounded-xl border border-border bg-card p-4 text-center w-full max-w-xs">
            <p className="text-xs text-muted-foreground">{t('total')}</p>
            <p className="text-2xl font-bold text-foreground">{total.toLocaleString()}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
