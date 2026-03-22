import { useLocale } from '@/hooks/useLocale';
import { useState, useMemo } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { Link } from 'react-router-dom';
import { Bell, MessageCircle, Heart, UserPlus, Gift, Settings, X, Sparkles, LogIn, Send } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

const heroImage = 'https://images.unsplash.com/photo-1577214407836-1f3a0604ecb2?w=1200&q=85';

interface Notification {
  id: string; titleKey: string; bodyKey: string; timeKey: string; read: boolean; icon: string;
}

function getSystemNotifications(): Notification[] {
  return [
    { id: '1', titleKey: 'welcomeAppNotif', bodyKey: 'discoverStories', timeKey: 'now', read: false, icon: '🕌' },
    { id: '2', titleKey: 'eveningAdhkarReminder', bodyKey: 'dailyDhikr', timeKey: 'every_day', read: true, icon: '🤲' },
  ];
}

function NotificationItem({ n, onDismiss, t, index }: { n: Notification; onDismiss: () => void; t: (k: string) => string; index: number }) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 12 }} 
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -40 }}
      transition={{ delay: index * 0.06 }}
      className={cn(
        'flex gap-3.5 p-4 mx-4 mb-2.5 rounded-2xl transition-all',
        !n.read ? 'glass-mystic shadow-elevated' : 'neu-card'
      )}
    >
      {/* Icon — 3D Glass Amber-Gold */}
      <div className={cn(
        'h-12 w-12 rounded-2xl flex items-center justify-center text-xl shrink-0 border transition-all',
        !n.read 
          ? 'bg-[hsl(var(--islamic-gold)/0.12)] border-[hsl(var(--islamic-gold)/0.15)] shadow-[0_0_16px_-4px_hsl(var(--islamic-gold)/0.15)]' 
          : 'bg-muted/30 border-border/10'
      )}>
        {n.icon}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <p className="text-sm font-bold text-foreground truncate">{t(n.titleKey)}</p>
          {!n.read && (
            <div className="h-2 w-2 rounded-full bg-[hsl(var(--mystic-amber))] shrink-0 animate-pulse-glow" />
          )}
        </div>
        <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2">{t(n.bodyKey)}</p>
        <p className="text-[10px] text-muted-foreground/40 mt-1.5 font-medium">{t(n.timeKey)}</p>
      </div>
      <button onClick={onDismiss} className="shrink-0 mt-1 p-1.5 rounded-lg hover:bg-muted/30 transition-colors active:scale-90">
        <X className="h-3.5 w-3.5 text-muted-foreground/30" />
      </button>
    </motion.div>
  );
}

export default function Messages() {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  const [activeTab, setActiveTab] = useState('notifications');
  const [notifications, setNotifications] = useState(getSystemNotifications);

  const msgTabs = useMemo(() => [
    { key: 'notifications', label: t('notificationsTab'), icon: Bell, count: notifications.filter(n => !n.read).length },
    { key: 'messages', label: t('messagesTab'), icon: MessageCircle, count: 0 },
    { key: 'activity', label: t('activityTab'), icon: Heart, count: 0 },
  ], [t, notifications]);

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir} data-testid="messages-page">
      
      {/* ═══ HERO IMAGE — Warm Lantern Glow ═══ */}
      <div className="relative overflow-hidden h-[200px]">
        <img 
          src={heroImage} 
          alt="" 
          className="w-full h-full object-cover animate-heroZoom"
          loading="eager"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-black/20 to-[hsl(var(--background))]" />
        
        {/* Header overlay */}
        <div className="absolute top-0 left-0 right-0 flex items-center justify-between px-5 pt-[calc(0.75rem+env(safe-area-inset-top,0px))]">
          <h1 className="text-lg font-black text-white drop-shadow-lg tracking-tight">{t('messagesTitle')}</h1>
          <Link to="/notifications" className="p-2.5 rounded-2xl bg-white/10 backdrop-blur-xl border border-white/10 hover:bg-white/15 transition-all active:scale-95">
            <Settings className="h-[18px] w-[18px] text-white/90" />
          </Link>
        </div>

        {/* Bottom curve */}
        <div className="absolute -bottom-1 left-0 right-0 h-6 rounded-t-[2rem] bg-background" />
      </div>

      {/* ═══ TAB BAR — Neumorphic Pills ═══ */}
      <div className="flex px-4 pb-4 gap-2 -mt-1">
        {msgTabs.map(tab => (
          <button 
            key={tab.key} 
            onClick={() => setActiveTab(tab.key)} 
            data-testid={`msg-tab-${tab.key}`}
            className={cn(
              'flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-2xl text-xs font-bold transition-all duration-300 relative',
              activeTab === tab.key 
                ? 'glass-mystic text-foreground shadow-float border border-primary/15' 
                : 'neu-pill text-muted-foreground hover:text-foreground'
            )}
          >
            <tab.icon className={cn('h-3.5 w-3.5', activeTab === tab.key && 'text-[hsl(var(--mystic-amber))]')} />
            {tab.label}
            {tab.count > 0 && (
              <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-[hsl(var(--mystic-amber))] text-white text-[9px] font-bold flex items-center justify-center animate-pulse-glow">
                {tab.count}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* ═══ CONTENT ═══ */}
      <AnimatePresence mode="wait">
        {activeTab === 'notifications' && (
          <motion.div key="notifs" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            {notifications.length > 0 ? notifications.map((n, i) => (
              <NotificationItem key={n.id} n={n} t={t} index={i} onDismiss={() => setNotifications(prev => prev.filter(x => x.id !== n.id))} />
            )) : (
              <EmptyState 
                icon={<Bell className="h-14 w-14 text-muted-foreground/15" />}
                title={t('noNotifications')}
              />
            )}
          </motion.div>
        )}

        {activeTab === 'messages' && (
          <motion.div key="msgs" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <EmptyState 
              icon={<MessageCircle className="h-14 w-14 text-muted-foreground/15" />}
              title={t('noMessages')}
              subtitle={t('startConversation')}
              action={
                <Link to="/stories" className="inline-flex items-center gap-2 mt-5 bg-primary text-primary-foreground px-6 py-3 rounded-2xl text-xs font-bold active:scale-95 transition-all shadow-elevated hover:shadow-float">
                  <UserPlus className="h-4 w-4" /> {t('findFriends')}
                </Link>
              }
            />
          </motion.div>
        )}

        {activeTab === 'activity' && (
          <motion.div key="activity" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <EmptyState 
              icon={<Heart className="h-14 w-14 text-muted-foreground/15" />}
              title={t('noActivity')}
              subtitle={t('activityWillAppear')}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* ═══ LOGIN CARD — Glassmorphic Centered ═══ */}
      {!user && (
        <div className="px-4 mt-6">
          <motion.div 
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-mystic rounded-3xl p-6 text-center relative overflow-hidden"
          >
            {/* Glow orbs */}
            <div className="absolute -top-8 -right-8 w-28 h-28 bg-[hsl(var(--islamic-gold)/0.06)] rounded-full blur-2xl" />
            <div className="absolute -bottom-6 -left-6 w-24 h-24 bg-[hsl(var(--islamic-green)/0.06)] rounded-full blur-2xl" />
            
            <div className="relative">
              <div className="h-16 w-16 mx-auto rounded-full bg-[hsl(var(--islamic-gold)/0.1)] border border-[hsl(var(--islamic-gold)/0.15)] flex items-center justify-center mb-4 animate-mystic-float shadow-[0_0_24px_-4px_hsl(var(--islamic-gold)/0.15)]">
                <LogIn className="h-7 w-7 text-[hsl(var(--mystic-amber))]" />
              </div>
              <p className="text-base font-bold text-foreground mb-1.5">{t('loginPromptTitle')}</p>
              <p className="text-xs text-muted-foreground mb-5 leading-relaxed max-w-[240px] mx-auto">{t('loginPromptDesc')}</p>
              <Link 
                to="/auth" 
                className="inline-flex items-center gap-2 bg-gradient-to-r from-[hsl(var(--mystic-moss))] to-[hsl(var(--islamic-emerald))] text-white px-8 py-3 rounded-2xl text-sm font-bold active:scale-95 transition-all shadow-[0_6px_24px_-6px_hsl(var(--islamic-green)/0.4)] hover:shadow-[0_8px_32px_-6px_hsl(var(--islamic-green)/0.5)]"
              >
                <Send className="h-4 w-4" /> {t('loginAction')}
              </Link>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
}

function EmptyState({ icon, title, subtitle, action }: { icon: React.ReactNode; title: string; subtitle?: string; action?: React.ReactNode }) {
  return (
    <div className="px-4 py-12 text-center">
      <div className="mx-auto mb-4 h-20 w-20 rounded-full glass-mystic flex items-center justify-center animate-mystic-float">
        {icon}
      </div>
      <p className="text-sm font-bold text-muted-foreground">{title}</p>
      {subtitle && <p className="text-xs text-muted-foreground/50 mt-1.5 max-w-[200px] mx-auto">{subtitle}</p>}
      {action}
    </div>
  );
}
