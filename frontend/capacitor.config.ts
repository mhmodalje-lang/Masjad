import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.azanwahikaya.app',
  appName: 'أذان وحكاية',
  webDir: 'dist',

  // ═══ Server Configuration ═══
  server: {
    // Use HTTPS scheme for secure content loading
    androidScheme: 'https',
    iosScheme: 'https',
    // Block mixed content for security
    cleartext: false,
    // Allow navigation to specific external domains only
    allowNavigation: [
      'https://api.alquran.cloud',
      'https://api.aladhan.com',
      'https://api.quran.com',
      'https://fonts.googleapis.com',
      'https://fonts.gstatic.com',
    ],
  },

  // ═══ Android Configuration ═══
  android: {
    allowMixedContent: false,
    // Minimum WebView version for modern features
    minWebViewVersion: '95.0',
    // Enable hardware acceleration
    backgroundColor: '#064e3b',
    // Override user agent to avoid "web wrapper" detection
    overrideUserAgent: 'AzanHikaya/1.0 Android',
    // Append to user agent instead of full override
    appendUserAgent: 'AzanHikaya/1.0',
    // Build options
    buildOptions: {
      keystorePath: undefined,
      keystoreAlias: undefined,
    },
  },

  // ═══ iOS Configuration ═══
  ios: {
    scheme: 'AzanHikaya',
    contentInset: 'automatic',
    backgroundColor: '#064e3b',
    // Override user agent
    overrideUserAgent: 'AzanHikaya/1.0 iOS',
    appendUserAgent: 'AzanHikaya/1.0',
    // Prefer this for proper scrolling behavior
    scrollEnabled: true,
    // Allow inline media playback (required for audio features like Athan)
    allowsLinkPreview: false,
  },

  // ═══ Plugins Configuration ═══
  plugins: {
    // Splash Screen - Native splash screen (not web)
    SplashScreen: {
      launchShowDuration: 2000,
      launchAutoHide: false, // We control hiding from JS
      launchFadeOutDuration: 300,
      backgroundColor: '#064e3b',
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
      showSpinner: false,
      splashFullScreen: true,
      splashImmersive: true,
      // iOS specific
      iosSpinnerStyle: 'small',
      spinnerColor: '#d4a843',
    },

    // Status Bar
    StatusBar: {
      style: 'DARK',
      backgroundColor: '#064e3b',
      overlaysWebView: false,
    },

    // Push Notifications
    PushNotifications: {
      presentationOptions: ['badge', 'sound', 'alert'],
    },

    // Keyboard - Handle keyboard properly
    Keyboard: {
      resize: 'body',
      style: 'DARK',
      resizeOnFullScreen: true,
    },

    // Local Notifications - For prayer times
    LocalNotifications: {
      smallIcon: 'ic_stat_mosque',
      iconColor: '#10b981',
      sound: 'athan_default.mp3',
    },

    // Haptics
    Haptics: {},

    // Network
    Network: {},

    // Geolocation - For Qibla & Prayer Times
    Geolocation: {
      // Only request when needed
    },

    // Preferences (Native Storage)
    Preferences: {},

    // Browser - For external links
    Browser: {
      // Open external links in in-app browser
    },

    // Share - Native share sheet
    Share: {},

    // Device
    Device: {},
  },
};

export default config;
