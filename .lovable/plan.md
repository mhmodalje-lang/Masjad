

## Two Features

### 1. PWA Auto-Update — Force new versions to reach all users

**Current state**: `registerType: "autoUpdate"` is set in vite config, but there's no user-facing prompt or forced reload when a new service worker is detected. Users with cached PWA may stay on old versions indefinitely.

**Plan**:
- In `src/main.tsx`, register the PWA update callback using `registerSW` from `virtual:pwa-register`
- When a new service worker is detected, show a toast notification ("تحديث جديد متوفر") with a "تحديث الآن" button
- On click, call `registration.update()` then `window.location.reload()`
- Also add `skipWaiting` in the workbox config so new service workers activate immediately
- Add a version check interval (every 30 minutes) to detect updates even while app is open

**Files to change**:
- `vite.config.ts`: Add `skipWaiting: true` and `clientsClaim: true` to workbox config
- `src/main.tsx`: Add SW registration with update prompt
- `src/components/layout/AppLayout.tsx`: Import and render update check component

### 2. Mosque List — Only show mosques with real prayer times

**Current state**: All nearby mosques from OpenStreetMap are shown. The `autoCheckAvailability` function checks each mosque against `fetch-mosque-times`, but mosques with `calculated` source (Aladhan coordinate-based, not mosque-specific) still show as available. The `hasAutoSync` flag doesn't distinguish between real mosque data (Mawaqit/website) and generic calculated times.

**Plan**:
- In `fetch-mosque-times` edge function: return the `source` field in the response (already done)
- In `MosquePrayerTimes.tsx` `autoCheckAvailability`: mark `hasAutoSync = true` ONLY when source is `mawaqit` or `website`, NOT when source is `calculated`
- Change the `checkMosqueAvailability` function similarly
- Update filter logic: "⚡ تلقائي" tab only shows mosques with real mosque-specific times
- Mosques with only `calculated` times show "أوقات حسابية فقط" instead of "⚡ أوقات تلقائية متوفرة"

**Files to change**:
- `supabase/functions/fetch-mosque-times/index.ts`: Ensure response always includes `source` field (already does)
- `src/pages/MosquePrayerTimes.tsx`: 
  - Update `autoCheckAvailability` and `checkMosqueAvailability` to check `data.source !== 'calculated'` for `hasAutoSync`
  - Add a third sync status: `hasAutoSync === true` (real), `hasAutoSync === false` (none), `hasAutoSync === 'calculated'` — or simpler: just check source in the response

### Technical Summary

```text
PWA Update Flow:
  New deploy → SW detects update → Toast appears → User clicks → Reload

Mosque Filter Flow:
  Search nearby → Check each against fetch-mosque-times → 
  source=mawaqit/website → ⚡ real times
  source=calculated → ⏳ calculated only  
  source=none → ✏️ manual only
```

