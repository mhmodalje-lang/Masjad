"""
أذان وحكاية - Backend API
Full Islamic App with Prayer Times, Notifications, AI Athkar, Mosque Search
"""
from fastapi import FastAPI, APIRouter, HTTPException, Query, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import httpx
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, date, timedelta
import asyncio
import math
import random
import hashlib
import hmac as hmac_lib
import base64
import json as json_module
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# ==================== CONFIG ====================
JWT_SECRET = os.environ.get('JWT_SECRET', 'almuadhin-global-secret-2026')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', 'hxhdh-78bec')
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY', '')
VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY', '')
VAPID_EMAIL = os.environ.get('VAPID_EMAIL', 'mailto:mohammadalrejab@gmail.com')
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY', '')
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'almuadhin')

# MongoDB
client_db = AsyncIOMotorClient(MONGO_URL)
db = client_db[DB_NAME]

# App
app = FastAPI(title="أذان وحكاية API", version="2.0")
api_router = APIRouter(prefix="/api")
security = HTTPBearer(auto_error=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== JWT ====================
def _b64enc(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def _b64dec(s: str) -> bytes:
    s += '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

def create_jwt(payload: dict, hours: int = 720) -> str:
    header = _b64enc(json_module.dumps({"alg":"HS256","typ":"JWT"}).encode())
    exp = datetime.utcnow() + timedelta(hours=hours)
    pl = {**payload, "exp": exp.isoformat(), "iat": datetime.utcnow().isoformat()}
    pl_enc = _b64enc(json_module.dumps(pl).encode())
    sig = hmac_lib.new(JWT_SECRET.encode(), f"{header}.{pl_enc}".encode(), hashlib.sha256).digest()
    return f"{header}.{pl_enc}.{_b64enc(sig)}"

def verify_jwt(token: str) -> Optional[dict]:
    try:
        h, p, s = token.split('.')
        expected = hmac_lib.new(JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
        if not hmac_lib.compare_digest(expected, _b64dec(s)):
            return None
        payload = json_module.loads(_b64dec(p))
        if datetime.utcnow() > datetime.fromisoformat(payload["exp"]):
            return None
        return payload
    except Exception:
        return None

def hash_password(pw: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', pw.encode(), salt, 100000)
    return f"{base64.b64encode(salt).decode()}:{base64.b64encode(dk).decode()}"

def check_password(pw: str, hashed: str) -> bool:
    try:
        s, dk = hashed.split(':')
        return hmac_lib.compare_digest(
            hashlib.pbkdf2_hmac('sha256', pw.encode(), base64.b64decode(s), 100000),
            base64.b64decode(dk)
        )
    except Exception:
        return False

async def get_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> Optional[dict]:
    if not creds:
        return None
    payload = verify_jwt(creds.credentials)
    if not payload:
        return None
    return await db.users.find_one({"id": payload.get("user_id")})

# ==================== MODELS ====================
class UserRegister(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class PushSubscription(BaseModel):
    endpoint: str
    p256dh: str
    auth: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    method: Optional[int] = 3
    school: Optional[int] = 0
    timezone: Optional[str] = "Asia/Riyadh"
    user_id: Optional[str] = None

class MosqueTimesRequest(BaseModel):
    mosqueName: str
    latitude: float
    longitude: float
    method: int = 3
    school: int = 0
    mosqueUuid: Optional[str] = None

class DhikrAIRequest(BaseModel):
    time_of_day: str = "morning"
    occasion: Optional[str] = None
    language: str = "ar"
    count: int = 5

# ==================== UTILS ====================
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

async def query_overpass(q: str) -> Optional[dict]:
    for ep in OVERPASS_ENDPOINTS:
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post(ep, content=q, headers={"Content-Type":"text/plain"})
                if r.status_code == 200:
                    return r.json()
        except Exception:
            continue
    return None

def clean_time(t: str) -> str:
    return re.sub(r'\s*\(.*?\)', '', t).strip()

# ==================== STATUS ====================
@api_router.get("/")
async def root():
    return {"message": "أذان وحكاية API", "version": "2.0", "status": "running"}

@api_router.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat(), "app": "أذان وحكاية"}

# ==================== AUTH ====================
@api_router.post("/auth/register")
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

@api_router.post("/auth/login")
async def login(data: UserLogin):
    email = data.email.lower().strip()
    user = await db.users.find_one({"email": email})
    if not user or not check_password(data.password, user.get("password_hash", "")):
        raise HTTPException(401, "بيانات الدخول غير صحيحة")
    token = create_jwt({"user_id": user["id"], "email": email})
    return {"access_token": token, "token_type": "bearer", "user": {k: user[k] for k in ("id","email","name","avatar","provider") if k in user}}

@api_router.post("/auth/google")
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

@api_router.post("/auth/forgot-password")
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

@api_router.get("/auth/me")
async def get_me(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "غير مصادق")
    return {k: user.get(k) for k in ("id","email","name","avatar","provider","created_at","bio","cover_image")}

@api_router.post("/auth/logout")
async def logout():
    return {"message": "تم تسجيل الخروج"}

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    cover_image: Optional[str] = None

@api_router.put("/auth/update-profile")
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

@api_router.get("/sohba/categories")
async def get_categories():
    return {"categories": SOHBA_CATEGORIES}

@api_router.get("/sohba/posts")
async def get_posts(category: str = "all", page: int = 1, limit: int = 20, author: str = "", user: dict = Depends(get_user)):
    query = {}
    if category != "all":
        query["category"] = category
    if author:
        query["author_id"] = author
    skip = (page - 1) * limit
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    total = await db.posts.count_documents(query)

    # Bulk fetch likes/saves/counts to avoid N+1 queries
    post_ids = [p["id"] for p in posts]
    user_id = user["id"] if user else None

    likes_set = set()
    saves_set = set()
    if user_id and post_ids:
        user_likes = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        likes_set = {d["post_id"] for d in user_likes}
        user_saves = await db.saves.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        saves_set = {d["post_id"] for d in user_saves}

    # Bulk count likes and comments via aggregation
    likes_counts = {}
    comments_counts = {}
    if post_ids:
        lc = db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
        async for doc in lc:
            likes_counts[doc["_id"]] = doc["c"]
        cc = db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
        async for doc in cc:
            comments_counts[doc["_id"]] = doc["c"]

    for post in posts:
        pid = post["id"]
        post["liked"] = pid in likes_set
        post["saved"] = pid in saves_set
        post["likes_count"] = likes_counts.get(pid, 0)
        post["comments_count"] = comments_counts.get(pid, 0)

    return {"posts": posts, "total": total, "page": page, "has_more": skip + limit < total}

@api_router.post("/sohba/posts")
async def create_post(data: CreatePostRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول للنشر")
    
    post_id = str(uuid.uuid4())
    post = {
        "id": post_id,
        "author_id": user["id"],
        "author_name": user.get("name", "مستخدم"),
        "author_avatar": user.get("avatar"),
        "content": data.content,
        "category": data.category,
        "image_url": data.image_url,
        "video_url": data.video_url,
        "thumbnail_url": data.thumbnail_url,
        "content_type": data.content_type,
        "duration": data.duration,
        "created_at": datetime.utcnow().isoformat(),
        "shares_count": 0,
    }
    await db.posts.insert_one(post)
    post.pop("_id", None)
    post["liked"] = False
    post["saved"] = False
    post["likes_count"] = 0
    post["comments_count"] = 0
    return {"post": post}

@api_router.post("/sohba/posts/{post_id}/like")
async def toggle_like(post_id: str, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    existing = await db.likes.find_one({"post_id": post_id, "user_id": user["id"]})
    if existing:
        await db.likes.delete_one({"post_id": post_id, "user_id": user["id"]})
        return {"liked": False}
    else:
        await db.likes.insert_one({"post_id": post_id, "user_id": user["id"], "created_at": datetime.utcnow().isoformat()})
        return {"liked": True}

@api_router.post("/sohba/posts/{post_id}/save")
async def toggle_save(post_id: str, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    existing = await db.saves.find_one({"post_id": post_id, "user_id": user["id"]})
    if existing:
        await db.saves.delete_one({"post_id": post_id, "user_id": user["id"]})
        return {"saved": False}
    else:
        await db.saves.insert_one({"post_id": post_id, "user_id": user["id"], "created_at": datetime.utcnow().isoformat()})
        return {"saved": True}

@api_router.get("/sohba/posts/{post_id}/comments")
async def get_comments(post_id: str, page: int = 1, limit: int = 50):
    skip = (page - 1) * limit
    cursor = db.comments.find({"post_id": post_id}, {"_id": 0}).sort("created_at", 1).skip(skip).limit(limit)
    comments = await cursor.to_list(length=limit)
    return {"comments": comments}

@api_router.post("/sohba/posts/{post_id}/comments")
async def create_comment(post_id: str, data: CreateCommentRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول للتعليق")
    comment = {
        "id": str(uuid.uuid4()),
        "post_id": post_id,
        "author_id": user["id"],
        "author_name": user.get("name", "مستخدم"),
        "author_avatar": user.get("avatar"),
        "content": data.content,
        "reply_to": data.dict().get("reply_to"),
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.comments.insert_one(comment)
    comment.pop("_id", None)
    return {"comment": comment}

@api_router.delete("/sohba/comments/{comment_id}")
async def delete_comment(comment_id: str, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    comment = await db.comments.find_one({"id": comment_id})
    if not comment:
        raise HTTPException(404, "التعليق غير موجود")
    is_admin = user.get("email") in ["mohammadalrejab@gmail.com"]
    if comment["author_id"] != user["id"] and not is_admin:
        raise HTTPException(403, "غير مصرح بالحذف")
    await db.comments.delete_one({"id": comment_id})
    return {"deleted": True}

# ==================== ADMIN SOCIAL MANAGEMENT ====================
@api_router.get("/admin/social/posts")
async def admin_list_posts(page: int = 1, limit: int = 30, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    skip = (page - 1) * limit
    cursor = db.posts.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    total = await db.posts.count_documents({})
    return {"posts": posts, "total": total}

@api_router.delete("/admin/social/posts/{post_id}")
async def admin_delete_post(post_id: str, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    await db.posts.delete_one({"id": post_id})
    await db.likes.delete_many({"post_id": post_id})
    await db.comments.delete_many({"post_id": post_id})
    await db.saves.delete_many({"post_id": post_id})
    return {"deleted": True}

@api_router.get("/admin/social/comments")
async def admin_list_comments(page: int = 1, limit: int = 50, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    skip = (page - 1) * limit
    cursor = db.comments.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    comments = await cursor.to_list(length=limit)
    total = await db.comments.count_documents({})
    return {"comments": comments, "total": total}

@api_router.delete("/admin/social/comments/{comment_id}")
async def admin_delete_comment(comment_id: str, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    await db.comments.delete_one({"id": comment_id})
    return {"deleted": True}

@api_router.get("/admin/social/users")
async def admin_list_users(page: int = 1, limit: int = 50, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    skip = (page - 1) * limit
    cursor = db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    total = await db.users.count_documents({})
    for u in users:
        u["posts_count"] = await db.posts.count_documents({"author_id": u["id"]})
        u["followers_count"] = await db.follows.count_documents({"following_id": u["id"]})
    return {"users": users, "total": total}

@api_router.get("/admin/social/stats")
async def admin_social_stats(user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    return {
        "total_posts": await db.posts.count_documents({}),
        "total_users": await db.users.count_documents({}),
        "total_comments": await db.comments.count_documents({}),
        "total_likes": await db.likes.count_documents({}),
        "total_follows": await db.follows.count_documents({}),
    }

@api_router.delete("/sohba/posts/{post_id}")
async def delete_post(post_id: str, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    post = await db.posts.find_one({"id": post_id})
    if not post:
        raise HTTPException(404, "المنشور غير موجود")
    is_admin = user.get("email") in ["mohammadalrejab@gmail.com"]
    if post["author_id"] != user["id"] and not is_admin:
        raise HTTPException(403, "غير مصرح بالحذف")
    await db.posts.delete_one({"id": post_id})
    await db.likes.delete_many({"post_id": post_id})
    await db.comments.delete_many({"post_id": post_id})
    await db.saves.delete_many({"post_id": post_id})
    return {"deleted": True}

# ==================== FOLLOW SYSTEM ====================
@api_router.post("/sohba/follow/{target_id}")
async def toggle_follow(target_id: str, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    if target_id == user["id"]:
        raise HTTPException(400, "لا يمكنك متابعة نفسك")
    existing = await db.follows.find_one({"follower_id": user["id"], "following_id": target_id})
    if existing:
        await db.follows.delete_one({"follower_id": user["id"], "following_id": target_id})
        return {"following": False}
    else:
        await db.follows.insert_one({"follower_id": user["id"], "following_id": target_id, "created_at": datetime.utcnow().isoformat()})
        return {"following": True}

@api_router.get("/sohba/profile/{user_id}")
async def get_profile(user_id: str, user: dict = Depends(get_user)):
    profile = await db.users.find_one({"id": user_id}, {"_id": 0, "password_hash": 0})
    if not profile:
        raise HTTPException(404, "المستخدم غير موجود")
    
    # Count total likes received on user's posts
    user_post_ids = []
    async for p in db.posts.find({"author_id": user_id}, {"id": 1, "_id": 0}):
        user_post_ids.append(p["id"])
    total_likes = 0
    if user_post_ids:
        total_likes = await db.likes.count_documents({"post_id": {"$in": user_post_ids}})
    
    # Count gifts received
    gifts_received = await db.gift_transactions.count_documents({"recipient_id": user_id}) if hasattr(db, 'gift_transactions') else 0
    try:
        gifts_received = await db.gift_transactions.count_documents({"recipient_id": user_id})
    except Exception:
        gifts_received = 0
    
    stats = {
        "posts_count": await db.posts.count_documents({"author_id": user_id}),
        "followers_count": await db.follows.count_documents({"following_id": user_id}),
        "following_count": await db.follows.count_documents({"follower_id": user_id}),
        "likes_count": total_likes,
        "gifts_count": gifts_received,
    }
    is_following = False
    if user and user["id"] != user_id:
        is_following = bool(await db.follows.find_one({"follower_id": user["id"], "following_id": user_id}))
    return {
        "profile": {k: profile.get(k) for k in ("id", "email", "name", "avatar", "bio", "cover_image", "created_at")},
        "stats": stats,
        "is_following": is_following
    }

@api_router.get("/sohba/my-stats")
async def get_my_stats(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    uid = user["id"]
    # Count total likes received on user's posts
    user_post_ids = []
    async for p in db.posts.find({"author_id": uid}, {"id": 1, "_id": 0}):
        user_post_ids.append(p["id"])
    total_likes = 0
    if user_post_ids:
        total_likes = await db.likes.count_documents({"post_id": {"$in": user_post_ids}})
    return {
        "posts": await db.posts.count_documents({"author_id": uid}),
        "stories": await db.posts.count_documents({"author_id": uid, "is_story": True}),
        "followers": await db.follows.count_documents({"following_id": uid}),
        "following": await db.follows.count_documents({"follower_id": uid}),
        "total_likes": total_likes,
        "saved_count": await db.saves.count_documents({"user_id": uid}),
        "liked_count": await db.likes.count_documents({"user_id": uid}),
    }

# ==================== RECOMMENDED USERS ====================
@api_router.get("/sohba/recommended-users")
async def recommended_users(limit: int = 10, user: dict = Depends(get_user)):
    """Get recommended users for new users or discovery"""
    user_id = user["id"] if user else None
    
    # Get IDs of users already followed
    followed_ids = set()
    if user_id:
        followed_ids.add(user_id)
        async for f in db.follows.find({"follower_id": user_id}, {"following_id": 1, "_id": 0}):
            followed_ids.add(f["following_id"])
    
    # Get users with most content/engagement, exclude already followed
    pipeline = [
        {"$match": {"id": {"$nin": list(followed_ids)}}} if followed_ids else {"$match": {}},
        {"$project": {"_id": 0, "password_hash": 0}},
        {"$limit": limit * 3}
    ]
    
    candidates = []
    async for u in db.users.aggregate(pipeline):
        uid = u["id"]
        followers = await db.follows.count_documents({"following_id": uid})
        posts_count = await db.posts.count_documents({"author_id": uid})
        candidates.append({
            "id": uid,
            "name": u.get("name", "مستخدم"),
            "avatar": u.get("avatar"),
            "bio": u.get("bio", ""),
            "followers_count": followers,
            "posts_count": posts_count,
            "score": followers * 2 + posts_count,
        })
    
    # Sort by score and return top N
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return {"users": candidates[:limit]}

@api_router.get("/sohba/feed/following")
async def following_feed(page: int = 1, limit: int = 20, user: dict = Depends(get_user)):
    """Get feed from followed users only"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    # Get followed user IDs
    followed_ids = []
    async for f in db.follows.find({"follower_id": user["id"]}, {"following_id": 1, "_id": 0}):
        followed_ids.append(f["following_id"])
    
    if not followed_ids:
        return {"posts": [], "total": 0, "page": page, "has_more": False}
    
    skip = (page - 1) * limit
    query = {"author_id": {"$in": followed_ids}}
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    total = await db.posts.count_documents(query)
    
    # Enrich posts
    post_ids = [p["id"] for p in posts]
    user_id = user["id"]
    likes_set = set()
    saves_set = set()
    if post_ids:
        user_likes = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        likes_set = {d["post_id"] for d in user_likes}
        user_saves = await db.saves.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        saves_set = {d["post_id"] for d in user_saves}
    
    likes_counts = {}
    comments_counts = {}
    if post_ids:
        lc = db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
        async for doc in lc:
            likes_counts[doc["_id"]] = doc["c"]
        cc = db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
        async for doc in cc:
            comments_counts[doc["_id"]] = doc["c"]
    
    for post in posts:
        pid = post["id"]
        post["liked"] = pid in likes_set
        post["saved"] = pid in saves_set
        post["likes_count"] = likes_counts.get(pid, 0)
        post["comments_count"] = comments_counts.get(pid, 0)
    
    return {"posts": posts, "total": total, "page": page, "has_more": skip + limit < total}

@api_router.get("/sohba/feed/videos")
async def video_feed(content_type: str = "all", page: int = 1, limit: int = 20, user: dict = Depends(get_user)):
    """Get video content feed (reels, lectures, long videos)"""
    skip = (page - 1) * limit
    
    if content_type == "all":
        query = {"content_type": {"$in": ["video_short", "video_long", "lecture"]}}
    else:
        query = {"content_type": content_type}
    
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    total = await db.posts.count_documents(query)
    
    # Enrich
    user_id = user["id"] if user else None
    post_ids = [p["id"] for p in posts]
    likes_set = set()
    if user_id and post_ids:
        user_likes = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        likes_set = {d["post_id"] for d in user_likes}
    
    likes_counts = {}
    comments_counts = {}
    if post_ids:
        lc = db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
        async for doc in lc:
            likes_counts[doc["_id"]] = doc["c"]
        cc = db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
        async for doc in cc:
            comments_counts[doc["_id"]] = doc["c"]
    
    for post in posts:
        pid = post["id"]
        post["liked"] = pid in likes_set
        post["likes_count"] = likes_counts.get(pid, 0)
        post["comments_count"] = comments_counts.get(pid, 0)
    
    return {"posts": posts, "total": total, "page": page, "has_more": skip + limit < total}

@api_router.post("/sohba/posts/{post_id}/share")
async def share_post(post_id: str, user: dict = Depends(get_user)):
    """Increment share count for a post"""
    result = await db.posts.update_one({"id": post_id}, {"$inc": {"shares_count": 1}})
    if result.modified_count == 0:
        raise HTTPException(404, "المنشور غير موجود")
    return {"shared": True}

@api_router.get("/sohba/user/{user_id}/posts")
async def get_user_posts(user_id: str, page: int = 1, limit: int = 20, content_type: str = "all", user: dict = Depends(get_user)):
    """Get posts by specific user"""
    skip = (page - 1) * limit
    query = {"author_id": user_id}
    if content_type != "all":
        query["content_type"] = content_type
    
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    total = await db.posts.count_documents(query)
    
    # Enrich
    current_user_id = user["id"] if user else None
    post_ids = [p["id"] for p in posts]
    likes_set = set()
    if current_user_id and post_ids:
        user_likes = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": current_user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        likes_set = {d["post_id"] for d in user_likes}
    
    likes_counts = {}
    comments_counts = {}
    if post_ids:
        lc = db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
        async for doc in lc:
            likes_counts[doc["_id"]] = doc["c"]
        cc = db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
        async for doc in cc:
            comments_counts[doc["_id"]] = doc["c"]
    
    for post in posts:
        pid = post["id"]
        post["liked"] = pid in likes_set
        post["likes_count"] = likes_counts.get(pid, 0)
        post["comments_count"] = comments_counts.get(pid, 0)
    
    return {"posts": posts, "total": total, "page": page, "has_more": skip + limit < total}

# ==================== PAGES SYSTEM ====================
@api_router.post("/sohba/pages")
async def create_page(data: CreatePageRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    page_id = str(uuid.uuid4())
    page = {
        "id": page_id,
        "owner_id": user["id"],
        "name": data.name,
        "description": data.description,
        "category": data.category,
        "avatar_url": data.avatar_url,
        "followers_count": 0,
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.pages.insert_one(page)
    page.pop("_id", None)
    return {"page": page}

@api_router.get("/sohba/pages")
async def list_pages(category: str = "all", page: int = 1, limit: int = 20):
    query = {} if category == "all" else {"category": category}
    skip = (page - 1) * limit
    cursor = db.pages.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    pages = await cursor.to_list(length=limit)
    return {"pages": pages}

# ==================== SEARCH & EXPLORE ====================

@api_router.get("/sohba/search")
async def search_sohba(q: str = Query("", min_length=1), type: str = "all", page: int = 1, limit: int = 30, user: dict = Depends(get_user)):
    """Search posts, users, and hashtags"""
    results = {"posts": [], "users": [], "hashtags": [], "total": 0}
    skip = (page - 1) * limit
    
    if not q.strip():
        return results
    
    search_regex = {"$regex": q.strip(), "$options": "i"}
    
    # Search posts
    if type in ("all", "posts"):
        post_query = {"$or": [
            {"content": search_regex},
            {"author_name": search_regex},
            {"category": search_regex},
        ]}
        post_cursor = db.posts.find(post_query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
        posts = await post_cursor.to_list(length=limit)
        
        # Enrich posts with like/save status
        post_ids = [p["id"] for p in posts]
        user_id = user["id"] if user else None
        likes_set = set()
        saves_set = set()
        if user_id and post_ids:
            user_likes = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
            likes_set = {d["post_id"] for d in user_likes}
            user_saves = await db.saves.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
            saves_set = {d["post_id"] for d in user_saves}
        
        likes_counts = {}
        comments_counts = {}
        if post_ids:
            lc = db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
            async for doc in lc:
                likes_counts[doc["_id"]] = doc["c"]
            cc = db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}])
            async for doc in cc:
                comments_counts[doc["_id"]] = doc["c"]
        
        for post in posts:
            pid = post["id"]
            post["liked"] = pid in likes_set
            post["saved"] = pid in saves_set
            post["likes_count"] = likes_counts.get(pid, 0)
            post["comments_count"] = comments_counts.get(pid, 0)
        
        results["posts"] = posts
    
    # Search users
    if type in ("all", "users"):
        user_query = {"$or": [
            {"name": search_regex},
            {"email": search_regex},
        ]}
        user_cursor = db.users.find(user_query, {"_id": 0, "password_hash": 0}).skip(skip).limit(limit)
        users_list = await user_cursor.to_list(length=limit)
        
        # Get follower counts for each user
        for u in users_list:
            u["followers_count"] = await db.follows.count_documents({"following_id": u["id"]})
            u["posts_count"] = await db.posts.count_documents({"author_id": u["id"]})
        
        results["users"] = [{k: u.get(k) for k in ("id", "name", "email", "avatar", "followers_count", "posts_count")} for u in users_list]
    
    results["total"] = len(results["posts"]) + len(results["users"])
    return results

@api_router.get("/sohba/explore")
async def explore_feed(page: int = 1, limit: int = 30, user: dict = Depends(get_user)):
    """Get trending/explore posts sorted by engagement"""
    skip = (page - 1) * limit
    
    # Get all posts with engagement data
    pipeline = [
        {"$lookup": {"from": "likes", "localField": "id", "foreignField": "post_id", "as": "likes_data"}},
        {"$lookup": {"from": "comments", "localField": "id", "foreignField": "post_id", "as": "comments_data"}},
        {"$addFields": {
            "likes_count": {"$size": "$likes_data"},
            "comments_count": {"$size": "$comments_data"},
            "engagement_score": {"$add": [{"$multiply": [{"$size": "$likes_data"}, 2]}, {"$size": "$comments_data"}]}
        }},
        {"$project": {"_id": 0, "likes_data": 0, "comments_data": 0}},
        {"$sort": {"engagement_score": -1, "created_at": -1}},
        {"$skip": skip},
        {"$limit": limit}
    ]
    
    posts = []
    async for doc in db.posts.aggregate(pipeline):
        posts.append(doc)
    
    # Enrich with user-specific data
    user_id = user["id"] if user else None
    if user_id:
        post_ids = [p["id"] for p in posts]
        if post_ids:
            user_likes = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
            likes_set = {d["post_id"] for d in user_likes}
            user_saves = await db.saves.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
            saves_set = {d["post_id"] for d in user_saves}
            for post in posts:
                post["liked"] = post["id"] in likes_set
                post["saved"] = post["id"] in saves_set
    else:
        for post in posts:
            post["liked"] = False
            post["saved"] = False
    
    total = await db.posts.count_documents({})
    return {"posts": posts, "total": total, "page": page, "has_more": skip + limit < total}

@api_router.get("/sohba/trending-users")
async def trending_users(limit: int = 20, user: dict = Depends(get_user)):
    """Get users with most followers"""
    pipeline = [
        {"$group": {"_id": "$following_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    trending = []
    async for doc in db.follows.aggregate(pipeline):
        u = await db.users.find_one({"id": doc["_id"]}, {"_id": 0, "password_hash": 0})
        if u:
            trending.append({
                "id": u["id"],
                "name": u.get("name", "مستخدم"),
                "avatar": u.get("avatar"),
                "followers_count": doc["count"],
                "posts_count": await db.posts.count_documents({"author_id": u["id"]}),
            })
    return {"users": trending}

# ==================== IMAGE UPLOAD ====================
UPLOAD_DIR = Path("/app/backend/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class UploadResponse(BaseModel):
    url: str
    filename: str

@api_router.post("/upload/image")
async def upload_image(user: dict = Depends(get_user)):
    """Redirect to /upload/file"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    return {"url": "", "message": "استخدم /api/upload/file"}

@api_router.post("/upload/file")
async def upload_file_base64(data: dict, user: dict = Depends(get_user)):
    """Upload file as base64. No size limit - uses chunked writing."""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    b64_data = data.get("data", "")
    original_filename = data.get("filename", "upload.jpg")
    
    if not b64_data:
        raise HTTPException(400, "لا توجد بيانات للرفع")
    
    # Remove data URL prefix if present
    if "," in b64_data:
        b64_data = b64_data.split(",", 1)[1]
    
    try:
        file_bytes = base64.b64decode(b64_data)
    except Exception:
        raise HTTPException(400, "بيانات غير صالحة")
    
    ext = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "jpg"
    safe_ext = ext.lower()[:5]
    unique_name = f"{uuid.uuid4().hex[:12]}.{safe_ext}"
    
    filepath = UPLOAD_DIR / unique_name
    filepath.write_bytes(file_bytes)
    
    file_url = f"/api/uploads/{unique_name}"
    return {"url": file_url, "filename": unique_name}

from fastapi import UploadFile, File as FastAPIFile

@api_router.post("/upload/multipart")
async def upload_multipart(file: UploadFile = FastAPIFile(...)):
    """Upload file via multipart form - unlimited size, streaming write."""
    ext = file.filename.rsplit(".", 1)[-1] if file.filename and "." in file.filename else "bin"
    safe_ext = ext.lower()[:5]
    unique_name = f"{uuid.uuid4().hex[:12]}.{safe_ext}"
    filepath = UPLOAD_DIR / unique_name
    
    # Stream write in chunks (no memory limit)
    with open(filepath, "wb") as f:
        while True:
            chunk = await file.read(1024 * 1024)  # 1MB chunks
            if not chunk:
                break
            f.write(chunk)
    
    file_url = f"/api/uploads/{unique_name}"
    return {"url": file_url, "filename": unique_name, "size": filepath.stat().st_size}

from fastapi.responses import FileResponse

@api_router.get("/uploads/{filename}")
async def serve_upload(filename: str):
    """Serve uploaded files"""
    filepath = UPLOAD_DIR / filename
    if not filepath.exists():
        raise HTTPException(404, "الملف غير موجود")
    content_types = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "gif": "image/gif", "webp": "image/webp", "mp4": "video/mp4", "webm": "video/webm"}
    ext = filename.rsplit(".", 1)[-1].lower()
    return FileResponse(str(filepath), media_type=content_types.get(ext, "application/octet-stream"))

# ==================== REWARDS & GOLD SYSTEM ====================
class ClaimRewardRequest(BaseModel):
    reward_type: str  # "daily_login", "post_created", "tasbeeh_100", "quran_page"

REWARD_VALUES = {
    "daily_login": 10,
    "post_created": 5,
    "tasbeeh_100": 3,
    "quran_page": 5,
    "comment_added": 2,
    "like_given": 1,
    "streak_bonus": 15,
}

@api_router.get("/rewards/balance")
async def get_gold_balance(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    wallet = await db.wallets.find_one({"user_id": user["id"]}, {"_id": 0})
    if not wallet:
        wallet = {"user_id": user["id"], "gold": 0, "total_earned": 0, "streak": 0, "last_daily": None}
        await db.wallets.insert_one(wallet)
        wallet.pop("_id", None)
    return {"gold": wallet.get("gold", 0), "total_earned": wallet.get("total_earned", 0), "streak": wallet.get("streak", 0)}

@api_router.post("/rewards/claim")
async def claim_reward(data: ClaimRewardRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    reward_type = data.reward_type
    gold_amount = REWARD_VALUES.get(reward_type, 0)
    if gold_amount == 0:
        raise HTTPException(400, "نوع المكافأة غير صالح")
    
    wallet = await db.wallets.find_one({"user_id": user["id"]})
    if not wallet:
        wallet = {"user_id": user["id"], "gold": 0, "total_earned": 0, "streak": 0, "last_daily": None}
        await db.wallets.insert_one(wallet)
    
    today = date.today().isoformat()
    
    # Check daily login (once per day)
    if reward_type == "daily_login":
        if wallet.get("last_daily") == today:
            return {"gold": wallet.get("gold", 0), "earned": 0, "message": "تم استلام مكافأة اليوم مسبقاً"}
        
        # Calculate streak
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        streak = wallet.get("streak", 0)
        if wallet.get("last_daily") == yesterday:
            streak += 1
        else:
            streak = 1
        
        # Streak bonus every 7 days
        bonus = REWARD_VALUES["streak_bonus"] if streak > 0 and streak % 7 == 0 else 0
        total_earn = gold_amount + bonus
        
        await db.wallets.update_one(
            {"user_id": user["id"]},
            {"$inc": {"gold": total_earn, "total_earned": total_earn}, "$set": {"last_daily": today, "streak": streak}}
        )
        
        # Log transaction
        await db.gold_transactions.insert_one({
            "user_id": user["id"], "type": reward_type, "amount": total_earn,
            "created_at": datetime.utcnow().isoformat(), "description": f"مكافأة يومية (سلسلة {streak} يوم)"
        })
        
        new_gold = wallet.get("gold", 0) + total_earn
        return {"gold": new_gold, "earned": total_earn, "streak": streak, "message": f"حصلت على {total_earn} ذهب!" + (f" (مكافأة سلسلة {streak} يوم!)" if bonus else "")}
    
    # Other rewards (max 5 per type per day)
    today_claims = await db.gold_transactions.count_documents({"user_id": user["id"], "type": reward_type, "created_at": {"$regex": f"^{today}"}})
    if today_claims >= 5:
        return {"gold": wallet.get("gold", 0), "earned": 0, "message": "وصلت للحد الأقصى اليوم"}
    
    await db.wallets.update_one(
        {"user_id": user["id"]},
        {"$inc": {"gold": gold_amount, "total_earned": gold_amount}},
        upsert=True
    )
    await db.gold_transactions.insert_one({
        "user_id": user["id"], "type": reward_type, "amount": gold_amount,
        "created_at": datetime.utcnow().isoformat()
    })
    
    new_gold = wallet.get("gold", 0) + gold_amount
    return {"gold": new_gold, "earned": gold_amount, "message": f"حصلت على {gold_amount} ذهب!"}

@api_router.get("/rewards/history")
async def get_reward_history(user: dict = Depends(get_user), page: int = 1, limit: int = 20):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    skip = (page - 1) * limit
    cursor = db.gold_transactions.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    transactions = await cursor.to_list(length=limit)
    return {"transactions": transactions}

@api_router.get("/rewards/leaderboard")
async def get_rewards_leaderboard(limit: int = 20):
    """Get top users by gold balance"""
    pipeline = [
        {"$project": {"_id": 0, "id": 1, "name": 1, "avatar": 1, "gold_balance": 1}},
        {"$sort": {"gold_balance": -1}},
        {"$limit": limit}
    ]
    users = await db.users.aggregate(pipeline).to_list(length=limit)
    leaderboard = []
    for i, u in enumerate(users):
        leaderboard.append({
            "rank": i + 1,
            "name": u.get("name", "مستخدم"),
            "avatar": u.get("avatar"),
            "gold_balance": u.get("gold_balance", 0)
        })
    return {"leaderboard": leaderboard}

@api_router.get("/asma-al-husna")
async def get_asma_al_husna():
    """Get the 99 Names of Allah"""
    names = [
        {"num": 1, "ar": "الرَّحْمَنُ", "meaning": "الذي وسعت رحمته كل شيء"},
        {"num": 2, "ar": "الرَّحِيمُ", "meaning": "الذي يرحم عباده المؤمنين"},
        {"num": 3, "ar": "المَلِكُ", "meaning": "المالك لكل شيء، المتصرف في خلقه"},
        {"num": 4, "ar": "القُدُّوسُ", "meaning": "المنزه عن كل عيب ونقص"},
        {"num": 5, "ar": "السَّلَامُ", "meaning": "السالم من كل عيب وآفة"},
        {"num": 6, "ar": "المُؤْمِنُ", "meaning": "الذي يُصَدِّق عباده ويؤمنهم من عذابه"},
        {"num": 7, "ar": "المُهَيْمِنُ", "meaning": "الشاهد على خلقه، المسيطر عليهم"},
        {"num": 8, "ar": "العَزِيزُ", "meaning": "الغالب الذي لا يُغلب"},
        {"num": 9, "ar": "الجَبَّارُ", "meaning": "الذي يجبر كسر عباده ويُصلح أحوالهم"},
        {"num": 10, "ar": "المُتَكَبِّرُ", "meaning": "المتعالي عن صفات الخلق"},
        {"num": 11, "ar": "الخَالِقُ", "meaning": "الذي أوجد الأشياء من العدم"},
        {"num": 12, "ar": "البَارِئُ", "meaning": "الذي خلق الخلق لا على مثال سابق"},
        {"num": 13, "ar": "المُصَوِّرُ", "meaning": "الذي صوّر جميع المخلوقات"},
        {"num": 14, "ar": "الغَفَّارُ", "meaning": "الذي يغفر الذنوب مرة بعد مرة"},
        {"num": 15, "ar": "القَهَّارُ", "meaning": "الذي قهر جميع المخلوقات"},
        {"num": 16, "ar": "الوَهَّابُ", "meaning": "الذي يهب النعم بلا عوض"},
        {"num": 17, "ar": "الرَّزَّاقُ", "meaning": "الذي يرزق جميع المخلوقات"},
        {"num": 18, "ar": "الفَتَّاحُ", "meaning": "الذي يفتح أبواب الرزق والرحمة"},
        {"num": 19, "ar": "العَلِيمُ", "meaning": "الذي يعلم كل شيء ظاهره وباطنه"},
        {"num": 20, "ar": "القَابِضُ", "meaning": "الذي يقبض الأرزاق والأرواح"},
        {"num": 21, "ar": "البَاسِطُ", "meaning": "الذي يبسط الرزق لمن يشاء"},
        {"num": 22, "ar": "الخَافِضُ", "meaning": "الذي يخفض من يشاء"},
        {"num": 23, "ar": "الرَّافِعُ", "meaning": "الذي يرفع من يشاء بالعز والطاعة"},
        {"num": 24, "ar": "المُعِزُّ", "meaning": "الذي يهب العزة لمن يشاء"},
        {"num": 25, "ar": "المُذِلُّ", "meaning": "الذي يذل من يشاء من الطغاة"},
        {"num": 26, "ar": "السَّمِيعُ", "meaning": "الذي يسمع كل شيء"},
        {"num": 27, "ar": "البَصِيرُ", "meaning": "الذي يرى كل شيء"},
        {"num": 28, "ar": "الحَكَمُ", "meaning": "الحاكم العدل بين خلقه"},
        {"num": 29, "ar": "العَدْلُ", "meaning": "العادل الذي لا يظلم أحداً"},
        {"num": 30, "ar": "اللَّطِيفُ", "meaning": "الرفيق بعباده الذي يوصل لهم مصالحهم"},
        {"num": 31, "ar": "الخَبِيرُ", "meaning": "العالم بحقائق الأشياء وبواطنها"},
        {"num": 32, "ar": "الحَلِيمُ", "meaning": "الذي لا يعاجل بالعقوبة"},
        {"num": 33, "ar": "العَظِيمُ", "meaning": "ذو العظمة المطلقة في ذاته وصفاته"},
        {"num": 34, "ar": "الغَفُورُ", "meaning": "الذي يكثر من المغفرة"},
        {"num": 35, "ar": "الشَّكُورُ", "meaning": "الذي يشكر اليسير من العمل ويثيب عليه"},
        {"num": 36, "ar": "العَلِيُّ", "meaning": "المتعالي فوق خلقه بذاته وصفاته"},
        {"num": 37, "ar": "الكَبِيرُ", "meaning": "ذو الكبرياء والعظمة"},
        {"num": 38, "ar": "الحَفِيظُ", "meaning": "الذي يحفظ كل شيء"},
        {"num": 39, "ar": "المُقِيتُ", "meaning": "الذي يقيت الخلائق ويوصل لهم أرزاقهم"},
        {"num": 40, "ar": "الحَسِيبُ", "meaning": "الكافي الذي يحاسب عباده"},
        {"num": 41, "ar": "الجَلِيلُ", "meaning": "ذو الجلال والعظمة"},
        {"num": 42, "ar": "الكَرِيمُ", "meaning": "الكثير الخير الجواد المعطي"},
        {"num": 43, "ar": "الرَّقِيبُ", "meaning": "المطلع على ما أكنّته الصدور"},
        {"num": 44, "ar": "المُجِيبُ", "meaning": "الذي يجيب دعوة الداعي"},
        {"num": 45, "ar": "الوَاسِعُ", "meaning": "الذي وسع رزقه جميع خلقه"},
        {"num": 46, "ar": "الحَكِيمُ", "meaning": "الذي يضع الأشياء في مواضعها"},
        {"num": 47, "ar": "الوَدُودُ", "meaning": "المحب لعباده الصالحين"},
        {"num": 48, "ar": "المَجِيدُ", "meaning": "ذو المجد والشرف والكرم"},
        {"num": 49, "ar": "البَاعِثُ", "meaning": "الذي يبعث الخلق يوم القيامة"},
        {"num": 50, "ar": "الشَّهِيدُ", "meaning": "الحاضر الذي لا يغيب عنه شيء"},
        {"num": 51, "ar": "الحَقُّ", "meaning": "الثابت الوجود حقاً"},
        {"num": 52, "ar": "الوَكِيلُ", "meaning": "المتكفل بأرزاق العباد"},
        {"num": 53, "ar": "القَوِيُّ", "meaning": "ذو القوة المتين"},
        {"num": 54, "ar": "المَتِينُ", "meaning": "الشديد القوي"},
        {"num": 55, "ar": "الوَلِيُّ", "meaning": "المتولي لأمور خلقه"},
        {"num": 56, "ar": "الحَمِيدُ", "meaning": "المحمود في كل أفعاله"},
        {"num": 57, "ar": "المُحْصِي", "meaning": "الذي أحصى كل شيء بعلمه"},
        {"num": 58, "ar": "المُبْدِئُ", "meaning": "الذي بدأ خلق الأشياء"},
        {"num": 59, "ar": "المُعِيدُ", "meaning": "الذي يعيد الخلق بعد فنائهم"},
        {"num": 60, "ar": "المُحْيِي", "meaning": "الذي يحيي الموتى"},
        {"num": 61, "ar": "المُمِيتُ", "meaning": "الذي يميت الأحياء"},
        {"num": 62, "ar": "الحَيُّ", "meaning": "الباقي حياً لا يموت"},
        {"num": 63, "ar": "القَيُّومُ", "meaning": "القائم بذاته المقيم لغيره"},
        {"num": 64, "ar": "الوَاجِدُ", "meaning": "الغني الذي لا يفتقر"},
        {"num": 65, "ar": "المَاجِدُ", "meaning": "ذو المجد التام"},
        {"num": 66, "ar": "الوَاحِدُ", "meaning": "المنفرد بذاته وصفاته"},
        {"num": 67, "ar": "الصَّمَدُ", "meaning": "المقصود في الحوائج"},
        {"num": 68, "ar": "القَادِرُ", "meaning": "القادر على كل شيء"},
        {"num": 69, "ar": "المُقْتَدِرُ", "meaning": "التام القدرة"},
        {"num": 70, "ar": "المُقَدِّمُ", "meaning": "الذي يقدم من يشاء"},
        {"num": 71, "ar": "المُؤَخِّرُ", "meaning": "الذي يؤخر من يشاء"},
        {"num": 72, "ar": "الأَوَّلُ", "meaning": "الذي ليس قبله شيء"},
        {"num": 73, "ar": "الآخِرُ", "meaning": "الذي ليس بعده شيء"},
        {"num": 74, "ar": "الظَّاهِرُ", "meaning": "الذي ظهر فوق كل شيء"},
        {"num": 75, "ar": "البَاطِنُ", "meaning": "المحتجب عن أبصار خلقه"},
        {"num": 76, "ar": "الوَالِي", "meaning": "المتولي لأمور خلقه"},
        {"num": 77, "ar": "المُتَعَالِي", "meaning": "المتعالي عن صفات المخلوقين"},
        {"num": 78, "ar": "البَرُّ", "meaning": "العطوف على عباده"},
        {"num": 79, "ar": "التَّوَّابُ", "meaning": "الذي يقبل توبة التائبين"},
        {"num": 80, "ar": "المُنْتَقِمُ", "meaning": "الذي ينتقم ممن عصاه"},
        {"num": 81, "ar": "العَفُوُّ", "meaning": "الذي يعفو عن الذنوب"},
        {"num": 82, "ar": "الرَّؤُوفُ", "meaning": "الرحيم بعباده"},
        {"num": 83, "ar": "مَالِكُ المُلْكِ", "meaning": "المتصرف في ملكه كيف يشاء"},
        {"num": 84, "ar": "ذُو الجَلَالِ وَالإِكْرَامِ", "meaning": "ذو العظمة والكبرياء والكرم"},
        {"num": 85, "ar": "المُقْسِطُ", "meaning": "العادل في حكمه"},
        {"num": 86, "ar": "الجَامِعُ", "meaning": "الذي يجمع الخلائق ليوم القيامة"},
        {"num": 87, "ar": "الغَنِيُّ", "meaning": "المستغني عن كل شيء"},
        {"num": 88, "ar": "المُغْنِي", "meaning": "الذي يغني من يشاء"},
        {"num": 89, "ar": "المَانِعُ", "meaning": "الذي يمنع ما يشاء عمن يشاء"},
        {"num": 90, "ar": "الضَّارُّ", "meaning": "المقدر للضر على من يشاء"},
        {"num": 91, "ar": "النَّافِعُ", "meaning": "المقدر للنفع لمن يشاء"},
        {"num": 92, "ar": "النُّورُ", "meaning": "نور السماوات والأرض"},
        {"num": 93, "ar": "الهَادِي", "meaning": "الذي يهدي من يشاء"},
        {"num": 94, "ar": "البَدِيعُ", "meaning": "المبدع لخلقه بلا مثال سابق"},
        {"num": 95, "ar": "البَاقِي", "meaning": "الذي لا ينتهي وجوده"},
        {"num": 96, "ar": "الوَارِثُ", "meaning": "الباقي بعد فناء خلقه"},
        {"num": 97, "ar": "الرَّشِيدُ", "meaning": "الذي يرشد الخلق لمصالحهم"},
        {"num": 98, "ar": "الصَّبُورُ", "meaning": "الذي لا يعجل بالعقوبة"},
        {"num": 99, "ar": "اللهُ", "meaning": "الاسم الأعظم الجامع لكل الأسماء"}
    ]
    return {"names": names, "total": 99}
class StoreItem(BaseModel):
    name: str
    description: str
    price_gold: int = 0
    price_usd: float = 0
    category: str = "theme"
    image_url: Optional[str] = None

@api_router.get("/store/items")
async def get_store_items(category: str = "all"):
    query = {} if category == "all" else {"category": category}
    items = await db.store_items.find(query, {"_id": 0}).to_list(100)
    if not items:
        # Seed default items
        defaults = [
            {"id": str(uuid.uuid4()), "name": "إطار ذهبي", "description": "إطار ذهبي مميز لصورتك الشخصية", "price_gold": 50, "price_usd": 0.99, "category": "frame", "image_url": None, "active": True},
            {"id": str(uuid.uuid4()), "name": "خلفية رمضانية", "description": "خلفية خاصة بشهر رمضان المبارك", "price_gold": 30, "price_usd": 0.49, "category": "theme", "image_url": None, "active": True},
            {"id": str(uuid.uuid4()), "name": "شارة حافظ", "description": "شارة مميزة تظهر بجانب اسمك", "price_gold": 100, "price_usd": 1.99, "category": "badge", "image_url": None, "active": True},
            {"id": str(uuid.uuid4()), "name": "تأثير نجوم", "description": "تأثير نجوم متحركة على منشوراتك", "price_gold": 75, "price_usd": 1.49, "category": "effect", "image_url": None, "active": True},
            {"id": str(uuid.uuid4()), "name": "عضوية مميزة (شهر)", "description": "وصول لميزات حصرية لمدة شهر", "price_gold": 500, "price_usd": 4.99, "category": "membership", "image_url": None, "active": True},
            {"id": str(uuid.uuid4()), "name": "صدقة جارية", "description": "تبرع بالذهب لمشاريع خيرية", "price_gold": 10, "price_usd": 0, "category": "charity", "image_url": None, "active": True},
        ]
        for item in defaults:
            await db.store_items.insert_one(item)
        items = [{k: v for k, v in d.items() if k != "_id"} for d in defaults]
    return {"items": items}

@api_router.post("/store/buy-gold")
async def buy_with_gold(data: dict, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    item_id = data.get("item_id")
    item = await db.store_items.find_one({"id": item_id}, {"_id": 0})
    if not item:
        raise HTTPException(404, "المنتج غير موجود")
    
    wallet = await db.wallets.find_one({"user_id": user["id"]})
    if not wallet or wallet.get("gold", 0) < item["price_gold"]:
        raise HTTPException(400, "رصيد الذهب غير كافٍ")
    
    await db.wallets.update_one({"user_id": user["id"]}, {"$inc": {"gold": -item["price_gold"]}})
    
    purchase = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "item_id": item_id,
        "item_name": item["name"],
        "price_gold": item["price_gold"],
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.purchases.insert_one(purchase)
    
    new_gold = wallet.get("gold", 0) - item["price_gold"]
    return {"success": True, "gold_remaining": new_gold, "message": f"تم شراء {item['name']}!"}

@api_router.get("/store/my-purchases")
async def get_my_purchases(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    purchases = await db.purchases.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"purchases": purchases}

# ==================== MEMBERSHIP ====================
@api_router.get("/membership/status")
async def get_membership(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    membership = await db.memberships.find_one({"user_id": user["id"]}, {"_id": 0})
    if not membership:
        return {"active": False, "plan": "free", "expires_at": None}
    # Check if expired
    if membership.get("expires_at"):
        from datetime import timezone
        exp = datetime.fromisoformat(membership["expires_at"])
        if exp < datetime.utcnow():
            return {"active": False, "plan": "free", "expires_at": membership["expires_at"], "was": membership.get("plan")}
    return {"active": True, "plan": membership.get("plan", "premium"), "expires_at": membership.get("expires_at")}

# ==================== STRIPE PAYMENTS ====================
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest
from starlette.requests import Request

# Store packages (server-side defined prices - NEVER accept from frontend)
STORE_PACKAGES = {
    "frame": {"name": "إطار ذهبي", "price": 0.99},
    "theme": {"name": "خلفية رمضانية", "price": 0.49},
    "badge": {"name": "شارة حافظ", "price": 1.99},
    "effect": {"name": "تأثير نجوم", "price": 1.49},
    "membership_monthly": {"name": "عضوية مميزة (شهر)", "price": 4.99},
    "gold_100": {"name": "100 ذهب", "price": 0.99},
    "gold_500": {"name": "500 ذهب", "price": 3.99},
    "gold_1000": {"name": "1000 ذهب", "price": 6.99},
}

@api_router.post("/payments/checkout")
async def create_checkout(data: dict, request: Request, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    package_id = data.get("package_id", "")
    origin_url = data.get("origin_url", "")
    item_id = data.get("item_id", "")
    
    if not origin_url:
        raise HTTPException(400, "origin_url مطلوب")
    
    # Get price from server-side packages OR from store item
    amount = 0.0
    package_name = ""
    
    if package_id in STORE_PACKAGES:
        amount = STORE_PACKAGES[package_id]["price"]
        package_name = STORE_PACKAGES[package_id]["name"]
    elif item_id:
        item = await db.store_items.find_one({"id": item_id}, {"_id": 0})
        if not item:
            raise HTTPException(404, "المنتج غير موجود")
        if item.get("price_usd", 0) <= 0:
            raise HTTPException(400, "هذا المنتج مجاني أو غير متاح للشراء بالمال")
        amount = float(item["price_usd"])
        package_name = item["name"]
    else:
        raise HTTPException(400, "يجب تحديد المنتج")
    
    success_url = f"{origin_url}/store?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{origin_url}/store"
    
    metadata = {
        "user_id": user["id"],
        "user_email": user.get("email", ""),
        "package_id": package_id,
        "item_id": item_id,
        "package_name": package_name,
    }
    
    host_url = str(request.base_url).rstrip("/")
    webhook_url = f"{host_url}api/webhook/stripe"
    
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    checkout_req = CheckoutSessionRequest(
        amount=amount,
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata,
    )
    
    session = await stripe_checkout.create_checkout_session(checkout_req)
    
    # Create payment transaction record
    txn = {
        "id": str(uuid.uuid4()),
        "session_id": session.session_id,
        "user_id": user["id"],
        "user_email": user.get("email", ""),
        "package_id": package_id,
        "item_id": item_id,
        "package_name": package_name,
        "amount": amount,
        "currency": "usd",
        "payment_status": "pending",
        "status": "initiated",
        "metadata": metadata,
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.payment_transactions.insert_one(txn)
    
    return {"url": session.url, "session_id": session.session_id}

@api_router.get("/payments/status/{session_id}")
async def get_payment_status(session_id: str, request: Request, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    txn = await db.payment_transactions.find_one({"session_id": session_id, "user_id": user["id"]}, {"_id": 0})
    if not txn:
        raise HTTPException(404, "المعاملة غير موجودة")
    
    # If already processed, return cached status
    if txn.get("payment_status") in ["paid", "expired"]:
        return {"status": txn["status"], "payment_status": txn["payment_status"], "amount": txn["amount"]}
    
    host_url = str(request.base_url).rstrip("/")
    webhook_url = f"{host_url}api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    checkout_status = await stripe_checkout.get_checkout_status(session_id)
    
    update_data = {
        "status": checkout_status.status,
        "payment_status": checkout_status.payment_status,
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    # Process successful payment (idempotent - check if already processed)
    if checkout_status.payment_status == "paid" and txn.get("payment_status") != "paid":
        update_data["payment_status"] = "paid"
        
        # Grant benefits based on package
        pkg_id = txn.get("package_id", "")
        if pkg_id.startswith("gold_"):
            gold_amount = int(pkg_id.split("_")[1])
            await db.wallets.update_one({"user_id": user["id"]}, {"$inc": {"gold": gold_amount, "total_earned": gold_amount}}, upsert=True)
            await db.gold_transactions.insert_one({"user_id": user["id"], "type": "purchase", "amount": gold_amount, "created_at": datetime.utcnow().isoformat(), "description": f"شراء {gold_amount} ذهب"})
        elif pkg_id == "membership_monthly":
            exp = (datetime.utcnow() + timedelta(days=30)).isoformat()
            await db.memberships.update_one({"user_id": user["id"]}, {"$set": {"plan": "premium", "expires_at": exp, "started_at": datetime.utcnow().isoformat()}}, upsert=True)
        
        # Record purchase for store items
        if txn.get("item_id"):
            await db.purchases.insert_one({"id": str(uuid.uuid4()), "user_id": user["id"], "item_id": txn["item_id"], "item_name": txn.get("package_name", ""), "price_usd": txn["amount"], "payment_method": "stripe", "created_at": datetime.utcnow().isoformat()})
    
    await db.payment_transactions.update_one({"session_id": session_id}, {"$set": update_data})
    
    return {"status": checkout_status.status, "payment_status": checkout_status.payment_status, "amount": txn["amount"]}

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    try:
        body = await request.body()
        sig = request.headers.get("Stripe-Signature", "")
        host_url = str(request.base_url).rstrip("/")
        webhook_url = f"{host_url}api/webhook/stripe"
        stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
        webhook_response = await stripe_checkout.handle_webhook(body, sig)
        
        if webhook_response.payment_status == "paid":
            txn = await db.payment_transactions.find_one({"session_id": webhook_response.session_id})
            if txn and txn.get("payment_status") != "paid":
                await db.payment_transactions.update_one(
                    {"session_id": webhook_response.session_id},
                    {"$set": {"payment_status": "paid", "status": "complete", "updated_at": datetime.utcnow().isoformat()}}
                )
        
        return {"received": True}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"received": True}

@api_router.get("/payments/packages")
async def get_packages():
    """Get available gold/membership packages"""
    return {"packages": [
        {"id": "gold_100", "name": "100 ذهب", "price": 0.99, "type": "gold", "amount": 100},
        {"id": "gold_500", "name": "500 ذهب", "price": 3.99, "type": "gold", "amount": 500},
        {"id": "gold_1000", "name": "1000 ذهب", "price": 6.99, "type": "gold", "amount": 1000},
        {"id": "membership_monthly", "name": "عضوية مميزة (شهر)", "price": 4.99, "type": "membership"},
    ]}


# ==================== VIRTUAL CREDITS SYSTEM (مثل تيك توك) ====================
# Currency conversion rates (approximate, updated periodically)
CURRENCY_DATA = {
    "US": {"code": "USD", "symbol": "$", "rate": 1.0},
    "GB": {"code": "GBP", "symbol": "£", "rate": 0.79},
    "EU": {"code": "EUR", "symbol": "€", "rate": 0.92},
    "DE": {"code": "EUR", "symbol": "€", "rate": 0.92},
    "FR": {"code": "EUR", "symbol": "€", "rate": 0.92},
    "SA": {"code": "SAR", "symbol": "ر.س", "rate": 3.75},
    "AE": {"code": "AED", "symbol": "د.إ", "rate": 3.67},
    "EG": {"code": "EGP", "symbol": "ج.م", "rate": 50.5},
    "MA": {"code": "MAD", "symbol": "د.م", "rate": 10.1},
    "DZ": {"code": "DZD", "symbol": "د.ج", "rate": 134.5},
    "TN": {"code": "TND", "symbol": "د.ت", "rate": 3.12},
    "TR": {"code": "TRY", "symbol": "₺", "rate": 36.5},
    "PK": {"code": "PKR", "symbol": "Rs", "rate": 278.0},
    "ID": {"code": "IDR", "symbol": "Rp", "rate": 15900.0},
    "MY": {"code": "MYR", "symbol": "RM", "rate": 4.48},
    "QA": {"code": "QAR", "symbol": "ر.ق", "rate": 3.64},
    "KW": {"code": "KWD", "symbol": "د.ك", "rate": 0.31},
    "BH": {"code": "BHD", "symbol": "د.ب", "rate": 0.376},
    "OM": {"code": "OMR", "symbol": "ر.ع", "rate": 0.385},
    "JO": {"code": "JOD", "symbol": "د.أ", "rate": 0.709},
    "LB": {"code": "LBP", "symbol": "ل.ل", "rate": 89500.0},
    "IQ": {"code": "IQD", "symbol": "د.ع", "rate": 1310.0},
    "IN": {"code": "INR", "symbol": "₹", "rate": 83.5},
    "BD": {"code": "BDT", "symbol": "৳", "rate": 110.0},
    "NG": {"code": "NGN", "symbol": "₦", "rate": 1580.0},
}

# Credit packages: price in EUR (base), credits given
CREDIT_PACKAGES = [
    {"id": "credits_5", "credits": 65, "price_eur": 0.05, "label": "65 نقطة", "popular": False},
    {"id": "credits_50", "credits": 650, "price_eur": 0.50, "label": "650 نقطة", "popular": False},
    {"id": "credits_100", "credits": 1300, "price_eur": 1.0, "label": "1,300 نقطة", "popular": True},
    {"id": "credits_500", "credits": 6800, "price_eur": 5.0, "label": "6,800 نقطة", "popular": False},
    {"id": "credits_1000", "credits": 14000, "price_eur": 10.0, "label": "14,000 نقطة", "popular": False},
    {"id": "credits_5000", "credits": 75000, "price_eur": 50.0, "label": "75,000 نقطة", "popular": False},
    {"id": "credits_10000", "credits": 160000, "price_eur": 100.0, "label": "160,000 نقطة", "popular": False},
    {"id": "credits_100000", "credits": 1700000, "price_eur": 1000.0, "label": "1,700,000 نقطة", "popular": False},
]

@api_router.get("/credits/detect-currency")
async def detect_currency(lat: float = Query(0), lon: float = Query(0)):
    """Detect user's currency based on GPS coordinates"""
    country_code = "US"
    try:
        if lat != 0 and lon != 0:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=ar")
                if r.status_code == 200:
                    data = r.json()
                    country_code = data.get("countryCode", "US")
    except Exception:
        pass
    
    currency = CURRENCY_DATA.get(country_code, CURRENCY_DATA["US"])
    return {"country_code": country_code, "currency": currency}

@api_router.get("/credits/packages")
async def get_credit_packages(country: str = "US"):
    """Get credit packages with local currency pricing"""
    currency = CURRENCY_DATA.get(country, CURRENCY_DATA["US"])
    packages = []
    for pkg in CREDIT_PACKAGES:
        local_price = round(pkg["price_eur"] * currency["rate"] / CURRENCY_DATA.get("EU", {"rate": 0.92})["rate"], 2)
        packages.append({
            **pkg,
            "local_price": local_price,
            "currency_code": currency["code"],
            "currency_symbol": currency["symbol"],
            "display_price": f"{currency['symbol']} {local_price:,.2f}",
        })
    return {"packages": packages, "currency": currency}

@api_router.get("/credits/balance")
async def get_credits_balance(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    wallet = await db.wallets.find_one({"user_id": user["id"]}, {"_id": 0})
    credits = wallet.get("credits", 0) if wallet else 0
    return {"credits": credits}

@api_router.post("/credits/purchase")
async def purchase_credits(data: dict, request: Request, user: dict = Depends(get_user)):
    """Create checkout session to purchase credits"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    package_id = data.get("package_id", "")
    origin_url = data.get("origin_url", "")
    pkg = next((p for p in CREDIT_PACKAGES if p["id"] == package_id), None)
    if not pkg:
        raise HTTPException(400, "الباقة غير صالحة")
    
    success_url = f"{origin_url}/rewards?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{origin_url}/rewards"
    
    host_url = str(request.base_url).rstrip("/")
    webhook_url = f"{host_url}api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=STRIPE_API_KEY, webhook_url=webhook_url)
    
    checkout_req = CheckoutSessionRequest(
        amount=pkg["price_eur"],
        currency="eur",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"user_id": user["id"], "package_id": package_id, "credits": str(pkg["credits"]), "type": "credit_purchase"},
    )
    session = await stripe_checkout.create_checkout_session(checkout_req)
    
    await db.payment_transactions.insert_one({
        "id": str(uuid.uuid4()), "session_id": session.session_id, "user_id": user["id"],
        "package_id": package_id, "amount": pkg["price_eur"], "currency": "eur",
        "credits": pkg["credits"], "type": "credit_purchase", "payment_status": "pending",
        "created_at": datetime.utcnow().isoformat(),
    })
    
    return {"url": session.url, "session_id": session.session_id}


# ==================== GIFT STORE (هدايا إسلامية) ====================
ISLAMIC_GIFTS = [
    {"id": "gift_lion", "name": "الأسد", "emoji": "🦁", "price_credits": 50, "description": "أسد الإسلام - هدية القوة"},
    {"id": "gift_crescent", "name": "الهلال الذهبي", "emoji": "🌙", "price_credits": 100, "description": "رمز الإسلام المتألق"},
    {"id": "gift_kaaba", "name": "الكعبة المشرفة", "emoji": "🕋", "price_credits": 500, "description": "هدية مميزة بيت الله الحرام"},
    {"id": "gift_star", "name": "النجمة", "emoji": "⭐", "price_credits": 30, "description": "نجمة الإبداع"},
    {"id": "gift_rose", "name": "الوردة", "emoji": "🌹", "price_credits": 20, "description": "وردة التقدير"},
    {"id": "gift_book", "name": "القرآن", "emoji": "📖", "price_credits": 200, "description": "نور المعرفة والهداية"},
    {"id": "gift_mosque", "name": "المسجد", "emoji": "🕌", "price_credits": 300, "description": "بيت من بيوت الله"},
    {"id": "gift_prayer", "name": "سجادة الصلاة", "emoji": "🧎", "price_credits": 150, "description": "للعابدين المخلصين"},
    {"id": "gift_crown", "name": "التاج الذهبي", "emoji": "👑", "price_credits": 1000, "description": "تاج الملوك - أغلى هدية"},
    {"id": "gift_diamond", "name": "الماسة", "emoji": "💎", "price_credits": 2000, "description": "ألماسة نادرة للمميزين"},
    {"id": "gift_dove", "name": "حمامة السلام", "emoji": "🕊️", "price_credits": 75, "description": "رسالة سلام ومحبة"},
    {"id": "gift_palm", "name": "النخلة", "emoji": "🌴", "price_credits": 40, "description": "نخلة البركة"},
]

@api_router.get("/gifts/list")
async def list_gifts():
    return {"gifts": ISLAMIC_GIFTS}

@api_router.post("/gifts/send")
async def send_gift(data: dict, user: dict = Depends(get_user)):
    """Send a gift to a content creator. 50% admin, 50% creator."""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    gift_id = data.get("gift_id", "")
    recipient_id = data.get("recipient_id", "")
    post_id = data.get("post_id", "")
    
    gift = next((g for g in ISLAMIC_GIFTS if g["id"] == gift_id), None)
    if not gift:
        raise HTTPException(400, "الهدية غير صالحة")
    
    if not recipient_id:
        raise HTTPException(400, "يجب تحديد المستلم")
    
    if recipient_id == user["id"]:
        raise HTTPException(400, "لا يمكنك إهداء نفسك")
    
    # Check sender credits
    wallet = await db.wallets.find_one({"user_id": user["id"]})
    sender_credits = wallet.get("credits", 0) if wallet else 0
    if sender_credits < gift["price_credits"]:
        raise HTTPException(400, "رصيد النقاط غير كافٍ")
    
    # Deduct from sender
    await db.wallets.update_one({"user_id": user["id"]}, {"$inc": {"credits": -gift["price_credits"]}})
    
    # 50/50 split: half to creator, half to admin pool
    creator_share = gift["price_credits"] // 2
    admin_share = gift["price_credits"] - creator_share
    
    # Add to creator's earnings
    await db.wallets.update_one(
        {"user_id": recipient_id},
        {"$inc": {"credits": creator_share, "total_earned_credits": creator_share}},
        upsert=True
    )
    
    # Add to admin pool
    await db.admin_pool.update_one(
        {"type": "gift_revenue"},
        {"$inc": {"total_credits": admin_share}},
        upsert=True
    )
    
    # Record gift transaction
    gift_record = {
        "id": str(uuid.uuid4()),
        "sender_id": user["id"],
        "sender_name": user.get("name", ""),
        "recipient_id": recipient_id,
        "post_id": post_id,
        "gift_id": gift_id,
        "gift_name": gift["name"],
        "gift_emoji": gift["emoji"],
        "credits": gift["price_credits"],
        "creator_share": creator_share,
        "admin_share": admin_share,
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.gift_transactions.insert_one(gift_record)
    gift_record.pop("_id", None)
    
    new_credits = sender_credits - gift["price_credits"]
    return {"success": True, "credits_remaining": new_credits, "gift": gift, "message": f"تم إرسال {gift['emoji']} {gift['name']}!"}

@api_router.get("/gifts/received")
async def get_received_gifts(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    gifts = await db.gift_transactions.find({"recipient_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"gifts": gifts}

@api_router.get("/gifts/on-post/{post_id}")
async def get_post_gifts(post_id: str):
    gifts = await db.gift_transactions.find({"post_id": post_id}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"gifts": gifts}


# ==================== AD MANAGER (إعلانات بنظام موافقة) ====================
@api_router.post("/ads/submit")
async def submit_ad(data: dict, user: dict = Depends(get_user)):
    """Submit an ad for admin review. Channels can embed their videos."""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    ad = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "user_name": user.get("name", ""),
        "title": data.get("title", ""),
        "description": data.get("description", ""),
        "video_url": data.get("video_url", ""),  # YouTube/Facebook embed URL
        "embed_type": data.get("embed_type", "youtube"),  # youtube, facebook, instagram, custom
        "channel_name": data.get("channel_name", ""),
        "price_credits": data.get("price_credits", 50),  # Admin sets price
        "status": "pending",  # pending -> approved -> active / rejected
        "views": 0,
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.user_ads.insert_one(ad)
    ad.pop("_id", None)
    return {"success": True, "ad": ad, "message": "تم إرسال الإعلان للمراجعة"}

@api_router.get("/ads/my-ads")
async def get_my_ads(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    ads = await db.user_ads.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"ads": ads}

@api_router.get("/ads/approved")
async def get_approved_ads():
    """Get approved ads for display"""
    ads = await db.user_ads.find({"status": "approved"}, {"_id": 0}).to_list(20)
    return {"ads": ads}

@api_router.post("/ads/watch/{ad_id}")
async def watch_ad(ad_id: str, user: dict = Depends(get_user)):
    """User watches an ad to earn credits"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    ad = await db.user_ads.find_one({"id": ad_id, "status": "approved"})
    if not ad:
        raise HTTPException(404, "الإعلان غير متاح")
    
    # Check if already watched today
    today = date.today().isoformat()
    already = await db.ad_views.find_one({"user_id": user["id"], "ad_id": ad_id, "date": today})
    if already:
        return {"earned": 0, "message": "شاهدت هذا الإعلان اليوم"}
    
    # Earn credits for watching
    earn_credits = 2  # Fixed earn per ad view
    await db.wallets.update_one({"user_id": user["id"]}, {"$inc": {"credits": earn_credits}}, upsert=True)
    await db.ad_views.insert_one({"user_id": user["id"], "ad_id": ad_id, "date": today, "created_at": datetime.utcnow().isoformat()})
    await db.user_ads.update_one({"id": ad_id}, {"$inc": {"views": 1}})
    
    return {"earned": earn_credits, "message": f"حصلت على {earn_credits} نقطة"}

# Admin ad management
@api_router.get("/admin/user-ads")
async def admin_get_user_ads(user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    ads = await db.user_ads.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"ads": ads}

@api_router.put("/admin/user-ads/{ad_id}")
async def admin_update_ad(ad_id: str, data: dict, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    
    update = {}
    if "status" in data:
        update["status"] = data["status"]
    if "price_credits" in data:
        update["price_credits"] = data["price_credits"]
    
    if update:
        await db.user_ads.update_one({"id": ad_id}, {"$set": update})
    return {"success": True}


# ==================== VENDOR MARKETPLACE (سوق المنتجات) ====================
@api_router.post("/marketplace/products")
async def create_product(data: dict, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    # Check if approved vendor
    vendor = await db.vendors.find_one({"user_id": user["id"], "status": "approved"})
    if not vendor:
        raise HTTPException(403, "يجب التسجيل كبائع والحصول على موافقة الإدارة أولاً")
    
    product = {
        "id": str(uuid.uuid4()),
        "vendor_id": user["id"],
        "vendor_name": vendor.get("shop_name", user.get("name", "")),
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "price": float(data.get("price", 0)),
        "currency": data.get("currency", "EUR"),
        "category": data.get("category", "general"),
        "image_url": data.get("image_url", ""),
        "location": data.get("location", vendor.get("location", {})),
        "status": "active",
        "views": 0,
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.products.insert_one(product)
    product.pop("_id", None)
    return {"success": True, "product": product}

@api_router.get("/marketplace/products")
async def list_products(lat: float = Query(0), lon: float = Query(0), category: str = "all", limit: int = 20):
    """List products sorted by distance (nearest first)"""
    query = {"status": "active"}
    if category != "all":
        query["category"] = category
    
    products = await db.products.find(query, {"_id": 0}).to_list(200)
    
    # Sort by distance if location provided
    if lat != 0 and lon != 0:
        def distance(p):
            loc = p.get("location", {})
            plat = loc.get("lat", 0)
            plon = loc.get("lon", 0)
            if plat == 0:
                return 999999
            dlat = math.radians(plat - lat)
            dlon = math.radians(plon - lon)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat)) * math.cos(math.radians(plat)) * math.sin(dlon/2)**2
            return 6371 * 2 * math.asin(math.sqrt(a))
        products.sort(key=distance)
    
    # Get admin commission rate
    settings = await db.admin_settings.find_one({"type": "marketplace"}, {"_id": 0})
    commission_rate = settings.get("commission_rate", 10) if settings else 10
    
    return {"products": products[:limit], "commission_rate": commission_rate}

@api_router.get("/marketplace/my-products")
async def my_products(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    products = await db.products.find({"vendor_id": user["id"]}, {"_id": 0}).to_list(100)
    return {"products": products}

# Admin marketplace settings
@api_router.put("/admin/marketplace/commission")
async def set_commission_rate(data: dict, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    rate = data.get("commission_rate", 10)
    await db.admin_settings.update_one({"type": "marketplace"}, {"$set": {"commission_rate": rate}}, upsert=True)
    return {"success": True, "commission_rate": rate}


# ==================== AI RELIGIOUS ASSISTANT (المساعد الديني) ====================
@api_router.post("/ai/ask")
async def ai_ask(data: dict, user: dict = Depends(get_user)):
    """AI Islamic assistant. 5 free questions, then requires credits. Max 20/day."""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    question = data.get("question", "").strip()
    session_id = data.get("session_id", str(uuid.uuid4()))
    if not question:
        raise HTTPException(400, "يجب كتابة السؤال")
    
    today = date.today().isoformat()
    
    # Count today's questions
    today_count = await db.ai_questions.count_documents({"user_id": user["id"], "date": today})
    
    if today_count >= 20:
        return {"answer": "", "error": "daily_limit", "message": "وصلت للحد الأقصى (20 سؤال). عُد غداً إن شاء الله.", "remaining": 0}
    
    # Check if needs credits (after 5 free)
    needs_credits = today_count >= 5
    if needs_credits:
        wallet = await db.wallets.find_one({"user_id": user["id"]})
        user_credits = wallet.get("credits", 0) if wallet else 0
        if user_credits < 5:
            return {"answer": "", "error": "no_credits", "message": "انتهت أسئلتك المجانية. شاهد فيديوهات لكسب نقاط أو اشترِ نقاطاً.", "remaining": 0, "credits": user_credits}
        # Deduct 5 credits per question
        await db.wallets.update_one({"user_id": user["id"]}, {"$inc": {"credits": -5}})
    
    # Call GPT-5.2 via emergent integrations
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage as LlmUserMessage
        
        system_prompt = """أنت مساعد إسلامي متخصص. تجيب فقط على الأسئلة المتعلقة بالإسلام والشريعة والقرآن والسنة والفقه والعقيدة والسيرة النبوية والأخلاق الإسلامية.
إذا سُئلت عن موضوع غير إسلامي، أجب بلطف: "أنا مختص بالأسئلة الإسلامية فقط. كيف أساعدك في أمور دينك؟"
أجب بالعربية دائماً. كن دقيقاً واذكر المصادر (القرآن، الحديث) كلما أمكن. لا تفتِ بدون دليل شرعي."""
        
        EMERGENT_KEY = os.environ.get("EMERGENT_LLM_KEY", "")
        
        chat = LlmChat(
            api_key=EMERGENT_KEY,
            session_id=f"islamic_assistant_{user['id']}_{session_id}",
            system_message=system_prompt,
        ).with_model("openai", "gpt-5.2")
        
        user_msg = LlmUserMessage(text=question)
        answer = await chat.send_message(user_msg)
        
    except Exception as e:
        logger.error(f"AI error: {e}")
        answer = "عذراً، حدث خطأ في الاتصال بالمساعد. حاول مرة أخرى."
    
    # Save question
    await db.ai_questions.insert_one({
        "user_id": user["id"],
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "date": today,
        "credits_used": 5 if needs_credits else 0,
        "created_at": datetime.utcnow().isoformat(),
    })
    
    remaining = 20 - today_count - 1
    free_remaining = max(0, 5 - today_count - 1)
    
    return {
        "answer": answer,
        "remaining": remaining,
        "free_remaining": free_remaining,
        "credits_used": 5 if needs_credits else 0,
        "session_id": session_id,
    }

@api_router.get("/ai/history")
async def ai_history(user: dict = Depends(get_user), session_id: str = ""):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    query = {"user_id": user["id"]}
    if session_id:
        query["session_id"] = session_id
    history = await db.ai_questions.find(query, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"history": history}

# ==================== USER BANK ACCOUNTS (للأرباح) ====================
@api_router.post("/user/bank-account")
async def set_bank_account(data: dict, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    bank_info = {
        "user_id": user["id"],
        "bank_name": data.get("bank_name", ""),
        "account_holder": data.get("account_holder", ""),
        "iban": data.get("iban", ""),
        "swift": data.get("swift", ""),
        "updated_at": datetime.utcnow().isoformat(),
    }
    await db.bank_accounts.update_one({"user_id": user["id"]}, {"$set": bank_info}, upsert=True)
    return {"success": True, "message": "تم حفظ معلومات الحساب البنكي"}

@api_router.get("/user/bank-account")
async def get_bank_account(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    account = await db.bank_accounts.find_one({"user_id": user["id"]}, {"_id": 0})
    return {"account": account}

@api_router.get("/user/earnings")
async def get_earnings(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    wallet = await db.wallets.find_one({"user_id": user["id"]}, {"_id": 0})
    gifts_received = await db.gift_transactions.count_documents({"recipient_id": user["id"]})
    total_earned = wallet.get("total_earned_credits", 0) if wallet else 0
    return {"total_earned_credits": total_earned, "gifts_received": gifts_received, "current_credits": wallet.get("credits", 0) if wallet else 0}

# Admin bank account settings
@api_router.post("/admin/bank-account")
async def admin_set_bank(data: dict, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    await db.admin_settings.update_one(
        {"type": "bank_account"},
        {"$set": {"bank_name": data.get("bank_name",""), "iban": data.get("iban",""), "swift": data.get("swift",""), "account_holder": data.get("account_holder",""), "updated_at": datetime.utcnow().isoformat()}},
        upsert=True
    )
    return {"success": True}

@api_router.get("/admin/bank-account")
async def admin_get_bank(user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    account = await db.admin_settings.find_one({"type": "bank_account"}, {"_id": 0})
    pool = await db.admin_pool.find_one({"type": "gift_revenue"}, {"_id": 0})
    return {"account": account, "revenue": pool}


# ==================== ADMIN ANNOUNCEMENTS ====================
@api_router.post("/admin/announcements")
async def create_announcement(data: dict, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    ann = {
        "id": str(uuid.uuid4()),
        "title": data.get("title", ""),
        "body": data.get("body", ""),
        "type": data.get("type", "info"),  # info, warning, promo
        "active": True,
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.announcements.insert_one(ann)
    ann.pop("_id", None)
    return {"success": True, "announcement": ann}

@api_router.get("/announcements")
async def get_announcements():
    """Public: get active announcements for homepage"""
    anns = await db.announcements.find({"active": True}, {"_id": 0}).sort("created_at", -1).to_list(5)
    return {"announcements": anns}

@api_router.delete("/admin/announcements/{ann_id}")
async def delete_announcement(ann_id: str, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    await db.announcements.update_one({"id": ann_id}, {"$set": {"active": False}})
    return {"success": True}

# ==================== VENDOR REGISTRATION ====================
@api_router.post("/marketplace/register-vendor")
async def register_vendor(data: dict, user: dict = Depends(get_user)):
    """Vendor registers shop for admin approval"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    existing = await db.vendors.find_one({"user_id": user["id"]})
    if existing:
        return {"vendor": {k: v for k, v in existing.items() if k != "_id"}, "message": "لديك طلب مسبق"}
    vendor = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "user_name": user.get("name", ""),
        "shop_name": data.get("shop_name", ""),
        "description": data.get("description", ""),
        "phone": data.get("phone", ""),
        "location": data.get("location", {}),
        "iban": data.get("iban", ""),
        "status": "pending",  # pending -> approved -> rejected
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.vendors.insert_one(vendor)
    vendor.pop("_id", None)
    return {"vendor": vendor, "message": "تم إرسال طلبك للمراجعة"}

@api_router.get("/marketplace/vendor-status")
async def vendor_status(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    vendor = await db.vendors.find_one({"user_id": user["id"]}, {"_id": 0})
    return {"vendor": vendor}

@api_router.get("/admin/vendors")
async def admin_list_vendors(user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    vendors = await db.vendors.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"vendors": vendors}

@api_router.put("/admin/vendors/{vendor_id}")
async def admin_update_vendor(vendor_id: str, data: dict, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    update = {}
    if "status" in data:
        update["status"] = data["status"]
    if update:
        await db.vendors.update_one({"id": vendor_id}, {"$set": update})
    return {"success": True}




# ==================== PRAYER TIMES ====================
@api_router.get("/prayer-times")
async def prayer_times(lat: float = Query(...), lon: float = Query(...), method: int = Query(4), school: int = Query(0)):
    """Get prayer times using Aladhan API"""
    try:
        today = date.today()
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"https://api.aladhan.com/v1/timings/{today.day}-{today.month}-{today.year}",
                params={"latitude": lat, "longitude": lon, "method": method, "school": school})
            r.raise_for_status()
            data = r.json()["data"]

        timings = data["timings"]
        hijri = data["date"]["hijri"]
        
        return {
            "success": True,
            "source": "aladhan",
            "times": {
                "fajr": clean_time(timings["Fajr"]),
                "sunrise": clean_time(timings["Sunrise"]),
                "dhuhr": clean_time(timings["Dhuhr"]),
                "asr": clean_time(timings["Asr"]),
                "maghrib": clean_time(timings["Maghrib"]),
                "isha": clean_time(timings["Isha"]),
                "midnight": clean_time(timings.get("Midnight", "")),
            },
            "hijri": {
                "date": f"{hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ",
                "day": hijri["day"],
                "month_ar": hijri["month"]["ar"],
                "month_en": hijri["month"]["en"],
                "month_num": hijri["month"]["number"],
                "year": hijri["year"],
            },
            "meta": data.get("meta", {})
        }
    except Exception as e:
        raise HTTPException(500, f"خطأ في جلب أوقات الصلاة: {str(e)}")

# ==================== MOSQUE SEARCH ====================
@api_router.get("/mosques/search")
async def search_mosques(
    lat: float = Query(...), lon: float = Query(...),
    radius: int = Query(5000), query: Optional[str] = Query(None)
):
    """Search mosques using Mawaqit API first, fallback to Overpass"""
    
    # Try Mawaqit first (has real prayer times!)
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            params = {"lat": lat, "lon": lon, "radius": radius}
            if query:
                params["word"] = query
            r = await c.get("https://mawaqit.net/api/2.0/mosque/search", params=params)
            if r.status_code == 200:
                mosques_raw = r.json()
                mosques = []
                for m in mosques_raw:
                    mosque = {
                        "osm_id": m.get("uuid", str(uuid.uuid4())),
                        "mawaqit_uuid": m.get("uuid"),
                        "name": m.get("name", ""),
                        "address": m.get("localisation", ""),
                        "latitude": float(m.get("latitude", 0)),
                        "longitude": float(m.get("longitude", 0)),
                        "websiteUrl": m.get("site"),
                        "phone": m.get("phone"),
                        "image": m.get("image"),
                        "hasAutoSync": True,
                        "hasMawaqit": True,
                        "times": m.get("times", []),
                        "iqama": m.get("iqama", []),
                        "jumua": m.get("jumua"),
                        "facilities": {
                            "womenSpace": m.get("womenSpace", False),
                            "parking": m.get("parking", False),
                            "ablutions": m.get("ablutions", False),
                            "handicapAccessibility": m.get("handicapAccessibility", False),
                            "childrenCourses": m.get("childrenCourses", False),
                            "adultCourses": m.get("adultCourses", False),
                        },
                        "_dist": float(m.get("proximity", 9999)) / 1000,
                    }
                    mosques.append(mosque)
                
                mosques.sort(key=lambda x: x["_dist"])
                return {"mosques": mosques[:50], "count": len(mosques), "source": "mawaqit"}
    except Exception as e:
        logger.warning(f"Mawaqit search failed: {e}")

    # Fallback to Overpass API
    try:
        if query:
            overpass_q = f'[out:json][timeout:20];(node["amenity"="place_of_worship"]["religion"="muslim"]["name"~"{query}",i](around:{radius},{lat},{lon});way["amenity"="place_of_worship"]["religion"="muslim"]["name"~"{query}",i](around:{radius},{lat},{lon}););out center body;'
        else:
            overpass_q = f'[out:json][timeout:20];(node["amenity"="place_of_worship"]["religion"="muslim"](around:{radius},{lat},{lon});way["amenity"="place_of_worship"]["religion"="muslim"](around:{radius},{lat},{lon}););out center body;'
        
        data = await query_overpass(overpass_q)
        mosques = []
        for el in (data or {}).get("elements", []):
            tags = el.get("tags", {})
            name = tags.get("name") or tags.get("name:ar")
            if not name:
                continue
            e_lat = el.get("lat") or el.get("center", {}).get("lat", 0)
            e_lon = el.get("lon") or el.get("center", {}).get("lon", 0)
            mosques.append({
                "osm_id": str(el.get("id")),
                "name": name,
                "address": tags.get("addr:street", "") + " " + tags.get("addr:city", ""),
                "latitude": e_lat, "longitude": e_lon,
                "hasAutoSync": False, "hasMawaqit": False,
                "_dist": haversine(lat, lon, e_lat, e_lon)
            })
        mosques.sort(key=lambda x: x["_dist"])
        return {"mosques": mosques[:50], "count": len(mosques), "source": "openstreetmap"}
    except Exception as e:
        raise HTTPException(500, f"خطأ في البحث: {str(e)}")

@api_router.post("/mosques/prayer-times")
async def mosque_times(req: MosqueTimesRequest):
    """Get mosque prayer times from Mawaqit or Aladhan"""
    
    # If we have UUID, use Mawaqit directly
    if req.mosqueUuid:
        try:
            async with httpx.AsyncClient(timeout=15) as c:
                r = await c.get(f"https://mawaqit.net/api/2.0/mosque/{req.mosqueUuid}/prayer-times")
                if r.status_code == 200:
                    data = r.json()
                    today_day = date.today().day
                    times_raw = data.get("times", {})
                    
                    if isinstance(times_raw, dict):
                        today_times = times_raw.get(str(today_day))
                    elif isinstance(times_raw, list) and len(times_raw) >= today_day:
                        today_times = times_raw[today_day - 1]
                    else:
                        today_times = None
                    
                    if today_times and len(today_times) >= 5:
                        keys = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]
                        times_map = {keys[i]: today_times[i] for i in range(min(len(keys), len(today_times)))}
                        return {
                            "success": True, "source": "mawaqit",
                            "times": times_map,
                            "jumua": data.get("jumua"),
                            "iqama": data.get("iqama"),
                        }
        except Exception as e:
            logger.warning(f"Mawaqit times error: {e}")

    # Try Mawaqit search by name
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get("https://mawaqit.net/api/2.0/mosque/search",
                params={"lat": req.latitude, "lon": req.longitude, "word": req.mosqueName[:20]})
            if r.status_code == 200:
                mosques = r.json()
                for m in mosques[:3]:
                    m_lat, m_lon = float(m.get("latitude", 0)), float(m.get("longitude", 0))
                    if haversine(req.latitude, req.longitude, m_lat, m_lon) < 0.5:
                        times = m.get("times", [])
                        if len(times) >= 5:
                            keys = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]
                            return {
                                "success": True, "source": "mawaqit",
                                "times": {keys[i]: times[i] for i in range(min(6, len(times)))},
                                "jumua": m.get("jumua"),
                                "iqama": m.get("iqama"),
                            }
    except Exception:
        pass

    # Fallback to Aladhan
    try:
        today = date.today()
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"https://api.aladhan.com/v1/timings/{today.day}-{today.month}-{today.year}",
                params={"latitude": req.latitude, "longitude": req.longitude, "method": req.method, "school": req.school})
            r.raise_for_status()
            t = r.json()["data"]["timings"]
            return {
                "success": True, "source": "calculated",
                "times": {
                    "fajr": clean_time(t["Fajr"]), "sunrise": clean_time(t["Sunrise"]),
                    "dhuhr": clean_time(t["Dhuhr"]), "asr": clean_time(t["Asr"]),
                    "maghrib": clean_time(t["Maghrib"]), "isha": clean_time(t["Isha"]),
                }
            }
    except Exception as e:
        raise HTTPException(500, str(e))

# ==================== PUSH NOTIFICATIONS ====================
@api_router.get("/push/vapid-key")
async def get_vapid_key():
    return {"publicKey": VAPID_PUBLIC_KEY}

@api_router.post("/push/subscribe")
async def subscribe_push(sub: PushSubscription, user: dict = Depends(get_user)):
    """Save push subscription to DB"""
    doc = {
        "id": str(uuid.uuid4()),
        "endpoint": sub.endpoint,
        "p256dh": sub.p256dh,
        "auth": sub.auth,
        "latitude": sub.latitude,
        "longitude": sub.longitude,
        "method": sub.method,
        "school": sub.school,
        "timezone": sub.timezone,
        "user_id": user["id"] if user else sub.user_id,
        "created_at": datetime.utcnow().isoformat(),
        "active": True,
    }
    await db.push_subscriptions.update_one(
        {"endpoint": sub.endpoint}, {"$set": doc}, upsert=True
    )
    return {"success": True, "message": "تم تسجيل الإشعارات بنجاح"}

@api_router.post("/push/test")
async def test_push(data: dict, user: dict = Depends(get_user)):
    """Send a test push notification"""
    endpoint = data.get("endpoint")
    if not endpoint:
        raise HTTPException(400, "endpoint مطلوب")
    
    sub = await db.push_subscriptions.find_one({"endpoint": endpoint})
    if not sub:
        raise HTTPException(404, "الاشتراك غير موجود")
    
    result = await send_push_notification(sub, {
        "title": "أذان وحكاية 🕌",
        "body": "تم تفعيل الإشعارات بنجاح!",
        "icon": "/pwa-icon-192.png",
        "badge": "/pwa-icon-192.png",
        "tag": "test",
    })
    return {"success": result}

async def send_push_notification(sub: dict, payload: dict) -> bool:
    """Send a web push notification using pywebpush"""
    try:
        from pywebpush import webpush, WebPushException
        webpush(
            subscription_info={
                "endpoint": sub["endpoint"],
                "keys": {"p256dh": sub["p256dh"], "auth": sub["auth"]},
            },
            data=json_module.dumps(payload),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_EMAIL},
        )
        return True
    except Exception as e:
        logger.error(f"Push failed: {e}")
        return False

@api_router.post("/push/send-prayer")
async def send_prayer_notifications(data: dict):
    """Send prayer time notifications to all subscribed users"""
    prayer_name = data.get("prayer", "")
    prayer_ar = {"fajr": "الفجر", "dhuhr": "الظهر", "asr": "العصر", "maghrib": "المغرب", "isha": "العشاء"}.get(prayer_name, prayer_name)
    
    subs = await db.push_subscriptions.find({"active": True}).to_list(None)
    sent = 0
    for sub in subs:
        payload = {
            "title": f"🕌 حان وقت صلاة {prayer_ar}",
            "body": "استعد للصلاة، حي على الصلاة، حي على الفلاح",
            "icon": "/pwa-icon-192.png",
            "badge": "/pwa-icon-192.png",
            "tag": f"prayer-{prayer_name}",
            "requireInteraction": True,
            "vibrate": [200, 100, 200, 100, 200],
            "actions": [{"action": "open", "title": "فتح التطبيق"}],
            "data": {"prayer": prayer_name, "type": "athan"}
        }
        if await send_push_notification(sub, payload):
            sent += 1
    
    return {"success": True, "sent": sent, "total": len(subs)}

# ==================== AI FEATURES ====================
@api_router.post("/ai/daily-athkar")
async def get_daily_athkar(req: DhikrAIRequest):
    """Generate contextual daily Athkar using Gemini AI"""
    
    prompts = {
        "morning": "أعطني 5 أذكار صباح مختلفة مع فضلها من الكتاب والسنة، بشكل JSON array من objects {text, virtue, count, reference}",
        "evening": "أعطني 5 أذكار مساء مختلفة مع فضلها من الكتاب والسنة، بشكل JSON array من objects {text, virtue, count, reference}",
        "after_prayer": "أعطني 5 أذكار بعد الصلاة مع فضلها، بشكل JSON array من objects {text, virtue, count, reference}",
        "sleep": "أعطني 5 أذكار النوم مع فضلها، بشكل JSON array من objects {text, virtue, count, reference}",
        "general": "أعطني 5 أذكار عامة يومية مع فضلها، بشكل JSON array من objects {text, virtue, count, reference}",
    }
    
    prompt = prompts.get(req.time_of_day, prompts["general"])
    if req.occasion:
        prompt += f". المناسبة: {req.occasion}"
    
    # Try Emergent LLM with Gemini
    if EMERGENT_LLM_KEY:
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"athkar-{req.time_of_day}-{date.today().isoformat()}",
                system_message="أنت عالم إسلامي متخصص في الأذكار والأدعية من الكتاب والسنة. أجب دائماً بـ JSON array صحيح فقط بدون أي نص إضافي."
            ).with_model("gemini", "gemini-2.0-flash")
            
            response = await chat.send_message(UserMessage(text=prompt))
            if response:
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    athkar = json_module.loads(json_match.group())
                    return {"success": True, "source": "gemini", "athkar": athkar, "time_of_day": req.time_of_day}
        except Exception as e:
            logger.warning(f"Emergent Gemini failed: {e}")
    
    # Fallback to static athkar
    return {
        "success": True, "source": "static",
        "time_of_day": req.time_of_day,
        "athkar": get_static_athkar(req.time_of_day)
    }

def get_static_athkar(time_of_day: str) -> list:
    morning = [
        {"text": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ", "virtue": "يُقال عند الصباح", "count": 1, "reference": "رواه مسلم"},
        {"text": "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ", "virtue": "من أذكار الصباح", "count": 1, "reference": "رواه الترمذي"},
        {"text": "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ", "virtue": "سيد الاستغفار", "count": 1, "reference": "رواه البخاري"},
        {"text": "أَعُوذُ بِكَلِمَاتِ اللهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", "virtue": "حماية من الشر", "count": 3, "reference": "رواه مسلم"},
        {"text": "بِسْمِ اللهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ", "virtue": "من قالها 3 مرات لم تضره مصيبة", "count": 3, "reference": "رواه أبو داود والترمذي"},
    ]
    evening = [
        {"text": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيكَ لَهُ", "virtue": "يُقال عند المساء", "count": 1, "reference": "رواه مسلم"},
        {"text": "اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ", "virtue": "من أذكار المساء", "count": 1, "reference": "رواه الترمذي"},
        {"text": "اللَّهُمَّ عَافِنِي فِي بَدَنِي، اللَّهُمَّ عَافِنِي فِي سَمْعِي، اللَّهُمَّ عَافِنِي فِي بَصَرِي", "virtue": "طلب العافية", "count": 3, "reference": "رواه أبو داود"},
        {"text": "أَعُوذُ بِكَلِمَاتِ اللهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", "virtue": "حماية من الشر", "count": 3, "reference": "رواه مسلم"},
        {"text": "حَسْبُنَا اللهُ وَنِعْمَ الْوَكِيلُ", "virtue": "من قالها صباحاً ومساءً كفاه الله", "count": 7, "reference": "رواه أبو داود"},
    ]
    return evening if "evening" in time_of_day else morning

@api_router.post("/ai/smart-reminder")
async def smart_reminder(data: dict):
    """Generate smart contextual Islamic reminder"""
    context = data.get("context", {})
    prayer = context.get("nextPrayer", "")
    minutes_left = context.get("minutesLeft", 0)
    
    prompt = f"أعطني تذكير إسلامي قصير (جملة واحدة) مناسب لشخص يبقى {minutes_left} دقيقة قبل صلاة {prayer}. أجب بالعربية فقط."
    
    if EMERGENT_LLM_KEY:
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"reminder-{prayer}-{datetime.now().isoformat()}",
                system_message="أنت مذكّر إسلامي لطيف. أجب بجملة واحدة فقط بالعربية."
            ).with_model("gemini", "gemini-2.0-flash")
            
            response = await chat.send_message(UserMessage(text=prompt))
            if response:
                return {"reminder": response.strip()}
        except Exception as e:
            logger.warning(f"Emergent reminder failed: {e}")
    
    reminders = [
        "تذكر أن الصلاة عماد الدين، استعد لها بالوضوء",
        "قال النبي ﷺ: أبرد بالظهر فإن شدة الحر من فيح جهنم",
        "الصلاة على وقتها من أحب الأعمال إلى الله",
        "لا تؤخر صلاتك، فإن الموت لا يستأذن",
    ]
    import random
    return {"reminder": random.choice(reminders)}

# ==================== HIJRI DATE ====================
@api_router.get("/hijri-date")
async def hijri_date(lat: float = Query(24.68), lon: float = Query(46.72)):
    try:
        today = date.today()
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"https://api.aladhan.com/v1/timings/{today.day}-{today.month}-{today.year}",
                params={"latitude": lat, "longitude": lon, "method": 4})
            r.raise_for_status()
            hijri = r.json()["data"]["date"]["hijri"]
        return {
            "hijriDate": f"{hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ",
            "day": hijri["day"], "month_ar": hijri["month"]["ar"],
            "month_en": hijri["month"]["en"], "year": hijri["year"],
            "month_num": hijri["month"]["number"],
        }
    except Exception as e:
        raise HTTPException(500, str(e))

# ==================== DAILY HADITH ====================
STATIC_HADITHS = [
    {"text": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى", "narrator": "عمر بن الخطاب", "source": "صحيح البخاري", "number": "1"},
    {"text": "مَنْ كَانَ يُؤْمِنُ بِاللهِ وَالْيَوْمِ الآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ", "narrator": "أبو هريرة", "source": "صحيح البخاري ومسلم", "number": "15"},
    {"text": "لا يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لِأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ", "narrator": "أنس بن مالك", "source": "صحيح البخاري ومسلم", "number": "13"},
    {"text": "الْمُسْلِمُ مَنْ سَلِمَ الْمُسْلِمُونَ مِنْ لِسَانِهِ وَيَدِهِ", "narrator": "عبد الله بن عمرو", "source": "صحيح البخاري", "number": "10"},
    {"text": "مَنْ سَلَكَ طَرِيقًا يَلْتَمِسُ فِيهِ عِلْمًا سَهَّلَ اللهُ لَهُ بِهِ طَرِيقًا إِلَى الجَنَّةِ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2699"},
    {"text": "إِنَّ اللهَ لا يَنْظُرُ إِلَى صُوَرِكُمْ وَأَمْوَالِكُمْ، وَلَكِنْ يَنْظُرُ إِلَى قُلُوبِكُمْ وَأَعْمَالِكُمْ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2564"},
    {"text": "الطُّهُورُ شَطْرُ الإِيمَانِ، وَالحَمْدُ لِلَّهِ تَمْلأُ المِيزَانَ", "narrator": "أبو مالك الأشعري", "source": "صحيح مسلم", "number": "223"},
    {"text": "خَيْرُكُمْ مَنْ تَعَلَّمَ القُرْآنَ وَعَلَّمَهُ", "narrator": "عثمان بن عفان", "source": "صحيح البخاري", "number": "5027"},
    {"text": "الدُّعَاءُ هُوَ الْعِبَادَةُ", "narrator": "النعمان بن بشير", "source": "سنن الترمذي", "number": "3247"},
    {"text": "مَا مِنْ عَبْدٍ يَسْتَغْفِرُ اللهَ إِلا غَفَرَ اللهُ لَهُ", "narrator": "أبو هريرة", "source": "سنن الترمذي", "number": "3559"},
    {"text": "تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ لَكَ صَدَقَةٌ", "narrator": "أبو ذر", "source": "سنن الترمذي", "number": "1956"},
    {"text": "أَحَبُّ الأَعْمَالِ إِلَى اللهِ أَدْوَمُهَا وَإِنْ قَلَّ", "narrator": "عائشة", "source": "صحيح البخاري ومسلم", "number": "6464"},
    {"text": "الدُّنْيَا سِجْنُ الْمُؤْمِنِ وَجَنَّةُ الْكَافِرِ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2956"},
    {"text": "مَنْ صَلَّى عَلَيَّ صَلاةً صَلَّى اللهُ عَلَيْهِ بِهَا عَشْرًا", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "408"},
    {"text": "اتَّقِ اللهَ حَيْثُمَا كُنْتَ وَأَتْبِعِ السَّيِّئَةَ الْحَسَنَةَ تَمْحُهَا وَخَالِقِ النَّاسَ بِخُلُقٍ حَسَنٍ", "narrator": "معاذ بن جبل", "source": "سنن الترمذي", "number": "1987"},
    {"text": "الصَّلَوَاتُ الْخَمْسُ وَالْجُمُعَةُ إِلَى الْجُمُعَةِ كَفَّارَاتٌ لِمَا بَيْنَهُنَّ مَا اجْتُنِبَتِ الْكَبَائِرُ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "233"},
    {"text": "إِذَا مَاتَ الإِنْسَانُ انْقَطَعَ عَمَلُهُ إِلا مِنْ ثَلاثٍ: صَدَقَةٍ جَارِيَةٍ، أَوْ عِلْمٍ يُنْتَفَعُ بِهِ، أَوْ وَلَدٍ صَالِحٍ يَدْعُو لَهُ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "1631"},
    {"text": "رِضَا اللهِ فِي رِضَا الْوَالِدَيْنِ وَسَخَطُ اللهِ فِي سَخَطِ الْوَالِدَيْنِ", "narrator": "عبد الله بن عمرو", "source": "سنن الترمذي", "number": "1899"},
    {"text": "مَا نَقَصَتْ صَدَقَةٌ مِنْ مَالٍ وَمَا زَادَ اللهُ عَبْدًا بِعَفْوٍ إِلا عِزًّا", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2588"},
    {"text": "كَلِمَتَانِ خَفِيفَتَانِ عَلَى اللِّسَانِ ثَقِيلَتَانِ فِي المِيزَانِ: سُبْحَانَ اللهِ وَبِحَمْدِهِ سُبْحَانَ اللهِ العَظِيمِ", "narrator": "أبو هريرة", "source": "صحيح البخاري ومسلم", "number": "6406"},
    {"text": "لَا تَحَاسَدُوا وَلَا تَنَاجَشُوا وَلَا تَبَاغَضُوا وَلَا تَدَابَرُوا وَكُونُوا عِبَادَ اللهِ إِخْوَانًا", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2564"},
    {"text": "مَنْ قَرَأَ آيَةَ الْكُرْسِيِّ دُبُرَ كُلِّ صَلاةٍ مَكْتُوبَةٍ لَمْ يَمْنَعْهُ مِنْ دُخُولِ الْجَنَّةِ إِلا أَنْ يَمُوتَ", "narrator": "أبو أمامة", "source": "سنن النسائي", "number": "9928"},
    {"text": "إِنَّ مِنْ أَحَبِّكُمْ إِلَيَّ وَأَقْرَبِكُمْ مِنِّي مَجْلِسًا يَوْمَ الْقِيَامَةِ أَحَاسِنُكُمْ أَخْلاقًا", "narrator": "جابر", "source": "سنن الترمذي", "number": "2018"},
    {"text": "الْجَنَّةُ تَحْتَ أَقْدَامِ الأُمَّهَاتِ", "narrator": "أنس بن مالك", "source": "سنن النسائي", "number": "3104"},
    {"text": "اقْرَأُوا الْقُرْآنَ فَإِنَّهُ يَأْتِي يَوْمَ الْقِيَامَةِ شَفِيعًا لِأَصْحَابِهِ", "narrator": "أبو أمامة", "source": "صحيح مسلم", "number": "804"},
    {"text": "مَنْ يُرِدِ اللهُ بِهِ خَيْرًا يُفَقِّهْهُ فِي الدِّينِ", "narrator": "معاوية بن أبي سفيان", "source": "صحيح البخاري", "number": "71"},
    {"text": "الْمُؤْمِنُ الْقَوِيُّ خَيْرٌ وَأَحَبُّ إِلَى اللهِ مِنَ الْمُؤْمِنِ الضَّعِيفِ وَفِي كُلٍّ خَيْرٌ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2664"},
    {"text": "بُنِيَ الإِسْلامُ عَلَى خَمْسٍ: شَهَادَةِ أَنْ لا إِلَهَ إِلا اللهُ وَأَنَّ مُحَمَّدًا رَسُولُ اللهِ وَإِقَامِ الصَّلاةِ وَإِيتَاءِ الزَّكَاةِ وَصَوْمِ رَمَضَانَ وَحَجِّ الْبَيْتِ", "narrator": "ابن عمر", "source": "صحيح البخاري ومسلم", "number": "8"},
    {"text": "مَثَلُ الَّذِي يَذْكُرُ رَبَّهُ وَالَّذِي لا يَذْكُرُ رَبَّهُ مَثَلُ الْحَيِّ وَالْمَيِّتِ", "narrator": "أبو موسى الأشعري", "source": "صحيح البخاري", "number": "6407"},
    {"text": "مَا مَلَأَ آدَمِيٌّ وِعَاءً شَرًّا مِنْ بَطْنٍ", "narrator": "المقدام بن معدي كرب", "source": "سنن الترمذي", "number": "2380"},
]

HADITH_TRANSLATIONS = {
    "1": {
        "en": {"text": "Actions are judged by intentions, and everyone will be rewarded according to what they intended.", "narrator": "Umar ibn Al-Khattab", "source": "Sahih Al-Bukhari"},
        "de": {"text": "Die Taten werden nach den Absichten beurteilt, und jeder wird nach dem belohnt, was er beabsichtigt hat.", "narrator": "Umar ibn Al-Khattab", "source": "Sahih Al-Bukhari"},
        "fr": {"text": "Les actes ne valent que par leurs intentions, et chacun sera rétribué selon ce qu'il a eu l'intention de faire.", "narrator": "Omar ibn Al-Khattab", "source": "Sahih Al-Boukhari"},
        "tr": {"text": "Ameller niyetlere göredir ve herkes niyet ettiğinin karşılığını alacaktır.", "narrator": "Ömer ibn Hattab", "source": "Sahih Buhari"},
        "ru": {"text": "Дела оцениваются по намерениям, и каждый получит то, что он намеревался.", "narrator": "Умар ибн аль-Хаттаб", "source": "Сахих аль-Бухари"},
        "sv": {"text": "Handlingar bedöms efter avsikter, och var och en belönas efter sin avsikt.", "narrator": "Umar ibn Al-Khattab", "source": "Sahih Al-Bukhari"},
        "nl": {"text": "Daden worden beoordeeld op intenties, en iedereen wordt beloond naar wat hij bedoelde.", "narrator": "Umar ibn Al-Khattab", "source": "Sahih Al-Bukhari"},
        "el": {"text": "Οι πράξεις κρίνονται από τις προθέσεις και καθένας ανταμείβεται σύμφωνα με αυτό που σκόπευε.", "narrator": "Ουμάρ ιμπν Αλ-Χαττάμπ", "source": "Σαχίχ Αλ-Μπουχάρι"},
    },
    "15": {
        "en": {"text": "Whoever believes in Allah and the Last Day, let him speak good or remain silent.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"},
        "de": {"text": "Wer an Allah und den Jüngsten Tag glaubt, soll Gutes sprechen oder schweigen.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"},
        "fr": {"text": "Quiconque croit en Allah et au Jour dernier, qu'il dise du bien ou qu'il se taise.", "narrator": "Abu Hurairah", "source": "Sahih Al-Boukhari & Mouslim"},
        "tr": {"text": "Allah'a ve ahiret gününe iman eden kimse ya hayır söylesin ya da sussun.", "narrator": "Ebu Hureyre", "source": "Sahih Buhari & Müslim"},
        "ru": {"text": "Кто верит в Аллаха и Судный день, пусть говорит благое или молчит.", "narrator": "Абу Хурайра", "source": "Сахих аль-Бухари и Муслим"},
        "sv": {"text": "Den som tror på Allah och den Yttersta dagen, låt honom tala gott eller vara tyst.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"},
        "nl": {"text": "Wie in Allah en de Laatste Dag gelooft, laat hem goed spreken of zwijgen.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"},
        "el": {"text": "Όποιος πιστεύει στον Αλλάχ και την Τελευταία Ημέρα, ας λέει καλά ή ας σιωπά.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"},
    },
    "13": {
        "en": {"text": "None of you truly believes until he loves for his brother what he loves for himself.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Bukhari & Muslim"},
        "de": {"text": "Keiner von euch glaubt wahrhaft, bis er für seinen Bruder wünscht, was er für sich selbst wünscht.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Bukhari & Muslim"},
        "fr": {"text": "Aucun d'entre vous ne croit véritablement tant qu'il n'aime pas pour son frère ce qu'il aime pour lui-même.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Boukhari & Mouslim"},
        "tr": {"text": "Sizden biriniz kendisi için istediğini kardeşi için de istemedikçe gerçek manada iman etmiş olmaz.", "narrator": "Enes bin Malik", "source": "Sahih Buhari & Müslim"},
        "ru": {"text": "Никто из вас не уверует по-настоящему, пока не полюбит для своего брата то, что любит для себя.", "narrator": "Анас ибн Малик", "source": "Сахих аль-Бухари и Муслим"},
        "sv": {"text": "Ingen av er tror verkligen förrän han önskar sin broder det han önskar sig själv.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Bukhari & Muslim"},
        "nl": {"text": "Niemand van jullie gelooft werkelijk totdat hij voor zijn broeder wenst wat hij voor zichzelf wenst.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Bukhari & Muslim"},
        "el": {"text": "Κανείς από εσάς δεν πιστεύει πραγματικά μέχρι να αγαπήσει για τον αδελφό του αυτό που αγαπά για τον εαυτό του.", "narrator": "Άνας ιμπν Μάλικ", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"},
    },
    "10": {
        "en": {"text": "A Muslim is one from whose tongue and hands other Muslims are safe.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Bukhari"},
        "sv": {"text": "En muslim är den vars tunga och händer andra muslimer är trygga från.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Bukhari"},
        "nl": {"text": "Een moslim is degene voor wiens tong en handen andere moslims veilig zijn.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Bukhari"},
        "el": {"text": "Μουσουλμάνος είναι αυτός από τη γλώσσα και τα χέρια του οποίου οι άλλοι μουσουλμάνοι είναι ασφαλείς.", "narrator": "Αμπντουλλάχ ιμπν Αμρ", "source": "Σαχίχ Αλ-Μπουχάρι"},
        "de": {"text": "Ein Muslim ist derjenige, vor dessen Zunge und Hand andere Muslime sicher sind.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Bukhari"},
        "fr": {"text": "Le musulman est celui dont la langue et les mains ne nuisent pas aux autres musulmans.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Boukhari"},
        "tr": {"text": "Müslüman, dilinden ve elinden diğer Müslümanların güvende olduğu kimsedir.", "narrator": "Abdullah bin Amr", "source": "Sahih Buhari"},
        "ru": {"text": "Мусульманин — тот, от чьего языка и рук другие мусульмане в безопасности.", "narrator": "Абдуллах ибн Амр", "source": "Сахих аль-Бухари"},
    },
    "2699": {
        "en": {"text": "Whoever takes a path seeking knowledge, Allah will make easy for him a path to Paradise.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "sv": {"text": "Den som tar en väg för att söka kunskap, Allah underlättar för honom vägen till Paradiset.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "nl": {"text": "Wie een pad bewandelt op zoek naar kennis, Allah maakt het pad naar het Paradijs gemakkelijk.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "el": {"text": "Όποιος ακολουθεί ένα μονοπάτι αναζητώντας γνώση, ο Αλλάχ θα του διευκολύνει το μονοπάτι προς τον Παράδεισο.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"},
        "de": {"text": "Wer einen Weg einschlägt, um Wissen zu suchen, dem erleichtert Allah den Weg zum Paradies.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "fr": {"text": "Quiconque emprunte un chemin à la recherche de la science, Allah lui facilitera un chemin vers le Paradis.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"},
        "tr": {"text": "Kim ilim öğrenmek için bir yola çıkarsa, Allah ona cennetin yolunu kolaylaştırır.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"},
        "ru": {"text": "Кто встал на путь поиска знания, Аллах облегчит ему путь в Рай.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"},
    },
    "2564": {
        "en": {"text": "Allah does not look at your appearance or wealth, but rather He looks at your hearts and deeds.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "sv": {"text": "Allah ser inte till ert utseende eller er rikedom, utan Han ser till era hjärtan och handlingar.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "nl": {"text": "Allah kijkt niet naar jullie uiterlijk of rijkdom, maar naar jullie harten en daden.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "el": {"text": "Ο Αλλάχ δεν κοιτάζει την εμφάνισή σας ή τον πλούτο σας, αλλά κοιτάζει τις καρδιές και τις πράξεις σας.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"},
        "de": {"text": "Allah schaut nicht auf euer Aussehen oder Vermögen, sondern auf eure Herzen und Taten.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "fr": {"text": "Allah ne regarde ni votre apparence ni vos richesses, mais Il regarde vos cœurs et vos actes.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"},
        "tr": {"text": "Allah sizin dış görünüşünüze ve mallarınıza bakmaz, kalplerinize ve amellerinize bakar.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"},
        "ru": {"text": "Аллах не смотрит на вашу внешность и богатство, а смотрит на ваши сердца и дела.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"},
    },
    "223": {"en": {"text": "Purification is half of faith, and praise be to Allah fills the scale.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Muslim"}, "sv": {"text": "Rening är halva tron, och lovprisning av Allah fyller vågskålen.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Muslim"}, "nl": {"text": "Reiniging is de helft van het geloof, en lof aan Allah vult de weegschaal.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Muslim"}, "el": {"text": "Η κάθαρση είναι το ήμισυ της πίστης, και η δοξολογία του Αλλάχ γεμίζει τη ζυγαριά.", "narrator": "Αμπού Μάλικ Αλ-Ασ'αρί", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Reinigung ist die Hälfte des Glaubens, und Alhamdulillah füllt die Waage.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Muslim"}, "fr": {"text": "La purification est la moitié de la foi, et la louange à Allah remplit la balance.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Mouslim"}, "tr": {"text": "Temizlik imanın yarısıdır ve Allah'a hamd etmek mizanı doldurur.", "narrator": "Ebu Malik el-Eş'arî", "source": "Sahih Müslim"}, "ru": {"text": "Очищение — половина веры, и восхваление Аллаха заполняет весы.", "narrator": "Абу Малик аль-Ашари", "source": "Сахих Муслим"}},
    "5027": {"en": {"text": "The best among you are those who learn the Quran and teach it.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Bukhari"}, "sv": {"text": "De bästa bland er är de som lär sig Koranen och lär ut den.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Bukhari"}, "nl": {"text": "De besten onder jullie zijn degenen die de Koran leren en onderwijzen.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Bukhari"}, "el": {"text": "Οι καλύτεροι μεταξύ σας είναι εκείνοι που μαθαίνουν το Κοράνι και το διδάσκουν.", "narrator": "Ουθμάν ιμπν Αφφάν", "source": "Σαχίχ Αλ-Μπουχάρι"}, "de": {"text": "Die Besten unter euch sind diejenigen, die den Quran lernen und lehren.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Bukhari"}, "fr": {"text": "Les meilleurs d'entre vous sont ceux qui apprennent le Coran et l'enseignent.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Boukhari"}, "tr": {"text": "Sizin en hayırlınız Kur'an'ı öğrenen ve öğretendir.", "narrator": "Osman bin Affan", "source": "Sahih Buhari"}, "ru": {"text": "Лучшие среди вас — те, кто изучает Коран и обучает ему.", "narrator": "Усман ибн Аффан", "source": "Сахих аль-Бухари"}},
    "3247": {"en": {"text": "Supplication (Dua) is worship itself.", "narrator": "An-Nu'man ibn Bashir", "source": "Sunan At-Tirmidhi"}, "sv": {"text": "Åkallan (Dua) är dyrkan i sig.", "narrator": "An-Nu'man ibn Bashir", "source": "Sunan At-Tirmidhi"}, "nl": {"text": "Smeekbede (Dua) is aanbidding zelf.", "narrator": "An-Nu'man ibn Bashir", "source": "Sunan At-Tirmidhi"}, "el": {"text": "Η ικεσία (Ντουά) είναι η ίδια η λατρεία.", "narrator": "Αν-Νου'μάν ιμπν Μπασίρ", "source": "Σουνάν Ατ-Τιρμιζί"}, "de": {"text": "Das Bittgebet (Dua) ist die Anbetung selbst.", "narrator": "An-Nu'man ibn Bashir", "source": "Sunan At-Tirmidhi"}, "fr": {"text": "L'invocation (Dua) est l'adoration elle-même.", "narrator": "An-Nu'man ibn Bashir", "source": "Sunan At-Tirmidhi"}, "tr": {"text": "Dua ibadetin ta kendisidir.", "narrator": "Nu'man bin Beşir", "source": "Sünen Tirmizî"}, "ru": {"text": "Мольба (Дуа) — это и есть поклонение.", "narrator": "Ан-Нуман ибн Башир", "source": "Сунан ат-Тирмизи"}},
    "3559": {"en": {"text": "No servant seeks forgiveness from Allah except that Allah forgives him.", "narrator": "Abu Hurairah", "source": "Sunan At-Tirmidhi"}, "sv": {"text": "Ingen tjänare söker förlåtelse från Allah utan att Allah förlåter honom.", "narrator": "Abu Hurairah", "source": "Sunan At-Tirmidhi"}, "nl": {"text": "Geen dienaar zoekt vergeving bij Allah of Allah vergeeft hem.", "narrator": "Abu Hurairah", "source": "Sunan At-Tirmidhi"}, "el": {"text": "Κανένας δούλος δεν ζητά συγχώρεση από τον Αλλάχ χωρίς ο Αλλάχ να τον συγχωρεί.", "narrator": "Αμπού Χουράιρα", "source": "Σουνάν Ατ-Τιρμιζί"}, "de": {"text": "Kein Diener bittet Allah um Vergebung, ohne dass Allah ihm vergibt.", "narrator": "Abu Hurairah", "source": "Sunan At-Tirmidhi"}, "fr": {"text": "Aucun serviteur ne demande pardon à Allah sans qu'Allah ne lui pardonne.", "narrator": "Abu Hurairah", "source": "Sunan At-Tirmidhi"}, "tr": {"text": "Hiçbir kul Allah'tan bağışlanma dilemez ki Allah onu bağışlamasın.", "narrator": "Ebu Hureyre", "source": "Sünen Tirmizî"}, "ru": {"text": "Нет раба, который просит прощения у Аллаха, кроме как Аллах прощает его.", "narrator": "Абу Хурайра", "source": "Сунан ат-Тирмизи"}},
    "1956": {"en": {"text": "Your smile in the face of your brother is charity.", "narrator": "Abu Dharr", "source": "Sunan At-Tirmidhi"}, "sv": {"text": "Ditt leende mot din broder är en välgörenhet.", "narrator": "Abu Dharr", "source": "Sunan At-Tirmidhi"}, "nl": {"text": "Uw glimlach naar uw broeder is liefdadigheid.", "narrator": "Abu Dharr", "source": "Sunan At-Tirmidhi"}, "el": {"text": "Το χαμόγελό σας στο πρόσωπο του αδελφού σας είναι ελεημοσύνη.", "narrator": "Αμπού Ντάρρ", "source": "Σουνάν Ατ-Τιρμιζί"}, "de": {"text": "Dein Lächeln gegenüber deinem Bruder ist eine Wohltätigkeit.", "narrator": "Abu Dharr", "source": "Sunan At-Tirmidhi"}, "fr": {"text": "Ton sourire au visage de ton frère est une aumône.", "narrator": "Abu Dharr", "source": "Sunan At-Tirmidhi"}, "tr": {"text": "Kardeşinin yüzüne gülümsemen sadakadır.", "narrator": "Ebu Zer", "source": "Sünen Tirmizî"}, "ru": {"text": "Твоя улыбка брату твоему — милостыня.", "narrator": "Абу Зарр", "source": "Сунан ат-Тирмизи"}},
    "6464": {"en": {"text": "The most beloved of deeds to Allah are the most consistent, even if small.", "narrator": "Aisha", "source": "Sahih Al-Bukhari & Muslim"}, "sv": {"text": "De mest älskade handlingarna hos Allah är de mest regelbundna, även om de är små.", "narrator": "Aisha", "source": "Sahih Al-Bukhari & Muslim"}, "nl": {"text": "De meest geliefde daden bij Allah zijn de meest consistente, zelfs als ze klein zijn.", "narrator": "Aisha", "source": "Sahih Al-Bukhari & Muslim"}, "el": {"text": "Οι πιο αγαπημένες πράξεις στον Αλλάχ είναι οι πιο σταθερές, ακόμα κι αν είναι μικρές.", "narrator": "Αΐσα", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"}, "de": {"text": "Die Allah liebsten Taten sind die beständigsten, auch wenn sie klein sind.", "narrator": "Aisha", "source": "Sahih Al-Bukhari & Muslim"}, "fr": {"text": "Les actes les plus aimés d'Allah sont les plus réguliers, même s'ils sont petits.", "narrator": "Aïcha", "source": "Sahih Al-Boukhari & Mouslim"}, "tr": {"text": "Allah'a en sevimli ameller az da olsa devamlı olanlarıdır.", "narrator": "Aişe", "source": "Sahih Buhari & Müslim"}, "ru": {"text": "Самые любимые дела пред Аллахом — самые постоянные, даже если малые.", "narrator": "Аиша", "source": "Сахих аль-Бухари и Муслим"}},
    "2956": {"en": {"text": "This world is a prison for the believer and a paradise for the disbeliever.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "Denna värld är ett fängelse för den troende och ett paradis för den otroende.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "Deze wereld is een gevangenis voor de gelovige en een paradijs voor de ongelovige.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Αυτός ο κόσμος είναι φυλακή για τον πιστό και παράδεισος για τον άπιστο.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Diese Welt ist ein Gefängnis für den Gläubigen und ein Paradies für den Ungläubigen.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Ce monde est une prison pour le croyant et un paradis pour le mécréant.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Dünya mümin için zindan, kâfir için cennettir.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Этот мир — тюрьма для верующего и рай для неверующего.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "408": {"en": {"text": "Whoever sends blessings upon me once, Allah will send blessings upon him tenfold.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "Den som sänder välsignelser över mig en gång, Allah sänder välsignelser över honom tio gånger.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "Wie eenmaal zegeningen over mij uitspreekt, Allah zegent hem tienvoudig.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Όποιος στέλνει ευλογίες σε μένα μία φορά, ο Αλλάχ θα του στείλει ευλογίες δεκαπλάσια.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Wer einmal Segen über mich spricht, dem sendet Allah zehnfach Segen.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Quiconque prie sur moi une fois, Allah priera sur lui dix fois.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Kim bana bir kez salât ederse, Allah ona on kez salât eder.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Кто благословит меня один раз, Аллах благословит его десятикратно.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "1987": {"en": {"text": "Fear Allah wherever you are, follow a bad deed with a good one to erase it, and treat people with good character.", "narrator": "Mu'adh ibn Jabal", "source": "Sunan At-Tirmidhi"}, "sv": {"text": "Frukta Allah var du än befinner dig, följ en dålig handling med en god som utplånar den, och behandla människor väl.", "narrator": "Mu'adh ibn Jabal", "source": "Sunan At-Tirmidhi"}, "nl": {"text": "Vrees Allah waar u ook bent, volg een slechte daad op met een goede om het uit te wissen, en behandel mensen met goed karakter.", "narrator": "Mu'adh ibn Jabal", "source": "Sunan At-Tirmidhi"}, "el": {"text": "Φοβήσου τον Αλλάχ όπου κι αν βρίσκεσαι, ακολούθησε μια κακή πράξη με μια καλή για να τη σβήσει, και φέρσου στους ανθρώπους με καλό χαρακτήρα.", "narrator": "Μουάζ ιμπν Τζαμπάλ", "source": "Σουνάν Ατ-Τιρμιζί"}, "de": {"text": "Fürchte Allah, wo immer du bist, folge einer schlechten Tat mit einer guten, die sie auslöscht, und behandle die Menschen mit gutem Charakter.", "narrator": "Mu'adh ibn Jabal", "source": "Sunan At-Tirmidhi"}, "fr": {"text": "Crains Allah où que tu sois, fais suivre une mauvaise action d'une bonne qui l'effacera, et comporte-toi avec les gens avec bon caractère.", "narrator": "Mu'adh ibn Jabal", "source": "Sunan At-Tirmidhi"}, "tr": {"text": "Nerede olursan ol Allah'tan kork, kötülüğün ardından onu silecek bir iyilik yap ve insanlara güzel ahlakla davran.", "narrator": "Muaz bin Cebel", "source": "Sünen Tirmizî"}, "ru": {"text": "Бойся Аллаха, где бы ты ни был, за плохим поступком следуй хорошим — он сотрёт его, и обращайся с людьми с хорошим нравом.", "narrator": "Муаз ибн Джабаль", "source": "Сунан ат-Тирмизи"}},
    "233": {"en": {"text": "The five daily prayers and Friday to Friday are expiation for sins committed between them, as long as major sins are avoided.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "De fem dagliga bönerna och fredag till fredag är försoning för synder emellan dem, så länge stora synder undviks.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "De vijf dagelijkse gebeden en vrijdag tot vrijdag zijn boetedoening voor zonden ertussen, zolang grote zonden worden vermeden.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Οι πέντε καθημερινές προσευχές και Παρασκευή με Παρασκευή είναι εξιλέωση για τις αμαρτίες μεταξύ τους, εφόσον αποφεύγονται οι μεγάλες αμαρτίες.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Die fünf täglichen Gebete und Freitag zu Freitag sind Sühne für die Sünden dazwischen, solange große Sünden vermieden werden.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Les cinq prières quotidiennes et vendredi en vendredi expient les péchés commis entre elles, tant que les grands péchés sont évités.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Beş vakit namaz ve cuma namazı aralarındaki günahlara kefârettir, büyük günahlardan kaçınıldığı sürece.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Пять ежедневных молитв и от пятницы до пятницы — искупление грехов между ними, если избегаются большие грехи.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "1631": {"en": {"text": "When a person dies, their deeds end except for three: ongoing charity, beneficial knowledge, or a righteous child who prays for them.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "När en person dör upphör hans handlingar utom tre: pågående välgörenhet, nyttig kunskap, eller ett rättfärdigt barn som ber för honom.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "Wanneer een persoon sterft, stoppen zijn daden behalve drie: doorlopende liefdadigheid, nuttige kennis, of een rechtschapen kind dat voor hem bidt.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Όταν ένας άνθρωπος πεθάνει, οι πράξεις του τελειώνουν εκτός από τρεις: συνεχής ελεημοσύνη, ωφέλιμη γνώση, ή ένα δίκαιο παιδί που προσεύχεται γι' αυτόν.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Wenn ein Mensch stirbt, enden seine Taten außer dreien: fortlaufende Wohltätigkeit, nützliches Wissen, oder ein rechtschaffenes Kind, das für ihn betet.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Quand une personne meurt, ses actes cessent sauf trois: une charité continue, un savoir utile, ou un enfant pieux qui prie pour elle.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "İnsan öldüğünde ameli kesilir, ancak üçü hariç: sadaka-i câriye, faydalı ilim veya kendisine dua eden hayırlı evlat.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Когда человек умирает, его дела прекращаются, кроме трёх: непрерывная милостыня, полезное знание, или праведный ребёнок, который молится за него.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "1899": {"en": {"text": "Allah's pleasure is in the pleasure of parents, and Allah's anger is in the anger of parents.", "narrator": "Abdullah ibn Amr", "source": "Sunan At-Tirmidhi"}, "sv": {"text": "Allahs tillfredsställelse ligger i föräldrarnas tillfredsställelse, och Allahs vrede ligger i föräldrarnas vrede.", "narrator": "Abdullah ibn Amr", "source": "Sunan At-Tirmidhi"}, "nl": {"text": "Allah's tevredenheid ligt in de tevredenheid van de ouders, en Allah's woede ligt in de woede van de ouders.", "narrator": "Abdullah ibn Amr", "source": "Sunan At-Tirmidhi"}, "el": {"text": "Η ευχαρίστηση του Αλλάχ βρίσκεται στην ευχαρίστηση των γονέων, και η οργή του Αλλάχ στην οργή των γονέων.", "narrator": "Αμπντουλλάχ ιμπν Αμρ", "source": "Σουνάν Ατ-Τιρμιζί"}, "de": {"text": "Allahs Zufriedenheit liegt in der Zufriedenheit der Eltern, und Allahs Zorn liegt im Zorn der Eltern.", "narrator": "Abdullah ibn Amr", "source": "Sunan At-Tirmidhi"}, "fr": {"text": "La satisfaction d'Allah réside dans la satisfaction des parents, et la colère d'Allah dans la colère des parents.", "narrator": "Abdullah ibn Amr", "source": "Sunan At-Tirmidhi"}, "tr": {"text": "Allah'ın rızası anne-babanın rızasında, Allah'ın gazabı anne-babanın gazabındadır.", "narrator": "Abdullah bin Amr", "source": "Sünen Tirmizî"}, "ru": {"text": "Довольство Аллаха — в довольстве родителей, и гнев Аллаха — в гневе родителей.", "narrator": "Абдуллах ибн Амр", "source": "Сунан ат-Тирмизи"}},
    "2588": {"en": {"text": "Charity does not decrease wealth, and Allah increases a servant in honor through forgiveness.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "Välgörenhet minskar inte rikedom, och Allah ökar en tjänares ära genom förlåtelse.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "Liefdadigheid vermindert geen rijkdom, en Allah verhoogt een dienaar in eer door vergeving.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Η ελεημοσύνη δεν μειώνει τον πλούτο, και ο Αλλάχ αυξάνει έναν δούλο σε τιμή μέσω της συγχώρεσης.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Wohltätigkeit mindert keinen Reichtum, und Allah erhöht einen Diener an Ehre durch Vergebung.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "L'aumône ne diminue pas la richesse, et Allah augmente l'honneur d'un serviteur par le pardon.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Sadaka malı eksiltmez, Allah affıyla kulunun izzetini artırır.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Милостыня не уменьшает богатство, и Аллах увеличивает честь раба через прощение.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "6406": {"en": {"text": "Two words are light on the tongue, heavy on the scale: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"}, "sv": {"text": "Två ord som är lätta på tungan, tunga på vågskålen: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"}, "nl": {"text": "Twee woorden licht op de tong, zwaar op de weegschaal: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"}, "el": {"text": "Δύο λέξεις ελαφριές στη γλώσσα, βαριές στη ζυγαριά: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"}, "de": {"text": "Zwei Worte, leicht auf der Zunge, schwer auf der Waage: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"}, "fr": {"text": "Deux mots légers sur la langue, lourds sur la balance: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Boukhari & Mouslim"}, "tr": {"text": "İki kelime dilde hafif, terazide ağır: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Ebu Hureyre", "source": "Sahih Buhari & Müslim"}, "ru": {"text": "Два слова легки на языке, тяжелы на весах: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Абу Хурайра", "source": "Сахих аль-Бухари и Муслим"}},
    "9928": {"en": {"text": "Whoever recites Ayat al-Kursi after every obligatory prayer, nothing prevents him from entering Paradise except death.", "narrator": "Abu Umamah", "source": "Sunan An-Nasa'i"}, "sv": {"text": "Den som läser Ayat al-Kursi efter varje obligatorisk bön, inget hindrar honom från Paradiset förutom döden.", "narrator": "Abu Umamah", "source": "Sunan An-Nasa'i"}, "nl": {"text": "Wie Ayat al-Kursi reciteert na elk verplicht gebed, niets belet hem het Paradijs binnen te gaan behalve de dood.", "narrator": "Abu Umamah", "source": "Sunan An-Nasa'i"}, "el": {"text": "Όποιος απαγγέλλει το Αγιάτ αλ-Κούρσι μετά κάθε υποχρεωτική προσευχή, τίποτα δεν τον εμποδίζει από τον Παράδεισο εκτός από τον θάνατο.", "narrator": "Αμπού Ουμάμα", "source": "Σουνάν Αν-Νασά'ι"}, "de": {"text": "Wer Ayat al-Kursi nach jedem Pflichtgebet rezitiert, den hindert nichts am Paradies außer dem Tod.", "narrator": "Abu Umamah", "source": "Sunan An-Nasa'i"}, "fr": {"text": "Quiconque récite Ayat al-Kursi après chaque prière obligatoire, rien ne l'empêche d'entrer au Paradis sauf la mort.", "narrator": "Abu Umamah", "source": "Sunan An-Nassaï"}, "tr": {"text": "Her farz namazdan sonra Âyetü'l-Kürsî okuyan kimseyi cennetten alıkoyan ölümden başka bir şey yoktur.", "narrator": "Ebu Ümame", "source": "Sünen Nesâî"}, "ru": {"text": "Кто читает Аят аль-Курси после каждой обязательной молитвы, ничто не мешает ему войти в Рай, кроме смерти.", "narrator": "Абу Умама", "source": "Сунан ан-Насаи"}},
    "804": {"en": {"text": "Read the Quran, for it will come as an intercessor for its companions on the Day of Resurrection.", "narrator": "Abu Umamah", "source": "Sahih Muslim"}, "sv": {"text": "Läs Koranen, ty den kommer som förespråkare för sina följeslagare på Uppståndelsens dag.", "narrator": "Abu Umamah", "source": "Sahih Muslim"}, "nl": {"text": "Lees de Koran, want hij zal komen als voorspreker voor zijn metgezellen op de Dag der Opstanding.", "narrator": "Abu Umamah", "source": "Sahih Muslim"}, "el": {"text": "Διαβάστε το Κοράνι, γιατί θα έρθει ως μεσίτης για τους συντρόφους του την Ημέρα της Ανάστασης.", "narrator": "Αμπού Ουμάμα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Lest den Quran, denn er wird am Tag der Auferstehung als Fürsprecher für seine Gefährten kommen.", "narrator": "Abu Umamah", "source": "Sahih Muslim"}, "fr": {"text": "Lisez le Coran, car il viendra comme intercesseur pour ses compagnons le Jour de la Résurrection.", "narrator": "Abu Umamah", "source": "Sahih Mouslim"}, "tr": {"text": "Kur'an okuyun, çünkü kıyamet günü ona sahip olanlara şefaatçi olarak gelecektir.", "narrator": "Ebu Ümame", "source": "Sahih Müslim"}, "ru": {"text": "Читайте Коран, ибо он придёт в День Воскресения как заступник за тех, кто его читал.", "narrator": "Абу Умама", "source": "Сахих Муслим"}},
    "71": {"en": {"text": "When Allah wishes good for someone, He grants him understanding of the religion.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Bukhari"}, "sv": {"text": "När Allah vill gott för någon, skänker Han honom förståelse av religionen.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Bukhari"}, "nl": {"text": "Wanneer Allah goed wil voor iemand, schenkt Hij hem begrip van de religie.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Bukhari"}, "el": {"text": "Όταν ο Αλλάχ θέλει καλό για κάποιον, του χαρίζει κατανόηση της θρησκείας.", "narrator": "Μουαγουίγια ιμπν Αμπί Σουφιάν", "source": "Σαχίχ Αλ-Μπουχάρι"}, "de": {"text": "Wenn Allah jemandem Gutes will, gewährt Er ihm Verständnis der Religion.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Bukhari"}, "fr": {"text": "Quand Allah veut du bien pour quelqu'un, Il lui accorde la compréhension de la religion.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Boukhari"}, "tr": {"text": "Allah bir kişiye hayır dilerse, onu dinde fakih kılar.", "narrator": "Muaviye bin Ebu Süfyan", "source": "Sahih Buhari"}, "ru": {"text": "Когда Аллах желает блага кому-то, Он дарует ему понимание религии.", "narrator": "Муавия ибн Абу Суфьян", "source": "Сахих аль-Бухари"}},
    "2664": {"en": {"text": "The strong believer is better and more beloved to Allah than the weak believer, and in each there is good.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "Den starke troende är bättre och mer älskad av Allah än den svage troende, och i vardera finns gott.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "De sterke gelovige is beter en meer geliefd bij Allah dan de zwakke gelovige, en in elk van beiden is goed.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Ο δυνατός πιστός είναι καλύτερος και πιο αγαπητός στον Αλλάχ από τον αδύναμο πιστό, και σε καθέναν υπάρχει καλό.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Der starke Gläubige ist besser und Allah lieber als der schwache Gläubige, und in jedem ist Gutes.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Le croyant fort est meilleur et plus aimé d'Allah que le croyant faible, et en chacun il y a du bien.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Kuvvetli mümin Allah'a zayıf müminden daha hayırlı ve daha sevimlidir, her ikisinde de hayır vardır.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Сильный верующий лучше и любимее Аллахом, чем слабый, и в каждом есть благо.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "8": {"en": {"text": "Islam is built upon five pillars: testifying that there is no god but Allah and Muhammad is His Messenger, establishing prayer, paying Zakat, fasting Ramadan, and making pilgrimage to the House.", "narrator": "Ibn Umar", "source": "Sahih Al-Bukhari & Muslim"}, "sv": {"text": "Islam bygger på fem pelare: att vittna att det inte finns någon gud utom Allah och att Muhammad är Hans sändebud, att förrätta bönen, att betala Zakat, att fasta under Ramadan och att vallfärda till Huset.", "narrator": "Ibn Umar", "source": "Sahih Al-Bukhari & Muslim"}, "nl": {"text": "De Islam is gebouwd op vijf zuilen: getuigen dat er geen god is dan Allah en dat Mohammed Zijn Boodschapper is, het gebed verrichten, Zakat betalen, vasten in Ramadan, en bedevaart naar het Huis.", "narrator": "Ibn Umar", "source": "Sahih Al-Bukhari & Muslim"}, "el": {"text": "Το Ισλάμ χτίστηκε πάνω σε πέντε πυλώνες: η μαρτυρία ότι δεν υπάρχει θεός εκτός του Αλλάχ και ο Μουχάμμαντ είναι ο Απεσταλμένος Του, η εκτέλεση της προσευχής, η πληρωμή Ζακάτ, η νηστεία του Ραμαζανιού και το προσκύνημα στο Σπίτι.", "narrator": "Ιμπν Ουμάρ", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"}, "de": {"text": "Der Islam basiert auf fünf Säulen: Das Bezeugnis, dass es keinen Gott außer Allah gibt und Muhammad Sein Gesandter ist, das Gebet zu verrichten, die Zakat zu entrichten, im Ramadan zu fasten und die Pilgerfahrt zum Haus zu unternehmen.", "narrator": "Ibn Umar", "source": "Sahih Al-Bukhari & Muslim"}, "fr": {"text": "L'Islam est bâti sur cinq piliers: témoigner qu'il n'y a de dieu qu'Allah et que Muhammad est Son Messager, accomplir la prière, payer la Zakat, jeûner le Ramadan et faire le pèlerinage à la Maison.", "narrator": "Ibn Umar", "source": "Sahih Al-Boukhari & Mouslim"}, "tr": {"text": "İslam beş esas üzerine kurulmuştur: Allah'tan başka ilah olmadığına ve Muhammed'in O'nun Resûlü olduğuna şehadet etmek, namaz kılmak, zekât vermek, Ramazan orucu tutmak ve Kâbe'yi haccetmek.", "narrator": "İbn Ömer", "source": "Sahih Buhari & Müslim"}, "ru": {"text": "Ислам построен на пяти столпах: свидетельство, что нет бога кроме Аллаха и Мухаммад — Его Посланник, совершение молитвы, выплата закята, пост в Рамадан и паломничество к Дому.", "narrator": "Ибн Умар", "source": "Сахих аль-Бухари и Муслим"}},
    "6407": {"en": {"text": "The likeness of the one who remembers his Lord and the one who does not is like the living and the dead.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Bukhari"}, "sv": {"text": "Liknelsen mellan den som minns sin Herre och den som inte gör det är som den levande och den döde.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Bukhari"}, "nl": {"text": "De gelijkenis van degene die zijn Heer gedenkt en degene die dat niet doet is als de levende en de dode.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Bukhari"}, "el": {"text": "Η ομοιότητα αυτού που μνημονεύει τον Κύριό του και αυτού που δεν το κάνει είναι σαν τον ζωντανό και τον νεκρό.", "narrator": "Αμπού Μούσα Αλ-Ασ'αρί", "source": "Σαχίχ Αλ-Μπουχάρι"}, "de": {"text": "Das Gleichnis dessen, der seines Herrn gedenkt, und dessen, der es nicht tut, ist wie das des Lebenden und des Toten.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Bukhari"}, "fr": {"text": "L'exemple de celui qui se souvient de son Seigneur et celui qui ne le fait pas est comme le vivant et le mort.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Boukhari"}, "tr": {"text": "Rabbini zikredenle zikretmeyenin misali, diri ile ölünün misali gibidir.", "narrator": "Ebu Musa el-Eş'arî", "source": "Sahih Buhari"}, "ru": {"text": "Подобие поминающего Господа и не поминающего — как живой и мёртвый.", "narrator": "Абу Муса аль-Ашари", "source": "Сахих аль-Бухари"}},
    "2380": {"en": {"text": "No human fills a vessel worse than his stomach.", "narrator": "Al-Miqdam ibn Ma'dikarib", "source": "Sunan At-Tirmidhi"}, "sv": {"text": "Ingen människa fyller ett kärl sämre än sin mage.", "narrator": "Al-Miqdam ibn Ma'dikarib", "source": "Sunan At-Tirmidhi"}, "nl": {"text": "Geen mens vult een vat slechter dan zijn maag.", "narrator": "Al-Miqdam ibn Ma'dikarib", "source": "Sunan At-Tirmidhi"}, "el": {"text": "Κανένας άνθρωπος δεν γεμίζει δοχείο χειρότερο από το στομάχι του.", "narrator": "Αλ-Μίκνταμ ιμπν Μα'ντικαρίμπ", "source": "Σουνάν Ατ-Τιρμιζί"}, "de": {"text": "Kein Mensch füllt ein Gefäß schlimmer als seinen Magen.", "narrator": "Al-Miqdam ibn Ma'dikarib", "source": "Sunan At-Tirmidhi"}, "fr": {"text": "L'homme ne remplit pas de récipient pire que son estomac.", "narrator": "Al-Miqdam ibn Ma'dikarib", "source": "Sunan At-Tirmidhi"}, "tr": {"text": "Âdemoğlu midesinden daha kötü bir kap doldurmamıştır.", "narrator": "Mikdam bin Ma'dîkerib", "source": "Sünen Tirmizî"}, "ru": {"text": "Человек не наполняет сосуда хуже своего желудка.", "narrator": "Аль-Микдам ибн Ма'дикариб", "source": "Сунан ат-Тирмизи"}},
    "2018": {"en": {"text": "The most beloved of you to me and nearest to me in assembly on the Day of Resurrection are those with the best character.", "narrator": "Jabir", "source": "Sunan At-Tirmidhi"}, "sv": {"text": "De mest älskade av er för mig och närmast mig på Uppståndelsens dag är de med bäst karaktär.", "narrator": "Jabir", "source": "Sunan At-Tirmidhi"}, "nl": {"text": "De meest geliefden van jullie bij mij en het dichtst bij mij op de Dag der Opstanding zijn degenen met het beste karakter.", "narrator": "Jabir", "source": "Sunan At-Tirmidhi"}, "el": {"text": "Οι πιο αγαπημένοι μου και πλησιέστεροί μου την Ημέρα της Ανάστασης είναι εκείνοι με τον καλύτερο χαρακτήρα.", "narrator": "Τζάμπιρ", "source": "Σουνάν Ατ-Τιρμιζί"}, "de": {"text": "Die mir Liebsten und mir am nächsten am Tag der Auferstehung sind jene mit dem besten Charakter.", "narrator": "Jabir", "source": "Sunan At-Tirmidhi"}, "fr": {"text": "Les plus aimés de moi et les plus proches de moi le Jour de la Résurrection sont ceux qui ont le meilleur caractère.", "narrator": "Jabir", "source": "Sunan At-Tirmidhi"}, "tr": {"text": "Kıyamet günü bana en sevimli ve en yakın olanınız ahlakı en güzel olanınızdır.", "narrator": "Cabir", "source": "Sünen Tirmizî"}, "ru": {"text": "Самые любимые мною и ближайшие ко мне в День Воскресения — обладающие лучшим нравом.", "narrator": "Джабир", "source": "Сунан ат-Тирмизи"}},
    "3104": {"en": {"text": "Paradise lies beneath the feet of mothers.", "narrator": "Anas ibn Malik", "source": "Sunan An-Nasa'i"}, "sv": {"text": "Paradiset ligger under mödrarnas fötter.", "narrator": "Anas ibn Malik", "source": "Sunan An-Nasa'i"}, "nl": {"text": "Het Paradijs ligt onder de voeten van moeders.", "narrator": "Anas ibn Malik", "source": "Sunan An-Nasa'i"}, "el": {"text": "Ο Παράδεισος βρίσκεται κάτω από τα πόδια των μητέρων.", "narrator": "Άνας ιμπν Μάλικ", "source": "Σουνάν Αν-Νασά'ι"}, "de": {"text": "Das Paradies liegt unter den Füßen der Mütter.", "narrator": "Anas ibn Malik", "source": "Sunan An-Nasa'i"}, "fr": {"text": "Le Paradis se trouve sous les pieds des mères.", "narrator": "Anas ibn Malik", "source": "Sunan An-Nassaï"}, "tr": {"text": "Cennet annelerin ayakları altındadır.", "narrator": "Enes bin Malik", "source": "Sünen Nesâî"}, "ru": {"text": "Рай находится под ногами матерей.", "narrator": "Анас ибн Малик", "source": "Сунан ан-Насаи"}},
}

@api_router.get("/daily-hadith")
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

@api_router.get("/quran/v4/chapters")
async def get_chapters_v4(language: str = Query("ar")):
    """Fetch all Surahs from Quran.com API v4"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/chapters", params={"language": language})
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran API error: {str(e)}")

@api_router.get("/quran/v4/chapters/{chapter_number}")
async def get_chapter_v4(chapter_number: int, language: str = Query("ar")):
    """Fetch specific Surah info from Quran.com API v4"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/chapters/{chapter_number}", params={"language": language})
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran API error: {str(e)}")

@api_router.get("/quran/v4/verses/by_chapter/{chapter_number}")
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

@api_router.get("/quran/v4/verses/by_juz/{juz_number}")
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

@api_router.get("/quran/v4/search")
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

@api_router.get("/quran/v4/juzs")
async def get_juzs_v4():
    """Fetch all Juz info from Quran.com API v4"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/juzs")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran API error: {str(e)}")

@api_router.get("/quran/v4/recitations/{recitation_id}/by_ayah/{verse_key}")
async def get_verse_audio_v4(recitation_id: int, verse_key: str):
    """Fetch verse audio recitation from Quran.com API v4"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{QURAN_V4_BASE}/recitations/{recitation_id}/by_ayah/{verse_key}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Quran audio error: {str(e)}")

@api_router.get("/quran/v4/resources/translations")
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

@api_router.get("/hadith/collections")
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

@api_router.get("/hadith/{collection}/books")
async def get_hadith_books(collection: str):
    """Fetch books within a Hadith collection"""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{SUNNAH_API_BASE}/collections/{collection}/books", headers={"X-API-Key": "SqD712P3E82xnwOAEOkGd5JZH8s9wRR24TqNFzjk"})
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, f"Hadith API error: {str(e)}")

@api_router.get("/hadith/{collection}/books/{book_number}/hadiths")
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

@api_router.get("/hadith/{collection}/{hadith_number}")
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
@api_router.get("/quran/surah/{number}")
async def get_surah(number: int, reciter: str = Query("ar.alafasy")):
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"https://api.alquran.cloud/v1/surah/{number}/{reciter}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, str(e))

@api_router.get("/quran/search")
async def search_quran(q: str = Query(...)):
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"https://api.alquran.cloud/v1/search/{q}/all/ar")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(500, str(e))

# ==================== USER DATA SYNC ====================
@api_router.post("/user/sync")
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

@api_router.get("/user/sync")
async def get_user_data(user: dict = Depends(get_user)):
    """Get synced user data"""
    if not user:
        raise HTTPException(401, "مطلوب تسجيل الدخول")
    doc = await db.user_data.find_one({"user_id": user["id"]}, {"_id": 0})
    return doc or {}

# ==================== ADMIN ====================
ADMIN_EMAILS = ['mohammadalrejab@gmail.com']

async def get_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="غير مصرح")
    payload = verify_jwt(credentials.credentials)
    if not payload or payload.get("email") not in ADMIN_EMAILS:
        raise HTTPException(status_code=403, detail="غير مصرح - ليس مسؤولاً")
    return payload

# OLD admin stats endpoint - replaced with new one below
# @api_router.get("/admin/stats")
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

@api_router.get("/admin/users")
async def admin_users(admin=Depends(get_admin_user), page: int = 1, limit: int = 20):
    """List all users"""
    skip = (page - 1) * limit
    users = await db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).skip(skip).to_list(limit)
    total = await db.users.count_documents({})
    return {"users": users, "total": total, "page": page, "pages": math.ceil(total / limit)}

@api_router.delete("/admin/users/{user_id}")
async def admin_delete_user(user_id: str, admin=Depends(get_admin_user)):
    """Delete a user"""
    result = await db.users.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return {"success": True, "message": "تم حذف المستخدم"}

@api_router.get("/admin/push-subscriptions")
async def admin_push_subs(admin=Depends(get_admin_user)):
    """List push subscriptions"""
    subs = await db.push_subscriptions.find({}, {"_id": 0}).to_list(100)
    return {"subscriptions": subs, "total": len(subs)}

class AdminNotification(BaseModel):
    title: str
    body: str
    target: str = "all"  # all, prayer, custom

@api_router.post("/admin/send-notification")
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

@api_router.get("/admin/ads")
async def admin_get_ads(admin=Depends(get_admin_user)):
    """List all ad placements"""
    ads = await db.ad_placements.find({}, {"_id": 0}).sort("priority", -1).to_list(100)
    return {"ads": ads, "total": len(ads)}

@api_router.post("/admin/ads")
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

@api_router.delete("/admin/ads/{ad_id}")
async def admin_delete_ad(ad_id: str, admin=Depends(get_admin_user)):
    """Delete ad placement"""
    result = await db.ad_placements.delete_one({"id": ad_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="الإعلان غير موجود")
    return {"success": True}

@api_router.get("/ads/active")
async def get_active_ads(placement: str = "all"):
    """Public endpoint - get active ads for a placement"""
    query = {"enabled": True}
    if placement != "all":
        query["$or"] = [{"placement": placement}, {"placement": "all"}]
    ads = await db.ad_placements.find(query, {"_id": 0}).sort("priority", -1).to_list(20)
    return {"ads": ads}

# Story moderation
@api_router.get("/admin/stories")
async def admin_get_stories(admin=Depends(get_admin_user), status: str = "pending"):
    """List stories for moderation"""
    stories = await db.stories.find({"status": status}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"stories": stories, "total": len(stories)}

@api_router.put("/admin/stories/{story_id}")
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

@api_router.get("/admin/pages")
async def admin_get_pages(admin=Depends(get_admin_user)):
    """List custom pages"""
    pages = await db.custom_pages.find({}, {"_id": 0}).sort("order", 1).to_list(100)
    return {"pages": pages}

@api_router.post("/admin/pages")
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

@api_router.delete("/admin/pages/{page_id}")
async def admin_delete_page(page_id: str, admin=Depends(get_admin_user)):
    await db.custom_pages.delete_one({"id": page_id})
    return {"success": True}

@api_router.get("/pages")
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

@api_router.get("/admin/ruqyah")
async def admin_get_ruqyah(admin=Depends(get_admin_user)):
    items = await db.ruqyah_items.find({}, {"_id": 0}).sort("order", 1).to_list(200)
    return {"items": items}

@api_router.post("/admin/ruqyah")
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

@api_router.delete("/admin/ruqyah/{item_id}")
async def admin_delete_ruqyah(item_id: str, admin=Depends(get_admin_user)):
    await db.ruqyah_items.delete_one({"id": item_id})
    return {"success": True}

@api_router.get("/ruqyah")
async def get_public_ruqyah(category: str = ""):
    query = {"enabled": True}
    if category:
        query["category"] = category
    items = await db.ruqyah_items.find(query, {"_id": 0}).sort("order", 1).to_list(200)
    return {"items": items}

# ===== ADMIN ALL STORIES (with status filter) =====
@api_router.get("/admin/all-stories")
async def admin_get_all_stories(admin=Depends(get_admin_user), status: str = "", page: int = 1, limit: int = 30):
    query = {}
    if status:
        query["status"] = status
    skip = (page - 1) * limit
    stories = await db.stories.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.stories.count_documents(query)
    return {"stories": stories, "total": total, "page": page}

@api_router.delete("/admin/stories/{story_id}")
async def admin_delete_story(story_id: str, admin=Depends(get_admin_user)):
    await db.stories.delete_one({"id": story_id})
    return {"success": True}

# ===== DONATIONS ADMIN =====
@api_router.get("/admin/donations")
async def admin_get_donations(admin=Depends(get_admin_user), status: str = ""):
    query = {}
    if status:
        query["status"] = status
    donations = await db.donations.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    total_amount = sum(d.get("amount", 0) for d in donations if d.get("status") == "approved")
    return {"donations": donations, "total": len(donations), "total_amount": total_amount}

@api_router.put("/admin/donations/{donation_id}")
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

@api_router.delete("/admin/donations/{donation_id}")
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

@api_router.get("/admin/scheduled-notifications")
async def admin_get_scheduled_notifs(admin=Depends(get_admin_user)):
    notifs = await db.scheduled_notifications.find({}, {"_id": 0}).to_list(50)
    return {"notifications": notifs}

@api_router.post("/admin/scheduled-notifications")
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

@api_router.delete("/admin/scheduled-notifications/{notif_id}")
async def admin_delete_scheduled_notif(notif_id: str, admin=Depends(get_admin_user)):
    await db.scheduled_notifications.delete_one({"id": notif_id})
    return {"success": True}

@api_router.get("/admin/settings")
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

@api_router.put("/admin/settings")
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

@api_router.get("/ad-config")
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

@api_router.post("/analytics/event")
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

@api_router.get("/admin/analytics/summary")
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

@api_router.get("/audio/dhikr")
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

@api_router.get("/localization/supported")
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

@api_router.get("/localization/strings/{lang}")
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

@api_router.get("/stories/categories")
async def get_story_categories():
    return {"categories": STORY_CATEGORIES}

class CreateStoryRequest(BaseModel):
    title: Optional[str] = None
    content: str = Field(..., min_length=1, max_length=10000)
    category: str = "istighfar"
    media_type: str = "text"  # text, image, video, embed
    image_url: Optional[str] = None
    embed_url: Optional[str] = None

@api_router.post("/stories/create")
async def create_story(data: CreateStoryRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول للنشر")
    post_id = str(uuid.uuid4())
    story = {
        "id": post_id,
        "author_id": user["id"],
        "author_name": user.get("name", "مستخدم"),
        "author_avatar": user.get("avatar"),
        "title": data.title or "",
        "content": data.content,
        "category": data.category,
        "media_type": data.media_type,
        "image_url": data.image_url,
        "embed_url": data.embed_url,
        "is_embed": data.media_type == "embed",
        "views_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "shares_count": 0,
        "is_story": True,
    }
    await db.posts.insert_one(story)
    story.pop("_id", None)
    story["liked"] = False
    story["saved"] = False
    story["likes_count"] = 0
    story["comments_count"] = 0
    return {"story": story}

@api_router.get("/stories/list")
async def list_stories(category: str = "all", page: int = 1, limit: int = 20, user: dict = Depends(get_user)):
    query = {"is_story": True}
    if category != "all":
        query["category"] = category
    skip = (page - 1) * limit
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    stories = await cursor.to_list(length=limit)
    total = await db.posts.count_documents(query)
    # Enrich
    post_ids = [s["id"] for s in stories]
    user_id = user["id"] if user else None
    likes_set, saves_set = set(), set()
    if user_id and post_ids:
        ul = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        likes_set = {d["post_id"] for d in ul}
        us = await db.saves.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        saves_set = {d["post_id"] for d in us}
    likes_counts, comments_counts = {}, {}
    if post_ids:
        async for doc in db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            likes_counts[doc["_id"]] = doc["c"]
        async for doc in db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            comments_counts[doc["_id"]] = doc["c"]
    for s in stories:
        pid = s["id"]
        s["liked"] = pid in likes_set
        s["saved"] = pid in saves_set
        s["likes_count"] = likes_counts.get(pid, 0)
        s["comments_count"] = comments_counts.get(pid, 0)
    return {"stories": stories, "total": total, "page": page, "has_more": skip + limit < total}

@api_router.get("/stories/my-saved")
async def get_my_saved_stories(limit: int = 50, user: dict = Depends(get_user)):
    """Get stories saved by current user"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    saved_docs = await db.saves.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    post_ids = [s["post_id"] for s in saved_docs]
    if not post_ids:
        return {"stories": []}
    stories = []
    for pid in post_ids:
        story = await db.posts.find_one({"id": pid, "is_story": True}, {"_id": 0})
        if story:
            story["liked"] = bool(await db.likes.find_one({"post_id": pid, "user_id": user["id"]}))
            story["saved"] = True
            story["likes_count"] = await db.likes.count_documents({"post_id": pid})
            story["comments_count"] = await db.comments.count_documents({"post_id": pid})
            stories.append(story)
    return {"stories": stories}

@api_router.get("/stories/my-liked")
async def get_my_liked_stories(limit: int = 50, user: dict = Depends(get_user)):
    """Get stories liked by current user"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    liked_docs = await db.likes.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    post_ids = [doc["post_id"] for doc in liked_docs]
    if not post_ids:
        return {"stories": []}
    stories = []
    for pid in post_ids:
        story = await db.posts.find_one({"id": pid, "is_story": True}, {"_id": 0})
        if story:
            story["liked"] = True
            story["saved"] = bool(await db.saves.find_one({"post_id": pid, "user_id": user["id"]}))
            story["likes_count"] = await db.likes.count_documents({"post_id": pid})
            story["comments_count"] = await db.comments.count_documents({"post_id": pid})
            stories.append(story)
    return {"stories": stories}

@api_router.post("/stories/auto-categorize")
async def auto_categorize_story(data: dict, user: dict = Depends(get_user)):
    """AI auto-categorize a story based on title and content"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    title = data.get("title", "")
    content = data.get("content", "")
    if not title and not content:
        return {"category": "general"}
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY
        ).with_model("gemini", "gemini-2.0-flash")
        categories_str = ", ".join([f"{c['key']}({c['label']})" for c in STORY_CATEGORIES if c['key'] != 'embed'])
        prompt = f"""صنف هذا المحتوى الإسلامي في واحدة من هذه الفئات فقط:
{categories_str}

العنوان: {title}
المحتوى: {content[:500]}

أجب بكلمة واحدة فقط هي مفتاح الفئة (مثل: istighfar, sahaba, quran, prophets, ruqyah, rizq, tawba, miracles, general)"""
        response = await chat.chat([UserMessage(content=prompt)])
        cat_key = response.content.strip().lower().replace('"', '').replace("'", "")
        valid_keys = [c["key"] for c in STORY_CATEGORIES if c["key"] != "embed"]
        if cat_key not in valid_keys:
            cat_key = "general"
        return {"category": cat_key}
    except Exception as e:
        logging.error(f"AI categorize error: {e}")
        return {"category": "general"}

@api_router.get("/stories/{story_id}")
async def get_story(story_id: str, user: dict = Depends(get_user)):
    story = await db.posts.find_one({"id": story_id}, {"_id": 0})
    if not story:
        raise HTTPException(404, "القصة غير موجودة")
    # Increment view
    await db.posts.update_one({"id": story_id}, {"$inc": {"views_count": 1}})
    story["views_count"] = story.get("views_count", 0) + 1
    # Enrich
    user_id = user["id"] if user else None
    story["liked"] = bool(await db.likes.find_one({"post_id": story_id, "user_id": user_id})) if user_id else False
    story["saved"] = bool(await db.saves.find_one({"post_id": story_id, "user_id": user_id})) if user_id else False
    story["likes_count"] = await db.likes.count_documents({"post_id": story_id})
    story["comments_count"] = await db.comments.count_documents({"post_id": story_id})
    return {"story": story}

@api_router.post("/stories/{story_id}/view")
async def track_story_view(story_id: str):
    await db.posts.update_one({"id": story_id}, {"$inc": {"views_count": 1}})
    return {"success": True}

@api_router.get("/ads/placement/{position}")
async def get_ads_by_placement(position: str):
    """Get active ads for a specific placement position"""
    query = {"enabled": True, "$or": [{"placement": position}, {"placement": "all"}]}
    ads = await db.ad_placements.find(query, {"_id": 0}).sort("priority", -1).to_list(5)
    return {"ads": ads}

@api_router.get("/stories/feed/most-viewed")
async def most_viewed_stories(limit: int = 20, user: dict = Depends(get_user)):
    pipeline = [
        {"$match": {"is_story": True}},
        {"$lookup": {"from": "likes", "localField": "id", "foreignField": "post_id", "as": "likes_data"}},
        {"$lookup": {"from": "comments", "localField": "id", "foreignField": "post_id", "as": "comments_data"}},
        {"$addFields": {
            "likes_count": {"$size": "$likes_data"},
            "comments_count": {"$size": "$comments_data"},
        }},
        {"$project": {"_id": 0, "likes_data": 0, "comments_data": 0}},
        {"$sort": {"views_count": -1, "created_at": -1}},
        {"$limit": limit}
    ]
    stories = []
    async for doc in db.posts.aggregate(pipeline):
        doc["liked"] = False
        doc["saved"] = False
        stories.append(doc)
    # Enrich user-specific
    if user:
        pids = [s["id"] for s in stories]
        if pids:
            ul = await db.likes.find({"post_id": {"$in": pids}, "user_id": user["id"]}, {"_id": 0, "post_id": 1}).to_list(None)
            ls = {d["post_id"] for d in ul}
            for s in stories:
                s["liked"] = s["id"] in ls
    return {"stories": stories}

@api_router.get("/stories/feed/most-interacted")
async def most_interacted_stories(limit: int = 20, user: dict = Depends(get_user)):
    pipeline = [
        {"$match": {"is_story": True}},
        {"$lookup": {"from": "likes", "localField": "id", "foreignField": "post_id", "as": "likes_data"}},
        {"$lookup": {"from": "comments", "localField": "id", "foreignField": "post_id", "as": "comments_data"}},
        {"$addFields": {
            "likes_count": {"$size": "$likes_data"},
            "comments_count": {"$size": "$comments_data"},
            "engagement": {"$add": [{"$multiply": [{"$size": "$likes_data"}, 2]}, {"$multiply": [{"$size": "$comments_data"}, 3]}, {"$ifNull": ["$views_count", 0]}]}
        }},
        {"$project": {"_id": 0, "likes_data": 0, "comments_data": 0}},
        {"$sort": {"engagement": -1, "created_at": -1}},
        {"$limit": limit}
    ]
    stories = []
    async for doc in db.posts.aggregate(pipeline):
        doc["liked"] = False
        doc["saved"] = False
        stories.append(doc)
    if user:
        pids = [s["id"] for s in stories]
        if pids:
            ul = await db.likes.find({"post_id": {"$in": pids}, "user_id": user["id"]}, {"_id": 0, "post_id": 1}).to_list(None)
            ls = {d["post_id"] for d in ul}
            for s in stories:
                s["liked"] = s["id"] in ls
    return {"stories": stories}

@api_router.get("/stories/feed/search")
async def search_stories(q: str = Query("", min_length=1), limit: int = 30, user: dict = Depends(get_user)):
    if not q.strip():
        return {"stories": []}
    search_regex = {"$regex": q.strip(), "$options": "i"}
    query = {"is_story": True, "$or": [{"title": search_regex}, {"content": search_regex}, {"author_name": search_regex}, {"category": search_regex}]}
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).limit(limit)
    stories = await cursor.to_list(length=limit)
    post_ids = [s["id"] for s in stories]
    likes_counts, comments_counts = {}, {}
    if post_ids:
        async for doc in db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            likes_counts[doc["_id"]] = doc["c"]
        async for doc in db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            comments_counts[doc["_id"]] = doc["c"]
    for s in stories:
        s["likes_count"] = likes_counts.get(s["id"], 0)
        s["comments_count"] = comments_counts.get(s["id"], 0)
        s["liked"] = False
        s["saved"] = False
    return {"stories": stories}

# ==================== ADMIN EMBED CONTENT (محتوى مضمن) ====================

class EmbedContentRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = ""
    embed_url: str = Field(..., min_length=5)
    platform: str = "youtube"  # youtube, dailymotion, vimeo, etc.
    category: str = "general"
    thumbnail_url: Optional[str] = None

@api_router.post("/admin/embed-content")
async def create_embed_content(data: EmbedContentRequest, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or (admin.get("email") not in ADMIN_EMAILS and not admin.get("is_admin")):
        raise HTTPException(403, "غير مصرح - للمشرف فقط")
    content = {
        "id": str(uuid.uuid4()),
        "title": data.title,
        "description": data.description,
        "embed_url": data.embed_url,
        "platform": data.platform,
        "category": data.category,
        "thumbnail_url": data.thumbnail_url,
        "views": 0,
        "active": True,
        "created_by": user["id"] if user else "system",
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.embed_content.insert_one(content)
    content.pop("_id", None)
    # Also create a story post so it appears in the Stories feed
    story_post = {
        "id": str(uuid.uuid4()),
        "author_id": user["id"] if user else "system",
        "author_name": admin.get("name", "المشرف") if admin else "المشرف",
        "author_avatar": admin.get("avatar") if admin else None,
        "title": data.title,
        "content": data.description or data.title,
        "category": data.category if data.category != "general" else "embed",
        "media_type": "embed",
        "image_url": data.thumbnail_url,
        "embed_url": data.embed_url,
        "platform": data.platform,
        "views_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "shares_count": 0,
        "is_story": True,
        "is_embed": True,
        "embed_content_id": content["id"],
    }
    await db.posts.insert_one(story_post)
    return {"success": True, "content": content}

@api_router.get("/admin/embed-content")
async def admin_list_embed_content(user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or (admin.get("email") not in ["mohammadalrejab@gmail.com"] and not admin.get("is_admin")):
        raise HTTPException(403, "غير مصرح")
    content = await db.embed_content.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"content": content}

@api_router.delete("/admin/embed-content/{content_id}")
async def delete_embed_content(content_id: str, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or (admin.get("email") not in ["mohammadalrejab@gmail.com"] and not admin.get("is_admin")):
        raise HTTPException(403, "غير مصرح")
    await db.embed_content.delete_one({"id": content_id})
    # Also remove linked story post
    await db.posts.delete_one({"embed_content_id": content_id})
    return {"success": True}

@api_router.get("/embed-content")
async def public_embed_content(category: str = "all", limit: int = 20):
    query = {"active": True}
    if category != "all":
        query["category"] = category
    content = db.embed_content.find(query, {"_id": 0}).sort("created_at", -1).limit(limit)
    items = await content.to_list(length=limit)
    return {"content": items}

# ==================== STATUS (legacy) ====================
class StatusCheckCreate(BaseModel):
    client_name: str

@api_router.post("/status")
async def create_status(data: StatusCheckCreate):
    doc = {"id": str(uuid.uuid4()), "client_name": data.client_name, "timestamp": datetime.utcnow().isoformat()}
    await db.status_checks.insert_one(doc)
    return doc

@api_router.get("/status")
async def get_status():
    docs = await db.status_checks.find({}, {"_id": 0}).to_list(100)
    return docs

# ==================== MIDDLEWARE ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_router.post("/contact")
async def submit_contact(data: dict):
    """Submit a contact form message"""
    doc = {
        "id": str(uuid.uuid4())[:8],
        "name": data.get("name", ""),
        "email": data.get("email", ""),
        "message": data.get("message", ""),
        "created_at": datetime.utcnow().isoformat(),
        "read": False
    }
    await db.contact_messages.insert_one(doc)
    return {"success": True, "message": "تم إرسال رسالتك"}

@api_router.post("/report")
async def report_content(data: dict, user: dict = Depends(get_user)):
    """Report inappropriate content"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    doc = {
        "id": str(uuid.uuid4())[:8],
        "reporter_id": user["id"],
        "content_id": data.get("content_id", ""),
        "content_type": data.get("content_type", ""),
        "reason": data.get("reason", ""),
        "created_at": datetime.utcnow().isoformat(),
        "resolved": False
    }
    await db.reports.insert_one(doc)
    return {"success": True}

@api_router.get("/ai/daily-dua")
async def get_daily_dua():
    """Get AI-generated daily dua"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY).with_model("gemini", "gemini-2.0-flash")
        prompt = """اختر دعاء إسلامي صحيح من القرآن أو السنة. أعطني:
1. نص الدعاء بالعربية فقط
2. المصدر (القرآن أو الحديث)

أجب بصيغة JSON فقط:
{"text": "نص الدعاء", "source": "المصدر"}"""
        response = await chat.chat([UserMessage(content=prompt)])
        import re
        match = re.search(r'\{[^}]+\}', response.content)
        if match:
            data = json_module.loads(match.group())
            return {"dua": data}
    except Exception as e:
        logging.error(f"Daily dua error: {e}")
    return {"dua": {"text": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", "source": "سورة البقرة 201"}}

@api_router.get("/ai/verse-of-day")
async def get_verse_of_day(language: str = Query("ar")):
    """Get AI-selected verse of the day with translation"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY).with_model("gemini", "gemini-2.0-flash")
        
        lang_names = {"en": "English", "de": "German", "fr": "French", "ru": "Russian", "tr": "Turkish", "nl": "Dutch", "sv": "Swedish", "el": "Greek"}
        
        if language == "ar":
            prompt = """اختر آية قرآنية ملهمة ومؤثرة. أعطني:
1. نص الآية بالعربية
2. اسم السورة
3. رقم الآية

أجب بصيغة JSON فقط:
{"text": "نص الآية", "surah": "اسم السورة", "ayah": رقم_الآية}"""
        else:
            lang_name = lang_names.get(language, "English")
            prompt = f"""Select an inspiring Quran verse. Give me:
1. The Arabic text of the verse
2. The {lang_name} translation of the verse
3. The Surah name in {lang_name} transliteration (e.g., "At-Talaq", "Al-Baqarah")
4. The Ayah number

Reply ONLY in JSON:
{{"text": "Arabic verse text", "translation": "{lang_name} translation", "surah": "Surah name in {lang_name}", "ayah": ayah_number}}"""
        
        response = await chat.chat([UserMessage(content=prompt)])
        import re
        match = re.search(r'\{[^}]+\}', response.content)
        if match:
            data = json_module.loads(match.group())
            return {"verse": data}
    except Exception as e:
        logging.error(f"Verse error: {e}")
    
    # Fallback with translation
    fallback_translations = {
        "en": {"translation": "And whoever fears Allah - He will make for him a way out", "surah": "At-Talaq"},
        "de": {"translation": "Und wer Allah fürchtet, dem wird Er einen Ausweg schaffen", "surah": "At-Talaq"},
        "fr": {"translation": "Et quiconque craint Allah, Il lui donnera une issue", "surah": "At-Talaq"},
        "ru": {"translation": "Тому, кто боится Аллаха, Он создаст выход", "surah": "Ат-Таляк"},
        "tr": {"translation": "Kim Allah'tan korkarsa, Allah ona bir çıkış yolu yaratır", "surah": "Talak"},
        "nl": {"translation": "En wie Allah vreest, Hij zal hem een uitweg verschaffen", "surah": "At-Talaq"},
        "sv": {"translation": "Och den som fruktar Allah, Han ska ge honom en utväg", "surah": "At-Talaq"},
        "el": {"translation": "Και όποιος φοβάται τον Αλλάχ, Αυτός θα του δώσει διέξοδο", "surah": "Ατ-Ταλάκ"},
    }
    fb = fallback_translations.get(language, fallback_translations["en"])
    if language == "ar":
        return {"verse": {"text": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ", "surah": "الطلاق", "ayah": 3}}
    return {"verse": {"text": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ", "translation": fb["translation"], "surah": fb["surah"], "ayah": 3}}

@api_router.get("/ai/hadith-of-day")
async def get_hadith_of_day(language: str = Query("ar")):
    """Get AI-selected hadith of the day with translation"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY).with_model("gemini", "gemini-2.0-flash")
        
        lang_names = {"en": "English", "de": "German", "fr": "French", "ru": "Russian", "tr": "Turkish", "nl": "Dutch", "sv": "Swedish", "el": "Greek"}
        
        if language == "ar":
            prompt = """اختر حديث نبوي صحيح ومشهور. أعطني:
1. نص الحديث مختصر
2. اسم الراوي
3. المصدر (البخاري/مسلم/الترمذي...)

أجب بصيغة JSON فقط:
{"text": "نص الحديث", "narrator": "اسم الراوي", "source": "المصدر"}"""
        else:
            lang_name = lang_names.get(language, "English")
            prompt = f"""Select a famous authentic hadith of Prophet Muhammad (PBUH). Give me:
1. The Arabic text of the hadith (short)
2. The {lang_name} translation
3. The narrator name in {lang_name}
4. The source in {lang_name} (e.g., "Sahih Bukhari", "Sahih Muslim")

Reply ONLY in JSON:
{{"text": "Arabic hadith text", "translation": "{lang_name} translation", "narrator": "Narrator in {lang_name}", "source": "Source in {lang_name}"}}"""
        
        response = await chat.chat([UserMessage(content=prompt)])
        import re
        match = re.search(r'\{[^}]+\}', response.content)
        if match:
            data = json_module.loads(match.group())
            return {"hadith": data}
    except Exception as e:
        logging.error(f"Hadith error: {e}")
    
    fallback_translations = {
        "en": {"translation": "The best of you are those who learn the Quran and teach it", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "de": {"translation": "Die Besten unter euch sind diejenigen, die den Quran lernen und lehren", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "fr": {"translation": "Les meilleurs d'entre vous sont ceux qui apprennent le Coran et l'enseignent", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "ru": {"translation": "Лучшие из вас те, кто изучает Коран и обучает ему", "narrator": "Усман ибн Аффан", "source": "Сахих Бухари"},
        "tr": {"translation": "Sizin en hayırlınız Kuran'ı öğrenen ve öğretendir", "narrator": "Osman bin Affan", "source": "Sahih Buhari"},
        "nl": {"translation": "De besten onder jullie zijn degenen die de Koran leren en onderwijzen", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "sv": {"translation": "De bästa bland er är de som lär sig Koranen och lär ut den", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "el": {"translation": "Οι καλύτεροι από εσάς είναι αυτοί που μαθαίνουν το Κοράνι και το διδάσκουν", "narrator": "Ουθμάν ιμπν Αφφάν", "source": "Σαχίχ Μπουχάρι"},
    }
    fb = fallback_translations.get(language, fallback_translations.get("en", {}))
    if language == "ar":
        return {"hadith": {"text": "خيركم من تعلم القرآن وعلمه", "narrator": "عثمان بن عفان", "source": "صحيح البخاري"}}
    return {"hadith": {"text": "خيركم من تعلم القرآن وعلمه", "translation": fb.get("translation", ""), "narrator": fb.get("narrator", "Uthman ibn Affan"), "source": fb.get("source", "Sahih Bukhari")}}

# ==================== VOICE SEARCH AI (بحث صوتي ذكي) ====================

@api_router.post("/stories/voice-search")
async def voice_search_stories(data: dict, user: dict = Depends(get_user)):
    """AI-powered voice search - analyzes query and finds matching stories"""
    query_text = data.get("query", "").strip()
    if not query_text:
        return {"stories": [], "ai_response": ""}
    
    # Use Gemini to understand the query and extract search terms
    ai_response = ""
    search_terms = [query_text]
    
    try:
        gemini_key = os.environ.get("GEMINI_API_KEY", "")
        if gemini_key:
            import httpx
            prompt = f"""أنت مساعد بحث في تطبيق إسلامي. المستخدم يبحث عن: "{query_text}"

استخرج كلمات البحث الرئيسية من هذا الطلب وأعطني:
1. قائمة بـ 3-5 كلمات مفتاحية للبحث (مفصولة بفاصلة)
2. رد قصير ومفيد للمستخدم

أجب بصيغة JSON فقط:
{{"keywords": ["كلمة1", "كلمة2"], "response": "رد قصير"}}"""
            
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}",
                    json={"contents": [{"parts": [{"text": prompt}]}]}
                )
                if resp.status_code == 200:
                    text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                    import re as re_module
                    json_match = re_module.search(r'\{.*\}', text, re_module.DOTALL)
                    if json_match:
                        import json as json_module
                        parsed = json_module.loads(json_match.group())
                        search_terms = parsed.get("keywords", [query_text])
                        ai_response = parsed.get("response", "")
    except Exception as e:
        logging.error(f"Voice search AI error: {e}")
    
    # Search stories using extracted keywords
    or_conditions = []
    for term in search_terms:
        term = term.strip()
        if term:
            regex = {"$regex": term, "$options": "i"}
            or_conditions.extend([{"title": regex}, {"content": regex}, {"author_name": regex}, {"category": regex}])
    
    if not or_conditions:
        or_conditions = [{"title": {"$regex": query_text, "$options": "i"}}, {"content": {"$regex": query_text, "$options": "i"}}]
    
    query_filter = {"is_story": True, "$or": or_conditions}
    cursor = db.posts.find(query_filter, {"_id": 0}).sort("views_count", -1).limit(30)
    stories = await cursor.to_list(length=30)
    
    # Add likes/comments counts
    post_ids = [s["id"] for s in stories]
    if post_ids:
        likes_counts = {}
        async for doc in db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            likes_counts[doc["_id"]] = doc["c"]
        comments_counts = {}
        async for doc in db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            comments_counts[doc["_id"]] = doc["c"]
        for s in stories:
            s["likes_count"] = likes_counts.get(s["id"], 0)
            s["comments_count"] = comments_counts.get(s["id"], 0)
            s["liked"] = False
            s["saved"] = False
    
    return {"stories": stories, "ai_response": ai_response, "keywords": search_terms}

# ==================== ADMIN MANAGEMENT (إدارة التطبيق) ====================

ADMIN_EMAILS = ['mohammadalrejab@gmail.com']

@api_router.get("/admin/stats")
async def admin_stats(user: dict = Depends(get_user)):
    """Get admin dashboard statistics"""
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or (admin.get("email") not in ADMIN_EMAILS and not admin.get("is_admin")):
        raise HTTPException(403, "غير مصرح")
    
    total_users = await db.users.count_documents({})
    total_stories = await db.posts.count_documents({"is_story": True})
    total_posts = await db.posts.count_documents({})
    total_donations = await db.donations.count_documents({})
    total_contacts = await db.contact_messages.count_documents({})
    
    # Latest categories with counts
    pipeline = [
        {"$match": {"is_story": True}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    categories = []
    async for doc in db.posts.aggregate(pipeline):
        categories.append({"category": doc["_id"], "count": doc["count"]})
    
    return {
        "total_users": total_users,
        "total_stories": total_stories,
        "total_posts": total_posts,
        "total_donations": total_donations,
        "total_contacts": total_contacts,
        "categories": categories
    }

@api_router.get("/admin/contacts")
async def admin_contacts(user: dict = Depends(get_user), limit: int = 50):
    """Get contact messages for admin"""
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or (admin.get("email") not in ADMIN_EMAILS and not admin.get("is_admin")):
        raise HTTPException(403, "غير مصرح")
    
    docs = await db.contact_messages.find({}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    return {"contacts": docs}

@api_router.get("/donations/list")
async def list_donations(limit: int = 50):
    """List donation requests"""
    docs = await db.donations.find({"active": True}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    return {"donations": docs}

@api_router.post("/donations/create")
async def create_donation(data: dict, user: dict = Depends(get_user)):
    """Create a donation request"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    doc = {
        "id": str(uuid.uuid4())[:8],
        "author_id": user["id"],
        "author_name": user.get("name", "مستخدم"),
        "title": data.get("title", ""),
        "description": data.get("description", ""),
        "contact_info": data.get("contact_info", ""),
        "amount_needed": data.get("amount_needed", ""),
        "category": data.get("category", "general"),
        "active": True,
        "created_at": datetime.utcnow().isoformat()
    }
    await db.donations.insert_one(doc)
    doc.pop("_id", None)
    return {"donation": doc}

@app.on_event("startup")
async def create_indexes():
    """Create MongoDB indexes for performance"""
    try:
        await db.posts.create_index([("created_at", -1)])
        await db.posts.create_index([("category", 1), ("created_at", -1)])
        await db.posts.create_index("author_id")
        await db.likes.create_index([("post_id", 1), ("user_id", 1)], unique=True)
        await db.saves.create_index([("post_id", 1), ("user_id", 1)], unique=True)
        await db.comments.create_index([("post_id", 1), ("created_at", 1)])
        await db.follows.create_index([("follower_id", 1), ("following_id", 1)], unique=True)
        await db.users.create_index("email", unique=True)
        await db.users.create_index("id", unique=True)
        await db.wallets.create_index("user_id", unique=True)
        await db.gold_transactions.create_index([("user_id", 1), ("created_at", -1)])
        await db.store_items.create_index("category")
        await db.purchases.create_index([("user_id", 1), ("created_at", -1)])
        await db.memberships.create_index("user_id", unique=True)
        await db.posts.create_index([("is_story", 1), ("views_count", -1)])
        await db.posts.create_index([("is_story", 1), ("category", 1)])
        await db.embed_content.create_index([("active", 1), ("created_at", -1)])
        await db.donation_requests.create_index([("created_at", -1)])
        await db.donation_requests.create_index([("status", 1)])
    except Exception as e:
        print(f"Index creation note: {e}")

# ==================== P2P DONATIONS (تبرعات مباشرة) ====================

@api_router.post("/donation-requests/create")
async def create_donation_request(data: dict, user: dict = Depends(get_user)):
    """Create a donation request (محتاج ينشر طلب)"""
    doc = {
        "id": str(uuid.uuid4())[:8],
        "user_id": user["id"],
        "user_name": user.get("name", "مجهول"),
        "title": data.get("title", ""),
        "description": data.get("description", ""),
        "contact_method": data.get("contact_method", ""),
        "contact_info": data.get("contact_info", ""),
        "amount_needed": data.get("amount_needed", ""),
        "category": data.get("category", "عام"),
        "status": "active",
        "created_at": datetime.utcnow().isoformat(),
        "views_count": 0
    }
    await db.donation_requests.insert_one(doc)
    doc.pop("_id", None)
    return {"request": doc}

@api_router.get("/donation-requests/list")
async def list_donation_requests(status: str = "active", limit: int = 30, page: int = 1):
    """List donation requests (عرض طلبات التبرع)"""
    skip = (page - 1) * limit
    query = {"status": status} if status != "all" else {}
    cursor = db.donation_requests.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    requests = await cursor.to_list(length=limit)
    total = await db.donation_requests.count_documents(query)
    return {"requests": requests, "total": total, "has_more": total > skip + limit}

@api_router.post("/donation-requests/{req_id}/contact")
async def contact_donor(req_id: str, data: dict, user: dict = Depends(get_user)):
    """Record that a donor wants to help (متبرع يتواصل)"""
    req = await db.donation_requests.find_one({"id": req_id})
    if not req:
        raise HTTPException(404, "الطلب غير موجود")
    
    contact_doc = {
        "id": str(uuid.uuid4())[:8],
        "request_id": req_id,
        "donor_id": user["id"],
        "donor_name": user.get("name", ""),
        "message": data.get("message", ""),
        "created_at": datetime.utcnow().isoformat()
    }
    await db.donation_contacts.insert_one(contact_doc)
    # Increment view count
    await db.donation_requests.update_one({"id": req_id}, {"$inc": {"views_count": 1}})
    return {"success": True, "contact_info": req.get("contact_info", ""), "message": "تم التواصل بنجاح، تواصل مع المحتاج مباشرة"}

# ==================== SEED CONTENT (محتوى تأسيسي) ====================

SEED_STORIES = {
    "istighfar": [
        {"title": "قصة استغفار الرجل الفقير", "content": "كان رجل فقير يعاني من ضيق الرزق، فنصحه عالم بكثرة الاستغفار. فلزم الاستغفار ليلاً ونهاراً، فما مضت أشهر حتى فتح الله عليه أبواب الرزق من حيث لا يحتسب. قال تعالى: فقلت استغفروا ربكم إنه كان غفاراً يرسل السماء عليكم مدراراً."},
        {"title": "الاستغفار وشفاء المريض", "content": "رُوي أن رجلاً شكا إلى الحسن البصري الجدب، فقال له: استغفر الله. وشكا إليه آخر الفقر فقال: استغفر الله. وشكا إليه ثالث قلة الولد فقال: استغفر الله. فقيل له: عجباً! يشتكون أموراً مختلفة وتأمرهم بشيء واحد! فتلا قوله تعالى: فقلت استغفروا ربكم إنه كان غفاراً."},
        {"title": "التائب من الذنب كمن لا ذنب له", "content": "جاء رجل إلى النبي صلى الله عليه وسلم فقال: يا رسول الله، إني أذنبت ذنباً عظيماً فهل لي من توبة؟ فقال: هل لك من أم؟ قال: لا. قال: هل لك من خالة؟ قال: نعم. قال: فبرّها. وفي رواية أخرى قال: التائب من الذنب كمن لا ذنب له."},
        {"title": "فضل الاستغفار بالأسحار", "content": "كان السلف الصالح يحرصون على الاستغفار في وقت السحر، فقد قال الله تعالى: والمستغفرين بالأسحار. وكان الإمام أحمد بن حنبل يقوم في الثلث الأخير من الليل يستغفر الله ويدعوه، حتى عُرف عنه أنه كان يستغفر الله أكثر من ألف مرة في اليوم."},
        {"title": "الاستغفار طريق الجنة", "content": "قال رسول الله صلى الله عليه وسلم: من لزم الاستغفار جعل الله له من كل همّ فرجاً، ومن كل ضيق مخرجاً، ورزقه من حيث لا يحتسب. فالاستغفار مفتاح الفرج والرزق والبركة في الحياة."},
    ],
    "sahaba": [
        {"title": "بلال بن رباح ومعاناة التوحيد", "content": "بلال بن رباح رضي الله عنه، أول مؤذن في الإسلام. عُذّب عذاباً شديداً في سبيل الله. كان أمية بن خلف يُلقيه على الرمال المحرقة ويضع الصخرة العظيمة على صدره، وبلال يقول: أحد أحد. حتى اشتراه أبو بكر الصديق وأعتقه لوجه الله."},
        {"title": "خالد بن الوليد سيف الله", "content": "خالد بن الوليد رضي الله عنه، سيف الله المسلول. لم يُهزم في معركة قط. قاد المسلمين في معركة مؤتة بعد استشهاد القادة الثلاثة، وقاد معركة اليرموك التي هزم فيها الروم. قال وهو على فراش الموت: ما في جسدي موضع شبر إلا وفيه ضربة سيف أو طعنة رمح، وها أنا أموت على فراشي كما يموت البعير."},
        {"title": "أبو بكر الصديق أول من آمن", "content": "أبو بكر الصديق رضي الله عنه، أول من آمن من الرجال، وصاحب النبي في الهجرة. أنفق كل ماله في سبيل الله. قال عنه النبي صلى الله عليه وسلم: ما نفعني مال قط ما نفعني مال أبي بكر. وكان يبكي عند تلاوة القرآن رحمة وخشوعاً."},
        {"title": "عمر بن الخطاب الفاروق", "content": "عمر بن الخطاب رضي الله عنه، الفاروق الذي فرّق الله به بين الحق والباطل. كان يتفقد رعيته بالليل، وذات ليلة سمع امرأة تبكي وأولادها جياع، فحمل على ظهره كيس الدقيق من بيت المال وطبخ لهم بنفسه حتى شبعوا."},
        {"title": "عثمان بن عفان ذو النورين", "content": "عثمان بن عفان رضي الله عنه، تزوج ابنتي النبي رقية ثم أم كلثوم. جهّز جيش العسرة بألف بعير كاملة العتاد. اشترى بئر رومة وجعلها وقفاً للمسلمين. كان كثير الحياء حتى قال عنه النبي: ألا أستحي ممن تستحي منه الملائكة."},
    ],
    "quran": [
        {"title": "فضل سورة البقرة", "content": "سورة البقرة أطول سور القرآن الكريم وفيها آية الكرسي التي هي أعظم آية في القرآن. قال النبي صلى الله عليه وسلم: اقرأوا سورة البقرة فإن أخذها بركة وتركها حسرة ولا تستطيعها البطلة. وفيها خواتيم سورة البقرة التي من قرأهما في ليلة كفتاه."},
        {"title": "معجزة حفظ القرآن", "content": "القرآن الكريم هو الكتاب الوحيد الذي حُفظ في الصدور والسطور منذ أكثر من 1400 سنة دون تغيير حرف واحد. يحفظه الملايين حول العالم من مختلف الأعمار والجنسيات. قال تعالى: إنا نحن نزلنا الذكر وإنا له لحافظون."},
        {"title": "الشفاء في القرآن", "content": "القرآن شفاء للأبدان والأرواح. قال تعالى: وننزل من القرآن ما هو شفاء ورحمة للمؤمنين. وقد ثبت عن النبي صلى الله عليه وسلم أنه كان يرقي نفسه بالمعوذات، وأمر بالرقية بالقرآن."},
        {"title": "فضل قراءة القرآن يومياً", "content": "قال النبي صلى الله عليه وسلم: اقرأوا القرآن فإنه يأتي يوم القيامة شفيعاً لأصحابه. وقال: الذي يقرأ القرآن وهو ماهر به مع السفرة الكرام البررة، والذي يقرأه وهو يتتعتع فيه وهو عليه شاق له أجران."},
        {"title": "قصة أصحاب الكهف", "content": "أصحاب الكهف فتية آمنوا بربهم وهربوا من ملك ظالم يأمرهم بعبادة الأصنام. لجأوا إلى كهف فضرب الله على آذانهم ثلاثمائة سنين وازدادوا تسعاً. قصتهم عبرة في الثبات على الإيمان والتوكل على الله."},
    ],
    "prophets": [
        {"title": "صبر أيوب عليه السلام", "content": "ابتلى الله نبيه أيوب عليه السلام بفقد المال والولد والمرض الشديد، فصبر صبراً جميلاً. مكث في البلاء سنوات طويلة، ولم يشكُ إلا لله. فلما دعا ربه: أني مسني الضر وأنت أرحم الراحمين، كشف الله ضره وآتاه أهله ومثلهم معهم."},
        {"title": "يوسف عليه السلام من البئر إلى العرش", "content": "ألقاه إخوته في البئر وهو صغير، ثم بيع عبداً في مصر، ثم سُجن ظلماً سنوات. لكنه صبر وتوكل على الله، فرفعه الله حتى صار عزيز مصر. قصته أحسن القصص كما وصفها الله في القرآن."},
        {"title": "إبراهيم خليل الرحمن", "content": "إبراهيم عليه السلام حطّم الأصنام وواجه قومه وحده. ألقوه في النار فقال: حسبي الله ونعم الوكيل. فجعلها الله برداً وسلاماً عليه. وابتلاه الله بذبح ابنه إسماعيل فامتثل، ففداه الله بذبح عظيم."},
        {"title": "موسى عليه السلام وفرعون", "content": "نشأ موسى في قصر فرعون، ثم أرسله الله لدعوة فرعون للتوحيد. واجه الطغيان بالحجة والمعجزات. شقّ الله له البحر فعبر بقومه، وأغرق فرعون وجنوده. درس عظيم في أن الحق يعلو مهما طال الباطل."},
        {"title": "نوح عليه السلام وصبره ألف سنة", "content": "دعا نوح قومه ألف سنة إلا خمسين عاماً. صبر على أذاهم وسخريتهم. لم يؤمن معه إلا قليل. أمره الله ببناء السفينة فبناها وسط سخرية قومه. ثم جاء الطوفان فأهلك الكافرين ونجا نوح ومن معه."},
    ],
    "ruqyah": [
        {"title": "الرقية بآية الكرسي", "content": "آية الكرسي من أعظم آيات الرقية الشرعية. قال النبي صلى الله عليه وسلم: من قرأ آية الكرسي دبر كل صلاة مكتوبة لم يمنعه من دخول الجنة إلا أن يموت. وهي حفظ من الشياطين والعين والحسد."},
        {"title": "المعوذات للحفظ والرقية", "content": "سورة الإخلاص والفلق والناس من أعظم سور الرقية. كان النبي صلى الله عليه وسلم ينفث بهن كل ليلة ويمسح بهن جسده. ثلاث مرات صباحاً ومساءً كافية بإذن الله للحفظ من كل سوء."},
        {"title": "الرقية من العين والحسد", "content": "العين حق كما أخبر النبي صلى الله عليه وسلم. ومن أعظم ما يُرقى به: بسم الله أرقيك، من كل شيء يؤذيك، من شر كل نفس أو عين حاسد الله يشفيك. والمحافظة على أذكار الصباح والمساء حصن منيع."},
        {"title": "رقية المريض بالقرآن", "content": "كان النبي صلى الله عليه وسلم يعود المريض ويقرأ عليه. من ذلك: اللهم رب الناس أذهب الباس واشف أنت الشافي لا شفاء إلا شفاؤك شفاء لا يغادر سقماً. والرقية بالفاتحة شفاء بإذن الله."},
        {"title": "حصن المسلم من الأذكار", "content": "أذكار الصباح والمساء هي حصن المسلم اليومي. بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء وهو السميع العليم (3 مرات). أعوذ بكلمات الله التامات من شر ما خلق (3 مرات). هذه الأذكار وقاية من كل شر بإذن الله."},
    ],
    "rizq": [
        {"title": "أسباب سعة الرزق", "content": "من أعظم أسباب الرزق: التقوى والتوكل على الله. قال تعالى: ومن يتق الله يجعل له مخرجاً ويرزقه من حيث لا يحتسب. وصلة الرحم تزيد في الرزق والعمر. والاستغفار والصدقة من أعظم مفاتيح الرزق."},
        {"title": "قصة المرأة التي تصدقت", "content": "كانت امرأة فقيرة لا تملك إلا رغيفاً واحداً، فجاءها سائل فأعطته نصفه. ثم جاءها آخر فأعطته النصف الثاني. فلما أصبحت وجدت على بابها طعاماً كثيراً. الصدقة لا تنقص المال بل تزيده وتبارك فيه."},
        {"title": "التوكل على الله والأخذ بالأسباب", "content": "قال النبي صلى الله عليه وسلم: لو أنكم توكلتم على الله حق توكله لرزقكم كما يرزق الطير، تغدو خماصاً وتروح بطاناً. الطير تغدو تبحث عن رزقها لا تجلس في عشها، فالتوكل يجمع بين الإيمان والعمل."},
        {"title": "بركة المال الحلال", "content": "المال الحلال فيه بركة من الله وإن كان قليلاً. والمال الحرام ممحوق البركة وإن كان كثيراً. قال النبي: إن الله طيب لا يقبل إلا طيباً. فاطلب الرزق الحلال تجد البركة والسعادة في حياتك."},
        {"title": "فضل الصدقة في الرزق", "content": "قال النبي صلى الله عليه وسلم: ما نقصت صدقة من مال. وقال تعالى: وما أنفقتم من شيء فهو يخلفه وهو خير الرازقين. الصدقة تدفع البلاء وتجلب الرزق وتُظلّ صاحبها يوم القيامة."},
    ],
    "tawba": [
        {"title": "باب التوبة مفتوح", "content": "قال النبي صلى الله عليه وسلم: إن الله يبسط يده بالليل ليتوب مسيء النهار ويبسط يده بالنهار ليتوب مسيء الليل حتى تطلع الشمس من مغربها. باب التوبة مفتوح دائماً فلا تؤخر توبتك."},
        {"title": "قصة الرجل الذي قتل مئة نفس", "content": "كان رجل قتل تسعة وتسعين نفساً ثم أراد التوبة، فسأل عالماً فأخبره أن باب التوبة مفتوح. فخرج يريد أرض صالحة ليتوب فيها، فمات في الطريق. فاختصمت فيه ملائكة الرحمة وملائكة العذاب، فقاس الله الأرض فكان أقرب لأرض التوبة، فأخذته ملائكة الرحمة."},
        {"title": "فرح الله بتوبة العبد", "content": "قال النبي صلى الله عليه وسلم: لله أفرح بتوبة عبده من رجل بأرض فلاة دويّة مهلكة، معه راحلته عليها طعامه وشرابه، فأضلها، فأتى شجرة فاضطجع في ظلها، فبينما هو كذلك إذا بها قائمة عنده. فرح الله بالتائب أشد من فرح هذا الرجل."},
        {"title": "شروط التوبة الصادقة", "content": "التوبة النصوح لها شروط: الإقلاع عن الذنب فوراً، والندم على ما فات، والعزم على عدم العودة. وإذا كان الذنب يتعلق بحق آدمي فلا بد من رد المظالم. ومن أعظم ثمرات التوبة أن الله يبدل السيئات حسنات."},
        {"title": "لا تقنط من رحمة الله", "content": "قال تعالى: قل يا عبادي الذين أسرفوا على أنفسهم لا تقنطوا من رحمة الله إن الله يغفر الذنوب جميعاً إنه هو الغفور الرحيم. مهما بلغت ذنوبك فرحمة الله أوسع. ومن أعظم الذنوب القنوط من رحمة الله."},
    ],
    "miracles": [
        {"title": "انشقاق القمر", "content": "من معجزات النبي صلى الله عليه وسلم انشقاق القمر. طلب منه المشركون آية فأشار إلى القمر فانشق نصفين حتى رأوا الجبل بينهما. قال تعالى: اقتربت الساعة وانشق القمر. وهذه المعجزة رآها أهل مكة بأعينهم."},
        {"title": "الإسراء والمعراج", "content": "أُسري بالنبي صلى الله عليه وسلم من المسجد الحرام إلى المسجد الأقصى، ثم عُرج به إلى السماوات العُلى حتى سمع صريف الأقلام. هناك فُرضت الصلوات الخمس. رحلة عظيمة تؤكد مكانة النبي عند ربه."},
        {"title": "نبع الماء من بين أصابعه", "content": "في غزوة الحديبية عطش الناس ولم يكن معهم ماء إلا إناء صغير. فوضع النبي يده في الإناء فجعل الماء ينبع من بين أصابعه حتى شرب الجيش كله. كرّمه الله بمعجزات تثبت صدق نبوته."},
        {"title": "حنين الجذع", "content": "كان النبي يخطب إلى جذع نخلة، فلما صُنع له المنبر ترك الجذع. فسمع الناس من الجذع صوتاً كصوت البعير يحنّ. فنزل النبي من المنبر فاحتضنه حتى سكن. حتى الجمادات تشتاق لرسول الله."},
        {"title": "إطعام الجيش من طعام قليل", "content": "في غزوة الخندق كان الجوع شديداً. دعا جابر بن عبدالله النبي وبضعة نفر لطعام قليل. فدعا النبي أهل الخندق جميعاً فأكلوا حتى شبعوا والطعام كما هو. بركة النبي لا تُحدّ."},
    ],
    "general": [
        {"title": "فضل الصلاة على النبي", "content": "قال النبي صلى الله عليه وسلم: من صلى عليّ صلاة واحدة صلى الله عليه بها عشراً. وقال: أولى الناس بي يوم القيامة أكثرهم عليّ صلاة. اللهم صلّ وسلّم وبارك على نبينا محمد وعلى آله وصحبه أجمعين."},
        {"title": "أهمية صلاة الفجر", "content": "قال النبي صلى الله عليه وسلم: ركعتا الفجر خير من الدنيا وما فيها. ومن صلى الفجر في جماعة فهو في ذمة الله. فلا تُضيّع صلاة الفجر فهي مفتاح يومك وبركة حياتك."},
        {"title": "فضل ذكر الله", "content": "قال تعالى: ألا بذكر الله تطمئن القلوب. وقال النبي: مثل الذي يذكر ربه والذي لا يذكره مثل الحي والميت. فاجعل لسانك رطباً بذكر الله في كل وقت وحين."},
        {"title": "بر الوالدين أعظم العبادات", "content": "سُئل النبي: أي العمل أحب إلى الله؟ قال: الصلاة على وقتها. قيل: ثم أي؟ قال: بر الوالدين. رضا الله في رضا الوالدين، وسخطه في سخطهما. فاحرص على برهما في حياتهما وبعد مماتهما."},
        {"title": "أخلاق المسلم", "content": "قال النبي صلى الله عليه وسلم: إنما بُعثت لأتمم مكارم الأخلاق. وقال: أكمل المؤمنين إيماناً أحسنهم خُلقاً. الخُلق الحسن يثقل الميزان يوم القيامة ويرفع درجات العبد في الجنة."},
    ],
}

@api_router.post("/admin/seed-content")
async def seed_content(user: dict = Depends(get_user)):
    """Seed real Islamic stories into the database - Admin only"""
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or (admin.get("email") not in ADMIN_EMAILS and not admin.get("is_admin")):
        raise HTTPException(403, "غير مصرح")
    
    total_created = 0
    for category, stories_list in SEED_STORIES.items():
        # Check how many exist in this category
        existing = await db.posts.count_documents({"is_story": True, "category": category})
        needed = max(0, 10 - existing)  # Seed up to 10 unique per category for initial load
        
        for i, story in enumerate(stories_list[:needed]):
            # Check duplicate by title
            exists = await db.posts.find_one({"title": story["title"], "is_story": True})
            if exists:
                continue
            
            doc = {
                "id": str(uuid.uuid4())[:8],
                "content": story["content"],
                "title": story["title"],
                "author_id": user["id"],
                "author_name": admin.get("name", "إدارة التطبيق"),
                "author_avatar": admin.get("avatar_url", ""),
                "category": category,
                "media_url": "",
                "media_type": "text",
                "is_embed": False,
                "embed_url": "",
                "is_story": True,
                "views_count": random.randint(50, 500),
                "likes_count": random.randint(5, 100),
                "comments_count": random.randint(1, 30),
                "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 90))).isoformat(),
                "auto_category": category
            }
            await db.posts.insert_one(doc)
            total_created += 1
    
    return {"success": True, "created": total_created, "message": f"تم إنشاء {total_created} قصة جديدة"}


# ==================== ARABIC ACADEMY ====================

ARABIC_LETTERS = [
    {"id": 1, "letter": "ا", "name_ar": "ألف", "name_en": "Alif", "transliteration": "a", "form_isolated": "ا", "form_initial": "ا", "form_medial": "ـا", "form_final": "ـا", "example_word": "أسد", "example_meaning": "Lion", "audio_hint": "ah"},
    {"id": 2, "letter": "ب", "name_ar": "باء", "name_en": "Ba", "transliteration": "b", "form_isolated": "ب", "form_initial": "بـ", "form_medial": "ـبـ", "form_final": "ـب", "example_word": "بيت", "example_meaning": "House", "audio_hint": "bah"},
    {"id": 3, "letter": "ت", "name_ar": "تاء", "name_en": "Ta", "transliteration": "t", "form_isolated": "ت", "form_initial": "تـ", "form_medial": "ـتـ", "form_final": "ـت", "example_word": "تفاح", "example_meaning": "Apple", "audio_hint": "tah"},
    {"id": 4, "letter": "ث", "name_ar": "ثاء", "name_en": "Tha", "transliteration": "th", "form_isolated": "ث", "form_initial": "ثـ", "form_medial": "ـثـ", "form_final": "ـث", "example_word": "ثعلب", "example_meaning": "Fox", "audio_hint": "thah"},
    {"id": 5, "letter": "ج", "name_ar": "جيم", "name_en": "Jim", "transliteration": "j", "form_isolated": "ج", "form_initial": "جـ", "form_medial": "ـجـ", "form_final": "ـج", "example_word": "جمل", "example_meaning": "Camel", "audio_hint": "jeem"},
    {"id": 6, "letter": "ح", "name_ar": "حاء", "name_en": "Ha", "transliteration": "ḥ", "form_isolated": "ح", "form_initial": "حـ", "form_medial": "ـحـ", "form_final": "ـح", "example_word": "حصان", "example_meaning": "Horse", "audio_hint": "hah"},
    {"id": 7, "letter": "خ", "name_ar": "خاء", "name_en": "Kha", "transliteration": "kh", "form_isolated": "خ", "form_initial": "خـ", "form_medial": "ـخـ", "form_final": "ـخ", "example_word": "خروف", "example_meaning": "Sheep", "audio_hint": "khah"},
    {"id": 8, "letter": "د", "name_ar": "دال", "name_en": "Dal", "transliteration": "d", "form_isolated": "د", "form_initial": "د", "form_medial": "ـد", "form_final": "ـد", "example_word": "ديك", "example_meaning": "Rooster", "audio_hint": "daal"},
    {"id": 9, "letter": "ذ", "name_ar": "ذال", "name_en": "Dhal", "transliteration": "dh", "form_isolated": "ذ", "form_initial": "ذ", "form_medial": "ـذ", "form_final": "ـذ", "example_word": "ذئب", "example_meaning": "Wolf", "audio_hint": "dhaal"},
    {"id": 10, "letter": "ر", "name_ar": "راء", "name_en": "Ra", "transliteration": "r", "form_isolated": "ر", "form_initial": "ر", "form_medial": "ـر", "form_final": "ـر", "example_word": "رمان", "example_meaning": "Pomegranate", "audio_hint": "raa"},
    {"id": 11, "letter": "ز", "name_ar": "زاي", "name_en": "Zay", "transliteration": "z", "form_isolated": "ز", "form_initial": "ز", "form_medial": "ـز", "form_final": "ـز", "example_word": "زهرة", "example_meaning": "Flower", "audio_hint": "zaay"},
    {"id": 12, "letter": "س", "name_ar": "سين", "name_en": "Sin", "transliteration": "s", "form_isolated": "س", "form_initial": "سـ", "form_medial": "ـسـ", "form_final": "ـس", "example_word": "سمك", "example_meaning": "Fish", "audio_hint": "seen"},
    {"id": 13, "letter": "ش", "name_ar": "شين", "name_en": "Shin", "transliteration": "sh", "form_isolated": "ش", "form_initial": "شـ", "form_medial": "ـشـ", "form_final": "ـش", "example_word": "شمس", "example_meaning": "Sun", "audio_hint": "sheen"},
    {"id": 14, "letter": "ص", "name_ar": "صاد", "name_en": "Sad", "transliteration": "ṣ", "form_isolated": "ص", "form_initial": "صـ", "form_medial": "ـصـ", "form_final": "ـص", "example_word": "صقر", "example_meaning": "Falcon", "audio_hint": "saad"},
    {"id": 15, "letter": "ض", "name_ar": "ضاد", "name_en": "Dad", "transliteration": "ḍ", "form_isolated": "ض", "form_initial": "ضـ", "form_medial": "ـضـ", "form_final": "ـض", "example_word": "ضفدع", "example_meaning": "Frog", "audio_hint": "daad"},
    {"id": 16, "letter": "ط", "name_ar": "طاء", "name_en": "Tah", "transliteration": "ṭ", "form_isolated": "ط", "form_initial": "طـ", "form_medial": "ـطـ", "form_final": "ـط", "example_word": "طائر", "example_meaning": "Bird", "audio_hint": "taa"},
    {"id": 17, "letter": "ظ", "name_ar": "ظاء", "name_en": "Zah", "transliteration": "ẓ", "form_isolated": "ظ", "form_initial": "ظـ", "form_medial": "ـظـ", "form_final": "ـظ", "example_word": "ظبي", "example_meaning": "Gazelle", "audio_hint": "zhaa"},
    {"id": 18, "letter": "ع", "name_ar": "عين", "name_en": "Ain", "transliteration": "'", "form_isolated": "ع", "form_initial": "عـ", "form_medial": "ـعـ", "form_final": "ـع", "example_word": "عنب", "example_meaning": "Grapes", "audio_hint": "ain"},
    {"id": 19, "letter": "غ", "name_ar": "غين", "name_en": "Ghain", "transliteration": "gh", "form_isolated": "غ", "form_initial": "غـ", "form_medial": "ـغـ", "form_final": "ـغ", "example_word": "غزال", "example_meaning": "Deer", "audio_hint": "ghain"},
    {"id": 20, "letter": "ف", "name_ar": "فاء", "name_en": "Fa", "transliteration": "f", "form_isolated": "ف", "form_initial": "فـ", "form_medial": "ـفـ", "form_final": "ـف", "example_word": "فيل", "example_meaning": "Elephant", "audio_hint": "faa"},
    {"id": 21, "letter": "ق", "name_ar": "قاف", "name_en": "Qaf", "transliteration": "q", "form_isolated": "ق", "form_initial": "قـ", "form_medial": "ـقـ", "form_final": "ـق", "example_word": "قمر", "example_meaning": "Moon", "audio_hint": "qaaf"},
    {"id": 22, "letter": "ك", "name_ar": "كاف", "name_en": "Kaf", "transliteration": "k", "form_isolated": "ك", "form_initial": "كـ", "form_medial": "ـكـ", "form_final": "ـك", "example_word": "كتاب", "example_meaning": "Book", "audio_hint": "kaaf"},
    {"id": 23, "letter": "ل", "name_ar": "لام", "name_en": "Lam", "transliteration": "l", "form_isolated": "ل", "form_initial": "لـ", "form_medial": "ـلـ", "form_final": "ـل", "example_word": "ليمون", "example_meaning": "Lemon", "audio_hint": "laam"},
    {"id": 24, "letter": "م", "name_ar": "ميم", "name_en": "Mim", "transliteration": "m", "form_isolated": "م", "form_initial": "مـ", "form_medial": "ـمـ", "form_final": "ـم", "example_word": "مسجد", "example_meaning": "Mosque", "audio_hint": "meem"},
    {"id": 25, "letter": "ن", "name_ar": "نون", "name_en": "Nun", "transliteration": "n", "form_isolated": "ن", "form_initial": "نـ", "form_medial": "ـنـ", "form_final": "ـن", "example_word": "نجمة", "example_meaning": "Star", "audio_hint": "noon"},
    {"id": 26, "letter": "ه", "name_ar": "هاء", "name_en": "Ha2", "transliteration": "h", "form_isolated": "ه", "form_initial": "هـ", "form_medial": "ـهـ", "form_final": "ـه", "example_word": "هلال", "example_meaning": "Crescent", "audio_hint": "haa"},
    {"id": 27, "letter": "و", "name_ar": "واو", "name_en": "Waw", "transliteration": "w", "form_isolated": "و", "form_initial": "و", "form_medial": "ـو", "form_final": "ـو", "example_word": "وردة", "example_meaning": "Rose", "audio_hint": "waaw"},
    {"id": 28, "letter": "ي", "name_ar": "ياء", "name_en": "Ya", "transliteration": "y", "form_isolated": "ي", "form_initial": "يـ", "form_medial": "ـيـ", "form_final": "ـي", "example_word": "يد", "example_meaning": "Hand", "audio_hint": "yaa"},
]

QURAN_VOCAB = [
    {"id": 1, "word": "بِسْمِ", "transliteration": "Bismi", "meaning": "In the name of", "surah": "Al-Fatiha", "ayah": 1},
    {"id": 2, "word": "اللَّهِ", "transliteration": "Allah", "meaning": "God", "surah": "Al-Fatiha", "ayah": 1},
    {"id": 3, "word": "الرَّحْمَنِ", "transliteration": "Ar-Rahman", "meaning": "The Most Gracious", "surah": "Al-Fatiha", "ayah": 1},
    {"id": 4, "word": "الرَّحِيمِ", "transliteration": "Ar-Raheem", "meaning": "The Most Merciful", "surah": "Al-Fatiha", "ayah": 1},
    {"id": 5, "word": "الْحَمْدُ", "transliteration": "Al-Hamdu", "meaning": "All praise", "surah": "Al-Fatiha", "ayah": 2},
    {"id": 6, "word": "رَبِّ", "transliteration": "Rabbi", "meaning": "Lord of", "surah": "Al-Fatiha", "ayah": 2},
    {"id": 7, "word": "الْعَالَمِينَ", "transliteration": "Al-Alameen", "meaning": "The Worlds", "surah": "Al-Fatiha", "ayah": 2},
    {"id": 8, "word": "مَالِكِ", "transliteration": "Maliki", "meaning": "Master of", "surah": "Al-Fatiha", "ayah": 4},
    {"id": 9, "word": "يَوْمِ", "transliteration": "Yawmi", "meaning": "Day of", "surah": "Al-Fatiha", "ayah": 4},
    {"id": 10, "word": "الدِّينِ", "transliteration": "Ad-Deen", "meaning": "Judgment", "surah": "Al-Fatiha", "ayah": 4},
    {"id": 11, "word": "إِيَّاكَ", "transliteration": "Iyyaka", "meaning": "You alone", "surah": "Al-Fatiha", "ayah": 5},
    {"id": 12, "word": "نَعْبُدُ", "transliteration": "Na'budu", "meaning": "We worship", "surah": "Al-Fatiha", "ayah": 5},
    {"id": 13, "word": "نَسْتَعِينُ", "transliteration": "Nasta'een", "meaning": "We seek help", "surah": "Al-Fatiha", "ayah": 5},
    {"id": 14, "word": "اهْدِنَا", "transliteration": "Ihdina", "meaning": "Guide us", "surah": "Al-Fatiha", "ayah": 6},
    {"id": 15, "word": "الصِّرَاطَ", "transliteration": "As-Sirat", "meaning": "The path", "surah": "Al-Fatiha", "ayah": 6},
    {"id": 16, "word": "الْمُسْتَقِيمَ", "transliteration": "Al-Mustaqeem", "meaning": "The straight", "surah": "Al-Fatiha", "ayah": 6},
    {"id": 17, "word": "جَنَّة", "transliteration": "Jannah", "meaning": "Paradise", "surah": "Various", "ayah": 0},
    {"id": 18, "word": "صَلَاة", "transliteration": "Salah", "meaning": "Prayer", "surah": "Various", "ayah": 0},
    {"id": 19, "word": "زَكَاة", "transliteration": "Zakah", "meaning": "Charity", "surah": "Various", "ayah": 0},
    {"id": 20, "word": "صِيَام", "transliteration": "Siyam", "meaning": "Fasting", "surah": "Various", "ayah": 0},
]

LIVE_STREAMS = [
    {
        "id": "makkah",
        "name_ar": "بث مباشر من مكة المكرمة",
        "name_en": "Makkah Live",
        "name_de": "Mekka Live",
        "name_ru": "Мекка в прямом эфире",
        "name_fr": "La Mecque en direct",
        "name_tr": "Mekke Canlı",
        "name_sv": "Mecka Live",
        "name_nl": "Mekka Live",
        "name_el": "Μέκκα Ζωντανά",
        "youtube_channel": "SaudiQuranTv",
        "embed_id": "gAzq1ch5RnY",
        "thumbnail": "https://i.ytimg.com/vi/gAzq1ch5RnY/maxresdefault_live.jpg",
        "city": "Makkah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True
    },
    {
        "id": "madinah",
        "name_ar": "بث مباشر من المدينة المنورة",
        "name_en": "Madinah Live",
        "name_de": "Medina Live",
        "name_ru": "Медина в прямом эфире",
        "name_fr": "Médine en direct",
        "name_tr": "Medine Canlı",
        "name_sv": "Medina Live",
        "name_nl": "Medina Live",
        "name_el": "Μεδίνα Ζωντανά",
        "youtube_channel": "SaudiSunnahTv",
        "embed_id": "VO359jOBfCk",
        "thumbnail": "https://i.ytimg.com/vi/VO359jOBfCk/maxresdefault_live.jpg",
        "city": "Madinah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True
    },
    {
        "id": "alaqsa",
        "name_ar": "بث مباشر من المسجد الأقصى",
        "name_en": "Al-Aqsa Mosque Live",
        "name_de": "Al-Aqsa-Moschee Live",
        "name_ru": "Мечеть Аль-Акса в прямом эфире",
        "name_fr": "Mosquée Al-Aqsa en direct",
        "name_tr": "Mescid-i Aksa Canlı",
        "name_sv": "Al-Aqsa-moskén Live",
        "name_nl": "Al-Aqsa Moskee Live",
        "name_el": "Τζαμί Αλ-Άκσα Ζωντανά",
        "youtube_channel": "AlAqsaTV",
        "embed_id": "jBYrnVptmCo",
        "thumbnail": "https://i.ytimg.com/vi/jBYrnVptmCo/maxresdefault_live.jpg",
        "city": "Jerusalem",
        "country": "Palestine",
        "category": "holy",
        "is_247": True
    },
    {
        "id": "umayyad",
        "name_ar": "بث مباشر من الجامع الأموي",
        "name_en": "Umayyad Mosque Live",
        "name_de": "Umayyaden-Moschee Live",
        "name_ru": "Мечеть Омейядов в прямом эфире",
        "name_fr": "Mosquée des Omeyyades en direct",
        "name_tr": "Emevi Camii Canlı",
        "name_sv": "Umayyadmoskén Live",
        "name_nl": "Umayyad Moskee Live",
        "name_el": "Τζαμί Ομεϋάδ Ζωντανά",
        "youtube_channel": "UmayyadMosque",
        "embed_id": "wQMmHBBl3cA",
        "thumbnail": "https://i.ytimg.com/vi/wQMmHBBl3cA/maxresdefault_live.jpg",
        "city": "Damascus",
        "country": "Syria",
        "category": "historic",
        "is_247": False
    },
    {
        "id": "cologne",
        "name_ar": "بث مباشر من مسجد كولونيا الكبير",
        "name_en": "Cologne Central Mosque Live",
        "name_de": "DITIB-Zentralmoschee Köln Live",
        "name_ru": "Центральная мечеть Кёльна в прямом эфире",
        "name_fr": "Mosquée centrale de Cologne en direct",
        "name_tr": "Köln Merkez Camii Canlı",
        "name_sv": "Kölns Centralmoské Live",
        "name_nl": "Centrale Moskee Keulen Live",
        "name_el": "Κεντρικό Τζαμί Κολωνίας Ζωντανά",
        "youtube_channel": "DitibCologne",
        "embed_id": "o4N9vYUFHzA",
        "thumbnail": "https://i.ytimg.com/vi/o4N9vYUFHzA/maxresdefault_live.jpg",
        "city": "Cologne",
        "country": "Germany",
        "category": "europe",
        "is_247": False
    }
]

@api_router.get("/arabic-academy/letters")
async def get_arabic_letters():
    """Get all 28 Arabic letters with forms and examples"""
    return {"success": True, "letters": ARABIC_LETTERS, "total": len(ARABIC_LETTERS)}

@api_router.get("/arabic-academy/vocab")
async def get_quran_vocab():
    """Get Quranic vocabulary words"""
    return {"success": True, "words": QURAN_VOCAB, "total": len(QURAN_VOCAB)}

@api_router.get("/arabic-academy/daily-word")
async def get_daily_word():
    """Get a daily Quranic word based on day of year"""
    day_of_year = datetime.utcnow().timetuple().tm_yday
    word = QURAN_VOCAB[day_of_year % len(QURAN_VOCAB)]
    return {"success": True, "word": word}

@api_router.get("/arabic-academy/progress/{user_id}")
async def get_academy_progress(user_id: str):
    """Get user's Arabic Academy progress"""
    progress = await db.arabic_progress.find_one({"user_id": user_id})
    if not progress:
        progress = {
            "user_id": user_id,
            "completed_letters": [],
            "completed_vocab": [],
            "stars": 0,
            "streak": 0,
            "total_xp": 0,
            "level": 1,
            "golden_bricks": 0,
            "last_activity": None
        }
    progress.pop("_id", None)
    return {"success": True, "progress": progress}

@api_router.post("/arabic-academy/progress")
async def save_academy_progress(data: dict):
    """Save user's Arabic Academy progress"""
    user_id = data.get("user_id", "guest")
    update_data = {
        "user_id": user_id,
        "completed_letters": data.get("completed_letters", []),
        "completed_vocab": data.get("completed_vocab", []),
        "stars": data.get("stars", 0),
        "streak": data.get("streak", 0),
        "total_xp": data.get("total_xp", 0),
        "level": data.get("level", 1),
        "golden_bricks": data.get("golden_bricks", 0),
        "last_activity": datetime.utcnow().isoformat()
    }
    await db.arabic_progress.update_one(
        {"user_id": user_id},
        {"$set": update_data},
        upsert=True
    )
    return {"success": True, "message": "Progress saved"}

@api_router.get("/arabic-academy/quiz/{letter_id}")
async def get_letter_quiz(letter_id: int):
    """Get quiz for a specific letter"""
    letter = next((lt for lt in ARABIC_LETTERS if lt["id"] == letter_id), None)
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")
    
    other_letters = [lt for lt in ARABIC_LETTERS if lt["id"] != letter_id]
    wrong_answers = random.sample(other_letters, min(3, len(other_letters)))
    
    options = [{"letter": letter["letter"], "name_ar": letter["name_ar"], "name_en": letter["name_en"], "correct": True}]
    for w in wrong_answers:
        options.append({"letter": w["letter"], "name_ar": w["name_ar"], "name_en": w["name_en"], "correct": False})
    random.shuffle(options)
    
    return {
        "success": True,
        "quiz": {
            "question_letter": letter,
            "options": options,
            "type": "identify"
        }
    }

# ==================== CURRICULUM 90-DAY ====================

ARABIC_NUMBERS = [
    {"id": i, "number": i, "arabic": n[0], "word_ar": n[1], "word_en": n[2], "transliteration": n[3]}
    for i, n in enumerate([
        ("٠", "صفر", "Zero", "Sifr"), ("١", "واحد", "One", "Wahid"), ("٢", "اثنان", "Two", "Ithnan"),
        ("٣", "ثلاثة", "Three", "Thalatha"), ("٤", "أربعة", "Four", "Arba'a"), ("٥", "خمسة", "Five", "Khamsa"),
        ("٦", "ستة", "Six", "Sitta"), ("٧", "سبعة", "Seven", "Sab'a"), ("٨", "ثمانية", "Eight", "Thamaniya"),
        ("٩", "تسعة", "Nine", "Tis'a"), ("١٠", "عشرة", "Ten", "Ashara"),
        ("٢٠", "عشرون", "Twenty", "Ishrun"), ("٣٠", "ثلاثون", "Thirty", "Thalathun"),
        ("٤٠", "أربعون", "Forty", "Arba'un"), ("٥٠", "خمسون", "Fifty", "Khamsun"),
        ("١٠٠", "مائة", "Hundred", "Mi'a"), ("١٠٠٠", "ألف", "Thousand", "Alf"),
    ], start=0)
]

VOCAB_CATEGORIES = {
    "animals": [
        {"id": "a1", "word": "قِطَّة", "transliteration": "Qitta", "meaning_en": "Cat", "meaning_de": "Katze", "meaning_fr": "Chat", "meaning_tr": "Kedi", "meaning_ru": "Кошка", "emoji": "🐱"},
        {"id": "a2", "word": "كَلْب", "transliteration": "Kalb", "meaning_en": "Dog", "meaning_de": "Hund", "meaning_fr": "Chien", "meaning_tr": "Köpek", "meaning_ru": "Собака", "emoji": "🐕"},
        {"id": "a3", "word": "أَسَد", "transliteration": "Asad", "meaning_en": "Lion", "meaning_de": "Löwe", "meaning_fr": "Lion", "meaning_tr": "Aslan", "meaning_ru": "Лев", "emoji": "🦁"},
        {"id": "a4", "word": "فِيل", "transliteration": "Fiil", "meaning_en": "Elephant", "meaning_de": "Elefant", "meaning_fr": "Éléphant", "meaning_tr": "Fil", "meaning_ru": "Слон", "emoji": "🐘"},
        {"id": "a5", "word": "طَائِر", "transliteration": "Taa'ir", "meaning_en": "Bird", "meaning_de": "Vogel", "meaning_fr": "Oiseau", "meaning_tr": "Kuş", "meaning_ru": "Птица", "emoji": "🐦"},
        {"id": "a6", "word": "سَمَكَة", "transliteration": "Samaka", "meaning_en": "Fish", "meaning_de": "Fisch", "meaning_fr": "Poisson", "meaning_tr": "Balık", "meaning_ru": "Рыба", "emoji": "🐟"},
        {"id": "a7", "word": "حِصَان", "transliteration": "Hisan", "meaning_en": "Horse", "meaning_de": "Pferd", "meaning_fr": "Cheval", "meaning_tr": "At", "meaning_ru": "Лошадь", "emoji": "🐴"},
        {"id": "a8", "word": "أَرْنَب", "transliteration": "Arnab", "meaning_en": "Rabbit", "meaning_de": "Kaninchen", "meaning_fr": "Lapin", "meaning_tr": "Tavşan", "meaning_ru": "Кролик", "emoji": "🐰"},
        {"id": "a9", "word": "بَقَرَة", "transliteration": "Baqara", "meaning_en": "Cow", "meaning_de": "Kuh", "meaning_fr": "Vache", "meaning_tr": "İnek", "meaning_ru": "Корова", "emoji": "🐄"},
        {"id": "a10", "word": "خَرُوف", "transliteration": "Kharuf", "meaning_en": "Sheep", "meaning_de": "Schaf", "meaning_fr": "Mouton", "meaning_tr": "Koyun", "meaning_ru": "Овца", "emoji": "🐑"},
    ],
    "food": [
        {"id": "f1", "word": "تُفَّاحَة", "transliteration": "Tuffaha", "meaning_en": "Apple", "meaning_de": "Apfel", "meaning_fr": "Pomme", "meaning_tr": "Elma", "meaning_ru": "Яблоко", "emoji": "🍎"},
        {"id": "f2", "word": "مَوْز", "transliteration": "Mawz", "meaning_en": "Banana", "meaning_de": "Banane", "meaning_fr": "Banane", "meaning_tr": "Muz", "meaning_ru": "Банан", "emoji": "🍌"},
        {"id": "f3", "word": "خُبْز", "transliteration": "Khubz", "meaning_en": "Bread", "meaning_de": "Brot", "meaning_fr": "Pain", "meaning_tr": "Ekmek", "meaning_ru": "Хлеб", "emoji": "🍞"},
        {"id": "f4", "word": "مَاء", "transliteration": "Maa'", "meaning_en": "Water", "meaning_de": "Wasser", "meaning_fr": "Eau", "meaning_tr": "Su", "meaning_ru": "Вода", "emoji": "💧"},
        {"id": "f5", "word": "حَلِيب", "transliteration": "Haleeb", "meaning_en": "Milk", "meaning_de": "Milch", "meaning_fr": "Lait", "meaning_tr": "Süt", "meaning_ru": "Молоко", "emoji": "🥛"},
        {"id": "f6", "word": "أُرْز", "transliteration": "Urz", "meaning_en": "Rice", "meaning_de": "Reis", "meaning_fr": "Riz", "meaning_tr": "Pirinç", "meaning_ru": "Рис", "emoji": "🍚"},
        {"id": "f7", "word": "بَيْض", "transliteration": "Bayd", "meaning_en": "Eggs", "meaning_de": "Eier", "meaning_fr": "Œufs", "meaning_tr": "Yumurta", "meaning_ru": "Яйца", "emoji": "🥚"},
        {"id": "f8", "word": "عَسَل", "transliteration": "Asal", "meaning_en": "Honey", "meaning_de": "Honig", "meaning_fr": "Miel", "meaning_tr": "Bal", "meaning_ru": "Мёд", "emoji": "🍯"},
        {"id": "f9", "word": "بُرْتُقَالَة", "transliteration": "Burtuqala", "meaning_en": "Orange", "meaning_de": "Orange", "meaning_fr": "Orange", "meaning_tr": "Portakal", "meaning_ru": "Апельсин", "emoji": "🍊"},
        {"id": "f10", "word": "عِنَب", "transliteration": "Inab", "meaning_en": "Grapes", "meaning_de": "Trauben", "meaning_fr": "Raisins", "meaning_tr": "Üzüm", "meaning_ru": "Виноград", "emoji": "🍇"},
    ],
    "body": [
        {"id": "b1", "word": "رَأْس", "transliteration": "Ra's", "meaning_en": "Head", "meaning_de": "Kopf", "meaning_fr": "Tête", "meaning_tr": "Baş", "meaning_ru": "Голова", "emoji": "🗣️"},
        {"id": "b2", "word": "يَد", "transliteration": "Yad", "meaning_en": "Hand", "meaning_de": "Hand", "meaning_fr": "Main", "meaning_tr": "El", "meaning_ru": "Рука", "emoji": "✋"},
        {"id": "b3", "word": "عَيْن", "transliteration": "Ayn", "meaning_en": "Eye", "meaning_de": "Auge", "meaning_fr": "Œil", "meaning_tr": "Göz", "meaning_ru": "Глаз", "emoji": "👁️"},
        {"id": "b4", "word": "أُذُن", "transliteration": "Udhun", "meaning_en": "Ear", "meaning_de": "Ohr", "meaning_fr": "Oreille", "meaning_tr": "Kulak", "meaning_ru": "Ухо", "emoji": "👂"},
        {"id": "b5", "word": "قَلْب", "transliteration": "Qalb", "meaning_en": "Heart", "meaning_de": "Herz", "meaning_fr": "Cœur", "meaning_tr": "Kalp", "meaning_ru": "Сердце", "emoji": "❤️"},
        {"id": "b6", "word": "قَدَم", "transliteration": "Qadam", "meaning_en": "Foot", "meaning_de": "Fuß", "meaning_fr": "Pied", "meaning_tr": "Ayak", "meaning_ru": "Нога", "emoji": "🦶"},
        {"id": "b7", "word": "أَنْف", "transliteration": "Anf", "meaning_en": "Nose", "meaning_de": "Nase", "meaning_fr": "Nez", "meaning_tr": "Burun", "meaning_ru": "Нос", "emoji": "👃"},
        {"id": "b8", "word": "فَم", "transliteration": "Fam", "meaning_en": "Mouth", "meaning_de": "Mund", "meaning_fr": "Bouche", "meaning_tr": "Ağız", "meaning_ru": "Рот", "emoji": "👄"},
    ],
    "family": [
        {"id": "fm1", "word": "أَب", "transliteration": "Ab", "meaning_en": "Father", "meaning_de": "Vater", "meaning_fr": "Père", "meaning_tr": "Baba", "meaning_ru": "Отец", "emoji": "👨"},
        {"id": "fm2", "word": "أُمّ", "transliteration": "Umm", "meaning_en": "Mother", "meaning_de": "Mutter", "meaning_fr": "Mère", "meaning_tr": "Anne", "meaning_ru": "Мать", "emoji": "👩"},
        {"id": "fm3", "word": "أَخ", "transliteration": "Akh", "meaning_en": "Brother", "meaning_de": "Bruder", "meaning_fr": "Frère", "meaning_tr": "Kardeş", "meaning_ru": "Брат", "emoji": "👦"},
        {"id": "fm4", "word": "أُخْت", "transliteration": "Ukht", "meaning_en": "Sister", "meaning_de": "Schwester", "meaning_fr": "Sœur", "meaning_tr": "Kız kardeş", "meaning_ru": "Сестра", "emoji": "👧"},
        {"id": "fm5", "word": "جَدّ", "transliteration": "Jadd", "meaning_en": "Grandfather", "meaning_de": "Großvater", "meaning_fr": "Grand-père", "meaning_tr": "Dede", "meaning_ru": "Дед", "emoji": "👴"},
        {"id": "fm6", "word": "جَدَّة", "transliteration": "Jadda", "meaning_en": "Grandmother", "meaning_de": "Großmutter", "meaning_fr": "Grand-mère", "meaning_tr": "Nine", "meaning_ru": "Бабушка", "emoji": "👵"},
        {"id": "fm7", "word": "طِفْل", "transliteration": "Tifl", "meaning_en": "Child", "meaning_de": "Kind", "meaning_fr": "Enfant", "meaning_tr": "Çocuk", "meaning_ru": "Ребёнок", "emoji": "👶"},
        {"id": "fm8", "word": "عَائِلَة", "transliteration": "Aa'ila", "meaning_en": "Family", "meaning_de": "Familie", "meaning_fr": "Famille", "meaning_tr": "Aile", "meaning_ru": "Семья", "emoji": "👨‍👩‍👧‍👦"},
    ],
    "nature": [
        {"id": "n1", "word": "شَمْس", "transliteration": "Shams", "meaning_en": "Sun", "meaning_de": "Sonne", "meaning_fr": "Soleil", "meaning_tr": "Güneş", "meaning_ru": "Солнце", "emoji": "☀️"},
        {"id": "n2", "word": "قَمَر", "transliteration": "Qamar", "meaning_en": "Moon", "meaning_de": "Mond", "meaning_fr": "Lune", "meaning_tr": "Ay", "meaning_ru": "Луна", "emoji": "🌙"},
        {"id": "n3", "word": "نَجْمَة", "transliteration": "Najma", "meaning_en": "Star", "meaning_de": "Stern", "meaning_fr": "Étoile", "meaning_tr": "Yıldız", "meaning_ru": "Звезда", "emoji": "⭐"},
        {"id": "n4", "word": "سَمَاء", "transliteration": "Samaa'", "meaning_en": "Sky", "meaning_de": "Himmel", "meaning_fr": "Ciel", "meaning_tr": "Gökyüzü", "meaning_ru": "Небо", "emoji": "🌤️"},
        {"id": "n5", "word": "مَطَر", "transliteration": "Matar", "meaning_en": "Rain", "meaning_de": "Regen", "meaning_fr": "Pluie", "meaning_tr": "Yağmur", "meaning_ru": "Дождь", "emoji": "🌧️"},
        {"id": "n6", "word": "بَحْر", "transliteration": "Bahr", "meaning_en": "Sea", "meaning_de": "Meer", "meaning_fr": "Mer", "meaning_tr": "Deniz", "meaning_ru": "Море", "emoji": "🌊"},
        {"id": "n7", "word": "جَبَل", "transliteration": "Jabal", "meaning_en": "Mountain", "meaning_de": "Berg", "meaning_fr": "Montagne", "meaning_tr": "Dağ", "meaning_ru": "Гора", "emoji": "⛰️"},
        {"id": "n8", "word": "شَجَرَة", "transliteration": "Shajara", "meaning_en": "Tree", "meaning_de": "Baum", "meaning_fr": "Arbre", "meaning_tr": "Ağaç", "meaning_ru": "Дерево", "emoji": "🌳"},
        {"id": "n9", "word": "زَهْرَة", "transliteration": "Zahra", "meaning_en": "Flower", "meaning_de": "Blume", "meaning_fr": "Fleur", "meaning_tr": "Çiçek", "meaning_ru": "Цветок", "emoji": "🌸"},
        {"id": "n10", "word": "أَرْض", "transliteration": "Ard", "meaning_en": "Earth", "meaning_de": "Erde", "meaning_fr": "Terre", "meaning_tr": "Toprak", "meaning_ru": "Земля", "emoji": "🌍"},
    ],
    "colors": [
        {"id": "c1", "word": "أَحْمَر", "transliteration": "Ahmar", "meaning_en": "Red", "meaning_de": "Rot", "meaning_fr": "Rouge", "meaning_tr": "Kırmızı", "meaning_ru": "Красный", "emoji": "🔴"},
        {"id": "c2", "word": "أَزْرَق", "transliteration": "Azraq", "meaning_en": "Blue", "meaning_de": "Blau", "meaning_fr": "Bleu", "meaning_tr": "Mavi", "meaning_ru": "Синий", "emoji": "🔵"},
        {"id": "c3", "word": "أَخْضَر", "transliteration": "Akhdar", "meaning_en": "Green", "meaning_de": "Grün", "meaning_fr": "Vert", "meaning_tr": "Yeşil", "meaning_ru": "Зелёный", "emoji": "🟢"},
        {"id": "c4", "word": "أَصْفَر", "transliteration": "Asfar", "meaning_en": "Yellow", "meaning_de": "Gelb", "meaning_fr": "Jaune", "meaning_tr": "Sarı", "meaning_ru": "Жёлтый", "emoji": "🟡"},
        {"id": "c5", "word": "أَبْيَض", "transliteration": "Abyad", "meaning_en": "White", "meaning_de": "Weiß", "meaning_fr": "Blanc", "meaning_tr": "Beyaz", "meaning_ru": "Белый", "emoji": "⚪"},
        {"id": "c6", "word": "أَسْوَد", "transliteration": "Aswad", "meaning_en": "Black", "meaning_de": "Schwarz", "meaning_fr": "Noir", "meaning_tr": "Siyah", "meaning_ru": "Чёрный", "emoji": "⚫"},
        {"id": "c7", "word": "بُرْتُقَالِي", "transliteration": "Burtuqali", "meaning_en": "Orange", "meaning_de": "Orange", "meaning_fr": "Orange", "meaning_tr": "Turuncu", "meaning_ru": "Оранжевый", "emoji": "🟠"},
        {"id": "c8", "word": "بَنَفْسَجِي", "transliteration": "Banafsaji", "meaning_en": "Purple", "meaning_de": "Lila", "meaning_fr": "Violet", "meaning_tr": "Mor", "meaning_ru": "Фиолетовый", "emoji": "🟣"},
    ],
    "home": [
        {"id": "h1", "word": "بَيْت", "transliteration": "Bayt", "meaning_en": "House", "meaning_de": "Haus", "meaning_fr": "Maison", "meaning_tr": "Ev", "meaning_ru": "Дом", "emoji": "🏠"},
        {"id": "h2", "word": "بَاب", "transliteration": "Bab", "meaning_en": "Door", "meaning_de": "Tür", "meaning_fr": "Porte", "meaning_tr": "Kapı", "meaning_ru": "Дверь", "emoji": "🚪"},
        {"id": "h3", "word": "كُرْسِي", "transliteration": "Kursi", "meaning_en": "Chair", "meaning_de": "Stuhl", "meaning_fr": "Chaise", "meaning_tr": "Sandalye", "meaning_ru": "Стул", "emoji": "🪑"},
        {"id": "h4", "word": "طَاوِلَة", "transliteration": "Tawila", "meaning_en": "Table", "meaning_de": "Tisch", "meaning_fr": "Table", "meaning_tr": "Masa", "meaning_ru": "Стол", "emoji": "🪵"},
        {"id": "h5", "word": "سَرِير", "transliteration": "Sareer", "meaning_en": "Bed", "meaning_de": "Bett", "meaning_fr": "Lit", "meaning_tr": "Yatak", "meaning_ru": "Кровать", "emoji": "🛏️"},
        {"id": "h6", "word": "نَافِذَة", "transliteration": "Nafidha", "meaning_en": "Window", "meaning_de": "Fenster", "meaning_fr": "Fenêtre", "meaning_tr": "Pencere", "meaning_ru": "Окно", "emoji": "🪟"},
        {"id": "h7", "word": "مَسْجِد", "transliteration": "Masjid", "meaning_en": "Mosque", "meaning_de": "Moschee", "meaning_fr": "Mosquée", "meaning_tr": "Cami", "meaning_ru": "Мечеть", "emoji": "🕌"},
        {"id": "h8", "word": "كِتَاب", "transliteration": "Kitab", "meaning_en": "Book", "meaning_de": "Buch", "meaning_fr": "Livre", "meaning_tr": "Kitap", "meaning_ru": "Книга", "emoji": "📖"},
    ],
    "verbs": [
        {"id": "v1", "word": "كَتَبَ", "transliteration": "Kataba", "meaning_en": "Wrote", "meaning_de": "Schrieb", "meaning_fr": "A écrit", "meaning_tr": "Yazdı", "meaning_ru": "Написал", "emoji": "✍️"},
        {"id": "v2", "word": "قَرَأَ", "transliteration": "Qara'a", "meaning_en": "Read", "meaning_de": "Las", "meaning_fr": "A lu", "meaning_tr": "Okudu", "meaning_ru": "Читал", "emoji": "📖"},
        {"id": "v3", "word": "أَكَلَ", "transliteration": "Akala", "meaning_en": "Ate", "meaning_de": "Aß", "meaning_fr": "A mangé", "meaning_tr": "Yedi", "meaning_ru": "Ел", "emoji": "🍽️"},
        {"id": "v4", "word": "شَرِبَ", "transliteration": "Shariba", "meaning_en": "Drank", "meaning_de": "Trank", "meaning_fr": "A bu", "meaning_tr": "İçti", "meaning_ru": "Пил", "emoji": "🥤"},
        {"id": "v5", "word": "ذَهَبَ", "transliteration": "Dhahaba", "meaning_en": "Went", "meaning_de": "Ging", "meaning_fr": "Est allé", "meaning_tr": "Gitti", "meaning_ru": "Пошёл", "emoji": "🚶"},
        {"id": "v6", "word": "جَلَسَ", "transliteration": "Jalasa", "meaning_en": "Sat", "meaning_de": "Saß", "meaning_fr": "S'est assis", "meaning_tr": "Oturdu", "meaning_ru": "Сел", "emoji": "🪑"},
        {"id": "v7", "word": "نَامَ", "transliteration": "Nama", "meaning_en": "Slept", "meaning_de": "Schlief", "meaning_fr": "A dormi", "meaning_tr": "Uyudu", "meaning_ru": "Спал", "emoji": "😴"},
        {"id": "v8", "word": "لَعِبَ", "transliteration": "La'iba", "meaning_en": "Played", "meaning_de": "Spielte", "meaning_fr": "A joué", "meaning_tr": "Oynadı", "meaning_ru": "Играл", "emoji": "⚽"},
    ],
    "greetings": [
        {"id": "g1", "word": "السَّلَامُ عَلَيْكُم", "transliteration": "As-Salamu Alaykum", "meaning_en": "Peace be upon you", "meaning_de": "Friede sei mit euch", "meaning_fr": "Paix sur vous", "meaning_tr": "Selamun aleyküm", "meaning_ru": "Мир вам", "emoji": "🤝"},
        {"id": "g2", "word": "صَبَاحُ الْخَيْر", "transliteration": "Sabah Al-Khayr", "meaning_en": "Good morning", "meaning_de": "Guten Morgen", "meaning_fr": "Bonjour", "meaning_tr": "Günaydın", "meaning_ru": "Доброе утро", "emoji": "🌅"},
        {"id": "g3", "word": "مَسَاءُ الْخَيْر", "transliteration": "Masa' Al-Khayr", "meaning_en": "Good evening", "meaning_de": "Guten Abend", "meaning_fr": "Bonsoir", "meaning_tr": "İyi akşamlar", "meaning_ru": "Добрый вечер", "emoji": "🌆"},
        {"id": "g4", "word": "شُكْرًا", "transliteration": "Shukran", "meaning_en": "Thank you", "meaning_de": "Danke", "meaning_fr": "Merci", "meaning_tr": "Teşekkürler", "meaning_ru": "Спасибо", "emoji": "🙏"},
        {"id": "g5", "word": "مَعَ السَّلَامَة", "transliteration": "Ma'a As-Salama", "meaning_en": "Goodbye", "meaning_de": "Auf Wiedersehen", "meaning_fr": "Au revoir", "meaning_tr": "Güle güle", "meaning_ru": "До свидания", "emoji": "👋"},
        {"id": "g6", "word": "مِنْ فَضْلِك", "transliteration": "Min Fadlik", "meaning_en": "Please", "meaning_de": "Bitte", "meaning_fr": "S'il vous plaît", "meaning_tr": "Lütfen", "meaning_ru": "Пожалуйста", "emoji": "😊"},
    ],
}

SENTENCE_TEMPLATES = [
    {"id": "s1", "words_ar": ["أَنَا", "أُحِبُّ", "التُّفَّاح"], "words_en": ["I", "love", "apples"], "sentence_ar": "أَنَا أُحِبُّ التُّفَّاح", "sentence_en": "I love apples", "difficulty": 1},
    {"id": "s2", "words_ar": ["هَذَا", "كِتَاب", "جَمِيل"], "words_en": ["This is", "a book", "beautiful"], "sentence_ar": "هَذَا كِتَاب جَمِيل", "sentence_en": "This is a beautiful book", "difficulty": 1},
    {"id": "s3", "words_ar": ["الْوَلَد", "يَلْعَبُ", "فِي الْحَدِيقَة"], "words_en": ["The boy", "plays", "in the park"], "sentence_ar": "الْوَلَد يَلْعَبُ فِي الْحَدِيقَة", "sentence_en": "The boy plays in the park", "difficulty": 2},
    {"id": "s4", "words_ar": ["ذَهَبْتُ", "إِلَى", "الْمَسْجِد"], "words_en": ["I went", "to", "the mosque"], "sentence_ar": "ذَهَبْتُ إِلَى الْمَسْجِد", "sentence_en": "I went to the mosque", "difficulty": 1},
    {"id": "s5", "words_ar": ["الشَّمْسُ", "سَاطِعَة", "الْيَوْم"], "words_en": ["The sun", "is bright", "today"], "sentence_ar": "الشَّمْسُ سَاطِعَة الْيَوْم", "sentence_en": "The sun is bright today", "difficulty": 2},
    {"id": "s6", "words_ar": ["أُمِّي", "تَطْبَخُ", "طَعَامًا", "لَذِيذًا"], "words_en": ["My mother", "cooks", "food", "delicious"], "sentence_ar": "أُمِّي تَطْبَخُ طَعَامًا لَذِيذًا", "sentence_en": "My mother cooks delicious food", "difficulty": 2},
    {"id": "s7", "words_ar": ["الْقَمَر", "جَمِيل", "فِي اللَّيْل"], "words_en": ["The moon", "is beautiful", "at night"], "sentence_ar": "الْقَمَر جَمِيل فِي اللَّيْل", "sentence_en": "The moon is beautiful at night", "difficulty": 2},
    {"id": "s8", "words_ar": ["بِسْمِ اللَّه", "الرَّحْمَن", "الرَّحِيم"], "words_en": ["In the name of Allah", "the Most Gracious", "the Most Merciful"], "sentence_ar": "بِسْمِ اللَّه الرَّحْمَن الرَّحِيم", "sentence_en": "In the name of Allah, the Most Gracious, the Most Merciful", "difficulty": 1},
    {"id": "s9", "words_ar": ["قَرَأَ", "الطِّفْل", "الْقُرْآن"], "words_en": ["Read", "the child", "the Quran"], "sentence_ar": "قَرَأَ الطِّفْل الْقُرْآن", "sentence_en": "The child read the Quran", "difficulty": 2},
    {"id": "s10", "words_ar": ["الْمَاء", "ضَرُورِيّ", "لِلْحَيَاة"], "words_en": ["Water", "is essential", "for life"], "sentence_ar": "الْمَاء ضَرُورِيّ لِلْحَيَاة", "sentence_en": "Water is essential for life", "difficulty": 3},
]

# Build 90-day curriculum
def build_90_day_curriculum():
    days = []
    day_num = 0
    # Level 1: Alphabet (Days 1-30) - 28 letters + 2 review
    for i, letter in enumerate(ARABIC_LETTERS):
        day_num += 1
        days.append({"day": day_num, "level": 1, "type": "letter", "content_id": letter["id"],
                      "title_en": f"Letter: {letter['name_en']}", "title_ar": f"حرف: {letter['name_ar']}", "xp": 10})
    days.append({"day": 29, "level": 1, "type": "review", "content_id": 0, "title_en": "Alphabet Review 1", "title_ar": "مراجعة الأبجدية ١", "xp": 20})
    days.append({"day": 30, "level": 1, "type": "review", "content_id": 0, "title_en": "Alphabet Review 2", "title_ar": "مراجعة الأبجدية ٢", "xp": 20})
    
    # Level 2: Numbers (Days 31-42)
    for i, num in enumerate(ARABIC_NUMBERS):
        day_num = 31 + i
        if day_num > 42:
            break
        days.append({"day": day_num, "level": 2, "type": "number", "content_id": num["id"],
                      "title_en": f"Number: {num['word_en']}", "title_ar": f"رقم: {num['word_ar']}", "xp": 10})
    
    # Level 3: Vocabulary (Days 43-78)
    all_vocab = []
    for cat_words in VOCAB_CATEGORIES.values():
        all_vocab.extend(cat_words)
    for i in range(36):
        day_num = 43 + i
        vocab_idx = i % len(all_vocab)
        v = all_vocab[vocab_idx]
        days.append({"day": day_num, "level": 3, "type": "vocab", "content_id": v["id"],
                      "title_en": f"Word: {v['meaning_en']}", "title_ar": f"كلمة: {v['word']}", "xp": 10})
    
    # Level 4: Sentences (Days 79-90)
    for i in range(12):
        day_num = 79 + i
        sent_idx = i % len(SENTENCE_TEMPLATES)
        s = SENTENCE_TEMPLATES[sent_idx]
        days.append({"day": day_num, "level": 4, "type": "sentence", "content_id": s["id"],
                      "title_en": f"Sentence: {s['sentence_en'][:30]}...", "title_ar": f"جملة: {s['sentence_ar'][:30]}...", "xp": 15})
    
    return days

CURRICULUM_90 = build_90_day_curriculum()

@api_router.get("/arabic-academy/curriculum")
async def get_curriculum():
    """Get the full 90-day curriculum"""
    return {"success": True, "curriculum": CURRICULUM_90, "total_days": len(CURRICULUM_90)}

@api_router.get("/arabic-academy/curriculum/day/{day}")
async def get_curriculum_day(day: int):
    """Get specific day lesson"""
    lesson = next((d for d in CURRICULUM_90 if d["day"] == day), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Day not found")
    
    content = None
    if lesson["type"] == "letter":
        content = next((lt for lt in ARABIC_LETTERS if lt["id"] == lesson["content_id"]), None)
    elif lesson["type"] == "number":
        content = next((n for n in ARABIC_NUMBERS if n["id"] == lesson["content_id"]), None)
    elif lesson["type"] == "vocab":
        for cat_words in VOCAB_CATEGORIES.values():
            found = next((v for v in cat_words if v["id"] == lesson["content_id"]), None)
            if found:
                content = found
                break
    elif lesson["type"] == "sentence":
        content = next((s for s in SENTENCE_TEMPLATES if s["id"] == lesson["content_id"]), None)
    
    return {"success": True, "lesson": lesson, "content": content}

@api_router.get("/arabic-academy/numbers")
async def get_arabic_numbers():
    """Get all Arabic numbers"""
    return {"success": True, "numbers": ARABIC_NUMBERS, "total": len(ARABIC_NUMBERS)}

@api_router.get("/arabic-academy/vocabulary")
async def get_vocabulary(category: str = "all"):
    """Get vocabulary by category"""
    if category == "all":
        all_words = []
        for cat, words in VOCAB_CATEGORIES.items():
            for w in words:
                all_words.append({**w, "category": cat})
        return {"success": True, "words": all_words, "total": len(all_words), "categories": list(VOCAB_CATEGORIES.keys())}
    elif category in VOCAB_CATEGORIES:
        words = [{**w, "category": category} for w in VOCAB_CATEGORIES[category]]
        return {"success": True, "words": words, "total": len(words), "categories": list(VOCAB_CATEGORIES.keys())}
    raise HTTPException(status_code=404, detail="Category not found")

@api_router.get("/arabic-academy/sentences")
async def get_sentences(difficulty: int = 0):
    """Get sentence building templates"""
    sentences = SENTENCE_TEMPLATES
    if difficulty > 0:
        sentences = [s for s in sentences if s["difficulty"] == difficulty]
    return {"success": True, "sentences": sentences, "total": len(sentences)}

@api_router.post("/arabic-academy/progress-v2")
async def save_progress_v2(data: dict):
    """Save enhanced progress with growth tree and day tracking"""
    user_id = data.get("user_id", "guest")
    update = {
        "user_id": user_id,
        "completed_days": data.get("completed_days", []),
        "completed_letters": data.get("completed_letters", []),
        "completed_numbers": data.get("completed_numbers", []),
        "completed_vocab": data.get("completed_vocab", []),
        "completed_sentences": data.get("completed_sentences", []),
        "stars": data.get("stars", 0),
        "total_xp": data.get("total_xp", 0),
        "golden_bricks": data.get("golden_bricks", 0),
        "tree_level": data.get("tree_level", 1),
        "streak": data.get("streak", 0),
        "last_activity": datetime.utcnow().isoformat(),
    }
    await db.arabic_progress.update_one({"user_id": user_id}, {"$set": update}, upsert=True)
    return {"success": True, "message": "Progress saved"}

@api_router.get("/arabic-academy/progress-v2/{user_id}")
async def get_progress_v2(user_id: str):
    """Get enhanced progress"""
    progress = await db.arabic_progress.find_one({"user_id": user_id})
    if not progress:
        progress = {
            "user_id": user_id, "completed_days": [], "completed_letters": [], "completed_numbers": [],
            "completed_vocab": [], "completed_sentences": [], "stars": 0, "total_xp": 0,
            "golden_bricks": 0, "tree_level": 1, "streak": 0, "last_activity": None
        }
    progress.pop("_id", None)
    return {"success": True, "progress": progress}

# ==================== LIVE STREAMS (MongoDB-backed + Admin CRUD) ====================

DEFAULT_STREAMS = [
    {
        "id": str(uuid.uuid4())[:8],
        "name": "Makkah Live - الحرم المكي",
        "embed_type": "channel",
        "embed_value": "UC2l1w7FCuff2-h429sAUSXQ",
        "thumbnail": "",
        "city": "Makkah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True,
        "is_active": True,
        "sort_order": 1
    },
    {
        "id": str(uuid.uuid4())[:8],
        "name": "Madinah Live - المسجد النبوي",
        "embed_type": "video",
        "embed_value": "rHWSRMcGGBQ",
        "thumbnail": "",
        "city": "Madinah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True,
        "is_active": True,
        "sort_order": 2
    },
    {
        "id": str(uuid.uuid4())[:8],
        "name": "Al-Aqsa Mosque Live - المسجد الأقصى",
        "embed_type": "channel",
        "embed_value": "UC2l1w7FCuff2-h429sAUSXQ",
        "thumbnail": "",
        "city": "Jerusalem",
        "country": "Palestine",
        "category": "holy",
        "is_247": True,
        "is_active": True,
        "sort_order": 3
    },
]

@api_router.get("/live-streams")
async def get_live_streams(category: str = "all"):
    """Get available live streams from DB"""
    query = {"is_active": True}
    if category != "all":
        query["category"] = category
    streams_cursor = db.live_streams.find(query).sort("sort_order", 1)
    streams = []
    async for s in streams_cursor:
        s.pop("_id", None)
        # Build embed URL
        if s.get("embed_type") == "channel":
            s["embed_url"] = f"https://www.youtube.com/embed/live_stream?channel={s['embed_value']}"
        else:
            s["embed_url"] = f"https://www.youtube.com/embed/{s['embed_value']}"
        streams.append(s)
    # If no streams in DB, seed defaults
    if not streams and category == "all":
        for ds in DEFAULT_STREAMS:
            await db.live_streams.insert_one({**ds})
        return await get_live_streams(category)
    return {"success": True, "streams": streams, "total": len(streams)}

@api_router.get("/live-streams/{stream_id}")
async def get_live_stream(stream_id: str):
    """Get a specific live stream"""
    stream = await db.live_streams.find_one({"id": stream_id})
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    stream.pop("_id", None)
    if stream.get("embed_type") == "channel":
        stream["embed_url"] = f"https://www.youtube.com/embed/live_stream?channel={stream['embed_value']}"
    else:
        stream["embed_url"] = f"https://www.youtube.com/embed/{stream['embed_value']}"
    return {"success": True, "stream": stream}

# Admin CRUD for Live Streams
@api_router.post("/admin/live-streams")
async def admin_create_stream(data: dict, user: dict = Depends(get_user)):
    """Admin: Add a new live stream"""
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    # Parse embed URL/ID from user input
    embed_input = data.get("embed_url", "").strip()
    embed_type = "video"
    embed_value = embed_input
    
    # Detect embed type from URL
    if "youtube.com/embed/live_stream?channel=" in embed_input:
        embed_type = "channel"
        embed_value = embed_input.split("channel=")[-1].split("&")[0]
    elif "youtube.com/embed/" in embed_input:
        embed_value = embed_input.split("/embed/")[-1].split("?")[0]
    elif "youtube.com/watch?v=" in embed_input:
        embed_value = embed_input.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in embed_input:
        embed_value = embed_input.split("youtu.be/")[-1].split("?")[0]
    elif "youtube.com/channel/" in embed_input:
        embed_type = "channel"
        embed_value = embed_input.split("/channel/")[-1].split("/")[0]
    
    stream = {
        "id": str(uuid.uuid4())[:8],
        "name": data.get("name", "Live Stream"),
        "embed_type": embed_type,
        "embed_value": embed_value,
        "thumbnail": data.get("thumbnail", ""),
        "city": data.get("city", ""),
        "country": data.get("country", ""),
        "category": data.get("category", "other"),
        "is_247": data.get("is_247", False),
        "is_active": True,
        "sort_order": data.get("sort_order", 99),
        "created_at": datetime.utcnow().isoformat(),
        "created_by": user["id"]
    }
    await db.live_streams.insert_one(stream)
    stream.pop("_id", None)
    return {"success": True, "stream": stream}

@api_router.put("/admin/live-streams/{stream_id}")
async def admin_update_stream(stream_id: str, data: dict, user: dict = Depends(get_user)):
    """Admin: Update a live stream"""
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    update = {}
    for field in ["name", "embed_type", "embed_value", "thumbnail", "city", "country", "category", "is_247", "is_active", "sort_order"]:
        if field in data:
            update[field] = data[field]
    
    # Handle embed_url input
    if "embed_url" in data:
        embed_input = data["embed_url"].strip()
        if "youtube.com/embed/live_stream?channel=" in embed_input:
            update["embed_type"] = "channel"
            update["embed_value"] = embed_input.split("channel=")[-1].split("&")[0]
        elif "youtube.com/embed/" in embed_input:
            update["embed_type"] = "video"
            update["embed_value"] = embed_input.split("/embed/")[-1].split("?")[0]
        elif "youtube.com/watch?v=" in embed_input:
            update["embed_type"] = "video"
            update["embed_value"] = embed_input.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in embed_input:
            update["embed_type"] = "video"
            update["embed_value"] = embed_input.split("youtu.be/")[-1].split("?")[0]
    
    if update:
        await db.live_streams.update_one({"id": stream_id}, {"$set": update})
    
    stream = await db.live_streams.find_one({"id": stream_id})
    if stream:
        stream.pop("_id", None)
    return {"success": True, "stream": stream}

@api_router.delete("/admin/live-streams/{stream_id}")
async def admin_delete_stream(stream_id: str, user: dict = Depends(get_user)):
    """Admin: Delete a live stream"""
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    await db.live_streams.delete_one({"id": stream_id})
    return {"success": True, "message": "Stream deleted"}

@api_router.get("/admin/live-streams")
async def admin_list_streams(user: dict = Depends(get_user)):
    """Admin: List all streams (including inactive)"""
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    streams = []
    async for s in db.live_streams.find().sort("sort_order", 1):
        s.pop("_id", None)
        if s.get("embed_type") == "channel":
            s["embed_url"] = f"https://www.youtube.com/embed/live_stream?channel={s['embed_value']}"
        else:
            s["embed_url"] = f"https://www.youtube.com/embed/{s['embed_value']}"
        streams.append(s)
    return {"success": True, "streams": streams, "total": len(streams)}


# ==================== TRANSLATION SERVICE ====================
SUPPORTED_LANGUAGES = ['ar', 'en', 'sv', 'nl', 'el', 'de', 'ru', 'fr', 'tr']
LANGUAGE_NAMES = {
    'ar': 'Arabic', 'en': 'English', 'sv': 'Swedish', 'nl': 'Dutch',
    'el': 'Greek', 'de': 'German', 'ru': 'Russian', 'fr': 'French', 'tr': 'Turkish'
}

async def translate_text_ai(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text using OpenAI GPT with Islamic context."""
    if not EMERGENT_LLM_KEY or source_lang == target_lang:
        return text
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"translate-{uuid.uuid4().hex[:8]}",
            system_message=f"You are an expert Islamic text translator. Translate the given text from {LANGUAGE_NAMES.get(source_lang, source_lang)} to {LANGUAGE_NAMES.get(target_lang, target_lang)}. Preserve Islamic terminology and spiritual meaning. Return ONLY the translated text, nothing else."
        )
        response = await chat.send_message(UserMessage(text=text))
        return response.strip()
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text

@api_router.post("/translate/story")
async def translate_story_content(
    story_id: str = Query(...),
    target_lang: str = Query(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    user: dict = Depends(get_user)
):
    """Translate a story's title and content to the target language and store it."""
    if target_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(400, f"Unsupported language: {target_lang}")
    
    story = await db.posts.find_one({"id": story_id, "is_story": True}, {"_id": 0})
    if not story:
        raise HTTPException(404, "Story not found")
    
    # Check if translation already exists
    existing = story.get("translations", {}).get(target_lang)
    if existing:
        return {"translated": True, "title": existing.get("title", ""), "content": existing.get("content", "")}
    
    # Detect source language (assume Arabic if contains Arabic chars)
    source_lang = "ar" if re.search(r'[\u0600-\u06FF]', story.get("content", "")) else "en"
    
    title = await translate_text_ai(story.get("title", ""), source_lang, target_lang) if story.get("title") else ""
    content = await translate_text_ai(story.get("content", ""), source_lang, target_lang)
    
    # Store translation in DB
    await db.posts.update_one(
        {"id": story_id},
        {"$set": {f"translations.{target_lang}": {"title": title, "content": content}}}
    )
    
    return {"translated": True, "title": title, "content": content}


@api_router.get("/stories/list-translated")
async def list_stories_translated(
    category: str = "all",
    page: int = 1,
    limit: int = 20,
    language: str = Query("ar"),
    user: dict = Depends(get_user)
):
    """List stories with translated content for the requested language."""
    query = {"is_story": True}
    if category != "all":
        query["category"] = category
    skip = (page - 1) * limit
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    stories = await cursor.to_list(length=limit)
    total = await db.posts.count_documents(query)
    
    # Enrich with likes/saves/comments
    post_ids = [s["id"] for s in stories]
    user_id = user["id"] if user else None
    likes_set, saves_set = set(), set()
    if user_id and post_ids:
        ul = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        likes_set = {d["post_id"] for d in ul}
        us = await db.saves.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        saves_set = {d["post_id"] for d in us}
    likes_counts, comments_counts = {}, {}
    if post_ids:
        async for doc in db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            likes_counts[doc["_id"]] = doc["c"]
        async for doc in db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            comments_counts[doc["_id"]] = doc["c"]
    
    for s in stories:
        pid = s["id"]
        s["liked"] = pid in likes_set
        s["saved"] = pid in saves_set
        s["likes_count"] = likes_counts.get(pid, 0)
        s["comments_count"] = comments_counts.get(pid, 0)
        # Apply translation if available and language is not source
        if language != "ar" and language in s.get("translations", {}):
            trans = s["translations"][language]
            s["title"] = trans.get("title", s.get("title", ""))
            s["content"] = trans.get("content", s.get("content", ""))
        s.pop("translations", None)  # Don't send all translations to client
    
    return {"stories": stories, "total": total, "page": page, "has_more": skip + limit < total}


@api_router.post("/stories/batch-translate")
async def batch_translate_stories(
    target_lang: str = Query(...),
    user: dict = Depends(get_user)
):
    """Batch translate all stories to a target language. Admin/background task."""
    if target_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(400, f"Unsupported language: {target_lang}")
    
    # Find stories without this language translation
    stories = await db.posts.find(
        {"is_story": True, f"translations.{target_lang}": {"$exists": False}},
        {"_id": 0, "id": 1, "title": 1, "content": 1}
    ).to_list(100)
    
    if not stories:
        return {"message": f"All stories already translated to {target_lang}", "count": 0}
    
    translated_count = 0
    for story in stories:
        try:
            source_lang = "ar" if re.search(r'[\u0600-\u06FF]', story.get("content", "")) else "en"
            title = await translate_text_ai(story.get("title", ""), source_lang, target_lang) if story.get("title") else ""
            content = await translate_text_ai(story.get("content", ""), source_lang, target_lang)
            await db.posts.update_one(
                {"id": story["id"]},
                {"$set": {f"translations.{target_lang}": {"title": title, "content": content}}}
            )
            translated_count += 1
        except Exception as e:
            logger.error(f"Failed to translate story {story['id']}: {e}")
    
    return {"message": f"Translated {translated_count} stories to {target_lang}", "count": translated_count}



# ==================== KIDS ZONE - INFINITE GAME ENGINE (PCG) ====================

# Confusable phoneme pairs for adaptive difficulty
CONFUSABLE_PHONEMES = [
    (6, 7, "ح", "خ"),   # Ha vs Kha
    (12, 13, "س", "ش"), # Sin vs Shin
    (14, 15, "ص", "ض"), # Sad vs Dad
    (16, 17, "ط", "ظ"), # Tah vs Zah
    (8, 9, "د", "ذ"),   # Dal vs Dhal
    (4, 5, "ث", "ج"),   # Tha vs Jim
    (18, 19, "ع", "غ"), # Ain vs Ghain
    (26, 27, "ه", "و"), # Ha2 vs Waw
    (3, 16, "ت", "ط"),  # Ta vs emphatic Tah
    (8, 15, "د", "ض"),  # Dal vs emphatic Dad
]

# Difficulty tiers with thresholds
DIFFICULTY_TIERS = [
    {"name": "seedling", "min_xp": 0, "choices": 2, "time_bonus": 30, "brick_reward": 1},
    {"name": "sprout", "min_xp": 100, "choices": 3, "time_bonus": 25, "brick_reward": 2},
    {"name": "sapling", "min_xp": 300, "choices": 4, "time_bonus": 20, "brick_reward": 3},
    {"name": "tree", "min_xp": 600, "choices": 4, "time_bonus": 15, "brick_reward": 4},
    {"name": "forest", "min_xp": 1000, "choices": 5, "time_bonus": 12, "brick_reward": 5},
]

# Virtual Mosque building stages
MOSQUE_STAGES = [
    {"stage": 1, "name": "foundation", "bricks_needed": 10, "emoji": "🧱"},
    {"stage": 2, "name": "walls", "bricks_needed": 25, "emoji": "🏗️"},
    {"stage": 3, "name": "dome", "bricks_needed": 50, "emoji": "🕌"},
    {"stage": 4, "name": "minaret", "bricks_needed": 80, "emoji": "🗼"},
    {"stage": 5, "name": "garden", "bricks_needed": 120, "emoji": "🌳"},
    {"stage": 6, "name": "golden_dome", "bricks_needed": 200, "emoji": "✨"},
]

def get_difficulty_tier(total_xp: int) -> dict:
    tier = DIFFICULTY_TIERS[0]
    for t in DIFFICULTY_TIERS:
        if total_xp >= t["min_xp"]:
            tier = t
    return tier

def get_mosque_progress(total_bricks: int) -> dict:
    current_stage = MOSQUE_STAGES[0]
    next_stage = MOSQUE_STAGES[1] if len(MOSQUE_STAGES) > 1 else None
    for i, stage in enumerate(MOSQUE_STAGES):
        if total_bricks >= stage["bricks_needed"]:
            current_stage = stage
            next_stage = MOSQUE_STAGES[i + 1] if i + 1 < len(MOSQUE_STAGES) else None
    return {
        "current_stage": current_stage,
        "next_stage": next_stage,
        "total_bricks": total_bricks,
        "bricks_to_next": (next_stage["bricks_needed"] - total_bricks) if next_stage else 0,
        "progress_pct": min(100, int((total_bricks / (next_stage["bricks_needed"] if next_stage else current_stage["bricks_needed"])) * 100)),
        "stages": MOSQUE_STAGES,
    }


@api_router.get("/kids-zone/generate-game")
async def generate_game(user_id: str = "", game_type: str = "auto", locale: str = "ar"):
    """Procedural Content Generator: generates a game based on user skill gaps."""
    import random
    
    # Get or create user skill profile
    skill = await db.kids_skills.find_one({"user_id": user_id}) if user_id else None
    if not skill:
        skill = {
            "user_id": user_id or "guest",
            "phoneme_accuracy": {},
            "total_xp": 0,
            "golden_bricks": 0,
            "games_played": 0,
            "weak_phonemes": [],
        }
    
    tier = get_difficulty_tier(skill.get("total_xp", 0))
    phoneme_acc = skill.get("phoneme_accuracy", {})
    
    # Identify weak phonemes (accuracy < 70%)
    weak_letters = []
    for pair in CONFUSABLE_PHONEMES:
        id_a, id_b = str(pair[0]), str(pair[1])
        acc_a = phoneme_acc.get(id_a, {}).get("accuracy", 50)
        acc_b = phoneme_acc.get(id_b, {}).get("accuracy", 50)
        if acc_a < 70:
            weak_letters.append(pair[0])
        if acc_b < 70:
            weak_letters.append(pair[1])
    
    # Auto-select game type based on weak areas
    game_types = ["letter_maze", "word_match", "tajweed_puzzle", "pronunciation"]
    if game_type == "auto":
        if weak_letters:
            # Prioritize pronunciation and letter games for weak phonemes
            game_type = random.choice(["letter_maze", "pronunciation", "tajweed_puzzle"])
        else:
            game_type = random.choice(game_types)
    
    # Procedurally generate game content
    if game_type == "letter_maze":
        game_data = _gen_letter_maze(tier, weak_letters)
    elif game_type == "word_match":
        game_data = _gen_word_match(tier)
    elif game_type == "tajweed_puzzle":
        game_data = _gen_tajweed_puzzle(tier, weak_letters)
    elif game_type == "pronunciation":
        game_data = _gen_pronunciation(tier, weak_letters)
    else:
        game_data = _gen_word_match(tier)
    
    game_id = str(uuid.uuid4())
    game_data["game_id"] = game_id
    game_data["game_type"] = game_type
    game_data["difficulty"] = tier["name"]
    game_data["time_limit"] = tier["time_bonus"]
    game_data["brick_reward"] = tier["brick_reward"]
    game_data["xp_reward"] = 10 + (DIFFICULTY_TIERS.index(tier) * 5)
    
    return {"success": True, "game": game_data}


def _gen_letter_maze(tier: dict, weak_letters: list) -> dict:
    """Generate a letter identification maze game."""
    import random
    # Pick target letters - prefer weak ones
    all_letters = list(ARABIC_LETTERS)
    if weak_letters:
        targets = [lt for lt in all_letters if lt["id"] in weak_letters]
        if len(targets) < 2:
            targets = random.sample(all_letters, 2)
    else:
        targets = random.sample(all_letters, min(3, tier["choices"]))
    
    target = random.choice(targets)
    # Generate grid with distractors
    grid_size = 3 if tier["choices"] <= 3 else 4
    grid = []
    distractors = [lt for lt in all_letters if lt["id"] != target["id"]]
    
    for row in range(grid_size):
        grid_row = []
        for col in range(grid_size):
            if row == 0 and col == 0:
                grid_row.append({"letter": target["letter"], "id": target["id"], "is_target": True})
            else:
                d = random.choice(distractors)
                grid_row.append({"letter": d["letter"], "id": d["id"], "is_target": False})
        grid.append(grid_row)
    
    # Shuffle target position
    target_row = random.randint(0, grid_size - 1)
    target_col = random.randint(0, grid_size - 1)
    grid[0][0], grid[target_row][target_col] = grid[target_row][target_col], grid[0][0]
    
    # Add confusable pair if exists
    confusable = None
    for pair in CONFUSABLE_PHONEMES:
        if target["id"] == pair[0]:
            confusable = {"id": pair[1], "letter": pair[3]}
            break
        if target["id"] == pair[1]:
            confusable = {"id": pair[0], "letter": pair[2]}
            break
    
    return {
        "target_letter": {
            "id": target["id"],
            "letter": target["letter"],
            "name_ar": target["name_ar"],
            "name_en": target["name_en"],
            "transliteration": target["transliteration"],
            "audio_hint": target["audio_hint"],
            "example_word": target["example_word"],
            "example_meaning": target["example_meaning"],
        },
        "grid": grid,
        "grid_size": grid_size,
        "confusable": confusable,
        "find_count": 1,
    }


def _gen_word_match(tier: dict) -> dict:
    """Generate a Quranic word matching game."""
    import random
    pool = list(QURAN_VOCAB)
    count = min(tier["choices"], len(pool))
    selected = random.sample(pool, count)
    
    words = [{"id": w["id"], "word": w["word"], "transliteration": w["transliteration"]} for w in selected]
    meanings = [{"id": w["id"], "meaning": w["meaning"], "surah": w["surah"]} for w in selected]
    random.shuffle(meanings)
    
    return {
        "words": words,
        "meanings": meanings,
        "pair_count": count,
    }


def _gen_tajweed_puzzle(tier: dict, weak_letters: list) -> dict:
    """Generate a Tajweed pronunciation rule puzzle."""
    import random
    
    tajweed_rules = [
        {"id": "idgham", "name_ar": "إدغام", "name_en": "Idgham (Merging)", "description": "When Noon Sakinah or Tanween is followed by ي ن م و ل ر", "example": "مَن يَعْمَلُ", "correct_rule": "merge"},
        {"id": "ikhfa", "name_ar": "إخفاء", "name_en": "Ikhfa (Hiding)", "description": "When Noon Sakinah or Tanween is followed by 15 specific letters", "example": "مِنْ قَبْلِ", "correct_rule": "hide"},
        {"id": "iqlab", "name_ar": "إقلاب", "name_en": "Iqlab (Conversion)", "description": "When Noon Sakinah or Tanween is followed by ب", "example": "أَنْبِئْهُمْ", "correct_rule": "convert"},
        {"id": "izhar", "name_ar": "إظهار", "name_en": "Izhar (Clear)", "description": "When Noon Sakinah or Tanween is followed by throat letters", "example": "مَنْ آمَنَ", "correct_rule": "clear"},
        {"id": "madd_tabii", "name_ar": "مدّ طبيعي", "name_en": "Madd Tabii (Natural)", "description": "Alif after Fathah, Ya after Kasrah, or Waw after Dammah (2 counts)", "example": "قَالَ", "correct_rule": "natural_stretch"},
        {"id": "qalqalah", "name_ar": "قلقلة", "name_en": "Qalqalah (Echoing)", "description": "Bouncing sound on Sukoon of letters ق ط ب ج د", "example": "أَحَدْ", "correct_rule": "echo"},
    ]
    
    selected = random.sample(tajweed_rules, min(3, len(tajweed_rules)))
    target_rule = random.choice(selected)
    
    # Generate choices - one correct + distractors
    all_rules = [r["correct_rule"] for r in tajweed_rules]
    choices = [target_rule["correct_rule"]]
    distractors = [r for r in all_rules if r != target_rule["correct_rule"]]
    choices.extend(random.sample(distractors, min(tier["choices"] - 1, len(distractors))))
    random.shuffle(choices)
    
    return {
        "question_rule": {
            "id": target_rule["id"],
            "name_ar": target_rule["name_ar"],
            "name_en": target_rule["name_en"],
            "example": target_rule["example"],
        },
        "description": target_rule["description"],
        "choices": choices,
        "correct_answer": target_rule["correct_rule"],
        "all_rules": [{"id": r["id"], "name_ar": r["name_ar"], "name_en": r["name_en"], "correct_rule": r["correct_rule"]} for r in tajweed_rules],
    }


def _gen_pronunciation(tier: dict, weak_letters: list) -> dict:
    """Generate a pronunciation challenge targeting weak phonemes."""
    import random
    
    # Pick words from Quran vocab + letter examples
    candidates = []
    if weak_letters:
        for lt in ARABIC_LETTERS:
            if lt["id"] in weak_letters:
                candidates.append({
                    "word": lt["example_word"],
                    "transliteration": lt["transliteration"],
                    "meaning": lt["example_meaning"],
                    "letter_id": lt["id"],
                    "letter": lt["letter"],
                    "source": "letter",
                })
    
    # Add Quranic words
    for qw in QURAN_VOCAB:
        candidates.append({
            "word": qw["word"],
            "transliteration": qw["transliteration"],
            "meaning": qw["meaning"],
            "letter_id": None,
            "letter": None,
            "source": "quran",
        })
    
    if not candidates:
        candidates = [{"word": lt["example_word"], "transliteration": lt["transliteration"], "meaning": lt["example_meaning"], "letter_id": lt["id"], "letter": lt["letter"], "source": "letter"} for lt in ARABIC_LETTERS]
    
    target = random.choice(candidates)
    accuracy_threshold = max(60, 85 - (DIFFICULTY_TIERS.index(tier) * 5))
    
    return {
        "target_word": target["word"],
        "transliteration": target["transliteration"],
        "meaning": target["meaning"],
        "letter_id": target["letter_id"],
        "letter": target["letter"],
        "source": target["source"],
        "accuracy_threshold": accuracy_threshold,
    }


@api_router.post("/kids-zone/submit-result")
async def submit_game_result(payload: dict):
    """Submit game result and update skill profile."""
    user_id = payload.get("user_id", "guest")
    game_type = payload.get("game_type", "")
    correct = payload.get("correct", False)
    score = payload.get("score", 0)
    phonemes_tested = payload.get("phonemes_tested", [])
    pronunciation_accuracy = payload.get("pronunciation_accuracy", 0)
    
    # Get or create skill profile
    skill = await db.kids_skills.find_one({"user_id": user_id})
    if not skill:
        skill = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "phoneme_accuracy": {},
            "total_xp": 0,
            "golden_bricks": 0,
            "games_played": 0,
            "weak_phonemes": [],
            "created_at": datetime.utcnow().isoformat(),
        }
        await db.kids_skills.insert_one(skill)
    
    # Calculate rewards
    xp_earned = score if correct else max(2, score // 3)
    tier = get_difficulty_tier(skill.get("total_xp", 0))
    bricks_earned = tier["brick_reward"] if correct else 0
    
    # Update phoneme accuracy for tested phonemes
    phoneme_acc = skill.get("phoneme_accuracy", {})
    for pid in phonemes_tested:
        pid_str = str(pid)
        if pid_str not in phoneme_acc:
            phoneme_acc[pid_str] = {"attempts": 0, "correct": 0, "accuracy": 50}
        phoneme_acc[pid_str]["attempts"] += 1
        if correct:
            phoneme_acc[pid_str]["correct"] += 1
        total = phoneme_acc[pid_str]["attempts"]
        corr = phoneme_acc[pid_str]["correct"]
        phoneme_acc[pid_str]["accuracy"] = int((corr / total) * 100) if total > 0 else 50
    
    # For pronunciation games, also update based on accuracy
    if game_type == "pronunciation" and pronunciation_accuracy > 0:
        for pid in phonemes_tested:
            pid_str = str(pid)
            if pid_str in phoneme_acc:
                # Blend speech accuracy with game accuracy
                old_acc = phoneme_acc[pid_str]["accuracy"]
                phoneme_acc[pid_str]["accuracy"] = int((old_acc * 0.7) + (pronunciation_accuracy * 0.3))
    
    # Identify new weak phonemes
    weak = []
    for pair in CONFUSABLE_PHONEMES:
        for pid in [pair[0], pair[1]]:
            pid_str = str(pid)
            if pid_str in phoneme_acc and phoneme_acc[pid_str]["accuracy"] < 70:
                weak.append(pid)
    
    # Update skill profile
    update = {
        "$set": {
            "phoneme_accuracy": phoneme_acc,
            "weak_phonemes": weak,
            "updated_at": datetime.utcnow().isoformat(),
        },
        "$inc": {
            "total_xp": xp_earned,
            "golden_bricks": bricks_earned,
            "games_played": 1,
        },
    }
    await db.kids_skills.update_one({"user_id": user_id}, update)
    
    new_xp = skill.get("total_xp", 0) + xp_earned
    new_bricks = skill.get("golden_bricks", 0) + bricks_earned
    new_tier = get_difficulty_tier(new_xp)
    mosque = get_mosque_progress(new_bricks)
    
    return {
        "success": True,
        "xp_earned": xp_earned,
        "bricks_earned": bricks_earned,
        "total_xp": new_xp,
        "total_bricks": new_bricks,
        "difficulty": new_tier["name"],
        "mosque_progress": mosque,
        "weak_phonemes": weak,
        "level_up": new_tier["name"] != tier["name"],
    }


@api_router.get("/kids-zone/progress")
async def get_kids_progress(user_id: str = ""):
    """Get user's skill map and progression data."""
    skill = await db.kids_skills.find_one({"user_id": user_id}, {"_id": 0}) if user_id else None
    if not skill:
        skill = {
            "user_id": user_id or "guest",
            "phoneme_accuracy": {},
            "total_xp": 0,
            "golden_bricks": 0,
            "games_played": 0,
            "weak_phonemes": [],
        }
    
    tier = get_difficulty_tier(skill.get("total_xp", 0))
    mosque = get_mosque_progress(skill.get("golden_bricks", 0))
    
    # Build per-letter skill map
    letter_skills = []
    for lt in ARABIC_LETTERS:
        pid = str(lt["id"])
        acc_data = skill.get("phoneme_accuracy", {}).get(pid, {"accuracy": 50, "attempts": 0, "correct": 0})
        letter_skills.append({
            "id": lt["id"],
            "letter": lt["letter"],
            "name_ar": lt["name_ar"],
            "accuracy": acc_data.get("accuracy", 50),
            "attempts": acc_data.get("attempts", 0),
            "is_weak": lt["id"] in skill.get("weak_phonemes", []),
        })
    
    return {
        "success": True,
        "profile": {
            "total_xp": skill.get("total_xp", 0),
            "golden_bricks": skill.get("golden_bricks", 0),
            "games_played": skill.get("games_played", 0),
            "difficulty": tier["name"],
            "tier": tier,
            "weak_phonemes": skill.get("weak_phonemes", []),
        },
        "letter_skills": letter_skills,
        "mosque": mosque,
        "confusable_pairs": [{"a": p[2], "b": p[3], "id_a": p[0], "id_b": p[1]} for p in CONFUSABLE_PHONEMES],
    }


@api_router.get("/kids-zone/mosque")
async def get_mosque_status(user_id: str = ""):
    """Get the virtual mosque building progress."""
    skill = await db.kids_skills.find_one({"user_id": user_id}, {"_id": 0}) if user_id else None
    bricks = skill.get("golden_bricks", 0) if skill else 0
    return {"success": True, "mosque": get_mosque_progress(bricks)}



# ==================== KIDS JOURNEY - CONNECTED LEARNING PATH ====================

# IRS Method: Introduce → Recognize → Say
# 5 Worlds, each with multiple stages, each stage has 3 activities

JOURNEY_WORLDS = [
    {
        "id": "w1", "title_ar": "الحروف", "title_en": "Letters",
        "emoji": "🔤", "color": "#3B82F6",
        "description_ar": "تعلم الحروف العربية", "description_en": "Learn Arabic Letters",
        "stages": [
            {"id": "w1s1", "title_ar": "أ ب ت ث", "title_en": "Alif Ba Ta Tha", "letters": [1, 2, 3, 4], "type": "letters"},
            {"id": "w1s2", "title_ar": "ج ح خ", "title_en": "Jim Ha Kha", "letters": [5, 6, 7], "type": "letters"},
            {"id": "w1s3", "title_ar": "د ذ ر ز", "title_en": "Dal Dhal Ra Za", "letters": [8, 9, 10, 11], "type": "letters"},
            {"id": "w1s4", "title_ar": "س ش ص ض", "title_en": "Sin Shin Sad Dad", "letters": [12, 13, 14, 15], "type": "letters"},
            {"id": "w1s5", "title_ar": "ط ظ ع غ", "title_en": "Tah Zah Ain Ghain", "letters": [16, 17, 18, 19], "type": "letters"},
            {"id": "w1s6", "title_ar": "ف ق ك ل", "title_en": "Fa Qaf Kaf Lam", "letters": [20, 21, 22, 23], "type": "letters"},
            {"id": "w1s7", "title_ar": "م ن ه و ي", "title_en": "Mim Nun Ha Waw Ya", "letters": [24, 25, 26, 27, 28], "type": "letters"},
            {"id": "w1boss", "title_ar": "تحدي الحروف", "title_en": "Letter Boss", "letters": list(range(1, 29)), "type": "boss"},
        ],
    },
    {
        "id": "w2", "title_ar": "الحركات", "title_en": "Vowels",
        "emoji": "📝", "color": "#10B981",
        "description_ar": "تعلم الحركات والتشكيل", "description_en": "Learn Harakat & Diacritics",
        "stages": [
            {"id": "w2s1", "title_ar": "الفَتحة", "title_en": "Fathah (a)", "haraka": "fathah", "type": "harakat",
             "examples": [{"letter": "بَ", "sound": "ba"}, {"letter": "تَ", "sound": "ta"}, {"letter": "سَ", "sound": "sa"}, {"letter": "نَ", "sound": "na"}]},
            {"id": "w2s2", "title_ar": "الكَسرة", "title_en": "Kasrah (i)", "haraka": "kasrah", "type": "harakat",
             "examples": [{"letter": "بِ", "sound": "bi"}, {"letter": "تِ", "sound": "ti"}, {"letter": "سِ", "sound": "si"}, {"letter": "نِ", "sound": "ni"}]},
            {"id": "w2s3", "title_ar": "الضَّمة", "title_en": "Dammah (u)", "haraka": "dammah", "type": "harakat",
             "examples": [{"letter": "بُ", "sound": "bu"}, {"letter": "تُ", "sound": "tu"}, {"letter": "سُ", "sound": "su"}, {"letter": "نُ", "sound": "nu"}]},
            {"id": "w2s4", "title_ar": "السُّكون", "title_en": "Sukoon", "haraka": "sukoon", "type": "harakat",
             "examples": [{"letter": "بْ", "sound": "b"}, {"letter": "تْ", "sound": "t"}, {"letter": "سْ", "sound": "s"}, {"letter": "نْ", "sound": "n"}]},
            {"id": "w2s5", "title_ar": "التنوين", "title_en": "Tanween", "haraka": "tanween", "type": "harakat",
             "examples": [{"letter": "بًا", "sound": "ban"}, {"letter": "بٍ", "sound": "bin"}, {"letter": "بٌ", "sound": "bun"}]},
            {"id": "w2boss", "title_ar": "تحدي الحركات", "title_en": "Harakat Boss", "haraka": "all", "type": "boss"},
        ],
    },
    {
        "id": "w3", "title_ar": "القراءة", "title_en": "Reading",
        "emoji": "📖", "color": "#8B5CF6",
        "description_ar": "تعلم قراءة الكلمات", "description_en": "Learn to Read Words",
        "stages": [
            {"id": "w3s1", "title_ar": "كلمات بسيطة", "title_en": "Simple Words", "type": "reading",
             "words": [{"ar": "كَتَبَ", "en": "wrote", "trans": "kataba"}, {"ar": "ذَهَبَ", "en": "went", "trans": "dhahaba"}, {"ar": "قَرَأَ", "en": "read", "trans": "qara'a"}]},
            {"id": "w3s2", "title_ar": "كلمات القرآن", "title_en": "Quran Words", "type": "reading",
             "words": [{"ar": "بِسْمِ", "en": "In the name", "trans": "bismi"}, {"ar": "اللَّهِ", "en": "Allah", "trans": "Allahi"}, {"ar": "الرَّحْمَنِ", "en": "Most Gracious", "trans": "Ar-Rahmani"}]},
            {"id": "w3s3", "title_ar": "جمل قصيرة", "title_en": "Short Phrases", "type": "reading",
             "words": [{"ar": "الحَمْدُ لِلَّهِ", "en": "Praise be to Allah", "trans": "Alhamdulillah"}, {"ar": "سُبْحَانَ اللَّهِ", "en": "Glory to Allah", "trans": "SubhanAllah"}]},
            {"id": "w3boss", "title_ar": "تحدي القراءة", "title_en": "Reading Boss", "type": "boss"},
        ],
    },
    {
        "id": "w4", "title_ar": "القرآن", "title_en": "Quran",
        "emoji": "🕌", "color": "#F59E0B",
        "description_ar": "اقرأ سور قصيرة", "description_en": "Read Short Surahs",
        "stages": [
            {"id": "w4s1", "title_ar": "الفاتحة", "title_en": "Al-Fatiha", "type": "surah",
             "ayahs": ["بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "الرَّحْمَنِ الرَّحِيمِ", "مَالِكِ يَوْمِ الدِّينِ", "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ", "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ"],
             "meanings": ["In the name of Allah, Most Gracious, Most Merciful", "Praise be to Allah, Lord of all worlds", "The Most Gracious, Most Merciful", "Master of the Day of Judgment", "You alone we worship, You alone we ask for help", "Guide us to the straight path", "The path of those You have blessed, not of those who earned anger, nor of those who went astray"]},
            {"id": "w4s2", "title_ar": "الإخلاص", "title_en": "Al-Ikhlas", "type": "surah",
             "ayahs": ["بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "قُلْ هُوَ اللَّهُ أَحَدٌ", "اللَّهُ الصَّمَدُ", "لَمْ يَلِدْ وَلَمْ يُولَدْ", "وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ"],
             "meanings": ["In the name of Allah, Most Gracious, Most Merciful", "Say: He is Allah, the One", "Allah, the Eternal Refuge", "He neither begets nor was He begotten", "Nor is there to Him any equal"]},
            {"id": "w4s3", "title_ar": "الناس", "title_en": "An-Nas", "type": "surah",
             "ayahs": ["بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "مَلِكِ النَّاسِ", "إِلَهِ النَّاسِ", "مِنْ شَرِّ الْوَسْوَاسِ الْخَنَّاسِ", "الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ", "مِنَ الْجِنَّةِ وَالنَّاسِ"],
             "meanings": ["In the name of Allah, Most Gracious, Most Merciful", "Say: I seek refuge in the Lord of mankind", "The King of mankind", "The God of mankind", "From the evil of the whisperer who withdraws", "Who whispers in the chests of mankind", "From among the jinn and mankind"]},
            {"id": "w4s4", "title_ar": "الفلق", "title_en": "Al-Falaq", "type": "surah",
             "ayahs": ["بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ", "مِنْ شَرِّ مَا خَلَقَ", "وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ", "وَمِنْ شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ", "وَمِنْ شَرِّ حَاسِدٍ إِذَا حَسَدَ"],
             "meanings": ["In the name of Allah, Most Gracious, Most Merciful", "Say: I seek refuge in the Lord of daybreak", "From the evil of that which He created", "From the evil of darkness when it settles", "From the evil of the blowers in knots", "From the evil of an envier when they envy"]},
            {"id": "w4boss", "title_ar": "تحدي القرآن", "title_en": "Quran Boss", "type": "boss"},
        ],
    },
    {
        "id": "w5", "title_ar": "التجويد", "title_en": "Tajweed",
        "emoji": "🎯", "color": "#EF4444",
        "description_ar": "أحكام التجويد", "description_en": "Tajweed Rules",
        "stages": [
            {"id": "w5s1", "title_ar": "إظهار و إدغام", "title_en": "Izhar & Idgham", "type": "tajweed",
             "rules": [
                 {"id": "izhar", "name_ar": "إظهار", "name_en": "Clear", "desc": "Noon Sakinah before throat letters", "example": "مَنْ آمَنَ"},
                 {"id": "idgham", "name_ar": "إدغام", "name_en": "Merge", "desc": "Noon Sakinah before ي ن م و ل ر", "example": "مَن يَعْمَلُ"},
             ]},
            {"id": "w5s2", "title_ar": "إخفاء و إقلاب", "title_en": "Ikhfa & Iqlab", "type": "tajweed",
             "rules": [
                 {"id": "ikhfa", "name_ar": "إخفاء", "name_en": "Hide", "desc": "Noon Sakinah before 15 letters", "example": "مِنْ قَبْلِ"},
                 {"id": "iqlab", "name_ar": "إقلاب", "name_en": "Convert", "desc": "Noon Sakinah before ب", "example": "أَنْبِئْهُمْ"},
             ]},
            {"id": "w5s3", "title_ar": "المدود", "title_en": "Madd (Stretching)", "type": "tajweed",
             "rules": [
                 {"id": "madd_tabii", "name_ar": "مد طبيعي", "name_en": "Natural (2 counts)", "desc": "Alif after Fathah, Ya after Kasrah, Waw after Dammah", "example": "قَالَ"},
             ]},
            {"id": "w5s4", "title_ar": "القلقلة", "title_en": "Qalqalah", "type": "tajweed",
             "rules": [
                 {"id": "qalqalah", "name_ar": "قلقلة", "name_en": "Echo", "desc": "Bouncing sound on ق ط ب ج د with Sukoon", "example": "أَحَدْ"},
             ]},
            {"id": "w5boss", "title_ar": "تحدي التجويد", "title_en": "Tajweed Boss", "type": "boss"},
        ],
    },
]

def build_flat_stages():
    """Build a flat list of all stages with world info."""
    stages = []
    for w in JOURNEY_WORLDS:
        for s in w["stages"]:
            stages.append({**s, "world_id": w["id"], "world_title_ar": w["title_ar"], "world_emoji": w["emoji"], "world_color": w["color"]})
    return stages

ALL_STAGES = build_flat_stages()
STAGE_INDEX = {s["id"]: i for i, s in enumerate(ALL_STAGES)}


@api_router.get("/kids-zone/journey")
async def get_journey(user_id: str = ""):
    """Get the full learning journey map with user progress."""
    # Get user progress
    prog = await db.kids_journey.find_one({"user_id": user_id}, {"_id": 0}) if user_id else None
    if not prog:
        prog = {"user_id": user_id or "guest", "completed": {}, "stars": {}, "current_stage": "w1s1"}

    completed = prog.get("completed", {})
    stars_map = prog.get("stars", {})
    current = prog.get("current_stage", "w1s1")

    # Build worlds with unlock status
    worlds = []
    prev_unlocked = True
    for w in JOURNEY_WORLDS:
        stages = []
        world_completed = 0
        for s in w["stages"]:
            sid = s["id"]
            is_complete = completed.get(sid, False)
            st = stars_map.get(sid, 0)
            is_current = sid == current
            is_unlocked = prev_unlocked
            if is_complete:
                world_completed += 1
                prev_unlocked = True
            elif is_current:
                is_unlocked = True
                prev_unlocked = False
            else:
                prev_unlocked = False

            stages.append({
                "id": sid,
                "title_ar": s["title_ar"],
                "title_en": s.get("title_en", ""),
                "type": s["type"],
                "unlocked": is_unlocked,
                "completed": is_complete,
                "stars": st,
                "is_current": is_current,
                "is_boss": s["type"] == "boss",
            })
        worlds.append({
            "id": w["id"],
            "title_ar": w["title_ar"],
            "title_en": w["title_en"],
            "emoji": w["emoji"],
            "color": w["color"],
            "description_ar": w["description_ar"],
            "description_en": w["description_en"],
            "stages": stages,
            "progress": world_completed,
            "total": len(stages),
        })
    
    # Get mosque/XP data
    skill = await db.kids_skills.find_one({"user_id": user_id}, {"_id": 0}) if user_id else None
    xp = skill.get("total_xp", 0) if skill else 0
    bricks_val = skill.get("golden_bricks", 0) if skill else 0

    return {
        "success": True,
        "worlds": worlds,
        "current_stage": current,
        "total_xp": xp,
        "golden_bricks": bricks_val,
        "mosque": get_mosque_progress(bricks_val),
    }


@api_router.get("/kids-zone/stage/{stage_id}")
async def get_stage_content(stage_id: str, user_id: str = ""):
    """Get the IRS content for a specific stage."""
    import random
    if stage_id not in STAGE_INDEX:
        raise HTTPException(status_code=404, detail="Stage not found")

    idx = STAGE_INDEX[stage_id]
    stage = ALL_STAGES[idx]
    stype = stage["type"]

    # Build IRS (Introduce-Recognize-Say) activities
    activities = []

    if stype == "letters":
        letter_ids = stage.get("letters", [])
        letters = [lt for lt in ARABIC_LETTERS if lt["id"] in letter_ids]
        # INTRODUCE: Show letters with names and sounds
        activities.append({
            "phase": "introduce",
            "phase_ar": "تعرّف",
            "phase_emoji": "👁️",
            "content": [{
                "id": lt["id"], "letter": lt["letter"], "name_ar": lt["name_ar"],
                "name_en": lt["name_en"], "transliteration": lt["transliteration"],
                "audio_hint": lt["audio_hint"], "example_word": lt["example_word"],
                "example_meaning": lt["example_meaning"],
            } for lt in letters],
        })
        # RECOGNIZE: Find letters in grid
        target = random.choice(letters)
        distractors = [lt for lt in ARABIC_LETTERS if lt["id"] not in letter_ids]
        grid_size = 3
        grid = []
        for r in range(grid_size):
            row = []
            for c in range(grid_size):
                if r == 0 and c == 0:
                    row.append({"letter": target["letter"], "id": target["id"], "correct": True})
                else:
                    d = random.choice(distractors)
                    row.append({"letter": d["letter"], "id": d["id"], "correct": False})
            grid.append(row)
        tr = random.randint(0, grid_size - 1)
        tc = random.randint(0, grid_size - 1)
        grid[0][0], grid[tr][tc] = grid[tr][tc], grid[0][0]
        activities.append({
            "phase": "recognize",
            "phase_ar": "اكتشف",
            "phase_emoji": "🔍",
            "game_type": "find_letter",
            "target": {"id": target["id"], "letter": target["letter"], "name_ar": target["name_ar"], "audio_hint": target["audio_hint"]},
            "grid": grid, "grid_size": grid_size,
        })
        # SAY: Pronounce each letter
        activities.append({
            "phase": "say",
            "phase_ar": "انطق",
            "phase_emoji": "🎤",
            "targets": [{"id": lt["id"], "letter": lt["letter"], "word": lt["example_word"], "transliteration": lt["transliteration"]} for lt in letters],
        })

    elif stype == "harakat":
        examples = stage.get("examples", [])
        activities.append({
            "phase": "introduce", "phase_ar": "تعرّف", "phase_emoji": "👁️",
            "haraka": stage.get("haraka"), "title_ar": stage["title_ar"],
            "content": examples,
        })
        # RECOGNIZE: Match letter+haraka to sound
        random.shuffle(examples)
        activities.append({
            "phase": "recognize", "phase_ar": "اكتشف", "phase_emoji": "🔍",
            "game_type": "match_sound",
            "pairs": [{"display": ex["letter"], "answer": ex["sound"]} for ex in examples],
        })
        activities.append({
            "phase": "say", "phase_ar": "انطق", "phase_emoji": "🎤",
            "targets": [{"letter": ex["letter"], "word": ex["letter"], "transliteration": ex["sound"]} for ex in examples],
        })

    elif stype == "reading":
        words = stage.get("words", [])
        activities.append({
            "phase": "introduce", "phase_ar": "تعرّف", "phase_emoji": "👁️",
            "content": words,
        })
        shuffled_meanings = list(words)
        random.shuffle(shuffled_meanings)
        activities.append({
            "phase": "recognize", "phase_ar": "اكتشف", "phase_emoji": "🔍",
            "game_type": "match_meaning",
            "words": [{"ar": w["ar"], "trans": w["trans"]} for w in words],
            "meanings": [{"ar": w["ar"], "en": w["en"]} for w in shuffled_meanings],
        })
        activities.append({
            "phase": "say", "phase_ar": "انطق", "phase_emoji": "🎤",
            "targets": [{"letter": w["ar"], "word": w["ar"], "transliteration": w["trans"]} for w in words],
        })

    elif stype == "surah":
        ayahs = stage.get("ayahs", [])
        meanings = stage.get("meanings", [])
        activities.append({
            "phase": "introduce", "phase_ar": "تعرّف", "phase_emoji": "👁️",
            "surah_name": stage["title_ar"],
            "ayahs": [{"text": a, "meaning": meanings[i] if i < len(meanings) else ""} for i, a in enumerate(ayahs)],
        })
        # RECOGNIZE: Put ayahs in correct order
        indices = list(range(len(ayahs)))
        shuffled = list(indices)
        random.shuffle(shuffled)
        activities.append({
            "phase": "recognize", "phase_ar": "اكتشف", "phase_emoji": "🔍",
            "game_type": "order_ayahs",
            "shuffled_ayahs": [{"text": ayahs[i], "correct_index": i} for i in shuffled],
        })
        activities.append({
            "phase": "say", "phase_ar": "انطق", "phase_emoji": "🎤",
            "targets": [{"letter": a, "word": a, "transliteration": ""} for a in ayahs[:3]],
        })

    elif stype == "tajweed":
        rules = stage.get("rules", [])
        activities.append({
            "phase": "introduce", "phase_ar": "تعرّف", "phase_emoji": "👁️",
            "content": rules,
        })
        target_rule = random.choice(rules)
        all_rule_ids = ["izhar", "idgham", "ikhfa", "iqlab", "madd_tabii", "qalqalah"]
        choices = [target_rule["id"]]
        others = [r for r in all_rule_ids if r != target_rule["id"]]
        choices.extend(random.sample(others, min(2, len(others))))
        random.shuffle(choices)
        activities.append({
            "phase": "recognize", "phase_ar": "اكتشف", "phase_emoji": "🔍",
            "game_type": "identify_rule",
            "example": target_rule["example"],
            "rule_name_ar": target_rule["name_ar"],
            "correct": target_rule["id"],
            "choices": choices,
        })
        activities.append({
            "phase": "say", "phase_ar": "انطق", "phase_emoji": "🎤",
            "targets": [{"letter": r["example"], "word": r["example"], "transliteration": r["name_en"]} for r in rules],
        })

    elif stype == "boss":
        activities.append({
            "phase": "boss", "phase_ar": "تحدي", "phase_emoji": "🏆",
            "world_id": stage["world_id"],
        })

    return {
        "success": True,
        "stage": {
            "id": stage_id,
            "title_ar": stage["title_ar"],
            "title_en": stage.get("title_en", ""),
            "type": stype,
            "world_id": stage["world_id"],
            "world_emoji": stage["world_emoji"],
            "world_color": stage["world_color"],
        },
        "activities": activities,
    }


@api_router.post("/kids-zone/complete-stage")
async def complete_stage(payload: dict):
    """Mark a stage as complete and unlock next."""
    user_id = payload.get("user_id", "guest")
    stage_id = payload.get("stage_id", "")
    stars_earned = min(3, max(1, payload.get("stars", 1)))

    if stage_id not in STAGE_INDEX:
        raise HTTPException(status_code=404, detail="Stage not found")

    idx = STAGE_INDEX[stage_id]
    next_id = ALL_STAGES[idx + 1]["id"] if idx + 1 < len(ALL_STAGES) else None

    # Update journey progress
    prog = await db.kids_journey.find_one({"user_id": user_id})
    if not prog:
        prog = {"id": str(uuid.uuid4()), "user_id": user_id, "completed": {}, "stars": {}, "current_stage": "w1s1"}
        await db.kids_journey.insert_one(prog)

    update = {
        "$set": {
            f"completed.{stage_id}": True,
            f"stars.{stage_id}": max(stars_earned, prog.get("stars", {}).get(stage_id, 0)),
        }
    }
    if next_id:
        update["$set"]["current_stage"] = next_id

    await db.kids_journey.update_one({"user_id": user_id}, update)

    # Also award XP and bricks
    xp_reward = 15 if "boss" in stage_id else 10
    brick_reward = 3 if "boss" in stage_id else 1
    await db.kids_skills.update_one(
        {"user_id": user_id},
        {"$inc": {"total_xp": xp_reward, "golden_bricks": brick_reward, "games_played": 1}},
        upsert=True,
    )

    skill = await db.kids_skills.find_one({"user_id": user_id}, {"_id": 0})
    bricks_val = skill.get("golden_bricks", 0) if skill else brick_reward

    return {
        "success": True,
        "stars": stars_earned,
        "xp_earned": xp_reward,
        "bricks_earned": brick_reward,
        "next_stage": next_id,
        "mosque": get_mosque_progress(bricks_val),
    }



# ==================== APP SETUP ====================
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown():
    client_db.close()
