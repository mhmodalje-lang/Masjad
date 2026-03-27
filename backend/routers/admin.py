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
import asyncio

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
    # Moderation Settings
    story_moderation_enabled: Optional[bool] = None

class AdPlacement(BaseModel):
    id: Optional[str] = None
    name: str
    provider: str = "admob"
    code: str = ""
    link_url: str = ""  # Click-through URL for image/banner ads
    image_url: str = ""  # Image URL for display ads
    placement: str = "home"  # home, prayer, quran, duas, ruqyah, notifications, kids_zone, arabic_academy, all
    ad_type: str = "banner"  # banner, interstitial, native, video, rewarded
    enabled: bool = True
    priority: int = 0
    # Country-level targeting
    countries_enabled: List[str] = []  # Empty = all countries. ISO codes: DE, TR, US, SA, etc.
    countries_blocked: List[str] = []  # Block specific countries

class AdPageRule(BaseModel):
    """Toggle ads on/off for specific pages and countries."""
    page: str  # home, prayer, quran, duas, ruqyah, kids_zone, arabic_academy, stories, etc.
    enabled: bool = True
    countries_enabled: List[str] = []  # Empty = all
    countries_blocked: List[str] = []
    ad_types_allowed: List[str] = ["banner", "interstitial", "rewarded"]

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
    await db.ad_placements.update_one({"id": ad_dict["id"]}, {"$set": ad_dict}, upsert=True)
    return {"success": True, "ad": ad_dict}

@router.delete("/admin/ads/{ad_id}")
async def admin_delete_ad(ad_id: str, admin=Depends(get_admin_user)):
    """Delete ad placement"""
    result = await db.ad_placements.delete_one({"id": ad_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="الإعلان غير موجود")
    return {"success": True}

# ==================== ADS PAGE/COUNTRY RULES ====================

@router.get("/admin/ads/rules")
async def admin_get_ad_rules(admin=Depends(get_admin_user)):
    """Get ad rules per page/country."""
    rules = await db.ad_page_rules.find({}, {"_id": 0}).to_list(100)
    if not rules:
        # Default rules for all pages
        default_pages = ["home", "prayer", "quran", "duas", "ruqyah", "kids_zone",
                         "arabic_academy", "stories", "explore", "live_streams",
                         "tasbeeh", "qibla", "notifications", "profile"]
        rules = [{"page": p, "enabled": True, "countries_enabled": [], "countries_blocked": [], "ad_types_allowed": ["banner", "interstitial", "rewarded"]} for p in default_pages]
    return {"rules": rules}

@router.put("/admin/ads/rules")
async def admin_update_ad_rules(rules: List[AdPageRule], admin=Depends(get_admin_user)):
    """Update ad rules per page and country. God-Mode toggle."""
    for rule in rules:
        rule_dict = rule.dict()
        rule_dict["updated_at"] = datetime.utcnow().isoformat()
        rule_dict["updated_by"] = admin.get("email", "")
        await db.ad_page_rules.update_one(
            {"page": rule_dict["page"]},
            {"$set": rule_dict},
            upsert=True
        )
    return {"success": True, "message": f"Updated {len(rules)} ad rules", "rules_count": len(rules)}

@router.get("/ads/active")
async def get_active_ads(placement: str = "all", country: str = ""):
    """Public endpoint - get active ads for a placement, filtered by country."""
    # Check page rule first
    page_rule = await db.ad_page_rules.find_one({"page": placement}, {"_id": 0})
    if page_rule and not page_rule.get("enabled", True):
        return {"ads": [], "page_disabled": True}

    # Country filtering from page rule
    if page_rule and country:
        blocked = page_rule.get("countries_blocked", [])
        enabled = page_rule.get("countries_enabled", [])
        if country.upper() in blocked:
            return {"ads": [], "country_blocked": True}
        if enabled and country.upper() not in enabled:
            return {"ads": [], "country_not_enabled": True}

    query = {"enabled": True}
    if placement != "all":
        query["$or"] = [{"placement": placement}, {"placement": "all"}]
    ads = await db.ad_placements.find(query, {"_id": 0}).sort("priority", -1).to_list(20)

    # Filter by country targeting on individual ads
    if country:
        filtered = []
        for ad in ads:
            blocked = ad.get("countries_blocked", [])
            enabled = ad.get("countries_enabled", [])
            if country.upper() in blocked:
                continue
            if enabled and country.upper() not in enabled:
                continue
            filtered.append(ad)
        ads = filtered

    return {"ads": ads}

# ==================== DAILY CONTENT CRUD (Hadith/Story - No Code Push) ====================

class DailyContent(BaseModel):
    id: Optional[str] = None
    content_type: str = "hadith"  # hadith, story, dua, tip, verse
    # Multilingual content - all 10 languages
    title: Dict[str, str] = {}  # {"ar": "...", "en": "...", "de": "...", ...}
    body: Dict[str, str] = {}
    source: Dict[str, str] = {}
    arabic_text: str = ""  # Original Arabic (for hadith/verse)
    image_url: str = ""
    active: bool = True
    schedule_date: str = ""  # YYYY-MM-DD or empty for immediate
    priority: int = 0

SUPPORTED_LOCALES = ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el", "de-AT"]

@router.get("/admin/daily-content")
async def admin_get_daily_content(admin=Depends(get_admin_user), content_type: str = ""):
    """Get all daily content items."""
    query = {}
    if content_type:
        query["content_type"] = content_type
    items = await db.daily_content.find(query, {"_id": 0}).sort("priority", -1).to_list(200)
    return {"items": items, "total": len(items), "supported_locales": SUPPORTED_LOCALES}

@router.post("/admin/daily-content")
async def admin_save_daily_content(item: DailyContent, admin=Depends(get_admin_user)):
    """Create or update daily content (hadith, story, dua, tip, verse)."""
    item_dict = item.dict()
    if not item_dict.get("id"):
        item_dict["id"] = str(uuid.uuid4())[:8]
    item_dict["updated_at"] = datetime.utcnow().isoformat()
    item_dict["updated_by"] = admin.get("email", "")
    await db.daily_content.update_one({"id": item_dict["id"]}, {"$set": item_dict}, upsert=True)
    return {"success": True, "item": item_dict}

@router.delete("/admin/daily-content/{item_id}")
async def admin_delete_daily_content(item_id: str, admin=Depends(get_admin_user)):
    """Delete daily content item."""
    await db.daily_content.delete_one({"id": item_id})
    return {"success": True}

@router.get("/daily-content/today")
async def get_today_daily_content(content_type: str = "hadith", locale: str = "ar"):
    """Public - get today's daily content in user's language."""
    today = date.today().isoformat()

    # Try scheduled content for today
    item = await db.daily_content.find_one(
        {"content_type": content_type, "active": True, "schedule_date": today},
        {"_id": 0}
    )

    # Fallback to any active content (rotation by day of year)
    if not item:
        items = await db.daily_content.find(
            {"content_type": content_type, "active": True},
            {"_id": 0}
        ).sort("priority", -1).to_list(365)

        if items:
            day_of_year = datetime.utcnow().timetuple().tm_yday
            item = items[day_of_year % len(items)]

    if not item:
        return {"success": False, "message": "No content available"}

    # Resolve locale - use exact match, then base language, then ar
    def resolve_text(field_dict, loc):
        if not isinstance(field_dict, dict):
            return field_dict if isinstance(field_dict, str) else ""
        text = field_dict.get(loc)
        if not text and "-" in loc:
            text = field_dict.get(loc.split("-")[0])
        if not text:
            text = field_dict.get("ar", "")
        return text or ""

    return {
        "success": True,
        "content_type": item.get("content_type", content_type),
        "title": resolve_text(item.get("title", {}), locale),
        "body": resolve_text(item.get("body", {}), locale),
        "source": resolve_text(item.get("source", {}), locale),
        "arabic_text": item.get("arabic_text", ""),
        "image_url": item.get("image_url", ""),
        "locale": locale,
    }

# ==================== MULTILINGUAL PUSH NOTIFICATION ENGINE ====================

class MultilingualNotification(BaseModel):
    """Send push notifications in user's saved locale."""
    title: Dict[str, str] = {}  # {"ar": "...", "en": "...", "de": "...", ...}
    body: Dict[str, str] = {}
    target: str = "all"  # all, locale:ar, locale:de, country:DE, user:user_id
    url: str = ""  # Deep link URL
    image_url: str = ""
    schedule_time: str = ""  # ISO datetime or empty for immediate
    priority: str = "normal"  # normal, high

@router.post("/admin/notifications/send-multilingual")
async def admin_send_multilingual_notification(data: MultilingualNotification, admin=Depends(get_admin_user)):
    """Send push notification in each user's saved locale. Auto-detects language."""
    subs = await db.push_subscriptions.find({}, {"_id": 0}).to_list(10000)

    sent_count = 0
    locale_counts = {}

    for sub in subs:
        user_locale = sub.get("locale", sub.get("language", "ar"))
        base_locale = user_locale.split("-")[0] if "-" in user_locale else user_locale

        # Check targeting
        if data.target.startswith("locale:"):
            target_locale = data.target.split(":")[1]
            if user_locale != target_locale and base_locale != target_locale:
                continue
        elif data.target.startswith("country:"):
            target_country = data.target.split(":")[1].upper()
            if sub.get("country", "").upper() != target_country:
                continue
        elif data.target.startswith("user:"):
            target_user = data.target.split(":")[1]
            if sub.get("user_id", "") != target_user:
                continue

        # Resolve notification text for this user's locale
        title = data.title.get(user_locale) or data.title.get(base_locale) or data.title.get("ar", "")
        body = data.body.get(user_locale) or data.body.get(base_locale) or data.body.get("ar", "")

        # In production, this would send via Web Push / FCM
        # For now, log the notification
        await db.notification_log.insert_one({
            "id": str(uuid.uuid4()),
            "subscription_id": sub.get("id", ""),
            "user_id": sub.get("user_id", ""),
            "locale": user_locale,
            "title": title,
            "body": body,
            "url": data.url,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat(),
        })

        sent_count += 1
        locale_counts[user_locale] = locale_counts.get(user_locale, 0) + 1

    # Save notification record
    await db.sent_notifications.insert_one({
        "id": str(uuid.uuid4()),
        "title": data.title,
        "body": data.body,
        "target": data.target,
        "url": data.url,
        "total_sent": sent_count,
        "locale_breakdown": locale_counts,
        "sent_by": admin.get("email", ""),
        "created_at": datetime.utcnow().isoformat(),
    })

    return {
        "success": True,
        "total_sent": sent_count,
        "locale_breakdown": locale_counts,
        "supported_locales": SUPPORTED_LOCALES,
    }

@router.get("/admin/notifications/history")
async def admin_get_notification_history(admin=Depends(get_admin_user), limit: int = 50):
    """Get notification send history."""
    history = await db.sent_notifications.find({}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    return {"notifications": history, "total": len(history)}

# ==================== ADMIN STATS (Enhanced God-Mode) ====================

@router.get("/admin/stats")
async def admin_stats(admin=Depends(get_admin_user)):
    """Enhanced dashboard statistics - God Mode."""
    users_count = await db.users.count_documents({})
    push_subs = await db.push_subscriptions.count_documents({})
    kids_profiles = await db.kids_points.count_documents({})
    adult_profiles = await db.adult_points.count_documents({})
    total_ads_watched = await db.ad_watch_log.count_documents({})
    stories_count = await db.posts.count_documents({"is_story": True})
    daily_content_count = await db.daily_content.count_documents({})

    # Today's activity
    today = date.today().isoformat()
    today_ads = await db.ad_watch_log.count_documents({"date": today})
    today_points = await db.points_transactions.count_documents({"created_at": {"$regex": f"^{today}"}})

    # Recent users
    recent_users = await db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).to_list(10)

    return {
        "stats": {
            "total_users": users_count,
            "push_subscribers": push_subs,
            "kids_profiles": kids_profiles,
            "adult_profiles": adult_profiles,
            "total_ads_watched": total_ads_watched,
            "today_ads_watched": today_ads,
            "today_points_earned": today_points,
            "total_stories": stories_count,
            "daily_content_items": daily_content_count,
        },
        "recent_users": recent_users,
    }

# Story moderation
@router.get("/admin/stories")
async def admin_get_stories(admin=Depends(get_admin_user), status: str = "pending"):
    """List stories for moderation"""
    query = {"is_story": True}
    if status:
        query["status"] = status
    stories = await db.posts.find(query, {"_id": 0}).sort("created_at", -1).to_list(50)
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
    result = await db.posts.update_one({"id": story_id}, {"$set": update})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="القصة غير موجودة")
    return {"success": True, "status": update["status"]}


# ===== PUBLISH REQUESTS MANAGEMENT =====
@router.get("/admin/publish-requests")
async def admin_get_publish_requests(admin=Depends(get_admin_user), status: str = ""):
    """List user publish requests"""
    query = {}
    if status:
        query["status"] = status
    requests = await db.publish_requests.find(query, {"_id": 0}).sort("requested_at", -1).to_list(100)
    return {"requests": requests, "total": len(requests)}

@router.put("/admin/publish-requests/{user_id}")
async def admin_handle_publish_request(user_id: str, data: dict, admin=Depends(get_admin_user)):
    """Approve or revoke user publish permission"""
    action = data.get("action", "")
    if action not in ["approve", "revoke"]:
        raise HTTPException(status_code=400, detail="إجراء غير صالح - استخدم approve أو revoke")
    
    new_status = "approved" if action == "approve" else "revoked"
    result = await db.publish_requests.update_one(
        {"user_id": user_id},
        {"$set": {
            "status": new_status,
            "handled_by": admin.get("email", ""),
            "handled_at": datetime.utcnow().isoformat(),
        }}
    )
    if result.modified_count == 0:
        # Create a record if it doesn't exist
        await db.publish_requests.insert_one({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "status": new_status,
            "handled_by": admin.get("email", ""),
            "handled_at": datetime.utcnow().isoformat(),
            "requested_at": datetime.utcnow().isoformat(),
        })
    return {"success": True, "status": new_status}


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
    query = {"is_story": True}
    if status:
        query["status"] = status
    skip = (page - 1) * limit
    stories = await db.posts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.posts.count_documents(query)
    return {"stories": stories, "total": total, "page": page}

@router.delete("/admin/stories/{story_id}")
async def admin_delete_story(story_id: str, admin=Depends(get_admin_user)):
    await db.posts.delete_one({"id": story_id})
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
            "story_moderation_enabled": True,
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



# ===== AI STORY GENERATION =====
STORY_CATEGORIES_INFO = {
    "istighfar": {"label": "قصص الاستغفار", "prompt": "قصص حقيقية ومؤثرة عن الاستغفار وفضله وكيف غير حياة أشخاص حقيقيين. قصص عن أثر الاستغفار في تفريج الهموم وفتح أبواب الرزق والشفاء"},
    "sahaba": {"label": "قصص الصحابة", "prompt": "قصص حقيقية من سيرة الصحابة رضي الله عنهم وبطولاتهم وتضحياتهم ومواقفهم المؤثرة في الإسلام"},
    "quran": {"label": "قصص القرآن", "prompt": "قصص مذكورة في القرآن الكريم مع شرح العبر والدروس المستفادة منها بأسلوب قصصي شيق"},
    "prophets": {"label": "قصص الأنبياء", "prompt": "قصص الأنبياء والرسل عليهم السلام ومعجزاتهم ودعوتهم ومواقفهم مع أقوامهم"},
    "ruqyah": {"label": "قصص الرقية", "prompt": "قصص حقيقية عن الشفاء بالرقية الشرعية والقرآن الكريم والأذكار وتجارب أشخاص شفاهم الله"},
    "rizq": {"label": "قصص الرزق", "prompt": "قصص حقيقية عن سعة الرزق والبركة فيه وكيف جاء الرزق من حيث لا يحتسب بفضل التوكل والدعاء"},
    "tawba": {"label": "قصص التوبة", "prompt": "قصص حقيقية مؤثرة عن التوبة والرجوع إلى الله وكيف تغيرت حياة أشخاص بعد التوبة النصوحة"},
    "miracles": {"label": "معجزات وعبر", "prompt": "قصص عن معجزات إلهية وعبر ومواقف عجيبة تدل على قدرة الله وحكمته"},
    "general": {"label": "قصص عامة", "prompt": "قصص إسلامية متنوعة عن الإيمان والأخلاق والمعاملات والحياة اليومية بمنظور إسلامي"},
}

# Track generation progress
generation_progress = {}

SUPPORTED_STORY_LANGS = {
    "ar": {"name": "أذان وحكاية", "instruction": "اكتب القصص باللغة العربية الفصحى بأسلوب أدبي مشوق"},
    "en": {"name": "Azan & Hikaya", "instruction": "Write the stories in fluent English with an engaging narrative style"},
    "de": {"name": "Azan & Hikaya", "instruction": "Schreibe die Geschichten auf fließendem Deutsch mit einem fesselnden Erzählstil"},
    "fr": {"name": "Azan & Hikaya", "instruction": "Écrivez les histoires en français courant avec un style narratif captivant"},
    "tr": {"name": "Azan & Hikaya", "instruction": "Hikayeleri akıcı Türkçe ile ilgi çekici bir anlatım tarzıyla yazın"},
    "ru": {"name": "Azan & Hikaya", "instruction": "Напишите истории на беглом русском языке с увлекательным повествовательным стилем"},
    "sv": {"name": "Azan & Hikaya", "instruction": "Skriv berättelserna på flytande svenska med en engagerande berättarstil"},
    "nl": {"name": "Azan & Hikaya", "instruction": "Schrijf de verhalen in vloeiend Nederlands met een boeiende vertelstijl"},
    "el": {"name": "Azan & Hikaya", "instruction": "Γράψτε τις ιστορίες σε άπταιστα ελληνικά με ένα συναρπαστικό αφηγηματικό ύφος"},
    "de-AT": {"name": "Azan & Hikaya", "instruction": "Schreibe die Geschichten auf fließendem österreichischem Deutsch mit einem fesselnden Erzählstil"},
}

async def generate_stories_batch(category: str, batch_num: int, count: int = 10, lang: str = "ar"):
    """Generate a batch of stories using AI"""
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    import json as json_lib
    
    cat_info = STORY_CATEGORIES_INFO.get(category)
    if not cat_info:
        return []
    
    lang_info = SUPPORTED_STORY_LANGS.get(lang, SUPPORTED_STORY_LANGS["ar"])
    
    llm_key = os.environ.get("EMERGENT_LLM_KEY", "")
    if not llm_key:
        logger.error("EMERGENT_LLM_KEY not found")
        return []
    
    system_msg = f"""{lang_info['instruction']}.
أنت كاتب قصص إسلامية محترف.
القصص يجب أن تكون:
- مبنية على أحداث واقعية أو مستوحاة من الواقع
- مكتوبة بأسلوب أدبي جذاب ومشوق
- تحتوي على عبرة ودرس مفيد
- مناسبة لجميع الأعمار
- متنوعة المواضيع ضمن الفئة المطلوبة
- طول كل قصة بين 150-400 كلمة

أرجع النتيجة كـ JSON array فقط بدون أي نص إضافي."""
    
    chat = LlmChat(
        api_key=llm_key,
        session_id=f"story-gen-{category}-{lang}-{batch_num}",
        system_message=system_msg
    )
    chat.with_model("openai", "gpt-4.1-mini")
    
    prompt = f"""اكتب {count} قصص في فئة: {cat_info['label']}
الموضوع: {cat_info['prompt']}
اللغة المطلوبة: {lang_info['instruction']}

الدفعة رقم {batch_num} - اجعل القصص فريدة ومختلفة عن بعضها.

أرجع JSON array بالشكل التالي فقط:
[
  {{"title": "عنوان القصة", "content": "نص القصة الكامل"}}
]"""
    
    try:
        response = await chat.send_message(UserMessage(text=prompt))
        # Parse the JSON from response
        text = response.strip()
        # Remove markdown code blocks if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            if text.startswith("json"):
                text = text[4:].strip()
        
        stories_data = json_lib.loads(text)
        if isinstance(stories_data, list):
            return stories_data
        return []
    except Exception as e:
        logger.error(f"Story generation error for {category} batch {batch_num}: {e}")
        return []

async def run_story_generation(category: str, total: int, admin_email: str, lang: str = "ar"):
    """Background task to generate stories for a category"""
    global generation_progress
    batch_size = 10
    batches = (total + batch_size - 1) // batch_size
    generated = 0
    
    progress_key = f"{category}_{lang}"
    lang_info = SUPPORTED_STORY_LANGS.get(lang, SUPPORTED_STORY_LANGS["ar"])
    generation_progress[progress_key] = {"total": total, "generated": 0, "status": "running", "lang": lang}
    
    for batch_num in range(1, batches + 1):
        count = min(batch_size, total - generated)
        try:
            stories = await generate_stories_batch(category, batch_num, count, lang)
            for s in stories:
                post_id = str(uuid.uuid4())
                story_doc = {
                    "id": post_id,
                    "author_id": "system",
                    "author_name": lang_info["name"],
                    "author_avatar": None,
                    "title": s.get("title", ""),
                    "content": s.get("content", ""),
                    "category": category,
                    "media_type": "text",
                    "image_url": None,
                    "video_url": None,
                    "embed_url": None,
                    "thumbnail_url": None,
                    "is_embed": False,
                    "views_count": random.randint(50, 500),
                    "created_at": datetime.utcnow().isoformat(),
                    "shares_count": random.randint(5, 50),
                    "is_story": True,
                    "status": "approved",
                    "generated_by": "ai",
                    "generated_for": admin_email,
                    "language": lang,
                }
                await db.posts.insert_one(story_doc)
                generated += 1
            
            generation_progress[progress_key] = {"total": total, "generated": generated, "status": "running", "lang": lang}
            await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"Batch {batch_num} error for {category}/{lang}: {e}")
            generation_progress[progress_key] = {"total": total, "generated": generated, "status": "error", "error": str(e), "lang": lang}
            return
    
    generation_progress[progress_key] = {"total": total, "generated": generated, "status": "done", "lang": lang}

@router.post("/admin/generate-stories")
async def admin_generate_stories(data: dict, background_tasks: BackgroundTasks, admin=Depends(get_admin_user)):
    """Generate AI stories for a category"""
    category = data.get("category", "")
    count = min(data.get("count", 10), 150)
    lang = data.get("language", "ar")
    
    if category not in STORY_CATEGORIES_INFO:
        raise HTTPException(400, f"فئة غير صالحة: {category}")
    
    progress_key = f"{category}_{lang}"
    if progress_key in generation_progress and generation_progress[progress_key].get("status") == "running":
        return {"success": False, "message": "جاري التوليد بالفعل لهذه الفئة", "progress": generation_progress[progress_key]}
    
    background_tasks.add_task(run_story_generation, category, count, admin.get("email", ""), lang)
    return {"success": True, "message": f"بدأ توليد {count} قصة في فئة {STORY_CATEGORIES_INFO[category]['label']} ({lang})", "category": category}

@router.get("/admin/generate-stories/progress")
async def admin_get_generation_progress(admin=Depends(get_admin_user)):
    """Get story generation progress"""
    return {"progress": generation_progress}

@router.post("/admin/generate-stories/all")
async def admin_generate_all_stories(data: dict, background_tasks: BackgroundTasks, admin=Depends(get_admin_user)):
    """Generate stories for all categories in all languages"""
    count_per_cat = min(data.get("count_per_category", 150), 150)
    languages = data.get("languages", ["ar"])
    
    total_tasks = 0
    for lang in languages:
        if lang not in SUPPORTED_STORY_LANGS:
            continue
        for cat in STORY_CATEGORIES_INFO:
            progress_key = f"{cat}_{lang}"
            if progress_key in generation_progress and generation_progress[progress_key].get("status") == "running":
                continue
            background_tasks.add_task(run_story_generation, cat, count_per_cat, admin.get("email", ""), lang)
            total_tasks += 1
    
    return {"success": True, "message": f"بدأ توليد {count_per_cat} قصة × {len(languages)} لغة × {len(STORY_CATEGORIES_INFO)} فئة = {total_tasks} مهمة"}
