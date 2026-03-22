import { useLocale } from '@/hooks/useLocale';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { MapPin, Search, ShoppingCart, Tag, Plus, Store as StoreIcon, Check, Clock, FileText, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { AnimatedBackground } from '@/components/AnimatedBackground';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Product {
  id: string; name: string; description: string; price: number; currency: string;
  category: string; image_url: string; vendor_name: string; location: { city?: string };
}

export default function Marketplace() {
  const { t, dir } = useLocale();
  const { user, getToken } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [category, setCategory] = useState('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [vendorStatus, setVendorStatus] = useState<any>(null);
  const [showRegister, setShowRegister] = useState(false);
  const [regForm, setRegForm] = useState({ shop_name: '', description: '', phone: '', iban: '' });
  const [showAddProduct, setShowAddProduct] = useState(false);
  const [productForm, setProductForm] = useState({ name: '', description: '', price: '', category: 'general', currency: 'EUR' });
  const [submitting, setSubmitting] = useState(false);

  const CATEGORIES = [
    { key: 'all', label: t('marketCatAll') },
    { key: 'clothing', label: t('marketCatClothing') },
    { key: 'books', label: t('marketCatBooks') },
    { key: 'accessories', label: t('marketCatAccessories') },
    { key: 'food', label: t('marketCatFood') },
    { key: 'perfume', label: t('marketCatPerfume') },
    { key: 'general', label: t('marketCatGeneral') },
  ];

  useEffect(() => { loadProducts(); checkVendor(); }, [category]);

  const checkVendor = async () => {
    if (!user) return;
    try {
      const r = await fetch(`${BACKEND_URL}/api/marketplace/vendor-status`, { headers: { Authorization: `Bearer ${getToken()}` } });
      const d = await r.json();
      setVendorStatus(d.vendor);
    } catch {}
  };

  const loadProducts = async () => {
    setLoading(true);
    try {
      let url = `${BACKEND_URL}/api/marketplace/products?category=${category}`;
      try {
        const pos = await new Promise<GeolocationPosition>((res, rej) => navigator.geolocation.getCurrentPosition(res, rej, { timeout: 3000 }));
        url += `&lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`;
      } catch {}
      const res = await fetch(url);
      const data = await res.json();
      setProducts(data.products || []);
    } catch {}
    setLoading(false);
  };

  const registerVendor = async () => {
    if (!regForm.shop_name.trim()) { toast.error(t('enterShopName')); return; }
    setSubmitting(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/marketplace/register-vendor`, {
        method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` },
        body: JSON.stringify(regForm),
      });
      const d = await r.json();
      if (r.ok) { toast.success(d.message || t('requestSent')); setVendorStatus(d.vendor); setShowRegister(false); }
      else toast.error(d.detail || t('errorOccurred'));
    } catch { toast.error(t('errorOccurred')); }
    setSubmitting(false);
  };

  const addProduct = async () => {
    if (!productForm.name || !productForm.price) { toast.error(t('fillNameAndPrice')); return; }
    setSubmitting(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/marketplace/products`, {
        method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` },
        body: JSON.stringify({ ...productForm, price: parseFloat(productForm.price) }),
      });
      const d = await r.json();
      if (r.ok) { toast.success(t('productAdded')); setShowAddProduct(false); loadProducts(); }
      else toast.error(d.detail || t('errorOccurred'));
    } catch { toast.error(t('errorOccurred')); }
    setSubmitting(false);
  };

  const filtered = search ? products.filter(p => p.name.includes(search) || p.description.includes(search)) : products;
  const isApprovedVendor = vendorStatus?.status === 'approved';

  return (
    <div className="min-h-screen pb-24" dir={dir} data-testid="marketplace-page">
      <div className="relative bg-gradient-to-br from-teal-900 via-emerald-900 to-green-900 px-5 pb-16 pt-safe-header overflow-hidden">
        <AnimatedBackground variant="marketplace" />
        <div className="relative pt-4 text-center z-10">
          <StoreIcon className="h-10 w-10 mx-auto mb-2 text-teal-600 dark:text-teal-300" />
          <h1 className="text-2xl font-bold text-white mb-1">{t('marketplaceTitle')}</h1>
          <p className="text-white/60 text-sm">{t('marketplaceSubtitle')}</p>
        </div>
        <div className="absolute -bottom-6 left-0 right-0 h-12 rounded-t-[2rem] bg-background" />
      </div>

      {user && !isApprovedVendor && (
        <div className="px-4 mt-2 mb-3">
          {vendorStatus?.status === 'pending' ? (
            <div className="rounded-2xl bg-amber-500/10 border border-amber-500/20 p-4 flex items-center gap-3">
              <Clock className="h-5 w-5 text-amber-500 shrink-0" />
              <div><p className="text-sm font-bold text-foreground">{t('requestUnderReview')}</p><p className="text-[10px] text-muted-foreground">{t('willNotifyApproval')}</p></div>
            </div>
          ) : !vendorStatus ? (
            <button onClick={() => setShowRegister(true)} className="w-full rounded-2xl bg-primary/10 border border-primary/20 p-4 flex items-center gap-3 active:scale-[0.98] transition-transform" data-testid="register-vendor-btn">
              <FileText className="h-5 w-5 text-primary shrink-0" />
              <div className="text-start"><p className="text-sm font-bold text-foreground">{t('wantToSell')}</p><p className="text-[10px] text-muted-foreground">{t('registerAndPublish')}</p></div>
            </button>
          ) : null}
        </div>
      )}

      <AnimatePresence>
        {showRegister && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="px-4 mb-3 overflow-hidden">
            <div className="rounded-2xl bg-card border border-primary/20 p-4 space-y-3">
              <p className="text-sm font-bold text-foreground">{t('registerAsVendor')}</p>
              <Input placeholder={t('enterShopName')} value={regForm.shop_name} onChange={e => setRegForm({...regForm, shop_name: e.target.value})} className="rounded-xl" />
              <Input placeholder={t('messagePlaceholder')} value={regForm.description} onChange={e => setRegForm({...regForm, description: e.target.value})} className="rounded-xl" />
              <Input placeholder={t('phoneWhatsapp')} value={regForm.phone} onChange={e => setRegForm({...regForm, phone: e.target.value})} className="rounded-xl" />
              <Input placeholder="IBAN" value={regForm.iban} onChange={e => setRegForm({...regForm, iban: e.target.value})} className="rounded-xl" />
              <div className="flex gap-2">
                <Button onClick={registerVendor} disabled={submitting} className="flex-1 rounded-xl">{submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : t('sendBtn')}</Button>
                <Button variant="outline" onClick={() => setShowRegister(false)} className="rounded-xl">{t('cancelBtn')}</Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="px-4 mt-2 mb-3 flex gap-2">
        <div className="flex-1 relative">
          <Search className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input placeholder={t('search') || 'Search...'} value={search} onChange={e => setSearch(e.target.value)} className="ps-9 rounded-xl" data-testid="marketplace-search" />
        </div>
        {isApprovedVendor && (
          <Button size="icon" className="rounded-xl h-10 w-10 shrink-0" onClick={() => setShowAddProduct(!showAddProduct)} data-testid="add-product-btn">
            <Plus className="h-4 w-4" />
          </Button>
        )}
      </div>

      <AnimatePresence>
        {showAddProduct && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="px-4 mb-3 overflow-hidden">
            <div className="rounded-2xl bg-card border border-primary/20 p-4 space-y-3">
              <p className="text-sm font-bold text-foreground">{t('productAdded').replace(t('productAdded'), t('publishBtn'))}</p>
              <Input placeholder={t('namePlaceholder')} value={productForm.name} onChange={e => setProductForm({...productForm, name: e.target.value})} className="rounded-xl" />
              <Input placeholder={t('messagePlaceholder')} value={productForm.description} onChange={e => setProductForm({...productForm, description: e.target.value})} className="rounded-xl" />
              <div className="grid grid-cols-2 gap-2">
                <Input placeholder={t('amountPlaceholder')} type="number" value={productForm.price} onChange={e => setProductForm({...productForm, price: e.target.value})} className="rounded-xl" />
                <select value={productForm.category} onChange={e => setProductForm({...productForm, category: e.target.value})}
                  className="rounded-xl bg-muted border border-border px-3 py-2 text-sm text-foreground">
                  {CATEGORIES.filter(c => c.key !== 'all').map(c => <option key={c.key} value={c.key}>{c.label}</option>)}
                </select>
              </div>
              <Button onClick={addProduct} disabled={submitting} className="w-full rounded-xl">{submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : t('publishBtn')}</Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="px-4 mb-4 flex gap-2 overflow-x-auto no-scrollbar">
        {CATEGORIES.map(c => (
          <button key={c.key} onClick={() => setCategory(c.key)}
            className={cn('shrink-0 px-4 py-2 rounded-full text-xs font-bold transition-all',
              category === c.key ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground')}>
            {c.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex justify-center py-12"><div className="h-8 w-8 border-2 border-primary border-t-transparent rounded-full animate-spin" /></div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16">
          <ShoppingCart className="h-12 w-12 mx-auto mb-3 text-muted-foreground/20" />
          <p className="text-sm text-muted-foreground">{t('noRequestsNow')}</p>
        </div>
      ) : (
        <div className="px-4 grid grid-cols-2 gap-3">
          {filtered.map((p, i) => (
            <motion.div key={p.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}
              className="rounded-2xl neu-card overflow-hidden" data-testid={`product-${p.id}`}>
              <div className="h-28 bg-muted/50 flex items-center justify-center">
                {p.image_url ? <img src={p.image_url.startsWith('/api') ? `${BACKEND_URL}${p.image_url}` : p.image_url} alt="" className="h-full w-full object-cover" /> :
                  <Tag className="h-8 w-8 text-muted-foreground/20" />}
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
