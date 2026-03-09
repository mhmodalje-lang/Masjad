import { useState, useEffect, useRef } from 'react';
import { supabase } from '@/integrations/supabase/client';
import type { PrayerTime } from './usePrayerTimes';

const SAVED_MOSQUE_KEY = 'selected_mosque';
const SAVED_TIMES_PREFIX = 'mosque_times_';
const SAVED_DIFFS_PREFIX = 'mosque_diffs_';
const LIVE_CACHE_PREFIX = 'mosque_live_';

type TimesSource = 'manual' | 'mawaqit' | 'website' | 'api' | 'calculated' | 'none';

interface SavedMosqueData {
  mosqueName: string | null;
  prayers: PrayerTime[] | null;
  loading: boolean;
  source: TimesSource;
  unlinkMosque: () => void;
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

function applyTimeDiff(time: string, diffMinutes: number): string {
  if (!time || diffMinutes === 0) return time;
  const [h, m] = time.split(':').map(Number);
  const total = h * 60 + m + diffMinutes;
  const newH = Math.floor(((total % 1440) + 1440) % 1440 / 60);
  const newM = ((total % 60) + 60) % 60;
  return `${String(newH).padStart(2, '0')}:${String(newM).padStart(2, '0')}`;
}

function makePrayerTime(key: string, time24: string, is12h: boolean): PrayerTime {
  const fmt = (t: string) => (!t ? '' : is12h ? to12Hour(t) : t);
  return { name: key, time24, time: fmt(time24), key };
}

function applyDiffsToTimes(times: Record<string, string>, diffs: Record<string, number>): Record<string, string> {
  return {
    fajr: applyTimeDiff(times.fajr || '', diffs.fajr_diff || 0),
    sunrise: applyTimeDiff(times.sunrise || '', diffs.sunrise_diff || 0),
    dhuhr: applyTimeDiff(times.dhuhr || '', diffs.dhuhr_diff || 0),
    asr: applyTimeDiff(times.asr || '', diffs.asr_diff || 0),
    maghrib: applyTimeDiff(times.maghrib || '', diffs.maghrib_diff || 0),
    isha: applyTimeDiff(times.isha || '', diffs.isha_diff || 0),
  };
}

function timesMapToPrayers(times: Record<string, string>, is12h: boolean): PrayerTime[] {
  return [
    makePrayerTime('fajr', times.fajr || '', is12h),
    makePrayerTime('sunrise', times.sunrise || '', is12h),
    makePrayerTime('dhuhr', times.dhuhr || '', is12h),
    makePrayerTime('asr', times.asr || '', is12h),
    makePrayerTime('maghrib', times.maghrib || '', is12h),
    makePrayerTime('isha', times.isha || '', is12h),
  ];
}

function getTodayStr(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

function parseStoredTimes(raw: string): { times: Record<string, string> | null; date: string | null } {
  try {
    const parsed = JSON.parse(raw);
    if (parsed._date && parsed.times) return { times: parsed.times, date: parsed._date };
    if (parsed.fajr || parsed.dhuhr || parsed.asr || parsed.maghrib || parsed.isha) return { times: parsed, date: null };
    return { times: null, date: null };
  } catch { return { times: null, date: null }; }
}

function getCalcSettings(): { method: number; school: number; latitude?: number; longitude?: number } {
  try {
    const cached = localStorage.getItem('cached-location');
    if (cached) {
      const parsed = JSON.parse(cached);
      return {
        method: parsed.calculationMethod || 3,
        school: parsed.school ?? 0,
        latitude: parsed.latitude,
        longitude: parsed.longitude,
      };
    }
  } catch { /* ignore */ }
  return { method: 3, school: 0 };
}

// Clear stale caches from previous days
function clearStaleCaches(mosqueOsmId: string, todayKey: string) {
  for (let i = localStorage.length - 1; i >= 0; i--) {
    const key = localStorage.key(i);
    if (!key) continue;
    if (key.startsWith(LIVE_CACHE_PREFIX + mosqueOsmId) && !key.endsWith(todayKey)) {
      localStorage.removeItem(key);
    }
    if (key.startsWith('mosque_api_' + mosqueOsmId) && !key.includes(todayKey)) {
      localStorage.removeItem(key);
    }
  }
}

export function useSavedMosqueTimes(): SavedMosqueData {
  const [data, setData] = useState<Omit<SavedMosqueData, 'unlinkMosque'>>({
    mosqueName: null, prayers: null, loading: true, source: 'none'
  });
  const [todayStr, setTodayStr] = useState(getTodayStr);
  const lastFetchRef = useRef<number>(0);

  // Refresh check every 30s: midnight change OR hourly re-fetch
  useEffect(() => {
    const interval = setInterval(() => {
      const now = getTodayStr();
      if (now !== todayStr) {
        setTodayStr(now);
        return;
      }
      // Hourly refresh: force re-fetch if >60 min since last fetch
      if (Date.now() - lastFetchRef.current > 60 * 60 * 1000) {
        // Clear live cache to force re-fetch
        const saved = localStorage.getItem(SAVED_MOSQUE_KEY);
        if (saved) {
          try {
            const mosque = JSON.parse(saved);
            const dateKey = now.replace(/-/g, '');
            const liveCacheKey = LIVE_CACHE_PREFIX + mosque.osm_id + '_' + dateKey;
            localStorage.removeItem(liveCacheKey);
          } catch { /* ignore */ }
        }
        lastFetchRef.current = Date.now();
        setTodayStr(prev => prev + '_' + Date.now()); // force re-render
      }
    }, 30_000);
    return () => clearInterval(interval);
  }, [todayStr]);

  useEffect(() => {
    const is12h = detectIs12Hour();
    const calcSettings = getCalcSettings();

    const load = async () => {
      const saved = localStorage.getItem(SAVED_MOSQUE_KEY);
      if (!saved) {
        setData({ mosqueName: null, prayers: null, loading: false, source: 'none' });
        return;
      }

      let mosque: any;
      try { mosque = JSON.parse(saved); } catch {
        setData({ mosqueName: null, prayers: null, loading: false, source: 'none' });
        return;
      }

      const dateKey = todayStr.split('_')[0].replace(/-/g, '');

      // Clear stale caches from previous days
      clearStaleCaches(mosque.osm_id, dateKey);

      // 1. Check for manually saved times
      const timesStr = localStorage.getItem(SAVED_TIMES_PREFIX + mosque.osm_id);
      if (timesStr) {
        const { times } = parseStoredTimes(timesStr);
        if (times && (times.fajr || times.dhuhr || times.asr || times.maghrib || times.isha)) {
          setData({
            mosqueName: mosque.name,
            prayers: timesMapToPrayers(times, is12h),
            loading: false,
            source: 'manual',
          });
          return;
        }
      }

      // Load saved diffs
      const diffsStr = localStorage.getItem(SAVED_DIFFS_PREFIX + mosque.osm_id);
      let diffs: Record<string, number> = {};
      if (diffsStr) {
        try { diffs = JSON.parse(diffsStr); } catch { /* ignore */ }
      }

      // 2. Try live cache (valid for current hour window)
      const liveCacheKey = LIVE_CACHE_PREFIX + mosque.osm_id + '_' + dateKey;
      const liveCache = localStorage.getItem(liveCacheKey);

      if (liveCache) {
        try {
          const cached = JSON.parse(liveCache);
          if (cached.times) {
            setData({
              mosqueName: mosque.name,
              prayers: timesMapToPrayers(applyDiffsToTimes(cached.times, diffs), is12h),
              loading: false,
              source: (cached.source || 'calculated') as TimesSource,
            });
            lastFetchRef.current = Date.now();
            return;
          }
        } catch { /* fall through */ }
      }

      // 3. Fetch from edge function (accepts ALL sources including calculated)
      try {
        const { data: liveData, error } = await supabase.functions.invoke('fetch-mosque-times', {
          body: {
            mosqueName: mosque.name,
            mosqueCity: mosque.address?.split(',').pop()?.trim() || '',
            websiteUrl: mosque.websiteUrl || null,
            mawaqitSlug: mosque.mawaqitSlug || null,
            latitude: mosque.latitude || null,
            longitude: mosque.longitude || null,
            countryCode: mosque.countryCode || null,
            method: calcSettings.method,
            school: calcSettings.school,
          },
        });

        if (!error && liveData?.success && liveData?.times) {
          localStorage.setItem(liveCacheKey, JSON.stringify({
            times: liveData.times,
            source: liveData.source,
          }));

          setData({
            mosqueName: mosque.name,
            prayers: timesMapToPrayers(applyDiffsToTimes(liveData.times, diffs), is12h),
            loading: false,
            source: (liveData.source as TimesSource) || 'calculated',
          });
          lastFetchRef.current = Date.now();
          return;
        }
      } catch { /* fall through to direct Aladhan */ }

      // 4. Direct Aladhan fallback using USER's coordinates for consistency
      const fallbackLat = calcSettings.latitude || mosque.latitude;
      const fallbackLon = calcSettings.longitude || mosque.longitude;
      if (fallbackLat && fallbackLon) {
        try {
          const today = new Date();
          const dd = String(today.getDate()).padStart(2, '0');
          const mm = String(today.getMonth() + 1).padStart(2, '0');
          const yyyy = today.getFullYear();

          const res = await fetch(
            `https://api.aladhan.com/v1/timings/${dd}-${mm}-${yyyy}?latitude=${fallbackLat}&longitude=${fallbackLon}&method=${calcSettings.method}&school=${calcSettings.school}&adjustment=0`,
            { cache: 'no-store' }
          );
          const json = await res.json();
          const timings = json.data.timings;
          const clean = (s: string) => s.replace(/\s*\(.*\)$/, '').trim();
          const times = {
            fajr: clean(timings.Fajr),
            sunrise: clean(timings.Sunrise),
            dhuhr: clean(timings.Dhuhr),
            asr: clean(timings.Asr),
            maghrib: clean(timings.Maghrib),
            isha: clean(timings.Isha),
          };

          // Cache it
          localStorage.setItem(liveCacheKey, JSON.stringify({ times, source: 'calculated' }));

          setData({
            mosqueName: mosque.name,
            prayers: timesMapToPrayers(applyDiffsToTimes(times, diffs), is12h),
            loading: false,
            source: 'api',
          });
          lastFetchRef.current = Date.now();
          return;
        } catch { /* fall through */ }
      }

      setData({ mosqueName: mosque.name, prayers: null, loading: false, source: 'none' });
    };

    lastFetchRef.current = Date.now();
    load();
  }, [todayStr]);

  const unlinkMosque = () => {
    const saved = localStorage.getItem('selected_mosque');
    if (saved) {
      try {
        const mosque = JSON.parse(saved);
        if (mosque.osm_id) {
          localStorage.removeItem(SAVED_TIMES_PREFIX + mosque.osm_id);
          for (let i = localStorage.length - 1; i >= 0; i--) {
            const key = localStorage.key(i);
            if (key?.startsWith(LIVE_CACHE_PREFIX + mosque.osm_id)) {
              localStorage.removeItem(key);
            }
          }
        }
      } catch { /* ignore */ }
    }
    localStorage.removeItem('selected_mosque');
    setData({ mosqueName: null, prayers: null, loading: false, source: 'none' });
  };

  return { ...data, unlinkMosque };
}
