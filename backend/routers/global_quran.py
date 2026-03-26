"""
Global Quran API — SINGLE LANGUAGE EXPERIENCE with INTELLIGENT FALLBACK
========================================================================
كل مستخدم يرى القرآن بلغته فقط. بدون خلط لغات.
Every user sees the Quran in their OWN language ONLY. No language mixing.

TAFSIR STRATEGY (V2026 — Sharia-Compliant Fallback):
====================================================
Primary Sources (Native Language):
- Arabic users → Arabic text + التفسير الميسر (Tafsir Al-Muyassar)
- English users → English text + Ibn Kathir
- Russian users → Russian text + Al-Sa'di (Elmir Kuliev)
- Turkish users → Turkish text + QuranEnc footnotes (Rowwad)
- French users → French text + QuranEnc footnotes (Rachid Maash)
- German users → German text + QuranEnc footnotes (Bubenheim)
- Dutch users → Dutch text + QuranEnc footnotes (Rowwad Center)

Fallback (For languages without native tafsir):
- Swedish users → Swedish text + English Ibn Kathir (fallback)
- Greek users → Greek text + English Ibn Kathir (fallback)

CRITICAL RULES:
- NEVER show Arabic tafsir to non-Arabic users
- NEVER use machine translation (Google Translate, etc.)
- ALL sources are authentic Islamic scholarly works
- Fallback is ONLY to English Ibn Kathir (never Arabic)

ALL from authentic Islamic sources. NO AI/LLM content.
"""

import re
import httpx
import logging
from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from deps import db

logger = logging.getLogger(__name__)
router = APIRouter(tags=["global-quran"])

QURAN_V4_BASE = "https://api.quran.com/api/v4"
QURANENC_BASE = "https://quranenc.com/api/v1"

# ═══════ QuranEnc keys (authentic Islamic source) ═══════
QURANENC_KEYS = {
    "tr": "turkish_rwwad",
    "de": "german_bubenheim",
    "fr": "french_rashid",
    "nl": "dutch_center",
}

# ═══════ Quran.com translation IDs ═══════
QURANCOM_IDS = {
    "en": 20,   # Saheeh International
    "ru": 79,   # Abu Adel
    "sv": 48,   # Knut Bernström
    "el": 20,   # English fallback
}

# ═══════ Real Tafsir IDs (Quran.com) ═══════
REAL_TAFSIR_IDS = {
    "ar": 16,   # التفسير الميسر
    "en": 169,  # Ibn Kathir
    "ru": 170,  # As-Sa'di
}

# Languages with QuranEnc footnotes (used as tafsir)
QURANENC_TAFSIR = {"fr", "de", "tr", "nl"}

TAFSIR_SOURCES = {
    "ar": "التفسير الميسر — مجمع الملك فهد",
    "en": "Tafsir Ibn Kathir",
    "ru": "Тафсир ас-Саади (Elmir Kuliev)",
    "fr": "Notes — Rachid Maash (QuranEnc)",
    "de": "Erläuterungen — Bubenheim (QuranEnc)",
    "tr": "Açıklamalar — Ruvvâd Merkezi (QuranEnc)",
    "nl": "Toelichtingen — Rowwad (QuranEnc)",
    "sv": "Tafsir Ibn Kathir (English fallback)",
    "el": "Tafsir Ibn Kathir (English fallback)",
}

CACHE_TTL = 30  # days


def _clean(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'<sup[^>]*>[\s\S]*?</sup>', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&amp;', '&')
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'")
    text = re.sub(r'\n\s*\n', '\n', text).strip()
    return re.sub(r'  +', ' ', text)


# ═══════════════════════════════════════════════════════════
# FETCHERS
# ═══════════════════════════════════════════════════════════

async def _quranenc_sura(chapter: int, key: str) -> dict:
    """Fetch entire sura from QuranEnc → {ayah: {text, footnotes}}"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURANENC_BASE}/translation/sura/{key}/{chapter}")
            r.raise_for_status()
            out = {}
            for v in r.json().get("result", []):
                n = int(v.get("aya", 0))
                fn = v.get("footnotes", "") or ""
                if fn:
                    fn = re.sub(r'\[\d+\]\s*', '', fn).strip()
                out[n] = {"text": v.get("translation", ""), "footnotes": fn}
            return out
    except Exception:
        return {}


async def _quranenc_verse(surah: int, ayah: int, key: str) -> dict:
    """Fetch single verse from QuranEnc → {text, footnotes}"""
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.get(f"{QURANENC_BASE}/translation/aya/{key}/{surah}/{ayah}")
            if r.status_code == 200:
                res = r.json().get("result", {})
                fn = res.get("footnotes", "") or ""
                if fn:
                    fn = re.sub(r'\[\d+\]\s*', '', fn).strip()
                return {"text": res.get("translation", ""), "footnotes": fn}
    except Exception:
        pass
    return {"text": "", "footnotes": ""}


async def _qurancom_tafsir(surah: int, ayah: int, tafsir_id: int) -> str:
    """Fetch real tafsir from Quran.com."""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/tafsirs/{tafsir_id}/by_ayah/{surah}:{ayah}")
            r.raise_for_status()
            return _clean(r.json().get("tafsir", {}).get("text", ""))
    except Exception:
        return ""


async def _get_tafsir(surah: int, ayah: int, lang: str) -> tuple:
    """
    Get tafsir with intelligent fallback system.
    
    Priority:
    1. Try user's language first
    2. If not available, fall back to English Ibn Kathir (for non-Arabic users)
    3. NEVER show Arabic tafsir to non-Arabic users
    
    Returns (text, source) or ("","")
    """
    # PRIMARY SOURCE: Try user's language first
    
    # Quran.com real tafsir: ar, en, ru
    if lang in REAL_TAFSIR_IDS:
        text = await _qurancom_tafsir(surah, ayah, REAL_TAFSIR_IDS[lang])
        if text:
            logger.info(f"✅ Tafsir found for {lang} (Quran.com ID {REAL_TAFSIR_IDS[lang]}): {surah}:{ayah}")
            return text, TAFSIR_SOURCES.get(lang, "")

    # QuranEnc footnotes: fr, de, tr, nl
    if lang in QURANENC_KEYS and lang in QURANENC_TAFSIR:
        data = await _quranenc_verse(surah, ayah, QURANENC_KEYS[lang])
        if data.get("footnotes"):
            logger.info(f"✅ Tafsir found for {lang} (QuranEnc): {surah}:{ayah}")
            return data["footnotes"], TAFSIR_SOURCES.get(lang, "")
    
    # FALLBACK: For languages without tafsir (sv, el, etc.), use English Ibn Kathir
    # CRITICAL: Only for non-Arabic users
    if lang != "ar":
        logger.warning(f"⚠️ No native tafsir for {lang}, falling back to English Ibn Kathir: {surah}:{ayah}")
        text = await _qurancom_tafsir(surah, ayah, 169)  # English Ibn Kathir
        if text:
            return text, "Tafsir Ibn Kathir (English fallback)"
    
    # Last resort: no tafsir available
    logger.error(f"❌ No tafsir available for {lang}: {surah}:{ayah}")
    return "", ""


# ═══════════════════════════════════════════════════════════
# BULK VERSES — كل آيات السورة بلغة المستخدم فقط
# ═══════════════════════════════════════════════════════════

@router.get("/quran/v4/global-verse/bulk/{surah_id}")
async def bulk_verses(
    surah_id: int,
    language: str = Query("ar"),
    from_ayah: int = Query(1),
    to_ayah: int = Query(7),
):
    """Returns verses in user's language ONLY. No language mixing."""
    lang = language.split("-")[0]
    verses = []

    if lang == "ar":
        # Arabic: get original text from Quran.com
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.get(f"{QURAN_V4_BASE}/verses/by_chapter/{surah_id}",
                    params={"fields": "text_uthmani", "words": "false", "per_page": to_ayah - from_ayah + 1})
                r.raise_for_status()
                for v in r.json().get("verses", []):
                    vn = v.get("verse_number", 0)
                    if from_ayah <= vn <= to_ayah:
                        verses.append({
                            "verse_key": f"{surah_id}:{vn}",
                            "verse_number": vn,
                            "text": v.get("text_uthmani", ""),
                            "audio_url": f"https://everyayah.com/data/Alafasy_128kbps/{str(surah_id).zfill(3)}{str(vn).zfill(3)}.mp3",
                        })
        except Exception:
            pass

    elif lang in QURANENC_KEYS:
        # QuranEnc languages: tr, de, fr, nl
        qenc = await _quranenc_sura(surah_id, QURANENC_KEYS[lang])
        for vn in range(from_ayah, to_ayah + 1):
            d = qenc.get(vn, {})
            if d.get("text"):
                verses.append({
                    "verse_key": f"{surah_id}:{vn}",
                    "verse_number": vn,
                    "text": d["text"],
                    "audio_url": f"https://everyayah.com/data/Alafasy_128kbps/{str(surah_id).zfill(3)}{str(vn).zfill(3)}.mp3",
                })

    else:
        # Quran.com languages: en, ru, sv, el
        tr_id = QURANCOM_IDS.get(lang, 20)
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.get(f"{QURAN_V4_BASE}/verses/by_chapter/{surah_id}",
                    params={"fields": "text_uthmani", "words": "false",
                            "translations": str(tr_id), "per_page": to_ayah - from_ayah + 1})
                r.raise_for_status()
                for v in r.json().get("verses", []):
                    vn = v.get("verse_number", 0)
                    if from_ayah <= vn <= to_ayah:
                        text = ""
                        if v.get("translations"):
                            text = _clean(v["translations"][0].get("text", ""))
                        verses.append({
                            "verse_key": f"{surah_id}:{vn}",
                            "verse_number": vn,
                            "text": text,
                            "audio_url": f"https://everyayah.com/data/Alafasy_128kbps/{str(surah_id).zfill(3)}{str(vn).zfill(3)}.mp3",
                        })
        except Exception:
            pass

    return {"success": True, "surah_id": surah_id, "language": lang, "verses": verses, "total": len(verses)}


# ═══════════════════════════════════════════════════════════
# SINGLE VERSE + TAFSIR — بلغة المستخدم فقط
# ═══════════════════════════════════════════════════════════

@router.get("/quran/v4/global-verse/{surah_id}/{ayah_id}")
async def single_verse(
    surah_id: int,
    ayah_id: int,
    language: str = Query("ar"),
):
    """Returns verse + tafsir in user's language ONLY. No mixing."""
    lang = language.split("-")[0]
    verse_key = f"{surah_id}:{ayah_id}"

    # Check cache
    cache_key = f"gv5_{lang}_{verse_key}"
    try:
        cached = await db.global_verse_cache.find_one(
            {"cache_key": cache_key, "expires_at": {"$gt": datetime.utcnow()}})
        if cached:
            return {
                "success": True, "verse_key": verse_key, "verse_number": ayah_id,
                "text": cached.get("text", ""),
                "arabic_text": cached.get("arabic_text", ""),
                "translation": cached.get("translation", ""),
                "tafsir": cached.get("tafsir", ""),
                "tafsir_source": cached.get("tafsir_source", ""),
                "surah_name": cached.get("surah_name", ""),
                "surah_name_translated": cached.get("surah_name_translated", ""),
                "audio_url": cached.get("audio_url", ""),
                "language": lang, "cached": True,
            }
    except Exception:
        pass

    # ── Always fetch Arabic text for all languages ──
    arabic_text = ""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/verses/by_key/{verse_key}",
                params={"fields": "text_uthmani", "words": "false"})
            r.raise_for_status()
            arabic_text = r.json().get("verse", {}).get("text_uthmani", "")
    except Exception:
        pass

    text = ""
    translation = ""
    surah_name = ""
    surah_name_translated = ""

    # Get verse text in user's language
    if lang == "ar":
        text = arabic_text
    elif lang in QURANENC_KEYS:
        d = await _quranenc_verse(surah_id, ayah_id, QURANENC_KEYS[lang])
        text = d.get("text", "")
        translation = text
    else:
        tr_id = QURANCOM_IDS.get(lang, 20)
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.get(f"{QURAN_V4_BASE}/verses/by_key/{verse_key}",
                    params={"fields": "text_uthmani", "words": "false", "translations": str(tr_id)})
                r.raise_for_status()
                vd = r.json().get("verse", {})
                if vd.get("translations"):
                    text = _clean(vd["translations"][0].get("text", ""))
                    translation = text
        except Exception:
            pass

    # Get surah name in user's language
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{QURAN_V4_BASE}/chapters/{surah_id}", params={"language": language})
            if r.status_code == 200:
                ch = r.json().get("chapter", {})
                if lang == "ar":
                    surah_name = ch.get("name_arabic", "")
                    surah_name_translated = surah_name
                else:
                    surah_name = ch.get("name_arabic", "")
                    surah_name_translated = ch.get("translated_name", {}).get("name", ch.get("name_simple", ""))
    except Exception:
        pass

    # Get tafsir in user's language ONLY
    tafsir_text, tafsir_source = await _get_tafsir(surah_id, ayah_id, lang)

    if tafsir_text and len(tafsir_text) > 2000:
        tafsir_text = tafsir_text[:2000].rsplit(' ', 1)[0] + "…"

    audio_url = f"https://everyayah.com/data/Alafasy_128kbps/{str(surah_id).zfill(3)}{str(ayah_id).zfill(3)}.mp3"

    result = {"text": text, "arabic_text": arabic_text, "translation": translation,
              "tafsir": tafsir_text, "tafsir_source": tafsir_source,
              "surah_name": surah_name, "surah_name_translated": surah_name_translated,
              "audio_url": audio_url}

    # Cache
    try:
        await db.global_verse_cache.update_one(
            {"cache_key": cache_key},
            {"$set": {**result, "cache_key": cache_key,
                      "cached_at": datetime.utcnow(),
                      "expires_at": datetime.utcnow() + timedelta(days=CACHE_TTL)}},
            upsert=True)
    except Exception:
        pass

    return {"success": True, "verse_key": verse_key, "verse_number": ayah_id,
            **result, "language": lang, "cached": False}
