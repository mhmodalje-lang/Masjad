import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { useTheme } from '@/components/ThemeProvider';
import { Moon, Sun, SunMoon, Search, Bell, User } from 'lucide-react';
import { cn } from '@/lib/utils';

export function TopNav() {
  const { user } = useAuth();
  const { theme, mode, toggle } = useTheme();
  const location = useLocation();

  // Don't show on pages that have their own hero/header
  const isHomePage = location.pathname === '/';
  if (isHomePage) return null;

  const ThemeIcon = mode === 'auto' ? SunMoon : mode === 'dark' ? Moon : Sun;

  return (
    <header
      data-testid="top-nav"
      className="sticky top-0 z-50 w-full border-b border-border/20 bg-card/90 backdrop-blur-2xl"
      dir="rtl"
    >
      <div className="flex items-center justify-between px-4 h-14">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 shrink-0">
          <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-700 flex items-center justify-center">
            <span className="text-white text-xs font-bold">م</span>
          </div>
          <span className="text-sm font-bold text-foreground hidden sm:block">المؤذن العالمي</span>
        </Link>

        {/* Actions */}
        <div className="flex items-center gap-1.5">
          <button
            onClick={toggle}
            data-testid="theme-toggle-nav"
            className={cn(
              'p-2 rounded-xl transition-all active:scale-95',
              theme === 'dark' ? 'bg-emerald-900/50 text-emerald-400' : 'bg-amber-50 text-amber-600'
            )}
          >
            <ThemeIcon className="h-4.5 w-4.5" />
          </button>
          <Link to="/messages" className="p-2 rounded-xl bg-muted/50 text-muted-foreground">
            <Bell className="h-4.5 w-4.5" />
          </Link>
          <Link
            to={user ? '/more' : '/auth'}
            className="p-2 rounded-xl bg-muted/50 text-muted-foreground"
          >
            <User className="h-4.5 w-4.5" />
          </Link>
        </div>
      </div>
    </header>
  );
}
