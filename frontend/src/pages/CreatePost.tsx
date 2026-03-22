import { useState, useRef } from 'react';
import { useLocale } from "@/hooks/useLocale";
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { X, Image, Video, FileText, Send, Loader2, Camera } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

const CATEGORIES = [
  { key: 'general', label: t('generalCategory'), labelKey: 'sohbaCatGeneral', emoji: '🌍' },
  { key: 'quran', label: 'القرآن', labelKey: 'sohbaCatQuran', emoji: '📖' },
  { key: 'hadith', label: 'الحديث', labelKey: 'sohbaCatHadith', emoji: '📜' },
  { key: 'dua', label: 'الدعاء', labelKey: 'sohbaCatDua', emoji: '🤲' },
  { key: 'stories', label: 'قصص', labelKey: 'sohbaCatStories', emoji: '📝' },
  { key: 'ramadan', label: 'رمضان', labelKey: 'sohbaCatRamadan', emoji: '🌙' },
  { key: 'family', label: 'الأسرة', labelKey: 'sohbaCatFamily', emoji: '👨‍👩‍👧‍👦' },
  { key: 'youth', label: 'الشباب', labelKey: 'sohbaCatYouth', emoji: '💪' },
];

const CONTENT_TYPES = [
  { key: 'text', labelKey: 'textOption', label: 'نص', icon: FileText },
  { key: 'image', labelKey: 'imageOption', label: 'صورة', icon: Image },
  { key: 'video_short', labelKey: 'videoOption', label: 'ريلز', icon: Video },
  { key: 'video_long', labelKey: 'videoOption', label: 'فيديو', icon: Camera },
];

export default function CreatePost() {
  const { t, dir } = useLocale();
  const { user, getToken } = useAuth();
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('general');
  const [contentType, setContentType] = useState('text');
  const [mediaFile, setMediaFile] = useState<File | null>(null);
  const [mediaPreview, setMediaPreview] = useState('');
  const [uploading, setUploading] = useState(false);
  const [publishing, setPublishing] = useState(false);

  if (!user) {
    navigate('/auth');
    return null;
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setMediaFile(file);
    
    const reader = new FileReader();
    reader.onload = (ev) => {
      setMediaPreview(ev.target?.result as string);
    };
    reader.readAsDataURL(file);

    // Auto-detect content type
    if (file.type.startsWith('image/')) {
      setContentType('image');
    } else if (file.type.startsWith('video/')) {
      setContentType('video_short');
    }
  };

  const uploadMedia = async (): Promise<string | null> => {
    if (!mediaFile) return null;
    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', mediaFile);
      
      const token = getToken();
      const res = await fetch(`${BACKEND_URL}/api/upload/multipart`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });
      
      if (!res.ok) throw new Error('فشل في رفع الملف');
      const data = await res.json();
      return data.url;
    } catch (err) {
      toast.error('فشل في رفع الملف');
      return null;
    } finally {
      setUploading(false);
    }
  };

  const handlePublish = async () => {
    if (!content.trim()) {
      toast.error('اكتب شيئاً أولاً');
      return;
    }
    
    setPublishing(true);
    try {
      let mediaUrl = null;
      if (mediaFile) {
        mediaUrl = await uploadMedia();
        if (!mediaUrl) {
          setPublishing(false);
          return;
        }
      }

      const token = getToken();
      const isVideo = contentType.includes('video');
      const body: any = {
        content: content.trim(),
        category,
        content_type: contentType,
      };
      
      if (mediaUrl) {
        if (isVideo) {
          body.video_url = mediaUrl;
        } else {
          body.image_url = mediaUrl;
        }
      }

      const res = await fetch(`${BACKEND_URL}/api/sohba/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) throw new Error('فشل في النشر');
      toast.success('تم النشر بنجاح! ✨');
      navigate('/');
    } catch (err) {
      toast.error('حدث خطأ أثناء النشر');
    } finally {
      setPublishing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background pb-20">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-card border-b border-border">
        <div className="flex items-center justify-between px-4 py-3">
          <button onClick={() => navigate(-1)} className="text-white">
            <X className="w-6 h-6" />
          </button>
          <h1 className="text-white font-bold text-lg">إنشاء منشور</h1>
          <button
            onClick={handlePublish}
            disabled={publishing || !content.trim()}
            className="px-4 py-1.5 bg-emerald-600 text-white rounded-full text-sm font-bold disabled:opacity-50 flex items-center gap-1"
          >
            {publishing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            نشر
          </button>
        </div>
      </div>

      <div className="p-4 space-y-4" dir={dir}>
        {/* Content Type Selector */}
        <div className="flex gap-2">
          {CONTENT_TYPES.map((ct) => (
            <button
              key={ct.key}
              onClick={() => setContentType(ct.key)}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm font-medium transition-all ${
                contentType === ct.key
                  ? 'bg-emerald-600 text-white'
                  : 'bg-muted/30 text-muted-foreground hover:bg-muted/50'
              }`}
            >
              <ct.icon className="w-4 h-4" />
              {ct.labelKey ? t(ct.labelKey) : ct.label}
            </button>
          ))}
        </div>

        {/* Author Info */}
        <div className="flex items-center gap-3">
          <img
            src={user.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name || '')}&background=1a7a4c&color=fff&size=40`}
            alt=""
            className="w-10 h-10 rounded-full border-2 border-emerald-500"
          />
          <span className="text-white font-bold">{user.name}</span>
        </div>

        {/* Text Input */}
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="شارك فكرتك مع المجتمع..."
          className="w-full min-h-[150px] bg-card text-foreground rounded-xl p-4 border border-border focus:border-primary focus:outline-none resize-none text-base leading-relaxed placeholder:text-muted-foreground"
          dir={dir}
          maxLength={5000}
        />
        <div className="text-left text-muted-foreground text-xs">{content.length}/5000</div>

        {/* Media Upload */}
        <div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*,video/*"
            onChange={handleFileSelect}
            className="hidden"
          />
          
          {mediaPreview ? (
            <div className="relative rounded-xl overflow-hidden">
              {mediaFile?.type.startsWith('video/') ? (
                <video src={mediaPreview} controls className="w-full max-h-80 rounded-xl" />
              ) : (
                <img src={mediaPreview} alt="" className="w-full max-h-80 object-cover rounded-xl" />
              )}
              <button
                onClick={() => { setMediaFile(null); setMediaPreview(''); }}
                className="absolute top-2 left-2 w-8 h-8 bg-black/60 rounded-full flex items-center justify-center text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={() => fileInputRef.current?.click()}
              className="w-full py-12 border-2 border-dashed border-border/10 rounded-xl text-muted-foreground hover:border-emerald-600 hover:text-emerald-500 transition-colors flex flex-col items-center gap-2"
            >
              <Image className="w-8 h-8" />
              <span className="text-sm">إضافة صورة أو فيديو</span>
            </button>
          )}
        </div>

        {/* Category Selector */}
        <div>
          <h3 className="text-white text-sm font-bold mb-2">{t('categoryLabel')}</h3>
          <div className="flex flex-wrap gap-2">
            {CATEGORIES.map((cat) => (
              <button
                key={cat.key}
                onClick={() => setCategory(cat.key)}
                className={`px-3 py-1.5 rounded-full text-sm transition-all ${
                  category === cat.key
                    ? 'bg-emerald-600 text-white'
                    : 'bg-muted/30 text-muted-foreground hover:bg-muted/50'
                }`}
              >
                {cat.emoji} {cat.labelKey ? t(cat.labelKey) : cat.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
