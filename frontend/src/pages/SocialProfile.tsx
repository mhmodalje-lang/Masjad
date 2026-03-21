import { useState, useEffect } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { ArrowRight, MessageCircle, Settings, Heart, Play, Film, Loader2, Users } from 'lucide-react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function avatar(name: string, img?: string) {
  if (img) return img;
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || '?')}&background=047857&color=fff&size=120&bold=true`;
}

function getMediaUrl(url?: string) {
  if (!url) return null;
  return url.startsWith('http') ? url : `${BACKEND_URL}${url.startsWith('/') ? '' : '/'}${url}`;
}

function formatCount(n: number) {
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return n.toString();
}

export default function SocialProfile() {
  const { t, dir } = useLocale();
  const { userId } = useParams<{ userId: string }>();
  const { user: currentUser, getToken } = useAuth();
  const navigate = useNavigate();
  const [profile, setProfile] = useState<any>(null);
  const [stats, setStats] = useState<any>({});
  const [isFollowing, setIsFollowing] = useState(false);
  const [posts, setPosts] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'posts' | 'info'>('posts');
  const [loading, setLoading] = useState(true);

  const isOwnProfile = currentUser?.id === userId;
  const targetId = isOwnProfile ? currentUser?.id : userId;

  useEffect(() => {
    if (targetId) {
      setLoading(true);
      fetchProfile();
      fetchPosts();
    }
  }, [targetId]);

  const fetchProfile = async () => {
    try {
      const token = getToken();
      const headers: Record<string, string> = {};
      if (token) headers.Authorization = `Bearer ${token}`;
      const res = await fetch(`${BACKEND_URL}/api/sohba/profile/${targetId}`, { headers });
      if (!res.ok) throw new Error('Failed');
      const data = await res.json();
      setProfile(data.profile);
      setStats(data.stats);
      setIsFollowing(data.is_following);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchPosts = async () => {
    try {
      const token = getToken();
      const headers: Record<string, string> = {};
      if (token) headers.Authorization = `Bearer ${token}`;
      const res = await fetch(`${BACKEND_URL}/api/sohba/user/${targetId}/posts?limit=30`, { headers });
      if (!res.ok) throw new Error('Failed');
      const data = await res.json();
      setPosts(data.posts || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleFollow = async () => {
    if (!currentUser) return navigate('/auth');
    const token = getToken();
    try {
      const res = await fetch(`${BACKEND_URL}/api/sohba/follow/${targetId}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setIsFollowing(data.following);
      setStats((prev: any) => ({
        ...prev,
        followers_count: data.following ? prev.followers_count + 1 : prev.followers_count - 1,
      }));
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-emerald-500 animate-spin" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center gap-4 text-muted-foreground">
        <Users className="w-12 h-12 text-muted-foreground/60" />
        <p>{t('userNotFound')}</p>
        <button onClick={() => navigate(-1)} className="text-emerald-500 text-sm font-bold">{t('goBack')}</button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pb-24">
      {/* Cover */}
      <div className="relative h-44 bg-gradient-to-br from-emerald-900 via-emerald-800 to-gray-900 overflow-hidden">
        {profile.cover_image && (
          <img src={profile.cover_image} alt="" className="w-full h-full object-cover" />
        )}
        <div className="absolute inset-0 bg-black/20" />
        {/* Islamic pattern */}
        <div className="absolute inset-0 opacity-[0.06]" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23fff' fill-opacity='.3'%3E%3Cpath d='M40 10L50 30H30z M40 70L30 50H50z M10 40L30 30V50z M70 40L50 50V30z'/%3E%3C/g%3E%3C/svg%3E")`,
        }} />
        <button onClick={() => navigate(-1)}
          className="absolute top-4 right-4 w-9 h-9 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center text-white">
          <ArrowRight className="w-5 h-5" />
        </button>
        {isOwnProfile && (
          <Link to="/account"
            className="absolute top-4 left-4 w-9 h-9 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center text-white">
            <Settings className="w-5 h-5" />
          </Link>
        )}
      </div>

      {/* Avatar & Info */}
      <div className="relative px-5 -mt-14" dir={dir}>
        <div className="flex justify-center">
          <img
            src={avatar(profile.name, profile.avatar)}
            alt={profile.name}
            className="w-[100px] h-[100px] rounded-full border-4 border-[#0a0e13] object-cover shadow-xl"
          />
        </div>
        <div className="text-center mt-3">
          <h1 className="text-foreground text-xl font-bold">{profile.name}</h1>
          {profile.bio && <p className="text-muted-foreground text-sm mt-1 max-w-xs mx-auto">{profile.bio}</p>}
        </div>

        {/* Stats */}
        <div className="flex items-center justify-center gap-8 mt-5">
          <div className="text-center">
            <p className="text-foreground text-lg font-bold">{formatCount(stats.following_count || 0)}</p>
            <p className="text-muted-foreground text-[11px]">{t('follow')}</p>
          </div>
          <div className="text-center">
            <p className="text-foreground text-lg font-bold">{formatCount(stats.followers_count || 0)}</p>
            <p className="text-muted-foreground text-[11px]">{t('followers')}</p>
          </div>
          <div className="text-center">
            <p className="text-foreground text-lg font-bold">{formatCount(stats.likes_count || 0)}</p>
            <p className="text-muted-foreground text-[11px]">{t('likes')}</p>
          </div>
          <div className="text-center">
            <p className="text-foreground text-lg font-bold">{formatCount(stats.gifts_count || 0)}</p>
            <p className="text-muted-foreground text-[11px]">الهدايا</p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3 mt-5 max-w-sm mx-auto">
          {isOwnProfile ? (
            <Link to="/account"
              className="flex-1 py-2.5 rounded-2xl bg-emerald-600 text-white text-center font-bold text-sm hover:bg-emerald-500 transition-colors">
              تعديل الملف الشخصي
            </Link>
          ) : (
            <>
              <button onClick={handleFollow}
                className={`flex-1 py-2.5 rounded-2xl font-bold text-sm flex items-center justify-center gap-2 transition-colors ${
                  isFollowing ? 'bg-muted/30 border border-border/30 text-muted-foreground' : 'bg-emerald-600 text-white'
                }`}>
                {isFollowing ? 'متابَع ✓' : t('follow')}
              </button>
              <Link to="/messages"
                className="flex-1 py-2.5 rounded-2xl bg-muted/30 border border-border/30 text-foreground text-center font-bold text-sm flex items-center justify-center gap-2">
                <MessageCircle className="w-4 h-4" /> المحادثة
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-white/5 mt-6">
        <button onClick={() => setActiveTab('posts')}
          className={`flex-1 py-3 text-center font-bold text-sm transition-colors ${
            activeTab === 'posts' ? 'text-foreground border-b-2 border-primary' : 'text-muted-foreground'
          }`}>
          ال{t('postsCount')}
        </button>
        <button onClick={() => setActiveTab('info')}
          className={`flex-1 py-3 text-center font-bold text-sm transition-colors ${
            activeTab === 'info' ? 'text-foreground border-b-2 border-primary' : 'text-muted-foreground'
          }`}>
          المعلومات
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'posts' ? (
        <div className="grid grid-cols-2 gap-1.5 p-3">
          {posts.length === 0 ? (
            <div className="col-span-2 text-center py-16 text-muted-foreground text-sm">
              لا توجد {t('postsCount')} حتى الآن
            </div>
          ) : (
            posts.map(post => (
              <Link key={post.id} to={`/stories?story=${post.id}`}
                className="relative aspect-[3/4] rounded-2xl overflow-hidden bg-gray-900 group">
                {getMediaUrl(post.image_url || post.thumbnail_url) ? (
                  <img src={getMediaUrl(post.image_url || post.thumbnail_url)!} alt=""
                    className="w-full h-full object-cover" loading="lazy" />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-emerald-900/50 to-gray-900 flex items-center justify-center p-3">
                    <p className="text-muted-foreground text-xs text-center line-clamp-4">{post.content}</p>
                  </div>
                )}
                {(post.content_type?.includes('video') || post.video_url) && (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Play className="w-8 h-8 text-white/60 fill-white/60" />
                  </div>
                )}
                <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 to-transparent p-2">
                  <p className="text-foreground text-[10px] line-clamp-2">{post.content}</p>
                  <div className="flex items-center gap-1 mt-0.5">
                    <Heart className="w-2.5 h-2.5 text-muted-foreground" />
                    <span className="text-muted-foreground text-[9px]">{post.likes_count || 0}</span>
                  </div>
                </div>
              </Link>
            ))
          )}
        </div>
      ) : (
        <div className="p-5" dir={dir}>
          <div className="bg-card border border-border/30 rounded-2xl p-5 space-y-4">
            <div>
              <span className="text-muted-foreground text-xs">{t('nameLabel')}</span>
              <p className="text-foreground font-bold mt-0.5">{profile.name}</p>
            </div>
            {profile.bio && (
              <div>
                <span className="text-muted-foreground text-xs">{t('bio')}</span>
                <p className="text-foreground mt-0.5">{profile.bio}</p>
              </div>
            )}
            <div>
              <span className="text-muted-foreground text-xs">{t('joinDate')}</span>
              <p className="text-white mt-0.5">{profile.created_at ? new Date(profile.created_at).toLocaleDateString('ar-SA') : '-'}</p>
            </div>
            <div>
              <span className="text-muted-foreground text-xs">{t('postsCount')}</span>
              <p className="text-white mt-0.5">{stats.posts_count || 0}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
