/**
 * Native Bridge - Platform detection and native feature utilities
 * Bridges web app with Capacitor native features
 * Provides graceful fallbacks when running as web app
 */

import { Capacitor } from '@capacitor/core';

// ═══ Platform Detection ═══
export function isNativeApp(): boolean {
  return Capacitor.isNativePlatform();
}

export function getPlatform(): 'ios' | 'android' | 'web' {
  return Capacitor.getPlatform() as 'ios' | 'android' | 'web';
}

export function isIOS(): boolean {
  return getPlatform() === 'ios';
}

export function isAndroid(): boolean {
  return getPlatform() === 'android';
}

// ═══ Haptic Feedback ═══
type HapticStyle = 'light' | 'medium' | 'heavy' | 'success' | 'warning' | 'error' | 'selection';

export async function hapticFeedback(style: HapticStyle = 'light'): Promise<void> {
  if (!isNativeApp()) return;
  try {
    const { Haptics, ImpactStyle, NotificationType } = await import('@capacitor/haptics');
    switch (style) {
      case 'light':
        await Haptics.impact({ style: ImpactStyle.Light });
        break;
      case 'medium':
        await Haptics.impact({ style: ImpactStyle.Medium });
        break;
      case 'heavy':
        await Haptics.impact({ style: ImpactStyle.Heavy });
        break;
      case 'success':
        await Haptics.notification({ type: NotificationType.Success });
        break;
      case 'warning':
        await Haptics.notification({ type: NotificationType.Warning });
        break;
      case 'error':
        await Haptics.notification({ type: NotificationType.Error });
        break;
      case 'selection':
        await Haptics.selectionStart();
        await Haptics.selectionChanged();
        await Haptics.selectionEnd();
        break;
    }
  } catch (e) {
    // Silently fail - haptics not available
  }
}

// ═══ Native Share ═══
export async function nativeShare(data: { title?: string; text?: string; url?: string; }): Promise<boolean> {
  if (isNativeApp()) {
    try {
      const { Share } = await import('@capacitor/share');
      await Share.share(data);
      return true;
    } catch { return false; }
  }
  // Web fallback
  if (navigator.share) {
    try {
      await navigator.share(data);
      return true;
    } catch { return false; }
  }
  return false;
}

// ═══ Status Bar ═══
export async function configureStatusBar(isDark: boolean): Promise<void> {
  if (!isNativeApp()) return;
  try {
    const { StatusBar, Style } = await import('@capacitor/status-bar');
    await StatusBar.setStyle({ style: isDark ? Style.Dark : Style.Light });
    await StatusBar.setBackgroundColor({ color: isDark ? '#064e3b' : '#d4c4a0' });
    await StatusBar.setOverlaysWebView({ overlay: false });
  } catch { /* not available */ }
}

// ═══ Keyboard ═══
export async function hideKeyboard(): Promise<void> {
  if (!isNativeApp()) return;
  try {
    const { Keyboard } = await import('@capacitor/keyboard');
    await Keyboard.hide();
  } catch { /* not available */ }
}

// ═══ Network Status ═══
export async function getNetworkStatus(): Promise<{ connected: boolean; connectionType: string }> {
  if (!isNativeApp()) {
    return { connected: navigator.onLine, connectionType: 'unknown' };
  }
  try {
    const { Network } = await import('@capacitor/network');
    const status = await Network.getStatus();
    return { connected: status.connected, connectionType: status.connectionType };
  } catch {
    return { connected: navigator.onLine, connectionType: 'unknown' };
  }
}

// ═══ Native Preferences (faster than localStorage on native) ═══
export async function setNativePreference(key: string, value: string): Promise<void> {
  if (!isNativeApp()) {
    localStorage.setItem(key, value);
    return;
  }
  try {
    const { Preferences } = await import('@capacitor/preferences');
    await Preferences.set({ key, value });
  } catch {
    localStorage.setItem(key, value);
  }
}

export async function getNativePreference(key: string): Promise<string | null> {
  if (!isNativeApp()) {
    return localStorage.getItem(key);
  }
  try {
    const { Preferences } = await import('@capacitor/preferences');
    const { value } = await Preferences.get({ key });
    return value;
  } catch {
    return localStorage.getItem(key);
  }
}

// ═══ Device Info ═══
export async function getDeviceInfo() {
  if (!isNativeApp()) {
    return { platform: 'web' as const, model: navigator.userAgent, osVersion: '' };
  }
  try {
    const { Device } = await import('@capacitor/device');
    const info = await Device.getInfo();
    return { platform: info.platform, model: info.model, osVersion: info.osVersion };
  } catch {
    return { platform: 'web' as const, model: '', osVersion: '' };
  }
}

// ═══ App State ═══
export async function addAppStateListener(callback: (isActive: boolean) => void): Promise<() => void> {
  if (!isNativeApp()) {
    const handler = () => callback(document.visibilityState === 'visible');
    document.addEventListener('visibilitychange', handler);
    return () => document.removeEventListener('visibilitychange', handler);
  }
  try {
    const { App } = await import('@capacitor/app');
    const listener = await App.addListener('appStateChange', (state) => {
      callback(state.isActive);
    });
    return () => listener.remove();
  } catch {
    return () => {};
  }
}

// ═══ Back Button (Android) ═══
export async function addBackButtonListener(callback: () => void): Promise<() => void> {
  if (!isNativeApp() || !isAndroid()) return () => {};
  try {
    const { App } = await import('@capacitor/app');
    const listener = await App.addListener('backButton', () => {
      callback();
    });
    return () => listener.remove();
  } catch {
    return () => {};
  }
}

// ═══ Exit App (Android) ═══
export async function exitApp(): Promise<void> {
  if (!isNativeApp()) return;
  try {
    const { App } = await import('@capacitor/app');
    await App.exitApp();
  } catch { /* not available */ }
}

// ═══ Open Browser ═══
export async function openInBrowser(url: string): Promise<void> {
  if (!isNativeApp()) {
    window.open(url, '_blank');
    return;
  }
  try {
    const { Browser } = await import('@capacitor/browser');
    await Browser.open({ url });
  } catch {
    window.open(url, '_blank');
  }
}
