import { useNavigate } from 'react-router-dom';
import { useCallback } from 'react';

/**
 * Smart back navigation - goes to previous page if history exists,
 * otherwise falls back to home. Prevents unexpected jumps.
 */
export function useSmartBack() {
  const navigate = useNavigate();

  const goBack = useCallback(() => {
    // Check if there's browser history to go back to
    if (window.history.length > 1) {
      navigate(-1);
    } else {
      // Only go to home if there's no history at all
      navigate('/', { replace: true });
    }
  }, [navigate]);

  return goBack;
}
