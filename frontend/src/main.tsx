import { createRoot } from "react-dom/client";
// Initialize i18next before app render
import './lib/i18nConfig';
import App from "./App.tsx";
import "./index.css";
import { Capacitor } from '@capacitor/core';

// Initialize theme before render to prevent flash
const savedTheme = localStorage.getItem('almuadhin_theme');
const theme = (savedTheme === 'light') ? 'light' : 'dark';
document.documentElement.classList.add(theme);
if (theme === 'dark') document.documentElement.classList.remove('light');
else document.documentElement.classList.remove('dark');

// ═══ Native App Detection ═══
// Add platform classes to body for CSS targeting
function detectPlatform() {
  try {
    const platform = Capacitor.getPlatform();
    const isNative = Capacitor.isNativePlatform();

    document.body.classList.add(`platform-${platform}`);
    if (isNative) {
      document.body.classList.add('native-app');
      // Prevent overscroll bouncing (native app indicator)
      document.body.style.overscrollBehavior = 'none';
      // Prevent pull-to-refresh on Android Chrome
      document.body.style.overflow = 'hidden';
    } else {
      document.body.classList.add('web-app');
    }
  } catch {
    document.body.classList.add('platform-web', 'web-app');
  }
}
detectPlatform();

// ═══ Register Service Worker (Web only) ═══
// Only register service worker on web (not in native app)
if ('serviceWorker' in navigator && !Capacitor.isNativePlatform()) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw-custom.js', { scope: '/' })
      .then(reg => {
        console.log('Service Worker registered:', reg.scope);
        // Check for updates
        reg.addEventListener('updatefound', () => {
          const newWorker = reg.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'activated') {
                console.log('New Service Worker activated');
              }
            });
          }
        });
      })
      .catch(err => console.error('SW registration failed:', err));
  });
}

createRoot(document.getElementById("root")!).render(<App />);
