import { useState, useEffect, useCallback, useRef } from 'react';
import { Heart, MessageCircle, Send, Bookmark, X, Loader2, Image, Video, Share2, User, Play, Pause, Music2, Plus, Gift, Radio } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
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

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken();
  if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

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

/* ========================================================== */
/*  FULL-SCREEN POST — TikTok-style with VISIBLE text always  */
/* ========================================================== */
function FullScreenPost({ post, onLike, onSave, onOpenComments, onOpenGifts, onOpenProfile, onShare, isActive }: {
  post: Post; onLike: () => void; onSave: () => void; onOpenComments: () => void;
  onOpenGifts: () => void; onOpenProfile: () => void; onShare: () => void; isActive?: boolean;
}) {
  const ci = (post.author_name || '').charCodeAt(0) % avatarColors.length;
  const rawUrl = post.image_url;
  const mediaUrl = rawUrl
    ? (rawUrl.startsWith('http') ? rawUrl : `${BACKEND_URL}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`)
    : null;
  const isVideo = post.media_type === 'video' || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));
  const videoRef = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(true);
  const [showFullCaption, setShowFullCaption] = useState(false);
  const [imgError, setImgError] = useState(false);
  const [showHeart, setShowHeart] = useState(false);
  const lastTap = useRef(0);

  // pause/play based on visibility
  useEffect(() => {
    if (!videoRef.current) return;
    if (isActive) { videoRef.current.play().catch(() => {}); setPlaying(true); }
    else { videoRef.current.pause(); setPlaying(false); }
  }, [isActive]);

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (videoRef.current.paused) { videoRef.current.play(); setPlaying(true); }
    else { videoRef.current.pause(); setPlaying(false); }
  };

  const handleDoubleTap = () => {
    if (!post.liked) onLike();
    setShowHeart(true);
    setTimeout(() => setShowHeart(false), 800);
  };

  const handleTap = () => {
    const now = Date.now();
    if (now - lastTap.current < 300) handleDoubleTap();
    else if (isVideo) togglePlay();
    lastTap.current = now;
  };

  // decide whether to show visual media
  const hasMedia = mediaUrl && !imgError;
  const showAsVideo = hasMedia && isVideo;
  const showAsImage = hasMedia && !isVideo;

  return (
    <div className="relative w-full bg-black flex-shrink-0" style={{ height: '100dvh' }} data-testid={`post-${post.id}`}>

      {/* ——— Media / Content Background ——— */}
      <div className="absolute inset-0" onClick={handleTap}>
        {showAsVideo ? (
          <video ref={videoRef} src={mediaUrl!} className="w-full h-full object-cover" loop muted playsInline autoPlay
            onError={() => setImgError(true)} />
        ) : showAsImage ? (
          <img src={mediaUrl!} alt="" className="w-full h-full object-cover"
            loading="lazy" onError={() => setImgError(true)} />
        ) : (
          /* TEXT-ONLY post — always visible */
          <div className="w-full h-full flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, #064e3b 0%, #0c0c0c 40%, #064e3b 100%)' }}>
            <p className="text-[22px] text-white leading-[2.2] text-center px-8 max-w-md"
              style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif", textShadow: '0 2px 12px rgba(0,0,0,.6)' }}
              dir="rtl">{post.content}</p>
          </div>
        )}

        {/* bottom gradient — always present for readable text */}
        <div className="absolute inset-x-0 bottom-0 pointer-events-none"
          style={{ height: '55%', background: 'linear-gradient(to top, rgba(0,0,0,.85) 0%, rgba(0,0,0,.35) 50%, transparent 100%)' }} />
        {/* top gradient */}
        <div className="absolute inset-x-0 top-0 h-28 pointer-events-none"
          style={{ background: 'linear-gradient(to bottom, rgba(0,0,0,.5), transparent)' }} />
      </div>

      {/* ——— Double-tap heart ——— */}
      <AnimatePresence>
        {showHeart && (
          <motion.div initial={{ opacity: 0, scale: .2 }} animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.5 }} className="absolute inset-0 flex items-center justify-center z-30 pointer-events-none">
            <Heart className="h-28 w-28 text-red-500 fill-red-500 drop-shadow-2xl" />
          </motion.div>
        )}
      </AnimatePresence>

      {/* ——— Pause icon ——— */}
      {showAsVideo && !playing && (
        <div className="absolute inset-0 flex items-center justify-center z-20 pointer-events-none">
          <div className="h-16 w-16 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center">
            <Play className="h-8 w-8 text-white fill-white ml-1" />
          </div>
        </div>
      )}

      {/* ===== RIGHT SIDE ACTION BUTTONS (TikTok style) ===== */}
      <div className="absolute left-3 bottom-28 flex flex-col items-center gap-5 z-20">
        {/* Avatar */}
        <button onClick={(e) => { e.stopPropagation(); onOpenProfile(); }} className="relative mb-1">
          <div className={cn('h-12 w-12 rounded-full flex items-center justify-center text-sm text-white font-bold border-2 border-white shadow-lg', avatarColors[ci])}>
            {post.author_avatar
              ? <img src={post.author_avatar} className="h-full w-full rounded-full object-cover" alt="" />
              : (post.author_name?.[0] || '؟')}
          </div>
          <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 h-5 w-5 rounded-full bg-primary flex items-center justify-center border border-white">
            <Plus className="h-3 w-3 text-white" />
          </div>
        </button>

        {/* Like */}
        <button onClick={(e) => { e.stopPropagation(); onLike(); }} className="flex flex-col items-center gap-0.5"
          data-testid={`like-${post.id}`}>
          <div className="h-11 w-11 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
            <Heart className={cn('h-7 w-7 transition-all', post.liked ? 'text-red-500 fill-red-500 scale-110' : 'text-white')} />
          </div>
          <span className="text-[11px] text-white font-bold tabular-nums">{post.likes_count || ''}</span>
        </button>

        {/* Comment */}
        <button onClick={(e) => { e.stopPropagation(); onOpenComments(); }} className="flex flex-col items-center gap-0.5"
          data-testid={`comments-${post.id}`}>
          <div className="h-11 w-11 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
            <MessageCircle className="h-7 w-7 text-white" />
          </div>
          <span className="text-[11px] text-white font-bold tabular-nums">{post.comments_count || ''}</span>
        </button>

        {/* Bookmark */}
        <button onClick={(e) => { e.stopPropagation(); onSave(); }} className="flex flex-col items-center gap-0.5"
          data-testid={`save-${post.id}`}>
          <div className="h-11 w-11 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
            <Bookmark className={cn('h-6 w-6 transition-all', post.saved ? 'text-amber-400 fill-amber-400' : 'text-white')} />
          </div>
        </button>

        {/* Share */}
        <button onClick={(e) => { e.stopPropagation(); onShare(); }} className="flex flex-col items-center gap-0.5">
          <div className="h-11 w-11 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
            <Share2 className="h-6 w-6 text-white" />
          </div>
        </button>

        {/* Gift */}
        <button onClick={(e) => { e.stopPropagation(); onOpenGifts(); }} className="flex flex-col items-center">
          <div className="h-11 w-11 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
            <Gift className="h-6 w-6 text-white" />
          </div>
        </button>

        {/* Spinning disc */}
        <div className="h-10 w-10 rounded-full border-2 border-white/30 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center"
          style={{ animation: 'spin 4s linear infinite' }}>
          <Music2 className="h-4 w-4 text-white/60" />
        </div>
      </div>

      {/* ===== BOTTOM — Author & caption (always visible) ===== */}
      <div className="absolute bottom-6 right-3 z-20 pointer-events-none" style={{ left: '70px' }} dir="rtl">
        <div className="flex items-center gap-2 mb-2 pointer-events-auto">
          <span className="text-[15px] font-bold text-white" style={{ textShadow: '0 1px 6px rgba(0,0,0,.7)' }}>
            @{post.author_name}
          </span>
          {post.category && post.category !== 'general' && (
            <span className="text-[10px] bg-white/15 text-white/80 px-2 py-0.5 rounded-full backdrop-blur-sm">{post.category}</span>
          )}
          <span className="text-[10px] text-white/50">{timeAgo(post.created_at)}</span>
        </div>

        {/* Caption — always visible if media exists */}
        {(hasMedia && post.content) && (
          <div className="pointer-events-auto">
            <p className={cn("text-[13px] text-white/90 leading-relaxed", !showFullCaption && "line-clamp-2")}
              style={{ textShadow: '0 1px 4px rgba(0,0,0,.5)' }} dir="rtl">{post.content}</p>
            {post.content.length > 60 && (
              <button onClick={() => setShowFullCaption(!showFullCaption)} className="text-[11px] text-white/50 mt-0.5">
                {showFullCaption ? 'أقل' : '...المزيد'}
              </button>
            )}
          </div>
        )}
      </div>

      {/* LIVE badge */}
      {post.category === 'live' && (
        <div className="absolute top-14 right-4 z-20 flex items-center gap-1.5 bg-red-600 rounded-lg px-2.5 py-1 shadow-lg">
          <Radio className="h-3.5 w-3.5 text-white animate-pulse" /><span className="text-[11px] text-white font-bold">مباشر</span>
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
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`)
      .then(r => r.json()).then(d => { setComments(d.comments || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [post.id]);

  const send = async () => {
    if (!text.trim()) return;
    setSending(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/comments`, {
        method: 'POST', headers: authHeaders(), body: JSON.stringify({ content: text.trim() })
      });
      if (r.status === 401) { toast.error('سجّل دخولك'); setSending(false); return; }
      const d = await r.json();
      if (d.comment) { setComments(p => [...p, d.comment]); setText(''); }
    } catch { toast.error('خطأ'); }
    setSending(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[70vh] flex flex-col shadow-2xl">
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
              const cci = (c.author_name || '').charCodeAt(0) % avatarColors.length;
              return (
                <div key={c.id} className="flex gap-2.5">
                  <div className={cn('h-8 w-8 rounded-full flex items-center justify-center text-[10px] text-white font-bold shrink-0', avatarColors[cci])}>
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
            dir="auto" placeholder="اكتب تعليقاً..." data-testid="comment-input"
            className="flex-1 bg-muted/50 rounded-2xl px-4 py-2.5 text-sm outline-none text-foreground placeholder:text-muted-foreground" />
          <button onClick={send} disabled={!text.trim() || sending} data-testid="send-comment-btn"
            className="h-10 w-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center shrink-0 disabled:opacity-40 active:scale-90 transition-transform">
            {sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </button>
        </div>
      </div>
    </motion.div>
  );
}

/* ========== GIFTS SHEET ========== */
function GiftsSheet({ post, onClose }: { post: Post; onClose: () => void }) {
  const [gifts, setGifts] = useState<any[]>([]);
  const [sending, setSending] = useState('');
  useEffect(() => { fetch(`${BACKEND_URL}/api/gifts/list`).then(r => r.json()).then(d => setGifts(d.gifts || [])).catch(() => {}); }, []);
  const sendGift = async (gift: any) => {
    setSending(gift.id);
    try {
      const r = await fetch(`${BACKEND_URL}/api/gifts/send`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ gift_id: gift.id, recipient_id: post.author_id, post_id: post.id }) });
      const d = await r.json();
      if (r.ok) { toast.success(d.message || 'تم إرسال الهدية'); onClose(); } else toast.error(d.detail || 'فشل');
    } catch { toast.error('خطأ'); }
    setSending('');
  };
  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/60" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[50vh] flex flex-col">
        <div className="flex justify-center pt-2 pb-1"><div className="w-10 h-1 rounded-full bg-muted-foreground/30" /></div>
        <div className="flex items-center justify-between px-5 py-2 border-b border-border/20">
          <div><span className="text-sm font-bold">إرسال هدية</span><p className="text-[10px] text-muted-foreground">لـ {post.author_name}</p></div>
          <button onClick={onClose}><X className="h-5 w-5 text-muted-foreground" /></button>
        </div>
        <div className="flex-1 overflow-y-auto px-4 py-3">
          {gifts.length === 0 ? (
            <p className="text-center text-xs text-muted-foreground py-8">لا توجد هدايا حالياً</p>
          ) : (
            <div className="grid grid-cols-4 gap-3">
              {gifts.map((g: any) => (
                <button key={g.id} onClick={() => sendGift(g)} disabled={sending === g.id}
                  className="flex flex-col items-center gap-1.5 p-3 rounded-2xl bg-muted/50 hover:bg-primary/10 active:scale-90 transition-all">
                  <span className="text-3xl">{g.emoji}</span>
                  <span className="text-[10px] font-bold">{g.name}</span>
                </button>
              ))}
            </div>
          )}
        </div>
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
    const h: Record<string, string> = {}; const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
    fetch(`${BACKEND_URL}/api/sohba/profile/${userId}`, { headers: h }).then(r => r.json())
      .then(d => { setProfile(d.profile); setStats(d.stats); setIsFollowing(d.is_following); }).catch(() => {});
    fetch(`${BACKEND_URL}/api/sohba/posts?author=${userId}&limit=30`, { headers: { ...h, 'Content-Type': 'application/json' } })
      .then(r => r.json()).then(d => setPosts(d.posts || [])).catch(() => {});
  }, [userId]);

  const toggleFollow = async () => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/follow/${userId}`, { method: 'POST', headers: authHeaders() });
      if (r.status === 401) { toast.error('سجّل دخولك'); return; }
      const d = await r.json();
      setIsFollowing(d.following);
      setStats((prev: any) => ({ ...prev, followers_count: (prev.followers_count || 0) + (d.following ? 1 : -1) }));
    } catch {}
  };

  if (!profile) return (
    <motion.div initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }}
      className="fixed inset-0 z-[999] bg-background flex items-center justify-center">
      <Loader2 className="h-6 w-6 animate-spin text-primary" />
    </motion.div>
  );

  const ci = (profile.name || '').charCodeAt(0) % avatarColors.length;
  return (
    <motion.div initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="fixed inset-0 z-[999] bg-background" dir="rtl">
      <div className="h-full overflow-y-auto pb-20">
        <div className="sticky top-0 z-10 bg-background/95 backdrop-blur-xl flex items-center justify-between px-4 h-12 border-b border-border/20">
          <span className="text-base font-bold">{profile.name}</span>
          <button onClick={onClose} className="p-2 rounded-full hover:bg-muted"><X className="h-5 w-5" /></button>
        </div>
        <div className="px-5 py-5">
          <div className="flex items-center gap-5">
            <div className={cn('h-20 w-20 rounded-full flex items-center justify-center text-2xl text-white font-bold border-[3px] border-primary/30 shrink-0', avatarColors[ci])}>
              {profile.avatar ? <img src={profile.avatar} className="h-full w-full rounded-full object-cover" alt="" /> : (profile.name?.[0] || '؟')}
            </div>
            <div className="flex-1 flex justify-around">
              <div className="text-center"><p className="text-lg font-bold">{stats.posts_count || 0}</p><p className="text-[11px] text-muted-foreground">منشور</p></div>
              <div className="text-center"><p className="text-lg font-bold">{stats.followers_count || 0}</p><p className="text-[11px] text-muted-foreground">متابع</p></div>
              <div className="text-center"><p className="text-lg font-bold">{stats.following_count || 0}</p><p className="text-[11px] text-muted-foreground">متابَع</p></div>
            </div>
          </div>
          <div className="mt-4 flex gap-2">
            <Button onClick={toggleFollow} variant={isFollowing ? 'outline' : 'default'} className="flex-1 rounded-xl h-9 text-sm font-bold">
              {isFollowing ? 'إلغاء المتابعة' : 'متابعة'}
            </Button>
          </div>
        </div>
        <div className="border-t border-border/20 pt-1">
          <div className="grid grid-cols-3 gap-0.5">
            {posts.map(p => {
              const url = p.image_url ? (p.image_url.startsWith('http') ? p.image_url : `${BACKEND_URL}${p.image_url}`) : null;
              return (
                <div key={p.id} className="aspect-square bg-muted overflow-hidden">
                  {url ? <img src={url} alt="" className="w-full h-full object-cover" loading="lazy" /> : (
                    <div className="w-full h-full flex items-center justify-center p-2 bg-gradient-to-br from-emerald-900/30 to-teal-900/30">
                      <p className="text-[9px] text-muted-foreground line-clamp-4 text-center" dir="rtl">{p.content}</p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          {posts.length === 0 && <div className="text-center py-16"><p className="text-sm text-muted-foreground">لا توجد منشورات</p></div>}
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
  const fileRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLInputElement>(null);

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
    if (!content.trim() && !imagePreview) { toast.error('اكتب شيئاً أو أضف صورة'); return; }
    setPosting(true);
    let uploadedUrl = '';
    if (imagePreview) {
      if (imagePreview.startsWith('data:')) {
        try {
          const r = await fetch(`${BACKEND_URL}/api/upload/file`, { method: 'POST', headers: authHeaders(), body: JSON.stringify({ data: imagePreview, filename: 'post.jpg' }) });
          const d = await r.json(); if (r.ok) uploadedUrl = d.url;
        } catch {}
      } else if (imagePreview.includes('/api/uploads/')) {
        uploadedUrl = imagePreview.replace(BACKEND_URL, '');
      }
    }
    try {
      const body: any = { content: content.trim() || 'منشور جديد', category };
      if (uploadedUrl) body.image_url = uploadedUrl;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(body) });
      if (r.status === 401) { toast.error('سجّل دخولك'); setPosting(false); return; }
      const d = await r.json();
      if (d.post) { onCreated(d.post); toast.success('تم النشر!'); onClose(); }
    } catch { toast.error('خطأ في النشر'); }
    setPosting(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="fixed inset-0 z-[999] flex flex-col" dir="rtl">
      <div className="flex-1 bg-black/60" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[85vh] flex flex-col border-t border-border/30">
        <div className="flex items-center justify-between p-4 border-b border-border/20">
          <button onClick={onClose} className="text-sm text-muted-foreground font-medium">إلغاء</button>
          <h3 className="text-sm font-bold">منشور جديد</h3>
          <button onClick={submit} disabled={(!content.trim() && !imagePreview) || posting}
            className="text-sm font-bold text-primary disabled:opacity-40" data-testid="submit-post-btn">
            {posting ? <Loader2 className="h-4 w-4 animate-spin" /> : 'نشر'}
          </button>
        </div>
        <div className="p-4 flex-1 overflow-y-auto">
          <textarea value={content} onChange={e => setContent(e.target.value)} dir="auto" autoFocus
            placeholder="شارك فكرة، آية، حديث، أو دعاء..." data-testid="post-content-input"
            className="w-full h-28 bg-transparent resize-none outline-none text-sm leading-relaxed text-foreground placeholder:text-muted-foreground" />
          {imagePreview && (
            <div className="relative mb-3 rounded-xl overflow-hidden">
              <img src={imagePreview} alt="" className="w-full max-h-48 object-cover rounded-xl" />
              <button onClick={() => setImagePreview(null)} className="absolute top-2 left-2 p-1.5 rounded-full bg-black/60 text-white">
                <X className="h-3.5 w-3.5" />
              </button>
            </div>
          )}
          <div className="flex gap-2 mt-2 mb-4">
            <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
            <input ref={videoRef} type="file" accept="video/*" className="hidden" onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
            <button onClick={() => fileRef.current?.click()} data-testid="upload-image-btn"
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-muted/50 text-xs text-muted-foreground hover:bg-primary/10 hover:text-primary transition-colors">
              <Image className="h-4 w-4" /> صورة
            </button>
            <button onClick={() => videoRef.current?.click()} data-testid="upload-video-btn"
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-muted/50 text-xs text-muted-foreground hover:bg-primary/10 hover:text-primary transition-colors">
              <Video className="h-4 w-4" /> فيديو
            </button>
          </div>
          <p className="text-xs font-bold text-muted-foreground mb-2">الفئة:</p>
          <div className="flex flex-wrap gap-2">
            {categories.map((c: any) => (
              <button key={c.key} onClick={() => setCategory(c.key)} data-testid={`cat-${c.key}`}
                className={cn('px-3.5 py-2 rounded-full text-xs font-bold transition-all',
                  category === c.key ? 'bg-primary text-primary-foreground shadow-md' : 'bg-muted/50 text-muted-foreground')}>
                {c.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

/* ========================================================== */
/*  MAIN SOHBA PAGE                                           */
/* ========================================================== */
export default function Sohba() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState('all');
  const [posts, setPosts] = useState<Post[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [commentPost, setCommentPost] = useState<Post | null>(null);
  const [giftPost, setGiftPost] = useState<Post | null>(null);
  const [profileUserId, setProfileUserId] = useState<string | null>(null);
  const [activePostIndex, setActivePostIndex] = useState(0);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const profileId = searchParams.get('profile');
    if (profileId) setProfileUserId(profileId);
    const shouldCreate = searchParams.get('create');
    if (shouldCreate === 'true' && user) setShowCreate(true);
  }, [searchParams, user]);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/categories`).then(r => r.json())
      .then(d => setCategories(d.categories || [])).catch(() => {});
  }, []);

  const loadPosts = useCallback(async (cat: string) => {
    setLoading(true);
    const h: Record<string, string> = { 'Content-Type': 'application/json' };
    const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts?category=${cat}&limit=50`, { headers: h });
      const d = await r.json();
      setPosts(d.posts || []);
    } catch {}
    setLoading(false);
  }, []);

  useEffect(() => { loadPosts(activeTab); }, [activeTab, loadPosts]);

  // Track which post is visible
  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;
    const observer = new IntersectionObserver(
      entries => entries.forEach(entry => {
        if (entry.isIntersecting) {
          const idx = parseInt(entry.target.getAttribute('data-index') || '0');
          setActivePostIndex(idx);
        }
      }),
      { root: container, threshold: 0.6 }
    );
    container.querySelectorAll('[data-index]').forEach(el => observer.observe(el));
    return () => observer.disconnect();
  }, [posts]);

  const toggleLike = async (id: string) => {
    if (!user) { toast.error('سجّل دخولك'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setPosts(p => p.map(x => x.id === id ? { ...x, liked: d.liked, likes_count: x.likes_count + (d.liked ? 1 : -1) } : x));
    } catch {}
  };

  const toggleSave = async (id: string) => {
    if (!user) { toast.error('سجّل دخولك'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/save`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setPosts(p => p.map(x => x.id === id ? { ...x, saved: d.saved } : x));
    } catch {}
  };

  const allTabs = [
    { key: 'all', label: 'لك' },
    { key: 'following', label: 'متابعين' },
    { key: 'live', label: 'مباشر' },
  ];

  return (
    <div className="flex flex-col bg-black" style={{ height: '100dvh' }} dir="rtl" data-testid="sohba-page">
      {/* Top tabs — TikTok style */}
      <div className="absolute top-0 left-0 right-0 z-40" style={{ paddingTop: 'env(safe-area-inset-top, 8px)' }}>
        <div className="flex items-center justify-center gap-6 px-4 py-3">
          {allTabs.map(tab => (
            <button key={tab.key} onClick={() => setActiveTab(tab.key)} data-testid={`sohba-tab-${tab.key}`}
              className="relative pb-1" style={{ whiteSpace: 'nowrap' }}>
              <span className={cn('text-[16px] font-bold transition-all',
                activeTab === tab.key ? 'text-white' : 'text-white/50')}>{tab.label}</span>
              {activeTab === tab.key && (
                <motion.div layoutId="tab-line" className="absolute bottom-0 left-1/2 -translate-x-1/2 h-[3px] w-8 bg-white rounded-full" />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Feed */}
      {loading && posts.length === 0 ? (
        <div className="flex-1 flex items-center justify-center"><Loader2 className="h-8 w-8 animate-spin text-white" /></div>
      ) : posts.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-center px-8">
          <div>
            <User className="h-14 w-14 text-white/15 mx-auto mb-3" />
            <p className="text-lg font-bold text-white/60">لا توجد منشورات بعد</p>
            <p className="text-sm text-white/30 mt-1">كن أول من ينشر!</p>
            {user && (
              <button onClick={() => setShowCreate(true)} data-testid="first-post-btn"
                className="mt-5 bg-white text-black px-8 py-3 rounded-2xl text-sm font-bold active:scale-95 transition-transform">
                أنشئ أول منشور
              </button>
            )}
          </div>
        </div>
      ) : (
        <div ref={scrollContainerRef} className="flex-1 overflow-y-scroll" style={{ scrollSnapType: 'y mandatory' }}>
          {posts.map((post, idx) => (
            <div key={post.id} data-index={idx} style={{ scrollSnapAlign: 'start', scrollSnapStop: 'always' }}>
              <FullScreenPost
                post={post}
                isActive={idx === activePostIndex}
                onLike={() => toggleLike(post.id)}
                onSave={() => toggleSave(post.id)}
                onOpenComments={() => setCommentPost(post)}
                onOpenGifts={() => { if (!user) { toast.error('سجّل دخولك'); return; } setGiftPost(post); }}
                onOpenProfile={() => setProfileUserId(post.author_id)}
                onShare={() => { navigator.clipboard?.writeText(`${window.location.origin}/sohba/${post.id}`).then(() => toast.success('تم نسخ الرابط')).catch(() => {}); }}
              />
            </div>
          ))}
        </div>
      )}

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
