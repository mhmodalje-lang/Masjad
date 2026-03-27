/**
 * useOfflineData - Fetches from API with IndexedDB caching
 * Network-first: tries API, falls back to cached data
 */
import { useState, useEffect, useCallback, useRef } from 'react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface UseOfflineDataOptions<T> {
  /** API endpoint path (e.g., '/api/ruqyah') */
  apiPath: string;
  /** IndexedDB cache key */
  cacheKey: string;
  /** Function to save data to IndexedDB */
  saveToCache: (data: T) => Promise<void>;
  /** Function to load data from IndexedDB */
  loadFromCache: () => Promise<T | undefined>;
  /** Transform API response before caching */
  transform?: (response: any) => T;
  /** Whether to auto-fetch on mount */
  autoFetch?: boolean;
  /** Custom headers */
  headers?: Record<string, string>;
  /** Skip fetch condition */
  skip?: boolean;
}

interface UseOfflineDataResult<T> {
  data: T | undefined;
  loading: boolean;
  error: string | null;
  isFromCache: boolean;
  isOffline: boolean;
  refetch: () => Promise<void>;
}

export function useOfflineData<T>(options: UseOfflineDataOptions<T>): UseOfflineDataResult<T> {
  const { apiPath, saveToCache, loadFromCache, transform, autoFetch = true, headers, skip = false } = options;
  const [data, setData] = useState<T | undefined>(undefined);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isFromCache, setIsFromCache] = useState(false);
  const [isOffline, setIsOffline] = useState(!navigator.onLine);
  const fetchedRef = useRef(false);

  useEffect(() => {
    const onOnline = () => setIsOffline(false);
    const onOffline = () => setIsOffline(true);
    window.addEventListener('online', onOnline);
    window.addEventListener('offline', onOffline);
    return () => {
      window.removeEventListener('online', onOnline);
      window.removeEventListener('offline', onOffline);
    };
  }, []);

  const fetchData = useCallback(async () => {
    if (skip) return;
    setLoading(true);
    setError(null);

    // Strategy: Network-first with cache fallback
    if (navigator.onLine) {
      try {
        const res = await fetch(`${BACKEND_URL}${apiPath}`, {
          headers: { 'Content-Type': 'application/json', ...headers },
          signal: AbortSignal.timeout(12000),
        });
        if (res.ok) {
          const json = await res.json();
          const transformed = transform ? transform(json) : json as T;
          setData(transformed);
          setIsFromCache(false);
          // Save to cache in background
          try { await saveToCache(transformed); } catch {}
          setLoading(false);
          return;
        }
      } catch {
        // Network failed, fall through to cache
      }
    }

    // Fallback: load from IndexedDB
    try {
      const cached = await loadFromCache();
      if (cached !== undefined) {
        setData(cached);
        setIsFromCache(true);
        setError(null);
      } else {
        setError('لا توجد بيانات محفوظة - اتصل بالإنترنت أولاً');
      }
    } catch {
      setError('فشل في قراءة البيانات المحفوظة');
    }

    setLoading(false);
  }, [apiPath, saveToCache, loadFromCache, transform, headers, skip]);

  useEffect(() => {
    if (autoFetch && !fetchedRef.current) {
      fetchedRef.current = true;
      fetchData();
    }
  }, [autoFetch, fetchData]);

  // Re-fetch when coming back online
  useEffect(() => {
    if (!isOffline && fetchedRef.current && isFromCache) {
      fetchData();
    }
  }, [isOffline]);

  return { data, loading, error, isFromCache, isOffline, refetch: fetchData };
}
