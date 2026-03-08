// Athan audio sources - free publicly available athan recordings
export interface AthanOption {
  id: string;
  name: string;
  nameAr: string;
  url: string;
  fajrUrl?: string; // Some muezzins have a different Fajr athan
}

export const ATHAN_OPTIONS: AthanOption[] = [
  {
    id: 'makkah',
    name: 'Makkah',
    nameAr: 'أذان مكة المكرمة',
    url: 'https://cdn.aladhan.com/audio/adhans/1.mp3',
    fajrUrl: 'https://cdn.aladhan.com/audio/adhans/1.mp3',
  },
  {
    id: 'madinah',
    name: 'Madinah',
    nameAr: 'أذان المدينة المنورة',
    url: 'https://cdn.aladhan.com/audio/adhans/2.mp3',
  },
  {
    id: 'alaqsa',
    name: 'Al-Aqsa',
    nameAr: 'أذان المسجد الأقصى',
    url: 'https://cdn.aladhan.com/audio/adhans/3.mp3',
  },
  {
    id: 'egypt',
    name: 'Egypt',
    nameAr: 'أذان مصري',
    url: 'https://cdn.aladhan.com/audio/adhans/4.mp3',
  },
  {
    id: 'mishary',
    name: 'Mishary Rashid',
    nameAr: 'مشاري راشد العفاسي',
    url: 'https://cdn.aladhan.com/audio/adhans/5.mp3',
  },
  {
    id: 'default',
    name: 'Simple Beep',
    nameAr: 'تنبيه بسيط',
    url: '', // Will use browser notification sound only
  },
];

export function getSelectedAthan(): AthanOption {
  const id = localStorage.getItem('athan-sound') || 'makkah';
  return ATHAN_OPTIONS.find(a => a.id === id) || ATHAN_OPTIONS[0];
}

export function setSelectedAthan(id: string) {
  localStorage.setItem('athan-sound', id);
}

let currentAudio: HTMLAudioElement | null = null;

export function playAthan(prayerKey?: string): HTMLAudioElement | null {
  stopAthan();
  
  const athan = getSelectedAthan();
  if (!athan.url) return null; // Simple beep mode - notification only
  
  const url = (prayerKey === 'fajr' && athan.fajrUrl) ? athan.fajrUrl : athan.url;
  
  currentAudio = new Audio(url);
  currentAudio.volume = parseFloat(localStorage.getItem('athan-volume') || '0.8');
  currentAudio.play().catch(() => {
    // Autoplay blocked - will rely on notification only
  });
  
  return currentAudio;
}

export function stopAthan() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio = null;
  }
}

export function previewAthan(id: string) {
  stopAthan();
  const athan = ATHAN_OPTIONS.find(a => a.id === id);
  if (!athan?.url) return null;
  
  currentAudio = new Audio(athan.url);
  currentAudio.volume = parseFloat(localStorage.getItem('athan-volume') || '0.8');
  currentAudio.play().catch(() => {});
  
  // Stop preview after 15 seconds
  setTimeout(() => stopAthan(), 15000);
  return currentAudio;
}
