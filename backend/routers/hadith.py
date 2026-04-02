"""
Hadith API Router — V2026 MULTI-LANGUAGE HADITH
================================================
Uses fawazahmed0/hadith-api for pre-translated hadiths.
Supports: Sahih Bukhari & Sahih Muslim in multiple languages.

Language Mapping:
- en: eng-bukhari / eng-muslim
- fr: fra-muslim
- ru: rus-bukhari
- tr: tur-bukhari
- de/nl/sv/el/ar: Fallback to English (eng-bukhari) with label
"""

import httpx
import random
import re
from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from deps import db

router = APIRouter(tags=["hadith"])

HADITH_CDN_BASE = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1"

# Language → collection mappings
HADITH_COLLECTIONS = {
    "en": {"bukhari": "eng-bukhari", "muslim": "eng-muslim"},
    "fr": {"muslim": "fra-muslim"},
    "ru": {"bukhari": "rus-bukhari"},
    "tr": {"bukhari": "tur-bukhari"},
    "ar": {"bukhari": "ara-bukhari", "muslim": "ara-muslim"},
}

# Fallback language for unsupported ones
HADITH_FALLBACK_LANG = "en"

# Languages that use fallback
HADITH_FALLBACK_LANGS = {"de", "nl", "sv", "el"}

HADITH_CACHE_TTL_DAYS = 30


def _clean_hadith_text(text: str) -> str:
    """Clean hadith text of HTML and special chars."""
    text = re.sub(r'<[^>]*>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&quot;', '"')
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return text.strip()


@router.get("/hadith/random")
async def get_random_hadith(
    language: str = Query("en"),
    collection: str = Query("bukhari"),
):
    """Get a random hadith in the specified language."""
    base_lang = language.split("-")[0]
    is_fallback = False
    actual_lang = base_lang

    # Determine collection key
    if base_lang in HADITH_COLLECTIONS:
        lang_colls = HADITH_COLLECTIONS[base_lang]
    elif base_lang in HADITH_FALLBACK_LANGS:
        lang_colls = HADITH_COLLECTIONS[HADITH_FALLBACK_LANG]
        is_fallback = True
        actual_lang = HADITH_FALLBACK_LANG
    else:
        lang_colls = HADITH_COLLECTIONS[HADITH_FALLBACK_LANG]
        is_fallback = True
        actual_lang = HADITH_FALLBACK_LANG

    # Find best collection
    if collection in lang_colls:
        coll_key = lang_colls[collection]
    else:
        # Use first available
        coll_key = list(lang_colls.values())[0]
        collection = list(lang_colls.keys())[0]

    # Check cache for collection
    cache_key = f"hadith_collection_{coll_key}"
    try:
        cached = await db.hadith_cache.find_one({"cache_key": cache_key})
        if cached and cached.get("hadiths"):
            hadiths = cached["hadiths"]
            h = random.choice(hadiths)
            return {
                "success": True,
                "hadith": _clean_hadith_text(h.get("text", "")),
                "hadith_number": h.get("hadithnumber", 0),
                "collection": collection.title(),
                "collection_name": cached.get("collection_name", ""),
                "language": base_lang,
                "is_fallback": is_fallback,
                "fallback_language": actual_lang if is_fallback else None,
                "cached": True,
            }
    except Exception:
        pass

    # Fetch from CDN
    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as c:
            url = f"{HADITH_CDN_BASE}/editions/{coll_key}.min.json"
            r = await c.get(url)
            r.raise_for_status()
            data = r.json()

            hadiths = data.get("hadiths", [])
            metadata = data.get("metadata", {})
            coll_name = metadata.get("name", collection.title())

            if not hadiths:
                raise HTTPException(404, "No hadiths found")

            # Cache the collection (store only first 500 for space)
            try:
                # Store subset for random access
                stored = [{"text": h.get("text", ""), "hadithnumber": h.get("hadithnumber", 0)} for h in hadiths[:1000]]
                await db.hadith_cache.update_one(
                    {"cache_key": cache_key},
                    {"$set": {
                        "cache_key": cache_key,
                        "hadiths": stored,
                        "total": len(hadiths),
                        "collection_name": coll_name,
                        "cached_at": datetime.utcnow(),
                    }},
                    upsert=True,
                )
            except Exception:
                pass

            h = random.choice(hadiths)
            return {
                "success": True,
                "hadith": _clean_hadith_text(h.get("text", "")),
                "hadith_number": h.get("hadithnumber", 0),
                "collection": collection.title(),
                "collection_name": coll_name,
                "language": base_lang,
                "is_fallback": is_fallback,
                "fallback_language": actual_lang if is_fallback else None,
                "cached": False,
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Failed to fetch hadith: {str(e)}")


@router.get("/hadith/by-number")
async def get_hadith_by_number(
    language: str = Query("en"),
    collection: str = Query("bukhari"),
    number: int = Query(1),
):
    """Get a specific hadith by number."""
    base_lang = language.split("-")[0]
    is_fallback = False
    actual_lang = base_lang

    if base_lang in HADITH_COLLECTIONS:
        lang_colls = HADITH_COLLECTIONS[base_lang]
    elif base_lang in HADITH_FALLBACK_LANGS:
        lang_colls = HADITH_COLLECTIONS[HADITH_FALLBACK_LANG]
        is_fallback = True
        actual_lang = HADITH_FALLBACK_LANG
    else:
        lang_colls = HADITH_COLLECTIONS[HADITH_FALLBACK_LANG]
        is_fallback = True
        actual_lang = HADITH_FALLBACK_LANG

    if collection in lang_colls:
        coll_key = lang_colls[collection]
    else:
        coll_key = list(lang_colls.values())[0]
        collection = list(lang_colls.keys())[0]

    # Check cache
    cache_key = f"hadith_collection_{coll_key}"
    try:
        cached = await db.hadith_cache.find_one({"cache_key": cache_key})
        if cached and cached.get("hadiths"):
            for h in cached["hadiths"]:
                if h.get("hadithnumber") == number:
                    return {
                        "success": True,
                        "hadith": _clean_hadith_text(h.get("text", "")),
                        "hadith_number": number,
                        "collection": collection.title(),
                        "collection_name": cached.get("collection_name", ""),
                        "language": base_lang,
                        "is_fallback": is_fallback,
                        "fallback_language": actual_lang if is_fallback else None,
                        "cached": True,
                    }
    except Exception:
        pass

    # Fetch from CDN
    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as c:
            url = f"{HADITH_CDN_BASE}/editions/{coll_key}/{number}.json"
            r = await c.get(url)
            r.raise_for_status()
            data = r.json()

            hadith_data = data.get("hadiths", [{}])
            h = hadith_data[0] if hadith_data else {}

            return {
                "success": True,
                "hadith": _clean_hadith_text(h.get("text", "")),
                "hadith_number": number,
                "collection": collection.title(),
                "language": base_lang,
                "is_fallback": is_fallback,
                "fallback_language": actual_lang if is_fallback else None,
                "cached": False,
            }
    except Exception as e:
        raise HTTPException(500, f"Failed to fetch hadith: {str(e)}")


@router.get("/hadith/collections")
async def get_hadith_collections(language: str = Query("en")):
    """Get available hadith collections for a language."""
    base_lang = language.split("-")[0]
    is_fallback: bool = False
    colls: list = []

    if base_lang in HADITH_COLLECTIONS:
        colls = list(HADITH_COLLECTIONS[base_lang].keys())
    elif base_lang in HADITH_FALLBACK_LANGS:
        colls = list(HADITH_COLLECTIONS[HADITH_FALLBACK_LANG].keys())
        is_fallback = True
    else:
        colls = list(HADITH_COLLECTIONS[HADITH_FALLBACK_LANG].keys())
        is_fallback = True

    return {
        "success": True,
        "language": base_lang,
        "collections": [c.title() for c in colls],
        "is_fallback": is_fallback,
    }
