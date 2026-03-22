import React, { useState, useEffect, useCallback } from 'react';
import { BookOpen, ExternalLink, Sparkles } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

// ═══ 10-Language Translations for Sponsored Content ═══
const AD_TRANSLATIONS: Record<string, Record<string, string>> = {
  "sponsored_wisdom": {
    ar: "حكمة مختارة",
    en: "Selected Wisdom",
    de: "Ausgewählte Weisheit",
    "de-AT": "Ausgewählte Weisheit",
    fr: "Sagesse sélectionnée",
    tr: "Seçilmiş Hikmet",
    ru: "Избранная мудрость",
    sv: "Utvald visdom",
    nl: "Geselecteerde wijsheid",
    el: "Επιλεγμένη σοφία"
  },
  "sponsored": {
    ar: "محتوى مدعوم",
    en: "Sponsored",
    de: "Gesponsert",
    "de-AT": "Gesponsert",
    fr: "Sponsorisé",
    tr: "Sponsorlu",
    ru: "Спонсируется",
    sv: "Sponsrad",
    nl: "Gesponsord",
    el: "Χορηγούμενο"
  },
  "learn_more": {
    ar: "اعرف المزيد",
    en: "Learn More",
    de: "Mehr erfahren",
    "de-AT": "Mehr erfahren",
    fr: "En savoir plus",
    tr: "Daha fazla",
    ru: "Узнать больше",
    sv: "Läs mer",
    nl: "Meer lezen",
    el: "Μάθετε περισσότερα"
  },
  "coins_earned": {
    ar: "حصلت على عملات!",
    en: "Coins earned!",
    de: "Münzen verdient!",
    "de-AT": "Münzen verdient!",
    fr: "Pièces gagnées !",
    tr: "Para kazanıldı!",
    ru: "Монеты получены!",
    sv: "Mynt tjänade!",
    nl: "Munten verdiend!",
    el: "Κέρδισες νομίσματα!"
  },
};

interface NativeAdCardProps {
  className?: string;
  placement?: string;
}

/**
 * NativeAdCard — Mimics DailyHadith design exactly.
 * Same rounded-3xl, bg-card, border, amber badge, font styles, shadow.
 * Fetches real Islamic sponsored content from backend.
 * Awards blessing coins when users interact (like DailyHadith share).
 * 
 * In production: Replace with AdMob Native Advanced template
 * that uses the same design tokens.
 */
export default function NativeAdCard({ className, placement = 'hadith_feed' }: NativeAdCardProps) {
  const { locale, dir } = useLocale();
  const lang = locale || 'ar';
  const [ad, setAd] = useState<any>(null);
  const [clicked, setClicked] = useState(false);
  const [coinsEarned, setCoinsEarned] = useState(0);
  const [loading, setLoading] = useState(true);

  const t = useCallback((key: string) => {
    return AD_TRANSLATIONS[key]?.[lang] || AD_TRANSLATIONS[key]?.['en'] || key;
  }, [lang]);

  useEffect(() => {
    const fetchAd = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/ads/content?placement=${placement}&locale=${locale}&limit=1`);
        const data = await res.json();
        if (data.success && data.ads?.length > 0) {
          setAd(data.ads[0]);
        }
      } catch {
        // Silent fail — card just won't show
      } finally {
        setLoading(false);
      }
    };
    fetchAd();
  }, [placement, locale]);

  const handleClick = useCallback(async () => {
    if (!ad || clicked) return;
    setClicked(true);

    // Haptic feedback on interaction
    if (navigator.vibrate) {
      navigator.vibrate(30);
    }

    try {
      const res = await fetch(`${BACKEND_URL}/api/ads/click/${ad.id}?user_id=guest`, { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        setCoinsEarned(data.coins_awarded || 1);
        setTimeout(() => {
          setCoinsEarned(0);
          setClicked(false);
        }, 3000);
      }
    } catch {
      setClicked(false);
    }
  }, [ad, clicked]);

  // Don't show if loading or no ad
  if (loading || !ad) return null;

  return (
    <div className={cn("px-4 mb-4", className)} dir={dir}>
      <div
        onClick={handleClick}
        className="rounded-3xl bg-card border border-border/40 p-5 shadow-elevated relative overflow-hidden cursor-pointer transition-all hover:scale-[1.005] active:scale-[0.995]"
      >
        {/* Decorative corner gradient — same as DailyHadith */}
        <div className="absolute top-0 left-0 w-32 h-32 bg-gradient-to-br from-amber-500/5 to-transparent rounded-br-full" />

        {/* Coins earned overlay */}
        {coinsEarned > 0 && (
          <div className="absolute inset-0 bg-emerald-500/10 backdrop-blur-[2px] flex items-center justify-center z-20 animate-in fade-in rounded-3xl">
            <div className="text-center">
              <span className="text-3xl">🪙</span>
              <p className="text-lg font-bold text-emerald-400 mt-1">+{coinsEarned}</p>
              <p className="text-xs text-emerald-300/70">{t('coins_earned')}</p>
            </div>
          </div>
        )}

        {/* Header badge — matches DailyHadith amber badge style */}
        <div className="flex items-center justify-between mb-4 relative">
          <span className="inline-flex items-center gap-2 rounded-full bg-amber-500/10 border border-amber-500/20 px-3 py-1 text-[11px] font-bold text-amber-600 dark:text-amber-400">
            <Sparkles className="h-3 w-3" />
            {t('sponsored_wisdom')}
          </span>
          <span className="text-[9px] px-2 py-0.5 rounded-full bg-muted/30 text-muted-foreground/50 font-medium">
            {t('sponsored')}
          </span>
        </div>

        {/* Content — mimics hadith text style */}
        <p className="text-sm text-muted-foreground mb-2">{ad.emoji || '✨'}</p>

        {/* Arabic-style centered text like hadith */}
        <p className="text-lg font-arabic text-foreground leading-[2.2] text-center mb-3" dir="rtl">
          {ad.title}
        </p>

        <p className="text-sm text-muted-foreground leading-relaxed text-center mb-4 border-t border-border/20 pt-3" dir="auto">
          {ad.description}
        </p>

        {/* Footer — matches DailyHadith bottom bar style */}
        <div className="flex items-center justify-between text-xs text-muted-foreground border-t border-border/40 pt-3">
          <span className="flex items-center gap-1.5">
            <ExternalLink className="h-3 w-3" />
            {t('learn_more')}
          </span>
          <button
            className="px-3 py-1.5 rounded-lg text-xs font-bold text-white transition-all hover:opacity-90"
            style={{ backgroundColor: ad.color || '#d4a843' }}
          >
            {ad.cta || t('learn_more')} →
          </button>
        </div>
      </div>
    </div>
  );
}
