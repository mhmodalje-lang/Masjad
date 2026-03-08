import { useState } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Sun, Moon } from 'lucide-react';

const morningAdhkar = [
  { arabic: 'أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ', translation: 'We have reached the morning and at this very time the whole kingdom belongs to Allah. All praise is for Allah.', count: 1 },
  { arabic: 'اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ', translation: 'O Allah, by Your grace we have reached the morning, by Your grace we reach the evening, by Your grace we live and die, and to You is the resurrection.', count: 1 },
  { arabic: 'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ', translation: 'Glory be to Allah and praise Him.', count: 100 },
  { arabic: 'لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ', translation: 'None has the right to be worshipped except Allah, alone, without partner. To Him belongs all sovereignty and praise, and He is over all things omnipotent.', count: 10 },
  { arabic: 'أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ', translation: 'I seek refuge in the complete words of Allah from the evil of what He has created.', count: 3 },
];

const eveningAdhkar = [
  { arabic: 'أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ', translation: 'We have reached the evening and at this very time the whole kingdom belongs to Allah. All praise is for Allah.', count: 1 },
  { arabic: 'اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ', translation: 'O Allah, by Your grace we have reached the evening, by Your grace we reach the morning, by Your grace we live and die, and to You is the final return.', count: 1 },
  { arabic: 'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ', translation: 'Glory be to Allah and praise Him.', count: 100 },
  { arabic: 'أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ', translation: 'I seek refuge in the complete words of Allah from the evil of what He has created.', count: 3 },
];

export default function Duas() {
  const { t } = useLocale();
  const [tab, setTab] = useState<'morning' | 'evening'>('morning');
  const adhkar = tab === 'morning' ? morningAdhkar : eveningAdhkar;

  return (
    <div className="min-h-screen">
      <div className="gradient-islamic px-5 pb-6 pt-12">
        <h1 className="text-2xl font-bold text-primary-foreground">{t('duas')}</h1>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[50%] bg-background" />
      </div>

      {/* Tabs */}
      <div className="px-5 pt-4 mb-4">
        <div className="flex gap-2">
          {(['morning', 'evening'] as const).map((key) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={cn(
                'flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition-all',
                tab === key
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary text-secondary-foreground'
              )}
            >
              {key === 'morning' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              {t(key === 'morning' ? 'morningAdhkar' : 'eveningAdhkar')}
            </button>
          ))}
        </div>
      </div>

      {/* Adhkar list */}
      <div className="px-5 space-y-4 pb-8">
        {adhkar.map((item, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="rounded-xl border border-border bg-card p-5"
          >
            <p className="text-xl font-arabic text-foreground leading-[2] text-right mb-3" dir="rtl">
              {item.arabic}
            </p>
            <p className="text-sm text-muted-foreground mb-2">{item.translation}</p>
            <span className="inline-block rounded-full bg-primary/10 px-3 py-0.5 text-xs font-medium text-primary">
              ×{item.count}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
