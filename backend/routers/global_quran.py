"""
Global Quran Verse API — V2026 TAFSIR REBUILD
==============================================
SINGLE unified endpoint. ALL 114 surahs, ALL 9 languages.

TAFSIR SOURCES (Islamic scholarly sources per language):
- ar: التفسير الميسر (Al-Muyassar) — مجمع الملك فهد (ID 16, tafsir endpoint)
- ru: Тафсир ас-Саади (As-Sa'di) — (ID 170, tafsir endpoint)
- en: Abdel Haleem (ID 85) — Oxford Islamic scholar
- de: Abu Reda (ID 208) — Islamic scholar
- fr: Montada Islamic Foundation (ID 136) — مؤسسة المنتدى الإسلامي
- tr: Elmalılı Hamdi Yazır (ID 52) — Ottoman Islamic scholar / tafsir
- nl: Abdalsalaam (ID 235) — Islamic scholar
- sv: Knut Bernström (ID 48) — Swedish Islamic scholar
- el: Rowwad Translation Center (QuranEnc) — مركز رواد الترجمة

All truncated to match Arabic Al-Muyassar length (~700 chars max).
"""

import re
import httpx
from fastapi import APIRouter, Query
from datetime import datetime, timedelta

from deps import db

router = APIRouter(tags=["global-quran"])

QURAN_V4_BASE = "https://api.quran.com/api/v4"

# ═══════════════════════════════════════════════════════════════
# BLOCKED IDS — NEVER USE
# ═══════════════════════════════════════════════════════════════
BLOCKED_IDS = {169}  # Ibn Kathir (too long)

# ═══════════════════════════════════════════════════════════════
# MAIN TRANSLATION IDs — for verse display
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
# TAFSIR SOURCES — Real Islamic scholarly tafsir per language
# ar/ru: Use Quran.com TAFSIR endpoint (real tafsir texts)
# Other languages: Use Islamic scholarly translations (translation endpoint)
# All truncated to ~700 chars to match Arabic التفسير الميسر length
# ═══════════════════════════════════════════════════════════════

# Languages with REAL tafsir on Quran.com (use /tafsirs/ endpoint)
TAFSIR_IDS = {
    "ar": 16,    # التفسير الميسر — مجمع الملك فهد
    "ru": 170,   # Тафсир ас-Саади
}

# Languages using Islamic scholarly translations as tafsir (use /translations/ endpoint)
TAFSIR_TRANSLATION_IDS = {
    "en": 85,    # Abdel Haleem — Oxford Islamic Studies
    "de": 208,   # Abu Reda Muhammad ibn Ahmad — Islamic scholar
    "fr": 136,   # Montada Islamic Foundation — مؤسسة المنتدى الإسلامي
    "tr": 52,    # Elmalılı Hamdi Yazır — Ottoman Islamic tafsir scholar
    "nl": 235,   # Abdalsalaam — Islamic scholar
    "sv": 48,    # Knut Bernström — Swedish Islamic scholar
    "el": 0,     # Rowwad (QuranEnc)
}

# Islamic source labels per language
TAFSIR_SOURCE_LABELS = {
    "ar": "التفسير الميسر — مجمع الملك فهد لطباعة المصحف الشريف",
    "en": "Abdel Haleem — Oxford Islamic Studies",
    "ru": "Тафсир ас-Саади — шейх Абдуррахман ас-Саади",
    "de": "Abu Reda Muhammad ibn Ahmad — Islamischer Gelehrter",
    "fr": "Fondation Islamique Montada — مؤسسة المنتدى الإسلامي",
    "tr": "Elmalılı Hamdi Yazır — Osmanlı İslam Müfessiri",
    "nl": "Malak Faris Abdalsalaam — Islamitische Geleerde",
    "sv": "Knut Bernström — Islamisk Forskare",
    "el": "Κέντρο Μετάφρασης Ρουάντ — مركز رواد الترجمة",
}

# Match Arabic التفسير الميسر max length (~688 chars for آية الكرسي)
MAX_TAFSIR_CHARS = 700

CACHE_TTL_DAYS = 30


def _clean_html(text: str) -> str:
    """Strip HTML tags and entities from API response text."""
    text = re.sub(r'<sup[^>]*>[\s\S]*?</sup>', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&amp;', '&')
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'")
    return text.strip()


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
                "tafsir": cached.get("tafsir", ""),
                "tafsir_source": cached.get("tafsir_source", ""),
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

    # ── Fetch Islamic Tafsir (scholarly source per language) ──
    tafsir_text = ""
    tafsir_source = TAFSIR_SOURCE_LABELS.get(base_lang, "")

    # Strategy 1: Real tafsir endpoint (ar, ru)
    if base_lang in TAFSIR_IDS:
        tafsir_id = TAFSIR_IDS[base_lang]
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.get(f"{QURAN_V4_BASE}/tafsirs/{tafsir_id}/by_ayah/{verse_key}")
                r.raise_for_status()
                data = r.json()
                raw = data.get("tafsir", {}).get("text", "")
                tafsir_text = _clean_html(raw)
        except Exception:
            pass

    # Strategy 2: Islamic scholarly translation as tafsir (all other languages)
    else:
        tafsir_tr_id = TAFSIR_TRANSLATION_IDS.get(base_lang, 0)
        if tafsir_tr_id in BLOCKED_IDS:
            tafsir_tr_id = 0
        if tafsir_tr_id > 0:
            try:
                async with httpx.AsyncClient(timeout=30) as c:
                    r = await c.get(
                        f"{QURAN_V4_BASE}/verses/by_key/{verse_key}",
                        params={"translations": str(tafsir_tr_id), "fields": "text_uthmani", "words": "false"},
                    )
                    r.raise_for_status()
                    data = r.json()
                    trs = data.get("verse", {}).get("translations", [])
                    if trs:
                        tafsir_text = _clean_html(trs[0].get("text", ""))
            except Exception:
                pass
        elif base_lang == "el":
            # Greek: use same QuranEnc text
            tafsir_text = translation

    # Truncate to match Arabic التفسير الميسر length
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
