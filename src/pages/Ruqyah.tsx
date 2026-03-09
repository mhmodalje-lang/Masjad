import { useState, useEffect, useCallback } from 'react';
import { supabase } from '@/integrations/supabase/client';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, Play, Square, ExternalLink, Shield, Volume2 } from 'lucide-react';
import PageHeader from '@/components/PageHeader';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface RuqyahCategory {
  id: string;
  name_ar: string;
  name_en: string | null;
  emoji: string;
  sort_order: number;
}

interface RuqyahTrack {
  id: string;
  category_id: string;
  title_ar: string;
  reciter_ar: string;
  reciter_en: string | null;
  media_type: string;
  media_url: string;
  youtube_id: string | null;
  duration_seconds: number | null;
  sort_order: number;
  is_active: boolean;
}

type ViewMode = 'categories' | 'tracks';

export default function Ruqyah() {
  const [categories, setCategories] = useState<RuqyahCategory[]>([]);
  const [tracks, setTracks] = useState<RuqyahTrack[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<RuqyahCategory | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('categories');
  const [playingId, setPlayingId] = useState<string | null>(null);
  const [audioEl, setAudioEl] = useState<HTMLAudioElement | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    const { data } = await supabase
      .from('ruqyah_categories')
      .select('*')
      .order('sort_order');
    if (data) setCategories(data as RuqyahCategory[]);
    setLoading(false);
  };

  const loadTracks = useCallback(async (categoryId: string) => {
    setLoading(true);
    const { data } = await supabase
      .from('ruqyah_tracks')
      .select('*')
      .eq('category_id', categoryId)
      .eq('is_active', true)
      .order('sort_order');
    if (data) setTracks(data as RuqyahTrack[]);
    setLoading(false);
  }, []);

  const openCategory = (cat: RuqyahCategory) => {
    setSelectedCategory(cat);
    setViewMode('tracks');
    loadTracks(cat.id);
    window.history.pushState({ view: 'tracks' }, '');
  };

  const goBack = () => {
    stopAudio();
    window.history.back();
  };

  useEffect(() => {
    const handlePopState = () => {
      if (viewMode === 'tracks') {
        setViewMode('categories');
        setSelectedCategory(null);
        stopAudio();
      }
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, [viewMode]);

  const stopAudio = () => {
    if (audioEl) {
      audioEl.pause();
      audioEl.currentTime = 0;
      setAudioEl(null);
    }
    setPlayingId(null);
  };

  const playTrack = (track: RuqyahTrack) => {
    if (track.media_type === 'youtube' && track.youtube_id) {
      window.open(`https://www.youtube.com/watch?v=${track.youtube_id}`, '_blank', 'noopener');
      return;
    }

    if (playingId === track.id) {
      stopAudio();
      return;
    }

    stopAudio();
    if (track.media_url) {
      const audio = new Audio(track.media_url);
      audio.volume = 0.8;
      audio.play().catch(() => {});
      audio.onended = () => {
        setPlayingId(null);
        setAudioEl(null);
      };
      setAudioEl(audio);
      setPlayingId(track.id);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (audioEl) {
        audioEl.pause();
      }
    };
  }, [audioEl]);

  return (
    <div className="min-h-screen pb-24 overflow-x-hidden" dir="rtl">
      <PageHeader
        title="🛡️ العلاج بالرقية الشرعية"
        subtitle="رقية شرعية من القرآن والسنة"
        image="https://images.unsplash.com/photo-1609599006353-e629aaabfeae?w=1200&q=85"
        actionsLeft={
          viewMode === 'tracks' ? (
            <button onClick={goBack} className="p-2.5 rounded-2xl bg-white/10 backdrop-blur-xl border border-white/10 transition-all active:scale-95">
              <ArrowRight className="h-4 w-4 text-white" />
            </button>
          ) : undefined
        }
      />

      <div className="px-5 pt-4">
        {/* Disclaimer */}
        <div className="rounded-2xl bg-accent/10 border border-accent/20 p-4 mb-5">
          <p className="text-xs text-muted-foreground leading-relaxed text-center">
            ⚠️ الرقية الشرعية مأخوذة من القرآن الكريم والسنة النبوية الشريفة.
            هذا القسم للاستماع والتحصين وليس بديلاً عن العلاج الطبي.
          </p>
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={viewMode + (selectedCategory?.id || '')}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.2 }}
          >
            {viewMode === 'categories' && (
              <div className="space-y-3">
                {loading ? (
                  <div className="text-center py-20">
                    <Shield className="h-8 w-8 animate-spin text-primary mx-auto" />
                  </div>
                ) : (
                  categories.map((cat, i) => (
                    <motion.button
                      key={cat.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.05 }}
                      onClick={() => openCategory(cat)}
                      className="w-full flex items-center gap-4 p-5 rounded-2xl bg-card border border-border hover:border-primary/30 transition-all text-right"
                    >
                      <div className="h-14 w-14 rounded-2xl bg-primary/10 flex items-center justify-center text-2xl shrink-0">
                        {cat.emoji}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-bold text-foreground">{cat.name_ar}</p>
                        {cat.name_en && (
                          <p className="text-xs text-muted-foreground mt-0.5">{cat.name_en}</p>
                        )}
                      </div>
                      <ArrowRight className="h-4 w-4 text-muted-foreground rotate-180 rtl:rotate-0 shrink-0" />
                    </motion.button>
                  ))
                )}
              </div>
            )}

            {viewMode === 'tracks' && selectedCategory && (
              <>
                <div className="flex items-center gap-3 mb-5">
                  <div className="h-12 w-12 rounded-2xl bg-primary/10 flex items-center justify-center text-xl shrink-0">
                    {selectedCategory.emoji}
                  </div>
                  <div>
                    <h2 className="text-lg font-bold text-foreground">{selectedCategory.name_ar}</h2>
                    <p className="text-xs text-muted-foreground">{tracks.length} رقية</p>
                  </div>
                </div>

                {loading ? (
                  <div className="text-center py-20">
                    <Shield className="h-8 w-8 animate-spin text-primary mx-auto" />
                  </div>
                ) : tracks.length === 0 ? (
                  <div className="text-center py-16">
                    <span className="text-5xl mb-4 block">🕌</span>
                    <p className="text-sm text-muted-foreground">لا توجد رقيات في هذا القسم بعد</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {tracks.map((track, i) => {
                      const isPlaying = playingId === track.id;
                      const isYoutube = track.media_type === 'youtube';

                      return (
                        <motion.div
                          key={track.id}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.04 }}
                          className={cn(
                            'flex items-center gap-4 p-4 rounded-2xl border transition-all',
                            isPlaying
                              ? 'bg-primary/5 border-primary/30'
                              : 'bg-card border-border hover:border-primary/20'
                          )}
                        >
                          {/* Play button */}
                          <Button
                            variant={isPlaying ? 'default' : 'outline'}
                            size="sm"
                            className="h-12 w-12 shrink-0 rounded-full p-0"
                            onClick={() => playTrack(track)}
                          >
                            {isYoutube ? (
                              <ExternalLink className="h-4 w-4" />
                            ) : isPlaying ? (
                              <Square className="h-4 w-4 fill-current" />
                            ) : (
                              <Play className="h-4 w-4 fill-current" />
                            )}
                          </Button>

                          {/* Info */}
                          <div className="flex-1 min-w-0" onClick={() => playTrack(track)}>
                            <p className="text-sm font-bold text-foreground line-clamp-1">{track.title_ar}</p>
                            <p className="text-xs text-muted-foreground mt-0.5">🎙️ {track.reciter_ar}</p>
                          </div>

                          {/* Audio indicator */}
                          {isPlaying && (
                            <div className="flex items-center gap-1 shrink-0">
                              <Volume2 className="h-4 w-4 text-primary animate-pulse" />
                            </div>
                          )}

                          {isYoutube && (
                            <span className="text-[10px] text-muted-foreground bg-muted rounded-full px-2 py-0.5 shrink-0">YouTube</span>
                          )}
                        </motion.div>
                      );
                    })}
                  </div>
                )}
              </>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
