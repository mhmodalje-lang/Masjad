import React, { useState, useRef, useEffect } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';
import { Send, Bot, User, Sparkles, Loader2, BookOpen, RotateCcw } from 'lucide-react';

const API_BASE = (import.meta as any).env?.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL || '';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

type AIMode = 'quran-helper' | 'arabic-tutor' | 'islamic-qa' | 'story-generator';

interface AIChatProps {
  mode: AIMode;
}

const MODE_CONFIG: Record<AIMode, {
  titleAr: string;
  titleEn: string;
  descAr: string;
  descEn: string;
  emoji: string;
  color: string;
  border: string;
  placeholderAr: string;
  placeholderEn: string;
  suggestionsAr: string[];
  suggestionsEn: string[];
}> = {
  'quran-helper': {
    titleAr: 'معلم القرآن الذكي',
    titleEn: 'AI Quran Teacher',
    descAr: 'اسألني عن أي سورة أو آية - أساعدك في الحفظ والتسميع',
    descEn: 'Ask me about any surah or ayah - I help with memorization',
    emoji: '📖',
    color: 'from-green-500/20 to-emerald-500/10',
    border: 'border-green-400/30',
    placeholderAr: 'اكتب سورة أو آية تريد حفظها...',
    placeholderEn: 'Write a surah or ayah you want to memorize...',
    suggestionsAr: ['سمّعني سورة الفاتحة', 'علمني سورة الإخلاص', 'ما فضل سورة الملك؟', 'اختبرني في جزء عمّ'],
    suggestionsEn: ['Quiz me on Al-Fatiha', 'Teach me Al-Ikhlas', 'What is the virtue of Al-Mulk?', 'Test me on Juz Amma'],
  },
  'arabic-tutor': {
    titleAr: 'معلمة العربية الذكية',
    titleEn: 'AI Arabic Teacher',
    descAr: 'أعلّمك الحروف والكلمات والقواعد بطريقة ممتعة',
    descEn: 'I teach you letters, words, and grammar in a fun way',
    emoji: '✏️',
    color: 'from-blue-500/20 to-indigo-500/10',
    border: 'border-blue-400/30',
    placeholderAr: 'اسأل عن حرف أو كلمة عربية...',
    placeholderEn: 'Ask about an Arabic letter or word...',
    suggestionsAr: ['علمني حرف الألف', 'ما ضد كلمة كبير؟', 'أعطني جملة مفيدة', 'ما جمع كلمة كتاب؟'],
    suggestionsEn: ['Teach me the letter Alif', 'What is the opposite of big?', 'Give me a useful sentence', 'What is the plural of book?'],
  },
  'islamic-qa': {
    titleAr: 'أسئلة إسلامية ذكية',
    titleEn: 'AI Islamic Q&A',
    descAr: 'اسألني أي سؤال إسلامي وسأجيبك بالدليل من القرآن والسنة',
    descEn: 'Ask me any Islamic question with evidence from Quran & Sunnah',
    emoji: '🤲',
    color: 'from-amber-500/20 to-yellow-500/10',
    border: 'border-amber-400/30',
    placeholderAr: 'اكتب سؤالك الإسلامي...',
    placeholderEn: 'Write your Islamic question...',
    suggestionsAr: ['لماذا نصلي خمس مرات؟', 'من هو أول نبي؟', 'ما هي أركان الإسلام؟', 'كيف أكون مسلماً صالحاً؟'],
    suggestionsEn: ['Why do we pray five times?', 'Who was the first prophet?', 'What are the pillars of Islam?', 'How can I be a good Muslim?'],
  },
  'story-generator': {
    titleAr: 'قصص إسلامية بالذكاء الاصطناعي',
    titleEn: 'AI Islamic Stories',
    descAr: 'أنشئ قصصاً إسلامية جميلة ومشوقة في كل مرة',
    descEn: 'Generate beautiful Islamic stories every time',
    emoji: '📚',
    color: 'from-purple-500/20 to-violet-500/10',
    border: 'border-purple-400/30',
    placeholderAr: 'اكتب موضوع القصة (أو اتركه فارغاً لقصة عشوائية)...',
    placeholderEn: 'Write a story topic (or leave empty for random)...',
    suggestionsAr: ['قصة عن الصدق', 'قصة عن بر الوالدين', 'قصة نبي موسى عليه السلام', 'قصة عن الصلاة'],
    suggestionsEn: ['A story about honesty', 'A story about respecting parents', 'Story of Prophet Musa', 'A story about prayer'],
  },
};

const AIChat: React.FC<AIChatProps> = ({ mode }) => {
  const { dir } = useLocale();
  const isRtl = dir === 'rtl';
  const config = MODE_CONFIG[mode];

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text?: string) => {
    const msgText = text || input.trim();
    if (!msgText || loading) return;

    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: msgText }]);
    setLoading(true);

    try {
      const endpoint = mode === 'story-generator' ? 'story-generator' : mode;
      const body = mode === 'story-generator'
        ? { topic: msgText, locale: isRtl ? 'ar' : 'en', age_group: '7-10' }
        : { message: msgText, session_id: sessionId, locale: isRtl ? 'ar' : 'en' };

      const res = await fetch(`${API_BASE}/api/kids-ai/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      if (data.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
        if (data.session_id) setSessionId(data.session_id);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: isRtl ? '⚠️ عذراً، حدث خطأ. حاول مرة أخرى.' : '⚠️ Sorry, an error occurred. Please try again.' }]);
      }
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: isRtl ? '⚠️ تعذر الاتصال. تأكد من الإنترنت.' : '⚠️ Connection failed. Check your internet.' }]);
    } finally {
      setLoading(false);
    }
  };

  const resetChat = () => {
    setMessages([]);
    setSessionId(null);
  };

  return (
    <div className="space-y-3" dir={dir}>
      {/* Header */}
      <div className={cn("text-center p-4 rounded-2xl bg-gradient-to-br border", config.color, config.border)}>
        <span className="text-4xl">{config.emoji}</span>
        <h3 className="font-bold mt-2 text-lg">{isRtl ? config.titleAr : config.titleEn}</h3>
        <p className="text-xs text-muted-foreground mt-1">{isRtl ? config.descAr : config.descEn}</p>
        <div className="flex items-center justify-center gap-1 mt-2">
          <Sparkles className="h-3 w-3 text-amber-500 dark:text-amber-400" />
          <span className="text-[10px] text-amber-500 dark:text-amber-400/70">{isRtl ? 'مدعوم بالذكاء الاصطناعي • مجاني' : 'AI-Powered • Free'}</span>
        </div>
      </div>

      {/* Suggestions */}
      {messages.length === 0 && (
        <div className="grid grid-cols-2 gap-2">
          {(isRtl ? config.suggestionsAr : config.suggestionsEn).map((s, i) => (
            <button
              key={i}
              onClick={() => sendMessage(s)}
              className="p-2.5 rounded-xl bg-white/5 border border-white/10 text-xs text-start hover:bg-white/10 transition-all"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Chat Messages */}
      {messages.length > 0 && (
        <div className="space-y-3 max-h-[400px] overflow-y-auto p-1">
          {messages.map((msg, i) => (
            <div key={i} className={cn("flex gap-2", msg.role === 'user' ? (isRtl ? 'flex-row-reverse' : 'flex-row') : '')}>
              <div className={cn(
                "w-7 h-7 rounded-full flex items-center justify-center shrink-0 text-xs",
                msg.role === 'user' ? 'bg-blue-500' : 'bg-green-500'
              )}>
                {msg.role === 'user' ? <User className="h-3.5 w-3.5 text-white" /> : <Bot className="h-3.5 w-3.5 text-white" />}
              </div>
              <div className={cn(
                "p-3 rounded-xl max-w-[85%] text-sm leading-relaxed whitespace-pre-wrap",
                msg.role === 'user' ? 'bg-blue-500/20 border border-blue-500/30' : 'bg-white/5 border border-white/10'
              )}>
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-2 items-center">
              <div className="w-7 h-7 rounded-full bg-green-500 flex items-center justify-center">
                <Bot className="h-3.5 w-3.5 text-white" />
              </div>
              <div className="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin text-green-500 dark:text-green-400" />
                <span className="text-xs text-muted-foreground">{isRtl ? 'يفكّر...' : 'Thinking...'}</span>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
      )}

      {/* Input Area */}
      <div className="flex items-center gap-2">
        {messages.length > 0 && (
          <button onClick={resetChat} className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 transition-all shrink-0" title={isRtl ? 'محادثة جديدة' : 'New chat'}>
            <RotateCcw className="h-4 w-4 text-muted-foreground" />
          </button>
        )}
        <div className="flex-1 flex items-center gap-2 bg-white/5 border border-white/10 rounded-xl p-1.5">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && sendMessage()}
            placeholder={isRtl ? config.placeholderAr : config.placeholderEn}
            className="flex-1 bg-transparent text-sm px-2 py-1 outline-none placeholder:text-muted-foreground/50"
            dir={dir}
            disabled={loading}
          />
          <button
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
            className="p-2 rounded-lg bg-green-600 hover:bg-green-500 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
          >
            <Send className={cn("h-4 w-4 text-white", isRtl && 'rotate-180')} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIChat;
