/**
 * PermissionManager - Native-like permission request UI
 * Shows pre-request screens explaining benefits before system prompts
 * Designed for Google Play Protect compliance (Android 14+ / API 34)
 */
import { useState, useEffect, useCallback } from 'react';
import { MapPin, Bell, HardDrive, X, ChevronLeft, Shield } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useLocale } from '@/hooks/useLocale';

type PermissionType = 'location' | 'notifications' | 'storage';
type PermissionStatus = 'prompt' | 'granted' | 'denied' | 'unsupported';

interface PermissionState {
  location: PermissionStatus;
  notifications: PermissionStatus;
  storage: PermissionStatus;
}

const PERMISSION_DISMISSED_KEY = 'permissions_dismissed';
const PERMISSION_CHECK_KEY = 'permissions_checked';

interface PermissionConfig {
  type: PermissionType;
  icon: typeof MapPin;
  title: string;
  subtitle: string;
  benefits: string[];
  gradient: string;
  iconColor: string;
}

const permissionConfigsBase = [
  {
    type: 'location' as PermissionType,
    icon: MapPin,
    titleKey: 'permLocationTitle',
    subtitleKey: 'permLocationSubtitle',
    benefitKeys: ['permLocationBenefit1', 'permLocationBenefit2', 'permLocationBenefit3', 'permLocationBenefit4'],
    gradient: 'from-emerald-600 to-teal-700',
    iconColor: 'text-emerald-500 dark:text-emerald-400',
  },
  {
    type: 'notifications' as PermissionType,
    icon: Bell,
    titleKey: 'permNotifTitle',
    subtitleKey: 'permNotifSubtitle',
    benefitKeys: ['permNotifBenefit1', 'permNotifBenefit2', 'permNotifBenefit3', 'permNotifBenefit4'],
    gradient: 'from-amber-600 to-orange-700',
    iconColor: 'text-amber-500 dark:text-amber-400',
  },
];

async function checkPermissionStatus(type: PermissionType): Promise<PermissionStatus> {
  try {
    if (type === 'location') {
      if (!navigator.geolocation) return 'unsupported';
      const result = await navigator.permissions.query({ name: 'geolocation' });
      return result.state as PermissionStatus;
    }
    if (type === 'notifications') {
      if (!('Notification' in window)) return 'unsupported';
      const state = Notification.permission;
      if (state === 'default') return 'prompt';
      return state as PermissionStatus;
    }
    if (type === 'storage') {
      if (!navigator.storage?.persist) return 'unsupported';
      const persisted = await navigator.storage.persisted();
      return persisted ? 'granted' : 'prompt';
    }
  } catch {
    return 'prompt';
  }
  return 'prompt';
}

async function requestPermission(type: PermissionType): Promise<boolean> {
  try {
    if (type === 'location') {
      return new Promise((resolve) => {
        navigator.geolocation.getCurrentPosition(
          () => resolve(true),
          () => resolve(false),
          { enableHighAccuracy: true, timeout: 10000 }
        );
      });
    }
    if (type === 'notifications') {
      const result = await Notification.requestPermission();
      return result === 'granted';
    }
    if (type === 'storage') {
      if (navigator.storage?.persist) {
        return await navigator.storage.persist();
      }
      return false;
    }
  } catch {
    return false;
  }
  return false;
}

export function PermissionManager() {
  const { t, dir } = useLocale();
  const [permStates, setPermStates] = useState<PermissionState>({
    location: 'prompt',
    notifications: 'prompt',
    storage: 'prompt',
  });
  const [currentStep, setCurrentStep] = useState(0);
  const [visible, setVisible] = useState(false);
  const [requesting, setRequesting] = useState(false);

  // Build translated permission configs
  const permissionConfigs: PermissionConfig[] = permissionConfigsBase.map(cfg => ({
    type: cfg.type,
    icon: cfg.icon,
    title: t(cfg.titleKey),
    subtitle: t(cfg.subtitleKey),
    benefits: cfg.benefitKeys.map(k => t(k)),
    gradient: cfg.gradient,
    iconColor: cfg.iconColor,
  }));

  // Determine which permissions still need requesting
  const pendingPermissions = permissionConfigs.filter(
    (p) => permStates[p.type] === 'prompt'
  );

  useEffect(() => {
    // Only show once ever - don't keep pestering users
    const dismissed = localStorage.getItem(PERMISSION_DISMISSED_KEY);
    if (dismissed === 'true') return;

    const checked = localStorage.getItem(PERMISSION_CHECK_KEY);
    if (checked) {
      // Don't re-check - user already handled this
      return;
    }

    const checkAll = async () => {
      const [loc, notif] = await Promise.all([
        checkPermissionStatus('location'),
        checkPermissionStatus('notifications'),
      ]);

      const newState: PermissionState = {
        location: loc,
        notifications: notif,
        storage: 'granted', // Skip storage permission
      };
      setPermStates(newState);

      // Show UI only if there are permissions to request
      const hasPending = [loc, notif].some((s) => s === 'prompt');
      if (hasPending) {
        // Show after a longer delay
        setTimeout(() => setVisible(true), 3000);
      }

      localStorage.setItem(PERMISSION_CHECK_KEY, String(Date.now()));
    };

    checkAll();
  }, []);

  const handleRequest = useCallback(async () => {
    if (pendingPermissions.length === 0) return;
    const perm = pendingPermissions[currentStep];
    if (!perm) return;

    setRequesting(true);
    const granted = await requestPermission(perm.type);
    setPermStates((prev) => ({
      ...prev,
      [perm.type]: granted ? 'granted' : 'denied',
    }));
    setRequesting(false);

    // Move to next permission or close
    if (currentStep < pendingPermissions.length - 1) {
      setCurrentStep((prev) => prev + 1);
    } else {
      setVisible(false);
    }
  }, [currentStep, pendingPermissions]);

  const handleDismiss = useCallback(() => {
    setVisible(false);
    localStorage.setItem(PERMISSION_DISMISSED_KEY, 'true');
  }, []);

  const handleSkip = useCallback(() => {
    if (currentStep < pendingPermissions.length - 1) {
      setCurrentStep((prev) => prev + 1);
    } else {
      setVisible(false);
      // All permissions skipped — don't show again
      localStorage.setItem(PERMISSION_DISMISSED_KEY, 'true');
    }
  }, [currentStep, pendingPermissions]);

  if (!visible || pendingPermissions.length === 0) return null;

  const config = pendingPermissions[currentStep];
  if (!config) return null;
  const Icon = config.icon;

  return (
    <div
      data-testid="permission-manager-overlay"
      className="fixed bottom-20 left-3 right-3 z-[60] animate-in slide-in-from-bottom-4 duration-500"
      dir={dir}
    >
      <div className="w-full max-w-md mx-auto glass-mystic rounded-2xl shadow-2xl overflow-hidden border border-border/20">
        {/* Compact Header */}
        <div className={cn('relative p-4 bg-gradient-to-br', config.gradient)}>
          <button
            onClick={handleDismiss}
            data-testid="permission-dismiss-btn"
            className="absolute top-3 start-3 p-1.5 rounded-xl bg-white/10 hover:bg-white/20 transition-colors"
          >
            <X className="h-3.5 w-3.5 text-white" />
          </button>

          <div className="flex items-center gap-3 ps-8">
            <div className="h-10 w-10 rounded-xl bg-white/15 flex items-center justify-center shrink-0">
              <Icon className={cn('h-5 w-5', config.iconColor)} />
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-sm font-bold text-white truncate">{config.title}</h2>
              <p className="text-white/70 text-xs mt-0.5 truncate">{config.subtitle}</p>
            </div>
          </div>
        </div>

        {/* Compact Actions */}
        <div className="p-3 flex gap-2">
          <button
            onClick={handleRequest}
            disabled={requesting}
            data-testid={`permission-grant-${config.type}`}
            className={cn(
              'flex-1 py-2.5 rounded-xl font-bold text-xs text-white transition-all active:scale-[0.98]',
              'bg-gradient-to-r',
              config.gradient,
              requesting && 'opacity-60'
            )}
          >
            {requesting ? '...' : t('permAllowBtn')}
          </button>
          <button
            onClick={handleSkip}
            data-testid={`permission-skip-${config.type}`}
            className="flex-1 py-2.5 rounded-xl text-xs text-muted-foreground hover:text-foreground transition-colors bg-muted/30"
          >
            {t('permLaterBtn')}
          </button>
        </div>
      </div>
    </div>
  );
}
