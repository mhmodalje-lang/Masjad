import { useEffect, useLayoutEffect } from 'react';
import { useLocation } from 'react-router-dom';

export default function ScrollToTop() {
  const { pathname } = useLocation();
  
  // Set browser scroll restoration to manual (let browser handle back button naturally)
  useEffect(() => {
    if ('scrollRestoration' in window.history) {
      window.history.scrollRestoration = 'auto'; // Let browser handle it
    }
  }, []);
  
  // Only scroll to top on forward navigation
  useLayoutEffect(() => {
    // For new page navigation (not back button), scroll to top
    window.scrollTo(0, 0);
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
  }, [pathname]);
  
  return null;
}
