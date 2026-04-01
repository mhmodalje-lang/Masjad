import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";
import { VitePWA } from "vite-plugin-pwa";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  envPrefix: ['VITE_', 'REACT_APP_'],
  server: {
    host: "0.0.0.0",
    port: 3000,
    allowedHosts: true,
    hmr: {
      overlay: false,
    },
  },
  plugins: [
    react(),
    mode === "development" && componentTagger(),
    mode === "production" && VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["favicon.ico", "pwa-icon-48.png", "pwa-icon-72.png", "pwa-icon-96.png", "pwa-icon-128.png", "pwa-icon-144.png", "pwa-icon-152.png", "pwa-icon-192.png", "pwa-icon-384.png", "pwa-icon-512.png", "pwa-icon-maskable.png", "apple-touch-icon.png"],
      manifest: {
        name: "أذان وحكاية - رفيقك الروحي",
        short_name: "أذان وحكاية",
        description: "مواقيت الصلاة، القرآن الكريم، الأذكار، اتجاه القبلة، صُحبة والمزيد",
        theme_color: "#257a4d",
        background_color: "#f2ede6",
        display: "standalone",
        orientation: "portrait",
        dir: "rtl",
        lang: "ar",
        start_url: "/",
        scope: "/",
        icons: [
          {
            src: "/pwa-icon-48.png",
            sizes: "48x48",
            type: "image/png",
          },
          {
            src: "/pwa-icon-72.png",
            sizes: "72x72",
            type: "image/png",
          },
          {
            src: "/pwa-icon-96.png",
            sizes: "96x96",
            type: "image/png",
          },
          {
            src: "/pwa-icon-144.png",
            sizes: "144x144",
            type: "image/png",
          },
          {
            src: "/pwa-icon-192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "/pwa-icon-384.png",
            sizes: "384x384",
            type: "image/png",
          },
          {
            src: "/pwa-icon-512.png",
            sizes: "512x512",
            type: "image/png",
          },
          {
            src: "/pwa-icon-maskable.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable",
          },
        ],
        categories: ["lifestyle", "education"],
      },
      workbox: {
        skipWaiting: true,
        clientsClaim: true,
        navigateFallbackDenylist: [/^\/~oauth/],
        globPatterns: ["**/*.{js,css,html,ico,png,jpg,svg,woff2}"],
        importScripts: ['/sw-custom.js'],
        maximumFileSizeToCacheInBytes: 5 * 1024 * 1024, // 5 MB limit
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\.alquran\.cloud\/.*/i,
            handler: "CacheFirst",
            options: {
              cacheName: "quran-api-cache",
              expiration: {
                maxEntries: 200,
                maxAgeSeconds: 60 * 60 * 24 * 30, // 30 days
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: /^https:\/\/api\.aladhan\.com\/.*/i,
            handler: "NetworkFirst",
            options: {
              cacheName: "prayer-times-cache",
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 3, // 3 hours
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
            handler: "CacheFirst",
            options: {
              cacheName: "google-fonts-cache",
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 365, // 1 year
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
            handler: "CacheFirst",
            options: {
              cacheName: "google-fonts-files",
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 365,
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
        ],
      },
    }),
  ].filter(Boolean),
  optimizeDeps: {
    include: [
      'react', 'react-dom', 'react-router-dom', 'react/jsx-runtime',
      'framer-motion', 'lucide-react', 'sonner', 'next-themes',
      '@tanstack/react-query', 'i18next', 'react-i18next', 'i18next-browser-languagedetector',
      'class-variance-authority', 'clsx', 'tailwind-merge',
      '@radix-ui/react-accordion', '@radix-ui/react-alert-dialog',
      '@radix-ui/react-avatar', '@radix-ui/react-checkbox',
      '@radix-ui/react-collapsible', '@radix-ui/react-dialog',
      '@radix-ui/react-dropdown-menu', '@radix-ui/react-label',
      '@radix-ui/react-popover', '@radix-ui/react-progress',
      '@radix-ui/react-radio-group', '@radix-ui/react-scroll-area',
      '@radix-ui/react-select', '@radix-ui/react-separator',
      '@radix-ui/react-slider', '@radix-ui/react-slot',
      '@radix-ui/react-switch', '@radix-ui/react-tabs',
      '@radix-ui/react-toast', '@radix-ui/react-toggle',
      '@radix-ui/react-toggle-group', '@radix-ui/react-tooltip',
      '@hookform/resolvers', 'react-hook-form', 'zod',
      'date-fns', 'recharts', 'vaul', 'cmdk', 'input-otp',
      'embla-carousel-react', 'react-day-picker', 'react-resizable-panels',
      '@capacitor/core', '@capacitor/app', '@capacitor/haptics',
      '@capacitor/share', '@capacitor/browser', '@capacitor/device',
      '@capacitor/geolocation', '@capacitor/keyboard', '@capacitor/network',
      '@capacitor/preferences', '@capacitor/splash-screen', '@capacitor/status-bar',
      'adhan', 'leaflet', 'lottie-react',
      'firebase/app', 'firebase/auth', 'firebase/analytics',
    ],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
    dedupe: ["react", "react-dom", "react/jsx-runtime"],
  },
  build: {
    chunkSizeWarningLimit: 3000,
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          'vendor-ui': ['framer-motion', '@radix-ui/react-dialog', '@radix-ui/react-tabs', '@radix-ui/react-select'],
          'vendor-query': ['@tanstack/react-query'],
          'vendor-i18n': ['i18next', 'react-i18next'],
          'vendor-capacitor': ['@capacitor/core', '@capacitor/app', '@capacitor/haptics', '@capacitor/share'],
        },
      },
    },
  },
}));
