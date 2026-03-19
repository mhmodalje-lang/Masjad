import React, { createContext, useContext, useEffect, useMemo, useState, useCallback, type ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import i18n from '@/lib/i18nConfig';
import { isRTL, getDir, applyDirection, SUPPORTED_LANGUAGES } from '@/lib/i18nConfig';

interface LocaleContextType {
  locale: string;
  t: (key: string) => string;
  dir: 'rtl' | 'ltr';
  isRTL: boolean;
  ready: boolean;
  setLocale: (locale: string) => void;
}

const LocaleContext = createContext<LocaleContextType | undefined>(undefined);

export function LocaleProvider({ children }: { children: ReactNode }) {
  const { t: i18nT, ready: i18nReady } = useTranslation();
  const [locale, setLocaleState] = useState<string>(() => {
    return i18n.language || 'ar';
  });
  const [dir, setDir] = useState<'rtl' | 'ltr'>(() => getDir(i18n.language || 'ar'));

  const isRTLValue = dir === 'rtl';

  // Sync with i18next language changes
  useEffect(() => {
    const handleLanguageChanged = (lng: string) => {
      setLocaleState(lng);
      const newDir = getDir(lng);
      setDir(newDir);
      applyDirection(lng);
    };

    i18n.on('languageChanged', handleLanguageChanged);

    // Apply initial direction
    applyDirection(locale);

    return () => {
      i18n.off('languageChanged', handleLanguageChanged);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Translation function - bridges i18next with existing codebase
  const t = useCallback((key: string): string => {
    const result = i18nT(key);
    // If i18next returns the key itself (not found), return the key
    return result || key;
  }, [i18nT]);

  const setLocale = useCallback((newLocale: string) => {
    // Update i18next language
    i18n.changeLanguage(newLocale);
    // Save user's manual selection
    localStorage.setItem('user-selected-locale', newLocale);
    localStorage.setItem('app-language', newLocale);
  }, []);

  const value = useMemo(() => ({
    locale,
    t,
    dir,
    isRTL: isRTLValue,
    ready: i18nReady,
    setLocale,
  }), [locale, t, dir, isRTLValue, i18nReady, setLocale]);

  return (
    <LocaleContext.Provider value={value}>
      {children}
    </LocaleContext.Provider>
  );
}

export function useLocale() {
  const ctx = useContext(LocaleContext);
  if (!ctx) throw new Error('useLocale must be used within LocaleProvider');
  return ctx;
}
