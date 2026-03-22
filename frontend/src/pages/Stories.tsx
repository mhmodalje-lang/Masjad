import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import {
  Heart, MessageCircle, Share2, X, Play, Pause, Volume2, VolumeX,
  Loader2, Send, Reply, Trash2, Bookmark, UserPlus, Search,
  Music2, Image, Video, BookOpen, Plus, MoreHorizontal,
  Repeat2, Flag, Eye, Copy, ChevronDown, Compass
} from 'lucide-react';
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
function authHeadersMultipart(): Record<string, string> {
  const h: Record<string, string> = {};
  const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

interface Post {
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
  category?: string;
  likes_count: number;
  comments_count: number;
  shares_count?: number;
  views_count?: number;
  liked: boolean;
  saved?: boolean;
  created_at: string;
  is_premium?: boolean;
  points_cost?: number;
  is_embed?: boolean;
}

interface Comment {
  id: string;
  author_id: string;
  author_name: string;
  author_avatar?: string;
  content: string;
  created_at: string;
  reply_to?: string;
}

function avatar(name: string, img?: string) {
  if (img) return img;
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || '?')}&background=047857&color=fff&size=96&bold=true&font-size=0.38`;
}

function getMediaUrl(url?: string) {
  if (!url) return null;
  return url.startsWith('http') ? url : `${BACKEND_URL}${url.startsWith('/') ? '' : '/'}${url}`;
}

function getYouTubeId(url: string): string | null {
  const m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|shorts\/))([^&?\s]+)/);
  return m ? m[1] : null;
}

function formatCount(n: number): string {
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return String(n || 0);
}

function timeAgo(iso: string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return 'الآن';
  if (m < 60) return `${m}د`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}س`;
  const days = Math.floor(h / 24);
  if (days < 7) return `${days}ي`;
  if (days < 30) return `${Math.floor(days / 7)}أسبوع`;
  return new Date(iso).toLocaleDateString('ar');
}

/* ═══════════════════════════════════════════════════════
   COMMENTS BOTTOM SHEET - TikTok Style
   ═══════════════════════════════════════════════════════ */
function CommentsSheet({ postId, onClose, onCountChange }: {
  postId: string; onClose: () => void; onCountChange: (delta: number) => void;
}) {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [replyTo, setReplyTo] = useState<Comment | null>(null);
  const [sending, setSending] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/comments`, { headers: authHeaders() })
      .then(r => r.json()).then(d => { setComments(d.comments || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [postId]);

  const submit = async () => {
    if (!text.trim() || !user || sending) return;
    setSending(true);
    try {
      const body: Record<string, string> = { content: text.trim() };
      if (replyTo) body.reply_to = replyTo.id;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/comments`, {
        method: 'POST', headers: authHeaders(), body: JSON.stringify(body),
      });
      const d = await r.json();
      if (d.comment) {
        setComments(prev => [...prev, d.comment]);
        setText(''); setReplyTo(null);
        onCountChange(1);
      }
    } catch { toast.error(t('commentFailed')); }
    setSending(false);
  };

  const deleteComment = async (cid: string) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/comments/${cid}`, { method: 'DELETE', headers: authHeaders() });
      if (r.ok) { setComments(prev => prev.filter(c => c.id !== cid)); onCountChange(-1); }
    } catch {}
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[80]" onClick={onClose}>
      {/* Dark overlay */}
      <div className="absolute inset-0 bg-black/50" />

      {/* Comments panel */}
      <motion.div
        initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 32, stiffness: 400 }}
        className="absolute bottom-0 left-0 right-0 h-[60vh] bg-[#161616] rounded-t-2xl overflow-hidden flex flex-col"
        onClick={e => e.stopPropagation()}>

        {/* Handle */}
        <div className="flex flex-col items-center pt-2.5 pb-2 border-b border-white/[0.08]">
          <div className="w-9 h-1 bg-white/20 rounded-full mb-2" />
          <p className="text-white font-semibold text-[14px]">{comments.length} {t('commentsTitle')}</p>
        </div>

        {/* List */}
        <div className="flex-1 overflow-y-auto px-4 py-3 space-y-5" dir={dir}>
          {loading ? (
            <div className="flex justify-center py-16"><Loader2 className="w-7 h-7 animate-spin text-white/30" /></div>
          ) : comments.length === 0 ? (
            <div className="flex flex-col items-center py-16">
              <MessageCircle className="w-12 h-12 text-white/10 mb-3" />
              <p className="text-white/30 text-sm">{t('beFirstToComment')}</p>
            </div>
          ) : comments.map(c => (
            <div key={c.id} className={cn("flex gap-3", c.reply_to && "ms-10")}>
              <img src={avatar(c.author_name, c.author_avatar)} alt=""
                className="w-9 h-9 rounded-full shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-0.5">
                  <span className="text-white/60 text-[12px] font-semibold">{c.author_name}</span>
                  <span className="text-white/20 text-[10px]">{timeAgo(c.created_at)}</span>
                </div>
                <p className="text-white text-[13px] leading-relaxed">{c.content}</p>
                <div className="flex items-center gap-5 mt-2">
                  <button onClick={() => { setReplyTo(c); inputRef.current?.focus(); }}
                    className="text-white/30 text-[11px] font-medium active:text-white/60">
                    {t('replyLabel')}
                  </button>
                  {user && c.author_id === user.id && (
                    <button onClick={() => deleteComment(c.id)}
                      className="text-white/30 text-[11px] active:text-red-400">
                      <Trash2 className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>
              {/* Like button for comment */}
              <button className="flex flex-col items-center gap-0.5 mt-2 shrink-0">
                <Heart className="w-4 h-4 text-white/20" />
              </button>
            </div>
          ))}
        </div>

        {/* Reply indicator */}
        <AnimatePresence>
          {replyTo && (
            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }}
              className="px-4 py-2 bg-white/[0.03] flex items-center justify-between border-t border-white/[0.05]" dir={dir}>
              <span className="text-[12px] text-white/40">{t('replyTo')} <b className="text-white/60">{replyTo.author_name}</b></span>
              <button onClick={() => setReplyTo(null)} className="p-1"><X className="w-3.5 h-3.5 text-white/30" /></button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Input */}
        {user ? (
          <div className="flex items-center gap-2.5 px-4 py-3 border-t border-white/[0.08] bg-[#161616]"
            dir={dir} style={{ paddingBottom: 'max(12px, env(safe-area-inset-bottom, 12px))' }}>
            <img src={avatar(user.name || '', user.avatar)} alt="" className="w-8 h-8 rounded-full shrink-0" />
            <div className="flex-1 flex items-center bg-white/[0.06] rounded-full overflow-hidden border border-white/[0.06]">
              <input ref={inputRef} value={text} onChange={e => setText(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && submit()}
                placeholder={replyTo ? `@${replyTo.author_name}` : t('writeComment')}
                className="flex-1 bg-transparent text-white px-4 py-2.5 text-[13px] placeholder:text-white/20 outline-none" />
              {text.trim() && (
                <button onClick={submit} disabled={sending}
                  className="px-4 py-2 text-rose-500 font-bold text-[13px] active:opacity-50 disabled:opacity-30">
                  {t('publishNow')}
                </button>
              )}
            </div>
          </div>
        ) : (
          <div className="px-4 py-4 border-t border-white/[0.08] text-center"
            style={{ paddingBottom: 'max(12px, env(safe-area-inset-bottom, 12px))' }}>
            <Link to="/auth" className="text-rose-500 text-[13px] font-bold">{t('loginToComment')}</Link>
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}

/* ═══════════════════════════════════════════════════════
   SHARE BOTTOM SHEET
   ═══════════════════════════════════════════════════════ */
function ShareSheet({ post, onClose }: { post: Post; onClose: () => void }) {
  const { t, dir } = useLocale();
  const { user } = useAuth();

  const handleShare = async (type: string) => {
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/share`, { method: 'POST', headers: authHeaders() });
    } catch {}

    if (type === 'native' && navigator.share) {
      navigator.share({ title: post.title || '', text: post.content, url: window.location.href }).catch(() => {});
    } else if (type === 'copy') {
      navigator.clipboard.writeText(window.location.href);
      toast.success(t('linkCopied'));
    } else if (type === 'repost') {
      toast.success(t('reposted'));
    }
    onClose();
  };

  const actions = [
    { icon: Repeat2, label: t('repostForFollowers'), color: 'text-green-400', action: () => handleShare('repost') },
    { icon: Send, label: t('sharePost'), color: 'text-blue-400', action: () => handleShare('native') },
    { icon: Copy, label: t('copyLink'), color: 'text-yellow-400', action: () => handleShare('copy') },
    { icon: Bookmark, label: t('addToFavorites'), color: 'text-purple-400', action: async () => {
      if (!user) return;
      try {
        const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/save`, { method: 'POST', headers: authHeaders() });
        const d = await r.json();
        toast.success(d.saved ? t('bookmarked') : t('unbookmarked'));
      } catch {}
      onClose();
    }},
    { icon: Flag, label: t('reportContent'), color: 'text-red-400', action: () => { toast.success(t('reportContent')); onClose(); } },
  ];

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[80]" onClick={onClose}>
      <div className="absolute inset-0 bg-black/50" />
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 32, stiffness: 400 }}
        className="absolute bottom-0 left-0 right-0 bg-[#161616] rounded-t-2xl overflow-hidden"
        onClick={e => e.stopPropagation()}>
        <div className="flex flex-col items-center pt-2.5 pb-3">
          <div className="w-9 h-1 bg-white/20 rounded-full" />
        </div>
        <div className="px-4 pb-4 space-y-1" dir={dir}
          style={{ paddingBottom: 'max(20px, env(safe-area-inset-bottom, 20px))' }}>
          {actions.map((a, i) => {
            const Icon = a.icon;
            return (
              <button key={i} onClick={a.action}
                className="w-full flex items-center gap-4 px-4 py-3.5 rounded-xl active:bg-white/[0.05] transition-colors">
                <Icon className={cn("w-5 h-5", a.color)} />
                <span className="text-white text-[14px] font-medium">{a.label}</span>
              </button>
            );
          })}
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ═══════════════════════════════════════════════════════
   CREATE POST SHEET - Full Featured
   ═══════════════════════════════════════════════════════ */
function CreateSheet({ onClose, onCreated }: {
  onClose: () => void; onCreated: (p: Post) => void;
}) {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const [content, setContent] = useState('');
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('general');
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState('');
  const [embedUrl, setEmbedUrl] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [contentType, setContentType] = useState<'text' | 'image' | 'video' | 'embed'>('text');
  const fileRef = useRef<HTMLInputElement>(null);

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]; if (!f) return;
    setFile(f);
    const reader = new FileReader();
    reader.onload = ev => setPreview(ev.target?.result as string);
    reader.readAsDataURL(f);
    setContentType(f.type.startsWith('video/') ? 'video' : 'image');
  };

  const submit = async () => {
    if ((!content.trim() && !embedUrl.trim() && !file) || !user) return;
    setSubmitting(true);
    try {
      let imageUrl: string | null = null;
      let videoUrl: string | null = null;

      if (file) {
        const fd = new FormData(); fd.append('file', file);
        const r = await fetch(`${BACKEND_URL}/api/upload/multipart`, {
          method: 'POST', headers: authHeadersMultipart(), body: fd
        });
        if (r.ok) {
          const d = await r.json();
          if (file.type.startsWith('video/')) videoUrl = d.url;
          else imageUrl = d.url;
        } else { toast.error(t('uploadFailed')); setSubmitting(false); return; }
      }

      const body: Record<string, string | undefined> = {
        content: content.trim() || title.trim() || embedUrl.trim() || 'محتوى جديد',
        category,
        title: title.trim() || undefined,
        image_url: imageUrl || videoUrl || undefined,
        media_type: videoUrl ? 'video' : imageUrl ? 'image' : embedUrl ? 'embed' : 'text',
        embed_url: embedUrl.trim() || undefined,
      };

      const r = await fetch(`${BACKEND_URL}/api/stories/create`, {
        method: 'POST', headers: authHeaders(), body: JSON.stringify(body)
      });
      const d = await r.json();
      if (d.story) {
        onCreated(d.story);
        onClose();
        toast.success(t('publishSuccess'));
      } else {
        toast.error(d.detail || t('publishFailed'));
      }
    } catch { toast.error(t('errorOccurred')); }
    setSubmitting(false);
  };

  const categories = [
    { key: 'general', label: '🌟 ' + t('storyCatGeneral') },
    { key: 'istighfar', label: '🤲 ' + t('storyCatIstighfar') },
    { key: 'sahaba', label: '⚔️ ' + t('storyCatSahaba') },
    { key: 'quran', label: '📖 ' + t('storyCatQuran') },
    { key: 'prophets', label: '🕌 ' + t('storyCatProphets') },
    { key: 'ruqyah', label: '🛡️ ' + t('storyCatRuqyah') },
    { key: 'rizq', label: '💎 ' + t('storyCatRizq') },
    { key: 'tawba', label: '💧 ' + t('storyCatTawba') },
    { key: 'miracles', label: '✨ ' + t('storyCatMiracles') },
  ];

  const isAdmin = user?.email === 'mohammadalrejab@gmail.com';

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[80] bg-black/80" onClick={onClose}>
      <motion.div
        initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="absolute bottom-0 left-0 right-0 max-h-[90vh] bg-[#0d0d0d] rounded-t-2xl overflow-y-auto border-t border-white/[0.08]"
        onClick={e => e.stopPropagation()}>

        <div className="p-5 space-y-4" dir={dir}>
          <div className="w-9 h-1 bg-white/20 rounded-full mx-auto -mt-1 mb-1" />

          {/* Header */}
          <div className="flex items-center justify-between">
            <button onClick={onClose} className="text-white/50 text-[14px] active:text-white/80">{t('cancel') || 'إلغاء'}</button>
            <h3 className="text-white font-bold text-[15px]">{t('createNewPost')}</h3>
            <button onClick={submit} disabled={submitting || (!content.trim() && !embedUrl.trim() && !file)}
              className="text-rose-500 font-bold text-[14px] disabled:text-white/20 active:opacity-60">
              {submitting ? t('posting') : t('postNow')}
            </button>
          </div>

          {/* Author */}
          {user && (
            <div className="flex items-center gap-3">
              <img src={avatar(user.name || '', user.avatar)} alt=""
                className="w-11 h-11 rounded-full border-2 border-emerald-600/30" />
              <div>
                <span className="text-white font-bold text-[14px] block">{user.name}</span>
                <span className="text-white/30 text-[11px]">{t('islamicContent')}</span>
              </div>
            </div>
          )}

          {/* Media Type Buttons */}
          <div className="flex gap-2">
            {[
              { key: 'text', icon: BookOpen, label: t('textType') },
              { key: 'image', icon: Image, label: t('imageType') },
              { key: 'video', icon: Video, label: t('addVideo') },
              ...(isAdmin ? [{ key: 'embed', icon: Compass, label: t('embedType') }] : []),
            ].map(btn => {
              const Icon = btn.icon;
              return (
                <button key={btn.key}
                  onClick={() => { setContentType(btn.key as any); if (btn.key === 'image' || btn.key === 'video') fileRef.current?.click(); }}
                  className={cn('flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-xl text-[12px] font-semibold transition-all',
                    contentType === btn.key ? 'bg-white/10 text-white border border-white/15' : 'bg-white/[0.04] text-white/40 border border-transparent')}>
                  <Icon className="w-4 h-4" /> {btn.label}
                </button>
              );
            })}
          </div>

          {/* Title */}
          <input value={title} onChange={e => setTitle(e.target.value)} placeholder={t('addTitle')}
            className="w-full bg-white/[0.04] text-white rounded-xl px-4 py-3.5 text-[14px] placeholder:text-white/20 outline-none border border-white/[0.06] focus:border-white/15 transition-colors" />

          {/* Content */}
          <textarea value={content} onChange={e => setContent(e.target.value)}
            placeholder={t('addDescription')}
            className="w-full bg-white/[0.04] text-white rounded-xl px-4 py-3.5 text-[14px] min-h-[100px] resize-none placeholder:text-white/20 outline-none border border-white/[0.06] focus:border-white/15 leading-relaxed transition-colors"
            maxLength={10000} />

          {/* Embed URL */}
          {contentType === 'embed' && (
            <input value={embedUrl} onChange={e => setEmbedUrl(e.target.value)}
              placeholder="YouTube / Vimeo URL"
              className="w-full bg-white/[0.04] text-white rounded-xl px-4 py-3.5 text-[14px] placeholder:text-white/20 outline-none border border-white/[0.06] focus:border-white/15" dir="ltr" />
          )}

          {/* File Input */}
          <input ref={fileRef} type="file" accept="image/*,video/*" onChange={handleFile} className="hidden" />

          {/* Preview */}
          {preview && (
            <div className="relative rounded-xl overflow-hidden">
              {file?.type.startsWith('video/') ? (
                <video src={preview} controls className="w-full max-h-48 bg-black rounded-xl" />
              ) : (
                <img src={preview} alt="" className="w-full max-h-48 object-cover rounded-xl" />
              )}
              <button onClick={() => { setFile(null); setPreview(''); }}
                className="absolute top-2 end-2 w-7 h-7 bg-black/70 backdrop-blur-sm rounded-full flex items-center justify-center">
                <X className="w-4 h-4 text-white" />
              </button>
            </div>
          )}

          {/* Categories */}
          <div>
            <p className="text-white/30 text-[11px] mb-2 font-medium">{t('selectCategory')}</p>
            <div className="flex flex-wrap gap-1.5">
              {categories.map(c => (
                <button key={c.key} onClick={() => setCategory(c.key)}
                  className={cn('px-3.5 py-2 rounded-full text-[11px] font-medium transition-all',
                    category === c.key
                      ? 'bg-emerald-600 text-white'
                      : 'bg-white/[0.04] text-white/40 border border-white/[0.06]')}>
                  {c.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ═══════════════════════════════════════════════════════
   SINGLE REEL SLIDE - TikTok Style
   ═══════════════════════════════════════════════════════ */
function ReelSlide({ post, isActive, onLike, onComment, onShare, onBookmark, onFollow, isFollowed }: {
  post: Post; isActive: boolean;
  onLike: () => void; onComment: () => void; onShare: () => void;
  onBookmark: () => void; onFollow: () => void; isFollowed: boolean;
}) {
  const { t, dir } = useLocale();
  const { user } = useAuth();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(false);
  const [paused, setPaused] = useState(false);
  const [progress, setProgress] = useState(0);
  const [showPlayIcon, setShowPlayIcon] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const isEmbed = post.is_embed || post.media_type === 'embed';
  const ytId = isEmbed && post.embed_url ? getYouTubeId(post.embed_url) : null;
  const mediaUrl = getMediaUrl(post.video_url || post.image_url);
  const isVideo = post.media_type === 'video' || post.content_type?.includes('video') || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));
  const isImage = post.media_type === 'image' || (mediaUrl && /\.(jpg|jpeg|png|gif|webp)/i.test(mediaUrl));

  // Auto-play/pause based on visibility
  useEffect(() => {
    if (!videoRef.current) return;
    if (isActive) {
      videoRef.current.currentTime = 0;
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
    if (videoRef.current.paused) { videoRef.current.play(); setPaused(false); }
    else { videoRef.current.pause(); setPaused(true); }
    setShowPlayIcon(true);
    setTimeout(() => setShowPlayIcon(false), 500);
  };

  const handleTimeUpdate = () => {
    if (!videoRef.current || !videoRef.current.duration) return;
    setProgress((videoRef.current.currentTime / videoRef.current.duration) * 100);
  };

  // Double tap to like
  const lastTap = useRef(0);
  const [showHeart, setShowHeart] = useState(false);
  const handleTap = (e: React.MouseEvent) => {
    const now = Date.now();
    if (now - lastTap.current < 280) {
      // Double tap = like
      if (!post.liked) onLike();
      setShowHeart(true);
      setTimeout(() => setShowHeart(false), 800);
    } else {
      // Single tap = play/pause
      if (isVideo && !isEmbed) togglePlay();
    }
    lastTap.current = now;
  };

  const contentText = post.content || '';
  const showExpand = contentText.length > 80;

  return (
    <div className="h-[100dvh] w-full snap-start snap-always relative flex items-center justify-center bg-black overflow-hidden select-none">

      {/* ═══ BACKGROUND MEDIA ═══ */}
      {ytId ? (
        <iframe
          src={`https://www.youtube.com/embed/${ytId}?autoplay=${isActive ? 1 : 0}&rel=0&loop=1&playlist=${ytId}&controls=0&playsinline=1&mute=${muted ? 1 : 0}&modestbranding=1`}
          className="absolute inset-0 w-full h-full scale-[1.2]" frameBorder={0}
          allow="autoplay; encrypted-media; gyroscope; picture-in-picture"
          style={{ pointerEvents: 'none' }}
        />
      ) : isVideo && mediaUrl ? (
        <video
          ref={videoRef} src={mediaUrl}
          className="absolute inset-0 w-full h-full object-cover"
          loop muted={muted} playsInline
          onTimeUpdate={handleTimeUpdate}
          poster={getMediaUrl(post.thumbnail_url) || undefined}
        />
      ) : isImage && mediaUrl ? (
        <img src={mediaUrl} alt="" className="absolute inset-0 w-full h-full object-cover" />
      ) : (
        /* Text-only post: Islamic gradient background */
        <div className="absolute inset-0 bg-gradient-to-br from-[#0a1a0f] via-[#0f1f15] to-[#05100a]">
          {/* Decorative Islamic pattern overlay */}
          <div className="absolute inset-0 opacity-[0.03]" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cpath d='M40 0L80 40L40 80L0 40Z' fill='none' stroke='%23d4af37' stroke-width='0.5'/%3E%3Ccircle cx='40' cy='40' r='20' fill='none' stroke='%23d4af37' stroke-width='0.5'/%3E%3C/svg%3E")`,
            backgroundSize: '80px 80px'
          }} />
        </div>
      )}

      {/* Tap area */}
      <div className="absolute inset-0 z-[5]" onClick={handleTap} />

      {/* ═══ DOUBLE TAP HEART ANIMATION ═══ */}
      <AnimatePresence>
        {showHeart && (
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 1.5, opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="absolute inset-0 flex items-center justify-center z-[15] pointer-events-none">
            <Heart className="w-28 h-28 text-rose-500 fill-rose-500 drop-shadow-2xl" />
          </motion.div>
        )}
      </AnimatePresence>

      {/* ═══ PLAY/PAUSE INDICATOR ═══ */}
      <AnimatePresence>
        {showPlayIcon && !showHeart && (
          <motion.div
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 0.8 }}
            exit={{ scale: 1.3, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="absolute inset-0 flex items-center justify-center z-[15] pointer-events-none">
            <div className="w-16 h-16 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center">
              {paused ? <Play className="w-8 h-8 text-white fill-white ms-1" /> : <Pause className="w-8 h-8 text-white" />}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ═══ TEXT CONTENT OVERLAY (for text/image posts) ═══ */}
      {(!isVideo && !isEmbed) && contentText && (
        <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 z-[8] px-8 pointer-events-none">
          <p className="text-white text-center text-[22px] font-bold leading-[2] drop-shadow-2xl"
            style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif", textShadow: '0 2px 20px rgba(0,0,0,0.8)' }}>
            {post.title || contentText}
          </p>
        </div>
      )}

      {/* ═══ TOP GRADIENT ═══ */}
      <div className="absolute top-0 left-0 right-0 h-24 bg-gradient-to-b from-black/40 to-transparent z-10 pointer-events-none" />

      {/* ═══ RIGHT SIDE ACTION BUTTONS (TikTok Style) ═══ */}
      <div className="absolute end-3 bottom-[140px] flex flex-col items-center gap-4 z-20"
        style={{ marginBottom: 'env(safe-area-inset-bottom, 0px)' }}>

        {/* Profile Picture + Follow */}
        <div className="relative mb-2">
          <Link to={`/social-profile/${post.author_id}`} className="block">
            <img src={avatar(post.author_name, post.author_avatar)} alt=""
              className="w-[46px] h-[46px] rounded-full border-[2px] border-white shadow-lg" />
          </Link>
          {user && user.id !== post.author_id && !isFollowed && (
            <motion.button
              initial={{ scale: 0 }} animate={{ scale: 1 }}
              onClick={onFollow}
              className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-[22px] h-[22px] rounded-full bg-rose-500 flex items-center justify-center shadow-lg shadow-rose-500/40">
              <Plus className="w-3 h-3 text-white stroke-[3]" />
            </motion.button>
          )}
        </div>

        {/* Like */}
        <button onClick={onLike} className="flex flex-col items-center active:scale-90 transition-transform">
          <Heart className={cn("w-[30px] h-[30px] drop-shadow-lg transition-all duration-200",
            post.liked ? "fill-rose-500 text-rose-500" : "text-white")} />
          <span className="text-white text-[11px] mt-1 font-bold">{formatCount(post.likes_count)}</span>
        </button>

        {/* Comments */}
        <button onClick={onComment} className="flex flex-col items-center active:scale-90 transition-transform">
          <MessageCircle className="w-[30px] h-[30px] text-white drop-shadow-lg" />
          <span className="text-white text-[11px] mt-1 font-bold">{formatCount(post.comments_count)}</span>
        </button>

        {/* Bookmark/Save */}
        <button onClick={onBookmark} className="flex flex-col items-center active:scale-90 transition-transform">
          <Bookmark className={cn("w-[28px] h-[28px] drop-shadow-lg transition-all",
            post.saved ? "fill-amber-400 text-amber-400" : "text-white")} />
          <span className="text-white text-[11px] mt-1 font-bold">{formatCount(post.shares_count || 0)}</span>
        </button>

        {/* Share */}
        <button onClick={onShare} className="flex flex-col items-center active:scale-90 transition-transform">
          <Share2 className="w-[28px] h-[28px] text-white drop-shadow-lg" />
          <span className="text-white text-[11px] mt-1 font-bold">{formatCount(post.views_count || 0)}</span>
        </button>

        {/* Spinning Music Disc */}
        <motion.div
          animate={isActive && !paused ? { rotate: 360 } : {}}
          transition={{ duration: 5, repeat: Infinity, ease: 'linear' }}
          className="w-10 h-10 mt-1 rounded-full border-2 border-white/30 overflow-hidden shadow-lg">
          <img src={avatar(post.author_name, post.author_avatar)} alt=""
            className="w-full h-full object-cover" />
        </motion.div>
      </div>

      {/* ═══ BOTTOM CONTENT AREA ═══ */}
      <div className="absolute bottom-0 left-0 right-0 z-20 pointer-events-none"
        style={{ paddingBottom: 'max(80px, calc(80px + env(safe-area-inset-bottom, 0px)))' }}>

        {/* Bottom gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent pointer-events-none" />

        <div className="relative px-4 pe-[72px] pb-3" dir={dir}>
          {/* Repost tag */}
          {post.shares_count && post.shares_count > 0 && (
            <div className="flex items-center gap-1.5 mb-2 pointer-events-auto">
              <Repeat2 className="w-3.5 h-3.5 text-white/50" />
              <span className="text-white/50 text-[11px]">{t('repostForFollowers')}</span>
            </div>
          )}

          {/* Author Name */}
          <div className="flex items-center gap-2 mb-1.5 pointer-events-auto">
            <Link to={`/social-profile/${post.author_id}`}
              className="text-white font-bold text-[15px] tracking-wide drop-shadow-lg">
              {post.author_name}
            </Link>
            {user && user.id !== post.author_id && !isFollowed && (
              <button onClick={onFollow}
                className="px-2.5 py-0.5 border border-white/40 text-white text-[11px] font-semibold rounded-md active:bg-white/10 transition-colors">
                {t('follow')}
              </button>
            )}
          </div>

          {/* Caption/Content with expand */}
          <div className="mb-1.5 pointer-events-auto" onClick={() => showExpand && setExpanded(!expanded)}>
            <p className={cn("text-white/90 text-[13px] leading-relaxed drop-shadow",
              !expanded && showExpand && "line-clamp-2")}>
              {contentText}
            </p>
            {showExpand && (
              <button className="text-white/50 text-[12px] mt-0.5 font-medium">
                {expanded ? '' : '...المزيد'}
              </button>
            )}
          </div>

          {/* Hashtags */}
          {post.category && (
            <div className="flex items-center gap-2 mb-2 pointer-events-auto flex-wrap">
              <span className="text-white/70 text-[12px] font-bold">#{post.category}</span>
              <span className="text-white/70 text-[12px] font-bold">#إسلام</span>
              <span className="text-white/70 text-[12px] font-bold">#محتوى_إسلامي</span>
            </div>
          )}

          {/* Sound/Music bar */}
          <div className="flex items-center gap-2 overflow-hidden pointer-events-auto" onClick={() => (isVideo || ytId) && setMuted(!muted)}>
            <Music2 className="w-3.5 h-3.5 text-white/50 shrink-0" />
            <div className="overflow-hidden flex-1">
              <motion.p
                animate={isActive && !paused ? { x: [0, -150, 0] } : {}}
                transition={{ duration: 10, repeat: Infinity, ease: 'linear' }}
                className="text-white/50 text-[11px] whitespace-nowrap">
                {post.author_name} · {t('originalSound')}
              </motion.p>
            </div>
            {(isVideo || ytId) && (
              <button className="shrink-0">
                {muted ? <VolumeX className="w-3.5 h-3.5 text-white/40" /> : <Volume2 className="w-3.5 h-3.5 text-white/40" />}
              </button>
            )}
          </div>
        </div>
      </div>

      {/* ═══ VIDEO PROGRESS BAR ═══ */}
      {isVideo && (
        <div className="absolute bottom-[80px] left-0 right-0 h-[2px] bg-white/10 z-30"
          style={{ bottom: 'max(80px, calc(80px + env(safe-area-inset-bottom, 0px)))' }}>
          <div className="h-full bg-white/80 transition-[width] duration-100" style={{ width: `${progress}%` }} />
        </div>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════
   MAIN STORIES PAGE - Full TikTok Clone
   ═══════════════════════════════════════════════════════ */
export default function Stories() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { t, dir } = useLocale();
  const [searchParams, setSearchParams] = useSearchParams();
  const [posts, setPosts] = useState<Post[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'forYou' | 'following' | 'explore'>('forYou');
  const [showComments, setShowComments] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [followedIds, setFollowedIds] = useState<Set<string>>(new Set());
  const containerRef = useRef<HTMLDivElement>(null);

  // Check if create param is set
  useEffect(() => {
    if (searchParams.get('create') === 'true' && user) {
      setShowCreate(true);
      const p = new URLSearchParams(searchParams);
      p.delete('create');
      setSearchParams(p, { replace: true });
    }
  }, [searchParams, user]);

  useEffect(() => {
    const handler = () => { if (user) setShowCreate(true); };
    window.addEventListener('open-create-story', handler);
    return () => window.removeEventListener('open-create-story', handler);
  }, [user]);

  // Fetch posts
  const fetchPosts = useCallback(async () => {
    setLoading(true);
    try {
      const h: Record<string, string> = {};
      const tk = getToken(); if (tk) h.Authorization = `Bearer ${tk}`;

      let url: string;
      switch (activeTab) {
        case 'following':
          url = `${BACKEND_URL}/api/sohba/feed/following?limit=30`;
          break;
        case 'explore':
          url = `${BACKEND_URL}/api/sohba/explore?limit=30`;
          break;
        default:
          url = `${BACKEND_URL}/api/sohba/explore?limit=30`;
      }

      const res = await fetch(url, { headers: h });
      const data = await res.json();
      const items = data.posts || data.stories || [];
      setPosts(items);
      setCurrentIndex(0);
    } catch (err) {
      console.error('Fetch error:', err);
    }
    setLoading(false);
  }, [activeTab, user]);

  useEffect(() => { fetchPosts(); }, [fetchPosts]);

  // Scroll handler for snap
  const handleScroll = useCallback(() => {
    if (!containerRef.current) return;
    const scrollTop = containerRef.current.scrollTop;
    const height = containerRef.current.clientHeight;
    const newIndex = Math.round(scrollTop / height);
    if (newIndex !== currentIndex && newIndex >= 0 && newIndex < posts.length) {
      setCurrentIndex(newIndex);
    }
  }, [currentIndex, posts.length]);

  // Actions
  const handleLike = async (idx: number) => {
    const post = posts[idx]; if (!post || !user) { if (!user) toast.error(t('loginRequired')); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setPosts(prev => prev.map((p, i) =>
        i === idx ? { ...p, liked: d.liked, likes_count: d.liked ? p.likes_count + 1 : Math.max(0, p.likes_count - 1) } : p
      ));
    } catch {}
  };

  const handleBookmark = async (idx: number) => {
    const post = posts[idx]; if (!post || !user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/save`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setPosts(prev => prev.map((p, i) => i === idx ? { ...p, saved: d.saved } : p));
      toast.success(d.saved ? t('bookmarked') : t('unbookmarked'));
    } catch {}
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
      toast.success(d.following ? t('follow') : t('unfollow'));
    } catch {}
  };

  const handleCreated = (p: Post) => {
    setPosts(prev => [p, ...prev]);
    setCurrentIndex(0);
    if (containerRef.current) containerRef.current.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // ═══ LOADING STATE ═══
  if (loading) {
    return (
      <div className="h-[100dvh] bg-black flex items-center justify-center">
        <div className="flex flex-col items-center gap-5">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
            className="w-12 h-12 rounded-full border-2 border-emerald-500/30 border-t-emerald-500" />
          <p className="text-white/30 text-[13px]">{t('discoverReels')}</p>
        </div>
      </div>
    );
  }

  // ═══ EMPTY STATE ═══
  if (posts.length === 0) {
    return (
      <div className="h-[100dvh] bg-black flex flex-col items-center justify-center px-8">
        <div className="w-24 h-24 rounded-full bg-white/[0.03] flex items-center justify-center mb-6 border border-white/[0.06]">
          <Play className="w-10 h-10 text-white/15" />
        </div>
        <h2 className="text-white text-lg font-bold mb-2">{t('noVideosToShow')}</h2>
        <p className="text-white/30 text-[13px] text-center mb-8">{t('startCreating')}</p>
        {user && (
          <button onClick={() => setShowCreate(true)}
            className="px-10 py-3.5 bg-rose-500 text-white rounded-lg font-bold text-[14px] active:scale-95 transition-transform shadow-lg shadow-rose-500/20">
            {t('createNewPost')}
          </button>
        )}
        <AnimatePresence>
          {showCreate && <CreateSheet onClose={() => setShowCreate(false)} onCreated={handleCreated} />}
        </AnimatePresence>
      </div>
    );
  }

  return (
    <div className="h-[100dvh] bg-black relative overflow-hidden">

      {/* ═══ TOP HEADER OVERLAY ═══ */}
      <div className="absolute top-0 left-0 right-0 z-30"
        style={{ paddingTop: 'max(8px, env(safe-area-inset-top, 8px))' }}>
        <div className="flex items-center justify-between px-4 py-2">
          {/* Search */}
          <Link to="/explore"
            className="w-9 h-9 rounded-full bg-black/20 backdrop-blur-md flex items-center justify-center active:scale-90 transition-transform">
            <Search className="w-4.5 h-4.5 text-white/80" />
          </Link>

          {/* ═══ TOP TABS (TikTok style) ═══ */}
          <div className="flex items-center gap-5">
            {[
              { key: 'explore' as const, label: t('explore') },
              { key: 'following' as const, label: t('followingTab') },
              { key: 'forYou' as const, label: t('forYou') },
            ].map(tab => (
              <button key={tab.key} onClick={() => setActiveTab(tab.key)}
                className={cn(
                  "relative text-[14px] font-bold transition-all py-1.5",
                  activeTab === tab.key ? "text-white" : "text-white/45"
                )}>
                {tab.label}
                {activeTab === tab.key && (
                  <motion.div layoutId="top-tab-line"
                    className="absolute -bottom-0.5 left-1/2 -translate-x-1/2 w-6 h-[2.5px] bg-white rounded-full"
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }} />
                )}
              </button>
            ))}
          </div>

          {/* More */}
          <button className="w-9 h-9 rounded-full bg-black/20 backdrop-blur-md flex items-center justify-center active:scale-90 transition-transform">
            <MoreHorizontal className="w-4.5 h-4.5 text-white/80" />
          </button>
        </div>
      </div>

      {/* ═══ REELS CONTAINER (Snap Scroll) ═══ */}
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className="h-full overflow-y-scroll snap-y snap-mandatory"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none', WebkitOverflowScrolling: 'touch' }}>

        {posts.map((post, index) => (
          <ReelSlide
            key={post.id}
            post={post}
            isActive={index === currentIndex}
            onLike={() => handleLike(index)}
            onComment={() => setShowComments(true)}
            onShare={() => setShowShare(true)}
            onBookmark={() => handleBookmark(index)}
            onFollow={() => handleFollow(post.author_id)}
            isFollowed={followedIds.has(post.author_id)}
          />
        ))}
      </div>

      {/* ═══ BOTTOM NAV (TikTok Style) ═══ */}
      <div className="absolute bottom-0 left-0 right-0 z-30 bg-black/90 backdrop-blur-md border-t border-white/[0.06]"
        style={{ paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}>
        <div className="flex items-center justify-around py-2 px-2" dir={dir}>
          {/* Home */}
          <Link to="/" className="flex flex-col items-center gap-0.5 py-1 px-3 active:opacity-60">
            <svg viewBox="0 0 24 24" fill="none" className="w-6 h-6">
              <path d="M3 9.5L12 2l9 7.5V20a2 2 0 01-2 2H5a2 2 0 01-2-2V9.5z" stroke="white" strokeWidth="1.8" strokeLinejoin="round" />
            </svg>
            <span className="text-white/60 text-[10px] font-medium">{t('navFeed')}</span>
          </Link>

          {/* Discover */}
          <Link to="/explore" className="flex flex-col items-center gap-0.5 py-1 px-3 active:opacity-60">
            <Compass className="w-6 h-6 text-white/60 stroke-[1.8]" />
            <span className="text-white/60 text-[10px] font-medium">{t('navDiscover')}</span>
          </Link>

          {/* Create - Center button */}
          <button onClick={() => user ? setShowCreate(true) : navigate('/auth')}
            className="relative -mt-2 active:scale-90 transition-transform">
            <div className="w-12 h-8 rounded-lg bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-500/30">
              <Plus className="w-5 h-5 text-white stroke-[3]" />
            </div>
          </button>

          {/* Inbox */}
          <Link to="/messages" className="flex flex-col items-center gap-0.5 py-1 px-3 active:opacity-60 relative">
            <MessageCircle className="w-6 h-6 text-white/60 stroke-[1.8]" />
            <span className="text-white/60 text-[10px] font-medium">{t('navInbox')}</span>
          </Link>

          {/* Profile */}
          <Link to={user ? "/profile" : "/auth"} className="flex flex-col items-center gap-0.5 py-1 px-3 active:opacity-60">
            {user ? (
              <img src={avatar(user.name || '', user.avatar)} alt="" className="w-6 h-6 rounded-full border border-white/20" />
            ) : (
              <svg viewBox="0 0 24 24" fill="none" className="w-6 h-6">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="white" strokeOpacity="0.6" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                <circle cx="12" cy="7" r="4" stroke="white" strokeOpacity="0.6" strokeWidth="1.8" />
              </svg>
            )}
            <span className="text-white/60 text-[10px] font-medium">{t('navProfile')}</span>
          </Link>
        </div>
      </div>

      {/* ═══ MODALS ═══ */}
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
        {showShare && posts[currentIndex] && (
          <ShareSheet post={posts[currentIndex]} onClose={() => setShowShare(false)} />
        )}
        {showCreate && (
          <CreateSheet onClose={() => setShowCreate(false)} onCreated={handleCreated} />
        )}
      </AnimatePresence>
    </div>
  );
}
