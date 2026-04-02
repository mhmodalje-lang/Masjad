/**
 * 🕌 Full-Screen Athan — Clean Mobile-First Design v4
 * No overlapping text. No notification tray audio.
 * Beautiful, clean, properly spaced for all screens.
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Volume2, VolumeX } from 'lucide-react';
import { stopAthan, playAthan } from '@/lib/athanAudio';
import { useLocale } from '@/hooks/useLocale';

const NAMES: Record<string, Record<string, string>> = {
  fajr:    { ar: 'الفجر', en: 'Fajr', tr: 'Sabah', fr: "L'Aube", de: 'Fajr', ru: 'Фаджр' },
  dhuhr:   { ar: 'الظهر', en: 'Dhuhr', tr: 'Öğle', fr: 'Dhuhr', de: 'Dhuhr', ru: 'Зухр' },
  asr:     { ar: 'العصر', en: 'Asr', tr: 'İkindi', fr: 'Asr', de: 'Asr', ru: 'Аср' },
  maghrib: { ar: 'المغرب', en: 'Maghrib', tr: 'Akşam', fr: 'Maghrib', de: 'Maghrib', ru: 'Магриб' },
  isha:    { ar: 'العشاء', en: 'Isha', tr: 'Yatsı', fr: 'Isha', de: 'Isha', ru: 'Иша' },
};

interface Props {
  prayerKey: string | null;
  prayerTime: string;
  onDismiss: () => void;
}

export default function FullScreenAthan({ prayerKey, prayerTime, onDismiss }: Props) {
  const { t, locale, dir } = useLocale();
  const [show, setShow] = useState(false);
  const [secs, setSecs] = useState(0);
  const [muted, setMuted] = useState(false);
  const wl = useRef<any>(null);
  const tmr = useRef<any>(null);
  const vib = useRef<any>(null);

  useEffect(() => {
    if (!prayerKey) return;
    setShow(true); setSecs(0); setMuted(false);
    // Wake Lock
    try { if ('wakeLock' in navigator) (navigator as any).wakeLock.request('screen').then((l: any) => { wl.current = l; }).catch(() => {}); } catch {}
    // Fullscreen
    try { document.documentElement.requestFullscreen?.(); } catch {}
    // Audio
    stopAthan(); playAthan(prayerKey);
    // Vibrate alarm pattern
    if ('vibrate' in navigator) {
      const v = () => navigator.vibrate([400, 200, 400, 200, 600]);
      v(); vib.current = setInterval(v, 5000);
    }
    // Timer
    tmr.current = setInterval(() => setSecs(p => p + 1), 1000);
    // Auto-dismiss 5min
    const auto = setTimeout(dismiss, 300000);
    return () => { clearInterval(tmr.current); clearTimeout(auto); };
  }, [prayerKey]);

  const dismiss = useCallback(() => {
    setShow(false);
    stopAthan();
    try { wl.current?.release(); } catch {} wl.current = null;
    try { if (document.fullscreenElement) document.exitFullscreen(); } catch {}
    clearInterval(tmr.current); clearInterval(vib.current);
    try { navigator.vibrate?.(0); } catch {}
    setTimeout(onDismiss, 400);
  }, [onDismiss]);

  const toggleMute = () => {
    if (muted) { if (prayerKey) { stopAthan(); playAthan(prayerKey); } setMuted(false); }
    else { stopAthan(); try { navigator.vibrate?.(0); } catch {} clearInterval(vib.current); setMuted(true); }
  };

  if (!prayerKey) return null;
  const name = NAMES[prayerKey]?.[locale] || NAMES[prayerKey]?.en || '';
  const arName = NAMES[prayerKey]?.ar || '';
  const mm = Math.floor(secs / 60).toString().padStart(2, '0');
  const ss = (secs % 60).toString().padStart(2, '0');

  return (
    <AnimatePresence>
      {show && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          className="fixed inset-0 z-[99999]" dir={dir}>

          {/* BG: Mecca with slow zoom */}
          <motion.img src="/mecca-hero.webp" alt="" className="absolute inset-0 w-full h-full object-cover"
            initial={{ scale: 1 }} animate={{ scale: 1.08 }} transition={{ duration: 60, ease: 'linear' }} />

          {/* Overlay */}
          <div className="absolute inset-0 bg-black/60" />

          {/* Layout: flex column with safe spacing */}
          <div className="absolute inset-0 flex flex-col items-center justify-between z-10"
            style={{ paddingTop: 'max(env(safe-area-inset-top), 16px)', paddingBottom: 'max(env(safe-area-inset-bottom), 16px)' }}>

            {/* TOP: Controls */}
            <div className="w-full flex justify-between px-5 pt-2">
              <motion.button initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
                onClick={toggleMute} className="w-11 h-11 rounded-full bg-white/10 flex items-center justify-center active:scale-90">
                {muted ? <VolumeX className="w-5 h-5 text-white/70" /> : <Volume2 className="w-5 h-5 text-white/70" />}
              </motion.button>
              <motion.button initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
                onClick={dismiss} className="w-11 h-11 rounded-full bg-white/10 flex items-center justify-center active:scale-90">
                <X className="w-5 h-5 text-white/70" />
              </motion.button>
            </div>

            {/* CENTER: Main content */}
            <div className="flex-1 flex flex-col items-center justify-center px-8 gap-4">
              {/* Small label */}
              <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}
                className="text-amber-300/60 text-xs tracking-[0.3em] uppercase">
                {t('prayerTimeNow') || 'حان وقت الصلاة'}
              </motion.p>

              {/* Prayer name */}
              <motion.h1 initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.5, type: 'spring', damping: 15 }}
                className="text-white text-5xl font-black leading-none"
                style={{ textShadow: '0 2px 20px rgba(212,168,67,0.3)' }}>
                {locale === 'ar' ? arName : name}
              </motion.h1>

              {locale !== 'ar' && (
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 }}
                  className="text-white/25 text-xl" dir="rtl">{arName}</motion.p>
              )}

              {/* Time */}
              <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.65 }}
                className="text-white/80 text-2xl font-light tabular-nums">
                {prayerTime}
              </motion.p>

              {/* Sound indicator */}
              {!muted && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 }}
                  className="flex items-center gap-2">
                  <div className="flex items-end gap-[2px] h-4">
                    {[0.3, 0.7, 1, 0.6, 0.9, 0.4, 0.8].map((h, i) => (
                      <motion.div key={i} animate={{ scaleY: [h, 1, h] }}
                        transition={{ duration: 0.5, repeat: Infinity, delay: i * 0.06 }}
                        className="w-[2px] bg-amber-400/50 rounded-full origin-bottom" style={{ height: '100%' }} />
                    ))}
                  </div>
                  <span className="text-white/30 text-xs">{mm}:{ss}</span>
                </motion.div>
              )}
            </div>

            {/* BOTTOM: Dua + Button */}
            <div className="w-full flex flex-col items-center gap-3 px-6 pb-2">
              {/* Dua for parents */}
              <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 }}
                className="text-amber-200/50 text-xs text-center leading-relaxed max-w-xs" dir="rtl">
                اللهم اغفر لوالديّ وارحمهما كما ربياني صغيرًا 🤲
              </motion.p>

              {/* Stop button */}
              <motion.button initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.9 }} onClick={dismiss}
                className="w-full max-w-xs py-4 rounded-2xl font-bold text-base text-white bg-amber-700/30 border border-amber-500/20 active:scale-95 backdrop-blur-sm">
                {t('stopAthan') || 'إيقاف الأذان'}
              </motion.button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
