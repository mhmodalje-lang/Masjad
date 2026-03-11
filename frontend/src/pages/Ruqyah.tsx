import { useState, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, Play, Pause, Square, Shield, Volume2, ChevronDown, BookOpen, Heart } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import PageHeader from '@/components/PageHeader';

interface RuqyahSection {
  id: string;
  title: string;
  emoji: string;
  color: string;
  description: string;
  items: RuqyahItem[];
}

interface RuqyahItem {
  id: string;
  title: string;
  arabic: string;
  translation?: string;
  reference: string;
  audioUrl?: string;
  benefit?: string;
}

const RUQYAH_DATA: RuqyahSection[] = [
  {
    id: 'protection',
    title: 'آيات الحفظ والحماية',
    emoji: '🛡️',
    color: 'from-emerald-600 to-teal-600',
    description: 'آيات قرآنية لحفظ النفس والمال',
    items: [
      {
        id: 'fatiha',
        title: 'سورة الفاتحة',
        arabic: 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ ﴿١﴾ الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ ﴿٢﴾ الرَّحْمَٰنِ الرَّحِيمِ ﴿٣﴾ مَالِكِ يَوْمِ الدِّينِ ﴿٤﴾ إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ ﴿٥﴾ اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ ﴿٦﴾ صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ ﴿٧﴾',
        reference: 'سورة الفاتحة - 1:1-7',
        benefit: 'أم الكتاب وأم القرآن، تُقرأ لكل شيء',
        audioUrl: 'https://cdn.islamic.network/quran/audio/128/ar.alafasy/1.mp3',
      },
      {
        id: 'ayat-kursi',
        title: 'آية الكرسي',
        arabic: 'اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ',
        reference: 'البقرة: 255',
        benefit: 'من قرأها دُبر كل صلاة لم يمنعه من دخول الجنة إلا أن يموت • حفظ من الشياطين',
        audioUrl: 'https://cdn.islamic.network/quran/audio/128/ar.alafasy/2.mp3',
      },
      {
        id: 'baqara-285-286',
        title: 'خاتمة البقرة (285-286)',
        arabic: 'آمَنَ الرَّسُولُ بِمَا أُنزِلَ إِلَيْهِ مِن رَّبِّهِ وَالْمُؤْمِنُونَ ۚ كُلٌّ آمَنَ بِاللَّهِ وَمَلَائِكَتِهِ وَكُتُبِهِ وَرُسُلِهِ لَا نُفَرِّقُ بَيْنَ أَحَدٍ مِّن رُّسُلِهِ ۚ وَقَالُوا سَمِعْنَا وَأَطَعْنَا ۖ غُفْرَانَكَ رَبَّنَا وَإِلَيْكَ الْمَصِيرُ ﴿٢٨٥﴾ لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا ۚ لَهَا مَا كَسَبَتْ وَعَلَيْهَا مَا اكْتَسَبَتْ ۗ رَبَّنَا لَا تُؤَاخِذْنَا إِن نَّسِينَا أَوْ أَخْطَأْنَا ۚ رَبَّنَا وَلَا تَحْمِلْ عَلَيْنَا إِصْرًا كَمَا حَمَلْتَهُ عَلَى الَّذِينَ مِن قَبْلِنَا ۚ رَبَّنَا وَلَا تُحَمِّلْنَا مَا لَا طَاقَةَ لَنَا بِهِ ۖ وَاعْفُ عَنَّا وَاغْفِرْ لَنَا وَارْحَمْنَا ۚ أَنتَ مَوْلَانَا فَانصُرْنَا عَلَى الْقَوْمِ الْكَافِرِينَ ﴿٢٨٦﴾',
        reference: 'البقرة: 285-286',
        benefit: 'من قرأها ليلاً كفتاه، أي أجزأتاه عن قيام الليل',
      },
    ],
  },
  {
    id: 'sihr',
    title: 'الرقية من السحر',
    emoji: '✨',
    color: 'from-purple-600 to-violet-600',
    description: 'الآيات المأثورة في علاج السحر',
    items: [
      {
        id: 'falaq-nas',
        title: 'المعوذتان - الفلق والناس',
        arabic: 'قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ ﴿١﴾ مِن شَرِّ مَا خَلَقَ ﴿٢﴾ وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ ﴿٣﴾ وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ ﴿٤﴾ وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ ﴿٥﴾\n\nقُلْ أَعُوذُ بِرَبِّ النَّاسِ ﴿١﴾ مَلِكِ النَّاسِ ﴿٢﴾ إِلَٰهِ النَّاسِ ﴿٣﴾ مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ ﴿٤﴾ الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ ﴿٥﴾ مِنَ الْجِنَّةِ وَالنَّاسِ ﴿٦﴾',
        reference: 'سورة الفلق والناس',
        benefit: 'نزلتا في سحر النبي ﷺ فشفاه الله بهما. تُقرأ ثلاث مرات صباحاً ومساءً',
        audioUrl: 'https://cdn.islamic.network/quran/audio/128/ar.alafasy/113.mp3',
      },
      {
        id: 'yunus-81',
        title: 'آيات يونس',
        arabic: 'فَلَمَّا أَلْقَوْا قَالَ مُوسَىٰ مَا جِئْتُم بِهِ السِّحْرُ ۖ إِنَّ اللَّهَ سَيُبْطِلُهُ ۖ إِنَّ اللَّهَ لَا يُصْلِحُ عَمَلَ الْمُفْسِدِينَ',
        reference: 'يونس: 81',
        benefit: 'تُقرأ للعلاج من السحر',
      },
      {
        id: 'araf-117-122',
        title: 'آيات الأعراف',
        arabic: 'وَأَوْحَيْنَا إِلَىٰ مُوسَىٰ أَنْ أَلْقِ عَصَاكَ ۖ فَإِذَا هِيَ تَلْقَفُ مَا يَأْفِكُونَ ﴿١١٧﴾ فَوَقَعَ الْحَقُّ وَبَطَلَ مَا كَانُوا يَعْمَلُونَ ﴿١١٨﴾ فَغُلِبُوا هُنَالِكَ وَانقَلَبُوا صَاغِرِينَ ﴿١١٩﴾',
        reference: 'الأعراف: 117-119',
        benefit: 'من الآيات المستخدمة في الرقية من السحر',
      },
    ],
  },
  {
    id: 'ain',
    title: 'الرقية من العين والحسد',
    emoji: '👁️',
    color: 'from-blue-600 to-cyan-600',
    description: 'الآيات الكريمة للحماية من العين',
    items: [
      {
        id: 'qalam-51',
        title: 'آية القلم',
        arabic: 'وَإِن يَكَادُ الَّذِينَ كَفَرُوا لَيُزْلِقُونَكَ بِأَبْصَارِهِمْ لَمَّا سَمِعُوا الذِّكْرَ وَيَقُولُونَ إِنَّهُ لَمَجْنُونٌ ﴿٥١﴾ وَمَا هُوَ إِلَّا ذِكْرٌ لِّلْعَالَمِينَ ﴿٥٢﴾',
        reference: 'القلم: 51-52',
        benefit: 'من أشهر آيات الرقية من العين',
      },
      {
        id: 'nazar-dua',
        title: 'دعاء الاستعاذة من العين',
        arabic: 'أَعُوذُ بِكَلِمَاتِ اللهِ التَّامَّاتِ مِنْ كُلِّ شَيْطَانٍ وَهَامَّةٍ، وَمِنْ كُلِّ عَيْنٍ لَامَّةٍ',
        reference: 'رواه البخاري',
        benefit: 'كان النبي ﷺ يعوّذ بها الحسن والحسين',
      },
    ],
  },
  {
    id: 'waswaas',
    title: 'الرقية من الوسواس',
    emoji: '🧠',
    color: 'from-amber-600 to-orange-600',
    description: 'علاج الوسواس القهري والقلق',
    items: [
      {
        id: 'ikhlas-x3',
        title: 'سورة الإخلاص (ثلاث مرات)',
        arabic: 'قُلْ هُوَ اللَّهُ أَحَدٌ ﴿١﴾ اللَّهُ الصَّمَدُ ﴿٢﴾ لَمْ يَلِدْ وَلَمْ يُولَدْ ﴿٣﴾ وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ ﴿٤﴾',
        reference: 'سورة الإخلاص × 3',
        benefit: 'تعدل ثلث القرآن. تُقرأ مع المعوذتين 3 مرات صباحاً ومساءً',
        audioUrl: 'https://cdn.islamic.network/quran/audio/128/ar.alafasy/112.mp3',
      },
      {
        id: 'baqara-285',
        title: 'دعاء دفع الوسواس',
        arabic: 'آمَنْتُ بِاللهِ وَرُسُلِهِ',
        reference: 'رواه البخاري ومسلم',
        benefit: 'يقال عند الشعور بالوسواس',
      },
      {
        id: 'quran-morning',
        title: 'أذكار الصباح والمساء',
        arabic: 'بِسْمِ اللهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ',
        reference: 'رواه أبو داود والترمذي',
        benefit: 'من قالها ثلاثاً صباحاً لم تصبه فجأة بلاء حتى يُمسي',
      },
    ],
  },
  {
    id: 'shifa',
    title: 'آيات الشفاء',
    emoji: '💚',
    color: 'from-green-600 to-emerald-600',
    description: 'الآيات الكريمة للشفاء من الأمراض',
    items: [
      {
        id: 'shifa-six',
        title: 'الآيات الست للشفاء',
        arabic: 'وَيَشْفِ صُدُورَ قَوْمٍ مُّؤْمِنِينَ (التوبة:14) • وَشِفَاءٌ لِّمَا فِي الصُّدُورِ (يونس:57) • يَخْرُجُ مِن بُطُونِهَا شَرَابٌ مُّخْتَلِفٌ أَلْوَانُهُ فِيهِ شِفَاءٌ لِّلنَّاسِ (النحل:69) • وَنُنَزِّلُ مِنَ الْقُرْآنِ مَا هُوَ شِفَاءٌ وَرَحْمَةٌ لِّلْمُؤْمِنِينَ (الإسراء:82) • وَإِذَا مَرِضْتُ فَهُوَ يَشْفِينِ (الشعراء:80) • قُلْ هُوَ لِلَّذِينَ آمَنُوا هُدًى وَشِفَاءٌ (فصلت:44)',
        reference: 'آيات الشفاء في القرآن',
        benefit: 'الآيات الست للشفاء المعروفة، تُقرأ على الماء ثم يُشرب',
      },
      {
        id: 'ruqyah-dua',
        title: 'دعاء النبي ﷺ للمريض',
        arabic: 'اللَّهُمَّ رَبَّ النَّاسِ، أَذْهِبِ الْبَأْسَ، اشْفِ أَنْتَ الشَّافِي، لَا شِفَاءَ إِلَّا شِفَاؤُكَ، شِفَاءً لَا يُغَادِرُ سَقَمًا',
        reference: 'رواه البخاري ومسلم',
        benefit: 'كان النبي ﷺ يرقي بها المرضى',
      },
    ],
  },
  {
    id: 'complete',
    title: 'الرقية الشرعية الكاملة',
    emoji: '📖',
    color: 'from-rose-600 to-pink-600',
    description: 'الرقية الكاملة كما وردت عن النبي ﷺ',
    items: [
      {
        id: 'complete-ruqyah',
        title: 'الرقية الجامعة',
        arabic: 'بِسْمِ اللهِ × 3\n\nأَعُوذُ بِاللهِ وَقُدْرَتِهِ مِن شَرِّ مَا أَجِدُ وَأُحَاذِرُ × 7\n\nقُلْ أَعُوذُ بِرَبِّ الفَلَق × 3\nقُلْ أَعُوذُ بِرَبِّ النَّاسِ × 3\nقُلْ هُوَ اللهُ أَحَدٌ × 3\nآيَة الكُرسِي × 1',
        reference: 'مجموع ما ورد عن النبي ﷺ في الصحيحين',
        benefit: 'تُقرأ على الشخص المصاب مع النفث عليه',
      },
      {
        id: 'talha-ruqyah',
        title: 'رقية طلحة',
        arabic: 'بِسْمِ اللهِ أَرْقِيكَ، مِنْ كُلِّ شَيءٍ يُؤذِيكَ، مِنْ شَرِّ كُلِّ نَفسٍ أَوْ عَينٍ حَاسِدٍ، اللهُ يَشفِيكَ، بِسمِ اللهِ أَرقِيكَ',
        reference: 'رواه مسلم',
        benefit: 'من الرقى الجائزة الثابتة',
      },
    ],
  },
];

const SECTION_COLORS: Record<string, string> = {
  protection: 'bg-emerald-500/10 border-emerald-500/30',
  sihr: 'bg-purple-500/10 border-purple-500/30',
  ain: 'bg-blue-500/10 border-blue-500/30',
  waswaas: 'bg-amber-500/10 border-amber-500/30',
  shifa: 'bg-green-500/10 border-green-500/30',
  complete: 'bg-rose-500/10 border-rose-500/30',
};

export default function Ruqyah() {
  const navigate = useNavigate();
  const [selectedSection, setSelectedSection] = useState<string | null>(null);
  const [expandedItem, setExpandedItem] = useState<string | null>(null);
  const [playingId, setPlayingId] = useState<string | null>(null);
  const [favorites, setFavorites] = useState<string[]>(() =>
    JSON.parse(localStorage.getItem('ruqyah_favorites') || '[]')
  );
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const toggleFavorite = (id: string) => {
    setFavorites(prev => {
      const updated = prev.includes(id) ? prev.filter(f => f !== id) : [...prev, id];
      localStorage.setItem('ruqyah_favorites', JSON.stringify(updated));
      return updated;
    });
  };

  const playAudio = useCallback((item: RuqyahItem) => {
    if (!item.audioUrl) return;
    
    if (playingId === item.id) {
      audioRef.current?.pause();
      setPlayingId(null);
      return;
    }
    
    if (audioRef.current) {
      audioRef.current.pause();
    }
    
    audioRef.current = new Audio(item.audioUrl);
    audioRef.current.play().then(() => setPlayingId(item.id));
    audioRef.current.onended = () => setPlayingId(null);
  }, [playingId]);

  const section = selectedSection ? RUQYAH_DATA.find(s => s.id === selectedSection) : null;

  return (
    <div className="min-h-screen pb-24" dir="rtl">
      {/* Header */}
      <div className="relative bg-gradient-to-br from-emerald-900 via-teal-900 to-green-900 px-4 pb-12 pt-safe-header text-center overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          {Array.from({length: 20}).map((_, i) => (
            <div key={i} className="absolute text-4xl" style={{left:`${Math.random()*100}%`, top:`${Math.random()*100}%`, opacity:0.3}}>✦</div>
          ))}
        </div>
        <button onClick={() => selectedSection ? setSelectedSection(null) : navigate(-1)} className="absolute start-4 top-safe-header mt-2 h-9 w-9 rounded-full bg-white/10 flex items-center justify-center">
          <ArrowRight className="h-5 w-5 text-white" />
        </button>
        <div className="relative">
          <div className="text-4xl mb-2">🛡️</div>
          <h1 className="text-2xl font-bold text-white font-arabic mb-1">الرقية الشرعية</h1>
          <p className="text-white/70 text-sm">العلاج بالقرآن الكريم والسنة النبوية</p>
          {section && (
            <motion.div initial={{opacity:0,y:10}} animate={{opacity:1,y:0}} className="mt-2 inline-flex items-center gap-2 bg-white/10 rounded-full px-3 py-1">
              <span>{section.emoji}</span>
              <span className="text-white text-sm">{section.title}</span>
            </motion.div>
          )}
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      <div className="px-4 pt-6">
        {/* Instructions */}
        {!selectedSection && (
          <motion.div initial={{opacity:0,y:10}} animate={{opacity:1,y:0}} className="mb-6 p-4 bg-amber-500/10 border border-amber-500/30 rounded-2xl">
            <p className="text-amber-700 dark:text-amber-300 text-sm font-arabic leading-relaxed text-center">
              📌 الرقية الشرعية هي العلاج بالقرآن الكريم والأدعية النبوية المأثورة<br/>
              <span className="text-xs opacity-80">تُقرأ على المريض مع النفث أو على الماء ثم الشرب منه</span>
            </p>
          </motion.div>
        )}

        {/* Section Grid */}
        {!selectedSection && (
          <div className="grid grid-cols-2 gap-3">
            {RUQYAH_DATA.map((sect, i) => (
              <motion.button
                key={sect.id}
                initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{delay:i*0.05}}
                onClick={() => setSelectedSection(sect.id)}
                className={cn('p-4 rounded-2xl border text-start transition-all active:scale-95', SECTION_COLORS[sect.id])}
              >
                <div className="text-2xl mb-2">{sect.emoji}</div>
                <div className="text-sm font-bold text-foreground font-arabic leading-tight">{sect.title}</div>
                <div className="text-xs text-muted-foreground mt-1">{sect.items.length} آيات/أدعية</div>
              </motion.button>
            ))}
          </div>
        )}

        {/* Section Content */}
        {section && (
          <div className="space-y-3">
            <p className="text-muted-foreground text-sm text-center mb-4">{section.description}</p>
            {section.items.map((item, i) => (
              <motion.div
                key={item.id}
                initial={{opacity:0,y:15}} animate={{opacity:1,y:0}} transition={{delay:i*0.05}}
                className="bg-card border border-border rounded-2xl overflow-hidden"
              >
                {/* Item Header */}
                <div className="flex items-center gap-3 p-4 cursor-pointer" onClick={() => setExpandedItem(expandedItem === item.id ? null : item.id)}>
                  <div className="flex-1">
                    <div className="font-bold text-sm text-foreground font-arabic">{item.title}</div>
                    <div className="text-xs text-muted-foreground mt-0.5">{item.reference}</div>
                  </div>
                  <div className="flex items-center gap-2">
                    {item.audioUrl && (
                      <button onClick={e => { e.stopPropagation(); playAudio(item); }}
                        className={cn('h-8 w-8 rounded-full flex items-center justify-center transition-all',
                          playingId === item.id ? 'bg-emerald-600 text-white animate-pulse' : 'bg-emerald-500/10 text-emerald-600 hover:bg-emerald-500/20'
                        )}>
                        {playingId === item.id ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4 ms-0.5" />}
                      </button>
                    )}
                    <button onClick={e => { e.stopPropagation(); toggleFavorite(item.id); }}
                      className="h-8 w-8 rounded-full flex items-center justify-center">
                      <Heart className={cn('h-4 w-4', favorites.includes(item.id) ? 'fill-rose-500 text-rose-500' : 'text-muted-foreground')} />
                    </button>
                    <ChevronDown className={cn('h-4 w-4 text-muted-foreground transition-transform', expandedItem === item.id && 'rotate-180')} />
                  </div>
                </div>

                {/* Expanded Content */}
                <AnimatePresence>
                  {expandedItem === item.id && (
                    <motion.div initial={{height:0,opacity:0}} animate={{height:'auto',opacity:1}} exit={{height:0,opacity:0}}>
                      <div className="px-4 pb-4 space-y-3 border-t border-border/50 pt-3">
                        {/* Arabic Text */}
                        <p className="text-foreground font-arabic text-lg leading-relaxed text-center whitespace-pre-line bg-muted/30 rounded-xl p-4">
                          {item.arabic}
                        </p>
                        {/* Benefit */}
                        {item.benefit && (
                          <div className="flex items-start gap-2 p-3 bg-emerald-500/5 border border-emerald-500/20 rounded-xl">
                            <Shield className="h-4 w-4 text-emerald-500 mt-0.5 shrink-0" />
                            <p className="text-xs text-emerald-700 dark:text-emerald-300 font-arabic leading-relaxed">{item.benefit}</p>
                          </div>
                        )}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
