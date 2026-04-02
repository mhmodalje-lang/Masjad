"""
Router: rewards_store
Comprehensive rewards system with:
- Profile decorations store (borders, fonts, badges, shapes, themes)
- Video ad rewards (points from watching ads)
- Level progression system (exponential difficulty)
- Kids level integration
- Admin management for ads, items, and points
"""
from fastapi import APIRouter, HTTPException, Body
from deps import db, logger
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import uuid

router = APIRouter(tags=["Rewards Store"])

# ═══════════════════════════════════════════
# LEVEL SYSTEM - 100 levels, exponential progression
# First levels easy, then gets harder and harder
# ═══════════════════════════════════════════
def generate_level_thresholds(max_level=100):
    """Generate XP thresholds for 100 levels with exponential growth."""
    thresholds = [0]  # Level 1 = 0 XP
    for i in range(1, max_level):
        if i <= 5:
            # Easy start: 50, 120, 200, 300, 420
            xp = int(50 * i + 10 * i * i)
        elif i <= 15:
            # Medium: grows faster
            xp = int(thresholds[-1] * 1.35 + 100 * i)
        elif i <= 30:
            # Hard: grows much faster
            xp = int(thresholds[-1] * 1.28 + 200 * i)
        elif i <= 50:
            # Very hard
            xp = int(thresholds[-1] * 1.22 + 500 * i)
        elif i <= 75:
            # Extreme
            xp = int(thresholds[-1] * 1.18 + 1000 * i)
        else:
            # Legendary (75-100)
            xp = int(thresholds[-1] * 1.15 + 2000 * i)
        thresholds.append(xp)
    return thresholds

LEVEL_THRESHOLDS = generate_level_thresholds(100)

def generate_kids_thresholds(max_level=50):
    """Generate kids XP thresholds - 50 levels, gentler curve."""
    thresholds = [0]
    for i in range(1, max_level):
        if i <= 5:
            xp = int(30 * i + 5 * i * i)
        elif i <= 15:
            xp = int(thresholds[-1] * 1.25 + 50 * i)
        elif i <= 30:
            xp = int(thresholds[-1] * 1.2 + 100 * i)
        else:
            xp = int(thresholds[-1] * 1.18 + 200 * i)
        thresholds.append(xp)
    return thresholds

KIDS_LEVEL_THRESHOLDS = generate_kids_thresholds(50)

def calc_level(xp: int, thresholds=None) -> dict:
    thresholds = thresholds or LEVEL_THRESHOLDS
    level = 1
    for i, t in enumerate(thresholds):
        if xp >= t:
            level = i + 1
        else:
            break
    next_threshold = thresholds[level] if level < len(thresholds) else thresholds[-1] * 2
    prev_threshold = thresholds[level - 1] if level > 0 else 0
    progress = (xp - prev_threshold) / max(1, next_threshold - prev_threshold)
    return {
        "level": level,
        "xp": xp,
        "next_level_xp": next_threshold,
        "prev_level_xp": prev_threshold,
        "progress": min(1.0, max(0.0, progress)),
        "xp_needed": max(0, next_threshold - xp),
    }


# ═══════════════════════════════════════════
# DEFAULT STORE ITEMS
# ═══════════════════════════════════════════
DEFAULT_STORE_ITEMS = [
    # --- Profile Borders ---
    {"id": "border_gold", "category": "border", "name_ar": "إطار ذهبي", "name_en": "Gold Border",
     "emoji": "🟡", "price": 100, "level_required": 1, "rarity": "common",
     "css_value": "ring-2 ring-yellow-500", "preview_color": "#EAB308"},
    {"id": "border_emerald", "category": "border", "name_ar": "إطار زمردي", "name_en": "Emerald Border",
     "emoji": "💚", "price": 200, "level_required": 2, "rarity": "common",
     "css_value": "ring-2 ring-emerald-500", "preview_color": "#10B981"},
    {"id": "border_royal", "category": "border", "name_ar": "إطار ملكي", "name_en": "Royal Border",
     "emoji": "👑", "price": 500, "level_required": 3, "rarity": "rare",
     "css_value": "ring-3 ring-purple-500 shadow-lg shadow-purple-500/30", "preview_color": "#8B5CF6"},
    {"id": "border_fire", "category": "border", "name_ar": "إطار ناري", "name_en": "Fire Border",
     "emoji": "🔥", "price": 1000, "level_required": 5, "rarity": "epic",
     "css_value": "ring-3 ring-orange-500 shadow-lg shadow-orange-500/40", "preview_color": "#F97316"},
    {"id": "border_diamond", "category": "border", "name_ar": "إطار ألماسي", "name_en": "Diamond Border",
     "emoji": "💎", "price": 3000, "level_required": 8, "rarity": "legendary",
     "css_value": "ring-4 ring-cyan-400 shadow-xl shadow-cyan-400/50", "preview_color": "#22D3EE"},
    {"id": "border_islamic", "category": "border", "name_ar": "إطار إسلامي", "name_en": "Islamic Border",
     "emoji": "🕌", "price": 5000, "level_required": 10, "rarity": "legendary",
     "css_value": "ring-4 ring-[#D4AF37] shadow-xl shadow-[#D4AF37]/40", "preview_color": "#D4AF37"},

    # --- Profile Badges ---
    {"id": "badge_star", "category": "badge", "name_ar": "نجمة ذهبية", "name_en": "Gold Star",
     "emoji": "⭐", "price": 80, "level_required": 1, "rarity": "common",
     "css_value": "⭐", "preview_color": "#FBBF24"},
    {"id": "badge_crescent", "category": "badge", "name_ar": "هلال ونجمة", "name_en": "Crescent & Star",
     "emoji": "☪️", "price": 150, "level_required": 2, "rarity": "common",
     "css_value": "☪️", "preview_color": "#10B981"},
    {"id": "badge_crown", "category": "badge", "name_ar": "تاج ذهبي", "name_en": "Gold Crown",
     "emoji": "👑", "price": 500, "level_required": 4, "rarity": "rare",
     "css_value": "👑", "preview_color": "#F59E0B"},
    {"id": "badge_flame", "category": "badge", "name_ar": "لهب نشط", "name_en": "Active Flame",
     "emoji": "🔥", "price": 800, "level_required": 5, "rarity": "rare",
     "css_value": "🔥", "preview_color": "#EF4444"},
    {"id": "badge_sword", "category": "badge", "name_ar": "سيف المعرفة", "name_en": "Sword of Knowledge",
     "emoji": "⚔️", "price": 2000, "level_required": 7, "rarity": "epic",
     "css_value": "⚔️", "preview_color": "#6366F1"},
    {"id": "badge_shield", "category": "badge", "name_ar": "درع الإيمان", "name_en": "Shield of Faith",
     "emoji": "🛡️", "price": 5000, "level_required": 10, "rarity": "legendary",
     "css_value": "🛡️", "preview_color": "#D4AF37"},

    # --- Profile Shapes ---
    {"id": "shape_circle", "category": "shape", "name_ar": "دائري", "name_en": "Circle",
     "emoji": "⭕", "price": 0, "level_required": 1, "rarity": "common",
     "css_value": "rounded-full", "preview_color": "#6B7280"},
    {"id": "shape_rounded", "category": "shape", "name_ar": "مربع مدور", "name_en": "Rounded Square",
     "emoji": "🟦", "price": 150, "level_required": 2, "rarity": "common",
     "css_value": "rounded-2xl", "preview_color": "#3B82F6"},
    {"id": "shape_hexagon", "category": "shape", "name_ar": "سداسي", "name_en": "Hexagon",
     "emoji": "⬡", "price": 600, "level_required": 4, "rarity": "rare",
     "css_value": "clip-hexagon", "preview_color": "#8B5CF6"},
    {"id": "shape_star", "category": "shape", "name_ar": "نجمي", "name_en": "Star Shape",
     "emoji": "✦", "price": 2500, "level_required": 7, "rarity": "epic",
     "css_value": "clip-star", "preview_color": "#F59E0B"},

    # --- Background Themes ---
    {"id": "theme_dark_gold", "category": "theme", "name_ar": "ذهبي داكن", "name_en": "Dark Gold",
     "emoji": "🌙", "price": 300, "level_required": 3, "rarity": "rare",
     "css_value": "bg-gradient-to-br from-yellow-900/40 to-amber-800/20", "preview_color": "#92400E"},
    {"id": "theme_ocean", "category": "theme", "name_ar": "محيط", "name_en": "Ocean",
     "emoji": "🌊", "price": 500, "level_required": 4, "rarity": "rare",
     "css_value": "bg-gradient-to-br from-blue-900/40 to-cyan-800/20", "preview_color": "#1E3A5F"},
    {"id": "theme_forest", "category": "theme", "name_ar": "غابة", "name_en": "Forest",
     "emoji": "🌲", "price": 800, "level_required": 5, "rarity": "epic",
     "css_value": "bg-gradient-to-br from-emerald-900/40 to-green-800/20", "preview_color": "#064E3B"},
    {"id": "theme_sunset", "category": "theme", "name_ar": "غروب", "name_en": "Sunset",
     "emoji": "🌅", "price": 1500, "level_required": 6, "rarity": "epic",
     "css_value": "bg-gradient-to-br from-orange-900/40 to-red-800/20", "preview_color": "#9A3412"},
    {"id": "theme_galaxy", "category": "theme", "name_ar": "مجرة", "name_en": "Galaxy",
     "emoji": "🌌", "price": 5000, "level_required": 9, "rarity": "legendary",
     "css_value": "bg-gradient-to-br from-purple-900/50 to-indigo-900/30", "preview_color": "#312E81"},
    {"id": "theme_islamic_art", "category": "theme", "name_ar": "فن إسلامي", "name_en": "Islamic Art",
     "emoji": "🕌", "price": 10000, "level_required": 12, "rarity": "legendary",
     "css_value": "bg-gradient-to-br from-[#1a472a]/50 to-[#D4AF37]/10", "preview_color": "#D4AF37"},

    # --- Name Fonts ---
    {"id": "font_bold", "category": "font", "name_ar": "خط عريض", "name_en": "Bold",
     "emoji": "𝐁", "price": 100, "level_required": 2, "rarity": "common",
     "css_value": "font-bold", "preview_color": "#6B7280"},
    {"id": "font_italic", "category": "font", "name_ar": "خط مائل", "name_en": "Italic",
     "emoji": "𝑰", "price": 150, "level_required": 2, "rarity": "common",
     "css_value": "italic", "preview_color": "#6B7280"},
    {"id": "font_gradient", "category": "font", "name_ar": "خط متدرج", "name_en": "Gradient",
     "emoji": "🎨", "price": 800, "level_required": 5, "rarity": "rare",
     "css_value": "text-gradient-islamic", "preview_color": "#D4AF37"},
    {"id": "font_glow", "category": "font", "name_ar": "خط متوهج", "name_en": "Glowing",
     "emoji": "✨", "price": 2000, "level_required": 7, "rarity": "epic",
     "css_value": "text-glow", "preview_color": "#FBBF24"},
]


# ═══════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════
class WatchAdRequest(BaseModel):
    user_id: str
    ad_id: str
    watch_duration: int = 0  # seconds watched

class PurchaseItemRequest(BaseModel):
    user_id: str
    item_id: str

class EquipItemRequest(BaseModel):
    user_id: str
    item_id: str
    slot: str  # border, badge, shape, theme, font

class UnequipItemRequest(BaseModel):
    user_id: str
    slot: str

class AdminAdRequest(BaseModel):
    title: str
    video_url: str
    thumbnail_url: str = ""
    points_reward: int = 10
    min_watch_seconds: int = 15
    enabled: bool = True

class AdminUpdateAdRequest(BaseModel):
    title: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    points_reward: Optional[int] = None
    min_watch_seconds: Optional[int] = None
    enabled: Optional[bool] = None

class AdminStoreItemRequest(BaseModel):
    id: Optional[str] = None
    category: str
    name_ar: str
    name_en: str
    emoji: str
    price: int
    level_required: int = 1
    rarity: str = "common"
    css_value: str = ""
    preview_color: str = "#6B7280"
    enabled: bool = True


# ═══════════════════════════════════════════
# INITIALIZATION - Seed store items
# ═══════════════════════════════════════════
async def ensure_store_seeded():
    """Seed default store items if collection is empty."""
    col = db["store_items"]
    count = await col.count_documents({})
    if count == 0:
        for item in DEFAULT_STORE_ITEMS:
            item["enabled"] = True
            item["created_at"] = datetime.utcnow().isoformat()
            await col.insert_one(item)
        logger.info(f"Seeded {len(DEFAULT_STORE_ITEMS)} store items")


# ═══════════════════════════════════════════
# USER POINTS & LEVEL ENDPOINTS
# ═══════════════════════════════════════════
@router.get("/rewards/profile/{user_id}")
async def get_rewards_profile(user_id: str):
    """Get user's complete rewards profile: points, level, inventory, equipped items."""
    await ensure_store_seeded()
    
    # Get or create user rewards profile
    col = db["user_rewards"]
    profile = await col.find_one({"user_id": user_id})
    if not profile:
        profile = {
            "user_id": user_id,
            "total_points": 0,
            "spent_points": 0,
            "ads_watched": 0,
            "last_ad_time": None,
            "daily_ads_count": 0,
            "daily_ads_date": None,
            "created_at": datetime.utcnow().isoformat(),
        }
        await col.insert_one(profile)
    
    available_points = profile.get("total_points", 0) - profile.get("spent_points", 0)
    level_info = calc_level(profile.get("total_points", 0))
    
    # Get inventory
    inv_col = db["user_inventory"]
    inventory = []
    async for item in inv_col.find({"user_id": user_id}):
        item.pop("_id", None)
        inventory.append(item)
    
    # Get equipped items
    eq_col = db["user_equipped"]
    equipped = {}
    async for eq in eq_col.find({"user_id": user_id}):
        equipped[eq["slot"]] = eq["item_id"]
    
    return {
        "success": True,
        "profile": {
            "user_id": user_id,
            "total_points": profile.get("total_points", 0),
            "available_points": available_points,
            "spent_points": profile.get("spent_points", 0),
            "ads_watched": profile.get("ads_watched", 0),
            "level": level_info,
            "inventory": [i["item_id"] for i in inventory],
            "equipped": equipped,
        }
    }


@router.get("/rewards/points-leaderboard")
async def get_leaderboard(limit: int = 20):
    """Get top users by points."""
    col = db["user_rewards"]
    leaders = []
    async for user in col.find().sort("total_points", -1).limit(limit):
        user.pop("_id", None)
        level_info = calc_level(user.get("total_points", 0))
        leaders.append({
            "user_id": user["user_id"],
            "total_points": user.get("total_points", 0),
            "level": level_info["level"],
            "ads_watched": user.get("ads_watched", 0),
        })
    return {"success": True, "leaderboard": leaders}


# ═══════════════════════════════════════════
# AD REWARD SYSTEM
# ═══════════════════════════════════════════
@router.get("/rewards/ads")
async def get_available_ads(user_id: str = ""):
    """Get list of available reward ads for user."""
    col = db["reward_ads"]
    ads = []
    async for ad in col.find({"enabled": True}):
        ad.pop("_id", None)
        ads.append({
            "id": ad["id"],
            "title": ad["title"],
            "video_url": ad["video_url"],
            "thumbnail_url": ad.get("thumbnail_url", ""),
            "points_reward": ad["points_reward"],
            "min_watch_seconds": ad.get("min_watch_seconds", 15),
        })
    
    # Check user cooldown
    can_watch = True
    cooldown_remaining = 0
    next_ad_time = None
    if user_id:
        rewards_col = db["user_rewards"]
        profile = await rewards_col.find_one({"user_id": user_id})
        if profile and profile.get("last_ad_time"):
            last_time = datetime.fromisoformat(profile["last_ad_time"])
            cooldown_end = last_time + timedelta(seconds=30)
            if datetime.utcnow() < cooldown_end:
                can_watch = False
                cooldown_remaining = int((cooldown_end - datetime.utcnow()).total_seconds())
                next_ad_time = cooldown_end.isoformat()
        
        # Check daily limit (max 20 ads per day)
        today = datetime.utcnow().date().isoformat()
        if profile and profile.get("daily_ads_date") == today:
            if profile.get("daily_ads_count", 0) >= 20:
                can_watch = False
    
    return {
        "success": True,
        "ads": ads,
        "can_watch": can_watch,
        "cooldown_remaining": cooldown_remaining,
        "next_ad_time": next_ad_time,
    }


@router.post("/rewards/ads/watch")
async def complete_ad_watch(req: WatchAdRequest):
    """Record ad watch completion and award points."""
    # Verify ad exists
    ad_col = db["reward_ads"]
    ad = await ad_col.find_one({"id": req.ad_id, "enabled": True})
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    
    min_watch = ad.get("min_watch_seconds", 15)
    if req.watch_duration < min_watch:
        return {"success": False, "message": "incomplete_watch", "required_seconds": min_watch}
    
    # Check cooldown
    rewards_col = db["user_rewards"]
    profile = await rewards_col.find_one({"user_id": req.user_id})
    
    now = datetime.utcnow()
    today = now.date().isoformat()
    
    if profile:
        if profile.get("last_ad_time"):
            last_time = datetime.fromisoformat(profile["last_ad_time"])
            if (now - last_time).total_seconds() < 30:
                return {"success": False, "message": "cooldown_active"}
        
        if profile.get("daily_ads_date") == today and profile.get("daily_ads_count", 0) >= 20:
            return {"success": False, "message": "daily_limit_reached"}
    
    points = ad["points_reward"]
    
    # Update or create profile
    if profile:
        daily_count = profile.get("daily_ads_count", 0) if profile.get("daily_ads_date") == today else 0
        await rewards_col.update_one(
            {"user_id": req.user_id},
            {"$set": {
                "total_points": profile.get("total_points", 0) + points,
                "ads_watched": profile.get("ads_watched", 0) + 1,
                "last_ad_time": now.isoformat(),
                "daily_ads_count": daily_count + 1,
                "daily_ads_date": today,
            }}
        )
    else:
        await rewards_col.insert_one({
            "user_id": req.user_id,
            "total_points": points,
            "spent_points": 0,
            "ads_watched": 1,
            "last_ad_time": now.isoformat(),
            "daily_ads_count": 1,
            "daily_ads_date": today,
            "created_at": now.isoformat(),
        })
    
    # Log ad view
    await db["ad_views"].insert_one({
        "id": str(uuid.uuid4()),
        "user_id": req.user_id,
        "ad_id": req.ad_id,
        "points_earned": points,
        "watch_duration": req.watch_duration,
        "timestamp": now.isoformat(),
    })
    
    new_total = (profile.get("total_points", 0) if profile else 0) + points
    new_level = calc_level(new_total)
    old_level = calc_level(new_total - points)
    level_up = new_level["level"] > old_level["level"]
    
    return {
        "success": True,
        "points_earned": points,
        "new_total": new_total,
        "available_points": new_total - (profile.get("spent_points", 0) if profile else 0),
        "level": new_level,
        "level_up": level_up,
    }


# ═══════════════════════════════════════════
# STORE - BROWSE & PURCHASE
# ═══════════════════════════════════════════
@router.get("/rewards/store")
async def get_store_items(category: str = "all", locale: str = "ar"):
    """Get all store items, optionally filtered by category."""
    await ensure_store_seeded()
    
    col = db["store_items"]
    query = {"enabled": True}
    if category != "all":
        query["category"] = category
    
    items = []
    async for item in col.find(query).sort("price", 1):
        item.pop("_id", None)
        lang_key = f"name_{locale}" if f"name_{locale}" in item else "name_en"
        items.append({
            "id": item["id"],
            "category": item["category"],
            "name": item.get(lang_key, item.get("name_en", "")),
            "name_ar": item.get("name_ar", ""),
            "name_en": item.get("name_en", ""),
            "emoji": item["emoji"],
            "price": item["price"],
            "level_required": item.get("level_required", 1),
            "rarity": item.get("rarity", "common"),
            "css_value": item.get("css_value", ""),
            "preview_color": item.get("preview_color", "#6B7280"),
        })
    
    categories = [
        {"id": "border", "name_ar": "إطارات", "name_en": "Borders", "emoji": "🖼️"},
        {"id": "badge", "name_ar": "شارات", "name_en": "Badges", "emoji": "🏅"},
        {"id": "shape", "name_ar": "أشكال", "name_en": "Shapes", "emoji": "⬡"},
        {"id": "theme", "name_ar": "خلفيات", "name_en": "Themes", "emoji": "🎨"},
        {"id": "font", "name_ar": "خطوط", "name_en": "Fonts", "emoji": "✍️"},
    ]
    
    return {"success": True, "items": items, "categories": categories, "total": len(items)}


@router.post("/rewards/store/purchase")
async def purchase_item(req: PurchaseItemRequest):
    """Purchase a store item using points."""
    await ensure_store_seeded()
    
    # Get item
    item_col = db["store_items"]
    item = await item_col.find_one({"id": req.item_id, "enabled": True})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if already owned
    inv_col = db["user_inventory"]
    existing = await inv_col.find_one({"user_id": req.user_id, "item_id": req.item_id})
    if existing:
        return {"success": False, "message": "already_owned"}
    
    # Check points
    rewards_col = db["user_rewards"]
    profile = await rewards_col.find_one({"user_id": req.user_id})
    if not profile:
        return {"success": False, "message": "no_points"}
    
    available = profile.get("total_points", 0) - profile.get("spent_points", 0)
    if available < item["price"]:
        return {"success": False, "message": "insufficient_points", "needed": item["price"] - available}
    
    # Check level
    level_info = calc_level(profile.get("total_points", 0))
    if level_info["level"] < item.get("level_required", 1):
        return {"success": False, "message": "level_too_low", "required_level": item["level_required"]}
    
    # Deduct points and add to inventory
    await rewards_col.update_one(
        {"user_id": req.user_id},
        {"$set": {"spent_points": profile.get("spent_points", 0) + item["price"]}}
    )
    
    await inv_col.insert_one({
        "user_id": req.user_id,
        "item_id": req.item_id,
        "category": item["category"],
        "purchased_at": datetime.utcnow().isoformat(),
    })
    
    new_available = available - item["price"]
    return {
        "success": True,
        "item_id": req.item_id,
        "points_spent": item["price"],
        "available_points": new_available,
    }


@router.post("/rewards/store/equip")
async def equip_item(req: EquipItemRequest):
    """Equip a decoration item."""
    inv_col = db["user_inventory"]
    owned = await inv_col.find_one({"user_id": req.user_id, "item_id": req.item_id})
    if not owned:
        # Check if it's a free item (price=0)
        item_col = db["store_items"]
        item = await item_col.find_one({"id": req.item_id, "price": 0})
        if not item:
            return {"success": False, "message": "not_owned"}
    
    eq_col = db["user_equipped"]
    await eq_col.update_one(
        {"user_id": req.user_id, "slot": req.slot},
        {"$set": {"user_id": req.user_id, "slot": req.slot, "item_id": req.item_id}},
        upsert=True
    )
    return {"success": True, "slot": req.slot, "item_id": req.item_id}


@router.post("/rewards/store/unequip")
async def unequip_item(req: UnequipItemRequest):
    """Remove a decoration from a slot."""
    eq_col = db["user_equipped"]
    await eq_col.delete_one({"user_id": req.user_id, "slot": req.slot})
    return {"success": True, "slot": req.slot}


@router.get("/rewards/user-decorations/{user_id}")
async def get_user_decorations(user_id: str):
    """Get a user's active decorations (for displaying on their profile)."""
    eq_col = db["user_equipped"]
    equipped = {}
    async for eq in eq_col.find({"user_id": user_id}):
        equipped[eq["slot"]] = eq["item_id"]
    
    # Get item details for equipped items
    item_col = db["store_items"]
    decoration_details = {}
    for slot, item_id in equipped.items():
        item = await item_col.find_one({"id": item_id})
        if item:
            decoration_details[slot] = {
                "item_id": item_id,
                "css_value": item.get("css_value", ""),
                "emoji": item.get("emoji", ""),
                "name_ar": item.get("name_ar", ""),
                "name_en": item.get("name_en", ""),
                "rarity": item.get("rarity", "common"),
                "preview_color": item.get("preview_color", ""),
            }
    
    # Get level
    rewards_col = db["user_rewards"]
    profile = await rewards_col.find_one({"user_id": user_id})
    level_info = calc_level(profile.get("total_points", 0) if profile else 0)
    
    return {
        "success": True,
        "decorations": decoration_details,
        "level": level_info,
    }


# ═══════════════════════════════════════════
# KIDS LEVEL SYSTEM
# ═══════════════════════════════════════════
@router.get("/rewards/kids-level/{user_id}")
async def get_kids_level(user_id: str):
    """Get kid's level based on their learning XP."""
    # Get XP from kids progress
    progress_col = db["kids_curriculum_progress"]
    progress = await progress_col.find_one({"user_id": user_id})
    xp = progress.get("total_xp", 0) if progress else 0
    
    # Also count lesson completions
    points_col = db["user_rewards"]
    await points_col.find_one({"user_id": user_id})
    
    level_info = calc_level(xp, KIDS_LEVEL_THRESHOLDS)
    
    return {
        "success": True,
        "xp": xp,
        "level": level_info,
    }


@router.post("/rewards/kids-level/add-xp")
async def add_kids_xp(user_id: str = Body(...), xp: int = Body(...)):
    """Add XP to kids level from lesson completion."""
    progress_col = db["kids_curriculum_progress"]
    progress = await progress_col.find_one({"user_id": user_id})
    current_xp = progress.get("total_xp", 0) if progress else 0
    new_xp = current_xp + xp
    
    if progress:
        await progress_col.update_one({"user_id": user_id}, {"$set": {"total_xp": new_xp}})
    
    old_level = calc_level(current_xp, KIDS_LEVEL_THRESHOLDS)
    new_level = calc_level(new_xp, KIDS_LEVEL_THRESHOLDS)
    
    return {
        "success": True,
        "xp": new_xp,
        "level": new_level,
        "level_up": new_level["level"] > old_level["level"],
    }


# ═══════════════════════════════════════════
# ADMIN ENDPOINTS
# ═══════════════════════════════════════════
@router.get("/admin/rewards/stats")
async def admin_rewards_stats():
    """Get overall rewards system statistics."""
    rewards_col = db["user_rewards"]
    store_col = db["store_items"]
    ad_col = db["reward_ads"]
    inv_col = db["user_inventory"]
    views_col = db["ad_views"]
    
    total_users = await rewards_col.count_documents({})
    total_items = await store_col.count_documents({"enabled": True})
    total_ads = await ad_col.count_documents({"enabled": True})
    total_purchases = await inv_col.count_documents({})
    total_ad_views = await views_col.count_documents({})
    
    # Sum total points
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$total_points"}, "spent": {"$sum": "$spent_points"}}}]
    result = await rewards_col.aggregate(pipeline).to_list(1)
    total_points_issued = result[0]["total"] if result else 0
    total_points_spent = result[0]["spent"] if result else 0
    
    return {
        "success": True,
        "stats": {
            "total_users": total_users,
            "total_store_items": total_items,
            "total_active_ads": total_ads,
            "total_purchases": total_purchases,
            "total_ad_views": total_ad_views,
            "total_points_issued": total_points_issued,
            "total_points_spent": total_points_spent,
        }
    }


@router.get("/admin/rewards/ads")
async def admin_get_ads():
    """Get all ads (including disabled) for admin management."""
    col = db["reward_ads"]
    ads = []
    async for ad in col.find():
        ad.pop("_id", None)
        ads.append(ad)
    return {"success": True, "ads": ads}


@router.post("/admin/rewards/ads")
async def admin_create_ad(req: AdminAdRequest):
    """Create a new reward ad."""
    col = db["reward_ads"]
    ad = {
        "id": str(uuid.uuid4())[:8],
        "title": req.title,
        "video_url": req.video_url,
        "thumbnail_url": req.thumbnail_url,
        "points_reward": req.points_reward,
        "min_watch_seconds": req.min_watch_seconds,
        "enabled": req.enabled,
        "created_at": datetime.utcnow().isoformat(),
        "total_views": 0,
    }
    await col.insert_one(ad)
    ad.pop("_id", None)
    return {"success": True, "ad": ad}


@router.put("/admin/rewards/ads/{ad_id}")
async def admin_update_ad(ad_id: str, req: AdminUpdateAdRequest):
    """Update an existing ad."""
    col = db["reward_ads"]
    update = {}
    for field in ["title", "video_url", "thumbnail_url", "points_reward", "min_watch_seconds", "enabled"]:
        val = getattr(req, field, None)
        if val is not None:
            update[field] = val
    
    if update:
        await col.update_one({"id": ad_id}, {"$set": update})
    
    return {"success": True}


@router.delete("/admin/rewards/ads/{ad_id}")
async def admin_delete_ad(ad_id: str):
    """Delete an ad."""
    await db["reward_ads"].delete_one({"id": ad_id})
    return {"success": True}


@router.post("/admin/rewards/store-item")
async def admin_create_store_item(req: AdminStoreItemRequest):
    """Create or update a store item."""
    col = db["store_items"]
    item_id = req.id or f"{req.category}_{str(uuid.uuid4())[:6]}"
    
    item = {
        "id": item_id,
        "category": req.category,
        "name_ar": req.name_ar,
        "name_en": req.name_en,
        "emoji": req.emoji,
        "price": req.price,
        "level_required": req.level_required,
        "rarity": req.rarity,
        "css_value": req.css_value,
        "preview_color": req.preview_color,
        "enabled": req.enabled,
        "created_at": datetime.utcnow().isoformat(),
    }
    
    await col.update_one({"id": item_id}, {"$set": item}, upsert=True)
    return {"success": True, "item": item}


@router.delete("/admin/rewards/store-item/{item_id}")
async def admin_delete_store_item(item_id: str):
    """Delete a store item."""
    await db["store_items"].delete_one({"id": item_id})
    return {"success": True}


@router.get("/admin/rewards/ad-analytics")
async def admin_ad_analytics():
    """Get ad viewing analytics."""
    views_col = db["ad_views"]
    
    # Group by ad
    pipeline = [
        {"$group": {
            "_id": "$ad_id",
            "total_views": {"$sum": 1},
            "total_points": {"$sum": "$points_earned"},
            "avg_duration": {"$avg": "$watch_duration"},
        }}
    ]
    analytics = await views_col.aggregate(pipeline).to_list(100)
    
    return {"success": True, "analytics": analytics}
