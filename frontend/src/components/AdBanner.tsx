import { useEffect, useRef, useState } from 'react';
import { Play, ExternalLink } from 'lucide-react';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || '';

interface AdData {
  id: string;
  name?: string;
  provider?: string;
  code?: string;
  placement?: string;
  ad_type?: string;
  enabled?: boolean;
  priority?: number;
  image_url?: string;
  link_url?: string;
}

function extractYouTubeID(url: string): string | null {
  const match = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]+)/);
  return match ? match[1] : null;
}

function isURL(str: string): boolean {
  return /^https?:\/\//.test(str.trim());
}

export function AdBanner({ position }: { position: string }) {
  const [ads, setAds] = useState<AdData[]>([]);
  const [loaded, setLoaded] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let mounted = true;
    fetch(`${BACKEND_URL}/api/ads/active?placement=${position}`)
      .then(r => r.json())
      .then(d => {
        if (!mounted) return;
        setAds(d.ads || []);
        setLoaded(true);
      })
      .catch(() => { if (mounted) setLoaded(true); });
    return () => { mounted = false; };
  }, [position]);

  // Execute ad scripts
  useEffect(() => {
    if (!containerRef.current || ads.length === 0) return;
    const ad = ads[0];
    const adCode = ad.code || '';
    // Only inject as HTML/script if it's actual script code (not a URL)
    if (!adCode || isURL(adCode)) return;

    const container = containerRef.current;
    while (container.firstChild) container.removeChild(container.firstChild);

    const temp = document.createElement('div');
    temp.innerHTML = adCode;
    const nonScriptHTML = adCode.replace(/<script[\s\S]*?<\/script>/gi, '');
    if (nonScriptHTML.trim()) {
      const wrapper = document.createElement('div');
      wrapper.innerHTML = nonScriptHTML;
      container.appendChild(wrapper);
    }
    const scripts = temp.querySelectorAll('script');
    scripts.forEach((origScript) => {
      const newScript = document.createElement('script');
      Array.from(origScript.attributes).forEach((attr) => newScript.setAttribute(attr.name, attr.value));
      if (origScript.textContent) newScript.textContent = origScript.textContent;
      container.appendChild(newScript);
    });
    return () => { while (container.firstChild) container.removeChild(container.firstChild); };
  }, [ads]);

  if (loaded && ads.length === 0) return null;
  if (!loaded) return null;

  const ad = ads[0];
  const adCode = ad.code || '';
  const provider = (ad.provider || '').toLowerCase();

  // YouTube ad - show as embedded video
  if (provider === 'youtube' || (isURL(adCode) && extractYouTubeID(adCode))) {
    const videoId = extractYouTubeID(adCode);
    if (videoId) {
      return (
        <div className="w-full my-3 px-4">
          <div className="w-full max-w-lg mx-auto rounded-2xl overflow-hidden border border-primary/10 bg-card shadow-sm">
            <div className="relative aspect-video bg-black">
              <iframe
                src={`https://www.youtube.com/embed/${videoId}?rel=0`}
                title={ad.name || 'فيديو'}
                className="w-full h-full"
                frameBorder={0}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
            {ad.name && (
              <div className="px-3 py-2 flex items-center justify-between">
                <span className="text-xs font-bold text-foreground truncate">{ad.name}</span>
                <span className="text-[9px] text-muted-foreground/50 bg-muted/50 px-1.5 py-0.5 rounded">إعلان</span>
              </div>
            )}
          </div>
        </div>
      );
    }
  }

  // Image ad (if image_url is present)
  if (ad.image_url) {
    const imgUrl = ad.image_url.startsWith('http') ? ad.image_url : `${BACKEND_URL}${ad.image_url}`;
    return (
      <div className="w-full my-3 px-4">
        <div className="w-full max-w-lg mx-auto rounded-2xl overflow-hidden border border-primary/10">
          {ad.link_url ? (
            <a href={ad.link_url} target="_blank" rel="noopener noreferrer nofollow">
              <img src={imgUrl} alt={ad.name || 'إعلان'} className="w-full rounded-t-2xl" loading="lazy" />
            </a>
          ) : (
            <img src={imgUrl} alt={ad.name || 'إعلان'} className="w-full rounded-t-2xl" loading="lazy" />
          )}
          <div className="bg-card px-3 py-1.5 flex items-center justify-between">
            {ad.name && <span className="text-[11px] text-foreground/70 font-medium truncate">{ad.name}</span>}
            <span className="text-[9px] text-muted-foreground/50">إعلان</span>
          </div>
        </div>
      </div>
    );
  }

  // URL ad (non-YouTube link)
  if (isURL(adCode) && !extractYouTubeID(adCode)) {
    return (
      <div className="w-full my-3 px-4">
        <a href={adCode} target="_blank" rel="noopener noreferrer nofollow"
          className="block w-full max-w-lg mx-auto rounded-2xl bg-card border border-primary/10 p-3 hover:bg-muted/30 transition-colors">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
              <ExternalLink className="h-5 w-5 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-foreground truncate">{ad.name || 'رابط'}</p>
              <p className="text-[10px] text-muted-foreground truncate">{adCode}</p>
            </div>
            <span className="text-[9px] text-muted-foreground/50 bg-muted/50 px-1.5 py-0.5 rounded shrink-0">إعلان</span>
          </div>
        </a>
      </div>
    );
  }

  // Script/code ad (Google AdSense, etc.)
  if (adCode && !isURL(adCode)) {
    return (
      <div className="w-full my-3 px-4">
        <div className="w-full max-w-lg mx-auto rounded-2xl overflow-hidden min-h-[50px]">
          <div ref={containerRef} className="w-full" />
        </div>
      </div>
    );
  }

  return null;
}

export function PopUnderLoader() {
  useEffect(() => {
    fetch(`${BACKEND_URL}/api/ads/active?placement=all`)
      .then(r => r.json())
      .then(d => {
        const ads = d.ads || [];
        const popupAds = ads.filter((ad: any) => ad.ad_type === 'popup' || ad.ad_type === 'interstitial');
        popupAds.forEach((ad: any) => {
          const code = ad.code || '';
          if (code && !isURL(code)) {
            const temp = document.createElement('div');
            temp.innerHTML = code;
            const scripts = temp.querySelectorAll('script');
            scripts.forEach((origScript) => {
              const newScript = document.createElement('script');
              Array.from(origScript.attributes).forEach((attr) => newScript.setAttribute(attr.name, attr.value));
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
