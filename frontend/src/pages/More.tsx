import { useAuth } from '@/hooks/useAuth';
import { useAdmin } from '@/hooks/useAdmin';
import { useTheme } from '@/components/ThemeProvider';
import { useDailyReminders } from '@/hooks/useDailyReminders';
import { Link, useNavigate } from 'react-router-dom';
import {
  Compass, Heart, Calculator, User, LogIn, LogOut, Moon, Sun, BookOpen, Clock,
  CheckCircle2, Shield, Bell, BellOff, ShieldCheck, ChevronLeft, Star,
  Share2, HelpCircle, Crown, Settings, Gem, Eye, Users, MessageSquare, Coins,
  Bot, Store, ShoppingBag, Mail, Info, Award, Sparkles, TrendingUp
} from 'lucide-react';
import { cn } from '@/lib/utils';
import AthanSelector from '@/components/AthanSelector';
import { toast } from 'sonner';
import { useState, useEffect } from 'react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

const tools = [
  { icon: Compass, label: 'القبلة', path: '/qibla', color: 'text-amber-400', bg: 'bg-amber-500/15' },
  { icon: Heart, label: 'التسبيح', path: '/tasbeeh', color: 'text-primary', bg: 'bg-primary/15' },
  { icon: Clock, label: 'الصلاة', path: '/prayer-times', color: 'text-amber-500', bg: 'bg-amber-500/15' },
  { icon: BookOpen, label: 'القرآن', path: '/quran', color: 'text-primary', bg: 'bg-primary/15' },
  { icon: Moon, label: 'الأدعية', path: '/duas', color: 'text-purple-400', bg: 'bg-purple-400/15' },
  { icon: ShieldCheck, label: 'الرقية', path: '/ruqyah', color: 'text-green-400', bg: 'bg-green-500/15' },
  { icon: Calculator, label: 'الزكاة', path: '/zakat', color: 'text-orange-400', bg: 'bg-orange-500/15' },
  { icon: CheckCircle2, label: 'المتابعة', path: '/tracker', color: 'text-cyan-400', bg: 'bg-cyan-500/15' },
  { icon: Star, label: 'أسماء الله', path: '/asma-al-husna', color: 'text-yellow-400', bg: 'bg-yellow-500/15' },
];

export default function More() {
  const { user, signOut } = useAuth();
  const { isAdmin } = useAdmin();
  const { theme, mode, setMode } = useTheme();
  const { enabled: remindersEnabled, toggle: toggleReminders } = useDailyReminders();
  const navigate = useNavigate();

  const handleToggleReminders = async () => {
    const result = await toggleReminders();
    if (result) toast.success(remindersEnabled ? 'تم إيقاف التذكيرات' : 'تم تفعيل التذكيرات');
    else toast.error('يرجى السماح بالإشعارات');
  };

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="more-page">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-12 flex items-center justify-between">
        <h1 className="text-lg font-black text-foreground">المزيد</h1>
        <div className="flex items-center gap-1">
          {isAdmin && (
            <Link to="/admin" className="p-2.5 rounded-xl hover:bg-muted/50" data-testid="admin-link">
              <Shield className="h-[18px] w-[18px] text-primary" />
            </Link>
          )}
        </div>
      </div>

      {/* User Card */}
      <div className="px-4 pt-4 pb-3">
        {user ? (
          <div className="flex items-center gap-4 p-4 rounded-2xl bg-card border border-border/30">
            <div className="h-14 w-14 rounded-full bg-gradient-to-br from-primary/30 to-primary/10 flex items-center justify-center shrink-0">
              {user.avatar ? (
                <img src={user.avatar} alt="" className="h-full w-full rounded-full object-cover" />
              ) : (
                <span className="text-xl font-bold text-primary">{user.name?.[0] || user.email?.[0] || '؟'}</span>
              )}
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-base font-bold text-foreground truncate">{user.name || 'مستخدم'}</h2>
              <p className="text-xs text-muted-foreground truncate">{user.email}</p>
            </div>
            <Link to="/account" className="p-2 rounded-xl bg-muted/50 hover:bg-muted">
              <Settings className="h-4 w-4 text-muted-foreground" />
            </Link>
          </div>
        ) : (
          <Link to="/auth" className="flex items-center gap-3 p-4 rounded-2xl bg-card border border-primary/20 active:scale-[0.98] transition-transform">
            <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
              <LogIn className="h-5 w-5 text-primary" />
            </div>
            <div>
              <span className="text-sm font-bold text-foreground block">تسجيل الدخول</span>
              <span className="text-xs text-muted-foreground">سجّل للوصول لكل الميزات</span>
            </div>
          </Link>
        )}
      </div>

      {/* Quick Features */}
      <div className="px-4 mb-4 grid grid-cols-2 gap-2.5">
        <Link to="/rewards" className="rounded-2xl bg-card border border-border/30 p-3.5 flex items-center gap-3 active:scale-[0.97] transition-transform">
          <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
            <Coins className="h-5 w-5 text-primary" />
          </div>
          <div>
            <p className="text-[13px] font-bold text-foreground">المكافآت</p>
            <p className="text-[10px] text-muted-foreground">اجمع النقاط</p>
          </div>
        </Link>
        <Link to="/ai-assistant" className="rounded-2xl bg-card border border-border/30 p-3.5 flex items-center gap-3 active:scale-[0.97] transition-transform">
          <div className="h-10 w-10 rounded-xl bg-blue-500/10 flex items-center justify-center shrink-0">
            <Bot className="h-5 w-5 text-blue-400" />
          </div>
          <div>
            <p className="text-[13px] font-bold text-foreground">المساعد الذكي</p>
            <p className="text-[10px] text-muted-foreground">اسأل عن دينك</p>
          </div>
        </Link>
        <Link to="/store" className="rounded-2xl bg-card border border-border/30 p-3.5 flex items-center gap-3 active:scale-[0.97] transition-transform">
          <div className="h-10 w-10 rounded-xl bg-purple-500/10 flex items-center justify-center shrink-0">
            <Crown className="h-5 w-5 text-purple-400" />
          </div>
          <div>
            <p className="text-[13px] font-bold text-foreground">المتجر</p>
            <p className="text-[10px] text-muted-foreground">عناصر مميزة</p>
          </div>
        </Link>
        <Link to="/marketplace" className="rounded-2xl bg-card border border-border/30 p-3.5 flex items-center gap-3 active:scale-[0.97] transition-transform">
          <div className="h-10 w-10 rounded-xl bg-teal-500/10 flex items-center justify-center shrink-0">
            <ShoppingBag className="h-5 w-5 text-teal-400" />
          </div>
          <div>
            <p className="text-[13px] font-bold text-foreground">السوق</p>
            <p className="text-[10px] text-muted-foreground">منتجات إسلامية</p>
          </div>
        </Link>
      </div>

      {/* Islamic Tools */}
      <div className="px-4 mb-4">
        <h3 className="text-[13px] font-bold text-foreground mb-3 flex items-center gap-2">
          <Sparkles className="h-3.5 w-3.5 text-primary" />الأدوات الإسلامية
        </h3>
        <div className="rounded-2xl bg-card border border-border/30 p-3">
          <div className="grid grid-cols-3 gap-3">
            {tools.map((item, i) => (
              <Link key={i} to={item.path} className="flex flex-col items-center gap-1.5 py-2 active:scale-95 transition-transform rounded-xl hover:bg-muted/30">
                <div className={cn('h-11 w-11 rounded-xl flex items-center justify-center', item.bg)}>
                  <item.icon className={cn('h-5 w-5', item.color)} />
                </div>
                <span className="text-[10px] font-medium text-foreground text-center leading-tight">{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Settings */}
      <div className="px-4 mb-4">
        <h3 className="text-[13px] font-bold text-foreground mb-3 flex items-center gap-2">
          <Settings className="h-3.5 w-3.5 text-muted-foreground" />الإعدادات
        </h3>
        <div className="rounded-2xl bg-card border border-border/30 divide-y divide-border/15">
          {/* Theme */}
          <button onClick={() => setMode(mode === 'auto' ? 'light' : mode === 'light' ? 'dark' : 'auto')}
            className="w-full flex items-center justify-between px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-lg bg-amber-500/15 flex items-center justify-center">
                {theme === 'dark' ? <Moon className="h-4 w-4 text-amber-400" /> : <Sun className="h-4 w-4 text-amber-500" />}
              </div>
              <span className="text-sm text-foreground">المظهر</span>
            </div>
            <span className="text-xs font-bold text-primary px-2 py-0.5 rounded-full bg-primary/10">
              {mode === 'auto' ? 'تلقائي' : mode === 'dark' ? 'ليلي' : 'نهاري'}
            </span>
          </button>
          {/* Reminders */}
          <button onClick={handleToggleReminders}
            className="w-full flex items-center justify-between px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-lg bg-red-500/15 flex items-center justify-center">
                {remindersEnabled ? <Bell className="h-4 w-4 text-red-400" /> : <BellOff className="h-4 w-4 text-red-400" />}
              </div>
              <span className="text-sm text-foreground">التذكيرات</span>
            </div>
            <span className={cn('text-xs font-bold px-2 py-0.5 rounded-full',
              remindersEnabled ? 'text-green-500 bg-green-500/10' : 'text-muted-foreground bg-muted')}>
              {remindersEnabled ? 'مفعّل' : 'معطّل'}
            </span>
          </button>
          {/* Notifications Settings */}
          <Link to="/notifications" className="flex items-center justify-between px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-lg bg-blue-500/15 flex items-center justify-center">
                <Bell className="h-4 w-4 text-blue-400" />
              </div>
              <span className="text-sm text-foreground">إعدادات الإشعارات</span>
            </div>
            <ChevronLeft className="h-4 w-4 text-muted-foreground/40" />
          </Link>
        </div>
      </div>

      {/* Athan Selector */}
      <div className="px-4 mb-4">
        <h3 className="text-[13px] font-bold text-foreground mb-3 flex items-center gap-2">
          <Sparkles className="h-3.5 w-3.5 text-primary" />صوت الأذان
        </h3>
        <div className="rounded-2xl bg-card border border-border/30 p-4">
          <AthanSelector />
        </div>
      </div>

      {/* Help Section */}
      <div className="px-4 mb-4">
        <h3 className="text-[13px] font-bold text-foreground mb-3 flex items-center gap-2">
          <HelpCircle className="h-3.5 w-3.5 text-green-400" />المساعدة والدعم
        </h3>
        <div className="rounded-2xl bg-card border border-border/30 divide-y divide-border/15">
          <Link to="/contact" className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-green-500/15 flex items-center justify-center"><Mail className="h-4 w-4 text-green-400" /></div>
            <span className="text-sm text-foreground">تواصل معنا</span>
            <ChevronLeft className="h-4 w-4 text-muted-foreground/40 mr-auto" />
          </Link>
          <Link to="/about" className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-purple-500/15 flex items-center justify-center"><Info className="h-4 w-4 text-purple-400" /></div>
            <span className="text-sm text-foreground">من نحن</span>
            <ChevronLeft className="h-4 w-4 text-muted-foreground/40 mr-auto" />
          </Link>
          <Link to="/privacy" className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-blue-500/15 flex items-center justify-center"><Shield className="h-4 w-4 text-blue-400" /></div>
            <span className="text-sm text-foreground">سياسة الخصوصية</span>
            <ChevronLeft className="h-4 w-4 text-muted-foreground/40 mr-auto" />
          </Link>
          <button onClick={() => toast.info('⭐ شكراً لتقييمك!')} className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-yellow-500/15 flex items-center justify-center"><Star className="h-4 w-4 text-yellow-400" /></div>
            <span className="text-sm text-foreground">قيّم التطبيق</span>
          </button>
          <button onClick={() => {
            if (navigator.share) navigator.share({ title: 'أذان وحكاية', url: window.location.origin });
            else { navigator.clipboard.writeText(window.location.origin); toast.success('تم نسخ الرابط'); }
          }} className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-blue-500/15 flex items-center justify-center"><Share2 className="h-4 w-4 text-blue-400" /></div>
            <span className="text-sm text-foreground">دعوة صديق</span>
          </button>
        </div>
      </div>

      {/* Donations */}
      <div className="px-4 mb-4">
        <Link to="/donations" className="flex items-center gap-4 p-4 rounded-2xl bg-gradient-to-r from-red-500/10 to-rose-500/5 border border-red-500/20 active:scale-[0.98] transition-transform">
          <div className="h-12 w-12 rounded-xl bg-red-500/15 flex items-center justify-center shrink-0">
            <Heart className="h-6 w-6 text-red-400" />
          </div>
          <div>
            <p className="text-sm font-bold text-foreground">التبرعات والمساعدة</p>
            <p className="text-[10px] text-muted-foreground">ساعد المحتاجين - ادعُ لوالديّ</p>
          </div>
          <ChevronLeft className="h-4 w-4 text-muted-foreground/40 mr-auto" />
        </Link>
      </div>

      {/* Logout */}
      {user && (
        <div className="px-4 mb-8">
          <button
            onClick={() => { signOut(); toast.success('تم تسجيل الخروج'); navigate('/'); }}
            data-testid="logout-btn"
            className="w-full flex items-center justify-center gap-2 py-3.5 rounded-2xl border border-red-500/20 bg-red-500/5 text-red-500 text-sm font-bold active:scale-[0.98] transition-all"
          >
            <LogOut className="h-4 w-4" /> تسجيل الخروج
          </button>
        </div>
      )}

      <p className="text-center text-[10px] text-muted-foreground/30 pb-4">أذان وحكاية v2.0.0</p>
    </div>
  );
}
