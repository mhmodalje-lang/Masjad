"""
Global Quran Verse API — V2026 AUTHENTIC ISLAMIC SOURCES REBUILD
================================================================
ALL translations and tafsir from AUTHENTIC Islamic sources ONLY.
NO LLM-generated tafsir. NO AI translation of religious content.

TRANSLATION SOURCES:
- ar: Original Arabic (Uthmani script)
- en: Saheeh International (Quran.com ID 20)
- de: Bubenheim & Elyas (QuranEnc german_bubenheim)
- fr: Rashid Maash (QuranEnc french_rashid) — with scholarly footnotes
- tr: Rowwad Translation Center (QuranEnc turkish_rwwad)
- ru: Abu Adel (Quran.com ID 79)
- sv: Knut Bernström (Quran.com ID 48)
- nl: Rowwad Translation Center (QuranEnc dutch_center)
- el: Quran.com English fallback (no Greek source on QuranEnc)

TAFSIR SOURCES (Real scholarly interpretation):
- ar: Al-Muyassar — King Fahd Complex
- en: Ibn Kathir Abridged (Quran.com ID 169)
- ru: As-Sa'di (Quran.com ID 170)
- fr: Scholarly footnotes from Rashid Maash (QuranEnc)
- tr: Scholarly footnotes from Turkish Rowwad (QuranEnc)
- de: Scholarly footnotes from Bubenheim (QuranEnc)
- Others: Arabic Al-Muyassar with clear language indicator
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

# ═══════════════════════════════════════════════════════════════
# QURANENC TRANSLATION KEYS — Authentic Islamic Sources
# ═══════════════════════════════════════════════════════════════
QURANENC_KEYS = {
    "tr": "turkish_rwwad",
    "de": "german_bubenheim",
    "fr": "french_rashid",
    "nl": "dutch_center",
}

QURANENC_HAS_FOOTNOTES = {"fr", "de", "tr", "nl"}

# ═══════════════════════════════════════════════════════════════
# QURAN.COM TRANSLATION IDs — for languages NOT on QuranEnc
# ═══════════════════════════════════════════════════════════════
QURANCOM_TRANSLATION_IDS = {
    "en": 20,
    "ru": 79,
    "sv": 48,
    "el": 20,  # English fallback for Greek
}

# ═══════════════════════════════════════════════════════════════
# REAL TAFSIR IDs (Quran.com) — Scholarly interpretation
# ═══════════════════════════════════════════════════════════════
REAL_TAFSIR_IDS = {
    "ar": 16,
    "en": 169,
    "ru": 170,
}

TAFSIR_SOURCE_LABELS = {
    "ar": "التفسير الميسر — مجمع الملك فهد لطباعة المصحف الشريف",
    "en": "Ibn Kathir — Tafsir of the Noble Quran",
    "ru": "Тафсир ас-Саади — шейх Абдуррахман ас-Саади",
    "fr": "Notes explicatives — Rachid Maash (QuranEnc)",
    "de": "Erläuterungen — Frank Bubenheim (QuranEnc)",
    "tr": "Açıklama Notları — Ruvvâd Tercüme Merkezi (QuranEnc)",
    "nl": "Toelichtingen — Rowwad Vertaalcentrum (QuranEnc)",
    "sv": "التفسير الميسر — Kung Fahds Komplex (Arabiska)",
    "el": "التفسير الميسر — Σύμπλεγμα Βασιλιά Φαχντ (Αραβικά)",
}

CACHE_TTL_DAYS = 30
MAX_TAFSIR_CHARS = 2000


def _clean_html(text: str) -> str:
    """Strip HTML tags and entities."""
    text = re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>', '', text, flags=re.DOTALL)
    text = re.sub(r'<sup[^>]*>[\s\S]*?</sup>', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&amp;', '&')
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'")
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()


async def _fetch_quranenc_verse(surah: int, ayah: int, key: str) -> dict:
    """Fetch translation + footnotes from QuranEnc.com (authentic Islamic source)."""
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.get(f"{QURANENC_BASE}/translation/aya/{key}/{surah}/{ayah}")
            if r.status_code == 200:
                data = r.json()
                result = data.get("result", {})
                if result:
                    translation = result.get("translation", "")
                    footnotes = result.get("footnotes", "") or ""
                    if footnotes:
                        footnotes = re.sub(r'\[\d+\]\s*', '', footnotes).strip()
                    return {"translation": translation, "footnotes": footnotes}
    except Exception:
        pass
    return {"translation": "", "footnotes": ""}


async def _fetch_quranenc_sura(chapter: int, key: str) -> dict:
    """Fetch entire sura from QuranEnc. Returns {ayah_num: {translation, footnotes}}."""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURANENC_BASE}/translation/sura/{key}/{chapter}")
            r.raise_for_status()
            data = r.json()
            result = {}
            for v in data.get("result", []):
                aya_num = int(v.get("aya", 0))
                footnotes = v.get("footnotes", "") or ""
                if footnotes:
                    footnotes = re.sub(r'\[\d+\]\s*', '', footnotes).strip()
                result[aya_num] = {
                    "translation": v.get("translation", ""),
                    "footnotes": footnotes,
                }
            return result
    except Exception:
        return {}


async def _fetch_real_tafsir(surah: int, ayah: int, tafsir_id: int) -> str:
    """Fetch REAL tafsir from Quran.com tafsir endpoint."""
    verse_key = f"{surah}:{ayah}"
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/tafsirs/{tafsir_id}/by_ayah/{verse_key}")
            r.raise_for_status()
            data = r.json()
            raw = data.get("tafsir", {}).get("text", "")
            return _clean_html(raw)
    except Exception:
        pass
    return ""


async def _get_tafsir(surah: int, ayah: int, base_lang: str) -> tuple:
    """Get tafsir from best authentic source. Returns (text, source, is_arabic)."""
    # Priority 1: Quran.com real tafsir (ar, en, ru)
    if base_lang in REAL_TAFSIR_IDS:
        text = await _fetch_real_tafsir(surah, ayah, REAL_TAFSIR_IDS[base_lang])
        if text:
            return text, TAFSIR_SOURCE_LABELS.get(base_lang, ""), False

    # Priority 2: QuranEnc scholarly footnotes (tr, fr, de, nl)
    if base_lang in QURANENC_KEYS and base_lang in QURANENC_HAS_FOOTNOTES:
        data = await _fetch_quranenc_verse(surah, ayah, QURANENC_KEYS[base_lang])
        if data.get("footnotes"):
            return data["footnotes"], TAFSIR_SOURCE_LABELS.get(base_lang, ""), False

    # Priority 3: Arabic Al-Muyassar (authentic Islamic source)
    text = await _fetch_real_tafsir(surah, ayah, 16)
    if text:
        return text, "التفسير الميسر — مجمع الملك فهد", True

    return "", "", False


@router.get("/quran/v4/global-verse/bulk/{surah_id}")
async def get_global_verses_bulk(
    surah_id: int,
    language: str = Query("ar"),
    from_ayah: int = Query(1),
    to_ayah: int = Query(7),
):
    """Bulk fetch verses — ALL from authentic Islamic sources."""
    base_lang = language.split("-")[0]
    verses = []

    quranenc_data = {}
    if base_lang in QURANENC_KEYS:
        quranenc_data = await _fetch_quranenc_sura(surah_id, QURANENC_KEYS[base_lang])

    try:
        async with httpx.AsyncClient(timeout=30) as c:
            params = {"fields": "text_uthmani", "words": "false", "per_page": to_ayah - from_ayah + 1, "page": 1}
            if not quranenc_data and base_lang != "ar":
                tr_id = QURANCOM_TRANSLATION_IDS.get(base_lang, 0)
                if tr_id > 0:
                    params["translations"] = str(tr_id)

            r = await c.get(f"{QURAN_V4_BASE}/verses/by_chapter/{surah_id}", params=params)
            r.raise_for_status()
            data = r.json()

            for v in data.get("verses", []):
                vn = v.get("verse_number", 0)
                if from_ayah <= vn <= to_ayah:
                    tr_text = ""
                    if quranenc_data and vn in quranenc_data:
                        tr_text = quranenc_data[vn].get("translation", "")
                    elif v.get("translations"):
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

    return {"success": True, "surah_id": surah_id, "language": base_lang, "verses": verses, "total": len(verses)}


@router.get("/quran/v4/global-verse/{surah_id}/{ayah_id}")
async def get_global_verse(
    surah_id: int,
    ayah_id: int,
    language: str = Query("ar"),
):
    """V2026 Global Quran Verse — AUTHENTIC ISLAMIC SOURCES ONLY."""
    base_lang = language.split("-")[0]
    verse_key = f"{surah_id}:{ayah_id}"

    cache_key = f"global_verse_v4_{base_lang}_{verse_key}"
    try:
        cached = await db.global_verse_cache.find_one({"cache_key": cache_key, "expires_at": {"$gt": datetime.utcnow()}})
        if cached:
            return {
                "success": True, "verse_key": verse_key,
                "arabic_text": cached.get("arabic_text", ""), "translation": cached.get("translation", ""),
                "tafsir": cached.get("tafsir", ""), "tafsir_source": cached.get("tafsir_source", ""),
                "tafsir_is_arabic": cached.get("tafsir_is_arabic", False),
                "surah_name": cached.get("surah_name", ""), "surah_name_translated": cached.get("surah_name_translated", ""),
                "verse_number": ayah_id, "audio_url": cached.get("audio_url", ""),
                "language": base_lang, "cached": True,
            }
    except Exception:
        pass

    arabic_text = ""
    translation = ""
    surah_name = ""
    surah_name_translated = ""

    if base_lang in QURANENC_KEYS:
        qenc_data = await _fetch_quranenc_verse(surah_id, ayah_id, QURANENC_KEYS[base_lang])
        translation = qenc_data.get("translation", "")

    try:
        async with httpx.AsyncClient(timeout=30) as c:
            params = {"fields": "text_uthmani", "words": "false"}
            if not translation and base_lang != "ar":
                tr_id = QURANCOM_TRANSLATION_IDS.get(base_lang, 20)
                if tr_id > 0:
                    params["translations"] = str(tr_id)

            r = await c.get(f"{QURAN_V4_BASE}/verses/by_key/{verse_key}", params=params)
            r.raise_for_status()
            data = r.json()
            verse_data = data.get("verse", {})
            arabic_text = verse_data.get("text_uthmani", "")

            if not translation and verse_data.get("translations"):
                translation = _clean_html(verse_data["translations"][0].get("text", ""))

            r2 = await c.get(f"{QURAN_V4_BASE}/chapters/{surah_id}", params={"language": language})
            if r2.status_code == 200:
                ch_data = r2.json().get("chapter", {})
                surah_name = ch_data.get("name_arabic", "")
                surah_name_translated = ch_data.get("translated_name", {}).get("name", ch_data.get("name_simple", ""))
    except Exception:
        pass

    tafsir_text, tafsir_source, tafsir_is_arabic = await _get_tafsir(surah_id, ayah_id, base_lang)

    if tafsir_text and len(tafsir_text) > MAX_TAFSIR_CHARS:
        tafsir_text = tafsir_text[:MAX_TAFSIR_CHARS].rsplit(' ', 1)[0] + "…"

    audio_url = f"https://everyayah.com/data/Alafasy_128kbps/{str(surah_id).zfill(3)}{str(ayah_id).zfill(3)}.mp3"

    result = {
        "arabic_text": arabic_text, "translation": translation,
        "tafsir": tafsir_text, "tafsir_source": tafsir_source,
        "tafsir_is_arabic": tafsir_is_arabic,
        "surah_name": surah_name, "surah_name_translated": surah_name_translated,
        "audio_url": audio_url,
    }
    try:
        await db.global_verse_cache.update_one(
            {"cache_key": cache_key},
            {"$set": {**result, "cache_key": cache_key, "cached_at": datetime.utcnow(), "expires_at": datetime.utcnow() + timedelta(days=CACHE_TTL_DAYS)}},
            upsert=True,
        )
    except Exception:
        pass

    return {"success": True, "verse_key": verse_key, **result, "verse_number": ayah_id, "language": base_lang, "cached": False}
