import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { useAdmin } from '@/hooks/useAdmin';
import { useTheme } from '@/components/ThemeProvider';
import { useLocale } from '@/hooks/useLocale';
import { useSmartBack } from '@/hooks/useSmartBack';
import {
  Settings, ChevronLeft, Star, Users, Heart,
  LogOut, Shield, Moon, Sun, SunMoon, Globe,
  HelpCircle, Bookmark, Grid3X3, Play, MoreVertical,
  Bot, Bell, Gift, Gem, Edit3, Share2, MessageSquare,
  Lock, Palette, ChevronRight, Zap, Crown, ShoppingBag,
  BookOpen, Eye, MessageCircle, Compass, Film,
  Home, Calculator, Clock, ChevronDown, X,
  Info, Mail, Phone, Award, Sparkles, TrendingUp,
} from 'lucide-react';
// eslint-disable-next-line @typescript-eslint/no-unused-vars
type LucideIconAlias = typeof Settings;
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { motion, AnimatePresence } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';
function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

const avatarColors = ['bg-amber-600', 'bg-yellow-600', 'bg-orange-600', 'bg-rose-600', 'bg-purple-600', 'bg-teal-600'];

interface Post {
  id: string; content: string; title?: string; image_url?: string; media_type?: string;
  likes_count: number; comments_count: number; views_count?: number; created_at: string;
  category?: string; embed_url?: string; is_embed?: boolean;
}

function timeAgo(iso: string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 60) return `${m}د`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}س`;
  return `${Math.floor(h / 24)}ي`;
}

/* ===== DROPDOWN MENU ===== */
function DropdownMenu({ open, onClose, children }: { open: boolean; onClose: () => void; children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!open) return;
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose();
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          ref={ref}
          initial={{ opacity: 0, scale: 0.9, y: -8 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: -8 }}
          transition={{ duration: 0.15 }}
          className="absolute left-4 top-12 z-[100] w-56 rounded-2xl bg-card border border-primary/20 shadow-2xl shadow-black/40 overflow-hidden"
        >
          {children}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

interface MenuItemProps { icon: typeof Settings; label: string; to?: string; onClick?: () => void; color?: string; badge?: string; }
function MenuItem({ icon: Icon, label, to, onClick, color, badge }: MenuItemProps) {
  const content = (
    <div className="flex items-center gap-3 px-4 py-3 hover:bg-primary/5 active:bg-primary/10 transition-colors cursor-pointer">
      <Icon className={cn('h-4 w-4', color || 'text-primary/70')} />
      <span className="text-[13px] font-medium text-foreground flex-1">{label}</span>
      {badge && <span className="text-[9px] bg-primary text-primary-foreground px-1.5 py-0.5 rounded-full font-bold">{badge}</span>}
    </div>
  );
  if (to) return <Link to={to} className="block">{content}</Link>;
  return <div onClick={onClick}>{content}</div>;
}

export default function Profile() {
  const { user, signOut } = useAuth();
  const { isAdmin } = useAdmin();
  const { mode, setMode } = useTheme();
  const { t, dir, isRTL } = useLocale();
  const navigate = useNavigate();
  const goBack = useSmartBack();
  const params = useParams();
  const viewingUserId = params.userId;

  const [stats, setStats] = useState({ posts: 0, stories: 0, followers: 0, following: 0, likes: 0, saved: 0, liked: 0 });
  const [myPosts, setMyPosts] = useState<Post[]>([]);
  const [savedPosts, setSavedPosts] = useState<Post[]>([]);
  const [likedPosts, setLikedPosts] = useState<Post[]>([]);
  const [activeTab, setActiveTab] = useState<'posts' | 'saved' | 'liked'>('posts');
  const [loadingPosts, setLoadingPosts] = useState(false);
  const [loadingSaved, setLoadingSaved] = useState(false);
  const [loadingLiked, setLoadingLiked] = useState(false);
  const [otherUser, setOtherUser] = useState<any>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const targetId = viewingUserId || user?.id;
    if (!targetId) return;
    setLoadingPosts(true);

    // Load stats
    if (!viewingUserId || viewingUserId === user?.id) {
      fetch(`${BACKEND_URL}/api/sohba/my-stats`, { headers: authHeaders() })
        .then(r => r.json())
        .then(d => setStats({
          posts: d.posts || 0,
          stories: d.stories || 0,
          followers: d.followers || 0,
          following: d.following || 0,
          likes: d.total_likes || 0,
          saved: d.saved_count || 0,
          liked: d.liked_count || 0
        }))
        .catch(() => {});
    }

    // Load my stories
    fetch(`${BACKEND_URL}/api/stories/list?limit=50`, { headers: authHeaders() })
      .then(r => r.json())
      .then(d => {
        const allStories = d.stories || [];
        const userStories = allStories.filter((s: any) => s.author_id === targetId);
        setMyPosts(userStories);
        setLoadingPosts(false);
      })
      .catch(() => setLoadingPosts(false));

    // If viewing another user
    if (viewingUserId && viewingUserId !== user?.id) {
      fetch(`${BACKEND_URL}/api/sohba/users/${viewingUserId}`, { headers: authHeaders() })
        .then(r => r.json())
        .then(d => setOtherUser(d.user || null))
        .catch(() => {});
    }
  }, [user, viewingUserId]);

  // Load saved stories when tab changes
  useEffect(() => {
    if (activeTab === 'saved' && savedPosts.length === 0 && !loadingSaved) {
      setLoadingSaved(true);
      fetch(`${BACKEND_URL}/api/stories/my-saved`, { headers: authHeaders() })
        .then(r => r.json())
        .then(d => { setSavedPosts(d.stories || []); setLoadingSaved(false); })
        .catch(() => setLoadingSaved(false));
    }
  }, [activeTab]);

  // Load liked stories when tab changes
  useEffect(() => {
    if (activeTab === 'liked' && likedPosts.length === 0 && !loadingLiked) {
      setLoadingLiked(true);
      fetch(`${BACKEND_URL}/api/stories/my-liked`, { headers: authHeaders() })
        .then(r => r.json())
        .then(d => { setLikedPosts(d.stories || []); setLoadingLiked(false); })
        .catch(() => setLoadingLiked(false));
    }
  }, [activeTab]);

  const handleLogout = () => { signOut(); toast.success(t('loggedOut')); navigate('/'); };
  const themeLabel = mode === 'auto' ? t('auto') : mode === 'dark' ? t('dark') : t('light');

  // Not logged in view
  if (!user) return (
    <div className="min-h-screen flex flex-col items-center justify-center px-8 pb-24 bg-background" dir={dir} data-testid="profile-page">
      <div className="h-24 w-24 rounded-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-5">
        <Users className="h-12 w-12 text-primary/40" />
      </div>
      <h2 className="text-xl font-black text-foreground mb-2">{t("welcomeUser")}</h2>
      <p className="text-sm text-muted-foreground text-center mb-8 max-w-[240px]">{t("loginForProfile")}</p>
      <Link to="/auth" className="bg-primary text-primary-foreground px-10 py-3.5 rounded-2xl text-sm font-bold shadow-lg shadow-primary/20 active:scale-95 transition-transform">
        {t("login")}
      </Link>
    </div>
  );

  const isOwnProfile = !viewingUserId || viewingUserId === user.id;
  const profile = isOwnProfile ? user : otherUser;
  const displayName = profile?.name || t('user');
  const displayAvatar = profile?.avatar ? (profile.avatar.startsWith('http') ? profile.avatar : `${BACKEND_URL}${profile.avatar}`) : '';

  const categoryColors: Record<string, string> = {
    prophets: 'from-emerald-500/80 to-emerald-700/80',
    sahaba: 'from-blue-500/80 to-blue-700/80',
    quran: 'from-amber-500/80 to-amber-700/80',
    ruqyah: 'from-purple-500/80 to-purple-700/80',
    rizq: 'from-teal-500/80 to-teal-700/80',
    tawba: 'from-rose-500/80 to-rose-700/80',
    miracles: 'from-indigo-500/80 to-indigo-700/80',
    istighfar: 'from-cyan-500/80 to-cyan-700/80',
    general: 'from-slate-500/80 to-slate-700/80',
    embed: 'from-red-500/80 to-red-700/80',
  };
  const categoryLabels: Record<string, string> = {
    prophets: t('prophets'), sahaba: t('companions'), quran: t('quran'), ruqyah: t('ruqyah'),
    rizq: t('rizq'), tawba: t('repentance'), miracles: t('miracles'), istighfar: t('istighfar'),
    general: t('general'), embed: t('videos'),
  };

  const renderPostGrid = (posts: Post[], loading: boolean, emptyIcon: typeof Settings, emptyMsg: string, emptySubMsg: string) => {
    const EmptyIcon = emptyIcon;
    if (loading) return (
      <div className="flex justify-center py-16">
        <div className="h-6 w-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    );
    if (posts.length === 0) return (
      <div className="text-center py-20 px-8">
        <div className="h-16 w-16 rounded-full bg-primary/5 flex items-center justify-center mx-auto mb-4">
          <EmptyIcon className="h-8 w-8 text-primary/20" />
        </div>
        <p className="text-sm font-bold text-muted-foreground/50">{emptyMsg}</p>
        <p className="text-xs text-muted-foreground/30 mt-1">{emptySubMsg}</p>
      </div>
    );
    return (
      <div className="grid grid-cols-2 gap-3 p-4">
        {posts.map(p => {
          const url = p.image_url ? (p.image_url.startsWith('http') ? p.image_url : `${BACKEND_URL}${p.image_url}`) : null;
          const isVideo = p.media_type === 'video' || (url && /\.(mp4|webm|mov)/i.test(url));
          const isEmbed = p.is_embed || p.media_type === 'embed';
          const catKey = p.category || 'general';
          const gradient = categoryColors[catKey] || categoryColors.general;
          const catLabel = categoryLabels[catKey] || catKey;

          return (
            <Link to={`/stories?story=${p.id}`} key={p.id}
              className="group rounded-2xl overflow-hidden border border-border/20 bg-card shadow-sm hover:shadow-lg hover:border-primary/30 transition-all duration-300">
              {/* Image/Gradient Top */}
              <div className="relative aspect-[4/3] overflow-hidden">
                {url ? (
                  <>
                    <img src={url} alt="" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy"
                      onError={(e) => { e.currentTarget.style.display = 'none'; (e.currentTarget.nextElementSibling as HTMLElement)?.classList.remove('hidden'); }} />
                    <div className="hidden w-full h-full bg-gradient-to-br from-primary/20 to-primary/40 flex items-center justify-center">
                      <BookOpen className="h-8 w-8 text-primary/40" />
                    </div>
                  </>
                ) : (
                  <div className={`w-full h-full bg-gradient-to-br ${gradient} flex items-center justify-center p-4`}>
                    <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.4\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")' }} />
                    <p className="text-white text-[11px] font-bold text-center line-clamp-3 leading-relaxed drop-shadow-sm relative z-10">
                      {p.title || p.content?.slice(0, 60)}
                    </p>
                  </div>
                )}
                {/* Overlay badges */}
                <div className="absolute top-2 right-2">
                  <span className="text-[8px] font-bold bg-black/50 backdrop-blur-sm text-white px-2 py-0.5 rounded-full">
                    {catLabel}
                  </span>
                </div>
                {(isVideo || isEmbed) && (
                  <div className="absolute top-2 left-2 h-6 w-6 rounded-full bg-black/50 backdrop-blur-sm flex items-center justify-center">
                    <Play className="h-3 w-3 text-white fill-white" />
                  </div>
                )}
                {/* Hover overlay */}
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <div className="flex items-center gap-3">
                    <span className="flex items-center gap-1"><Heart className="h-4 w-4 text-white fill-white" /><span className="text-xs text-white font-bold">{p.likes_count || 0}</span></span>
                    <span className="flex items-center gap-1"><Eye className="h-4 w-4 text-white" /><span className="text-xs text-white font-bold">{p.views_count || 0}</span></span>
                  </div>
                </div>
              </div>
              {/* Card Body */}
              <div className="p-3">
                <h3 className="text-[12px] font-bold text-foreground line-clamp-2 leading-relaxed mb-1.5">
                  {p.title || p.content?.slice(0, 50)}
                </h3>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-[10px] text-muted-foreground">
                    <span className="flex items-center gap-0.5"><Heart className="h-3 w-3" />{p.likes_count || 0}</span>
                    <span className="flex items-center gap-0.5"><MessageCircle className="h-3 w-3" />{p.comments_count || 0}</span>
                  </div>
                  <span className="text-[9px] text-muted-foreground/60">{timeAgo(p.created_at)}</span>
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    );
  };

  return (
    <div className="min-h-screen pb-28 bg-background" dir={dir} data-testid="profile-page">
      {/* ===== HEADER BAR ===== */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/10 px-4 h-12 flex items-center justify-between">
        <div className="flex items-center gap-2">
          {!isOwnProfile && (
            <button onClick={goBack} className="p-2 rounded-xl hover:bg-muted/50">
              <ChevronRight className="h-5 w-5 text-foreground" />
            </button>
          )}
          <span className="text-lg font-black text-foreground">{displayName}</span>
        </div>
        <div className="flex items-center gap-0.5 relative">
          {isAdmin && isOwnProfile && (
            <Link to="/admin" className="p-2.5 rounded-xl hover:bg-muted/50" data-testid="admin-link">
              <Shield className="h-[18px] w-[18px] text-primary" />
            </Link>
          )}
          {isOwnProfile && (
            <button onClick={() => setMenuOpen(!menuOpen)} className="p-2.5 rounded-xl hover:bg-muted/50">
              <MoreVertical className="h-[18px] w-[18px] text-muted-foreground" />
            </button>
          )}
          {/* ===== DROPDOWN MENU ===== */}
          <DropdownMenu open={menuOpen} onClose={() => setMenuOpen(false)}>
            <div className="py-1">
              <p className="px-4 py-2 text-[10px] font-bold text-primary/60 uppercase tracking-wider">الإعدادات</p>
              <MenuItem icon={Edit3} label="{t('editProfile')}" to="/account" color="text-primary" />
              <MenuItem icon={mode === 'dark' ? Moon : Sun} label={`المظهر: ${themeLabel}`}
                onClick={() => { setMode(mode === 'auto' ? 'light' : mode === 'light' ? 'dark' : 'auto'); setMenuOpen(false); }}
                color="text-amber-500" />
              <MenuItem icon={Bell} label="الإشعارات" to="/notifications" color="text-red-400" />
              <MenuItem icon={Lock} label="الخصوصية" to="/account" color="text-gray-400" />
            </div>
            <div className="border-t border-border/20 py-1">
              <p className="px-4 py-2 text-[10px] font-bold text-primary/60 uppercase tracking-wider">المساعدة</p>
              <MenuItem icon={HelpCircle} label={t('supportHelp')} onClick={() => { navigate('/contact'); setMenuOpen(false); }} color="text-green-400" />
              <MenuItem icon={Star} label={t('rateApp')} onClick={() => { toast.info(t('thankYouRating')); setMenuOpen(false); }} color="text-yellow-400" />
              <MenuItem icon={Share2} label={t('inviteFriend')} onClick={() => {
                if (navigator.share) navigator.share({ title: displayName, url: window.location.origin });
                else { navigator.clipboard.writeText(window.location.origin); toast.success(t('linkCopied')); }
                setMenuOpen(false);
              }} color="text-blue-400" />
              <MenuItem icon={Info} label={t('aboutApp')} onClick={() => { navigate('/about'); setMenuOpen(false); }} color="text-purple-400" />
            </div>
            <div className="border-t border-border/20 py-1">
              <MenuItem icon={LogOut} label={t('logout')} onClick={handleLogout} color="text-red-500" />
            </div>
          </DropdownMenu>
        </div>
      </div>

      {/* ===== PROFILE HERO ===== */}
      <div className="px-5 pt-6 pb-4">
        <div className="flex items-center gap-5">
          <div className="relative shrink-0">
            <div className="h-[84px] w-[84px] rounded-full bg-gradient-to-br from-primary/40 to-primary/10 p-[3px]">
              <div className="h-full w-full rounded-full bg-card flex items-center justify-center overflow-hidden">
                {displayAvatar ? (
                  <img src={displayAvatar} alt="" className="h-full w-full rounded-full object-cover" onError={(e) => (e.currentTarget.style.display = 'none')} />
                ) : (
                  <span className="text-3xl font-bold text-primary/50">{displayName[0]}</span>
                )}
              </div>
            </div>
            {isOwnProfile && (
              <Link to="/account" className="absolute -bottom-0.5 -left-0.5 h-7 w-7 rounded-full bg-primary flex items-center justify-center border-[2.5px] border-background shadow-md">
                <Edit3 className="h-3 w-3 text-primary-foreground" />
              </Link>
            )}
          </div>

          <div className="flex-1 grid grid-cols-3">
            <div className="text-center">
              <p className="text-[18px] font-black text-foreground leading-tight">{stats.stories || myPosts.length}</p>
              <p className="text-[10px] text-muted-foreground font-medium mt-0.5">{t('story')}</p>
            </div>
            <div className="text-center">
              <p className="text-[18px] font-black text-foreground leading-tight">{stats.followers}</p>
              <p className="text-[10px] text-muted-foreground font-medium mt-0.5">{t('followers')}</p>
            </div>
            <div className="text-center">
              <p className="text-[18px] font-black text-foreground leading-tight">{stats.likes}</p>
              <p className="text-[10px] text-muted-foreground font-medium mt-0.5">{t('likes')}</p>
            </div>
          </div>
        </div>

        <div className="mt-3">
          <p className="text-[14px] font-bold text-foreground">{displayName}</p>
          {isOwnProfile && <p className="text-[11px] text-muted-foreground">{user.email}</p>}
        </div>

        <div className="flex gap-2 mt-4">
          {isOwnProfile ? (
            <>
              <Button variant="outline" className="flex-1 rounded-xl h-10 text-[13px] font-bold border-primary/20 hover:bg-primary/5" asChild>
                <Link to="/account"><Edit3 className="h-3.5 w-3.5 ml-1.5" />{t('editProfile')}</Link>
              </Button>
              <Button variant="outline" className="flex-1 rounded-xl h-10 text-[13px] font-bold border-primary/20 hover:bg-primary/5" onClick={() => {
                if (navigator.share) navigator.share({ title: displayName, url: window.location.origin });
                else { navigator.clipboard.writeText(window.location.origin); toast.success(t('linkCopied')); }
              }}>
                <Share2 className="h-3.5 w-3.5 ml-1.5" />{t('share')}
              </Button>
            </>
          ) : (
            <Button className="flex-1 rounded-xl h-10 text-[13px] font-bold bg-primary">
              <Users className="h-3.5 w-3.5 ml-1.5" />{t('follow')}
            </Button>
          )}
        </div>
      </div>

      {/* ===== QUICK ACTIONS (own profile) ===== */}
      {isOwnProfile && (
        <div className="px-4 mb-4">
          <div className="grid grid-cols-4 gap-2">
            <Link to="/stories" className="flex flex-col items-center gap-1.5 p-3 rounded-2xl bg-card border border-border/20 active:scale-95 transition-transform">
              <BookOpen className="h-5 w-5 text-primary" />
              <span className="text-[9px] font-bold text-foreground">{t('myStories')}</span>
            </Link>
            <Link to="/explore" className="flex flex-col items-center gap-1.5 p-3 rounded-2xl bg-card border border-border/20 active:scale-95 transition-transform">
              <Compass className="h-5 w-5 text-blue-400" />
              <span className="text-[9px] font-bold text-foreground">{t('explore')}</span>
            </Link>
            <Link to="/ai-assistant" className="flex flex-col items-center gap-1.5 p-3 rounded-2xl bg-card border border-border/20 active:scale-95 transition-transform">
              <Bot className="h-5 w-5 text-purple-400" />
              <span className="text-[9px] font-bold text-foreground">{t('assistant')}</span>
            </Link>
            <Link to="/more" className="flex flex-col items-center gap-1.5 p-3 rounded-2xl bg-card border border-border/20 active:scale-95 transition-transform">
              <Sparkles className="h-5 w-5 text-amber-400" />
              <span className="text-[9px] font-bold text-foreground">{t('more')}</span>
            </Link>
          </div>
        </div>
      )}

      {/* ===== CONTENT TABS ===== */}
      <div className="flex border-b border-border/20 sticky top-12 z-40 bg-background">
        <button onClick={() => setActiveTab('posts')}
          className={cn('flex-1 flex items-center justify-center gap-1.5 py-3 border-b-2 transition-all',
            activeTab === 'posts' ? 'border-primary' : 'border-transparent')}>
          <Grid3X3 className={cn('h-[18px] w-[18px]', activeTab === 'posts' ? 'text-primary' : 'text-muted-foreground/50')} />
          <span className={cn('text-[11px] font-bold', activeTab === 'posts' ? 'text-primary' : 'text-muted-foreground/50')}>{t('myStories')}</span>
        </button>
        <button onClick={() => setActiveTab('saved')}
          className={cn('flex-1 flex items-center justify-center gap-1.5 py-3 border-b-2 transition-all',
            activeTab === 'saved' ? 'border-primary' : 'border-transparent')}>
          <Bookmark className={cn('h-[18px] w-[18px]', activeTab === 'saved' ? 'text-primary' : 'text-muted-foreground/50')} />
          <span className={cn('text-[11px] font-bold', activeTab === 'saved' ? 'text-primary' : 'text-muted-foreground/50')}>{t('savedStories')}</span>
          {stats.saved > 0 && <span className="text-[8px] bg-primary/20 text-primary px-1.5 rounded-full font-bold">{stats.saved}</span>}
        </button>
        <button onClick={() => setActiveTab('liked')}
          className={cn('flex-1 flex items-center justify-center gap-1.5 py-3 border-b-2 transition-all',
            activeTab === 'liked' ? 'border-primary' : 'border-transparent')}>
          <Heart className={cn('h-[18px] w-[18px]', activeTab === 'liked' ? 'text-primary' : 'text-muted-foreground/50')} />
          <span className={cn('text-[11px] font-bold', activeTab === 'liked' ? 'text-primary' : 'text-muted-foreground/50')}>{t('likedStories')}</span>
          {stats.liked > 0 && <span className="text-[8px] bg-primary/20 text-primary px-1.5 rounded-full font-bold">{stats.liked}</span>}
        </button>
      </div>

      {/* ===== POSTS/SAVED/LIKED GRID ===== */}
      {activeTab === 'posts' && renderPostGrid(myPosts, loadingPosts, BookOpen, t('noStoriesYetProfile'), t('publishFirst'))}
      {activeTab === 'saved' && renderPostGrid(savedPosts, loadingSaved, Bookmark, t('savedStories'), t('noStoriesYetProfile'))}
      {activeTab === 'liked' && renderPostGrid(likedPosts, loadingLiked, Heart, t('likedStories'), t('noStoriesYetProfile'))}

      {/* ===== VERSION ===== */}
      {isOwnProfile && (
        <p className="text-center text-[10px] text-muted-foreground/30 pb-4 pt-6">{t('appName')} v2.0.0</p>
      )}
    </div>
  );
}
