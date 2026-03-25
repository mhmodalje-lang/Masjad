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

// Register Service Worker (Web only)
if ('serviceWorker' in navigator && !Capacitor.isNativePlatform()) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw-custom.js', { scope: '/' })
      .then(reg => console.log('SW registered:', reg.scope))
      .catch(err => console.error('SW registration failed:', err));
  });
}

createRoot(document.getElementById("root")!).render(<App />);
