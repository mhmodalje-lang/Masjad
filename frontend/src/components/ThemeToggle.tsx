import { useState, useEffect } from 'react';
import { Sun, Moon, Monitor } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { ThemeMode, getSavedTheme, setTheme, getEffectiveTheme } from '@/lib/theme';
import { cn } from '@/lib/utils';

export function ThemeToggle({ compact = false }: { compact?: boolean }) {
  const [mode, setMode] = useState<ThemeMode>(getSavedTheme);
  const [effective, setEffective] = useState<'dark' | 'light'>(getEffectiveTheme);

  const cycle = () => {
    const next: ThemeMode = mode === 'dark' ? 'light' : mode === 'light' ? 'system' : 'dark';
    setMode(next);
    setTheme(next);
    setEffective(next === 'system' ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : next);
  };

  const icons: Record<ThemeMode, React.ReactNode> = {
    dark: <Moon className="h-4 w-4" />,
    light: <Sun className="h-4 w-4" />,
    system: <Monitor className="h-4 w-4" />,
  };

  const labels: Record<ThemeMode, string> = {
    dark: 'داكن',
    light: 'فاتح',
    system: 'تلقائي',
  };

  if (compact) {
    return (
      <button onClick={cycle} className={cn(
        'h-9 w-9 rounded-full flex items-center justify-center transition-all duration-300',
        'bg-white/10 hover:bg-white/20 backdrop-blur-sm',
        'border border-white/20'
      )}>
        <AnimatePresence mode="wait">
          <motion.div key={mode} initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }} transition={{ duration: 0.2 }}>
            {icons[mode]}
          </motion.div>
        </AnimatePresence>
      </button>
    );
  }

  return (
    <button onClick={cycle} className={cn(
      'flex items-center gap-2 px-3 py-2 rounded-xl transition-all duration-300',
      'bg-card border border-border hover:bg-accent',
      'text-sm font-medium text-foreground'
    )}>
      <AnimatePresence mode="wait">
        <motion.div key={mode} initial={{ y: -10, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: 10, opacity: 0 }} transition={{ duration: 0.15 }}>
          {icons[mode]}
        </motion.div>
      </AnimatePresence>
      <span>{labels[mode]}</span>
    </button>
  );
}
