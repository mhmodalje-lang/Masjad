import { useState } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { Link } from 'react-router-dom';
import { ArrowRight, ArrowLeft, Trash2, Mail, CheckCircle2, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

export default function DataDeletion() {
  const { t, dir, isRTL } = useLocale();
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;
  const [email, setEmail] = useState('');
  const [reason, setReason] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) { toast.error(t('enterEmail')); return; }
    setLoading(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/data-deletion-request`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.trim(), reason: reason.trim() }),
      });
      if (res.ok) {
        setSubmitted(true);
      } else {
        const data = await res.json();
        toast.error(data.detail || t('errorOccurred'));
      }
    } catch {
      toast.error(t('connectionError'));
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen pb-24 bg-background" dir={dir}>
        <div className="sticky top-0 z-50 glass-nav bg-background/80 border-b border-border/10 px-4 h-14 flex items-center gap-3">
          <Link to="/" className="p-2 rounded-xl bg-muted/50 active:scale-95"><BackArrow className="h-5 w-5 text-foreground" /></Link>
          <h1 className="text-lg font-bold text-foreground">{t('dataDeletionTitle')}</h1>
        </div>
        <div className="px-5 py-12 text-center space-y-4 max-w-md mx-auto">
          <CheckCircle2 className="h-16 w-16 mx-auto text-emerald-500" />
          <h2 className="text-xl font-bold text-foreground">{t('dataDeletionSuccess')}</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">{t('dataDeletionSuccessMsg')}</p>
          <p className="text-xs text-muted-foreground">{t('dataDeletionTimeframe')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir}>
      <div className="sticky top-0 z-50 glass-nav bg-background/80 border-b border-border/10 px-4 h-14 flex items-center gap-3">
        <Link to="/" className="p-2 rounded-xl bg-muted/50 active:scale-95"><BackArrow className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">{t('dataDeletionTitle')}</h1>
      </div>
      <div className="px-5 py-6 space-y-5 max-w-lg mx-auto">
        <div className="rounded-2xl neu-card p-5">
          <div className="flex items-center gap-3 mb-4">
            <Trash2 className="h-8 w-8 text-red-500" />
            <div>
              <h3 className="text-base font-bold text-foreground">{t('dataDeletionTitle')}</h3>
              <p className="text-xs text-muted-foreground">{t('dataDeletionSubtitle')}</p>
            </div>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed mb-4">{t('dataDeletionDesc')}</p>

          <div className="bg-amber-500/10 border border-amber-500/20 rounded-xl p-3 mb-4">
            <p className="text-xs text-amber-600 dark:text-amber-400 font-medium">{t('dataDeletionWarning')}</p>
          </div>

          <h4 className="text-sm font-bold text-foreground mb-2">{t('dataDeletionWhatDeleted')}</h4>
          <ul className="space-y-1 text-sm text-muted-foreground mb-5">
            <li>• {t('dataDeletionItem1')}</li>
            <li>• {t('dataDeletionItem2')}</li>
            <li>• {t('dataDeletionItem3')}</li>
            <li>• {t('dataDeletionItem4')}</li>
            <li>• {t('dataDeletionItem5')}</li>
          </ul>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="rounded-2xl neu-card p-5 space-y-4">
            <div>
              <label className="text-sm font-bold text-foreground mb-2 block">{t('dataDeletionEmailLabel')}</label>
              <div className="relative">
                <Mail className="absolute end-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  type="email"
                  placeholder={t('dataDeletionEmailPlaceholder')}
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  className="pe-9 rounded-2xl h-12 bg-card"
                  required
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-bold text-foreground mb-2 block">{t('dataDeletionReasonLabel')}</label>
              <textarea
                placeholder={t('dataDeletionReasonPlaceholder')}
                value={reason}
                onChange={e => setReason(e.target.value)}
                className="w-full rounded-2xl p-3 min-h-[80px] bg-card border border-border text-sm text-foreground resize-none"
              />
            </div>
          </div>

          <Button
            type="submit"
            disabled={loading || !email.trim()}
            className="w-full rounded-2xl h-12 bg-red-600 hover:bg-red-700 text-white font-bold text-base"
          >
            {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : t('dataDeletionSubmit')}
          </Button>
        </form>

        <p className="text-[10px] text-muted-foreground text-center leading-relaxed">
          {t('dataDeletionFooter')}
        </p>
      </div>
    </div>
  );
}
