import { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { Link } from 'react-router-dom';
import { Bell, MessageCircle, Heart, ChevronLeft, UserPlus, Gift, Settings, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const msgTabs = [
  { key: 'notifications', label: 'الإشعارات', icon: Bell },
  { key: 'messages', label: 'الرسائل', icon: MessageCircle },
  { key: 'activity', label: 'النشاط', icon: Heart },
];

interface Notification {
  id: string; title: string; body: string; time: string; read: boolean; icon: string;
}

function getSystemNotifications(): Notification[] {
  return [
    { id: '1', title: 'مرحباً بك في المؤذن العالمي', body: 'اكتشف صُحبة — شارك لحظاتك الإيمانية مع الأمة', time: 'الآن', read: false, icon: '🕌' },
    { id: '2', title: 'لا تنسَ أذكار المساء', body: 'سبحان الله وبحمده، سبحان الله العظيم', time: 'كل يوم', read: true, icon: '🤲' },
  ];
}

function NotificationItem({ n, onDismiss }: { n: Notification; onDismiss: () => void }) {
  return (
    <motion.div initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }}
      className={cn('flex gap-3 p-4 border-b border-border/20', !n.read && 'bg-primary/3')}>
      <div className="h-11 w-11 rounded-full bg-muted/50 flex items-center justify-center text-xl shrink-0">{n.icon}</div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-0.5">
          <p className="text-sm font-bold text-foreground truncate">{n.title}</p>
          {!n.read && <div className="h-2 w-2 rounded-full bg-primary shrink-0" />}
        </div>
        <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2">{n.body}</p>
        <p className="text-[10px] text-muted-foreground/50 mt-1">{n.time}</p>
      </div>
      <button onClick={onDismiss} className="shrink-0 mt-2"><X className="h-3.5 w-3.5 text-muted-foreground/30" /></button>
    </motion.div>
  );
}

export default function Messages() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('notifications');
  const [notifications, setNotifications] = useState(getSystemNotifications);

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="messages-page">
      <div className="sticky top-0 z-40 bg-card/95 backdrop-blur-xl border-b border-border/20">
        <div className="flex items-center justify-between px-4 py-3 pt-safe-header">
          <h1 className="text-lg font-bold text-foreground">الرسائل</h1>
          <Link to="/notifications" className="p-2 rounded-xl bg-muted/50"><Settings className="h-4 w-4 text-muted-foreground" /></Link>
        </div>
        <div className="flex px-4 pb-2 gap-1">
          {msgTabs.map(tab => (
            <button key={tab.key} onClick={() => setActiveTab(tab.key)} data-testid={`msg-tab-${tab.key}`}
              className={cn('flex-1 flex items-center justify-center gap-1.5 py-2 rounded-xl text-xs font-bold transition-all',
                activeTab === tab.key ? 'bg-primary text-primary-foreground' : 'bg-muted/40 text-muted-foreground')}>
              <tab.icon className="h-3.5 w-3.5" />{tab.label}
            </button>
          ))}
        </div>
      </div>

      {activeTab === 'notifications' && (
        <div>
          {notifications.length > 0 ? notifications.map(n => (
            <NotificationItem key={n.id} n={n} onDismiss={() => setNotifications(prev => prev.filter(x => x.id !== n.id))} />
          )) : (
            <div className="p-10 text-center">
              <Bell className="h-12 w-12 text-muted-foreground/20 mx-auto mb-3" />
              <p className="text-sm font-bold text-muted-foreground">لا توجد إشعارات</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'messages' && (
        <div className="p-10 text-center">
          <MessageCircle className="h-14 w-14 text-muted-foreground/20 mx-auto mb-3" />
          <p className="text-sm font-bold text-muted-foreground">لا توجد رسائل بعد</p>
          <p className="text-xs text-muted-foreground/50 mt-1">ابدأ محادثة مع أصدقائك في صُحبة</p>
          <Link to="/sohba" className="inline-flex items-center gap-2 mt-4 bg-primary text-primary-foreground px-5 py-2.5 rounded-2xl text-xs font-bold active:scale-95 transition-transform">
            <UserPlus className="h-3.5 w-3.5" /> ابحث عن أصدقاء
          </Link>
        </div>
      )}

      {activeTab === 'activity' && (
        <div className="p-10 text-center">
          <Heart className="h-14 w-14 text-muted-foreground/20 mx-auto mb-3" />
          <p className="text-sm font-bold text-muted-foreground">لا يوجد نشاط جديد</p>
          <p className="text-xs text-muted-foreground/50 mt-1">سيظهر هنا عندما يتفاعل أحد مع منشوراتك</p>
        </div>
      )}

      {!user && (
        <div className="px-4 mt-4">
          <div className="rounded-3xl bg-primary/5 border border-primary/15 p-5 text-center">
            <Gift className="h-8 w-8 text-primary mx-auto mb-2" />
            <p className="text-sm font-bold text-foreground mb-1">سجّل دخولك</p>
            <p className="text-xs text-muted-foreground mb-3">للحصول على إشعارات ورسائل من أصدقائك</p>
            <Link to="/auth" className="inline-block bg-primary text-primary-foreground px-6 py-2.5 rounded-2xl text-xs font-bold">تسجيل الدخول</Link>
          </div>
        </div>
      )}
    </div>
  );
}
