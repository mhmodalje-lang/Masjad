import { useState } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { useAuth } from '@/hooks/useAuth';
import { X, Flag, AlertTriangle, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { motion } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const tk = getToken(); if (tk) h['Authorization'] = `Bearer ${tk}`;
  return h;
}

interface ReportSheetProps {
  contentId: string;
  contentType: 'post' | 'comment' | 'user' | 'story';
  reportedUserId?: string;
  onClose: () => void;
}

const REPORT_REASONS = [
  { key: 'spam', labelKey: 'reportReasonSpam', icon: '🚫' },
  { key: 'harassment', labelKey: 'reportReasonHarassment', icon: '😤' },
  { key: 'hate_speech', labelKey: 'reportReasonHateSpeech', icon: '🛑' },
  { key: 'inappropriate', labelKey: 'reportReasonInappropriate', icon: '⚠️' },
  { key: 'violence', labelKey: 'reportReasonViolence', icon: '🔴' },
  { key: 'other', labelKey: 'reportReasonOther', icon: '📝' },
];

export default function ReportSheet({ contentId, contentType, reportedUserId, onClose }: ReportSheetProps) {
  const { t, dir } = useLocale();
  const { user } = useAuth();
  const [selectedReason, setSelectedReason] = useState('');
  const [details, setDetails] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!selectedReason || !user) return;
    setSubmitting(true);
    try {
      const r = await fetch(`${BACKEND_URL}/api/report`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({
          content_id: contentId,
          content_type: contentType,
          reported_user_id: reportedUserId || '',
          reason: selectedReason,
          reason_category: selectedReason,
          details: details.trim(),
        }),
      });
      if (r.ok) {
        toast.success(t('reportSuccess'));
        onClose();
      } else {
        toast.error(t('error'));
      }
    } catch {
      toast.error(t('error'));
    }
    setSubmitting(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[80] bg-black/60 backdrop-blur-sm flex items-end justify-center"
      onClick={onClose}
    >
      <motion.div
        initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="w-full max-w-lg bg-card rounded-t-[28px] overflow-hidden border-t border-border/30 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-border/20">
          <div className="flex items-center gap-2">
            <Flag className="w-4 h-4 text-red-500" />
            <h3 className="text-foreground font-bold text-sm">{t('reportTitle')}</h3>
          </div>
          <button onClick={onClose} className="p-1.5 rounded-full bg-muted/30 hover:bg-muted/50">
            <X className="w-4 h-4 text-muted-foreground" />
          </button>
        </div>

        {/* Reasons */}
        <div className="p-4 space-y-2 max-h-[50vh] overflow-y-auto" dir={dir}>
          <p className="text-xs text-muted-foreground mb-3">{t('selectReportReason')}</p>
          {REPORT_REASONS.map(reason => (
            <button
              key={reason.key}
              onClick={() => setSelectedReason(reason.key)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border transition-all text-start ${
                selectedReason === reason.key
                  ? 'border-red-500/50 bg-red-500/10 text-foreground'
                  : 'border-border/20 bg-muted/10 text-muted-foreground hover:bg-muted/20'
              }`}
            >
              <span className="text-lg">{reason.icon}</span>
              <span className="text-sm font-medium">{t(reason.labelKey)}</span>
            </button>
          ))}

          {/* Additional details */}
          {selectedReason && (
            <div className="mt-3">
              <textarea
                value={details}
                onChange={e => setDetails(e.target.value)}
                placeholder={t('reportDetails')}
                className="w-full bg-muted/20 text-foreground rounded-xl px-4 py-3 text-sm border border-border/20 outline-none focus:border-red-500/50 resize-none h-20 placeholder:text-muted-foreground/50"
                dir="auto"
              />
            </div>
          )}
        </div>

        {/* Submit */}
        <div className="p-4 border-t border-border/20">
          <button
            onClick={handleSubmit}
            disabled={!selectedReason || submitting}
            className="w-full py-3 rounded-xl bg-red-600 text-white text-sm font-bold disabled:opacity-30 flex items-center justify-center gap-2 active:scale-95 transition-transform"
          >
            {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <AlertTriangle className="w-4 h-4" />}
            {t('reportSubmit')}
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}
