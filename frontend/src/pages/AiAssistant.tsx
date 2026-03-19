import { useLocale } from '@/hooks/useLocale';
import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { Send, Bot, User, Loader2, Lock, Coins, Film, ArrowRight, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { Link } from 'react-router-dom';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function AiAssistant() {
  const { t, dir, isRTL } = useLocale();
  const { user, getToken } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [remaining, setRemaining] = useState(20);
  const [freeRemaining, setFreeRemaining] = useState(5);
  const [sessionId] = useState(() => crypto.randomUUID());
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  const sampleQuestions = [t('sampleQ1'), t('sampleQ2'), t('sampleQ3'), t('sampleQ4')];

  const ask = async () => {
    if (!input.trim() || loading) return;
    if (!user) { toast.error(t('loginFirstMsg')); return; }

    const q = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: q }]);
    setLoading(true);

    try {
      const res = await fetch(`${BACKEND_URL}/api/ai/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` },
        body: JSON.stringify({ question: q, session_id: sessionId }),
      });
      const data = await res.json();

      if (data.error === 'daily_limit') {
        toast.error(data.message);
        setRemaining(0);
      } else if (data.error === 'no_credits') {
        toast.error(data.message);
      } else if (data.answer) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
        if (data.remaining !== undefined) setRemaining(data.remaining);
        if (data.free_remaining !== undefined) setFreeRemaining(data.free_remaining);
      }
    } catch {
      toast.error(t('connectionError'));
    }
    setLoading(false);
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center pb-24" dir={dir} data-testid="ai-assistant-page">
        <div className="text-center px-8">
          <Bot className="h-14 w-14 mx-auto mb-4 text-primary" />
          <h2 className="text-xl font-bold text-foreground mb-2">{t('aiAssistantTitle')}</h2>
          <p className="text-sm text-muted-foreground mb-6">{t('aiAssistantDesc')}</p>
          <Link to="/auth"><Button data-testid="ai-login-btn">{t('loginBtn')}</Button></Link>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen" dir={dir} data-testid="ai-assistant-page">
      <div className="bg-gradient-to-b from-primary/15 to-transparent px-5 pt-safe-header-compact pb-3 shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-primary/15 flex items-center justify-center">
              <Bot className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h1 className="text-base font-bold text-foreground">{t('aiAssistantTitle')}</h1>
              <p className="text-[10px] text-muted-foreground">{t('poweredByGPT')}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="text-[10px] bg-muted rounded-full px-2.5 py-1 text-muted-foreground">
              {freeRemaining > 0 ? t('freeRemaining').replace('{count}', String(freeRemaining)) : <span className="flex items-center gap-1"><Coins className="h-3 w-3" />{t('perQuestion')}</span>}
            </div>
            <div className="text-[10px] bg-primary/10 rounded-full px-2.5 py-1 text-primary font-bold">
              {remaining} {t('remainingLabel')}
            </div>
          </div>
        </div>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
        {messages.length === 0 && (
          <div className="text-center py-16">
            <Bot className="h-16 w-16 mx-auto mb-4 text-primary/20" />
            <p className="text-lg font-bold text-foreground mb-2">{t('bismillah')}</p>
            <p className="text-sm text-muted-foreground mb-6">{t('askMeAnything')}</p>
            <div className="grid grid-cols-2 gap-2 max-w-sm mx-auto">
              {sampleQuestions.map(q => (
                <button key={q} onClick={() => { setInput(q); }} className="text-xs bg-muted/50 border border-border/30 rounded-xl px-3 py-2.5 text-start text-muted-foreground hover:bg-primary/5 hover:text-primary transition-colors">
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              className={cn('flex gap-2.5 max-w-[90%]', msg.role === 'user' ? (isRTL ? 'ml-auto flex-row-reverse' : 'mr-auto flex-row-reverse') : (isRTL ? 'mr-auto' : 'ml-auto'))}>
              <div className={cn('h-7 w-7 rounded-lg flex items-center justify-center shrink-0 mt-1',
                msg.role === 'user' ? 'bg-primary/15' : 'bg-accent/15')}>
                {msg.role === 'user' ? <User className="h-3.5 w-3.5 text-primary" /> : <Bot className="h-3.5 w-3.5 text-accent" />}
              </div>
              <div className={cn('rounded-2xl px-4 py-3 text-sm leading-relaxed',
                msg.role === 'user' ? 'bg-primary text-primary-foreground rounded-tr-sm' : 'bg-card border border-border/30 text-foreground rounded-tl-sm')}>
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <div className={cn("flex gap-2.5", isRTL ? "mr-auto" : "ml-auto")}>
            <div className="h-7 w-7 rounded-lg bg-accent/15 flex items-center justify-center shrink-0">
              <Bot className="h-3.5 w-3.5 text-accent" />
            </div>
            <div className="bg-card border border-border/30 rounded-2xl rounded-tl-sm px-4 py-3">
              <div className="flex gap-1">
                <span className="h-2 w-2 bg-muted-foreground/30 rounded-full animate-bounce" style={{animationDelay:'0ms'}} />
                <span className="h-2 w-2 bg-muted-foreground/30 rounded-full animate-bounce" style={{animationDelay:'150ms'}} />
                <span className="h-2 w-2 bg-muted-foreground/30 rounded-full animate-bounce" style={{animationDelay:'300ms'}} />
              </div>
            </div>
          </div>
        )}
      </div>

      {freeRemaining <= 0 && (
        <div className="px-4 py-2 shrink-0">
          <Link to="/rewards" className="flex items-center gap-2 bg-amber-500/10 border border-amber-500/20 rounded-xl px-3 py-2 text-xs text-amber-600">
            <Film className="h-3.5 w-3.5" />
            <span>{t('watchVideosForPoints')}</span>
            {isRTL ? <ArrowLeft className="h-3 w-3 ms-auto" /> : <ArrowRight className="h-3 w-3 ms-auto" />}
          </Link>
        </div>
      )}

      <div className="px-4 pb-safe pt-2 bg-card/80 backdrop-blur-xl border-t border-border/20 shrink-0">
        <div className="flex items-center gap-2">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && ask()}
            placeholder={t('writeYourQuestion')}
            className="flex-1 bg-muted/50 border border-border/30 rounded-xl px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/40"
            disabled={loading || remaining <= 0}
            data-testid="ai-input"
          />
          <Button size="icon" onClick={ask} disabled={!input.trim() || loading || remaining <= 0}
            className="rounded-xl h-10 w-10 shrink-0" data-testid="ai-send-btn">
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </Button>
        </div>
      </div>
    </div>
  );
}
