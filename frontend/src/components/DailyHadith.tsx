import { useState, useEffect } from 'react';
import { BookOpen, Share2 } from 'lucide-react';
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
        <div className="rounded-3xl bg-card border border-border/40 p-5 animate-pulse">
          <div className="h-4 bg-muted rounded w-24 mb-4" />
          <div className="h-6 bg-muted rounded w-full mb-2" />
          <div className="h-6 bg-muted rounded w-3/4" />
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 mb-4" data-testid="daily-hadith">
      <div className="rounded-3xl bg-card border border-border/40 p-5 shadow-elevated relative overflow-hidden">
        <div className="absolute top-0 left-0 w-32 h-32 bg-gradient-to-br from-amber-500/5 to-transparent rounded-br-full" />
        
        <div className="flex items-center justify-between mb-4 relative">
          <span className="inline-flex items-center gap-2 rounded-full bg-amber-500/10 border border-amber-500/20 px-3 py-1 text-[11px] font-bold text-amber-600 dark:text-amber-400">
            <BookOpen className="h-3 w-3" />
            {t('hadithOfDay')}
          </span>
          <button
            onClick={handleShare}
            className="p-2 rounded-xl hover:bg-muted transition-colors"
            data-testid="share-hadith-btn"
          >
            <Share2 className="h-4 w-4 text-muted-foreground" />
          </button>
        </div>

        <p className="text-sm text-muted-foreground mb-2">{t('prophetSaid')}</p>
        
        {/* Arabic text always shown */}
        {hadith.arabic_text ? (
          <>
            <p className="text-lg font-arabic text-foreground leading-[2.2] text-center mb-3" dir="rtl">
              «{hadith.arabic_text}»
            </p>
            <p className="text-sm text-muted-foreground leading-relaxed text-center mb-4 border-t border-border/20 pt-3" dir="auto">
              «{hadith.text}»
            </p>
          </>
        ) : (
          <p className="text-lg font-arabic text-foreground leading-[2.2] text-center mb-4" dir="auto">
            «{hadith.text}»
          </p>
        )}

        <div className="flex items-center justify-between text-xs text-muted-foreground border-t border-border/40 pt-3">
          <span>{t('narratorLabel')} {hadith.narrator}</span>
          <span>{hadith.source}</span>
        </div>
      </div>
    </div>
  );
}
