import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

export default function ScrollToTop() {
  const { pathname } = useLocation();
  
  useEffect(() => {
    // Let browser handle scroll restoration naturally
    if ('scrollRestoration' in window.history) {
      window.history.scrollRestoration = 'auto';
    }
  }, []);
  
  useEffect(() => {
    // Only scroll to top on new page loads, not on back/forward navigation
    // Check if this is a history navigation (back/forward)
    const navigation = (window.performance?.getEntriesByType?.('navigation')?.[0] as any);
    const isBackForward = navigation?.type === 'back_forward';
    
    if (!isBackForward) {
      // New navigation - scroll to top
      window.scrollTo(0, 0);
    }
  }, [pathname]);
  
  return null;
}
