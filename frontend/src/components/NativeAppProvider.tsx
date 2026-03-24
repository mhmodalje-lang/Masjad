/**
 * NativeAppProvider - Manages native app lifecycle and features
 * Handles: back button, app state, status bar, keyboard, deep links
 * Only activates when running inside Capacitor (native app)
 */
import { useEffect, useCallback, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { isNativeApp, isAndroid, configureStatusBar, hapticFeedback, exitApp } from '@/lib/nativeBridge';
import { useTheme } from '@/components/ThemeProvider';

// ═══ Track navigation for back button ═══
const ROOT_PATHS = ['/', '/stories', '/kids-zone', '/more'];

export function NativeAppProvider({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { theme } = useTheme();
  const backPressCount = useRef(0);
  const backPressTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // ═══ Configure Status Bar on theme change ═══
  useEffect(() => {
    if (!isNativeApp()) return;
    configureStatusBar(theme === 'dark');
  }, [theme]);

  // ═══ Handle Android Back Button ═══
  const handleBackButton = useCallback(() => {
    const isRootPage = ROOT_PATHS.includes(location.pathname);

    if (isRootPage) {
      // Double-tap to exit on root pages
      backPressCount.current += 1;
      if (backPressCount.current >= 2) {
        exitApp();
        return;
      }
      hapticFeedback('warning');
      // Reset counter after 2 seconds
      if (backPressTimer.current) clearTimeout(backPressTimer.current);
      backPressTimer.current = setTimeout(() => {
        backPressCount.current = 0;
      }, 2000);
    } else {
      // Navigate back on non-root pages
      hapticFeedback('light');
      const idx = (window.history.state as any)?.idx;
      if (typeof idx === 'number' && idx > 0) {
        window.history.back();
      } else {
        navigate('/', { replace: true });
      }
    }
  }, [location.pathname, navigate]);

  useEffect(() => {
    if (!isNativeApp() || !isAndroid()) return;
    let cleanup: (() => void) | null = null;

    (async () => {
      try {
        const { App } = await import('@capacitor/app');
        const listener = await App.addListener('backButton', () => {
          handleBackButton();
        });
        cleanup = () => listener.remove();
      } catch { /* not available */ }
    })();

    return () => { cleanup?.(); };
  }, [handleBackButton]);

  // ═══ Handle Keyboard (iOS scroll fix) ═══
  useEffect(() => {
    if (!isNativeApp()) return;
    let cleanup: (() => void) | null = null;

    (async () => {
      try {
        const { Keyboard } = await import('@capacitor/keyboard');
        const showListener = await Keyboard.addListener('keyboardWillShow', (info) => {
          document.documentElement.style.setProperty('--keyboard-height', `${info.keyboardHeight}px`);
          document.body.classList.add('keyboard-open');
        });
        const hideListener = await Keyboard.addListener('keyboardWillHide', () => {
          document.documentElement.style.setProperty('--keyboard-height', '0px');
          document.body.classList.remove('keyboard-open');
        });
        cleanup = () => {
          showListener.remove();
          hideListener.remove();
        };
      } catch { /* keyboard plugin not available */ }
    })();

    return () => { cleanup?.(); };
  }, []);

  // ═══ Handle App State (pause/resume) ═══
  useEffect(() => {
    if (!isNativeApp()) return;
    let cleanup: (() => void) | null = null;

    (async () => {
      try {
        const { App } = await import('@capacitor/app');
        const listener = await App.addListener('appStateChange', (state) => {
          if (state.isActive) {
            // App resumed - refresh time-sensitive data
            document.dispatchEvent(new CustomEvent('app-resumed'));
          }
        });
        cleanup = () => listener.remove();
      } catch { /* not available */ }
    })();

    return () => { cleanup?.(); };
  }, []);

  // ═══ Hide splash screen after app is ready ═══
  useEffect(() => {
    if (!isNativeApp()) return;
    (async () => {
      try {
        const { SplashScreen } = await import('@capacitor/splash-screen');
        // Give the app a moment to render
        setTimeout(() => {
          SplashScreen.hide({ fadeOutDuration: 300 });
        }, 500);
      } catch { /* not available */ }
    })();
  }, []);

  return <>{children}</>;
}
