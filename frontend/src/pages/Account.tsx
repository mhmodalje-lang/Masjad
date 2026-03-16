import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { User, ArrowRight, Camera, Save, Loader2, Eye, EyeOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = getToken(); if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

export default function Account() {
  const { user, loading, signOut, refreshUser } = useAuth();
  const navigate = useNavigate();
  const fileRef = useRef<HTMLInputElement>(null);
  
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [avatarUrl, setAvatarUrl] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [saving, setSaving] = useState(false);
  const [uploadingAvatar, setUploadingAvatar] = useState(false);

  useEffect(() => {
    if (!loading && !user) navigate('/auth', { replace: true });
  }, [user, loading, navigate]);

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setEmail(user.email || '');
      setAvatarUrl(user.avatar || '');
    }
  }, [user]);

  const handleAvatarUpload = async (file: File) => {
    setUploadingAvatar(true);
    try {
      const reader = new FileReader();
      reader.onload = async () => {
        try {
          const r = await fetch(`${BACKEND_URL}/api/upload/file`, {
            method: 'POST', headers: authHeaders(),
            body: JSON.stringify({ data: reader.result, filename: 'avatar.jpg' })
          });
          const d = await r.json();
          if (r.ok && d.url) {
            setAvatarUrl(d.url.startsWith('http') ? d.url : `${BACKEND_URL}${d.url}`);
            toast.success('تم رفع الصورة');
          } else toast.error('فشل رفع الصورة');
        } catch { toast.error('خطأ في الرفع'); }
        setUploadingAvatar(false);
      };
      reader.readAsDataURL(file);
    } catch { setUploadingAvatar(false); toast.error('خطأ'); }
  };

  const handleSave = async () => {
    if (!name.trim()) { toast.error('يجب كتابة الاسم'); return; }
    setSaving(true);
    try {
      const body: any = { name: name.trim() };
      if (avatarUrl) body.avatar = avatarUrl;
      if (newPassword.trim().length >= 6) body.password = newPassword;
      
      const r = await fetch(`${BACKEND_URL}/api/auth/update-profile`, {
        method: 'PUT', headers: authHeaders(), body: JSON.stringify(body)
      });
      const d = await r.json();
      if (r.ok) {
        toast.success('تم حفظ التعديلات');
        // Update local storage
        const stored = localStorage.getItem('auth_user');
        if (stored) {
          const u = JSON.parse(stored);
          u.name = name.trim();
          if (avatarUrl) u.avatar = avatarUrl;
          localStorage.setItem('auth_user', JSON.stringify(u));
        }
        if (refreshUser) refreshUser();
        setNewPassword('');
      } else toast.error(d.detail || 'فشل الحفظ');
    } catch { toast.error('خطأ في الاتصال'); }
    setSaving(false);
  };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <Loader2 className="h-8 w-8 animate-spin text-primary" />
    </div>
  );
  if (!user) return null;

  const displayAvatar = avatarUrl 
    ? (avatarUrl.startsWith('http') ? avatarUrl : `${BACKEND_URL}${avatarUrl}`)
    : '';

  return (
    <div className="min-h-screen pb-28 bg-background" dir="rtl" data-testid="account-page">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-12 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button onClick={() => navigate(-1)} className="p-2 rounded-xl hover:bg-muted/50">
            <ArrowRight className="h-5 w-5 text-foreground" />
          </button>
          <span className="text-base font-bold">تعديل الملف الشخصي</span>
        </div>
        <button onClick={handleSave} disabled={saving}
          className="flex items-center gap-1 text-sm font-bold text-primary disabled:opacity-40" data-testid="save-profile-btn">
          {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
          حفظ
        </button>
      </div>

      {/* Avatar Section */}
      <div className="flex flex-col items-center py-8 px-5">
        <div className="relative">
          <div className="h-24 w-24 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 border-[3px] border-primary/30 flex items-center justify-center overflow-hidden">
            {displayAvatar ? (
              <img src={displayAvatar} alt="" className="h-full w-full rounded-full object-cover"
                onError={() => setAvatarUrl('')} />
            ) : (
              <User className="h-12 w-12 text-primary/50" />
            )}
            {uploadingAvatar && (
              <div className="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center">
                <Loader2 className="h-6 w-6 animate-spin text-white" />
              </div>
            )}
          </div>
          <button onClick={() => fileRef.current?.click()}
            className="absolute -bottom-1 -left-1 h-8 w-8 rounded-full bg-primary flex items-center justify-center border-2 border-background shadow-lg"
            data-testid="change-avatar-btn">
            <Camera className="h-3.5 w-3.5 text-white" />
          </button>
          <input ref={fileRef} type="file" accept="image/*" className="hidden"
            onChange={e => e.target.files?.[0] && handleAvatarUpload(e.target.files[0])} />
        </div>
        <p className="text-xs text-muted-foreground mt-3">اضغط على الكاميرا لتغيير الصورة</p>
      </div>

      {/* Form Fields */}
      <div className="px-5 space-y-5">
        {/* Name */}
        <div>
          <label className="text-xs font-bold text-muted-foreground mb-1.5 block">الاسم الكامل</label>
          <input type="text" dir="auto" value={name} onChange={e => setName(e.target.value)}
            placeholder="أدخل اسمك الكامل" data-testid="name-input"
            className="w-full h-12 rounded-2xl bg-card border border-border/30 px-4 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-all"
            style={{ unicodeBidi: 'plaintext' as any }} />
        </div>

        {/* Email (read-only) */}
        <div>
          <label className="text-xs font-bold text-muted-foreground mb-1.5 block">البريد الإلكتروني</label>
          <input type="email" value={email} readOnly
            className="w-full h-12 rounded-2xl bg-muted/50 border border-border/30 px-4 text-sm text-muted-foreground cursor-not-allowed" />
          <p className="text-[10px] text-muted-foreground mt-1">لا يمكن تغيير البريد الإلكتروني</p>
        </div>

        {/* New Password */}
        <div>
          <label className="text-xs font-bold text-muted-foreground mb-1.5 block">كلمة مرور جديدة (اختياري)</label>
          <div className="relative">
            <input type={showPassword ? 'text' : 'password'} dir="auto" value={newPassword}
              onChange={e => setNewPassword(e.target.value)}
              placeholder="اترك فارغاً إذا لا تريد التغيير" data-testid="password-input"
              className="w-full h-12 rounded-2xl bg-card border border-border/30 px-4 pl-12 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-all"
              style={{ unicodeBidi: 'plaintext' as any }} />
            <button onClick={() => setShowPassword(!showPassword)}
              className="absolute left-3 top-1/2 -translate-y-1/2 p-1.5 rounded-full hover:bg-muted">
              {showPassword ? <EyeOff className="h-4 w-4 text-muted-foreground" /> : <Eye className="h-4 w-4 text-muted-foreground" />}
            </button>
          </div>
          {newPassword && newPassword.length < 6 && (
            <p className="text-[10px] text-red-500 mt-1">يجب أن تكون 6 أحرف على الأقل</p>
          )}
        </div>

        {/* Save Button */}
        <Button onClick={handleSave} disabled={saving} className="w-full h-12 rounded-2xl text-sm font-bold mt-6" data-testid="save-btn">
          {saving ? <Loader2 className="h-4 w-4 animate-spin ml-2" /> : null}
          حفظ التعديلات
        </Button>

        {/* Logout */}
        <button onClick={() => { signOut(); navigate('/'); }}
          className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl border border-red-500/20 bg-red-500/5 text-red-500 text-sm font-bold mt-4">
          تسجيل الخروج
        </button>
      </div>
    </div>
  );
}
