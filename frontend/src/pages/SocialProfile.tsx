import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { ArrowRight, MessageCircle, Settings, Grid3X3, Info, Play } from 'lucide-react';
import PostCard from '@/components/social/PostCard';
import { Loader2 } from 'lucide-react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

export default function SocialProfile() {
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

  const formatCount = (n: number) => {
    if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
    if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
    return n.toString();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-emerald-500 animate-spin" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
        المستخدم غير موجود
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 pb-20">
      {/* Cover Image */}
      <div className="relative h-48 bg-gradient-to-br from-emerald-900 via-emerald-800 to-gray-900">
        {profile.cover_image && (
          <img src={profile.cover_image} alt="" className="w-full h-full object-cover" />
        )}
        <div className="absolute inset-0 bg-black/30" />
        
        {/* Back button */}
        <button
          onClick={() => navigate(-1)}
          className="absolute top-4 right-4 w-9 h-9 rounded-full bg-black/40 flex items-center justify-center text-white"
        >
          <ArrowRight className="w-5 h-5" />
        </button>
        
        {isOwnProfile && (
          <Link
            to="/account"
            className="absolute top-4 left-4 w-9 h-9 rounded-full bg-black/40 flex items-center justify-center text-white"
          >
            <Settings className="w-5 h-5" />
          </Link>
        )}
      </div>

      {/* Profile Info */}
      <div className="relative px-4 -mt-12" dir="rtl">
        {/* Avatar */}
        <div className="flex justify-center sm:justify-end">
          <img
            src={profile.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(profile.name || '')}&background=1a7a4c&color=fff&size=120`}
            alt={profile.name}
            className="w-24 h-24 rounded-full border-4 border-gray-950 object-cover shadow-lg"
          />
        </div>

        {/* Name & Bio */}
        <div className="text-center mt-3">
          <h1 className="text-white text-xl font-bold">{profile.name}</h1>
          {profile.bio && (
            <p className="text-gray-400 text-sm mt-1 max-w-sm mx-auto">{profile.bio}</p>
          )}
        </div>

        {/* Stats */}
        <div className="flex items-center justify-center gap-6 mt-5">
          <div className="text-center">
            <p className="text-white text-lg font-bold">{formatCount(stats.following_count || 0)}</p>
            <p className="text-gray-500 text-xs">متابعة</p>
          </div>
          <div className="text-center">
            <p className="text-white text-lg font-bold">{formatCount(stats.followers_count || 0)}</p>
            <p className="text-gray-500 text-xs">متابعين</p>
          </div>
          <div className="text-center">
            <p className="text-white text-lg font-bold">{formatCount(stats.likes_count || 0)}</p>
            <p className="text-gray-500 text-xs">الإعجابات</p>
          </div>
          <div className="text-center">
            <p className="text-white text-lg font-bold">{formatCount(stats.gifts_count || 0)}</p>
            <p className="text-gray-500 text-xs">الهدايا</p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3 mt-5 max-w-md mx-auto">
          {isOwnProfile ? (
            <Link
              to="/account"
              className="flex-1 py-2.5 rounded-xl bg-emerald-600 text-white text-center font-bold text-sm hover:bg-emerald-500 transition-colors"
            >
              تعديل الملف الشخصي
            </Link>
          ) : (
            <>
              <button
                onClick={handleFollow}
                className={`flex-1 py-2.5 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-colors ${
                  isFollowing
                    ? 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                    : 'bg-emerald-600 text-white hover:bg-emerald-500'
                }`}
              >
                {isFollowing ? 'متابَع ✓' : '+ متابعة'}
              </button>
              <Link
                to="/messages"
                className="flex-1 py-2.5 rounded-xl bg-gray-800 text-white text-center font-bold text-sm flex items-center justify-center gap-2 hover:bg-gray-700 transition-colors"
              >
                <MessageCircle className="w-4 h-4" />
                المحادثة
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Content Tabs */}
      <div className="flex border-b border-gray-800 mt-6">
        <button
          onClick={() => setActiveTab('posts')}
          className={`flex-1 py-3 text-center font-bold text-sm transition-colors ${
            activeTab === 'posts'
              ? 'text-white border-b-2 border-emerald-500'
              : 'text-gray-500 hover:text-gray-300'
          }`}
        >
          المنشورات
        </button>
        <button
          onClick={() => setActiveTab('info')}
          className={`flex-1 py-3 text-center font-bold text-sm transition-colors ${
            activeTab === 'info'
              ? 'text-white border-b-2 border-emerald-500'
              : 'text-gray-500 hover:text-gray-300'
          }`}
        >
          المعلومات
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'posts' ? (
        <div className="grid grid-cols-2 gap-1 p-1">
          {posts.length === 0 ? (
            <div className="col-span-2 text-center py-12 text-gray-500">
              لا توجد منشورات حتى الآن
            </div>
          ) : (
            posts.map((post) => (
              <PostCard key={post.id} post={post} layout="grid" />
            ))
          )}
        </div>
      ) : (
        <div className="p-4" dir="rtl">
          <div className="bg-gray-900 rounded-xl p-4 space-y-3">
            <div>
              <span className="text-gray-500 text-sm">الاسم</span>
              <p className="text-white">{profile.name}</p>
            </div>
            {profile.bio && (
              <div>
                <span className="text-gray-500 text-sm">النبذة</span>
                <p className="text-white">{profile.bio}</p>
              </div>
            )}
            <div>
              <span className="text-gray-500 text-sm">تاريخ الانضمام</span>
              <p className="text-white">{new Date(profile.created_at).toLocaleDateString('ar-SA')}</p>
            </div>
            <div>
              <span className="text-gray-500 text-sm">عدد المنشورات</span>
              <p className="text-white">{stats.posts_count || 0}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
