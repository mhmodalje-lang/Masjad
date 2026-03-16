import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { useAdmin } from '@/hooks/useAdmin';
import { useTheme } from '@/components/ThemeProvider';
import {
  Settings, ChevronLeft, Star, Users, Heart,
  LogOut, Shield, Moon, Sun, SunMoon, Globe,
  HelpCircle, Share2, MessageSquare, Bookmark,
  Crown, Gift, Gem, Grid3X3, Play, MoreHorizontal,
  Bot, Compass, Calculator, BookOpen, Clock, Bell,
  ShoppingBag, Store, CheckCircle2, ShieldCheck,
  type LucideIcon
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken();
  if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

interface QuickLinkProps { icon: LucideIcon; label: string; to?: string; onClick?: () => void; badge?: string; }
function QuickLink({ icon: Icon, label, to, onClick, badge }: QuickLinkProps) {
  const inner = (
    <div className="flex items-center justify-between py-3.5 px-1 border-b border-border/20 last:border-0 active:bg-muted/30 transition-colors">
      <div className="flex items-center gap-3">
        <div className="h-9 w-9 rounded-xl bg-primary/8 flex items-center justify-center">
          <Icon className="h-[18px] w-[18px] text-primary" />
        </div>
        <span className="text-sm font-medium text-foreground">{label}</span>
      </div>
      <div className="flex items-center gap-2">
        {badge && <span className="text-[10px] bg-primary/10 text-primary px-2 py-0.5 rounded-full font-bold">{badge}</span>}
        <ChevronLeft className="h-4 w-4 text-muted-foreground" />
      </div>
    </div>
  );
  if (to) return <Link to={to}>{inner}</Link>;
  return <div onClick={onClick} className="cursor-pointer">{inner}</div>;
}

interface Post {
  id: string; content: string; image_url?: string; media_type?: string;
  likes_count: number; comments_count: number;
}

export default function Profile() {
  const { user, signOut } = useAuth();
  const { isAdmin } = useAdmin();
  const { theme, mode, setMode } = useTheme();
  const navigate = useNavigate();
  const [stats, setStats] = useState({ posts: 0, followers: 0, following: 0 });
  const [myPosts, setMyPosts] = useState<Post[]>([]);
  const [activeView, setActiveView] = useState<'grid' | 'saved'>('grid');

  useEffect(() => {
    if (!user) return;
    fetch(`${BACKEND_URL}/api/sohba/my-stats`, { headers: authHeaders() })
      .then(r => r.json())
      .then(d => setStats({ posts: d.posts || 0, followers: d.followers || 0, following: d.following || 0 }))
      .catch(() => {});
    fetch(`${BACKEND_URL}/api/sohba/posts?author=${user.id}&limit=50`, { headers: authHeaders() })
      .then(r => r.json())
      .then(d => setMyPosts(d.posts || []))
      .catch(() => {});
  }, [user]);

  const handleLogout = () => {
    signOut();
    toast.success('تم تسجيل الخروج');
    navigate('/');
  };

  const themeLabel = mode === 'auto' ? 'تلقائي' : mode === 'dark' ? 'ليلي' : 'نهاري';
  const ThemeIcon = mode === 'auto' ? SunMoon : mode === 'dark' ? Moon : Sun;

  if (!user) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-8 pb-24" dir="rtl" data-testid="profile-page">
        <div className="h-20 w-20 rounded-full bg-muted/50 flex items-center justify-center mb-4">
          <Users className="h-10 w-10 text-muted-foreground/40" />
        </div>
        <h2 className="text-lg font-bold text-foreground mb-1">مرحباً بك</h2>
        <p className="text-sm text-muted-foreground text-center mb-6">سجّل دخولك لعرض ملفك الشخصي</p>
        <Link to="/auth" className="bg-primary text-primary-foreground px-8 py-3 rounded-2xl text-sm font-bold active:scale-95 transition-transform">
          تسجيل الدخول
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="profile-page">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-12 flex items-center justify-between">
        <span className="text-base font-bold text-foreground">{user?.name || 'حسابي'}</span>
        <div className="flex items-center gap-1">
          {isAdmin && (
            <Link to="/admin" className="p-2 rounded-xl hover:bg-muted/50" data-testid="admin-link">
              <Shield className="h-[18px] w-[18px] text-amber-500" />
            </Link>
          )}
          <Link to="/more" className="p-2 rounded-xl hover:bg-muted/50" data-testid="more-link">
            <MoreHorizontal className="h-[18px] w-[18px] text-muted-foreground" />
          </Link>
        </div>
      </div>

      {/* Profile Info (Instagram style) */}
      <div className="px-5 py-5">
        <div className="flex items-center gap-5">
          <div className="relative shrink-0">
            <div className="h-20 w-20 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 border-[3px] border-primary/30 flex items-center justify-center overflow-hidden">
              {user?.avatar ? (
                <img src={user.avatar} alt="" className="h-full w-full rounded-full object-cover" />
              ) : (
                <span className="text-3xl text-primary/60">{user?.name?.[0] || user?.email?.[0] || '؟'}</span>
              )}
            </div>
          </div>
          <div className="flex-1 flex justify-around">
            <div className="text-center"><p className="text-lg font-bold text-foreground">{stats.posts}</p><p className="text-[11px] text-muted-foreground">منشور</p></div>
            <div className="text-center"><p className="text-lg font-bold text-foreground">{stats.followers}</p><p className="text-[11px] text-muted-foreground">متابع</p></div>
            <div className="text-center"><p className="text-lg font-bold text-foreground">{stats.following}</p><p className="text-[11px] text-muted-foreground">متابَع</p></div>
          </div>
        </div>

        <div className="mt-3">
          <p className="text-sm font-bold text-foreground">{user?.name || 'مستخدم'}</p>
          <p className="text-xs text-muted-foreground">{user?.email}</p>
        </div>

        <div className="flex gap-2 mt-4">
          <Button variant="outline" className="flex-1 rounded-xl h-9 text-sm font-bold" asChild>
            <Link to="/account">تعديل الملف</Link>
          </Button>
          <Button variant="outline" className="flex-1 rounded-xl h-9 text-sm font-bold" onClick={() => {
            if (navigator.share) navigator.share({ title: 'المؤذن العالمي', url: window.location.origin });
            else { navigator.clipboard.writeText(window.location.origin); toast.success('تم نسخ الرابط'); }
          }}>مشاركة</Button>
        </div>
      </div>

      {/* Content Tabs */}
      <div className="flex border-b border-border/20">
        <button onClick={() => setActiveView('grid')}
          className={cn('flex-1 flex items-center justify-center py-3 border-b-2 transition-all',
            activeView === 'grid' ? 'border-foreground' : 'border-transparent')}>
          <Grid3X3 className={cn('h-5 w-5', activeView === 'grid' ? 'text-foreground' : 'text-muted-foreground')} />
        </button>
        <button onClick={() => setActiveView('saved')}
          className={cn('flex-1 flex items-center justify-center py-3 border-b-2 transition-all',
            activeView === 'saved' ? 'border-foreground' : 'border-transparent')}>
          <Bookmark className={cn('h-5 w-5', activeView === 'saved' ? 'text-foreground' : 'text-muted-foreground')} />
        </button>
      </div>

      {/* Posts Grid */}
      {activeView === 'grid' && (
        <div>
          {myPosts.length === 0 ? (
            <div className="text-center py-16 px-8">
              <Grid3X3 className="h-12 w-12 text-muted-foreground/20 mx-auto mb-3" />
              <p className="text-sm text-muted-foreground">لا توجد منشورات بعد</p>
              <Link to="/sohba?create=true" className="inline-block mt-4 bg-primary text-primary-foreground px-6 py-2.5 rounded-xl text-sm font-bold">
                أنشئ أول منشور
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-0.5">
              {myPosts.map(p => {
                const url = p.image_url ? (p.image_url.startsWith('http') ? p.image_url : `${BACKEND_URL}${p.image_url}`) : null;
                const isVideoPost = p.media_type === 'video' || (url && /\.(mp4|webm|mov)/i.test(url));
                return (
                  <div key={p.id} className="aspect-square bg-muted overflow-hidden relative group cursor-pointer">
                    {url ? <img src={url} alt="" className="w-full h-full object-cover" loading="lazy" /> : (
                      <div className="w-full h-full flex items-center justify-center p-2 bg-gradient-to-br from-emerald-900/20 to-teal-900/20">
                        <p className="text-[9px] text-muted-foreground line-clamp-4 text-center" dir="rtl">{p.content}</p>
                      </div>
                    )}
                    {isVideoPost && <div className="absolute top-1.5 left-1.5"><Play className="h-3.5 w-3.5 text-white fill-white drop-shadow-md" /></div>}
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                      <div className="flex items-center gap-3">
                        <div className="flex items-center gap-1"><Heart className="h-4 w-4 text-white fill-white" /><span className="text-xs text-white font-bold">{p.likes_count || 0}</span></div>
                        <div className="flex items-center gap-1"><MessageSquare className="h-4 w-4 text-white fill-white" /><span className="text-xs text-white font-bold">{p.comments_count || 0}</span></div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {activeView === 'saved' && (
        <div className="text-center py-16 px-8">
          <Bookmark className="h-12 w-12 text-muted-foreground/20 mx-auto mb-3" />
          <p className="text-sm text-muted-foreground">المحفوظات ستظهر هنا</p>
        </div>
      )}

      {/* Quick Settings */}
      <div className="px-5 mt-4 mb-4">
        <div className="rounded-2xl bg-card border border-border/30 p-3">
          <QuickLink icon={Bookmark} label="المحفوظات" to="/sohba" />
          <QuickLink icon={Gift} label="المكافآت" to="/rewards" badge="جديد" />
          <QuickLink icon={ThemeIcon} label={`المظهر: ${themeLabel}`}
            onClick={() => setMode(mode === 'auto' ? 'light' : mode === 'light' ? 'dark' : 'auto')} />
          <QuickLink icon={Bell} label="الإشعارات" to="/notifications" />
          <QuickLink icon={Bot} label="المساعد الذكي" to="/ai-assistant" />
          <QuickLink icon={Star} label="قيّمنا" onClick={() => toast.info('شكراً لدعمك!')} />
          <QuickLink icon={HelpCircle} label="المزيد والإعدادات" to="/more" />
        </div>
      </div>

      {/* Logout */}
      <div className="px-5 mb-8">
        <button onClick={handleLogout} data-testid="logout-btn"
          className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl border border-red-500/20 bg-red-500/5 text-red-500 text-sm font-bold transition-all active:scale-[0.98]">
          <LogOut className="h-4 w-4" />تسجيل الخروج
        </button>
      </div>
    </div>
  );
}
