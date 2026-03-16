import { useState, useEffect } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { useAdmin } from '@/hooks/useAdmin';
import { useTheme } from '@/components/ThemeProvider';
import {
  Settings, ChevronLeft, Star, Users, Heart,
  LogOut, Shield, Moon, Sun, SunMoon, Globe,
  HelpCircle, Bookmark, Grid3X3, Play, MoreHorizontal,
  Bot, Bell, Gift, Gem, Edit3, Share2, MessageSquare,
  Lock, Palette, ChevronRight, Zap, Crown, ShoppingBag,
  BookOpen, Eye, MessageCircle, Compass, Film,
  type LucideIcon
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';
function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

const avatarColors = ['bg-emerald-600', 'bg-blue-600', 'bg-amber-600', 'bg-purple-600', 'bg-rose-600', 'bg-teal-600'];

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

interface SettingsItem { icon: LucideIcon; label: string; to?: string; onClick?: () => void; badge?: string; value?: string; color?: string; }
function SettingsRow({ icon: Icon, label, to, onClick, badge, value, color }: SettingsItem) {
  const content = (
    <div className="flex items-center justify-between py-3.5 active:bg-muted/30 transition-colors">
      <div className="flex items-center gap-3">
        <div className={cn('h-9 w-9 rounded-xl flex items-center justify-center', color || 'bg-primary/10')}>
          <Icon className={cn('h-[18px] w-[18px]', color ? 'text-white' : 'text-primary')} />
        </div>
        <span className="text-[13px] font-medium text-foreground">{label}</span>
      </div>
      <div className="flex items-center gap-2">
        {badge && <span className="text-[9px] bg-red-500 text-white px-1.5 py-0.5 rounded-full font-bold">{badge}</span>}
        {value && <span className="text-[11px] text-muted-foreground">{value}</span>}
        <ChevronLeft className="h-4 w-4 text-muted-foreground/50" />
      </div>
    </div>
  );
  if (to) return <Link to={to} className="block">{content}</Link>;
  return <div onClick={onClick} className="cursor-pointer">{content}</div>;
}

export default function Profile() {
  const { user, signOut } = useAuth();
  const { isAdmin } = useAdmin();
  const { mode, setMode } = useTheme();
  const navigate = useNavigate();
  const params = useParams();
  const viewingUserId = params.userId;

  const [stats, setStats] = useState({ posts: 0, followers: 0, following: 0, likes: 0 });
  const [myPosts, setMyPosts] = useState<Post[]>([]);
  const [activeTab, setActiveTab] = useState<'posts' | 'saved' | 'liked'>('posts');
  const [loadingPosts, setLoadingPosts] = useState(false);
  const [otherUser, setOtherUser] = useState<any>(null);

  useEffect(() => {
    const targetId = viewingUserId || user?.id;
    if (!targetId) return;
    setLoadingPosts(true);

    // Load stats
    if (!viewingUserId || viewingUserId === user?.id) {
      fetch(`${BACKEND_URL}/api/sohba/my-stats`, { headers: authHeaders() })
        .then(r => r.json())
        .then(d => setStats({ posts: d.posts || 0, followers: d.followers || 0, following: d.following || 0, likes: d.total_likes || 0 }))
        .catch(() => {});
    }

    // Load posts
    fetch(`${BACKEND_URL}/api/stories/list?limit=50`, { headers: authHeaders() })
      .then(r => r.json())
      .then(d => {
        const allStories = d.stories || [];
        const userStories = allStories.filter((s: any) => s.author_id === targetId);
        setMyPosts(userStories);
        setStats(prev => ({ ...prev, posts: userStories.length }));
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

  const handleLogout = () => { signOut(); toast.success('تم تسجيل الخروج'); navigate('/'); };

  const themeLabel = mode === 'auto' ? 'تلقائي' : mode === 'dark' ? 'ليلي' : 'نهاري';
  const ThemeIcon = mode === 'auto' ? SunMoon : mode === 'dark' ? Moon : Sun;

  // Not logged in view
  if (!user) return (
    <div className="min-h-screen flex flex-col items-center justify-center px-8 pb-24 bg-background" dir="rtl" data-testid="profile-page">
      <div className="h-24 w-24 rounded-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-5">
        <Users className="h-12 w-12 text-primary/40" />
      </div>
      <h2 className="text-xl font-black text-foreground mb-2">مرحباً بك</h2>
      <p className="text-sm text-muted-foreground text-center mb-8 max-w-[240px]">سجّل دخولك للوصول لملفك الشخصي وقصصك</p>
      <Link to="/auth" className="bg-primary text-primary-foreground px-10 py-3.5 rounded-2xl text-sm font-bold shadow-lg shadow-primary/20 active:scale-95 transition-transform">
        تسجيل الدخول
      </Link>
    </div>
  );

  const isOwnProfile = !viewingUserId || viewingUserId === user.id;
  const profile = isOwnProfile ? user : otherUser;
  const displayName = profile?.name || 'مستخدم';
  const displayAvatar = profile?.avatar ? (profile.avatar.startsWith('http') ? profile.avatar : `${BACKEND_URL}${profile.avatar}`) : '';

  return (
    <div className="min-h-screen pb-28 bg-background" dir="rtl" data-testid="profile-page">

      {/* ===== HEADER BAR ===== */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/10 px-4 h-12 flex items-center justify-between">
        <div className="flex items-center gap-2">
          {!isOwnProfile && (
            <button onClick={() => navigate(-1)} className="p-2 rounded-xl hover:bg-muted/50">
              <ChevronRight className="h-5 w-5 text-foreground" />
            </button>
          )}
          <span className="text-lg font-black text-foreground">{displayName}</span>
        </div>
        <div className="flex items-center gap-0.5">
          {isAdmin && isOwnProfile && (
            <Link to="/admin" className="p-2.5 rounded-xl hover:bg-muted/50" data-testid="admin-link">
              <Shield className="h-[18px] w-[18px] text-amber-500" />
            </Link>
          )}
          {isOwnProfile && (
            <Link to="/more" className="p-2.5 rounded-xl hover:bg-muted/50">
              <MoreHorizontal className="h-[18px] w-[18px] text-muted-foreground" />
            </Link>
          )}
        </div>
      </div>

      {/* ===== PROFILE HERO ===== */}
      <div className="px-5 pt-6 pb-4">
        <div className="flex items-center gap-5">
          <div className="relative shrink-0">
            <div className="h-[84px] w-[84px] rounded-full bg-gradient-to-br from-primary/30 to-accent/20 p-[3px]">
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
                <Edit3 className="h-3 w-3 text-white" />
              </Link>
            )}
          </div>

          <div className="flex-1 grid grid-cols-3">
            <div className="text-center">
              <p className="text-[18px] font-black text-foreground leading-tight">{stats.posts}</p>
              <p className="text-[10px] text-muted-foreground font-medium mt-0.5">قصة</p>
            </div>
            <div className="text-center">
              <p className="text-[18px] font-black text-foreground leading-tight">{stats.followers}</p>
              <p className="text-[10px] text-muted-foreground font-medium mt-0.5">متابع</p>
            </div>
            <div className="text-center">
              <p className="text-[18px] font-black text-foreground leading-tight">{stats.likes}</p>
              <p className="text-[10px] text-muted-foreground font-medium mt-0.5">إعجاب</p>
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
              <Button variant="outline" className="flex-1 rounded-xl h-10 text-[13px] font-bold border-border/50" asChild>
                <Link to="/account"><Edit3 className="h-3.5 w-3.5 ml-1.5" />تعديل الملف</Link>
              </Button>
              <Button variant="outline" className="flex-1 rounded-xl h-10 text-[13px] font-bold border-border/50" onClick={() => {
                if (navigator.share) navigator.share({ title: displayName, url: window.location.origin });
                else { navigator.clipboard.writeText(window.location.origin); toast.success('تم نسخ الرابط'); }
              }}>
                <Share2 className="h-3.5 w-3.5 ml-1.5" />مشاركة
              </Button>
            </>
          ) : (
            <Button className="flex-1 rounded-xl h-10 text-[13px] font-bold">
              <Users className="h-3.5 w-3.5 ml-1.5" />متابعة
            </Button>
          )}
        </div>
      </div>

      {/* ===== CONTENT TABS ===== */}
      <div className="flex border-b border-border/20 sticky top-12 z-40 bg-background">
        <button onClick={() => setActiveTab('posts')}
          className={cn('flex-1 flex items-center justify-center gap-1.5 py-3 border-b-2 transition-all',
            activeTab === 'posts' ? 'border-foreground' : 'border-transparent')}>
          <Grid3X3 className={cn('h-[18px] w-[18px]', activeTab === 'posts' ? 'text-foreground' : 'text-muted-foreground/50')} />
          <span className={cn('text-[11px] font-bold', activeTab === 'posts' ? 'text-foreground' : 'text-muted-foreground/50')}>قصصي</span>
        </button>
        <button onClick={() => setActiveTab('saved')}
          className={cn('flex-1 flex items-center justify-center gap-1.5 py-3 border-b-2 transition-all',
            activeTab === 'saved' ? 'border-foreground' : 'border-transparent')}>
          <Bookmark className={cn('h-[18px] w-[18px]', activeTab === 'saved' ? 'text-foreground' : 'text-muted-foreground/50')} />
          <span className={cn('text-[11px] font-bold', activeTab === 'saved' ? 'text-foreground' : 'text-muted-foreground/50')}>المحفوظات</span>
        </button>
        <button onClick={() => setActiveTab('liked')}
          className={cn('flex-1 flex items-center justify-center gap-1.5 py-3 border-b-2 transition-all',
            activeTab === 'liked' ? 'border-foreground' : 'border-transparent')}>
          <Heart className={cn('h-[18px] w-[18px]', activeTab === 'liked' ? 'text-foreground' : 'text-muted-foreground/50')} />
          <span className={cn('text-[11px] font-bold', activeTab === 'liked' ? 'text-foreground' : 'text-muted-foreground/50')}>المعجبات</span>
        </button>
      </div>

      {/* ===== POSTS GRID ===== */}
      {activeTab === 'posts' && (
        <div>
          {loadingPosts ? (
            <div className="flex justify-center py-16">
              <div className="h-6 w-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            </div>
          ) : myPosts.length === 0 ? (
            <div className="text-center py-20 px-8">
              <div className="h-16 w-16 rounded-full bg-muted/30 flex items-center justify-center mx-auto mb-4">
                <BookOpen className="h-8 w-8 text-muted-foreground/30" />
              </div>
              <p className="text-sm font-bold text-muted-foreground/50">لا توجد قصص بعد</p>
              <p className="text-xs text-muted-foreground/30 mt-1">شارك أول قصة إسلامية!</p>
              {isOwnProfile && (
                <Link to="/stories?create=true"
                  className="inline-flex items-center gap-1.5 mt-5 bg-primary text-primary-foreground px-6 py-2.5 rounded-xl text-sm font-bold shadow-md shadow-primary/20 active:scale-95 transition-transform">
                  <Zap className="h-3.5 w-3.5" />أنشئ قصة
                </Link>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-[1px] bg-border/10">
              {myPosts.map(p => {
                const url = p.image_url ? (p.image_url.startsWith('http') ? p.image_url : `${BACKEND_URL}${p.image_url}`) : null;
                const isVideo = p.media_type === 'video' || (url && /\.(mp4|webm|mov)/i.test(url));
                const isEmbed = p.is_embed || p.media_type === 'embed';
                return (
                  <Link to={`/stories?story=${p.id}`} key={p.id} className="aspect-square bg-card relative group overflow-hidden">
                    {url ? (
                      <img src={url} alt="" className="w-full h-full object-cover" loading="lazy"
                        onError={(e) => { e.currentTarget.style.display = 'none'; (e.currentTarget.nextElementSibling as HTMLElement)?.classList.remove('hidden'); }} />
                    ) : null}
                    <div className={cn('w-full h-full flex items-center justify-center p-3',
                      url ? 'hidden absolute inset-0' : '',
                      'bg-gradient-to-br from-slate-800/40 to-slate-900/60')}>
                      <p className="text-[9px] text-foreground/70 line-clamp-5 text-center leading-relaxed" dir="rtl">{p.title || p.content}</p>
                    </div>
                    {(isVideo || isEmbed) && <div className="absolute top-2 left-2"><Play className="h-4 w-4 text-white fill-white drop-shadow-lg" /></div>}
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/50 transition-all duration-200 flex items-center justify-center opacity-0 group-hover:opacity-100">
                      <div className="flex items-center gap-4">
                        <span className="flex items-center gap-1"><Heart className="h-4 w-4 text-white fill-white" /><span className="text-xs text-white font-bold">{p.likes_count || 0}</span></span>
                        <span className="flex items-center gap-1"><MessageSquare className="h-4 w-4 text-white fill-white" /><span className="text-xs text-white font-bold">{p.comments_count || 0}</span></span>
                      </div>
                    </div>
                  </Link>
                );
              })}
            </div>
          )}
        </div>
      )}

      {activeTab === 'saved' && (
        <div className="text-center py-20 px-8">
          <div className="h-16 w-16 rounded-full bg-muted/30 flex items-center justify-center mx-auto mb-4">
            <Bookmark className="h-8 w-8 text-muted-foreground/30" />
          </div>
          <p className="text-sm font-bold text-muted-foreground/50">المحفوظات</p>
          <p className="text-xs text-muted-foreground/30 mt-1">القصص المحفوظة ستظهر هنا</p>
        </div>
      )}

      {activeTab === 'liked' && (
        <div className="text-center py-20 px-8">
          <div className="h-16 w-16 rounded-full bg-muted/30 flex items-center justify-center mx-auto mb-4">
            <Heart className="h-8 w-8 text-muted-foreground/30" />
          </div>
          <p className="text-sm font-bold text-muted-foreground/50">القصص التي أعجبتك</p>
          <p className="text-xs text-muted-foreground/30 mt-1">أعجب بقصة وستظهر هنا</p>
        </div>
      )}

      {/* ===== SETTINGS SECTION (own profile only) ===== */}
      {isOwnProfile && (
        <div className="px-4 mt-6 space-y-3">
          <div className="rounded-2xl bg-card border border-border/20 px-4 divide-y divide-border/10">
            <SettingsRow icon={BookOpen} label="حكاياتي" to="/stories" color="bg-gradient-to-br from-emerald-500 to-teal-500" />
            <SettingsRow icon={Compass} label="استكشاف" to="/explore" color="bg-gradient-to-br from-indigo-500 to-blue-500" />
            <SettingsRow icon={Bot} label="المساعد الذكي" to="/ai-assistant" color="bg-gradient-to-br from-purple-500 to-violet-500" />
            <SettingsRow icon={Gift} label="المكافآت والنقاط" to="/rewards" badge="جديد" color="bg-gradient-to-br from-amber-500 to-orange-500" />
            <SettingsRow icon={ShoppingBag} label="المتجر" to="/marketplace" color="bg-gradient-to-br from-blue-500 to-indigo-500" />
          </div>

          <div className="rounded-2xl bg-card border border-border/20 px-4 divide-y divide-border/10">
            <SettingsRow icon={ThemeIcon} label="المظهر" value={themeLabel}
              onClick={() => setMode(mode === 'auto' ? 'light' : mode === 'light' ? 'dark' : 'auto')}
              color="bg-gradient-to-br from-slate-600 to-slate-700" />
            <SettingsRow icon={Bell} label="الإشعارات" to="/messages" color="bg-gradient-to-br from-red-500 to-rose-500" />
            <SettingsRow icon={Lock} label="الخصوصية والأمان" to="/account" color="bg-gradient-to-br from-gray-600 to-gray-700" />
          </div>

          <div className="rounded-2xl bg-card border border-border/20 px-4 divide-y divide-border/10">
            <SettingsRow icon={Star} label="قيّم التطبيق" onClick={() => toast.info('شكراً لتقييمك! ⭐')} color="bg-gradient-to-br from-yellow-500 to-amber-500" />
            <SettingsRow icon={HelpCircle} label="المزيد والمساعدة" to="/more" color="bg-gradient-to-br from-green-500 to-emerald-500" />
          </div>

          <button onClick={handleLogout} data-testid="logout-btn"
            className="w-full flex items-center justify-center gap-2.5 py-3.5 rounded-2xl bg-red-500/5 border border-red-500/15 text-red-500 text-sm font-bold active:scale-[0.98] transition-all mt-4">
            <LogOut className="h-4 w-4" />تسجيل الخروج
          </button>

          <p className="text-center text-[10px] text-muted-foreground/30 pb-4 pt-2">أذان وحكاية v2.0.0</p>
        </div>
      )}
    </div>
  );
}
