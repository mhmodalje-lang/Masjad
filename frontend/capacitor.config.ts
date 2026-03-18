import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.azanwahikaya.app',
  appName: 'أذان وحكاية',
  webDir: 'dist',
  server: {
    // For production: comment out url to use local assets
    // url: 'https://your-production-url.com',
    cleartext: false,
  },
  android: {
    allowMixedContent: false,
    minWebViewVersion: '95.0',
    // AdMob Configuration
    // Add in AndroidManifest.xml:
    // <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" 
    //            android:value="ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY"/>
  },
  ios: {
    // AdMob Configuration
    // Add GADApplicationIdentifier in Info.plist
    // with your AdMob App ID
    scheme: 'أذان وحكاية',
    contentInset: 'automatic',
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      launchAutoHide: true,
      backgroundColor: '#0c1a14',
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
      showSpinner: false,
      splashFullScreen: true,
      splashImmersive: true,
    },
    StatusBar: {
      style: 'DARK',
      backgroundColor: '#064e3b',
    },
    PushNotifications: {
      presentationOptions: ['badge', 'sound', 'alert'],
    },
    Keyboard: {
      resize: 'body',
      style: 'DARK',
    },
  },
};

export default config;
