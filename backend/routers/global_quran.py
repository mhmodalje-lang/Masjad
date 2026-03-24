"""
Global Quran Verse API — V2026 Architecture Overhaul
=====================================================
SINGLE unified endpoint for fetching Quran verses with translation + explanation.
Used by the GlobalQuranVerse frontend component across ALL pages.

Design: One endpoint returns everything needed to render a verse:
- Arabic text (Uthmani script)
- Translation in user's language
- Concise explanation/tafsir (short, NOT 10-page Ibn Kathir)
- Audio URL
- Surah metadata

ID Mapping (Quran.com API v4):
- MAIN TRANSLATIONS: Used for verse display
- EXPLANATION IDs: Used for "Show Explanation" button (different scholarly source)
"""

import re
import httpx
from fastapi import APIRouter, Query
from datetime import datetime, timedelta

from deps import db

router = APIRouter(tags=["global-quran"])

QURAN_V4_BASE = "https://api.quran.com/api/v4"

# ═══════════════════════════════════════════════════════════════
# MAIN TRANSLATION IDs — for verse display in user's language
# ═══════════════════════════════════════════════════════════════
MAIN_TRANSLATION_IDS = {
    "en": 20,    # Saheeh International
    "de": 27,    # Frank Bubenheim & Nadeem
    "fr": 31,    # Muhammad Hamidullah
    "tr": 77,    # Diyanet İşleri
    "ru": 79,    # Abu Adel
    "sv": 48,    # Knut Bernström
    "nl": 144,   # Sofian S. Siregar
    "el": 0,     # Greek via QuranEnc (handled separately)
}

# ═══════════════════════════════════════════════════════════════
# EXPLANATION IDs — for "Show Explanation/Tafsir" button
# These are DIFFERENT from main translations to provide a
# second scholarly perspective. Short & concise.
# ═══════════════════════════════════════════════════════════════

# Languages with NATIVE tafsir on Quran.com (use tafsir endpoint)
TAFSIR_IDS = {
    "ar": 16,    # Tafsir Al-Muyassar (التفسير الميسر) — concise Arabic
    "ru": 170,   # Al-Sa'di (Тафсир ас-Саади) — concise Russian
}

# Languages using a SECOND translation as explanation (use translation endpoint)
EXPLANATION_TRANSLATION_IDS = {
    "en": 85,    # Abdel Haleem (concise modern English, NOT Ibn Kathir 169)
    "de": 208,   # Abu Reda (vs main Bubenheim 27)
    "fr": 136,   # Montada Islamic Foundation (vs main Hamidullah 31)
    "tr": 52,    # Elmalılı Hamdi Yazır (vs main Diyanet 77)
    "sv": 0,     # Only 1 Swedish translation → use Arabic Al-Muyassar
    "nl": 235,   # Abdalsalaam (vs main Siregar 144)
    "el": 0,     # Greek via QuranEnc
}

# Explanation source labels per language
EXPLANATION_SOURCE_LABELS = {
    "ar": "التفسير الميسر — مجمع الملك فهد",
    "en": "Dr. Mustafa Khattab — Abdel Haleem",
    "ru": "Краткое толкование — ас-Саади",
    "de": "Abu Reda Muhammad ibn Ahmad",
    "fr": "Fondation Islamique Montada",
    "tr": "Elmalılı Hamdi Yazır",
    "sv": "التفسير الميسر (Arabisk)",
    "nl": "Malak Faris Abdalsalaam",
    "el": "Κέντρο Μετάφρασης Ρουάντ",
}

CACHE_TTL_DAYS = 30


def _clean_html(text: str) -> str:
    """Strip HTML tags and entities from API response text."""
    text = re.sub(r'<sup[^>]*>[\s\S]*?</sup>', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    return text.replace('&nbsp;', ' ').strip()


async def _fetch_quranenc_greek(surah: int, ayah: int) -> str:
    """Fetch Greek translation from QuranEnc.com (Rowwad)."""
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.get(
                f"https://quranenc.com/api/v1/translation/aya/greek_rwwad/{surah}/{ayah}"
            )
            if r.status_code == 200:
                data = r.json()
                return data.get("result", {}).get("translation", "")
    except Exception:
        pass
    return ""


@router.get("/quran/v4/global-verse/bulk/{surah_id}")
async def get_global_verses_bulk(
    surah_id: int,
    language: str = Query("ar"),
    from_ayah: int = Query(1),
    to_ayah: int = Query(7),
):
    """
    Bulk fetch multiple verses for a surah range.
    Used by the Quran reader for full surah display.
    """
    base_lang = language.split("-")[0]
    verses = []

    # Fetch all verses at once from Quran.com v4
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            main_tr_id = MAIN_TRANSLATION_IDS.get(base_lang, 20)
            params = {
                "fields": "text_uthmani",
                "words": "false",
                "per_page": to_ayah - from_ayah + 1,
                "page": 1,
            }
            if base_lang != "ar" and main_tr_id > 0:
                params["translations"] = str(main_tr_id)

            r = await c.get(
                f"{QURAN_V4_BASE}/verses/by_chapter/{surah_id}",
                params=params,
            )
            r.raise_for_status()
            data = r.json()

            for v in data.get("verses", []):
                vn = v.get("verse_number", 0)
                if from_ayah <= vn <= to_ayah:
                    tr_text = ""
                    if v.get("translations"):
                        tr_text = _clean_html(v["translations"][0].get("text", ""))
                    verses.append({
                        "verse_key": f"{surah_id}:{vn}",
                        "verse_number": vn,
                        "arabic_text": v.get("text_uthmani", ""),
                        "translation": tr_text,
                        "audio_url": f"https://everyayah.com/data/Alafasy_128kbps/{str(surah_id).zfill(3)}{str(vn).zfill(3)}.mp3",
                    })
    except Exception:
        pass

    # Handle Greek separately
    if base_lang == "el":
        for v in verses:
            if not v["translation"]:
                sn, an = v["verse_key"].split(":")
                v["translation"] = await _fetch_quranenc_greek(int(sn), int(an))

    return {
        "success": True,
        "surah_id": surah_id,
        "language": base_lang,
        "verses": verses,
        "total": len(verses),
    }


@router.get("/quran/v4/global-verse/{surah_id}/{ayah_id}")
async def get_global_verse(
    surah_id: int,
    ayah_id: int,
    language: str = Query("ar"),
):
    """
    V2026 Global Quran Verse Endpoint.
    Returns everything needed to render a single verse:
    - Arabic text, translation, concise explanation, audio, surah metadata.
    Used by GlobalQuranVerse component across ALL pages.
    """
    base_lang = language.split("-")[0]
    verse_key = f"{surah_id}:{ayah_id}"

    # ── Check cache ──
    cache_key = f"global_verse_v2_{base_lang}_{verse_key}"
    try:
        cached = await db.global_verse_cache.find_one({
            "cache_key": cache_key,
            "expires_at": {"$gt": datetime.utcnow()},
        })
        if cached:
            return {
                "success": True,
                "verse_key": verse_key,
                "arabic_text": cached.get("arabic_text", ""),
                "translation": cached.get("translation", ""),
                "explanation": cached.get("explanation", ""),
                "explanation_source": cached.get("explanation_source", ""),
                "surah_name": cached.get("surah_name", ""),
                "surah_name_translated": cached.get("surah_name_translated", ""),
                "verse_number": ayah_id,
                "audio_url": cached.get("audio_url", ""),
                "language": base_lang,
                "cached": True,
            }
    except Exception:
        pass

    # ── Fetch Arabic text + main translation from Quran.com v4 ──
    arabic_text = ""
    translation = ""
    surah_name = ""
    surah_name_translated = ""

    try:
        async with httpx.AsyncClient(timeout=30) as c:
            # Fetch verse with translation
            main_tr_id = MAIN_TRANSLATION_IDS.get(base_lang, 20)
            params = {
                "fields": "text_uthmani",
                "words": "false",
            }
            if base_lang != "ar" and main_tr_id > 0:
                params["translations"] = str(main_tr_id)

            r = await c.get(f"{QURAN_V4_BASE}/verses/by_key/{verse_key}", params=params)
            r.raise_for_status()
            data = r.json()
            verse_data = data.get("verse", {})
            arabic_text = verse_data.get("text_uthmani", "")

            if verse_data.get("translations"):
                translation = _clean_html(verse_data["translations"][0].get("text", ""))

            # Fetch surah metadata
            r2 = await c.get(f"{QURAN_V4_BASE}/chapters/{surah_id}", params={"language": language})
            if r2.status_code == 200:
                ch_data = r2.json().get("chapter", {})
                surah_name = ch_data.get("name_arabic", "")
                surah_name_translated = ch_data.get("translated_name", {}).get("name", ch_data.get("name_simple", ""))
    except Exception:
        pass

    # ── Handle Greek translation (QuranEnc) ──
    if base_lang == "el" and not translation:
        translation = await _fetch_quranenc_greek(surah_id, ayah_id)

    # ── Fetch concise explanation ──
    explanation = ""
    explanation_source = EXPLANATION_SOURCE_LABELS.get(base_lang, "")

    # Strategy 1: Languages with native tafsir (ar, ru)
    if base_lang in TAFSIR_IDS:
        tafsir_id = TAFSIR_IDS[base_lang]
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.get(f"{QURAN_V4_BASE}/tafsirs/{tafsir_id}/by_ayah/{verse_key}")
                r.raise_for_status()
                data = r.json()
                raw = data.get("tafsir", {}).get("text", "")
                explanation = _clean_html(raw)
        except Exception:
            pass

    # Strategy 2: Languages using a second translation as explanation
    elif base_lang in EXPLANATION_TRANSLATION_IDS:
        expl_id = EXPLANATION_TRANSLATION_IDS[base_lang]
        if expl_id > 0:
            try:
                async with httpx.AsyncClient(timeout=30) as c:
                    r = await c.get(
                        f"{QURAN_V4_BASE}/verses/by_key/{verse_key}",
                        params={"translations": str(expl_id), "fields": "text_uthmani", "words": "false"},
                    )
                    r.raise_for_status()
                    data = r.json()
                    trs = data.get("verse", {}).get("translations", [])
                    if trs:
                        explanation = _clean_html(trs[0].get("text", ""))
            except Exception:
                pass
        elif base_lang == "sv":
            # Swedish: use Arabic Al-Muyassar as explanation
            try:
                async with httpx.AsyncClient(timeout=30) as c:
                    r = await c.get(f"{QURAN_V4_BASE}/tafsirs/16/by_ayah/{verse_key}")
                    r.raise_for_status()
                    data = r.json()
                    explanation = _clean_html(data.get("tafsir", {}).get("text", ""))
            except Exception:
                pass
        elif base_lang == "el":
            # Greek: use QuranEnc footnotes or same translation
            explanation = translation  # Same source for now

    # ── Build audio URL (EveryAyah CDN — Alafasy) ──
    audio_url = f"https://everyayah.com/data/Alafasy_128kbps/{str(surah_id).zfill(3)}{str(ayah_id).zfill(3)}.mp3"

    # ── Cache result ──
    result = {
        "arabic_text": arabic_text,
        "translation": translation,
        "explanation": explanation,
        "explanation_source": explanation_source,
        "surah_name": surah_name,
        "surah_name_translated": surah_name_translated,
        "audio_url": audio_url,
    }
    try:
        await db.global_verse_cache.update_one(
            {"cache_key": cache_key},
            {"$set": {
                **result,
                "cache_key": cache_key,
                "cached_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(days=CACHE_TTL_DAYS),
            }},
            upsert=True,
        )
    except Exception:
        pass

    return {
        "success": True,
        "verse_key": verse_key,
        **result,
        "verse_number": ayah_id,
        "language": base_lang,
        "cached": False,
    }
