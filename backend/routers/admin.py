"""
Router: admin
"""
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from deps import db, get_user, logger, security, verify_jwt, create_jwt, hash_password, check_password, ADMIN_EMAILS, STRIPE_API_KEY, EMERGENT_LLM_KEY, haversine, query_overpass, clean_time, OVERPASS_ENDPOINTS, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_EMAIL, FIREBASE_PROJECT_ID, RESEND_API_KEY, GEMINI_API_KEY
from starlette.requests import Request
from deps import get_admin_user
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
from deps import get_admin_user

router = APIRouter(tags=["Admin"])

ADMIN_EMAILS = ['mohammadalrejab@gmail.com']

from fastapi.security import HTTPAuthorizationCredentials

async def get_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="غير مصرح")
    payload = verify_jwt(credentials.credentials)
    if not payload or payload.get("email") not in ADMIN_EMAILS:
        raise HTTPException(status_code=403, detail="غير مصرح - ليس مسؤولاً")
    return payload

# OLD admin stats endpoint - replaced with new one below
# @router.get("/admin/stats")
# async def admin_stats(admin=Depends(get_admin_user)):
#     """Dashboard statistics"""
#     users_count = await db.users.count_documents({})
#     push_subs = await db.push_subscriptions.count_documents({})
#     status_checks = await db.status_checks.count_documents({})
#     
#     # Recent users
#     recent_users = await db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).to_list(10)
#     
#     return {
#         "stats": {
#             "total_users": users_count,
#             "push_subscribers": push_subs,
#             "status_checks": status_checks,
#         },
#         "recent_users": recent_users,
#     }

@router.get("/admin/users")
async def admin_users(admin=Depends(get_admin_user), page: int = 1, limit: int = 20):
    """List all users"""
    skip = (page - 1) * limit
    users = await db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).skip(skip).to_list(limit)
    total = await db.users.count_documents({})
    return {"users": users, "total": total, "page": page, "pages": math.ceil(total / limit)}

@router.delete("/admin/users/{user_id}")
async def admin_delete_user(user_id: str, admin=Depends(get_admin_user)):
    """Delete a user"""
    result = await db.users.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return {"success": True, "message": "تم حذف المستخدم"}

@router.get("/admin/push-subscriptions")
async def admin_push_subs(admin=Depends(get_admin_user)):
    """List push subscriptions"""
    subs = await db.push_subscriptions.find({}, {"_id": 0}).to_list(100)
    return {"subscriptions": subs, "total": len(subs)}

class AdminNotification(BaseModel):
    title: str
    body: str
    target: str = "all"  # all, prayer, custom

@router.post("/admin/send-notification")
async def admin_send_notification(data: AdminNotification, admin=Depends(get_admin_user)):
    """Send notification to all users (placeholder - needs VAPID for actual push)"""
    subs = await db.push_subscriptions.find({}, {"_id": 0}).to_list(1000)
    return {
        "success": True,
        "message": f"تم إرسال الإشعار إلى {len(subs)} مشترك",
        "title": data.title,
        "body": data.body,
        "target_count": len(subs),
    }

class AdminAppSettings(BaseModel):
    app_name: Optional[str] = None
    default_method: Optional[int] = None
    default_school: Optional[int] = None
    maintenance_mode: Optional[bool] = None
    announcement: Optional[str] = None
    # Ad Settings
    ads_enabled: Optional[bool] = None
    video_ads_muted: Optional[bool] = None
    gdpr_consent_required: Optional[bool] = None
    admob_app_id: Optional[str] = None
    adsense_publisher_id: Optional[str] = None
    ad_banner_enabled: Optional[bool] = None
    ad_interstitial_enabled: Optional[bool] = None
    ad_rewarded_enabled: Optional[bool] = None

class AdPlacement(BaseModel):
    id: Optional[str] = None
    name: str
    provider: str  # exoclick, popads, clickadu, hilltopads, monetag, adsterra, ysense, admob, adsense, youtube, custom
    code: str = ""
    placement: str = "home"  # home, prayer, quran, duas, ruqyah, notifications, all
    ad_type: str = "banner"  # banner, interstitial, native, video, popup
    enabled: bool = True
    priority: int = 0

@router.get("/admin/ads")
async def admin_get_ads(admin=Depends(get_admin_user)):
    """List all ad placements"""
    ads = await db.ad_placements.find({}, {"_id": 0}).sort("priority", -1).to_list(100)
    return {"ads": ads, "total": len(ads)}

@router.post("/admin/ads")
async def admin_create_ad(ad: AdPlacement, admin=Depends(get_admin_user)):
    """Create or update ad placement"""
    ad_dict = ad.dict()
    if not ad_dict.get("id"):
        ad_dict["id"] = str(uuid.uuid4())[:8]
    ad_dict["created_at"] = datetime.utcnow().isoformat()
    ad_dict["created_by"] = admin.get("email", "")
    
    await db.ad_placements.update_one(
        {"id": ad_dict["id"]},
        {"$set": ad_dict},
        upsert=True
    )
    return {"success": True, "ad": ad_dict}

@router.delete("/admin/ads/{ad_id}")
async def admin_delete_ad(ad_id: str, admin=Depends(get_admin_user)):
    """Delete ad placement"""
    result = await db.ad_placements.delete_one({"id": ad_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="الإعلان غير موجود")
    return {"success": True}

@router.get("/ads/active")
async def get_active_ads(placement: str = "all"):
    """Public endpoint - get active ads for a placement"""
    query = {"enabled": True}
    if placement != "all":
        query["$or"] = [{"placement": placement}, {"placement": "all"}]
    ads = await db.ad_placements.find(query, {"_id": 0}).sort("priority", -1).to_list(20)
    return {"ads": ads}

# Story moderation
@router.get("/admin/stories")
async def admin_get_stories(admin=Depends(get_admin_user), status: str = "pending"):
    """List stories for moderation"""
    stories = await db.stories.find({"status": status}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"stories": stories, "total": len(stories)}

@router.put("/admin/stories/{story_id}")
async def admin_moderate_story(story_id: str, data: dict, admin=Depends(get_admin_user)):
    """Approve or reject a story"""
    action = data.get("action", "")
    if action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="إجراء غير صالح")
    
    update = {
        "status": "approved" if action == "approve" else "rejected",
        "moderated_by": admin.get("email", ""),
        "moderated_at": datetime.utcnow().isoformat(),
    }
    result = await db.stories.update_one({"id": story_id}, {"$set": update})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="القصة غير موجودة")
    return {"success": True, "status": update["status"]}

# Custom pages management  
class CustomPage(BaseModel):
    id: Optional[str] = None
    title: str
    category: str = ""
    content: str = ""
    enabled: bool = True
    order: int = 0

@router.get("/admin/pages")
async def admin_get_pages(admin=Depends(get_admin_user)):
    """List custom pages"""
    pages = await db.custom_pages.find({}, {"_id": 0}).sort("order", 1).to_list(100)
    return {"pages": pages}

@router.post("/admin/pages")
async def admin_create_page(page: CustomPage, admin=Depends(get_admin_user)):
    """Create or update custom page"""
    page_dict = page.dict()
    if not page_dict.get("id"):
        page_dict["id"] = str(uuid.uuid4())[:8]
    page_dict["updated_at"] = datetime.utcnow().isoformat()
    page_dict["updated_by"] = admin.get("email", "")
    
    await db.custom_pages.update_one(
        {"id": page_dict["id"]},
        {"$set": page_dict},
        upsert=True
    )
    return {"success": True, "page": page_dict}

@router.delete("/admin/pages/{page_id}")
async def admin_delete_page(page_id: str, admin=Depends(get_admin_user)):
    await db.custom_pages.delete_one({"id": page_id})
    return {"success": True}

@router.get("/pages")
async def get_public_pages(category: str = ""):
    """Public - get enabled custom pages"""
    query = {"enabled": True}
    if category:
        query["category"] = category
    pages = await db.custom_pages.find(query, {"_id": 0}).sort("order", 1).to_list(50)
    return {"pages": pages}

# ===== RUQYAH MANAGEMENT =====
class RuqyahItem(BaseModel):
    id: Optional[str] = None
    title: str
    content: str = ""
    category: str = "general"  # عين, حسد, سحر, مس, general
    audio_url: str = ""
    video_url: str = ""  # Original URL from YouTube/Vimeo/Dailymotion etc.
    embed_url: str = ""  # Auto-generated embed URL for iframe
    video_type: str = ""  # youtube, vimeo, dailymotion, facebook, custom
    thumbnail_url: str = ""  # Video thumbnail
    order: int = 0
    enabled: bool = True


def parse_video_url(url: str) -> dict:
    """Parse video URL and return embed URL, video type, and thumbnail"""
    if not url:
        return {"embed_url": "", "video_type": "", "thumbnail_url": ""}
    
    import re
    
    # YouTube
    yt_match = re.match(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})', url)
    if yt_match:
        vid = yt_match.group(1)
        return {
            "embed_url": f"https://www.youtube.com/embed/{vid}",
            "video_type": "youtube",
            "thumbnail_url": f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        }
    
    # Vimeo
    vm_match = re.match(r'(?:https?://)?(?:www\.)?vimeo\.com/(\d+)', url)
    if vm_match:
        vid = vm_match.group(1)
        return {
            "embed_url": f"https://player.vimeo.com/video/{vid}",
            "video_type": "vimeo",
            "thumbnail_url": ""
        }
    
    # Dailymotion
    dm_match = re.match(r'(?:https?://)?(?:www\.)?dailymotion\.com/video/([a-zA-Z0-9]+)', url)
    if dm_match:
        vid = dm_match.group(1)
        return {
            "embed_url": f"https://www.dailymotion.com/embed/video/{vid}",
            "video_type": "dailymotion",
            "thumbnail_url": f"https://www.dailymotion.com/thumbnail/video/{vid}"
        }

    # Facebook Video
    if 'facebook.com' in url or 'fb.watch' in url:
        from urllib.parse import quote
        return {
            "embed_url": f"https://www.facebook.com/plugins/video.php?href={quote(url)}&show_text=false",
            "video_type": "facebook",
            "thumbnail_url": ""
        }

    # If already an embed URL or custom
    if '/embed/' in url or 'player.' in url:
        return {"embed_url": url, "video_type": "custom", "thumbnail_url": ""}
    
    # Generic - return as-is for custom embed
    return {"embed_url": url, "video_type": "custom", "thumbnail_url": ""}

@router.get("/admin/ruqyah")
async def admin_get_ruqyah(admin=Depends(get_admin_user)):
    items = await db.ruqyah_items.find({}, {"_id": 0}).sort("order", 1).to_list(200)
    return {"items": items}

@router.post("/admin/ruqyah")
async def admin_save_ruqyah(item: RuqyahItem, admin=Depends(get_admin_user)):
    item_dict = item.dict()
    if not item_dict.get("id"):
        item_dict["id"] = str(uuid.uuid4())[:8]
    # Auto-parse video URL to get embed URL, type, and thumbnail
    if item_dict.get("video_url"):
        video_info = parse_video_url(item_dict["video_url"])
        item_dict["embed_url"] = video_info["embed_url"]
        item_dict["video_type"] = video_info["video_type"]
        if video_info["thumbnail_url"]:
            item_dict["thumbnail_url"] = video_info["thumbnail_url"]
    item_dict["updated_at"] = datetime.utcnow().isoformat()
    await db.ruqyah_items.update_one({"id": item_dict["id"]}, {"$set": item_dict}, upsert=True)
    return {"success": True, "item": item_dict}

@router.delete("/admin/ruqyah/{item_id}")
async def admin_delete_ruqyah(item_id: str, admin=Depends(get_admin_user)):
    await db.ruqyah_items.delete_one({"id": item_id})
    return {"success": True}

@router.get("/ruqyah")
async def get_public_ruqyah(category: str = ""):
    query = {"enabled": True}
    if category:
        query["category"] = category
    items = await db.ruqyah_items.find(query, {"_id": 0}).sort("order", 1).to_list(200)
    return {"items": items}

# ===== ADMIN ALL STORIES (with status filter) =====
@router.get("/admin/all-stories")
async def admin_get_all_stories(admin=Depends(get_admin_user), status: str = "", page: int = 1, limit: int = 30):
    query = {}
    if status:
        query["status"] = status
    skip = (page - 1) * limit
    stories = await db.stories.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.stories.count_documents(query)
    return {"stories": stories, "total": total, "page": page}

@router.delete("/admin/stories/{story_id}")
async def admin_delete_story(story_id: str, admin=Depends(get_admin_user)):
    await db.stories.delete_one({"id": story_id})
    return {"success": True}

# ===== DONATIONS ADMIN =====
@router.get("/admin/donations")
async def admin_get_donations(admin=Depends(get_admin_user), status: str = ""):
    query = {}
    if status:
        query["status"] = status
    donations = await db.donations.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    total_amount = sum(d.get("amount", 0) for d in donations if d.get("status") == "approved")
    return {"donations": donations, "total": len(donations), "total_amount": total_amount}

@router.put("/admin/donations/{donation_id}")
async def admin_moderate_donation(donation_id: str, data: dict, admin=Depends(get_admin_user)):
    action = data.get("action", "")
    if action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="action invalid")
    update = {
        "status": "approved" if action == "approve" else "rejected",
        "moderated_by": admin.get("email", ""),
        "moderated_at": datetime.utcnow().isoformat(),
    }
    await db.donations.update_one({"id": donation_id}, {"$set": update})
    return {"success": True, "status": update["status"]}

@router.delete("/admin/donations/{donation_id}")
async def admin_delete_donation(donation_id: str, admin=Depends(get_admin_user)):
    await db.donations.delete_one({"id": donation_id})
    return {"success": True}



# Notification scheduling
class ScheduledNotification(BaseModel):
    id: Optional[str] = None
    title: str
    body: str
    schedule_time: str = ""  # HH:MM or empty for immediate
    repeat: str = "once"  # once, daily, weekly
    target: str = "all"
    enabled: bool = True

@router.get("/admin/scheduled-notifications")
async def admin_get_scheduled_notifs(admin=Depends(get_admin_user)):
    notifs = await db.scheduled_notifications.find({}, {"_id": 0}).to_list(50)
    return {"notifications": notifs}

@router.post("/admin/scheduled-notifications")
async def admin_create_scheduled_notif(notif: ScheduledNotification, admin=Depends(get_admin_user)):
    notif_dict = notif.dict()
    if not notif_dict.get("id"):
        notif_dict["id"] = str(uuid.uuid4())[:8]
    notif_dict["created_at"] = datetime.utcnow().isoformat()
    
    await db.scheduled_notifications.update_one(
        {"id": notif_dict["id"]},
        {"$set": notif_dict},
        upsert=True
    )
    return {"success": True, "notification": notif_dict}

@router.delete("/admin/scheduled-notifications/{notif_id}")
async def admin_delete_scheduled_notif(notif_id: str, admin=Depends(get_admin_user)):
    await db.scheduled_notifications.delete_one({"id": notif_id})
    return {"success": True}

@router.get("/admin/settings")
async def admin_get_settings(admin=Depends(get_admin_user)):
    """Get app settings"""
    settings = await db.app_settings.find_one({"key": "global"}, {"_id": 0})
    if not settings:
        settings = {
            "key": "global",
            "app_name": "أذان وحكاية",
            "default_method": 4,
            "default_school": 0,
            "maintenance_mode": False,
            "announcement": "",
            "ads_enabled": True,
            "video_ads_muted": True,
            "gdpr_consent_required": True,
            "ad_banner_enabled": True,
            "ad_interstitial_enabled": False,
            "ad_rewarded_enabled": True,
            "admob_app_id": "",
            "adsense_publisher_id": "",
        }
    return settings

@router.put("/admin/settings")
async def admin_update_settings(data: AdminAppSettings, admin=Depends(get_admin_user)):
    """Update app settings"""
    update = {k: v for k, v in data.dict().items() if v is not None}
    update["updated_at"] = datetime.utcnow().isoformat()
    update["updated_by"] = admin.get("email", "")
    
    # Ensure defaults are preserved
    existing = await db.app_settings.find_one({"key": "global"}, {"_id": 0}) or {}
    merged = {**existing, **update, "key": "global"}
    
    await db.app_settings.replace_one(
        {"key": "global"},
        merged,
        upsert=True
    )
    return {"success": True, "message": "تم تحديث الإعدادات"}

# ==================== PUBLIC AD CONFIG (إعدادات الإعلانات العامة) ====================

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

