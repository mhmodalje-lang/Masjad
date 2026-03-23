"""
Router: auth
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
from fastapi.security import HTTPAuthorizationCredentials

router = APIRouter(tags=["Authentication"])

class UserRegister(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    cover_image: Optional[str] = None

@router.put("/auth/update-profile")
async def update_profile(req: UpdateProfileRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "غير مصادق")
    update = {}
    if req.name and req.name.strip():
        update["name"] = req.name.strip()
    if req.avatar:
        update["avatar"] = req.avatar
    if req.bio is not None:
        update["bio"] = req.bio.strip()[:500]
    if req.cover_image:
        update["cover_image"] = req.cover_image
    if req.password and len(req.password) >= 6:
        import hashlib
        update["password_hash"] = hashlib.sha256(req.password.encode()).hexdigest()
    if update:
        await db.users.update_one({"id": user["id"]}, {"$set": update})
    return {"success": True, "message": "تم تحديث الملف الشخصي"}

# ==================== SOCIAL PLATFORM (صُحبة) ====================

SOHBA_CATEGORIES = [
    {"key": "general", "label": "عام", "labelKey": "sohbaCatGeneral", "icon": "globe"},
    {"key": "quran", "label": "القرآن الكريم", "labelKey": "sohbaCatQuran", "icon": "book"},
    {"key": "hadith", "label": "الحديث الشريف", "labelKey": "sohbaCatHadith", "icon": "scroll"},
    {"key": "ramadan", "label": "رمضان", "labelKey": "sohbaCatRamadan", "icon": "moon"},
    {"key": "dua", "label": "الدعاء والأذكار", "labelKey": "sohbaCatDua", "icon": "hands"},
    {"key": "stories", "label": "قصص وعبر", "labelKey": "sohbaCatStories", "icon": "feather"},
    {"key": "hajj", "label": "الحج والعمرة", "labelKey": "sohbaCatHajj", "icon": "kaaba"},
    {"key": "halal", "label": "السفر الحلال", "labelKey": "sohbaCatHalal", "icon": "plane"},
    {"key": "family", "label": "الأسرة المسلمة", "labelKey": "sohbaCatFamily", "icon": "heart"},
    {"key": "youth", "label": "الشباب", "labelKey": "sohbaCatYouth", "icon": "users"},
]

@router.post("/auth/register")
async def register(data: UserRegister):
    email = data.email.lower().strip()
    if await db.users.find_one({"email": email}):
        raise HTTPException(400, "البريد الإلكتروني مسجل مسبقاً")
    uid = str(uuid.uuid4())
    user = {
        "id": uid, "email": email,
        "name": data.name or email.split("@")[0],
        "password_hash": hash_password(data.password),
        "provider": "email",
        "created_at": datetime.utcnow().isoformat(),
        "avatar": None,
    }
    await db.users.insert_one(user)
    token = create_jwt({"user_id": uid, "email": email})
    return {"access_token": token, "token_type": "bearer", "user": {k: user[k] for k in ("id","email","name","avatar","provider")}}

@router.post("/auth/login")
async def login(data: UserLogin):
    email = data.email.lower().strip()
    user = await db.users.find_one({"email": email})
    if not user or not check_password(data.password, user.get("password_hash", "")):
        raise HTTPException(401, "بيانات الدخول غير صحيحة")
    token = create_jwt({"user_id": user["id"], "email": email})
    return {"access_token": token, "token_type": "bearer", "user": {k: user[k] for k in ("id","email","name","avatar","provider") if k in user}}

@router.post("/auth/google")
async def google_login(data: dict):
    """Exchange Emergent OAuth session_id for app JWT"""
    session_id = data.get("session_id")
    if not session_id:
        raise HTTPException(400, "session_id مطلوب")

    # REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
                headers={"X-Session-ID": session_id}
            )
            if r.status_code != 200:
                raise HTTPException(401, "جلسة Google غير صالحة")
            gdata = r.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(401, "فشل التحقق من Google")

    email = gdata.get("email", "")
    name = gdata.get("name", email.split("@")[0])
    photo = gdata.get("picture", None)
    google_id = gdata.get("id", "")

    if not email:
        raise HTTPException(400, "لم يتم الحصول على البريد الإلكتروني من Google")

    # Upsert user
    user = await db.users.find_one({"email": email})
    if not user:
        uid = str(uuid.uuid4())
        user = {
            "id": uid, "email": email, "name": name,
            "avatar": photo, "provider": "google",
            "google_id": google_id,
            "created_at": datetime.utcnow().isoformat(),
        }
        await db.users.insert_one(user)
    else:
        await db.users.update_one({"id": user["id"]}, {"$set": {"name": name, "avatar": photo, "google_id": google_id, "provider": "google"}})
        user["name"] = name
        user["avatar"] = photo

    token = create_jwt({"user_id": user["id"], "email": email})
    return {"access_token": token, "token_type": "bearer", "user": {k: user.get(k) for k in ("id","email","name","avatar","provider")}}

@router.post("/auth/forgot-password")
async def forgot_password(data: dict):
    """Send password reset (placeholder - shows message to user)"""
    email = data.get("email", "").lower().strip()
    if not email:
        raise HTTPException(400, "البريد الإلكتروني مطلوب")
    user = await db.users.find_one({"email": email})
    if not user:
        # Don't reveal if email exists
        return {"message": "إذا كان البريد مسجلاً سيتم إرسال رابط إعادة تعيين كلمة المرور"}
    # For now return success message - real email sending would need SendGrid/etc
    return {"message": "إذا كان البريد مسجلاً سيتم إرسال رابط إعادة تعيين كلمة المرور"}

@router.get("/auth/me")
async def get_me(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "غير مصادق")
    return {k: user.get(k) for k in ("id","email","name","avatar","provider","created_at","bio","cover_image")}

@router.post("/auth/logout")
async def logout():
    return {"message": "تم تسجيل الخروج"}

@router.delete("/auth/delete-account")
async def delete_account(user: dict = Depends(get_user)):
    """Delete user account and ALL associated data - required by App Store & Play Store policies.
    Complies with Apple App Store Review Guideline 5.1.1(v) and Google Play Data Safety requirements.
    """
    if not user:
        raise HTTPException(401, "غير مصادق")
    uid = user["id"]
    email = user.get("email", "")
    try:
        # ---- Social / Content Data ----
        await db.posts.delete_many({"author_id": uid})
        await db.stories.delete_many({"author_id": uid})
        await db.comments.delete_many({"author_id": uid})
        await db.likes.delete_many({"user_id": uid})
        await db.saves.delete_many({"user_id": uid})
        await db.follows.delete_many({"$or": [{"follower_id": uid}, {"following_id": uid}]})
        await db.reports.delete_many({"$or": [{"reporter_id": uid}, {"reported_user_id": uid}]})
        await db.embed_content.delete_many({"author_id": uid})

        # ---- Messaging & Notifications ----
        await db.notifications.delete_many({"$or": [{"user_id": uid}, {"from_user_id": uid}]})
        await db.messages.delete_many({"$or": [{"sender_id": uid}, {"receiver_id": uid}]})
        await db.push_subscriptions.delete_many({"user_id": uid})
        await db.notification_log.delete_many({"user_id": uid})
        await db.sent_notifications.delete_many({"user_id": uid})
        await db.scheduled_notifications.delete_many({"user_id": uid})

        # ---- Points / Economy / Wallet ----
        await db.points.delete_many({"user_id": uid})
        await db.points_transactions.delete_many({"user_id": uid})
        await db.adult_points.delete_many({"user_id": uid})
        await db.wallets.delete_many({"user_id": uid})
        await db.gold_transactions.delete_many({"user_id": uid})
        await db.gift_transactions.delete_many({"$or": [{"sender_id": uid}, {"receiver_id": uid}]})
        await db.baraka_wallets.delete_many({"user_id": uid})
        await db.baraka_transactions.delete_many({"user_id": uid})
        await db.purchases.delete_many({"user_id": uid})
        await db.memberships.delete_many({"user_id": uid})
        await db.redeemed_items.delete_many({"user_id": uid})
        await db.payment_transactions.delete_many({"user_id": uid})
        await db.unlocked_stories.delete_many({"user_id": uid})

        # ---- Prayer & Worship Tracking ----
        await db.prayer_tracking.delete_many({"user_id": uid})

        # ---- Kids Zone Data ----
        await db.kids_curriculum_progress.delete_many({"user_id": uid})
        await db.kids_journey.delete_many({"user_id": uid})
        await db.kids_learn_progress.delete_many({"user_id": uid})
        await db.kids_points.delete_many({"user_id": uid})
        await db.kids_skills.delete_many({"user_id": uid})
        await db.lesson_points_log.delete_many({"user_id": uid})
        await db.parental_consents.delete_many({"user_id": uid})
        await db.parental_passes.delete_many({"user_id": uid})

        # ---- Learning / Arabic Academy ----
        await db.arabic_progress.delete_many({"user_id": uid})
        await db.ai_questions.delete_many({"user_id": uid})

        # ---- Analytics & Tracking (GDPR compliance) ----
        await db.analytics_events.delete_many({"user_id": uid})
        await db.ad_clicks.delete_many({"user_id": uid})
        await db.ad_views.delete_many({"user_id": uid})
        await db.ad_watch_log.delete_many({"user_id": uid})
        await db.user_ads.delete_many({"user_id": uid})
        await db.user_data.delete_many({"user_id": uid})

        # ---- Donations & Banking ----
        await db.donations.delete_many({"user_id": uid})
        await db.donation_requests.delete_many({"user_id": uid})
        await db.bank_accounts.delete_many({"user_id": uid})

        # ---- Marketplace / Vendor ----
        await db.vendors.delete_many({"user_id": uid})
        await db.products.delete_many({"vendor_id": uid})

        # ---- Contact / Support ----
        await db.contact_messages.delete_many({"$or": [{"user_id": uid}, {"email": email}]})

        # ---- Blocks ----
        await db.blocks.delete_many({"$or": [{"blocker_id": uid}, {"blocked_id": uid}]})

        # ---- Finally delete user account ----
        await db.users.delete_one({"id": uid})

        logger.info(f"Account fully deleted (all data purged): {uid}")
        return {"success": True, "message": "تم حذف الحساب وجميع البيانات بنجاح"}
    except Exception as e:
        logger.error(f"Error deleting account {uid}: {e}")
        raise HTTPException(500, "حدث خطأ أثناء حذف الحساب")

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    cover_image: Optional[str] = None

@router.put("/auth/update-profile")
async def update_profile(req: UpdateProfileRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "غير مصادق")
    update = {}
    if req.name and req.name.strip():
        update["name"] = req.name.strip()
    if req.avatar:
        update["avatar"] = req.avatar
    if req.bio is not None:
        update["bio"] = req.bio.strip()[:500]
    if req.cover_image:
        update["cover_image"] = req.cover_image
    if req.password and len(req.password) >= 6:
        import hashlib
        update["password_hash"] = hashlib.sha256(req.password.encode()).hexdigest()
    if update:
        await db.users.update_one({"id": user["id"]}, {"$set": update})
    return {"success": True, "message": "تم تحديث الملف الشخصي"}

# ==================== SOCIAL PLATFORM (صُحبة) ====================

SOHBA_CATEGORIES = [
    {"key": "general", "label": "عام", "labelKey": "sohbaCatGeneral", "icon": "globe"},
    {"key": "quran", "label": "القرآن الكريم", "labelKey": "sohbaCatQuran", "icon": "book"},
    {"key": "hadith", "label": "الحديث الشريف", "labelKey": "sohbaCatHadith", "icon": "scroll"},
    {"key": "ramadan", "label": "رمضان", "labelKey": "sohbaCatRamadan", "icon": "moon"},
    {"key": "dua", "label": "الدعاء والأذكار", "labelKey": "sohbaCatDua", "icon": "hands"},
    {"key": "stories", "label": "قصص وعبر", "labelKey": "sohbaCatStories", "icon": "feather"},
    {"key": "hajj", "label": "الحج والعمرة", "labelKey": "sohbaCatHajj", "icon": "kaaba"},
    {"key": "halal", "label": "السفر الحلال", "labelKey": "sohbaCatHalal", "icon": "plane"},
    {"key": "family", "label": "الأسرة المسلمة", "labelKey": "sohbaCatFamily", "icon": "heart"},
    {"key": "youth", "label": "الشباب", "labelKey": "sohbaCatYouth", "icon": "users"},
]

class CreatePostRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    category: str = "general"
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    content_type: str = "text"  # text, image, video_short, video_long, lecture
    duration: Optional[int] = None  # video duration in seconds

class CreateCommentRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    reply_to: Optional[str] = None  # comment_id being replied to

class CreatePageRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = ""
    category: str = "general"
    avatar_url: Optional[str] = None

