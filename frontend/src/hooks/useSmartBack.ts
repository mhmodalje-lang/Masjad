import { useNavigate } from 'react-router-dom';
import { useCallback } from 'react';

/**
 * Simplest possible back navigation.
 * Uses window.history.back() which triggers React Router's popstate handling.
 * Falls back to a route if user landed directly on this page.
 */
export function useSmartBack(fallback: string = '/') {
  const navigate = useNavigate();

  const goBack = useCallback(() => {
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) {
      window.history.back();
    } else {
      navigate(fallback, { replace: true });
    }
  }, [navigate, fallback]);

  return goBack;
}
