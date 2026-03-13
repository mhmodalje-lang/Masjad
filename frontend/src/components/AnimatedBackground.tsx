import Lottie from 'lottie-react';
import { useEffect, useState } from 'react';

// Animated gradient circles (pure CSS - always works, no external dependency)
export function AnimatedBackground({ variant = 'default' }: { variant?: 'islamic' | 'marketplace' | 'prayer' | 'default' }) {
  const colors = {
    islamic: ['bg-emerald-500/10', 'bg-teal-500/8', 'bg-green-500/6'],
    marketplace: ['bg-amber-500/10', 'bg-orange-500/8', 'bg-yellow-500/6'],
    prayer: ['bg-blue-500/10', 'bg-cyan-500/8', 'bg-sky-500/6'],
    default: ['bg-primary/10', 'bg-accent/8', 'bg-primary/5'],
  };

  const c = colors[variant];

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      <div className={`absolute -top-1/2 -right-1/2 w-full h-full rounded-full ${c[0]} blur-3xl animate-pulse`} style={{ animationDuration: '4s' }} />
      <div className={`absolute -bottom-1/3 -left-1/3 w-2/3 h-2/3 rounded-full ${c[1]} blur-3xl animate-pulse`} style={{ animationDuration: '6s', animationDelay: '1s' }} />
      <div className={`absolute top-1/4 left-1/4 w-1/2 h-1/2 rounded-full ${c[2]} blur-3xl animate-pulse`} style={{ animationDuration: '5s', animationDelay: '2s' }} />
      
      {/* Floating geometric Islamic pattern */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.04]" xmlns="http://www.w3.org/2000/svg">
        <pattern id={`pat-${variant}`} x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
          <path d="M30 0L37 15H23zM0 30L15 37V23zM60 30L45 23V37zM30 60L23 45H37z" fill="currentColor" className="text-foreground" />
        </pattern>
        <rect width="100%" height="100%" fill={`url(#pat-${variant})`} />
      </svg>
    </div>
  );
}

// Lottie animation wrapper with fallback
const LOTTIE_URLS: Record<string, string> = {
  mosque: 'https://lottie.host/c7abfc45-93bb-4e68-befe-d5c2b48e2ac3/QWYfFtqR0t.json',
  shopping: 'https://lottie.host/fa2ee9f8-8c1e-4e1e-8899-2b54d6ba0b6f/WsZVXSZhXP.json',
  stars: 'https://lottie.host/b03d46ef-27a6-48c0-8cd5-17bc0d31e0c9/JbLFUveMJq.json',
  chat: 'https://lottie.host/e84ae2f1-5f8c-430a-a2f6-0ac1e3c8bcf0/VaGM3JIZCn.json',
};

export function LottieIcon({ name, className = 'h-20 w-20' }: { name: string; className?: string }) {
  const [data, setData] = useState<any>(null);
  
  useEffect(() => {
    const url = LOTTIE_URLS[name];
    if (url) {
      fetch(url).then(r => r.json()).then(setData).catch(() => {});
    }
  }, [name]);

  if (!data) return null;

  return (
    <div className={className}>
      <Lottie animationData={data} loop autoplay style={{ width: '100%', height: '100%' }} />
    </div>
  );
}
