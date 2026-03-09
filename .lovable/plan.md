

## Problem

The goals card (`أكمل أهداف اليوم`) uses `-mt-12` to overlap into the hero image, but when the notification prompt, occasion banner, or location error banner appear between the hero and the goals card, they get stacked/overlapped because the negative margin pulls the goals card up on top of them.

From the screenshot: the notification prompt is partially hidden behind the goals card.

## Fix

**Reorder the layout** so the goals card comes immediately after the hero image (where `-mt-12` makes visual sense), and move the conditional banners (notification prompt, occasion banner, location error) below the goals card.

### Changes in `src/pages/Index.tsx`:

**Current order** (lines 170-257):
1. Hero image end
2. AdBanner (home-top)
3. OccasionBanner
4. Location error banner
5. Notification prompt
6. Goals card (`-mt-12`)

**New order:**
1. Hero image end
2. Goals card (`-mt-12`) — stays right after hero so negative margin works correctly
3. AdBanner (home-top)
4. OccasionBanner
5. Notification prompt
6. Location error banner

This ensures the `-mt-12` only pulls the goals card into the hero image area, and all conditional banners render below it with proper spacing and no overlap.

### File: `src/pages/Index.tsx`
- Move the goals card block (lines 223-257) to right after line 170 (after hero image closes)
- Move AdBanner, OccasionBanner, location error, and notification prompt blocks to after the goals card
- All blocks keep their existing `mb-4`/`mb-5` spacing

