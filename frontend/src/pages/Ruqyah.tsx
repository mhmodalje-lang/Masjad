import { useState } from 'react';
import { ChevronLeft, Play } from 'lucide-react';
import { useSmartBack } from '@/hooks/useSmartBack';
import { motion } from 'framer-motion';

const RUQYAH_CONTENT = [
  {
    id: 'ayat-kursi',
    title: 'آية الكرسي',
    subtitle: 'للحفظ والحماية',
    icon: '🔰',
    arabic: 'اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَّهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ',
    reference: 'البقرة: 255',
  },
  {
    id: 'falaq',
    title: 'سورة الفلق',
    subtitle: 'من شر ما خلق',
    icon: '✨',
    arabic: 'قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ ۝ مِن شَرِّ مَا خَلَقَ ۝ وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ ۝ وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ ۝ وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ',
    reference: 'الفلق: 1-5',
  },
  {
    id: 'nas',
    title: 'سورة الناس',
    subtitle: 'من شر الوسواس',
    icon: '✨',
    arabic: 'قُلْ أَعُوذُ بِرَبِّ النَّاسِ ۝ مَلِكِ النَّاسِ ۝ إِلَٰهِ النَّاسِ ۝ مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ ۝ الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ ۝ مِنَ الْجِنَّةِ وَالنَّاسِ',
    reference: 'الناس: 1-6',
  },
  {
    id: 'ikhlas',
    title: 'سورة الإخلاص',
    subtitle: 'تعدل ثلث القرآن',
    icon: '📿',
    arabic: 'قُلْ هُوَ اللَّهُ أَحَدٌ ۝ اللَّهُ الصَّمَدُ ۝ لَمْ يَلِدْ وَلَمْ يُولَدْ ۝ وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ',
    reference: 'الإخلاص: 1-4',
  },
  {
    id: 'morning-adhkar',
    title: 'أذكار الصباح',
    subtitle: 'للحفظ من كل سوء',
    icon: '🌅',
    arabic: 'أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ',
    reference: 'أذكار الصباح',
  },
  {
    id: 'evening-adhkar',
    title: 'أذكار المساء',
    subtitle: 'للحفظ والحماية',
    icon: '🌙',
    arabic: 'أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ',
    reference: 'أذكار المساء',
  },
  {
    id: 'home-protection',
    title: 'حماية المنزل',
    subtitle: 'من الجن والشياطين',
    icon: '🏠',
    arabic: 'بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ (ثلاث مرات)',
    reference: 'حديث صحيح',
  },
  {
    id: 'sleep-protection',
    title: 'أذكار النوم',
    subtitle: 'للحفظ أثناء النوم',
    icon: '🛌',
    arabic: 'اللَّهُمَّ بِاسْمِكَ أَمُوتُ وَأَحْيَا',
    reference: 'البخاري',
  },
];

export default function Ruqyah() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const goBack = useSmartBack();
  const selected = RUQYAH_CONTENT.find(item => item.id === selectedId);

  return (
    <div className="min-h-screen bg-background pb-20" dir="rtl">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-background/80 backdrop-blur-xl border-b border-border/40">
        <div className="flex items-center justify-between px-4 py-3.5">
          <div className="flex items-center gap-3">
            <button onClick={goBack} className="p-1.5">
              <ChevronLeft className="h-5 w-5 text-foreground rotate-180" />
            </button>
            <div>
              <h1 className="text-base font-bold text-foreground flex items-center gap-2">
                <span>🛡️</span> الرقية الشرعية
              </h1>
              <p className="text-xs text-muted-foreground">للحفظ والحماية من كل سوء</p>
            </div>
          </div>
        </div>
      </div>

      {/* Content Grid */}
      <div className="px-4 pt-4 space-y-3">
        {RUQYAH_CONTENT.map((item) => (
          <motion.div
            key={item.id}
            layoutId={item.id}
            onClick={() => setSelectedId(item.id)}
            className="bg-card border border-border/40 rounded-2xl p-4 active:scale-[0.98] transition-transform cursor-pointer"
          >
            <div className="flex items-start gap-3 mb-3">
              <span className="text-3xl">{item.icon}</span>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-bold text-foreground mb-1">{item.title}</h3>
                <p className="text-xs text-muted-foreground">{item.subtitle}</p>
              </div>
              <button className="p-2 rounded-full bg-primary/10 text-primary">
                <Play className="h-4 w-4" />
              </button>
            </div>
            
            {selectedId === item.id && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="border-t border-border/30 pt-3"
              >
                <p className="text-base font-arabic text-foreground leading-[2.5] text-center mb-3">
                  {item.arabic}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">{item.reference}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedId(null);
                    }}
                    className="text-xs text-primary font-semibold"
                  >
                    إخفاء
                  </button>
                </div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>

      {/* Info Card */}
      <div className="px-4 pt-4 pb-6">
        <div className="bg-primary/5 border border-primary/20 rounded-2xl p-4">
          <h3 className="text-sm font-bold text-primary mb-2">💡 فائدة</h3>
          <p className="text-xs text-foreground/80 leading-relaxed">
            الرقية الشرعية من القرآن والسنة لها فضل عظيم في الحفظ من الجن والشياطين والعين والحسد. 
            داوم عليها صباحاً ومساءً وقبل النوم.
          </p>
        </div>
      </div>
    </div>
  );
}
