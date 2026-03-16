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
          <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/40 to-background" />
        </>
      ) : (
        <>
          <div className="absolute inset-0 gradient-islamic" />
          <div className="absolute inset-0 islamic-pattern opacity-15" />
        </>
      )}
      <div className="flex items-center justify-between relative z-10 px-5 gap-3">
        {actionsLeft || (backTo ? (
          <button onClick={handleBack} className="w-10 h-10 rounded-2xl glass-dark flex items-center justify-center shrink-0 transition-all active:scale-95">
            <ArrowRight className="h-5 w-5 text-white" />
          </button>
        ) : <div className="w-10 shrink-0" />)}
        <div className="text-center flex-1 min-w-0">
          <div className="inline-flex items-center gap-2 rounded-2xl glass-dark px-5 py-2">
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
