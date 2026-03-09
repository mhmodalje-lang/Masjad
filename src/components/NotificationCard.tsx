import { useState } from 'react';
import { Bell, X, Settings } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { requestNotificationPermission } from '@/hooks/useAthanNotifications';
import { toast } from 'sonner';

export default function NotificationCard() {
  const [dismissed, setDismissed] = useState(() => {
    return localStorage.getItem('notif-card-dismissed') === 'true';
  });
  const [enabled, setEnabled] = useState(() => {
    return localStorage.getItem('athan-notifications') === 'true';
  });

  if (dismissed || enabled) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        className="px-4 mb-5"
      >
        <div className="rounded-3xl bg-card border border-border/50 p-5 shadow-elevated relative overflow-hidden">
          {/* Close button */}
          <button
            onClick={() => {
              setDismissed(true);
              localStorage.setItem('notif-card-dismissed', 'true');
            }}
            className="absolute top-3 left-3 h-7 w-7 rounded-full bg-muted flex items-center justify-center"
          >
            <X className="h-3.5 w-3.5 text-muted-foreground" />
          </button>

          {/* Fake notification preview */}
          <div className="mb-4 rounded-2xl bg-muted/60 border border-border/30 p-3 flex items-start gap-3">
            <div className="h-8 w-8 rounded-lg bg-primary/15 flex items-center justify-center shrink-0 mt-0.5">
              <Bell className="h-4 w-4 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-bold text-foreground">حان وقت صلاة الظهر</p>
              <p className="text-[10px] text-muted-foreground mt-0.5">لا تفوت الصلاة في وقتها</p>
            </div>
            <span className="text-[9px] text-muted-foreground shrink-0">الآن</span>
          </div>

          <h4 className="text-sm font-bold text-foreground mb-1">إدارة الإشعارات</h4>
          <p className="text-xs text-muted-foreground mb-4">
            فعّل التنبيهات لتصلك إشعارات عند كل أذان ولا تفوت أي صلاة
          </p>

          <button
            onClick={async () => {
              const granted = await requestNotificationPermission();
              if (granted) {
                setEnabled(true);
                localStorage.setItem('athan-notifications', 'true');
                toast.success('تم تفعيل إشعارات الصلاة');
              } else {
                toast.error('لم يتم منح إذن الإشعارات');
              }
            }}
            className="w-full rounded-2xl bg-primary text-primary-foreground py-3 text-sm font-bold transition-all active:scale-[0.98] flex items-center justify-center gap-2"
          >
            <Settings className="h-4 w-4" />
            تفعيل الإشعارات
          </button>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
