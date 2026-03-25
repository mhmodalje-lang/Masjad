"""
Router: islamic_tools
"""
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from deps import db, get_user, get_admin_user, logger, security, verify_jwt, create_jwt, hash_password, check_password, ADMIN_EMAILS, STRIPE_API_KEY, EMERGENT_LLM_KEY, haversine, query_overpass, clean_time, OVERPASS_ENDPOINTS, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_EMAIL, FIREBASE_PROJECT_ID, RESEND_API_KEY, GEMINI_API_KEY
from starlette.requests import Request
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from data.multilingual_content import STORY_CATEGORIES_TRANSLATED, STORE_LISTING_TRANSLATED, SEO_KEYWORDS_TRANSLATED, UI_STRINGS_ALL, _t
import uuid
import random
import math
import re
import httpx
import os
import json as json_module

router = APIRouter(tags=["Islamic Tools"])

# (ad-config endpoint removed - already defined in admin router)
# (analytics/event endpoint removed - already defined in admin router)
# (admin/analytics/summary endpoint removed - already defined in admin router)

# ==================== AUDIO LOCALIZATION (تعريب الصوتيات) ====================

# (audio/dhikr endpoint removed - already defined in admin router)

@router.get("/localization/supported")
async def get_supported_localizations():
    """Get all supported languages and their features - full 10 languages"""
    from data.multilingual_content import SUPPORTED_LANGUAGES_FULL
    return {
        "ui_languages": SUPPORTED_LANGUAGES_FULL,
        "quran_translations": {
            "ar": {"id": None, "source": "original"},
            "en": {"id": 131, "source": "Saheeh International"},
            "ru": {"id": 45, "source": "Russian Translation"},
            "tr": {"id": 77, "source": "Diyanet İşleri"},
            "de": {"id": 27, "source": "Bubenheim & Elyas"},
            "fr": {"id": 31, "source": "Muhammad Hamidullah"},
            "sv": {"id": 48, "source": "Knut Bernström"},
            "nl": {"id": 144, "source": "Sofian S. Siregar"},
            "el": {"id": 131, "source": "Saheeh International (via English)"},
        },
        "prayer_times_global": True,
        "prayer_times_methods": {
            "default": 2,
            "turkey": 13,
            "russia": 2,
            "germany": 3,
            "france": 12,
            "sweden": 3,
            "netherlands": 3,
            "greece": 2,
        },
        "privacy_policy_languages": ["ar", "en", "ru", "tr", "de", "fr", "sv", "nl", "el"],
        "audio_languages": ["ar", "en"],
        "auto_language_detection": True,
        "store_listing": STORE_LISTING_TRANSLATED,
        "seo_keywords": SEO_KEYWORDS_TRANSLATED,
    }

@router.get("/localization/strings/{lang}")
async def get_ui_strings(lang: str):
    """Get UI translations for a specific language - all 10 languages supported"""
    effective_lang = lang
    if lang == "de-AT":
        effective_lang = "de"
    strings = UI_STRINGS_ALL
    return {"lang": lang, "strings": strings.get(effective_lang, strings["ar"]), "dir": "rtl" if lang == "ar" else "ltr"}

# ==================== STORIES SYSTEM (حكايات) ====================
# Uses the existing posts/comments/likes collections but with story-specific endpoints

STORY_CATEGORIES = STORY_CATEGORIES_TRANSLATED

