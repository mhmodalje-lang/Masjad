import React, { useState } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { ChevronLeft, ChevronRight, BookOpen, ZoomIn } from 'lucide-react';
import { cn } from '@/lib/utils';

/* ═══════════════════════════════════════════════════════════════
   SALAH TEACHING GUIDE V2 - 4K 3D Illustrated Prayer Steps
   Images: Generated via OpenAI gpt-image-1 (Pixar/UE5 style)
   Character: "Noor" - 7-year-old Muslim boy in white Thobe
   ═══════════════════════════════════════════════════════════════ */

// Step color mapping
const STEP_COLORS: Record<string, { bg: string; border: string; text: string; badge: string; glow: string }> = {
  qiyam_niyyah: { bg: 'from-emerald-900/50 to-emerald-800/30', border: 'border-emerald-500/40', text: 'text-emerald-600 dark:text-emerald-300', badge: 'bg-emerald-600', glow: 'shadow-emerald-500/20' },
  takbir: { bg: 'from-amber-900/50 to-amber-800/30', border: 'border-amber-500/40', text: 'text-amber-600 dark:text-amber-300', badge: 'bg-amber-600', glow: 'shadow-amber-500/20' },
  qiyam_qiraa: { bg: 'from-teal-900/50 to-teal-800/30', border: 'border-teal-500/40', text: 'text-teal-600 dark:text-teal-300', badge: 'bg-teal-600', glow: 'shadow-teal-500/20' },
  qiyam_fatiha: { bg: 'from-yellow-900/50 to-yellow-800/30', border: 'border-yellow-500/40', text: 'text-yellow-600 dark:text-yellow-300', badge: 'bg-yellow-600', glow: 'shadow-yellow-500/20' },
  ruku: { bg: 'from-blue-900/50 to-blue-800/30', border: 'border-blue-500/40', text: 'text-blue-600 dark:text-blue-300', badge: 'bg-blue-600', glow: 'shadow-blue-500/20' },
  itidal: { bg: 'from-cyan-900/50 to-cyan-800/30', border: 'border-cyan-500/40', text: 'text-cyan-600 dark:text-cyan-300', badge: 'bg-cyan-600', glow: 'shadow-cyan-500/20' },
  sujud_1: { bg: 'from-green-900/50 to-green-800/30', border: 'border-green-500/40', text: 'text-green-600 dark:text-green-300', badge: 'bg-green-600', glow: 'shadow-green-500/20' },
  juloos: { bg: 'from-purple-900/50 to-purple-800/30', border: 'border-purple-500/40', text: 'text-purple-600 dark:text-purple-300', badge: 'bg-purple-600', glow: 'shadow-purple-500/20' },
  sujud_2: { bg: 'from-green-900/50 to-green-800/30', border: 'border-green-500/40', text: 'text-green-600 dark:text-green-300', badge: 'bg-green-600', glow: 'shadow-green-500/20' },
  tashahhud: { bg: 'from-indigo-900/50 to-indigo-800/30', border: 'border-indigo-500/40', text: 'text-indigo-600 dark:text-indigo-300', badge: 'bg-indigo-600', glow: 'shadow-indigo-500/20' },
  tasleem: { bg: 'from-rose-900/50 to-rose-800/30', border: 'border-rose-500/40', text: 'text-rose-600 dark:text-rose-300', badge: 'bg-rose-600', glow: 'shadow-rose-500/20' },
};

interface SalahStep {
  step: number;
  position: string;
  image_url: string;
  title: string;
  description: string;
  dhikr_ar: string;
  dhikr_transliteration: string;
  body_position: string;
}

interface SalahGuideProps {
  steps: SalahStep[];
}

const SalahGuide: React.FC<SalahGuideProps> = ({ steps }) => {
  const { t, dir } = useLocale();
  const isRtl = dir === 'rtl';
  const [currentStep, setCurrentStep] = useState(0);
  const [viewMode, setViewMode] = useState<'card' | 'list'>('card');
  const [zoomedImage, setZoomedImage] = useState<string | null>(null);

  if (!steps || steps.length === 0) return null;

  const step = steps[currentStep];
  const colors = STEP_COLORS[step?.position] || STEP_COLORS.qiyam_niyyah;

  const goNext = () => setCurrentStep(prev => Math.min(prev + 1, steps.length - 1));
  const goPrev = () => setCurrentStep(prev => Math.max(prev - 1, 0));

  return (
    <div className="space-y-3" dir={dir}>
      {/* Zoomed Image Modal */}
      {zoomedImage && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
          onClick={() => setZoomedImage(null)}
        >
          <img
            src={zoomedImage}
            alt="Prayer position"
            className="max-w-full max-h-[90vh] rounded-2xl object-contain"
          />
          <button
            onClick={() => setZoomedImage(null)}
            className="absolute top-4 right-4 text-white/70 hover:text-white text-3xl font-bold"
          >
            ×
          </button>
        </div>
      )}

      {/* Header */}
      <div className="text-center p-5 rounded-2xl bg-gradient-to-br from-green-500/20 to-emerald-500/10 border border-green-400/30 relative overflow-hidden">
        {/* Decorative mosque pattern */}
        <div className="absolute inset-0 opacity-5">
          <div className="flex justify-center gap-4 mt-2">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="w-8 h-12 border-t-[16px] border-t-green-400 rounded-t-full" />
            ))}
          </div>
        </div>
        <span className="text-4xl">🕌</span>
        <h3 className="font-bold mt-2 text-xl bg-gradient-to-r from-green-300 to-emerald-200 bg-clip-text text-transparent">
          {isRtl ? 'تعليم الصلاة خطوة بخطوة' : 'Learn Prayer Step by Step'}
        </h3>
        <p className="text-[11px] text-muted-foreground mt-1">
          {isRtl
            ? 'مع نور • رسومات ثلاثية الأبعاد عالية الجودة • مبني على الفقه الإسلامي الصحيح'
            : 'With Noor • High-Quality 3D Illustrations • Based on Authentic Islamic Jurisprudence'}
        </p>
        {/* View mode toggle */}
        <div className="flex items-center justify-center gap-2 mt-3 relative z-10">
          <button
            onClick={() => setViewMode('card')}
            className={cn(
              "px-4 py-1.5 rounded-full text-xs font-semibold transition-all",
              viewMode === 'card'
                ? 'bg-green-600 text-white shadow-lg shadow-green-600/30'
                : 'bg-white/10 text-muted-foreground hover:bg-white/15'
            )}
          >
            {isRtl ? '🎴 بطاقات' : '🎴 Cards'}
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={cn(
              "px-4 py-1.5 rounded-full text-xs font-semibold transition-all",
              viewMode === 'list'
                ? 'bg-green-600 text-white shadow-lg shadow-green-600/30'
                : 'bg-white/10 text-muted-foreground hover:bg-white/15'
            )}
          >
            {isRtl ? '📋 قائمة' : '📋 List'}
          </button>
        </div>
      </div>

      {/* ═══════════════════ CARD VIEW ═══════════════════ */}
      {viewMode === 'card' && (
        <>
          {/* Step Progress Bar */}
          <div className="flex gap-1.5 px-2">
            {steps.map((s, i) => (
              <button
                key={s.step}
                onClick={() => setCurrentStep(i)}
                className={cn(
                  "flex-1 h-2.5 rounded-full transition-all duration-500 hover:scale-y-150",
                  i === currentStep
                    ? 'bg-gradient-to-r from-green-400 to-emerald-500 scale-y-125 shadow-lg shadow-green-500/30'
                    : i < currentStep
                    ? 'bg-green-700/80'
                    : 'bg-white/10'
                )}
                title={s.title}
              />
            ))}
          </div>

          {/* Step Counter */}
          <div className="text-center">
            <span className={cn(
              "inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-bold text-white shadow-lg",
              colors.badge, colors.glow
            )}>
              {isRtl ? `الخطوة ${step.step} من ${steps.length}` : `Step ${step.step} of ${steps.length}`}
            </span>
          </div>

          {/* Main Step Card */}
          <div className={cn(
            "rounded-2xl border-2 p-4 bg-gradient-to-br transition-all duration-700 shadow-2xl",
            colors.bg, colors.border, colors.glow
          )}>
            {/* Step Title */}
            <h4 className={cn("text-xl font-bold text-center mb-3", colors.text)}>
              {step.title}
            </h4>

            {/* 3D Image */}
            {step.image_url && (
              <div
                className="relative mb-4 rounded-xl overflow-hidden cursor-pointer group shadow-xl"
                onClick={() => setZoomedImage(step.image_url)}
              >
                <img
                  src={step.image_url}
                  alt={step.title}
                  className="w-full h-auto rounded-xl object-cover transition-transform duration-500 group-hover:scale-105"
                  loading="lazy"
                />
                {/* Zoom overlay */}
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all flex items-center justify-center">
                  <ZoomIn className="h-8 w-8 text-white opacity-0 group-hover:opacity-80 transition-opacity" />
                </div>
                {/* Step badge on image */}
                <div className={cn(
                  "absolute top-3 rounded-full w-9 h-9 flex items-center justify-center text-sm font-bold text-white shadow-lg",
                  colors.badge,
                  isRtl ? 'right-3' : 'left-3'
                )}>
                  {step.step}
                </div>
              </div>
            )}

            {/* Body Position Indicator */}
            {step.body_position && (
              <div className="text-center mb-3 px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
                <span className="text-xs text-muted-foreground">
                  {isRtl ? '🦴 وضع الجسم: ' : '🦴 Body Position: '}
                </span>
                <span className="text-xs font-semibold">{step.body_position}</span>
              </div>
            )}

            {/* Description */}
            <div className="p-4 rounded-xl bg-white/5 border border-white/10 mb-3 backdrop-blur-sm">
              <p className="text-sm leading-relaxed" dir={dir}>
                {step.description}
              </p>
            </div>

            {/* Dhikr / Recitation */}
            {step.dhikr_ar && (
              <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/25 shadow-inner">
                <div className="flex items-center gap-2 mb-2">
                  <BookOpen className="h-4 w-4 text-amber-500 dark:text-amber-400" />
                  <span className="text-xs font-bold text-amber-500 dark:text-amber-400">{isRtl ? 'الذكر' : 'Dhikr / Recitation'}</span>
                </div>
                <p className="text-lg font-bold text-amber-200 text-center leading-loose" dir="rtl">
                  {step.dhikr_ar}
                </p>
                {step.dhikr_transliteration && (
                  <p className="text-xs text-amber-500 dark:text-amber-400/60 text-center mt-1.5 italic" dir="ltr">
                    {step.dhikr_transliteration}
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Navigation Buttons */}
          <div className="flex items-center justify-between gap-3 px-1">
            <button
              onClick={isRtl ? goNext : goPrev}
              disabled={isRtl ? currentStep >= steps.length - 1 : currentStep <= 0}
              className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 disabled:opacity-20 disabled:cursor-not-allowed transition-all text-sm font-semibold"
            >
              <ChevronRight className="h-4 w-4" />
              {isRtl ? 'التالي' : 'Previous'}
            </button>
            <div className="flex items-center gap-1">
              {steps.map((_, i) => (
                <div
                  key={i}
                  className={cn(
                    "w-2 h-2 rounded-full transition-all",
                    i === currentStep ? 'bg-green-400 w-4' : 'bg-white/20'
                  )}
                />
              ))}
            </div>
            <button
              onClick={isRtl ? goPrev : goNext}
              disabled={isRtl ? currentStep <= 0 : currentStep >= steps.length - 1}
              className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-green-600 hover:bg-green-500 disabled:opacity-20 disabled:cursor-not-allowed transition-all text-sm font-semibold text-white shadow-lg shadow-green-600/30"
            >
              {isRtl ? 'السابق' : 'Next'}
              <ChevronLeft className="h-4 w-4" />
            </button>
          </div>
        </>
      )}

      {/* ═══════════════════ LIST VIEW ═══════════════════ */}
      {viewMode === 'list' && (
        <div className="space-y-4">
          {steps.map((s) => {
            const c = STEP_COLORS[s.position] || STEP_COLORS.qiyam_niyyah;
            return (
              <div key={s.step} className={cn(
                "rounded-2xl border-2 p-4 bg-gradient-to-br shadow-xl",
                c.bg, c.border
              )}>
                {/* Step badge + Title */}
                <div className="flex items-center gap-3 mb-3">
                  <div className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center text-base font-bold text-white shrink-0 shadow-lg",
                    c.badge
                  )}>
                    {s.step}
                  </div>
                  <h5 className={cn("font-bold text-base", c.text)}>{s.title}</h5>
                </div>

                {/* 3D Image */}
                {s.image_url && (
                  <div
                    className="rounded-xl overflow-hidden mb-3 cursor-pointer shadow-lg group"
                    onClick={() => setZoomedImage(s.image_url)}
                  >
                    <img
                      src={s.image_url}
                      alt={s.title}
                      className="w-full h-auto object-cover rounded-xl transition-transform duration-500 group-hover:scale-105"
                      loading="lazy"
                    />
                  </div>
                )}

                {/* Body position */}
                {s.body_position && (
                  <div className="text-center mb-2 px-2 py-1.5 rounded-lg bg-white/5 border border-white/10">
                    <span className="text-[10px] text-muted-foreground">🦴 </span>
                    <span className="text-[11px] font-medium">{s.body_position}</span>
                  </div>
                )}

                {/* Description */}
                <p className="text-xs text-muted-foreground leading-relaxed mb-2">{s.description}</p>

                {/* Dhikr */}
                {s.dhikr_ar && (
                  <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
                    <p className="text-base font-bold text-amber-200 text-center leading-relaxed" dir="rtl">{s.dhikr_ar}</p>
                    {s.dhikr_transliteration && (
                      <p className="text-[10px] text-amber-500 dark:text-amber-400/50 text-center mt-1 italic" dir="ltr">{s.dhikr_transliteration}</p>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Islamic Reference Footer */}
      <div className="text-center p-4 rounded-xl bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10">
        <p className="text-[10px] text-muted-foreground leading-relaxed">
          {isRtl
            ? '📚 المرجع: صفة صلاة النبي ﷺ — الشيخ محمد ناصر الدين الألباني\n🎨 الرسومات: رسومات ثلاثية الأبعاد بأسلوب بيكسار/UE5 عبر OpenAI'
            : '📚 Reference: The Prophet\'s Prayer Described ﷺ — Shaykh al-Albani\n🎨 Illustrations: 3D renders in Pixar/UE5 style via OpenAI'}
        </p>
      </div>
    </div>
  );
};

export default SalahGuide;
