/**
 * ═══════════════════════════════════════════════════════
 * 🗄️ Offline Storage - IndexedDB Layer
 * ═══════════════════════════════════════════════════════
 * Stores all app data locally for offline access:
 * - Prayer times
 * - Quran chapters & verses
 * - Ruqyah items
 * - Stories
 * - Settings & preferences
 * - Daily content (hadith, verse, dua)
 * - User location
 */

const DB_NAME = 'azanhikaya_offline';
const DB_VERSION = 5;

type StoreName = 
  | 'prayer_times'
  | 'quran_chapters'
  | 'quran_verses'
  | 'ruqyah'
  | 'stories'
  | 'settings'
  | 'daily_content'
  | 'user_location'
  | 'sync_queue'
  | 'cached_pages';

let dbInstance: IDBDatabase | null = null;

function openDB(): Promise<IDBDatabase> {
  if (dbInstance) return Promise.resolve(dbInstance);
  
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    
    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      
      const stores: { name: StoreName; keyPath: string; indexes?: { name: string; keyPath: string; unique?: boolean }[] }[] = [
        { name: 'prayer_times', keyPath: 'date', indexes: [{ name: 'location', keyPath: 'locationKey' }] },
        { name: 'quran_chapters', keyPath: 'number' },
        { name: 'quran_verses', keyPath: 'key', indexes: [{ name: 'chapter', keyPath: 'chapter_number' }] },
        { name: 'ruqyah', keyPath: 'id' },
        { name: 'stories', keyPath: 'id', indexes: [{ name: 'category', keyPath: 'category' }] },
        { name: 'settings', keyPath: 'key' },
        { name: 'daily_content', keyPath: 'type' },
        { name: 'user_location', keyPath: 'id' },
        { name: 'sync_queue', keyPath: 'id' },
        { name: 'cached_pages', keyPath: 'url' },
      ];
      
      for (const store of stores) {
        if (!db.objectStoreNames.contains(store.name)) {
          const os = db.createObjectStore(store.name, { keyPath: store.keyPath });
          if (store.indexes) {
            for (const idx of store.indexes) {
              os.createIndex(idx.name, idx.keyPath, { unique: idx.unique ?? false });
            }
          }
        }
      }
    };
    
    request.onsuccess = () => {
      dbInstance = request.result;
      resolve(dbInstance);
    };
    
    request.onerror = () => reject(request.error);
  });
}

// ─── Generic CRUD ───

async function put<T>(storeName: StoreName, data: T): Promise<void> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readwrite');
    tx.objectStore(storeName).put(data);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function putMany<T>(storeName: StoreName, items: T[]): Promise<void> {
  if (!items.length) return;
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readwrite');
    const store = tx.objectStore(storeName);
    for (const item of items) store.put(item);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function get<T>(storeName: StoreName, key: IDBValidKey): Promise<T | undefined> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readonly');
    const req = tx.objectStore(storeName).get(key);
    req.onsuccess = () => resolve(req.result as T | undefined);
    req.onerror = () => reject(req.error);
  });
}

async function getAll<T>(storeName: StoreName): Promise<T[]> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readonly');
    const req = tx.objectStore(storeName).getAll();
    req.onsuccess = () => resolve(req.result as T[]);
    req.onerror = () => reject(req.error);
  });
}

async function getByIndex<T>(storeName: StoreName, indexName: string, value: IDBValidKey): Promise<T[]> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readonly');
    const idx = tx.objectStore(storeName).index(indexName);
    const req = idx.getAll(value);
    req.onsuccess = () => resolve(req.result as T[]);
    req.onerror = () => reject(req.error);
  });
}

async function clear(storeName: StoreName): Promise<void> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readwrite');
    tx.objectStore(storeName).clear();
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

// ─── Prayer Times ───

export interface CachedPrayerTimes {
  date: string;       // YYYY-MM-DD
  locationKey: string; // lat_lon
  times: Record<string, string>;
  hijri: {
    date: string;
    day: string;
    month_ar: string;
    month_en: string;
    month_num: number;
    year: string;
  };
  source: string;
  cached_at: number;
}

export async function savePrayerTimes(data: CachedPrayerTimes): Promise<void> {
  await put('prayer_times', data);
}

export async function getPrayerTimes(date: string): Promise<CachedPrayerTimes | undefined> {
  return get('prayer_times', date);
}

export async function getLatestPrayerTimes(): Promise<CachedPrayerTimes | undefined> {
  const all = await getAll<CachedPrayerTimes>('prayer_times');
  if (!all.length) return undefined;
  return all.sort((a, b) => b.cached_at - a.cached_at)[0];
}

// ─── Quran ───

export interface CachedSurah {
  number: number;
  name_arabic: string;
  name_en: string;
  revelation_type: string;
  verses_count: number;
}

export async function saveQuranChapters(chapters: CachedSurah[]): Promise<void> {
  await putMany('quran_chapters', chapters);
}

export async function getQuranChapters(): Promise<CachedSurah[]> {
  return getAll('quran_chapters');
}

export interface CachedVerse {
  key: string;        // chapter_verse
  chapter_number: number;
  verse_number: number;
  text_uthmani: string;
  translation?: string;
}

export async function saveQuranVerses(verses: CachedVerse[]): Promise<void> {
  await putMany('quran_verses', verses);
}

export async function getQuranVersesByChapter(chapter: number): Promise<CachedVerse[]> {
  return getByIndex('quran_verses', 'chapter', chapter);
}

// ─── Ruqyah ───

export async function saveRuqyah(items: any[]): Promise<void> {
  await putMany('ruqyah', items);
}

export async function getRuqyah(): Promise<any[]> {
  return getAll('ruqyah');
}

// ─── Stories ───

export async function saveStories(stories: any[]): Promise<void> {
  await putMany('stories', stories);
}

export async function getStories(category?: string): Promise<any[]> {
  if (category && category !== 'all') {
    return getByIndex('stories', 'category', category);
  }
  return getAll('stories');
}

// ─── Daily Content ───

export interface CachedDailyContent {
  type: string;       // 'hadith' | 'verse' | 'dua'
  data: any;
  date: string;
  cached_at: number;
}

export async function saveDailyContent(content: CachedDailyContent): Promise<void> {
  await put('daily_content', content);
}

export async function getDailyContent(type: string): Promise<CachedDailyContent | undefined> {
  return get('daily_content', type);
}

// ─── User Location ───

export interface CachedLocation {
  id: string;          // 'last_known'
  latitude: number;
  longitude: number;
  city?: string;
  country?: string;
  cached_at: number;
}

export async function saveLocation(loc: CachedLocation): Promise<void> {
  await put('user_location', loc);
}

export async function getLastLocation(): Promise<CachedLocation | undefined> {
  return get('user_location', 'last_known');
}

// ─── Settings ───

export async function saveSetting(key: string, value: any): Promise<void> {
  await put('settings', { key, value, updated_at: Date.now() });
}

export async function getSetting(key: string): Promise<any> {
  const item = await get<{ key: string; value: any }>('settings', key);
  return item?.value;
}

// ─── Background Sync Queue ───

export interface SyncItem {
  id: string;
  url: string;
  method: string;
  body?: any;
  headers?: Record<string, string>;
  created_at: number;
}

export async function addToSyncQueue(item: SyncItem): Promise<void> {
  await put('sync_queue', item);
}

export async function getSyncQueue(): Promise<SyncItem[]> {
  return getAll('sync_queue');
}

export async function clearSyncQueue(): Promise<void> {
  await clear('sync_queue');
}

export async function removeSyncItem(id: string): Promise<void> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('sync_queue', 'readwrite');
    tx.objectStore('sync_queue').delete(id);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

// ─── Process Sync Queue (called when online) ───

export async function processSyncQueue(): Promise<void> {
  const items = await getSyncQueue();
  for (const item of items) {
    try {
      await fetch(item.url, {
        method: item.method,
        headers: item.headers,
        body: item.body ? JSON.stringify(item.body) : undefined,
      });
      await removeSyncItem(item.id);
    } catch {
      // Will retry next time
    }
  }
}

// ─── Utility ───

export async function getOfflineDataSummary(): Promise<Record<string, number>> {
  const [prayers, chapters, ruqyah, stories, daily] = await Promise.all([
    getAll('prayer_times'),
    getAll('quran_chapters'),
    getAll('ruqyah'),
    getAll('stories'),
    getAll('daily_content'),
  ]);
  return {
    prayer_times: prayers.length,
    quran_chapters: chapters.length,
    ruqyah: ruqyah.length,
    stories: stories.length,
    daily_content: daily.length,
  };
}

export { openDB };
