import { useLocale } from '@/hooks/useLocale';
import { useState, useEffect, useMemo, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Bell, Volume2, Clock, BookOpen, Moon, MessageSquare, Sparkles, TestTube, ChevronDown, Smartphone, Zap } from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import { Button } from '@/components/ui/button';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { requestNotificationPermission } from '@/hooks/useAthanNotifications';
import { sendTestNotification, sendTestAthanAlert } from '@/lib/prayerNotifications';
import { testAthanPlayback } from '@/lib/athanAudio';
import { subscribeToPush, isSubscribedToPush } from '@/lib/pushSubscription';
import { toast } from 'sonner';
import AthanSelector from '@/components/AthanSelector';

const PRAYER_KEYS = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha'] as const;

const PRAYER_EMOJIS: Record<string, string> = {
  fajr: '🌅', dhuhr: '☀️', asr: '🌤️', maghrib: '🌇', isha: '🌙'
};

function PrayerToggleRow({ prayerKey, label, enabled, onToggle }: {
  prayerKey: string; label: string; enabled: boolean; onToggle: () => void;
}) {
  return (
    <div className="flex items-center gap-3 py-3 border-b border-border/15 last:border-b-0">
      <span className="text-xl">{PRAYER_EMOJIS[prayerKey] || '🕌'}</span>
      <span className="flex-1 text-sm font-bold text-foreground">{label}</span>
      <Switch
        checked={enabled}
        onCheckedChange={onToggle}
        className="shrink-0 data-[state=checked]:bg-primary"
      />
    </div>
  );
}

interface NotifSetting {
  key: string;
  label: string;
  description: string;
  icon: React.ReactNode;
  schedule?: string;
  defaultEnabled?: boolean;
}

function getPrayerSettings(t: (k: string) => string): NotifSetting[] {
  return [
    { key: 'prayer-reminder', label: t('notifPrayerReminder'), description: t('notifPrayerReminderDesc'), icon: <Clock className="h-5 w-5" />, schedule: t('notifBefore10Min'), defaultEnabled: true },
    { key: 'prayer-tracker-reminder', label: t('notifPrayerTracker'), description: t('notifPrayerTrackerDesc'), icon: <Bell className="h-5 w-5" />, defaultEnabled: true },
  ];
}

function getDailyGoalSettings(t: (k: string) => string): NotifSetting[] {
  return [
    { key: 'quran-listen-reminder', label: t('notifQuranListen'), description: t('notifQuranListenDesc'), icon: <BookOpen className="h-5 w-5" />, schedule: t('notifAtEvening'), defaultEnabled: true },
    { key: 'dhikr-daily-reminder', label: t('notifDhikrDaily'), description: t('notifDhikrDailyDesc'), icon: <Sparkles className="h-5 w-5" />, defaultEnabled: true },
  ];
}

function getOtherSettings(t: (k: string) => string): NotifSetting[] {
  return [
    { key: 'daily-stories-reminder', label: t('notifStories'), description: t('notifStoriesDesc'), icon: <MessageSquare className="h-5 w-5" />, schedule: t('notifAtNight'), defaultEnabled: true },
    { key: 'friday-reminder', label: t('notifFriday'), description: t('notifFridayDesc'), icon: <BookOpen className="h-5 w-5" />, defaultEnabled: true },
    { key: 'suhoor-reminder', label: t('notifSuhoor'), description: t('notifSuhoorDesc'), icon: <Moon className="h-5 w-5" />, schedule: t('notifSuhoorSchedule'), defaultEnabled: true },
  ];
}

function SettingRow({ setting }: { setting: NotifSetting }) {
  const { t } = useLocale();
  const [enabled, setEnabled] = useState(() => {
    const saved = localStorage.getItem(`notif-${setting.key}`);
    return saved !== null ? saved === 'true' : (setting.defaultEnabled ?? false);
  });

  const toggle = async () => {
    if (!enabled) {
      const granted = await requestNotificationPermission();
      if (!granted) {
        toast.error(t('allowNotifBrowser'));
        return;
      }
    }
    const newVal = !enabled;
    setEnabled(newVal);
    localStorage.setItem(`notif-${setting.key}`, String(newVal));
  };

  return (
    <div className="flex items-start gap-3 py-4 border-b border-border/20 last:border-b-0">
      <div className="mt-0.5 h-9 w-9 rounded-xl bg-primary/10 flex items-center justify-center shrink-0 text-primary">
        {setting.icon}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-bold text-foreground">{setting.label}</p>
        <p className="text-xs text-muted-foreground mt-0.5">{setting.description}</p>
        {setting.schedule && enabled && (
          <div className="mt-1.5 inline-flex items-center gap-1.5 rounded-full bg-muted px-2.5 py-0.5">
            <Clock className="h-3 w-3 text-muted-foreground" />
            <span className="text-[10px] text-muted-foreground">{setting.schedule}</span>
          </div>
        )}
      </div>
      <Switch
        checked={enabled}
        onCheckedChange={toggle}
        className="shrink-0 mt-1 data-[state=checked]:bg-primary"
      />
    </div>
  );
}

function SettingsSection({ title, settings }: { title: string; settings: NotifSetting[] }) {
  return (
    <div className="px-4 mt-5">
      <p className="text-xs font-bold text-muted-foreground mb-2 me-1">{title}</p>
      <div className="rounded-2xl neu-card px-4">
        {settings.map(s => <SettingRow key={s.key} setting={s} />)}
      </div>
    </div>
  );
}

export default function NotificationSettings() {
  const { t, dir, locale } = useLocale();
  const isAr = locale === 'ar';
  const [showAthanSelector, setShowAthanSelector] = useState(false);
  const [pushSubscribed, setPushSubscribed] = useState(false);
  const [pushLoading, setPushLoading] = useState(false);
  const [permissionStatus, setPermissionStatus] = useState<string>('default');

  // Individual prayer notification toggles
  const [enabledPrayers, setEnabledPrayers] = useState<string[]>(() => {
    const saved = localStorage.getItem('notif-enabled-prayers');
    if (saved) {
      try { return JSON.parse(saved); } catch {}
    }
    return [...PRAYER_KEYS]; // Default: all enabled
  });

  // Master notifications toggle
  const [masterEnabled, setMasterEnabled] = useState(() => {
    return localStorage.getItem('athan-notifications') !== 'false';
  });

  const prayerSettings = useMemo(() => getPrayerSettings(t), [t]);
  const dailyGoalSettings = useMemo(() => getDailyGoalSettings(t), [t]);
  const otherSettings = useMemo(() => getOtherSettings(t), [t]);

  // Check permission status
  useEffect(() => {
    if ('Notification' in window) {
      setPermissionStatus(Notification.permission);
    }
    isSubscribedToPush().then(setPushSubscribed);
  }, []);

  const prayerLabels: Record<string, string> = {
    fajr: isAr ? 'الفجر' : 'Fajr',
    dhuhr: isAr ? 'الظهر' : 'Dhuhr',
    asr: isAr ? 'العصر' : 'Asr',
    maghrib: isAr ? 'المغرب' : 'Maghrib',
    isha: isAr ? 'العشاء' : 'Isha',
  };

  const togglePrayer = useCallback((key: string) => {
    setEnabledPrayers(prev => {
      const updated = prev.includes(key) ? prev.filter(p => p !== key) : [...prev, key];
      localStorage.setItem('notif-enabled-prayers', JSON.stringify(updated));
      return updated;
    });
  }, []);

  const toggleMaster = useCallback(async () => {
    if (!masterEnabled) {
      // Enable - request permission first
      const granted = await requestNotificationPermission();
      if (!granted) {
        toast.error(t('allowNotifBrowser'));
        return;
      }
      setMasterEnabled(true);
      localStorage.setItem('athan-notifications', 'true');
      setPermissionStatus('granted');
      toast.success(t('notificationsEnabled'));
    } else {
      setMasterEnabled(false);
      localStorage.setItem('athan-notifications', 'false');
      toast.success(t('notificationsDisabled'));
    }
  }, [masterEnabled, t]);

  const handleEnablePush = async () => {
    setPushLoading(true);
    try {
      const granted = await requestNotificationPermission();
      if (!granted) {
        toast.error(t('allowNotifBrowser'));
        return;
      }
      const cached = localStorage.getItem('cached-location');
      if (cached) {
        const loc = JSON.parse(cached);
        const success = await subscribeToPush(loc.latitude, loc.longitude, loc.calculationMethod || 3);
        setPushSubscribed(success);
        if (success) {
          toast.success(t('bgNotifEnabled'));
        } else {
          toast.error(t('bgNotifFailed'));
        }
      } else {
        toast.error(t('enableLocationFirst'));
      }
    } catch {
      toast.error(t('errorOccurred'));
    } finally {
      setPushLoading(false);
    }
  };

  const handleTestNotification = async () => {
    const granted = await requestNotificationPermission();
    if (!granted) {
      toast.error(t('allowNotifFirst'));
      return;
    }
    setPermissionStatus('granted');
    const sent = await sendTestNotification();
    if (sent) {
      toast.success(t('testNotifSent'));
    } else {
      toast.error(t('testNotifFailed'));
    }
  };

  const handleTestFullscreen = () => {
    const sent = sendTestAthanAlert();
    if (sent) {
      toast.success(isAr ? 'تم إرسال تنبيه تجريبي فوق الشاشة' : 'Test fullscreen alert sent');
    } else {
      toast.error(isAr ? 'افتح الصفحة الرئيسية أولاً' : 'Go to home page first');
    }
  };

  const handleTestAthan = () => {
    const played = testAthanPlayback();
    if (played) {
      toast.success(t('playingAthan'));
    } else {
      toast.error(t('playAthanFailed'));
    }
  };

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir}>
      {/* Header */}
      <div className="sticky top-0 z-20 bg-background/80 backdrop-blur-xl border-b border-border/30">
        <div className="flex items-center justify-between px-4 pt-[calc(0.75rem+env(safe-area-inset-top,0px))] pb-3">
          <Link to="/more" className="p-2 -me-2 rounded-xl transition-all active:scale-90">
            <ArrowRight className="h-5 w-5 text-foreground" />
          </Link>
          <h1 className="text-base font-bold text-foreground">{t('notifAndAthan')}</h1>
          <div className="w-9" />
        </div>
      </div>

      {/* Permission Status Banner */}
      {permissionStatus !== 'granted' && (
        <div className="px-4 mt-4">
          <div className={cn(
            "rounded-2xl border p-4",
            permissionStatus === 'denied'
              ? "bg-red-500/10 border-red-500/20"
              : "bg-amber-500/10 border-amber-500/20"
          )}>
            <div className="flex items-start gap-3">
              <Bell className={cn("h-5 w-5 mt-0.5 shrink-0", permissionStatus === 'denied' ? "text-red-500" : "text-amber-500")} />
              <div className="flex-1">
                <p className="text-sm font-bold text-foreground">
                  {permissionStatus === 'denied'
                    ? (isAr ? '❌ الإشعارات محظورة في المتصفح' : '❌ Notifications blocked in browser')
                    : (isAr ? '⚠️ الإشعارات غير مفعّلة' : '⚠️ Notifications not enabled')
                  }
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {permissionStatus === 'denied'
                    ? (isAr ? 'افتح إعدادات المتصفح → الإشعارات → اسمح لهذا الموقع' : 'Go to browser settings → Notifications → Allow this site')
                    : (isAr ? 'اضغط الزر أدناه لتفعيل الإشعارات' : 'Click the button below to enable notifications')
                  }
                </p>
                {permissionStatus !== 'denied' && (
                  <Button
                    onClick={async () => {
                      const granted = await requestNotificationPermission();
                      if (granted) {
                        setPermissionStatus('granted');
                        setMasterEnabled(true);
                        localStorage.setItem('athan-notifications', 'true');
                        toast.success(t('notificationsEnabled'));
                      }
                    }}
                    size="sm"
                    className="mt-2 rounded-xl gap-1.5"
                  >
                    <Bell className="h-3.5 w-3.5" />
                    {isAr ? 'تفعيل الإشعارات' : 'Enable Notifications'}
                  </Button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Master toggle */}
      <div className="px-4 mt-4">
        <div className="rounded-2xl neu-card p-4">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-primary/15 flex items-center justify-center text-primary">
              <Bell className="h-5 w-5" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-bold text-foreground">
                {isAr ? 'إشعارات الأذان' : 'Athan Notifications'}
              </p>
              <p className="text-xs text-muted-foreground">
                {masterEnabled
                  ? (isAr ? 'مفعّل — ستتلقى تنبيهات عند وقت الصلاة' : 'ON — You will receive alerts at prayer time')
                  : (isAr ? 'معطّل' : 'OFF')
                }
              </p>
            </div>
            <Switch
              checked={masterEnabled}
              onCheckedChange={toggleMaster}
              className="shrink-0 data-[state=checked]:bg-primary"
            />
          </div>
        </div>
      </div>

      {/* Individual prayer toggles */}
      {masterEnabled && (
        <div className="px-4 mt-3">
          <p className="text-xs font-bold text-muted-foreground mb-2 me-1">
            {isAr ? 'اختر الصلوات' : 'Select Prayers'}
          </p>
          <div className="rounded-2xl neu-card px-4">
            {PRAYER_KEYS.map(key => (
              <PrayerToggleRow
                key={key}
                prayerKey={key}
                label={prayerLabels[key]}
                enabled={enabledPrayers.includes(key)}
                onToggle={() => togglePrayer(key)}
              />
            ))}
          </div>
        </div>
      )}

      {/* Push notification banner */}
      {!pushSubscribed && masterEnabled && (
        <div className="px-4 mt-4">
          <div className="rounded-2xl bg-primary/10 border border-primary/20 p-4">
            <div className="flex items-start gap-3">
              <Smartphone className="h-5 w-5 text-primary mt-0.5 shrink-0" />
              <div className="flex-1">
                <p className="text-sm font-bold text-foreground">{t('bgAthanNotif')}</p>
                <p className="text-xs text-muted-foreground mt-1">{t('bgAthanNotifDesc')}</p>
                <Button
                  onClick={handleEnablePush}
                  disabled={pushLoading}
                  size="sm"
                  className="mt-2 rounded-xl gap-1.5"
                >
                  {pushLoading ? <Bell className="h-3.5 w-3.5 animate-pulse" /> : <Bell className="h-3.5 w-3.5" />}
                  {t('enableNotif')}
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Test buttons */}
      <div className="px-4 mt-4 flex flex-col gap-2">
        <div className="flex gap-2">
          <Button
            onClick={handleTestNotification}
            variant="outline"
            className="flex-1 h-11 rounded-2xl gap-2 text-sm font-bold"
          >
            <TestTube className="h-4 w-4" />
            {t('testNotif')}
          </Button>
          <Button
            onClick={handleTestAthan}
            variant="outline"
            className="flex-1 h-11 rounded-2xl gap-2 text-sm font-bold"
          >
            <Volume2 className="h-4 w-4" />
            {t('testAthan')}
          </Button>
        </div>
        <Button
          onClick={handleTestFullscreen}
          variant="outline"
          className="w-full h-11 rounded-2xl gap-2 text-sm font-bold"
        >
          <Zap className="h-4 w-4" />
          {isAr ? 'اختبار تنبيه فوق الشاشة' : 'Test Fullscreen Alert'}
        </Button>
      </div>

      {/* Additional prayer settings */}
      <SettingsSection title={t("prayersSection")} settings={prayerSettings} />

      {/* Athan selector */}
      <div className="px-4 mt-3">
        <button
          onClick={() => setShowAthanSelector(!showAthanSelector)}
          className="w-full flex items-center justify-between rounded-2xl neu-card p-4 transition-all active:scale-[0.98]"
        >
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-accent/10 flex items-center justify-center">
              <Volume2 className="h-5 w-5 text-accent-foreground" />
            </div>
            <div className={isAr ? "text-right" : "text-left"}>
              <p className="text-sm font-bold text-foreground">{t('selectAthanSound')}</p>
              <p className="text-xs text-muted-foreground mt-0.5">
                {(() => {
                  const id = localStorage.getItem('athan-sound') || 'makkah';
                  const names: Record<string, string> = { makkah: t('athanMakkah'), madinah: t('athanMadinah'), turkish: t('athanTurkish'), umayyad: t('athanUmayyad'), quds: t('athanQuds'), abdulbasit: t('athanAbdulbasit'), shahat: t('athanShahat'), saqqaf: t('athanSaqqaf'), default: t('athanSimple') };
                  return names[id] || t('athanMakkah');
                })()}
              </p>
            </div>
          </div>
          <ChevronDown className={cn("h-4 w-4 text-muted-foreground transition-transform", showAthanSelector && "rotate-180")} />
        </button>
      </div>

      <AnimatePresence>
        {showAthanSelector && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="px-4 mt-2 overflow-hidden"
          >
            <div className="rounded-2xl neu-card p-4">
              <AthanSelector />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Daily goals */}
      <SettingsSection title={t("dailyGoalsSection")} settings={dailyGoalSettings} />

      {/* Other */}
      <SettingsSection title={t("otherAlerts")} settings={otherSettings} />

      {/* Info note */}
      <div className="px-4 mt-6 mb-8">
        <div className="rounded-2xl bg-muted/50 border border-border/30 p-4">
          <p className="text-xs text-muted-foreground leading-relaxed">
            {t('pwaNotifTip')}
          </p>
        </div>
      </div>
    </div>
  );
}
