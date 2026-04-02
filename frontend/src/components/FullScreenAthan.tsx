/**
 * 🕌 Full-Screen Athan Experience
 * ================================
 * - Immersive full-screen overlay with beautiful mosque visuals
 * - Wake Lock to keep screen on during athan
 * - Alarm-like audio behavior (not media player)
 * - Works from ANY page (mounted in AppLayout)
 * - Auto-dismiss after full athan (5 min) or user interaction
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Volume2, VolumeX, Moon, Sun } from 'lucide-react';
import { stopAthan, playAthan, getSelectedAthan } from '@/lib/athanAudio';
import { useLocale } from '@/hooks/useLocale';

// Prayer-specific themes
const PRAYER_THEMES: Record<string, { gradient: string; bg: string; icon: string; pattern: string }> = {
  fajr:    { gradient: 'from-indigo-950 via-purple-950 to-blue-950', bg: '#1a0533', icon: '🌅', pattern: 'radial-gradient(circle at 50% 30%, rgba(99,102,241,0.15), transparent 70%)' },
  dhuhr:   { gradient: 'from-amber-900 via-orange-950 to-yellow-950', bg: '#2d1800', icon: '☀️', pattern: 'radial-gradient(circle at 50% 30%, rgba(245,158,11,0.15), transparent 70%)' },
  asr:     { gradient: 'from-sky-950 via-blue-950 to-indigo-950', bg: '#001233', icon: '🌤️', pattern: 'radial-gradient(circle at 50% 30%, rgba(14,165,233,0.12), transparent 70%)' },
  maghrib: { gradient: 'from-orange-950 via-red-950 to-purple-950', bg: '#1a0a00', icon: '🌇', pattern: 'radial-gradient(circle at 50% 30%, rgba(234,88,12,0.15), transparent 70%)' },
  isha:    { gradient: 'from-slate-950 via-gray-950 to-zinc-950', bg: '#0a0a0f', icon: '🌙', pattern: 'radial-gradient(circle at 50% 30%, rgba(99,102,241,0.1), transparent 70%)' },
};

const PRAYER_NAMES: Record<string, Record<string, string>> = {
  fajr:    { ar: 'الفجر', en: 'Fajr', tr: 'Sabah', fr: "L'Aube", de: 'Fajr', ru: 'Фаджр', sv: 'Fajr', nl: 'Fajr', el: 'Φάτζρ' },
  dhuhr:   { ar: 'الظهر', en: 'Dhuhr', tr: 'Öğle', fr: 'Midi', de: 'Dhuhr', ru: 'Зухр', sv: 'Dhuhr', nl: 'Dhuhr', el: 'Ζουχρ' },
  asr:     { ar: 'العصر', en: 'Asr', tr: 'İkindi', fr: "L'Après-midi", de: 'Asr', ru: 'Аср', sv: 'Asr', nl: 'Asr', el: 'Ασρ' },
  maghrib: { ar: 'المغرب', en: 'Maghrib', tr: 'Akşam', fr: 'Coucher', de: 'Maghrib', ru: 'Магриб', sv: 'Maghrib', nl: 'Maghrib', el: 'Μαγκρίμπ' },
  isha:    { ar: 'العشاء', en: 'Isha', tr: 'Yatsı', fr: 'Nuit', de: 'Isha', ru: 'Иша', sv: 'Isha', nl: 'Isha', el: 'Ίσα' },
};

interface FullScreenAthanProps {
  prayerKey: string | null;
  prayerTime: string;
  onDismiss: () => void;
}

export default function FullScreenAthan({ prayerKey, prayerTime, onDismiss }: FullScreenAthanProps) {
  const { t, locale, dir } = useLocale();
  const [visible, setVisible] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [muted, setMuted] = useState(false);
  const wakeLockRef = useRef<any>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Activate full-screen athan
  useEffect(() => {
    if (prayerKey) {
      setVisible(true);
      setElapsed(0);
      acquireWakeLock();
      requestFullscreen();
      // Start athan audio with alarm-like behavior
      startAthanAudio(prayerKey);
      // Start elapsed timer
      timerRef.current = setInterval(() => {
        setElapsed(prev => prev + 1);
      }, 1000);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [prayerKey]);

  // Auto-dismiss after 5 minutes
  useEffect(() => {
    if (!visible) return;
    const timer = setTimeout(() => handleDismiss(), 5 * 60 * 1000);
    return () => clearTimeout(timer);
  }, [visible]);

  // Wake Lock API - keeps screen on
  const acquireWakeLock = async () => {
    try {
      if ('wakeLock' in navigator) {
        wakeLockRef.current = await (navigator as any).wakeLock.request('screen');
        console.log('[Athan] Wake Lock acquired');
      }
    } catch (e) {
      console.warn('[Athan] Wake Lock failed:', e);
    }
  };

  const releaseWakeLock = () => {
    if (wakeLockRef.current) {
      wakeLockRef.current.release();
      wakeLockRef.current = null;
      console.log('[Athan] Wake Lock released');
    }
  };

  // Fullscreen API
  const requestFullscreen = async () => {
    try {
      const elem = document.documentElement;
      if (elem.requestFullscreen) {
        await elem.requestFullscreen();
      } else if ((elem as any).webkitRequestFullscreen) {
        await (elem as any).webkitRequestFullscreen();
      }
    } catch { /* Fullscreen not available */ }
  };

  const exitFullscreen = () => {
    try {
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else if ((document as any).webkitExitFullscreen) {
        (document as any).webkitExitFullscreen();
      }
    } catch {}
  };

  // Start Athan audio with alarm behavior
  const startAthanAudio = (prayer: string) => {
    stopAthan();
    const audio = playAthan(prayer);
    audioRef.current = audio;
    
    // Vibrate in alarm pattern
    if ('vibrate' in navigator) {
      // Continuous alarm-like vibration pattern
      const vibratePattern = () => {
        navigator.vibrate([500, 300, 500, 300, 800, 500, 500, 300, 500, 300, 800]);
      };
      vibratePattern();
      // Repeat vibration every 5 seconds
      const vibInterval = setInterval(vibratePattern, 5000);
      setTimeout(() => clearInterval(vibInterval), 5 * 60 * 1000);
    }
  };

  const handleDismiss = useCallback(() => {
    setVisible(false);
    stopAthan();
    releaseWakeLock();
    exitFullscreen();
    if (timerRef.current) clearInterval(timerRef.current);
    navigator.vibrate?.(0); // Stop vibration
    setTimeout(onDismiss, 400);
  }, [onDismiss]);

  const toggleMute = () => {
    if (muted) {
      // Unmute - replay
      if (prayerKey) startAthanAudio(prayerKey);
      setMuted(false);
    } else {
      stopAthan();
      navigator.vibrate?.(0);
      setMuted(true);
    }
  };

  if (!prayerKey) return null;
  const theme = PRAYER_THEMES[prayerKey] || PRAYER_THEMES.isha;
  const prayerName = PRAYER_NAMES[prayerKey]?.[locale] || PRAYER_NAMES[prayerKey]?.ar || prayerKey;
  const arabicName = PRAYER_NAMES[prayerKey]?.ar || '';
  const formatElapsed = `${Math.floor(elapsed / 60)}:${(elapsed % 60).toString().padStart(2, '0')}`;

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
          className={`fixed inset-0 z-[99999] flex flex-col items-center justify-center bg-gradient-to-b ${theme.gradient}`}
          dir={dir}
          style={{ background: theme.bg }}
        >
          {/* Ambient light effect */}
          <div className="absolute inset-0" style={{ background: theme.pattern }} />
          
          {/* Islamic geometric pattern overlay */}
          <div className="absolute inset-0 opacity-[0.04]" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }} />

          {/* Top bar - mute & close */}
          <div className="absolute top-0 left-0 right-0 flex items-center justify-between px-6 z-20" style={{ paddingTop: 'max(env(safe-area-inset-top, 12px), 16px)' }}>
            <button onClick={toggleMute} className="p-3 rounded-full bg-white/10 backdrop-blur-md border border-white/10 active:scale-95 transition-transform">
              {muted ? <VolumeX className="h-5 w-5 text-white/70" /> : <Volume2 className="h-5 w-5 text-white/70" />}
            </button>
            <button onClick={handleDismiss} className="p-3 rounded-full bg-white/10 backdrop-blur-md border border-white/10 active:scale-95 transition-transform">
              <X className="h-5 w-5 text-white/70" />
            </button>
          </div>

          {/* Main content */}
          <div className="flex flex-col items-center text-center px-8 relative z-10 max-w-md">
            
            {/* Mosque silhouette animation */}
            <motion.div 
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, type: 'spring', damping: 15 }}
              className="relative mb-8"
            >
              {/* Glowing orb behind icon */}
              <motion.div 
                animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.6, 0.3] }}
                transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
                className="absolute inset-0 rounded-full bg-white/10 blur-3xl scale-150"
              />
              <span className="text-8xl relative z-10 block">{theme.icon}</span>
            </motion.div>

            {/* "حان وقت الصلاة" */}
            <motion.p
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="text-white/50 text-base font-medium mb-3 tracking-wide"
            >
              {t('prayerTimeNow') || 'حان وقت الصلاة'}
            </motion.p>

            {/* Prayer name - large */}
            <motion.h1
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4, type: 'spring' }}
              className="text-white text-6xl font-bold mb-2 leading-tight"
            >
              {locale === 'ar' ? arabicName : prayerName}
            </motion.h1>

            {/* Secondary name */}
            {locale !== 'ar' && (
              <motion.p
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="text-white/40 text-2xl font-arabic mb-4"
                dir="rtl"
              >
                {arabicName}
              </motion.p>
            )}

            {/* Time */}
            <motion.p
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.55 }}
              className="text-white/70 text-4xl font-light tabular-nums mb-8"
            >
              {prayerTime}
            </motion.p>

            {/* Audio indicator with pulse */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="flex items-center gap-3 mb-10"
            >
              {!muted && (
                <>
                  {/* Sound wave animation */}
                  <div className="flex items-end gap-0.5 h-5">
                    {[0.3, 0.6, 1, 0.7, 0.4, 0.8, 0.5].map((h, i) => (
                      <motion.div
                        key={i}
                        animate={{ scaleY: [h, 1, h] }}
                        transition={{ duration: 0.8, repeat: Infinity, delay: i * 0.1 }}
                        className="w-1 bg-white/40 rounded-full origin-bottom"
                        style={{ height: '100%' }}
                      />
                    ))}
                  </div>
                  <span className="text-white/40 text-sm">{t('athanPlaying') || 'الأذان يُرفع'}</span>
                  <span className="text-white/30 text-xs tabular-nums">{formatElapsed}</span>
                </>
              )}
              {muted && (
                <span className="text-white/30 text-sm">{t('athanMuted') || 'صامت'}</span>
              )}
            </motion.div>
          </div>

          {/* Bottom section */}
          <div className="absolute bottom-0 left-0 right-0 flex flex-col items-center gap-4 z-20" style={{ paddingBottom: 'max(env(safe-area-inset-bottom, 20px), 24px)' }}>
            {/* Quranic verse */}
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.2 }}
              className="text-white/20 text-xs font-arabic leading-relaxed max-w-xs text-center px-8"
              dir="rtl"
            >
              حَافِظُوا عَلَى الصَّلَوَاتِ وَالصَّلَاةِ الْوُسْطَىٰ وَقُومُوا لِلَّهِ قَانِتِينَ
            </motion.p>

            {/* Dismiss button */}
            <motion.button
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.8 }}
              onClick={handleDismiss}
              className="w-72 bg-white/10 backdrop-blur-md border border-white/15 text-white font-bold rounded-2xl px-10 py-4 text-lg transition-all active:scale-95 hover:bg-white/15"
            >
              {t('stopAthan') || 'إيقاف الأذان'}
            </motion.button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

// Helper to get saved volume
function getSavedVolume(): number {
  return parseFloat(localStorage.getItem('athan-volume') || '0.8');
}
