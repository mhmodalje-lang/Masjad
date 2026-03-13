import { useLocation, Link } from 'react-router-dom';
import { Home, Clock, Users, MessageCircle, LayoutGrid } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const navItems = [
  { path: '/', icon: Home, label: 'الرئيسية', exact: true },
  { path: '/prayer-times', icon: Clock, label: 'الصلاة' },
  { path: '/sohba', icon: Users, label: 'صُحبة' },
  { path: '/messages', icon: MessageCircle, label: 'الرسائل' },
  { path: '/more', icon: LayoutGrid, label: 'المزيد' },
];

export function BottomNav() {
  const location = useLocation();

  return (
    <nav
      data-testid="bottom-nav"
      className="fixed bottom-0 left-0 right-0 z-50 border-t border-border/30 bg-card/90 backdrop-blur-2xl"
    >
      <div className="flex items-center justify-around pb-[env(safe-area-inset-bottom,0px)]" dir="rtl">
        {navItems.map((item) => {
          const isActive = item.exact
            ? location.pathname === item.path
            : location.pathname.startsWith(item.path);

          return (
            <Link
              key={item.path}
              to={item.path}
              data-testid={`nav-${item.path.replace('/', '') || 'home'}`}
              className={cn(
                'relative flex flex-col items-center gap-0.5 flex-1 py-2.5 transition-all duration-300 min-w-0',
                isActive ? 'text-primary' : 'text-muted-foreground hover:text-foreground'
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="nav-indicator"
                  className="absolute -top-px left-1/2 -translate-x-1/2 h-[3px] w-8 rounded-full bg-primary"
                  transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                />
              )}
              <item.icon className={cn('h-[22px] w-[22px] shrink-0 transition-transform', isActive && 'scale-110 stroke-[2.5px]')} />
              <span className="font-semibold text-[11px] leading-tight text-center truncate w-full px-0.5">
                {item.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
