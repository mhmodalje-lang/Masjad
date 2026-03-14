import { useState, useEffect, useCallback, useRef } from 'react';
import { Heart, MessageCircle, Send, Bookmark, MoreHorizontal, Plus, X, Loader2, Image, Video, Gift, Share2, User, ChevronDown, Coins, Radio, Eye, Play, Pause } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Post {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  content: string; category: string; image_url?: string; media_type?: string;
  created_at: string; likes_count: number; comments_count: number;
  shares_count: number; liked: boolean; saved: boolean;
}
interface Comment { id: string; author_name: string; author_avatar?: string; content: string; created_at: string; }
interface GiftItem { id: string; name: string; emoji: string; price_credits: number; }

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders() { return { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` }; }
function timeAgo(iso: string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return 'الآن';
  if (m < 60) return `${m}د`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}س`;
  return `${Math.floor(h / 24)}ي`;
}

const avatarColors = ['bg-emerald-600', 'bg-blue-600', 'bg-amber-600', 'bg-purple-600', 'bg-rose-600', 'bg-teal-600'];

/* ========== ISLAMIC DECORATIVE BORDER SVG ========== */
function IslamicFrame() {
  return (
    <div className="absolute inset-0 pointer-events-none z-[5]">
      {/* Top border */}
      <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-transparent via-amber-500/40 to-transparent" />
      {/* Bottom border */}
      <div className="absolute bottom-0 inset-x-0 h-1 bg-gradient-to-r from-transparent via-amber-500/40 to-transparent" />
      {/* Corner ornaments */}
      <svg className="absolute top-2 right-2 w-8 h-8 text-amber-500/20" viewBox="0 0 40 40">
        <path d="M20 0 L25 10 L40 10 L28 18 L32 30 L20 22 L8 30 L12 18 L0 10 L15 10 Z" fill="currentColor" />
      </svg>
      <svg className="absolute top-2 left-2 w-8 h-8 text-amber-500/20" viewBox="0 0 40 40">
        <path d="M20 0 L25 10 L40 10 L28 18 L32 30 L20 22 L8 30 L12 18 L0 10 L15 10 Z" fill="currentColor" />
      </svg>
      {/* Islamic geometric pattern overlay */}
      <div className="absolute inset-0 opacity-[0.03]" style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 5L35 15H25zM5 30L15 35V25zM55 30L45 25V35zM30 55L25 45H35z' fill='%23D4A853' fill-opacity='0.5'/%3E%3Ccircle cx='30' cy='30' r='3' fill='none' stroke='%23D4A853' stroke-opacity='0.3'/%3E%3C/svg%3E")`,
      }} />
    </div>
  );
}

/* ========== FULL-SCREEN POST (TikTok-Style matching the image) ========== */
function FullScreenPost({ post, onLike, onSave, onOpenComments, onOpenGifts, onOpenProfile, onShare }: {
  post: Post; onLike: () => void; onSave: () => void; onOpenComments: () => void; onOpenGifts: () => void; onOpenProfile: () => void; onShare: () => void;
}) {
  const ci = (post.author_name || '').charCodeAt(0) % avatarColors.length;
  const rawUrl = post.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('/api/') ? `${BACKEND_URL}${rawUrl}` : rawUrl) : null;
  const isVideo = post.media_type === 'video' || (mediaUrl && /\.(mp4|webm|mov)/.test(mediaUrl));
  const videoRef = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(true);

  const togglePlay = () => {
    if (videoRef.current) {
      if (videoRef.current.paused) { videoRef.current.play(); setPlaying(true); }
      else { videoRef.current.pause(); setPlaying(false); }
    }
  };

  return (
    <div className="relative h-[calc(100dvh-3.5rem)] w-full snap-start bg-black flex-shrink-0" data-testid={`post-${post.id}`}>
      <IslamicFrame />

      {/* Media / Content Area */}
      <div className="absolute inset-0">
        {mediaUrl && isVideo ? (
          <div className="relative w-full h-full" onClick={togglePlay}>
            <video ref={videoRef} src={mediaUrl} className="w-full h-full object-cover" loop muted playsInline autoPlay />
            {!playing && <div className="absolute inset-0 flex items-center justify-center"><Play className="h-16 w-16 text-white/60" /></div>}
          </div>
        ) : mediaUrl ? (
          <img src={mediaUrl} alt="" className="w-full h-full object-cover" loading="lazy" />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-emerald-950 via-black to-emerald-950 p-10">
            <p className="text-lg text-white/90 leading-relaxed font-arabic text-center max-w-md">{post.content}</p>
          </div>
        )}
        {/* Bottom gradient */}
        <div className="absolute inset-x-0 bottom-0 h-2/5 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
        {/* Top gradient */}
        <div className="absolute inset-x-0 top-0 h-20 bg-gradient-to-b from-black/30 to-transparent" />
      </div>

      {/* ===== RIGHT SIDE ACTION BUTTONS (like TikTok image) ===== */}
      <div className="absolute right-3 bottom-36 flex flex-col items-center gap-5 z-20">
        {/* Like */}
        <button onClick={onLike} className="flex flex-col items-center gap-1" data-testid={`like-${post.id}`}>
          <Heart className={cn('h-8 w-8 drop-shadow-lg', post.liked ? 'text-red-500 fill-red-500' : 'text-white')} />
          <span className="text-[11px] text-white font-semibold drop-shadow-lg">{post.likes_count > 0 ? post.likes_count : ''}</span>
        </button>
        {/* Comment */}
        <button onClick={onOpenComments} className="flex flex-col items-center gap-1" data-testid={`comments-${post.id}`}>
          <MessageCircle className="h-8 w-8 text-white drop-shadow-lg" />
          <span className="text-[11px] text-white font-semibold drop-shadow-lg">{post.comments_count > 0 ? post.comments_count : ''}</span>
        </button>
        {/* Share */}
        <button onClick={onShare} className="flex flex-col items-center gap-1">
          <Share2 className="h-7 w-7 text-white drop-shadow-lg" />
          <span className="text-[11px] text-white font-semibold drop-shadow-lg">{post.shares_count > 0 ? post.shares_count : ''}</span>
        </button>
        {/* Send/Gift */}
        <button onClick={onOpenGifts} className="flex flex-col items-center gap-1" data-testid={`gift-${post.id}`}>
          <Send className="h-7 w-7 text-white drop-shadow-lg" />
        </button>
        {/* Bookmark */}
        <button onClick={onSave} className="flex flex-col items-center gap-1" data-testid={`save-${post.id}`}>
          <Bookmark className={cn('h-7 w-7 drop-shadow-lg', post.saved ? 'text-amber-400 fill-amber-400' : 'text-white')} />
        </button>
        {/* More */}
        <button className="flex flex-col items-center">
          <MoreHorizontal className="h-7 w-7 text-white drop-shadow-lg" />
        </button>
      </div>

      {/* ===== BOTTOM AUTHOR INFO (matching the image exactly) ===== */}
      <div className="absolute bottom-4 right-4 left-16 z-20" dir="rtl">
        {/* Author row */}
        <div className="flex items-center gap-2.5 mb-2">
          <button onClick={onOpenProfile} className="shrink-0">
            <div className={cn('h-11 w-11 rounded-full flex items-center justify-center text-sm text-white font-bold border-2 border-white/60 shadow-lg', avatarColors[ci])}>
              {post.author_avatar ? <img src={post.author_avatar} className="h-full w-full rounded-full object-cover" /> : (post.author_name?.[0] || '؟')}
            </div>
          </button>
          <span className="text-[13px] font-bold text-white drop-shadow-lg">{post.author_name}</span>
          <button className="border border-white/60 rounded-lg px-3 py-1 text-[11px] text-white font-bold" data-testid={`follow-btn-${post.id}`}>
            متابعة
          </button>
        </div>

        {/* Caption */}
        {(mediaUrl && post.content) && (
          <p className="text-[13px] text-white/90 leading-relaxed drop-shadow-md line-clamp-2 mb-1.5">{post.content}</p>
        )}

        {/* Likes info */}
        {post.likes_count > 0 && (
          <p className="text-[11px] text-white/60 drop-shadow-md">
            حاز على إعجاب <span className="text-white/80 font-semibold">{post.likes_count}</span> شخص
          </p>
        )}
      </div>

      {/* LIVE indicator for live posts */}
      {post.category === 'live' && (
        <div className="absolute top-4 left-4 z-20 flex items-center gap-1.5 bg-red-600 rounded-lg px-2.5 py-1">
          <Radio className="h-3.5 w-3.5 text-white animate-pulse" />
          <span className="text-[10px] text-white font-bold">مباشر</span>
        </div>
      )}
    </div>
  );
}

/* ========== COMMENTS SHEET ========== */
function CommentsSheet({ post, onClose }: { post: Post; onClose: () => void }) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  useEffect(() => { fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`).then(r => r.json()).then(d => setComments(d.comments || [])).catch(() => {}); }, [post.id]);
  const send = async () => {
    if (!text.trim()) return; setSending(true);
    try { const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ content: text.trim() }) }); if (r.status === 401) { toast.error('سجّل دخولك'); setSending(false); return; } const d = await r.json(); if (d.comment) { setComments(p => [...p, d.comment]); setText(''); } } catch { toast.error('خطأ'); } setSending(false);
  };
  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }} className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[65vh] flex flex-col">
        <div className="flex items-center justify-between px-5 py-3 border-b border-border/20"><span className="text-sm font-bold">{comments.length} تعليق</span><button onClick={onClose}><X className="h-5 w-5 text-muted-foreground" /></button></div>
        <div className="flex-1 overflow-y-auto px-5 py-3 space-y-3">
          {comments.length === 0 && <p className="text-center text-xs text-muted-foreground py-8">لا توجد تعليقات</p>}
          {comments.map(c => (<div key={c.id} className="flex gap-2"><div className={cn('h-7 w-7 rounded-full flex items-center justify-center text-[9px] text-white font-bold shrink-0', avatarColors[(c.author_name||'').charCodeAt(0) % avatarColors.length])}>{c.author_name?.[0]}</div><div className="flex-1"><div className="flex items-center gap-2"><span className="text-[11px] font-bold text-foreground">{c.author_name}</span><span className="text-[9px] text-muted-foreground">{timeAgo(c.created_at)}</span></div><p className="text-xs text-foreground/80 mt-0.5">{c.content}</p></div></div>))}
        </div>
        <div className="px-4 py-3 border-t border-border/20 flex gap-2"><input value={text} onChange={e=>setText(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder="اكتب تعليقاً..." className="flex-1 bg-muted/50 rounded-2xl px-4 py-2.5 text-sm outline-none" data-testid="comment-input" /><button onClick={send} disabled={!text.trim()||sending} className="h-10 w-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center shrink-0 disabled:opacity-40" data-testid="send-comment-btn">{sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}</button></div>
      </div>
    </motion.div>
  );
}

/* ========== GIFTS SHEET ========== */
function GiftsSheet({ post, onClose }: { post: Post; onClose: () => void }) {
  const [gifts, setGifts] = useState<GiftItem[]>([]);
  const [sending, setSending] = useState('');
  useEffect(() => { fetch(`${BACKEND_URL}/api/gifts/list`).then(r=>r.json()).then(d=>setGifts(d.gifts||[])).catch(()=>{}); }, []);
  const sendGift = async (gift: GiftItem) => {
    setSending(gift.id);
    try { const r = await fetch(`${BACKEND_URL}/api/gifts/send`, { method:'POST', headers:authHeaders(), body:JSON.stringify({ gift_id:gift.id, recipient_id:post.author_id, post_id:post.id }) }); const d = await r.json(); if (r.ok) { toast.success(d.message); onClose(); } else toast.error(d.detail||'فشل'); } catch { toast.error('خطأ'); }
    setSending('');
  };
  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }} className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/60" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[50vh] flex flex-col">
        <div className="flex items-center justify-between px-5 py-3 border-b border-border/20"><div><span className="text-sm font-bold">إرسال هدية</span><p className="text-[10px] text-muted-foreground">لـ {post.author_name}</p></div><button onClick={onClose}><X className="h-5 w-5 text-muted-foreground" /></button></div>
        <div className="flex-1 overflow-y-auto px-4 py-3"><div className="grid grid-cols-4 gap-3">
          {gifts.map(g=>(<button key={g.id} onClick={()=>sendGift(g)} disabled={sending===g.id} className="flex flex-col items-center gap-1 p-3 rounded-2xl bg-muted/50 hover:bg-primary/10 active:scale-95 transition-all" data-testid={`send-gift-${g.id}`}><span className="text-2xl">{g.emoji}</span><span className="text-[9px] font-bold">{g.name}</span><span className="flex items-center gap-0.5 text-[8px] text-amber-500"><Coins className="h-2.5 w-2.5"/>{g.price_credits}</span></button>))}
        </div></div>
      </div>
    </motion.div>
  );
}

/* ========== USER PROFILE SHEET ========== */
function ProfileSheet({ userId, onClose }: { userId: string; onClose: () => void }) {
  const [profile, setProfile] = useState<any>(null);
  const [stats, setStats] = useState<any>({});
  const [posts, setPosts] = useState<Post[]>([]);
  const [isFollowing, setIsFollowing] = useState(false);
  useEffect(() => {
    const h: any = {}; const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
    fetch(`${BACKEND_URL}/api/sohba/profile/${userId}`, { headers: h }).then(r=>r.json()).then(d=>{ setProfile(d.profile); setStats(d.stats); setIsFollowing(d.is_following); });
    fetch(`${BACKEND_URL}/api/sohba/posts?author=${userId}&limit=20`, { headers: h }).then(r=>r.json()).then(d=>setPosts(d.posts||[])).catch(()=>{});
  }, [userId]);
  const toggleFollow = async () => { try { const r = await fetch(`${BACKEND_URL}/api/sohba/follow/${userId}`, { method:'POST', headers:authHeaders() }); if (r.status===401){toast.error('سجّل دخولك');return;} const d=await r.json(); setIsFollowing(d.following); } catch{} };
  if (!profile) return null;
  const ci = (profile.name || '').charCodeAt(0) % avatarColors.length;
  return (
    <motion.div initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }} className="fixed inset-0 z-[999] bg-background" dir="rtl">
      <div className="h-full overflow-y-auto pb-20">
        <div className="relative bg-gradient-to-br from-primary/15 to-accent/10 px-5 pt-6 pb-8">
          <button onClick={onClose} className="absolute top-4 left-4 p-2 rounded-full bg-black/20"><X className="h-5 w-5" /></button>
          <div className="text-center pt-4">
            <div className={cn('h-20 w-20 mx-auto rounded-full flex items-center justify-center text-2xl text-white font-bold border-4 border-background', avatarColors[ci])}>
              {profile.avatar ? <img src={profile.avatar} className="h-full w-full rounded-full object-cover" /> : (profile.name?.[0] || '؟')}
            </div>
            <h2 className="text-lg font-bold mt-3">{profile.name}</h2>
            <div className="flex items-center justify-center gap-6 mt-3">
              <div className="text-center"><p className="text-lg font-bold">{stats.posts_count||0}</p><p className="text-[10px] text-muted-foreground">منشور</p></div>
              <div className="text-center"><p className="text-lg font-bold">{stats.followers_count||0}</p><p className="text-[10px] text-muted-foreground">متابع</p></div>
              <div className="text-center"><p className="text-lg font-bold">{stats.following_count||0}</p><p className="text-[10px] text-muted-foreground">متابَع</p></div>
            </div>
            <div className="flex gap-2 mt-4 justify-center">
              <Button onClick={toggleFollow} variant={isFollowing ? "outline" : "default"} className="rounded-xl px-6">{isFollowing ? 'إلغاء المتابعة' : 'متابعة'}</Button>
              <Button variant="outline" className="rounded-xl" asChild><Link to="/rewards">ادعم</Link></Button>
            </div>
          </div>
        </div>
        <div className="px-3 mt-4 grid grid-cols-3 gap-1">
          {posts.map(p=>(<div key={p.id} className="aspect-square bg-muted rounded-lg overflow-hidden">{p.image_url ? <img src={p.image_url.startsWith('/api/')?`${BACKEND_URL}${p.image_url}`:p.image_url} alt="" className="w-full h-full object-cover" /> : <div className="w-full h-full flex items-center justify-center p-2"><p className="text-[9px] text-muted-foreground line-clamp-4 text-center">{p.content}</p></div>}</div>))}
        </div>
      </div>
    </motion.div>
  );
}

/* ========== CREATE POST SHEET ========== */
function CreatePostSheet({ categories, onClose, onCreated }: { categories: any[]; onClose: () => void; onCreated: (p: Post) => void }) {
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('general');
  const [posting, setPosting] = useState(false);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    if (file.size < 5 * 1024 * 1024) {
      const reader = new FileReader();
      reader.onload = () => setImagePreview(reader.result as string);
      reader.readAsDataURL(file);
    } else {
      setUploadProgress(1);
      const formData = new FormData(); formData.append('file', file);
      try {
        const res = await fetch(`${BACKEND_URL}/api/upload/multipart`, { method: 'POST', body: formData });
        const data = await res.json();
        if (res.ok && data.url) { setImagePreview(`${BACKEND_URL}${data.url}`); setUploadProgress(100); }
        else { toast.error('فشل رفع الملف'); setUploadProgress(0); }
      } catch { toast.error('خطأ في الرفع'); setUploadProgress(0); }
    }
  };

  const submit = async () => {
    if (!content.trim() && !imagePreview) { toast.error('اكتب شيئاً أو أضف صورة'); return; }
    setPosting(true);
    let uploadedUrl = '';
    if (imagePreview) {
      if (imagePreview.startsWith('data:')) {
        try { const r = await fetch(`${BACKEND_URL}/api/upload/file`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ data: imagePreview, filename: 'post.jpg' }) }); const d = await r.json(); if (r.ok) uploadedUrl = d.url; } catch {}
      } else if (imagePreview.includes('/api/uploads/')) { uploadedUrl = imagePreview.replace(BACKEND_URL, ''); }
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
      <div className="flex-1 bg-black/60" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[85vh] flex flex-col border-t border-border/30">
        <div className="flex items-center justify-between p-4 border-b border-border/20">
          <button onClick={onClose} className="text-sm text-muted-foreground">إلغاء</button>
          <h3 className="text-sm font-bold">منشور جديد</h3>
          <button onClick={submit} disabled={(!content.trim()&&!imagePreview)||posting} className="text-sm font-bold text-primary disabled:opacity-40" data-testid="submit-post-btn">{posting ? <Loader2 className="h-4 w-4 animate-spin" /> : 'نشر'}</button>
        </div>
        <div className="p-4 flex-1 overflow-y-auto">
          <textarea value={content} onChange={e=>setContent(e.target.value)} placeholder="شارك فكرة، آية، حديث، أو دعاء..." className="w-full h-28 bg-transparent resize-none outline-none text-sm leading-relaxed" autoFocus data-testid="post-content-input" />
          {imagePreview && (<div className="relative mb-3 rounded-xl overflow-hidden"><img src={imagePreview} alt="" className="w-full max-h-48 object-cover rounded-xl" /><button onClick={()=>{setImagePreview(null);setUploadProgress(0)}} className="absolute top-2 left-2 p-1.5 rounded-full bg-black/60 text-white"><X className="h-3.5 w-3.5" /></button>{uploadProgress>0&&uploadProgress<100&&<div className="absolute inset-0 bg-black/40 flex items-center justify-center"><Loader2 className="h-8 w-8 text-white animate-spin" /></div>}</div>)}
          <div className="flex gap-2 mt-2 mb-4">
            <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={e=>e.target.files?.[0]&&handleFile(e.target.files[0])} />
            <input ref={videoRef} type="file" accept="video/*" className="hidden" onChange={e=>e.target.files?.[0]&&handleFile(e.target.files[0])} />
            <button onClick={()=>fileRef.current?.click()} className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-muted/50 text-xs text-muted-foreground hover:bg-primary/10 hover:text-primary transition-colors" data-testid="upload-image-btn"><Image className="h-4 w-4" /> صورة</button>
            <button onClick={()=>videoRef.current?.click()} className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-muted/50 text-xs text-muted-foreground hover:bg-primary/10 hover:text-primary transition-colors" data-testid="upload-video-btn"><Video className="h-4 w-4" /> فيديو</button>
          </div>
          <p className="text-xs font-bold text-muted-foreground mb-2">الفئة:</p>
          <div className="flex flex-wrap gap-2">
            {categories.map(c=>(<button key={c.key} onClick={()=>setCategory(c.key)} data-testid={`cat-${c.key}`} className={cn('px-4 py-2 rounded-full text-xs font-bold transition-all', category===c.key ? 'bg-primary text-primary-foreground' : 'bg-muted/50 text-muted-foreground')}>{c.label}</button>))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

/* ========== MAIN SOHBA PAGE ========== */
export default function Sohba() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('all');
  const [posts, setPosts] = useState<Post[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [commentPost, setCommentPost] = useState<Post | null>(null);
  const [giftPost, setGiftPost] = useState<Post | null>(null);
  const [profileUserId, setProfileUserId] = useState<string | null>(null);

  useEffect(() => { fetch(`${BACKEND_URL}/api/sohba/categories`).then(r=>r.json()).then(d=>setCategories(d.categories||[])).catch(()=>{}); }, []);

  const loadPosts = useCallback(async (cat: string) => {
    setLoading(true);
    const h: any = {}; const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
    try { const r = await fetch(`${BACKEND_URL}/api/sohba/posts?category=${cat}&limit=50`, { headers: h }); const d = await r.json(); setPosts(d.posts || []); } catch {}
    setLoading(false);
  }, []);

  useEffect(() => { loadPosts(activeTab); }, [activeTab, loadPosts]);

  const toggleLike = async (id: string) => {
    if (!user) { toast.error('سجّل دخولك'); return; }
    try { const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/like`, { method: 'POST', headers: authHeaders() }); const d = await r.json(); setPosts(p => p.map(x => x.id === id ? { ...x, liked: d.liked, likes_count: x.likes_count + (d.liked ? 1 : -1) } : x)); } catch {}
  };

  const toggleSave = async (id: string) => {
    if (!user) { toast.error('سجّل دخولك'); return; }
    try { const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/save`, { method: 'POST', headers: authHeaders() }); const d = await r.json(); setPosts(p => p.map(x => x.id === id ? { ...x, saved: d.saved } : x)); } catch {}
  };

  const allTabs = [{ key: 'all', label: 'الكل' }, { key: 'live', label: '🔴 مباشر' }, ...categories];

  return (
    <div className="h-screen flex flex-col bg-black" dir="rtl" data-testid="sohba-page">
      {/* Top tabs */}
      <div className="sticky top-0 z-40 bg-black/80 backdrop-blur-xl pt-safe-header">
        <div className="flex gap-1 px-3 py-2 overflow-x-auto no-scrollbar">
          {allTabs.map(tab => (
            <button key={tab.key} onClick={() => setActiveTab(tab.key)} data-testid={`sohba-tab-${tab.key}`}
              className={cn('shrink-0 px-3 py-1.5 rounded-full text-xs font-bold transition-all',
                activeTab === tab.key ? 'bg-white text-black' : 'text-white/60')}>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Feed - Snap Scroll */}
      {loading && posts.length === 0 ? (
        <div className="flex-1 flex items-center justify-center"><Loader2 className="h-8 w-8 animate-spin text-white" /></div>
      ) : posts.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-center px-8">
          <div>
            <User className="h-14 w-14 text-white/15 mx-auto mb-3" />
            <p className="text-base font-bold text-white/60">لا توجد منشورات بعد</p>
            {user && <button onClick={() => setShowCreate(true)} className="mt-4 bg-white text-black px-6 py-2.5 rounded-2xl text-sm font-bold" data-testid="first-post-btn">أنشئ أول منشور</button>}
          </div>
        </div>
      ) : (
        <div className="flex-1 overflow-y-scroll snap-y snap-mandatory">
          {posts.map(post => (
            <FullScreenPost key={post.id} post={post}
              onLike={() => toggleLike(post.id)}
              onSave={() => toggleSave(post.id)}
              onOpenComments={() => setCommentPost(post)}
              onOpenGifts={() => { if (!user) { toast.error('سجّل دخولك'); return; } setGiftPost(post); }}
              onOpenProfile={() => setProfileUserId(post.author_id)}
              onShare={() => { navigator.clipboard?.writeText(`${window.location.origin}/sohba/${post.id}`).then(() => toast.success('تم نسخ الرابط')); }}
            />
          ))}
        </div>
      )}

      {/* Create FAB */}
      <button data-testid="create-post-btn"
        onClick={() => { if (!user) { toast.error('سجّل دخولك'); navigate('/auth'); return; } setShowCreate(true); }}
        className="fixed bottom-20 left-1/2 -translate-x-1/2 z-40 h-12 px-5 rounded-full bg-primary text-primary-foreground shadow-lg shadow-primary/30 flex items-center justify-center gap-2 active:scale-90 transition-transform">
        <Plus className="h-5 w-5" /><span className="text-sm font-bold">إنشاء</span>
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
