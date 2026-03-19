import { useState, useEffect, useCallback } from 'react';
import IslamicHeader from '@/components/social/IslamicHeader';
import CategoryTabs from '@/components/social/CategoryTabs';
import PostCard from '@/components/social/PostCard';
import RecommendedUsers from '@/components/social/RecommendedUsers';
import { useAuth } from '@/hooks/useAuth';
import { Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

export default function SocialHome() {
  const { user, getToken } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'trending' | 'video'>('trending');
  const [activeCategory, setActiveCategory] = useState('foryou');
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const fetchPosts = useCallback(async (pageNum: number = 1, append: boolean = false) => {
    setLoading(pageNum === 1);
    try {
      const token = getToken();
      const headers: Record<string, string> = {};
      if (token) headers.Authorization = `Bearer ${token}`;

      let url = '';
      if (activeTab === 'video') {
        url = `${BACKEND_URL}/api/sohba/feed/videos?page=${pageNum}&limit=20`;
      } else if (activeCategory === 'following') {
        url = `${BACKEND_URL}/api/sohba/feed/following?page=${pageNum}&limit=20`;
      } else if (activeCategory === 'foryou') {
        url = `${BACKEND_URL}/api/sohba/explore?page=${pageNum}&limit=20`;
      } else {
        const catMap: Record<string, string> = {
          'islamic': 'general',
          'featured': 'all',
          'quran': 'quran',
          'hadith': 'hadith',
          'stories': 'stories',
          'family': 'family',
        };
        const cat = catMap[activeCategory] || 'all';
        url = `${BACKEND_URL}/api/sohba/posts?category=${cat}&page=${pageNum}&limit=20`;
      }

      const res = await fetch(url, { headers });
      const data = await res.json();
      const newPosts = data.posts || [];

      if (append) {
        setPosts(prev => [...prev, ...newPosts]);
      } else {
        setPosts(newPosts);
      }
      setHasMore(data.has_more || false);
      setPage(pageNum);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [activeTab, activeCategory, getToken]);

  useEffect(() => {
    fetchPosts(1, false);
  }, [activeTab, activeCategory]);

  const handleLoadMore = () => {
    if (hasMore && !loading) {
      fetchPosts(page + 1, true);
    }
  };

  const handleTabChange = (tab: 'trending' | 'video') => {
    setActiveTab(tab);
    if (tab === 'video') {
      navigate('/reels');
    }
  };

  return (
    <div className="min-h-screen bg-gray-950">
      <IslamicHeader activeTab={activeTab} onTabChange={handleTabChange} />
      
      {activeTab === 'trending' && (
        <CategoryTabs activeCategory={activeCategory} onCategoryChange={setActiveCategory} />
      )}

      {/* Content */}
      <div className="pb-20">
        {loading && posts.length === 0 ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 text-emerald-500 animate-spin" />
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-8" dir="rtl">
            <p className="text-gray-400 text-base mb-6">
              لا يوجد محتوى حتى الآن، تابع بعض المستخدمين الموصى بهم!
            </p>
            <RecommendedUsers />
          </div>
        ) : (
          <>
            {/* Posts Grid */}
            <div className="grid grid-cols-2 gap-1 p-1">
              {posts.map((post) => (
                <PostCard key={post.id} post={post} layout="grid" />
              ))}
            </div>
            
            {/* Load More */}
            {hasMore && (
              <div className="flex justify-center py-6">
                <button
                  onClick={handleLoadMore}
                  disabled={loading}
                  className="px-6 py-2 bg-emerald-600 text-white rounded-full text-sm font-bold hover:bg-emerald-500 transition-colors disabled:opacity-50"
                >
                  {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'عرض المزيد'}
                </button>
              </div>
            )}

            {/* Always show recommended users at bottom */}
            <RecommendedUsers />
          </>
        )}
      </div>
    </div>
  );
}
