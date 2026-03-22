import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import {
  Heart, MessageCircle, Share2, X, Play, Pause, Volume2, VolumeX,
  Gift, Loader2, Send, Reply, Trash2, ChevronUp, ChevronDown,
  Music2, Bookmark, UserPlus, ArrowLeft, ArrowRight
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

interface VideoPost {
  id: string;
  author_id: string;
  author_name: string;
  author_avatar?: string;
  content: string;
  title?: string;
  video_url?: string;
  image_url?: string;
  thumbnail_url?: string;
  embed_url?: string;
  content_type?: string;
  media_type?: string;
  likes_count: number;
  comments_count: number;
  shares_count?: number;
  views_count?: number;
  liked: boolean;
  saved?: boolean;
  created_at: string;
}

interface Comment {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  content: string; created_at: string; reply_to?: string;
}

function avatar(name: string, img?: string) {
  if (img) return img;
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || '?')}&background=047857&color=fff&size=80&bold=true&font-size=0.4`;
}

function getMediaUrl(url?: string) {
  if (!url) return null;
  return url.startsWith('http') ? url : `${BACKEND_URL}${url.startsWith('/') ? '' : '/'}${url}`;
}

function getYouTubeId(url: string): string | null {
  const m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|shorts\/))([^&?\s]+)/);
  return m ? m[1] : null;
}

function timeAgo(iso: string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return 'الآن';
  if (m < 60) return `${m}د`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}س`;
  const days = Math.floor(h / 24);
  if (days < 30) return `${days}ي`;
  return new Date(iso).toLocaleDateString();
}

function formatCount(n: number): string {
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return String(n);
}

/* ============ COMMENTS BOTTOM SHEET ============ */
function CommentsSheet({ postId, onClose, onCountChange }: {
  postId: string; onClose: () => void; onCountChange: (delta: number) => void;
}) {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [replyTo, setReplyTo] = useState<Comment | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/comments`, { headers: authHeaders() })
      .then(r => r.json()).then(d => { setComments(d.comments || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [postId]);

  const submit = async () => {
    if (!text.trim() || !user) return;
    try {
      const body: Record<string, string> = { content: text.trim() };
      if (replyTo) body.reply_to = replyTo.id;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/comments`, {
        method: 'POST', headers: authHeaders(), body: JSON.stringify(body),
      });
      const d = await r.json();
      if (d.comment) { setComments(prev => [...prev, d.comment]); setText(''); setReplyTo(null); onCountChange(1); }
    } catch { toast.error(t('commentFailed')); }
  };

  const deleteComment = async (cid: string) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/comments/${cid}`, { method: 'DELETE', headers: authHeaders() });
      if (r.ok) { setComments(prev => prev.filter(c => c.id !== cid)); onCountChange(-1); }
    } catch {}
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[80] bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 30, stiffness: 400 }}
        className="absolute bottom-0 left-0 right-0 max-h-[65vh] bg-[#1a1a2e] rounded-t-3xl overflow-hidden flex flex-col"
        onClick={e => e.stopPropagation()}>

        {/* Handle + Title */}
        <div className="flex flex-col items-center pt-3 pb-2 border-b border-white/10">
          <div className="w-10 h-1 bg-white/20 rounded-full mb-3" />
          <h3 className="text-white font-bold text-sm">{t('commentsTitle')} ({comments.length})</h3>
        </div>

        {/* Comments List */}
        <div className="flex-1 overflow-y-auto px-4 py-3 space-y-4" dir={dir}>
          {loading ? (
            <div className="flex justify-center py-10"><Loader2 className="w-6 h-6 animate-spin text-white/40" /></div>
          ) : comments.length === 0 ? (
            <p className="text-center text-white/40 py-10 text-sm">{t('beFirstToComment')}</p>
          ) : comments.map(c => (
            <div key={c.id} className={cn("flex gap-3", c.reply_to && "ms-8 border-s-2 border-white/10 ps-3")}>
              <img src={avatar(c.author_name, c.author_avatar)} alt="" className="w-9 h-9 rounded-full shrink-0 ring-1 ring-white/10" />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-white text-[13px] font-bold">{c.author_name}</span>
                  <span className="text-white/30 text-[10px]">{timeAgo(c.created_at)}</span>
                </div>
                <p className="text-white/80 text-[13px] mt-0.5 leading-relaxed">{c.content}</p>
                <div className="flex items-center gap-4 mt-1.5">
                  <button onClick={() => { setReplyTo(c); inputRef.current?.focus(); }}
                    className="flex items-center gap-1 text-[11px] text-white/40 hover:text-white/70">
                    <Reply className="w-3 h-3" /> {t('replyLabel')}
                  </button>
                  {user && (c.author_id === user.id) && (
                    <button onClick={() => deleteComment(c.id)}
                      className="flex items-center gap-1 text-[11px] text-white/40 hover:text-red-400">
                      <Trash2 className="w-3 h-3" /> {t('deleteLabel')}
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Reply indicator */}
        {replyTo && (
          <div className="px-4 py-2 bg-white/5 flex items-center justify-between border-t border-white/5" dir={dir}>
            <span className="text-xs text-emerald-400">{t('replyTo')} {replyTo.author_name}</span>
            <button onClick={() => setReplyTo(null)}><X className="w-3.5 h-3.5 text-white/40" /></button>
          </div>
        )}

        {/* Input */}
        {user ? (
          <div className="flex items-center gap-2 p-3 border-t border-white/10 bg-[#1a1a2e]" dir={dir}
            style={{ paddingBottom: 'max(12px, env(safe-area-inset-bottom, 12px))' }}>
            <img src={avatar(user.name || '', user.avatar)} alt="" className="w-8 h-8 rounded-full shrink-0" />
            <input ref={inputRef} value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && submit()}
              placeholder={replyTo ? `${t('replyToPlaceholder')} ${replyTo.author_name}...` : t('writeComment')}
              className="flex-1 bg-white/10 text-white rounded-full px-4 py-2.5 text-sm placeholder:text-white/30 outline-none focus:bg-white/15 transition-colors" />
            <button onClick={submit} disabled={!text.trim()}
              className="w-9 h-9 rounded-full bg-emerald-500 flex items-center justify-center disabled:opacity-30 active:scale-90 transition-transform">
              <Send className="w-4 h-4 text-white" />
            </button>
          </div>
        ) : (
          <div className="p-4 border-t border-white/10 text-center"
            style={{ paddingBottom: 'max(12px, env(safe-area-inset-bottom, 12px))' }}>
            <Link to="/auth" className="text-emerald-400 text-sm font-bold hover:underline">{t('loginToComment')}</Link>
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}

/* ============ SINGLE REEL SLIDE ============ */
function ReelSlide({ post, isActive, onLike, onComment, onShare, onFollow, isFollowed }: {
  post: VideoPost; isActive: boolean;
  onLike: () => void; onComment: () => void; onShare: () => void;
  onFollow: () => void; isFollowed: boolean;
}) {
  const { t, dir } = useLocale();
  const { user } = useAuth();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(false);
  const [paused, setPaused] = useState(false);
  const [progress, setProgress] = useState(0);
  const [showPlayIcon, setShowPlayIcon] = useState(false);

  const isEmbed = post.media_type === 'embed';
  const ytId = isEmbed && post.embed_url ? getYouTubeId(post.embed_url) : null;
  const mediaUrl = getMediaUrl(post.video_url || post.image_url);
  const isVideo = post.media_type === 'video' || post.content_type?.includes('video') || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));

  useEffect(() => {
    if (!videoRef.current) return;
    if (isActive) {
      videoRef.current.play().catch(() => {});
      setPaused(false);
    } else {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
      setProgress(0);
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
    setShowPlayIcon(true);
    setTimeout(() => setShowPlayIcon(false), 600);
  };

  const handleTimeUpdate = () => {
    if (!videoRef.current) return;
    const pct = (videoRef.current.currentTime / videoRef.current.duration) * 100;
    setProgress(pct);
  };

  const handleDoubleTap = useCallback(() => {
    if (!post.liked) onLike();
  }, [post.liked, onLike]);

  let lastTap = useRef(0);
  const handleTap = () => {
    const now = Date.now();
    if (now - lastTap.current < 300) {
      handleDoubleTap();
    } else {
      if (isVideo) togglePlay();
    }
    lastTap.current = now;
  };

  return (
    <div className="h-[100dvh] w-full snap-start relative flex items-center justify-center bg-black overflow-hidden select-none">
      {/* Background Media */}
      {ytId ? (
        <iframe
          src={`https://www.youtube.com/embed/${ytId}?autoplay=${isActive ? 1 : 0}&rel=0&loop=1&controls=0&playsinline=1&mute=${muted ? 1 : 0}`}
          className="absolute inset-0 w-full h-full pointer-events-none" frameBorder={0}
          allow="autoplay; encrypted-media"
        />
      ) : isVideo && mediaUrl ? (
        <video
          ref={videoRef}
          src={mediaUrl}
          className="absolute inset-0 w-full h-full object-contain"
          loop muted={muted} playsInline
          onTimeUpdate={handleTimeUpdate}
          onClick={handleTap}
        />
      ) : mediaUrl ? (
        <div className="absolute inset-0" onClick={handleTap}>
          <img src={mediaUrl} alt="" className="w-full h-full object-cover" />
          <div className="absolute inset-0 bg-black/20" />
        </div>
      ) : (
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-950 via-gray-950 to-black" onClick={handleTap} />
      )}

      {/* Play/Pause indicator */}
      <AnimatePresence>
        {showPlayIcon && (
          <motion.div
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 1.5, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none"
          >
            <div className="w-20 h-20 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center">
              {paused ? <Play className="w-10 h-10 text-white fill-white ms-1" /> : <Pause className="w-10 h-10 text-white" />}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Top gradient for safe area */}
      <div className="absolute top-0 left-0 right-0 h-28 bg-gradient-to-b from-black/50 to-transparent z-10 pointer-events-none" />

      {/* Right Side Actions */}
      <div className="absolute end-3 bottom-28 flex flex-col items-center gap-5 z-20"
        style={{ marginBottom: 'env(safe-area-inset-bottom, 0px)' }}>

        {/* Author Avatar + Follow */}
        <div className="relative mb-1">
          <Link to={`/social-profile/${post.author_id}`}>
            <img src={avatar(post.author_name, post.author_avatar)} alt=""
              className="w-12 h-12 rounded-full border-[2.5px] border-white shadow-lg shadow-black/30" />
          </Link>
          {user && user.id !== post.author_id && !isFollowed && (
            <button onClick={onFollow}
              className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-6 h-6 rounded-full bg-rose-500 flex items-center justify-center shadow-lg shadow-rose-500/30 active:scale-90 transition-transform">
              <UserPlus className="w-3 h-3 text-white" />
            </button>
          )}
        </div>

        {/* Like */}
        <button onClick={onLike} className="flex flex-col items-center active:scale-90 transition-transform">
          <div className={cn("w-12 h-12 rounded-full flex items-center justify-center",
            post.liked ? "bg-rose-500/20" : "bg-white/10 backdrop-blur-sm")}>
            <Heart className={cn("w-7 h-7 drop-shadow-lg transition-all",
              post.liked ? "fill-rose-500 text-rose-500 scale-110" : "text-white")} />
          </div>
          <span className="text-white text-[11px] mt-1 font-bold drop-shadow">{formatCount(post.likes_count)}</span>
        </button>

        {/* Comments */}
        <button onClick={onComment} className="flex flex-col items-center active:scale-90 transition-transform">
          <div className="w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
            <MessageCircle className="w-7 h-7 text-white drop-shadow-lg" />
          </div>
          <span className="text-white text-[11px] mt-1 font-bold drop-shadow">{formatCount(post.comments_count)}</span>
        </button>

        {/* Share */}
        <button onClick={onShare} className="flex flex-col items-center active:scale-90 transition-transform">
          <div className="w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
            <Share2 className="w-6 h-6 text-white drop-shadow-lg" />
          </div>
          <span className="text-white text-[11px] mt-1 font-bold drop-shadow">{formatCount(post.shares_count || 0)}</span>
        </button>

        {/* Mute/Unmute */}
        {(isVideo || ytId) && (
          <button onClick={() => setMuted(!muted)}
            className="w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center active:scale-90 transition-transform">
            {muted ? <VolumeX className="w-5 h-5 text-white/60" /> : <Volume2 className="w-5 h-5 text-white/60" />}
          </button>
        )}

        {/* Music disc animation */}
        <motion.div
          animate={isActive && !paused ? { rotate: 360 } : {}}
          transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
          className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-800 to-gray-900 border-2 border-gray-700 flex items-center justify-center shadow-lg"
        >
          <div className="w-4 h-4 rounded-full bg-white/20" />
        </motion.div>
      </div>

      {/* Bottom Content */}
      <div className="absolute bottom-0 left-0 right-0 z-20 pointer-events-none"
        style={{ paddingBottom: 'max(16px, env(safe-area-inset-bottom, 16px))' }}>
        {/* Bottom gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />

        <div className="relative px-4 pe-20 pb-2" dir={dir}>
          {/* Author + Follow */}
          <div className="flex items-center gap-2 mb-2 pointer-events-auto">
            <Link to={`/social-profile/${post.author_id}`}
              className="text-white font-bold text-[15px] drop-shadow-lg hover:underline">
              @{post.author_name}
            </Link>
            {user && user.id !== post.author_id && !isFollowed && (
              <button onClick={onFollow}
                className="px-3 py-1 bg-white/20 backdrop-blur-sm text-white text-[11px] font-bold rounded-lg border border-white/20 active:scale-95 transition-transform">
                {t('follow')}
              </button>
            )}
          </div>

          {/* Content/Caption */}
          <p className="text-white/90 text-[13px] leading-relaxed drop-shadow line-clamp-3 mb-2">
            {post.title && <span className="font-bold">{post.title} </span>}
            {post.content}
          </p>

          {/* Music bar */}
          <div className="flex items-center gap-2 overflow-hidden">
            <Music2 className="w-3.5 h-3.5 text-white/50 shrink-0" />
            <div className="overflow-hidden">
              <motion.p
                animate={{ x: isActive ? [0, -200, 0] : 0 }}
                transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}
                className="text-white/50 text-[11px] whitespace-nowrap"
              >
                {post.author_name} • Original Sound
              </motion.p>
            </div>
          </div>
        </div>

        {/* Progress bar */}
        {isVideo && (
          <div className="relative h-[3px] bg-white/20 w-full">
            <motion.div
              className="absolute top-0 start-0 h-full bg-white rounded-full"
              style={{ width: `${progress}%` }}
              transition={{ duration: 0.1 }}
            />
          </div>
        )}
      </div>
    </div>
  );
}

/* ============ MAIN REELS PAGE ============ */
export default function VideoReels() {
  const { t, dir } = useLocale();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [posts, setPosts] = useState<VideoPost[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showComments, setShowComments] = useState(false);
  const [followedIds, setFollowedIds] = useState<Set<string>>(new Set());
  const [activeTab, setActiveTab] = useState<'forYou' | 'following'>('forYou');
  const containerRef = useRef<HTMLDivElement>(null);

  const fetchPosts = useCallback(async () => {
    try {
      const headers: Record<string, string> = {};
      const tk = getToken();
      if (tk) headers.Authorization = `Bearer ${tk}`;

      const endpoint = activeTab === 'following' && user
        ? `${BACKEND_URL}/api/sohba/feed/following?limit=30`
        : `${BACKEND_URL}/api/sohba/explore?limit=30`;

      const res = await fetch(endpoint, { headers });
      const data = await res.json();
      setPosts(data.posts || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [activeTab, user]);

  useEffect(() => {
    setLoading(true);
    setCurrentIndex(0);
    fetchPosts();
  }, [fetchPosts]);

  const handleScroll = useCallback(() => {
    if (!containerRef.current) return;
    const scrollTop = containerRef.current.scrollTop;
    const height = containerRef.current.clientHeight;
    const newIndex = Math.round(scrollTop / height);
    if (newIndex !== currentIndex && newIndex >= 0 && newIndex < posts.length) {
      setCurrentIndex(newIndex);
    }
  }, [currentIndex, posts.length]);

  const handleLike = async (postId: string, index: number) => {
    if (!user) { toast.error(t('loginRequired')); return; }
    try {
      const res = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/like`, {
        method: 'POST', headers: authHeaders(),
      });
      const data = await res.json();
      setPosts(prev => prev.map((p, i) =>
        i === index ? { ...p, liked: data.liked, likes_count: data.liked ? p.likes_count + 1 : p.likes_count - 1 } : p
      ));
    } catch {}
  };

  const handleShare = async (postId: string) => {
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/share`, { method: 'POST', headers: authHeaders() });
    } catch {}
    const post = posts.find(p => p.id === postId);
    if (navigator.share && post) {
      navigator.share({ title: post.title || '', text: post.content }).catch(() => {});
    } else {
      toast.success(t('contentCopied'));
    }
  };

  const handleFollow = async (userId: string) => {
    if (!user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/follow/${userId}`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setFollowedIds(prev => {
        const n = new Set(prev);
        d.following ? n.add(userId) : n.delete(userId);
        return n;
      });
    } catch {}
  };

  if (loading) {
    return (
      <div className="h-[100dvh] bg-black flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 animate-spin text-white/40" />
          <p className="text-white/30 text-sm">{t('discoverReels')}</p>
        </div>
      </div>
    );
  }

  if (posts.length === 0) {
    return (
      <div className="h-[100dvh] bg-black flex flex-col items-center justify-center px-6">
        <div className="w-24 h-24 rounded-full bg-white/5 flex items-center justify-center mb-6">
          <Play className="w-12 h-12 text-white/20" />
        </div>
        <h2 className="text-white text-xl font-bold mb-2">{t('noReelsYet')}</h2>
        <p className="text-white/40 text-sm text-center mb-8">{t('noContent')}</p>
        <button onClick={() => navigate('/stories?create=true')}
          className="px-8 py-3 bg-emerald-500 text-white rounded-full font-bold text-sm active:scale-95 transition-transform">
          {t('createContent')}
        </button>
        <button onClick={() => navigate(-1)}
          className="mt-4 px-6 py-2 text-white/50 text-sm active:scale-95">
          {dir === 'rtl' ? <ArrowRight className="inline w-4 h-4 me-1" /> : <ArrowLeft className="inline w-4 h-4 me-1" />}
          {t('back') || 'رجوع'}
        </button>
      </div>
    );
  }

  return (
    <div className="h-[100dvh] bg-black relative overflow-hidden">
      {/* Top Header - over content */}
      <div className="absolute top-0 left-0 right-0 z-30"
        style={{ paddingTop: 'max(12px, env(safe-area-inset-top, 12px))' }}>
        <div className="flex items-center justify-between px-4 py-2">
          <button onClick={() => navigate(-1)}
            className="w-10 h-10 rounded-full bg-black/30 backdrop-blur-md flex items-center justify-center active:scale-90 transition-transform">
            {dir === 'rtl' ? <ArrowRight className="w-5 h-5 text-white" /> : <ArrowLeft className="w-5 h-5 text-white" />}
          </button>

          {/* Tabs */}
          <div className="flex items-center gap-6">
            <button onClick={() => setActiveTab('following')}
              className={cn("text-sm font-bold transition-all pb-0.5",
                activeTab === 'following' ? "text-white border-b-2 border-white" : "text-white/50")}>
              {t('followingTab')}
            </button>
            <button onClick={() => setActiveTab('forYou')}
              className={cn("text-sm font-bold transition-all pb-0.5",
                activeTab === 'forYou' ? "text-white border-b-2 border-white" : "text-white/50")}>
              {t('forYouTab')}
            </button>
          </div>

          <div className="w-10" />
        </div>
      </div>

      {/* Reels Container */}
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className="h-full overflow-y-scroll snap-y snap-mandatory"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none', WebkitOverflowScrolling: 'touch' }}
      >
        {posts.map((post, index) => (
          <ReelSlide
            key={post.id}
            post={post}
            isActive={index === currentIndex}
            onLike={() => handleLike(post.id, index)}
            onComment={() => setShowComments(true)}
            onShare={() => handleShare(post.id)}
            onFollow={() => handleFollow(post.author_id)}
            isFollowed={followedIds.has(post.author_id)}
          />
        ))}
      </div>

      {/* Comments Sheet */}
      <AnimatePresence>
        {showComments && posts[currentIndex] && (
          <CommentsSheet
            postId={posts[currentIndex].id}
            onClose={() => setShowComments(false)}
            onCountChange={d => setPosts(prev => prev.map((p, i) =>
              i === currentIndex ? { ...p, comments_count: p.comments_count + d } : p
            ))}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
