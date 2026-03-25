import { useNavigate } from 'react-router-dom';
import { useCallback } from 'react';

/**
 * Robust back navigation hook.
 * Uses window.history.back() for natural back navigation.
 * Falls back to a specified route if user landed directly on this page.
 * Instant — no animations or delays.
 */
export function useSmartBack(fallback: string = '/') {
  const navigate = useNavigate();

  const goBack = useCallback(() => {
    // Check if there's history to go back to
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) {
      window.history.back();
    } else {
      // No history — navigate to fallback instantly
      navigate(fallback, { replace: true });
    }
  }, [navigate, fallback]);

  return goBack;
}
