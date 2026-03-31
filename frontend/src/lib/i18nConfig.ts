/**
 * Professional i18next Configuration for Azan & Hikaya
 * Supports: Arabic (ar), English (en), German (de), Russian (ru), French (fr), Turkish (tr)
 * Features:
 * - Auto-detection of browser/system language
 * - RTL/LTR automatic switching
 * - Static bundled translations (no API dependency)
 * - Religious text preservation (Duas/Dhikr stay in Arabic)
 */
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import all locale files
import arTranslations from '@/locales/ar.json';
import enTranslations from '@/locales/en.json';
import deTranslations from '@/locales/de.json';
import ruTranslations from '@/locales/ru.json';
import frTranslations from '@/locales/fr.json';
import trTranslations from '@/locales/tr.json';
import svTranslations from '@/locales/sv.json';
import nlTranslations from '@/locales/nl.json';
import elTranslations from '@/locales/el.json';
import deATTranslations from '@/locales/de-AT.json';

// RTL languages list
export const RTL_LANGUAGES = ['ar', 'he', 'fa', 'ur', 'ps', 'sd', 'yi', 'ku'];

// Supported languages with metadata
export const SUPPORTED_LANGUAGES: Array<{code: string; label: string; flag: string; dir: 'rtl' | 'ltr'; nativeName: string}> = [
  { code: 'ar', label: 'العربية', flag: '🇸🇦', dir: 'rtl', nativeName: 'العربية' },
  { code: 'en', label: 'English', flag: '🇬🇧', dir: 'ltr', nativeName: 'English' },
  { code: 'de', label: 'Deutsch', flag: '🇩🇪', dir: 'ltr', nativeName: 'Deutsch' },
  { code: 'ru', label: 'Русский', flag: '🇷🇺', dir: 'ltr', nativeName: 'Русский' },
  { code: 'fr', label: 'Français', flag: '🇫🇷', dir: 'ltr', nativeName: 'Français' },
  { code: 'tr', label: 'Türkçe', flag: '🇹🇷', dir: 'ltr', nativeName: 'Türkçe' },
  { code: 'sv', label: 'Svenska', flag: '🇸🇪', dir: 'ltr', nativeName: 'Svenska' },
  { code: 'nl', label: 'Nederlands', flag: '🇳🇱', dir: 'ltr', nativeName: 'Nederlands' },
  { code: 'el', label: 'Ελληνικά', flag: '🇬🇷', dir: 'ltr', nativeName: 'Ελληνικά' },
  { code: 'de-AT', label: 'Österreichisch', flag: '🇦🇹', dir: 'ltr', nativeName: 'Österreichisches Deutsch' },
];

export const SUPPORTED_LANGUAGE_CODES = SUPPORTED_LANGUAGES.map(l => l.code);

/**
 * Check if a language is RTL
 */
export function isRTL(lang: string): boolean {
  return RTL_LANGUAGES.includes(lang);
}

/**
 * Get direction for a language
 */
export function getDir(lang: string): 'rtl' | 'ltr' {
  return isRTL(lang) ? 'rtl' : 'ltr';
}

/**
 * Apply document direction and lang attribute
 */
export function applyDirection(lang: string): void {
  const dir = getDir(lang);
  document.documentElement.dir = dir;
  document.documentElement.lang = lang;
  document.documentElement.setAttribute('data-direction', dir);
  // Add/remove RTL class for CSS targeting
  if (dir === 'rtl') {
    document.documentElement.classList.add('rtl');
    document.documentElement.classList.remove('ltr');
  } else {
    document.documentElement.classList.add('ltr');
    document.documentElement.classList.remove('rtl');
  }
}

// Initialize i18next
i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      ar: { translation: arTranslations },
      en: { translation: enTranslations },
      de: { translation: deTranslations },
      ru: { translation: ruTranslations },
      fr: { translation: frTranslations },
      tr: { translation: trTranslations },
      sv: { translation: svTranslations },
      nl: { translation: nlTranslations },
      el: { translation: elTranslations },
      'de-AT': { translation: deATTranslations },
    },
    fallbackLng: 'ar',
    supportedLngs: SUPPORTED_LANGUAGE_CODES,
    interpolation: {
      escapeValue: false, // React already escapes
    },
    detection: {
      // Only use user's manual language selection, default to Arabic
      order: ['localStorage', 'querystring'],
      lookupQuerystring: 'lang',
      lookupLocalStorage: 'user-selected-locale',
      caches: ['localStorage'],
    },
    react: {
      useSuspense: false, // Don't suspend - we have our own loading state
    },
  });

// Apply initial direction
applyDirection(i18n.language || 'ar');

// Listen for language changes to update document direction
i18n.on('languageChanged', (lng: string) => {
  applyDirection(lng);
});

export default i18n;
