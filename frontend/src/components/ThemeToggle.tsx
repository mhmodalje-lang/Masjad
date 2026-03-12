import { Moon, Sun, SunMoon } from 'lucide-react';
import { useTheme } from '@/components/ThemeProvider';
import { cn } from '@/lib/utils';

export function ThemeToggle() {
  const { theme, mode, toggle } = useTheme();

  const icons = { dark: Moon, light: Sun, auto: SunMoon };
  const Icon = icons[mode];

  return (
    <button
      onClick={toggle}
      data-testid="theme-toggle"
      aria-label={`الوضع الحالي: ${mode === 'auto' ? 'تلقائي' : mode === 'dark' ? 'ليلي' : 'نهاري'}`}
      className={cn(
        'relative inline-flex h-8 w-14 items-center rounded-full transition-all duration-500 shrink-0',
        theme === 'dark'
          ? 'bg-emerald-900 border border-emerald-700/50'
          : 'bg-amber-100 border border-amber-300/50'
      )}
    >
      <span
        className={cn(
          'inline-flex h-6 w-6 rounded-full transition-all duration-500 items-center justify-center',
          theme === 'dark'
            ? 'translate-x-[4px] bg-emerald-400'
            : 'translate-x-[30px] bg-amber-400'
        )}
      >
        <Icon className={cn('h-3.5 w-3.5', theme === 'dark' ? 'text-emerald-950' : 'text-amber-900')} />
      </span>
    </button>
  );
}
