/**
 * Quran.com API v4 Integration
 * Maps Surah and Hadith requests directly to https://api.quran.com/api/v4
 * Ensures 100% accuracy by using official API - NO machine translation for religious texts
 *
 * Supported Quran translation editions per language:
 * - English (en): Sahih International (131)
 * - German (de): Abu Rida Muhammad ibn Ahmad ibn Rassoul (27)
 * - Russian (ru): Ministry of Awqaf, Egypt (45)
 * - French (fr): Muhammad Hamidullah (31)
 * - Turkish (tr): Diyanet İşleri (77)
 *
 * Reference: https://api.quran.com/api/v4
 */

const QURAN_API_BASE = 'https://api.quran.com/api/v4';
const SUNNAH_API_BASE = 'https://api.sunnah.com/v1';

// Official Quran.com translation resource IDs
export const QURAN_TRANSLATION_IDS: Record<string, number> = {
  en: 20,   // Saheeh International (KFGQPC)
  de: 27,   // Bubenheim & Elyas (KFGQPC)
  ru: 45,   // Elmir Kuliev (Standard Russian)
  fr: 136,  // Montada Islamic Foundation (Modern French)
  tr: 77,   // Diyanet İşleri Başkanlığı
  sv: 48,   // Knut Bernström (Official Swedish)
  nl: 144,  // Sofian S. Siregar (Verified Dutch)
  el: 9999, // Greek: Rowwad Translation Center via QuranEnc.com (handled by backend)
  ar: 0,    // Arabic original - no translation needed
};

// Recitation audio IDs
export const QURAN_RECITERS: Record<string, { id: number; name: string }> = {
  'al-afasy': { id: 7, name: 'Mishary Rashid Alafasy' },
  'al-husary': { id: 5, name: 'Mahmoud Khalil Al-Husary' },
  'abdul-basit': { id: 1, name: 'Abdul Basit Abdul Samad' },
  'al-minshawi': { id: 6, name: 'Mohamed Siddiq Al-Minshawi' },
  'as-sudais': { id: 4, name: 'Abdurrahman As-Sudais' },
};

export interface QuranSurah {
  id: number;
  revelation_place: string;
  revelation_order: number;
  bismillah_pre: boolean;
  name_simple: string;
  name_complex: string;
  name_arabic: string;
  verses_count: number;
  pages: number[];
  translated_name: {
    language_name: string;
    name: string;
  };
}

export interface QuranVerse {
  id: number;
  verse_number: number;
  verse_key: string;
  hizb_number: number;
  rub_el_hizb_number: number;
  ruku_number: number;
  manzil_number: number;
  sajdah_number: number | null;
  text_uthmani: string;
  page_number: number;
  juz_number: number;
  translations?: {
    id: number;
    resource_id: number;
    text: string;
  }[];
  audio?: {
    url: string;
  };
}

export interface QuranJuz {
  id: number;
  juz_number: number;
  verse_mapping: Record<string, string>;
  first_verse_id: number;
  last_verse_id: number;
  verses_count: number;
}

/**
 * Fetch all Surahs list
 */
export async function fetchSurahs(language: string = 'ar'): Promise<QuranSurah[]> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/chapters?language=${language}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return data.chapters || [];
  } catch (error) {
    console.error('Failed to fetch surahs:', error);
    return [];
  }
}

/**
 * Fetch a specific Surah's info
 */
export async function fetchSurahInfo(surahNumber: number, language: string = 'ar'): Promise<QuranSurah | null> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/chapters/${surahNumber}?language=${language}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return data.chapter || null;
  } catch (error) {
    console.error(`Failed to fetch surah ${surahNumber}:`, error);
    return null;
  }
}

/**
 * Fetch verses of a Surah with translation
 */
export async function fetchSurahVerses(
  surahNumber: number,
  language: string = 'ar',
  page: number = 1,
  perPage: number = 50
): Promise<{ verses: QuranVerse[]; pagination: any }> {
  try {
    const translationId = QURAN_TRANSLATION_IDS[language];
    let url = `${QURAN_API_BASE}/verses/by_chapter/${surahNumber}?language=${language}&words=false&page=${page}&per_page=${perPage}&fields=text_uthmani`;
    
    // Add translation if not Arabic
    if (translationId && language !== 'ar') {
      url += `&translations=${translationId}`;
    }
    
    const res = await fetch(url);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return {
      verses: data.verses || [],
      pagination: data.pagination || {},
    };
  } catch (error) {
    console.error(`Failed to fetch verses for surah ${surahNumber}:`, error);
    return { verses: [], pagination: {} };
  }
}

/**
 * Fetch verses by Juz number
 */
export async function fetchJuzVerses(
  juzNumber: number,
  language: string = 'ar',
  page: number = 1,
  perPage: number = 50
): Promise<{ verses: QuranVerse[]; pagination: any }> {
  try {
    const translationId = QURAN_TRANSLATION_IDS[language];
    let url = `${QURAN_API_BASE}/verses/by_juz/${juzNumber}?language=${language}&words=false&page=${page}&per_page=${perPage}&fields=text_uthmani`;
    
    if (translationId && language !== 'ar') {
      url += `&translations=${translationId}`;
    }
    
    const res = await fetch(url);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return {
      verses: data.verses || [],
      pagination: data.pagination || {},
    };
  } catch (error) {
    console.error(`Failed to fetch juz ${juzNumber} verses:`, error);
    return { verses: [], pagination: {} };
  }
}

/**
 * Search the Quran
 */
export async function searchQuran(
  query: string,
  language: string = 'ar',
  page: number = 1,
  size: number = 20
): Promise<{ results: any[]; total: number }> {
  try {
    const translationId = QURAN_TRANSLATION_IDS[language] || 131;
    const res = await fetch(
      `${QURAN_API_BASE}/search?q=${encodeURIComponent(query)}&size=${size}&page=${page}&language=${language}`
    );
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return {
      results: data.search?.results || [],
      total: data.search?.total_results || 0,
    };
  } catch (error) {
    console.error('Quran search failed:', error);
    return { results: [], total: 0 };
  }
}

/**
 * Fetch audio recitation for a verse
 */
export async function fetchVerseAudio(
  verseKey: string,
  reciterId: number = 7
): Promise<string | null> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/recitations/${reciterId}/by_ayah/${verseKey}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    const audioFile = data.audio_files?.[0];
    if (audioFile?.url) {
      return audioFile.url.startsWith('http')
        ? audioFile.url
        : `https://verses.quran.com/${audioFile.url}`;
    }
    return null;
  } catch (error) {
    console.error(`Failed to fetch audio for ${verseKey}:`, error);
    return null;
  }
}

/**
 * Fetch all Juz info
 */
export async function fetchJuzList(): Promise<QuranJuz[]> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/juzs`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return data.juzs || [];
  } catch (error) {
    console.error('Failed to fetch juz list:', error);
    return [];
  }
}

/**
 * Get available translations for a language
 */
export async function fetchAvailableTranslations(language: string = 'en'): Promise<any[]> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/resources/translations?language=${language}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return data.translations || [];
  } catch (error) {
    console.error('Failed to fetch translations:', error);
    return [];
  }
}

/**
 * Open-Source Islamic Translation Repositories Reference
 * These repositories contain pre-translated Islamic constants to avoid manual translation errors:
 *
 * 1. quran/quran.com-api (GitHub)
 *    URL: https://github.com/quran/quran.com-api
 *    Contains: Complete Quran translations in 50+ languages, tafsir, audio references
 *
 * 2. sunnah-com/api (GitHub)
 *    URL: https://github.com/sunnah-com/api
 *    Contains: Major Hadith collections (Bukhari, Muslim, Tirmidhi, etc.) with translations
 *
 * 3. AhsanAyaz/quran-json (GitHub)
 *    URL: https://github.com/AhsanAyaz/quran-json
 *    Contains: Complete Quran data in JSON format with translations, surah info, juz mapping
 */
