import { useState, useEffect } from 'react';

interface LocationData {
  latitude: number;
  longitude: number;
  city: string;
  country: string;
  loading: boolean;
  error: string | null;
}

export function useLocation() {
  const [location, setLocation] = useState<LocationData>({
    latitude: 21.4225, // Makkah default
    longitude: 39.8262,
    city: 'Makkah',
    country: 'Saudi Arabia',
    loading: true,
    error: null,
  });

  const detectLocation = () => {
    setLocation(prev => ({ ...prev, loading: true, error: null }));

    if (!navigator.geolocation) {
      setLocation(prev => ({ ...prev, loading: false, error: 'Geolocation not supported' }));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        try {
          const res = await fetch(
            `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`
          );
          const data = await res.json();
          setLocation({
            latitude,
            longitude,
            city: data.city || data.locality || 'Unknown',
            country: data.countryName || 'Unknown',
            loading: false,
            error: null,
          });
        } catch {
          setLocation({
            latitude,
            longitude,
            city: 'Unknown',
            country: 'Unknown',
            loading: false,
            error: null,
          });
        }
      },
      () => {
        setLocation(prev => ({ ...prev, loading: false }));
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  useEffect(() => {
    detectLocation();
  }, []);

  return { ...location, detectLocation };
}
