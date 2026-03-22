import { useLocale } from "@/hooks/useLocale";
import { useState, useEffect, useCallback, useRef } from 'react';
import {
  Heart, MessageCircle, Send, X, Loader2, Image, Video,
  BookOpen, Plus, Eye, ArrowRight, ArrowLeft, Share2, Bookmark, Film,
  Play, Volume2, VolumeX, Trash2, Reply, Search, Users,
  ChevronDown, TrendingUp, Flame, Star, Clock, Hash, Lock,
  Compass, Music2, Zap
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import IslamicAd from '@/components/IslamicAd';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { AdBanner } from '@/components/AdBanner';

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

interface Story {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  title?: string; content: string; category: string; image_url?: string;
  video_url?: string; thumbnail_url?: string; content_type?: string;
  media_type?: string; created_at: string; likes_count: number;
  comments_count: number; shares_count?: number; views_count?: number;
  liked: boolean; saved: boolean;
  embed_url?: string; platform?: string; is_embed?: boolean;
  is_premium?: boolean; points_cost?: number;
}

interface Comment {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  content: string; created_at: string; reply_to?: string;
}

interface Category { key: string; label: string; emoji: string; icon: string; color: string; labelKey?: string; }

function timeAgo(iso: string, t?: (k: string) => string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return t ? t('now') : 'الآن';
  if (m < 60) return t ? t('minutesAgo').replace('{n}', String(m)) : `${m}د`;
  const h = Math.floor(m / 60);
  if (h < 24) return t ? t('hoursAgo').replace('{n}', String(h)) : `${h}س`;
  const days = Math.floor(h / 24);
  if (days < 30) return t ? t('daysAgo').replace('{n}', String(days)) : `${days}ي`;
  return new Date(iso).toLocaleDateString();
}

function getMediaUrl(url?: string) {
  if (!url) return null;
  return url.startsWith('http') ? url : `${BACKEND_URL}${url.startsWith('/') ? '' : '/'}${url}`;
}

function getYouTubeId(url: string): string | null {
  const m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|shorts\/))([^&?\s]+)/);
  return m ? m[1] : null;
}

function avatar(name: string, img?: string) {
  if (img) return img;
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || '?')}&background=047857&color=fff&size=80&bold=true&font-size=0.4`;
}

function formatCount(n: number): string {
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return String(n);
}

/* ==================== COMMENTS SHEET ==================== */
function CommentsSheet({ storyId, onClose, onCountChange }: {
  storyId: string; onClose: () => void; onCountChange: (delta: number) => void;
}) {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [replyTo, setReplyTo] = useState<Comment | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/posts/${storyId}/comments`, { headers: authHeaders() })
      .then(r => r.json()).then(d => { setComments(d.comments || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [storyId]);

  const submit = async () => {
    if (!text.trim() || !user) return;
    try {
      const body: Record<string, string> = { content: text.trim() };
      if (replyTo) body.reply_to = replyTo.id;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${storyId}/comments`, {
        method: 'POST', headers: authHeaders(), body: JSON.stringify(body),
      });
      const d = await r.json();
      if (d.comment) {
        setComments(prev => [...prev, d.comment]);
        setText(''); setReplyTo(null);
        onCountChange(1);
      }
    } catch { toast.error(t('commentFailed')); }
  };

  const deleteComment = async (cid: string) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/comments/${cid}`, { method: 'DELETE', headers: authHeaders() });
      if (r.ok) { setComments(prev => prev.filter(c => c.id !== cid)); onCountChange(-1); toast.success(t('deleted')); }
      else toast.error(t('cannotDeleteComment'));
    } catch { toast.error(t('error')); }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="absolute bottom-0 left-0 right-0 max-h-[70vh] bg-card rounded-t-3xl overflow-hidden flex flex-col border-t border-primary/20"
        onClick={e => e.stopPropagation()}>
        <div className="flex flex-col items-center pt-3 pb-2 border-b border-border/20">
          <div className="w-10 h-1 bg-muted-foreground/20 rounded-full mb-3" />
          <h3 className="text-foreground font-bold text-sm">{t('commentsTitle')} ({comments.length})</h3>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4" dir={dir}>
          {loading ? <div className="flex justify-center py-8"><Loader2 className="w-6 h-6 animate-spin text-emerald-500" /></div>
           : comments.length === 0 ? <p className="text-center text-muted-foreground py-8 text-sm">{t('beFirstToComment')}</p>
           : comments.map(c => {
            const canDel = user && (c.author_id === user.id || user.email === 'mohammadalrejab@gmail.com');
            return (
              <div key={c.id} className={cn("flex gap-2.5", c.reply_to && "ms-8 border-s-2 border-emerald-900/50 ps-3")}>
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
          <div className="flex items-center gap-2 p-3 border-t border-border/20 bg-card" dir={dir}
            style={{ paddingBottom: 'max(12px, env(safe-area-inset-bottom, 12px))' }}>
            <input ref={inputRef} value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && submit()}
              placeholder={replyTo ? `${t('replyToPlaceholder')} ${replyTo.author_name}...` : t('writeComment')}
              className="flex-1 bg-muted/30 text-foreground rounded-full px-4 py-2.5 text-sm placeholder:text-muted-foreground/60 border border-border/20 outline-none focus:border-emerald-600/50" />
            <button onClick={submit} disabled={!text.trim()}
              className="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center disabled:opacity-30 active:scale-90 transition-transform">
              <Send className="w-4 h-4 text-white" />
            </button>
          </div>
        ) : (
          <div className="p-4 border-t border-border/20 text-center"
            style={{ paddingBottom: 'max(12px, env(safe-area-inset-bottom, 12px))' }}>
            <Link to="/auth" className="text-emerald-500 text-sm font-bold hover:underline">{t('loginToComment')}</Link>
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}

/* ==================== CREATE POST SHEET ==================== */
function CreateSheet({ categories, onClose, onCreated }: {
  categories: Category[]; onClose: () => void; onCreated: (s: Story) => void;
}) {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const [content, setContent] = useState('');
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('general');
  const [contentType, setContentType] = useState('text');
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState('');
  const [embedUrl, setEmbedUrl] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]; if (!f) return;
    setFile(f);
    const reader = new FileReader();
    reader.onload = ev => setPreview(ev.target?.result as string);
    reader.readAsDataURL(f);
    setContentType(f.type.startsWith('video/') ? 'video_short' : 'image');
  };

  const submit = async () => {
    if (!content.trim() && !embedUrl.trim()) { toast.error(t('writeFirst')); return; }
    if (!user) { toast.error(t('loginFirst')); return; }
    setSubmitting(true);
    try {
      let imageUrl: string | null = null;
      let videoUrl: string | null = null;

      if (file) {
        const fd = new FormData(); fd.append('file', file);
        const r = await fetch(`${BACKEND_URL}/api/upload/multipart`, { method: 'POST', headers: authHeadersMultipart(), body: fd });
        if (r.ok) {
          const d = await r.json();
          if (file.type.startsWith('video/')) videoUrl = d.url;
          else imageUrl = d.url;
        } else { toast.error(t('uploadFailed')); setSubmitting(false); return; }
      }

      if (contentType === 'embed' && embedUrl.trim()) {
        const body: Record<string, string> = {
          content: content.trim() || embedUrl,
          category,
          embed_url: embedUrl.trim(),
          media_type: 'embed',
          title: title.trim() || '',
        };
        const r = await fetch(`${BACKEND_URL}/api/stories/create`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(body) });
        const d = await r.json();
        if (d.story) { onCreated(d.story); onClose(); toast.success(t('publishSuccess')); }
        else toast.error(d.detail || t('publishFailed'));
      } else {
        const storyBody: Record<string, string | undefined> = {
          content: content.trim(),
          category,
          title: title.trim() || '',
          image_url: imageUrl || (videoUrl ? videoUrl : undefined),
          media_type: videoUrl ? 'video' : imageUrl ? 'image' : 'text',
        };
        const r = await fetch(`${BACKEND_URL}/api/stories/create`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(storyBody) });
        const d = await r.json();
        if (d.story) { onCreated(d.story); onClose(); toast.success(t('publishSuccess')); }
        else toast.error(d.detail || t('publishFailed'));
      }
    } catch (err) { toast.error(t('errorOccurred')); console.error(err); }
    setSubmitting(false);
  };

  const isAdmin = user?.email === 'mohammadalrejab@gmail.com';

  const typeBtns = [
    { key: 'text', label: t('textType'), icon: BookOpen },
    { key: 'image', label: t('imageType'), icon: Image },
    { key: 'video_short', label: t('videosTab'), icon: Video },
    ...(isAdmin ? [{ key: 'embed', label: t('embedType'), icon: Compass }] : []),
  ];

  const catBtns = [
    { key: 'general', label: t('storyCatGeneral'), e: '🌟' },
    { key: 'istighfar', label: t('storyCatIstighfar'), e: '🤲' },
    { key: 'sahaba', label: t('storyCatSahaba'), e: '⚔️' },
    { key: 'quran', label: t('storyCatQuran'), e: '📖' },
    { key: 'prophets', label: t('storyCatProphets'), e: '🕌' },
    { key: 'ruqyah', label: t('storyCatRuqyah'), e: '🛡️' },
    { key: 'rizq', label: t('storyCatRizq'), e: '💎' },
    { key: 'tawba', label: t('storyCatTawba'), e: '💧' },
    { key: 'miracles', label: t('storyCatMiracles'), e: '✨' },
  ];

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[60] bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="absolute bottom-0 left-0 right-0 max-h-[92vh] bg-card rounded-t-3xl overflow-y-auto border-t border-primary/20"
        onClick={e => e.stopPropagation()}>
        <div className="p-5 space-y-4" dir={dir}>
          <div className="w-10 h-1 bg-muted-foreground/20 rounded-full mx-auto -mt-1 mb-2" />
          <div className="flex items-center justify-between">
            <h3 className="text-foreground font-bold text-lg">{t('newPost')}</h3>
            <button onClick={onClose} className="p-2 rounded-full bg-muted/30 active:scale-90 transition-transform"><X className="w-5 h-5 text-muted-foreground" /></button>
          </div>

          {/* Content Type Selector */}
          <div className="flex gap-2 overflow-x-auto pb-1" style={{ scrollbarWidth: 'none' }}>
            {typeBtns.map(btn => {
              const Icon = btn.icon;
              return (
                <button key={btn.key} onClick={() => setContentType(btn.key)}
                  className={cn('shrink-0 flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all',
                    contentType === btn.key ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/20' : 'bg-muted/30 text-muted-foreground hover:bg-muted/50')}>
                  <Icon className="w-4 h-4" /> {btn.label}
                </button>
              );
            })}
          </div>

          {user && (
            <div className="flex items-center gap-3">
              <img src={avatar(user.name || '', user.avatar)} alt="" className="w-10 h-10 rounded-full ring-2 ring-emerald-600/20" />
              <span className="text-foreground font-bold text-sm">{user.name}</span>
            </div>
          )}

          <input data-testid="create-post-title" value={title} onChange={e => setTitle(e.target.value)} placeholder={t("titleOptional")}
            className="w-full bg-muted/20 text-foreground rounded-xl px-4 py-3 text-sm border border-border/20 outline-none focus:border-emerald-600/50 placeholder:text-muted-foreground/50 transition-colors" />

          <textarea data-testid="create-post-content" value={content} onChange={e => setContent(e.target.value)}
            placeholder={t("shareIdea")}
            className="w-full bg-muted/20 text-foreground rounded-xl px-4 py-3 text-sm min-h-[120px] resize-none border border-border/20 outline-none focus:border-emerald-600/50 placeholder:text-muted-foreground/50 leading-relaxed transition-colors"
            maxLength={10000} />
          <p className={cn("text-start text-[10px]", content.length > 9500 ? "text-red-400" : content.length > 5000 ? "text-amber-400" : "text-muted-foreground")}>{content.length}/10000</p>

          {contentType === 'embed' && (
            <input value={embedUrl} onChange={e => setEmbedUrl(e.target.value)}
              placeholder={t('videoUrlPlaceholder')}
              className="w-full bg-muted/20 text-foreground rounded-xl px-4 py-3 text-sm border border-border/20 outline-none focus:border-emerald-600/50 placeholder:text-muted-foreground/50" dir="ltr" />
          )}

          {(contentType === 'image' || contentType === 'video_short') && (
            <>
              <input ref={fileRef} type="file" accept={contentType === 'image' ? 'image/*' : 'video/*'} onChange={handleFile} className="hidden" />
              {preview ? (
                <div className="relative rounded-xl overflow-hidden">
                  {file?.type.startsWith('video/') ? (
                    <video src={preview} controls className="w-full max-h-52 rounded-xl bg-black" />
                  ) : (
                    <img src={preview} alt="" className="w-full max-h-52 object-cover rounded-xl" />
                  )}
                  <button onClick={() => { setFile(null); setPreview(''); }}
                    className="absolute top-2 start-2 w-7 h-7 bg-black/70 rounded-full flex items-center justify-center"><X className="w-3.5 h-3.5 text-white" /></button>
                </div>
              ) : (
                <button onClick={() => fileRef.current?.click()}
                  className="w-full py-12 border-2 border-dashed border-border/30 rounded-xl text-muted-foreground hover:border-emerald-600/50 hover:text-emerald-500 transition-all flex flex-col items-center gap-3 bg-muted/10">
                  {contentType === 'image' ? <Image className="w-8 h-8" /> : <Video className="w-8 h-8" />}
                  <span className="text-sm font-medium">{contentType === 'image' ? t('chooseImage') : t('chooseVideo')}</span>
                </button>
              )}
            </>
          )}

          <div>
            <p className="text-muted-foreground text-xs mb-2 font-medium">{t('categoryLabel')}</p>
            <div className="flex flex-wrap gap-2">
              {catBtns.map(c => (
                <button key={c.key} onClick={() => setCategory(c.key)}
                  className={cn('px-3 py-2 rounded-xl text-xs font-medium transition-all',
                    category === c.key ? 'bg-emerald-600 text-white shadow-sm' : 'bg-muted/20 text-muted-foreground hover:bg-muted/40')}>
                  {c.e} {c.label}
                </button>
              ))}
            </div>
          </div>

          <button data-testid="create-post-submit" onClick={submit} disabled={submitting || (!content.trim() && !embedUrl.trim())}
            className="w-full py-3.5 bg-gradient-to-r from-emerald-600 to-emerald-500 text-white rounded-xl font-bold text-sm disabled:opacity-30 active:scale-[0.98] transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/20">
            {submitting ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-4 h-4" />}
            {t('publishNow')}
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ==================== STORY READER ==================== */
function StoryReader({ story, onBack, onOpenViewer, videoIdx }: {
  story: Story; onBack: () => void; onOpenViewer: (i: number) => void; videoIdx: number;
}) {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const [liked, setLiked] = useState(story.liked);
  const [likesCount, setLikesCount] = useState(story.likes_count);
  const [saved, setSaved] = useState(story.saved);
  const [commentsCount, setCommentsCount] = useState(story.comments_count);
  const [showComments, setShowComments] = useState(false);

  const isEmbed = story.is_embed || story.media_type === 'embed';
  const ytId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;
  const mediaUrl = getMediaUrl(story.image_url);
  const isVideo = story.media_type === 'video' || story.content_type?.includes('video') || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));

  const toggleLike = async () => {
    if (!user) { toast.error(t('loginRequired')); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setLiked(d.liked); setLikesCount(prev => d.liked ? prev + 1 : prev - 1);
    } catch {}
  };

  const toggleSave = async () => {
    if (!user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/save`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setSaved(d.saved); toast.success(d.saved ? t('savedPost') : t('deleted'));
    } catch {}
  };

  const handleShare = async () => {
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/share`, { method: 'POST', headers: authHeaders() });
    } catch {}
    if (navigator.share) {
      navigator.share({ title: story.title || t('myStoriesTab'), text: story.content }).catch(() => {});
    } else {
      navigator.clipboard.writeText(story.content);
      toast.success(t('contentCopied'));
    }
  };

  const paragraphs = story.content.split('\n').filter(p => p.trim());
  const contentWithAds: Array<{ type: 'text' | 'ad'; content?: string }> = [];
  paragraphs.forEach((p, i) => {
    contentWithAds.push({ type: 'text', content: p });
    if ((i + 1) % 3 === 0 && i < paragraphs.length - 1) {
      contentWithAds.push({ type: 'ad' });
    }
  });

  return (
    <div className="min-h-[100dvh] bg-background" dir={dir}
      style={{ paddingBottom: 'max(80px, calc(80px + env(safe-area-inset-bottom, 0px)))' }}>
      {/* Header */}
      <div className="sticky top-0 z-40 bg-background/90 backdrop-blur-xl border-b border-border/10"
        style={{ paddingTop: 'env(safe-area-inset-top, 0px)' }}>
        <div className="flex items-center justify-between px-4 h-14">
          <button onClick={onBack} className="p-2 rounded-xl bg-muted/30 active:scale-95 transition-transform">
            {dir === 'rtl' ? <ArrowRight className="h-5 w-5 text-foreground" /> : <ArrowLeft className="h-5 w-5 text-foreground" />}
          </button>
          <h2 className="text-sm font-bold text-foreground/80 truncate flex-1 mx-3 text-center">
            {story.title || t('thePost')}
          </h2>
          {(isVideo || isEmbed) && (
            <button onClick={() => onOpenViewer(videoIdx)} className="p-2 rounded-xl bg-muted/30 active:scale-95 transition-transform">
              <Play className="h-4 w-4 text-emerald-500" />
            </button>
          )}
        </div>
      </div>

      {/* Media */}
      {ytId ? (
        <div className="w-full aspect-video bg-black">
          <iframe src={`https://www.youtube.com/embed/${ytId}?rel=0`} title={story.title}
            className="w-full h-full" frameBorder={0}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
        </div>
      ) : isEmbed && story.embed_url ? (
        <div className="w-full aspect-video bg-black"><iframe src={story.embed_url} className="w-full h-full" frameBorder={0} allowFullScreen /></div>
      ) : isVideo && mediaUrl ? (
        <div className="w-full aspect-video bg-black"><video src={mediaUrl} className="w-full h-full object-contain" controls autoPlay playsInline /></div>
      ) : mediaUrl ? (
        <div className="w-full max-h-80 overflow-hidden"><img src={mediaUrl} alt="" className="w-full object-cover" /></div>
      ) : null}

      {/* Author */}
      <div className="px-5 pt-5 pb-3">
        <div className="flex items-center gap-3">
          <Link to={`/social-profile/${story.author_id}`}>
            <img src={avatar(story.author_name, story.author_avatar)} alt=""
              className="h-11 w-11 rounded-full ring-2 ring-emerald-600/20" />
          </Link>
          <div className="flex-1">
            <Link to={`/social-profile/${story.author_id}`} className="text-sm font-bold text-foreground hover:underline">
              {story.author_name}
            </Link>
            <p className="text-[11px] text-muted-foreground">{timeAgo(story.created_at)}</p>
          </div>
        </div>
      </div>

      {story.title && <h1 className="text-xl font-bold text-foreground px-5 mb-3">{story.title}</h1>}

      <div className="px-5">
        {contentWithAds.map((item, i) => (
          item.type === 'ad' ? (
            <div key={`ad-${i}`} className="my-4"><AdBanner position="home" /></div>
          ) : (
            <p key={i} className="text-[15px] text-foreground/80 leading-[2.4] mb-2"
              style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>
              {item.content}
            </p>
          )
        ))}
      </div>

      {/* Actions Bar */}
      <div className="mx-5 mt-6 flex items-center gap-4 py-4 border-t border-border/20">
        <button onClick={toggleLike} className="flex items-center gap-1.5 active:scale-90 transition-transform">
          <Heart className={cn("h-6 w-6", liked ? "text-red-500 fill-red-500" : "text-muted-foreground")} />
          <span className={cn("font-bold text-sm", liked ? "text-red-500" : "text-muted-foreground")}>{likesCount}</span>
        </button>
        <button onClick={() => setShowComments(true)} className="flex items-center gap-1.5 active:scale-90 transition-transform">
          <MessageCircle className="h-6 w-6 text-muted-foreground" />
          <span className="font-bold text-sm text-muted-foreground">{commentsCount}</span>
        </button>
        <button onClick={handleShare} className="active:scale-90 transition-transform">
          <Share2 className="h-6 w-6 text-muted-foreground" />
        </button>
        <button onClick={toggleSave} className="active:scale-90 transition-transform ms-auto">
          <Bookmark className={cn("h-6 w-6", saved ? "text-emerald-500 fill-emerald-500" : "text-muted-foreground")} />
        </button>
        <span className="flex items-center gap-1 text-[11px] text-muted-foreground"><Eye className="h-3.5 w-3.5" />{story.views_count || 0}</span>
      </div>

      <AnimatePresence>
        {showComments && <CommentsSheet storyId={story.id} onClose={() => setShowComments(false)}
          onCountChange={d => setCommentsCount(prev => prev + d)} />}
      </AnimatePresence>
    </div>
  );
}

/* ==================== FULLSCREEN VIEWER ==================== */
function FullscreenViewer({ stories, initialIndex, onClose }: { stories: Story[]; initialIndex: number; onClose: () => void }) {
  const { t } = useLocale();
  const [idx, setIdx] = useState(initialIndex);
  const [showComments, setShowComments] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const story = stories[idx];

  const handleScroll = useCallback(() => {
    if (!containerRef.current) return;
    const newIdx = Math.round(containerRef.current.scrollTop / containerRef.current.clientHeight);
    if (newIdx !== idx && newIdx >= 0 && newIdx < stories.length) setIdx(newIdx);
  }, [idx, stories.length]);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTo({ top: initialIndex * containerRef.current.clientHeight, behavior: 'auto' });
    }
  }, []);

  if (!story) return null;

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[70] bg-black">
      <div className="absolute top-0 left-0 right-0 z-30 flex items-center justify-between px-4 py-3 bg-gradient-to-b from-black/70 to-transparent"
        style={{ paddingTop: 'max(12px, env(safe-area-inset-top, 12px))' }}>
        <button onClick={onClose} className="text-white p-2 rounded-full bg-black/30 backdrop-blur-sm active:scale-90 transition-transform"><X className="w-6 h-6" /></button>
        <span className="text-white/50 text-xs bg-black/30 px-3 py-1 rounded-full backdrop-blur-sm">{idx + 1}/{stories.length}</span>
        <div className="w-10" />
      </div>
      <div ref={containerRef} onScroll={handleScroll}
        className="h-full overflow-y-scroll snap-y snap-mandatory"
        style={{ scrollbarWidth: 'none', WebkitOverflowScrolling: 'touch' }}>
        {stories.map((s, i) => (
          <ViewerSlide key={s.id} story={s} isActive={i === idx} onOpenComments={() => setShowComments(true)} />
        ))}
      </div>
      <AnimatePresence>
        {showComments && <CommentsSheet storyId={story.id} onClose={() => setShowComments(false)} onCountChange={() => {}} />}
      </AnimatePresence>
    </motion.div>
  );
}

function ViewerSlide({ story, isActive, onOpenComments }: { story: Story; isActive: boolean; onOpenComments: () => void }) {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(false);
  const [liked, setLiked] = useState(story.liked);
  const [likesCount, setLikesCount] = useState(story.likes_count);

  const isEmbed = story.is_embed || story.media_type === 'embed';
  const ytId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;
  const mediaUrl = getMediaUrl(story.image_url || story.video_url);
  const isVideo = story.media_type === 'video' || story.content_type?.includes('video') || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));

  useEffect(() => {
    if (!videoRef.current) return;
    if (isActive) videoRef.current.play().catch(() => {});
    else { videoRef.current.pause(); videoRef.current.currentTime = 0; }
  }, [isActive]);

  const toggleLike = async () => {
    if (!user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setLiked(d.liked); setLikesCount(prev => d.liked ? prev + 1 : prev - 1);
    } catch {}
  };

  return (
    <div className="h-[100dvh] w-full snap-start relative flex items-center justify-center bg-black">
      {ytId ? (
        <iframe src={`https://www.youtube.com/embed/${ytId}?autoplay=${isActive ? 1 : 0}&rel=0&loop=1&controls=0`}
          className="absolute inset-0 w-full h-full" frameBorder={0} allow="autoplay; encrypted-media" />
      ) : isVideo && mediaUrl ? (
        <video ref={videoRef} src={mediaUrl} className="absolute inset-0 w-full h-full object-contain" loop muted={muted} playsInline />
      ) : mediaUrl ? (
        <div className="absolute inset-0"><img src={mediaUrl} alt="" className="w-full h-full object-cover" /><div className="absolute inset-0 bg-black/30" /></div>
      ) : (
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-900 via-gray-900 to-black" />
      )}

      {story.content && (
        <div className="absolute inset-x-0 bottom-32 px-6 z-10 pointer-events-none" dir={dir}>
          <p className="text-white text-lg font-bold leading-relaxed drop-shadow-lg text-center">{story.content}</p>
        </div>
      )}

      <div className="absolute end-3 bottom-36 flex flex-col items-center gap-5 z-20">
        <Link to={`/social-profile/${story.author_id}`}>
          <img src={avatar(story.author_name, story.author_avatar)} alt="" className="w-11 h-11 rounded-full border-2 border-white shadow-lg" />
        </Link>
        <button onClick={toggleLike} className="flex flex-col items-center">
          <Heart className={cn("w-7 h-7 drop-shadow-lg", liked ? "fill-red-500 text-red-500" : "text-white")} />
          <span className="text-white text-[11px] mt-0.5 font-bold">{likesCount}</span>
        </button>
        <button onClick={onOpenComments} className="flex flex-col items-center">
          <MessageCircle className="w-7 h-7 text-white drop-shadow-lg" />
          <span className="text-white text-[11px] mt-0.5 font-bold">{story.comments_count}</span>
        </button>
        <button className="flex flex-col items-center">
          <Share2 className="w-7 h-7 text-white drop-shadow-lg" />
        </button>
        {isVideo && <button onClick={() => setMuted(!muted)}>
          {muted ? <VolumeX className="w-5 h-5 text-white/50" /> : <Volume2 className="w-5 h-5 text-white/50" />}
        </button>}
      </div>

      <div className="absolute bottom-5 end-4 start-16 z-20" dir={dir}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-white font-bold text-sm drop-shadow-lg">{story.author_name}</span>
          <span className="px-2 py-0.5 bg-emerald-600 text-white text-[10px] font-bold rounded-md">{t('follow')}</span>
        </div>
        {story.title && <p className="text-white/80 text-xs drop-shadow line-clamp-1">{story.title}</p>}
      </div>
    </div>
  );
}

/* ==================== MAIN STORIES PAGE ==================== */
export default function Stories() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { t, dir, locale } = useLocale();
  const [searchParams, setSearchParams] = useSearchParams();
  const [categories, setCategories] = useState<Category[]>([]);
  const [stories, setStories] = useState<Story[]>([]);
  const [activeTab, setActiveTab] = useState<'forYou' | 'reels' | 'videos' | 'following'>('forYou');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(() => searchParams.get('cat'));
  const [showCreate, setShowCreate] = useState(false);
  const [showCommentsFor, setShowCommentsFor] = useState<string | null>(null);
  const [showViewer, setShowViewer] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [recommended, setRecommended] = useState<any[]>([]);
  const [followedIds, setFollowedIds] = useState<Set<string>>(new Set());
  const [unlockedStoryIds, setUnlockedStoryIds] = useState<Set<string>>(new Set());

  const selectedStoryId = searchParams.get('story');

  const PREMIUM_CATS = new Set(['prophets', 'miracles', 'ruqyah']);
  const isPremiumStory = (s: Story) => s.is_premium || PREMIUM_CATS.has(s.category);
  const isStoryUnlocked = (s: Story) => !isPremiumStory(s) || unlockedStoryIds.has(s.id) || s.author_id === user?.id;

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/stories/categories`).then(r => r.json())
      .then(d => setCategories(d.categories || [])).catch(() => {});
    const h: Record<string, string> = {}; const tk = getToken(); if (tk) h.Authorization = `Bearer ${tk}`;
    fetch(`${BACKEND_URL}/api/sohba/recommended-users?limit=8`, { headers: h })
      .then(r => r.json()).then(d => setRecommended(d.users || [])).catch(() => {});
    if (user) {
      fetch(`${BACKEND_URL}/api/stories/check-unlocked?user_id=${user.id}`)
        .then(r => r.json()).then(d => {
          if (d.success) setUnlockedStoryIds(new Set(d.unlocked_story_ids || []));
        }).catch(() => {});
    }
    if (searchParams.get('create') === 'true' && user) {
      setShowCreate(true);
      const p = new URLSearchParams(searchParams);
      p.delete('create');
      setSearchParams(p, { replace: true });
    }
  }, [user]);

  useEffect(() => {
    const handler = () => { if (user) setShowCreate(true); };
    window.addEventListener('open-create-story', handler);
    return () => window.removeEventListener('open-create-story', handler);
  }, [user]);

  const handleSelectCategory = useCallback((cat: string | null) => {
    setSelectedCategory(cat);
    const params = new URLSearchParams(searchParams);
    if (cat) params.set('cat', cat); else params.delete('cat');
    params.delete('story');
    setSearchParams(params, { replace: true });
  }, [searchParams, setSearchParams]);

  const handleOpenStory = useCallback((storyId: string) => {
    const s = stories.find(x => x.id === storyId);
    if (s && isPremiumStory(s) && !isStoryUnlocked(s)) {
      const cost = s.points_cost || 2;
      const msg = t('storyPremiumUnlock').replace('{cost}', String(cost));
      if (confirm(msg)) { unlockPremiumStory(storyId, cost); }
      return;
    }
    const params = new URLSearchParams(searchParams);
    params.set('story', storyId);
    setSearchParams(params);
  }, [searchParams, setSearchParams, stories, unlockedStoryIds, locale]);

  const unlockPremiumStory = async (storyId: string, cost: number = 2) => {
    if (!user) { toast.error(t('loginRequired')); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/stories/unlock-premium`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.id, story_id: storyId, points_cost: cost, mode: 'adults' }),
      });
      const d = await r.json();
      if (d.success) {
        setUnlockedStoryIds(prev => new Set([...prev, storyId]));
        toast.success(`${t('storyUnlocked')} -${cost} ${t('storyPoints')}`);
        const params = new URLSearchParams(searchParams);
        params.set('story', storyId);
        setSearchParams(params);
      } else if (d.message === 'insufficient_points') {
        toast.error(t('insufficientPointsStory'));
      }
    } catch { toast.error(t('genericError')); }
  };

  const handleBackFromStory = useCallback(() => {
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) window.history.back();
    else setSearchParams({}, { replace: true });
  }, [setSearchParams]);

  const loadStories = useCallback(async (cat?: string, pageNum: number = 1, append: boolean = false) => {
    if (pageNum === 1) setLoading(true); else setLoadingMore(true);
    const langParam = `&language=${locale}`;
    let url: string;

    if (activeTab === 'following' && user) {
      url = `${BACKEND_URL}/api/sohba/feed/following?limit=20&page=${pageNum}`;
    } else {
      url = cat
        ? `${BACKEND_URL}/api/stories/list-translated?category=${cat}&limit=20&page=${pageNum}${langParam}`
        : `${BACKEND_URL}/api/stories/list-translated?limit=20&page=${pageNum}${langParam}`;
    }

    try {
      const r = await fetch(url, { headers: authHeaders() });
      const d = await r.json();
      const ns = d.stories || d.posts || [];
      if (append) setStories(prev => [...prev, ...ns]); else setStories(ns);
      setHasMore(ns.length >= 20);
    } catch {}
    setLoading(false); setLoadingMore(false);
  }, [locale, activeTab, user]);

  useEffect(() => {
    setPage(1); setHasMore(true);
    loadStories(selectedCategory || undefined, 1, false);
  }, [selectedCategory, loadStories, activeTab]);

  const toggleLike = async (id: string) => {
    if (!user) { toast.error(t('loginRequired')); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStories(p => p.map(x => x.id === id ? { ...x, liked: d.liked, likes_count: x.likes_count + (d.liked ? 1 : -1) } : x));
    } catch {}
  };

  const toggleSave = async (id: string) => {
    if (!user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/save`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStories(p => p.map(x => x.id === id ? { ...x, saved: d.saved } : x));
      toast.success(d.saved ? t('savedPost') : t('deleted'));
    } catch {}
  };

  const handleShare = async (id: string) => {
    const s = stories.find(x => x.id === id); if (!s) return;
    try { await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/share`, { method: 'POST', headers: authHeaders() }); } catch {}
    if (navigator.share) navigator.share({ title: s.title || t('myStoriesTab'), text: s.content }).catch(() => {});
    else { navigator.clipboard.writeText(s.content); toast.success(t('contentCopied')); }
  };

  const handleFollow = async (uid: string) => {
    if (!user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/follow/${uid}`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setFollowedIds(prev => { const n = new Set(prev); d.following ? n.add(uid) : n.delete(uid); return n; });
    } catch {}
  };

  // === STORY READER VIEW ===
  if (selectedStoryId) {
    const story = stories.find(s => s.id === selectedStoryId);
    if (!story) {
      return <StoryReaderFetch storyId={selectedStoryId} onBack={handleBackFromStory} stories={stories} />;
    }
    const videoStories = stories.filter(s => s.is_embed || s.media_type === 'embed' || s.media_type === 'video' || s.content_type?.includes('video'));
    const vidIdx = videoStories.findIndex(v => v.id === story.id);
    return (
      <>
        <StoryReader story={story} onBack={handleBackFromStory}
          onOpenViewer={(i) => setShowViewer(i)} videoIdx={vidIdx >= 0 ? vidIdx : 0} />
        <AnimatePresence>
          {showViewer !== null && <FullscreenViewer stories={videoStories} initialIndex={showViewer} onClose={() => setShowViewer(null)} />}
        </AnimatePresence>
      </>
    );
  }

  const videoStories = stories.filter(s => s.is_embed || s.media_type === 'embed' || s.media_type === 'video' || s.content_type?.includes('video'));
  const textStories = stories.filter(s => !s.is_embed && s.media_type !== 'embed' && s.media_type !== 'video' && !s.content_type?.includes('video'));

  const tabs = [
    { key: 'forYou' as const, label: t('forYouTab'), icon: Flame },
    { key: 'reels' as const, label: t('reelsTab'), icon: Film },
    { key: 'videos' as const, label: t('longVideosTab'), icon: Play },
    { key: 'following' as const, label: t('followingTab'), icon: Users },
  ];

  return (
    <div className="min-h-[100dvh] bg-background" dir={dir} data-testid="stories-page"
      style={{ paddingBottom: 'max(80px, calc(80px + env(safe-area-inset-bottom, 0px)))' }}>

      {/* === MODERN HEADER === */}
      <div className="sticky top-0 z-50" style={{ paddingTop: 'env(safe-area-inset-top, 0px)' }}>
        <div className="bg-background/95 backdrop-blur-xl border-b border-border/10">
          {/* Top bar */}
          <div className="flex items-center justify-between px-4 pt-3 pb-2">
            <Link to="/explore" className="h-10 w-10 rounded-full bg-muted/30 flex items-center justify-center active:scale-90 transition-transform">
              <Search className="w-[18px] h-[18px] text-foreground/60" />
            </Link>

            <h1 className="text-lg font-extrabold text-foreground tracking-tight">
              {t('navStories')}
            </h1>

            {user ? (
              <button data-testid="create-post-btn" onClick={() => setShowCreate(true)}
                className="h-10 w-10 rounded-full bg-emerald-600 flex items-center justify-center active:scale-90 transition-transform shadow-lg shadow-emerald-600/25">
                <Plus className="w-[18px] h-[18px] text-white" />
              </button>
            ) : <div className="w-10" />}
          </div>

          {/* Tabs */}
          <div className="flex px-4 gap-1">
            {tabs.map(tab => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.key;
              return (
                <button key={tab.key} onClick={() => setActiveTab(tab.key)}
                  className={cn(
                    "flex-1 flex items-center justify-center gap-1.5 py-2.5 text-[12px] font-bold transition-all relative",
                    isActive ? "text-foreground" : "text-muted-foreground/60"
                  )}>
                  <Icon className="w-3.5 h-3.5" />
                  <span>{tab.label}</span>
                  {isActive && (
                    <motion.div layoutId="stories-tab-indicator"
                      className="absolute bottom-0 left-2 right-2 h-[2.5px] bg-emerald-500 rounded-full"
                      transition={{ type: 'spring', stiffness: 400, damping: 30 }} />
                  )}
                </button>
              );
            })}
          </div>

          {/* Category pills - only on forYou tab */}
          {activeTab === 'forYou' && (
            <div className="px-3 pt-2 pb-3">
              <div className="flex gap-2 overflow-x-auto no-scrollbar" style={{ scrollbarWidth: 'none' }}>
                <button onClick={() => handleSelectCategory(null)}
                  className={cn(
                    "shrink-0 px-4 py-2 rounded-full text-[12px] font-bold transition-all",
                    !selectedCategory
                      ? 'bg-emerald-600 text-white shadow-sm'
                      : 'bg-muted/20 text-muted-foreground hover:bg-muted/40'
                  )}>
                  {t('allLabel')}
                </button>
                {categories.map(cat => (
                  <button key={cat.key} onClick={() => handleSelectCategory(cat.key)}
                    className={cn(
                      "shrink-0 px-4 py-2 rounded-full text-[12px] font-bold transition-all flex items-center gap-1.5",
                      selectedCategory === cat.key
                        ? 'bg-emerald-600 text-white shadow-sm'
                        : 'bg-muted/20 text-muted-foreground hover:bg-muted/40'
                    )}>
                    <span>{cat.emoji}</span>
                    {cat.labelKey ? t(cat.labelKey) : cat.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* === CONTENT === */}
      <div className="px-3 py-3">

        {/* TAB: Reels Grid */}
        {activeTab === 'reels' && (
          <>
            {loading ? (
              <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-emerald-500" /></div>
            ) : videoStories.length === 0 && textStories.length === 0 ? (
              <EmptyState icon={Film} title={t('noReelsYet')} subtitle={t('noContent')}
                action={user ? { label: t('addVideo'), onClick: () => setShowCreate(true) } : undefined} />
            ) : (
              <div className="grid grid-cols-3 gap-1 sm:gap-1.5">
                {[...videoStories, ...stories].slice(0, 30).map((s, idx) => {
                  const mediaUrl = getMediaUrl(s.image_url || s.thumbnail_url);
                  const ytId = s.embed_url ? getYouTubeId(s.embed_url) : null;
                  const isVid = s.media_type === 'video' || s.is_embed;
                  return (
                    <div key={`${s.id}-${idx}`}
                      onClick={() => isVid ? setShowViewer(videoStories.findIndex(v => v.id === s.id)) : handleOpenStory(s.id)}
                      className="relative aspect-[9/14] rounded-xl overflow-hidden cursor-pointer group bg-muted/10">
                      {mediaUrl ? (
                        <img src={ytId ? `https://img.youtube.com/vi/${ytId}/hqdefault.jpg` : mediaUrl}
                          alt="" className="w-full h-full object-cover" loading="lazy" />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-emerald-950/50 to-muted/20 flex items-center justify-center">
                          {isVid ? <Film className="w-8 h-8 text-white/10" /> : <BookOpen className="w-8 h-8 text-white/10" />}
                        </div>
                      )}
                      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />
                      {isVid && (
                        <div className="absolute top-2 start-2">
                          <Play className="w-4 h-4 text-white fill-white drop-shadow" />
                        </div>
                      )}
                      <div className="absolute bottom-0 start-0 end-0 p-2">
                        <p className="text-white text-[10px] font-bold line-clamp-2 leading-snug drop-shadow">{s.title || s.content}</p>
                        <div className="flex items-center gap-2 mt-1">
                          <span className="text-white/60 text-[9px] flex items-center gap-0.5">
                            <Heart className="w-2.5 h-2.5" /> {formatCount(s.likes_count)}
                          </span>
                          {s.views_count ? (
                            <span className="text-white/60 text-[9px] flex items-center gap-0.5">
                              <Eye className="w-2.5 h-2.5" /> {formatCount(s.views_count)}
                            </span>
                          ) : null}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </>
        )}

        {/* TAB: Long Videos (YouTube style) */}
        {activeTab === 'videos' && (
          <>
            {loading ? (
              <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-emerald-500" /></div>
            ) : videoStories.length === 0 ? (
              <EmptyState icon={Play} title={t('noVideosYet')} subtitle={t('noContent')}
                action={user ? { label: t('addVideo'), onClick: () => setShowCreate(true) } : undefined} />
            ) : (
              <div className="space-y-4">
                {videoStories.map((s, idx) => {
                  const mediaUrl = getMediaUrl(s.image_url || s.thumbnail_url);
                  const ytId = s.embed_url ? getYouTubeId(s.embed_url) : null;
                  const thumbUrl = ytId ? `https://img.youtube.com/vi/${ytId}/hqdefault.jpg` : mediaUrl;
                  return (
                    <div key={s.id} onClick={() => setShowViewer(idx)}
                      className="bg-card rounded-2xl overflow-hidden border border-border/10 cursor-pointer active:scale-[0.99] transition-transform shadow-sm">
                      {/* Thumbnail */}
                      <div className="relative aspect-video bg-black/50">
                        {thumbUrl ? (
                          <img src={thumbUrl} alt="" className="w-full h-full object-cover" loading="lazy" />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-emerald-950 to-black">
                            <Film className="w-12 h-12 text-white/10" />
                          </div>
                        )}
                        <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-colors" />
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="w-14 h-14 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center border border-white/10">
                            <Play className="w-7 h-7 text-white fill-white ms-0.5" />
                          </div>
                        </div>
                        {s.views_count ? (
                          <div className="absolute bottom-2 end-2 bg-black/60 backdrop-blur-sm px-2 py-0.5 rounded text-[10px] text-white font-medium">
                            {formatCount(s.views_count)} {t('views')}
                          </div>
                        ) : null}
                      </div>
                      {/* Info */}
                      <div className="p-3 flex gap-3">
                        <img src={avatar(s.author_name, s.author_avatar)} alt=""
                          className="w-10 h-10 rounded-full shrink-0 ring-1 ring-border/20" />
                        <div className="flex-1 min-w-0">
                          <h3 className="text-foreground text-[14px] font-bold line-clamp-2 leading-snug">{s.title || s.content}</h3>
                          <p className="text-muted-foreground text-[12px] mt-1">
                            {s.author_name} • {timeAgo(s.created_at)} • {formatCount(s.likes_count)} ❤️
                          </p>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </>
        )}

        {/* TAB: For You / Following (Feed) */}
        {(activeTab === 'forYou' || activeTab === 'following') && (
          <>
            {loading ? (
              <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-emerald-500" /></div>
            ) : stories.length === 0 ? (
              <EmptyState
                icon={activeTab === 'following' ? Users : BookOpen}
                title={activeTab === 'following' ? t('noFollowingContent') : t('noContent')}
                subtitle={t('createContent')}
                action={user ? { label: t('createContent'), onClick: () => setShowCreate(true) } : undefined}
              />
            ) : (
              <>
                {/* Recommended Users */}
                {activeTab === 'forYou' && recommended.length > 0 && (
                  <div className="mb-4">
                    <h3 className="text-foreground/70 text-[13px] font-bold mb-3 flex items-center gap-1.5 px-1">
                      <Users className="w-3.5 h-3.5 text-emerald-500" /> {t('recommendedUsers')}
                    </h3>
                    <div className="flex gap-2.5 overflow-x-auto pb-2" style={{ scrollbarWidth: 'none' }}>
                      {recommended.map(u => (
                        <div key={u.id} className="shrink-0 w-[85px] flex flex-col items-center bg-card rounded-2xl p-2.5 gap-2 border border-border/10">
                          <Link to={`/social-profile/${u.id}`}>
                            <img src={avatar(u.name, u.avatar)} alt="" className="w-12 h-12 rounded-full ring-2 ring-emerald-600/20" />
                          </Link>
                          <span className="text-foreground text-[10px] font-bold text-center truncate w-full">{u.name}</span>
                          <button onClick={() => handleFollow(u.id)}
                            className={cn("w-full py-1.5 rounded-lg text-[10px] font-bold transition-all active:scale-95",
                              followedIds.has(u.id) ? 'bg-muted/30 text-muted-foreground border border-border/20' : 'bg-emerald-600 text-white shadow-sm')}>
                            {followedIds.has(u.id) ? t('unfollow') : t('follow')}
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Video Reels Row */}
                {activeTab === 'forYou' && videoStories.length > 0 && (
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-3 px-1">
                      <h2 className="text-[14px] font-bold text-foreground flex items-center gap-1.5">
                        <Film className="h-4 w-4 text-emerald-500" /> {t('reelsTab')}
                      </h2>
                      <button onClick={() => setActiveTab('reels')} className="text-[12px] text-emerald-500 font-bold">{t('allLabel')}</button>
                    </div>
                    <div className="flex gap-2 overflow-x-auto" style={{ scrollbarWidth: 'none' }}>
                      {videoStories.slice(0, 6).map((s, idx) => {
                        const mUrl = getMediaUrl(s.image_url || s.thumbnail_url);
                        const ytId = s.embed_url ? getYouTubeId(s.embed_url) : null;
                        return (
                          <div key={s.id} onClick={() => setShowViewer(idx)}
                            className="shrink-0 w-28 aspect-[9/14] rounded-2xl overflow-hidden cursor-pointer relative bg-muted/10 active:scale-95 transition-transform">
                            {mUrl ? (
                              <img src={ytId ? `https://img.youtube.com/vi/${ytId}/hqdefault.jpg` : mUrl}
                                alt="" className="w-full h-full object-cover" />
                            ) : (
                              <div className="w-full h-full bg-gradient-to-br from-emerald-950/40 to-muted/20" />
                            )}
                            <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
                            <div className="absolute inset-0 flex items-center justify-center">
                              <div className="w-10 h-10 rounded-full bg-white/15 backdrop-blur-sm flex items-center justify-center">
                                <Play className="w-5 h-5 text-white fill-white" />
                              </div>
                            </div>
                            <p className="absolute bottom-2 start-2 end-2 text-white text-[9px] font-bold line-clamp-2">{s.title || s.content}</p>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Posts Feed */}
                <div className="space-y-3">
                  {(activeTab === 'forYou' ? textStories : stories).map((s, idx) => (
                    <div key={s.id}>
                      {idx > 0 && idx % 4 === 0 && (
                        <div className="mb-3"><IslamicAd placement="stories" variant="banner" /></div>
                      )}
                      <div className="bg-card rounded-2xl overflow-hidden border border-border/10 shadow-sm active:scale-[0.99] transition-transform">
                        {/* Media */}
                        {getMediaUrl(s.image_url) && (
                          <div className="relative cursor-pointer" onClick={() => handleOpenStory(s.id)}>
                            <img src={getMediaUrl(s.image_url)!} alt="" className="w-full max-h-56 object-cover" loading="lazy" />
                          </div>
                        )}
                        <div className="p-3.5 cursor-pointer" onClick={() => handleOpenStory(s.id)}>
                          {/* Author row */}
                          <div className="flex items-center gap-3 mb-2.5">
                            <img src={avatar(s.author_name, s.author_avatar)} alt="" className="h-9 w-9 rounded-full ring-1 ring-border/20" />
                            <div className="flex-1 min-w-0">
                              <span className="text-[13px] font-bold text-foreground block">{s.author_name}</span>
                              <span className="text-[10px] text-muted-foreground/50">{timeAgo(s.created_at)}</span>
                            </div>
                            {isPremiumStory(s) && (
                              <span className={cn(
                                "px-2 py-0.5 rounded-full text-[9px] font-bold flex items-center gap-0.5",
                                isStoryUnlocked(s) ? "bg-emerald-600/10 text-emerald-500" : "bg-amber-500/10 text-amber-500"
                              )}>
                                {isStoryUnlocked(s) ? <Star className="h-2.5 w-2.5" /> : <Lock className="h-2.5 w-2.5" />}
                                {isStoryUnlocked(s) ? t('premiumStory') : `${s.points_cost || 2} ${t('storyPoints')}`}
                              </span>
                            )}
                          </div>
                          {s.title && <h3 className="text-[15px] font-bold text-foreground mb-1.5 leading-snug">{s.title}</h3>}
                          <p className={cn("text-[13px] text-muted-foreground leading-[1.7] line-clamp-3",
                            isPremiumStory(s) && !isStoryUnlocked(s) && "blur-[3px] select-none"
                          )}>{s.content}</p>
                          {isPremiumStory(s) && !isStoryUnlocked(s) && (
                            <div className="mt-2 flex items-center gap-2 text-amber-500 text-xs font-bold">
                              <Lock className="h-3 w-3" /><span>{t('storyUnlockFor')} {s.points_cost || 2} {t('storyPoints')}</span>
                            </div>
                          )}
                        </div>
                        {/* Action bar */}
                        <div className="flex items-center px-3.5 pb-3 pt-0">
                          <div className="flex items-center gap-5 flex-1">
                            <button onClick={() => toggleLike(s.id)} className="flex items-center gap-1 active:scale-90 transition-transform">
                              <Heart className={cn("h-5 w-5", s.liked ? "text-red-500 fill-red-500" : "text-muted-foreground/40")} />
                              <span className={cn("text-[11px] font-bold", s.liked ? "text-red-500" : "text-muted-foreground/40")}>{s.likes_count || 0}</span>
                            </button>
                            <button onClick={() => setShowCommentsFor(s.id)} className="flex items-center gap-1 active:scale-90 transition-transform">
                              <MessageCircle className="h-5 w-5 text-muted-foreground/40" />
                              <span className="text-[11px] font-bold text-muted-foreground/40">{s.comments_count || 0}</span>
                            </button>
                            <button onClick={() => handleShare(s.id)} className="active:scale-90 transition-transform">
                              <Send className="h-[18px] w-[18px] text-muted-foreground/40" />
                            </button>
                          </div>
                          <button onClick={() => toggleSave(s.id)} className="active:scale-90 transition-transform">
                            <Bookmark className={cn("h-5 w-5", s.saved ? "text-emerald-500 fill-emerald-500" : "text-muted-foreground/40")} />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {hasMore && stories.length >= 20 && (
                  <div className="flex justify-center mt-6 mb-4">
                    <button onClick={() => { const n = page + 1; setPage(n); loadStories(selectedCategory || undefined, n, true); }}
                      disabled={loadingMore}
                      className="px-8 py-3 rounded-xl bg-card border border-border/20 text-emerald-500 text-[13px] font-bold active:scale-95 transition-transform disabled:opacity-50 shadow-sm">
                      {loadingMore ? <Loader2 className="h-4 w-4 animate-spin mx-auto" /> : t('loadMore')}
                    </button>
                  </div>
                )}
              </>
            )}
          </>
        )}
      </div>

      {/* Modals */}
      <AnimatePresence>
        {showCreate && <CreateSheet categories={categories} onClose={() => setShowCreate(false)} onCreated={s => setStories(prev => [s, ...prev])} />}
        {showCommentsFor && <CommentsSheet storyId={showCommentsFor} onClose={() => setShowCommentsFor(null)}
          onCountChange={d => setStories(p => p.map(x => x.id === showCommentsFor ? { ...x, comments_count: x.comments_count + d } : x))} />}
        {showViewer !== null && <FullscreenViewer stories={videoStories} initialIndex={showViewer} onClose={() => setShowViewer(null)} />}
      </AnimatePresence>
    </div>
  );
}

/* ==================== EMPTY STATE COMPONENT ==================== */
function EmptyState({ icon: Icon, title, subtitle, action }: {
  icon: React.ElementType; title: string; subtitle: string;
  action?: { label: string; onClick: () => void };
}) {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="w-20 h-20 rounded-3xl bg-muted/10 flex items-center justify-center mb-5 border border-border/10">
        <Icon className="h-10 w-10 text-muted-foreground/20" />
      </div>
      <p className="text-foreground text-[15px] font-bold mb-1.5">{title}</p>
      <p className="text-muted-foreground/50 text-[13px] text-center max-w-[250px] mb-6">{subtitle}</p>
      {action && (
        <button onClick={action.onClick}
          className="px-8 py-3 bg-emerald-600 text-white rounded-xl text-[13px] font-bold active:scale-95 transition-transform shadow-lg shadow-emerald-600/20">
          {action.label}
        </button>
      )}
    </div>
  );
}

/* Helper: Fetch and show a single story */
function StoryReaderFetch({ storyId, onBack, stories }: { storyId: string; onBack: () => void; stories: Story[] }) {
  const { t } = useLocale();
  const [story, setStory] = useState<Story | null>(null);
  const [loading, setLoading] = useState(true);
  const [showViewer, setShowViewer] = useState<number | null>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/stories/${storyId}`, { headers: authHeaders() })
      .then(r => r.json()).then(d => { setStory(d.story || null); setLoading(false); })
      .catch(() => setLoading(false));
  }, [storyId]);

  if (loading) return <div className="min-h-[100dvh] bg-background flex items-center justify-center"><Loader2 className="h-8 w-8 animate-spin text-emerald-500" /></div>;
  if (!story) return <div className="min-h-[100dvh] bg-background flex items-center justify-center text-muted-foreground">{t('contentNotFound')}</div>;

  return (
    <>
      <StoryReader story={story} onBack={onBack} onOpenViewer={(i) => setShowViewer(i)} videoIdx={0} />
      <AnimatePresence>
        {showViewer !== null && <FullscreenViewer stories={[story]} initialIndex={0} onClose={() => setShowViewer(null)} />}
      </AnimatePresence>
    </>
  );
}
