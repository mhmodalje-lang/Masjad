import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SectionTitleProps {
  icon?: LucideIcon;
  emoji?: string;
  title: string;
  subtitle?: string;
  className?: string;
}

export default function SectionTitle({ icon: Icon, emoji, title, subtitle, className }: SectionTitleProps) {
  return (
    <div className={cn('flex items-center gap-3 mb-4', className)}>
      {(emoji || Icon) && (
        <div className="h-8 w-8 rounded-lg glass-futuristic border-neon flex items-center justify-center shrink-0">
          {emoji ? (
            <span className="text-sm">{emoji}</span>
          ) : Icon ? (
            <Icon className="h-4 w-4 text-primary" />
          ) : null}
        </div>
      )}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-bold text-primary">{title}</p>
        {subtitle && <p className="text-xs text-muted-foreground leading-relaxed">{subtitle}</p>}
      </div>
    </div>
  );
}
