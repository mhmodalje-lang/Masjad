import { useState, useEffect, useCallback } from 'react';
import { Users, TrendingUp, Search, Heart, MessageCircle, Share2, Bookmark, Plus, Send, X, ChevronLeft, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Category { key: string; label: string; }
interface Post {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  content: string; category: string; image_url?: string; created_at: string;
  likes_count: number; comments_count: number; shares_count: number;
  liked: boolean; saved: boolean;
}
interface Comment {
  id: string; author_name: string; author_avatar?: string; content: string; created_at: string;
}

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders() { return { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` }; }

function timeAgo(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'الآن';
  if (mins < 60) return `منذ ${mins} دقيقة`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `منذ ${hrs} ساعة`;
  const days = Math.floor(hrs / 24);
  if (days < 30) return `منذ ${days} يوم`;
  return `منذ ${Math.floor(days / 30)} شهر`;
}

const avatarColors = ['bg-emerald-600', 'bg-blue-600', 'bg-amber-600', 'bg-purple-600', 'bg-rose-600', 'bg-teal-600', 'bg-orange-600'];

function PostCard({ post, onLike, onSave, onOpenComments }: { post: Post; onLike: () => void; onSave: () => void; onOpenComments: () => void }) {
  const ci = (post.author_name || '').charCodeAt(0) % avatarColors.length;
  return (
    <div className="bg-card border-b border-border/20 p-4" data-testid={`post-${post.id}`}>
      <div className="flex items-center gap-3 mb-3">
        <div className={cn('h-10 w-10 rounded-full flex items-center justify-center text-white text-sm font-bold shrink-0', avatarColors[ci])}>
          {post.author_avatar ? <img src={post.author_avatar} className="h-full w-full rounded-full object-cover" /> : (post.author_name?.[0] || '؟')}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-bold text-foreground truncate">{post.author_name}</p>
          <p className="text-[10px] text-muted-foreground">{timeAgo(post.created_at)}</p>
        </div>
      </div>
      <p className="text-sm text-foreground leading-relaxed whitespace-pre-line mb-3 font-arabic">{post.content}</p>
      {post.image_url && (
        <div className="rounded-2xl overflow-hidden mb-3 bg-muted">
          <img src={post.image_url} alt="" className="w-full max-h-80 object-cover" loading="lazy" />
        </div>
      )}
      <div className="flex items-center justify-between pt-2 border-t border-border/15">
        <button onClick={onLike} className={cn('flex items-center gap-1.5 text-xs', post.liked ? 'text-red-500' : 'text-muted-foreground')} data-testid={`like-${post.id}`}>
          <Heart className={cn('h-4 w-4', post.liked && 'fill-current')} />
          <span>{post.likes_count || ''}</span>
        </button>
        <button onClick={onOpenComments} className="flex items-center gap-1.5 text-xs text-muted-foreground" data-testid={`comment-${post.id}`}>
          <MessageCircle className="h-4 w-4" />
          <span>{post.comments_count || ''}</span>
        </button>
        <button className="flex items-center gap-1.5 text-xs text-muted-foreground">
          <Share2 className="h-4 w-4" />
          <span>{post.shares_count || ''}</span>
        </button>
        <button onClick={onSave} className={cn('text-xs', post.saved ? 'text-primary' : 'text-muted-foreground')} data-testid={`save-${post.id}`}>
          <Bookmark className={cn('h-4 w-4', post.saved && 'fill-current')} />
        </button>
      </div>
    </div>
  );
}

function CommentSheet({ postId, onClose }: { postId: string; onClose: () => void }) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/comments`).then(r => r.json()).then(d => { setComments(d.comments || []); setLoading(false); }).catch(() => setLoading(false));
  }, [postId]);

  const sendComment = async () => {
    if (!text.trim()) return;
    setSending(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/comments`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ content: text.trim() }) });
      if (r.status === 401) { toast.error('سجّل دخولك أولاً'); setSending(false); return; }
      const d = await r.json();
      if (d.comment) { setComments(prev => [...prev, d.comment]); setText(''); toast.success('تم إضافة تعليقك'); }
    } catch { toast.error('حدث خطأ'); }
    setSending(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }} className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[70vh] flex flex-col border-t border-border/30">
        <div className="flex items-center justify-between p-4 border-b border-border/20">
          <h3 className="text-sm font-bold text-foreground">التعليقات ({comments.length})</h3>
          <button onClick={onClose} className="p-1"><X className="h-5 w-5 text-muted-foreground" /></button>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {loading ? <Loader2 className="h-6 w-6 animate-spin text-muted-foreground mx-auto" /> :
            comments.length === 0 ? <p className="text-center text-sm text-muted-foreground py-8">لا توجد تعليقات بعد</p> :
            comments.map(c => (
              <div key={c.id} className="flex gap-2">
                <div className={cn('h-8 w-8 rounded-full flex items-center justify-center text-white text-xs font-bold shrink-0', avatarColors[(c.author_name || '').charCodeAt(0) % avatarColors.length])}>
                  {c.author_name?.[0] || '؟'}
                </div>
                <div className="bg-muted/50 rounded-2xl px-3 py-2 flex-1">
                  <p className="text-xs font-bold text-foreground">{c.author_name}</p>
                  <p className="text-xs text-foreground/80 mt-0.5">{c.content}</p>
                  <p className="text-[9px] text-muted-foreground mt-1">{timeAgo(c.created_at)}</p>
                </div>
              </div>
            ))
          }
        </div>
        <div className="p-3 border-t border-border/20 flex gap-2">
          <input value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendComment()} placeholder="اكتب تعليقاً..." className="flex-1 bg-muted/50 rounded-2xl px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground" data-testid="comment-input" />
          <button onClick={sendComment} disabled={!text.trim() || sending} className="h-10 w-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center shrink-0 disabled:opacity-40" data-testid="send-comment-btn">
            {sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </button>
        </div>
      </div>
    </motion.div>
  );
}

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
          <textarea
            value={content}
            onChange={e => setContent(e.target.value)}
            placeholder="شارك فكرة، آية، حديث، أو دعاء..."
            className="w-full h-32 bg-transparent resize-none outline-none text-sm text-foreground placeholder:text-muted-foreground leading-relaxed"
            autoFocus
            data-testid="post-content-input"
          />
          <div className="mt-3">
            <p className="text-xs font-bold text-muted-foreground mb-2">اختر الفئة:</p>
            <div className="flex flex-wrap gap-2">
              {categories.map(c => (
                <button
                  key={c.key}
                  onClick={() => setCategory(c.key)}
                  className={cn('px-3 py-1.5 rounded-full text-xs font-medium transition-all', category === c.key ? 'bg-primary text-primary-foreground' : 'bg-muted/50 text-muted-foreground')}
                  data-testid={`cat-${c.key}`}
                >
                  {c.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default function Sohba() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('all');
  const [posts, setPosts] = useState<Post[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [commentPostId, setCommentPostId] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);

  // Load categories
  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/categories`).then(r => r.json()).then(d => setCategories(d.categories || [])).catch(() => {});
  }, []);

  // Load posts
  const loadPosts = useCallback(async (cat: string, pg: number, append = false) => {
    setLoading(true);
    try {
      const token = getToken();
      const headers: Record<string, string> = {};
      if (token) headers['Authorization'] = `Bearer ${token}`;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts?category=${cat}&page=${pg}&limit=20`, { headers });
      const d = await r.json();
      if (append) setPosts(prev => [...prev, ...(d.posts || [])]);
      else setPosts(d.posts || []);
      setHasMore(d.has_more || false);
    } catch { toast.error('خطأ في تحميل المنشورات'); }
    setLoading(false);
  }, []);

  useEffect(() => { setPage(1); loadPosts(activeTab, 1); }, [activeTab, loadPosts]);

  const toggleLike = async (postId: string) => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setPosts(prev => prev.map(p => p.id === postId ? { ...p, liked: d.liked, likes_count: p.likes_count + (d.liked ? 1 : -1) } : p));
    } catch {}
  };

  const toggleSave = async (postId: string) => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/save`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setPosts(prev => prev.map(p => p.id === postId ? { ...p, saved: d.saved } : p));
    } catch {}
  };

  const onPostCreated = (post: Post) => { setPosts(prev => [post, ...prev]); };

  const allTabs = [{ key: 'all', label: 'الكل' }, ...categories];

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="sohba-page">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-card/95 backdrop-blur-xl border-b border-border/20">
        <div className="flex items-center justify-between px-4 py-3 pt-safe-header">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-primary" />
            <h1 className="text-lg font-bold text-foreground">صُحبة</h1>
          </div>
          <button className="p-2 rounded-xl bg-muted/50"><Search className="h-4 w-4 text-muted-foreground" /></button>
        </div>
        <div className="flex gap-1 px-4 pb-2 overflow-x-auto no-scrollbar">
          {allTabs.map(tab => (
            <button key={tab.key} onClick={() => setActiveTab(tab.key)} data-testid={`sohba-tab-${tab.key}`}
              className={cn('shrink-0 px-3.5 py-1.5 rounded-full text-xs font-bold transition-all', activeTab === tab.key ? 'bg-primary text-primary-foreground' : 'bg-muted/40 text-muted-foreground')}>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Posts */}
      {loading && posts.length === 0 ? (
        <div className="flex items-center justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>
      ) : posts.length === 0 ? (
        <div className="p-10 text-center">
          <Users className="h-14 w-14 text-muted-foreground/20 mx-auto mb-3" />
          <p className="text-base font-bold text-muted-foreground">لا توجد منشورات بعد</p>
          <p className="text-xs text-muted-foreground/60 mt-1">كن أول من ينشر في هذه الفئة!</p>
          {user && (
            <button onClick={() => setShowCreate(true)} className="mt-4 bg-primary text-primary-foreground px-6 py-2.5 rounded-2xl text-sm font-bold active:scale-95 transition-transform">
              أنشئ أول منشور
            </button>
          )}
        </div>
      ) : (
        <>
          {posts.map(post => (
            <PostCard key={post.id} post={post} onLike={() => toggleLike(post.id)} onSave={() => toggleSave(post.id)} onOpenComments={() => setCommentPostId(post.id)} />
          ))}
          {hasMore && (
            <button onClick={() => { const np = page + 1; setPage(np); loadPosts(activeTab, np, true); }} className="w-full py-4 text-sm text-primary font-bold">
              تحميل المزيد
            </button>
          )}
        </>
      )}

      {/* Create FAB */}
      <button
        data-testid="create-post-btn"
        onClick={() => { if (!user) { toast.error('سجّل دخولك أولاً'); navigate('/auth'); return; } setShowCreate(true); }}
        className="fixed bottom-20 left-5 z-40 h-14 w-14 rounded-full bg-primary text-primary-foreground shadow-lg shadow-primary/25 flex items-center justify-center active:scale-90 transition-transform"
      >
        <Plus className="h-6 w-6" />
      </button>

      {/* Sheets */}
      <AnimatePresence>
        {showCreate && <CreatePostSheet categories={categories} onClose={() => setShowCreate(false)} onCreated={onPostCreated} />}
        {commentPostId && <CommentSheet postId={commentPostId} onClose={() => setCommentPostId(null)} />}
      </AnimatePresence>
    </div>
  );
}
