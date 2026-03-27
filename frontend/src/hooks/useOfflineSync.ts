/**
 * useOfflineSync - Auto-saves fetched data to IndexedDB for offline access
 * Call this at app level to pre-cache all essential data
 */
import { useEffect, useRef } from 'react';
import {
  saveQuranChapters,
  saveRuqyah,
  saveStories,
  saveDailyContent,
  getOfflineDataSummary,
  processSyncQueue,
} from '@/lib/offlineStorage';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

export function useOfflineSync() {
  const syncedRef = useRef(false);

  useEffect(() => {
    if (syncedRef.current) return;
    syncedRef.current = true;

    const syncData = async () => {
      if (!navigator.onLine) {
        console.log('[OfflineSync] Offline - skipping sync');
        return;
      }

      console.log('[OfflineSync] Starting background sync...');

      // 1. Quran chapters
      try {
        const res = await fetch(`${BACKEND_URL}/api/quran/v4/chapters?language=ar`, { signal: AbortSignal.timeout(10000) });
        if (res.ok) {
          const data = await res.json();
          if (data.chapters?.length) {
            await saveQuranChapters(data.chapters);
            console.log(`[OfflineSync] Cached ${data.chapters.length} surahs`);
          }
        }
      } catch {}

      // 2. Ruqyah
      try {
        const res = await fetch(`${BACKEND_URL}/api/ruqyah`, { signal: AbortSignal.timeout(10000) });
        if (res.ok) {
          const data = await res.json();
          if (data.items?.length) {
            await saveRuqyah(data.items);
            console.log(`[OfflineSync] Cached ${data.items.length} ruqyah items`);
          }
        }
      } catch {}

      // 3. Stories (first page)
      try {
        const res = await fetch(`${BACKEND_URL}/api/stories/list?page=1&per_page=50`, { signal: AbortSignal.timeout(10000) });
        if (res.ok) {
          const data = await res.json();
          if (data.stories?.length) {
            await saveStories(data.stories);
            console.log(`[OfflineSync] Cached ${data.stories.length} stories`);
          }
        }
      } catch {}

      // 4. Daily content
      try {
        const [hadithRes, verseRes] = await Promise.allSettled([
          fetch(`${BACKEND_URL}/api/daily-hadith?language=ar`, { signal: AbortSignal.timeout(8000) }),
          fetch(`${BACKEND_URL}/api/ai/verse-of-day`, { signal: AbortSignal.timeout(8000) }),
        ]);

        if (hadithRes.status === 'fulfilled' && hadithRes.value.ok) {
          const data = await hadithRes.value.json();
          await saveDailyContent({ type: 'hadith', data, date: new Date().toISOString().split('T')[0], cached_at: Date.now() });
        }
        if (verseRes.status === 'fulfilled' && verseRes.value.ok) {
          const data = await verseRes.value.json();
          await saveDailyContent({ type: 'verse', data, date: new Date().toISOString().split('T')[0], cached_at: Date.now() });
        }
      } catch {}

      // 5. Process sync queue
      try { await processSyncQueue(); } catch {}

      // Log summary
      try {
        const summary = await getOfflineDataSummary();
        console.log('[OfflineSync] Offline data summary:', summary);
      } catch {}
    };

    // Delay sync to not block app load
    const timer = setTimeout(syncData, 3000);

    // Re-sync when coming back online
    const onOnline = () => {
      console.log('[OfflineSync] Back online - syncing...');
      syncData();
    };
    window.addEventListener('online', onOnline);

    return () => {
      clearTimeout(timer);
      window.removeEventListener('online', onOnline);
    };
  }, []);
}
