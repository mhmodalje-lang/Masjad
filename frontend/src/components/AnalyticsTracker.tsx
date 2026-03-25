import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { trackPageView, initAnalytics, setAnalyticsUserProperties } from '@/lib/analytics';
import i18n from '@/lib/i18nConfig';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

// Page name mapping using translation keys
const PAGE_NAME_KEYS: Record<string, string> = {
  '/': 'home',
  '/prayer-times': 'prayerTimes',
  '/qibla': 'qibla',
  '/quran': 'quran',
  '/tasbeeh': 'tasbeeh',
  '/duas': 'duas',
  '/more': 'more',
  '/tracker': 'prayerTracker',
  '/zakat': 'zakatCalculator',
  '/stories': 'stories',
  '/auth': 'auth',
  '/admin': 'admin',
  '/ruqyah': 'ruqyah',
  '/asma-al-husna': 'asmaAlHusna',
  '/sohba': 'sohba',
  '/explore': 'explore',
  '/ai-assistant': 'aiAssistant',
  '/marketplace': 'marketplace',
  '/rewards': 'rewards',
  '/store': 'store',
  '/donations': 'donations',
};

// Get or create session ID
function getSessionId(): string {
  let sid = sessionStorage.getItem('analytics_session_id');
  if (!sid) {
    sid = crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).substr(2, 16);
    sessionStorage.setItem('analytics_session_id', sid);
  }
  return sid;
}

export default function AnalyticsTracker() {
  const location = useLocation();
  const initialized = useRef(false);

  // Initialize Firebase Analytics on mount
  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      initAnalytics().then(() => {
        // Set user properties
        const lang = localStorage.getItem('user-selected-locale') || navigator.language;
        const theme = localStorage.getItem('almuadhin_theme') || 'dark';
        setAnalyticsUserProperties({
          app_language: lang,
          app_theme: theme,
          platform: /Mobi|Android/i.test(navigator.userAgent) ? 'mobile' : 'desktop',
        });
      });
    }
  }, []);

  // Track page views on route change (debounced for rapid navigation)
  useEffect(() => {
    const pagePath = location.pathname;
    const pageKey = PAGE_NAME_KEYS[pagePath];
    const pageName = pageKey ? i18n.t(pageKey) : pagePath;

    // Firebase Analytics
    trackPageView(pagePath, pageName);

    // Backend analytics (debounced, non-blocking)
    const timer = setTimeout(() => {
      const userId = localStorage.getItem('user_id') || 'anonymous';
      fetch(`${BACKEND_URL}/api/analytics/event`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_type: 'page_view',
          page: pagePath,
          user_id: userId,
          session_id: getSessionId(),
          metadata: { page_name: pageName },
          user_agent: navigator.userAgent,
        }),
      }).catch(() => {});
    }, 1000); // 1s debounce

    return () => clearTimeout(timer);
  }, [location.pathname]);

  return null;
}
