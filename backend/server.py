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
    return {k: user.get(k) for k in ("id","email","name","avatar","provider","created_at")}

@api_router.post("/auth/logout")
async def logout():
    return {"message": "تم تسجيل الخروج"}

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    password: Optional[str] = None

@api_router.put("/auth/update-profile")
async def update_profile(req: UpdateProfileRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "غير مصادق")
    update = {}
    if req.name and req.name.strip():
        update["name"] = req.name.strip()
    if req.avatar:
        update["avatar"] = req.avatar
    if req.password and len(req.password) >= 6:
        import hashlib
        update["password_hash"] = hashlib.sha256(req.password.encode()).hexdigest()
    if update:
        await db.users.update_one({"id": user["id"]}, {"$set": update})
    return {"success": True, "message": "تم تحديث الملف الشخصي"}

# ==================== SOCIAL PLATFORM (صُحبة) ====================

SOHBA_CATEGORIES = [
    {"key": "general", "label": "عام", "icon": "globe"},
    {"key": "quran", "label": "القرآن الكريم", "icon": "book"},
    {"key": "hadith", "label": "الحديث الشريف", "icon": "scroll"},
    {"key": "ramadan", "label": "رمضان", "icon": "moon"},
    {"key": "dua", "label": "الدعاء والأذكار", "icon": "hands"},
    {"key": "stories", "label": "قصص وعبر", "icon": "feather"},
    {"key": "hajj", "label": "الحج والعمرة", "icon": "kaaba"},
    {"key": "halal", "label": "السفر الحلال", "icon": "plane"},
    {"key": "family", "label": "الأسرة المسلمة", "icon": "heart"},
    {"key": "youth", "label": "الشباب", "icon": "users"},
]

class CreatePostRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    category: str = "general"
    image_url: Optional[str] = None

class CreateCommentRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)

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
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.comments.insert_one(comment)
    comment.pop("_id", None)
    return {"comment": comment}

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
    stats = {
        "posts_count": await db.posts.count_documents({"author_id": user_id}),
        "followers_count": await db.follows.count_documents({"following_id": user_id}),
        "following_count": await db.follows.count_documents({"follower_id": user_id}),
    }
    is_following = False
    if user and user["id"] != user_id:
        is_following = bool(await db.follows.find_one({"follower_id": user["id"], "following_id": user_id}))
    return {"profile": {k: profile.get(k) for k in ("id","email","name","avatar","created_at")}, "stats": stats, "is_following": is_following}

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

@api_router.get("/daily-hadith")
async def daily_hadith():
    """Get today's hadith - rotates daily from collection"""
    today = date.today()
    day_of_year = today.timetuple().tm_yday
    idx = day_of_year % len(STATIC_HADITHS)
    hadith = STATIC_HADITHS[idx]
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

# ==================== QURAN ====================
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
    result = await db.custom_pages.delete_one({"id": page_id})
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
        "quran_translations": True,
        "prayer_times_global": True,
        "privacy_policy_languages": ["ar", "en", "ru", "tr"],
        "audio_languages": ["ar"],
        "auto_language_detection": True,
    }

# ==================== STORIES SYSTEM (حكايات) ====================
# Uses the existing posts/comments/likes collections but with story-specific endpoints

STORY_CATEGORIES = [
    {"key": "general", "label": "عام", "emoji": "📝", "icon": "file-text", "color": "#64748b"},
    {"key": "istighfar", "label": "قصص الاستغفار", "emoji": "🤲", "icon": "sparkles", "color": "#10b981"},
    {"key": "sahaba", "label": "قصص الصحابة", "emoji": "📖", "icon": "book", "color": "#f59e0b"},
    {"key": "quran", "label": "قصص القرآن", "emoji": "📗", "icon": "book-open", "color": "#059669"},
    {"key": "prophets", "label": "قصص الأنبياء", "emoji": "🌟", "icon": "star", "color": "#8b5cf6"},
    {"key": "ruqyah", "label": "قصص الرقية", "emoji": "🛡️", "icon": "shield", "color": "#3b82f6"},
    {"key": "rizq", "label": "قصص الرزق", "emoji": "✨", "icon": "coins", "color": "#eab308"},
    {"key": "tawba", "label": "قصص التوبة", "emoji": "💚", "icon": "heart", "color": "#22c55e"},
    {"key": "miracles", "label": "معجزات وعبر", "emoji": "🌙", "icon": "moon", "color": "#6366f1"},
    {"key": "embed", "label": "فيديوهات", "emoji": "🎬", "icon": "film", "color": "#ef4444"},
]

@api_router.get("/stories/categories")
async def get_story_categories():
    return {"categories": STORY_CATEGORIES}

class CreateStoryRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=10000)
    category: str = "istighfar"
    media_type: str = "text"  # text, image, video
    image_url: Optional[str] = None

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
        "title": data.title,
        "content": data.content,
        "category": data.category,
        "media_type": data.media_type,
        "image_url": data.image_url,
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
    post_ids = [l["post_id"] for l in liked_docs]
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
async def get_verse_of_day():
    """Get AI-selected verse of the day"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY).with_model("gemini", "gemini-2.0-flash")
        prompt = """اختر آية قرآنية ملهمة ومؤثرة. أعطني:
1. نص الآية بالعربية
2. اسم السورة
3. رقم الآية

أجب بصيغة JSON فقط:
{"text": "نص الآية", "surah": "اسم السورة", "ayah": رقم_الآية}"""
        response = await chat.chat([UserMessage(content=prompt)])
        import re
        match = re.search(r'\{[^}]+\}', response.content)
        if match:
            data = json_module.loads(match.group())
            return {"verse": data}
    except Exception as e:
        logging.error(f"Verse error: {e}")
    return {"verse": {"text": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ", "surah": "الطلاق", "ayah": 3}}

@api_router.get("/ai/hadith-of-day")
async def get_hadith_of_day():
    """Get AI-selected hadith of the day"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY).with_model("gemini", "gemini-2.0-flash")
        prompt = """اختر حديث نبوي صحيح ومشهور. أعطني:
1. نص الحديث مختصر
2. اسم الراوي
3. المصدر (البخاري/مسلم/الترمذي...)

أجب بصيغة JSON فقط:
{"text": "نص الحديث", "narrator": "اسم الراوي", "source": "المصدر"}"""
        response = await chat.chat([UserMessage(content=prompt)])
        import re
        match = re.search(r'\{[^}]+\}', response.content)
        if match:
            data = json_module.loads(match.group())
            return {"hadith": data}
    except Exception as e:
        logging.error(f"Hadith error: {e}")
    return {"hadith": {"text": "خيركم من تعلم القرآن وعلمه", "narrator": "عثمان بن عفان", "source": "صحيح البخاري"}}

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


# ==================== APP SETUP ====================
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown():
    client_db.close()
