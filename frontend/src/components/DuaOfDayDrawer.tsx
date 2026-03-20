import { useState } from 'react';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { Drawer, DrawerContent } from '@/components/ui/drawer';
import { dailyDuas } from '@/data/dhikrDetails';
import { useLocale } from '@/hooks/useLocale';

interface Props {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

function getTodayDua() {
  const dayOfYear = Math.floor((Date.now() - new Date(new Date().getFullYear(), 0, 0).getTime()) / 86400000);
  return dailyDuas[dayOfYear % dailyDuas.length];
}

export default function DuaOfDayDrawer({ open, onOpenChange }: Props) {
  const { t, dir, locale } = useLocale();
  const dua = getTodayDua();
  const isAr = locale === 'ar';
  const [done, setDone] = useState(() => {
    const key = new Date().toISOString().split('T')[0];
    return localStorage.getItem(`dua-done-${key}`) === '1';
  });

  const markDone = () => {
    const key = new Date().toISOString().split('T')[0];
    localStorage.setItem(`dua-done-${key}`, '1');
    setDone(true);
    setTimeout(() => onOpenChange(false), 600);
  };

  return (
    <Drawer open={open} onOpenChange={onOpenChange}>
      <DrawerContent className="pb-8 max-h-[85vh]">
        <div className="flex flex-col items-center px-5 pt-4 pb-2 overflow-y-auto" dir={dir}>
          {/* Title */}
          <h3 className="text-base font-bold text-foreground mb-1">{t(dua.titleKey)}</h3>
          <p className="text-xs text-muted-foreground mb-4">{t(dua.subtitleKey)}</p>

          {/* Arabic Text - Clean container with no overflow */}
          <div className="bg-muted/30 rounded-2xl p-5 mb-3 w-full">
            <p
              className="text-lg text-foreground text-center leading-[2.5] whitespace-pre-line"
              dir="rtl"
              style={{ fontFamily: "'Amiri', 'Traditional Arabic', 'Noto Naskh Arabic', serif" }}
            >
              {dua.arabic}
            </p>
          </div>

          {/* Translation for non-Arabic users */}
          {!isAr && dua.translationKey && (
            <div className="bg-primary/5 rounded-xl p-3.5 mb-3 w-full border border-primary/10">
              <p className="text-sm text-foreground text-center leading-relaxed" dir="auto">
                {t(dua.translationKey)}
              </p>
            </div>
          )}

          {/* Transliteration - Separate clear section */}
          {dua.transliteration && (
            <div className="bg-blue-500/5 rounded-xl p-3.5 mb-3 w-full border border-blue-500/10">
              <p className="text-xs text-muted-foreground text-center italic leading-relaxed" dir="ltr">
                {dua.transliteration}
              </p>
            </div>
          )}

          {/* Reference */}
          {dua.referenceKey && (
            <p className="text-[11px] text-primary font-bold bg-primary/8 px-3 py-1 rounded-lg mb-5">
              {t(dua.referenceKey)}
            </p>
          )}

          {/* Complete button */}
          <button
            onClick={markDone}
            className="relative active:scale-95 transition-transform"
          >
            <motion.div
              className={`h-14 w-14 rounded-full flex items-center justify-center shadow-lg ${done ? 'bg-primary' : 'bg-accent'}`}
              animate={done ? { scale: [1, 1.2, 1] } : {}}
            >
              <Check className={`h-7 w-7 ${done ? 'text-primary-foreground' : 'text-accent-foreground'}`} />
            </motion.div>
          </button>
          {!done && <p className="text-xs text-muted-foreground mt-2">{t('tapToMarkComplete')}</p>}
        </div>
      </DrawerContent>
    </Drawer>
  );
}
