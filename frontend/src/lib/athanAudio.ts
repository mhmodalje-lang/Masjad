// Athan audio sources - local files for reliability
export interface AthanOption {
  id: string;
  name: string;
  nameAr: string;
  url: string;
  fajrUrl?: string;
}

export const ATHAN_OPTIONS: AthanOption[] = [
  { id: 'makkah', name: 'Makkah', nameAr: 'أذان مكة المكرمة', url: '/audio/athan/makkah.mp3' },
  { id: 'madinah', name: 'Madinah', nameAr: 'أذان المدينة المنورة', url: '/audio/athan/madinah.mp3' },
  { id: 'turkish', name: 'Turkish Athan', nameAr: 'الأذان التركي', url: '/audio/athan/turkish.mp3' },
  { id: 'umayyad', name: 'Umayyad Mosque (Damascus)', nameAr: 'الجامع الأموي (دمشق)', url: '/audio/athan/umayyad.mp3' },
  { id: 'quds', name: 'Al-Aqsa Mosque (Jerusalem)', nameAr: 'المسجد الأقصى (القدس)', url: '/audio/athan/quds.mp3', fajrUrl: '/audio/athan/quds-fajr.mp3' },
  { id: 'abdulbasit', name: 'Abdul Basit Abdul Samad', nameAr: 'عبد الباسط عبد الصمد', url: '/audio/athan/abdulbasit.mp3' },
  { id: 'shahat', name: 'Shahat Anwar', nameAr: 'شحات محمد أنور', url: '/audio/athan/shahat.mp3', fajrUrl: '/audio/athan/shahat-fajr.mp3' },
  { id: 'saqqaf', name: 'Al-Saqqaf', nameAr: 'السقاف', url: '/audio/athan/saqqaf.mp3', fajrUrl: '/audio/athan/saqqaf-fajr.mp3' },
  { id: 'default', name: 'Simple Beep', nameAr: 'تنبيه بسيط', url: '' },
];

// ==================== SOUND MODE ====================
// Sound modes: 'sound' = always play, 'vibrate' = vibrate only, 'silent' = no sound/vibrate, 'auto' = follow device
export type AthanSoundMode = 'sound' | 'vibrate' | 'silent' | 'auto';

export function getAthanSoundMode(): AthanSoundMode {
  return (localStorage.getItem('athan-sound-mode') as AthanSoundMode) || 'auto';
}

export function setAthanSoundMode(mode: AthanSoundMode) {
  localStorage.setItem('athan-sound-mode', mode);
}

/**
 * Detect if the device is effectively in a silent/muted state.
 * Uses AudioContext to check if audio output is possible.
 * This is a best-effort detection for web apps.
 */
export async function isDeviceEffectivelySilent(): Promise<boolean> {
  try {
    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioCtx) return false;

    const ctx = new AudioCtx();

    // If AudioContext is suspended, audio won't play (no user gesture or blocked)
    if (ctx.state === 'suspended') {
      try { await ctx.resume(); } catch { /* ignore */ }
      // If still suspended after resume attempt, consider it silent
      if (ctx.state === 'suspended') {
        ctx.close();
        return true;
      }
    }

    // iOS silent switch detection technique:
    // Create a short oscillator and measure if it produces actual output
    const osc = ctx.createOscillator();
    const analyser = ctx.createAnalyser();
    const gain = ctx.createGain();
    gain.gain.value = 0.001; // Near-inaudible
    analyser.fftSize = 256;

    osc.connect(gain);
    gain.connect(analyser);
    analyser.connect(ctx.destination);
    osc.frequency.value = 200;
    osc.start();

    // Wait for audio pipeline to process
    await new Promise(resolve => setTimeout(resolve, 150));

    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteTimeDomainData(dataArray);

    // Check if all values are at silence level (128 = silence in time domain)
    const allSilent = dataArray.every(v => v >= 126 && v <= 130);

    osc.stop();
    ctx.close();

    // If the analyser shows all silence, the device might be muted
    // However, this is not 100% reliable - some devices still show data
    return allSilent;
  } catch {
    return false;
  }
}

/**
 * Determine if athan audio should play based on the sound mode setting.
 * Returns true if audio should play, false if it should be skipped.
 */
export async function shouldPlayAthanAudio(): Promise<boolean> {
  const mode = getAthanSoundMode();
  if (mode === 'sound') return true;
  if (mode === 'silent' || mode === 'vibrate') return false;

  // Auto mode: try to detect device state
  const isSilent = await isDeviceEffectivelySilent();
  return !isSilent;
}

/**
 * Determine if the device should vibrate for athan.
 */
export function shouldVibrateForAthan(): boolean {
  const mode = getAthanSoundMode();
  if (mode === 'silent') return false;
  return true; // vibrate in 'sound', 'vibrate', and 'auto' modes
}

/**
 * Vibrate the device for athan notification.
 */
export function vibrateForAthan() {
  if (!shouldVibrateForAthan()) return;
  try {
    if ('vibrate' in navigator) {
      // Long vibration pattern for prayer time
      navigator.vibrate([400, 200, 400, 200, 400, 300, 600]);
    }
  } catch { /* vibration not supported */ }
}

export function getSelectedAthan(): AthanOption {
  const id = localStorage.getItem('athan-sound') || 'makkah';
  return ATHAN_OPTIONS.find(a => a.id === id) || ATHAN_OPTIONS[0];
}

export function setSelectedAthan(id: string) {
  localStorage.setItem('athan-sound', id);
}

let currentAudio: HTMLAudioElement | null = null;
const preloadedAudios = new Map<string, HTMLAudioElement>();

/** Stop ALL audio - global kill switch */
function killAllAudio() {
  // Stop currentAudio
  if (currentAudio) {
    try { currentAudio.pause(); currentAudio.currentTime = 0; } catch {}
    currentAudio = null;
  }
  // Also pause any preloaded audios that might be playing
  preloadedAudios.forEach((audio) => {
    try {
      if (!audio.paused) {
        audio.pause();
        audio.currentTime = 0;
      }
    } catch {}
  });
}

function getSavedVolume() {
  return parseFloat(localStorage.getItem('athan-volume') || '0.8');
}

function ensureAudio(url: string): HTMLAudioElement {
  const existing = preloadedAudios.get(url);
  if (existing) return existing;
  const audio = new Audio();
  audio.preload = 'auto';
  audio.src = url;
  audio.load();
  preloadedAudios.set(url, audio);
  return audio;
}

export function preloadAthanById(id: string, _highPriority: boolean = false) {
  const athan = ATHAN_OPTIONS.find(a => a.id === id);
  if (!athan) return;
  if (athan.url) ensureAudio(athan.url);
  if (athan.fajrUrl) ensureAudio(athan.fajrUrl);
}

export function preloadSelectedAthan(_highPriority: boolean = false) {
  const athan = getSelectedAthan();
  if (athan.url) ensureAudio(athan.url);
  if (athan.fajrUrl) ensureAudio(athan.fajrUrl);
}

export function preloadAllAthans() {
  for (const athan of ATHAN_OPTIONS) {
    if (athan.url) ensureAudio(athan.url);
    if (athan.fajrUrl) ensureAudio(athan.fajrUrl);
  }
}

function createAndPlayAudio(url: string): HTMLAudioElement {
  const audio = new Audio(url);
  audio.volume = getSavedVolume();

  // ══ CRITICAL: Override Media Session so Athan doesn't appear as "song" ══
  if ('mediaSession' in navigator) {
    try {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: '🕌 الأذان',
        artist: 'أذان وحكاية',
        album: 'صلاة',
        artwork: [
          { src: '/pwa-icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/pwa-icon-512.png', sizes: '512x512', type: 'image/png' },
        ]
      });
      navigator.mediaSession.setActionHandler('play', () => { audio.play(); });
      navigator.mediaSession.setActionHandler('pause', () => { stopAthan(); });
      navigator.mediaSession.setActionHandler('stop', () => { stopAthan(); });
    } catch {}
  }

  audio.onerror = (e) => {
    console.warn('Athan audio failed:', url, e);
    if (currentAudio === audio) currentAudio = null;
  };
  audio.onended = () => {
    if (currentAudio === audio) currentAudio = null;
    // Clear media session when done
    if ('mediaSession' in navigator) {
      try { navigator.mediaSession.metadata = null; } catch {}
    }
  };

  audio.play().catch(err => {
    console.warn('Athan play blocked:', err.message);
    if (currentAudio === audio) currentAudio = null;
  });

  return audio;
}

export function playAthan(prayerKey?: string): HTMLAudioElement | null {
  stopAthan();

  const mode = getAthanSoundMode();

  // If mode is silent - no audio, no vibration
  if (mode === 'silent') {
    console.log('[Athan] Silent mode — skipping audio');
    return null;
  }

  // If mode is vibrate - vibrate only, no audio
  if (mode === 'vibrate') {
    console.log('[Athan] Vibrate mode — vibrating only');
    vibrateForAthan();
    return null;
  }

  // Auto mode: check device state asynchronously
  if (mode === 'auto') {
    // Start async detection, play immediately but stop if device is silent
    shouldPlayAthanAudio().then(shouldPlay => {
      if (!shouldPlay) {
        console.log('[Athan] Auto mode detected silent device — stopping audio, vibrating');
        stopAthan();
        vibrateForAthan();
      }
    });
  }

  // Sound mode or auto mode (optimistically play) 
  const athan = getSelectedAthan();
  if (!athan.url) {
    playBeep();
    vibrateForAthan();
    return null;
  }
  const url = prayerKey === 'fajr' && athan.fajrUrl ? athan.fajrUrl : athan.url;
  currentAudio = createAndPlayAudio(url);
  vibrateForAthan();
  return currentAudio;
}

export function stopAthan() {
  killAllAudio();
}

export function previewAthan(id: string): HTMLAudioElement | null {
  stopAthan();
  const athan = ATHAN_OPTIONS.find(a => a.id === id);
  if (!athan?.url) return null;
  currentAudio = createAndPlayAudio(athan.url);
  return currentAudio;
}

/** Test athan playback - returns true if audio started */
export function testAthanPlayback(): boolean {
  stopAthan();

  const mode = getAthanSoundMode();
  
  // For test, if silent or vibrate mode, inform user
  if (mode === 'silent') {
    console.log('[Athan Test] Silent mode active — no audio');
    return false;
  }
  if (mode === 'vibrate') {
    vibrateForAthan();
    console.log('[Athan Test] Vibrate mode — vibrating only');
    return true;
  }

  const athan = getSelectedAthan();
  if (!athan.url) {
    playBeep();
    return true;
  }
  const audio = createAndPlayAudio(athan.url);
  if (audio) {
    // Stop after 5 seconds for test
    setTimeout(() => {
      if (currentAudio === audio) {
        stopAthan();
      }
    }, 5000);
    return true;
  }
  return false;
}

/** Simple beep for the "default" option */
function playBeep() {
  try {
    const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    const vol = getSavedVolume();
    osc.frequency.setValueAtTime(800, ctx.currentTime);
    gain.gain.setValueAtTime(vol * 0.6, ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0, ctx.currentTime + 1);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 1);
    setTimeout(() => ctx.close(), 2000);
  } catch {}
}

// Preload selected athan on module load
preloadSelectedAthan(true);

// Only preload all athans when user opens settings, not on startup
if (typeof window !== 'undefined') {
  const warmSelected = () => preloadSelectedAthan(true);
  if ('requestIdleCallback' in window) {
    (window as any).requestIdleCallback(warmSelected, { timeout: 3000 });
  } else {
    globalThis.setTimeout(warmSelected, 2000);
  }
}
