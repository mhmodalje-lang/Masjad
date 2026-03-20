import i18n from '@/lib/i18nConfig';

export default function MosqueScene() {
  return (
    <div className="relative w-full h-48 overflow-hidden">
      <img
        src="/mecca-hero.webp"
        alt={i18n.t('holyMosque')}
        className="w-full h-full object-cover"
        loading="eager"
      />
      <div className="absolute inset-0 bg-gradient-to-b from-black/30 to-background" />
    </div>
  );
}
