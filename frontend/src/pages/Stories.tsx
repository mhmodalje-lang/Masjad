import { useLocale } from '@/hooks/useLocale';
import { useState, useEffect, useCallback, useRef } from 'react';
import { Heart, MessageCircle, Send, X, Loader2, Image, Video, BookOpen, Plus, Eye, ArrowRight, Share2, Bookmark, Film, Play, Maximize2, Volume2, VolumeX, Trash2, Reply, Search, TrendingUp, Users, Gift } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
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
interface RecommendedUser {
  id: string; name: string; avatar?: string; followers_count: number; posts_count: number;
}

const avatarColors = ['bg-amber-600', 'bg-yellow-600', 'bg-orange-600', 'bg-rose-600', 'bg-purple-600', 'bg-teal-600'];

function timeAgo(iso: string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return 'الآن';
  if (m < 60) return `${m}د`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}س`;
  return `${Math.floor(h / 24)}ي`;
}

function getMediaUrl(url?: string) {
  if (!url) return null;
  return url.startsWith('http') ? url : `${BACKEND_URL}${url.startsWith('/') ? '' : '/'}${url}`;
}

function getYouTubeId(url: string): string | null {
  const m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|shorts\/))([^&?\s]+)/);
  return m ? m[1] : null;
}

function getAvatarUrl(name: string, avatar?: string) {
  if (avatar) return avatar;
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || '?')}&background=1a7a4c&color=fff&size=80&bold=true`;
}

/* ==================== COMMENTS SHEET ==================== */
function CommentsSheet({ storyId, onClose, onCommentAdded }: { storyId: string; onClose: () => void; onCommentAdded: () => void }) {
  const { user } = useAuth();
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
        setText('');
        setReplyTo(null);
        onCommentAdded();
      }
    } catch { toast.error('فشل إرسال التعليق'); }
  };

  const deleteComment = async (commentId: string) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/comments/${commentId}`, {
        method: 'DELETE', headers: authHeaders(),
      });
      if (r.ok) {
        setComments(prev => prev.filter(c => c.id !== commentId));
        toast.success('تم حذف التعليق');
      } else {
        toast.error('لا يمكن حذف هذا التعليق');
      }
    } catch { toast.error('خطأ في الحذف'); }
  };

  const handleReply = (comment: Comment) => {
    setReplyTo(comment);
    inputRef.current?.focus();
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 25, stiffness: 300 }}
        className="absolute bottom-0 left-0 right-0 max-h-[75vh] bg-gray-900 rounded-t-3xl overflow-hidden flex flex-col"
        onClick={e => e.stopPropagation()}>

        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-800">
          <h3 className="text-white font-bold text-base">التعليقات ({comments.length})</h3>
          <button onClick={onClose} className="p-1.5 rounded-full bg-gray-800 hover:bg-gray-700">
            <X className="w-4 h-4 text-gray-400" />
          </button>
        </div>

        {/* Comments List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4" dir="rtl">
          {loading ? (
            <div className="flex justify-center py-8"><Loader2 className="w-6 h-6 animate-spin text-emerald-500" /></div>
          ) : comments.length === 0 ? (
            <p className="text-center text-gray-500 py-8">لا توجد تعليقات بعد</p>
          ) : (
            comments.map(c => {
              const ci = (c.author_name || '').charCodeAt(0) % 6;
              const canDelete = user && (c.author_id === user.id || user.email === 'mohammadalrejab@gmail.com');
              const isReply = c.reply_to;
              return (
                <div key={c.id} className={cn("flex gap-3", isReply && "mr-8 border-r-2 border-emerald-700/30 pr-3")}>
                  <img src={getAvatarUrl(c.author_name, c.author_avatar)} alt="" className="w-8 h-8 rounded-full shrink-0 mt-0.5" />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-white">{c.author_name}</span>
                      <span className="text-[10px] text-gray-500">{timeAgo(c.created_at)}</span>
                    </div>
                    <p className="text-gray-300 text-sm mt-0.5 leading-relaxed">{c.content}</p>
                    <div className="flex items-center gap-4 mt-1.5">
                      <button onClick={() => handleReply(c)} className="flex items-center gap-1 text-[11px] text-gray-500 hover:text-emerald-400">
                        <Reply className="w-3 h-3" /> رد
                      </button>
                      {canDelete && (
                        <button onClick={() => deleteComment(c.id)} className="flex items-center gap-1 text-[11px] text-gray-500 hover:text-red-400">
                          <Trash2 className="w-3 h-3" /> حذف
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Reply indicator */}
        {replyTo && (
          <div className="px-4 py-2 bg-gray-800/80 flex items-center justify-between" dir="rtl">
            <span className="text-xs text-emerald-400">الرد على {replyTo.author_name}</span>
            <button onClick={() => setReplyTo(null)} className="text-gray-500 hover:text-white"><X className="w-3 h-3" /></button>
          </div>
        )}

        {/* Input */}
        {user ? (
          <div className="flex items-center gap-2 p-3 border-t border-gray-800 bg-gray-900" dir="rtl">
            <input
              ref={inputRef}
              value={text} onChange={e => setText(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && submit()}
              placeholder={replyTo ? `الرد على ${replyTo.author_name}...` : "اكتب تعليقاً..."}
              className="flex-1 bg-gray-800 text-white rounded-full px-4 py-2.5 text-sm placeholder:text-gray-600 border-none outline-none focus:ring-1 focus:ring-emerald-600"
            />
            <button onClick={submit} disabled={!text.trim()}
              className="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center disabled:opacity-40 active:scale-90 transition-transform">
              <Send className="w-4 h-4 text-white" />
            </button>
          </div>
        ) : (
          <div className="p-3 border-t border-gray-800 text-center">
            <Link to="/auth" className="text-emerald-400 text-sm font-bold">سجّل دخولك للتعليق</Link>
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}

/* ==================== CREATE STORY SHEET ==================== */
function CreateStorySheet({ categories, onClose, onCreated }: {
  categories: Category[]; onClose: () => void; onCreated: (s: Story) => void;
}) {
  const { user } = useAuth();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
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
    if (f.type.startsWith('video/')) setContentType('video_short');
    else if (f.type.startsWith('image/')) setContentType('image');
  };

  const submit = async () => {
    if (!content.trim() && !embedUrl.trim()) { toast.error('اكتب شيئاً'); return; }
    setSubmitting(true);
    try {
      let imageUrl = null;
      let videoUrl = null;
      // Upload file
      if (file) {
        const fd = new FormData(); fd.append('file', file);
        const r = await fetch(`${BACKEND_URL}/api/upload/multipart`, { method: 'POST', headers: authHeadersMultipart(), body: fd });
        if (r.ok) {
          const d = await r.json();
          if (file.type.startsWith('video/')) videoUrl = d.url;
          else imageUrl = d.url;
        }
      }
      // Handle embed
      if (embedUrl.trim()) {
        const body: any = {
          content: content.trim() || embedUrl,
          category,
          embed_url: embedUrl.trim(),
          media_type: 'embed',
          title: title.trim() || undefined,
        };
        const r = await fetch(`${BACKEND_URL}/api/stories`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(body) });
        const d = await r.json();
        if (d.story) { onCreated(d.story); onClose(); toast.success('تم النشر ✨'); }
      } else {
        // Regular post through sohba
        const body: any = {
          content: content.trim(),
          category,
          content_type: contentType,
          image_url: imageUrl,
          video_url: videoUrl,
        };
        const r = await fetch(`${BACKEND_URL}/api/sohba/posts`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(body) });
        const d = await r.json();
        if (d.post) {
          // Also create as story
          const storyBody: any = {
            content: content.trim(),
            category,
            title: title.trim() || undefined,
            image_url: imageUrl || videoUrl,
            media_type: videoUrl ? 'video' : imageUrl ? 'image' : 'text',
          };
          await fetch(`${BACKEND_URL}/api/stories`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(storyBody) });
          onCreated({ ...d.post, liked: false, saved: false, likes_count: 0, comments_count: 0, views_count: 0 } as Story);
          onClose();
          toast.success('تم النشر ✨');
        }
      }
    } catch { toast.error('فشل النشر'); }
    setSubmitting(false);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 25 }}
        className="absolute bottom-0 left-0 right-0 max-h-[90vh] bg-gray-900 rounded-t-3xl overflow-y-auto"
        onClick={e => e.stopPropagation()}>

        <div className="p-5 space-y-4" dir="rtl">
          <div className="flex items-center justify-between">
            <h3 className="text-white font-bold text-lg">إنشاء منشور</h3>
            <button onClick={onClose} className="p-2 rounded-full bg-gray-800"><X className="w-4 h-4 text-gray-400" /></button>
          </div>

          {/* Content Type */}
          <div className="flex gap-2">
            {[
              { key: 'text', label: 'نص', icon: '📝' },
              { key: 'image', label: 'صورة', icon: '🖼️' },
              { key: 'video_short', label: 'ريلز', icon: '🎬' },
              { key: 'embed', label: 'رابط فيديو', icon: '🔗' },
            ].map(ct => (
              <button key={ct.key} onClick={() => setContentType(ct.key)}
                className={cn('px-3 py-2 rounded-xl text-xs font-medium transition-all flex items-center gap-1',
                  contentType === ct.key ? 'bg-emerald-600 text-white' : 'bg-gray-800 text-gray-400')}>
                <span>{ct.icon}</span> {ct.label}
              </button>
            ))}
          </div>

          <input value={title} onChange={e => setTitle(e.target.value)} placeholder="العنوان (اختياري)"
            className="w-full bg-gray-800 text-white rounded-xl px-4 py-3 text-sm border-none outline-none focus:ring-1 focus:ring-emerald-600 placeholder:text-gray-600" />

          <textarea value={content} onChange={e => setContent(e.target.value)} placeholder="شارك فكرتك..."
            className="w-full bg-gray-800 text-white rounded-xl px-4 py-3 text-sm min-h-[120px] resize-none border-none outline-none focus:ring-1 focus:ring-emerald-600 placeholder:text-gray-600 leading-relaxed"
            maxLength={5000} />

          {/* Embed URL */}
          {contentType === 'embed' && (
            <input value={embedUrl} onChange={e => setEmbedUrl(e.target.value)} placeholder="رابط يوتيوب أو فيديو..."
              className="w-full bg-gray-800 text-white rounded-xl px-4 py-3 text-sm border-none outline-none focus:ring-1 focus:ring-emerald-600 placeholder:text-gray-600" dir="ltr" />
          )}

          {/* File Upload */}
          {(contentType === 'image' || contentType === 'video_short') && (
            <>
              <input ref={fileRef} type="file" accept={contentType === 'image' ? 'image/*' : 'video/*'} onChange={handleFile} className="hidden" />
              {preview ? (
                <div className="relative rounded-xl overflow-hidden">
                  {file?.type.startsWith('video/') ? (
                    <video src={preview} controls className="w-full max-h-48 rounded-xl" />
                  ) : (
                    <img src={preview} alt="" className="w-full max-h-48 object-cover rounded-xl" />
                  )}
                  <button onClick={() => { setFile(null); setPreview(''); }}
                    className="absolute top-2 left-2 w-7 h-7 bg-black/60 rounded-full flex items-center justify-center"><X className="w-3 h-3 text-white" /></button>
                </div>
              ) : (
                <button onClick={() => fileRef.current?.click()}
                  className="w-full py-10 border-2 border-dashed border-gray-700 rounded-xl text-gray-500 hover:border-emerald-600 hover:text-emerald-500 transition-colors flex flex-col items-center gap-2">
                  {contentType === 'image' ? <Image className="w-6 h-6" /> : <Video className="w-6 h-6" />}
                  <span className="text-sm">{contentType === 'image' ? 'إضافة صورة' : 'إضافة فيديو'}</span>
                </button>
              )}
            </>
          )}

          {/* Category */}
          <div className="flex flex-wrap gap-2">
            {[
              { key: 'general', label: 'عام', emoji: '🌍' },
              { key: 'quran', label: 'القرآن', emoji: '📖' },
              { key: 'hadith', label: 'الحديث', emoji: '📜' },
              { key: 'dua', label: 'الدعاء', emoji: '🤲' },
              { key: 'stories', label: 'قصص', emoji: '📝' },
              { key: 'family', label: 'الأسرة', emoji: '👨‍👩‍👧‍👦' },
            ].map(cat => (
              <button key={cat.key} onClick={() => setCategory(cat.key)}
                className={cn('px-3 py-1.5 rounded-full text-xs transition-all',
                  category === cat.key ? 'bg-emerald-600 text-white' : 'bg-gray-800 text-gray-400')}>
                {cat.emoji} {cat.label}
              </button>
            ))}
          </div>

          <button onClick={submit} disabled={submitting || (!content.trim() && !embedUrl.trim())}
            className="w-full py-3 bg-emerald-600 text-white rounded-xl font-bold text-sm disabled:opacity-50 active:scale-[0.98] transition-transform flex items-center justify-center gap-2">
            {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            نشر
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ==================== FULLSCREEN VIDEO VIEWER ==================== */
function FullscreenViewer({ stories, initialIndex, onClose }: { stories: Story[]; initialIndex: number; onClose: () => void }) {
  const { user } = useAuth();
  const [idx, setIdx] = useState(initialIndex);
  const [muted, setMuted] = useState(false);
  const [paused, setPaused] = useState(false);
  const [showComments, setShowComments] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const story = stories[idx];

  // Snap scroll handler
  const handleScroll = useCallback(() => {
    if (!containerRef.current) return;
    const scrollTop = containerRef.current.scrollTop;
    const height = containerRef.current.clientHeight;
    const newIdx = Math.round(scrollTop / height);
    if (newIdx !== idx && newIdx >= 0 && newIdx < stories.length) {
      setIdx(newIdx);
    }
  }, [idx, stories.length]);

  // Scroll to initial index
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTo({ top: initialIndex * containerRef.current.clientHeight, behavior: 'auto' });
    }
  }, []);

  const toggleLike = async () => {
    if (!user || !story) return;
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/like`, { method: 'POST', headers: authHeaders() });
    } catch {}
  };

  const handleShare = async () => {
    if (!story) return;
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/share`, { method: 'POST', headers: authHeaders() });
      if (navigator.share) {
        await navigator.share({ title: story.title || 'حكاياتي', text: story.content, url: window.location.href });
      } else {
        await navigator.clipboard.writeText(story.content);
        toast.success('تم نسخ المحتوى');
      }
    } catch {}
  };

  if (!story) return null;

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[70] bg-black">

      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-30 flex items-center justify-between px-4 py-3 bg-gradient-to-b from-black/70 to-transparent">
        <button onClick={onClose} className="text-white p-2"><X className="w-6 h-6" /></button>
        <div className="flex items-center gap-4">
          <span className="text-white/60 text-sm font-bold">الترندات</span>
          <span className="text-white text-sm font-bold border-b-2 border-white pb-0.5">فيديو</span>
        </div>
        <div className="w-10" />
      </div>

      {/* Snap Scroll Container */}
      <div ref={containerRef} onScroll={handleScroll}
        className="h-full overflow-y-scroll snap-y snap-mandatory"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none', WebkitOverflowScrolling: 'touch' }}>
        {stories.map((s, i) => (
          <ReelSlide key={s.id} story={s} isActive={i === idx} onLike={toggleLike} onShare={handleShare}
            onOpenComments={() => setShowComments(true)} />
        ))}
      </div>

      {/* Comments */}
      <AnimatePresence>
        {showComments && story && (
          <CommentsSheet storyId={story.id} onClose={() => setShowComments(false)} onCommentAdded={() => {}} />
        )}
      </AnimatePresence>
    </motion.div>
  );
}

/* ==================== REEL SLIDE ==================== */
function ReelSlide({ story, isActive, onLike, onShare, onOpenComments }: {
  story: Story; isActive: boolean; onLike: () => void; onShare: () => void; onOpenComments: () => void;
}) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(false);
  const [paused, setPaused] = useState(false);

  const isEmbed = story.is_embed || story.media_type === 'embed';
  const ytId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;
  const mediaUrl = getMediaUrl(story.image_url || story.video_url);
  const isVideo = story.media_type === 'video' || story.content_type?.includes('video') ||
    (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));

  useEffect(() => {
    if (!videoRef.current) return;
    if (isActive) { videoRef.current.play().catch(() => {}); setPaused(false); }
    else { videoRef.current.pause(); videoRef.current.currentTime = 0; }
  }, [isActive]);

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (videoRef.current.paused) { videoRef.current.play(); setPaused(false); }
    else { videoRef.current.pause(); setPaused(true); }
  };

  return (
    <div className="h-screen w-full snap-start relative flex items-center justify-center bg-black">
      {/* Background */}
      {ytId ? (
        <div className="absolute inset-0">
          <iframe src={`https://www.youtube.com/embed/${ytId}?autoplay=${isActive ? 1 : 0}&rel=0&loop=1&controls=0&modestbranding=1`}
            className="w-full h-full" frameBorder={0} allow="autoplay; encrypted-media" />
        </div>
      ) : isVideo && mediaUrl ? (
        <video ref={videoRef} src={mediaUrl} className="absolute inset-0 w-full h-full object-contain"
          loop muted={muted} playsInline onClick={togglePlay} />
      ) : mediaUrl ? (
        <div className="absolute inset-0">
          <img src={mediaUrl} alt="" className="w-full h-full object-cover" />
          <div className="absolute inset-0 bg-black/20" />
        </div>
      ) : (
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-900 via-gray-900 to-black" />
      )}

      {/* Pause overlay */}
      {paused && isVideo && (
        <div className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none">
          <div className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
            <Play className="w-8 h-8 text-white fill-white" />
          </div>
        </div>
      )}

      {/* Content text */}
      {story.content && (
        <div className="absolute inset-x-0 bottom-28 px-5 z-10 pointer-events-none" dir="rtl">
          <p className="text-white text-lg font-bold leading-relaxed drop-shadow-lg text-center">{story.content}</p>
        </div>
      )}

      {/* Right Actions */}
      <div className="absolute left-3 bottom-32 flex flex-col items-center gap-5 z-20">
        <Link to={`/social-profile/${story.author_id}`} className="relative">
          <img src={getAvatarUrl(story.author_name, story.author_avatar)} alt=""
            className="w-11 h-11 rounded-full border-2 border-white shadow-lg" />
        </Link>
        <button onClick={onLike} className="flex flex-col items-center">
          <Heart className={cn("w-7 h-7 drop-shadow-lg", story.liked ? "fill-red-500 text-red-500" : "text-white")} />
          <span className="text-white text-[11px] mt-0.5 font-bold drop-shadow">{story.likes_count}</span>
        </button>
        <button onClick={onOpenComments} className="flex flex-col items-center">
          <MessageCircle className="w-7 h-7 text-white drop-shadow-lg" />
          <span className="text-white text-[11px] mt-0.5 font-bold drop-shadow">{story.comments_count}</span>
        </button>
        <button onClick={onShare} className="flex flex-col items-center">
          <Share2 className="w-7 h-7 text-white drop-shadow-lg" />
          <span className="text-white text-[11px] mt-0.5 font-bold drop-shadow">{story.shares_count || 0}</span>
        </button>
        {isVideo && (
          <button onClick={() => setMuted(!muted)}>
            {muted ? <VolumeX className="w-5 h-5 text-white/60" /> : <Volume2 className="w-5 h-5 text-white/60" />}
          </button>
        )}
      </div>

      {/* Bottom Author Info */}
      <div className="absolute bottom-5 right-4 left-16 z-20" dir="rtl">
        <div className="flex items-center gap-2 mb-1">
          <Link to={`/social-profile/${story.author_id}`} className="text-white font-bold text-sm drop-shadow-lg hover:underline">
            {story.author_name}
          </Link>
          <span className="px-2 py-0.5 bg-emerald-600 text-white text-[10px] font-bold rounded-md">متابعة</span>
        </div>
        {story.title && <p className="text-white/80 text-xs drop-shadow">{story.title}</p>}
      </div>
    </div>
  );
}

/* ==================== VIDEO GRID CARD ==================== */
function VideoGridCard({ story, onClick }: { story: Story; onClick: () => void }) {
  const isEmbed = story.is_embed || story.media_type === 'embed';
  const ytId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;
  const mediaUrl = getMediaUrl(story.image_url || story.thumbnail_url);

  return (
    <div onClick={onClick} className="relative aspect-[9/14] rounded-xl overflow-hidden cursor-pointer group bg-gray-800">
      {ytId ? (
        <img src={`https://img.youtube.com/vi/${ytId}/hqdefault.jpg`} alt="" className="w-full h-full object-cover" />
      ) : mediaUrl ? (
        <img src={mediaUrl} alt="" className="w-full h-full object-cover" loading="lazy" />
      ) : (
        <div className="w-full h-full bg-gradient-to-br from-emerald-900 to-gray-900 flex items-center justify-center">
          <Film className="w-8 h-8 text-white/20" />
        </div>
      )}
      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
      <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
        <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
          <Play className="w-6 h-6 text-white fill-white" />
        </div>
      </div>
      <div className="absolute bottom-0 left-0 right-0 p-2.5" dir="rtl">
        <p className="text-white text-xs font-bold line-clamp-2 leading-relaxed">{story.title || story.content}</p>
        <div className="flex items-center gap-2 mt-1">
          <span className="text-white/70 text-[10px]">{story.author_name}</span>
          <span className="text-white/50 text-[10px] mr-auto flex items-center gap-0.5">
            <Heart className="w-2.5 h-2.5" /> {story.likes_count || 0}
          </span>
        </div>
      </div>
    </div>
  );
}

/* ==================== STORY CARD ==================== */
function StoryCard({ story, onOpen, onToggleLike, onOpenComments, onToggleSave, onShare }: {
  story: Story; onOpen: () => void;
  onToggleLike: (e: React.MouseEvent) => void;
  onOpenComments: (e: React.MouseEvent) => void;
  onToggleSave: (e: React.MouseEvent) => void;
  onShare: (e: React.MouseEvent) => void;
}) {
  const mediaUrl = getMediaUrl(story.image_url);
  const isEmbed = story.is_embed || story.media_type === 'embed';
  const isVideo = story.media_type === 'video' || story.content_type?.includes('video') || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));
  const ytId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;

  return (
    <div className="rounded-2xl bg-gray-900 border border-gray-800/50 overflow-hidden hover:border-emerald-700/30 transition-all shadow-sm">
      {/* Media */}
      {isEmbed && story.embed_url ? (
        <div className="relative aspect-video overflow-hidden cursor-pointer" onClick={onOpen}>
          {ytId ? (
            <img src={`https://img.youtube.com/vi/${ytId}/hqdefault.jpg`} alt="" className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full bg-gray-800 flex items-center justify-center"><Film className="w-8 h-8 text-gray-600" /></div>
          )}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-14 w-14 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center">
              <Play className="h-7 w-7 text-white fill-white" />
            </div>
          </div>
          <div className="absolute top-2 right-2 bg-red-600 text-white text-[9px] px-2 py-0.5 rounded-full font-bold flex items-center gap-1">
            <Play className="h-2.5 w-2.5 fill-white" />{story.platform || 'فيديو'}
          </div>
        </div>
      ) : isVideo && mediaUrl ? (
        <div className="relative aspect-video overflow-hidden cursor-pointer" onClick={onOpen}>
          <video src={mediaUrl} className="w-full h-full object-cover" muted preload="metadata" />
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-14 w-14 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center">
              <Play className="h-7 w-7 text-white fill-white" />
            </div>
          </div>
        </div>
      ) : mediaUrl ? (
        <div className="relative h-44 overflow-hidden cursor-pointer" onClick={onOpen}>
          <img src={mediaUrl} alt="" className="w-full h-full object-cover" loading="lazy" />
        </div>
      ) : null}

      {/* Content */}
      <div className="p-4 cursor-pointer" dir="rtl" onClick={onOpen}>
        <div className="flex items-center gap-2 mb-2">
          <img src={getAvatarUrl(story.author_name, story.author_avatar)} alt="" className="h-7 w-7 rounded-full" />
          <span className="text-xs font-bold text-white truncate">{story.author_name}</span>
          <span className="text-[10px] text-gray-500 mr-auto">{timeAgo(story.created_at)}</span>
        </div>
        {story.title && <h3 className="text-[15px] font-bold text-white mb-1.5 line-clamp-2">{story.title}</h3>}
        {!isEmbed && <p className="text-[13px] text-gray-400 leading-relaxed line-clamp-3">{story.content}</p>}
      </div>

      {/* Actions */}
      <div className="flex items-center justify-between px-4 pb-3 pt-1 border-t border-gray-800/30 mx-4">
        <div className="flex items-center gap-4">
          <button onClick={onToggleLike} className="flex items-center gap-1.5 text-xs active:scale-90 transition-transform">
            <Heart className={cn("h-[18px] w-[18px]", story.liked ? "text-red-500 fill-red-500" : "text-gray-500")} />
            <span className={cn("font-bold", story.liked ? "text-red-500" : "text-gray-500")}>{story.likes_count || 0}</span>
          </button>
          <button onClick={onOpenComments} className="flex items-center gap-1.5 text-xs active:scale-90 transition-transform">
            <MessageCircle className="h-[18px] w-[18px] text-gray-500" />
            <span className="font-bold text-gray-500">{story.comments_count || 0}</span>
          </button>
          <button onClick={onShare} className="flex items-center gap-1.5 text-xs active:scale-90 transition-transform">
            <Share2 className="h-[18px] w-[18px] text-gray-500" />
          </button>
          <button onClick={onToggleSave} className="active:scale-90 transition-transform">
            <Bookmark className={cn("h-[18px] w-[18px]", story.saved ? "text-emerald-500 fill-emerald-500" : "text-gray-500")} />
          </button>
        </div>
        <span className="flex items-center gap-1 text-[10px] text-gray-600"><Eye className="h-3.5 w-3.5" />{story.views_count || 0}</span>
      </div>
    </div>
  );
}

/* ==================== RECOMMENDED USERS ==================== */
function RecommendedUsersSection() {
  const { user, getToken: gT } = useAuth();
  const [users, setUsers] = useState<RecommendedUser[]>([]);
  const [followedIds, setFollowedIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    const h: Record<string, string> = {};
    const t = getToken(); if (t) h.Authorization = `Bearer ${t}`;
    fetch(`${BACKEND_URL}/api/sohba/recommended-users?limit=6`, { headers: h })
      .then(r => r.json()).then(d => setUsers(d.users || [])).catch(() => {});
  }, []);

  const handleFollow = async (targetId: string) => {
    if (!user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/follow/${targetId}`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setFollowedIds(prev => { const n = new Set(prev); d.following ? n.add(targetId) : n.delete(targetId); return n; });
    } catch {}
  };

  if (users.length === 0) return null;

  return (
    <div className="py-4" dir="rtl">
      <h3 className="text-white text-sm font-bold mb-3 flex items-center gap-2 px-1">
        <Users className="w-4 h-4 text-emerald-500" /> مستخدمون موصى بهم
      </h3>
      <div className="flex gap-3 overflow-x-auto pb-2" style={{ scrollbarWidth: 'none' }}>
        {users.map(u => (
          <div key={u.id} className="shrink-0 w-28 flex flex-col items-center bg-gray-800/50 rounded-xl p-3 gap-2">
            <Link to={`/social-profile/${u.id}`}>
              <img src={getAvatarUrl(u.name, u.avatar)} alt="" className="w-14 h-14 rounded-full border-2 border-emerald-600" />
            </Link>
            <span className="text-white text-[11px] font-bold text-center truncate w-full">{u.name}</span>
            <button onClick={() => handleFollow(u.id)}
              className={cn("w-full py-1 rounded-lg text-[11px] font-bold",
                followedIds.has(u.id) ? 'bg-gray-700 text-gray-400' : 'bg-emerald-600 text-white')}>
              {followedIds.has(u.id) ? 'متابَع ✓' : 'متابعة'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ==================== STORY DETAIL ==================== */
function StoryDetail({ storyId, onBack, stories, onOpenViewer }: {
  storyId: string; onBack: () => void; stories: Story[]; onOpenViewer: (i: number) => void;
}) {
  const { user } = useAuth();
  const [story, setStory] = useState<Story | null>(null);
  const [loading, setLoading] = useState(true);
  const [showComments, setShowComments] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(`${BACKEND_URL}/api/stories/${storyId}`, { headers: authHeaders() })
      .then(r => r.json()).then(d => { setStory(d.story || null); setLoading(false); })
      .catch(() => setLoading(false));
  }, [storyId]);

  const toggleLike = async () => {
    if (!user || !story) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStory(s => s ? { ...s, liked: d.liked, likes_count: s.likes_count + (d.liked ? 1 : -1) } : s);
    } catch {}
  };

  const toggleSave = async () => {
    if (!user || !story) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/save`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStory(s => s ? { ...s, saved: d.saved } : s);
      toast.success(d.saved ? 'تم الحفظ' : 'تم إلغاء الحفظ');
    } catch {}
  };

  const handleShare = async () => {
    if (!story) return;
    if (navigator.share) {
      await navigator.share({ title: story.title || 'حكاياتي', text: story.content });
    } else {
      await navigator.clipboard.writeText(story.content);
      toast.success('تم نسخ المحتوى');
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-950"><Loader2 className="h-8 w-8 animate-spin text-emerald-500" /></div>;
  if (!story) return <div className="min-h-screen flex items-center justify-center bg-gray-950 text-gray-500">المحتوى غير موجود</div>;

  const isEmbed = story.is_embed || story.media_type === 'embed';
  const ytId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;
  const mediaUrl = getMediaUrl(story.image_url);
  const isVideo = story.media_type === 'video' || story.content_type?.includes('video') || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));

  return (
    <div className="min-h-screen pb-24 bg-gray-950" dir="rtl">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-gray-900/95 backdrop-blur-xl border-b border-gray-800/30">
        <div className="flex items-center justify-between px-4 h-14">
          <button onClick={onBack} className="p-2 rounded-xl bg-gray-800 active:scale-95"><ArrowRight className="h-5 w-5 text-white" /></button>
          <h2 className="text-sm font-bold text-white truncate flex-1 mx-3 text-center">التفاصيل</h2>
          <div className="flex items-center gap-1">
            {(isVideo || isEmbed) && (
              <button onClick={() => { const i = stories.findIndex(s => s.id === story.id); if (i >= 0) onOpenViewer(i); }}
                className="p-2 rounded-xl bg-gray-800"><Maximize2 className="h-4 w-4 text-gray-400" /></button>
            )}
          </div>
        </div>
      </div>

      {/* Media */}
      {ytId ? (
        <div className="w-full aspect-video bg-black">
          <iframe src={`https://www.youtube.com/embed/${ytId}?rel=0`} title={story.title} className="w-full h-full" frameBorder={0}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
        </div>
      ) : isEmbed && story.embed_url ? (
        <div className="w-full aspect-video"><iframe src={story.embed_url} className="w-full h-full" frameBorder={0} allowFullScreen /></div>
      ) : isVideo && mediaUrl ? (
        <div className="w-full aspect-video bg-black"><video src={mediaUrl} className="w-full h-full object-contain" controls autoPlay playsInline /></div>
      ) : mediaUrl ? (
        <div className="w-full max-h-72 overflow-hidden"><img src={mediaUrl} alt="" className="w-full h-72 object-cover" /></div>
      ) : null}

      {/* Content */}
      <div className="px-5 py-5">
        <div className="flex items-center gap-3 mb-4">
          <Link to={`/social-profile/${story.author_id}`}>
            <img src={getAvatarUrl(story.author_name, story.author_avatar)} alt="" className="h-10 w-10 rounded-full border-2 border-emerald-600" />
          </Link>
          <div>
            <p className="text-sm font-bold text-white">{story.author_name}</p>
            <p className="text-[10px] text-gray-500">{timeAgo(story.created_at)}</p>
          </div>
        </div>
        {story.title && <h1 className="text-xl font-bold text-white mb-4">{story.title}</h1>}
        <p className="text-[15px] text-gray-300 leading-[2.2] whitespace-pre-wrap" style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>{story.content}</p>

        {/* Actions */}
        <div className="flex items-center gap-5 mt-6 pt-4 border-t border-gray-800/30">
          <button onClick={toggleLike} className="flex items-center gap-2 active:scale-90 transition-transform">
            <Heart className={cn("h-6 w-6", story.liked ? "text-red-500 fill-red-500" : "text-gray-500")} />
            <span className="font-bold text-white">{story.likes_count}</span>
          </button>
          <button onClick={() => setShowComments(true)} className="flex items-center gap-2 active:scale-90 transition-transform">
            <MessageCircle className="h-6 w-6 text-gray-500" /><span className="font-bold text-white">{story.comments_count}</span>
          </button>
          <button onClick={handleShare} className="active:scale-90 transition-transform">
            <Share2 className="h-6 w-6 text-gray-500" />
          </button>
          <button onClick={toggleSave} className="active:scale-90 transition-transform">
            <Bookmark className={cn("h-6 w-6", story.saved ? "text-emerald-500 fill-emerald-500" : "text-gray-500")} />
          </button>
          <span className="flex items-center gap-1.5 text-xs text-gray-600 mr-auto"><Eye className="h-4 w-4" />{story.views_count || 0}</span>
        </div>
      </div>

      <AnimatePresence>
        {showComments && <CommentsSheet storyId={story.id} onClose={() => setShowComments(false)} onCommentAdded={() => setStory(s => s ? { ...s, comments_count: s.comments_count + 1 } : s)} />}
      </AnimatePresence>
    </div>
  );
}

/* ==================== MAIN STORIES / حكاياتي PAGE ==================== */
export default function Stories() {
  const { user } = useAuth();
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

  const selectedStoryId = searchParams.get('story');

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/stories/categories`).then(r => r.json())
      .then(d => setCategories(d.categories || [])).catch(() => {});
    if (searchParams.get('create') === 'true' && user) setShowCreate(true);
  }, [searchParams, user]);

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
    const url = cat
      ? `${BACKEND_URL}/api/stories/list?category=${cat}&limit=20&page=${pageNum}`
      : `${BACKEND_URL}/api/stories/list?limit=20&page=${pageNum}`;
    try {
      const r = await fetch(url, { headers: authHeaders() });
      const d = await r.json();
      const newStories = d.stories || [];
      if (append) setStories(prev => [...prev, ...newStories]);
      else setStories(newStories);
      setHasMore(newStories.length >= 20);
    } catch {}
    setLoading(false); setLoadingMore(false);
  }, []);

  useEffect(() => {
    setPage(1); setHasMore(true);
    loadStories(selectedCategory || undefined, 1, false);
  }, [selectedCategory, loadStories]);

  const handleLoadMore = () => {
    const nextPage = page + 1; setPage(nextPage);
    loadStories(selectedCategory || undefined, nextPage, true);
  };

  const toggleLike = async (id: string) => {
    if (!user) { toast.error('سجّل دخولك'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStories(p => p.map(x => x.id === id ? { ...x, liked: d.liked, likes_count: x.likes_count + (d.liked ? 1 : -1) } : x));
    } catch {}
  };

  const toggleSave = async (id: string) => {
    if (!user) { toast.error('سجّل دخولك'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/save`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStories(p => p.map(x => x.id === id ? { ...x, saved: d.saved } : x));
      toast.success(d.saved ? 'تم الحفظ' : 'تم إلغاء الحفظ');
    } catch {}
  };

  const handleShare = async (id: string) => {
    const story = stories.find(s => s.id === id);
    if (!story) return;
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/share`, { method: 'POST', headers: authHeaders() });
    } catch {}
    if (navigator.share) {
      await navigator.share({ title: story.title || 'حكاياتي', text: story.content }).catch(() => {});
    } else {
      await navigator.clipboard.writeText(story.content);
      toast.success('تم نسخ المحتوى');
    }
  };

  // Story detail view
  if (selectedStoryId) {
    return <StoryDetail storyId={selectedStoryId} onBack={handleBackFromStory} stories={stories}
      onOpenViewer={(i) => setShowViewer(i)} />;
  }

  // Sort categories
  const sortedCats = [...categories].sort((a, b) => {
    if (a.key === 'general') return -1; if (b.key === 'general') return 1;
    if (a.key === 'embed') return -1; if (b.key === 'embed') return 1;
    return 0;
  });

  const videoStories = stories.filter(s => s.is_embed || s.media_type === 'embed' || s.media_type === 'video' || s.content_type?.includes('video'));
  const textStories = stories.filter(s => !s.is_embed && s.media_type !== 'embed' && s.media_type !== 'video' && !s.content_type?.includes('video'));
  const isVideoCategory = selectedCategory === 'embed';

  return (
    <div className="min-h-screen pb-24 bg-gray-950" dir="rtl" data-testid="stories-page">
      {/* Islamic Header */}
      <div className="sticky top-0 z-50 bg-gradient-to-b from-emerald-800 to-emerald-700 text-white">
        {/* Islamic Pattern */}
        <div className="absolute inset-0 opacity-[0.08]" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />
        <div className="absolute top-1 left-3 text-lg opacity-50 animate-pulse">🏮</div>
        <div className="absolute top-1 right-3 text-lg opacity-50 animate-pulse" style={{ animationDelay: '1s' }}>🏮</div>

        {/* Main Header */}
        <div className="relative flex items-center justify-between px-4 pt-3 pb-2">
          <Link to="/explore" className="p-2 rounded-full hover:bg-white/10 transition-colors">
            <Search className="w-5 h-5" />
          </Link>
          <div className="flex items-center gap-5">
            <button onClick={() => setActiveTab('video')}
              className={cn("text-base font-bold transition-all pb-1", activeTab === 'video' ? 'text-white border-b-2 border-white' : 'text-white/50')}>
              فيديو
            </button>
            <button onClick={() => setActiveTab('trending')}
              className={cn("text-base font-bold transition-all pb-1", activeTab === 'trending' ? 'text-white border-b-2 border-white' : 'text-white/50')}>
              الترندات
            </button>
            <h1 className="text-lg font-black flex items-center gap-1.5">
              <BookOpen className="w-5 h-5" /> حكاياتي
            </h1>
          </div>
          {user ? (
            <button onClick={() => setShowCreate(true)} className="p-2 rounded-full hover:bg-white/10">
              <Plus className="w-5 h-5" />
            </button>
          ) : <div className="w-9" />}
        </div>

        {/* Category Tabs */}
        {activeTab === 'trending' && (
          <div className="relative flex gap-1.5 px-3 pb-3 overflow-x-auto" style={{ scrollbarWidth: 'none' }}>
            <button onClick={() => handleSelectCategory(null)}
              className={cn('shrink-0 px-4 py-1.5 rounded-full text-xs font-bold transition-all',
                !selectedCategory ? 'bg-white text-emerald-800' : 'text-white/70 hover:bg-white/10')}>
              الكل
            </button>
            {sortedCats.map(cat => (
              <button key={cat.key} onClick={() => handleSelectCategory(cat.key)}
                className={cn('shrink-0 flex items-center gap-1 px-3.5 py-1.5 rounded-full text-xs font-bold transition-all',
                  selectedCategory === cat.key ? 'bg-white text-emerald-800' : 'text-white/70 hover:bg-white/10')}>
                <span className="text-sm">{cat.emoji}</span>{cat.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Content */}
      <div className="px-3 py-3">
        {activeTab === 'video' ? (
          /* === VIDEO TAB - Full screen viewer === */
          videoStories.length === 0 ? (
            <div className="text-center py-16">
              <Film className="w-12 h-12 text-gray-700 mx-auto mb-3" />
              <p className="text-gray-600 text-sm">لا توجد فيديوهات بعد</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-2">
              {videoStories.map((s, idx) => (
                <VideoGridCard key={s.id} story={s} onClick={() => setShowViewer(idx)} />
              ))}
            </div>
          )
        ) : (
          /* === TRENDING TAB === */
          <>
            {loading ? (
              <div className="flex justify-center py-16"><Loader2 className="h-8 w-8 animate-spin text-emerald-500" /></div>
            ) : stories.length === 0 ? (
              <div className="text-center py-10">
                <BookOpen className="h-14 w-14 text-gray-700 mx-auto mb-3" />
                <p className="text-gray-500 text-sm mb-4">لا يوجد محتوى حتى الآن، تابع بعض المستخدمين!</p>
                <RecommendedUsersSection />
                {user && <button onClick={() => setShowCreate(true)}
                  className="mt-4 bg-emerald-600 text-white px-8 py-3 rounded-2xl text-sm font-bold active:scale-95">أنشئ محتوى ✨</button>}
              </div>
            ) : (
              <>
                {/* Recommended Users */}
                <RecommendedUsersSection />

                {/* Video Grid (if not in video-only category) */}
                {!isVideoCategory && videoStories.length > 0 && (
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <h2 className="text-sm font-bold text-white flex items-center gap-2">
                        <Film className="h-4 w-4 text-emerald-500" /> فيديوهات
                      </h2>
                      <button onClick={() => setActiveTab('video')} className="text-xs text-emerald-400 font-bold">عرض الكل</button>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      {videoStories.slice(0, 4).map((s, idx) => (
                        <VideoGridCard key={s.id} story={s} onClick={() => setShowViewer(idx)} />
                      ))}
                    </div>
                  </div>
                )}

                {/* Text/Image Stories */}
                {(isVideoCategory ? videoStories : textStories).length > 0 && (
                  <div className="space-y-3">
                    {(isVideoCategory ? videoStories : textStories).map(s => (
                      <StoryCard key={s.id} story={s}
                        onOpen={() => handleOpenStory(s.id)}
                        onToggleLike={e => { e.stopPropagation(); toggleLike(s.id); }}
                        onOpenComments={e => { e.stopPropagation(); setShowCommentsFor(s.id); }}
                        onToggleSave={e => { e.stopPropagation(); toggleSave(s.id); }}
                        onShare={e => { e.stopPropagation(); handleShare(s.id); }}
                      />
                    ))}
                  </div>
                )}

                {/* Load More */}
                {hasMore && stories.length >= 20 && (
                  <div className="flex justify-center mt-6">
                    <button onClick={handleLoadMore} disabled={loadingMore}
                      className="flex items-center gap-2 px-8 py-3 rounded-2xl bg-gray-800 border border-emerald-700/30 text-emerald-400 text-sm font-bold active:scale-95 disabled:opacity-50">
                      {loadingMore ? <><Loader2 className="h-4 w-4 animate-spin" /> جاري التحميل...</> : <>المزيد</>}
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
        {showCreate && <CreateStorySheet categories={categories} onClose={() => setShowCreate(false)} onCreated={s => { setStories(prev => [s, ...prev]); }} />}
        {showCommentsFor && <CommentsSheet storyId={showCommentsFor} onClose={() => setShowCommentsFor(null)} onCommentAdded={() => setStories(p => p.map(x => x.id === showCommentsFor ? { ...x, comments_count: x.comments_count + 1 } : x))} />}
        {showViewer !== null && <FullscreenViewer stories={videoStories} initialIndex={showViewer} onClose={() => setShowViewer(null)} />}
      </AnimatePresence>
    </div>
  );
}
