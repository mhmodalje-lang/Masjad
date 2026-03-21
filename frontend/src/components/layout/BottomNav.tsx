import { useLocation, Link } from 'react-router-dom';
import { Home, BookOpen, Plus, MessageSquare, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { useLocale } from '@/hooks/useLocale';
import { useTheme } from '@/components/ThemeProvider';

export function BottomNav() {
  const location = useLocation();
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  const navItems = [
    { path: '/', icon: Home, label: t('navHome'), exact: true },
    { path: '/stories', icon: BookOpen, label: t('navStories') },
    { path: '/create', icon: Plus, label: '', isCreate: true },
    { path: '/messages', icon: MessageSquare, label: t('navMessages') },
    { path: '/more', icon: User, label: t('navMore') },
  ];

  const hiddenPaths = ['/auth', '/reels'];
  if (hiddenPaths.some(p => location.pathname.startsWith(p))) return null;

  return (
    <nav
      data-testid="bottom-nav"
      className="fixed bottom-0 left-0 right-0 z-50"
    >
      {/* Glass background - theme-aware */}
      <div className={cn(
        'backdrop-blur-xl border-t transition-colors duration-300',
        isDark
          ? 'bg-[#0f1a24]/95 border-emerald-800/25 shadow-[0_-4px_30px_rgba(0,0,0,0.3)]'
          : 'bg-white/95 border-border/40 shadow-[0_-4px_30px_rgba(0,0,0,0.06)]'
      )}>
        <div
          className="flex items-end justify-around px-2 pb-[env(safe-area-inset-bottom,4px)] pt-1.5"
          dir={dir}
        >
          {navItems.map((item) => {
            const isActive = item.exact
              ? location.pathname === item.path
              : location.pathname.startsWith(item.path);

            if (item.isCreate) {
              return (
                <Link
                  key="create"
                  to={user ? '/stories?create=true' : '/auth'}
                  data-testid="nav-create"
                  className="relative flex flex-col items-center -mt-5"
                >
                  <div className={cn(
                    'h-14 w-14 rounded-2xl bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center shadow-lg shadow-emerald-500/40 active:scale-90 transition-transform border-2 border-emerald-300/40 ring-4',
                    isDark ? 'ring-[#0f1a24]/90' : 'ring-white/90'
                  )}>
                    <Plus className="h-7 w-7 text-white stroke-[3px]" />
                  </div>
                </Link>
              );
            }

            return (
              <Link
                key={item.path}
                to={item.path}
                data-testid={`nav-${item.path.replace('/', '') || 'home'}`}
                className={cn(
                  'relative flex flex-col items-center gap-1 py-2 px-3 rounded-xl transition-all duration-200 min-w-[56px]',
                  isActive
                    ? isDark ? 'text-emerald-300' : 'text-primary'
                    : isDark ? 'text-emerald-200/50 active:text-emerald-200' : 'text-muted-foreground active:text-foreground'
                )}
              >
                {/* Active indicator dot */}
                {isActive && (
                  <motion.div
                    layoutId="nav-dot"
                    className={cn(
                      'absolute -top-0.5 h-1 w-1 rounded-full',
                      isDark ? 'bg-emerald-400' : 'bg-primary'
                    )}
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                  />
                )}
                {/* Icon container */}
                <div className={cn(
                  'h-8 w-8 rounded-xl flex items-center justify-center transition-all duration-200',
                  isActive
                    ? isDark ? 'bg-emerald-500/20 scale-110' : 'bg-primary/10 scale-110'
                    : 'bg-transparent'
                )}>
                  <item.icon className={cn(
                    'h-[20px] w-[20px] transition-all duration-200',
                    isActive ? 'stroke-[2.5px]' : 'stroke-[1.8px]'
                  )} />
                </div>
                {/* Label */}
                <span className={cn(
                  "text-[10px] leading-none text-center truncate max-w-[60px]",
                  isActive ? 'font-bold' : 'font-medium opacity-70'
                )}>
                  {item.label}
                </span>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
