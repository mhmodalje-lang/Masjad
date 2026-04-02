"""
Router: gamification
====================
Unified Points System: Golden Bricks (Kids) + Blessing Points (Adults)
Rewarded Ads Engine + Parental Gate (Math Lock)
"""
from fastapi import APIRouter, HTTPException
from deps import db
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, date, timedelta
import uuid
import random

router = APIRouter(tags=["Gamification"])

# ======================== CONSTANTS ========================

# Google Test Ad Unit IDs (Official - safe for development)
GOOGLE_TEST_AD_UNITS = {
    "rewarded": "ca-app-pub-3940256099942544/5224354917",
    "interstitial": "ca-app-pub-3940256099942544/1033173712",
    "banner": "ca-app-pub-3940256099942544/6300978111",
    "rewarded_interstitial": "ca-app-pub-3940256099942544/5354046379",
    "native": "ca-app-pub-3940256099942544/2247696110",
}

# Points configuration
KIDS_REWARDS = {
    "lesson_complete": 10,
    "quiz_perfect": 20,
    "daily_streak": 5,
    "mosque_part_earned": 15,
    "game_won": 8,
    "letter_mastered": 12,
    "surah_memorized": 50,
    "ad_watched": 25,
    "challenge_complete": 30,
    "wudu_practiced": 10,
    "salah_practiced": 15,
}

ADULT_REWARDS = {
    "daily_login": 10,
    "prayer_logged": 5,
    "quran_page_read": 8,
    "tasbeeh_100": 3,
    "dua_memorized": 15,
    "hadith_shared": 5,
    "post_created": 5,
    "community_help": 10,
    "streak_7_days": 50,
    "streak_30_days": 200,
    "ad_watched": 15,
    "donation_made": 25,
}

# Mosque building stages (Kids - Golden Bricks)
MOSQUE_STAGES = [
    {"stage": "foundation", "bricks_needed": 0, "emoji": "🧱", "name_key": "mosque_foundation"},
    {"stage": "walls", "bricks_needed": 50, "emoji": "🏗️", "name_key": "mosque_walls"},
    {"stage": "pillars", "bricks_needed": 120, "emoji": "🏛️", "name_key": "mosque_pillars"},
    {"stage": "dome_base", "bricks_needed": 200, "emoji": "⛪", "name_key": "mosque_dome_base"},
    {"stage": "dome", "bricks_needed": 300, "emoji": "🕌", "name_key": "mosque_dome"},
    {"stage": "minaret", "bricks_needed": 450, "emoji": "🗼", "name_key": "mosque_minaret"},
    {"stage": "garden", "bricks_needed": 600, "emoji": "🌳", "name_key": "mosque_garden"},
    {"stage": "golden_dome", "bricks_needed": 800, "emoji": "✨", "name_key": "mosque_golden_dome"},
    {"stage": "complete", "bricks_needed": 1000, "emoji": "🕋", "name_key": "mosque_complete"},
]

# Adult spiritual ranks (Blessing Points)
SPIRITUAL_RANKS = [
    {"rank": "seeker", "points_needed": 0, "emoji": "🌱", "name_key": "rank_seeker"},
    {"rank": "learner", "points_needed": 100, "emoji": "📖", "name_key": "rank_learner"},
    {"rank": "devoted", "points_needed": 300, "emoji": "🤲", "name_key": "rank_devoted"},
    {"rank": "steadfast", "points_needed": 600, "emoji": "⭐", "name_key": "rank_steadfast"},
    {"rank": "knowledgeable", "points_needed": 1000, "emoji": "🌟", "name_key": "rank_knowledgeable"},
    {"rank": "hafiz", "points_needed": 2000, "emoji": "📜", "name_key": "rank_hafiz"},
    {"rank": "mumin", "points_needed": 3500, "emoji": "💎", "name_key": "rank_mumin"},
    {"rank": "muhsin", "points_needed": 5000, "emoji": "🌙", "name_key": "rank_muhsin"},
    {"rank": "muttaqin", "points_needed": 10000, "emoji": "☀️", "name_key": "rank_muttaqin"},
]


# ======================== MODELS ========================

class EarnPointsRequest(BaseModel):
    user_id: str
    mode: str = "adults"  # "kids" or "adults"
    reward_type: str
    metadata: Optional[Dict[str, Any]] = None

class AdWatchedRequest(BaseModel):
    user_id: str
    mode: str = "adults"
    ad_type: str = "rewarded"  # rewarded, interstitial, banner
    ad_unit_id: Optional[str] = None
    content_to_unlock: Optional[str] = None  # lesson_id, mosque_part, etc.
    duration_seconds: Optional[int] = None

class ParentalGateVerify(BaseModel):
    user_id: str
    challenge_id: str
    answer: int

class UnlockContentRequest(BaseModel):
    user_id: str
    content_type: str  # "premium_lesson", "mosque_part", "story", "quiz_pack"
    content_id: str
    cost_bricks: int = 0

class ParentalConsentRequest(BaseModel):
    user_id: str
    consent: bool = True

class LessonPointsRequest(BaseModel):
    user_id: str
    mode: str = "kids"
    lesson_id: Optional[str] = None

class RedeemRewardRequest(BaseModel):
    user_id: str
    mode: str = "adults"
    reward_id: str
    cost: int


# ======================== HELPERS ========================

def get_mosque_stage(bricks: int) -> dict:
    """Get current mosque building stage based on bricks."""
    current = MOSQUE_STAGES[0]
    for stage in MOSQUE_STAGES:
        if bricks >= stage["bricks_needed"]:
            current = stage
        else:
            break
    next_stage = None
    idx = MOSQUE_STAGES.index(current)
    if idx < len(MOSQUE_STAGES) - 1:
        next_stage = MOSQUE_STAGES[idx + 1]
    return {
        "current": current,
        "next": next_stage,
        "progress_percent": min(100, int((bricks / max(1, next_stage["bricks_needed"] if next_stage else current["bricks_needed"])) * 100)),
    }

def get_spiritual_rank(points: int) -> dict:
    """Get current spiritual rank based on blessing points."""
    current = SPIRITUAL_RANKS[0]
    for rank in SPIRITUAL_RANKS:
        if points >= rank["points_needed"]:
            current = rank
        else:
            break
    next_rank = None
    idx = SPIRITUAL_RANKS.index(current)
    if idx < len(SPIRITUAL_RANKS) - 1:
        next_rank = SPIRITUAL_RANKS[idx + 1]
    return {
        "current": current,
        "next": next_rank,
        "progress_percent": min(100, int((points / max(1, next_rank["points_needed"] if next_rank else current["points_needed"])) * 100)),
    }


# ======================== POINTS BALANCE ========================

@router.get("/points/balance")
async def get_points_balance(user_id: str, mode: str = "adults"):
    """Get unified points balance - Golden Bricks (kids) or Blessing Points (adults)."""
    collection = "kids_points" if mode == "kids" else "adult_points"
    profile = await db[collection].find_one({"user_id": user_id}, {"_id": 0})

    if not profile:
        profile = {
            "user_id": user_id,
            "mode": mode,
            "points": 0,
            "total_earned": 0,
            "streak": 0,
            "last_active": None,
            "ads_watched": 0,
            "unlocked_content": [],
            "created_at": datetime.utcnow().isoformat(),
        }
        await db[collection].insert_one({**profile})

    if mode == "kids":
        mosque = get_mosque_stage(profile.get("points", 0))
        return {
            "success": True,
            "mode": "kids",
            "golden_bricks": profile.get("points", 0),
            "total_earned": profile.get("total_earned", 0),
            "streak": profile.get("streak", 0),
            "mosque": mosque,
            "ads_watched": profile.get("ads_watched", 0),
            "unlocked_content": profile.get("unlocked_content", []),
        }
    else:
        rank = get_spiritual_rank(profile.get("points", 0))
        return {
            "success": True,
            "mode": "adults",
            "blessing_points": profile.get("points", 0),
            "total_earned": profile.get("total_earned", 0),
            "streak": profile.get("streak", 0),
            "rank": rank,
            "ads_watched": profile.get("ads_watched", 0),
            "unlocked_content": profile.get("unlocked_content", []),
        }


# ======================== EARN POINTS ========================

@router.post("/points/earn")
def _calculate_streak(last_active: str, current_streak: int) -> int:
    """Calculate updated streak based on last active date."""
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    if last_active == today:
        return current_streak
    if last_active == yesterday:
        return current_streak + 1
    return 1


async def _ensure_points_profile(user_id: str, mode: str, collection: str) -> dict:
    """Get or create a points profile for the user."""
    profile = await db[collection].find_one({"user_id": user_id})
    if not profile:
        profile = {
            "user_id": user_id, "mode": mode, "points": 0, "total_earned": 0,
            "streak": 0, "last_active": None, "ads_watched": 0,
            "unlocked_content": [], "created_at": datetime.utcnow().isoformat(),
        }
        await db[collection].insert_one({**profile})
    return profile


@router.post("/points/earn")
async def earn_points(data: EarnPointsRequest):
    """Earn points for completing activities."""
    rewards = KIDS_REWARDS if data.mode == "kids" else ADULT_REWARDS
    points = rewards.get(data.reward_type, 0)
    if points == 0:
        raise HTTPException(status_code=400, detail="Invalid reward type")

    collection = "kids_points" if data.mode == "kids" else "adult_points"
    profile = await _ensure_points_profile(data.user_id, data.mode, collection)

    streak = _calculate_streak(profile.get("last_active", ""), profile.get("streak", 0))
    streak_bonus = rewards.get("daily_streak", 5) * 3 if (streak > 0 and streak % 7 == 0) else 0
    total_earn = points + streak_bonus

    await db[collection].update_one(
        {"user_id": data.user_id},
        {"$inc": {"points": total_earn, "total_earned": total_earn}, "$set": {"last_active": date.today().isoformat(), "streak": streak}},
        upsert=True,
    )
    await db.points_transactions.insert_one({
        "id": str(uuid.uuid4()), "user_id": data.user_id, "mode": data.mode,
        "type": data.reward_type, "points": total_earn, "streak": streak,
        "streak_bonus": streak_bonus, "metadata": data.metadata or {},
        "created_at": datetime.utcnow().isoformat(),
    })

    new_total = profile.get("points", 0) + total_earn
    result = {"success": True, "earned": total_earn, "streak_bonus": streak_bonus, "streak": streak, "new_total": new_total}
    if data.mode == "kids":
        result["golden_bricks"] = new_total
        result["mosque"] = get_mosque_stage(new_total)
    else:
        result["blessing_points"] = new_total
        result["rank"] = get_spiritual_rank(new_total)
    return result


# ======================== REWARDED ADS ========================

@router.get("/rewards/ad-config")
async def get_ad_config():
    """Get rewarded ad configuration with test unit IDs."""
    # Check if production keys exist in settings
    settings = await db.app_settings.find_one({"key": "global"}, {"_id": 0}) or {}
    use_test = not settings.get("admob_live_mode", False)

    ad_units = GOOGLE_TEST_AD_UNITS if use_test else {
        "rewarded": settings.get("admob_rewarded_id", GOOGLE_TEST_AD_UNITS["rewarded"]),
        "interstitial": settings.get("admob_interstitial_id", GOOGLE_TEST_AD_UNITS["interstitial"]),
        "banner": settings.get("admob_banner_id", GOOGLE_TEST_AD_UNITS["banner"]),
    }

    return {
        "success": True,
        "test_mode": use_test,
        "ad_units": ad_units,
        "rewards": {
            "kids_ad_watched": KIDS_REWARDS["ad_watched"],
            "adults_ad_watched": ADULT_REWARDS["ad_watched"],
        },
        "parental_gate_required": True,
    }


@router.post("/rewards/ad-watched")
async def reward_ad_watched(data: AdWatchedRequest):
    """Process rewarded ad completion - triggers point earning."""
    rewards = KIDS_REWARDS if data.mode == "kids" else ADULT_REWARDS
    points = rewards.get("ad_watched", 15)

    collection = "kids_points" if data.mode == "kids" else "adult_points"

    # Rate limit: max 5 rewarded ads per day
    today = date.today().isoformat()
    today_ads = await db.ad_watch_log.count_documents({
        "user_id": data.user_id,
        "date": today,
    })

    if today_ads >= 5:
        return {
            "success": False,
            "message": "daily_ad_limit_reached",
            "max_daily": 5,
            "watched_today": today_ads,
        }

    # Log the ad watch
    await db.ad_watch_log.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": data.user_id,
        "mode": data.mode,
        "ad_type": data.ad_type,
        "ad_unit_id": data.ad_unit_id or "",
        "content_unlocked": data.content_to_unlock or "",
        "duration_seconds": data.duration_seconds or 0,
        "date": today,
        "timestamp": datetime.utcnow().isoformat(),
    })

    # Award points
    await db[collection].update_one(
        {"user_id": data.user_id},
        {
            "$inc": {"points": points, "total_earned": points, "ads_watched": 1},
        },
        upsert=True,
    )

    # Log transaction
    await db.points_transactions.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": data.user_id,
        "mode": data.mode,
        "type": "ad_watched",
        "points": points,
        "metadata": {"ad_type": data.ad_type, "content_unlocked": data.content_to_unlock},
        "created_at": datetime.utcnow().isoformat(),
    })

    # Unlock content if specified
    unlocked = None
    if data.content_to_unlock:
        await db[collection].update_one(
            {"user_id": data.user_id},
            {"$addToSet": {"unlocked_content": data.content_to_unlock}},
        )
        unlocked = data.content_to_unlock

    profile = await db[collection].find_one({"user_id": data.user_id}, {"_id": 0})
    new_total = profile.get("points", 0) if profile else points

    result = {
        "success": True,
        "points_earned": points,
        "new_total": new_total,
        "ads_watched_today": today_ads + 1,
        "max_daily": 5,
        "content_unlocked": unlocked,
    }

    if data.mode == "kids":
        result["golden_bricks"] = new_total
        result["mosque"] = get_mosque_stage(new_total)
    else:
        result["blessing_points"] = new_total
        result["rank"] = get_spiritual_rank(new_total)

    return result


# ======================== UNLOCK PREMIUM CONTENT ========================

@router.post("/rewards/unlock-content")
async def unlock_content(data: UnlockContentRequest):
    """Unlock premium content using points/bricks."""
    collection = "kids_points"  # Only kids use bricks to unlock
    profile = await db[collection].find_one({"user_id": data.user_id}, {"_id": 0})

    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    current_bricks = profile.get("points", 0)
    if current_bricks < data.cost_bricks:
        raise HTTPException(status_code=400, detail="Not enough bricks")

    # Check if already unlocked
    if data.content_id in profile.get("unlocked_content", []):
        return {"success": True, "already_unlocked": True}

    # Deduct bricks and unlock
    await db[collection].update_one(
        {"user_id": data.user_id},
        {
            "$inc": {"points": -data.cost_bricks},
            "$addToSet": {"unlocked_content": data.content_id},
        },
    )

    return {
        "success": True,
        "content_unlocked": data.content_id,
        "bricks_spent": data.cost_bricks,
        "remaining_bricks": current_bricks - data.cost_bricks,
    }


# ======================== PARENTAL GATE (MATH LOCK) ========================

# In-memory challenge store (simple, no DB needed for ephemeral challenges)
_active_challenges: Dict[str, dict] = {}

@router.get("/parental-gate/challenge")
async def get_parental_challenge(user_id: str):
    """Generate a math challenge for parental gate."""
    # Generate age-appropriate math problem
    challenge_type = random.choice(["addition", "subtraction", "multiplication"])

    if challenge_type == "addition":
        a = random.randint(3, 15)
        b = random.randint(2, 12)
        answer = a + b
        question = f"{a} + {b} = ?"
    elif challenge_type == "subtraction":
        a = random.randint(10, 20)
        b = random.randint(2, a - 1)
        answer = a - b
        question = f"{a} - {b} = ?"
    else:  # multiplication
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        answer = a * b
        question = f"{a} × {b} = ?"

    challenge_id = str(uuid.uuid4())[:12]

    # Store challenge (expires in 5 minutes)
    _active_challenges[challenge_id] = {
        "answer": answer,
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "attempts": 0,
    }

    # Cleanup old challenges (older than 10 min)
    now = datetime.utcnow()
    expired = [k for k, v in _active_challenges.items() if (now - v["created_at"]).seconds > 600]
    for k in expired:
        del _active_challenges[k]

    return {
        "success": True,
        "challenge_id": challenge_id,
        "question": question,
        "challenge_type": challenge_type,
        "hint": "Only parents/adults should answer this",
    }


@router.post("/parental-gate/verify")
async def verify_parental_gate(data: ParentalGateVerify):
    """Verify parental gate math answer."""
    challenge = _active_challenges.get(data.challenge_id)

    if not challenge:
        raise HTTPException(status_code=400, detail="Challenge expired or invalid")

    if challenge["user_id"] != data.user_id:
        raise HTTPException(status_code=403, detail="Challenge belongs to different user")

    challenge["attempts"] += 1

    if challenge["attempts"] > 3:
        del _active_challenges[data.challenge_id]
        return {
            "success": False,
            "passed": False,
            "message": "too_many_attempts",
            "max_attempts": 3,
        }

    if data.answer == challenge["answer"]:
        # Success - remove challenge
        del _active_challenges[data.challenge_id]

        # Create a temporary pass token (valid 15 min)
        pass_token = str(uuid.uuid4())
        await db.parental_passes.insert_one({
            "token": pass_token,
            "user_id": data.user_id,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(minutes=15)).isoformat(),
        })

        return {
            "success": True,
            "passed": True,
            "pass_token": pass_token,
            "valid_minutes": 15,
        }
    else:
        return {
            "success": True,
            "passed": False,
            "message": "wrong_answer",
            "attempts_remaining": 3 - challenge["attempts"],
        }


@router.get("/parental-gate/check-pass")
async def check_parental_pass(user_id: str, token: str):
    """Check if a parental gate pass is still valid."""
    pass_doc = await db.parental_passes.find_one({
        "token": token,
        "user_id": user_id,
    }, {"_id": 0})

    if not pass_doc:
        return {"valid": False}

    expires = datetime.fromisoformat(pass_doc["expires_at"])
    if datetime.utcnow() > expires:
        await db.parental_passes.delete_one({"token": token})
        return {"valid": False}

    return {"valid": True, "expires_at": pass_doc["expires_at"]}


# ======================== POINTS HISTORY ========================

@router.get("/points/history")
async def get_points_history(user_id: str, mode: str = "adults", limit: int = 50):
    """Get points transaction history."""
    transactions = await db.points_transactions.find(
        {"user_id": user_id, "mode": mode},
        {"_id": 0},
    ).sort("created_at", -1).to_list(limit)

    return {
        "success": True,
        "transactions": transactions,
        "total": len(transactions),
    }


# ======================== LEADERBOARD ========================

@router.get("/points/leaderboard")
async def get_leaderboard(mode: str = "adults", limit: int = 20):
    """Get top users leaderboard."""
    collection = "kids_points" if mode == "kids" else "adult_points"

    top_users = await db[collection].find(
        {},
        {"_id": 0, "user_id": 1, "points": 1, "streak": 1, "total_earned": 1},
    ).sort("points", -1).to_list(limit)

    # Enrich with user display names
    leaderboard = []
    for i, entry in enumerate(top_users):
        user = await db.users.find_one({"id": entry["user_id"]}, {"_id": 0, "name": 1, "avatar": 1})
        display_name = user.get("name", entry["user_id"][:8]) if user else entry["user_id"][:8]

        item = {
            "rank": i + 1,
            "user_id": entry["user_id"],
            "display_name": display_name,
            "points": entry.get("points", 0),
            "streak": entry.get("streak", 0),
        }

        if mode == "kids":
            item["golden_bricks"] = entry.get("points", 0)
            item["mosque_stage"] = get_mosque_stage(entry.get("points", 0))["current"]["stage"]
        else:
            item["blessing_points"] = entry.get("points", 0)
            item["spiritual_rank"] = get_spiritual_rank(entry.get("points", 0))["current"]["rank"]

        leaderboard.append(item)

    return {
        "success": True,
        "mode": mode,
        "leaderboard": leaderboard,
        "total": len(leaderboard),
    }


# ======================== PREMIUM CONTENT CATALOG ========================

@router.get("/rewards/premium-catalog")
async def get_premium_catalog(mode: str = "kids", locale: str = "en"):
    """Get catalog of premium content that can be unlocked via ads or bricks."""
    if mode == "kids":
        catalog = [
            {"id": "premium_lesson_advanced_tajweed", "type": "premium_lesson", "title_key": "advanced_tajweed", "cost_bricks": 30, "unlock_via_ad": True},
            {"id": "premium_lesson_quran_stories", "type": "premium_lesson", "title_key": "quran_stories_pack", "cost_bricks": 25, "unlock_via_ad": True},
            {"id": "mosque_golden_minaret", "type": "mosque_part", "title_key": "golden_minaret", "cost_bricks": 50, "unlock_via_ad": True},
            {"id": "mosque_crystal_dome", "type": "mosque_part", "title_key": "crystal_dome", "cost_bricks": 75, "unlock_via_ad": True},
            {"id": "premium_quiz_prophets", "type": "quiz_pack", "title_key": "prophets_quiz_pack", "cost_bricks": 20, "unlock_via_ad": True},
            {"id": "premium_story_companions", "type": "story", "title_key": "companions_stories", "cost_bricks": 35, "unlock_via_ad": True},
            {"id": "mosque_fountain", "type": "mosque_part", "title_key": "mosque_fountain", "cost_bricks": 40, "unlock_via_ad": True},
            {"id": "premium_lesson_arabic_calligraphy", "type": "premium_lesson", "title_key": "arabic_calligraphy", "cost_bricks": 45, "unlock_via_ad": True},
        ]
    else:
        catalog = [
            {"id": "premium_tafsir_detailed", "type": "premium_lesson", "title_key": "detailed_tafsir", "cost_points": 100, "unlock_via_ad": True},
            {"id": "premium_hadith_collection", "type": "premium_lesson", "title_key": "extended_hadith", "cost_points": 80, "unlock_via_ad": True},
            {"id": "premium_fiqh_course", "type": "premium_lesson", "title_key": "fiqh_course", "cost_points": 150, "unlock_via_ad": True},
            {"id": "premium_seerah_deep", "type": "premium_lesson", "title_key": "deep_seerah", "cost_points": 120, "unlock_via_ad": True},
        ]

    return {
        "success": True,
        "mode": mode,
        "catalog": catalog,
    }


# ======================== PARENTAL CONSENT ========================

@router.post("/parental-consent/save")
async def save_parental_consent(data: ParentalConsentRequest):
    """Save parental consent for kids section access."""
    await db.parental_consents.update_one(
        {"user_id": data.user_id},
        {
            "$set": {
                "user_id": data.user_id,
                "consent": data.consent,
                "consented_at": datetime.utcnow().isoformat(),
            }
        },
        upsert=True,
    )
    return {"success": True, "consent": data.consent}


@router.get("/parental-consent/check")
async def check_parental_consent(user_id: str):
    """Check if parental consent has been given for kids section."""
    doc = await db.parental_consents.find_one({"user_id": user_id}, {"_id": 0})
    if doc and doc.get("consent"):
        return {"success": True, "has_consent": True, "consented_at": doc.get("consented_at")}
    return {"success": True, "has_consent": False}


# ======================== DAILY LESSON POINTS (MAX 5/DAY) ========================

@router.post("/points/lesson-complete")
async def earn_lesson_points(data: LessonPointsRequest):
    """Award 1 point for lesson completion. Max 5 lessons per day."""
    today = date.today().isoformat()
    
    # Check daily lesson count
    daily_count = await db.lesson_points_log.count_documents({
        "user_id": data.user_id,
        "date": today,
    })
    
    if daily_count >= 5:
        return {
            "success": False,
            "message": "daily_lesson_limit_reached",
            "points_earned": 0,
            "lessons_today": daily_count,
            "max_daily": 5,
        }
    
    # Log the lesson completion
    await db.lesson_points_log.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": data.user_id,
        "lesson_id": data.lesson_id or str(uuid.uuid4())[:8],
        "date": today,
        "timestamp": datetime.utcnow().isoformat(),
    })
    
    # Award 1 point
    collection = "kids_points" if data.mode == "kids" else "adult_points"
    await db[collection].update_one(
        {"user_id": data.user_id},
        {
            "$inc": {"points": 1, "total_earned": 1},
            "$set": {"last_active": today},
        },
        upsert=True,
    )
    
    # Log transaction
    await db.points_transactions.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": data.user_id,
        "mode": data.mode,
        "type": "lesson_complete",
        "points": 1,
        "metadata": {"lesson_id": data.lesson_id, "daily_count": daily_count + 1},
        "created_at": datetime.utcnow().isoformat(),
    })
    
    profile = await db[collection].find_one({"user_id": data.user_id}, {"_id": 0})
    new_total = profile.get("points", 0) if profile else 1
    
    return {
        "success": True,
        "points_earned": 1,
        "new_total": new_total,
        "lessons_today": daily_count + 1,
        "max_daily": 5,
        "remaining_today": 4 - daily_count,
    }


# ======================== STORE REDEMPTION ITEMS ========================

REDEEM_CATALOG = [
    {
        "id": "ebook_quran_stories",
        "title_ar": "كتاب إلكتروني - قصص القرآن",
        "title_en": "E-Book - Quran Stories",
        "description_ar": "كتاب إلكتروني يحتوي على قصص القرآن الكريم مصورة",
        "description_en": "Illustrated Quran stories e-book",
        "cost": 50,
        "type": "ebook",
        "emoji": "📚",
        "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=200",
    },
    {
        "id": "ebook_prophets",
        "title_ar": "كتاب إلكتروني - قصص الأنبياء",
        "title_en": "E-Book - Prophet Stories",
        "description_ar": "قصص الأنبياء للأطفال مع صور جميلة",
        "description_en": "Prophet stories for children with illustrations",
        "cost": 50,
        "type": "ebook",
        "emoji": "📖",
        "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=200",
    },
    {
        "id": "coupon_10_discount",
        "title_ar": "قسيمة خصم 10%",
        "title_en": "10% Discount Coupon",
        "description_ar": "قسيمة خصم على المنتجات الإسلامية",
        "description_en": "Discount coupon for Islamic products",
        "cost": 100,
        "type": "coupon",
        "emoji": "🎫",
        "image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=200",
    },
    {
        "id": "premium_dua_collection",
        "title_ar": "مجموعة أدعية مميزة",
        "title_en": "Premium Dua Collection",
        "description_ar": "مجموعة شاملة من الأدعية المأثورة مع الترجمة",
        "description_en": "Comprehensive collection of authentic duas with translation",
        "cost": 30,
        "type": "content",
        "emoji": "🤲",
        "image": "https://images.unsplash.com/photo-1609599006353-e629aaabfeae?w=200",
    },
    {
        "id": "premium_ringtones",
        "title_ar": "نغمات إسلامية مميزة",
        "title_en": "Premium Islamic Ringtones",
        "description_ar": "مجموعة نغمات إسلامية جميلة",
        "description_en": "Beautiful Islamic ringtones collection",
        "cost": 75,
        "type": "digital",
        "emoji": "🔔",
        "image": "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?w=200",
    },
]


@router.get("/store/redeem-catalog")
async def get_redeem_catalog(user_id: str = "", locale: str = "ar"):
    """Get catalog of items that can be redeemed with points."""
    redeemed = []
    if user_id:
        docs = await db.redeemed_items.find({"user_id": user_id}, {"_id": 0, "reward_id": 1}).to_list(100)
        redeemed = [d["reward_id"] for d in docs]
    
    items = []
    for item in REDEEM_CATALOG:
        items.append({
            **item,
            "title": item["title_ar"] if locale == "ar" else item["title_en"],
            "description": item["description_ar"] if locale == "ar" else item["description_en"],
            "redeemed": item["id"] in redeemed,
        })
    
    return {"success": True, "items": items}


@router.post("/store/redeem")
async def redeem_reward(data: RedeemRewardRequest):
    """Redeem points for a store reward."""
    # Find the item
    item = next((i for i in REDEEM_CATALOG if i["id"] == data.reward_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if already redeemed
    existing = await db.redeemed_items.find_one({
        "user_id": data.user_id,
        "reward_id": data.reward_id,
    })
    if existing:
        return {"success": False, "message": "already_redeemed"}
    
    # Check points
    collection = "kids_points" if data.mode == "kids" else "adult_points"
    profile = await db[collection].find_one({"user_id": data.user_id}, {"_id": 0})
    
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    current_points = profile.get("points", 0)
    cost = item["cost"]
    
    if current_points < cost:
        return {
            "success": False,
            "message": "insufficient_points",
            "current_points": current_points,
            "cost": cost,
        }
    
    # Deduct points
    await db[collection].update_one(
        {"user_id": data.user_id},
        {"$inc": {"points": -cost}},
    )
    
    # Record redemption
    await db.redeemed_items.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": data.user_id,
        "reward_id": data.reward_id,
        "cost": cost,
        "mode": data.mode,
        "redeemed_at": datetime.utcnow().isoformat(),
    })
    
    # Log transaction
    await db.points_transactions.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": data.user_id,
        "mode": data.mode,
        "type": "redeem",
        "points": -cost,
        "metadata": {"reward_id": data.reward_id, "reward_title": item.get("title_en", "")},
        "created_at": datetime.utcnow().isoformat(),
    })
    
    return {
        "success": True,
        "reward_id": data.reward_id,
        "points_spent": cost,
        "remaining_points": current_points - cost,
    }


# ======================== PREMIUM STORIES ========================

@router.post("/stories/unlock-premium")
async def unlock_premium_story(data: dict):
    """Unlock a premium story by spending points."""
    user_id = data.get("user_id", "")
    story_id = data.get("story_id", "")
    points_cost = data.get("points_cost", 2)
    mode = data.get("mode", "adults")
    
    if not user_id or not story_id:
        raise HTTPException(status_code=400, detail="user_id and story_id required")
    
    # Check if already unlocked
    existing = await db.unlocked_stories.find_one({
        "user_id": user_id,
        "story_id": story_id,
    })
    if existing:
        return {"success": True, "already_unlocked": True}
    
    # Check points
    collection = "kids_points" if mode == "kids" else "adult_points"
    profile = await db[collection].find_one({"user_id": user_id}, {"_id": 0})
    current_points = profile.get("points", 0) if profile else 0
    
    if current_points < points_cost:
        return {
            "success": False,
            "message": "insufficient_points",
            "current_points": current_points,
            "cost": points_cost,
        }
    
    # Deduct points
    await db[collection].update_one(
        {"user_id": user_id},
        {"$inc": {"points": -points_cost}},
    )
    
    # Record unlock
    await db.unlocked_stories.insert_one({
        "user_id": user_id,
        "story_id": story_id,
        "cost": points_cost,
        "unlocked_at": datetime.utcnow().isoformat(),
    })
    
    return {
        "success": True,
        "story_unlocked": story_id,
        "points_spent": points_cost,
        "remaining_points": current_points - points_cost,
    }


@router.get("/stories/check-unlocked")
async def check_unlocked_stories(user_id: str):
    """Check which premium stories user has unlocked."""
    docs = await db.unlocked_stories.find(
        {"user_id": user_id}, {"_id": 0, "story_id": 1}
    ).to_list(500)
    unlocked_ids = [d["story_id"] for d in docs]
    return {"success": True, "unlocked_story_ids": unlocked_ids}
