import { useState, useEffect, createContext, useContext, type ReactNode } from 'react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface AdConfig {
  ads_enabled: boolean;
  video_ads_muted: boolean;
  gdpr_consent_required: boolean;
  ad_banner_enabled: boolean;
  ad_interstitial_enabled: boolean;
  ad_rewarded_enabled: boolean;
  admob_app_id: string;
  adsense_publisher_id: string;
}

const defaultConfig: AdConfig = {
  ads_enabled: true,
  video_ads_muted: true,
  gdpr_consent_required: true,
  ad_banner_enabled: true,
  ad_interstitial_enabled: false,
  ad_rewarded_enabled: true,
  admob_app_id: '',
  adsense_publisher_id: '',
};

const AdConfigContext = createContext<AdConfig>(defaultConfig);

export function AdConfigProvider({ children }: { children: ReactNode }) {
  const [config, setConfig] = useState<AdConfig>(defaultConfig);

  useEffect(() => {
    let mounted = true;
    fetch(`${BACKEND_URL}/api/ad-config`)
      .then(r => r.json())
      .then(data => {
        if (mounted) setConfig({ ...defaultConfig, ...data });
      })
      .catch(() => {});
    return () => { mounted = false; };
  }, []);

  return (
    <AdConfigContext.Provider value={config}>
      {children}
    </AdConfigContext.Provider>
  );
}

export function useAdConfig() {
  return useContext(AdConfigContext);
}
