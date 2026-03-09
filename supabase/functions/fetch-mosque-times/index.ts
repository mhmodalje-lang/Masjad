import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
};

interface MosqueTimes {
  fajr: string;
  sunrise: string;
  dhuhr: string;
  asr: string;
  maghrib: string;
  isha: string;
}

// ─── Well-known mosque aliases ───
const MOSQUE_ALIASES: Record<string, string[]> = {
  'المسجد الحرام': ['الكعبة', 'الحرم المكي', 'الحرم', 'masjid al-haram', 'kaaba', 'makkah', 'haram'],
  'المسجد النبوي': ['الحرم النبوي', 'الحرم المدني', 'masjid nabawi', 'prophets mosque', 'madinah'],
  'المسجد الأقصى': ['الاقصى', 'الأقصى', 'al-aqsa', 'aqsa'],
};

function getAliasSearchNames(mosqueName: string): string[] {
  const lower = mosqueName.toLowerCase().trim();
  const names: string[] = [];
  for (const [canonical, aliases] of Object.entries(MOSQUE_ALIASES)) {
    if (aliases.some(a => lower.includes(a) || a.includes(lower)) || lower.includes(canonical) || canonical.includes(lower)) {
      names.push(canonical);
      names.push(...aliases);
    }
  }
  return names;
}

// ─── Name matching ───
function namesMatch(requested: string, found: string): boolean {
  const normalize = (s: string) =>
    s.toLowerCase()
      .replace(/[\"''""]/g, ' ')
      .replace(/[^ -\u007F\w\s\u0600-\u06FF]/g, ' ')
      .replace(/\b(moschee|mosque|masjid|camii|cami|cmii|cmi|مسجد|جامع)\b/gi, ' ')
      .replace(/\s+/g, ' ').trim();
  const a = normalize(requested), b = normalize(found);
  if (!a || !b) return false;
  if (a === b) return true;
  if (a.includes(b) || b.includes(a)) return true;
  const aliasesA = getAliasSearchNames(requested);
  const aliasesB = getAliasSearchNames(found);
  if (aliasesA.length > 0 && aliasesB.length > 0) {
    const setA = new Set(aliasesA.map(normalize));
    if (aliasesB.some(al => setA.has(normalize(al)))) return true;
  }
  if (aliasesA.length > 0) {
    const nf = normalize(found);
    if (aliasesA.some(al => { const na = normalize(al); return na && (nf.includes(na) || na.includes(nf)); })) return true;
  }
  if (aliasesB.length > 0) {
    const na2 = normalize(requested);
    if (aliasesB.some(al => { const nb = normalize(al); return nb && (na2.includes(nb) || nb.includes(na2)); })) return true;
  }
  const wordsA = a.split(/\s+/).filter(w => w.length > 2);
  const wordsB = b.split(/\s+/).filter(w => w.length > 2);
  if (!wordsA.length || !wordsB.length) return false;
  return wordsA.filter(w => wordsB.some(wb => wb.includes(w) || w.includes(wb))).length >= 1;
}

// Extract max 3 search variants
function getSearchVariants(mosqueName: string): string[] {
  const variants: string[] = [mosqueName];
  const aliases = getAliasSearchNames(mosqueName);
  for (const alias of aliases) {
    if (!variants.includes(alias) && variants.length < 3) variants.push(alias);
  }
  if (variants.length < 3) {
    const cleaned = mosqueName
      .replace(/\b(moschee|mosque|masjid|camii|cami|cmii|cmi|e\.v\.|e\.V\.|مسجد|جامع)\b/gi, '')
      .replace(/\s+/g, ' ').trim();
    if (cleaned && cleaned !== mosqueName && variants.length < 3) variants.push(cleaned);
  }
  return variants.slice(0, 3);
}

// Fetch with 5s timeout
async function fetchWithTimeout(url: string, options: RequestInit = {}, timeoutMs = 5000): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

// ─── 1. Mawaqit API search ───
async function fetchFromMawaqitAPI(mosqueName: string, lat?: number, lon?: number): Promise<{ times: MosqueTimes; source: string; matchedName?: string } | null> {
  const variants = getSearchVariants(mosqueName);
  for (const searchWord of variants) {
    try {
      let url = `https://mawaqit.net/api/2.0/mosque/search?word=${encodeURIComponent(searchWord)}`;
      if (lat && lon) url += `&lat=${lat}&lon=${lon}`;
      const res = await fetchWithTimeout(url, { headers: { "User-Agent": "Mozilla/5.0", "Accept": "application/json" } });
      if (!res.ok) continue;
      const mosques = await res.json();
      if (!Array.isArray(mosques) || !mosques.length) continue;
      const mosque = mosques.find((m: any) => namesMatch(mosqueName, m.name || ''));
      if (!mosque?.times || mosque.times.length < 5) continue;
      const times: MosqueTimes = {
        fajr: mosque.times[0] || '', sunrise: mosque.times[1] || '',
        dhuhr: mosque.times[2] || '', asr: mosque.times[3] || '',
        maghrib: mosque.times[4] || '', isha: mosque.times[5] || '',
      };
      console.log(`Mawaqit matched: ${mosque.name} (search: "${searchWord}")`);
      return { times, source: 'mawaqit', matchedName: mosque.name };
    } catch { continue; }
  }
  return null;
}

// ─── 2. Mawaqit slug scrape ───
async function fetchByMawaqitSlug(slug: string): Promise<{ times: MosqueTimes; source: string } | null> {
  try {
    const res = await fetchWithTimeout(`https://mawaqit.net/en/m/${slug}`, { headers: { "User-Agent": "Mozilla/5.0" } });
    if (!res.ok) return null;
    const html = await res.text();
    const keys: (keyof MosqueTimes)[] = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha'];
    const times: MosqueTimes = { fajr: '', sunrise: '', dhuhr: '', asr: '', maghrib: '', isha: '' };
    const blocks = html.match(/<div class="[^"]*">\s*<div class="name">[^<]*<\/div>\s*<div class="time"><div>(\d{1,2}:\d{2})<\/div><\/div>/g);
    if (blocks && blocks.length >= 5) {
      const rx = /<div class="time"><div>(\d{1,2}:\d{2})<\/div><\/div>/;
      for (let i = 0; i < Math.min(blocks.length, 5); i++) {
        const m = blocks[i].match(rx);
        if (m) times[keys[i]] = m[1];
      }
    }
    const sr = html.match(/chourouk-id[^>]*><div>(\d{1,2}:\d{2})<\/div>/);
    if (sr) times.sunrise = sr[1];
    if (!Object.values(times).some(v => v)) return null;
    return { times, source: 'mawaqit' };
  } catch { return null; }
}

// ─── 3. Aladhan API (calculated) ───
async function fetchCalculatedTimes(lat: number, lon: number, method: number, school: number): Promise<{ times: MosqueTimes; source: string } | null> {
  try {
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const yyyy = today.getFullYear();
    const url = `https://api.aladhan.com/v1/timings/${dd}-${mm}-${yyyy}?latitude=${lat}&longitude=${lon}&method=${method}&school=${school}&adjustment=0`;
    const res = await fetchWithTimeout(url, {}, 8000);
    if (!res.ok) return null;
    const json = await res.json();
    const t = json?.data?.timings;
    if (!t) return null;
    const clean = (s: string) => s?.replace(/\s*\(.*\)$/, '').trim() || '';
    const times: MosqueTimes = {
      fajr: clean(t.Fajr), sunrise: clean(t.Sunrise),
      dhuhr: clean(t.Dhuhr), asr: clean(t.Asr),
      maghrib: clean(t.Maghrib), isha: clean(t.Isha),
    };
    return { times, source: 'calculated' };
  } catch { return null; }
}

// ─── 4. AI extraction from any website ───
async function extractTimesWithAI(websiteUrl: string): Promise<{ times: MosqueTimes; source: string } | null> {
  const GEMINI_API_KEY = Deno.env.get("GEMINI_API_KEY");
  if (!GEMINI_API_KEY) return null;
  try {
    const pageRes = await fetchWithTimeout(websiteUrl, { headers: { "User-Agent": "Mozilla/5.0" } });
    if (!pageRes.ok) return null;
    let html = await pageRes.text();
    if (html.length > 15000) html = html.substring(0, 15000);
    const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`;
    const prompt = `Extract prayer/salah times from this mosque website HTML.
I need IQAMAH times if available, otherwise ATHAN times.
Return ONLY JSON: {"fajr":"HH:MM","sunrise":"HH:MM","dhuhr":"HH:MM","asr":"HH:MM","maghrib":"HH:MM","isha":"HH:MM"}
Use 24h format. Empty string if not found. NO other text.

HTML:
${html}`;
    const geminiRes = await fetchWithTimeout(geminiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { temperature: 0.1, maxOutputTokens: 200 },
      }),
    }, 10000);
    if (!geminiRes.ok) return null;
    const geminiData = await geminiRes.json();
    const text = geminiData.candidates?.[0]?.content?.parts?.[0]?.text || '';
    const jsonMatch = text.match(/\{[\s\S]*?\}/);
    if (!jsonMatch) return null;
    const parsed = JSON.parse(jsonMatch[0]);
    const validTime = (t: string) => /^\d{1,2}:\d{2}$/.test(t);
    const times: MosqueTimes = {
      fajr: validTime(parsed.fajr) ? parsed.fajr : '',
      sunrise: validTime(parsed.sunrise) ? parsed.sunrise : '',
      dhuhr: validTime(parsed.dhuhr) ? parsed.dhuhr : '',
      asr: validTime(parsed.asr) ? parsed.asr : '',
      maghrib: validTime(parsed.maghrib) ? parsed.maghrib : '',
      isha: validTime(parsed.isha) ? parsed.isha : '',
    };
    if (!Object.values(times).some(v => v)) return null;
    return { times, source: 'website' };
  } catch { return null; }
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { mosqueName, mosqueCity, websiteUrl, mawaqitSlug, latitude, longitude, countryCode, method, school } = await req.json();
    console.log("fetch-mosque-times:", { mosqueName, mawaqitSlug, latitude, longitude, method, school });

    const userMethod = method ?? 3;
    const userSchool = school ?? 0;

    let result: { times: MosqueTimes; source: string; matchedName?: string } | null = null;

    // Priority 1: Direct Mawaqit slug
    if (!result && mawaqitSlug) {
      result = await fetchByMawaqitSlug(mawaqitSlug);
    }

    // Priority 2: Mawaqit API search by name
    if (!result && mosqueName) {
      result = await fetchFromMawaqitAPI(mosqueName, latitude, longitude);
    }

    // Priority 3: Website URL → check if Mawaqit, then AI scrape
    if (!result && websiteUrl) {
      const mawaqitMatch = websiteUrl.match(/mawaqit\.net\/\w+\/m\/([^/?]+)/);
      if (mawaqitMatch) result = await fetchByMawaqitSlug(mawaqitMatch[1]);
      if (!result) result = await extractTimesWithAI(websiteUrl);
    }

    // Priority 4: ALWAYS fall back to Aladhan calculated times
    if (!result && latitude && longitude) {
      result = await fetchCalculatedTimes(latitude, longitude, userMethod, userSchool);
    }

    return new Response(JSON.stringify({
      times: result?.times || null,
      source: result?.source || 'none',
      matchedName: result?.matchedName || null,
      success: !!result,
    }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (e) {
    console.error("Error:", e);
    return new Response(
      JSON.stringify({ error: e instanceof Error ? e.message : "Unknown error", success: false }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
