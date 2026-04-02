"""
Quran API Service - Fetches official translations from api.alquran.cloud
Uses KFGQPC (King Fahd Complex) & Noble Quran verified translations.
Central Source: King Fahd Complex (KFGQPC) / The Noble Quran (Quran.com API v4)
Caches results in MongoDB for performance.
"""
import httpx
import asyncio
import os
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient

# ═══════════════════════════════════════════════════════════════
# OFFICIAL TRANSLATION EDITIONS - Globally Recognized Sources
# ═══════════════════════════════════════════════════════════════
QURAN_EDITIONS = {
    "ar": "quran-uthmani",          # Original Uthmani text (King Fahd Complex)
    "en": "en.sahih",               # Saheeh International (KFGQPC)
    "de": "de.bubenheim",           # Frank Bubenheim & Nadeem
    "fr": "fr.hamidullah",          # Muhammad Hamidullah (classic French)
    "tr": "tr.diyanet",             # Diyanet İşleri (Turkey's official authority)
    "ru": "ru.abuadel",             # Abu Adel (verified Russian)
    "sv": "sv.bernstrom",           # Knut Bernström (official Swedish)
    "nl": "nl.siregar",             # Sofian S. Siregar (verified Dutch)
    "el": "el.rwwad",               # QuranEnc Rowwad (Greek)
}

# Tafsir (interpretation) editions where available
TAFSIR_EDITIONS = {
    "ar": "ar.muyassar",            # King Fahad Complex - Tafsir Muyassar
    "en": "en.sahih",               # Sahih International (includes brief tafsir notes)
}

# Surahs used in Kids Zone (Juz Amma - short surahs)
KIDS_SURAH_NUMBERS = [1, 99, 101, 102, 103, 105, 106, 107, 109, 112, 113, 114, 108, 110, 111]

API_BASE = "https://api.alquran.cloud/v1"
CACHE_TTL_DAYS = 30  # Cache for 30 days

# MongoDB connection
_db: object | None = None

def get_db() -> object:
    global _db
    if _db is None:
        mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
        client = AsyncIOMotorClient(mongo_url)
        _db = client.sohba_app
    return _db


async def fetch_surah_translation(surah_number: int, edition: str) -> dict | None:
    """Fetch a single surah translation from alquran.cloud API."""
    url = f"{API_BASE}/surah/{surah_number}/{edition}"
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    return data["data"]
    except Exception as e:
        print(f"[QuranAPI] Error fetching surah {surah_number}/{edition}: {e}")
    return None


async def get_cached_surah(surah_number: int, lang: str) -> dict | None:
    """Get cached surah translation from MongoDB."""
    db = get_db()
    cache = await db.quran_cache.find_one({
        "surah_number": surah_number,
        "lang": lang,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    return cache


async def cache_surah(surah_number: int, lang: str, data: dict):
    """Cache surah translation in MongoDB."""
    db = get_db()
    await db.quran_cache.update_one(
        {"surah_number": surah_number, "lang": lang},
        {"$set": {
            "surah_number": surah_number,
            "lang": lang,
            "data": data,
            "cached_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=CACHE_TTL_DAYS)
        }},
        upsert=True
    )


async def get_surah_with_translation(surah_number: int, lang: str) -> dict | None:
    """Get surah with official translation - from cache or API."""
    # Normalize language
    if lang not in QURAN_EDITIONS:
        lang = "en"
    
    # Check cache first
    cached = await get_cached_surah(surah_number, lang)
    if cached:
        return cached["data"]
    
    # Fetch from API
    edition = QURAN_EDITIONS[lang]
    surah_data = await fetch_surah_translation(surah_number, edition)
    
    if surah_data:
        # Format the data
        formatted = {
            "number": surah_data["number"],
            "name": surah_data["name"],
            "englishName": surah_data["englishName"],
            "englishNameTranslation": surah_data["englishNameTranslation"],
            "numberOfAyahs": surah_data["numberOfAyahs"],
            "revelationType": surah_data.get("revelationType", ""),
            "ayahs": [
                {
                    "number": a["numberInSurah"],
                    "text": a["text"],
                    "juz": a.get("juz", 0),
                    "page": a.get("page", 0),
                }
                for a in surah_data.get("ayahs", [])
            ],
            "edition": {
                "identifier": surah_data.get("edition", {}).get("identifier", edition),
                "language": surah_data.get("edition", {}).get("language", lang),
                "name": surah_data.get("edition", {}).get("name", ""),
                "englishName": surah_data.get("edition", {}).get("englishName", ""),
            }
        }
        
        # Cache it
        await cache_surah(surah_number, lang, formatted)
        return formatted
    
    return None


async def get_surah_arabic_and_translation(surah_number: int, lang: str) -> dict | None:
    """Get surah with both Arabic text and translation side by side."""
    # Always get Arabic text
    arabic_data = await get_surah_with_translation(surah_number, "ar")
    
    if lang == "ar":
        return arabic_data
    
    # Get translation
    trans_data = await get_surah_with_translation(surah_number, lang)
    
    if arabic_data and trans_data:
        # Merge Arabic + Translation
        merged_ayahs = []
        for i, ar_ayah in enumerate(arabic_data.get("ayahs", [])):
            tr_ayah = trans_data["ayahs"][i] if i < len(trans_data["ayahs"]) else {}
            merged_ayahs.append({
                "number": ar_ayah["number"],
                "arabic": ar_ayah["text"],
                "translation": tr_ayah.get("text", ""),
            })
        
        return {
            "number": arabic_data["number"],
            "name_ar": arabic_data["name"],
            "name_en": arabic_data.get("englishName", ""),
            "total_ayahs": arabic_data["numberOfAyahs"],
            "ayahs": merged_ayahs,
            "translation_source": trans_data.get("edition", {}).get("englishName", ""),
            "translation_edition": trans_data.get("edition", {}).get("identifier", ""),
        }
    elif arabic_data:
        # Return Arabic only if translation fails
        return {
            "number": arabic_data["number"],
            "name_ar": arabic_data["name"],
            "name_en": arabic_data.get("englishName", ""),
            "total_ayahs": arabic_data["numberOfAyahs"],
            "ayahs": [
                {"number": a["number"], "arabic": a["text"], "translation": ""}
                for a in arabic_data.get("ayahs", [])
            ],
            "translation_source": "",
            "translation_edition": "",
        }
    
    return None


async def get_kids_surahs_all(lang: str) -> list:
    """Get all kids surahs with official translations for a given language."""
    results = []
    
    for surah_num in KIDS_SURAH_NUMBERS:
        surah = await get_surah_arabic_and_translation(surah_num, lang)
        if surah:
            # Map surah number to simple ID
            surah_id_map = {
                1: "fatiha", 99: "zilzal", 101: "qariah", 102: "takathur",
                103: "asr", 105: "fil", 106: "quraysh", 107: "maun",
                108: "kawthar", 109: "kafiroon", 110: "nasr", 111: "masad",
                112: "ikhlas", 113: "falaq", 114: "nas"
            }
            surah["id"] = surah_id_map.get(surah_num, f"s{surah_num}")
            results.append(surah)
    
    return results


async def prefetch_kids_surahs():
    """Pre-fetch and cache all kids surahs for all languages. Call on startup."""
    print("[QuranAPI] Pre-fetching kids surahs for all languages...")
    for lang in QURAN_EDITIONS:
        for surah_num in KIDS_SURAH_NUMBERS:
            cached = await get_cached_surah(surah_num, lang)
            if not cached:
                await get_surah_with_translation(surah_num, lang)
                await asyncio.sleep(0.2)  # Rate limit: 5 req/sec
    print("[QuranAPI] Pre-fetch complete.")
