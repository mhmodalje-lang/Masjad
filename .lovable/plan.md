

## Comprehensive Bug Fix Plan

### Issues Found

**1. Progress bar calculation broken (Index.tsx line 80)**
`remaining` format is `"5h 30m"` or `"30m"` but the code does `remaining.split(':')` expecting `HH:MM:SS`. This produces `NaN` for progress, which could cascade into render issues.

**2. Stale closure in useGeoLocation error handler (line 126)**
`location.latitude` references the initial state value captured at render time, not the current value. Should use `prev` from the setter or a ref.

**3. Notification permissions not requested proactively**
The app only requests notification permission when the user manually toggles the bell icon. No onboarding prompt or automatic permission flow exists.

**4. usePrayerTimes skips fetch when lat/lon = 0 (line 72)**
If geolocation is denied and there's no cache, latitude/longitude stay at 0 and prayer times never load. Need to show a clear error UI.

**5. Notification timers cleared on re-render**
`useAthanNotifications` uses `scheduledRef` but doesn't account for when prayers array changes reference (e.g. mosque times loaded after API times).

### Plan

#### Fix 1: Progress bar calculation (Index.tsx)
- Parse `remaining` format (`"Xh Ym"` / `"Xm"`) correctly instead of splitting by `:`
- Extract hours and minutes with regex: `/(\d+)h\s*(\d+)m|(\d+)m/`

#### Fix 2: Stale closure in useGeoLocation
- Use `prev` argument in the `setLocation` callback inside the error handler:
  ```
  setLocation(prev => ({
    ...prev,
    loading: false,
    error: (prev.latitude !== 0 || prev.longitude !== 0) ? null : 'يرجى تفعيل...',
  }));
  ```

#### Fix 3: Show location error in Index.tsx
- When `location.error` is set and `prayers.length === 0`, show an error card with a "تفعيل الموقع" button that calls `location.detectLocation()`
- Replace the empty prayer grid with a clear message

#### Fix 4: Notification permission prompt
- On first app load, if `athan-notifications` is not set, show a one-time prompt card on the home page asking the user to enable notifications
- Card with bell icon + "تفعيل إشعارات الصلاة" button
- On click, request permission and enable notifications
- Store `notification-prompt-shown` in localStorage

#### Fix 5: Notification timer stability
- Remove the `scheduledRef` guard that prevents re-scheduling when prayers change
- Instead, always clear previous timers and reschedule when `prayers` array changes

### Files to change:
1. **`src/pages/Index.tsx`** — Fix progress parsing, add location error UI, add notification prompt card
2. **`src/hooks/useGeoLocation.tsx`** — Fix stale closure in error handler
3. **`src/hooks/useAthanNotifications.tsx`** — Remove scheduledRef guard, allow rescheduling
4. **`src/lib/prayerNotifications.ts`** — Already clears old timers (no change needed)

