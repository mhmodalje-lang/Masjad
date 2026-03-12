import { useState, useEffect, useCallback } from 'react';
import { Users, Search, Heart, MessageCircle, Plus, Send, X, Loader2, Play, Image, Video } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Category { key: string; label: string; }
interface Post {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  content: string; category: string; image_url?: string; media_type?: string;
  created_at: string; likes_count: number; comments_count: number;
  shares_count: number; liked: boolean; saved: boolean;
}
interface Comment {
  id: string; author_name: string; author_avatar?: string; content: string; created_at: string;
}

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders() { return { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` }; }

function timeAgo(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const m = Math.floor(diff / 60000);
  if (m < 1) return 'الآن';
  if (m < 60) return `${m}د`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}س`;
  const d = Math.floor(h / 24);
  if (d < 7) return `${d}ي`;
  return `${Math.floor(d / 7)}أ`;
}

const avatarColors = ['bg-emerald-600', 'bg-blue-600', 'bg-amber-600', 'bg-purple-600', 'bg-rose-600', 'bg-teal-600', 'bg-cyan-600', 'bg-orange-600'];

// Sample media for visual posts (placeholders to make the feed look rich)
const sampleMedia = [
  { url: 'https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?w=400&q=60', type: 'image' },
  { url: 'https://images.unsplash.com/photo-1564769625905-50e93615e769?w=400&q=60', type: 'image' },
  { url: 'https://images.unsplash.com/photo-1519817650390-64a93db51149?w=400&q=60', type: 'image' },
  { url: 'https://images.unsplash.com/photo-1542816417-0983c9c9ad53?w=400&q=60', type: 'video' },
  { url: 'https://images.unsplash.com/photo-1585036156171-384164a8c596?w=400&q=60', type: 'image' },
  { url: 'https://images.unsplash.com/photo-1466442929976-97f336a657be?w=400&q=60', type: 'image' },
];

// Grid Card Component
function GridCard({ post, onLike, onOpenDetail, index }: { post: Post; onLike: () => void; onOpenDetail: () => void; index: number }) {
  const ci = (post.author_name || '').charCodeAt(0) % avatarColors.length;
  const media = post.image_url || sampleMedia[index % sampleMedia.length]?.url;
  const isVideo = post.media_type === 'video' || sampleMedia[index % sampleMedia.length]?.type === 'video';
  const shortContent = post.content.length > 80 ? post.content.slice(0, 80) + '...' : post.content;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.05 }}
      className="break-inside-avoid mb-3"
      data-testid={`grid-post-${post.id}`}
    >
      <div onClick={onOpenDetail} className="rounded-2xl overflow-hidden bg-card border border-border/20 shadow-sm active:scale-[0.98] transition-transform cursor-pointer">
        {/* Media */}
        <div className="relative aspect-[3/4] bg-muted overflow-hidden">
          <img src={media} alt="" className="w-full h-full object-cover" loading="lazy" />
          {isVideo && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/20">
              <div className="h-12 w-12 rounded-full bg-white/90 flex items-center justify-center shadow-lg">
                <Play className="h-5 w-5 text-foreground fill-current ms-0.5" />
              </div>
            </div>
          )}
          {/* Like overlay */}
          <button
            onClick={(e) => { e.stopPropagation(); onLike(); }}
            className="absolute top-2 left-2 p-1.5 rounded-full bg-black/30 backdrop-blur-sm"
          >
            <Heart className={cn('h-4 w-4', post.liked ? 'text-red-400 fill-current' : 'text-white')} />
          </button>
        </div>

        {/* Content */}
        <div className="p-2.5">
          <p className="text-xs text-foreground leading-relaxed line-clamp-3 font-arabic mb-2">{shortContent}</p>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <div className={cn('h-5 w-5 rounded-full flex items-center justify-center text-[8px] text-white font-bold', avatarColors[ci])}>
                {post.author_avatar ? <img src={post.author_avatar} className="h-full w-full rounded-full object-cover" /> : (post.author_name?.[0] || '؟')}
              </div>
              <span className="text-[10px] text-muted-foreground truncate max-w-[70px]">{post.author_name}</span>
            </div>
            <div className="flex items-center gap-1">
              <Heart className={cn('h-3 w-3', post.liked ? 'text-red-500 fill-current' : 'text-muted-foreground')} />
              <span className="text-[10px] text-muted-foreground">{post.likes_count || ''}</span>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

// Post Detail Modal
function PostDetail({ post, onClose, onLike, onSave }: { post: Post; onClose: () => void; onLike: () => void; onSave: () => void }) {
  const ci = (post.author_name || '').charCodeAt(0) % avatarColors.length;
  const [comments, setComments] = useState<Comment[]>([]);
  const [commentText, setCommentText] = useState('');
  const [sending, setSending] = useState(false);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`).then(r => r.json()).then(d => setComments(d.comments || [])).catch(() => {});
  }, [post.id]);

  const sendComment = async () => {
    if (!commentText.trim()) return;
    setSending(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ content: commentText.trim() }) });
      if (r.status === 401) { toast.error('سجّل دخولك أولاً'); setSending(false); return; }
      const d = await r.json();
      if (d.comment) { setComments(prev => [...prev, d.comment]); setCommentText(''); }
    } catch { toast.error('حدث خطأ'); }
    setSending(false);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-[999] bg-black/70 backdrop-blur-sm flex flex-col" dir="rtl">
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-lg mx-auto bg-card min-h-full">
          {/* Header */}
          <div className="sticky top-0 z-10 flex items-center justify-between p-3 bg-card/95 backdrop-blur-xl border-b border-border/20">
            <button onClick={onClose} className="p-2 rounded-full bg-muted/50"><X className="h-5 w-5 text-foreground" /></button>
            <div className="flex items-center gap-2">
              <div className={cn('h-8 w-8 rounded-full flex items-center justify-center text-xs text-white font-bold', avatarColors[ci])}>
                {post.author_avatar ? <img src={post.author_avatar} className="h-full w-full rounded-full object-cover" /> : (post.author_name?.[0] || '؟')}
              </div>
              <div>
                <p className="text-xs font-bold text-foreground">{post.author_name}</p>
                <p className="text-[9px] text-muted-foreground">{timeAgo(post.created_at)}</p>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="p-4">
            <p className="text-sm text-foreground leading-relaxed whitespace-pre-line font-arabic">{post.content}</p>
            {post.image_url && <img src={post.image_url} alt="" className="w-full rounded-2xl mt-3" />}
          </div>

          {/* Actions */}
          <div className="flex items-center justify-around py-3 border-y border-border/20 px-4">
            <button onClick={onLike} className={cn('flex items-center gap-1.5 text-sm', post.liked ? 'text-red-500' : 'text-muted-foreground')}>
              <Heart className={cn('h-5 w-5', post.liked && 'fill-current')} />
              <span>{post.likes_count}</span>
            </button>
            <span className="flex items-center gap-1.5 text-sm text-muted-foreground">
              <MessageCircle className="h-5 w-5" />
              <span>{comments.length}</span>
            </span>
            <button onClick={onSave} className={cn('text-sm', post.saved ? 'text-primary' : 'text-muted-foreground')}>
              {post.saved ? 'محفوظ' : 'حفظ'}
            </button>
          </div>

          {/* Comments */}
          <div className="p-4 space-y-3">
            {comments.length === 0 && <p className="text-center text-xs text-muted-foreground py-4">لا توجد تعليقات — كن أول من يعلّق</p>}
            {comments.map(c => (
              <div key={c.id} className="flex gap-2">
                <div className={cn('h-7 w-7 rounded-full flex items-center justify-center text-[9px] text-white font-bold shrink-0', avatarColors[(c.author_name||'').charCodeAt(0) % avatarColors.length])}>
                  {c.author_name?.[0] || '؟'}
                </div>
                <div className="bg-muted/40 rounded-2xl px-3 py-2 flex-1">
                  <p className="text-[10px] font-bold text-foreground">{c.author_name}</p>
                  <p className="text-xs text-foreground/80">{c.content}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Comment input fixed at bottom */}
      <div className="bg-card border-t border-border/20 p-3 flex gap-2 max-w-lg mx-auto w-full">
        <input value={commentText} onChange={e => setCommentText(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendComment()}
          placeholder="اكتب تعليقاً..." className="flex-1 bg-muted/50 rounded-2xl px-4 py-2.5 text-sm outline-none" data-testid="comment-input" />
        <button onClick={sendComment} disabled={!commentText.trim() || sending} className="h-10 w-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center shrink-0 disabled:opacity-40" data-testid="send-comment-btn">
          {sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
        </button>
      </div>
    </motion.div>
  );
}

// Create Post Sheet
function CreatePostSheet({ categories, onClose, onCreated }: { categories: Category[]; onClose: () => void; onCreated: (p: Post) => void }) {
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('general');
  const [posting, setPosting] = useState(false);

  const submit = async () => {
    if (!content.trim()) { toast.error('اكتب شيئاً أولاً'); return; }
    setPosting(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ content: content.trim(), category }) });
      if (r.status === 401) { toast.error('سجّل دخولك أولاً'); setPosting(false); return; }
      const d = await r.json();
      if (d.post) { onCreated(d.post); toast.success('تم نشر منشورك'); onClose(); }
    } catch { toast.error('حدث خطأ في النشر'); }
    setPosting(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }} className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[80vh] flex flex-col border-t border-border/30">
        <div className="flex items-center justify-between p-4 border-b border-border/20">
          <button onClick={onClose} className="text-sm text-muted-foreground">إلغاء</button>
          <h3 className="text-sm font-bold text-foreground">منشور جديد</h3>
          <button onClick={submit} disabled={!content.trim() || posting} className="text-sm font-bold text-primary disabled:opacity-40" data-testid="submit-post-btn">
            {posting ? <Loader2 className="h-4 w-4 animate-spin" /> : 'نشر'}
          </button>
        </div>
        <div className="p-4 flex-1 overflow-y-auto">
          <textarea value={content} onChange={e => setContent(e.target.value)} placeholder="شارك فكرة، آية، حديث، أو دعاء..."
            className="w-full h-32 bg-transparent resize-none outline-none text-sm text-foreground placeholder:text-muted-foreground leading-relaxed" autoFocus data-testid="post-content-input" />
          
          {/* Media buttons */}
          <div className="flex gap-2 mt-2 mb-4">
            <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-muted/50 text-xs text-muted-foreground">
              <Image className="h-3.5 w-3.5" /> صورة
            </button>
            <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-muted/50 text-xs text-muted-foreground">
              <Video className="h-3.5 w-3.5" /> فيديو
            </button>
          </div>

          <p className="text-xs font-bold text-muted-foreground mb-2">اختر الفئة:</p>
          <div className="flex flex-wrap gap-2">
            {categories.map(c => (
              <button key={c.key} onClick={() => setCategory(c.key)} data-testid={`cat-${c.key}`}
                className={cn('px-3 py-1.5 rounded-full text-xs font-medium transition-all', category === c.key ? 'bg-primary text-primary-foreground' : 'bg-muted/50 text-muted-foreground')}>
                {c.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

// Main Sohba Page
export default function Sohba() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('all');
  const [posts, setPosts] = useState<Post[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [detailPost, setDetailPost] = useState<Post | null>(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/categories`).then(r => r.json()).then(d => setCategories(d.categories || [])).catch(() => {});
  }, []);

  const loadPosts = useCallback(async (cat: string, pg: number, append = false) => {
    setLoading(true);
    try {
      const headers: Record<string, string> = {};
      const token = getToken();
      if (token) headers['Authorization'] = `Bearer ${token}`;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts?category=${cat}&page=${pg}&limit=20`, { headers });
      const d = await r.json();
      if (append) setPosts(prev => [...prev, ...(d.posts || [])]);
      else setPosts(d.posts || []);
      setHasMore(d.has_more || false);
    } catch {}
    setLoading(false);
  }, []);

  useEffect(() => { setPage(1); loadPosts(activeTab, 1); }, [activeTab, loadPosts]);

  const toggleLike = async (postId: string) => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      const update = (p: Post) => p.id === postId ? { ...p, liked: d.liked, likes_count: p.likes_count + (d.liked ? 1 : -1) } : p;
      setPosts(prev => prev.map(update));
      if (detailPost?.id === postId) setDetailPost(prev => prev ? update(prev) : null);
    } catch {}
  };

  const toggleSave = async (postId: string) => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/save`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      const update = (p: Post) => p.id === postId ? { ...p, saved: d.saved } : p;
      setPosts(prev => prev.map(update));
      if (detailPost?.id === postId) setDetailPost(prev => prev ? update(prev) : null);
    } catch {}
  };

  const allTabs = [{ key: 'all', label: 'الكل' }, ...categories];

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="sohba-page">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-card/95 backdrop-blur-xl border-b border-border/15">
        <div className="flex items-center justify-between px-4 py-3 pt-safe-header">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-primary" />
            <h1 className="text-lg font-bold text-foreground">صُحبة</h1>
          </div>
          <button className="p-2 rounded-xl bg-muted/50"><Search className="h-4 w-4 text-muted-foreground" /></button>
        </div>

        {/* Category tabs */}
        <div className="flex gap-1 px-3 pb-2.5 overflow-x-auto no-scrollbar">
          {allTabs.map(tab => (
            <button key={tab.key} onClick={() => setActiveTab(tab.key)} data-testid={`sohba-tab-${tab.key}`}
              className={cn('shrink-0 px-3 py-1.5 rounded-full text-[11px] font-bold transition-all',
                activeTab === tab.key ? 'bg-primary text-primary-foreground shadow-sm' : 'bg-muted/40 text-muted-foreground')}>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      {loading && posts.length === 0 ? (
        <div className="flex items-center justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>
      ) : posts.length === 0 ? (
        <div className="p-10 text-center">
          <Users className="h-14 w-14 text-muted-foreground/15 mx-auto mb-3" />
          <p className="text-base font-bold text-muted-foreground">لا توجد منشورات بعد</p>
          <p className="text-xs text-muted-foreground/50 mt-1">كن أول من ينشر!</p>
          {user && (
            <button onClick={() => setShowCreate(true)} className="mt-4 bg-primary text-primary-foreground px-6 py-2.5 rounded-2xl text-sm font-bold active:scale-95 transition-transform">
              أنشئ منشوراً
            </button>
          )}
        </div>
      ) : (
        <div className="px-2.5 pt-3">
          {/* 2-Column Masonry Grid */}
          <div className="columns-2 gap-2.5">
            {posts.map((post, i) => (
              <GridCard key={post.id} post={post} index={i} onLike={() => toggleLike(post.id)} onOpenDetail={() => setDetailPost(post)} />
            ))}
          </div>
          {hasMore && (
            <button onClick={() => { const np = page + 1; setPage(np); loadPosts(activeTab, np, true); }} className="w-full py-4 text-sm text-primary font-bold">
              تحميل المزيد
            </button>
          )}
        </div>
      )}

      {/* Create FAB */}
      <button data-testid="create-post-btn"
        onClick={() => { if (!user) { toast.error('سجّل دخولك أولاً'); navigate('/auth'); return; } setShowCreate(true); }}
        className="fixed bottom-20 left-5 z-40 h-14 w-14 rounded-full bg-primary text-primary-foreground shadow-lg shadow-primary/25 flex items-center justify-center active:scale-90 transition-transform">
        <Plus className="h-6 w-6" />
      </button>

      {/* Sheets */}
      <AnimatePresence>
        {showCreate && <CreatePostSheet categories={categories} onClose={() => setShowCreate(false)} onCreated={p => setPosts(prev => [p, ...prev])} />}
        {detailPost && <PostDetail post={detailPost} onClose={() => setDetailPost(null)} onLike={() => toggleLike(detailPost.id)} onSave={() => toggleSave(detailPost.id)} />}
      </AnimatePresence>
    </div>
  );
}
