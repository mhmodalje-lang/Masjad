import { useState, useEffect } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { Link } from 'react-router-dom';
import { useSmartBack } from '@/hooks/useSmartBack';
import { ArrowRight, ArrowLeft, Heart, Plus, Send, Loader2, AlertTriangle, User, MessageSquare, X } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = localStorage.getItem('auth_token') || ''; if (t) h['Authorization'] = `Bearer ${t}`;
  return h;
}

interface DonationRequest {
  id: string; user_name?: string; author_name?: string; title: string; description: string;
  contact_info: string; contact_method?: string; amount_needed?: string; created_at: string; category: string;
  views_count?: number; status?: string;
}

export default function Donations() {
  const { t, dir, isRTL, locale } = useLocale();
  const { user } = useAuth();
  const goBack = useSmartBack();
  const [requests, setRequests] = useState<DonationRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/donation-requests/list`)
      .then(r => r.json())
      .then(d => { setRequests(d.requests || []); setLoading(false); })
      .catch(() => {
        fetch(`${BACKEND_URL}/api/donations/list`)
          .then(r => r.json())
          .then(d => { setRequests(d.donations || []); setLoading(false); })
          .catch(() => setLoading(false));
      });
  }, []);

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir} data-testid="donations-page">
      <div className="sticky top-0 z-50 glass-nav bg-background/80 border-b border-border/10 px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button onClick={goBack} className="p-2 rounded-xl bg-muted/50 active:scale-95"><BackArrow className="h-5 w-5 text-foreground" /></button>
          <h1 className="text-lg font-bold text-foreground flex items-center gap-2"><Heart className="h-5 w-5 text-red-500 dark:text-red-400" />{t('donationsTitle')}</h1>
        </div>
        {user && <button onClick={() => setShowCreate(true)} className="flex items-center gap-1.5 px-3 py-2 rounded-full bg-primary text-primary-foreground text-xs font-bold active:scale-95">
          <Plus className="h-3.5 w-3.5" />{t('requestHelp')}
        </button>}
      </div>

      <div className="mx-4 mt-4 rounded-2xl bg-amber-500/10 border border-amber-500/20 p-4">
        <div className="flex items-start gap-2">
          <AlertTriangle className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-bold text-foreground">{t('importantNotice')}</p>
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{t('donationsDisclaimer')}</p>
          </div>
        </div>
      </div>

      <div className="px-4 py-4">
        {loading ? (
          <div className="flex justify-center py-16"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>
        ) : requests.length === 0 ? (
          <div className="text-center py-16">
            <Heart className="h-16 w-16 text-muted-foreground/15 mx-auto mb-4" />
            <p className="text-base font-bold text-muted-foreground/50">{t('noRequestsNow')}</p>
            <p className="text-xs text-muted-foreground/30 mt-1">{t('beFirstToPost')}</p>
          </div>
        ) : (
          <div className="space-y-3">
            {requests.map(r => (
              <div key={r.id} className="rounded-2xl neu-card p-4">
                <div className="flex items-center gap-2 mb-2">
                  <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center"><User className="h-4 w-4 text-primary" /></div>
                  <span className="text-sm font-bold text-foreground">{r.user_name || r.author_name || t('anonymous')}</span>
                  <span className={cn("text-[10px] text-muted-foreground", isRTL ? "mr-auto" : "ml-auto")}>{new Date(r.created_at).toLocaleDateString(locale)}</span>
                </div>
                <h3 className="text-[15px] font-bold text-foreground mb-1">{r.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{r.description}</p>
                {r.amount_needed && <p className="text-sm font-bold text-primary mt-2">{t('amountNeeded')}: {r.amount_needed}</p>}
                <div className="mt-3 pt-3 border-t border-border/20">
                  <a href={`mailto:${r.contact_info}`} className="flex items-center gap-2 text-xs text-primary font-bold">
                    <MessageSquare className="h-3.5 w-3.5" />{t('contactInfo')}: {r.contact_info}
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <AnimatePresence>
        {showCreate && <CreateDonationSheet onClose={() => setShowCreate(false)} onCreated={d => setRequests(p => [d, ...p])} />}
      </AnimatePresence>
    </div>
  );
}

function CreateDonationSheet({ onClose, onCreated }: { onClose: () => void; onCreated: (d: DonationRequest) => void }) {
  const { t, dir } = useLocale();
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [contact, setContact] = useState('');
  const [amount, setAmount] = useState('');
  const [posting, setPosting] = useState(false);

  const submit = async () => {
    if (!title.trim() || !desc.trim() || !contact.trim()) { toast.error(t('fillAllFields')); return; }
    setPosting(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/donation-requests/create`, {
        method: 'POST', headers: authHeaders(),
        body: JSON.stringify({ title: title.trim(), description: desc.trim(), contact_info: contact.trim(), amount_needed: amount.trim() })
      });
      const d = await r.json();
      if (d.request) { onCreated(d.request); toast.success(t('requestPublished')); onClose(); }
    } catch { toast.error(t('errorOccurred')); }
    setPosting(false);
  };

  return (
    <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="fixed inset-0 z-[999] flex flex-col" dir={dir}>
      <div className="flex-1 bg-black/60" onClick={onClose} />
      <div className="bg-card rounded-t-3xl max-h-[85vh] flex flex-col border-t border-primary/20">
        <div className="flex items-center justify-between p-4 border-b border-border/20">
          <button onClick={onClose} className="text-sm text-muted-foreground">{t('cancelBtn')}</button>
          <h3 className="text-sm font-bold">{t('requestHelp')}</h3>
          <button onClick={submit} disabled={posting} className="text-sm font-bold text-primary disabled:opacity-40">
            {posting ? <Loader2 className="h-4 w-4 animate-spin" /> : t('publishBtn')}
          </button>
        </div>
        <div className="p-4 space-y-3 overflow-y-auto">
          <input value={title} onChange={e => setTitle(e.target.value)} placeholder={t('requestTitlePlaceholder')} dir="auto"
            className="w-full bg-muted/40 rounded-xl px-4 py-3 text-sm outline-none text-foreground border border-border/30" />
          <textarea value={desc} onChange={e => setDesc(e.target.value)} placeholder={t('requestDescPlaceholder')} dir="auto"
            className="w-full h-28 bg-muted/40 rounded-xl px-4 py-3 text-sm outline-none text-foreground border border-border/30 resize-none" />
          <input value={contact} onChange={e => setContact(e.target.value)} placeholder={t('contactInfoPlaceholder')} dir="auto"
            className="w-full bg-muted/40 rounded-xl px-4 py-3 text-sm outline-none text-foreground border border-border/30" />
          <input value={amount} onChange={e => setAmount(e.target.value)} placeholder={t('amountPlaceholder')} dir="auto"
            className="w-full bg-muted/40 rounded-xl px-4 py-3 text-sm outline-none text-foreground border border-border/30" />
        </div>
      </div>
    </motion.div>
  );
}
