import React, { useState, useEffect, useCallback } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface IslamicAdProps {
  placement?: string;
  variant?: 'card' | 'banner' | 'inline';
  className?: string;
}

/**
 * Islamic Sponsored Content Component
 * ====================================
 * Self-hosted halal content system. Fetches real Islamic sponsored 
 * content from backend (books, courses, charities, products).
 * Awards blessing coins when users interact.
 * NO 3rd party ad networks. NO policy violations.
 */
export default function IslamicAd({ placement = 'main', variant = 'card', className }: IslamicAdProps) {
  const { locale, dir } = useLocale();
  const [ad, setAd] = useState<any>(null);
  const [clicked, setClicked] = useState(false);
  const [coinsEarned, setCoinsEarned] = useState(0);

  useEffect(() => {
    const fetchAd = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/ads/content?placement=${placement}&locale=${locale}&limit=1`);
        const data = await res.json();
        if (data.success && data.ads.length > 0) {
          setAd(data.ads[0]);
        }
      } catch (e) { /* silent */ }
    };
    fetchAd();
  }, [placement, locale]);

  const handleClick = useCallback(async () => {
    if (!ad || clicked) return;
    setClicked(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/ads/click/${ad.id}?user_id=guest`, { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        setCoinsEarned(data.coins_awarded);
        setTimeout(() => { setCoinsEarned(0); setClicked(false); }, 3000);
      }
    } catch (e) { setClicked(false); }
  }, [ad, clicked]);

  if (!ad) return null;

  // ═══ BANNER VARIANT ═══
  if (variant === 'banner') {
    return (
      <div dir={dir} onClick={handleClick} className={cn(
        "w-full px-4 py-3 rounded-2xl border cursor-pointer transition-all hover:scale-[1.01] active:scale-[0.99] relative overflow-hidden",
        "border-border/20",
        className
      )} style={{ background: `linear-gradient(135deg, ${ad.color}12, ${ad.color}06)`, borderColor: `${ad.color}25` }}>
        {coinsEarned > 0 && (
          <div className="absolute inset-0 bg-emerald-500/10 flex items-center justify-center z-10 animate-in fade-in">
            <span className="text-sm font-bold text-emerald-300">+{coinsEarned} 🪙</span>
          </div>
        )}
        <div className="flex items-center gap-3">
          <span className="text-2xl">{ad.emoji}</span>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold text-foreground truncate">{ad.title}</p>
            <p className="text-xs text-foreground/60 truncate">{ad.description}</p>
          </div>
          <span className="px-3 py-1.5 rounded-lg text-xs font-bold text-white shrink-0" style={{ backgroundColor: ad.color }}>{ad.cta}</span>
        </div>
      </div>
    );
  }

  // ═══ INLINE VARIANT ═══
  if (variant === 'inline') {
    return (
      <div dir={dir} onClick={handleClick} className={cn(
        "px-4 py-3 rounded-xl cursor-pointer transition-all hover:scale-[1.01] active:scale-[0.99] relative overflow-hidden",
        className
      )} style={{ background: `linear-gradient(135deg, ${ad.color}10, transparent)` }}>
        {coinsEarned > 0 && (
          <div className="absolute inset-0 bg-emerald-500/10 flex items-center justify-center z-10">
            <span className="text-sm font-bold text-emerald-300">+{coinsEarned} 🪙</span>
          </div>
        )}
        <div className="flex items-center gap-2">
          <span className="text-lg">{ad.emoji}</span>
          <p className="text-sm font-medium text-foreground/80 flex-1 truncate">{ad.title}</p>
          <span className="text-xs font-bold px-2 py-1 rounded-md" style={{ color: ad.color, backgroundColor: `${ad.color}15` }}>{ad.cta}</span>
        </div>
      </div>
    );
  }

  // ═══ CARD VARIANT (default) ═══
  return (
    <div dir={dir} onClick={handleClick} className={cn(
      "w-full p-4 rounded-2xl border cursor-pointer transition-all hover:scale-[1.01] active:scale-[0.99] relative overflow-hidden",
      "bg-card/60 border-border/30 shadow-sm",
      className
    )} style={{ borderColor: `${ad.color}25` }}>
      {coinsEarned > 0 && (
        <div className="absolute inset-0 bg-emerald-500/10 backdrop-blur-sm flex items-center justify-center z-10 animate-in fade-in">
          <div className="text-center">
            <span className="text-3xl">🪙</span>
            <p className="text-lg font-bold text-emerald-300 mt-1">+{coinsEarned}</p>
          </div>
        </div>
      )}
      <div className="flex items-start gap-3">
        <div className="w-14 h-14 rounded-xl flex items-center justify-center text-2xl shrink-0"
             style={{ background: `linear-gradient(135deg, ${ad.color}25, ${ad.color}10)` }}>
          {ad.emoji}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-base font-bold text-foreground">{ad.title}</p>
          <p className="text-sm text-foreground/60 mt-1 line-clamp-2">{ad.description}</p>
          <button className="mt-3 px-4 py-2 rounded-xl text-xs font-bold text-white transition-all hover:opacity-90"
                  style={{ backgroundColor: ad.color }}>
            {ad.cta} →
          </button>
        </div>
      </div>
    </div>
  );
}
