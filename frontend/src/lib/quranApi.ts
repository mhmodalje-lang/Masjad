/**
 * Quran.com API v4 Integration — STRICT DATA MAPPING (V2026)
 * 
 * ALL Quran translations, tafsir, and Surah names are fetched DIRECTLY
 * from https://api.quran.com/api/v4 — NO AI translation, NO manual text.
 *
 * VERIFIED Translation IDs (tested against live API):
 * - English (en): 20 — Saheeh International
 * - French (fr): 31 — Muhammad Hamidullah
 * - German (de): 27 — Bubenheim & Elyas
 * - Turkish (tr): 77 — Diyanet İşleri
 * - Russian (ru): 79 — Abu Adel
 * - Dutch (nl): 235 — Malak Faris Abdalsalaam
 * - Swedish (sv): 48 — Knut Bernström
 * - Greek (el): NONE — show "Coming Soon" + Arabic original
 * - Arabic (ar): Tafsir 16 — Tafsir Al-Muyassar (for explanation)
 */

const QURAN_API_BASE = 'https://api.quran.com/api/v4';

// ═══════ VERIFIED TRANSLATION IDS ═══════
export const QURAN_TRANSLATION_IDS: Record<string, number> = {
  en: 20,   // Saheeh International
  fr: 31,   // Muhammad Hamidullah
  de: 27,   // Bubenheim & Elyas
  tr: 77,   // Diyanet İşleri
  ru: 79,   // Abu Adel
  nl: 235,  // Malak Faris Abdalsalaam
  sv: 48,   // Knut Bernström
  // el: NONE — Greek translation not available in public API
  // ar: Uses Tafsir Al-Muyassar (16) as explanation
};

// ═══════ TAFSIR IDS (per language where available) ═══════
export const QURAN_TAFSIR_IDS: Record<string, number> = {
  ar: 16,   // Tafsir Al-Muyassar (Arabic)
  en: 169,  // Ibn Kathir Abridged (English)
  ru: 170,  // Al-Sa'di (Russian)
};

// Arabic tafsir as universal fallback
export const TAFSIR_MUYASSAR_ID = 16;
export const TAFSIR_IBN_KATHIR_AR = 14;

// ═══════ RECITER IDS ═══════
export const QURAN_RECITERS: Record<string, { id: number; name: string }> = {
  'al-afasy': { id: 7, name: 'Mishary Rashid Alafasy' },
  'al-husary': { id: 5, name: 'Mahmoud Khalil Al-Husary' },
  'abdul-basit': { id: 1, name: 'Abdul Basit Abdul Samad' },
  'al-minshawi': { id: 6, name: 'Mohamed Siddiq Al-Minshawi' },
  'as-sudais': { id: 4, name: 'Abdurrahman As-Sudais' },
};

// ═══════ TYPES ═══════
export interface QuranChapter {
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
}

export interface QuranJuz {
  id: number;
  juz_number: number;
  verse_mapping: Record<string, string>;
  first_verse_id: number;
  last_verse_id: number;
  verses_count: number;
}

// ═══════ HELPER: Get translation ID for a language ═══════
export function getTranslationId(language: string): number | null {
  return QURAN_TRANSLATION_IDS[language] ?? null;
}

// ═══════ HELPER: "Coming Soon" labels ═══════
const COMING_SOON_LABELS: Record<string, string> = {
  en: 'Translation coming soon',
  fr: 'Traduction à venir',
  de: 'Übersetzung kommt bald',
  tr: 'Çeviri yakında',
  ru: 'Перевод скоро',
  nl: 'Vertaling komt binnenkort',
  sv: 'Översättning kommer snart',
  el: 'Η μετάφραση έρχεται σύντομα',
  ar: '',
};

export function getComingSoonLabel(language: string): string {
  return COMING_SOON_LABELS[language] || COMING_SOON_LABELS['en'];
}

// ═══════ HELPER: Strip HTML from translation text ═══════
function stripHtml(text: string): string {
  return text.replace(/<sup[^>]*>.*?<\/sup>/gi, '').replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim();
}

// ═══════ 1. Fetch ALL chapters with localized names ═══════
export async function fetchChapters(language: string = 'ar'): Promise<QuranChapter[]> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/chapters?language=${language}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return data.chapters || [];
  } catch (error) {
    console.error('Failed to fetch chapters:', error);
    return [];
  }
}

// ═══════ 2. Fetch single chapter info ═══════
export async function fetchChapterInfo(chapterNumber: number, language: string = 'ar'): Promise<QuranChapter | null> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/chapters/${chapterNumber}?language=${language}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return data.chapter || null;
  } catch (error) {
    console.error(`Failed to fetch chapter ${chapterNumber}:`, error);
    return null;
  }
}

// ═══════ 3. Fetch verses by chapter WITH translations (dual-fetch approach) ═══════
export async function fetchVersesByChapter(
  chapterNumber: number,
  language: string = 'ar',
  page: number = 1,
  perPage: number = 50
): Promise<{ verses: QuranVerse[]; pagination: any }> {
  try {
    // Step 1: Fetch Arabic verses
    const versesUrl = `${QURAN_API_BASE}/verses/by_chapter/${chapterNumber}?language=${language}&words=false&page=${page}&per_page=${perPage}&fields=text_uthmani`;
    const versesRes = await fetch(versesUrl);
    if (!versesRes.ok) throw new Error(`Verses API error: ${versesRes.status}`);
    const versesData = await versesRes.json();
    const verses: QuranVerse[] = versesData.verses || [];
    const pagination = versesData.pagination || {};

    // Step 2: Fetch translations separately from /quran/translations/{id}
    const translationId = getTranslationId(language);
    if (translationId && verses.length > 0) {
      try {
        const transUrl = `${QURAN_API_BASE}/quran/translations/${translationId}?chapter_number=${chapterNumber}`;
        const transRes = await fetch(transUrl);
        if (transRes.ok) {
          const transData = await transRes.json();
          const transArr = transData.translations || [];
          // Match by position (translations are ordered by verse number)
          for (let i = 0; i < verses.length && i < transArr.length; i++) {
            const rawText = transArr[i]?.text || '';
            verses[i].translations = [{
              id: translationId,
              resource_id: translationId,
              text: stripHtml(rawText),
            }];
          }
        }
      } catch (e) {
        console.warn('Translation fetch failed, showing Arabic only:', e);
      }
    }

    // For Arabic: fetch Al-Muyassar tafsir as explanation
    if (language === 'ar' && verses.length > 0) {
      try {
        const muyassarUrl = `${QURAN_API_BASE}/tafsirs/16/by_chapter/${chapterNumber}`;
        const muyassarRes = await fetch(muyassarUrl);
        if (muyassarRes.ok) {
          const muyassarData = await muyassarRes.json();
          const tafsirArr = muyassarData.tafsirs || [];
          // Match by verse_key
          const tafsirMap = new Map<string, string>();
          for (const t of tafsirArr) {
            if (t.verse_key) {
              tafsirMap.set(t.verse_key, stripHtml(t.text || ''));
            }
          }
          for (const verse of verses) {
            const tafsirText = tafsirMap.get(verse.verse_key);
            if (tafsirText) {
              verse.translations = [{
                id: 16,
                resource_id: 16,
                text: tafsirText,
              }];
            }
          }
        }
      } catch (e) {
        console.warn('Muyassar fetch failed:', e);
      }
    }

    return { verses, pagination };
  } catch (error) {
    console.error(`Failed to fetch verses for chapter ${chapterNumber}:`, error);
    return { verses: [], pagination: {} };
  }
}

// ═══════ 4. Fetch verses by Juz WITH translations ═══════
export async function fetchVersesByJuz(
  juzNumber: number,
  language: string = 'ar',
  page: number = 1,
  perPage: number = 50
): Promise<{ verses: QuranVerse[]; pagination: any }> {
  try {
    const versesUrl = `${QURAN_API_BASE}/verses/by_juz/${juzNumber}?language=${language}&words=false&page=${page}&per_page=${perPage}&fields=text_uthmani`;
    const res = await fetch(versesUrl);
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

// ═══════ 4b. Fetch chapter tafsir (per language or fallback to Arabic) ═══════
export async function fetchChapterTafsir(
  chapterNumber: number,
  language: string = 'ar'
): Promise<Map<string, string>> {
  const tafsirMap = new Map<string, string>();
  
  // Get tafsir ID for the language, fallback to Arabic Muyassar
  const tafsirId = QURAN_TAFSIR_IDS[language] || TAFSIR_MUYASSAR_ID;
  
  try {
    const res = await fetch(`${QURAN_API_BASE}/tafsirs/${tafsirId}/by_chapter/${chapterNumber}`);
    if (!res.ok) return tafsirMap;
    const data = await res.json();
    for (const t of (data.tafsirs || [])) {
      if (t.verse_key) {
        tafsirMap.set(t.verse_key, stripHtml(t.text || ''));
      }
    }
  } catch (e) {
    console.warn(`Tafsir fetch failed for chapter ${chapterNumber}, lang ${language}:`, e);
  }
  
  return tafsirMap;
}

// ═══════ 4c. Tafsir label per language ═══════
export function getTafsirLabel(language: string): string {
  const labels: Record<string, string> = {
    ar: 'التفسير الميسر',
    en: 'Tafsir Ibn Kathir (Abridged)',
    fr: 'Explication (Tafsir Al-Muyassar)',
    de: 'Erklärung (Tafsir Al-Muyassar)',
    tr: 'Tefsir (Tefsir el-Müyesser)',
    ru: 'Тафсир ас-Саади',
    nl: 'Uitleg (Tafsir Al-Muyassar)',
    sv: 'Förklaring (Tafsir Al-Muyassar)',
    el: 'Ερμηνεία (Tafsir Al-Muyassar)',
  };
  return labels[language] || labels['en'];
}

// ═══════ 4d. Translation label per language ═══════
export function getTranslationLabel(language: string): string {
  const labels: Record<string, string> = {
    ar: 'ترجمة المعاني',
    en: 'Translation of Meanings',
    fr: 'Traduction des sens',
    de: 'Übersetzung der Bedeutungen',
    tr: 'Anlam Çevirisi',
    ru: 'Перевод смыслов',
    nl: 'Vertaling van de betekenissen',
    sv: 'Översättning av innebörderna',
    el: 'Μετάφραση νοημάτων',
  };
  return labels[language] || labels['en'];
}


// ═══════ 5. Fetch translation for a specific verse ═══════
export async function fetchVerseTranslation(
  verseKey: string,
  language: string
): Promise<string | null> {
  const translationId = getTranslationId(language);
  if (!translationId) return null;
  
  try {
    const res = await fetch(`${QURAN_API_BASE}/quran/translations/${translationId}?verse_key=${verseKey}`);
    if (!res.ok) return null;
    const data = await res.json();
    const translations = data.translations || [];
    if (translations.length > 0) {
      return stripHtml(translations[0].text || '');
    }
    return null;
  } catch {
    return null;
  }
}

// ═══════ 6. Fetch Tafsir for a verse ═══════
export async function fetchTafsir(
  verseKey: string,
  tafsirId: number = QURAN_TAFSIR_IDS.ibn_kathir_ar
): Promise<string | null> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/tafsirs/${tafsirId}/by_ayah/${verseKey}`);
    if (!res.ok) return null;
    const data = await res.json();
    if (data.tafsir) {
      return stripHtml(data.tafsir.text || '');
    }
    return null;
  } catch {
    return null;
  }
}

// ═══════ 7. Fetch verse Arabic text (Uthmani) ═══════
export async function fetchVerseUthmani(verseKey: string): Promise<string | null> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/quran/verses/uthmani?verse_key=${verseKey}`);
    if (!res.ok) return null;
    const data = await res.json();
    if (data.verses && data.verses.length > 0) {
      return data.verses[0].text_uthmani || null;
    }
    return null;
  } catch {
    return null;
  }
}

// ═══════ 8. Search the Quran ═══════
export async function searchQuran(
  query: string,
  language: string = 'ar',
  page: number = 1,
  size: number = 20
): Promise<{ results: any[]; total: number }> {
  try {
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

// ═══════ 9. Fetch verse audio ═══════
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

// ═══════ 10. Fetch all Juz info ═══════
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

// ═══════ 11. Fetch random verse for "Verse of the Day" ═══════
export async function fetchVerseOfDay(language: string = 'ar'): Promise<{
  text: string;
  translation?: string;
  surah: string;
  surahArabic: string;
  ayah: number;
  chapterNumber: number;
} | null> {
  try {
    const now = new Date();
    const startOfYear = new Date(now.getFullYear(), 0, 0);
    const diff = now.getTime() - startOfYear.getTime();
    const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    const INSPIRING_VERSES = [
      '2:286', '2:255', '2:152', '2:186', '3:139', '3:173', '5:3', '6:162',
      '9:51', '10:62', '12:87', '13:28', '14:7', '15:9', '16:97', '17:82',
      '20:114', '21:87', '23:115', '24:35', '25:74', '28:24', '29:69', '31:17',
      '33:56', '35:32', '39:53', '40:60', '42:19', '47:7', '48:29', '49:13',
      '55:13', '56:10', '59:22', '61:13', '65:2', '65:3', '67:2', '68:4',
    ];
    
    const verseKey = INSPIRING_VERSES[dayOfYear % INSPIRING_VERSES.length];
    const [chapterNum, verseNum] = verseKey.split(':').map(Number);
    
    const arabicText = await fetchVerseUthmani(verseKey);
    if (!arabicText) return null;
    
    const chapter = await fetchChapterInfo(chapterNum, language);
    
    let translation: string | undefined;
    if (language !== 'ar') {
      const trans = await fetchVerseTranslation(verseKey, language);
      if (trans) {
        translation = trans;
      } else {
        translation = getComingSoonLabel(language);
      }
    }
    
    return {
      text: arabicText,
      translation,
      surah: chapter?.translated_name?.name || chapter?.name_simple || '',
      surahArabic: chapter?.name_arabic || '',
      ayah: verseNum,
      chapterNumber: chapterNum,
    };
  } catch (error) {
    console.error('Failed to fetch verse of day:', error);
    return null;
  }
}

// ═══════ 12. Fetch audio for full Surah ═══════
export async function fetchSurahAudio(
  chapterNumber: number,
  reciterId: number = 7
): Promise<string | null> {
  try {
    const res = await fetch(`${QURAN_API_BASE}/chapter_recitations/${reciterId}/${chapterNumber}`);
    if (!res.ok) return null;
    const data = await res.json();
    return data.audio_file?.audio_url || null;
  } catch {
    return null;
  }
}
