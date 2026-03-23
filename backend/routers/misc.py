"""
Router: misc
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
from starlette.requests import Request
from emergentintegrations.payments.stripe.checkout import StripeCheckout

router = APIRouter(tags=["Miscellaneous"])

@router.post("/webhook/stripe")
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


@router.post("/user/bank-account")
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

@router.get("/user/bank-account")
async def get_bank_account(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    account = await db.bank_accounts.find_one({"user_id": user["id"]}, {"_id": 0})
    return {"account": account}

@router.get("/user/earnings")
async def get_earnings(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    wallet = await db.wallets.find_one({"user_id": user["id"]}, {"_id": 0})
    gifts_received = await db.gift_transactions.count_documents({"recipient_id": user["id"]})
    total_earned = wallet.get("total_earned_credits", 0) if wallet else 0
    return {"total_earned_credits": total_earned, "gifts_received": gifts_received, "current_credits": wallet.get("credits", 0) if wallet else 0}

# Admin bank account settings
@router.post("/admin/bank-account")
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

@router.get("/admin/bank-account")
async def admin_get_bank(user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    account = await db.admin_settings.find_one({"type": "bank_account"}, {"_id": 0})
    pool = await db.admin_pool.find_one({"type": "gift_revenue"}, {"_id": 0})
    return {"account": account, "revenue": pool}


# ==================== ADMIN ANNOUNCEMENTS ====================
@router.post("/admin/announcements")
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

@router.get("/announcements")
async def get_announcements():
    """Public: get active announcements for homepage"""
    anns = await db.announcements.find({"active": True}, {"_id": 0}).sort("created_at", -1).to_list(5)
    return {"announcements": anns}

@router.delete("/admin/announcements/{ann_id}")
async def delete_announcement(ann_id: str, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    await db.announcements.update_one({"id": ann_id}, {"$set": {"active": False}})
    return {"success": True}

# ==================== VENDOR REGISTRATION ====================
@router.post("/marketplace/register-vendor")
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

@router.get("/marketplace/vendor-status")
async def vendor_status(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    vendor = await db.vendors.find_one({"user_id": user["id"]}, {"_id": 0})
    return {"vendor": vendor}

@router.get("/admin/vendors")
async def admin_list_vendors(user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or not admin.get("is_admin"):
        raise HTTPException(403, "غير مصرح")
    vendors = await db.vendors.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"vendors": vendors}

@router.put("/admin/vendors/{vendor_id}")
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

@router.post("/user/sync")
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

@router.get("/user/sync")
async def get_user_data(user: dict = Depends(get_user)):
    """Get synced user data"""
    if not user:
        raise HTTPException(401, "مطلوب تسجيل الدخول")
    doc = await db.user_data.find_one({"user_id": user["id"]}, {"_id": 0})
    return doc or {}

# ==================== ADMIN ====================

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

class EmbedContentRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = ""
    embed_url: str = Field(..., min_length=5)
    platform: str = "youtube"  # youtube, dailymotion, vimeo, etc.
    category: str = "general"
    thumbnail_url: Optional[str] = None

@router.post("/admin/embed-content")
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

@router.get("/admin/embed-content")
async def admin_list_embed_content(user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or (admin.get("email") not in ["mohammadalrejab@gmail.com"] and not admin.get("is_admin")):
        raise HTTPException(403, "غير مصرح")
    content = await db.embed_content.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"content": content}

@router.delete("/admin/embed-content/{content_id}")
async def delete_embed_content(content_id: str, user: dict = Depends(get_user)):
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or (admin.get("email") not in ["mohammadalrejab@gmail.com"] and not admin.get("is_admin")):
        raise HTTPException(403, "غير مصرح")
    await db.embed_content.delete_one({"id": content_id})
    # Also remove linked story post
    await db.posts.delete_one({"embed_content_id": content_id})
    return {"success": True}

@router.get("/embed-content")
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

@router.post("/status")
async def create_status(data: StatusCheckCreate):
    doc = {"id": str(uuid.uuid4()), "client_name": data.client_name, "timestamp": datetime.utcnow().isoformat()}
    await db.status_checks.insert_one(doc)
    return doc

@router.get("/status")
async def get_status():
    docs = await db.status_checks.find({}, {"_id": 0}).to_list(100)
    return docs

@router.post("/contact")
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

@router.post("/report")
async def report_content(data: dict, user: dict = Depends(get_user)):
    """Report inappropriate content - required by App Store for user-generated content"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    doc = {
        "id": str(uuid.uuid4())[:8],
        "reporter_id": user["id"],
        "reporter_name": user.get("name", ""),
        "content_id": data.get("content_id", ""),
        "content_type": data.get("content_type", ""),  # post, comment, user, story
        "reported_user_id": data.get("reported_user_id", ""),
        "reason": data.get("reason", ""),
        "reason_category": data.get("reason_category", "other"),  # spam, harassment, hate_speech, inappropriate, violence, other
        "details": data.get("details", ""),
        "created_at": datetime.utcnow().isoformat(),
        "status": "pending",  # pending, reviewed, resolved, dismissed
        "resolved": False
    }
    await db.reports.insert_one(doc)
    return {"success": True, "message": "تم الإبلاغ بنجاح وسيتم مراجعته"}

@router.post("/block-user")
async def block_user(data: dict, user: dict = Depends(get_user)):
    """Block a user - hides their content from the blocker"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    blocked_id = data.get("user_id", "")
    if not blocked_id or blocked_id == user["id"]:
        raise HTTPException(400, "لا يمكن حظر نفسك")
    existing = await db.blocks.find_one({"blocker_id": user["id"], "blocked_id": blocked_id})
    if existing:
        # Unblock
        await db.blocks.delete_one({"blocker_id": user["id"], "blocked_id": blocked_id})
        return {"success": True, "blocked": False, "message": "تم إلغاء الحظر"}
    else:
        doc = {
            "id": str(uuid.uuid4())[:8],
            "blocker_id": user["id"],
            "blocked_id": blocked_id,
            "created_at": datetime.utcnow().isoformat()
        }
        await db.blocks.insert_one(doc)
        # Also unfollow
        await db.follows.delete_one({"follower_id": user["id"], "following_id": blocked_id})
        await db.follows.delete_one({"follower_id": blocked_id, "following_id": user["id"]})
        return {"success": True, "blocked": True, "message": "تم حظر المستخدم"}

@router.get("/blocked-users")
async def get_blocked_users(user: dict = Depends(get_user)):
    """Get list of blocked user IDs"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    blocks = await db.blocks.find({"blocker_id": user["id"]}).to_list(500)
    return {"blocked_ids": [b["blocked_id"] for b in blocks]}


@router.get("/admin/stats")
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

@router.get("/admin/contacts")
async def admin_contacts(user: dict = Depends(get_user), limit: int = 50):
    """Get contact messages for admin"""
    admin = await db.users.find_one({"id": user["id"]}) if user else None
    if not admin or (admin.get("email") not in ADMIN_EMAILS and not admin.get("is_admin")):
        raise HTTPException(403, "غير مصرح")
    
    docs = await db.contact_messages.find({}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    return {"contacts": docs}

@router.get("/donations/list")
async def list_donations(limit: int = 50):
    """List donation requests"""
    docs = await db.donations.find({"active": True}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    return {"donations": docs}

@router.post("/donations/create")
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

# ==================== P2P DONATIONS (تبرعات مباشرة) ====================

@router.post("/donation-requests/create")
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

@router.get("/donation-requests/list")
async def list_donation_requests(status: str = "active", limit: int = 30, page: int = 1):
    """List donation requests (عرض طلبات التبرع)"""
    skip = (page - 1) * limit
    query = {"status": status} if status != "all" else {}
    cursor = db.donation_requests.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    requests = await cursor.to_list(length=limit)
    total = await db.donation_requests.count_documents(query)
    return {"requests": requests, "total": total, "has_more": total > skip + limit}

@router.post("/donation-requests/{req_id}/contact")
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

