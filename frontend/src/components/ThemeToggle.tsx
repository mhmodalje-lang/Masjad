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
          ? 'bg-[#0c1a2e] border border-[#D4AF37]/30'
          : 'bg-[#064E3B]/10 border border-[#064E3B]/20'
      )}
    >
      <span
        className={cn(
          'inline-flex h-6 w-6 rounded-full transition-all duration-500 items-center justify-center',
          theme === 'dark'
            ? 'translate-x-[4px] bg-[#D4AF37]'
            : 'translate-x-[30px] bg-[#064E3B]'
        )}
      >
        <Icon className={cn('h-3.5 w-3.5', theme === 'dark' ? 'text-[#0c1a2e]' : 'text-white')} />
      </span>
    </button>
  );
}
