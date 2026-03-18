import { getAnalytics, logEvent, setUserProperties, isSupported } from 'firebase/analytics';
import app from './firebase';

let analytics: any = null;

// Initialize analytics only if supported (not in SSR or unsupported browsers)
export async function initAnalytics() {
  try {
    const supported = await isSupported();
    if (supported) {
      analytics = getAnalytics(app);
      console.log('Firebase Analytics initialized');
    }
  } catch (e) {
    console.warn('Firebase Analytics not supported:', e);
  }
  return analytics;
}

// Track page views
export function trackPageView(pageName: string, pageTitle?: string) {
  if (!analytics) return;
  try {
    logEvent(analytics, 'page_view', {
      page_path: pageName,
      page_title: pageTitle || pageName,
    });
  } catch (e) {
    // Silently fail
  }
}

// Track custom events
export function trackEvent(eventName: string, params?: Record<string, any>) {
  if (!analytics) return;
  try {
    logEvent(analytics, eventName, params);
  } catch (e) {
    // Silently fail
  }
}

// Track screen views (for mobile-like tracking)
export function trackScreenView(screenName: string, screenClass?: string) {
  if (!analytics) return;
  try {
    logEvent(analytics, 'screen_view', {
      firebase_screen: screenName,
      firebase_screen_class: screenClass || screenName,
    });
  } catch (e) {
    // Silently fail
  }
}

// Set user properties
export function setAnalyticsUserProperties(properties: Record<string, string>) {
  if (!analytics) return;
  try {
    setUserProperties(analytics, properties);
  } catch (e) {
    // Silently fail
  }
}

// Track ad events
export function trackAdEvent(adType: string, action: string, placement?: string) {
  trackEvent('ad_interaction', {
    ad_type: adType,
    action: action,
    placement: placement || 'unknown',
  });
}

// Track Islamic feature usage
export function trackIslamicFeature(feature: string, details?: Record<string, any>) {
  trackEvent('islamic_feature_used', {
    feature_name: feature,
    ...details,
  });
}

export default analytics;
