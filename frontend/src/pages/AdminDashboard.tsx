import { useState, useEffect, useRef, useCallback, memo } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useAdmin } from '@/hooks/useAdmin';
import { useNavigate } from 'react-router-dom';
import {
  Users, Bell, Settings, BarChart3, Shield, Send, Trash2, Plus,
  ChevronLeft, ChevronRight, RefreshCw, Megaphone, AlertTriangle,
  Monitor, FileText, Clock, BookOpen, Check, X, Eye, EyeOff,
  Coins, ShoppingBag, Film, CreditCard, Building2, Store
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

  useEffect(() => { if (!adminLoading && !isAdmin && !user) navigate('/auth'); }, [isAdmin, adminLoading, user]);
  useEffect(() => { if (isAdmin) { fetchStats(); fetchSettings(); fetchAds(); fetchPages(); fetchNotifs(); fetchUserAds(); fetchBankInfo(); fetchBroadcasts(); fetchVendors(); fetchEmbedContent(); } }, [isAdmin]);
  useEffect(() => { if (isAdmin && tab === 'users') fetchUsers(usersPage); }, [isAdmin, tab, usersPage]);

  const api = async (path: string, method='GET', body?: any, useAuth=true) => {
    const opts: any = { method, headers: useAuth ? authHeaders() : {'Content-Type':'application/json'} };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${BACKEND_URL}/api${path}`, opts);
    return res.json();
  };

  async function fetchStats() { setLoading(true); try { const d = await api('/admin/stats'); setStats(d.stats); } catch {} setLoading(false); }
  async function fetchUsers(p: number) { try { const d = await api(`/admin/users?page=${p}`); setUsers(d.users||[]); setUsersTotal(d.total||0); } catch {} }
  async function fetchSettings() { try { const d = await api('/admin/settings'); setAnnouncement(d.announcement||''); setMaintenance(d.maintenance_mode||false); } catch {} }
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
    if (!embedForm.title.trim() || !embedForm.embed_url.trim()) { toast.error('العنوان والرابط مطلوبان'); return; }
    const processedUrl = buildEmbedUrl(embedForm.embed_url, embedForm.platform);
    let thumbnailUrl = embedForm.thumbnail_url;
    if (!thumbnailUrl && embedForm.platform === 'youtube') {
      const vid = extractYouTubeID(embedForm.embed_url);
      if (vid) thumbnailUrl = `https://img.youtube.com/vi/${vid}/hqdefault.jpg`;
    }
    const d = await api('/admin/embed-content','POST',{...embedForm, embed_url: processedUrl, thumbnail_url: thumbnailUrl || undefined});
    if (d.success) { toast.success('تم إضافة المحتوى المضمن'); setShowEmbedForm(false); setEmbedForm({title:'',description:'',embed_url:'',platform:'youtube',category:'general',thumbnail_url:''}); fetchEmbedContent(); }
  }
  async function deleteEmbedContent(id: string) { if(!confirm('حذف؟')) return; await api(`/admin/embed-content/${id}`,'DELETE'); toast.success('تم'); fetchEmbedContent(); }

  async function deleteUser(id: string) { if(!confirm('حذف؟')) return; await api(`/admin/users/${id}`,'DELETE'); toast.success('تم'); fetchUsers(usersPage); fetchStats(); }
  async function sendNotif() { if(!nTitle||!nBody) return toast.error('املأ الحقول'); const d = await api('/admin/send-notification','POST',{title:nTitle,body:nBody}); if(d.success) { toast.success(d.message); setNTitle(''); setNBody(''); } }
  async function saveSettings() { const d = await api('/admin/settings','PUT',{announcement,maintenance_mode:maintenance}); if(d.success) toast.success('تم الحفظ'); }
  async function saveAd() { const d = await api('/admin/ads','POST',adForm); if(d.success) { toast.success('تم حفظ الإعلان'); setShowAdForm(false); fetchAds(); } }
  async function deleteAd(id: string) { await api(`/admin/ads/${id}`,'DELETE'); toast.success('تم الحذف'); fetchAds(); }
  async function savePage() { const d = await api('/admin/pages','POST',pageForm); if(d.success) { toast.success('تم حفظ الصفحة'); setShowPageForm(false); fetchPages(); } }
  async function deletePage(id: string) { await api(`/admin/pages/${id}`,'DELETE'); toast.success('تم'); fetchPages(); }
  async function saveSchedNotif() { const d = await api('/admin/scheduled-notifications','POST',notifForm); if(d.success) { toast.success('تم'); setShowNotifForm(false); fetchNotifs(); } }
  async function deleteSchedNotif(id: string) { await api(`/admin/scheduled-notifications/${id}`,'DELETE'); toast.success('تم'); fetchNotifs(); }
  async function updateAdStatus(id: string, status: string) { await api(`/admin/user-ads/${id}`,'PUT',{status}); toast.success('تم التحديث'); fetchUserAds(); }
  async function saveBankInfo() { await api('/admin/bank-account','POST',bankForm); toast.success('تم حفظ الحساب البنكي'); }
  async function saveCommission() { await api('/admin/marketplace/commission','PUT',{commission_rate:commissionRate}); toast.success('تم'); }
  async function publishBroadcast() {
    if (!broadcastTitle.trim() || !broadcastBody.trim()) { toast.error('يجب ملء العنوان والمحتوى'); return; }
    await api('/admin/announcements','POST',{title:broadcastTitle,body:broadcastBody,type:broadcastType});
    toast.success('تم النشر للجميع!');
    setBroadcastTitle(''); setBroadcastBody(''); fetchBroadcasts();
  }
  async function deleteBroadcast(id: string) { await api(`/admin/announcements/${id}`,'DELETE'); toast.success('تم'); fetchBroadcasts(); }
  async function updateVendorStatus(id: string, status: string) { await api(`/admin/vendors/${id}`,'PUT',{status}); toast.success('تم'); fetchVendors(); }

  if (adminLoading) return <div className="min-h-screen flex items-center justify-center"><RefreshCw className="h-8 w-8 animate-spin text-primary" /></div>;
  if (!isAdmin) return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4 px-5" dir="rtl">
      <Shield className="h-16 w-16 text-primary/30" />
      <h1 className="text-xl font-bold text-foreground">لوحة الإدارة</h1>
      <p className="text-sm text-muted-foreground text-center">{user ? 'هذا الحساب ليس مسؤولاً' : 'يجب تسجيل الدخول أولاً'}</p>
      <button onClick={() => navigate(user ? '/' : '/auth')} className="rounded-xl bg-primary text-primary-foreground px-6 py-3 text-sm font-bold">{user ? 'الرئيسية' : 'تسجيل الدخول'}</button>
    </div>
  );

  const tabs = [
    { key:'overview', label:'نظرة عامة', icon:BarChart3 },
    { key:'embed', label:'محتوى مضمن', icon:Film },
    { key:'broadcast', label:'البث', icon:Megaphone },
    { key:'users', label:'المستخدمين', icon:Users },
    { key:'ads', label:'الإعلانات', icon:Monitor },
    { key:'user-ads', label:'إعلانات القنوات', icon:Film },
    { key:'vendors', label:'البائعين', icon:ShoppingBag },
    { key:'notifications', label:'الإشعارات', icon:Bell },
    { key:'pages', label:'الصفحات', icon:FileText },
    { key:'revenue', label:'الإيرادات', icon:CreditCard },
    { key:'settings', label:'الإعدادات', icon:Settings },
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
            className="w-full rounded-xl bg-muted border border-border/50 px-3 py-2 text-sm text-foreground resize-none focus:border-primary/50 focus:ring-1 focus:ring-primary/30 outline-none transition-all" />
        ) : (
          <input type="text" {...sharedProps}
            className="w-full rounded-xl bg-muted border border-border/50 px-3 py-2 text-sm text-foreground focus:border-primary/50 focus:ring-1 focus:ring-primary/30 outline-none transition-all" />
        )}
      </div>
    );
  });

  const SelectField = ({ label, value, onChange, options }: any) => (
    <div>
      <label className="text-xs font-medium text-foreground mb-1 block">{label}</label>
      <select dir="auto" value={value} onChange={e=>onChange(e.target.value)} className="w-full rounded-xl bg-muted border border-border/50 px-3 py-2 text-sm text-foreground text-right" style={{ unicodeBidi: 'plaintext' }}>
        {options.map((o:string)=><option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  );

  return (
    <div className="min-h-screen pb-28" dir="rtl" data-testid="admin-dashboard">
      <div className="bg-gradient-to-b from-primary/20 to-transparent px-5 pt-7 pb-5">
        <div className="flex items-center gap-3 mb-4">
          <div className="h-12 w-12 rounded-xl bg-primary/15 flex items-center justify-center"><Shield className="h-6 w-6 text-primary" /></div>
          <div><h1 className="text-xl font-bold text-foreground">لوحة الإدارة</h1><p className="text-xs text-muted-foreground">{user?.email}</p></div>
        </div>
        <div dir="ltr" className="w-full overflow-x-auto scrollbar-hide pb-1" style={{ WebkitOverflowScrolling: 'touch' }}>
          <div className="flex gap-2" style={{ direction: 'rtl', minWidth: 'max-content' }}>
            {tabs.map(t=>(
              <button key={t.key} onClick={()=>setTab(t.key)} data-testid={`admin-tab-${t.key}`}
                className={cn('inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all shrink-0',
                  tab===t.key ? 'bg-primary text-primary-foreground shadow-lg' : 'bg-card border border-border/50 text-muted-foreground hover:bg-muted')}
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
              {[{l:'مستخدمين',v:stats?.total_users??0,i:Users,c:'text-blue-500 bg-blue-500/10'},{l:'مشتركين',v:stats?.push_subscribers??0,i:Bell,c:'text-green-500 bg-green-500/10'},{l:'إعلانات',v:ads.length,i:Monitor,c:'text-amber-500 bg-amber-500/10'}]
              .map(s=>(
                <div key={s.l} className="rounded-2xl bg-card border border-border/50 p-4 text-center">
                  <div className={cn("h-10 w-10 rounded-xl flex items-center justify-center mx-auto mb-2",s.c)}><s.i className="h-5 w-5"/></div>
                  <p className="text-2xl font-bold text-foreground">{s.v}</p>
                  <p className="text-xs text-muted-foreground mt-1">{s.l}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ===== BROADCAST (البث) ===== */}
        {tab==='broadcast' && (
          <div className="space-y-4">
            <h2 className="text-base font-bold text-foreground">نشر إعلان عام</h2>
            <p className="text-xs text-muted-foreground">سيظهر فوراً في الصفحة الرئيسية لجميع المستخدمين</p>
            <div className="rounded-2xl bg-card border border-primary/20 p-4 space-y-3">
              <InputField label="العنوان" value={broadcastTitle} onChange={setBroadcastTitle} placeholder="عنوان الإعلان..." />
              <InputField label="المحتوى" value={broadcastBody} onChange={setBroadcastBody} placeholder="نص الإعلان..." multiline />
              <SelectField label="النوع" value={broadcastType} onChange={setBroadcastType} options={['info','warning','promo']} />
              <Button onClick={publishBroadcast} className="w-full rounded-xl gap-2" data-testid="publish-broadcast-btn">
                <Megaphone className="h-4 w-4" />نشر للجميع
              </Button>
            </div>
            
            <h3 className="text-sm font-bold text-foreground mt-4">الإعلانات النشطة ({broadcastList.length})</h3>
            {broadcastList.map(a => (
              <div key={a.id} className="rounded-xl bg-card border border-border/50 p-4 flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-foreground">{a.title}</p>
                  <p className="text-xs text-muted-foreground mt-1">{a.body}</p>
                  <p className="text-[10px] text-muted-foreground mt-1">{a.type} • {new Date(a.created_at).toLocaleDateString('ar')}</p>
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
                <h2 className="text-base font-bold text-foreground">المحتوى المضمن</h2>
                <p className="text-xs text-muted-foreground">أضف فيديوهات وصور من YouTube وأي منصة بالتضمين</p>
              </div>
              <Button onClick={() => setShowEmbedForm(true)} size="sm" className="rounded-xl gap-1 shrink-0"><Plus className="h-3.5 w-3.5" />إضافة</Button>
            </div>

            {showEmbedForm && (
              <div className="rounded-2xl bg-card border border-primary/20 p-4 space-y-3">
                <InputField label="العنوان" value={embedForm.title} onChange={(v: string) => setEmbedForm(f => ({...f, title: v}))} placeholder="عنوان المحتوى..." />
                <InputField label="الوصف" value={embedForm.description} onChange={(v: string) => setEmbedForm(f => ({...f, description: v}))} placeholder="وصف مختصر..." multiline />
                <InputField label="رابط الفيديو/المحتوى" value={embedForm.embed_url} onChange={(v: string) => setEmbedForm(f => ({...f, embed_url: v}))} placeholder="https://youtube.com/watch?v=..." />
                <SelectField label="المنصة" value={embedForm.platform} onChange={(v: string) => setEmbedForm(f => ({...f, platform: v}))} options={['youtube','dailymotion','vimeo','tiktok','instagram','other']} />
                <SelectField label="القسم" value={embedForm.category} onChange={(v: string) => setEmbedForm(f => ({...f, category: v}))} options={['general','quran','hadith','lectures','nasheed','stories','other']} />
                <InputField label="صورة مصغرة (اختياري)" value={embedForm.thumbnail_url} onChange={(v: string) => setEmbedForm(f => ({...f, thumbnail_url: v}))} placeholder="رابط الصورة المصغرة (تلقائي لـ YouTube)" />
                <div className="flex gap-2 pt-1">
                  <Button onClick={saveEmbedContent} className="flex-1 rounded-xl gap-2"><Film className="h-4 w-4" />حفظ المحتوى</Button>
                  <Button variant="outline" onClick={() => setShowEmbedForm(false)} className="rounded-xl">إلغاء</Button>
                </div>
                <p className="text-[10px] text-muted-foreground">💡 ملاحظة: استخدم التضمين (embed) لنشر محتوى من أي منصة بشكل قانوني بدون مخالفة حقوق النشر</p>
              </div>
            )}

            <h3 className="text-sm font-bold text-foreground">المحتوى المنشور ({embedContent.length})</h3>
            {embedContent.length === 0 ? (
              <p className="text-center py-8 text-muted-foreground text-sm">لا يوجد محتوى مضمن بعد</p>
            ) : (
              embedContent.map(item => (
                <div key={item.id} className="rounded-xl bg-card border border-border/50 p-4 space-y-2">
                  {item.thumbnail_url && (
                    <div className="rounded-lg overflow-hidden h-36 w-full mb-2">
                      <img src={item.thumbnail_url} alt="" className="w-full h-full object-cover" />
                    </div>
                  )}
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-foreground">{item.title}</p>
                      {item.description && <p className="text-xs text-muted-foreground mt-0.5">{item.description}</p>}
                      <p className="text-[10px] text-muted-foreground mt-1">{item.platform} • {item.category} • {item.views || 0} مشاهدة</p>
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
            <h2 className="text-base font-bold text-foreground">المستخدمين ({usersTotal})</h2>
            {users.length===0 ? <p className="text-center py-8 text-muted-foreground text-sm">لا يوجد مستخدمين</p> :
            users.map(u=>(
              <div key={u.id} className="rounded-xl bg-card border border-border/50 p-3 flex items-center justify-between">
                <div className="min-w-0 flex-1"><p className="text-sm font-bold text-foreground truncate">{u.name||'بدون اسم'}</p><p className="text-xs text-muted-foreground truncate">{u.email}</p></div>
                <button onClick={()=>deleteUser(u.id)} className="p-1.5 rounded-lg bg-destructive/10 text-destructive mr-2"><Trash2 className="h-3.5 w-3.5"/></button>
              </div>
            ))}
          </div>
        )}

        {/* ===== ADS ===== */}
        {tab==='ads' && (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <h2 className="text-base font-bold text-foreground">إدارة الإعلانات</h2>
              <button onClick={()=>{setAdForm({name:'',provider:'Google AdSense',code:'',placement:'home',ad_type:'banner',enabled:true,priority:0}); setShowAdForm(true);}}
                className="flex items-center gap-1 text-xs bg-primary text-primary-foreground px-3 py-1.5 rounded-lg"><Plus className="h-3 w-3"/>جديد</button>
            </div>

            {showAdForm && (
              <div className="rounded-xl bg-card border border-primary/30 p-3 space-y-2">
                <InputField label="اسم الإعلان" value={adForm.name} onChange={(v:string)=>setAdForm({...adForm,name:v})} placeholder="إعلان الرئيسية..." />
                <SelectField label="المنصة" value={adForm.provider} onChange={(v:string)=>setAdForm({...adForm,provider:v})} options={AD_PROVIDERS} />
                <InputField label="كود الإعلان (HTML/Script)" value={adForm.code} onChange={(v:string)=>setAdForm({...adForm,code:v})} placeholder="<script>..." multiline />
                <div className="grid grid-cols-2 gap-2">
                  <SelectField label="الموضع" value={adForm.placement} onChange={(v:string)=>setAdForm({...adForm,placement:v})} options={AD_PLACEMENTS} />
                  <SelectField label="النوع" value={adForm.ad_type} onChange={(v:string)=>setAdForm({...adForm,ad_type:v})} options={AD_TYPES} />
                </div>
                <div className="flex gap-2">
                  <Button onClick={saveAd} size="sm" className="flex-1 rounded-lg gap-1"><Check className="h-3 w-3"/>حفظ</Button>
                  <Button onClick={()=>setShowAdForm(false)} size="sm" variant="outline" className="rounded-lg"><X className="h-3 w-3"/></Button>
                </div>
              </div>
            )}

            {ads.length===0 && !showAdForm ? <p className="text-center py-8 text-muted-foreground text-sm">لا يوجد إعلانات بعد</p> :
            ads.map(ad=>(
              <div key={ad.id} className="rounded-xl bg-card border border-border/50 p-3">
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
              <p className="text-xs font-bold text-foreground mb-1">المنصات المدعومة:</p>
              <div className="flex flex-wrap gap-1">{AD_PROVIDERS.map(p=><span key={p} className="text-[10px] bg-primary/10 text-primary px-2 py-0.5 rounded-full">{p}</span>)}</div>
            </div>
          </div>
        )}

        {/* ===== NOTIFICATIONS ===== */}
        {tab==='notifications' && (
          <div className="space-y-3">
            <h2 className="text-base font-bold text-foreground">الإشعارات</h2>
            
            {/* Send instant */}
            <div className="rounded-xl bg-card border border-border/50 p-3 space-y-2">
              <p className="text-xs font-bold text-foreground">إرسال فوري</p>
              <InputField label="العنوان" value={nTitle} onChange={setNTitle} placeholder="عنوان..." />
              <InputField label="المحتوى" value={nBody} onChange={setNBody} placeholder="محتوى..." multiline />
              <Button onClick={sendNotif} size="sm" className="w-full rounded-lg gap-1"><Send className="h-3 w-3"/>إرسال</Button>
            </div>

            {/* Scheduled */}
            <div className="flex justify-between items-center">
              <p className="text-xs font-bold text-foreground">إشعارات مجدولة</p>
              <button onClick={()=>{setNotifForm({title:'',body:'',schedule_time:'',repeat:'once',enabled:true}); setShowNotifForm(true);}}
                className="flex items-center gap-1 text-[10px] bg-primary text-primary-foreground px-2 py-1 rounded"><Plus className="h-3 w-3"/>جديد</button>
            </div>

            {showNotifForm && (
              <div className="rounded-xl bg-card border border-primary/30 p-3 space-y-2">
                <InputField label="العنوان" value={notifForm.title} onChange={(v:string)=>setNotifForm({...notifForm,title:v})} placeholder="تذكير..." />
                <InputField label="المحتوى" value={notifForm.body} onChange={(v:string)=>setNotifForm({...notifForm,body:v})} placeholder="محتوى..." />
                <div className="grid grid-cols-2 gap-2">
                  <InputField label="الوقت (HH:MM)" value={notifForm.schedule_time} onChange={(v:string)=>setNotifForm({...notifForm,schedule_time:v})} placeholder="08:00" />
                  <SelectField label="التكرار" value={notifForm.repeat} onChange={(v:string)=>setNotifForm({...notifForm,repeat:v})} options={['once','daily','weekly']} />
                </div>
                <div className="flex gap-2">
                  <Button onClick={saveSchedNotif} size="sm" className="flex-1 rounded-lg gap-1"><Check className="h-3 w-3"/>حفظ</Button>
                  <Button onClick={()=>setShowNotifForm(false)} size="sm" variant="outline" className="rounded-lg"><X className="h-3 w-3"/></Button>
                </div>
              </div>
            )}

            {scheduledNotifs.map(n=>(
              <div key={n.id} className="rounded-xl bg-card border border-border/50 p-3 flex items-center justify-between">
                <div><p className="text-sm font-bold text-foreground">{n.title}</p><p className="text-[10px] text-muted-foreground">{n.schedule_time||'فوري'} • {n.repeat}</p></div>
                <button onClick={()=>deleteSchedNotif(n.id)} className="p-1 rounded-lg bg-destructive/10 text-destructive"><Trash2 className="h-3 w-3"/></button>
              </div>
            ))}
          </div>
        )}

        {/* ===== PAGES ===== */}
        {tab==='pages' && (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <h2 className="text-base font-bold text-foreground">إدارة الصفحات</h2>
              <button onClick={()=>{setPageForm({title:'',category:'',content:'',enabled:true,order:0}); setShowPageForm(true);}}
                className="flex items-center gap-1 text-xs bg-primary text-primary-foreground px-3 py-1.5 rounded-lg"><Plus className="h-3 w-3"/>صفحة جديدة</button>
            </div>

            {showPageForm && (
              <div className="rounded-xl bg-card border border-primary/30 p-3 space-y-2">
                <InputField label="عنوان الصفحة" value={pageForm.title} onChange={(v:string)=>setPageForm({...pageForm,title:v})} placeholder="رقية العين..." />
                <InputField label="الفئة" value={pageForm.category} onChange={(v:string)=>setPageForm({...pageForm,category:v})} placeholder="رقية / أذكار / ..." />
                <InputField label="المحتوى" value={pageForm.content} onChange={(v:string)=>setPageForm({...pageForm,content:v})} placeholder="محتوى الصفحة..." multiline />
                <div className="flex gap-2">
                  <Button onClick={savePage} size="sm" className="flex-1 rounded-lg gap-1"><Check className="h-3 w-3"/>حفظ</Button>
                  <Button onClick={()=>setShowPageForm(false)} size="sm" variant="outline" className="rounded-lg"><X className="h-3 w-3"/></Button>
                </div>
              </div>
            )}

            {pages.length===0 && !showPageForm ? <p className="text-center py-8 text-muted-foreground text-sm">لا يوجد صفحات مخصصة</p> :
            pages.map(p=>(
              <div key={p.id} className="rounded-xl bg-card border border-border/50 p-3 flex items-center justify-between">
                <div><p className="text-sm font-bold text-foreground">{p.title}</p><p className="text-[10px] text-muted-foreground">{p.category} • {p.enabled?'مفعّل':'معطّل'}</p></div>
                <button onClick={()=>deletePage(p.id)} className="p-1 rounded-lg bg-destructive/10 text-destructive"><Trash2 className="h-3 w-3"/></button>
              </div>
            ))}
          </div>
        )}

        {/* ===== SETTINGS ===== */}
        {tab==='settings' && (
          <div className="space-y-4">
            <h2 className="text-base font-bold text-foreground">إعدادات التطبيق</h2>
            <div className="rounded-xl bg-card border border-border/50 p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2"><AlertTriangle className="h-4 w-4 text-amber-500"/><div><p className="text-sm font-bold text-foreground">وضع الصيانة</p><p className="text-[10px] text-muted-foreground">إيقاف مؤقت</p></div></div>
                <Switch checked={maintenance} onCheckedChange={setMaintenance} />
              </div>
              <InputField label="إعلان عام" value={announcement} onChange={setAnnouncement} placeholder="رسالة للجميع..." />
              <Button onClick={saveSettings} size="sm" className="w-full rounded-xl gap-1"><Settings className="h-3 w-3"/>حفظ</Button>
            </div>
            
            {/* Admin Bank Account */}
            <h2 className="text-base font-bold text-foreground">الحساب البنكي (لاستقبال الأرباح)</h2>
            <div className="rounded-xl bg-card border border-primary/20 p-4 space-y-3">
              <InputField label="اسم البنك" value={bankForm.bank_name||''} onChange={(v:string)=>setBankForm({...bankForm,bank_name:v})} placeholder="بنك..." />
              <InputField label="صاحب الحساب" value={bankForm.account_holder||''} onChange={(v:string)=>setBankForm({...bankForm,account_holder:v})} placeholder="الاسم..." />
              <InputField label="IBAN" value={bankForm.iban||''} onChange={(v:string)=>setBankForm({...bankForm,iban:v})} placeholder="SA00..." />
              <InputField label="SWIFT" value={bankForm.swift||''} onChange={(v:string)=>setBankForm({...bankForm,swift:v})} placeholder="SWIFT..." />
              <Button onClick={saveBankInfo} size="sm" className="w-full rounded-xl gap-1"><Building2 className="h-3 w-3"/>حفظ الحساب البنكي</Button>
            </div>

            {/* Marketplace Commission */}
            <h2 className="text-base font-bold text-foreground">عمولة السوق</h2>
            <div className="rounded-xl bg-card border border-border/50 p-4 space-y-3">
              <div className="flex items-center gap-3">
                <InputField label="نسبة العمولة %" value={String(commissionRate)} onChange={(v:string)=>setCommissionRate(Number(v)||0)} placeholder="10" />
                <Button onClick={saveCommission} size="sm" className="rounded-xl mt-5">حفظ</Button>
              </div>
            </div>

            <div className="rounded-xl bg-card border border-border/50 p-4 space-y-1 text-xs text-muted-foreground">
              <p className="font-bold text-foreground text-sm">معلومات</p>
              <p>أذان وحكاية v3.0</p>
              <p>المسؤول: {user?.email}</p>
              <p>الذكاء الاصطناعي: GPT-5.2</p>
            </div>
          </div>
        )}

        {/* ===== USER ADS (إعلانات القنوات) ===== */}
        {tab==='user-ads' && (
          <div className="space-y-3">
            <h2 className="text-base font-bold text-foreground">إعلانات القنوات ({userAds.length})</h2>
            <p className="text-xs text-muted-foreground">الإعلانات المقدمة من أصحاب القنوات للمراجعة والموافقة</p>
            {userAds.length === 0 ? <p className="text-center py-8 text-muted-foreground text-sm">لا توجد إعلانات بعد</p> :
            userAds.map(ad => (
              <div key={ad.id} className="rounded-xl bg-card border border-border/50 p-4 space-y-2">
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
                    {ad.status === 'approved' ? 'موافق' : ad.status === 'rejected' ? 'مرفوض' : 'في الانتظار'}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">{ad.description}</p>
                {ad.video_url && <p className="text-[10px] text-blue-500 truncate">{ad.video_url}</p>}
                <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
                  <span>المشاهدات: {ad.views || 0}</span>
                  <span>السعر: {ad.price_credits} نقطة</span>
                </div>
                {ad.status === 'pending' && (
                  <div className="flex gap-2 pt-1">
                    <Button onClick={() => updateAdStatus(ad.id, 'approved')} size="sm" className="flex-1 rounded-xl gap-1 bg-green-600 hover:bg-green-700"><Check className="h-3 w-3"/>موافقة</Button>
                    <Button onClick={() => updateAdStatus(ad.id, 'rejected')} size="sm" variant="destructive" className="flex-1 rounded-xl gap-1"><X className="h-3 w-3"/>رفض</Button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* ===== VENDORS (البائعين) ===== */}
        {tab==='vendors' && (
          <div className="space-y-3">
            <h2 className="text-base font-bold text-foreground">طلبات البائعين ({vendors.length})</h2>
            <p className="text-xs text-muted-foreground">لا يُنشر أي منتج إلا بعد موافقتك على البائع</p>
            {vendors.length === 0 ? <p className="text-center py-8 text-muted-foreground text-sm">لا توجد طلبات</p> :
            vendors.map(v => (
              <div key={v.id} className="rounded-xl bg-card border border-border/50 p-4 space-y-2">
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
                    {v.status === 'approved' ? 'موافق' : v.status === 'rejected' ? 'مرفوض' : 'في الانتظار'}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">{v.description}</p>
                {v.iban && <p className="text-[10px] text-muted-foreground">IBAN: {v.iban}</p>}
                {v.status === 'pending' && (
                  <div className="flex gap-2 pt-1">
                    <Button onClick={() => updateVendorStatus(v.id, 'approved')} size="sm" className="flex-1 rounded-xl gap-1 bg-green-600 hover:bg-green-700"><Check className="h-3 w-3"/>موافقة</Button>
                    <Button onClick={() => updateVendorStatus(v.id, 'rejected')} size="sm" variant="destructive" className="flex-1 rounded-xl gap-1"><X className="h-3 w-3"/>رفض</Button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* ===== REVENUE (الإيرادات) ===== */}
        {tab==='revenue' && (
          <div className="space-y-4">
            <h2 className="text-base font-bold text-foreground">الإيرادات</h2>
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-2xl bg-card border border-amber-500/20 p-4 text-center">
                <Coins className="h-8 w-8 text-amber-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-foreground">{adminRevenue?.total_credits || 0}</p>
                <p className="text-xs text-muted-foreground">نقاط من الهدايا (50%)</p>
              </div>
              <div className="rounded-2xl bg-card border border-green-500/20 p-4 text-center">
                <CreditCard className="h-8 w-8 text-green-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-foreground">-</p>
                <p className="text-xs text-muted-foreground">Stripe (قريباً)</p>
              </div>
            </div>
            <div className="rounded-xl bg-muted/50 border border-border/30 p-4 text-sm text-muted-foreground">
              <p className="font-bold text-foreground mb-2">كيف يعمل نظام الإيرادات:</p>
              <ul className="space-y-1 text-xs list-disc list-inside">
                <li>عند إرسال هدية: 50% للإدارة و 50% لصانع المحتوى</li>
                <li>المستخدمون يشترون النقاط عبر Stripe</li>
                <li>أصحاب القنوات يرفعون إعلانات وتحدد الإدارة السعر</li>
                <li>عمولة السوق تُخصم تلقائياً من كل عملية بيع</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
