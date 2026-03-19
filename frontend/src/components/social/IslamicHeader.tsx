import { Search } from 'lucide-react';
import { Link } from 'react-router-dom';

interface IslamicHeaderProps {
  activeTab: 'trending' | 'video';
  onTabChange: (tab: 'trending' | 'video') => void;
  title?: string;
}

export default function IslamicHeader({ activeTab, onTabChange, title = 'أذان وحكاية' }: IslamicHeaderProps) {
  return (
    <div className="sticky top-0 z-40 bg-gradient-to-b from-emerald-800 to-emerald-700 text-white">
      {/* Islamic Pattern Overlay */}
      <div className="absolute inset-0 opacity-10" style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
      }} />
      
      {/* Lantern Decorations */}
      <div className="absolute top-0 left-4 text-2xl opacity-60 animate-pulse">🏮</div>
      <div className="absolute top-0 right-4 text-2xl opacity-60 animate-pulse" style={{ animationDelay: '1s' }}>🏮</div>
      
      {/* Main Header */}
      <div className="relative flex items-center justify-between px-4 pt-3 pb-2">
        <Link to="/explore" className="p-2 rounded-full hover:bg-white/10 transition-colors">
          <Search className="w-5 h-5" />
        </Link>
        
        <div className="flex items-center gap-6">
          <button
            onClick={() => onTabChange('video')}
            className={`text-base font-bold transition-all pb-1 ${
              activeTab === 'video'
                ? 'text-white border-b-2 border-white'
                : 'text-white/60 hover:text-white/80'
            }`}
          >
            فيديو
          </button>
          <button
            onClick={() => onTabChange('trending')}
            className={`text-base font-bold transition-all pb-1 ${
              activeTab === 'trending'
                ? 'text-white border-b-2 border-white'
                : 'text-white/60 hover:text-white/80'
            }`}
          >
            الترندات
          </button>
          <span className="text-lg font-bold">{title}</span>
        </div>
        
        <div className="w-9" /> {/* Spacer for alignment */}
      </div>
    </div>
  );
}
