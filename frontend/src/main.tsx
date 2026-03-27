import { createRoot } from "react-dom/client";
import { Capacitor } from '@capacitor/core';
import './lib/i18nConfig';
import App from "./App.tsx";
import "./index.css";

// Initialize theme before render to prevent flash
const savedTheme = localStorage.getItem('almuadhin_theme');
const theme = (savedTheme === 'light') ? 'light' : 'dark';
document.documentElement.classList.add(theme);
if (theme === 'dark') document.documentElement.classList.remove('light');
else document.documentElement.classList.remove('dark');

// Platform detection
try {
  const platform = Capacitor.getPlatform();
  document.body.classList.add(`platform-${platform}`);
  if (Capacitor.isNativePlatform()) {
    document.body.classList.add('native-app');
  } else {
    document.body.classList.add('web-app');
  }
} catch {
  document.body.classList.add('platform-web', 'web-app');
}

// Register Service Worker (Web only - Capacitor handles its own)
if ('serviceWorker' in navigator && !Capacitor.isNativePlatform()) {
  window.addEventListener('load', () => {
    // Register the custom SW for prayer notifications
    navigator.serviceWorker.register('/sw-custom.js', { scope: '/' })
      .then(reg => {
        console.log('[SW] Custom SW registered:', reg.scope);
        
        // Check for updates periodically
        setInterval(() => {
          reg.update().catch(() => {});
        }, 30 * 60 * 1000); // Every 30 minutes
        
        // Handle updates
        reg.addEventListener('updatefound', () => {
          const newWorker = reg.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'activated') {
                // New SW activated - refresh if user approves
                if (document.hidden) {
                  // Auto-refresh if tab is not visible
                  window.location.reload();
                }
              }
            });
          }
        });
      })
      .catch(err => console.error('[SW] Registration failed:', err));
  });
}

// Request persistent storage for offline data
if (navigator.storage && navigator.storage.persist) {
  navigator.storage.persist().then(granted => {
    if (granted) {
      console.log('[Storage] Persistent storage granted');
    }
  }).catch(() => {});
}

createRoot(document.getElementById("root")!).render(<App />);
