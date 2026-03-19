/**
 * Translates hadith/dua reference source names based on the current locale.
 * Arabic references are used in the data files and translated for other languages.
 */

const REFERENCE_MAP: Record<string, Record<string, string>> = {
  'البخاري': {
    en: 'Al-Bukhari', de: 'Al-Bukhari', fr: 'Al-Boukhari', ru: 'Аль-Бухари', tr: 'Buhari'
  },
  'مسلم': {
    en: 'Muslim', de: 'Muslim', fr: 'Muslim', ru: 'Муслим', tr: 'Müslim'
  },
  'البخاري ومسلم': {
    en: 'Al-Bukhari & Muslim', de: 'Al-Bukhari & Muslim', fr: 'Al-Boukhari & Muslim', ru: 'Аль-Бухари и Муслим', tr: 'Buhari ve Müslim'
  },
  'أبو داود': {
    en: 'Abu Dawud', de: 'Abu Dawud', fr: 'Abou Dawoud', ru: 'Абу Давуд', tr: 'Ebu Davud'
  },
  'الترمذي': {
    en: 'At-Tirmidhi', de: 'At-Tirmidhi', fr: 'At-Tirmidhi', ru: 'Ат-Тирмизи', tr: 'Tirmizi'
  },
  'النسائي': {
    en: "An-Nasa'i", de: "An-Nasa'i", fr: "An-Nassai", ru: 'Ан-Насаи', tr: 'Nesai'
  },
  'ابن ماجه': {
    en: 'Ibn Majah', de: 'Ibn Madscha', fr: 'Ibn Majah', ru: 'Ибн Маджа', tr: 'İbn Mace'
  },
  'ابن حبان': {
    en: 'Ibn Hibban', de: 'Ibn Hibban', fr: 'Ibn Hibban', ru: 'Ибн Хиббан', tr: 'İbn Hibban'
  },
  'ابن السني': {
    en: "Ibn As-Sunni", de: "Ibn As-Sunni", fr: "Ibn As-Sunni", ru: 'Ибн Ас-Сунни', tr: "İbn Es-Sünni"
  },
  'الطبراني': {
    en: 'At-Tabarani', de: 'At-Tabarani', fr: 'At-Tabarani', ru: 'Ат-Табарани', tr: 'Taberani'
  },
  'الموطأ': {
    en: "Al-Muwatta", de: "Al-Muwatta", fr: "Al-Mouwatta", ru: "Аль-Муватта", tr: "Muvatta"
  },
  'أبو داود والترمذي': {
    en: 'Abu Dawud & At-Tirmidhi', de: 'Abu Dawud & At-Tirmidhi', fr: 'Abou Dawoud & At-Tirmidhi', ru: 'Абу Давуд и Ат-Тирмизи', tr: 'Ebu Davud ve Tirmizi'
  },
  'أبو داود - إذا نسي التسمية': {
    en: 'Abu Dawud - If forgot Bismillah', de: 'Abu Dawud - Wenn Bismillah vergessen', fr: "Abou Dawoud - Si Bismillah oublié", ru: 'Абу Давуд - Если забыл Бисмиллях', tr: 'Ebu Davud - Bismillah unutulursa'
  },
  'البخاري - سيد الاستغفار': {
    en: 'Al-Bukhari - Master of Forgiveness', de: 'Al-Bukhari - Meister der Vergebung', fr: "Al-Boukhari - Maître du pardon", ru: 'Аль-Бухари - Господин истигфара', tr: 'Buhari - İstiğfarın Efendisi'
  },
  'البخاري - صلاة الاستخارة': {
    en: 'Al-Bukhari - Istikhara Prayer', de: 'Al-Bukhari - Istikharah-Gebet', fr: 'Al-Boukhari - Prière Istikhara', ru: 'Аль-Бухари - Молитва Истихара', tr: 'Buhari - İstihare Namazı'
  },
  'الترمذي - عند شرب اللبن': {
    en: 'At-Tirmidhi - When drinking milk', de: 'At-Tirmidhi - Beim Milchtrinken', fr: 'At-Tirmidhi - En buvant du lait', ru: 'Ат-Тирмизи - При питье молока', tr: 'Tirmizi - Süt içerken'
  },
  'عند استلام الحجر الأسود': {
    en: 'When touching the Black Stone', de: 'Beim Berühren des Schwarzen Steins', fr: 'En touchant la Pierre Noire', ru: 'При прикосновении к Чёрному камню', tr: 'Hacer-ül Esved\'e dokunurken'
  },
  // Quran references
  'القرآن 2:201': { en: "Quran 2:201", de: "Quran 2:201", fr: "Coran 2:201", ru: "Коран 2:201", tr: "Kur'an 2:201" },
  'القرآن 2:250': { en: "Quran 2:250", de: "Quran 2:250", fr: "Coran 2:250", ru: "Коран 2:250", tr: "Kur'an 2:250" },
  'القرآن 2:158': { en: "Quran 2:158", de: "Quran 2:158", fr: "Coran 2:158", ru: "Коран 2:158", tr: "Kur'an 2:158" },
  'القرآن 3:8': { en: "Quran 3:8", de: "Quran 3:8", fr: "Coran 3:8", ru: "Коран 3:8", tr: "Kur'an 3:8" },
  'القرآن 14:40': { en: "Quran 14:40", de: "Quran 14:40", fr: "Coran 14:40", ru: "Коран 14:40", tr: "Kur'an 14:40" },
  'القرآن 14:41': { en: "Quran 14:41", de: "Quran 14:41", fr: "Coran 14:41", ru: "Коран 14:41", tr: "Kur'an 14:41" },
  'القرآن 17:24': { en: "Quran 17:24", de: "Quran 17:24", fr: "Coran 17:24", ru: "Коран 17:24", tr: "Kur'an 17:24" },
  'القرآن 20:25-26': { en: "Quran 20:25-26", de: "Quran 20:25-26", fr: "Coran 20:25-26", ru: "Коран 20:25-26", tr: "Kur'an 20:25-26" },
  'القرآن 20:25-28': { en: "Quran 20:25-28", de: "Quran 20:25-28", fr: "Coran 20:25-28", ru: "Коран 20:25-28", tr: "Kur'an 20:25-28" },
  'القرآن 20:114': { en: "Quran 20:114", de: "Quran 20:114", fr: "Coran 20:114", ru: "Коран 20:114", tr: "Kur'an 20:114" },
  'القرآن 21:87': { en: "Quran 21:87", de: "Quran 21:87", fr: "Coran 21:87", ru: "Коран 21:87", tr: "Kur'an 21:87" },
  'القرآن 25:74': { en: "Quran 25:74", de: "Quran 25:74", fr: "Coran 25:74", ru: "Коран 25:74", tr: "Kur'an 25:74" },
  'القرآن 37:100': { en: "Quran 37:100", de: "Quran 37:100", fr: "Coran 37:100", ru: "Коран 37:100", tr: "Kur'an 37:100" },
  'القرآن 43:13-14': { en: "Quran 43:13-14", de: "Quran 43:13-14", fr: "Coran 43:13-14", ru: "Коран 43:13-14", tr: "Kur'an 43:13-14" },
};

/**
 * Translate a hadith/dua reference name from Arabic to the current locale.
 * Returns the original text if no translation is available.
 */
export function translateReference(arabicRef: string, locale: string): string {
  if (locale === 'ar') return arabicRef;
  
  // Exact match
  if (REFERENCE_MAP[arabicRef] && REFERENCE_MAP[arabicRef][locale]) {
    return REFERENCE_MAP[arabicRef][locale];
  }
  
  // Fallback to English if exact locale not found
  if (REFERENCE_MAP[arabicRef] && REFERENCE_MAP[arabicRef]['en']) {
    return REFERENCE_MAP[arabicRef]['en'];
  }
  
  // Try partial match for composite references
  let translated = arabicRef;
  for (const [arKey, translations] of Object.entries(REFERENCE_MAP)) {
    if (arabicRef.includes(arKey)) {
      const replacement = translations[locale] || translations['en'];
      if (replacement) {
        translated = translated.replace(arKey, replacement);
      }
    }
  }
  
  return translated;
}
