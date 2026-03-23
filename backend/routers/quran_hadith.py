"""
Router: quran_hadith
"""
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from deps import db, get_user, logger, security, verify_jwt, create_jwt, hash_password, check_password, ADMIN_EMAILS, STRIPE_API_KEY, EMERGENT_LLM_KEY, haversine, query_overpass, clean_time, OVERPASS_ENDPOINTS, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_EMAIL, FIREBASE_PROJECT_ID, RESEND_API_KEY, GEMINI_API_KEY
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import uuid
import random
import math
import re
import httpx
import os
import json as json_module

from routers.prayer import STATIC_HADITHS, HADITH_TRANSLATIONS

router = APIRouter(tags=["Quran & Hadith"])

@router.get("/daily-hadith")
async def daily_hadith(language: str = Query("ar")):
    """Get today's hadith - rotates daily from collection. Supports all languages."""
    today = date.today()
    day_of_year = today.timetuple().tm_yday
    idx = day_of_year % len(STATIC_HADITHS)
    hadith = STATIC_HADITHS[idx]
    
    # For non-Arabic languages, return localized translation
    if language != "ar" and hadith["number"] in HADITH_TRANSLATIONS:
        trans_data = HADITH_TRANSLATIONS[hadith["number"]]
        # Try exact language, fallback to English
        lang_key = language if language in trans_data else "en"
        if lang_key in trans_data:
            trans = trans_data[lang_key]
            return {
                "success": True,
                "hadith": {
                    "text": trans["text"],
                    "narrator": trans["narrator"],
                    "source": trans["source"],
                    "number": hadith["number"],
                    "arabic_text": hadith["text"],
                    "arabic_narrator": hadith["narrator"],
                    "arabic_source": hadith["source"],
                    "translation_language": lang_key,
                },
                "date": today.isoformat(),
            }
    
    return {
        "success": True,
        "hadith": {
            "text": hadith["text"],
            "narrator": hadith["narrator"],
            "source": hadith["source"],
            "number": hadith["number"],
        },
        "date": today.isoformat(),
    }

# ==================== QURAN (Quran.com API v4) ====================
# Official Quran translation IDs per language (KFGQPC / Noble Quran verified)
QURAN_TRANSLATION_IDS = {
    "en": 20,    # Saheeh International (KFGQPC)
    "de": 27,    # Frank Bubenheim & Nadeem (Widely recognized German)
    "ru": 45,    # Elmir Kuliev (Standard Russian)
    "fr": 136,   # Montada Islamic Foundation (Modern French)
    "tr": 77,    # Diyanet Isleri (Turkey's official authority)
    "sv": 48,    # Knut Bernström (Official Swedish)
    "nl": 235,   # Malak Faris Abdalsalaam (Modern Dutch)
    "el": 20,    # Fallback to English Saheeh International
}

QURAN_V4_BASE = "https://api.quran.com/api/v4"

# ==================== TAFSIR RESOURCE IDS ====================
# Arabic: Tafsir Al-Muyassar (التفسير الميسر) - King Fahd Complex
# English: Ibn Kathir Abridged - Best available scholarly English tafsir
# Russian: Al-Sa'di - Best available Russian tafsir
# Others: Fallback to English Ibn Kathir (Abridged)
TAFSIR_RESOURCE_IDS = {
    "ar": 16,    # Tafsir Al-Muyassar (التفسير الميسر)
    "en": 169,   # Ibn Kathir (Abridged)
    "ru": 170,   # Al-Sa'di (Russian)
    "de": 169,   # Fallback → English Ibn Kathir
    "fr": 169,   # Fallback → English Ibn Kathir
    "tr": 169,   # Fallback → English Ibn Kathir
    "sv": 169,   # Fallback → English Ibn Kathir
    "nl": 169,   # Fallback → English Ibn Kathir
    "el": 169,   # Fallback → English Ibn Kathir
}

TAFSIR_CACHE_TTL_DAYS = 30

@router.get("/quran/v4/chapters")
async def get_chapters_v4(language: str = Query("ar")):
    """Fetch all Surahs from Quran.com API v4"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/chapters", params={"language": language})
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran API error: {str(e)}")

@router.get("/quran/v4/chapters/{chapter_number}")
async def get_chapter_v4(chapter_number: int, language: str = Query("ar")):
    """Fetch specific Surah info from Quran.com API v4"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/chapters/{chapter_number}", params={"language": language})
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran API error: {str(e)}")

@router.get("/quran/v4/verses/by_chapter/{chapter_number}")
async def get_verses_v4(
    chapter_number: int,
    language: str = Query("ar"),
    page: int = Query(1),
    per_page: int = Query(50),
    translations: Optional[str] = Query(None),
):
    """Fetch verses of a Surah with translations from Quran.com API v4"""
    try:
        params = {
            "language": language,
            "page": page,
            "per_page": per_page,
            "words": "false",
            "fields": "text_uthmani",
        }
        # Auto-select translation if not specified
        if translations:
            params["translations"] = translations
        elif language != "ar" and language in QURAN_TRANSLATION_IDS:
            params["translations"] = str(QURAN_TRANSLATION_IDS[language])

        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/verses/by_chapter/{chapter_number}", params=params)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran API error: {str(e)}")

@router.get("/quran/v4/verses/by_juz/{juz_number}")
async def get_juz_verses_v4(
    juz_number: int,
    language: str = Query("ar"),
    page: int = Query(1),
    per_page: int = Query(50),
    translations: Optional[str] = Query(None),
):
    """Fetch verses by Juz number from Quran.com API v4"""
    try:
        params = {
            "language": language,
            "page": page,
            "per_page": per_page,
            "words": "false",
            "fields": "text_uthmani",
        }
        if translations:
            params["translations"] = translations
        elif language != "ar" and language in QURAN_TRANSLATION_IDS:
            params["translations"] = str(QURAN_TRANSLATION_IDS[language])

        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/verses/by_juz/{juz_number}", params=params)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran API error: {str(e)}")

@router.get("/quran/v4/search")
async def search_quran_v4(
    q: str = Query(...),
    language: str = Query("ar"),
    page: int = Query(1),
    size: int = Query(20),
):
    """Search the Quran via Quran.com API v4 with fallback to legacy API"""
    try:
        params = {
            "q": q,
            "language": language,
            "page": page,
            "size": size,
        }
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/search", params=params)
            if r.status_code == 200:
                data = r.json()
                return data
            # Fallback to legacy alquran.cloud API if v4 search fails
            r2 = await c.get(f"https://api.alquran.cloud/v1/search/{q}/all/ar")
            if r2.status_code == 200:
                return r2.json()
            return {"search": {"results": [], "total_results": 0}}
    except Exception as e:
        # Final fallback - return empty results
        return {"search": {"results": [], "total_results": 0}, "error": str(e)}

@router.get("/quran/v4/juzs")
async def get_juzs_v4():
    """Fetch all Juz info from Quran.com API v4"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/juzs")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran API error: {str(e)}")

@router.get("/quran/v4/recitations/{recitation_id}/by_ayah/{verse_key}")
async def get_verse_audio_v4(recitation_id: int, verse_key: str):
    """Fetch verse audio recitation from Quran.com API v4"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/recitations/{recitation_id}/by_ayah/{verse_key}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran audio error: {str(e)}")

@router.get("/quran/v4/resources/translations")
async def get_available_translations_v4(language: str = Query("en")):
    """Fetch available Quran translations from Quran.com API v4"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/resources/translations", params={"language": language})
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran API error: {str(e)}")

# ==================== TAFSIR (Exegesis) API ====================

@router.get("/quran/v4/tafsir/{verse_key}")
async def get_tafsir_for_verse(
    verse_key: str,
    language: str = Query("ar"),
):
    """
    Fetch Tafsir (Exegesis) for a specific verse.
    - Arabic: Tafsir Al-Muyassar (التفسير الميسر) from King Fahd Complex
    - English: Ibn Kathir (Abridged)
    - Russian: Al-Sa'di
    - Others: Falls back to English Ibn Kathir (Abridged)
    
    Implements MongoDB caching for 30 days for instant loading.
    """
    # Validate verse_key format (e.g., "1:1", "2:255")
    if not re.match(r'^\d+:\d+$', verse_key):
        raise HTTPException(400, "Invalid verse key format. Use chapter:verse (e.g., 1:1)")
    
    base_lang = language.split('-')[0]  # Handle de-AT -> de
    tafsir_id = TAFSIR_RESOURCE_IDS.get(base_lang, TAFSIR_RESOURCE_IDS["en"])
    # Languages with native tafsir: ar (16), en (169), ru (170)
    # All others fallback to English Ibn Kathir (169)
    is_fallback = base_lang not in ["ar", "en", "ru"]
    
    # Check MongoDB cache first
    cache_key = f"tafsir_{tafsir_id}_{verse_key}"
    try:
        cached = await db.tafsir_cache.find_one({
            "cache_key": cache_key,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        if cached:
            return {
                "success": True,
                "verse_key": verse_key,
                "language": base_lang,
                "tafsir_id": tafsir_id,
                "tafsir_name": cached.get("tafsir_name", ""),
                "text": cached.get("text", ""),
                "is_fallback_language": cached.get("is_fallback", False),
                "cached": True,
            }
    except Exception:
        pass  # Cache miss, fetch from API
    
    # Fetch from Quran.com API v4
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/tafsirs/{tafsir_id}/by_ayah/{verse_key}")
            r.raise_for_status()
            data = r.json()
            
            tafsir_data = data.get("tafsir", {})
            raw_text = tafsir_data.get("text", "")
            # Clean HTML tags from tafsir text
            clean_text = re.sub(r'<[^>]*>', '', raw_text).replace('&nbsp;', ' ').strip()
            tafsir_name = tafsir_data.get("resource_name", "")
            
            # Cache in MongoDB
            try:
                await db.tafsir_cache.update_one(
                    {"cache_key": cache_key},
                    {"$set": {
                        "cache_key": cache_key,
                        "verse_key": verse_key,
                        "tafsir_id": tafsir_id,
                        "tafsir_name": tafsir_name,
                        "text": clean_text,
                        "is_fallback": is_fallback,
                        "cached_at": datetime.utcnow(),
                        "expires_at": datetime.utcnow() + timedelta(days=TAFSIR_CACHE_TTL_DAYS),
                    }},
                    upsert=True,
                )
            except Exception:
                pass  # Non-critical: caching failure
            
            return {
                "success": True,
                "verse_key": verse_key,
                "language": base_lang,
                "tafsir_id": tafsir_id,
                "tafsir_name": tafsir_name,
                "text": clean_text,
                "is_fallback_language": is_fallback,
                "cached": False,
            }
    except httpx.HTTPStatusError as e:
        raise HTTPException(e.response.status_code, f"Tafsir API error: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Tafsir fetch error: {str(e)}")


@router.get("/quran/v4/tafsir/bulk/{chapter_number}")
async def get_bulk_tafsir_for_chapter(
    chapter_number: int,
    language: str = Query("ar"),
    page: int = Query(1),
    per_page: int = Query(50),
):
    """
    Fetch Tafsir for all verses of a chapter (bulk). 
    More efficient than per-verse fetching.
    Cached in MongoDB for 30 days.
    """
    if chapter_number < 1 or chapter_number > 114:
        raise HTTPException(400, "Invalid chapter number (1-114)")
    
    base_lang = language.split('-')[0]
    tafsir_id = TAFSIR_RESOURCE_IDS.get(base_lang, TAFSIR_RESOURCE_IDS["en"])
    # Languages with native tafsir: ar (16), en (169), ru (170)
    # All others fallback to English Ibn Kathir (169)
    is_fallback = base_lang not in ["ar", "en", "ru"]
    
    # Check bulk cache
    bulk_cache_key = f"tafsir_bulk_{tafsir_id}_{chapter_number}_p{page}"
    try:
        cached = await db.tafsir_cache.find_one({
            "cache_key": bulk_cache_key,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        if cached:
            return {
                "success": True,
                "chapter": chapter_number,
                "language": base_lang,
                "tafsir_id": tafsir_id,
                "tafsirs": cached.get("tafsirs", []),
                "is_fallback_language": cached.get("is_fallback", False),
                "cached": True,
            }
    except Exception:
        pass
    
    # Fetch from API - use the chapter tafsir endpoint 
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            # Quran.com v4 doesn't have a direct bulk tafsir endpoint per chapter
            # We fetch verses first to know the count, then fetch tafsir per verse
            verses_r = await c.get(f"{QURAN_V4_BASE}/verses/by_chapter/{chapter_number}", params={
                "page": page, "per_page": per_page, "fields": "verse_key"
            })
            verses_r.raise_for_status()
            verses_data = verses_r.json()
            verse_keys = [v["verse_key"] for v in verses_data.get("verses", [])]
            
            tafsirs_list = []
            for vk in verse_keys:
                try:
                    tr = await c.get(f"{QURAN_V4_BASE}/tafsirs/{tafsir_id}/by_ayah/{vk}")
                    if tr.status_code == 200:
                        td = tr.json().get("tafsir", {})
                        raw = td.get("text", "")
                        clean = re.sub(r'<[^>]*>', '', raw).replace('&nbsp;', ' ').strip()
                        tafsirs_list.append({
                            "verse_key": vk,
                            "text": clean,
                            "tafsir_name": td.get("resource_name", ""),
                        })
                except Exception:
                    tafsirs_list.append({"verse_key": vk, "text": "", "tafsir_name": ""})
            
            # Cache bulk result
            try:
                await db.tafsir_cache.update_one(
                    {"cache_key": bulk_cache_key},
                    {"$set": {
                        "cache_key": bulk_cache_key,
                        "chapter": chapter_number,
                        "tafsir_id": tafsir_id,
                        "tafsirs": tafsirs_list,
                        "is_fallback": is_fallback,
                        "cached_at": datetime.utcnow(),
                        "expires_at": datetime.utcnow() + timedelta(days=TAFSIR_CACHE_TTL_DAYS),
                    }},
                    upsert=True,
                )
            except Exception:
                pass
            
            return {
                "success": True,
                "chapter": chapter_number,
                "language": base_lang,
                "tafsir_id": tafsir_id,
                "tafsirs": tafsirs_list,
                "is_fallback_language": is_fallback,
                "cached": False,
            }
    except Exception as e:
        raise HTTPException(500, f"Bulk tafsir fetch error: {str(e)}")


# ==================== HADITH (Sunnah.com API) ====================
SUNNAH_API_BASE = "https://api.sunnah.com/v1"

@router.get("/hadith/collections")
async def get_hadith_collections():
    """Fetch available Hadith collections from Sunnah.com API"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{SUNNAH_API_BASE}/collections", headers={"X-API-Key": "SqD712P3E82xnwOAEOkGd5JZH8s9wRR24TqNFzjk"})
            r.raise_for_status()
            return r.json()
    except Exception:
        # Fallback to static collections list
        return {
            "data": [
                {"name": "bukhari", "hasBooks": True, "hasChapters": True, "collection": [{"lang": "ar", "title": "صحيح البخاري"}, {"lang": "en", "title": "Sahih al-Bukhari"}]},
                {"name": "muslim", "hasBooks": True, "hasChapters": True, "collection": [{"lang": "ar", "title": "صحيح مسلم"}, {"lang": "en", "title": "Sahih Muslim"}]},
                {"name": "tirmidhi", "hasBooks": True, "hasChapters": True, "collection": [{"lang": "ar", "title": "سنن الترمذي"}, {"lang": "en", "title": "Jami` at-Tirmidhi"}]},
                {"name": "abudawud", "hasBooks": True, "hasChapters": True, "collection": [{"lang": "ar", "title": "سنن أبي داود"}, {"lang": "en", "title": "Sunan Abi Dawud"}]},
                {"name": "nasai", "hasBooks": True, "hasChapters": True, "collection": [{"lang": "ar", "title": "سنن النسائي"}, {"lang": "en", "title": "Sunan an-Nasa'i"}]},
                {"name": "ibnmajah", "hasBooks": True, "hasChapters": True, "collection": [{"lang": "ar", "title": "سنن ابن ماجه"}, {"lang": "en", "title": "Sunan Ibn Majah"}]},
            ]
        }

@router.get("/hadith/{collection}/books")
async def get_hadith_books(collection: str):
    """Fetch books within a Hadith collection"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{SUNNAH_API_BASE}/collections/{collection}/books", headers={"X-API-Key": "SqD712P3E82xnwOAEOkGd5JZH8s9wRR24TqNFzjk"})
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Hadith API error: {str(e)}")

@router.get("/hadith/{collection}/books/{book_number}/hadiths")
async def get_hadiths_by_book(collection: str, book_number: int, page: int = Query(1), limit: int = Query(20)):
    """Fetch Hadiths from a specific book in a collection"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(
                f"{SUNNAH_API_BASE}/collections/{collection}/books/{book_number}/hadiths",
                params={"page": page, "limit": limit},
                headers={"X-API-Key": "SqD712P3E82xnwOAEOkGd5JZH8s9wRR24TqNFzjk"}
            )
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Hadith API error: {str(e)}")

@router.get("/hadith/{collection}/{hadith_number}")
async def get_specific_hadith(collection: str, hadith_number: str):
    """Fetch a specific Hadith by number"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(
                f"{SUNNAH_API_BASE}/collections/{collection}/hadiths/{hadith_number}",
                headers={"X-API-Key": "SqD712P3E82xnwOAEOkGd5JZH8s9wRR24TqNFzjk"}
            )
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Hadith API error: {str(e)}")

# Keep legacy endpoints for backward compatibility
@router.get("/quran/surah/{number}")
async def get_surah(number: int, reciter: str = Query("ar.alafasy")):
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"https://api.alquran.cloud/v1/surah/{number}/{reciter}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/quran/search")
async def search_quran(q: str = Query(...)):
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"https://api.alquran.cloud/v1/search/{q}/all/ar")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, str(e))

# ==================== USER DATA SYNC ====================
@router.post("/user/sync")
async def sync_user_data(data: dict, user: dict = Depends(get_user)):
    """Sync user data to cloud"""
    if not user:
        raise HTTPException(401, "مطلوب تسجيل الدخول")
    
    sync_doc = {
        "user_id": user["id"],
        "updated_at": datetime.utcnow().isoformat(),
        **{k: data[k] for k in data if k not in ("user_id", "_id")}
    }
    await db.user_data.update_one({"user_id": user["id"]}, {"$set": sync_doc}, upsert=True)
    return {"success": True}

@router.get("/user/sync")
async def get_user_data(user: dict = Depends(get_user)):
    """Get synced user data"""
    if not user:
        raise HTTPException(401, "مطلوب تسجيل الدخول")
    doc = await db.user_data.find_one({"user_id": user["id"]}, {"_id": 0})
    return doc or {}

# ==================== ADMIN ====================
