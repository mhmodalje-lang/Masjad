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
# Official Quran translation IDs per language
QURAN_TRANSLATION_IDS = {
    "en": 131,   # Sahih International
    "de": 27,    # Abu Rida Muhammad ibn Ahmad ibn Rassoul
    "ru": 45,    # Ministry of Awqaf, Egypt
    "fr": 31,    # Muhammad Hamidullah
    "tr": 77,    # Diyanet Isleri
}

QURAN_V4_BASE = "https://api.quran.com/api/v4"

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
