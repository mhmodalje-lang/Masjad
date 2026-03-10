

## Plan: Fix Mosque Filters & Auto-Check Availability

### Problems Found (from logs)

1. **False name matches**: "مسجد السلام As-Salam Moschee Osnabrück" incorrectly matched "Ibrahim Al-Khalil Moschee Osnabrück" because they share the city word "Osnabrück". The `namesMatch` function counts city names as valid matches.

2. **All mosques sent with same coordinates**: Every edge function call uses `lat=52.263197 lon=8.041693` (user's location). The Mawaqit API returns the same 6 mosques for every request because it searches by proximity. Each mosque has its own coordinates from OpenStreetMap but they're not being used.

3. **Filter tabs show 0/0**: `hasAutoSync` is `undefined` for all mosques because `autoCheckAvailability` was removed. The filter tabs for "تلقائي" and "يدوي" are always empty.

### Changes

#### 1. Fix `supabase/functions/fetch-mosque-times/index.ts` — Stricter name matching
- Add a stop-words list: city names like "Osnabrück", "Berlin", etc. and generic words like "Moschee", "e.V.", "Islamische", "Gemeinschaft" should NOT count as name matches
- Require at least 1 **unique/distinctive** word match (not generic terms)
- Use mosque's own coordinates in the Mawaqit search URL so the API returns results near THAT mosque, not the user

#### 2. Fix `src/pages/MosquePrayerTimes.tsx` — Auto-check availability (batched)
- After mosques load, auto-check availability for all mosques in batches of 3 with 500ms delays between batches
- This populates `hasAutoSync` so filter tabs work
- Use each mosque's own `latitude`/`longitude` when calling the edge function
- Fix the `loadTimesForMosque` to pass mosque's own coordinates (not `getCalcSettings()` which returns user's location)

#### 3. Ensure `selectMosque` and `loadTimesForMosque` use mosque coordinates
- Currently `getCalcSettings()` returns the user's cached location — only use this for `method` and `school` settings, NOT for lat/lon
- Always pass `mosque.latitude` and `mosque.longitude` to the edge function

