import React, { memo } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Home, BookOpen, Plus, GraduationCap, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useLocale } from '@/hooks/useLocale';
import { useTheme } from '@/components/ThemeProvider';
import { hapticFeedback } from '@/lib/nativeBridge';

export const BottomNav = memo(function BottomNav() {
  const location = useLocation();
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  const navItems = [
    { path: '/', icon: Home, label: t('navHome'), exact: true },
    { path: '/stories', icon: BookOpen, label: t('navStories') },
    { path: '/create', icon: Plus, label: '', isCreate: true },
    { path: '/kids-zone', icon: GraduationCap, label: t('navAcademy') },
    { path: '/more', icon: User, label: t('navMore') },
  ];

  const hiddenPaths = ['/auth', '/reels', '/privacy', '/terms', '/about', '/contact', '/delete-data', '/content-policy'];
  if (hiddenPaths.some(p => location.pathname.startsWith(p))) return null;

  return (
    <nav
      data-testid="bottom-nav"
      className="fixed bottom-0 left-0 right-0 z-50 contain-layout"
    >
      {/* Mystic Glass Bar */}
      <div className={cn(
        'glass-nav border-t transition-colors duration-300',
        isDark
          ? 'bg-[hsl(154,35%,8%)]/95 border-[hsl(43,82%,52%)]/[0.1] shadow-[0_-4px_30px_rgba(0,30,15,0.6)]'
          : 'bg-[hsl(32,30%,84%)]/95 border-[hsl(28,30%,60%)]/[0.15] shadow-[0_-4px_30px_rgba(60,40,20,0.08)]'
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
                  onClick={() => hapticFeedback('medium')}
                  className="relative flex flex-col items-center -mt-5"
                >
                  <div
                    className={cn(
                      'h-[52px] w-[52px] rounded-full flex items-center justify-center active:scale-[0.88] transition-transform duration-150',
                      'bg-gradient-to-br from-[hsl(152,55%,22%)] to-[hsl(155,50%,30%)]',
                      'shadow-[0_4px_20px_-2px_hsl(152,55%,22%,0.5)]',
                      'border-[3px]',
                      isDark 
                        ? 'border-[hsl(154,35%,8%)] ring-2 ring-[hsl(43,82%,52%)]/25' 
                        : 'border-[hsl(32,30%,84%)] ring-2 ring-[hsl(152,55%,22%)]/15'
                    )}
                  >
                    <Plus className="h-6 w-6 text-white stroke-[2.5px]" />
                  </div>
                </Link>
              );
            }

            return (
              <Link
                key={item.path}
                to={item.path}
                data-testid={`nav-${item.path.replace('/', '') || 'home'}`}
                onClick={() => hapticFeedback('selection')}
                className={cn(
                  'relative flex flex-col items-center gap-1 py-1.5 px-3 rounded-2xl transition-colors duration-200 min-w-[60px]',
                  isActive
                    ? isDark ? 'text-[hsl(43,82%,52%)]' : 'text-[hsl(152,55%,22%)]'
                    : isDark ? 'text-[hsl(37,28%,55%)] active:text-white/80' : 'text-muted-foreground active:text-foreground'
                )}
              >
                {/* Active indicator — simple CSS, no layoutId */}
                {isActive && (
                  <div
                    className={cn(
                      'absolute -top-1 h-[3px] w-6 rounded-full transition-opacity duration-200',
                      isDark 
                        ? 'bg-gradient-to-r from-transparent via-[hsl(43,82%,52%)] to-transparent shadow-[0_0_12px_hsl(43,82%,52%,0.5)]' 
                        : 'bg-gradient-to-r from-transparent via-[hsl(152,55%,22%)] to-transparent shadow-[0_0_12px_hsl(152,55%,22%,0.3)]'
                    )}
                  />
                )}
                {/* Icon */}
                <div className={cn(
                  'h-8 w-8 rounded-xl flex items-center justify-center transition-all duration-200',
                  isActive
                    ? isDark 
                      ? 'bg-[hsl(43,82%,52%)]/12 scale-110' 
                      : 'bg-[hsl(152,55%,22%)]/8 scale-110'
                    : 'bg-transparent scale-100'
                )}>
                  <item.icon className={cn(
                    'h-[22px] w-[22px] transition-all duration-200',
                    isActive ? 'stroke-[2.5px]' : 'stroke-[1.8px]'
                  )} />
                </div>
                {/* Label */}
                <span className={cn(
                  "text-[11px] leading-tight text-center truncate max-w-[68px] transition-all duration-200",
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
});
