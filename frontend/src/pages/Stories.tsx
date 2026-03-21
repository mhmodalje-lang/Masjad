import { useLocale } from "@/hooks/useLocale";
import { useState, useEffect, useCallback, useRef } from 'react';
import {
  Heart, MessageCircle, Send, X, Loader2, Image, Video,
  BookOpen, Plus, Eye, ArrowRight, Share2, Bookmark, Film,
  Play, Volume2, VolumeX, Trash2, Reply, Search, Users,
  ChevronDown, TrendingUp, Flame, Star, Clock, Hash
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
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
}
interface Comment {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  content: string; created_at: string; reply_to?: string;
}
interface Category { key: string; label: string; emoji: string; icon: string; color: string; }

function timeAgo(iso: string, t?: (k: string) => string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return t ? t('now') : 'Now';
  if (m < 60) return t ? t('minutesAgo').replace('{n}', String(m)) : `${m}m`;
  const h = Math.floor(m / 60);
  if (h < 24) return t ? t('hoursAgo').replace('{n}', String(h)) : `${h}h`;
  const days = Math.floor(h / 24);
  if (days < 30) return t ? t('daysAgo').replace('{n}', String(days)) : `${days}d`;
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
      const body: any = { content: text.trim() };
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
              <div key={c.id} className={cn("flex gap-2.5", c.reply_to && "mr-8 border-r-2 border-emerald-900/50 pr-3")}>
                <img src={avatar(c.author_name, c.author_avatar)} alt="" className="w-8 h-8 rounded-full shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] font-bold text-foreground">{c.author_name}</span>
                    <span className="text-[10px] text-muted-foreground">{timeAgo(c.created_at)}</span>
                  </div>
                  <p className="text-foreground/80 text-[13px] mt-0.5 leading-relaxed">{c.content}</p>
                  <div className="flex items-center gap-4 mt-1">
                    <button onClick={() => { setReplyTo(c); inputRef.current?.focus(); }}
                      className="flex items-center gap-1 text-[11px] text-muted-foreground hover:text-emerald-400">
                      <Reply className="w-3 h-3" /> {t('replyLabel')}
                    </button>
                    {canDel && (
                      <button onClick={() => deleteComment(c.id)}
                        className="flex items-center gap-1 text-[11px] text-muted-foreground hover:text-red-400">
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
            <span className="text-xs text-emerald-400">{t('replyTo')} {replyTo.author_name}</span>
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
            <Link to="/auth" className="text-emerald-400 text-sm font-bold hover:underline">{t('loginToComment')}</Link>
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

      // Upload file if exists
      if (file) {
        const fd = new FormData(); fd.append('file', file);
        const r = await fetch(`${BACKEND_URL}/api/upload/multipart`, { method: 'POST', headers: authHeadersMultipart(), body: fd });
        if (r.ok) {
          const d = await r.json();
          if (file.type.startsWith('video/')) videoUrl = d.url;
          else imageUrl = d.url;
        } else { toast.error(t('uploadFailed')); setSubmitting(false); return; }
      }

      // Handle embed (YouTube etc) - admin only
      if (contentType === 'embed' && embedUrl.trim()) {
        const body: any = {
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
        // Create story via correct endpoint
        const storyBody: any = {
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
    { key: 'text', label: 'نص', icon: '📝' },
    { key: 'image', label: t('imageType'), icon: '🖼️' },
    { key: 'video_short', label: t('videosTab'), icon: '🎬' },
    ...(isAdmin ? [{ key: 'embed', label: t('embedType'), icon: '🔗' }] : []),
  ];

  const catBtns = [
    { key: 'general', label: t('generalCategory'), e: '🌍' },
    { key: 'quran', label: t('quranCategory'), e: '📖' },
    { key: 'hadith', label: t('hadithCategory'), e: '📜' },
    { key: 'dua', label: t('duaCategory'), e: '🤲' },
    { key: 'stories', label: t('storiesCategory'), e: '✍️' },
    { key: 'family', label: t('familyCategory'), e: '👨‍👩‍👧' },
  ];

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[60] bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="absolute bottom-0 left-0 right-0 max-h-[92vh] bg-card rounded-t-[28px] overflow-y-auto border-t border-primary/30"
        onClick={e => e.stopPropagation()}>
        <div className="p-5 space-y-4" dir={dir}>
          {/* Handle bar */}
          <div className="w-10 h-1 bg-white/10 rounded-full mx-auto -mt-1 mb-2" />

          <div className="flex items-center justify-between">
            <h3 className="text-foreground font-bold text-lg">{t('newPost')}</h3>
            <button onClick={onClose} className="p-2 rounded-full bg-muted/30"><X className="w-5 h-5 text-muted-foreground" /></button>
          </div>

          {/* Content Type */}
          <div className="flex gap-2 overflow-x-auto pb-1" style={{ scrollbarWidth: 'none' }}>
            {typeBtns.map(btn => (
              <button key={btn.key} onClick={() => setContentType(btn.key)}
                className={cn('shrink-0 flex items-center gap-1.5 px-4 py-2.5 rounded-2xl text-sm font-medium transition-all',
                  contentType === btn.key ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/20' : 'bg-muted/30 text-muted-foreground hover:bg-muted/50')}>
                <span>{btn.icon}</span> {btn.label}
              </button>
            ))}
          </div>

          {/* Author */}
          {user && (
            <div className="flex items-center gap-3">
              <img src={avatar(user.name || '', user.avatar)} alt="" className="w-10 h-10 rounded-full" />
              <span className="text-foreground font-bold text-sm">{user.name}</span>
            </div>
          )}

          {/* Title (optional) */}
          <input data-testid="create-post-title" value={title} onChange={e => setTitle(e.target.value)} placeholder={t("titleOptional")}
            className="w-full bg-muted/30 text-foreground rounded-2xl px-4 py-3 text-sm border border-border/20 outline-none focus:border-emerald-600/50 placeholder:text-muted-foreground/60" />

          {/* Content */}
          <textarea data-testid="create-post-content" value={content} onChange={e => setContent(e.target.value)}
            placeholder={t("shareIdea")}
            className="w-full bg-muted/30 text-foreground rounded-2xl px-4 py-3 text-sm min-h-[140px] resize-none border border-border/20 outline-none focus:border-emerald-600/50 placeholder:text-muted-foreground/60 leading-relaxed"
            maxLength={5000} />
          <p className="text-left text-muted-foreground text-[10px]">{content.length}/5000</p>

          {/* Embed URL */}
          {contentType === 'embed' && (
            <input value={embedUrl} onChange={e => setEmbedUrl(e.target.value)}
              placeholder={t('videoUrlPlaceholder')}
              className="w-full bg-muted/30 text-foreground rounded-2xl px-4 py-3 text-sm border border-border/20 outline-none focus:border-emerald-600/50 placeholder:text-muted-foreground/60" dir="ltr" />
          )}

          {/* File Upload */}
          {(contentType === 'image' || contentType === 'video_short') && (
            <>
              <input ref={fileRef} type="file" accept={contentType === 'image' ? 'image/*' : 'video/*'} onChange={handleFile} className="hidden" />
              {preview ? (
                <div className="relative rounded-2xl overflow-hidden">
                  {file?.type.startsWith('video/') ? (
                    <video src={preview} controls className="w-full max-h-52 rounded-2xl bg-black" />
                  ) : (
                    <img src={preview} alt="" className="w-full max-h-52 object-cover rounded-2xl" />
                  )}
                  <button onClick={() => { setFile(null); setPreview(''); }}
                    className="absolute top-2 left-2 w-7 h-7 bg-black/70 rounded-full flex items-center justify-center"><X className="w-3.5 h-3.5 text-white" /></button>
                </div>
              ) : (
                <button onClick={() => fileRef.current?.click()}
                  className="w-full py-14 border border-dashed border-border/30 rounded-2xl text-muted-foreground hover:border-emerald-600/50 hover:text-emerald-500 transition-all flex flex-col items-center gap-2 bg-muted/15">
                  {contentType === 'image' ? <Image className="w-7 h-7" /> : <Video className="w-7 h-7" />}
                  <span className="text-sm">{contentType === 'image' ? t('chooseImage') : t('chooseVideo')}</span>
                </button>
              )}
            </>
          )}

          {/* Category */}
          <div>
            <p className="text-muted-foreground text-xs mb-2">{t('categoryLabel')}</p>
            <div className="flex flex-wrap gap-2">
              {catBtns.map(c => (
                <button key={c.key} onClick={() => setCategory(c.key)}
                  className={cn('px-3.5 py-2 rounded-2xl text-xs font-medium transition-all',
                    category === c.key ? 'bg-emerald-600 text-white' : 'bg-muted/30 text-muted-foreground hover:bg-muted/50')}>
                  {c.e} {c.label}
                </button>
              ))}
            </div>
          </div>

          {/* Submit */}
          <button data-testid="create-post-submit" onClick={submit} disabled={submitting || (!content.trim() && !embedUrl.trim())}
            className="w-full py-3.5 bg-gradient-to-r from-emerald-600 to-emerald-500 text-white rounded-2xl font-bold text-sm disabled:opacity-30 active:scale-[0.98] transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/20">
            {submitting ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-4 h-4" />}
            {t('publishNow')}
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ==================== STORY READER (قارئ القصة) ==================== */
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

  // Split content for ad placement (every 3 paragraphs)
  const paragraphs = story.content.split('\n').filter(p => p.trim());
  const contentWithAds: Array<{ type: 'text' | 'ad'; content?: string }> = [];
  paragraphs.forEach((p, i) => {
    contentWithAds.push({ type: 'text', content: p });
    if ((i + 1) % 3 === 0 && i < paragraphs.length - 1) {
      contentWithAds.push({ type: 'ad' });
    }
  });

  return (
    <div className="min-h-screen bg-background pb-24" dir={dir}>
      {/* Header */}
      <div className="sticky top-0 z-40 bg-background/95 backdrop-blur-xl border-b border-border/20">
        <div className="flex items-center justify-between px-4 h-14">
          <button onClick={onBack} className="p-2 rounded-xl bg-muted/30 active:scale-95">
            <ArrowRight className="h-5 w-5 text-foreground" />
          </button>
          <h2 className="text-sm font-bold text-foreground/80 truncate flex-1 mx-3 text-center">
            {story.title || t('thePost')}
          </h2>
          {(isVideo || isEmbed) && (
            <button onClick={() => onOpenViewer(videoIdx)} className="p-2 rounded-xl bg-muted/30">
              <Play className="h-4 w-4 text-emerald-400" />
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
              className="h-11 w-11 rounded-full border-2 border-emerald-600/30" />
          </Link>
          <div className="flex-1">
            <Link to={`/social-profile/${story.author_id}`} className="text-sm font-bold text-foreground hover:underline">
              {story.author_name}
            </Link>
            <p className="text-[11px] text-muted-foreground">{timeAgo(story.created_at)}</p>
          </div>
        </div>
      </div>

      {/* Title */}
      {story.title && (
        <h1 className="text-xl font-bold text-foreground px-5 mb-3">{story.title}</h1>
      )}

      {/* Content with inline ads */}
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
        <button onClick={toggleSave} className="active:scale-90 transition-transform mr-auto">
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
  const { user } = useAuth();
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

  const goNext = useCallback(() => {
    if (idx < stories.length - 1) {
      const newIdx = idx + 1;
      setIdx(newIdx);
      if (containerRef.current) {
        containerRef.current.scrollTo({ top: newIdx * containerRef.current.clientHeight, behavior: 'smooth' });
      }
    }
  }, [idx, stories.length]);

  const goPrev = useCallback(() => {
    if (idx > 0) {
      const newIdx = idx - 1;
      setIdx(newIdx);
      if (containerRef.current) {
        containerRef.current.scrollTo({ top: newIdx * containerRef.current.clientHeight, behavior: 'smooth' });
      }
    }
  }, [idx]);

  if (!story) return null;

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[70] bg-black">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-30 flex items-center justify-between px-4 py-3 bg-gradient-to-b from-black/70 to-transparent">
        <button onClick={onClose} className="text-white p-2 rounded-full bg-black/30 backdrop-blur-sm active:scale-90 transition-transform"><X className="w-6 h-6" /></button>
        <span className="text-white/50 text-xs bg-black/30 px-3 py-1 rounded-full backdrop-blur-sm">{idx + 1}/{stories.length}</span>
        <div className="w-10" />
      </div>

      {/* Previous Button */}
      {idx > 0 && (
        <button
          onClick={goPrev}
          className="absolute top-1/2 -translate-y-1/2 right-3 z-30 w-10 h-10 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center text-white/80 hover:bg-black/60 active:scale-90 transition-all"
          aria-label={t('previous') || 'Previous'}
        >
          <ChevronDown className="w-5 h-5 rotate-180" />
        </button>
      )}

      {/* Next Button */}
      {idx < stories.length - 1 && (
        <button
          onClick={goNext}
          className="absolute bottom-24 right-3 z-30 w-10 h-10 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center text-white/80 hover:bg-black/60 active:scale-90 transition-all"
          aria-label={t('next') || 'Next'}
        >
          <ChevronDown className="w-5 h-5" />
        </button>
      )}

      <div ref={containerRef} onScroll={handleScroll}
        className="h-full overflow-y-scroll snap-y snap-mandatory"
        style={{ scrollbarWidth: 'none' }}>
        {stories.map((s, i) => <ReelSlide key={s.id} story={s} isActive={i === idx} onOpenComments={() => setShowComments(true)} />)}
      </div>
      <AnimatePresence>
        {showComments && <CommentsSheet storyId={story.id} onClose={() => setShowComments(false)} onCountChange={() => {}} />}
      </AnimatePresence>
    </motion.div>
  );
}

function ReelSlide({ story, isActive, onOpenComments }: { story: Story; isActive: boolean; onOpenComments: () => void }) {
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
    <div className="h-screen w-full snap-start relative flex items-center justify-center bg-black">
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

      <div className="absolute left-3 bottom-36 flex flex-col items-center gap-5 z-20">
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

      <div className="absolute bottom-5 right-4 left-16 z-20" dir={dir}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-white font-bold text-sm drop-shadow-lg">{story.author_name}</span>
          <span className="px-2 py-0.5 bg-emerald-600 text-white text-[10px] font-bold rounded-md">{t('follow')}</span>
        </div>
        {story.title && <p className="text-white/80 text-xs drop-shadow line-clamp-1">{story.title}</p>}
      </div>
    </div>
  );
}

/* ==================== MAIN حكاياتي PAGE ==================== */
export default function Stories() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { t, dir, locale } = useLocale();
  const [searchParams, setSearchParams] = useSearchParams();
  const [categories, setCategories] = useState<Category[]>([]);
  const [stories, setStories] = useState<Story[]>([]);
  const [activeTab, setActiveTab] = useState<'trending' | 'video'>('trending');
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

  const selectedStoryId = searchParams.get('story');

  // Load categories + recommended users
  useEffect(() => {
    fetch(`${BACKEND_URL}/api/stories/categories`).then(r => r.json())
      .then(d => setCategories(d.categories || [])).catch(() => {});
    const h: Record<string, string> = {}; const tk = getToken(); if (tk) h.Authorization = `Bearer ${tk}`;
    fetch(`${BACKEND_URL}/api/sohba/recommended-users?limit=8`, { headers: h })
      .then(r => r.json()).then(d => setRecommended(d.users || [])).catch(() => {});
    // Open create sheet from URL
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
    const params = new URLSearchParams(searchParams);
    params.set('story', storyId);
    setSearchParams(params);
  }, [searchParams, setSearchParams]);

  const handleBackFromStory = useCallback(() => {
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) window.history.back();
    else setSearchParams({}, { replace: true });
  }, [setSearchParams]);

  const loadStories = useCallback(async (cat?: string, pageNum: number = 1, append: boolean = false) => {
    if (pageNum === 1) setLoading(true); else setLoadingMore(true);
    const langParam = `&language=${locale}`;
    const url = cat
      ? `${BACKEND_URL}/api/stories/list-translated?category=${cat}&limit=20&page=${pageNum}${langParam}`
      : `${BACKEND_URL}/api/stories/list-translated?limit=20&page=${pageNum}${langParam}`;
    try {
      const r = await fetch(url, { headers: authHeaders() });
      const d = await r.json();
      const ns = d.stories || [];
      if (append) setStories(prev => [...prev, ...ns]); else setStories(ns);
      setHasMore(ns.length >= 20);
    } catch {}
    setLoading(false); setLoadingMore(false);
  }, [locale]);

  useEffect(() => {
    setPage(1); setHasMore(true);
    loadStories(selectedCategory || undefined, 1, false);
  }, [selectedCategory, loadStories]);

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
      // Fetch story if not in current list
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

  const sortedCats = [...categories].sort((a, b) => {
    if (a.key === 'general') return -1; if (b.key === 'general') return 1;
    if (a.key === 'embed') return -1; if (b.key === 'embed') return 1;
    return 0;
  });

  const videoStories = stories.filter(s => s.is_embed || s.media_type === 'embed' || s.media_type === 'video' || s.content_type?.includes('video'));
  const textStories = stories.filter(s => !s.is_embed && s.media_type !== 'embed' && s.media_type !== 'video' && !s.content_type?.includes('video'));

  return (
    <div className="min-h-screen bg-background pb-24" dir={dir} data-testid="stories-page">
      {/* === MODERN 2026 HEADER === */}
      <div className="sticky top-0 z-50">
        <div className="relative bg-gradient-to-b from-emerald-800 via-teal-700 to-emerald-800/95 backdrop-blur-xl overflow-hidden">
          {/* Geometric pattern */}
          <div className="absolute inset-0 opacity-[0.06]" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23fff' fill-opacity='.3'%3E%3Cpath d='M40 10L50 30H30z M40 70L30 50H50z M10 40L30 30V50z M70 40L50 50V30z'/%3E%3C/g%3E%3C/svg%3E")`,
          }} />
          <div className="absolute top-0 left-2 text-base opacity-40 animate-pulse">🏮</div>
          <div className="absolute top-0 right-2 text-base opacity-40 animate-pulse" style={{ animationDelay: '0.7s' }}>🏮</div>

          <div className="relative flex items-center justify-between px-4 pt-3 pb-2">
            <Link to="/explore" className="p-2.5 rounded-2xl bg-white/15 backdrop-blur-sm hover:bg-white/25 transition-all text-white">
              <Search className="w-[18px] h-[18px]" />
            </Link>
            <div className="flex items-center gap-5 text-white">
              <button onClick={() => setActiveTab('video')}
                className={cn("text-[15px] font-bold transition-all pb-1", activeTab === 'video' ? 'text-white border-b-2 border-emerald-300' : 'text-white/50')}>
                {t('videoTab')}
              </button>
              <button onClick={() => setActiveTab('trending')}
                className={cn("text-[15px] font-bold transition-all pb-1", activeTab === 'trending' ? 'text-white border-b-2 border-emerald-300' : 'text-white/50')}>
                {t('trendsTab')}
              </button>
              <h1 className="text-[17px] font-black flex items-center gap-1.5 text-white">
                <BookOpen className="w-[18px] h-[18px]" /> {t('myStoriesTab')}
              </h1>
            </div>
            {user ? (
              <button data-testid="create-post-btn" onClick={() => setShowCreate(true)} className="p-2.5 rounded-2xl bg-white/15 backdrop-blur-sm hover:bg-white/25 text-white">
                <Plus className="w-[18px] h-[18px]" />
              </button>
            ) : <div className="w-10" />}
          </div>

          {/* Category pills */}
          {activeTab === 'trending' && (
            <div className="relative flex gap-1.5 px-3 pb-3 overflow-x-auto" style={{ scrollbarWidth: 'none' }}>
              <button onClick={() => handleSelectCategory(null)}
                className={cn('shrink-0 px-4 py-[7px] rounded-full text-[12px] font-bold transition-all',
                  !selectedCategory ? 'bg-white text-emerald-800 shadow-md' : 'bg-white/15 text-white/80 hover:bg-white/25')}>
                <Flame className="w-3 h-3 inline mr-1" />{t('allLabel')}
              </button>
              {sortedCats.map(cat => (
                <button key={cat.key} onClick={() => handleSelectCategory(cat.key)}
                  className={cn('shrink-0 flex items-center gap-1 px-3.5 py-[7px] rounded-full text-[12px] font-bold transition-all',
                    selectedCategory === cat.key ? 'bg-white text-emerald-800 shadow-md' : 'bg-white/15 text-white/80 hover:bg-white/25')}>
                  <span className="text-sm">{cat.emoji}</span>{cat.labelKey ? t(cat.labelKey) : cat.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* === CONTENT === */}
      <div className="px-3 py-3">
        {activeTab === 'video' ? (
          videoStories.length === 0 ? (
            <div className="text-center py-20">
              <Film className="w-14 h-14 text-muted-foreground mx-auto mb-3" />
              <p className="text-muted-foreground text-sm">{t('noVideosYet')}</p>
              {user && <button onClick={() => setShowCreate(true)}
                className="mt-4 px-6 py-2.5 bg-emerald-600 text-white rounded-2xl text-sm font-bold">{t('addVideo')}</button>}
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-2">
              {videoStories.map((s, idx) => (
                <div key={s.id} onClick={() => setShowViewer(idx)}
                  className="relative aspect-[9/14] rounded-2xl overflow-hidden cursor-pointer group bg-gray-900">
                  {getMediaUrl(s.image_url || s.thumbnail_url) ? (
                    <img src={getMediaUrl(s.image_url || s.thumbnail_url)!} alt="" className="w-full h-full object-cover" loading="lazy" />
                  ) : s.embed_url && getYouTubeId(s.embed_url) ? (
                    <img src={`https://img.youtube.com/vi/${getYouTubeId(s.embed_url)}/hqdefault.jpg`} alt="" className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-emerald-900 to-gray-900 flex items-center justify-center">
                      <Film className="w-8 h-8 text-white/10" />
                    </div>
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
                  <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                      <Play className="w-6 h-6 text-white fill-white" />
                    </div>
                  </div>
                  <div className="absolute bottom-0 left-0 right-0 p-2.5">
                    <p className="text-white text-[11px] font-bold line-clamp-2">{s.title || s.content}</p>
                    <span className="text-white/50 text-[10px]">{s.author_name}</span>
                  </div>
                </div>
              ))}
            </div>
          )
        ) : (
          <>
            {loading ? (
              <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-emerald-500" /></div>
            ) : stories.length === 0 ? (
              <div className="text-center py-10">
                <BookOpen className="h-14 w-14 text-muted-foreground mx-auto mb-3" />
                <p className="text-muted-foreground text-sm mb-6">{t('noContent')}</p>
                {user && <button onClick={() => setShowCreate(true)}
                  className="bg-emerald-600 text-white px-8 py-3 rounded-2xl text-sm font-bold active:scale-95">{t('createContent')}</button>}
              </div>
            ) : (
              <>
                {/* Recommended Users */}
                {recommended.length > 0 && (
                  <div className="mb-4">
                    <h3 className="text-foreground/80 text-[13px] font-bold mb-2.5 flex items-center gap-1.5">
                      <Users className="w-3.5 h-3.5 text-emerald-500" /> {t('recommendedUsers')}
                    </h3>
                    <div className="flex gap-2.5 overflow-x-auto pb-2" style={{ scrollbarWidth: 'none' }}>
                      {recommended.map(u => (
                        <div key={u.id} className="shrink-0 w-[100px] flex flex-col items-center bg-muted/20 border border-border/20 rounded-2xl p-3 gap-1.5">
                          <Link to={`/social-profile/${u.id}`}>
                            <img src={avatar(u.name, u.avatar)} alt="" className="w-14 h-14 rounded-full border-2 border-emerald-700/50" />
                          </Link>
                          <span className="text-foreground text-[11px] font-bold text-center truncate w-full">{u.name}</span>
                          <button onClick={() => handleFollow(u.id)}
                            className={cn("w-full py-1.5 rounded-xl text-[10px] font-bold transition-all",
                              followedIds.has(u.id) ? 'bg-muted/30 text-muted-foreground' : 'bg-emerald-600 text-white')}>
                            {followedIds.has(u.id) ? t('unfollow') : t('follow')}
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Video section */}
                {videoStories.length > 0 && (
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <h2 className="text-[13px] font-bold text-white/80 flex items-center gap-1.5">
                        <Film className="h-3.5 w-3.5 text-emerald-500" /> {t('videosLabel')}
                      </h2>
                      <button onClick={() => setActiveTab('video')} className="text-[11px] text-emerald-400 font-bold">{t('allLabel')}</button>
                    </div>
                    <div className="flex gap-2 overflow-x-auto" style={{ scrollbarWidth: 'none' }}>
                      {videoStories.slice(0, 4).map((s, idx) => (
                        <div key={s.id} onClick={() => setShowViewer(idx)}
                          className="shrink-0 w-32 aspect-[9/14] rounded-2xl overflow-hidden cursor-pointer relative bg-gray-900">
                          {getMediaUrl(s.image_url || s.thumbnail_url) ? (
                            <img src={getMediaUrl(s.image_url || s.thumbnail_url)!} alt="" className="w-full h-full object-cover" />
                          ) : s.embed_url && getYouTubeId(s.embed_url) ? (
                            <img src={`https://img.youtube.com/vi/${getYouTubeId(s.embed_url)}/hqdefault.jpg`} alt="" className="w-full h-full object-cover" />
                          ) : (
                            <div className="w-full h-full bg-gradient-to-br from-emerald-900 to-gray-900" />
                          )}
                          <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
                          <div className="absolute inset-0 flex items-center justify-center">
                            <Play className="w-6 h-6 text-white/70 fill-white/70" />
                          </div>
                          <p className="absolute bottom-1.5 right-1.5 left-1.5 text-white text-[10px] font-bold line-clamp-2">{s.title || s.content}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Posts */}
                <div className="space-y-3">
                  {textStories.map((s, idx) => (
                    <div key={s.id}>
                      <div className="bg-muted/20 border border-border/20 rounded-2xl overflow-hidden hover:border-primary/30 transition-all">
                        {/* Media */}
                        {getMediaUrl(s.image_url) && (
                          <div className="relative cursor-pointer" onClick={() => handleOpenStory(s.id)}>
                            <img src={getMediaUrl(s.image_url)!} alt="" className="w-full max-h-56 object-cover" loading="lazy" />
                          </div>
                        )}
                        <div className="p-4 cursor-pointer" onClick={() => handleOpenStory(s.id)}>
                          <div className="flex items-center gap-2.5 mb-2.5">
                            <img src={avatar(s.author_name, s.author_avatar)} alt="" className="h-8 w-8 rounded-full" />
                            <span className="text-[13px] font-bold text-foreground">{s.author_name}</span>
                            <span className="text-[10px] text-muted-foreground mr-auto">{timeAgo(s.created_at)}</span>
                          </div>
                          {s.title && <h3 className="text-[15px] font-bold text-foreground mb-1.5 line-clamp-2">{s.title}</h3>}
                          <p className="text-[13px] text-muted-foreground leading-relaxed line-clamp-3">{s.content}</p>
                        </div>
                        <div className="flex items-center justify-between px-4 pb-3 border-t border-border/20 mx-4 pt-2.5">
                          <div className="flex items-center gap-5">
                            <button onClick={() => toggleLike(s.id)} className="flex items-center gap-1.5 text-xs active:scale-90">
                              <Heart className={cn("h-[18px] w-[18px]", s.liked ? "text-red-500 fill-red-500" : "text-muted-foreground")} />
                              <span className={cn("font-bold", s.liked ? "text-red-500" : "text-muted-foreground")}>{s.likes_count || 0}</span>
                            </button>
                            <button onClick={() => setShowCommentsFor(s.id)} className="flex items-center gap-1.5 text-xs active:scale-90">
                              <MessageCircle className="h-[18px] w-[18px] text-muted-foreground" />
                              <span className="font-bold text-muted-foreground">{s.comments_count || 0}</span>
                            </button>
                            <button onClick={() => handleShare(s.id)} className="active:scale-90">
                              <Share2 className="h-[18px] w-[18px] text-muted-foreground" />
                            </button>
                            <button onClick={() => toggleSave(s.id)} className="active:scale-90">
                              <Bookmark className={cn("h-[18px] w-[18px]", s.saved ? "text-emerald-500 fill-emerald-500" : "text-muted-foreground")} />
                            </button>
                          </div>
                        </div>
                      </div>
                      {idx === 2 && <div className="mt-3"><AdBanner position="home" /></div>}
                    </div>
                  ))}
                </div>

                {hasMore && stories.length >= 20 && (
                  <div className="flex justify-center mt-6">
                    <button onClick={() => { const n = page + 1; setPage(n); loadStories(selectedCategory || undefined, n, true); }}
                      disabled={loadingMore}
                      className="px-8 py-3 rounded-2xl bg-muted/30 border border-border/20 text-emerald-400 text-sm font-bold active:scale-95 disabled:opacity-50">
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

  if (loading) return <div className="min-h-screen bg-background flex items-center justify-center"><Loader2 className="h-8 w-8 animate-spin text-emerald-500" /></div>;
  if (!story) return <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground">{t('contentNotFound')}</div>;

  return (
    <>
      <StoryReader story={story} onBack={onBack} onOpenViewer={(i) => setShowViewer(i)} videoIdx={0} />
      <AnimatePresence>
        {showViewer !== null && <FullscreenViewer stories={[story]} initialIndex={0} onClose={() => setShowViewer(null)} />}
      </AnimatePresence>
    </>
  );
}
