import { useLocale } from '@/hooks/useLocale';
import { Link } from 'react-router-dom';
import { ArrowRight, Mail, Phone, MessageSquare, Globe, Send } from 'lucide-react';
import { toast } from 'sonner';
import { useState } from 'react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

export default function ContactUs() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);

  const handleSubmit = async () => {
    if (!name.trim() || !message.trim()) { toast.error('يرجى ملء الحقول المطلوبة'); return; }
    setSending(true);
    try {
      // Save contact form to backend
      await fetch(`${BACKEND_URL}/api/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name.trim(), email: email.trim(), message: message.trim() })
      });
      toast.success('تم إرسال رسالتك بنجاح! سنرد عليك قريباً');
      setName(''); setEmail(''); setMessage('');
    } catch {
      toast.error('خطأ في الإرسال');
    }
    setSending(false);
  };

  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="contact-page">
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center gap-3">
        <Link to="/more" className="p-2 rounded-xl bg-muted/50 active:scale-95"><ArrowRight className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">تواصل معنا</h1>
      </div>
      <div className="px-5 py-6 space-y-4">
        {/* Contact Cards */}
        <a href="mailto:mohammadalrejab@gmail.com" className="flex items-center gap-4 p-4 rounded-2xl bg-card border border-border/30 active:scale-[0.98] transition-transform">
          <div className="h-12 w-12 rounded-xl bg-red-500/10 flex items-center justify-center shrink-0">
            <Mail className="h-5 w-5 text-red-400" />
          </div>
          <div>
            <p className="text-sm font-bold text-foreground">البريد الإلكتروني</p>
            <p className="text-xs text-primary" dir="ltr">mohammadalrejab@gmail.com</p>
          </div>
        </a>
        <a href="tel:+4917684034961" className="flex items-center gap-4 p-4 rounded-2xl bg-card border border-border/30 active:scale-[0.98] transition-transform">
          <div className="h-12 w-12 rounded-xl bg-green-500/10 flex items-center justify-center shrink-0">
            <Phone className="h-5 w-5 text-green-400" />
          </div>
          <div>
            <p className="text-sm font-bold text-foreground">الهاتف / واتساب</p>
            <p className="text-xs text-primary" dir="ltr">+4917684034961</p>
          </div>
        </a>
        <a href="https://wa.me/4917684034961" target="_blank" rel="noopener noreferrer" className="flex items-center gap-4 p-4 rounded-2xl bg-card border border-border/30 active:scale-[0.98] transition-transform">
          <div className="h-12 w-12 rounded-xl bg-emerald-500/10 flex items-center justify-center shrink-0">
            <MessageSquare className="h-5 w-5 text-emerald-400" />
          </div>
          <div>
            <p className="text-sm font-bold text-foreground">واتساب مباشر</p>
            <p className="text-xs text-muted-foreground">تواصل فوري</p>
          </div>
        </a>

        {/* Contact Form */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-4">أرسل رسالة</h3>
          <div className="space-y-3">
            <input value={name} onChange={e => setName(e.target.value)} placeholder="الاسم *" dir="auto"
              className="w-full bg-muted/40 rounded-xl px-4 py-3 text-sm outline-none text-foreground border border-border/30 focus:border-primary/40" />
            <input value={email} onChange={e => setEmail(e.target.value)} placeholder="البريد الإلكتروني" dir="auto" type="email"
              className="w-full bg-muted/40 rounded-xl px-4 py-3 text-sm outline-none text-foreground border border-border/30 focus:border-primary/40" />
            <textarea value={message} onChange={e => setMessage(e.target.value)} placeholder="رسالتك *" dir="auto"
              className="w-full h-32 bg-muted/40 rounded-xl px-4 py-3 text-sm outline-none text-foreground border border-border/30 focus:border-primary/40 resize-none" />
            <button onClick={handleSubmit} disabled={sending || !name.trim() || !message.trim()}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-primary text-primary-foreground font-bold text-sm disabled:opacity-50 active:scale-[0.98] transition-transform">
              <Send className="h-4 w-4" /> {sending ? 'جاري الإرسال...' : 'إرسال'}
            </button>
          </div>
        </div>
        <p className="text-center text-xs text-muted-foreground/50 pt-2">المالك والمطور: محمد الرجب</p>
      </div>
    </div>
  );
}
