import { ExternalLink } from 'lucide-react';
import i18n from '@/lib/i18nConfig';

interface VideoItem {
  id: string;
  titleKey: string;
  channelKey: string;
  youtubeId: string;
}

const videos: VideoItem[] = [
  { id: '1', titleKey: 'videoSurahYasin', channelKey: 'channelQuranKareem', youtubeId: 'CZyaMQPQzKU' },
  { id: '2', titleKey: 'videoMorningAdhkar', channelKey: 'channelAdhkarMuslim', youtubeId: 'XeAKk15nf7U' },
  { id: '3', titleKey: 'videoSurahKahf', channelKey: 'channelQuranKareem', youtubeId: 'pr3wAE8u5sY' },
  { id: '4', titleKey: 'videoDuaRizq', channelKey: 'channelDuasAccepted', youtubeId: 'HcNsBCLBVVs' },
];

function VideoThumb({ video }: { video: VideoItem }) {
  const handleError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const target = e.currentTarget;
    target.onerror = null;
    target.src = '/mecca-hero.webp';
    target.className = target.className + ' opacity-50';
  };

  return (
    <img
      src={`https://img.youtube.com/vi/${video.youtubeId}/hqdefault.jpg`}
      alt={i18n.t(video.titleKey)}
      className="w-full h-full object-cover group-active:scale-105 transition-transform"
      loading="lazy"
      decoding="async"
      width="320"
      height="180"
      onError={handleError}
    />
  );
}

export default function VideoContentCarousel() {
  return (
    <div className="overflow-x-auto snap-x snap-mandatory flex gap-3 px-4 no-scrollbar">
      {videos.map((video) => (
        <a
          key={video.id}
          href={`https://www.youtube.com/watch?v=${video.youtubeId}`}
          target="_blank"
          rel="noopener noreferrer"
          className="relative flex-shrink-0 w-52 snap-start group"
        >
          <div className="relative overflow-hidden rounded-2xl bg-muted h-28">
            <VideoThumb video={video} />
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="h-11 w-11 rounded-full bg-black/50 backdrop-blur-sm flex items-center justify-center">
                <div className="w-0 h-0 border-t-[8px] border-t-transparent border-l-[14px] border-l-white border-b-[8px] border-b-transparent ms-1" />
              </div>
            </div>
            <div className="absolute top-2 end-2 h-6 w-6 rounded-full bg-black/40 flex items-center justify-center">
              <ExternalLink className="h-3 w-3 text-white" />
            </div>
          </div>
          <p className="text-xs font-medium mt-2 text-end line-clamp-2 leading-relaxed">{i18n.t(video.titleKey)}</p>
          <p className="text-xs text-muted-foreground text-end">{i18n.t(video.channelKey)}</p>
        </a>
      ))}
    </div>
  );
}
