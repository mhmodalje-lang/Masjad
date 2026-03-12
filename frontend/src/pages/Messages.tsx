import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { Link } from 'react-router-dom';
import { Bell, MessageCircle, Users, Heart, ChevronLeft, UserPlus, Gift, Settings } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const msgTabs = [
  { key: 'notifications', label: 'الإشعارات', icon: Bell },
  { key: 'messages', label: 'الرسائل', icon: MessageCircle },
  { key: 'activity', label: 'النشاط', icon: Heart },
];

interface Notification {
  id: string;
  type: 'welcome' | 'reward' | 'follow' | 'like' | 'system';
  title: string;
  body: string;
  time: string;
  read: boolean;
  icon: string;
}

const sampleNotifications: Notification[] = [
  {
    id: '1',
    type: 'welcome',
    title: 'فريق المؤذن العالمي',
    body: 'السلام عليكم ورحمة الله وبركاته، تم إصدار مكافآتك الحصرية للمستخدمين الجدد! اجمع ذهبك اليومي الآن.',
    time: 'منذ 5 دقائق',
    read: false,
    icon: '🕌',
  },
  {
    id: '2',
    type: 'reward',
    title: 'مكافأة يومية',
    body: 'لقد حصلت على 100 ذهبية لتسجيل دخولك اليوم! استمر في سلسلة تسجيل الدخول.',
    time: 'منذ ساعة',
    read: false,
    icon: '🎁',
  },
  {
    id: '3',
    type: 'system',
    title: 'تحديث رمضان',
    body: 'ميزات جديدة لشهر رمضان! تقويم رمضان، تحديات يومية، ومسابقات قرآنية.',
    time: 'منذ يوم',
    read: true,
    icon: '🌙',
  },
  {
    id: '4',
    type: 'system',
    title: 'ليلة القدر',
    body: 'تبقى 4 أيام على ليلة القدر المباركة! لا تفوّت العشر الأواخر.',
    time: 'منذ يومين',
    read: true,
    icon: '✨',
  },
];

function NotificationItem({ notification }: { notification: Notification }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 10 }}
      animate={{ opacity: 1, x: 0 }}
      className={cn(
        'flex gap-3 p-4 border-b border-border/30 transition-colors',
        !notification.read && 'bg-primary/3'
      )}
    >
      <div className="h-11 w-11 rounded-full bg-muted/60 flex items-center justify-center text-xl shrink-0">
        {notification.icon}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-0.5">
          <p className="text-sm font-bold text-foreground truncate">{notification.title}</p>
          {!notification.read && <div className="h-2 w-2 rounded-full bg-primary shrink-0" />}
        </div>
        <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2">{notification.body}</p>
        <p className="text-[10px] text-muted-foreground/60 mt-1">{notification.time}</p>
      </div>
      <ChevronLeft className="h-4 w-4 text-muted-foreground/40 shrink-0 mt-3" />
    </motion.div>
  );
}

export default function Messages() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('notifications');
  const [notifications] = useState(sampleNotifications);

  return (
    <div className="min-h-screen pb-24" dir="rtl" data-testid="messages-page">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-card/95 backdrop-blur-xl border-b border-border/30">
        <div className="flex items-center justify-between px-4 py-3 pt-safe-header">
          <h1 className="text-lg font-bold text-foreground">الرسائل</h1>
          <Link to="/notifications" className="p-2 rounded-xl bg-muted/50">
            <Settings className="h-4.5 w-4.5 text-muted-foreground" />
          </Link>
        </div>

        {/* Tabs */}
        <div className="flex px-4 pb-2 gap-1">
          {msgTabs.map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              data-testid={`msg-tab-${tab.key}`}
              className={cn(
                'flex-1 flex items-center justify-center gap-1.5 py-2 rounded-xl text-xs font-bold transition-all',
                activeTab === tab.key
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted/40 text-muted-foreground'
              )}
            >
              <tab.icon className="h-3.5 w-3.5" />
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      {activeTab === 'notifications' && (
        <div>
          {notifications.map(n => (
            <NotificationItem key={n.id} notification={n} />
          ))}
        </div>
      )}

      {activeTab === 'messages' && (
        <div className="p-8 text-center">
          <div className="h-16 w-16 rounded-full bg-muted/30 flex items-center justify-center mx-auto mb-4">
            <MessageCircle className="h-8 w-8 text-muted-foreground/30" />
          </div>
          <p className="text-sm font-bold text-muted-foreground">لا توجد رسائل بعد</p>
          <p className="text-xs text-muted-foreground/60 mt-1">ابدأ محادثة مع أصدقائك في صُحبة</p>
          <Link
            to="/sohba"
            className="inline-flex items-center gap-2 mt-4 bg-primary text-primary-foreground px-5 py-2.5 rounded-2xl text-xs font-bold transition-all active:scale-95"
          >
            <UserPlus className="h-3.5 w-3.5" />
            ابحث عن أصدقاء
          </Link>
        </div>
      )}

      {activeTab === 'activity' && (
        <div className="p-8 text-center">
          <div className="h-16 w-16 rounded-full bg-muted/30 flex items-center justify-center mx-auto mb-4">
            <Heart className="h-8 w-8 text-muted-foreground/30" />
          </div>
          <p className="text-sm font-bold text-muted-foreground">لا يوجد نشاط جديد</p>
          <p className="text-xs text-muted-foreground/60 mt-1">عندما يتفاعل أحد مع منشوراتك ستظهر الإشعارات هنا</p>
        </div>
      )}

      {/* Friend suggestions */}
      {!user && (
        <div className="px-4 mt-4">
          <div className="rounded-3xl bg-gradient-to-br from-primary/10 to-primary/5 border border-primary/20 p-5 text-center">
            <Gift className="h-8 w-8 text-primary mx-auto mb-2" />
            <p className="text-sm font-bold text-foreground mb-1">سجّل دخولك</p>
            <p className="text-xs text-muted-foreground mb-3">للحصول على إشعارات مخصصة ورسائل من أصدقائك</p>
            <Link
              to="/auth"
              className="inline-block bg-primary text-primary-foreground px-6 py-2.5 rounded-2xl text-xs font-bold"
            >
              تسجيل الدخول
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
