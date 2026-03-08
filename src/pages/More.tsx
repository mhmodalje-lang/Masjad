import { useLocale } from '@/hooks/useLocale';
import { Link } from 'react-router-dom';
import { Heart, Calendar, BarChart3, Calculator, Settings } from 'lucide-react';
import { motion } from 'framer-motion';

const items = [
  { icon: Heart, labelKey: 'tasbeeh', path: '/tasbeeh', color: 'text-primary' },
  { icon: Calendar, labelKey: 'calendar', path: '/calendar', color: 'text-islamic-green' },
  { icon: BarChart3, labelKey: 'tracker', path: '/tracker', color: 'text-accent' },
  { icon: Calculator, labelKey: 'zakatCalculator', path: '/zakat', color: 'text-islamic-gold' },
  { icon: Settings, labelKey: 'settings', path: '/settings', color: 'text-muted-foreground' },
];

export default function More() {
  const { t } = useLocale();

  return (
    <div className="min-h-screen">
      <div className="gradient-islamic px-5 pb-6 pt-12">
        <h1 className="text-2xl font-bold text-primary-foreground">{t('more')}</h1>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[50%] bg-background" />
      </div>

      <div className="px-5 pt-4 space-y-3">
        {items.map((item, i) => (
          <motion.div
            key={item.path}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.06 }}
          >
            <Link
              to={item.path}
              className="flex items-center gap-4 rounded-xl border border-border bg-card p-4 hover:shadow-md transition-all active:scale-[0.98]"
            >
              <item.icon className={`h-6 w-6 ${item.color}`} />
              <span className="text-foreground font-medium">{t(item.labelKey)}</span>
            </Link>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
