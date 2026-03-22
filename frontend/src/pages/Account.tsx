import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useLocale } from '@/hooks/useLocale';
import { useNavigate } from 'react-router-dom';
import { useSmartBack } from '@/hooks/useSmartBack';
import { User, ArrowRight, ArrowLeft, Camera, Save, Loader2, Eye, EyeOff, Trash2, AlertTriangle } from 'lucide-react';
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
  const { t, dir, isRTL } = useLocale();
  const goBack = useSmartBack();
  const navigate = useNavigate();
  const fileRef = useRef<HTMLInputElement>(null);
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;
  
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [avatarUrl, setAvatarUrl] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [saving, setSaving] = useState(false);
  const [uploadingAvatar, setUploadingAvatar] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteConfirmText, setDeleteConfirmText] = useState('');
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!loading && !user) navigate('/auth', { replace: true });
  }, [user, loading, navigate]);

  useEffect(() => {
    if (user) { setName(user.name || ''); setEmail(user.email || ''); setAvatarUrl(user.avatar || ''); }
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
            toast.success(t('photoUploaded'));
          } else toast.error(t('photoUploadFailed'));
        } catch { toast.error(t('uploadError')); }
        setUploadingAvatar(false);
      };
      reader.readAsDataURL(file);
    } catch { setUploadingAvatar(false); toast.error(t('error')); }
  };

  const handleSave = async () => {
    if (!name.trim()) { toast.error(t('nameRequired')); return; }
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
        toast.success(t('changesSaved'));
        const stored = localStorage.getItem('auth_user');
        if (stored) { const u = JSON.parse(stored); u.name = name.trim(); if (avatarUrl) u.avatar = avatarUrl; localStorage.setItem('auth_user', JSON.stringify(u)); }
        if (refreshUser) refreshUser();
        setNewPassword('');
      } else toast.error(d.detail || t('saveFailed'));
    } catch { toast.error(t('connectionError')); }
    setSaving(false);
  };

  if (loading) return (<div className="min-h-screen flex items-center justify-center"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>);
  if (!user) return null;

  const handleDeleteAccount = async () => {
    if (deleteConfirmText.trim().toLowerCase() !== t('deleteWord').toLowerCase()) {
      toast.error(t('typeDeleteToConfirm'));
      return;
    }
    setDeleting(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/auth/delete-account`, {
        method: 'DELETE',
        headers: authHeaders(),
      });
      if (r.ok) {
        toast.success(t('deleteAccountSuccess'));
        signOut();
        navigate('/', { replace: true });
      } else {
        const d = await r.json();
        toast.error(d.detail || t('deleteAccountError'));
      }
    } catch {
      toast.error(t('deleteAccountError'));
    }
    setDeleting(false);
  };

  const displayAvatar = avatarUrl ? (avatarUrl.startsWith('http') ? avatarUrl : `${BACKEND_URL}${avatarUrl}`) : '';

  return (
    <div className="min-h-screen pb-28 bg-background" dir={dir} data-testid="account-page">
      <div className="sticky top-0 z-50 glass-nav bg-background/80 border-b border-border/10 px-4 h-12 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button onClick={goBack} className="p-2 rounded-xl hover:bg-muted/50"><BackArrow className="h-5 w-5 text-foreground" /></button>
          <span className="text-base font-bold">{t('editProfileTitle')}</span>
        </div>
        <button onClick={handleSave} disabled={saving} className="flex items-center gap-1 text-sm font-bold text-primary disabled:opacity-40" data-testid="save-profile-btn">
          {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
          {t('save')}
        </button>
      </div>

      <div className="flex flex-col items-center py-8 px-5">
        <div className="relative">
          <div className="h-24 w-24 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 border-[3px] border-primary/30 flex items-center justify-center overflow-hidden">
            {displayAvatar ? (<img src={displayAvatar} alt="" className="h-full w-full rounded-full object-cover" onError={() => setAvatarUrl('')} />) : (<User className="h-12 w-12 text-primary/50" />)}
            {uploadingAvatar && (<div className="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center"><Loader2 className="h-6 w-6 animate-spin text-white" /></div>)}
          </div>
          <button onClick={() => fileRef.current?.click()} className="absolute -bottom-1 -left-1 h-8 w-8 rounded-full bg-primary flex items-center justify-center border-2 border-background shadow-lg" data-testid="change-avatar-btn">
            <Camera className="h-3.5 w-3.5 text-white" />
          </button>
          <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={e => e.target.files?.[0] && handleAvatarUpload(e.target.files[0])} />
        </div>
        <p className="text-xs text-muted-foreground mt-3">{t('tapCameraToChange')}</p>
      </div>

      <div className="px-5 space-y-5">
        <div>
          <label className="text-xs font-bold text-muted-foreground mb-1.5 block">{t('fullName')}</label>
          <input type="text" dir="auto" value={name} onChange={e => setName(e.target.value)} placeholder={t('enterFullName')} data-testid="name-input"
            className="w-full h-12 rounded-2xl neu-card px-4 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-all" />
        </div>
        <div>
          <label className="text-xs font-bold text-muted-foreground mb-1.5 block">{t('email')}</label>
          <input type="email" value={email} readOnly className="w-full h-12 rounded-2xl bg-muted/50 border border-border/30 px-4 text-sm text-muted-foreground cursor-not-allowed" />
          <p className="text-[10px] text-muted-foreground mt-1">{t('emailCannotChange')}</p>
        </div>
        <div>
          <label className="text-xs font-bold text-muted-foreground mb-1.5 block">{t('newPasswordOptional')}</label>
          <div className="relative">
            <input type={showPassword ? 'text' : 'password'} dir="auto" value={newPassword} onChange={e => setNewPassword(e.target.value)} placeholder={t('leaveEmptyNoChange')} data-testid="password-input"
              className="w-full h-12 rounded-2xl neu-card px-4 pl-12 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-all" />
            <button onClick={() => setShowPassword(!showPassword)} className="absolute left-3 top-1/2 -translate-y-1/2 p-1.5 rounded-full hover:bg-muted">
              {showPassword ? <EyeOff className="h-4 w-4 text-muted-foreground" /> : <Eye className="h-4 w-4 text-muted-foreground" />}
            </button>
          </div>
          {newPassword && newPassword.length < 6 && (<p className="text-[10px] text-red-500 mt-1">{t('minSixChars')}</p>)}
        </div>
        <Button onClick={handleSave} disabled={saving} className="w-full h-12 rounded-2xl text-sm font-bold mt-6" data-testid="save-btn">
          {saving ? <Loader2 className="h-4 w-4 animate-spin ml-2" /> : null} {t('saveChanges')}
        </Button>
        <button onClick={() => { signOut(); navigate('/'); }} className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl border border-red-500/20 bg-red-500/5 text-red-500 text-sm font-bold mt-4">
          {t('logout')}
        </button>

        {/* Delete Account - Required by App Store & Play Store */}
        <button onClick={() => setShowDeleteConfirm(true)}
          className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl border border-red-600/30 bg-red-600/5 text-red-600 text-xs font-semibold mt-3 hover:bg-red-600/10 transition-colors">
          <Trash2 className="h-3.5 w-3.5" />
          {t('deleteAccount')}
        </button>
      </div>

      {/* Delete Account Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-5" onClick={() => setShowDeleteConfirm(false)}>
          <div className="bg-card rounded-2xl p-5 max-w-sm w-full border border-red-500/20 shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-red-500/10 flex items-center justify-center">
                <AlertTriangle className="h-5 w-5 text-red-500" />
              </div>
              <h3 className="text-base font-bold text-foreground">{t('deleteAccountTitle')}</h3>
            </div>
            <p className="text-sm text-muted-foreground mb-3 leading-relaxed">{t('deleteAccountConfirm')}</p>
            <p className="text-xs text-red-500/80 mb-4 bg-red-500/5 rounded-xl p-3 border border-red-500/10">
              {t('dataWillBeDeleted')}
            </p>
            <label className="text-xs font-bold text-muted-foreground mb-1.5 block">
              {t('typeDeleteToConfirm')}
            </label>
            <input
              type="text"
              dir="auto"
              value={deleteConfirmText}
              onChange={e => setDeleteConfirmText(e.target.value)}
              placeholder={t('deleteWord')}
              className="w-full h-11 rounded-xl bg-muted/30 border border-red-500/20 px-3 text-sm text-foreground placeholder:text-muted-foreground/50 outline-none focus:border-red-500/50 mb-4"
            />
            <div className="flex gap-2">
              <button onClick={() => { setShowDeleteConfirm(false); setDeleteConfirmText(''); }}
                className="flex-1 py-2.5 rounded-xl bg-muted/30 text-foreground text-sm font-bold">
                {t('cancel')}
              </button>
              <button
                onClick={handleDeleteAccount}
                disabled={deleting || deleteConfirmText.trim().toLowerCase() !== t('deleteWord').toLowerCase()}
                className="flex-1 py-2.5 rounded-xl bg-red-600 text-white text-sm font-bold disabled:opacity-30 flex items-center justify-center gap-2">
                {deleting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-3.5 w-3.5" />}
                {t('deleteAccount')}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
