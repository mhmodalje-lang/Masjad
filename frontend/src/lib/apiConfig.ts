/**
 * Centralized API Configuration
 * ═══════════════════════════════
 * Single source of truth for backend URL.
 * To change production URL:
 *   1. Edit frontend/.env → REACT_APP_BACKEND_URL=https://your-domain.com
 *   2. Rebuild: yarn build
 *   3. Sync: npx cap sync android
 */

// Backend URL from environment variable
export const API_BASE_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

/**
 * Build a full API URL
 * @param path - API path starting with /api/
 * @returns Full URL string
 */
export function apiUrl(path: string): string {
  // Ensure path starts with /
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_BASE_URL}${cleanPath}`;
}

/**
 * Fetch with timeout and offline fallback
 */
export async function apiFetch(path: string, options?: RequestInit & { timeout?: number }): Promise<Response> {
  const url = apiUrl(path);
  const { timeout = 15000, ...fetchOptions } = options || {};
  
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(url, {
      ...fetchOptions,
      signal: controller.signal,
    });
    return response;
  } catch (error: any) {
    if (error.name === 'AbortError') {
      throw new Error('طلب API تجاوز الوقت المحدد');
    }
    if (!navigator.onLine) {
      throw new Error('لا يوجد اتصال بالإنترنت');
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * Current configuration info (for debugging)
 */
export function getApiConfig() {
  return {
    baseUrl: API_BASE_URL,
    isConfigured: !!API_BASE_URL,
    environment: import.meta.env.MODE,
  };
}
