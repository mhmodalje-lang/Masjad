import { useLocale } from '@/hooks/useLocale';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { Coins, ShoppingBag, Crown, Sparkles, Gift, Heart, Check, Lock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

const CATEGORY_ICONS: Record<string, typeof Coins> = {
  frame: Crown, theme: Sparkles, badge: Gift, effect: Sparkles, membership: Crown, charity: Heart,
};

const CATEGORY_LABELS: Record<string, string> = {
  all: 'الكل', frame: 'إطارات', theme: 'خلفيات', badge: 'شارات', effect: 'تأثيرات', membership: 'عضويات', charity: 'صدقات',
};

interface StoreItemType {
  id: string; name: string; description: string; price_gold: number; price_usd: number; category: string; image_url: string | null;
}

export default function Store() {
  const { user, getToken } = useAuth();
  const [items, setItems] = useState<StoreItemType[]>([]);
  const [gold, setGold] = useState(0);
  const [category, setCategory] = useState('all');
  const [loading, setLoading] = useState(true);
  const [purchases, setPurchases] = useState<string[]>([]);

  useEffect(() => {
    Promise.all([
      fetch(`${BACKEND_URL}/api/store/items`).then(r => r.json()),
      user ? fetch(`${BACKEND_URL}/api/rewards/balance`, { headers: { Authorization: `Bearer ${getToken()}` } }).then(r => r.json()) : Promise.resolve({ gold: 0 }),
      user ? fetch(`${BACKEND_URL}/api/store/my-purchases`, { headers: { Authorization: `Bearer ${getToken()}` } }).then(r => r.json()) : Promise.resolve({ purchases: [] }),
    ]).then(([storeData, balanceData, purchData]) => {
      setItems(storeData.items || []);
      setGold(balanceData.gold || 0);
      setPurchases((purchData.purchases || []).map((p: any) => p.item_id));
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [user]);

  const handleBuy = async (item: StoreItemType) => {
    if (!user) { toast.error('يجب تسجيل الدخول أولاً'); return; }
    if (gold < item.price_gold) { toast.error('رصيد الذهب غير كافٍ'); return; }

    try {
      const res = await fetch(`${BACKEND_URL}/api/store/buy-gold`, {
        method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` },
        body: JSON.stringify({ item_id: item.id }),
      });
      const data = await res.json();
      if (res.ok) {
        toast.success(data.message);
        setGold(data.gold_remaining);
        setPurchases(prev => [...prev, item.id]);
      } else {
        toast.error(data.detail || 'فشل الشراء');
      }
    } catch { toast.error('حدث خطأ'); }
  };

  const filtered = category === 'all' ? items : items.filter(i => i.category === category);
  const categories = ['all', ...new Set(items.map(i => i.category))];

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="store-page">
      {/* Header */}
      <div className="bg-gradient-to-br from-amber-900 via-yellow-900 to-orange-900 px-5 pb-14 pt-safe-header overflow-hidden relative">
        <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 30% 40%, rgba(255,215,0,0.3), transparent 50%)' }} />
        <div className="relative pt-4 text-center">
          <ShoppingBag className="h-10 w-10 mx-auto mb-2 text-amber-300" />
          <h1 className="text-2xl font-bold text-white mb-1">المتجر</h1>
          <p className="text-white/60 text-sm mb-4">اقتنِ عناصر مميزة بالذهب</p>
          
          {/* Gold balance */}
          <div className="inline-flex items-center gap-2 bg-black/30 backdrop-blur-xl rounded-full px-5 py-2.5">
            <Coins className="h-5 w-5 text-amber-400" />
            <span className="text-xl font-bold text-amber-300 tabular-nums">{gold}</span>
            <span className="text-amber-300/60 text-xs">ذهب</span>
          </div>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Categories */}
      <div className="px-4 mt-2 mb-4 flex gap-2 overflow-x-auto no-scrollbar">
        {categories.map(cat => (
          <button key={cat} onClick={() => setCategory(cat)}
            className={cn('shrink-0 px-4 py-2 rounded-full text-xs font-bold transition-all',
              category === cat ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
            )} data-testid={`store-cat-${cat}`}>
            {CATEGORY_LABELS[cat] || cat}
          </button>
        ))}
      </div>

      {/* Items Grid */}
      {loading ? (
        <div className="flex justify-center py-12"><div className="h-8 w-8 border-2 border-primary border-t-transparent rounded-full animate-spin" /></div>
      ) : (
        <div className="px-4 grid grid-cols-2 gap-3">
          {filtered.map((item, i) => {
            const Icon = CATEGORY_ICONS[item.category] || Gift;
            const owned = purchases.includes(item.id);
            return (
              <motion.div key={item.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
                className={cn('rounded-2xl border bg-card overflow-hidden transition-all', owned && 'border-primary/30 bg-primary/5')}
                data-testid={`store-item-${item.id}`}>
                <div className="p-4 text-center">
                  <div className={cn('h-14 w-14 mx-auto mb-3 rounded-2xl flex items-center justify-center',
                    owned ? 'bg-primary/15' : 'bg-muted')}>
                    {owned ? <Check className="h-6 w-6 text-primary" /> : <Icon className="h-6 w-6 text-muted-foreground" />}
                  </div>
                  <h3 className="text-sm font-bold text-foreground mb-1">{item.name}</h3>
                  <p className="text-[11px] text-muted-foreground mb-3 line-clamp-2">{item.description}</p>
                  
                  {owned ? (
                    <span className="text-xs text-primary font-bold">مملوك</span>
                  ) : (
                    <div className="space-y-1.5">
                      <div className="flex items-center justify-center gap-1">
                        <Coins className="h-3.5 w-3.5 text-amber-500" />
                        <span className="text-sm font-bold text-foreground">{item.price_gold}</span>
                      </div>
                      <Button size="sm" className="w-full rounded-xl h-8 text-xs" onClick={() => handleBuy(item)}
                        disabled={gold < item.price_gold}
                        data-testid={`buy-${item.id}`}>
                        {gold < item.price_gold ? <Lock className="h-3 w-3 me-1" /> : null}
                        {gold < item.price_gold ? 'غير كافٍ' : 'شراء'}
                      </Button>
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}
