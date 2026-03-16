import { useState, useEffect, useCallback, useRef } from 'react';
import { Search, X, Loader2, Heart, MessageCircle, Play, TrendingUp, Hash, Grid3X3, Users, Compass, Flame, Sparkles, BookOpen, Mic, Star, Eye } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';
function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

interface Post {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  content: string; category: string; image_url?: string; media_type?: string;
  created_at: string; likes_count: number; comments_count: number;
  shares_count: number; liked: boolean; saved: boolean; engagement_score?: number;
}
interface UserResult { id: string; name: string; email: string; avatar?: string; followers_count: number; posts_count: number; }

const avatarColors = ['bg-emerald-600','bg-blue-600','bg-amber-600','bg-purple-600','bg-rose-600','bg-teal-600','bg-indigo-600','bg-cyan-600'];

const quickCategories = [
  { key: 'quran', label: 'قرآن', icon: BookOpen, color: 'from-emerald-500 to-teal-600' },
  { key: 'hadith', label: 'حديث', icon: Star, color: 'from-amber-500 to-orange-600' },
  { key: 'dua', label: 'دعاء', icon: Sparkles, color: 'from-purple-500 to-violet-600' },
  { key: 'general', label: 'عام', icon: Compass, color: 'from-blue-500 to-indigo-600' },
  { key: 'live', label: 'مباشر', icon: Flame, color: 'from-red-500 to-rose-600' },
];

/* ========== POST CARD — Bento Grid ========== */
function BentoPostCard({ post, size = 'sm' }: { post: Post; size?: 'sm' | 'md' | 'lg' }) {
  const rawUrl = post.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('http') ? rawUrl : `${BACKEND_URL}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`) : null;
  const isVideo = post.media_type === 'video' || (mediaUrl && /\.(mp4|webm|mov)/i.test(mediaUrl));
  const [imgOk, setImgOk] = useState(true);
  const navigate = useNavigate();

  const aspectClass = size === 'lg' ? 'row-span-2 aspect-[3/4]' : size === 'md' ? 'aspect-[4/5]' : 'aspect-square';

  return (
    <button onClick={() => navigate(`/sohba?post=${post.id}`)}
      className={cn('relative rounded-2xl overflow-hidden group', aspectClass)} data-testid={`explore-card-${post.id}`}>
      {mediaUrl && imgOk ? (
        <>
          <img src={mediaUrl} alt="" className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
            loading="lazy" onError={() => setImgOk(false)} />
          {isVideo && (
            <div className="absolute top-2.5 right-2.5 bg-black/50 rounded-full p-1.5 backdrop-blur-sm">
              <Play className="h-3 w-3 text-white fill-white" />
            </div>
          )}
        </>
      ) : (
        <div className={cn('w-full h-full flex items-center justify-center p-4',
          post.category === 'quran' ? 'bg-gradient-to-br from-emerald-900/90 to-emerald-950' :
          post.category === 'hadith' ? 'bg-gradient-to-br from-amber-900/90 to-amber-950' :
          post.category === 'dua' ? 'bg-gradient-to-br from-purple-900/90 to-purple-950' :
          'bg-gradient-to-br from-slate-800 to-slate-900')}>
          <p className={cn('text-white/90 text-center leading-relaxed', size === 'lg' ? 'text-sm' : 'text-[10px] line-clamp-5')}
            dir="rtl" style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>{post.content}</p>
        </div>
      )}

      {/* Bottom overlay */}
      <div className="absolute inset-x-0 bottom-0 p-2.5"
        style={{ background: 'linear-gradient(to top, rgba(0,0,0,.7) 0%, transparent 100%)' }}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1.5 min-w-0">
            <div className={cn('h-5 w-5 rounded-full flex items-center justify-center text-[7px] text-white font-bold shrink-0',
              avatarColors[(post.author_name||'').charCodeAt(0) % avatarColors.length])}>
              {post.author_name?.[0] || '؟'}
            </div>
            <span className="text-[10px] text-white/90 font-medium truncate">{post.author_name}</span>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <span className="flex items-center gap-0.5 text-[9px] text-white/70">
              <Heart className="h-2.5 w-2.5" />{post.likes_count || 0}
            </span>
          </div>
        </div>
      </div>
    </button>
  );
}

/* ========== USER CARD ========== */
function UserBubble({ user: u }: { user: UserResult }) {
  const ci = (u.name || '').charCodeAt(0) % avatarColors.length;
  return (
    <Link to={`/sohba?profile=${u.id}`} className="flex flex-col items-center gap-1.5 shrink-0 w-[68px]">
      <div className={cn('h-14 w-14 rounded-full flex items-center justify-center text-sm text-white font-bold border-2 border-primary/40 shadow-lg shadow-primary/10', avatarColors[ci])}>
        {u.avatar ? <img src={u.avatar} className="h-full w-full rounded-full object-cover" alt="" /> : (u.name?.[0] || '؟')}
      </div>
      <span className="text-[10px] text-foreground font-medium truncate w-full text-center">{u.name}</span>
      <span className="text-[8px] text-muted-foreground">{u.followers_count} متابع</span>
    </Link>
  );
}

/* ========== MAIN EXPLORE PAGE ========== */
export default function Explore() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState<'all' | 'posts' | 'users'>('all');
  const [explorePosts, setExplorePosts] = useState<Post[]>([]);
  const [searchResults, setSearchResults] = useState<{ posts: Post[]; users: UserResult[] } | null>(null);
  const [trendingUsers, setTrendingUsers] = useState<UserResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [isSearchActive, setIsSearchActive] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const searchTimer = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => { loadExplore(); loadTrendingUsers(); }, []);

  const loadExplore = async () => {
    setLoading(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/explore?limit=50`, { headers: authHeaders() });
      const d = await r.json(); setExplorePosts(d.posts || []);
    } catch {} setLoading(false);
  };

  const loadTrendingUsers = async () => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/trending-users?limit=15`, { headers: authHeaders() });
      const d = await r.json(); setTrendingUsers(d.users || []);
    } catch {}
  };

  const doSearch = useCallback(async (q: string, type: string) => {
    if (!q.trim()) { setSearchResults(null); return; }
    setSearching(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/search?q=${encodeURIComponent(q)}&type=${type}&limit=50`, { headers: authHeaders() });
      const d = await r.json();
      setSearchResults({ posts: d.posts || [], users: d.users || [] });
    } catch { setSearchResults({ posts: [], users: [] }); }
    setSearching(false);
  }, []);

  const handleSearchInput = (val: string) => {
    setSearchQuery(val);
    if (searchTimer.current) clearTimeout(searchTimer.current);
    searchTimer.current = setTimeout(() => doSearch(val, searchType), 400);
  };

  const clearSearch = () => { setSearchQuery(''); setSearchResults(null); setIsSearchActive(false); searchInputRef.current?.blur(); };

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="explore-page">

      {/* ===== HEADER ===== */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl">
        <div className="px-4 pt-3 pb-2">
          <div className="flex items-center gap-2">
            {!isSearchActive && <h1 className="text-xl font-black text-foreground shrink-0">استكشف</h1>}
            <div className={cn('relative transition-all', isSearchActive ? 'flex-1' : 'flex-1')}>
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
              <input ref={searchInputRef} type="search" dir="auto" value={searchQuery}
                onChange={e => handleSearchInput(e.target.value)}
                onFocus={() => setIsSearchActive(true)}
                placeholder="ابحث عن محتوى، أشخاص..." data-testid="explore-search-input"
                className="w-full h-10 rounded-2xl bg-muted/60 border border-border/30 pr-10 pl-10 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-all"
                style={{ unicodeBidi: 'plaintext' } as any} autoComplete="off" spellCheck={false} />
              {searchQuery && (
                <button onClick={clearSearch} className="absolute left-3 top-1/2 -translate-y-1/2 p-0.5 rounded-full bg-muted-foreground/20">
                  <X className="h-3 w-3 text-muted-foreground" />
                </button>
              )}
            </div>
            {isSearchActive && <button onClick={clearSearch} className="text-sm text-primary font-bold shrink-0">إلغاء</button>}
          </div>
        </div>

        {/* Quick Categories (hidden during search) */}
        {!isSearchActive && (
          <div className="px-4 pb-3 flex gap-2 overflow-x-auto no-scrollbar">
            {quickCategories.map(cat => (
              <button key={cat.key} onClick={() => navigate(`/sohba`)}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-2xl bg-card border border-border/30 shrink-0 active:scale-95 transition-transform">
                <div className={cn('h-6 w-6 rounded-lg bg-gradient-to-br flex items-center justify-center', cat.color)}>
                  <cat.icon className="h-3 w-3 text-white" />
                </div>
                <span className="text-xs font-bold text-foreground">{cat.label}</span>
              </button>
            ))}
          </div>
        )}

        {/* Search Tabs */}
        {isSearchActive && searchQuery && (
          <div className="px-4 pb-2 flex gap-2">
            {([
              { key: 'all', label: 'الكل', icon: Grid3X3 },
              { key: 'posts', label: 'منشورات', icon: Hash },
              { key: 'users', label: 'أشخاص', icon: Users },
            ] as const).map(t => (
              <button key={t.key} onClick={() => { setSearchType(t.key); doSearch(searchQuery, t.key); }}
                className={cn('flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-bold transition-all',
                  searchType === t.key ? 'bg-primary text-primary-foreground' : 'bg-muted/60 text-muted-foreground')}>
                <t.icon className="h-3 w-3" />{t.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* ===== CONTENT ===== */}
      {searchResults ? (
        /* Search Results */
        <div className="px-4 py-3">
          {searching ? (
            <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
          ) : (
            <>
              {searchResults.users.length > 0 && (searchType === 'all' || searchType === 'users') && (
                <div className="mb-5">
                  <h3 className="text-sm font-bold text-foreground mb-3 flex items-center gap-2">
                    <Users className="h-4 w-4 text-primary" />أشخاص
                  </h3>
                  <div className="space-y-2">
                    {searchResults.users.map(u => {
                      const ci = (u.name||'').charCodeAt(0) % avatarColors.length;
                      return (
                        <Link key={u.id} to={`/sohba?profile=${u.id}`}
                          className="flex items-center gap-3 p-3 rounded-2xl bg-card border border-border/30 active:scale-[0.98] transition-all">
                          <div className={cn('h-11 w-11 rounded-full flex items-center justify-center text-sm text-white font-bold shrink-0', avatarColors[ci])}>
                            {u.avatar ? <img src={u.avatar} className="h-full w-full rounded-full object-cover" alt="" /> : (u.name?.[0] || '؟')}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-bold text-foreground truncate">{u.name || 'مستخدم'}</p>
                            <p className="text-[11px] text-muted-foreground">{u.followers_count} متابع • {u.posts_count} منشور</p>
                          </div>
                        </Link>
                      );
                    })}
                  </div>
                </div>
              )}

              {searchResults.posts.length > 0 && (searchType === 'all' || searchType === 'posts') && (
                <div>
                  <h3 className="text-sm font-bold text-foreground mb-3 flex items-center gap-2">
                    <Hash className="h-4 w-4 text-primary" />منشورات
                  </h3>
                  <div className="grid grid-cols-3 gap-1 rounded-xl overflow-hidden">
                    {searchResults.posts.map(p => <BentoPostCard key={p.id} post={p} size="sm" />)}
                  </div>
                </div>
              )}

              {searchResults.posts.length === 0 && searchResults.users.length === 0 && (
                <div className="text-center py-20">
                  <Search className="h-14 w-14 text-muted-foreground/20 mx-auto mb-4" />
                  <p className="text-base font-bold text-muted-foreground/60">لا توجد نتائج</p>
                  <p className="text-xs text-muted-foreground/40 mt-1">جرّب كلمات مختلفة</p>
                </div>
              )}
            </>
          )}
        </div>
      ) : (
        /* Explore Feed */
        <div className="px-3">
          {/* Trending Users */}
          {trendingUsers.length > 0 && (
            <div className="mb-5">
              <h3 className="text-sm font-bold text-foreground mb-3 px-1 flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-primary" />بارزون
              </h3>
              <div className="flex gap-3 overflow-x-auto no-scrollbar pb-2 px-1">
                {trendingUsers.map(u => <UserBubble key={u.id} user={u} />)}
              </div>
            </div>
          )}

          {/* Bento Grid Posts */}
          {loading ? (
            <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>
          ) : explorePosts.length === 0 ? (
            <div className="text-center py-20 px-8">
              <Compass className="h-16 w-16 text-muted-foreground/15 mx-auto mb-4" />
              <p className="text-base font-bold text-muted-foreground/50">لا يوجد محتوى بعد</p>
              <p className="text-xs text-muted-foreground/30 mt-1">كن أول من ينشر!</p>
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-1 rounded-xl overflow-hidden">
              {explorePosts.map((p, i) => (
                <BentoPostCard key={p.id} post={p} size={i === 0 ? 'lg' : i % 7 === 3 ? 'md' : 'sm'} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
