import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { useAdmin } from '@/hooks/useAdmin';
import { useTheme } from '@/components/ThemeProvider';
import {
  Settings, ChevronLeft, Star, Users, Eye, Heart,
  LogOut, Shield, Moon, Sun, SunMoon, Globe,
  HelpCircle, Share2, MessageSquare, Bookmark,
  Crown, Gift, Gem, type LucideIcon
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { motion } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface StatProps { icon: LucideIcon; value: number; label: string; }
function StatBadge({ icon: Icon, value, label }: StatProps) {
  return (
    <div className="flex flex-col items-center gap-1">
      <div className="h-10 w-10 rounded-2xl bg-muted/60 flex items-center justify-center">
        <Icon className="h-4.5 w-4.5 text-muted-foreground" />
      </div>
      <span className="text-sm font-bold text-foreground">{value}</span>
      <span className="text-[10px] text-muted-foreground">{label}</span>
    </div>
  );
}

interface QuickLinkProps { icon: LucideIcon; label: string; to?: string; onClick?: () => void; badge?: string; }
function QuickLink({ icon: Icon, label, to, onClick, badge }: QuickLinkProps) {
  const inner = (
    <div className="flex items-center justify-between py-3.5 px-1 border-b border-border/30 last:border-0 active:bg-muted/30 transition-colors">
      <div className="flex items-center gap-3">
        <div className="h-9 w-9 rounded-xl bg-primary/8 flex items-center justify-center">
          <Icon className="h-4.5 w-4.5 text-primary" />
        </div>
        <span className="text-sm font-medium text-foreground">{label}</span>
      </div>
      <div className="flex items-center gap-2">
        {badge && <span className="text-[10px] bg-primary/10 text-primary px-2 py-0.5 rounded-full font-bold">{badge}</span>}
        <ChevronLeft className="h-4 w-4 text-muted-foreground" />
      </div>
    </div>
  );
  if (to) return <Link to={to}>{inner}</Link>;
  return <div onClick={onClick} className="cursor-pointer">{inner}</div>;
}

export default function Profile() {
  const { user, signOut } = useAuth();
  const { isAdmin } = useAdmin();
  const { theme, mode, setMode } = useTheme();
  const navigate = useNavigate();
  const [stats, setStats] = useState({ visitors: 0, friends: 0, followers: 0, following: 0 });
  const [loginStreak, setLoginStreak] = useState(0);

  // Load login streak
  useEffect(() => {
    const streakData = localStorage.getItem('login_streak');
    if (streakData) {
      try {
        const { count, lastDate } = JSON.parse(streakData);
        const today = new Date().toISOString().split('T')[0];
        const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
        if (lastDate === today) {
          setLoginStreak(count);
        } else if (lastDate === yesterday) {
          const newCount = count + 1;
          setLoginStreak(newCount);
          localStorage.setItem('login_streak', JSON.stringify({ count: newCount, lastDate: today }));
        } else {
          setLoginStreak(1);
          localStorage.setItem('login_streak', JSON.stringify({ count: 1, lastDate: today }));
        }
      } catch { setLoginStreak(1); }
    } else {
      const today = new Date().toISOString().split('T')[0];
      localStorage.setItem('login_streak', JSON.stringify({ count: 1, lastDate: today }));
      setLoginStreak(1);
    }
  }, []);

  const handleLogout = () => {
    signOut();
    toast.success('تم تسجيل الخروج');
    navigate('/');
  };

  const themeLabel = mode === 'auto' ? 'تلقائي' : mode === 'dark' ? 'ليلي' : 'نهاري';
  const ThemeIcon = mode === 'auto' ? SunMoon : mode === 'dark' ? Moon : Sun;

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="profile-page">
      {/* Header */}
      <div className="relative bg-gradient-to-br from-emerald-900 via-teal-800 to-green-900 px-5 pb-20 pt-safe-header overflow-hidden">
        <div className="absolute inset-0 opacity-[0.06]">
          <div className="absolute inset-0" style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.4\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")' }} />
        </div>

        {/* Top bar */}
        <div className="relative flex items-center justify-between mb-6 pt-4">
          <h1 className="text-lg font-bold text-white">حسابي</h1>
          <div className="flex items-center gap-2">
            {isAdmin && (
              <Link to="/admin" className="p-2 rounded-xl bg-white/10 backdrop-blur-sm" data-testid="admin-link">
                <Shield className="h-4.5 w-4.5 text-amber-400" />
              </Link>
            )}
            <Link to="/more" className="p-2 rounded-xl bg-white/10 backdrop-blur-sm">
              <Settings className="h-4.5 w-4.5 text-white/80" />
            </Link>
          </div>
        </div>

        {/* Profile info */}
        <div className="relative flex items-center gap-4">
          <div className="h-18 w-18 rounded-full bg-white/15 backdrop-blur-sm border-2 border-white/20 flex items-center justify-center">
            {user?.avatar ? (
              <img src={user.avatar} alt="" className="h-full w-full rounded-full object-cover" />
            ) : (
              <span className="text-3xl text-white/80">
                {user?.name?.[0] || user?.email?.[0] || '؟'}
              </span>
            )}
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">{user?.name || 'مستخدم'}</h2>
            <p className="text-white/50 text-xs mt-0.5">{user?.email || ''}</p>
            {loginStreak > 1 && (
              <span className="inline-flex items-center gap-1 mt-1.5 bg-amber-500/20 text-amber-300 text-[10px] px-2 py-0.5 rounded-full font-bold">
                <Gem className="h-3 w-3" />
                {loginStreak} يوم متتابع
              </span>
            )}
          </div>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Stats */}
      <div className="px-5 -mt-2 mb-4">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-3xl bg-card border border-border/40 p-5 shadow-sm"
        >
          <div className="grid grid-cols-4 gap-2">
            <StatBadge icon={Eye} value={stats.visitors} label="زوار" />
            <StatBadge icon={Users} value={stats.friends} label="أصدقاء" />
            <StatBadge icon={Heart} value={stats.followers} label="متابعين" />
            <StatBadge icon={Share2} value={stats.following} label="متابَعين" />
          </div>
        </motion.div>
      </div>

      {/* Membership Card */}
      <div className="px-5 mb-4">
        <div className="rounded-3xl bg-gradient-to-br from-amber-900/30 via-amber-800/20 to-yellow-900/10 border border-amber-500/20 p-5 relative overflow-hidden">
          <div className="absolute top-2 left-2 opacity-10">
            <Crown className="h-20 w-20 text-amber-400" />
          </div>
          <div className="relative">
            <div className="flex items-center gap-2 mb-2">
              <Crown className="h-5 w-5 text-amber-400" />
              <h3 className="text-sm font-bold text-amber-200">العضوية الاحترافية</h3>
            </div>
            <p className="text-[11px] text-amber-200/60 mb-3">
              بدون إعلانات + خصم ذهبي يومي + ميزات حصرية
            </p>
            <button
              data-testid="membership-btn"
              className="bg-amber-500 hover:bg-amber-400 text-amber-950 text-xs font-bold px-5 py-2 rounded-2xl transition-all active:scale-95"
            >
              انضم الآن
            </button>
          </div>
        </div>
      </div>

      {/* Quick Links */}
      <div className="px-5 mb-4">
        <div className="rounded-3xl bg-card border border-border/40 p-4">
          <QuickLink icon={Bookmark} label="المحفوظات" to="/favorites" />
          <QuickLink icon={Gift} label="المكافآت" to="/rewards" badge="جديد" />
          <QuickLink
            icon={ThemeIcon}
            label={`المظهر: ${themeLabel}`}
            onClick={() => setMode(mode === 'auto' ? 'light' : mode === 'light' ? 'dark' : 'auto')}
          />
          <QuickLink icon={Globe} label="اللغة" to="/more" badge="العربية" />
        </div>
      </div>

      <div className="px-5 mb-4">
        <div className="rounded-3xl bg-card border border-border/40 p-4">
          <QuickLink icon={Star} label="قيّمنا" onClick={() => toast.info('شكراً لدعمك!')} />
          <QuickLink icon={Share2} label="دعوة الأصدقاء" onClick={() => {
            if (navigator.share) {
              navigator.share({ title: 'المؤذن العالمي', text: 'تطبيق إسلامي شامل', url: window.location.origin });
            } else {
              navigator.clipboard.writeText(window.location.origin);
              toast.success('تم نسخ الرابط');
            }
          }} />
          <QuickLink icon={HelpCircle} label="الأسئلة الشائعة" to="/more" />
          <QuickLink icon={MessageSquare} label="تواصل معنا" onClick={() => toast.info('ادعمنا@almuadhin.com')} />
        </div>
      </div>

      {/* Login/Logout */}
      <div className="px-5 mb-8">
        {user ? (
          <button
            onClick={handleLogout}
            data-testid="logout-btn"
            className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl border border-red-500/20 bg-red-500/5 text-red-500 text-sm font-bold transition-all active:scale-[0.98]"
          >
            <LogOut className="h-4 w-4" />
            تسجيل الخروج
          </button>
        ) : (
          <Link
            to="/auth"
            data-testid="login-btn"
            className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl bg-primary text-primary-foreground text-sm font-bold transition-all active:scale-[0.98]"
          >
            تسجيل الدخول
          </Link>
        )}
      </div>
    </div>
  );
}
