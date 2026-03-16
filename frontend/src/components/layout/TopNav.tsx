import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { useTheme } from '@/components/ThemeProvider';
import { Moon, Sun, SunMoon, Bell, User } from 'lucide-react';
import { cn } from '@/lib/utils';

export function TopNav() {
  const { user } = useAuth();
  const { theme, mode, toggle } = useTheme();
  const location = useLocation();

  const isHomePage = location.pathname === '/';
  if (isHomePage) return null;

  const ThemeIcon = mode === 'auto' ? SunMoon : mode === 'dark' ? Moon : Sun;

  return (
    <header
      data-testid="top-nav"
      className="sticky top-0 z-50 w-full border-b border-border/20 bg-card/90 backdrop-blur-2xl"
      dir="rtl"
    >
      <div className="flex items-center justify-between px-4 h-12">
        <Link to="/" className="flex items-center gap-2 shrink-0">
          <div className="h-7 w-7 rounded-lg bg-gradient-to-br from-primary to-amber-600 flex items-center justify-center shadow-md shadow-primary/20">
            <span className="text-primary-foreground text-[10px] font-bold">أ</span>
          </div>
          <span className="text-sm font-bold text-foreground hidden sm:block">أذان وحكاية</span>
        </Link>

        <div className="flex items-center gap-1">
          <button
            onClick={toggle}
            data-testid="theme-toggle-nav"
            className={cn(
              'p-2 rounded-xl transition-all active:scale-95',
              theme === 'dark' ? 'bg-primary/10 text-primary' : 'bg-amber-100 text-amber-700'
            )}
          >
            <ThemeIcon className="h-4 w-4" />
          </button>
          <Link to="/notifications" className="p-2 rounded-xl hover:bg-muted/50 text-muted-foreground">
            <Bell className="h-4 w-4" />
          </Link>
          <Link
            to={user ? '/profile' : '/auth'}
            className="p-2 rounded-xl hover:bg-muted/50 text-muted-foreground"
          >
            <User className="h-4 w-4" />
          </Link>
        </div>
      </div>
    </header>
  );
}
