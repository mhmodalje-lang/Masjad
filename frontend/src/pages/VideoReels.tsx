import { useState, useEffect, useRef, useCallback } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Heart, MessageCircle, Share2, ArrowRight, Play, Pause,
  Volume2, VolumeX, X, Send, Reply, Trash2, Loader2, Flag,
  Bookmark, MoreVertical, Pencil, ChevronDown
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import ReportSheet from '@/components/ReportSheet';

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
  if (days < 30) return `${days}d`;
  const months = Math.floor(days / 30);
  return `${months}mo`;
}

function truncateWords(text: string, maxWords: number): { truncated: string; isTruncated: boolean } {
  if (!text) return { truncated: '', isTruncated: false };
  const words = text.split(/\s+/);
  if (words.length <= maxWords) return { truncated: text, isTruncated: false };
  return { truncated: words.slice(0, maxWords).join(' ') + ' ...', isTruncated: true };
}

function formatCount(n: number): string {
  if (n >= 1000000) return (n / 1000000).toFixed(1).replace('.0', '') + 'M';
  if (n >= 1000) return (n / 1000).toFixed(1).replace('.0', '') + 'K';
  return String(n || 0);
}

/* ==================== INSTAGRAM-STYLE COMMENTS SHEET ==================== */
function ReelCommentsSheet({ post, onClose, getMediaUrl }: {
  post: VideoPost;
  onClose: () => void;
  getMediaUrl: (url?: string) => string;
}) {
  const { user, getToken } = useAuth();
  const { t, dir } = useLocale();
  interface Comment { id: string; author_id: string; author_name: string; author_avatar?: string; content: string; created_at: string; reply_to?: string; }
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [replyTo, setReplyTo] = useState<Comment | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`, { headers: authHeaders() })
      .then(r => r.json()).then(d => { setComments(d.comments || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [post.id]);

  const submit = async () => {
    if (!text.trim() || !user) return;
    try {
      const body: any = { content: text.trim() };
      if (replyTo) body.reply_to = replyTo.id;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`, {
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
      className="fixed inset-0 z-[60] bg-black/80 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="absolute bottom-0 left-0 right-0 max-h-[90vh] bg-[#1a1a1a] rounded-t-[20px] overflow-hidden flex flex-col"
        onClick={e => e.stopPropagation()}>

        {/* Handle bar */}
        <div className="flex justify-center pt-2 pb-1">
          <div className="w-10 h-1 rounded-full bg-white/20" />
        </div>

        {/* Video Preview at top */}
        <div className="relative w-full aspect-video bg-black mx-auto max-w-sm rounded-lg overflow-hidden mx-3">
          {post.video_url ? (
            <video src={getMediaUrl(post.video_url)} className="w-full h-full object-cover" muted playsInline loop autoPlay />
          ) : post.image_url ? (
            <img src={getMediaUrl(post.image_url)} alt="" className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-emerald-900 to-black flex items-center justify-center">
              <p className="text-white/80 text-sm text-center px-4" dir={dir}>{post.content}</p>
            </div>
          )}
          {/* Sound button */}
          <button className="absolute bottom-2 left-2 w-7 h-7 rounded-full bg-black/50 flex items-center justify-center">
            <Volume2 className="w-3.5 h-3.5 text-white/70" />
          </button>
        </div>

        {/* Author info + Description */}
        <div className="px-4 pt-3 pb-2" dir={dir}>
          {/* Author row */}
          <div className="flex items-center gap-2.5 mb-2">
            <Link to={`/social-profile/${post.author_id}`} className="relative">
              <div className="p-[2px] rounded-full bg-gradient-to-tr from-amber-500 via-pink-500 to-purple-600">
                <img src={avatar(post.author_name, post.author_avatar)} alt="" className="w-9 h-9 rounded-full border-2 border-[#1a1a1a]" />
              </div>
            </Link>
            <Link to={`/social-profile/${post.author_id}`} className="font-bold text-white text-[14px]">{post.author_name}</Link>
            <button onClick={() => {
              const token = getToken();
              if (token) {
                fetch(`${BACKEND_URL}/api/sohba/follow/${post.author_id}`, { method: 'POST', headers: { Authorization: `Bearer ${token}` } })
                  .then(r => r.json()).then(d => toast.success(d.following ? t('followed') : t('unfollowed')))
                  .catch(() => {});
              }
            }} className="ms-auto px-3 py-1 border border-white/30 rounded-lg text-white text-[12px] font-medium active:scale-95 transition-transform">
              {t('follow')}
            </button>
          </div>
          {/* Full description */}
          <p className="text-white text-[14px] leading-relaxed mb-1">{post.content}</p>
          <span className="text-white/40 text-[12px]">{timeAgo(post.created_at)}</span>
        </div>

        {/* Divider */}
        <div className="border-t border-white/10 mx-4" />

        {/* Comments */}
        <div className="flex-1 overflow-y-auto px-4 py-3 space-y-4 min-h-[150px]" dir={dir}>
          {loading ? (
            <div className="flex justify-center py-8"><Loader2 className="w-6 h-6 animate-spin text-white/30" /></div>
          ) : comments.length === 0 ? (
            <p className="text-center text-white/30 py-8 text-sm">{t('beFirstToComment')}</p>
          ) : comments.map(c => {
            const canDel = user && (c.author_id === user.id || user.email === 'mohammadalrejab@gmail.com');
            return (
              <div key={c.id} className={`flex gap-2.5 ${c.reply_to ? 'ms-8 border-s-2 border-white/10 ps-3' : ''}`}>
                <img src={avatar(c.author_name, c.author_avatar)} alt="" className="w-8 h-8 rounded-full shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] font-bold text-white">{c.author_name}</span>
                    <span className="text-[10px] text-white/30">{timeAgo(c.created_at)}</span>
                  </div>
                  <p className="text-white/80 text-[13px] mt-0.5 leading-relaxed">{c.content}</p>
                  <div className="flex items-center gap-4 mt-1.5">
                    <button onClick={() => { setReplyTo(c); inputRef.current?.focus(); }}
                      className="text-[11px] text-white/40 font-medium">{t('replyLabel')}</button>
                    {canDel && (
                      <button onClick={() => deleteComment(c.id)}
                        className="text-[11px] text-red-400/60 font-medium">{t('deleteLabel')}</button>
                    )}
                  </div>
                </div>
                {/* Like on comment */}
                <button className="shrink-0 mt-3">
                  <Heart className="w-3.5 h-3.5 text-white/30" />
                </button>
              </div>
            );
          })}
        </div>

        {/* Reply indicator */}
        {replyTo && (
          <div className="px-4 py-2 bg-white/5 flex items-center justify-between border-t border-white/10" dir={dir}>
            <span className="text-xs text-white/40">{t('replyTo')} {replyTo.author_name}</span>
            <button onClick={() => setReplyTo(null)}><X className="w-3.5 h-3.5 text-white/40" /></button>
          </div>
        )}

        {/* Comment input */}
        {user ? (
          <div className="flex items-center gap-2.5 px-4 py-3 border-t border-white/10 bg-[#1a1a1a]" dir={dir}>
            <img src={avatar(user.name || '', user.avatar)} alt="" className="w-8 h-8 rounded-full shrink-0" />
            <input ref={inputRef} value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && submit()}
              placeholder={replyTo ? `${t('replyToPlaceholder')} ${replyTo.author_name}...` : `${t('addCommentFor')} ${post.author_name}...`}
              className="flex-1 bg-transparent text-white text-sm placeholder:text-white/30 outline-none"
              style={{ paddingBottom: 'env(safe-area-inset-bottom, 0px)' }} />
            <button onClick={submit} disabled={!text.trim()}
              className="text-emerald-500 text-sm font-bold disabled:opacity-20">
              <Send className="w-5 h-5" />
            </button>
          </div>
        ) : (
          <div className="p-4 border-t border-white/10 text-center">
            <Link to="/auth" className="text-emerald-500 text-sm font-bold">{t('loginToComment')}</Link>
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}

/* ==================== EDIT DESCRIPTION SHEET ==================== */
function EditDescSheet({ post, onClose, onSaved }: {
  post: VideoPost;
  onClose: () => void;
  onSaved: (newContent: string) => void;
}) {
  const { t, dir } = useLocale();
  const [content, setContent] = useState(post.content || '');
  const [saving, setSaving] = useState(false);

  const save = async () => {
    setSaving(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}`, {
        method: 'PATCH', headers: authHeaders(), body: JSON.stringify({ content }),
      });
      if (r.ok) { onSaved(content); toast.success(t('saved') || 'Saved'); onClose(); }
      else toast.error(t('error'));
    } catch { toast.error(t('error')); }
    setSaving(false);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[70] bg-black/70 backdrop-blur-sm flex items-end justify-center" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="w-full max-w-lg bg-[#1a1a1a] rounded-t-[20px] overflow-hidden" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
          <button onClick={onClose} className="text-white/50 text-sm">{t('cancel') || 'Cancel'}</button>
          <h3 className="text-white font-bold text-sm">{t('editDescription') || 'Edit'}</h3>
          <button onClick={save} disabled={saving} className="text-emerald-500 font-bold text-sm disabled:opacity-30">
            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : (t('save') || 'Save')}
          </button>
        </div>
        <div className="p-4" dir={dir}>
          <textarea
            value={content}
            onChange={e => setContent(e.target.value)}
            className="w-full bg-white/5 text-white rounded-xl px-4 py-3 text-sm border border-white/10 outline-none focus:border-emerald-500/50 resize-none h-32 placeholder:text-white/30"
            dir="auto"
          />
        </div>
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
  saved?: boolean;
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
  const [reportTarget, setReportTarget] = useState<{ id: string; userId: string } | null>(null);
  const [editingPost, setEditingPost] = useState<VideoPost | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchVideos();
  }, []);

  const fetchVideos = async () => {
    try {
      const token = getToken();
      const headers: Record<string, string> = {};
      if (token) headers.Authorization = `Bearer ${token}`;
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
        method: 'POST', headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setPosts(prev => prev.map((p, i) =>
        i === index ? { ...p, liked: data.liked, likes_count: data.liked ? p.likes_count + 1 : p.likes_count - 1 } : p
      ));
    } catch (err) { console.error(err); }
  };

  const handleShare = async (postId: string) => {
    const token = getToken();
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/share`, {
        method: 'POST', headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (navigator.share) {
        const post = posts.find(p => p.id === postId);
        navigator.share({ title: t('videoTab'), text: post?.content || '' }).catch(() => {});
      }
    } catch (err) { console.error(err); }
  };

  const handleFollow = async (userId: string) => {
    if (!user) return;
    const token = getToken();
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/follow/${userId}`, {
        method: 'POST', headers: { Authorization: `Bearer ${token}` },
      });
      const d = await r.json();
      setFollowedIds(prev => { const n = new Set(prev); d.following ? n.add(userId) : n.delete(userId); return n; });
    } catch (err) { console.error(err); }
  };

  const handleDelete = async (postId: string) => {
    if (!user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}`, {
        method: 'DELETE', headers: authHeaders(),
      });
      if (r.ok) {
        setPosts(prev => prev.filter(p => p.id !== postId));
        toast.success(t('deleted'));
      }
    } catch { toast.error(t('error')); }
  };

  const handleSave = async (postId: string, index: number) => {
    if (!user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/save`, {
        method: 'POST', headers: authHeaders(),
      });
      const d = await r.json();
      setPosts(prev => prev.map((p, i) => i === index ? { ...p, saved: d.saved } : p));
    } catch {}
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
    if (newIndex !== currentIndex) setCurrentIndex(newIndex);
  }, [currentIndex]);

  if (loading) {
    return (
      <div className="h-screen bg-black flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const commentsPost = posts.find(p => p.id === showCommentsFor);

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
      <div ref={containerRef} onScroll={handleScroll}
        className="h-full overflow-y-scroll snap-y snap-mandatory"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none', WebkitOverflowScrolling: 'touch' }}>
        {posts.map((post, index) => (
          <ReelItem
            key={post.id}
            post={post}
            isActive={index === currentIndex}
            isOwner={!!user && post.author_id === user.id}
            onLike={() => handleLike(post.id, index)}
            onShare={() => handleShare(post.id)}
            onFollow={() => handleFollow(post.author_id)}
            onComment={() => setShowCommentsFor(post.id)}
            onSave={() => handleSave(post.id, index)}
            onDelete={() => handleDelete(post.id)}
            onEdit={() => setEditingPost(post)}
            onReport={(id: string, userId: string) => setReportTarget({ id, userId })}
            getMediaUrl={getMediaUrl}
            t={t}
            followed={followedIds.has(post.author_id)}
          />
        ))}
      </div>

      {/* Modals */}
      <AnimatePresence>
        {commentsPost && (
          <ReelCommentsSheet post={commentsPost} onClose={() => setShowCommentsFor(null)} getMediaUrl={getMediaUrl} />
        )}
        {reportTarget && (
          <ReportSheet contentId={reportTarget.id} contentType="post" reportedUserId={reportTarget.userId} onClose={() => setReportTarget(null)} />
        )}
        {editingPost && (
          <EditDescSheet post={editingPost} onClose={() => setEditingPost(null)}
            onSaved={(newContent) => setPosts(prev => prev.map(p => p.id === editingPost.id ? { ...p, content: newContent } : p))} />
        )}
      </AnimatePresence>
    </div>
  );
}


/* ==================== REEL ITEM - INSTAGRAM STYLE ==================== */
function ReelItem({ post, isActive, isOwner, onLike, onShare, onFollow, onComment, onSave, onDelete, onEdit, onReport, getMediaUrl, t, followed }: {
  post: VideoPost;
  isActive: boolean;
  isOwner: boolean;
  onLike: () => void;
  onShare: () => void;
  onFollow: () => void;
  onComment: () => void;
  onSave: () => void;
  onDelete: () => void;
  onEdit: () => void;
  onReport: (id: string, userId: string) => void;
  getMediaUrl: (url?: string) => string;
  t: (key: string) => string;
  followed: boolean;
}) {
  const { user } = useAuth();
  const { dir } = useLocale();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(true);
  const [descExpanded, setDescExpanded] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [showMuteIcon, setShowMuteIcon] = useState(false);
  const hasVideo = post.video_url;
  const isEmbed = post.embed_url;
  const ytId = isEmbed ? (() => { try { const u = new URL(post.embed_url || ''); return u.searchParams.get('v') || u.pathname.split('/').pop(); } catch { return null; } })() : null;

  useEffect(() => {
    if (!videoRef.current) return;
    if (isActive) videoRef.current.play().catch(() => {});
    else { videoRef.current.pause(); videoRef.current.currentTime = 0; }
  }, [isActive]);

  /* Tap = mute/unmute, Double-tap = like */
  const lastTap = useRef(0);
  const onTap = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('button, a, iframe')) return;
    const now = Date.now();
    if (now - lastTap.current < 300) {
      if (!post.liked) onLike();
    } else {
      setMuted(m => !m);
      if (videoRef.current) videoRef.current.muted = !muted;
      setShowMuteIcon(true);
      setTimeout(() => setShowMuteIcon(false), 700);
    }
    lastTap.current = now;
  };

  const desc = truncateWords(post.content || '', 8);

  return (
    <div className="h-screen w-full snap-start relative bg-black overflow-hidden" onClick={onTap}>

      {/* ===== FULL SCREEN MEDIA ===== */}
      {ytId ? (
        <iframe
          src={`https://www.youtube.com/embed/${ytId}?autoplay=${isActive ? 1 : 0}&mute=${muted ? 1 : 0}&rel=0&loop=1&playlist=${ytId}&controls=0&playsinline=1&modestbranding=1&showinfo=0`}
          className="absolute inset-0 w-full h-full pointer-events-none"
          frameBorder={0} allow="autoplay; encrypted-media" allowFullScreen />
      ) : hasVideo ? (
        <video ref={videoRef} src={getMediaUrl(post.video_url)}
          className="absolute inset-0 w-full h-full object-cover" loop muted={muted} playsInline />
      ) : post.image_url ? (
        <img src={getMediaUrl(post.image_url)} alt="" className="absolute inset-0 w-full h-full object-cover" />
      ) : (
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-900 via-gray-900 to-black flex items-center justify-center px-10">
          <p className="text-white text-xl font-bold text-center leading-[2]" dir={dir}
            style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif", textShadow: '0 3px 20px rgba(0,0,0,0.8)' }}>
            {post.content}
          </p>
        </div>
      )}

      {/* Mute/Unmute indicator (brief, center, Instagram style) */}
      <AnimatePresence>
        {showMuteIcon && (
          <motion.div initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}
            className="absolute inset-0 flex items-center justify-center z-30 pointer-events-none">
            <div className="w-14 h-14 rounded-full bg-black/60 flex items-center justify-center">
              {muted ? <VolumeX className="w-6 h-6 text-white" /> : <Volume2 className="w-6 h-6 text-white" />}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Bottom gradient */}
      <div className="absolute bottom-0 left-0 right-0 h-[50%] bg-gradient-to-t from-black/80 via-black/25 to-transparent z-10 pointer-events-none" />

      {/* ===== RIGHT SIDE BUTTONS (Instagram Reels) - Always right ===== */}
      <div className="absolute right-3 bottom-20 flex flex-col items-center gap-5 z-20">
        {/* Avatar + follow badge */}
        <div className="relative mb-2">
          <Link to={`/social-profile/${post.author_id}`} onClick={e => e.stopPropagation()}>
            <div className="p-[2px] rounded-full bg-gradient-to-tr from-yellow-400 via-pink-500 to-purple-600">
              <img src={avatar(post.author_name, post.author_avatar)} alt="" className="w-10 h-10 rounded-full border-2 border-black object-cover" />
            </div>
          </Link>
          {!followed && user && post.author_id !== user.id && (
            <button onClick={e => { e.stopPropagation(); onFollow(); }}
              className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-5 h-5 rounded-full bg-blue-500 flex items-center justify-center border-2 border-black">
              <span className="text-white text-[10px] font-bold leading-none">+</span>
            </button>
          )}
        </div>

        {/* Like */}
        <button onClick={e => { e.stopPropagation(); onLike(); }} className="flex flex-col items-center">
          <Heart className={`w-7 h-7 drop-shadow-lg ${post.liked ? 'fill-red-500 text-red-500' : 'text-white'}`} />
          <span className="text-white text-[11px] mt-1 font-bold drop-shadow">{formatCount(post.likes_count)}</span>
        </button>

        {/* Comments */}
        <button onClick={e => { e.stopPropagation(); onComment(); }} className="flex flex-col items-center">
          <MessageCircle className="w-7 h-7 text-white drop-shadow-lg" />
          <span className="text-white text-[11px] mt-1 font-bold drop-shadow">{formatCount(post.comments_count)}</span>
        </button>

        {/* Share */}
        <button onClick={e => { e.stopPropagation(); onShare(); }} className="flex flex-col items-center">
          <Send className="w-6 h-6 text-white drop-shadow-lg -rotate-[25deg]" />
          <span className="text-white text-[11px] mt-1 font-bold drop-shadow">{formatCount(post.shares_count || 0)}</span>
        </button>

        {/* Bookmark/Save */}
        <button onClick={e => { e.stopPropagation(); onSave(); }} className="flex flex-col items-center">
          <Bookmark className={`w-7 h-7 drop-shadow-lg ${post.saved ? 'fill-white text-white' : 'text-white'}`} />
        </button>

        {/* Three dots menu */}
        <div className="relative">
          <button onClick={e => { e.stopPropagation(); setShowMenu(!showMenu); }} className="flex flex-col items-center">
            <MoreVertical className="w-6 h-6 text-white drop-shadow-lg" />
          </button>
          {showMenu && (
            <>
              <div className="fixed inset-0 z-30" onClick={() => setShowMenu(false)} />
              <div className="absolute right-0 bottom-8 z-40 bg-[#262626] border border-white/10 rounded-xl shadow-2xl py-1 min-w-[160px]" dir={dir}>
                {isOwner && (
                  <>
                    <button onClick={() => { onEdit(); setShowMenu(false); }}
                      className="w-full flex items-center gap-2.5 px-4 py-2.5 text-[13px] text-white hover:bg-white/10">
                      <Pencil className="h-4 w-4 text-white/60" />{t('editDescription') || 'Edit Description'}
                    </button>
                    <button onClick={() => { if (confirm(t('confirmDelete') || 'Delete?')) onDelete(); setShowMenu(false); }}
                      className="w-full flex items-center gap-2.5 px-4 py-2.5 text-[13px] text-red-400 hover:bg-white/10">
                      <Trash2 className="h-4 w-4" />{t('deleteLabel')}
                    </button>
                    <div className="border-t border-white/10 my-0.5" />
                  </>
                )}
                <button onClick={() => { onReport(post.id, post.author_id); setShowMenu(false); }}
                  className="w-full flex items-center gap-2.5 px-4 py-2.5 text-[13px] text-red-400 hover:bg-white/10">
                  <Flag className="h-4 w-4" />{t('reportContent')}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* ===== BOTTOM - Author + Description ===== */}
      <div className="absolute bottom-5 left-4 right-16 z-20" dir="rtl">
        <div className="flex items-center gap-2.5 mb-1.5">
          <Link to={`/social-profile/${post.author_id}`} onClick={e => e.stopPropagation()}
            className="text-white font-extrabold text-[14px] drop-shadow-lg">{post.author_name}</Link>
          {user && post.author_id !== user.id && (
            <button onClick={e => { e.stopPropagation(); onFollow(); }}
              className={`px-3 py-[3px] text-[12px] font-bold rounded-lg border ${followed ? 'border-white/30 text-white/70' : 'border-white text-white'}`}>
              {followed ? t('following') || t('unfollow') : t('follow')}
            </button>
          )}
        </div>

        {/* Description */}
        {descExpanded ? (
          <div>
            <p className="text-white/90 text-[13px] leading-relaxed drop-shadow">{post.content}</p>
            <button onClick={e => { e.stopPropagation(); setDescExpanded(false); }} className="text-white/50 text-[12px] mt-0.5">{t('showLess')}</button>
          </div>
        ) : (
          <p className="text-white/90 text-[13px] leading-relaxed drop-shadow">
            {desc.truncated}
            {desc.isTruncated && <button onClick={e => { e.stopPropagation(); setDescExpanded(true); }} className="text-white/50 text-[12px] mr-1"> ...{t('showMore')}</button>}
          </p>
        )}
      </div>
    </div>
  );
}
