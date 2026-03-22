import { useState, useEffect, useRef, useCallback } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Heart, MessageCircle, Gift, Share2, ArrowRight, Play, Pause, Volume2, VolumeX, X, Send, Reply, Trash2, Loader2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const tk = getToken(); if (tk) h['Authorization'] = `Bearer ${tk}`;
  return h;
}

function avatar(name: string, img?: string) {
  if (img) return img;
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || '?')}&background=047857&color=fff&size=80`;
}

function timeAgo(iso: string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return 'now';
  if (m < 60) return `${m}m`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h`;
  const days = Math.floor(h / 24);
  return `${days}d`;
}

/* ==================== COMMENTS SHEET for Reels ==================== */
function ReelCommentsSheet({ postId, onClose }: { postId: string; onClose: () => void }) {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  interface Comment { id: string; author_id: string; author_name: string; author_avatar?: string; content: string; created_at: string; reply_to?: string; }
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
      const body: any = { content: text.trim() };
      if (replyTo) body.reply_to = replyTo.id;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/comments`, {
        method: 'POST', headers: authHeaders(), body: JSON.stringify(body),
      });
      const d = await r.json();
      if (d.comment) { setComments(prev => [...prev, d.comment]); setText(''); setReplyTo(null); }
    } catch { toast.error(t('commentFailed')); }
  };

  const deleteComment = async (cid: string) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/comments/${cid}`, { method: 'DELETE', headers: authHeaders() });
      if (r.ok) { setComments(prev => prev.filter(c => c.id !== cid)); toast.success(t('deleted')); }
    } catch {}
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="absolute bottom-0 left-0 right-0 max-h-[70vh] bg-card rounded-t-[28px] overflow-hidden flex flex-col border-t border-primary/30"
        onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between px-5 py-4 border-b border-border/20">
          <h3 className="text-foreground font-bold">{t('commentsTitle')} ({comments.length})</h3>
          <button onClick={onClose} className="p-1.5 rounded-full bg-muted/30 hover:bg-muted/50"><X className="w-4 h-4 text-muted-foreground" /></button>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4" dir={dir}>
          {loading ? <div className="flex justify-center py-8"><Loader2 className="w-6 h-6 animate-spin text-emerald-500" /></div>
           : comments.length === 0 ? <p className="text-center text-muted-foreground py-8 text-sm">{t('beFirstToComment')}</p>
           : comments.map(c => {
            const canDel = user && (c.author_id === user.id || user.email === 'mohammadalrejab@gmail.com');
            return (
              <div key={c.id} className={`flex gap-2.5 ${c.reply_to ? 'ms-8 border-s-2 border-emerald-900/50 ps-3' : ''}`}>
                <img src={avatar(c.author_name, c.author_avatar)} alt="" className="w-8 h-8 rounded-full shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] font-bold text-foreground">{c.author_name}</span>
                    <span className="text-[10px] text-muted-foreground">{timeAgo(c.created_at)}</span>
                  </div>
                  <p className="text-foreground/80 text-[13px] mt-0.5 leading-relaxed">{c.content}</p>
                  <div className="flex items-center gap-4 mt-1">
                    <button onClick={() => { setReplyTo(c); inputRef.current?.focus(); }}
                      className="flex items-center gap-1 text-[11px] text-muted-foreground hover:text-emerald-500">
                      <Reply className="w-3 h-3" /> {t('replyLabel')}
                    </button>
                    {canDel && (
                      <button onClick={() => deleteComment(c.id)}
                        className="flex items-center gap-1 text-[11px] text-muted-foreground hover:text-red-500">
                        <Trash2 className="w-3 h-3" /> {t('deleteLabel')}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        {replyTo && (
          <div className="px-4 py-2 bg-emerald-900/20 flex items-center justify-between border-t border-border/20" dir={dir}>
            <span className="text-xs text-emerald-500">{t('replyTo')} {replyTo.author_name}</span>
            <button onClick={() => setReplyTo(null)}><X className="w-3.5 h-3.5 text-muted-foreground" /></button>
          </div>
        )}
        {user ? (
          <div className="flex items-center gap-2 p-3 border-t border-border/20 bg-card" dir={dir}>
            <input ref={inputRef} value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && submit()}
              placeholder={replyTo ? `${t('replyToPlaceholder')} ${replyTo.author_name}...` : t('writeComment')}
              className="flex-1 bg-muted/30 text-foreground rounded-full px-4 py-2.5 text-sm placeholder:text-muted-foreground/60 border border-border/20 outline-none focus:border-emerald-600/50" />
            <button onClick={submit} disabled={!text.trim()}
              className="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center disabled:opacity-30 active:scale-90">
              <Send className="w-4 h-4 text-white" />
            </button>
          </div>
        ) : (
          <div className="p-4 border-t border-border/20 text-center">
            <Link to="/auth" className="text-emerald-500 text-sm font-bold hover:underline">{t('loginToComment')}</Link>
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}

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
  const [followedIds, setFollowedIds] = useState<Set<string>>(new Set());
  const [showCommentsFor, setShowCommentsFor] = useState<string | null>(null);
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
      if (navigator.share) {
        const post = posts.find(p => p.id === postId);
        navigator.share({ title: t('videoTab'), text: post?.content || '' }).catch(() => {});
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleFollow = async (userId: string) => {
    if (!user) return;
    const token = getToken();
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/follow/${userId}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
      const d = await r.json();
      setFollowedIds(prev => {
        const n = new Set(prev);
        d.following ? n.add(userId) : n.delete(userId);
        return n;
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
            onFollow={() => handleFollow(post.author_id)}
            onComment={() => setShowCommentsFor(post.id)}
            getMediaUrl={getMediaUrl}
            t={t}
            followed={followedIds.has(post.author_id)}
          />
        ))}
      </div>

      {/* Comments Sheet */}
      <AnimatePresence>
        {showCommentsFor && (
          <ReelCommentsSheet postId={showCommentsFor} onClose={() => setShowCommentsFor(null)} />
        )}
      </AnimatePresence>
    </div>
  );
}

function ReelItem({ post, isActive, onLike, onShare, onFollow, onComment, getMediaUrl, t, followed }: {
  post: VideoPost;
  isActive: boolean;
  onLike: () => void;
  onShare: () => void;
  onFollow: () => void;
  onComment: () => void;
  getMediaUrl: (url?: string) => string;
  t: (key: string) => string;
  followed: boolean;
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
      <div className="absolute end-2.5 bottom-32 flex flex-col items-center gap-4 z-20"
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
        <button onClick={onComment} className="flex flex-col items-center active:scale-90 transition-transform">
          <MessageCircle className="w-6 h-6 text-white drop-shadow-lg" />
          <span className="text-white text-[10px] mt-0.5 font-bold drop-shadow">{post.comments_count}</span>
        </button>

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
      </div>

      {/* Mute toggle for video - separated below to avoid overlap */}
      {hasVideo && (
        <div className="absolute end-3 bottom-16 z-20"
          style={{ marginBottom: 'env(safe-area-inset-bottom, 0px)' }}>
          <button onClick={() => setMuted(!muted)} className="w-9 h-9 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center active:scale-90 transition-transform">
            {muted ? (
              <VolumeX className="w-4 h-4 text-white/70" />
            ) : (
              <Volume2 className="w-4 h-4 text-white/70" />
            )}
          </button>
        </div>
      )}

      {/* Bottom Info */}
      <div className="absolute bottom-5 left-0 right-14 px-3.5 z-20" dir={dir}
        style={{ paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}>
        <div className="flex items-center gap-2 mb-1.5">
          <Link to={`/social-profile/${post.author_id}`} className="text-white font-bold text-[14px] drop-shadow-lg hover:underline">
            {post.author_name}
          </Link>
          <button onClick={onFollow}
            className={`px-2 py-0.5 ${followed ? 'bg-white/20' : 'bg-emerald-600'} text-white text-[10px] font-bold rounded-md active:scale-95 transition-transform`}>
            {followed ? t('unfollow') : t('follow')}
          </button>
        </div>
        <p className="text-white/85 text-[12px] line-clamp-2 leading-relaxed drop-shadow">
          {post.content}
        </p>
      </div>
    </div>
  );
}
