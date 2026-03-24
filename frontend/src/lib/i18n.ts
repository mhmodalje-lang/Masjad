/**
 * i18n utilities - Backward compatible wrapper around i18next
 * This file maintains the existing API while delegating to i18next
 */
import i18n from '@/lib/i18nConfig';
import { isRTL, getDir, SUPPORTED_LANGUAGES, RTL_LANGUAGES, SUPPORTED_LANGUAGE_CODES } from '@/lib/i18nConfig';
import enTranslations from '@/locales/en.json';

// Re-export for backward compatibility
export { isRTL as isRTLLanguage, getDir as getDirection };

/**
 * Detect device language - returns the 2-letter language code
 */
export function detectDeviceLanguage(): string {
  // Check if user has already set a language preference
  const saved = typeof localStorage !== 'undefined' ? localStorage.getItem('user-selected-locale') : null;
  if (saved && SUPPORTED_LANGUAGE_CODES.includes(saved)) return saved;

  const appLang = typeof localStorage !== 'undefined' ? localStorage.getItem('app-language') : null;
  if (appLang && SUPPORTED_LANGUAGE_CODES.includes(appLang)) return appLang;

  // Auto-detect from browser/device
  try {
    const browserLang = navigator.language?.toLowerCase() || '';
    // Check for Austrian German specifically
    if (browserLang === 'de-at' || browserLang.startsWith('de-at')) return 'de-AT';
    const langCode = browserLang.split('-')[0];
    
    if (SUPPORTED_LANGUAGE_CODES.includes(langCode)) {
      return langCode;
    }

    // Check navigator.languages for secondary preferences
    const langs = navigator.languages || [];
    for (const lang of langs) {
      const full = lang.toLowerCase();
      if (full === 'de-at' || full.startsWith('de-at')) return 'de-AT';
      const code = full.split('-')[0];
      if (SUPPORTED_LANGUAGE_CODES.includes(code)) {
        return code;
      }
    }
  } catch {}

  // Default to English for international users
  return 'en';
}

/**
 * Load translations for a language.
 * With i18next, translations are pre-loaded. This returns the resource bundle.
 */
export async function loadTranslations(lang: string): Promise<Record<string, string>> {
  // Ensure i18next has loaded the language
  if (i18n.language !== lang) {
    await i18n.changeLanguage(lang);
  }
  
  // Get resource bundle from i18next
  const bundle = i18n.getResourceBundle(lang, 'translation');
  if (bundle && Object.keys(bundle).length > 0) {
    return bundle as Record<string, string>;
  }
  
  // Fallback to English
  return enTranslations as Record<string, string>;
}

/**
 * Get list of supported languages with labels and flags
 */
export function getSupportedLanguages() {
  return SUPPORTED_LANGUAGES.map(l => ({
    code: l.code,
    label: l.label,
    flag: l.flag,
    dir: l.dir,
  }));
}

/**
 * Get a single translation key (synchronous - uses i18next)
 */
export function getTranslation(key: string, lang: string): string {
  return i18n.getFixedT(lang)(key) || (enTranslations as Record<string, string>)[key] || key;
}

/**
 * Get all Arabic source strings
 */
export function getArabicStrings(): Record<string, string> {
  return enTranslations as Record<string, string>;
}
