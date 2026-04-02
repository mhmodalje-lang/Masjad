"""
Router: auth
"""
from fastapi import APIRouter, HTTPException, Depends
from deps import db, get_user, logger, create_jwt, hash_password, check_password
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from data.multilingual_content import SOHBA_CATEGORIES_TRANSLATED, get_error
import uuid
import httpx

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

SOHBA_CATEGORIES = SOHBA_CATEGORIES_TRANSLATED

@router.post("/auth/register")
async def register(data: UserRegister):
    email = data.email.lower().strip()
    if await db.users.find_one({"email": email}):
        raise HTTPException(400, get_error("email_already_registered"))
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
async def _cleanup_social_data(uid: str) -> None:
    """Delete all social/content data for a user."""
    await db.posts.delete_many({"author_id": uid})
    await db.stories.delete_many({"author_id": uid})
    await db.comments.delete_many({"author_id": uid})
    await db.likes.delete_many({"user_id": uid})
    await db.saves.delete_many({"user_id": uid})
    await db.follows.delete_many({"$or": [{"follower_id": uid}, {"following_id": uid}]})
    await db.reports.delete_many({"$or": [{"reporter_id": uid}, {"reported_user_id": uid}]})
    await db.embed_content.delete_many({"author_id": uid})


async def _cleanup_messaging_data(uid: str) -> None:
    """Delete all messaging/notification data for a user."""
    await db.notifications.delete_many({"$or": [{"user_id": uid}, {"from_user_id": uid}]})
    await db.messages.delete_many({"$or": [{"sender_id": uid}, {"receiver_id": uid}]})
    await db.push_subscriptions.delete_many({"user_id": uid})
    await db.notification_log.delete_many({"user_id": uid})
    await db.sent_notifications.delete_many({"user_id": uid})
    await db.scheduled_notifications.delete_many({"user_id": uid})


async def _cleanup_economy_data(uid: str) -> None:
    """Delete all economy/wallet data for a user."""
    for col_name in ["points", "points_transactions", "adult_points", "wallets",
                     "gold_transactions", "baraka_wallets", "baraka_transactions",
                     "purchases", "memberships", "redeemed_items", "payment_transactions",
                     "unlocked_stories"]:
        await db[col_name].delete_many({"user_id": uid})
    await db.gift_transactions.delete_many({"$or": [{"sender_id": uid}, {"receiver_id": uid}]})


async def _cleanup_kids_data(uid: str) -> None:
    """Delete all kids zone/learning data for a user."""
    for col_name in ["kids_curriculum_progress", "kids_journey", "kids_learn_progress",
                     "kids_points", "kids_skills", "lesson_points_log",
                     "parental_consents", "parental_passes", "arabic_progress", "ai_questions"]:
        await db[col_name].delete_many({"user_id": uid})


async def _cleanup_analytics_data(uid: str, email: str) -> None:
    """Delete all analytics/tracking/misc data for a user (GDPR compliance)."""
    for col_name in ["analytics_events", "ad_clicks", "ad_views", "ad_watch_log",
                     "user_ads", "user_data", "prayer_tracking", "donations",
                     "donation_requests", "bank_accounts"]:
        await db[col_name].delete_many({"user_id": uid})
    await db.vendors.delete_many({"user_id": uid})
    await db.products.delete_many({"vendor_id": uid})
    await db.contact_messages.delete_many({"$or": [{"user_id": uid}, {"email": email}]})
    await db.blocks.delete_many({"$or": [{"blocker_id": uid}, {"blocked_id": uid}]})


async def delete_account(user: dict = Depends(get_user)):
    """Delete user account and ALL associated data.
    Complies with Apple App Store Guideline 5.1.1(v) and Google Play Data Safety.
    """
    if not user:
        raise HTTPException(401, "غير مصادق")
    uid = user["id"]
    email = user.get("email", "")
    try:
        await _cleanup_social_data(uid)
        await _cleanup_messaging_data(uid)
        await _cleanup_economy_data(uid)
        await _cleanup_kids_data(uid)
        await _cleanup_analytics_data(uid, email)
        await db.users.delete_one({"id": uid})
        logger.info(f"Account fully deleted (all data purged): {uid}")
        return {"success": True, "message": "تم حذف الحساب وجميع البيانات بنجاح"}
    except Exception as e:
        logger.error(f"Error deleting account {uid}: {e}")
        raise HTTPException(500, "حدث خطأ أثناء حذف الحساب")

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

