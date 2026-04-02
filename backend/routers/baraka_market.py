"""
Router: Baraka Market (مركز المكافآت) & Ad Configuration
========================================================
Handles: Reward videos, blessing coins, golden bricks transfer, ad config
"""
from fastapi import APIRouter, HTTPException
from deps import db
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter(tags=["Baraka Market"])

# ═══ MODELS ═══
class EarnCoinsRequest(BaseModel):
    ad_type: str = "rewarded_video"  # rewarded_video, interstitial, native
    placement: str = "baraka_market"  # baraka_market, daily_feed, etc.

class TransferBricksRequest(BaseModel):
    kid_id: str
    amount: int = 50

class AdConfigUpdate(BaseModel):
    key: str
    value: str

# ═══ AD CONFIG DEFAULTS ═══
DEFAULT_AD_CONFIG = {
    "id": "global_ad_config",
    "rewards_enabled": True,
    "rewarded_video_enabled": True,
    "native_ads_enabled": True,
    "interstitial_enabled": False,
    "kids_zone_ads": False,  # ALWAYS FALSE - COPPA compliance
    "native_ad_frequency": 3,  # Show native ad after every N items
    "rewarded_video_coins": 20,
    "transfer_bricks_amount": 50,
    "daily_reward_limit": 10,  # Max reward claims per day
    "disabled_countries": [],
    "disabled_user_ids": [],
    "admob_banner_id": "ca-app-pub-3940256099942544/6300978111",  # Test IDs
    "admob_interstitial_id": "ca-app-pub-3940256099942544/1033173712",
    "admob_rewarded_id": "ca-app-pub-3940256099942544/5224354917",
    "admob_native_id": "ca-app-pub-3940256099942544/2247696110",
    "updated_at": None,
}


# ═══ WALLET ENDPOINTS ═══

@router.get("/baraka/wallet/{user_id}")
async def get_baraka_wallet(user_id: str):
    """Get user's Baraka wallet (blessing coins + golden bricks)."""
    wallet = await db.baraka_wallets.find_one({"user_id": user_id}, {"_id": 0})
    if not wallet:
        wallet = {
            "user_id": user_id,
            "blessing_coins": 0,
            "golden_bricks": 0,
            "total_earned_coins": 0,
            "total_earned_bricks": 0,
            "total_transferred_bricks": 0,
            "ads_watched_today": 0,
            "last_ad_date": None,
            "created_at": datetime.utcnow().isoformat(),
        }
        await db.baraka_wallets.insert_one({**wallet, "_id": str(uuid.uuid4())})
    return {"success": True, "wallet": wallet}


@router.post("/baraka/earn")
async def earn_blessing_coins(data: EarnCoinsRequest, user_id: str = "guest"):
    """Earn blessing coins from watching a rewarded ad."""
    # Check ad config
    config = await _get_ad_config()
    if not config.get("rewards_enabled", True):
        raise HTTPException(403, "Rewards are currently disabled")
    if not config.get("rewarded_video_enabled", True):
        raise HTTPException(403, "Rewarded videos are currently disabled")

    # Get or create wallet
    wallet = await db.baraka_wallets.find_one({"user_id": user_id})
    if not wallet:
        wallet = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "blessing_coins": 0,
            "golden_bricks": 0,
            "total_earned_coins": 0,
            "total_earned_bricks": 0,
            "total_transferred_bricks": 0,
            "ads_watched_today": 0,
            "last_ad_date": None,
            "created_at": datetime.utcnow().isoformat(),
        }
        await db.baraka_wallets.insert_one(wallet)

    # Check daily limit
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if wallet.get("last_ad_date") != today:
        await db.baraka_wallets.update_one(
            {"user_id": user_id},
            {"$set": {"ads_watched_today": 0, "last_ad_date": today}}
        )
        wallet["ads_watched_today"] = 0

    daily_limit = config.get("daily_reward_limit", 10)
    if wallet.get("ads_watched_today", 0) >= daily_limit:
        return {"success": False, "message": "Daily reward limit reached", "limit": daily_limit}

    # Grant coins
    coins = config.get("rewarded_video_coins", 20)
    await db.baraka_wallets.update_one(
        {"user_id": user_id},
        {"$inc": {"blessing_coins": coins, "total_earned_coins": coins, "ads_watched_today": 1},
         "$set": {"last_ad_date": today}}
    )

    # Log transaction
    tx = {
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "type": "earn",
        "ad_type": data.ad_type,
        "placement": data.placement,
        "amount": coins,
        "currency": "blessing_coins",
        "created_at": datetime.utcnow().isoformat(),
    }
    await db.baraka_transactions.insert_one(tx)

    updated = await db.baraka_wallets.find_one({"user_id": user_id}, {"_id": 0})
    return {
        "success": True,
        "earned": coins,
        "wallet": updated,
        "ads_remaining": daily_limit - (wallet.get("ads_watched_today", 0) + 1),
    }


@router.post("/baraka/transfer")
async def transfer_golden_bricks(data: TransferBricksRequest, user_id: str = "guest"):
    """Transfer golden bricks to a kid's account after watching a rewarded ad."""
    config = await _get_ad_config()
    if not config.get("rewards_enabled", True):
        raise HTTPException(403, "Rewards are currently disabled")

    amount = config.get("transfer_bricks_amount", 50)

    # Update parent wallet
    parent_wallet = await db.baraka_wallets.find_one({"user_id": user_id})
    if not parent_wallet:
        parent_wallet = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "blessing_coins": 0, "golden_bricks": 0,
            "total_earned_coins": 0, "total_earned_bricks": 0,
            "total_transferred_bricks": 0, "ads_watched_today": 0,
            "last_ad_date": None, "created_at": datetime.utcnow().isoformat(),
        }
        await db.baraka_wallets.insert_one(parent_wallet)

    await db.baraka_wallets.update_one(
        {"user_id": user_id},
        {"$inc": {"golden_bricks": amount, "total_earned_bricks": amount, "total_transferred_bricks": amount}}
    )

    # Update kid wallet
    kid_wallet = await db.baraka_wallets.find_one({"user_id": data.kid_id})
    if not kid_wallet:
        kid_wallet = {
            "_id": str(uuid.uuid4()),
            "user_id": data.kid_id,
            "blessing_coins": 0, "golden_bricks": 0,
            "total_earned_coins": 0, "total_earned_bricks": 0,
            "total_transferred_bricks": 0, "ads_watched_today": 0,
            "last_ad_date": None, "created_at": datetime.utcnow().isoformat(),
        }
        await db.baraka_wallets.insert_one(kid_wallet)

    await db.baraka_wallets.update_one(
        {"user_id": data.kid_id},
        {"$inc": {"golden_bricks": amount, "total_earned_bricks": amount}}
    )

    # Log transactions
    now = datetime.utcnow().isoformat()
    await db.baraka_transactions.insert_many([
        {"_id": str(uuid.uuid4()), "user_id": user_id, "type": "transfer_out",
         "amount": amount, "currency": "golden_bricks", "to_user": data.kid_id, "created_at": now},
        {"_id": str(uuid.uuid4()), "user_id": data.kid_id, "type": "transfer_in",
         "amount": amount, "currency": "golden_bricks", "from_user": user_id, "created_at": now},
    ])

    return {
        "success": True,
        "transferred": amount,
        "to_kid": data.kid_id,
        "parent_wallet": await db.baraka_wallets.find_one({"user_id": user_id}, {"_id": 0}),
    }


@router.get("/baraka/transactions/{user_id}")
async def get_baraka_transactions(user_id: str, limit: int = 20):
    """Get user's transaction history."""
    txs = await db.baraka_transactions.find(
        {"user_id": user_id}, {"_id": 0}
    ).sort("created_at", -1).limit(limit).to_list(limit)
    return {"success": True, "transactions": txs, "total": len(txs)}


@router.get("/baraka/leaderboard")
async def get_baraka_leaderboard(limit: int = 10):
    """Get top earners leaderboard."""
    top = await db.baraka_wallets.find(
        {}, {"_id": 0, "user_id": 1, "blessing_coins": 1, "total_earned_coins": 1}
    ).sort("total_earned_coins", -1).limit(limit).to_list(limit)
    return {"success": True, "leaderboard": top}


# ═══ AD CONFIGURATION (ADMIN) ═══

async def _get_ad_config() -> dict:
    """Get current ad configuration."""
    config = await db.ads_config.find_one({"id": "global_ad_config"}, {"_id": 0})
    if not config:
        config = {**DEFAULT_AD_CONFIG}
        await db.ads_config.insert_one({**config, "_id": "global_ad_config"})
    return config


@router.get("/admin/ads_config")
async def get_ads_config():
    """Get full ad configuration."""
    config = await _get_ad_config()
    return {"success": True, "config": config}


@router.post("/admin/ads_config")
async def update_ads_config(updates: dict):
    """Update ad configuration. Admin only."""
    await _get_ad_config()

    # NEVER allow kids zone ads
    if "kids_zone_ads" in updates:
        updates["kids_zone_ads"] = False  # Force COPPA compliance

    updates["updated_at"] = datetime.utcnow().isoformat()

    await db.ads_config.update_one(
        {"id": "global_ad_config"},
        {"$set": updates},
        upsert=True,
    )

    updated = await _get_ad_config()
    return {"success": True, "config": updated}


@router.get("/admin/ads_config/check_user/{user_id}")
async def check_user_ad_eligibility(user_id: str, country: str = ""):
    """Check if a user is eligible for ads."""
    config = await _get_ad_config()
    eligible = True
    reason = "eligible"

    if not config.get("rewards_enabled", True):
        eligible = False
        reason = "rewards_globally_disabled"
    elif user_id in config.get("disabled_user_ids", []):
        eligible = False
        reason = "user_disabled"
    elif country and country in config.get("disabled_countries", []):
        eligible = False
        reason = "country_disabled"

    return {"success": True, "eligible": eligible, "reason": reason, "user_id": user_id}
