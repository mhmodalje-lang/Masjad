import { useState, useEffect, useRef, useCallback } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Heart, MessageCircle, Gift, Share2, ArrowRight, Play, Pause, Volume2, VolumeX } from 'lucide-react';
import { Link } from 'react-router-dom';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface VideoPost {
  id: string;
  author_id: string;
  author_name: string;
  author_avatar?: string;
  content: string;
  video_url?: string;
  image_url?: string;
  thumbnail_url?: string;
  content_type: string;
  likes_count: number;
  comments_count: number;
  shares_count?: number;
  liked: boolean;
  created_at: string;
}

export default function VideoReels() {
  const { t, dir } = useLocale();
  const { user, getToken } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [posts, setPosts] = useState<VideoPost[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchVideos();
  }, []);

  const fetchVideos = async () => {
    try {
      const token = getToken();
      const headers: Record<string, string> = {};
      if (token) headers.Authorization = `Bearer ${token}`;
      
      // Fetch all posts including images as "reels"
      const res = await fetch(`${BACKEND_URL}/api/sohba/explore?limit=30`, { headers });
      const data = await res.json();
      setPosts(data.posts || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async (postId: string, index: number) => {
    if (!user) return;
    const token = getToken();
    try {
      const res = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/like`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setPosts(prev => prev.map((p, i) => 
        i === index ? { ...p, liked: data.liked, likes_count: data.liked ? p.likes_count + 1 : p.likes_count - 1 } : p
      ));
    } catch (err) {
      console.error(err);
    }
  };

  const handleShare = async (postId: string) => {
    const token = getToken();
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/share`, {
        method: 'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
    } catch (err) {
      console.error(err);
    }
  };

  const getMediaUrl = (url?: string) => {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return `${BACKEND_URL}${url}`;
  };

  const handleScroll = useCallback(() => {
    if (!containerRef.current) return;
    const scrollTop = containerRef.current.scrollTop;
    const height = containerRef.current.clientHeight;
    const newIndex = Math.round(scrollTop / height);
    if (newIndex !== currentIndex) {
      setCurrentIndex(newIndex);
    }
  }, [currentIndex]);

  if (loading) {
    return (
      <div className="h-screen bg-black flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="h-screen bg-black relative">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-30 flex items-center justify-between px-3.5 py-2.5 bg-gradient-to-b from-black/50 to-transparent"
        style={{ paddingTop: 'max(8px, env(safe-area-inset-top, 8px))' }}>
        <button onClick={() => navigate(-1)} className="text-white p-1 active:scale-90 transition-transform">
          <ArrowRight className="w-5 h-5" />
        </button>
        <div className="flex items-center gap-4">
          <span className="text-white/50 text-[12px] font-bold">{t('trending')}</span>
          <span className="text-white text-[12px] font-bold border-b-2 border-white pb-0.5">{t('videoTab')}</span>
        </div>
        <div className="w-5" />
      </div>

      {/* Reels Container */}
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className="h-full overflow-y-scroll snap-y snap-mandatory scrollbar-hide"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {posts.map((post, index) => (
          <ReelItem
            key={post.id}
            post={post}
            isActive={index === currentIndex}
            onLike={() => handleLike(post.id, index)}
            onShare={() => handleShare(post.id)}
            getMediaUrl={getMediaUrl}
          />
        ))}
      </div>
    </div>
  );
}

function ReelItem({ post, isActive, onLike, onShare, getMediaUrl }: {
  post: VideoPost;
  isActive: boolean;
  onLike: () => void;
  onShare: () => void;
  getMediaUrl: (url?: string) => string;
}) {
  const { dir } = useLocale();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(false);
  const [paused, setPaused] = useState(false);
  const hasVideo = post.video_url;

  useEffect(() => {
    if (!videoRef.current) return;
    if (isActive) {
      videoRef.current.play().catch(() => {});
      setPaused(false);
    } else {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
    }
  }, [isActive]);

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (videoRef.current.paused) {
      videoRef.current.play();
      setPaused(false);
    } else {
      videoRef.current.pause();
      setPaused(true);
    }
  };

  return (
    <div className="h-screen w-full snap-start relative flex items-center justify-center bg-black">
      {/* Background Media */}
      {hasVideo ? (
        <video
          ref={videoRef}
          src={getMediaUrl(post.video_url)}
          className="absolute inset-0 w-full h-full object-cover"
          loop
          muted={muted}
          playsInline
          onClick={togglePlay}
        />
      ) : post.image_url ? (
        <div className="absolute inset-0">
          <img
            src={getMediaUrl(post.image_url)}
            alt=""
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/30" />
        </div>
      ) : (
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-900 via-gray-900 to-black" />
      )}

      {/* Pause Indicator */}
      {paused && hasVideo && (
        <div className="absolute inset-0 flex items-center justify-center z-10">
          <div className="w-14 h-14 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
            <Play className="w-7 h-7 text-white fill-white ms-0.5" />
          </div>
        </div>
      )}

      {/* Content text overlay */}
      <div className="absolute inset-0 flex items-center justify-center px-10 z-10 pointer-events-none">
        <p className="text-white text-lg font-bold text-center leading-[1.8] drop-shadow-lg" dir={dir}
          style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif", textShadow: '0 2px 16px rgba(0,0,0,0.7)' }}>
          {post.content}
        </p>
      </div>

      {/* Top gradient */}
      <div className="absolute top-0 left-0 right-0 h-20 bg-gradient-to-b from-black/40 to-transparent z-10 pointer-events-none" />

      {/* Right Side Actions - compact */}
      <div className="absolute end-2.5 bottom-24 flex flex-col items-center gap-4 z-20"
        style={{ marginBottom: 'env(safe-area-inset-bottom, 0px)' }}>
        {/* Author Avatar */}
        <Link to={`/social-profile/${post.author_id}`} className="relative mb-1">
          <img
            src={post.author_avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(post.author_name)}&background=1a7a4c&color=fff&size=48`}
            alt=""
            className="w-10 h-10 rounded-full border-[2px] border-white shadow-lg"
          />
        </Link>

        {/* Like */}
        <button onClick={onLike} className="flex flex-col items-center active:scale-90 transition-transform">
          <Heart className={`w-6 h-6 ${post.liked ? 'fill-red-500 text-red-500' : 'text-white'} drop-shadow-lg`} />
          <span className="text-white text-[10px] mt-0.5 font-bold drop-shadow">{post.likes_count}</span>
        </button>

        {/* Comments */}
        <Link to={`/post/${post.id}`} className="flex flex-col items-center active:scale-90 transition-transform">
          <MessageCircle className="w-6 h-6 text-white drop-shadow-lg" />
          <span className="text-white text-[10px] mt-0.5 font-bold drop-shadow">{post.comments_count}</span>
        </Link>

        {/* Gift */}
        <button className="flex flex-col items-center active:scale-90 transition-transform">
          <Gift className="w-6 h-6 text-white drop-shadow-lg" />
          <span className="text-white text-[10px] mt-0.5 font-bold drop-shadow">0</span>
        </button>

        {/* Share */}
        <button onClick={onShare} className="flex flex-col items-center active:scale-90 transition-transform">
          <Share2 className="w-6 h-6 text-white drop-shadow-lg" />
          <span className="text-white text-[10px] mt-0.5 font-bold drop-shadow">{post.shares_count || 0}</span>
        </button>

        {/* Mute toggle for video */}
        {hasVideo && (
          <button onClick={() => setMuted(!muted)} className="mt-1 active:scale-90 transition-transform">
            {muted ? (
              <VolumeX className="w-5 h-5 text-white/50" />
            ) : (
              <Volume2 className="w-5 h-5 text-white/50" />
            )}
          </button>
        )}
      </div>

      {/* Bottom Info */}
      <div className="absolute bottom-5 left-0 right-14 px-3.5 z-20" dir={dir}
        style={{ paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}>
        <div className="flex items-center gap-2 mb-1.5">
          <Link to={`/social-profile/${post.author_id}`} className="text-white font-bold text-[14px] drop-shadow-lg hover:underline">
            {post.author_name}
          </Link>
          <button className="px-2 py-0.5 bg-emerald-600 text-white text-[10px] font-bold rounded-md active:scale-95 transition-transform">
            متابعة
          </button>
        </div>
        <p className="text-white/85 text-[12px] line-clamp-2 leading-relaxed drop-shadow">
          {post.content}
        </p>
      </div>
    </div>
  );
}
