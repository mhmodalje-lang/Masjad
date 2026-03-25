"""
Router: kids_learn
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
from kids_learning import (
    build_daily_lesson, get_quran_memorization_plan, get_all_duas,
    get_all_hadiths, get_prophet_stories, get_islamic_pillars,
    get_library_categories, get_library_items,
    QURAN_SURAHS_FOR_KIDS, KIDS_DUAS, KIDS_HADITHS, PROPHET_STORIES, 
    ISLAMIC_PILLARS, KIDS_LIBRARY_CATEGORIES, KIDS_LIBRARY_ITEMS,
)
from kids_learning_extended import (
    ALL_PROPHETS, WUDU_STEPS, SALAH_STEPS, ARABIC_ALPHABET,
    ACHIEVEMENT_BADGES, EXTENDED_LIBRARY, EXTENDED_DUAS, EXTENDED_HADITHS,
    get_wudu_steps, get_salah_steps, get_alphabet, get_vocabulary as ext_get_vocabulary,
    get_achievements, get_all_prophets,
)
from kids_curriculum import (
    get_curriculum_overview, generate_lesson, CURRICULUM_STAGES,
)
from kids_curriculum_advanced import ADDITIONAL_SURAHS
from kids_tafsir import get_kids_tafsir, get_surah_kids_tafsir, KIDS_TAFSIR
from quran_api_service import (
    get_kids_surahs_all, get_surah_arabic_and_translation,
    QURAN_EDITIONS, KIDS_SURAH_NUMBERS, prefetch_kids_surahs
)
from kids_games_engine import generate_daily_games
from arabic_course_engine import get_course_overview, get_alphabet_lesson, generate_letter_games, ARABIC_LETTERS

router = APIRouter(tags=["Kids Learn"])

# Surah number to ID mapping
SURAH_ID_MAP = {
    1: "fatiha", 99: "zilzal", 101: "qariah", 102: "takathur",
    103: "asr", 105: "fil", 106: "quraysh", 107: "maun",
    108: "kawthar", 109: "kafiroon", 110: "nasr", 111: "masad",
    112: "ikhlas", 113: "falaq", 114: "nas"
}
SURAH_NAME_MAP = {v: k for k, v in SURAH_ID_MAP.items()}

@router.get("/kids-learn/daily-lesson")
async def get_daily_lesson(day: int = 0, locale: str = "ar"):
    """Get comprehensive daily lesson. If day=0, use today's day of year."""
    if day <= 0:
        day = datetime.now().timetuple().tm_yday
    lesson = build_daily_lesson(day, locale)
    return {"success": True, "lesson": lesson}


@router.get("/kids-learn/quran/surahs")
async def get_quran_surahs_for_kids(locale: str = "ar", background_tasks: BackgroundTasks = None):
    """Get all Quran surahs for kids with OFFICIAL translations from KFGQPC sources."""
    lang = locale if locale in QURAN_EDITIONS else "ar"
    
    try:
        # Try to get from official API (cached in MongoDB)
        api_surahs = await get_kids_surahs_all(lang)
        if api_surahs and len(api_surahs) >= 10:
            # Sort by surah number
            api_surahs.sort(key=lambda x: x.get("number", 0))
            # Inject kids tafsir for each ayah
            for s in api_surahs:
                sid = s.get("id", "")
                if sid in KIDS_TAFSIR:
                    for ayah in s.get("ayahs", []):
                        anum = ayah.get("number", 0)
                        tafsir_text = get_kids_tafsir(sid, anum, lang)
                        if tafsir_text:
                            ayah["tafsir_kids"] = tafsir_text
            return {"success": True, "surahs": api_surahs, "total": len(api_surahs)}
    except Exception as e:
        logger.warning(f"API fetch failed, falling back to local data: {e}")
    
    # Fallback to local data if API fails
    plan = get_quran_memorization_plan(locale)
    for s in ADDITIONAL_SURAHS:
        if not any(p.get("id") == s["id"] for p in plan):
            plan.append({
                "id": s["id"], "number": s["number"],
                "name_ar": s["name_ar"], "name_en": s["name_en"],
                "difficulty": s.get("difficulty", 1), "total_ayahs": s["total_ayahs"],
                "ayahs": [{"number": a["num"], "arabic": a["ar"], "translation": a.get(lang, a.get("en", ""))} for a in s["ayahs"]],
            })
    # Inject kids tafsir
    for s in plan:
        sid = s.get("id", "")
        if sid in KIDS_TAFSIR:
            for ayah in s.get("ayahs", []):
                anum = ayah.get("number", 0)
                tafsir_text = get_kids_tafsir(sid, anum, lang)
                if tafsir_text:
                    ayah["tafsir_kids"] = tafsir_text
    plan.sort(key=lambda x: x.get("number", 0))
    return {"success": True, "surahs": plan, "total": len(plan)}


@router.get("/kids-learn/quran/surah/{surah_id}")
async def get_quran_surah_detail(surah_id: str, locale: str = "ar"):
    """Get specific surah with ayahs - OFFICIAL translation + kids tafsir."""
    lang = locale if locale in QURAN_EDITIONS else "ar"
    
    # Get surah number from ID
    surah_number = SURAH_NAME_MAP.get(surah_id)
    
    if surah_number:
        try:
            # Try official API first
            surah_data = await get_surah_arabic_and_translation(surah_number, lang)
            if surah_data:
                surah_data["id"] = surah_id
                # Inject kids tafsir
                if surah_id in KIDS_TAFSIR:
                    for ayah in surah_data.get("ayahs", []):
                        anum = ayah.get("number", 0)
                        tafsir_text = get_kids_tafsir(surah_id, anum, lang)
                        if tafsir_text:
                            ayah["tafsir_kids"] = tafsir_text
                return {"success": True, "surah": surah_data}
        except Exception as e:
            logger.warning(f"API fetch failed for {surah_id}/{lang}: {e}")
    
    # Fallback to local data
    surah = next((s for s in QURAN_SURAHS_FOR_KIDS if s["id"] == surah_id), None)
    if not surah:
        surah = next((s for s in ADDITIONAL_SURAHS if s["id"] == surah_id), None)
    if not surah:
        raise HTTPException(status_code=404, detail="Surah not found")
    
    ayahs_list = []
    for a in surah["ayahs"]:
        ayah_data = {"number": a["num"], "arabic": a["ar"], "translation": a.get(lang, a.get("en", ""))}
        tafsir_text = get_kids_tafsir(surah["id"], a["num"], lang)
        if tafsir_text:
            ayah_data["tafsir_kids"] = tafsir_text
        ayahs_list.append(ayah_data)
    
    return {
        "success": True,
        "surah": {
            "id": surah["id"], "number": surah["number"],
            "name_ar": surah["name_ar"], "name_en": surah["name_en"],
            "difficulty": surah.get("difficulty", 1), "total_ayahs": surah["total_ayahs"],
            "ayahs": ayahs_list,
        }
    }


@router.get("/kids-learn/duas")
async def get_kids_duas(category: str = "all", locale: str = "ar"):
    """Get all kids duas, optionally filtered by category."""
    all_duas = get_all_duas(locale)
    if category != "all":
        all_duas = [d for d in all_duas if d["category"] == category]
    categories = list(set(d["category"] for d in KIDS_DUAS))
    return {"success": True, "duas": all_duas, "total": len(all_duas), "categories": categories}


@router.get("/kids-learn/hadiths")
async def get_kids_hadiths(category: str = "all", locale: str = "ar"):
    """Get all kids hadiths with simplified explanations."""
    all_hadiths = get_all_hadiths(locale)
    if category != "all":
        all_hadiths = [h for h in all_hadiths if h["category"] == category]
    categories = list(set(h["category"] for h in KIDS_HADITHS))
    return {"success": True, "hadiths": all_hadiths, "total": len(all_hadiths), "categories": categories}


@router.get("/kids-learn/prophets")
async def get_kids_prophets(locale: str = "ar"):
    """Get all prophet stories for kids."""
    stories = get_prophet_stories(locale)
    return {"success": True, "prophets": stories, "total": len(stories)}


@router.get("/kids-learn/prophets/{prophet_id}")
async def get_prophet_detail(prophet_id: str, locale: str = "ar"):
    """Get specific prophet story detail. NO English fallback - uses Arabic."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "ar"
    prophet = next((p for p in PROPHET_STORIES if p["id"] == prophet_id), None)
    if not prophet:
        raise HTTPException(status_code=404, detail="Prophet story not found")
    return {
        "success": True,
        "prophet": {
            "id": prophet["id"], "number": prophet["number"], "emoji": prophet["emoji"],
            "name": prophet["name"].get(lang, prophet["name"].get("ar", "")),
            "title": prophet["title"].get(lang, prophet["title"].get("ar", "")),
            "summary": prophet["summary"].get(lang, prophet["summary"].get("ar", "")),
            "lesson": prophet["lesson"].get(lang, prophet["lesson"].get("ar", "")),
            "quran_ref": prophet["quran_ref"],
        }
    }


@router.get("/kids-learn/islamic-pillars")
async def get_kids_islamic_pillars(locale: str = "ar"):
    """Get the 5 pillars of Islam for kids."""
    pillars = get_islamic_pillars(locale)
    return {"success": True, "pillars": pillars, "total": len(pillars)}


@router.get("/kids-learn/library/categories")
async def get_kids_library_categories(locale: str = "ar"):
    """Get all kids library categories."""
    cats = get_library_categories(locale)
    return {"success": True, "categories": cats, "total": len(cats)}


@router.get("/kids-learn/library/items")
async def get_kids_library_items(category: str = "all", locale: str = "ar"):
    """Get library items, optionally filtered by category."""
    items = get_library_items(category, locale)
    return {"success": True, "items": items, "total": len(items)}


@router.post("/kids-learn/progress")
async def save_kids_learn_progress(payload: dict):
    """Save kids learning progress."""
    user_id = payload.get("user_id", "guest")
    day = payload.get("day", 0)
    sections_completed = payload.get("sections_completed", [])
    
    # Update or create progress record
    prog = await db.kids_learn_progress.find_one({"user_id": user_id})
    if not prog:
        prog = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "completed_days": [],
            "total_lessons": 0,
            "streak": 0,
            "longest_streak": 0,
            "memorized_surahs": [],
            "memorized_ayahs": 0,
            "learned_duas": [],
            "learned_hadiths": [],
            "xp": 0,
            "created_at": datetime.utcnow().isoformat(),
        }
        await db.kids_learn_progress.insert_one(prog)
    
    completed_days = prog.get("completed_days", [])
    if day not in completed_days:
        completed_days.append(day)
    
    # Calculate streak
    streak = prog.get("streak", 0) + 1
    longest = max(streak, prog.get("longest_streak", 0))
    
    xp_earned = len(sections_completed) * 10
    
    update = {
        "$set": {
            "completed_days": completed_days,
            "streak": streak,
            "longest_streak": longest,
        },
        "$inc": {
            "total_lessons": 1,
            "xp": xp_earned,
            "memorized_ayahs": 1 if "quran" in sections_completed else 0,
        }
    }
    
    # Track learned duas and hadiths
    if "dua" in sections_completed:
        dua_id = payload.get("dua_id", "")
        if dua_id:
            update.setdefault("$addToSet", {})["learned_duas"] = dua_id
    if "hadith" in sections_completed:
        hadith_id = payload.get("hadith_id", "")
        if hadith_id:
            update.setdefault("$addToSet", {})["learned_hadiths"] = hadith_id
    
    await db.kids_learn_progress.update_one({"user_id": user_id}, update)
    
    return {
        "success": True,
        "xp_earned": xp_earned,
        "total_days": len(completed_days),
        "streak": streak,
    }


@router.get("/kids-learn/progress")
async def get_kids_learn_progress(user_id: str = "guest"):
    """Get kids learning progress."""
    prog = await db.kids_learn_progress.find_one({"user_id": user_id}, {"_id": 0})
    if not prog:
        prog = {
            "user_id": user_id,
            "completed_days": [],
            "total_lessons": 0,
            "streak": 0,
            "longest_streak": 0,
            "memorized_surahs": [],
            "memorized_ayahs": 0,
            "learned_duas": [],
            "learned_hadiths": [],
            "xp": 0,
        }
    return {"success": True, "progress": prog}


# ==================== CURRICULUM ENGINE API ====================

@router.get("/kids-learn/curriculum")
async def api_curriculum_overview(locale: str = "en"):
    """Get the full 1000-day curriculum overview with 15 stages."""
    data = get_curriculum_overview(locale)
    return {"success": True, **data}


@router.get("/kids-learn/curriculum/lesson/{day}")
async def api_curriculum_lesson(day: int, locale: str = "en"):
    """Get a structured lesson for a specific day (1-1000)."""
    if day < 1 or day > 1000:
        raise HTTPException(status_code=400, detail="Day must be between 1 and 1000")
    lesson = generate_lesson(day, locale)
    return {"success": True, "lesson": lesson}


@router.get("/kids-learn/wudu")
async def api_wudu_steps(locale: str = "ar"):
    """Get Wudu (ablution) steps for kids."""
    steps = get_wudu_steps(locale)
    return {"success": True, "steps": steps, "total": len(steps)}


@router.get("/kids-learn/salah")
async def api_salah_steps(locale: str = "ar"):
    """Get Salah (prayer) steps for kids."""
    steps = get_salah_steps(locale)
    return {"success": True, "steps": steps, "total": len(steps)}


@router.get("/kids-learn/alphabet")
async def api_arabic_alphabet():
    """Get the full Arabic alphabet course."""
    letters = get_alphabet()
    return {"success": True, "letters": letters, "total": len(letters)}


@router.get("/kids-learn/vocabulary/{category}")
async def api_arabic_vocabulary(category: str):
    """Get Arabic vocabulary by category: numbers, colors, animals, body, family."""
    vocab = ext_get_vocabulary(category)
    if not vocab:
        raise HTTPException(status_code=404, detail="Category not found. Use: numbers, colors, animals, body, family")
    return {"success": True, "items": vocab, "total": len(vocab), "category": category}


@router.get("/kids-learn/achievements")
async def api_achievements(user_id: str = "guest"):
    """Get user's earned achievement badges."""
    prog = await db.kids_learn_progress.find_one({"user_id": user_id}, {"_id": 0})
    if not prog:
        prog = {"total_lessons": 0, "streak": 0, "memorized_ayahs": 0, "learned_duas": [], "learned_hadiths": [], "xp": 0}
    lang = "en"
    earned = get_achievements(prog)
    all_badges = [{"id": b["id"], "emoji": b["emoji"],
                   "title_ar": b["title_ar"], "title_en": b["title_en"],
                   "title_de": b.get("title_de",""), "title_fr": b.get("title_fr",""),
                   "title_tr": b.get("title_tr",""), "title_ru": b.get("title_ru",""),
                   "title_sv": b.get("title_sv",""), "title_nl": b.get("title_nl",""),
                   "title_el": b.get("title_el",""),
                   "desc_ar": b["desc_ar"], "desc_en": b["desc_en"],
                   "earned": any(e["id"] == b["id"] for e in earned)} for b in ACHIEVEMENT_BADGES]
    return {"success": True, "badges": all_badges, "earned_count": len(earned), "total": len(ACHIEVEMENT_BADGES)}


@router.get("/kids-learn/prophets-full")
async def api_all_25_prophets(locale: str = "ar"):
    """Get all 25 prophets mentioned in Quran."""
    prophets = get_all_prophets(locale)
    return {"success": True, "prophets": prophets, "total": len(prophets)}


@router.post("/kids-learn/curriculum/progress")
async def save_curriculum_progress(payload: dict):
    """Save curriculum progress for a specific day."""
    user_id = payload.get("user_id", "guest")
    day = payload.get("day", 0)
    sections_done = payload.get("sections_done", 0)
    total_sections = payload.get("total_sections", 1)
    xp_reward = payload.get("xp_reward", 10)
    
    prog = await db.kids_curriculum_progress.find_one({"user_id": user_id})
    if not prog:
        prog = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "current_day": 1,
            "completed_days": [],
            "total_xp": 0,
            "streak": 0,
            "longest_streak": 0,
            "stage_progress": {},
            "created_at": datetime.utcnow().isoformat(),
        }
        await db.kids_curriculum_progress.insert_one(prog)
    
    completed = prog.get("completed_days", [])
    if day not in completed:
        completed.append(day)
    
    current = max(completed) + 1 if completed else 1
    streak = prog.get("streak", 0) + 1
    longest = max(streak, prog.get("longest_streak", 0))
    
    await db.kids_curriculum_progress.update_one(
        {"user_id": user_id},
        {"$set": {
            "completed_days": completed,
            "current_day": min(current, 1000),
            "streak": streak,
            "longest_streak": longest,
        }, "$inc": {"total_xp": xp_reward}}
    )
    
    return {
        "success": True,
        "current_day": min(current, 1000),
        "total_completed": len(completed),
        "total_xp": prog.get("total_xp", 0) + xp_reward,
        "streak": streak,
        "xp_earned": xp_reward,
    }


@router.get("/kids-learn/curriculum/progress")
async def get_curriculum_progress(user_id: str = "guest"):
    """Get curriculum progress."""
    prog = await db.kids_curriculum_progress.find_one({"user_id": user_id}, {"_id": 0})
    if not prog:
        prog = {
            "user_id": user_id, "current_day": 1, "completed_days": [],
            "total_xp": 0, "streak": 0, "longest_streak": 0,
        }
    return {"success": True, "progress": prog}




# ═══════════════════════════════════════════════════════════════
# DIGITAL SHIELD — AI Awareness, Privacy for Girls, Modern Ethics
# ═══════════════════════════════════════════════════════════════

_DIGITAL_SHIELD_CACHE = None

def _load_digital_shield():
    global _DIGITAL_SHIELD_CACHE
    if _DIGITAL_SHIELD_CACHE is None:
        import os
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'daily_lessons.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                _DIGITAL_SHIELD_CACHE = json_module.load(f)
        except Exception as e:
            logger.error(f"Failed to load digital shield lessons: {e}")
            _DIGITAL_SHIELD_CACHE = []
    return _DIGITAL_SHIELD_CACHE


@router.get("/kids-learn/digital-shield")
async def get_digital_shield_lessons(locale: str = "en", theme: str = "all"):
    """Get all Digital Shield lessons (30 lessons on AI awareness, privacy, ethics)."""
    lessons = _load_digital_shield()
    result = []
    for lesson in lessons:
        lang = locale if locale in lesson.get("title", {}) else "en"
        item = {
            "id": lesson["id"],
            "theme": lesson.get("theme", "general"),
            "icon": lesson.get("icon", "shield"),
            "title": lesson["title"].get(lang, lesson["title"].get("en", "")),
            "content": lesson["content"].get(lang, lesson["content"].get("en", "")),
            "key_lesson": lesson["key_lesson"].get(lang, lesson["key_lesson"].get("en", "")),
        }
        if theme == "all" or item["theme"] == theme:
            result.append(item)
    return {"success": True, "lessons": result, "total": len(result)}


@router.get("/kids-learn/digital-shield/today")
async def get_today_digital_shield(locale: str = "en"):
    """Get today's Digital Shield lesson (rotates daily)."""
    from datetime import datetime
    lessons = _load_digital_shield()
    if not lessons:
        return {"success": False, "error": "No lessons available"}
    day_of_year = datetime.now().timetuple().tm_yday
    idx = (day_of_year - 1) % len(lessons)
    lesson = lessons[idx]
    lang = locale if locale in lesson.get("title", {}) else "en"
    return {
        "success": True,
        "lesson": {
            "id": lesson["id"],
            "theme": lesson.get("theme", "general"),
            "icon": lesson.get("icon", "shield"),
            "title": lesson["title"].get(lang, lesson["title"].get("en", "")),
            "content": lesson["content"].get(lang, lesson["content"].get("en", "")),
            "key_lesson": lesson["key_lesson"].get(lang, lesson["key_lesson"].get("en", "")),
        },
        "lesson_number": idx + 1,
        "total_lessons": len(lessons),
    }


@router.get("/kids-learn/digital-shield/themes")
async def get_digital_shield_themes(locale: str = "en"):
    """Get list of Digital Shield themes with lesson counts."""
    lessons = _load_digital_shield()
    theme_map = {}
    for lesson in lessons:
        t = lesson.get("theme", "general")
        if t not in theme_map:
            theme_map[t] = 0
        theme_map[t] += 1
    
    theme_icons = {
        "deepfakes": "shield-alert",
        "privacy": "lock",
        "social_media": "heart-off",
        "misinformation": "search",
        "ethics": "scale",
        "safety": "shield-check",
    }
    
    themes = [
        {"id": t, "count": c, "icon": theme_icons.get(t, "shield")}
        for t, c in theme_map.items()
    ]
    return {"success": True, "themes": themes}



# ═══════════════════════════════════════════════════════════════
# GAME ENGINE — Interactive Daily Games for Noor Academy
# ═══════════════════════════════════════════════════════════════

@router.get("/kids-learn/daily-games")
async def get_daily_games(locale: str = "en", day: int = 0):
    """Get today's set of interactive games (or a specific day's games)."""
    if day <= 0:
        from datetime import datetime
        day = datetime.now().timetuple().tm_yday
    
    try:
        games_data = generate_daily_games(day, locale)
        return {"success": True, **games_data}
    except Exception as e:
        logger.error(f"Error generating daily games: {e}")
        return {"success": False, "error": str(e)}


@router.get("/kids-learn/game/{day}")
async def get_game_by_day(day: int, locale: str = "en"):
    """Get games for a specific day number (1-365)."""
    if day < 1 or day > 365:
        return {"success": False, "error": "Day must be between 1 and 365"}
    games_data = generate_daily_games(day, locale)
    return {"success": True, **games_data}


class GameResultPayload(BaseModel):
    user_id: str
    game_id: str
    day: int
    score: int
    max_score: int
    xp_earned: int
    time_seconds: int = 0


@router.post("/kids-learn/game-result")
async def save_game_result(payload: GameResultPayload):
    """Save a game result and update streaks/XP."""
    coll = db["kids_game_results"]
    today_str = date.today().isoformat()
    
    result = {
        "id": str(uuid.uuid4()),
        "user_id": payload.user_id,
        "game_id": payload.game_id,
        "day": payload.day,
        "score": payload.score,
        "max_score": payload.max_score,
        "xp_earned": payload.xp_earned,
        "time_seconds": payload.time_seconds,
        "date": today_str,
        "created_at": datetime.utcnow().isoformat(),
    }
    await coll.insert_one(result)
    
    # Update user profile: XP + streak
    profile_coll = db["kids_profiles"]
    profile = await profile_coll.find_one({"user_id": payload.user_id})
    if not profile:
        profile = {
            "user_id": payload.user_id,
            "total_xp": 0,
            "level": 1,
            "streak_days": 0,
            "last_active_date": "",
            "games_completed": 0,
            "badges": [],
            "coins": 0,
            "created_at": datetime.utcnow().isoformat(),
        }
        await profile_coll.insert_one(profile)
    
    # Update XP
    new_xp = profile.get("total_xp", 0) + payload.xp_earned
    new_level = 1 + new_xp // 100  # Level up every 100 XP
    new_games = profile.get("games_completed", 0) + 1
    
    # Update streak
    last_date = profile.get("last_active_date", "")
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    if last_date == today_str:
        new_streak = profile.get("streak_days", 0)
    elif last_date == yesterday:
        new_streak = profile.get("streak_days", 0) + 1
    else:
        new_streak = 1
    
    await profile_coll.update_one(
        {"user_id": payload.user_id},
        {"$set": {
            "total_xp": new_xp,
            "level": new_level,
            "streak_days": new_streak,
            "last_active_date": today_str,
            "games_completed": new_games,
        }}
    )
    
    return {
        "success": True,
        "xp_earned": payload.xp_earned,
        "total_xp": new_xp,
        "level": new_level,
        "streak_days": new_streak,
        "games_completed": new_games,
    }


@router.get("/kids-learn/profile/{user_id}")
async def get_kid_profile(user_id: str):
    """Get a kid's game profile with stats."""
    profile_coll = db["kids_profiles"]
    profile = await profile_coll.find_one({"user_id": user_id})
    if not profile:
        profile = {
            "user_id": user_id,
            "total_xp": 0,
            "level": 1,
            "streak_days": 0,
            "last_active_date": "",
            "games_completed": 0,
            "badges": [],
            "coins": 0,
        }
    
    # Check streak validity
    today_str = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    last_date = profile.get("last_active_date", "")
    if last_date not in [today_str, yesterday] and last_date != "":
        profile["streak_days"] = 0  # Streak broken
    
    # Remove mongo _id
    profile.pop("_id", None)
    
    return {"success": True, "profile": profile}


@router.post("/kids-learn/reward-ad")
async def reward_ad_watched(user_id: str, coins: int = 10):
    """Reward coins for watching an ad."""
    profile_coll = db["kids_profiles"]
    profile = await profile_coll.find_one({"user_id": user_id})
    if not profile:
        return {"success": False, "error": "Profile not found"}
    
    new_coins = profile.get("coins", 0) + coins
    await profile_coll.update_one(
        {"user_id": user_id},
        {"$set": {"coins": new_coins}}
    )
    
    return {"success": True, "coins": new_coins, "earned": coins}



# ═══════════════════════════════════════════════════════════════
# ARABIC & QURAN COURSE — Comprehensive Learning Path (0 → C1)
# ═══════════════════════════════════════════════════════════════

@router.get("/kids-learn/course/overview")
async def course_overview(locale: str = "en"):
    """Get the full Arabic & Quran course structure (Foundation → C1)."""
    levels = get_course_overview(locale)
    return {"success": True, "levels": levels, "total_levels": len(levels)}


@router.get("/kids-learn/course/alphabet")
async def course_alphabet(locale: str = "en"):
    """Get all 28 Arabic letters with forms and examples."""
    lang = locale if locale != "de-AT" else "de"
    letters = []
    for i, lt in enumerate(ARABIC_LETTERS):
        letters.append({
            "index": i,
            "letter": lt["letter"],
            "name": lt["transliteration"].get(lang, lt["transliteration"].get("en", lt["name"])),
            "sound": lt["sound"],
            "forms": lt["forms"],
            "emoji": lt["emoji"],
            "word_ar": lt["word"]["ar"],
            "word_en": lt["word"].get(lang, lt["word"]["en"]),
        })
    return {"success": True, "letters": letters, "total": len(letters)}


@router.get("/kids-learn/course/alphabet/{index}")
async def course_alphabet_letter(index: int, locale: str = "en"):
    """Get a specific letter lesson with games."""
    lesson = get_alphabet_lesson(index, locale)
    if not lesson:
        return {"success": False, "error": "Invalid letter index"}
    games = generate_letter_games(index, locale)
    return {"success": True, "lesson": lesson, "games": games}


# ═══════════════════════════════════════════════════════════════
# NOOR ACADEMY V2 — Modern Islamic Education Platform (2026)
# ═══════════════════════════════════════════════════════════════

from data.noor_academy_v2 import (
    ACADEMY_TRACKS, NOORANIYA_LEVELS,
    AQEEDAH_LEVELS, FIQH_LEVELS, SEERAH_LEVELS,
    TEACHING_METHODS, ACADEMY_BADGES,
)
# Import expanded lesson data (30 Nooraniya + 20 Adab)
from data.noor_academy_v2 import NOORANIYA_ALL_LESSONS as NOORANIYA_LESSONS
from data.noor_academy_v2 import ADAB_ALL_LESSONS as ADAB_LESSONS

SUPPORTED_LANGS = ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"]

def _resolve_lang(locale: str) -> str:
    if locale == "de-AT":
        return "de"
    return locale if locale in SUPPORTED_LANGS else "en"

def _t(obj, lang: str, fallback: str = "en"):
    """Translate a multilingual dict to the target language."""
    if isinstance(obj, dict):
        return obj.get(lang, obj.get(fallback, ""))
    return obj


@router.get("/kids-learn/academy/overview")
async def academy_overview(locale: str = "ar"):
    """Get Noor Academy V2 overview — all 5 learning tracks."""
    lang = _resolve_lang(locale)
    tracks = []
    for t in ACADEMY_TRACKS:
        tracks.append({
            "id": t["id"],
            "emoji": t["emoji"],
            "color": t["color"],
            "icon": t["icon"],
            "order": t["order"],
            "title": _t(t["title"], lang),
            "description": _t(t["desc"], lang),
            "total_levels": t["total_levels"],
            "total_lessons": t["total_lessons"],
            "age_range": t["age_range"],
            "method": t["method"],
        })
    return {
        "success": True,
        "academy_name": _t({"ar": "أكاديمية نور ٢.٠", "en": "Noor Academy 2.0", "de": "Noor Akademie 2.0", "fr": "Académie Noor 2.0", "tr": "Noor Akademi 2.0", "ru": "Академия Нур 2.0", "sv": "Noor Akademi 2.0", "nl": "Noor Academie 2.0", "el": "Ακαδημία Νουρ 2.0"}, lang),
        "tagline": _t({"ar": "أحدث أساليب التعليم ٢٠٢٦ — من الصفر حتى الإتقان", "en": "Modern 2026 Teaching Methods — From Zero to Mastery", "de": "Moderne Lehrmethoden 2026 — Von Null bis zur Meisterschaft", "fr": "Méthodes modernes 2026 — De zéro à la maîtrise", "tr": "2026 Modern Öğretim Yöntemleri — Sıfırdan Ustalığa", "ru": "Современные методы обучения 2026 — От нуля до мастерства", "sv": "Moderna undervisningsmetoder 2026 — Från noll till mästerskap", "nl": "Moderne lesmethoden 2026 — Van nul tot meesterschap", "el": "Σύγχρονες μέθοδοι 2026 — Από το μηδέν ως την κατάκτηση"}, lang),
        "tracks": tracks,
        "total_tracks": len(tracks),
        "teaching_methods": [{
            "id": k, "icon": v["icon"],
            "name": _t(v, lang),
        } for k, v in TEACHING_METHODS.items()],
        "badges": [{
            "id": b["id"], "emoji": b["emoji"],
            "title": _t(b["title"], lang),
        } for b in ACADEMY_BADGES],
        "language": lang,
    }


@router.get("/kids-learn/academy/track/{track_id}")
async def academy_track_detail(track_id: str, locale: str = "ar"):
    """Get detailed info for a specific learning track."""
    lang = _resolve_lang(locale)
    track = next((t for t in ACADEMY_TRACKS if t["id"] == track_id), None)
    if not track:
        return {"success": False, "error": f"Track '{track_id}' not found. Valid: nooraniya, aqeedah, fiqh, seerah, adab"}

    levels_data = {
        "nooraniya": NOORANIYA_LEVELS,
        "aqeedah": AQEEDAH_LEVELS,
        "fiqh": FIQH_LEVELS,
        "seerah": SEERAH_LEVELS,
        "adab": [{"level": i+1, "emoji": l["emoji"], "title": l["title"], "lessons": 1} for i, l in enumerate(ADAB_LESSONS)],
    }

    levels = []
    raw_levels = levels_data.get(track_id, [])
    for lv in raw_levels:
        lvl = {
            "level": lv["level"],
            "emoji": lv["emoji"],
            "title": _t(lv["title"], lang),
            "lessons": lv.get("lessons", 1),
        }
        if "color" in lv:
            lvl["color"] = lv["color"]
        if "desc" in lv:
            lvl["description"] = _t(lv["desc"], lang)
        if "skills" in lv:
            lvl["skills"] = lv["skills"]
        levels.append(lvl)

    return {
        "success": True,
        "track": {
            "id": track["id"],
            "emoji": track["emoji"],
            "color": track["color"],
            "title": _t(track["title"], lang),
            "description": _t(track["desc"], lang),
            "method": track["method"],
            "age_range": track["age_range"],
        },
        "levels": levels,
        "total_levels": len(levels),
        "language": lang,
    }


@router.get("/kids-learn/academy/nooraniya/lesson/{lesson_id}")
async def academy_nooraniya_lesson(lesson_id: int, locale: str = "ar"):
    """Get a specific Nooraniya lesson (1-70)."""
    lang = _resolve_lang(locale)
    lesson = next((l for l in NOORANIYA_LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        return {"success": False, "error": f"Nooraniya lesson {lesson_id} not found"}

    level_info = next((lv for lv in NOORANIYA_LEVELS if lv["level"] == lesson["level"]), None)

    result = {
        "id": lesson["id"],
        "level": lesson["level"],
        "level_title": _t(level_info["title"], lang) if level_info else "",
        "lesson_in_level": lesson["lesson"],
        "emoji": lesson["emoji"],
        "title": _t(lesson["title"], lang),
        "method": lesson["method"],
        "method_info": {
            "icon": TEACHING_METHODS.get(lesson["method"], {}).get("icon", "📖"),
            "name": _t(TEACHING_METHODS.get(lesson["method"], {}), lang),
        },
        "xp": lesson.get("xp", 15),
    }

    # Translate content
    content = lesson.get("content", {})
    translated_content = {}
    for key, val in content.items():
        if isinstance(val, dict) and ("ar" in val or "en" in val):
            translated_content[key] = _t(val, lang)
        elif isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
            translated_content[key] = [
                {k: _t(v, lang) if isinstance(v, dict) and ("ar" in v or "en" in v) else v for k, v in item.items()}
                for item in val
            ]
        else:
            translated_content[key] = val
    result["content"] = translated_content

    # Translate quiz
    quiz = lesson.get("quiz", {})
    result["quiz"] = {
        "type": quiz.get("type", ""),
        "question": _t(quiz.get("question", {}), lang),
        "correct": quiz.get("correct"),
        "options": quiz.get("options", []),
    }

    return {
        "success": True,
        "lesson": result,
        "has_next": lesson_id < len(NOORANIYA_LESSONS),
        "has_prev": lesson_id > 1,
        "language": lang,
    }


@router.get("/kids-learn/academy/adab")
async def academy_adab_list(locale: str = "ar"):
    """Get all 10 Islamic manners (Adab) lessons."""
    lang = _resolve_lang(locale)
    lessons = []
    for adab in ADAB_LESSONS:
        lessons.append({
            "id": adab["id"],
            "emoji": adab["emoji"],
            "title": _t(adab["title"], lang),
            "rules_count": len(adab["rules"].get(lang, adab["rules"].get("en", []))),
        })
    return {
        "success": True,
        "title": _t({"ar": "الآداب الإسلامية", "en": "Islamic Manners", "de": "Islamische Umgangsformen", "fr": "Bonnes manières islamiques", "tr": "İslami Adap", "ru": "Исламские манеры", "sv": "Islamiska seder", "nl": "Islamitische manieren", "el": "Ισλαμικοί τρόποι"}, lang),
        "lessons": lessons,
        "total": len(lessons),
        "language": lang,
    }


@router.get("/kids-learn/academy/adab/{adab_id}")
async def academy_adab_detail(adab_id: int, locale: str = "ar"):
    """Get a specific Adab lesson detail."""
    lang = _resolve_lang(locale)
    adab = next((a for a in ADAB_LESSONS if a["id"] == adab_id), None)
    if not adab:
        return {"success": False, "error": f"Adab lesson {adab_id} not found"}

    return {
        "success": True,
        "adab": {
            "id": adab["id"],
            "emoji": adab["emoji"],
            "title": _t(adab["title"], lang),
            "rules": adab["rules"].get(lang, adab["rules"].get("en", [])),
            "hadith": _t(adab["hadith"], lang),
        },
        "has_next": adab_id < len(ADAB_LESSONS),
        "has_prev": adab_id > 1,
        "language": lang,
    }
