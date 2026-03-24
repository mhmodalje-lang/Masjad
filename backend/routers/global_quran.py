"""
Global Quran Verse API — V2026 REAL TAFSIR + LLM TRANSLATION
==============================================================
SINGLE unified endpoint. ALL 114 surahs, ALL 9 languages.

REAL TAFSIR SOURCES:
- ar: التفسير الميسر (Al-Muyassar) — مجمع الملك فهد
- en: Ibn Kathir Abridged (ID 169)
- ru: Тафсир ас-Саади (As-Sa'di) (ID 170)
- fr: QuranEnc french_rashid footnotes
- de/tr/sv/nl/el: LLM translation of Ibn Kathir into target language (cached in MongoDB)
"""

import os
import re
import httpx
import asyncio
import logging
from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from dotenv import load_dotenv

from deps import db

load_dotenv()
logger = logging.getLogger(__name__)

router = APIRouter(tags=["global-quran"])

QURAN_V4_BASE = "https://api.quran.com/api/v4"
QURANENC_BASE = "https://quranenc.com/api/v1"

# ═══════════════════════════════════════════════════════════════
# MAIN TRANSLATION IDs — for verse display (NOT tafsir)
# ═══════════════════════════════════════════════════════════════
MAIN_TRANSLATION_IDS = {
    "en": 20,    # Saheeh International
    "de": 27,    # Frank Bubenheim & Nadeem
    "fr": 31,    # Muhammad Hamidullah
    "tr": 77,    # Diyanet İşleri
    "ru": 79,    # Abu Adel
    "sv": 48,    # Knut Bernström
    "nl": 144,   # Sofian S. Siregar
    "el": 0,     # Greek via QuranEnc
}

# ═══════════════════════════════════════════════════════════════
# REAL TAFSIR SOURCES — Actual scholarly explanations
# Languages with Quran.com TAFSIR endpoint (REAL tafsir texts):
# ═══════════════════════════════════════════════════════════════
REAL_TAFSIR_IDS = {
    "ar": 16,    # التفسير الميسر — مجمع الملك فهد
    "en": 169,   # Ibn Kathir Abridged — Real tafsir with explanation
    "ru": 170,   # Тафсир ас-Саади
}

# Languages using QuranEnc footnotes (real explanatory notes):
QURANENC_TAFSIR_KEYS = {
    "fr": "french_rashid",       # Rashid Maash — has DETAILED footnotes
    "en_alt": "english_rwwad",   # English Rowwad — backup footnotes
}

# Languages that need LLM translation of tafsir
LLM_TAFSIR_LANGS = {"de", "tr", "sv", "nl", "el", "fr"}

# Tafsir source labels per language
TAFSIR_SOURCE_LABELS = {
    "ar": "التفسير الميسر — مجمع الملك فهد لطباعة المصحف الشريف",
    "en": "Ibn Kathir — Tafsir of the Noble Quran",
    "ru": "Тафсир ас-Саади — шейх Абдуррахман ас-Саади",
    "fr": "Ibn Kathir — Tafsir du Noble Coran",
    "de": "Ibn Kathir — Tafsir des edlen Quran",
    "tr": "İbn Kesir — Kur'an-ı Kerim Tefsiri",
    "sv": "Ibn Kathir — Tafsir av den Ädla Koranen",
    "nl": "Ibn Kathir — Tafsir van de Edele Koran",
    "el": "Ιμπν Κατίρ — Τάφσιρ του Ευγενούς Κορανίου",
}

# Language full names for LLM prompt
LANG_NAMES = {
    "fr": "French", "de": "German", "tr": "Turkish",
    "sv": "Swedish", "nl": "Dutch", "el": "Greek",
}


async def _translate_tafsir_llm(english_tafsir: str, target_lang: str, verse_key: str) -> str:
    """Translate English tafsir to target language using LLM. Cache in MongoDB."""
    if not english_tafsir:
        return ""

    # Check MongoDB cache first
    cache_key = f"llm_tafsir_{target_lang}_{verse_key}"
    try:
        cached = await db.llm_tafsir_cache.find_one({"cache_key": cache_key})
        if cached and cached.get("text"):
            return cached["text"]
    except Exception:
        pass

    # Translate using LLM
    api_key = os.environ.get("EMERGENT_LLM_KEY", "")
    if not api_key:
        return ""

    lang_name = LANG_NAMES.get(target_lang, target_lang)
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(
            api_key=api_key,
            session_id=f"tafsir_translate_{cache_key}",
            system_message=f"You are a precise translator of Islamic Quran tafsir (commentary). Translate the following scholarly Quran tafsir text from English to {lang_name}. Maintain the scholarly Islamic tone and terminology. Keep Arabic terms like Allah, Quran, Surah, and proper names in their commonly used form in {lang_name}. Do NOT add any commentary of your own. Output ONLY the translated text, nothing else."
        )
        chat.with_model("gemini", "gemini-2.5-flash")

        # Truncate if too long for translation
        source = english_tafsir[:2000]
        msg = UserMessage(text=f"Translate this Quran tafsir to {lang_name}:\n\n{source}")
        translated = await chat.send_message(msg)

        if translated and len(translated) > 20:
            # Cache in MongoDB
            try:
                await db.llm_tafsir_cache.update_one(
                    {"cache_key": cache_key},
                    {"$set": {
                        "cache_key": cache_key,
                        "text": translated,
                        "source_lang": "en",
                        "target_lang": target_lang,
                        "verse_key": verse_key,
                        "created_at": datetime.utcnow(),
                    }},
                    upsert=True,
                )
            except Exception:
                pass
            return translated
    except Exception as e:
        logger.warning(f"LLM tafsir translation failed for {verse_key} to {target_lang}: {e}")

    return ""

# Max chars for tafsir display
MAX_TAFSIR_CHARS = 1500  # Allow more for real tafsir content

CACHE_TTL_DAYS = 30


def _clean_html(text: str) -> str:
    """Strip HTML tags and entities from API response text."""
    # Remove <h1>, <h2> headers and their content for Ibn Kathir
    text = re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>', '', text, flags=re.DOTALL)
    text = re.sub(r'<sup[^>]*>[\s\S]*?</sup>', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&amp;', '&')
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'")
    # Clean multiple spaces/newlines
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()


async def _fetch_quranenc_greek(surah: int, ayah: int) -> str:
    """Fetch Greek translation from QuranEnc.com (Rowwad)."""
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.get(
                f"{QURANENC_BASE}/translation/aya/greek_rwwad/{surah}/{ayah}"
            )
            if r.status_code == 200:
                data = r.json()
                return data.get("result", {}).get("translation", "")
    except Exception:
        pass
    return ""


async def _fetch_quranenc_footnotes(surah: int, ayah: int, key: str) -> str:
    """Fetch scholarly footnotes from QuranEnc.com (real explanatory notes)."""
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.get(
                f"{QURANENC_BASE}/translation/aya/{key}/{surah}/{ayah}"
            )
            if r.status_code == 200:
                data = r.json()
                footnotes = data.get("result", {}).get("footnotes", "") or ""
                if footnotes:
                    # Clean footnote markers like [123]
                    footnotes = re.sub(r'\[\d+\]\s*', '', footnotes)
                    return footnotes.strip()
    except Exception:
        pass
    return ""


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
    V2026 Global Quran Verse Endpoint — REAL TAFSIR VERSION.
    Returns everything needed to render a single verse:
    - Arabic text, translation, REAL tafsir (not duplicate translation), audio, surah metadata.
    """
    base_lang = language.split("-")[0]
    verse_key = f"{surah_id}:{ayah_id}"

    # ── Check cache ──
    cache_key = f"global_verse_v3_{base_lang}_{verse_key}"
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
                "tafsir": cached.get("tafsir", ""),
                "tafsir_source": cached.get("tafsir_source", ""),
                "tafsir_is_arabic": cached.get("tafsir_is_arabic", False),
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

    # ══════════════════════════════════════════════════════════════
    # FETCH REAL TAFSIR — scholarly explanation, NOT another translation
    # ══════════════════════════════════════════════════════════════
    tafsir_text = ""
    tafsir_source = TAFSIR_SOURCE_LABELS.get(base_lang, "")
    tafsir_is_arabic = False

    # Strategy 1: Real tafsir endpoint (ar, en, ru)
    if base_lang in REAL_TAFSIR_IDS:
        tafsir_id = REAL_TAFSIR_IDS[base_lang]
        tafsir_text = await _fetch_real_tafsir(surah_id, ayah_id, tafsir_id)

    # Strategy 2: LLM translation of English tafsir (fr, de, tr, sv, nl, el)
    elif base_lang in LLM_TAFSIR_LANGS:
        # First fetch the English tafsir (Ibn Kathir)
        en_tafsir = await _fetch_real_tafsir(surah_id, ayah_id, 169)
        if en_tafsir:
            # Translate to target language using LLM
            tafsir_text = await _translate_tafsir_llm(en_tafsir, base_lang, verse_key)
            if tafsir_text:
                tafsir_is_arabic = False
            else:
                # Fallback to Arabic if LLM fails
                tafsir_text = await _fetch_real_tafsir(surah_id, ayah_id, 16)
                tafsir_is_arabic = True
                tafsir_source = "التفسير الميسر"
        else:
            # If English tafsir not available, fallback to Arabic
            tafsir_text = await _fetch_real_tafsir(surah_id, ayah_id, 16)
            tafsir_is_arabic = True
            tafsir_source = "التفسير الميسر"

    # Truncate if too long
    if len(tafsir_text) > MAX_TAFSIR_CHARS:
        tafsir_text = tafsir_text[:MAX_TAFSIR_CHARS].rsplit(' ', 1)[0] + "…"

    # ── Build audio URL (EveryAyah CDN — Alafasy) ──
    audio_url = f"https://everyayah.com/data/Alafasy_128kbps/{str(surah_id).zfill(3)}{str(ayah_id).zfill(3)}.mp3"

    # ── Cache result ──
    result = {
        "arabic_text": arabic_text,
        "translation": translation,
        "tafsir": tafsir_text,
        "tafsir_source": tafsir_source,
        "tafsir_is_arabic": tafsir_is_arabic,
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
