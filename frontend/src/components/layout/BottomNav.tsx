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
      {/* Mystic Glass Bar */}
      <div className={cn(
        'glass-nav border-t transition-all duration-500',
        isDark
          ? 'bg-[hsl(220,25%,8%)]/95 border-white/[0.06] shadow-[0_-4px_30px_rgba(0,0,0,0.5)]'
          : 'bg-[hsl(30,20%,97%)]/92 border-[hsl(152,55%,22%)]/[0.08] shadow-[0_-4px_30px_rgba(0,0,0,0.04)]'
      )} style={{ backdropFilter: 'blur(20px) saturate(1.5)', WebkitBackdropFilter: 'blur(20px) saturate(1.5)' }}>
        <div
          className="flex items-center justify-around px-3 pt-2 pb-3"
          style={{ paddingBottom: 'max(12px, env(safe-area-inset-bottom, 12px))' }}
          dir={dir}
        >
          {navItems.map((item) => {
            const isActive = item.exact
              ? location.pathname === item.path
              : location.pathname.startsWith(item.path);

            {/* ═══ Floating + Button ═══ */}
            if (item.isCreate) {
              return (
                <Link
                  key="create"
                  to={user ? '/stories?create=true' : '/auth'}
                  data-testid="nav-create"
                  className="relative flex flex-col items-center -mt-5"
                >
                  <motion.div
                    whileTap={{ scale: 0.88 }}
                    className={cn(
                      'h-[52px] w-[52px] rounded-full flex items-center justify-center',
                      'bg-gradient-to-br from-[hsl(152,55%,22%)] to-[hsl(155,50%,30%)]',
                      'shadow-[0_4px_20px_-2px_hsl(152,55%,22%,0.5)]',
                      'border-[3px]',
                      isDark 
                        ? 'border-[hsl(220,25%,10%)] ring-2 ring-[hsl(155,55%,42%)]/20' 
                        : 'border-[hsl(30,20%,97%)] ring-2 ring-[hsl(152,55%,22%)]/10'
                    )}
                  >
                    <Plus className="h-6 w-6 text-white stroke-[2.5px]" />
                  </motion.div>
                </Link>
              );
            }

            return (
              <Link
                key={item.path}
                to={item.path}
                data-testid={`nav-${item.path.replace('/', '') || 'home'}`}
                className={cn(
                  'relative flex flex-col items-center gap-1 py-1.5 px-3 rounded-2xl transition-all duration-300 min-w-[60px]',
                  isActive
                    ? isDark ? 'text-[hsl(38,72%,54%)]' : 'text-[hsl(152,55%,22%)]'
                    : isDark ? 'text-[hsl(210,10%,50%)] active:text-white/80' : 'text-muted-foreground active:text-foreground'
                )}
              >
                {/* Active glow indicator */}
                {isActive && (
                  <motion.div
                    layoutId="nav-glow"
                    className={cn(
                      'absolute -top-1 h-[3px] w-6 rounded-full',
                      isDark 
                        ? 'bg-gradient-to-r from-transparent via-[hsl(38,72%,54%)] to-transparent shadow-[0_0_12px_hsl(38,72%,54%,0.4)]' 
                        : 'bg-gradient-to-r from-transparent via-[hsl(152,55%,22%)] to-transparent shadow-[0_0_12px_hsl(152,55%,22%,0.3)]'
                    )}
                    transition={{ type: 'spring', stiffness: 350, damping: 28 }}
                  />
                )}
                {/* Icon */}
                <div className={cn(
                  'h-8 w-8 rounded-xl flex items-center justify-center transition-all duration-300',
                  isActive
                    ? isDark 
                      ? 'bg-[hsl(38,72%,54%)]/12 scale-110' 
                      : 'bg-[hsl(152,55%,22%)]/8 scale-110'
                    : 'bg-transparent scale-100'
                )}>
                  <item.icon className={cn(
                    'h-[22px] w-[22px] transition-all duration-300',
                    isActive ? 'stroke-[2.5px]' : 'stroke-[1.8px]'
                  )} />
                </div>
                {/* Label */}
                <span className={cn(
                  "text-[11px] leading-tight text-center truncate max-w-[68px] transition-all duration-300",
                  isActive ? 'font-bold opacity-100' : 'font-medium opacity-70'
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
