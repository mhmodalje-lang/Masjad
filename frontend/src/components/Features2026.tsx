import React, { useState, useEffect } from 'react';
import { X, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLocale } from '@/hooks/useLocale';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

/* 1. Daily Dua Widget - shows AI-generated dua */
export function DailyDuaWidget() {
  const { t, dir } = useLocale();
  const [dua, setDua] = useState<{ text: string; source: string } | null>(null);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    // Check if already dismissed today
    const today = new Date().toISOString().split('T')[0];
    const cached = localStorage.getItem('daily_dua_cache');
    if (cached) {
      try {
        const data = JSON.parse(cached);
        if (data.date === today) { setDua(data.dua); return; }
      } catch {}
    }
    // Fetch from AI
    fetch(`${BACKEND_URL}/api/ai/daily-dua`)
      .then(r => r.json())
      .then(d => {
        if (d.dua) {
          setDua(d.dua);
          localStorage.setItem('daily_dua_cache', JSON.stringify({ date: today, dua: d.dua }));
        }
      })
      .catch(() => {
        setDua({ text: 'اللَّهُمَّ إِنِّي أَسْأَلُكَ الْهُدَى وَالتُّقَى وَالْعَفَافَ وَالْغِنَى', source: t('sahihMuslim') });
      });
  }, []);

  if (!dua || !visible) return null;

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
      className="mx-4 mb-4 rounded-2xl bg-gradient-to-br from-primary/10 via-primary/5 to-transparent border border-primary/20 p-4 relative overflow-hidden" dir={dir}>
      <div className="absolute top-0 left-0 w-24 h-24 bg-primary/5 rounded-full -translate-x-8 -translate-y-8" />
      <button onClick={() => setVisible(false)} className="absolute top-2 left-2 p-1 rounded-full bg-muted/50">
        <X className="h-3 w-3 text-muted-foreground" />
      </button>
      <div className="flex items-start gap-2 mb-2">
        <Sparkles className="h-4 w-4 text-primary shrink-0 mt-0.5" />
        <span className="text-[10px] font-bold text-primary">{t('duaOfDay')}</span>
      </div>
      <p className="text-[15px] text-foreground leading-[2] font-medium" style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>{dua.text}</p>
      <p className="text-[10px] text-muted-foreground mt-2 text-left">{dua.source}</p>
    </motion.div>
  );
}

/* 2. Reading Time Estimate */
export function ReadingTime({ text }: { text: string }) {
  const { t } = useLocale();
  const words = text.split(/\s+/).length;
  const minutes = Math.max(1, Math.ceil(words / 200));
  return (
    <span className="text-[10px] text-muted-foreground flex items-center gap-1">
      ⏱ {minutes} {t('minutesReading')}
    </span>
  );
}

/* 3. Skeleton Loader */
export function StorySkeleton() {
  return (
    <div className="rounded-2xl bg-card border border-border/30 overflow-hidden animate-pulse">
      <div className="h-44 bg-muted/30" />
      <div className="p-4 space-y-3">
        <div className="flex items-center gap-2">
          <div className="h-7 w-7 rounded-full bg-muted/40" />
          <div className="h-3 w-20 rounded bg-muted/40" />
        </div>
        <div className="h-4 w-3/4 rounded bg-muted/40" />
        <div className="h-3 w-full rounded bg-muted/30" />
        <div className="h-3 w-2/3 rounded bg-muted/30" />
      </div>
    </div>
  );
}

export function VideoSkeleton() {
  return (
    <div className="rounded-2xl bg-card border border-border/30 overflow-hidden animate-pulse">
      <div className="aspect-[4/3] bg-muted/30" />
      <div className="p-2.5 space-y-1.5">
        <div className="h-3 w-3/4 rounded bg-muted/40" />
        <div className="h-2 w-1/2 rounded bg-muted/30" />
      </div>
    </div>
  );
}

/* 4. Pull to Refresh Indicator */
export function PullToRefresh({ onRefresh, children }: { onRefresh: () => Promise<void>; children: React.ReactNode }) {
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = async () => {
    setRefreshing(true);
    await onRefresh();
    setRefreshing(false);
  };

  return (
    <div>
      {refreshing && (
        <div className="flex justify-center py-3">
          <div className="h-5 w-5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
      )}
      {children}
    </div>
  );
}

/* 5. Content Report */
export function ReportButton({ contentId, contentType }: { contentId: string; contentType: string }) {
  const { t } = useLocale();
  const [reported, setReported] = useState(false);

  const handleReport = async () => {
    try {
      await fetch(`${BACKEND_URL}/api/report`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ content_id: contentId, content_type: contentType, reason: 'inappropriate' })
      });
      setReported(true);
    } catch {}
  };

  if (reported) return <span className="text-[10px] text-green-500">✓ {t('reported')}</span>;
  return (
    <button onClick={handleReport} className="text-[10px] text-muted-foreground hover:text-red-500 dark:text-red-400 transition-colors">
      {t('reportBtn')}
    </button>
  );
}

/* 6. Share as Image */
export async function shareStoryAsImage(title: string, content: string, author: string) {
  const appName = 'Azan & Hikaya';
  const text = `📖 ${title}\n\n${content.slice(0, 200)}${content.length > 200 ? '...' : ''}\n\n✍️ ${author}\n\n🕌 ${appName}`;
  if (navigator.share) {
    try {
      await navigator.share({ title, text });
    } catch {}
  } else {
    navigator.clipboard.writeText(text);
  }
}

/* 7. Recently Viewed */
export function useRecentlyViewed() {
  const addViewed = (storyId: string) => {
    const key = 'recently_viewed';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    const filtered = existing.filter((id: string) => id !== storyId);
    filtered.unshift(storyId);
    localStorage.setItem(key, JSON.stringify(filtered.slice(0, 20)));
  };

  const getViewed = (): string[] => {
    return JSON.parse(localStorage.getItem('recently_viewed') || '[]');
  };

  return { addViewed, getViewed };
}

/* 8. Prayer Time Countdown */
export function PrayerCountdown({ nextPrayer }: { nextPrayer?: { name: string; time: string } }) {
  const [timeLeft, setTimeLeft] = useState('');

  useEffect(() => {
    if (!nextPrayer) return;
    const update = () => {
      const now = new Date();
      const [h, m] = nextPrayer.time.split(':').map(Number);
      const target = new Date(now);
      target.setHours(h, m, 0, 0);
      if (target < now) target.setDate(target.getDate() + 1);
      const diff = target.getTime() - now.getTime();
      const hours = Math.floor(diff / 3600000);
      const mins = Math.floor((diff % 3600000) / 60000);
      const secs = Math.floor((diff % 60000) / 1000);
      setTimeLeft(`${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`);
    };
    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, [nextPrayer]);

  if (!nextPrayer || !timeLeft) return null;

  return (
    <div className="text-center">
      <p className="text-[10px] text-muted-foreground mb-0.5">{t('nextPrayerColon')} {nextPrayer.name}</p>
      <p className="text-lg font-mono font-bold text-primary" dir="ltr">{timeLeft}</p>
    </div>
  );
}

/* 9. Verse of the Day — V2026: Uses GlobalQuranVerse component */
export function VerseOfDay() {
  const { t, locale } = useLocale();
  const [verseRef, setVerseRef] = useState<{ surah: number; ayah: number } | null>(null);

  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    const cacheKey = `verse_of_day_ref_${locale}`;
    const cached = localStorage.getItem(cacheKey);
    if (cached) {
      try {
        const d = JSON.parse(cached);
        if (d.date === today) { setVerseRef(d.ref); return; }
      } catch {}
    }
    fetch(`${BACKEND_URL}/api/ai/verse-of-day?language=${locale}`)
      .then(r => r.json())
      .then(d => {
        if (d.verse) {
          // Extract surah:ayah from the response
          const ref = { surah: d.verse.surah_number || 65, ayah: d.verse.ayah || 2 };
          setVerseRef(ref);
          localStorage.setItem(cacheKey, JSON.stringify({ date: today, ref }));
        }
      })
      .catch(() => {
        // Default: At-Talaq 65:2-3
        setVerseRef({ surah: 65, ayah: 2 });
      });
  }, [locale]);

  if (!verseRef) return null;

  // Dynamically import GlobalQuranVerse to avoid circular dependencies
  const GlobalQuranVerse = React.lazy(() => import('@/components/GlobalQuranVerse'));

  return (
    <div className="mx-4 mb-4">
      <p className="text-[10px] font-bold text-primary mb-2 px-1">📖 {t('verseOfDay')}</p>
      <React.Suspense fallback={<div className="h-24 rounded-2xl bg-card/60 animate-pulse" />}>
        <GlobalQuranVerse
          surahId={verseRef.surah}
          ayahId={verseRef.ayah}
          compact={false}
          showExplanation={true}
          showAudio={true}
          showSurahName={true}
        />
      </React.Suspense>
    </div>
  );
}

/* 10. Hadith of the Day */
export function HadithOfDay() {
  const { t, locale } = useLocale();
  const [hadith, setHadith] = useState<{ text: string; translation?: string; narrator: string; source: string } | null>(null);

  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    const cacheKey = `hadith_of_day_${locale}`;
    const cached = localStorage.getItem(cacheKey);
    if (cached) {
      try {
        const d = JSON.parse(cached);
        if (d.date === today) { setHadith(d.hadith); return; }
      } catch {}
    }
    fetch(`${BACKEND_URL}/api/ai/hadith-of-day?language=${locale}`)
      .then(r => r.json())
      .then(d => {
        if (d.hadith) {
          setHadith(d.hadith);
          localStorage.setItem(cacheKey, JSON.stringify({ date: today, hadith: d.hadith }));
        }
      })
      .catch(() => {
        setHadith({ text: 'إنما الأعمال بالنيات وإنما لكل امرئ ما نوى', narrator: t('umarIbnKhattab'), source: t('bukhariAndMuslim') });
      });
  }, [locale]);

  if (!hadith) return null;
  const isAr = locale === 'ar';
  return (
    <div className="mx-4 mb-4 rounded-2xl bg-card border border-border/30 p-4">
      <p className="text-[10px] font-bold text-primary mb-2">📿 {t('hadithOfDay')}</p>
      <p className="text-[14px] text-foreground leading-[2] text-center" dir="rtl" style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>
        «{hadith.text}»
      </p>
      {!isAr && hadith.translation && (
        <p className="text-sm text-muted-foreground leading-relaxed text-center mt-2 pt-2 border-t border-border/30" dir="auto">
          «{hadith.translation}»
        </p>
      )}
      <p className="text-[10px] text-muted-foreground mt-2" dir="auto">{t('narratedBy')} {hadith.narrator} - {hadith.source}</p>
    </div>
  );
}

/* 11. Streak Badge */
export function StreakBadge() {
  const { t } = useLocale();
  const [streak, setStreak] = useState(0);
  useEffect(() => {
    const data = localStorage.getItem('login_streak');
    if (data) {
      try {
        const { count, lastDate } = JSON.parse(data);
        const today = new Date().toISOString().split('T')[0];
        const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
        if (lastDate === today) setStreak(count);
        else if (lastDate === yesterday) {
          const newCount = count + 1;
          setStreak(newCount);
          localStorage.setItem('login_streak', JSON.stringify({ count: newCount, lastDate: today }));
        } else {
          setStreak(1);
          localStorage.setItem('login_streak', JSON.stringify({ count: 1, lastDate: today }));
        }
      } catch { setStreak(1); }
    } else {
      const today = new Date().toISOString().split('T')[0];
      localStorage.setItem('login_streak', JSON.stringify({ count: 1, lastDate: today }));
      setStreak(1);
    }
  }, []);

  if (streak < 2) return null;
  return (
    <div className="inline-flex items-center gap-1 bg-primary/10 text-primary text-[10px] px-2 py-0.5 rounded-full font-bold">
      🔥 {streak} {t('consecutiveDays')}
    </div>
  );
}

/* 12. Font Size Control */
export function useFontSize() {
  const [size, setSize] = useState(() => {
    return parseInt(localStorage.getItem('font_size') || '16');
  });

  const increase = () => {
    const newSize = Math.min(24, size + 2);
    setSize(newSize);
    localStorage.setItem('font_size', String(newSize));
    document.documentElement.style.fontSize = `${newSize}px`;
  };

  const decrease = () => {
    const newSize = Math.max(12, size - 2);
    setSize(newSize);
    localStorage.setItem('font_size', String(newSize));
    document.documentElement.style.fontSize = `${newSize}px`;
  };

  useEffect(() => {
    document.documentElement.style.fontSize = `${size}px`;
  }, []);

  return { size, increase, decrease };
}
