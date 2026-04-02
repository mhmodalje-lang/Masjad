/**
 * 🕌 Full-Screen Athan — Premium Immersive Experience v3
 * =======================================================
 * - Mecca image with cinematic slow zoom
 * - Animated mosque silhouette + crescent moon SVG
 * - Wake Lock + Fullscreen API + Alarm vibration
 * - "ادعو لوالدي بالرحمة" dedication message
 * - Works from ANY page (mounted in AppLayout)
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

const DUA_PARENTS: Record<string, string> = {
  ar: 'اللهم ارحم والديّ كما ربياني صغيرًا 🤲',
  en: 'O Allah, have mercy on my parents as they raised me when I was small 🤲',
  tr: "Allah'ım, beni küçükken yetiştirdikleri gibi anne babama merhamet et 🤲",
  fr: "Ô Allah, aie pitié de mes parents comme ils m'ont élevé petit 🤲",
  de: 'O Allah, erbarme Dich meiner Eltern, wie sie mich großgezogen haben 🤲',
  ru: 'О Аллах, помилуй моих родителей, как они растили меня в детстве 🤲',
  sv: 'O Allah, förbarma dig över mina föräldrar som de uppfostrade mig 🤲',
  nl: 'O Allah, heb genade met mijn ouders zoals zij mij hebben grootgebracht 🤲',
  el: 'Ω Αλλάχ, ελέησε τους γονείς μου όπως με μεγάλωσαν μικρό 🤲',
};

/* ══ Animated Mosque Silhouette SVG ══ */
function MosqueSilhouette() {
  return (
    <motion.svg
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 0.12, y: 0 }}
      transition={{ delay: 0.8, duration: 2, ease: 'easeOut' }}
      viewBox="0 0 800 200" fill="white" className="absolute bottom-0 left-0 right-0 w-full pointer-events-none"
      style={{ maxHeight: '20vh' }}
    >
      {/* Central dome */}
      <ellipse cx="400" cy="140" rx="80" ry="70" />
      <rect x="370" y="60" width="60" height="80" rx="30" />
      {/* Crescent on top */}
      <circle cx="400" cy="50" r="12" />
      <circle cx="406" cy="48" r="10" fill="black" />
      {/* Left minaret */}
      <rect x="230" y="80" width="18" height="120" rx="3" />
      <ellipse cx="239" cy="80" rx="14" ry="20" />
      <circle cx="239" cy="56" r="5" />
      <circle cx="243" cy="55" r="4" fill="black" />
      {/* Right minaret */}
      <rect x="552" y="80" width="18" height="120" rx="3" />
      <ellipse cx="561" cy="80" rx="14" ry="20" />
      <circle cx="561" cy="56" r="5" />
      <circle cx="565" cy="55" r="4" fill="black" />
      {/* Side domes */}
      <ellipse cx="310" cy="160" rx="45" ry="35" />
      <ellipse cx="490" cy="160" rx="45" ry="35" />
      {/* Base */}
      <rect x="180" y="190" width="440" height="20" rx="4" />
      {/* Far minarets */}
      <rect x="160" y="120" width="12" height="80" rx="2" />
      <rect x="628" y="120" width="12" height="80" rx="2" />
    </motion.svg>
  );
}

/* ══ Floating Stars ══ */
function FloatingStars() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {[...Array(20)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute rounded-full bg-white"
          style={{
            width: Math.random() * 3 + 1,
            height: Math.random() * 3 + 1,
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 60}%`,
          }}
          animate={{ opacity: [0, 0.6, 0] }}
          transition={{ duration: 2 + Math.random() * 3, repeat: Infinity, delay: Math.random() * 4 }}
        />
      ))}
    </div>
  );
}

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
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [prayerKey]);

  useEffect(() => {
    if (!visible) return;
    const t = setTimeout(() => handleDismiss(), 5 * 60 * 1000);
    return () => clearTimeout(t);
  }, [visible]);

  const acquireWakeLock = async () => {
    try { if ('wakeLock' in navigator) wakeLockRef.current = await (navigator as any).wakeLock.request('screen'); } catch {}
  };
  const releaseWakeLock = () => { try { wakeLockRef.current?.release(); } catch {} wakeLockRef.current = null; };
  const requestFullscreen = async () => {
    try {
      const el = document.documentElement;
      if (el.requestFullscreen) await el.requestFullscreen();
      else if ((el as any).webkitRequestFullscreen) await (el as any).webkitRequestFullscreen();
    } catch {}
  };
  const exitFullscreen = () => {
    try { if (document.fullscreenElement) document.exitFullscreen(); } catch {}
  };

  const startAthanAudio = (prayer: string) => {
    stopAthan();
    playAthan(prayer);
    if ('vibrate' in navigator) {
      const vib = () => navigator.vibrate([500, 200, 500, 200, 800, 400, 500, 200, 500]);
      vib();
      vibIntervalRef.current = setInterval(vib, 6000);
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
          {/* ═══ Mecca Background with Cinematic Zoom ═══ */}
          <motion.div
            className="absolute inset-0"
            initial={{ scale: 1.0 }}
            animate={{ scale: 1.12 }}
            transition={{ duration: 90, ease: 'linear' }}
          >
            <img src="/mecca-hero.webp" alt="" className="w-full h-full object-cover" />
          </motion.div>

          {/* Dark cinematic overlay */}
          <div className="absolute inset-0" style={{ background: 'linear-gradient(to bottom, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.40) 40%, rgba(0,0,0,0.70) 100%)' }} />

          {/* Floating stars (for Isha/Fajr feel) */}
          <FloatingStars />

          {/* Animated mosque silhouette at bottom */}
          <MosqueSilhouette />

          {/* Golden shimmer line */}
          <motion.div
            className="absolute top-0 left-0 right-0 h-[2px]"
            style={{ background: 'linear-gradient(90deg, transparent 0%, #d4a843 50%, transparent 100%)' }}
            animate={{ opacity: [0.2, 0.7, 0.2] }}
            transition={{ duration: 3, repeat: Infinity }}
          />

          {/* ═══ Top Controls ═══ */}
          <div className="absolute top-0 left-0 right-0 flex items-center justify-between px-5 z-30" style={{ paddingTop: 'max(env(safe-area-inset-top, 14px), 18px)' }}>
            <motion.button initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}
              onClick={toggleMute}
              className="p-3 rounded-full bg-black/40 backdrop-blur-xl border border-white/10 active:scale-90 transition-transform">
              {muted ? <VolumeX className="h-5 w-5 text-white/80" /> : <Volume2 className="h-5 w-5 text-white/80" />}
            </motion.button>
            <motion.button initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}
              onClick={handleDismiss}
              className="p-3 rounded-full bg-black/40 backdrop-blur-xl border border-white/10 active:scale-90 transition-transform">
              <X className="h-5 w-5 text-white/80" />
            </motion.button>
          </div>

          {/* ═══ Center Content ═══ */}
          <div className="absolute inset-0 flex flex-col items-center justify-center z-20 px-6">

            {/* Crescent + Star animated icon */}
            <motion.div
              initial={{ scale: 0, rotate: -30 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ delay: 0.3, type: 'spring', damping: 10 }}
              className="relative mb-3"
            >
              <motion.div
                animate={{ scale: [1, 1.25, 1], opacity: [0.15, 0.4, 0.15] }}
                transition={{ duration: 4, repeat: Infinity }}
                className="absolute inset-0 rounded-full blur-3xl scale-[3]"
                style={{ background: 'radial-gradient(circle, rgba(212,168,67,0.5), transparent)' }}
              />
              <svg width="80" height="80" viewBox="0 0 100 100" className="relative z-10 drop-shadow-2xl">
                {/* Crescent */}
                <motion.circle cx="50" cy="50" r="30" fill="#d4a843" animate={{ opacity: [0.8, 1, 0.8] }} transition={{ duration: 2, repeat: Infinity }} />
                <circle cx="60" cy="42" r="25" fill="black" fillOpacity="0.85" />
                {/* Star */}
                <motion.polygon
                  points="78,28 80,34 86,34 81,38 83,44 78,40 73,44 75,38 70,34 76,34"
                  fill="#d4a843"
                  animate={{ opacity: [0.6, 1, 0.6], scale: [0.9, 1.1, 0.9] }}
                  transition={{ duration: 2.5, repeat: Infinity }}
                  style={{ transformOrigin: '78px 36px' }}
                />
              </svg>
            </motion.div>

            {/* حان وقت الصلاة */}
            <motion.p initial={{ y: 15, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.5 }}
              className="text-amber-200/60 text-sm font-medium tracking-[0.25em] uppercase mb-2">
              {t('prayerTimeNow') || 'حان وقت الصلاة'}
            </motion.p>

            {/* Prayer Name */}
            <motion.h1 initial={{ y: 25, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.6, type: 'spring' }}
              className="text-white text-6xl sm:text-7xl font-black mb-1 drop-shadow-2xl"
              style={{ textShadow: '0 4px 40px rgba(212,168,67,0.4)' }}>
              {locale === 'ar' ? arabicName : prayerName}
            </motion.h1>

            {locale !== 'ar' && (
              <motion.p initial={{ y: 10, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.7 }}
                className="text-white/30 text-2xl font-arabic mb-2" dir="rtl">
                صلاة {arabicName}
              </motion.p>
            )}

            {/* Time pill */}
            <motion.div initial={{ y: 15, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.75 }}
              className="bg-white/10 backdrop-blur-xl rounded-2xl px-8 py-3 border border-white/10 mb-5">
              <span className="text-white/90 text-3xl font-light tabular-nums">{prayerTime}</span>
            </motion.div>

            {/* Sound wave */}
            {!muted && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.9 }} className="flex items-center gap-3 mb-5">
                <div className="flex items-end gap-[3px] h-6">
                  {[0.3, 0.7, 1, 0.8, 0.4, 0.9, 0.5, 0.7, 0.3].map((h, i) => (
                    <motion.div key={i}
                      animate={{ scaleY: [h, 1, h] }}
                      transition={{ duration: 0.5 + i * 0.06, repeat: Infinity, delay: i * 0.04 }}
                      className="w-[3px] rounded-full origin-bottom"
                      style={{ height: '100%', background: 'linear-gradient(to top, rgba(212,168,67,0.7), rgba(255,255,255,0.5))' }}
                    />
                  ))}
                </div>
                <span className="text-white/35 text-sm">{t('athanPlaying') || 'الأذان يُرفع'}</span>
                <span className="text-white/20 text-xs tabular-nums font-mono">{mm}:{ss}</span>
              </motion.div>
            )}
            {muted && <p className="text-white/20 text-sm mb-5">{t('athanMuted') || 'صامت'}</p>}

            {/* ═══ Dua for Parents ═══ */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 1.3 }}
              className="bg-amber-950/40 backdrop-blur-sm rounded-2xl px-5 py-3.5 border border-amber-500/15 max-w-sm">
              <p className="text-amber-200/80 text-[13px] text-center leading-relaxed font-medium" dir={locale === 'ar' ? 'rtl' : 'ltr'}>
                {duaParents}
              </p>
            </motion.div>
          </div>

          {/* ═══ Bottom ═══ */}
          <div className="absolute bottom-0 left-0 right-0 flex flex-col items-center gap-2.5 z-30 px-6" style={{ paddingBottom: 'max(env(safe-area-inset-bottom, 16px), 22px)' }}>
            <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.8 }}
              className="text-white/10 text-[10px] font-arabic text-center max-w-xs" dir="rtl">
              حَافِظُوا عَلَى الصَّلَوَاتِ وَالصَّلَاةِ الْوُسْطَىٰ وَقُومُوا لِلَّهِ قَانِتِينَ
            </motion.p>
            <motion.button initial={{ y: 25, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 1.0, type: 'spring' }}
              onClick={handleDismiss}
              className="w-full max-w-xs py-4 rounded-2xl font-bold text-lg text-white active:scale-95 transition-transform"
              style={{ background: 'linear-gradient(135deg, rgba(212,168,67,0.35), rgba(212,168,67,0.15))', border: '1px solid rgba(212,168,67,0.3)', backdropFilter: 'blur(16px)' }}>
              {t('stopAthan') || 'إيقاف الأذان'}
            </motion.button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
