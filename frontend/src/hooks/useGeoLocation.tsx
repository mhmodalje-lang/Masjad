import { useState, useEffect, useRef } from 'react';
import i18n from '@/lib/i18nConfig';
import { saveLocation, getLastLocation } from '@/lib/offlineStorage';

interface LocationData {
  latitude: number;
  longitude: number;
  city: string;
  country: string;
  countryCode: string;
  calculationMethod: number;
  school: number; // 0 = Shafi/Maliki/Hanbali, 1 = Hanafi
  loading: boolean;
  error: string | null;
}

/** Keep 6 decimal places for ~0.11 m precision */
function roundCoord(val: number): number {
  return Math.round(val * 1_000_000) / 1_000_000;
}

/**
 * Aladhan calculation-method mapping identical to IslamicFinder / Athan app.
 * 1 = Karachi, 2 = ISNA, 3 = MWL, 4 = Umm Al-Qura, 5 = Egyptian
 */
function getCalculationMethodByCountry(countryCode: string): number {
  const code = countryCode?.toUpperCase();

  // Gulf / Arabian Peninsula → Umm Al-Qura (4)
  if (['SA', 'AE', 'QA', 'KW', 'BH', 'OM', 'YE'].includes(code)) return 4;

  // North Africa → Egyptian General Authority (5)
  if (['EG', 'LY', 'SD', 'SO', 'DJ', 'ER'].includes(code)) return 5;

  // Maghreb → MWL (3) – widely accepted
  if (['DZ', 'MA', 'TN', 'MR'].includes(code)) return 3;

  // South & Central Asia → Karachi (1)
  if (['PK', 'IN', 'BD', 'AF', 'LK', 'NP', 'MM', 'UZ', 'TJ', 'KG', 'TM', 'KZ'].includes(code)) return 1;

  // Southeast Asia → MWL (3) – most common
  if (['MY', 'ID', 'BN', 'SG', 'PH', 'TH'].includes(code)) return 3;

  // Turkey → Diyanet (13)
  if (code === 'TR') return 13;

  // Iran → Institute of Geophysics, Tehran (7)
  if (code === 'IR') return 7;

  // Iraq, Syria, Jordan, Palestine, Lebanon → MWL (3)
  if (['IQ', 'SY', 'JO', 'PS', 'LB'].includes(code)) return 3;

  // Europe → MWL (3)
  if (['DE', 'FR', 'GB', 'NL', 'BE', 'SE', 'NO', 'DK', 'ES', 'IT', 'CH', 'AT',
       'FI', 'IE', 'PT', 'GR', 'PL', 'CZ', 'HU', 'RO', 'BG', 'HR', 'RS', 'BA',
       'AL', 'MK', 'XK', 'ME', 'SI', 'SK', 'LT', 'LV', 'EE', 'IS', 'LU', 'MT',
       'CY', 'UA', 'BY', 'MD', 'RU'].includes(code)) return 3;

  // North America → ISNA (2)
  if (['US', 'CA', 'MX'].includes(code)) return 2;

  // Australia & NZ → MWL (3)
  if (['AU', 'NZ'].includes(code)) return 3;

  // Sub-Saharan Africa → Egyptian (5)
  if (['NG', 'ET', 'KE', 'TZ', 'UG', 'GH', 'SN', 'ML', 'NE', 'TD', 'CM', 'CI'].includes(code)) return 5;

  // Default → MWL
  return 3;
}

/**
 * Auto-detect Asr juristic school:
 * 0 = Standard (Shafi'i/Maliki/Hanbali), 1 = Hanafi
 */
export function getSchoolByCountry(countryCode: string): number {
  const code = countryCode?.toUpperCase();
  // Hanafi-majority regions
  if (['TR', 'PK', 'AF', 'BD', 'IN', 'UZ', 'TJ', 'KG', 'TM', 'KZ', 'IQ', 'SY',
       'JO', 'PS', 'LB', 'BA', 'AL', 'XK', 'MK'].includes(code)) return 1;
  return 0;
}

export function useGeoLocation() {
  const [location, setLocation] = useState<LocationData>(() => {
    try {
      const cached = localStorage.getItem('cached-location');
      if (cached) {
        const parsed = JSON.parse(cached);
        const cc = parsed.countryCode || '';
        return {
          ...parsed,
          countryCode: cc,
          calculationMethod: parsed.calculationMethod || getCalculationMethodByCountry(cc),
          school: parsed.school ?? getSchoolByCountry(cc),
          loading: true,
          error: null,
        };
      }
    } catch {}

    return {
      latitude: 21.4225,
      longitude: 39.8262,
      city: 'مكة المكرمة',
      country: 'السعودية',
      countryCode: 'SA',
      calculationMethod: 4,
      school: 0,
      loading: true,
      error: null,
    };
  });

  const hasDetected = useRef(false);

  // Also save to IndexedDB for offline access
  const saveToIndexedDB = async (lat: number, lon: number, city?: string, country?: string) => {
    try {
      await saveLocation({ id: 'last_known', latitude: lat, longitude: lon, city, country, cached_at: Date.now() });
    } catch {}
  };

  const detectLocation = () => {
    if (!navigator.geolocation) {
      // Try IndexedDB for offline fallback
      getLastLocation().then(cached => {
        if (cached) {
          setLocation(prev => ({
            ...prev,
            latitude: cached.latitude,
            longitude: cached.longitude,
            city: cached.city || prev.city,
            country: cached.country || prev.country,
            loading: false,
            error: null,
          }));
        } else {
          // Fallback to Mecca
          setLocation({
            latitude: 21.4225,
            longitude: 39.8262,
            city: 'مكة المكرمة',
            country: 'السعودية',
            countryCode: 'SA',
            calculationMethod: 4,
            school: 0,
            loading: false,
            error: null,
          });
        }
      }).catch(() => {
        setLocation({
          latitude: 21.4225,
          longitude: 39.8262,
          city: 'مكة المكرمة',
          country: 'السعودية',
          countryCode: 'SA',
          calculationMethod: 4,
          school: 0,
          loading: false,
          error: null,
        });
      });
      return;
    }

    setLocation(prev => ({ ...prev, loading: true, error: null }));

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const latitude = roundCoord(position.coords.latitude);
        const longitude = roundCoord(position.coords.longitude);

        try {
          const res = await fetch(
            `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=${i18n.language || 'en'}`
          );
          const data = await res.json();
          const countryCode = data.countryCode || '';
          const calculationMethod = getCalculationMethodByCountry(countryCode);
          const school = getSchoolByCountry(countryCode);

          const loc: LocationData = {
            latitude,
            longitude,
            city: data.city || data.locality || '',
            country: data.countryName || '',
            countryCode,
            calculationMethod,
            school,
            loading: false,
            error: null,
          };

          setLocation(loc);

          // Save to localStorage
          try {
            localStorage.setItem('cached-location', JSON.stringify({
              latitude: loc.latitude,
              longitude: loc.longitude,
              city: loc.city,
              country: loc.country,
              countryCode: loc.countryCode,
              calculationMethod: loc.calculationMethod,
              school: loc.school,
            }));
          } catch {}

          // Save to IndexedDB for offline
          saveToIndexedDB(loc.latitude, loc.longitude, loc.city, loc.country);
        } catch {
          setLocation(prev => ({
            ...prev,
            latitude,
            longitude,
            loading: false,
            error: null,
          }));
        }
      },
      () => {
        // If user denies location, use Mecca as default fallback
        setLocation(prev => {
          if (prev.latitude !== 0 || prev.longitude !== 0) {
            // Use cached location
            return { ...prev, loading: false, error: null };
          }
          // Fallback to Mecca
          const meccaLocation: LocationData = {
            latitude: 21.4225,
            longitude: 39.8262,
            city: 'مكة المكرمة',
            country: 'السعودية',
            countryCode: 'SA',
            calculationMethod: 4,
            school: 0,
            loading: false,
            error: null,
          };
          try {
            localStorage.setItem('cached-location', JSON.stringify({
              latitude: meccaLocation.latitude,
              longitude: meccaLocation.longitude,
              city: meccaLocation.city,
              country: meccaLocation.country,
              countryCode: meccaLocation.countryCode,
              calculationMethod: meccaLocation.calculationMethod,
              school: meccaLocation.school,
            }));
          } catch {}
          return meccaLocation;
        });
      },
      { enableHighAccuracy: false, timeout: 8000, maximumAge: 600000 }
    );
  };

  useEffect(() => {
    if (!hasDetected.current) {
      hasDetected.current = true;
      detectLocation();
    }
  }, []);

  return { ...location, detectLocation };
}
