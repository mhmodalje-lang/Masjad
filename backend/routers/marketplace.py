"""
Router: marketplace
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
from deps import get_admin_user

router = APIRouter(tags=["Marketplace & Ads"])

@router.post("/ads/submit")
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

@router.get("/ads/my-ads")
async def get_my_ads(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    ads = await db.user_ads.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"ads": ads}

@router.get("/ads/approved")
async def get_approved_ads():
    """Get approved ads for display"""
    ads = await db.user_ads.find({"status": "approved"}, {"_id": 0}).to_list(20)
    return {"ads": ads}

@router.post("/ads/watch/{ad_id}")
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
@router.get("/admin/user-ads")
async def admin_get_user_ads(user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    ads = await db.user_ads.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"ads": ads}

@router.put("/admin/user-ads/{ad_id}")
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
@router.post("/marketplace/products")
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

@router.get("/marketplace/products")
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

@router.get("/marketplace/my-products")
async def my_products(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    products = await db.products.find({"vendor_id": user["id"]}, {"_id": 0}).to_list(100)
    return {"products": products}

# Admin marketplace settings
@router.put("/admin/marketplace/commission")
async def set_commission_rate(data: dict, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    rate = data.get("commission_rate", 10)
    await db.admin_settings.update_one({"type": "marketplace"}, {"$set": {"commission_rate": rate}}, upsert=True)
    return {"success": True, "commission_rate": rate}


# ==================== AI RELIGIOUS ASSISTANT (المساعد الديني) ====================
