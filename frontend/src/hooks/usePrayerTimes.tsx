import { useState, useEffect, useRef } from 'react';
import i18n from '@/lib/i18nConfig';
import {
  savePrayerTimes,
  getPrayerTimes as getCachedPrayerTimes,
  getLatestPrayerTimes,
  saveLocation,
  type CachedPrayerTimes,
} from '@/lib/offlineStorage';

export interface PrayerTime {
  name: string;
  time: string;       // formatted for display (12h or 24h)
  time24: string;     // always 24h for calculations
  key: string;
}

interface PrayerTimesData {
  prayers: PrayerTime[];
  hijriDate: string;
  hijriDay: string;
  hijriMonthAr: string;
  hijriMonthEn: string;
  hijriMonthNumber: number;
  hijriYear: string;
  hijriMonth: string;
  loading: boolean;
  error: string | null;
  isFromCache: boolean;
}

function detectIs12Hour(): boolean {
  try {
    const testDate = new Date(2024, 0, 1, 14, 0);
    const formatted = new Intl.DateTimeFormat(navigator.language, { hour: 'numeric' }).format(testDate);
    return !formatted.includes('14');
  } catch { return false; }
}

function to12Hour(time24: string): string {
  const [h, m] = time24.split(':').map(Number);
  const period = h >= 12 ? 'PM' : 'AM';
  const hour12 = h === 0 ? 12 : h > 12 ? h - 12 : h;
  return `${hour12}:${String(m).padStart(2, '0')} ${period}`;
}

function formatTime(time24: string, is12h: boolean): string {
  if (!is12h) return time24;
  return to12Hour(time24);
}

function getHighLatitudeParams(lat: number): { method?: number; latitudeAdjustmentMethod?: number } {
  const absLat = Math.abs(lat);
  if (absLat > 60) return { method: 3, latitudeAdjustmentMethod: 2 };
  if (absLat > 48) return { latitudeAdjustmentMethod: 1 };
  return {};
}

function getTodayStr() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

export function usePrayerTimes(
  latitude: number,
  longitude: number,
  method: number = 4,
  school: number = 0
): PrayerTimesData {
  const is12h = detectIs12Hour();
  const [data, setData] = useState<PrayerTimesData>({
    prayers: [], hijriDate: '', hijriDay: '', hijriMonthAr: '', hijriMonthEn: '',
    hijriMonthNumber: 0, hijriYear: '', hijriMonth: '', loading: true, error: null, isFromCache: false,
  });
  
  const lastFetchKey = useRef('');
  const [todayStr, setTodayStr] = useState(getTodayStr);

  // Midnight refresh
  useEffect(() => {
    const interval = setInterval(() => {
      const now = getTodayStr();
      setTodayStr(prev => {
        if (prev !== now) { lastFetchKey.current = ''; return now; }
        return prev;
      });
    }, 30_000);
    return () => clearInterval(interval);
  }, []);

  // Build prayer data from cached format
  const buildPrayerData = (cached: CachedPrayerTimes, fromCache: boolean): PrayerTimesData => {
    const isAr = i18n.language === 'ar';
    const suffix = isAr ? 'هـ' : 'H';
    const monthName = isAr ? cached.hijri.month_ar : cached.hijri.month_en;
    
    const prayerKeys = [
      { key: 'fajr', field: 'fajr' },
      { key: 'sunrise', field: 'sunrise' },
      { key: 'dhuhr', field: 'dhuhr' },
      { key: 'asr', field: 'asr' },
      { key: 'maghrib', field: 'maghrib' },
      { key: 'isha', field: 'isha' },
    ];

    const prayers: PrayerTime[] = prayerKeys
      .filter(p => cached.times[p.field])
      .map(p => ({
        name: p.key,
        time24: cached.times[p.field],
        time: formatTime(cached.times[p.field], is12h),
        key: p.key,
      }));

    return {
      prayers,
      hijriDate: `${cached.hijri.day} ${monthName} ${cached.hijri.year} ${suffix}`,
      hijriDay: cached.hijri.day,
      hijriMonthAr: cached.hijri.month_ar,
      hijriMonthEn: cached.hijri.month_en,
      hijriMonthNumber: cached.hijri.month_num,
      hijriYear: cached.hijri.year,
      hijriMonth: monthName,
      loading: false,
      error: null,
      isFromCache: fromCache,
    };
  };

  useEffect(() => {
    if (latitude === 0 && longitude === 0) return;

    const fetchKey = `${latitude}-${longitude}-${method}-${school}-${todayStr}`;
    if (fetchKey === lastFetchKey.current) return;
    lastFetchKey.current = fetchKey;

    const fetchPrayers = async () => {
      // Save location for offline use
      try {
        await saveLocation({ id: 'last_known', latitude, longitude, cached_at: Date.now() });
      } catch {}

      // Try network first
      if (navigator.onLine) {
        try {
          const today = new Date();
          const dd = String(today.getDate()).padStart(2, '0');
          const mm = String(today.getMonth() + 1).padStart(2, '0');
          const yyyy = today.getFullYear();

          const hlParams = getHighLatitudeParams(latitude);
          const effectiveMethod = hlParams.method || method;
          let apiUrl = `https://api.aladhan.com/v1/timings/${dd}-${mm}-${yyyy}?latitude=${latitude}&longitude=${longitude}&method=${effectiveMethod}&school=${school}&adjustment=0`;
          if (hlParams.latitudeAdjustmentMethod) {
            apiUrl += `&latitudeAdjustmentMethod=${hlParams.latitudeAdjustmentMethod}`;
          }

          const res = await fetch(apiUrl, { signal: AbortSignal.timeout(10000) });
          const json = await res.json();
          const timings = json.data.timings;
          const hijri = json.data.date.hijri;

          const cleanTime = (t: string) => t.replace(/\s*\(.*\)$/, '').trim();

          // Save to IndexedDB
          const cachedData: CachedPrayerTimes = {
            date: todayStr,
            locationKey: `${latitude.toFixed(2)}_${longitude.toFixed(2)}`,
            times: {
              fajr: cleanTime(timings.Fajr),
              sunrise: cleanTime(timings.Sunrise),
              dhuhr: cleanTime(timings.Dhuhr),
              asr: cleanTime(timings.Asr),
              maghrib: cleanTime(timings.Maghrib),
              isha: cleanTime(timings.Isha),
              midnight: cleanTime(timings.Midnight || ''),
            },
            hijri: {
              date: `${hijri.day} ${hijri.month.ar} ${hijri.year}`,
              day: hijri.day,
              month_ar: hijri.month.ar,
              month_en: hijri.month.en,
              month_num: hijri.month.number,
              year: hijri.year,
            },
            source: 'aladhan',
            cached_at: Date.now(),
          };

          try { await savePrayerTimes(cachedData); } catch {}

          setData(buildPrayerData(cachedData, false));
          return;
        } catch {
          // Network failed, try cache
        }
      }

      // Fallback: IndexedDB cache
      try {
        let cached = await getCachedPrayerTimes(todayStr);
        if (!cached) {
          cached = await getLatestPrayerTimes();
        }
        if (cached) {
          setData(buildPrayerData(cached, true));
          return;
        }
      } catch {}

      setData(prev => ({ ...prev, loading: false, error: 'تعذر تحميل مواقيت الصلاة - تحقق من الاتصال' }));
    };

    fetchPrayers();
  }, [latitude, longitude, method, school, is12h, todayStr]);

  return data;
}

export function getNextPrayer(prayers: PrayerTime[]): { prayer: PrayerTime | null; remaining: string } {
  const now = new Date();
  const currentMinutes = now.getHours() * 60 + now.getMinutes();

  for (const prayer of prayers) {
    if (prayer.key === 'sunrise') continue;
    const [h, m] = prayer.time24.split(':').map(Number);
    const prayerMinutes = h * 60 + m;
    if (prayerMinutes > currentMinutes) {
      const diff = prayerMinutes - currentMinutes;
      const hours = Math.floor(diff / 60);
      const mins = diff % 60;
      return { prayer, remaining: hours > 0 ? `${hours}h ${mins}m` : `${mins}m` };
    }
  }

  if (prayers.length > 0) {
    const fajr = prayers[0];
    const [h, m] = fajr.time24.split(':').map(Number);
    const fajrMinutes = h * 60 + m;
    const diff = (24 * 60 - currentMinutes) + fajrMinutes;
    const hours = Math.floor(diff / 60);
    const mins = diff % 60;
    return { prayer: fajr, remaining: `${hours}h ${mins}m` };
  }

  return { prayer: null, remaining: '' };
}
