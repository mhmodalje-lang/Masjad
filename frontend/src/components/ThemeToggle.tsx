import { Moon, Sun, SunMoon } from 'lucide-react';
import { useTheme } from '@/components/ThemeProvider';
import { cn } from '@/lib/utils';
import i18n from '@/lib/i18nConfig';

export function ThemeToggle() {
  const { theme, mode, toggle } = useTheme();

  const icons = { dark: Moon, light: Sun, auto: SunMoon };
  const Icon = icons[mode];

  return (
    <button
      onClick={toggle}
      data-testid="theme-toggle"
      aria-label={`${i18n.t('currentMode')}: ${mode === 'auto' ? i18n.t('automatic') : mode === 'dark' ? i18n.t('darkMode') : i18n.t('lightMode')}`}
      className={cn(
        'relative inline-flex h-8 w-14 items-center rounded-full transition-all duration-500 shrink-0',
        theme === 'dark'
          ? 'bg-[#0a1f14] border border-[#D4AF37]/30'
          : 'bg-[hsl(var(--mystic-moss))]/10 border border-[hsl(var(--mystic-moss))]/20'
      )}
    >
      <span
        className={cn(
          'inline-flex h-6 w-6 rounded-full transition-all duration-500 items-center justify-center',
          theme === 'dark'
            ? 'translate-x-[4px] bg-[#D4AF37]'
            : 'translate-x-[30px] bg-[hsl(var(--mystic-moss))]'
        )}
      >
        <Icon className={cn('h-3.5 w-3.5', theme === 'dark' ? 'text-[#0a1f14]' : 'text-white')} />
      </span>
    </button>
  );
}
