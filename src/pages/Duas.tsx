import { useState } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import {
  Search, Bookmark, ChevronDown,
  Bed, Droplets, Home, Shirt, Plane, UtensilsCrossed,
  Heart, Stethoscope, Frown, SmilePlus, Shield,
  Landmark, Users
} from 'lucide-react';
import { duasData } from '@/data/duas';

interface CatItem {
  icon: any;
  label: string;
  dataKey: string;
  useEmoji?: boolean;
}

const dailyCategories: CatItem[] = [
  { icon: Bed, label: 'النوم', dataKey: 'sleep' },
  { icon: Droplets, label: 'الوضوء', dataKey: 'wudu' },
  { icon: Landmark, label: 'مسجد', dataKey: 'mosque' },
  { icon: Heart, label: 'صلاة', dataKey: 'salah' },
  { icon: Home, label: 'منزل', dataKey: 'home' },
  { icon: Shirt, label: 'ملابس', dataKey: 'clothes' },
  { icon: Plane, label: 'سفر', dataKey: 'travel' },
  { icon: UtensilsCrossed, label: 'طعام', dataKey: 'food' },
];

const adhkarCategories: CatItem[] = [
  { icon: '📿', label: 'الذكر اليومي', dataKey: 'daily-dhikr', useEmoji: true },
  { icon: '🌙', label: 'إحياء الذكرى اليومي', dataKey: 'daily-revival', useEmoji: true },
  { icon: '🤲', label: 'بعد الصلوات', dataKey: 'after-prayer', useEmoji: true },
  { icon: '🍎', label: 'رزق', dataKey: 'rizq', useEmoji: true },
  { icon: '📖', label: 'معرفة', dataKey: 'knowledge', useEmoji: true },
  { icon: '🕌', label: 'الإيمان', dataKey: 'faith', useEmoji: true },
  { icon: '⚖️', label: 'يوم الحساب', dataKey: 'judgment', useEmoji: true },
  { icon: '💚', label: 'مغفرة', dataKey: 'forgiveness', useEmoji: true },
  { icon: '🤲', label: 'مشيداً بالله', dataKey: 'praising', useEmoji: true },
];

const moreCategories: CatItem[] = [
  { icon: Users, label: 'عائلة', dataKey: 'family' },
  { icon: Stethoscope, label: 'الصحة / المرض', dataKey: 'health' },
  { icon: Frown, label: 'الخسارة / الفشل', dataKey: 'loss' },
  { icon: SmilePlus, label: 'الحزن / السعادة', dataKey: 'sadness' },
  { icon: Shield, label: 'الصبر', dataKey: 'patience' },
  { icon: Heart, label: 'الدّين', dataKey: 'debt' },
  { icon: Heart, label: 'أثناء الحيض', dataKey: 'menstruation' },
];

const occasionalCategories: CatItem[] = [
  { icon: '🪦', label: 'المتوفى', dataKey: 'deceased', useEmoji: true },
  { icon: '🕋', label: 'الحج / العمرة', dataKey: 'hajj', useEmoji: true },
  { icon: '🌙', label: 'رمضان', dataKey: 'ramadan', useEmoji: true },
  { icon: '🌳', label: 'طبيعة', dataKey: 'nature', useEmoji: true },
  { icon: '🤝', label: 'السلوكيات الحميدة', dataKey: 'goodManners', useEmoji: true },
  { icon: '🪧', label: 'إتخاذ القرار / التوجيه', dataKey: 'guidance', useEmoji: true },
];

export default function Duas() {
  const { t } = useLocale();
  const [expandedKey, setExpandedKey] = useState<string | null>(null);

  const toggle = (key: string) => {
    setExpandedKey(expandedKey === key ? null : key);
  };

  const renderSection = (title: string, items: CatItem[]) => (
    <>
      <div className="px-5 mt-6 mb-2">
        <p className="text-sm font-bold text-foreground">{title}</p>
      </div>
      <div className="px-5">
        {items.map((cat) => {
          const category = duasData[cat.dataKey];
          const duas = category?.duas || [];
          const isOpen = expandedKey === cat.dataKey;
          return (
            <div key={cat.dataKey}>
              <button
                onClick={() => toggle(cat.dataKey)}
                className="w-full flex items-center justify-between py-4 border-b border-border"
              >
                <div className="flex items-center gap-2">
                  <ChevronDown className={cn(
                    'h-4 w-4 text-muted-foreground transition-transform',
                    isOpen && 'rotate-180'
                  )} />
                  <span className="text-[10px] text-muted-foreground">({duas.length})</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="font-medium text-foreground">{cat.label}</span>
                  {cat.useEmoji ? (
                    <span className="text-2xl">{cat.icon}</span>
                  ) : (
                    <cat.icon className="h-6 w-6 text-muted-foreground" />
                  )}
                </div>
              </button>
              {isOpen && duas.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  className="py-3 space-y-3"
                >
                  {duas.map((dua, j) => (
                    <div key={j} className="rounded-xl bg-card border border-border p-4">
                      <p className="text-lg font-arabic text-foreground leading-[2] text-center mb-2">
                        {dua.arabic}
                      </p>
                      <p className="text-xs text-muted-foreground mb-1">
                        {t(dua.translationKey)}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] text-primary font-medium">×{dua.count}</span>
                        {dua.reference && (
                          <span className="text-[10px] text-muted-foreground">📖 {dua.reference}</span>
                        )}
                      </div>
                    </div>
                  ))}
                </motion.div>
              )}
            </div>
          );
        })}
      </div>
    </>
  );

  return (
    <div className="min-h-screen pb-safe" dir="rtl">
      <div className="px-5 pt-12 pb-3 flex items-center justify-between">
        <div className="flex gap-3">
          <button className="p-1"><Search className="h-5 w-5 text-muted-foreground" /></button>
          <button className="p-1"><Bookmark className="h-5 w-5 text-muted-foreground" /></button>
        </div>
        <h1 className="text-xl font-bold text-foreground">الدُعاء والذكر</h1>
      </div>

      {renderSection('يومي', dailyCategories)}
      {renderSection('أذكار', adhkarCategories)}
      {renderSection('أخرى', moreCategories)}
      {renderSection('متقطع', occasionalCategories)}

      <div className="h-8" />
    </div>
  );
}
