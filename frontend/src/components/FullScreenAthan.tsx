/**
 * 🕌 Full-Screen Athan — Premium Immersive Experience
 * ====================================================
 * - Mecca image with slow cinematic zoom
 * - Wake Lock + Fullscreen API
 * - Alarm-like vibration & audio
 * - "ادعو لوالدي بالرحمة" message
 * - Works from ANY page
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Volume2, VolumeX } from 'lucide-react';
import { stopAthan, playAthan } from '@/lib/athanAudio';
import { useLocale } from '@/hooks/useLocale';

const PRAYER_NAMES: Record<string, Record<string, string>> = {
  fajr:    { ar: 'الفجر', en: 'Fajr', tr: 'Sabah', fr: "L'Aube", de: 'Fajr', ru: 'Фаджр', sv: 'Fajr', nl: 'Fajr', el: 'Φάτζρ' },
  dhuhr:   { ar: 'الظهر', en: 'Dhuhr', tr: 'Öğle', fr: 'Dhuhr', de: 'Dhuhr', ru: 'Зухр', sv: 'Dhuhr', nl: 'Dhuhr', el: 'Ζουχρ' },
  asr:     { ar: 'العصر', en: 'Asr', tr: 'İkindi', fr: 'Asr', de: 'Asr', ru: 'Аср', sv: 'Asr', nl: 'Asr', el: 'Ασρ' },
  maghrib: { ar: 'المغرب', en: 'Maghrib', tr: 'Akşam', fr: 'Maghrib', de: 'Maghrib', ru: 'Магриб', sv: 'Maghrib', nl: 'Maghrib', el: 'Μαγκρίμπ' },
  isha:    { ar: 'العشاء', en: 'Isha', tr: 'Yatsı', fr: 'Isha', de: 'Isha', ru: 'Иша', sv: 'Isha', nl: 'Isha', el: 'Ίσα' },
};

const PRAYER_ICONS: Record<string, string> = {
  fajr: '🌅', dhuhr: '☀️', asr: '🌤️', maghrib: '🌇', isha: '🌙',
};

const DUA_PARENTS: Record<string, string> = {
  ar: 'اللهم ارحم والديّ كما ربياني صغيرًا 🤲',
  en: 'O Allah, have mercy on my parents as they raised me when I was small 🤲',
  tr: "Allah'ım, beni küçükken yetiştirdikleri gibi anne babama merhamet et 🤲",
  fr: "Ô Allah, aie pitié de mes parents comme ils m'ont élevé petit 🤲",
  de: 'O Allah, erbarme Dich meiner Eltern, wie sie mich als Kind großgezogen haben 🤲',
  ru: 'О Аллах, помилуй моих родителей, как они растили меня в детстве 🤲',
  sv: 'O Allah, förbarma dig över mina föräldrar som de uppfostrade mig som liten 🤲',
  nl: 'O Allah, heb genade met mijn ouders zoals zij mij als kind hebben grootgebracht 🤲',
  el: 'Ω Αλλάχ, ελέησε τους γονείς μου όπως με μεγάλωσαν μικρό 🤲',
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
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const vibIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (prayerKey) {
      setVisible(true);
      setElapsed(0);
      setMuted(false);
      acquireWakeLock();
      requestFullscreen();
      startAthanAudio(prayerKey);
      timerRef.current = setInterval(() => setElapsed(prev => prev + 1), 1000);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [prayerKey]);

  useEffect(() => {
    if (!visible) return;
    const timer = setTimeout(() => handleDismiss(), 5 * 60 * 1000);
    return () => clearTimeout(timer);
  }, [visible]);

  const acquireWakeLock = async () => {
    try {
      if ('wakeLock' in navigator) {
        wakeLockRef.current = await (navigator as any).wakeLock.request('screen');
      }
    } catch {}
  };

  const releaseWakeLock = () => {
    try { wakeLockRef.current?.release(); } catch {}
    wakeLockRef.current = null;
  };

  const requestFullscreen = async () => {
    try {
      const el = document.documentElement;
      if (el.requestFullscreen) await el.requestFullscreen();
      else if ((el as any).webkitRequestFullscreen) await (el as any).webkitRequestFullscreen();
    } catch {}
  };

  const exitFullscreen = () => {
    try {
      if (document.fullscreenElement) document.exitFullscreen();
      else if ((document as any).webkitExitFullscreen) (document as any).webkitExitFullscreen();
    } catch {}
  };

  const startAthanAudio = (prayer: string) => {
    stopAthan();
    playAthan(prayer);
    if ('vibrate' in navigator) {
      const vibrate = () => navigator.vibrate([500, 200, 500, 200, 800, 400, 500, 200, 500, 200, 800]);
      vibrate();
      vibIntervalRef.current = setInterval(vibrate, 6000);
    }
  };

  const handleDismiss = useCallback(() => {
    setVisible(false);
    stopAthan();
    releaseWakeLock();
    exitFullscreen();
    if (timerRef.current) clearInterval(timerRef.current);
    if (vibIntervalRef.current) clearInterval(vibIntervalRef.current);
    try { navigator.vibrate?.(0); } catch {}
    setTimeout(onDismiss, 500);
  }, [onDismiss]);

  const toggleMute = () => {
    if (muted) {
      if (prayerKey) { stopAthan(); playAthan(prayerKey); }
      setMuted(false);
    } else {
      stopAthan();
      try { navigator.vibrate?.(0); } catch {}
      if (vibIntervalRef.current) clearInterval(vibIntervalRef.current);
      setMuted(true);
    }
  };

  if (!prayerKey) return null;
  const prayerName = PRAYER_NAMES[prayerKey]?.[locale] || PRAYER_NAMES[prayerKey]?.en || prayerKey;
  const arabicName = PRAYER_NAMES[prayerKey]?.ar || '';
  const icon = PRAYER_ICONS[prayerKey] || '🕌';
  const duaParents = DUA_PARENTS[locale] || DUA_PARENTS.ar;
  const mm = Math.floor(elapsed / 60);
  const ss = (elapsed % 60).toString().padStart(2, '0');

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.6 }}
          className="fixed inset-0 z-[99999] overflow-hidden"
          dir={dir}
        >
          {/* === Mecca Background with Cinematic Slow Zoom === */}
          <motion.div
            className="absolute inset-0"
            initial={{ scale: 1 }}
            animate={{ scale: 1.15 }}
            transition={{ duration: 60, ease: 'linear' }}
          >
            <img
              src="/mecca-hero.webp"
              alt="Mecca"
              className="w-full h-full object-cover"
            />
          </motion.div>

          {/* Dark gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-black/80" />

          {/* Golden shimmer at top */}
          <motion.div
            className="absolute top-0 left-0 right-0 h-1"
            style={{ background: 'linear-gradient(90deg, transparent, #d4a843, transparent)' }}
            animate={{ opacity: [0.3, 0.8, 0.3] }}
            transition={{ duration: 3, repeat: Infinity }}
          />

          {/* Top controls */}
          <div className="absolute top-0 left-0 right-0 flex items-center justify-between px-5 z-30" style={{ paddingTop: 'max(env(safe-area-inset-top, 12px), 16px)' }}>
            <motion.button
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              onClick={toggleMute}
              className="p-3.5 rounded-full bg-black/30 backdrop-blur-xl border border-white/10 active:scale-90 transition-transform"
            >
              {muted ? <VolumeX className="h-5 w-5 text-white/80" /> : <Volume2 className="h-5 w-5 text-white/80" />}
            </motion.button>
            <motion.button
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              onClick={handleDismiss}
              className="p-3.5 rounded-full bg-black/30 backdrop-blur-xl border border-white/10 active:scale-90 transition-transform"
            >
              <X className="h-5 w-5 text-white/80" />
            </motion.button>
          </div>

          {/* === Center Content === */}
          <div className="absolute inset-0 flex flex-col items-center justify-center z-20 px-6">
            {/* Prayer icon with golden glow */}
            <motion.div
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, type: 'spring', damping: 12 }}
              className="relative mb-4"
            >
              <motion.div
                animate={{ scale: [1, 1.3, 1], opacity: [0.2, 0.5, 0.2] }}
                transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
                className="absolute inset-0 rounded-full blur-3xl scale-[2]"
                style={{ background: 'radial-gradient(circle, rgba(212,168,67,0.4), transparent)' }}
              />
              <span className="text-7xl relative z-10 block drop-shadow-2xl">{icon}</span>
            </motion.div>

            {/* حان وقت الصلاة */}
            <motion.p
              initial={{ y: 15, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="text-amber-200/70 text-sm font-medium tracking-[0.2em] uppercase mb-3"
            >
              {t('prayerTimeNow') || 'حان وقت الصلاة'}
            </motion.p>

            {/* Prayer Name — BIG */}
            <motion.h1
              initial={{ y: 25, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.5, type: 'spring' }}
              className="text-white text-7xl font-black mb-1 drop-shadow-2xl"
              style={{ textShadow: '0 4px 30px rgba(212,168,67,0.3)' }}
            >
              {locale === 'ar' ? arabicName : prayerName}
            </motion.h1>

            {/* Arabic subtitle for non-Arabic users */}
            {locale !== 'ar' && (
              <motion.p
                initial={{ y: 15, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
                className="text-white/35 text-3xl font-arabic mb-3"
                dir="rtl"
              >
                صلاة {arabicName}
              </motion.p>
            )}

            {/* Time */}
            <motion.div
              initial={{ y: 15, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.65 }}
              className="bg-white/10 backdrop-blur-md rounded-2xl px-8 py-3 border border-white/10 mb-6"
            >
              <span className="text-white/90 text-3xl font-light tabular-nums">{prayerTime}</span>
            </motion.div>

            {/* Sound wave + timer */}
            {!muted && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8 }}
                className="flex items-center gap-3 mb-6"
              >
                <div className="flex items-end gap-[3px] h-6">
                  {[0.3, 0.6, 1, 0.8, 0.5, 0.9, 0.4, 0.7, 0.6].map((h, i) => (
                    <motion.div
                      key={i}
                      animate={{ scaleY: [h, 1, h] }}
                      transition={{ duration: 0.6 + i * 0.08, repeat: Infinity, delay: i * 0.05 }}
                      className="w-[3px] rounded-full origin-bottom"
                      style={{ height: '100%', background: 'linear-gradient(to top, rgba(212,168,67,0.6), rgba(255,255,255,0.4))' }}
                    />
                  ))}
                </div>
                <span className="text-white/40 text-sm">{t('athanPlaying') || 'الأذان يُرفع'}</span>
                <span className="text-white/25 text-xs tabular-nums font-mono">{mm}:{ss}</span>
              </motion.div>
            )}
            {muted && (
              <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-white/25 text-sm mb-6">
                {t('athanMuted') || 'صامت'}
              </motion.p>
            )}

            {/* === ادعو لوالدي === */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.2 }}
              className="bg-amber-900/20 backdrop-blur-sm rounded-2xl px-6 py-3 border border-amber-500/15 max-w-sm"
            >
              <p className="text-amber-200/80 text-sm text-center leading-relaxed font-medium" dir={locale === 'ar' ? 'rtl' : 'ltr'}>
                {duaParents}
              </p>
            </motion.div>
          </div>

          {/* === Bottom Section === */}
          <div className="absolute bottom-0 left-0 right-0 flex flex-col items-center gap-3 z-30 px-6" style={{ paddingBottom: 'max(env(safe-area-inset-bottom, 16px), 20px)' }}>
            {/* Quranic verse */}
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.5 }}
              className="text-white/15 text-[11px] font-arabic text-center leading-relaxed max-w-xs"
              dir="rtl"
            >
              حَافِظُوا عَلَى الصَّلَوَاتِ وَالصَّلَاةِ الْوُسْطَىٰ وَقُومُوا لِلَّهِ قَانِتِينَ
            </motion.p>

            {/* Stop Athan Button */}
            <motion.button
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.9, type: 'spring' }}
              onClick={handleDismiss}
              className="w-full max-w-xs py-4 rounded-2xl font-bold text-lg text-white transition-all active:scale-95"
              style={{ background: 'linear-gradient(135deg, rgba(212,168,67,0.3), rgba(212,168,67,0.15))', border: '1px solid rgba(212,168,67,0.25)', backdropFilter: 'blur(12px)' }}
            >
              {t('stopAthan') || 'إيقاف الأذان'}
            </motion.button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
