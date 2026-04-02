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

// Service Worker is managed by VitePWA (registerSW.js) — no manual registration needed.
// VitePWA handles: precaching, offline mode, updates.
// sw-custom.js (imported by Workbox) handles: prayer notifications, push.

// Request persistent storage for offline data
if (navigator.storage && navigator.storage.persist) {
  navigator.storage.persist().then(granted => {
    if (granted) {
      console.log('[Storage] Persistent storage granted');
    }
  }).catch(() => {});
}

createRoot(document.getElementById("root")!).render(<App />);
