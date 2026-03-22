import { useState, useEffect, useCallback, lazy, Suspense } from 'react';
import DuaOfDayDrawer from '@/components/DuaOfDayDrawer';
import { dailyDuas } from '@/data/dhikrDetails';
import { useLocale } from '@/hooks/useLocale';
import { useAuth } from '@/hooks/useAuth';
import { useUnifiedPrayer } from '@/hooks/useUnifiedPrayer';
import { useAthanNotifications, requestNotificationPermission } from '@/hooks/useAthanNotifications';
import OccasionAthanAlert from '@/components/OccasionAthanAlert';
import OccasionBanner from '@/components/OccasionBanner';
import DailyGoals from '@/components/DailyGoals';
import NotificationCard from '@/components/NotificationCard';
import IslamicAd from '@/components/IslamicAd';
import { Link } from 'react-router-dom';
import { Compass, BookOpen, Heart, Calculator, Moon, Bell, BellOff, ChevronLeft, MessageSquare, Zap, Building2, Unlink, MapPin, MapPinOff, User, Volume2, Megaphone, X, Search, Settings as SettingsIcon } from 'lucide-react';
import { AdBanner } from '@/components/AdBanner';
import { VerseOfDay, StreakBadge } from '@/components/Features2026';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
const meccaImage = '/mecca-hero.webp';
import { getCurrentOccasion, isRamadan } from '@/data/islamicOccasions';
import { subscribeToPush, unsubscribeFromPush, updatePushMosqueTimes } from '@/lib/pushSubscription';
import { useSearchParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
const FeaturedVideos = lazy(() => import('@/components/FeaturedVideos'));
const NativeAdCard = lazy(() => import('@/components/NativeAdCard'));

// Lazy load below-the-fold components
const DailyHadith = lazy(() => import('@/components/DailyHadith'));
const QuranPlayer = lazy(() => import('@/components/QuranPlayer'));
const SuggestedGoals = lazy(() => import('@/components/SuggestedGoals'));
const HijriCalendar = lazy(() => import('@/components/HijriCalendar'));

const getQuickAccessItems = (t: (key: string) => string) => [
  { icon: Heart, label: t('quickTasbeeh'), path: '/tasbeeh', emoji: '📿', color: 'from-emerald-500/15 to-emerald-600/5' },
  { icon: Compass, label: t('quickQibla'), path: '/qibla', emoji: '🧭', color: 'from-blue-500/15 to-blue-600/5' },
  { icon: BookOpen, label: t('quickQuran'), path: '/quran', emoji: '📖', color: 'from-green-500/15 to-green-600/5' },
  { icon: Moon, label: t('quickDuas'), path: '/duas', emoji: '🤲', color: 'from-purple-500/15 to-purple-600/5' },
  { icon: MessageSquare, label: t('quickStories'), path: '/stories', emoji: '📝', color: 'from-amber-500/15 to-amber-600/5' },
  { icon: Search, label: t('explore'), path: '/explore', emoji: '🔍', color: 'from-cyan-500/15 to-cyan-600/5' },
  { icon: SettingsIcon, label: t('more'), path: '/more', emoji: '⚙️', color: 'from-slate-500/15 to-slate-600/5' },
  { icon: Zap, label: t('donations'), path: '/donations', emoji: '💝', color: 'from-rose-500/15 to-rose-600/5' },
];

export default function Index() {
  const { t, isRTL, locale } = useLocale();
  const { user } = useAuth();
  const {
    prayers, nextPrayer, remaining, hijriDate, hijriDay, hijriMonthNumber, hijriYear,
    loading, source, sourceLabel, mosqueName, city, latitude, longitude,
    locationLoading, locationError, detectLocation, unlinkMosque, calculationMethod,
  } = useUnifiedPrayer();
  
  const usingMosque = source === 'mosque';

  const [showHijri, setShowHijri] = useState(() => {
    const saved = localStorage.getItem('date-display-mode');
    return saved ? saved === 'hijri' : true; // Default Hijri
  });

  const toggleDateMode = () => {
    const newMode = !showHijri;
    setShowHijri(newMode);
    localStorage.setItem('date-display-mode', newMode ? 'hijri' : 'gregorian');
  };

  // Get today's Gregorian date in user's locale
  const localeMap: Record<string, string> = {
    ar: 'ar-SA-u-ca-gregory', en: 'en-US', de: 'de-DE', ru: 'ru-RU', fr: 'fr-FR', tr: 'tr-TR'
  };
  const gregorianDate = new Date().toLocaleDateString(localeMap[locale] || 'en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });

  const [notificationsEnabled, setNotificationsEnabled] = useState(() => {
    return localStorage.getItem('athan-notifications') === 'true';
  });

  const currentOccasion = getCurrentOccasion(hijriMonthNumber, parseInt(hijriDay) || 1);
  const [alertPrayer, setAlertPrayer] = useState<{ key: string; time: string } | null>(null);
  const [searchParams, setSearchParams] = useSearchParams();

  const handleAthanAlert = useCallback((prayerKey: string, prayerTime: string) => {
    setAlertPrayer({ key: prayerKey, time: prayerTime });
  }, []);

  useEffect(() => {
    const prayer = searchParams.get('athan_prayer');
    const time = searchParams.get('athan_time');
    if (prayer && time) {
      setAlertPrayer({ key: prayer, time });
      searchParams.delete('athan_prayer');
      searchParams.delete('athan_time');
      setSearchParams(searchParams, { replace: true });
    }
  }, []);

  useEffect(() => {
    if (!('serviceWorker' in navigator)) return;
    const handler = (event: MessageEvent) => {
      if (event.data?.type === 'ATHAN_ALERT') {
        setAlertPrayer({ key: event.data.prayer, time: event.data.time });
      }
    };
    navigator.serviceWorker.addEventListener('message', handler);
    return () => navigator.serviceWorker.removeEventListener('message', handler);
  }, []);

  const [prayersDone, setPrayersDone] = useState(0);
  const [tasbeehDone, setTasbeehDone] = useState(0);

  useEffect(() => {
    const todayKey = new Date().toISOString().split('T')[0];
    const prayerData = localStorage.getItem('prayer-tracker');
    if (prayerData) {
      const parsed = JSON.parse(prayerData);
      setPrayersDone(parsed[todayKey]?.length || 0);
    }
    const tasbeehTotal = parseInt(localStorage.getItem('tasbeeh-total') || '0');
    setTasbeehDone(Math.min(tasbeehTotal > 0 ? 1 : 0, 4));
  }, []);

  const [progress, setProgress] = useState(0);
  useEffect(() => {
    if (!remaining || !nextPrayer) return;
    const hMatch = remaining.match(/(\d+)h/);
    const mMatch = remaining.match(/(\d+)m/);
    const hours = hMatch ? parseInt(hMatch[1]) : 0;
    const mins = mMatch ? parseInt(mMatch[1]) : 0;
    const totalSecs = hours * 3600 + mins * 60;
    const maxSecs = 6 * 3600;
    setProgress(Math.max(0, Math.min(1, 1 - totalSecs / maxSecs)));
  }, [remaining, nextPrayer]);

  useAthanNotifications(prayers, notificationsEnabled, handleAthanAlert);

  useEffect(() => {
    if (notificationsEnabled && latitude && longitude && !locationLoading) {
      subscribeToPush(latitude, longitude, calculationMethod).catch(console.error);
    }
  }, [notificationsEnabled, latitude, longitude, locationLoading]);

  useEffect(() => {
    if (!notificationsEnabled) return;
    if (usingMosque && prayers.length > 0) {
      updatePushMosqueTimes(prayers.map(p => ({ key: p.key, time24: p.time24 }))).catch(console.error);
    } else {
      updatePushMosqueTimes(null).catch(console.error);
    }
  }, [prayers, usingMosque, notificationsEnabled]);

  const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';
  const [announcements, setAnnouncements] = useState<any[]>([]);
  const [dismissedAnn, setDismissedAnn] = useState<string[]>(() => {
    try { return JSON.parse(localStorage.getItem('dismissed_announcements') || '[]'); } catch { return []; }
  });

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/announcements`).then(r => r.json()).then(d => setAnnouncements(d.announcements || [])).catch(() => {});
  }, []);

  const dismissAnn = (id: string) => {
    const updated = [...dismissedAnn, id];
    setDismissedAnn(updated);
    localStorage.setItem('dismissed_announcements', JSON.stringify(updated));
  };

  const visibleAnn = announcements.filter(a => !dismissedAnn.includes(a.id));

  const toggleNotifications = async () => {
    if (!notificationsEnabled) {
      const granted = await requestNotificationPermission();
      if (granted) {
        setNotificationsEnabled(true);
        localStorage.setItem('athan-notifications', 'true');
        toast.success(t('notificationsEnabled'));
      } else {
        toast.error(t('notificationsDenied'));
      }
    } else {
      setNotificationsEnabled(false);
      localStorage.setItem('athan-notifications', 'false');
      unsubscribeFromPush().catch(console.error);
      toast.success(t('notificationsDisabled'));
    }
  };

  const circleR = 44;
  const circleC = 2 * Math.PI * circleR;
  const strokeDashoffset = isNaN(circleC * (1 - progress)) ? 0 : circleC * (1 - progress);

  const fajrTime = prayers.find(p => p.key === 'fajr')?.time || '--:--';
  const maghribTime = prayers.find(p => p.key === 'maghrib')?.time || '--:--';

  const ramadanActive = isRamadan(hijriMonthNumber);
  const totalGoals = 5 + (ramadanActive ? 2 : 0);
  const completedGoals = prayersDone + tasbeehDone;

  const [duaDrawerOpen, setDuaDrawerOpen] = useState(false);
  const todayDua = dailyDuas[Math.floor((Date.now() - new Date(new Date().getFullYear(), 0, 0).getTime()) / 86400000) % dailyDuas.length];

  const prayerNames: Record<string, string> = {
    fajr: t('fajr'), sunrise: t('sunrise'), dhuhr: t('dhuhr'), asr: t('asr'), maghrib: t('maghrib'), isha: t('isha')
  };

  const prayerIcons: Record<string, string> = {
    fajr: '🌅', sunrise: '☀️', dhuhr: '🕐', asr: '🌤️', maghrib: '🌇', isha: '🌙'
  };

  return (
    <div className="min-h-screen pb-24" dir={isRTL ? 'rtl' : 'ltr'}>
      <DuaOfDayDrawer open={duaDrawerOpen} onOpenChange={setDuaDrawerOpen} />
      {alertPrayer && (
        <OccasionAthanAlert
          prayerKey={alertPrayer.key}
          prayerTime={alertPrayer.time}
          occasion={currentOccasion}
          onDismiss={() => setAlertPrayer(null)}
        />
      )}

      {/* ===== HERO — Mystic Minimalism ===== */}
      <div className="relative overflow-hidden h-[280px]">
        <img
          src={meccaImage}
          alt={t('holyMosqueAlt')}
          className="w-full h-full object-cover animate-heroZoom"
          loading="eager"
          // @ts-ignore
          fetchpriority="high"
          width="1335"
          height="280"
          decoding="async"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/30 to-[hsl(var(--background))]" />
        
        {/* Top bar - notifications & profile */}
        <div className="absolute top-0 left-0 right-0 flex items-center justify-between px-5 pt-[calc(0.75rem+env(safe-area-inset-top,0px))]">
          <button
            onClick={toggleNotifications}
            aria-label={notificationsEnabled ? t('disableNotifications') : t('enableNotificationsLabel')}
            className="p-2.5 rounded-2xl bg-white/10 backdrop-blur-xl border border-white/10 transition-all active:scale-95 hover:bg-white/15"
          >
            {notificationsEnabled ? (
              <Bell className="h-5 w-5 text-white fill-current" />
            ) : (
              <BellOff className="h-5 w-5 text-white/60" />
            )}
          </button>
          <div className="flex-1" />
          <Link
            to="/account"
            className="p-2.5 rounded-2xl bg-white/10 backdrop-blur-xl border border-white/10 transition-all active:scale-95 hover:bg-white/15"
          >
            <User className="h-5 w-5 text-white/90" />
          </Link>
        </div>

        {/* Center content - Floating Date + Location with Mist Effect */}
        <div className="absolute bottom-12 left-0 right-0 px-5">
          {/* Date with toggle — larger & elegant */}
          <div className="flex items-center justify-center gap-2 mb-3">
            <button
              onClick={toggleDateMode}
              className="group flex items-center gap-2.5 bg-white/10 backdrop-blur-xl border border-white/10 rounded-full px-5 py-2 transition-all active:scale-95 hover:bg-white/15"
            >
              <span className="text-white text-sm font-bold tracking-wide drop-shadow-lg">
                {showHijri && hijriDate ? hijriDate : gregorianDate}
              </span>
              <span className="text-[10px] text-amber-200/90 font-bold bg-amber-500/20 px-2 py-0.5 rounded-full">
                {showHijri && hijriDate ? t('hijriDate') : t('gregorianDate')}
              </span>
            </button>
          </div>

          {/* Location — floating glass pill */}
          <div className="flex items-center justify-center">
            <button
              onClick={() => detectLocation()}
              className="flex items-center gap-2.5 bg-white/10 backdrop-blur-xl border border-white/10 rounded-full px-5 py-2.5 transition-all active:scale-95 hover:bg-white/15"
            >
              <MapPin className="h-4 w-4 text-emerald-300" />
              <span className="text-white font-bold text-sm drop-shadow-lg">
                {locationLoading ? '...' : city || t('detectLocation')}
              </span>
            </button>
          </div>
        </div>
      </div>

      {/* ===== NEXT PRAYER CARD — Glassmorphism 2.0 ===== */}
      <div className="px-4 -mt-10 relative z-10 mb-5">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-mystic rounded-3xl p-5 shadow-float animate-fade-in"
        >
          <div className="flex items-center gap-5">
            {/* Countdown ring — large, smooth, with pulse */}
            <div className="relative shrink-0 animate-pulse-glow rounded-full">
              <svg width="110" height="110" viewBox="0 0 110 110">
                {/* Background track */}
                <circle cx="55" cy="55" r={circleR} fill="none" stroke="hsl(var(--border))" strokeWidth="4" opacity="0.2" />
                {/* Progress ring */}
                <circle
                  cx="55" cy="55" r={circleR}
                  fill="none"
                  stroke="url(#prayer-gradient)"
                  strokeWidth="4"
                  strokeLinecap="round"
                  strokeDasharray={circleC}
                  strokeDashoffset={strokeDashoffset}
                  transform="rotate(-90 55 55)"
                  className="transition-all duration-1000"
                />
                {/* Gradient definition */}
                <defs>
                  <linearGradient id="prayer-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="hsl(var(--islamic-green))" />
                    <stop offset="100%" stopColor="hsl(var(--islamic-gold))" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-[10px] text-muted-foreground font-medium tracking-wider uppercase">{t('remaining')}</span>
                <span className="text-lg font-extrabold tabular-nums text-foreground leading-none mt-0.5">
                  {remaining || '00:00'}
                </span>
              </div>
            </div>

            {/* Next prayer info */}
            <div className="flex-1 min-w-0">
              <p className="text-[11px] text-muted-foreground mb-1 font-medium tracking-wide uppercase">{t('nextPrayerLabel')}</p>
              <p className="text-2xl font-extrabold text-foreground leading-tight tracking-tight">
                {nextPrayer ? prayerNames[nextPrayer.key] || t(nextPrayer.key) : '—'}
              </p>
              <p className="text-xl font-light tabular-nums text-primary mt-0.5">
                {nextPrayer?.time || '—'}
              </p>
              <div className="flex items-center gap-2 mt-3">
                <Link
                  to="/tracker"
                  className="text-[11px] text-primary font-bold bg-primary/8 px-3.5 py-1.5 rounded-xl transition-all active:scale-95 hover:bg-primary/12 truncate max-w-[45%] border border-primary/10"
                >
                  {t('prayerTracking')}
                </Link>
                <Link
                  to="/notifications"
                  className="text-[11px] text-muted-foreground bg-muted/40 px-3.5 py-1.5 rounded-xl transition-all active:scale-95 hover:bg-muted/60 truncate max-w-[45%]"
                >
                  <Volume2 className="h-3 w-3 inline me-1" />
                  {t('athanLabel')}
                </Link>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* ===== OCCASION BANNER ===== */}
      {currentOccasion && <OccasionBanner occasion={currentOccasion} />}

      {/* ===== ADMIN ANNOUNCEMENTS ===== */}
      <AnimatePresence>
        {visibleAnn.map(ann => (
          <motion.div key={ann.id} initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, height: 0 }}
            className="px-4 mb-3">
            <div className={cn('rounded-2xl p-4 relative border',
              ann.type === 'warning' ? 'bg-amber-500/10 border-amber-500/30' :
              ann.type === 'promo' ? 'bg-primary/10 border-primary/30' :
              'bg-blue-500/10 border-blue-500/30'
            )} data-testid={`announcement-${ann.id}`}>
              <button onClick={() => dismissAnn(ann.id)} className="absolute top-2.5 left-2.5 p-1.5 rounded-full bg-black/10 hover:bg-black/20 transition-colors"><X className="h-3.5 w-3.5 text-foreground/60" /></button>
              <div className="flex items-start gap-3">
                <Megaphone className={cn('h-5 w-5 shrink-0 mt-0.5',
                  ann.type === 'warning' ? 'text-amber-500' : ann.type === 'promo' ? 'text-primary' : 'text-blue-500'
                )} />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-foreground">{ann.title}</p>
                  <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{ann.body}</p>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>

      {/* ===== LOCATION ERROR ===== */}
      {locationError && prayers.length === 0 && (
        <div className="px-4 mb-4">
          <div className="rounded-3xl bg-destructive/10 border border-destructive/30 p-6 flex flex-col items-center gap-3">
            <MapPinOff className="h-8 w-8 text-destructive" />
            <p className="text-sm font-bold text-foreground text-center">{locationError === '__LOCATION_ERROR__' ? t('locationErrorMsg') : locationError}</p>
            <button
              onClick={() => detectLocation()}
              className="rounded-2xl bg-primary text-primary-foreground px-6 py-2.5 text-sm font-bold transition-all active:scale-95"
            >
              {t('enableLocation')}
            </button>
          </div>
        </div>
      )}

      <AdBanner position="home" />

      {/* ===== PRAYER TIMES GRID ===== */}
      <div className="px-4 mb-5">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-lg">🕌</span>
            <h3 className="text-sm font-bold text-foreground">{t('prayerTimes')}</h3>
          </div>
          <Link to="/prayer-times" className="text-xs text-primary font-bold flex items-center gap-0.5 hover:underline">
            {t('moreLabel')}
            <ChevronLeft className="h-3.5 w-3.5" />
          </Link>
        </div>
        
        {usingMosque && mosqueName && (
          <div className="flex items-center justify-between mb-2.5 px-1">
            <p className="text-[11px] text-primary flex items-center gap-1.5 font-medium">
              <Building2 className="h-3.5 w-3.5" />
              {mosqueName}
              <span className="bg-primary/15 text-primary text-[8px] px-1.5 py-0.5 rounded-full font-bold">{t('mosqueLabel')}</span>
            </p>
            <button
              onClick={() => {
                unlinkMosque();
                toast.success(t('mosqueUnlinked'));
              }}
              className="flex items-center gap-0.5 text-[10px] text-destructive font-medium"
            >
              <Unlink className="h-2.5 w-2.5" />
              {t('unlinkMosque')}
            </button>
          </div>
        )}
        
        <div className="grid grid-cols-3 gap-2.5">
          {prayers.map((prayer) => {
            const isNext = nextPrayer?.key === prayer.key;
            return (
              <motion.div
                key={prayer.key}
                whileTap={{ scale: 0.97 }}
                className={cn(
                  'rounded-2xl border p-3.5 text-center transition-all duration-300',
                  isNext
                    ? 'glass-mystic border-primary/20 shadow-float animate-pulse-glow'
                    : 'neu-card hover:shadow-elevated'
                )}
              >
                <span className="text-lg mb-1 block">{prayerIcons[prayer.key] || '🕐'}</span>
                <p className={cn('text-[11px] mb-0.5 font-bold', isNext ? 'text-primary' : 'text-muted-foreground')}>
                  {prayerNames[prayer.key] || t(prayer.key)}
                </p>
                <p className={cn('text-sm font-bold tabular-nums', isNext ? 'text-primary' : 'text-foreground')}>
                  {prayer.time}
                </p>
              </motion.div>
            );
          })}
        </div>

        {/* Mosque link — glass card */}
        <Link
          to="/mosque-times"
          className="mt-3 flex items-center justify-between glass-mystic rounded-2xl p-3.5 transition-all active:scale-[0.98] hover:shadow-float"
        >
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center">
              <Building2 className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-sm font-bold text-foreground">{t('mosqueTimes')}</p>
              <p className="text-[10px] text-muted-foreground">{t('chooseNearbyMosque')}</p>
            </div>
          </div>
          <ChevronLeft className="h-4 w-4 text-muted-foreground" />
        </Link>
      </div>

      {/* ===== RAMADAN BAR ===== */}
      {ramadanActive && (
        <div className="px-4 mb-5">
          <Link to="/ramadan-challenge">
            <div className="rounded-3xl gradient-prayer-bar p-5 flex items-center justify-between relative overflow-hidden active:scale-[0.98] transition-transform">
              <div className="absolute inset-0 islamic-pattern opacity-15" />
              <div className="text-white text-sm relative z-10">
                <span className="text-white/60 text-xs font-medium">{t('iftar')}</span>
                <p className="font-bold tabular-nums text-lg">{maghribTime}</p>
              </div>
              <div className="text-center relative z-10">
                <span className="text-3xl">🌙</span>
                <p className="text-white/70 text-[10px] mt-1 font-medium">{t('ramadanChallenge')}</p>
              </div>
              <div className="text-white text-sm text-start relative z-10">
                <span className="text-white/60 text-xs font-medium">{t('fajrLabel')}</span>
                <p className="font-bold tabular-nums text-lg">{fajrTime}</p>
              </div>
            </div>
          </Link>
          <Link to="/ramadan-calendar" className="mt-2.5 block">
            <div className="rounded-2xl bg-card border border-accent/20 p-3.5 flex items-center justify-between active:scale-[0.98] transition-transform hover:border-accent/40">
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-xl bg-accent/10 flex items-center justify-center text-lg">📅</div>
                <div>
                  <p className="text-sm font-bold text-foreground">{t('ramadanCalendarTitle')}</p>
                  <p className="text-[10px] text-muted-foreground">{t('ramadanCalendarDesc')}</p>
                </div>
              </div>
              <ChevronLeft className="h-4 w-4 text-muted-foreground" />
            </div>
          </Link>
        </div>
      )}

      {/* ===== DAILY HADITH ===== */}
      <Suspense fallback={<div className="h-40" />}>
        <DailyHadith />
      </Suspense>

      {/* ===== NATIVE SPONSORED CARD (blends with Hadith design) ===== */}
      <Suspense fallback={null}>
        <NativeAdCard placement="hadith_feed" />
      </Suspense>

      {/* ===== FEATURED VIDEO CONTENT ===== */}
      <Suspense fallback={<div className="h-48" />}>
        <FeaturedVideos />
      </Suspense>

      {/* ===== DAILY GOALS ===== */}
      <DailyGoals hijriMonthNumber={hijriMonthNumber} />

      {/* ===== AI DAILY WIDGETS ===== */}
      <VerseOfDay />

      {/* ===== NOTIFICATION CARD ===== */}
      <NotificationCard />

      {/* ===== ISLAMIC SPONSORED CONTENT ===== */}
      <div className="px-4 mb-4">
        <IslamicAd placement="main" variant="card" />
      </div>

      {/* ===== QURAN PLAYER ===== */}
      <Suspense fallback={<div className="h-32" />}>
        <QuranPlayer />
        
        {/* ===== RUQYAH SECTION ===== */}
        <div className="px-4 mb-6">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-lg">🛡️</span>
              <h3 className="text-sm font-bold text-foreground">{t('ruqyahTitle').replace('🛡️ ', '')}</h3>
            </div>
            <Link to="/ruqyah" className="text-xs text-primary font-bold flex items-center gap-0.5 hover:underline">
              {t('moreLabel')}
              <ChevronLeft className="h-3.5 w-3.5" />
            </Link>
          </div>
          
          <div className="grid grid-cols-2 gap-2.5">
            {[
              { title: t('ruqyahAyatKursi'), subtitle: t('ruqyahAyatKursiDesc'), icon: '🔰' },
              { title: t('ruqyahMuawwidhat'), subtitle: t('ruqyahMuawwidhatDesc'), icon: '✨' },
              { title: t('ruqyahBaqara'), subtitle: t('ruqyahBaqaraDesc'), icon: '📖' },
              { title: t('ruqyahMorning'), subtitle: t('ruqyahMorningDesc'), icon: '🌅' },
            ].map((item, idx) => (
              <Link
                key={idx}
                to="/ruqyah"
                className="bg-card border border-border/40 rounded-2xl p-3.5 active:scale-[0.97] transition-all hover:border-primary/30 hover:shadow-sm"
              >
                <div className="flex items-start gap-2.5">
                  <span className="text-2xl">{item.icon}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-foreground mb-0.5">{item.title}</p>
                    <p className="text-[11px] text-muted-foreground leading-relaxed">{item.subtitle}</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </Suspense>

      {/* ===== DUA OF DAY ===== */}
      <div className="px-4 mb-5">
        <div
          onClick={() => setDuaDrawerOpen(true)}
          className="rounded-3xl bg-card border border-border/40 p-6 shadow-card relative overflow-hidden cursor-pointer active:scale-[0.98] transition-transform"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-primary/5 to-transparent rounded-bl-full" />
          <span className="inline-block rounded-full bg-primary/10 border border-primary/20 px-3 py-1 text-[11px] font-bold text-primary mb-3">
            {t('duaOfDay')}
          </span>
          <p className="text-sm font-bold text-foreground mb-3">{t(todayDua.subtitleKey)}</p>
          <p className="text-lg font-arabic text-foreground leading-[2.2] text-center mb-2 line-clamp-2" dir="rtl">
            {todayDua.arabic}
          </p>
          {locale !== 'ar' && todayDua.translationKey && (
            <p className="text-sm text-muted-foreground leading-relaxed text-center mb-3 line-clamp-2" dir="auto">
              {t(todayDua.translationKey)}
            </p>
          )}
          <span className="inline-block rounded-2xl border border-primary/30 bg-primary/5 px-5 py-2.5 text-xs font-bold text-primary transition-all hover:bg-primary/10">
            {t('readWithTranslation')}
          </span>
        </div>
      </div>

      {/* ===== SUGGESTED GOALS ===== */}
      <Suspense fallback={<div className="h-24" />}>
        <SuggestedGoals />
      </Suspense>

      {/* ===== QUICK ACCESS ===== */}
      <div className="px-4 mb-5">
        <div className="flex items-center gap-2 mb-3">
          <Zap className="h-4 w-4 text-accent" />
          <h3 className="text-sm font-bold text-foreground">{t('quickAccessLabel')}</h3>
        </div>
        <div className="grid grid-cols-4 gap-2.5">
          {getQuickAccessItems(t).map((item) => (
            <Link 
              key={item.path} 
              to={item.path} 
              className="flex flex-col items-center gap-2 p-3 rounded-2xl bg-card border border-border/40 transition-all active:scale-95 hover:border-primary/30 hover:shadow-sm group"
            >
              <div className={cn(
                "h-12 w-12 rounded-2xl flex items-center justify-center text-2xl bg-gradient-to-br transition-all",
                item.color
              )}>
                {item.emoji}
              </div>
              <span className="text-[11px] font-bold text-foreground text-center leading-tight">
                {item.label}
              </span>
            </Link>
          ))}
        </div>
      </div>

      {/* ===== QURAN GOAL ===== */}
      <div className="px-4 mb-5">
        <div className="rounded-3xl bg-card border border-border/40 p-6 shadow-card relative overflow-hidden">
          <div className="absolute bottom-0 left-0 w-32 h-32 bg-gradient-to-tr from-accent/5 to-transparent rounded-tr-full" />
          <span className="inline-block rounded-full bg-accent/10 border border-accent/20 px-3 py-1 text-[11px] font-bold text-accent mb-2">
            {t('quranCompletion')}
          </span>
          <p className="text-sm font-bold text-foreground mb-1">{t('startDailyRecitation')}</p>
          <p className="text-xs text-muted-foreground mb-3 leading-relaxed">{t('setYourPace')}</p>
          <Link
            to="/quran-goal"
            className="inline-block rounded-2xl bg-primary/10 border border-primary/20 px-5 py-2.5 text-xs font-bold text-primary transition-all active:scale-95 hover:bg-primary/15"
          >
            {t('setQuranGoal')}
          </Link>
        </div>
      </div>

      {/* ===== HIJRI CALENDAR ===== */}
      <div className="px-4 mb-8">
        <div className="flex items-center gap-2 mb-3">
          <span className="text-lg">📅</span>
          <h3 className="text-sm font-bold text-foreground">{t('hijriCalendarTitle')}</h3>
        </div>
        <Suspense fallback={<div className="h-48" />}>
          <HijriCalendar
            hijriDay={hijriDay}
            hijriMonth={hijriMonthNumber || undefined}
            hijriYear={hijriYear}
          />
        </Suspense>
      </div>
    </div>
  );
}
