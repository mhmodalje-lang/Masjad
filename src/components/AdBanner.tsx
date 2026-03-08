import { useEffect, useState } from 'react';
import { supabase } from '@/integrations/supabase/client';

interface AdSlot {
  id: string;
  name: string;
  slot_type: string;
  ad_code: string | null;
  position: string;
  is_active: boolean;
}

export function AdBanner({ position }: { position: string }) {
  const [ad, setAd] = useState<AdSlot | null>(null);

  useEffect(() => {
    supabase
      .from('ad_slots')
      .select('*')
      .eq('position', position)
      .eq('is_active', true)
      .limit(1)
      .single()
      .then(({ data }) => {
        if (data) setAd(data as AdSlot);
      });
  }, [position]);

  if (!ad || !ad.ad_code) return null;

  return (
    <div className="w-full flex justify-center my-3 px-4">
      <div
        className="w-full max-w-lg rounded-xl overflow-hidden bg-muted/30"
        dangerouslySetInnerHTML={{ __html: ad.ad_code }}
      />
    </div>
  );
}
