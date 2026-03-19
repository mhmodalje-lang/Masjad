import { useRef, useEffect } from 'react';

const CATEGORIES = [
  { key: 'following', label: 'متابعة' },
  { key: 'foryou', label: 'من أجلك' },
  { key: 'islamic', label: 'إسلامي' },
  { key: 'featured', label: 'مميز' },
  { key: 'quran', label: 'القرآن' },
  { key: 'hadith', label: 'الحديث' },
  { key: 'stories', label: 'قصص وعبر' },
  { key: 'family', label: 'الأسرة' },
];

interface CategoryTabsProps {
  activeCategory: string;
  onCategoryChange: (category: string) => void;
}

export default function CategoryTabs({ activeCategory, onCategoryChange }: CategoryTabsProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (scrollRef.current) {
      const activeEl = scrollRef.current.querySelector(`[data-category="${activeCategory}"]`);
      if (activeEl) {
        activeEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    }
  }, [activeCategory]);
  
  return (
    <div className="bg-emerald-700/90 backdrop-blur-sm">
      <div
        ref={scrollRef}
        className="flex items-center gap-1 px-3 py-2 overflow-x-auto scrollbar-hide"
        dir="rtl"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {CATEGORIES.map((cat) => (
          <button
            key={cat.key}
            data-category={cat.key}
            onClick={() => onCategoryChange(cat.key)}
            className={`shrink-0 px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
              activeCategory === cat.key
                ? 'bg-white text-emerald-800 shadow-md'
                : 'text-white/80 hover:text-white hover:bg-white/10'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>
    </div>
  );
}
