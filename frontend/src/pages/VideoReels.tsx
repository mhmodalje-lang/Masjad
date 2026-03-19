import { useState, useEffect, useRef, useCallback } from 'react';
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
      <div className="absolute top-0 left-0 right-0 z-30 flex items-center justify-between px-4 py-3 bg-gradient-to-b from-black/60 to-transparent">
        <button onClick={() => navigate(-1)} className="text-white">
          <ArrowRight className="w-6 h-6" />
        </button>
        <div className="flex items-center gap-4">
          <span className="text-white/60 text-sm font-bold">الترندات</span>
          <span className="text-white text-sm font-bold border-b-2 border-white pb-0.5">فيديو</span>
        </div>
        <div className="w-6" />
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
          <div className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
            <Play className="w-8 h-8 text-white fill-white" />
          </div>
        </div>
      )}

      {/* Content text overlay */}
      <div className="absolute inset-0 flex items-center justify-center px-8 z-10 pointer-events-none">
        <p className="text-white text-xl font-bold text-center leading-relaxed drop-shadow-lg" dir="rtl">
          {post.content}
        </p>
      </div>

      {/* Right Side Actions */}
      <div className="absolute right-3 bottom-32 flex flex-col items-center gap-5 z-20">
        {/* Author Avatar */}
        <Link to={`/social-profile/${post.author_id}`} className="relative">
          <img
            src={post.author_avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(post.author_name)}&background=1a7a4c&color=fff&size=48`}
            alt=""
            className="w-12 h-12 rounded-full border-2 border-white shadow-lg"
          />
        </Link>

        {/* Like */}
        <button onClick={onLike} className="flex flex-col items-center">
          <Heart className={`w-8 h-8 ${post.liked ? 'fill-red-500 text-red-500' : 'text-white'} drop-shadow-lg`} />
          <span className="text-white text-xs mt-1 font-bold drop-shadow">{post.likes_count}</span>
        </button>

        {/* Comments */}
        <Link to={`/post/${post.id}`} className="flex flex-col items-center">
          <MessageCircle className="w-8 h-8 text-white drop-shadow-lg" />
          <span className="text-white text-xs mt-1 font-bold drop-shadow">{post.comments_count}</span>
        </Link>

        {/* Gift */}
        <button className="flex flex-col items-center">
          <Gift className="w-8 h-8 text-white drop-shadow-lg" />
          <span className="text-white text-xs mt-1 font-bold drop-shadow">0</span>
        </button>

        {/* Share */}
        <button onClick={onShare} className="flex flex-col items-center">
          <Share2 className="w-8 h-8 text-white drop-shadow-lg" />
          <span className="text-white text-xs mt-1 font-bold drop-shadow">{post.shares_count || 0}</span>
        </button>

        {/* Mute toggle for video */}
        {hasVideo && (
          <button onClick={() => setMuted(!muted)} className="mt-2">
            {muted ? (
              <VolumeX className="w-6 h-6 text-white/60" />
            ) : (
              <Volume2 className="w-6 h-6 text-white/60" />
            )}
          </button>
        )}
      </div>

      {/* Bottom Info */}
      <div className="absolute bottom-6 left-0 right-16 px-4 z-20" dir="rtl">
        <div className="flex items-center gap-3 mb-2">
          <Link to={`/social-profile/${post.author_id}`} className="text-white font-bold text-base drop-shadow-lg hover:underline">
            {post.author_name}
          </Link>
          <button className="px-3 py-1 bg-emerald-600 text-white text-xs font-bold rounded-md">
            متابعة
          </button>
        </div>
        <p className="text-white/90 text-sm line-clamp-2 leading-relaxed drop-shadow">
          {post.content}
        </p>
      </div>
    </div>
  );
}
