import { useState, useEffect, useCallback, useRef } from 'react';
import { Search, X, Loader2, Heart, Eye, MessageCircle, TrendingUp, Flame, BookOpen, Star, Sparkles, Compass, Play, ArrowRight, Send, Film, Bookmark, Maximize2, Mic, MicOff } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { useLocale } from '@/hooks/useLocale';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { AdBanner } from '@/components/AdBanner';

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
  engagement?: number; embed_url?: string; platform?: string; is_embed?: boolean;
}

interface Comment {
  id: string; author_name: string; author_avatar?: string; content: string; created_at: string;
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
    } catch { toast.error('خطأ'); }
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
          <span className="text-sm font-bold">{comments.length} {t('comment')}</span>
          <button onClick={onClose} className="p-1.5 rounded-full hover:bg-muted/50"><X className="h-5 w-5 text-muted-foreground" /></button>
        </div>
        <div className="flex-1 overflow-y-auto px-5 py-3 space-y-4 min-h-[120px]">
          {loading ? <div className="flex justify-center py-8"><Loader2 className="h-5 w-5 animate-spin text-muted-foreground" /></div>
            : comments.length === 0 ? <p className="text-center text-xs text-muted-foreground py-10">لا توجد {t('comment')}ات بعد</p>
            : comments.map(c => {
              const ci = (c.author_name || '').charCodeAt(0) % avatarColors.length;
              return (
                <div key={c.id} className="flex gap-2.5">
                  <div className={cn('h-8 w-8 rounded-full flex items-center justify-center text-[10px] text-white font-bold shrink-0', avatarColors[ci])}>
                    {c.author_name?.[0]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-[12px] font-bold text-foreground">{c.author_name}</span>
                      <span className="text-[10px] text-muted-foreground">{timeAgo(c.created_at)}</span>
                    </div>
                    <p className="text-[13px] text-foreground/85 mt-0.5" dir="auto">{c.content}</p>
                  </div>
                </div>
              );
            })
          }
        </div>
        <div className="px-4 py-3 border-t border-border/20 flex gap-2 bg-card">
          <input value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()}
            dir="auto" placeholder={t('addComment')}
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

/* ========== STORY DETAIL VIEW (inline) ========== */
function StoryDetailView({ storyId, onBack }: { storyId: string; onBack: () => void }) {
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
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    if (!story) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${story.id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      setStory(s => s ? { ...s, liked: d.liked, likes_count: s.likes_count + (d.liked ? 1 : -1) } : s);
    } catch {}
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-background"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>;
  if (!story) return <div className="min-h-screen flex flex-col items-center justify-center bg-background gap-3">
    <p className="text-muted-foreground">القصة غير موجودة</p>
    <button onClick={onBack} className="text-primary text-sm font-bold">العودة</button>
  </div>;

  const ci = (story.author_name || '').charCodeAt(0) % avatarColors.length;
  const rawUrl = story.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('http') ? rawUrl : `${BACKEND_URL}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`) : null;
  const isEmbed = story.is_embed || story.media_type === 'embed';

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl">
      <div className="sticky top-0 z-40 bg-card/95 backdrop-blur-xl border-b border-border/20">
        <div className="flex items-center justify-between px-4 h-14">
          <button onClick={onBack} className="p-2 rounded-xl bg-muted/50 active:scale-95"><ArrowRight className="h-5 w-5 text-foreground" /></button>
          <h2 className="text-sm font-bold text-foreground truncate flex-1 mx-3 text-center">القصة</h2>
          <div className="w-9" />
        </div>
      </div>

      {isEmbed && story.embed_url ? (
        <div className="w-full aspect-video">
          <iframe src={story.embed_url} title={story.title} className="w-full h-full" frameBorder={0}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
        </div>
      ) : mediaUrl ? (
        <div className="w-full max-h-72 overflow-hidden"><img src={mediaUrl} alt="" className="w-full h-72 object-cover" /></div>
      ) : null}

      <div className="px-5 py-5">
        <div className="flex items-center gap-3 mb-4">
          <div className={cn('h-10 w-10 rounded-full flex items-center justify-center text-sm text-white font-bold', avatarColors[ci])}>
            {story.author_name?.[0] || '؟'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold text-foreground">{story.author_name}</p>
            <p className="text-[10px] text-muted-foreground">{timeAgo(story.created_at)}</p>
          </div>
        </div>
        {story.title && <h1 className="text-xl font-bold text-foreground mb-4 leading-relaxed">{story.title}</h1>}
        <p className="text-sm text-foreground leading-[2.2] whitespace-pre-wrap" style={{ fontFamily: "'Amiri','Noto Naskh Arabic',serif" }}>{story.content}</p>

        <div className="flex items-center gap-5 mt-6 pt-4 border-t border-border/20">
          <button onClick={toggleLike} className="flex items-center gap-2 text-sm active:scale-90 transition-transform">
            <Heart className={cn("h-6 w-6 transition-all", story.liked ? "text-red-500 fill-red-500" : "text-muted-foreground")} />
            <span className={cn("font-bold", story.liked ? "text-red-500" : "text-foreground")}>{story.likes_count}</span>
          </button>
          <button onClick={() => setShowComments(true)} className="flex items-center gap-2 text-sm active:scale-90 transition-transform">
            <MessageCircle className="h-6 w-6 text-muted-foreground" />
            <span className="font-bold text-foreground">{story.comments_count}</span>
          </button>
          <span className="flex items-center gap-1.5 text-xs text-muted-foreground mr-auto">
            <Eye className="h-4 w-4" />{story.views_count || 0} مشاهدة
          </span>
        </div>
      </div>

      <AnimatePresence>
        {showComments && <CommentsSheet storyId={story.id} onClose={() => setShowComments(false)} />}
      </AnimatePresence>
    </div>
  );
}

/* ========== HORIZONTAL STORY CARD ========== */
function HorizontalStoryCard({ story, rank, onOpen, onLike }: { story: Story; rank?: number; onOpen: () => void; onLike: () => void }) {
  const ci = (story.author_name || '').charCodeAt(0) % avatarColors.length;
  const rawUrl = story.image_url;
  const mediaUrl = rawUrl ? (rawUrl.startsWith('http') ? rawUrl : `${BACKEND_URL}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`) : null;
  const isEmbed = story.is_embed || story.media_type === 'embed';

  return (
    <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
      className="flex gap-3 p-3 rounded-2xl bg-card border border-border/30 w-full text-right active:scale-[0.98] transition-all hover:border-primary/30 hover:shadow-md cursor-pointer"
      dir="rtl" onClick={onOpen}>
      {mediaUrl ? (
        <div className="h-20 w-20 rounded-xl overflow-hidden shrink-0 relative">
          <img src={mediaUrl} alt="" className="h-full w-full object-cover" loading="lazy" />
          {rank && <div className="absolute top-1 right-1 h-5 w-5 rounded-full bg-primary text-primary-foreground text-[9px] font-bold flex items-center justify-center">{rank}</div>}
          {isEmbed && <div className="absolute bottom-1 left-1"><Play className="h-3.5 w-3.5 text-white drop-shadow" /></div>}
        </div>
      ) : (
        <div className="h-20 w-20 rounded-xl shrink-0 bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center relative">
          {isEmbed ? <Film className="h-6 w-6 text-primary/40" /> : <BookOpen className="h-6 w-6 text-primary/40" />}
          {rank && <div className="absolute top-1 right-1 h-5 w-5 rounded-full bg-primary text-primary-foreground text-[9px] font-bold flex items-center justify-center">{rank}</div>}
        </div>
      )}
      <div className="flex-1 min-w-0 py-0.5">
        <p className="text-xs font-bold text-foreground line-clamp-2 mb-1">{story.title || story.content}</p>
        <div className="flex items-center gap-2 mb-1.5">
          <div className={cn('h-4 w-4 rounded-full flex items-center justify-center text-[7px] text-white font-bold shrink-0', avatarColors[ci])}>{story.author_name?.[0] || '؟'}</div>
          <span className="text-[10px] text-muted-foreground truncate">{story.author_name}</span>
          <span className="text-[9px] text-muted-foreground">{timeAgo(story.created_at)}</span>
        </div>
        <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
          <span className="flex items-center gap-0.5"><Eye className="h-3 w-3" />{story.views_count || 0}</span>
          <button onClick={e => { e.stopPropagation(); onLike(); }} className="flex items-center gap-0.5 active:scale-90">
            <Heart className={cn("h-3 w-3", story.liked ? "text-red-500 fill-red-500" : "")} />{story.likes_count || 0}
          </button>
          <span className="flex items-center gap-0.5"><MessageCircle className="h-3 w-3" />{story.comments_count || 0}</span>
        </div>
      </div>
    </motion.div>
  );
}

/* ========== MAIN EXPLORE PAGE ========== */
export default function Explore() {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchQuery, setSearchQuery] = useState('');
  const [mostViewed, setMostViewed] = useState<Story[]>([]);
  const [mostInteracted, setMostInteracted] = useState<Story[]>([]);
  const [searchResults, setSearchResults] = useState<Story[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [isSearchActive, setIsSearchActive] = useState(false);
  const [showCommentsFor, setShowCommentsFor] = useState<string | null>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const searchTimer = useRef<ReturnType<typeof setTimeout>>();
  const [isListening, setIsListening] = useState(false);
  const [aiResponse, setAiResponse] = useState('');
  const recognitionRef = useRef<any>(null);
  const [showMoreViewed, setShowMoreViewed] = useState(false);
  const [showMoreInteracted, setShowMoreInteracted] = useState(false);

  // Story detail from URL params — browser back works automatically
  const selectedStoryId = searchParams.get('story');

  // Open story — PUSH URL params (creates history entry)
  const handleOpenStory = useCallback((storyId: string) => {
    const params = new URLSearchParams(searchParams);
    params.set('story', storyId);
    setSearchParams(params); // push, not replace
  }, [searchParams, setSearchParams]);

  // Back from story — browser back
  const handleBackFromStory = useCallback(() => {
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) {
      window.history.back();
    } else {
      setSearchParams({}, { replace: true });
    }
  }, [setSearchParams]);

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
    if (!q.trim()) { setSearchResults(null); setAiResponse(''); return; }
    setSearching(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/stories/feed/search?q=${encodeURIComponent(q)}&limit=30`, { headers: authHeaders() });
      const d = await r.json();
      setSearchResults(d.stories || []);
    } catch { setSearchResults([]); }
    setSearching(false);
  }, []);

  // AI Voice Search
  const doVoiceSearch = useCallback(async (q: string) => {
    if (!q.trim()) return;
    setSearching(true);
    setAiResponse('');
    try {
      const r = await fetch(`${BACKEND_URL}/api/stories/voice-search`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ query: q })
      });
      const d = await r.json();
      setSearchResults(d.stories || []);
      if (d.ai_response) setAiResponse(d.ai_response);
    } catch { setSearchResults([]); }
    setSearching(false);
  }, []);

  const handleSearchInput = (val: string) => {
    setSearchQuery(val);
    if (searchTimer.current) clearTimeout(searchTimer.current);
    searchTimer.current = setTimeout(() => doSearch(val), 400);
  };

  const clearSearch = () => { setSearchQuery(''); setSearchResults(null); setIsSearchActive(false); setAiResponse(''); searchInputRef.current?.blur(); };

  // Voice recognition
  const toggleVoiceSearch = () => {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      return;
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      toast.error(t('voiceNotSupported'));
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'ar-SA';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
      setIsSearchActive(true);
      toast.info('🎤 تحدّث الآن... ابحث عن قصة');
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setSearchQuery(transcript);
      setIsListening(false);
      // Use AI-powered voice search
      doVoiceSearch(transcript);
    };

    recognition.onerror = () => {
      setIsListening(false);
      toast.error(t('voiceNotRecognized') + '، حاول مرة أخرى');
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;
    recognition.start();
  };

  const toggleLike = async (id: string) => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${id}/like`, { method: 'POST', headers: authHeaders() });
      const d = await r.json();
      const update = (list: Story[]) => list.map(x => x.id === id ? { ...x, liked: d.liked, likes_count: x.likes_count + (d.liked ? 1 : -1) } : x);
      setMostViewed(update);
      setMostInteracted(update);
      if (searchResults) setSearchResults(update);
    } catch {}
  };

  // Show story detail
  if (selectedStoryId) {
    return <StoryDetailView storyId={selectedStoryId} onBack={handleBackFromStory} />;
  }

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="explore-page">
      {/* HEADER */}
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
                placeholder={t("searchStoryOrAuthor") + "..."}
                className="w-full h-10 rounded-2xl bg-muted/50 border border-border/30 pr-10 pl-16 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/40 focus:ring-2 focus:ring-primary/15 transition-all"
                style={{ unicodeBidi: 'plaintext' } as any} autoComplete="off" spellCheck={false} />
              <div className="absolute left-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                {searchQuery && (
                  <button onClick={clearSearch} className="p-0.5 rounded-full bg-muted-foreground/20">
                    <X className="h-3 w-3 text-muted-foreground" />
                  </button>
                )}
                {/* Voice Search Button */}
                <button
                  onClick={toggleVoiceSearch}
                  className={cn(
                    "p-1.5 rounded-full transition-all",
                    isListening ? "bg-red-500 animate-pulse" : "bg-primary/10 hover:bg-primary/20"
                  )}
                >
                  {isListening ? (
                    <MicOff className="h-3.5 w-3.5 text-white" />
                  ) : (
                    <Mic className="h-3.5 w-3.5 text-primary" />
                  )}
                </button>
              </div>
            </div>
            {isSearchActive && <button onClick={clearSearch} className="text-sm text-primary font-bold shrink-0">إلغاء</button>}
          </div>
        </div>
      </div>

      {/* Voice Listening Indicator */}
      <AnimatePresence>
        {isListening && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="mx-4 mt-3 rounded-2xl bg-red-500/10 border border-red-500/20 p-4 flex items-center gap-3"
          >
            <div className="h-10 w-10 rounded-full bg-red-500 flex items-center justify-center animate-pulse">
              <Mic className="h-5 w-5 text-white" />
            </div>
            <div>
              <p className="text-sm font-bold text-foreground">جاري الاستماع...</p>
              <p className="text-xs text-muted-foreground">{t('saySomethingLike')}: "أريد قصة عن الاستغفار"</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* AI Response */}
      {aiResponse && (
        <div className="mx-4 mt-3 rounded-2xl bg-primary/5 border border-primary/20 p-4">
          <div className="flex items-center gap-2 mb-1">
            <Sparkles className="h-4 w-4 text-primary" />
            <span className="text-xs font-bold text-primary">المساعد الذكي</span>
          </div>
          <p className="text-sm text-foreground">{aiResponse}</p>
        </div>
      )}

      {/* CONTENT */}
      {searchResults !== null ? (
        <div className="px-4 py-4">
          {searching ? (
            <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
          ) : searchResults.length === 0 ? (
            <div className="text-center py-20">
              <Search className="h-14 w-14 text-muted-foreground/20 mx-auto mb-4" />
              <p className="text-base font-bold text-muted-foreground/60">لا توجد نتائج</p>
              <p className="text-xs text-muted-foreground/40 mt-1">جرّب كلمات مختلفة أو استخدم البحث الصوتي 🎤</p>
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-xs text-muted-foreground mb-3">{searchResults.length} نتيجة</p>
              {searchResults.map((s, i) => (
                <HorizontalStoryCard key={s.id} story={s} onOpen={() => handleOpenStory(s.id)} onLike={() => toggleLike(s.id)} />
              ))}
            </div>
          )}
        </div>
      ) : loading ? (
        <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>
      ) : (
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
                  <p className="text-[10px] text-muted-foreground">{t('storiesEveryoneReads')}</p>
                </div>
              </div>
              <div className="space-y-2">
                {(showMoreViewed ? mostViewed : mostViewed.slice(0, 5)).map((s, i) => (
                  <HorizontalStoryCard key={s.id} story={s} rank={i + 1} onOpen={() => handleOpenStory(s.id)} onLike={() => toggleLike(s.id)} />
                ))}
              </div>
              {mostViewed.length > 5 && (
                <button
                  onClick={() => setShowMoreViewed(!showMoreViewed)}
                  className="w-full mt-3 py-2.5 rounded-xl bg-card border border-primary/20 text-primary text-xs font-bold active:scale-[0.98] transition-transform"
                >
                  {showMoreViewed ? t('showLess') : `المزيد (${mostViewed.length - 5})`}
                </button>
              )}
            </section>
          )}

          {/* Ad between sections */}
          <AdBanner position="home" />

          {/* Most Interacted */}
          {mostInteracted.length > 0 && (
            <section>
              <div className="flex items-center gap-2 mb-3">
                <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-rose-500 to-pink-600 flex items-center justify-center shadow-md shadow-rose-500/20">
                  <Flame className="h-4 w-4 text-white" />
                </div>
                <div>
                  <h2 className="text-sm font-bold text-foreground">الأكثر تفاعلاً</h2>
                  <p className="text-[10px] text-muted-foreground">{t('touchedHearts')}</p>
                </div>
              </div>
              <div className="space-y-2">
                {(showMoreInteracted ? mostInteracted : mostInteracted.slice(0, 5)).map((s, i) => (
                  <HorizontalStoryCard key={s.id} story={s} rank={i + 1} onOpen={() => handleOpenStory(s.id)} onLike={() => toggleLike(s.id)} />
                ))}
              </div>
              {mostInteracted.length > 5 && (
                <button
                  onClick={() => setShowMoreInteracted(!showMoreInteracted)}
                  className="w-full mt-3 py-2.5 rounded-xl bg-card border border-primary/20 text-primary text-xs font-bold active:scale-[0.98] transition-transform"
                >
                  {showMoreInteracted ? t('showLess') : `المزيد (${mostInteracted.length - 5})`}
                </button>
              )}
            </section>
          )}

          {/* Empty state */}
          {mostViewed.length === 0 && mostInteracted.length === 0 && (
            <div className="text-center py-16 px-8">
              <Compass className="h-16 w-16 text-muted-foreground/15 mx-auto mb-4" />
              <p className="text-base font-bold text-muted-foreground/50">{t('noContentYet')}</p>
              <p className="text-xs text-muted-foreground/30 mt-1">{t('publishFirstStoryInspire')}</p>
              <button onClick={() => navigate('/stories?create=true')}
                className="mt-4 bg-primary text-primary-foreground px-6 py-2.5 rounded-2xl text-sm font-bold shadow-md">
                {t('publishFirst')} ✨
              </button>
            </div>
          )}
        </div>
      )}

      <AnimatePresence>
        {showCommentsFor && <CommentsSheet storyId={showCommentsFor} onClose={() => setShowCommentsFor(null)} />}
      </AnimatePresence>
    </div>
  );
}
