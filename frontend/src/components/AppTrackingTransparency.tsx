/**
 * AppTrackingTransparency - iOS 14.5+ ATT compliance
 * Required by Apple for any app that tracks users or uses advertising identifiers
 * Shows BEFORE any tracking begins (GDPR + ATT combined approach)
 */
import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Eye, EyeOff } from 'lucide-react';
import { isNativeApp, isIOS, hapticFeedback } from '@/lib/nativeBridge';
import { useLocale } from '@/hooks/useLocale';

const ATT_STORAGE_KEY = 'att-consent-status';

export type ATTStatus = 'not-determined' | 'authorized' | 'denied' | 'restricted';

export function getATTStatus(): ATTStatus {
  return (localStorage.getItem(ATT_STORAGE_KEY) as ATTStatus) || 'not-determined';
}

export default function AppTrackingTransparency() {
  const { locale } = useLocale();
  const [show, setShow] = useState(false);
  const isArabic = locale === 'ar';

  useEffect(() => {
    // Only show on iOS native app and if not already determined
    if (!isNativeApp() || !isIOS()) return;
    if (getATTStatus() !== 'not-determined') return;

    // Show after a short delay to not stack with other prompts
    const timer = setTimeout(() => setShow(true), 2000);
    return () => clearTimeout(timer);
  }, []);

  const handleAuthorize = () => {
    hapticFeedback('light');
    localStorage.setItem(ATT_STORAGE_KEY, 'authorized');
    localStorage.setItem('personalized-ads', 'true');
    setShow(false);
  };

  const handleDeny = () => {
    hapticFeedback('light');
    localStorage.setItem(ATT_STORAGE_KEY, 'denied');
    localStorage.setItem('personalized-ads', 'false');
    setShow(false);
  };

  if (!show) return null;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-[250] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <motion.div
          className="w-full max-w-sm bg-card rounded-3xl p-6 shadow-2xl border border-border/20"
          initial={{ scale: 0.85, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.85, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 25 }}
          dir={isArabic ? 'rtl' : 'ltr'}
        >
          {/* Icon */}
          <div className="flex justify-center mb-5">
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center">
              <Shield className="h-8 w-8 text-primary" />
            </div>
          </div>

          {/* Title */}
          <h3 className="text-lg font-bold text-center mb-3">
            {isArabic
              ? '"أذان وحكاية" يود إذنك للتتبع'
              : '"Azan & Hikaya" Would Like Permission to Track'}
          </h3>

          {/* Description */}
          <p className="text-sm text-muted-foreground text-center mb-6 leading-relaxed">
            {isArabic
              ? 'نستخدم بياناتك لتقديم إعلانات مخصصة وتحسين تجربتك. لن نشارك بياناتك الشخصية مع أطراف ثالثة.'
              : 'Your data will be used to deliver personalized ads and improve your experience. We do not share your personal data with third parties.'}
          </p>

          {/* Buttons */}
          <div className="flex flex-col gap-2">
            <button
              onClick={handleAuthorize}
              className="w-full flex items-center justify-center gap-2 rounded-2xl bg-primary text-primary-foreground font-bold py-3 transition-all active:scale-[0.98]"
            >
              <Eye className="h-4 w-4" />
              {isArabic ? 'السماح' : 'Allow'}
            </button>
            <button
              onClick={handleDeny}
              className="w-full flex items-center justify-center gap-2 rounded-2xl bg-muted/50 text-foreground font-medium py-3 transition-all active:scale-[0.98]"
            >
              <EyeOff className="h-4 w-4" />
              {isArabic ? 'عدم السماح' : 'Ask App Not to Track'}
            </button>
          </div>

          {/* Privacy link */}
          <p className="text-xs text-muted-foreground text-center mt-4">
            {isArabic ? (
              <a href="/privacy" className="underline">سياسة الخصوصية</a>
            ) : (
              <a href="/privacy" className="underline">Privacy Policy</a>
            )}
          </p>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
