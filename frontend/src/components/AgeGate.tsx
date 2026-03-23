import { useState } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { ShieldCheck, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';

const AGE_GATE_KEY = 'age_gate_passed';

export function hasPassedAgeGate(): boolean {
  return localStorage.getItem(AGE_GATE_KEY) === '1';
}

export default function AgeGate({ onPass }: { onPass: () => void }) {
  const { t, dir } = useLocale();
  const [selectedAge, setSelectedAge] = useState<string | null>(null);
  const [showUnderAge, setShowUnderAge] = useState(false);

  const handleConfirm = () => {
    if (selectedAge === 'above') {
      localStorage.setItem(AGE_GATE_KEY, '1');
      onPass();
    } else {
      setShowUnderAge(true);
    }
  };

  if (showUnderAge) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-950 via-teal-950 to-green-950 p-6" dir={dir}>
        <div className="max-w-sm w-full text-center space-y-6">
          <AlertTriangle className="h-16 w-16 mx-auto text-amber-400" />
          <h2 className="text-xl font-bold text-white">{t('ageGateUnderTitle')}</h2>
          <p className="text-sm text-white/70 leading-relaxed">{t('ageGateUnderMsg')}</p>
          <Button
            onClick={() => { setShowUnderAge(false); setSelectedAge(null); }}
            className="w-full rounded-2xl h-12 bg-white/10 hover:bg-white/20 text-white font-bold"
          >
            {t('goBack')}
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-950 via-teal-950 to-green-950 p-6" dir={dir}>
      <div className="max-w-sm w-full space-y-6">
        <div className="text-center">
          <ShieldCheck className="h-16 w-16 mx-auto text-emerald-400 mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">{t('ageGateTitle')}</h2>
          <p className="text-sm text-white/70 leading-relaxed">{t('ageGateMessage')}</p>
        </div>

        <div className="space-y-3">
          <button
            onClick={() => setSelectedAge('above')}
            className={`w-full p-4 rounded-2xl border-2 text-start transition-all ${
              selectedAge === 'above'
                ? 'border-emerald-400 bg-emerald-400/10 text-white'
                : 'border-white/20 bg-white/5 text-white/80 hover:border-white/40'
            }`}
          >
            <p className="font-bold text-base">{t('ageGateAbove16')}</p>
            <p className="text-xs opacity-70 mt-1">{t('ageGateAbove16Desc')}</p>
          </button>

          <button
            onClick={() => setSelectedAge('between')}
            className={`w-full p-4 rounded-2xl border-2 text-start transition-all ${
              selectedAge === 'between'
                ? 'border-amber-400 bg-amber-400/10 text-white'
                : 'border-white/20 bg-white/5 text-white/80 hover:border-white/40'
            }`}
          >
            <p className="font-bold text-base">{t('ageGate13to16')}</p>
            <p className="text-xs opacity-70 mt-1">{t('ageGate13to16Desc')}</p>
          </button>

          <button
            onClick={() => setSelectedAge('under')}
            className={`w-full p-4 rounded-2xl border-2 text-start transition-all ${
              selectedAge === 'under'
                ? 'border-red-400 bg-red-400/10 text-white'
                : 'border-white/20 bg-white/5 text-white/80 hover:border-white/40'
            }`}
          >
            <p className="font-bold text-base">{t('ageGateUnder13')}</p>
            <p className="text-xs opacity-70 mt-1">{t('ageGateUnder13Desc')}</p>
          </button>
        </div>

        <Button
          onClick={handleConfirm}
          disabled={!selectedAge}
          className="w-full rounded-2xl h-12 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-base disabled:opacity-30"
        >
          {t('ageGateConfirm')}
        </Button>

        <p className="text-[10px] text-white/40 text-center leading-relaxed">
          {t('ageGateLegal')}
        </p>
      </div>
    </div>
  );
}
