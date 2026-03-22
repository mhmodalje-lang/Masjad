import React from 'react';
import { useLocale } from '@/hooks/useLocale';
import { cn } from '@/lib/utils';

interface NativeAdContainerProps {
  className?: string;
  variant?: 'card' | 'inline' | 'banner';
}

/**
 * Native Ad Container - visually matches the app's design language.
 * Same padding, corner radius (16px), and shadow as content cards.
 * Adapts to Light/Dark mode dynamically.
 * 
 * In production: Replace inner content with AdMob Native Ad SDK.
 * Currently shows a simulated ad placeholder for development.
 */
export default function NativeAdContainer({ className, variant = 'card' }: NativeAdContainerProps) {
  const { dir } = useLocale();

  if (variant === 'banner') {
    return (
      <div dir={dir} className={cn(
        "w-full px-4 py-3 rounded-2xl border transition-colors",
        "bg-gradient-to-r from-muted/30 to-muted/10 border-border/20",
        "dark:from-white/[0.03] dark:to-white/[0.01]",
        className
      )}>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-muted/30 flex items-center justify-center text-lg">📢</div>
          <div className="flex-1">
            <p className="text-sm font-medium text-foreground/70">Sponsored</p>
            <p className="text-xs text-foreground/40">Ad placeholder • Dev Mode</p>
          </div>
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-muted/20 text-foreground/40">AD</span>
        </div>
      </div>
    );
  }

  return (
    <div dir={dir} className={cn(
      "w-full p-4 rounded-2xl border transition-colors",
      "bg-card/60 border-border/30 shadow-sm",
      "dark:bg-card/40 dark:border-border/20",
      className
    )}>
      <div className="flex items-start gap-3">
        <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-muted/40 to-muted/20 flex items-center justify-center text-2xl shrink-0">
          📢
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-muted/30 text-foreground/40 font-medium">Sponsored</span>
          </div>
          <p className="text-sm font-medium text-foreground/80 line-clamp-2">Native Ad Placeholder</p>
          <p className="text-xs text-foreground/40 mt-1">This space will show native ads from AdMob in production</p>
        </div>
      </div>
    </div>
  );
}
