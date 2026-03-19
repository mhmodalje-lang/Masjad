import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { Link } from 'react-router-dom';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface RecommendedUser {
  id: string;
  name: string;
  avatar?: string;
  bio?: string;
  followers_count: number;
  posts_count: number;
}

export default function RecommendedUsers() {
  const { user, getToken } = useAuth();
  const [users, setUsers] = useState<RecommendedUser[]>([]);
  const [followedIds, setFollowedIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecommended();
  }, []);

  const fetchRecommended = async () => {
    try {
      const token = getToken();
      const headers: Record<string, string> = {};
      if (token) headers.Authorization = `Bearer ${token}`;
      const res = await fetch(`${BACKEND_URL}/api/sohba/recommended-users?limit=8`, { headers });
      const data = await res.json();
      setUsers(data.users || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFollow = async (targetId: string) => {
    if (!user) return;
    const token = getToken();
    try {
      const res = await fetch(`${BACKEND_URL}/api/sohba/follow/${targetId}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setFollowedIds(prev => {
        const next = new Set(prev);
        if (data.following) next.add(targetId);
        else next.delete(targetId);
        return next;
      });
    } catch (err) {
      console.error(err);
    }
  };

  if (loading || users.length === 0) return null;

  return (
    <div className="py-6 px-4" dir="rtl">
      <h3 className="text-white text-lg font-bold text-center mb-4">مستخدمون موصى بهم</h3>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {users.slice(0, 8).map((u) => (
          <div key={u.id} className="flex flex-col items-center bg-gray-800/50 rounded-xl p-4 gap-2">
            <Link to={`/social-profile/${u.id}`}>
              <img
                src={u.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(u.name)}&background=1a7a4c&color=fff&size=80`}
                alt={u.name}
                className="w-16 h-16 rounded-full border-2 border-emerald-500 object-cover"
              />
            </Link>
            <Link to={`/social-profile/${u.id}`} className="text-white text-sm font-bold text-center truncate w-full hover:underline">
              {u.name}
            </Link>
            <button
              onClick={() => handleFollow(u.id)}
              className={`w-full py-1.5 rounded-lg text-sm font-bold transition-all ${
                followedIds.has(u.id)
                  ? 'bg-gray-700 text-gray-300'
                  : 'bg-emerald-600 text-white hover:bg-emerald-500'
              }`}
            >
              {followedIds.has(u.id) ? 'متابَع ✓' : 'متابعة'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
