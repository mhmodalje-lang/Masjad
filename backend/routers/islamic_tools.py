"""
Router: islamic_tools
"""
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from deps import db, get_user, get_admin_user, logger, security, verify_jwt, create_jwt, hash_password, check_password, ADMIN_EMAILS, STRIPE_API_KEY, EMERGENT_LLM_KEY, haversine, query_overpass, clean_time, OVERPASS_ENDPOINTS, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_EMAIL, FIREBASE_PROJECT_ID, RESEND_API_KEY, GEMINI_API_KEY
from starlette.requests import Request
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

router = APIRouter(tags=["Islamic Tools"])

@router.get("/ad-config")
async def get_ad_config(request: Request):
    """Public endpoint - returns ad configuration for the app with geo-targeting"""
    settings = await db.app_settings.find_one({"key": "global"}, {"_id": 0}) or {}
    
    # Determine user region from Accept-Language header for Tier-based ad targeting
    accept_lang = request.headers.get("accept-language", "ar")
    primary_lang = accept_lang.split(",")[0].split("-")[0].strip().lower() if accept_lang else "ar"
    
    # Tier 1 countries (highest ad revenue): US, UK, CA, AU, DE, FR, NL, NO, SE, DK, CH
    # Tier 2: TR, RU, BR, MX, PL, etc.
    tier1_langs = ["en", "de", "fr", "nl", "no", "sv", "da"]
    tier2_langs = ["tr", "ru", "pt", "pl", "es", "it"]
    
    ad_tier = "tier1" if primary_lang in tier1_langs else ("tier2" if primary_lang in tier2_langs else "tier3")
    
    return {
        "ads_enabled": settings.get("ads_enabled", True),
        "video_ads_muted": settings.get("video_ads_muted", True),
        "gdpr_consent_required": settings.get("gdpr_consent_required", True),
        "ad_banner_enabled": settings.get("ad_banner_enabled", True),
        "ad_interstitial_enabled": settings.get("ad_interstitial_enabled", False),
        "ad_rewarded_enabled": settings.get("ad_rewarded_enabled", True),
        "admob_app_id": settings.get("admob_app_id", ""),
        "adsense_publisher_id": settings.get("adsense_publisher_id", ""),
        "ad_tier": ad_tier,
        "user_language": primary_lang,
    }

# ==================== ANALYTICS TRACKING (التحليلات) ====================

@router.post("/analytics/event")
async def track_analytics_event(data: dict):
    """Track user analytics events"""
    event = {
        "id": str(uuid.uuid4()),
        "event_type": data.get("event_type", "page_view"),
        "page": data.get("page", ""),
        "user_id": data.get("user_id", "anonymous"),
        "session_id": data.get("session_id", ""),
        "metadata": data.get("metadata", {}),
        "user_agent": data.get("user_agent", ""),
        "timestamp": datetime.utcnow().isoformat(),
    }
    await db.analytics_events.insert_one(event)
    return {"success": True}

@router.get("/admin/analytics/summary")
async def admin_analytics_summary(admin=Depends(get_admin_user), days: int = 7):
    """Get analytics summary for admin dashboard"""
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    
    # Total events
    total_events = await db.analytics_events.count_documents({"timestamp": {"$gte": cutoff}})
    
    # Page views by page
    pipeline = [
        {"$match": {"timestamp": {"$gte": cutoff}, "event_type": "page_view"}},
        {"$group": {"_id": "$page", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]
    page_views = await db.analytics_events.aggregate(pipeline).to_list(20)
    
    # Unique users
    unique_users = len(await db.analytics_events.distinct("user_id", {"timestamp": {"$gte": cutoff}}))
    
    # Daily counts
    daily_pipeline = [
        {"$match": {"timestamp": {"$gte": cutoff}}},
        {"$group": {
            "_id": {"$substr": ["$timestamp", 0, 10]},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    daily_counts = await db.analytics_events.aggregate(daily_pipeline).to_list(30)
    
    return {
        "total_events": total_events,
        "unique_users": unique_users,
        "top_pages": [{"page": p["_id"], "views": p["count"]} for p in page_views],
        "daily_counts": [{"date": d["_id"], "count": d["count"]} for d in daily_counts],
        "period_days": days,
    }

# ==================== AUDIO LOCALIZATION (تعريب الصوتيات) ====================


@router.get("/audio/dhikr")
async def get_dhikr_audio(lang: str = "ar"):
    """Get dhikr audio URLs based on language - for localized audio playback"""
    # Audio mapping by language - these can be updated via admin
    audio_config = await db.app_settings.find_one({"key": "audio_localization"}, {"_id": 0})
    
    if not audio_config:
        # Default audio configuration
        audio_config = {
            "languages": {
                "ar": {"label": "العربية", "available": True},
                "en": {"label": "English", "available": True},
                "ru": {"label": "Русский", "available": False},
                "tr": {"label": "Türkçe", "available": False},
                "de": {"label": "Deutsch", "available": False},
                "fr": {"label": "Français", "available": False},
            },
            "dhikr_list": [
                {"key": "subhanallah", "ar": "سبحان الله", "en": "Glory be to Allah"},
                {"key": "alhamdulillah", "ar": "الحمد لله", "en": "Praise be to Allah"},
                {"key": "allahuakbar", "ar": "الله أكبر", "en": "Allah is the Greatest"},
                {"key": "istighfar", "ar": "أستغفر الله", "en": "I seek forgiveness from Allah"},
                {"key": "hawqala", "ar": "لا حول ولا قوة إلا بالله", "en": "There is no power except with Allah"},
            ]
        }
    
    return {
        "language": lang,
        "languages_available": audio_config.get("languages", {}),
        "dhikr_list": audio_config.get("dhikr_list", []),
    }

@router.get("/localization/supported")
async def get_supported_localizations():
    """Get all supported languages and their features"""
    return {
        "ui_languages": [
            {"code": "ar", "label": "العربية", "flag": "🇸🇦", "dir": "rtl", "complete": True},
            {"code": "en", "label": "English", "flag": "🇬🇧", "dir": "ltr", "complete": True},
            {"code": "ru", "label": "Русский", "flag": "🇷🇺", "dir": "ltr", "complete": True},
            {"code": "tr", "label": "Türkçe", "flag": "🇹🇷", "dir": "ltr", "complete": True},
            {"code": "de", "label": "Deutsch", "flag": "🇩🇪", "dir": "ltr", "complete": True},
            {"code": "fr", "label": "Français", "flag": "🇫🇷", "dir": "ltr", "complete": True},
        ],
        "quran_translations": {
            "ar": {"id": None, "source": "original"},
            "en": {"id": 131, "source": "Saheeh International"},
            "ru": {"id": 45, "source": "Russian Translation"},
            "tr": {"id": 77, "source": "Diyanet İşleri"},
            "de": {"id": 27, "source": "Bubenheim & Elyas"},
            "fr": {"id": 31, "source": "Muhammad Hamidullah"},
        },
        "prayer_times_global": True,
        "prayer_times_methods": {
            "default": 2,
            "turkey": 13,
            "russia": 2,
            "germany": 3,
            "france": 12,
        },
        "privacy_policy_languages": ["ar", "en", "ru", "tr", "de", "fr"],
        "audio_languages": ["ar", "en"],
        "auto_language_detection": True,
        "store_listing": {
            "ar": {"title": "أذان وحكاية - مواقيت الصلاة والقرآن", "short": "مواقيت الصلاة، القرآن، الأذكار"},
            "en": {"title": "Azan & Hikaya - Prayer Times & Quran", "short": "Prayer Times, Quran, Azkar"},
            "ru": {"title": "Азан и Хикая - Время молитв и Коран", "short": "Время молитв, Коран, Азкар"},
            "tr": {"title": "Ezan ve Hikaye - Namaz Vakitleri ve Kur'an", "short": "Namaz Vakitleri, Kur'an, Zikirler"},
            "de": {"title": "Azan & Hikaya - Gebetszeiten & Koran", "short": "Gebetszeiten, Koran, Dhikr"},
            "fr": {"title": "Azan & Hikaya - Heures de prière & Coran", "short": "Heures de prière, Coran, Dhikr"},
        },
        "seo_keywords": {
            "ar": ["مواقيت الصلاة", "القرآن الكريم", "أذكار", "أدعية", "حكاياتي", "منصة إسلامية"],
            "en": ["prayer times", "quran", "islamic app", "muslim", "azkar", "duas"],
            "ru": ["время молитв", "коран", "исламское приложение", "мусульманин", "намаз"],
            "tr": ["namaz vakitleri", "kuran", "islam uygulaması", "müslüman", "dua", "zikir"],
            "de": ["gebetszeiten", "koran", "islamische app", "muslim", "dhikr", "dua"],
        },
    }

@router.get("/localization/strings/{lang}")
async def get_ui_strings(lang: str):
    """Get UI translations for a specific language"""
    strings = {
        "ar": {
            "home": "الرئيسية", "prayer_times": "مواقيت الصلاة", "quran": "القرآن الكريم",
            "qibla": "اتجاه القبلة", "tasbeeh": "التسبيح", "duas": "الأدعية",
            "stories": "حكاياتي", "messages": "الرسائل", "more": "المزيد",
            "login": "تسجيل الدخول", "register": "إنشاء حساب", "profile": "الملف الشخصي",
            "follow": "متابعة", "following": "متابَع", "followers": "متابعين",
            "likes": "الإعجابات", "comments": "التعليقات", "share": "مشاركة",
            "create_post": "إنشاء منشور", "trending": "الترندات", "video": "فيديو",
            "search": "بحث", "settings": "الإعدادات", "logout": "خروج",
        },
        "en": {
            "home": "Home", "prayer_times": "Prayer Times", "quran": "Quran",
            "qibla": "Qibla", "tasbeeh": "Tasbeeh", "duas": "Duas",
            "stories": "Hikayati", "messages": "Messages", "more": "More",
            "login": "Login", "register": "Register", "profile": "Profile",
            "follow": "Follow", "following": "Following", "followers": "Followers",
            "likes": "Likes", "comments": "Comments", "share": "Share",
            "create_post": "Create Post", "trending": "Trending", "video": "Video",
            "search": "Search", "settings": "Settings", "logout": "Logout",
        },
        "ru": {
            "home": "Главная", "prayer_times": "Время молитв", "quran": "Коран",
            "qibla": "Кибла", "tasbeeh": "Тасбих", "duas": "Дуа",
            "stories": "Хикаяти", "messages": "Сообщения", "more": "Ещё",
            "login": "Войти", "register": "Регистрация", "profile": "Профиль",
            "follow": "Подписаться", "following": "Подписан", "followers": "Подписчики",
            "likes": "Нравится", "comments": "Комментарии", "share": "Поделиться",
            "create_post": "Создать пост", "trending": "В тренде", "video": "Видео",
            "search": "Поиск", "settings": "Настройки", "logout": "Выход",
        },
        "tr": {
            "home": "Ana Sayfa", "prayer_times": "Namaz Vakitleri", "quran": "Kur'an",
            "qibla": "Kıble", "tasbeeh": "Tesbih", "duas": "Dualar",
            "stories": "Hikayelerim", "messages": "Mesajlar", "more": "Daha Fazla",
            "login": "Giriş", "register": "Kayıt Ol", "profile": "Profil",
            "follow": "Takip Et", "following": "Takip Ediliyor", "followers": "Takipçiler",
            "likes": "Beğeniler", "comments": "Yorumlar", "share": "Paylaş",
            "create_post": "Gönderi Oluştur", "trending": "Trendler", "video": "Video",
            "search": "Ara", "settings": "Ayarlar", "logout": "Çıkış",
        },
        "de": {
            "home": "Startseite", "prayer_times": "Gebetszeiten", "quran": "Koran",
            "qibla": "Qibla", "tasbeeh": "Tasbih", "duas": "Bittgebete",
            "stories": "Hikayati", "messages": "Nachrichten", "more": "Mehr",
            "login": "Anmelden", "register": "Registrieren", "profile": "Profil",
            "follow": "Folgen", "following": "Gefolgt", "followers": "Follower",
            "likes": "Gefällt mir", "comments": "Kommentare", "share": "Teilen",
            "create_post": "Beitrag erstellen", "trending": "Trends", "video": "Video",
            "search": "Suche", "settings": "Einstellungen", "logout": "Abmelden",
        },
    }
    return {"lang": lang, "strings": strings.get(lang, strings["ar"]), "dir": "rtl" if lang == "ar" else "ltr"}

# ==================== STORIES SYSTEM (حكايات) ====================
# Uses the existing posts/comments/likes collections but with story-specific endpoints

STORY_CATEGORIES = [
    {"key": "general", "label": "عام", "labelKey": "storyCatGeneral", "emoji": "📝", "icon": "file-text", "color": "#64748b"},
    {"key": "istighfar", "label": "قصص الاستغفار", "labelKey": "storyCatIstighfar", "emoji": "🤲", "icon": "sparkles", "color": "#10b981"},
    {"key": "sahaba", "label": "قصص الصحابة", "labelKey": "storyCatSahaba", "emoji": "📖", "icon": "book", "color": "#f59e0b"},
    {"key": "quran", "label": "قصص القرآن", "labelKey": "storyCatQuran", "emoji": "📗", "icon": "book-open", "color": "#059669"},
    {"key": "prophets", "label": "قصص الأنبياء", "labelKey": "storyCatProphets", "emoji": "🌟", "icon": "star", "color": "#8b5cf6"},
    {"key": "ruqyah", "label": "قصص الرقية", "labelKey": "storyCatRuqyah", "emoji": "🛡️", "icon": "shield", "color": "#3b82f6"},
    {"key": "rizq", "label": "قصص الرزق", "labelKey": "storyCatRizq", "emoji": "✨", "icon": "coins", "color": "#eab308"},
    {"key": "tawba", "label": "قصص التوبة", "labelKey": "storyCatTawba", "emoji": "💚", "icon": "heart", "color": "#22c55e"},
    {"key": "miracles", "label": "معجزات وعبر", "labelKey": "storyCatMiracles", "emoji": "🌙", "icon": "moon", "color": "#6366f1"},
    {"key": "embed", "label": "فيديوهات", "labelKey": "storyCatEmbed", "emoji": "🎬", "icon": "film", "color": "#ef4444"},
]

