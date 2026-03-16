import { useEffect } from 'react';
import { useLocation, useNavigationType } from 'react-router-dom';

/**
 * Only scrolls to top on PUSH (new page) navigation.
 * Does NOT scroll on POP (back/forward) — lets browser restore position naturally.
 */
export default function ScrollToTop() {
  const { pathname } = useLocation();
  const navType = useNavigationType();

  useEffect(() => {
    if ('scrollRestoration' in window.history) {
      window.history.scrollRestoration = 'manual';
    }
  }, []);

  useEffect(() => {
    if (navType === 'PUSH') {
      window.scrollTo(0, 0);
    }
  }, [pathname, navType]);

  return null;
}
