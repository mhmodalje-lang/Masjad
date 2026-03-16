import { useEffect, useRef, useState, useCallback, useMemo } from 'react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface AdData {
  id: string;
  title?: string;
  description?: string;
  image_url?: string;
  link_url?: string;
  ad_code?: string;
  ad_type?: string;
  placement?: string;
  enabled?: boolean;
  priority?: number;
}

export function AdBanner({ position }: { position: string }) {
  const [ads, setAds] = useState<AdData[]>([]);
  const [loaded, setLoaded] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const tracked = useRef(false);

  useEffect(() => {
    let mounted = true;
    fetch(`${BACKEND_URL}/api/ads/placement/${position}`)
      .then(r => r.json())
      .then(d => {
        if (!mounted) return;
        setAds(d.ads || []);
        setLoaded(true);
      })
      .catch(() => {
        if (!mounted) return;
        setLoaded(true);
      });
    return () => { mounted = false; };
  }, [position]);

  // Track impression
  useEffect(() => {
    if (ads.length > 0 && !tracked.current) {
      tracked.current = true;
      // Track ad view
      ads.forEach(ad => {
        fetch(`${BACKEND_URL}/api/ads/watch/${ad.id}`, { method: 'POST' }).catch(() => {});
      });
    }
  }, [ads]);

  // Execute ad scripts
  useEffect(() => {
    if (!containerRef.current || ads.length === 0) return;
    const ad = ads[0];
    if (ad.ad_code && (ad.ad_type === 'script' || ad.ad_type === 'native' || ad.ad_type === 'adsense')) {
      const container = containerRef.current;
      const temp = document.createElement('div');
      temp.innerHTML = ad.ad_code;
      const scripts = temp.querySelectorAll('script');
      scripts.forEach((origScript) => {
        const newScript = document.createElement('script');
        Array.from(origScript.attributes).forEach((attr) => {
          newScript.setAttribute(attr.name, attr.value);
        });
        if (origScript.textContent) newScript.textContent = origScript.textContent;
        container.appendChild(newScript);
      });
      const nonScriptHTML = ad.ad_code.replace(/<script[\s\S]*?<\/script>/gi, '');
      if (nonScriptHTML.trim()) {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = nonScriptHTML;
        container.prepend(wrapper);
      }
      return () => { while (container.firstChild) container.removeChild(container.firstChild); };
    }
  }, [ads]);

  if (loaded && ads.length === 0) return null;
  if (!loaded) return null;

  const ad = ads[0];

  // Image ad
  if (ad.image_url) {
    const img = (
      <img src={ad.image_url.startsWith('http') ? ad.image_url : `${BACKEND_URL}${ad.image_url}`}
        alt={ad.title || 'إعلان'} className="w-full rounded-xl" loading="lazy" />
    );
    return (
      <div className="w-full flex justify-center my-3 px-4">
        <div className="w-full max-w-lg rounded-xl overflow-hidden border border-primary/10">
          {ad.link_url ? (
            <a href={ad.link_url} target="_blank" rel="noopener noreferrer nofollow">{img}</a>
          ) : img}
          <div className="bg-card/50 px-3 py-1.5 flex items-center justify-between">
            <span className="text-[9px] text-muted-foreground/50">إعلان</span>
            {ad.title && <span className="text-[10px] text-foreground/70 font-medium">{ad.title}</span>}
          </div>
        </div>
      </div>
    );
  }

  // Script/code ad
  if (ad.ad_code) {
    return (
      <div className="w-full flex justify-center my-3 px-4">
        <div className="w-full max-w-lg rounded-xl overflow-hidden">
          <div ref={containerRef} className="w-full bg-muted/10" />
        </div>
      </div>
    );
  }

  return null;
}

export function PopUnderLoader() {
  useEffect(() => {
    fetch(`${BACKEND_URL}/api/ads/active?placement=popunder`)
      .then(r => r.json())
      .then(d => {
        const ads = d.ads || [];
        ads.forEach((ad: any) => {
          if (ad.ad_code) {
            const temp = document.createElement('div');
            temp.innerHTML = ad.ad_code;
            const scripts = temp.querySelectorAll('script');
            scripts.forEach((origScript) => {
              const newScript = document.createElement('script');
              Array.from(origScript.attributes).forEach((attr) => {
                newScript.setAttribute(attr.name, attr.value);
              });
              if (origScript.textContent) newScript.textContent = origScript.textContent;
              document.head.appendChild(newScript);
            });
          }
        });
      })
      .catch(() => {});
  }, []);
  return null;
}
