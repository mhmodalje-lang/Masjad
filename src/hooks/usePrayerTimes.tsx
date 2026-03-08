import { useState, useEffect } from 'react';

export interface PrayerTime {
  name: string;
  time: string;
  key: string;
}

interface PrayerTimesData {
  prayers: PrayerTime[];
  hijriDate: string;
  hijriMonth: string;
  hijriYear: string;
  loading: boolean;
  error: string | null;
}

export function usePrayerTimes(latitude: number, longitude: number, method: number = 2) {
  const [data, setData] = useState<PrayerTimesData>({
    prayers: [],
    hijriDate: '',
    hijriMonth: '',
    hijriYear: '',
    loading: true,
    error: null,
  });

  useEffect(() => {
    const fetchPrayers = async () => {
      try {
        const today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const yyyy = today.getFullYear();

        const res = await fetch(
          `https://api.aladhan.com/v1/timings/${dd}-${mm}-${yyyy}?latitude=${latitude}&longitude=${longitude}&method=${method}`
        );
        const json = await res.json();
        const timings = json.data.timings;
        const hijri = json.data.date.hijri;

        const prayers: PrayerTime[] = [
          { name: 'fajr', time: timings.Fajr, key: 'fajr' },
          { name: 'sunrise', time: timings.Sunrise, key: 'sunrise' },
          { name: 'dhuhr', time: timings.Dhuhr, key: 'dhuhr' },
          { name: 'asr', time: timings.Asr, key: 'asr' },
          { name: 'maghrib', time: timings.Maghrib, key: 'maghrib' },
          { name: 'isha', time: timings.Isha, key: 'isha' },
        ];

        setData({
          prayers,
          hijriDate: `${hijri.day} ${hijri.month.en} ${hijri.year}`,
          hijriMonth: hijri.month.ar,
          hijriYear: hijri.year,
          loading: false,
          error: null,
        });
      } catch {
        setData(prev => ({ ...prev, loading: false, error: 'Failed to fetch prayer times' }));
      }
    };

    fetchPrayers();
  }, [latitude, longitude, method]);

  return data;
}

export function getNextPrayer(prayers: PrayerTime[]): { prayer: PrayerTime | null; remaining: string } {
  const now = new Date();
  const currentMinutes = now.getHours() * 60 + now.getMinutes();

  for (const prayer of prayers) {
    if (prayer.key === 'sunrise') continue;
    const [h, m] = prayer.time.split(':').map(Number);
    const prayerMinutes = h * 60 + m;
    if (prayerMinutes > currentMinutes) {
      const diff = prayerMinutes - currentMinutes;
      const hours = Math.floor(diff / 60);
      const mins = diff % 60;
      return {
        prayer,
        remaining: hours > 0 ? `${hours}h ${mins}m` : `${mins}m`,
      };
    }
  }

  // After Isha, next is Fajr tomorrow
  if (prayers.length > 0) {
    const fajr = prayers[0];
    const [h, m] = fajr.time.split(':').map(Number);
    const fajrMinutes = h * 60 + m;
    const diff = (24 * 60 - currentMinutes) + fajrMinutes;
    const hours = Math.floor(diff / 60);
    const mins = diff % 60;
    return { prayer: fajr, remaining: `${hours}h ${mins}m` };
  }

  return { prayer: null, remaining: '' };
}
