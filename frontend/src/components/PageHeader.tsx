import { ReactNode } from 'react';
import { ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export interface PageHeaderProps {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  actionsLeft?: ReactNode;
  compact?: boolean;
  image?: string;
  backTo?: string;
}

export default function PageHeader({ title, subtitle, actions, actionsLeft, compact, image, backTo }: PageHeaderProps) {
  const navigate = useNavigate();

  const handleBack = () => {
    const idx = (window.history.state as any)?.idx;
    if (typeof idx === 'number' && idx > 0) {
      window.history.back();
    } else {
      navigate(backTo || '/', { replace: true });
    }
  };

  return (
    <div className={`relative overflow-hidden ${image ? 'pb-16 pt-safe-header' : compact ? 'pb-12 pt-safe-header-compact' : 'pb-14 pt-safe-header'}`}>
      {image ? (
        <>
          <img src={image} alt="" className="absolute inset-0 w-full h-full object-cover animate-heroZoom" loading="eager" />
          <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/30 to-[hsl(var(--background))]" />
        </>
      ) : (
        <>
          <div className="absolute inset-0 bg-gradient-to-b from-[hsl(var(--mystic-moss))] via-[hsl(var(--islamic-emerald))] to-[hsl(var(--mystic-moss))]/90" />
          <div className="absolute inset-0 opacity-[0.04]" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23fff' fill-opacity='.3'%3E%3Cpath d='M40 10L50 30H30z M40 70L30 50H50z M10 40L30 30V50z M70 40L50 50V30z'/%3E%3C/g%3E%3C/svg%3E")`,
          }} />
        </>
      )}
      <div className="flex items-center justify-between relative z-10 px-5 gap-3">
        {actionsLeft || (backTo ? (
          <button onClick={handleBack} className="w-10 h-10 rounded-2xl bg-white/10 backdrop-blur-xl border border-white/10 flex items-center justify-center shrink-0 transition-all active:scale-95 hover:bg-white/15">
            <ArrowRight className="h-5 w-5 text-white" />
          </button>
        ) : <div className="w-10 shrink-0" />)}
        <div className="text-center flex-1 min-w-0">
          <div className="inline-flex items-center gap-2 rounded-2xl bg-white/10 backdrop-blur-xl border border-white/10 px-5 py-2">
            <h1 className="text-lg font-extrabold text-white whitespace-nowrap tracking-tight">{title}</h1>
          </div>
          {subtitle && (
            <p className="text-white/70 text-xs mt-2.5 leading-relaxed font-medium max-w-[280px] mx-auto">{subtitle}</p>
          )}
        </div>
        {actions || <div className="w-10 shrink-0" />}
      </div>
      <div className="absolute -bottom-1 left-0 right-0 h-8 rounded-t-[2rem] bg-background" />
    </div>
  );
}
