"""
Router: economy
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
        raise HTTPException(401, "يجب تسجيل الدخول")
    wallet = await db.wallets.find_one({"user_id": user["id"]}, {"_id": 0})
    if not wallet:
        wallet = {"user_id": user["id"], "gold": 0, "total_earned": 0, "streak": 0, "last_daily": None}
        await db.wallets.insert_one(wallet)
        wallet.pop("_id", None)
    return {"gold": wallet.get("gold", 0), "total_earned": wallet.get("total_earned", 0), "streak": wallet.get("streak", 0)}

@router.post("/rewards/claim")
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

@router.get("/rewards/history")
async def get_reward_history(user: dict = Depends(get_user), page: int = 1, limit: int = 20):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
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

@router.get("/store/items")
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

@router.post("/store/buy-gold")
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

@router.get("/store/my-purchases")
async def get_my_purchases(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    purchases = await db.purchases.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"purchases": purchases}

# ==================== MEMBERSHIP ====================
@router.get("/membership/status")
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

@router.post("/payments/checkout")
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

@router.get("/payments/status/{session_id}")
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

@router.get("/credits/balance")
async def get_credits_balance(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    wallet = await db.wallets.find_one({"user_id": user["id"]}, {"_id": 0})
    credits = wallet.get("credits", 0) if wallet else 0
    return {"credits": credits}

@router.post("/credits/purchase")
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

@router.get("/gifts/list")
async def list_gifts():
    return {"gifts": ISLAMIC_GIFTS}

@router.post("/gifts/send")
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

@router.get("/gifts/received")
async def get_received_gifts(user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    gifts = await db.gift_transactions.find({"recipient_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"gifts": gifts}

@router.get("/gifts/on-post/{post_id}")
async def get_post_gifts(post_id: str):
    gifts = await db.gift_transactions.find({"post_id": post_id}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"gifts": gifts}


