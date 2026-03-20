import { useState, useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { ArrowLeft, ArrowRight, Radio, Wifi, WifiOff, ExternalLink, Play } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface LiveStream {
  id: string;
  name_ar: string;
  name_en: string;
  name_de: string;
  name_ru: string;
  name_fr: string;
  name_tr: string;
  name_sv: string;
  name_nl: string;
  name_el: string;
  youtube_channel: string;
  embed_id: string;
  thumbnail: string;
  city: string;
  country: string;
  category: string;
  is_247: boolean;
}

const CATEGORY_CONFIG = [
  { key: 'all', emoji: '🌍', labelKey: 'allStreams' },
  { key: 'haramain', emoji: '🕋', labelKey: 'haramain' },
  { key: 'holy', emoji: '🕌', labelKey: 'holySites' },
  { key: 'historic', emoji: '🏛️', labelKey: 'historicMosques' },
  { key: 'europe', emoji: '🇪🇺', labelKey: 'europeanMosques' },
];

export default function LiveStreams() {
  const { t, dir, locale } = useLocale();
  const navigate = useNavigate();
  const [streams, setStreams] = useState<LiveStream[]>([]);
  const [activeCategory, setActiveCategory] = useState('all');
  const [activeStreamId, setActiveStreamId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStreams() {
      try {
        const res = await fetch(`${BACKEND_URL}/api/live-streams`);
        const data = await res.json();
        if (data.success) setStreams(data.streams);
      } catch (e) {
        console.error('Failed to fetch live streams:', e);
      }
      setLoading(false);
    }
    fetchStreams();
  }, []);

  const getStreamName = (stream: LiveStream): string => {
    const nameKey = `name_${locale}` as keyof LiveStream;
    return (stream[nameKey] as string) || stream.name_en || stream.name_ar;
  };

  const filteredStreams = activeCategory === 'all'
    ? streams
    : streams.filter(s => s.category === activeCategory);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-28 bg-background" dir={dir}>
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center justify-between">
        <button onClick={() => navigate(-1)} className="p-2 rounded-xl hover:bg-muted/50">
          {dir === 'rtl' ? <ArrowRight className="h-5 w-5" /> : <ArrowLeft className="h-5 w-5" />}
        </button>
        <h1 className="text-lg font-black text-foreground flex items-center gap-2">
          <Radio className="h-5 w-5 text-red-500 animate-pulse" /> {t('liveStreams')}
        </h1>
        <div className="w-9" />
      </div>

      {/* Live indicator banner */}
      <div className="mx-4 mt-4 mb-3 px-4 py-3 bg-gradient-to-r from-red-500/10 to-rose-500/5 border border-red-500/20 rounded-2xl">
        <div className="flex items-center gap-2">
          <div className="relative">
            <div className="w-3 h-3 bg-red-500 rounded-full" />
            <div className="absolute inset-0 w-3 h-3 bg-red-500 rounded-full animate-ping" />
          </div>
          <span className="text-sm font-bold text-red-500">{t('liveNow')}</span>
          <span className="text-xs text-muted-foreground">{t('liveDescription')}</span>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="px-4 mb-4 flex gap-2 overflow-x-auto no-scrollbar">
        {CATEGORY_CONFIG.map(cat => (
          <button
            key={cat.key}
            onClick={() => setActiveCategory(cat.key)}
            className={cn(
              'flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all shrink-0',
              activeCategory === cat.key
                ? 'bg-primary text-primary-foreground'
                : 'bg-card border border-border/30 text-muted-foreground hover:text-foreground'
            )}
          >
            <span>{cat.emoji}</span>
            {t(cat.labelKey)}
          </button>
        ))}
      </div>

      {/* Active Stream Player */}
      {activeStreamId && (
        <div className="px-4 mb-4">
          <div className="relative rounded-2xl overflow-hidden bg-black aspect-video shadow-2xl">
            <iframe
              src={`https://www.youtube.com/embed/${streams.find(s => s.id === activeStreamId)?.embed_id}?autoplay=1&rel=0&modestbranding=1`}
              className="w-full h-full"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              title="Live Stream"
            />
          </div>
          <div className="flex items-center justify-between mt-3">
            <div>
              <h3 className="text-sm font-bold text-foreground">
                {getStreamName(streams.find(s => s.id === activeStreamId)!)}
              </h3>
              <p className="text-xs text-muted-foreground">
                📍 {streams.find(s => s.id === activeStreamId)?.city}, {streams.find(s => s.id === activeStreamId)?.country}
              </p>
            </div>
            <button
              onClick={() => setActiveStreamId(null)}
              className="px-3 py-1.5 text-xs font-bold text-red-500 bg-red-500/10 rounded-lg"
            >
              {t('closePlayer')}
            </button>
          </div>
        </div>
      )}

      {/* Stream Cards */}
      <div className="px-4 space-y-3">
        {filteredStreams.map(stream => (
          <button
            key={stream.id}
            onClick={() => setActiveStreamId(stream.id)}
            className={cn(
              'w-full flex items-center gap-4 p-4 rounded-2xl border transition-all active:scale-[0.98]',
              activeStreamId === stream.id
                ? 'bg-primary/5 border-primary/30 shadow-lg'
                : 'bg-card border-border/30 hover:border-primary/20 hover:shadow-md'
            )}
          >
            {/* Thumbnail */}
            <div className="relative w-20 h-14 rounded-xl overflow-hidden bg-muted shrink-0">
              <img
                src={stream.thumbnail}
                alt={getStreamName(stream)}
                className="w-full h-full object-cover"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = '';
                  (e.target as HTMLImageElement).style.display = 'none';
                }}
              />
              <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
                <Play className="w-6 h-6 text-white fill-white" />
              </div>
              {stream.is_247 && (
                <div className="absolute top-1 left-1 px-1.5 py-0.5 bg-red-500 rounded text-[8px] text-white font-bold flex items-center gap-0.5">
                  <div className="w-1.5 h-1.5 bg-white rounded-full animate-pulse" />
                  24/7
                </div>
              )}
            </div>

            {/* Info */}
            <div className="flex-1 text-start min-w-0">
              <h3 className="text-sm font-bold text-foreground truncate">{getStreamName(stream)}</h3>
              <p className="text-xs text-muted-foreground">📍 {stream.city}, {stream.country}</p>
              <div className="flex items-center gap-1 mt-1">
                {stream.is_247 ? (
                  <span className="flex items-center gap-1 text-[10px] text-green-500 font-bold">
                    <Wifi className="w-3 h-3" /> {t('live247')}
                  </span>
                ) : (
                  <span className="flex items-center gap-1 text-[10px] text-amber-500 font-bold">
                    <Radio className="w-3 h-3" /> {t('livePrayerTimes')}
                  </span>
                )}
              </div>
            </div>

            {/* Play indicator */}
            <div className={cn(
              'w-10 h-10 rounded-full flex items-center justify-center shrink-0',
              activeStreamId === stream.id
                ? 'bg-primary text-primary-foreground'
                : 'bg-primary/10 text-primary'
            )}>
              <Play className="w-5 h-5 fill-current" />
            </div>
          </button>
        ))}

        {filteredStreams.length === 0 && (
          <div className="text-center py-12">
            <WifiOff className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
            <p className="text-sm text-muted-foreground">{t('noStreamsAvailable')}</p>
          </div>
        )}
      </div>
    </div>
  );
}
