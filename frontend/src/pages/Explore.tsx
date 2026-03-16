import { useState, useEffect, useCallback, useRef } from 'react';
import { Search, X, Loader2, Heart, Eye, MessageCircle, TrendingUp, Flame, BookOpen, Star, Sparkles, Compass, Play } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';

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
  comments_count: number; views_count?: number; liked: boolean; saved: boolean; engagement?: number;
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

/* ========== HORIZONTAL STORY CARD ========== */
function HorizontalStoryCard({ story, rank }: { story: Story; rank?: number }) {
  const navigate = useNavigate();
  const ci = (story.author_name || '').charCodeAt(0) % avatarColors.length;
  const rawUrl = story.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('http') ? rawUrl : `${BACKEND_URL}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`) : null;

  return (
    <motion.button
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      onClick={() => navigate('/stories')}
      className="flex gap-3 p-3 rounded-2xl bg-card border border-border/30 w-full text-right active:scale-[0.98] transition-all hover:border-primary/30 hover:shadow-md"
      dir="rtl"
    >
      {/* Thumbnail or rank */}
      {mediaUrl ? (
        <div className="h-20 w-20 rounded-xl overflow-hidden shrink-0 relative">
          <img src={mediaUrl} alt="" className="h-full w-full object-cover" loading="lazy" />
          {rank && (
            <div className="absolute top-1 right-1 h-5 w-5 rounded-full bg-primary text-primary-foreground text-[9px] font-bold flex items-center justify-center">
              {rank}
            </div>
          )}
        </div>
      ) : (
        <div className="h-20 w-20 rounded-xl shrink-0 bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center relative">
          <BookOpen className="h-6 w-6 text-primary/40" />
          {rank && (
            <div className="absolute top-1 right-1 h-5 w-5 rounded-full bg-primary text-primary-foreground text-[9px] font-bold flex items-center justify-center">
              {rank}
            </div>
          )}
        </div>
      )}

      <div className="flex-1 min-w-0 py-0.5">
        <p className="text-xs font-bold text-foreground line-clamp-2 mb-1">{story.title || story.content}</p>
        <div className="flex items-center gap-2 mb-1.5">
          <div className={cn('h-4 w-4 rounded-full flex items-center justify-center text-[7px] text-white font-bold shrink-0', avatarColors[ci])}>
            {story.author_name?.[0] || '؟'}
          </div>
          <span className="text-[10px] text-muted-foreground truncate">{story.author_name}</span>
          <span className="text-[9px] text-muted-foreground">{timeAgo(story.created_at)}</span>
        </div>
        <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
          <span className="flex items-center gap-0.5"><Eye className="h-3 w-3" />{story.views_count || 0}</span>
          <span className="flex items-center gap-0.5"><Heart className="h-3 w-3" />{story.likes_count || 0}</span>
          <span className="flex items-center gap-0.5"><MessageCircle className="h-3 w-3" />{story.comments_count || 0}</span>
        </div>
      </div>
    </motion.button>
  );
}

/* ========== GRID STORY CARD ========== */
function GridStoryCard({ story, size = 'sm' }: { story: Story; size?: 'sm' | 'lg' }) {
  const navigate = useNavigate();
  const rawUrl = story.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('http') ? rawUrl : `${BACKEND_URL}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`) : null;
  const [imgOk, setImgOk] = useState(true);
  const ci = (story.author_name || '').charCodeAt(0) % avatarColors.length;
  const aspectClass = size === 'lg' ? 'row-span-2 aspect-[3/4]' : 'aspect-square';

  return (
    <button onClick={() => navigate('/stories')}
      className={cn('relative rounded-2xl overflow-hidden group', aspectClass)}>
      {mediaUrl && imgOk ? (
        <img src={mediaUrl} alt="" className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          loading="lazy" onError={() => setImgOk(false)} />
      ) : (
        <div className={cn('w-full h-full flex items-center justify-center p-3',
          'bg-gradient-to-br from-emerald-900/80 to-slate-900')}>
          <p className="text-white/80 text-center leading-relaxed text-[10px] line-clamp-5" dir="rtl"
            style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>{story.title || story.content}</p>
        </div>
      )}
      <div className="absolute inset-x-0 bottom-0 p-2.5"
        style={{ background: 'linear-gradient(to top, rgba(0,0,0,.75) 0%, transparent 100%)' }}>
        <p className="text-[9px] text-white/90 font-bold line-clamp-1 mb-0.5">{story.title || ''}</p>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1 min-w-0">
            <div className={cn('h-4 w-4 rounded-full flex items-center justify-center text-[6px] text-white font-bold shrink-0', avatarColors[ci])}>
              {story.author_name?.[0] || '؟'}
            </div>
            <span className="text-[8px] text-white/80 truncate">{story.author_name}</span>
          </div>
          <div className="flex items-center gap-1.5 shrink-0">
            <span className="flex items-center gap-0.5 text-[8px] text-white/70"><Eye className="h-2.5 w-2.5" />{story.views_count || 0}</span>
            <span className="flex items-center gap-0.5 text-[8px] text-white/70"><Heart className="h-2.5 w-2.5" />{story.likes_count || 0}</span>
          </div>
        </div>
      </div>
    </button>
  );
}

/* ========== SEARCH RESULT CARD ========== */
function SearchResultCard({ story }: { story: Story }) {
  const navigate = useNavigate();
  const ci = (story.author_name || '').charCodeAt(0) % avatarColors.length;
  const rawUrl = story.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('http') ? rawUrl : `${BACKEND_URL}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`) : null;

  return (
    <button onClick={() => navigate('/stories')}
      className="flex gap-3 p-3.5 rounded-2xl bg-card border border-border/30 w-full text-right active:scale-[0.98] transition-all" dir="rtl">
      {mediaUrl ? (
        <div className="h-16 w-16 rounded-xl overflow-hidden shrink-0">
          <img src={mediaUrl} alt="" className="h-full w-full object-cover" loading="lazy" />
        </div>
      ) : (
        <div className="h-16 w-16 rounded-xl shrink-0 bg-gradient-to-br from-primary/15 to-primary/5 flex items-center justify-center">
          <BookOpen className="h-5 w-5 text-primary/30" />
        </div>
      )}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-bold text-foreground line-clamp-1 mb-0.5">{story.title || story.content.substring(0, 50)}</p>
        <p className="text-[11px] text-muted-foreground line-clamp-2 mb-1">{story.content}</p>
        <div className="flex items-center gap-2">
          <div className={cn('h-4 w-4 rounded-full flex items-center justify-center text-[7px] text-white font-bold shrink-0', avatarColors[ci])}>
            {story.author_name?.[0] || '؟'}
          </div>
          <span className="text-[10px] text-muted-foreground">{story.author_name}</span>
          <span className="text-[9px] text-muted-foreground mr-auto">{timeAgo(story.created_at)}</span>
        </div>
      </div>
    </button>
  );
}

/* ========== MAIN EXPLORE PAGE ========== */
export default function Explore() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [mostViewed, setMostViewed] = useState<Story[]>([]);
  const [mostInteracted, setMostInteracted] = useState<Story[]>([]);
  const [searchResults, setSearchResults] = useState<Story[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [isSearchActive, setIsSearchActive] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const searchTimer = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [viewedRes, interactedRes] = await Promise.all([
        fetch(`${BACKEND_URL}/api/stories/feed/most-viewed?limit=10`, { headers: authHeaders() }),
        fetch(`${BACKEND_URL}/api/stories/feed/most-interacted?limit=20`, { headers: authHeaders() }),
      ]);
      const viewedData = await viewedRes.json();
      const interactedData = await interactedRes.json();
      setMostViewed(viewedData.stories || []);
      setMostInteracted(interactedData.stories || []);
    } catch {}
    setLoading(false);
  };

  const doSearch = useCallback(async (q: string) => {
    if (!q.trim()) { setSearchResults(null); return; }
    setSearching(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/stories/feed/search?q=${encodeURIComponent(q)}&limit=30`, { headers: authHeaders() });
      const d = await r.json();
      setSearchResults(d.stories || []);
    } catch { setSearchResults([]); }
    setSearching(false);
  }, []);

  const handleSearchInput = (val: string) => {
    setSearchQuery(val);
    if (searchTimer.current) clearTimeout(searchTimer.current);
    searchTimer.current = setTimeout(() => doSearch(val), 400);
  };

  const clearSearch = () => { setSearchQuery(''); setSearchResults(null); setIsSearchActive(false); searchInputRef.current?.blur(); };

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="explore-page">
      {/* ===== HEADER ===== */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20">
        <div className="px-4 pt-3 pb-3">
          <div className="flex items-center gap-2">
            {!isSearchActive && (
              <h1 className="text-xl font-black text-foreground shrink-0 flex items-center gap-2">
                <Compass className="h-5 w-5 text-primary" />
                استكشف
              </h1>
            )}
            <div className="relative flex-1">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
              <input ref={searchInputRef} type="search" dir="auto" value={searchQuery}
                onChange={e => handleSearchInput(e.target.value)}
                onFocus={() => setIsSearchActive(true)}
                placeholder="ابحث عن قصة أو كاتب..." data-testid="explore-search-input"
                className="w-full h-10 rounded-2xl bg-muted/50 border border-border/30 pr-10 pl-10 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/40 focus:ring-2 focus:ring-primary/15 transition-all"
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
      </div>

      {/* ===== CONTENT ===== */}
      {searchResults !== null ? (
        /* ---- SEARCH RESULTS ---- */
        <div className="px-4 py-4">
          {searching ? (
            <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
          ) : searchResults.length === 0 ? (
            <div className="text-center py-20">
              <Search className="h-14 w-14 text-muted-foreground/20 mx-auto mb-4" />
              <p className="text-base font-bold text-muted-foreground/60">لا توجد نتائج</p>
              <p className="text-xs text-muted-foreground/40 mt-1">جرّب كلمات مختلفة</p>
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-xs text-muted-foreground mb-3">{searchResults.length} نتيجة</p>
              {searchResults.map(s => <SearchResultCard key={s.id} story={s} />)}
            </div>
          )}
        </div>
      ) : loading ? (
        <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>
      ) : (
        /* ---- EXPLORE FEED ---- */
        <div className="px-4 py-4 space-y-6">
          {/* Most Viewed */}
          {mostViewed.length > 0 && (
            <section>
              <div className="flex items-center gap-2 mb-3">
                <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center shadow-md shadow-amber-500/20">
                  <Eye className="h-4 w-4 text-white" />
                </div>
                <div>
                  <h2 className="text-sm font-bold text-foreground">الأكثر مشاهدة</h2>
                  <p className="text-[10px] text-muted-foreground">القصص التي يقرأها الجميع</p>
                </div>
              </div>
              <div className="space-y-2">
                {mostViewed.slice(0, 5).map((s, i) => <HorizontalStoryCard key={s.id} story={s} rank={i + 1} />)}
              </div>
              {mostViewed.length > 5 && (
                <button onClick={() => navigate('/stories')} className="w-full mt-2 py-2 text-xs text-primary font-bold text-center">
                  عرض المزيد ←
                </button>
              )}
            </section>
          )}

          {/* Most Interacted */}
          {mostInteracted.length > 0 && (
            <section>
              <div className="flex items-center gap-2 mb-3">
                <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-rose-500 to-pink-600 flex items-center justify-center shadow-md shadow-rose-500/20">
                  <Flame className="h-4 w-4 text-white" />
                </div>
                <div>
                  <h2 className="text-sm font-bold text-foreground">الأكثر تفاعلاً</h2>
                  <p className="text-[10px] text-muted-foreground">قصص أثرت في القلوب</p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-1.5 rounded-xl overflow-hidden">
                {mostInteracted.slice(0, 9).map((s, i) => (
                  <GridStoryCard key={s.id} story={s} size={i === 0 ? 'lg' : 'sm'} />
                ))}
              </div>
            </section>
          )}

          {/* Empty state */}
          {mostViewed.length === 0 && mostInteracted.length === 0 && (
            <div className="text-center py-16 px-8">
              <Compass className="h-16 w-16 text-muted-foreground/15 mx-auto mb-4" />
              <p className="text-base font-bold text-muted-foreground/50">لا يوجد محتوى بعد</p>
              <p className="text-xs text-muted-foreground/30 mt-1">انشر قصتك وكن أول من يلهم الآخرين</p>
              <button onClick={() => navigate('/stories?create=true')}
                className="mt-4 bg-primary text-primary-foreground px-6 py-2.5 rounded-2xl text-sm font-bold shadow-md">
                انشر أول قصة ✨
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
