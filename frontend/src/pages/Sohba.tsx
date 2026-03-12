import { useState } from 'react';
import { Users, TrendingUp, Search, Heart, MessageCircle, Share2, Bookmark, Plus, Image, Video, Hash } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';

const tabs = [
  { key: 'forYou', label: 'من أجلك' },
  { key: 'following', label: 'متابعة' },
  { key: 'ramadan', label: 'رمضان' },
  { key: 'featured', label: 'مميز' },
  { key: 'faith', label: 'تقوية الإيمان' },
  { key: 'hajj', label: 'الحج والعمرة' },
  { key: 'halal', label: 'السفر الحلال' },
];

const trendingTags = [
  { tag: '#لحظات_رمضان', count: '12.5K' },
  { tag: '#ليلة_القدر', count: '8.2K' },
  { tag: '#مذكرة_الصيام', count: '5.7K' },
  { tag: '#رمضان_2026', count: '15.3K' },
  { tag: '#أذكار_المساء', count: '3.1K' },
];

interface Post {
  id: string;
  author: string;
  avatar: string;
  time: string;
  content: string;
  image?: string;
  likes: number;
  comments: number;
  shares: number;
  liked: boolean;
  saved: boolean;
  tags?: string[];
}

const samplePosts: Post[] = [
  {
    id: '1',
    author: 'جليسة القرآن',
    avatar: 'ج',
    time: 'منذ 2 ساعة',
    content: 'يقول ﷺ: "ما من عبد يتعار من الليل فيقول: لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير، سبحان الله، والحمد لله، ولا إله إلا الله، والله أكبر، ولا حول ولا قوة إلا بالله"',
    likes: 160,
    comments: 23,
    shares: 45,
    liked: false,
    saved: false,
    tags: ['#أذكار', '#قيام_الليل'],
  },
  {
    id: '2',
    author: 'Sara Ali',
    avatar: 'S',
    time: 'منذ 4 ساعات',
    content: 'لا تنسوا في العشر الأواخر أن تدعوا بدعاء سيدنا عمر رضي الله عنه:\n"اللهم اجعلني من عتقائك من النار في هذا الشهر الكريم"',
    likes: 431,
    comments: 56,
    shares: 120,
    liked: true,
    saved: true,
    tags: ['#ليلة_القدر', '#رمضان_2026'],
  },
  {
    id: '3',
    author: 'KENAN',
    avatar: 'K',
    time: 'منذ 6 ساعات',
    content: 'قال الله عن ليلة القدر:\n﴿فيها يُفرق كل أمر حكيم﴾\nليلة واحدة تساوي عمراً كاملاً من العبادة. لا تفوّتوها!',
    likes: 290,
    comments: 34,
    shares: 89,
    liked: false,
    saved: false,
    tags: ['#ليلة_القدر'],
  },
];

function PostCard({ post, onToggleLike, onToggleSave }: { post: Post; onToggleLike: () => void; onToggleSave: () => void }) {
  const avatarColors = ['bg-emerald-600', 'bg-blue-600', 'bg-amber-600', 'bg-purple-600', 'bg-rose-600'];
  const colorIdx = post.author.charCodeAt(0) % avatarColors.length;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-card border-b border-border/30 p-4"
    >
      {/* Author */}
      <div className="flex items-center gap-3 mb-3">
        <div className={cn('h-10 w-10 rounded-full flex items-center justify-center text-white text-sm font-bold', avatarColors[colorIdx])}>
          {post.avatar}
        </div>
        <div className="flex-1">
          <p className="text-sm font-bold text-foreground">{post.author}</p>
          <p className="text-[10px] text-muted-foreground">{post.time}</p>
        </div>
      </div>

      {/* Content */}
      <p className="text-sm text-foreground leading-relaxed whitespace-pre-line mb-2 font-arabic">
        {post.content}
      </p>

      {/* Tags */}
      {post.tags && post.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {post.tags.map(tag => (
            <span key={tag} className="text-[11px] text-primary font-medium">{tag}</span>
          ))}
        </div>
      )}

      {/* Image placeholder */}
      {post.image && (
        <div className="rounded-2xl bg-muted h-48 mb-3 overflow-hidden">
          <img src={post.image} alt="" className="w-full h-full object-cover" />
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-between pt-2 border-t border-border/20">
        <button
          onClick={onToggleLike}
          className={cn('flex items-center gap-1.5 text-xs transition-all', post.liked ? 'text-red-500' : 'text-muted-foreground')}
        >
          <Heart className={cn('h-4.5 w-4.5', post.liked && 'fill-current')} />
          <span className="font-medium">{post.likes}</span>
        </button>
        <button className="flex items-center gap-1.5 text-xs text-muted-foreground">
          <MessageCircle className="h-4.5 w-4.5" />
          <span className="font-medium">{post.comments}</span>
        </button>
        <button className="flex items-center gap-1.5 text-xs text-muted-foreground">
          <Share2 className="h-4.5 w-4.5" />
          <span className="font-medium">{post.shares}</span>
        </button>
        <button
          onClick={onToggleSave}
          className={cn('flex items-center gap-1.5 text-xs transition-all', post.saved ? 'text-primary' : 'text-muted-foreground')}
        >
          <Bookmark className={cn('h-4.5 w-4.5', post.saved && 'fill-current')} />
        </button>
      </div>
    </motion.div>
  );
}

export default function Sohba() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('forYou');
  const [posts, setPosts] = useState(samplePosts);
  const [showTrending, setShowTrending] = useState(false);

  const toggleLike = (id: string) => {
    setPosts(prev => prev.map(p => p.id === id ? { ...p, liked: !p.liked, likes: p.liked ? p.likes - 1 : p.likes + 1 } : p));
  };

  const toggleSave = (id: string) => {
    setPosts(prev => prev.map(p => p.id === id ? { ...p, saved: !p.saved } : p));
    toast.success('تم الحفظ');
  };

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="sohba-page">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-card/95 backdrop-blur-xl border-b border-border/30">
        <div className="flex items-center justify-between px-4 py-3 pt-safe-header">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-primary" />
            <h1 className="text-lg font-bold text-foreground">صُحبة</h1>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowTrending(!showTrending)}
              className="p-2 rounded-xl bg-muted/50 transition-all active:scale-95"
              data-testid="trending-btn"
            >
              <TrendingUp className="h-4.5 w-4.5 text-muted-foreground" />
            </button>
            <button className="p-2 rounded-xl bg-muted/50 transition-all active:scale-95">
              <Search className="h-4.5 w-4.5 text-muted-foreground" />
            </button>
          </div>
        </div>

        {/* Tabs scrollable */}
        <div className="flex gap-1 px-4 pb-2 overflow-x-auto no-scrollbar">
          {tabs.map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              data-testid={`sohba-tab-${tab.key}`}
              className={cn(
                'shrink-0 px-4 py-1.5 rounded-full text-xs font-bold transition-all',
                activeTab === tab.key
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted/50 text-muted-foreground'
              )}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Trending Tags */}
      <AnimatePresence>
        {showTrending && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden bg-card border-b border-border/30"
          >
            <div className="p-4">
              <h3 className="text-xs font-bold text-muted-foreground mb-2 flex items-center gap-1.5">
                <Hash className="h-3.5 w-3.5" />
                الوسوم الرائجة
              </h3>
              <div className="flex flex-wrap gap-2">
                {trendingTags.map(t => (
                  <span key={t.tag} className="inline-flex items-center gap-1 bg-primary/8 text-primary text-[11px] font-bold px-3 py-1.5 rounded-full">
                    {t.tag}
                    <span className="text-primary/50 text-[9px]">{t.count}</span>
                  </span>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Posts Feed */}
      <div>
        {posts.map(post => (
          <PostCard
            key={post.id}
            post={post}
            onToggleLike={() => toggleLike(post.id)}
            onToggleSave={() => toggleSave(post.id)}
          />
        ))}
      </div>

      {/* Empty state for other tabs */}
      {activeTab !== 'forYou' && (
        <div className="p-8 text-center">
          <Users className="h-12 w-12 text-muted-foreground/30 mx-auto mb-3" />
          <p className="text-sm font-bold text-muted-foreground">قريباً</p>
          <p className="text-xs text-muted-foreground/60 mt-1">محتوى هذا القسم قيد التطوير</p>
        </div>
      )}

      {/* FAB - Create Post */}
      {user && (
        <button
          data-testid="create-post-btn"
          onClick={() => toast.info('ميزة النشر قريباً')}
          className="fixed bottom-20 left-5 z-40 h-14 w-14 rounded-full bg-primary text-primary-foreground shadow-lg shadow-primary/30 flex items-center justify-center transition-all active:scale-90 hover:shadow-xl"
        >
          <Plus className="h-6 w-6" />
        </button>
      )}
    </div>
  );
}
