import { useState, useEffect } from 'react';
import { ChevronLeft, Play, Video, Volume2 } from 'lucide-react';
import { useSmartBack } from '@/hooks/useSmartBack';
import { useLocale } from '@/hooks/useLocale';
import { motion, AnimatePresence } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

const RUQYAH_CATEGORIES = [
  { key: '', label: 'الكل', labelKey: 'allStories', emoji: '📋' },
  { key: 'general', label: 'عام', labelKey: 'general', emoji: '📖' },
  { key: 'عين', label: 'عين', emoji: '👁️' },
  { key: 'حسد', label: 'حسد', emoji: '🧿' },
  { key: 'سحر', label: 'سحر', emoji: '⚡' },
  { key: 'مس', label: 'مس', emoji: '🔥' },
  { key: 'أرق', label: 'أرق', emoji: '😴' },
  { key: 'وسواس', label: 'وسواس', emoji: '💭' },
  { key: 'حماية', label: 'حماية', emoji: '🛡️' },
];

const STATIC_RUQYAH = [
  {
    id: 'ayat-kursi', title: 'آية الكرسي', subtitle: 'للحفظ والحماية', icon: '🔰',
    arabic: 'اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَّهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ',
    reference: 'البقرة: 255', category: 'حماية',
  },
  {
    id: 'falaq', title: 'سورة الفلق', subtitle: 'من شر ما خلق', icon: '✨',
    arabic: 'قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ ۝ مِن شَرِّ مَا خَلَقَ ۝ وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ ۝ وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ ۝ وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ',
    reference: 'الفلق: 1-5', category: 'حماية',
  },
  {
    id: 'nas', title: 'سورة الناس', subtitle: 'من شر الوسواس', icon: '✨',
    arabic: 'قُلْ أَعُوذُ بِرَبِّ النَّاسِ ۝ مَلِكِ النَّاسِ ۝ إِلَٰهِ النَّاسِ ۝ مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ ۝ الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ ۝ مِنَ الْجِنَّةِ وَالنَّاسِ',
    reference: 'الناس: 1-6', category: 'حماية',
  },
  {
    id: 'ikhlas', title: 'سورة الإخلاص', subtitle: 'تعدل ثلث القرآن', icon: '📿',
    arabic: 'قُلْ هُوَ اللَّهُ أَحَدٌ ۝ اللَّهُ الصَّمَدُ ۝ لَمْ يَلِدْ وَلَمْ يُولَدْ ۝ وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ',
    reference: 'الإخلاص: 1-4', category: 'general',
  },
  {
    id: 'home-protection', title: 'حماية المنزل', subtitle: 'من الجن والشياطين', icon: '🏠',
    arabic: 'بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ (ثلاث مرات)',
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
  const [apiItems, setApiItems] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/ruqyah`)
      .then(r => r.json())
      .then(d => {
        if (d.items && d.items.length > 0) {
          const items = d.items.map((item: any) => ({
            id: item.id,
            title: item.title,
            subtitle: item.category,
            icon: item.video_url ? '🎬' : item.audio_url ? '🔊' : '📿',
            arabic: item.content,
            reference: item.category,
            category: item.category || 'general',
            video_url: item.video_url || '',
            embed_url: item.embed_url || '',
            video_type: item.video_type || '',
            audio_url: item.audio_url || '',
            thumbnail_url: item.thumbnail_url || '',
          }));
          setApiItems(items);
          setAllContent([...items, ...STATIC_RUQYAH]);
        }
      }).catch(() => {});
  }, []);

  const filteredContent = activeCategory
    ? allContent.filter(item => item.category === activeCategory)
    : allContent;

  return (
    <div className="min-h-screen bg-background pb-20" dir={dir}>
      {/* Header */}
      <div className="sticky top-0 z-40 bg-background/80 backdrop-blur-xl border-b border-border/40">
        <div className="flex items-center justify-between px-4 py-3.5">
          <div className="flex items-center gap-3">
            <button onClick={goBack} className="p-1.5">
              <ChevronLeft className={`h-5 w-5 text-foreground ${dir === 'rtl' ? 'rotate-180' : ''}`} />
            </button>
            <div>
              <h1 className="text-base font-bold text-foreground flex items-center gap-2">
                <span>🛡️</span> {t('ruqyahTitle').replace('🛡️ ', '')}
              </h1>
              <p className="text-xs text-muted-foreground">{t('ruqyahSubtitle')}</p>
            </div>
          </div>
        </div>

        {/* Category Filter */}
        <div className="flex gap-2 px-4 pb-3 overflow-x-auto scrollbar-hide">
          {RUQYAH_CATEGORIES.map(cat => (
            <button
              key={cat.key}
              onClick={() => setActiveCategory(cat.key)}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-xs font-bold whitespace-nowrap transition-all border ${
                activeCategory === cat.key
                  ? 'bg-primary text-primary-foreground border-primary shadow-md shadow-primary/20'
                  : 'bg-card text-muted-foreground border-border/40 hover:border-primary/30 hover:bg-muted/50'
              }`}
            >
              <span className="text-sm">{cat.emoji}</span>
              {cat.labelKey ? t(cat.labelKey) : cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="px-4 pt-4 space-y-4">
        <AnimatePresence mode="popLayout">
          {filteredContent.map((item) => (
            <motion.div
              key={item.id}
              layout
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              onClick={() => setSelectedId(selectedId === item.id ? null : item.id)}
              className="bg-card border border-border/30 rounded-2xl overflow-hidden active:scale-[0.99] transition-transform cursor-pointer shadow-sm"
            >
              {/* Card Header */}
              <div className="p-4 flex items-center gap-3">
                <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-primary/15 to-primary/5 flex items-center justify-center shrink-0 border border-primary/10">
                  <span className="text-2xl">{item.icon}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-[15px] font-bold text-foreground leading-snug">{item.title}</h3>
                  <p className="text-xs text-muted-foreground mt-0.5">{item.subtitle || item.category}</p>
                </div>
                {item.embed_url ? (
                  <div className="p-2.5 rounded-xl bg-red-500/10 text-red-500 shrink-0">
                    <Video className="h-4 w-4" />
                  </div>
                ) : item.audio_url ? (
                  <div className="p-2.5 rounded-xl bg-blue-500/10 text-blue-500 shrink-0">
                    <Volume2 className="h-4 w-4" />
                  </div>
                ) : (
                  <div className="p-2.5 rounded-xl bg-primary/10 text-primary shrink-0">
                    <ChevronLeft className={`h-4 w-4 transition-transform ${selectedId === item.id ? 'rotate-90' : dir === 'rtl' ? 'rotate-180' : ''}`} />
                  </div>
                )}
              </div>

              {/* Thumbnail preview for video items */}
              {item.thumbnail_url && selectedId !== item.id && (
                <div className="mx-4 mb-4 rounded-xl overflow-hidden relative">
                  <img src={item.thumbnail_url} alt={item.title} className="w-full h-36 object-cover" />
                  <div className="absolute inset-0 flex items-center justify-center bg-black/30">
                    <div className="h-12 w-12 rounded-full bg-red-600 flex items-center justify-center shadow-lg">
                      <Play className="h-5 w-5 text-white fill-white" />
                    </div>
                  </div>
                </div>
              )}

              {/* Expanded Content */}
              <AnimatePresence>
                {selectedId === item.id && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="border-t border-border/20"
                  >
                    <div className="p-4 space-y-4">
                      {/* Video Embed */}
                      {item.embed_url && (
                        <VideoEmbed embedUrl={item.embed_url} title={item.title} />
                      )}

                      {/* Arabic Text */}
                      {item.arabic && (
                        <div className="bg-muted/30 rounded-2xl p-5 border border-border/20">
                          <p className="text-[17px] font-arabic text-foreground leading-[2.8] text-center" dir="rtl">
                            {item.arabic}
                          </p>
                        </div>
                      )}

                      <div className="flex items-center justify-between pt-1">
                        <span className="text-xs text-primary font-medium bg-primary/10 px-3 py-1 rounded-full">{item.reference || item.category}</span>
                        <button
                          onClick={(e) => { e.stopPropagation(); setSelectedId(null); }}
                          className="text-xs text-muted-foreground font-bold bg-muted/50 px-3 py-1.5 rounded-full hover:bg-muted"
                        >
                          إغلاق ✕
                        </button>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </AnimatePresence>

        {filteredContent.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground text-sm">{t('noRuqyahYet')}</p>
          </div>
        )}
      </div>

      {/* Disclaimer */}
      <div className="px-4 pt-4 pb-6">
        <div className="bg-primary/5 border border-primary/20 rounded-2xl p-4">
          <p className="text-xs text-foreground/80 leading-relaxed whitespace-pre-line">
            {t('ruqyahDisclaimer')}
          </p>
        </div>
      </div>
    </div>
  );
}
