import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import {
  Heart, MessageCircle, Share2, Send, Bookmark, MoreHorizontal,
  ArrowRight, ArrowLeft, Play, Pause, Volume2, VolumeX, X,
  Reply, Trash2, Loader2, Subtitles, Maximize, RotateCw,
  Info, Eye, EyeOff, AlertTriangle, Settings, Copy,
  Download, MessageSquare, ChevronDown
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

function getToken() { return localStorage.getItem('auth_token') || ''; }
function authHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const tk = getToken(); if (tk) h['Authorization'] = `Bearer ${tk}`;
  return h;
}

function avatar(name: string, img?: string) {
  if (img) return img;
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || '?')}&background=047857&color=fff&size=80`;
}

function timeAgo(iso: string): string {
  const d = Date.now() - new Date(iso).getTime();
  const m = Math.floor(d / 60000);
  if (m < 1) return 'now';
  if (m < 60) return `${m}m`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h`;
  const days = Math.floor(h / 24);
  return `${days}d`;
}

/* Format numbers like Instagram: 23.3K, 2,097, 7.5M */
function formatCount(n: number, t: (k: string) => string): string {
  if (n >= 1000000) {
    const val = (n / 1000000).toFixed(1).replace(/\.0$/, '');
    return `${val} ${t('million')}`;
  }
  if (n >= 10000) {
    const val = (n / 1000).toFixed(1).replace(/\.0$/, '');
    return `${val} ${t('thousand')}`;
  }
  if (n >= 1000) {
    return n.toLocaleString();
  }
  return String(n);
}

/* ==================== COMMENTS SHEET ==================== */
function ReelCommentsSheet({ postId, onClose, commentsCount }: { postId: string; onClose: () => void; commentsCount: number }) {
  const { user } = useAuth();
  const { t, dir } = useLocale();
  interface Comment { id: string; author_id: string; author_name: string; author_avatar?: string; content: string; created_at: string; reply_to?: string; }
  const [comments, setComments] = useState<Comment[]>([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [replyTo, setReplyTo] = useState<Comment | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/comments`, { headers: authHeaders() })
      .then(r => r.json()).then(d => { setComments(d.comments || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [postId]);

  const submit = async () => {
    if (!text.trim() || !user) return;
    try {
      const body: any = { content: text.trim() };
      if (replyTo) body.reply_to = replyTo.id;
      const r = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/comments`, {
        method: 'POST', headers: authHeaders(), body: JSON.stringify(body),
      });
      const d = await r.json();
      if (d.comment) { setComments(prev => [...prev, d.comment]); setText(''); setReplyTo(null); }
    } catch { toast.error(t('commentFailed')); }
  };

  const deleteComment = async (cid: string) => {
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/comments/${cid}`, { method: 'DELETE', headers: authHeaders() });
      if (r.ok) { setComments(prev => prev.filter(c => c.id !== cid)); toast.success(t('deleted') || 'Deleted'); }
    } catch {}
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[70] bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="absolute bottom-0 left-0 right-0 max-h-[75vh] bg-[#262626] rounded-t-[20px] overflow-hidden flex flex-col"
        onClick={e => e.stopPropagation()}>
        {/* Handle bar */}
        <div className="flex justify-center pt-2 pb-1">
          <div className="w-10 h-1 rounded-full bg-gray-500" />
        </div>
        <div className="flex items-center justify-center px-5 py-2 border-b border-white/10">
          <h3 className="text-white font-bold text-[15px]">{t('commentsTitle')} ({commentsCount})</h3>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4" dir={dir}>
          {loading ? <div className="flex justify-center py-8"><Loader2 className="w-6 h-6 animate-spin text-gray-400" /></div>
           : comments.length === 0 ? <p className="text-center text-gray-500 py-8 text-sm">{t('beFirstToComment') || 'Be the first to comment'}</p>
           : comments.map(c => {
            const canDel = user && (c.author_id === user.id || user.email === 'mohammadalrejab@gmail.com');
            return (
              <div key={c.id} className={`flex gap-3 ${c.reply_to ? 'ms-8 border-s-2 border-gray-600 ps-3' : ''}`}>
                <img src={avatar(c.author_name, c.author_avatar)} alt="" className="w-8 h-8 rounded-full shrink-0 mt-0.5" />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] font-semibold text-white">{c.author_name}</span>
                    <span className="text-[11px] text-gray-500">{timeAgo(c.created_at)}</span>
                  </div>
                  <p className="text-white/80 text-[13px] mt-0.5 leading-relaxed">{c.content}</p>
                  <div className="flex items-center gap-4 mt-1.5">
                    <button onClick={() => { setReplyTo(c); inputRef.current?.focus(); }}
                      className="flex items-center gap-1 text-[11px] text-gray-500 hover:text-white">
                      <Reply className="w-3 h-3" /> {t('replyLabel') || 'Reply'}
                    </button>
                    {canDel && (
                      <button onClick={() => deleteComment(c.id)}
                        className="flex items-center gap-1 text-[11px] text-gray-500 hover:text-red-400">
                        <Trash2 className="w-3 h-3" /> {t('deleteLabel') || 'Delete'}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        {replyTo && (
          <div className="px-4 py-2 bg-white/5 flex items-center justify-between border-t border-white/10" dir={dir}>
            <span className="text-xs text-blue-400">{t('replyTo') || 'Reply to'} {replyTo.author_name}</span>
            <button onClick={() => setReplyTo(null)}><X className="w-3.5 h-3.5 text-gray-500" /></button>
          </div>
        )}
        {user ? (
          <div className="flex items-center gap-2 p-3 border-t border-white/10 bg-[#262626]" dir={dir}>
            <img src={avatar(user.name || '', user.avatar)} alt="" className="w-8 h-8 rounded-full shrink-0" />
            <input ref={inputRef} value={text} onChange={e => setText(e.target.value)} onKeyDown={e => e.key === 'Enter' && submit()}
              placeholder={replyTo ? `${t('replyToPlaceholder') || 'Reply to'} ${replyTo.author_name}...` : (t('writeComment') || 'Add a comment...')}
              className="flex-1 bg-transparent text-white text-sm placeholder:text-gray-500 outline-none" />
            <button onClick={submit} disabled={!text.trim()}
              className="text-blue-500 font-bold text-sm disabled:opacity-30">
              {t('sendDM') || 'Post'}
            </button>
          </div>
        ) : (
          <div className="p-4 border-t border-white/10 text-center">
            <Link to="/auth" className="text-blue-500 text-sm font-bold">{t('loginToComment') || 'Log in to comment'}</Link>
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}

/* ==================== OPTIONS BOTTOM SHEET ==================== */
function OptionsSheet({ post, onClose, onSave, saved, t, dir }: {
  post: VideoPost;
  onClose: () => void;
  onSave: () => void;
  saved: boolean;
  t: (k: string) => string;
  dir: string;
}) {
  const { user } = useAuth();
  const [autoScroll, setAutoScroll] = useState(false);
  const [showReport, setShowReport] = useState(false);
  const [reportReason, setReportReason] = useState('');
  const [showWhySee, setShowWhySee] = useState(false);

  const reportReasons = [
    { key: 'inappropriate', label: t('inappropriate') },
    { key: 'spam', label: t('spam') },
    { key: 'harassment', label: t('harassment') },
    { key: 'violence', label: t('violence') },
    { key: 'misinformation', label: t('misinformation') },
    { key: 'other', label: t('other') },
  ];

  const handleReport = async () => {
    if (!reportReason) return;
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/report`, {
        method: 'POST', headers: authHeaders(),
        body: JSON.stringify({ reason: reportReason }),
      });
      toast.success(t('reelReported'));
      onClose();
    } catch { toast.error('Error'); }
  };

  const handleNotInterested = async () => {
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/not-interested`, {
        method: 'POST', headers: authHeaders(),
      });
      toast.success(t('notInterested'));
      onClose();
    } catch {}
  };

  if (showReport) {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        className="fixed inset-0 z-[70] bg-black/60 backdrop-blur-sm" onClick={onClose}>
        <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
          transition={{ type: 'spring', damping: 28, stiffness: 350 }}
          className="absolute bottom-0 left-0 right-0 bg-[#262626] rounded-t-[20px] overflow-hidden"
          onClick={e => e.stopPropagation()}>
          <div className="flex justify-center pt-2 pb-1">
            <div className="w-10 h-1 rounded-full bg-gray-500" />
          </div>
          <div className="px-5 py-3 border-b border-white/10 text-center">
            <h3 className="text-white font-bold text-[15px]">{t('reelReport')}</h3>
          </div>
          <div className="p-4 space-y-1" dir={dir}>
            {reportReasons.map(r => (
              <button key={r.key} onClick={() => setReportReason(r.key)}
                className={`w-full text-start px-4 py-3 rounded-xl text-[14px] transition-colors ${
                  reportReason === r.key ? 'bg-white/10 text-white' : 'text-gray-300 hover:bg-white/5'
                }`}>
                {r.label}
              </button>
            ))}
          </div>
          <div className="flex gap-3 p-4 border-t border-white/10">
            <button onClick={onClose} className="flex-1 py-3 rounded-xl bg-white/10 text-white font-semibold text-sm">
              {t('cancelReport')}
            </button>
            <button onClick={handleReport} disabled={!reportReason}
              className="flex-1 py-3 rounded-xl bg-red-500 text-white font-semibold text-sm disabled:opacity-40">
              {t('confirmReport')}
            </button>
          </div>
        </motion.div>
      </motion.div>
    );
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[70] bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="absolute bottom-0 left-0 right-0 bg-[#262626] rounded-t-[20px] overflow-hidden"
        onClick={e => e.stopPropagation()}>
        {/* Handle bar */}
        <div className="flex justify-center pt-2 pb-1">
          <div className="w-10 h-1 rounded-full bg-gray-500" />
        </div>

        {/* Top action: Save only (no remix/sequence) */}
        <div className="flex justify-center gap-6 px-5 py-4 border-b border-white/10">
          <button onClick={() => { onSave(); onClose(); }} className="flex flex-col items-center gap-1.5">
            <div className="w-14 h-14 rounded-full border border-white/20 flex items-center justify-center">
              <Bookmark className={`w-6 h-6 ${saved ? 'fill-white text-white' : 'text-white'}`} />
            </div>
            <span className="text-white text-[11px]">{saved ? t('reelSaved') : t('reelSave')}</span>
          </button>
        </div>

        {/* Menu items */}
        <div className="py-2" dir={dir}>
          {/* Closed Captions */}
          <button className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-white/5 transition-colors">
            <Subtitles className="w-6 h-6 text-white" />
            <span className="text-white text-[14px] flex-1 text-start">{t('closedCaptions')}</span>
          </button>

          {/* Full Screen */}
          <button className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-white/5 transition-colors">
            <Maximize className="w-6 h-6 text-white" />
            <span className="text-white text-[14px] flex-1 text-start">{t('fullScreenMode')}</span>
          </button>

          {/* Auto Scroll */}
          <button onClick={() => {
            setAutoScroll(!autoScroll);
            // Store the preference
            localStorage.setItem('reels_auto_scroll', String(!autoScroll));
          }} className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-white/5 transition-colors">
            <RotateCw className="w-6 h-6 text-white" />
            <span className="text-white text-[14px] flex-1 text-start">{t('autoScroll')}</span>
            <span className="bg-blue-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full me-2">
              {t('newFeature')}
            </span>
            <div className={`w-11 h-6 rounded-full transition-colors relative ${autoScroll ? 'bg-blue-600' : 'bg-gray-600'}`}>
              <div className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-transform ${autoScroll ? 'translate-x-5' : 'translate-x-0.5'}`} />
            </div>
          </button>

          {/* Why seeing this */}
          <button onClick={() => setShowWhySee(!showWhySee)} className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-white/5 transition-colors">
            <Info className="w-6 h-6 text-white" />
            <span className="text-white text-[14px] flex-1 text-start">{t('whySeeThis')}</span>
          </button>
          {showWhySee && (
            <div className="px-14 pb-3 text-gray-400 text-[12px]">{t('whySeeThisDesc')}</div>
          )}

          {/* Interested */}
          <button className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-white/5 transition-colors">
            <Eye className="w-6 h-6 text-white" />
            <span className="text-white text-[14px] flex-1 text-start">{t('interested')}</span>
          </button>

          {/* Not Interested */}
          <button onClick={handleNotInterested} className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-white/5 transition-colors">
            <EyeOff className="w-6 h-6 text-white" />
            <span className="text-white text-[14px] flex-1 text-start">{t('notInterested')}</span>
          </button>

          {/* Report */}
          <button onClick={() => setShowReport(true)} className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-white/5 transition-colors">
            <AlertTriangle className="w-6 h-6 text-red-500" />
            <span className="text-red-500 text-[14px] flex-1 text-start">{t('reelReport')}</span>
          </button>

          {/* Manage Preferences */}
          <button className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-white/5 transition-colors border-t border-white/10">
            <Settings className="w-6 h-6 text-white" />
            <span className="text-white text-[14px] flex-1 text-start">{t('managePreferences')}</span>
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ==================== SHARE BOTTOM SHEET ==================== */
function ShareSheet({ post, onClose, t, dir }: {
  post: VideoPost;
  onClose: () => void;
  t: (k: string) => string;
  dir: string;
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [users, setUsers] = useState<any[]>([]);
  const [loadingUsers, setLoadingUsers] = useState(true);

  useEffect(() => {
    // Fetch trending users for sharing
    fetch(`${BACKEND_URL}/api/sohba/trending-users?limit=12`, { headers: authHeaders() })
      .then(r => r.json())
      .then(d => { setUsers(d.users || []); setLoadingUsers(false); })
      .catch(() => setLoadingUsers(false));
  }, []);

  const filteredUsers = searchQuery
    ? users.filter(u => u.name?.toLowerCase().includes(searchQuery.toLowerCase()))
    : users;

  const shareUrl = `${window.location.origin}/reels?post=${post.id}`;

  const handleCopyLink = () => {
    navigator.clipboard.writeText(shareUrl).then(() => {
      toast.success(t('linkCopied'));
    }).catch(() => {
      toast.error('Failed to copy');
    });
  };

  const handleNativeShare = () => {
    if (navigator.share) {
      navigator.share({
        title: post.author_name,
        text: post.content,
        url: shareUrl,
      }).catch(() => {});
    }
  };

  const handleWhatsApp = () => {
    window.open(`https://wa.me/?text=${encodeURIComponent(post.content + '\n' + shareUrl)}`, '_blank');
  };

  const handleFacebook = () => {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`, '_blank');
  };

  const handleMessenger = () => {
    window.open(`fb-messenger://share?link=${encodeURIComponent(shareUrl)}`, '_blank');
  };

  const handleSMS = () => {
    window.open(`sms:?body=${encodeURIComponent(post.content + '\n' + shareUrl)}`, '_blank');
  };

  const handleDownload = async () => {
    if (post.video_url) {
      const url = post.video_url.startsWith('http') ? post.video_url : `${BACKEND_URL}${post.video_url}`;
      const a = document.createElement('a');
      a.href = url;
      a.download = `reel_${post.id}.mp4`;
      a.click();
    }
    toast.success(t('downloadVideo'));
  };

  const sendToUser = async (userId: string) => {
    // Track share
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/share`, {
        method: 'POST', headers: authHeaders(),
      });
      toast.success(t('shared') || 'Sent!');
    } catch {}
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-[70] bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 350 }}
        className="absolute bottom-0 left-0 right-0 max-h-[75vh] bg-[#262626] rounded-t-[20px] overflow-hidden flex flex-col"
        onClick={e => e.stopPropagation()}>
        {/* Handle bar */}
        <div className="flex justify-center pt-2 pb-1">
          <div className="w-10 h-1 rounded-full bg-gray-500" />
        </div>

        {/* Search bar */}
        <div className="px-4 py-2" dir={dir}>
          <div className="flex items-center gap-2 bg-[#3a3a3a] rounded-xl px-3 py-2.5">
            <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder={t('searchUsers')}
              className="flex-1 bg-transparent text-white text-sm placeholder:text-gray-500 outline-none"
            />
          </div>
        </div>

        {/* Users Grid */}
        <div className="px-4 py-2 overflow-x-auto">
          {loadingUsers ? (
            <div className="flex justify-center py-6"><Loader2 className="w-5 h-5 animate-spin text-gray-400" /></div>
          ) : filteredUsers.length > 0 ? (
            <div className="grid grid-cols-3 gap-4 max-h-[200px] overflow-y-auto">
              {filteredUsers.map(u => (
                <button key={u.id} onClick={() => sendToUser(u.id)}
                  className="flex flex-col items-center gap-1.5 py-2 active:scale-95 transition-transform">
                  <div className="relative">
                    <img src={avatar(u.name, u.avatar)} alt="" className="w-14 h-14 rounded-full" />
                  </div>
                  <span className="text-white text-[11px] text-center line-clamp-1 max-w-[80px]">{u.name}</span>
                </button>
              ))}
            </div>
          ) : (
            <p className="text-center text-gray-500 py-4 text-sm">{t('noReelsYet')}</p>
          )}
        </div>

        {/* Share Actions Row 1 */}
        <div className="border-t border-white/10">
          <div className="flex overflow-x-auto gap-1 px-3 py-3 scrollbar-hide" style={{ scrollbarWidth: 'none' }}>
            {/* Add to Story */}
            <button className="flex flex-col items-center gap-1.5 min-w-[72px] py-1">
              <div className="w-14 h-14 rounded-full bg-[#3a3a3a] flex items-center justify-center">
                <svg className="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 8v8M8 12h8" />
                </svg>
              </div>
              <span className="text-white text-[10px] text-center leading-tight">{t('addToStory')}</span>
            </button>

            {/* WhatsApp */}
            <button onClick={handleWhatsApp} className="flex flex-col items-center gap-1.5 min-w-[72px] py-1">
              <div className="w-14 h-14 rounded-full bg-[#25D366] flex items-center justify-center">
                <svg className="w-7 h-7 text-white" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                </svg>
              </div>
              <span className="text-white text-[10px]">WhatsApp</span>
            </button>

            {/* Copy Link */}
            <button onClick={handleCopyLink} className="flex flex-col items-center gap-1.5 min-w-[72px] py-1">
              <div className="w-14 h-14 rounded-full bg-[#3a3a3a] flex items-center justify-center">
                <Copy className="w-6 h-6 text-white" />
              </div>
              <span className="text-white text-[10px] text-center leading-tight">{t('copyLink')}</span>
            </button>

            {/* Share */}
            <button onClick={handleNativeShare} className="flex flex-col items-center gap-1.5 min-w-[72px] py-1">
              <div className="w-14 h-14 rounded-full bg-[#3a3a3a] flex items-center justify-center">
                <Share2 className="w-6 h-6 text-white" />
              </div>
              <span className="text-white text-[10px]">{t('share')}</span>
            </button>

            {/* SMS */}
            <button onClick={handleSMS} className="flex flex-col items-center gap-1.5 min-w-[72px] py-1">
              <div className="w-14 h-14 rounded-full bg-[#3478F6] flex items-center justify-center">
                <MessageSquare className="w-6 h-6 text-white" />
              </div>
              <span className="text-white text-[10px]">SMS</span>
            </button>

            {/* Facebook */}
            <button onClick={handleFacebook} className="flex flex-col items-center gap-1.5 min-w-[72px] py-1">
              <div className="w-14 h-14 rounded-full bg-[#1877F2] flex items-center justify-center">
                <svg className="w-7 h-7 text-white" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </div>
              <span className="text-white text-[10px]">Facebook</span>
            </button>

            {/* Messenger */}
            <button onClick={handleMessenger} className="flex flex-col items-center gap-1.5 min-w-[72px] py-1">
              <div className="w-14 h-14 rounded-full bg-[#0084FF] flex items-center justify-center">
                <svg className="w-7 h-7 text-white" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0C5.373 0 0 4.974 0 11.111c0 3.498 1.744 6.614 4.469 8.654V24l4.088-2.242c1.092.301 2.246.464 3.443.464 6.627 0 12-4.975 12-11.111S18.627 0 12 0zm1.191 14.963l-3.055-3.26-5.963 3.26L10.732 8.2l3.131 3.259L19.752 8.2l-6.561 6.763z"/>
                </svg>
              </div>
              <span className="text-white text-[10px]">Messenger</span>
            </button>

            {/* Download */}
            <button onClick={handleDownload} className="flex flex-col items-center gap-1.5 min-w-[72px] py-1">
              <div className="w-14 h-14 rounded-full bg-[#3a3a3a] flex items-center justify-center">
                <Download className="w-6 h-6 text-white" />
              </div>
              <span className="text-white text-[10px]">{t('downloadVideo')}</span>
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ==================== VIDEO POST INTERFACE ==================== */
interface VideoPost {
  id: string;
  author_id: string;
  author_name: string;
  author_avatar?: string;
  content: string;
  video_url?: string;
  image_url?: string;
  thumbnail_url?: string;
  content_type: string;
  likes_count: number;
  comments_count: number;
  shares_count?: number;
  saves_count?: number;
  views_count?: number;
  liked: boolean;
  saved?: boolean;
  created_at: string;
}

/* ==================== MAIN VIDEO REELS PAGE ==================== */
export default function VideoReels() {
  const { t, dir, locale } = useLocale();
  const { user, getToken } = useAuth();
  const navigate = useNavigate();
  const [posts, setPosts] = useState<VideoPost[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [followedIds, setFollowedIds] = useState<Set<string>>(new Set());
  const [showCommentsFor, setShowCommentsFor] = useState<string | null>(null);
  const [showOptionsFor, setShowOptionsFor] = useState<string | null>(null);
  const [showShareFor, setShowShareFor] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'forYou' | 'following'>('forYou');
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchVideos();
  }, [activeTab]);

  const fetchVideos = async () => {
    try {
      setLoading(true);
      const token = getToken();
      const headers: Record<string, string> = {};
      if (token) headers.Authorization = `Bearer ${token}`;

      const res = await fetch(`${BACKEND_URL}/api/sohba/explore?limit=30`, { headers });
      const data = await res.json();
      setPosts(data.posts || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async (postId: string, index: number) => {
    if (!user) { navigate('/auth'); return; }
    const token = getToken();
    try {
      const res = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/like`, {
        method: 'POST', headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setPosts(prev => prev.map((p, i) =>
        i === index ? { ...p, liked: data.liked, likes_count: data.liked ? p.likes_count + 1 : p.likes_count - 1 } : p
      ));
    } catch (err) { console.error(err); }
  };

  const handleSave = async (postId: string, index: number) => {
    if (!user) { navigate('/auth'); return; }
    const token = getToken();
    try {
      const res = await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/save`, {
        method: 'POST', headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setPosts(prev => prev.map((p, i) =>
        i === index ? { ...p, saved: data.saved, saves_count: data.saved ? (p.saves_count || 0) + 1 : Math.max(0, (p.saves_count || 0) - 1) } : p
      ));
    } catch (err) { console.error(err); }
  };

  const handleShare = async (postId: string) => {
    const token = getToken();
    try {
      await fetch(`${BACKEND_URL}/api/sohba/posts/${postId}/share`, {
        method: 'POST', headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
    } catch (err) { console.error(err); }
  };

  const handleFollow = async (userId: string) => {
    if (!user) { navigate('/auth'); return; }
    const token = getToken();
    try {
      const r = await fetch(`${BACKEND_URL}/api/sohba/follow/${userId}`, {
        method: 'POST', headers: { Authorization: `Bearer ${token}` },
      });
      const d = await r.json();
      setFollowedIds(prev => {
        const n = new Set(prev);
        d.following ? n.add(userId) : n.delete(userId);
        return n;
      });
    } catch (err) { console.error(err); }
  };

  const getMediaUrl = (url?: string) => {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return `${BACKEND_URL}${url}`;
  };

  const handleScroll = useCallback(() => {
    if (!containerRef.current) return;
    const scrollTop = containerRef.current.scrollTop;
    const height = containerRef.current.clientHeight;
    const newIndex = Math.round(scrollTop / height);
    if (newIndex !== currentIndex && newIndex >= 0 && newIndex < posts.length) {
      setCurrentIndex(newIndex);
      // Track view
      const post = posts[newIndex];
      if (post) {
        fetch(`${BACKEND_URL}/api/sohba/posts/${post.id}/view`, {
          method: 'POST', headers: authHeaders(),
        }).catch(() => {});
      }
    }
  }, [currentIndex, posts]);

  const currentPost = posts[currentIndex];

  if (loading) {
    return (
      <div className="h-screen bg-black flex items-center justify-center">
        <div className="w-10 h-10 border-3 border-white border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (posts.length === 0) {
    return (
      <div className="h-screen bg-black flex flex-col items-center justify-center gap-4">
        <Play className="w-16 h-16 text-gray-600" />
        <p className="text-gray-400 text-lg">{t('noReelsYet')}</p>
        <button onClick={() => navigate(-1)} className="text-blue-500 font-semibold">{t('goBack') || 'Go Back'}</button>
      </div>
    );
  }

  return (
    <div className="h-screen bg-black relative overflow-hidden">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-30 flex items-center justify-between px-4 bg-gradient-to-b from-black/70 via-black/30 to-transparent"
        style={{ paddingTop: 'max(10px, env(safe-area-inset-top, 10px))', paddingBottom: '8px' }}>
        <button onClick={() => navigate(-1)} className="text-white p-1 active:scale-90 transition-transform">
          {dir === 'rtl' ? <ArrowRight className="w-5 h-5" /> : <ArrowLeft className="w-5 h-5" />}
        </button>
        <div className="flex items-center gap-4">
          <button
            onClick={() => setActiveTab('forYou')}
            className={`text-[13px] font-bold pb-0.5 transition-colors ${
              activeTab === 'forYou' ? 'text-white border-b-2 border-white' : 'text-white/50'
            }`}>
            {t('reelForYou')}
          </button>
          <button
            onClick={() => setActiveTab('following')}
            className={`text-[13px] font-bold pb-0.5 transition-colors ${
              activeTab === 'following' ? 'text-white border-b-2 border-white' : 'text-white/50'
            }`}>
            {t('reelFollowing')}
          </button>
        </div>
        <div className="w-5" />
      </div>

      {/* Reels Container */}
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className="h-full overflow-y-scroll snap-y snap-mandatory"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none', WebkitOverflowScrolling: 'touch' }}
      >
        <style>{`div::-webkit-scrollbar { display: none; }`}</style>
        {posts.map((post, index) => (
          <ReelItem
            key={post.id}
            post={post}
            index={index}
            isActive={index === currentIndex}
            onLike={() => handleLike(post.id, index)}
            onSave={() => handleSave(post.id, index)}
            onShare={() => setShowShareFor(post.id)}
            onFollow={() => handleFollow(post.author_id)}
            onComment={() => setShowCommentsFor(post.id)}
            onOptions={() => setShowOptionsFor(post.id)}
            onSendShare={() => { handleShare(post.id); setShowShareFor(post.id); }}
            getMediaUrl={getMediaUrl}
            t={t}
            dir={dir}
            followed={followedIds.has(post.author_id)}
          />
        ))}
      </div>

      {/* Comments Sheet */}
      <AnimatePresence>
        {showCommentsFor && (
          <ReelCommentsSheet
            postId={showCommentsFor}
            onClose={() => setShowCommentsFor(null)}
            commentsCount={currentPost?.comments_count || 0}
          />
        )}
      </AnimatePresence>

      {/* Options Sheet */}
      <AnimatePresence>
        {showOptionsFor && currentPost && (
          <OptionsSheet
            post={currentPost}
            onClose={() => setShowOptionsFor(null)}
            onSave={() => handleSave(currentPost.id, currentIndex)}
            saved={currentPost.saved || false}
            t={t}
            dir={dir}
          />
        )}
      </AnimatePresence>

      {/* Share Sheet */}
      <AnimatePresence>
        {showShareFor && currentPost && (
          <ShareSheet
            post={currentPost}
            onClose={() => setShowShareFor(null)}
            t={t}
            dir={dir}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

/* ==================== REEL ITEM COMPONENT ==================== */
function ReelItem({ post, index, isActive, onLike, onSave, onShare, onFollow, onComment, onOptions, onSendShare, getMediaUrl, t, dir, followed }: {
  post: VideoPost;
  index: number;
  isActive: boolean;
  onLike: () => void;
  onSave: () => void;
  onShare: () => void;
  onFollow: () => void;
  onComment: () => void;
  onOptions: () => void;
  onSendShare: () => void;
  getMediaUrl: (url?: string) => string;
  t: (key: string) => string;
  dir: string;
  followed: boolean;
}) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(true);
  const [paused, setPaused] = useState(false);
  const [liked, setLiked] = useState(post.liked);
  const [showHeart, setShowHeart] = useState(false);
  const [videoError, setVideoError] = useState(false);
  const hasVideo = !!post.video_url && !videoError;
  const lastTapRef = useRef(0);

  // Sync liked state
  useEffect(() => { setLiked(post.liked); }, [post.liked]);

  useEffect(() => {
    if (!videoRef.current) return;
    const handleError = () => { setVideoError(true); };
    videoRef.current.addEventListener('error', handleError);
    if (isActive && !videoError) {
      videoRef.current.play().catch(() => {});
      setPaused(false);
    } else {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
    }
    return () => { videoRef.current?.removeEventListener('error', handleError); };
  }, [isActive, videoError]);

  const togglePlay = () => {
    if (!videoRef.current && !hasVideo) return;
    if (videoRef.current) {
      if (videoRef.current.paused) {
        videoRef.current.play();
        setPaused(false);
      } else {
        videoRef.current.pause();
        setPaused(true);
      }
    }
  };

  // Double tap to like
  const handleTap = (e: React.MouseEvent) => {
    const now = Date.now();
    if (now - lastTapRef.current < 300) {
      // Double tap - like
      if (!post.liked) onLike();
      setShowHeart(true);
      setTimeout(() => setShowHeart(false), 800);
    } else {
      // Single tap - toggle play
      togglePlay();
    }
    lastTapRef.current = now;
  };

  return (
    <div className="h-screen w-full snap-start relative flex items-center justify-center bg-black select-none">
      {/* Background Media */}
      {post.video_url && !videoError ? (
        <video
          ref={videoRef}
          src={getMediaUrl(post.video_url)}
          poster={post.thumbnail_url ? getMediaUrl(post.thumbnail_url) : undefined}
          className="absolute inset-0 w-full h-full object-cover"
          loop
          muted={muted}
          playsInline
          preload="metadata"
          onClick={handleTap}
          onError={() => setVideoError(true)}
        />
      ) : null}

      {/* Fallback: Show thumbnail/image when video errors */}
      {(videoError || !post.video_url) && (post.thumbnail_url || post.image_url) ? (
        <div className="absolute inset-0" onClick={handleTap}>
          <img
            src={getMediaUrl(post.thumbnail_url || post.image_url)}
            alt=""
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/30" />
        </div>
      ) : null}

      {/* Fallback: gradient background when no media */}
      {!post.video_url && !post.thumbnail_url && !post.image_url && (
        <div className="absolute inset-0 bg-gradient-to-b from-[#1a1a2e] via-[#16213e] to-[#0f3460]" onClick={handleTap} />
      )}

      {/* Double-tap heart animation */}
      <AnimatePresence>
        {showHeart && (
          <motion.div
            initial={{ scale: 0, opacity: 1 }}
            animate={{ scale: 1.2, opacity: 1 }}
            exit={{ scale: 1.5, opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="absolute inset-0 flex items-center justify-center z-20 pointer-events-none"
          >
            <Heart className="w-24 h-24 text-white fill-white drop-shadow-2xl" />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Pause Indicator */}
      <AnimatePresence>
        {paused && hasVideo && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none"
          >
            <div className="w-16 h-16 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center">
              <Play className="w-8 h-8 text-white fill-white ms-1" />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Top gradient */}
      <div className="absolute top-0 left-0 right-0 h-28 bg-gradient-to-b from-black/60 to-transparent z-10 pointer-events-none" />

      {/* Bottom gradient - taller for better text readability */}
      <div className="absolute bottom-0 left-0 right-0 h-72 bg-gradient-to-t from-black/80 via-black/40 to-transparent z-10 pointer-events-none" />

      {/* ===== RIGHT SIDE ACTION BUTTONS (Instagram Reels style) ===== */}
      <div className="absolute end-2 flex flex-col items-center gap-4 z-20"
        style={{ bottom: '100px', marginBottom: 'env(safe-area-inset-bottom, 0px)' }}>

        {/* Author Avatar with gradient ring */}
        <Link to={`/social-profile/${post.author_id}`} className="relative mb-2">
          <div className="w-11 h-11 rounded-full p-[2px] bg-gradient-to-br from-[#f09433] via-[#e6683c] via-[#dc2743] via-[#cc2366] to-[#bc1888]">
            <img
              src={avatar(post.author_name, post.author_avatar)}
              alt=""
              className="w-full h-full rounded-full border-[2px] border-black object-cover"
            />
          </div>
          {!followed && (
            <button onClick={(e) => { e.preventDefault(); e.stopPropagation(); onFollow(); }}
              className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-5 h-5 bg-[#0095f6] rounded-full flex items-center justify-center border-[1.5px] border-black">
              <span className="text-white text-[12px] font-bold leading-none">+</span>
            </button>
          )}
        </Link>

        {/* Like / Heart */}
        <button onClick={onLike} className="flex flex-col items-center active:scale-90 transition-transform">
          <Heart className={`w-[26px] h-[26px] ${post.liked ? 'fill-red-500 text-red-500' : 'text-white'} drop-shadow-lg`} />
          <span className="text-white text-[11px] mt-0.5 font-bold drop-shadow">{formatCount(post.likes_count, t)}</span>
        </button>

        {/* Comments */}
        <button onClick={onComment} className="flex flex-col items-center active:scale-90 transition-transform">
          <MessageCircle className="w-[26px] h-[26px] text-white drop-shadow-lg" />
          <span className="text-white text-[11px] mt-0.5 font-bold drop-shadow">{formatCount(post.comments_count, t)}</span>
        </button>

        {/* Repost / Share arrows */}
        <button onClick={onSendShare} className="flex flex-col items-center active:scale-90 transition-transform">
          <svg className="w-[26px] h-[26px] text-white drop-shadow-lg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
            <path d="M7 17l-4-4 4-4" /><path d="M17 7l4 4-4 4" /><path d="M3 13h13a4 4 0 0 0 0-8h-1" /><path d="M21 11H8a4 4 0 0 0 0 8h1" />
          </svg>
          <span className="text-white text-[11px] mt-0.5 font-bold drop-shadow">{formatCount(post.shares_count || 0, t)}</span>
        </button>

        {/* Send / DM */}
        <button onClick={onShare} className="flex flex-col items-center active:scale-90 transition-transform">
          <Send className="w-[24px] h-[24px] text-white drop-shadow-lg" style={{ transform: dir === 'rtl' ? 'scaleX(-1)' : 'none' }} />
          <span className="text-white text-[11px] mt-0.5 font-bold drop-shadow">{formatCount(post.views_count || 0, t)}</span>
        </button>

        {/* Bookmark / Save */}
        <button onClick={onSave} className="flex flex-col items-center active:scale-90 transition-transform">
          <Bookmark className={`w-[26px] h-[26px] ${post.saved ? 'fill-white text-white' : 'text-white'} drop-shadow-lg`} />
          <span className="text-white text-[11px] mt-0.5 font-bold drop-shadow">{formatCount(post.saves_count || 0, t)}</span>
        </button>

        {/* More options (three dots) */}
        <button onClick={onOptions} className="active:scale-90 transition-transform mt-1">
          <MoreHorizontal className="w-[22px] h-[22px] text-white drop-shadow-lg" />
        </button>
      </div>

      {/* ===== BOTTOM INFO (Username + Follow + Caption) - Instagram exact layout ===== */}
      <div className="absolute bottom-0 start-0 end-14 z-20" dir={dir}
        style={{ paddingBottom: 'max(14px, env(safe-area-inset-bottom, 14px))' }}>

        {/* Username row with follow button */}
        <div className="flex items-center gap-2 px-4 mb-2">
          <Link to={`/social-profile/${post.author_id}`}
            className="flex items-center gap-2">
            <span className="text-white font-extrabold text-[15px] drop-shadow-lg">{post.author_name}</span>
          </Link>
          <span className="text-white/30 text-[12px]">•</span>
          <button onClick={onFollow}
            className={`px-3 py-0.5 rounded-md text-[13px] font-bold transition-all active:scale-95 ${
              followed
                ? 'text-white/60'
                : 'text-white'
            }`}>
            {followed ? t('following') : t('follow')}
          </button>
        </div>

        {/* Caption / Content - prominent text like Instagram */}
        <div className="px-4 mb-1.5">
          <p className="text-white text-[15px] leading-[1.6] drop-shadow-lg"
            style={{ textShadow: '0 1px 6px rgba(0,0,0,0.9)' }}>
            {post.content}
          </p>
        </div>

        {/* Audio/Music bar - like Instagram */}
        <div className="px-4">
          <div className="flex items-center gap-1.5">
            <svg className="w-3 h-3 text-white shrink-0" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
            </svg>
            <span className="text-white/80 text-[12px] truncate drop-shadow">{post.author_name} · {t('originalAudio')}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
