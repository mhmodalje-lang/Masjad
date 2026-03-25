import { useState, useEffect, useRef, useCallback, memo } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { useAuth } from '@/hooks/useAuth';
import { useAdmin } from '@/hooks/useAdmin';
import { useNavigate } from 'react-router-dom';
import {
  Users, Bell, Settings, BarChart3, Shield, Send, Trash2, Plus,
  ChevronLeft, ChevronRight, RefreshCw, Megaphone, AlertTriangle,
  Monitor, FileText, Clock, BookOpen, Check, X, Eye, EyeOff,
  Coins, ShoppingBag, Film, CreditCard, Building2, Store,
  Heart, MessageSquare, Sparkles, Volume2
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';
function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders() { return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getToken()}` }; }

const AD_PROVIDERS = [
  'Google AdSense', 'Google AdMob', 'ExoClick', 'PopAds', 'Clickadu',
  'HilltopAds', 'Monetag', 'Adsterra', 'ySense', 'YouTube', 'Custom'
];
const AD_PLACEMENTS = ['home','prayer','quran','duas','ruqyah','notifications','all'];
const AD_TYPES = ['banner','interstitial','native','video','popup'];

export default function AdminDashboard() {
  const { t, dir } = useLocale();
  const { user } = useAuth();
  const { isAdmin, loading: adminLoading } = useAdmin();
  const navigate = useNavigate();
  const [tab, setTab] = useState('overview');
  const [stats, setStats] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [usersTotal, setUsersTotal] = useState(0);
  const [usersPage, setUsersPage] = useState(1);
  const [ads, setAds] = useState<any[]>([]);
  const [pages, setPages] = useState<any[]>([]);
  const [scheduledNotifs, setScheduledNotifs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  // Settings
  const [announcement, setAnnouncement] = useState('');
  const [maintenance, setMaintenance] = useState(false);
  // Notification form
  const [nTitle, setNTitle] = useState('');
  const [nBody, setNBody] = useState('');
  // Ad form
  const [showAdForm, setShowAdForm] = useState(false);
  const [adForm, setAdForm] = useState({ name:'', provider:'Google AdSense', code:'', placement:'home', ad_type:'banner', enabled:true, priority:0 });
  // Page form
  const [showPageForm, setShowPageForm] = useState(false);
  const [pageForm, setPageForm] = useState({ title:'', category:'', content:'', enabled:true, order:0 });
  // Scheduled notif form
  const [showNotifForm, setShowNotifForm] = useState(false);
  const [notifForm, setNotifForm] = useState({ title:'', body:'', schedule_time:'', repeat:'once', enabled:true });
  // User Ads
  const [userAds, setUserAds] = useState<any[]>([]);
  // Bank
  const [bankForm, setBankForm] = useState({ bank_name:'', account_holder:'', iban:'', swift:'' });
  const [adminRevenue, setAdminRevenue] = useState<any>(null);
  // Marketplace
  const [commissionRate, setCommissionRate] = useState(10);
  // Announcements (Broadcast)
  const [broadcastTitle, setBroadcastTitle] = useState('');
  const [broadcastBody, setBroadcastBody] = useState('');
  const [broadcastType, setBroadcastType] = useState('info');
  const [broadcastList, setBroadcastList] = useState<any[]>([]);
  // Vendors
  const [vendors, setVendors] = useState<any[]>([]);
  // Embed Content
  const [embedContent, setEmbedContent] = useState<any[]>([]);
  const [showEmbedForm, setShowEmbedForm] = useState(false);
  const [embedForm, setEmbedForm] = useState({ title:'', description:'', embed_url:'', platform:'youtube', category:'general', thumbnail_url:'' });
  // Stories Management
  const [adminStories, setAdminStories] = useState<any[]>([]);
  const [storiesFilter, setStoriesFilter] = useState('');
  const [storiesTotal, setStoriesTotal] = useState(0);
  // Ruqyah Management
  const [ruqyahItems, setRuqyahItems] = useState<any[]>([]);
  const [showRuqyahForm, setShowRuqyahForm] = useState(false);
  const [ruqyahForm, setRuqyahForm] = useState({ title:'', content:'', category:'general', audio_url:'', video_url:'', order:0, enabled:true });
  // Donations Management
  const [adminDonations, setAdminDonations] = useState<any[]>([]);
  const [donationsFilter, setDonationsFilter] = useState('');
  const [donationsTotal, setDonationsTotal] = useState(0);
  const [donationsTotalAmount, setDonationsTotalAmount] = useState(0);
  // Ad Settings
  const [adSettings, setAdSettings] = useState({
    ads_enabled: true, video_ads_muted: true, gdpr_consent_required: true,
    ad_banner_enabled: true, ad_interstitial_enabled: false, ad_rewarded_enabled: true,
    admob_app_id: '', adsense_publisher_id: ''
  });
  // Analytics
  const [analyticsData, setAnalyticsData] = useState<any>(null);
  // Social Management
  const [socialPosts, setSocialPosts] = useState<any[]>([]);
  const [socialComments, setSocialComments] = useState<any[]>([]);
  const [socialStats, setSocialStats] = useState<any>(null);
  const [socialUsers, setSocialUsers] = useState<any[]>([]);
  // Ad Page Rules (God-Mode)
  const [adRules, setAdRules] = useState<any[]>([]);
  // Daily Content Management
  const [dailyContentItems, setDailyContentItems] = useState<any[]>([]);
  const [showDailyForm, setShowDailyForm] = useState(false);
  const [dailyForm, setDailyForm] = useState<any>({ content_type:'hadith', title:{}, body:{}, source:{}, arabic_text:'', active:true, schedule_date:'', priority:0 });
  const [dailyEditLang, setDailyEditLang] = useState('ar');
  // Multilingual Notification
  const [mlNotifTitle, setMlNotifTitle] = useState<Record<string,string>>({});
  const [mlNotifBody, setMlNotifBody] = useState<Record<string,string>>({});
  const [mlNotifTarget, setMlNotifTarget] = useState('all');
  const [mlNotifHistory, setMlNotifHistory] = useState<any[]>([]);
  const SUPPORTED_LOCALES = ['ar','en','de','fr','tr','ru','sv','nl','el','de-AT'];
  const ALL_PAGES = ['home','prayer','quran','duas','ruqyah','kids_zone','arabic_academy','stories','explore','live_streams','tasbeeh','qibla','notifications','profile'];

  useEffect(() => { if (!adminLoading && !isAdmin && !user) navigate('/auth'); }, [isAdmin, adminLoading, user]);
  useEffect(() => { if (isAdmin) { fetchStats(); fetchSettings(); fetchAds(); fetchPages(); fetchNotifs(); fetchUserAds(); fetchBankInfo(); fetchBroadcasts(); fetchVendors(); fetchEmbedContent(); fetchRuqyah(); } }, [isAdmin]);
  useEffect(() => { if (isAdmin && tab === 'users') fetchUsers(usersPage); }, [isAdmin, tab, usersPage]);
  useEffect(() => { if (isAdmin && tab === 'stories-mgmt') fetchAdminStories(); }, [isAdmin, tab, storiesFilter]);
  useEffect(() => { if (isAdmin && tab === 'social-mgmt') { fetchSocialStats(); fetchSocialPosts(); fetchSocialComments(); fetchSocialUsers(); } }, [isAdmin, tab]);
  useEffect(() => { if (isAdmin && tab === 'donations-mgmt') fetchAdminDonations(); }, [isAdmin, tab, donationsFilter]);
  useEffect(() => { if (isAdmin && tab === 'ad-rules') fetchAdRules(); }, [isAdmin, tab]);
  useEffect(() => { if (isAdmin && tab === 'daily-content') fetchDailyContent(); }, [isAdmin, tab]);
  useEffect(() => { if (isAdmin && tab === 'multilingual-notif') fetchMlNotifHistory(); }, [isAdmin, tab]);

  const api = async (path: string, method='GET', body?: any, useAuth=true) => {
    const opts: any = { method, headers: useAuth ? authHeaders() : {'Content-Type':'application/json'} };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${BACKEND_URL}/api${path}`, opts);
    return res.json();
  };

  async function fetchStats() { 
    setLoading(true); 
    try { 
      const d = await api('/admin/stats'); 
      // Merge stats from both endpoints
      const newStats = d.stats || d;
      setStats(newStats); 
    } catch {} 
    setLoading(false); 
  }
  async function fetchUsers(p: number) { try { const d = await api(`/admin/users?page=${p}`); setUsers(d.users||[]); setUsersTotal(d.total||0); } catch {} }
  async function fetchSettings() { 
    try { 
      const d = await api('/admin/settings'); 
      setAnnouncement(d.announcement||''); 
      setMaintenance(d.maintenance_mode||false);
      setAdSettings({
        ads_enabled: d.ads_enabled ?? true,
        video_ads_muted: d.video_ads_muted ?? true,
        gdpr_consent_required: d.gdpr_consent_required ?? true,
        ad_banner_enabled: d.ad_banner_enabled ?? true,
        ad_interstitial_enabled: d.ad_interstitial_enabled ?? false,
        ad_rewarded_enabled: d.ad_rewarded_enabled ?? true,
        admob_app_id: d.admob_app_id || '',
        adsense_publisher_id: d.adsense_publisher_id || '',
      });
    } catch {} 
  }
  async function fetchAds() { try { const d = await api('/admin/ads'); setAds(d.ads||[]); } catch {} }
  async function fetchPages() { try { const d = await api('/admin/pages'); setPages(d.pages||[]); } catch {} }
  async function fetchNotifs() { try { const d = await api('/admin/scheduled-notifications'); setScheduledNotifs(d.notifications||[]); } catch {} }
  async function fetchUserAds() { try { const d = await api('/admin/user-ads'); setUserAds(d.ads||[]); } catch {} }
  async function fetchBankInfo() { try { const d = await api('/admin/bank-account'); setBankForm(d.account||{}); setAdminRevenue(d.revenue); } catch {} }
  async function fetchBroadcasts() { try { const d = await api('/announcements', 'GET', null, false); setBroadcastList(d.announcements||[]); } catch {} }
  async function fetchVendors() { try { const d = await api('/admin/vendors'); setVendors(d.vendors||[]); } catch {} }
  async function fetchEmbedContent() { try { const d = await api('/admin/embed-content'); setEmbedContent(d.content||[]); } catch {} }
  function extractYouTubeID(url: string): string | null {
    const match = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]+)/);
    return match ? match[1] : null;
  }
  function buildEmbedUrl(url: string, platform: string): string {
    if (platform === 'youtube') {
      const vid = extractYouTubeID(url);
      if (vid) return `https://www.youtube.com/embed/${vid}`;
    }
    if (platform === 'dailymotion') {
      const match = url.match(/dailymotion\.com\/video\/([\w]+)/);
      if (match) return `https://www.dailymotion.com/embed/video/${match[1]}`;
    }
    if (platform === 'vimeo') {
      const match = url.match(/vimeo\.com\/(\d+)/);
      if (match) return `https://player.vimeo.com/video/${match[1]}`;
    }
    return url;
  }
  async function saveEmbedContent() {
    if (!embedForm.title.trim() || !embedForm.embed_url.trim()) { toast.error(t('titleAndLinkRequired')); return; }
    const processedUrl = buildEmbedUrl(embedForm.embed_url, embedForm.platform);
    let thumbnailUrl = embedForm.thumbnail_url;
    if (!thumbnailUrl && embedForm.platform === 'youtube') {
      const vid = extractYouTubeID(embedForm.embed_url);
      if (vid) thumbnailUrl = `https://img.youtube.com/vi/${vid}/hqdefault.jpg`;
    }
    const d = await api('/admin/embed-content','POST',{...embedForm, embed_url: processedUrl, thumbnail_url: thumbnailUrl || undefined});
    if (d.success) { toast.success(t('embedSavedSuccess')); setShowEmbedForm(false); setEmbedForm({title:'',description:'',embed_url:'',platform:'youtube',category:'general',thumbnail_url:''}); fetchEmbedContent(); }
  }
  async function deleteEmbedContent(id: string) { if(!confirm(t('confirmDelete'))) return; await api(`/admin/embed-content/${id}`,'DELETE'); toast.success(t('savedSuccess')); fetchEmbedContent(); }

  async function deleteUser(id: string) { if(!confirm(t('confirmDelete'))) return; await api(`/admin/users/${id}`,'DELETE'); toast.success(t('savedSuccess')); fetchUsers(usersPage); fetchStats(); }
  async function sendNotif() { if(!nTitle||!nBody) return toast.error(t('fillFields')); const d = await api('/admin/send-notification','POST',{title:nTitle,body:nBody}); if(d.success) { toast.success(d.message); setNTitle(''); setNBody(''); } }
  async function saveSettings() { const d = await api('/admin/settings','PUT',{announcement,maintenance_mode:maintenance}); if(d.success) toast.success(t('savedSuccess')); }
  async function saveAdSettings() { 
    const d = await api('/admin/settings','PUT', adSettings); 
    if(d.success) toast.success(t('adSettingsSavedSuccess')); 
  }
  async function fetchAnalytics() {
    try { const d = await api('/admin/analytics/summary?days=7'); setAnalyticsData(d); } catch {}
  }
  async function fetchSocialStats() { try { const d = await api('/admin/social/stats'); setSocialStats(d); } catch {} }
  async function fetchSocialPosts() { try { const d = await api('/admin/social/posts?limit=30'); setSocialPosts(d.posts || []); } catch {} }
  async function fetchSocialComments() { try { const d = await api('/admin/social/comments?limit=50'); setSocialComments(d.comments || []); } catch {} }
  async function fetchSocialUsers() { try { const d = await api('/admin/social/users?limit=50'); setSocialUsers(d.users || []); } catch {} }
  async function deleteSocialPost(id: string) { if (!confirm(t('confirmDeletePost'))) return; await api(`/admin/social/posts/${id}`, 'DELETE'); toast.success(t('deletedSuccess')); fetchSocialPosts(); fetchSocialStats(); }
  async function deleteSocialComment(id: string) { if (!confirm(t('confirmDeleteComment'))) return; await api(`/admin/social/comments/${id}`, 'DELETE'); toast.success(t('deletedSuccess')); fetchSocialComments(); }
  async function saveAd() { const d = await api('/admin/ads','POST',adForm); if(d.success) { toast.success(t('adSavedSuccess')); setShowAdForm(false); fetchAds(); } }
  async function deleteAd(id: string) { await api(`/admin/ads/${id}`,'DELETE'); toast.success(t('deletedSuccess')); fetchAds(); }
  async function savePage() { const d = await api('/admin/pages','POST',pageForm); if(d.success) { toast.success(t('pageSavedSuccess')); setShowPageForm(false); fetchPages(); } }
  async function deletePage(id: string) { await api(`/admin/pages/${id}`,'DELETE'); toast.success(t('savedSuccess')); fetchPages(); }
  async function saveSchedNotif() { const d = await api('/admin/scheduled-notifications','POST',notifForm); if(d.success) { toast.success(t('savedSuccess')); setShowNotifForm(false); fetchNotifs(); } }
  async function deleteSchedNotif(id: string) { await api(`/admin/scheduled-notifications/${id}`,'DELETE'); toast.success(t('savedSuccess')); fetchNotifs(); }
  async function updateAdStatus(id: string, status: string) { await api(`/admin/user-ads/${id}`,'PUT',{status}); toast.success(t('statusUpdated')); fetchUserAds(); }
  async function saveBankInfo() { await api('/admin/bank-account','POST',bankForm); toast.success(t('bankSavedSuccess')); }
  async function saveCommission() { await api('/admin/marketplace/commission','PUT',{commission_rate:commissionRate}); toast.success(t('savedSuccess')); }
  async function publishBroadcast() {
    if (!broadcastTitle.trim() || !broadcastBody.trim()) { toast.error(t('fillTitleAndBody')); return; }
    await api('/admin/announcements','POST',{title:broadcastTitle,body:broadcastBody,type:broadcastType});
    toast.success(t('publishedSuccess'));
    setBroadcastTitle(''); setBroadcastBody(''); fetchBroadcasts();
  }
  async function deleteBroadcast(id: string) { await api(`/admin/announcements/${id}`,'DELETE'); toast.success(t('savedSuccess')); fetchBroadcasts(); }
  async function updateVendorStatus(id: string, status: string) { await api(`/admin/vendors/${id}`,'PUT',{status}); toast.success(t('savedSuccess')); fetchVendors(); }
  // Stories management
  async function fetchAdminStories() { try { const d = await api(`/admin/all-stories?status=${storiesFilter}`); setAdminStories(d.stories||[]); setStoriesTotal(d.total||0); } catch {} }
  async function moderateStory(id: string, action: string) { await api(`/admin/stories/${id}`,'PUT',{action}); toast.success(action === 'approve' ? t('approved') : t('rejected')); fetchAdminStories(); }
  async function deleteStory(id: string) { if(!confirm(t('confirmDeleteStory'))) return; await api(`/admin/stories/${id}`,'DELETE'); toast.success(t('deletedSuccess')); fetchAdminStories(); }
  // Ruqyah management
  async function fetchRuqyah() { try { const d = await api('/admin/ruqyah'); setRuqyahItems(d.items||[]); } catch {} }
  async function saveRuqyah() { if(!ruqyahForm.title.trim()) { toast.error(t('titleRequired')); return; } const d = await api('/admin/ruqyah','POST',ruqyahForm); if(d.success) { toast.success(t('savedSuccess')); setShowRuqyahForm(false); setRuqyahForm({title:'',content:'',category:'general',audio_url:'',video_url:'',order:0,enabled:true}); fetchRuqyah(); } }
  async function deleteRuqyah(id: string) { if(!confirm(t('confirmDelete'))) return; await api(`/admin/ruqyah/${id}`,'DELETE'); toast.success(t('savedSuccess')); fetchRuqyah(); }
  // Donations management
  async function fetchAdminDonations() { try { const d = await api(`/admin/donations?status=${donationsFilter}`); setAdminDonations(d.donations||[]); setDonationsTotal(d.total||0); setDonationsTotalAmount(d.total_amount||0); } catch {} }
  async function moderateDonation(id: string, action: string) { await api(`/admin/donations/${id}`,'PUT',{action}); toast.success(action === 'approve' ? t('approved') : t('rejected')); fetchAdminDonations(); }
  async function deleteDonation(id: string) { if(!confirm(t('confirmDelete'))) return; await api(`/admin/donations/${id}`,'DELETE'); toast.success(t('savedSuccess')); fetchAdminDonations(); }

  // ===== GOD-MODE: Ad Rules per Page/Country =====
  async function fetchAdRules() { try { const d = await api('/admin/ads/rules'); setAdRules(d.rules||[]); } catch {} }
  async function saveAdRules() {
    try { await api('/admin/ads/rules','PUT', adRules); toast.success('Ad rules saved!'); } catch { toast.error('Failed to save'); }
  }
  function toggleAdRule(page: string, field: string, value: any) {
    setAdRules(prev => prev.map(r => r.page === page ? { ...r, [field]: value } : r));
  }

  // ===== GOD-MODE: Daily Content CRUD =====
  async function fetchDailyContent() { try { const d = await api('/admin/daily-content'); setDailyContentItems(d.items||[]); } catch {} }
  async function saveDailyContent() {
    try { await api('/admin/daily-content','POST', dailyForm); toast.success('Content saved!'); setShowDailyForm(false); fetchDailyContent(); } catch { toast.error('Failed'); }
  }
  async function deleteDailyContent(id: string) { if(!confirm('Delete?')) return; await api(`/admin/daily-content/${id}`,'DELETE'); toast.success('Deleted'); fetchDailyContent(); }

  // ===== GOD-MODE: Multilingual Push Notifications =====
  async function fetchMlNotifHistory() { try { const d = await api('/admin/notifications/history'); setMlNotifHistory(d.notifications||[]); } catch {} }
  async function sendMlNotification() {
    if (!mlNotifTitle.ar && !mlNotifTitle.en) { toast.error('Title needed in at least Arabic or English'); return; }
    try {
      const d = await api('/admin/notifications/send-multilingual','POST',{ title: mlNotifTitle, body: mlNotifBody, target: mlNotifTarget });
      toast.success(`Sent to ${d.total_sent} subscribers!`);
      setMlNotifTitle({}); setMlNotifBody({});
      fetchMlNotifHistory();
    } catch { toast.error('Failed to send'); }
  }

  if (adminLoading) return <div className="min-h-screen flex items-center justify-center"><RefreshCw className="h-8 w-8 animate-spin text-primary" /></div>;
  if (!isAdmin) return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4 px-5" dir={dir}>
      <Shield className="h-16 w-16 text-primary/30" />
      <h1 className="text-xl font-bold text-foreground">{t('adminPanel')}</h1>
      <p className="text-sm text-muted-foreground text-center">{user ? t('notAdminAccount') : t('loginFirst')}</p>
      <button onClick={() => navigate(user ? '/' : '/auth')} className="rounded-xl bg-primary text-primary-foreground px-6 py-3 text-sm font-bold">{user ? t('home') : t('loginLabel')}</button>
    </div>
  );

  const tabs = [
    { key:'overview', label:t('overview'), icon:BarChart3 },
    { key:'social-mgmt', label:t('socialManagement'), icon:MessageSquare },
    { key:'stories-mgmt', label:t('storiesManagement'), icon:BookOpen },
    { key:'ruqyah-mgmt', label:t('ruqyahManagement'), icon:Volume2 },
    { key:'donations-mgmt', label:t('donationsManagement'), icon:Heart },
    { key:'embed', label:t('embedContent'), icon:Film },
    { key:'broadcast', label:t('broadcast'), icon:Megaphone },
    { key:'users', label:t('usersManagement'), icon:Users },
    { key:'ads', label:t('adsManagement'), icon:Monitor },
    { key:'user-ads', label:t('userAdsManagement'), icon:Film },
    { key:'vendors', label:t('vendorRole'), icon:ShoppingBag },
    { key:'notifications', label:t('scheduledNotifications'), icon:Bell },
    { key:'multilingual-notif', label:'Multilingual Push', icon:Send },
    { key:'ad-rules', label:'Ad Rules (God-Mode)', icon:Shield },
    { key:'daily-content', label:'Daily Content', icon:Sparkles },
    { key:'pages', label:t('pagesManagement'), icon:FileText },
    { key:'revenue', label:t('commissionRate'), icon:CreditCard },
    { key:'settings', label:t('settingsLabel'), icon:Settings },
  ];

  const InputField = memo(({ label, value, onChange, placeholder, multiline=false }: any) => {
    const ref = useRef<any>(null);
    useEffect(() => {
      if (ref.current && ref.current !== document.activeElement) {
        ref.current.value = value || '';
      }
    }, [value]);
    const handleBlur = () => { if (ref.current) onChange(ref.current.value); };
    const handleKeyDown = (e: any) => { if (e.key === 'Enter' && !multiline) handleBlur(); };
    const sharedProps = {
      ref, dir: 'auto' as const, defaultValue: value || '', onBlur: handleBlur, onKeyDown: handleKeyDown,
      placeholder, autoComplete: 'off', spellCheck: false,
      style: { unicodeBidi: 'plaintext', textAlign: 'right' as const },
    };
    return (
      <div>
        <label className="text-xs font-medium text-foreground mb-1 block">{label}</label>
        {multiline ? (
          <textarea {...sharedProps} rows={3}
            className="w-full rounded-xl bg-muted border border-border/10 px-3 py-2 text-sm text-foreground resize-none focus:border-primary/50 focus:ring-1 focus:ring-primary/30 outline-none transition-all" />
        ) : (
          <input type="text" {...sharedProps}
            className="w-full rounded-xl bg-muted border border-border/10 px-3 py-2 text-sm text-foreground focus:border-primary/50 focus:ring-1 focus:ring-primary/30 outline-none transition-all" />
        )}
      </div>
    );
  });

  const SelectField = ({ label, value, onChange, options }: any) => (
    <div>
      <label className="text-xs font-medium text-foreground mb-1 block">{label}</label>
      <select dir="auto" value={value} onChange={e=>onChange(e.target.value)} className="w-full rounded-xl bg-muted border border-border/10 px-3 py-2 text-sm text-foreground text-right" style={{ unicodeBidi: 'plaintext' }}>
        {options.map((o:string)=><option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  );

  return (
    <div className="min-h-screen pb-28" dir={dir} data-testid="admin-dashboard">
      <div className="bg-gradient-to-b from-primary/20 to-transparent px-5 pt-7 pb-5">
        <div className="flex items-center gap-3 mb-4">
          <div className="h-12 w-12 rounded-xl bg-primary/15 flex items-center justify-center"><Shield className="h-6 w-6 text-primary" /></div>
          <div><h1 className="text-xl font-bold text-foreground">{t('adminPanel')}</h1><p className="text-xs text-muted-foreground">{user?.email}</p></div>
        </div>
        <div dir="ltr" className="w-full overflow-x-auto scrollbar-hide pb-1" style={{ WebkitOverflowScrolling: 'touch' }}>
          <div className="flex gap-2" style={{ direction: 'rtl', minWidth: 'max-content' }}>
            {tabs.map(t=>(
              <button key={t.key} onClick={()=>setTab(t.key)} data-testid={`admin-tab-${t.key}`}
                className={cn('inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all shrink-0',
                  tab===t.key ? 'bg-primary text-primary-foreground shadow-lg' : 'neu-card text-muted-foreground hover:bg-muted')}
                style={{ whiteSpace: 'nowrap' }}>
                <t.icon className="h-4 w-4 shrink-0" /><span style={{ whiteSpace: 'nowrap' }}>{t.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="px-5 mt-4">
        {/* ===== OVERVIEW ===== */}
        {tab==='overview' && (
          <div className="space-y-4">
            <div className="grid grid-cols-3 gap-3">
              {[{l:t('totalUsers'),v:stats?.total_users??0,i:Users,c:'text-blue-500 bg-blue-500/10'},{l:t('scheduledNotifications'),v:stats?.push_subscribers??0,i:Bell,c:'text-green-500 bg-green-500/10'},{l:t('totalAds'),v:ads.length,i:Monitor,c:'text-amber-500 bg-amber-500/10'}]
              .map(s=>(
                <div key={s.l} className="rounded-2xl neu-card p-4 text-center">
                  <div className={cn("h-10 w-10 rounded-xl flex items-center justify-center mx-auto mb-2",s.c)}><s.i className="h-5 w-5"/></div>
                  <p className="text-2xl font-bold text-foreground">{s.v}</p>
                  <p className="text-xs text-muted-foreground mt-1">{s.l}</p>
                </div>
              ))}
            </div>
            
            {/* Admin Info Card */}
            <div className="rounded-2xl bg-gradient-to-r from-primary/10 to-primary/5 border border-primary/20 p-4">
              <h3 className="text-sm font-bold text-foreground mb-2 flex items-center gap-2"><Shield className="h-4 w-4 text-primary" />{t('settingsLabel')}</h3>
              <p className="text-xs text-muted-foreground">{t('email')}: <span className="text-primary" dir="ltr">mohammadalrejab@gmail.com</span></p>
              <p className="text-xs text-muted-foreground mt-1">{t('name')}: <span className="text-primary" dir="ltr">+4917684034961</span></p>
            </div>

            {/* Category Stats */}
            <div className="rounded-2xl neu-card p-4">
              <h3 className="text-sm font-bold text-foreground mb-3 flex items-center gap-2"><BookOpen className="h-4 w-4 text-primary" />{t('overview')} {t('categoryField')}</h3>
              <div className="space-y-2">
                {stats?.categories?.length > 0 ? stats.categories.map((cat: any) => (
                  <div key={cat.category} className="flex items-center justify-between py-1.5 border-b border-border/10 last:border-0">
                    <span className="text-xs font-medium text-foreground">{cat.category}</span>
                    <span className="text-xs font-bold text-primary bg-primary/10 px-2 py-0.5 rounded-full">{cat.count}</span>
                  </div>
                )) : <p className="text-xs text-muted-foreground text-center py-4">{t('noData')}</p>}
              </div>
              {/* Seed Content Button */}
              <button 
                onClick={async () => {
                  try {
                    const r = await api('/admin/seed-content', 'POST');
                    toast.success(r.message || `تم {t('add')} ${r.created}`);
                    fetchStats();
                  } catch { toast.error(t('loadingData')); }
                }}
                className="w-full mt-3 py-2.5 rounded-xl bg-primary/10 border border-primary/30 text-primary text-xs font-bold active:scale-[0.98] transition-transform"
              >
                {t('embedContent')}
              </button>
            </div>
          </div>
        )}


        {/* ===== SOCIAL PLATFORM MANAGEMENT ===== */}
        {tab==='social-mgmt' && (
          <div className="space-y-4">
            {/* Social Stats */}
            {socialStats && (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {[
                  { label: t('totalPosts'), value: socialStats.total_posts, color: 'text-emerald-500' },
                  { label: t('totalUsers'), value: socialStats.total_users, color: 'text-blue-500' },
                  { label: t('adsManagement'), value: socialStats.total_comments, color: 'text-purple-500' },
                  { label: t('overview'), value: socialStats.total_likes, color: 'text-red-500' },
                  { label: t('usersManagement'), value: socialStats.total_follows, color: 'text-yellow-500' },
                ].map((s, i) => (
                  <div key={i} className="bg-card rounded-xl p-3 border border-border/30">
                    <p className={cn("text-lg font-bold", s.color)}>{s.value}</p>
                    <p className="text-[11px] text-muted-foreground">{s.label}</p>
                  </div>
                ))}
              </div>
            )}

            {/* Social Posts */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-bold text-foreground">{t('totalPosts')} ({socialPosts.length})</h3>
                <button onClick={fetchSocialPosts} className="p-1.5 rounded-lg bg-muted"><RefreshCw className="h-3.5 w-3.5 text-muted-foreground" /></button>
              </div>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {socialPosts.map(p => (
                  <div key={p.id} className="bg-card rounded-xl p-3 border border-border/20" dir={dir}>
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <span className="text-xs font-bold text-foreground">{p.author_name}</span>
                        <span className="text-[10px] text-muted-foreground mr-2">{p.content_type || 'text'}</span>
                        <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">{p.content}</p>
                      </div>
                      <button onClick={() => deleteSocialPost(p.id)} className="p-1.5 rounded-lg bg-red-500/10 text-red-500 hover:bg-red-500/20 shrink-0">
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Social Comments */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-bold text-foreground">{t('adsManagement')} ({socialComments.length})</h3>
                <button onClick={fetchSocialComments} className="p-1.5 rounded-lg bg-muted"><RefreshCw className="h-3.5 w-3.5 text-muted-foreground" /></button>
              </div>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {socialComments.map(c => (
                  <div key={c.id} className="bg-card rounded-xl p-2.5 border border-border/20 flex items-start justify-between gap-2" dir={dir}>
                    <div className="flex-1 min-w-0">
                      <span className="text-xs font-bold text-foreground">{c.author_name}</span>
                      <p className="text-[11px] text-muted-foreground mt-0.5 line-clamp-1">{c.content}</p>
                    </div>
                    <button onClick={() => deleteSocialComment(c.id)} className="p-1 rounded bg-red-500/10 text-red-500 shrink-0">
                      <Trash2 className="h-3 w-3" />
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Social Users */}
            <div>
              <h3 className="text-sm font-bold text-foreground mb-2">{t('usersManagement')} ({socialUsers.length})</h3>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {socialUsers.map(u => (
                  <div key={u.id} className="bg-card rounded-xl p-2.5 border border-border/20 flex items-center gap-2" dir={dir}>
                    <div className="w-8 h-8 rounded-full bg-emerald-600/20 flex items-center justify-center text-emerald-500 text-xs font-bold shrink-0">
                      {(u.name || '?')[0]}
                    </div>
                    <div className="flex-1 min-w-0">
                      <span className="text-xs font-bold text-foreground">{u.name}</span>
                      <span className="text-[10px] text-muted-foreground mr-2">{u.email}</span>
                    </div>
                    <div className="flex gap-2 text-[10px] text-muted-foreground shrink-0">
                      <span>{u.posts_count || 0} {t('totalPosts')}</span>
                      <span>{u.followers_count || 0} {t('usersManagement')}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ===== STORIES MANAGEMENT ===== */}
        {tab==='stories-mgmt' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-foreground">{t('storiesManagement')} ({storiesTotal})</h2>
              <button onClick={fetchAdminStories} className="p-2 rounded-lg bg-muted"><RefreshCw className="h-4 w-4 text-muted-foreground" /></button>
            </div>
            <div className="flex gap-2 overflow-x-auto pb-1">
              {[{k:'',l:t('overview')},{k:'pending',l:t('pending')},{k:'approved',l:t('approved')},{k:'rejected',l:t('rejected')}].map(f=>(
                <button key={f.k} onClick={()=>setStoriesFilter(f.k)}
                  className={cn('px-3 py-1.5 rounded-lg text-xs font-bold shrink-0 transition-all',
                    storiesFilter===f.k ? 'bg-primary text-primary-foreground' : 'neu-card text-muted-foreground')}>
                  {f.l}
                </button>
              ))}
            </div>
            {adminStories.length === 0 ? <p className="text-center py-8 text-muted-foreground text-sm">{t('noData')}</p> :
            adminStories.map(s => (
              <div key={s.id} className="rounded-xl neu-card p-4 space-y-2">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-foreground truncate">{s.title || t('noData')}</p>
                    <p className="text-xs text-muted-foreground line-clamp-2 mt-1">{s.content?.slice(0,120)}</p>
                    <div className="flex items-center gap-2 mt-2 flex-wrap">
                      <span className="text-[10px] bg-muted px-2 py-0.5 rounded">{s.category || t('overview')}</span>
                      <span className="text-[10px] text-muted-foreground">{s.author_name || t('noData')}</span>
                      <span className="text-[10px] text-muted-foreground">❤️ {s.likes_count||0} 💬 {s.comments_count||0} 👁 {s.views_count||0}</span>
                      <span className={cn('text-[10px] px-2 py-0.5 rounded-full font-bold',
                        s.status === 'approved' ? 'bg-green-500/10 text-green-500' :
                        s.status === 'rejected' ? 'bg-red-500/10 text-red-500' :
                        'bg-amber-500/10 text-amber-500'
                      )}>
                        {s.status === 'approved' ? t('approved') : s.status === 'rejected' ? t('rejected') : t('pending')}
                      </span>
                    </div>
                  </div>
                  {s.image_url && <img src={s.image_url.startsWith('http') ? s.image_url : `${BACKEND_URL}${s.image_url}`} alt="" className="h-16 w-16 rounded-lg object-cover shrink-0" />}
                </div>
                <div className="flex gap-2 pt-1">
                  {s.status !== 'approved' && <Button onClick={() => moderateStory(s.id, 'approve')} size="sm" className="flex-1 rounded-xl gap-1 bg-green-600 hover:bg-green-700 text-[11px]"><Check className="h-3 w-3"/>{t('approveAction')}</Button>}
                  {s.status !== 'rejected' && <Button onClick={() => moderateStory(s.id, 'reject')} size="sm" variant="outline" className="flex-1 rounded-xl gap-1 text-[11px] border-red-500/30 text-red-500"><X className="h-3 w-3"/>{t('rejectAction')}</Button>}
                  <button onClick={() => deleteStory(s.id)} className="p-2 rounded-lg bg-destructive/10 text-destructive shrink-0"><Trash2 className="h-3.5 w-3.5" /></button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ===== RUQYAH MANAGEMENT ===== */}
        {tab==='ruqyah-mgmt' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base font-bold text-foreground">{t('ruqyahManagement')} ({ruqyahItems.length})</h2>
                <p className="text-xs text-muted-foreground"> {t('ruqyahManagement')}</p>
              </div>
              <Button onClick={() => { setRuqyahForm({title:'',content:'',category:'general',audio_url:'',video_url:'',order:0,enabled:true}); setShowRuqyahForm(true); }} size="sm" className="rounded-xl gap-1"><Plus className="h-3.5 w-3.5" />{t('add')}</Button>
            </div>

            {showRuqyahForm && (
              <div className="rounded-2xl bg-card border border-primary/20 p-4 space-y-3">
                <InputField label={t('notifTitle')} value={ruqyahForm.title} onChange={(v: string) => setRuqyahForm({...ruqyahForm, title: v})} placeholder="..." />
                <InputField label={t('notifBody')} value={ruqyahForm.content} onChange={(v: string) => setRuqyahForm({...ruqyahForm, content: v})} placeholder="..." multiline />
                <SelectField label={t('categoryField')} value={ruqyahForm.category} onChange={(v: string) => setRuqyahForm({...ruqyahForm, category: v})} options={['general',t('ruqyahCatEye'),t('ruqyahCatEnvy'),t('ruqyahCatMagic'),'مس','أرق','وسواس',t('protectionLabel')]} />
                <InputField label={t('adLinkUrl')} value={ruqyahForm.audio_url} onChange={(v: string) => setRuqyahForm({...ruqyahForm, audio_url: v})} placeholder="https://..." />
                <InputField label={t('adVideoUrl')} value={ruqyahForm.video_url} onChange={(v: string) => setRuqyahForm({...ruqyahForm, video_url: v})} placeholder="https://www.youtube.com/watch?v=..." />
                {ruqyahForm.video_url && (
                  <div className="rounded-lg bg-muted/50 p-2">
                    <p className="text-[10px] text-muted-foreground mb-1"></p>
                    <p className="text-[10px] text-primary truncate">{ruqyahForm.video_url}</p>
                  </div>
                )}
                <InputField label={t('settingsLabel')} value={String(ruqyahForm.order)} onChange={(v: string) => setRuqyahForm({...ruqyahForm, order: Number(v)||0})} placeholder="0" />
                <div className="flex items-center gap-2">
                  <Switch checked={ruqyahForm.enabled} onCheckedChange={(v) => setRuqyahForm({...ruqyahForm, enabled: v})} />
                  <span className="text-xs text-foreground">{t('adActive')}</span>
                </div>
                <div className="flex gap-2 pt-1">
                  <Button onClick={saveRuqyah} className="flex-1 rounded-xl gap-2"><Check className="h-4 w-4" />{t('save')}</Button>
                  <Button variant="outline" onClick={() => setShowRuqyahForm(false)} className="rounded-xl">{t('cancel')}</Button>
                </div>
              </div>
            )}

            {ruqyahItems.length === 0 && !showRuqyahForm ? <p className="text-center py-8 text-muted-foreground text-sm">{t('noData')}</p> :
            ruqyahItems.map(item => (
              <div key={item.id} className="rounded-xl neu-card p-4">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className={cn("h-2 w-2 rounded-full", item.enabled ? 'bg-green-500' : 'bg-red-500')} />
                      <p className="text-sm font-bold text-foreground">{item.title}</p>
                    </div>
                    <p className="text-xs text-muted-foreground line-clamp-2 mt-1">{item.content?.slice(0,100)}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <span className="text-[10px] bg-primary/10 text-primary px-2 py-0.5 rounded-full">{item.category}</span>
                      {item.audio_url && <span className="text-[10px] text-blue-500">🔊</span>}
                      {item.video_url && <span className="text-[10px] text-red-500">🎬 ({item.video_type || ''})</span>}
                      <span className="text-[10px] text-muted-foreground">{t('settingsLabel')}: {item.order}</span>
                    </div>
                  </div>
                  <div className="flex gap-1">
                    <button onClick={() => { setRuqyahForm(item); setShowRuqyahForm(true); }} className="p-2 rounded-lg bg-primary/10 text-primary"><Sparkles className="h-3.5 w-3.5" /></button>
                    <button onClick={() => deleteRuqyah(item.id)} className="p-2 rounded-lg bg-destructive/10 text-destructive"><Trash2 className="h-3.5 w-3.5" /></button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ===== DONATIONS MANAGEMENT ===== */}
        {tab==='donations-mgmt' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base font-bold text-foreground">{t('donationsManagement')} ({donationsTotal})</h2>
                <p className="text-xs text-muted-foreground"></p>
              </div>
              <button onClick={fetchAdminDonations} className="p-2 rounded-lg bg-muted"><RefreshCw className="h-4 w-4 text-muted-foreground" /></button>
            </div>
            
            {donationsTotalAmount > 0 && (
              <div className="rounded-2xl bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/20 p-4 text-center">
                <p className="text-2xl font-bold text-green-600">${donationsTotalAmount.toLocaleString()}</p>
                <p className="text-xs text-muted-foreground">{t('donationsManagement')}</p>
              </div>
            )}

            <div className="flex gap-2 overflow-x-auto pb-1">
              {[{k:'',l:t('overview')},{k:'pending',l:t('pending')},{k:'approved',l:t('approved')},{k:'rejected',l:t('rejected')}].map(f=>(
                <button key={f.k} onClick={()=>setDonationsFilter(f.k)}
                  className={cn('px-3 py-1.5 rounded-lg text-xs font-bold shrink-0 transition-all',
                    donationsFilter===f.k ? 'bg-primary text-primary-foreground' : 'neu-card text-muted-foreground')}>
                  {f.l}
                </button>
              ))}
            </div>

            {adminDonations.length === 0 ? <p className="text-center py-8 text-muted-foreground text-sm">{t('noData')}</p> :
            adminDonations.map(d => (
              <div key={d.id} className="rounded-xl neu-card p-4 space-y-2">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-foreground">{d.title || t('donationsManagement')}</p>
                    <p className="text-xs text-muted-foreground mt-1">{d.description?.slice(0,100)}</p>
                    <div className="flex items-center gap-2 mt-2 flex-wrap">
                      <span className="text-[10px] bg-green-500/10 text-green-600 px-2 py-0.5 rounded-full font-bold">${d.amount || 0}</span>
                      <span className="text-[10px] text-muted-foreground">{d.donor_name || t('noData')}</span>
                      <span className={cn('text-[10px] px-2 py-0.5 rounded-full font-bold',
                        d.status === 'approved' ? 'bg-green-500/10 text-green-500' :
                        d.status === 'rejected' ? 'bg-red-500/10 text-red-500' :
                        'bg-amber-500/10 text-amber-500'
                      )}>
                        {d.status === 'approved' ? t('approved') : d.status === 'rejected' ? t('rejected') : t('pending')}
                      </span>
                    </div>
                  </div>
                </div>
                {d.status === 'pending' && (
                  <div className="flex gap-2 pt-1">
                    <Button onClick={() => moderateDonation(d.id, 'approve')} size="sm" className="flex-1 rounded-xl gap-1 bg-green-600 hover:bg-green-700 text-[11px]"><Check className="h-3 w-3"/>{t('approveAction')}</Button>
                    <Button onClick={() => moderateDonation(d.id, 'reject')} size="sm" variant="outline" className="flex-1 rounded-xl gap-1 text-[11px] border-red-500/30 text-red-500"><X className="h-3 w-3"/>{t('rejectAction')}</Button>
                  </div>
                )}
                <div className="flex justify-end">
                  <button onClick={() => deleteDonation(d.id)} className="p-1.5 rounded-lg bg-destructive/10 text-destructive"><Trash2 className="h-3 w-3" /></button>
                </div>
              </div>
            ))}
          </div>
        )}


        {/* ===== BROADCAST ({t('broadcast')}) ===== */}
        {tab==='broadcast' && (
          <div className="space-y-4">
            <h2 className="text-base font-bold text-foreground">{t('publishBroadcast')}</h2>
            <p className="text-xs text-muted-foreground"></p>
            <div className="rounded-2xl bg-card border border-primary/20 p-4 space-y-3">
              <InputField label={t('notifTitle')} value={broadcastTitle} onChange={setBroadcastTitle} placeholder={t('notifTitle')} />
              <InputField label={t('notifBody')} value={broadcastBody} onChange={setBroadcastBody} placeholder={t('notifBody')} multiline />
              <SelectField label={t('type')} value={broadcastType} onChange={setBroadcastType} options={['info','warning','promo']} />
              <Button onClick={publishBroadcast} className="w-full rounded-xl gap-2" data-testid="publish-broadcast-btn">
                <Megaphone className="h-4 w-4" />{t('publishBroadcast')}
              </Button>
            </div>
            
            <h3 className="text-sm font-bold text-foreground mt-4">{t('adsManagement')}  ({broadcastList.length})</h3>
            {broadcastList.map(a => (
              <div key={a.id} className="rounded-xl neu-card p-4 flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-foreground">{a.title}</p>
                  <p className="text-xs text-muted-foreground mt-1">{a.body}</p>
                  <p className="text-[10px] text-muted-foreground mt-1">{a.type} • {new Date(a.created_at).toLocaleDateString(locale)}</p>
                </div>
                <button onClick={() => deleteBroadcast(a.id)} className="p-2 rounded-lg bg-destructive/10 text-destructive shrink-0"><Trash2 className="h-3.5 w-3.5" /></button>
              </div>
            ))}
          </div>
        )}

        {/* ===== EMBED CONTENT ===== */}
        {tab==='embed' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base font-bold text-foreground">{t('embedContent')}</h2>
                <p className="text-xs text-muted-foreground"></p>
              </div>
              <Button onClick={() => setShowEmbedForm(true)} size="sm" className="rounded-xl gap-1 shrink-0"><Plus className="h-3.5 w-3.5" />{t('add')}</Button>
            </div>

            {showEmbedForm && (
              <div className="rounded-2xl bg-card border border-primary/20 p-4 space-y-3">
                <InputField label={t('notifTitle')} value={embedForm.title} onChange={(v: string) => setEmbedForm(f => ({...f, title: v}))} placeholder={t('notifTitle')} />
                <InputField label={t('adDescription')} value={embedForm.description} onChange={(v: string) => setEmbedForm(f => ({...f, description: v}))} placeholder={t('adDescription')} multiline />
                <InputField label={t('embedUrl')} value={embedForm.embed_url} onChange={(v: string) => setEmbedForm(f => ({...f, embed_url: v}))} placeholder="https://youtube.com/watch?v=..." />
                <SelectField label={t('settingsLabel')} value={embedForm.platform} onChange={(v: string) => setEmbedForm(f => ({...f, platform: v}))} options={['youtube','dailymotion','vimeo','tiktok','instagram','other']} />
                <SelectField label="" value={embedForm.category} onChange={(v: string) => setEmbedForm(f => ({...f, category: v}))} options={['general','istighfar','sahaba','quran','prophets','ruqyah','rizq','tawba','miracles','embed']} />
                <InputField label={t('thumbnail')} value={embedForm.thumbnail_url} onChange={(v: string) => setEmbedForm(f => ({...f, thumbnail_url: v}))} placeholder={t('adLinkUrl')} />
                <div className="flex gap-2 pt-1">
                  <Button onClick={saveEmbedContent} className="flex-1 rounded-xl gap-2"><Film className="h-4 w-4" />{t('save')}</Button>
                  <Button variant="outline" onClick={() => setShowEmbedForm(false)} className="rounded-xl">{t('cancel')}</Button>
                </div>
                <p className="text-[10px] text-muted-foreground">{t('embedNote')}</p>
              </div>
            )}

            <h3 className="text-sm font-bold text-foreground"> ال{t('totalPosts')} ({embedContent.length})</h3>
            {embedContent.length === 0 ? (
              <p className="text-center py-8 text-muted-foreground text-sm">{t('noEmbedYet')}</p>
            ) : (
              embedContent.map(item => (
                <div key={item.id} className="rounded-xl neu-card p-4 space-y-2">
                  {item.thumbnail_url && (
                    <div className="rounded-lg overflow-hidden h-36 w-full mb-2">
                      <img src={item.thumbnail_url} alt="" className="w-full h-full object-cover" />
                    </div>
                  )}
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-foreground">{item.title}</p>
                      {item.description && <p className="text-xs text-muted-foreground mt-0.5">{item.description}</p>}
                      <p className="text-[10px] text-muted-foreground mt-1">{item.platform} • {item.category} • {item.views || 0} {t('viewAction')}</p>
                    </div>
                    <button onClick={() => deleteEmbedContent(item.id)} className="p-2 rounded-lg bg-destructive/10 text-destructive shrink-0"><Trash2 className="h-3.5 w-3.5" /></button>
                  </div>
                  {/* Preview iframe */}
                  {item.embed_url && (item.embed_url.includes('youtube') || item.embed_url.includes('vimeo') || item.embed_url.includes('dailymotion')) && (
                    <div className="rounded-lg overflow-hidden aspect-video">
                      <iframe src={item.embed_url} title={item.title} className="w-full h-full" frameBorder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}

        {/* ===== USERS ===== */}
        {tab==='users' && (
          <div className="space-y-2">
            <h2 className="text-base font-bold text-foreground">{t('usersManagement')} ({usersTotal})</h2>
            {users.length===0 ? <p className="text-center py-8 text-muted-foreground text-sm">{t('noData')}</p> :
            users.map(u=>(
              <div key={u.id} className="rounded-xl neu-card p-3 flex items-center justify-between">
                <div className="min-w-0 flex-1"><p className="text-sm font-bold text-foreground truncate">{u.name||t('noData')}</p><p className="text-xs text-muted-foreground truncate">{u.email}</p></div>
                <button onClick={()=>deleteUser(u.id)} className="p-1.5 rounded-lg bg-destructive/10 text-destructive mr-2"><Trash2 className="h-3.5 w-3.5"/></button>
              </div>
            ))}
          </div>
        )}

        {/* ===== ADS ===== */}
        {tab==='ads' && (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <h2 className="text-base font-bold text-foreground">{t('adminPanel')} {t('adsManagement')}</h2>
              <button onClick={()=>{setAdForm({name:'',provider:'Google AdSense',code:'',placement:'home',ad_type:'banner',enabled:true,priority:0}); setShowAdForm(true);}}
                className="flex items-center gap-1 text-xs bg-primary text-primary-foreground px-3 py-1.5 rounded-lg"><Plus className="h-3 w-3"/>{t('add')}</button>
            </div>

            {showAdForm && (
              <div className="rounded-xl bg-card border border-primary/30 p-3 space-y-2">
                <InputField label={t('adName')} value={adForm.name} onChange={(v:string)=>setAdForm({...adForm,name:v})} placeholder={t('adName')} />
                <SelectField label={t('settingsLabel')} value={adForm.provider} onChange={(v:string)=>setAdForm({...adForm,provider:v})} options={AD_PROVIDERS} />
                <InputField label={t('adCode')} value={adForm.code} onChange={(v:string)=>setAdForm({...adForm,code:v})} placeholder="<script>...</script>" multiline />
                <div className="grid grid-cols-2 gap-2">
                  <SelectField label={t('adPosition')} value={adForm.placement} onChange={(v:string)=>setAdForm({...adForm,placement:v})} options={AD_PLACEMENTS} />
                  <SelectField label={t('type')} value={adForm.ad_type} onChange={(v:string)=>setAdForm({...adForm,ad_type:v})} options={AD_TYPES} />
                </div>
                <div className="flex gap-2">
                  <Button onClick={saveAd} size="sm" className="flex-1 rounded-lg gap-1"><Check className="h-3 w-3"/>{t('save')}</Button>
                  <Button onClick={()=>setShowAdForm(false)} size="sm" variant="outline" className="rounded-lg"><X className="h-3 w-3"/></Button>
                </div>
              </div>
            )}

            {ads.length===0 && !showAdForm ? <p className="text-center py-8 text-muted-foreground text-sm">{t('noData')}</p> :
            ads.map(ad=>(
              <div key={ad.id} className="rounded-xl neu-card p-3">
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    <span className={cn("h-2 w-2 rounded-full", ad.enabled?'bg-green-500':'bg-red-500')}/>
                    <p className="text-sm font-bold text-foreground">{ad.name}</p>
                  </div>
                  <button onClick={()=>deleteAd(ad.id)} className="p-1 rounded-lg bg-destructive/10 text-destructive"><Trash2 className="h-3 w-3"/></button>
                </div>
                <div className="flex gap-2 text-[10px] text-muted-foreground flex-wrap">
                  <span className="bg-muted px-2 py-0.5 rounded">{ad.provider}</span>
                  <span className="bg-muted px-2 py-0.5 rounded">{ad.placement}</span>
                  <span className="bg-muted px-2 py-0.5 rounded">{ad.ad_type}</span>
                </div>
              </div>
            ))}

            <div className="rounded-xl bg-muted/50 border border-border/30 p-3">
              <p className="text-xs font-bold text-foreground mb-1">{t('adProviders')}:</p>
              <div className="flex flex-wrap gap-1">{AD_PROVIDERS.map(p=><span key={p} className="text-[10px] bg-primary/10 text-primary px-2 py-0.5 rounded-full">{p}</span>)}</div>
            </div>
          </div>
        )}

        {/* ===== NOTIFICATIONS ===== */}
        {tab==='notifications' && (
          <div className="space-y-3">
            <h2 className="text-base font-bold text-foreground">{t('scheduledNotifications')}</h2>
            
            {/* Send instant */}
            <div className="rounded-xl neu-card p-3 space-y-2">
              <p className="text-xs font-bold text-foreground">{t('send')}</p>
              <InputField label={t('notifTitle')} value={nTitle} onChange={setNTitle} placeholder={t('notifTitle')} />
              <InputField label={t('notifBody')} value={nBody} onChange={setNBody} placeholder={t('notifBody')} multiline />
              <Button onClick={sendNotif} size="sm" className="w-full rounded-lg gap-1"><Send className="h-3 w-3"/>{t('send')}</Button>
            </div>

            {/* Scheduled */}
            <div className="flex justify-between items-center">
              <p className="text-xs font-bold text-foreground">{t('scheduledNotifications')}</p>
              <button onClick={()=>{setNotifForm({title:'',body:'',schedule_time:'',repeat:'once',enabled:true}); setShowNotifForm(true);}}
                className="flex items-center gap-1 text-[10px] bg-primary text-primary-foreground px-2 py-1 rounded"><Plus className="h-3 w-3"/>{t('add')}</button>
            </div>

            {showNotifForm && (
              <div className="rounded-xl bg-card border border-primary/30 p-3 space-y-2">
                <InputField label={t('notifTitle')} value={notifForm.title} onChange={(v:string)=>setNotifForm({...notifForm,title:v})} placeholder={t('scheduledNotifications')} />
                <InputField label={t('notifBody')} value={notifForm.body} onChange={(v:string)=>setNotifForm({...notifForm,body:v})} placeholder={t('notifBody')} />
                <div className="grid grid-cols-2 gap-2">
                  <InputField label={`${t('schedTime')} (HH:MM)`} value={notifForm.schedule_time} onChange={(v:string)=>setNotifForm({...notifForm,schedule_time:v})} placeholder="08:00" />
                  <SelectField label={t('recurring')} value={notifForm.repeat} onChange={(v:string)=>setNotifForm({...notifForm,repeat:v})} options={['once','daily','weekly']} />
                </div>
                <div className="flex gap-2">
                  <Button onClick={saveSchedNotif} size="sm" className="flex-1 rounded-lg gap-1"><Check className="h-3 w-3"/>{t('save')}</Button>
                  <Button onClick={()=>setShowNotifForm(false)} size="sm" variant="outline" className="rounded-lg"><X className="h-3 w-3"/></Button>
                </div>
              </div>
            )}

            {scheduledNotifs.map(n=>(
              <div key={n.id} className="rounded-xl neu-card p-3 flex items-center justify-between">
                <div><p className="text-sm font-bold text-foreground">{n.title}</p><p className="text-[10px] text-muted-foreground">{n.schedule_time||t('send')} • {n.repeat}</p></div>
                <button onClick={()=>deleteSchedNotif(n.id)} className="p-1 rounded-lg bg-destructive/10 text-destructive"><Trash2 className="h-3 w-3"/></button>
              </div>
            ))}
          </div>
        )}

        {/* ===== PAGES ===== */}
        {tab==='pages' && (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <h2 className="text-base font-bold text-foreground">{t('adminPanel')} {t('pagesManagement')}</h2>
              <button onClick={()=>{setPageForm({title:'',category:'',content:'',enabled:true,order:0}); setShowPageForm(true);}}
                className="flex items-center gap-1 text-xs bg-primary text-primary-foreground px-3 py-1.5 rounded-lg"><Plus className="h-3 w-3"/>{t('add')}</button>
            </div>

            {showPageForm && (
              <div className="rounded-xl bg-card border border-primary/30 p-3 space-y-2">
                <InputField label={t('pageTitle')} value={pageForm.title} onChange={(v:string)=>setPageForm({...pageForm,title:v})} placeholder={t('pageTitle')} />
                <InputField label={t('categoryField')} value={pageForm.category} onChange={(v:string)=>setPageForm({...pageForm,category:v})} placeholder={t('categoryField')} />
                <InputField label={t('notifBody')} value={pageForm.content} onChange={(v:string)=>setPageForm({...pageForm,content:v})} placeholder={t('notifBody')} multiline />
                <div className="flex gap-2">
                  <Button onClick={savePage} size="sm" className="flex-1 rounded-lg gap-1"><Check className="h-3 w-3"/>{t('save')}</Button>
                  <Button onClick={()=>setShowPageForm(false)} size="sm" variant="outline" className="rounded-lg"><X className="h-3 w-3"/></Button>
                </div>
              </div>
            )}

            {pages.length===0 && !showPageForm ? <p className="text-center py-8 text-muted-foreground text-sm">{t('noData')}</p> :
            pages.map(p=>(
              <div key={p.id} className="rounded-xl neu-card p-3 flex items-center justify-between">
                <div><p className="text-sm font-bold text-foreground">{p.title}</p><p className="text-[10px] text-muted-foreground">{p.category} • {p.enabled?t('adActive'):t('disabled')}</p></div>
                <button onClick={()=>deletePage(p.id)} className="p-1 rounded-lg bg-destructive/10 text-destructive"><Trash2 className="h-3 w-3"/></button>
              </div>
            ))}
          </div>
        )}

        {/* ===== SETTINGS ===== */}
        {tab==='settings' && (
          <div className="space-y-4">
            <h2 className="text-base font-bold text-foreground">{t('appSettingsTitle')}</h2>
            <div className="rounded-xl neu-card p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2"><AlertTriangle className="h-4 w-4 text-amber-500"/><div><p className="text-sm font-bold text-foreground">{t('maintenanceMode')}</p><p className="text-[10px] text-muted-foreground">{t('tempPause')}</p></div></div>
                <Switch checked={maintenance} onCheckedChange={setMaintenance} />
              </div>
              <InputField label={t('generalAnnouncementLabel')} value={announcement} onChange={setAnnouncement} placeholder={t('msgForAll')} />
              <Button onClick={saveSettings} size="sm" className="w-full rounded-xl gap-1"><Settings className="h-3 w-3"/>{t('save')}</Button>
            </div>
            
            {/* Admin Bank Account */}
            <h2 className="text-base font-bold text-foreground">{t('bankAccountTitle')}</h2>
            <div className="rounded-xl bg-card border border-primary/20 p-4 space-y-3">
              <InputField label={t('bankNameLabel')} value={bankForm.bank_name||''} onChange={(v:string)=>setBankForm({...bankForm,bank_name:v})} placeholder="بنك..." />
              <InputField label="{t('accountHolder')}" value={bankForm.account_holder||''} onChange={(v:string)=>setBankForm({...bankForm,account_holder:v})} placeholder="الاسم..." />
              <InputField label="IBAN" value={bankForm.iban||''} onChange={(v:string)=>setBankForm({...bankForm,iban:v})} placeholder="SA00..." />
              <InputField label="SWIFT" value={bankForm.swift||''} onChange={(v:string)=>setBankForm({...bankForm,swift:v})} placeholder="SWIFT..." />
              <Button onClick={saveBankInfo} size="sm" className="w-full rounded-xl gap-1"><Building2 className="h-3 w-3"/>حفظ الحساب {t('bankAccount')}ي</Button>
            </div>

            {/* Marketplace Commission */}
            <h2 className="text-base font-bold text-foreground">{t('marketCommission')}</h2>
            <div className="rounded-xl neu-card p-4 space-y-3">
              <div className="flex items-center gap-3">
                <InputField label="{t('commissionRate')} %" value={String(commissionRate)} onChange={(v:string)=>setCommissionRate(Number(v)||0)} placeholder="10" />
                <Button onClick={saveCommission} size="sm" className="rounded-xl mt-5">{t('save')}</Button>
              </div>
            </div>

            {/* Ad Settings - {t('adSettingsTitle')} */}
            <h2 className="text-base font-bold text-foreground flex items-center gap-2">
              <Film className="h-4 w-4 text-primary"/>{t('adSettingsTitle')}
            </h2>
            <div className="rounded-xl bg-card border border-primary/20 p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Monitor className="h-4 w-4 text-emerald-500"/>
                  <div><p className="text-sm font-bold text-foreground">{t('enableAds')}</p><p className="text-[10px] text-muted-foreground">عرض {t('adsManagement')} في التطبيق</p></div>
                </div>
                <Switch checked={adSettings.ads_enabled} onCheckedChange={(v)=>setAdSettings({...adSettings, ads_enabled:v})} />
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Volume2 className="h-4 w-4 text-blue-500"/>
                  <div><p className="text-sm font-bold text-foreground">{t('muteVideo')}</p><p className="text-[10px] text-muted-foreground">كتم الصوت تلقائياً لإعلانات الفيديو</p></div>
                </div>
                <Switch checked={adSettings.video_ads_muted} onCheckedChange={(v)=>setAdSettings({...adSettings, video_ads_muted:v})} />
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Shield className="h-4 w-4 text-amber-500"/>
                  <div><p className="text-sm font-bold text-foreground">{t('gdprConsent')}</p><p className="text-[10px] text-muted-foreground">طلب الموافقة من {t('usersManagement')} الأوروبيين</p></div>
                </div>
                <Switch checked={adSettings.gdpr_consent_required} onCheckedChange={(v)=>setAdSettings({...adSettings, gdpr_consent_required:v})} />
              </div>
              <div className="border-t border-border/30 pt-3 space-y-2">
                <p className="text-xs font-bold text-foreground">{t('adTypes')}</p>
                <div className="flex items-center justify-between">
                  <p className="text-xs text-muted-foreground">{t('bannerAds')}</p>
                  <Switch checked={adSettings.ad_banner_enabled} onCheckedChange={(v)=>setAdSettings({...adSettings, ad_banner_enabled:v})} />
                </div>
                <div className="flex items-center justify-between">
                  <p className="text-xs text-muted-foreground">{t('interstitialAds')}</p>
                  <Switch checked={adSettings.ad_interstitial_enabled} onCheckedChange={(v)=>setAdSettings({...adSettings, ad_interstitial_enabled:v})} />
                </div>
                <div className="flex items-center justify-between">
                  <p className="text-xs text-muted-foreground">{t('rewardedAds')}</p>
                  <Switch checked={adSettings.ad_rewarded_enabled} onCheckedChange={(v)=>setAdSettings({...adSettings, ad_rewarded_enabled:v})} />
                </div>
              </div>
              <div className="border-t border-border/30 pt-3 space-y-2">
                <InputField label="AdMob App ID" value={adSettings.admob_app_id} onChange={(v:string)=>setAdSettings({...adSettings, admob_app_id:v})} placeholder="ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY" />
                <InputField label="AdSense Publisher ID" value={adSettings.adsense_publisher_id} onChange={(v:string)=>setAdSettings({...adSettings, adsense_publisher_id:v})} placeholder="pub-XXXXXXXXXXXXXXXX" />
              </div>
              <Button onClick={saveAdSettings} size="sm" className="w-full rounded-xl gap-1"><Settings className="h-3 w-3"/>حفظ {t('adSettingsTitle')}</Button>
            </div>

            {/* Analytics Quick View */}
            <h2 className="text-base font-bold text-foreground flex items-center gap-2">
              <BarChart3 className="h-4 w-4 text-primary"/>{t('analyticsTitle')}
            </h2>
            <div className="rounded-xl neu-card p-4 space-y-3">
              <Button onClick={fetchAnalytics} size="sm" variant="outline" className="w-full rounded-xl gap-1"><RefreshCw className="h-3 w-3"/>{t('refreshAnalytics')}</Button>
              {analyticsData && (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="rounded-xl bg-muted/50 p-3 text-center">
                      <p className="text-xl font-bold text-foreground">{analyticsData.total_events || 0}</p>
                      <p className="text-[10px] text-muted-foreground">{t('totalEvents')}</p>
                    </div>
                    <div className="rounded-xl bg-muted/50 p-3 text-center">
                      <p className="text-xl font-bold text-foreground">{analyticsData.unique_users || 0}</p>
                      <p className="text-[10px] text-muted-foreground">{t('uniqueUsers')}</p>
                    </div>
                  </div>
                  {analyticsData.top_pages?.length > 0 && (
                    <div>
                      <p className="text-xs font-bold text-foreground mb-1">{t('mostVisitedPages')}</p>
                      {analyticsData.top_pages.slice(0, 5).map((p: any, i: number) => (
                        <div key={i} className="flex justify-between text-xs py-0.5">
                          <span className="text-muted-foreground">{p.page}</span>
                          <span className="font-bold text-foreground">{p.views}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="rounded-xl neu-card p-4 space-y-1 text-xs text-muted-foreground">
              <p className="font-bold text-foreground text-sm">{t('infoLabel')}</p>
              <p>Azan & Hikaya v3.0</p>
              <p>{t('responsibleLabel')} {user?.email}</p>
              <p>{t('aiLabel')} GPT-5.2</p>
            </div>
          </div>
        )}

        {/* ===== USER ADS (إعلانات القنوات) ===== */}
        {tab==='user-ads' && (
          <div className="space-y-3">
            <h2 className="text-base font-bold text-foreground">{t('channelAds')} ({userAds.length})</h2>
            <p className="text-xs text-muted-foreground">{t('channelAdsDesc')}</p>
            {userAds.length === 0 ? <p className="text-center py-8 text-muted-foreground text-sm">{t('noAdsYet')}</p> :
            userAds.map(ad => (
              <div key={ad.id} className="rounded-xl neu-card p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-bold text-foreground truncate">{ad.title}</p>
                    <p className="text-[10px] text-muted-foreground">{ad.channel_name} • {ad.user_name}</p>
                  </div>
                  <span className={cn('text-[10px] px-2 py-0.5 rounded-full font-bold shrink-0',
                    ad.status === 'approved' ? 'bg-green-500/10 text-green-500' :
                    ad.status === 'rejected' ? 'bg-red-500/10 text-red-500' :
                    'bg-amber-500/10 text-amber-500'
                  )}>
                    {ad.status === 'approved' ? t('approved') : ad.status === 'rejected' ? t('rejected') : t('pendingStatus')}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">{ad.description}</p>
                {ad.video_url && <p className="text-[10px] text-blue-500 truncate">{ad.video_url}</p>}
                <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
                  <span>{t('viewsLabel')} {ad.views || 0}</span>
                  <span>{t('priceLabel')} {ad.price_credits} {t('pointsUnit')}</span>
                </div>
                {ad.status === 'pending' && (
                  <div className="flex gap-2 pt-1">
                    <Button onClick={() => updateAdStatus(ad.id, 'approved')} size="sm" className="flex-1 rounded-xl gap-1 bg-green-600 hover:bg-green-700"><Check className="h-3 w-3"/>{t('approveAction')}</Button>
                    <Button onClick={() => updateAdStatus(ad.id, 'rejected')} size="sm" variant="destructive" className="flex-1 rounded-xl gap-1"><X className="h-3 w-3"/>{t('rejectAction')}</Button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* ===== VENDORS ({t('vendorRole')}) ===== */}
        {tab==='vendors' && (
          <div className="space-y-3">
            <h2 className="text-base font-bold text-foreground">{t('vendorRequests')} ({vendors.length})</h2>
            <p className="text-xs text-muted-foreground">{t('vendorNoPublish')}</p>
            {vendors.length === 0 ? <p className="text-center py-8 text-muted-foreground text-sm">{t('noVendorRequests')}</p> :
            vendors.map(v => (
              <div key={v.id} className="rounded-xl neu-card p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-bold text-foreground truncate">{v.shop_name || v.user_name}</p>
                    <p className="text-[10px] text-muted-foreground">{v.user_name} • {v.phone}</p>
                  </div>
                  <span className={cn('text-[10px] px-2 py-0.5 rounded-full font-bold shrink-0',
                    v.status === 'approved' ? 'bg-green-500/10 text-green-500' :
                    v.status === 'rejected' ? 'bg-red-500/10 text-red-500' :
                    'bg-amber-500/10 text-amber-500'
                  )}>
                    {v.status === 'approved' ? t('approved') : v.status === 'rejected' ? t('rejected') : t('pendingStatus')}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">{v.description}</p>
                {v.iban && <p className="text-[10px] text-muted-foreground">IBAN: {v.iban}</p>}
                {v.status === 'pending' && (
                  <div className="flex gap-2 pt-1">
                    <Button onClick={() => updateVendorStatus(v.id, 'approved')} size="sm" className="flex-1 rounded-xl gap-1 bg-green-600 hover:bg-green-700"><Check className="h-3 w-3"/>{t('approveAction')}</Button>
                    <Button onClick={() => updateVendorStatus(v.id, 'rejected')} size="sm" variant="destructive" className="flex-1 rounded-xl gap-1"><X className="h-3 w-3"/>{t('rejectAction')}</Button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* ===== REVENUE (الإيرادات) ===== */}
        {tab==='revenue' && (
          <div className="space-y-4">
            <h2 className="text-base font-bold text-foreground">{t('revenueTitle')}</h2>
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-2xl bg-card border border-amber-500/20 p-4 text-center">
                <Coins className="h-8 w-8 text-amber-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-foreground">{adminRevenue?.total_credits || 0}</p>
                <p className="text-xs text-muted-foreground">{t('giftPointsRevenue')}</p>
              </div>
              <div className="rounded-2xl bg-card border border-green-500/20 p-4 text-center">
                <CreditCard className="h-8 w-8 text-green-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-foreground">-</p>
                <p className="text-xs text-muted-foreground">{t('electronicPayment')}</p>
              </div>
            </div>
            <div className="rounded-xl bg-muted/50 border border-border/30 p-4 text-sm text-muted-foreground">
              <p className="font-bold text-foreground mb-2">{t('revenueHowItWorks')}</p>
              <ul className="space-y-1 text-xs list-disc list-inside">
                <li>{t('revenueRule1')}</li>
                <li>{t('revenueRule2')}</li>
                <li>{t('revenueRule3')}</li>
                <li>{t('revenueRule4')}</li>
              </ul>
            </div>
          </div>
        )}

        {/* ===== GOD-MODE: AD RULES PER PAGE/COUNTRY ===== */}
        {tab==='ad-rules' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-foreground flex items-center gap-2"><Shield className="h-5 w-5 text-amber-500"/>{t('adRulesGodMode')}</h2>
              <Button onClick={saveAdRules} size="sm" className="rounded-xl bg-green-600 hover:bg-green-700 gap-1"><Check className="h-3 w-3"/>{t('saveAllRules')}</Button>
            </div>
            <p className="text-xs text-muted-foreground">{t('adRulesDesc')}</p>
            <div className="space-y-3">
              {adRules.map((rule: any, i: number) => (
                <div key={rule.page} className={cn("rounded-2xl border p-4 space-y-3", rule.enabled ? "bg-card border-green-500/30" : "bg-muted/30 border-red-500/30")}>
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-foreground capitalize">{rule.page.replace('_', ' ')}</span>
                    <div className="flex items-center gap-2">
                      <span className={cn("text-xs font-bold", rule.enabled ? "text-green-500" : "text-red-500")}>{rule.enabled ? 'ON' : 'OFF'}</span>
                      <Switch checked={rule.enabled} onCheckedChange={(v) => toggleAdRule(rule.page, 'enabled', v)} />
                    </div>
                  </div>
                  {rule.enabled && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                      <div>
                        <label className="text-muted-foreground block mb-1">{t('countriesEnabled')}</label>
                        <input className="w-full rounded-lg bg-background border border-border/10 px-3 py-2 text-xs text-foreground" placeholder="DE, US, SA, TR"
                          value={(rule.countries_enabled||[]).join(', ')}
                          onChange={e => toggleAdRule(rule.page, 'countries_enabled', e.target.value.split(',').map((s:string) => s.trim()).filter(Boolean))} />
                      </div>
                      <div>
                        <label className="text-muted-foreground block mb-1">{t('countriesBlocked')}</label>
                        <input className="w-full rounded-lg bg-background border border-border/10 px-3 py-2 text-xs text-foreground" placeholder="CN, KP"
                          value={(rule.countries_blocked||[]).join(', ')}
                          onChange={e => toggleAdRule(rule.page, 'countries_blocked', e.target.value.split(',').map((s:string) => s.trim()).filter(Boolean))} />
                      </div>
                      <div className="col-span-2">
                        <label className="text-muted-foreground block mb-1">{t('allowedAdTypes')}</label>
                        <div className="flex gap-2 flex-wrap">
                          {['banner','interstitial','rewarded','native','video'].map(at => (
                            <button key={at} onClick={() => {
                              const current = rule.ad_types_allowed || [];
                              const next = current.includes(at) ? current.filter((x:string)=>x!==at) : [...current, at];
                              toggleAdRule(rule.page, 'ad_types_allowed', next);
                            }} className={cn("px-2 py-1 rounded-lg text-xs font-bold border", (rule.ad_types_allowed||[]).includes(at) ? "bg-primary/20 border-primary text-primary" : "bg-muted border-border/10 text-muted-foreground")}>
                              {at}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ===== GOD-MODE: DAILY CONTENT MANAGEMENT ===== */}
        {tab==='daily-content' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-foreground flex items-center gap-2"><Sparkles className="h-5 w-5 text-amber-500"/>{t('dailyContentTitle')}</h2>
              <Button onClick={() => { setDailyForm({ content_type:'hadith', title:{}, body:{}, source:{}, arabic_text:'', active:true, schedule_date:'', priority:0 }); setShowDailyForm(true); }} size="sm" className="rounded-xl gap-1"><Plus className="h-3 w-3"/>{t('addContent')}</Button>
            </div>

            {showDailyForm && (
              <div className="rounded-2xl border border-primary/30 bg-card p-4 space-y-3">
                <div className="flex gap-2 items-center">
                  <select className="rounded-lg bg-background border border-border/10 px-3 py-2 text-sm text-foreground" value={dailyForm.content_type} onChange={e => setDailyForm({...dailyForm, content_type: e.target.value})}>
                    <option value="hadith">{t('hadithType')}</option>
                    <option value="story">{t('storyType')}</option>
                    <option value="dua">{t('duaType')}</option>
                    <option value="tip">{t('tipType')}</option>
                    <option value="verse">{t('verseType')}</option>
                  </select>
                  <input type="date" className="rounded-lg bg-background border border-border/10 px-3 py-2 text-sm text-foreground" placeholder="Schedule Date" value={dailyForm.schedule_date} onChange={e => setDailyForm({...dailyForm, schedule_date: e.target.value})} />
                  <div className="flex items-center gap-1">
                    <span className="text-xs text-muted-foreground">{t('activeLabel')}</span>
                    <Switch checked={dailyForm.active} onCheckedChange={v => setDailyForm({...dailyForm, active: v})} />
                  </div>
                </div>
                <div>
                  <label className="text-xs text-muted-foreground mb-1 block">{t('arabicTextOriginal')}</label>
                  <textarea className="w-full rounded-lg bg-background border border-border/10 px-3 py-2 text-sm text-foreground h-20" dir="rtl" value={dailyForm.arabic_text} onChange={e => setDailyForm({...dailyForm, arabic_text: e.target.value})} placeholder={t('originalArabicText')} />
                </div>
                <div>
                  <div className="flex gap-1 flex-wrap mb-2">
                    {SUPPORTED_LOCALES.map(loc => (
                      <button key={loc} onClick={() => setDailyEditLang(loc)} className={cn("px-2 py-1 rounded text-xs font-bold border", dailyEditLang === loc ? "bg-primary text-primary-foreground border-primary" : "bg-muted border-border/10 text-muted-foreground")}>
                        {loc}
                      </button>
                    ))}
                  </div>
                  <div className="space-y-2">
                    <input className="w-full rounded-lg bg-background border border-border/10 px-3 py-2 text-sm text-foreground" placeholder={`Title (${dailyEditLang})`}
                      dir={dailyEditLang === 'ar' ? 'rtl' : 'ltr'}
                      value={dailyForm.title[dailyEditLang] || ''} onChange={e => setDailyForm({...dailyForm, title: {...dailyForm.title, [dailyEditLang]: e.target.value}})} />
                    <textarea className="w-full rounded-lg bg-background border border-border/10 px-3 py-2 text-sm text-foreground h-16" placeholder={`Body (${dailyEditLang})`}
                      dir={dailyEditLang === 'ar' ? 'rtl' : 'ltr'}
                      value={dailyForm.body[dailyEditLang] || ''} onChange={e => setDailyForm({...dailyForm, body: {...dailyForm.body, [dailyEditLang]: e.target.value}})} />
                    <input className="w-full rounded-lg bg-background border border-border/10 px-3 py-2 text-sm text-foreground" placeholder={`Source (${dailyEditLang})`}
                      dir={dailyEditLang === 'ar' ? 'rtl' : 'ltr'}
                      value={dailyForm.source[dailyEditLang] || ''} onChange={e => setDailyForm({...dailyForm, source: {...dailyForm.source, [dailyEditLang]: e.target.value}})} />
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button onClick={saveDailyContent} size="sm" className="rounded-xl bg-green-600 hover:bg-green-700 gap-1"><Check className="h-3 w-3"/>Save</Button>
                  <Button onClick={() => setShowDailyForm(false)} size="sm" variant="outline" className="rounded-xl gap-1"><X className="h-3 w-3"/>Cancel</Button>
                </div>
              </div>
            )}

            <div className="space-y-2">
              {dailyContentItems.length === 0 && <p className="text-sm text-muted-foreground text-center py-8">{t('noContentYet')}</p>}
              {dailyContentItems.map((item: any) => (
                <div key={item.id} className="rounded-2xl neu-card p-3 space-y-1">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={cn("px-2 py-0.5 rounded-full text-xs font-bold", item.content_type === 'hadith' ? "bg-emerald-500/20 text-emerald-400" : item.content_type === 'story' ? "bg-blue-500/20 text-blue-400" : "bg-amber-500/20 text-amber-500 dark:text-amber-400")}>
                        {item.content_type}
                      </span>
                      <span className={cn("w-2 h-2 rounded-full", item.active ? "bg-green-500" : "bg-red-500")} />
                      {item.schedule_date && <span className="text-xs text-muted-foreground">{item.schedule_date}</span>}
                    </div>
                    <div className="flex gap-1">
                      <Button size="sm" variant="ghost" className="h-7 w-7 p-0" onClick={() => { setDailyForm(item); setShowDailyForm(true); }}><Settings className="h-3 w-3"/></Button>
                      <Button size="sm" variant="ghost" className="h-7 w-7 p-0 text-red-500" onClick={() => deleteDailyContent(item.id)}><Trash2 className="h-3 w-3"/></Button>
                    </div>
                  </div>
                  <p className="text-xs text-foreground font-medium" dir="rtl">{item.arabic_text?.substring(0, 100) || item.title?.ar || item.title?.en || 'Untitled'}...</p>
                  <p className="text-xs text-muted-foreground">{t('languages')}: {Object.keys(item.title || {}).filter(k => item.title[k]).join(', ') || '-'}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ===== GOD-MODE: MULTILINGUAL PUSH NOTIFICATIONS ===== */}
        {tab==='multilingual-notif' && (
          <div className="space-y-4">
            <h2 className="text-base font-bold text-foreground flex items-center gap-2"><Send className="h-5 w-5 text-blue-500"/>{t('multilingualPushTitle')}</h2>
            <p className="text-xs text-muted-foreground">{t('multilingualPushDesc')}</p>

            <div className="rounded-2xl border border-primary/30 bg-card p-4 space-y-3">
              <div>
                <label className="text-xs font-bold text-foreground block mb-1">{t('target')}</label>
                <select className="w-full rounded-lg bg-background border border-border/10 px-3 py-2 text-sm text-foreground" value={mlNotifTarget} onChange={e => setMlNotifTarget(e.target.value)}>
                  <option value="all">{t('allUsers')}</option>
                  {SUPPORTED_LOCALES.map(loc => <option key={loc} value={`locale:${loc}`}>Locale: {loc}</option>)}
                  {['DE','TR','SA','US','GB','FR','RU','SE','NL','GR','AT'].map(c => <option key={c} value={`country:${c}`}>Country: {c}</option>)}
                </select>
              </div>

              <div className="space-y-3">
                {SUPPORTED_LOCALES.map(loc => (
                  <div key={loc} className="rounded-xl bg-muted/30 border border-border/30 p-3 space-y-2">
                    <span className="text-xs font-bold text-primary">{loc.toUpperCase()}</span>
                    <input className="w-full rounded-lg bg-background border border-border/10 px-3 py-2 text-sm text-foreground"
                      dir={loc === 'ar' ? 'rtl' : 'ltr'} placeholder={`Title (${loc})`}
                      value={mlNotifTitle[loc] || ''} onChange={e => setMlNotifTitle({...mlNotifTitle, [loc]: e.target.value})} />
                    <textarea className="w-full rounded-lg bg-background border border-border/10 px-3 py-2 text-sm text-foreground h-12"
                      dir={loc === 'ar' ? 'rtl' : 'ltr'} placeholder={`Body (${loc})`}
                      value={mlNotifBody[loc] || ''} onChange={e => setMlNotifBody({...mlNotifBody, [loc]: e.target.value})} />
                  </div>
                ))}
              </div>

              <Button onClick={sendMlNotification} className="w-full rounded-xl gap-2 bg-blue-600 hover:bg-blue-700"><Send className="h-4 w-4"/>{t('sendMultiNotif')}</Button>
            </div>

            {mlNotifHistory.length > 0 && (
              <div className="space-y-2">
                <h3 className="text-sm font-bold text-foreground">{t('historyLabel')}</h3>
                {mlNotifHistory.map((n: any, i: number) => (
                  <div key={i} className="rounded-xl neu-card p-3 text-xs space-y-1">
                    <div className="flex justify-between"><span className="font-bold text-foreground">{n.title?.ar || n.title?.en || 'Notification'}</span><span className="text-muted-foreground">{n.created_at?.substring(0,10)}</span></div>
                    <p className="text-muted-foreground">{t('target')}: {n.target} | {t('sentTo')} {n.total_sent}</p>
                    <p className="text-muted-foreground">{t('localesLabel')} {JSON.stringify(n.locale_breakdown)}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}
