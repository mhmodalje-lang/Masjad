import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { MapPin, Search, ShoppingCart, Tag, Plus, Store as StoreIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Product {
  id: string; name: string; description: string; price: number; currency: string;
  category: string; image_url: string; vendor_name: string; location: { city?: string };
}

const CATEGORIES = [
  { key: 'all', label: 'الكل' },
  { key: 'clothing', label: 'ملابس' },
  { key: 'books', label: 'كتب' },
  { key: 'accessories', label: 'إكسسوارات' },
  { key: 'food', label: 'طعام' },
  { key: 'perfume', label: 'عطور' },
  { key: 'general', label: 'عام' },
];

export default function Marketplace() {
  const { user, getToken } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [category, setCategory] = useState('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState({ name: '', description: '', price: '', category: 'general', currency: 'EUR' });

  useEffect(() => {
    loadProducts();
  }, [category]);

  const loadProducts = async () => {
    setLoading(true);
    try {
      let url = `${BACKEND_URL}/api/marketplace/products?category=${category}`;
      if (navigator.geolocation) {
        const pos = await new Promise<GeolocationPosition>((resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 3000 })).catch(() => null);
        if (pos) url += `&lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`;
      }
      const res = await fetch(url);
      const data = await res.json();
      setProducts(data.products || []);
    } catch { }
    setLoading(false);
  };

  const addProduct = async () => {
    if (!user) { toast.error('سجّل دخولك أولاً'); return; }
    if (!form.name || !form.price) { toast.error('يجب ملء الاسم والسعر'); return; }

    let location = {};
    try {
      const pos = await new Promise<GeolocationPosition>((resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 3000 }));
      location = { lat: pos.coords.latitude, lon: pos.coords.longitude };
    } catch { }

    try {
      const res = await fetch(`${BACKEND_URL}/api/marketplace/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` },
        body: JSON.stringify({ ...form, price: parseFloat(form.price), location }),
      });
      if (res.ok) {
        toast.success('تم إضافة المنتج');
        setShowAdd(false);
        setForm({ name: '', description: '', price: '', category: 'general', currency: 'EUR' });
        loadProducts();
      }
    } catch { toast.error('حدث خطأ'); }
  };

  const filtered = search ? products.filter(p => p.name.includes(search) || p.description.includes(search)) : products;

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="marketplace-page">
      {/* Header */}
      <div className="bg-gradient-to-br from-teal-900 via-emerald-900 to-green-900 px-5 pb-14 pt-safe-header overflow-hidden relative">
        <div className="relative pt-4 text-center">
          <StoreIcon className="h-10 w-10 mx-auto mb-2 text-teal-300" />
          <h1 className="text-2xl font-bold text-white mb-1">السوق</h1>
          <p className="text-white/60 text-sm">منتجات إسلامية من حولك</p>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {/* Search + Add */}
      <div className="px-4 mt-2 mb-3 flex gap-2">
        <div className="flex-1 relative">
          <Search className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input placeholder="بحث..." value={search} onChange={e => setSearch(e.target.value)}
            className="ps-9 rounded-xl" data-testid="marketplace-search" />
        </div>
        {user && (
          <Button size="icon" variant="outline" className="rounded-xl h-10 w-10 shrink-0"
            onClick={() => setShowAdd(!showAdd)} data-testid="add-product-btn">
            <Plus className="h-4 w-4" />
          </Button>
        )}
      </div>

      {/* Add Product Form */}
      {showAdd && (
        <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} className="px-4 mb-4">
          <div className="rounded-2xl bg-card border border-primary/20 p-4 space-y-3">
            <p className="text-sm font-bold text-foreground">إضافة منتج</p>
            <Input placeholder="اسم المنتج" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} className="rounded-xl" />
            <Input placeholder="الوصف" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} className="rounded-xl" />
            <div className="grid grid-cols-2 gap-2">
              <Input placeholder="السعر" type="number" value={form.price} onChange={e => setForm({ ...form, price: e.target.value })} className="rounded-xl" />
              <select value={form.category} onChange={e => setForm({ ...form, category: e.target.value })}
                className="rounded-xl bg-muted border border-border px-3 py-2 text-sm">
                {CATEGORIES.filter(c => c.key !== 'all').map(c => <option key={c.key} value={c.key}>{c.label}</option>)}
              </select>
            </div>
            <Button onClick={addProduct} className="w-full rounded-xl">نشر المنتج</Button>
          </div>
        </motion.div>
      )}

      {/* Categories */}
      <div className="px-4 mb-4 flex gap-2 overflow-x-auto no-scrollbar">
        {CATEGORIES.map(c => (
          <button key={c.key} onClick={() => setCategory(c.key)}
            className={cn('shrink-0 px-4 py-2 rounded-full text-xs font-bold transition-all',
              category === c.key ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground')}>
            {c.label}
          </button>
        ))}
      </div>

      {/* Products */}
      {loading ? (
        <div className="flex justify-center py-12"><div className="h-8 w-8 border-2 border-primary border-t-transparent rounded-full animate-spin" /></div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16">
          <ShoppingCart className="h-12 w-12 mx-auto mb-3 text-muted-foreground/30" />
          <p className="text-sm text-muted-foreground">لا توجد منتجات بعد</p>
        </div>
      ) : (
        <div className="px-4 grid grid-cols-2 gap-3">
          {filtered.map((p, i) => (
            <motion.div key={p.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}
              className="rounded-2xl bg-card border border-border/40 overflow-hidden" data-testid={`product-${p.id}`}>
              <div className="h-28 bg-muted/50 flex items-center justify-center">
                {p.image_url ? <img src={p.image_url.startsWith('/api') ? `${BACKEND_URL}${p.image_url}` : p.image_url} alt="" className="h-full w-full object-cover" /> :
                  <Tag className="h-8 w-8 text-muted-foreground/30" />}
              </div>
              <div className="p-3">
                <h3 className="text-sm font-bold text-foreground truncate">{p.name}</h3>
                <p className="text-[10px] text-muted-foreground line-clamp-2 mb-2">{p.description}</p>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-primary">{p.currency} {p.price}</span>
                  {p.location?.city && (
                    <span className="flex items-center gap-0.5 text-[9px] text-muted-foreground">
                      <MapPin className="h-2.5 w-2.5" />{p.location.city}
                    </span>
                  )}
                </div>
                <p className="text-[9px] text-muted-foreground mt-1">{p.vendor_name}</p>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
