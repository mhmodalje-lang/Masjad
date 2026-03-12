import { useAuth } from '@/hooks/useAuth';
import { useAdmin } from '@/hooks/useAdmin';
import { useTheme } from '@/components/ThemeProvider';
import { useDailyReminders } from '@/hooks/useDailyReminders';
import { Link, useNavigate } from 'react-router-dom';
import {
  Compass, Heart, Calculator, User, LogIn, LogOut, Moon, Sun, BookOpen, Clock,
  CheckCircle2, Shield, Bell, BellOff, ShieldCheck, ChevronLeft, Star,
  Share2, HelpCircle, Crown, Settings, Gem, Eye, Users, MessageSquare
} from 'lucide-react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import AthanSelector from '@/components/AthanSelector';
import { toast } from 'sonner';
import { useState, useEffect } from 'react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

const tools = [
  { icon: Compass, label: 'القبلة', path: '/qibla', color: 'text-teal-500', bg: 'bg-teal-500/10' },
  { icon: Heart, label: 'التسبيح', path: '/tasbeeh', color: 'text-amber-500', bg: 'bg-amber-500/10' },
  { icon: Clock, label: 'الصلاة', path: '/prayer-times', color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
  { icon: BookOpen, label: 'القرآن', path: '/quran', color: 'text-blue-500', bg: 'bg-blue-500/10' },
  { icon: Moon, label: 'الأدعية', path: '/duas', color: 'text-purple-500', bg: 'bg-purple-500/10' },
  { icon: ShieldCheck, label: 'الرقية', path: '/ruqyah', color: 'text-green-500', bg: 'bg-green-500/10' },
  { icon: Calculator, label: 'الزكاة', path: '/zakat', color: 'text-orange-500', bg: 'bg-orange-500/10' },
  { icon: CheckCircle2, label: 'المتابعة', path: '/tracker', color: 'text-cyan-500', bg: 'bg-cyan-500/10' },
];

interface QuickLinkProps { icon: typeof User; label: string; to?: string; onClick?: () => void; trailing?: React.ReactNode; }
function QuickLink({ icon: Icon, label, to, onClick, trailing }: QuickLinkProps) {
  const inner = (
    <div className="flex items-center justify-between py-3 px-1 border-b border-border/20 last:border-0">
      <div className="flex items-center gap-3">
        <Icon className="h-4.5 w-4.5 text-muted-foreground" />
        <span className="text-sm text-foreground">{label}</span>
      </div>
      {trailing || <ChevronLeft className="h-4 w-4 text-muted-foreground/40" />}
    </div>
  );
  if (to) return <Link to={to}>{inner}</Link>;
  return <div onClick={onClick} className="cursor-pointer active:bg-muted/30 rounded-lg transition-colors">{inner}</div>;
}

export default function More() {
  const { user, signOut } = useAuth();
  const { isAdmin } = useAdmin();
  const { theme, mode, setMode } = useTheme();
  const { enabled: remindersEnabled, toggle: toggleReminders } = useDailyReminders();
  const navigate = useNavigate();
  const [stats, setStats] = useState({ posts: 0, followers: 0, following: 0 });
  const [loginStreak, setLoginStreak] = useState(0);

  useEffect(() => {
    if (!user) return;
    const token = localStorage.getItem('auth_token');
    if (!token) return;
    fetch(`${BACKEND_URL}/api/sohba/my-stats`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.ok ? r.json() : null)
      .then(d => { if (d) setStats(d); })
      .catch(() => {});
  }, [user]);

  useEffect(() => {
    const streakData = localStorage.getItem('login_streak');
    const today = new Date().toISOString().split('T')[0];
    if (streakData) {
      try {
        const { count, lastDate } = JSON.parse(streakData);
        if (lastDate === today) { setLoginStreak(count); }
        else {
          const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
          const newCount = lastDate === yesterday ? count + 1 : 1;
          setLoginStreak(newCount);
          localStorage.setItem('login_streak', JSON.stringify({ count: newCount, lastDate: today }));
        }
      } catch { setLoginStreak(1); }
    } else {
      localStorage.setItem('login_streak', JSON.stringify({ count: 1, lastDate: today }));
      setLoginStreak(1);
    }
  }, []);

  const handleToggleReminders = async () => {
    const result = await toggleReminders();
    if (result) { toast.success(remindersEnabled ? 'تم إيقاف التذكيرات' : 'تم تفعيل التذكيرات'); }
    else { toast.error('يرجى السماح بالإشعارات'); }
  };

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="more-page">
      {/* Profile Section */}
      <div className="relative bg-gradient-to-br from-emerald-900 via-teal-800 to-green-900 px-5 pb-16 pt-safe-header overflow-hidden">
        <div className="absolute inset-0 opacity-[0.05]" style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'40\' height=\'40\' viewBox=\'0 0 40 40\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23fff\' fill-opacity=\'.3\'%3E%3Cpath d=\'M20 0l5 10h10l-8 6 3 10-10-7-10 7 3-10-8-6h10z\'/%3E%3C/g%3E%3C/svg%3E")' }} />
        <div className="relative flex items-center justify-between mb-5 pt-3">
          <h1 className="text-lg font-bold text-white">المزيد</h1>
          <div className="flex items-center gap-2">
            {isAdmin && (
              <Link to="/admin" className="p-2 rounded-xl bg-white/10" data-testid="admin-link">
                <Shield className="h-4 w-4 text-amber-400" />
              </Link>
            )}
            <Link to="/notifications" className="p-2 rounded-xl bg-white/10">
              <Settings className="h-4 w-4 text-white/70" />
            </Link>
          </div>
        </div>

        {user ? (
          <div className="relative flex items-center gap-4">
            <div className="h-16 w-16 rounded-full bg-white/15 border-2 border-white/20 flex items-center justify-center shrink-0">
              {user.avatar ? (
                <img src={user.avatar} alt="" className="h-full w-full rounded-full object-cover" />
              ) : (
                <span className="text-2xl text-white/80">{user.name?.[0] || user.email?.[0] || '؟'}</span>
              )}
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-lg font-bold text-white truncate">{user.name || 'مستخدم'}</h2>
              <p className="text-white/40 text-xs truncate">{user.email}</p>
              {loginStreak > 1 && (
                <span className="inline-flex items-center gap-1 mt-1 bg-amber-500/20 text-amber-300 text-[10px] px-2 py-0.5 rounded-full font-bold">
                  <Gem className="h-3 w-3" /> {loginStreak} يوم متتابع
                </span>
              )}
            </div>
          </div>
        ) : (
          <Link to="/auth" className="relative flex items-center gap-3 bg-white/10 rounded-2xl p-4 active:scale-[0.98] transition-transform">
            <LogIn className="h-5 w-5 text-white" />
            <span className="text-white font-bold text-sm">تسجيل الدخول / إنشاء حساب</span>
          </Link>
        )}
        <div className="absolute -bottom-5 left-0 right-0 h-10 rounded-t-[2rem] bg-background" />
      </div>

      {/* Stats */}
      {user && (
        <div className="px-5 -mt-1 mb-4">
          <div className="rounded-2xl bg-card border border-border/30 p-4 flex items-center justify-around">
            <div className="text-center"><span className="text-sm font-bold text-foreground">{stats.posts}</span><p className="text-[10px] text-muted-foreground">منشورات</p></div>
            <div className="w-px h-8 bg-border/30" />
            <div className="text-center"><span className="text-sm font-bold text-foreground">{stats.followers}</span><p className="text-[10px] text-muted-foreground">متابعين</p></div>
            <div className="w-px h-8 bg-border/30" />
            <div className="text-center"><span className="text-sm font-bold text-foreground">{stats.following}</span><p className="text-[10px] text-muted-foreground">متابَعين</p></div>
          </div>
        </div>
      )}

      {/* Tools Grid */}
      <div className="px-5 mb-4">
        <h3 className="text-sm font-bold text-foreground mb-3">الأدوات الإسلامية</h3>
        <div className="rounded-2xl bg-card border border-border/30 p-4">
          <div className="grid grid-cols-4 gap-4">
            {tools.map((item, i) => (
              <Link key={i} to={item.path} className="flex flex-col items-center gap-1.5 active:scale-95 transition-transform">
                <div className={cn('h-12 w-12 rounded-2xl flex items-center justify-center', item.bg)}>
                  <item.icon className={cn('h-5 w-5', item.color)} />
                </div>
                <span className="text-[10px] font-medium text-foreground text-center">{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Settings */}
      <div className="px-5 mb-4">
        <h3 className="text-sm font-bold text-foreground mb-3">الإعدادات</h3>
        <div className="rounded-2xl bg-card border border-border/30 px-4">
          <QuickLink icon={user ? User : LogIn} label={user ? 'حسابي' : 'تسجيل الدخول'} to={user ? '/account' : '/auth'} />
          <QuickLink
            icon={theme === 'dark' ? Moon : Sun}
            label={`المظهر: ${mode === 'auto' ? 'تلقائي' : mode === 'dark' ? 'ليلي' : 'نهاري'}`}
            onClick={() => setMode(mode === 'auto' ? 'light' : mode === 'light' ? 'dark' : 'auto')}
            trailing={
              <span className={cn('text-[10px] font-bold px-2 py-0.5 rounded-full',
                theme === 'dark' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-600'
              )}>{mode === 'auto' ? 'تلقائي' : mode === 'dark' ? 'ليلي' : 'نهاري'}</span>
            }
          />
          <QuickLink
            icon={remindersEnabled ? Bell : BellOff}
            label="التذكيرات اليومية"
            onClick={handleToggleReminders}
            trailing={
              <span className={cn('text-[10px] font-bold px-2 py-0.5 rounded-full', remindersEnabled ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground')}>
                {remindersEnabled ? 'مفعّل' : 'معطّل'}
              </span>
            }
          />
        </div>
      </div>

      {/* Athan */}
      <div className="px-5 mb-4">
        <div className="rounded-2xl bg-card border border-border/30 p-4">
          <h3 className="text-sm font-bold text-foreground mb-3">صوت الأذان</h3>
          <AthanSelector />
        </div>
      </div>

      {/* Quick Links */}
      <div className="px-5 mb-4">
        <div className="rounded-2xl bg-card border border-border/30 px-4">
          <QuickLink icon={Star} label="قيّمنا" onClick={() => toast.info('شكراً لدعمك!')} />
          <QuickLink icon={Share2} label="دعوة صديق" onClick={() => {
            if (navigator.share) navigator.share({ title: 'المؤذن العالمي', url: window.location.origin });
            else { navigator.clipboard.writeText(window.location.origin); toast.success('تم نسخ الرابط'); }
          }} />
          <QuickLink icon={HelpCircle} label="المساعدة والدعم" onClick={() => toast.info('ادعمنا@almuadhin.com')} />
        </div>
      </div>

      {/* Logout */}
      {user && (
        <div className="px-5 mb-8">
          <button
            onClick={() => { signOut(); toast.success('تم تسجيل الخروج'); navigate('/'); }}
            data-testid="logout-btn"
            className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl border border-red-500/20 bg-red-500/5 text-red-500 text-sm font-bold active:scale-[0.98] transition-all"
          >
            <LogOut className="h-4 w-4" /> تسجيل الخروج
          </button>
        </div>
      )}
    </div>
  );
}
