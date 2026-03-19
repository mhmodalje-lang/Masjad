import { useLocation, Link } from 'react-router-dom';
import { Home, BookOpen, Plus, MessageSquare, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';

const navItems = [
  { path: '/', icon: Home, label: 'الرئيسية', exact: true },
  { path: '/stories', icon: BookOpen, label: 'حكاياتي' },
  { path: '/create', icon: Plus, label: '', isCreate: true },
  { path: '/messages', icon: MessageSquare, label: 'الرسائل' },
  { path: '/more', icon: User, label: 'المزيد' },
];

export function BottomNav() {
  const location = useLocation();
  const { user } = useAuth();

  const hiddenPaths = ['/auth', '/reels'];
  if (hiddenPaths.some(p => location.pathname.startsWith(p))) return null;

  return (
    <nav
      data-testid="bottom-nav"
      className="fixed bottom-0 left-0 right-0 z-50 bg-gradient-to-t from-emerald-900 via-emerald-800 to-emerald-700 shadow-2xl"
    >
      <div className="absolute inset-0 opacity-[0.07]" style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.3'%3E%3Cpath d='M20 18v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
      }} />
      <div className="relative flex items-center justify-around pb-[env(safe-area-inset-bottom,0px)]" dir="rtl">
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
                className="relative flex flex-col items-center gap-0.5 flex-1 py-1.5 min-w-0"
              >
                <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center shadow-lg shadow-emerald-500/30 active:scale-90 transition-transform border-2 border-emerald-300/30">
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
                'relative flex flex-col items-center gap-1 flex-1 py-2.5 transition-all duration-300 min-w-0',
                isActive ? 'text-white' : 'text-emerald-200/60 hover:text-emerald-100'
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="nav-indicator"
                  className="absolute top-0 inset-x-0 mx-auto h-[3px] w-8 rounded-b-full bg-emerald-300"
                  transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                />
              )}
              <item.icon className={cn(
                'h-[22px] w-[22px] shrink-0 transition-all duration-200',
                isActive && 'scale-110 stroke-[2.5px]'
              )} />
              <span className={cn(
                "text-[10px] leading-tight text-center truncate w-full px-0.5",
                isActive ? 'font-bold' : 'font-medium'
              )}>
                {item.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
