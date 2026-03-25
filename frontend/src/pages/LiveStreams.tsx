import { useState, useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { useAdmin } from '@/hooks/useAdmin';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/lib/utils';
import { ArrowLeft, ArrowRight, Radio, Wifi, WifiOff, Play, Plus, Trash2, Edit, Save, X, ExternalLink } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useSmartBack } from '@/hooks/useSmartBack';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface LiveStream {
  id: string;
  name: string;
  embed_type: string;
  embed_value: string;
  embed_url?: string;
  thumbnail: string;
  city: string;
  country: string;
  category: string;
  is_247: boolean;
  is_active?: boolean;
  sort_order?: number;
}

const CATEGORY_CONFIG = [
  { key: 'all', emoji: '🌍', labelKey: 'allStreams' },
  { key: 'haramain', emoji: '🕋', labelKey: 'haramain' },
  { key: 'holy', emoji: '🕌', labelKey: 'holySites' },
  { key: 'historic', emoji: '🏛️', labelKey: 'historicMosques' },
  { key: 'europe', emoji: '🇪🇺', labelKey: 'europeanMosques' },
  { key: 'other', emoji: '📺', labelKey: 'other' },
];

export default function LiveStreams() {
  const { t, dir, locale } = useLocale();
  const { isAdmin } = useAdmin();
  const { user } = useAuth();
  const navigate = useNavigate();
  const goBack = useSmartBack();
  const [streams, setStreams] = useState<LiveStream[]>([]);
  const [activeCategory, setActiveCategory] = useState('all');
  const [activeStreamId, setActiveStreamId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    embed_url: '',
    city: '',
    country: '',
    category: 'other',
    is_247: false,
    sort_order: 99,
  });

  const fetchStreams = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/api/live-streams`);
      const data = await res.json();
      if (data.success) setStreams(data.streams);
    } catch (e) {
      console.error('Failed to fetch live streams:', e);
    }
    setLoading(false);
  };

  useEffect(() => { fetchStreams(); }, []);

  const getEmbedUrl = (stream: LiveStream) => {
    if (stream.embed_url) return stream.embed_url;
    if (stream.embed_type === 'channel') {
      return `https://www.youtube.com/embed/live_stream?channel=${stream.embed_value}`;
    }
    return `https://www.youtube.com/embed/${stream.embed_value}`;
  };

  const handleAddStream = async () => {
    if (!formData.name || !formData.embed_url) {
      toast.error(t('fillRequiredFields'));
      return;
    }
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch(`${BACKEND_URL}/api/admin/live-streams`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.success) {
        toast.success(t('streamAdded'));
        setShowAddForm(false);
        setFormData({ name: '', embed_url: '', city: '', country: '', category: 'other', is_247: false, sort_order: 99 });
        fetchStreams();
      } else {
        toast.error(data.detail || 'Error');
      }
    } catch (e) {
      toast.error('Failed to add stream');
    }
  };

  const handleDeleteStream = async (streamId: string) => {
    if (!confirm(t('confirmDelete'))) return;
    try {
      const token = localStorage.getItem('auth_token');
      await fetch(`${BACKEND_URL}/api/admin/live-streams/${streamId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });
      toast.success(t('streamDeleted'));
      fetchStreams();
    } catch (e) {
      toast.error('Failed to delete');
    }
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
      <div className="sticky top-0 z-50 glass-nav bg-background/80 border-b border-border/10 px-4 h-14 flex items-center justify-between">
        <button onClick={goBack} className="p-2 rounded-xl hover:bg-muted/50">
          {dir === 'rtl' ? <ArrowRight className="h-5 w-5" /> : <ArrowLeft className="h-5 w-5" />}
        </button>
        <h1 className="text-lg font-black text-foreground flex items-center gap-2">
          <Radio className="h-5 w-5 text-red-500 animate-pulse" /> {t('liveStreams')}
        </h1>
        {isAdmin && (
          <button onClick={() => setShowAddForm(!showAddForm)} className="p-2 rounded-xl bg-primary/10 text-primary">
            <Plus className="h-5 w-5" />
          </button>
        )}
        {!isAdmin && <div className="w-9" />}
      </div>

      {/* Admin Add Form */}
      {isAdmin && showAddForm && (
        <div className="mx-4 mt-4 p-4 bg-card rounded-2xl border border-primary/30 space-y-3">
          <h3 className="text-sm font-bold flex items-center gap-2">
            <Plus className="w-4 h-4 text-primary" /> {t('addNewStream')}
          </h3>
          <input
            value={formData.name}
            onChange={e => setFormData({ ...formData, name: e.target.value })}
            placeholder={t('streamName')}
            className="w-full px-3 py-2 rounded-xl bg-muted/50 border border-border/30 text-sm"
          />
          <input
            value={formData.embed_url}
            onChange={e => setFormData({ ...formData, embed_url: e.target.value })}
            placeholder="YouTube URL / Embed / Video ID"
            className="w-full px-3 py-2 rounded-xl bg-muted/50 border border-border/30 text-sm"
            dir="ltr"
          />
          <div className="grid grid-cols-2 gap-2">
            <input
              value={formData.city}
              onChange={e => setFormData({ ...formData, city: e.target.value })}
              placeholder={t('city')}
              className="px-3 py-2 rounded-xl bg-muted/50 border border-border/30 text-sm"
            />
            <input
              value={formData.country}
              onChange={e => setFormData({ ...formData, country: e.target.value })}
              placeholder={t('country')}
              className="px-3 py-2 rounded-xl bg-muted/50 border border-border/30 text-sm"
            />
          </div>
          <div className="flex gap-2">
            <select
              value={formData.category}
              onChange={e => setFormData({ ...formData, category: e.target.value })}
              className="flex-1 px-3 py-2 rounded-xl bg-muted/50 border border-border/30 text-sm"
            >
              {CATEGORY_CONFIG.filter(c => c.key !== 'all').map(c => (
                <option key={c.key} value={c.key}>{t(c.labelKey)}</option>
              ))}
            </select>
            <label className="flex items-center gap-2 text-xs">
              <input
                type="checkbox"
                checked={formData.is_247}
                onChange={e => setFormData({ ...formData, is_247: e.target.checked })}
                className="rounded"
              />
              24/7
            </label>
          </div>
          <div className="flex gap-2">
            <button onClick={handleAddStream} className="flex-1 py-2 bg-primary text-primary-foreground rounded-xl text-sm font-bold flex items-center justify-center gap-1">
              <Save className="w-4 h-4" /> {t('save')}
            </button>
            <button onClick={() => setShowAddForm(false)} className="px-4 py-2 bg-muted rounded-xl text-sm">
              {t('cancel')}
            </button>
          </div>
        </div>
      )}

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
                : 'neu-card text-muted-foreground hover:text-foreground'
            )}
          >
            <span>{cat.emoji}</span>
            {t(cat.labelKey)}
          </button>
        ))}
      </div>

      {/* Active Stream Player */}
      {activeStreamId && (() => {
        const activeStream = streams.find(s => s.id === activeStreamId);
        if (!activeStream) return null;
        return (
          <div className="px-4 mb-4">
            <div className="relative rounded-2xl overflow-hidden bg-black aspect-video shadow-2xl">
              <iframe
                src={`${getEmbedUrl(activeStream)}?autoplay=1&rel=0&modestbranding=1`}
                className="w-full h-full"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                title={activeStream.name}
              />
            </div>
            <div className="flex items-center justify-between mt-3">
              <div>
                <h3 className="text-sm font-bold text-foreground">{activeStream.name}</h3>
                <p className="text-xs text-muted-foreground">📍 {activeStream.city}, {activeStream.country}</p>
              </div>
              <button
                onClick={() => setActiveStreamId(null)}
                className="px-3 py-1.5 text-xs font-bold text-red-500 bg-red-500/10 rounded-lg"
              >
                {t('closePlayer')}
              </button>
            </div>
          </div>
        );
      })()}

      {/* Stream Cards */}
      <div className="px-4 space-y-3">
        {filteredStreams.map(stream => (
          <div
            key={stream.id}
            className={cn(
              'w-full flex items-center gap-4 p-4 rounded-2xl border transition-all',
              activeStreamId === stream.id
                ? 'bg-primary/5 border-primary/30 shadow-lg'
                : 'bg-card border-border/30 hover:border-primary/20 hover:shadow-md'
            )}
          >
            <button
              onClick={() => setActiveStreamId(stream.id)}
              className="flex items-center gap-4 flex-1 text-start"
            >
              {/* Thumbnail/Play */}
              <div className="relative w-20 h-14 rounded-xl overflow-hidden bg-muted shrink-0 flex items-center justify-center">
                {stream.thumbnail ? (
                  <img src={stream.thumbnail} alt={stream.name} className="w-full h-full object-cover" />
                ) : (
                  <div className="bg-gradient-to-br from-primary/20 to-primary/5 w-full h-full flex items-center justify-center">
                    <Play className="w-6 h-6 text-primary fill-primary" />
                  </div>
                )}
                {stream.is_247 && (
                  <div className="absolute top-1 left-1 px-1.5 py-0.5 bg-red-500 rounded text-[8px] text-white font-bold flex items-center gap-0.5">
                    <div className="w-1.5 h-1.5 bg-white rounded-full animate-pulse" />
                    24/7
                  </div>
                )}
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-bold text-foreground truncate">{stream.name}</h3>
                {(stream.city || stream.country) && (
                  <p className="text-xs text-muted-foreground">📍 {stream.city}{stream.city && stream.country ? ', ' : ''}{stream.country}</p>
                )}
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
            </button>

            {/* Admin actions */}
            {isAdmin && (
              <button
                onClick={() => handleDeleteStream(stream.id)}
                className="p-2 rounded-lg bg-red-500/10 text-red-500 hover:bg-red-500/20 shrink-0"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}

            {/* Play button */}
            <button
              onClick={() => setActiveStreamId(stream.id)}
              className={cn(
                'w-10 h-10 rounded-full flex items-center justify-center shrink-0',
                activeStreamId === stream.id
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-primary/10 text-primary'
              )}
            >
              <Play className="w-5 h-5 fill-current" />
            </button>
          </div>
        ))}

        {filteredStreams.length === 0 && (
          <div className="text-center py-12">
            <WifiOff className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
            <p className="text-sm text-muted-foreground">{t('noStreamsAvailable')}</p>
            {isAdmin && (
              <button
                onClick={() => setShowAddForm(true)}
                className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-xl text-sm font-bold"
              >
                <Plus className="w-4 h-4 inline mr-1" /> {t('addNewStream')}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
