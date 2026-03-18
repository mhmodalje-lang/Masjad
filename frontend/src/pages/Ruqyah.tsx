import { useState, useEffect } from 'react';
import { ChevronLeft, ChevronDown, Play, Video, Volume2, X } from 'lucide-react';
import { useSmartBack } from '@/hooks/useSmartBack';
import { useLocale } from '@/hooks/useLocale';
import { motion, AnimatePresence } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

const RUQYAH_CATEGORIES = [
  { key: '', label: 'الكل', emoji: '📋' },
  { key: 'عام', label: 'عام', emoji: '📖' },
  { key: 'general', label: 'عامة', emoji: '📖' },
  { key: 'عين', label: 'عين', emoji: '👁' },
  { key: 'حسد', label: 'حسد', emoji: '🧿' },
  { key: 'سحر', label: 'سحر', emoji: '⚡' },
  { key: 'مس', label: 'مس', emoji: '🔥' },
  { key: 'أرق', label: 'أرق', emoji: '😴' },
  { key: 'وسواس', label: 'وسواس', emoji: '💭' },
  { key: 'حماية', label: 'حماية', emoji: '🛡' },
];

const CATEGORY_ICONS: Record<string, string> = {
  'حماية': '🛡',
  'عام': '📖',
  'general': '📖',
  'عين': '👁',
  'حسد': '🧿',
  'سحر': '⚡',
  'مس': '🔥',
  'أرق': '😴',
  'وسواس': '💭',
};

const STATIC_RUQYAH = [
  {
    id: 'ayat-kursi', title: 'آية الكرسي', subtitle: 'للحفظ والحماية', icon: '🛡',
    arabic: 'اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَّهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ',
    reference: 'البقرة: 255', category: 'حماية',
  },
  {
    id: 'falaq', title: 'سورة الفلق', subtitle: 'من شر ما خلق', icon: '🧿',
    arabic: 'قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ ۝ مِن شَرِّ مَا خَلَقَ ۝ وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ ۝ وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ ۝ وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ',
    reference: 'الفلق: 1-5', category: 'حسد',
  },
  {
    id: 'nas', title: 'سورة الناس', subtitle: 'من شر الوسواس', icon: '💭',
    arabic: 'قُلْ أَعُوذُ بِرَبِّ النَّاسِ ۝ مَلِكِ النَّاسِ ۝ إِلَٰهِ النَّاسِ ۝ مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ ۝ الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ ۝ مِنَ الْجِنَّةِ وَالنَّاسِ',
    reference: 'الناس: 1-6', category: 'وسواس',
  },
  {
    id: 'ikhlas', title: 'سورة الإخلاص', subtitle: 'تعدل ثلث القرآن', icon: '📖',
    arabic: 'قُلْ هُوَ اللَّهُ أَحَدٌ ۝ اللَّهُ الصَّمَدُ ۝ لَمْ يَلِدْ وَلَمْ يُولَدْ ۝ وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ',
    reference: 'الإخلاص: 1-4', category: 'عام',
  },
  {
    id: 'home-protection', title: 'حماية المنزل', subtitle: 'من الجن والشياطين', icon: '🏠',
    arabic: 'بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ\n\n(تُقرأ ثلاث مرات صباحاً ومساءً)',
    reference: 'حديث صحيح', category: 'حماية',
  },
];

function VideoEmbed({ embedUrl, title }: { embedUrl: string; title: string }) {
  return (
    <div className="relative w-full rounded-xl overflow-hidden bg-black" style={{ paddingBottom: '56.25%' }}>
      <iframe
        src={embedUrl}
        title={title}
        className="absolute inset-0 w-full h-full"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        loading="lazy"
        sandbox="allow-scripts allow-same-origin allow-popups allow-presentation"
      />
    </div>
  );
}

export default function Ruqyah() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [activeCategory, setActiveCategory] = useState('');
  const goBack = useSmartBack();
  const { t, dir } = useLocale();
  const [allContent, setAllContent] = useState<any[]>(STATIC_RUQYAH);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/ruqyah`)
      .then(r => r.json())
      .then(d => {
        if (d.items && d.items.length > 0) {
          const items = d.items.map((item: any) => ({
            id: item.id,
            title: item.title,
            subtitle: item.category,
            icon: CATEGORY_ICONS[item.category] || '📿',
            arabic: item.content,
            reference: item.category,
            category: item.category || 'عام',
            video_url: item.video_url || '',
            embed_url: item.embed_url || '',
            video_type: item.video_type || '',
            audio_url: item.audio_url || '',
            thumbnail_url: item.thumbnail_url || '',
          }));
          // Merge API items with static, avoid duplicates by title
          const staticTitles = new Set(STATIC_RUQYAH.map(s => s.title));
          const uniqueApiItems = items.filter((i: any) => !staticTitles.has(i.title));
          setAllContent([...STATIC_RUQYAH, ...uniqueApiItems]);
        }
      }).catch(() => {});
  }, []);

  const filteredContent = activeCategory
    ? allContent.filter(item => item.category === activeCategory)
    : allContent;

  return (
    <div className="min-h-screen bg-background pb-24" dir="rtl">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-background/95 backdrop-blur-xl border-b border-border/30">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3 flex-1">
            <button onClick={goBack} className="p-1.5 rounded-xl hover:bg-muted/50">
              <ChevronLeft className="h-5 w-5 text-foreground rotate-180" />
            </button>
            <div>
              <h1 className="text-base font-bold text-foreground flex items-center gap-1.5">
                <span className="text-lg">🛡</span>
                العلاج بالرقية الشرعية
              </h1>
              <p className="text-[11px] text-muted-foreground">رقية شرعية من القرآن والسنة</p>
            </div>
          </div>
        </div>

        {/* Category Filter - Fixed for mobile */}
        <div className="pb-2.5 px-3">
          <div className="flex gap-1.5 overflow-x-auto scrollbar-hide pb-1" style={{ WebkitOverflowScrolling: 'touch' }}>
            {RUQYAH_CATEGORIES.map(cat => (
              <button
                key={cat.key}
                onClick={() => setActiveCategory(cat.key)}
                className={`inline-flex items-center gap-1 px-3 py-1.5 rounded-lg text-[11px] font-bold whitespace-nowrap transition-all shrink-0 ${
                  activeCategory === cat.key
                    ? 'bg-primary text-primary-foreground shadow-sm'
                    : 'bg-muted/60 text-foreground/70 hover:bg-muted'
                }`}
              >
                <span className="text-xs leading-none">{cat.emoji}</span>
                <span>{cat.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content Cards */}
      <div className="px-3 pt-3 space-y-2.5">
        {filteredContent.map((item) => (
          <div
            key={item.id}
            className="bg-card rounded-xl border border-border/30 overflow-hidden shadow-sm"
          >
            {/* Card Header - Always visible */}
            <button
              onClick={() => setSelectedId(selectedId === item.id ? null : item.id)}
              className="w-full p-3.5 flex items-center gap-3 text-right active:bg-muted/30 transition-colors"
            >
              {/* Icon */}
              <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-primary/12 to-primary/5 flex items-center justify-center shrink-0 border border-primary/10">
                <span className="text-xl leading-none">{item.icon}</span>
              </div>

              {/* Text */}
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-bold text-foreground leading-tight truncate">{item.title}</h3>
                <p className="text-[11px] text-muted-foreground mt-0.5 truncate">{item.subtitle || item.category}</p>
              </div>

              {/* Action icon */}
              <div className={`p-2 rounded-lg shrink-0 ${
                item.embed_url ? 'bg-red-500/10' : item.audio_url ? 'bg-blue-500/10' : 'bg-muted/50'
              }`}>
                {item.embed_url ? (
                  <Video className="h-3.5 w-3.5 text-red-500" />
                ) : item.audio_url ? (
                  <Volume2 className="h-3.5 w-3.5 text-blue-500" />
                ) : (
                  <ChevronDown className={`h-3.5 w-3.5 text-muted-foreground transition-transform duration-200 ${selectedId === item.id ? 'rotate-180' : ''}`} />
                )}
              </div>
            </button>

            {/* Expanded Content */}
            {selectedId === item.id && (
              <div className="border-t border-border/20 bg-muted/10">
                <div className="p-4 space-y-3">
                  {/* Video Embed */}
                  {item.embed_url && (
                    <VideoEmbed embedUrl={item.embed_url} title={item.title} />
                  )}

                  {/* Thumbnail for video */}
                  {item.thumbnail_url && !item.embed_url && (
                    <div className="rounded-xl overflow-hidden relative">
                      <img src={item.thumbnail_url} alt={item.title} className="w-full h-40 object-cover" />
                      <div className="absolute inset-0 flex items-center justify-center bg-black/30">
                        <div className="h-12 w-12 rounded-full bg-red-600 flex items-center justify-center">
                          <Play className="h-5 w-5 text-white fill-white" />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Arabic Text - Clean, no overlap */}
                  {item.arabic && (
                    <div className="bg-background rounded-xl p-4 border border-border/20">
                      <p
                        className="text-base text-foreground leading-[2.4] text-center whitespace-pre-line"
                        dir="rtl"
                        style={{ fontFamily: "'Amiri', 'Traditional Arabic', 'Noto Naskh Arabic', serif", wordSpacing: '2px' }}
                      >
                        {item.arabic}
                      </p>
                    </div>
                  )}

                  {/* Reference & Close */}
                  <div className="flex items-center justify-between gap-2">
                    {item.reference && (
                      <span className="text-[11px] text-primary font-bold bg-primary/8 px-2.5 py-1 rounded-lg">
                        {item.reference}
                      </span>
                    )}
                    <button
                      onClick={(e) => { e.stopPropagation(); setSelectedId(null); }}
                      className="flex items-center gap-1 text-[11px] text-muted-foreground font-bold bg-muted/60 px-2.5 py-1 rounded-lg hover:bg-muted mr-auto"
                    >
                      <X className="h-3 w-3" />
                      اغلاق
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}

        {filteredContent.length === 0 && (
          <div className="text-center py-16">
            <span className="text-4xl block mb-3">🔍</span>
            <p className="text-muted-foreground text-sm">لا توجد رقية في هذا التصنيف</p>
          </div>
        )}
      </div>

      {/* Disclaimer */}
      <div className="px-3 pt-4 pb-6">
        <div className="bg-primary/5 border border-primary/15 rounded-xl p-3.5">
          <p className="text-[11px] text-foreground/70 leading-relaxed whitespace-pre-line">
            {t('ruqyahDisclaimer')}
          </p>
        </div>
      </div>
    </div>
  );
}
