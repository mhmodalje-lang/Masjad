import { useLocation, Link } from 'react-router-dom';
import { Home, Search, Plus, BookOpen, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { useLocale } from '@/hooks/useLocale';

const navItems = [
  { path: '/', icon: Home, labelKey: 'home', exact: true },
  { path: '/explore', icon: Search, labelKey: 'explore' },
  { path: '/create', icon: Plus, labelKey: '', isCreate: true },
  { path: '/stories', icon: BookOpen, labelKey: 'stories' },
  { path: '/more', icon: User, labelKey: 'morePage' },
];

export function BottomNav() {
  const location = useLocation();
  const { user } = useAuth();
  const { t, dir } = useLocale();

  const hiddenPaths = ['/auth'];
  if (hiddenPaths.some(p => location.pathname.startsWith(p))) return null;

  return (
    <nav
      data-testid="bottom-nav"
      className="fixed bottom-0 left-0 right-0 z-50 border-t border-border/40 bg-background/90 backdrop-blur-xl"
    >
      <div className="flex items-center justify-around pb-[env(safe-area-inset-bottom,0px)]" dir={dir}>
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
                className="relative flex flex-col items-center gap-0.5 flex-1 py-1.5 transition-all min-w-0"
              >
                <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-primary via-primary to-accent flex items-center justify-center shadow-lg shadow-primary/25 transition-transform active:scale-90">
                  <Plus className="h-6 w-6 text-primary-foreground stroke-[2.5px]" />
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
                'relative flex flex-col items-center gap-1 flex-1 py-2.5 transition-all duration-300 min-w-0',
                isActive ? 'text-primary' : 'text-muted-foreground hover:text-foreground'
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="nav-indicator"
                  className="absolute top-0 inset-x-0 mx-auto h-[3px] w-8 rounded-b-full bg-primary"
                  transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                />
              )}
              <item.icon className={cn(
                'h-[22px] w-[22px] shrink-0 transition-all duration-200',
                isActive && 'scale-110 stroke-[2.5px]'
              )} />
              <span className={cn(
                "text-[10px] leading-tight text-center truncate w-full px-0.5 transition-all",
                isActive ? 'font-bold' : 'font-medium'
              )}>
                {t(item.labelKey)}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
