import { useEffect, useRef } from 'react';
import { useLocation, useNavigationType } from 'react-router-dom';

/**
 * Instant scroll to top on PUSH navigation only.
 * On POP (back/forward), the browser restores position naturally.
 * Uses 'auto' behavior for instant scroll (no smooth animation delay).
 */
export default function ScrollToTop() {
  const { pathname } = useLocation();
  const navType = useNavigationType();
  const prevPathRef = useRef(pathname);

  useEffect(() => {
    // Only scroll to top on PUSH (new page navigation)
    // Skip on POP (back/forward) - let browser handle restoration
    if (navType === 'PUSH' && prevPathRef.current !== pathname) {
      // Use instant scroll for faster feel
      window.scrollTo({ top: 0, behavior: 'instant' as ScrollBehavior });
    }
    prevPathRef.current = pathname;
  }, [pathname, navType]);

  return null;
}
