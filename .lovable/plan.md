

## Analysis

The `auth_raw_errors` security finding is **already resolved**. Auth.tsx (lines 50, 61) uses generic Arabic error messages — no raw Supabase errors are leaked to users.

However, there's a minor leak in `supabase/functions/auth-email-hook/index.ts` line 299 where `error.message` is returned in a JSON response. This is a server-side edge function response, not user-facing UI, but should still be fixed for defense in depth.

## Plan

1. **Fix edge function error leak** (`supabase/functions/auth-email-hook/index.ts` line 298-299): Replace `error.message` in the catch-all response with a generic `"Internal server error"` string. Keep `console.error` for logging.

2. **Dismiss the finding** if it still exists, since Auth.tsx is already safe.

That's the only change needed — a single line edit in the edge function.

