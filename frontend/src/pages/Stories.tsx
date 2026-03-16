import { useState, useEffect, useCallback, useRef } from 'react';
import { Heart, MessageCircle, Send, X, Loader2, Image, Video, BookOpen, Plus, Eye, ArrowRight, Sparkles, Shield, Star, Moon, Coins, ChevronLeft, Share2, Bookmark } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

interface Story {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  title?: string; content: string; category: string; image_url?: string;
  media_type?: string; created_at: string; likes_count: number;
  comments_count: number; views_count?: number; liked: boolean; saved: boolean;
}

interface Comment {
  id: string; author_name: string; author_avatar?: string; content: string; created_at: string;
}

interface Category {
  key: string; label: string; emoji: string; icon: string; color: string;
}

const avatarColors = ['bg-emerald-600', 'bg-blue-600', 'bg-amber-600', 'bg-purple-600', 'bg-rose-600', 'bg-teal-600'];

function timeAgo(iso: string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return 'الآن';
  if (m < 60) return `منذ ${m} دقيقة`;
  const h = Math.floor(m / 60);
  if (h < 24) return `منذ ${h} ساعة`;
  const days = Math.floor(h / 24);
  if (days < 30) return `منذ ${days} يوم`;
  return `منذ ${Math.floor(days / 30)} شهر`;
}

const catIcons: Record<string, any> = {
  istighfar: Sparkles, sahaba: BookOpen, quran: BookOpen, prophets: Star,
  ruqyah: Shield, rizq: Coins, tawba: Heart, miracles: Moon,
};

/* ========== COMMENTS SHEET ========== */
function CommentsSheet({ storyId, onClose }: { storyId: string; onClose: () => void }) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`${BACKEND_URL}/api/sohba/posts/${storyId}/comments`)
      .then(r => r.json()).then(d => { setComments(d.comments || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [storyId]);

  const send = async () => {
    if (!text.trim()) return;
    setSending(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${storyId}/comments`, {
        method: 'POST', headers: authHeaders(), body: JSON.stringify({ content: text.trim() })
      });
      if (r.status === 401) { toast.error('سجّل دخولك أولاً'); setSending(false); return; }
      const d = await r.json();
      if (d.comment) { setComments(p => [...p, d.comment]); setText(''); }
    } catch { toast.error('خطأ في إرسال التعليق'); }
    setSending(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[70vh] flex flex-col shadow-2xl border-t border-border/30">
        <div className="flex justify-center pt-2 pb-1"><div className="w-10 h-1 rounded-full bg-muted-foreground/30" /></div>
        <div className="flex items-center justify-between px-5 py-2 border-b border-border/20">
          <span className="text-sm font-bold">{comments.length} تعليق</span>
          <button onClick={onClose} className="p-1.5 rounded-full hover:bg-muted/50"><X className="h-5 w-5 text-muted-foreground" /></button>
        </div>
        <div className="flex-1 overflow-y-auto px-5 py-3 space-y-4 min-h-[120px]">
          {loading ? (
            <div className="flex justify-center py-8"><Loader2 className="h-5 w-5 animate-spin text-muted-foreground" /></div>
          ) : comments.length === 0 ? (
            <p className="text-center text-xs text-muted-foreground py-10">لا توجد تعليقات بعد<br />كن أول من يعلّق!</p>
          ) : (
            comments.map(c => {
              const ci = (c.author_name || '').charCodeAt(0) % avatarColors.length;
              return (
                <div key={c.id} className="flex gap-2.5">
                  <div className={cn('h-8 w-8 rounded-full flex items-center justify-center text-[10px] text-white font-bold shrink-0', avatarColors[ci])}>
                    {c.author_avatar ? <img src={c.author_avatar} className="h-full w-full rounded-full object-cover" alt="" /> : c.author_name?.[0]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-[12px] font-bold text-foreground">{c.author_name}</span>
                      <span className="text-[10px] text-muted-foreground">{timeAgo(c.created_at)}</span>
                    </div>
                    <p className="text-[13px] text-foreground/85 mt-0.5 leading-relaxed" dir="auto">{c.content}</p>
                  </div>
                </div>
              );
            })
          )}
        </div>
        <div className="px-4 py-3 border-t border-border/20 flex gap-2 bg-card">
          <input value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()}
            dir="auto" placeholder="اكتب تعليقاً..."
            className="flex-1 bg-muted/50 rounded-2xl px-4 py-2.5 text-sm outline-none text-foreground placeholder:text-muted-foreground" />
          <button onClick={send} disabled={!text.trim() || sending}
            className="h-10 w-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center shrink-0 disabled:opacity-40">
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
  const [category, setCategory] = useState(categories[0]?.key || 'istighfar');
  const [mediaType, setMediaType] = useState('text');
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [posting, setPosting] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const maxChars = 5000;

  const handleFile = async (file: File) => {
    if (file.size < 5 * 1024 * 1024) {
      const reader = new FileReader();
      reader.onload = () => setImagePreview(reader.result as string);
      reader.readAsDataURL(file);
    } else {
      const formData = new FormData(); formData.append('file', file);
      try {
        const res = await fetch(`${BACKEND_URL}/api/upload/multipart`, { method: 'POST', body: formData });
        const data = await res.json();
        if (res.ok && data.url) setImagePreview(`${BACKEND_URL}${data.url}`);
        else toast.error('فشل رفع الملف');
      } catch { toast.error('خطأ في الرفع'); }
    }
  };

  const submit = async () => {
    if (!title.trim() || !content.trim()) { toast.error('يرجى كتابة العنوان والقصة'); return; }
    setPosting(true);
    let uploadedUrl = '';
    if (imagePreview) {
      if (imagePreview.startsWith('data:')) {
        try {
          const r = await fetch(`${BACKEND_URL}/api/upload/file`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ data: imagePreview, filename: 'story.jpg' }) });
          const d = await r.json(); if (r.ok) uploadedUrl = d.url;
        } catch {}
      } else if (imagePreview.includes('/api/uploads/')) {
        uploadedUrl = imagePreview.replace(BACKEND_URL, '');
      }
    }
    try {
      const body: any = { title: title.trim(), content: content.trim(), category, media_type: mediaType };
      if (uploadedUrl) body.image_url = uploadedUrl;
      const r = await fetch(`${BACKEND_URL}/api/stories/create`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(body) });
      if (r.status === 401) { toast.error('سجّل دخولك أولاً'); setPosting(false); return; }
      const d = await r.json();
      if (d.story) { onCreated(d.story); toast.success('تم نشر قصتك بنجاح! ✨'); onClose(); }
    } catch { toast.error('خطأ في النشر'); }
    setPosting(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/60" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[90vh] flex flex-col border-t border-border/30">
        <div className="flex items-center justify-between p-4 border-b border-border/20">
          <button onClick={onClose} className="text-sm text-muted-foreground font-medium">إلغاء</button>
          <h3 className="text-sm font-bold">قصة جديدة ✨</h3>
          <button onClick={submit} disabled={!title.trim() || !content.trim() || posting}
            className="text-sm font-bold text-primary disabled:opacity-40">
            {posting ? <Loader2 className="h-4 w-4 animate-spin" /> : 'نشر'}
          </button>
        </div>
        <div className="p-4 flex-1 overflow-y-auto space-y-4">
          <div>
            <input value={title} onChange={e => setTitle(e.target.value)} dir="auto" placeholder="عنوان القصة..."
              className="w-full bg-muted/40 rounded-xl px-4 py-3 text-base font-bold outline-none text-foreground placeholder:text-muted-foreground border border-border/30 focus:border-primary/40" maxLength={200} />
          </div>
          <div>
            <textarea value={content} onChange={e => setContent(e.target.value)} dir="auto"
              placeholder="اكتب قصتك هنا... شارك تجربتك الإيمانية"
              className="w-full h-36 bg-muted/40 rounded-xl px-4 py-3 text-sm leading-relaxed resize-none outline-none text-foreground placeholder:text-muted-foreground border border-border/30 focus:border-primary/40"
              maxLength={maxChars} />
            <p className="text-[10px] text-muted-foreground mt-1 text-left">{content.length}/{maxChars}</p>
          </div>

          {imagePreview && (
            <div className="relative rounded-xl overflow-hidden">
              <img src={imagePreview} alt="" className="w-full max-h-48 object-cover rounded-xl" />
              <button onClick={() => setImagePreview(null)} className="absolute top-2 left-2 p-1.5 rounded-full bg-black/60 text-white">
                <X className="h-3.5 w-3.5" />
              </button>
            </div>
          )}

          <div className="flex gap-2">
            <input ref={fileRef} type="file" accept="image/*,video/*" className="hidden" onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
            <button onClick={() => { setMediaType('image'); fileRef.current?.click(); }}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-muted/50 text-xs text-muted-foreground hover:bg-primary/10 hover:text-primary transition-colors border border-border/20">
              <Image className="h-4 w-4" /> صورة
            </button>
            <button onClick={() => { setMediaType('video'); fileRef.current?.click(); }}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-muted/50 text-xs text-muted-foreground hover:bg-primary/10 hover:text-primary transition-colors border border-border/20">
              <Video className="h-4 w-4" /> فيديو
            </button>
          </div>

          <div>
            <p className="text-xs font-bold text-muted-foreground mb-2">القسم:</p>
            <div className="flex flex-wrap gap-2">
              {categories.map((c) => (
                <button key={c.key} onClick={() => setCategory(c.key)}
                  className={cn('px-3.5 py-2 rounded-full text-xs font-bold transition-all flex items-center gap-1.5',
                    category === c.key ? 'bg-primary text-primary-foreground shadow-md' : 'bg-muted/50 text-muted-foreground border border-border/20')}>
                  <span>{c.emoji}</span> {c.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

/* ========== STORY CARD ========== */
function StoryCard({ story, onOpen, onLike }: { story: Story; onOpen: () => void; onLike: () => void }) {
  const ci = (story.author_name || '').charCodeAt(0) % avatarColors.length;
  const rawUrl = story.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('http') ? rawUrl : `${BACKEND_URL}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`) : null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-card border border-border/40 overflow-hidden hover:border-primary/30 transition-all cursor-pointer shadow-sm hover:shadow-md"
      onClick={onOpen}
    >
      {mediaUrl && (
        <div className="relative h-40 overflow-hidden">
          <img src={mediaUrl} alt="" className="w-full h-full object-cover" loading="lazy" />
          <div className="absolute inset-0" style={{ background: 'linear-gradient(to top, rgba(0,0,0,.5), transparent)' }} />
        </div>
      )}
      <div className="p-4" dir="rtl">
        <div className="flex items-center gap-2 mb-2">
          <div className={cn('h-7 w-7 rounded-full flex items-center justify-center text-[10px] text-white font-bold shrink-0', avatarColors[ci])}>
            {story.author_avatar ? <img src={story.author_avatar} className="h-full w-full rounded-full object-cover" alt="" /> : (story.author_name?.[0] || '؟')}
          </div>
          <span className="text-xs font-bold text-foreground truncate">{story.author_name}</span>
          <span className="text-[10px] text-muted-foreground mr-auto">{timeAgo(story.created_at)}</span>
        </div>
        {story.title && <h3 className="text-sm font-bold text-foreground mb-1.5 line-clamp-2">{story.title}</h3>}
        <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">{story.content}</p>
        <div className="flex items-center justify-between mt-3 pt-2.5 border-t border-border/20">
          <div className="flex items-center gap-3">
            <button onClick={e => { e.stopPropagation(); onLike(); }} className="flex items-center gap-1 text-xs">
              <Heart className={cn("h-3.5 w-3.5", story.liked ? "text-red-500 fill-red-500" : "text-muted-foreground")} />
              <span className="text-muted-foreground">{story.likes_count || 0}</span>
            </button>
            <span className="flex items-center gap-1 text-xs text-muted-foreground">
              <MessageCircle className="h-3.5 w-3.5" />{story.comments_count || 0}
            </span>
          </div>
          <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
            <Eye className="h-3 w-3" />{story.views_count || 0}
          </span>
        </div>
      </div>
    </motion.div>
  );
}

/* ========== STORY DETAIL VIEW ========== */
function StoryDetail({ story: initialStory, onBack, onLike }: { story: Story; onBack: () => void; onLike: (id: string) => void }) {
  const [story, setStory] = useState(initialStory);
  const [showComments, setShowComments] = useState(false);
  const rawUrl = story.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('http') ? rawUrl : `${BACKEND_URL}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`) : null;
  const ci = (story.author_name || '').charCodeAt(0) % avatarColors.length;

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/stories/${story.id}/view`, { method: 'POST' }).catch(() => {});
  }, [story.id]);

  return (
    <div className="min-h-screen pb-24" dir="rtl">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-card/95 backdrop-blur-xl border-b border-border/20">
        <div className="flex items-center justify-between px-4 h-14">
          <button onClick={onBack} className="p-2 rounded-xl bg-muted/50 active:scale-95">
            <ArrowRight className="h-5 w-5 text-foreground" />
          </button>
          <h2 className="text-sm font-bold text-foreground truncate flex-1 mx-3 text-center">القصة</h2>
          <button onClick={() => {
            navigator.clipboard?.writeText(`${window.location.origin}/stories?story=${story.id}`);
            toast.success('تم نسخ الرابط');
          }} className="p-2 rounded-xl bg-muted/50"><Share2 className="h-4 w-4 text-muted-foreground" /></button>
        </div>
      </div>

      {mediaUrl && (
        <div className="w-full max-h-72 overflow-hidden">
          <img src={mediaUrl} alt="" className="w-full h-72 object-cover" />
        </div>
      )}

      <div className="px-5 py-5">
        <div className="flex items-center gap-3 mb-4">
          <Link to={`/profile/${story.author_id}`}>
            <div className={cn('h-10 w-10 rounded-full flex items-center justify-center text-sm text-white font-bold', avatarColors[ci])}>
              {story.author_avatar ? <img src={story.author_avatar} className="h-full w-full rounded-full object-cover" alt="" /> : (story.author_name?.[0] || '؟')}
            </div>
          </Link>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold text-foreground">{story.author_name}</p>
            <p className="text-[10px] text-muted-foreground">{timeAgo(story.created_at)}</p>
          </div>
        </div>

        {story.title && <h1 className="text-xl font-bold text-foreground mb-4 leading-relaxed">{story.title}</h1>}
        <p className="text-sm text-foreground leading-[2.2] whitespace-pre-wrap" style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>{story.content}</p>

        <div className="flex items-center gap-4 mt-6 pt-4 border-t border-border/20">
          <button onClick={() => onLike(story.id)} className="flex items-center gap-1.5 text-sm">
            <Heart className={cn("h-5 w-5 transition-all", story.liked ? "text-red-500 fill-red-500" : "text-muted-foreground")} />
            <span className="font-bold text-foreground">{story.likes_count}</span>
          </button>
          <button onClick={() => setShowComments(true)} className="flex items-center gap-1.5 text-sm">
            <MessageCircle className="h-5 w-5 text-muted-foreground" />
            <span className="font-bold text-foreground">{story.comments_count}</span>
          </button>
          <span className="flex items-center gap-1.5 text-xs text-muted-foreground mr-auto">
            <Eye className="h-4 w-4" />{(story.views_count || 0)} مشاهدة
          </span>
        </div>
      </div>

      <AnimatePresence>
        {showComments && <CommentsSheet storyId={story.id} onClose={() => setShowComments(false)} />}
      </AnimatePresence>
    </div>
  );
}

/* ========== MAIN STORIES PAGE ========== */
export default function Stories() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [categories, setCategories] = useState<Category[]>([]);
  const [stories, setStories] = useState<Story[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedStory, setSelectedStory] = useState<Story | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/stories/categories`).then(r => r.json())
      .then(d => setCategories(d.categories || [])).catch(() => {});
    const shouldCreate = searchParams.get('create');
    if (shouldCreate === 'true' && user) setShowCreate(true);
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

  useEffect(() => {
    if (selectedCategory) loadStories(selectedCategory);
    else loadStories();
  }, [selectedCategory, loadStories]);

  const toggleLike = async (id: string) => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStories(p => p.map(x => x.id === id ? { ...x, liked: d.liked, likes_count: x.likes_count + (d.liked ? 1 : -1) } : x));
      if (selectedStory?.id === id) {
        setSelectedStory(s => s ? { ...s, liked: d.liked, likes_count: s.likes_count + (d.liked ? 1 : -1) } : s);
      }
    } catch {}
  };

  if (selectedStory) {
    return <StoryDetail story={selectedStory} onBack={() => setSelectedStory(null)} onLike={toggleLike} />;
  }

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="stories-page">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20">
        <div className="px-4 pt-3 pb-2 flex items-center justify-between">
          <h1 className="text-xl font-black text-foreground flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-primary" />
            حكايات
          </h1>
          {user && (
            <button onClick={() => setShowCreate(true)}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-primary text-primary-foreground text-xs font-bold shadow-md shadow-primary/20 active:scale-95">
              <Plus className="h-3.5 w-3.5" /> قصة جديدة
            </button>
          )}
        </div>

        {/* Category tabs */}
        <div className="px-3 pb-3 flex gap-2 overflow-x-auto no-scrollbar">
          <button
            onClick={() => setSelectedCategory(null)}
            className={cn('px-3.5 py-2 rounded-full text-xs font-bold transition-all shrink-0 border',
              !selectedCategory ? 'bg-primary text-primary-foreground border-primary' : 'bg-card text-muted-foreground border-border/30')}
          >الكل</button>
          {categories.map(cat => {
            const Icon = catIcons[cat.key] || BookOpen;
            return (
              <button key={cat.key} onClick={() => setSelectedCategory(cat.key)}
                className={cn('flex items-center gap-1.5 px-3.5 py-2 rounded-full text-xs font-bold transition-all shrink-0 border',
                  selectedCategory === cat.key ? 'bg-primary text-primary-foreground border-primary' : 'bg-card text-muted-foreground border-border/30')}>
                <span className="text-sm">{cat.emoji}</span> {cat.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Stories Grid */}
      <div className="px-4 py-4">
        {loading ? (
          <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>
        ) : stories.length === 0 ? (
          <div className="text-center py-20 px-8">
            <BookOpen className="h-16 w-16 text-muted-foreground/15 mx-auto mb-4" />
            <p className="text-base font-bold text-muted-foreground/50">لا توجد قصص بعد</p>
            <p className="text-xs text-muted-foreground/30 mt-1">كن أول من يشارك قصته!</p>
            {user && (
              <button onClick={() => setShowCreate(true)}
                className="mt-5 bg-primary text-primary-foreground px-8 py-3 rounded-2xl text-sm font-bold active:scale-95 transition-transform shadow-md">
                أنشئ أول قصة ✨
              </button>
            )}
            {!user && (
              <Link to="/auth" className="mt-5 inline-block bg-primary text-primary-foreground px-8 py-3 rounded-2xl text-sm font-bold">
                سجّل دخولك للنشر
              </Link>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {stories.map(s => (
              <StoryCard key={s.id} story={s} onOpen={() => setSelectedStory(s)} onLike={() => toggleLike(s.id)} />
            ))}
          </div>
        )}
      </div>

      {/* Create Sheet */}
      <AnimatePresence>
        {showCreate && <CreateStorySheet categories={categories} onClose={() => setShowCreate(false)} onCreated={s => setStories(prev => [s, ...prev])} />}
      </AnimatePresence>
    </div>
  );
}
