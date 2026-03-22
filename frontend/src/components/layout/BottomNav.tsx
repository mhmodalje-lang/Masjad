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
        'glass-nav border-t transition-colors duration-300',
        isDark
          ? 'bg-[#0c1a2e]/92 border-white/[0.06] shadow-[0_-4px_30px_rgba(0,0,0,0.4)]'
          : 'bg-white/85 border-[#064E3B]/[0.08] shadow-[0_-4px_30px_rgba(6,78,59,0.06)]'
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
                    'h-14 w-14 rounded-2xl bg-gradient-to-br from-[#064E3B] to-[#0A6B52] flex items-center justify-center shadow-lg shadow-[#064E3B]/30 active:scale-90 transition-transform border-2 border-[#0A6B52]/40 ring-4',
                    isDark ? 'ring-[#0c1a2e]/90' : 'ring-white/90'
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
                    ? isDark ? 'text-[#D4AF37]' : 'text-[#064E3B]'
                    : isDark ? 'text-[#94A3B8] active:text-white/80' : 'text-muted-foreground active:text-foreground'
                )}
              >
                {/* Active indicator dot */}
                {isActive && (
                  <motion.div
                    layoutId="nav-dot"
                    className={cn(
                      'absolute -top-0.5 h-1 w-1 rounded-full',
                      isDark ? 'bg-[#D4AF37]' : 'bg-[#064E3B]'
                    )}
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                  />
                )}
                {/* Icon container */}
                <div className={cn(
                  'h-8 w-8 rounded-xl flex items-center justify-center transition-all duration-200',
                  isActive
                    ? isDark ? 'bg-[#D4AF37]/15 scale-110' : 'bg-[#064E3B]/10 scale-110'
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
