import { useState, useEffect } from 'react';
import { ChevronLeft, ChevronDown, Play, Video, Volume2, X } from 'lucide-react';
import { useSmartBack } from '@/hooks/useSmartBack';
import { useLocale } from '@/hooks/useLocale';
import { motion, AnimatePresence } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

const CATEGORY_ICONS: Record<string, string> = {
  'حماية': '🛡', 'protection': '🛡',
  'عام': '📖', 'general': '📖',
  'عين': '👁', 'evil-eye': '👁',
  'حسد': '🧿', 'envy': '🧿',
  'سحر': '⚡', 'magic': '⚡',
  'مس': '🔥', 'jinn': '🔥',
  'أرق': '😴', 'insomnia': '😴',
  'وسواس': '💭', 'whispers': '💭',
};

function getRuqyahCategories(t: (key: string) => string) {
  return [
    { key: '', label: t('ruqyahCatAll'), emoji: '📋' },
    { key: 'general', label: t('ruqyahCatGeneral'), emoji: '📖' },
    { key: 'evil-eye', label: t('ruqyahCatEye'), emoji: '👁' },
    { key: 'envy', label: t('ruqyahCatEnvy'), emoji: '🧿' },
    { key: 'magic', label: t('ruqyahCatMagic'), emoji: '⚡' },
    { key: 'jinn', label: t('ruqyahCatTouch'), emoji: '🔥' },
    { key: 'insomnia', label: t('ruqyahCatInsomnia'), emoji: '😴' },
    { key: 'whispers', label: t('ruqyahCatWhispers'), emoji: '💭' },
    { key: 'protection', label: t('ruqyahCatProtection'), emoji: '🛡' },
  ];
}

function getStaticRuqyah(t: (key: string) => string, locale: string) {
  const isAr = locale === 'ar';
  return [
    {
      id: 'ayat-kursi', title: t('ruqyahAyatKursiTitle'), subtitle: t('ruqyahAyatKursiSubtitle'), icon: '🛡',
      arabic: 'اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَّهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ',
      translation: isAr ? '' : t('ruqyahAyatKursiTranslation'),
      reference: t('ruqyahRefBaqara255'), category: 'protection',
    },
    {
      id: 'falaq', title: t('ruqyahFalaqTitle'), subtitle: t('ruqyahFalaqSubtitle'), icon: '🧿',
      arabic: 'قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ ۝ مِن شَرِّ مَا خَلَقَ ۝ وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ ۝ وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ ۝ وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ',
      translation: isAr ? '' : t('ruqyahFalaqTranslation'),
      reference: t('ruqyahRefFalaq'), category: 'envy',
    },
    {
      id: 'nas', title: t('ruqyahNasTitle'), subtitle: t('ruqyahNasSubtitle'), icon: '💭',
      arabic: 'قُلْ أَعُوذُ بِرَبِّ النَّاسِ ۝ مَلِكِ النَّاسِ ۝ إِلَٰهِ النَّاسِ ۝ مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ ۝ الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ ۝ مِنَ الْجِنَّةِ وَالنَّاسِ',
      translation: isAr ? '' : t('ruqyahNasTranslation'),
      reference: t('ruqyahRefNas'), category: 'whispers',
    },
    {
      id: 'ikhlas', title: t('ruqyahIkhlasTitle'), subtitle: t('ruqyahIkhlasSubtitle'), icon: '📖',
      arabic: 'قُلْ هُوَ اللَّهُ أَحَدٌ ۝ اللَّهُ الصَّمَدُ ۝ لَمْ يَلِدْ وَلَمْ يُولَدْ ۝ وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ',
      translation: isAr ? '' : t('ruqyahIkhlasTranslation'),
      reference: t('ruqyahRefIkhlas'), category: 'general',
    },
    {
      id: 'home-protection', title: t('ruqyahHomeProtTitle'), subtitle: t('ruqyahHomeProtSubtitle'), icon: '🏠',
      arabic: 'بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ',
      translation: isAr ? '' : t('ruqyahHomeProtTranslation') + '\n\n' + t('ruqyahReadThrice'),
      reference: t('ruqyahRefSahihHadith'), category: 'protection',
    },
  ];
}

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
  const { t, dir, locale } = useLocale();
  const categories = getRuqyahCategories(t);
  const staticRuqyah = getStaticRuqyah(t, locale);
  const [allContent, setAllContent] = useState<any[]>(staticRuqyah);

  useEffect(() => {
    // Regenerate static content when locale changes
    setAllContent(prev => {
      const newStatic = getStaticRuqyah(t, locale);
      const staticIds = new Set(newStatic.map(s => s.id));
      const apiItems = prev.filter(item => !staticIds.has(item.id));
      return [...newStatic, ...apiItems];
    });
  }, [locale, t]);

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
            category: item.category || 'general',
            video_url: item.video_url || '',
            embed_url: item.embed_url || '',
            video_type: item.video_type || '',
            audio_url: item.audio_url || '',
            thumbnail_url: item.thumbnail_url || '',
          }));
          const staticIds = new Set(staticRuqyah.map(s => s.id));
          const uniqueApiItems = items.filter((i: any) => !staticIds.has(i.id));
          setAllContent([...getStaticRuqyah(t, locale), ...uniqueApiItems]);
        }
      }).catch(() => {});
  }, []);

  const filteredContent = activeCategory
    ? allContent.filter(item => item.category === activeCategory)
    : allContent;

  return (
    <div className="min-h-screen bg-background pb-24" dir={dir}>
      {/* Header */}
      <div className="sticky top-0 z-40 bg-background/95 backdrop-blur-xl border-b border-border/30">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3 flex-1">
            <button onClick={goBack} className="p-1.5 rounded-xl hover:bg-muted/50">
              <ChevronLeft className={`h-5 w-5 text-foreground ${dir === 'rtl' ? 'rotate-180' : ''}`} />
            </button>
            <div>
              <h1 className="text-base font-bold text-foreground flex items-center gap-1.5">
                <span className="text-lg">🛡</span>
                {t('ruqyahPageTitle')}
              </h1>
              <p className="text-[11px] text-muted-foreground">{t('ruqyahPageSubtitle')}</p>
            </div>
          </div>
        </div>

        {/* Category Filter */}
        <div className="pb-2.5 px-3">
          <div className="flex gap-1.5 overflow-x-auto scrollbar-hide pb-1" style={{ WebkitOverflowScrolling: 'touch' }}>
            {categories.map(cat => (
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
            {/* Card Header */}
            <button
              onClick={() => setSelectedId(selectedId === item.id ? null : item.id)}
              className={`w-full p-3.5 flex items-center gap-3 ${dir === 'rtl' ? 'text-right' : 'text-left'} active:bg-muted/30 transition-colors`}
            >
              <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-primary/12 to-primary/5 flex items-center justify-center shrink-0 border border-primary/10">
                <span className="text-xl leading-none">{item.icon}</span>
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-bold text-foreground leading-tight truncate">{item.title}</h3>
                <p className="text-[11px] text-muted-foreground mt-0.5 truncate">{item.subtitle || item.category}</p>
              </div>
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
                  {item.embed_url && (
                    <VideoEmbed embedUrl={item.embed_url} title={item.title} />
                  )}
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
                  {item.arabic && (
                    <div className="bg-background rounded-xl p-4 border border-border/20">
                      {/* Show translation first for non-Arabic users */}
                      {item.translation && locale !== 'ar' && (
                        <p className="text-base text-foreground leading-relaxed mb-3 whitespace-pre-line" dir={dir}>
                          {item.translation}
                        </p>
                      )}
                      {/* Arabic original - collapsible for non-Arabic */}
                      {locale !== 'ar' && (
                        <details className="mt-2">
                          <summary className="text-xs text-primary cursor-pointer font-bold">{t('showArabicOriginal')}</summary>
                          <p
                            className="text-base text-foreground/80 leading-[2.4] text-center whitespace-pre-line mt-2"
                            dir="rtl"
                            style={{ fontFamily: "'Amiri', 'Traditional Arabic', 'Noto Naskh Arabic', serif", wordSpacing: '2px' }}
                          >
                            {item.arabic}
                          </p>
                        </details>
                      )}
                      {/* Arabic users see the text directly */}
                      {locale === 'ar' && (
                        <p
                          className="text-base text-foreground leading-[2.4] text-center whitespace-pre-line"
                          dir="rtl"
                          style={{ fontFamily: "'Amiri', 'Traditional Arabic', 'Noto Naskh Arabic', serif", wordSpacing: '2px' }}
                        >
                          {item.arabic}
                        </p>
                      )}
                    </div>
                  )}
                  <div className="flex items-center justify-between gap-2">
                    {item.reference && (
                      <span className="text-[11px] text-primary font-bold bg-primary/8 px-2.5 py-1 rounded-lg">
                        {item.reference}
                      </span>
                    )}
                    <button
                      onClick={(e) => { e.stopPropagation(); setSelectedId(null); }}
                      className={`flex items-center gap-1 text-[11px] text-muted-foreground font-bold bg-muted/60 px-2.5 py-1 rounded-lg hover:bg-muted ${dir === 'rtl' ? 'mr-auto' : 'ml-auto'}`}
                    >
                      <X className="h-3 w-3" />
                      {t('closeBtn')}
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
            <p className="text-muted-foreground text-sm">{t('noRuqyahInCategory')}</p>
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
