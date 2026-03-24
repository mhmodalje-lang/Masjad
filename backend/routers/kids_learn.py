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

QURAN_V4_BASE = "https://api.quran.com/api/v4"
KIDS_TRANSLATION_IDS = {
    "en": 20, "fr": 31, "de": 27, "tr": 77, "ru": 79,
    "nl": 235, "sv": 48, "ar": 16,
}

router = APIRouter(tags=["Kids Learn"])

@router.get("/kids-learn/daily-lesson")
async def get_daily_lesson(day: int = 0, locale: str = "ar"):
    """Get comprehensive daily lesson. If day=0, use today's day of year."""
    if day <= 0:
        day = datetime.now().timetuple().tm_yday
    lesson = build_daily_lesson(day, locale)
    return {"success": True, "lesson": lesson}


@router.get("/kids-learn/quran/surahs")
async def get_quran_surahs_for_kids(locale: str = "ar"):
    """Get all Quran surahs available for kids memorization."""
    plan = get_quran_memorization_plan(locale)
    # Add additional surahs from advanced curriculum
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    for s in ADDITIONAL_SURAHS:
        if not any(p.get("id") == s["id"] for p in plan):
            plan.append({
                "id": s["id"], "number": s["number"],
                "name_ar": s["name_ar"], "name_en": s["name_en"],
                "difficulty": s["difficulty"], "total_ayahs": s["total_ayahs"],
            })
    plan.sort(key=lambda x: x["number"])
    return {"success": True, "surahs": plan, "total": len(plan)}


@router.get("/kids-learn/quran/surah/{surah_id}")
async def get_quran_surah_detail(surah_id: str, locale: str = "ar"):
    """Get specific surah with ayahs — translations fetched from Quran.com v4 API."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    surah = next((s for s in QURAN_SURAHS_FOR_KIDS if s["id"] == surah_id), None)
    if not surah:
        surah = next((s for s in ADDITIONAL_SURAHS if s["id"] == surah_id), None)
    if not surah:
        raise HTTPException(status_code=404, detail="Surah not found")
    
    chapter_num = surah["number"]
    
    # Fetch translation from Quran.com v4 API
    trans_id = KIDS_TRANSLATION_IDS.get(lang)
    api_translations = {}
    
    if trans_id and lang != "ar":
        try:
            async with httpx.AsyncClient(timeout=15) as c:
                r = await c.get(f"{QURAN_V4_BASE}/quran/translations/{trans_id}", params={"chapter_number": chapter_num})
                if r.status_code == 200:
                    data = r.json()
                    for i, t in enumerate(data.get("translations", [])):
                        raw = t.get("text", "")
                        # Strip HTML tags
                        clean = re.sub(r'<sup[^>]*>.*?</sup>', '', raw)
                        clean = re.sub(r'<[^>]*>', '', clean).replace("&nbsp;", " ").strip()
                        api_translations[i + 1] = clean
        except Exception as e:
            logger.warning(f"Kids Quran API fetch failed for surah {chapter_num}: {e}")
    elif lang == "ar":
        # Fetch Muyassar tafsir for Arabic
        try:
            async with httpx.AsyncClient(timeout=15) as c:
                r = await c.get(f"{QURAN_V4_BASE}/tafsirs/16/by_chapter/{chapter_num}")
                if r.status_code == 200:
                    data = r.json()
                    for t in data.get("tafsirs", []):
                        verse_key = t.get("verse_key", "")
                        if verse_key:
                            ayah_num = int(verse_key.split(":")[1])
                            raw = t.get("text", "")
                            clean = re.sub(r'<[^>]*>', '', raw).replace("&nbsp;", " ").strip()
                            api_translations[ayah_num] = clean
        except Exception as e:
            logger.warning(f"Kids Quran Muyassar fetch failed for surah {chapter_num}: {e}")
    
    # Fetch tafsir/explanation from Quran.com v4 API
    TAFSIR_IDS = {"ar": 16, "en": 169, "ru": 170}
    tafsir_id = TAFSIR_IDS.get(lang, 16)  # fallback to Arabic Muyassar
    api_tafsirs = {}
    
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{QURAN_V4_BASE}/tafsirs/{tafsir_id}/by_chapter/{chapter_num}")
            if r.status_code == 200:
                data = r.json()
                for t in data.get("tafsirs", []):
                    verse_key = t.get("verse_key", "")
                    if verse_key:
                        ayah_num = int(verse_key.split(":")[1])
                        raw = t.get("text", "")
                        clean = re.sub(r'<[^>]*>', '', raw).replace("&nbsp;", " ").strip()
                        api_tafsirs[ayah_num] = clean
    except Exception as e:
        logger.warning(f"Kids Quran tafsir fetch failed for surah {chapter_num}: {e}")
    
    # Build ayahs with API translations + tafsir
    ayahs = []
    for a in surah["ayahs"]:
        ayah_num = a["num"]
        translation = api_translations.get(ayah_num)
        if not translation:
            # Fallback to hardcoded text if API fails
            translation = a.get(lang, a.get("en", ""))
        if not translation and lang == "el":
            translation = a.get("el", "Η μετάφραση έρχεται σύντομα")
        
        tafsir_text = api_tafsirs.get(ayah_num, "")
        
        ayahs.append({
            "number": ayah_num,
            "arabic": a["ar"],
            "translation": translation or "",
            "tafsir": tafsir_text,
        })
    
    return {
        "success": True,
        "surah": {
            "id": surah["id"], "number": surah["number"],
            "name_ar": surah["name_ar"], "name_en": surah["name_en"],
            "difficulty": surah["difficulty"], "total_ayahs": surah["total_ayahs"],
            "ayahs": ayahs,
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
    """Get specific prophet story detail."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    prophet = next((p for p in PROPHET_STORIES if p["id"] == prophet_id), None)
    if not prophet:
        raise HTTPException(status_code=404, detail="Prophet story not found")
    return {
        "success": True,
        "prophet": {
            "id": prophet["id"], "number": prophet["number"], "emoji": prophet["emoji"],
            "name": prophet["name"].get(lang, prophet["name"]["en"]),
            "title": prophet["title"].get(lang, prophet["title"]["en"]),
            "summary": prophet["summary"].get(lang, prophet["summary"]["en"]),
            "lesson": prophet["lesson"].get(lang, prophet["lesson"]["en"]),
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


