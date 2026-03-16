/**
 * Theme management for أذان وحكاية
 * Islamic color themes: Dark (Emerald/Gold) and Light (Cream/Gold)
 */

export type ThemeMode = 'dark' | 'light' | 'system';

const THEME_KEY = 'almuadhin_theme';

export function getSystemTheme(): 'dark' | 'light' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export function getSavedTheme(): ThemeMode {
  return (localStorage.getItem(THEME_KEY) as ThemeMode) || 'system';
}

export function getEffectiveTheme(): 'dark' | 'light' {
  const saved = getSavedTheme();
  if (saved === 'system') return getSystemTheme();
  return saved;
}

export function setTheme(mode: ThemeMode): void {
  localStorage.setItem(THEME_KEY, mode);
  applyTheme(mode === 'system' ? getSystemTheme() : mode);
}

export function applyTheme(theme: 'dark' | 'light'): void {
  const root = document.documentElement;
  if (theme === 'dark') {
    root.classList.add('dark');
    root.classList.remove('light');
  } else {
    root.classList.remove('dark');
    root.classList.add('light');
  }
}

export function initTheme(): void {
  applyTheme(getEffectiveTheme());
  // Watch system changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (getSavedTheme() === 'system') {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });
}
