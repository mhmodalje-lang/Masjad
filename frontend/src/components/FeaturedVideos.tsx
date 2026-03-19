import { useState, useEffect, useRef } from 'react';
import { Play, X, ChevronLeft, Film, Volume2, VolumeX } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { useLocale } from '@/hooks/useLocale';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface EmbedItem {
  id: string;
  title: string;
  description?: string;
  embed_url: string;
  platform: string;
  category: string;
  thumbnail_url?: string;
}

export default function FeaturedVideos() {
  const { t } = useLocale();
  const [videos, setVideos] = useState<EmbedItem[]>([]);
  const [activeVideo, setActiveVideo] = useState<EmbedItem | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/embed-content?limit=10`)
      .then(r => r.json())
      .then(d => setVideos(d.content || []))
      .catch(() => {});
  }, []);

  if (videos.length === 0) return null;

  const getYouTubeThumbnail = (url: string) => {
    const match = url.match(/youtube\.com\/embed\/([\w-]+)/);
    return match ? `https://img.youtube.com/vi/${match[1]}/hqdefault.jpg` : null;
  };

  return (
    <div className="mb-5">
      {/* Section Header */}
      <div className="flex items-center justify-between px-4 mb-3">
        <div className="flex items-center gap-2">
          <Film className="h-4 w-4 text-red-500" />
          <h3 className="text-sm font-bold text-foreground">{t('featuredContent')}</h3>
        </div>
        <span className="text-[10px] text-muted-foreground bg-muted/50 px-2 py-0.5 rounded-full">{videos.length} {t('videosCount')}</span>
      </div>

      {/* Horizontal Scroll */}
      <div 
        ref={scrollRef}
        className="flex gap-3 px-4 overflow-x-auto scrollbar-hide snap-x snap-mandatory"
        style={{ scrollSnapType: 'x mandatory' }}
      >
        {videos.map((video, idx) => {
          const thumbnail = video.thumbnail_url || getYouTubeThumbnail(video.embed_url);
          return (
            <div
              key={video.id}
              onClick={() => { setActiveVideo(video); setCurrentIndex(idx); }}
              className="flex-shrink-0 w-[280px] snap-start cursor-pointer group"
            >
              <div className="relative rounded-2xl overflow-hidden aspect-video bg-muted border border-border/30 shadow-sm">
                {thumbnail ? (
                  <img 
                    src={thumbnail} 
                    alt={video.title}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                    loading="lazy"
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-red-500/20 to-red-600/10 flex items-center justify-center">
                    <Film className="h-10 w-10 text-red-500/50" />
                  </div>
                )}
                {/* Play overlay */}
                <div className="absolute inset-0 bg-black/30 flex items-center justify-center opacity-80 group-hover:opacity-100 transition-opacity">
                  <div className="h-12 w-12 rounded-full bg-red-600 flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform">
                    <Play className="h-5 w-5 text-white fill-white ml-0.5" />
                  </div>
                </div>
                {/* Platform badge */}
                <div className="absolute top-2 left-2 bg-black/60 backdrop-blur-sm px-2 py-0.5 rounded-full">
                  <span className="text-[10px] text-white font-bold capitalize">{video.platform}</span>
                </div>
              </div>
              <div className="mt-2 px-1">
                <p className="text-xs font-bold text-foreground line-clamp-1">{video.title}</p>
                {video.description && (
                  <p className="text-[10px] text-muted-foreground line-clamp-1 mt-0.5">{video.description}</p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Video Player Modal */}
      <AnimatePresence>
        {activeVideo && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[999] bg-black/90 flex flex-col items-center justify-center"
            onClick={() => setActiveVideo(null)}
          >
            <div className="w-full max-w-2xl px-4" onClick={e => e.stopPropagation()}>
              {/* Close button */}
              <button
                onClick={() => setActiveVideo(null)}
                className="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20 transition-colors z-10"
              >
                <X className="h-5 w-5 text-white" />
              </button>

              {/* Video player */}
              <div className="relative w-full aspect-video rounded-2xl overflow-hidden bg-black shadow-2xl">
                <iframe
                  src={`${activeVideo.embed_url}?autoplay=1&rel=0`}
                  title={activeVideo.title}
                  className="w-full h-full"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              </div>

              {/* Video info */}
              <div className="mt-4 text-center">
                <h3 className="text-base font-bold text-white">{activeVideo.title}</h3>
                {activeVideo.description && (
                  <p className="text-sm text-white/60 mt-1">{activeVideo.description}</p>
                )}
              </div>

              {/* Navigation */}
              {videos.length > 1 && (
                <div className="flex justify-center gap-4 mt-4">
                  <button
                    onClick={() => {
                      const prev = currentIndex > 0 ? currentIndex - 1 : videos.length - 1;
                      setCurrentIndex(prev);
                      setActiveVideo(videos[prev]);
                    }}
                    className="p-3 rounded-full bg-white/10 hover:bg-white/20 transition-colors"
                  >
                    <ChevronLeft className="h-5 w-5 text-white rotate-180" />
                  </button>
                  <span className="text-white/50 text-sm self-center">{currentIndex + 1} / {videos.length}</span>
                  <button
                    onClick={() => {
                      const next = currentIndex < videos.length - 1 ? currentIndex + 1 : 0;
                      setCurrentIndex(next);
                      setActiveVideo(videos[next]);
                    }}
                    className="p-3 rounded-full bg-white/10 hover:bg-white/20 transition-colors"
                  >
                    <ChevronLeft className="h-5 w-5 text-white" />
                  </button>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
