import { useState, useEffect, useCallback, useRef } from 'react';
import { Search, X, Loader2, Heart, MessageCircle, Play, User, TrendingUp, Hash, Grid3X3, Users } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken();
  if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

interface Post {
  id: string; author_id: string; author_name: string; author_avatar?: string;
  content: string; category: string; image_url?: string; media_type?: string;
  created_at: string; likes_count: number; comments_count: number;
  shares_count: number; liked: boolean; saved: boolean;
}

interface UserResult {
  id: string; name: string; email: string; avatar?: string;
  followers_count: number; posts_count: number;
}

const avatarColors = ['bg-emerald-600', 'bg-blue-600', 'bg-amber-600', 'bg-purple-600', 'bg-rose-600', 'bg-teal-600'];

function timeAgo(iso: string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return 'الآن';
  if (m < 60) return `${m}د`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}س`;
  return `${Math.floor(h / 24)}ي`;
}

/* ========== GRID POST CARD ========== */
function GridPostCard({ post, onClick }: { post: Post; onClick: () => void }) {
  const rawUrl = post.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('/api/') ? `${BACKEND_URL}${rawUrl}` : rawUrl) : null;
  const isVideo = post.media_type === 'video' || (mediaUrl && /\.(mp4|webm|mov)/.test(mediaUrl));

  return (
    <button onClick={onClick} className="relative aspect-square rounded-xl overflow-hidden bg-muted/50 group" data-testid={`explore-post-${post.id}`}>
      {mediaUrl ? (
        <>
          <img src={mediaUrl} alt="" className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105" loading="lazy" />
          {isVideo && (
            <div className="absolute top-2 left-2 bg-black/50 rounded-full p-1">
              <Play className="h-3 w-3 text-white fill-white" />
            </div>
          )}
        </>
      ) : (
        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-emerald-900/40 to-teal-900/40 p-3">
          <p className="text-[10px] text-white/80 line-clamp-5 text-center leading-relaxed">{post.content}</p>
        </div>
      )}
      {/* Overlay on hover */}
      <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <Heart className="h-4 w-4 text-white fill-white" />
            <span className="text-xs text-white font-bold">{post.likes_count}</span>
          </div>
          <div className="flex items-center gap-1">
            <MessageCircle className="h-4 w-4 text-white fill-white" />
            <span className="text-xs text-white font-bold">{post.comments_count}</span>
          </div>
        </div>
      </div>
    </button>
  );
}

/* ========== USER CARD ========== */
function UserCard({ user: u }: { user: UserResult }) {
  const ci = (u.name || '').charCodeAt(0) % avatarColors.length;
  return (
    <Link to={`/sohba?profile=${u.id}`} className="flex items-center gap-3 p-3 rounded-2xl bg-card border border-border/30 active:scale-[0.98] transition-all">
      <div className={cn('h-12 w-12 rounded-full flex items-center justify-center text-sm text-white font-bold shrink-0', avatarColors[ci])}>
        {u.avatar ? <img src={u.avatar} className="h-full w-full rounded-full object-cover" alt="" /> : (u.name?.[0] || '؟')}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-bold text-foreground truncate">{u.name || 'مستخدم'}</p>
        <p className="text-[11px] text-muted-foreground">{u.followers_count} متابع • {u.posts_count} منشور</p>
      </div>
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
  const [isSearchFocused, setIsSearchFocused] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const searchTimeoutRef = useRef<ReturnType<typeof setTimeout>>();

  // Load explore feed
  useEffect(() => {
    loadExplore();
    loadTrendingUsers();
  }, []);

  const loadExplore = async () => {
    setLoading(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/explore?limit=50`, { headers: authHeaders() });
      const d = await r.json();
      setExplorePosts(d.posts || []);
    } catch {}
    setLoading(false);
  };

  const loadTrendingUsers = async () => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/trending-users?limit=10`, { headers: authHeaders() });
      const d = await r.json();
      setTrendingUsers(d.users || []);
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

  const handleSearchChange = (val: string) => {
    setSearchQuery(val);
    if (searchTimeoutRef.current) clearTimeout(searchTimeoutRef.current);
    searchTimeoutRef.current = setTimeout(() => {
      doSearch(val, searchType);
    }, 400);
  };

  const clearSearch = () => {
    setSearchQuery('');
    setSearchResults(null);
    setIsSearchFocused(false);
    searchInputRef.current?.blur();
  };

  const searchTabs = [
    { key: 'all', label: 'الكل', icon: Grid3X3 },
    { key: 'posts', label: 'منشورات', icon: Hash },
    { key: 'users', label: 'أشخاص', icon: Users },
  ];

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="explore-page">
      {/* Search Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 pt-safe-header pb-3">
        <div className="flex items-center gap-2">
          <div className="flex-1 relative">
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-muted-foreground" />
            <input
              ref={searchInputRef}
              type="search"
              dir="auto"
              value={searchQuery}
              onChange={e => handleSearchChange(e.target.value)}
              onFocus={() => setIsSearchFocused(true)}
              placeholder="ابحث عن منشورات، أشخاص..."
              className="w-full h-10 rounded-2xl bg-muted/60 border border-border/30 pr-10 pl-10 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-all"
              data-testid="explore-search-input"
            />
            {searchQuery && (
              <button onClick={clearSearch} className="absolute left-3 top-1/2 -translate-y-1/2 p-0.5 rounded-full bg-muted-foreground/20">
                <X className="h-3.5 w-3.5 text-muted-foreground" />
              </button>
            )}
          </div>
          {isSearchFocused && (
            <button onClick={clearSearch} className="text-sm text-primary font-bold shrink-0">إلغاء</button>
          )}
        </div>

        {/* Search Type Tabs */}
        {(searchQuery || isSearchFocused) && (
          <div className="flex gap-2 mt-3">
            {searchTabs.map(tab => (
              <button
                key={tab.key}
                onClick={() => { setSearchType(tab.key as any); doSearch(searchQuery, tab.key); }}
                className={cn(
                  'flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold transition-all',
                  searchType === tab.key ? 'bg-primary text-primary-foreground' : 'bg-muted/60 text-muted-foreground'
                )}
              >
                <tab.icon className="h-3.5 w-3.5" />
                {tab.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Search Results */}
      {searchResults ? (
        <div className="px-4 py-4">
          {searching ? (
            <div className="flex justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
          ) : (
            <>
              {/* User Results */}
              {searchResults.users.length > 0 && (searchType === 'all' || searchType === 'users') && (
                <div className="mb-6">
                  <h3 className="text-sm font-bold text-foreground mb-3 flex items-center gap-2">
                    <Users className="h-4 w-4 text-primary" />أشخاص
                  </h3>
                  <div className="space-y-2">
                    {searchResults.users.map(u => <UserCard key={u.id} user={u} />)}
                  </div>
                </div>
              )}

              {/* Post Results */}
              {searchResults.posts.length > 0 && (searchType === 'all' || searchType === 'posts') && (
                <div>
                  <h3 className="text-sm font-bold text-foreground mb-3 flex items-center gap-2">
                    <Hash className="h-4 w-4 text-primary" />منشورات
                  </h3>
                  <div className="grid grid-cols-3 gap-1">
                    {searchResults.posts.map(p => (
                      <GridPostCard key={p.id} post={p} onClick={() => navigate(`/sohba?post=${p.id}`)} />
                    ))}
                  </div>
                </div>
              )}

              {/* No results */}
              {searchResults.posts.length === 0 && searchResults.users.length === 0 && (
                <div className="text-center py-16">
                  <Search className="h-12 w-12 text-muted-foreground/30 mx-auto mb-3" />
                  <p className="text-sm text-muted-foreground">لا توجد نتائج لـ "{searchQuery}"</p>
                </div>
              )}
            </>
          )}
        </div>
      ) : (
        /* Explore Feed */
        <div className="px-2 py-4">
          {/* Trending Users */}
          {trendingUsers.length > 0 && (
            <div className="mb-5 px-2">
              <h3 className="text-sm font-bold text-foreground mb-3 flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-primary" />مستخدمون بارزون
              </h3>
              <div className="flex gap-3 overflow-x-auto no-scrollbar pb-2">
                {trendingUsers.map(u => {
                  const ci = (u.name || '').charCodeAt(0) % avatarColors.length;
                  return (
                    <Link key={u.id} to={`/sohba?profile=${u.id}`} className="flex flex-col items-center gap-1.5 shrink-0 w-16">
                      <div className={cn('h-14 w-14 rounded-full flex items-center justify-center text-sm text-white font-bold border-2 border-primary/30', avatarColors[ci])}>
                        {u.avatar ? <img src={u.avatar} className="h-full w-full rounded-full object-cover" alt="" /> : (u.name?.[0] || '؟')}
                      </div>
                      <span className="text-[10px] text-foreground font-medium truncate w-full text-center">{u.name}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          )}

          {/* Explore Grid */}
          {loading ? (
            <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
          ) : explorePosts.length === 0 ? (
            <div className="text-center py-16 px-8">
              <Grid3X3 className="h-14 w-14 text-muted-foreground/20 mx-auto mb-3" />
              <p className="text-sm text-muted-foreground">لا يوجد محتوى بعد</p>
              <p className="text-xs text-muted-foreground/60 mt-1">كن أول من ينشر محتوى!</p>
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-1 px-1">
              {explorePosts.map(p => (
                <GridPostCard key={p.id} post={p} onClick={() => navigate(`/sohba?post=${p.id}`)} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
