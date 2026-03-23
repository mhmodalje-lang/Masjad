import { useState, useEffect } from 'react';
import { BookOpen, Share2, Sparkles } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface HadithData {
  text: string;
  narrator: string;
  source: string;
  number: string;
  arabic_text?: string;
  arabic_narrator?: string;
  arabic_source?: string;
  translation_language?: string;
}

export default function DailyHadith() {
  const { t, locale } = useLocale();
  const [hadith, setHadith] = useState<HadithData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const cached = localStorage.getItem('daily-hadith-cache');
    const today = new Date().toISOString().split('T')[0];
    const cacheKey = `${today}-${locale}`;

    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        if (parsed.cacheKey === cacheKey && parsed.hadith) {
          setHadith(parsed.hadith);
          setLoading(false);
          return;
        }
      } catch {}
    }

    fetch(`${BACKEND_URL}/api/daily-hadith?language=${locale}`)
      .then(r => r.json())
      .then(data => {
        if (data.success && data.hadith) {
          setHadith(data.hadith);
          localStorage.setItem('daily-hadith-cache', JSON.stringify({ cacheKey, hadith: data.hadith }));
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [locale]);

  const handleShare = async () => {
    if (!hadith) return;
    const text = `${t('hadithShareTitle')}\n\n${t('prophetSaid')}\n«${hadith.text}»\n\n${t('narratorLabel')} ${hadith.narrator}\n${hadith.source}\n\n— ${t('appName')}`;
    if (navigator.share) {
      await navigator.share({ text }).catch(() => {});
    } else {
      await navigator.clipboard.writeText(text).catch(() => {});
    }
  };

  if (loading || !hadith) {
    return (
      <div className="px-4 mb-4">
        <div className="glass-mystic rounded-3xl p-6 shimmer-mystic">
          <div className="h-4 bg-muted/40 rounded-full w-28 mb-5" />
          <div className="h-5 bg-muted/30 rounded-full w-full mb-3" />
          <div className="h-5 bg-muted/30 rounded-full w-3/4 mx-auto" />
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 mb-4" data-testid="daily-hadith">
      {/* ═══ Glassmorphism 2.0 Card ═══ */}
      <div className="glass-mystic rounded-3xl p-6 relative overflow-hidden group transition-all duration-500 hover:shadow-float">
        {/* Decorative glow orbs */}
        <div className="absolute -top-8 -left-8 w-32 h-32 bg-[hsl(var(--islamic-green)/0.06)] rounded-full blur-2xl group-hover:bg-[hsl(var(--islamic-green)/0.1)] transition-all duration-700" />
        <div className="absolute -bottom-6 -right-6 w-24 h-24 bg-[hsl(var(--islamic-gold)/0.05)] rounded-full blur-2xl" />
        
        {/* Top bar: badge + share */}
        <div className="flex items-center justify-between mb-5 relative">
          <span className="inline-flex items-center gap-2 neu-pill px-4 py-1.5 text-[11px] font-bold text-[hsl(var(--mystic-amber))]">
            <Sparkles className="h-3.5 w-3.5" />
            {t('hadithOfDay')}
          </span>
          <button
            onClick={handleShare}
            className="p-2.5 rounded-xl glass-card hover:shadow-float transition-all duration-300 active:scale-90"
            data-testid="share-hadith-btn"
          >
            <Share2 className="h-4 w-4 text-muted-foreground" />
          </button>
        </div>

        {/* Prophet said label */}
        <p className="text-xs text-muted-foreground mb-3 tracking-wide font-medium uppercase">
          {t('prophetSaid')}
        </p>
        
        {/* Hadith text — elegant centered typography */}
        {hadith.translation_pending ? (
          <>
            <p className="text-lg font-arabic text-foreground leading-[2.4] text-center mb-4 px-2" dir="rtl">
              «{hadith.arabic_text || hadith.text}»
            </p>
            <div className="w-16 h-[1px] mx-auto bg-gradient-to-r from-transparent via-[hsl(var(--islamic-gold)/0.3)] to-transparent mb-3" />
            <div className="flex items-center justify-center gap-2 py-2 px-4 rounded-xl bg-amber-500/10 border border-amber-500/20 mx-4">
              <BookOpen className="h-3.5 w-3.5 text-amber-600" />
              <span className="text-xs font-bold text-amber-700 dark:text-amber-400">
                {t('hadithTranslationPending') || 'Translation Pending'}
              </span>
            </div>
          </>
        ) : hadith.arabic_text ? (
          <>
            <p className="text-lg font-arabic text-foreground leading-[2.4] text-center mb-4 px-2" dir="rtl">
              «{hadith.arabic_text}»
            </p>
            <div className="w-16 h-[1px] mx-auto bg-gradient-to-r from-transparent via-[hsl(var(--islamic-gold)/0.3)] to-transparent mb-4" />
            <p className="text-sm text-muted-foreground leading-relaxed text-center mb-4 px-2" dir="auto">
              «{hadith.text}»
            </p>
          </>
        ) : (
          <p className="text-lg font-arabic text-foreground leading-[2.4] text-center mb-5 px-2" dir="auto">
            «{hadith.text}»
          </p>
        )}

        {/* Footer — source info */}
        <div className="flex items-center justify-between text-[11px] text-muted-foreground/70 pt-4 border-t border-[hsl(var(--border)/0.2)]">
          <span className="flex items-center gap-1.5">
            <BookOpen className="h-3 w-3" />
            {t('narratorLabel')} {hadith.narrator}
          </span>
          <span className="font-medium">{hadith.source}</span>
        </div>
      </div>
    </div>
  );
}
