"""
Router: social
"""
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from deps import db, get_user, logger, security, verify_jwt, create_jwt, hash_password, check_password, ADMIN_EMAILS, STRIPE_API_KEY, EMERGENT_LLM_KEY, haversine, query_overpass, clean_time, OVERPASS_ENDPOINTS, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_EMAIL, FIREBASE_PROJECT_ID, RESEND_API_KEY, GEMINI_API_KEY
from pathlib import Path
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

# Import SOHBA_CATEGORIES from auth router
from .auth import SOHBA_CATEGORIES

router = APIRouter(tags=["Social (Sohba)"])

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


@router.get("/sohba/categories")
async def get_categories():
    return {"categories": SOHBA_CATEGORIES}

@router.get("/sohba/posts")
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

@router.post("/sohba/posts")
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

@router.post("/sohba/posts/{post_id}/like")
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

@router.post("/sohba/posts/{post_id}/save")
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

@router.get("/sohba/posts/{post_id}/comments")
async def get_comments(post_id: str, page: int = 1, limit: int = 50):
    skip = (page - 1) * limit
    cursor = db.comments.find({"post_id": post_id}, {"_id": 0}).sort("created_at", 1).skip(skip).limit(limit)
    comments = await cursor.to_list(length=limit)
    return {"comments": comments}

@router.post("/sohba/posts/{post_id}/comments")
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

@router.delete("/sohba/comments/{comment_id}")
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
@router.get("/admin/social/posts")
async def admin_list_posts(page: int = 1, limit: int = 30, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    skip = (page - 1) * limit
    cursor = db.posts.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    total = await db.posts.count_documents({})
    return {"posts": posts, "total": total}

@router.delete("/admin/social/posts/{post_id}")
async def admin_delete_post(post_id: str, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    await db.posts.delete_one({"id": post_id})
    await db.likes.delete_many({"post_id": post_id})
    await db.comments.delete_many({"post_id": post_id})
    await db.saves.delete_many({"post_id": post_id})
    return {"deleted": True}

@router.get("/admin/social/comments")
async def admin_list_comments(page: int = 1, limit: int = 50, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    skip = (page - 1) * limit
    cursor = db.comments.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    comments = await cursor.to_list(length=limit)
    total = await db.comments.count_documents({})
    return {"comments": comments, "total": total}

@router.delete("/admin/social/comments/{comment_id}")
async def admin_delete_comment(comment_id: str, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    await db.comments.delete_one({"id": comment_id})
    return {"deleted": True}

@router.get("/admin/social/users")
async def admin_list_users(page: int = 1, limit: int = 50, user: dict = Depends(get_user)):
    if not user or user.get("email") not in ["mohammadalrejab@gmail.com"]:
        raise HTTPException(403, "غير مصرح")
    skip = (page - 1) * limit
    cursor = db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    total = await db.users.count_documents({})
    # Bulk aggregation instead of N+1 queries
    user_ids = [u["id"] for u in users]
    post_counts: dict = {}
    async for doc in db.posts.aggregate([{"$match": {"author_id": {"$in": user_ids}}}, {"$group": {"_id": "$author_id", "count": {"$sum": 1}}}]):
        post_counts[doc["_id"]] = doc["count"]
    follower_counts: dict = {}
    async for doc in db.follows.aggregate([{"$match": {"following_id": {"$in": user_ids}}}, {"$group": {"_id": "$following_id", "count": {"$sum": 1}}}]):
        follower_counts[doc["_id"]] = doc["count"]
    for u in users:
        u["posts_count"] = post_counts.get(u["id"], 0)
        u["followers_count"] = follower_counts.get(u["id"], 0)
    return {"users": users, "total": total}

@router.get("/admin/social/stats")
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

@router.delete("/sohba/posts/{post_id}")
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

@router.patch("/sohba/posts/{post_id}")
async def update_post(post_id: str, data: dict, user: dict = Depends(get_user)):
    """Update post content/description - only post owner can edit"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    post = await db.posts.find_one({"id": post_id})
    if not post:
        raise HTTPException(404, "المنشور غير موجود")
    if post["author_id"] != user["id"]:
        raise HTTPException(403, "غير مصرح بالتعديل")
    update_fields = {}
    if "content" in data:
        update_fields["content"] = data["content"]
    if update_fields:
        await db.posts.update_one({"id": post_id}, {"$set": update_fields})
    return {"success": True, "updated": update_fields}

# ==================== FOLLOW SYSTEM ====================
@router.post("/sohba/follow/{target_id}")
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

@router.get("/sohba/profile/{user_id}")
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

@router.get("/sohba/my-stats")
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
@router.get("/sohba/recommended-users")
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

@router.get("/sohba/feed/following")
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

@router.get("/sohba/feed/videos")
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

@router.post("/sohba/posts/{post_id}/share")
async def share_post(post_id: str, user: dict = Depends(get_user)):
    """Increment share count for a post"""
    result = await db.posts.update_one({"id": post_id}, {"$inc": {"shares_count": 1}})
    if result.modified_count == 0:
        raise HTTPException(404, "المنشور غير موجود")
    return {"shared": True}

@router.get("/sohba/user/{user_id}/posts")
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
@router.post("/sohba/pages")
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

@router.get("/sohba/pages")
async def list_pages(category: str = "all", page: int = 1, limit: int = 20):
    query = {} if category == "all" else {"category": category}
    skip = (page - 1) * limit
    cursor = db.pages.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    pages = await cursor.to_list(length=limit)
    return {"pages": pages}

# ==================== SEARCH & EXPLORE ====================

@router.get("/sohba/search")
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

@router.get("/sohba/explore")
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

@router.get("/sohba/trending-users")
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
