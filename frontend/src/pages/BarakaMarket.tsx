import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { ArrowLeft, Coins, Star, ShoppingBag, Play, CheckCircle, Lock, ChevronRight, Sparkles, Trophy, TrendingUp, Eye } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

const API = import.meta.env.REACT_APP_BACKEND_URL || '';

/* ═══ Types ═══ */
interface StoreItem {
  id: string; category: string; name: string; name_ar: string; name_en: string;
  emoji: string; price: number; level_required: number; rarity: string;
  css_value: string; preview_color: string;
}
interface AdItem {
  id: string; title: string; video_url: string; thumbnail_url: string;
  points_reward: number; min_watch_seconds: number;
}
interface LevelInfo {
  level: number; xp: number; next_level_xp: number; prev_level_xp: number;
  progress: number; xp_needed: number;
}
interface RewardsProfile {
  user_id: string; total_points: number; available_points: number;
  spent_points: number; ads_watched: number;
  level: LevelInfo; inventory: string[]; equipped: Record<string, string>;
}

const RARITY_COLORS: Record<string, string> = {
  common: 'border-gray-400/30 bg-gray-500/5',
  rare: 'border-blue-400/40 bg-blue-500/10',
  epic: 'border-purple-400/40 bg-purple-500/10',
  legendary: 'border-[#D4AF37]/50 bg-[#D4AF37]/10 animate-pulse-glow',
};
const RARITY_TEXT: Record<string, string> = {
  common: 'text-gray-400', rare: 'text-blue-400', epic: 'text-purple-400', legendary: 'text-[#D4AF37]',
};

const CATEGORY_TABS = ['border', 'badge', 'shape', 'theme', 'font'] as const;
type CategoryTab = typeof CATEGORY_TABS[number];

export default function BarakaMarket() {
  const { t, locale, dir } = useLocale();
  const navigate = useNavigate();
  const userId = localStorage.getItem('noor_user_id') || 'guest_' + Math.random().toString(36).slice(2, 8);
  const isRTL = dir === 'rtl';

  // Store userId for persistence
  useEffect(() => {
    if (!localStorage.getItem('noor_user_id')) {
      localStorage.setItem('noor_user_id', userId);
    }
  }, [userId]);

  const [activeTab, setActiveTab] = useState<'store' | 'inventory' | 'earn'>('store');
  const [storeCategory, setStoreCategory] = useState<CategoryTab>('border');
  const [profile, setProfile] = useState<RewardsProfile | null>(null);
  const [storeItems, setStoreItems] = useState<StoreItem[]>([]);
  const [ads, setAds] = useState<AdItem[]>([]);
  const [canWatch, setCanWatch] = useState(true);
  const [cooldown, setCooldown] = useState(0);
  const [watchingAd, setWatchingAd] = useState<string | null>(null);
  const [watchProgress, setWatchProgress] = useState(0);
  const [videoPlaying, setVideoPlaying] = useState(false);
  const [videoEnded, setVideoEnded] = useState(false);
  const [currentAd, setCurrentAd] = useState<AdItem | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const [loading, setLoading] = useState(true);
  const cooldownRef = useRef<NodeJS.Timeout | null>(null);
  const progressRef = useRef<NodeJS.Timeout | null>(null);

  const loadProfile = useCallback(async () => {
    try {
      const r = await fetch(`${API}/api/rewards/profile/${userId}`);
      const d = await r.json();
      if (d.success) setProfile(d.profile);
    } catch { }
  }, [userId]);

  const loadStore = useCallback(async () => {
    try {
      const r = await fetch(`${API}/api/rewards/store?locale=${locale}`);
      const d = await r.json();
      if (d.success) setStoreItems(d.items);
    } catch { }
  }, [locale]);

  const loadAds = useCallback(async () => {
    try {
      const r = await fetch(`${API}/api/rewards/ads?user_id=${userId}`);
      const d = await r.json();
      if (d.success) {
        setAds(d.ads);
        setCanWatch(d.can_watch);
        if (d.cooldown_remaining > 0) {
          setCooldown(d.cooldown_remaining);
        }
      }
    } catch { }
  }, [userId]);

  useEffect(() => {
    setLoading(true);
    Promise.all([loadProfile(), loadStore(), loadAds()]).finally(() => setLoading(false));
  }, [loadProfile, loadStore, loadAds]);

  // Cooldown countdown
  useEffect(() => {
    if (cooldown > 0) {
      cooldownRef.current = setInterval(() => {
        setCooldown(p => {
          if (p <= 1) {
            clearInterval(cooldownRef.current!);
            setCanWatch(true);
            return 0;
          }
          return p - 1;
        });
      }, 1000);
      return () => { if (cooldownRef.current) clearInterval(cooldownRef.current); };
    }
  }, [cooldown]);

  const handleWatchAd = async (ad: AdItem) => {
    if (!canWatch || watchingAd) return;
    setWatchingAd(ad.id);
    setCurrentAd(ad);
    setWatchProgress(0);
    setVideoPlaying(true);
    setVideoEnded(false);
  };

  // Track video progress via timeupdate
  const onVideoTimeUpdate = () => {
    if (!videoRef.current || !currentAd) return;
    const progress = videoRef.current.currentTime / Math.max(1, currentAd.min_watch_seconds);
    setWatchProgress(Math.min(1, progress));
    if (videoRef.current.currentTime >= currentAd.min_watch_seconds && !videoEnded) {
      setVideoEnded(true);
      completeAdWatch(currentAd);
    }
  };

  const onVideoEnded = () => {
    if (currentAd && !videoEnded) {
      setVideoEnded(true);
      completeAdWatch(currentAd);
    }
  };

  const closeVideoPlayer = () => {
    if (videoRef.current) {
      videoRef.current.pause();
      videoRef.current.src = '';
    }
    setVideoPlaying(false);
    setWatchingAd(null);
    setCurrentAd(null);
    setWatchProgress(0);
    setVideoEnded(false);
  };

  const completeAdWatch = async (ad: AdItem) => {
    try {
      const duration = videoRef.current ? Math.floor(videoRef.current.currentTime) : ad.min_watch_seconds + 1;
      const r = await fetch(`${API}/api/rewards/ads/watch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, ad_id: ad.id, watch_duration: duration }),
      });
      const d = await r.json();
      if (d.success) {
        toast.success(t('adComplete').replace('{n}', String(d.points_earned)));
        if (d.level_up) {
          toast.success(t('levelUp').replace('{n}', String(d.level.level)), { duration: 5000 });
        }
        setCanWatch(false);
        setCooldown(30);
        // Close video after short delay to show completion
        setTimeout(() => {
          closeVideoPlayer();
          loadProfile();
        }, 1500);
      } else {
        toast.error(d.message === 'cooldown_active' ? t('cooldownMsg').replace('{n}', '30') : t('dailyLimitMsg'));
        closeVideoPlayer();
      }
    } catch {
      toast.error(t('genericError'));
      closeVideoPlayer();
    }
  };

  const handlePurchase = async (item: StoreItem) => {
    if (!profile) return;
    if (profile.available_points < item.price) {
      toast.error(t('notEnoughPoints'));
      return;
    }
    if (profile.level.level < item.level_required) {
      toast.error(t('levelRequired').replace('{n}', String(item.level_required)));
      return;
    }
    try {
      const r = await fetch(`${API}/api/rewards/store/purchase`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, item_id: item.id }),
      });
      const d = await r.json();
      if (d.success) {
        toast.success(t('purchaseSuccess'));
        await loadProfile();
      } else if (d.message === 'already_owned') {
        toast.info(t('ownedBtn'));
      } else {
        toast.error(d.message === 'insufficient_points' ? t('notEnoughPoints') : t('levelRequired').replace('{n}', String(item.level_required)));
      }
    } catch { toast.error(t('genericError')); }
  };

  const handleEquip = async (itemId: string, category: string) => {
    try {
      const r = await fetch(`${API}/api/rewards/store/equip`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, item_id: itemId, slot: category }),
      });
      const d = await r.json();
      if (d.success) {
        toast.success(t('equipSuccess'));
        await loadProfile();
      }
    } catch { toast.error(t('genericError')); }
  };

  const handleUnequip = async (slot: string) => {
    try {
      await fetch(`${API}/api/rewards/store/unequip`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, slot }),
      });
      await loadProfile();
    } catch { }
  };

  const isOwned = (id: string) => profile?.inventory.includes(id) || false;
  const isEquipped = (id: string) => Object.values(profile?.equipped || {}).includes(id);
  const getItemsByCategory = (cat: string) => storeItems.filter(i => i.category === cat);

  const getRarityLabel = (r: string) => {
    const map: Record<string, string> = { common: t('rarityCommon'), rare: t('rarityRare'), epic: t('rarityEpic'), legendary: t('rarityLegendary') };
    return map[r] || r;
  };

  const getCategoryLabel = (c: string) => {
    const map: Record<string, string> = { border: t('storeBorders'), badge: t('storeBadges'), shape: t('storeShapes'), theme: t('storeThemes'), font: t('storeFonts') };
    return map[c] || c;
  };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin w-10 h-10 border-3 border-[#D4AF37] border-t-transparent rounded-full" />
    </div>
  );

  return (
    <div className="min-h-screen bg-background pb-24" dir={dir}>
      {/* Header */}
      <div className="sticky top-0 z-30 bg-background/80 backdrop-blur-xl border-b border-border/20">
        <div className="flex items-center gap-3 px-4 pt-3 pb-2">
          <button onClick={() => navigate(-1)} className="p-2 rounded-full bg-muted/30 hover:bg-muted/50 transition-all">
            {isRTL ? <ChevronRight className="w-5 h-5" /> : <ArrowLeft className="w-5 h-5" />}
          </button>
          <div className="flex-1">
            <h1 className="text-lg font-bold bg-gradient-to-r from-[#D4AF37] to-amber-500 bg-clip-text text-transparent">{t('storeTitle')}</h1>
            <p className="text-[10px] text-muted-foreground">{t('storeSubtitle')}</p>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#D4AF37]/10 border border-[#D4AF37]/20">
            <Coins className="w-4 h-4 text-[#D4AF37]" />
            <span className="text-sm font-bold text-[#D4AF37]">{profile?.available_points || 0}</span>
          </div>
        </div>

        {/* Level Bar */}
        {profile && (
          <div className="px-4 pb-2">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#D4AF37] to-amber-600 flex items-center justify-center">
                  <span className="text-xs font-black text-white">{profile.level.level}</span>
                </div>
                <span className="text-[10px] text-muted-foreground font-bold">{t('myLevel')}</span>
              </div>
              <div className="flex-1">
                <div className="h-2 bg-muted/40 rounded-full overflow-hidden">
                  <div className="h-full rounded-full bg-gradient-to-r from-[#D4AF37] to-amber-500 transition-all duration-500"
                    style={{ width: `${(profile.level.progress * 100)}%` }} />
                </div>
                <p className="text-[9px] text-muted-foreground mt-0.5 text-end">
                  {profile.level.xp} / {profile.level.next_level_xp} XP
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Tab Bar */}
        <div className="flex gap-1 px-4 pb-2">
          {(['store', 'inventory', 'earn'] as const).map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              className={cn(
                "flex-1 py-2 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1",
                activeTab === tab
                  ? 'bg-[#D4AF37]/15 text-[#D4AF37] border border-[#D4AF37]/30'
                  : 'bg-muted/20 text-muted-foreground'
              )}>
              {tab === 'store' && <ShoppingBag className="w-3.5 h-3.5" />}
              {tab === 'inventory' && <Star className="w-3.5 h-3.5" />}
              {tab === 'earn' && <Play className="w-3.5 h-3.5" />}
              {tab === 'store' ? t('storeTitle') : tab === 'inventory' ? t('profilePreview') : t('storeAds')}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="px-4 py-3 space-y-4">

        {/* ═══ STORE TAB ═══ */}
        {activeTab === 'store' && (
          <>
            {/* Category Selector */}
            <div className="flex gap-1.5 overflow-x-auto pb-1 scrollbar-hide">
              {CATEGORY_TABS.map(cat => (
                <button key={cat} onClick={() => setStoreCategory(cat)}
                  className={cn(
                    "px-3 py-1.5 rounded-full text-[11px] font-bold whitespace-nowrap transition-all",
                    storeCategory === cat
                      ? 'bg-[#D4AF37]/20 text-[#D4AF37] border border-[#D4AF37]/30'
                      : 'bg-muted/20 text-muted-foreground border border-transparent'
                  )}>
                  {getCategoryLabel(cat)}
                </button>
              ))}
            </div>

            {/* Items Grid */}
            <div className="grid grid-cols-2 gap-3">
              {getItemsByCategory(storeCategory).map(item => {
                const owned = isOwned(item.id) || item.price === 0;
                const equipped = isEquipped(item.id);
                const canBuy = profile && profile.available_points >= item.price && profile.level.level >= item.level_required;
                const levelLocked = profile && profile.level.level < item.level_required;

                return (
                  <div key={item.id}
                    className={cn(
                      "rounded-2xl border-2 p-3 transition-all relative overflow-hidden",
                      RARITY_COLORS[item.rarity] || RARITY_COLORS.common,
                      equipped && "ring-2 ring-[#D4AF37]/60"
                    )}>
                    {/* Rarity badge */}
                    <div className={cn("absolute top-1.5 end-1.5 text-[8px] font-bold px-1.5 py-0.5 rounded-full", RARITY_TEXT[item.rarity])}>
                      {getRarityLabel(item.rarity)}
                    </div>

                    {/* Preview */}
                    <div className="flex flex-col items-center mb-2 pt-2">
                      <div className="w-14 h-14 rounded-2xl flex items-center justify-center text-3xl"
                        style={{ background: item.preview_color + '20', border: `2px solid ${item.preview_color}40` }}>
                        {item.emoji}
                      </div>
                      <p className="text-xs font-bold mt-2 text-center line-clamp-1">{isRTL ? item.name_ar : item.name_en}</p>
                    </div>

                    {/* Level requirement */}
                    {levelLocked && (
                      <div className="flex items-center justify-center gap-1 text-[9px] text-orange-400 mb-1">
                        <Lock className="w-3 h-3" /> {t('levelRequired').replace('{n}', String(item.level_required))}
                      </div>
                    )}

                    {/* Action Button */}
                    {equipped ? (
                      <button onClick={() => handleUnequip(item.category)}
                        className="w-full py-1.5 rounded-xl bg-[#D4AF37]/20 text-[#D4AF37] text-[11px] font-bold border border-[#D4AF37]/30">
                        {t('equippedBtn')} ✓
                      </button>
                    ) : owned ? (
                      <button onClick={() => handleEquip(item.id, item.category)}
                        className="w-full py-1.5 rounded-xl bg-emerald-500/15 text-emerald-400 text-[11px] font-bold border border-emerald-400/30">
                        {t('equipBtn')}
                      </button>
                    ) : (
                      <button onClick={() => handlePurchase(item)} disabled={!canBuy || !!levelLocked}
                        className={cn(
                          "w-full py-1.5 rounded-xl text-[11px] font-bold flex items-center justify-center gap-1 transition-all",
                          canBuy && !levelLocked
                            ? "bg-[#D4AF37]/15 text-[#D4AF37] border border-[#D4AF37]/30 active:scale-95"
                            : "bg-muted/20 text-muted-foreground border border-border/20 opacity-60"
                        )}>
                        <Coins className="w-3 h-3" />
                        {item.price} {t('buyBtn')}
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </>
        )}

        {/* ═══ INVENTORY TAB ═══ */}
        {activeTab === 'inventory' && profile && (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-3 gap-2">
              <div className="rounded-xl bg-[#D4AF37]/10 border border-[#D4AF37]/20 p-3 text-center">
                <Trophy className="w-5 h-5 mx-auto text-[#D4AF37] mb-1" />
                <p className="text-lg font-black text-[#D4AF37]">{profile.level.level}</p>
                <p className="text-[9px] text-muted-foreground">{t('myLevel')}</p>
              </div>
              <div className="rounded-xl bg-emerald-500/10 border border-emerald-400/20 p-3 text-center">
                <Coins className="w-5 h-5 mx-auto text-emerald-400 mb-1" />
                <p className="text-lg font-black text-emerald-400">{profile.available_points}</p>
                <p className="text-[9px] text-muted-foreground">{t('availablePoints')}</p>
              </div>
              <div className="rounded-xl bg-blue-500/10 border border-blue-400/20 p-3 text-center">
                <Eye className="w-5 h-5 mx-auto text-blue-400 mb-1" />
                <p className="text-lg font-black text-blue-400">{profile.ads_watched}</p>
                <p className="text-[9px] text-muted-foreground">{t('adsWatched')}</p>
              </div>
            </div>

            {/* Equipped Items */}
            <div className="space-y-2">
              <h3 className="text-sm font-bold">{t('profilePreview')}</h3>
              <div className="rounded-2xl bg-card/40 border border-border/20 p-4 space-y-3">
                {CATEGORY_TABS.map(slot => {
                  const equippedId = profile.equipped[slot];
                  const item = storeItems.find(i => i.id === equippedId);
                  return (
                    <div key={slot} className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-xl flex items-center justify-center text-lg"
                        style={{ background: item ? item.preview_color + '15' : '#6B728015' }}>
                        {item ? item.emoji : '—'}
                      </div>
                      <div className="flex-1">
                        <p className="text-xs font-bold">{getCategoryLabel(slot)}</p>
                        <p className="text-[10px] text-muted-foreground">
                          {item ? (isRTL ? item.name_ar : item.name_en) : '—'}
                        </p>
                      </div>
                      {item && (
                        <button onClick={() => handleUnequip(slot)}
                          className="text-[10px] text-red-400 px-2 py-1 rounded-lg bg-red-500/10 border border-red-400/20">
                          {t('unequipBtn')}
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Owned Items */}
            <div className="space-y-2">
              <h3 className="text-sm font-bold">{t('ownedBtn')} ({profile.inventory.length})</h3>
              <div className="grid grid-cols-4 gap-2">
                {profile.inventory.map(itemId => {
                  const item = storeItems.find(i => i.id === itemId);
                  if (!item) return null;
                  const equipped = isEquipped(itemId);
                  return (
                    <button key={itemId} onClick={() => equipped ? handleUnequip(item.category) : handleEquip(itemId, item.category)}
                      className={cn(
                        "rounded-xl p-2 text-center border transition-all",
                        equipped ? "border-[#D4AF37]/40 bg-[#D4AF37]/10" : "border-border/20 bg-muted/10"
                      )}>
                      <span className="text-2xl block">{item.emoji}</span>
                      <p className="text-[8px] text-muted-foreground mt-1 line-clamp-1">{isRTL ? item.name_ar : item.name_en}</p>
                      {equipped && <CheckCircle className="w-3 h-3 text-[#D4AF37] mx-auto mt-0.5" />}
                    </button>
                  );
                })}
              </div>
            </div>
          </>
        )}

        {/* ═══ EARN POINTS TAB ═══ */}
        {activeTab === 'earn' && (
          <>
            {/* FULL SCREEN VIDEO PLAYER OVERLAY */}
            {videoPlaying && currentAd && (
              <div className="fixed inset-0 z-[100] bg-black flex flex-col">
                {/* Video */}
                <div className="flex-1 relative flex items-center justify-center">
                  <video
                    ref={videoRef}
                    src={currentAd.video_url}
                    autoPlay
                    playsInline
                    onTimeUpdate={onVideoTimeUpdate}
                    onEnded={onVideoEnded}
                    className="w-full h-full object-contain"
                    controlsList="nodownload nofullscreen noremoteplayback"
                  />
                  {/* Close button - only after min watch time */}
                  {videoEnded && (
                    <button onClick={closeVideoPlayer}
                      className="absolute top-4 end-4 w-10 h-10 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center text-white text-xl z-10">
                      ✕
                    </button>
                  )}
                </div>

                {/* Progress bar at bottom */}
                <div className="px-4 py-3 bg-black/90">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs text-white/60">
                      {videoEnded ? t('adComplete').replace('{n}', String(currentAd.points_reward)) : t('watchingAd')}
                    </span>
                    <span className="text-xs text-[#D4AF37] font-bold">+{currentAd.points_reward} {t('pointsPerAd').replace('{n} ', '')}</span>
                  </div>
                  <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <div className={cn("h-full rounded-full transition-all", videoEnded ? "bg-emerald-500" : "bg-[#D4AF37]")}
                      style={{ width: `${watchProgress * 100}%` }} />
                  </div>
                  {!videoEnded && (
                    <p className="text-[10px] text-white/40 text-center mt-1">
                      {Math.round(watchProgress * 100)}% — {t('watchingAd')}
                    </p>
                  )}
                </div>
              </div>
            )}

            <div className="rounded-2xl bg-gradient-to-br from-[#D4AF37]/10 to-amber-600/5 border border-[#D4AF37]/20 p-4 text-center">
              <Sparkles className="w-8 h-8 mx-auto text-[#D4AF37] mb-2" />
              <h3 className="text-base font-bold">{t('earnPointsTitle')}</h3>
              <p className="text-xs text-muted-foreground mt-1">{t('earnPointsDesc')}</p>
            </div>

            {/* Ad Cards */}
            {ads.length === 0 ? (
              <div className="text-center py-8">
                <Play className="w-10 h-10 mx-auto text-muted-foreground/30 mb-3" />
                <p className="text-muted-foreground text-sm">{t('noAdsAvailable')}</p>
                <p className="text-xs text-muted-foreground/60 mt-1">
                  {t('noAdsAvailable')}
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {ads.map(ad => {
                  const isWatching = watchingAd === ad.id;
                  return (
                    <div key={ad.id}
                      className={cn(
                        "rounded-2xl border overflow-hidden transition-all",
                        isWatching ? "border-[#D4AF37]/40 bg-[#D4AF37]/5" : "border-border/20 bg-card/40"
                      )}>
                      {/* Ad thumbnail / video preview */}
                      {ad.thumbnail_url && (
                        <div className="relative h-32 bg-black/20 overflow-hidden">
                          <img src={ad.thumbnail_url} alt={ad.title} className="w-full h-full object-cover" />
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                              <Play className="w-6 h-6 text-white" fill="white" />
                            </div>
                          </div>
                        </div>
                      )}

                      <div className="p-4">
                        <div className="flex items-center gap-3">
                          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500/20 to-blue-500/20 flex items-center justify-center flex-shrink-0">
                            <Play className="w-5 h-5 text-emerald-400" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-bold truncate">{ad.title}</p>
                            <p className="text-[10px] text-muted-foreground">
                              ⏱ {ad.min_watch_seconds}s
                            </p>
                          </div>
                          <div className="flex items-center gap-1 px-2.5 py-1.5 rounded-full bg-[#D4AF37]/10 border border-[#D4AF37]/20 flex-shrink-0">
                            <Coins className="w-3.5 h-3.5 text-[#D4AF37]" />
                            <span className="text-xs font-bold text-[#D4AF37]">+{ad.points_reward}</span>
                          </div>
                        </div>

                        {/* Watch button */}
                        <button onClick={() => handleWatchAd(ad)}
                          disabled={!canWatch || !!watchingAd}
                          className={cn(
                            "w-full mt-3 py-2.5 rounded-xl text-sm font-bold flex items-center justify-center gap-2 transition-all active:scale-95",
                            canWatch && !watchingAd
                              ? "bg-emerald-500/15 text-emerald-400 border border-emerald-400/30 hover:bg-emerald-500/25"
                              : "bg-muted/20 text-muted-foreground border border-border/20 opacity-50 cursor-not-allowed"
                          )}>
                          {canWatch ? (
                            <><Play className="w-4 h-4" /> {t('watchAdBtn')}</>
                          ) : cooldown > 0 ? (
                            <>{t('cooldownMsg').replace('{n}', String(cooldown))}</>
                          ) : (
                            <>{t('dailyLimitMsg')}</>
                          )}
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Level Progress */}
            {profile && (
              <div className="rounded-2xl bg-card/40 border border-border/20 p-4 space-y-3">
                <div className="flex items-center gap-3">
                  <TrendingUp className="w-5 h-5 text-[#D4AF37]" />
                  <h3 className="text-sm font-bold">{t('myLevel')}: {profile.level.level}</h3>
                </div>
                <div className="h-3 bg-muted/40 rounded-full overflow-hidden">
                  <div className="h-full rounded-full bg-gradient-to-r from-[#D4AF37] to-amber-500 transition-all duration-500"
                    style={{ width: `${profile.level.progress * 100}%` }} />
                </div>
                <div className="flex justify-between text-[10px] text-muted-foreground">
                  <span>{profile.level.xp} XP</span>
                  <span>{profile.level.xp_needed} XP {t('levelRequired').replace(t('levelRequired').split('{n}')[0], '').replace('{n}', String(profile.level.level + 1))}</span>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
