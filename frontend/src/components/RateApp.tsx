/**
 * RateApp - Prompts users to rate the app on App Store / Play Store
 * Shows after meaningful engagement (e.g., 5th session, completed a task)
 * Compliant with Apple and Google guidelines for review prompts
 */
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Star, X, ExternalLink } from 'lucide-react';
import { isNativeApp, isIOS, isAndroid, hapticFeedback, openInBrowser } from '@/lib/nativeBridge';
import { useLocale } from '@/hooks/useLocale';

const RATE_STORAGE_KEY = 'app-rate-state';
const MIN_SESSIONS = 5;
const MIN_DAYS = 3;
const REMIND_AFTER_DAYS = 30;

const STORE_URLS = {
  ios: 'https://apps.apple.com/app/id0000000000', // Replace with actual App Store ID
  android: 'https://play.google.com/store/apps/details?id=com.azanwahikaya.app',
};

interface RateState {
  sessionCount: number;
  firstSessionDate: string;
  lastPromptDate?: string;
  rated: boolean;
  dismissed: boolean;
}

function getRateState(): RateState {
  try {
    const raw = localStorage.getItem(RATE_STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return {
    sessionCount: 0,
    firstSessionDate: new Date().toISOString(),
    rated: false,
    dismissed: false,
  };
}

function saveRateState(state: RateState) {
  localStorage.setItem(RATE_STORAGE_KEY, JSON.stringify(state));
}

export default function RateApp() {
  const { t, locale } = useLocale();
  const [show, setShow] = useState(false);

  useEffect(() => {
    // Only show in native app
    if (!isNativeApp()) return;

    const state = getRateState();
    state.sessionCount += 1;
    saveRateState(state);

    // Don't show if already rated
    if (state.rated) return;

    // Check minimum sessions
    if (state.sessionCount < MIN_SESSIONS) return;

    // Check minimum days since first use
    const daysSinceFirst = (Date.now() - new Date(state.firstSessionDate).getTime()) / (1000 * 60 * 60 * 24);
    if (daysSinceFirst < MIN_DAYS) return;

    // If dismissed, wait REMIND_AFTER_DAYS
    if (state.dismissed && state.lastPromptDate) {
      const daysSincePrompt = (Date.now() - new Date(state.lastPromptDate).getTime()) / (1000 * 60 * 60 * 24);
      if (daysSincePrompt < REMIND_AFTER_DAYS) return;
    }

    // Show prompt with delay
    const timer = setTimeout(() => {
      setShow(true);
      hapticFeedback('light');
    }, 8000);

    return () => clearTimeout(timer);
  }, []);

  const handleRate = async () => {
    hapticFeedback('success');
    const state = getRateState();
    state.rated = true;
    state.lastPromptDate = new Date().toISOString();
    saveRateState(state);
    setShow(false);

    const url = isIOS() ? STORE_URLS.ios : STORE_URLS.android;
    await openInBrowser(url);
  };

  const handleDismiss = () => {
    hapticFeedback('light');
    const state = getRateState();
    state.dismissed = true;
    state.lastPromptDate = new Date().toISOString();
    saveRateState(state);
    setShow(false);
  };

  const isArabic = locale === 'ar';

  if (!show) return null;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-[200] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={handleDismiss}
      >
        <motion.div
          className="w-full max-w-sm bg-card rounded-3xl p-6 shadow-2xl border border-border/30"
          initial={{ scale: 0.8, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.8, opacity: 0, y: 20 }}
          transition={{ type: 'spring', stiffness: 300, damping: 25 }}
          onClick={(e) => e.stopPropagation()}
          dir={isArabic ? 'rtl' : 'ltr'}
        >
          {/* Close button */}
          <button
            onClick={handleDismiss}
            className="absolute top-4 right-4 p-1.5 rounded-full hover:bg-muted/50 text-muted-foreground"
          >
            <X className="h-4 w-4" />
          </button>

          {/* Stars decoration */}
          <div className="flex justify-center mb-4">
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map((i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                >
                  <Star className="h-8 w-8 fill-amber-400 text-amber-400" />
                </motion.div>
              ))}
            </div>
          </div>

          {/* Title */}
          <h3 className="text-xl font-bold text-center mb-2">
            {isArabic ? 'هل أعجبك التطبيق؟' : 'Enjoying the App?'}
          </h3>

          {/* Description */}
          <p className="text-sm text-muted-foreground text-center mb-6 leading-relaxed">
            {isArabic
              ? 'إذا أعجبك تطبيق أذان وحكاية، يرجى تقييمه في المتجر. تقييمك يساعدنا كثيراً!'
              : 'If you enjoy Azan & Hikaya, please rate us on the store. Your review helps us a lot!'}
          </p>

          {/* Buttons */}
          <div className="flex flex-col gap-2">
            <button
              onClick={handleRate}
              className="w-full flex items-center justify-center gap-2 rounded-2xl bg-primary text-primary-foreground font-bold py-3 px-4 transition-all active:scale-[0.98]"
            >
              <ExternalLink className="h-4 w-4" />
              {isArabic ? 'قيّم التطبيق' : 'Rate the App'}
            </button>
            <button
              onClick={handleDismiss}
              className="w-full rounded-2xl text-muted-foreground font-medium py-2.5 px-4 hover:bg-muted/30 transition-all"
            >
              {isArabic ? 'لاحقاً' : 'Maybe Later'}
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
