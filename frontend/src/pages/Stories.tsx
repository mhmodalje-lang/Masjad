import { useState, useEffect, useCallback, useRef } from 'react';
import { Heart, MessageCircle, Send, X, Loader2, Image, Video, BookOpen, Plus, Eye, ArrowRight, Sparkles, Shield, Star, Moon, Coins, ChevronLeft, Share2, Bookmark, FileText, Film, Play, Maximize2, Volume2, VolumeX } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
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
  media_type?: string; created_at: string; likes_count: number;
  comments_count: number; views_count?: number; liked: boolean; saved: boolean;
  embed_url?: string; platform?: string; is_embed?: boolean;
}
interface Comment { id: string; author_name: string; author_avatar?: string; content: string; created_at: string; }
interface Category { key: string; label: string; emoji: string; icon: string; color: string; }

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
  const m = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]+)/);
  return m ? m[1] : null;
}

/* ========== FULLSCREEN VIDEO VIEWER ========== */
function FullscreenViewer({ stories, initialIndex, onClose }: { stories: Story[]; initialIndex: number; onClose: () => void }) {
  const [idx, setIdx] = useState(initialIndex);
  const { user } = useAuth();
  const navigate = useNavigate();
  const touchY = useRef(0);
  const [story, setStory] = useState(stories[idx]);
  const [showComments, setShowComments] = useState(false);
  
  useEffect(() => {
    setStory(stories[idx]);
  }, [idx, stories]);
  
  const goNext = () => { 
    if (idx < stories.length - 1) {
      setIdx(i => i + 1);
    }
  };
  
  const goPrev = () => { 
    if (idx > 0) {
      setIdx(i => i - 1);
    }
  };

  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = ''; };
  }, []);
  
  // Keyboard navigation
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowUp') goPrev();
      if (e.key === 'ArrowDown') goNext();
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [idx, stories.length]);

  const toggleLike = async () => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStory(s => ({ ...s, liked: d.liked, likes_count: s.likes_count + (d.liked ? 1 : -1) }));
    } catch {}
  };

  const toggleSave = async () => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/save`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStory(s => ({ ...s, saved: d.saved }));
      toast.success(d.saved ? 'تم الحفظ' : 'تم إلغاء الحفظ');
    } catch {}
  };
  
  const handleShare = async () => {
    const url = `${window.location.origin}/stories?story=${story.id}`;
    if (navigator.share) {
      try {
        await navigator.share({ title: story.title || 'قصة', text: story.content.substring(0, 100), url });
        toast.success('تمت المشاركة');
      } catch {}
    } else {
      navigator.clipboard?.writeText(url);
      toast.success('تم نسخ الرابط');
    }
  };
  
  const handleRepost = async () => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    // TODO: Implement repost functionality
    toast.success('سيتم إضافة ميزة إعادة النشر قريباً');
  };

  if (!story) return null;
  const isEmbed = story.is_embed || story.media_type === 'embed';
  const embedYtId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;
  const mediaUrl = getMediaUrl(story.image_url);
  const isVideo = story.media_type === 'video' || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));

  return (
    <>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        className="fixed inset-0 z-[1000] bg-black flex flex-col" dir="rtl"
        onTouchStart={e => { touchY.current = e.touches[0].clientY; }}
        onTouchEnd={e => {
          const dy = e.changedTouches[0].clientY - touchY.current;
          if (Math.abs(dy) > 100) { dy < 0 ? goNext() : goPrev(); }
        }}>
        {/* Top Bar */}
        <div className="absolute top-0 left-0 right-0 z-50 flex items-center justify-between px-4 py-4 bg-gradient-to-b from-black/80 via-black/40 to-transparent">
          <button onClick={onClose} className="p-2.5 rounded-full bg-white/20 backdrop-blur-sm active:scale-90"><X className="h-6 w-6 text-white" /></button>
          <span className="text-base text-white/80 font-bold">{idx + 1} / {stories.length}</span>
        </div>
        
        {/* Video Content */}
        <div className="flex-1 flex items-center justify-center">
          {embedYtId ? (
            <iframe src={`https://www.youtube.com/embed/${embedYtId}?autoplay=1&rel=0`} title={story.title}
              className="w-full h-full" frameBorder={0}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
          ) : isEmbed && story.embed_url ? (
            <iframe src={story.embed_url} title={story.title} className="w-full h-full" frameBorder={0}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
          ) : isVideo && mediaUrl ? (
            <video src={mediaUrl} className="w-full h-full object-contain" controls autoPlay playsInline loop />
          ) : mediaUrl ? (
            <img src={mediaUrl} alt="" className="w-full h-full object-contain" />
          ) : (
            <div className="px-8 text-center max-w-lg">
              {story.title && <h2 className="text-2xl font-bold text-white mb-6">{story.title}</h2>}
              <p className="text-base text-white/90 leading-[2.2] whitespace-pre-wrap" style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>{story.content}</p>
            </div>
          )}
        </div>
        
        {/* Bottom Info & Actions */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/95 via-black/60 to-transparent px-5 pb-8 pt-20">
          <div className="flex items-end gap-4">
            {/* Author Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-2">
                <div className={cn('h-10 w-10 rounded-full flex items-center justify-center text-sm text-white font-bold', avatarColors[(story.author_name||'').charCodeAt(0)%6])}>{story.author_name?.[0]}</div>
                <span className="text-base font-bold text-white">{story.author_name}</span>
              </div>
              {story.title && <p className="text-base font-bold text-white line-clamp-2 mb-1">{story.title}</p>}
              <p className="text-sm text-white/70 line-clamp-2">{story.content.substring(0, 100)}...</p>
            </div>
            
            {/* Action Buttons */}
            <div className="flex flex-col items-center gap-6 pb-2">
              {/* Like */}
              <button onClick={toggleLike} className="active:scale-90 transition-transform flex flex-col items-center gap-1">
                <div className="h-12 w-12 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
                  <Heart className={cn("h-7 w-7", story.liked ? "text-red-500 fill-red-500" : "text-white")} />
                </div>
                <span className="text-xs text-white font-bold">{story.likes_count||0}</span>
              </button>
              
              {/* Comments */}
              <button onClick={() => setShowComments(true)} className="active:scale-90 transition-transform flex flex-col items-center gap-1">
                <div className="h-12 w-12 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
                  <MessageCircle className="h-7 w-7 text-white" />
                </div>
                <span className="text-xs text-white font-bold">{story.comments_count||0}</span>
              </button>
              
              {/* Save */}
              <button onClick={toggleSave} className="active:scale-90 transition-transform flex flex-col items-center gap-1">
                <div className="h-12 w-12 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
                  <Bookmark className={cn("h-6 w-6", story.saved ? "text-primary fill-primary" : "text-white")} />
                </div>
              </button>
              
              {/* Share */}
              <button onClick={handleShare} className="active:scale-90 transition-transform flex flex-col items-center gap-1">
                <div className="h-12 w-12 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
                  <Share2 className="h-6 w-6 text-white" />
                </div>
              </button>
            </div>
          </div>
        </div>
        
        {/* Navigation Arrows */}
        {idx > 0 && (
          <button onClick={goPrev} 
            className="absolute top-1/2 right-4 -translate-y-1/2 p-3 rounded-full bg-black/40 backdrop-blur-sm border border-white/20 active:scale-90">
            <ChevronLeft className="h-6 w-6 text-white rotate-180" />
          </button>
        )}
        {idx < stories.length - 1 && (
          <button onClick={goNext} 
            className="absolute top-1/2 left-4 -translate-y-1/2 p-3 rounded-full bg-black/40 backdrop-blur-sm border border-white/20 active:scale-90">
            <ChevronLeft className="h-6 w-6 text-white" />
          </button>
        )}
        
        {/* Swipe Indicator */}
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 pointer-events-none">
          <motion.div 
            initial={{ opacity: 0, y: 0 }}
            animate={{ opacity: [0.5, 0], y: [0, 30] }}
            transition={{ duration: 1.5, repeat: 3, repeatDelay: 2 }}
            className="flex flex-col items-center gap-2">
            <ChevronLeft className="h-8 w-8 text-white/50 -rotate-90" />
            <span className="text-xs text-white/50">اسحب للأعلى/الأسفل</span>
          </motion.div>
        </div>
      </motion.div>
      
      {/* Comments Sheet */}
      <AnimatePresence>
        {showComments && <CommentsSheet storyId={story.id} onClose={() => setShowComments(false)} onCommentAdded={() => setStory(s => ({ ...s, comments_count: s.comments_count + 1 }))} />}
      </AnimatePresence>
    </>
  );
}

/* ========== COMMENTS SHEET ========== */
function CommentsSheet({ storyId, onClose, onCommentAdded }: { storyId: string; onClose: () => void; onCommentAdded?: () => void }) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/posts/${storyId}/comments`)
      .then(r => r.json()).then(d => { setComments(d.comments || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [storyId]);
  const send = async () => {
    if (!text.trim()) return;
    setSending(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${storyId}/comments`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ content: text.trim() }) });
      if (r.status === 401) { toast.error('سجّل دخولك'); setSending(false); return; }
      const d = await r.json();
      if (d.comment) { setComments(p => [...p, d.comment]); setText(''); onCommentAdded?.(); }
    } catch { toast.error('خطأ'); }
    setSending(false);
  };
  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="fixed inset-0 z-[1001] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[70vh] flex flex-col border-t border-primary/20">
        <div className="flex justify-center pt-2 pb-1"><div className="w-10 h-1 rounded-full bg-muted-foreground/30" /></div>
        <div className="flex items-center justify-between px-5 py-2 border-b border-border/20">
          <span className="text-sm font-bold">{comments.length} تعليق</span>
          <button onClick={onClose} className="p-1.5 rounded-full hover:bg-muted/50"><X className="h-5 w-5 text-muted-foreground" /></button>
        </div>
        <div className="flex-1 overflow-y-auto px-5 py-3 space-y-4 min-h-[120px]">
          {loading ? <div className="flex justify-center py-8"><Loader2 className="h-5 w-5 animate-spin text-muted-foreground" /></div>
            : comments.length === 0 ? <p className="text-center text-xs text-muted-foreground py-10">لا توجد تعليقات</p>
            : comments.map(c => (
              <div key={c.id} className="flex gap-2.5">
                <div className={cn('h-8 w-8 rounded-full flex items-center justify-center text-[10px] text-white font-bold shrink-0', avatarColors[(c.author_name||'').charCodeAt(0)%6])}>{c.author_name?.[0]}</div>
                <div><span className="text-xs font-bold text-foreground">{c.author_name}</span><span className="text-[10px] text-muted-foreground mr-2">{timeAgo(c.created_at)}</span><p className="text-[13px] text-foreground/85 mt-0.5">{c.content}</p></div>
              </div>
            ))}
        </div>
        <div className="px-4 py-3 border-t border-border/20 flex gap-2 bg-card">
          <input value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} dir="auto" placeholder="تعليق..."
            className="flex-1 bg-muted/50 rounded-2xl px-4 py-2.5 text-sm outline-none text-foreground" />
          <button onClick={send} disabled={!text.trim() || sending}
            className="h-10 w-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center disabled:opacity-40">
            {sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </button>
        </div>
      </div>
    </motion.div>
  );
}

/* ========== CREATE STORY SHEET ========== */
function CreateStorySheet({ categories, onClose, onCreated }: { categories: Category[]; onClose: () => void; onCreated: (s: Story) => void }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('general');
  const [mediaType, setMediaType] = useState('text');
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [posting, setPosting] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const userCategories = categories.filter(c => c.key !== 'embed');

  const handleFile = async (file: File) => {
    setUploading(true);
    const isVid = file.type.startsWith('video/');
    setMediaType(isVid ? 'video' : 'image');
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch(`${BACKEND_URL}/api/upload/multipart`, { method: 'POST', headers: authHeadersMultipart(), body: formData });
      const data = await res.json();
      if (res.ok && data.url) { setImagePreview(`${BACKEND_URL}${data.url}`); toast.success('تم الرفع'); }
      else toast.error('فشل الرفع');
    } catch { toast.error('خطأ'); }
    setUploading(false);
  };

  const autoCategorize = async () => {
    if (!title.trim() && !content.trim()) return;
    setAiLoading(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/stories/auto-categorize`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ title, content }) });
      const d = await r.json();
      if (d.category) { setCategory(d.category); toast.success('تم التصنيف بالذكاء الاصطناعي ✨'); }
    } catch {}
    setAiLoading(false);
  };

  const submit = async () => {
    if (!title.trim() || !content.trim()) { toast.error('اكتب العنوان والقصة'); return; }
    setPosting(true);
    let uploadedUrl = '';
    if (imagePreview?.includes('/api/uploads/')) uploadedUrl = imagePreview.replace(BACKEND_URL, '');
    try {
      const body: any = { title: title.trim(), content: content.trim(), category, media_type: mediaType };
      if (uploadedUrl) body.image_url = uploadedUrl;
      const r = await fetch(`${BACKEND_URL}/api/stories/create`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(body) });
      const d = await r.json();
      if (d.story) { onCreated(d.story); toast.success('تم النشر! ✨'); onClose(); }
    } catch { toast.error('خطأ'); }
    setPosting(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/60" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[90vh] flex flex-col border-t border-primary/20">
        <div className="flex items-center justify-between p-4 border-b border-border/20">
          <button onClick={onClose} className="text-sm text-muted-foreground">إلغاء</button>
          <h3 className="text-sm font-bold">قصة جديدة ✨</h3>
          <button onClick={submit} disabled={!title.trim() || !content.trim() || posting}
            className="text-sm font-bold text-primary disabled:opacity-40">
            {posting ? <Loader2 className="h-4 w-4 animate-spin" /> : 'نشر'}
          </button>
        </div>
        <div className="p-4 flex-1 overflow-y-auto space-y-4">
          <input value={title} onChange={e => setTitle(e.target.value)} dir="auto" placeholder="عنوان القصة..." maxLength={200}
            className="w-full bg-muted/40 rounded-xl px-4 py-3 text-base font-bold outline-none text-foreground border border-border/30 focus:border-primary/40" />
          <textarea value={content} onChange={e => setContent(e.target.value)} dir="auto" placeholder="اكتب قصتك هنا..."
            className="w-full h-36 bg-muted/40 rounded-xl px-4 py-3 text-sm leading-relaxed resize-none outline-none text-foreground border border-border/30 focus:border-primary/40" maxLength={5000} />
          {imagePreview && (
            <div className="relative rounded-xl overflow-hidden">
              {mediaType === 'video' ? <video src={imagePreview} className="w-full max-h-48 object-cover rounded-xl" controls />
                : <img src={imagePreview} alt="" className="w-full max-h-48 object-cover rounded-xl" />}
              <button onClick={() => setImagePreview(null)} className="absolute top-2 left-2 p-1.5 rounded-full bg-black/60 text-white"><X className="h-3.5 w-3.5" /></button>
            </div>
          )}
          {uploading && <div className="flex items-center gap-2"><Loader2 className="h-4 w-4 animate-spin text-primary" /><span className="text-xs text-muted-foreground">جاري الرفع...</span></div>}
          <div className="flex gap-2">
            <input ref={fileRef} type="file" accept="image/*,video/*" className="hidden" onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
            <button onClick={() => fileRef.current?.click()}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-muted/50 text-xs text-muted-foreground border border-border/20"><Image className="h-4 w-4" /> صورة</button>
            <button onClick={() => { fileRef.current?.setAttribute('accept', 'video/*'); fileRef.current?.click(); }}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-muted/50 text-xs text-muted-foreground border border-border/20"><Video className="h-4 w-4" /> فيديو</button>
          </div>
          <div>
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs font-bold text-muted-foreground">القسم:</p>
              <button onClick={autoCategorize} disabled={aiLoading || (!title.trim() && !content.trim())}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-primary/10 text-primary text-[10px] font-bold disabled:opacity-40 active:scale-95">
                {aiLoading ? <Loader2 className="h-3 w-3 animate-spin" /> : <Sparkles className="h-3 w-3" />} تصنيف ذكي
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {userCategories.map(c => (
                <button key={c.key} onClick={() => setCategory(c.key)}
                  className={cn('px-3 py-2 rounded-full text-xs font-bold flex items-center gap-1',
                    category === c.key ? 'bg-primary text-primary-foreground' : 'bg-muted/50 text-muted-foreground border border-border/20')}>
                  <span>{c.emoji}</span>{c.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

/* ========== VIDEO GRID CARD (2-column layout) ========== */
function VideoGridCard({ story, onClick }: { story: Story; onClick: () => void }) {
  const isEmbed = story.is_embed || story.media_type === 'embed';
  const ytId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;
  const mediaUrl = getMediaUrl(story.image_url);

  return (
    <div onClick={onClick} className="rounded-2xl overflow-hidden bg-card border border-border/30 cursor-pointer active:scale-[0.97] transition-transform group">
      <div className="relative aspect-[4/3] bg-black/20">
        {ytId ? (
          <img src={`https://img.youtube.com/vi/${ytId}/hqdefault.jpg`} alt="" className="w-full h-full object-cover" loading="lazy" />
        ) : mediaUrl ? (
          <img src={mediaUrl} alt="" className="w-full h-full object-cover" loading="lazy"
            onError={(e) => { (e.target as HTMLImageElement).src = ''; }} />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center">
            <Film className="h-8 w-8 text-primary/30" />
          </div>
        )}
        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-all flex items-center justify-center">
          <div className="h-10 w-10 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center opacity-80 group-hover:opacity-100 transition-opacity">
            <Play className="h-5 w-5 text-white fill-white" />
          </div>
        </div>
        {(isEmbed && story.platform) && (
          <div className="absolute top-1.5 right-1.5 bg-red-600/90 text-white text-[8px] px-1.5 py-0.5 rounded-full font-bold">
            {story.platform}
          </div>
        )}
        <div className="absolute bottom-1.5 left-1.5 flex items-center gap-1 bg-black/50 rounded-full px-1.5 py-0.5">
          <Eye className="h-2.5 w-2.5 text-white/80" />
          <span className="text-[9px] text-white/80">{story.views_count || 0}</span>
        </div>
      </div>
      <div className="p-2.5">
        <p className="text-[11px] font-bold text-foreground line-clamp-2 leading-relaxed" dir="rtl">{story.title || story.content}</p>
        <div className="flex items-center justify-between mt-1.5">
          <span className="text-[9px] text-muted-foreground truncate">{story.author_name}</span>
          <div className="flex items-center gap-2">
            <span className="flex items-center gap-0.5 text-[9px] text-muted-foreground"><Heart className="h-2.5 w-2.5" />{story.likes_count||0}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ========== STORY CARD (for text stories) ========== */
function StoryCard({ story, onOpen, onToggleLike, onOpenComments, onToggleSave }: {
  story: Story; onOpen: () => void;
  onToggleLike: (e: React.MouseEvent) => void;
  onOpenComments: (e: React.MouseEvent) => void;
  onToggleSave: (e: React.MouseEvent) => void;
}) {
  const mediaUrl = getMediaUrl(story.image_url);
  const isEmbed = story.is_embed || story.media_type === 'embed';
  const isVideo = story.media_type === 'video' || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));
  const ytId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;
  const ci = (story.author_name||'').charCodeAt(0)%6;

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-card border border-border/40 overflow-hidden hover:border-primary/30 transition-all shadow-sm">
      {isEmbed && story.embed_url ? (
        <div className="relative aspect-video overflow-hidden cursor-pointer" onClick={onOpen}>
          {ytId ? (
            <img src={`https://img.youtube.com/vi/${ytId}/hqdefault.jpg`} alt="" className="w-full h-full object-cover" />
          ) : (
            <iframe src={story.embed_url} title={story.title} className="w-full h-full pointer-events-none" frameBorder={0} />
          )}
          <div className="absolute inset-0 bg-transparent" />
          <div className="absolute top-2 right-2 bg-red-600 text-white text-[9px] px-2 py-0.5 rounded-full font-bold flex items-center gap-1">
            <Play className="h-2.5 w-2.5 fill-white" />{story.platform || 'فيديو'}
          </div>
          <div className="absolute bottom-2 left-2 p-2 rounded-full bg-black/50 backdrop-blur-sm">
            <Maximize2 className="h-4 w-4 text-white" />
          </div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-14 w-14 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center">
              <Play className="h-7 w-7 text-white fill-white" />
            </div>
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
      <div className="p-4 cursor-pointer" dir="rtl" onClick={onOpen}>
        <div className="flex items-center gap-2 mb-2">
          <div className={cn('h-7 w-7 rounded-full flex items-center justify-center text-[10px] text-white font-bold shrink-0', avatarColors[ci])}>{story.author_name?.[0]}</div>
          <span className="text-xs font-bold text-foreground truncate">{story.author_name}</span>
          <span className="text-[10px] text-muted-foreground mr-auto">{timeAgo(story.created_at)}</span>
        </div>
        {story.title && <h3 className="text-[15px] font-bold text-foreground mb-1.5 line-clamp-2">{story.title}</h3>}
        {!isEmbed && <p className="text-[13px] text-muted-foreground leading-relaxed line-clamp-3">{story.content}</p>}
      </div>
      <div className="flex items-center justify-between px-4 pb-3 pt-1 border-t border-border/15 mx-4">
        <div className="flex items-center gap-4">
          <button onClick={onToggleLike} className="flex items-center gap-1.5 text-xs active:scale-90 transition-transform">
            <Heart className={cn("h-[18px] w-[18px]", story.liked ? "text-red-500 fill-red-500" : "text-muted-foreground")} />
            <span className={cn("font-bold", story.liked ? "text-red-500" : "text-muted-foreground")}>{story.likes_count||0}</span>
          </button>
          <button onClick={onOpenComments} className="flex items-center gap-1.5 text-xs active:scale-90 transition-transform">
            <MessageCircle className="h-[18px] w-[18px] text-muted-foreground" /><span className="font-bold text-muted-foreground">{story.comments_count||0}</span>
          </button>
          <button onClick={onToggleSave} className="active:scale-90 transition-transform">
            <Bookmark className={cn("h-[18px] w-[18px]", story.saved ? "text-primary fill-primary" : "text-muted-foreground")} />
          </button>
        </div>
        <span className="flex items-center gap-1 text-[10px] text-muted-foreground"><Eye className="h-3.5 w-3.5" />{story.views_count||0}</span>
      </div>
    </motion.div>
  );
}

/* ========== STORY DETAIL ========== */
function StoryDetail({ storyId, onBack, stories, onOpenViewer }: { storyId: string; onBack: () => void; stories: Story[]; onOpenViewer: (i: number) => void }) {
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

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>;
  if (!story) return <div className="min-h-screen flex items-center justify-center text-muted-foreground">القصة غير موجودة</div>;

  const isEmbed = story.is_embed || story.media_type === 'embed';
  const ytId = isEmbed && story.embed_url ? getYouTubeId(story.embed_url) : null;
  const mediaUrl = getMediaUrl(story.image_url);
  const isVideo = story.media_type === 'video' || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl">
      <div className="sticky top-0 z-40 bg-card/95 backdrop-blur-xl border-b border-border/20">
        <div className="flex items-center justify-between px-4 h-14">
          <button onClick={onBack} className="p-2 rounded-xl bg-muted/50 active:scale-95"><ArrowRight className="h-5 w-5 text-foreground" /></button>
          <h2 className="text-sm font-bold text-foreground truncate flex-1 mx-3 text-center">القصة</h2>
          <div className="flex items-center gap-1">
            {(isVideo || isEmbed) && (
              <button onClick={() => { const i = stories.findIndex(s => s.id === story.id); if (i >= 0) onOpenViewer(i); }}
                className="p-2 rounded-xl bg-muted/50"><Maximize2 className="h-4 w-4 text-muted-foreground" /></button>
            )}
          </div>
        </div>
      </div>
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
      <div className="px-5 py-5">
        <div className="flex items-center gap-3 mb-4">
          <div className={cn('h-10 w-10 rounded-full flex items-center justify-center text-sm text-white font-bold', avatarColors[(story.author_name||'').charCodeAt(0)%6])}>{story.author_name?.[0]}</div>
          <div><p className="text-sm font-bold text-foreground">{story.author_name}</p><p className="text-[10px] text-muted-foreground">{timeAgo(story.created_at)}</p></div>
        </div>
        {story.title && <h1 className="text-xl font-bold text-foreground mb-4">{story.title}</h1>}
        <p className="text-[15px] text-foreground leading-[2.2] whitespace-pre-wrap" style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>{story.content}</p>
        <div className="flex items-center gap-5 mt-6 pt-4 border-t border-border/20">
          <button onClick={toggleLike} className="flex items-center gap-2 active:scale-90 transition-transform">
            <Heart className={cn("h-6 w-6", story.liked ? "text-red-500 fill-red-500" : "text-muted-foreground")} />
            <span className="font-bold text-foreground">{story.likes_count}</span>
          </button>
          <button onClick={() => setShowComments(true)} className="flex items-center gap-2 active:scale-90 transition-transform">
            <MessageCircle className="h-6 w-6 text-muted-foreground" /><span className="font-bold text-foreground">{story.comments_count}</span>
          </button>
          <button onClick={toggleSave} className="active:scale-90 transition-transform">
            <Bookmark className={cn("h-6 w-6", story.saved ? "text-primary fill-primary" : "text-muted-foreground")} />
          </button>
          <span className="flex items-center gap-1.5 text-xs text-muted-foreground mr-auto"><Eye className="h-4 w-4" />{story.views_count||0}</span>
        </div>
      </div>
      <AnimatePresence>
        {showComments && <CommentsSheet storyId={story.id} onClose={() => setShowComments(false)} onCommentAdded={() => setStory(s => s ? { ...s, comments_count: s.comments_count + 1 } : s)} />}
      </AnimatePresence>
    </div>
  );
}

/* ========== MAIN STORIES PAGE ========== */
export default function Stories() {
  const { user } = useAuth();
  const [searchParams] = useSearchParams();
  const [categories, setCategories] = useState<Category[]>([]);
  const [stories, setStories] = useState<Story[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedStoryId, setSelectedStoryId] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [showCommentsFor, setShowCommentsFor] = useState<string | null>(null);
  const [showViewer, setShowViewer] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/stories/categories`).then(r => r.json())
      .then(d => setCategories(d.categories || [])).catch(() => {});
    if (searchParams.get('create') === 'true' && user) setShowCreate(true);
    const sp = searchParams.get('story');
    if (sp) setSelectedStoryId(sp);
  }, [searchParams, user]);

  const loadStories = useCallback(async (cat?: string) => {
    setLoading(true);
    const url = cat ? `${BACKEND_URL}/api/stories/list?category=${cat}&limit=50` : `${BACKEND_URL}/api/stories/list?limit=50`;
    try {
      const r = await fetch(url, { headers: authHeaders() });
      const d = await r.json();
      setStories(d.stories || []);
    } catch {}
    setLoading(false);
  }, []);

  useEffect(() => { loadStories(selectedCategory || undefined); }, [selectedCategory, loadStories]);

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

  if (selectedStoryId) {
    return <StoryDetail storyId={selectedStoryId} onBack={() => setSelectedStoryId(null)} stories={stories} onOpenViewer={(i) => setShowViewer(i)} />;
  }

  // Sort categories: general first, embed second
  const sortedCats = [...categories].sort((a, b) => {
    if (a.key === 'general') return -1; if (b.key === 'general') return 1;
    if (a.key === 'embed') return -1; if (b.key === 'embed') return 1;
    return 0;
  });

  // Separate video stories for grid display
  const videoStories = stories.filter(s => s.is_embed || s.media_type === 'embed' || s.media_type === 'video');
  const textStories = stories.filter(s => !s.is_embed && s.media_type !== 'embed' && s.media_type !== 'video');
  const isVideoCategory = selectedCategory === 'embed';

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="stories-page">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20">
        <div className="px-4 pt-3 pb-2 flex items-center justify-between">
          <h1 className="text-xl font-black text-foreground flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-primary" /> حكايات
          </h1>
          {user && (
            <button onClick={() => setShowCreate(true)}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-primary text-primary-foreground text-xs font-bold shadow-md shadow-primary/20 active:scale-95">
              <Plus className="h-3.5 w-3.5" /> جديدة
            </button>
          )}
        </div>
        <div className="px-3 pb-3 flex gap-2 overflow-x-auto no-scrollbar">
          <button onClick={() => setSelectedCategory(null)}
            className={cn('px-3.5 py-2 rounded-full text-xs font-bold shrink-0 border transition-all',
              !selectedCategory ? 'bg-primary text-primary-foreground border-primary' : 'bg-card text-muted-foreground border-border/30')}>
            الكل
          </button>
          {sortedCats.map(cat => (
            <button key={cat.key} onClick={() => setSelectedCategory(cat.key)}
              className={cn('flex items-center gap-1.5 px-3.5 py-2 rounded-full text-xs font-bold shrink-0 border transition-all',
                selectedCategory === cat.key ? 'bg-primary text-primary-foreground border-primary' : 'bg-card text-muted-foreground border-border/30')}>
              <span className="text-sm">{cat.emoji}</span>{cat.label}
            </button>
          ))}
        </div>
      </div>

      <div className="px-4 py-4">
        {loading ? (
          <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>
        ) : stories.length === 0 ? (
          <div className="text-center py-20">
            <BookOpen className="h-16 w-16 text-muted-foreground/15 mx-auto mb-4" />
            <p className="text-base font-bold text-muted-foreground/50">لا توجد قصص</p>
            {user && <button onClick={() => setShowCreate(true)} className="mt-5 bg-primary text-primary-foreground px-8 py-3 rounded-2xl text-sm font-bold active:scale-95 shadow-md">أنشئ قصة ✨</button>}
          </div>
        ) : (
          <>
            {/* Video Grid Section */}
            {(isVideoCategory || (!selectedCategory && videoStories.length > 0)) && videoStories.length > 0 && (
              <div className="mb-6">
                {!isVideoCategory && (
                  <div className="flex items-center justify-between mb-3">
                    <h2 className="text-[15px] font-bold text-foreground flex items-center gap-2">
                      <Film className="h-4 w-4 text-primary" /> فيديوهات
                    </h2>
                    <button onClick={() => setSelectedCategory('embed')} className="text-xs text-primary font-bold">عرض الكل</button>
                  </div>
                )}
                <div className="grid grid-cols-2 gap-2.5">
                  {(isVideoCategory ? videoStories : videoStories.slice(0, 6)).map((s, idx) => {
                    const vidIdx = videoStories.findIndex(v => v.id === s.id);
                    return (
                      <VideoGridCard key={s.id} story={s} onClick={() => setShowViewer(vidIdx >= 0 ? vidIdx : 0)} />
                    );
                  })}
                </div>
              </div>
            )}

            {/* Ad between sections */}
            {!isVideoCategory && <AdBanner position="home" />}

            {/* Text Stories (cards) */}
            {!isVideoCategory && textStories.length > 0 && (
              <div className="space-y-4">
                {textStories.map((s, idx) => (
                  <div key={s.id}>
                    <StoryCard story={s} onOpen={() => setSelectedStoryId(s.id)}
                      onToggleLike={e => { e.stopPropagation(); toggleLike(s.id); }}
                      onOpenComments={e => { e.stopPropagation(); setShowCommentsFor(s.id); }}
                      onToggleSave={e => { e.stopPropagation(); toggleSave(s.id); }} />
                    {idx === 2 && <AdBanner position="home" />}
                  </div>
                ))}
              </div>
            )}

            {/* Video category - show all as grid only */}
            {isVideoCategory && videoStories.length === 0 && (
              <div className="text-center py-12">
                <Film className="h-12 w-12 text-muted-foreground/20 mx-auto mb-3" />
                <p className="text-sm text-muted-foreground/50">لا توجد فيديوهات</p>
              </div>
            )}
          </>
        )}
      </div>

      <AnimatePresence>
        {showCreate && <CreateStorySheet categories={categories} onClose={() => setShowCreate(false)} onCreated={s => setStories(prev => [s, ...prev])} />}
        {showCommentsFor && <CommentsSheet storyId={showCommentsFor} onClose={() => setShowCommentsFor(null)} onCommentAdded={() => setStories(p => p.map(x => x.id === showCommentsFor ? { ...x, comments_count: x.comments_count + 1 } : x))} />}
        {showViewer !== null && <FullscreenViewer stories={videoStories} initialIndex={showViewer} onClose={() => setShowViewer(null)} />}
      </AnimatePresence>
    </div>
  );
}
