"""
Router: economy
"""
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from deps import db, get_user, logger, security, verify_jwt, create_jwt, hash_password, check_password, ADMIN_EMAILS, STRIPE_API_KEY, EMERGENT_LLM_KEY, haversine, query_overpass, clean_time, OVERPASS_ENDPOINTS, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_EMAIL, FIREBASE_PROJECT_ID, RESEND_API_KEY, GEMINI_API_KEY
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from data.asma_al_husna_data import get_asma_al_husna
from data.multilingual_content import (
    STORE_ITEMS_TRANSLATED, STORE_PACKAGES_TRANSLATED, GOLD_PACKAGES_TRANSLATED,
    CREDIT_PACKAGES_TRANSLATED, ISLAMIC_GIFTS_TRANSLATED, ERROR_MESSAGES, get_error, _t
)
import uuid
import random
import math
import re
import httpx
import os
import json as json_module
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest
from starlette.requests import Request

router = APIRouter(tags=["Economy"])

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

@router.get("/rewards/balance")
async def get_gold_balance(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, get_error("login_required"))
    wallet = await db.wallets.find_one({"user_id": user["id"]}, {"_id": 0})
    if not wallet:
        wallet = {"user_id": user["id"], "gold": 0, "total_earned": 0, "streak": 0, "last_daily": None}
        await db.wallets.insert_one(wallet)
        wallet.pop("_id", None)
    return {"gold": wallet.get("gold", 0), "total_earned": wallet.get("total_earned", 0), "streak": wallet.get("streak", 0)}

@router.post("/rewards/claim")
async def claim_reward(data: ClaimRewardRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, get_error("login_required"))
    
    reward_type = data.reward_type
    gold_amount = REWARD_VALUES.get(reward_type, 0)
    if gold_amount == 0:
        raise HTTPException(400, get_error("invalid_reward_type"))
    
    wallet = await db.wallets.find_one({"user_id": user["id"]})
    if not wallet:
        wallet = {"user_id": user["id"], "gold": 0, "total_earned": 0, "streak": 0, "last_daily": None}
        await db.wallets.insert_one(wallet)
    
    today = date.today().isoformat()
    
    # Check daily login (once per day)
    if reward_type == "daily_login":
        if wallet.get("last_daily") == today:
            return {"gold": wallet.get("gold", 0), "earned": 0, "message": get_error("reward_already_claimed")}
        
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

@router.get("/rewards/history")
async def get_reward_history(user: dict = Depends(get_user), page: int = 1, limit: int = 20):
    if not user:
        raise HTTPException(401, get_error("login_required"))
    skip = (page - 1) * limit
    cursor = db.gold_transactions.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    transactions = await cursor.to_list(length=limit)
    return {"transactions": transactions}

@router.get("/rewards/leaderboard")
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

@router.get("/asma-al-husna")
async def get_asma_al_husna_endpoint(locale: str = "ar"):
    """Get the 99 Names of Allah - multilingual (from authentic Islamic sources)"""
    names = get_asma_al_husna(locale)
    return {"names": names, "total": 99}
class StoreItem(BaseModel):
    name: str
    description: str
    price_gold: int = 0
    price_usd: float = 0
    category: str = "theme"
    image_url: Optional[str] = None

@router.get("/store/items")
async def get_store_items(category: str = "all", locale: str = "ar"):
    lang = locale if locale in ["ar", "en", "de", "de-AT", "fr", "tr", "ru", "sv", "nl", "el"] else "ar"
    if lang == "de-AT":
        lang = "de"
    query = {} if category == "all" else {"category": category}
    items = await db.store_items.find(query, {"_id": 0}).to_list(100)
    if not items:
        # Seed default items with multilingual support
        defaults = []
        for item_data in STORE_ITEMS_TRANSLATED:
            defaults.append({
                "id": str(uuid.uuid4()),
                "name": _t(item_data["name"], lang),
                "name_i18n": item_data["name"],
                "description": _t(item_data["description"], lang),
                "description_i18n": item_data["description"],
                "price_gold": item_data["price_gold"],
                "price_usd": item_data["price_usd"],
                "category": item_data["category"],
                "image_url": item_data["image_url"],
                "active": item_data["active"],
            })
        for item in defaults:
            await db.store_items.insert_one(item)
        items = [{k: v for k, v in d.items() if k != "_id"} for d in defaults]
    else:
        # Localize existing items
        for item in items:
            if "name_i18n" in item and isinstance(item["name_i18n"], dict):
                item["name"] = item["name_i18n"].get(lang, item["name_i18n"].get("ar", item.get("name", "")))
            if "description_i18n" in item and isinstance(item["description_i18n"], dict):
                item["description"] = item["description_i18n"].get(lang, item["description_i18n"].get("ar", item.get("description", "")))
    return {"items": items}

@router.post("/store/buy-gold")
async def buy_with_gold(data: dict, user: dict = Depends(get_user)):
    locale = data.get("locale", "ar")
    if not user:
        raise HTTPException(401, get_error("login_required", locale))
    
    item_id = data.get("item_id")
    item = await db.store_items.find_one({"id": item_id}, {"_id": 0})
    if not item:
        raise HTTPException(404, get_error("product_not_found", locale))
    
    wallet = await db.wallets.find_one({"user_id": user["id"]})
    if not wallet or wallet.get("gold", 0) < item["price_gold"]:
        raise HTTPException(400, get_error("insufficient_gold", locale))
    
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

@router.get("/store/my-purchases")
async def get_my_purchases(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, get_error("login_required"))
    purchases = await db.purchases.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"purchases": purchases}

# ==================== MEMBERSHIP ====================
@router.get("/membership/status")
async def get_membership(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, get_error("login_required"))
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
STORE_PACKAGES = STORE_PACKAGES_TRANSLATED

@router.post("/payments/checkout")
async def create_checkout(data: dict, request: Request, user: dict = Depends(get_user)):
    locale = data.get("locale", "ar")
    if not user:
        raise HTTPException(401, get_error("login_required", locale))
    
    package_id = data.get("package_id", "")
    origin_url = data.get("origin_url", "")
    item_id = data.get("item_id", "")
    
    if not origin_url:
        raise HTTPException(400, get_error("origin_url_required", locale))
    
    # Get price from server-side packages OR from store item
    amount = 0.0
    package_name = ""
    
    if package_id in STORE_PACKAGES:
        amount = STORE_PACKAGES[package_id]["price"]
        pkg_name_dict = STORE_PACKAGES[package_id]["name"]
        package_name = _t(pkg_name_dict, locale) if isinstance(pkg_name_dict, dict) else pkg_name_dict
    elif item_id:
        item = await db.store_items.find_one({"id": item_id}, {"_id": 0})
        if not item:
            raise HTTPException(404, get_error("product_not_found", locale))
        if item.get("price_usd", 0) <= 0:
            raise HTTPException(400, get_error("product_free_or_unavailable", locale))
        amount = float(item["price_usd"])
        package_name = item["name"]
    else:
        raise HTTPException(400, get_error("must_select_product", locale))
    
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

@router.get("/payments/status/{session_id}")
async def get_payment_status(session_id: str, request: Request, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, get_error("login_required"))
    
    txn = await db.payment_transactions.find_one({"session_id": session_id, "user_id": user["id"]}, {"_id": 0})
    if not txn:
        raise HTTPException(404, get_error("transaction_not_found"))
    
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

@router.get("/payments/packages")
async def get_packages(locale: str = "ar"):
    """Get available gold/membership packages - multilingual"""
    lang = locale if locale in ["ar", "en", "de", "de-AT", "fr", "tr", "ru", "sv", "nl", "el"] else "ar"
    result = []
    for pkg in GOLD_PACKAGES_TRANSLATED:
        p = dict(pkg)
        p["name"] = _t(pkg["name"], lang)
        result.append(p)
    return {"packages": result}


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

# Credit packages: price in EUR (base), credits given - multilingual
CREDIT_PACKAGES = CREDIT_PACKAGES_TRANSLATED

@router.get("/credits/detect-currency")
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

@router.get("/credits/packages")
async def get_credit_packages(country: str = "US", locale: str = "ar"):
    """Get credit packages with local currency pricing - multilingual"""
    currency = CURRENCY_DATA.get(country, CURRENCY_DATA["US"])
    packages = []
    for pkg in CREDIT_PACKAGES:
        local_price = round(pkg["price_eur"] * currency["rate"] / CURRENCY_DATA.get("EU", {"rate": 0.92})["rate"], 2)
        pkg_copy = dict(pkg)
        if isinstance(pkg_copy.get("label"), dict):
            pkg_copy["label"] = _t(pkg_copy["label"], locale)
        packages.append({
            **pkg_copy,
            "local_price": local_price,
            "currency_code": currency["code"],
            "currency_symbol": currency["symbol"],
            "display_price": f"{currency['symbol']} {local_price:,.2f}",
        })
    return {"packages": packages, "currency": currency}

@router.get("/credits/balance")
async def get_credits_balance(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, get_error("login_required"))
    wallet = await db.wallets.find_one({"user_id": user["id"]}, {"_id": 0})
    credits = wallet.get("credits", 0) if wallet else 0
    return {"credits": credits}

@router.post("/credits/purchase")
async def purchase_credits(data: dict, request: Request, user: dict = Depends(get_user)):
    """Create checkout session to purchase credits"""
    locale = data.get("locale", "ar")
    if not user:
        raise HTTPException(401, get_error("login_required", locale))
    
    package_id = data.get("package_id", "")
    origin_url = data.get("origin_url", "")
    pkg = next((p for p in CREDIT_PACKAGES if p["id"] == package_id), None)
    if not pkg:
        raise HTTPException(400, get_error("invalid_package", locale))
    
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
ISLAMIC_GIFTS = ISLAMIC_GIFTS_TRANSLATED

@router.get("/gifts/list")
async def list_gifts(locale: str = "ar"):
    """List available gifts - multilingual"""
    lang = locale if locale in ["ar", "en", "de", "de-AT", "fr", "tr", "ru", "sv", "nl", "el"] else "ar"
    result = []
    for g in ISLAMIC_GIFTS:
        gift_copy = dict(g)
        if isinstance(gift_copy.get("name"), dict):
            gift_copy["name"] = _t(gift_copy["name"], lang)
        if isinstance(gift_copy.get("description"), dict):
            gift_copy["description"] = _t(gift_copy["description"], lang)
        result.append(gift_copy)
    return {"gifts": result}

@router.post("/gifts/send")
async def send_gift(data: dict, user: dict = Depends(get_user)):
    """Send a gift to a content creator. 50% admin, 50% creator."""
    locale = data.get("locale", "ar")
    if not user:
        raise HTTPException(401, get_error("login_required", locale))
    
    gift_id = data.get("gift_id", "")
    recipient_id = data.get("recipient_id", "")
    post_id = data.get("post_id", "")
    
    gift = next((g for g in ISLAMIC_GIFTS if g["id"] == gift_id), None)
    if not gift:
        raise HTTPException(400, get_error("invalid_gift", locale))
    
    if not recipient_id:
        raise HTTPException(400, get_error("must_select_recipient", locale))
    
    if recipient_id == user["id"]:
        raise HTTPException(400, get_error("cannot_gift_self", locale))
    
    # Check sender credits
    wallet = await db.wallets.find_one({"user_id": user["id"]})
    sender_credits = wallet.get("credits", 0) if wallet else 0
    if sender_credits < gift["price_credits"]:
        raise HTTPException(400, get_error("insufficient_credits", locale))
    
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
    
    # Get localized gift name
    gift_name = _t(gift["name"], locale) if isinstance(gift.get("name"), dict) else gift.get("name", "")
    
    # Record gift transaction
    gift_record = {
        "id": str(uuid.uuid4()),
        "sender_id": user["id"],
        "sender_name": user.get("name", ""),
        "recipient_id": recipient_id,
        "post_id": post_id,
        "gift_id": gift_id,
        "gift_name": gift_name,
        "gift_emoji": gift["emoji"],
        "credits": gift["price_credits"],
        "creator_share": creator_share,
        "admin_share": admin_share,
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.gift_transactions.insert_one(gift_record)
    gift_record.pop("_id", None)
    
    new_credits = sender_credits - gift["price_credits"]
    return {"success": True, "credits_remaining": new_credits, "gift": {"id": gift["id"], "name": gift_name, "emoji": gift["emoji"]}, "message": f"{gift['emoji']} {gift_name}"}

@router.get("/gifts/received")
async def get_received_gifts(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, get_error("login_required"))
    gifts = await db.gift_transactions.find({"recipient_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"gifts": gifts}

@router.get("/gifts/on-post/{post_id}")
async def get_post_gifts(post_id: str):
    gifts = await db.gift_transactions.find({"post_id": post_id}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"gifts": gifts}


