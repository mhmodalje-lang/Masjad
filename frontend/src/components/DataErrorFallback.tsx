/**
 * DataErrorFallback - Shown when API data fails to load
 * Provides retry and offline information
 */
import { WifiOff, RefreshCw, Home } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface DataErrorFallbackProps {
  error?: string;
  onRetry?: () => void;
  isOffline?: boolean;
}

export default function DataErrorFallback({ error, onRetry, isOffline }: DataErrorFallbackProps) {
  const navigate = useNavigate();
  const offline = isOffline ?? !navigator.onLine;
  
  return (
    <div className="flex flex-col items-center justify-center py-16 px-6 text-center" dir="rtl">
      <div className="w-20 h-20 rounded-3xl bg-amber-500/10 flex items-center justify-center mb-6">
        {offline ? (
          <WifiOff className="h-10 w-10 text-amber-500" />
        ) : (
          <span className="text-4xl">⚠️</span>
        )}
      </div>
      
      <h3 className="text-lg font-bold text-foreground mb-2">
        {offline ? 'غير متصل بالإنترنت' : 'تعذر تحميل البيانات'}
      </h3>
      
      <p className="text-sm text-muted-foreground mb-6 max-w-sm leading-relaxed">
        {offline 
          ? 'تحقق من اتصالك بالإنترنت وحاول مرة أخرى. بعض المحتوى المحفوظ قد يكون متاحاً.'
          : error || 'حدث خطأ في تحميل البيانات. يرجى المحاولة مرة أخرى.'
        }
      </p>
      
      <div className="flex gap-3">
        {onRetry && (
          <button
            onClick={onRetry}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 text-white font-bold text-sm transition-all active:scale-95 hover:bg-emerald-700"
          >
            <RefreshCw className="h-4 w-4" />
            إعادة المحاولة
          </button>
        )}
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-muted text-foreground font-bold text-sm transition-all active:scale-95"
        >
          <Home className="h-4 w-4" />
          الرئيسية
        </button>
      </div>
    </div>
  );
}
