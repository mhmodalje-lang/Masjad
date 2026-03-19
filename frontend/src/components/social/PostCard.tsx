import { useState } from 'react';
import { Heart, MessageCircle, Share2, Bookmark, Play } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Post {
  id: string;
  author_id: string;
  author_name: string;
  author_avatar?: string;
  content: string;
  category: string;
  image_url?: string;
  video_url?: string;
  thumbnail_url?: string;
  content_type: string;
  likes_count: number;
  comments_count: number;
  shares_count?: number;
  liked: boolean;
  saved?: boolean;
  created_at: string;
}

interface PostCardProps {
  post: Post;
  onLike?: (postId: string) => void;
  onSave?: (postId: string) => void;
  layout?: 'grid' | 'full';
}

export default function PostCard({ post, onLike, onSave, layout = 'grid' }: PostCardProps) {
  const { user, getToken } = useAuth();
  const [liked, setLiked] = useState(post.liked);
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [saved, setSaved] = useState(post.saved || false);

  const handleLike = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!user) return;
    const token = getToken();
    try {
      const res = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/like`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setLiked(data.liked);
      setLikesCount(prev => data.liked ? prev + 1 : prev - 1);
      onLike?.(post.id);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSave = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!user) return;
    const token = getToken();
    try {
      const res = await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/save`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setSaved(data.saved);
      onSave?.(post.id);
    } catch (err) {
      console.error(err);
    }
  };

  const getImageUrl = (url?: string) => {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return `${BACKEND_URL}${url}`;
  };

  const timeAgo = (dateStr: string) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 60) return `${mins} د`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours} س`;
    const days = Math.floor(hours / 24);
    return `${days} ي`;
  };

  const isVideo = post.content_type?.includes('video') || post.content_type === 'lecture';

  if (layout === 'grid') {
    return (
      <div className="relative group rounded-xl overflow-hidden bg-gray-900 shadow-lg">
        <Link to={isVideo ? `/reels?post=${post.id}` : `/post/${post.id}`}>
          {/* Media */}
          {(post.image_url || post.thumbnail_url) ? (
            <div className="relative aspect-[3/4]">
              <img
                src={getImageUrl(post.thumbnail_url || post.image_url)}
                alt=""
                className="w-full h-full object-cover"
                loading="lazy"
              />
              {isVideo && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/20">
                  <div className="w-12 h-12 rounded-full bg-white/30 backdrop-blur-sm flex items-center justify-center">
                    <Play className="w-6 h-6 text-white fill-white" />
                  </div>
                </div>
              )}
              {/* Gradient overlay for text */}
              <div className="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-black/80 to-transparent" />
              
              {/* Content overlay */}
              <div className="absolute bottom-0 left-0 right-0 p-3" dir="rtl">
                <p className="text-white text-sm font-medium line-clamp-3 leading-relaxed">
                  {post.content}
                </p>
                <div className="flex items-center gap-2 mt-2">
                  <img
                    src={post.author_avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(post.author_name)}&background=1a7a4c&color=fff&size=32`}
                    alt=""
                    className="w-6 h-6 rounded-full border border-white/30"
                  />
                  <span className="text-white/80 text-xs">{post.author_name}</span>
                  <span className="text-white/50 text-xs mr-auto flex items-center gap-1">
                    <Heart className={`w-3 h-3 ${liked ? 'fill-red-500 text-red-500' : ''}`} />
                    {likesCount}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            /* Text-only post */
            <div className="p-4 min-h-[200px] flex flex-col justify-between bg-gradient-to-br from-emerald-900 to-gray-900" dir="rtl">
              <p className="text-white text-sm leading-relaxed line-clamp-6">{post.content}</p>
              <div className="flex items-center gap-2 mt-3">
                <img
                  src={post.author_avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(post.author_name)}&background=1a7a4c&color=fff&size=32`}
                  alt=""
                  className="w-6 h-6 rounded-full border border-white/30"
                />
                <span className="text-white/80 text-xs">{post.author_name}</span>
                <span className="text-white/50 text-xs mr-auto flex items-center gap-1">
                  <Heart className={`w-3 h-3 ${liked ? 'fill-red-500 text-red-500' : ''}`} />
                  {likesCount}
                </span>
              </div>
            </div>
          )}
        </Link>
      </div>
    );
  }

  // Full layout - for detail view
  return (
    <div className="bg-gray-900 rounded-xl overflow-hidden shadow-lg" dir="rtl">
      {/* Author header */}
      <div className="flex items-center gap-3 p-3">
        <Link to={`/social-profile/${post.author_id}`}>
          <img
            src={post.author_avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(post.author_name)}&background=1a7a4c&color=fff&size=40`}
            alt=""
            className="w-10 h-10 rounded-full border-2 border-emerald-500"
          />
        </Link>
        <div className="flex-1">
          <Link to={`/social-profile/${post.author_id}`} className="text-white font-bold text-sm hover:underline">
            {post.author_name}
          </Link>
          <p className="text-gray-400 text-xs">{timeAgo(post.created_at)}</p>
        </div>
      </div>
      
      {/* Content */}
      <p className="text-white px-3 pb-3 text-sm leading-relaxed">{post.content}</p>
      
      {/* Media */}
      {post.image_url && (
        <img src={getImageUrl(post.image_url)} alt="" className="w-full" loading="lazy" />
      )}
      {post.video_url && (
        <video src={getImageUrl(post.video_url)} controls className="w-full" />
      )}
      
      {/* Actions */}
      <div className="flex items-center justify-around p-3 border-t border-gray-800">
        <button onClick={handleLike} className="flex items-center gap-1.5 text-sm">
          <Heart className={`w-5 h-5 ${liked ? 'fill-red-500 text-red-500' : 'text-gray-400'}`} />
          <span className={liked ? 'text-red-500' : 'text-gray-400'}>{likesCount}</span>
        </button>
        <Link to={`/post/${post.id}`} className="flex items-center gap-1.5 text-sm text-gray-400">
          <MessageCircle className="w-5 h-5" />
          <span>{post.comments_count}</span>
        </Link>
        <button className="flex items-center gap-1.5 text-sm text-gray-400">
          <Share2 className="w-5 h-5" />
          <span>{post.shares_count || 0}</span>
        </button>
        <button onClick={handleSave} className="flex items-center gap-1.5 text-sm">
          <Bookmark className={`w-5 h-5 ${saved ? 'fill-yellow-500 text-yellow-500' : 'text-gray-400'}`} />
        </button>
      </div>
    </div>
  );
}
