import { useAuth } from '@/hooks/useAuth';
import { useAdmin } from '@/hooks/useAdmin';
import { useTheme } from '@/components/ThemeProvider';
import { useDailyReminders } from '@/hooks/useDailyReminders';
import { useLocale } from '@/hooks/useLocale';
import { Link, useNavigate } from 'react-router-dom';
import {
  Compass, Heart, Calculator, User, LogIn, LogOut, Moon, Sun, BookOpen, Clock,
  CheckCircle2, Shield, Bell, BellOff, ShieldCheck, ChevronLeft, Star,
  Share2, HelpCircle, Crown, Settings, Gem, Eye, Users, MessageSquare, Coins,
  Bot, Store, ShoppingBag, Mail, Info, Award, Sparkles, TrendingUp
} from 'lucide-react';
import { cn } from '@/lib/utils';
import AthanSelector from '@/components/AthanSelector';
import { useFontSize } from '@/components/Features2026';
import { toast } from 'sonner';
import { useState, useEffect } from 'react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

const tools = [
  { icon: Compass, labelKey: 'qibla', path: '/qibla', color: 'text-amber-400', bg: 'bg-gradient-to-br from-amber-500/20 to-amber-600/10', emoji: '🧭' },
  { icon: Heart, labelKey: 'tasbih', path: '/tasbeeh', color: 'text-primary', bg: 'bg-gradient-to-br from-emerald-500/20 to-emerald-600/10', emoji: '📿' },
  { icon: Clock, labelKey: 'prayer', path: '/prayer-times', color: 'text-amber-500', bg: 'bg-gradient-to-br from-sky-500/20 to-sky-600/10', emoji: '🕌' },
  { icon: BookOpen, labelKey: 'quran', path: '/quran', color: 'text-primary', bg: 'bg-gradient-to-br from-green-500/20 to-green-600/10', emoji: '📖' },
  { icon: Moon, labelKey: 'duas', path: '/duas', color: 'text-purple-400', bg: 'bg-gradient-to-br from-purple-500/20 to-purple-600/10', emoji: '🤲' },
  { icon: ShieldCheck, labelKey: 'ruqyah', path: '/ruqyah', color: 'text-green-400', bg: 'bg-gradient-to-br from-teal-500/20 to-teal-600/10', emoji: '🛡️' },
  { icon: Calculator, labelKey: 'zakat', path: '/zakat', color: 'text-orange-400', bg: 'bg-gradient-to-br from-orange-500/20 to-orange-600/10', emoji: '💰' },
  { icon: CheckCircle2, labelKey: 'followUp', path: '/tracker', color: 'text-cyan-400', bg: 'bg-gradient-to-br from-cyan-500/20 to-cyan-600/10', emoji: '✅' },
  { icon: Star, labelKey: 'namesOfAllah', path: '/asma-al-husna', color: 'text-yellow-400', bg: 'bg-gradient-to-br from-yellow-500/20 to-yellow-600/10', emoji: '✨' },
];

export default function More() {
  const { user, signOut } = useAuth();
  const { isAdmin } = useAdmin();
  const { theme, mode, setMode } = useTheme();
  const { enabled: remindersEnabled, toggle: toggleReminders } = useDailyReminders();
  const { size: fontSize, increase: fontIncrease, decrease: fontDecrease } = useFontSize();
  const { locale, setLocale, t } = useLocale();
  const navigate = useNavigate();

  const handleToggleReminders = async () => {
    const result = await toggleReminders();
    if (result) toast.success(remindersEnabled ? 'تم إيقاف التذكيرات' : 'تم تفعيل التذكيرات');
    else toast.error('يرجى السماح بالإشعارات');
  };
  
  const languages = [
    { code: 'ar', name: 'العربية', nativeName: 'العربية', flag: '🇸🇦' },
    { code: 'en', name: 'English', nativeName: 'English', flag: '🇬🇧' },
    { code: 'ru', name: 'Russian', nativeName: 'Русский', flag: '🇷🇺' },
    { code: 'de', name: 'German', nativeName: 'Deutsch', flag: '🇩🇪' },
    { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷' },
    { code: 'tr', name: 'Turkish', nativeName: 'Türkçe', flag: '🇹🇷' },
  ];
  
  const currentLanguage = languages.find(l => l.code === locale) || languages[0];

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="more-page">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-12 flex items-center justify-between">
        <h1 className="text-lg font-black text-foreground">{t('more')}</h1>
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
          <Link to="/profile" className="flex items-center gap-4 p-4 rounded-2xl bg-card border border-border/30 active:scale-[0.98] transition-transform">
            <div className="h-14 w-14 rounded-full bg-gradient-to-br from-primary/30 to-primary/10 flex items-center justify-center shrink-0 ring-2 ring-primary/20">
              {user.avatar ? (
                <img src={user.avatar} alt="" className="h-full w-full rounded-full object-cover" />
              ) : (
                <span className="text-xl font-bold text-primary">{user.name?.[0] || user.email?.[0] || '؟'}</span>
              )}
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-base font-bold text-foreground truncate">{user.name || 'مستخدم'}</h2>
              <p className="text-xs text-muted-foreground truncate">{user.email}</p>
              <p className="text-[10px] text-primary font-semibold mt-0.5">{t('viewProfile')} ←</p>
            </div>
            <Link to="/account" onClick={(e) => e.stopPropagation()} className="p-2 rounded-xl bg-muted/50 hover:bg-muted">
              <Settings className="h-4 w-4 text-muted-foreground" />
            </Link>
          </Link>
        ) : (
          <Link to="/auth" className="flex items-center gap-3 p-4 rounded-2xl bg-card border border-primary/20 active:scale-[0.98] transition-transform">
            <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
              <LogIn className="h-5 w-5 text-primary" />
            </div>
            <div>
              <span className="text-sm font-bold text-foreground block">{t('loginSignup')}</span>
              <span className="text-xs text-muted-foreground">{t('loginPrompt')}</span>
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
            <p className="text-[13px] font-bold text-foreground">{t('rewards')}</p>
            <p className="text-[10px] text-muted-foreground">{t('collectPoints')}</p>
          </div>
        </Link>
        <Link to="/ai-assistant" className="rounded-2xl bg-card border border-border/30 p-3.5 flex items-center gap-3 active:scale-[0.97] transition-transform">
          <div className="h-10 w-10 rounded-xl bg-blue-500/10 flex items-center justify-center shrink-0">
            <Bot className="h-5 w-5 text-blue-400" />
          </div>
          <div>
            <p className="text-[13px] font-bold text-foreground">{t('aiAssistant')}</p>
            <p className="text-[10px] text-muted-foreground">{t('askAboutReligion')}</p>
          </div>
        </Link>
        <Link to="/store" className="rounded-2xl bg-card border border-border/30 p-3.5 flex items-center gap-3 active:scale-[0.97] transition-transform">
          <div className="h-10 w-10 rounded-xl bg-purple-500/10 flex items-center justify-center shrink-0">
            <Crown className="h-5 w-5 text-purple-400" />
          </div>
          <div>
            <p className="text-[13px] font-bold text-foreground">{t('shop')}</p>
            <p className="text-[10px] text-muted-foreground">{t('featuredItems')}</p>
          </div>
        </Link>
        <Link to="/marketplace" className="rounded-2xl bg-card border border-border/30 p-3.5 flex items-center gap-3 active:scale-[0.97] transition-transform">
          <div className="h-10 w-10 rounded-xl bg-teal-500/10 flex items-center justify-center shrink-0">
            <ShoppingBag className="h-5 w-5 text-teal-400" />
          </div>
          <div>
            <p className="text-[13px] font-bold text-foreground">{t('marketplace')}</p>
            <p className="text-[10px] text-muted-foreground">{t('islamicProducts')}</p>
          </div>
        </Link>
      </div>

      {/* Islamic Tools */}
      <div className="px-4 mb-4">
        <h3 className="text-[13px] font-bold text-foreground mb-3 flex items-center gap-2">
          <Sparkles className="h-3.5 w-3.5 text-primary" />{t('islamicTools')}
        </h3>
        <div className="rounded-2xl bg-card border border-border/30 p-3">
          <div className="grid grid-cols-3 gap-3">
            {tools.map((item, i) => (
              <Link key={i} to={item.path} className="flex flex-col items-center gap-1.5 py-2 active:scale-95 transition-transform rounded-xl hover:bg-muted/30">
                <div className={cn("h-14 w-14 rounded-2xl flex items-center justify-center shadow-sm border border-border/20", item.bg)}>
                  <span className="text-2xl">{(item as any).emoji}</span>
                </div>
                <span className="text-[11px] font-bold text-foreground text-center leading-tight">{t(item.labelKey)}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Settings */}
      <div className="px-4 mb-4">
        <h3 className="text-[13px] font-bold text-foreground mb-3 flex items-center gap-2">
          <Settings className="h-3.5 w-3.5 text-muted-foreground" />{t('settings')}
        </h3>
        <div className="rounded-2xl bg-card border border-border/30 divide-y divide-border/15">
          {/* Theme */}
          <button onClick={() => setMode(mode === 'auto' ? 'light' : mode === 'light' ? 'dark' : 'auto')}
            className="w-full flex items-center justify-between px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-lg bg-amber-500/15 flex items-center justify-center">
                {theme === 'dark' ? <Moon className="h-4 w-4 text-amber-400" /> : <Sun className="h-4 w-4 text-amber-500" />}
              </div>
              <span className="text-sm text-foreground">{t('theme')}</span>
            </div>
            <span className="text-xs font-bold text-primary px-2 py-0.5 rounded-full bg-primary/10">
              {mode === 'auto' ? t('auto') : mode === 'dark' ? t('dark') : t('light')}
            </span>
          </button>
          {/* Reminders */}
          <button onClick={handleToggleReminders}
            className="w-full flex items-center justify-between px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-lg bg-red-500/15 flex items-center justify-center">
                {remindersEnabled ? <Bell className="h-4 w-4 text-red-400" /> : <BellOff className="h-4 w-4 text-red-400" />}
              </div>
              <span className="text-sm text-foreground">{t('reminders')}</span>
            </div>
            <span className={cn('text-xs font-bold px-2 py-0.5 rounded-full',
              remindersEnabled ? 'text-green-500 bg-green-500/10' : 'text-muted-foreground bg-muted')}>
              {remindersEnabled ? t('enabled') : t('disabled')}
            </span>
          </button>
          {/* Notifications Settings */}
          <Link to="/notifications" className="flex items-center justify-between px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-lg bg-blue-500/15 flex items-center justify-center">
                <Bell className="h-4 w-4 text-blue-400" />
              </div>
              <span className="text-sm text-foreground">{t('notificationSettings')}</span>
            </div>
            <ChevronLeft className="h-4 w-4 text-muted-foreground/40" />
          </Link>
          {/* Font Size */}
          <div className="flex items-center justify-between px-4 py-3.5">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-lg bg-cyan-500/15 flex items-center justify-center">
                <span className="text-cyan-400 text-sm font-bold">أ</span>
              </div>
              <span className="text-sm text-foreground">{t('fontSize')}</span>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={fontDecrease} className="h-7 w-7 rounded-lg bg-muted/50 flex items-center justify-center text-xs font-bold text-foreground active:scale-90">-</button>
              <span className="text-xs font-bold text-primary w-6 text-center">{fontSize}</span>
              <button onClick={fontIncrease} className="h-7 w-7 rounded-lg bg-muted/50 flex items-center justify-center text-xs font-bold text-foreground active:scale-90">+</button>
            </div>
          </div>
          {/* Language Selector - Shows all languages as a grid */}
          <div className="px-4 py-3.5">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-lg bg-blue-500/15 flex items-center justify-center">
                  <span className="text-blue-400 text-sm font-bold">🌍</span>
                </div>
                <span className="text-sm font-bold text-foreground">{t('language')}</span>
              </div>
              {localStorage.getItem('user-selected-locale') && (
                <button onClick={() => {
                  localStorage.removeItem('user-selected-locale');
                  const detected = navigator.language?.split('-')[0] || 'ar';
                  setLocale(detected);
                  localStorage.removeItem('user-selected-locale');
                  toast.success(t('languageAutoDetected'));
                }} className="text-[10px] text-primary font-semibold px-2 py-1 rounded-lg bg-primary/10">
                  {t('resetToAuto')}
                </button>
              )}
            </div>
            {!localStorage.getItem('user-selected-locale') && (
              <p className="text-[10px] text-muted-foreground mb-2 px-1">🔄 {t('languageAutoDetected')}</p>
            )}
            <div className="grid grid-cols-3 gap-2">
              {languages.map(lang => (
                <button key={lang.code} onClick={() => { setLocale(lang.code); toast.success(`${t('languageChanged')}: ${lang.nativeName}`); }}
                  className={`flex flex-col items-center gap-1 p-2.5 rounded-xl border transition-all ${
                    locale === lang.code 
                      ? 'bg-primary/10 border-primary text-primary' 
                      : 'bg-card border-border/30 text-muted-foreground hover:border-primary/30'
                  }`}>
                  <span className="text-lg">{lang.flag}</span>
                  <span className="text-[11px] font-bold">{lang.nativeName}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Athan Selector */}
      <div className="px-4 mb-4">
        <h3 className="text-[13px] font-bold text-foreground mb-3 flex items-center gap-2">
          <Sparkles className="h-3.5 w-3.5 text-primary" />{t('athanSound')}
        </h3>
        <div className="rounded-2xl bg-card border border-border/30 p-4">
          <AthanSelector />
        </div>
      </div>

      {/* Help Section */}
      <div className="px-4 mb-4">
        <h3 className="text-[13px] font-bold text-foreground mb-3 flex items-center gap-2">
          <HelpCircle className="h-3.5 w-3.5 text-green-400" />{t('helpSupport')}
        </h3>
        <div className="rounded-2xl bg-card border border-border/30 divide-y divide-border/15">
          <Link to="/contact" className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-green-500/15 flex items-center justify-center"><Mail className="h-4 w-4 text-green-400" /></div>
            <span className="text-sm text-foreground">{t('contactUs')}</span>
            <ChevronLeft className="h-4 w-4 text-muted-foreground/40 mr-auto" />
          </Link>
          <Link to="/about" className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-purple-500/15 flex items-center justify-center"><Info className="h-4 w-4 text-purple-400" /></div>
            <span className="text-sm text-foreground">{t('aboutUs')}</span>
            <ChevronLeft className="h-4 w-4 text-muted-foreground/40 mr-auto" />
          </Link>
          <Link to="/privacy" className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-blue-500/15 flex items-center justify-center"><Shield className="h-4 w-4 text-blue-400" /></div>
            <span className="text-sm text-foreground">{t('privacyPolicy')}</span>
            <ChevronLeft className="h-4 w-4 text-muted-foreground/40 mr-auto" />
          </Link>
          <Link to="/terms" className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-indigo-500/15 flex items-center justify-center"><Shield className="h-4 w-4 text-indigo-400" /></div>
            <span className="text-sm text-foreground">{t('termsOfService')}</span>
            <ChevronLeft className="h-4 w-4 text-muted-foreground/40 mr-auto" />
          </Link>
          <button onClick={() => toast.info('⭐ شكراً لتقييمك!')} className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-yellow-500/15 flex items-center justify-center"><Star className="h-4 w-4 text-yellow-400" /></div>
            <span className="text-sm text-foreground">{t('rateApp')}</span>
          </button>
          <button onClick={() => {
            if (navigator.share) navigator.share({ title: t('appName'), url: window.location.origin });
            else { navigator.clipboard.writeText(window.location.origin); toast.success(t('linkCopied')); }
          }} className="w-full flex items-center gap-3 px-4 py-3.5 active:bg-muted/30 transition-colors">
            <div className="h-8 w-8 rounded-lg bg-blue-500/15 flex items-center justify-center"><Share2 className="h-4 w-4 text-blue-400" /></div>
            <span className="text-sm text-foreground">{t('inviteFriend')}</span>
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
            <p className="text-sm font-bold text-foreground">{t('donations')}</p>
            <p className="text-[10px] text-muted-foreground">{t('helpNeedy')}</p>
          </div>
          <ChevronLeft className="h-4 w-4 text-muted-foreground/40 mr-auto" />
        </Link>
      </div>

      {/* Logout */}
      {user && (
        <div className="px-4 mb-8">
          <button
            onClick={() => { signOut(); toast.success(t('loggedOut')); navigate('/'); }}
            data-testid="logout-btn"
            className="w-full flex items-center justify-center gap-2 py-3.5 rounded-2xl border border-red-500/20 bg-red-500/5 text-red-500 text-sm font-bold active:scale-[0.98] transition-all"
          >
            <LogOut className="h-4 w-4" /> {t('logout')}
          </button>
        </div>
      )}

      <p className="text-center text-[10px] text-muted-foreground/30 pb-4">{t('appName')} v2.0.0</p>
    </div>
  );
}
