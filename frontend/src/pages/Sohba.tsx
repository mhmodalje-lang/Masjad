import { useState, useEffect, useCallback, useRef } from 'react';
import { Users, Search, Heart, MessageCircle, Plus, Send, X, Loader2, Play, Image, Video, Gift, Share2, Bookmark, User, ChevronDown, Coins } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';

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
interface GiftItem {
  id: string; name: string; emoji: string; price_credits: number;
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
  return `${Math.floor(h / 24)}ي`;
}

const avatarColors = ['bg-emerald-600', 'bg-blue-600', 'bg-amber-600', 'bg-purple-600', 'bg-rose-600', 'bg-teal-600'];

// ============ FULL-SCREEN POST CARD (TikTok-style) ============
function FullScreenPost({ post, onLike, onOpenComments, onOpenGifts, onOpenProfile }: {
  post: Post; onLike: () => void; onOpenComments: () => void; onOpenGifts: () => void; onOpenProfile: () => void;
}) {
  const ci = (post.author_name || '').charCodeAt(0) % avatarColors.length;
  const mediaUrl = post.image_url ? (post.image_url.startsWith('/api/') ? `${BACKEND_URL}${post.image_url}` : post.image_url) : null;
  const isVideo = post.media_type === 'video';

  return (
    <div className="relative h-[calc(100vh-8rem)] snap-start flex flex-col bg-card" data-testid={`post-${post.id}`}>
      {/* Media / Content Area */}
      <div className="flex-1 relative overflow-hidden">
        {mediaUrl ? (
          <>
            {isVideo ? (
              <video src={mediaUrl} className="w-full h-full object-cover" controls playsInline />
            ) : (
              <img src={mediaUrl} alt="" className="w-full h-full object-cover" loading="lazy" />
            )}
            {/* Gradient overlay for text */}
            <div className="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-black/80 to-transparent" />
          </>
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary/5 to-accent/5 p-8">
            <p className="text-base text-foreground leading-relaxed font-arabic text-center">{post.content}</p>
          </div>
        )}

        {/* Author info - bottom left */}
        <div className="absolute bottom-4 right-4 left-16 z-10">
          <button onClick={onOpenProfile} className="flex items-center gap-2 mb-2">
            <div className={cn('h-9 w-9 rounded-full flex items-center justify-center text-xs text-white font-bold border-2 border-white/50', avatarColors[ci])}>
              {post.author_avatar ? <img src={post.author_avatar} className="h-full w-full rounded-full object-cover" /> : (post.author_name?.[0] || '؟')}
            </div>
            <div className="text-start">
              <p className="text-sm font-bold text-white drop-shadow-lg">{post.author_name}</p>
              <p className="text-[10px] text-white/60">{timeAgo(post.created_at)}</p>
            </div>
          </button>
          {mediaUrl && post.content && (
            <p className="text-xs text-white/90 line-clamp-2 drop-shadow-md">{post.content}</p>
          )}
        </div>

        {/* Action buttons - right side (TikTok style) */}
        <div className="absolute bottom-6 left-3 flex flex-col items-center gap-5 z-10">
          <button onClick={onLike} className="flex flex-col items-center gap-0.5" data-testid={`like-${post.id}`}>
            <div className={cn('h-10 w-10 rounded-full flex items-center justify-center', post.liked ? 'bg-red-500' : 'bg-black/30 backdrop-blur-sm')}>
              <Heart className={cn('h-5 w-5', post.liked ? 'text-white fill-current' : 'text-white')} />
            </div>
            <span className="text-[10px] text-white font-bold drop-shadow-lg">{post.likes_count || ''}</span>
          </button>

          <button onClick={onOpenComments} className="flex flex-col items-center gap-0.5" data-testid={`comments-${post.id}`}>
            <div className="h-10 w-10 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center">
              <MessageCircle className="h-5 w-5 text-white" />
            </div>
            <span className="text-[10px] text-white font-bold drop-shadow-lg">{post.comments_count || ''}</span>
          </button>

          <button onClick={onOpenGifts} className="flex flex-col items-center gap-0.5" data-testid={`gift-${post.id}`}>
            <div className="h-10 w-10 rounded-full bg-amber-500/80 backdrop-blur-sm flex items-center justify-center">
              <Gift className="h-5 w-5 text-white" />
            </div>
            <span className="text-[10px] text-white font-bold drop-shadow-lg">ادعم</span>
          </button>

          <button className="flex flex-col items-center gap-0.5">
            <div className="h-10 w-10 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center">
              <Share2 className="h-5 w-5 text-white" />
            </div>
          </button>
        </div>
      </div>
    </div>
  );
}

// ============ COMMENTS SHEET ============
function CommentsSheet({ post, onClose }: { post: Post; onClose: () => void }) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`).then(r => r.json()).then(d => setComments(d.comments || [])).catch(() => {});
  }, [post.id]);

  const send = async () => {
    if (!text.trim()) return;
    setSending(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ content: text.trim() }) });
      if (r.status === 401) { toast.error('سجّل دخولك'); setSending(false); return; }
      const d = await r.json();
      if (d.comment) { setComments(prev => [...prev, d.comment]); setText(''); }
    } catch { toast.error('خطأ'); }
    setSending(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }} className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/50" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[65vh] flex flex-col">
        <div className="flex items-center justify-between px-5 py-3 border-b border-border/20">
          <span className="text-sm font-bold text-foreground">{comments.length} تعليق</span>
          <button onClick={onClose}><X className="h-5 w-5 text-muted-foreground" /></button>
        </div>
        <div className="flex-1 overflow-y-auto px-5 py-3 space-y-3">
          {comments.length === 0 && <p className="text-center text-xs text-muted-foreground py-8">لا توجد تعليقات</p>}
          {comments.map(c => (
            <div key={c.id} className="flex gap-2">
              <div className={cn('h-7 w-7 rounded-full flex items-center justify-center text-[9px] text-white font-bold shrink-0', avatarColors[(c.author_name||'').charCodeAt(0) % avatarColors.length])}>
                {c.author_name?.[0] || '؟'}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-bold text-foreground">{c.author_name}</span>
                  <span className="text-[9px] text-muted-foreground">{timeAgo(c.created_at)}</span>
                </div>
                <p className="text-xs text-foreground/80 mt-0.5">{c.content}</p>
              </div>
            </div>
          ))}
        </div>
        <div className="px-4 py-3 border-t border-border/20 flex gap-2">
          <input value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()}
            placeholder="اكتب تعليقاً..." className="flex-1 bg-muted/50 rounded-2xl px-4 py-2 text-sm outline-none" data-testid="comment-input" />
          <button onClick={send} disabled={!text.trim() || sending} className="h-9 w-9 rounded-full bg-primary text-primary-foreground flex items-center justify-center shrink-0 disabled:opacity-40" data-testid="send-comment-btn">
            {sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </button>
        </div>
      </div>
    </motion.div>
  );
}

// ============ GIFTS SHEET ============
function GiftsSheet({ post, onClose }: { post: Post; onClose: () => void }) {
  const [gifts, setGifts] = useState<GiftItem[]>([]);
  const [sending, setSending] = useState('');

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/gifts/list`).then(r => r.json()).then(d => setGifts(d.gifts || [])).catch(() => {});
  }, []);

  const sendGift = async (gift: GiftItem) => {
    setSending(gift.id);
    try {
      const r = await fetch(`${BACKEND_URL}/api/gifts/send`, {
        method: 'POST', headers: authHeaders(),
        body: JSON.stringify({ gift_id: gift.id, recipient_id: post.author_id, post_id: post.id }),
      });
      const d = await r.json();
      if (r.ok) {
        toast.success(d.message);
        onClose();
      } else {
        toast.error(d.detail || 'فشل الإرسال');
      }
    } catch { toast.error('خطأ'); }
    setSending('');
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }} className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/50" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[50vh] flex flex-col">
        <div className="flex items-center justify-between px-5 py-3 border-b border-border/20">
          <div>
            <span className="text-sm font-bold text-foreground">إرسال هدية</span>
            <p className="text-[10px] text-muted-foreground">لـ {post.author_name}</p>
          </div>
          <button onClick={onClose}><X className="h-5 w-5 text-muted-foreground" /></button>
        </div>
        <div className="flex-1 overflow-y-auto px-4 py-3">
          <div className="grid grid-cols-4 gap-3">
            {gifts.map(g => (
              <button key={g.id} onClick={() => sendGift(g)} disabled={sending === g.id}
                className="flex flex-col items-center gap-1 p-3 rounded-2xl bg-muted/50 hover:bg-primary/10 active:scale-95 transition-all"
                data-testid={`send-gift-${g.id}`}>
                <span className="text-2xl">{g.emoji}</span>
                <span className="text-[9px] font-bold text-foreground">{g.name}</span>
                <span className="flex items-center gap-0.5 text-[8px] text-amber-500">
                  <Coins className="h-2.5 w-2.5" />{g.price_credits}
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

// ============ USER PROFILE SHEET ============
function ProfileSheet({ userId, onClose }: { userId: string; onClose: () => void }) {
  const [profile, setProfile] = useState<any>(null);
  const [stats, setStats] = useState<any>({});
  const [posts, setPosts] = useState<Post[]>([]);
  const [isFollowing, setIsFollowing] = useState(false);

  useEffect(() => {
    const token = getToken();
    const headers: Record<string, string> = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    fetch(`${BACKEND_URL}/api/sohba/profile/${userId}`, { headers })
      .then(r => r.json())
      .then(d => { setProfile(d.profile); setStats(d.stats); setIsFollowing(d.is_following); });

    fetch(`${BACKEND_URL}/api/sohba/posts?author=${userId}&limit=20`, { headers })
      .then(r => r.json())
      .then(d => setPosts(d.posts || [])).catch(() => {});
  }, [userId]);

  const toggleFollow = async () => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/follow/${userId}`, { method: 'POST', headers: authHeaders() });
      if (r.status === 401) { toast.error('سجّل دخولك'); return; }
      const d = await r.json();
      setIsFollowing(d.following);
      setStats((prev: any) => ({ ...prev, followers_count: prev.followers_count + (d.following ? 1 : -1) }));
    } catch { }
  };

  if (!profile) return null;
  const ci = (profile.name || '').charCodeAt(0) % avatarColors.length;

  return (
    <motion.div initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }} className="fixed inset-0 z-[999] bg-background" dir="rtl">
      <div className="h-full overflow-y-auto pb-20">
        {/* Header */}
        <div className="relative bg-gradient-to-br from-primary/15 to-accent/10 px-5 pt-safe-header pb-8">
          <button onClick={onClose} className="absolute top-4 left-4 p-2 rounded-full bg-black/20"><X className="h-5 w-5 text-foreground" /></button>
          <div className="text-center pt-4">
            <div className={cn('h-20 w-20 mx-auto rounded-full flex items-center justify-center text-2xl text-white font-bold border-4 border-background', avatarColors[ci])}>
              {profile.avatar ? <img src={profile.avatar} className="h-full w-full rounded-full object-cover" /> : (profile.name?.[0] || '؟')}
            </div>
            <h2 className="text-lg font-bold text-foreground mt-3">{profile.name}</h2>
            <div className="flex items-center justify-center gap-6 mt-3">
              <div className="text-center"><p className="text-lg font-bold text-foreground">{stats.posts_count || 0}</p><p className="text-[10px] text-muted-foreground">منشور</p></div>
              <div className="text-center"><p className="text-lg font-bold text-foreground">{stats.followers_count || 0}</p><p className="text-[10px] text-muted-foreground">متابع</p></div>
              <div className="text-center"><p className="text-lg font-bold text-foreground">{stats.following_count || 0}</p><p className="text-[10px] text-muted-foreground">متابَع</p></div>
            </div>
            <div className="flex gap-2 mt-4 justify-center">
              <Button onClick={toggleFollow} variant={isFollowing ? "outline" : "default"} className="rounded-xl px-6" data-testid="follow-btn">
                {isFollowing ? 'إلغاء المتابعة' : 'متابعة'}
              </Button>
              <Button variant="outline" className="rounded-xl" asChild><Link to="/rewards">ادعم</Link></Button>
            </div>
          </div>
        </div>

        {/* Posts grid */}
        <div className="px-3 mt-4 grid grid-cols-3 gap-1">
          {posts.map(p => (
            <div key={p.id} className="aspect-square bg-muted rounded-lg overflow-hidden">
              {p.image_url ? (
                <img src={p.image_url.startsWith('/api/') ? `${BACKEND_URL}${p.image_url}` : p.image_url} alt="" className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center p-2">
                  <p className="text-[9px] text-muted-foreground line-clamp-4 text-center">{p.content}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

// ============ CREATE POST SHEET ============
function CreatePostSheet({ categories, onClose, onCreated }: { categories: Category[]; onClose: () => void; onCreated: (p: Post) => void }) {
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('general');
  const [posting, setPosting] = useState(false);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    // For small files, use base64
    if (file.size < 5 * 1024 * 1024) {
      const reader = new FileReader();
      reader.onload = () => setImagePreview(reader.result as string);
      reader.readAsDataURL(file);
    } else {
      // Large files: use multipart streaming upload
      setUploadProgress(1);
      const formData = new FormData();
      formData.append('file', file);
      try {
        const res = await fetch(`${BACKEND_URL}/api/upload/multipart`, { method: 'POST', body: formData });
        const data = await res.json();
        if (res.ok && data.url) {
          setImagePreview(`${BACKEND_URL}${data.url}`);
          setUploadProgress(100);
        } else {
          toast.error('فشل رفع الملف');
          setUploadProgress(0);
        }
      } catch {
        toast.error('خطأ في الرفع');
        setUploadProgress(0);
      }
    }
  };

  const submit = async () => {
    if (!content.trim() && !imagePreview) { toast.error('اكتب شيئاً أو أضف صورة'); return; }
    setPosting(true);
    let uploadedUrl = '';

    if (imagePreview) {
      if (imagePreview.startsWith('data:')) {
        // Base64 upload
        try {
          const upRes = await fetch(`${BACKEND_URL}/api/upload/file`, {
            method: 'POST', headers: authHeaders(),
            body: JSON.stringify({ data: imagePreview, filename: 'post.jpg' }),
          });
          const upData = await upRes.json();
          if (upRes.ok) uploadedUrl = upData.url;
        } catch { }
      } else if (imagePreview.includes('/api/uploads/')) {
        uploadedUrl = imagePreview.replace(BACKEND_URL, '');
      }
    }

    try {
      const body: any = { content: content.trim(), category };
      if (uploadedUrl) body.image_url = uploadedUrl;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(body) });
      if (r.status === 401) { toast.error('سجّل دخولك'); setPosting(false); return; }
      const d = await r.json();
      if (d.post) { onCreated(d.post); toast.success('تم النشر!'); onClose(); }
    } catch { toast.error('خطأ في النشر'); }
    setPosting(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }} className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/50" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[85vh] flex flex-col border-t border-border/30">
        <div className="flex items-center justify-between p-4 border-b border-border/20">
          <button onClick={onClose} className="text-sm text-muted-foreground">إلغاء</button>
          <h3 className="text-sm font-bold text-foreground">منشور جديد</h3>
          <button onClick={submit} disabled={(!content.trim() && !imagePreview) || posting}
            className="text-sm font-bold text-primary disabled:opacity-40" data-testid="submit-post-btn">
            {posting ? <Loader2 className="h-4 w-4 animate-spin" /> : 'نشر'}
          </button>
        </div>
        <div className="p-4 flex-1 overflow-y-auto">
          <textarea value={content} onChange={e => setContent(e.target.value)}
            placeholder="شارك فكرة، آية، حديث، أو دعاء..."
            className="w-full h-28 bg-transparent resize-none outline-none text-sm text-foreground placeholder:text-muted-foreground leading-relaxed" autoFocus data-testid="post-content-input" />

          {imagePreview && (
            <div className="relative mb-3 rounded-xl overflow-hidden">
              {imagePreview.includes('.mp4') || imagePreview.includes('.webm') ? (
                <video src={imagePreview} className="w-full max-h-48 object-cover rounded-xl" controls />
              ) : (
                <img src={imagePreview} alt="preview" className="w-full max-h-48 object-cover rounded-xl" />
              )}
              <button onClick={() => { setImagePreview(null); setUploadProgress(0); }}
                className="absolute top-2 left-2 p-1.5 rounded-full bg-black/60 text-white">
                <X className="h-3.5 w-3.5" />
              </button>
              {uploadProgress > 0 && uploadProgress < 100 && (
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                  <Loader2 className="h-8 w-8 text-white animate-spin" />
                </div>
              )}
            </div>
          )}

          <div className="flex gap-2 mt-2 mb-4">
            <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
            <input ref={videoRef} type="file" accept="video/*" className="hidden" onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
            <button onClick={() => fileRef.current?.click()} className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-muted/50 text-xs text-muted-foreground hover:bg-primary/10 hover:text-primary transition-colors" data-testid="upload-image-btn">
              <Image className="h-4 w-4" /> صورة
            </button>
            <button onClick={() => videoRef.current?.click()} className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-muted/50 text-xs text-muted-foreground hover:bg-primary/10 hover:text-primary transition-colors" data-testid="upload-video-btn">
              <Video className="h-4 w-4" /> فيديو
            </button>
          </div>

          <p className="text-xs font-bold text-muted-foreground mb-2">الفئة:</p>
          <div className="flex flex-wrap gap-2">
            {categories.map(c => (
              <button key={c.key} onClick={() => setCategory(c.key)} data-testid={`cat-${c.key}`}
                className={cn('px-4 py-2 rounded-full text-xs font-bold transition-all', category === c.key ? 'bg-primary text-primary-foreground' : 'bg-muted/50 text-muted-foreground')}>
                {c.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

// ============ MAIN SOHBA PAGE ============
export default function Sohba() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('all');
  const [posts, setPosts] = useState<Post[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [commentPost, setCommentPost] = useState<Post | null>(null);
  const [giftPost, setGiftPost] = useState<Post | null>(null);
  const [profileUserId, setProfileUserId] = useState<string | null>(null);
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
    } catch { }
    setLoading(false);
  }, []);

  useEffect(() => { setPage(1); loadPosts(activeTab, 1); }, [activeTab, loadPosts]);

  const toggleLike = async (postId: string) => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setPosts(prev => prev.map(p => p.id === postId ? { ...p, liked: d.liked, likes_count: p.likes_count + (d.liked ? 1 : -1) } : p));
    } catch { }
  };

  const allTabs = [{ key: 'all', label: 'الكل' }, ...categories];

  return (
    <div className="min-h-screen" dir="rtl" data-testid="sohba-page">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-card/95 backdrop-blur-xl border-b border-border/15">
        <div className="flex items-center justify-between px-4 py-2.5 pt-safe-header">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-primary" />
            <h1 className="text-lg font-bold text-foreground">صُحبة</h1>
          </div>
          <button className="p-2 rounded-xl bg-muted/50"><Search className="h-4 w-4 text-muted-foreground" /></button>
        </div>
        <div className="flex gap-1.5 px-3 pb-2 overflow-x-auto no-scrollbar">
          {allTabs.map(tab => (
            <button key={tab.key} onClick={() => setActiveTab(tab.key)} data-testid={`sohba-tab-${tab.key}`}
              className={cn('shrink-0 px-3.5 py-1.5 rounded-full text-xs font-bold transition-all',
                activeTab === tab.key ? 'bg-primary text-primary-foreground' : 'bg-muted/40 text-muted-foreground')}>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Feed - TikTok style vertical scroll */}
      {loading && posts.length === 0 ? (
        <div className="flex items-center justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>
      ) : posts.length === 0 ? (
        <div className="p-10 text-center">
          <Users className="h-14 w-14 text-muted-foreground/15 mx-auto mb-3" />
          <p className="text-base font-bold text-muted-foreground">لا توجد منشورات بعد</p>
          {user && (
            <button onClick={() => setShowCreate(true)} className="mt-4 bg-primary text-primary-foreground px-6 py-2.5 rounded-2xl text-sm font-bold" data-testid="first-post-btn">
              أنشئ أول منشور
            </button>
          )}
        </div>
      ) : (
        <div className="snap-y snap-mandatory pb-20">
          {posts.map((post) => (
            <FullScreenPost
              key={post.id}
              post={post}
              onLike={() => toggleLike(post.id)}
              onOpenComments={() => setCommentPost(post)}
              onOpenGifts={() => { if (!user) { toast.error('سجّل دخولك'); return; } setGiftPost(post); }}
              onOpenProfile={() => setProfileUserId(post.author_id)}
            />
          ))}
          {hasMore && (
            <button onClick={() => { const np = page + 1; setPage(np); loadPosts(activeTab, np, true); }}
              className="w-full py-6 text-sm text-primary font-bold flex items-center justify-center gap-2">
              <ChevronDown className="h-4 w-4" /> تحميل المزيد
            </button>
          )}
        </div>
      )}

      {/* Create FAB */}
      <button data-testid="create-post-btn"
        onClick={() => { if (!user) { toast.error('سجّل دخولك'); navigate('/auth'); return; } setShowCreate(true); }}
        className="fixed bottom-20 left-5 z-40 h-14 w-14 rounded-full bg-primary text-primary-foreground shadow-lg shadow-primary/25 flex items-center justify-center active:scale-90 transition-transform">
        <Plus className="h-6 w-6" />
      </button>

      {/* Sheets */}
      <AnimatePresence>
        {showCreate && <CreatePostSheet categories={categories} onClose={() => setShowCreate(false)} onCreated={p => setPosts(prev => [p, ...prev])} />}
        {commentPost && <CommentsSheet post={commentPost} onClose={() => setCommentPost(null)} />}
        {giftPost && <GiftsSheet post={giftPost} onClose={() => setGiftPost(null)} />}
        {profileUserId && <ProfileSheet userId={profileUserId} onClose={() => setProfileUserId(null)} />}
      </AnimatePresence>
    </div>
  );
}
