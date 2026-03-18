import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { trackPageView, initAnalytics, setAnalyticsUserProperties } from '@/lib/analytics';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

// Page name mapping for Arabic names
const PAGE_NAMES: Record<string, string> = {
  '/': 'الرئيسية',
  '/prayer-times': 'مواقيت الصلاة',
  '/qibla': 'اتجاه القبلة',
  '/quran': 'القرآن الكريم',
  '/tasbeeh': 'التسبيح',
  '/duas': 'الأدعية',
  '/more': 'المزيد',
  '/tracker': 'متتبع الصلاة',
  '/zakat': 'حاسبة الزكاة',
  '/stories': 'الحكايات',
  '/auth': 'تسجيل الدخول',
  '/admin': 'لوحة التحكم',
  '/ruqyah': 'الرقية الشرعية',
  '/asma-al-husna': 'أسماء الله الحسنى',
  '/sohba': 'صُحبة',
  '/explore': 'استكشاف',
  '/ai-assistant': 'المساعد الذكي',
  '/marketplace': 'السوق',
  '/rewards': 'المكافآت',
  '/store': 'المتجر',
  '/donations': 'التبرعات',
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

  // Track page views on route change
  useEffect(() => {
    const pagePath = location.pathname;
    const pageName = PAGE_NAMES[pagePath] || pagePath;

    // Firebase Analytics
    trackPageView(pagePath, pageName);

    // Backend analytics (non-blocking)
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
  }, [location.pathname]);

  return null;
}
